from src.ccp.models.experience_ladder_models import RouteDecisionPacket, InlineRewardPacket
from uuid import uuid4
from datetime import datetime

class InlineRewardComposer:
    def compose(self, decision: RouteDecisionPacket) -> InlineRewardPacket:
        return InlineRewardPacket(
            reward_id=str(uuid4()),
            client_id=decision.client_id,
            surface=decision.to_surface,
            next_step_type=decision.next_step_type,
            headline="Great Job!",
            body="You have unlocked the next drill.",
            voice_prompt_job="prompt_job",
            task_ticket_id=str(uuid4()),
            created_at=datetime.utcnow()
        )
