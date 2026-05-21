from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Any, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict

class DirectionalIntegrityDecision(str, Enum):
    PASS = "PASS"
    REVIEW = "REVIEW"
    FAIL = "FAIL"

class DirectionalIntegritySurfaceClass(str, Enum):
    SEMANTIC_PLANNING = "SEMANTIC_PLANNING"
    RENDER_RELEASE = "RENDER_RELEASE"
    COACHING_INTERVENTION = "COACHING_INTERVENTION"
    SOCIAL_REACTION = "SOCIAL_REACTION"
    LONG_FORM_AUTHORITY = "LONG_FORM_AUTHORITY"
    COMMERCIAL_TRUST_TRANSFER = "COMMERCIAL_TRUST_TRANSFER"

class DirectionalIntegritySeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    BLOCKING = "BLOCKING"

class DirectionalIntegrityResolutionPath(str, Enum):
    CONTINUE = "CONTINUE"
    REGENERATE = "REGENERATE"
    OPERATOR_REVIEW = "OPERATOR_REVIEW"
    HARD_BLOCK = "HARD_BLOCK"
    CIRCUIT_BREAK = "CIRCUIT_BREAK"

class DirectionalIntegrityFallbackReason(str, Enum):
    NONE = "NONE"
    MISSING_POLICY = "MISSING_POLICY"
    MISSING_ONTOLOGY = "MISSING_ONTOLOGY"
    MISSING_CROSSWALK = "MISSING_CROSSWALK"
    MISSING_HARD_NEGATIVE_SERVICE = "MISSING_HARD_NEGATIVE_SERVICE"
    NULL_RUNTIME_PACKET = "NULL_RUNTIME_PACKET"
    SDA_QUERY_DEGRADED = "SDA_QUERY_DEGRADED"
    INTERNAL_ANALYZER_ERROR = "INTERNAL_ANALYZER_ERROR"

class DirectionalIntegrityDomain(str, Enum):
    CCF = "CCF"
    CMF = "CMF"
    CBCS = "CBCS"
    REACTIONS = "REACTIONS"
    WEBINAR = "WEBINAR"
    COMMERCIAL = "COMMERCIAL"

class DirectionalIntegrityDimension(str, Enum):
    INVARIANT_PRESERVATION = "INVARIANT_PRESERVATION"
    REPRESENTATION_DRIFT = "REPRESENTATION_DRIFT"
    HARD_NEGATIVE_ADJACENCY = "HARD_NEGATIVE_ADJACENCY"
    TRAJECTORY_RISK = "TRAJECTORY_RISK"

class DirectionalIntegrityArtifactRef(BaseModel):
    model_config = ConfigDict(extra="forbid")
    artifact_id: str = Field(..., min_length=3)
    artifact_kind: str = Field(..., min_length=3)
    artifact_path: Optional[str] = None
    artifact_hash: Optional[str] = None

class DirectionalIntegrityEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid")
    evidence_id: str
    source_kind: Literal["invariant_field","archetypal_geometry","representation_geometry","species_hypothesis","candidate_text","candidate_media","crosswalk_resolution","hard_negative","policy_rule","operator_note"]
    summary: str
    cited_values: dict[str, Any] = Field(default_factory=dict)
    artifact_ref: Optional[DirectionalIntegrityArtifactRef] = None

class DirectionalIntegrityDimensionScore(BaseModel):
    model_config = ConfigDict(extra="forbid")
    dimension: DirectionalIntegrityDimension
    score: float = Field(..., ge=0.0, le=1.0)
    severity: DirectionalIntegritySeverity
    threshold_warning: float = Field(..., ge=0.0, le=1.0)
    threshold_block: float = Field(..., ge=0.0, le=1.0)
    rationale: str
    evidence: list[DirectionalIntegrityEvidence] = Field(default_factory=list)
    blocking: bool = False

class InvariantFieldPacket(BaseModel):
    model_config = ConfigDict(extra="forbid")
    packet_id: str
    primary_invariant_ids: list[str] = Field(default_factory=list)
    secondary_invariant_ids: list[str] = Field(default_factory=list)
    invariant_activation_intensity: dict[str, float] = Field(default_factory=dict)
    invariant_resonance_multiplier_hint: Optional[dict[str, float]] = None
    source_evidence: list[DirectionalIntegrityEvidence] = Field(default_factory=list)

class ArchetypalGeometryPacket(BaseModel):
    model_config = ConfigDict(extra="forbid")
    packet_id: str
    geometry_id: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    required_preservations: list[str] = Field(default_factory=list)
    forbidden_drifts: list[str] = Field(default_factory=list)
    source_evidence: list[DirectionalIntegrityEvidence] = Field(default_factory=list)

class RepresentationGeometryPacket(BaseModel):
    model_config = ConfigDict(extra="forbid")
    packet_id: str
    representation_geometry_id: str
    authority_source: Optional[str] = None
    belonging_mode: Optional[str] = None
    identity_frame: Optional[str] = None
    coercion_risk_budget: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    forbidden_drifts: list[str] = Field(default_factory=list)
    source_evidence: list[DirectionalIntegrityEvidence] = Field(default_factory=list)

