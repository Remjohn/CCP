from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, HttpUrl


class RedFlagSeverity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class DiagnosticExcerptSource(str, Enum):
    transcript_snippet = "transcript_snippet"
    pause_pattern = "pause_pattern"
    scoring_evidence = "scoring_evidence"
    session_summary = "session_summary"


class InterceptGateStatus(str, Enum):
    locked = "locked"
    ready = "ready"
    recording = "recording"
    completed = "completed"
    blocked = "blocked"


class BroadcastSessionStatus(str, Enum):
    draft = "draft"
    queued = "queued"
    ready = "ready"
    live = "live"
    completed = "completed"
    failed = "failed"


class EvidencePointer(BaseModel):
    session_id: str = Field(..., min_length=1)
    asset_id: str = Field(..., min_length=1)
    workspace_section: str = Field(..., min_length=1)
    workspace_entry_id: str = Field(..., min_length=1)


class ConvictionScoreBreakdown(BaseModel):
    composite_score: float = Field(..., ge=0.0, le=100.0)


class ProgressArcSnapshot(BaseModel):
    completion_percent: float = Field(..., ge=0.0, le=100.0)
    current_program_step: str = Field(..., min_length=1)
    streak_days: int = Field(..., ge=0)
    mood_indicator: str = Field(..., min_length=1)
    next_required_action: str = Field(..., min_length=1)


class DiagnosticExcerpt(BaseModel):
    excerpt_id: str = Field(..., min_length=1)
    source_type: DiagnosticExcerptSource
    display_excerpt: str = Field(..., min_length=8, max_length=500)
    rationale: str = Field(..., min_length=8, max_length=300)
    excerpt_hash: str = Field(..., min_length=32, max_length=128)
    evidence_pointer: EvidencePointer
    flagged_at: datetime
    confidence_label: str = Field(..., min_length=1)


class RedFlagFeedEntry(BaseModel):
    flag_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    client_id: str = Field(..., min_length=1)
    severity: RedFlagSeverity
    flag_title: str = Field(..., min_length=3, max_length=120)
    flag_summary: str = Field(..., min_length=8, max_length=240)
    excerpt: DiagnosticExcerpt
    gate_status: InterceptGateStatus = Field(default=InterceptGateStatus.locked)
    created_at: datetime


class ClientCardProjection(BaseModel):
    projection_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    client_id: str = Field(..., min_length=1)
    client_display_name: str = Field(..., min_length=1, max_length=120)
    client_workspace_url: HttpUrl
    progress_arc: ProgressArcSnapshot
    conviction: ConvictionScoreBreakdown
    red_flags: list[RedFlagFeedEntry] = Field(default_factory=list)
    primary_cta: str = Field(..., min_length=1, max_length=80)
    updated_at: datetime


class BroadcastQueueItem(BaseModel):
    broadcast_session_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    program_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1, max_length=160)
    status: BroadcastSessionStatus
    planned_start_at: datetime | None = None
    studio_session_id: str = Field(default="", max_length=120)
    audience_surface: str = Field(..., min_length=1, max_length=80)


class DashboardSummary(BaseModel):
    coach_id: str = Field(..., min_length=1)
    workspace_id: str = Field(..., min_length=1)
    generated_at: datetime
    client_cards: list[ClientCardProjection] = Field(default_factory=list)
    broadcast_queue: list[BroadcastQueueItem] = Field(default_factory=list)


class ReviewAcknowledgementRequest(BaseModel):
    coach_id: str = Field(..., min_length=1)
    client_id: str = Field(..., min_length=1)
    excerpt_hash: str = Field(..., min_length=32, max_length=128)
    acknowledgement_phrase: str = Field(
        ...,
        pattern=r"^I have reviewed this$",
    )


class ReviewAcknowledgementRecord(BaseModel):
    acknowledgement_id: str = Field(..., min_length=1)
    flag_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    client_id: str = Field(..., min_length=1)
    excerpt_hash: str = Field(..., min_length=32, max_length=128)
    acknowledged_at: datetime
    gate_status_after_ack: InterceptGateStatus = Field(
        default=InterceptGateStatus.ready
    )


class InterceptStartRequest(BaseModel):
    coach_id: str = Field(..., min_length=1)
    client_id: str = Field(..., min_length=1)
    flag_id: str = Field(..., min_length=1)
    workspace_id: str = Field(..., min_length=1)


class InterceptSessionRecord(BaseModel):
    intercept_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    client_id: str = Field(..., min_length=1)
    flag_id: str = Field(..., min_length=1)
    gate_status: InterceptGateStatus
    excerpt_hash: str = Field(..., min_length=32, max_length=128)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    recorder_session_id: str = Field(default="", max_length=120)
    workspace_id: str = Field(..., min_length=1)


class BroadcastLaunchRequest(BaseModel):
    coach_id: str = Field(..., min_length=1)
    workspace_id: str = Field(..., min_length=1)
    program_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1, max_length=160)
    target_surface: str = Field(..., min_length=1, max_length=80)


class BroadcastLaunchResult(BaseModel):
    broadcast_session_id: str = Field(..., min_length=1)
    studio_session_id: str = Field(..., min_length=1)
    status: BroadcastSessionStatus
    launch_receipt_id: str = Field(..., min_length=1)
