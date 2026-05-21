from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class RuntimeStatus(str, Enum):
    COMPILED = "compiled"
    REJECTED_ACTIONABLE = "rejected_actionable"
    BLOCKED_EVIDENCE_CONFLICT = "blocked_evidence_conflict"
    PENDING_RERECORD = "pending_rerecord"


class SimilarityBand(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    TERMINAL = "terminal"


class ArchetypeChoice(str, Enum):
    ARC_MYTH_DEBUNK = "ARC-MYTH-DEBUNK"
    ARC_ACHIEVEMENT_STORY = "ARC-ACH-STORY"
    ARC_OBSERVATIONAL_HUMOR = "ARC-OBS-HUMOR"
    ARC_WITNESS = "ARC-WITNESS"
    ARC_CONTRAST = "ARC-CONTRAST"
    ARC_COMP = "ARC-COMP"


class SentenceAuditRecord(BaseModel):
    sentence_id: str = Field(min_length=1)
    sentence_index: int = Field(ge=0)
    text: str = Field(min_length=1)
    start_offset: int = Field(ge=0)
    end_offset: int = Field(gt=0)
    hedge_hits: list[str] = Field(default_factory=list)
    named_specificity_hits: list[str] = Field(default_factory=list)
    similarity_score: float = Field(ge=0.0, le=1.0)
    similarity_band: SimilarityBand
    collapse_reason: str = Field(min_length=1)
    failed: bool = False


class CoalitionInputs(BaseModel):
    coalition_id: str = Field(min_length=1)
    family_mix: list[str] = Field(min_length=1)
    stance_polarity: str = Field(min_length=1)
    source_count: int = Field(ge=1)
    evidence_strength: float = Field(ge=0.0, le=1.0)
    intended_business_job: str = Field(min_length=1)


class CoachResponseCapturePacket(BaseModel):
    capture_id: str = Field(min_length=1)
    coach_id: str = Field(min_length=1)
    transcript_text: str = Field(min_length=1)
    transcript_language: str = Field(min_length=2, max_length=8)
    captured_at: datetime
    source_asset_id: str = Field(min_length=1)
    trigger_guard_session_id: str | None = None


class ContainerIntensityProfile(BaseModel):
    narrative_arc: str = Field(min_length=1)
    intensity_level: str = Field(min_length=1)
    pacing_profile: str = Field(min_length=1)
    emotional_job: str = Field(min_length=1)


class SflBindingStatus(str, Enum):
    SFL_BOUND = "sfl_bound"
    SFL_NOT_BOUND = "sfl_not_bound"
    SFL_PARTIAL = "sfl_partial"
    SFL_UNAVAILABLE = "sfl_unavailable"


class CompositionDepthClass(str, Enum):
    REPETITION_WITH_VARIATION = "repetition_with_variation"
    LAYERED_INTERPRETATION = "layered_interpretation"
    RHYTHMIC_STRUCTURE = "rhythmic_structure"
    STRATEGIC_AMBIGUITY = "strategic_ambiguity"


class SflFunctionBinding(BaseModel):
    function_id: str = Field(min_length=1, pattern=r"^SFL-FN-\d{3}$")
    family_id: str = Field(min_length=1, pattern=r"^SFL-FAM-\d{3}$")
    canonical_name: str = Field(min_length=1)
    polarity: str = Field(min_length=1)
    weight: float = Field(ge=0.0, le=1.0)
    binding_rationale: str = Field(min_length=1)


class SubliminalFunctionStackPacket(BaseModel):
    stack_id: str = Field(min_length=1)
    archetype_choice: ArchetypeChoice
    active_functions: list[SflFunctionBinding] = Field(min_length=1, max_length=8)
    crosswalk_source_id: str = Field(min_length=1)
    total_weight: float = Field(ge=0.0, le=1.0)
    binding_surface: str = Field(min_length=1)
    anti_bloat_check_passed: bool = True


class CompositionDepthPacket(BaseModel):
    depth_id: str = Field(min_length=1)
    depth_class: CompositionDepthClass
    intensity: float = Field(ge=0.0, le=1.0)
    cross_surface_applicable: bool = True
    governing_rationale: str = Field(min_length=1)


class VariationProfileBinding(BaseModel):
    variation_id: str = Field(min_length=1)
    asymmetry_target: float = Field(ge=0.0, le=1.0)
    resonance_spacing: float = Field(ge=0.0, le=1.0)
    predictability_break_threshold: float = Field(ge=0.0, le=1.0)
    paradox_retention: bool = False
    variation_rationale: str = Field(min_length=1)


class ArchetypeVariationDecision(BaseModel):
    decision_id: str = Field(min_length=1)
    archetype_choice: ArchetypeChoice
    applied_axes: list[str] = Field(min_length=1)
    variation_binding: VariationProfileBinding
    depth_class_influence: CompositionDepthClass
    decision_rationale: str = Field(min_length=1)


class ArchetypeSflExecutionContract(BaseModel):
    contract_id: str = Field(min_length=1)
    runtime_session_id: str = Field(min_length=1)
    archetype_choice: ArchetypeChoice
    structural_invariants: list[str] = Field(min_length=1)
    anti_draft_profile: list[str] = Field(min_length=1)
    sfl_function_stack: SubliminalFunctionStackPacket
    composition_depth: CompositionDepthPacket
    variation_binding: VariationProfileBinding
    intensity_profile: ContainerIntensityProfile
    coalition_family_mix: list[str] = Field(min_length=1)
    authorized_render_targets: list[str] = Field(min_length=1)
    dspy_signature_fields: dict[str, str] = Field(min_length=1)
    skill_execution_mode: str = Field(default="typed_dspy_module")


class ArchetypeContainerManifest(BaseModel):
    runtime_session_id: str = Field(min_length=1)
    container_id: str = Field(min_length=1)
    selected_archetype: ArchetypeChoice
    archetype_intent: str = Field(min_length=1)
    activation_condition_summary: str = Field(min_length=1)
    structural_invariants: list[str] = Field(min_length=1)
    anti_draft_profile: list[str] = Field(min_length=1)
    distillation_funnel: list[str] = Field(min_length=1)
    accepted_sentence_ids: list[str] = Field(min_length=1)
    coalition_inputs: CoalitionInputs
    intensity_profile: ContainerIntensityProfile
    cmf_render_hints: list[str] = Field(min_length=1)
    authorized_render_targets: list[str] = Field(min_length=1)
    created_at: datetime
    sfl_function_stack: SubliminalFunctionStackPacket | None = None
    composition_depth: CompositionDepthPacket | None = None
    variation_binding: VariationProfileBinding | None = None
    variation_decision: ArchetypeVariationDecision | None = None
    execution_contract: ArchetypeSflExecutionContract | None = None
    sfl_binding_status: SflBindingStatus = SflBindingStatus.SFL_NOT_BOUND


class ActionableRejectionPayload(BaseModel):
    runtime_session_id: str = Field(min_length=1)
    rejection_code: str = Field(min_length=1)
    similarity_score: float = Field(ge=0.0, le=1.0)
    similarity_band: SimilarityBand
    failing_sentence_ids: list[str] = Field(min_length=1)
    failing_sentences: list[str] = Field(min_length=1)
    collapse_reasons: list[str] = Field(min_length=1)
    coaching_fix: str = Field(min_length=1)
    rerecord_prompt: str = Field(min_length=1)
    trigger_guard_reroute_token: str | None = None
    trigger_guard_session_id: str | None = None


class CCFRoutingRecommendation(BaseModel):
    runtime_session_id: str = Field(min_length=1)
    coach_id: str = Field(min_length=1)
    status: RuntimeStatus
    selected_archetype: ArchetypeChoice | None = None
    container_manifest: ArchetypeContainerManifest | None = None
    rejection_payload: ActionableRejectionPayload | None = None
    downstream_family_targets: list[str] = Field(default_factory=list)
    downstream_system_targets: list[str] = Field(default_factory=list)
    receipt_chain_hash: str = Field(min_length=1)
    generated_at: datetime
    sfl_binding_status: SflBindingStatus = SflBindingStatus.SFL_NOT_BOUND
