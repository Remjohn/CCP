"""
FR-CBCS-10 — Deep Disclosure Protocol — Integration Tests
===========================================================
Tests for InteractionModeRouter, CasaLinguisticValidator covering
all 3 ACs plus edge cases.
"""

from __future__ import annotations

import tempfile

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cbcs_models import (
    CasaVerdict,
    DisclosureError,
    InteractionMode,
)
from src.ccp.services.deep_disclosure_protocol import (
    CasaLinguisticValidator,
    InteractionModeRouter,
)


# ── Helpers ────────────────────────────────────────────────────────────

def _make_router(coach: str = "TST") -> tuple[InteractionModeRouter, ReceiptChain]:
    tmp = tempfile.mkdtemp()
    rc = ReceiptChain(coach_acronym=coach, log_dir=tmp)
    router = InteractionModeRouter(coach_acronym=coach, receipt_chain=rc)
    return router, rc


def _make_validator(coach: str = "TST") -> tuple[CasaLinguisticValidator, ReceiptChain]:
    tmp = tempfile.mkdtemp()
    rc = ReceiptChain(coach_acronym=coach, log_dir=tmp)
    val = CasaLinguisticValidator(coach_acronym=coach, receipt_chain=rc)
    return val, rc


# ════════════════════════════════════════════════════════════════════════
# 1. Constructor & ADR-01
# ════════════════════════════════════════════════════════════════════════

class TestConstructor:
    def test_valid_coach_2_char_router(self) -> None:
        r, _ = _make_router("TS")
        assert r is not None

    def test_valid_coach_4_char_validator(self) -> None:
        v, _ = _make_validator("TEST")
        assert v is not None

    def test_invalid_coach_1_char_router(self) -> None:
        with pytest.raises(ValueError, match="INVALID_COACH_SCOPE"):
            _make_router("T")

    def test_invalid_coach_5_char_router(self) -> None:
        with pytest.raises(ValueError, match="INVALID_COACH_SCOPE"):
            _make_router("TESTI")

    def test_invalid_coach_1_char_validator(self) -> None:
        with pytest.raises(ValueError, match="INVALID_COACH_SCOPE"):
            _make_validator("T")

    def test_invalid_coach_5_char_validator(self) -> None:
        with pytest.raises(ValueError, match="INVALID_COACH_SCOPE"):
            _make_validator("TESTI")


# ════════════════════════════════════════════════════════════════════════
# 2. Interaction Mode Routing (Stage 1)
# ════════════════════════════════════════════════════════════════════════

class TestModeRouting:
    """Test 3-mode interaction routing based on LIWC + SPT."""

    def test_vulnerable_reception_high_neg_emotion(self) -> None:
        router, _ = _make_router()
        mode = router.route(negative_emotion=0.08)
        assert mode == InteractionMode.VULNERABLE_RECEPTION

    def test_elevated_challenge_high_cog_high_spt(self) -> None:
        router, _ = _make_router()
        mode = router.route(cognitive_processes=0.15, spt_stage=3)
        assert mode == InteractionMode.ELEVATED_CHALLENGE

    def test_elevated_challenge_needs_spt_3(self) -> None:
        """cognitive_processes high but spt=2 → fallback, not ELEVATED."""
        router, _ = _make_router()
        mode = router.route(cognitive_processes=0.15, spt_stage=2)
        # Falls through to default
        assert mode == InteractionMode.ACTIVE_CONSTRUCTIVE_RESPONDING

    def test_ac3_active_constructive_pos_emotion(self) -> None:
        """AC3: positive_emotion=0.08 → ACTIVE_CONSTRUCTIVE_RESPONDING."""
        router, _ = _make_router()
        mode = router.route(positive_emotion=0.08)
        assert mode == InteractionMode.ACTIVE_CONSTRUCTIVE_RESPONDING

    def test_vulnerable_priority_over_elevated(self) -> None:
        """Negative emotion takes priority over cognitive processes."""
        router, _ = _make_router()
        mode = router.route(negative_emotion=0.08, cognitive_processes=0.15, spt_stage=4)
        assert mode == InteractionMode.VULNERABLE_RECEPTION

    def test_default_fallback(self) -> None:
        """All scores at 0 → default to ACTIVE_CONSTRUCTIVE_RESPONDING."""
        router, _ = _make_router()
        mode = router.route()
        assert mode == InteractionMode.ACTIVE_CONSTRUCTIVE_RESPONDING

    def test_routing_receipt_logged(self) -> None:
        router, rc = _make_router()
        router.route(positive_emotion=0.08)
        entries = rc.query(action="disclosure-mode-route")
        assert len(entries) == 1
        assert entries[0].decision == "ACTIVE_CONSTRUCTIVE_RESPONDING"


