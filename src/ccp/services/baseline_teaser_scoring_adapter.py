from src.ccp.models.onboarding_models import BenchmarkTeaserScore
from datetime import datetime
import uuid

class BaselineTeaserScoringAdapter:
    async def generate_teaser(self, session_id: str) -> BenchmarkTeaserScore:
        # Internally would call TraitScoringEngine
        return BenchmarkTeaserScore(
            teaser_id=str(uuid.uuid4()),
            session_id=session_id,
            benchmark_score=75,
            score_label="Clear and Concise",
            one_line_insight="You have strong vocal clarity.",
            next_move_hint="Focus on pacing in your next session.",
            confidence_note="High confidence derived from 60s sample.",
            revealed_at_utc=datetime.utcnow().isoformat()
        )
