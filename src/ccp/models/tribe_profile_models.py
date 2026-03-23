"""
CCP FR6 Tribe Profile & Context Premise Map — Data Models (Unit 1)
Pydantic v2 models for all FR6 pipeline objects.

Spec reference: FR6 Tech Spec
  §Stage A — Tribe Soul Extraction (Genesis Setup)
  §Stage B — Context Premise Distillation & Neo4j Graph Persistence
  §Phase B2 — L1/L2/L3 Depth Stratification (Clark & Brennan 1991)
  §Phase B3 — T/V/R Emotional Mode Mapping
  §Phase B4 — Visual Recognition Code & Language Registry
  §Phase B5 — Coach-Tribe Resonance Cross-Reference
  §Phase B6 — Psychometric Extension Mapping (5 dimensions)
  §Phase B7 — Neo4j Graph Ontology
  §Phase B9 — 4 Laws of Tribe Profile Distillation

Architecture reference:
  §Layer 2 (MEMORY — Neo4j HGM)
  §5.2 (Corrected Intake Flow — Tribe Extraction)
  §Context_Premise_Trigger_Matching_Layer

Research basis:
  Clark & Brennan Common Ground Theory (1991)
  Tubbs et al. Mind After Midnight (2022)
  Suler Online Disinhibition (2004)
  Kozinets Netnography (2020)
  Higgins Regulatory Focus Theory (1997)
  Haidt MFT / MFQ-2 (2023)
  Lazarus & Folkman Transactional Model (1984)
  Fricker Epistemic Injustice (2007)
  Nader Reconsolidation (2000)
  Tedeschi & Calhoun PTG (2004)

Primary outputs:
  - tribe_profile.json (Stage A)
  - tribe_profile_distilled.json (Stage B)
  - DEP-ENG-006: Context Premise Map (Neo4j graph + JSON)
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


# ══════════════════════════════════════════════════════════════
# Enums
# ══════════════════════════════════════════════════════════════

class DepthLevel(str, Enum):
    """Clark & Brennan L1/L2/L3 depth stratification.
    L1 = public statements (performative broadcast)
    L2 = private struggles (communal in-group disclosure)
    L3 = unspoken feelings (authentic anonymous disinhibition, 2am test)
    """
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"


class EmotionalMode(str, Enum):
    """T/V/R emotional mode classification.
    T = Tension (confrontation, common enemies, injustices)
    V = Vulnerability (private pain, anxieties, taboos)
    R = Recognition (belonging, rituals, insider language)
    """
    TENSION = "T"
    VULNERABILITY = "V"
    RECOGNITION = "R"


class TriggerIntensity(str, Enum):
    """Activation intensity of a tribe emotional trigger."""
    DORMANT = "dormant"
    ACTIVE = "active"
    NUCLEAR = "nuclear"


class AuthenticationVerdict(str, Enum):
    """4 Laws of Tribe Profile Distillation verdict.
    AUTHENTICATED = 4/4 laws pass
    PROVISIONAL = 3/4 laws pass (usable with flags)
    FAILED = ≤2/4 pass (return to H11)
    """
    AUTHENTICATED = "AUTHENTICATED"
    PROVISIONAL = "PROVISIONAL"
    FAILED = "FAILED"


class RegulatoryFocus(str, Enum):
    """Higgins Regulatory Focus Theory (1997)."""
    PROMOTION = "promotion"
    PREVENTION = "prevention"
    MIXED = "mixed"


class MoralFoundationType(str, Enum):
    """Haidt MFT / MFQ-2 (2023): 6 moral foundations."""
    CARE_HARM = "care_harm"
    FAIRNESS_CHEATING = "fairness_cheating"
    LOYALTY_BETRAYAL = "loyalty_betrayal"
    AUTHORITY_SUBVERSION = "authority_subversion"
    SANCTITY_DEGRADATION = "sanctity_degradation"
    LIBERTY_OPPRESSION = "liberty_oppression"


class CopingTrajectoryPosition(str, Enum):
    """Lazarus & Folkman (1984) stress-coping cycle phase.
    SEARCH = peak intervention receptivity."""
    SEARCH = "search"
    ACTIVE = "active"
    EXHAUSTED = "exhausted"


class HermeneuticalGapMethod(str, Enum):
    """Fricker (2007) / Dotson (2011) — detection methods."""
    TRUNCATION = "truncation"
    PARABOLA = "parabola"
    NOVELTY = "novelty"


class LanguageRegisterType(str, Enum):
    """In-group language register classification."""
    SAFE = "safe"
    SACRED = "sacred"
    OUTSIDER = "outsider"


class VisualCodeType(str, Enum):
    """Visual recognition code classification."""
    INSIDER = "insider"
    REJECTION = "rejection"
    SACRED = "sacred"


class ResearchDimension(str, Enum):
    """The 4-dimension research planning framework."""
    CULTURAL_ARTIFACT = "cultural_artifact_archiving"
    HUMOR_PROFILE = "humor_profile_deconstruction"
    EMOTIONAL_LANDSCAPE = "emotional_landscape_mapping"
    SOCIAL_DYNAMICS = "social_dynamics_hierarchy"


class Neo4jNodeType(str, Enum):
    """Neo4j node types for the Context Premise graph ontology."""
    FRUSTRATION = "Frustration"
    WANT = "Want"
    DREAM = "Dream"
    FEAR = "Fear"
    SUSPICION = "Suspicion"
    INSECURITY = "Insecurity"
    ENVY_FEELING = "EnvyFeeling"
    ENEMY = "Enemy"
    COPING_MECHANISM = "CopingMechanism"
    HIDDEN_BELIEF = "HiddenBelief"
    EMOTIONAL_TRIGGER = "EmotionalTrigger"
    SUCCESS_MARKER = "SuccessMarker"
    SEGMENT = "Segment"
    HERMENEUTICAL_GAP = "HermeneuticalGap"


class Neo4jRelationshipType(str, Enum):
    """Neo4j relationship types for the Context Premise graph ontology."""
    TRIGGERS = "TRIGGERS"
    CONTRADICTS = "CONTRADICTS"
    FUELS = "FUELS"
    MASKS = "MASKS"
    VIOLATES = "VIOLATES"
    BELONGS_TO = "BELONGS_TO"
    AT_DEPTH = "AT_DEPTH"
    RESONATES_WITH = "RESONATES_WITH"


class TribeProfilePipelineStepStatus(str, Enum):
    """Pipeline step status tracking."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    FAILED = "failed"
    SKIPPED = "skipped"


