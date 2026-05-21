"""
FR-ERA3-35 Audit Intelligence Engine API Router
================================================
FastAPI endpoints exposing the Audit Intelligence Engine.
"""

from __future__ import annotations

from typing import Dict, Optional
from fastapi import APIRouter, HTTPException, Path, Body
from pydantic import BaseModel, Field

from src.ccp.api.phase0_intake import service as intake_service
from src.ccp.models.phase0_intake_models import Phase0ProspectPacket
from src.ccp.models.phase0_audit_models import (
    AuditIntelligenceReport,
    PdfAuditPayload,
    ExplainerAuditVideoPayload
)
from src.ccp.services.audit_intelligence_engine import AuditIntelligenceEngine


router = APIRouter()
engine = AuditIntelligenceEngine()

# In-memory persistence for generated audit reports
reports_db: Dict[str, AuditIntelligenceReport] = {}


# ── Request Body Schemas ───────────────────────────────────────────────

class AuditGenerateRequest(BaseModel):
    prospect_id: str = Field(..., description="Unique internal identifier for the prospect")
    audit_target_id: str = Field(..., description="The specific audit target ID to analyze")
    provisional_override: Optional[bool] = Field(default=True, description="Enable provisional contract mode for unbuilt upstream specs")


class AuditDirectGenerateRequest(BaseModel):
    packet: Phase0ProspectPacket = Field(..., description="Full prospect packet snapshot")
    audit_target_id: str = Field(..., description="The specific audit target ID to analyze")
    provisional_override: Optional[bool] = Field(default=True, description="Enable provisional contract mode for unbuilt upstream specs")


# ── REST API Endpoints ─────────────────────────────────────────────────

@router.post("/audits/generate", response_model=AuditIntelligenceReport)
def generate_audit(payload: AuditGenerateRequest = Body(...)):
    """Generates an audit report by looking up a prospect record in the intake store."""
    packet = intake_service.get_prospect(payload.prospect_id)
    if not packet:
        raise HTTPException(
            status_code=404,
            detail=f"Prospect with ID {payload.prospect_id} not found in Phase-0 intake database"
        )
    
    try:
        report = engine.generate_audit(
            packet=packet,
            target_id=payload.audit_target_id,
            provisional_override=payload.provisional_override
        )
        reports_db[report.report_id] = report
        return report
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.post("/audits/generate-direct", response_model=AuditIntelligenceReport)
def generate_audit_direct(payload: AuditDirectGenerateRequest = Body(...)):
    """Generates an audit report directly from an incoming prospect packet snapshot."""
    try:
        report = engine.generate_audit(
            packet=payload.packet,
            target_id=payload.audit_target_id,
            provisional_override=payload.provisional_override
        )
        reports_db[report.report_id] = report
        return report
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.get("/audits/{report_id}", response_model=AuditIntelligenceReport)
def get_audit(report_id: str = Path(...)):
    """Retrieves a cached/generated audit report by its ID."""
    report = reports_db.get(report_id)
    if not report:
        raise HTTPException(status_code=404, detail=f"Audit report with ID {report_id} not found")
    return report


@router.get("/audits/{report_id}/pdf-payload", response_model=PdfAuditPayload)
def get_pdf_payload(report_id: str = Path(...)):
    """Extracts a structured PDF payload for the designated audit report."""
    report = reports_db.get(report_id)
    if not report:
        raise HTTPException(status_code=404, detail=f"Audit report with ID {report_id} not found")
    try:
        return engine.extract_pdf_payload(report)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Failed to extract PDF payload: {str(ex)}")


@router.get("/audits/{report_id}/video-payload", response_model=ExplainerAuditVideoPayload)
def get_video_payload(report_id: str = Path(...)):
    """Extracts a structured 120s animated video explainer payload for the designated audit report."""
    report = reports_db.get(report_id)
    if not report:
        raise HTTPException(status_code=404, detail=f"Audit report with ID {report_id} not found")
    try:
        return engine.extract_video_payload(report)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Failed to extract video payload: {str(ex)}")
