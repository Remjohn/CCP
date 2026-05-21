from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field

from src.ccp.models.ca11_models import ContentMachineResult, ResolvedPalette
from src.ccp.models.reaction_engine_models import (
    ReactionArtifactRecord,
    ReactionScoreCard,
    ReactionSessionRecord,
    ReactionTopicBrief,
)
from src.ccp.models.visual_engine_models import CanvasComposition

class DuelLifecycleState(str, Enum):
    proposed = "proposed"
    accepted = "accepted"
    waiting_for_opponent = "waiting_for_opponent"
    awaiting_comparison = "awaiting_comparison"
    unified = "unified"
    closed = "closed"
    rejected_bracket = "rejected_bracket"

class DuelBracketTier(str, Enum):
    foundation = "foundation"
    emerging = "emerging"
    advanced = "advanced"
    sovereign = "sovereign"

class DuelBracketSnapshot(BaseModel):
    coach_id: str = Field(..., min_length=1)
    bracket_tier: DuelBracketTier = Field(...)
    local_bracket_key: str = Field(..., min_length=1)
    overall_trait_average: float = Field(..., ge=1.0, le=10.0)
    confidence_directness_index: float = Field(..., ge=1.0, le=10.0)
    polarity_authority_index: float = Field(..., ge=1.0, le=10.0)
    calculated_at: datetime = Field(...)

class DuelInvitePayload(BaseModel):
    startapp: Literal["react_duel"] = Field(default="react_duel")
    duel_id: str = Field(..., min_length=1)
    inviter_coach_id: str = Field(..., min_length=1)
    invitee_coach_id: str = Field(..., min_length=1)
    topic: ReactionTopicBrief = Field(...)
    palette: ResolvedPalette = Field(...)
    inviter_bracket: DuelBracketSnapshot = Field(...)
    invitee_bracket: DuelBracketSnapshot | None = None
    lifecycle_state: DuelLifecycleState = Field(default=DuelLifecycleState.proposed)
    async_only: Literal[True] = Field(default=True)
    expires_at: datetime = Field(..., description="Must be min(now + 12h, topic.expires_at) to avoid CORE rejection")

class DuelParticipantState(BaseModel):
    coach_id: str = Field(..., min_length=1)
    accepted_at: datetime | None = None
    session: ReactionSessionRecord | None = None
    artifact: ReactionArtifactRecord | None = None
    scorecard: ReactionScoreCard | None = None
    ready_for_unification: bool = Field(default=False)

class UnifiedDuelProjection(BaseModel):
    duel_id: str = Field(..., min_length=1)
    lifecycle_state: DuelLifecycleState = Field(...)
    topic_id: str = Field(..., min_length=1)
    bracket_tier: DuelBracketTier = Field(...)
    left_side: DuelParticipantState = Field(...)
    right_side: DuelParticipantState = Field(...)
    unified_artifact_id: str | None = None
    render_format: Literal["split_screen_vs"] = Field(default="split_screen_vs")
    composition: CanvasComposition | None = None
    audience_vote_open: bool = Field(default=False)
    content_machine_result: ContentMachineResult | None = None
