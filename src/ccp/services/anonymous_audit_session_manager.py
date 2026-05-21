from src.ccp.models.onboarding_models import AnonymousOnboardingSession, OnboardingState, AnonymousReferralToken
import uuid
import os
from datetime import datetime

class AnonymousAuditSessionManager:
    async def create_session(self, token: AnonymousReferralToken) -> AnonymousOnboardingSession:
        return AnonymousOnboardingSession(
            session_id=str(uuid.uuid4()),
            coach_id=token.coach_id,
            state=OnboardingState.anonymous_session_created,
            referral_token_id=token.referral_token_id,
            anonymous_device_nonce=os.urandom(16).hex(),
            created_at_utc=datetime.utcnow().isoformat(),
            updated_at_utc=datetime.utcnow().isoformat()
        )
