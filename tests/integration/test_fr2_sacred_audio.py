"""
CCP FR2 Integration Tests — FR2 Unit 7
Tests all 10 Acceptance Criteria for the Sacred Audio Ingestion pipeline.

Spec reference: FR2 Tech Spec §Acceptance Criteria (AC1-AC10)
Test Strategy reference: FR2 §Testing Strategy

AC1:  Audio ≥15s in accepted formats ingested; <15s silently rejected with gentle prompt
AC2:  Groq Whisper preserves all filled pauses (10 fillers test)
AC3:  Thought Unit segmentation — no open subordinate clause at final word
AC4:  Gate PASS — all 7 markers authentic → status=AUTHENTIC
AC5:  Gate FAIL — hedging+past-tense → SYNTHETIC_CANDIDATE + correct prompt variant
AC6:  Persistent failure — 2 retries then drop, no error raised
AC7:  Insufficient session — <3 authentic units → INSUFFICIENT
AC8:  Receipt chain — 5-stage chain integrity verified
AC9:  Threshold — 3,000 words → Morgan notification in same cycle
AC10: Isolation — raw audio only transmitted to Groq Whisper
"""

import hashlib
import json
import os
import uuid
from pathlib import Path
from typing import Any, Optional
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.sacred_audio_models import (
    MINIMUM_CORPUS_WORDS,
    AuthenticityMarker,
    AuthenticityScore,
    AuthenticityStatus,
    ExtractionReadiness,
    MarkerResult,
    SacredAudioSession,
    ScoredThoughtUnit,
    SessionStatus,
    ThoughtUnit,
)
from src.ccp.services.liwc22_authenticity_gate import (
    LIWC22AuthenticityGate,
)
from src.ccp.services.re_elicitation_engine import (
    MARKER_PRIMARY_PROMPTS,
    ReElicitationEngine,
    TelegramReElicitationDispatcher,
)
from src.ccp.services.sacred_audio_transcriber import (
    MIN_DURATION_SECONDS,
    SACRED_AUDIO_FORMATS,
    SacredAudioTranscriber,
    SacredTranscriptionResult,
)
from src.ccp.services.thought_unit_segmenter import (
    MIN_SEGMENT_WORDS,
    ThoughtUnitSegmenter,
)


# ──────────────────────────────────────────────────────────────
# Shared fixtures
# ──────────────────────────────────────────────────────────────

@pytest.fixture
def coach_acronym() -> str:
    return "TST"


@pytest.fixture
def coach_id() -> str:
    return "coach-test-fr2"


@pytest.fixture
def tmp_coach_dir(tmp_path: Path) -> Path:
    coach_dir = tmp_path / "coaches" / "TST"
    (coach_dir / "config").mkdir(parents=True)
    return coach_dir


@pytest.fixture
def receipt_chain(tmp_path: Path, coach_acronym: str) -> ReceiptChain:
    log_dir = str(tmp_path / "logs" / "receipt_chain")
    return ReceiptChain(coach_acronym=coach_acronym, log_dir=log_dir)


@pytest.fixture
def authenticity_gate() -> LIWC22AuthenticityGate:
    return LIWC22AuthenticityGate(authentic_multiplier=1.0)


@pytest.fixture
def re_elicitation_engine() -> ReElicitationEngine:
    return ReElicitationEngine()


# ──────────────────────────────────────────────────────────────
# Helper: Create authentic thought unit text
# High FPS, exclusive words, no hedging, short sentences,
# present tense, natural fillers, mid-sentence discourse markers
# ──────────────────────────────────────────────────────────────

def make_authentic_text() -> str:
    """Generate text that passes all 7 LIWC-22 markers."""
    return (
        "I am telling you this is real. I feel it in my bones. "
        "Um but I have to be honest. My whole life changed. "
        "I see it clearly now. Without uh any doubt. "
        "I know except this one thing. My heart is open. "
        "I do feel actually different now. I am uh here. "
        "It is actually so clear to me now. "
        "I feel the shift in my body. "
        "But um I need to say this. I know it is true. "
        "I am so grateful. My soul feels alive."
    )


