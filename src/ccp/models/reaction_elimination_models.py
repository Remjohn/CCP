from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class TimerAggressionLevel(str, Enum):
    CALM = "calm"
    PRESSURED = "pressured"
    INTENSE = "intense"
    FINAL = "final"


class EliminationRoundState(str, Enum):
    READY = "ready"
    ROUND_ACTIVE = "round_active"
    OPTION_ELIMINATED = "option_eliminated"
    ROUND_CLOSED = "round_closed"
    LADDER_COMPLETE = "ladder_complete"
    PROCESSING = "processing"
    SCORED = "scored"
    REDEMPTION_REQUIRED = "redemption_required"
    EXPIRED = "expired"


class EliminationOption(BaseModel):
    option_id: str = Field(...)
    surface_text: str = Field(..., min_length=2)
    subtitle: str = Field(default="")
    eliminated: bool = Field(default=False)
    eliminated_round: int | None = Field(default=None, ge=1, le=7)
    survived_to_end: bool = Field(default=False)


class TimerAggressionProfile(BaseModel):
    level: TimerAggressionLevel = Field(...)
    pulse_duration_ms: int = Field(..., ge=200, le=3000)
    accent_token: str = Field(..., min_length=1, description="CSS variable/token name")
    scale_amplitude: float = Field(..., ge=0.0, le=0.5)
    border_flash_enabled: bool = Field(default=False)


class EliminationRoundPrompt(BaseModel):
    round_index: int = Field(..., ge=1, le=7)
    round_duration_seconds: Literal[10] = Field(default=10)
    active_option_count: int = Field(..., ge=2, le=8)
    aggression_profile: TimerAggressionProfile = Field(...)


class EliminationRoundResult(BaseModel):
    round_prompt: EliminationRoundPrompt = Field(...)
    eliminated_option_id: str = Field(...)
    eliminated_at: datetime = Field(...)
    remaining_option_ids: list[str] = Field(..., min_length=1, max_length=7)
    state_after_round: EliminationRoundState = Field(...)


class LastOneStandingPromptPack(BaseModel):
    session_id: str = Field(...)
    coach_id: str = Field(...)
    startapp: Literal["react_elimination"] = Field(default="react_elimination")
    source_mode: Literal["last_one_standing"] = Field(default="last_one_standing")
    title: str = Field(..., min_length=3)
    options: list[EliminationOption] = Field(..., min_length=8, max_length=8)
    rounds: list[EliminationRoundPrompt] = Field(..., min_length=7, max_length=7)
    issued_at: datetime = Field(...)
    expires_at: datetime = Field(...)
    ttl_seconds: int = Field(..., ge=60, le=3600)


class RemainingOptionsProjection(BaseModel):
    session_id: str = Field(...)
    active_option_ids: list[str] = Field(..., min_length=1, max_length=8)
    eliminated_option_ids: list[str] = Field(default_factory=list, max_length=7)
    current_round_index: int = Field(..., ge=1, le=7)
    current_state: EliminationRoundState = Field(...)
    current_aggression_level: TimerAggressionLevel = Field(...)


class EliminationNarrativeArc(BaseModel):
    session_id: str = Field(...)
    elimination_order: list[str] = Field(..., min_length=7, max_length=7, description="Ordered first-out to last-out")
    survivor_option_id: str = Field(...)
    total_rounds_completed: Literal[7] = Field(default=7)


class LastOneStandingSessionProjection(BaseModel):
    session_id: str = Field(...)
    coach_id: str = Field(...)
    prompt_pack: LastOneStandingPromptPack = Field(...)
    round_results: list[EliminationRoundResult] = Field(..., min_length=1, max_length=7)
    remaining_projection: RemainingOptionsProjection = Field(...)
    narrative_arc: EliminationNarrativeArc | None = Field(default=None)
    upload_status: Literal[
        "pending_background",
        "uploading",
        "uploaded",
        "failed_retryable",
    ] = Field(...)
    scoring_status: Literal[
        "recording",
        "processing",
        "scored",
        "redemption_required",
    ] = Field(...)
    export_eligible: bool = Field(default=False)
    score_ready: bool = Field(default=False)
    receipt_id: str | None = Field(default=None)
