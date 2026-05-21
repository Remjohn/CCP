from fastapi import APIRouter
from src.ccp.models.score_viewer_models import (
    ScoreCardViewerPayload,
    ScoreViewerAckRequest,
    ScoreViewerAckResponse,
    TraitDetailPayload
)

router = APIRouter()

@router.get("/score/{coach_id}/current", response_model=ScoreCardViewerPayload)
async def get_current_score(coach_id: str):
    pass

@router.get("/score/{coach_id}/history")
async def get_score_history(coach_id: str):
    pass

@router.post("/score/{coach_id}/ack", response_model=ScoreViewerAckResponse)
async def ack_insight(coach_id: str, request: ScoreViewerAckRequest):
    pass

@router.get("/score/{coach_id}/trait/{trait_name}", response_model=TraitDetailPayload)
async def get_trait_detail(coach_id: str, trait_name: str):
    pass