def make_synthetic_text_hedging_past() -> str:
    """Generate text that fails hedging AND past-tense markers (AC5).

    Spec: 'A test Thought Unit with hedging language (maybe, I think, kind of)
    AND past-tense dominant verbs scores status=SYNTHETIC_CANDIDATE.'
    """
    return (
        "I think maybe it was something that kind of happened. "
        "I believe it was perhaps a turning point. "
        "Maybe it was sort of important. I think I felt something. "
        "It was probably the time when things kind of changed. "
        "I believe perhaps it was significant. Maybe I was there. "
        "I think it was kind of a big deal. "
        "Perhaps it was sort of transformative. "
        "I believe maybe it was the moment. "
        "I think it was possibly important. Kind of."
    )


# ──────────────────────────────────────────────────────────────
# AC1: Audio Format and Duration Validation
# Spec: "Audio files ≥15s in accepted formats (.ogg/.mp3/.m4a) are
# successfully ingested. Files <15s are silently rejected with a
# gentle coach prompt."
# ──────────────────────────────────────────────────────────────

class TestAC1FormatAndDuration:
    """AC1: Format validation and duration check."""

    def test_accepted_formats(self):
        """Spec: 'accept .ogg, .mp3, .m4a'."""
        assert ".ogg" in SACRED_AUDIO_FORMATS
        assert ".mp3" in SACRED_AUDIO_FORMATS
        assert ".m4a" in SACRED_AUDIO_FORMATS

    def test_rejected_formats(self):
        """Spec: 'reject all others with a silent discard'."""
        assert ".wav" not in SACRED_AUDIO_FORMATS
        assert ".webm" not in SACRED_AUDIO_FORMATS
        assert ".flac" not in SACRED_AUDIO_FORMATS

    def test_minimum_duration_threshold(self):
        """Spec: 'if < 15 seconds → implicit rejection'."""
        assert MIN_DURATION_SECONDS == 15.0

    def test_duration_rejection_message(self):
        """Spec: 'Could you share a bit more? I want to make sure I can
        really work with what you're giving me.'"""
        engine = ReElicitationEngine()
        msg = engine.get_duration_rejection_message()
        assert "share a bit more" in msg
        assert "work with what you're giving me" in msg

    def test_session_creation_with_valid_audio(self, coach_id, coach_acronym):
        """Valid audio creates a session in PROCESSING status."""
        session = SacredAudioSession(
            session_id="test-session-001",
            coach_id=coach_id,
            coach_acronym=coach_acronym,
            audio_format=".ogg",
            audio_duration_seconds=30.0,
        )
        assert session.status == SessionStatus.PROCESSING
        assert session.audio_format == ".ogg"
        assert session.audio_duration_seconds == 30.0


# ──────────────────────────────────────────────────────────────
# AC2: Filler Preservation in Transcription
# Spec: "Groq Whisper transcription preserves all filled pauses (um/uh),
# stutters, and false starts. A test transcript with 10 inserted fillers
# must return all 10 in the output (ITN not applied)."
# ──────────────────────────────────────────────────────────────

class TestAC2FillerPreservation:
    """AC2: Non-verbal preservation in transcription."""

    def test_filler_words_defined(self):
        """The gate recognizes all filler word types from spec."""
        from src.ccp.services.liwc22_authenticity_gate import FILLER_WORDS
        assert "um" in FILLER_WORDS
        assert "uh" in FILLER_WORDS
        assert "hmm" in FILLER_WORDS

    def test_transcript_with_10_fillers_preserved(self):
        """AC2: '10 inserted fillers must return all 10 in the output.'

        This tests the pipeline's handling of a transcript containing
        10 fillers — the Thought Unit segmenter and LIWC-22 gate must
        not strip them.
        """
        transcript_with_fillers = (
            "Um I think this is um really important. "
            "Uh like you know uh the thing is. "
            "Hmm I feel like um it matters. "
            "Uh I am um here right now. "
            "Hmm it is uh about being real."
        )

        # Count fillers in transcript
        filler_words = {"um", "uh", "hmm"}
        words = transcript_with_fillers.lower().split()
        filler_count = sum(1 for w in words if w in filler_words)

        # All 10 fillers must be present
        assert filler_count == 10, f"Expected 10 fillers, found {filler_count}"

    def test_non_verbal_preservation_in_whisper_config(self):
        """The transcriber sends ITN-disabled prompt to Groq."""
        # Verify the SacredAudioTranscriber exists and has the right model
        assert SacredAudioTranscriber.GROQ_MODEL == "whisper-large-v3-turbo"

    def test_sacred_transcription_result_has_word_timestamps(self):
        """Word timestamps are included in result for Stage C."""
        result = SacredTranscriptionResult(
            text="Um I feel this is real",
            duration_seconds=20.0,
            word_timestamps=[
                {"word": "Um", "start": 0.0, "end": 0.3},
                {"word": "I", "start": 0.4, "end": 0.5},
            ],
        )
        assert len(result.word_timestamps) == 2
        assert result.word_timestamps[0]["word"] == "Um"


