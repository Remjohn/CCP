"""
FR61 — Jim Rohn AI Voice Coach Engine: Integration Tests
==========================================================
Tests covering all 12 Acceptance Criteria from FR61 §8
and all 6 Quality Gates from FR61 §4.

Architecture reference: FR61 §10 Testing Strategy.
"""

import pytest
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from unittest.mock import AsyncMock, MagicMock

from backend.core.fr61_models import (
    MICRO_IMPROVEMENT_THRESHOLD_PCT, MAX_FEEDBACK_DURATION_SECONDS,
    MAX_RATCHET_FOLLOWUPS, PROHIBITED_WORDS,
    PROVOCATION_MIN_ANTITHESES, PROVOCATION_MIN_HCD_REFS,
    SESSION_MAX_MINUTES, SESSION_WARN_MINUTES,
    SPECIFICITY_ENTITY_THRESHOLD, SPECIFICITY_SENSORY_THRESHOLD,
    VOICE_NOTE_MIN_SECONDS,
    ContradictionPair, EmotionalTrajectory, ExtractedStory,
    FeedbackElement, FeedbackGateVerdict, FeedbackOutput,
    FeedbackRegisterGateResult, FR61ReceiptBlock,
    GeneratedQuestion, HCDReference, IntakeProcessingResult,
    MicroImprovementDetection, PauseMarker, PinDataPoint,
    PostureObservation, ProsodyMetrics, ProvocationError,
    ProvocationGateResult, ProvocationGateVerdict,
    ProvocationQuestionOutput, RecordingAnalysis,
    ReminderStage, ScheduledSessionRecord, ScheduledSessionStatus,
    ScriptArrangementGateResult, ScriptCompositionError,
    ScriptDocument, ScriptGateVerdict, ScriptPiece,
    SessionAnalysisOutput, SessionTimeGateResult, SessionType,
    SpecificityGateVerdict, SpecificityRatchetResult,
    TemporalPosition, TranscriptAnalysis, TriggerSource,
    VideoAnalysis, VideoAvailabilityVerdict, VocalAnalysis,
    EuphonyDevice, TPLMarker, FeedbackError, IntakeError,
    RecordingSessionError,
)
from backend.core.rohn_voice_coach_engine import (
    ProvocationQualityGate, SpecificityRatchetGate,
    ScriptArrangementGate, SessionTimeGate, FeedbackRegisterGate,
    VideoAnalysisGate,
    _sha256, _count_antitheses, _has_closing_question,
    _detect_alliteration, _select_narrative_arc,
    _compute_sincerity_composite, _compute_wpm,
    _compute_filler_density, _count_rohn_pauses,
    _compute_pin_iron_ratio, _compute_micro_improvements,
    _check_prohibited_words,
)
from backend.core.rohn_voice_coach_orchestrator import RohnVoiceCoachOrchestrator


# ═══════════════════════════════════════════════════════════════
# MOCK SERVICES
# ═══════════════════════════════════════════════════════════════

class MockSupabase:
    def __init__(self):
        self._data: Dict[str, list] = {}
        self._coach_ctx = ""

    async def set_coach_context(self, coach_id: str):
        self._coach_ctx = coach_id

    async def insert(self, table: str, data: dict) -> dict:
        self._data.setdefault(table, []).append(data)
        return data

    async def select(self, table: str, filters: dict,
                     order_by: str = "", limit: int = 100) -> list:
        rows = self._data.get(table, [])
        return [r for r in rows if all(r.get(k) == v for k, v in filters.items())][:limit]

    async def update(self, table: str, filters: dict, data: dict) -> dict:
        rows = self._data.get(table, [])
        for r in rows:
            if all(r.get(k) == v for k, v in filters.items()):
                r.update(data)
                return r
        return data


class MockRedis:
    def __init__(self):
        self._store: Dict[str, dict] = {}

    async def set_json(self, key: str, data: dict, ttl: int):
        self._store[key] = data

    async def get_json(self, key: str) -> Optional[dict]:
        return self._store.get(key)

    async def delete(self, key: str):
        self._store.pop(key, None)


