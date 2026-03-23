"""
FR-CBCS-02 — Social Penetration Depth Gauge — Integration Tests
================================================================
Covers 3 ACs + Stage 1/2 classification + Stage 3/4 gate + ADR-01 +
receipt chain + edge cases.
"""

from __future__ import annotations

import tempfile

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cbcs_models import (
    BLOCKED_MOOD_STATES,
    BlockingReason,
    COGNITIVE_PROCESSES_THRESHOLD,
    DELIVERY_COPING_MINIMUM,
    DELIVERY_SPT_MINIMUM,
    DeliveryPermissionGateEval,
    DeliveryVerdict,
    EMOTIONAL_COMPLEXITY_THRESHOLD,
    EXCLUSIVE_WORDS_THRESHOLD,
    FIRST_PERSON_FREQ_THRESHOLD,
    HEDGING_WORDS_THRESHOLD,
    LIWCScores,
    PROVISIONAL_DELAY_HOURS,
    SPTClassificationResult,
    SPTDepthGaugeRow,
    SPTError,
    SPTStage,
    TRAILING_WINDOW_14_DAYS,
    TRAILING_WINDOW_30_DAYS,
)
from src.ccp.services.delivery_gate_evaluator import DeliveryGateEvaluator
from src.ccp.services.spt_stage_engine import SPTStageEngine


# ═══════════════════════════════════════════════════════════════════════
# Fixtures & Helpers
# ═══════════════════════════════════════════════════════════════════════


def _make_engine(coach: str = "TST") -> tuple[SPTStageEngine, ReceiptChain]:
    tmp = tempfile.mkdtemp()
    rc = ReceiptChain(coach_acronym=coach, log_dir=tmp)
    engine = SPTStageEngine(
        coach_acronym=coach,
        coach_id="coach_test_uuid",
        receipt_chain=rc,
    )
    return engine, rc


def _make_gate(coach: str = "TST") -> tuple[DeliveryGateEvaluator, ReceiptChain]:
    tmp = tempfile.mkdtemp()
    rc = ReceiptChain(coach_acronym=coach, log_dir=tmp)
    gate = DeliveryGateEvaluator(
        coach_acronym=coach,
        coach_id="coach_test_uuid",
        receipt_chain=rc,
    )
    return gate, rc


def _orientation_liwc() -> LIWCScores:
    """LIWC scores that classify as Stage 1 Orientation."""
    return LIWCScores(
        first_person_freq=0.02,
        emotional_complexity=0.1,
    )


def _exploratory_liwc() -> LIWCScores:
    """LIWC scores that classify as Stage 2 Exploratory Affective."""
    return LIWCScores(
        first_person_freq=0.08,
        emotional_complexity=0.3,
        exclusive_words=0.05,
        hedging_words=0.08,
    )


def _affective_liwc() -> LIWCScores:
    """LIWC scores that classify as Stage 3 Affective Exchange."""
    return LIWCScores(
        first_person_freq=0.12,
        emotional_complexity=0.4,
        exclusive_words=0.15,
        hedging_words=0.02,
    )


def _stable_liwc_30d() -> LIWCScores:
    """30-day LIWC scores that classify as Stage 4 Stable Exchange."""
    return LIWCScores(
        first_person_freq=0.15,
        emotional_complexity=0.5,
        exclusive_words=0.2,
        hedging_words=0.01,
        cognitive_processes=0.25,
    )


# ═══════════════════════════════════════════════════════════════════════
# § Enums & Constants
# ═══════════════════════════════════════════════════════════════════════


class TestEnumsConstants:
    def test_spt_stage_members(self):
        assert SPTStage.ORIENTATION.value == 1
        assert SPTStage.EXPLORATORY_AFFECTIVE.value == 2
        assert SPTStage.AFFECTIVE_EXCHANGE.value == 3
        assert SPTStage.STABLE_EXCHANGE.value == 4

    def test_delivery_verdict_members(self):
        assert set(DeliveryVerdict.__members__.keys()) == {"PASS", "PROVISIONAL", "FAIL"}

    def test_blocking_reason_members(self):
        assert set(BlockingReason.__members__.keys()) == {
            "SPT_FAILED", "MOOD_FAILED", "COPING_FAILED",
        }

    def test_spt_error_members(self):
        assert len(SPTError.__members__) == 5

    def test_threshold_constants(self):
        assert FIRST_PERSON_FREQ_THRESHOLD == 0.05
        assert EMOTIONAL_COMPLEXITY_THRESHOLD == 0.2
        assert EXCLUSIVE_WORDS_THRESHOLD == 0.1
        assert HEDGING_WORDS_THRESHOLD == 0.05
        assert COGNITIVE_PROCESSES_THRESHOLD == 0.15
        assert DELIVERY_SPT_MINIMUM == 3
        assert DELIVERY_COPING_MINIMUM == 3
        assert PROVISIONAL_DELAY_HOURS == 24

    def test_blocked_mood_states(self):
        assert BLOCKED_MOOD_STATES == ["Processing", "Tension", "Escape"]

    def test_trailing_windows(self):
        assert TRAILING_WINDOW_14_DAYS == 14
        assert TRAILING_WINDOW_30_DAYS == 30