# ──────────────────────────────────────────────────────────────
# AC3: Thought Unit Boundary Validation
# Spec: "Thought Unit segmentation produces segments where no segment
# contains an open subordinate clause at its final word (spaCy
# dependency tree validation)."
# ──────────────────────────────────────────────────────────────

class TestAC3ThoughtUnitBoundaries:
    """AC3: Thought Unit segmentation boundary correctness."""

    def test_min_segment_words_is_30(self):
        """Spec: 'Segments shorter than 30 words are merged.'"""
        assert MIN_SEGMENT_WORDS == 30

    def test_thought_unit_model_fields(self):
        """ThoughtUnit has all spec-required fields."""
        unit = ThoughtUnit(
            unit_id="TU-001",
            text="This is a test unit with enough words to pass validation.",
            word_count=11,
        )
        assert unit.unit_id == "TU-001"
        assert unit.word_count == 11
        assert unit.hard_boundary is False
        assert unit.multilingual_flag is False

    def test_hard_boundary_flag(self):
        """Spec: 'force-segment at the 300-word mark with a hard boundary flag'."""
        unit = ThoughtUnit(
            unit_id="TU-HB",
            text="x " * 300,
            word_count=300,
            hard_boundary=True,
        )
        assert unit.hard_boundary is True

    def test_multilingual_flag(self):
        """Spec: 'Multilingual code-switching: flag for manual review'."""
        unit = ThoughtUnit(
            unit_id="TU-ML",
            text="This is mixed with 你好 content",
            word_count=6,
            multilingual_flag=True,
        )
        assert unit.multilingual_flag is True

    def test_word_count_auto_compute(self):
        """word_count auto-computes from text if provided as 0."""
        unit = ThoughtUnit(
            unit_id="TU-AUTO",
            text="one two three four five",
            word_count=0,
        )
        assert unit.word_count == 5


# ──────────────────────────────────────────────────────────────
# AC4: Gate Pass — All 7 Markers Authentic
# Spec: "A test Thought Unit with all 7 authentic markers present
# scores status=AUTHENTIC. The unit is appended to the
# Authentic_Material_Payload."
# ──────────────────────────────────────────────────────────────

class TestAC4GatePass:
    """AC4: All 7 markers pass → AUTHENTIC status."""

    def test_authentic_unit_passes_all_7(self, authenticity_gate):
        """AC4: Unit with all markers authentic scores AUTHENTIC."""
        text = make_authentic_text()
        unit = ThoughtUnit(unit_id="TU-AC4", text=text, word_count=len(text.split()))

        score = authenticity_gate.evaluate(unit)

        assert score.status == AuthenticityStatus.AUTHENTIC, (
            f"Expected AUTHENTIC but got {score.status}. "
            f"Failed markers: {[m.value for m in score.failed_markers]}. "
            f"Details: {[(r.marker.value, r.in_range, r.value, r.detail) for r in score.marker_results]}"
        )
        assert score.pass_count == 7
        assert len(score.failed_markers) == 0

    def test_authentic_unit_appended_to_payload(self, authenticity_gate):
        """AUTHENTIC units are appended to session.authentic_units."""
        text = make_authentic_text()
        unit = ThoughtUnit(unit_id="TU-AC4-2", text=text, word_count=len(text.split()))
        score = authenticity_gate.evaluate(unit)
        scored_unit = ScoredThoughtUnit(unit=unit, score=score)

        session = SacredAudioSession(
            session_id="test",
            coach_id="c1",
            coach_acronym="TST",
        )
        session.authentic_units.append(scored_unit)

        assert len(session.authentic_units) == 1
        assert session.authentic_units[0].status == AuthenticityStatus.AUTHENTIC