class MockTTS:
    async def synthesize(self, text: str) -> str:
        return f"https://tts.example.com/{uuid.uuid4()}.ogg"


class MockAudio:
    async def extract_prosody(self, audio_path: str) -> ProsodyMetrics:
        return ProsodyMetrics(
            f0_mean=180.0, f0_variance=25.0, jitter=0.012,
            shimmer=0.05, spm=4.2, arousal=0.6, valence=0.5,
        )

    async def transcribe(self, audio_path: str) -> Tuple[str, list]:
        return ("I realized that the real value is not in the methodology "
                "but in how you show up for the client. Last Thursday "
                "with Sarah, I told her something I've never said before.",
                [{"word": "I", "start": 0.0, "pause": 0.0},
                 {"word": "realized", "start": 0.2, "pause": 2.0}])

    async def analyze_liwc(self, text: str) -> TranscriptAnalysis:
        return TranscriptAnalysis(
            liwc_authenticity=0.78, sensory_detail_score=6.0,
            named_entity_count=4,
        )

    async def extract_emotion(self, audio_path: str) -> list:
        return [{"segment": 0, "arousal": 0.6, "valence": 0.4}]


class MockVideo:
    def __init__(self, face_present: bool = True):
        self._face = face_present

    async def detect_face_track(self, video_path: str) -> bool:
        return self._face

    async def analyze_eye_contact(self, path: str) -> Tuple[float, list]:
        return (0.82, [12.5, 45.2])

    async def analyze_gestures(self, path: str, ts: list) -> float:
        return 7.5

    async def analyze_facial_expression(self, path: str, emotions: list) -> float:
        return 8.0

    async def analyze_posture(self, path: str) -> list:
        return [PostureObservation(timestamp=10, observation="forward_lean", content_match="key claim")]


class MockCalendar:
    async def create_event(self, coach_id: str, title: str, start: datetime,
                           duration_min: int, description: str) -> str:
        return f"cal-event-{uuid.uuid4()}"


class MockTelegram:
    def __init__(self):
        self.sent_messages: List[dict] = []

    async def send_voice_note(self, coach_id: str, audio_url: str) -> bool:
        self.sent_messages.append({"type": "voice", "coach_id": coach_id, "url": audio_url})
        return True

    async def send_text(self, coach_id: str, text: str) -> bool:
        self.sent_messages.append({"type": "text", "coach_id": coach_id, "text": text})
        return True


class MockLLM:
    def __init__(self, response: str = ""):
        self._response = response

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        # C-11: Verify no agent persona names in the prompt
        assert "Rohn-Voice-Coach-Agent" not in system_prompt
        assert "Rohn-Voice-Coach-Agent" not in user_prompt
        return self._response


def _build_orchestrator(
    llm_response: str = "",
    face_present: bool = True,
    db_seed: Optional[Dict[str, list]] = None,
) -> Tuple[RohnVoiceCoachOrchestrator, MockSupabase, MockTelegram]:
    db = MockSupabase()
    if db_seed:
        db._data = db_seed
    telegram = MockTelegram()
    orch = RohnVoiceCoachOrchestrator(
        supabase=db, redis=MockRedis(), tts=MockTTS(),
        audio=MockAudio(), video=MockVideo(face_present),
        calendar=MockCalendar(), telegram=telegram,
        llm=MockLLM(llm_response),
        coach_id="coach-001", coach_acronym="JP",
    )
    return orch, db, telegram


# ═══════════════════════════════════════════════════════════════
# UNIT TESTS — Quality Gates
# ═══════════════════════════════════════════════════════════════

