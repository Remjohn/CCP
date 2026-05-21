"""
FR-ERA3-39 Phase-0 Campaign Workspace API Router
=================================================
FastAPI endpoints for aggregating Campaign Workspace views, binding coach records,
staging bulk file uploads inside a shared namespace workspace, and triggering pipeline execution.
"""

from __future__ import annotations

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query, Path, Body
from pydantic import BaseModel, Field

from src.ccp.models.phase0_campaign_frontend_models import (
    Phase0CampaignWorkspace,
    Phase0CoachRow,
    Phase0CoachBinding,
    Phase0BatchUploadSession,
    Phase0ReadinessSummary,
    Phase0ExecutionRequest,
    Phase0WorkspaceFilterState,
    Phase0BulkAttachmentResult,
    Phase0WorkspaceHealth,
)

from src.ccp.api.phase0_operator_console import (
    intake_service,
    workspace_service,
    delivery_orchestrator,
    receipt_chain,
)
from src.ccp.services.phase0_campaign_workspace_service import Phase0CampaignWorkspaceService

# Initialize Campaign Workspace Router
router = APIRouter()

# Instantiate the campaign workspace service reusing global shared state
campaign_workspace_service = Phase0CampaignWorkspaceService(
    intake_service=intake_service,
    workspace_service=workspace_service,
    delivery_orchestrator=delivery_orchestrator,
    receipt_chain=receipt_chain,
)


# ── Request Body Schemas ───────────────────────────────────────────────

class CoachBindRequest(BaseModel):
    workspace_id: str = Field(..., description="Unique campaign workspace identifier")
    row_id: str = Field(..., description="The unique row or prospect intake ID")
    coach_id: str = Field(..., description="The target coach ID to normalise/bind")
    provisional_label: Optional[str] = Field(None, description="Provisional display label for draft bindings")


class BatchUploadFileInfo(BaseModel):
    original_filename: str = Field(..., description="The filename of the staged media file")
    media_kind: str = Field("supporting_reference", description="The kind/type of intake source material")
    file_size_bytes: int = Field(1024, ge=0, description="The file size in bytes")
    mime_type: Optional[str] = Field(None, description="The MIME type of the uploaded file")
    duration_seconds: Optional[float] = Field(None, ge=0, description="Optional audio/video play duration")


class BatchUploadRequest(BaseModel):
    workspace_id: str = Field(..., description="Unique campaign workspace identifier")
    operator_id: str = Field(..., description="Unique operator ID staging the uploads")
    files: List[BatchUploadFileInfo] = Field(..., description="List of files to process and attach")
    target_row_ids: List[str] = Field(..., description="List of potential target row IDs for file routing")


class ExecuteWorkspaceRequest(BaseModel):
    workspace_id: str = Field(..., description="Unique campaign workspace identifier")
    row_ids: List[str] = Field(..., min_length=1, description="List of ready row/prospect IDs to execute")
    operator_id: str = Field(..., description="Unique operator ID triggering the execution")


# ── API Endpoints ──────────────────────────────────────────────────────

@router.get("/workspace", response_model=Phase0CampaignWorkspace)
def get_campaign_workspace(
    workspace_id: str = Query(..., description="Unique workspace identifier"),
    operator_id: str = Query(..., description="Operator requesting the workspace view"),
    readiness_filter: str = Query("ALL", description="Filter by ALL, READY, BLOCKED, PARTIAL"),
    delivery_filter: str = Query("ALL", description="Filter by ALL, NOT_STARTED, RUNNING, REVIEW, DELIVERED"),
    payment_filter: str = Query("ALL", description="Filter by ALL, UNPAID, PAID, UPGRADED"),
    search_query: str = Query("", description="Query to filter rows by name or coach ID"),
    sort_key: str = Query("UPDATED", description="Sort key: UPDATED, READY_FIRST, NAME, PAYMENT_STATE"),
):
    """
    AC8: Fetch full campaign workspace view. Automatically applies status filtering and sorting,
    returning fully synthesized coach rows in a single structured payload.
    """
    try:
        # Validate and build filter state
        filter_state = Phase0WorkspaceFilterState(
            readiness_filter=readiness_filter,
            delivery_filter=delivery_filter,
            payment_filter=payment_filter,
            search_query=search_query,
            sort_key=sort_key,
        )
        
        # Update the filter state on the workspace
        campaign_workspace_service.update_filter_state(workspace_id, filter_state)
        
        # Fetch the synthesized view
        return campaign_workspace_service.get_workspace_view(workspace_id, operator_id)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Failed to fetch workspace: {str(ex)}")