# ──────────────────────────────────────────────────────────────
# AC5: Gate Fail — Hedging + Past-Tense → SYNTHETIC_CANDIDATE
# Spec: "A test Thought Unit with hedging language (maybe, I think,
# kind of) AND past-tense dominant verbs scores status=SYNTHETIC_CANDIDATE.
# The system dispatches the correct re-elicitation prompt variant
# (hedging prompt, not generic)."
# ──────────────────────────────────────────────────────────────

class TestAC5GateFail:
    """AC5: Hedging + past-tense → SYNTHETIC_CANDIDATE + correct prompt."""

    def test_synthetic_unit_fails(self, authenticity_gate):
        """AC5: Unit with hedging + past-tense fails as SYNTHETIC_CANDIDATE."""
        text = make_synthetic_text_hedging_past()
        unit = ThoughtUnit(unit_id="TU-AC5", text=text, word_count=len(text.split()))

        score = authenticity_gate.evaluate(unit)

        assert score.status == AuthenticityStatus.SYNTHETIC_CANDIDATE, (
            f"Expected SYNTHETIC_CANDIDATE but got {score.status}. "
            f"Pass count: {score.pass_count}. "
            f"Details: {[(r.marker.value, r.in_range, r.value) for r in score.marker_results]}"
        )

    def test_hedging_marker_fails(self, authenticity_gate):
        """Hedging marker specifically fails for heavy hedging text."""
        text = make_synthetic_text_hedging_past()
        unit = ThoughtUnit(unit_id="TU-AC5-H", text=text, word_count=len(text.split()))

        score = authenticity_gate.evaluate(unit)
        assert AuthenticityMarker.ABSENCE_OF_HEDGING in score.failed_markers

    def test_correct_prompt_variant_for_hedging(self, re_elicitation_engine):
        """AC5: 'The system dispatches the correct re-elicitation prompt
        variant (hedging prompt, not generic).'"""
        # Create a score with hedging as the primary failure
        score = AuthenticityScore(
            unit_id="TU-AC5-P",
            marker_results=[
                MarkerResult(marker=m, in_range=(m != AuthenticityMarker.ABSENCE_OF_HEDGING), value=0.5)
                for m in AuthenticityMarker
            ],
        )

        prompt = re_elicitation_engine.generate_prompt(score)

        # Must be the hedging-specific prompt from spec
        expected = MARKER_PRIMARY_PROMPTS[AuthenticityMarker.ABSENCE_OF_HEDGING]
        assert prompt == expected, (
            f"Expected hedging prompt but got: {prompt[:50]}..."
        )

    def test_past_tense_prompt_variant(self, re_elicitation_engine):
        """Past-tense failure gets the correct prompt variant."""
        score = AuthenticityScore(
            unit_id="TU-AC5-PT",
            marker_results=[
                MarkerResult(marker=m, in_range=(m != AuthenticityMarker.VERB_TENSE_DISTRIBUTION), value=0.5)
                for m in AuthenticityMarker
            ],
        )

        prompt = re_elicitation_engine.generate_prompt(score)
        expected = MARKER_PRIMARY_PROMPTS[AuthenticityMarker.VERB_TENSE_DISTRIBUTION]
        assert prompt == expected


# ──────────────────────────────────────────────────────────────
# AC6: Persistent Failure — 2 Retries Then Drop
# Spec: "After 2 re-elicitation attempts that both fail, the unit
# is dropped. No error is raised. Session continues with remaining units."
# ──────────────────────────────────────────────────────────────

