"""
FR-CBCS-06 — SEARCH Phase Detection Engine — Integration Tests
================================================================
Covers: 4-signal convergence, reconsolidation window validation,
state machine lifecycle, and acceptance criteria AC1-AC3.
"""

from __future__ import annotations

import tempfile

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cbcs_models import (
    SEARCH_AGENCY_WORDS_THRESHOLD,
    SEARCH_FUTURE_FOCUS_THRESHOLD,
    SEARCH_HEDGING_WORDS_MAX,
    SEARCH_INFO_SEEKING_THRESHOLD,
    SEARCH_MAX_HOURS,
    SEARCH_MIN_HOURS,
    SEARCH_MIN_WORD_COUNT,
    SearchLiwcSignals,
    SearchPhaseDetectionRow,
    SearchPhaseError,
    SearchPhaseStatus,
)
from src.ccp.services.search_phase_detector import (
    ReconsolidationWindowValidator,
    SearchPhaseDetector,
)


# ── Helpers ─────────────────────────────────────────────────────────────

def _make_detector(coach: str = "TST") -> tuple[SearchPhaseDetector, ReceiptChain]:
    tmp = tempfile.mkdtemp()
    rc = ReceiptChain(coach_acronym=coach, log_dir=tmp)
    det = SearchPhaseDetector(coach_acronym=coach, receipt_chain=rc)
    return det, rc


def _make_validator(coach: str = "TST") -> tuple[ReconsolidationWindowValidator, ReceiptChain]:
    tmp = tempfile.mkdtemp()
    rc = ReceiptChain(coach_acronym=coach, log_dir=tmp)
    val = ReconsolidationWindowValidator(coach_acronym=coach, receipt_chain=rc)
    return val, rc


def _converging_signals() -> SearchLiwcSignals:
    """All 4 signals meeting thresholds."""
    return SearchLiwcSignals(
        info_seeking=SEARCH_INFO_SEEKING_THRESHOLD + 0.01,
        future_focus=SEARCH_FUTURE_FOCUS_THRESHOLD + 0.01,
        agency_words=SEARCH_AGENCY_WORDS_THRESHOLD + 0.01,
        hedging_words=SEARCH_HEDGING_WORDS_MAX - 0.005,
    )


def _make_detecting_row() -> SearchPhaseDetectionRow:
    """Pre-built DETECTING row for validator tests."""
    det, _ = _make_detector()
    row = det.check_convergence("c1", "coach1", _converging_signals(), 20)
    assert row is not None
    return row


# ═══════════════════════════════════════════════════════════════════════
# SECTION 1 — Convergence Detection
# ═══════════════════════════════════════════════════════════════════════

