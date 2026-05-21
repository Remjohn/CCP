"""
FR-ERA3-35C Eval Card System and Shareable Audit Board Models
=============================================================
Canonical Pydantic v2 schemas and validation logic for premium cards and boards.
"""

from __future__ import annotations

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, model_validator


# ── Enums ──────────────────────────────────────────────────────────────

class VisibleCardStatKey(str, Enum):
    humanity = "humanity"
    presence = "presence"
    trust = "trust"
    memorability = "memorability"
    resonance = "resonance"
    signal = "signal"
    ai_slop_risk = "ai_slop_risk"


class EvalCardRole(str, Enum):
    audit_primary = "audit_primary"
    audit_secondary = "audit_secondary"
    before_snapshot = "before_snapshot"
    after_snapshot = "after_snapshot"
    marketing_preview = "marketing_preview"
    operator_review = "operator_review"


class EvalBoardKind(str, Enum):
    single_card_detail = "single_card_detail"
    audit_spread = "audit_spread"
    before_after_comparison = "before_after_comparison"
    shareable_summary = "shareable_summary"


class CardScoreBand(str, Enum):
    weak = "weak"
    developing = "developing"
    strong = "strong"
    elite = "elite"


class BoardDensity(str, Enum):
    compact = "compact"
    standard = "standard"
    spacious = "spacious"


# ── Models ─────────────────────────────────────────────────────────────

class CardThumbnailAsset(BaseModel):
    asset_id: str = Field(..., min_length=1)
    storage_uri: str = Field(..., min_length=1)
    width: int = Field(..., ge=1)
    height: int = Field(..., ge=1)
    alt_text: str = Field(..., min_length=1)
    source_kind: str = Field(..., min_length=1)


class EvalCardStatLine(BaseModel):
    key: VisibleCardStatKey = Field(...)
    label: str = Field(..., min_length=1)
    score: int = Field(..., ge=0, le=99)
    band: CardScoreBand = Field(...)


class CardVerdictBlock(BaseModel):
    verdict_line: str = Field(..., min_length=1)
    fix_line: str = Field(..., min_length=1)
    confidence_note: Optional[str] = Field(default=None)


class CardThemeProjection(BaseModel):
    background_primary: str = Field(..., min_length=1)
    background_secondary: str = Field(..., min_length=1)
    accent: str = Field(..., min_length=1)
    text_primary: str = Field(..., min_length=1)
    brand_hue_used: bool = Field(default=False)


class EvalCardFace(BaseModel):
    title: str = Field(..., min_length=1)
    subtitle: Optional[str] = Field(default=None)
    thumbnail: CardThumbnailAsset = Field(...)
    overall_score: int = Field(..., ge=0, le=99)
    role: EvalCardRole = Field(...)
    card_type_label: str = Field(..., min_length=1)
    visible_stats: List[EvalCardStatLine] = Field(..., min_length=7, max_length=7)
    verdict: CardVerdictBlock = Field(...)

    @model_validator(mode="after")
    def validate_visible_stats_keys(self) -> EvalCardFace:
        keys_present = [stat.key for stat in self.visible_stats]
        if len(keys_present) != 7:
            raise ValueError("visible_stats must contain exactly 7 stats")
        if len(set(keys_present)) != 7:
            raise ValueError("visible_stats must not contain duplicate keys")
        required_keys = set(VisibleCardStatKey)
        if set(keys_present) != required_keys:
            raise ValueError(f"visible_stats must contain exactly: {list(VisibleCardStatKey)}")
        return self


class EvalCard(BaseModel):
    card_id: str = Field(..., min_length=1)
    report_id: str = Field(..., min_length=1)
    face: EvalCardFace = Field(...)
    theme: CardThemeProjection = Field(...)
    source_content_type: str = Field(..., min_length=1)
    archetype_hint: Optional[str] = Field(default=None)
    generated_at: str = Field(..., min_length=1)
    provisional_upstream_contract: bool = Field(default=False)


class EvalBoardLayout(BaseModel):
    board_kind: EvalBoardKind = Field(...)
    density: BoardDensity = Field(default=BoardDensity.standard)
    columns: int = Field(..., ge=1, le=6)
    featured_card_id: Optional[str] = Field(default=None)
    card_order: List[str] = Field(default_factory=list)
    screenshot_safe: bool = Field(default=True)


class EvalCardBoard(BaseModel):
    board_id: str = Field(..., min_length=1)
    report_id: str = Field(..., min_length=1)
    board_kind: EvalBoardKind = Field(...)
    title: str = Field(..., min_length=1)
    subtitle: Optional[str] = Field(default=None)
    cards: List[EvalCard] = Field(default_factory=list)
    layout: EvalBoardLayout = Field(...)
    summary_line: str = Field(..., min_length=1)
    share_caption: Optional[str] = Field(default=None)


class ShareableAuditBoardRenderRequest(BaseModel):
    board: EvalCardBoard = Field(...)
    output_format: str = Field(..., min_length=1)
    target_surface: str = Field(..., min_length=1)
    watermark_enabled: bool = Field(default=True)
