from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field

class BlindRankStateName(str, Enum):
    SESSION_READY = "session_ready"
    ITEM_REVEALED = "item_revealed"
    AWAITING_SLOT_LOCK = "awaiting_slot_lock"
    SLOT_LOCKED = "slot_locked"
    NEXT_ITEM_PENDING = "next_item_pending"
    BOARD_COMPLETE = "board_complete"
    DEFENSE_RECORDING = "defense_recording"
    PROCESSING = "processing"
    SCORED = "scored"
    REDEMPTION_REQUIRED = "redemption_required"
    EXPIRED = "expired"

class BlindRankTransitionName(str, Enum):
    REVEAL_FIRST_ITEM = "reveal_first_item"
    LOCK_SLOT = "lock_slot"
    REVEAL_NEXT_ITEM = "reveal_next_item"
    COMPLETE_BOARD = "complete_board"
    START_DEFENSE_RECORDING = "start_defense_recording"
    FINALIZE_DEFENSE = "finalize_defense"
    EXPIRE_SESSION = "expire_session"

class BlindRankItem(BaseModel):
    item_id: str = Field(..., description="Deterministic item identifier inside this session")
    reveal_index: int = Field(..., ge=1, le=5)
    surface_text: str | None = Field(default=None, description="The visible label. Null until JIT fetched/revealed (AC-5.2B)")
    surface_text_encrypted: str = Field(..., description="Encrypted string for initial payload to prevent inspection")
    subtitle: str | None = Field(default=None)
    revealed: bool = Field(default=False)
    locked_slot: int | None = Field(default=None, ge=1, le=5, description="Computed projection from event log")

class BlindRankSlot(BaseModel):
    slot_number: Literal[1, 2, 3, 4, 5] = Field(...)
    label: str = Field(..., min_length=1, description="Human label for the slot")
    occupied_item_id: str | None = Field(default=None, description="Computed projection from event log")
    locked: bool = Field(default=False)
    locked_at: datetime | None = Field(default=None)

class BlindRankAssignmentEvent(BaseModel):
    assignment_index: int = Field(..., ge=1, le=5)
    item_id: str = Field(...)
    slot_number: Literal[1, 2, 3, 4, 5] = Field(...)
    irreversible: Literal[True] = Field(default=True, description="Canonical source of truth for assignments")
    assigned_at: datetime = Field(...)
    state_after_assignment: BlindRankStateName = Field(...)

class BlindRankPromptPack(BaseModel):
    session_id: str = Field(...)
    coach_id: str = Field(...)
    startapp: Literal["react_blind_rank"] = Field(default="react_blind_rank")
    source_mode: Literal["blind_rank_reveal"] = Field(default="blind_rank_reveal")
    slot_labels: list[str] = Field(..., min_length=5, max_length=5, description="Visible labels for rank positions")
    ordered_items: list[BlindRankItem] = Field(..., min_length=5, max_length=5, description="Unrevealed text remains encrypted")
    current_state: BlindRankStateName = Field(default=BlindRankStateName.SESSION_READY)
    issued_at: datetime = Field(...)
    expires_at: datetime = Field(...)
    ttl_seconds: int = Field(..., ge=60, le=86400, description="Phase2-M01 Ephemeral Decay mandate")

class BlindRankBoardProjection(BaseModel):
    session_id: str = Field(...)
    slots: list[BlindRankSlot] = Field(..., min_length=5, max_length=5)
    revealed_item_ids: list[str] = Field(default_factory=list, max_length=5)
    remaining_slot_numbers: list[int] = Field(default_factory=list, max_length=5)
    current_item_id: str | None = Field(default=None)
    locked_assignments: list[BlindRankAssignmentEvent] = Field(default_factory=list, max_length=5)
    state_name: BlindRankStateName = Field(...)
    board_complete: bool = Field(default=False)

class BlindRankFinalizePayload(BaseModel):
    session_id: str = Field(...)
    coach_id: str = Field(...)
    recording_session_id: str = Field(..., description="Links board state to streaming audio/video artifact")
    prompt_pack: BlindRankPromptPack = Field(...)
    board_projection: BlindRankBoardProjection = Field(...)
    defense_started_at: datetime = Field(...)
    upload_status: Literal[
        "pending_background",
        "uploading",
        "uploaded",
        "failed_retryable",
    ] = Field(...)

class BlindRankSessionProjection(BaseModel):
    session_id: str = Field(...)
    coach_id: str = Field(...)
    prompt_pack: BlindRankPromptPack = Field(...)
    board_projection: BlindRankBoardProjection = Field(...)
    scoring_status: Literal[
        "recording",
        "processing",
        "scored",
        "redemption_required",
    ] = Field(...)
    export_eligible: bool = Field(default=False)
    score_ready: bool = Field(default=False)
    receipt_id: str | None = Field(default=None)
