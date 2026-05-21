from src.ccp.models.challenge_arena_models import SundayPostcardProjection, PostcardStatus
from uuid import uuid4
from datetime import datetime
from src.ccp.services.challenge_weekly_rollup import WeeklyTelemetryRollupEngine

class SundayPostcardAssembler:
    async def generate_postcard(self, participant_id: str) -> SundayPostcardProjection:
        engine = WeeklyTelemetryRollupEngine()
        rollup = await engine.rollup(participant_id)
        
        return SundayPostcardProjection(
            postcard_id=uuid4(),
            participant_id=participant_id,
            coach_id="coach_1",
            status=PostcardStatus.PUBLISHED,
            telemetry=rollup,
            qualitative_interpretation="Strong work with 5000 words spoken.",
            forward_forecast="Next week you tackle Structure.",
            published_at=datetime.utcnow()
        )
