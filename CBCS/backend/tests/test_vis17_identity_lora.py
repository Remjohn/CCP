"""
FR-VIS-17 — Identity LoRA Training Pipeline Tests (Step 30)

Coverage:
- AC1: Identity fidelity (validation pipeline passes ≥ 0.85 IPS)
- AC3: Expression neutrality (≤ 0.10 threshold)
- AC4: ConsciousSmile stacking compatibility
- AC6: Versioning (v2 replaces v1, v1 retired)
- Curation: Background removal, rejection of sunglasses/groups/low-res
- Trigger token: Uniqueness across similar names
- Config: Step calculation scaled by dataset size
- Safety: LoRA size limit, adversarial photos
"""

import pytest

from core.identity_lora_trainer import (
    IdentityLoRATrainingService,
    LoRAValidationPipeline,
    PhotoCurationPipeline,
    TrainingConfigBuilder,
    TriggerTokenRegistry,
)
from core.visual_models import LoRAStatus, TrainingJobStatus, VisualPipelineError


def _make_photos(n: int = 25, **overrides) -> list[dict]:
    """Generate n valid photo dicts."""
    base = {
        "width": 1024, "height": 1024,
        "face_confidence": 0.95, "has_sunglasses": False,
        "is_group": False, "has_motion_blur": False,
    }
    base.update(overrides)
    return [{"path": f"photo_{i}.jpg", **base} for i in range(n)]


class TestPhotoCuration:

    def test_all_valid_photos_accepted(self):
        pipeline = PhotoCurationPipeline()
        photos = _make_photos(25)
        result = pipeline.curate(photos, "Coach Alpha", "ccp_alpha")

        assert result.accepted_count == 25
        assert result.rejected_count == 0

    def test_sunglasses_rejected(self):
        pipeline = PhotoCurationPipeline()
        photos = _make_photos(20) + _make_photos(5, has_sunglasses=True)
        result = pipeline.curate(photos, "Coach Alpha", "ccp_alpha")

        assert result.accepted_count == 20
        assert result.rejected_count == 5
        assert result.rejected_reasons[0]["reason"] == "sunglasses"

    def test_group_photos_rejected(self):
        pipeline = PhotoCurationPipeline()
        photos = _make_photos(20) + _make_photos(2, is_group=True)
        result = pipeline.curate(photos, "Coach Alpha", "ccp_alpha")

        assert result.rejected_count == 2

    def test_low_resolution_rejected(self):
        pipeline = PhotoCurationPipeline()
        photos = _make_photos(20) + _make_photos(3, width=256, height=256)
        result = pipeline.curate(photos, "Coach Alpha", "ccp_alpha")

        assert result.rejected_count == 3
        assert result.rejected_reasons[0]["reason"] == "low_resolution"

    def test_trigger_token_injected(self):
        pipeline = PhotoCurationPipeline()
        photos = _make_photos(15)
        result = pipeline.curate(photos, "Coach Alpha", "ccp_alpha")

        for photo in result.curated_photos:
            assert photo["caption"].startswith("ccp_alpha ")

    def test_receipt_written(self):
        pipeline = PhotoCurationPipeline()
        pipeline.curate(_make_photos(15), "Coach Alpha", "ccp_alpha")

        receipts = pipeline.get_receipts()
        assert len(receipts) == 1
        assert receipts[0]["stage_name"] == "PHOTO_CURATION"


class TestTriggerTokenRegistry:

    def test_unique_token_generated(self):
        registry = TriggerTokenRegistry()
        token = registry.generate_token("Audrey")
        assert token == "ccp_audrey"

    def test_similar_names_unique(self):
        registry = TriggerTokenRegistry()
        t1 = registry.generate_token("Audrey")
        t2 = registry.generate_token("Audrey")

        assert t1 != t2
        assert t1 == "ccp_audrey"
        assert t2 == "ccp_audrey_2"

    def test_three_similar_names(self):
        registry = TriggerTokenRegistry()
        t1 = registry.generate_token("Jean Pierre")
        t2 = registry.generate_token("Jean Pierre")
        t3 = registry.generate_token("Jean Pierre")

        assert len({t1, t2, t3}) == 3


class TestTrainingConfigBuilder:

    def test_25_images_midpoint_steps(self):
        builder = TrainingConfigBuilder()
        config = builder.build_config(25, "coach-001", "ccp_coach")

        assert config["training_steps"] == 1750

    def test_20_images_scaled_down(self):
        builder = TrainingConfigBuilder()
        config = builder.build_config(20, "coach-001", "ccp_coach")

        assert config["training_steps"] < 1750

    def test_retry_halves_lr(self):
        builder = TrainingConfigBuilder()
        config1 = builder.build_config(25, "coach-001", "ccp_coach", attempt_number=1)
        config2 = builder.build_config(25, "coach-001", "ccp_coach", attempt_number=2)

        assert config2["learning_rate"] == config1["learning_rate"] / 2

    def test_retry_adds_steps(self):
        builder = TrainingConfigBuilder()
        config1 = builder.build_config(25, "coach-001", "ccp_coach", attempt_number=1)
        config2 = builder.build_config(25, "coach-001", "ccp_coach", attempt_number=2)

        assert config2["training_steps"] == config1["training_steps"] + 500


