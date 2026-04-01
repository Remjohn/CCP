"""
FR-VIS-17 — Identity LoRA Training Pipeline
Build Step 30 · DEP-VIS-011, DEP-VIS-014

Photo curation pipeline, training config builder, 5-metric validation,
auto-retry, EFS deployment, versioning, trigger token registry.

§10 Testing: Curation, trigger token uniqueness, config generation,
adversarial photos, LoRA size limit.
"""

from __future__ import annotations

import hashlib
import re
import uuid
from datetime import datetime, timezone
from typing import Any

from core.commercial_models import build_receipt, compute_receipt_hash
from core.visual_models import (
    EXPRESSION_NEUTRALITY_THRESHOLD,
    IDENTITY_LORA_DEFAULT_WEIGHT,
    IDENTITY_SCORE_THRESHOLD,
    MAX_TRAINING_RETRIES,
    RECEIPT_STAGE_LORA_DEPLOY,
    RECEIPT_STAGE_LORA_TRAINING_COMPLETE,
    RECEIPT_STAGE_LORA_TRAINING_START,
    RECEIPT_STAGE_PHOTO_CURATION,
    STYLE_FLEXIBILITY_MIN_PASS,
    CurationResult,
    IdentityLoRAEntry,
    LoRAStatus,
    TrainingJobRow,
    TrainingJobStatus,
    ValidationReport,
    VisualPipelineError,
)


# =====================================================
#  Photo Curation Pipeline (§4 Stage 1)
# =====================================================

class PhotoCurationPipeline:
    """
    §4 Stage 1: Reference Photo Submission & Curation.
    Background removal → auto-captioning → quality filter → trigger token injection.
    """

    MIN_PHOTOS = 15
    MAX_PHOTOS = 30
    MIN_RESOLUTION = 512
    MIN_FACE_CONFIDENCE = 0.85
    REJECTION_CRITERIA = {"sunglasses", "group_photo", "low_resolution", "motion_blur", "no_face"}

    def __init__(self) -> None:
        self._receipts: list[dict] = []
        self._last_receipt_hash = ""

    def curate(
        self,
        photos: list[dict[str, Any]],
        coach_name: str,
        trigger_token: str,
    ) -> CurationResult:
        """
        Process submitted photos through curation pipeline.

        Each photo dict should have:
        - 'path': str — original file path
        - 'width': int — image width
        - 'height': int — image height
        - 'face_confidence': float — face detection confidence
        - 'has_sunglasses': bool
        - 'is_group': bool
        - 'has_motion_blur': bool
        - 'caption': str (optional, auto-generated if missing)
        """
        accepted: list[dict[str, str]] = []
        rejected: list[dict[str, str]] = []

        for photo in photos:
            reason = self._check_rejection(photo)
            if reason:
                rejected.append({"path": photo.get("path", ""), "reason": reason})
            else:
                # Apply background removal (simulated)
                # Apply auto-captioning (simulated)
                caption = photo.get("caption", f"A person, {coach_name}")

                # Inject trigger token
                captioned = f"{trigger_token} {caption}"

                accepted.append({
                    "path": photo.get("path", ""),
                    "caption": captioned,
                    "width": str(photo.get("width", 1024)),
                    "height": str(photo.get("height", 1024)),
                })

        result = CurationResult(
            accepted_count=len(accepted),
            rejected_count=len(rejected),
            rejected_reasons=rejected,
            curated_photos=accepted,
            trigger_token=trigger_token,
        )

        # Receipt Chain Guard
        receipt = build_receipt(
            stage_name=RECEIPT_STAGE_PHOTO_CURATION,
            agent_name="photo_curation_pipeline",
            input_payload={
                "total_photos": len(photos),
                "coach_name": coach_name,
            },
            output_payload={
                "accepted": len(accepted),
                "rejected": len(rejected),
            },
            previous_receipt_hash=self._last_receipt_hash,
        )
        self._receipts.append(receipt)
        self._last_receipt_hash = compute_receipt_hash(receipt)

        return result

    def _check_rejection(self, photo: dict[str, Any]) -> str | None:
        """Check if a photo should be rejected."""
        if photo.get("has_sunglasses", False):
            return "sunglasses"
        if photo.get("is_group", False):
            return "group_photo"
        w = photo.get("width", 0)
        h = photo.get("height", 0)
        if w < self.MIN_RESOLUTION or h < self.MIN_RESOLUTION:
            return "low_resolution"
        if photo.get("has_motion_blur", False):
            return "motion_blur"
        if photo.get("face_confidence", 0) < self.MIN_FACE_CONFIDENCE:
            return "no_face"
        return None

    def get_receipts(self) -> list[dict]:
        return list(self._receipts)


