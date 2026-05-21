from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class AuthorityQuizLevelState(str, Enum):
    READY = "ready"
    QUESTION_ACTIVE = "question_active"
    ANSWERED_CORRECT = "answered_correct"
    ANSWERED_INCORRECT = "answered_incorrect"
    LADDER_ADVANCED = "ladder_advanced"
    LADDER_COMPLETE = "ladder_complete"
    PROCESSING = "processing"
    SCORED = "scored"
    REDEMPTION_REQUIRED = "redemption_required"
    EXPIRED = "expired"


class AuthorityQuizQuestion(BaseModel):
    question_id: str = Field(...)
    level_index: int = Field(..., ge=1)
    prompt_text: str = Field(..., min_length=5)
    answer_options: list[str] = Field(..., min_length=2, max_length=6)
    correct_answer_key: str = Field(..., min_length=1, max_length=2)
    stakes_label: str = Field(..., min_length=2, description="Visible level framing")
    time_limit_seconds: int = Field(default=20, ge=5, le=120)


class AuthorityQuizEscalationDelta(BaseModel):
    luminance_drop_pct: float = Field(..., ge=0.0, le=0.8)
    contrast_boost_pct: float = Field(..., ge=0.0, le=1.0)
    saturation_boost_pct: float = Field(..., ge=0.0, le=1.0)
    pad_dominance_delta: float = Field(..., ge=0.0, le=1.0)
    pad_arousal_delta: float = Field(..., ge=0.0, le=1.0)


class AuthorityQuizEscalationProfile(BaseModel):
    level_index: int = Field(..., ge=1)
    total_levels: int = Field(..., ge=1)
    escalation_fraction: float = Field(..., ge=0.0, le=1.0)
    delta: AuthorityQuizEscalationDelta = Field(...)


class AuthorityQuizVisualPressureProjection(BaseModel):
    level_index: int = Field(..., ge=1)
    escalation_profile: AuthorityQuizEscalationProfile | None = Field(default=None)
    audience_mood_state: str = Field(..., min_length=1)
    palette_token_version: str = Field(default="1.0")
    background_primary: str = Field(..., min_length=4)
    background_secondary: str = Field(..., min_length=4)
    accent: str = Field(..., min_length=4)
    border_emphasis: float = Field(..., ge=0.0, le=1.0)
    ambient_glow_strength: float = Field(..., ge=0.0, le=1.0)


class AuthorityQuizLevelResult(BaseModel):
    question_id: str = Field(...)
    level_index: int = Field(..., ge=1)
    selected_answer_key: str = Field(..., min_length=1, max_length=2)
    was_correct: bool = Field(default=False)
    answered_at: datetime = Field(...)
    state_after_answer: AuthorityQuizLevelState = Field(...)
    pressure_projection: AuthorityQuizVisualPressureProjection = Field(...)


class AuthorityQuizPromptPack(BaseModel):
    session_id: str = Field(...)
    coach_id: str = Field(...)
    startapp: Literal["react_authority_quiz"] = Field(default="react_authority_quiz")
    source_mode: Literal["authority_quiz"] = Field(default="authority_quiz")
    title: str = Field(..., min_length=3)
    questions: list[AuthorityQuizQuestion] = Field(..., min_length=3, max_length=10)
    base_mood_state: str = Field(..., min_length=1)
    issued_at: datetime = Field(...)
    expires_at: datetime = Field(...)
    ttl_seconds: int = Field(..., ge=60, le=86400)


class AuthorityQuizSessionProjection(BaseModel):
    session_id: str = Field(...)
    coach_id: str = Field(...)
    prompt_pack: AuthorityQuizPromptPack = Field(...)
    level_results: list[AuthorityQuizLevelResult] = Field(..., min_length=1, max_length=10)
    current_level_index: int = Field(..., ge=1)
    current_state: AuthorityQuizLevelState = Field(...)
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
