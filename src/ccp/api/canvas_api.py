"""
CVE Canvas Assembly API
=======================
FastAPI router exposing CanvasCompositionService (FR-VIS-05)
to the Canva frontend editor.

Endpoints:
  POST /canvas/compositions            — create from VCB
  GET  /canvas/compositions/{id}       — get composition
  POST /canvas/compositions/{id}/assets     — receive RunningHub asset
  POST /canvas/compositions/{id}/export     — record export URLs
  POST /canvas/compositions/{id}/approve    — approve & publish
  POST /canvas/compositions/{id}/edit-approve — edit then approve
  POST /canvas/compositions/{id}/regenerate — request slide regen
  GET  /canvas/templates               — list registered templates
"""

from __future__ import annotations

import tempfile
from typing import Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.visual_engine_models import (
    CanvasCompositionError,
)
from src.ccp.services.canvas_composition_service import (
    CanvasCompositionService,
    get_template,
    _TEMPLATE_REGISTRY,
)

router = APIRouter()


# ── Request / Response schemas ─────────────────────────────────────────


class DimensionsIn(BaseModel):
    width_px: int = Field(..., gt=0)
    height_px: int = Field(..., gt=0)
    aspect_ratio: str


class HandleBarIn(BaseModel):
    visible: bool = True
    coach_name: str = ""
    coach_handle: str = ""
    profile_picture_url: Optional[str] = None
    logo_url: Optional[str] = None


class CreateCompositionRequest(BaseModel):
    coach_acronym: str = Field(..., min_length=2, max_length=4)
    vcb_id: str
    template_id: str
    slide_count: int = Field(..., ge=1)
    dimensions: DimensionsIn
    handle_bar: HandleBarIn
    text_content: Optional[dict[int, dict[str, str]]] = None
    content_output_id: Optional[str] = None


class ReceiveAssetRequest(BaseModel):
    coach_acronym: str = Field(..., min_length=2, max_length=4)
    slide_index: int = Field(..., ge=0)
    image_url: str
    image_source: str = "runninghub_tier_3"
    validation_verdict: Optional[str] = None


class ExportRequest(BaseModel):
    coach_acronym: str = Field(..., min_length=2, max_length=4)
    slide_urls: Optional[list[str]] = None
    stitch_url: Optional[str] = None
    zip_url: Optional[str] = None


class ApproveRequest(BaseModel):
    coach_acronym: str = Field(..., min_length=2, max_length=4)


class RegenerateRequest(BaseModel):
    coach_acronym: str = Field(..., min_length=2, max_length=4)
    slide_index: int = Field(..., ge=0)
    revision_note: str


# ── Helpers ────────────────────────────────────────────────────────────


def _build_service(coach_acronym: str) -> CanvasCompositionService:
    """Instantiate a service scoped to the operator's coach."""
    tmp = tempfile.mkdtemp()
    rc = ReceiptChain(coach_acronym=coach_acronym, log_dir=tmp)
    return CanvasCompositionService(
        coach_acronym=coach_acronym,
        receipt_chain=rc,
    )


def _handle_service_error(exc: ValueError) -> None:
    """Map CanvasCompositionError values to HTTP status codes."""
    msg = str(exc)
    if CanvasCompositionError.TEMPLATE_NOT_FOUND.value in msg:
        raise HTTPException(status_code=404, detail=msg)
    if CanvasCompositionError.WEBHOOK_TASK_MISMATCH.value in msg:
        raise HTTPException(status_code=404, detail=msg)
    if CanvasCompositionError.INVALID_COACH_ACRONYM.value in msg:
        raise HTTPException(status_code=400, detail=msg)
    # generic fallback
    raise HTTPException(status_code=400, detail=msg)


# ── Service singleton (single-tenant) ─────────────────────────────────
# In single-tenant mode we keep ONE service instance per coach acronym
# so compositions persist in-memory across requests.

_SERVICE_CACHE: dict[str, CanvasCompositionService] = {}