# ═══════════════════════════════════════════════════════════════════════
# § Stage 1+2: SPT Classification
# ═══════════════════════════════════════════════════════════════════════


class TestSPTClassification:
    def test_orientation_stage(self):
        engine, _ = _make_engine()
        result = engine.classify_client("client-001", _orientation_liwc())
        assert result.spt_stage == 1
        assert result.spt_stage_name == "ORIENTATION"

    def test_exploratory_affective_stage(self):
        engine, _ = _make_engine()
        result = engine.classify_client("client-002", _exploratory_liwc())
        assert result.spt_stage == 2
        assert result.spt_stage_name == "EXPLORATORY_AFFECTIVE"

    def test_affective_exchange_stage(self):
        engine, _ = _make_engine()
        result = engine.classify_client("client-003", _affective_liwc())
        assert result.spt_stage == 3
        assert result.spt_stage_name == "AFFECTIVE_EXCHANGE"

    def test_stable_exchange_stage(self):
        engine, _ = _make_engine()
        result = engine.classify_client(
            "client-004",
            _affective_liwc(),
            _stable_liwc_30d(),
        )
        assert result.spt_stage == 4
        assert result.spt_stage_name == "STABLE_EXCHANGE"

    def test_stable_requires_30d_window(self):
        """Without 30-day data, cannot reach Stable Exchange."""
        engine, _ = _make_engine()
        result = engine.classify_client("client-005", _affective_liwc(), None)
        assert result.spt_stage == 3  # falls back to Affective Exchange

    def test_stable_requires_affective_baseline(self):
        """30d data present but 14d doesn't reach Affective → no Stable."""
        engine, _ = _make_engine()
        result = engine.classify_client(
            "client-006",
            _exploratory_liwc(),
            _stable_liwc_30d(),
        )
        assert result.spt_stage == 2  # Exploratory, not Stable

    def test_trailing_window_14d_for_stages_1_to_3(self):
        engine, _ = _make_engine()
        r1 = engine.classify_client("c1", _orientation_liwc())
        r2 = engine.classify_client("c2", _exploratory_liwc())
        r3 = engine.classify_client("c3", _affective_liwc())
        assert r1.trailing_window_days == 14
        assert r2.trailing_window_days == 14
        assert r3.trailing_window_days == 14

    def test_trailing_window_30d_for_stage_4(self):
        engine, _ = _make_engine()
        result = engine.classify_client(
            "c4", _affective_liwc(), _stable_liwc_30d()
        )
        assert result.trailing_window_days == 30

    def test_liwc_snapshot_preserved(self):
        engine, _ = _make_engine()
        liwc = _affective_liwc()
        result = engine.classify_client("c1", liwc)
        assert result.liwc_snapshot.first_person_freq == liwc.first_person_freq

    def test_coach_id_set(self):
        engine, _ = _make_engine()
        result = engine.classify_client("c1", _orientation_liwc())
        assert result.coach_id == "coach_test_uuid"

    def test_timestamp_present(self):
        engine, _ = _make_engine()
        result = engine.classify_client("c1", _orientation_liwc())
        assert "T" in result.timestamp_utc  # ISO 8601


# ═══════════════════════════════════════════════════════════════════════
# § AC2: Safe Defaults / Missing Voice Profile
# ═══════════════════════════════════════════════════════════════════════


class TestAC2_SafeDefaults:
    def test_missing_voice_profile_defaults_to_orientation(self):
        engine, _ = _make_engine()
        result = engine.classify_client("client-no-data", None)
        assert result.spt_stage == 1
        assert result.spt_stage_name == "ORIENTATION"

    def test_missing_voice_profile_warning(self):
        engine, _ = _make_engine()
        result = engine.classify_client("client-no-data", None)
        assert any("MISSING_VOICE_PROFILE" in w for w in result.classification_warnings)

    def test_missing_voice_profile_no_crash(self):
        """Ensures no TypeError or crash — returns clean result."""
        engine, _ = _make_engine()
        result = engine.classify_client("client-no-data", None)
        assert isinstance(result, SPTClassificationResult)
        assert result.client_id == "client-no-data"

    def test_missing_profile_chains_to_gate_fail(self):
        """AC2: missing profile → stage 1 → gate Condition 1 fails → FAIL verdict."""
        engine, _ = _make_engine()
        result = engine.classify_client("client-empty", None)
        gate, _ = _make_gate()
        eval_result = gate.evaluate(
            client_id="client-empty",
            spt_stage=result.spt_stage,
            mood_state="Flow",
            coping_position=4,
        )
        assert eval_result.verdict == "FAIL"
        assert "SPT_FAILED" in eval_result.blocking_reason


