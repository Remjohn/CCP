"""
FR-VIS-04 — Visual Validation Agent — Integration Tests
========================================================
59 tests covering 6 ACs × 4 stages + ADR-01 + receipt + edge cases.
"""

from __future__ import annotations

import tempfile
from typing import Any
from unittest.mock import MagicMock

import pytest

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
from src.ccp.services.visual_validation_agent import (
    VisualValidationAgent,
    _compute_agss_composite,
)

# ═══════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════


def _make_agent(
    coach: str = "TST",
    vision: Any = "DEFAULT",
) -> tuple[VisualValidationAgent, ReceiptChain]:
    """Factory for agent + receipt chain with tempdir isolation."""
    tmp = tempfile.mkdtemp()
    rc = ReceiptChain(coach_acronym=coach, log_dir=tmp)
    if vision == "DEFAULT":
        vision = _good_vision()
    agent = VisualValidationAgent(
        coach_acronym=coach,
        receipt_chain=rc,
        image_analysis=vision,
    )
    return agent, rc


def _good_vision(
    agss: dict[str, float] | None = None,
    auth: dict[str, str] | None = None,
    drift: dict[str, Any] | None = None,
) -> MagicMock:
    """Create a mock vision wrapper that returns good scores by default."""
    mock = MagicMock()
    mock.score_agss.return_value = agss or {
        "lighting_naturalism": 8.0,
        "texture_authenticity": 7.5,
        "compositional_coherence": 7.8,
        "emotional_believability": 7.2,
    }
    mock.check_authenticity.return_value = auth or {
        "expression_naturalness": "PASS",
        "facial_proportion": "PASS",
        "skin_texture": "PASS",
    }
    mock.detect_drift.return_value = drift or {"drift_score": 0.15}
    return mock


def _failing_agss_vision(first_score: float = 5.8, second_score: float = 7.2):
    """Vision that returns low AGSS first, then high."""
    mock = MagicMock()
    scores = iter(
        [
            {
                "lighting_naturalism": first_score,
                "texture_authenticity": first_score,
                "compositional_coherence": first_score,
                "emotional_believability": first_score,
            },
            {
                "lighting_naturalism": second_score,
                "texture_authenticity": second_score,
                "compositional_coherence": second_score,
                "emotional_believability": second_score,
            },
        ]
    )
    mock.score_agss.side_effect = lambda *a, **kw: next(scores)
    mock.check_authenticity.return_value = {
        "expression_naturalness": "PASS",
        "facial_proportion": "PASS",
        "skin_texture": "PASS",
    }
    mock.detect_drift.return_value = {"drift_score": 0.10}
    return mock


def _double_failing_agss_vision(score: float = 5.8):
    """Vision that always returns low AGSS (both attempts fail)."""
    mock = MagicMock()
    mock.score_agss.return_value = {
        "lighting_naturalism": score,
        "texture_authenticity": score,
        "compositional_coherence": score,
        "emotional_believability": score,
    }
    mock.check_authenticity.return_value = {
        "expression_naturalness": "PASS",
        "facial_proportion": "PASS",
        "skin_texture": "PASS",
    }
    mock.detect_drift.return_value = {"drift_score": 0.10}
    return mock


def _failing_auth_vision(
    expr: str = "FAIL", face: str = "PASS", skin: str = "PASS",
    second_expr: str = "PASS", second_face: str = "PASS", second_skin: str = "PASS",
):
    """Vision that fails authenticity then passes on retry."""
    mock = MagicMock()
    mock.score_agss.return_value = {
        "lighting_naturalism": 8.0,
        "texture_authenticity": 8.0,
        "compositional_coherence": 8.0,
        "emotional_believability": 8.0,
    }
    auths = iter([
        {"expression_naturalness": expr, "facial_proportion": face, "skin_texture": skin},
        {"expression_naturalness": second_expr, "facial_proportion": second_face, "skin_texture": second_skin},
    ])
    mock.check_authenticity.side_effect = lambda *a, **kw: next(auths)
    mock.detect_drift.return_value = {"drift_score": 0.10}
    return mock