class SpeciesHypothesisPacket(BaseModel):
    model_config = ConfigDict(extra="forbid")
    packet_id: str
    species_label: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    derivation_refs: list[str] = Field(default_factory=list)
    shadow_drifts: list[str] = Field(default_factory=list)

class HardNegativeCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    hard_negative_id: str
    adjacency_score: float = Field(..., ge=0.0, le=1.0)
    divergence_axes: list[str] = Field(default_factory=list)
    failure_reason: str
    evidence: list[DirectionalIntegrityEvidence] = Field(default_factory=list)

class HardNegativeEvaluationReport(BaseModel):
    model_config = ConfigDict(extra="forbid")
    report_id: str
    top_matches: list[HardNegativeCandidate] = Field(default_factory=list)
    strongest_adjacency_score: float = Field(..., ge=0.0, le=1.0)
    blocked_by_hard_negative: bool = False
    fallback_reason: DirectionalIntegrityFallbackReason = DirectionalIntegrityFallbackReason.NONE

class DirectionalIntegrityPolicyRule(BaseModel):
    model_config = ConfigDict(extra="forbid")
    rule_id: str
    dimension: DirectionalIntegrityDimension
    warning_threshold: float = Field(..., ge=0.0, le=1.0)
    block_threshold: float = Field(..., ge=0.0, le=1.0)
    applies_to_surface: DirectionalIntegritySurfaceClass
    applies_to_domain: DirectionalIntegrityDomain
    description: str

class DirectionalIntegrityPolicyBundle(BaseModel):
    model_config = ConfigDict(extra="forbid")
    policy_id: str
    domain: DirectionalIntegrityDomain
    surface_class: DirectionalIntegritySurfaceClass
    version: str
    fail_closed: bool = True
    rules: list[DirectionalIntegrityPolicyRule]
    review_if_dependency_degraded: bool = True
    block_if_dependency_degraded: bool = True
    notes: Optional[str] = None

class DirectionalIntegrityRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    request_id: str
    domain: DirectionalIntegrityDomain
    surface_class: DirectionalIntegritySurfaceClass
    actor_id: str
    coach_id: Optional[str] = None
    content_archetype: Optional[str] = None
    edge_product_label: Optional[str] = None
    candidate_text: Optional[str] = None
    candidate_media_refs: list[DirectionalIntegrityArtifactRef] = Field(default_factory=list)
    invariant_field: InvariantFieldPacket
    archetypal_geometry: ArchetypalGeometryPacket
    representation_geometry: RepresentationGeometryPacket
    species_hypothesis: Optional[SpeciesHypothesisPacket] = None
    metadata: dict[str, Any] = Field(default_factory=dict)

class DirectionalIntegrityDecisionSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")
    decision: DirectionalIntegrityDecision
    resolution_path: DirectionalIntegrityResolutionPath
    blocking: bool
    advisory_only: bool
    summary: str

class DirectionalIntegrityReport(BaseModel):
    model_config = ConfigDict(extra="forbid")
    report_id: str
    request_id: str
    domain: DirectionalIntegrityDomain
    surface_class: DirectionalIntegritySurfaceClass
    policy_id: str
    evaluated_at_utc: datetime
    decision_summary: DirectionalIntegrityDecisionSummary
    invariant_preservation_score: DirectionalIntegrityDimensionScore
    representation_drift_score: DirectionalIntegrityDimensionScore
    hard_negative_adjacency_score: DirectionalIntegrityDimensionScore
    trajectory_risk_score: DirectionalIntegrityDimensionScore
    overall_confidence: float = Field(..., ge=0.0, le=1.0)
    invariant_resonance_multiplier: dict[str, float] = Field(default_factory=dict)
    symbolic_density: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    identity_proximity: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    hard_negative_report: Optional[HardNegativeEvaluationReport] = None
    fallback_reason: DirectionalIntegrityFallbackReason = DirectionalIntegrityFallbackReason.NONE
    dependency_warnings: list[str] = Field(default_factory=list)
    required_corrections: list[str] = Field(default_factory=list)
    lineage_refs: list[str] = Field(default_factory=list)

class DirectionalIntegrityEngineResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    report: DirectionalIntegrityReport
    should_continue_automation: bool
    should_queue_operator_review: bool
    should_trigger_regeneration: bool
    should_trip_circuit_break: bool


# ── SFL Interop Models ──

class PerceptualInteropDecision(str, Enum):
    PASS = "PASS"
    REVIEW = "REVIEW"
    DOWNGRADE = "DOWNGRADE"
    BLOCK = "BLOCK"
    MISSING = "MISSING"


