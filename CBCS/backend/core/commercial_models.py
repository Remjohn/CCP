"""
Commercial Intelligence Layer — Shared Models
FR-COM-01 through FR-COM-04

Shared Pydantic models, enums, constants, and error types for the
entire Commercial Intelligence Layer (Phase 5).
"""

from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


# =====================================================
#  FR-COM-01: Billing & Credit System
# =====================================================

class SubscriptionTier(str, Enum):
    FREE_TRIAL = "free_trial"
    BASE = "base"
    PREMIUM = "premium"
    CONCIERGE = "concierge"


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELLED = "cancelled"
    TRIALING = "trialing"
    PAUSED = "paused"


class BillingEventType(str, Enum):
    CBCS_CREDIT = "cbcs_credit"
    SUBSCRIPTION_PAYMENT = "subscription_payment"
    PAYMENT_FAILED = "payment_failed"
    GRACE_DISPATCH = "grace_dispatch"
    USAGE_REPORTED = "usage_reported"
    REACTIVATION = "reactivation"


class BillingQueueStatus(str, Enum):
    PENDING = "pending"
    BILLED = "billed"
    FAILED = "failed"
    GRACE_DISPATCHED = "grace_dispatched"


class JailAction(str, Enum):
    INSTANT_USAGE_LOCK = "instant_usage_lock"
    GRACE_PERIOD_MUTE = "grace_period_mute"
    WATERMARK_ENFORCEMENT = "watermark_enforcement"
    REACTIVATION = "reactivation"


class BillingError(Exception):
    """Raised when a billing gate blocks an action."""

    def __init__(self, code: str, message: str, redirect: str = "/wallet"):
        self.code = code
        self.message = message
        self.redirect = redirect
        super().__init__(f"[{code}] {message}")


class BillingGateResult(BaseModel):
    """Result of a require_credits() middleware check."""
    allowed: bool
    coach_id: str
    action: str
    cost_cents: int = 0
    status: SubscriptionStatus
    receipt_id: Optional[str] = None
    grace_dispatch: bool = False


