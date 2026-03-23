"""
FR-CBCS-12 — Coping-Diagnostic Invitation Engine
==================================================
CommercialMatrixRouter   — position-to-tier mapping (§4 Stage 1)
CommercialMatrixGate     — price ceiling enforcement gate (§4 Stage 2)

Academic grounding:
  - Prochaska & DiClemente (1983) Readiness to Change
  - Sweller (1988) Cognitive Load Theory
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cbcs_models import (
    INVITATION_TIER_CEILINGS,
    INVITATION_TIER_MAP,
    CommercialRoutingVerdict,
    CommercialRoutingVerdictRow,
    CopingInvitationError,
    InvitationTier,
)


# ═══════════════════════════════════════════════════════════════════════
# Stage 1 — CommercialMatrixRouter (Tier Mapping)
# ═══════════════════════════════════════════════════════════════════════


class CommercialMatrixRouter:
    """
    Maps integer coping_position (1-5) to InvitationTier enum.

    Rules (§4 Stage 1 exact dictionary):
      1 → DEFICIENCY_ESCAPE_ROUTE     (ceiling $0)
      2 → ILL_INFORMED_BRIDGE         (ceiling $49)
      3 → NEEDS_INJECTION_CATALYST    (ceiling $399)
      4 → INFORMATION_HEALTH_PARTNERSHIP (ceiling $5000)
      5 → DONOR_MASTERY_PATH          (no ceiling)
    """

    def __init__(
        self,
        coach_id: str,
        receipt_chain: ReceiptChain | None = None,
    ) -> None:
        if not (2 <= len(coach_id) <= 4):
            raise ValueError(
                f"coach_id must be 2–4 characters (ADR-01). Got: {coach_id!r}"
            )
        self._coach_id = coach_id
        self._rc = receipt_chain

    def resolve_tier(self, coping_position: int) -> InvitationTier:
        """
        Resolve the InvitationTier for a given coping_position.

        Args:
            coping_position: Integer 1-5 from FR-CBCS-04 output.

        Returns:
            InvitationTier enum member.

        Raises:
            ValueError: If coping_position is outside 1-5.
        """
        if coping_position not in INVITATION_TIER_MAP:
            raise ValueError(
                f"{CopingInvitationError.INVALID_COPING_POSITION.value}: "
                f"coping_position must be 1-5. Got: {coping_position}"
            )
        tier_str = INVITATION_TIER_MAP[coping_position]
        return InvitationTier(tier_str)

    def get_price_ceiling(self, coping_position: int) -> float | None:
        """
        Return the price ceiling for a coping_position.

        Returns:
            Float ceiling (e.g. 49.0) or None for no ceiling (position 5).
        """
        if coping_position not in INVITATION_TIER_CEILINGS:
            raise ValueError(
                f"{CopingInvitationError.INVALID_COPING_POSITION.value}: "
                f"coping_position must be 1-5. Got: {coping_position}"
            )
        return INVITATION_TIER_CEILINGS[coping_position]


# ═══════════════════════════════════════════════════════════════════════
# Stage 2 — CommercialMatrixGate (Price Ceiling Enforcement)
# ═══════════════════════════════════════════════════════════════════════


class CommercialMatrixGate:
    """
    Evaluates whether a proposed product price is safe for the client's
    current coping position.

    Gate logic (§4 Stage 2 exact thresholds):
      PASS         — product_price ≤ ceiling for coping_position
      PROVISIONAL  — product_price exceeds ceiling by exactly 1 tier level
      FAIL_VIOLATION — product_price exceeds ceiling by ≥ 2 tier levels
                     → "Matrix Violation: Endangering Client Safety"
    """

    def __init__(
        self,
        coach_id: str,
        receipt_chain: ReceiptChain | None = None,
    ) -> None:
        if not (2 <= len(coach_id) <= 4):
            raise ValueError(
                f"coach_id must be 2–4 characters (ADR-01). Got: {coach_id!r}"
            )
        self._coach_id = coach_id
        self._rc = receipt_chain
        self._router = CommercialMatrixRouter(coach_id=coach_id)

    # ── Public API ────────────────────────────────────────────────────

    def evaluate(
        self,
        client_id: str,
        coping_position: int,
        target_product_price: float,
    ) -> CommercialRoutingVerdictRow:
        """
        Evaluate whether a product price is appropriate for the coping position.

        Args:
            client_id: Target client identifier.
            coping_position: Integer 1-5 from FR-CBCS-04.
            target_product_price: Proposed product price (float, ≥ 0).

        Returns:
            CommercialRoutingVerdictRow with gate_verdict and full schema.

        Raises:
            ValueError: If coping_position is invalid.
        """
        tier = self._router.resolve_tier(coping_position)
        ceiling = self._router.get_price_ceiling(coping_position)

        verdict = self._compute_verdict(
            coping_position, target_product_price, ceiling
        )

        row = CommercialRoutingVerdictRow(
            routing_id=str(uuid.uuid4()),
            client_id=client_id,
            coach_id=self._coach_id,
            computed_coping_position=coping_position,
            invitation_tier=tier.value,
            target_product_price=target_product_price,
            gate_verdict=verdict.value,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

        if self._rc is not None:
            self._rc.log(
                agent_id=self._coach_id,
                action="commercial-matrix-gate",
                asset_id=row.routing_id,
                output_summary=(
                    f"position={coping_position} tier={tier.value} "
                    f"price={target_product_price} verdict={verdict.value}"
                ),
            )

        return row

    # ── Private helpers ───────────────────────────────────────────────

    def _compute_verdict(
        self,
        coping_position: int,
        price: float,
        ceiling: float | None,
    ) -> CommercialRoutingVerdict:
        """
        Determine PASS / PROVISIONAL / FAIL_VIOLATION.

        Tier-excess logic:
          - Find how many tier levels the price exceeds.
          - 0 levels over  → PASS
          - 1 level over   → PROVISIONAL
          - ≥ 2 levels over → FAIL_VIOLATION
        """
        if ceiling is None:
            # Position 5 — no ceiling, always PASS
            return CommercialRoutingVerdict.PASS

        if price <= ceiling:
            return CommercialRoutingVerdict.PASS

        # Count how many tier levels are exceeded
        tiers_exceeded = self._count_tiers_exceeded(coping_position, price)

        if tiers_exceeded == 1:
            return CommercialRoutingVerdict.PROVISIONAL
        else:
            return CommercialRoutingVerdict.FAIL_VIOLATION

    @staticmethod
    def _count_tiers_exceeded(coping_position: int, price: float) -> int:
        """
        Count how many tier levels above the client's ceiling the price exceeds.

        Example:
          - Position 2 (ceiling $49), price $99:
            Does $99 > P3 ceiling ($399)? No → tiers_exceeded = 1 (PROVISIONAL)
          - Position 2 (ceiling $49), price $997:
            Does $997 > P3 ceiling ($399)? Yes → +1
            Does $997 > P4 ceiling ($5000)? No → stop → tiers_exceeded = 2 (FAIL)
          - Position 1 (ceiling $0), price $997:
            Does $997 > P2 ceiling ($49)? Yes → +1
            Does $997 > P3 ceiling ($399)? Yes → +1
            Does $997 > P4 ceiling ($5000)? No → stop → tiers_exceeded = 2 (FAIL)

        Returns:
            1 for PROVISIONAL, ≥2 for FAIL_VIOLATION.
        """
        # Price already exceeds client's ceiling — count how many FURTHER
        # tier ceilings it also exceeds
        further_exceeded = 0
        for pos in range(coping_position + 1, 6):
            next_ceiling = INVITATION_TIER_CEILINGS.get(pos)
            if next_ceiling is None:
                # Position 5 has no ceiling — price fits
                break
            if price > next_ceiling:
                further_exceeded += 1
            else:
                break
        # 1 + further_exceeded = total tiers exceeded
        return 1 + further_exceeded
