"""
FR-CBCS-08 — Transportation Score Gate — Integration Tests
===========================================================
Tests for TransportationScoreEvaluator covering all 3 ACs plus edge cases.
"""

from __future__ import annotations

import tempfile

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cbcs_models import (
    DISTANCING_WORDS,
    PROSODIC_MATCH_THRESHOLD,
    SENSORY_WORDS,
    TransportGateError,
    TransportGateVerdict,
)
from src.ccp.services.transportation_score_gate import TransportationScoreEvaluator


# ── Helpers ────────────────────────────────────────────────────────────

def _make_evaluator(coach: str = "TST") -> tuple[TransportationScoreEvaluator, ReceiptChain]:
    tmp = tempfile.mkdtemp()
    rc = ReceiptChain(coach_acronym=coach, log_dir=tmp)
    ev = TransportationScoreEvaluator(coach_acronym=coach, receipt_chain=rc)
    return ev, rc


def _aligned_vectors(dim: int = 5, value: float = 1.0) -> tuple[list[float], list[float]]:
    """Return two identical vectors → cosine similarity = 1.0."""
    v = [value] * dim
    return v, list(v)


def _partial_vectors(dim: int = 5) -> tuple[list[float], list[float]]:
    """Return vectors yielding cosine sim ≈ 0.5 (below threshold)."""
    a = [1.0, 0.0, 1.0, 0.0, 1.0]
    b = [0.0, 1.0, 0.0, 1.0, 0.0]
    return a, b


# Draft snippets
_SENSORY_ARC_DRAFT = (
    "I was sitting in a dark room, feeling the cold air. "
    "Now I am standing in bright sunlight."
)
_NO_SENSORY_ARC_DRAFT = (
    "I was thinking about all those moments long ago. "
    "Now I am ready to move forward into a new chapter."
)
_DISTANCING_DRAFT = "I think maybe we should focus on something new."
_NO_ARC_DRAFT = "The sky is bright and the air feels cold and heavy."
_EMPTY_DRAFT = ""
_WHITESPACE_DRAFT = "   \n  \t  "


# ════════════════════════════════════════════════════════════════════════
# 1. Constructor & ADR-01
# ════════════════════════════════════════════════════════════════════════

class TestConstructor:
    """ADR-01 coach scope enforcement."""

    def test_valid_coach_2_char(self) -> None:
        ev, _ = _make_evaluator("TS")
        assert ev is not None

    def test_valid_coach_4_char(self) -> None:
        ev, _ = _make_evaluator("TEST")
        assert ev is not None

    def test_invalid_coach_1_char(self) -> None:
        with pytest.raises(ValueError, match="INVALID_COACH_SCOPE"):
            _make_evaluator("T")

    def test_invalid_coach_5_char(self) -> None:
        with pytest.raises(ValueError, match="INVALID_COACH_SCOPE"):
            _make_evaluator("TESTI")


# ════════════════════════════════════════════════════════════════════════
# 2. Static Component Analysis (Stage 2)
# ════════════════════════════════════════════════════════════════════════

class TestSensoryCount:
    """Sensory detail word counting."""

    def test_multiple_sensory_words(self) -> None:
        count = TransportationScoreEvaluator.count_sensory_details(
            "I see the dark room and feel the cold breeze."
        )
        # see, dark, feel, cold → 4
        assert count == 4

    def test_zero_sensory(self) -> None:
        count = TransportationScoreEvaluator.count_sensory_details(
            "This is a purely abstract philosophical statement."
        )
        assert count == 0

    def test_case_insensitive(self) -> None:
        count = TransportationScoreEvaluator.count_sensory_details("SEE HEAR FEEL")
        assert count == 3

    def test_all_13_sensory_words(self) -> None:
        draft = " ".join(SENSORY_WORDS)
        count = TransportationScoreEvaluator.count_sensory_details(draft)
        assert count == 13


