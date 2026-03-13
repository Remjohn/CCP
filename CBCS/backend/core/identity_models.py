"""
Identity Engine Data Models — Pydantic Schemas

These models define the type-safe contracts for the 12-dimensional
identity vector that flows through the entire Identity Engine:
    Aria (Layer 2) → Chronos (Layer 3) → Sentinel (Layer 4) → Ritual Selection (Layer 5)

Architecture reference: identity_engine_architecture.md, Section 3, Layers 2-4.
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime


# ─── Enums ───────────────────────────────────────────────────────────

class ConfidenceLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class CulturalFrame(str, Enum):
    """
    Cultural expression style classification (Architecture Layer 2E).
    Derived from Markus & Kitayama (1991) independent vs. interdependent
    self-construal framework + diasporic hybrid pattern.
    """
    DIRECT_INDIVIDUALIST = "DIRECT_INDIVIDUALIST"
    RELATIONAL_COLLECTIVIST = "RELATIONAL_COLLECTIVIST"
    HYBRID_DIASPORIC = "HYBRID_DIASPORIC"


class DominantGapType(str, Enum):
    """Higgins' self-discrepancy categories."""
    IDEAL = "IDEAL"       # Actual-Ideal gap dominant → dejection
    OUGHT = "OUGHT"       # Actual-Ought gap dominant → agitation
    FEARED = "FEARED"     # Feared-Self proximity dominant → anxiety


class EmotionalSignature(str, Enum):
    """Predicted emotional response from self-discrepancy type."""
    DEJECTION = "DEJECTION"     # High Actual-Ideal gap
    AGITATION = "AGITATION"     # High Actual-Ought gap
    ANXIETY = "ANXIETY"         # High Feared-Self proximity


class DominantNeed(str, Enum):
    """SDT basic psychological needs (Deci & Ryan, 2000)."""
    AUTONOMY = "AUTONOMY"
    COMPETENCE = "COMPETENCE"
    RELATEDNESS = "RELATEDNESS"


class NeedTrajectory(str, Enum):
    """Direction of need satisfaction change over time."""
    RISING = "RISING"
    FALLING = "FALLING"
    STABLE = "STABLE"
    UNKNOWN = "UNKNOWN"     # < 3 entries — insufficient data


class DefensePattern(str, Enum):
    """
    Identity defense mechanisms detected from journal language.
    Mapped to Breakwell's IPT threat types in Architecture Layer 4B.
    """
    DEFLECTION = "DEFLECTION"
    INTELLECTUALIZATION = "INTELLECTUALIZATION"
    EXTERNALIZATION = "EXTERNALIZATION"
    WITHDRAWAL = "WITHDRAWAL"
    MINIMIZATION = "MINIMIZATION"
    PROJECTION = "PROJECTION"
    NONE = "NONE"


class CognitiveDistortionType(str, Enum):
    """
    Burns' consolidated 10-type taxonomy.
    Derived from Paper 7 (Cognitive Distortion NLP Survey),
    Table 1 — the 10 types appearing in ≥48% of NLP studies.
    """
    ALL_OR_NOTHING = "ALL_OR_NOTHING"
    OVERGENERALIZATION = "OVERGENERALIZATION"
    MENTAL_FILTER = "MENTAL_FILTER"
    DISQUALIFYING_POSITIVE = "DISQUALIFYING_POSITIVE"
    JUMPING_TO_CONCLUSIONS = "JUMPING_TO_CONCLUSIONS"
    MAGNIFICATION = "MAGNIFICATION"
    EMOTIONAL_REASONING = "EMOTIONAL_REASONING"
    SHOULD_STATEMENTS = "SHOULD_STATEMENTS"
    LABELLING = "LABELLING"
    PERSONALIZATION = "PERSONALIZATION"


class ThreatType(str, Enum):
    """Breakwell's Identity Process Theory threat taxonomy."""
    CONTINUITY = "CONTINUITY"           # "I'm not the same person"
    DISTINCTIVENESS = "DISTINCTIVENESS" # "I'm becoming like everyone else"
    SELF_ESTEEM = "SELF_ESTEEM"         # "I'm not good enough"
    SELF_EFFICACY = "SELF_EFFICACY"     # "I can't do what this requires"
    NONE = "NONE"


class ThreatSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class TrajectoryType(str, Enum):
    """
    Overall user trajectory classification (Architecture Layer 3C).
    Requires ≥14 identity vector entries for reliable classification.
    """
    REDEMPTION_ARC = "REDEMPTION_ARC"
    CONTAMINATION_ARC = "CONTAMINATION_ARC"
    PLATEAU = "PLATEAU"
    OSCILLATION = "OSCILLATION"
    BREAKTHROUGH = "BREAKTHROUGH"
    UNKNOWN = "UNKNOWN"     # < 14 entries


