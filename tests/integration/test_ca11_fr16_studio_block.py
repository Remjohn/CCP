"""FR-CA11-16 — CCP Studio Block (Recording & Streaming) — Integration Tests.

Covers all 10 Acceptance Criteria:
  AC1:  Plugin Registration (/studio command → Studio Block renders)
  AC2:  Webcam Recording (YouTube mode, 1080p → valid video config)
  AC3:  Shorts Aspect Ratio (1080×1920 9:16, 720p disabled)
  AC4:  Teleprompter Scroll (500 words at 2.5 w/s → ~200s ±10%)
  AC5:  Asset Overlay (click toggle on/off)
  AC6:  S3 Upload (session status transitions)
  AC7:  CMF Trigger (mode → template mapping)
  AC8:  Streaming (WebSocket + RTMP config)
  AC9:  Crash Recovery (≥60s recoverable from IndexedDB chunks)
  AC10: Receipt Chain (FR47 DEP-ENG-041 integrity)

DEP-IDs produced: DEP-ENG-087 through DEP-ENG-093
DEP-IDs consumed: DEP-ENG-041 (Receipt Chain Guard)
"""
from __future__ import annotations

import asyncio
import uuid

import pytest

from src.ccp.models.ca11_models import (
    CRASH_RECOVERY_MIN_SECONDS,
    CMF_TEMPLATE_MAP,
    DEFAULT_FRAMERATE,
    INDEXEDDB_CHUNK_INTERVAL_SECONDS,
    QUALITY_TIERS,
    STUDIO_AGENT_NAME,
    TELEPROMPTER_DEFAULT_SPEED_WPS,
    TELEPROMPTER_FONT_SIZES,
    TELEPROMPTER_SPEED_MAX_WPS,
    TELEPROMPTER_SPEED_MIN_WPS,
    AssetPanelEntry,
    AssetType,
    CrashRecoveryResult,
    IndexedDBChunk,
    RecordingMode,
    RecordingQualityConfig,
    StudioAspectRatio,
    StudioBlockError,
    StudioBlockRegistration,
    StudioBlockResult,
    StudioResolution,
    StudioSessionRecord,
    StudioSessionStatus,
    StreamConfig,
    StreamDestination,
    StreamHealthMetrics,
    TeleprompterConfig,
    TeleprompterScrollResult,
)
from src.ccp.services.studio_block_service import (
    STUDIO_SESSIONS_SQL,
    StudioBlockService,
    build_stream_config,
    calculate_teleprompter_scroll,
    compute_crash_recovery,
    extract_text_blocks,
    register_studio_plugin,
    resolve_cmf_template,
    resolve_quality_config,
    scan_block_tree,
    toggle_asset_overlay,
    validate_indexeddb_chunk,
    validate_teleprompter_config,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

COACH_ID = "coach-diego-001"


def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# ===================================================================
# AC1 — Plugin Registration (DEP-ENG-087)  [5 tests]
# ===================================================================


class TestPluginRegistration:
    def test_register_command(self):
        reg = register_studio_plugin()
        assert reg.command == "/studio"

    def test_block_type(self):
        reg = register_studio_plugin()
        assert reg.block_type == "ccp-studio-block"

    def test_five_panels(self):
        reg = register_studio_plugin()
        assert len(reg.panels) == 5
        assert "preview" in reg.panels
        assert "controls" in reg.panels
        assert "teleprompter" in reg.panels
        assert "assets" in reg.panels
        assert "soundboard" in reg.panels

    def test_five_recording_modes(self):
        reg = register_studio_plugin()
        assert len(reg.recording_modes) == 5
        for mode in RecordingMode:
            assert mode.value in reg.recording_modes

    def test_service_register(self):
        svc = StudioBlockService()
        reg = svc.register()
        assert isinstance(reg, StudioBlockRegistration)
        assert reg.command == "/studio"


# ===================================================================
# AC2 — Webcam Recording Config (DEP-ENG-088)  [6 tests]
# ===================================================================


class TestRecordingConfig:
    def test_youtube_1080p(self):
        config = resolve_quality_config(RecordingMode.YOUTUBE_LONGFORM.value)
        assert config.resolution == StudioResolution.HD_1080.value
        assert config.aspect_ratio == StudioAspectRatio.LANDSCAPE_16_9.value
        assert config.width == 1920
        assert config.height == 1080
        assert config.video_bitrate_bps == 8_000_000

    def test_youtube_720p(self):
        config = resolve_quality_config(
            RecordingMode.YOUTUBE_LONGFORM.value,
            StudioResolution.HD_720.value,
        )
        assert config.resolution == StudioResolution.HD_720.value
        assert config.width == 1280
        assert config.height == 720

    def test_webinar_default_1080p(self):
        config = resolve_quality_config(RecordingMode.WEBINAR_VOD.value)
        assert config.resolution == StudioResolution.HD_1080.value
        assert config.video_bitrate_bps == 6_000_000

    def test_course_video(self):
        config = resolve_quality_config(RecordingMode.COURSE_VIDEO.value)
        assert config.width == 1920
        assert config.height == 1080

    def test_loom_quick_720p_only(self):
        config = resolve_quality_config(RecordingMode.LOOM_QUICK.value)
        assert config.resolution == StudioResolution.HD_720.value
        assert config.width == 1280
        assert config.height == 720
        assert config.video_bitrate_bps == 3_000_000

    def test_framerate_default_30(self):
        config = resolve_quality_config(RecordingMode.YOUTUBE_LONGFORM.value)
        assert config.framerate == DEFAULT_FRAMERATE == 30

    def test_invalid_mode_raises(self):
        with pytest.raises(ValueError, match=StudioBlockError.INVALID_MODE_RESOLUTION.value):
            resolve_quality_config("invalid_mode")

    def test_invalid_resolution_for_mode(self):
        with pytest.raises(ValueError, match=StudioBlockError.INVALID_MODE_RESOLUTION.value):
            resolve_quality_config(RecordingMode.LOOM_QUICK.value, StudioResolution.HD_1080.value)


# ===================================================================
# AC3 — Shorts Aspect Ratio (9:16, 720p disabled)  [4 tests]
# ===================================================================


class TestShortsAspectRatio:
    def test_shorts_1080p_portrait(self):
        config = resolve_quality_config(RecordingMode.SHORT_FORM_VERTICAL.value)
        assert config.aspect_ratio == StudioAspectRatio.PORTRAIT_9_16.value
        assert config.width == 1080
        assert config.height == 1920
        assert config.resolution == StudioResolution.HD_1080.value

    def test_shorts_720p_disabled(self):
        with pytest.raises(ValueError, match="720p is disabled"):
            resolve_quality_config(
                RecordingMode.SHORT_FORM_VERTICAL.value,
                StudioResolution.HD_720.value,
            )

    def test_shorts_only_one_selectable_resolution(self):
        tier = QUALITY_TIERS[RecordingMode.SHORT_FORM_VERTICAL.value]
        assert len(tier["selectable_resolutions"]) == 1
        assert tier["selectable_resolutions"][0] == StudioResolution.HD_1080.value

    def test_shorts_bitrate(self):
        config = resolve_quality_config(RecordingMode.SHORT_FORM_VERTICAL.value)
        assert config.video_bitrate_bps == 8_000_000


# ===================================================================
# AC4 — Teleprompter Scroll (500 words at 2.5 w/s → ~200s ±10%)  [7 tests]
# ===================================================================


class TestTeleprompterScroll:
    def test_500_words_at_2_5_wps(self):
        """AC4: 500 words at 2.5 w/s → ~200 seconds (±10%)."""
        result = calculate_teleprompter_scroll(500, 2.5)
        assert result.word_count == 500
        assert result.speed_wps == 2.5
        # Expected 200.0 seconds, ±10% means 180–220
        assert 180.0 <= result.scroll_duration_seconds <= 220.0
        # Exact: 200.0
        assert result.scroll_duration_seconds == 200.0

    def test_1000_words_at_max_speed(self):
        result = calculate_teleprompter_scroll(1000, TELEPROMPTER_SPEED_MAX_WPS)
        assert result.speed_wps == TELEPROMPTER_SPEED_MAX_WPS
        assert result.scroll_duration_seconds == 200.0  # 1000 / 5.0

    def test_zero_words(self):
        result = calculate_teleprompter_scroll(0, 2.5)
        assert result.scroll_duration_seconds == 0.0

    def test_clamp_below_min_speed(self):
        result = calculate_teleprompter_scroll(100, 0.1)
        assert result.speed_wps == TELEPROMPTER_SPEED_MIN_WPS - 0.0
        assert result.scroll_duration_seconds == 100.0  # 100 / 1.0

    def test_clamp_above_max_speed(self):
        result = calculate_teleprompter_scroll(100, 99.9)
        assert result.speed_wps == TELEPROMPTER_SPEED_MAX_WPS
        assert result.scroll_duration_seconds == 20.0  # 100 / 5.0

    def test_default_speed(self):
        result = calculate_teleprompter_scroll(250)
        assert result.speed_wps == TELEPROMPTER_DEFAULT_SPEED_WPS
        assert result.scroll_duration_seconds == 100.0  # 250 / 2.5

    def test_validate_config_valid(self):
        cfg = TeleprompterConfig(speed_wps=2.5, font_size_px=24)
        assert validate_teleprompter_config(cfg) is True

    def test_validate_config_invalid_font(self):
        cfg = TeleprompterConfig(speed_wps=2.5, font_size_px=99)
        assert validate_teleprompter_config(cfg) is False


class TestTextExtraction:
    def test_extract_text_blocks(self):
        blocks = [
            {"type": "paragraph", "content": "Hello world"},
            {"type": "image", "url": "s3://some.png"},
            {"type": "heading", "content": "Title"},
            {"type": "list", "content": "Item one"},
        ]
        text = extract_text_blocks(blocks)
        assert "Hello world" in text
        assert "Title" in text
        assert "Item one" in text
        assert "s3://" not in text

    def test_extract_empty_blocks(self):
        assert extract_text_blocks([]) == ""

    def test_extract_skips_image_blocks(self):
        blocks = [
            {"type": "image", "url": "s3://photo.jpg"},
            {"type": "excalidraw", "data": "{}"},
        ]
        assert extract_text_blocks(blocks) == ""


# ===================================================================
# AC5 — Asset Overlay Toggle (DEP-ENG-090)  [5 tests]
# ===================================================================


class TestAssetPanel:
    def test_scan_block_tree_images(self):
        blocks = [
            {"type": "image", "id": "img-1", "url": "s3://photo.jpg"},
            {"type": "paragraph", "id": "p-1", "content": "text"},
        ]
        assets = scan_block_tree(blocks)
        assert len(assets) == 1
        assert assets[0].asset_type == AssetType.IMAGE.value
        assert assets[0].source_block_id == "img-1"

    def test_scan_excalidraw(self):
        blocks = [{"type": "excalidraw", "id": "exc-1", "thumbnail_url": "s3://thumb.png"}]
        assets = scan_block_tree(blocks)
        assert len(assets) == 1
        assert assets[0].asset_type == AssetType.EXCALIDRAW.value

    def test_scan_canva(self):
        blocks = [{"type": "canva", "id": "c-1"}]
        assets = scan_block_tree(blocks)
        assert len(assets) == 1
        assert assets[0].asset_type == AssetType.CANVA.value

    def test_toggle_overlay_on(self):
        asset = AssetPanelEntry(
            asset_type="image", source_block_id="b-1", is_overlay_active=False,
        )
        toggled = toggle_asset_overlay(asset)
        assert toggled.is_overlay_active is True

    def test_toggle_overlay_off(self):
        asset = AssetPanelEntry(
            asset_type="image", source_block_id="b-1", is_overlay_active=True,
        )
        toggled = toggle_asset_overlay(asset)
        assert toggled.is_overlay_active is False


# ===================================================================
# AC6 — S3 Upload + Session Status (DEP-ENG-091)  [4 tests]
# ===================================================================


class TestSessionLifecycle:
    def test_create_session_success(self):
        svc = StudioBlockService()
        result = _run(svc.create_session(
            coach_id=COACH_ID,
            recording_mode=RecordingMode.YOUTUBE_LONGFORM.value,
        ))
        assert result.success is True
        assert result.session is not None
        assert result.session.status == StudioSessionStatus.RECORDING.value
        assert result.session.coach_id == COACH_ID

    def test_create_session_shorts(self):
        svc = StudioBlockService()
        result = _run(svc.create_session(
            coach_id=COACH_ID,
            recording_mode=RecordingMode.SHORT_FORM_VERTICAL.value,
        ))
        assert result.success is True
        assert result.session.aspect_ratio == StudioAspectRatio.PORTRAIT_9_16.value

    def test_create_session_invalid_mode(self):
        svc = StudioBlockService()
        result = _run(svc.create_session(
            coach_id=COACH_ID,
            recording_mode="invalid",
        ))
        assert result.success is False
        assert StudioBlockError.INVALID_MODE_RESOLUTION.value in result.error

    def test_upload_complete_transitions_to_processing(self):
        svc = StudioBlockService()
        result = _run(svc.complete_upload(
            session_id=str(uuid.uuid4()),
            s3_url="s3://bucket/recording.webm",
            recording_mode=RecordingMode.YOUTUBE_LONGFORM.value,
            coach_id=COACH_ID,
            source_page_id="page-001",
            duration=300,
        ))
        assert result.success is True
        assert result.session.status == StudioSessionStatus.PROCESSING.value
        assert result.session.s3_recording_url == "s3://bucket/recording.webm"
        assert result.session.duration_seconds == 300


# ===================================================================
# AC7 — CMF Trigger (mode → template mapping)  [6 tests]
# ===================================================================


class TestCMFTrigger:
    def test_youtube_longform_template(self):
        assert resolve_cmf_template(RecordingMode.YOUTUBE_LONGFORM.value) == "youtube_longform"

    def test_short_form_template(self):
        assert resolve_cmf_template(RecordingMode.SHORT_FORM_VERTICAL.value) == "short_form_vertical"

    def test_webinar_template(self):
        assert resolve_cmf_template(RecordingMode.WEBINAR_VOD.value) == "webinar_vod"

    def test_course_template(self):
        assert resolve_cmf_template(RecordingMode.COURSE_VIDEO.value) == "course_video"

    def test_loom_template(self):
        assert resolve_cmf_template(RecordingMode.LOOM_QUICK.value) == "loom_quick"

    def test_invalid_mode_raises(self):
        with pytest.raises(ValueError, match=StudioBlockError.CMF_TRIGGER_FAILED.value):
            resolve_cmf_template("nonexistent_mode")

    def test_cmf_applied_on_upload_complete(self):
        svc = StudioBlockService()
        result = _run(svc.complete_upload(
            session_id=str(uuid.uuid4()),
            s3_url="s3://bucket/video.webm",
            recording_mode=RecordingMode.WEBINAR_VOD.value,
            coach_id=COACH_ID,
            source_page_id=None,
            duration=600,
        ))
        assert result.session.cmf_pipeline_template == "webinar_vod"
        assert result.session.cmf_job_id is not None


# ===================================================================
# AC8 — Streaming (WebSocket + RTMP) (DEP-ENG-093)  [5 tests]
# ===================================================================


class TestStreaming:
    def test_build_stream_config(self):
        dest = StreamDestination(
            platform="youtube_live",
            rtmp_url="rtmp://a.rtmp.youtube.com/live2",
            stream_key="key-123",
        )
        config = build_stream_config("sess-001", [dest])
        assert config.session_id == "sess-001"
        assert "ws/stream/sess-001" in config.websocket_url
        assert len(config.destinations) == 1
        assert config.parallel_s3_archive is True

    def test_stream_health_defaults(self):
        config = build_stream_config("s1", [])
        assert config.health.connection_status == "connecting"
        assert config.health.bitrate_kbps == 0.0

    def test_start_stream_session(self):
        svc = StudioBlockService()
        dest = StreamDestination(
            platform="youtube_live",
            rtmp_url="rtmp://a.rtmp.youtube.com/live2",
            stream_key="key-abc",
        )
        result = _run(svc.start_stream(
            session_id="sess-stream-001",
            coach_id=COACH_ID,
            recording_mode=RecordingMode.WEBINAR_VOD.value,
            destinations=[dest],
        ))
        assert result.success is True
        assert result.session.is_stream is True
        assert result.session.status == StudioSessionStatus.STREAMING.value
        assert len(result.session.stream_destinations) == 1

    def test_multiple_destinations(self):
        dests = [
            StreamDestination(platform="youtube_live", rtmp_url="rtmp://yt.com/live"),
            StreamDestination(platform="facebook_live", rtmp_url="rtmp://fb.com/live"),
        ]
        config = build_stream_config("sess-multi", dests)
        assert len(config.destinations) == 2

    def test_custom_stream_service_url(self):
        config = build_stream_config(
            "s1", [], service_base_url="wss://custom.stream.io",
        )
        assert config.websocket_url == "wss://custom.stream.io/ws/stream/s1"


# ===================================================================
# AC9 — Crash Recovery (≥60s from IndexedDB chunks)  [6 tests]
# ===================================================================


class TestCrashRecovery:
    @staticmethod
    def _make_chunks(session_id: str, count: int) -> list[IndexedDBChunk]:
        return [
            IndexedDBChunk(
                session_id=session_id,
                sequence_number=i,
                blob_size_bytes=500_000,
                duration_seconds=INDEXEDDB_CHUNK_INTERVAL_SECONDS,
            )
            for i in range(count)
        ]

    def test_120s_recording_recoverable(self):
        """AC9: 2-minute recording → ≥60s must be recoverable."""
        # 2 minutes = 120s / 5s per chunk = 24 chunks
        chunks = self._make_chunks("sess-crash-1", 24)
        result = compute_crash_recovery(chunks)
        assert result.is_recoverable is True
        assert result.total_duration_seconds == 120.0
        assert result.chunks_recovered == 24

    def test_exactly_60s_recoverable(self):
        chunks = self._make_chunks("sess-min", 12)  # 12 × 5s = 60s
        result = compute_crash_recovery(chunks)
        assert result.is_recoverable is True
        assert result.total_duration_seconds == 60.0

    def test_below_60s_not_recoverable(self):
        chunks = self._make_chunks("sess-short", 11)  # 55s
        result = compute_crash_recovery(chunks)
        assert result.is_recoverable is False
        assert result.total_duration_seconds == 55.0

    def test_empty_chunks_not_recoverable(self):
        result = compute_crash_recovery([])
        assert result.is_recoverable is False
        assert result.chunks_recovered == 0

    def test_chunks_sorted_by_sequence(self):
        chunks = [
            IndexedDBChunk(session_id="s1", sequence_number=3, blob_size_bytes=100),
            IndexedDBChunk(session_id="s1", sequence_number=1, blob_size_bytes=100),
            IndexedDBChunk(session_id="s1", sequence_number=2, blob_size_bytes=100),
        ]
        result = compute_crash_recovery(chunks)
        assert result.chunks_recovered == 3

    def test_validate_indexeddb_chunk_valid(self):
        chunk = IndexedDBChunk(session_id="s1", sequence_number=0, blob_size_bytes=1000)
        assert validate_indexeddb_chunk(chunk) is True

    def test_validate_indexeddb_chunk_wrong_duration(self):
        chunk = IndexedDBChunk(
            session_id="s1", sequence_number=0, blob_size_bytes=1000,
            duration_seconds=3.0,
        )
        assert validate_indexeddb_chunk(chunk) is False

    def test_service_recover_from_crash(self):
        svc = StudioBlockService()
        chunks = self._make_chunks("sess-recover", 24)
        result = _run(svc.recover_from_crash("sess-recover", chunks))
        assert isinstance(result, CrashRecoveryResult)
        assert result.is_recoverable is True
        assert result.total_duration_seconds >= CRASH_RECOVERY_MIN_SECONDS


# ===================================================================
# AC10 — Receipt Chain (FR47 DEP-ENG-041)  [6 tests]
# ===================================================================


class TestReceiptChain:
    def test_session_create_emits_receipt(self):
        svc = StudioBlockService()
        _run(svc.create_session(
            coach_id=COACH_ID,
            recording_mode=RecordingMode.YOUTUBE_LONGFORM.value,
        ))
        assert len(svc.receipt_chain) == 1
        assert svc.receipt_chain[0]["stage_name"] == "session-create"
        assert svc.receipt_chain[0]["agent_name"] == STUDIO_AGENT_NAME

    def test_upload_complete_emits_two_receipts(self):
        svc = StudioBlockService()
        _run(svc.complete_upload(
            session_id=str(uuid.uuid4()),
            s3_url="s3://bucket/rec.webm",
            recording_mode=RecordingMode.YOUTUBE_LONGFORM.value,
            coach_id=COACH_ID,
            source_page_id=None,
            duration=120,
        ))
        # upload-complete + cmf-trigger = 2 receipts
        assert len(svc.receipt_chain) == 2
        assert svc.receipt_chain[0]["stage_name"] == "upload-complete"
        assert svc.receipt_chain[1]["stage_name"] == "cmf-trigger"

    def test_receipt_chain_integrity(self):
        svc = StudioBlockService()
        _run(svc.create_session(
            coach_id=COACH_ID,
            recording_mode=RecordingMode.YOUTUBE_LONGFORM.value,
        ))
        _run(svc.complete_upload(
            session_id=str(uuid.uuid4()),
            s3_url="s3://bucket/rec.webm",
            recording_mode=RecordingMode.YOUTUBE_LONGFORM.value,
            coach_id=COACH_ID,
            source_page_id=None,
            duration=120,
        ))
        # 1 (session-create) + 2 (upload-complete + cmf-trigger) = 3 receipts
        assert len(svc.receipt_chain) == 3
        assert svc.verify_receipt_chain() is True

    def test_first_receipt_has_empty_previous_hash(self):
        svc = StudioBlockService()
        _run(svc.create_session(
            coach_id=COACH_ID,
            recording_mode=RecordingMode.YOUTUBE_LONGFORM.value,
        ))
        assert svc.receipt_chain[0]["previous_receipt_hash"] == ""

    def test_streaming_session_emits_receipt(self):
        svc = StudioBlockService()
        dest = StreamDestination(
            platform="youtube_live",
            rtmp_url="rtmp://a.rtmp.youtube.com/live2",
        )
        _run(svc.start_stream(
            session_id="s1",
            coach_id=COACH_ID,
            recording_mode=RecordingMode.WEBINAR_VOD.value,
            destinations=[dest],
        ))
        assert len(svc.receipt_chain) == 1
        assert svc.receipt_chain[0]["stage_name"] == "session-create"

    def test_receipt_contains_required_fields(self):
        svc = StudioBlockService()
        _run(svc.create_session(
            coach_id=COACH_ID,
            recording_mode=RecordingMode.YOUTUBE_LONGFORM.value,
        ))
        receipt = svc.receipt_chain[0]
        assert "receipt_id" in receipt
        assert "previous_receipt_hash" in receipt
        assert "input_payload_hash" in receipt
        assert "output_payload_hash" in receipt
        assert "stage_name" in receipt
        assert "agent_name" in receipt
        assert "timestamp" in receipt


# ===================================================================
# SQL Schema & Constants  [3 tests]
# ===================================================================


class TestSQLAndConstants:
    def test_studio_sessions_sql(self):
        assert "studio_sessions" in STUDIO_SESSIONS_SQL
        assert "coach_id" in STUDIO_SESSIONS_SQL
        assert "recording_mode" in STUDIO_SESSIONS_SQL
        assert "s3_recording_url" in STUDIO_SESSIONS_SQL

    def test_quality_tiers_all_modes(self):
        for mode in RecordingMode:
            assert mode.value in QUALITY_TIERS
            tier = QUALITY_TIERS[mode.value]
            assert "aspect_ratio" in tier
            assert "default_resolution" in tier
            assert "bitrate_bps" in tier

    def test_cmf_template_map_all_modes(self):
        for mode in RecordingMode:
            assert mode.value in CMF_TEMPLATE_MAP
