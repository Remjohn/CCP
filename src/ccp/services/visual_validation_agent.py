"""
FR-VIS-04 — Visual Validation Agent
====================================
Post-generation quality gate (Gate V-04) that validates every
RunningHub-produced image across three checks:

  Stage 1 — AGSS Scoring (Artificial-Sincerity composite 0–10)
  Stage 2 — Authenticity Feature Verification (3 binary checks)
  Stage 3 — Character Drift Detection (0–1 drift score vs reference)
  Stage 4 — Remediation & Escalation (1 retry, then PENDING_HUMAN_REVIEW)

C-11 Persona Masking: agent names MUST NOT appear in external payloads.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Optional, Protocol

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.visual_engine_models import (
    AGSS_THRESHOLD,
    AGSS_WEIGHT_COMPOSITION,
    AGSS_WEIGHT_EMOTION,
    AGSS_WEIGHT_LIGHTING,
    AGSS_WEIGHT_TEXTURE,
    AGSSComponentScores,
    AGSSResult,
    AuthenticityCheck,
    AuthenticityResult,
    CHARACTER_DRIFT_THRESHOLD,
    CharacterDriftResult,
    MAX_VALIDATION_RETRIES,
    RemediationAction,
    RemediationRecord,
    ValidationFailureType,
    ValidationVerdict,
    VisualValidationError,
    VisualValidationResult,
)


# ── protocol for LLM-vision wrapper (dependency-injected) ──────────────

class ImageAnalysisWrapper(Protocol):
    """Structural typing contract for the vision-analysis tool."""

    def score_agss(
        self, image_url: str, slide_context: dict[str, Any]
    ) -> dict[str, Any]:
        """Return dict with lighting_naturalism, texture_authenticity,
        compositional_coherence, emotional_believability (floats 0-10)."""
        ...

    def check_authenticity(
        self, image_url: str
    ) -> dict[str, str]:
        """Return dict with expression_naturalness, facial_proportion,
        skin_texture — each 'PASS' or 'FAIL'."""
        ...

    def detect_drift(
        self, image_url: str, reference_url: str
    ) -> dict[str, Any]:
        """Return dict with drift_score (float 0-1)."""
        ...


# ── helper — compute weighted AGSS composite ───────────────────────────

def _compute_agss_composite(scores: AGSSComponentScores) -> float:
    """Weighted average of 4 AGSS components → 0-10 float."""
    return round(
        scores.lighting_naturalism * AGSS_WEIGHT_LIGHTING
        + scores.texture_authenticity * AGSS_WEIGHT_TEXTURE
        + scores.compositional_coherence * AGSS_WEIGHT_COMPOSITION
        + scores.emotional_believability * AGSS_WEIGHT_EMOTION,
        2,
    )


# ── main validation agent ──────────────────────────────────────────────

class VisualValidationAgent:
    """Orchestrates Gate V-04 visual validation across slides.

    Parameters
    ----------
    coach_acronym : str
        2-4 char coach scope (ADR-01).
    receipt_chain : ReceiptChain
        Audit log.
    image_analysis : ImageAnalysisWrapper | None
        If *None* the service-unavailable fallback activates.
    """

    def __init__(
        self,
        coach_acronym: str,
        receipt_chain: ReceiptChain,
        image_analysis: Optional[ImageAnalysisWrapper] = None,
    ) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(
                f"{VisualValidationError.INVALID_COACH_ACRONYM.value}: "
                f"'{coach_acronym}' length must be 2-4."
            )
        self._coach = coach_acronym
        self._rc = receipt_chain
        self._vision = image_analysis

    # ── public — validate a single slide ────────────────────────────

    def validate_slide(
        self,
        vcb_id: str,
        slide_index: int,
        image_url: str,
        slide_context: dict[str, Any] | None = None,
        reference_image_url: str | None = None,
        reference_character_id: str | None = None,
    ) -> VisualValidationResult:
        """Run all 3 checks on one slide image.

        Returns a *VisualValidationResult* with:
          - overall_verdict: VALIDATED | PENDING_HUMAN_REVIEW |
            VALIDATION_SERVICE_UNAVAILABLE
        """
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        vid = f"VVR-{self._coach}-{now[:10].replace('-', '')}-{uuid.uuid4().hex[:6]}-S{slide_index:02d}"
        warnings: list[str] = []

        # ── fallback: vision unavailable ────────────────────────────
        if self._vision is None:
            return self._build_service_unavailable(
                vid, vcb_id, slide_index, image_url, now
            )

        ctx = slide_context or {}

        # ── Stage 1 — AGSS ──────────────────────────────────────────
        agss_result = self._score_agss(image_url, ctx, warnings)

        # ── Stage 2 — Authenticity ──────────────────────────────────
        auth_result = self._check_authenticity(image_url, warnings)

        # ── Stage 3 — Character Drift ──────────────────────────────
        drift_result = self._check_drift(
            image_url, reference_image_url, reference_character_id, warnings
        )

        # ── Stage 4 — Remediation routing ──────────────────────────
        remediations: list[RemediationRecord] = []
        retry_count = 0
        verdict = self._derive_verdict(agss_result, auth_result, drift_result)

        if verdict != ValidationVerdict.VALIDATED.value:
            # one automated retry per failure type
            retry_count, verdict, agss_result, auth_result, drift_result = (
                self._attempt_remediation(
                    image_url,
                    ctx,
                    reference_image_url,
                    reference_character_id,
                    agss_result,
                    auth_result,
                    drift_result,
                    remediations,
                    warnings,
                )
            )

        # ── Receipt audit ──────────────────────────────────────────
        entry = self._rc.log(
            agent_id="visual-validation-agent",
            action="gate-v04-validation",
            asset_id=vid,
            input_summary=f"vcb={vcb_id} slide={slide_index}",
            output_summary=f"verdict={verdict} agss={agss_result.composite_score}",
            metadata={
                "coach": self._coach,
                "retry_count": retry_count,
            },
        )

        return VisualValidationResult(
            validation_id=vid,
            vcb_id=vcb_id,
            slide_index=slide_index,
            coach_acronym=self._coach,
            image_url=image_url,
            agss=agss_result,
            authenticity=auth_result,
            character_drift=drift_result,
            overall_verdict=verdict,
            retry_count=retry_count,
            remediations=remediations,
            receipt_chain_block=entry.receipt_id,
            timestamp_utc=now,
            warnings=warnings,
        )

    # ── public — batch validate a carousel ─────────────────────────

    def validate_batch(
        self,
        vcb_id: str,
        slides: list[dict[str, Any]],
    ) -> list[VisualValidationResult]:
        """Validate each slide independently (AC6).

        Each element of *slides* must contain:
          - image_url : str
          - slide_index : int
        And optionally:
          - slide_context : dict
          - reference_image_url : str | None
          - reference_character_id : str | None
        """
        results: list[VisualValidationResult] = []
        for slide in slides:
            r = self.validate_slide(
                vcb_id=vcb_id,
                slide_index=slide["slide_index"],
                image_url=slide["image_url"],
                slide_context=slide.get("slide_context"),
                reference_image_url=slide.get("reference_image_url"),
                reference_character_id=slide.get("reference_character_id"),
            )
            results.append(r)
        return results

    # ── internal — AGSS scoring (Stage 1) ──────────────────────────

    def _score_agss(
        self,
        image_url: str,
        ctx: dict[str, Any],
        warnings: list[str],
    ) -> AGSSResult:
        assert self._vision is not None
        try:
            raw = self._vision.score_agss(image_url, ctx)
        except Exception as exc:
            warnings.append(f"AGSS scoring error: {exc}")
            return self._agss_unavailable()

        scores = AGSSComponentScores(
            lighting_naturalism=float(raw.get("lighting_naturalism", 0.0)),
            texture_authenticity=float(raw.get("texture_authenticity", 0.0)),
            compositional_coherence=float(raw.get("compositional_coherence", 0.0)),
            emotional_believability=float(raw.get("emotional_believability", 0.0)),
        )
        composite = _compute_agss_composite(scores)
        result_label = "PASS" if composite >= AGSS_THRESHOLD else "FAIL"
        return AGSSResult(
            composite_score=composite,
            components=scores,
            threshold=AGSS_THRESHOLD,
            result=result_label,
        )

    def _agss_unavailable(self) -> AGSSResult:
        """Fallback scores when vision call fails."""
        z = AGSSComponentScores(
            lighting_naturalism=0.0,
            texture_authenticity=0.0,
            compositional_coherence=0.0,
            emotional_believability=0.0,
        )
        return AGSSResult(
            composite_score=0.0,
            components=z,
            threshold=AGSS_THRESHOLD,
            result="FAIL",
        )

    # ── internal — authenticity verification (Stage 2) ─────────────

    def _check_authenticity(
        self,
        image_url: str,
        warnings: list[str],
    ) -> AuthenticityResult:
        assert self._vision is not None
        try:
            raw = self._vision.check_authenticity(image_url)
        except Exception as exc:
            warnings.append(f"Authenticity check error: {exc}")
            return AuthenticityResult(
                expression_naturalness="FAIL",
                facial_proportion="FAIL",
                skin_texture="FAIL",
                overall_result="FAIL",
            )

        expr = raw.get("expression_naturalness", "FAIL")
        face = raw.get("facial_proportion", "FAIL")
        skin = raw.get("skin_texture", "FAIL")
        overall = "PASS" if all(v == "PASS" for v in [expr, face, skin]) else "FAIL"
        return AuthenticityResult(
            expression_naturalness=expr,
            facial_proportion=face,
            skin_texture=skin,
            overall_result=overall,
        )

    # ── internal — character drift (Stage 3) ───────────────────────

    def _check_drift(
        self,
        image_url: str,
        reference_url: str | None,
        reference_id: str | None,
        warnings: list[str],
    ) -> CharacterDriftResult:
        if reference_url is None:
            # no reference → skip drift check → auto-pass
            return CharacterDriftResult(
                reference_image_used=False,
                reference_character_id=None,
                drift_score=0.0,
                threshold=CHARACTER_DRIFT_THRESHOLD,
                result="PASS",
            )
        assert self._vision is not None
        try:
            raw = self._vision.detect_drift(image_url, reference_url)
        except Exception as exc:
            warnings.append(f"Drift detection error: {exc}")
            return CharacterDriftResult(
                reference_image_used=True,
                reference_character_id=reference_id,
                drift_score=1.0,
                threshold=CHARACTER_DRIFT_THRESHOLD,
                result="FAIL",
            )
        drift = float(raw.get("drift_score", 1.0))
        result_label = "PASS" if drift <= CHARACTER_DRIFT_THRESHOLD else "FAIL"
        return CharacterDriftResult(
            reference_image_used=True,
            reference_character_id=reference_id,
            drift_score=drift,
            threshold=CHARACTER_DRIFT_THRESHOLD,
            result=result_label,
        )

    # ── internal — verdict derivation ──────────────────────────────

    @staticmethod
    def _derive_verdict(
        agss: AGSSResult,
        auth: AuthenticityResult,
        drift: CharacterDriftResult,
    ) -> str:
        if (
            agss.result == "PASS"
            and auth.overall_result == "PASS"
            and drift.result == "PASS"
        ):
            return ValidationVerdict.VALIDATED.value
        return "NEEDS_REMEDIATION"

    # ── internal — remediation (Stage 4) ───────────────────────────

    def _attempt_remediation(
        self,
        image_url: str,
        ctx: dict[str, Any],
        reference_url: str | None,
        reference_id: str | None,
        agss: AGSSResult,
        auth: AuthenticityResult,
        drift: CharacterDriftResult,
        remediations: list[RemediationRecord],
        warnings: list[str],
    ) -> tuple[int, str, AGSSResult, AuthenticityResult, CharacterDriftResult]:
        """One retry per failure type. Returns (retry_count, verdict,
        updated agss/auth/drift)."""
        retry = 1

        # ── remediate AGSS ──────────────────────────────────────────
        if agss.result == "FAIL":
            remediations.append(
                RemediationRecord(
                    failure_type=ValidationFailureType.AGSS_BELOW_THRESHOLD.value,
                    action_taken=RemediationAction.ENHANCED_IMPERFECTION.value,
                    retry_number=1,
                    details=f"AGSS {agss.composite_score} < {AGSS_THRESHOLD}",
                )
            )
            agss = self._score_agss(image_url, ctx, warnings)
            if agss.result == "FAIL":
                remediations.append(
                    RemediationRecord(
                        failure_type=ValidationFailureType.AGSS_BELOW_THRESHOLD.value,
                        action_taken=RemediationAction.PENDING_HUMAN_REVIEW.value,
                        retry_number=2,
                        details=f"Second AGSS fail {agss.composite_score}",
                    )
                )
                return (
                    retry,
                    ValidationVerdict.PENDING_HUMAN_REVIEW.value,
                    agss,
                    auth,
                    drift,
                )

        # ── remediate Authenticity ──────────────────────────────────
        if auth.overall_result == "FAIL":
            failed_checks = self._identify_auth_failures(auth)
            for fc in failed_checks:
                remediations.append(
                    RemediationRecord(
                        failure_type=fc,
                        action_taken=RemediationAction.ENHANCED_IMPERFECTION.value,
                        retry_number=1,
                        details=f"Authenticity {fc} FAIL",
                    )
                )
            auth = self._check_authenticity(image_url, warnings)
            if auth.overall_result == "FAIL":
                for fc in self._identify_auth_failures(auth):
                    remediations.append(
                        RemediationRecord(
                            failure_type=fc,
                            action_taken=RemediationAction.PENDING_HUMAN_REVIEW.value,
                            retry_number=2,
                            details=f"Second authenticity {fc} fail",
                        )
                    )
                return (
                    retry,
                    ValidationVerdict.PENDING_HUMAN_REVIEW.value,
                    agss,
                    auth,
                    drift,
                )

        # ── remediate Drift ────────────────────────────────────────
        if drift.result == "FAIL":
            remediations.append(
                RemediationRecord(
                    failure_type=ValidationFailureType.CHARACTER_DRIFT.value,
                    action_taken=RemediationAction.INCREASED_REF_STRENGTH.value,
                    retry_number=1,
                    details=f"drift {drift.drift_score} > {CHARACTER_DRIFT_THRESHOLD}",
                )
            )
            drift = self._check_drift(
                image_url, reference_url, reference_id, warnings
            )
            if drift.result == "FAIL":
                remediations.append(
                    RemediationRecord(
                        failure_type=ValidationFailureType.CHARACTER_DRIFT.value,
                        action_taken=RemediationAction.PENDING_HUMAN_REVIEW.value,
                        retry_number=2,
                        details=f"Second drift fail {drift.drift_score}",
                    )
                )
                return (
                    retry,
                    ValidationVerdict.PENDING_HUMAN_REVIEW.value,
                    agss,
                    auth,
                    drift,
                )

        # all checks now pass after remediation
        return (retry, self._derive_verdict(agss, auth, drift), agss, auth, drift)

    # ── helpers ─────────────────────────────────────────────────────

    @staticmethod
    def _identify_auth_failures(auth: AuthenticityResult) -> list[str]:
        """Return list of ValidationFailureType values for failed checks."""
        fails: list[str] = []
        if auth.expression_naturalness == "FAIL":
            fails.append(ValidationFailureType.AUTHENTICITY_EXPRESSION.value)
        if auth.facial_proportion == "FAIL":
            fails.append(ValidationFailureType.AUTHENTICITY_PROPORTION.value)
        if auth.skin_texture == "FAIL":
            fails.append(ValidationFailureType.AUTHENTICITY_TEXTURE.value)
        return fails

    def _build_service_unavailable(
        self,
        vid: str,
        vcb_id: str,
        slide_index: int,
        image_url: str,
        now: str,
    ) -> VisualValidationResult:
        """§6 fallback — all images → PENDING_HUMAN_REVIEW."""
        zero = AGSSComponentScores(
            lighting_naturalism=0.0,
            texture_authenticity=0.0,
            compositional_coherence=0.0,
            emotional_believability=0.0,
        )
        entry = self._rc.log(
            agent_id="visual-validation-agent",
            action="gate-v04-service-unavailable",
            asset_id=vid,
            input_summary=f"vcb={vcb_id} slide={slide_index}",
            output_summary="VALIDATION_SERVICE_UNAVAILABLE → PENDING_HUMAN_REVIEW",
        )
        return VisualValidationResult(
            validation_id=vid,
            vcb_id=vcb_id,
            slide_index=slide_index,
            coach_acronym=self._coach,
            image_url=image_url,
            agss=AGSSResult(
                composite_score=0.0,
                components=zero,
                threshold=AGSS_THRESHOLD,
                result="UNAVAILABLE",
            ),
            authenticity=AuthenticityResult(
                expression_naturalness="UNAVAILABLE",
                facial_proportion="UNAVAILABLE",
                skin_texture="UNAVAILABLE",
                overall_result="UNAVAILABLE",
            ),
            character_drift=CharacterDriftResult(
                reference_image_used=False,
                drift_score=0.0,
                threshold=CHARACTER_DRIFT_THRESHOLD,
                result="UNAVAILABLE",
            ),
            overall_verdict=ValidationVerdict.PENDING_HUMAN_REVIEW.value,
            retry_count=0,
            remediations=[],
            receipt_chain_block=entry.receipt_id,
            timestamp_utc=now,
            warnings=["VALIDATION_SERVICE_UNAVAILABLE — all images flagged for human review"],
        )
