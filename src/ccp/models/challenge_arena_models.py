from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class ChallengeLayer(str, Enum):
    FOUNDATION = "foundation"
    STRUCTURE = "structure"
    NUANCE = "nuance"
    COMMAND = "command"


class CapacityTrack(str, Enum):
    RECOVERY = "recovery"
    FOUNDATION = "foundation"
    GROWTH = "growth"
    MOMENTUM = "momentum"
    PEAK = "peak"


class JourneyPhase(str, Enum):
    DISCOVER = "discover"
    ONBOARD = "onboard"
    IMMERSE = "immerse"
    MASTER = "master"
    REPLAY = "replay"


class AssignmentKind(str, Enum):
    VERTICAL = "vertical"
    LATERAL = "lateral"
    RECOVERY = "recovery"


class ProgressionDecision(str, Enum):
    VERTICAL_ADVANCE = "vertical_advance"
    LATERAL_VARIATION = "lateral_variation"
    HOLD_FOR_REVISION = "hold_for_revision"


class SessionStatus(str, Enum):
    ROUTED = "routed"
    HABIT_PENDING = "habit_pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"
    EXPIRED = "expired"


class PostcardStatus(str, Enum):
    NOT_DUE = "not_due"
    PENDING = "pending"
    PUBLISHED = "published"
    ACKNOWLEDGED = "acknowledged"


class TraitScoreSummary(BaseModel):
    trait_id: str = Field(..., min_length=3)
    label: str = Field(..., min_length=2)
    score: int = Field(..., ge=1, le=10)


class Fr61EvidenceSnapshot(BaseModel):
    conviction_density: float = Field(..., ge=0.0, le=1.0)
    hedge_frequency: float = Field(..., ge=0.0)
    micro_pause_count: int = Field(..., ge=0)
    pitch_stability: float = Field(..., ge=0.0, le=1.0)
    words_spoken: int = Field(..., ge=0)
    evidence_captured_at: datetime = Field(...)
    trait_scores: list[TraitScoreSummary] = Field(default_factory=list)


class HabitVerificationProjection(BaseModel):
    tracker_id: UUID = Field(...)
    environmental_cue: str | None = Field(default=None, max_length=280)
    concrete_action: str | None = Field(default=None, max_length=280)
    habit_status: str = Field(...)
    verification_verdict: str = Field(...)
    last_checked_date: datetime = Field(...)


class LateralProgressionState(BaseModel):
    current_layer: ChallengeLayer = Field(...)
    capacity_track: CapacityTrack = Field(...)
    journey_phase: JourneyPhase = Field(...)
    session_index: int = Field(..., ge=1)
    layer_attempt_count: int = Field(..., ge=0)
    vertical_ready: bool = Field(...)
    blocked_reason: str | None = Field(default=None, max_length=120)
    previous_locked_fingerprint: str | None = Field(default=None, max_length=120)
    current_fingerprint: str = Field(..., min_length=3, max_length=120)
    same_screen_protection_active: bool = Field(...)


class ChallengeAssignment(BaseModel):
    assignment_id: UUID = Field(...)
    journey_id: str = Field(..., min_length=3)
    journey_node_id: str = Field(..., min_length=3)
    command_key: str = Field(..., min_length=3)
    variation_key: str = Field(..., min_length=3)
    assignment_kind: AssignmentKind = Field(...)
    decision: ProgressionDecision = Field(...)
    target_layer: ChallengeLayer = Field(...)
    target_capacity_track: CapacityTrack = Field(...)
    session_index: int = Field(..., ge=1)
    prompt_text: str = Field(..., min_length=10)
    why_now: str = Field(..., min_length=10)
    expires_at: datetime = Field(...)


class WeeklyTelemetryRollup(BaseModel):
    week_start_utc: datetime = Field(...)
    week_end_utc: datetime = Field(...)
    sessions_completed: int = Field(..., ge=0)
    cumulative_words_spoken: int = Field(..., ge=0)
    cumulative_micro_pauses: int = Field(..., ge=0)
    avg_hedge_frequency: float = Field(..., ge=0.0)
    prior_week_avg_hedge_frequency: float = Field(..., ge=0.0)
    delta_words_spoken: int = Field(...)
    delta_hedge_frequency: float = Field(...)


class SundayPostcardProjection(BaseModel):
    postcard_id: UUID = Field(...)
    participant_id: str = Field(..., min_length=3)
    coach_id: str = Field(..., min_length=3)
    status: PostcardStatus = Field(...)
    telemetry: WeeklyTelemetryRollup = Field(...)
    qualitative_interpretation: str = Field(..., min_length=20)
    forward_forecast: str = Field(..., min_length=10)
    published_at: datetime = Field(...)
    acknowledged_at: datetime | None = Field(default=None)


class ChallengeArenaSessionProjection(BaseModel):
    startapp: Literal["challenge"] = Field(default="challenge")
    participant_id: str = Field(..., min_length=3)
    coach_id: str = Field(..., min_length=3)
    current_state: LateralProgressionState = Field(...)
    assignment: ChallengeAssignment = Field(...)
    latest_habit_verification: HabitVerificationProjection | None = Field(default=None)
    latest_evidence: Fr61EvidenceSnapshot | None = Field(default=None)
    postcard_status: PostcardStatus = Field(...)
    streak_count: int = Field(..., ge=0)
    active_days_this_week: int = Field(..., ge=0, le=7)


class ChallengeDailyRouteRequest(BaseModel):
    participant_id: str = Field(..., min_length=3)
    coach_id: str = Field(..., min_length=3)
    journey_id: str = Field(..., min_length=3)
    coping_position: int = Field(..., ge=0)
    atlas_week: int = Field(..., ge=0)
    current_layer: ChallengeLayer = Field(...)
    capacity_track: CapacityTrack = Field(...)


class ChallengeSessionCompletionRequest(BaseModel):
    participant_id: str = Field(..., min_length=3)
    assignment_id: UUID = Field(...)
    words_spoken: int = Field(..., ge=0)
    micro_pause_count: int = Field(..., ge=0)
    conviction_density: float = Field(..., ge=0.0, le=1.0)
    hedge_frequency: float = Field(..., ge=0.0)
    pitch_stability: float = Field(..., ge=0.0, le=1.0)
    completed_at: datetime = Field(...)
