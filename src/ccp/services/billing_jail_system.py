from __future__ import annotations
from typing import Any
from src.ccp.models.billing_models import ALACARTE_VIDEO_PRICE_CENTS, BillingStatus, REDIS_KEY_STATUS


class InstantUsageLock:
    """Instant Usage Lock: The $9.99 à la carte video charge is locked the moment
    the rendering pipeline successfully initiates, preventing cancel-before-delivery exploits."""

    def __init__(self, supabase_client: Any = None) -> None:
        self._supabase = supabase_client

    async def lock_usage(self, coach_id: str, action: str) -> None:
        if self._supabase is not None:
            from uuid import uuid4
            from datetime import datetime, timezone
            self._supabase.table("billing_events").insert({"id": str(uuid4()), "coach_id": coach_id, "event_type": "alacarte_video", "amount_cents": ALACARTE_VIDEO_PRICE_CENTS, "description": f"Instant usage lock for {action}", "created_at": datetime.now(timezone.utc).isoformat()}).execute()


class GracePeriodMuter:
    """Grace Period Mute: On payment failure, bots stop sending messages.
    AFFiNE workspace enters read-only. Data is preserved, never deleted."""

    def __init__(self, redis_client: Any = None, supabase_client: Any = None) -> None:
        self._redis = redis_client
        self._supabase = supabase_client

    async def mute_coach(self, coach_id: str) -> None:
        if self._redis is not None:
            await self._redis.set(REDIS_KEY_STATUS.format(coach_id=coach_id), BillingStatus.PAST_DUE.value)
        if self._supabase is not None:
            from datetime import datetime, timezone
            self._supabase.table("coach_subscriptions").update({"status": BillingStatus.PAST_DUE.value, "updated_at": datetime.now(timezone.utc).isoformat()}).eq("coach_id", coach_id).execute()

    async def unmute_coach(self, coach_id: str) -> None:
        if self._redis is not None:
            await self._redis.set(REDIS_KEY_STATUS.format(coach_id=coach_id), BillingStatus.ACTIVE.value)
        if self._supabase is not None:
            from datetime import datetime, timezone
            self._supabase.table("coach_subscriptions").update({"status": BillingStatus.ACTIVE.value, "updated_at": datetime.now(timezone.utc).isoformat()}).eq("coach_id", coach_id).execute()


class WatermarkEnforcer:
    """Watermark Enforcement: For $0 Proof Layer, require_credits middleware
    injects requires_watermark: true into CCFRoutingRecommendation payload.
    Removed upon upgrade to Speaking & Learning or higher."""

    def __init__(self, redis_client: Any = None) -> None:
        self._redis = redis_client

    async def should_watermark(self, coach_id: str) -> bool:
        if self._redis is not None:
            tier = await self._redis.get(f"coach:{coach_id}:tier")
            return tier == "proof_layer" or tier is None
        return True

    def inject_watermark_flag(self, routing_payload: dict, requires_watermark: bool) -> dict:
        routing_payload["requires_watermark"] = requires_watermark
        return routing_payload
