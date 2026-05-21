"""
src/ccp/models/benchmark_profile_models.py
==========================================
Pydantic v2 model definitions for FR-ERA3-35B Content Benchmark Profiles and Card Weighting Bundles.
"""

from __future__ import annotations
from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, model_validator, field_validator
from src.ccp.models.archetype_container_runtime_models import ArchetypeChoice


class ContentType(str, Enum):
    SINGLE_IMAGE_POST = "single_image_post"
    CAROUSEL = "carousel"
    REEL = "reel"


class CardRole(str, Enum):
    AUDIT_CARD = "audit_card"
    PROOF_CARD = "proof_card"
    COMPARISON_CARD = "comparison_card"
    PROGRESS_CARD = "progress_card"


class VisibleScoreKey(str, Enum):
    HUMANITY = "humanity"
    PRESENCE = "presence"
    TRUST = "trust"
    MEMORABILITY = "memorability"
    RESONANCE = "resonance"
    SIGNAL = "signal"
    AI_SLOP_RISK = "ai_slop_risk"


class VisibleScoreWeightMap(BaseModel):
    humanity: float = Field(ge=0.0, le=1.0)
    presence: float = Field(ge=0.0, le=1.0)
    trust: float = Field(ge=0.0, le=1.0)
    memorability: float = Field(ge=0.0, le=1.0)
    resonance: float = Field(ge=0.0, le=1.0)
    signal: float = Field(ge=0.0, le=1.0)

    @model_validator(mode="after")
    def weights_sum_to_one(self) -> VisibleScoreWeightMap:
        total = (self.humanity + self.presence + self.trust
                 + self.memorability + self.resonance + self.signal)
        # Checking to make sure it's within tolerance [0.99, 1.01]
        if not (0.99 <= total <= 1.01):
            raise ValueError(f"Weights must sum to 1.0, got {total:.4f}")
        return self


class PenaltyAdjustmentMap(BaseModel):
    ai_slop_penalty_multiplier: float = Field(ge=0.0, le=1.0, default=0.15)
    trust_floor: float = Field(ge=0.0, le=100.0, default=30.0)
    humanity_floor: float = Field(ge=0.0, le=100.0, default=25.0)
    overall_cap_when_trust_below_floor: float = Field(ge=0.0, le=100.0, default=65.0)
    overall_cap_when_humanity_below_floor: float = Field(ge=0.0, le=100.0, default=60.0)
    overall_cap_when_slop_above_threshold: float = Field(ge=0.0, le=100.0, default=55.0)
    slop_danger_threshold: float = Field(ge=0.0, le=100.0, default=70.0)
    presence_without_trust_cap: float = Field(ge=0.0, le=100.0, default=70.0)


class ModalityDimension(BaseModel):
    dimension_id: str = Field(..., min_length=1)
    dimension_name: str = Field(..., min_length=1)
    feeds_cluster: str = Field(..., min_length=1)
    weight_in_cluster: float = Field(..., ge=0.0, le=1.0)


class ModalitySupportProfile(BaseModel):
    modality_id: str = Field(..., min_length=1)
    content_type: ContentType
    dimensions: List[ModalityDimension] = Field(..., min_length=1)


class ContentBenchmarkProfile(BaseModel):
    profile_id: str = Field(..., min_length=1)
    profile_version: str = Field(default="1.0", min_length=1)
    content_type: ContentType
    base_weights: VisibleScoreWeightMap
    penalties: PenaltyAdjustmentMap
    modality_profile: ModalitySupportProfile
    rationale: str = Field(..., min_length=1)


class ScoreEmphasis(BaseModel):
    score_key: VisibleScoreKey
    emphasis_delta: float = Field(...)
    rationale: str = Field(..., min_length=1)

    @field_validator("emphasis_delta")
    @classmethod
    def validate_emphasis_delta(cls, v: float) -> float:
        if not (-0.3 <= v <= 0.3):
            raise ValueError(f"Emphasis delta must be in [-0.3, +0.3], got {v}")
        return v


class ArchetypeScoreBundle(BaseModel):
    bundle_id: str = Field(..., min_length=1)
    archetype_choice: ArchetypeChoice
    content_type: ContentType
    emphasis_adjustments: List[ScoreEmphasis] = Field(..., min_length=1)
    penalty_overrides: Optional[PenaltyAdjustmentMap] = None
    bundle_rationale: str = Field(..., min_length=1)


class CardWeightingBundle(BaseModel):
    bundle_id: str = Field(..., min_length=1)
    content_type: ContentType
    archetype_choice: ArchetypeChoice
    card_role: CardRole
    resolved_weights: VisibleScoreWeightMap
    resolved_penalties: PenaltyAdjustmentMap
    modality_dimensions: List[ModalityDimension] = Field(default_factory=list)
    source_profile_id: str = Field(..., min_length=1)
    source_bundle_id: str = Field(..., min_length=1)
    resolution_trace: str = Field(..., min_length=1)