# =====================================================
#  Trigger Token Registry (§4 Stage 1)
# =====================================================

class TriggerTokenRegistry:
    """
    §10 Unit Test: Trigger Token Uniqueness.
    Generates unique trigger tokens per coach.
    """

    def __init__(self) -> None:
        self._tokens: dict[str, str] = {}  # trigger_token → coach_id

    def generate_token(self, coach_name: str) -> str:
        """
        Generate unique trigger token from coach name.
        Format: ccp_{normalized_name}
        Appends _N suffix for duplicates.
        """
        # Normalize: lowercase, alphanumeric only
        normalized = re.sub(r"[^a-z0-9]", "", coach_name.lower())
        base_token = f"ccp_{normalized}"

        if base_token not in self._tokens:
            self._tokens[base_token] = ""
            return base_token

        # Collision — append suffix
        suffix = 2
        while f"{base_token}_{suffix}" in self._tokens:
            suffix += 1

        token = f"{base_token}_{suffix}"
        self._tokens[token] = ""
        return token

    def register_token(self, token: str, coach_id: str) -> None:
        """Register a token → coach_id mapping."""
        self._tokens[token] = coach_id

    def is_unique(self, token: str) -> bool:
        return token not in self._tokens

    def get_coach_id(self, token: str) -> str | None:
        return self._tokens.get(token) or None


# =====================================================
#  Training Config Builder (§4 Stage 2)
# =====================================================

class TrainingConfigBuilder:
    """
    §10 Unit Test: Config Generation.
    Generates AI-Toolkit YAML config from coach profile.
    """

    DEFAULT_CONFIG = {
        "base_model": "FLUX 2 Dev FP16",
        "lora_rank": 24,
        "lora_alpha": 48,
        "target_modules": "MMDiT attention layers",
        "learning_rate": 4e-4,
        "batch_size": 1,
        "gradient_accumulation": 4,
        "resolution": 1024,
        "regularization_images": 200,
        "mixed_precision": "bf16",
        "optimizer": "AdamW 8-bit",
    }

    def build_config(
        self,
        dataset_size: int,
        coach_id: str,
        trigger_token: str,
        attempt_number: int = 1,
    ) -> dict[str, Any]:
        """
        Build training configuration.
        Steps = midpoint of 1500-2000 range, scaled by dataset size.
        """
        config = dict(self.DEFAULT_CONFIG)

        # Calculate training steps based on dataset size
        # Midpoint: 1750 for 25 images. Scale proportionally.
        base_steps = 1750
        scale = dataset_size / 25.0
        steps = int(base_steps * max(0.6, min(1.4, scale)))

        # Auto-retry adjustment: halve LR, add 500 steps
        if attempt_number > 1:
            config["learning_rate"] = config["learning_rate"] / (2 ** (attempt_number - 1))
            steps += 500 * (attempt_number - 1)

        config["training_steps"] = steps
        config["coach_id"] = coach_id
        config["trigger_token"] = trigger_token
        config["dataset_size"] = dataset_size

        return config


# =====================================================
#  Validation Pipeline (§4 Stage 3)
# =====================================================