class TestConvergenceDetection:
    """§4 Stage 1 — 4-signal convergence."""

    def test_all_4_signals_met_returns_detecting(self) -> None:
        det, _ = _make_detector()
        row = det.check_convergence("c1", "coach1", _converging_signals(), 20)
        assert row is not None
        assert row.status == "DETECTING"

    def test_below_word_count_returns_none(self) -> None:
        det, _ = _make_detector()
        row = det.check_convergence("c1", "coach1", _converging_signals(), SEARCH_MIN_WORD_COUNT - 1)
        assert row is None

    def test_exactly_min_word_count_works(self) -> None:
        det, _ = _make_detector()
        row = det.check_convergence("c1", "coach1", _converging_signals(), SEARCH_MIN_WORD_COUNT)
        assert row is not None

    def test_info_seeking_below_threshold_fails(self) -> None:
        det, _ = _make_detector()
        signals = SearchLiwcSignals(
            info_seeking=SEARCH_INFO_SEEKING_THRESHOLD - 0.01,
            future_focus=0.08,
            agency_words=0.08,
            hedging_words=0.01,
        )
        row = det.check_convergence("c1", "coach1", signals, 20)
        assert row is None

    def test_future_focus_below_threshold_fails(self) -> None:
        det, _ = _make_detector()
        signals = SearchLiwcSignals(
            info_seeking=0.1,
            future_focus=SEARCH_FUTURE_FOCUS_THRESHOLD - 0.01,
            agency_words=0.08,
            hedging_words=0.01,
        )
        row = det.check_convergence("c1", "coach1", signals, 20)
        assert row is None

    def test_agency_below_threshold_fails(self) -> None:
        det, _ = _make_detector()
        signals = SearchLiwcSignals(
            info_seeking=0.1,
            future_focus=0.08,
            agency_words=SEARCH_AGENCY_WORDS_THRESHOLD - 0.01,
            hedging_words=0.01,
        )
        row = det.check_convergence("c1", "coach1", signals, 20)
        assert row is None

    def test_hedging_above_threshold_fails(self) -> None:
        det, _ = _make_detector()
        signals = SearchLiwcSignals(
            info_seeking=0.1,
            future_focus=0.08,
            agency_words=0.08,
            hedging_words=SEARCH_HEDGING_WORDS_MAX + 0.01,
        )
        row = det.check_convergence("c1", "coach1", signals, 20)
        assert row is None

    def test_hedging_exactly_at_threshold_fails(self) -> None:
        """Strict inequality: hedging < 0.02. Equal → fail."""
        det, _ = _make_detector()
        signals = SearchLiwcSignals(
            info_seeking=0.1,
            future_focus=0.08,
            agency_words=0.08,
            hedging_words=SEARCH_HEDGING_WORDS_MAX,
        )
        row = det.check_convergence("c1", "coach1", signals, 20)
        assert row is None


# ═══════════════════════════════════════════════════════════════════════
# SECTION 2 — Cluster Confidence
# ═══════════════════════════════════════════════════════════════════════

class TestClusterConfidence:
    """cluster_confidence_score calculation."""

    def test_confidence_between_0_and_1(self) -> None:
        det, _ = _make_detector()
        row = det.check_convergence("c1", "coach1", _converging_signals(), 20)
        assert row is not None
        assert 0.0 <= row.cluster_confidence_score <= 1.0

    def test_strong_signals_high_confidence(self) -> None:
        det, _ = _make_detector()
        strong = SearchLiwcSignals(
            info_seeking=0.16,  # 2x threshold
            future_focus=0.10,  # 2x threshold
            agency_words=0.10,  # 2x threshold
            hedging_words=0.0,  # perfectly low
        )
        row = det.check_convergence("c1", "coach1", strong, 20)
        assert row is not None
        assert row.cluster_confidence_score >= 0.9

    def test_barely_met_signals_moderate_confidence(self) -> None:
        det, _ = _make_detector()
        barely = SearchLiwcSignals(
            info_seeking=SEARCH_INFO_SEEKING_THRESHOLD + 0.001,
            future_focus=SEARCH_FUTURE_FOCUS_THRESHOLD + 0.001,
            agency_words=SEARCH_AGENCY_WORDS_THRESHOLD + 0.001,
            hedging_words=SEARCH_HEDGING_WORDS_MAX - 0.001,
        )
        row = det.check_convergence("c1", "coach1", barely, 20)
        assert row is not None
        assert row.cluster_confidence_score < 0.9


# ═══════════════════════════════════════════════════════════════════════
# SECTION 3 — Reconsolidation Window Validation
# ═══════════════════════════════════════════════════════════════════════

