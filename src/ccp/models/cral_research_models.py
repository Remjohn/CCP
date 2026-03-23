"""
CCP Step 8 — CRAL Research Models (Unit 1)
Pydantic v2 models for the CRAL 9-Skill Research Subsystem (FR14).

Architecture reference:
    FR14_CRAL_Research_Subsystem_Tech_Spec.md
    CCP_Evolution_Architecture_Report_V4 §3.3 — CRAL Production Flow
    CRAL_Documentation_V1 — Diagonal Research Method

Models defined:
    DEP-ENG-022: SessionResearchPlan — The Orchestrator's compiled firing map
    MomentConfig: Per-moment configuration (methodology, quality gate, word limit)
    ResearchPlannerDirective: The 40-60 word research directive
    MomentFinding: Individual moment finding (appended to DEP-ENG-021)
    MomentQualityGateResult: Quality gate evaluation result
    OODAState: OODA loop state tracking

Relationship to Step 7:
    CRALFindingIndex (DEP-ENG-021) schema is already defined in
    adapter_registry_v2_models.py — this step builds the PRODUCER.
    CRALFinding and CRALMomentKey are imported from there.

ADR-01: coach_id scopes all operations.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field

from src.ccp.models.adapter_registry_v2_models import CRALMomentKey


# ══════════════════════════════════════════════════════════════
# OODA Loop State
# ══════════════════════════════════════════════════════════════

class OODAPhase(str, Enum):
    """OODA loop phases for the Research Orchestrator."""
    OBSERVE = "OBSERVE"
    ORIENT = "ORIENT"
    DECIDE = "DECIDE"
    ACT = "ACT"
    COMPLETE = "COMPLETE"
    FALLBACK = "FALLBACK"
    ERROR = "ERROR"


class MomentStatus(str, Enum):
    """Execution status for each moment in the OODA sequence."""
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    EXECUTING = "EXECUTING"
    PASS = "PASS"
    PROVISIONAL = "PROVISIONAL"
    FAIL = "FAIL"
    RETRY = "RETRY"
    SKIPPED = "SKIPPED"


# ══════════════════════════════════════════════════════════════
# Moment Configuration
# ══════════════════════════════════════════════════════════════

class SourceDiscipline(str, Enum):
    """Research methodology per moment — Diagonal Research Method.
    Each moment uses a distinct journalistic discipline."""
    DIGITAL_ETHNOGRAPHY = "digital_ethnography"        # M1
    PRECISION_JOURNALISM = "precision_journalism"      # M2
    BEHAVIORAL_SCIENCE = "behavioral_science"          # M3
    NARRATIVE_JOURNALISM = "narrative_journalism"       # M4
    SCIENCE_JOURNALISM = "science_journalism"           # M5
    INVESTIGATIVE_JOURNALISM = "investigative_journalism"  # M6
    ORAL_HISTORY = "oral_history"                       # M7


class EmotionalRegister(str, Enum):
    """Target emotional register per moment."""
    CULTURAL_URGENCY = "cultural_urgency"              # M1
    SUBSTANTIVE_ANCHOR = "substantive_anchor"          # M2
    PREDICTION_GAP = "prediction_gap"                  # M3
    STORY_STRUCTURE = "story_structure"                 # M4
    SURFACE_VIOLATION = "surface_violation"             # M5
    MAXIMUM_PROXIMITY = "maximum_proximity"             # M6
    TRIBAL_RECOGNITION = "tribal_recognition"           # M7


class HumanEvidenceTarget(str, Enum):
    """Type of human evidence required per moment.
    Neural coupling (Hasson 2010) requires named humans, not statistics."""
    VERIFIED_COMMUNITY_MEMBER = "verified_community_member"  # M1
    NAMED_INSTITUTIONAL_SOURCE = "named_institutional_source"  # M2
    RESEARCHER_DOCUMENTER = "researcher_documenter"            # M3
    NARRATIVE_PROTAGONIST = "narrative_protagonist"             # M4
    COUNTER_INTUITIVE_SUBJECT = "counter_intuitive_subject"    # M5
    INTERNAL_INSTITUTIONAL_SOURCE = "internal_institutional_source"  # M6
    ORDINARY_TRIBE_MEMBER = "ordinary_tribe_member"            # M7


class MomentConfig(BaseModel):
    """Configuration for a single CRAL moment executor skill.

    FR14 §Stage 3: Each Moment executor is governed by a strict
    240-word signal contract. Each has a distinct methodology and quality gate.
    """
    moment_key: CRALMomentKey = Field(description="Which moment this config is for.")
    source_discipline: SourceDiscipline = Field(
        description="Research methodology for this moment."
    )
    emotional_register: EmotionalRegister = Field(
        description="Target emotional register."
    )
    human_evidence_target: HumanEvidenceTarget = Field(
        description="Type of human evidence required."
    )
    max_words: int = Field(
        default=240,
        description="Maximum word count for the finding output (240-word signal contract)."
    )
    quality_gate_description: str = Field(
        description="Description of the quality gate for this moment."
    )
    dependencies: list[CRALMomentKey] = Field(
        default_factory=list,
        description="Moments that must PASS before this one fires."
    )


# Default moment configurations — FR14 §Stage 3
MOMENT_CONFIGS: dict[CRALMomentKey, MomentConfig] = {
    CRALMomentKey.M1_TIMELY: MomentConfig(
        moment_key=CRALMomentKey.M1_TIMELY,
        source_discipline=SourceDiscipline.DIGITAL_ETHNOGRAPHY,
        emotional_register=EmotionalRegister.CULTURAL_URGENCY,
        human_evidence_target=HumanEvidenceTarget.VERIFIED_COMMUNITY_MEMBER,
        quality_gate_description=(
            "Source must be < 4 weeks old community discourse. "
            "The cultural NOW signal validates the topic's relevance window."
        ),
        dependencies=[],  # M1 fires immediately
    ),
    CRALMomentKey.M2_BELIEVABLE: MomentConfig(
        moment_key=CRALMomentKey.M2_BELIEVABLE,
        source_discipline=SourceDiscipline.PRECISION_JOURNALISM,
        emotional_register=EmotionalRegister.SUBSTANTIVE_ANCHOR,
        human_evidence_target=HumanEvidenceTarget.NAMED_INSTITUTIONAL_SOURCE,
        quality_gate_description=(
            "Must contain named institutional source or primary filing. "
            "Fires post DEP-ENG-005 (Trigger Profile)."
        ),
        dependencies=[CRALMomentKey.M1_TIMELY],
    ),
    CRALMomentKey.M3_UNDENIABLE: MomentConfig(
        moment_key=CRALMomentKey.M3_UNDENIABLE,
        source_discipline=SourceDiscipline.BEHAVIORAL_SCIENCE,
        emotional_register=EmotionalRegister.PREDICTION_GAP,
        human_evidence_target=HumanEvidenceTarget.RESEARCHER_DOCUMENTER,
        quality_gate_description=(
            "Must cite a study/researcher documenting the systematic error. "
            "Fires post DEP-ENG-016 (Mood Routing). Maps the prediction gap."
        ),
        dependencies=[CRALMomentKey.M2_BELIEVABLE],
    ),
    CRALMomentKey.M4_RESONANT: MomentConfig(
        moment_key=CRALMomentKey.M4_RESONANT,
        source_discipline=SourceDiscipline.NARRATIVE_JOURNALISM,
        emotional_register=EmotionalRegister.STORY_STRUCTURE,
        human_evidence_target=HumanEvidenceTarget.NARRATIVE_PROTAGONIST,
        quality_gate_description=(
            "Must contain 5 narrative elements: protagonist, status, contact moment, "
            "shift, outcome. Fires post archetype selection. "
            "Celebrity Rejection: is_celebrity == true triggers FAIL + regeneration."
        ),
        dependencies=[CRALMomentKey.M3_UNDENIABLE],
    ),
    CRALMomentKey.M5_SURPRISING: MomentConfig(
        moment_key=CRALMomentKey.M5_SURPRISING,
        source_discipline=SourceDiscipline.SCIENCE_JOURNALISM,
        emotional_register=EmotionalRegister.SURFACE_VIOLATION,
        human_evidence_target=HumanEvidenceTarget.COUNTER_INTUITIVE_SUBJECT,
        quality_gate_description=(
            "Must explicitly contradict the M3 prediction gap within optimal "
            "incongruity limits (Loewenstein 1994 Information Gap Theory)."
        ),
        dependencies=[CRALMomentKey.M4_RESONANT],
    ),
    CRALMomentKey.M6_IRREFUTABLE: MomentConfig(
        moment_key=CRALMomentKey.M6_IRREFUTABLE,
        source_discipline=SourceDiscipline.INVESTIGATIVE_JOURNALISM,
        emotional_register=EmotionalRegister.MAXIMUM_PROXIMITY,
        human_evidence_target=HumanEvidenceTarget.INTERNAL_INSTITUTIONAL_SOURCE,
        quality_gate_description=(
            "Evidence must originate internally from the mechanism's creator/institution. "
            "Maximum source proximity requirement — no secondary analysis."
        ),
        dependencies=[CRALMomentKey.M5_SURPRISING],
    ),
    CRALMomentKey.M7_RELATABLE: MomentConfig(
        moment_key=CRALMomentKey.M7_RELATABLE,
        source_discipline=SourceDiscipline.ORAL_HISTORY,
        emotional_register=EmotionalRegister.TRIBAL_RECOGNITION,
        human_evidence_target=HumanEvidenceTarget.ORDINARY_TRIBE_MEMBER,
        quality_gate_description=(
            "Must contain verified vernacular extraction (slang/cultural syntax "
            "native to tribe). Fires LAST — requires M1-M6 all PASS."
        ),
        dependencies=[
            CRALMomentKey.M1_TIMELY, CRALMomentKey.M2_BELIEVABLE,
            CRALMomentKey.M3_UNDENIABLE, CRALMomentKey.M4_RESONANT,
            CRALMomentKey.M5_SURPRISING, CRALMomentKey.M6_IRREFUTABLE,
        ],
    ),
}


# ══════════════════════════════════════════════════════════════
# Research Planner Directive
# ══════════════════════════════════════════════════════════════

class PlannerDirectiveVerdict(str, Enum):
    """Verdict from the Research Planner directive validation.
    FR14 §Stage 2 Logic Gate."""
    PASS = "PASS"
    PROVISIONAL = "PROVISIONAL"
    FAIL = "FAIL"


class ResearchPlannerDirective(BaseModel):
    """The compiled research directive from the Research Planner.

    FR14 §Stage 2: 40-60 word directive text containing the
    constraint 'human_evidence_required'. Previous-Finding Exclusion
    ensures no overlap with already-gathered moment findings.
    """
    moment_key: CRALMomentKey = Field(description="Target moment for this directive.")
    directive_text: str = Field(
        description="The 40-60 word research directive for the moment executor."
    )
    word_count: int = Field(
        default=0,
        description="Computed word count of directive_text."
    )
    contains_human_evidence_constraint: bool = Field(
        default=False,
        description="True if directive contains 'human_evidence_required'."
    )
    previous_findings_excluded: list[CRALMomentKey] = Field(
        default_factory=list,
        description="List of previous moment findings injected as exclusion constraints."
    )
    verdict: PlannerDirectiveVerdict = Field(
        default=PlannerDirectiveVerdict.FAIL,
        description="Validation verdict."
    )
    verbosity_warning: bool = Field(
        default=False,
        description="True if directive is 61-65 words (PROVISIONAL range)."
    )

    def validate_directive(self) -> PlannerDirectiveVerdict:
        """FR14 §Stage 2 Logic Gate: Validate directive compliance.

        PASS: 40-60 words AND contains human_evidence_required.
        PROVISIONAL: 61-65 words AND contains human_evidence_required.
        FAIL: < 40 words OR > 65 words OR lacks human_evidence_required.
        """
        self.word_count = len(self.directive_text.split())
        self.contains_human_evidence_constraint = (
            "human_evidence_required" in self.directive_text.lower()
        )

        if not self.contains_human_evidence_constraint:
            self.verdict = PlannerDirectiveVerdict.FAIL
            return self.verdict

        if 40 <= self.word_count <= 60:
            self.verdict = PlannerDirectiveVerdict.PASS
            return self.verdict

        if 61 <= self.word_count <= 65:
            self.verbosity_warning = True
            self.verdict = PlannerDirectiveVerdict.PROVISIONAL
            return self.verdict

        self.verdict = PlannerDirectiveVerdict.FAIL
        return self.verdict


# ══════════════════════════════════════════════════════════════
# Moment Quality Gate
# ══════════════════════════════════════════════════════════════

class MomentQualityGateResult(BaseModel):
    """Result from a moment executor's quality gate evaluation.

    FR14 §Stage 3: Each moment has a distinct quality gate.
    Finding > 240 words = immediate length limit exception.
    """
    moment_key: CRALMomentKey = Field(description="Which moment was evaluated.")
    verdict: str = Field(
        default="FAIL",
        description="PASS | PROVISIONAL | FAIL"
    )
    word_count: int = Field(default=0, description="Word count of the finding.")
    word_limit_exceeded: bool = Field(default=False)
    human_evidence_present: bool = Field(default=False)
    celebrity_detected: bool = Field(
        default=False,
        description="True if a celebrity entity was detected (M4 specific)."
    )
    quality_gate_details: str = Field(
        default="",
        description="Description of the quality gate evaluation result."
    )
    retry_count: int = Field(default=0, description="Number of regeneration retries.")
    max_retries: int = Field(default=3, description="Maximum retries before session abort.")


# ══════════════════════════════════════════════════════════════
# OODA State Tracking
# ══════════════════════════════════════════════════════════════

class MomentState(BaseModel):
    """Tracking state for a single moment within the OODA loop."""
    moment_key: CRALMomentKey
    status: MomentStatus = Field(default=MomentStatus.PENDING)
    directive: Optional[ResearchPlannerDirective] = None
    quality_gate: Optional[MomentQualityGateResult] = None
    receipt_id: str = Field(default="")
    retry_count: int = Field(default=0)
    error_message: str = Field(default="")


class OODAState(BaseModel):
    """Full OODA loop state for the Research Orchestrator.

    Tracks the current phase, all moment states, and session metadata.
    """
    coach_id: str = Field(description="ADR-01 tenant isolation.")
    session_id: str = Field(default="", description="Unique CRAL session identifier.")
    phase: OODAPhase = Field(default=OODAPhase.OBSERVE)
    moments: dict[str, MomentState] = Field(
        default_factory=dict,
        description="Keyed by CRALMomentKey value."
    )
    current_moment: Optional[CRALMomentKey] = None
    completed_count: int = Field(default=0)
    total_moments: int = Field(default=7)
    fallback_mode: bool = Field(default=False)
    error_log: list[str] = Field(default_factory=list)

    def initialize_moments(self) -> None:
        """Initialize all 7 moment states."""
        for mk in CRALMomentKey:
            self.moments[mk.value] = MomentState(moment_key=mk)

    def is_moment_ready(self, moment_key: CRALMomentKey) -> bool:
        """Check if a moment's dependencies are all PASS."""
        config = MOMENT_CONFIGS.get(moment_key)
        if config is None:
            return False
        for dep in config.dependencies:
            dep_state = self.moments.get(dep.value)
            if dep_state is None or dep_state.status != MomentStatus.PASS:
                return False
        return True

    def all_moments_complete(self) -> bool:
        """Check if all 7 moments have status PASS."""
        return all(
            ms.status == MomentStatus.PASS
            for ms in self.moments.values()
        )

    def get_next_moment(self) -> Optional[CRALMomentKey]:
        """Get the next moment that is PENDING and has all dependencies met."""
        for mk in CRALMomentKey:
            state = self.moments.get(mk.value)
            if state and state.status == MomentStatus.PENDING and self.is_moment_ready(mk):
                return mk
        return None