class LoRAValidationPipeline:
    """
    §4 Stage 3: 5-metric validation.
    IPS ≥ 0.85, style flexibility ≥ 3/5, expression neutrality ≤ 0.10,
    background independence ≥ 0.85, ConsciousSmile compatibility.
    """

    def validate(
        self,
        identity_score: float,
        style_flexibility_pass: int,
        expression_neutrality: float,
        background_independence: float,
        conscious_smile_compatible: bool,
    ) -> ValidationReport:
        """Run all 5 validation metrics."""
        failures: list[str] = []

        if identity_score < IDENTITY_SCORE_THRESHOLD:
            failures.append(
                f"Identity score {identity_score:.2f} < {IDENTITY_SCORE_THRESHOLD} threshold"
            )

        if style_flexibility_pass < STYLE_FLEXIBILITY_MIN_PASS:
            failures.append(
                f"Style flexibility {style_flexibility_pass}/5 < {STYLE_FLEXIBILITY_MIN_PASS}/5 minimum"
            )

        if expression_neutrality > EXPRESSION_NEUTRALITY_THRESHOLD:
            failures.append(
                f"Expression neutrality {expression_neutrality:.2f} > {EXPRESSION_NEUTRALITY_THRESHOLD} threshold"
            )

        if background_independence < IDENTITY_SCORE_THRESHOLD:
            failures.append(
                f"Background independence {background_independence:.2f} < {IDENTITY_SCORE_THRESHOLD} threshold"
            )

        if not conscious_smile_compatible:
            failures.append("ConsciousSmile compatibility test failed — artifacts detected")

        return ValidationReport(
            identity_score=identity_score,
            style_flexibility_pass=style_flexibility_pass,
            expression_neutrality=expression_neutrality,
            background_independence=background_independence,
            conscious_smile_compatible=conscious_smile_compatible,
            passed=len(failures) == 0,
            failure_reasons=failures,
        )


# =====================================================
#  Identity LoRA Training Service (§4 Stages 1-4)
# =====================================================