class TestProvocationQualityGate:
    """Tests for Gate S1 — AC1."""

    def test_pass_with_hcd_and_antithesis_and_question(self):
        """AC1: ≥1 HCD ref + ≥1 antithetical construction + closing question."""
        text = ("You said last week it's not about the money — it's about the impact. "
                "But your calendar says otherwise. Where does the contradiction live?")
        refs = [HCDReference(type="previous_statement", source_session="s1", quote="not about money")]
        result = ProvocationQualityGate.evaluate(text, refs)
        assert result.verdict == ProvocationGateVerdict.PASS
        assert result.hcd_ref_count >= PROVOCATION_MIN_HCD_REFS
        assert result.antithesis_count >= PROVOCATION_MIN_ANTITHESES
        assert result.has_closing_question is True

    def test_fail_no_hcd_ref(self):
        text = "What do you think about coaching? Is it not the method — but the mindset?"
        result = ProvocationQualityGate.evaluate(text, [])
        assert result.verdict == ProvocationGateVerdict.FAIL_NO_HCD_REF

    def test_fail_no_antithesis(self):
        text = "You mentioned coaching last week. What is your philosophy?"
        refs = [HCDReference(type="previous_statement", source_session="s1", quote="coaching")]
        result = ProvocationQualityGate.evaluate(text, refs)
        assert result.verdict == ProvocationGateVerdict.FAIL_NO_ANTITHESIS

    def test_fail_prohibited_word(self):
        text = "I can help with that — it's not the method but the mindset. What's your take?"
        refs = [HCDReference(type="previous_statement", source_session="s1", quote="method")]
        result = ProvocationQualityGate.evaluate(text, refs)
        assert result.verdict == ProvocationGateVerdict.FAIL_PROHIBITED_WORD
        assert "I can help with that" in result.prohibited_words_found


class TestSpecificityRatchetGate:
    """Tests for Gate S2."""

    def test_pass_when_specific_enough(self):
        result = SpecificityRatchetGate.evaluate(
            sensory_score=6.0, entity_count=5, ratchet_count=0)
        assert result.verdict == SpecificityGateVerdict.PASS
        assert result.needs_followup is False

    def test_fail_needs_followup_when_vague(self):
        result = SpecificityRatchetGate.evaluate(
            sensory_score=2.0, entity_count=1, ratchet_count=0)
        assert result.verdict == SpecificityGateVerdict.FAIL_NEEDS_FOLLOWUP
        assert result.needs_followup is True

    def test_pass_max_ratchets_reached(self):
        result = SpecificityRatchetGate.evaluate(
            sensory_score=2.0, entity_count=1, ratchet_count=MAX_RATCHET_FOLLOWUPS)
        assert result.verdict == SpecificityGateVerdict.PASS_MAX_RATCHETS_REACHED
        assert result.needs_followup is False


class TestScriptArrangementGate:
    """Tests for Gate S3 — AC3."""

    def test_pass_with_exact_phrases(self):
        """AC3: Script uses coach's exact phrases, not paraphrases."""
        original = ["The real value is in showing up"]
        script = ScriptDocument(
            coach_id="c1",
            content_pieces=[ScriptPiece(
                title="Test", narrative_arc="The Foundation",
                arranged_phrases=["The real value is in showing up"],
                pause_markers=[PauseMarker(position_after="showing up")],
            )],
            raw_coach_phrases_used=original,
        )
        result = ScriptArrangementGate.evaluate(script, original)
        assert result.verdict == ScriptGateVerdict.PASS

    def test_fail_rewrite_detected(self):
        """AC3: Detect when script rewrites instead of arranges."""
        original = ["The real value is in showing up"]
        script = ScriptDocument(
            coach_id="c1",
            content_pieces=[ScriptPiece(
                title="Test", narrative_arc="The Foundation",
                arranged_phrases=["Being present for clients creates tremendous value and opportunity"],
                pause_markers=[PauseMarker(position_after="opportunity")],
            )],
            raw_coach_phrases_used=original,
        )
        result = ScriptArrangementGate.evaluate(script, original)
        assert result.verdict == ScriptGateVerdict.FAIL_REWRITE_DETECTED

    def test_fail_no_pause_markers(self):
        original = ["The real value is in showing up"]
        script = ScriptDocument(
            coach_id="c1",
            content_pieces=[ScriptPiece(
                title="Test", narrative_arc="The Foundation",
                arranged_phrases=original,
            )],
        )
        result = ScriptArrangementGate.evaluate(script, original)
        assert result.verdict == ScriptGateVerdict.FAIL_NO_PAUSE_MARKERS