class EscalationPhase(str, Enum):
    """3-phase escalation trajectory from Paper 4."""
    PHASE_1_SURFACE = "PHASE_1_SURFACE"       # Weeks 1-2, flexible defenses
    PHASE_2_DEEP = "PHASE_2_DEEP"             # Weeks 3-4, withdrawal
    PHASE_3_DECISION = "PHASE_3_DECISION"     # Weeks 5-6, breakthrough or dropout
    UNKNOWN = "UNKNOWN"


# ─── Layer 2A: Narrative Identity ────────────────────────────────────

class NarrativeIdentityScore(BaseModel):
    """
    McAdams' Life Story Model dimensions, computationally extracted.
    Architecture Layer 2A.
    """
    agency: float = Field(0.0, ge=0.0, le=1.0, description="Self-as-agent strength (0=passive, 1=fully agentic)")
    communion: float = Field(0.0, ge=0.0, le=1.0, description="Relational connection strength")
    redemption_arc: float = Field(0.0, ge=-1.0, le=1.0, description="-1=contamination, +1=redemption")
    meaning_making: float = Field(0.0, ge=0.0, le=1.0, description="Exploratory processing / insight language")
    cultural_frame: CulturalFrame = CulturalFrame.DIRECT_INDIVIDUALIST
    confidence: ConfidenceLevel = ConfidenceLevel.LOW
    evidence_quotes: list[str] = Field(default_factory=list)


# ─── Layer 2B: Self-Discrepancy ──────────────────────────────────────

class SelfDiscrepancyProfile(BaseModel):
    """
    Higgins' Self-Discrepancy Theory + Markus & Nurius' Possible Selves.
    Computed from Aria's existing Dream, Fear, Identity extractions.
    Architecture Layer 2B.
    """
    actual_ideal_gap: float = Field(0.0, ge=0.0, le=1.0, description="Semantic distance: identity ↔ dreams")
    actual_ought_gap: float = Field(0.0, ge=0.0, le=1.0, description="Semantic distance: identity ↔ obligations")
    feared_self_proximity: float = Field(0.0, ge=0.0, le=1.0, description="Semantic similarity: identity ↔ fears (higher = closer)")
    hope_fear_balance: float = Field(0.0, ge=-1.0, le=1.0, description="0=balanced (max motivation), -1=all feared, +1=all hoped")
    dominant_gap_type: DominantGapType = DominantGapType.IDEAL
    predicted_emotional_signature: EmotionalSignature = EmotionalSignature.DEJECTION
    confidence: ConfidenceLevel = ConfidenceLevel.LOW


# ─── Layer 2C: SDT Need Profile ──────────────────────────────────────

class SDTNeedProfile(BaseModel):
    """
    Self-Determination Theory basic need satisfaction profile.
    Replaces the broken 4-archetype identity pillar system.
    Architecture Layer 2C.
    """
    autonomy: int = Field(50, ge=0, le=100, description="Autonomy satisfaction (0=frustrated, 100=satisfied)")
    competence: int = Field(50, ge=0, le=100, description="Competence satisfaction")
    relatedness: int = Field(50, ge=0, le=100, description="Relatedness satisfaction")
    autonomy_markers: list[str] = Field(default_factory=list, description="Evidence quotes for autonomy scoring")
    competence_markers: list[str] = Field(default_factory=list, description="Evidence quotes for competence scoring")
    relatedness_markers: list[str] = Field(default_factory=list, description="Evidence quotes for relatedness scoring")
    dominant_need: DominantNeed = DominantNeed.AUTONOMY
    need_trajectory: NeedTrajectory = NeedTrajectory.UNKNOWN
    confidence: ConfidenceLevel = ConfidenceLevel.LOW


# ─── Layer 2D: Cognitive Distortion Report ───────────────────────────

class DetectedDistortion(BaseModel):
    """A single detected cognitive distortion instance."""
    type: CognitiveDistortionType
    evidence_quote: str
    confidence: float = Field(0.0, ge=0.0, le=1.0)
    identity_signal: str = Field("", description="Which identity dimension this distortion affects")
    reasoning: str = Field("", description="DoT reasoning chain for this classification")


class CognitiveDistortionReport(BaseModel):
    """
    Multi-label cognitive distortion detection per journal entry.
    Architecture Layer 2D.
    Uses DoT (Diagnosis of Thought) framework for classification.
    """
    distortions: list[DetectedDistortion] = Field(default_factory=list)
    dominant_distortion: Optional[CognitiveDistortionType] = None
    distortion_density: float = Field(0.0, ge=0.0, description="Distortions per 100 words")


# ─── Layer 4: Threat Assessment ──────────────────────────────────────