# ════════════════════════════════════════════════════════════════════════
# 3. Static CASA Metrics (Stage 2)
# ════════════════════════════════════════════════════════════════════════

class TestFirstPersonCount:
    def test_multiple_fp(self) -> None:
        count = CasaLinguisticValidator.count_first_person_singular(
            "I hear you. This is my perspective and I believe in mine."
        )
        # I, my, I, mine → 4
        assert count == 4

    def test_zero_fp(self) -> None:
        count = CasaLinguisticValidator.count_first_person_singular(
            "The system processes data efficiently."
        )
        assert count == 0

    def test_case_insensitive_me(self) -> None:
        count = CasaLinguisticValidator.count_first_person_singular("tell ME something")
        assert count >= 1


class TestRoboticCount:
    def test_as_an_ai(self) -> None:
        count = CasaLinguisticValidator.count_robotic_qualifiers(
            "I understand. As an AI language model, I process data."
        )
        assert count >= 1

    def test_assistant_keyword(self) -> None:
        count = CasaLinguisticValidator.count_robotic_qualifiers(
            "I am your assistant and I am here to help."
        )
        # "assistant" + "I am here to help" → 2
        assert count == 2

    def test_clean_draft(self) -> None:
        count = CasaLinguisticValidator.count_robotic_qualifiers(
            "I hear you. That takes real courage."
        )
        assert count == 0


class TestQuestionCount:
    def test_two_questions(self) -> None:
        count = CasaLinguisticValidator.count_reflective_questions(
            "I hear you. Why did you do that? What else are you feeling?"
        )
        assert count == 2

    def test_one_question(self) -> None:
        count = CasaLinguisticValidator.count_reflective_questions(
            "I hear you. What made you most proud?"
        )
        assert count == 1

    def test_zero_questions(self) -> None:
        count = CasaLinguisticValidator.count_reflective_questions(
            "I hear you. That took real strength."
        )
        assert count == 0


class TestTrimmer:
    def test_trim_to_first_question(self) -> None:
        """AC2 trimming: only first question survives."""
        result = CasaLinguisticValidator.trim_to_first_question(
            "I hear you. Why did you do that? What else are you feeling?"
        )
        assert "Why did you do that?" in result
        assert "What else are you feeling?" not in result

    def test_single_question_no_trim(self) -> None:
        draft = "I hear you. What made you proud?"
        result = CasaLinguisticValidator.trim_to_first_question(draft)
        assert result == draft

    def test_no_question_no_trim(self) -> None:
        draft = "I hear you. That was beautiful."
        result = CasaLinguisticValidator.trim_to_first_question(draft)
        assert result == draft


# ════════════════════════════════════════════════════════════════════════
# 4. Full CASA Gate Validation (Stage 3)
# ════════════════════════════════════════════════════════════════════════

class TestCasaPass:
    def test_full_pass(self) -> None:
        val, _ = _make_validator()
        row = val.validate(
            "client-001",
            "I hear you. What made you most proud?",
            InteractionMode.ACTIVE_CONSTRUCTIVE_RESPONDING,
        )
        assert row.casa_verdict == CasaVerdict.PASS.value
        assert row.metrics_payload.fp_count > 0
        assert row.metrics_payload.robotic_count == 0
        assert row.metrics_payload.question_count <= 1
        assert row.final_dispatched_text == "I hear you. What made you most proud?"

    def test_pass_no_questions(self) -> None:
        val, _ = _make_validator()
        row = val.validate(
            "c1",
            "I see your strength in this moment.",
            InteractionMode.VULNERABLE_RECEPTION,
        )
        assert row.casa_verdict == CasaVerdict.PASS.value

    def test_pass_receipt_logged(self) -> None:
        val, rc = _make_validator()
        val.validate("c1", "I hear you.", InteractionMode.VULNERABLE_RECEPTION)
        entries = rc.query(action="casa-linguistic-validate")
        assert len(entries) == 1
        assert entries[0].decision == "PASS"


