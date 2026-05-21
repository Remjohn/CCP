"""
CCP FR4 Emotional DNA Extraction — Data Models (Unit 1)
Pydantic v2 models for all FR4 pipeline objects.

Spec reference: FR4 Tech Spec §Phase 5 EMIT output schema,
    §Phase 3 V1-V5/V6-V10 variable definitions,
    §Phase 4 CSIP v3.0 extensions,
    §Phase 2 granularity triage tiers,
    §Phase 6 cross-validation constraints
Architecture reference: §7.1 (JIT Skill Compiler Block A — Emotional DNA as pre-load),
    §5.3 (Genesis Pipeline — Stage 1), §12.3 (V5.0 Onboarding Prerequisites)

Primary output:
  - DEP-LIB-001: EmotionalDNAProfile (10-variable profile + CSIP v3 extensions)
"""

import hashlib
import json
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional, Union

from pydantic import BaseModel, Field, field_validator


# ──────────────────────────────────────────────────────────────
# Constants from spec
# ──────────────────────────────────────────────────────────────

# Spec §Prerequisite Gate: "authenticated_word_count ≥ 3000"
MINIMUM_CORPUS_WORDS: int = 3000

# Spec §Phase 2 Granularity Triage
GRANULARITY_HIGH_THRESHOLD: int = 25
GRANULARITY_MEDIUM_THRESHOLD: int = 12

# Spec §Phase 6 Constraint C cross-validation
CROSS_VALIDATION_MFT_DIVERGENCE_PCT: float = 15.0

# Spec §Phase 3 V2: "5+ extended passages (≥200 words)"
V2_MINIMUM_PASSAGES: int = 5
V2_MINIMUM_PASSAGE_WORDS: int = 200

# Spec §Phase 3 V1: "Minimum 3 passages"
V1_MINIMUM_EVIDENCE_PASSAGES: int = 3

# Spec §Phase 3 V3: "Minimum 5 action-classified + 5 reflective-classified"
V3_MINIMUM_ACTION_PASSAGES: int = 5
V3_MINIMUM_REFLECTIVE_PASSAGES: int = 5

# Spec §Phase 3 V4: "Minimum 3 outrage + 3 analytical-distance"
V4_MINIMUM_OUTRAGE_PASSAGES: int = 3
V4_MINIMUM_ANALYTICAL_PASSAGES: int = 3

# Spec §Phase 3 V5: "Minimum 5 attribution passages across ≥2 categories"
V5_MINIMUM_ATTRIBUTION_PASSAGES: int = 5
V5_MINIMUM_CATEGORIES: int = 2

# Spec §Phase 3 V6-V10: "minimum 3 passages each for Primary and Secondary"
MFT_MINIMUM_EVIDENCE_PASSAGES: int = 3


# ──────────────────────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────────────────────

class TriageTier(str, Enum):
    """Spec §Phase 2: Granularity triage classification."""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class AppraisalSequenceType(str, Enum):
    """Spec §Phase 3 V2: Appraisal sequence ordering types."""
    MECHANISM_FIRST = "mechanism_first"
    MORAL_VERDICT_FIRST = "moral_verdict_first"
    NARRATIVE_FIRST = "narrative_first"
    COPING_FIRST = "coping_first"
    MIXED = "mixed"


class AgencyAttributionType(str, Enum):
    """Spec §Phase 3 V5: Agency attribution bias categories."""
    SELF = "self"
    INDIVIDUAL = "individual"
    INSTITUTIONAL = "institutional"
    SYSTEMIC = "systemic"


class FairnessSubType(str, Enum):
    """Spec §Phase 3 V7: MFQ-2 fairness sub-type distinction."""
    EQUALITY = "equality"
    PROPORTIONALITY = "proportionality"


class ClusterAlignment(str, Enum):
    """Spec §Phase 3 V6-V10: Individualizing vs Binding cluster alignment."""
    INDIVIDUALIZING = "individualizing"
    BINDING = "binding"
    BALANCED = "balanced"


class ResolutionPatternType(str, Enum):
    """Spec §Phase 4 EXT-5: Resolution pattern classification."""
    RESOLVES = "resolves"
    LEAVES_OPEN = "leaves_open"
    CONVERTS = "converts"


class ResidencyTime(str, Enum):
    """Spec §Phase 4 EXT-1: Emotion residency time classification."""
    SHORT = "SHORT"
    MEDIUM = "MEDIUM"
    LONG = "LONG"