# ══════════════════════════════════════════════════════════════
# Base Entry Models (atomic units)
# ══════════════════════════════════════════════════════════════

class DepthStratifiedEntry(BaseModel):
    """A single entry in any of the 12 base dimensions,
    with depth/mode/intensity classification per spec §Phase B2–B3."""
    text: str = ""
    depth: DepthLevel = DepthLevel.L1
    mode: EmotionalMode = EmotionalMode.TENSION
    intensity: TriggerIntensity = TriggerIntensity.DORMANT
    source: str = ""
    source_platform: str = ""
    provenance_score: float = Field(default=0.0, ge=0.0, le=1.0)
    liwc_authenticity_score: Optional[float] = Field(
        default=None, ge=0.0, le=1.0,
        description="LIWC-22 authenticity percentile for L3 verification",
    )


class EmotionalTriggerEntry(DepthStratifiedEntry):
    """Extended entry for the emotional_triggers dimension.
    Includes activation keywords and moral foundation mapping."""
    activation_keywords: list[str] = Field(default_factory=list)
    activation_conditions: str = ""
    moral_foundation: Optional[MoralFoundationType] = None


class CopingMechanismEntry(DepthStratifiedEntry):
    """Extended entry for the coping_mechanism dimension.
    Includes Lazarus & Folkman trajectory position."""
    trajectory_position: Optional[CopingTrajectoryPosition] = None


# ══════════════════════════════════════════════════════════════
# Visual Recognition Codes (Phase B4)
# ══════════════════════════════════════════════════════════════

class VisualRecognitionCode(BaseModel):
    """A single visual recognition code entry.
    Spec §Phase B4: insider objects, rejection triggers, sacred objects."""
    code_type: VisualCodeType = VisualCodeType.INSIDER
    description: str = ""
    tribe_significance: str = ""
    handling_notes: str = Field(
        default="",
        description="Sacred objects: handling instructions",
    )
    examples: list[str] = Field(default_factory=list)


# ══════════════════════════════════════════════════════════════
# In-Group Language Registry (Phase B4)
# ══════════════════════════════════════════════════════════════

class LanguageRegistryEntry(BaseModel):
    """A single in-group language term.
    Spec §Phase B4: safe/sacred/outsider vocabulary."""
    term: str = ""
    register: LanguageRegisterType = LanguageRegisterType.SAFE
    context: str = ""
    emotional_register: str = ""
    example_usage: str = ""
    # Sacred-specific
    required_mode: Optional[EmotionalMode] = None
    misuse_risk: str = ""
    # Outsider-specific
    why_rejected: str = ""
    use_instead: str = ""


# ══════════════════════════════════════════════════════════════
# Anti-Aspirational Markers (Law 4 extension)
# ══════════════════════════════════════════════════════════════

class AntiAspirationalMarker(BaseModel):
    """Something the tribe actively rejects.
    Spec §Phase A3 3D: performative wellness, fake inclusivity, tourist language, etc."""
    marker: str = ""
    why_rejected: str = ""
    evidence_quotes: list[str] = Field(default_factory=list)


# ══════════════════════════════════════════════════════════════
# Volume Quota Configuration (Stage A validation)
# ══════════════════════════════════════════════════════════════

