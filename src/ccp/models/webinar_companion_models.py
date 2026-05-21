from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from src.ccp.models.ca11_models import ResolvedPalette
from src.ccp.models.cross_system_models import WebinarPart


class VideoRect(BaseModel):
    x: float = Field(..., ge=0.0, le=1.0)
    y: float = Field(..., ge=0.0, le=1.0)
    width: float = Field(..., gt=0.0, le=1.0)
    height: float = Field(..., gt=0.0, le=1.0)


class WebinarPromptAnchor(BaseModel):
    prompt_id: str = Field(..., min_length=1)
    webinar_id: str = Field(..., min_length=1)
    slide_index_start: int = Field(..., ge=0)
    slide_index_end: int = Field(..., ge=0)
    trigger_at_seconds: float = Field(..., ge=0.0)
    prompt_type: Literal["poll", "voice_note", "reaction", "cta"]
    copy: str = Field(..., min_length=1, max_length=280)
    poll_choices: list[str] | None = None
    cta_url: str | None = None
    preferred_geometry: Literal["lower_third", "right_drawer"] = Field(default="lower_third")
    expires_at_seconds: float | None = Field(default=None, ge=0.0)


class ParticipationCaptureRecord(BaseModel):
    capture_id: str = Field(..., min_length=1)
    webinar_id: str = Field(..., min_length=1)
    participant_person_id: str = Field(..., min_length=1)
    prompt_id: str = Field(..., min_length=1)
    module_part: WebinarPart | None = None
    slide_index_start: int = Field(..., ge=0)
    slide_index_end: int = Field(..., ge=0)
    reaction_type: Literal["poll", "voice_note", "reaction", "cta"]
    poll_choice_key: str | None = None
    voice_note_asset_id: str | None = None
    reaction_emoji: str | None = None
    submitted_at: datetime = Field(...)


class RepSlideAdvanceEvent(BaseModel):
    rep_session_id: str = Field(..., min_length=1)
    webinar_id: str = Field(..., min_length=1)
    previous_slide_index: int = Field(..., ge=0)
    next_slide_index: int = Field(..., ge=0)
    previous_slide_started_at: datetime = Field(...)
    previous_slide_stopped_at: datetime = Field(...)
    advanced_at: datetime = Field(...)
    previous_slide_transcript: str = Field(..., min_length=1)


class RepSlideScoreCard(BaseModel):
    rep_session_id: str = Field(..., min_length=1)
    webinar_id: str = Field(..., min_length=1)
    slide_index: int = Field(..., ge=0)
    delivered_at: datetime = Field(...)
    hedge_density: float = Field(..., ge=0.0)
    pause_architecture_score: float = Field(..., ge=0.0, le=100.0)
    cta_pressure_stability: float = Field(..., ge=0.0, le=100.0)
    highlighted_traits: list[str] = Field(default_factory=list)
    feedback_summary: str = Field(..., min_length=1)
    next_slide_unlocked: bool = Field(default=False)


class WebinarCompanionSessionProjection(BaseModel):
    startapp: Literal["webinar"] = Field(default="webinar")
    webinar_id: str = Field(..., min_length=1)
    session_mode: Literal["live_watch", "replay_watch", "rep_review", "extract_review"]
    palette: ResolvedPalette = Field(...)
    video_url: str = Field(..., min_length=1)
    protected_focal_region: VideoRect = Field(...)
    prompt_anchors: list[WebinarPromptAnchor] = Field(default_factory=list)
    participation_open: bool = Field(default=True)
    downloadable_asset_ids: list[str] = Field(default_factory=list)
    current_rep_score: RepSlideScoreCard | None = None
