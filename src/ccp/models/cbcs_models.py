"""
CBCS — Conscious Behavioral Change System — Shared Models
==========================================================
Central Pydantic model definitions for the CBCS Relationship Intelligence
phase (FR-CBCS-01 through FR-CBCS-14).

Each FR-CBCS spec appends its models here in dependency order.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ════════════════════════════════════════════════════════════════════════
# FR-CBCS-02 — Social Penetration Depth Gauge
# ════════════════════════════════════════════════════════════════════════

# ── Constants ──────────────────────────────────────────────────────────

# LIWC-22 thresholds for SPT stage classification (§4 Stage 2)
FIRST_PERSON_FREQ_THRESHOLD: float = 0.05
EMOTIONAL_COMPLEXITY_THRESHOLD: float = 0.2
EXCLUSIVE_WORDS_THRESHOLD: float = 0.1
HEDGING_WORDS_THRESHOLD: float = 0.05
COGNITIVE_PROCESSES_THRESHOLD: float = 0.15

# Trailing windows (days) for classification
TRAILING_WINDOW_14_DAYS: int = 14
TRAILING_WINDOW_30_DAYS: int = 30

# Delivery gate thresholds (§4 Stage 3)
DELIVERY_SPT_MINIMUM: int = 3
DELIVERY_COPING_MINIMUM: int = 3
BLOCKED_MOOD_STATES: list[str] = ["Processing", "Tension", "Escape"]

# Provisional delay (hours)
PROVISIONAL_DELAY_HOURS: int = 24


# ── Enums ──────────────────────────────────────────────────────────────


class SPTStage(int, Enum):
    """Social Penetration Theory stages (Altman & Taylor, 1973)."""
    ORIENTATION = 1
    EXPLORATORY_AFFECTIVE = 2
    AFFECTIVE_EXCHANGE = 3
    STABLE_EXCHANGE = 4


class DeliveryVerdict(str, Enum):
    """Triple-Condition Delivery Permission Gate verdicts."""
    PASS = "PASS"
    PROVISIONAL = "PROVISIONAL"
    FAIL = "FAIL"


class SPTError(str, Enum):
    """Error codes for the Social Penetration Depth Gauge."""
    INVALID_COACH_ACRONYM = "INVALID_COACH_ACRONYM"
    MISSING_VOICE_PROFILE = "MISSING_VOICE_PROFILE"
    MISSING_LIWC_SCORES = "MISSING_LIWC_SCORES"
    CLASSIFICATION_ERROR = "CLASSIFICATION_ERROR"
    GATE_EVALUATION_ERROR = "GATE_EVALUATION_ERROR"


class BlockingReason(str, Enum):
    """Exact blocking-reason strings for the delivery gate."""
    SPT_FAILED = "SPT_FAILED"
    MOOD_FAILED = "MOOD_FAILED"
    COPING_FAILED = "COPING_FAILED"


# ── Models ─────────────────────────────────────────────────────────────


class LIWCScores(BaseModel):
    """LIWC-22 marker scores from client Voice DNA disclosure profiles."""
    first_person_freq: float = Field(
        ..., ge=0.0, le=1.0,
        description="First-person pronoun frequency (normalised).",
    )
    emotional_complexity: float = Field(
        ..., ge=0.0, le=1.0,
        description="Emotional complexity score.",
    )
    exclusive_words: float = Field(
        default=0.0, ge=0.0, le=1.0,
        description="Exclusive word frequency (but, except, without).",
    )
    hedging_words: float = Field(
        default=0.0, ge=0.0, le=1.0,
        description="Hedging word frequency (maybe, sort of, perhaps).",
    )
    cognitive_processes: float = Field(
        default=0.0, ge=0.0, le=1.0,
        description="Cognitive process word frequency.",
    )


class SPTClassificationResult(BaseModel):
    """Output of Stage 1 — SPT stage classification for a single client."""
    client_id: str = Field(...)
    coach_id: str = Field(..., description="ADR-01 boundary.")
    spt_stage: int = Field(..., ge=1, le=4)
    spt_stage_name: str = Field(...)
    trailing_window_days: int = Field(...)
    liwc_snapshot: LIWCScores = Field(...)
    classification_warnings: list[str] = Field(default_factory=list)
    timestamp_utc: str = Field(...)


class SPTDepthGaugeRow(BaseModel):
    """Persisted row in social_penetration_depth_gauge table."""
    client_id: str = Field(...)
    coach_id: str = Field(...)
    spt_stage: int = Field(..., ge=1, le=4)
    spt_stage_name: str = Field(...)
    previous_stage: int = Field(default=1, ge=1, le=4)
    trailing_window_days: int = Field(...)
    last_computed_utc: str = Field(...)


class DeliveryPermissionGateEval(BaseModel):
    """Output schema for the Triple-Condition Delivery Permission Gate (§5)."""
    gate_id: str = Field(...)
    client_id: str = Field(...)
    coach_id: str = Field(..., description="ADR-01 boundary.")
    spt_condition: bool = Field(...)
    mood_condition: bool = Field(...)
    coping_condition: bool = Field(...)
    all_passed: bool = Field(...)
    verdict: str = Field(...)
    blocking_reason: list[str] = Field(default_factory=list)
    provisional_delay_hours: int = Field(default=0)
    last_evaluated: str = Field(...)


# ════════════════════════════════════════════════════════════════════════
# FR-CBCS-07 — Telegram Intimacy Index
# ════════════════════════════════════════════════════════════════════════

# ── Constants ──────────────────────────────────────────────────────────

# TII calculation window
TII_WINDOW_DAYS: int = 30

# Maximum expected messages per day for frequency normalization (§4 Stage 4)
MAX_EXPECTED_FREQUENCY: float = 3.0

# Maximum hours for latency normalization
MAX_LATENCY_HOURS: float = 24.0

# Voice note ratio multiplier
VOICE_RATIO_MULTIPLIER: float = 2.0

# Component weights for composite TII (§4 Stage 4)
TII_WEIGHT_FREQUENCY: float = 0.10
TII_WEIGHT_CONSISTENCY: float = 0.15
TII_WEIGHT_DISCLOSURE: float = 0.30
TII_WEIGHT_LATENCY: float = 0.10
TII_WEIGHT_VOICE: float = 0.10
TII_WEIGHT_INITIATIVE: float = 0.25

# Gate thresholds (§4 Stage 2)
TII_PASS_THRESHOLD: float = 0.4
TII_PROVISIONAL_FLOOR: float = 0.3
TII_PROVISIONAL_CONSISTENCY: float = 0.8

# PSR stage boundaries (§4 Stage 3)
PSR_INTENSE_PERSONAL_THRESHOLD: float = 0.4
PSR_BORDERLINE_THRESHOLD: float = 0.8


# ── Enums ──────────────────────────────────────────────────────────────


class PSRStage(str, Enum):
    """Parasocial Relationship stages (Horton & Wohl, 1956)."""
    ENTERTAINMENT_SOCIAL = "Entertainment-Social"
    INTENSE_PERSONAL = "Intense-Personal"
    BORDERLINE = "Borderline"


class TIIVerdict(str, Enum):
    """TII Delivery Threshold Gate verdicts."""
    PASS = "PASS"
    PROVISIONAL = "PROVISIONAL"
    FAIL = "FAIL"


class TIIError(str, Enum):
    """Error codes for the Telegram Intimacy Index."""
    INVALID_COACH_ACRONYM = "INVALID_COACH_ACRONYM"
    MISSING_MESSAGE_HISTORY = "MISSING_MESSAGE_HISTORY"
    ZERO_DIVISION_GUARD = "ZERO_DIVISION_GUARD"
    CALCULATION_ERROR = "CALCULATION_ERROR"


# ── Models ─────────────────────────────────────────────────────────────


class ClientMessageStats(BaseModel):
    """Aggregated message statistics for TII calculation (30-day window)."""
    client_id: str = Field(...)
    message_count: int = Field(default=0, ge=0)
    days_active_in_last_30: int = Field(default=0, ge=0, le=30)
    avg_response_time_hours: float = Field(default=24.0, ge=0.0)
    voice_message_count: int = Field(default=0, ge=0)
    total_client_messages: int = Field(default=0, ge=0)
    days_client_initiated: int = Field(default=0, ge=0)
    spt_stage: int = Field(default=1, ge=1, le=4)


class TIIComponentScores(BaseModel):
    """Individual TII component scores (all 0.0-1.0)."""
    interaction_frequency_score: float = Field(..., ge=0.0, le=1.0)
    consistency_score: float = Field(..., ge=0.0, le=1.0)
    disclosure_depth_score: float = Field(..., ge=0.0, le=1.0)
    response_latency_score: float = Field(..., ge=0.0, le=1.0)
    voice_note_ratio_score: float = Field(..., ge=0.0, le=1.0)
    initiative_frequency_score: float = Field(..., ge=0.0, le=1.0)


class TelegramIntimacyIndexRow(BaseModel):
    """Persisted row in telegram_intimacy_index table (§5)."""
    tii_id: str = Field(...)
    client_id: str = Field(...)
    coach_id: str = Field(..., description="ADR-01 boundary.")
    interaction_frequency_score: float = Field(..., ge=0.0, le=1.0)
    consistency_score: float = Field(..., ge=0.0, le=1.0)
    disclosure_depth_score: float = Field(..., ge=0.0, le=1.0)
    response_latency_score: float = Field(..., ge=0.0, le=1.0)
    voice_note_ratio_score: float = Field(..., ge=0.0, le=1.0)
    initiative_frequency_score: float = Field(..., ge=0.0, le=1.0)
    composite_tii: float = Field(..., ge=0.0, le=1.0)
    psr_stage: str = Field(...)
    last_computed: str = Field(...)


class TIIGateResult(BaseModel):
    """Output of the TII Delivery Threshold Gate (§4 Stage 2)."""
    client_id: str = Field(...)
    coach_id: str = Field(...)
    composite_tii: float = Field(..., ge=0.0, le=1.0)
    consistency_score: float = Field(..., ge=0.0, le=1.0)
    verdict: str = Field(...)
    operator_alert: Optional[str] = Field(default=None)
    last_evaluated: str = Field(...)


# ════════════════════════════════════════════════════════════════════════
# FR-CBCS-04 — Information Coping Trajectory Mapper
# ════════════════════════════════════════════════════════════════════════

# ── Constants ──────────────────────────────────────────────────────────

# LIWC thresholds for individual position classification (§4 Stage 2)
ICT_SOCIAL_WORDS_THRESHOLD: float = 0.15
ICT_INSIGHT_THRESHOLD_HIGH: float = 0.05
ICT_INSIGHT_THRESHOLD_LOW: float = 0.03
ICT_COGNITIVE_PROCESSES_THRESHOLD_HIGH: float = 0.15
ICT_COGNITIVE_PROCESSES_THRESHOLD_LOW: float = 0.10
ICT_POSITIVE_EMOTION_THRESHOLD: float = 0.05
ICT_INFORMATION_SEEKING_THRESHOLD: float = 0.1
ICT_FUTURE_FOCUS_THRESHOLD: float = 0.05
ICT_ANXIETY_THRESHOLD: float = 0.02
ICT_NEGATIVE_EMOTION_THRESHOLD: float = 0.05
ICT_INTERACTION_FREQ_THRESHOLD: float = 1.0  # per week

# Position 5 sustained-period requirement (days)
ICT_POSITION_4_SUSTAINED_DAYS: int = 30

# Tribe aggregation gate thresholds (§4 Stage 3)
TRIBE_SAMPLE_PASS_THRESHOLD: int = 5
TRIBE_DEFAULT_POSITION: int = 2

# Content archetype mapping
CONTENT_ARCHETYPE_MAP: dict[str, str] = {
    "low": "Validation/Defense",
    "mid": "Curiosity/Bridge",
    "high": "Expansion/Agency",
}

# Position label map
POSITION_LABEL_MAP: dict[int, str] = {
    1: "Deficiency",
    2: "Ill-Informed",
    3: "Needs Injection",
    4: "Information Health",
    5: "Information Donor",
}


# ── Enums ──────────────────────────────────────────────────────────────


class ICTError(str, Enum):
    """Error types for the ICT Mapper."""
    MISSING_LIWC_SCORES = "MISSING_LIWC_SCORES"
    CLASSIFICATION_ERROR = "CLASSIFICATION_ERROR"
    AGGREGATION_ERROR = "AGGREGATION_ERROR"
    INVALID_COACH_SCOPE = "INVALID_COACH_SCOPE"


class TribeGateVerdict(str, Enum):
    """Tribe minimum-sample gate verdicts (§4 Stage 3)."""
    PASS = "PASS"
    PROVISIONAL = "PROVISIONAL"
    FAIL = "FAIL"


# ── Models ─────────────────────────────────────────────────────────────


class ICTLiwcScores(BaseModel):
    """LIWC-22 dimensions required for ICT classification (§4 Stage 2)."""
    cognitive_processes: float = Field(..., ge=0.0)
    positive_emotion: float = Field(default=0.0, ge=0.0)
    negative_emotion: float = Field(default=0.0, ge=0.0)
    anxiety: float = Field(default=0.0, ge=0.0)
    insight: float = Field(default=0.0, ge=0.0)
    social_words: float = Field(default=0.0, ge=0.0)
    information_seeking: float = Field(default=0.0, ge=0.0)
    future_focus: float = Field(default=0.0, ge=0.0)


class InformationCopingTrajectoryRow(BaseModel):
    """Primary output — individual ICT classification (§5)."""
    ict_id: str = Field(...)
    client_id: str = Field(...)
    coach_id: str = Field(...)
    position: int = Field(..., ge=1, le=5)
    position_label: str = Field(...)
    liwc_markers_snapshot: dict[str, float] = Field(...)
    classification_confidence: float = Field(..., ge=0.0, le=1.0)
    last_updated: str = Field(...)


class PositionDistribution(BaseModel):
    """Percentage distribution across the 5 coping positions."""
    p1: float = Field(default=0.0, ge=0.0, le=1.0)
    p2: float = Field(default=0.0, ge=0.0, le=1.0)
    p3: float = Field(default=0.0, ge=0.0, le=1.0)
    p4: float = Field(default=0.0, ge=0.0, le=1.0)
    p5: float = Field(default=0.0, ge=0.0, le=1.0)


class TribeIctSnapshotRow(BaseModel):
    """Primary output — tribe-level ICT aggregation (§5)."""
    snapshot_id: str = Field(...)
    coach_id: str = Field(...)
    aggregate_position: int = Field(..., ge=1, le=5)
    position_distribution: PositionDistribution = Field(...)
    recommended_content_archetype: str = Field(...)
    computed_date: str = Field(...)


# ════════════════════════════════════════════════════════════════════════
# FR-CBCS-01 — Change Talk Vault
# ════════════════════════════════════════════════════════════════════════

# ── Constants ──────────────────────────────────────────────────────────

# DARN-CAT regex patterns (§4 Stage 3)
DARN_CAT_PATTERNS: dict[str, str] = {
    "Desire": r"\b(want|wish|desire|hope\s+to)\b",
    "Ability": r"\b(can|able\s+to|possible\s+to|could)\b",
    "Reasons": r"\b(because|since|so\s+that)\b",
    "Need": r"\b(must|have\s+to|need\s+to|got\s+to)\b",
    "Commitment": r"\b(will|promise|swear|guarantee|definitely\s+going\s+to)\b",
    "Activation": r"\b(ready|prepared|starting\s+tomorrow|willing)\b",
    "Taking_Steps": r"\b(started|did|completed|just\s+finished)\b",
}

# Vault quality gate thresholds (§4 Stage 5)
VAULT_PASS_THRESHOLD: int = 3
VAULT_PROVISIONAL_MIN: int = 1

# Emotional modes (§5 enum)
EMOTIONAL_MODES: list[str] = [
    "Escape", "Processing", "Discovery", "Status",
    "Tension", "Vulnerability", "Recognition",
]


# ── Enums ──────────────────────────────────────────────────────────────


class DarnCatDimension(str, Enum):
    """DARN-CAT commitment language dimensions (Miller & Rollnick, 2012)."""
    DESIRE = "Desire"
    ABILITY = "Ability"
    REASONS = "Reasons"
    NEED = "Need"
    COMMITMENT = "Commitment"
    ACTIVATION = "Activation"
    TAKING_STEPS = "Taking_Steps"


class VaultGateVerdict(str, Enum):
    """Minimum Vault Threshold Gate verdicts (§4 Stage 5)."""
    PASS = "PASS"
    PROVISIONAL = "PROVISIONAL"
    FAIL = "FAIL"


class ChangeTalkError(str, Enum):
    """Error types for the Change Talk Vault."""
    EMPTY_TEXT = "EMPTY_TEXT"
    EXTRACTION_ERROR = "EXTRACTION_ERROR"
    DB_WRITE_ERROR = "DB_WRITE_ERROR"
    INVALID_COACH_SCOPE = "INVALID_COACH_SCOPE"


# ── Models ─────────────────────────────────────────────────────────────


class ChangeTalkArchiveRow(BaseModel):
    """Primary output — single DARN-CAT extracted entry (§5)."""
    entry_id: str = Field(...)
    client_id: str = Field(...)
    coach_id: str = Field(...)
    statement_text: str = Field(...)
    darn_cat_dimension: str = Field(...)
    liwc_intensity_score: float = Field(..., ge=0.0, le=100.0)
    coping_stage_at_time: int = Field(..., ge=1, le=5)
    emotional_mode: str = Field(...)
    timestamp: str = Field(...)


class VaultQueryResult(BaseModel):
    """Result of querying the vault for a client's commitment entries."""
    client_id: str = Field(...)
    coach_id: str = Field(...)
    total_entries: int = Field(..., ge=0)
    commitment_count: int = Field(..., ge=0)
    verdict: str = Field(...)
    confidence_flag: Optional[str] = Field(default=None)
    top_statement: Optional[ChangeTalkArchiveRow] = Field(default=None)