@router.post("/workspace/coach-bind", response_model=Phase0CoachBinding)
def bind_coach_row(
    payload: CoachBindRequest = Body(...),
):
    """
    AC1: Bind/map an internal prospect packet record to a stable coach_id.
    Validates binding status and records a receipt event.
    """
    try:
        return campaign_workspace_service.bind_coach(
            workspace_id=payload.workspace_id,
            row_id=payload.row_id,
            coach_id=payload.coach_id,
            provisional_label=payload.provisional_label,
        )
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Coach binding error: {str(ex)}")


@router.post("/workspace/batch-upload", response_model=Phase0BulkAttachmentResult)
def batch_stage_upload(
    payload: BatchUploadRequest = Body(...),
):
    """
    AC2 & AC3 & AC4: Bulk upload / attach multiple files staged across one or many coach rows.
    Preserves artifact lineage by matching files to specific coach namespaces.
    """
    try:
        # Map Pydantic file structures to raw dictionaries for internal service
        files_dict_list = []
        for f in payload.files:
            files_dict_list.append({
                "original_filename": f.original_filename,
                "media_kind": f.media_kind,
                "file_size_bytes": f.file_size_bytes,
                "mime_type": f.mime_type,
                "duration_seconds": f.duration_seconds,
            })
            
        return campaign_workspace_service.bulk_stage_upload(
            workspace_id=payload.workspace_id,
            operator_id=payload.operator_id,
            files=files_dict_list,
            target_row_ids=payload.target_row_ids,
        )
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Batch upload staging error: {str(ex)}")


@router.post("/workspace/execute", response_model=List[Phase0ExecutionRequest])
def trigger_pipeline_execution(
    payload: ExecuteWorkspaceRequest = Body(...),
):
    """
    AC6 & AC7: Trigger delivery pipeline for selected ready rows.
    Automatically blocks execution and raises an error if any of the target rows are not ready.
    """
    try:
        return campaign_workspace_service.trigger_pipeline_execution(
            workspace_id=payload.workspace_id,
            row_ids=payload.row_ids,
            operator_id=payload.operator_id,
        )
    except ValueError as ex:
        # Captures F2 (Provisional block) or F6 (Unready block) constraints
        raise HTTPException(status_code=400, detail=str(ex))
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Execution trigger failure: {str(ex)}")


@router.get("/workspace/health", response_model=Phase0WorkspaceHealth)
def check_workspace_health(
    workspace_id: str = Query(..., description="Unique campaign workspace identifier"),
):
    """
    Query system health and integrations. Verifies intake APIs, downstream delivery systems,
    commercial APIs, receipt chains, and shared pre-container storage endpoints.
    """
    try:
        return campaign_workspace_service.check_health(workspace_id)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Workspace health check failed: {str(ex)}")


@router.get("/workspace/{phase0_packet_id}", response_model=Phase0CoachRow)
def get_workspace_row_detail(
    phase0_packet_id: str = Path(..., description="Prospect packet or row ID to detail"),
    workspace_id: str = Query(..., description="Unique campaign workspace identifier"),
):
    """
    AC5: Deep-dive query detail for a single coach row / prospect packet.
    """
    try:
        rows = campaign_workspace_service.synthesize_rows(workspace_id)
        row = next((r for r in rows if r.row_id == phase0_packet_id or r.phase0_packet_id == phase0_packet_id), None)
        if not row:
            raise HTTPException(
                status_code=404,
                detail=f"Prospect row with ID '{phase0_packet_id}' not found in workspace '{workspace_id}'"
            )
        return row
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Failed to fetch row details: {str(ex)}")