class EmotionalDNAPipelineStepStatus(str, Enum):
    """Pipeline step execution status."""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    HALTED = "HALTED"


class IncoherenceType(str, Enum):
    """Spec §Phase 6 Constraint C: Types of appraisal-MFT incoherence."""
    HIGH_CARE_SELF_AGENCY = "high_care_self_agency"
    HIGH_LIBERTY_SELF_AGENCY = "high_liberty_self_agency"
    HIGH_LOYALTY_HIGH_NORM = "high_loyalty_high_norm"
    HIGH_SANCTITY_COPING_FIRST = "high_sanctity_coping_first"


# ──────────────────────────────────────────────────────────────
# Evidence Passage
# ──────────────────────────────────────────────────────────────

class EvidencePassage(BaseModel):
    """A single corpus evidence passage supporting a variable.
    Spec §Mandate 7: Every variable requires corpus citation."""
    passage_text: str
    source_session_id: str = ""
    passage_index: int = 0
    label: str = ""
    confidence: float = 0.0


# ──────────────────────────────────────────────────────────────
# V1–V5: Cognitive Appraisal Architecture
# ──────────────────────────────────────────────────────────────

class V1TriggerSpecificityThreshold(BaseModel):
    """Spec §Phase 3 V1: Trigger Specificity Threshold (Scale 1-10).
    Scherer CPM: Goal Relevance SEC + Novelty Check."""
    score: Optional[int] = Field(default=None, ge=1, le=10)
    scale: str = "1-10"
    evidence_passages: list[EvidencePassage] = Field(default_factory=list)

    def is_populated(self) -> bool:
        return self.score is not None and len(self.evidence_passages) >= 1


class V2AppraisalSequenceOrdering(BaseModel):
    """Spec §Phase 3 V2: Appraisal Sequence Ordering (Categorical).
    Scherer CPM: SEC cascade ordering."""
    type: Optional[AppraisalSequenceType] = None
    percentage_breakdown: dict[str, float] = Field(default_factory=dict)
    evidence_passages: list[EvidencePassage] = Field(default_factory=list)

    def is_populated(self) -> bool:
        return self.type is not None and len(self.evidence_passages) >= 1


class V3CopingPotentialPattern(BaseModel):
    """Spec §Phase 3 V3: Coping Potential Pattern (Ratio 0.0-1.0).
    Lazarus: Secondary Appraisal — controllability assessment."""
    ratio: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    scale: str = "0.0-1.0 (action/total)"
    action_count: int = 0
    reflective_count: int = 0
    evidence_passages: list[EvidencePassage] = Field(default_factory=list)

    def is_populated(self) -> bool:
        return self.ratio is not None and len(self.evidence_passages) >= 1


class V4NormCompatibilityThreshold(BaseModel):
    """Spec §Phase 3 V4: Norm Compatibility Threshold (Scale 1-10).
    Scherer CPM: Internal Standards SEC."""
    score: Optional[int] = Field(default=None, ge=1, le=10)
    scale: str = "1-10"
    evidence_passages: list[EvidencePassage] = Field(default_factory=list)

    def is_populated(self) -> bool:
        return self.score is not None and len(self.evidence_passages) >= 1


class V5AgencyAttributionBias(BaseModel):
    """Spec §Phase 3 V5: Agency Attribution Bias (Categorical + dominant).
    EMA: Causal Attribution."""
    dominant: Optional[AgencyAttributionType] = None
    secondary: Optional[AgencyAttributionType] = None
    distribution: dict[str, int] = Field(default_factory=dict)
    evidence_passages: list[EvidencePassage] = Field(default_factory=list)

    def is_populated(self) -> bool:
        return self.dominant is not None and len(self.evidence_passages) >= 1


class AppraisalVariables(BaseModel):
    """Container for V1-V5 cognitive appraisal variables."""
    v1_trigger_specificity_threshold: V1TriggerSpecificityThreshold = Field(
        default_factory=V1TriggerSpecificityThreshold
    )
    v2_appraisal_sequence_ordering: V2AppraisalSequenceOrdering = Field(
        default_factory=V2AppraisalSequenceOrdering
    )
    v3_coping_potential_pattern: V3CopingPotentialPattern = Field(
        default_factory=V3CopingPotentialPattern
    )
    v4_norm_compatibility_threshold: V4NormCompatibilityThreshold = Field(
        default_factory=V4NormCompatibilityThreshold
    )
    v5_agency_attribution_bias: V5AgencyAttributionBias = Field(
        default_factory=V5AgencyAttributionBias
    )

    def populated_count(self) -> int:
        """Count how many V1-V5 variables are populated with evidence."""
        count = 0
        if self.v1_trigger_specificity_threshold.is_populated():
            count += 1
        if self.v2_appraisal_sequence_ordering.is_populated():
            count += 1
        if self.v3_coping_potential_pattern.is_populated():
            count += 1
        if self.v4_norm_compatibility_threshold.is_populated():
            count += 1
        if self.v5_agency_attribution_bias.is_populated():
            count += 1
        return count