# ════════════════════════════════════════════════════════════════════════
# FR-CBCS-06 — SEARCH Phase Detection Engine
# ════════════════════════════════════════════════════════════════════════

# ── Constants ──────────────────────────────────────────────────────────

# 4-signal convergence thresholds (§4 Stage 1)
SEARCH_INFO_SEEKING_THRESHOLD: float = 0.08
SEARCH_FUTURE_FOCUS_THRESHOLD: float = 0.05
SEARCH_AGENCY_WORDS_THRESHOLD: float = 0.05
SEARCH_HEDGING_WORDS_MAX: float = 0.02

# Minimum word count for stable ratios (§4 Stage 1)
SEARCH_MIN_WORD_COUNT: int = 10

# Reconsolidation window bounds (hours) (§4 Stage 2)
SEARCH_MIN_HOURS: float = 4.0
SEARCH_MAX_HOURS: float = 24.0


# ── Enums ──────────────────────────────────────────────────────────────


class SearchPhaseStatus(str, Enum):
    """SEARCH phase detection lifecycle states (§4 Stage 3)."""
    DETECTING = "DETECTING"
    CONFIRMED = "CONFIRMED"
    PROVISIONAL_WAIT = "PROVISIONAL_WAIT"
    EXPIRED = "EXPIRED"
    MANUAL_OVERRIDE = "MANUAL_OVERRIDE"