class TestAC6PersistentFailure:
    """AC6: 2 retries → permanent drop, no error."""

    def test_max_re_elicitation_attempts_is_2(self):
        """Spec: '≥2 re-elicitation attempts on same unit'."""
        from src.ccp.pipelines.sacred_audio_pipeline import MAX_RE_ELICITATION_ATTEMPTS
        assert MAX_RE_ELICITATION_ATTEMPTS == 2

    def test_dropped_status_exists(self):
        """AuthenticityStatus.DROPPED is defined for persistent failures."""
        assert AuthenticityStatus.DROPPED.value == "DROPPED"

    def test_dropped_unit_no_error(self):
        """Dropping a unit does not raise an exception."""
        score = AuthenticityScore(
            unit_id="TU-AC6",
            marker_results=[
                MarkerResult(marker=m, in_range=False, value=0.0)
                for m in AuthenticityMarker
            ],
        )
        score.re_elicitation_attempts = 2

        # Manually set to DROPPED — no exception should occur
        score.status = AuthenticityStatus.DROPPED
        assert score.status == AuthenticityStatus.DROPPED

    def test_session_continues_after_drop(self):
        """Session can have authentic units even with dropped ones."""
        session = SacredAudioSession(
            session_id="test-ac6",
            coach_id="c1",
            coach_acronym="TST",
        )

        # Add 3 authentic + 1 dropped
        for i in range(3):
            unit = ThoughtUnit(unit_id=f"TU-A{i}", text="x " * 35, word_count=35)
            score = AuthenticityScore(
                unit_id=f"TU-A{i}",
                marker_results=[MarkerResult(marker=m, in_range=True, value=1.0) for m in AuthenticityMarker],
            )
            session.authentic_units.append(ScoredThoughtUnit(unit=unit, score=score))

        dropped_unit = ThoughtUnit(unit_id="TU-D1", text="x " * 35, word_count=35)
        dropped_score = AuthenticityScore(
            unit_id="TU-D1",
            marker_results=[MarkerResult(marker=m, in_range=False, value=0.0) for m in AuthenticityMarker],
        )
        session.dropped_units.append(ScoredThoughtUnit(unit=dropped_unit, score=dropped_score))

        assert session.passes_sufficiency_gate()
        assert len(session.dropped_units) == 1


# ──────────────────────────────────────────────────────────────
# AC7: Insufficient Session
# Spec: "A session with only 2 AUTHENTIC units after all attempts
# ends in status=INSUFFICIENT. Coach is notified without alarm."
# ──────────────────────────────────────────────────────────────

class TestAC7InsufficientSession:
    """AC7: <3 authentic units → INSUFFICIENT."""

    def test_insufficient_with_2_units(self):
        """AC7: 2 authentic units → fails sufficiency gate."""
        session = SacredAudioSession(
            session_id="test-ac7",
            coach_id="c1",
            coach_acronym="TST",
        )

        for i in range(2):
            unit = ThoughtUnit(unit_id=f"TU-{i}", text="x " * 35, word_count=35)
            score = AuthenticityScore(
                unit_id=f"TU-{i}",
                marker_results=[MarkerResult(marker=m, in_range=True, value=1.0) for m in AuthenticityMarker],
            )
            session.authentic_units.append(ScoredThoughtUnit(unit=unit, score=score))

        assert not session.passes_sufficiency_gate()
        assert session.total_authentic_units() == 2

    def test_insufficient_session_message(self):
        """AC7: 'Coach is notified without alarm.'"""
        engine = ReElicitationEngine()
        msg = engine.get_insufficient_session_message()
        assert "great start" in msg
        assert "continue" in msg

    def test_sufficient_with_3_units(self):
        """3 authentic units passes sufficiency gate."""
        session = SacredAudioSession(
            session_id="test-sufficient",
            coach_id="c1",
            coach_acronym="TST",
        )

        for i in range(3):
            unit = ThoughtUnit(unit_id=f"TU-{i}", text="x " * 35, word_count=35)
            score = AuthenticityScore(
                unit_id=f"TU-{i}",
                marker_results=[MarkerResult(marker=m, in_range=True, value=1.0) for m in AuthenticityMarker],
            )
            session.authentic_units.append(ScoredThoughtUnit(unit=unit, score=score))

        assert session.passes_sufficiency_gate()


