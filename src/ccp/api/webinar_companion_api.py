from fastapi import APIRouter
from src.ccp.models.webinar_companion_models import (
    WebinarCompanionSessionProjection,
    ParticipationCaptureRecord,
    RepSlideAdvanceEvent,
    RepSlideScoreCard
)

router = APIRouter()

@router.get("/webinar/{session_id}")
async def get_webinar_session(session_id: str):
    pass

@router.post("/webinar/{session_id}/prompt/{prompt_id}/submit")
async def submit_prompt(session_id: str, prompt_id: str, payload: dict):
    pass

@router.post("/webinar/rep/{rep_session_id}/slide-advance")
async def advance_slide(rep_session_id: str, payload: dict):
    pass

@router.get("/webinar/rep/{rep_session_id}/slide/{slide_index}/score")
async def get_slide_score(rep_session_id: str, slide_index: int):
    pass
