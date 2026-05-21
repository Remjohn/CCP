"""
FR58 — Offer Tier Architecture
================================
Financial and psychological routing governor: binds commercial offer
tiers to individual Information Coping Trajectories via the Tier Matrix
and the Upward-Only Routing Gate. Incorporates the Loyalty Unlock Flow (Phase1-M06).

Classes
-------
TierCeilingResolver
    Maps an ICT coping position (1-5 / null) and purchase history to an OfferTierCeiling enum (0-4).

UpwardOnlyRoutingGate
    Evaluates a target campaign tier against the computed ceiling and
    historical purchase maximum, returning an UpwardRoutingVerdict.

OfferTierGovernor
    Orchestrates resolution, SVI evaluation (Loyalty Unlock), routing gate,
    and writes receipt chain entries (DEP-ENG-041).
"""

from __future__ import annotations

import math
import uuid
from datetime import datetime, timezone
from typing import Any

from src.ccp.models.cpsc_models import (
    OfferTierCeiling,
    OfferTierError,
    OfferTierGovernorRow,
    UpwardRoutingVerdict,
)
from src.ccp.core.receipt_chain import ReceiptChain

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Coping position thresholds for 5-layer assignment (§4 Stage 1 Step 2)
# TIER_A_PROOF ($0): coping_position <= 2
# TIER_B_FIRST_PROOF_UNLOCK ($29.99 one-time): coping_position <= 2 AND has purchased tier 1 bridge
# TIER_C_SPEAKING_LEARNING ($39.99/mo): coping_position == 3
# TIER_D_COACH_OS ($99.99/mo): coping_position == 4
# TIER_E_OPERATOR ($199.99/mo): coping_position == 5

TIER_C_COPING: int = 3
TIER_D_COPING: int = 4
TIER_E_COPING: int = 5

# Fail-safe fallback (§4 Stage 1 Step 3): coping=None → TIER_A_PROOF
COPING_NULL_FALLBACK: int = 0

# Integer mappings for tier comparisons (0-4)
_TIER_INT_MAP = {
    OfferTierCeiling.TIER_A_PROOF: 0,
    OfferTierCeiling.TIER_B_FIRST_PROOF_UNLOCK: 1,
    OfferTierCeiling.TIER_C_SPEAKING_LEARNING: 2,
    OfferTierCeiling.TIER_D_COACH_OS: 3,
    OfferTierCeiling.TIER_E_OPERATOR: 4,
}

# Loyalty Unlock Flow Thresholds (§4 Stage 2 Step 2)
LOYALTY_STREAK_MIN_DAYS: int = 30
LOYALTY_PEER_HELPFULNESS_MIN: float = 0.85


# ---------------------------------------------------------------------------
# TierCeilingResolver
# ---------------------------------------------------------------------------

class TierCeilingResolver:
    """
    Maps an ICT coping_position integer to an OfferTierCeiling enum (5-layer).

    Parameters
    ----------
    coping_position : int | None
        Client's Information Coping Trajectory position (1-5).
        None → fallback to COPING_NULL_FALLBACK=0 → TIER_A_PROOF.
    historical_purchased_tiers : list[Any] | None
        Prior purchase history to identify first proof unlock bridge.
    """

    def __init__(self, coping_position: int | None, historical_purchased_tiers: list[Any] | None = None) -> None:
        self._cp = coping_position if coping_position is not None else COPING_NULL_FALLBACK
        self._history = historical_purchased_tiers or []

    def resolve(self) -> tuple[int, OfferTierCeiling]:
        """Return ``(computed_coping_position, eligible_tier_ceiling)``."""
        cp = self._cp
        if cp >= TIER_E_COPING:
            return cp, OfferTierCeiling.TIER_E_OPERATOR
        if cp == TIER_D_COPING:
            return cp, OfferTierCeiling.TIER_D_COACH_OS
        if cp == TIER_C_COPING:
            return cp, OfferTierCeiling.TIER_C_SPEAKING_LEARNING
        
        # cp <= 2 -> Proof tier, upgraded to First Proof Unlock if bridge (1) purchased
        valid_tiers = []
        for v in self._history:
            try:
                fv = float(v)
                if not math.isnan(fv) and fv >= 0:
                    valid_tiers.append(int(fv))
            except (TypeError, ValueError):
                pass
        
        if 1 in valid_tiers:
            return cp, OfferTierCeiling.TIER_B_FIRST_PROOF_UNLOCK
            
        return cp, OfferTierCeiling.TIER_A_PROOF