class VolumeQuotaResult(BaseModel):
    """Result of checking a single volume quota against the spec thresholds."""
    field_name: str = ""
    required_minimum: int = 0
    actual_count: int = 0
    passed: bool = False

    def check(self) -> bool:
        """Evaluate pass/fail."""
        self.passed = self.actual_count >= self.required_minimum
        return self.passed


# ══════════════════════════════════════════════════════════════
# Tribe Profile — Stage A Output (tribe_profile.json)
# ══════════════════════════════════════════════════════════════

class TribeSlangItem(BaseModel):
    """A slang term with context and mode tag."""
    term: str = ""
    definition: str = ""
    example_quote: str = ""
    mode: Optional[EmotionalMode] = None


class InsideJokeItem(BaseModel):
    """An inside joke with reference and mode tag."""
    joke_reference: str = ""
    context: str = ""
    example_quote: str = ""
    mode: Optional[EmotionalMode] = None


class HeroEnemyItem(BaseModel):
    """A shared hero or common enemy."""
    name: str = ""
    role: str = Field(default="hero", description="'hero' or 'enemy'")
    evidence_quote: str = ""


class HumorExampleItem(BaseModel):
    """A humor example with style classification."""
    style: str = ""
    content: str = ""
    source: str = ""


class HumorTargetItem(BaseModel):
    """A humor target with example joke."""
    target: str = ""
    example_joke: str = ""


class TabooItem(BaseModel):
    """A humor taboo / no-go zone."""
    topic: str = ""
    evidence_reaction: str = ""


class EmotionalQuoteItem(BaseModel):
    """A verbatim emotional quote (aspiration/anxiety)."""
    text: str = ""
    source: str = ""
    depth: DepthLevel = DepthLevel.L1


class HighArousalTriggerItem(BaseModel):
    """A high-arousal trigger event type with reaction quote."""
    event_type: str = ""
    valence: str = Field(default="positive", description="'positive' or 'negative'")
    reaction_quote: str = ""


class CulturalArtifactsSection(BaseModel):
    """Spec §Phase A3 3A: Cultural artifacts extracted."""
    tribe_slang: list[TribeSlangItem] = Field(default_factory=list)
    inside_jokes: list[InsideJokeItem] = Field(default_factory=list)
    shared_heroes: list[HeroEnemyItem] = Field(default_factory=list)
    common_enemies: list[HeroEnemyItem] = Field(default_factory=list)


class HumorProfileSection(BaseModel):
    """Spec §Phase A3 3B: Humor DNA profiling."""
    dominant_style: str = ""
    secondary_style: str = ""
    style_examples: list[HumorExampleItem] = Field(default_factory=list)
    humor_targets: list[HumorTargetItem] = Field(default_factory=list)
    taboos_and_no_go_zones: list[TabooItem] = Field(default_factory=list)


class EmotionalResonanceSection(BaseModel):
    """Spec §Phase A3 3C: Emotional resonance mapping."""
    primary_aspirations: list[EmotionalQuoteItem] = Field(default_factory=list)
    core_anxieties: list[EmotionalQuoteItem] = Field(default_factory=list)
    high_arousal_triggers: list[HighArousalTriggerItem] = Field(default_factory=list)