class IdentityLoRATrainingService:
    """
    Full training pipeline: curate → configure → train → validate → deploy.
    """

    def __init__(self) -> None:
        self._curation = PhotoCurationPipeline()
        self._token_registry = TriggerTokenRegistry()
        self._config_builder = TrainingConfigBuilder()
        self._validator = LoRAValidationPipeline()
        self._registry: dict[str, IdentityLoRAEntry] = {}  # coach_id → entry
        self._jobs: dict[str, TrainingJobRow] = {}  # job_id → job
        self._receipts: list[dict] = []
        self._last_receipt_hash = ""

    def submit_training_job(
        self,
        coach_id: str,
        coach_name: str,
        photos: list[dict[str, Any]],
    ) -> TrainingJobRow:
        """Submit a new LoRA training job."""
        # Generate trigger token
        trigger_token = self._token_registry.generate_token(coach_name)
        self._token_registry.register_token(trigger_token, coach_id)

        # Curate photos
        curation = self._curation.curate(photos, coach_name, trigger_token)

        if curation.accepted_count < PhotoCurationPipeline.MIN_PHOTOS:
            raise VisualPipelineError(
                code="INSUFFICIENT_PHOTOS",
                message=(
                    f"Only {curation.accepted_count} photos accepted "
                    f"(minimum {PhotoCurationPipeline.MIN_PHOTOS}). "
                    f"Rejected: {curation.rejected_count}. "
                    f"Reasons: {[r['reason'] for r in curation.rejected_reasons]}"
                ),
            )

        # Determine version
        version = 1
        existing = self._registry.get(coach_id)
        if existing:
            version = existing.lora_version + 1

        # Build config
        config = self._config_builder.build_config(
            dataset_size=curation.accepted_count,
            coach_id=coach_id,
            trigger_token=trigger_token,
        )

        # Create job
        job_id = f"LORA-{coach_id[:8]}-{version:03d}"
        job = TrainingJobRow(
            job_id=job_id,
            coach_id=coach_id,
            target_version=version,
            reference_photos=[{"path": p["path"], "caption": p["caption"]} for p in curation.curated_photos],
            training_config=config,
            status=TrainingJobStatus.QUEUED,
        )
        self._jobs[job_id] = job

        # Receipt Chain Guard
        receipt = build_receipt(
            stage_name=RECEIPT_STAGE_LORA_TRAINING_START,
            agent_name="identity_lora_training_service",
            input_payload={
                "coach_id": coach_id,
                "photo_count": len(photos),
                "accepted": curation.accepted_count,
            },
            output_payload={"job_id": job_id, "version": version, "trigger_token": trigger_token},
            previous_receipt_hash=self._last_receipt_hash,
        )
        self._receipts.append(receipt)
        self._last_receipt_hash = compute_receipt_hash(receipt)

        return job

    def complete_training(
        self,
        job_id: str,
        identity_score: float,
        style_flexibility_pass: int,
        expression_neutrality: float,
        background_independence: float,
        conscious_smile_compatible: bool,
        file_size_mb: float = 60.0,
        training_hours: float = 2.0,
    ) -> IdentityLoRAEntry | None:
        """
        Complete a training job with validation metrics.
        Returns IdentityLoRAEntry if validation passes, None if retry needed.
        """
        job = self._jobs.get(job_id)
        if job is None:
            raise VisualPipelineError(code="JOB_NOT_FOUND", message=f"Job {job_id} not found.")

        # File size check (§10 Safety)
        if file_size_mb > 200:
            raise VisualPipelineError(
                code="LORA_SIZE_ANOMALY",
                message=f"LoRA file {file_size_mb}MB exceeds 200MB limit — likely rank/alpha misconfigured.",
            )

        # Run validation
        report = self._validator.validate(
            identity_score, style_flexibility_pass, expression_neutrality,
            background_independence, conscious_smile_compatible,
        )

        job.validation_report = report.model_dump()
        job.training_duration_hours = training_hours

        if not report.passed:
            if job.attempt_number < MAX_TRAINING_RETRIES:
                job.status = TrainingJobStatus.RETRYING
                job.attempt_number += 1
                # Rebuild config with adjusted LR
                job.training_config = self._config_builder.build_config(
                    dataset_size=len(job.reference_photos),
                    coach_id=job.coach_id,
                    trigger_token=job.training_config.get("trigger_token", ""),
                    attempt_number=job.attempt_number,
                )
                return None
            else:
                job.status = TrainingJobStatus.FAILED
                job.error_message = f"Max retries ({MAX_TRAINING_RETRIES}) exceeded. Failures: {report.failure_reasons}"
                return None

        # Validation passed — deploy
        job.status = TrainingJobStatus.COMPLETED

        file_path = f"/efs/ccp-models/loras/{job.coach_id}_identity_v{job.target_version}.safetensors"
        trigger_token = job.training_config.get("trigger_token", "")

        entry = IdentityLoRAEntry(
            coach_id=job.coach_id,
            lora_version=job.target_version,
            trigger_token=trigger_token,
            file_path=file_path,
            file_size_mb=file_size_mb,
            lora_rank=job.training_config.get("lora_rank", 24),
            lora_alpha=job.training_config.get("lora_alpha", 48),
            training_steps=job.training_config.get("training_steps", 0),
            reference_photo_count=len(job.reference_photos),
            identity_score=identity_score,
            style_flexibility_score=float(style_flexibility_pass),
            expression_neutrality=expression_neutrality,
            conscious_smile_compatible=conscious_smile_compatible,
            status=LoRAStatus.ACTIVE,
            trained_at=datetime.now(timezone.utc),
            deployed_at=datetime.now(timezone.utc),
        )

        # Retire previous version
        existing = self._registry.get(job.coach_id)
        if existing:
            existing.status = LoRAStatus.RETIRED
            existing.retired_at = datetime.now(timezone.utc)

        self._registry[job.coach_id] = entry

        # Receipt Chain Guard
        receipt = build_receipt(
            stage_name=RECEIPT_STAGE_LORA_TRAINING_COMPLETE,
            agent_name="identity_lora_training_service",
            input_payload={"job_id": job_id, "validation_passed": True},
            output_payload={
                "file_path": file_path,
                "version": job.target_version,
                "identity_score": identity_score,
            },
            previous_receipt_hash=self._last_receipt_hash,
        )
        entry.receipt_chain_block = receipt["receipt_id"]
        self._receipts.append(receipt)
        self._last_receipt_hash = compute_receipt_hash(receipt)

        return entry

    def get_active_lora(self, coach_id: str) -> IdentityLoRAEntry | None:
        """Get the active LoRA for a coach."""
        entry = self._registry.get(coach_id)
        if entry and entry.status == LoRAStatus.ACTIVE:
            return entry
        return None

    def get_job(self, job_id: str) -> TrainingJobRow | None:
        return self._jobs.get(job_id)

    def get_token_registry(self) -> TriggerTokenRegistry:
        return self._token_registry

    def get_curation_pipeline(self) -> PhotoCurationPipeline:
        return self._curation

    def get_receipts(self) -> list[dict]:
        return list(self._receipts)
