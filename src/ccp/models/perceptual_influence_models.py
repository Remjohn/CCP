"""
FR-ERA3-27 — Perceptual Influence Models
========================================
Pydantic models, enums, and constants for the Perceptual Influence Evaluator.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ── Enums ──────────────────────────────────────────────────────────────

class PerceptualInfluenceDecision(str, Enum):
    PASS = "PASS"
    REVIEW = "REVIEW"
    DOWNGRADE = "DOWNGRADE"


class PerceptualInfluenceSurface(str, Enum):
    SEMANTIC_PLANNING = "SEMANTIC_PLANNING"
    RENDER_RELEASE = "RENDER_RELEASE"
    COMMERCIAL_TRUST_TRANSFER = "COMMERCIAL_TRUST_TRANSFER"
    SOCIAL_SHARE = "SOCIAL_SHARE"
    COACHING_INTERVENTION = "COACHING_INTERVENTION"
    INTERNAL_REVIEW = "INTERNAL_REVIEW"


class PerceptualInfluenceDomain(str, Enum):
    CCF = "CCF"
    CMF = "CMF"
    CBCS = "CBCS"
    REACTIONS = "REACTIONS"
    COMMERCIAL = "COMMERCIAL"
    WEBINAR = "WEBINAR"


class PerceptualInfluenceFallbackReason(str, Enum):
    MISSING_SFL_REGISTRY = "MISSING_SFL_REGISTRY"
    MISSING_DI_PREREQUISITE = "MISSING_DI_PREREQUISITE"
    MISSING_FUNCTION_STACK = "MISSING_FUNCTION_STACK"
    NULL_CANDIDATE = "NULL_CANDIDATE"
    CONTRADICTORY_METRICS = "CONTRADICTORY_METRICS"
    MISSING_POLICY = "MISSING_POLICY"
    MISSING_BRAND_POSTURE = "MISSING_BRAND_POSTURE"
    ANALYZER_CRASH = "ANALYZER_CRASH"


class PerceptualInfluenceResolutionPath(str, Enum):
    REGENERATE = "REGENERATE"
    OPERATOR_REVIEW = "OPERATOR_REVIEW"
    SURFACE_DOWNGRADE = "SURFACE_DOWNGRADE"
    ENRICH_SFL_STACK = "ENRICH_SFL_STACK"
    RESTORE_TENSION = "RESTORE_TENSION"


class PerceptualInfluenceDimension(str, Enum):
    COGNITIVE_IMPRINT = "COGNITIVE_IMPRINT"
    SYMBOLIC_DENSITY = "SYMBOLIC_DENSITY"
    HUMAN_CONGRUENCE = "HUMAN_CONGRUENCE"
    CONTRAST_CLARITY = "CONTRAST_CLARITY"
    MEMORABILITY_PRESSURE = "MEMORABILITY_PRESSURE"
    OVEREXPLANATION_RISK = "OVEREXPLANATION_RISK"
    SYNTHETIC_SMOOTHNESS = "SYNTHETIC_SMOOTHNESS"
    INFLUENCE_ALIGNMENT = "INFLUENCE_ALIGNMENT"


class PerceptualInfluenceSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"
    NONE = "NONE"


class FalseDepthClass(str, Enum):
    PERFORMATIVE_PROFUNDITY = "PERFORMATIVE_PROFUNDITY"
    DEAD_POLISH = "DEAD_POLISH"
    SYNTHETIC_AUTHORITY = "SYNTHETIC_AUTHORITY"
    EMPTY_MOTIVATIONAL_SMOOTHNESS = "EMPTY_MOTIVATIONAL_SMOOTHNESS"
    OVERRESOLVED_MEANING = "OVERRESOLVED_MEANING"


# ── Models ─────────────────────────────────────────────────────────────

class PerceptualEvidenceItem(BaseModel):
    evidence_id: str = Field(..., description="Unique ID for this evidence item")
    dimension: PerceptualInfluenceDimension
    observation: str = Field(..., description="What was observed in the candidate")
    rationale: str = Field(..., description="Why this observation matters for this dimension")
    contribution: float = Field(..., ge=-1.0, le=1.0, description="Signed contribution to dimension score")
    source_span: Optional[str] = Field(None, description="Text span or location in candidate that triggered this evidence")
    sfl_function_ref: Optional[str] = Field(None, description="SFL function ID if evidence relates to a specific function activation")


class PerceptualDimensionScore(BaseModel):
    dimension: PerceptualInfluenceDimension
    score: float = Field(..., ge=0.0, le=1.0, description="Normalized score for this dimension")
    severity: PerceptualInfluenceSeverity
    evidence: list[PerceptualEvidenceItem] = Field(default_factory=list)
    explanation: str = Field(..., description="Human-readable summary of the dimensional assessment")


class FalseDepthDetectionResult(BaseModel):
    detected: bool = Field(..., description="Whether any false-depth failure class was detected")
    detected_classes: list[FalseDepthClass] = Field(default_factory=list)
    evidence: list[PerceptualEvidenceItem] = Field(default_factory=list)
    severity: PerceptualInfluenceSeverity = PerceptualInfluenceSeverity.NONE
    explanation: str = ""


class BrandPostureContext(BaseModel):
    brand_posture_id: str
    authority_source: str = Field(..., description="earned, institutional, experiential, etc.")
    belonging_mode: str = Field(..., description="invitational, tribal, aspirational, etc.")
    identity_frame: str = Field(..., description="sovereign, collaborative, etc.")
    forbidden_influence_patterns: list[str] = Field(default_factory=list)
    permitted_influence_families: list[str] = Field(default_factory=list)


class InfluenceAlignmentResult(BaseModel):
    aligned: bool
    alignment_score: float = Field(..., ge=0.0, le=1.0)
    brand_posture_match: bool
    representation_geometry_match: bool
    archetype_match: bool
    surface_sensitivity_match: bool
    misalignment_details: list[str] = Field(default_factory=list)
    evidence: list[PerceptualEvidenceItem] = Field(default_factory=list)


class SFLFunctionStackSnapshot(BaseModel):
    stack_id: str
    active_families: list[str]
    active_functions: list[str]
    weight_profile: dict[str, float] = Field(default_factory=dict)
    intended_effects: list[str] = Field(default_factory=list)


class PerceptualInfluenceRequest(BaseModel):
    request_id: str
    domain: PerceptualInfluenceDomain
    surface_class: PerceptualInfluenceSurface
    actor_id: str
    coach_id: str
    candidate_text: str = Field(..., min_length=1, description="The artifact text to evaluate")
    sfl_function_stack: Optional[SFLFunctionStackSnapshot] = None
    brand_posture: Optional[BrandPostureContext] = None
    content_archetype_id: Optional[str] = None
    representation_geometry_id: Optional[str] = None
    directional_integrity_report_id: Optional[str] = Field(None, description="ID of the prerequisite DI report from FR-ERA3-22")
    directional_integrity_decision: Optional[str] = Field(None, description="DI decision: PASS, REVIEW, or FAIL")
    coalition_signature_id: Optional[str] = None
    edge_product_id: Optional[str] = None


class PerceptualInfluenceDecisionSummary(BaseModel):
    decision: PerceptualInfluenceDecision
    resolution_path: Optional[PerceptualInfluenceResolutionPath] = None
    required_corrections: list[str] = Field(default_factory=list)
    rationale: str = ""


class PerceptualInfluenceMetricBundle(BaseModel):
    cognitive_imprint_score: PerceptualDimensionScore
    symbolic_density_score: PerceptualDimensionScore
    human_congruence_score: PerceptualDimensionScore
    contrast_clarity_score: PerceptualDimensionScore
    memorability_pressure: PerceptualDimensionScore
    overexplanation_risk_score: PerceptualDimensionScore
    synthetic_smoothness_score: PerceptualDimensionScore


class PerceptualInfluenceReport(BaseModel):
    report_id: str = Field(..., description="Unique report ID, prefixed PIR-")
    request_id: str
    metric_bundle: PerceptualInfluenceMetricBundle
    influence_alignment: InfluenceAlignmentResult
    false_depth_result: FalseDepthDetectionResult
    decision_summary: PerceptualInfluenceDecisionSummary
    fallback_reason: Optional[PerceptualInfluenceFallbackReason] = None
    policy_id: str = Field(default="NONE", description="ID of the surface policy applied")
    di_prerequisite_report_id: Optional[str] = None
    di_prerequisite_decision: Optional[str] = None
    lineage_refs: list[str] = Field(default_factory=list, description="IDs of consumed artifacts: SFL stack, DI report, coalition, etc.")
    evaluated_at_utc: datetime = Field(default_factory=datetime.utcnow)


class PerceptualInfluenceEvaluatorResult(BaseModel):
    report: PerceptualInfluenceReport
    receipt_ids: list[str] = Field(default_factory=list)


class PerceptualInfluencePolicyBundle(BaseModel):
    policy_id: str
    domain: PerceptualInfluenceDomain
    surface_class: PerceptualInfluenceSurface
    pass_thresholds: dict[str, float] = Field(
        ...,
        description="Minimum positive-dimension scores for PASS. Keys are dimension names."
    )
    risk_ceilings: dict[str, float] = Field(
        ...,
        description="Maximum negative-dimension scores for PASS. Keys: overexplanation_risk, synthetic_smoothness."
    )
    influence_alignment_required: bool = True
    false_depth_blocks: bool = True
    missing_sfl_behavior: PerceptualInfluenceDecision = PerceptualInfluenceDecision.DOWNGRADE
    missing_di_behavior: PerceptualInfluenceDecision = PerceptualInfluenceDecision.DOWNGRADE
    notes: str = ""
