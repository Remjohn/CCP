"""
Step 14 — V²WS + Full Cross-System Integration + Data Intelligence Layer
Models for: FR27, FR30, FR31, FR32, FR33, FR34, FR35, FR36, FR37,
            FR41, FR42, FR43, FR45, FR46, FR47, FR48, FR49, FR50

Every field is traced to an explicit spec instruction.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator, model_validator


# ─────────────────────────────────────────────────────
# CONSTANTS (spec-traced)
# ─────────────────────────────────────────────────────

# FR27 — <2s Latency Protocol
LATENCY_P95_BUDGET_MS: int = 2000  # FR27 AC1: sub-2s guarantee
CRISIS_SCAN_BUDGET_MS: int = 100   # FR27 Stage 1 / FR31: <100ms gate
GHOST_TYPING_TRIGGER_MS: int = 1800  # FR27 §6: fallback grace trigger
TECH_LATENCY_CAP_MS: int = 2700    # FR27 Stage 2 REVISED: <2700ms end-to-end
ARTISAN_MAX_TOKENS: int = 150       # FR27 Stage 3: max_output_tokens

# FR30 — Dormancy Recovery
DORMANCY_THRESHOLDS_DAYS: list[int] = [3, 5, 10, 30]  # FR30 §4.1
DORMANCY_ARTISAN_TOKEN_CAP: int = 50  # FR30 Stage 3: <50 tokens
DORMANCY_MIN_CLIENTS_FOR_SBM: int = 3  # FR37 §6: min 3 active clients

# FR31 — Crisis Guardian
CRISIS_DICTIONARY_SIZE: int = 500  # FR31 §2: 500-word dictionary
CRISIS_SCAN_TARGET_MS: int = 100   # FR31 AC1: sub-100ms execution
CRISIS_FALSE_POSITIVE_POLICY: str = "100_FALSE_POSITIVES_OVER_1_MISSED"

# FR32 — Atlas Roadmap
ROADMAP_DAYS: int = 28  # FR32 §4.2: 28-day grid
ACTIVE_DAYS_PER_WEEK: int = 4
REFLECTION_DAYS_PER_WEEK: int = 1
REST_DAYS_PER_WEEK: int = 2
WEEKLY_OVERLOAD_MULTIPLIER: float = 1.10  # FR32 §4.3: +10% per week
ANTI_ESCALATION_LOCK_DAYS: int = 14  # FR32 §4.4: 14-day recovery block
MILESTONE_INDICES: list[int] = [6, 13, 20, 27]  # FR32 §4.2: milestone checkpoints

# FR32 — Capacity Track Thresholds (FR32 §4.1 REVISED)
RECOVERY_FEAR_THRESHOLD: float = 0.8
RECOVERY_COPING_THRESHOLD: float = 0.75
FOUNDATION_FEAR_RANGE: tuple[float, float] = (0.6, 0.79)
GROWTH_FEAR_RANGE: tuple[float, float] = (0.4, 0.59)
GROWTH_AGENCY_MIN: float = 0.5
MOMENTUM_FEAR_RANGE: tuple[float, float] = (0.2, 0.39)
MOMENTUM_AGENCY_MIN: float = 0.65
PEAK_FEAR_MAX: float = 0.2
PEAK_AGENCY_MIN: float = 0.8

# FR33 — V²WS YOLO Mode
YOLO_REQUIRED_INPUTS: int = 5
YOLO_SLIDE_WIDTH: int = 1920
YOLO_SLIDE_HEIGHT: int = 1080
YOLO_SPEAKER_NOTE_OFFSET_X: int = 2000
YOLO_SLIDE_SPACING: int = 500
YOLO_MAX_WORDS_PER_SLIDE: int = 150

# FR34 — V²WS Interactive Mode
INTERACTIVE_STALE_TIMEOUT_HOURS: int = 12

# FR36 — Transparent Collage
ALPHA_EDGE_DILATION_PX: int = 1  # FR36 §4.3: 1-pixel edge dilation

# FR41 — Cross-Ecosystem Meeting
CROSS_ECOSYSTEM_SCHEDULE_DAY: int = 1  # 1st of month
CROSS_ECOSYSTEM_MIN_ECOSYSTEMS: int = 3

# FR42 — Publer Sync
PUBLER_48H_CRON_HOURS: int = 6  # FR42 Stage 3: run every 6 hours
PUBLER_RATE_LIMIT_WAIT_S: int = 120  # FR42 Stage 4: 120-second wait

# FR43 — Data Analyst
DATA_ANALYST_MIN_GLOBAL_N: int = 10  # FR43 §4.1: N >= 10 globally
DATA_ANALYST_MIN_ARC_N: int = 5  # FR43 §4.1: N >= 5 per arc-type
DATA_ANALYST_CADENCE_DAY: str = "MONDAY"
DATA_ANALYST_CADENCE_HOUR_UTC: int = 6

# FR45 — Notion Export
NOTION_PAGE_SECTIONS: int = 7  # FR45 §4.2: 7 sections
NOTION_MAX_BLOCKS_PER_REQUEST: int = 100
NOTION_APPROVAL_POLL_MINUTES: int = 5

# FR46 — Universal Asset ID
ASSET_ID_COACH_ACRONYM_LENGTH: tuple[int, int] = (2, 4)
PERSON_ID_COACH_SEQUENCE_ZERO: str = "0000"

# FR47 — Receipt Chain Guard
RECEIPT_GENESIS_MARKER: str = "GENESIS"
RECEIPT_HASH_ALGORITHM: str = "sha256"

# FR49 — Single Tenant
TENANT_DEPLOY_POLL_INTERVAL_S: int = 10
TENANT_DEPLOY_TIMEOUT_S: int = 300


# ─────────────────────────────────────────────────────
# ENUMS
# ─────────────────────────────────────────────────────

class ModelTier(str, Enum):
    """FR27 §5: ModelRouter execution tiers."""
    LOCAL_REGEX_ONLY = "LOCAL_REGEX_ONLY"
    FAST_CLASSIFICATION = "FAST_CLASSIFICATION"
    HEAVY_REASONING = "HEAVY_REASONING"


class CrisisCheckResult(str, Enum):
    """FR27 Stage 1 / FR31: crisis scan outcome."""
    PASS = "PASS"
    FAIL = "FAIL"


class DormancyTier(int, Enum):
    """FR30 §3: 4-tier escalation path."""
    TIER_1 = 1  # Day 3
    TIER_2 = 2  # Day 5
    TIER_3 = 3  # Day 10
    TIER_4 = 4  # Day 30


class DormancyState(str, Enum):
    """FR30: user pipeline state."""
    ACTIVE = "ACTIVE"
    ACTIVE_MOMENTUM = "ACTIVE_MOMENTUM"
    RECOVERY_MODE_TIER_1 = "RECOVERY_MODE_TIER_1"
    RECOVERY_MODE_TIER_2 = "RECOVERY_MODE_TIER_2"
    RECOVERY_MODE_TIER_3 = "RECOVERY_MODE_TIER_3"
    RECOVERY_MODE_TIER_4 = "RECOVERY_MODE_TIER_4"
    CRISIS_HOLD = "CRISIS_HOLD"


class CapacityTrack(str, Enum):
    """FR32 §4.1: 5 Capacity Tracks."""
    RECOVERY = "Recovery"
    FOUNDATION = "Foundation"
    GROWTH = "Growth"
    MOMENTUM = "Momentum"
    PEAK = "Peak"


class RoadmapDayType(str, Enum):
    """FR32 §4.2: day types in the 4+1+2 template."""
    ACTIVE = "ACTIVE"
    REFLECTION = "REFLECTION"
    REST = "REST"


class WebinarPart(str, Enum):
    """FR33/FR34: 5-part webinar flow."""
    HOOK = "Hook"
    PROBLEM_EXPANSION = "Problem Expansion"
    PARADIGM_SHIFT = "Paradigm Shift"
    THE_METHOD = "The Method"
    THE_OFFER = "The Offer"


class InteractivePhase(str, Enum):
    """FR34 §5: interactive mode phases."""
    SOC_INTAKE = "SOC_INTAKE"
    WAITING_FOR_OUTLINE_APPROVAL = "WAITING_FOR_OUTLINE_APPROVAL"
    MODULE_ASSEMBLY = "MODULE_ASSEMBLY"
    WAITING_FOR_MODULE_APPROVAL = "WAITING_FOR_MODULE_APPROVAL"
    IMAGE_RECEIPT = "IMAGE_RECEIPT"
    COMPILATION = "COMPILATION"
    COMPLETE = "COMPLETE"


class ExcalidrawLayoutStrategy(str, Enum):
    """FR35 §4.1: canvas layout strategies."""
    HORIZONTAL_SLIDE_SEQUENCE = "HORIZONTAL_SLIDE_SEQUENCE"
    VERTICAL_SCROLLING = "VERTICAL_SCROLLING"


class PipelineType(str, Enum):
    """FR46 §4.2: pipeline enum for Asset ID."""
    CCF = "CCF"
    CBCS = "CBCS"
    V2WS = "V2WS"
    TIER = "TIER"


class FormatTag(str, Enum):
    """FR46 §4.2: format enum for Asset ID."""
    CAROUSEL = "CAROUSEL"
    REEL = "REEL"
    SCRIPT = "SCRIPT"
    DECK = "DECK"
    RITUAL = "RITUAL"
    AUDIO = "AUDIO"


class MoodState(str, Enum):
    """FR48 §4.1: mood enum for fingerprint."""
    PROCESSING = "P"
    ESCAPE = "E"
    DISCOVERY = "D"
    STATUS = "S"


class RegulatoryFrame(str, Enum):
    """FR48 §4.1: regulatory frame enum."""
    PROMOTION = "PRO"
    PREVENTION = "PRV"


class AudienceCohort(str, Enum):
    """FR48 §4.1: audience cohort enum."""
    NEW = "N"
    DEVELOPING = "DEV"
    LOYAL = "L"


class ReceiptStatus(str, Enum):
    """FR47 §4.2: receipt status codes."""
    SUCCESS = "SUCCESS"
    QUARANTINED = "QUARANTINED"
    CHAIN_BROKEN = "CHAIN_BROKEN"
    GENESIS = "GENESIS"


class TenantStatus(str, Enum):
    """FR49 §5: tenant deployment status."""
    PROVISIONING = "PROVISIONING"
    ACTIVE = "ACTIVE"
    FAILED = "FAILED"
    DECOMMISSIONED = "DECOMMISSIONED"


class SovereignImageResolution(str, Enum):
    """FR50 §5: sovereign image query result."""
    SUCCESS = "SUCCESS"
    NO_MATCH = "NO_MATCH"
    API_FAILURE = "API_FAILURE"


class SyllabusSection(str, Enum):
    """FR41 §4.3: syllabus sections."""
    GLOBAL_TAILWIND = "Global Tailwind"
    GLOBAL_HEADWIND = "Global Headwind"
    COHORT_MICRO_TRENDS = "Cohort Micro-Trends"


class AnalystTag(str, Enum):
    """FR43 §4.3: performance tag values."""
    HIGH = "HIGH"
    AVERAGE = "AVERAGE"
    UNDER = "UNDER"


class CRALPriority(str, Enum):
    """FR43 §5: CRAL moment priority levels."""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ArcWeightDirection(str, Enum):
    """FR43 §5: mode routing adjustment direction."""
    INCREASE = "INCREASE"
    DECREASE = "DECREASE"


# ─────────────────────────────────────────────────────
# FR27 MODELS — <2s Latency Protocol (DEP-PROTO-017)
# ─────────────────────────────────────────────────────

class ModelExecutionTier(BaseModel):
    """FR27 §5: single task tier configuration."""
    agent: str
    function: str
    model_tier: ModelTier
    max_output_tokens: int = Field(default=150, ge=1)
    max_latency_budget_ms: int = Field(ge=1)


class ModelTierMap(BaseModel):
    """FR27 §5: DEP-PROTO-017 model execution tier map."""
    tasks: list[ModelExecutionTier]
    fallback_model: ModelTier = ModelTier.FAST_CLASSIFICATION
    timeout_trigger_ms: int = GHOST_TYPING_TRIGGER_MS


class LatencyReceipt(BaseModel):
    """FR27: latency tracking receipt for a single pipeline run."""
    receipt_id: str = Field(default_factory=lambda: str(uuid4()))
    coach_id: str = Field(min_length=2, max_length=4)
    session_id: str
    stage_name: str
    agent_name: str
    latency_ms: int = Field(ge=0)
    crisis_check: CrisisCheckResult = CrisisCheckResult.PASS
    ghost_typing_triggered: bool = False
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


# ─────────────────────────────────────────────────────
# FR30 MODELS — Dormancy Recovery (DEP-ENG-025)
# ─────────────────────────────────────────────────────

class DormancyRecoveryPayload(BaseModel):
    """FR30 §5: DEP-ENG-025 output schema."""
    user_id: str
    coach_id: str = Field(min_length=2, max_length=4)
    trigger_timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    dormancy_tier: DormancyTier
    days_silent: int = Field(ge=0)
    recovery_context: DormancyRecoveryContext
    pipeline_state_update: DormancyStateUpdate


class DormancyRecoveryContext(BaseModel):
    """FR30 §5: contextual memory for recovery."""
    stalled_milestone: Optional[str] = None
    last_l3_fear: Optional[str] = None
    required_friction_level: str = "ultra_low_yes_no_question"


class DormancyStateUpdate(BaseModel):
    """FR30 §5: pipeline state change record."""
    previous_state: DormancyState
    new_state: DormancyState
    journaling_queue: str = "PAUSED"


# ─────────────────────────────────────────────────────
# FR31 MODELS — Crisis Guardian (DEP-ENG-026)
# ─────────────────────────────────────────────────────

class CrisisEscalationProtocol(BaseModel):
    """FR31 §5: DEP-ENG-026 output schema."""
    user_id: str
    coach_id: str = Field(min_length=2, max_length=4)
    detection_timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    scan_latency_ms: int = Field(ge=0)
    circuit_breaker: CrisisCircuitBreakerResult
    deployment: CrisisDeployment
    escalation: CrisisEscalation


class CrisisCircuitBreakerResult(BaseModel):
    """FR31 §5: circuit breaker detection details."""
    status: str = "TRIPPED"
    trigger_keyword: str
    exact_message_snippet: str = Field(max_length=500)


class CrisisDeployment(BaseModel):
    """FR31 §5: crisis deployment state."""
    automation_halted: bool = True
    user_state_locked: bool = True
    resources_dispatched: str


class CrisisEscalation(BaseModel):
    """FR31 §5: escalation routing details."""
    coach_notified: bool
    admin_channel_id: str


# ─────────────────────────────────────────────────────
# FR32 MODELS — Atlas Roadmap (DEP-ENG-027)
# ─────────────────────────────────────────────────────

class RoadmapDay(BaseModel):
    """FR32 §5: a single day in the 28-day roadmap."""
    day: int = Field(ge=1, le=28)
    week_number: int = Field(ge=1, le=4)
    type: RoadmapDayType
    assigned_intensity_load: float = Field(ge=0.0, le=2.0)
    ritual_category_selection: str = "NONE"


class AntiPatternLock(BaseModel):
    """FR32 §5: escalation lock metadata."""
    escalation_lock_expiry: str = "14_DAYS"
    track_locked_until: Optional[str] = None


class AtlasRoadmap(BaseModel):
    """FR32 §5: DEP-ENG-027 output — 30-day ritual roadmap."""
    user_id: str
    coach_id: str = Field(min_length=2, max_length=4)
    generation_date: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    capacity_track: CapacityTrack
    roadmap_architecture: list[RoadmapDay] = Field(min_length=28, max_length=28)
    milestone_checkpoints: list[int] = Field(default=MILESTONE_INDICES)
    anti_pattern_locks: AntiPatternLock = Field(default_factory=AntiPatternLock)

    @model_validator(mode="after")
    def validate_4_1_2_structure(self) -> "AtlasRoadmap":
        """FR32 AC2: enforce 4+1+2 matrix constraint."""
        for week_num in range(1, 5):
            week_days = [d for d in self.roadmap_architecture
                         if d.week_number == week_num]
            active = sum(1 for d in week_days if d.type == RoadmapDayType.ACTIVE)
            reflection = sum(1 for d in week_days if d.type == RoadmapDayType.REFLECTION)
            rest = sum(1 for d in week_days if d.type == RoadmapDayType.REST)
            if active != ACTIVE_DAYS_PER_WEEK:
                raise ValueError(
                    f"Week {week_num}: expected {ACTIVE_DAYS_PER_WEEK} ACTIVE days, got {active}"
                )
            if reflection != REFLECTION_DAYS_PER_WEEK:
                raise ValueError(
                    f"Week {week_num}: expected {REFLECTION_DAYS_PER_WEEK} REFLECTION days, got {reflection}"
                )
            if rest != REST_DAYS_PER_WEEK:
                raise ValueError(
                    f"Week {week_num}: expected {REST_DAYS_PER_WEEK} REST days, got {rest}"
                )
        return self

    @model_validator(mode="after")
    def validate_rest_intensity_zero(self) -> "AtlasRoadmap":
        """FR32 §4.3: REST days are hard-coded to intensity 0.00."""
        for d in self.roadmap_architecture:
            if d.type == RoadmapDayType.REST and d.assigned_intensity_load != 0.0:
                raise ValueError(
                    f"Day {d.day}: REST day must have intensity 0.00, got {d.assigned_intensity_load}"
                )
        return self


# ─────────────────────────────────────────────────────
# FR33 MODELS — V²WS YOLO Mode (DEP-ENG-028)
# ─────────────────────────────────────────────────────

class YoloIntake(BaseModel):
    """FR33 §4.1: the 5-variable intake vector."""
    actionable_lesson_thesis: str = Field(min_length=1)
    target_audience_segment: str = Field(min_length=1)
    final_offer_cta: str = Field(min_length=1)
    key_stories_array: list[str] = Field(min_length=1)
    tone_energy_constraint: str = Field(min_length=1)


class WebinarModuleScript(BaseModel):
    """FR33 §4.3: single module in the webinar."""
    part: WebinarPart
    slide_content: str
    speaker_script: str = Field(max_length=900)  # ~150 words
    visual_instructions: str = ""


class V2WSExcalidrawPayload(BaseModel):
    """FR33 §5: DEP-ENG-028 final output."""
    type: str = "excalidraw"
    version: int = 2
    source: str = "ccf_yolo_pipeline"
    elements: list[dict[str, Any]] = Field(default_factory=list)
    app_state: dict[str, Any] = Field(
        default_factory=lambda: {"viewBackgroundColor": "#fafafa"}
    )
    files: dict[str, Any] = Field(default_factory=dict)


# ─────────────────────────────────────────────────────
# FR34 MODELS — V²WS Interactive Mode (DEP-ENG-029)
# ─────────────────────────────────────────────────────

class InteractiveModuleState(BaseModel):
    """FR34 §5: single module in the interactive assembly."""
    index: int = Field(ge=1)
    title: str
    status: str = "PENDING"
    script_content: str = ""
    asset_base64: Optional[str] = None


class InteractiveV2WSState(BaseModel):
    """FR34 §5: DEP-ENG-029 interactive session state."""
    session_id: str = Field(default_factory=lambda: f"V2WS-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{str(uuid4())[:4].upper()}")
    coach_id: str = Field(min_length=2, max_length=4)
    current_phase: InteractivePhase = InteractivePhase.SOC_INTAKE
    active_module_index: int = Field(default=0, ge=0)
    outline_approved: bool = False
    modules: list[InteractiveModuleState] = Field(default_factory=list)
    excalidraw_payload_ready: bool = False


# ─────────────────────────────────────────────────────
# FR35 MODELS — Unified Excalidraw Pipeline (DEP-ENG-030)
# ─────────────────────────────────────────────────────

class SpatialLayoutEntry(BaseModel):
    """FR35 §4.1: coordinate mapping for a single element."""
    element_id: str = Field(default_factory=lambda: str(uuid4()))
    x: float
    y: float
    width: float
    height: float
    element_type: str  # "rectangle", "text", "image"
    group_id: str = ""
    stroke_color: str = "#111827"
    background_color: str = "#ffffff"


class UnifiedExcalidrawPayload(BaseModel):
    """FR35 §5: DEP-ENG-030 unified output."""
    type: str = "excalidraw"
    version: int = 2
    source: str = "ccp_benjamin_unified"
    elements: list[dict[str, Any]] = Field(default_factory=list)
    app_state: dict[str, Any] = Field(
        default_factory=lambda: {"viewBackgroundColor": "#ffffff"}
    )
    files: dict[str, Any] = Field(default_factory=dict)


# ─────────────────────────────────────────────────────
# FR36 MODELS — Transparent Collage (DEP-ENG-031)
# ─────────────────────────────────────────────────────

class VisualPromptObject(BaseModel):
    """FR36 §4.1: visual reasoning protocol output."""
    emotion: str = Field(min_length=1)
    pose: str = Field(min_length=1)
    prop: str = Field(min_length=1)
    t2i_prompt: str = ""


class TransparentCollageOutput(BaseModel):
    """FR36 §5: DEP-ENG-031 output — base64 transparent PNG."""
    asset_id: str
    base64_png: str = Field(min_length=1)
    transparency_failed: bool = False
    source_emotion: str = ""
    source_prop: str = ""


# ─────────────────────────────────────────────────────
# FR37 MODELS — Cross-System Intelligence (DEP-ENG-032)
# ─────────────────────────────────────────────────────

class PainPointFrequency(BaseModel):
    """FR37 §5: single pain point frequency entry."""
    theme: str
    frequency: int = Field(ge=0)


class SundayBotMeetingPayload(BaseModel):
    """FR37 §5: DEP-ENG-032 output schema."""
    routing_id: str = Field(
        default_factory=lambda: f"SBM-{datetime.now(timezone.utc).strftime('%Y')}-Week{datetime.now(timezone.utc).isocalendar()[1]:02d}"
    )
    coach_id: str = Field(min_length=2, max_length=4)
    period: dict[str, str] = Field(default_factory=dict)
    aggregation_metrics: SBMAggregationMetrics
    strategic_synthesis: SBMStrategicSynthesis
    pii_leak_status: str = "CLEAN"


class SBMAggregationMetrics(BaseModel):
    """FR37 §5: aggregation metrics section."""
    active_clients_analyzed: int = Field(ge=0)
    top_pain_points: list[PainPointFrequency] = Field(default_factory=list)
    top_coping_mechanisms: list[PainPointFrequency] = Field(default_factory=list)


class SBMStrategicSynthesis(BaseModel):
    """FR37 §5: strategic synthesis section."""
    recommended_meta_theme: str = Field(min_length=1)
    archetype_targeting_weight: str = ""


# ─────────────────────────────────────────────────────
# FR41 MODELS — Cross-Ecosystem Meeting (DEP-ENG-036)
# ─────────────────────────────────────────────────────

class SanitizedPerformanceBrief(BaseModel):
    """FR41 §4.1: anonymized performance brief per tenant."""
    tenant_id: str
    coach_id: str = Field(min_length=2, max_length=4)
    period_days: int = 30
    format_performance: dict[str, float] = Field(default_factory=dict)
    hook_performance: dict[str, float] = Field(default_factory=dict)
    structural_rhythm: dict[str, float] = Field(default_factory=dict)

    @field_validator("format_performance", "hook_performance", "structural_rhythm")
    @classmethod
    def no_string_values(cls, v: dict[str, float]) -> dict[str, float]:
        """FR41 AC1: zero-PII — only floats allowed."""
        for key, val in v.items():
            if not isinstance(val, (int, float)):
                raise ValueError(f"PII leak risk: value for '{key}' is not numeric")
        return v


class CrossPollinationSyllabus(BaseModel):
    """FR41 §5: DEP-ENG-036 output."""
    month: str
    total_ecosystems: int = Field(ge=0)
    total_output_analyzed: int = Field(ge=0)
    global_headwinds: list[str] = Field(default_factory=list)
    global_tailwinds: list[str] = Field(default_factory=list)
    cohort_micro_trends: list[str] = Field(default_factory=list)


# ─────────────────────────────────────────────────────
# FR42 MODELS — Publer Sync (DEP-ENG-037)
# ─────────────────────────────────────────────────────

class ContentPerformanceRow(BaseModel):
    """FR42 §5: DEP-ENG-037 content_performance table row."""
    universal_asset_id: str
    publer_post_id: str = ""
    platform: str = ""
    platform_post_url: str = ""
    published_at: Optional[str] = None
    reach: int = Field(default=0, ge=0)
    impressions: int = Field(default=0, ge=0)
    saves: int = Field(default=0, ge=0)
    shares: int = Field(default=0, ge=0)
    comments: int = Field(default=0, ge=0)
    likes: int = Field(default=0, ge=0)
    video_views: int = Field(default=0, ge=0)
    engagement_rate: float = Field(default=0.0, ge=0.0)
    first_insights_at: Optional[str] = None
    day_7_snapshot: Optional[dict[str, Any]] = None
    day_30_snapshot: Optional[dict[str, Any]] = None
    analyst_reviewed: bool = False

    @property
    def computed_engagement_rate(self) -> float:
        """FR42 AC2: (saves + shares + comments + likes) / reach."""
        if self.reach == 0:
            return 0.0
        return (self.saves + self.shares + self.comments + self.likes) / self.reach


# ─────────────────────────────────────────────────────
# FR43 MODELS — Data Analyst Agent (DEP-ENG-038)
# ─────────────────────────────────────────────────────

class ParameterUpdate(BaseModel):
    """FR43 §5: DEP-ENG-038 parameter_update.json."""
    coach_id: str
    evaluation_period: str
    arc_priority_weights: dict[str, float] = Field(default_factory=dict)
    cral_moment_priority: dict[str, CRALPriority] = Field(default_factory=dict)
    mode_routing_adjustments: dict[str, ArcWeightDirection] = Field(default_factory=dict)
    scheduling_updates: dict[str, dict[str, Any]] = Field(default_factory=dict)
    next_cycle_directive: str = ""
    timestamp_generated: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


# ─────────────────────────────────────────────────────
# FR45 MODELS — Notion Export Pipeline (DEP-ENG-039)
# ─────────────────────────────────────────────────────

class NotionPagePayload(BaseModel):
    """FR45 §5: DEP-ENG-039 notion page creation payload."""
    parent_database_id: str
    title: str
    universal_asset_id: str
    arc_type: str = ""
    status: str = "Draft"
    sections: list[NotionSection] = Field(default_factory=list)


class NotionSection(BaseModel):
    """FR45 §4.2: one of the 7 required sections."""
    section_name: str
    block_type: str  # "callout", "heading_2", "paragraph", "image", etc.
    content: str = ""
    url: str = ""


# ─────────────────────────────────────────────────────
# FR46 MODELS — Universal Asset & Person ID (DEP-ENG-040)
# ─────────────────────────────────────────────────────

class PersonID(BaseModel):
    """FR46 §4.1: person ID."""
    person_id: str  # PID-{COACH}-{SEQ}
    coach_acronym: str = Field(min_length=2, max_length=4)
    sequence: str = Field(min_length=4, max_length=4)
    is_coach: bool = False


class UniversalAssetID(BaseModel):
    """FR46 §4.2: asset ID."""
    asset_id: str  # {COACH}-{PIPELINE}-{DATE}-{SEQ}-{FORMAT}
    coach_acronym: str = Field(min_length=2, max_length=4)
    pipeline: PipelineType
    date_str: str  # YYYYMMDD
    sequence: str
    format_tag: FormatTag


class IDGenerationPayload(BaseModel):
    """FR46 §5: DEP-ENG-040 output."""
    transaction_timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    coach_id: str
    assigned_person_id: Optional[str] = None
    assigned_asset_id: Optional[str] = None
    id_metadata: dict[str, str] = Field(default_factory=dict)


# ─────────────────────────────────────────────────────
# FR47 MODELS — Receipt Chain Guard (DEP-ENG-041)
# ─────────────────────────────────────────────────────

class ReceiptBlock(BaseModel):
    """FR47 §5: DEP-ENG-041 canonical receipt block."""
    receipt_id: str = Field(default_factory=lambda: str(uuid4()))
    asset_id: str = ""
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    executing_agent: str
    pi_extensions_triggered: list[str] = Field(default_factory=list)
    mode: str = "EXECUTION"
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)
    input_payload_hash: str = ""
    output_payload_hash: str = ""
    previous_receipt_hash: str = RECEIPT_GENESIS_MARKER
    current_receipt_hash: str = ""
    status_code: ReceiptStatus = ReceiptStatus.SUCCESS

    def compute_hash(self) -> str:
        """FR47 §3: SHA-256 deterministic hash."""
        payload = json.dumps({
            "receipt_id": self.receipt_id,
            "asset_id": self.asset_id,
            "timestamp": self.timestamp,
            "executing_agent": self.executing_agent,
            "input_payload_hash": self.input_payload_hash,
            "output_payload_hash": self.output_payload_hash,
            "previous_receipt_hash": self.previous_receipt_hash,
        }, sort_keys=True)
        return hashlib.sha256(payload.encode()).hexdigest()


# ─────────────────────────────────────────────────────
# FR48 MODELS — Forensic Audit Protocol (DEP-ENG-042)
# ─────────────────────────────────────────────────────

class SkillFingerprintID(BaseModel):
    """FR48 §4.1: skill fingerprint registration."""
    skill_id: str  # SKILL-{ARCH}-{COACH}-{MOOD}-{FRAME}-{COHORT}-{DATE}-{SEQ}
    archetype_template_id: str
    archetype_template_version: str = "1.0"
    compilation_date: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    maturity: str = "draft"
    assembly_status: str = "COMPLETE"
    context: SkillContext
    dep_snapshot: dict[str, str] = Field(default_factory=dict)
    outputs: list[str] = Field(default_factory=list)
    promoted_to_stable: bool = False


class SkillContext(BaseModel):
    """FR48 §5: compilation context parameters."""
    coach_id: str
    mood_state: MoodState
    regulatory_frame: RegulatoryFrame
    audience_cohort: AudienceCohort
    tmt_function: str = ""
    sdt_need_primary: str = ""


class ForensicLineage(BaseModel):
    """FR48 §4.3: forensic reconstruction output."""
    asset_id: str
    skill_fingerprint_id: str
    context: SkillContext
    agent_sequence: list[str] = Field(default_factory=list)
    receipt_chain: list[ReceiptBlock] = Field(default_factory=list)
    cral_override: bool = False
    cral_rationale: str = ""


# ─────────────────────────────────────────────────────
# FR49 MODELS — Single-Tenant Deployment (DEP-ENG-043)
# ─────────────────────────────────────────────────────

class DeploymentManifest(BaseModel):
    """FR49 §4.1: deployment manifest."""
    coach_name: str = Field(min_length=1)
    coach_acronym: str = Field(min_length=2, max_length=4)
    admin_email: str = Field(min_length=1)
    region: str = "us-east-1"
    generated_password: str = Field(default_factory=lambda: str(uuid4()))


class TenantRegistryRow(BaseModel):
    """FR49 §5: DEP-ENG-043 tenant_registry record."""
    tenant_id: str = Field(default_factory=lambda: str(uuid4()))
    coach_name: str
    coach_acronym: str = Field(min_length=2, max_length=4)
    deployment_date: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    status: TenantStatus = TenantStatus.PROVISIONING
    infrastructure: TenantInfrastructure = Field(
        default_factory=lambda: TenantInfrastructure()
    )


class TenantInfrastructure(BaseModel):
    """FR49 §5: infrastructure connection details."""
    supabase_project_ref: str = ""
    supabase_rest_url: str = ""
    supabase_service_role_key: str = ""
    neo4j_uri: str = ""
    neo4j_username: str = "neo4j"
    neo4j_password_vault_id: str = ""


# ─────────────────────────────────────────────────────
# FR50 MODELS — Sovereign Image Rule (DEP-ENG-044)
# ─────────────────────────────────────────────────────

class SovereignImageQuery(BaseModel):
    """FR50 §4.1: sovereign image query parameters."""
    coach_id: str = Field(min_length=2, max_length=4)
    target_mood: str
    target_format: str = "Square_1080"


class SovereignImageResult(BaseModel):
    """FR50 §5: DEP-ENG-044 output schema."""
    asset_id: str
    resolution_status: SovereignImageResolution
    search_parameters: SovereignImageQuery
    selected_photo: Optional[SelectedPhoto] = None
    ai_generation_request: Optional[str] = None


class SelectedPhoto(BaseModel):
    """FR50 §5: selected photo details."""
    notion_page_id: str
    temporary_s3_url: str
    usage_count_updated_to: int = Field(ge=0)
    last_used: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d")
    )


# ─────────────────────────────────────────────────────
# Rebuild forward references for models that reference
# classes defined after them
# ─────────────────────────────────────────────────────

DormancyRecoveryPayload.model_rebuild()
CrisisEscalationProtocol.model_rebuild()
SundayBotMeetingPayload.model_rebuild()
SovereignImageResult.model_rebuild()
