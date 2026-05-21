from fastapi import APIRouter, HTTPException
from src.ccp.models.onboarding_models import (
    OnboardingLaunchResponse,
    TeaserRevealResponse,
    OfferRevealResponse,
    RegistrationRequest,
    RegistrationResponse,
    OnboardingState
)
from src.ccp.services.referral_token_resolver import ReferralTokenResolver
from src.ccp.services.anonymous_audit_session_manager import AnonymousAuditSessionManager
from src.ccp.services.baseline_audit_recorder import BaselineAuditRecorder
from src.ccp.services.baseline_teaser_scoring_adapter import BaselineTeaserScoringAdapter
from src.ccp.services.post_reveal_offer_projector import PostRevealOfferProjector
from src.ccp.services.anonymous_registration_linker import AnonymousRegistrationLinker
from datetime import datetime

router = APIRouter()

@router.post("/onboarding/session/start", response_model=OnboardingLaunchResponse)
async def start_session(token: str | None = None):
    resolver = ReferralTokenResolver()
    token_obj = await resolver.resolve(token)
    manager = AnonymousAuditSessionManager()
    session = await manager.create_session(token_obj)
    return OnboardingLaunchResponse(session=session)

@router.post("/onboarding/session/{session_id}/audit-upload")
async def upload_audit(session_id: str, payload: dict):
    # Mock upload
    return {"status": "uploaded"}

@router.post("/onboarding/session/{session_id}/audit-complete")
async def complete_audit(session_id: str):
    return {"status": "teaser_processing"}

@router.get("/onboarding/session/{session_id}/teaser", response_model=TeaserRevealResponse)
async def get_teaser(session_id: str):
    adapter = BaselineTeaserScoringAdapter()
    teaser = await adapter.generate_teaser(session_id)
    return TeaserRevealResponse(
        session_id=session_id,
        state=OnboardingState.teaser_revealed,
        teaser=teaser
    )

@router.get("/onboarding/session/{session_id}/offer", response_model=OfferRevealResponse)
async def get_offer(session_id: str):
    # In reality we fetch session, simulate revealed state
    from src.ccp.models.onboarding_models import AnonymousOnboardingSession
    session = AnonymousOnboardingSession(
        session_id=session_id, coach_id="coach_1", state=OnboardingState.teaser_revealed,
        anonymous_device_nonce="nonce", created_at_utc=datetime.utcnow().isoformat(),
        updated_at_utc=datetime.utcnow().isoformat(), benchmark_revealed_at=datetime.utcnow().isoformat()
    )
    
    projector = PostRevealOfferProjector()
    try:
        offer = await projector.project(session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    return OfferRevealResponse(
        session_id=session_id,
        state=OnboardingState.offer_revealed,
        offer=offer
    )

@router.post("/onboarding/session/{session_id}/register", response_model=RegistrationResponse)
async def register(session_id: str, request: RegistrationRequest):
    from src.ccp.models.onboarding_models import AnonymousOnboardingSession
    session = AnonymousOnboardingSession(
        session_id=session_id, coach_id="coach_1", state=OnboardingState.offer_revealed,
        anonymous_device_nonce="nonce", created_at_utc=datetime.utcnow().isoformat(),
        updated_at_utc=datetime.utcnow().isoformat(), benchmark_revealed_at=datetime.utcnow().isoformat()
    )
    
    linker = AnonymousRegistrationLinker()
    try:
        link = await linker.link(session, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    return RegistrationResponse(
        session_id=session_id,
        state=OnboardingState.identity_linked,
        link=link,
        next_action="challenge_handoff_available"
    )

@router.post("/onboarding/session/{session_id}/challenge-handoff")
async def challenge_handoff(session_id: str):
    return {"status": "handoff_ready"}
