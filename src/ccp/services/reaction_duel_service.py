import uuid
from datetime import datetime
from src.ccp.models.reaction_duel_models import (
    DuelBracketSnapshot,
    DuelBracketTier,
    DuelLifecycleState,
    UnifiedDuelProjection
)

class DuelBracketMatcher:
    @staticmethod
    def calculate_bracket(coach_id: str, traits: list) -> DuelBracketSnapshot:
        # Mocking trait derivation
        # Real implementation would call TraitScoringEngine.score_all_traits()
        
        # formula: confidence_directness_index = (conviction_score + pacing_score) / 20.0
        # formula: polarity_authority_index = (impact_score + (anti_centroid_charge * 100)) / 20.0
        overall = 7.5
        cd_index = 8.0
        pa_index = 8.0
        
        if overall < 4.0:
            tier = DuelBracketTier.foundation
        elif overall < 7.0:
            tier = DuelBracketTier.emerging
        elif overall < 9.0:
            tier = DuelBracketTier.advanced
        else:
            tier = DuelBracketTier.sovereign

        return DuelBracketSnapshot(
            coach_id=coach_id,
            bracket_tier=tier,
            local_bracket_key=f"{tier.value}_bracket",
            overall_trait_average=overall,
            confidence_directness_index=cd_index,
            polarity_authority_index=pa_index,
            calculated_at=datetime.utcnow()
        )

    @staticmethod
    def validate_pairing(inviter: DuelBracketSnapshot, invitee: DuelBracketSnapshot) -> bool:
        if inviter.local_bracket_key != invitee.local_bracket_key:
            return False
        if inviter.bracket_tier != invitee.bracket_tier:
            return False
        return True

class ReactionDuelService:
    def __init__(self, content_machine_pipeline, canvas_composition_service):
        self.cm_pipeline = content_machine_pipeline
        self.canvas_service = canvas_composition_service

    def propose_duel(self, inviter_id: str, invitee_id: str, topic_id: str):
        inviter_bracket = DuelBracketMatcher.calculate_bracket(inviter_id, [])
        invitee_bracket = DuelBracketMatcher.calculate_bracket(invitee_id, [])
        
        if not DuelBracketMatcher.validate_pairing(inviter_bracket, invitee_bracket):
            return {"status": "rejected", "reason": "Bracket mismatch. Safe failure enforced."}
            
        return {"status": "proposed", "duel_id": str(uuid.uuid4())}

    async def publish_duel(self, projection: UnifiedDuelProjection):
        # Wait for both artifacts to hit scored
        if not projection.left_side.artifact or not projection.right_side.artifact:
            return projection
            
        # Unified composition
        projection.render_format = "split_screen_vs"
        projection.audience_vote_open = True
        projection.lifecycle_state = DuelLifecycleState.unified
        return projection
