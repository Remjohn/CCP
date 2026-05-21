"""
FR-ERA3-34 Phase-0 Workspace API Router
=======================================
Shared workspace and artifact-store endpoints.
"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Body, HTTPException, Path
from pydantic import BaseModel, Field

from src.ccp.models.phase0_intake_models import Phase0ProspectPacket
from src.ccp.models.phase0_workspace_models import (
    Phase0ArtifactFamily,
    Phase0ArtifactManifest,
    Phase0ArtifactRecord,
    Phase0ArtifactStatus,
    Phase0ReadinessState,
    Phase0UpgradeBridgeState,
    Phase0WorkspaceRecord,
)
from src.ccp.services.phase0_artifact_store import Phase0ArtifactStore
from src.ccp.services.phase0_migration_service import Phase0MigrationService
from src.ccp.services.phase0_workspace_service import Phase0WorkspaceService


router = APIRouter()
workspace_service = Phase0WorkspaceService()
artifact_store = Phase0ArtifactStore(workspace_service=workspace_service)
migration_service = Phase0MigrationService(
    workspace_service=workspace_service,
    artifact_store=artifact_store,
)


class ArtifactRegisterRequest(BaseModel):
    family: Phase0ArtifactFamily = Field(...)
    source_receipt_id: str = Field(...)
    display_label: str = Field(...)
    mime_type: Optional[str] = Field(default=None)
    file_size_bytes: Optional[int] = Field(default=None, ge=0)
    storage_uri: Optional[str] = Field(default=None)
    checksum_sha256: Optional[str] = Field(default=None)
    parent_artifact_ids: list[str] = Field(default_factory=list)
    metadata: dict[str, str] = Field(default_factory=dict)


class ArtifactTransitionRequest(BaseModel):
    target_status: Phase0ArtifactStatus = Field(...)
    human_review_note: Optional[str] = Field(default=None)


class UpgradeBridgeRequest(BaseModel):
    target_tier: str = Field(...)
    payment_amount_cents: Optional[int] = Field(default=None, ge=0)
    credit_applied_cents: Optional[int] = Field(default=None, ge=0)


@router.post("/workspaces", response_model=Phase0WorkspaceRecord)
def create_workspace(payload: Phase0ProspectPacket = Body(...)):
    try:
        return workspace_service.create_workspace(payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail={"error": "WORKSPACE_CREATE_REJECTED", "reason": str(exc)})


@router.get("/workspaces/{workspace_id}", response_model=Phase0WorkspaceRecord)
def get_workspace(workspace_id: str = Path(...)):
    try:
        return workspace_service.get_workspace(workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/workspaces/{workspace_id}/artifacts", response_model=list[Phase0ArtifactRecord])
def list_artifacts(workspace_id: str = Path(...)):
    try:
        return artifact_store.get_artifacts_by_workspace(workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.post("/workspaces/{workspace_id}/artifacts", response_model=Phase0ArtifactRecord)
def register_artifact(
    workspace_id: str = Path(...),
    payload: ArtifactRegisterRequest = Body(...),
):
    try:
        return artifact_store.register_artifact(
            workspace_id=workspace_id,
            family=payload.family,
            source_receipt_id=payload.source_receipt_id,
            display_label=payload.display_label,
            mime_type=payload.mime_type,
            file_size_bytes=payload.file_size_bytes,
            storage_uri=payload.storage_uri,
            checksum_sha256=payload.checksum_sha256,
            parent_artifact_ids=payload.parent_artifact_ids,
            metadata=payload.metadata,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.patch("/workspaces/{workspace_id}/artifacts/{artifact_id}/status", response_model=Phase0ArtifactRecord)
def transition_artifact(
    workspace_id: str = Path(...),
    artifact_id: str = Path(...),
    payload: ArtifactTransitionRequest = Body(...),
):
    try:
        artifact = artifact_store.transition_artifact(
            artifact_id=artifact_id,
            target_status=payload.target_status,
            human_review_note=payload.human_review_note,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    if artifact.workspace_id != workspace_id:
        raise HTTPException(status_code=400, detail="ARTIFACT_WORKSPACE_MISMATCH")
    return artifact


@router.get("/workspaces/{workspace_id}/manifest", response_model=Phase0ArtifactManifest)
def get_manifest(workspace_id: str = Path(...)):
    try:
        return artifact_store.assemble_manifest(workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/workspaces/{workspace_id}/readiness", response_model=Phase0ReadinessState)
def get_readiness(workspace_id: str = Path(...)):
    try:
        return workspace_service.compute_readiness(workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/workspaces/{workspace_id}/upgrade-bridge", response_model=Phase0UpgradeBridgeState)
def initiate_upgrade_bridge(
    workspace_id: str = Path(...),
    payload: UpgradeBridgeRequest = Body(...),
):
    try:
        return migration_service.initiate_upgrade_bridge(
            workspace_id=workspace_id,
            target_tier=payload.target_tier,
            payment_amount_cents=payload.payment_amount_cents,
            credit_applied_cents=payload.credit_applied_cents,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
