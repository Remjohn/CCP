from fastapi import APIRouter
from src.ccp.models.experience_ladder_models import (
    RouteVoiceNoteRequest,
    RouteVoiceNoteResponse,
    ExperienceStatePacket
)

router = APIRouter()

@router.post("/experience/route-voice-note", response_model=RouteVoiceNoteResponse)
async def route_voice_note(request: RouteVoiceNoteRequest):
    pass

@router.get("/experience/state/{client_id}", response_model=ExperienceStatePacket)
async def get_state(client_id: str):
    pass

@router.post("/experience/state/{client_id}/advance")
async def advance_state(client_id: str):
    pass

@router.post("/experience/state/{client_id}/resume")
async def resume_state(client_id: str):
    pass

@router.get("/experience/health")
async def get_health():
    pass
