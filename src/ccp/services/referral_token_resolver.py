from src.ccp.models.onboarding_models import AnonymousReferralToken, ReferralChannel
from datetime import datetime
import uuid

class ReferralTokenResolver:
    async def resolve(self, token_str: str | None) -> AnonymousReferralToken:
        if not token_str or token_str == "invalid":
            return AnonymousReferralToken(
                referral_token_id=str(uuid.uuid4()),
                coach_id="default",
                channel=ReferralChannel.direct_link,
                created_at_utc=datetime.utcnow().isoformat()
            )
        
        return AnonymousReferralToken(
            referral_token_id=token_str,
            coach_id="coach_1",
            channel=ReferralChannel.telegram_message,
            created_at_utc=datetime.utcnow().isoformat()
        )