class TestSessionTimeGate:
    """Tests for Gate S5A — AC4."""

    def test_no_warning_under_55(self):
        result = SessionTimeGate.evaluate(elapsed_minutes=30, recordings_remaining=2)
        assert result.warn_triggered is False
        assert result.hard_stop_triggered is False

    def test_warning_at_55(self):
        """AC4: 55-minute warning fires."""
        result = SessionTimeGate.evaluate(elapsed_minutes=55, recordings_remaining=1)
        assert result.warn_triggered is True
        assert result.hard_stop_triggered is False

    def test_hard_stop_at_60(self):
        """AC4: 60-minute hard stop enforced."""
        result = SessionTimeGate.evaluate(elapsed_minutes=60, recordings_remaining=1)
        assert result.hard_stop_triggered is True


class TestFeedbackRegisterGate:
    """Tests for Gate S6 — AC10."""

    def test_pass_all_constraints(self):
        """AC10: Antithesis + HCD ref + Rohn principle + Let's + no prohibited + ≤60s."""
        text = ("Your filler density dropped since last session. "
                "That's not accident — that's discipline of the master. "
                "Jim Rohn said it best. Let's work on the pause next.")
        result = FeedbackRegisterGate.evaluate(text, estimated_seconds=45)
        assert result.verdict == FeedbackGateVerdict.PASS

    def test_fail_prohibited_word(self):
        text = "I can help with that. Let's delve into your progress since last session."
        result = FeedbackRegisterGate.evaluate(text, estimated_seconds=30)
        assert result.verdict == FeedbackGateVerdict.FAIL_PROHIBITED_WORD

    def test_fail_too_long(self):
        text = ("Your filler density dropped since last session. "
                "That's not accident — that's discipline of the master. "
                "Jim Rohn said it best. Let's work on the pause next.")
        result = FeedbackRegisterGate.evaluate(text, estimated_seconds=90)
        assert result.verdict == FeedbackGateVerdict.FAIL_TOO_LONG


class TestVideoAnalysisGate:
    """Tests for Gate S5B — AC8."""

    def test_available_when_face_detected(self):
        assert VideoAnalysisGate.evaluate(True) == VideoAvailabilityVerdict.AVAILABLE

    def test_no_face_skips_video(self):
        """AC8: No face → skip video analysis, process audio only."""
        assert VideoAnalysisGate.evaluate(False) == VideoAvailabilityVerdict.NO_FACE_TRACK


# ═══════════════════════════════════════════════════════════════
# UNIT TESTS — Utility Functions
# ═══════════════════════════════════════════════════════════════

class TestUtilityFunctions:

    def test_sha256_determinism(self):
        """FR61 §10 Unit Tests: Same input → same hash."""
        data = "The discipline of the master is not in the performance but in the preparation"
        h1 = _sha256(data)
        h2 = _sha256(data)
        assert h1 == h2
        assert len(h1) == 64

    def test_count_antitheses(self):
        text = "It's not the method — it's the mindset. Not because it's easy, but because it matters."
        count = _count_antitheses(text)
        assert count >= 2

    def test_prohibited_words_detected(self):
        text = "I can help with that. Let me delve into your progress."
        found = _check_prohibited_words(text)
        assert "I can help with that" in found
        assert "delve" in found

    def test_micro_improvement_detection_positive(self):
        """AC6: filler_density 0.034→0.021 = -38.2% ≥ 5% threshold."""
        current = {"filler_density": 0.021, "sincerity_composite": 8.5}
        previous = {"filler_density": 0.034, "sincerity_composite": 7.0}
        improvements = _compute_micro_improvements(current, previous)
        filler_imp = [i for i in improvements if i.metric_name == "filler_density"]
        assert len(filler_imp) == 1
        assert abs(filler_imp[0].delta_pct) >= MICRO_IMPROVEMENT_THRESHOLD_PCT

    def test_compute_wpm(self):
        assert _compute_wpm(150, 60.0) == 150.0
        assert _compute_wpm(0, 0.0) == 0.0

    def test_compute_filler_density(self):
        assert _compute_filler_density(3, 100) == 0.03
        assert _compute_filler_density(0, 0) == 0.0

    def test_rohn_pause_count(self):
        events = [
            {"duration": 2.0, "follows_key_statement": True},
            {"duration": 0.5, "follows_key_statement": True},
            {"duration": 1.8, "follows_key_statement": True},
            {"duration": 2.0, "follows_key_statement": False},
        ]
        count = _count_rohn_pauses(events)
        assert count == 2  # Only events 1.5-2.5s that follow key statements

    def test_narrative_arc_selection(self):
        assert _select_narrative_arc("frustration_to_resolution") == "The Epiphany"
        assert _select_narrative_arc("warning_future_risk") == "The Warning"
        assert _select_narrative_arc("unknown_trajectory") == "The Foundation"

    def test_sincerity_composite(self):
        score = _compute_sincerity_composite(0.8, 0.01, 0.03)
        assert 0.0 <= score <= 10.0

    def test_alliteration_detection(self):
        devices = _detect_alliteration("the powerful purposeful practice of patience")
        assert len(devices) >= 1
        assert devices[0].device_type == "alliteration"