class TestDistancingCount:
    """Distancing language counting — zero tolerance."""

    def test_two_distancing_words(self) -> None:
        count = TransportationScoreEvaluator.count_distancing_language(
            "I think maybe we should focus."
        )
        # "I think", "maybe" → 2
        assert count == 2

    def test_zero_distancing(self) -> None:
        count = TransportationScoreEvaluator.count_distancing_language(
            "You are the sovereign authority of your life."
        )
        assert count == 0

    def test_all_9_distancing_words(self) -> None:
        draft = " and ".join(DISTANCING_WORDS)
        count = TransportationScoreEvaluator.count_distancing_language(draft)
        assert count == len(DISTANCING_WORDS)

    def test_case_insensitive_distancing(self) -> None:
        count = TransportationScoreEvaluator.count_distancing_language(
            "MAYBE PERHAPS I THINK"
        )
        assert count == 3


class TestProsodicMatch:
    """Cosine similarity for Voice DNA parity."""

    def test_identical_vectors(self) -> None:
        a, b = _aligned_vectors()
        score = TransportationScoreEvaluator.compute_prosodic_match(a, b)
        assert score == pytest.approx(1.0)

    def test_orthogonal_vectors(self) -> None:
        a, b = _partial_vectors()
        score = TransportationScoreEvaluator.compute_prosodic_match(a, b)
        assert score < PROSODIC_MATCH_THRESHOLD

    def test_empty_vectors(self) -> None:
        score = TransportationScoreEvaluator.compute_prosodic_match([], [])
        assert score == 0.0

    def test_zero_magnitude_vector(self) -> None:
        score = TransportationScoreEvaluator.compute_prosodic_match(
            [0.0, 0.0, 0.0], [1.0, 1.0, 1.0]
        )
        assert score == 0.0

    def test_mismatched_lengths(self) -> None:
        score = TransportationScoreEvaluator.compute_prosodic_match(
            [1.0, 2.0], [1.0, 2.0, 3.0]
        )
        assert score == 0.0


class TestNarrativeArc:
    """Past→present/future tense shift detection."""

    def test_valid_arc(self) -> None:
        assert TransportationScoreEvaluator.detect_narrative_arc(
            "I was lost in darkness. Now I am standing in the light."
        ) is True

    def test_no_past_tense(self) -> None:
        assert TransportationScoreEvaluator.detect_narrative_arc(
            "I am here now. I will go forward."
        ) is False

    def test_no_present_future(self) -> None:
        assert TransportationScoreEvaluator.detect_narrative_arc(
            "I was sitting there. I felt alone. I remembered."
        ) is False

    def test_wrong_order(self) -> None:
        # Present before past — not a valid arc
        assert TransportationScoreEvaluator.detect_narrative_arc(
            "Now I am free. Back then I was trapped."
        ) is False

    def test_empty_string(self) -> None:
        assert TransportationScoreEvaluator.detect_narrative_arc("") is False


# ════════════════════════════════════════════════════════════════════════
# 3. Full Evaluation (Stage 3 Gate)
# ════════════════════════════════════════════════════════════════════════

class TestEvaluatePass:
    """PASS verdict — all 4 conditions met."""

    def test_full_pass(self) -> None:
        ev, rc = _make_evaluator()
        a, b = _aligned_vectors()
        result = ev.evaluate(_SENSORY_ARC_DRAFT, a, b)
        assert result.gate_verdict == TransportGateVerdict.PASS.value
        assert result.metrics_payload.sensory_count > 0
        assert result.metrics_payload.distancing_count == 0
        assert result.metrics_payload.prosodic_match_score >= PROSODIC_MATCH_THRESHOLD
        assert result.metrics_payload.narrative_arc_found is True
        assert result.failure_details == []
        assert len(result.evaluation_id) == 36  # UUID format
        assert len(result.script_hash) == 64  # SHA-256

    def test_pass_failure_details_empty_array(self) -> None:
        """AC3: PASS verdict MUST return failure_details as explicitly empty array []."""
        ev, _ = _make_evaluator()
        a, b = _aligned_vectors()
        result = ev.evaluate(_SENSORY_ARC_DRAFT, a, b)
        assert result.gate_verdict == TransportGateVerdict.PASS.value
        assert result.failure_details == []
        assert isinstance(result.failure_details, list)

    def test_pass_receipt_logged(self) -> None:
        ev, rc = _make_evaluator()
        a, b = _aligned_vectors()
        ev.evaluate(_SENSORY_ARC_DRAFT, a, b)
        entries = rc.query(action="transportation-gate-evaluate")
        assert len(entries) == 1
        assert entries[0].decision == "PASS"


