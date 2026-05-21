from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, Field

class ViewerScoreBand(str, Enum):
    low = "low"
    developing = "developing"
    strong = "strong"

class TrendDirection(str, Enum):
    up = "up"
    down = "down"
    flat = "flat"
    unavailable = "unavailable"

class SignalMetricKey(str, Enum):
    conviction_density = "conviction_density"
    hedge_frequency = "hedge_frequency"
    pause_architecture = "pause_architecture"
    pitch_stability = "pitch_stability"

class RecommendationPriority(str, Enum):
    primary = "primary"
    secondary = "secondary"

class ProjectionAvailability(str, Enum):
    available = "available"
    partial = "partial"
    unavailable = "unavailable"

class TraitRadarPoint(BaseModel):
    trait_name: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    score: int = Field(..., ge=1, le=10)
    max_score: int = Field(default=10, ge=1)
    category: str = Field(..., min_length=1)
    score_band: ViewerScoreBand = Field(...)

class EvidenceCitationCard(BaseModel):
    signal_source: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    rubric_points: int = Field(..., ge=0)

class ScoreMeaningBlock(BaseModel):
    headline: str = Field(..., min_length=1)
    interpretation: str = Field(..., min_length=1)
    why_it_matters: str = Field(..., min_length=1)
    next_step: str = Field(..., min_length=1)
    priority: RecommendationPriority = Field(default=RecommendationPriority.primary)

class TraitInsightCard(BaseModel):
    trait_name: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    score: int = Field(..., ge=1, le=10)
    category: str = Field(..., min_length=1)
    evidence: list[EvidenceCitationCard] = Field(default_factory=list)
    meaning: ScoreMeaningBlock = Field(...)
    is_weak_focus: bool = Field(default=False)
    is_strength_anchor: bool = Field(default=False)

class Fr61SignalDeltaCard(BaseModel):
    metric_key: SignalMetricKey = Field(...)
    label: str = Field(..., min_length=1)
    current_value: float | None = Field(default=None)
    baseline_value: float | None = Field(default=None)
    delta_value: float | None = Field(default=None)
    direction: TrendDirection = Field(...)
    availability: ProjectionAvailability = Field(...)
    explanation: str = Field(..., min_length=1)
    next_step: str = Field(..., min_length=1)

class ProductionLockExplanation(BaseModel):
    all_categories_met: bool = Field(default=False)
    locked_categories: list[str] = Field(default_factory=list)
    unlock_message: str = Field(default="")
    participant_copy: str = Field(..., min_length=1)

class ScoreViewerTheme(BaseModel):
    mood_key: str = Field(..., min_length=1)
    background_primary: str = Field(..., min_length=1)
    background_secondary: str = Field(..., min_length=1)
    text_primary: str = Field(..., min_length=1)
    accent: str = Field(..., min_length=1)
    brand_hue_used: bool = Field(default=False)

class ScoreDataAvailability(BaseModel):
    scorecard_file: ProjectionAvailability = Field(...)
    signal_cards: ProjectionAvailability = Field(...)
    evidence_citations: ProjectionAvailability = Field(...)
    production_lock: ProjectionAvailability = Field(...)

class ScoreCardViewerPayload(BaseModel):
    coach_id: str = Field(..., min_length=1)
    version: str = Field(..., min_length=1)
    scored_at: str = Field(..., min_length=1)
    last_updated: str = Field(..., min_length=1)
    availability: ScoreDataAvailability = Field(...)
    dominant_trait_label: str | None = Field(default=None)
    weak_focus_labels: list[str] = Field(default_factory=list)
    radar_points: list[TraitRadarPoint] = Field(default_factory=list)
    signal_cards: list[Fr61SignalDeltaCard] = Field(default_factory=list)
    top_insights: list[TraitInsightCard] = Field(default_factory=list)
    production_lock: ProductionLockExplanation = Field(...)
    theme: ScoreViewerTheme = Field(...)
    source_availability_banner: str = Field(..., min_length=1)

class ScoreViewerAckRequest(BaseModel):
    insight_key: str = Field(..., min_length=1)
    acknowledged_next_step: str = Field(..., min_length=1)

class ScoreViewerAckResponse(BaseModel):
    coach_id: str = Field(..., min_length=1)
    ack_id: str = Field(..., min_length=1)
    insight_key: str = Field(..., min_length=1)
    receipt_id: str = Field(..., min_length=1)

class TraitDetailPayload(BaseModel):
    coach_id: str = Field(..., min_length=1)
    trait_name: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    score: int = Field(..., ge=1, le=10)
    score_band: ViewerScoreBand = Field(...)
    category: str = Field(..., min_length=1)
    evidence: list[EvidenceCitationCard] = Field(default_factory=list)
    meaning: ScoreMeaningBlock = Field(...)
    history_points: list[int] = Field(default_factory=list)