class CoachSubscriptionRow(BaseModel):
    """Mirrors coach_subscriptions table row."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    coach_id: str
    stripe_customer_id: str
    stripe_subscription_id: str
    stripe_metered_item_id: Optional[str] = None
    tier: SubscriptionTier = SubscriptionTier.BASE
    weekly_base_price_cents: int = 2500
    cbcs_unit_price_cents: int = 400
    status: SubscriptionStatus = SubscriptionStatus.ACTIVE
    payment_method_last4: Optional[str] = None
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    active_client_count: int = 0
    total_weekly_cost_cents: int = 2500
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class BillingEventRow(BaseModel):
    """Mirrors billing_events table row."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    coach_id: str
    event_type: BillingEventType
    stripe_event_id: Optional[str] = None
    amount_cents: Optional[int] = None
    client_id: Optional[str] = None
    description: Optional[str] = None
    receipt_chain_block: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class BillingQueueRow(BaseModel):
    """Mirrors billing_queue table row (CBAR Q5)."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    coach_id: str
    client_telegram_user_id: int
    program_id: Optional[str] = None
    idempotency_key: str
    scheduled_dispatch_at: datetime
    status: BillingQueueStatus = BillingQueueStatus.PENDING
    stripe_usage_record_id: Optional[str] = None
    retry_count: int = 0
    billed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class WalletDisplayData(BaseModel):
    """Data for AFFiNE Wallet Block rendering."""
    coach_id: str
    tier: SubscriptionTier
    weekly_base_cost_cents: int
    active_client_count: int
    cbcs_unit_cents: int = 400
    total_weekly_cost_cents: int
    payment_status: SubscriptionStatus
    payment_method_last4: Optional[str] = None
    alert_message: Optional[str] = None


# =====================================================
#  FR-COM-02: Global Admin Dashboard
# =====================================================

class AdminActionType(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"
    REGENERATE = "regenerate"
    PAUSE_PIPELINE = "pause_pipeline"
    RESUME_PIPELINE = "resume_pipeline"
    RETRY_FAILED = "retry_failed"
    SEND_NUDGE = "send_nudge"
    SEND_PAYMENT_REMINDER = "send_payment_reminder"
    CAPACITY_OVERRIDE = "capacity_override"  # CBAR Q7


class AdminActionRow(BaseModel):
    """Mirrors admin_actions table row."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    admin_user_id: str
    action_type: AdminActionType
    target_coach_id: Optional[str] = None
    target_content_id: Optional[str] = None
    notes: Optional[str] = None
    receipt_chain_block: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PipelineHealthSnapshotRow(BaseModel):
    """Mirrors pipeline_health_snapshots table row."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    snapshot_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    active_renders: int = 0
    failed_24h: int = 0
    failed_by_type: Optional[dict[str, int]] = None
    avg_render_time_seconds: Optional[float] = None
    gpu_utilization_pct: Optional[float] = None
    total_active_coaches: int = 0
    total_pending_review: int = 0
    total_cbcs_users_week: int = 0
    revenue_week_cents: int = 0
    aws_cost_week_cents: int = 0
    margin_pct: Optional[float] = None


class FactoryFloorItem(BaseModel):
    """A single item in the Factory Floor review queue."""
    content_id: str
    coach_id: str
    coach_name: str
    program_name: Optional[str] = None
    content_type: str
    status: str
    generation_timestamp: datetime
    pipeline_stage: str
    lora_version_id: Optional[str] = None  # CBAR Q6 — LoRA Version Lock


class LoRAVersionCheckResult(BaseModel):
    """Result of CBAR Q6 LoRA Version Lock check."""
    match: bool
    asset_lora_version: Optional[str] = None
    current_lora_version: Optional[str] = None
    action_required: Optional[str] = None  # "stale_approve" | "re_render" | None


class TreasuryMetrics(BaseModel):
    """Aggregated Treasury view data."""
    total_active_coaches: int = 0
    coaches_by_tier: dict[str, int] = Field(default_factory=dict)
    cbcs_users_this_week: int = 0
    revenue_subscriptions_cents: int = 0
    revenue_cbcs_cents: int = 0
    revenue_total_cents: int = 0
    aws_cost_cents: int = 0
    margin_pct: float = 0.0
    failed_payments: list[dict[str, Any]] = Field(default_factory=list)


# =====================================================
#  FR-COM-03: Telegram Code Onboarding Agent
# =====================================================

class OnboardingEventType(str, Enum):
    CODE_ENTERED = "code_entered"
    CODE_VALID = "code_valid"
    CODE_INVALID = "code_invalid"
    CODE_EXPIRED = "code_expired"
    PROGRAM_FULL = "program_full"
    INTAKE_STARTED = "intake_started"
    INTAKE_COMPLETED = "intake_completed"
    PROVISIONING_STARTED = "provisioning_started"
    PROVISIONING_COMPLETED = "provisioning_completed"
    PROVISIONING_FAILED = "provisioning_failed"
    DUPLICATE_BLOCKED = "duplicate_blocked"


class ClientProfileStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    DROPPED = "dropped"
    BILLING_MUTED = "billing_muted"


class OnboardingError(Exception):
    """Raised during onboarding flow errors."""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")


class OnboardingEventRow(BaseModel):
    """Mirrors onboarding_events table row."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    telegram_user_id: int
    event_type: OnboardingEventType
    program_code: Optional[str] = None
    coach_id: Optional[str] = None
    program_id: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ClientProfileExtension(BaseModel):
    """Extension columns added to profiles table via ALTER TABLE."""
    program_id: Optional[str] = None
    telegram_user_id: Optional[int] = None
    primary_goal: Optional[str] = None
    intake_data: Optional[dict[str, Any]] = None
    enrollment_code: Optional[str] = None
    status: ClientProfileStatus = ClientProfileStatus.ACTIVE
    first_message_sent: bool = False
    first_message_sent_at: Optional[datetime] = None
    billing_reported: bool = False
    enrolled_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    receipt_chain_block: Optional[str] = None


class IntakeSession(BaseModel):
    """Tracks conversational intake state machine."""
    telegram_user_id: int
    coach_id: str
    program_id: str
    program_code: str
    intake_fields: list[str] = Field(default_factory=lambda: ["first_name", "primary_goal"])
    current_field_index: int = 0
    collected_data: dict[str, str] = Field(default_factory=dict)
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def is_complete(self) -> bool:
        return self.current_field_index >= len(self.intake_fields)

    @property
    def current_field(self) -> Optional[str]:
        if self.current_field_index < len(self.intake_fields):
            return self.intake_fields[self.current_field_index]
        return None


class ProvisioningResult(BaseModel):
    """Result of the atomic auto-provisioning sequence."""
    success: bool
    profile_id: Optional[str] = None
    billing_reported: bool = False
    affine_pushed: bool = False
    checkin_scheduled: bool = False
    coach_notified: bool = False
    receipt_id: Optional[str] = None
    error: Optional[str] = None


# =====================================================
#  FR-COM-04: Program & Campaign Manager
# =====================================================

class ProgramStatus(str, Enum):
    DRAFT = "draft"
    ENROLLING = "enrolling"
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class CampaignStatus(str, Enum):
    DRAFT = "draft"
    LIVE = "live"
    PAUSED = "paused"
    ENDED = "ended"


class AnalyticsEventType(str, Enum):
    """CBAR Q9 — Event types for funnel analytics."""
    FUNNEL_VIEW = "funnel_view"
    TELEGRAM_CLICK = "telegram_click"
    ENROLLMENT_COMPLETE = "enrollment_complete"


class ProgramRegistryError(Exception):
    """Raised during program registry operations."""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")