class TestEvaluateFail:
    """FAIL verdict — Condition 2, 3, or 4 violated."""

    def test_ac1_distancing_language_fail(self) -> None:
        """AC1: 'I think maybe we should focus on...' → distancing_count=2 → FAIL."""
        ev, _ = _make_evaluator()
        a, b = _aligned_vectors()
        result = ev.evaluate(_DISTANCING_DRAFT, a, b)
        assert result.gate_verdict == TransportGateVerdict.FAIL.value
        assert result.metrics_payload.distancing_count == 2
        assert any("Condition 2" in d for d in result.failure_details)

    def test_fail_no_narrative_arc(self) -> None:
        """No tense transition → Condition 4 fails."""
        ev, _ = _make_evaluator()
        a, b = _aligned_vectors()
        result = ev.evaluate(_NO_ARC_DRAFT, a, b)
        assert result.gate_verdict == TransportGateVerdict.FAIL.value
        assert result.metrics_payload.narrative_arc_found is False
        assert any("Condition 4" in d for d in result.failure_details)

    def test_fail_low_prosodic_match(self) -> None:
        """Orthogonal vectors → Condition 3 fails."""
        ev, _ = _make_evaluator()
        a, b = _partial_vectors()
        result = ev.evaluate(_SENSORY_ARC_DRAFT, a, b)
        assert result.gate_verdict == TransportGateVerdict.FAIL.value
        assert result.metrics_payload.prosodic_match_score < PROSODIC_MATCH_THRESHOLD
        assert any("Condition 3" in d for d in result.failure_details)

    def test_fail_multiple_conditions(self) -> None:
        """Multiple conditions fail simultaneously."""
        ev, _ = _make_evaluator()
        a, b = _partial_vectors()
        result = ev.evaluate(_DISTANCING_DRAFT, a, b)
        assert result.gate_verdict == TransportGateVerdict.FAIL.value
        assert len(result.failure_details) >= 2

    def test_fail_receipt_logged(self) -> None:
        ev, rc = _make_evaluator()
        a, b = _aligned_vectors()
        result = ev.evaluate(_DISTANCING_DRAFT, a, b)
        entries = rc.query(action="transportation-gate-evaluate")
        assert len(entries) == 1
        assert entries[0].decision == "FAIL"


class TestEvaluateProvisional:
    """PROVISIONAL_REVIEW — only Condition 1 (sensory) fails."""

    def test_ac2_provisional_no_sensory(self) -> None:
        """AC2: Passes distancing, prosodic 0.88, narrative arc, BUT zero sensory → PROVISIONAL_REVIEW."""
        ev, _ = _make_evaluator()
        a, b = _aligned_vectors()
        result = ev.evaluate(_NO_SENSORY_ARC_DRAFT, a, b)
        assert result.gate_verdict == TransportGateVerdict.PROVISIONAL_REVIEW.value
        assert result.metrics_payload.sensory_count == 0
        assert result.metrics_payload.distancing_count == 0
        assert result.metrics_payload.narrative_arc_found is True
        assert result.failure_details == []

    def test_provisional_receipt_logged(self) -> None:
        ev, rc = _make_evaluator()
        a, b = _aligned_vectors()
        ev.evaluate(_NO_SENSORY_ARC_DRAFT, a, b)
        entries = rc.query(action="transportation-gate-evaluate")
        assert len(entries) == 1
        assert entries[0].decision == "PROVISIONAL_REVIEW"


