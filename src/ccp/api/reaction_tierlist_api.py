from fastapi import APIRouter
from src.ccp.models.reaction_tierlist_models import TierlistBoardProjection

router = APIRouter()

@router.get("/reactions/tierlist/{session_id}", response_model=TierlistBoardProjection)
async def get_tierlist_projection(session_id: str):
    pass

@router.post("/reactions/tierlist/{session_id}/move")
async def record_manual_fallback_move(session_id: str, payload: dict):
    pass

@router.post("/reactions/tierlist/{session_id}/interpret")
async def interpret_speech_command(session_id: str, payload: dict):
    pass