# ──────────────────────────────────────────────────────────────
# V6–V10: Moral Foundations (MFQ-2)
# ──────────────────────────────────────────────────────────────

class MoralFoundationWeight(BaseModel):
    """A single moral foundation weight with evidence.
    Spec §Phase 3 V6-V10: weight = foundation_keyword_frequency / total."""
    weight: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    evidence_passages: list[EvidencePassage] = Field(default_factory=list)

    def is_populated(self) -> bool:
        return self.weight is not None and len(self.evidence_passages) >= 1


class V7FairnessCheating(MoralFoundationWeight):
    """Spec §Phase 3 V7: Fairness/Cheating with sub-type distinction.
    MFQ-2: Equality vs Proportionality."""
    sub_type: Optional[FairnessSubType] = None


class V10SanctityDegradation(MoralFoundationWeight):
    """Spec §Phase 3 V10a: Sanctity/Degradation sub-weight."""
    pass


class V10bLibertyOppression(MoralFoundationWeight):
    """Spec §Phase 3 V10b: Liberty/Oppression sub-weight."""
    pass


class MoralFoundations(BaseModel):
    """Container for V6-V10 moral foundation weights.
    Spec §Phase 3: 'Sum across V6-V10 = 1.0'."""
    v6_care_harm: MoralFoundationWeight = Field(default_factory=MoralFoundationWeight)
    v7_fairness_cheating: Union[V7FairnessCheating, MoralFoundationWeight] = Field(default_factory=V7FairnessCheating)
    v8_loyalty_betrayal: MoralFoundationWeight = Field(default_factory=MoralFoundationWeight)
    v9_authority_subversion: MoralFoundationWeight = Field(default_factory=MoralFoundationWeight)
    v10_sanctity_degradation: Union[V10SanctityDegradation, MoralFoundationWeight] = Field(default_factory=V10SanctityDegradation)
    v10b_liberty_oppression: Union[V10bLibertyOppression, MoralFoundationWeight] = Field(default_factory=V10bLibertyOppression)
    primary_foundation: Optional[str] = None
    secondary_foundation: Optional[str] = None
    cluster_alignment: Optional[ClusterAlignment] = None

    def populated_count(self) -> int:
        """Count how many V6-V10 foundation weights are populated."""
        count = 0
        if self.v6_care_harm.is_populated():
            count += 1
        if self.v7_fairness_cheating.is_populated():
            count += 1
        if self.v8_loyalty_betrayal.is_populated():
            count += 1
        if self.v9_authority_subversion.is_populated():
            count += 1
        if self.v10_sanctity_degradation.is_populated():
            count += 1
        # V10b is part of V10 combined — counts with V10a
        return count

    def all_weights(self) -> dict[str, Optional[float]]:
        """Return all foundation weights as a dict."""
        return {
            "care_harm": self.v6_care_harm.weight,
            "fairness_cheating": self.v7_fairness_cheating.weight,
            "loyalty_betrayal": self.v8_loyalty_betrayal.weight,
            "authority_subversion": self.v9_authority_subversion.weight,
            "sanctity_degradation": self.v10_sanctity_degradation.weight,
            "liberty_oppression": self.v10b_liberty_oppression.weight,
        }


# ──────────────────────────────────────────────────────────────
# Phase 4: CSIP v3.0 Extension Variables
# ──────────────────────────────────────────────────────────────

class EmotionResidencyTime(BaseModel):
    """Spec §Phase 4 EXT-1: Emotion Residency Time per emotional register.
    SHORT: <2 sentences; MEDIUM: 3-5 sentences; LONG: 6+ sentences."""
    per_register: dict[str, ResidencyTime] = Field(default_factory=dict)
    evidence_passages: list[EvidencePassage] = Field(default_factory=list)

    def is_populated(self) -> bool:
        return len(self.per_register) > 0 and len(self.evidence_passages) >= 1


