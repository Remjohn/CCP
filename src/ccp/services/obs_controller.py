"""FR-CA11-13 — OBS Recording Pipeline Controller.

Python-side controller that communicates with OBS Studio's WebSocket
API v5 to provide programmatic recording control, scene switching, and
post-recording pipeline triggers.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Optional, Protocol

from src.ccp.models.ca11_models import (
    OBSCommandResult,
    OBSConnectionState,
    PipelineStatus,
    RecordingState,
    RecordingStatusPayload,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_OBS_HOST = "localhost"
DEFAULT_OBS_PORT = 4455
MAX_RECONNECT_ATTEMPTS = 5
RECONNECT_BACKOFF_BASE = 2  # seconds, exponential
PIPELINE_TIMEOUT_SECONDS = 600  # 10 minutes
RECORDING_COMMANDS = {"/record-start", "/record-stop", "/scene", "/record-status"}

# ---------------------------------------------------------------------------
# SQL
# ---------------------------------------------------------------------------

SESSION_RECORDING_SQL = """
CREATE TABLE IF NOT EXISTS session_recordings (
    recording_id    TEXT PRIMARY KEY,
    coach_id        TEXT NOT NULL,
    session_id      TEXT NOT NULL,
    recording_file  TEXT,
    duration_sec    INTEGER DEFAULT 0,
    scenes_used     TEXT[],
    started_at      TIMESTAMPTZ,
    stopped_at      TIMESTAMPTZ,
    pipeline_status TEXT NOT NULL DEFAULT 'PENDING_UPLOAD',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""

# ---------------------------------------------------------------------------
# Protocols
# ---------------------------------------------------------------------------


class WebSocketProtocol(Protocol):
    async def connect(self, host: str, port: int, password: str) -> bool: ...
    async def send_request(self, request_type: str,
                           data: dict[str, Any] | None = None) -> dict[str, Any]: ...
    async def close(self) -> None: ...


class S3UploaderProtocol(Protocol):
    async def upload(self, local_path: str, s3_key: str) -> str: ...


class PipelineTriggerProtocol(Protocol):
    async def trigger_session_intelligence(self, session_id: str,
                                           recording_url: str) -> bool: ...


# ---------------------------------------------------------------------------
# OBS Controller
# ---------------------------------------------------------------------------


class OBSController:
    """Controls OBS Studio via WebSocket API v5."""

    def __init__(
        self,
        ws: WebSocketProtocol | None = None,
        s3_uploader: S3UploaderProtocol | None = None,
        pipeline_trigger: PipelineTriggerProtocol | None = None,
    ) -> None:
        self._ws = ws
        self._s3 = s3_uploader
        self._pipeline = pipeline_trigger
        self._connection_state = OBSConnectionState.disconnected
        self._recording_state = RecordingState.idle
        self._current_scene: str | None = None
        self._scenes_used: list[str] = []
        self._recording_start: datetime | None = None
        self._coach_id: str | None = None
        self._reconnect_attempts = 0

    @property
    def connection_state(self) -> OBSConnectionState:
        return self._connection_state

    @property
    def recording_state(self) -> RecordingState:
        return self._recording_state

    async def connect(self, host: str = DEFAULT_OBS_HOST,
                      port: int = DEFAULT_OBS_PORT,
                      password: str = "", coach_id: str = "") -> OBSCommandResult:
        self._coach_id = coach_id
        if not self._ws:
            return OBSCommandResult(
                success=False,
                error="Could not connect to OBS. Please check that OBS is running and WebSocket is enabled.",
            )
        try:
            self._connection_state = OBSConnectionState.connecting
            ok = await self._ws.connect(host, port, password)
            if ok:
                self._connection_state = OBSConnectionState.authenticated
                self._reconnect_attempts = 0
                return OBSCommandResult(success=True, message="Connected to OBS ✅")
            self._connection_state = OBSConnectionState.disconnected
            return OBSCommandResult(success=False, error="Authentication failed")
        except Exception as exc:
            self._connection_state = OBSConnectionState.disconnected
            return OBSCommandResult(
                success=False,
                error=f"Could not connect to OBS. Please check that OBS is running and WebSocket is enabled.",
            )

    async def start_recording(self) -> OBSCommandResult:
        if self._connection_state != OBSConnectionState.authenticated:
            return OBSCommandResult(
                success=False,
                error="Could not connect to OBS. Please check that OBS is running and WebSocket is enabled.",
            )
        if self._recording_state == RecordingState.recording:
            return OBSCommandResult(
                success=False, error="Already recording",
                recording_state=RecordingState.recording,
            )
        if self._ws:
            try:
                await self._ws.send_request("StartRecord")
                self._recording_state = RecordingState.recording
                self._recording_start = datetime.now(timezone.utc)
                self._scenes_used = []
                if self._current_scene:
                    self._scenes_used.append(self._current_scene)
                return OBSCommandResult(
                    success=True, message="Recording started ⏺️",
                    recording_state=RecordingState.recording,
                )
            except Exception as exc:
                return OBSCommandResult(success=False, error=str(exc))
        return OBSCommandResult(success=False, error="WebSocket not available")

    async def stop_recording(self) -> OBSCommandResult:
        if self._recording_state != RecordingState.recording:
            return OBSCommandResult(
                success=False, error="Not currently recording",
                recording_state=self._recording_state,
            )
        if self._ws:
            try:
                self._recording_state = RecordingState.stopping
                result = await self._ws.send_request("StopRecord")
                self._recording_state = RecordingState.idle
                stopped_at = datetime.now(timezone.utc)
                duration = int((stopped_at - self._recording_start).total_seconds()) if self._recording_start else 0
                file_path = result.get("outputPath", "")

                # Post-recording pipeline
                recording_url = await self._handle_post_recording(
                    file_path, duration, stopped_at)

                return OBSCommandResult(
                    success=True,
                    message="Recording stopped. Processing session recap... ⏱️",
                    recording_state=RecordingState.idle,
                )
            except Exception as exc:
                self._recording_state = RecordingState.idle
                return OBSCommandResult(success=False, error=str(exc))
        return OBSCommandResult(success=False, error="WebSocket not available")

    async def switch_scene(self, scene_name: str) -> OBSCommandResult:
        if self._connection_state != OBSConnectionState.authenticated:
            return OBSCommandResult(success=False, error="Not connected to OBS")
        if self._ws:
            try:
                await self._ws.send_request(
                    "SetCurrentProgramScene",
                    {"sceneName": scene_name},
                )
                self._current_scene = scene_name
                if scene_name not in self._scenes_used:
                    self._scenes_used.append(scene_name)
                return OBSCommandResult(
                    success=True,
                    message=f"Switched to {scene_name} 🎬",
                    scene_name=scene_name,
                )
            except Exception as exc:
                return OBSCommandResult(success=False, error=str(exc))
        return OBSCommandResult(success=False, error="WebSocket not available")

    async def get_recording_status(self) -> RecordingStatusPayload:
        duration = 0
        if self._recording_state == RecordingState.recording and self._recording_start:
            duration = int((datetime.now(timezone.utc) - self._recording_start).total_seconds())
        return RecordingStatusPayload(
            coach_id=self._coach_id or "unknown",
            recording_duration_seconds=duration,
            obs_scenes_used=list(self._scenes_used),
            recording_started_at=self._recording_start,
        )

    async def set_browser_source(self, source_name: str, url: str) -> OBSCommandResult:
        if self._connection_state != OBSConnectionState.authenticated:
            return OBSCommandResult(success=False, error="Not connected to OBS")
        if self._ws:
            try:
                await self._ws.send_request(
                    "SetInputSettings",
                    {"inputName": source_name, "inputSettings": {"url": url}},
                )
                return OBSCommandResult(success=True, message=f"Browser source '{source_name}' updated")
            except Exception as exc:
                return OBSCommandResult(success=False, error=str(exc))
        return OBSCommandResult(success=False, error="WebSocket not available")

    async def disconnect(self) -> None:
        if self._ws:
            try:
                await self._ws.close()
            except Exception:
                pass
        self._connection_state = OBSConnectionState.disconnected

    # --- Private ---

    async def _handle_post_recording(
        self, file_path: str, duration: int, stopped_at: datetime,
    ) -> str | None:
        """Upload to S3 and trigger session intelligence pipeline."""
        if not file_path or not self._s3:
            return None
        coach = self._coach_id or "unknown"
        session_id = str(uuid.uuid4())
        s3_key = f"{coach}/sessions/{session_id}.mp4"
        try:
            recording_url = await self._s3.upload(file_path, s3_key)
        except Exception:
            return None

        if self._pipeline:
            try:
                await self._pipeline.trigger_session_intelligence(session_id, recording_url)
            except Exception:
                pass  # DamageControl handles retries in production
        return recording_url


# ---------------------------------------------------------------------------
# Telegram Bot Command Router
# ---------------------------------------------------------------------------


class OBSTelegramRouter:
    """Routes Telegram bot commands to OBS controller methods."""

    def __init__(self, controller: OBSController, authorized_coach_ids: set[str]) -> None:
        self._controller = controller
        self._authorized = authorized_coach_ids

    async def handle_command(
        self, command: str, user_id: str, args: str = "",
    ) -> OBSCommandResult:
        # AC7 — Authentication check
        if user_id not in self._authorized:
            return OBSCommandResult(success=False, error="Unauthorized")

        if command == "/record-start":
            return await self._controller.start_recording()
        elif command == "/record-stop":
            return await self._controller.stop_recording()
        elif command == "/scene":
            if not args.strip():
                return OBSCommandResult(success=False, error="Scene name required")
            return await self._controller.switch_scene(args.strip())
        elif command == "/record-status":
            status = await self._controller.get_recording_status()
            return OBSCommandResult(
                success=True,
                message=f"State: {self._controller.recording_state.value}, Duration: {status.recording_duration_seconds}s",
                recording_state=self._controller.recording_state,
            )
        return OBSCommandResult(success=False, error=f"Unknown command: {command}")