class OverallScoreComputation(BaseModel):
    raw_scores: Dict[str, float] = Field(..., min_length=7)
    card_weighting_bundle: CardWeightingBundle
    weighted_base: float = Field(..., ge=0.0, le=100.0)
    slop_penalty_applied: float = Field(..., ge=0.0, le=100.0)
    caps_applied: List[str] = Field(default_factory=list)
    final_overall: int = Field(..., ge=0, le=99)
    computation_trace: str = Field(..., min_length=1)


# =========================================================================
# Canonical Baselines (5.6)
# =========================================================================

SINGLE_IMAGE_BASELINE = ContentBenchmarkProfile(
    profile_id="CBP-IMG-001",
    content_type=ContentType.SINGLE_IMAGE_POST,
    base_weights=VisibleScoreWeightMap(
        humanity=0.20, presence=0.12, trust=0.22,
        memorability=0.20, resonance=0.10, signal=0.16,
    ),
    penalties=PenaltyAdjustmentMap(),
    modality_profile=ModalitySupportProfile(
        modality_id="MOD-IMG-001",
        content_type=ContentType.SINGLE_IMAGE_POST,
        dimensions=[
            ModalityDimension(dimension_id="IMG-D1", dimension_name="screenshot_proof_quality", feeds_cluster="visual_proof", weight_in_cluster=0.4),
            ModalityDimension(dimension_id="IMG-D2", dimension_name="visual_authority_cues", feeds_cluster="visual_proof", weight_in_cluster=0.3),
            ModalityDimension(dimension_id="IMG-D3", dimension_name="visual_genericity_risk", feeds_cluster="ai_slop_risk", weight_in_cluster=0.2),
            ModalityDimension(dimension_id="IMG-D4", dimension_name="caption_image_coherence", feeds_cluster="caption_alignment", weight_in_cluster=0.4),
        ],
    ),
    rationale="Image posts are static. Signal, Trust, and Memorability dominate because the post must cut through feed noise with a single frame plus caption.",
)

CAROUSEL_BASELINE = ContentBenchmarkProfile(
    profile_id="CBP-CAR-001",
    content_type=ContentType.CAROUSEL,
    base_weights=VisibleScoreWeightMap(
        humanity=0.14, presence=0.10, trust=0.22,
        memorability=0.24, resonance=0.16, signal=0.14,
    ),
    penalties=PenaltyAdjustmentMap(),
    modality_profile=ModalitySupportProfile(
        modality_id="MOD-CAR-001",
        content_type=ContentType.CAROUSEL,
        dimensions=[
            ModalityDimension(dimension_id="CAR-D1", dimension_name="slide_sequence_logic", feeds_cluster="structure", weight_in_cluster=0.35),
            ModalityDimension(dimension_id="CAR-D2", dimension_name="frame_to_frame_proof_movement", feeds_cluster="structure", weight_in_cluster=0.25),
            ModalityDimension(dimension_id="CAR-D3", dimension_name="visual_narrative_progression", feeds_cluster="structure", weight_in_cluster=0.25),
            ModalityDimension(dimension_id="CAR-D4", dimension_name="caption_interaction", feeds_cluster="caption_alignment", weight_in_cluster=0.4),
        ],
    ),
    rationale="Carousels are sequential. Memorability and Trust dominate because carousels must reward swiping with proof progression.",
)

REEL_BASELINE = ContentBenchmarkProfile(
    profile_id="CBP-REEL-001",
    content_type=ContentType.REEL,
    base_weights=VisibleScoreWeightMap(
        humanity=0.20, presence=0.22, trust=0.12,
        memorability=0.18, resonance=0.18, signal=0.10,
    ),
    penalties=PenaltyAdjustmentMap(),
    modality_profile=ModalitySupportProfile(
        modality_id="MOD-REEL-001",
        content_type=ContentType.REEL,
        dimensions=[
            ModalityDimension(dimension_id="REEL-D1", dimension_name="script_semantic_density", feeds_cluster="structure", weight_in_cluster=0.25),
            ModalityDimension(dimension_id="REEL-D2", dimension_name="keyframe_quality", feeds_cluster="visual_proof", weight_in_cluster=0.2),
            ModalityDimension(dimension_id="REEL-D3", dimension_name="shot_transition_quality", feeds_cluster="temporal_craft", weight_in_cluster=0.3),
            ModalityDimension(dimension_id="REEL-D4", dimension_name="temporal_coherence", feeds_cluster="temporal_craft", weight_in_cluster=0.3),
            ModalityDimension(dimension_id="REEL-D5", dimension_name="pacing_rhythm", feeds_cluster="temporal_craft", weight_in_cluster=0.2),
            ModalityDimension(dimension_id="REEL-D6", dimension_name="caption_video_alignment", feeds_cluster="caption_alignment", weight_in_cluster=0.4),
            ModalityDimension(dimension_id="REEL-D7", dimension_name="discontinuity_absence", feeds_cluster="temporal_craft", weight_in_cluster=0.2),
        ],
    ),
    rationale="Reels are temporal. Presence and Humanity dominate because reels expose the speaker's embodied authority. Temporal Craft dimensions from OmniShotCut inform shot-transition quality and discontinuity detection.",
)