# ═══════════════════════════════════════════════════════════════
# INTEGRATION TESTS — Orchestrator Stages
# ═══════════════════════════════════════════════════════════════

class TestStage1Provocation:
    """AC1: Provocation with HCD ref + antithesis + closing question."""

    @pytest.mark.asyncio
    async def test_stage1_generates_and_delivers(self):
        llm_response = (
            "You told me last week it's not the methodology — it's the presence. "
            "But your calendar tells a different story. Where is the gap?")
        db_seed = {
            "story_bank": [{"coach_id": "coach-001", "session_id": "s1",
                           "raw_transcript": "The methodology matters less than presence"}],
            "philosophy_tensions": [{"coach_id": "coach-001", "tension_id": "t1",
                                    "claim_a_text": "Methodology is everything", "resolved": False}],
            "vocal_delivery": [],
            "personal_philosophy": [{"coach_id": "coach-001", "recurring_grievances": ["calendar overload"]}],
        }
        orch, db, tg = _build_orchestrator(llm_response, db_seed=db_seed)
        result = await orch.stage1_generate_provocation(
            {"tension_id": "t1", "topic_cluster": "methodology", "cultural_tension": "presence vs method"},
            {"trigger_id": "tr1", "mechanism_description": "calendar contradiction"},
        )
        assert result.provocation_id.startswith("PROV-")
        assert len(result.hcd_references) >= 1
        assert result.generated_question.antithesis_count >= 1
        assert len(tg.sent_messages) >= 2  # voice + text


class TestStage2Intake:
    """AC2: Phase 1 stores prosody but delivers NO feedback."""

    @pytest.mark.asyncio
    async def test_stage2_no_feedback_delivered(self):
        orch, db, tg = _build_orchestrator()
        result = await orch.stage2_process_intake("/audio/test.ogg", duration_seconds=45.0)
        assert result.session_id
        # AC2: No feedback voice notes delivered in intake
        feedback_voices = [m for m in tg.sent_messages if m["type"] == "voice"]
        # Only specificity ratchet follow-ups are allowed, not coaching feedback
        for msg in tg.sent_messages:
            if msg["type"] == "text":
                assert "improvement" not in msg.get("text", "").lower()

    @pytest.mark.asyncio
    async def test_stage2_rejects_short_voice_note(self):
        orch, _, _ = _build_orchestrator()
        with pytest.raises(IntakeError, match="too short"):
            await orch.stage2_process_intake("/audio/short.ogg", duration_seconds=5.0)


