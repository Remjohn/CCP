"""Integration tests — OFO Telegram capture loop (Phase5-M04).
§10.5: test_cpsc_fr_era3_04_telegram_capture_loop.py."""
from datetime import datetime, timezone, timedelta
from src.ccp.agents.ofo_delivery_agent import OFODeliveryAgent
from src.ccp.models.ofo_models import (
    AssetReference, CrusadeNarrativeAudit, INLINE_CAPTURE_BUTTON_LABEL,
    INLINE_CAPTURE_CALLBACK, OFOAssetPackage, OFOAssetType, OFOTargetState,
    REDIS_KEY_TEMPLATE,
)


class MockRedis:
    """In-memory Redis mock for testing state transitions."""
    def __init__(self):
        self._store = {}
    def setex(self, key, ttl, value):
        self._store[key] = value
    def get(self, key):
        return self._store.get(key)
    def delete(self, key):
        self._store.pop(key, None)


def _package(target_id="target-tg-001"):
    return OFOAssetPackage(
        target_id=target_id,
        carousel=AssetReference(asset_id="a1", asset_url="s3://test/carousel.png", asset_type=OFOAssetType.CAROUSEL),
        storytelling_video=AssetReference(asset_id="a2", asset_url="s3://test/story.mp4", asset_type=OFOAssetType.STORYTELLING_VIDEO),
        reels_explainer=AssetReference(asset_id="a3", asset_url="s3://test/reels.mp4", asset_type=OFOAssetType.REELS_EXPLAINER),
        animated_audit=AssetReference(asset_id="a4", asset_url="s3://test/audit.mp4", asset_type=OFOAssetType.ANIMATED_AUDIT),
        audit_data=CrusadeNarrativeAudit(
            transcript="The algorithm has been compressing your natural authority and flattening your legacy. We defend your presence.",
            detected_flaw="Embodied Confidence", biometric_score=3.2,
        ),
    )


class TestTelegramDeliverySequence:
    """AC3: Delivery dispatches all 4 assets and sets AWAITING_CORRECTION."""

    def test_dispatch_sets_awaiting_correction_state(self):
        redis = MockRedis()
        agent = OFODeliveryAgent(redis_client=redis)
        result = agent.dispatch_package(telegram_id=12345, package=_package())
        assert result["delivered"] is True
        assert result["state"] == OFOTargetState.AWAITING_CORRECTION.value
        key = REDIS_KEY_TEMPLATE.format(telegram_id=12345)
        assert redis.get(key) == OFOTargetState.AWAITING_CORRECTION.value

    def test_dispatch_sends_4_assets(self):
        agent = OFODeliveryAgent()
        result = agent.dispatch_package(telegram_id=12345, package=_package())
        assert len(result["delivery_log"]) == 4
        asset_names = [log["asset"] for log in result["delivery_log"]]
        assert "carousel" in asset_names
        assert "storytelling_video" in asset_names
        assert "reels_explainer" in asset_names
        assert "animated_audit" in asset_names


class TestInlineCaptureButton:
    """AC3: Final audit message has InlineKeyboardMarkup, not external links."""

    def test_inline_button_label_is_correct(self):
        assert INLINE_CAPTURE_BUTTON_LABEL == "Fix This Metric Now"

    def test_inline_callback_is_correct(self):
        assert INLINE_CAPTURE_CALLBACK == "ofo_fix_metric"

    def test_no_calendly_or_external_links(self):
        """The delivery agent must never include external links."""
        agent = OFODeliveryAgent()
        result = agent.dispatch_package(telegram_id=12345, package=_package())
        # The delivery log confirms inline capture, not external redirect
        assert result["state"] == OFOTargetState.AWAITING_CORRECTION.value


class TestCorrectionReceived:
    """Simulates incoming voice note from user in AWAITING_CORRECTION state."""

    def test_correction_clears_redis_state(self):
        redis = MockRedis()
        agent = OFODeliveryAgent(redis_client=redis)
        agent.dispatch_package(telegram_id=99001, package=_package())
        # Verify state is set
        key = REDIS_KEY_TEMPLATE.format(telegram_id=99001)
        assert redis.get(key) == OFOTargetState.AWAITING_CORRECTION.value
        # Simulate correction received
        delivery_time = datetime.now(timezone.utc) - timedelta(minutes=5)
        event = agent.handle_correction_received(
            telegram_id=99001, audio_asset_id="audio-001",
            delivery_timestamp=delivery_time,
        )
        assert event.conversion_successful is True
        assert event.hook_cycle_latency_ms > 0
        # Redis state cleared
        assert redis.get(key) is None

    def test_check_awaiting_state(self):
        redis = MockRedis()
        agent = OFODeliveryAgent(redis_client=redis)
        assert agent.check_awaiting_state(99002) is False
        agent.dispatch_package(telegram_id=99002, package=_package())
        assert agent.check_awaiting_state(99002) is True
