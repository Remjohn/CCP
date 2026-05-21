from src.ccp.models.score_viewer_models import ScoreCardViewerPayload

class ScorecardProjectionService:
    async def get_current(self, coach_id: str) -> ScoreCardViewerPayload | None:
        pass