class TopicCeiling(BaseModel):
    """A single topic cluster's emotional ceiling."""
    topic: str
    max_ttt: str = ""
    construction_signature_at_ceiling: str = ""
    evidence_passages: list[EvidencePassage] = Field(default_factory=list)


class EmotionalCeilingPerTopic(BaseModel):
    """Spec §Phase 4 EXT-2: Emotional Ceiling Per Topic."""
    topic_ceilings: list[TopicCeiling] = Field(default_factory=list)

    def is_populated(self) -> bool:
        return len(self.topic_ceilings) > 0


class TopicFloor(BaseModel):
    """A single topic cluster's emotional floor."""
    topic: str
    min_ttt: str = ""
    evidence_passages: list[EvidencePassage] = Field(default_factory=list)


class EmotionalFloorPerTopic(BaseModel):
    """Spec §Phase 4 EXT-3: Emotional Floor Per Topic."""
    topic_floors: list[TopicFloor] = Field(default_factory=list)

    def is_populated(self) -> bool:
        return len(self.topic_floors) > 0


class SuppressionPattern(BaseModel):
    """Spec §Phase 4 EXT-4: A single suppression pattern entry."""
    emotion: str
    compression_artifact: str = ""
    triggering_context: str = ""
    evidence_passages: list[EvidencePassage] = Field(default_factory=list)


class SuppressionPatterns(BaseModel):
    """Container for all suppression patterns."""
    patterns: list[SuppressionPattern] = Field(default_factory=list)

    def is_populated(self) -> bool:
        return len(self.patterns) > 0


class EmotionalBleedSignature(BaseModel):
    """Spec §Phase 4 EXT-5: A single emotional bleed signature.
    Example: 'I'm heartbroken that — no, I'm FURIOUS that they...'"""
    primary_emotion: str
    bleeds_into: str
    trigger_context: str = ""
    construction_marker: str = ""
    evidence_passages: list[EvidencePassage] = Field(default_factory=list)


class ResolutionPattern(BaseModel):
    """Spec §Phase 4 EXT-5: Resolution pattern classification."""
    dominant: Optional[ResolutionPatternType] = None
    per_register_overrides: dict[str, ResolutionPatternType] = Field(default_factory=dict)
    evidence_passages: list[EvidencePassage] = Field(default_factory=list)

    def is_populated(self) -> bool:
        return self.dominant is not None and len(self.evidence_passages) >= 1


class CSIPv3Extensions(BaseModel):
    """Spec §Phase 4: All 5 CSIP v3.0 behavioral extension variables."""
    emotion_residency_time: EmotionResidencyTime = Field(
        default_factory=EmotionResidencyTime
    )
    emotional_ceiling_per_topic: EmotionalCeilingPerTopic = Field(
        default_factory=EmotionalCeilingPerTopic
    )
    emotional_floor_per_topic: EmotionalFloorPerTopic = Field(
        default_factory=EmotionalFloorPerTopic
    )
    suppression_patterns: SuppressionPatterns = Field(
        default_factory=SuppressionPatterns
    )
    resolution_pattern: ResolutionPattern = Field(
        default_factory=ResolutionPattern
    )
    emotional_bleed_signatures: list[EmotionalBleedSignature] = Field(
        default_factory=list
    )

    def populated_count(self) -> int:
        """Count how many CSIP v3 extensions are populated."""
        count = 0
        if self.emotion_residency_time.is_populated():
            count += 1
        if self.emotional_ceiling_per_topic.is_populated():
            count += 1
        if self.emotional_floor_per_topic.is_populated():
            count += 1
        if self.suppression_patterns.is_populated():
            count += 1
        if self.resolution_pattern.is_populated():
            count += 1
        return count


# ──────────────────────────────────────────────────────────────
# Granularity Triage
# ──────────────────────────────────────────────────────────────

class GranularityTriageResult(BaseModel):
    """Spec §Phase 2: Granularity triage output.
    Determines extraction depth based on distinct emotional term count.
    Barrett (2017) Emotional Granularity."""
    tier: Optional[TriageTier] = None
    distinct_emotional_term_count: int = 0
    emotional_terms_found: list[str] = Field(default_factory=list)
    extraction_depth_note: str = ""


# ──────────────────────────────────────────────────────────────
# Extraction Status
# ──────────────────────────────────────────────────────────────

