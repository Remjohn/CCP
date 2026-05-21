"""
FR-ERA3-38 Phase-0 Operator Console and SLA Tracker Models
==========================================================
Canonical Pydantic v2 models and enums for Phase-0 Operator Console operations.
"""

from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, field_validator


class Phase0TopLevelState(str, Enum):
    """Canonical operator-facing states for Phase-0 packages."""
    NEW_INTAKE = "NEW_INTAKE"
    BLOCKED_MISSING_INPUTS = "BLOCKED_MISSING_INPUTS"
    AUDIT_IN_PROGRESS = "AUDIT_IN_PROGRESS"
    ASSETS_RENDERING = "ASSETS_RENDERING"
    READY_TO_DELIVER = "READY_TO_DELIVER"
    DELIVERED_AWAITING_PAYMENT = "DELIVERED_AWAITING_PAYMENT"
    PAID_UNLOCKED = "PAID_UNLOCKED"
    UPGRADED_HANDED_OFF = "UPGRADED_HANDED_OFF"
    FAILED = "FAILED"


class Phase0AlertSeverity(str, Enum):
    """Severity levels for operator-facing alerts."""
    INFO = "INFO"
    WARNING = "WARNING"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Phase0EscalationLevel(str, Enum):
    """Operational escalation levels for troubleshooting."""
    NONE = "NONE"
    OPERATOR_REVIEW = "OPERATOR_REVIEW"
    SAME_DAY_RECOVERY = "SAME_DAY_RECOVERY"
    MANAGER_ATTENTION = "MANAGER_ATTENTION"
    MANUAL_OVERRIDE_REQUIRED = "MANUAL_OVERRIDE_REQUIRED"


class Phase0RunStatus(BaseModel):
    """Unified run tracking for aggregation from downstream states."""
    coach_id: str = Field(..., min_length=1)
    phase0_packet_id: str = Field(..., min_length=1)
    delivery_run_id: Optional[str] = Field(default=None)
    top_level_state: Phase0TopLevelState
    intake_ready: bool
    audit_ready: bool
    render_ready: bool
    review_required: bool
    delivered: bool
    payment_completed: bool
    unlock_propagated: bool
    upgraded_target_tier: Optional[Literal["SPEAKING_LEARNING", "COACH_OS"]] = Field(default=None)
    updated_at_utc: datetime = Field(default_factory=datetime.utcnow)


class Phase0SlaState(BaseModel):
    """SLA timer tracking against 24-hour targets."""
    coach_id: str = Field(..., min_length=1)
    phase0_packet_id: str = Field(..., min_length=1)
    sla_started_at_utc: datetime
    sla_deadline_utc: datetime
    minutes_remaining: int
    risk_band: Literal["GREEN", "YELLOW", "ORANGE", "RED", "BREACHED"]
    breached: bool = Field(default=False)
    based_on_run_id: Optional[str] = Field(default=None)
    updated_at_utc: datetime = Field(default_factory=datetime.utcnow)


class Phase0Alert(BaseModel):
    """Actionable alert item requiring operator review or automatic resolution."""
    alert_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    phase0_packet_id: str = Field(..., min_length=1)
    severity: Phase0AlertSeverity
    alert_type: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    summary: str = Field(..., min_length=1)
    recommended_action: str = Field(..., min_length=1)
    source_state_ref: str = Field(..., min_length=1)
    created_at_utc: datetime = Field(default_factory=datetime.utcnow)
    acknowledged_at_utc: Optional[datetime] = Field(default=None)


class Phase0MissingInputState(BaseModel):
    """First-class representation of missing inputs blocking intake or delivery."""
    coach_id: str = Field(..., min_length=1)
    phase0_packet_id: str = Field(..., min_length=1)
    missing_fields: List[str] = Field(default_factory=list)
    blocking: bool = Field(default=True)
    last_request_sent_at_utc: Optional[datetime] = Field(default=None)
    operator_note: Optional[str] = Field(default=None)
    updated_at_utc: datetime = Field(default_factory=datetime.utcnow)


class Phase0EscalationState(BaseModel):
    """Typed manual or programmatic operational escalations."""
    escalation_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    phase0_packet_id: str = Field(..., min_length=1)
    escalation_level: Phase0EscalationLevel = Field(default=Phase0EscalationLevel.NONE)
    escalation_reason: str = Field(..., min_length=1)
    linked_alert_ids: List[str] = Field(default_factory=list)
    active: bool = Field(default=True)
    created_at_utc: datetime = Field(default_factory=datetime.utcnow)
    resolved_at_utc: Optional[datetime] = Field(default=None)


class Phase0OperatorQueueItem(BaseModel):
    """Consolidated representation of a package row in the console queue."""
    coach_id: str = Field(..., min_length=1)
    phase0_packet_id: str = Field(..., min_length=1)
    display_name: str = Field(..., min_length=1)
    run_status: Phase0RunStatus
    sla_state: Phase0SlaState
    active_alert_count: int = Field(default=0, ge=0)
    highest_alert_severity: Optional[Phase0AlertSeverity] = Field(default=None)
    next_action: str = Field(..., min_length=1)
    payment_state_label: str = Field(..., min_length=1)
    upgrade_state_label: str = Field(..., min_length=1)


class Phase0OperatorQueueView(BaseModel):
    """Full-feed view representation for console monitoring and batch sweeps."""
    workspace_id: str = Field(..., min_length=1)
    generated_at_utc: datetime = Field(default_factory=datetime.utcnow)
    total_active_packages: int = Field(default=0, ge=0)
    green_count: int = Field(default=0, ge=0)
    yellow_count: int = Field(default=0, ge=0)
    orange_count: int = Field(default=0, ge=0)
    red_count: int = Field(default=0, ge=0)
    breached_count: int = Field(default=0, ge=0)
    items: List[Phase0OperatorQueueItem] = Field(default_factory=list)


class Phase0PackageDetailView(BaseModel):
    """Detailed trace view of a single package execution."""
    coach_id: str = Field(..., min_length=1)
    phase0_packet_id: str = Field(..., min_length=1)
    run_status: Phase0RunStatus
    sla_state: Phase0SlaState
    missing_input_state: Optional[Phase0MissingInputState] = Field(default=None)
    escalation_state: Optional[Phase0EscalationState] = Field(default=None)
    alerts: List[Phase0Alert] = Field(default_factory=list)
    receipt_ids: List[str] = Field(default_factory=list)
    primary_review_action: Optional[str] = Field(default=None)
