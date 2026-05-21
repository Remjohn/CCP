from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field

from src.ccp.models.ca11_models import ContentMachineResult, ResolvedPalette
# The following imports will be valid when FR-ERA3-05-CORE is physically present in the workspace
from src.ccp.models.reaction_engine_models import (
    ReactionArtifactRecord,
    ReactionScoreCard,
    ReactionSessionRecord,
    ReactionTopicBrief,
)


class SoloUiPhase(str, Enum):
    brief = "brief"
    recording = "recording"
    scoring = "scoring"
    score_reveal = "score_reveal"
    deployed = "deployed"
    redemption = "redemption"


class SoloDeploymentDecision(str, Enum):
    deployed_to_cmf = "deployed_to_cmf"
    pending_cmf_retry = "pending_cmf_retry"
    redemption_required = "redemption_required"


class SoloTopicBriefView(ReactionTopicBrief):
    startapp: Literal["react_solo"] = Field(default="react_solo")
    palette: ResolvedPalette = Field(...)
    min_duration_seconds: int = Field(default=120, ge=120, le=300)
    max_duration_seconds: int = Field(default=300, ge=120, le=300)
    briefing_audio_required: bool = Field(default=True)
    expires_in_seconds: int = Field(..., ge=1, le=86400)
    source_label: str = Field(..., min_length=1)


class SoloRecordingViewState(BaseModel):
    session: ReactionSessionRecord = Field(...)
    phase: SoloUiPhase = Field(default=SoloUiPhase.recording)
    elapsed_seconds: int = Field(default=0, ge=0, le=300)
    max_duration_seconds: int = Field(default=300, ge=120, le=300)
    upload_ticket: str = Field(..., min_length=1)
    upload_status: Literal[
        "not_started",
        "pending_background",
        "uploading",
        "uploaded",
        "failed_retryable",
    ] = Field(default="not_started")
    stream_status: Literal["connected", "degraded", "recovered"] = Field(default="connected")
    stop_acknowledged_at: datetime | None = None
    local_blob_persisted: bool = Field(default=False)


class SoloScoreRevealPayload(BaseModel):
    artifact: ReactionArtifactRecord = Field(...)
    scorecard: ReactionScoreCard = Field(...)
    export_decision: SoloDeploymentDecision | None = Field(default=None)
    export_eligible: bool = Field(default=False)
    approval_required: bool = Field(default=True)
    coaching_cues: list[str] = Field(default_factory=list, max_length=2)
    cmf_delivery_deadline_at: datetime | None = None


class SoloDeploymentProjection(BaseModel):
    artifact_id: str = Field(..., min_length=1)
    decision: SoloDeploymentDecision = Field(...)
    content_machine_result: ContentMachineResult | None = None
    queue_status: Literal["not_queued", "queued", "delivered", "failed_retryable"] = Field(default="not_queued")
    delivery_eta_minutes: int | None = Field(default=None, ge=1, le=20)
    delivered_at: datetime | None = None
    redemption_session_id: str | None = None


class SoloReactionLaunchPayload(BaseModel):
    coach_id: str = Field(..., min_length=1)
    startapp: Literal["react_solo"] = Field(default="react_solo")
    ui_phase: SoloUiPhase = Field(default=SoloUiPhase.brief)
    topic: SoloTopicBriefView = Field(...)
    active_recording: SoloRecordingViewState | None = None
    last_score_reveal: SoloScoreRevealPayload | None = None
