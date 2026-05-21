from fastapi import APIRouter, HTTPException
from src.ccp.models.reaction_duel_models import UnifiedDuelProjection, DuelInvitePayload
from src.ccp.services.reaction_duel_service import ReactionDuelService

router = APIRouter()

@router.post("/reactions/duels")
async def create_duel(payload: dict):
    # Dependency injection mocking for now
    svc = ReactionDuelService(None, None)
    result = svc.propose_duel(payload.get("inviter_coach_id"), payload.get("invitee_coach_id"), payload.get("topic_id"))
    return result

@router.post("/reactions/duels/{duel_id}/accept")
async def accept_duel(duel_id: str, payload: dict):
    return {"status": "accepted"}

@router.get("/reactions/duels/{duel_id}", response_model=UnifiedDuelProjection)
async def get_duel(duel_id: str):
    pass

@router.post("/reactions/duels/{duel_id}/publish", response_model=UnifiedDuelProjection)
async def publish_duel(duel_id: str, payload: dict):
    pass
