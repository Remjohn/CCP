"""
FR-ERA3-35 Phase-0 Audit Intelligence Engine Models
=====================================================
Canonical Pydantic v2 schemas and enums for Phase-0 Audit Intelligence.
"""

from __future__ import annotations

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, model_validator


# ── Enums ──────────────────────────────────────────────────────────────

class AuditSeverity(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class AuditTargetContentType(str, Enum):
    SINGLE_IMAGE_CAPTION = "single_image_caption"
    CAROUSEL_CAPTION = "carousel_caption"
    REEL_CAPTION = "reel_caption"


class BridgeTierRecommendation(str, Enum):
    PROOF_UNLOCK_2999 = "proof_unlock_2999"
    SPEAKING_LEARNING_3999 = "speaking_learning_3999"
    COACH_OS_9999 = "coach_os_9999"


class ForecastDirection(str, Enum):
    IMPROVING = "improving"
    FLAT = "flat"
    DEGRADING = "degrading"


class VideoStructureAvailability(str, Enum):
    UNAVAILABLE = "unavailable"
    HEURISTIC = "heuristic"
    SEGMENTED = "segmented"


# ── Models ─────────────────────────────────────────────────────────────

class VisibleScoreSnapshot(BaseModel):
    """Canonical visible scores mapped to phase0_eval_card_scoring_model_v_1."""
    humanity: int = Field(..., ge=0, le=99)
    presence: int = Field(..., ge=0, le=99)
    trust: int = Field(..., ge=0, le=99)
    memorability: int = Field(..., ge=0, le=99)
    resonance: int = Field(..., ge=0, le=99)
    signal: int = Field(..., ge=0, le=99)
    ai_slop_risk: int = Field(..., ge=0, le=99)


class AuditFinding(BaseModel):
    finding_id: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    severity: AuditSeverity = Field(...)
    description: str = Field(..., min_length=1)
    evidence_summary: str = Field(..., min_length=1)


class DamageIndex(BaseModel):
    overall_damage_score: int = Field(..., ge=0, le=99)
    authority_dilution_score: int = Field(..., ge=0, le=99)
    memorability_weakness_score: int = Field(..., ge=0, le=99)
    proof_weakness_score: int = Field(..., ge=0, le=99)
    humanity_weakness_score: int = Field(..., ge=0, le=99)
    genericity_blending_score: int = Field(..., ge=0, le=99)
    experiential_deficit_score: int = Field(..., ge=0, le=99)
    speaking_gap_score: int = Field(..., ge=0, le=99)
    reaction_gap_score: int = Field(..., ge=0, le=99)
    explanation: str = Field(..., min_length=1)


class CompoundingForecast(BaseModel):
    direction: ForecastDirection = Field(...)
    thirty_day_risk_score: int = Field(..., ge=0, le=99, alias="30_day_risk_score")
    ninety_day_risk_score: int = Field(..., ge=0, le=99, alias="90_day_risk_score")
    trust_decay_risk: int = Field(..., ge=0, le=99)
    authority_decay_risk: int = Field(..., ge=0, le=99)
    invisibility_risk: int = Field(..., ge=0, le=99)
    summary: str = Field(..., min_length=1)

    class Config:
        populate_by_name = True


class StrengthReinforcementBlock(BaseModel):
    retained_strengths: List[str] = Field(default_factory=list)
    why_they_work: List[str] = Field(default_factory=list)
    preserve_instructions: List[str] = Field(default_factory=list)
    reinforcement_summary: str = Field(..., min_length=1)


class PrescriptionBlock(BaseModel):
    primary_shift: str = Field(..., min_length=1)
    supporting_shifts: List[str] = Field(default_factory=list)
    speaking_improvement_path: List[str] = Field(default_factory=list)
    reaction_improvement_path: List[str] = Field(default_factory=list)
    content_improvement_path: List[str] = Field(default_factory=list)
    why_now: str = Field(..., min_length=1)


class ProofOfPrescriptionBlock(BaseModel):
    proof_summary: str = Field(..., min_length=1)
    transformed_asset_refs: List[str] = Field(default_factory=list)
    scoring_card_refs: List[str] = Field(default_factory=list)
    before_after_claim: str = Field(..., min_length=1)
    confidence_score: int = Field(..., ge=0, le=99)


class ContinuityBridgeRecommendation(BaseModel):
    recommended_tier: BridgeTierRecommendation = Field(...)
    reason: str = Field(..., min_length=1)
    ladder_copy: str = Field(..., min_length=1)
    upgrade_credit_note: str = Field(default="")
    next_best_action: str = Field(..., min_length=1)


class AuditTargetDescriptor(BaseModel):
    audit_target_id: str = Field(..., min_length=1)
    prospect_id: str = Field(..., min_length=1)
    content_type: AuditTargetContentType = Field(...)
    primary_media_source_ids: List[str] = Field(default_factory=list)
    caption_id: Optional[str] = Field(default=None)
    platform_hint: Optional[str] = Field(default=None)
    archetype_hint: Optional[str] = Field(default=None)
    content_url: Optional[str] = Field(default=None)


class CaptionAuditBlock(BaseModel):
    visible_scores: VisibleScoreSnapshot = Field(...)
    key_findings: List[AuditFinding] = Field(default_factory=list)
    caption_alignment_notes: List[str] = Field(default_factory=list)
    proof_language_notes: List[str] = Field(default_factory=list)
    genericity_notes: List[str] = Field(default_factory=list)
    summary: str = Field(..., min_length=1)


class SingleImageAuditBlock(BaseModel):
    visible_scores: VisibleScoreSnapshot = Field(...)
    key_findings: List[AuditFinding] = Field(default_factory=list)
    visual_authority_notes: List[str] = Field(default_factory=list)
    proof_density_notes: List[str] = Field(default_factory=list)
    image_caption_coherence_notes: List[str] = Field(default_factory=list)
    summary: str = Field(..., min_length=1)


class CarouselAuditBlock(BaseModel):
    visible_scores: VisibleScoreSnapshot = Field(...)
    key_findings: List[AuditFinding] = Field(default_factory=list)
    sequencing_notes: List[str] = Field(default_factory=list)
    frame_to_frame_logic_notes: List[str] = Field(default_factory=list)
    caption_interaction_notes: List[str] = Field(default_factory=list)
    summary: str = Field(..., min_length=1)


class VideoStructureAuditBlock(BaseModel):
    availability: VideoStructureAvailability = Field(...)
    hook_retention_score: int = Field(..., ge=0, le=99)
    pacing_coherence_score: int = Field(..., ge=0, le=99)
    shot_transition_coherence_score: int = Field(..., ge=0, le=99)
    temporal_salience_score: int = Field(..., ge=0, le=99)
    structure_notes: List[str] = Field(default_factory=list)
    fallback_mode_reason: str = Field(default="")


class ReelAuditBlock(BaseModel):
    visible_scores: VisibleScoreSnapshot = Field(...)
    key_findings: List[AuditFinding] = Field(default_factory=list)
    script_semantic_notes: List[str] = Field(default_factory=list)
    key_frame_notes: List[str] = Field(default_factory=list)
    caption_video_alignment_notes: List[str] = Field(default_factory=list)
    video_structure: VideoStructureAuditBlock = Field(...)
    summary: str = Field(..., min_length=1)


class AuditIntelligenceReport(BaseModel):
    report_id: str = Field(..., min_length=1)
    prospect_id: str = Field(..., min_length=1)
    coach_id: Optional[str] = Field(default=None)
    audit_target: AuditTargetDescriptor = Field(...)
    visible_scores: VisibleScoreSnapshot = Field(...)
    damage_index: DamageIndex = Field(...)
    compounding_forecast: CompoundingForecast = Field(...)
    strength_reinforcement: StrengthReinforcementBlock = Field(...)
    prescription: PrescriptionBlock = Field(...)
    proof_of_prescription: ProofOfPrescriptionBlock = Field(...)
    continuity_bridge: ContinuityBridgeRecommendation = Field(...)
    caption_block: CaptionAuditBlock = Field(...)
    single_image_block: Optional[SingleImageAuditBlock] = Field(default=None)
    carousel_block: Optional[CarouselAuditBlock] = Field(default=None)
    reel_block: Optional[ReelAuditBlock] = Field(default=None)
    operator_summary: str = Field(..., min_length=1)
    participant_summary: str = Field(..., min_length=1)
    receipt_ids: List[str] = Field(default_factory=list)
    
    # Metadata for fallback adapters
    provisional_upstream_contract: bool = Field(default=False)

    @model_validator(mode="after")
    def validate_modality_blocks(self) -> AuditIntelligenceReport:
        content_type = self.audit_target.content_type
        
        # Check single_image modality alignment
        if content_type == AuditTargetContentType.SINGLE_IMAGE_CAPTION:
            if self.single_image_block is None:
                raise ValueError("single_image_block is required for SINGLE_IMAGE_CAPTION")
            if self.carousel_block is not None or self.reel_block is not None:
                raise ValueError("Only single_image_block may be populated for SINGLE_IMAGE_CAPTION")
                
        # Check carousel modality alignment
        elif content_type == AuditTargetContentType.CAROUSEL_CAPTION:
            if self.carousel_block is None:
                raise ValueError("carousel_block is required for CAROUSEL_CAPTION")
            if self.single_image_block is not None or self.reel_block is not None:
                raise ValueError("Only carousel_block may be populated for CAROUSEL_CAPTION")
                
        # Check reel modality alignment
        elif content_type == AuditTargetContentType.REEL_CAPTION:
            if self.reel_block is None:
                raise ValueError("reel_block is required for REEL_CAPTION")
            if self.single_image_block is not None or self.carousel_block is not None:
                raise ValueError("Only reel_block may be populated for REEL_CAPTION")
                
        return self


class PdfAuditPayload(BaseModel):
    report_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    cover_thumbnail_asset_id: Optional[str] = Field(default=None)
    visible_scores: VisibleScoreSnapshot = Field(...)
    card_refs: List[str] = Field(default_factory=list)
    sections: List[str] = Field(default_factory=list)
    summary_copy: str = Field(..., min_length=1)
    render_template_key: str = Field(..., min_length=1)


class ExplainerAuditVideoPayload(BaseModel):
    report_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    visible_scores: VisibleScoreSnapshot = Field(...)
    card_refs: List[str] = Field(default_factory=list)
    scene_script_blocks: List[str] = Field(default_factory=list)
    voiceover_script: str = Field(..., min_length=1)
    avatar_ref_id: Optional[str] = Field(default=None)
    render_template_key: str = Field(..., min_length=1)