class SearchPhaseError(str, Enum):
    """Error types for the SEARCH Phase Detection Engine."""
    INSUFFICIENT_WORDS = "INSUFFICIENT_WORDS"
    CONVERGENCE_FAILURE = "CONVERGENCE_FAILURE"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INVALID_COACH_SCOPE = "INVALID_COACH_SCOPE"


# ── Models ─────────────────────────────────────────────────────────────


class SearchLiwcSignals(BaseModel):
    """4 LIWC signals required for SEARCH convergence (§4 Stage 1)."""
    info_seeking: float = Field(..., ge=0.0)
    future_focus: float = Field(..., ge=0.0)
    agency_words: float = Field(..., ge=0.0)
    hedging_words: float = Field(..., ge=0.0)


class SearchPhaseDetectionRow(BaseModel):
    """Primary output — SEARCH phase detection event (§5)."""
    detection_id: str = Field(...)
    client_id: str = Field(...)
    coach_id: str = Field(...)
    analytical_thinking_score: float = Field(...)
    discrepancy_word_freq: float = Field(...)
    future_focus_freq: float = Field(...)
    self_reference_freq: float = Field(...)
    cluster_confidence_score: float = Field(..., ge=0.0, le=1.0)
    status: str = Field(...)
    triggered_priming_at: Optional[str] = Field(default=None)
    last_updated: str = Field(...)


# ════════════════════════════════════════════════════════════════════════
# FR-CBCS-03 — Personal Relevance Trigger
# ════════════════════════════════════════════════════════════════════════

# ── Constants ──────────────────────────────────────────────────────────

# Behavioral pattern regex (§4 Stage 3)
BEHAVIORAL_PATTERNS: list[str] = [
    r"\bmissed\b", r"\bstopped\b", r"\bfailed\s+to\b",
    r"\bdidn'?t\s+do\b", r"\blast\s+time\s+you\b",
    r"\bhabit\s+tracking\b", r"\bdays\s+in\s+a\s+row\b",
]

# Identity pattern regex (§4 Stage 3)
IDENTITY_PATTERNS: list[str] = [
    r"\bwho\s+you\s+are\b", r"\bidentity\b", r"\bvalues\b",
    r"\bbelief\b", r"\bthe\s+kind\s+of\s+person\b",
]

# Defense mechanism mappings (§4 Stage 2)
DEFENSE_MECHANISM_MAP: dict[str, str] = {
    "Intellectualization": "Retreats into logic to avoid vulnerable processing",
    "Avoidance": "Deflects attention away from the core emotional wound",
}
DEFENSE_FALLBACK: str = "General Resistance"

# Primary driver fallback
PRIMARY_DRIVER_FALLBACK: str = "Autonomy"


# ── Enums ──────────────────────────────────────────────────────────────


class IdentityTriggerVerdict(str, Enum):
    """Identity-First Trigger Gate verdicts (§4 Stage 3)."""
    PASS = "PASS"
    PROVISIONAL = "PROVISIONAL"
    FAIL = "FAIL"