def _double_failing_auth_vision(expr: str = "FAIL"):
    """Vision that always fails expression naturalness."""
    mock = MagicMock()
    mock.score_agss.return_value = {
        "lighting_naturalism": 8.0,
        "texture_authenticity": 8.0,
        "compositional_coherence": 8.0,
        "emotional_believability": 8.0,
    }
    mock.check_authenticity.return_value = {
        "expression_naturalness": expr,
        "facial_proportion": "PASS",
        "skin_texture": "PASS",
    }
    mock.detect_drift.return_value = {"drift_score": 0.10}
    return mock


def _failing_drift_vision(first: float = 0.42, second: float = 0.22):
    """Vision that returns high drift then low drift."""
    mock = MagicMock()
    mock.score_agss.return_value = {
        "lighting_naturalism": 8.0,
        "texture_authenticity": 8.0,
        "compositional_coherence": 8.0,
        "emotional_believability": 8.0,
    }
    mock.check_authenticity.return_value = {
        "expression_naturalness": "PASS",
        "facial_proportion": "PASS",
        "skin_texture": "PASS",
    }
    drifts = iter([{"drift_score": first}, {"drift_score": second}])
    mock.detect_drift.side_effect = lambda *a, **kw: next(drifts)
    return mock


def _double_failing_drift_vision(score: float = 0.42):
    """Vision that always returns high drift."""
    mock = MagicMock()
    mock.score_agss.return_value = {
        "lighting_naturalism": 8.0,
        "texture_authenticity": 8.0,
        "compositional_coherence": 8.0,
        "emotional_believability": 8.0,
    }
    mock.check_authenticity.return_value = {
        "expression_naturalness": "PASS",
        "facial_proportion": "PASS",
        "skin_texture": "PASS",
    }
    mock.detect_drift.return_value = {"drift_score": score}
    return mock


# ═══════════════════════════════════════════════════════════════════════
# § Constants
# ═══════════════════════════════════════════════════════════════════════


class TestConstants:
    def test_agss_threshold(self):
        assert AGSS_THRESHOLD == 6.5

    def test_drift_threshold(self):
        assert CHARACTER_DRIFT_THRESHOLD == 0.30

    def test_max_retries(self):
        assert MAX_VALIDATION_RETRIES == 1

    def test_agss_weights_sum_to_one(self):
        total = (
            AGSS_WEIGHT_LIGHTING
            + AGSS_WEIGHT_TEXTURE
            + AGSS_WEIGHT_COMPOSITION
            + AGSS_WEIGHT_EMOTION
        )
        assert abs(total - 1.0) < 1e-9


# ═══════════════════════════════════════════════════════════════════════
# § Enums
# ═══════════════════════════════════════════════════════════════════════


class TestEnums:
    def test_validation_verdict_members(self):
        assert set(ValidationVerdict.__members__.keys()) == {
            "VALIDATED",
            "REMEDIATION_IN_PROGRESS",
            "PENDING_HUMAN_REVIEW",
            "VALIDATION_SERVICE_UNAVAILABLE",
        }

    def test_authenticity_check_members(self):
        assert set(AuthenticityCheck.__members__.keys()) == {
            "EXPRESSION_NATURALNESS",
            "FACIAL_PROPORTION",
            "SKIN_TEXTURE",
        }

    def test_failure_type_members(self):
        assert set(ValidationFailureType.__members__.keys()) == {
            "AGSS_BELOW_THRESHOLD",
            "AUTHENTICITY_EXPRESSION",
            "AUTHENTICITY_PROPORTION",
            "AUTHENTICITY_TEXTURE",
            "CHARACTER_DRIFT",
        }

    def test_remediation_action_members(self):
        assert set(RemediationAction.__members__.keys()) == {
            "ENHANCED_IMPERFECTION",
            "INCREASED_REF_STRENGTH",
            "PENDING_HUMAN_REVIEW",
            "NONE",
        }

    def test_visual_validation_error_members(self):
        assert set(VisualValidationError.__members__.keys()) == {
            "INVALID_IMAGE_FORMAT",
            "VISION_API_ERROR",
            "VALIDATION_SERVICE_UNAVAILABLE",
            "REMEDIATION_EXHAUSTED",
            "INVALID_COACH_ACRONYM",
        }


