"""
FR-CBCS-07 — Telegram Intimacy Index — Integration Tests
=========================================================
Covers 3 ACs + 6-component math + PSR classification + TII gate +
ADR-01 + receipt chain + backward compatibility + edge cases.
"""

from __future__ import annotations

import tempfile

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cbcs_models import (
    ClientMessageStats,
    PSR_BORDERLINE_THRESHOLD,
    PSR_INTENSE_PERSONAL_THRESHOLD,
    PSRStage,
    TII_PASS_THRESHOLD,
    TII_PROVISIONAL_CONSISTENCY,
    TII_PROVISIONAL_FLOOR,
    TII_WEIGHT_CONSISTENCY,
    TII_WEIGHT_DISCLOSURE,
    TII_WEIGHT_FREQUENCY,
    TII_WEIGHT_INITIATIVE,
    TII_WEIGHT_LATENCY,
    TII_WEIGHT_VOICE,
    TIIError,
    TIIGateResult,
    TIIVerdict,
    TelegramIntimacyIndexRow,
)
from src.ccp.services.tii_calculator import TIICalculator


# ═══════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════


def _make_calc(coach: str = "TST") -> tuple[TIICalculator, ReceiptChain]:
    tmp = tempfile.mkdtemp()
    rc = ReceiptChain(coach_acronym=coach, log_dir=tmp)
    calc = TIICalculator(coach_acronym=coach, coach_id="coach-tii-uuid", receipt_chain=rc)
    return calc, rc


def _active_client() -> ClientMessageStats:
    """A highly engaged client → high TII."""
    return ClientMessageStats(
        client_id="client-active",
        message_count=60,
        days_active_in_last_30=25,
        avg_response_time_hours=2.0,
        voice_message_count=20,
        total_client_messages=50,
        days_client_initiated=20,
        spt_stage=3,
    )


def _passive_client() -> ClientMessageStats:
    """A passive client → low TII."""
    return ClientMessageStats(
        client_id="client-passive",
        message_count=5,
        days_active_in_last_30=3,
        avg_response_time_hours=20.0,
        voice_message_count=0,
        total_client_messages=5,
        days_client_initiated=1,
        spt_stage=1,
    )


def _zero_activity_client() -> ClientMessageStats:
    """Zero messages, zero activity → all 0.0."""
    return ClientMessageStats(
        client_id="client-zero",
        message_count=0,
        days_active_in_last_30=0,
        avg_response_time_hours=24.0,
        voice_message_count=0,
        total_client_messages=0,
        days_client_initiated=0,
        spt_stage=1,
    )


# ═══════════════════════════════════════════════════════════════════════
# § Enums & Constants
# ═══════════════════════════════════════════════════════════════════════


class TestEnumsConstants:
    def test_psr_stage_members(self):
        assert PSRStage.ENTERTAINMENT_SOCIAL.value == "Entertainment-Social"
        assert PSRStage.INTENSE_PERSONAL.value == "Intense-Personal"
        assert PSRStage.BORDERLINE.value == "Borderline"

    def test_tii_verdict_members(self):
        assert set(TIIVerdict.__members__.keys()) == {"PASS", "PROVISIONAL", "FAIL"}

    def test_weight_sum_equals_one(self):
        total = (
            TII_WEIGHT_FREQUENCY + TII_WEIGHT_CONSISTENCY
            + TII_WEIGHT_DISCLOSURE + TII_WEIGHT_LATENCY
            + TII_WEIGHT_VOICE + TII_WEIGHT_INITIATIVE
        )
        assert abs(total - 1.0) < 1e-9

    def test_threshold_ordering(self):
        assert TII_PROVISIONAL_FLOOR < TII_PASS_THRESHOLD
        assert PSR_INTENSE_PERSONAL_THRESHOLD < PSR_BORDERLINE_THRESHOLD


# ═══════════════════════════════════════════════════════════════════════
# § Component Score Calculations (§4 Stage 4)
# ═══════════════════════════════════════════════════════════════════════


