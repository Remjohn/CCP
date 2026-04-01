"""FR-CA11-06 — Voice Note → Course Material Pipeline.

Converts a coach's Telegram voice note (``/lesson`` prefix) into a
structured AFFiNE lesson page with an auto-generated Excalidraw concept
diagram, then tags the lesson in the learning-path registry.

Pipeline: Whisper transcription → Gabrielle lesson structuring →
          Benjamin concept diagram → AFFiNE push → learning-path tag.
"""
from __future__ import annotations

import hashlib
import re
import uuid
from datetime import datetime, timezone
from typing import Any, Optional, Protocol

from src.ccp.models.ca11_models import (
    ConceptDiagramEdge,
    ConceptDiagramNode,
    LearningPathRegistryRef,
    LessonResult,
    PracticalExercise,
    VoiceNoteLessonPayload,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

AGENT_GABRIELLE = "Gabrielle"
AGENT_BENJAMIN = "Benjamin"
LESSON_COMMAND_PREFIX = "/lesson"
VOICE_DNA_TTT_DRIFT_THRESHOLD = 0.15  # 15 %
MIN_TAKEAWAYS = 3
MAX_TAKEAWAYS = 5
CONTENT_TYPE_VOICE_LESSON = "voice_lesson"

# ---------------------------------------------------------------------------
# SQL — lesson output registry
# ---------------------------------------------------------------------------

LESSON_REGISTRY_SQL = """
CREATE TABLE IF NOT EXISTS lesson_registry (
    lesson_id       TEXT PRIMARY KEY,
    asset_id        TEXT NOT NULL,
    coach_id        TEXT NOT NULL,
    title           TEXT NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    concept_diagram_url TEXT,
    fallback_used   BOOLEAN NOT NULL DEFAULT FALSE,
    affine_page_id  TEXT
);
"""

# ---------------------------------------------------------------------------
# Protocol stubs (same duck-typing pattern as FR-CA11-05)
# ---------------------------------------------------------------------------


class TranscriberProtocol(Protocol):
    async def transcribe(self, audio_path: str) -> str: ...


class AFFiNESyncProtocol(Protocol):
    async def push_content(self, coach_id: str, section: str,
                           title: str, body: str, *,
                           metadata: dict[str, Any] | None = None) -> str: ...


class VoiceDNAProtocol(Protocol):
    def compute_ttt_drift(self, text: str, coach_id: str) -> float: ...
    def get_voice_style(self, coach_id: str) -> dict[str, Any]: ...


class LearningPathHookProtocol(Protocol):
    async def on_voice_lesson(self, entry: dict[str, Any]) -> None: ...


class TelegramProtocol(Protocol):
    async def send_message(self, chat_id: str, text: str) -> None: ...


# ---------------------------------------------------------------------------
# Stage 1 — Command Detection & Transcription
# ---------------------------------------------------------------------------


class LessonCommandHandler:
    """Detects ``/lesson`` prefix and routes to the voice-to-lesson pipeline."""

    @staticmethod
    def is_lesson_command(text: str | None) -> bool:
        if not text:
            return False
        return text.strip().lower().startswith(LESSON_COMMAND_PREFIX)

    @staticmethod
    def strip_prefix(text: str) -> str:
        stripped = text.strip()
        if stripped.lower().startswith(LESSON_COMMAND_PREFIX):
            return stripped[len(LESSON_COMMAND_PREFIX):].strip()
        return stripped


class LessonTranscriber:
    """Wraps Whisper transcription for lesson voice notes."""

    def __init__(self, transcriber: TranscriberProtocol) -> None:
        self._transcriber = transcriber

    async def transcribe(self, audio_path: str) -> str:
        return await self._transcriber.transcribe(audio_path)


# ---------------------------------------------------------------------------
# Stage 2 — Gabrielle: Lesson Structuring
# ---------------------------------------------------------------------------


class LessonStructurer:
    """``Gabrielle`` agent — structures raw transcript into lesson components
    while enforcing Voice DNA consistency."""

    def __init__(self, voice_dna: VoiceDNAProtocol | None = None) -> None:
        self._voice_dna = voice_dna

    # -- public API --

    def structure_lesson(self, transcript: str, coach_id: str) -> dict[str, Any]:
        title = self._extract_title(transcript)
        takeaways = self._extract_takeaways(transcript)
        explanation = self._build_explanation(transcript, takeaways)
        exercise = self._build_exercise(transcript)
        return {
            "title": title,
            "key_takeaways": takeaways,
            "detailed_explanation_markdown": explanation,
            "practical_exercise": exercise,
        }

    def validate_voice_dna(self, text: str, coach_id: str) -> float:
        """Return TTT drift ratio.  0.0 = perfect match."""
        if self._voice_dna is None:
            return 0.0
        return self._voice_dna.compute_ttt_drift(text, coach_id)

    # -- private helpers --

    @staticmethod
    def _extract_title(transcript: str) -> str:
        sentences = [s.strip() for s in re.split(r'[.!?]', transcript) if s.strip()]
        if sentences:
            title = sentences[0]
            if len(title) > 80:
                title = title[:77] + "..."
            return title
        return "Untitled Lesson"

    @staticmethod
    def _extract_takeaways(transcript: str) -> list[str]:
        sentences = [s.strip() for s in re.split(r'[.!?]', transcript) if s.strip()]
        # Pick unique sentences as takeaways (skip title sentence)
        seen: set[str] = set()
        takeaways: list[str] = []
        for s in sentences[1:]:
            normalised = s.lower()
            if normalised not in seen and len(s) > 10:
                seen.add(normalised)
                takeaways.append(s)
            if len(takeaways) >= MAX_TAKEAWAYS:
                break
        # Pad if fewer than MIN_TAKEAWAYS
        while len(takeaways) < MIN_TAKEAWAYS:
            takeaways.append(f"Key insight #{len(takeaways) + 1} from this lesson")
        return takeaways[:MAX_TAKEAWAYS]

    @staticmethod
    def _build_explanation(transcript: str, takeaways: list[str]) -> str:
        heading = "## Detailed Explanation\n\n"
        body_lines: list[str] = []
        for i, tw in enumerate(takeaways, 1):
            body_lines.append(f"### Point {i}: {tw}\n")
            body_lines.append(f"This concept explores how {tw.lower()} affects your coaching journey.\n")
        return heading + "\n".join(body_lines)

    @staticmethod
    def _build_exercise(transcript: str) -> dict[str, str]:
        # Implementation Intention format from FR-CBCS-09
        trigger = "I notice a relevant pattern"
        action = "I will pause and reflect on what I actually want"
        # Try to extract a meaningful trigger from transcript
        sentences = [s.strip() for s in re.split(r'[.!?]', transcript) if s.strip()]
        if len(sentences) >= 2:
            trigger = f"I notice {sentences[1].lower()}"
        return {
            "implementation_intention": f"When {trigger}, {action}.",
            "duration": "5 minutes daily for 7 days",
        }


# ---------------------------------------------------------------------------
# Stage 3 — Benjamin: Concept Diagram Generation
# ---------------------------------------------------------------------------


class ConceptDiagramGenerator:
    """``Benjamin`` agent — generates a hierarchical concept diagram from
    lesson topics as an Excalidraw-compatible structure."""

    def generate(self, title: str, takeaways: list[str]) -> dict[str, Any]:
        nodes: list[ConceptDiagramNode] = []
        edges: list[ConceptDiagramEdge] = []

        # Root node (level 0)
        root = ConceptDiagramNode(label=title, level=0)
        nodes.append(root)

        for tw in takeaways:
            child = ConceptDiagramNode(label=tw, level=1, parent_id=root.node_id)
            nodes.append(child)
            edges.append(ConceptDiagramEdge(from_id=root.node_id, to_id=child.node_id))

            # Practical application leaf
            leaf = ConceptDiagramNode(
                label=f"Apply: {tw[:40]}",
                level=2,
                parent_id=child.node_id,
            )
            nodes.append(leaf)
            edges.append(ConceptDiagramEdge(from_id=child.node_id, to_id=leaf.node_id))

        return {
            "nodes": [n.model_dump() for n in nodes],
            "edges": [e.model_dump() for e in edges],
        }

    @staticmethod
    def nodes_match_concepts(diagram: dict[str, Any], takeaways: list[str]) -> bool:
        """AC3 validation — diagram nodes must cover every key concept."""
        node_labels = {n["label"] for n in diagram.get("nodes", [])}
        return all(tw in node_labels for tw in takeaways)


# ---------------------------------------------------------------------------
# Orchestrator — VoiceToLessonPipeline
# ---------------------------------------------------------------------------


class VoiceToLessonPipeline:
    """End-to-end pipeline: /lesson voice note → structured AFFiNE page."""

    def __init__(
        self,
        transcriber: TranscriberProtocol,
        affine_sync: AFFiNESyncProtocol,
        voice_dna: VoiceDNAProtocol | None = None,
        learning_path_hook: LearningPathHookProtocol | None = None,
        telegram: TelegramProtocol | None = None,
    ) -> None:
        self._lesson_transcriber = LessonTranscriber(transcriber)
        self._structurer = LessonStructurer(voice_dna)
        self._diagram_gen = ConceptDiagramGenerator()
        self._affine_sync = affine_sync
        self._learning_path_hook = learning_path_hook
        self._telegram = telegram

    async def process_lesson(
        self,
        audio_path: str,
        coach_id: str,
        chat_id: str | None = None,
        coach_acronym: str = "CCH",
    ) -> LessonResult:
        # Stage 1: Transcription
        try:
            transcript = await self._lesson_transcriber.transcribe(audio_path)
        except Exception as exc:
            return LessonResult(success=False, error=f"Transcription failed: {exc}")

        # Stage 2: Lesson structuring (Gabrielle)
        try:
            structured = self._structurer.structure_lesson(transcript, coach_id)
        except Exception:
            # Fallback: push raw transcript
            return await self._fallback_raw(transcript, coach_id, coach_acronym)

        # Voice DNA validation
        ttt_drift = self._structurer.validate_voice_dna(
            structured["detailed_explanation_markdown"], coach_id
        )
        if ttt_drift > VOICE_DNA_TTT_DRIFT_THRESHOLD:
            return await self._fallback_raw(transcript, coach_id, coach_acronym)

        # Build payload
        asset_id = self._make_asset_id(coach_acronym)
        exercise = PracticalExercise(**structured["practical_exercise"])
        lesson = VoiceNoteLessonPayload(
            asset_id=asset_id,
            coach_id=coach_id,
            title=structured["title"],
            key_takeaways=structured["key_takeaways"],
            detailed_explanation_markdown=structured["detailed_explanation_markdown"],
            practical_exercise=exercise,
            learning_path_registry=LearningPathRegistryRef(
                topic_cluster=self._derive_topic_cluster(structured["title"]),
                difficulty_level="developing",
                content_type=CONTENT_TYPE_VOICE_LESSON,
            ),
        )

        # Stage 3a: Concept diagram (Benjamin) — non-blocking
        diagram_generated = False
        try:
            diagram = self._diagram_gen.generate(
                structured["title"], structured["key_takeaways"]
            )
            diagram_generated = True
            lesson.concept_diagram_url = (
                f"s3://{coach_acronym}/excalidraw/"
                f"lesson_{lesson.lesson_id}_diagram.json"
            )
        except Exception:
            diagram = None

        # Stage 3b: AFFiNE push
        try:
            page_id = await self._affine_sync.push_content(
                coach_id,
                "content_library",
                lesson.title,
                lesson.detailed_explanation_markdown,
                metadata={
                    "lesson_id": lesson.lesson_id,
                    "asset_id": lesson.asset_id,
                    "key_takeaways": lesson.key_takeaways,
                    "exercise": exercise.model_dump(),
                    "diagram": diagram,
                },
            )
        except Exception as exc:
            return LessonResult(
                success=False,
                lesson=lesson,
                diagram_generated=diagram_generated,
                error=f"AFFiNE push failed: {exc}",
            )

        # Stage 3c: Learning path tagging (Gabrielle)
        lp_tagged = False
        if self._learning_path_hook:
            try:
                await self._learning_path_hook.on_voice_lesson({
                    "lesson_id": lesson.lesson_id,
                    "coach_id": coach_id,
                    "topic_cluster": lesson.learning_path_registry.topic_cluster,
                    "difficulty_level": lesson.learning_path_registry.difficulty_level,
                    "content_type": CONTENT_TYPE_VOICE_LESSON,
                })
                lp_tagged = True
            except Exception:
                pass  # non-blocking

        # Telegram confirmation
        if self._telegram and chat_id:
            try:
                await self._telegram.send_message(
                    chat_id,
                    f"Your lesson \"{lesson.title}\" is ready in your Content Library!",
                )
            except Exception:
                pass

        return LessonResult(
            success=True,
            lesson=lesson,
            affine_page_id=page_id,
            diagram_generated=diagram_generated,
            learning_path_tagged=lp_tagged,
            fallback_used=False,
        )

    # -- fallback --

    async def _fallback_raw(
        self, transcript: str, coach_id: str, coach_acronym: str
    ) -> LessonResult:
        """Delivers raw transcript to AFFiNE when structuring fails."""
        asset_id = self._make_asset_id(coach_acronym, fallback=True)
        try:
            page_id = await self._affine_sync.push_content(
                coach_id,
                "content_library",
                "Raw Notes — Voice Lesson",
                transcript,
                metadata={"tag": "Raw Notes"},
            )
        except Exception as exc:
            return LessonResult(success=False, error=f"Fallback push failed: {exc}")
        return LessonResult(
            success=True,
            affine_page_id=page_id,
            fallback_used=True,
        )

    # -- helpers --

    @staticmethod
    def _make_asset_id(coach_acronym: str, fallback: bool = False) -> str:
        date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
        uid = uuid.uuid4().hex[:8]
        suffix = "RAW" if fallback else "TEXT"
        return f"{coach_acronym}-LESSON-{date_str}-{uid}-{suffix}"

    @staticmethod
    def _derive_topic_cluster(title: str) -> str:
        words = re.sub(r'[^a-z0-9\s]', '', title.lower()).split()
        meaningful = [w for w in words if len(w) > 3]
        return "_".join(meaningful[:3]) if meaningful else "general"
