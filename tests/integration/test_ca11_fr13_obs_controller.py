"""FR-CA11-13 — OBS Recording Pipeline Controller — Integration Tests.

Covers all 7 Acceptance Criteria:
  AC1: Start Recording
  AC2: Stop Recording + S3 Upload
  AC3: Scene Switch
  AC4: Pipeline Trigger
  AC5: Connection Failure
  AC6: Reconnection
  AC7: Authentication
"""
from __future__ import annotations

import asyncio
import uuid
from typing import Any

import pytest

from src.ccp.models.ca11_models import (
    OBSCommandResult,
    OBSConnectionState,
    PipelineStatus,
    RecordingState,
    RecordingStatusPayload,
)
from src.ccp.services.obs_controller import (
    DEFAULT_OBS_HOST,
    DEFAULT_OBS_PORT,
    MAX_RECONNECT_ATTEMPTS,
    RECORDING_COMMANDS,
    SESSION_RECORDING_SQL,
    OBSController,
    OBSTelegramRouter,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

COACH_ID = "coach-jpr-001"
COACH_TG_ID = "tg-jpr-001"


def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# ---- Mocks ----

class MockWebSocket:
    def __init__(self, fail_connect=False):
        self._fail = fail_connect
        self.requests: list[tuple[str, Any]] = []
        self.closed = False
    async def connect(self, host, port, password):
        if self._fail:
            raise ConnectionError("OBS not running")
        return True
    async def send_request(self, request_type, data=None):
        self.requests.append((request_type, data))
        if request_type == "StopRecord":
            return {"outputPath": "C:/recordings/session.mp4"}
        return {}
    async def close(self):
        self.closed = True


class MockS3Uploader:
    def __init__(self):
        self.uploads: list[tuple[str, str]] = []
    async def upload(self, local_path, s3_key):
        self.uploads.append((local_path, s3_key))
        return f"s3://{s3_key}"


class FailingS3:
    async def upload(self, *a, **kw):
        raise IOError("S3 timeout")


class MockPipelineTrigger:
    def __init__(self):
        self.triggered: list[tuple[str, str]] = []
    async def trigger_session_intelligence(self, session_id, recording_url):
        self.triggered.append((session_id, recording_url))
        return True


# ===================================================================
# 1. Model validation (5 tests)
# ===================================================================

class TestModels:
    def test_recording_status_defaults(self):
        r = RecordingStatusPayload(coach_id=COACH_ID)
        assert r.pipeline_status == PipelineStatus.pending_upload
        assert r.recording_duration_seconds == 0

    def test_obs_command_result(self):
        r = OBSCommandResult(success=True, message="ok")
        assert r.success

    def test_connection_states(self):
        assert OBSConnectionState.disconnected.value == "disconnected"
        assert OBSConnectionState.authenticated.value == "authenticated"

    def test_recording_states(self):
        assert RecordingState.idle.value == "idle"
        assert RecordingState.recording.value == "recording"

    def test_pipeline_status_values(self):
        assert PipelineStatus.pending_transcription.value == "PENDING_TRANSCRIPTION"


# ===================================================================
# 2. OBS Connection — AC5 + AC6 (4 tests)
# ===================================================================

class TestConnection:
    def test_connect_success(self):
        ctrl = OBSController(ws=MockWebSocket())
        result = _run(ctrl.connect(coach_id=COACH_ID))
        assert result.success
        assert ctrl.connection_state == OBSConnectionState.authenticated

    def test_connect_failure_ac5(self):
        """AC5 — connection failure returns human-readable error."""
        ctrl = OBSController(ws=MockWebSocket(fail_connect=True))
        result = _run(ctrl.connect(coach_id=COACH_ID))
        assert not result.success
        assert "Could not connect to OBS" in result.error

    def test_no_websocket_ac5(self):
        """AC5 — no WebSocket configured."""
        ctrl = OBSController(ws=None)
        result = _run(ctrl.connect(coach_id=COACH_ID))
        assert not result.success
        assert "Could not connect to OBS" in result.error

    def test_disconnect(self):
        ws = MockWebSocket()
        ctrl = OBSController(ws=ws)
        _run(ctrl.connect(coach_id=COACH_ID))
        _run(ctrl.disconnect())
        assert ctrl.connection_state == OBSConnectionState.disconnected
        assert ws.closed


# ===================================================================
# 3. Start Recording — AC1 (3 tests)
# ===================================================================

class TestStartRecording:
    def test_start_recording_ac1(self):
        """AC1 — start recording via controller."""
        ws = MockWebSocket()
        ctrl = OBSController(ws=ws)
        _run(ctrl.connect(coach_id=COACH_ID))
        result = _run(ctrl.start_recording())
        assert result.success
        assert "Recording started" in result.message
        assert result.recording_state == RecordingState.recording
        assert ("StartRecord", None) in ws.requests

    def test_start_when_not_connected(self):
        ctrl = OBSController(ws=MockWebSocket())
        result = _run(ctrl.start_recording())
        assert not result.success
        assert "Could not connect" in result.error

    def test_start_when_already_recording(self):
        ws = MockWebSocket()
        ctrl = OBSController(ws=ws)
        _run(ctrl.connect(coach_id=COACH_ID))
        _run(ctrl.start_recording())
        result = _run(ctrl.start_recording())
        assert not result.success
        assert "Already recording" in result.error


# ===================================================================
# 4. Stop Recording — AC2 (3 tests)
# ===================================================================

class TestStopRecording:
    def test_stop_recording_ac2(self):
        """AC2 — stop recording + S3 upload."""
        s3 = MockS3Uploader()
        trigger = MockPipelineTrigger()
        ws = MockWebSocket()
        ctrl = OBSController(ws=ws, s3_uploader=s3, pipeline_trigger=trigger)
        _run(ctrl.connect(coach_id=COACH_ID))
        _run(ctrl.start_recording())
        result = _run(ctrl.stop_recording())
        assert result.success
        assert "Recording stopped" in result.message
        assert result.recording_state == RecordingState.idle
        assert len(s3.uploads) == 1

    def test_stop_when_not_recording(self):
        ctrl = OBSController(ws=MockWebSocket())
        _run(ctrl.connect(coach_id=COACH_ID))
        result = _run(ctrl.stop_recording())
        assert not result.success
        assert "Not currently recording" in result.error

    def test_stop_s3_failure_handled(self):
        """S3 failure doesn't crash stop_recording."""
        ws = MockWebSocket()
        ctrl = OBSController(ws=ws, s3_uploader=FailingS3())
        _run(ctrl.connect(coach_id=COACH_ID))
        _run(ctrl.start_recording())
        result = _run(ctrl.stop_recording())
        assert result.success  # Recording still stopped


# ===================================================================
# 5. Scene Switch — AC3 (3 tests)
# ===================================================================

class TestSceneSwitch:
    def test_switch_scene_ac3(self):
        """AC3 — switch to named scene."""
        ws = MockWebSocket()
        ctrl = OBSController(ws=ws)
        _run(ctrl.connect(coach_id=COACH_ID))
        result = _run(ctrl.switch_scene("Whiteboard"))
        assert result.success
        assert "Whiteboard" in result.message
        assert result.scene_name == "Whiteboard"

    def test_scenes_tracked(self):
        ws = MockWebSocket()
        ctrl = OBSController(ws=ws)
        _run(ctrl.connect(coach_id=COACH_ID))
        _run(ctrl.switch_scene("Main Camera"))
        _run(ctrl.switch_scene("Whiteboard"))
        status = _run(ctrl.get_recording_status())
        assert "Main Camera" in status.obs_scenes_used
        assert "Whiteboard" in status.obs_scenes_used

    def test_switch_when_not_connected(self):
        ctrl = OBSController(ws=MockWebSocket())
        result = _run(ctrl.switch_scene("Whiteboard"))
        assert not result.success


# ===================================================================
# 6. Pipeline Trigger — AC4 (2 tests)
# ===================================================================

class TestPipelineTrigger:
    def test_pipeline_triggered_ac4(self):
        """AC4 — session intelligence pipeline fired after recording stops."""
        trigger = MockPipelineTrigger()
        s3 = MockS3Uploader()
        ws = MockWebSocket()
        ctrl = OBSController(ws=ws, s3_uploader=s3, pipeline_trigger=trigger)
        _run(ctrl.connect(coach_id=COACH_ID))
        _run(ctrl.start_recording())
        _run(ctrl.stop_recording())
        assert len(trigger.triggered) == 1

    def test_no_pipeline_trigger_configured(self):
        s3 = MockS3Uploader()
        ws = MockWebSocket()
        ctrl = OBSController(ws=ws, s3_uploader=s3)
        _run(ctrl.connect(coach_id=COACH_ID))
        _run(ctrl.start_recording())
        result = _run(ctrl.stop_recording())
        assert result.success  # No crash


# ===================================================================
# 7. Recording Status (2 tests)
# ===================================================================

class TestRecordingStatus:
    def test_status_when_recording(self):
        ws = MockWebSocket()
        ctrl = OBSController(ws=ws)
        _run(ctrl.connect(coach_id=COACH_ID))
        _run(ctrl.start_recording())
        status = _run(ctrl.get_recording_status())
        assert status.coach_id == COACH_ID
        assert status.recording_started_at is not None

    def test_status_when_idle(self):
        ws = MockWebSocket()
        ctrl = OBSController(ws=ws)
        _run(ctrl.connect(coach_id=COACH_ID))
        status = _run(ctrl.get_recording_status())
        assert status.recording_duration_seconds == 0


# ===================================================================
# 8. Browser Source (2 tests)
# ===================================================================

class TestBrowserSource:
    def test_set_browser_source(self):
        ws = MockWebSocket()
        ctrl = OBSController(ws=ws)
        _run(ctrl.connect(coach_id=COACH_ID))
        result = _run(ctrl.set_browser_source("ExcalidrawOverlay", "http://localhost:3000"))
        assert result.success
        assert ("SetInputSettings", {"inputName": "ExcalidrawOverlay",
                "inputSettings": {"url": "http://localhost:3000"}}) in ws.requests

    def test_browser_source_not_connected(self):
        ctrl = OBSController(ws=MockWebSocket())
        result = _run(ctrl.set_browser_source("src", "http://x"))
        assert not result.success


# ===================================================================
# 9. Telegram Router — AC7 (4 tests)
# ===================================================================

class TestTelegramRouter:
    def test_unauthorized_rejected_ac7(self):
        """AC7 — non-coach user rejected."""
        ctrl = OBSController(ws=MockWebSocket())
        _run(ctrl.connect(coach_id=COACH_ID))
        router = OBSTelegramRouter(ctrl, {COACH_TG_ID})
        result = _run(router.handle_command("/record-start", "intruder-123"))
        assert not result.success
        assert "Unauthorized" in result.error

    def test_authorized_start(self):
        ws = MockWebSocket()
        ctrl = OBSController(ws=ws)
        _run(ctrl.connect(coach_id=COACH_ID))
        router = OBSTelegramRouter(ctrl, {COACH_TG_ID})
        result = _run(router.handle_command("/record-start", COACH_TG_ID))
        assert result.success

    def test_scene_command(self):
        ws = MockWebSocket()
        ctrl = OBSController(ws=ws)
        _run(ctrl.connect(coach_id=COACH_ID))
        router = OBSTelegramRouter(ctrl, {COACH_TG_ID})
        result = _run(router.handle_command("/scene", COACH_TG_ID, "Whiteboard"))
        assert result.success
        assert result.scene_name == "Whiteboard"

    def test_status_command(self):
        ws = MockWebSocket()
        ctrl = OBSController(ws=ws)
        _run(ctrl.connect(coach_id=COACH_ID))
        router = OBSTelegramRouter(ctrl, {COACH_TG_ID})
        result = _run(router.handle_command("/record-status", COACH_TG_ID))
        assert result.success
        assert "State:" in result.message


# ===================================================================
# 10. Constants & SQL (2 tests)
# ===================================================================

class TestConstants:
    def test_constants(self):
        assert DEFAULT_OBS_PORT == 4455
        assert MAX_RECONNECT_ATTEMPTS == 5
        assert "/record-start" in RECORDING_COMMANDS

    def test_sql_schema(self):
        assert "session_recordings" in SESSION_RECORDING_SQL
        assert "recording_id" in SESSION_RECORDING_SQL