class TestComponentScores:
    def test_frequency_score_high_activity(self):
        calc, _ = _make_calc()
        row = calc.calculate(_active_client())
        # 60/30/3 = 0.6667
        assert 0.65 <= row.interaction_frequency_score <= 0.68

    def test_frequency_score_clamped_at_one(self):
        calc, _ = _make_calc()
        stats = ClientMessageStats(
            client_id="c", message_count=200, days_active_in_last_30=30,
            spt_stage=1, total_client_messages=200,
        )
        row = calc.calculate(stats)
        assert row.interaction_frequency_score <= 1.0

    def test_consistency_score(self):
        calc, _ = _make_calc()
        row = calc.calculate(_active_client())
        # 25/30 = 0.8333
        assert 0.83 <= row.consistency_score <= 0.84

    def test_disclosure_depth_score(self):
        calc, _ = _make_calc()
        row = calc.calculate(_active_client())
        # spt_stage=3 → 3/4 = 0.75
        assert row.disclosure_depth_score == 0.75

    def test_response_latency_score(self):
        calc, _ = _make_calc()
        row = calc.calculate(_active_client())
        # (24 - 2) / 24 ≈ 0.9167
        assert 0.91 <= row.response_latency_score <= 0.92

    def test_latency_score_max_when_instant(self):
        calc, _ = _make_calc()
        stats = ClientMessageStats(
            client_id="c", avg_response_time_hours=0.0, spt_stage=1,
        )
        row = calc.calculate(stats)
        assert row.response_latency_score == 1.0

    def test_latency_score_zero_when_24h(self):
        calc, _ = _make_calc()
        stats = ClientMessageStats(
            client_id="c", avg_response_time_hours=24.0, spt_stage=1,
        )
        row = calc.calculate(stats)
        assert row.response_latency_score == 0.0

    def test_voice_note_ratio(self):
        calc, _ = _make_calc()
        row = calc.calculate(_active_client())
        # 20/50 * 2.0 = 0.8
        assert row.voice_note_ratio_score == 0.8

    def test_voice_ratio_clamped(self):
        calc, _ = _make_calc()
        stats = ClientMessageStats(
            client_id="c", voice_message_count=40,
            total_client_messages=40, spt_stage=1,
        )
        row = calc.calculate(stats)
        # 40/40 * 2.0 = 2.0 → clamped to 1.0
        assert row.voice_note_ratio_score == 1.0

    def test_initiative_frequency(self):
        calc, _ = _make_calc()
        row = calc.calculate(_active_client())
        # 20/25 = 0.8
        assert row.initiative_frequency_score == 0.8

    def test_all_scores_in_range(self):
        calc, _ = _make_calc()
        row = calc.calculate(_active_client())
        for field in [
            row.interaction_frequency_score, row.consistency_score,
            row.disclosure_depth_score, row.response_latency_score,
            row.voice_note_ratio_score, row.initiative_frequency_score,
            row.composite_tii,
        ]:
            assert 0.0 <= field <= 1.0


# ═══════════════════════════════════════════════════════════════════════
# § Composite TII & Weights
# ═══════════════════════════════════════════════════════════════════════


class TestCompositeTII:
    def test_composite_weighted_correctly(self):
        calc, _ = _make_calc()
        row = calc.calculate(_active_client())
        # Manual: 0.1*freq + 0.15*consist + 0.3*disc + 0.1*lat + 0.1*voice + 0.25*init
        expected = (
            0.1 * row.interaction_frequency_score
            + 0.15 * row.consistency_score
            + 0.3 * row.disclosure_depth_score
            + 0.1 * row.response_latency_score
            + 0.1 * row.voice_note_ratio_score
            + 0.25 * row.initiative_frequency_score
        )
        assert abs(row.composite_tii - round(expected, 4)) < 0.001

    def test_composite_clamped_at_one(self):
        calc, _ = _make_calc()
        # Extremely active client with max everything
        stats = ClientMessageStats(
            client_id="c", message_count=200, days_active_in_last_30=30,
            avg_response_time_hours=0.0, voice_message_count=100,
            total_client_messages=100, days_client_initiated=30, spt_stage=4,
        )
        row = calc.calculate(stats)
        assert row.composite_tii <= 1.0


# ═══════════════════════════════════════════════════════════════════════
# § AC2: Zero Division Guard
# ═══════════════════════════════════════════════════════════════════════


class TestAC2_ZeroDivision:
    def test_zero_activity_no_crash(self):
        """AC2: days_active=0 → composite_tii=0.0, no ZeroDivisionError."""
        calc, _ = _make_calc()
        row = calc.calculate(_zero_activity_client())
        assert isinstance(row, TelegramIntimacyIndexRow)

    def test_zero_activity_composite_is_low(self):
        calc, _ = _make_calc()
        row = calc.calculate(_zero_activity_client())
        # All 0 except disclosure (spt=1 → 0.25) and latency (24h → 0.0)
        # composite = 0.3*0.25 = 0.075
        assert row.composite_tii < 0.1

    def test_zero_messages_voice_ratio_zero(self):
        calc, _ = _make_calc()
        row = calc.calculate(_zero_activity_client())
        assert row.voice_note_ratio_score == 0.0

    def test_zero_active_days_initiative_zero(self):
        calc, _ = _make_calc()
        row = calc.calculate(_zero_activity_client())
        assert row.initiative_frequency_score == 0.0

    def test_zero_active_days_consistency_zero(self):
        calc, _ = _make_calc()
        row = calc.calculate(_zero_activity_client())
        assert row.consistency_score == 0.0


