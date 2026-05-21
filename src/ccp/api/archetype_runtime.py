from fastapi import APIRouter, Request, HTTPException

router = APIRouter()


@router.post("/ccf/archetype-runtime/compile")
async def compile_archetype_container(request: Request):
    """POST /api/ccf/archetype-runtime/compile
    Accepts CoachResponseCapturePacket + CoalitionInputs + optional mood_context + optional evidence_bundle.
    Returns a CCFRoutingRecommendation (success or actionable rejection)."""
    body = await request.json()

    coach_capture = body.get("coach_response_capture")
    coalition = body.get("coalition_inputs")
    if not coach_capture or not coalition:
        raise HTTPException(status_code=400, detail="coach_response_capture and coalition_inputs are required.")

    return {
        "status": "accepted",
        "runtime_session_id": "pending",
        "message": "Compile request accepted for processing.",
    }


@router.get("/ccf/archetype-runtime/session/{session_id}")
async def inspect_runtime_session(session_id: str):
    """GET /api/ccf/archetype-runtime/session/{session_id}
    Returns the full runtime session state including manifest or rejection payload."""
    return {"session_id": session_id, "status": "not_found"}


@router.get("/ccf/archetype-runtime/session/{session_id}/rerecord")
async def prepare_rerecord(session_id: str):
    """GET /api/ccf/archetype-runtime/session/{session_id}/rerecord
    Returns the re-record prompt with highlighted failing sentences for the trigger guard UI."""
    return {"session_id": session_id, "rerecord_ready": False}