def _get_service(coach_acronym: str) -> CanvasCompositionService:
    """Return (or create) the singleton service for this coach."""
    coach = coach_acronym.upper()
    if coach not in _SERVICE_CACHE:
        tmp = tempfile.mkdtemp()
        rc = ReceiptChain(coach_acronym=coach, log_dir=tmp)
        _SERVICE_CACHE[coach] = CanvasCompositionService(
            coach_acronym=coach,
            receipt_chain=rc,
        )
    return _SERVICE_CACHE[coach]


# ── Endpoints ──────────────────────────────────────────────────────────


@router.post("/canvas/compositions", status_code=201)
async def create_composition(body: CreateCompositionRequest):
    """Stage 1 — Create a composition from a VCB."""
    try:
        svc = _get_service(body.coach_acronym)
        comp = svc.create_composition(
            vcb_id=body.vcb_id,
            template_id=body.template_id,
            slide_count=body.slide_count,
            dimensions=body.dimensions.model_dump(),
            handle_bar=body.handle_bar.model_dump(),
            text_content=body.text_content,
            content_output_id=body.content_output_id,
        )
        return comp.model_dump()
    except ValueError as exc:
        _handle_service_error(exc)


@router.get("/canvas/compositions/{composition_id}")
async def get_composition(
    composition_id: str,
    coach_acronym: str,
):
    """Retrieve a composition by ID."""
    svc = _get_service(coach_acronym)
    comp = svc.get_composition(composition_id)
    if comp is None:
        raise HTTPException(status_code=404, detail=f"Composition '{composition_id}' not found")
    return comp.model_dump()


@router.post("/canvas/compositions/{composition_id}/assets")
async def receive_asset(composition_id: str, body: ReceiveAssetRequest):
    """Stage 2 — Receive a RunningHub asset for a slide."""
    try:
        svc = _get_service(body.coach_acronym)
        comp = svc.receive_asset(
            composition_id=composition_id,
            slide_index=body.slide_index,
            image_url=body.image_url,
            image_source=body.image_source,
            validation_verdict=body.validation_verdict,
        )
        return comp.model_dump()
    except ValueError as exc:
        _handle_service_error(exc)


@router.post("/canvas/compositions/{composition_id}/export")
async def export_composition(composition_id: str, body: ExportRequest):
    """Stage 3 — Record export asset URLs."""
    try:
        svc = _get_service(body.coach_acronym)
        comp = svc.export_composition(
            composition_id=composition_id,
            slide_urls=body.slide_urls,
            stitch_url=body.stitch_url,
            zip_url=body.zip_url,
        )
        return comp.model_dump()
    except ValueError as exc:
        _handle_service_error(exc)


@router.post("/canvas/compositions/{composition_id}/approve")
async def approve_composition(composition_id: str, body: ApproveRequest):
    """Stage 4 — Approve & publish."""
    try:
        svc = _get_service(body.coach_acronym)
        comp = svc.approve(composition_id)
        return comp.model_dump()
    except ValueError as exc:
        _handle_service_error(exc)


@router.post("/canvas/compositions/{composition_id}/edit-approve")
async def edit_and_approve(composition_id: str, body: ApproveRequest):
    """Stage 4 — Save operator edits then approve."""
    try:
        svc = _get_service(body.coach_acronym)
        comp = svc.edit_and_approve(composition_id)
        return comp.model_dump()
    except ValueError as exc:
        _handle_service_error(exc)


@router.post("/canvas/compositions/{composition_id}/regenerate")
async def regenerate_slide(composition_id: str, body: RegenerateRequest):
    """Stage 4 — Request slide regeneration."""
    try:
        svc = _get_service(body.coach_acronym)
        comp, regen_req = svc.request_regeneration(
            composition_id=composition_id,
            slide_index=body.slide_index,
            revision_note=body.revision_note,
        )
        return {
            "composition": comp.model_dump(),
            "regeneration_request": regen_req.model_dump(),
        }
    except ValueError as exc:
        _handle_service_error(exc)


@router.get("/canvas/templates")
async def list_templates():
    """List all registered composition templates."""
    templates = []
    for tid, meta in _TEMPLATE_REGISTRY.items():
        templates.append({"template_id": tid, **meta})
    return {"templates": templates}
