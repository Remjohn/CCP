from __future__ import annotations
from typing import Any
from src.ccp.models.billing_models import ALACARTE_VIDEO_PRICE_CENTS, TIER_MONTHLY_PRICE_CENTS, WalletDisplayPayload

TIER_DISPLAY_NAMES: dict[str, str] = {
    "proof_layer": "Proof Layer ($0)",
    "speaking_learning": "Speaking & Learning ($39.99/mo)",
    "coach_os": "Coach OS ($99.99/mo)",
    "elite": "Elite ($199.99/mo)",
}


class WalletBlockService:
    """AFFiNE Wallet Block — coach-facing billing dashboard showing current cost breakdown."""

    def __init__(self, supabase_client: Any = None) -> None:
        self._supabase = supabase_client

    async def get_wallet_display(self, coach_id: str) -> WalletDisplayPayload:
        tier = "proof_layer"
        status = "active"
        payment_method_last4 = ""
        current_period_end = ""

        if self._supabase is not None:
            result = self._supabase.table("coach_subscriptions").select("*").eq("coach_id", coach_id).execute()
            if result and hasattr(result, "data") and result.data:
                row = result.data[0]
                tier = row.get("tier", "proof_layer")
                status = row.get("status", "active")
                payment_method_last4 = row.get("payment_method_last4", "")
                current_period_end = row.get("current_period_end", "")

        monthly_base_cents = TIER_MONTHLY_PRICE_CENTS.get(tier, 0)

        # Count à la carte videos this billing period
        alacarte_video_count = 0
        if self._supabase is not None:
            video_result = self._supabase.table("billing_events").select("id").eq("coach_id", coach_id).eq("event_type", "alacarte_video").execute()
            if video_result and hasattr(video_result, "data"):
                alacarte_video_count = len(video_result.data)

        alacarte_video_total_cents = alacarte_video_count * ALACARTE_VIDEO_PRICE_CENTS
        total_monthly_cost_cents = monthly_base_cents + alacarte_video_total_cents

        return WalletDisplayPayload(
            coach_id=coach_id,
            tier=tier,
            tier_display_name=TIER_DISPLAY_NAMES.get(tier, tier),
            monthly_base_cents=monthly_base_cents,
            alacarte_video_count=alacarte_video_count,
            alacarte_video_total_cents=alacarte_video_total_cents,
            total_monthly_cost_cents=total_monthly_cost_cents,
            status=status,
            payment_method_last4=payment_method_last4,
            current_period_end=current_period_end,
        )
