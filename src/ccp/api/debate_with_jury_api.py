from fastapi import APIRouter, HTTPException
from src.ccp.models.reaction_debate_models import DebateLaunchPayload, DebateCounterTakeIntent, DebateVsArtifactProjection

router = APIRouter()

@router.get("/reactions/debates/{debate_id}", response_model=DebateLaunchPayload)
async def get_debate_launch_payload(debate_id: str):
    """Fetches the launch payload for the react_debate mini app."""
    # Stubs logic
    pass

@router.post("/reactions/debates/{debate_id}/counter-react", response_model=DebateCounterTakeIntent)
async def create_counter_react(debate_id: str, payload: dict):
    """Creates a counter-take recording session bound to an opponent artifact and stance."""
    from src.ccp.services.debate_with_jury_service import DebateWithJuryService
    from src.ccp.services.content_machine import ContentMachinePipeline
    service = DebateWithJuryService(ContentMachinePipeline())
    try:
        return service.create_counter_take_intent(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/reactions/debates/{debate_id}/approve", response_model=DebateVsArtifactProjection)
async def approve_debate_publication(debate_id: str, payload: dict):
    """Explicit approval before VS artifact publication."""
    pass