# ═══════════════════════════════════════════════════════════════════════
# § Stage 3+4: Delivery Gate
# ═══════════════════════════════════════════════════════════════════════


class TestDeliveryGate:
    def test_all_pass(self):
        gate, _ = _make_gate()
        result = gate.evaluate("c1", spt_stage=3, mood_state="Flow", coping_position=4)
        assert result.verdict == "PASS"
        assert result.all_passed is True
        assert result.blocking_reason == []

    def test_spt_4_pass(self):
        gate, _ = _make_gate()
        result = gate.evaluate("c1", spt_stage=4, mood_state="Flow", coping_position=5)
        assert result.verdict == "PASS"

    def test_fail_spt_below_threshold(self):
        gate, _ = _make_gate()
        result = gate.evaluate("c1", spt_stage=2, mood_state="Flow", coping_position=4)
        assert result.verdict == "FAIL"
        assert "SPT_FAILED" in result.blocking_reason

    def test_fail_coping_below_threshold(self):
        gate, _ = _make_gate()
        result = gate.evaluate("c1", spt_stage=3, mood_state="Flow", coping_position=2)
        assert result.verdict == "FAIL"
        assert "COPING_FAILED" in result.blocking_reason

    def test_fail_both_spt_and_coping(self):
        gate, _ = _make_gate()
        result = gate.evaluate("c1", spt_stage=1, mood_state="Flow", coping_position=1)
        assert result.verdict == "FAIL"
        assert "SPT_FAILED" in result.blocking_reason
        assert "COPING_FAILED" in result.blocking_reason

    def test_gate_id_is_uuid(self):
        gate, _ = _make_gate()
        result = gate.evaluate("c1", spt_stage=3, mood_state="Flow", coping_position=3)
        assert len(result.gate_id) == 36  # UUID format

    def test_coach_id_propagated(self):
        gate, _ = _make_gate()
        result = gate.evaluate("c1", spt_stage=3, mood_state="Flow", coping_position=3)
        assert result.coach_id == "coach_test_uuid"


# ═══════════════════════════════════════════════════════════════════════
# § AC1: PROVISIONAL Verdict
# ═══════════════════════════════════════════════════════════════════════


class TestAC1_Provisional:
    def test_provisional_processing_mood(self):
        """AC1: spt=3, coping=4, mood=Processing → PROVISIONAL."""
        gate, _ = _make_gate()
        result = gate.evaluate("c1", spt_stage=3, mood_state="Processing", coping_position=4)
        assert result.verdict == "PROVISIONAL"
        assert result.provisional_delay_hours == 24

    def test_provisional_tension_mood(self):
        gate, _ = _make_gate()
        result = gate.evaluate("c1", spt_stage=3, mood_state="Tension", coping_position=3)
        assert result.verdict == "PROVISIONAL"

    def test_provisional_escape_mood(self):
        gate, _ = _make_gate()
        result = gate.evaluate("c1", spt_stage=4, mood_state="Escape", coping_position=5)
        assert result.verdict == "PROVISIONAL"

    def test_provisional_has_mood_blocking_reason(self):
        gate, _ = _make_gate()
        result = gate.evaluate("c1", spt_stage=3, mood_state="Processing", coping_position=4)
        assert "MOOD_FAILED" in result.blocking_reason
        assert "SPT_FAILED" not in result.blocking_reason
        assert "COPING_FAILED" not in result.blocking_reason

    def test_provisional_conditions_correct(self):
        gate, _ = _make_gate()
        result = gate.evaluate("c1", spt_stage=3, mood_state="Processing", coping_position=4)
        assert result.spt_condition is True
        assert result.mood_condition is False
        assert result.coping_condition is True
        assert result.all_passed is False

    def test_mood_fail_plus_spt_fail_is_not_provisional(self):
        """If spt also fails, it's FAIL not PROVISIONAL."""
        gate, _ = _make_gate()
        result = gate.evaluate("c1", spt_stage=2, mood_state="Processing", coping_position=4)
        assert result.verdict == "FAIL"

    def test_mood_fail_plus_coping_fail_is_not_provisional(self):
        gate, _ = _make_gate()
        result = gate.evaluate("c1", spt_stage=3, mood_state="Processing", coping_position=2)
        assert result.verdict == "FAIL"


