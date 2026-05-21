from fastapi import APIRouter
from src.ccp.models.testimonial_models import (
    MomentumTriggerEvent,
    TestimonialCaptureSession,
    TransformationProofObject,
    ConsentLevel,
    UserCardProjection,
    ShareArtifactRequest,
    ShareArtifactResponse,
    PeerEndorsementDecision
)

router = APIRouter()

@router.post("/testimonial/triggers")
async def ingest_trigger(event: MomentumTriggerEvent):
    pass

@router.get("/testimonial/capture/{capture_session_id}", response_model=TestimonialCaptureSession)
async def get_capture_session(capture_session_id: str):
    pass

@router.post("/testimonial/capture/{capture_session_id}/recording")
async def submit_recording(capture_session_id: str, payload: dict):
    pass

@router.post("/testimonial/capture/{capture_session_id}/attachments")
async def submit_attachment(capture_session_id: str, payload: dict):
    pass

@router.post("/testimonial/capture/{capture_session_id}/consent")
async def submit_consent(capture_session_id: str, payload: dict):
    pass

@router.post("/testimonial/capture/{capture_session_id}/finalize", response_model=TransformationProofObject)
async def finalize_proof(capture_session_id: str):
    pass

@router.get("/testimonial/cards/{person_id}/current", response_model=UserCardProjection)
async def get_current_card(person_id: str):
    pass

@router.get("/testimonial/cards/{person_id}/history")
async def get_card_history(person_id: str):
    pass

@router.post("/testimonial/cards/{person_id}/share", response_model=ShareArtifactResponse)
async def share_card(person_id: str, request: ShareArtifactRequest):
    pass

@router.get("/testimonial/peer-gate/{person_id}", response_model=PeerEndorsementDecision)
async def get_peer_gate(person_id: str):
    pass