class PersonalRelevanceError(str, Enum):
    """Error types for the Personal Relevance Trigger."""
    MISSING_EMOTIONAL_DNA = "MISSING_EMOTIONAL_DNA"
    SYNTHESIS_ERROR = "SYNTHESIS_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INVALID_COACH_SCOPE = "INVALID_COACH_SCOPE"


# ── Models ─────────────────────────────────────────────────────────────


class EmotionalArchitecture(BaseModel):
    """Nested emotional architecture within the identity profile."""
    primary_driver: str = Field(...)
    defense_mechanism: str = Field(...)


class UnifiedIdentityProfile(BaseModel):
    """Primary output — synthesized client identity profile (§5)."""
    client_id: str = Field(...)
    coach_id: str = Field(...)
    core_identity_statement: str = Field(...)
    emotional_architecture: EmotionalArchitecture = Field(...)
    highest_intensity_change_talk: str = Field(...)
    last_synthesized: str = Field(...)


class IdentityTargetingVerdict(BaseModel):
    """Output of the Identity-First Trigger Gate (§4 Stage 3)."""
    is_valid: bool = Field(...)
    verdict: str = Field(...)
    rewrite_instruction: Optional[str] = Field(default=None)
    rejected_behavioral_phrases: list[str] = Field(default_factory=list)


# ════════════════════════════════════════════════════════════════════════
# FR-CBCS-08 — Transportation Score Gate
# ════════════════════════════════════════════════════════════════════════

# ── Constants ──────────────────────────────────────────────────────────

# 13 Sensory detail words (§4 Stage 2)
SENSORY_WORDS: list[str] = [
    "see", "smell", "hear", "feel", "taste",
    "look", "sound", "dark", "bright", "cold",
    "hot", "heavy", "light",
]

# 9 Distancing language words — strictly forbidden (§4 Stage 2)
DISTANCING_WORDS: list[str] = [
    "maybe", "might", "could", "probably", "perhaps",
    "i think", "sort of", "kind of", "guess",
]

# Prosodic match threshold (§4 Stage 3)
PROSODIC_MATCH_THRESHOLD: float = 0.85

# Max rewrite attempts before permanent FAIL
TRANSPORT_MAX_REWRITE_ATTEMPTS: int = 3


# ── Enums ──────────────────────────────────────────────────────────────


class TransportGateVerdict(str, Enum):
    """Transportation Score Gate verdicts (§4 Stage 3)."""
    PASS = "PASS"
    FAIL = "FAIL"
    PROVISIONAL_REVIEW = "PROVISIONAL_REVIEW"


class TransportGateError(str, Enum):
    """Error types for the Transportation Score Gate."""
    SCRIPT_EMPTY = "SCRIPT_EMPTY"
    EVALUATION_ERROR = "EVALUATION_ERROR"
    PROSODIC_MATCH_ERROR = "PROSODIC_MATCH_ERROR"
    INVALID_COACH_SCOPE = "INVALID_COACH_SCOPE"


# ── Models ─────────────────────────────────────────────────────────────


class TransportMetricsPayload(BaseModel):
    """Four Transportation Theory components (§4 Stage 2)."""
    sensory_count: int = Field(...)
    distancing_count: int = Field(...)
    prosodic_match_score: float = Field(...)
    narrative_arc_found: bool = Field(...)


class TransportationGateResult(BaseModel):
    """Primary output — Transportation Score Gate evaluation (§5)."""
    evaluation_id: str = Field(...)
    script_hash: str = Field(...)
    gate_verdict: str = Field(...)
    metrics_payload: TransportMetricsPayload = Field(...)
    failure_details: list[str] = Field(default_factory=list)
    evaluated_at: str = Field(...)


# ════════════════════════════════════════════════════════════════════════
# FR-CBCS-09 — Habit Architecture Module
# ════════════════════════════════════════════════════════════════════════

# ── Constants ──────────────────────────────────────────────────────────

# Abandonment threshold in days (§4 Stage 4)
HABIT_ABANDONMENT_DAYS: int = 14

# Abstract verbs that fail concrete_action check (§4 Stage 2)
ABSTRACT_VERBS: list[str] = [
    "feel", "be", "focus", "try", "think", "hope",
    "wish", "want", "believe", "know", "understand",
]


# ── Enums ──────────────────────────────────────────────────────────────


class HabitStatus(str, Enum):
    """Habit lifecycle state machine (§4 Stage 4)."""
    FORMING = "FORMING"
    VERIFIED = "VERIFIED"
    BROKEN = "BROKEN"
    ABANDONED = "ABANDONED"


class HabitVerificationVerdict(str, Enum):
    """Implementation Intention Verification Gate verdicts (§4 Stage 3)."""
    PASS = "PASS"
    PROVISIONAL = "PROVISIONAL"
    FAIL = "FAIL"


class HabitArchitectureError(str, Enum):
    """Error types for the Habit Architecture Module."""
    EMPTY_MESSAGE = "EMPTY_MESSAGE"
    PARSING_ERROR = "PARSING_ERROR"
    STATE_TRANSITION_ERROR = "STATE_TRANSITION_ERROR"
    INVALID_COACH_SCOPE = "INVALID_COACH_SCOPE"


# ── Models ─────────────────────────────────────────────────────────────


class HabitArchitectureTrackerRow(BaseModel):
    """Primary output — habit intention tracker row (§5)."""
    tracker_id: str = Field(...)
    client_id: str = Field(...)
    coach_id: str = Field(...)
    environmental_cue: Optional[str] = Field(default=None)
    concrete_action: Optional[str] = Field(default=None)
    habit_status: str = Field(...)
    verification_verdict: str = Field(...)
    last_checked_date: str = Field(...)


# ════════════════════════════════════════════════════════════════════════
# FR-CBCS-10 — Deep Disclosure Protocol
# ════════════════════════════════════════════════════════════════════════

# ── Constants ──────────────────────────────────────────────────────────

# LIWC thresholds for interaction mode routing (§4 Stage 1)
DISCLOSURE_NEG_EMOTION_THRESHOLD: float = 0.05
DISCLOSURE_COG_PROCESS_THRESHOLD: float = 0.1
DISCLOSURE_POS_EMOTION_THRESHOLD: float = 0.05

# SPT stage minimum for ELEVATED_CHALLENGE mode (§4 Stage 1)
DISCLOSURE_SPT_STAGE_MIN: int = 3

# Robotic qualifier phrases — strictly forbidden (§4 Stage 2)
ROBOTIC_QUALIFIERS: list[str] = [
    "As an AI",
    "I am here to help",
    "Let me know if",
    "assistant",
    "virtual",
]


# ── Enums ──────────────────────────────────────────────────────────────


class InteractionMode(str, Enum):
    """3-Mode interaction state routing (§4 Stage 1)."""
    VULNERABLE_RECEPTION = "VULNERABLE_RECEPTION"
    ELEVATED_CHALLENGE = "ELEVATED_CHALLENGE"
    ACTIVE_CONSTRUCTIVE_RESPONDING = "ACTIVE_CONSTRUCTIVE_RESPONDING"


class CasaVerdict(str, Enum):
    """CASA Linguistic Gate verdicts (§4 Stage 3)."""
    PASS = "PASS"
    PROVISIONAL_TRIMMED = "PROVISIONAL_TRIMMED"
    FAIL_REWRITE = "FAIL_REWRITE"


class DisclosureError(str, Enum):
    """Error types for the Deep Disclosure Protocol."""
    EMPTY_DRAFT = "EMPTY_DRAFT"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    MODE_ROUTING_ERROR = "MODE_ROUTING_ERROR"
    INVALID_COACH_SCOPE = "INVALID_COACH_SCOPE"