# ═══════════════════════════════════════════════════════════════════════
# § AC3: Blocking Reason Exact Strings
# ═══════════════════════════════════════════════════════════════════════


class TestAC3_BlockingReasons:
    def test_coping_failed_string_exact(self):
        """AC3: coping < 3 → blocking_reason contains exactly 'COPING_FAILED'."""
        gate, _ = _make_gate()
        result = gate.evaluate("c1", spt_stage=3, mood_state="Flow", coping_position=2)
        assert "COPING_FAILED" in result.blocking_reason

    def test_spt_failed_string_exact(self):
        gate, _ = _make_gate()
        result = gate.evaluate("c1", spt_stage=1, mood_state="Flow", coping_position=4)
        assert "SPT_FAILED" in result.blocking_reason

    def test_mood_failed_string_exact(self):
        gate, _ = _make_gate()
        result = gate.evaluate("c1", spt_stage=3, mood_state="Tension", coping_position=3)
        assert "MOOD_FAILED" in result.blocking_reason

    def test_all_three_blocking_reasons(self):
        gate, _ = _make_gate()
        result = gate.evaluate("c1", spt_stage=1, mood_state="Processing", coping_position=1)
        assert "SPT_FAILED" in result.blocking_reason
        assert "MOOD_FAILED" in result.blocking_reason
        assert "COPING_FAILED" in result.blocking_reason

    def test_pass_has_empty_blocking_reason(self):
        gate, _ = _make_gate()
        result = gate.evaluate("c1", spt_stage=3, mood_state="Flow", coping_position=3)
        assert result.blocking_reason == []


# ═══════════════════════════════════════════════════════════════════════
# § Batch Classification
# ═══════════════════════════════════════════════════════════════════════


class TestBatch:
    def test_batch_classify_multiple(self):
        engine, _ = _make_engine()
        results = engine.classify_batch([
            {"client_id": "c1", "liwc_14d": _orientation_liwc()},
            {"client_id": "c2", "liwc_14d": _affective_liwc()},
            {"client_id": "c3"},  # missing → Orientation
        ])
        assert len(results) == 3
        assert results[0].spt_stage == 1
        assert results[1].spt_stage == 3
        assert results[2].spt_stage == 1

    def test_batch_with_30d(self):
        engine, _ = _make_engine()
        results = engine.classify_batch([
            {
                "client_id": "c4",
                "liwc_14d": _affective_liwc(),
                "liwc_30d": _stable_liwc_30d(),
            },
        ])
        assert results[0].spt_stage == 4


# ═══════════════════════════════════════════════════════════════════════
# § DB Row Conversion
# ═══════════════════════════════════════════════════════════════════════


class TestDBRow:
    def test_to_depth_gauge_row(self):
        engine, _ = _make_engine()
        result = engine.classify_client("c1", _affective_liwc())
        row = engine.to_depth_gauge_row(result, previous_stage=2)
        assert row.spt_stage == 3
        assert row.previous_stage == 2
        assert row.client_id == "c1"
        assert row.coach_id == "coach_test_uuid"

    def test_row_default_previous_stage(self):
        engine, _ = _make_engine()
        result = engine.classify_client("c1", _orientation_liwc())
        row = engine.to_depth_gauge_row(result)
        assert row.previous_stage == 1


# ═══════════════════════════════════════════════════════════════════════
# § ADR-01
# ═══════════════════════════════════════════════════════════════════════


class TestADR01:
    def test_engine_valid_coach(self):
        engine, _ = _make_engine(coach="TST")
        result = engine.classify_client("c1", _orientation_liwc())
        assert result.coach_id == "coach_test_uuid"

    def test_engine_1char_rejected(self):
        tmp = tempfile.mkdtemp()
        rc = ReceiptChain(coach_acronym="TST", log_dir=tmp)
        with pytest.raises(ValueError, match="INVALID_COACH_ACRONYM"):
            SPTStageEngine(coach_acronym="X", coach_id="test", receipt_chain=rc)

    def test_engine_5char_rejected(self):
        tmp = tempfile.mkdtemp()
        rc = ReceiptChain(coach_acronym="TST", log_dir=tmp)
        with pytest.raises(ValueError, match="INVALID_COACH_ACRONYM"):
            SPTStageEngine(coach_acronym="ABCDE", coach_id="test", receipt_chain=rc)

    def test_gate_1char_rejected(self):
        tmp = tempfile.mkdtemp()
        rc = ReceiptChain(coach_acronym="TST", log_dir=tmp)
        with pytest.raises(ValueError, match="INVALID_COACH_ACRONYM"):
            DeliveryGateEvaluator(coach_acronym="X", coach_id="test", receipt_chain=rc)

    def test_gate_5char_rejected(self):
        tmp = tempfile.mkdtemp()
        rc = ReceiptChain(coach_acronym="TST", log_dir=tmp)
        with pytest.raises(ValueError, match="INVALID_COACH_ACRONYM"):
            DeliveryGateEvaluator(coach_acronym="ABCDE", coach_id="test", receipt_chain=rc)


