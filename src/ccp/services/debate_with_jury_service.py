import uuid
from datetime import datetime, timedelta
from typing import Optional

from src.ccp.models.reaction_debate_models import (
    DebateStance,
    JuryVoteStatus,
    AudienceJuryInlineVote,
    VoteThenReactPrompt,
    DebateVsArtifactProjection,
    DebateCounterTakeIntent
)
from src.ccp.models.ca11_models import ContentMachineResult
from src.ccp.services.content_machine import ContentMachinePipeline
# from src.ccp.services.canvas_composition_service import CanvasCompositionService

class AudienceJuryWebhookAdapter:
    """Parses and handles inline jury votes from Telegram callbacks."""
    
    @staticmethod
    def parse_and_validate_callback(callback_data: str, user_id: str) -> Optional[AudienceJuryInlineVote]:
        # Parse "vote:debate_id:artifact_id:voted_side"
        parts = callback_data.split(":")
        if len(parts) == 4 and parts[0] == "vote":
            return AudienceJuryInlineVote(
                vote_id=str(uuid.uuid4()),
                debate_id=parts[1],
                artifact_id=parts[2],
                voter_person_id=user_id,
                voted_side=DebateStance(parts[3]),
                callback_token=callback_data,
                status=JuryVoteStatus.accepted,
                opens_mini_app=False,
                registered_at=datetime.utcnow()
            )
        return None

class VoteThenReactPromptBuilder:
    """Builds the deep link and tethered copy after a successful vote."""
    
    @staticmethod
    def build_prompt(vote: AudienceJuryInlineVote) -> VoteThenReactPrompt:
        stance_str = vote.voted_side.value
        copy = f"You voted {stance_str.upper()}. Do you want to defend your position and record a counter-take?"
        return VoteThenReactPrompt(
            prompt_id=str(uuid.uuid4()),
            source_vote_id=vote.vote_id,
            selected_stance=vote.voted_side,
            prompt_copy=copy,
            cta_label="Defend Your Vote",
            deep_link_url=f"https://t.me/ccp_bot/debate?startapp=react_debate&stance={stance_str}",
            expires_at=datetime.utcnow() + timedelta(hours=24)
        )

class DebateContentRoutingAdapter:
    """Adapts a DebateVsArtifactProjection into a CMF session report."""
    @staticmethod
    def adapt(projection: DebateVsArtifactProjection) -> dict:
        return {
            "topic": projection.root_artifact.topic.id if projection.root_artifact.topic else "unknown",
            "primary_speaker": projection.root_artifact.person_id,
            "context_payload": {
                "format": "debate_vs",
                "tally_for": projection.tally_for,
                "tally_against": projection.tally_against,
                "stances": ["for", "against"]
            },
            "audio_assets": [
                projection.root_artifact.id,
                projection.counter_artifact.id if projection.counter_artifact else None
            ]
        }

class DebateWithJuryService:
    def __init__(self, content_machine_pipeline: ContentMachinePipeline):
        self.cmf_pipeline = content_machine_pipeline
        # self.canvas_service = canvas_composition_service
        
    def process_jury_vote(self, callback_data: str, user_id: str) -> Optional[VoteThenReactPrompt]:
        vote = AudienceJuryWebhookAdapter.parse_and_validate_callback(callback_data, user_id)
        if not vote:
            return None
        # Mocking persistence deduplication:
        # In a real impl, we check Redis. Here we assume success.
        vote.status = JuryVoteStatus.accepted
        return VoteThenReactPromptBuilder.build_prompt(vote)

    def create_counter_take_intent(self, payload: dict) -> DebateCounterTakeIntent:
        # Visual Adversary Rule (Phase2-M05): strictly require a side
        stance = payload.get("selected_stance")
        if stance not in ["for", "against"]:
            raise ValueError("Neutral or missing stance is not allowed for counter-take.")
            
        return DebateCounterTakeIntent(
            debate_id=payload["debate_id"],
            source_artifact_id=payload["source_artifact_id"],
            selected_stance=DebateStance(stance)
        )

    async def publish_debate(self, projection: DebateVsArtifactProjection, coach_id: str) -> DebateVsArtifactProjection:
        # Evaluate Gate 1: Visual Adversary Rule
        if projection.render_format != "split_screen_vs":
            projection.visual_adversary_passed = False
            projection.public_share_ready = False
            return projection
            
        # Compose Canvas VS (Mocked)
        projection.visual_adversary_passed = True
        projection.public_share_ready = True
        
        # Route to CMF
        report = DebateContentRoutingAdapter.adapt(projection)
        try:
            res = await self.cmf_pipeline.process_session(report, coach_id)
            projection.content_machine_result = res
        except Exception:
            pass # Fails gracefully, remains shareable
            
        return projection