class TribeProfile(BaseModel):
    """Spec §Phase A4 EMIT: Stage A output — tribe_profile.json.
    Raw tribe cultural intelligence extracted from H11 Dossier."""
    coach_id: str = ""
    coach_acronym: str = ""
    version: int = Field(default=1, ge=1)
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )

    # §Phase A3 3A
    cultural_artifacts: CulturalArtifactsSection = Field(
        default_factory=CulturalArtifactsSection,
    )
    # §Phase A3 3B
    humor_profile: HumorProfileSection = Field(
        default_factory=HumorProfileSection,
    )
    # §Phase A3 3C
    emotional_resonance: EmotionalResonanceSection = Field(
        default_factory=EmotionalResonanceSection,
    )
    # §Phase A3 3D — Law extensions
    visual_recognition_codes: list[VisualRecognitionCode] = Field(
        default_factory=list,
    )
    anti_aspirational_markers: list[AntiAspirationalMarker] = Field(
        default_factory=list,
    )
    # Depth distribution from Stage A (pre-distillation)
    depth_distribution: dict[str, float] = Field(
        default_factory=lambda: {"surface": 0.0, "mechanism": 0.0, "collision": 0.0},
    )

    # ── Volume Quota Validation (AC3) ──

    def validate_volume_quotas(self) -> list[VolumeQuotaResult]:
        """Spec §Phase A5 VALIDATE: Check all volume quotas.
        Returns list of quota results; any failure → validation fails."""
        quotas = [
            VolumeQuotaResult(
                field_name="tribe_slang",
                required_minimum=10,
                actual_count=len(self.cultural_artifacts.tribe_slang),
            ),
            VolumeQuotaResult(
                field_name="inside_jokes",
                required_minimum=5,
                actual_count=len(self.cultural_artifacts.inside_jokes),
            ),
            VolumeQuotaResult(
                field_name="shared_heroes",
                required_minimum=5,
                actual_count=len(self.cultural_artifacts.shared_heroes),
            ),
            VolumeQuotaResult(
                field_name="common_enemies",
                required_minimum=5,
                actual_count=len(self.cultural_artifacts.common_enemies),
            ),
            VolumeQuotaResult(
                field_name="humor_style_examples",
                required_minimum=3,
                actual_count=len(self.humor_profile.style_examples),
            ),
            VolumeQuotaResult(
                field_name="humor_targets",
                required_minimum=5,
                actual_count=len(self.humor_profile.humor_targets),
            ),
            VolumeQuotaResult(
                field_name="taboos_and_no_go_zones",
                required_minimum=2,
                actual_count=len(self.humor_profile.taboos_and_no_go_zones),
            ),
            VolumeQuotaResult(
                field_name="primary_aspirations",
                required_minimum=5,
                actual_count=len(self.emotional_resonance.primary_aspirations),
            ),
            VolumeQuotaResult(
                field_name="core_anxieties",
                required_minimum=5,
                actual_count=len(self.emotional_resonance.core_anxieties),
            ),
            VolumeQuotaResult(
                field_name="high_arousal_positive_triggers",
                required_minimum=3,
                actual_count=len([
                    t for t in self.emotional_resonance.high_arousal_triggers
                    if t.valence == "positive"
                ]),
            ),
            VolumeQuotaResult(
                field_name="high_arousal_negative_triggers",
                required_minimum=3,
                actual_count=len([
                    t for t in self.emotional_resonance.high_arousal_triggers
                    if t.valence == "negative"
                ]),
            ),
            VolumeQuotaResult(
                field_name="visual_insider_objects",
                required_minimum=5,
                actual_count=len([
                    v for v in self.visual_recognition_codes
                    if v.code_type == VisualCodeType.INSIDER
                ]),
            ),
            VolumeQuotaResult(
                field_name="visual_rejection_triggers",
                required_minimum=3,
                actual_count=len([
                    v for v in self.visual_recognition_codes
                    if v.code_type == VisualCodeType.REJECTION
                ]),
            ),
            VolumeQuotaResult(
                field_name="anti_aspirational_markers",
                required_minimum=3,
                actual_count=len(self.anti_aspirational_markers),
            ),
        ]
        for q in quotas:
            q.check()
        return quotas

    def passes_all_volume_quotas(self) -> bool:
        """AC3: True only if ALL volume quotas are met."""
        return all(q.passed for q in self.validate_volume_quotas())


# ══════════════════════════════════════════════════════════════
# Context Premise Dimension (12 base dimensions)
# ══════════════════════════════════════════════════════════════

class ContextPremiseDimension(BaseModel):
    """A single dimension within the Context Premise Map.
    Contains depth-stratified entries per spec §Phase B2."""
    entries: list[DepthStratifiedEntry] = Field(default_factory=list)

    def get_entries_at_depth(self, depth: DepthLevel) -> list[DepthStratifiedEntry]:
        """Filter entries by depth level."""
        return [e for e in self.entries if e.depth == depth]

    def get_entries_by_mode(self, mode: EmotionalMode) -> list[DepthStratifiedEntry]:
        """Filter entries by emotional mode."""
        return [e for e in self.entries if e.mode == mode]


class EmotionalTriggerDimension(BaseModel):
    """Extended dimension for emotional_triggers with activation data."""
    entries: list[EmotionalTriggerEntry] = Field(default_factory=list)

    def get_entries_at_depth(self, depth: DepthLevel) -> list[EmotionalTriggerEntry]:
        return [e for e in self.entries if e.depth == depth]

    def get_entries_by_mode(self, mode: EmotionalMode) -> list[EmotionalTriggerEntry]:
        return [e for e in self.entries if e.mode == mode]


class CopingMechanismDimension(BaseModel):
    """Extended dimension for coping_mechanism with trajectory data."""
    entries: list[CopingMechanismEntry] = Field(default_factory=list)

    def get_entries_at_depth(self, depth: DepthLevel) -> list[CopingMechanismEntry]:
        return [e for e in self.entries if e.depth == depth]


# ══════════════════════════════════════════════════════════════
# Psychometric Extensions (Phase B6 — 5 dimensions)
# ══════════════════════════════════════════════════════════════

class HermeneuticalGapMarker(BaseModel):
    """Spec §Phase B6: Fricker (2007) / Dotson (2011).
    Evidence of unarticulated experience."""
    text: str = ""
    detection_method: HermeneuticalGapMethod = HermeneuticalGapMethod.TRUNCATION
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class ReconsolidationEngagementProxies(BaseModel):
    """Spec §Phase B6: Nader (2000) — behavioral engagement proxies."""
    save_rate: float = Field(default=0.0, ge=0.0)
    comment_depth: float = Field(default=0.0, ge=0.0)
    share_velocity: float = Field(default=0.0, ge=0.0)
    dm_response_rate: float = Field(default=0.0, ge=0.0)


