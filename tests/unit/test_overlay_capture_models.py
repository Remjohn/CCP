import pytest
from src.ccp.models.overlay_capture_models import (
    AdaptiveResolutionProfile, CompositeCaptureMetadata, OverlayCaptureStatus,
    OverlayInteractionEvent, OverlayMediaFormat, OverlayModeConfig,
)


class TestAdaptiveResolutionProfileDefaults:
    def test_defaults_to_720p(self):
        profile = AdaptiveResolutionProfile(media_format=OverlayMediaFormat.WEBM_VP9)
        assert profile.width == 720
        assert profile.height == 1280
        assert profile.frame_rate == 30
        assert profile.device_tier == "mid"
        assert profile.resolution_downgraded is False

    def test_high_resolution_1080p(self):
        profile = AdaptiveResolutionProfile(width=1080, height=1920, media_format=OverlayMediaFormat.WEBM_VP9, device_tier="high")
        assert profile.width == 1080
        assert profile.height == 1920

    def test_low_resolution_540p(self):
        profile = AdaptiveResolutionProfile(width=540, height=960, frame_rate=24, media_format=OverlayMediaFormat.MP4_H264, device_tier="low", resolution_downgraded=True)
        assert profile.width == 540
        assert profile.frame_rate == 24
        assert profile.resolution_downgraded is True


class TestMediaFormatDetection:
    def test_webm_format(self):
        assert OverlayMediaFormat.WEBM_VP9.value == "video/webm;codecs=vp9"

    def test_mp4_format(self):
        assert OverlayMediaFormat.MP4_H264.value == "video/mp4;codecs=avc1"


class TestOverlayInteractionEventSchema:
    def test_valid_event(self):
        event = OverlayInteractionEvent(
            event_type="round_state_change", session_id="sess-001", timestamp_ms=12345,
            round_index=2, from_state="question", to_state="answer",
            overlay_elements={"letter": "A"}, capture_state={"fps": 30},
        )
        assert event.event_type == "round_state_change"
        assert event.round_index == 2

    def test_event_without_round_index(self):
        event = OverlayInteractionEvent(
            event_type="overlay_mounted", session_id="sess-001", timestamp_ms=0,
        )
        assert event.round_index is None


class TestCompositeCaptureMetadata:
    def test_pending_background_default(self):
        meta = CompositeCaptureMetadata(
            session_id="sess-001", coach_id="coach-001",
            resolution=AdaptiveResolutionProfile(media_format=OverlayMediaFormat.WEBM_VP9),
            capture_status=OverlayCaptureStatus.STOPPED,
        )
        assert meta.upload_status == "pending_background"
        assert meta.audio_track_present is True
        assert meta.video_track_present is True


class TestOverlayModeConfig:
    def test_rosco_ring_config(self):
        config = OverlayModeConfig(
            mode_key="react_alphabet", overlay_layout="rosco_ring",
            sound_pack="alphabet", camera_position="background_fill",
        )
        assert config.target_aspect_ratio == "9:16"
        assert config.requires_face_tracking is False