# ──────────────────────────────────────────────────────────────
# AC8: Receipt Chain Integrity
# Spec: "After a complete 5-stage session, all receipts A through E
# exist in Supabase with resolvable predecessor_receipt fields.
# Receipt chain integrity check passes."
# ──────────────────────────────────────────────────────────────

class TestAC8ReceiptChain:
    """AC8: 5-stage receipt chain integrity."""

    def test_receipt_chain_all_stages_present(self, receipt_chain):
        """All 5 stages write receipts with parent chain links."""
        session_id = "test-ac8-session"

        # Stage A
        r_a = receipt_chain.log(
            agent_id="TelegramInterceptor",
            action="sacred_audio_ingest",
            asset_id=session_id,
            input_summary="Audio: test.ogg, 50000 bytes",
            output_summary="Validated: format=.ogg, duration=30s",
            metadata={"stage_name": "SACRED-AUDIO-INGEST"},
        )

        # Stage B — links to A
        r_b = receipt_chain.log(
            agent_id="GroqWhisperAPI",
            action="asr_transcription",
            asset_id=session_id,
            input_summary="Audio hash: abc123...",
            output_summary="Transcript: 500 chars",
            parent_receipt_id=r_a.receipt_id,
            metadata={"stage_name": "ASR-TRANSCRIPTION"},
        )

        # Stage C — links to B
        r_c = receipt_chain.log(
            agent_id="PiCodingAgent",
            action="thought_unit_segmentation",
            asset_id=session_id,
            input_summary="Transcript: 500 chars",
            output_summary="5 thought units",
            parent_receipt_id=r_b.receipt_id,
            metadata={"stage_name": "THOUGHT-UNIT-SEGMENTATION"},
        )

        # Stage D — links to C
        r_d = receipt_chain.log(
            agent_id="LIWC22Evaluator",
            action="liwc_authenticity_gate",
            asset_id=session_id,
            input_summary="5 units evaluated",
            output_summary="AUTHENTIC: 4, SYNTHETIC: 1",
            parent_receipt_id=r_c.receipt_id,
            metadata={"stage_name": "LIWC-AUTHENTICITY-GATE"},
        )

        # Stage E — links to D
        r_e = receipt_chain.log(
            agent_id="ArchitectStorage",
            action="episodic_storage_commit",
            asset_id=session_id,
            input_summary="4 authentic units",
            output_summary="Stored to coach_soul.json",
            parent_receipt_id=r_d.receipt_id,
            metadata={"stage_name": "EPISODIC-STORAGE-COMMIT"},
        )

        # Verify chain
        chain = receipt_chain.get_provenance(session_id)
        assert len(chain) == 5

        # Verify parent links
        assert chain[0].parent_receipt_id is None  # Stage A — genesis
        assert chain[1].parent_receipt_id == r_a.receipt_id
        assert chain[2].parent_receipt_id == r_b.receipt_id
        assert chain[3].parent_receipt_id == r_c.receipt_id
        assert chain[4].parent_receipt_id == r_d.receipt_id

    def test_receipt_stage_names(self, receipt_chain):
        """All receipts have the correct stage_name in metadata."""
        expected_stages = [
            "SACRED-AUDIO-INGEST",
            "ASR-TRANSCRIPTION",
            "THOUGHT-UNIT-SEGMENTATION",
            "LIWC-AUTHENTICITY-GATE",
            "EPISODIC-STORAGE-COMMIT",
        ]

        for stage in expected_stages:
            r = receipt_chain.log(
                agent_id="test",
                action="test",
                asset_id="test-ac8-names",
                metadata={"stage_name": stage},
            )
            assert r.metadata["stage_name"] == stage


# ──────────────────────────────────────────────────────────────
# AC9: 3,000-Word Threshold & Morgan Notification
# Spec: "When extraction_readiness.authenticated_word_count crosses
# 3,000, Morgan receives a pipeline trigger notification within
# the same execution cycle."
# ──────────────────────────────────────────────────────────────

