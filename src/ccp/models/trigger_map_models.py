"""
CCP FR5 Trigger Map Builder — Data Models (Unit 1)
Pydantic v2 models for all FR5 pipeline objects.

Spec reference: FR5 Tech Spec
  §Phase 1 INGEST — prerequisite gate (emotional_dna.json confidence ≥ 0.5)
  §Phase 2 — Trigger identification (6 LIWC-22 markers + V6-V10 MFT mapping)
  §Phase 3 — Origin classification (Conway AKB hierarchy: ESK/GE/LP)
  §Phase 4 — PTG assessment (Tedeschi & Calhoun: resolved_dual_layer/active_processing/raw_unresolved)
  §Phase 5 — Narrative identity (McAdams: redemption/contamination/mixed + 5 positioning types)
  §Phase 6 — Reconsolidation sensitivity (Nader: 1-10 scale, V1 cross-validation)
  §Phase 7 — Archetype mapping (emotional state → archetype candidates, TTT eligibility)
  §Phase 8 EMIT — trigger_map.json (DEP-LIB-002)
  §Phase 9 VALIDATE & CHECKPOINT — 9 checks + receipt write

Architecture reference:
  §7.1 (JIT Skill Compiler Block A — Trigger Map as pre-load)
  §5.3 (Genesis Pipeline — Stage 2)

Research basis:
  Conway AKB hierarchy (2005)
  Tedeschi & Calhoun PTG (2004)
  McAdams Narrative Identity (2001)
  Nader Reconsolidation (2000)
  Haidt MFQ-2 (2023)
  LIWC-22 markers

Primary output:
  - DEP-LIB-002: TriggerMap (trigger_map.json)
"""

import hashlib
import json
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


# ──────────────────────────────────────────────────────────────
# Constants from spec
# ──────────────────────────────────────────────────────────────

# Spec §Phase 1 Gate: emotional_dna.json confidence ≥ 0.5
EMOTIONAL_DNA_MINIMUM_CONFIDENCE: float = 0.5

# Spec §Phase 4: minimum 2 resolved_dual_layer triggers for viable map
MINIMUM_RESOLVED_TRIGGERS: int = 2

# Spec §Phase 6: Reconsolidation sensitivity scale bounds
RECONSOLIDATION_MIN: int = 1
RECONSOLIDATION_MAX: int = 10

# Spec §Phase 9 Validation: minimum checks
VALIDATION_CHECK_COUNT: int = 9

# Spec §Weekly feedback loop: minimum entries before precedence recalculation
MINIMUM_ACTIVATION_ENTRIES_FOR_PRECEDENCE: int = 3

# Spec §Phase 2: LIWC-22 marker categories for trigger identification
LIWC_22_TRIGGER_MARKERS: list[str] = [
    "anger",
    "anxiety",
    "sadness",
    "moral_outrage_proxy",
    "authenticity",
    "cognitive_processing",
]

# Spec §Phase 7: Archetype mapping — emotional states from trigger_map.json template
TRIGGER_EMOTIONAL_STATES: list[str] = [
    "disgust_protective_fury",
    "betrayal_anger",
    "outrage_mechanism_opacity",
    "protective_urgency",
    "righteous_authority",
    "grief_tinged_outrage",
]


# ──────────────────────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────────────────────

class AKBLevel(str, Enum):
    """Spec §Phase 3: Conway AKB hierarchy — memory specificity levels.
    Conway (2005) Self-Memory System."""
    LIFETIME_PERIOD = "lifetime_period"
    GENERAL_EVENT = "general_event"
    EVENT_SPECIFIC_KNOWLEDGE = "event_specific_knowledge"


class PTGStatus(str, Enum):
    """Spec §Phase 4: Tedeschi & Calhoun PTG framework (2004).
    raw_unresolved = HARD EXCLUDE from content activation (code-level filter)."""
    RESOLVED_DUAL_LAYER = "resolved_dual_layer"
    ACTIVE_PROCESSING = "active_processing"
    RAW_UNRESOLVED = "raw_unresolved"


class NarrativeSequenceType(str, Enum):
    """Spec §Phase 5: McAdams Narrative Identity (2001) — sequence types."""
    REDEMPTION = "redemption"
    CONTAMINATION = "contamination"
    MIXED = "mixed"