# ── Models ─────────────────────────────────────────────────────────────


class CasaMetricsPayload(BaseModel):
    """CASA linguistic metrics (§4 Stage 2)."""
    fp_count: int = Field(...)
    robotic_count: int = Field(...)
    question_count: int = Field(...)


class DisclosureInteractionLogRow(BaseModel):
    """Primary output — disclosure interaction log entry (§5)."""
    interaction_id: str = Field(...)
    client_id: str = Field(...)
    coach_id: str = Field(...)
    interaction_mode: str = Field(...)
    casa_verdict: str = Field(...)
    metrics_payload: CasaMetricsPayload = Field(...)
    final_dispatched_text: str = Field(...)
    timestamp_utc: str = Field(...)


# ════════════════════════════════════════════════════════════════════════
# FR-CBCS-11 — Neural Brand Bond Protocol
# ════════════════════════════════════════════════════════════════════════

# ── Constants ──────────────────────────────────────────────────────────

# Social noun words for dmPFC activation (§4 Stage 2)
SOCIAL_NOUNS: list[str] = [
    "person", "friend", "he", "she", "they", "people",
    "client", "someone", "brother", "sister", "manager",
]

# Brand cliché phrases — strictly forbidden (§4 Stage 2)
BRAND_CLICHES: list[str] = [
    "synergy", "unlock your potential", "next level",
    "transform your life", "scale your", "10x",
    "game changer", "revolutionary",
]

# Minimum word count for story length guard (§4 Stage 2)
BRAND_STORY_MIN_WORDS: int = 50

# Story structure mapping from brand values (§4 Stage 1)
STORY_STRUCTURE_MAP: dict[str, str] = {
    "Expansion": "HERO_JOURNEY",
    "Growth": "HERO_JOURNEY",
    "Achievement": "HERO_JOURNEY",
    "Success": "HERO_JOURNEY",
    "Security": "FAIL_STATE_WARNING",
    "Safety": "FAIL_STATE_WARNING",
    "Trust": "FAIL_STATE_WARNING",
    "Consistency": "FAIL_STATE_WARNING",
    "Discipline": "FAIL_STATE_WARNING",
    "Innovation": "PARADIGM_SHIFT",
    "Disruption": "PARADIGM_SHIFT",
    "Truth": "PARADIGM_SHIFT",
    "Awakening": "PARADIGM_SHIFT",
}


# ── Enums ──────────────────────────────────────────────────────────────


class StoryStructure(str, Enum):
    """3 strict story structural frameworks (§4 Stage 1)."""
    HERO_JOURNEY = "HERO_JOURNEY"
    FAIL_STATE_WARNING = "FAIL_STATE_WARNING"
    PARADIGM_SHIFT = "PARADIGM_SHIFT"


class DmpfcVerdict(str, Enum):
    """dmPFC Semantic Gate verdicts (§4 Stage 3)."""
    PASS = "PASS"
    PROVISIONAL_REVIEW = "PROVISIONAL_REVIEW"
    FAIL_REJECTED = "FAIL_REJECTED"


class NeuralBrandError(str, Enum):
    """Error types for the Neural Brand Bond Protocol."""
    STORY_TOO_SHORT = "STORY_TOO_SHORT"
    EVALUATION_ERROR = "EVALUATION_ERROR"
    UNKNOWN_BRAND_VALUE = "UNKNOWN_BRAND_VALUE"
    INVALID_COACH_SCOPE = "INVALID_COACH_SCOPE"


# ── Models ─────────────────────────────────────────────────────────────


class DmpfcMetricsPayload(BaseModel):
    """dmPFC semantic metrics (§4 Stage 2)."""
    social_nouns_found: int = Field(...)
    cliches_found: int = Field(...)
    moral_sentiment_matched: bool = Field(...)


class DmpfcGateVerdictRow(BaseModel):
    """Primary output — dmPFC Gate evaluation (§5)."""
    eval_id: str = Field(...)
    coach_id: str = Field(...)
    story_structure_used: str = Field(...)
    semantic_verdict: str = Field(...)
    metrics_payload: DmpfcMetricsPayload = Field(...)
    evaluated_at: str = Field(...)


# ════════════════════════════════════════════════════════════════════════
# FR-CBCS-05 — 72-Hour Identity Anchor Protocol
# ════════════════════════════════════════════════════════════════════════

# ── Constants ──────────────────────────────────────────────────────────

# Reactance gate — banned commercial phrase patterns (§4 Stage 2)
COMMERCIAL_KEYWORDS: list[str] = [
    "buy", "offer", "tomorrow", "special", "announce",
    "coming up", "get ready", "product", "program",
]

# Reactance gate — urgent punctuation pattern (§4 Stage 2)
# Matches 2+ consecutive exclamation marks OR all-caps words of 3+ letters
URGENT_PUNCTUATION_PATTERN: str = r"(!{2,}|\b[A-Z]{3,}\b)"

# Campaign cooldown after ABORT (days) (§4 Stage 3)
IDENTITY_ANCHOR_COOLDOWN_DAYS: int = 14

# Max consecutive LLM regeneration attempts before hard abort (§4 Stage 2 FAIL)
IDENTITY_ANCHOR_MAX_RETRIES: int = 3


# ── Enumerations ───────────────────────────────────────────────────────


class ProtocolStatus(str, Enum):
    """State machine statuses for the 72-Hour Protocol (§4 Stage 4)."""
    GENERATED = "GENERATED"
    D3_SENT = "D3_SENT"
    D2_SENT = "D2_SENT"
    D1_SENT = "D1_SENT"
    COMPLETED = "COMPLETED"
    ABORTED = "ABORTED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


class ReactanceVerdict(str, Enum):
    """BehavioralScienceGuard gate verdicts (§4 Stage 2)."""
    PASS = "PASS"
    PROVISIONAL = "PROVISIONAL"
    FAIL = "FAIL"


class IdentityAnchorError(str, Enum):
    """Error types for the 72-Hour Identity Anchor Protocol."""
    SCRIPT_EMPTY = "SCRIPT_EMPTY"
    MAX_RETRIES_EXCEEDED = "MAX_RETRIES_EXCEEDED"
    INVALID_COACH_SCOPE = "INVALID_COACH_SCOPE"
    STATE_MACHINE_ERROR = "STATE_MACHINE_ERROR"


# ── Models ─────────────────────────────────────────────────────────────


class ReactanceGateResult(BaseModel):
    """Output from BehavioralScienceGuard (DEP-ENG-060)."""
    verdict: str = Field(...)
    commercial_flag_count: int = Field(...)
    urgent_punctuation_count: int = Field(...)
    flagged_phrases: list[str] = Field(default_factory=list)


class ProtocolSequencePayload(BaseModel):
    """Primary output — 72-Hour sequence payload (DEP-ENG-059, §5)."""
    sequence_id: str = Field(...)
    client_id: str = Field(...)
    coach_id: str = Field(...)
    day_minus_3_script: str = Field(...)
    day_minus_2_script: str = Field(...)
    day_minus_1_script: str = Field(...)
    status: str = Field(...)
    abort_reason: Optional[str] = Field(default=None)
    last_updated: str = Field(...)


# ════════════════════════════════════════════════════════════════════════
# FR-CBCS-12 — Coping-Diagnostic Invitation Engine
# ════════════════════════════════════════════════════════════════════════

# ── Constants ──────────────────────────────────────────────────────────