class ReconsolidationSensitivityExt(BaseModel):
    """Spec §Phase B6: Audience reconsolidation sensitivity."""
    overall_score: float = Field(default=0.0, ge=0.0, le=10.0)
    engagement_proxies: ReconsolidationEngagementProxies = Field(
        default_factory=ReconsolidationEngagementProxies,
    )


class MoralFoundationViolated(BaseModel):
    """Spec §Phase B6: Haidt MFT/MFQ-2 — audience moral foundation."""
    primary: Optional[MoralFoundationType] = None
    secondary: Optional[MoralFoundationType] = None
    weighting: dict[str, float] = Field(default_factory=dict)


class PsychometricExtensions(BaseModel):
    """Spec §Phase B6: 5 psychometric extension dimensions."""
    regulatory_focus_orientation: RegulatoryFocus = RegulatoryFocus.MIXED
    moral_foundation_violated: MoralFoundationViolated = Field(
        default_factory=MoralFoundationViolated,
    )
    coping_trajectory_position: CopingTrajectoryPosition = CopingTrajectoryPosition.SEARCH
    hermeneutical_gap_markers: list[HermeneuticalGapMarker] = Field(
        default_factory=list,
    )
    reconsolidation_sensitivity: ReconsolidationSensitivityExt = Field(
        default_factory=ReconsolidationSensitivityExt,
    )


# ══════════════════════════════════════════════════════════════
# Audience Segment
# ══════════════════════════════════════════════════════════════

class AudienceSegment(BaseModel):
    """Spec §Phase B7: Audience segment for Neo4j graph."""
    segment_id: str = ""
    dhd_label: str = ""
    regulatory_focus: RegulatoryFocus = RegulatoryFocus.MIXED
    coping_stage: CopingTrajectoryPosition = CopingTrajectoryPosition.SEARCH
    reconsolidation_readiness: float = Field(default=0.0, ge=0.0, le=10.0)


# ══════════════════════════════════════════════════════════════
# Coach-Tribe Resonance Cross-Reference (Phase B5)
# ══════════════════════════════════════════════════════════════

class AlignmentPoint(BaseModel):
    """Where coach's philosophy addresses tribe's pain."""
    coach_belief: str = ""
    tribe_pain: str = ""
    leverage_description: str = ""


class FrictionPoint(BaseModel):
    """Where coach's belief contradicts tribe's experience."""
    coach_belief: str = ""
    tribe_experience: str = ""
    risk_description: str = ""


class GapAnalysis(BaseModel):
    """Tribe pains the coach's philosophy doesn't address yet."""
    tribe_pain: str = ""
    opportunity_description: str = ""


class CoachTribeResonance(BaseModel):
    """Spec §Phase B5: Coach-tribe resonance cross-reference.
    Missing friction is a red flag per spec."""
    alignment_points: list[AlignmentPoint] = Field(default_factory=list)
    friction_points: list[FrictionPoint] = Field(default_factory=list)
    gaps: list[GapAnalysis] = Field(default_factory=list)

    def passes_resonance_gate(self) -> bool:
        """AC12: ≥3 alignment points AND ≥1 friction point."""
        return (
            len(self.alignment_points) >= 3
            and len(self.friction_points) >= 1
        )

    def has_zero_friction_warning(self) -> bool:
        """Spec: Zero friction points → WARNING: relationship is idealized."""
        return len(self.friction_points) == 0


# ══════════════════════════════════════════════════════════════
# Depth Distribution & Mode Distribution
# ══════════════════════════════════════════════════════════════

class DepthDistribution(BaseModel):
    """Spec §Phase B2 hard gate: L2 ≥30%, L3 ≥10%."""
    l1_ratio: float = Field(default=0.0, ge=0.0, le=1.0)
    l2_ratio: float = Field(default=0.0, ge=0.0, le=1.0)
    l3_ratio: float = Field(default=0.0, ge=0.0, le=1.0)

    def passes_depth_gate(self) -> bool:
        """AC4: L2 ≥30% AND L3 ≥10%."""
        return self.l2_ratio >= 0.30 and self.l3_ratio >= 0.10


class ModeDistribution(BaseModel):
    """Spec §Phase B3 gate: ≥3 triggers per mode (T/V/R)."""
    tension_count: int = Field(default=0, ge=0)
    vulnerability_count: int = Field(default=0, ge=0)
    recognition_count: int = Field(default=0, ge=0)

    def passes_mode_gate(self) -> bool:
        """AC5: ≥3 triggers per mode."""
        return (
            self.tension_count >= 3
            and self.vulnerability_count >= 3
            and self.recognition_count >= 3
        )

    def is_mode_incomplete(self) -> bool:
        """Any mode <3 → MODE-INCOMPLETE."""
        return not self.passes_mode_gate()


