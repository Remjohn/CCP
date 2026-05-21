from __future__ import annotations
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

class EmotionalJob(str, Enum):
    ORIENT = "orient"
    RELIEVE = "relieve"
    VALIDATE = "validate"
    INVITE = "invite"
    REDIRECT = "redirect"
    CELEBRATE = "celebrate"

class JobSelectionReason(str, Enum):
    SESSION_START = "session_start"
    HESITATION_RECOVERY = "hesitation_recovery"
    DISCLOSURE_ACK = "disclosure_ack"
    ACTION_READY = "action_ready"
    CORRECTION_REQUIRED = "correction_required"
    WIN_CONFIRMED = "win_confirmed"

class RenderSource(str, Enum):
    CONSCIOUS_VOICE = "conscious_voice"
    PRE_RECORDED_HUMAN = "pre_recorded_human"

class PromptStatus(str, Enum):
    RESOLVED = "resolved"
    RENDER_QUEUED = "render_queued"
    RENDERED = "rendered"
    GATE_REJECTED = "gate_rejected"
    DISPATCHED = "dispatched"
    RETRY_PENDING = "retry_pending"
    FALLBACK_RENDERED = "fallback_rendered"
    FAILED_PRESTIGE_GUARD = "failed_prestige_guard"

class DeliverySurface(str, Enum):
    TELEGRAM = "telegram"
    MINI_APP = "mini_app"
    AFFINE = "affine"

class SonicBedProfile(BaseModel):
    bed_id: str = Field(min_length=1)
    display_name: str = Field(min_length=1)
    emotional_job: EmotionalJob
    fade_in_ms: int = Field(ge=0)
    fade_out_ms: int = Field(ge=0)
    target_gain: float = Field(ge=0.0, le=1.0)
    duration_ceiling_seconds: int = Field(gt=0, le=90)

class VoicePromptTriggerContext(BaseModel):
    coach_id: str = Field(min_length=1)
    user_id: str = Field(min_length=1)
    surface: DeliverySurface
    reason: JobSelectionReason
    locale: str = Field(min_length=2, max_length=8)
    source_session_id: str | None = None
    score_delta: float | None = Field(default=None, ge=-100.0, le=100.0)
    streak_days: int | None = Field(default=None, ge=0)

class VoicePromptPacket(BaseModel):
    voice_prompt_id: str = Field(min_length=1)
    coach_id: str = Field(min_length=1)
    user_id: str = Field(min_length=1)
    emotional_job: EmotionalJob
    job_selection_reason: JobSelectionReason
    surface: DeliverySurface
    locale: str = Field(min_length=2, max_length=8)
    script_text: str = Field(min_length=1, max_length=1200)
    sonic_bed_profile: SonicBedProfile
    voice_dna_profile_ref: str = Field(min_length=1)
    render_source_preference: RenderSource = RenderSource.CONSCIOUS_VOICE
    duration_target_seconds: int = Field(gt=0, le=90)
    created_at: datetime

class PreRecordedFallbackPack(BaseModel):
    fallback_pack_id: str = Field(min_length=1)
    coach_id: str = Field(min_length=1)
    emotional_job: EmotionalJob
    locale: str = Field(min_length=2, max_length=8)
    audio_asset_id: str = Field(min_length=1)
    transcript_reference: str = Field(min_length=1)
    duration_seconds: int = Field(gt=0, le=90)

class VoicePromptRenderAttempt(BaseModel):
    render_attempt_id: str = Field(min_length=1)
    voice_prompt_id: str = Field(min_length=1)
    render_source: RenderSource
    provider_reference: str = Field(min_length=1)
    audio_asset_id: str | None = None
    sample_rate_hz: int = Field(gt=0)
    duration_seconds: int = Field(gt=0, le=90)
    prestige_gate_passed: bool = False
    rejection_reason: str | None = None
    created_at: datetime

class VoicePromptDeliveryRecord(BaseModel):
    delivery_id: str = Field(min_length=1)
    voice_prompt_id: str = Field(min_length=1)
    surface: DeliverySurface
    dispatched_at: datetime | None = None
    delivery_status: PromptStatus
    retry_count: int = Field(ge=0)
    telegram_chat_id: str | None = None

class VoicePromptTelemetryRecord(BaseModel):
    telemetry_id: str = Field(min_length=1)
    voice_prompt_id: str = Field(min_length=1)
    replay_count: int = Field(ge=0)
    completion_count: int = Field(ge=0)
    forward_count: int = Field(ge=0)
    reply_count: int = Field(ge=0)
    resonance_marker: bool = False
    recorded_at: datetime
