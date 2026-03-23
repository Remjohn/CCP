"""
FR55: Session Booking Intelligence
====================================
Two classes:
  ConvergenceDetector       — Stage 1: 4-signal convergence matrix
  BookingReadinessEvaluator — Stage 2: gate verdict + OperatorBookingBriefRow
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

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

_ADR01_MIN = 2
_ADR01_MAX = 4


def _validate_coach_id(coach_id: str) -> None:
    if not (_ADR01_MIN <= len(coach_id) <= _ADR01_MAX):
        raise ValueError(
            f"ADR-01: coach_id must be {_ADR01_MIN}-{_ADR01_MAX} chars; "
            f"got {len(coach_id)!r}"
        )


# ══════════════════════════════════════════════════════════════════════
# Stage 1 — ConvergenceDetector
# ══════════════════════════════════════════════════════════════════════


class ConvergenceDetector:
    """
    Evaluates the 4-signal convergence matrix (§4 Stage 1).

    Inputs (per client):
      - coping_trajectory (int, 1-5) — from FR-CBCS-04
      - spt_stage (int, 1-5) — from FR-CBCS-02
      - search_phase_status (str) — from FR-CBCS-06 ("CONFIRMED" | other)
      - composite_tii (float, 0.0-1.0) — from FR-CBCS-07

    Resolution rules:
      HIGH_CONFIDENCE_READY → coping ≥ 4 AND spt ≥ 3 AND search == "CONFIRMED" AND tii ≥ 0.4
      WATCHLIST_BUILDING    → coping ≥ 3 AND spt ≥ 3 AND tii ≥ 0.3 (search not required)
      NOT_READY             → everything else
    """

    def __init__(self, coach_id: str) -> None:
        _validate_coach_id(coach_id)
        self._coach_id = coach_id

    # ------------------------------------------------------------------

    def evaluate_convergence(
        self,
        coping_trajectory: int | None,
        spt_stage: int | None,
        search_phase_status: str | None,
        composite_tii: float | None,
    ) -> tuple[RecommendationStatus, float]:
        """
        Resolve recommendation_status and confidence_score from 4 CBCS signals.

        Missing (None) inputs resolve to safe defaults per §6 backward compat:
        coping=0, spt=0, search="UNKNOWN", tii=0.0 → always NOT_READY.

        Returns
        -------
        (RecommendationStatus, confidence_score)
        """
        coping = coping_trajectory if coping_trajectory is not None else 0
        spt = spt_stage if spt_stage is not None else 0
        search = search_phase_status if search_phase_status is not None else "UNKNOWN"
        tii = composite_tii if composite_tii is not None else 0.0

        # HIGH_CONFIDENCE_READY: all 4 must converge
        if (
            coping >= BOOKING_COPING_HIGH
            and spt >= BOOKING_SPT_HIGH
            and search == "CONFIRMED"
            and tii >= BOOKING_TII_HIGH
        ):
            return RecommendationStatus.HIGH_CONFIDENCE_READY, BOOKING_CONFIDENCE_HIGH

        # WATCHLIST_BUILDING: 3 of 4 (search not strictly required)
        if (
            coping >= BOOKING_COPING_WATCH
            and spt >= BOOKING_SPT_WATCH
            and tii >= BOOKING_TII_WATCH
        ):
            return RecommendationStatus.WATCHLIST_BUILDING, BOOKING_CONFIDENCE_WATCH

        # NOT_READY
        return RecommendationStatus.NOT_READY, BOOKING_CONFIDENCE_FAIL


# ══════════════════════════════════════════════════════════════════════
# Stage 2 — BookingReadinessEvaluator
# ══════════════════════════════════════════════════════════════════════


class BookingReadinessEvaluator:
    """
    Booking Readiness Gate + OperatorBookingBriefRow emission (§4 Stage 2).

    Gate verdicts:
      HIGH_CONFIDENCE_READY → PASS → brief pushed to Priority Actions
      WATCHLIST_BUILDING    → PROVISIONAL_WATCHLIST → silent monitoring
      NOT_READY             → FAIL_NURTURE_MODE → client excluded
    """

    def __init__(
        self,
        coach_id: str,
        receipt_chain: ReceiptChain | None = None,
    ) -> None:
        _validate_coach_id(coach_id)
        self._coach_id = coach_id
        self._rc = receipt_chain
        self._detector = ConvergenceDetector(coach_id=coach_id)

    # ------------------------------------------------------------------

    def evaluate(
        self,
        client_id: str,
        coping_trajectory: int | None,
        spt_stage: int | None,
        search_phase_status: str | None,
        composite_tii: float | None,
    ) -> OperatorBookingBriefRow:
        """
        Full evaluation pipeline: convergence → gate → brief row.

        Parameters
        ----------
        client_id:
            Identifier for the client being evaluated.
        coping_trajectory:
            Coping position (1-5) from FR-CBCS-04. None = missing.
        spt_stage:
            SPT stage (1-5) from FR-CBCS-02. None = missing.
        search_phase_status:
            String status from FR-CBCS-06 ("CONFIRMED" | other). None = missing.
        composite_tii:
            Float TII score (0.0-1.0) from FR-CBCS-07. None = missing.

        Returns
        -------
        OperatorBookingBriefRow (DEP-ENG-076)
        """
        # Stage 1 — Convergence detection
        rec_status, confidence = self._detector.evaluate_convergence(
            coping_trajectory=coping_trajectory,
            spt_stage=spt_stage,
            search_phase_status=search_phase_status,
            composite_tii=composite_tii,
        )

        # Log convergence receipt
        if self._rc is not None:
            self._rc.log(
                agent_id="convergence-detector",
                action="convergence-detect",
                output_summary=(
                    f"client={client_id} status={rec_status.value} "
                    f"confidence={confidence}"
                ),
            )

        # Stage 2 — Gate verdict
        gate_verdict = self._map_gate_verdict(rec_status)

        # Build qualifying metrics snapshot (§5 — all 4 populated)
        qualifying_metrics = QualifyingMetrics(
            tii_snapshot=composite_tii if composite_tii is not None else 0.0,
            spt_snapshot=spt_stage if spt_stage is not None else 0,
            search_confirmed=(search_phase_status == "CONFIRMED") if search_phase_status else False,
            coping_tier=coping_trajectory if coping_trajectory is not None else 0,
        )

        row = OperatorBookingBriefRow(
            briefing_id=str(uuid.uuid4()),
            client_id=client_id,
            coach_id=self._coach_id,
            recommendation_status=rec_status.value,
            confidence_score_calc=confidence,
            gate_verdict=gate_verdict.value,
            qualifying_metrics=qualifying_metrics,
            evaluated_at=datetime.now(timezone.utc).isoformat(),
        )

        # Log gate receipt
        if self._rc is not None:
            self._rc.log(
                agent_id="convergence-detector",
                action="booking-readiness-gate",
                output_summary=(
                    f"client={client_id} verdict={gate_verdict.value} "
                    f"briefing_id={row.briefing_id}"
                ),
            )

        return row

    # ------------------------------------------------------------------

    @staticmethod
    def _map_gate_verdict(status: RecommendationStatus) -> BookingGateVerdict:
        """Map recommendation status to gate verdict (§4 Stage 2)."""
        if status == RecommendationStatus.HIGH_CONFIDENCE_READY:
            return BookingGateVerdict.PASS
        if status == RecommendationStatus.WATCHLIST_BUILDING:
            return BookingGateVerdict.PROVISIONAL_WATCHLIST
        return BookingGateVerdict.FAIL_NURTURE_MODE