# ══════════════════════════════════════════════════════════════
# 4 Laws Validation Result (Phase B9)
# ══════════════════════════════════════════════════════════════

class LawValidationResult(BaseModel):
    """Result of a single Law check in the 4 Laws of Tribe Profile Distillation."""
    law_number: int = 0
    law_name: str = ""
    checks: list[str] = Field(default_factory=list)
    checks_passed: list[bool] = Field(default_factory=list)
    passed: bool = False

    def evaluate(self) -> bool:
        """A law passes only if ALL its checks pass."""
        self.passed = all(self.checks_passed) if self.checks_passed else False
        return self.passed


class FourLawsValidation(BaseModel):
    """Spec §Phase B9: 4 Laws of Tribe Profile Distillation.
    Verdict: AUTHENTICATED (4/4), PROVISIONAL (3/4), FAILED (≤2/4)."""
    law_1_mode_mapped: LawValidationResult = Field(default_factory=LawValidationResult)
    law_2_visual_codes: LawValidationResult = Field(default_factory=LawValidationResult)
    law_3_language_registry: LawValidationResult = Field(default_factory=LawValidationResult)
    law_4_authenticity_gate: LawValidationResult = Field(default_factory=LawValidationResult)

    def laws_passing(self) -> int:
        """Count how many laws passed."""
        return sum([
            self.law_1_mode_mapped.passed,
            self.law_2_visual_codes.passed,
            self.law_3_language_registry.passed,
            self.law_4_authenticity_gate.passed,
        ])

    def get_verdict(self) -> AuthenticationVerdict:
        """AC11: Determine authentication verdict."""
        count = self.laws_passing()
        if count == 4:
            return AuthenticationVerdict.AUTHENTICATED
        elif count == 3:
            return AuthenticationVerdict.PROVISIONAL
        else:
            return AuthenticationVerdict.FAILED


# ══════════════════════════════════════════════════════════════
# Neo4j Graph Node & Relationship Models (Phase B7)
# ══════════════════════════════════════════════════════════════

class GraphNode(BaseModel):
    """A typed node for Neo4j persistence.
    Per-coach isolation enforced via coach_id property."""
    node_type: Neo4jNodeType
    coach_id: str = ""
    text: str = ""
    depth_level: Optional[DepthLevel] = None
    mode: Optional[EmotionalMode] = None
    intensity: Optional[TriggerIntensity] = None
    source_evidence: str = ""
    provenance_score: float = Field(default=0.0, ge=0.0, le=1.0)
    # Extended fields for specific node types
    trajectory_position: Optional[CopingTrajectoryPosition] = None
    activation_keywords: list[str] = Field(default_factory=list)
    moral_foundation: Optional[MoralFoundationType] = None
    # Segment-specific
    segment_id: str = ""
    dhd_label: str = ""
    regulatory_focus: Optional[RegulatoryFocus] = None
    coping_stage: Optional[CopingTrajectoryPosition] = None
    reconsolidation_readiness: float = Field(default=0.0, ge=0.0, le=10.0)
    # HermeneuticalGap-specific
    detection_method: Optional[HermeneuticalGapMethod] = None
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    # Internal ID
    node_id: str = ""


class GraphRelationship(BaseModel):
    """A typed relationship between two Neo4j nodes."""
    relationship_type: Neo4jRelationshipType
    source_node_id: str = ""
    target_node_id: str = ""
    properties: dict[str, Any] = Field(default_factory=dict)


# ══════════════════════════════════════════════════════════════
# Tribe Profile Distilled — Stage B Output
# (tribe_profile_distilled.json = DEP-ENG-006 JSON serialization)
# ══════════════════════════════════════════════════════════════