class TestCasaFail:
    def test_ac1_robotic_qualifier_fail(self) -> None:
        """AC1: 'I understand. As an AI language model...' → robotic=1 → FAIL_REWRITE."""
        val, _ = _make_validator()
        row = val.validate(
            "client-001",
            "I understand. As an AI language model, I can assist you.",
            InteractionMode.ACTIVE_CONSTRUCTIVE_RESPONDING,
        )
        assert row.casa_verdict == CasaVerdict.FAIL_REWRITE.value
        assert row.metrics_payload.robotic_count >= 1

    def test_no_first_person_fail(self) -> None:
        """No I/me/my/mine → FAIL even without robotic."""
        val, _ = _make_validator()
        row = val.validate(
            "c1",
            "The world is a beautiful place.",
            InteractionMode.ACTIVE_CONSTRUCTIVE_RESPONDING,
        )
        assert row.casa_verdict == CasaVerdict.FAIL_REWRITE.value
        assert row.metrics_payload.fp_count == 0

    def test_fail_receipt_logged(self) -> None:
        val, rc = _make_validator()
        val.validate(
            "c1",
            "As an AI, I am here to help you.",
            InteractionMode.ACTIVE_CONSTRUCTIVE_RESPONDING,
        )
        entries = rc.query(action="casa-linguistic-validate")
        assert len(entries) == 1
        assert entries[0].decision == "FAIL_REWRITE"


class TestCasaProvisional:
    def test_ac2_interrogation_trimming(self) -> None:
        """AC2: Two questions → PROVISIONAL_TRIMMED, second question removed."""
        val, _ = _make_validator()
        row = val.validate(
            "client-001",
            "I hear you. Why did you do that? What else are you feeling?",
            InteractionMode.VULNERABLE_RECEPTION,
        )
        assert row.casa_verdict == CasaVerdict.PROVISIONAL_TRIMMED.value
        assert row.metrics_payload.question_count == 2
        assert "Why did you do that?" in row.final_dispatched_text
        assert "What else are you feeling?" not in row.final_dispatched_text

    def test_provisional_receipt_logged(self) -> None:
        val, rc = _make_validator()
        val.validate(
            "c1",
            "I hear you. Why? What else?",
            InteractionMode.VULNERABLE_RECEPTION,
        )
        entries = rc.query(action="casa-linguistic-validate")
        assert len(entries) == 1
        assert entries[0].decision == "PROVISIONAL_TRIMMED"


class TestEmptyDraft:
    def test_empty_string_fail(self) -> None:
        val, _ = _make_validator()
        row = val.validate("c1", "", InteractionMode.ACTIVE_CONSTRUCTIVE_RESPONDING)
        assert row.casa_verdict == CasaVerdict.FAIL_REWRITE.value
        assert row.final_dispatched_text == ""

    def test_whitespace_only_fail(self) -> None:
        val, _ = _make_validator()
        row = val.validate("c1", "   \n  ", InteractionMode.ACTIVE_CONSTRUCTIVE_RESPONDING)
        assert row.casa_verdict == CasaVerdict.FAIL_REWRITE.value


# ════════════════════════════════════════════════════════════════════════
# 5. Output Schema Integrity
# ════════════════════════════════════════════════════════════════════════

class TestOutputSchema:
    def test_interaction_id_is_uuid(self) -> None:
        val, _ = _make_validator()
        row = val.validate("c1", "I hear you.", InteractionMode.VULNERABLE_RECEPTION)
        import uuid
        uuid.UUID(row.interaction_id)

    def test_timestamp_is_iso8601(self) -> None:
        val, _ = _make_validator()
        row = val.validate("c1", "I hear you.", InteractionMode.VULNERABLE_RECEPTION)
        from datetime import datetime
        datetime.fromisoformat(row.timestamp_utc)

    def test_coach_id_matches(self) -> None:
        val, _ = _make_validator("TST")
        row = val.validate("c1", "I hear you.", InteractionMode.VULNERABLE_RECEPTION)
        assert row.coach_id == "TST"

    def test_interaction_mode_stored(self) -> None:
        val, _ = _make_validator()
        row = val.validate("c1", "I hear you.", InteractionMode.ELEVATED_CHALLENGE)
        assert row.interaction_mode == InteractionMode.ELEVATED_CHALLENGE.value


# ════════════════════════════════════════════════════════════════════════
# 6. C-11 Persona Masking
# ════════════════════════════════════════════════════════════════════════

class TestPersonaMasking:
    def test_no_agent_name_in_result(self) -> None:
        val, _ = _make_validator()
        row = val.validate("c1", "I hear you.", InteractionMode.VULNERABLE_RECEPTION)
        dump = row.model_dump_json()
        assert "casa-linguistic-validator" not in dump
        assert "interaction-mode-router" not in dump
