from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class RenderSurfaceType(str, Enum):
    SINGLE_IMAGE = "single_image"
    CAROUSEL = "carousel"
    REEL = "reel"
    AUDIT_CARD = "audit_card"
    AUDIT_BOARD = "audit_board"
    AUDIT_EXPLAINER = "audit_explainer"
    COURSE_VIDEO = "course_video"


class CompositionDepthMode(str, Enum):
    REPETITION_WITH_VARIATION = "repetition_with_variation"
    LAYERED_INTERPRETATION = "layered_interpretation"
    RHYTHMIC_STRUCTURE = "rhythmic_structure"
    STRATEGIC_AMBIGUITY = "strategic_ambiguity"


class VariationHintMode(str, Enum):
    ASYMMETRY_BALANCE = "asymmetry_balance"
    RESONANCE_CARRY = "resonance_carry"
    SALIENCE_DISTRIBUTION = "salience_distribution"
    PARADOX_RETENTION = "paradox_retention"
    PREDICTABILITY_BREAK = "predictability_break"


class TemporalRelationType(str, Enum):
    VANILLA_SHOT = "vanilla_shot"
    TRANSITION = "transition"
    HARD_CUT = "hard_cut"
    SUDDEN_JUMP_RISK = "sudden_jump_risk"


class RenderFallbackDecision(str, Enum):
    PASS = "pass"
    REVIEW = "review"
    DOWNGRADE = "downgrade"
    BLOCK = "block"


class ScoreCardVisibleScore(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label: str = Field(..., min_length=2, max_length=32)
    score_0_99: int = Field(..., ge=0, le=99)


class ScoreCardRenderBundle(BaseModel):
    model_config = ConfigDict(extra="forbid")

    card_id: str = Field(..., min_length=1, max_length=80)
    content_thumbnail_asset_id: str = Field(..., min_length=1, max_length=120)
    surface_type: RenderSurfaceType = Field(default=RenderSurfaceType.AUDIT_CARD)
    overall_score_0_99: int = Field(..., ge=0, le=99)
    ai_slop_risk_0_99: int = Field(..., ge=0, le=99)
    visible_scores: list[ScoreCardVisibleScore] = Field(..., min_length=6, max_length=6)
    verdict_line: str = Field(..., min_length=8, max_length=240)
    format_ratio: str = Field(..., min_length=2, max_length=8)


class AuditBoardRenderBundle(BaseModel):
    model_config = ConfigDict(extra="forbid")

    board_id: str = Field(..., min_length=1, max_length=80)
    card_ids: list[str] = Field(..., min_length=1)
    hero_thumbnail_asset_id: str = Field(..., min_length=1, max_length=120)
    board_layout_template_id: str = Field(..., min_length=1, max_length=120)
    page_count: int = Field(..., ge=1, le=50)
    export_targets: list[str] = Field(default_factory=list)


class TemporalCraftHint(BaseModel):
    model_config = ConfigDict(extra="forbid")

    cluster_id: str = Field(..., min_length=1, max_length=80)
    relation_type: TemporalRelationType
    cut_ms: int = Field(..., ge=0)
    hold_ms: int = Field(..., ge=0)
    pause_weight_ms: int = Field(..., ge=0)
    transition_label: str = Field(..., min_length=1, max_length=80)
    sudden_jump_risk: float = Field(..., ge=0.0, le=1.0)
    interpretability_note: str = Field(..., min_length=8, max_length=240)


class TemporalCraftHints(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hint_set_id: str = Field(..., min_length=1, max_length=80)
    source_video_asset_id: str = Field(default="", max_length=120)
    hints: list[TemporalCraftHint] = Field(default_factory=list)
    rhythm_summary: str = Field(..., min_length=8, max_length=240)


class CompositionDepthRenderProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    profile_id: str = Field(..., min_length=1, max_length=80)
    surface_type: RenderSurfaceType
    repetition_with_variation_weight: float = Field(..., ge=0.0, le=1.0)
    layered_interpretation_weight: float = Field(..., ge=0.0, le=1.0)
    rhythmic_structure_weight: float = Field(..., ge=0.0, le=1.0)
    strategic_ambiguity_weight: float = Field(..., ge=0.0, le=1.0)
    preserve_subtext: bool = Field(default=True)
    allow_explicit_exposition: bool = Field(default=False)


class VariationRenderHints(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hint_id: str = Field(..., min_length=1, max_length=80)
    surface_type: RenderSurfaceType
    asymmetry_balance_target: float = Field(..., ge=0.0, le=1.0)
    resonance_carry_target: float = Field(..., ge=0.0, le=1.0)
    salience_distribution_target: float = Field(..., ge=0.0, le=1.0)
    paradox_retention_target: float = Field(..., ge=0.0, le=1.0)
    predictability_break_target: float = Field(..., ge=0.0, le=1.0)
    notes: list[str] = Field(default_factory=list)


class RenderPerceptualPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    plan_id: str = Field(..., min_length=1, max_length=80)
    content_output_id: str = Field(..., min_length=1, max_length=120)
    coach_id: str = Field(..., min_length=1, max_length=120)
    surface_type: RenderSurfaceType
    function_stack_packet_id: str = Field(..., min_length=1, max_length=120)
    directional_integrity_report_id: str = Field(..., min_length=1, max_length=120)
    perceptual_influence_report_id: str = Field(..., min_length=1, max_length=120)
    depth_profile: CompositionDepthRenderProfile
    variation_hints: VariationRenderHints
    temporal_hints: TemporalCraftHints
    target_thumbnail_count: int = Field(..., ge=1, le=24)
    card_safe: bool = Field(default=False)
    pdf_safe: bool = Field(default=False)
    generated_at: datetime


class PreservationDimensionResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dimension_name: str = Field(..., min_length=3, max_length=64)
    intended_level: float = Field(..., ge=0.0, le=1.0)
    realized_level: float = Field(..., ge=0.0, le=1.0)
    preserved: bool
    rationale: str = Field(..., min_length=8, max_length=240)


class RenderPreservationReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    report_id: str = Field(..., min_length=1, max_length=80)
    plan_id: str = Field(..., min_length=1, max_length=80)
    manifest_id: str = Field(default="", max_length=80)
    fallback_decision: RenderFallbackDecision
    dimensions: list[PreservationDimensionResult] = Field(default_factory=list)
    lost_intents: list[str] = Field(default_factory=list)
    downgraded_surfaces: list[str] = Field(default_factory=list)
    reviewer_notes: list[str] = Field(default_factory=list)
    created_at: datetime
