"""
FR-CBCS-14: Conscious Relationship Nurturing Architecture
==========================================================
Two classes:
  CycleStateRouter               — Stage 1: resolves ActiveCycle from orchestration context
  ConsciousNurturingOrchestrator — Stage 2: cooldown gate + queue lock enforcement
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cbcs_models import (
    ActiveCycle,
    COMMERCIAL_COOLDOWN_DAYS,
    COMMERCIAL_COOLDOWN_INFO_SEEKING_THRESHOLD,
    COMMERCIAL_COOLDOWN_PROVISIONAL_MIN_DAYS,
    CooldownGateVerdict,
    NurturingArchError,
    RelationshipCycleLog,
    WEEKLY_CYCLE_WEEKDAY,
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
# Stage 1 — CycleStateRouter
# ══════════════════════════════════════════════════════════════════════


class CycleStateRouter:
    """
    Resolves the meta-state ActiveCycle enum for a given client.

    Hierarchy (highest priority first):
    1. CAMPAIGN — search_phase_confirmed OR operator_manual_trigger
    2. WEEKLY   — current weekday == Sunday AND no CAMPAIGN override
    3. DAILY    — default fallback
    """

    def __init__(self, coach_id: str) -> None:
        _validate_coach_id(coach_id)
        self._coach_id = coach_id

    # ------------------------------------------------------------------

    def resolve_cycle(
        self,
        search_phase_confirmed: bool = False,
        operator_manual_trigger: bool = False,
        current_weekday: int | None = None,
    ) -> ActiveCycle:
        """
        Determine the active orchestration cycle.

        Parameters
        ----------
        search_phase_confirmed:
            True if FR-CBCS-06 returned SearchPhaseStatus.CONFIRMED.
        operator_manual_trigger:
            True if an operator has explicitly triggered a campaign.
        current_weekday:
            Numeric weekday (0=Monday, 6=Sunday). Defaults to today's UTC weekday.

        Returns
        -------
        ActiveCycle
        """
        if current_weekday is None:
            current_weekday = datetime.now(timezone.utc).weekday()

        # CAMPAIGN wins over everything
        if search_phase_confirmed or operator_manual_trigger:
            return ActiveCycle.CAMPAIGN

        # WEEKLY on Sundays (no campaign)
        if current_weekday == WEEKLY_CYCLE_WEEKDAY:
            return ActiveCycle.WEEKLY

        # DAILY default
        return ActiveCycle.DAILY


# ══════════════════════════════════════════════════════════════════════
# Stage 2 — ConsciousNurturingOrchestrator
# ══════════════════════════════════════════════════════════════════════


class ConsciousNurturingOrchestrator:
    """
    Meta-level governance layer for all CBCS components.

    Responsibilities:
    - Resolves active cycle state (DAILY / WEEKLY / CAMPAIGN)
    - Enforces queue_lock_active for CAMPAIGN isolation
    - Applies 21-day Commercial Cooldown Gate to offer dispatch
    - Emits RelationshipCycleLog with full audit trail
    """

    def __init__(
        self,
        coach_id: str,
        receipt_chain: ReceiptChain | None = None,
    ) -> None:
        _validate_coach_id(coach_id)
        self._coach_id = coach_id
        self._rc = receipt_chain
        self._router = CycleStateRouter(coach_id=coach_id)

    # ------------------------------------------------------------------

    def orchestrate(
        self,
        client_id: str,
        days_since_last_offer: float,
        last_offer_sent_utc: datetime | None = None,
        search_phase_confirmed: bool = False,
        operator_manual_trigger: bool = False,
        contains_offer: bool = False,
        liwc_info_seeking: float = 0.0,
        current_weekday: int | None = None,
        last_executed_node: str = "NONE",
    ) -> RelationshipCycleLog:
        """
        Evaluate one orchestration tick and emit a RelationshipCycleLog.

        Parameters
        ----------
        client_id:
            Identifier for the client.
        days_since_last_offer:
            Float days since any commercial offer was dispatched.
        last_offer_sent_utc:
            UTC datetime of last offer send (used to compute expiry). If None,
            computed as now() - days_since_last_offer.
        search_phase_confirmed:
            True if Search Phase is currently CONFIRMED (triggers CAMPAIGN).
        operator_manual_trigger:
            True if operator manually initiated a campaign.
        contains_offer:
            True if the outbound payload this tick contains a commercial offer.
        liwc_info_seeking:
            Client's trailing LIWC info_seeking score (0.0–1.0).
        current_weekday:
            Override for day-of-week (0=Mon, 6=Sun). Defaults to UTC today.
        last_executed_node:
            Label of the last FR-CBCS node that ran (for audit trail).

        Returns
        -------
        RelationshipCycleLog
        """
        if days_since_last_offer < 0:
            raise ValueError(
                f"{NurturingArchError.INVALID_DAYS_ELAPSED}: "
                f"days_since_last_offer must be ≥ 0, got {days_since_last_offer}"
            )

        active_cycle = self._router.resolve_cycle(
            search_phase_confirmed=search_phase_confirmed,
            operator_manual_trigger=operator_manual_trigger,
            current_weekday=current_weekday,
        )

        # Queue lock is active whenever we're in CAMPAIGN mode
        queue_lock_active = active_cycle == ActiveCycle.CAMPAIGN

        # Cooldown gate — only evaluated when payload contains an offer
        cooldown_verdict = self._compute_cooldown_verdict(
            days_since_last_offer=days_since_last_offer,
            contains_offer=contains_offer,
            liwc_info_seeking=liwc_info_seeking,
        )

        # Compute cooldown expiry: last_offer_sent + 21 days
        if last_offer_sent_utc is None:
            last_offer_sent_utc = datetime.now(timezone.utc) - timedelta(days=days_since_last_offer)
        cooldown_expiry = last_offer_sent_utc + timedelta(days=COMMERCIAL_COOLDOWN_DAYS)
        cooldown_expiry_ts = cooldown_expiry.isoformat()

        row = RelationshipCycleLog(
            orchestration_id=str(uuid.uuid4()),
            client_id=client_id,
            coach_id=self._coach_id,
            active_cycle=active_cycle.value,
            queue_lock_active=queue_lock_active,
            cooldown_gate_verdict=cooldown_verdict.value,
            cooldown_expiry_timestamp=cooldown_expiry_ts,
            last_executed_node=last_executed_node,
            computation_timestamp=datetime.now(timezone.utc).isoformat(),
        )

        if self._rc is not None:
            self._rc.log(
                agent_id="conscious-nurturing-orchestrator",
                action="relationship-cycle-orchestrate",
                output_summary=(
                    f"client={client_id} cycle={active_cycle.value} "
                    f"queue_lock={queue_lock_active} cooldown={cooldown_verdict.value}"
                ),
            )

        return row

    # ------------------------------------------------------------------

    @staticmethod
    def _compute_cooldown_verdict(
        days_since_last_offer: float,
        contains_offer: bool,
        liwc_info_seeking: float,
    ) -> CooldownGateVerdict:
        """
        Compute commercial cooldown gate verdict.

        If payload does NOT contain an offer → PASS (no gate needed).
        If days > 21 → PASS.
        If 14 < days ≤ 21 AND info_seeking > 0.1 → PROVISIONAL_OVERRIDE.
        Else → FAIL_COOLDOWN_ACTIVE.
        """
        if not contains_offer:
            return CooldownGateVerdict.PASS

        if days_since_last_offer > COMMERCIAL_COOLDOWN_DAYS:
            return CooldownGateVerdict.PASS

        if (
            days_since_last_offer > COMMERCIAL_COOLDOWN_PROVISIONAL_MIN_DAYS
            and liwc_info_seeking > COMMERCIAL_COOLDOWN_INFO_SEEKING_THRESHOLD
        ):
            return CooldownGateVerdict.PROVISIONAL_OVERRIDE

        return CooldownGateVerdict.FAIL_COOLDOWN_ACTIVE