class TribeProfileDistilled(BaseModel):
    """Spec §Phase B8 EMIT: Stage B output — tribe_profile_distilled.json.
    Mode-mapped, depth-stratified profile. JSON serialization of DEP-ENG-006.
    This is the Context Premise Map."""
    dep_id: str = "DEP-ENG-006"
    version: str = "3.0"
    coach_id: str = ""
    coach_acronym: str = ""

    # 12 base dimensions (spec §Context Premise Map Schema)
    frustrations: ContextPremiseDimension = Field(default_factory=ContextPremiseDimension)
    wants: ContextPremiseDimension = Field(default_factory=ContextPremiseDimension)
    dreams: ContextPremiseDimension = Field(default_factory=ContextPremiseDimension)
    fears: ContextPremiseDimension = Field(default_factory=ContextPremiseDimension)
    suspicions: ContextPremiseDimension = Field(default_factory=ContextPremiseDimension)
    insecurities: ContextPremiseDimension = Field(default_factory=ContextPremiseDimension)
    envy_feelings: ContextPremiseDimension = Field(default_factory=ContextPremiseDimension)
    enemies: ContextPremiseDimension = Field(default_factory=ContextPremiseDimension)
    coping_mechanism: CopingMechanismDimension = Field(default_factory=CopingMechanismDimension)
    hidden_beliefs: ContextPremiseDimension = Field(default_factory=ContextPremiseDimension)
    emotional_triggers: EmotionalTriggerDimension = Field(default_factory=EmotionalTriggerDimension)
    success_markers: ContextPremiseDimension = Field(default_factory=ContextPremiseDimension)

    # 5 psychometric extensions (spec §Phase B6)
    psychometric_extensions: PsychometricExtensions = Field(
        default_factory=PsychometricExtensions,
    )

    # Audience segments
    segments: list[AudienceSegment] = Field(default_factory=list)

    # Distribution metrics
    depth_distribution: DepthDistribution = Field(default_factory=DepthDistribution)
    mode_distribution: ModeDistribution = Field(default_factory=ModeDistribution)

    # Coach-Tribe Resonance (Phase B5)
    coach_tribe_resonance: CoachTribeResonance = Field(
        default_factory=CoachTribeResonance,
    )

    # Visual & Language (Phase B4)
    visual_recognition_codes: list[VisualRecognitionCode] = Field(
        default_factory=list,
    )
    language_registry: list[LanguageRegistryEntry] = Field(
        default_factory=list,
    )

    # 4 Laws Validation (Phase B9)
    four_laws_validation: FourLawsValidation = Field(
        default_factory=FourLawsValidation,
    )
    authentication_status: AuthenticationVerdict = AuthenticationVerdict.FAILED

    # Metadata
    last_updated: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )

    # ── Computed helpers ──

    def get_all_entries(self) -> list[DepthStratifiedEntry]:
        """Get all entries across all 12 dimensions for distribution calculation."""
        all_entries: list[DepthStratifiedEntry] = []
        for dim_name in [
            "frustrations", "wants", "dreams", "fears", "suspicions",
            "insecurities", "envy_feelings", "enemies", "hidden_beliefs",
            "success_markers",
        ]:
            dim: ContextPremiseDimension = getattr(self, dim_name)
            all_entries.extend(dim.entries)
        # Coping mechanism
        all_entries.extend(self.coping_mechanism.entries)
        # Emotional triggers
        all_entries.extend(self.emotional_triggers.entries)
        return all_entries

    def compute_depth_distribution(self) -> DepthDistribution:
        """Calculate depth ratios across all entries."""
        entries = self.get_all_entries()
        total = len(entries)
        if total == 0:
            self.depth_distribution = DepthDistribution()
            return self.depth_distribution
        l1_count = sum(1 for e in entries if e.depth == DepthLevel.L1)
        l2_count = sum(1 for e in entries if e.depth == DepthLevel.L2)
        l3_count = sum(1 for e in entries if e.depth == DepthLevel.L3)
        self.depth_distribution = DepthDistribution(
            l1_ratio=l1_count / total,
            l2_ratio=l2_count / total,
            l3_ratio=l3_count / total,
        )
        return self.depth_distribution

    def compute_mode_distribution(self) -> ModeDistribution:
        """Calculate mode counts for emotional triggers."""
        t_entries = self.emotional_triggers.get_entries_by_mode(EmotionalMode.TENSION)
        v_entries = self.emotional_triggers.get_entries_by_mode(EmotionalMode.VULNERABILITY)
        r_entries = self.emotional_triggers.get_entries_by_mode(EmotionalMode.RECOGNITION)
        self.mode_distribution = ModeDistribution(
            tension_count=len(t_entries),
            vulnerability_count=len(v_entries),
            recognition_count=len(r_entries),
        )
        return self.mode_distribution

    def get_safe_terms(self) -> list[LanguageRegistryEntry]:
        """Get all SAFE vocabulary terms."""
        return [e for e in self.language_registry if e.register == LanguageRegisterType.SAFE]

    def get_outsider_terms(self) -> list[LanguageRegistryEntry]:
        """Get all OUTSIDER vocabulary terms."""
        return [e for e in self.language_registry if e.register == LanguageRegisterType.OUTSIDER]

    def get_sacred_terms(self) -> list[LanguageRegistryEntry]:
        """Get all SACRED vocabulary terms."""
        return [e for e in self.language_registry if e.register == LanguageRegisterType.SACRED]

    def get_insider_visuals(self) -> list[VisualRecognitionCode]:
        """Get insider visual codes."""
        return [v for v in self.visual_recognition_codes if v.code_type == VisualCodeType.INSIDER]

    def get_rejection_visuals(self) -> list[VisualRecognitionCode]:
        """Get rejection visual codes."""
        return [v for v in self.visual_recognition_codes if v.code_type == VisualCodeType.REJECTION]

    def get_sacred_visuals(self) -> list[VisualRecognitionCode]:
        """Get sacred visual codes."""
        return [v for v in self.visual_recognition_codes if v.code_type == VisualCodeType.SACRED]

    def is_failed(self) -> bool:
        """Check if this profile is FAILED — cannot feed downstream."""
        return self.authentication_status == AuthenticationVerdict.FAILED


