from src.ccp.models.reaction_ranking_quiz_models import (
    RankingQuizSessionProjection,
    RankingQuizProposalArtifact,
    RankingQuizComparisonProjection
)

class ReactionRankingQuizProjectionService:
    def create_session_from_tierlist(self, source_artifact_id: str) -> RankingQuizSessionProjection:
        # Resolves tierlist artifact into a frozen session snapshot
        pass

    def compute_proposal_diff(self, original_ranking: list, proposed_items: list) -> list:
        # Generates diffs
        pass
