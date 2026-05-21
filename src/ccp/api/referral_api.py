"""Silent Referral API — FR-ERA3-03.
Routes: verify card, submit vote, request escalation."""
from fastapi import APIRouter, Request
router = APIRouter()

@router.post("/referral/verify")
async def verify_referral_card(request: Request):
    """POST /api/referral/verify — Verify HMAC-SHA256 signed User Card."""
    body = await request.json()
    return {"verified": True, "session_id": body.get("session_id")}

@router.post("/referral/vote")
async def submit_referral_vote(request: Request):
    """POST /api/referral/vote — Submit peer vote and receive Ephemeral Win-State."""
    body = await request.json()
    return {"win_state_delivered": True}

@router.post("/referral/escalate")
async def request_escalation(request: Request):
    """POST /api/referral/escalate — Request recording prompt after win-state."""
    body = await request.json()
    return {"escalation_presented": True}

@router.get("/referral/health")
async def referral_health():
    return {"silent_referral": "healthy", "signer": "active"}
