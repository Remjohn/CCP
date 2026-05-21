"""
FR-ERA3-28 - Perceptual Failure Corpus and Contrast Harness models.

Typed contracts for perceptual failure cases, mutation suites, probe requests,
and harness reports used by the SFL adversarial corpus layer.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class PerceptualFailureClass(str, Enum):
    FALSE_DEPTH = "false_depth"
    DEAD_POLISH = "dead_polish"
    SYNTHETIC_AUTHORITY = "synthetic_authority"
    OVERRESOLVED_MEANING = "overresolved_meaning"
    EMPTY_MOTIVATIONAL_SMOOTHNESS = "empty_motivational_smoothness"


class MutationOperatorKind(str, Enum):
    OVER_SMOOTHING = "OVER_SMOOTHING"
    IMPLICATION_STRIPPING = "IMPLICATION_STRIPPING"
    SYMBOLIC_FLATTENING = "SYMBOLIC_FLATTENING"
    RHYTHM_NORMALIZATION = "RHYTHM_NORMALIZATION"
    PROOF_INFLATION = "PROOF_INFLATION"
    PRESTIGE_THEATER_INJECTION = "PRESTIGE_THEATER_INJECTION"
    MOTIVATIONAL_SOFTENING = "MOTIVATIONAL_SOFTENING"
    PAUSE_WEIGHT_REMOVAL = "PAUSE_WEIGHT_REMOVAL"


class PerceptualExpectationStatus(str, Enum):
    EXPECT_DOWNGRADE = "EXPECT_DOWNGRADE"
    EXPECT_REVIEW = "EXPECT_REVIEW"
    EXPECT_BLOCK = "EXPECT_BLOCK"
    EXPECT_WARNING = "EXPECT_WARNING"


class PerceptualHarnessDecision(str, Enum):
    PASS = "PASS"
    REVIEW = "REVIEW"
    DOWNGRADE = "DOWNGRADE"
    BLOCK = "BLOCK"
    INVALID = "INVALID"
    ERROR = "ERROR"


class PerceptualSurfaceClass(str, Enum):
    SEMANTIC_PLANNING = "SEMANTIC_PLANNING"
    RENDER_RELEASE = "RENDER_RELEASE"
    COACHING_INTERVENTION = "COACHING_INTERVENTION"
    SOCIAL_REACTION = "SOCIAL_REACTION"
    LONG_FORM_AUTHORITY = "LONG_FORM_AUTHORITY"
    COMMERCIAL_TRUST_TRANSFER = "COMMERCIAL_TRUST_TRANSFER"
    PHASE0_AUDIT_PROOF = "PHASE0_AUDIT_PROOF"


class FailureLabelBundle(BaseModel):
    model_config = ConfigDict(extra="forbid")

    primary_label: str = Field(..., min_length=3, max_length=80)
    public_label: str = Field(..., min_length=3, max_length=80)
    short_badge: str = Field(..., min_length=2, max_length=32)
    failure_class: PerceptualFailureClass
    descriptor_tags: list[str] = Field(default_factory=list)
    symptom_markers: list[str] = Field(default_factory=list)
    remediation_markers: list[str] = Field(default_factory=list)


class EvaluatorExpectationBundle(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expected_status: PerceptualExpectationStatus
    minimum_human_congruence_drop: float = Field(..., ge=0.0, le=1.0)
    minimum_memorability_drop: float = Field(..., ge=0.0, le=1.0)
    minimum_symbolic_density_drop: float = Field(..., ge=0.0, le=1.0)
    minimum_contrast_clarity_drop: float = Field(..., ge=0.0, le=1.0)
    minimum_overexplanation_risk_rise: float = Field(..., ge=0.0, le=1.0)
    minimum_synthetic_smoothness_rise: float = Field(..., ge=0.0, le=1.0)
    route_block_surfaces: list[PerceptualSurfaceClass] = Field(default_factory=list)
    route_review_surfaces: list[PerceptualSurfaceClass] = Field(default_factory=list)
    rationale: str = Field(..., min_length=20, max_length=800)


class SemanticInteropReference(BaseModel):
    model_config = ConfigDict(extra="forbid")

    linked_hard_negative_ids: list[str] = Field(default_factory=list)
    linked_invariant_ids: list[str] = Field(default_factory=list)
    linked_geometry_ids: list[str] = Field(default_factory=list)
    ownership_statement: str = Field(
        default="Semantic hard negatives remain owned by FR-ERA3-24; this object only references them."
    )

    @field_validator("linked_hard_negative_ids", "linked_invariant_ids", "linked_geometry_ids", mode="before")
    @classmethod
    def _normalize_reference_lists(cls, value: Any) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [value]
        if isinstance(value, tuple | set):
            return [str(item) for item in value]
        if isinstance(value, list):
            normalized: list[str] = []
            for item in value:
                if isinstance(item, dict):
                    raise ValueError("Semantic interop references must remain IDs only; inline semantic objects are forbidden.")
                normalized.append(str(item))
            return normalized
        raise ValueError("Semantic interop reference fields must be sequences of string IDs.")

    @model_validator(mode="after")
    def _validate_reference_only(self) -> "SemanticInteropReference":
        ownership_text = self.ownership_statement.lower()
        if "fr-era3-24" not in ownership_text or "reference" not in ownership_text:
            raise ValueError("ownership_statement must explicitly preserve FR-ERA3-24 ownership and reference-only semantics.")
        for hard_negative_id in self.linked_hard_negative_ids:
            if not hard_negative_id.startswith("HN-"):
                raise ValueError("linked_hard_negative_ids must contain canonical FR-ERA3-24 hard-negative IDs.")
        for invariant_id in self.linked_invariant_ids:
            if not invariant_id.startswith("INV-"):
                raise ValueError("linked_invariant_ids must contain invariant IDs only.")
        for geometry_id in self.linked_geometry_ids:
            if not geometry_id.startswith("SDA-"):
                raise ValueError("linked_geometry_ids must contain SDA geometry IDs only.")
        return self


class PerceptualMutationOperation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(..., pattern=r"^PMO-[A-Z0-9-]{4,64}$")
    kind: MutationOperatorKind
    label: str = Field(..., min_length=3, max_length=120)
    description: str = Field(..., min_length=20, max_length=800)
    severity: float = Field(..., ge=0.0, le=1.0)
    config: dict[str, Any] = Field(default_factory=dict)


class PerceptualMutationSuite(BaseModel):
    model_config = ConfigDict(extra="forbid")

    suite_id: str = Field(..., pattern=r"^PMS-[A-Z0-9-]{4,64}$")
    label: str = Field(..., min_length=3, max_length=120)
    target_failure_class: PerceptualFailureClass
    target_surfaces: list[PerceptualSurfaceClass] = Field(default_factory=list)
    operations: list[PerceptualMutationOperation] = Field(..., min_length=1)
    expectation_bundle: EvaluatorExpectationBundle
    notes: Optional[str] = Field(default=None, max_length=800)

    @model_validator(mode="after")
    def _validate_operations(self) -> "PerceptualMutationSuite":
        operation_ids = [operation.operation_id for operation in self.operations]
        if len(operation_ids) != len(set(operation_ids)):
            raise ValueError("Mutation suites cannot contain duplicate operation IDs.")
        return self


class PerceptualContrastCaseRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str = Field(..., pattern=r"^PFC-[A-Z0-9-]{4,64}$")
    failure_class: PerceptualFailureClass
    title: str = Field(..., min_length=5, max_length=160)
    summary: str = Field(..., min_length=30, max_length=1000)
    labels: FailureLabelBundle
    source_surface: PerceptualSurfaceClass
    source_archetype_ids: list[str] = Field(default_factory=list)
    source_function_family_ids: list[str] = Field(default_factory=list)
    valid_anchor_excerpt: str = Field(..., min_length=30, max_length=2500)
    failing_variant_excerpt: str = Field(..., min_length=30, max_length=2500)
    why_it_fails: list[str] = Field(..., min_length=1)
    what_it_fake_signals: list[str] = Field(default_factory=list)
    what_it_erases: list[str] = Field(default_factory=list)
    expectation_bundle: EvaluatorExpectationBundle
    semantic_interop: SemanticInteropReference = Field(default_factory=SemanticInteropReference)
    mutation_suite_ids: list[str] = Field(default_factory=list)
    maintained: bool = Field(default=True)
    version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$")

    @model_validator(mode="after")
    def _validate_case_integrity(self) -> "PerceptualContrastCaseRecord":
        if self.labels.failure_class != self.failure_class:
            raise ValueError("FailureLabelBundle.failure_class must match case failure_class.")
        if len(self.mutation_suite_ids) != len(set(self.mutation_suite_ids)):
            raise ValueError("mutation_suite_ids must be unique per case.")
        if not self.why_it_fails:
            raise ValueError("Perceptual contrast cases must define at least one failure rationale.")
        return self


class FalseDepthContrastCase(PerceptualContrastCaseRecord):
    failure_class: PerceptualFailureClass = Field(default=PerceptualFailureClass.FALSE_DEPTH)


class DeadPolishContrastCase(PerceptualContrastCaseRecord):
    failure_class: PerceptualFailureClass = Field(default=PerceptualFailureClass.DEAD_POLISH)


class SyntheticAuthorityContrastCase(PerceptualContrastCaseRecord):
    failure_class: PerceptualFailureClass = Field(default=PerceptualFailureClass.SYNTHETIC_AUTHORITY)


class OverresolvedMeaningCase(PerceptualContrastCaseRecord):
    failure_class: PerceptualFailureClass = Field(default=PerceptualFailureClass.OVERRESOLVED_MEANING)


class EmptyMotivationalSmoothnessCase(PerceptualContrastCaseRecord):
    failure_class: PerceptualFailureClass = Field(default=PerceptualFailureClass.EMPTY_MOTIVATIONAL_SMOOTHNESS)


class PerceptualFailureCorpusManifest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    manifest_version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$")
    generated_at: datetime
    schema_version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$")
    corpus_root: str
    case_counts: dict[str, int] = Field(default_factory=dict)
    suite_counts: dict[str, int] = Field(default_factory=dict)
    maintained_case_ids: list[str] = Field(default_factory=list)
    maintained_suite_ids: list[str] = Field(default_factory=list)
    deprecated_case_ids: list[str] = Field(default_factory=list)
    deprecated_suite_ids: list[str] = Field(default_factory=list)
    notes: Optional[str] = Field(default=None, max_length=1200)

    @model_validator(mode="after")
    def _validate_counts(self) -> "PerceptualFailureCorpusManifest":
        for key, value in self.case_counts.items():
            if value < 0:
                raise ValueError(f"case_counts[{key}] cannot be negative.")
        for key, value in self.suite_counts.items():
            if value < 0:
                raise ValueError(f"suite_counts[{key}] cannot be negative.")
        return self


class PerceptualHarnessProbeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    probe_id: str = Field(..., pattern=r"^PFP-[A-Z0-9-]{4,64}$")
    candidate_text: str = Field(..., min_length=20)
    surface_class: PerceptualSurfaceClass
    case_ids: list[str] = Field(default_factory=list)
    suite_ids: list[str] = Field(default_factory=list)
    evaluate_mutations: bool = Field(default=True)
    metadata: dict[str, Any] = Field(default_factory=dict)


class PerceptualHarnessProbeResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    probe_id: str
    case_id: Optional[str] = None
    suite_id: Optional[str] = None
    operation_id: Optional[str] = None
    expected_status: Optional[PerceptualExpectationStatus] = None
    observed_decision: PerceptualHarnessDecision
    decision_match: bool
    evidence: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    remediation: list[str] = Field(default_factory=list)


class PerceptualFailureHarnessReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    report_id: str = Field(..., pattern=r"^PFR-[A-Z0-9-]{4,64}$")
    evaluated_at: datetime
    request: PerceptualHarnessProbeRequest
    resolved_case_ids: list[str] = Field(default_factory=list)
    resolved_suite_ids: list[str] = Field(default_factory=list)
    decision: PerceptualHarnessDecision
    results: list[PerceptualHarnessProbeResult] = Field(default_factory=list)
    summary: str = Field(..., min_length=20, max_length=1200)
    receipt_ids: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


CASE_CLASS_BY_FAILURE: dict[PerceptualFailureClass, type[PerceptualContrastCaseRecord]] = {
    PerceptualFailureClass.FALSE_DEPTH: FalseDepthContrastCase,
    PerceptualFailureClass.DEAD_POLISH: DeadPolishContrastCase,
    PerceptualFailureClass.SYNTHETIC_AUTHORITY: SyntheticAuthorityContrastCase,
    PerceptualFailureClass.OVERRESOLVED_MEANING: OverresolvedMeaningCase,
    PerceptualFailureClass.EMPTY_MOTIVATIONAL_SMOOTHNESS: EmptyMotivationalSmoothnessCase,
}


CASE_DIRECTORY_BY_FAILURE: dict[PerceptualFailureClass, str] = {
    PerceptualFailureClass.FALSE_DEPTH: "false_depth",
    PerceptualFailureClass.DEAD_POLISH: "dead_polish",
    PerceptualFailureClass.SYNTHETIC_AUTHORITY: "synthetic_authority",
    PerceptualFailureClass.OVERRESOLVED_MEANING: "overresolved_meaning",
    PerceptualFailureClass.EMPTY_MOTIVATIONAL_SMOOTHNESS: "empty_motivational_smoothness",
}