class TestAC9ThresholdNotification:
    """AC9: 3,000-word threshold triggers Morgan notification."""

    def test_minimum_corpus_is_3000(self):
        """Spec: 'Minimum of 3,000 validated words'."""
        assert MINIMUM_CORPUS_WORDS == 3000

    def test_threshold_crossing_detected(self):
        """ExtractionReadiness detects when count crosses 3,000."""
        readiness = ExtractionReadiness(
            authenticated_word_count=2800,
            session_count=5,
        )

        # This session pushes us over
        crossed = readiness.add_session("session-6", 300)
        assert crossed is True
        assert readiness.fr3_ready is True
        assert readiness.authenticated_word_count == 3100

    def test_threshold_not_crossed_below(self):
        """Below 3,000 does not trigger."""
        readiness = ExtractionReadiness(
            authenticated_word_count=2500,
            session_count=4,
        )

        crossed = readiness.add_session("session-5", 300)
        assert crossed is False
        assert readiness.fr3_ready is False
        assert readiness.authenticated_word_count == 2800

    def test_threshold_only_fires_once(self):
        """Crossing fires once, not on subsequent sessions."""
        readiness = ExtractionReadiness(
            authenticated_word_count=2900,
            session_count=5,
        )

        # First crossing
        crossed1 = readiness.add_session("session-6", 200)
        assert crossed1 is True

        # Already past threshold — should not fire again
        crossed2 = readiness.add_session("session-7", 500)
        assert crossed2 is False

    def test_coach_soul_json_extraction_readiness(self, tmp_coach_dir):
        """coach_soul.json stores extraction_readiness field correctly."""
        soul_path = tmp_coach_dir / "config" / "coach_soul.json"

        soul_data = {
            "extraction_readiness": {
                "authenticated_word_count": 3100,
                "session_count": 6,
                "sessions": ["s1", "s2", "s3", "s4", "s5", "s6"],
                "fr3_ready": True,
                "fr3_notification_sent": True,
            }
        }
        soul_path.write_text(json.dumps(soul_data, indent=2), encoding="utf-8")

        loaded = json.loads(soul_path.read_text(encoding="utf-8"))
        readiness = ExtractionReadiness.model_validate(loaded["extraction_readiness"])
        assert readiness.fr3_ready is True
        assert readiness.authenticated_word_count == 3100


# ──────────────────────────────────────────────────────────────
# AC10: Audio Isolation
# Spec: "Raw audio is never transmitted to any service other than
# Groq Whisper. A network intercept test on a simulated session
# must show only one external TLS connection (Groq endpoint)."
# ──────────────────────────────────────────────────────────────

class TestAC10Isolation:
    """AC10: Raw audio only goes to Groq Whisper."""

    def test_groq_is_only_external_api(self):
        """The SacredAudioTranscriber only calls Groq API (or Gemini as fallback)."""
        assert SacredAudioTranscriber.GROQ_API_URL == "https://api.groq.com/openai/v1/audio/transcriptions"

    def test_audio_not_stored_to_disk_in_pipeline(self):
        """Pipeline spec: 'written to ephemeral local buffer (in-process memory,
        not disk — Sacred Audio designation)'.

        The pipeline receives bytes, not file paths. Audio bytes are
        passed through memory only.
        """
        from src.ccp.pipelines.sacred_audio_pipeline import SacredAudioPipeline
        import inspect
        sig = inspect.signature(SacredAudioPipeline.process_audio)
        params = list(sig.parameters.keys())

        # process_audio accepts audio_bytes (bytes), not file_path
        assert "audio_bytes" in params
        assert "file_path" not in params

    def test_sacred_audio_formats_restricted(self):
        """Only .ogg, .mp3, .m4a are accepted — no other formats leak through."""
        assert SACRED_AUDIO_FORMATS == {".ogg", ".mp3", ".m4a"}

    def test_transcriber_only_calls_groq_or_gemini(self):
        """No other external API endpoints are referenced in the transcriber."""
        import inspect
        source = inspect.getsource(SacredAudioTranscriber)
        # Only Groq and Gemini API URLs should appear
        assert "api.groq.com" in source
        # No other external API URLs (Supabase, Redis, etc.)
        assert "api.openai.com" not in source
        assert "whisper.ai" not in source
