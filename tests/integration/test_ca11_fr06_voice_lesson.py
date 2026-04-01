"""FR-CA11-06 — Voice Note → Course Material Pipeline — Integration Tests.

Covers all 5 Acceptance Criteria:
  AC1: 90-second voice note → structured lesson page
  AC2: Voice DNA TTT drift < 15 %
  AC3: Concept diagram nodes match key concepts
  AC4: learning_path_registry entry with correct tags
  AC5: Practical exercise in Implementation Intention format
"""
from __future__ import annotations

import asyncio
import re
import uuid
from typing import Any, Optional

import pytest

from src.ccp.models.ca11_models import (
    ConceptDiagramEdge,
    ConceptDiagramNode,
    LearningPathRegistryRef,
    LessonResult,
    PracticalExercise,
    VoiceNoteLessonPayload,
)
from src.ccp.services.voice_to_lesson import (
    AGENT_BENJAMIN,
    AGENT_GABRIELLE,
    CONTENT_TYPE_VOICE_LESSON,
    LESSON_COMMAND_PREFIX,
    LESSON_REGISTRY_SQL,
    MAX_TAKEAWAYS,
    MIN_TAKEAWAYS,
    VOICE_DNA_TTT_DRIFT_THRESHOLD,
    ConceptDiagramGenerator,
    LessonCommandHandler,
    LessonStructurer,
    LessonTranscriber,
    VoiceToLessonPipeline,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

COACH_ID = "uuid-coach-test-01"
COACH_ACRONYM = "JPR"
CHAT_ID = "chat-777"

SAMPLE_TRANSCRIPT = (
    "External validation destroys inner authority. "
    "When we seek approval from others, we give away our power. "
    "The approval-seeking pattern comes from childhood authority dynamics. "
    "True confidence is an inside job that requires deliberate practice. "
    "Start noticing when you look for permission before acting. "
    "Inner authority means trusting yourself even when others disagree."
)

SHORT_TRANSCRIPT = "Boundaries matter. They protect your energy."


def _run(coro):
    """Synchronous helper — no pytest-asyncio required."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# ---- Mocks ----

class MockTranscriber:
    def __init__(self, text: str = SAMPLE_TRANSCRIPT):
        self._text = text
        self.called = False
    async def transcribe(self, audio_path: str) -> str:
        self.called = True
        return self._text


class FailingTranscriber:
    async def transcribe(self, audio_path: str) -> str:
        raise RuntimeError("Whisper unavailable")


class MockAFFiNeSync:
    def __init__(self):
        self.pushes: list[dict] = []
    async def push_content(self, coach_id, section, title, body, *, metadata=None):
        page_id = f"page-{uuid.uuid4().hex[:8]}"
        self.pushes.append({
            "coach_id": coach_id, "section": section,
            "title": title, "body": body, "metadata": metadata,
            "page_id": page_id,
        })
        return page_id


class FailingAFFiNeSync:
    async def push_content(self, *a, **kw):
        raise ConnectionError("AFFiNE offline")


class MockVoiceDNA:
    def __init__(self, drift: float = 0.05):
        self._drift = drift
    def compute_ttt_drift(self, text: str, coach_id: str) -> float:
        return self._drift
    def get_voice_style(self, coach_id: str) -> dict:
        return {"style": "warm-authoritative"}


class MockLearningPathHook:
    def __init__(self):
        self.entries: list[dict] = []
    async def on_voice_lesson(self, entry: dict) -> None:
        self.entries.append(entry)


class MockTelegram:
    def __init__(self):
        self.messages: list[tuple[str, str]] = []
    async def send_message(self, chat_id: str, text: str) -> None:
        self.messages.append((chat_id, text))


def _pipeline(
    *,
    transcript: str = SAMPLE_TRANSCRIPT,
    drift: float = 0.05,
    failing_transcriber: bool = False,
    failing_sync: bool = False,
    with_lp: bool = True,
    with_telegram: bool = True,
):
    transcriber = FailingTranscriber() if failing_transcriber else MockTranscriber(transcript)
    sync = FailingAFFiNeSync() if failing_sync else MockAFFiNeSync()
    lp = MockLearningPathHook() if with_lp else None
    tg = MockTelegram() if with_telegram else None
    vdna = MockVoiceDNA(drift)
    pipe = VoiceToLessonPipeline(
        transcriber=transcriber,
        affine_sync=sync,
        voice_dna=vdna,
        learning_path_hook=lp,
        telegram=tg,
    )
    return pipe, transcriber, sync, lp, tg, vdna


# ===================================================================
# 1. Model validation (7 tests)
# ===================================================================

class TestModels:
    def test_practical_exercise_valid(self):
        ex = PracticalExercise(
            implementation_intention="When I notice X, I will Y.",
            duration="5 minutes daily for 7 days",
        )
        assert "When" in ex.implementation_intention

    def test_practical_exercise_empty_intention_rejected(self):
        with pytest.raises(Exception):
            PracticalExercise(implementation_intention="", duration="1 day")

    def test_concept_diagram_node_defaults(self):
        n = ConceptDiagramNode(label="Root", level=0)
        assert n.node_id  # UUID generated
        assert n.parent_id is None

    def test_concept_diagram_edge(self):
        e = ConceptDiagramEdge(from_id="a", to_id="b")
        assert e.from_id == "a"

    def test_learning_path_registry_ref_default_type(self):
        ref = LearningPathRegistryRef(topic_cluster="validation", difficulty_level="developing")
        assert ref.content_type == "voice_lesson"

    def test_voice_note_lesson_payload_roundtrip(self):
        p = VoiceNoteLessonPayload(
            asset_id="JPR-LESSON-20260324-abc-TEXT",
            coach_id=COACH_ID,
            title="Test Lesson",
            key_takeaways=["One", "Two", "Three"],
            detailed_explanation_markdown="## Test",
            practical_exercise=PracticalExercise(
                implementation_intention="When X, I will Y.",
                duration="5 min",
            ),
            learning_path_registry=LearningPathRegistryRef(
                topic_cluster="test", difficulty_level="developing",
            ),
        )
        d = p.model_dump()
        assert d["title"] == "Test Lesson"
        assert len(d["key_takeaways"]) == 3

    def test_lesson_result_success_fields(self):
        r = LessonResult(success=True, diagram_generated=True, learning_path_tagged=True)
        assert r.success
        assert r.fallback_used is False


# ===================================================================
# 2. Command handler (4 tests)
# ===================================================================

class TestLessonCommandHandler:
    def test_detects_lesson_prefix(self):
        assert LessonCommandHandler.is_lesson_command("/lesson")
        assert LessonCommandHandler.is_lesson_command("/lesson some text")
        assert LessonCommandHandler.is_lesson_command("  /LESSON ")

    def test_rejects_non_lesson(self):
        assert not LessonCommandHandler.is_lesson_command("/help")
        assert not LessonCommandHandler.is_lesson_command(None)
        assert not LessonCommandHandler.is_lesson_command("")

    def test_strip_prefix(self):
        assert LessonCommandHandler.strip_prefix("/lesson some topic") == "some topic"

    def test_strip_prefix_no_prefix(self):
        assert LessonCommandHandler.strip_prefix("hello") == "hello"


# ===================================================================
# 3. Lesson structurer — Gabrielle (8 tests)
# ===================================================================

class TestLessonStructurer:
    def test_structure_has_all_sections(self):
        s = LessonStructurer()
        result = s.structure_lesson(SAMPLE_TRANSCRIPT, COACH_ID)
        assert "title" in result
        assert "key_takeaways" in result
        assert "detailed_explanation_markdown" in result
        assert "practical_exercise" in result

    def test_title_extracted_from_first_sentence(self):
        s = LessonStructurer()
        result = s.structure_lesson(SAMPLE_TRANSCRIPT, COACH_ID)
        assert "External validation" in result["title"]

    def test_takeaways_count_within_bounds(self):
        s = LessonStructurer()
        result = s.structure_lesson(SAMPLE_TRANSCRIPT, COACH_ID)
        assert MIN_TAKEAWAYS <= len(result["key_takeaways"]) <= MAX_TAKEAWAYS

    def test_takeaways_padded_for_short_transcript(self):
        s = LessonStructurer()
        result = s.structure_lesson(SHORT_TRANSCRIPT, COACH_ID)
        assert len(result["key_takeaways"]) >= MIN_TAKEAWAYS

    def test_explanation_is_markdown(self):
        s = LessonStructurer()
        result = s.structure_lesson(SAMPLE_TRANSCRIPT, COACH_ID)
        assert result["detailed_explanation_markdown"].startswith("## ")

    def test_exercise_is_implementation_intention(self):
        s = LessonStructurer()
        result = s.structure_lesson(SAMPLE_TRANSCRIPT, COACH_ID)
        intention = result["practical_exercise"]["implementation_intention"]
        assert intention.startswith("When ")
        assert "duration" in result["practical_exercise"]

    def test_voice_dna_no_drift_without_provider(self):
        s = LessonStructurer(voice_dna=None)
        assert s.validate_voice_dna("any text", COACH_ID) == 0.0

    def test_voice_dna_drift_returns_value(self):
        vdna = MockVoiceDNA(drift=0.12)
        s = LessonStructurer(voice_dna=vdna)
        assert s.validate_voice_dna("text", COACH_ID) == 0.12


# ===================================================================
# 4. Concept diagram — Benjamin (5 tests)
# ===================================================================

class TestConceptDiagramGenerator:
    def test_generates_hierarchical_tree(self):
        gen = ConceptDiagramGenerator()
        diagram = gen.generate("Root Topic", ["Sub A", "Sub B"])
        assert len(diagram["nodes"]) == 5  # 1 root + 2 children + 2 leaves
        assert len(diagram["edges"]) == 4

    def test_root_is_level_zero(self):
        gen = ConceptDiagramGenerator()
        diagram = gen.generate("Root", ["A"])
        root = diagram["nodes"][0]
        assert root["level"] == 0
        assert root["label"] == "Root"

    def test_children_are_level_one(self):
        gen = ConceptDiagramGenerator()
        diagram = gen.generate("Root", ["Child"])
        child = diagram["nodes"][1]
        assert child["level"] == 1
        assert child["label"] == "Child"

    def test_nodes_match_concepts_ac3(self):
        """AC3 — diagram nodes match key concepts."""
        gen = ConceptDiagramGenerator()
        takeaways = ["Insight A", "Insight B", "Insight C"]
        diagram = gen.generate("Title", takeaways)
        assert gen.nodes_match_concepts(diagram, takeaways)

    def test_nodes_mismatch_detected(self):
        gen = ConceptDiagramGenerator()
        diagram = gen.generate("Title", ["X"])
        assert not gen.nodes_match_concepts(diagram, ["Y"])


# ===================================================================
# 5. Full pipeline — AC1 (5 tests)
# ===================================================================

class TestPipelineAC1:
    """AC1 — 90-second voice note → structured lesson page."""

    def test_successful_pipeline(self):
        pipe, _, sync, lp, tg, _ = _pipeline()
        result = _run(pipe.process_lesson("audio.ogg", COACH_ID, CHAT_ID, COACH_ACRONYM))
        assert result.success
        assert result.lesson is not None
        assert result.affine_page_id is not None
        assert result.diagram_generated
        assert not result.fallback_used

    def test_affine_receives_push(self):
        pipe, _, sync, _, _, _ = _pipeline()
        _run(pipe.process_lesson("audio.ogg", COACH_ID, CHAT_ID, COACH_ACRONYM))
        assert len(sync.pushes) == 1
        push = sync.pushes[0]
        assert push["section"] == "content_library"
        assert push["coach_id"] == COACH_ID

    def test_telegram_confirmation_sent(self):
        pipe, _, _, _, tg, _ = _pipeline()
        result = _run(pipe.process_lesson("audio.ogg", COACH_ID, CHAT_ID, COACH_ACRONYM))
        assert len(tg.messages) == 1
        assert "Content Library" in tg.messages[0][1]

    def test_transcription_failure_returns_error(self):
        pipe, _, _, _, _, _ = _pipeline(failing_transcriber=True)
        result = _run(pipe.process_lesson("audio.ogg", COACH_ID))
        assert not result.success
        assert "Transcription failed" in result.error

    def test_affine_failure_returns_error(self):
        pipe, _, _, _, _, _ = _pipeline(failing_sync=True)
        result = _run(pipe.process_lesson("audio.ogg", COACH_ID))
        assert not result.success
        assert "AFFiNE push failed" in result.error


# ===================================================================
# 6. Voice DNA — AC2 (4 tests)
# ===================================================================

class TestPipelineAC2:
    """AC2 — Voice DNA TTT drift < 15 %."""

    def test_low_drift_passes(self):
        pipe, _, _, _, _, _ = _pipeline(drift=0.05)
        result = _run(pipe.process_lesson("audio.ogg", COACH_ID))
        assert result.success
        assert not result.fallback_used

    def test_high_drift_triggers_fallback(self):
        pipe, _, sync, _, _, _ = _pipeline(drift=0.20)
        result = _run(pipe.process_lesson("audio.ogg", COACH_ID))
        assert result.success
        assert result.fallback_used
        # Fallback pushes raw transcript
        assert len(sync.pushes) == 1
        assert "Raw Notes" in sync.pushes[0]["title"]

    def test_exact_threshold_triggers_fallback(self):
        """Drift == 0.15 is AT the threshold — should NOT trigger fallback
        (> threshold only)."""
        pipe, _, _, _, _, _ = _pipeline(drift=0.15)
        result = _run(pipe.process_lesson("audio.ogg", COACH_ID))
        assert result.success
        assert not result.fallback_used

    def test_drift_threshold_constant(self):
        assert VOICE_DNA_TTT_DRIFT_THRESHOLD == 0.15


# ===================================================================
# 7. Concept diagram — AC3 (covered above, additional edge case)
# ===================================================================

class TestPipelineAC3:
    """AC3 — Concept diagram nodes match key concepts."""

    def test_diagram_url_populated(self):
        pipe, _, _, _, _, _ = _pipeline()
        result = _run(pipe.process_lesson("audio.ogg", COACH_ID, CHAT_ID, COACH_ACRONYM))
        assert result.lesson.concept_diagram_url is not None
        assert "excalidraw" in result.lesson.concept_diagram_url
        assert COACH_ACRONYM in result.lesson.concept_diagram_url


# ===================================================================
# 8. Learning path tagging — AC4 (4 tests)
# ===================================================================

class TestPipelineAC4:
    """AC4 — learning_path_registry entry with correct tags."""

    def test_learning_path_tagged(self):
        pipe, _, _, lp, _, _ = _pipeline()
        result = _run(pipe.process_lesson("audio.ogg", COACH_ID, CHAT_ID, COACH_ACRONYM))
        assert result.learning_path_tagged
        assert len(lp.entries) == 1
        entry = lp.entries[0]
        assert entry["content_type"] == CONTENT_TYPE_VOICE_LESSON
        assert entry["difficulty_level"] == "developing"

    def test_learning_path_entry_has_topic_cluster(self):
        pipe, _, _, lp, _, _ = _pipeline()
        _run(pipe.process_lesson("audio.ogg", COACH_ID, CHAT_ID, COACH_ACRONYM))
        assert lp.entries[0]["topic_cluster"]  # non-empty

    def test_no_hook_still_succeeds(self):
        pipe, _, _, _, _, _ = _pipeline(with_lp=False)
        result = _run(pipe.process_lesson("audio.ogg", COACH_ID, CHAT_ID, COACH_ACRONYM))
        assert result.success
        assert not result.learning_path_tagged

    def test_payload_registry_matches(self):
        pipe, _, _, _, _, _ = _pipeline()
        result = _run(pipe.process_lesson("audio.ogg", COACH_ID, CHAT_ID, COACH_ACRONYM))
        reg = result.lesson.learning_path_registry
        assert reg.content_type == "voice_lesson"
        assert reg.difficulty_level == "developing"


# ===================================================================
# 9. Practical exercise — AC5 (3 tests)
# ===================================================================

class TestPipelineAC5:
    """AC5 — Practical exercise in Implementation Intention format."""

    def test_exercise_present(self):
        pipe, _, _, _, _, _ = _pipeline()
        result = _run(pipe.process_lesson("audio.ogg", COACH_ID))
        ex = result.lesson.practical_exercise
        assert ex is not None

    def test_exercise_has_when_trigger(self):
        pipe, _, _, _, _, _ = _pipeline()
        result = _run(pipe.process_lesson("audio.ogg", COACH_ID))
        intention = result.lesson.practical_exercise.implementation_intention
        assert intention.startswith("When ")

    def test_exercise_has_duration(self):
        pipe, _, _, _, _, _ = _pipeline()
        result = _run(pipe.process_lesson("audio.ogg", COACH_ID))
        assert result.lesson.practical_exercise.duration


# ===================================================================
# 10. Constants & SQL (2 tests)
# ===================================================================

class TestConstants:
    def test_agent_names(self):
        assert AGENT_GABRIELLE == "Gabrielle"
        assert AGENT_BENJAMIN == "Benjamin"

    def test_sql_schema(self):
        assert "lesson_registry" in LESSON_REGISTRY_SQL
        assert "lesson_id" in LESSON_REGISTRY_SQL
