from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field

class TimingVerificationStatus(str, Enum):
    VERIFIED = "verified"
    VERIFIED_WITH_DRIFT = "verified_with_drift"
    SUSPICIOUS = "suspicious"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"

class AlphabetRoundState(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    ANSWER_CAPTURED = "answer_captured"
    TIMEOUT = "timeout"
    CLOSED = "closed"

class AlphabetChallengeRoundPrompt(BaseModel):
    round_index: int = Field(..., ge=1)
    letter: str = Field(..., min_length=1, max_length=1, description="Displayed constraint letter")
    category_prompt: str = Field(..., min_length=3, description="Domain/category for valid answers")
    answer_window_ms: Literal[3000] = Field(default=3000)

class AlphabetTimingCapture(BaseModel):
    client_clock_source: Literal["performance.now", "date.now_fallback"] = Field(...)
    letter_revealed_at_client_ms: float = Field(..., ge=0)
    answer_detected_at_client_ms: float | None = Field(default=None, ge=0)
    elapsed_ms: float | None = Field(default=None, ge=0)
    timing_pass: bool = Field(default=False)
    client_epoch_revealed_at_ms: int = Field(..., ge=0, description="Wall clock for coarse audit correlation")
    client_epoch_answered_at_ms: int | None = Field(default=None, ge=0)
    submission_enqueued_at_ms: int | None = Field(default=None, ge=0)
    submission_sent_at_ms: int | None = Field(default=None, ge=0)

class AlphabetRoundResult(BaseModel):
    prompt: AlphabetChallengeRoundPrompt = Field(...)
    state: AlphabetRoundState = Field(...)
    timing: AlphabetTimingCapture = Field(...)
    captured_phrase: str = Field(default="", description="Client-side captured answer text or first-pass transcript")
    semantic_validity: Literal[
        "pending",
        "valid",
        "invalid",
        "ambiguous",
    ] = Field(default="pending", description="valid (NIM confidence >= 0.85), invalid (< 0.60), ambiguous (0.60-0.84, preserves score but triggers async human review)")
    failure_reason: Literal[
        "none",
        "timeout",
        "invalid_term",
        "empty_answer",
        "suspicious_timing",
    ] = Field(default="none")

class AlphabetChallengePromptPack(BaseModel):
    session_id: str = Field(...)
    coach_id: str = Field(...)
    startapp: Literal["react_alphabet"] = Field(default="react_alphabet")
    source_mode: Literal["alphabet_challenge"] = Field(default="alphabet_challenge")
    challenge_title: str = Field(..., min_length=3)
    rounds: list[AlphabetChallengeRoundPrompt] = Field(..., min_length=1, max_length=26)
    current_round_index: int = Field(default=1, ge=1)
    issued_at: datetime = Field(...)
    expires_at: datetime = Field(...)
    ttl_seconds: int = Field(..., ge=60, le=3600)

class AlphabetTimingVerificationPayload(BaseModel):
    session_id: str = Field(...)
    coach_id: str = Field(...)
    round_results: list[AlphabetRoundResult] = Field(..., min_length=1, max_length=26)
    verification_status: TimingVerificationStatus = Field(...)
    suspicious_round_indexes: list[int] = Field(default_factory=list, max_length=26)
    server_received_at: datetime = Field(...)
    receipt_id: str | None = Field(default=None)

class AlphabetFinalizePayload(BaseModel):
    session_id: str = Field(...)
    coach_id: str = Field(...)
    prompt_pack: AlphabetChallengePromptPack = Field(...)
    timing_payload: AlphabetTimingVerificationPayload = Field(...)
    upload_status: Literal[
        "pending_background",
        "uploading",
        "uploaded",
        "failed_retryable",
    ] = Field(...)

class AlphabetChallengeSessionProjection(BaseModel):
    session_id: str = Field(...)
    coach_id: str = Field(...)
    prompt_pack: AlphabetChallengePromptPack = Field(...)
    round_results: list[AlphabetRoundResult] = Field(..., min_length=1, max_length=26)
    rounds_passed_in_time: int = Field(default=0, ge=0)
    rounds_semantically_valid: int = Field(default=0, ge=0)
    verification_status: TimingVerificationStatus = Field(...)
    scoring_status: Literal[
        "recording",
        "processing",
        "scored",
        "redemption_required",
    ] = Field(...)
    export_eligible: bool = Field(default=False)
    score_ready: bool = Field(default=False)
    receipt_id: str | None = Field(default=None)