class CoachingProgramRow(BaseModel):
    """Mirrors coaching_programs table row."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    coach_id: str
    program_name: str
    description: Optional[str] = None
    duration_days: int
    check_in_schedule: list[str]
    max_clients: int = 30
    current_enrolled: int = 0
    client_price_display: Optional[str] = None
    enrollment_code: str
    intake_fields: list[str] = Field(default_factory=lambda: ["first_name", "primary_goal"])
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: ProgramStatus = ProgramStatus.ENROLLING
    receipt_chain_block: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def available_capacity(self) -> int:
        return max(0, self.max_clients - self.current_enrolled)


class CampaignRow(BaseModel):
    """Mirrors campaigns table row."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    coach_id: str
    program_id: str
    campaign_name: str
    enrollment_code_override: Optional[str] = None
    funnel_url: Optional[str] = None
    funnel_s3_path: Optional[str] = None
    telegram_bot_link: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    total_enrollments: int = 0
    total_funnel_views: int = 0
    conversion_rate: Optional[float] = None
    status: CampaignStatus = CampaignStatus.DRAFT
    receipt_chain_block: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ProgramValidationResponse(BaseModel):
    """Response from POST /api/programs/validate-code."""
    valid: bool
    reason: Optional[str] = None  # CODE_NOT_FOUND, PROGRAM_FULL, PROGRAM_EXPIRED, CAMPAIGN_PAUSED
    coach_id: Optional[str] = None
    program_id: Optional[str] = None
    program_name: Optional[str] = None
    available_capacity: Optional[int] = None
    intake_fields: Optional[list[str]] = None
    check_in_schedule: Optional[list[str]] = None
    status: Optional[str] = None


class AnalyticsEventRow(BaseModel):
    """Mirrors analytics_events table row (CBAR Q9)."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: AnalyticsEventType
    campaign_id: str
    coach_id: str
    signed_token_hash: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# =====================================================
#  Receipt Chain Guard — shared utility
# =====================================================

RECEIPT_STAGE_BILLING_GATE = "BILLING_GATE"
RECEIPT_STAGE_WEBHOOK_SYNC = "WEBHOOK_SYNC"
RECEIPT_STAGE_USAGE_REPORT = "USAGE_REPORT"
RECEIPT_STAGE_JAIL_ACTION = "JAIL_ACTION"
RECEIPT_STAGE_ADMIN_ACTION = "ADMIN_ACTION"
RECEIPT_STAGE_HEALTH_SNAPSHOT = "HEALTH_SNAPSHOT"
RECEIPT_STAGE_CODE_VALIDATE = "CODE_VALIDATE"
RECEIPT_STAGE_INTAKE_COMPLETE = "INTAKE_COMPLETE"
RECEIPT_STAGE_PROVISIONING = "PROVISIONING"
RECEIPT_STAGE_FIRST_MESSAGE = "FIRST_MESSAGE"
RECEIPT_STAGE_PROGRAM_CREATE = "PROGRAM_CREATE"
RECEIPT_STAGE_CAMPAIGN_LAUNCH = "CAMPAIGN_LAUNCH"
RECEIPT_STAGE_FUNNEL_DEPLOY = "FUNNEL_DEPLOY"
RECEIPT_STAGE_CAPACITY_OVERRIDE = "CAPACITY_OVERRIDE"

# CBAR Q5 Constants
BILLING_QUEUE_PREFLIGHT_MINUTES = 30
BILLING_QUEUE_WORKER_RATE_PER_SEC = 80
BILLING_QUEUE_RETRY_MINUTES = 5
BILLING_QUEUE_MAX_ESCALATION_MINUTES = 30
BILLING_QUEUE_MAX_RETRIES = 6  # 30min / 5min

# CBAR Q4 Constants
GRACE_WINDOW_DEADLINE_HOURS = 24

# FR-COM-04 Code generation
ENROLLMENT_CODE_LENGTH = 8

# FR-COM-02 Health snapshot interval
HEALTH_SNAPSHOT_INTERVAL_MINUTES = 15

# FR-COM-02 Treasury alerts
TREASURY_AWS_COST_WARNING_PCT = 40.0
TREASURY_PAYMENT_FAILURE_ESCALATION_HOURS = 48
TREASURY_CBCS_CHURN_WEEKLY_THRESHOLD = 5


def compute_receipt_hash(payload: dict) -> str:
    """Compute SHA-256 hash for Receipt Chain Guard per DEP-ENG-041."""
    canonical = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def build_receipt(
    stage_name: str,
    agent_name: str,
    input_payload: dict,
    output_payload: dict,
    previous_receipt_hash: str = "",
) -> dict:
    """Build a Receipt Chain Guard entry per FR47 DEP-ENG-041 schema."""
    receipt_id = str(uuid.uuid4())
    return {
        "receipt_id": receipt_id,
        "previous_receipt_hash": previous_receipt_hash,
        "input_payload_hash": compute_receipt_hash(input_payload),
        "output_payload_hash": compute_receipt_hash(output_payload),
        "stage_name": stage_name,
        "agent_name": agent_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
