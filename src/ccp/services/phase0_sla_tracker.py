"""
FR-ERA3-38 Phase-0 SLA Tracker Service
=======================================
Calculates countdown windows, categorizes risk levels, and manages SLA tracking records.
"""

from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.phase0_operator_console_models import Phase0SlaState


class Phase0SlaTracker:
    """Service responsible for tracking SLA execution targets for outreach packages."""

    def __init__(self, receipt_chain: Optional[ReceiptChain] = None):
        self.receipt_chain = receipt_chain

    def start_tracking(
        self,
        coach_id: str,
        phase0_packet_id: str,
        sla_started_at_utc: datetime,
        based_on_run_id: Optional[str] = None,
    ) -> Phase0SlaState:
        """Commences monitoring for an outreach package and logs a receipt of trace."""
        sla_deadline_utc = sla_started_at_utc + timezone_utc_offset()
        
        current_time = datetime.now(timezone.utc)
        minutes_remaining = int((sla_deadline_utc - current_time).total_seconds() / 60)
        risk_band = self.resolve_risk_band(minutes_remaining)
        
        sla_state = Phase0SlaState(
            coach_id=coach_id,
            phase0_packet_id=phase0_packet_id,
            sla_started_at_utc=sla_started_at_utc,
            sla_deadline_utc=sla_deadline_utc,
            minutes_remaining=minutes_remaining,
            risk_band=risk_band,
            breached=(minutes_remaining <= 0),
            based_on_run_id=based_on_run_id,
            updated_at_utc=current_time,
        )

        if self.receipt_chain is not None:
            self.receipt_chain.log(
                action="PHASE0-SLA-TRACKER-INIT",
                coach_acronym=coach_id[:3].upper() if len(coach_id) >= 3 else "P0W",
                payload={
                    "phase0_packet_id": phase0_packet_id,
                    "sla_started_at": sla_started_at_utc.isoformat(),
                    "sla_deadline": sla_deadline_utc.isoformat(),
                    "risk_band": risk_band,
                },
            )

        return sla_state

    def update_sla_status(
        self,
        sla_state: Phase0SlaState,
        current_time: Optional[datetime] = None,
    ) -> Phase0SlaState:
        """Recalculates countdown minutes and stamps the updated risk category."""
        if current_time is None:
            current_time = datetime.now(timezone.utc)

        # Make sure current_time is timezone aware for matching
        if current_time.tzinfo is None:
            current_time = current_time.replace(tzinfo=timezone.utc)
        
        deadline = sla_state.sla_deadline_utc
        if deadline.tzinfo is None:
            deadline = deadline.replace(tzinfo=timezone.utc)

        minutes_remaining = int((deadline - current_time).total_seconds() / 60)
        risk_band = self.resolve_risk_band(minutes_remaining)
        
        sla_state.minutes_remaining = minutes_remaining
        sla_state.risk_band = risk_band
        sla_state.breached = (minutes_remaining <= 0)
        sla_state.updated_at_utc = current_time
        
        return sla_state

    @staticmethod
    def resolve_risk_band(minutes_remaining: int) -> Literal["GREEN", "YELLOW", "ORANGE", "RED", "BREACHED"]:
        """Resolves minutes remaining to a canonical risk color-band."""
        if minutes_remaining <= 0:
            return "BREACHED"
        elif minutes_remaining <= 60:
            return "RED"
        elif minutes_remaining <= 180:
            return "ORANGE"
        elif minutes_remaining <= 360:
            return "YELLOW"
        else:
            return "GREEN"


def timezone_utc_offset() -> timezone | datetime.timedelta:
    """Helper to return the strict 24-hour timedelta representing delivery SLA window."""
    import datetime as dt
    return dt.timedelta(hours=24)
