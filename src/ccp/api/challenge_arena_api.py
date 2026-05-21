from fastapi import APIRouter
from src.ccp.models.challenge_arena_models import (
    ChallengeArenaSessionProjection,
    ChallengeDailyRouteRequest,
    ChallengeAssignment,
    HabitVerificationProjection,
    ChallengeSessionCompletionRequest,
    Fr61EvidenceSnapshot,
    SundayPostcardProjection
)

router = APIRouter()

@router.get("/challenge/{participant_id}", response_model=ChallengeArenaSessionProjection)
async def get_challenge_projection(participant_id: str):
    pass

@router.post("/challenge/{participant_id}/daily-route", response_model=ChallengeAssignment)
async def get_daily_route(participant_id: str, request: ChallengeDailyRouteRequest):
    pass

@router.post("/challenge/{participant_id}/habit-intention", response_model=HabitVerificationProjection)
async def submit_habit_intention(participant_id: str, payload: dict):
    pass

@router.post("/challenge/{participant_id}/session-complete", response_model=Fr61EvidenceSnapshot)
async def complete_session(participant_id: str, request: ChallengeSessionCompletionRequest):
    pass

@router.get("/challenge/{participant_id}/postcard/current", response_model=SundayPostcardProjection)
async def get_current_postcard(participant_id: str):
    pass

@router.post("/challenge/{participant_id}/postcard/ack")
async def ack_postcard(participant_id: str):
    pass