# ══════════════════════════════════════════════════════════════
# Pipeline Session Tracking
# ══════════════════════════════════════════════════════════════

class TribeProfilePipelineSession(BaseModel):
    """Session state for the FR6 two-stage pipeline."""
    coach_id: str = ""
    coach_acronym: str = ""
    started_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )
    completed_at: Optional[str] = None

    # Stage A steps
    stage_a_ingest: TribeProfilePipelineStepStatus = TribeProfilePipelineStepStatus.PENDING
    stage_a_research_planning: TribeProfilePipelineStepStatus = TribeProfilePipelineStepStatus.PENDING
    stage_a_cultural_harvesting: TribeProfilePipelineStepStatus = TribeProfilePipelineStepStatus.PENDING
    stage_a_emit: TribeProfilePipelineStepStatus = TribeProfilePipelineStepStatus.PENDING
    stage_a_validate: TribeProfilePipelineStepStatus = TribeProfilePipelineStepStatus.PENDING
    stage_a_checkpoint: TribeProfilePipelineStepStatus = TribeProfilePipelineStepStatus.PENDING

    # Stage B steps
    stage_b_ingest: TribeProfilePipelineStepStatus = TribeProfilePipelineStepStatus.PENDING
    stage_b_depth_stratification: TribeProfilePipelineStepStatus = TribeProfilePipelineStepStatus.PENDING
    stage_b_mode_mapping: TribeProfilePipelineStepStatus = TribeProfilePipelineStepStatus.PENDING
    stage_b_visual_language: TribeProfilePipelineStepStatus = TribeProfilePipelineStepStatus.PENDING
    stage_b_resonance: TribeProfilePipelineStepStatus = TribeProfilePipelineStepStatus.PENDING
    stage_b_psychometric: TribeProfilePipelineStepStatus = TribeProfilePipelineStepStatus.PENDING
    stage_b_neo4j: TribeProfilePipelineStepStatus = TribeProfilePipelineStepStatus.PENDING
    stage_b_emit: TribeProfilePipelineStepStatus = TribeProfilePipelineStepStatus.PENDING
    stage_b_validate: TribeProfilePipelineStepStatus = TribeProfilePipelineStepStatus.PENDING
    stage_b_checkpoint: TribeProfilePipelineStepStatus = TribeProfilePipelineStepStatus.PENDING

    # Receipt IDs
    receipt_tribe_ingest: str = ""
    receipt_tribe_emit: str = ""
    receipt_distill_ingest: str = ""
    receipt_distill_emit: str = ""

    # Outputs
    tribe_profile_path: str = ""
    tribe_profile_distilled_path: str = ""
    h9_receipt_path: str = ""

    def is_stage_a_complete(self) -> bool:
        """Check if all Stage A steps are complete."""
        return all(
            getattr(self, f"stage_a_{step}") == TribeProfilePipelineStepStatus.COMPLETE
            for step in [
                "ingest", "research_planning", "cultural_harvesting",
                "emit", "validate", "checkpoint",
            ]
        )

    def is_stage_b_complete(self) -> bool:
        """Check if all Stage B steps are complete."""
        return all(
            getattr(self, f"stage_b_{step}") == TribeProfilePipelineStepStatus.COMPLETE
            for step in [
                "ingest", "depth_stratification", "mode_mapping",
                "visual_language", "resonance", "psychometric",
                "neo4j", "emit", "validate", "checkpoint",
            ]
        )

    def is_complete(self) -> bool:
        """Full pipeline complete."""
        return self.is_stage_a_complete() and self.is_stage_b_complete()


# ══════════════════════════════════════════════════════════════
# Backward Compatibility Result (AC13)
# ══════════════════════════════════════════════════════════════

class ContextPremiseFallbackResult(BaseModel):
    """Spec §Backward Compatibility: Result when Context Premise Map
    doesn't exist. Content generated using topic-based prompts from
    coach_soul.json. Trigger Matching Layer gracefully degrades."""
    used_fallback: bool = True
    reason: str = "Context Premise Map (DEP-ENG-006) not found"
    coach_soul_path: str = ""
    limitations: list[str] = Field(
        default_factory=lambda: [
            "Content without Context Premise Map delivers professional empathy only",
            "Trigger Matching Layer 4-axis engine cannot execute",
            "Archetype selection uses coach emotional state only, not audience mode routing",
            "DARN-CAT questions are topic-generic, not L3-vocabulary-anchored",
        ],
    )
    fallback_content_seed: dict[str, Any] = Field(
        default_factory=dict,
        description="Topic-based prompts derived from coach_soul.json",
    )
