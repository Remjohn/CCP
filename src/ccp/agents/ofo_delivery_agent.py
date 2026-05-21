"""OFO Delivery Agent — FR-ERA3-04 / DEP-OFO-003.
Telegram delivery of 4-Asset Proof Package with InlineKeyboardMarkup and Redis state lock."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
from src.ccp.models.ofo_models import (
    INLINE_CAPTURE_BUTTON_LABEL, INLINE_CAPTURE_CALLBACK,
    OFOAssetPackage, OFOConversionEvent, OFOTargetState,
    REDIS_KEY_TEMPLATE, REDIS_STATE_TTL_SECONDS,
)


class OFODeliveryAgent:
    """Telegram delivery agent for the 4-Asset Proof Package (DEP-OFO-003).

    Phase5-M04 enforcement: Final message contains InlineKeyboardMarkup button.
    No external links, no Calendly, no browser redirection.
    """

    def __init__(self, *, bot: Any = None, redis_client: Any = None,
                 receipt_chain: Any = None) -> None:
        self._bot = bot
        self._redis = redis_client
        self._receipt = receipt_chain

    def dispatch_package(self, *, telegram_id: int, package: OFOAssetPackage) -> dict:
        """Send the 4-Asset Package via Telegram in strict chronological order (§4 Phase 4 Step 13).

        Sequence: Carousel (media group) → Storytelling Video → Reels Explainer → Animated Audit (with inline button).
        """
        delivery_log = []

        # Step 1: Send Carousel as media group
        carousel_result = self._send_media(
            telegram_id=telegram_id, asset_url=package.carousel.asset_url,
            caption="Your personalized visual analysis", media_type="photo",
        )
        delivery_log.append({"asset": "carousel", "sent": carousel_result})

        # Step 2: Send Storytelling Video
        story_result = self._send_media(
            telegram_id=telegram_id, asset_url=package.storytelling_video.asset_url,
            caption="The story behind your coaching authority", media_type="video",
        )
        delivery_log.append({"asset": "storytelling_video", "sent": story_result})

        # Step 3: Send Reels Explainer
        reels_result = self._send_media(
            telegram_id=telegram_id, asset_url=package.reels_explainer.asset_url,
            caption="60-second deep dive into your metrics", media_type="video",
        )
        delivery_log.append({"asset": "reels_explainer", "sent": reels_result})

        # Step 4: Send Animated Audit with InlineKeyboardMarkup (Phase5-M04)
        audit_result = self._send_audit_with_inline_button(
            telegram_id=telegram_id, package=package,
        )
        delivery_log.append({"asset": "animated_audit", "sent": audit_result})

        # Step 5: Set Redis state lock (§4 Phase 4 Step 15)
        self._set_awaiting_correction(telegram_id=telegram_id)

        if self._receipt:
            self._receipt.log(action="ofo-package-delivered", metadata={
                "target_id": package.target_id, "telegram_id": telegram_id,
                "assets_sent": len(delivery_log),
            })

        return {
            "delivered": True, "telegram_id": telegram_id,
            "target_id": package.target_id, "delivery_log": delivery_log,
            "state": OFOTargetState.AWAITING_CORRECTION.value,
        }

    def _send_media(self, *, telegram_id: int, asset_url: str, caption: str, media_type: str) -> bool:
        """Send a single media asset via Telegram Bot API."""
        if self._bot:
            try:
                if media_type == "photo":
                    self._bot.send_photo(chat_id=telegram_id, photo=asset_url, caption=caption)
                else:
                    self._bot.send_video(chat_id=telegram_id, video=asset_url, caption=caption)
                return True
            except Exception:
                return False
        return True  # Simulated success when no bot configured

    def _send_audit_with_inline_button(self, *, telegram_id: int, package: OFOAssetPackage) -> bool:
        """Send the Animated Audit with InlineKeyboardMarkup (Phase5-M04).

        The button label is 'Fix This Metric Now' — NO external links, NO Calendly.
        Tapping invokes recording state machine within active Telegram context.
        """
        audit_caption = (
            f"🎯 Your Animated Video Audit\n\n"
            f"Detected: {package.audit_data.detected_flaw}\n"
            f"Score: {package.audit_data.biometric_score}/10\n\n"
            f"The algorithm has been flattening your authority. "
            f"Tap the button below to record a 60-second correction directly here."
        )
        inline_keyboard = {
            "inline_keyboard": [[{
                "text": INLINE_CAPTURE_BUTTON_LABEL,
                "callback_data": INLINE_CAPTURE_CALLBACK,
            }]]
        }
        if self._bot:
            try:
                self._bot.send_video(
                    chat_id=telegram_id, video=package.animated_audit.asset_url,
                    caption=audit_caption, reply_markup=inline_keyboard,
                )
                return True
            except Exception:
                return False
        return True

    def _set_awaiting_correction(self, *, telegram_id: int) -> None:
        """Write AWAITING_CORRECTION state to Redis with 15-minute TTL (§4 Phase 4 Step 15)."""
        key = REDIS_KEY_TEMPLATE.format(telegram_id=telegram_id)
        if self._redis:
            self._redis.setex(key, REDIS_STATE_TTL_SECONDS, OFOTargetState.AWAITING_CORRECTION.value)

    def handle_correction_received(self, *, telegram_id: int, audio_asset_id: str,
                                   delivery_timestamp: datetime) -> OFOConversionEvent:
        """Process incoming audio correction from peer in AWAITING_CORRECTION state."""
        now = datetime.now(timezone.utc)
        latency_ms = int((now - delivery_timestamp).total_seconds() * 1000)

        # Clear Redis state
        key = REDIS_KEY_TEMPLATE.format(telegram_id=telegram_id)
        if self._redis:
            self._redis.delete(key)

        event = OFOConversionEvent(
            target_id=str(telegram_id), telegram_session_id=f"tg-{telegram_id}",
            audio_correction_asset_id=audio_asset_id,
            hook_cycle_latency_ms=latency_ms, conversion_successful=True,
        )

        if self._receipt:
            self._receipt.log(action="ofo-correction-received", metadata={
                "telegram_id": telegram_id, "latency_ms": latency_ms,
                "audio_asset_id": audio_asset_id,
            })

        return event

    def check_awaiting_state(self, telegram_id: int) -> bool:
        """Check if a user is in AWAITING_CORRECTION state."""
        key = REDIS_KEY_TEMPLATE.format(telegram_id=telegram_id)
        if self._redis:
            val = self._redis.get(key)
            return val == OFOTargetState.AWAITING_CORRECTION.value if val else False
        return False
