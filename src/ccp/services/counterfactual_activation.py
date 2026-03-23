"""
FR-CBCS-13: Counterfactual Activation Window
=============================================
Two classes:
  CounterfactualTriggerRouter  — Stage 1: resolves ActivationMode from primary_driver
  EpistemicDeliveryGuard       — Stage 2: temporal gate + LIWC provisional edge-case
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cbcs_models import (
    ActivationMode,
    COUNTERFACTUAL_GATE_HOURS,
    COUNTERFACTUAL_PROVISIONAL_COGNITIVE_THRESHOLD,
    COUNTERFACTUAL_PROVISIONAL_MIN_HOURS,
    CounterfactualError,
    DOWNWARD_DRIVERS,
    EpistemicActivationRow,
    EpistemicGateVerdict,
    UPWARD_DRIVERS,
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
# Stage 1 — CounterfactualTriggerRouter
# ══════════════════════════════════════════════════════════════════════


class CounterfactualTriggerRouter:
    """
    Resolves ActivationMode from the client's identity profile primary_driver.

    UPWARD_COUNTERFACTUAL  → primary_driver ∈ UPWARD_DRIVERS
    DOWNWARD_COUNTERFACTUAL → primary_driver ∈ DOWNWARD_DRIVERS
    Unknown driver          → raises ValueError with ROUTING_ERROR
    """

    def __init__(self, coach_id: str) -> None:
        _validate_coach_id(coach_id)
        self._coach_id = coach_id

    # ------------------------------------------------------------------

    def resolve_activation_mode(self, primary_driver: str) -> ActivationMode:
        """
        Map a primary_driver string to the correct ActivationMode enum.

        Parameters
        ----------
        primary_driver:
            String from UnifiedIdentityProfile.emotional_architecture.primary_driver

        Returns
        -------
        ActivationMode
        """
        if primary_driver in UPWARD_DRIVERS:
            return ActivationMode.UPWARD_COUNTERFACTUAL
        if primary_driver in DOWNWARD_DRIVERS:
            return ActivationMode.DOWNWARD_COUNTERFACTUAL
        raise ValueError(
            f"{CounterfactualError.ROUTING_ERROR}: "
            f"Unknown primary_driver {primary_driver!r}. "
            f"Valid upward={UPWARD_DRIVERS}, downward={DOWNWARD_DRIVERS}"
        )


# ══════════════════════════════════════════════════════════════════════
# Stage 2 — EpistemicDeliveryGuard
# ══════════════════════════════════════════════════════════════════════


class EpistemicDeliveryGuard:
    """
    Epistemic Check-in Gate — enforces temporal delivery bounds and
    emits EpistemicActivationRow.

    Gate logic (§4):
    ┌───────────────────────────────────────────────────────────────────┐
    │ PASS               │ hours ≥ 72 AND client_replied == False       │
    │ PROVISIONAL_EARLY  │ 48 ≤ hours < 72 AND NOT replied AND          │
    │                    │ liwc_cog_processes > 0.1                     │
    │ FAIL_BLOCKED       │ client_replied == True  OR                   │
    │                    │ hours < 72 (not reaching provisional)        │
    └───────────────────────────────────────────────────────────────────┘
    """

    def __init__(
        self,
        coach_id: str,
        receipt_chain: ReceiptChain | None = None,
    ) -> None:
        _validate_coach_id(coach_id)
        self._coach_id = coach_id
        self._rc = receipt_chain
        self._router = CounterfactualTriggerRouter(coach_id=coach_id)

    # ------------------------------------------------------------------

    def evaluate(
        self,
        client_id: str,
        primary_driver: str,
        hours_since_offer: float,
        client_replied_to_offer: bool,
        liwc_cog_processes: float = 0.0,
        dispatched_text: str | None = None,
    ) -> EpistemicActivationRow:
        """
        Evaluate the epistemic delivery gate and return an EpistemicActivationRow.

        Parameters
        ----------
        client_id:
            Identifier for the client.
        primary_driver:
            From UnifiedIdentityProfile.emotional_architecture.primary_driver.
        hours_since_offer:
            Float hours elapsed since Day 0 offer was sent.
        client_replied_to_offer:
            True if the client has already replied to the offer.
        liwc_cog_processes:
            Trailing LIWC cognitive_processes score (0.0–1.0).
        dispatched_text:
            The finalized counterfactual script (populated only on PASS or
            operator override; None otherwise).

        Returns
        -------
        EpistemicActivationRow
        """
        if hours_since_offer < 0:
            raise ValueError(
                f"{CounterfactualError.INVALID_HOURS_ELAPSED}: "
                f"hours_since_offer must be ≥ 0, got {hours_since_offer}"
            )

        activation_mode = self._router.resolve_activation_mode(primary_driver)
        verdict = self._compute_verdict(
            hours_since_offer, client_replied_to_offer, liwc_cog_processes
        )

        # Only PASS (and operator overrides) carry dispatched_text
        resolved_text = dispatched_text if verdict != EpistemicGateVerdict.FAIL_BLOCKED else None

        row = EpistemicActivationRow(
            eval_id=str(uuid.uuid4()),
            client_id=client_id,
            coach_id=self._coach_id,
            activation_mode_assigned=activation_mode.value,
            gate_verdict=verdict.value,
            hours_elapsed_since_offer=hours_since_offer,
            dispatched_text=resolved_text,
            last_evaluated=datetime.now(timezone.utc).isoformat(),
        )

        if self._rc is not None:
            self._rc.log(
                agent_id="epistemic-delivery-guard",
                action="epistemic-gate-evaluate",
                output_summary=(
                    f"client={client_id} mode={activation_mode.value} "
                    f"verdict={verdict.value} hours={hours_since_offer:.1f}"
                ),
            )

        return row

    # ------------------------------------------------------------------

    @staticmethod
    def _compute_verdict(
        hours: float,
        replied: bool,
        cog_processes: float,
    ) -> EpistemicGateVerdict:
        """
        Pure verdict computation — no side effects.

        FAIL_BLOCKED wins if client already replied.
        PASS if hours ≥ 72 and not replied.
        PROVISIONAL if 48 ≤ hours < 72, not replied, and cog_processes > 0.1.
        FAIL_BLOCKED otherwise.
        """
        if replied:
            return EpistemicGateVerdict.FAIL_BLOCKED

        if hours >= COUNTERFACTUAL_GATE_HOURS:
            return EpistemicGateVerdict.PASS

        if (
            hours >= COUNTERFACTUAL_PROVISIONAL_MIN_HOURS
            and cog_processes > COUNTERFACTUAL_PROVISIONAL_COGNITIVE_THRESHOLD
        ):
            return EpistemicGateVerdict.PROVISIONAL_EARLY_FIRE

        return EpistemicGateVerdict.FAIL_BLOCKED