class ExtractionStatus(BaseModel):
    """Spec §Phase 5: Extraction status metadata."""
    triage_tier: Optional[TriageTier] = None
    confidence: float = 0.0
    populated_variables: int = 0
    total_variables: int = 10
    csip_v3_populated: int = 0
    csip_v3_total: int = 5
    csip_confidence: float = 0.0
    last_extracted: Optional[str] = None
    corpus_word_count: int = 0
    sources_used: list[str] = Field(default_factory=list)


# ──────────────────────────────────────────────────────────────
# Cross-Validation (Constraint C)
# ──────────────────────────────────────────────────────────────

class IncoherenceFlag(BaseModel):
    """Spec §Phase 6 Constraint C: A single incoherence flag.
    'On any incoherence: flag for operator review. Do NOT auto-correct.'"""
    incoherence_type: IncoherenceType
    description: str
    conflicting_variables: list[str] = Field(default_factory=list)
    evidence_summary: str = ""


class CrossValidationResult(BaseModel):
    """Spec §Phase 6: Full cross-validation output."""
    constraint_a_passed: bool = False
    constraint_b_passed: bool = False
    constraint_c_passed: bool = False
    constraint_d_passed: bool = False
    incoherence_flags: list[IncoherenceFlag] = Field(default_factory=list)
    variables_forced_to_null: list[str] = Field(default_factory=list)
    operator_review_required: bool = False

    def all_passed(self) -> bool:
        return (
            self.constraint_a_passed
            and self.constraint_b_passed
            and self.constraint_d_passed
            # Constraint C flags don't block — they trigger operator review
        )


# ──────────────────────────────────────────────────────────────
# DEP-LIB-001: Emotional DNA Profile (Primary Output)
# ──────────────────────────────────────────────────────────────

class EmotionalDNAProfile(BaseModel):
    """DEP-LIB-001 — The complete 10-variable Emotional DNA profile.
    Spec §Phase 5 EMIT: exact JSON schema.
    Primary output of the FR4 pipeline."""
    dep_id: str = "DEP-LIB-001"
    version: str = "1.0"
    extraction_status: ExtractionStatus = Field(default_factory=ExtractionStatus)
    appraisal_variables: AppraisalVariables = Field(default_factory=AppraisalVariables)
    moral_foundations: MoralFoundations = Field(default_factory=MoralFoundations)
    csip_v3_extensions: CSIPv3Extensions = Field(default_factory=CSIPv3Extensions)
    profile_hash: str = ""

    def compute_confidence(self) -> None:
        """Spec §Phase 5: 'Confidence = populated_variables / total_variables'."""
        appraisal_count = self.appraisal_variables.populated_count()
        mft_count = self.moral_foundations.populated_count()
        total_populated = appraisal_count + mft_count
        self.extraction_status.populated_variables = total_populated
        self.extraction_status.confidence = total_populated / self.extraction_status.total_variables

        csip_count = self.csip_v3_extensions.populated_count()
        self.extraction_status.csip_v3_populated = csip_count
        if self.extraction_status.csip_v3_total > 0:
            self.extraction_status.csip_confidence = (
                csip_count / self.extraction_status.csip_v3_total
            )

    def compute_hash(self) -> str:
        """Hash the profile for receipt chain."""
        data = self.model_dump(exclude={"profile_hash"})
        self.profile_hash = hashlib.sha256(
            json.dumps(data, default=str).encode()
        ).hexdigest()
        return self.profile_hash


# ──────────────────────────────────────────────────────────────
# Pipeline Session
# ──────────────────────────────────────────────────────────────

class EmotionalDNAPipelineSession(BaseModel):
    """Top-level session tracking the FR4 pipeline execution."""
    session_id: str
    coach_id: str
    coach_acronym: str
    date: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d")
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    # Phase outputs
    corpus_word_count: int = 0
    corpus_sources: list[str] = Field(default_factory=list)
    triage_result: Optional[GranularityTriageResult] = None
    profile: EmotionalDNAProfile = Field(default_factory=EmotionalDNAProfile)
    cross_validation: Optional[CrossValidationResult] = None

    # Step statuses
    step_statuses: dict[str, EmotionalDNAPipelineStepStatus] = Field(
        default_factory=dict
    )

    # Receipt tracking
    receipt_ids: dict[str, str] = Field(default_factory=dict)

    # Integration flags
    dep_lib_001_written: bool = False
    coach_soul_updated: bool = False
    fr3_readiness_checked: bool = False