# ═══════════════════════════════════════════════════════════════════════
# § AGSS Composite Calculation
# ═══════════════════════════════════════════════════════════════════════


class TestAGSSComposite:
    def test_equal_scores(self):
        s = AGSSComponentScores(
            lighting_naturalism=8.0,
            texture_authenticity=8.0,
            compositional_coherence=8.0,
            emotional_believability=8.0,
        )
        assert _compute_agss_composite(s) == 8.0

    def test_weighted_average(self):
        s = AGSSComponentScores(
            lighting_naturalism=10.0,
            texture_authenticity=6.0,
            compositional_coherence=8.0,
            emotional_believability=4.0,
        )
        expected = 10.0 * 0.25 + 6.0 * 0.25 + 8.0 * 0.25 + 4.0 * 0.25
        assert _compute_agss_composite(s) == round(expected, 2)

    def test_zero_scores(self):
        s = AGSSComponentScores(
            lighting_naturalism=0.0,
            texture_authenticity=0.0,
            compositional_coherence=0.0,
            emotional_believability=0.0,
        )
        assert _compute_agss_composite(s) == 0.0

    def test_max_scores(self):
        s = AGSSComponentScores(
            lighting_naturalism=10.0,
            texture_authenticity=10.0,
            compositional_coherence=10.0,
            emotional_believability=10.0,
        )
        assert _compute_agss_composite(s) == 10.0


# ═══════════════════════════════════════════════════════════════════════
# § AC1: AGSS Pass → VALIDATED
# ═══════════════════════════════════════════════════════════════════════


class TestAC1_AGSS_Pass:
    def test_all_pass_verdict_validated(self):
        agent, _ = _make_agent()
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        assert r.overall_verdict == ValidationVerdict.VALIDATED.value

    def test_agss_composite_above_threshold(self):
        agent, _ = _make_agent()
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        assert r.agss.composite_score >= AGSS_THRESHOLD
        assert r.agss.result == "PASS"

    def test_all_authenticity_pass(self):
        agent, _ = _make_agent()
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        assert r.authenticity.overall_result == "PASS"

    def test_no_drift_without_reference(self):
        agent, _ = _make_agent()
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        assert r.character_drift.result == "PASS"
        assert r.character_drift.reference_image_used is False

    def test_drift_pass_with_reference(self):
        agent, _ = _make_agent()
        r = agent.validate_slide(
            "VCB-TST-001", 0, "https://example.com/img.png",
            reference_image_url="https://example.com/ref.png",
            reference_character_id="CHAR-001",
        )
        assert r.character_drift.result == "PASS"
        assert r.character_drift.reference_image_used is True

    def test_zero_retries(self):
        agent, _ = _make_agent()
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        assert r.retry_count == 0
        assert r.remediations == []

    def test_receipt_chain_logged(self):
        agent, rc = _make_agent()
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        assert r.receipt_chain_block is not None
        entries = rc.query(action="gate-v04-validation")
        assert len(entries) >= 1

    def test_validation_id_format(self):
        agent, _ = _make_agent()
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        assert r.validation_id.startswith("VVR-TST-")
        assert "-S00" in r.validation_id


# ═══════════════════════════════════════════════════════════════════════
# § AC2: AGSS Fail → Remediation → Pass
# ═══════════════════════════════════════════════════════════════════════


class TestAC2_AGSS_Remediation:
    def test_first_fail_triggers_remediation(self):
        vision = _failing_agss_vision(first_score=5.8, second_score=7.2)
        agent, _ = _make_agent(vision=vision)
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        assert r.overall_verdict == ValidationVerdict.VALIDATED.value

    def test_remediation_records_enhanced_imperfection(self):
        vision = _failing_agss_vision(first_score=5.8, second_score=7.2)
        agent, _ = _make_agent(vision=vision)
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        agss_rems = [
            rem for rem in r.remediations
            if rem.failure_type == ValidationFailureType.AGSS_BELOW_THRESHOLD.value
        ]
        assert len(agss_rems) >= 1
        assert agss_rems[0].action_taken == RemediationAction.ENHANCED_IMPERFECTION.value

    def test_retry_count_is_one(self):
        vision = _failing_agss_vision(first_score=5.8, second_score=7.2)
        agent, _ = _make_agent(vision=vision)
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        assert r.retry_count == 1


