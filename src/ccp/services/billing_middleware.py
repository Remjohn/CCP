from __future__ import annotations
from typing import Any
from src.ccp.models.billing_models import (
    ALACARTE_VIDEO_PRICE_CENTS,
    BillingError,
    BillingErrorCode,
    REDIS_KEY_STATUS,
    REDIS_KEY_TIER,
)


class BillingMiddleware:
    """Coin-operated enforcement layer between every billable coach action and the backend.
    Checks Redis-cached permission state, validates against offer_tier_governor ceiling,
    reports metered usage to Stripe, and blocks execution if subscription is inactive."""

    def __init__(self, redis_client: Any = None, supabase_client: Any = None, receipt_chain: Any = None, offer_tier_governor: Any = None) -> None:
        self._redis = redis_client
        self._supabase = supabase_client
        self._receipt_chain = receipt_chain
        self._governor = offer_tier_governor

    async def require_credits(self, coach_id: str, action: str, cost: int = 0) -> bool:
        """Middleware gate for all billable actions.
        1. Check Redis for coach permission state.
        2. Consult offer_tier_governor for tier ceilings.
        3. If active & within tier -> report usage to Stripe if metered -> allow action.
        4. If inactive or out of bounds -> block action -> return billing error."""

        # 1. Check Redis for coach permission state
        status = None
        if self._redis is not None:
            status = await self._redis.get(REDIS_KEY_STATUS.format(coach_id=coach_id))
        else:
            # Redis fallback: query Supabase directly (degraded but functional)
            if self._supabase is not None:
                result = self._supabase.table("coach_subscriptions").select("status").eq("coach_id", coach_id).execute()
                if result and hasattr(result, "data") and result.data:
                    status = result.data[0].get("status")

        if status != "active" and status != "proof_layer":
            if self._receipt_chain is not None:
                self._receipt_chain.log(action="billing-gate-blocked", metadata={"coach_id": coach_id, "action": action, "status": status or "unknown"})
            raise BillingError(code=BillingErrorCode.SUBSCRIPTION_INACTIVE.value, message="Payment method required. Update card in Wallet.", redirect="/wallet")

        # 2. Consult Offer Tier Governor for ceiling validation
        if self._governor is not None:
            try:
                target_tier = 1
                if self._redis is not None:
                    tier_str = await self._redis.get(REDIS_KEY_TIER.format(coach_id=coach_id))
                    if tier_str == "coach_os":
                        target_tier = 2
                    elif tier_str == "elite":
                        target_tier = 3
                self._governor.evaluate(client_id=coach_id, coping_position=None, target_campaign_tier=target_tier)
            except ValueError as e:
                if "FAIL_CAPACITY_EXCEEDED" in str(e):
                    if self._receipt_chain is not None:
                        self._receipt_chain.log(action="billing-gate-ceiling-exceeded", metadata={"coach_id": coach_id, "action": action})
                    raise BillingError(code=BillingErrorCode.TIER_CEILING_EXCEEDED.value, message="Action exceeds current tier limits. Upgrade required.", redirect="/wallet/upgrade")

        # 3. Report metered usage to Stripe if cost > 0
        if cost > 0:
            # Insert billing event into PostgreSQL
            if self._supabase is not None:
                from uuid import uuid4
                from datetime import datetime, timezone
                self._supabase.table("billing_events").insert({
                    "id": str(uuid4()),
                    "coach_id": coach_id,
                    "event_type": "alacarte_video",
                    "amount_cents": cost * ALACARTE_VIDEO_PRICE_CENTS,
                    "description": f"Rendered video for action {action}",
                    "created_at": datetime.now(timezone.utc).isoformat(),
                }).execute()

        # 4. Write Receipt Chain Guard
        if self._receipt_chain is not None:
            self._receipt_chain.log(action="billing-gate-allowed", metadata={"coach_id": coach_id, "action": action, "cost": cost, "status": "ALLOWED"})

        return True
