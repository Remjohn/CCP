from __future__ import annotations
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

class SurfaceType(str, Enum):
    law28 = "law28"
    webinar = "webinar"
    networking = "networking"
    social = "social"

class LadderStage(str, Enum):
    discover = "discover"
    onboard = "onboard"
    immerse = "immerse"
    master = "master"
    replay = "replay"

class MomentumLevel(str, Enum):
    low = "low"
    stable = "stable"
    rising = "rising"
    hot = "hot"

class SafetyProfile(str, Enum):
    normal = "normal"
    sensitive = "sensitive"
    cooldown_required = "cooldown_required"

class RecoveryState(str, Enum):
    none = "none"
    comeback_due = "comeback_due"
    habit_broken = "habit_broken"
    shame_sensitive = "shame_sensitive"

class NextStepType(str, Enum):
    reward = "reward"
    scorecard_step = "scorecard_step"
    rebuttal_prompt = "rebuttal_prompt"
    recovery_invitation = "recovery_invitation"
    next_drill = "next_drill"

class RouteReason(str, Enum):
    active_surface_continuation = "active_surface_continuation"
    journey_progression = "journey_progression"
    comeback_recovery = "comeback_recovery"
    surface_rotation = "surface_rotation"
    readiness_override = "readiness_override"

class SurfaceReadinessSnapshot(BaseModel):
    surface: SurfaceType
    readiness_score: float = Field(..., ge=0.0, le=1.0)
    active_task_id: str = Field(default="", max_length=120)
    has_open_session: bool = False
    journey_id: str = Field(default="", max_length=120)
    journey_content_id: str = Field(default="", max_length=120)
    recommended_action_label: str = Field(..., min_length=1, max_length=120)

class ExperienceStatePacket(BaseModel):
    packet_id: str = Field(..., min_length=1)
    client_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    stage: LadderStage
    active_surface: SurfaceType
    momentum_level: MomentumLevel
    safety_profile: SafetyProfile
    recovery_state: RecoveryState
    current_journey_id: str = Field(default="", max_length=120)
    current_task_id: str = Field(default="", max_length=120)
    last_score_band: str = Field(default="", max_length=40)
    streak_days: int = Field(default=0, ge=0)
    missed_days: int = Field(default=0, ge=0)
    coping_position: int = Field(default=0, ge=0)
    atlas_week: int = Field(default=0, ge=0)
    readiness: list[SurfaceReadinessSnapshot] = Field(default_factory=list)
    next_step_type: NextStepType
    next_step_label: str = Field(..., min_length=1, max_length=160)
    next_prompt_text: str = Field(..., min_length=1, max_length=320)
    inline_deadline_ms: int = Field(default=3000, ge=500, le=3000)
    updated_at: datetime

class VoiceNoteIngressPacket(BaseModel):
    client_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    telegram_message_id: str = Field(..., min_length=1)
    voice_file_id: str = Field(..., min_length=1)
    voice_duration_seconds: int = Field(..., ge=1, le=600)
    submitted_at: datetime

class RouteDecisionPacket(BaseModel):
    route_id: str = Field(..., min_length=1)
    client_id: str = Field(..., min_length=1)
    from_surface: SurfaceType
    to_surface: SurfaceType
    reason: RouteReason
    next_step_type: NextStepType
    next_step_label: str = Field(..., min_length=1, max_length=160)
    route_latency_ms: int = Field(..., ge=0, le=3000)
    decided_at: datetime

class InlineRewardPacket(BaseModel):
    reward_id: str = Field(..., min_length=1)
    client_id: str = Field(..., min_length=1)
    surface: SurfaceType
    next_step_type: NextStepType
    headline: str = Field(..., min_length=1, max_length=160)
    body: str = Field(..., min_length=1, max_length=360)
    voice_prompt_job: str = Field(..., min_length=1, max_length=80)
    task_ticket_id: str = Field(default="", max_length=120)
    created_at: datetime

class AsyncExhaustJob(BaseModel):
    job_id: str = Field(..., min_length=1)
    client_id: str = Field(..., min_length=1)
    surface: SurfaceType
    source_route_id: str = Field(..., min_length=1)
    job_type: str = Field(..., min_length=1, max_length=120)
    status: str = Field(..., min_length=1, max_length=40)
    created_at: datetime

class RouteVoiceNoteRequest(BaseModel):
    ingress: VoiceNoteIngressPacket

class RouteVoiceNoteResponse(BaseModel):
    state_packet: ExperienceStatePacket
    route_decision: RouteDecisionPacket
    inline_reward: InlineRewardPacket
    exhaust_job: AsyncExhaustJob | None = None
