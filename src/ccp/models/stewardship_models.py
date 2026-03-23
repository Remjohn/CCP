"""
CCP Pydantic Models — Stewardship Mode
FR-GA Task 4 — Models for Signal Monitoring Protocol (DEP-PROTO-020)
and Stewardship Reports (DEP-ENG-053).

Spec reference: FR_GA_Guardian_Agent_Tech_Spec.md §Stewardship Mode
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class SignalType(str, Enum):
    """Three signal categories monitored weekly by the Guardian Agent.

    Spec reference: FR_GA_Guardian_Agent_Tech_Spec.md §Signal Monitoring Protocol
    """

    LEXICON_DRIFT = "LEXICON_DRIFT"
    CULTURAL_EVOLUTION = "CULTURAL_EVOLUTION"
    CAMPAIGN_FATIGUE = "CAMPAIGN_FATIGUE"


class RecommendationStatus(str, Enum):
    """Status of a refresh recommendation."""

    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXECUTED = "EXECUTED"


class SignalDetection(BaseModel):
    """A single detected signal from the weekly monitoring sweep."""

    signal_type: SignalType = Field(..., description="Category of signal detected")
    detected_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO 8601 UTC timestamp of detection",
    )
    evidence: list[str] = Field(
        default_factory=list,
        description="Specific evidence items supporting this detection",
    )
    severity: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Severity score (0.0 = informational, 1.0 = critical)",
    )
    affected_dep_ids: list[str] = Field(
        default_factory=list,
        description="DEP-IDs affected by this signal (e.g., DEP-ENG-007)",
    )
    metrics: dict[str, Any] = Field(
        default_factory=dict,
        description="Quantitative metrics (e.g., unmapped_term_count, relevance_score_avg)",
    )


class RefreshRecommendation(BaseModel):
    """A recommendation for foundational data refresh.

    Spec reference: FR_GA_Guardian_Agent_Tech_Spec.md §Stewardship Mode
    AC3: A Stewardship refresh recommendation is NOT executed until
    /ccf-guardian approve [recommendation_id] is issued.
    """

    recommendation_id: str = Field(
        ...,
        description="Unique ID for this recommendation",
    )
    coach_id: str = Field(..., description="Coach Person ID")
    signal_type: SignalType = Field(..., description="Which signal triggered this")
    signal_detections: list[SignalDetection] = Field(
        default_factory=list,
        description="Signal detections that led to this recommendation",
    )
    recommended_action: str = Field(
        ...,
        description="Specific action recommended (e.g., 'Refresh Tribe Lexicon entries: ...')",
    )
    affected_components: list[str] = Field(
        default_factory=list,
        description="Components that would be modified (e.g., 'character_lexicon', 'tribe_soul')",
    )
    status: RecommendationStatus = Field(
        default=RecommendationStatus.PENDING,
        description="Current status — PENDING until operator approves via slash command",
    )
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO 8601 UTC timestamp",
    )
    approved_at: Optional[str] = Field(
        default=None,
        description="Timestamp of operator approval (None if not yet approved)",
    )
    approved_by: Optional[str] = Field(
        default=None,
        description="Operator ID who approved (None if not yet approved)",
    )
    executed_at: Optional[str] = Field(
        default=None,
        description="Timestamp of execution (None if not yet executed)",
    )
    receipt_id: Optional[str] = Field(
        default=None,
        description="Receipt chain ID for the approval/execution",
    )


class EvolutionaryRecalibration(BaseModel):
    """Tracks sustained TTT drift for potential DEP-ENG-005 re-extraction.

    Spec reference: FR_GA_Guardian_Agent_Tech_Spec.md §Evolutionary Recalibration Handshake
    If coach sustains >15% TTT drift towards a NEW authentic vector for 4 consecutive
    weeks, trigger DEP-ENG-005 Re-Extraction Event. Sophia's baseline permanently updated.
    """

    coach_id: str = Field(..., description="Coach Person ID")
    drift_direction: str = Field(
        default="",
        description="Description of the new authentic vector detected",
    )
    consecutive_weeks: int = Field(
        default=0,
        ge=0,
        description="Number of consecutive weeks drift sustained above threshold",
    )
    drift_percentages: list[float] = Field(
        default_factory=list,
        description="Weekly drift percentages recorded (most recent last)",
    )
    threshold: float = Field(
        default=0.15,
        description="Drift threshold (15% per spec)",
    )
    trigger_threshold_weeks: int = Field(
        default=4,
        description="Consecutive weeks required to trigger re-extraction",
    )
    re_extraction_triggered: bool = Field(
        default=False,
        description="True if re-extraction event was triggered",
    )
    triggered_at: Optional[str] = Field(
        default=None,
        description="Timestamp when re-extraction was triggered",
    )

    def should_trigger(self) -> bool:
        """Check if conditions met for DEP-ENG-005 re-extraction."""
        return (
            self.consecutive_weeks >= self.trigger_threshold_weeks
            and not self.re_extraction_triggered
        )


class DataPromotionTimeout(BaseModel):
    """Tracks patterns awaiting Semantic memory promotion.

    Spec reference: FR_GA_Guardian_Agent_Tech_Spec.md §Data Promotion Timeout Deadlock
    14-consecutive-session threshold + 21-day unreviewed → CRITICAL_BLOCKING →
    pipeline halt. NO silent auto-promotion bypass.
    """

    pattern_id: str = Field(..., description="Unique pattern identifier")
    coach_id: str = Field(..., description="Coach Person ID")
    pattern_description: str = Field(
        default="",
        description="What the pattern captures",
    )
    consecutive_sessions: int = Field(
        default=0,
        ge=0,
        description="Number of consecutive sessions this pattern appeared",
    )
    session_threshold: int = Field(
        default=14,
        description="Sessions required for promotion eligibility",
    )
    queued_at: Optional[str] = Field(
        default=None,
        description="When the pattern entered the review queue",
    )
    status: str = Field(
        default="TRACKING",
        description="TRACKING | PENDING | CRITICAL_BLOCKING | PROMOTED | REJECTED",
    )
    timeout_days: int = Field(
        default=21,
        description="Days before PENDING escalates to CRITICAL_BLOCKING",
    )

    def is_blocking(self) -> bool:
        """Check if this pattern is blocking pipeline execution."""
        return self.status == "CRITICAL_BLOCKING"

    def check_timeout(self) -> bool:
        """Check if the pattern has exceeded the timeout and should escalate."""
        if self.status != "PENDING" or self.queued_at is None:
            return False
        queued = datetime.fromisoformat(self.queued_at)
        now = datetime.now(timezone.utc)
        # Ensure queued is timezone-aware
        if queued.tzinfo is None:
            queued = queued.replace(tzinfo=timezone.utc)
        elapsed = (now - queued).days
        return elapsed >= self.timeout_days


class StewardshipReport(BaseModel):
    """Quarterly compiled Stewardship Report (DEP-ENG-053).

    Spec reference: FR_GA_Guardian_Agent_Tech_Spec.md §Stewardship Report
    Includes relevance assessments, signal occurrences, logged approved
    refreshes, and upcoming recommendations.
    """

    report_id: str = Field(..., description="Unique report identifier")
    coach_id: str = Field(..., description="Coach Person ID")
    coach_acronym: str = Field(..., min_length=3, max_length=3)
    quarter: str = Field(
        ...,
        description="Quarter identifier (e.g., '2026-Q1')",
    )
    generated_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO 8601 UTC timestamp of report generation",
    )
    # Signal summary
    total_signals_detected: int = Field(default=0)
    signals_by_type: dict[str, int] = Field(
        default_factory=dict,
        description="Count of signals per type (LEXICON_DRIFT, CULTURAL_EVOLUTION, CAMPAIGN_FATIGUE)",
    )
    signal_detections: list[SignalDetection] = Field(
        default_factory=list,
        description="All signal detections in this quarter",
    )
    # Recommendation summary
    total_recommendations: int = Field(default=0)
    approved_recommendations: list[RefreshRecommendation] = Field(
        default_factory=list,
        description="Recommendations that were approved and executed",
    )
    pending_recommendations: list[RefreshRecommendation] = Field(
        default_factory=list,
        description="Recommendations still awaiting operator action",
    )
    rejected_recommendations: list[RefreshRecommendation] = Field(
        default_factory=list,
        description="Recommendations that were rejected",
    )
    # Relevance assessments
    character_lexicon_health: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Average relevance score across Character Lexicon entries",
    )
    tribe_lexicon_coverage: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Percentage of active tribal vocabulary mapped in the lexicon",
    )
    campaign_diversity_score: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Semiotic diversity in recent campaigns (1.0 = no fatigue)",
    )
    # Evolutionary tracking
    ttt_drift_status: Optional[EvolutionaryRecalibration] = Field(
        default=None,
        description="Current TTT drift tracking status",
    )
    data_promotion_queue: list[DataPromotionTimeout] = Field(
        default_factory=list,
        description="Patterns awaiting Semantic memory promotion",
    )
    # Upcoming recommendations
    upcoming_recommendations: list[str] = Field(
        default_factory=list,
        description="Proactive recommendations for the next quarter",
    )