class ThreatAssessment(BaseModel):
    """
    Identity threat detection output from Sentinel agent.
    Architecture Layer 4A.
    """
    threat_type: ThreatType = ThreatType.NONE
    severity: ThreatSeverity = ThreatSeverity.LOW
    active_defense: DefensePattern = DefensePattern.NONE
    recommended_intervention: str = Field("", description="Matched intervention from defense-intervention matrix")
    convergent_signals: int = Field(0, ge=0, description="Number of independent signals that agree on this threat")
    confidence: ConfidenceLevel = ConfidenceLevel.LOW
    evidence_quotes: list[str] = Field(default_factory=list)


class InterventionRecommendation(BaseModel):
    """Defense → Intervention matching output."""
    intervention_type: str
    rationale: str
    priority: ThreatSeverity = ThreatSeverity.LOW


# ─── Master Composite: Identity Vector ───────────────────────────────

class IdentityVector(BaseModel):
    """
    The 12-dimensional identity vector — the master data object that
    flows through the entire Identity Engine.

    Produced by: Aria (Layer 2 sub-agents)
    Consumed by: Chronos (Layer 3), Sentinel (Layer 4), Ritual Selection (Layer 5)
    Stored in: Neo4j as IdentitySnapshot node via graph_db.create_identity_vector()
    
    This replaces the hardcoded `identity_pillar: str = "The Builder"`.
    """
    # Layer 2A: Narrative Identity
    narrative: NarrativeIdentityScore = Field(default_factory=NarrativeIdentityScore)

    # Layer 2B: Self-Discrepancy
    discrepancy: SelfDiscrepancyProfile = Field(default_factory=SelfDiscrepancyProfile)

    # Layer 2C: SDT Need Profile
    sdt: SDTNeedProfile = Field(default_factory=SDTNeedProfile)

    # Layer 2D: Cognitive Distortion Report
    distortions: CognitiveDistortionReport = Field(default_factory=CognitiveDistortionReport)

    # Layer 4: Threat State (populated by Sentinel, defaults until enough data)
    threat: ThreatAssessment = Field(default_factory=ThreatAssessment)

    # Metadata
    timestamp: Optional[datetime] = None
    entry_id: str = ""
    word_count: int = Field(0, ge=0)
    confidence: float = Field(0.0, ge=0.0, le=1.0, description="Overall vector confidence (weighted avg of sub-models)")

    def to_neo4j_dict(self) -> dict:
        """
        Flattens the composite model into a flat dict for Neo4j storage.
        Used by graph_db.create_identity_vector().
        """
        return {
            # Narrative Identity
            "agency": self.narrative.agency,
            "communion": self.narrative.communion,
            "redemption_arc": self.narrative.redemption_arc,
            "meaning_making": self.narrative.meaning_making,
            # Self-Discrepancy
            "actual_ideal_gap": self.discrepancy.actual_ideal_gap,
            "actual_ought_gap": self.discrepancy.actual_ought_gap,
            "feared_self_proximity": self.discrepancy.feared_self_proximity,
            "hope_fear_balance": self.discrepancy.hope_fear_balance,
            # SDT Need Profile
            "autonomy": self.sdt.autonomy,
            "competence": self.sdt.competence,
            "relatedness": self.sdt.relatedness,
            # Threat state
            "threat_level": 0.0 if self.threat.severity == ThreatSeverity.LOW else
                           0.33 if self.threat.severity == ThreatSeverity.MEDIUM else
                           0.66 if self.threat.severity == ThreatSeverity.HIGH else 1.0,
            "active_defense": self.threat.active_defense.value,
            # Metadata
            "cultural_frame": self.narrative.cultural_frame.value,
            "word_count": self.word_count,
            "confidence": self.confidence,
        }


# ─── Chronos Output Models ──────────────────────────────────────────

class TrendDirection(str, Enum):
    RISING = "RISING"
    FALLING = "FALLING"
    STABLE = "STABLE"
    UNKNOWN = "UNKNOWN"


class DimensionTrend(BaseModel):
    """Rolling trend for a single identity vector dimension."""
    dimension: str
    direction: TrendDirection = TrendDirection.UNKNOWN
    slope: float = 0.0
    confidence: ConfidenceLevel = ConfidenceLevel.LOW


class ChangePoint(BaseModel):
    """A detected structural break in an identity dimension time series."""
    dimension: str
    entry_index: int = Field(..., description="Index of the entry where the break occurred")
    entry_id: str = ""
    pre_mean: float = 0.0
    post_mean: float = 0.0
    magnitude: float = Field(0.0, description="Absolute difference between pre and post means")


class TemporalAnalysis(BaseModel):
    """
    Complete output from Chronos (Layer 3).
    Contains trends, change points, and trajectory classification.
    """
    trends: list[DimensionTrend] = Field(default_factory=list)
    change_points: list[ChangePoint] = Field(default_factory=list)
    trajectory: TrajectoryType = TrajectoryType.UNKNOWN
    entry_count: int = 0
    sufficient_data_for_trends: bool = False      # ≥7 entries
    sufficient_data_for_trajectory: bool = False   # ≥14 entries
