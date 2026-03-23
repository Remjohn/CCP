"""
FR55 — Session Booking Intelligence  (CPSC Spec 1 of 10)
=========================================================
Tests for ConvergenceDetector and BookingReadinessEvaluator.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path
import shutil
import tempfile

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cpsc_models import (
    BOOKING_CONFIDENCE_FAIL,
    BOOKING_CONFIDENCE_HIGH,
    BOOKING_CONFIDENCE_WATCH,
    BOOKING_COPING_HIGH,
    BOOKING_COPING_WATCH,
    BOOKING_SPT_HIGH,
    BOOKING_SPT_WATCH,
    BOOKING_TII_HIGH,
    BOOKING_TII_WATCH,
    BookingGateVerdict,
    OperatorBookingBriefRow,
    QualifyingMetrics,
    RecommendationStatus,
    SessionBookingError,
)
from src.ccp.services.session_booking_intelligence import (
    BookingReadinessEvaluator,
    ConvergenceDetector,
)


# ══════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════

CID = "TST"


def _make_rc() -> ReceiptChain:
    return ReceiptChain(coach_acronym=CID)


def _make_rc_isolated() -> tuple[ReceiptChain, str]:
    """Create a receipt chain with an isolated temp log dir."""
    tmp = tempfile.mkdtemp(prefix="fr55_rc_")
    rc = ReceiptChain(coach_acronym=CID, log_dir=tmp)
    return rc, tmp


# ══════════════════════════════════════════════════════════════════════
# 1. Constants
# ══════════════════════════════════════════════════════════════════════


class TestConstants:
    """Verify threshold constants match spec §4."""

    def test_coping_high(self) -> None:
        assert BOOKING_COPING_HIGH == 4

    def test_spt_high(self) -> None:
        assert BOOKING_SPT_HIGH == 3

    def test_tii_high(self) -> None:
        assert BOOKING_TII_HIGH == pytest.approx(0.4)

    def test_coping_watch(self) -> None:
        assert BOOKING_COPING_WATCH == 3

    def test_spt_watch(self) -> None:
        assert BOOKING_SPT_WATCH == 3

    def test_tii_watch(self) -> None:
        assert BOOKING_TII_WATCH == pytest.approx(0.3)

    def test_confidence_high(self) -> None:
        assert BOOKING_CONFIDENCE_HIGH == pytest.approx(1.0)

    def test_confidence_watch(self) -> None:
        assert BOOKING_CONFIDENCE_WATCH == pytest.approx(0.6)

    def test_confidence_fail(self) -> None:
        assert BOOKING_CONFIDENCE_FAIL == pytest.approx(0.0)


# ══════════════════════════════════════════════════════════════════════
# 2. ADR-01 Constructor Validation
# ══════════════════════════════════════════════════════════════════════


class TestADR01Constructor:
    """ADR-01: coach_id must be 2-4 chars."""

    def test_2_char_ok(self) -> None:
        ConvergenceDetector(coach_id="AB")
        BookingReadinessEvaluator(coach_id="AB")

    def test_3_char_ok(self) -> None:
        ConvergenceDetector(coach_id="ABC")
        BookingReadinessEvaluator(coach_id="ABC")

    def test_4_char_ok(self) -> None:
        ConvergenceDetector(coach_id="ABCD")
        BookingReadinessEvaluator(coach_id="ABCD")

    def test_1_char_rejected(self) -> None:
        with pytest.raises(ValueError, match="ADR-01"):
            ConvergenceDetector(coach_id="A")
        with pytest.raises(ValueError, match="ADR-01"):
            BookingReadinessEvaluator(coach_id="A")

    def test_5_char_rejected(self) -> None:
        with pytest.raises(ValueError, match="ADR-01"):
            ConvergenceDetector(coach_id="ABCDE")
        with pytest.raises(ValueError, match="ADR-01"):
            BookingReadinessEvaluator(coach_id="ABCDE")


# ══════════════════════════════════════════════════════════════════════
# 3. ConvergenceDetector
# ══════════════════════════════════════════════════════════════════════


class TestConvergenceDetector:
    """Stage 1 — 4-signal convergence matrix."""

    def setup_method(self) -> None:
        self.cd = ConvergenceDetector(coach_id=CID)

    # ── HIGH_CONFIDENCE_READY ──────────────────────────────────────

    def test_high_confidence_all_met(self) -> None:
        status, conf = self.cd.evaluate_convergence(4, 3, "CONFIRMED", 0.4)
        assert status == RecommendationStatus.HIGH_CONFIDENCE_READY
        assert conf == pytest.approx(BOOKING_CONFIDENCE_HIGH)

    def test_high_confidence_above_thresholds(self) -> None:
        status, conf = self.cd.evaluate_convergence(5, 5, "CONFIRMED", 0.9)
        assert status == RecommendationStatus.HIGH_CONFIDENCE_READY
        assert conf == pytest.approx(1.0)

    # ── WATCHLIST_BUILDING ─────────────────────────────────────────

    def test_watchlist_search_not_confirmed(self) -> None:
        """Coping/spt/tii pass HIGH thresholds, but search != CONFIRMED → watchlist."""
        status, conf = self.cd.evaluate_convergence(4, 4, "PENDING", 0.9)
        assert status == RecommendationStatus.WATCHLIST_BUILDING
        assert conf == pytest.approx(BOOKING_CONFIDENCE_WATCH)

    def test_watchlist_exact_thresholds(self) -> None:
        status, conf = self.cd.evaluate_convergence(3, 3, "UNKNOWN", 0.3)
        assert status == RecommendationStatus.WATCHLIST_BUILDING
        assert conf == pytest.approx(0.6)

    def test_watchlist_search_none(self) -> None:
        """None search → UNKNOWN → watchlist if other signals pass."""
        status, _ = self.cd.evaluate_convergence(3, 3, None, 0.3)
        assert status == RecommendationStatus.WATCHLIST_BUILDING

    # ── NOT_READY ──────────────────────────────────────────────────

    def test_not_ready_coping_low(self) -> None:
        status, conf = self.cd.evaluate_convergence(2, 3, "CONFIRMED", 0.5)
        assert status == RecommendationStatus.NOT_READY
        assert conf == pytest.approx(BOOKING_CONFIDENCE_FAIL)

    def test_not_ready_spt_low(self) -> None:
        status, _ = self.cd.evaluate_convergence(5, 2, "CONFIRMED", 0.9)
        assert status == RecommendationStatus.NOT_READY

    def test_not_ready_tii_low(self) -> None:
        status, _ = self.cd.evaluate_convergence(3, 3, "UNKNOWN", 0.29)
        assert status == RecommendationStatus.NOT_READY

    def test_not_ready_all_low(self) -> None:
        status, conf = self.cd.evaluate_convergence(1, 1, "UNKNOWN", 0.0)
        assert status == RecommendationStatus.NOT_READY
        assert conf == pytest.approx(0.0)

    # ── None handling (§6 backward compat) ─────────────────────────

    def test_all_none_resolves_not_ready(self) -> None:
        """All None inputs → safe defaults → NOT_READY."""
        status, conf = self.cd.evaluate_convergence(None, None, None, None)
        assert status == RecommendationStatus.NOT_READY
        assert conf == pytest.approx(0.0)

    def test_coping_none_other_high(self) -> None:
        """None coping → 0 → NOT_READY even if others pass."""
        status, _ = self.cd.evaluate_convergence(None, 5, "CONFIRMED", 0.9)
        assert status == RecommendationStatus.NOT_READY

    def test_spt_none_other_high(self) -> None:
        status, _ = self.cd.evaluate_convergence(5, None, "CONFIRMED", 0.9)
        assert status == RecommendationStatus.NOT_READY

    def test_tii_none_other_high(self) -> None:
        status, _ = self.cd.evaluate_convergence(5, 5, "CONFIRMED", None)
        assert status == RecommendationStatus.NOT_READY

    # ── Boundary tests ─────────────────────────────────────────────

    def test_coping_3_spt_3_tii_029_not_ready(self) -> None:
        """tii just below 0.3 → NOT_READY."""
        status, _ = self.cd.evaluate_convergence(3, 3, "UNKNOWN", 0.29)
        assert status == RecommendationStatus.NOT_READY

    def test_coping_4_spt_3_tii_039_confirmed_watchlist(self) -> None:
        """tii just below HIGH threshold but above WATCH → WATCHLIST."""
        status, _ = self.cd.evaluate_convergence(4, 3, "CONFIRMED", 0.39)
        assert status == RecommendationStatus.WATCHLIST_BUILDING

    def test_coping_4_spt_3_tii_04_confirmed_high(self) -> None:
        """tii at exact HIGH threshold with all signals → HIGH."""
        status, _ = self.cd.evaluate_convergence(4, 3, "CONFIRMED", 0.40)
        assert status == RecommendationStatus.HIGH_CONFIDENCE_READY


# ══════════════════════════════════════════════════════════════════════
# 4. BookingReadinessEvaluator — Gate Verdicts
# ══════════════════════════════════════════════════════════════════════


class TestBookingReadinessEvaluator:
    """Stage 2 — gate verdict + brief row generation."""

    def setup_method(self) -> None:
        self.rc = _make_rc()
        self.ev = BookingReadinessEvaluator(coach_id=CID, receipt_chain=self.rc)

    # ── PASS ───────────────────────────────────────────────────────

    def test_pass_verdict(self) -> None:
        row = self.ev.evaluate("c1", 5, 4, "CONFIRMED", 0.8)
        assert row.gate_verdict == BookingGateVerdict.PASS.value
        assert row.recommendation_status == RecommendationStatus.HIGH_CONFIDENCE_READY.value
        assert row.confidence_score_calc == pytest.approx(1.0)

    # ── PROVISIONAL_WATCHLIST ──────────────────────────────────────

    def test_provisional_watchlist_verdict(self) -> None:
        row = self.ev.evaluate("c2", 4, 4, "PENDING", 0.9)
        assert row.gate_verdict == BookingGateVerdict.PROVISIONAL_WATCHLIST.value
        assert row.recommendation_status == RecommendationStatus.WATCHLIST_BUILDING.value
        assert row.confidence_score_calc == pytest.approx(0.6)

    # ── FAIL_NURTURE_MODE ──────────────────────────────────────────

    def test_fail_nurture_mode_verdict(self) -> None:
        row = self.ev.evaluate("c3", 1, 1, "UNKNOWN", 0.0)
        assert row.gate_verdict == BookingGateVerdict.FAIL_NURTURE_MODE.value
        assert row.recommendation_status == RecommendationStatus.NOT_READY.value
        assert row.confidence_score_calc == pytest.approx(0.0)

    # ── Row fields ─────────────────────────────────────────────────

    def test_row_has_client_id(self) -> None:
        row = self.ev.evaluate("client_x", 5, 3, "CONFIRMED", 0.5)
        assert row.client_id == "client_x"

    def test_row_has_coach_id(self) -> None:
        row = self.ev.evaluate("c1", 5, 3, "CONFIRMED", 0.5)
        assert row.coach_id == CID

    def test_row_has_briefing_id_uuid(self) -> None:
        row = self.ev.evaluate("c1", 5, 3, "CONFIRMED", 0.5)
        parsed = uuid.UUID(row.briefing_id, version=4)
        assert str(parsed) == row.briefing_id

    def test_row_has_evaluated_at_iso(self) -> None:
        row = self.ev.evaluate("c1", 5, 3, "CONFIRMED", 0.5)
        dt = datetime.fromisoformat(row.evaluated_at)
        assert dt.tzinfo is not None  # timezone-aware

    def test_no_receipt_chain_ok(self) -> None:
        """Service must work without receipt chain."""
        ev = BookingReadinessEvaluator(coach_id=CID)
        row = ev.evaluate("c1", 5, 3, "CONFIRMED", 0.5)
        assert row.gate_verdict == BookingGateVerdict.PASS.value


# ══════════════════════════════════════════════════════════════════════
# 5. Acceptance Criteria
# ══════════════════════════════════════════════════════════════════════


class TestAcceptanceCriteria:
    """Verbatim AC scenarios from tech spec §7."""

    def setup_method(self) -> None:
        self.rc = _make_rc()
        self.ev = BookingReadinessEvaluator(coach_id=CID, receipt_chain=self.rc)

    # AC1 — coping=4, spt=4, tii=0.9, search="PENDING" → PROVISIONAL_WATCHLIST
    def test_ac1_search_pending_blocks_high(self) -> None:
        row = self.ev.evaluate("ac1_client", 4, 4, "PENDING", 0.9)
        assert row.recommendation_status == RecommendationStatus.WATCHLIST_BUILDING.value
        assert row.gate_verdict == BookingGateVerdict.PROVISIONAL_WATCHLIST.value
        assert row.confidence_score_calc == pytest.approx(0.6)

    # AC2 — WATCHLIST row inserted, zero push notifications
    def test_ac2_watchlist_no_push_field(self) -> None:
        """WATCHLIST brief has no push_notification field (silent monitoring)."""
        row = self.ev.evaluate("ac2_client", 3, 3, "UNKNOWN", 0.35)
        assert row.gate_verdict == BookingGateVerdict.PROVISIONAL_WATCHLIST.value
        row_dict = row.model_dump()
        assert "push_notification" not in row_dict
        assert "notification" not in row_dict

    # AC3 — PASS → all 4 qualifying_metrics populated
    def test_ac3_pass_all_metrics_populated(self) -> None:
        row = self.ev.evaluate("ac3_client", 5, 4, "CONFIRMED", 0.8)
        assert row.gate_verdict == BookingGateVerdict.PASS.value
        qm = row.qualifying_metrics
        assert qm.tii_snapshot == pytest.approx(0.8)
        assert qm.spt_snapshot == 4
        assert qm.search_confirmed is True
        assert qm.coping_tier == 5

    def test_ac3_pass_metrics_are_not_none(self) -> None:
        """All qualifying_metrics fields are non-null."""
        row = self.ev.evaluate("ac3b", 4, 3, "CONFIRMED", 0.45)
        qm = row.qualifying_metrics
        assert qm.tii_snapshot is not None
        assert qm.spt_snapshot is not None
        assert qm.search_confirmed is not None
        assert qm.coping_tier is not None


# ══════════════════════════════════════════════════════════════════════
# 6. QualifyingMetrics — None Input Handling
# ══════════════════════════════════════════════════════════════════════


class TestQualifyingMetricsNoneHandling:
    """§6 — None inputs resolve to safe defaults in metrics snapshot."""

    def setup_method(self) -> None:
        self.ev = BookingReadinessEvaluator(coach_id=CID)

    def test_all_none_metrics_populated(self) -> None:
        row = self.ev.evaluate("n1", None, None, None, None)
        qm = row.qualifying_metrics
        assert qm.tii_snapshot == pytest.approx(0.0)
        assert qm.spt_snapshot == 0
        assert qm.search_confirmed is False
        assert qm.coping_tier == 0

    def test_partial_none_coping(self) -> None:
        row = self.ev.evaluate("n2", None, 3, "CONFIRMED", 0.5)
        assert row.qualifying_metrics.coping_tier == 0

    def test_partial_none_search(self) -> None:
        row = self.ev.evaluate("n3", 4, 3, None, 0.5)
        assert row.qualifying_metrics.search_confirmed is False

    def test_partial_none_tii(self) -> None:
        row = self.ev.evaluate("n4", 4, 3, "CONFIRMED", None)
        assert row.qualifying_metrics.tii_snapshot == pytest.approx(0.0)

    def test_partial_none_spt(self) -> None:
        row = self.ev.evaluate("n5", 4, None, "CONFIRMED", 0.5)
        assert row.qualifying_metrics.spt_snapshot == 0


# ══════════════════════════════════════════════════════════════════════
# 7. Output Schema (DEP-ENG-076)
# ══════════════════════════════════════════════════════════════════════


class TestOutputSchema:
    """Verify OperatorBookingBriefRow output matches spec §5."""

    def setup_method(self) -> None:
        self.ev = BookingReadinessEvaluator(coach_id=CID)

    def test_model_dump_keys(self) -> None:
        row = self.ev.evaluate("s1", 5, 4, "CONFIRMED", 0.8)
        d = row.model_dump()
        expected_keys = {
            "briefing_id", "client_id", "coach_id",
            "recommendation_status", "confidence_score_calc",
            "gate_verdict", "qualifying_metrics", "evaluated_at",
        }
        assert set(d.keys()) == expected_keys

    def test_qualifying_metrics_keys(self) -> None:
        row = self.ev.evaluate("s2", 5, 4, "CONFIRMED", 0.8)
        qm_dict = row.qualifying_metrics.model_dump()
        expected = {"tii_snapshot", "spt_snapshot", "search_confirmed", "coping_tier"}
        assert set(qm_dict.keys()) == expected

    def test_confidence_bounded_0_1(self) -> None:
        for coping, spt, search, tii in [
            (5, 5, "CONFIRMED", 0.9),
            (3, 3, "UNKNOWN", 0.3),
            (1, 1, "UNKNOWN", 0.0),
        ]:
            row = self.ev.evaluate("b1", coping, spt, search, tii)
            assert 0.0 <= row.confidence_score_calc <= 1.0

    def test_recommendation_status_values(self) -> None:
        """All statuses are valid enum values."""
        for coping, spt, search, tii, expected in [
            (5, 4, "CONFIRMED", 0.8, "HIGH_CONFIDENCE_READY"),
            (3, 3, "UNKNOWN", 0.3, "WATCHLIST_BUILDING"),
            (1, 1, "UNKNOWN", 0.0, "NOT_READY"),
        ]:
            row = self.ev.evaluate("v1", coping, spt, search, tii)
            assert row.recommendation_status == expected

    def test_gate_verdict_values(self) -> None:
        """All gate verdicts are valid enum values."""
        for coping, spt, search, tii, expected in [
            (5, 4, "CONFIRMED", 0.8, "PASS"),
            (3, 3, "UNKNOWN", 0.3, "PROVISIONAL_WATCHLIST"),
            (1, 1, "UNKNOWN", 0.0, "FAIL_NURTURE_MODE"),
        ]:
            row = self.ev.evaluate("g1", coping, spt, search, tii)
            assert row.gate_verdict == expected


# ══════════════════════════════════════════════════════════════════════
# 8. Receipt Chain
# ══════════════════════════════════════════════════════════════════════


class TestReceiptChain:
    """Verify receipt logging on evaluate."""

    def test_two_receipts_logged(self) -> None:
        rc, tmp = _make_rc_isolated()
        ev = BookingReadinessEvaluator(coach_id=CID, receipt_chain=rc)
        ev.evaluate("r1", 5, 3, "CONFIRMED", 0.5)
        conv = rc.query(action="convergence-detect")
        gate = rc.query(action="booking-readiness-gate")
        assert len(conv) >= 1
        assert len(gate) >= 1
        shutil.rmtree(tmp, ignore_errors=True)

    def test_convergence_receipt(self) -> None:
        rc, tmp = _make_rc_isolated()
        ev = BookingReadinessEvaluator(coach_id=CID, receipt_chain=rc)
        ev.evaluate("r2", 5, 3, "CONFIRMED", 0.5)
        conv = rc.query(action="convergence-detect")
        assert len(conv) >= 1
        assert "r2" in conv[0].output_summary
        shutil.rmtree(tmp, ignore_errors=True)

    def test_gate_receipt(self) -> None:
        rc, tmp = _make_rc_isolated()
        ev = BookingReadinessEvaluator(coach_id=CID, receipt_chain=rc)
        ev.evaluate("r3", 5, 3, "CONFIRMED", 0.5)
        gate = rc.query(action="booking-readiness-gate")
        assert len(gate) >= 1
        assert "PASS" in gate[0].output_summary
        shutil.rmtree(tmp, ignore_errors=True)

    def test_no_receipt_chain_no_error(self) -> None:
        """None receipt chain does not crash."""
        ev = BookingReadinessEvaluator(coach_id=CID, receipt_chain=None)
        row = ev.evaluate("r4", 1, 1, "UNKNOWN", 0.0)
        assert row.gate_verdict == BookingGateVerdict.FAIL_NURTURE_MODE.value


# ══════════════════════════════════════════════════════════════════════
# 9. Persona Masking (C-11)
# ══════════════════════════════════════════════════════════════════════


class TestPersonaMasking:
    """C-11: No agent class names in output JSON."""

    def test_no_class_names_in_output(self) -> None:
        ev = BookingReadinessEvaluator(coach_id=CID)
        row = ev.evaluate("pm1", 5, 3, "CONFIRMED", 0.5)
        json_str = row.model_dump_json()
        for forbidden in [
            "ConvergenceDetector",
            "BookingReadinessEvaluator",
            "SessionBookingError",
        ]:
            assert forbidden not in json_str, f"C-11 violation: {forbidden} in output"


# ══════════════════════════════════════════════════════════════════════
# 10. Enum Coverage
# ══════════════════════════════════════════════════════════════════════


class TestEnumCoverage:
    """Verify enum members match spec."""

    def test_recommendation_status_members(self) -> None:
        names = {m.name for m in RecommendationStatus}
        assert names == {"HIGH_CONFIDENCE_READY", "WATCHLIST_BUILDING", "NOT_READY"}

    def test_booking_gate_verdict_members(self) -> None:
        names = {m.name for m in BookingGateVerdict}
        assert names == {"PASS", "PROVISIONAL_WATCHLIST", "FAIL_NURTURE_MODE"}

    def test_session_booking_error_members(self) -> None:
        names = {m.name for m in SessionBookingError}
        assert names == {
            "INVALID_COACH_SCOPE",
            "CONVERGENCE_ERROR",
            "GATE_EVALUATION_ERROR",
            "MISSING_METRICS",
        }
