from src.ccp.models.onboarding_models import AnonymousRegistrationLink, RegistrationMode
from datetime import datetime
import uuid
from src.ccp.services.benchmark_reveal_guard import BenchmarkRevealGuard

class AnonymousRegistrationLinker:
    async def link(self, session, request) -> AnonymousRegistrationLink:
        BenchmarkRevealGuard.assert_reveal_completed(session)
        return AnonymousRegistrationLink(
            link_id=str(uuid.uuid4()),
            session_id=session.session_id,
            registration_mode=request.registration_mode,
            person_id=str(uuid.uuid4()) if request.telegram_user_id else None,
            linked_at_utc=datetime.utcnow().isoformat()
        )
