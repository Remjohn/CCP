"""
FR-ERA3-34 Phase-0 Prospect Workspace and Artifact Store Models
================================================================
Canonical schemas for the shared Phase-0 workspace runtime.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Optional
import uuid

from pydantic import BaseModel, Field, field_validator


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class Phase0WorkspaceStatus(str, Enum):
    CREATED = "created"
    INTAKE_RECEIVED = "intake_received"
    ARTIFACTS_COLLECTING = "artifacts_collecting"
    AUDIT_IN_PROGRESS = "audit_in_progress"
    PREVIEW_READY = "preview_ready"
    DELIVERED = "delivered"
    PAYMENT_UNLOCKED = "payment_unlocked"
    UPGRADED = "upgraded"
    ARCHIVED = "archived"
    BLOCKED = "blocked"


class Phase0ArtifactStatus(str, Enum):
    UPLOADED = "uploaded"
    NORMALIZED = "normalized"
    AUDIT_READY = "audit_ready"
    PREVIEW_READY = "preview_ready"
    DELIVERED = "delivered"
    PAYMENT_UNLOCKED = "payment_unlocked"
    UPGRADED = "upgraded"
    QUARANTINED = "quarantined"
    REJECTED = "rejected"


class Phase0ArtifactFamily(str, Enum):
    INTAKE_SOURCE = "intake_source"
    NORMALIZED_SOURCE = "normalized_source"
    AUDIT_REPORT = "audit_report"
    PREVIEW_ASSET = "preview_asset"
    PRODUCED_PROOF = "produced_proof"
    PAYMENT_BRIDGE = "payment_bridge"
    UPGRADE_METADATA = "upgrade_metadata"


class Phase0DeliveryWindowStatus(str, Enum):
    NOT_STARTED = "not_started"
    ON_TRACK = "on_track"
    AT_RISK = "at_risk"
    BREACHED = "breached"
    DELIVERED = "delivered"


class Phase0WorkspaceRecord(BaseModel):
    workspace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    prospect_id: str = Field(..., min_length=1)
    prospect_packet_id: str = Field(..., min_length=1)
    coach_id: Optional[str] = Field(default=None)
    display_name: str = Field(..., min_length=1, max_length=200)
    status: Phase0WorkspaceStatus = Field(default=Phase0WorkspaceStatus.CREATED)
    artifact_count: int = Field(default=0, ge=0)
    campaign_id: Optional[str] = Field(default=None)
    delivery_sla_deadline_utc: Optional[str] = Field(default=None)
    created_at: str = Field(default_factory=utc_now_iso)
    updated_at: str = Field(default_factory=utc_now_iso)
    created_by_receipt_id: str = Field(..., min_length=1)
    last_transition_receipt_id: Optional[str] = Field(default=None)


class Phase0ArtifactRecord(BaseModel):
    artifact_id: str = Field(..., min_length=1)
    workspace_id: str = Field(..., min_length=1)
    prospect_id: str = Field(..., min_length=1)
    family: Phase0ArtifactFamily = Field(...)
    status: Phase0ArtifactStatus = Field(default=Phase0ArtifactStatus.UPLOADED)
    display_label: str = Field(..., min_length=1, max_length=300)
    mime_type: Optional[str] = Field(default=None)
    file_size_bytes: Optional[int] = Field(default=None, ge=0)
    storage_uri: Optional[str] = Field(default=None)
    checksum_sha256: Optional[str] = Field(default=None)
    parent_artifact_ids: list[str] = Field(default_factory=list)
    source_receipt_id: str = Field(..., min_length=1)
    metadata: dict[str, str] = Field(default_factory=dict)
    created_at: str = Field(default_factory=utc_now_iso)
    updated_at: str = Field(default_factory=utc_now_iso)
    transitioned_at: Optional[str] = Field(default=None)
    transition_receipt_id: Optional[str] = Field(default=None)

    @field_validator("metadata", mode="before")
    @classmethod
    def ensure_metadata_values_strings(cls, value: object) -> dict[str, str]:
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise TypeError("metadata must be a dictionary")
        return {str(k): str(v) for k, v in value.items()}


class Phase0ArtifactManifest(BaseModel):
    manifest_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    workspace_id: str = Field(..., min_length=1)
    prospect_id: str = Field(..., min_length=1)
    assembled_at: str = Field(default_factory=utc_now_iso)
    assembly_receipt_id: str = Field(..., min_length=1)
    intake_sources: list[str] = Field(default_factory=list)
    normalized_sources: list[str] = Field(default_factory=list)
    audit_reports: list[str] = Field(default_factory=list)
    preview_assets: list[str] = Field(default_factory=list)
    produced_proofs: list[str] = Field(default_factory=list)
    payment_bridges: list[str] = Field(default_factory=list)
    upgrade_metadata_refs: list[str] = Field(default_factory=list)
    total_artifact_count: int = Field(..., ge=0)
    completeness_summary: dict[str, str] = Field(default_factory=dict)
    is_delivery_ready: bool = Field(default=False)
    is_payment_bridge_ready: bool = Field(default=False)


class Phase0ReadinessState(BaseModel):
    workspace_id: str = Field(..., min_length=1)
    prospect_id: str = Field(..., min_length=1)
    workspace_status: Phase0WorkspaceStatus = Field(...)
    delivery_window_status: Phase0DeliveryWindowStatus = Field(...)
    sla_deadline_utc: Optional[str] = Field(default=None)
    hours_remaining: Optional[float] = Field(default=None, ge=0.0)
    blocking_families: list[str] = Field(default_factory=list)
    warning_families: list[str] = Field(default_factory=list)
    quarantined_artifact_ids: list[str] = Field(default_factory=list)
    rejected_artifact_ids: list[str] = Field(default_factory=list)
    human_review_required: bool = Field(default=False)
    readiness_summary: str = Field(default="")
    computed_at: str = Field(default_factory=utc_now_iso)
    computation_receipt_id: str = Field(..., min_length=1)


class Phase0UpgradeBridgeState(BaseModel):
    bridge_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    workspace_id: str = Field(..., min_length=1)
    prospect_id: str = Field(..., min_length=1)
    target_tier: str = Field(..., min_length=1)
    payment_confirmed: bool = Field(default=False)
    payment_receipt_id: Optional[str] = Field(default=None)
    payment_amount_cents: Optional[int] = Field(default=None, ge=0)
    credit_applied_cents: Optional[int] = Field(default=None, ge=0)
    migration_status: str = Field(default="pending")
    target_coach_acronym: Optional[str] = Field(default=None, min_length=3, max_length=3)
    migration_receipt_id: Optional[str] = Field(default=None)
    initiated_at: str = Field(default_factory=utc_now_iso)
    confirmed_at: Optional[str] = Field(default=None)
    completed_at: Optional[str] = Field(default=None)
    abort_reason: Optional[str] = Field(default=None)


class Phase0MigrationResult(BaseModel):
    workspace_id: str = Field(..., min_length=1)
    prospect_id: str = Field(..., min_length=1)
    target_coach_acronym: str = Field(..., min_length=3, max_length=3)
    scaffold_path: str = Field(..., min_length=1)
    migrated_artifact_count: int = Field(..., ge=0)
    remapped_asset_ids: dict[str, str] = Field(default_factory=dict)
    archived_workspace_status: Phase0WorkspaceStatus = Field(...)
    migration_receipt_id: str = Field(..., min_length=1)
