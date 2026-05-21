from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4
from src.ccp.models.cbcs_models import (
    CBCSEvidencePacket, CBCSSubmissionKind, EvidenceCitation, EvidenceMetric, SemanticDynamicsContext,
    CbcsPerceptualIntakeEnvelope,
)
from src.ccp.models.sda_models import FeedbackLoop, RecursivePattern


class CBCSEvidenceEngineService:
    """Extracts evidence from FR61 trait scoring, Change Talk Vault, SPT classification,
    and habit verification. Enriches with SDA longitudinal patterns."""

    def __init__(self, trait_scoring_engine: Any = None, change_talk_vault: Any = None, spt_stage_engine: Any = None, habit_architecture: Any = None, supabase_client: Any = None, receipt_chain: Any = None) -> None:
        self._trait_scoring = trait_scoring_engine
        self._change_talk = change_talk_vault
        self._spt_engine = spt_stage_engine
        self._habit_arch = habit_architecture
        self._supabase = supabase_client
        self._receipt_chain = receipt_chain

    async def extract_evidence(self, *, client_id: str, coach_id: str, submission_kind: CBCSSubmissionKind, transcript: str = "", perceptual_intake: Optional[CbcsPerceptualIntakeEnvelope] = None) -> CBCSEvidencePacket:
        now = datetime.now(timezone.utc)
        trait_metrics: list[EvidenceMetric] = []
        change_talk_summary: list[str] = []
        spt_stage = None
        habit_verified = None
        citations: list[EvidenceCitation] = []

        # FR61 trait scoring
        if self._trait_scoring is not None:
            try:
                scores = self._trait_scoring.score_all_traits(client_id=client_id, coach_id=coach_id)
                if scores and isinstance(scores, dict):
                    for name, value in scores.items():
                        trait_metrics.append(EvidenceMetric(metric_name=name, current_value=float(value), interpretation=f"FR61 score for {name}"))
                citations.append(EvidenceCitation(source_system="trait_scoring_engine", source_ref="score_all_traits", excerpt="FR61 biometric scoring"))
            except Exception:
                pass

        # Change Talk extraction
        if self._change_talk is not None:
            try:
                result = self._change_talk.extract(text=transcript, client_id=client_id, coach_id=coach_id)
                if result and hasattr(result, "top_statement") and result.top_statement:
                    change_talk_summary.append(result.top_statement.statement_text)
                citations.append(EvidenceCitation(source_system="change_talk_vault", source_ref="extract", excerpt="DARN-CAT commitment evidence"))
            except Exception:
                pass

        # SPT classification
        if self._spt_engine is not None:
            try:
                spt_result = self._spt_engine.classify_client(client_id=client_id, coach_id=coach_id)
                if spt_result and hasattr(spt_result, "spt_stage"):
                    spt_stage = spt_result.spt_stage
                citations.append(EvidenceCitation(source_system="spt_stage_engine", source_ref="classify_client", excerpt="Social Penetration Theory classification"))
            except Exception:
                pass

        # Habit verification
        if self._habit_arch is not None:
            try:
                habit_result = self._habit_arch.parse_and_verify(client_id=client_id, coach_id=coach_id)
                if habit_result and hasattr(habit_result, "verification_verdict"):
                    habit_verified = habit_result.verification_verdict == "PASS"
            except Exception:
                pass

        # SDA longitudinal patterns
        semantic_dynamics = SemanticDynamicsContext()
        if self._supabase is not None:
            try:
                ser_result = self._supabase.table("semantic_evolution_record").select("*").eq("client_id", client_id).eq("coach_id", coach_id).order("last_updated_at", desc=True).limit(1).execute()
                if ser_result and hasattr(ser_result, "data") and ser_result.data:
                    record = ser_result.data[0]
                    patterns_raw = record.get("recursive_patterns", [])
                    loops_raw = record.get("feedback_loops", [])
                    semantic_dynamics.active_recursive_patterns = [RecursivePattern(**p) if isinstance(p, dict) else p for p in patterns_raw]
                    semantic_dynamics.identified_feedback_loops = [FeedbackLoop(**l) if isinstance(l, dict) else l for l in loops_raw]
            except Exception:
                pass

        packet = CBCSEvidencePacket(
            evidence_packet_id=str(uuid4()), client_id=client_id, coach_id=coach_id,
            submission_kind=submission_kind, generated_at=now, trait_metrics=trait_metrics,
            change_talk_summary=change_talk_summary, spt_stage=spt_stage,
            habit_verified=habit_verified, citations=citations, semantic_dynamics=semantic_dynamics,
            perceptual_intake=perceptual_intake,
        )

        if self._receipt_chain is not None:
            self._receipt_chain.log(action="evidence-extraction", metadata={"evidence_packet_id": packet.evidence_packet_id, "client_id": client_id, "trait_count": len(trait_metrics), "perceptual_intake_present": perceptual_intake is not None})

        return packet

