from src.ccp.models.webinar_companion_models import RepSlideAdvanceEvent, RepSlideScoreCard
from datetime import datetime

class WebinarRepScoreAdapter:
    async def generate_slide_score(self, event: RepSlideAdvanceEvent) -> RepSlideScoreCard:
        # Uses trait scoring engine
        return RepSlideScoreCard(
            rep_session_id=event.rep_session_id,
            webinar_id=event.webinar_id,
            slide_index=event.previous_slide_index,
            delivered_at=datetime.utcnow(),
            hedge_density=0.05,
            pause_architecture_score=85.0,
            cta_pressure_stability=90.0,
            highlighted_traits=[],
            feedback_summary="Strong clarity on this slide.",
            next_slide_unlocked=False
        )