# ═══════════════════════════════════════════════════════════════════════
# § Receipt Chain
# ═══════════════════════════════════════════════════════════════════════


class TestReceiptChain:
    def test_classify_emits_receipt(self):
        engine, rc = _make_engine()
        engine.classify_client("c1", _orientation_liwc())
        entries = rc.query(action="spt-classify")
        assert len(entries) >= 1
        assert entries[0].asset_id == "c1"

    def test_classify_receipt_metadata(self):
        engine, rc = _make_engine()
        engine.classify_client("c1", _affective_liwc())
        entries = rc.query(action="spt-classify")
        assert entries[0].metadata["spt_stage"] == 3

    def test_gate_emits_receipt(self):
        gate, rc = _make_gate()
        gate.evaluate("c1", spt_stage=3, mood_state="Flow", coping_position=4)
        entries = rc.query(action="delivery-gate-eval")
        assert len(entries) >= 1
        assert entries[0].person_id == "c1"

    def test_gate_receipt_metadata(self):
        gate, rc = _make_gate()
        gate.evaluate("c1", spt_stage=3, mood_state="Flow", coping_position=4)
        entries = rc.query(action="delivery-gate-eval")
        assert entries[0].metadata["verdict"] == "PASS"

    def test_missing_profile_still_emits_receipt(self):
        engine, rc = _make_engine()
        engine.classify_client("c-empty", None)
        entries = rc.query(action="spt-classify")
        assert len(entries) >= 1
        assert entries[0].metadata["spt_stage"] == 1

    def test_batch_emits_receipt_per_client(self):
        engine, rc = _make_engine()
        engine.classify_batch([
            {"client_id": "c1", "liwc_14d": _orientation_liwc()},
            {"client_id": "c2", "liwc_14d": _affective_liwc()},
        ])
        entries = rc.query(action="spt-classify")
        assert len(entries) == 2


# ═══════════════════════════════════════════════════════════════════════
# § Model Validation
# ═══════════════════════════════════════════════════════════════════════


class TestModelValidation:
    def test_liwc_scores_clamped(self):
        with pytest.raises(Exception):
            LIWCScores(first_person_freq=1.5, emotional_complexity=0.3)

    def test_liwc_negative_rejected(self):
        with pytest.raises(Exception):
            LIWCScores(first_person_freq=-0.1, emotional_complexity=0.3)

    def test_spt_stage_bounds(self):
        with pytest.raises(Exception):
            SPTClassificationResult(
                client_id="c1", coach_id="x", spt_stage=5,
                spt_stage_name="X", trailing_window_days=14,
                liwc_snapshot=_orientation_liwc(), timestamp_utc="T",
            )

    def test_depth_gauge_row_stage_bounds(self):
        with pytest.raises(Exception):
            SPTDepthGaugeRow(
                client_id="c1", coach_id="x", spt_stage=0,
                spt_stage_name="X", trailing_window_days=14,
                last_computed_utc="T",
            )


# ═══════════════════════════════════════════════════════════════════════
# § Backward Compatibility (§6)
# ═══════════════════════════════════════════════════════════════════════


class TestBackwardCompatibility:
    def test_legacy_client_no_voice_data_held(self):
        """§6: Active client without Voice DNA → stage 1 → gate FAIL."""
        engine, _ = _make_engine()
        result = engine.classify_client("legacy-client", None)
        assert result.spt_stage == 1

        gate, _ = _make_gate()
        eval_result = gate.evaluate(
            "legacy-client", spt_stage=result.spt_stage,
            mood_state="Flow", coping_position=4,
        )
        assert eval_result.verdict == "FAIL"
        assert "SPT_FAILED" in eval_result.blocking_reason

    def test_legacy_client_not_false_elevated(self):
        """Missing data must NOT produce stage > 1."""
        engine, _ = _make_engine()
        result = engine.classify_client("legacy-client", None)
        assert result.spt_stage == 1