# ═══════════════════════════════════════════════════════════════════════
# § AC3: Authenticity Fail — Expression Incoherence
# ═══════════════════════════════════════════════════════════════════════


class TestAC3_Authenticity_Fail:
    def test_expression_fail_detected(self):
        vision = _failing_auth_vision(expr="FAIL")
        agent, _ = _make_agent(vision=vision)
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        # after remediation (retry succeeds), check the remediation record
        expr_rems = [
            rem for rem in r.remediations
            if rem.failure_type == ValidationFailureType.AUTHENTICITY_EXPRESSION.value
        ]
        assert len(expr_rems) >= 1

    def test_expression_fail_remediation_pass(self):
        vision = _failing_auth_vision(expr="FAIL", second_expr="PASS")
        agent, _ = _make_agent(vision=vision)
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        assert r.overall_verdict == ValidationVerdict.VALIDATED.value

    def test_facial_proportion_fail(self):
        vision = _failing_auth_vision(expr="PASS", face="FAIL", second_face="PASS")
        agent, _ = _make_agent(vision=vision)
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        prop_rems = [
            rem for rem in r.remediations
            if rem.failure_type == ValidationFailureType.AUTHENTICITY_PROPORTION.value
        ]
        assert len(prop_rems) >= 1
        assert r.overall_verdict == ValidationVerdict.VALIDATED.value

    def test_skin_texture_fail(self):
        vision = _failing_auth_vision(expr="PASS", skin="FAIL", second_skin="PASS")
        agent, _ = _make_agent(vision=vision)
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        skin_rems = [
            rem for rem in r.remediations
            if rem.failure_type == ValidationFailureType.AUTHENTICITY_TEXTURE.value
        ]
        assert len(skin_rems) >= 1

    def test_multiple_auth_failures_recorded(self):
        vision = _failing_auth_vision(
            expr="FAIL", face="FAIL", skin="FAIL",
            second_expr="PASS", second_face="PASS", second_skin="PASS",
        )
        agent, _ = _make_agent(vision=vision)
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        auth_rems = [
            rem for rem in r.remediations
            if rem.failure_type.startswith("AUTHENTICITY_")
        ]
        assert len(auth_rems) >= 3


# ═══════════════════════════════════════════════════════════════════════
# § AC4: Character Drift → Remediation → Pass
# ═══════════════════════════════════════════════════════════════════════


class TestAC4_Drift_Remediation:
    def test_drift_fail_triggers_ref_strength_increase(self):
        vision = _failing_drift_vision(first=0.42, second=0.22)
        agent, _ = _make_agent(vision=vision)
        r = agent.validate_slide(
            "VCB-TST-001", 0, "https://example.com/img.png",
            reference_image_url="https://example.com/ref.png",
            reference_character_id="CHAR-001",
        )
        drift_rems = [
            rem for rem in r.remediations
            if rem.failure_type == ValidationFailureType.CHARACTER_DRIFT.value
        ]
        assert len(drift_rems) >= 1
        assert drift_rems[0].action_taken == RemediationAction.INCREASED_REF_STRENGTH.value

    def test_drift_remediation_passes(self):
        vision = _failing_drift_vision(first=0.42, second=0.22)
        agent, _ = _make_agent(vision=vision)
        r = agent.validate_slide(
            "VCB-TST-001", 0, "https://example.com/img.png",
            reference_image_url="https://example.com/ref.png",
            reference_character_id="CHAR-001",
        )
        assert r.overall_verdict == ValidationVerdict.VALIDATED.value

    def test_drift_score_below_threshold_after_retry(self):
        vision = _failing_drift_vision(first=0.42, second=0.22)
        agent, _ = _make_agent(vision=vision)
        r = agent.validate_slide(
            "VCB-TST-001", 0, "https://example.com/img.png",
            reference_image_url="https://example.com/ref.png",
        )
        assert r.character_drift.drift_score <= CHARACTER_DRIFT_THRESHOLD


# ═══════════════════════════════════════════════════════════════════════
# § AC5: Second Failure → PENDING_HUMAN_REVIEW
# ═══════════════════════════════════════════════════════════════════════


