"""
FR-ERA3-38 Phase-0 Operator Console and SLA Tracker API Router
==============================================================
FastAPI endpoints for aggregating Phase-0 package queues, deep-dive detail traces,
and executing manual operator retry, escalation, and alert acknowledgment actions.
"""

from __future__ import annotations
from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException, Path, Body, Query
from pydantic import BaseModel, Field

from src.ccp.services.phase0_operator_console_service import Phase0OperatorConsoleService
from src.ccp.services.phase0_intake_service import Phase0IntakeService
from src.ccp.services.phase0_workspace_service import Phase0WorkspaceService
from src.ccp.services.phase0_delivery_orchestrator import Phase0DeliveryOrchestrator
from src.ccp.models.phase0_operator_console_models import (
    Phase0OperatorQueueView,
    Phase0PackageDetailView,
    Phase0EscalationLevel,
    Phase0EscalationState,
)

router = APIRouter()

from src.ccp.core.receipt_chain import ReceiptChain

# Instantiate shared global instances for the operator console API.
intake_service = Phase0IntakeService()
workspace_service = Phase0WorkspaceService()
delivery_orchestrator = Phase0DeliveryOrchestrator()
receipt_chain = ReceiptChain(coach_acronym="P0W")

console_service = Phase0OperatorConsoleService(
    workspace_service=workspace_service,
    delivery_orchestrator=delivery_orchestrator,
    receipt_chain=receipt_chain,
)


# ── Request Body Schemas ───────────────────────────────────────────────

class OperatorActionRequest(BaseModel):
    operator_id: str = Field(..., description="Unique ID of the operator performing this action")


class EscalateRequest(BaseModel):
    operator_id: str = Field(..., description="Unique ID of the operator triggering the escalation")
    level: Phase0EscalationLevel = Field(..., description="The escalation urgency tier level to elevate to")
    reason: str = Field(..., description="Detailed explanation for triggering this escalation")


class AcknowledgeAlertRequest(BaseModel):
    alert_id: str = Field(..., description="The unique ID of the alert requiring acknowledgment")
    operator_id: str = Field(..., description="Unique ID of the operator acknowledging the alert")


# ── API Endpoints ──────────────────────────────────────────────────────

@router.get("/operator/queue", response_model=Phase0OperatorQueueView)
def get_operator_queue(
    workspace_id: str = Query(..., description="Unique workspace namespace identifier to group target runs")
):
    """
    AC1 & AC2 & AC8: Sweeps all active prospect intake packets and maps them to a
    consolidated queue matrix with sorted 24h SLA countdown priority.
    """
    try:
        packets = list(intake_service.prospects.values())
        return console_service.get_operator_queue_view(
            workspace_id=workspace_id,
            packets=packets
        )
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.get("/operator/package/{phase0_packet_id}", response_model=Phase0PackageDetailView)
def get_package_detail(
    phase0_packet_id: str = Path(..., description="Unique Phase-0 Prospect package ID to inspect")
):
    """
    AC3 & AC6 & AC7: Compiles a complete details view trace including active alerts,
    downstream run steps, Stripe payment parameters, and escalation statuses.
    """
    packet = intake_service.prospects.get(phase0_packet_id)
    if not packet:
        raise HTTPException(
            status_code=404,
            detail=f"Prospect packet with ID '{phase0_packet_id}' not found"
        )
    try:
        coach_id = packet.coach_id or "P0W"
        return console_service.get_package_detail_view(
            coach_id=coach_id,
            packet_id=phase0_packet_id,
            packet=packet
        )
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.post("/operator/package/{phase0_packet_id}/retry")
def trigger_retry(
    phase0_packet_id: str = Path(..., description="Unique Phase-0 package ID to retry"),
    payload: OperatorActionRequest = Body(...)
):
    """
    AC4 & AC5: Executes manual force-retry or override pipeline command post-recovery.
    Logs console action and logs target receipt chain entries.
    """
    packet = intake_service.prospects.get(phase0_packet_id)
    if not packet:
        raise HTTPException(
            status_code=404,
            detail=f"Prospect packet with ID '{phase0_packet_id}' not found"
        )
    try:
        coach_id = packet.coach_id or "P0W"
        success = console_service.trigger_retry(
            coach_id=coach_id,
            packet_id=phase0_packet_id,
            operator_id=payload.operator_id
        )
        if not success:
            raise HTTPException(status_code=400, detail="Failed to dispatch retry action to downstream pipelines")
        return {"status": "success", "message": "Manual retry override logged and dispatched downstream"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.post("/operator/package/{phase0_packet_id}/escalate", response_model=Phase0EscalationState)
def trigger_escalation(
    phase0_packet_id: str = Path(..., description="Unique Phase-0 package ID to escalate"),
    payload: EscalateRequest = Body(...)
):
    """
    AC5: Elevates or raises the typed operational escalation severity profile for a package.
    """
    packet = intake_service.prospects.get(phase0_packet_id)
    if not packet:
        raise HTTPException(
            status_code=404,
            detail=f"Prospect packet with ID '{phase0_packet_id}' not found"
        )
    try:
        coach_id = packet.coach_id or "P0W"
        return console_service.trigger_escalation(
            coach_id=coach_id,
            packet_id=phase0_packet_id,
            level=payload.level,
            reason=payload.reason,
            operator_id=payload.operator_id
        )
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.post("/operator/package/{phase0_packet_id}/acknowledge-alert")
def acknowledge_alert(
    phase0_packet_id: str = Path(..., description="Unique Phase-0 package ID associated with the alert"),
    payload: AcknowledgeAlertRequest = Body(...)
):
    """
    AC4: Acknowledges an active warning or high alert, removing it from the active console view counts.
    """
    try:
        success = console_service.acknowledge_alert(
            alert_id=payload.alert_id,
            operator_id=payload.operator_id
        )
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Active alert with ID '{payload.alert_id}' not found or already acknowledged"
            )
        return {"status": "success", "message": f"Alert '{payload.alert_id}' successfully acknowledged"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