# Price ceiling per coping position (§4 Stage 1)
# Indexed by coping_position (1-5); 0 = free; None = no ceiling
INVITATION_TIER_CEILINGS: dict[int, Optional[float]] = {
    1: 0.0,       # DEFICIENCY_ESCAPE_ROUTE — free only
    2: 49.0,      # ILL_INFORMED_BRIDGE — ≤ $49
    3: 399.0,     # NEEDS_INJECTION_CATALYST — ≤ $399
    4: 5000.0,    # INFORMATION_HEALTH_PARTNERSHIP — ≤ $5000
    5: None,      # DONOR_MASTERY_PATH — no ceiling
}

# Tier labels per coping position (§4 Stage 1)
INVITATION_TIER_MAP: dict[int, str] = {
    1: "DEFICIENCY_ESCAPE_ROUTE",
    2: "ILL_INFORMED_BRIDGE",
    3: "NEEDS_INJECTION_CATALYST",
    4: "INFORMATION_HEALTH_PARTNERSHIP",
    5: "DONOR_MASTERY_PATH",
}


# ── Enumerations ───────────────────────────────────────────────────────


class InvitationTier(str, Enum):
    """5 commercial tier mappings aligned to coping positions (§4 Stage 1)."""
    DEFICIENCY_ESCAPE_ROUTE = "DEFICIENCY_ESCAPE_ROUTE"
    ILL_INFORMED_BRIDGE = "ILL_INFORMED_BRIDGE"
    NEEDS_INJECTION_CATALYST = "NEEDS_INJECTION_CATALYST"
    INFORMATION_HEALTH_PARTNERSHIP = "INFORMATION_HEALTH_PARTNERSHIP"
    DONOR_MASTERY_PATH = "DONOR_MASTERY_PATH"


class CommercialRoutingVerdict(str, Enum):
    """Commercial Matrix Routing Gate verdicts (§4 Stage 2)."""
    PASS = "PASS"
    PROVISIONAL = "PROVISIONAL"
    FAIL_VIOLATION = "FAIL_VIOLATION"


class CopingInvitationError(str, Enum):
    """Error types for the Coping-Diagnostic Invitation Engine."""
    INVALID_COPING_POSITION = "INVALID_COPING_POSITION"
    ROUTING_ERROR = "ROUTING_ERROR"
    PRICE_VALIDATION_ERROR = "PRICE_VALIDATION_ERROR"
    INVALID_COACH_SCOPE = "INVALID_COACH_SCOPE"


# ── Models ─────────────────────────────────────────────────────────────


class CommercialRoutingVerdictRow(BaseModel):
    """Primary output — commercial routing verdict (DEP-ENG-067, §5)."""
    routing_id: str = Field(...)
    client_id: str = Field(...)
    coach_id: str = Field(...)
    computed_coping_position: int = Field(..., ge=1, le=5)
    invitation_tier: str = Field(...)
    target_product_price: float = Field(...)
    gate_verdict: str = Field(...)
    timestamp: str = Field(...)


# ══════════════════════════════════════════════════════════════════════
# FR-CBCS-13 — Counterfactual Activation Window
# ══════════════════════════════════════════════════════════════════════

# ── Enums ──────────────────────────────────────────────────────────────


class ActivationMode(str, Enum):
    """Counterfactual framing direction resolved from identity profile."""
    UPWARD_COUNTERFACTUAL = "UPWARD_COUNTERFACTUAL"
    DOWNWARD_COUNTERFACTUAL = "DOWNWARD_COUNTERFACTUAL"


class EpistemicGateVerdict(str, Enum):
    """Epistemic Delivery Gate verdict (§4 quality gate)."""
    PASS = "PASS"
    PROVISIONAL_EARLY_FIRE = "PROVISIONAL_EARLY_FIRE"
    FAIL_BLOCKED = "FAIL_BLOCKED"


class CounterfactualError(str, Enum):
    """Error types for the Counterfactual Activation Window."""
    INVALID_COACH_SCOPE = "INVALID_COACH_SCOPE"
    INVALID_HOURS_ELAPSED = "INVALID_HOURS_ELAPSED"
    ROUTING_ERROR = "ROUTING_ERROR"
    GATE_EVALUATION_ERROR = "GATE_EVALUATION_ERROR"


# ── Constants ──────────────────────────────────────────────────────────

# primary_driver values that map to UPWARD_COUNTERFACTUAL
UPWARD_DRIVERS: list[str] = [
    "Expansion", "Autonomy", "Growth", "Achievement",
]

# primary_driver values that map to DOWNWARD_COUNTERFACTUAL
DOWNWARD_DRIVERS: list[str] = [
    "Security", "Belonging", "Safety", "Connection",
]

# Temporal thresholds (hours)
COUNTERFACTUAL_GATE_HOURS: float = 72.0
COUNTERFACTUAL_PROVISIONAL_MIN_HOURS: float = 48.0
COUNTERFACTUAL_PROVISIONAL_COGNITIVE_THRESHOLD: float = 0.1  # cog_processes LIWC

# ── Models ─────────────────────────────────────────────────────────────


class EpistemicActivationRow(BaseModel):
    """Primary output — epistemic gate row (DEP-ENG-068, §5)."""
    eval_id: str = Field(...)
    client_id: str = Field(...)
    coach_id: str = Field(...)
    activation_mode_assigned: str = Field(...)
    gate_verdict: str = Field(...)
    hours_elapsed_since_offer: float = Field(...)
    dispatched_text: str | None = Field(default=None)
    last_evaluated: str = Field(...)


# ══════════════════════════════════════════════════════════════════════
# FR-CBCS-14 — Conscious Relationship Nurturing Architecture
# ══════════════════════════════════════════════════════════════════════

# ── Enums ──────────────────────────────────────────────────────────────


class ActiveCycle(str, Enum):
    """Temporal orchestration cycle state."""
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    CAMPAIGN = "CAMPAIGN"


class CooldownGateVerdict(str, Enum):
    """Commercial cooldown gate verdict (§4 quality gate)."""
    PASS = "PASS"
    PROVISIONAL_OVERRIDE = "PROVISIONAL_OVERRIDE"
    FAIL_COOLDOWN_ACTIVE = "FAIL_COOLDOWN_ACTIVE"


class NurturingArchError(str, Enum):
    """Error types for the Conscious Relationship Nurturing Architecture."""
    INVALID_COACH_SCOPE = "INVALID_COACH_SCOPE"
    INVALID_DAYS_ELAPSED = "INVALID_DAYS_ELAPSED"
    ORCHESTRATION_ERROR = "ORCHESTRATION_ERROR"
    QUEUE_LOCK_VIOLATION = "QUEUE_LOCK_VIOLATION"


# ── Constants ──────────────────────────────────────────────────────────

# Strict 21-day commercial cooldown threshold
COMMERCIAL_COOLDOWN_DAYS: float = 21.0

# Provisional override window: 14-21 days + client-initiated info_seeking
COMMERCIAL_COOLDOWN_PROVISIONAL_MIN_DAYS: float = 14.0

# LIWC info_seeking threshold for provisional override
COMMERCIAL_COOLDOWN_INFO_SEEKING_THRESHOLD: float = 0.1

# Weekday index for Sunday (WEEKLY cycle trigger)
WEEKLY_CYCLE_WEEKDAY: int = 6  # 0=Monday, 6=Sunday

# ── Models ─────────────────────────────────────────────────────────────


class RelationshipCycleLog(BaseModel):
    """Primary output — relationship cycle orchestration log (DEP-ENG-070/071, §5)."""
    orchestration_id: str = Field(...)
    client_id: str = Field(...)
    coach_id: str = Field(...)
    active_cycle: str = Field(...)
    queue_lock_active: bool = Field(...)
    cooldown_gate_verdict: str = Field(...)
    cooldown_expiry_timestamp: str = Field(...)
    last_executed_node: str = Field(...)
    computation_timestamp: str = Field(...)


