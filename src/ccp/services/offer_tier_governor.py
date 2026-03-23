"""
FR58 — Offer Tier Architecture
================================
Financial and psychological routing governor: binds commercial offer
tiers to individual Information Coping Trajectories via the Tier Matrix
and the Upward-Only Routing Gate.

Classes
-------
TierCeilingResolver
    Maps an ICT coping position (1-5 / null) to an OfferTierCeiling enum.

UpwardOnlyRoutingGate
    Evaluates a target campaign tier against the computed ceiling and
    historical purchase maximum, returning an UpwardRoutingVerdict.

OfferTierGovernor
    Orchestrates both stages, assembles OfferTierGovernorRow, and writes
    receipt chain entries (DEP-ENG-041).
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

# Coping position thresholds for tier assignment (§4 Stage 1)
TIER_1_MAX_COPING: int = 3   # coping ≤ 3 → TIER_1_CHALLENGE
TIER_2_COPING: int = 4       # coping = 4 → TIER_2_CORE
TIER_3_COPING: int = 5       # coping = 5 → TIER_3_PREMIUM

# Null fallback: coping=None → TIER_1 baseline (§6 backward compat)
COPING_NULL_FALLBACK: int = 1

# Integer mappings for tier comparisons
_TIER_INT_MAP = {
    OfferTierCeiling.TIER_1_CHALLENGE: 1,
    OfferTierCeiling.TIER_2_CORE: 2,
    OfferTierCeiling.TIER_3_PREMIUM: 3,
}


# ---------------------------------------------------------------------------
# TierCeilingResolver
# ---------------------------------------------------------------------------

class TierCeilingResolver:
    """
    Maps an ICT coping_position integer to an OfferTierCeiling enum.

    Parameters
    ----------
    coping_position : int | None
        Client's Information Coping Trajectory position (1-5).
        None → fallback to COPING_NULL_FALLBACK=1 → TIER_1_CHALLENGE.
    """

    def __init__(self, coping_position: int | None) -> None:
        self._cp = coping_position if coping_position is not None else COPING_NULL_FALLBACK

    def resolve(self) -> tuple[int, OfferTierCeiling]:
        """Return ``(computed_coping_position, eligible_tier_ceiling)``."""
        cp = self._cp
        if cp >= TIER_3_COPING:
            return cp, OfferTierCeiling.TIER_3_PREMIUM
        if cp == TIER_2_COPING:
            return cp, OfferTierCeiling.TIER_2_CORE
        return cp, OfferTierCeiling.TIER_1_CHALLENGE


# ---------------------------------------------------------------------------
# UpwardOnlyRoutingGate
# ---------------------------------------------------------------------------

def _safe_tier_history_max(historical_tiers: list[Any]) -> int:
    """
    Return the maximum valid integer tier from a potentially corrupt list.

    Ignores None, NaN, negative values — defaults to 0 if all values
    are invalid (§10 Safety test: null/NaN/-1 → 0).
    """
    valid: list[int] = []
    for v in (historical_tiers or []):
        try:
            fv = float(v)
            if not math.isnan(fv) and fv >= 1:
                valid.append(int(fv))
        except (TypeError, ValueError):
            pass
    return max(valid) if valid else 0


class UpwardOnlyRoutingGate:
    """
    Enforces upward-only tier routing.

    Parameters
    ----------
    target_tier : int
        Campaign tier FR59 wants to send to the client (1, 2, or 3).
    ceiling : OfferTierCeiling
        Computed tier ceiling from TierCeilingResolver.
    historical_tiers : list
        Prior purchase tier history. Corrupt values (None, NaN, -1)
        are treated as 0 (§6 / §10).

    Gate logic (§4 Stage 2)
    -----------------------
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
    Orchestrates FR58: resolves tier ceiling, evaluates upward-only gate,
    and returns an OfferTierGovernorRow.

    Parameters
    ----------
    coach_id : str
        ADR-01 boundary key.
    receipt_chain : ReceiptChain
        Live receipt chain (DEP-ENG-041).
    """

    _AGENT_ID = "offer-tier-governor"

    def __init__(self, coach_id: str, receipt_chain: ReceiptChain) -> None:
        if not isinstance(coach_id, str) or len(coach_id) < 2:
            raise ValueError("coach_id must be a non-empty string (min 2 chars).")
        self._coach_id = coach_id
        self._rc = receipt_chain

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

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
            ICT coping position (1-5). None → TIER_1 baseline.
        target_campaign_tier : int
            Campaign tier FR59 wants to assign (1, 2, or 3).
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
        cp, ceiling = TierCeilingResolver(coping_position).resolve()

        root_receipt = self._rc.log(
            agent_id=self._AGENT_ID,
            action="tier-ceiling-resolve",
            output_summary=(
                f"coach={self._coach_id} client={client_id} "
                f"coping={cp} ceiling={ceiling.value}"
            ),
        )

        # ── Stage 2: Upward-Only Routing Gate ────────────────────────
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