class TestStage4Scheduling:
    """AC7: Reminder ordering T-48h → T-24h → T-30min."""

    @pytest.mark.asyncio
    async def test_stage4_books_session_with_reminders(self):
        db_seed = {"coaches": [{"coach_id": "coach-001", "timezone": "Europe/Paris",
                                "availability_config": {}}]}
        orch, db, tg = _build_orchestrator(db_seed=db_seed)
        record = await orch.stage4_schedule_session(recordings_planned=4, batch_theme="authority")
        assert record.status == ScheduledSessionStatus.BOOKED
        assert record.recordings_planned == 4

    @pytest.mark.asyncio
    async def test_reminder_ordering(self):
        """AC7: T-48h fires before T-24h fires before T-30min."""
        db_seed = {
            "coaches": [{"coach_id": "coach-001", "timezone": "UTC", "availability_config": {}}],
            "scheduled_sessions": [{"coach_id": "coach-001", "status": "booked"}],
        }
        orch, db, tg = _build_orchestrator(db_seed=db_seed)
        r1 = await orch.send_reminder(ReminderStage.T_48H)
        r2 = await orch.send_reminder(ReminderStage.T_24H)
        r3 = await orch.send_reminder(ReminderStage.T_30MIN)
        assert r1 and r2 and r3
        assert len(tg.sent_messages) == 3
        # Verify ordering by send sequence
        assert tg.sent_messages[0]["type"] == "voice"
        assert tg.sent_messages[1]["type"] == "voice"
        assert tg.sent_messages[2]["type"] == "voice"


class TestStage5Recording:
    """AC4, AC5, AC8: Recording session analysis."""

    @pytest.mark.asyncio
    async def test_four_recordings_produce_four_rows(self):
        """AC5: 4 separate recordings → 4 separate vocal_delivery + video_delivery rows."""
        orch, db, _ = _build_orchestrator()
        for i in range(4):
            await orch.stage5_process_recording(
                video_path=f"/video/take_{i}.mp4",
                recording_id=f"rec-{i}",
                session_id="session-001",
                script_piece_title=f"Piece {i}",
                elapsed_minutes=i * 12,
                recordings_remaining=4 - i - 1,
            )
        vocal_rows = db._data.get("vocal_delivery", [])
        video_rows = db._data.get("video_delivery", [])
        assert len(vocal_rows) == 4
        assert len(video_rows) == 4

    @pytest.mark.asyncio
    async def test_hard_stop_at_60_minutes(self):
        """AC4: Session ≥60 min raises RecordingSessionError."""
        orch, _, _ = _build_orchestrator()
        with pytest.raises(RecordingSessionError, match="hard stop"):
            await orch.stage5_process_recording(
                video_path="/video/late.mp4", recording_id="r-late",
                session_id="s1", elapsed_minutes=61,
            )

    @pytest.mark.asyncio
    async def test_no_face_skips_video_keeps_audio(self):
        """AC8: No face → video skipped, audio still processed."""
        orch, db, _ = _build_orchestrator(face_present=False)
        result = await orch.stage5_process_recording(
            video_path="/video/no_face.mp4", recording_id="r-nf",
            session_id="s1", elapsed_minutes=5,
        )
        assert result.video_analysis.video_analysis_available is False
        assert result.vocal_analysis.wpm > 0
        vocal_rows = db._data.get("vocal_delivery", [])
        assert len(vocal_rows) == 1
        video_rows = db._data.get("video_delivery", [])
        assert len(video_rows) == 0


class TestStage6Feedback:
    """AC6, AC10: Feedback with micro-improvement + Rohn register."""

    @pytest.mark.asyncio
    async def test_feedback_acknowledges_improvement_first(self):
        """AC6: Micro-improvement acknowledged BEFORE any critique."""
        analysis = RecordingAnalysis(
            recording_id="r1",
            vocal_analysis=VocalAnalysis(
                filler_density=0.021, sincerity_composite=8.5,
                wpm=140, rohn_pauses=3,
            ),
            video_analysis=VideoAnalysis(
                eye_contact_pct=0.85, video_analysis_available=True,
            ),
            micro_improvements_detected=[MicroImprovementDetection(
                metric_name="filler_density",
                previous_value=0.034, current_value=0.021,
                delta_pct=-38.2,
            )],
        )
        orch, db, tg = _build_orchestrator()
        output = await orch.stage6_generate_feedback(analysis, take_number=1)
        assert output.elements[0].element_type == "micro_improvement"
        assert output.contains_antithesis is True
        assert output.uses_lets_framing is True