class TestAC5_Escalation:
    def test_double_agss_fail_escalates(self):
        vision = _double_failing_agss_vision(score=5.8)
        agent, _ = _make_agent(vision=vision)
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        assert r.overall_verdict == ValidationVerdict.PENDING_HUMAN_REVIEW.value

    def test_double_agss_fail_remediation_has_escalation_record(self):
        vision = _double_failing_agss_vision(score=5.8)
        agent, _ = _make_agent(vision=vision)
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        escalations = [
            rem for rem in r.remediations
            if rem.action_taken == RemediationAction.PENDING_HUMAN_REVIEW.value
        ]
        assert len(escalations) >= 1

    def test_double_auth_fail_escalates(self):
        vision = _double_failing_auth_vision(expr="FAIL")
        agent, _ = _make_agent(vision=vision)
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        assert r.overall_verdict == ValidationVerdict.PENDING_HUMAN_REVIEW.value

    def test_double_drift_fail_escalates(self):
        vision = _double_failing_drift_vision(score=0.50)
        agent, _ = _make_agent(vision=vision)
        r = agent.validate_slide(
            "VCB-TST-001", 0, "https://example.com/img.png",
            reference_image_url="https://example.com/ref.png",
        )
        assert r.overall_verdict == ValidationVerdict.PENDING_HUMAN_REVIEW.value

    def test_escalation_contains_both_validation_results(self):
        vision = _double_failing_agss_vision(score=4.0)
        agent, _ = _make_agent(vision=vision)
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        # should have 2 remediation records (first attempt + escalation)
        assert len(r.remediations) >= 2


# ═══════════════════════════════════════════════════════════════════════
# § AC6: Slide Independence (Batch)
# ═══════════════════════════════════════════════════════════════════════


class TestAC6_Batch_Independence:
    def _make_batch_slides(self) -> list[dict[str, Any]]:
        """7-slide carousel: slides 2, 5 fail; rest pass."""
        return [
            {"slide_index": i, "image_url": f"https://example.com/s{i}.png"}
            for i in range(7)
        ]

    def test_batch_returns_7_results(self):
        agent, _ = _make_agent()
        slides = self._make_batch_slides()
        results = agent.validate_batch("VCB-TST-001", slides)
        assert len(results) == 7

    def test_batch_all_pass(self):
        agent, _ = _make_agent()
        slides = self._make_batch_slides()
        results = agent.validate_batch("VCB-TST-001", slides)
        assert all(r.overall_verdict == ValidationVerdict.VALIDATED.value for r in results)

    def test_batch_mixed_results(self):
        """Slides 0,1,3,4,6 use good vision; slides 2,5 use bad."""
        # We need per-slide control; build a custom vision mock
        mock = MagicMock()

        def agss_side_effect(url: str, ctx: dict) -> dict:
            # URL format: https://example.com/s{i}.png
            # Extract index from the last path segment
            filename = url.rsplit("/", 1)[-1]  # "s2.png"
            idx = int(filename.replace("s", "").replace(".png", ""))
            if idx in (2, 5):
                # Always-fail AGSS for these
                return {
                    "lighting_naturalism": 4.0,
                    "texture_authenticity": 4.0,
                    "compositional_coherence": 4.0,
                    "emotional_believability": 4.0,
                }
            return {
                "lighting_naturalism": 8.0,
                "texture_authenticity": 8.0,
                "compositional_coherence": 8.0,
                "emotional_believability": 8.0,
            }

        mock.score_agss.side_effect = agss_side_effect
        mock.check_authenticity.return_value = {
            "expression_naturalness": "PASS",
            "facial_proportion": "PASS",
            "skin_texture": "PASS",
        }
        mock.detect_drift.return_value = {"drift_score": 0.10}

        agent, _ = _make_agent(vision=mock)
        slides = self._make_batch_slides()
        results = agent.validate_batch("VCB-TST-001", slides)

        for r in results:
            if r.slide_index in (2, 5):
                assert r.overall_verdict == ValidationVerdict.PENDING_HUMAN_REVIEW.value
            else:
                assert r.overall_verdict == ValidationVerdict.VALIDATED.value

    def test_batch_slide_indices_preserved(self):
        agent, _ = _make_agent()
        slides = self._make_batch_slides()
        results = agent.validate_batch("VCB-TST-001", slides)
        assert [r.slide_index for r in results] == list(range(7))


