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


class DebateStance(str, Enum):
    for_side = "for"
    against_side = "against"


class JuryVoteStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    duplicate = "duplicate"
    expired = "expired"


class DebateLaunchPayload(BaseModel):
    startapp: Literal["react_debate"] = Field(default="react_debate")
    debate_id: str = Field(..., min_length=1)
    lane_key: str = Field(..., min_length=1)
    lane_title: str = Field(..., min_length=1)
    topic: ReactionTopicBrief = Field(...)
    palette: ResolvedPalette = Field(...)
    source_artifact_id: str = Field(..., min_length=1)
    source_speaker_person_id: str = Field(..., min_length=1)
    allowed_stances: list[DebateStance] = Field(
        default_factory=lambda: [DebateStance.for_side, DebateStance.against_side],
        min_length=2,
        max_length=2,
    )
    neutral_allowed: Literal[False] = Field(default=False)
    latest_tally_for: int = Field(default=0, ge=0)
    latest_tally_against: int = Field(default=0, ge=0)


class DebateCounterTakeIntent(BaseModel):
    debate_id: str = Field(..., min_length=1)
    source_artifact_id: str = Field(..., min_length=1)
    selected_stance: DebateStance = Field(...)
    prior_vote_id: str | None = None
    must_select_before_recording: bool = Field(default=True)
    session: ReactionSessionRecord | None = None


class AudienceJuryInlineVote(BaseModel):
    vote_id: str = Field(..., min_length=1)
    debate_id: str = Field(..., min_length=1)
    artifact_id: str = Field(..., min_length=1)
    voter_person_id: str = Field(..., min_length=1)
    voted_side: DebateStance = Field(...)
    callback_token: str = Field(..., min_length=1)
    status: JuryVoteStatus = Field(default=JuryVoteStatus.pending)
    registered_at: datetime | None = None
    opens_mini_app: Literal[False] = Field(default=False)


class VoteThenReactPrompt(BaseModel):
    prompt_id: str = Field(..., min_length=1)
    source_vote_id: str = Field(..., min_length=1)
    selected_stance: DebateStance = Field(...)
    prompt_copy: str = Field(..., min_length=1)
    cta_label: str = Field(..., min_length=1)
    deep_link_url: str = Field(..., min_length=1)
    startapp: Literal["react_debate"] = Field(default="react_debate")
    expires_at: datetime = Field(...)


class DebateVsArtifactProjection(BaseModel):
    debate_id: str = Field(..., min_length=1)
    root_artifact: ReactionArtifactRecord = Field(...)
    counter_artifact: ReactionArtifactRecord | None = None
    root_scorecard: ReactionScoreCard | None = None
    counter_scorecard: ReactionScoreCard | None = None
    render_format: Literal["split_screen_vs"] = Field(default="split_screen_vs")
    composition: CanvasComposition | None = None
    content_machine_result: ContentMachineResult | None = None
    tally_for: int = Field(default=0, ge=0)
    tally_against: int = Field(default=0, ge=0)
    visual_adversary_passed: bool = Field(default=False)
    public_share_ready: bool = Field(default=False)
