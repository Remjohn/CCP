from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Literal, Optional
from pydantic import BaseModel, Field


class OverlayMediaFormat(str, Enum):
    WEBM_VP9 = "video/webm;codecs=vp9"
    MP4_H264 = "video/mp4;codecs=avc1"


class OverlayCaptureStatus(str, Enum):
    IDLE = "idle"
    RECORDING = "recording"
    PAUSED_BACKGROUNDED = "paused_backgrounded"
    STOPPED = "stopped"
    FAILED_RECOVERABLE = "failed_recoverable"


class AdaptiveResolutionProfile(BaseModel):
    width: int = Field(default=720, ge=360)
    height: int = Field(default=1280, ge=640)
    frame_rate: int = Field(default=30, ge=15, le=60)
    video_bitrate_bps: int = Field(default=4_000_000, ge=1_000_000, le=8_000_000)
    media_format: OverlayMediaFormat = Field(...)
    device_tier: Literal["low", "mid", "high"] = Field(default="mid")
    resolution_downgraded: bool = Field(default=False)


class OverlayInteractionEvent(BaseModel):
    event_type: Literal[
        "overlay_mounted",
        "capture_started",
        "round_state_change",
        "transition_played",
        "sound_cue_played",
        "capture_stopped",
        "resolution_adapted",
        "capture_failed",
    ] = Field(...)
    session_id: str = Field(...)
    timestamp_ms: int = Field(..., ge=0)
    round_index: int | None = Field(default=None, ge=1)
    from_state: str | None = Field(default=None)
    to_state: str | None = Field(default=None)
    overlay_elements: dict = Field(default_factory=dict, description="Mode-specific visible element state snapshot")
    capture_state: dict = Field(default_factory=dict, description="Current recording health: fps, resolution, audio level")
    receipt_id: str | None = Field(default=None)


class CompositeCaptureMetadata(BaseModel):
    session_id: str = Field(...)
    coach_id: str = Field(...)
    resolution: AdaptiveResolutionProfile = Field(...)
    capture_status: OverlayCaptureStatus = Field(...)
    started_at: datetime | None = Field(default=None)
    stopped_at: datetime | None = Field(default=None)
    duration_ms: int = Field(default=0, ge=0)
    blob_size_bytes: int = Field(default=0, ge=0)
    upload_status: Literal[
        "pending_background",
        "uploading",
        "uploaded",
        "failed_retryable",
    ] = Field(default="pending_background")
    interaction_event_count: int = Field(default=0, ge=0)
    audio_track_present: bool = Field(default=True)
    video_track_present: bool = Field(default=True)


class OverlayModeConfig(BaseModel):
    mode_key: str = Field(..., min_length=1, description="e.g. react_alphabet, react_tierlist")
    overlay_layout: Literal[
        "rosco_ring",
        "tier_rows",
        "rank_slots",
        "elimination_grid",
        "question_card",
        "split_screen",
        "generic_overlay",
    ] = Field(...)
    sound_pack: str = Field(default="default", description="Audio sprite pack identifier")
    camera_position: Literal["background_fill", "pip_corner", "split_half"] = Field(default="background_fill")
    requires_face_tracking: bool = Field(default=False)
    target_aspect_ratio: Literal["9:16", "16:9", "1:1"] = Field(default="9:16")
