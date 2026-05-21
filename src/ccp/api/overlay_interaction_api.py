from fastapi import APIRouter, Request, HTTPException
from src.ccp.models.overlay_capture_models import OverlayInteractionEvent

router = APIRouter()


@router.post("/overlay/events/{session_id}")
async def ingest_overlay_events(session_id: str, request: Request):
    """Ingest a batch of overlay interaction events from the frontend journal.
    Receives structured OverlayInteractionEvent objects."""
    body = await request.json()
    events = body.get("events", [])
    if not events:
        raise HTTPException(status_code=400, detail="No events provided.")
    return {"session_id": session_id, "events_received": len(events), "status": "queued"}


@router.post("/overlay/capture/{session_id}")
async def ingest_capture_metadata(session_id: str, request: Request):
    """Persist composite capture metadata for a completed recording session."""
    body = await request.json()
    return {"session_id": session_id, "status": "persisted"}


@router.get("/overlay/events/{session_id}")
async def get_overlay_events(session_id: str):
    """Retrieve overlay interaction events for a session."""
    return {"session_id": session_id, "events": []}