# ═══════════════════════════════════════════════════════════════════════
# § PSR Stage Classification (§4 Stage 3)
# ═══════════════════════════════════════════════════════════════════════


class TestPSRClassification:
    def test_entertainment_social(self):
        calc, _ = _make_calc()
        row = calc.calculate(_passive_client())
        assert row.psr_stage == "Entertainment-Social"

    def test_intense_personal(self):
        calc, _ = _make_calc()
        row = calc.calculate(_active_client())
        # Active client has high TII → likely Intense-Personal
        assert row.composite_tii >= 0.4
        assert row.psr_stage in ("Intense-Personal", "Borderline")

    def test_borderline_at_0_8(self):
        """AC3: composite_tii=0.82 → psr_stage='Borderline'."""
        calc, _ = _make_calc()
        # Need to engineer stats that produce composite >= 0.8
        stats = ClientMessageStats(
            client_id="c-borderline",
            message_count=90, days_active_in_last_30=30,
            avg_response_time_hours=0.5, voice_message_count=40,
            total_client_messages=50, days_client_initiated=30, spt_stage=4,
        )
        row = calc.calculate(stats)
        assert row.composite_tii >= 0.8
        assert row.psr_stage == "Borderline"

    def test_exact_0_4_is_intense_personal(self):
        calc, _ = _make_calc()
        result = calc.evaluate_gate("c", composite_tii=0.4, consistency_score=0.5)
        assert result.verdict == "PASS"


# ═══════════════════════════════════════════════════════════════════════
# § AC1: Hard TII Gate
# ═══════════════════════════════════════════════════════════════════════


class TestAC1_HardGate:
    def test_tii_0_29_is_fail(self):
        """AC1: composite_tii=0.29 → FAIL, NOT rounded up to PROVISIONAL."""
        calc, _ = _make_calc()
        result = calc.evaluate_gate("c1", composite_tii=0.29, consistency_score=0.9)
        assert result.verdict == "FAIL"

    def test_tii_0_30_high_consistency_is_provisional(self):
        calc, _ = _make_calc()
        result = calc.evaluate_gate("c1", composite_tii=0.30, consistency_score=0.85)
        assert result.verdict == "PROVISIONAL"

    def test_tii_0_35_low_consistency_is_fail(self):
        """Between 0.3-0.4 but consistency <= 0.8 → FAIL."""
        calc, _ = _make_calc()
        result = calc.evaluate_gate("c1", composite_tii=0.35, consistency_score=0.5)
        assert result.verdict == "FAIL"

    def test_tii_0_4_is_pass(self):
        calc, _ = _make_calc()
        result = calc.evaluate_gate("c1", composite_tii=0.4, consistency_score=0.5)
        assert result.verdict == "PASS"

    def test_tii_0_7_is_pass(self):
        calc, _ = _make_calc()
        result = calc.evaluate_gate("c1", composite_tii=0.7, consistency_score=0.3)
        assert result.verdict == "PASS"

    def test_provisional_has_operator_alert(self):
        calc, _ = _make_calc()
        result = calc.evaluate_gate("c1", composite_tii=0.35, consistency_score=0.9)
        assert result.verdict == "PROVISIONAL"
        assert result.operator_alert is not None
        assert "Deep Disclosure" in result.operator_alert

    def test_fail_no_operator_alert(self):
        calc, _ = _make_calc()
        result = calc.evaluate_gate("c1", composite_tii=0.1, consistency_score=0.1)
        assert result.verdict == "FAIL"
        assert result.operator_alert is None


# ═══════════════════════════════════════════════════════════════════════
# § AC3: Enum Resolution
# ═══════════════════════════════════════════════════════════════════════


