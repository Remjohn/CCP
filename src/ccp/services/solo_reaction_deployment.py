from typing import Any, Dict
from datetime import datetime

from src.ccp.models.reaction_solo_models import (
    SoloDeploymentDecision,
    SoloDeploymentProjection,
)
from src.ccp.models.reaction_engine_models import ReactionArtifactRecord, ReactionScoreCard
from src.ccp.services.content_machine import ContentMachinePipeline
from src.ccp.models.ca11_models import ContentMachineResult


class ReactionToSessionReportAdapter:
    """Adapts a CORE reaction artifact and scorecard into a CMF session report."""
    
    @staticmethod
    def adapt(artifact: ReactionArtifactRecord, scorecard: ReactionScoreCard) -> Dict[str, Any]:
        return {
            "source_artifact_id": artifact.id,
            "session_id": artifact.session_id,
            "key_insights": [beat for beat in scorecard.semantic_beats if beat.score >= 0.8],
            "breakthrough_moments": [
                {"timestamp": ev.timestamp, "description": ev.description}
                for ev in scorecard.evidence
            ],
            "emotional_beats": {
                "conviction_trajectory": scorecard.conviction_trajectory,
                "pacing_trajectory": scorecard.pacing_trajectory
            },
            "overall_score": scorecard.overall_score
        }

class SoloReactionDeploymentService:
    def __init__(self, content_machine_pipeline: ContentMachinePipeline):
        self.cmf_pipeline = content_machine_pipeline
        
    async def deploy_artifact(
        self, 
        artifact: ReactionArtifactRecord, 
        scorecard: ReactionScoreCard, 
        coach_id: str, 
        coach_acronym: str = "CCH"
    ) -> SoloDeploymentProjection:
        # Gate: Earned Export Gate (Phase2-M04)
        if scorecard.conviction_score < 0.85:
            return SoloDeploymentProjection(
                artifact_id=artifact.id,
                decision=SoloDeploymentDecision.redemption_required,
                queue_status="not_queued"
            )
            
        session_report = ReactionToSessionReportAdapter.adapt(artifact, scorecard)
        
        try:
            # Route to CMF
            cmf_result: ContentMachineResult = await self.cmf_pipeline.process_session(
                session_report=session_report,
                coach_id=coach_id,
                coach_acronym=coach_acronym
            )
            
            # Surface truthful status
            return SoloDeploymentProjection(
                artifact_id=artifact.id,
                decision=SoloDeploymentDecision.deployed_to_cmf,
                content_machine_result=cmf_result,
                queue_status="queued" if cmf_result.status == "processing" else "delivered",
                delivery_eta_minutes=20,
                delivered_at=datetime.utcnow() if cmf_result.status == "delivered" else None
            )
            
        except Exception:
            return SoloDeploymentProjection(
                artifact_id=artifact.id,
                decision=SoloDeploymentDecision.pending_cmf_retry,
                queue_status="failed_retryable"
            )
