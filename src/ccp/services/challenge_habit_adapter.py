from src.ccp.models.challenge_arena_models import HabitVerificationProjection
from uuid import uuid4
from datetime import datetime

class ChallengeHabitAdapter:
    async def verify_intent(self, participant_id: str, intent: str) -> HabitVerificationProjection:
        return HabitVerificationProjection(
            tracker_id=uuid4(),
            environmental_cue="When I wake up",
            concrete_action="I will speak",
            habit_status="active",
            verification_verdict="PASS",
            last_checked_date=datetime.utcnow()
        )