class TestWindowValidation:
    """§4 Stage 2 — 4h-24h reconsolidation window."""

    def test_confirmed_within_window(self) -> None:
        """Follow-up at 6 hours (4h-24h) → CONFIRMED."""
        val, _ = _make_validator()
        row = _make_detecting_row()
        result = val.validate(row, _converging_signals(), 20, 6.0)
        assert result.status == "CONFIRMED"
        assert result.triggered_priming_at is not None

    def test_confirmed_at_exactly_4h(self) -> None:
        """Follow-up at exactly 4.0 hours → CONFIRMED (4h <= t <= 24h)."""
        val, _ = _make_validator()
        row = _make_detecting_row()
        result = val.validate(row, _converging_signals(), 20, 4.0)
        assert result.status == "CONFIRMED"

    def test_confirmed_at_exactly_24h(self) -> None:
        """Follow-up at exactly 24.0 hours → CONFIRMED (boundary)."""
        val, _ = _make_validator()
        row = _make_detecting_row()
        result = val.validate(row, _converging_signals(), 20, 24.0)
        assert result.status == "CONFIRMED"

    def test_provisional_under_4h(self) -> None:
        """Follow-up at 2 hours (< 4h) → PROVISIONAL_WAIT."""
        val, _ = _make_validator()
        row = _make_detecting_row()
        result = val.validate(row, _converging_signals(), 20, 2.0)
        assert result.status == "PROVISIONAL_WAIT"

    def test_expired_over_24h(self) -> None:
        """Follow-up at 25 hours (> 24h) → EXPIRED."""
        val, _ = _make_validator()
        row = _make_detecting_row()
        result = val.validate(row, _converging_signals(), 20, 25.0)
        assert result.status == "EXPIRED"

    def test_expired_if_followup_not_converging(self) -> None:
        """Follow-up with bad signals → EXPIRED even within window."""
        val, _ = _make_validator()
        row = _make_detecting_row()
        bad_signals = SearchLiwcSignals(
            info_seeking=0.01, future_focus=0.01,
            agency_words=0.01, hedging_words=0.05,
        )
        result = val.validate(row, bad_signals, 20, 6.0)
        assert result.status == "EXPIRED"

    def test_expired_if_followup_low_word_count(self) -> None:
        """Follow-up with < 10 words → EXPIRED."""
        val, _ = _make_validator()
        row = _make_detecting_row()
        result = val.validate(row, _converging_signals(), 5, 6.0)
        assert result.status == "EXPIRED"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 4 — Expiration & Manual Override
# ═══════════════════════════════════════════════════════════════════════

class TestExpirationAndOverride:
    """Stale expiration + manual override paths."""

    def test_expire_stale_over_24h(self) -> None:
        val, _ = _make_validator()
        row = _make_detecting_row()
        result = val.expire_stale(row, 24.01)
        assert result.status == "EXPIRED"

    def test_expire_stale_under_24h_unchanged(self) -> None:
        val, _ = _make_validator()
        row = _make_detecting_row()
        result = val.expire_stale(row, 23.0)
        assert result.status == "DETECTING"

    def test_manual_override(self) -> None:
        val, _ = _make_validator()
        row = _make_detecting_row()
        result = val.manual_override(row)
        assert result.status == "MANUAL_OVERRIDE"
        assert result.triggered_priming_at is not None

    def test_manual_override_preserves_detection_id(self) -> None:
        val, _ = _make_validator()
        row = _make_detecting_row()
        result = val.manual_override(row)
        assert result.detection_id == row.detection_id


# ═══════════════════════════════════════════════════════════════════════
# SECTION 5 — Output Schema
# ═══════════════════════════════════════════════════════════════════════

class TestOutputSchema:
    """§5 schema compliance."""

    def test_detecting_row_has_all_fields(self) -> None:
        row = _make_detecting_row()
        assert row.detection_id  # UUID
        assert row.client_id == "c1"
        assert row.coach_id == "coach1"
        assert isinstance(row.analytical_thinking_score, float)
        assert isinstance(row.discrepancy_word_freq, float)
        assert isinstance(row.future_focus_freq, float)
        assert isinstance(row.self_reference_freq, float)
        assert 0.0 <= row.cluster_confidence_score <= 1.0
        assert row.status == "DETECTING"
        assert row.triggered_priming_at is None
        assert row.last_updated

    def test_confirmed_row_has_triggered_at(self) -> None:
        val, _ = _make_validator()
        row = _make_detecting_row()
        result = val.validate(row, _converging_signals(), 20, 6.0)
        assert result.triggered_priming_at is not None
        assert "T" in result.triggered_priming_at  # ISO8601

    def test_status_enum_values(self) -> None:
        for s in SearchPhaseStatus:
            assert s.value in [
                "DETECTING", "CONFIRMED", "PROVISIONAL_WAIT",
                "EXPIRED", "MANUAL_OVERRIDE",
            ]