class TestEmptyScript:
    """Empty/whitespace script → immediate FAIL with SCRIPT_EMPTY."""

    def test_empty_string(self) -> None:
        ev, _ = _make_evaluator()
        result = ev.evaluate(_EMPTY_DRAFT)
        assert result.gate_verdict == TransportGateVerdict.FAIL.value
        assert TransportGateError.SCRIPT_EMPTY.value in result.failure_details

    def test_whitespace_only(self) -> None:
        ev, _ = _make_evaluator()
        result = ev.evaluate(_WHITESPACE_DRAFT)
        assert result.gate_verdict == TransportGateVerdict.FAIL.value
        assert TransportGateError.SCRIPT_EMPTY.value in result.failure_details

    def test_empty_script_receipt(self) -> None:
        ev, rc = _make_evaluator()
        ev.evaluate(_EMPTY_DRAFT)
        entries = rc.query(action="transportation-gate-evaluate")
        assert len(entries) == 1
        assert entries[0].decision == "FAIL"


# ════════════════════════════════════════════════════════════════════════
# 4. Output Schema Integrity (Stage 4)
# ════════════════════════════════════════════════════════════════════════

class TestOutputSchema:
    """Verify output field resolution rules (§4 Stage 4)."""

    def test_evaluation_id_is_uuid(self) -> None:
        ev, _ = _make_evaluator()
        a, b = _aligned_vectors()
        result = ev.evaluate(_SENSORY_ARC_DRAFT, a, b)
        import uuid as _uuid
        _uuid.UUID(result.evaluation_id)  # raises if invalid

    def test_script_hash_is_sha256(self) -> None:
        ev, _ = _make_evaluator()
        a, b = _aligned_vectors()
        result = ev.evaluate(_SENSORY_ARC_DRAFT, a, b)
        assert len(result.script_hash) == 64
        int(result.script_hash, 16)  # raises if not valid hex

    def test_evaluated_at_is_iso8601(self) -> None:
        ev, _ = _make_evaluator()
        a, b = _aligned_vectors()
        result = ev.evaluate(_SENSORY_ARC_DRAFT, a, b)
        from datetime import datetime
        datetime.fromisoformat(result.evaluated_at)  # raises if invalid

    def test_deterministic_hash(self) -> None:
        ev, _ = _make_evaluator()
        a, b = _aligned_vectors()
        r1 = ev.evaluate(_SENSORY_ARC_DRAFT, a, b)
        r2 = ev.evaluate(_SENSORY_ARC_DRAFT, a, b)
        assert r1.script_hash == r2.script_hash

    def test_unique_evaluation_ids(self) -> None:
        ev, _ = _make_evaluator()
        a, b = _aligned_vectors()
        r1 = ev.evaluate(_SENSORY_ARC_DRAFT, a, b)
        r2 = ev.evaluate(_SENSORY_ARC_DRAFT, a, b)
        assert r1.evaluation_id != r2.evaluation_id


# ════════════════════════════════════════════════════════════════════════
# 5. Prosodic Match Defaults
# ════════════════════════════════════════════════════════════════════════

class TestProsodicDefaults:
    """When syntax vectors are None, prosodic_match defaults to 0.0."""

    def test_no_vectors_prosodic_zero(self) -> None:
        ev, _ = _make_evaluator()
        result = ev.evaluate(_SENSORY_ARC_DRAFT)
        assert result.metrics_payload.prosodic_match_score == 0.0
        # prosodic=0.0 < 0.85 → Condition 3 fails → FAIL
        assert result.gate_verdict == TransportGateVerdict.FAIL.value

    def test_only_draft_frequencies_none_baseline(self) -> None:
        ev, _ = _make_evaluator()
        result = ev.evaluate(_SENSORY_ARC_DRAFT, [1.0, 1.0], None)
        assert result.metrics_payload.prosodic_match_score == 0.0


# ════════════════════════════════════════════════════════════════════════
# 6. C-11 Persona Masking
# ════════════════════════════════════════════════════════════════════════

class TestPersonaMasking:
    """Agent names must NOT leak into external payloads (C-11)."""

    def test_no_agent_name_in_result(self) -> None:
        ev, _ = _make_evaluator()
        a, b = _aligned_vectors()
        result = ev.evaluate(_SENSORY_ARC_DRAFT, a, b)
        dump = result.model_dump_json()
        assert "transportation-score-evaluator" not in dump
