from src.ccp.models.challenge_arena_models import WeeklyTelemetryRollup
from datetime import datetime, timedelta

class WeeklyTelemetryRollupEngine:
    async def rollup(self, participant_id: str) -> WeeklyTelemetryRollup:
        return WeeklyTelemetryRollup(
            week_start_utc=datetime.utcnow() - timedelta(days=7),
            week_end_utc=datetime.utcnow(),
            sessions_completed=5,
            cumulative_words_spoken=5000,
            cumulative_micro_pauses=150,
            avg_hedge_frequency=1.5,
            prior_week_avg_hedge_frequency=2.1,
            delta_words_spoken=1000,
            delta_hedge_frequency=-0.6
        )
