"""
Upstream Contract for Reaction Engine Models
This file provides structures for imports by solo/debate/duel reactions,
enriched with SFL-visible score schemas.
"""

from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import List, Optional, Any
from pydantic import BaseModel, Field, ConfigDict

# =========================================================================
# Existing Legacy Models (Preserved to maintain brownfield contracts)
# =========================================================================

class ReactionTopicBrief(BaseModel):
    model_config = ConfigDict(extra="forbid")
    topic_id: str = Field(default="TGT-DUMMY")
    title: str = Field(default="Dummy Title")
    expires_at: datetime = Field(default_factory=datetime.utcnow)

class ReactionSessionRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")
    session_id: str = Field(default="SES-DUMMY")

class ReactionArtifactRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(default="ART-DUMMY")
    session_id: str = Field(default="SES-DUMMY")

class SemanticBeat(BaseModel):
    model_config = ConfigDict(extra="forbid")
    score: float = Field(default=0.9)
    description: str = Field(default="Beat Description")

class EvidenceItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    timestamp: float = Field(default=0.0)
    description: str = Field(default="Evidence Description")

class ReactionScoreCard(BaseModel):
    model_config = ConfigDict(extra="allow")  # allow for downstream compatibility or dynamic metrics
    conviction_score: float = Field(default=0.9)
    semantic_beats: List[SemanticBeat] = Field(default_factory=list)
    evidence: List[EvidenceItem] = Field(default_factory=list)
    conviction_trajectory: List[float] = Field(default_factory=list)
    pacing_trajectory: List[float] = Field(default_factory=list)
    overall_score: float = Field(default=85.0)
    
    # Preserved primary metrics
    impact_score: float = Field(default=75.0, ge=0.0, le=100.0)
    anti_centroid_charge: float = Field(default=0.65, ge=0.0, le=1.0)
    damage_index: float = Field(default=12.0, ge=0.0, le=100.0)
    compounding_forecast: float = Field(default=8.5, ge=-10.0, le=10.0)


# =========================================================================
# New SFL Perceptual, Visible, and Routing Models
# =========================================================================

class ReactionVisibleScoreName(str, Enum):
    HUMANITY = "humanity"
    PRESENCE = "presence"
    TRUST = "trust"
    MEMORABILITY = "memorability"
    RESONANCE = "resonance"
    SIGNAL = "signal"
    AI_SLOP_RISK = "ai_slop_risk"

class ReactionPerceptualVerdict(str, Enum):
    STRONG = "strong"
    UNSTABLE = "unstable"
    WEAK = "weak"
    BLOCKING = "blocking"

class ReactionSlopClass(str, Enum):
    NONE = "none"
    CENTROID_SAFETY = "centroid_safety"
    SYNTHETIC_FORCE = "synthetic_force"
    DEAD_POLISH = "dead_polish"
    HOLLOW_HEAT = "hollow_heat"

class ReactionRouteAction(str, Enum):
    PASS_TO_EXPORT_GATE = "pass_to_export_gate"
    REVIEW_BEFORE_EXPORT = "review_before_export"
    ROUTE_TO_REDEMPTION = "route_to_redemption"
    COACHING_INTERVENTION = "coaching_intervention"
    JURY_ONLY_NO_PROMOTION = "jury_only_no_promotion"

class ReactionVisibleMetricEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid")
    metric_id: str = Field(..., min_length=1)
    summary: str = Field(..., min_length=1)
    source_signal: str = Field(..., min_length=1)
    source_value: float = Field(...)
    contribution: float = Field(..., ge=-1.0, le=1.0)

class ReactionPerceptualScore(BaseModel):
    model_config = ConfigDict(extra="forbid")
    score_name: ReactionVisibleScoreName = Field(...)
    score_0_99: int = Field(..., ge=0, le=99)
    verdict: ReactionPerceptualVerdict = Field(...)
    rationale: str = Field(..., min_length=1)
    evidence: List[ReactionVisibleMetricEvidence] = Field(default_factory=list)

class ReactionPresenceSignal(BaseModel):
    model_config = ConfigDict(extra="forbid")
    presence_score_0_99: int = Field(..., ge=0, le=99)
    conviction_density: float = Field(..., ge=0.0, le=100.0)
    pacing_score: float = Field(..., ge=0.0, le=100.0)
    pause_weight_score: float = Field(..., ge=0.0, le=1.0)
    stance_force_score: float = Field(..., ge=0.0, le=1.0)
    hedge_pressure_score: float = Field(..., ge=0.0, le=1.0)
    interpretation: str = Field(..., min_length=1)

class ReactionSlopRiskState(BaseModel):
    model_config = ConfigDict(extra="forbid")
    overall_risk_score_0_99: int = Field(..., ge=0, le=99)
    slop_class: ReactionSlopClass = Field(...)
    centroid_collapse_detected: bool = Field(default=False)
    synthetic_smoothness_detected: bool = Field(default=False)
    false_force_detected: bool = Field(default=False)
    dead_polish_detected: bool = Field(default=False)
    required_correction: str = Field(..., min_length=1)

class ReactionVisibleScoreSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")
    humanity: ReactionPerceptualScore = Field(...)
    presence: ReactionPerceptualScore = Field(...)
    trust: ReactionPerceptualScore = Field(...)
    memorability: ReactionPerceptualScore = Field(...)
    resonance: ReactionPerceptualScore = Field(...)
    signal: ReactionPerceptualScore = Field(...)
    ai_slop_risk: ReactionPerceptualScore = Field(...)
    top_strengths: List[str] = Field(default_factory=list)
    top_weaknesses: List[str] = Field(default_factory=list)

class ReactionBenchmarkCarryover(BaseModel):
    model_config = ConfigDict(extra="forbid")
    artifact_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    reaction_mode: str = Field(..., min_length=1)
    visible_scores: ReactionVisibleScoreSummary = Field(...)
    presence_signal: ReactionPresenceSignal = Field(...)
    slop_risk_state: ReactionSlopRiskState = Field(...)
    challenge_readiness: bool = Field(...)
    speaker_course_recommended: bool = Field(...)
    accountability_followup_recommended: bool = Field(...)
    benchmark_headline: str = Field(..., min_length=1)

class ReactionPerceptualRoutingDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")
    artifact_id: str = Field(..., min_length=1)
    route_action: ReactionRouteAction = Field(...)
    export_gate_eligible: bool = Field(...)
    jury_visibility_allowed: bool = Field(...)
    social_promotion_allowed: bool = Field(...)
    trigger_redemption: bool = Field(...)
    explanation: str = Field(..., min_length=1)


# Legacy SQL Stub definitions
REACTION_TOPICS_SQL = "SELECT 1"
REACTION_SESSIONS_SQL = "SELECT 1"
REACTION_ARTIFACTS_SQL = "SELECT 1"
REACTION_VOTES_SQL = "SELECT 1"
REACTION_SUPERVISORS_SQL = "SELECT 1"
REACTION_REDEMPTIONS_SQL = "SELECT 1"
REACTION_UPLOAD_SESSIONS_SQL = "SELECT 1"
