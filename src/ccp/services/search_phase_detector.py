"""
FR-CBCS-06 — SEARCH Phase Detection Engine
============================================
4-signal linguistic convergence detection with 24-hour reconsolidation
window validation and state machine lifecycle.

Spec ref: FR_CBCS_06_SEARCH_Phase_Detection_Engine_Tech_Spec.md
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

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


class SearchPhaseDetector:
    """Detects SEARCH phase onset via 4-signal LIWC convergence.

    Parameters
    ----------
    coach_acronym : str
        2-4 character coach identifier (ADR-01).
    receipt_chain : ReceiptChain
        Immutable audit trail.
    """

    def __init__(self, coach_acronym: str, receipt_chain: ReceiptChain) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(SearchPhaseError.INVALID_COACH_SCOPE.value)
        self._coach = coach_acronym
        self._rc = receipt_chain

    # ── Stage 1: Convergence Check ─────────────────────────────────────

    def check_convergence(
        self,
        client_id: str,
        coach_id: str,
        signals: SearchLiwcSignals,
        word_count: int,
    ) -> SearchPhaseDetectionRow | None:
        """Evaluate 4-signal convergence on a client message.

        Parameters
        ----------
        client_id : str
            Unique client identifier.
        coach_id : str
            Coach boundary (ADR-01).
        signals : SearchLiwcSignals
            LIWC-22 signal values.
        word_count : int
            Total words in the message (must be >= 10).

        Returns
        -------
        SearchPhaseDetectionRow | None
            A DETECTING row if convergence met, None otherwise.
        """
        if word_count < SEARCH_MIN_WORD_COUNT:
            return None

        converged = self._signals_converge(signals)
        if not converged:
            return None

        confidence = self._cluster_confidence(signals)

        row = SearchPhaseDetectionRow(
            detection_id=str(uuid.uuid4()),
            client_id=client_id,
            coach_id=coach_id,
            analytical_thinking_score=signals.info_seeking,
            discrepancy_word_freq=signals.hedging_words,
            future_focus_freq=signals.future_focus,
            self_reference_freq=signals.agency_words,
            cluster_confidence_score=round(confidence, 4),
            status=SearchPhaseStatus.DETECTING.value,
            triggered_priming_at=None,
            last_updated=datetime.now(timezone.utc).isoformat(),
        )

        self._rc.log(
            agent_id="search-phase-detector",
            action="search-convergence-check",
            asset_id=row.detection_id,
            person_id=client_id,
            input_summary=f"word_count={word_count}, signals={signals.model_dump()}",
            output_summary=f"status=DETECTING, confidence={confidence:.4f}",
        )
        return row

    # ── Signal Convergence (§4 Stage 1) ────────────────────────────────

    @staticmethod
    def _signals_converge(s: SearchLiwcSignals) -> bool:
        """All 4 signals must meet thresholds simultaneously."""
        return (
            s.info_seeking > SEARCH_INFO_SEEKING_THRESHOLD
            and s.future_focus > SEARCH_FUTURE_FOCUS_THRESHOLD
            and s.agency_words > SEARCH_AGENCY_WORDS_THRESHOLD
            and s.hedging_words < SEARCH_HEDGING_WORDS_MAX
        )

    # ── Cluster Confidence ─────────────────────────────────────────────

    @staticmethod
    def _cluster_confidence(s: SearchLiwcSignals) -> float:
        """Average of normalized 4 metrics mapped to 0.0-1.0 band.

        For the 3 'above threshold' signals: ratio = value / (threshold * 2).
        For hedging (below threshold): ratio = 1.0 - (value / (threshold * 2)).
        All clamped to [0.0, 1.0].
        """
        def _norm_above(val: float, threshold: float) -> float:
            if threshold == 0:
                return 1.0 if val > 0 else 0.0
            return min(1.0, max(0.0, val / (threshold * 2)))

        def _norm_below(val: float, threshold: float) -> float:
            if threshold == 0:
                return 0.0
            return min(1.0, max(0.0, 1.0 - (val / (threshold * 2))))

        scores = [
            _norm_above(s.info_seeking, SEARCH_INFO_SEEKING_THRESHOLD),
            _norm_above(s.future_focus, SEARCH_FUTURE_FOCUS_THRESHOLD),
            _norm_above(s.agency_words, SEARCH_AGENCY_WORDS_THRESHOLD),
            _norm_below(s.hedging_words, SEARCH_HEDGING_WORDS_MAX),
        ]
        return sum(scores) / len(scores)


class ReconsolidationWindowValidator:
    """Validates SEARCH detections through the 4h-24h reconsolidation window.

    Parameters
    ----------
    coach_acronym : str
        2-4 character coach identifier (ADR-01).
    receipt_chain : ReceiptChain
        Immutable audit trail.
    """

    def __init__(self, coach_acronym: str, receipt_chain: ReceiptChain) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(SearchPhaseError.INVALID_COACH_SCOPE.value)
        self._coach = coach_acronym
        self._rc = receipt_chain

    # ── Stage 2: Window Validation ─────────────────────────────────────

    def validate(
        self,
        detection: SearchPhaseDetectionRow,
        followup_signals: SearchLiwcSignals,
        followup_word_count: int,
        hours_since_detecting: float,
    ) -> SearchPhaseDetectionRow:
        """Validate a DETECTING row against a follow-up message.

        Parameters
        ----------
        detection : SearchPhaseDetectionRow
            The existing DETECTING row.
        followup_signals : SearchLiwcSignals
            LIWC signals from the follow-up message.
        followup_word_count : int
            Word count of the follow-up message.
        hours_since_detecting : float
            Hours elapsed since the DETECTING timestamp.

        Returns
        -------
        SearchPhaseDetectionRow
            Updated row with new status.
        """
        now_iso = datetime.now(timezone.utc).isoformat()

        # Follow-up must also pass convergence + word count
        if followup_word_count < SEARCH_MIN_WORD_COUNT:
            return self._transition(detection, SearchPhaseStatus.EXPIRED, now_iso)

        converged = SearchPhaseDetector._signals_converge(followup_signals)
        if not converged:
            return self._transition(detection, SearchPhaseStatus.EXPIRED, now_iso)

        # Time-window gating (§4 Stage 2)
        if hours_since_detecting > SEARCH_MAX_HOURS:
            return self._transition(detection, SearchPhaseStatus.EXPIRED, now_iso)

        if hours_since_detecting < SEARCH_MIN_HOURS:
            # Possible monologue loop → PROVISIONAL_WAIT
            result = self._transition(
                detection, SearchPhaseStatus.PROVISIONAL_WAIT, now_iso
            )
            self._rc.log(
                agent_id="reconsolidation-window-validator",
                action="search-window-validate",
                asset_id=detection.detection_id,
                person_id=detection.client_id,
                input_summary=f"hours={hours_since_detecting:.2f}",
                output_summary="status=PROVISIONAL_WAIT (monologue guard)",
            )
            return result

        # 4h <= hours <= 24h → CONFIRMED
        result = self._transition(
            detection, SearchPhaseStatus.CONFIRMED, now_iso,
            triggered_at=now_iso,
        )
        self._rc.log(
            agent_id="reconsolidation-window-validator",
            action="search-window-validate",
            asset_id=detection.detection_id,
            person_id=detection.client_id,
            input_summary=f"hours={hours_since_detecting:.2f}",
            output_summary="status=CONFIRMED",
        )
        return result

    # ── Expiration Check ───────────────────────────────────────────────

    def expire_stale(
        self,
        detection: SearchPhaseDetectionRow,
        hours_since_detecting: float,
    ) -> SearchPhaseDetectionRow:
        """Expire a DETECTING row that exceeded the 24h window (AC3).

        Parameters
        ----------
        detection : SearchPhaseDetectionRow
            Row to check.
        hours_since_detecting : float
            Hours elapsed since DETECTING timestamp.

        Returns
        -------
        SearchPhaseDetectionRow
            Updated row (EXPIRED if > 24h, unchanged otherwise).
        """
        if hours_since_detecting > SEARCH_MAX_HOURS:
            now_iso = datetime.now(timezone.utc).isoformat()
            result = self._transition(detection, SearchPhaseStatus.EXPIRED, now_iso)
            self._rc.log(
                agent_id="reconsolidation-window-validator",
                action="search-expire-stale",
                asset_id=detection.detection_id,
                person_id=detection.client_id,
                input_summary=f"hours={hours_since_detecting:.2f}",
                output_summary="status=EXPIRED (24h window exceeded)",
            )
            return result
        return detection

    # ── Manual Override ────────────────────────────────────────────────

    def manual_override(
        self,
        detection: SearchPhaseDetectionRow,
    ) -> SearchPhaseDetectionRow:
        """Apply MANUAL_OVERRIDE status (operator command)."""
        now_iso = datetime.now(timezone.utc).isoformat()
        result = self._transition(
            detection, SearchPhaseStatus.MANUAL_OVERRIDE, now_iso,
            triggered_at=now_iso,
        )
        self._rc.log(
            agent_id="reconsolidation-window-validator",
            action="search-manual-override",
            asset_id=detection.detection_id,
            person_id=detection.client_id,
            input_summary="operator_override",
            output_summary="status=MANUAL_OVERRIDE",
        )
        return result

    # ── State Transition ───────────────────────────────────────────────

    @staticmethod
    def _transition(
        detection: SearchPhaseDetectionRow,
        new_status: SearchPhaseStatus,
        now_iso: str,
        triggered_at: str | None = None,
    ) -> SearchPhaseDetectionRow:
        """Create updated row with new status."""
        return SearchPhaseDetectionRow(
            detection_id=detection.detection_id,
            client_id=detection.client_id,
            coach_id=detection.coach_id,
            analytical_thinking_score=detection.analytical_thinking_score,
            discrepancy_word_freq=detection.discrepancy_word_freq,
            future_focus_freq=detection.future_focus_freq,
            self_reference_freq=detection.self_reference_freq,
            cluster_confidence_score=detection.cluster_confidence_score,
            status=new_status.value,
            triggered_priming_at=triggered_at or detection.triggered_priming_at,
            last_updated=now_iso,
        )