# ══════════════════════════════════════════════════════════════
# DEP-ENG-022: Session Research Plan
# ══════════════════════════════════════════════════════════════

class SessionResearchPlan(BaseModel):
    """DEP-ENG-022 — CRAL Session Research Plan.

    The Orchestrator's compiled firing map for the session.
    Used for auditing and the Fingerprint Archive.

    CRAL_Documentation_V1: 'DEP-ENG-022 (CRAL Session Research Plan) —
    the Orchestrator's compiled firing map for the session, used for
    auditing and the Fingerprint Archive.'
    """
    dep_id: str = Field(default="DEP-ENG-022")
    coach_id: str = Field(description="ADR-01 tenant isolation.")
    session_id: str = Field(description="Unique CRAL session identifier.")
    theme: str = Field(description="Content theme for this research session.")
    archetype_id: str = Field(
        default="",
        description="Archetype family driving this compilation."
    )
    trigger_id: str = Field(
        default="",
        description="Trigger that initiated this research session."
    )
    mood_state: str = Field(
        default="",
        description="MoodStatePrimary value at session initiation."
    )
    moment_sequence: list[CRALMomentKey] = Field(
        default_factory=lambda: list(CRALMomentKey),
        description="Planned execution sequence (M1 → M7)."
    )
    moment_directives: dict[str, str] = Field(
        default_factory=dict,
        description="Keyed by CRALMomentKey value — compiled directive text per moment."
    )
    moment_statuses: dict[str, str] = Field(
        default_factory=dict,
        description="Keyed by CRALMomentKey value — final status per moment."
    )
    fallback_invoked: bool = Field(
        default=False,
        description="True if backward compatibility fallback was triggered."
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO 8601 session plan creation timestamp."
    )
    receipt_chain_hash: str = Field(
        default="",
        description="Final receipt chain hash for this session."
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional session metadata."
    )