# ═══════════════════════════════════════════════════════════════════════
# § Service Unavailable Fallback (§6)
# ═══════════════════════════════════════════════════════════════════════


class TestServiceUnavailable:
    def test_no_vision_returns_pending_human_review(self):
        agent, _ = _make_agent(vision=None)
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        assert r.overall_verdict == ValidationVerdict.PENDING_HUMAN_REVIEW.value

    def test_no_vision_agss_unavailable(self):
        agent, _ = _make_agent(vision=None)
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        assert r.agss.result == "UNAVAILABLE"

    def test_no_vision_auth_unavailable(self):
        agent, _ = _make_agent(vision=None)
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        assert r.authenticity.overall_result == "UNAVAILABLE"

    def test_no_vision_drift_unavailable(self):
        agent, _ = _make_agent(vision=None)
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        assert r.character_drift.result == "UNAVAILABLE"

    def test_no_vision_warning_present(self):
        agent, _ = _make_agent(vision=None)
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        assert any("VALIDATION_SERVICE_UNAVAILABLE" in w for w in r.warnings)

    def test_no_vision_receipt_logged(self):
        agent, rc = _make_agent(vision=None)
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        entries = rc.query(action="gate-v04-service-unavailable")
        assert len(entries) >= 1


# ═══════════════════════════════════════════════════════════════════════
# § ADR-01 Coach Scope Validation
# ═══════════════════════════════════════════════════════════════════════


class TestADR01:
    def test_valid_3char_coach(self):
        agent, _ = _make_agent(coach="TST")
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        assert r.coach_acronym == "TST"

    def test_valid_3char_coach_alt(self):
        agent, _ = _make_agent(coach="JPX")
        r = agent.validate_slide("VCB-JPX-001", 0, "https://example.com/img.png")
        assert r.coach_acronym == "JPX"

    def test_adapter_accepts_2char_coach(self):
        """ADR-01: adapter allows 2-4 char coach acronyms."""
        tmp = tempfile.mkdtemp()
        rc = ReceiptChain(coach_acronym="JPX", log_dir=tmp)
        agent = VisualValidationAgent(coach_acronym="JP", receipt_chain=rc, image_analysis=_good_vision())
        r = agent.validate_slide("VCB-JP-001", 0, "https://example.com/img.png")
        assert r.coach_acronym == "JP"

    def test_1char_coach_rejected(self):
        with pytest.raises(ValueError, match="INVALID_COACH_ACRONYM"):
            _make_agent(coach="X")

    def test_5char_coach_rejected(self):
        with pytest.raises(ValueError, match="INVALID_COACH_ACRONYM"):
            _make_agent(coach="ABCDE")

    def test_empty_coach_rejected(self):
        with pytest.raises(ValueError, match="INVALID_COACH_ACRONYM"):
            _make_agent(coach="")


# ═══════════════════════════════════════════════════════════════════════
# § Receipt Chain Integration
# ═══════════════════════════════════════════════════════════════════════


class TestReceiptChain:
    def test_receipt_entry_contains_asset_id(self):
        agent, rc = _make_agent()
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        entries = rc.query(asset_id=r.validation_id)
        assert len(entries) == 1

    def test_receipt_metadata_has_coach(self):
        agent, rc = _make_agent()
        agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        entries = rc.query(action="gate-v04-validation")
        assert entries[0].metadata.get("coach") == "TST"

    def test_multiple_slides_create_multiple_receipts(self):
        agent, rc = _make_agent()
        for i in range(3):
            agent.validate_slide("VCB-TST-001", i, f"https://example.com/s{i}.png")
        entries = rc.query(action="gate-v04-validation")
        assert len(entries) == 3


# ═══════════════════════════════════════════════════════════════════════
# § Edge Cases
# ═══════════════════════════════════════════════════════════════════════


