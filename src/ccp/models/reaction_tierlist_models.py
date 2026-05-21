from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field

from src.ccp.models.ca11_models import ResolvedPalette
from src.ccp.models.reaction_engine_models import (
    ReactionArtifactRecord,
    ReactionScoreCard,
    ReactionSessionRecord,
    ReactionTopicBrief,
)


class TierLabel(str, Enum):
    s = "S"
    a = "A"
    b = "B"
    c = "C"
    d = "D"
    f = "F"


class TierlistItem(BaseModel):
    item_id: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    asset_url: str | None = None
    current_tier: TierLabel | None = None
    current_rank_index: int | None = Field(default=None, ge=0)


class TierlistMoveEvent(BaseModel):
    event_id: str = Field(..., min_length=1)
    item_id: str = Field(..., min_length=1)
    spoken_phrase: str = Field(..., min_length=1)
    target_tier: TierLabel = Field(...)
    target_rank_index: int = Field(..., ge=0)
    confidence: float = Field(..., ge=0.0, le=1.0) # Fallback threshold: < 0.85
    created_at: datetime = Field(...)
    source: Literal["speech", "manual_fallback"] = Field(default="speech")


class TierlistBoardProjection(BaseModel):
    startapp: Literal["react_tierlist"] = Field(default="react_tierlist")
    topic: ReactionTopicBrief = Field(...)
    session: ReactionSessionRecord | None = None
    tiers: list[TierLabel] = Field(default_factory=lambda: [TierLabel.s, TierLabel.a, TierLabel.b, TierLabel.c])
    ranked_items: list[TierlistItem] = Field(default_factory=list)
    unranked_items: list[TierlistItem] = Field(default_factory=list)
    move_events: list[TierlistMoveEvent] = Field(default_factory=list)
    snap_animation_enabled: bool = Field(default=True)
    speech_degraded: bool = Field(default=False)


class TierlistResultProjection(BaseModel):
    artifact: ReactionArtifactRecord = Field(...)
    final_board: TierlistBoardProjection = Field(...)
    total_move_count: int = Field(default=0, ge=0)
    words_ranked_count: int = Field(default=0, ge=0)