# ═══════════════════════════════════════════════════════════════════════
# SECTION 6 — ADR-01 Coach Scope & Receipt Chain
# ═══════════════════════════════════════════════════════════════════════

class TestCoachScopeAndReceipt:
    """ADR-01 enforcement + receipt chain."""

    def test_detector_rejects_1char_coach(self) -> None:
        with pytest.raises(ValueError, match="INVALID_COACH_SCOPE"):
            tmp = tempfile.mkdtemp()
            rc = ReceiptChain(coach_acronym="TST", log_dir=tmp)
            SearchPhaseDetector(coach_acronym="X", receipt_chain=rc)

    def test_detector_rejects_5char_coach(self) -> None:
        with pytest.raises(ValueError, match="INVALID_COACH_SCOPE"):
            tmp = tempfile.mkdtemp()
            rc = ReceiptChain(coach_acronym="TST", log_dir=tmp)
            SearchPhaseDetector(coach_acronym="ABCDE", receipt_chain=rc)

    def test_validator_rejects_1char_coach(self) -> None:
        with pytest.raises(ValueError, match="INVALID_COACH_SCOPE"):
            tmp = tempfile.mkdtemp()
            rc = ReceiptChain(coach_acronym="TST", log_dir=tmp)
            ReconsolidationWindowValidator(coach_acronym="X", receipt_chain=rc)

    def test_receipt_emitted_on_convergence(self) -> None:
        det, rc = _make_detector()
        det.check_convergence("c1", "coach1", _converging_signals(), 20)
        entries = rc.query(action="search-convergence-check")
        assert len(entries) >= 1
        assert entries[0].agent_id == "search-phase-detector"

    def test_receipt_emitted_on_validate(self) -> None:
        val, rc = _make_validator()
        row = _make_detecting_row()
        val.validate(row, _converging_signals(), 20, 6.0)
        entries = rc.query(action="search-window-validate")
        assert len(entries) >= 1
        assert entries[0].agent_id == "reconsolidation-window-validator"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 7 — Acceptance Criteria
# ═══════════════════════════════════════════════════════════════════════

class TestAcceptanceCriteria:
    """Verbatim AC1-AC3 from the spec."""

    def test_ac1_single_dimension_outlier_blocked(self) -> None:
        """AC1: info_seeking=0.9 but future_focus=0.0 → False (no row)."""
        det, _ = _make_detector()
        signals = SearchLiwcSignals(
            info_seeking=0.9,
            future_focus=0.0,
            agency_words=0.08,
            hedging_words=0.01,
        )
        row = det.check_convergence("c1", "coach1", signals, 20)
        assert row is None

    def test_ac2_two_hits_within_2_hours_provisional(self) -> None:
        """AC2: Client hits 4 constraints twice within 2 hours → PROVISIONAL_WAIT."""
        val, _ = _make_validator()
        row = _make_detecting_row()
        result = val.validate(row, _converging_signals(), 20, 2.0)
        assert result.status == "PROVISIONAL_WAIT"

    def test_ac3_24h_expiration(self) -> None:
        """AC3: DETECTING row older than 24h0m → EXPIRED."""
        val, _ = _make_validator()
        row = _make_detecting_row()
        result = val.expire_stale(row, 24.01)
        assert result.status == "EXPIRED"