# ---------------------------------------------------------------------------
# UpwardOnlyRoutingGate
# ---------------------------------------------------------------------------

def _safe_tier_history_max(historical_tiers: list[Any]) -> int:
    """
    Return the maximum valid integer tier from a potentially corrupt list.

    Ignores None, NaN, negative values — defaults to 0 if all values
    are invalid.
    """
    valid: list[int] = []
    for v in (historical_tiers or []):
        try:
            fv = float(v)
            if not math.isnan(fv) and fv >= 0:
                valid.append(int(fv))
        except (TypeError, ValueError):
            pass
    return max(valid) if valid else 0


class UpwardOnlyRoutingGate:
    """
    Enforces upward-only tier routing for the 5-layer model.

    Parameters
    ----------
    target_tier : int
        Campaign tier FR59 wants to send to the client (0, 1, 2, 3, or 4).
    ceiling : OfferTierCeiling
        Computed tier ceiling from TierCeilingResolver.
    historical_tiers : list
        Prior purchase tier history. Corrupt values (None, NaN, -1)
        are treated as 0.

    Gate logic
    ----------
    ceiling_int = _TIER_INT_MAP[ceiling]
    history_max = safe_max(historical_tiers)

    FAIL_CAPACITY_EXCEEDED : target > ceiling_int
    PROVISIONAL_DOWNSELL   : target <= ceiling_int AND target < history_max
    PASS_AUTHORIZED        : target <= ceiling_int AND target >= history_max
    """

    def __init__(
        self,
        target_tier: int,
        ceiling: OfferTierCeiling,
        historical_tiers: list[Any],
    ) -> None:
        self._target = target_tier
        self._ceiling_int = _TIER_INT_MAP[ceiling]
        self._history_max = _safe_tier_history_max(historical_tiers)

    def evaluate(self) -> UpwardRoutingVerdict:
        if self._target > self._ceiling_int:
            return UpwardRoutingVerdict.FAIL_CAPACITY_EXCEEDED
        if self._target < self._history_max:
            return UpwardRoutingVerdict.PROVISIONAL_DOWNSELL_ATTEMPT
        return UpwardRoutingVerdict.PASS_AUTHORIZED


# ---------------------------------------------------------------------------
# OfferTierGovernor
# ---------------------------------------------------------------------------

