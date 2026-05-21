from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from src.ccp.models.cpsc_models import PaymentTier, RewardDispatchResult

TIER_REWARD_ASSETS: dict[str, dict[str, str]] = {
    "SPEAKING_LEARNING": {
        "asset_type": "video",
        "asset_url": "visual-assets/rewards/speaking_learning_welcome.mp4",
    },
    "COACH_OS": {
        "asset_type": "video",
        "asset_url": "visual-assets/rewards/coach_os_welcome.mp4",
    },
}

FALLBACK_IMAGE_URL = "visual-assets/rewards/branded_congratulations.jpg"


class PaymentRewardDispatcher:
    """Pushes pre-rendered experiential reward via Telegram Bot API sendVideo/sendAudio.
    Assets are pre-built and stored in the visual-assets Supabase bucket —
    NOT generated at payment time. Enforces Phase1-M07 Payment Masking Rule."""

    def __init__(
        self,
        bot_token: str = "",
        receipt_chain: Any = None,
    ) -> None:
        self._bot_token = bot_token
        self._receipt_chain = receipt_chain

    async def push_reward(
        self,
        chat_id: int,
        tier: PaymentTier,
    ) -> RewardDispatchResult:
        """Send a pre-rendered reward asset via Telegram Bot API.
        Falls back to branded image if the video/audio asset is missing."""
        reward_config = TIER_REWARD_ASSETS.get(tier.value, TIER_REWARD_ASSETS["SPEAKING_LEARNING"])
        asset_type = reward_config["asset_type"]
        asset_url = reward_config["asset_url"]

        telegram_message_id = 0

        if self._bot_token:
            import httpx

            try:
                if asset_type == "video":
                    url = f"https://api.telegram.org/bot{self._bot_token}/sendVideo"
                    send_data = {"chat_id": chat_id, "video": asset_url}
                else:
                    url = f"https://api.telegram.org/bot{self._bot_token}/sendAudio"
                    send_data = {"chat_id": chat_id, "audio": asset_url}

                async with httpx.AsyncClient() as client:
                    response = await client.post(url, json=send_data)
                    response.raise_for_status()
                    result = response.json()
                    telegram_message_id = result.get("result", {}).get("message_id", 0)
            except Exception:
                # Fallback: send branded congratulations image instead
                try:
                    fallback_url = f"https://api.telegram.org/bot{self._bot_token}/sendPhoto"
                    async with httpx.AsyncClient() as client:
                        await client.post(fallback_url, json={
                            "chat_id": chat_id,
                            "photo": FALLBACK_IMAGE_URL,
                            "caption": "Congratulations! Your upgrade is confirmed. Welcome to your new tier.",
                        })
                    asset_type = "image"
                    asset_url = FALLBACK_IMAGE_URL
                except Exception:
                    pass

                if self._receipt_chain is not None:
                    self._receipt_chain.log(action="reward-asset-fallback", metadata={
                        "chat_id": chat_id,
                        "tier": tier.value,
                    })

        dispatch_result = RewardDispatchResult(
            dispatch_id=str(uuid4()),
            chat_id=chat_id,
            tier=tier.value,
            asset_type=asset_type,
            asset_url=asset_url,
            telegram_message_id=telegram_message_id,
            dispatched_at=datetime.now(timezone.utc).isoformat(),
        )

        if self._receipt_chain is not None:
            self._receipt_chain.log(action="reward-dispatched", metadata={
                "dispatch_id": dispatch_result.dispatch_id,
                "chat_id": chat_id,
                "tier": tier.value,
                "asset_type": asset_type,
            })

        return dispatch_result
