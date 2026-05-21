from src.ccp.models.reaction_tierlist_models import TierlistResultProjection, TierlistBoardProjection, TierlistMoveEvent
from typing import List

class ReactionTierlistProjectionService:
    def calculate_totals(self, moves: List[TierlistMoveEvent]) -> tuple[int, int]:
        """Calculates total moves and total distinct items ranked."""
        total_move_count = len(moves)
        distinct_items = len(set([move.item_id for move in moves]))
        return total_move_count, distinct_items

    def construct_result_projection(self, artifact, board: TierlistBoardProjection, moves: List[TierlistMoveEvent]) -> TierlistResultProjection:
        total_moves, words_ranked = self.calculate_totals(moves)
        return TierlistResultProjection(
            artifact=artifact,
            final_board=board,
            total_move_count=total_moves,
            words_ranked_count=words_ranked
        )