class SemanticVsPerceptualDecisionState(str, Enum):
    SEMANTIC_PASS__PERCEPTUAL_PASS = "SEMANTIC_PASS__PERCEPTUAL_PASS"
    SEMANTIC_PASS__PERCEPTUAL_REVIEW = "SEMANTIC_PASS__PERCEPTUAL_REVIEW"
    SEMANTIC_PASS__PERCEPTUAL_DOWNGRADE = "SEMANTIC_PASS__PERCEPTUAL_DOWNGRADE"
    SEMANTIC_PASS__PERCEPTUAL_BLOCK = "SEMANTIC_PASS__PERCEPTUAL_BLOCK"
    SEMANTIC_PASS__PERCEPTUAL_MISSING = "SEMANTIC_PASS__PERCEPTUAL_MISSING"
    SEMANTIC_REVIEW__PERCEPTUAL_PASS = "SEMANTIC_REVIEW__PERCEPTUAL_PASS"
    SEMANTIC_REVIEW__PERCEPTUAL_REVIEW = "SEMANTIC_REVIEW__PERCEPTUAL_REVIEW"
    SEMANTIC_REVIEW__PERCEPTUAL_DOWNGRADE = "SEMANTIC_REVIEW__PERCEPTUAL_DOWNGRADE"
    SEMANTIC_REVIEW__PERCEPTUAL_BLOCK = "SEMANTIC_REVIEW__PERCEPTUAL_BLOCK"
    SEMANTIC_REVIEW__PERCEPTUAL_MISSING = "SEMANTIC_REVIEW__PERCEPTUAL_MISSING"
    SEMANTIC_FAIL__PERCEPTUAL_PASS = "SEMANTIC_FAIL__PERCEPTUAL_PASS"
    SEMANTIC_FAIL__PERCEPTUAL_REVIEW = "SEMANTIC_FAIL__PERCEPTUAL_REVIEW"
    SEMANTIC_FAIL__PERCEPTUAL_DOWNGRADE = "SEMANTIC_FAIL__PERCEPTUAL_DOWNGRADE"
    SEMANTIC_FAIL__PERCEPTUAL_BLOCK = "SEMANTIC_FAIL__PERCEPTUAL_BLOCK"
    SEMANTIC_FAIL__PERCEPTUAL_MISSING = "SEMANTIC_FAIL__PERCEPTUAL_MISSING"


class JointRoutingAction(str, Enum):
    CONTINUE = "CONTINUE"
    REGENERATE = "REGENERATE"
    OPERATOR_REVIEW = "OPERATOR_REVIEW"
    DOWNGRADE_SURFACE = "DOWNGRADE_SURFACE"
    HOLD_FOR_PERCEPTUAL_PREREQUISITE = "HOLD_FOR_PERCEPTUAL_PREREQUISITE"
    HARD_BLOCK = "HARD_BLOCK"
    CIRCUIT_BREAK = "CIRCUIT_BREAK"


class JointFailureClass(str, Enum):
    NONE = "NONE"
    SEMANTIC_FAILURE = "SEMANTIC_FAILURE"
    PERCEPTUAL_FAILURE = "PERCEPTUAL_FAILURE"
    MIXED_FAILURE = "MIXED_FAILURE"
    MISSING_PERCEPTUAL_PREREQUISITE = "MISSING_PERCEPTUAL_PREREQUISITE"


class PerceptualAttachmentSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")
    perceptual_report_id: str = Field(..., min_length=3)
    perceptual_decision: PerceptualInteropDecision = Field(...)
    human_congruence_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    cognitive_imprint_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    false_depth_detected: bool = Field(default=False)
    dead_polish_detected: bool = Field(default=False)
    dependency_warnings: list[str] = Field(default_factory=list)
    required_corrections: list[str] = Field(default_factory=list)
    lineage_refs: list[str] = Field(default_factory=list)


class JointFailureSurface(BaseModel):
    model_config = ConfigDict(extra="forbid")
    failure_class: JointFailureClass = Field(...)
    combined_state: SemanticVsPerceptualDecisionState = Field(...)
    semantic_failure_present: bool = Field(...)
    perceptual_failure_present: bool = Field(...)
    missing_perceptual_prerequisite: bool = Field(...)
    summary: str = Field(..., min_length=1)
    blocking_reasons: list[str] = Field(default_factory=list)
    required_corrections: list[str] = Field(default_factory=list)


class JointValidatorRoutingDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action: JointRoutingAction = Field(...)
    should_continue_automation: bool = Field(...)
    should_queue_operator_review: bool = Field(...)
    should_trigger_regeneration: bool = Field(...)
    should_trip_circuit_break: bool = Field(...)
    explanation: str = Field(..., min_length=1)


class DirectionalIntegrityInteropReport(BaseModel):
    model_config = ConfigDict(extra="forbid")
    interop_report_id: str = Field(..., min_length=3)
    semantic_report_id: str = Field(..., min_length=3)
    semantic_decision: str = Field(..., min_length=3)
    combined_state: SemanticVsPerceptualDecisionState = Field(...)
    semantic_report_generated_at_utc: datetime = Field(...)
    perceptual_attachment: Optional[PerceptualAttachmentSummary] = Field(default=None)
    failure_surface: JointFailureSurface = Field(...)
    routing_decision: JointValidatorRoutingDecision = Field(...)
    lineage_refs: list[str] = Field(default_factory=list)
    dependency_warnings: list[str] = Field(default_factory=list)