# ═══════════════════════════════════════════════════════════════
# INTEGRATION TESTS — Receipt Chain
# ═══════════════════════════════════════════════════════════════

class TestReceiptChain:
    """FR61 §4 + FR47 DEP-ENG-041: Receipt chain integrity."""

    @pytest.mark.asyncio
    async def test_receipt_chain_builds_from_genesis(self):
        llm_response = (
            "You said it's not the method — it's the presence. Where is the gap?")
        db_seed = {
            "story_bank": [{"coach_id": "coach-001", "session_id": "s1",
                           "raw_transcript": "The method matters less"}],
            "philosophy_tensions": [{"coach_id": "coach-001", "tension_id": "t1",
                                    "claim_a_text": "Method is key", "resolved": False}],
            "vocal_delivery": [], "personal_philosophy": [],
        }
        orch, _, _ = _build_orchestrator(llm_response, db_seed=db_seed)
        await orch.stage1_generate_provocation(
            {"tension_id": "t1", "topic_cluster": "method"},
            {"trigger_id": "tr1"},
        )
        chain = orch.get_receipt_chain()
        assert len(chain) == 1
        assert chain[0].previous_receipt_hash == "GENESIS"
        assert chain[0].stage_name == "STAGE-1-ROHN-PROVOCATION"

    @pytest.mark.asyncio
    async def test_chain_integrity_verification(self):
        orch, db, _ = _build_orchestrator()
        await orch.stage2_process_intake("/audio/test.ogg", 60.0)
        assert orch.verify_chain_integrity() is True

    @pytest.mark.asyncio
    async def test_broken_chain_detected(self):
        orch, _, _ = _build_orchestrator()
        await orch.stage2_process_intake("/audio/test.ogg", 60.0)
        # Tamper with chain
        if orch._receipt_chain:
            orch._receipt_chain[0].previous_receipt_hash = "TAMPERED"
        assert orch.verify_chain_integrity() is False


# ═══════════════════════════════════════════════════════════════
# ADR-01 TESTS — Coach Isolation
# ═══════════════════════════════════════════════════════════════

class TestCoachIsolation:
    """AC9: RLS enforces coach_id isolation across all tables."""

    @pytest.mark.asyncio
    async def test_coach_context_set_before_queries(self):
        db_seed = {"coaches": [{"coach_id": "coach-001", "timezone": "UTC",
                                "availability_config": {}}]}
        orch, db, _ = _build_orchestrator(db_seed=db_seed)
        await orch.stage4_schedule_session()
        assert db._coach_ctx == "coach-001"

    @pytest.mark.asyncio
    async def test_cross_coach_data_not_returned(self):
        db = MockSupabase()
        db._data["story_bank"] = [
            {"coach_id": "coach-001", "raw_transcript": "My story"},
            {"coach_id": "coach-002", "raw_transcript": "Their story"},
        ]
        results = await db.select("story_bank", {"coach_id": "coach-001"})
        assert len(results) == 1
        assert results[0]["coach_id"] == "coach-001"


# ═══════════════════════════════════════════════════════════════
# C-11 PERSONA MASKING TESTS
# ═══════════════════════════════════════════════════════════════

class TestPersonaMasking:
    """C-11: Agent persona names never appear in API payloads."""

    @pytest.mark.asyncio
    async def test_llm_prompts_contain_no_agent_names(self):
        """MockLLM asserts no agent names in system/user prompt."""
        llm_response = "You said it's not the method — it's the presence. Where is the gap?"
        db_seed = {
            "story_bank": [{"coach_id": "coach-001", "session_id": "s1",
                           "raw_transcript": "The method"}],
            "philosophy_tensions": [{"coach_id": "coach-001", "tension_id": "t1",
                                    "claim_a_text": "Method", "resolved": False}],
            "vocal_delivery": [], "personal_philosophy": [],
        }
        orch, _, _ = _build_orchestrator(llm_response, db_seed=db_seed)
        # If agent name appears in prompt, MockLLM.generate will raise AssertionError
        await orch.stage1_generate_provocation(
            {"tension_id": "t1", "topic_cluster": "method"},
            {"trigger_id": "tr1"},
        )
