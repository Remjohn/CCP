from typing import Optional
import uuid
from datetime import datetime, timedelta

from src.ccp.models.reaction_mirror_quiz_models import (
    MirrorQuizQuestionPack,
    MirrorQuizGenerationStatus,
    MirrorQuizReadinessStatus,
    AudienceMirrorQuestion,
    MirrorQuizEvidenceQuote
)

class MirrorQuizQuestionService:
    def __init__(self):
        pass

    def load_latest_cmm(self, coach_id: str) -> Optional[dict]:
        # Mock Supabase lookup: returning none simulates AC-6.3B blocked
        # To bypass, the test or handler provides a dict
        return None

    def load_story_archive(self, coach_id: str) -> Optional[dict]:
        return None

    def build_question_pack(self, coach_id: str, cmm_data: Optional[dict] = None) -> MirrorQuizQuestionPack:
        if not cmm_data or not cmm_data.get('operator_confirmed', False):
            return MirrorQuizQuestionPack(
                pack_id=str(uuid.uuid4()),
                coach_id=coach_id,
                cmm_id="blocked",
                generation_status=MirrorQuizGenerationStatus.BLOCKED_CMM_NOT_READY,
                readiness_status=MirrorQuizReadinessStatus.CMM_NOT_READY,
                receipt_id="none",
                issued_at=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(days=1),
                ttl_seconds=86400
            )
        
        # Valid CMM present
        entries = cmm_data.get('entries', [])
        valid_entries = [e for e in entries if e.get('approved', False)]
        
        if not valid_entries:
            return MirrorQuizQuestionPack(
                pack_id=str(uuid.uuid4()),
                coach_id=coach_id,
                cmm_id=cmm_data.get('cmm_id', 'unknown'),
                generation_status=MirrorQuizGenerationStatus.BLOCKED_NO_APPROVED_TENSIONS,
                readiness_status=MirrorQuizReadinessStatus.CMM_TOO_THIN,
                receipt_id="none",
                issued_at=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(days=1),
                ttl_seconds=86400
            )

        # Mocking an extracted question for AC-6.3A
        question = AudienceMirrorQuestion(
            question_id=f"{coach_id}-{cmm_data['cmm_id']}-tension1",
            ordinal=1,
            surface_text="How do you handle this complaint?",
            audience_verbatim=valid_entries[0]['verbatim'],
            primary_tension="complaint",
            coaching_intent="resolve_belief_conflict",
            evidence_quotes=[
                MirrorQuizEvidenceQuote(
                    evidence_id="e1",
                    cmm_id=cmm_data['cmm_id'],
                    layer_type="collective_wound",
                    source_material="sacred_audio_transcript",
                    quoted_text=valid_entries[0]['verbatim'],
                    normalized_tension="complaint",
                    selection_reason="direct quote"
                )
            ]
        )

        return MirrorQuizQuestionPack(
            pack_id=str(uuid.uuid4()),
            coach_id=coach_id,
            cmm_id=cmm_data['cmm_id'],
            generation_status=MirrorQuizGenerationStatus.DEGRADED_STORYLESS,
            readiness_status=MirrorQuizReadinessStatus.STORY_ARCHIVE_MISSING,
            questions=[question],
            receipt_id="receipt-1",
            issued_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=1),
            ttl_seconds=86400
        )