class TestEdgeCases:
    def test_agss_exactly_at_threshold_passes(self):
        """6.5 exactly should pass."""
        vision = _good_vision(agss={
            "lighting_naturalism": 6.5,
            "texture_authenticity": 6.5,
            "compositional_coherence": 6.5,
            "emotional_believability": 6.5,
        })
        agent, _ = _make_agent(vision=vision)
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        assert r.agss.result == "PASS"
        assert r.overall_verdict == ValidationVerdict.VALIDATED.value

    def test_agss_just_below_threshold_fails(self):
        """6.49 should fail."""
        vision = _good_vision(agss={
            "lighting_naturalism": 6.49,
            "texture_authenticity": 6.49,
            "compositional_coherence": 6.49,
            "emotional_believability": 6.49,
        })
        # make it double-fail for predictable escalation
        vision.score_agss.return_value = {
            "lighting_naturalism": 6.49,
            "texture_authenticity": 6.49,
            "compositional_coherence": 6.49,
            "emotional_believability": 6.49,
        }
        agent, _ = _make_agent(vision=vision)
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        assert r.overall_verdict == ValidationVerdict.PENDING_HUMAN_REVIEW.value

    def test_drift_exactly_at_threshold_passes(self):
        """0.30 should pass (≤ 0.30)."""
        vision = _good_vision(drift={"drift_score": 0.30})
        agent, _ = _make_agent(vision=vision)
        r = agent.validate_slide(
            "VCB-TST-001", 0, "https://example.com/img.png",
            reference_image_url="https://example.com/ref.png",
        )
        assert r.character_drift.result == "PASS"

    def test_drift_just_above_threshold_fails(self):
        """0.31 should fail."""
        vision = _double_failing_drift_vision(score=0.31)
        agent, _ = _make_agent(vision=vision)
        r = agent.validate_slide(
            "VCB-TST-001", 0, "https://example.com/img.png",
            reference_image_url="https://example.com/ref.png",
        )
        assert r.overall_verdict == ValidationVerdict.PENDING_HUMAN_REVIEW.value

    def test_vision_api_exception_degrades_agss(self):
        """If score_agss raises, AGSS should fail gracefully."""
        vision = _good_vision()
        vision.score_agss.side_effect = RuntimeError("API timeout")
        # auth/drift still pass but AGSS fails → remediation → second call also fails
        agent, _ = _make_agent(vision=vision)
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        assert r.overall_verdict == ValidationVerdict.PENDING_HUMAN_REVIEW.value
        assert any("AGSS scoring error" in w for w in r.warnings)

    def test_vision_api_exception_degrades_auth(self):
        """If check_authenticity raises, auth should fail gracefully."""
        vision = _good_vision()
        vision.check_authenticity.side_effect = RuntimeError("API timeout")
        agent, _ = _make_agent(vision=vision)
        r = agent.validate_slide("VCB-TST-001", 0, "https://example.com/img.png")
        assert r.overall_verdict == ValidationVerdict.PENDING_HUMAN_REVIEW.value

    def test_vision_api_exception_degrades_drift(self):
        """If detect_drift raises, drift should fail with score 1.0."""
        vision = _good_vision()
        vision.detect_drift.side_effect = RuntimeError("API timeout")
        agent, _ = _make_agent(vision=vision)
        r = agent.validate_slide(
            "VCB-TST-001", 0, "https://example.com/img.png",
            reference_image_url="https://example.com/ref.png",
        )
        assert r.character_drift.drift_score == 1.0


# ═══════════════════════════════════════════════════════════════════════
# § Model Validation
# ═══════════════════════════════════════════════════════════════════════


class TestModelValidation:
    def test_agss_component_clamped(self):
        with pytest.raises(Exception):
            AGSSComponentScores(
                lighting_naturalism=11.0,
                texture_authenticity=8.0,
                compositional_coherence=8.0,
                emotional_believability=8.0,
            )

    def test_agss_component_negative_rejected(self):
        with pytest.raises(Exception):
            AGSSComponentScores(
                lighting_naturalism=-1.0,
                texture_authenticity=8.0,
                compositional_coherence=8.0,
                emotional_believability=8.0,
            )

    def test_drift_score_clamped(self):
        with pytest.raises(Exception):
            CharacterDriftResult(
                drift_score=1.5,
                threshold=0.30,
                result="FAIL",
            )