class TestAC3_EnumResolution:
    def test_0_82_maps_to_borderline(self):
        """AC3: composite_tii=0.82 → psr_stage='Borderline'."""
        calc, _ = _make_calc()
        # Use the internal classifier directly
        psr = calc._classify_psr(0.82)
        assert psr == "Borderline"

    def test_0_39_maps_to_entertainment_social(self):
        calc, _ = _make_calc()
        psr = calc._classify_psr(0.39)
        assert psr == "Entertainment-Social"

    def test_0_4_maps_to_intense_personal(self):
        calc, _ = _make_calc()
        psr = calc._classify_psr(0.4)
        assert psr == "Intense-Personal"

    def test_0_79_maps_to_intense_personal(self):
        calc, _ = _make_calc()
        psr = calc._classify_psr(0.79)
        assert psr == "Intense-Personal"

    def test_0_8_maps_to_borderline(self):
        calc, _ = _make_calc()
        psr = calc._classify_psr(0.8)
        assert psr == "Borderline"

    def test_0_0_maps_to_entertainment_social(self):
        calc, _ = _make_calc()
        psr = calc._classify_psr(0.0)
        assert psr == "Entertainment-Social"


# ═══════════════════════════════════════════════════════════════════════
# § Batch
# ═══════════════════════════════════════════════════════════════════════


class TestBatch:
    def test_batch_returns_all(self):
        calc, _ = _make_calc()
        rows = calc.calculate_batch([_active_client(), _passive_client(), _zero_activity_client()])
        assert len(rows) == 3

    def test_batch_client_ids(self):
        calc, _ = _make_calc()
        rows = calc.calculate_batch([_active_client(), _passive_client()])
        ids = {r.client_id for r in rows}
        assert ids == {"client-active", "client-passive"}


# ═══════════════════════════════════════════════════════════════════════
# § ADR-01
# ═══════════════════════════════════════════════════════════════════════


class TestADR01:
    def test_valid_3char_coach(self):
        calc, _ = _make_calc(coach="TST")
        row = calc.calculate(_active_client())
        assert row.coach_id == "coach-tii-uuid"

    def test_1char_rejected(self):
        tmp = tempfile.mkdtemp()
        rc = ReceiptChain(coach_acronym="TST", log_dir=tmp)
        with pytest.raises(ValueError, match="INVALID_COACH_ACRONYM"):
            TIICalculator(coach_acronym="X", coach_id="t", receipt_chain=rc)

    def test_5char_rejected(self):
        tmp = tempfile.mkdtemp()
        rc = ReceiptChain(coach_acronym="TST", log_dir=tmp)
        with pytest.raises(ValueError, match="INVALID_COACH_ACRONYM"):
            TIICalculator(coach_acronym="ABCDE", coach_id="t", receipt_chain=rc)


# ═══════════════════════════════════════════════════════════════════════
# § Receipt Chain
# ═══════════════════════════════════════════════════════════════════════


class TestReceiptChain:
    def test_calculate_emits_receipt(self):
        calc, rc = _make_calc()
        calc.calculate(_active_client())
        entries = rc.query(action="tii-calculate")
        assert len(entries) >= 1

    def test_receipt_has_client_id(self):
        calc, rc = _make_calc()
        calc.calculate(_active_client())
        entries = rc.query(action="tii-calculate")
        assert entries[0].person_id == "client-active"

    def test_receipt_metadata_has_composite(self):
        calc, rc = _make_calc()
        calc.calculate(_active_client())
        entries = rc.query(action="tii-calculate")
        assert "composite_tii" in entries[0].metadata
        assert entries[0].metadata["composite_tii"] > 0

    def test_batch_emits_per_client(self):
        calc, rc = _make_calc()
        calc.calculate_batch([_active_client(), _passive_client()])
        entries = rc.query(action="tii-calculate")
        assert len(entries) == 2


# ═══════════════════════════════════════════════════════════════════════
# § Backward Compatibility (§6)
# ═══════════════════════════════════════════════════════════════════════


class TestBackwardCompatibility:
    def test_zero_interactions_resolves_to_fail(self):
        """§6: 0 interactions → composite=0.0 → gate FAIL."""
        calc, _ = _make_calc()
        row = calc.calculate(_zero_activity_client())
        result = calc.evaluate_gate(row.client_id, row.composite_tii, row.consistency_score)
        assert result.verdict == "FAIL"


# ═══════════════════════════════════════════════════════════════════════
# § Model Validation
# ═══════════════════════════════════════════════════════════════════════


class TestModelValidation:
    def test_tii_score_clamped(self):
        with pytest.raises(Exception):
            TelegramIntimacyIndexRow(
                tii_id="x", client_id="c", coach_id="x",
                interaction_frequency_score=1.5, consistency_score=0,
                disclosure_depth_score=0, response_latency_score=0,
                voice_note_ratio_score=0, initiative_frequency_score=0,
                composite_tii=0, psr_stage="X", last_computed="T",
            )

    def test_message_stats_negative_rejected(self):
        with pytest.raises(Exception):
            ClientMessageStats(client_id="c", message_count=-1)