class NarrativePositioning(str, Enum):
    """Spec §Phase 5: McAdams Narrative Identity — positioning types."""
    RELUCTANT_HERO = "reluctant_hero"
    WHISTLEBLOWER = "whistleblower"
    REFORMED_INSIDER = "reformed_insider"
    OUTSIDER_WITNESS = "outsider_witness"
    SURVIVOR_GUIDE = "survivor_guide"


class MoralFoundationType(str, Enum):
    """Spec §Phase 2: Haidt MFQ-2 (2023) — 6 moral foundations."""
    CARE_HARM = "care_harm"
    FAIRNESS_CHEATING = "fairness_cheating"
    LOYALTY_BETRAYAL = "loyalty_betrayal"
    AUTHORITY_SUBVERSION = "authority_subversion"
    SANCTITY_DEGRADATION = "sanctity_degradation"
    LIBERTY_OPPRESSION = "liberty_oppression"


class TriggerPrecedence(str, Enum):
    """Spec §Weekly feedback loop: precedence levels for activation ranking.
    Calculated after ≥3 activation_history entries."""
    CLIMB = "climb"
    HOLD = "hold"
    FALL = "fall"
    DORMANT = "dormant"


class TriggerMapPipelineStepStatus(str, Enum):
    """Pipeline step execution status."""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    HALTED = "HALTED"


# ──────────────────────────────────────────────────────────────
# Evidence & LIWC-22 Marker
# ──────────────────────────────────────────────────────────────

class TriggerEvidencePassage(BaseModel):
    """Corpus evidence passage supporting a trigger classification.
    Mandate 7: Every classification requires corpus citation."""
    passage_text: str
    source_session_id: str = ""
    passage_index: int = 0
    label: str = ""
    confidence: float = 0.0


class LIWC22MarkerScore(BaseModel):
    """Spec §Phase 2: A single LIWC-22 marker score for a text segment."""
    marker: str = Field(..., description="LIWC-22 category name")
    score: float = Field(default=0.0, ge=0.0, le=1.0)
    raw_count: int = 0
    evidence_passages: list[TriggerEvidencePassage] = Field(default_factory=list)


# ──────────────────────────────────────────────────────────────
# Phase 3: Conway AKB Origin Classification
# ──────────────────────────────────────────────────────────────

class SensoryAnchor(BaseModel):
    """Spec §Phase 3: Sensory-perceptual detail attached to ESK-level memories.
    Conway AKB: Event-Specific Knowledge includes sensory traces."""
    modality: str = Field(
        default="", description="visual, auditory, olfactory, tactile, gustatory"
    )
    description: str = ""
    evidence_passage: Optional[TriggerEvidencePassage] = None


class OriginClassification(BaseModel):
    """Spec §Phase 3: Conway AKB hierarchy classification for a trigger's
    originating experience.
    Conway (2005): Lifetime Period → General Event → Event-Specific Knowledge."""
    akb_level: Optional[AKBLevel] = None
    narrative_summary: str = ""
    sensory_anchors: list[SensoryAnchor] = Field(default_factory=list)
    temporal_context: str = ""
    evidence_passages: list[TriggerEvidencePassage] = Field(default_factory=list)

    def is_populated(self) -> bool:
        return self.akb_level is not None and len(self.evidence_passages) >= 1

    def has_sensory_detail(self) -> bool:
        """Guardian Interview Phase 4 ESK Test: sensory-perceptual detail present."""
        return len(self.sensory_anchors) > 0


# ──────────────────────────────────────────────────────────────
# Phase 4: PTG Assessment
# ──────────────────────────────────────────────────────────────

class PTGAssessment(BaseModel):
    """Spec §Phase 4: Tedeschi & Calhoun PTG framework (2004).
    resolved_dual_layer = path out fully encoded, can access both original
    pain AND resolution simultaneously.
    active_processing = partial resolution, still developing.
    raw_unresolved = live trauma — NOT suitable for content activation.
    HARD EXCLUDE: raw_unresolved triggers are filtered at code level."""
    status: Optional[PTGStatus] = None
    resolution_signal: str = ""
    evidence_passages: list[TriggerEvidencePassage] = Field(default_factory=list)

    def is_populated(self) -> bool:
        return self.status is not None and len(self.evidence_passages) >= 1

    def is_content_safe(self) -> bool:
        """Spec §Phase 4 Safety Gate: raw_unresolved = HARD EXCLUDE."""
        return self.status != PTGStatus.RAW_UNRESOLVED

    def is_fully_resolved(self) -> bool:
        """Check if this trigger has full dual-layer resolution."""
        return self.status == PTGStatus.RESOLVED_DUAL_LAYER


