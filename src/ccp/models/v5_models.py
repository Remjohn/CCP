"""
CCP V5.0 Data Models — FR1 Unit 1
DEP-ENG-023: Cultural Memory Map (CMM)
DEP-ENG-024: Coach Story Archive
DEP-ENG-025: Context Selection Object (Context Performance Registry)
DEP-ENG-045: Context Performance Registry (table initialization schema)

Spec reference: FR1 Tech Spec §Phase 0, Steps 0-A through 0-D
Architecture reference: CCP_Technical_Architecture.md §3.1

These models define the V5.0 Supabase table schemas. Every field is traced
to an explicit spec instruction. No fields are added beyond what the spec defines.

PRODUCTION LOCK GATE is in morgan_orchestrator.py (Unit 2 / Unit 3).
CMM EXTRACTION PROTOCOL (DEP-PROTO-014) is in cmm_extraction.py (Unit 4).
STORY ARCHIVE APPROVAL GATE (DEP-PROTO-016) is in story_archive.py (Unit 5).
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


# ──────────────────────────────────────────────────────────────
# DEP-ENG-023: Cultural Memory Map (CMM)
# Spec: Phase 0, Step 0-A — "Morgan runs the CMM extraction pass using all
# onboarding source material... Operator reviews all 7 CMM layer entries."
# ──────────────────────────────────────────────────────────────

class CMMLayerType(str, Enum):
    """The 7 CMM layers as defined in FR1 Phase 0, Step 0-A."""
    FORMATIVE_TEXTS = "formative_texts_and_works"
    COLLECTIVE_WOUND = "collective_wound_history"
    INDUSTRY_MYTHOLOGY = "industry_mythology"
    GENERATIONAL_SIGNATURE = "generational_signature"
    LINGUISTIC_TEMPLATES = "linguistic_template_library"
    ASPIRATIONAL_ARCHETYPE = "aspirational_archetype"
    SHARED_ENEMY = "shared_enemy_typology"


class CMMEntry(BaseModel):
    """A single entry within a CMM layer.

    Spec: "≥3 entries per layer" — each entry is a discrete
    cultural data point identified from onboarding material.
    Operator approval is required (not automatic).
    """
    entry_id: str = Field(..., description="Unique entry identifier")
    layer_type: CMMLayerType = Field(..., description="Which of the 7 CMM layers this belongs to")
    content: str = Field(..., min_length=10, description="The cultural intelligence content")
    source_material: str = Field(
        ...,
        description="Which onboarding source this was extracted from "
                    "(Sacred Audio transcript, business canvas, tribe soul, or philosophy brief)"
    )
    operator_approved: bool = Field(
        default=False,
        description="Spec: 'CMM is NOT written automatically — the Agent identifies, the operator decides.'"
    )
    approved_at: Optional[datetime] = Field(default=None)
    coach_id: str = Field(..., description="Coach instance scope — ADR-01 single-tenant isolation")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CulturalMemoryMap(BaseModel):
    """DEP-ENG-023: Cultural Memory Map.

    Spec: cultural_memory_map table (PK: cmm_id) — JSONB payload containing
    7 layers. Completion gate: ≥4 of 7 layers populated with ≥3 entries per layer.
    Architecture §3.1: 'cultural_memory_map (PK: cmm_id): JSONB payload containing
    7 layers (Formative Texts, Collective Wound History, Industry Mythology,
    Generational Signature, Linguistic Templates, Aspirational Archetype, Enemy Typology)'
    """
    cmm_id: str = Field(..., description="Primary key — PK: cmm_id per Architecture §3.1")
    coach_id: str = Field(..., description="Single-tenant scope — ADR-01")
    entries: list[CMMEntry] = Field(default_factory=list)
    status: str = Field(
        default="initialized",
        description="initialized | in_progress | operator_confirmed"
    )
    operator_confirmed: bool = Field(
        default=False,
        description="Set to True only when operator has reviewed and confirmed all entries"
    )
    confirmed_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def get_entries_by_layer(self, layer: CMMLayerType) -> list[CMMEntry]:
        """Return all approved entries for a given layer."""
        return [e for e in self.entries if e.layer_type == layer and e.operator_approved]

    def get_populated_layer_count(self) -> int:
        """Count layers with ≥3 approved entries each.

        Spec gate: ≥4 of 7 layers populated with ≥3 entries per layer.
        """
        count = 0
        for layer in CMMLayerType:
            if len(self.get_entries_by_layer(layer)) >= 3:
                count += 1
        return count

    def passes_completion_gate(self) -> bool:
        """Gate G-CMM: ≥4 of 7 layers with ≥3 entries AND operator_confirmed == True.

        Spec: 'Completion gate: Operator confirms all entries via Telegram review prompt.'
        Both conditions must be true.
        """
        return self.operator_confirmed and self.get_populated_layer_count() >= 4


# ──────────────────────────────────────────────────────────────
# DEP-ENG-024: Coach Story Archive
# Spec: Phase 0, Step 0-B — "Morgan dispatches a structured story extraction
# interview via Telegram... Each story is structured using the Hartian 5-element schema"
# ──────────────────────────────────────────────────────────────

class StoryType(str, Enum):
    """The 5 story categories from FR1 Phase 0, Step 0-B."""
    PERSONAL_TRANSFORMATION = "personal_transformation_moments"
    PROFESSIONAL_FAILURE = "professional_failures"
    CLIENT_BREAKTHROUGH = "client_breakthrough_testimonials"
    INFLECTION_POINT = "inflection_points"
    COLLECTIVE_WOUND = "collective_wound_experiences"


class HartianStorySchema(BaseModel):
    """The Hartian 5-element story schema.

    Spec: 'Each story is structured using the Hartian 5-element schema:
    1. Protagonist status
    2. Moment of contact
    3. Internal shift
    4. Outcome
    5. Tribal markers'
    """
    protagonist_status: str = Field(
        ...,
        min_length=10,
        description="What was the coach's position/state before — Element 1"
    )
    moment_of_contact: str = Field(
        ...,
        min_length=10,
        description="The specific event or encounter — Element 2"
    )
    internal_shift: str = Field(
        ...,
        min_length=10,
        description="The precise moment of realization — Element 3"
    )
    outcome: str = Field(
        ...,
        min_length=10,
        description="What changed as a result — Element 4"
    )
    tribal_markers: list[str] = Field(
        ...,
        min_length=1,
        description="Phrases, references, or cultural touchstones the audience will recognize — Element 5"
    )


class CoachStoryEntry(BaseModel):
    """A single entry in the Coach Story Archive.

    Spec: 'Each approved story tagged with: story_type, mechanism_tag,
    arc_phase_fit, cral_moment_fit, emotional_register'
    DEP-PROTO-016 approval gate: operator approves/rejects each entry.
    """
    story_id: str = Field(..., description="Unique story identifier — PK per Architecture §3.1")
    coach_id: str = Field(..., description="Single-tenant scope — ADR-01")
    story_type: StoryType = Field(..., description="One of the 5 story categories")
    hartian_schema: HartianStorySchema = Field(..., description="The 5-element structured story")

    # Tagging fields — spec: "tagged with: story_type, mechanism_tag, arc_phase_fit, cral_moment_fit, emotional_register"
    mechanism_tag: str = Field(default="", description="The mechanism this story demonstrates")
    arc_phase_fit: str = Field(
        default="",
        description="Which arc phase(s) this story is best suited for"
    )
    cral_moment_fit: str = Field(
        default="",
        description="Which CRAL moment (M1-M7) this story pre-addresses"
    )
    emotional_register: str = Field(
        default="",
        description="The emotional register (vulnerable, triumphant, humorous, etc.)"
    )

    # Approval gate (DEP-PROTO-016)
    operator_approved: bool = Field(
        default=False,
        description="DEP-PROTO-016: 'each story is reviewed and the operator approves/rejects'"
    )
    approved_at: Optional[datetime] = Field(default=None)
    rejection_reason: Optional[str] = Field(default=None)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CoachStoryArchive(BaseModel):
    """DEP-ENG-024: Coach Story Archive.

    Spec: 'coach_story_archive (PK: story_id): Enforces the Hartian 5-element schema'
    Completion gate (DEP-PROTO-016): ≥3 approved entries across ≥2 story types.
    """
    archive_id: str = Field(..., description="Primary key for this archive instance")
    coach_id: str = Field(..., description="Single-tenant scope — ADR-01")
    entries: list[CoachStoryEntry] = Field(default_factory=list)
    status: str = Field(
        default="initialized",
        description="initialized | seeding | gate_passed"
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def get_approved_entries(self) -> list[CoachStoryEntry]:
        """Return all operator-approved story entries."""
        return [e for e in self.entries if e.operator_approved]

    def get_approved_story_types(self) -> set[StoryType]:
        """Return the set of story types with at least one approved entry."""
        return {e.story_type for e in self.get_approved_entries()}

    def passes_proto016_gate(self) -> bool:
        """DEP-PROTO-016 completion gate: ≥3 approved entries across ≥2 story types.

        Spec: 'Completion gate: ≥3 approved entries across ≥2 story types'
        Both conditions must be true simultaneously.
        """
        approved = self.get_approved_entries()
        return len(approved) >= 3 and len(self.get_approved_story_types()) >= 2

    def query_by_cral_moment(self, cral_moment: str) -> list[CoachStoryEntry]:
        """Query approved stories by CRAL moment fit.

        Used by Context Reasoning Layer (Step 11-B): 'Does coach_story_archive
        contain a first-person story that outperforms external research for M4 RESONANT?'
        """
        return [
            e for e in self.get_approved_entries()
            if e.cral_moment_fit and cral_moment.upper() in e.cral_moment_fit.upper()
        ]


# ──────────────────────────────────────────────────────────────
# DEP-ENG-045 / DEP-ENG-025: Context Performance Registry
# Spec: Phase 0, Step 0-D — "Create empty context_performance_registry table entry.
# coach_id initialized. Confidence score defaults to routing rules until ≥5 sessions."
# Architecture §3.1: 'context_performance_registry (PK: registry_id): Maps context
# selection rationale against public performance metrics'
# ──────────────────────────────────────────────────────────────

class ContextSelectionObject(BaseModel):
    """DEP-ENG-025: Context Selection Object — logged per production session.

    Spec Step 11-B (Context Reasoning Layer): 'Answers logged as Context Selection
    Object → context_performance_registry'

    The 3 questions answered by Research Planner V4.0 before each session:
    Q1: Does coach_story_archive contain a first-person story for M4 RESONANT?
    Q2: Which CMM layers have strongest performance for this audience/trigger/arc phase?
    Q3: Which humor mechanism has strongest precedent for this arc phase and regulatory frame?
    """
    session_id: str = Field(..., description="The production session this object belongs to")
    coach_id: str = Field(..., description="Single-tenant scope — ADR-01")
    trigger_category: str = Field(..., description="The trigger category for this session")
    arc_phase: str = Field(..., description="The arc phase targeted this session")

    # Q1: Story Archive eligibility (M4 RESONANT)
    story_archive_queried: bool = Field(
        default=False,
        description="Whether coach_story_archive was queried for M4 RESONANT"
    )
    story_archive_used: bool = Field(
        default=False,
        description="AC5: 'selects that story over external research and logs story_archive_used: true'"
    )
    story_id_selected: Optional[str] = Field(
        default=None,
        description="Which story_id was selected for M4 RESONANT (if story_archive_used)"
    )

    # Q2: CMM layer performance weighting
    cmm_layers_queried: list[str] = Field(
        default_factory=list,
        description="Which CMM layers were checked for this session"
    )
    cmm_layer_selected: Optional[str] = Field(
        default=None,
        description="Which CMM layer had strongest performance precedent"
    )

    # Q3: Humor mechanism precedent
    humor_mechanism_queried: bool = Field(default=False)
    humor_mechanism_selected: Optional[str] = Field(
        default=None,
        description="Which humor mechanism had strongest precedent for this arc phase"
    )

    # Performance outcomes (populated after publication + Publer retrieval)
    performance_metrics: dict = Field(
        default_factory=dict,
        description="Post-publication metrics: likes, retweets, saves — populated by Data Analyst"
    )

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ContextPerformanceRegistry(BaseModel):
    """DEP-ENG-045: Context Performance Registry — initialized in Step 0-D.

    Spec: 'Create empty context_performance_registry table entry. coach_id initialized.
    Confidence score defaults to routing rules until ≥5 sessions are recorded.'
    """
    registry_id: str = Field(..., description="Primary key — PK: registry_id per Architecture §3.1")
    coach_id: str = Field(..., description="Single-tenant scope — ADR-01")
    status: str = Field(
        default="initialized",
        description="initialized | active | self_improving"
    )
    confidence_model: str = Field(
        default="default_routing_rules",
        description="Spec: 'defaults to routing rules until ≥5 sessions are recorded'"
    )
    session_count: int = Field(
        default=0,
        description="Number of production sessions logged. Confidence model upgrades at ≥5."
    )
    total_sessions: int = Field(
        default=0,
        description="Total sessions recorded across all batches (mirrors session_count)"
    )
    session_history: list[dict] = Field(
        default_factory=list,
        description="Per-session context selection + engagement outcome records"
    )
    context_selections: list[ContextSelectionObject] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def should_upgrade_confidence_model(self) -> bool:
        """Check if the confidence model should upgrade from default_routing_rules.

        Spec: 'defaults to routing rules until ≥5 sessions are recorded'
        At ≥5 sessions, the CPR has enough data to begin self-improving routing.
        """
        return self.session_count >= 5 and self.confidence_model == "default_routing_rules"

    def log_context_selection(self, selection: ContextSelectionObject) -> None:
        """Add a context selection object and increment session count."""
        self.context_selections.append(selection)
        self.session_count += 1
        self.updated_at = datetime.now(timezone.utc)
        if self.should_upgrade_confidence_model():
            self.confidence_model = "performance_weighted"
            self.status = "self_improving"


# ──────────────────────────────────────────────────────────────
# Humor Mechanism Registry — Step 0-C
# Spec: 'Create empty humor_mechanism_registry table entry for this coach.
# coach_id initialized. No entries yet — populated after first production sessions.'
# Architecture §3.1: 'humor_mechanism_registry (PK: registry_id): Logs successfully
# deployed humor arcs to ensure compliance with the Boredom Ban.'
# ──────────────────────────────────────────────────────────────

class HumorMechanismEntry(BaseModel):
    """A single humor mechanism deployment record.

    Populated after production sessions, not at initialization.
    Used by Boredom Ban (8-week rolling uniqueness enforcement).
    """
    entry_id: str = Field(..., description="Unique entry identifier")
    coach_id: str = Field(..., description="Single-tenant scope — ADR-01")
    mechanism_name: str = Field(..., description="The humor architecture name/ID")
    architectures_fired: list[str] = Field(
        default_factory=list,
        description="Which of the 14 humor architectures fired in this deployment"
    )
    arc_phase: str = Field(default="", description="The arc phase this humor was deployed in")
    session_id: str = Field(default="", description="Production session this belongs to")
    script_id: str = Field(default="", description="The specific script this humor was in")
    deployed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class HumorMechanismTag(BaseModel):
    """humor_mechanism_tag JSONB field on content_performance.

    Spec AC8: 'every generated script has a humor_mechanism_tag JSONB field populated
    in content_performance. An empty tag is not acceptable (if no humor architecture fires,
    the tag should contain {"architectures_fired": [], "reason": "no_applicable_mechanism"})'
    """
    architectures_fired: list[str] = Field(
        default_factory=list,
        description="Which humor architectures fired. Empty list is valid per spec AC8."
    )
    reason: Optional[str] = Field(
        default=None,
        description="Set to 'no_applicable_mechanism' when architectures_fired is empty"
    )
    primary_mechanism: Optional[str] = Field(
        default=None,
        description="The dominant humor architecture if multiple fired"
    )
    arc_phase: str = Field(default="", description="The arc phase this was applied in")
    confidence: float = Field(
        default=0.0,
        description="Classification confidence 0.0–1.0 from HumorMechanismTagger"
    )
    classified_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp of classification by HumorMechanismTagger (Step 11-D)"
    )

    def model_post_init(self, __context) -> None:
        """Enforce spec AC8: if no architectures fired, reason must be set."""
        if not self.architectures_fired and not self.reason:
            self.reason = "no_applicable_mechanism"


class HumorMechanismRegistry(BaseModel):
    """Humor Mechanism Registry — initialized empty in Step 0-C.

    Spec: 'Create empty humor_mechanism_registry table entry for this coach.
    coach_id initialized. No entries yet — populated after first production sessions.'
    Completion gate: 'Table entry exists (status: initialized)'
    """
    registry_id: str = Field(..., description="Primary key")
    coach_id: str = Field(..., description="Single-tenant scope — ADR-01")
    status: str = Field(
        default="initialized",
        description="initialized | active. Set to initialized at Step 0-C."
    )
    entries: list[HumorMechanismEntry] = Field(
        default_factory=list,
        description="Empty at initialization. Populated after production sessions."
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def get_recent_mechanisms(self, weeks: int = 8) -> list[str]:
        """Return mechanism names deployed within the rolling window.

        Used by Boredom Ban for 8-week rolling uniqueness check.
        """
        from datetime import timedelta
        cutoff = datetime.now(timezone.utc) - timedelta(weeks=weeks)
        recent = [e for e in self.entries if e.deployed_at >= cutoff]
        mechanisms: list[str] = []
        for entry in recent:
            mechanisms.extend(entry.architectures_fired)
        return mechanisms