class OfferTierGovernor:
    """
    Orchestrates FR58: resolves 5-layer ceiling, executes Loyalty Unlock Flow,
    evaluates upward-only gate, and returns an OfferTierGovernorRow.

    Parameters
    ----------
    coach_id : str
        ADR-01 boundary key.
    receipt_chain : ReceiptChain
        Live receipt chain (DEP-ENG-041).
    engagement_feedback : Any
        Service to fetch SVI (Stored Value Index) metrics (DEP-ENG-091).
    """

    _AGENT_ID = "offer-tier-governor"

    def __init__(self, coach_id: str, receipt_chain: ReceiptChain, engagement_feedback: Any = None) -> None:
        if not isinstance(coach_id, str) or len(coach_id) < 2:
            raise ValueError("coach_id must be a non-empty string (min 2 chars).")
        self._coach_id = coach_id
        self._rc = receipt_chain
        self._engagement = engagement_feedback

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def _evaluate_loyalty_unlock(self, client_id: str, ceiling: OfferTierCeiling) -> OfferTierCeiling:
        """Execute Phase1-M06 The Stored Value Rule (§4 Stage 2).

        If a user is TIER_A_PROOF but has high SVI, organically unlock
        TIER_C_SPEAKING_LEARNING via entitlement grant.
        """
        if ceiling != OfferTierCeiling.TIER_A_PROOF:
            return ceiling

        # Fetch SVI metrics
        streak_days = 0
        helpfulness = 0.0
        if self._engagement:
            try:
                metrics = self._engagement.get_svi_metrics(client_id)
                streak_days = metrics.get("streak_days", 0)
                helpfulness = metrics.get("peer_helpfulness_score", 0.0)
            except Exception:
                pass  # Fail closed: no unlock if service fails

        if streak_days >= LOYALTY_STREAK_MIN_DAYS and helpfulness >= LOYALTY_PEER_HELPFULNESS_MIN:
            new_ceiling = OfferTierCeiling.TIER_C_SPEAKING_LEARNING
            self._rc.log(
                agent_id=self._AGENT_ID,
                action="loyalty-unlock-granted",
                output_summary=(
                    f"coach={self._coach_id} client={client_id} "
                    f"streak={streak_days} helpfulness={helpfulness} "
                    f"granted={new_ceiling.value}"
                ),
            )
            return new_ceiling

        return ceiling

    def evaluate(
        self,
        *,
        client_id: str,
        coping_position: int | None,
        target_campaign_tier: int,
        historical_purchased_tiers: list[Any] | None = None,
    ) -> OfferTierGovernorRow:
        """
        Evaluate offer routing and return an OfferTierGovernorRow.

        Parameters
        ----------
        client_id : str
            Target prospect / client identifier.
        coping_position : int | None
            ICT coping position (1-5). None → TIER_A baseline.
        target_campaign_tier : int
            Campaign tier FR59 wants to assign (0, 1, 2, 3, or 4).
        historical_purchased_tiers : list | None
            Prior purchase history. May contain corrupt values.

        Returns
        -------
        OfferTierGovernorRow

        Raises
        ------
        ValueError(OfferTierError.FAIL_CAPACITY_EXCEEDED)
            If target tier exceeds eligible ceiling (hard abort,
            receipt logged before raising).
        """
        history = historical_purchased_tiers or []

        # ── Stage 1: Tier Ceiling Resolution ─────────────────────────
        cp, ceiling = TierCeilingResolver(coping_position, history).resolve()

        # ── Stage 2: Loyalty Unlock Flow ─────────────────────────────
        ceiling = self._evaluate_loyalty_unlock(client_id, ceiling)

        root_receipt = self._rc.log(
            agent_id=self._AGENT_ID,
            action="tier-ceiling-resolve",
            output_summary=(
                f"coach={self._coach_id} client={client_id} "
                f"coping={cp} ceiling={ceiling.value}"
            ),
        )

        # ── Stage 3: Upward-Only Routing Gate ────────────────────────
        gate = UpwardOnlyRoutingGate(target_campaign_tier, ceiling, history)
        verdict = gate.evaluate()

        if verdict == UpwardRoutingVerdict.FAIL_CAPACITY_EXCEEDED:
            self._rc.log(
                agent_id=self._AGENT_ID,
                action="offer-routing-gate",
                output_summary=(
                    f"coach={self._coach_id} client={client_id} "
                    f"target={target_campaign_tier} ceiling={ceiling.value} "
                    "verdict=FAIL_CAPACITY_EXCEEDED — client excluded silently"
                ),
                parent_receipt_id=root_receipt.receipt_id,
            )
            raise ValueError(OfferTierError.FAIL_CAPACITY_EXCEEDED)

        self._rc.log(
            agent_id=self._AGENT_ID,
            action="offer-routing-gate",
            output_summary=(
                f"coach={self._coach_id} client={client_id} "
                f"target={target_campaign_tier} verdict={verdict.value}"
            ),
            parent_receipt_id=root_receipt.receipt_id,
        )

        return OfferTierGovernorRow(
            governor_evaluation_id=str(uuid.uuid4()),
            client_id=client_id,
            coach_id=self._coach_id,
            computed_coping_position=cp,
            eligible_tier_ceiling=ceiling.value,
            target_campaign_tier=target_campaign_tier,
            gate_verdict=verdict.value,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
