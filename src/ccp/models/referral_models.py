"""Silent Referral Architecture Models — FR-ERA3-03.
UserCardPayload, SignedUserCard, VoteValidationResult, ReferralEscalationState, and error types."""
from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field


class UserCardPayload(BaseModel):
    """Cryptographically bound user card payload per §5 / DEP-SEC-011."""
    session_id: str = Field(..., description="Unique session ID where the score was achieved")
    coach_id: str = Field(..., description="The ID of the coach who achieved the score")
    timestamp: datetime = Field(..., description="The exact time the score was calculated")
    biometric_hash: str = Field(..., description="SHA-256 hash of the biometric data points")
    score_value: int = Field(..., ge=0, le=100, description="The validated biometric score")


class SignedUserCard(BaseModel):
    """User card with HMAC-SHA256 signature per Phase5-M01."""
    payload: UserCardPayload
    signature: str = Field(..., description="HMAC-SHA256 signature of the payload")


class VoteValidationResult(BaseModel):
    """Ephemeral Win-State result per Phase5-M02 / EXP-TRG-005."""
    is_correct: bool = Field(..., description="Whether the peer's vote matched the consensus")
    win_state_message: str = Field(..., description="The Ephemeral Win-State message (e.g., 'Your intuition matches the top 10%')")
    expansion_trigger_unlocked: bool = Field(..., description="MUST be True before prompting the peer to record")


class ReferralEscalationState(BaseModel):
    """State machine for the Vote-Then-React escalation pathway per §4 Phase 3."""
    peer_telegram_id: int
    coach_source_id: str
    vote_submitted: bool = False
    win_state_delivered: bool = False
    escalation_presented: bool = False


class SignatureMismatchError(Exception):
    """Raised when HMAC signature verification fails (AC1 failure case)."""
    pass


class EarnedEscalationViolation(Exception):
    """Raised when escalation is attempted before win_state_delivered (AC2 failure case)."""
    pass
