"""
Audience Deep Trigger Data Models — Pydantic Schemas

Type-safe contracts for the Audience Deep Trigger Map: the audience-side
equivalent of the coach's trigger_map.json. These models encode 7 research
dimensions into a single AudienceTriggerProfile that mirrors the quantitative
precision of the coach-side MFQ-2 profile.

Research Mapping:
    RegulatoryFocusProfile   → Higgins' Regulatory Focus Theory (RFT)
    MoralEmotionProfile      → Haidt MFT + Tangney moral emotion taxonomy
    CopingTrajectoryPosition → Lazarus & Folkman transactional model
    HermeneuticalGapProfile  → Fricker/Dotson testimonial smothering
    ReconsolidationMarkers   → Nader memory reconsolidation + prediction error
    AuthenticityScore        → Kozinets L-depth + Pennebaker LIWC-22 proxy

Architecture Layer: Context Premise Engine (Audience Side)
Consumed by: audience_aggregator.py → intersection_engine.py → blueprint_orchestrator.py
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime


# ─── Enums ───────────────────────────────────────────────────────────

class RegulatoryOrientation(str, Enum):
    """
    Higgins' Regulatory Focus Theory (1997).
    Promotion = ideal-self pursuit, eagerness strategies, gain-seeking.
    Prevention = ought-self fulfillment, vigilance strategies, loss-avoidance.
    Dual-dominant = no clear differential (Δ < 0.15 threshold).
    """
    PROMOTION = "PROMOTION"
    PREVENTION = "PREVENTION"
    DUAL_DOMINANT = "DUAL_DOMINANT"


class CopingPhase(str, Enum):
    """
    Lazarus & Folkman Transactional Model phases.
    The SEARCH_PHASE is the critical detection target — it represents
    peak intervention receptivity (the person is actively seeking help).
    """
    PRE_CONTEMPLATION = "PRE_CONTEMPLATION"
    SEARCH_PHASE = "SEARCH_PHASE"
    ACTIVE_COPING = "ACTIVE_COPING"
    MAINTENANCE = "MAINTENANCE"


class LDepth(str, Enum):
    """
    L-depth framework (Kozinets netnography + circadian neurobiology).
    L1 = broadcast-mode, polished, high self-monitoring.
    L2 = communal in-group, semi-private, moderate authenticity.
    L3 = anonymous disinhibition, raw unpolished, 2am-test pass.
    """
    L1_PERFORMATIVE = "L1_PERFORMATIVE"
    L2_COMMUNAL = "L2_COMMUNAL"
    L3_AUTHENTIC = "L3_AUTHENTIC"


class MoralFoundation(str, Enum):
    """
    Haidt's Moral Foundations Theory (MFT) — 6-foundation model.
    Used for both coach-side (MFQ-2 instrument) and audience-side
    (reverse-engineered from moral emotion linguistic signatures).
    """
    CARE_HARM = "CARE_HARM"
    FAIRNESS_CHEATING = "FAIRNESS_CHEATING"
    LOYALTY_BETRAYAL = "LOYALTY_BETRAYAL"
    AUTHORITY_SUBVERSION = "AUTHORITY_SUBVERSION"
    SANCTITY_DEGRADATION = "SANCTITY_DEGRADATION"
    LIBERTY_OPPRESSION = "LIBERTY_OPPRESSION"


class DataPhase(str, Enum):
    """
    3-phase audience data lifecycle (from Audience Data Sourcing Analysis).
    COLD = <10 analyzed texts, Mode C (Hermeneutical Scan only).
    WARM = 10-50 texts, Mode B (Partial Depth).
    HOT  = >50 texts, Mode A (Full Depth).
    """
    COLD = "COLD"
    WARM = "WARM"
    HOT = "HOT"


class ConfidenceLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


# ─── Sub-Profile 1: Regulatory Focus ────────────────────────────────

class RegulatoryFocusProfile(BaseModel):
    """
    Higgins' Regulatory Focus Theory — linguistic extraction.

    Eagerness (promotion) vs. vigilance (prevention) detected from
    language patterns: abstract vs. concrete verbs, gain vs. loss
    vocabulary, ideal-self vs. ought-self referencing.

    Research: ACL Anthology (2023) — "Prevention or Promotion?
    Predicting Author's Regulatory Focus"
    """
    eagerness_score: float = Field(
        0.0, ge=0.0, le=1.0,
        description="Promotion orientation strength (0=absent, 1=dominant)"
    )
    vigilance_score: float = Field(
        0.0, ge=0.0, le=1.0,
        description="Prevention orientation strength (0=absent, 1=dominant)"
    )
    dominant_orientation: RegulatoryOrientation = RegulatoryOrientation.DUAL_DOMINANT
    linguistic_evidence: list[str] = Field(
        default_factory=list,
        description="Top marker phrases detected as evidence"
    )


# ─── Sub-Profile 2: Moral Emotion ───────────────────────────────────

class MoralEmotionProfile(BaseModel):
    """
    Moral Foundation weighted vector — reverse-engineered from moral
    emotion linguistic signatures using the convergence matrix.

    Pipeline: Text → Moral Emotion Detection (indignation, compassion,
    contempt, disgust) → Appraisal Profile (Scherer CPM) → Foundation
    Inversion → Weighted MFT Vector.

    Research: Haidt MFT (2012), Tangney moral emotions (2007),
    Scherer CPM (2001), LIWC psychological distancing (Pennebaker)
    """
    foundation_weights: dict[str, float] = Field(
        default_factory=lambda: {
            "care_harm": 0.0,
            "fairness_cheating": 0.0,
            "loyalty_betrayal": 0.0,
            "authority_subversion": 0.0,
            "sanctity_degradation": 0.0,
            "liberty_oppression": 0.0,
        },
        description="Weighted moral foundation vector, each 0-1, sum ≈ 1.0"
    )
    dominant_emotion: Optional[str] = Field(
        None,
        description="Primary moral emotion detected (indignation, compassion, contempt, disgust, elevation)"
    )
    appraisal_profile: dict[str, float] = Field(
        default_factory=lambda: {
            "relevance": 0.0,
            "goal_conduciveness": 0.0,
            "coping_potential": 0.0,
            "normative_significance": 0.0,
        },
        description="Scherer CPM Stimulus Evaluation Check scores, each 0-1"
    )


# ─── Sub-Profile 3: Coping Trajectory ───────────────────────────────

class CopingTrajectoryPosition(BaseModel):
    """
    Lazarus & Folkman Transactional Model — coping phase detection.

    The SEARCH_PHASE is the highest-value detection: it represents
    peak receptivity to coaching intervention. Detected through
    temporal language shifts, agency attribution changes, and
    help-seeking behavior markers.

    Research: Coping Trajectory Staging Framework
    """
    phase: CopingPhase = CopingPhase.PRE_CONTEMPLATION
    temporal_language_shift: float = Field(
        0.0, ge=-1.0, le=1.0,
        description="Past→future tense ratio delta (-1=stuck in past, +1=fully future-oriented)"
    )
    agency_attribution_delta: float = Field(
        0.0, ge=-1.0, le=1.0,
        description="Change in agentic language (-1=fully external, +1=fully internal attribution)"
    )
    search_phase_confidence: float = Field(
        0.0, ge=0.0, le=1.0,
        description="Confidence that individual is in the search phase"
    )


# ─── Sub-Profile 4: Hermeneutical Gap ───────────────────────────────

class HermeneuticalGapProfile(BaseModel):
    """
    Testimonial smothering detection — tri-modal heuristic.

    Detects unarticulated experience through three independent signals:
    1. Discourse truncation (syntactic evidence of self-censorship)
    2. Affective parabola (emotional escalation + abrupt flattening)
    3. Metaphor novelty (non-conventional figurative language)

    High composite score = individual is experiencing something they
    cannot yet name — this is the highest-value signal for content
    that provides new interpretive frameworks.

    Research: Detecting Hermeneutical Injustice Computationally
    """
    discourse_truncation_score: float = Field(
        0.0, ge=0.0, le=1.0,
        description="Evidence of syntactic truncation and phatic tokens"
    )
    affective_parabola_score: float = Field(
        0.0, ge=0.0, le=1.0,
        description="Emotional escalation followed by abrupt flattening"
    )
    metaphor_novelty_score: float = Field(
        0.0, ge=0.0, le=1.0,
        description="Presence of non-conventional figurative language"
    )
    composite_gap_score: float = Field(
        0.0, ge=0.0, le=1.0,
        description="Weighted composite: 0.4*truncation + 0.3*parabola + 0.3*novelty"
    )


# ─── Sub-Profile 5: Reconsolidation Markers ─────────────────────────

class ReconsolidationMarkers(BaseModel):
    """
    Memory reconsolidation potential markers — from neurobiology of
    content "hits".

    Prediction error is the gateway to memory reconsolidation: content
    that violates audience expectations creates a labilization window
    where existing schemas can be updated. High prediction-error
    sensitivity + high save/share ratio = audience primed for deep impact.

    Research: Audience Reconsolidation and Content Impact,
    Nader et al. (2000) reconsolidation theory
    """
    prediction_error_sensitivity: float = Field(
        0.0, ge=0.0, le=1.0,
        description="Responsiveness to expectation violations (surprise markers)"
    )
    save_share_ratio: float = Field(
        0.0, ge=0.0, le=10.0,
        description="Save-intent / share-intent ratio (>1 = deep impact, <1 = surface virality)"
    )
    neural_coupling_proxy: float = Field(
        0.0, ge=0.0, le=1.0,
        description="Proxy for speaker-listener neural coupling (narrative mirroring markers)"
    )
    parasocial_engagement: float = Field(
        0.0, ge=0.0, le=1.0,
        description="Markers of one-directional relational investment with creator"
    )


# ─── Sub-Profile 6: Authenticity Score ───────────────────────────────

class AuthenticityScore(BaseModel):
    """
    L-depth classification + LIWC-22 authenticity proxy.

    Approximates Pennebaker's LIWC-22 Authenticity variable using
    open-source heuristics: self-reference density, negative emotion
    frequency, cognitive complexity inverse, narrative style detection.

    Combined with contextual signals (timestamp, platform, anonymity)
    to classify text into L1 (performative) / L2 (communal) / L3 (authentic).

    Research: Verified L3 Data Through Digital Ethnography,
    Mind After Midnight hypothesis (circadian neurobiology)
    """
    l_depth: LDepth = LDepth.L1_PERFORMATIVE
    liwc_authenticity_proxy: float = Field(
        0.0, ge=0.0, le=1.0,
        description="Approximated LIWC-22 authenticity (higher = less self-monitoring)"
    )
    self_reference_density: float = Field(
        0.0, ge=0.0, le=1.0,
        description="I/me/my pronoun density (normalized by word count)"
    )
    temporal_context: Optional[str] = Field(
        None,
        description="Timestamp context: 'late_night', 'peak_hours', 'unknown'"
    )


# ─── Composite: Audience Trigger Profile ─────────────────────────────

class AudienceTriggerProfile(BaseModel):
    """
    The complete audience-side counterpart to the coach's trigger_map.json.

    This is the central data structure of the Context Premise Engine.
    Each analyzed text unit produces one AudienceTriggerProfile.
    Multiple profiles are aggregated into a CohortContextPremise
    by the audience_aggregator.py module.

    Architecture: Context Premise Engine → Audience Aggregator →
    Intersection Engine → Blueprint Orchestrator
    """
    # ── Sub-profiles ──
    regulatory_focus: RegulatoryFocusProfile = Field(
        default_factory=RegulatoryFocusProfile
    )
    moral_emotion: MoralEmotionProfile = Field(
        default_factory=MoralEmotionProfile
    )
    coping_trajectory: CopingTrajectoryPosition = Field(
        default_factory=CopingTrajectoryPosition
    )
    hermeneutical_gap: HermeneuticalGapProfile = Field(
        default_factory=HermeneuticalGapProfile
    )
    reconsolidation: ReconsolidationMarkers = Field(
        default_factory=ReconsolidationMarkers
    )
    authenticity: AuthenticityScore = Field(
        default_factory=AuthenticityScore
    )

    # ── Meta ──
    text_id: Optional[str] = Field(
        None, description="Unique identifier for the source text unit"
    )
    source_text_snippet: Optional[str] = Field(
        None, description="First 200 chars of source text for provenance"
    )
    confidence: ConfidenceLevel = ConfidenceLevel.LOW
    data_phase: DataPhase = DataPhase.COLD
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def to_neo4j_dict(self) -> dict:
        """Flattens the profile into a dict suitable for Neo4j properties."""
        return {
            "text_id": self.text_id,
            "confidence": self.confidence.value,
            "data_phase": self.data_phase.value,
            "created_at": self.created_at.isoformat(),
            # Regulatory Focus
            "rf_eagerness": self.regulatory_focus.eagerness_score,
            "rf_vigilance": self.regulatory_focus.vigilance_score,
            "rf_orientation": self.regulatory_focus.dominant_orientation.value,
            # Moral Emotion (flatten the 6-foundation vector)
            "mft_care_harm": self.moral_emotion.foundation_weights.get("care_harm", 0.0),
            "mft_fairness_cheating": self.moral_emotion.foundation_weights.get("fairness_cheating", 0.0),
            "mft_loyalty_betrayal": self.moral_emotion.foundation_weights.get("loyalty_betrayal", 0.0),
            "mft_authority_subversion": self.moral_emotion.foundation_weights.get("authority_subversion", 0.0),
            "mft_sanctity_degradation": self.moral_emotion.foundation_weights.get("sanctity_degradation", 0.0),
            "mft_liberty_oppression": self.moral_emotion.foundation_weights.get("liberty_oppression", 0.0),
            "mft_dominant_emotion": self.moral_emotion.dominant_emotion,
            # Coping Trajectory
            "coping_phase": self.coping_trajectory.phase.value,
            "coping_search_confidence": self.coping_trajectory.search_phase_confidence,
            # Hermeneutical Gap
            "herm_composite": self.hermeneutical_gap.composite_gap_score,
            "herm_truncation": self.hermeneutical_gap.discourse_truncation_score,
            "herm_parabola": self.hermeneutical_gap.affective_parabola_score,
            "herm_novelty": self.hermeneutical_gap.metaphor_novelty_score,
            # Reconsolidation
            "recon_prediction_error": self.reconsolidation.prediction_error_sensitivity,
            "recon_save_share": self.reconsolidation.save_share_ratio,
            "recon_coupling": self.reconsolidation.neural_coupling_proxy,
            "recon_parasocial": self.reconsolidation.parasocial_engagement,
            # Authenticity
            "auth_l_depth": self.authenticity.l_depth.value,
            "auth_proxy": self.authenticity.liwc_authenticity_proxy,
            "auth_self_ref": self.authenticity.self_reference_density,
        }


# ─── Cohort-Level Aggregate ──────────────────────────────────────────

class CohortContextPremise(BaseModel):
    """
    Aggregated audience profile for a segment/cohort.

    Produced by audience_aggregator.py through L-depth weighted averaging.
    This is the audience-side input to the Intersection Engine.
    """
    segment_id: Optional[str] = None
    segment_label: Optional[str] = None
    sample_size: int = 0

    # Aggregate profiles (weighted averages)
    regulatory_focus: RegulatoryFocusProfile = Field(
        default_factory=RegulatoryFocusProfile
    )
    moral_emotion: MoralEmotionProfile = Field(
        default_factory=MoralEmotionProfile
    )
    coping_trajectory: CopingTrajectoryPosition = Field(
        default_factory=CopingTrajectoryPosition
    )
    hermeneutical_gap: HermeneuticalGapProfile = Field(
        default_factory=HermeneuticalGapProfile
    )
    reconsolidation: ReconsolidationMarkers = Field(
        default_factory=ReconsolidationMarkers
    )

    # Aggregate meta
    data_phase: DataPhase = DataPhase.COLD
    mean_authenticity: float = Field(
        0.0, ge=0.0, le=1.0,
        description="Mean LIWC authenticity proxy across all texts in cohort"
    )
    l_depth_distribution: dict[str, float] = Field(
        default_factory=lambda: {
            "L1_PERFORMATIVE": 0.0,
            "L2_COMMUNAL": 0.0,
            "L3_AUTHENTIC": 0.0,
        },
        description="Proportion of texts at each L-depth level"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ─── Coach-Side Match Vector ────────────────────────────────────────

class CoachMatchVector(BaseModel):
    """
    Coach profile adapted for comparison with CohortContextPremise.

    Produced by coach_profile_adapter.py from trigger_map.json +
    emotional_dna.json. Contains only the dimensions that have
    audience-side equivalents for cosine similarity computation.
    """
    coach_id: Optional[str] = None

    # MFT vector (aggregated from coach's triggers)
    mft_weights: dict[str, float] = Field(
        default_factory=lambda: {
            "care_harm": 0.0,
            "fairness_cheating": 0.0,
            "loyalty_betrayal": 0.0,
            "authority_subversion": 0.0,
            "sanctity_degradation": 0.0,
            "liberty_oppression": 0.0,
        }
    )

    # Regulatory orientation (from emotional DNA patterns)
    regulatory_orientation: RegulatoryOrientation = RegulatoryOrientation.DUAL_DOMINANT

    # Content-eligible trigger IDs (only resolved_dual_layer triggers)
    eligible_trigger_ids: list[str] = Field(default_factory=list)

    # Reconsolidation threshold (from trigger_map)
    mean_prediction_error_threshold: float = Field(
        5.0, ge=1.0, le=10.0,
        description="Mean prediction error threshold across eligible triggers"
    )


# ─── Intersection Result ────────────────────────────────────────────

class IntersectionTheme(BaseModel):
    """A single theme from the intersection computation."""
    theme_label: str
    intersection_score: float = Field(0.0, ge=0.0, le=1.0)
    mft_alignment: float = Field(0.0, ge=0.0, le=1.0)
    regulatory_fit: float = Field(0.0, ge=0.0, le=1.0)
    reconsolidation_potential: float = Field(0.0, ge=0.0, le=1.0)
    recommended_depth: str = "SURFACE"
    coach_trigger_id: Optional[str] = None


class IntersectionResult(BaseModel):
    """
    Output of the Intersection Engine.

    Contains ranked themes ordered by intersection_score,
    plus aggregate match quality metrics.
    """
    themes: list[IntersectionTheme] = Field(default_factory=list)
    overall_mft_cosine: float = Field(0.0, ge=0.0, le=1.0)
    overall_regulatory_fit: float = Field(0.0, ge=0.0, le=1.0)
    audience_coping_phase: CopingPhase = CopingPhase.PRE_CONTEMPLATION
    audience_data_phase: DataPhase = DataPhase.COLD


# ─── Blueprint Output ───────────────────────────────────────────────

class BlueprintTrack(str, Enum):
    """Proposal 6 dual-track designation."""
    CORE = "CORE"
    SATELLITE = "SATELLITE"


class BlueprintItem(BaseModel):
    """A single content item in the generated blueprint."""
    item_id: str
    track: BlueprintTrack
    theme_label: str
    coach_trigger_id: Optional[str] = None
    audience_foundation: Optional[str] = None
    emotional_frame: Optional[str] = None
    content_depth: str = "SURFACE"
    narrative_arc_type: Optional[str] = None
    intersection_score: float = Field(0.0, ge=0.0, le=1.0)
    data_confidence: ConfidenceLevel = ConfidenceLevel.LOW


class ContentBlueprint(BaseModel):
    """
    The final output of the Blueprint Orchestrator.

    Contains an ordered list of BlueprintItems split between
    Core (intersection-first) and Satellite (audience-first) tracks.
    """
    blueprint_id: Optional[str] = None
    coach_id: Optional[str] = None
    segment_id: Optional[str] = None
    items: list[BlueprintItem] = Field(default_factory=list)
    core_ratio: float = Field(0.6, ge=0.0, le=1.0)
    satellite_ratio: float = Field(0.4, ge=0.0, le=1.0)
    data_phase: DataPhase = DataPhase.COLD
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def core_items(self) -> list[BlueprintItem]:
        return [i for i in self.items if i.track == BlueprintTrack.CORE]

    @property
    def satellite_items(self) -> list[BlueprintItem]:
        return [i for i in self.items if i.track == BlueprintTrack.SATELLITE]