# ══════════════════════════════════════════════════════════════════════
# FR-ERA3-18 — CBCS Four-Engine Runtime
# ══════════════════════════════════════════════════════════════════════

from datetime import datetime

from src.ccp.models.sda_models import (
    DirectionalIntegrityReport,
    EmergentContextualInvariant,
    FeedbackLoop,
    InvariantFieldPacket,
    RecursivePattern,
    RepresentationGeometryPacket,
)


class CBCSSubmissionKind(str, Enum):
    VOICE_NOTE = "voice_note"
    TEXT_REFLECTION = "text_reflection"
    JOURNAL_RESPONSE = "journal_response"


class CapacityTrack(str, Enum):
    RECOVERY = "recovery"
    FOUNDATION = "foundation"
    GROWTH = "growth"
    MOMENTUM = "momentum"
    PEAK = "peak"


class DiagnosticChangeType(str, Enum):
    HOLD = "hold"
    UPGRADE = "upgrade"
    DOWNGRADE = "downgrade"
    RITUAL_INTENSITY_REDUCTION = "ritual_intensity_reduction"
    REFLECTION_SUBSTITUTION = "reflection_substitution"


class RelationshipInterceptionReason(str, Enum):
    NONE = "none"
    CAPACITY_TRACK_DOWNGRADE = "capacity_track_downgrade"
    RITUAL_INTENSITY_REDUCTION = "ritual_intensity_reduction"
    EARLY_JOURNEY_SAFE_FRAMING = "early_journey_safe_framing"
    CORROSIVE_LOOP_INTERRUPTION = "corrosive_loop_interruption"
    DIRECTIONAL_INTEGRITY_FAILURE = "directional_integrity_failure"


class TrendWindowStatus(str, Enum):
    POSITIVE = "positive"
    FLAT = "flat"
    NEGATIVE = "negative"
    INSUFFICIENT = "insufficient"


class SemanticDynamicsContext(BaseModel):
    active_recursive_patterns: list[RecursivePattern] = Field(default_factory=list)
    identified_feedback_loops: list[FeedbackLoop] = Field(default_factory=list)
    emergent_contextual_invariants: list[EmergentContextualInvariant] = Field(default_factory=list)
    invariant_field_packet: Optional[InvariantFieldPacket] = Field(default=None)
    representation_geometry_packet: Optional[RepresentationGeometryPacket] = Field(default=None)


class EvidenceMetric(BaseModel):
    metric_name: str = Field(..., min_length=1)
    current_value: float = Field(...)
    previous_value: Optional[float] = Field(default=None)
    delta_value: Optional[float] = Field(default=None)
    interpretation: str = Field(..., min_length=1)


class EvidenceCitation(BaseModel):
    source_system: str = Field(..., min_length=1)
    source_ref: str = Field(..., min_length=1)
    excerpt: str = Field(..., min_length=1)


class CBCSEvidencePacket(BaseModel):
    """DEP-CBCS-402: Canonical evidence output from FR61 scoring + CBCS sub-engines."""
    evidence_packet_id: str = Field(...)
    client_id: str = Field(...)
    coach_id: str = Field(...)
    submission_kind: CBCSSubmissionKind = Field(...)
    generated_at: datetime = Field(...)
    trait_metrics: list[EvidenceMetric] = Field(default_factory=list)
    change_talk_summary: list[str] = Field(default_factory=list)
    spt_stage: Optional[int] = Field(default=None, ge=1, le=4)
    habit_verified: Optional[bool] = Field(default=None)
    citations: list[EvidenceCitation] = Field(default_factory=list)
    semantic_dynamics: SemanticDynamicsContext = Field(default_factory=SemanticDynamicsContext)
    perceptual_intake: Optional[CbcsPerceptualIntakeEnvelope] = Field(default=None)


class DiagnosticCapacityDecision(BaseModel):
    """DEP-CBCS-403: Internal-only capacity-track and difficulty adjustment decision.
    NEVER directly serialized to Telegram (Phase4-M07)."""
    decision_id: str = Field(...)
    client_id: str = Field(...)
    coach_id: str = Field(...)
    previous_track: CapacityTrack = Field(...)
    new_track: CapacityTrack = Field(...)
    change_type: DiagnosticChangeType = Field(...)
    rationale: str = Field(..., min_length=1)
    weaker_signal_names: list[str] = Field(default_factory=list)
    stronger_signal_names: list[str] = Field(default_factory=list)
    requires_relationship_intercept: bool = Field(...)
    created_at: datetime = Field(...)


class RitualAdjustmentPlan(BaseModel):
    """DEP-CBCS-404: Next ritual/drill mutation plan from diagnostic delta."""
    plan_id: str = Field(...)
    client_id: str = Field(...)
    coach_id: str = Field(...)
    ritual_type: str = Field(..., min_length=1)
    intensity_level: int = Field(..., ge=1, le=5)
    replaced_with_reflection: bool = Field(default=False)
    learning_path_reason: str = Field(..., min_length=1)
    draft_prompt: str = Field(..., min_length=1)
    scheduled_for_iso: Optional[datetime] = Field(default=None)


class MacroTrendSnapshot(BaseModel):
    window_days: int = Field(..., ge=1)
    status: TrendWindowStatus = Field(...)
    headline_metric: str = Field(..., min_length=1)
    positive_delta_label: Optional[str] = Field(default=None)
    supporting_sentence: str = Field(..., min_length=1)


class CumulativeInvestmentStats(BaseModel):
    total_sessions_completed: int = Field(..., ge=0)
    total_words_spoken: int = Field(..., ge=0)
    current_streak_days: int = Field(..., ge=0)
    strongest_hidden_gain: Optional[str] = Field(default=None)


class RelationshipTrendContext(BaseModel):
    """DEP-CBCS-405: 14/30-day macro-trend snapshot + cumulative investment."""
    context_id: str = Field(...)
    client_id: str = Field(...)
    coach_id: str = Field(...)
    fourteen_day: MacroTrendSnapshot = Field(...)
    thirty_day: MacroTrendSnapshot = Field(...)
    cumulative_stats: CumulativeInvestmentStats = Field(...)
    resonance_marker_hint: Optional[str] = Field(default=None)
    dominant_invariant_field: Optional[str] = Field(default=None)


class RelationshipFramedNotification(BaseModel):
    """DEP-CBCS-406: The ONLY user-facing message contract from this runtime."""
    notification_id: str = Field(...)
    client_id: str = Field(...)
    coach_id: str = Field(...)
    interception_reason: RelationshipInterceptionReason = Field(...)
    safe_headline: str = Field(..., min_length=1, max_length=180)
    safe_body: str = Field(..., min_length=1, max_length=1200)
    visible_macro_metric: Optional[str] = Field(default=None)
    visible_cumulative_metric: Optional[str] = Field(default=None)
    dispatch_channel: str = Field(..., min_length=1)
    integrity_report: Optional[DirectionalIntegrityReport] = Field(default=None)
    created_at: datetime = Field(...)


class CBCSRuntimeSession(BaseModel):
    """DEP-CBCS-401: Envelope for a single evidence-routing pass."""
    session_id: str = Field(...)
    client_id: str = Field(...)
    coach_id: str = Field(...)
    submission_kind: CBCSSubmissionKind = Field(...)
    evidence_packet: CBCSEvidencePacket = Field(...)
    diagnostic_decision: DiagnosticCapacityDecision = Field(...)
    ritual_plan: RitualAdjustmentPlan = Field(...)
    relationship_context: RelationshipTrendContext = Field(...)
    user_notification: RelationshipFramedNotification = Field(...)
    perceptual_recommendation: Optional[CbcsPerceptualRecommendation] = Field(default=None)


