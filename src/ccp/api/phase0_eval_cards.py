"""
FR-ERA3-35C Eval Card System and Shareable Audit Board API Router
=================================================================
FastAPI endpoints for card projection, board assembly, and premium export rendering.
"""

from __future__ import annotations

from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException, Path, Body, Query
from pydantic import BaseModel, Field

from src.ccp.api.phase0_audit import reports_db
from src.ccp.models.phase0_audit_models import AuditIntelligenceReport
from src.ccp.models.phase0_eval_card_models import (
    EvalCard,
    EvalCardBoard,
    EvalCardRole,
    EvalBoardKind,
    BoardDensity,
    ShareableAuditBoardRenderRequest
)
from src.ccp.services.eval_card_projection_service import EvalCardProjectionService
from src.ccp.services.eval_board_assembly_service import EvalBoardAssemblyService


router = APIRouter()
projection_service = EvalCardProjectionService()
assembly_service = EvalBoardAssemblyService()

# In-memory databases
cards_db: Dict[str, EvalCard] = {}
boards_db: Dict[str, EvalCardBoard] = {}


# ── Request Body Schemas ───────────────────────────────────────────────

class CardProjectRequest(BaseModel):
    report_id: str = Field(..., description="The unique ID of the generated audit report")
    role: EvalCardRole = Field(default=EvalCardRole.audit_primary, description="Role intended for this card")


class CardProjectDirectRequest(BaseModel):
    report: AuditIntelligenceReport = Field(..., description="The complete AuditIntelligenceReport")
    role: EvalCardRole = Field(default=EvalCardRole.audit_primary, description="Role intended for this card")


class BoardAssembleRequest(BaseModel):
    report_id: str = Field(..., description="Unique ID of the parent report")
    board_kind: EvalBoardKind = Field(..., description="The type of board spread")
    card_ids: List[str] = Field(..., description="List of card IDs to include on this board")
    title: str = Field(..., description="Board Title")
    subtitle: Optional[str] = Field(default=None, description="Board Subtitle")
    density: BoardDensity = Field(default=BoardDensity.standard, description="Layout spacing density")
    columns: Optional[int] = Field(default=None, description="Explicit column count")
    featured_card_id: Optional[str] = Field(default=None, description="Featured highlight card ID")


# ── API Endpoints ──────────────────────────────────────────────────────

@router.post("/eval-cards/project", response_model=EvalCard)
async def project_card_from_report(payload: CardProjectRequest = Body(...)):
    """Projects an existing audit report from database into a premium card face."""
    report = reports_db.get(payload.report_id)
    if not report:
        raise HTTPException(
            status_code=404,
            detail=f"Audit report with ID {payload.report_id} not found"
        )
    try:
        card = await projection_service.project_card(report=report, role=payload.role)
        cards_db[card.card_id] = card
        return card
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.post("/eval-cards/project-direct", response_model=EvalCard)
async def project_card_direct(payload: CardProjectDirectRequest = Body(...)):
    """Projects a complete incoming AuditIntelligenceReport snapshot direct to card."""
    try:
        card = await projection_service.project_card(report=payload.report, role=payload.role)
        cards_db[card.card_id] = card
        return card
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.get("/eval-cards/{card_id}", response_model=EvalCard)
def get_card(card_id: str = Path(...)):
    """Retrieves a projected card from the database."""
    card = cards_db.get(card_id)
    if not card:
        raise HTTPException(status_code=404, detail=f"EvalCard with ID {card_id} not found")
    return card


@router.post("/eval-cards/assemble-board", response_model=EvalCardBoard)
def assemble_board(payload: BoardAssembleRequest = Body(...)):
    """Assembles designated projected cards into a screenshot-safe multi-card board."""
    cards = []
    for cid in payload.card_ids:
        card = cards_db.get(cid)
        if not card:
            raise HTTPException(
                status_code=404,
                detail=f"EvalCard with ID {cid} not found; cannot assemble board"
            )
        cards.append(card)

    try:
        board = assembly_service.assemble_board(
            report_id=payload.report_id,
            board_kind=payload.board_kind,
            cards=cards,
            title=payload.title,
            subtitle=payload.subtitle,
            density=payload.density,
            columns=payload.columns,
            featured_card_id=payload.featured_card_id
        )
        boards_db[board.board_id] = board
        return board
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.get("/eval-cards/boards/{board_id}", response_model=EvalCardBoard)
def get_board(board_id: str = Path(...)):
    """Retrieves an assembled card board from the database."""
    board = boards_db.get(board_id)
    if not board:
        raise HTTPException(status_code=404, detail=f"EvalCardBoard with ID {board_id} not found")
    return board


@router.post("/eval-cards/render-board")
def request_shareable_render(request: ShareableAuditBoardRenderRequest = Body(...)):
    """
    Renders a screenshot-ready high-contrast share surface.
    Simulates high-fidelity export rendering to Telegram/AFFiNE canvas formats.
    """
    if not request.board.layout.screenshot_safe:
        raise HTTPException(
            status_code=400,
            detail="Board layout must be explicitly configured as screenshot_safe to render."
        )

    # Returns export metadata and location URI
    return {
        "board_id": request.board.board_id,
        "render_uri": f"https://render.ccp.coaches/exports/{request.board.board_id}.png",
        "output_format": request.output_format,
        "target_surface": request.target_surface,
        "watermark_applied": request.watermark_enabled,
        "resolution": "2400x1600",
        "status": "rendered_success"
    }
