from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ResolvedPalette(BaseModel):
    background_primary: str
    background_secondary: str
    accent: str


class ReactionArtifactRecord(BaseModel):
    artifact_id: str


class ReactionScoreCard(BaseModel):
    score: int


class ReactionSessionRecord(BaseModel):
    session_id: str


class RankingQuizSourceItem(BaseModel):
    item_id: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    original_slot_index: int = Field(..., ge=0)
    asset_url: str | None = None


class RankingQuizOriginalRanking(BaseModel):
    source_artifact_id: str = Field(..., min_length=1)
    source_mode: Literal["react_tierlist"] = Field(default="react_tierlist")
    published_by_person_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    frozen_at: datetime = Field(...)
    items: list[RankingQuizSourceItem] = Field(..., min_length=1)


class RankingQuizProposalItem(BaseModel):
    item_id: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    proposed_slot_index: int = Field(..., ge=0)


class RankingQuizDiffEntry(BaseModel):
    item_id: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    original_slot_index: int = Field(..., ge=0)
    proposed_slot_index: int = Field(..., ge=0)
    slot_delta: int = Field(...)


class RankingQuizProposalArtifact(BaseModel):
    proposal_id: str = Field(..., min_length=1)
    session_id: str = Field(..., min_length=1)
    proposer_person_id: str = Field(..., min_length=1)
    status: Literal["submitted", "duplicate_suppressed"] = Field(default="submitted")
    proposal_items: list[RankingQuizProposalItem] = Field(..., min_length=1)
    diff_entries: list[RankingQuizDiffEntry] = Field(default_factory=list)
    changed_item_count: int = Field(..., ge=0)
    proposal_caption: str | None = Field(default=None, max_length=280)
    defense_session: ReactionSessionRecord | None = None
    defense_artifact: ReactionArtifactRecord | None = None
    defense_scorecard: ReactionScoreCard | None = None
    submitted_at: datetime = Field(...)


class RankingQuizSessionProjection(BaseModel):
    startapp: Literal["react_ranking_quiz"] = Field(default="react_ranking_quiz")
    session_id: str = Field(..., min_length=1)
    palette: ResolvedPalette = Field(...)
    original_ranking: RankingQuizOriginalRanking = Field(...)
    working_order: list[RankingQuizProposalItem] = Field(..., min_length=1)
    share_token: str = Field(..., min_length=1)
    proposal_count: int = Field(default=0, ge=0)
    proposal_submission_open: bool = Field(default=True)


class RankingQuizComparisonProjection(BaseModel):
    session: RankingQuizSessionProjection = Field(...)
    proposal: RankingQuizProposalArtifact = Field(...)