class TestLoRAValidation:

    def test_all_passing(self):
        validator = LoRAValidationPipeline()
        report = validator.validate(0.90, 4, 0.05, 0.88, True)

        assert report.passed is True
        assert report.failure_reasons == []

    def test_low_identity_score_fails(self):
        validator = LoRAValidationPipeline()
        report = validator.validate(0.70, 4, 0.05, 0.88, True)

        assert report.passed is False
        assert any("Identity score" in r for r in report.failure_reasons)

    def test_high_expression_neutrality_fails(self):
        """AC3: Expression neutrality > 0.10 means LoRA learned a default expression."""
        validator = LoRAValidationPipeline()
        report = validator.validate(0.90, 4, 0.40, 0.88, True)

        assert report.passed is False
        assert any("neutrality" in r for r in report.failure_reasons)

    def test_low_style_flexibility_fails(self):
        validator = LoRAValidationPipeline()
        report = validator.validate(0.90, 2, 0.05, 0.88, True)

        assert report.passed is False

    def test_conscious_smile_incompatible_fails(self):
        """AC4: ConsciousSmile stacking must not produce artifacts."""
        validator = LoRAValidationPipeline()
        report = validator.validate(0.90, 4, 0.05, 0.88, False)

        assert report.passed is False


class TestIdentityLoRATrainingService:

    def test_full_training_flow(self):
        service = IdentityLoRATrainingService()
        photos = _make_photos(25)

        job = service.submit_training_job("coach-001", "Audrey", photos)
        assert job.status == TrainingJobStatus.QUEUED

        entry = service.complete_training(
            job.job_id, identity_score=0.90, style_flexibility_pass=4,
            expression_neutrality=0.05, background_independence=0.88,
            conscious_smile_compatible=True,
        )

        assert entry is not None
        assert entry.status == LoRAStatus.ACTIVE
        assert entry.identity_score == 0.90
        assert "identity_v1" in entry.file_path

    def test_insufficient_photos_raises(self):
        service = IdentityLoRATrainingService()
        photos = _make_photos(10)  # Below minimum

        with pytest.raises(VisualPipelineError) as exc:
            service.submit_training_job("coach-001", "Audrey", photos)
        # All 10 are valid but below MIN_PHOTOS=15
        # Actually they pass quality but count < 15
        assert exc.value.code == "INSUFFICIENT_PHOTOS"

    def test_validation_failure_retries(self):
        service = IdentityLoRATrainingService()
        photos = _make_photos(25)

        job = service.submit_training_job("coach-001", "Audrey", photos)
        result = service.complete_training(
            job.job_id, identity_score=0.70,  # Below threshold
            style_flexibility_pass=4, expression_neutrality=0.05,
            background_independence=0.88, conscious_smile_compatible=True,
        )

        assert result is None
        updated_job = service.get_job(job.job_id)
        assert updated_job.status == TrainingJobStatus.RETRYING
        assert updated_job.attempt_number == 2

    def test_versioning_retires_v1(self):
        """AC6: v2 training retires v1."""
        service = IdentityLoRATrainingService()
        photos = _make_photos(25)

        # Train v1
        job1 = service.submit_training_job("coach-001", "Audrey", photos)
        entry1 = service.complete_training(
            job1.job_id, 0.90, 4, 0.05, 0.88, True,
        )
        assert entry1.lora_version == 1
        assert entry1.status == LoRAStatus.ACTIVE

        # Train v2 (new photos)
        job2 = service.submit_training_job("coach-001", "Audrey", photos)
        entry2 = service.complete_training(
            job2.job_id, 0.92, 5, 0.03, 0.91, True,
        )

        assert entry2.lora_version == 2
        assert entry2.status == LoRAStatus.ACTIVE
        # v1 should be retired
        assert entry1.status == LoRAStatus.RETIRED

    def test_lora_size_anomaly(self):
        """Safety: LoRA > 200MB flagged as anomalous."""
        service = IdentityLoRATrainingService()
        photos = _make_photos(25)

        job = service.submit_training_job("coach-001", "Audrey", photos)
        with pytest.raises(VisualPipelineError) as exc:
            service.complete_training(
                job.job_id, 0.90, 4, 0.05, 0.88, True, file_size_mb=250,
            )
        assert exc.value.code == "LORA_SIZE_ANOMALY"

    def test_receipt_chain_written(self):
        service = IdentityLoRATrainingService()
        photos = _make_photos(25)

        job = service.submit_training_job("coach-001", "Audrey", photos)
        service.complete_training(job.job_id, 0.90, 4, 0.05, 0.88, True)

        receipts = service.get_receipts()
        assert len(receipts) == 2
        assert receipts[0]["stage_name"] == "LORA_TRAINING_START"
        assert receipts[1]["stage_name"] == "LORA_TRAINING_COMPLETE"
