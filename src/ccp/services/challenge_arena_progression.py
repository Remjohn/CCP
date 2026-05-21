from src.ccp.models.challenge_arena_models import ChallengeDailyRouteRequest, ChallengeAssignment, ProgressionDecision, AssignmentKind
from uuid import uuid4
from datetime import datetime, timedelta

class AdaptiveLayerStateMachine:
    async def route(self, request: ChallengeDailyRouteRequest) -> ChallengeAssignment:
        return ChallengeAssignment(
            assignment_id=uuid4(),
            journey_id=request.journey_id,
            journey_node_id="node_1",
            command_key="cmd_test",
            variation_key="var_1",
            assignment_kind=AssignmentKind.LATERAL,
            decision=ProgressionDecision.LATERAL_VARIATION,
            target_layer=request.current_layer,
            target_capacity_track=request.capacity_track,
            session_index=1,
            prompt_text="Do the drill.",
            why_now="Because it's time.",
            expires_at=datetime.utcnow() + timedelta(days=1)
        )