# ──────────────────────────────────────────────────────────────
# Phase 5: McAdams Narrative Identity
# ──────────────────────────────────────────────────────────────

class NarrativeIdentityClassification(BaseModel):
    """Spec §Phase 5: McAdams Narrative Identity (2001).
    Sequence type: redemption, contamination, or mixed.
    Positioning: how the coach positions themselves relative to the trigger."""
    sequence_type: Optional[NarrativeSequenceType] = None
    positioning: Optional[NarrativePositioning] = None
    evidence_passages: list[TriggerEvidencePassage] = Field(default_factory=list)

    def is_populated(self) -> bool:
        return (
            self.sequence_type is not None
            and self.positioning is not None
            and len(self.evidence_passages) >= 1
        )


# ──────────────────────────────────────────────────────────────
# Phase 6: Nader Reconsolidation Sensitivity
# ──────────────────────────────────────────────────────────────

class ReconsolidationSensitivity(BaseModel):
    """Spec §Phase 6: Nader et al. (2000) — prediction error threshold
    required to labilize this trigger's episodic trace.
    Scale: 1-10 (1=easily labilized, 10=requires high specificity).
    Must be cross-validated against V1 (Trigger Specificity Threshold)."""
    score: Optional[int] = Field(default=None, ge=1, le=10)
    scale: str = "1-10 (1=easily labilized, 10=requires high specificity)"
    last_labilized: Optional[str] = None
    v1_cross_validated: bool = False
    v1_score_at_validation: Optional[int] = None
    evidence_passages: list[TriggerEvidencePassage] = Field(default_factory=list)

    @field_validator("score")
    @classmethod
    def validate_score_range(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and not (RECONSOLIDATION_MIN <= v <= RECONSOLIDATION_MAX):
            raise ValueError(
                f"Reconsolidation sensitivity must be {RECONSOLIDATION_MIN}-"
                f"{RECONSOLIDATION_MAX}, got {v}"
            )
        return v

    def is_populated(self) -> bool:
        return self.score is not None and len(self.evidence_passages) >= 1


# ──────────────────────────────────────────────────────────────
# Phase 7: Archetype Mapping
# ──────────────────────────────────────────────────────────────

class ArchetypeMapping(BaseModel):
    """Spec §Phase 7: Maps the emotional state produced by trigger activation
    to archetype candidates from the Trigger-First Engine Architecture.
    TTT eligibility check included."""
    emotional_state: str = ""
    moral_foundation: str = ""
    primary_archetype: str = ""
    secondary_archetype: str = ""
    ttt_minimum: str = ""
    coach_eligible: Optional[bool] = None

    def is_populated(self) -> bool:
        return bool(self.emotional_state and self.primary_archetype)


# ──────────────────────────────────────────────────────────────
# Weekly Feedback Loop: Activation History
# ──────────────────────────────────────────────────────────────

class ActivationHistoryEntry(BaseModel):
    """Spec §Weekly feedback loop: A single activation record.
    Records when a trigger was activated in content and its LIWC-22 scores."""
    activation_id: str = ""
    trigger_id: str = ""
    activation_date: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    content_asset_id: str = ""
    liwc_22_scores: dict[str, float] = Field(
        default_factory=dict,
        description="LIWC-22 marker scores at activation time",
    )
    engagement_metrics: dict[str, Any] = Field(
        default_factory=dict,
        description="Engagement data from content performance",
    )
    notes: str = ""


class PrecedenceCalculation(BaseModel):
    """Spec §Weekly feedback loop: Precedence recalculation result.
    Requires ≥3 activation_history entries before calculation."""
    trigger_id: str = ""
    precedence: Optional[TriggerPrecedence] = None
    activation_count: int = 0
    trend_direction: float = 0.0  # positive = climbing, negative = falling
    calculation_date: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    evidence_summary: str = ""


# ──────────────────────────────────────────────────────────────
# Staleness Tracking
# ──────────────────────────────────────────────────────────────

class StalenessTracking(BaseModel):
    """Spec: Monitors whether life events have shifted MFT weightings.
    Triggers recalibration when drift detected.
    Research: Haidt MFT foundation stability — foundations shift with
    major life events."""
    last_drift_check: Optional[str] = None
    drift_detected: bool = False
    recalibration_recommended: bool = False
    weeks_since_last_recalibration: Optional[int] = None


# ──────────────────────────────────────────────────────────────
# Moral Foundation Mapping (Phase 2 sub-model, before TriggerEntry)
# ──────────────────────────────────────────────────────────────

class MoralFoundationMapping(BaseModel):
    """Spec §Phase 2: MFQ-2 moral foundation mapping for a trigger.
    Haidt MFQ-2 (2023): which foundation(s) are violated."""
    primary: Optional[MoralFoundationType] = None
    secondary: Optional[MoralFoundationType] = None
    evidence_passages: list[TriggerEvidencePassage] = Field(default_factory=list)

    def is_populated(self) -> bool:
        return self.primary is not None


# ──────────────────────────────────────────────────────────────
# Complete Trigger Entry
# ──────────────────────────────────────────────────────────────

class TriggerEntry(BaseModel):
    """Spec §Phase 8 EMIT: A single fully-classified trigger.
    Each trigger = a permanent fire — something this coach cannot stop
    responding to. Not a topic, but a violation-mechanism pair."""
    trigger_id: str = ""
    label: str = ""
    description: str = ""

    # Phase 2: Moral foundation mapping
    moral_foundation: MoralFoundationMapping = Field(
        default_factory=lambda: MoralFoundationMapping()
    )

    # Phase 3: Conway AKB origin classification
    originating_experience: OriginClassification = Field(
        default_factory=OriginClassification
    )

    # Phase 4: PTG assessment
    ptg_status: PTGAssessment = Field(default_factory=PTGAssessment)

    # Phase 5: McAdams narrative identity
    narrative_identity: NarrativeIdentityClassification = Field(
        default_factory=NarrativeIdentityClassification
    )

    # Phase 6: Nader reconsolidation sensitivity
    reconsolidation_sensitivity: ReconsolidationSensitivity = Field(
        default_factory=ReconsolidationSensitivity
    )

    # Activation data
    activation_keywords: list[str] = Field(default_factory=list)
    activation_mechanisms: list[str] = Field(default_factory=list)
    evidence_passages: list[TriggerEvidencePassage] = Field(default_factory=list)

    # Precedence (calculated by weekly feedback loop)
    precedence: Optional[TriggerPrecedence] = None

    def is_fully_classified(self) -> bool:
        """Check if all classification phases are populated."""
        return (
            bool(self.label)
            and self.originating_experience.is_populated()
            and self.ptg_status.is_populated()
            and self.narrative_identity.is_populated()
            and self.reconsolidation_sensitivity.is_populated()
        )

    def is_content_safe(self) -> bool:
        """Spec §Phase 4 Safety Gate: raw_unresolved = HARD EXCLUDE."""
        return self.ptg_status.is_content_safe()


# ──────────────────────────────────────────────────────────────
# Map Status
# ──────────────────────────────────────────────────────────────

class TriggerMapStatus(BaseModel):
    """Status metadata for the overall trigger map."""
    last_built: Optional[str] = None
    last_recalibrated: Optional[str] = None
    total_triggers_mapped: int = 0
    resolved_trigger_count: int = 0
    candidate_trigger_count: int = 0
    excluded_trigger_count: int = 0
    confidence: Optional[float] = None


# ──────────────────────────────────────────────────────────────
# Validation Result
# ──────────────────────────────────────────────────────────────

class TriggerMapValidationCheck(BaseModel):
    """A single validation check result from Phase 9."""
    check_id: str = ""
    check_name: str = ""
    passed: bool = False
    detail: str = ""


class TriggerMapValidationResult(BaseModel):
    """Spec §Phase 9: Complete validation output — 9 checks."""
    checks: list[TriggerMapValidationCheck] = Field(default_factory=list)
    all_passed: bool = False
    minimum_viable: bool = False
    operator_review_required: bool = False

    def compute_result(self) -> None:
        """Compute overall result from individual checks."""
        self.all_passed = all(c.passed for c in self.checks)
        # Minimum viable = at least MINIMUM_RESOLVED_TRIGGERS resolved triggers
        # (checked in pipeline, set here)


# ──────────────────────────────────────────────────────────────
# DEP-LIB-002: TriggerMap (Primary Output)
# ──────────────────────────────────────────────────────────────

class TriggerMap(BaseModel):
    """DEP-LIB-002 — The complete trigger map.
    Spec §Phase 8 EMIT: exact JSON schema.
    Primary output of the FR5 pipeline.

    triggers[] = fully resolved (resolved_dual_layer) triggers
    candidate_triggers[] = active_processing triggers (not yet fully resolved)
    raw_unresolved triggers are EXCLUDED entirely — never emitted."""
    schema_version: str = "2.0"
    dep_id: str = "DEP-LIB-002"
    ccp_layer: str = "Memory (L2)"
    pi_extensions: list[str] = Field(
        default_factory=lambda: ["SoulResonance", "TriggerFirst"]
    )
    description: str = (
        "Trigger Map — the coach's permanent trigger architecture. "
        "Contains primary triggers with MFT foundation mapping, PTG status, "
        "ESK anchors, archetype mappings, and activation history."
    )
    research_basis: str = (
        "Haidt MFQ-2 (2023), Tedeschi & Calhoun PTG (2004), "
        "Conway Self-Memory System/AKB (2005), Nader Reconsolidation (2000), "
        "McAdams Narrative Identity (2001), Tulving Episodic-Semantic Taxonomy (1972)"
    )

    coach_id: str = ""
    map_status: TriggerMapStatus = Field(default_factory=TriggerMapStatus)

    # Fully resolved triggers (resolved_dual_layer)
    triggers: list[TriggerEntry] = Field(default_factory=list)

    # Active processing triggers (candidate, not yet fully resolved)
    candidate_triggers: list[TriggerEntry] = Field(default_factory=list)

    # Archetype mapping table
    trigger_archetype_map: list[ArchetypeMapping] = Field(default_factory=list)

    # Weekly feedback loop data
    activation_history: list[ActivationHistoryEntry] = Field(default_factory=list)

    # Staleness tracking
    staleness_tracking: StalenessTracking = Field(default_factory=StalenessTracking)

    # Integrity
    map_hash: str = ""

    def compute_status(self) -> None:
        """Update map_status counts from current trigger lists."""
        self.map_status.total_triggers_mapped = (
            len(self.triggers) + len(self.candidate_triggers)
        )
        self.map_status.resolved_trigger_count = len(self.triggers)
        self.map_status.candidate_trigger_count = len(self.candidate_triggers)
        now = datetime.now(timezone.utc).isoformat()
        self.map_status.last_built = now

    def compute_confidence(self) -> None:
        """Compute map confidence based on trigger classification completeness."""
        if not self.triggers and not self.candidate_triggers:
            self.map_status.confidence = 0.0
            return

        all_triggers = self.triggers + self.candidate_triggers
        classified_count = sum(
            1 for t in all_triggers if t.is_fully_classified()
        )
        total = len(all_triggers)
        self.map_status.confidence = classified_count / total if total > 0 else 0.0

    def compute_hash(self) -> str:
        """Hash the trigger map for receipt chain integrity."""
        data = self.model_dump(exclude={"map_hash"})
        self.map_hash = hashlib.sha256(
            json.dumps(data, default=str).encode()
        ).hexdigest()
        return self.map_hash

    def meets_minimum_viable(self) -> bool:
        """Spec §AC4: minimum 2 resolved_dual_layer triggers for viable map."""
        return len(self.triggers) >= MINIMUM_RESOLVED_TRIGGERS

    def get_content_safe_triggers(self) -> list[TriggerEntry]:
        """Return only triggers that pass the PTG safety gate.
        Spec §Phase 4: raw_unresolved = HARD EXCLUDE."""
        return [t for t in self.triggers if t.is_content_safe()]


# ──────────────────────────────────────────────────────────────
# Pipeline Session
# ──────────────────────────────────────────────────────────────

class TriggerMapPipelineSession(BaseModel):
    """Top-level session tracking the FR5 pipeline execution."""
    session_id: str
    coach_id: str
    coach_acronym: str
    date: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d")
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    # Input references
    emotional_dna_confidence: float = 0.0
    emotional_dna_path: str = ""

    # Phase outputs
    identified_triggers: list[TriggerEntry] = Field(default_factory=list)
    trigger_map: TriggerMap = Field(default_factory=TriggerMap)
    validation_result: Optional[TriggerMapValidationResult] = None

    # Counters
    raw_trigger_count: int = 0
    classified_trigger_count: int = 0
    excluded_trigger_count: int = 0

    # Step statuses
    step_statuses: dict[str, TriggerMapPipelineStepStatus] = Field(
        default_factory=dict
    )

    # Receipt tracking
    receipt_ids: dict[str, str] = Field(default_factory=dict)

    # Integration flags
    dep_lib_002_written: bool = False
    coach_soul_updated: bool = False
