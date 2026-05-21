from fastapi import APIRouter
from src.ccp.models.reaction_blind_rank_models import BlindRankPromptPack, BlindRankFinalizePayload, BlindRankSessionProjection
from src.ccp.services.blind_rank_finalize_adapter import create_prompt_pack

router = APIRouter()

@router.post("/reactions/blind-rank/session", response_model=BlindRankPromptPack)
async def create_session(payload: dict):
    coach_id = payload.get("coach_id", "default_coach")
    return create_prompt_pack(coach_id)

@router.post("/reactions/blind-rank/finalize", response_model=BlindRankSessionProjection)
async def finalize_session(payload: dict):
    # This acts as the handoff adapter
    pass