# ══════════════════════════════════════════════════════════════════════
# FR-ERA3-18 — SFL-Aware CBCS Four-Engine Runtime extension (§5)
# ══════════════════════════════════════════════════════════════════════

class VisibleScoreName(str, Enum):
    HUMANITY = "humanity"
    PRESENCE = "presence"
    TRUST = "trust"
    MEMORABILITY = "memorability"
    RESONANCE = "resonance"
    SIGNAL = "signal"
    AI_SLOP_RISK = "ai_slop_risk"


class PerceptualSeverity(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class CoachingSurfaceType(str, Enum):
    VOICE_NOTE = "voice_note"
    ACCOUNTABILITY_MESSAGE = "accountability_message"
    LIVE_REACTION_PROMPT = "live_reaction_prompt"
    JOURNALING_PROMPT = "journaling_prompt"
    RELATIONSHIP_REFRAME = "relationship_reframe"


class RecommendationClass(str, Enum):
    REINFORCE = "reinforce"
    REPAIR = "repair"
    SLOW_DOWN = "slow_down"
    SHARPEN = "sharpen"
    HUMANIZE = "humanize"
    DECOMPRESS = "decompress"
    PROOF_GROUND = "proof_ground"


class SourceSystem(str, Enum):
    FR27 = "fr_era3_27"
    FR35 = "fr_era3_35"
    LEGACY_CBCS = "legacy_cbcs"


class PerceptualSourceReference(BaseModel):
    source_system: SourceSystem = Field(...)
    source_contract_id: str = Field(..., min_length=1)
    source_artifact_id: str = Field(..., min_length=1)
    source_version: str = Field(..., min_length=1)
    generated_at_utc: str = Field(..., min_length=1)


class ScoreBand(BaseModel):
    score_0_99: int = Field(..., ge=0, le=99)
    severity: PerceptualSeverity = Field(...)
    rationale: str = Field(..., min_length=1)


class VisibleScoreCarryover(BaseModel):
    humanity: ScoreBand = Field(...)
    presence: ScoreBand = Field(...)
    trust: ScoreBand = Field(...)
    memorability: ScoreBand = Field(...)
    resonance: ScoreBand = Field(...)
    signal: ScoreBand = Field(...)
    ai_slop_risk: ScoreBand = Field(...)


class PerceptualWeaknessSignal(BaseModel):
    signal_id: str = Field(..., min_length=1)
    score_name: VisibleScoreName = Field(...)
    severity: PerceptualSeverity = Field(...)
    label: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    coaching_implication: str = Field(..., min_length=1)


class PerceptualStrengthSignal(BaseModel):
    signal_id: str = Field(..., min_length=1)
    score_name: VisibleScoreName = Field(...)
    severity: PerceptualSeverity = Field(...)
    label: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    preservation_note: str = Field(..., min_length=1)


class PerceptualEffectSummary(BaseModel):
    summary_id: str = Field(..., min_length=1)
    primary_weaknesses: list[PerceptualWeaknessSignal] = Field(default_factory=list)
    primary_strengths: list[PerceptualStrengthSignal] = Field(default_factory=list)
    anti_slop_warning_active: bool = Field(...)
    synthetic_tone_risk_active: bool = Field(...)
    recommendation_hint: str = Field(..., min_length=1)


class CardEvidenceSnapshot(BaseModel):
    board_id: str = Field(..., min_length=1)
    card_ids: list[str] = Field(default_factory=list)
    thumbnail_asset_ids: list[str] = Field(default_factory=list)
    primary_card_labels: list[str] = Field(default_factory=list)
    review_url: Optional[str] = Field(default=None)


class AuditPrescriptionItem(BaseModel):
    item_id: str = Field(..., min_length=1)
    target_score: VisibleScoreName = Field(...)
    plain_language_problem: str = Field(..., min_length=1)
    plain_language_fix: str = Field(..., min_length=1)
    urgency: PerceptualSeverity = Field(...)


class AuditIntelligenceSummaryInput(BaseModel):
    audit_id: str = Field(..., min_length=1)
    summary_headline: str = Field(..., min_length=1)
    visible_scores: VisibleScoreCarryover = Field(...)
    effect_summary: PerceptualEffectSummary = Field(...)
    prescription_items: list[AuditPrescriptionItem] = Field(default_factory=list)
    card_snapshot: Optional[CardEvidenceSnapshot] = Field(default=None)
    source_reference: PerceptualSourceReference = Field(...)


class CbcsPerceptualIntakeEnvelope(BaseModel):
    envelope_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    client_id: str = Field(..., min_length=1)
    visible_scores: VisibleScoreCarryover = Field(...)
    effect_summary: PerceptualEffectSummary = Field(...)
    source_reference: PerceptualSourceReference = Field(...)
    card_snapshot: Optional[CardEvidenceSnapshot] = Field(default=None)
    audit_prescriptions: list[AuditPrescriptionItem] = Field(default_factory=list)
    relationship_context_note: Optional[str] = Field(default=None)


class CbcsPerceptualRecommendation(BaseModel):
    recommendation_id: str = Field(..., min_length=1)
    recommendation_class: RecommendationClass = Field(...)
    target_surface: CoachingSurfaceType = Field(...)
    primary_score_target: VisibleScoreName = Field(...)
    plain_language_goal: str = Field(..., min_length=1)
    recommended_behavior: str = Field(..., min_length=1)
    prohibited_behavior: str = Field(..., min_length=1)
    explanation_for_operator: str = Field(..., min_length=1)


class VoiceNotePerceptualGuidance(BaseModel):
    guidance_id: str = Field(..., min_length=1)
    focus_score: VisibleScoreName = Field(...)
    target_duration_seconds: int = Field(..., ge=10, le=600)
    delivery_instruction: str = Field(..., min_length=1)
    pacing_instruction: str = Field(..., min_length=1)
    proof_instruction: str = Field(..., min_length=1)
    anti_slop_instruction: str = Field(..., min_length=1)
    example_prompt: str = Field(..., min_length=1)


class AccountabilityPerceptualPrescription(BaseModel):
    prescription_id: str = Field(..., min_length=1)
    focus_scores: list[VisibleScoreName] = Field(default_factory=list)
    accountability_task: str = Field(..., min_length=1)
    repetition_window_days: int = Field(..., ge=1, le=30)
    review_signal: str = Field(..., min_length=1)
    escalation_condition: str = Field(..., min_length=1)
    downgrade_sensitive: bool = Field(...)


class RelationshipFramedCoachingMessage(BaseModel):
    message_id: str = Field(..., min_length=1)
    target_surface: CoachingSurfaceType = Field(...)
    safe_headline: str = Field(..., min_length=1)
    safe_body: str = Field(..., min_length=1)
    long_loop_reference: str = Field(..., min_length=1)
    score_translation_note: str = Field(..., min_length=1)
    mentions_cards: bool = Field(...)


class CbcsPerceptualRuntimeReceipt(BaseModel):
    receipt_id: str = Field(..., min_length=1)
    envelope_id: str = Field(..., min_length=1)
    recommendation_id: str = Field(..., min_length=1)
    relationship_message_id: str = Field(..., min_length=1)
    fallback_mode: Optional[str] = Field(default=None)
    source_contract_id: str = Field(..., min_length=1)


