"""
CCP FR-CA11-05 — AI Session Recap Generator
DEP-ENG-075 PROPOSED

Agent: Lena (Session Intelligence Analyst, Perception Department)

Converts OBS coaching session recordings into structured Session Intelligence
Reports: Whisper STT → LLM extraction → AFFiNE Session Archive → Telegram
client summary → Context Premise graph update → CRAL evidence injection.

Spec reference: FR-CA11-05_AI_Session_Recap_Generator_Tech_Spec.md
  §4 — Stage 1: Recording Upload & Transcription
  §4 — Stage 2: Intelligence Extraction (Lena)
  §4 — Stage 3: Mind Map Generation & Delivery (Benjamin)
  §4 — Stage 4: Intelligence Propagation (Aria + CRAL)
  §5 — DEP-ENG-075 PROPOSED (SessionIntelligenceReport)
  §6 — Backward Compatibility: transcription failure fallback
  §7 — Tasks 1-9
  §8 — AC1-AC6

Architecture references:
  FR2 (Sacred Audio): Whisper STT pipeline
  FR29 (Aria): Context Premise Extraction
  DEP-ENG-021: CRAL Finding Index
  DEP-ENG-041: Receipt Chain Guard
  FR-CA11-02: AFFiNE Sync Service
  FR-CA11-13: OBS Recording Controller (trigger)
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import re
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.ca11_models import (
    ActionItem,
    BreakthroughMoment,
    DarnCatCategory,
    DifficultyLevel,
    EmotionalBeat,
    KeyInsight,
    MindMapEdge,
    MindMapNode,
    MoodState,
    ReceiptChainGuardRef,
    SessionIntelligenceReport,
    SessionMindMap,
)

logger = logging.getLogger(__name__)

# ── Constants ─────────────────────────────────────────────────────────────────

AGENT_LENA = "Lena"
AGENT_BENJAMIN = "Benjamin"
AGENT_ARIA = "Aria"

# SLA targets (seconds)
SLA_30MIN_SESSION = 600  # 10 minutes
SLA_60MIN_SESSION = 900  # 15 minutes
SLA_90MIN_SESSION = 1200  # 20 minutes

# DARN-CAT keywords for change talk detection
DARN_CAT_MARKERS: dict[DarnCatCategory, list[str]] = {
    DarnCatCategory.DESIRE: ["i want", "i wish", "i'd like", "i hope"],
    DarnCatCategory.ABILITY: ["i can", "i could", "i'm able", "i might be able"],
    DarnCatCategory.REASON: ["because", "the reason", "it matters", "it would help"],
    DarnCatCategory.NEED: ["i need", "i have to", "i must", "i've got to"],
    DarnCatCategory.COMMITMENT: ["i will", "i'm going to", "i promise", "i intend"],
    DarnCatCategory.ACTIVATION: ["i've started", "i've begun", "i've already", "i took"],
    DarnCatCategory.TAKING_STEPS: ["i did", "i went", "i called", "i made"],
}

# Emotional intensity thresholds
INTENSITY_LOW = 0.3
INTENSITY_HIGH = 0.7

# CRAL M1-M7 qualifying insight threshold
CRAL_INSIGHT_MIN_SIGNIFICANCE = 0.6


# ── SQL Schema ────────────────────────────────────────────────────────────────
# Task 1

SESSION_INTELLIGENCE_SQL = """
CREATE TABLE IF NOT EXISTS session_intelligence (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    coach_id UUID NOT NULL,
    client_id UUID NOT NULL,
    recording_url TEXT NOT NULL,
    transcript_url TEXT,
    key_insights JSONB DEFAULT '[]'::JSONB,
    action_items JSONB DEFAULT '[]'::JSONB,
    emotional_beats JSONB DEFAULT '[]'::JSONB,
    topic_clusters JSONB DEFAULT '[]'::JSONB,
    breakthrough_moments JSONB DEFAULT '[]'::JSONB,
    mind_map_url TEXT,
    processing_status TEXT DEFAULT 'QUEUED'
        CHECK (processing_status IN ('QUEUED', 'TRANSCRIBING', 'EXTRACTING', 'COMPLETE', 'FAILED')),
    processing_started_at TIMESTAMPTZ,
    processing_completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    receipt_hash TEXT
);

CREATE INDEX IF NOT EXISTS idx_si_coach ON session_intelligence(coach_id);
CREATE INDEX IF NOT EXISTS idx_si_client ON session_intelligence(client_id);
CREATE INDEX IF NOT EXISTS idx_si_status ON session_intelligence(processing_status);
"""


# ══════════════════════════════════════════════════════════════════════════════
# Unit 3 — Whisper STT Integration
# ══════════════════════════════════════════════════════════════════════════════


class WhisperTranscriber:
    """Wraps NVIDIA NIM Whisper STT for session transcription.

    In production, calls the NIM endpoint. Here, provides the interface
    and fallback logic.
    """

    def __init__(
        self,
        nim_endpoint: Optional[str] = None,
    ):
        self._endpoint = nim_endpoint or "http://localhost:8000/v1/audio/transcriptions"

    async def transcribe(
        self, recording_url: str
    ) -> list[dict[str, Any]]:
        """Transcribe a recording into timestamped segments.

        Returns list of segments: [{"start": "00:00:00", "end": "00:01:05", "text": "..."}]

        In production, calls NVIDIA NIM Whisper endpoint.
        Here, raises NotImplementedError to be mocked in tests.
        """
        raise NotImplementedError(
            "WhisperTranscriber.transcribe requires NVIDIA NIM endpoint"
        )


# ══════════════════════════════════════════════════════════════════════════════
# Unit 4 — Intelligence Extraction Engine (Lena)
# ══════════════════════════════════════════════════════════════════════════════


class IntelligenceExtractor:
    """Lena — Session Intelligence Analyst.

    Extracts structured intelligence from a session transcript.
    Key targets: insights, action items, emotional beats,
    topic clusters, breakthrough moments (DARN-CAT).
    """

    @staticmethod
    def extract_key_insights(
        transcript_segments: list[dict[str, Any]],
        min_insights: int = 3,
        max_insights: int = 7,
    ) -> list[KeyInsight]:
        """Extract key coaching moments from transcript.

        Identifies segments where coach's question provoked a
        significant client response (measured by response length
        and emotional markers).
        """
        insights: list[KeyInsight] = []
        for i, seg in enumerate(transcript_segments):
            speaker = seg.get("speaker", "unknown")
            text = seg.get("text", "")
            timestamp = seg.get("start", "00:00:00")

            # Coach question followed by substantial client response
            if speaker == "coach" and "?" in text and i + 1 < len(transcript_segments):
                next_seg = transcript_segments[i + 1]
                if next_seg.get("speaker") == "client" and len(next_seg.get("text", "")) > 30:
                    insights.append(KeyInsight(
                        timestamp=timestamp,
                        coach_statement=text,
                        client_response=next_seg["text"],
                        psychological_significance=_infer_significance(
                            text, next_seg["text"]
                        ),
                    ))

        # Respect min/max bounds
        if len(insights) < min_insights:
            # Pad with notable client statements as fallback
            for seg in transcript_segments:
                if len(insights) >= min_insights:
                    break
                if seg.get("speaker") == "client" and len(seg.get("text", "")) > 50:
                    insights.append(KeyInsight(
                        timestamp=seg.get("start", "00:00:00"),
                        coach_statement="[context]",
                        client_response=seg["text"],
                        psychological_significance="Notable client statement",
                    ))

        return insights[:max_insights]

    @staticmethod
    def extract_action_items(
        key_insights: list[KeyInsight],
        transcript_segments: list[dict[str, Any]],
        min_items: int = 2,
        max_items: int = 5,
    ) -> list[ActionItem]:
        """Extract action items using Gollwitzer Implementation Intentions.

        Format: "When [X], I will [Y]."
        """
        items: list[ActionItem] = []

        for seg in transcript_segments:
            text = seg.get("text", "").lower()
            # Detect implementation intention patterns
            if "when" in text and ("i will" in text or "i'll" in text):
                items.append(ActionItem(
                    implementation_intention=seg["text"],
                    context_premise_dimension="general",
                ))
            elif seg.get("speaker") == "client" and any(
                marker in text for marker in DARN_CAT_MARKERS[DarnCatCategory.COMMITMENT]
            ):
                items.append(ActionItem(
                    implementation_intention=seg["text"],
                    context_premise_dimension="general",
                ))

        # Generate from insights if not enough
        while len(items) < min_items and key_insights:
            insight = key_insights[len(items) % len(key_insights)]
            items.append(ActionItem(
                implementation_intention=(
                    f"When I notice {insight.psychological_significance.lower()}, "
                    f"I will pause and reflect on it."
                ),
                context_premise_dimension="general",
            ))

        return items[:max_items]

    @staticmethod
    def extract_emotional_beats(
        transcript_segments: list[dict[str, Any]],
    ) -> list[EmotionalBeat]:
        """Map emotional intensity timeline across the session.

        Uses word count, punctuation density, and emotion markers
        as proxy for emotional intensity.
        """
        beats: list[EmotionalBeat] = []
        for seg in transcript_segments:
            if seg.get("speaker") != "client":
                continue

            text = seg.get("text", "")
            timestamp = seg.get("start", "00:00:00")
            intensity = _compute_intensity(text)
            mood = _classify_mood(text, intensity)

            beats.append(EmotionalBeat(
                timestamp=timestamp,
                intensity=round(intensity, 2),
                mood_state=mood,
            ))
        return beats

    @staticmethod
    def extract_topic_clusters(
        transcript_segments: list[dict[str, Any]],
    ) -> list[str]:
        """Extract thematic categories as Context Premise dimensions."""
        from src.ccp.services.learning_path_builder import CONTEXT_PREMISE_DIMENSIONS

        found: set[str] = set()
        full_text = " ".join(
            seg.get("text", "") for seg in transcript_segments
        ).lower()

        # Simple keyword matching against Context Premise dimensions
        dimension_keywords: dict[str, list[str]] = {
            "fears": ["afraid", "fear", "scared", "worry", "anxious"],
            "enemies": ["enemy", "obstacle", "barrier", "block"],
            "dreams": ["dream", "hope", "vision", "aspire", "goal"],
            "hidden_beliefs": ["believe", "belief", "convince", "assume"],
            "daily_frustrations": ["frustrat", "annoy", "bother", "irritat"],
            "identity_crisis": ["identity", "who am i", "don't know who"],
            "secret_desires": ["secretly", "desire", "wish", "longing"],
            "misconceptions": ["misunderstand", "wrong about", "myth"],
            "failure_stories": ["failed", "failure", "didn't work", "gave up"],
            "success_stories": ["succeed", "success", "achieved", "accomplish"],
            "role_models": ["role model", "mentor", "look up to", "inspire"],
            "transformation_triggers": ["turning point", "moment", "realized", "changed"],
        }

        for dim, keywords in dimension_keywords.items():
            if dim in CONTEXT_PREMISE_DIMENSIONS:
                for kw in keywords:
                    if kw in full_text:
                        found.add(dim)
                        break

        return sorted(found) if found else ["general"]

    @staticmethod
    def detect_breakthrough_moments(
        transcript_segments: list[dict[str, Any]],
    ) -> list[BreakthroughMoment]:
        """Detect DARN-CAT change talk markers in client speech (AC6)."""
        moments: list[BreakthroughMoment] = []

        for seg in transcript_segments:
            if seg.get("speaker") != "client":
                continue

            text = seg.get("text", "").lower()
            timestamp = seg.get("start", "00:00:00")

            for category, markers in DARN_CAT_MARKERS.items():
                for marker in markers:
                    if marker in text:
                        moments.append(BreakthroughMoment(
                            timestamp=timestamp,
                            darn_cat_category=category,
                            raw_text=seg["text"],
                        ))
                        break  # One match per segment per category

        return moments


# ══════════════════════════════════════════════════════════════════════════════
# Unit 5 — Mind Map Generator (Benjamin)
# ══════════════════════════════════════════════════════════════════════════════


class MindMapGenerator:
    """Benjamin — generates session mind maps as Excalidraw structures.

    Central node = session title, branch nodes = topic clusters,
    leaf nodes = key insights (optional).
    """

    @staticmethod
    def generate(
        session_id: str,
        topic_clusters: list[str],
        key_insights: Optional[list[KeyInsight]] = None,
        emotional_beats: Optional[list[EmotionalBeat]] = None,
    ) -> SessionMindMap:
        """Build a mind map from session intelligence.

        AC5: Mind Map Integrity — nodes for all topic clusters,
        correct rendering structure.
        """
        nodes: list[MindMapNode] = []
        edges: list[MindMapEdge] = []

        # Central node
        central = MindMapNode(
            node_id="central",
            label=f"Session {session_id[:8]}",
            node_type="central",
            x=400.0,
            y=300.0,
        )
        nodes.append(central)

        # Topic cluster branch nodes
        angle_step = 360.0 / max(len(topic_clusters), 1)
        radius = 200.0
        for i, cluster in enumerate(topic_clusters):
            angle = math.radians(angle_step * i)
            x = 400.0 + radius * math.cos(angle)
            y = 300.0 + radius * math.sin(angle)

            # Color from emotional beats if available
            color = None
            if emotional_beats:
                avg_intensity = sum(b.intensity for b in emotional_beats) / len(
                    emotional_beats
                )
                color = _intensity_to_color(avg_intensity)

            node = MindMapNode(
                node_id=f"topic-{i}",
                label=cluster.replace("_", " ").title(),
                node_type="topic",
                x=round(x, 1),
                y=round(y, 1),
                color=color,
            )
            nodes.append(node)
            edges.append(MindMapEdge(from_id="central", to_id=f"topic-{i}"))

        return SessionMindMap(
            session_id=session_id,
            nodes=nodes,
            edges=edges,
        )


# ══════════════════════════════════════════════════════════════════════════════
# Unit 6 — Intelligence Propagation (Aria + CRAL)
# ══════════════════════════════════════════════════════════════════════════════


class IntelligencePropagator:
    """Propagates session intelligence to Context Premise (Aria) and CRAL.

    AC3: Context Premise Update — session topics → Neo4j graph.
    AC4: CRAL Feed — qualifying insights → CRAL Finding Index.
    AC6: Change Talk Detection → Change Talk Vault.
    """

    def __init__(
        self,
        neo4j_client: Any = None,
        cral_client: Any = None,
        change_talk_vault: Any = None,
    ):
        self._neo4j = neo4j_client
        self._cral = cral_client
        self._change_talk_vault = change_talk_vault

    def update_context_premise(
        self,
        client_id: str,
        topic_clusters: list[str],
        session_id: str,
    ) -> dict[str, Any]:
        """Update client's Context Premise in Neo4j (AC3).

        Returns the update metadata.
        """
        update = {
            "client_id": client_id,
            "session_id": session_id,
            "topic_clusters_added": topic_clusters,
            "source": "coaching_session",
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        if self._neo4j is not None:
            self._neo4j.update_context_premise(update)
        return update

    def feed_cral(
        self,
        coach_id: str,
        session_id: str,
        key_insights: list[KeyInsight],
    ) -> list[dict[str, Any]]:
        """Inject qualifying insights into CRAL Finding Index (AC4).

        Returns list of accepted CRAL entries.
        """
        cral_entries: list[dict[str, Any]] = []
        for insight in key_insights:
            # Check if insight significance qualifies for CRAL
            sig_score = _significance_score(insight.psychological_significance)
            if sig_score >= CRAL_INSIGHT_MIN_SIGNIFICANCE:
                entry = {
                    "session_id": session_id,
                    "coach_id": coach_id,
                    "timestamp": insight.timestamp,
                    "insight": insight.psychological_significance,
                    "source": "coaching_session",
                    "significance_score": sig_score,
                }
                cral_entries.append(entry)
                if self._cral is not None:
                    self._cral.inject_finding(entry)
        return cral_entries

    def detect_and_store_change_talk(
        self,
        client_id: str,
        session_id: str,
        breakthrough_moments: list[BreakthroughMoment],
    ) -> list[dict[str, Any]]:
        """Store breakthrough moments in Change Talk Vault (AC6)."""
        vault_entries: list[dict[str, Any]] = []
        for moment in breakthrough_moments:
            entry = {
                "client_id": client_id,
                "session_id": session_id,
                "timestamp": moment.timestamp,
                "darn_cat_category": moment.darn_cat_category.value,
                "raw_text": moment.raw_text,
                "source": "coaching_session",
            }
            vault_entries.append(entry)
            if self._change_talk_vault is not None:
                self._change_talk_vault.store(entry)
        return vault_entries


# ══════════════════════════════════════════════════════════════════════════════
# Unit 7 — Main Orchestrator (SessionRecapGenerator)
# ══════════════════════════════════════════════════════════════════════════════


class SessionRecapGenerator:
    """Full session recap pipeline orchestrator.

    Combines: Whisper STT → Lena extraction → Benjamin mind map →
    Aria Context Premise → CRAL feed → AFFiNE delivery → Telegram.

    AC1: End-to-End within 10 min SLA.
    """

    def __init__(
        self,
        coach_acronym: str,
        coach_id: str,
        transcriber: Optional[WhisperTranscriber] = None,
        affine_sync: Any = None,
        telegram_client: Any = None,
        neo4j_client: Any = None,
        cral_client: Any = None,
        change_talk_vault: Any = None,
        receipt_chain: Optional[ReceiptChain] = None,
    ):
        self.coach_acronym = coach_acronym.upper()
        self.coach_id = coach_id
        self._transcriber = transcriber or WhisperTranscriber()
        self._extractor = IntelligenceExtractor()
        self._mind_map_gen = MindMapGenerator()
        self._propagator = IntelligencePropagator(
            neo4j_client=neo4j_client,
            cral_client=cral_client,
            change_talk_vault=change_talk_vault,
        )
        self._affine_sync = affine_sync
        self._telegram = telegram_client
        self._receipt_chain = receipt_chain or ReceiptChain(
            coach_acronym=self.coach_acronym,
        )

    async def process_session(
        self,
        client_id: str,
        recording_url: str,
        transcript_segments: Optional[list[dict[str, Any]]] = None,
    ) -> SessionIntelligenceReport:
        """Full pipeline: recording → intelligence report.

        Steps:
        1. Transcribe (Whisper STT via NVIDIA NIM)
        2. Extract intelligence (Lena)
        3. Generate mind map (Benjamin)
        4. Propagate intelligence (Aria + CRAL)
        5. Deliver to AFFiNE + Telegram
        6. Write receipt
        """
        session_id = str(uuid.uuid4())

        # Stage 1: Transcription
        if transcript_segments is None:
            try:
                transcript_segments = await self._transcriber.transcribe(
                    recording_url
                )
            except Exception as exc:
                logger.error(
                    "[%s] Transcription failed: %s — queued for retry",
                    AGENT_LENA, exc,
                )
                # Fallback: return empty report marked for retry
                return SessionIntelligenceReport(
                    session_id=session_id,
                    coach_id=self.coach_id,
                    client_id=client_id,
                    recording_url=recording_url,
                    transcript_url="",
                )

        transcript_url = f"s3://{self.coach_acronym}/transcripts/{session_id}.json"

        # Stage 2: Intelligence Extraction (Lena)
        key_insights = self._extractor.extract_key_insights(transcript_segments)
        action_items = self._extractor.extract_action_items(
            key_insights, transcript_segments
        )
        emotional_beats = self._extractor.extract_emotional_beats(transcript_segments)
        topic_clusters = self._extractor.extract_topic_clusters(transcript_segments)
        breakthrough_moments = self._extractor.detect_breakthrough_moments(
            transcript_segments
        )

        # Stage 3: Mind Map (Benjamin)
        mind_map = self._mind_map_gen.generate(
            session_id, topic_clusters, key_insights, emotional_beats
        )
        mind_map_url = f"s3://{self.coach_acronym}/excalidraw/session_{session_id}_mindmap.json"

        # Stage 4: Intelligence Propagation
        self._propagator.update_context_premise(
            client_id, topic_clusters, session_id
        )
        self._propagator.feed_cral(
            self.coach_id, session_id, key_insights
        )
        self._propagator.detect_and_store_change_talk(
            client_id, session_id, breakthrough_moments
        )

        # Build report
        report = SessionIntelligenceReport(
            session_id=session_id,
            coach_id=self.coach_id,
            client_id=client_id,
            recording_url=recording_url,
            transcript_url=transcript_url,
            key_insights=key_insights,
            action_items=action_items,
            emotional_beats=emotional_beats,
            topic_clusters=topic_clusters,
            breakthrough_moments=breakthrough_moments,
            mind_map_url=mind_map_url,
        )

        # Stage 5: Delivery
        await self._deliver_to_affine(report)
        await self._deliver_to_telegram(client_id, report)

        # Stage 6: Receipt
        self._write_receipt(
            action="process_session",
            asset_id=f"SESSION-{session_id[:8]}",
            payload=report,
        )

        logger.info(
            "[%s] Session recap complete: %s → %d insights, %d actions, %d beats, %d clusters, %d breakthroughs",
            AGENT_LENA,
            session_id[:8],
            len(key_insights),
            len(action_items),
            len(emotional_beats),
            len(topic_clusters),
            len(breakthrough_moments),
        )

        return report

    async def _deliver_to_affine(
        self, report: SessionIntelligenceReport
    ) -> None:
        """Push Session Intelligence Report to AFFiNE Session Archive."""
        if self._affine_sync is not None:
            await self._affine_sync.push_session(report.model_dump(mode="json"))

    async def _deliver_to_telegram(
        self,
        client_id: str,
        report: SessionIntelligenceReport,
    ) -> None:
        """Send formatted client summary via Telegram."""
        if self._telegram is not None:
            summary = _format_telegram_summary(report)
            await self._telegram.send_message(client_id, summary)

    def _write_receipt(
        self, action: str, asset_id: str, payload: Any
    ) -> str:
        """Write receipt to Receipt Chain Guard."""
        if hasattr(payload, "model_dump"):
            data = payload.model_dump(mode="json")
        else:
            data = str(payload)
        payload_hash = hashlib.sha256(
            json.dumps(data, sort_keys=True, default=str).encode()
        ).hexdigest()

        entry = self._receipt_chain.log(
            agent_id=AGENT_LENA,
            action=action,
            asset_id=asset_id,
            input_summary=f"Session recap payload hash: {payload_hash}",
            output_summary="Session Intelligence Report generated",
            decision="extracted",
            metadata={"schema_ref": "DEP-ENG-041"},
        )
        return entry.receipt_id


# ══════════════════════════════════════════════════════════════════════════════
# Internal Helpers
# ══════════════════════════════════════════════════════════════════════════════


def _infer_significance(coach_statement: str, client_response: str) -> str:
    """Infer psychological significance from Q&A exchange."""
    # Simple heuristic: long, emotionally rich responses are more significant
    response_len = len(client_response)
    has_emotion = any(
        w in client_response.lower()
        for w in ["never", "always", "afraid", "realize", "feel", "believe"]
    )
    if response_len > 100 and has_emotion:
        return "Deep personal reflection — potential breakthrough moment"
    elif response_len > 60:
        return "Substantive client exploration"
    return "Client engagement with coaching prompt"


def _compute_intensity(text: str) -> float:
    """Compute emotional intensity proxy from text features."""
    word_count = len(text.split())
    exclamation_count = text.count("!")
    question_count = text.count("?")
    ellipsis_count = text.count("...")
    emotion_words = sum(
        1 for w in ["never", "always", "love", "hate", "afraid", "realize", "feel"]
        if w in text.lower()
    )

    # Normalize to 0.0 - 1.0
    raw = (
        min(word_count / 50.0, 1.0) * 0.3
        + min(exclamation_count / 3.0, 1.0) * 0.2
        + min(question_count / 3.0, 1.0) * 0.1
        + min(ellipsis_count / 2.0, 1.0) * 0.1
        + min(emotion_words / 3.0, 1.0) * 0.3
    )
    return min(raw, 1.0)


def _classify_mood(text: str, intensity: float) -> MoodState:
    """Classify mood state from text and intensity."""
    text_lower = text.lower()
    if any(w in text_lower for w in ["realize", "discover", "understand", "see now"]):
        return MoodState.DISCOVERY
    if any(w in text_lower for w in ["avoid", "escape", "run", "don't want"]):
        return MoodState.ESCAPE
    if any(w in text_lower for w in ["achieve", "succeed", "status", "prove"]):
        return MoodState.STATUS
    return MoodState.PROCESSING


def _significance_score(significance_text: str) -> float:
    """Score a significance statement for CRAL qualification."""
    text_lower = significance_text.lower()
    score = 0.5  # baseline
    if "breakthrough" in text_lower or "deep" in text_lower:
        score += 0.3
    if "potential" in text_lower or "reflection" in text_lower:
        score += 0.1
    if "engagement" in text_lower:
        score -= 0.1
    return min(score, 1.0)


def _intensity_to_color(intensity: float) -> str:
    """Map emotional intensity to a hex color (cool → warm)."""
    if intensity >= INTENSITY_HIGH:
        return "#FF6B6B"  # Warm red
    elif intensity >= INTENSITY_LOW:
        return "#FFA96B"  # Warm orange
    return "#6BCBFF"  # Cool blue


def _format_telegram_summary(report: SessionIntelligenceReport) -> str:
    """Format a Telegram-friendly session summary."""
    lines = ["📋 Session Recap Ready!\n"]

    if report.key_insights:
        lines.append("💡 Key Takeaways:")
        for i, insight in enumerate(report.key_insights[:3], 1):
            lines.append(f"  {i}. {insight.psychological_significance}")

    if report.action_items:
        lines.append("\n✅ Action Items:")
        for i, item in enumerate(report.action_items[:3], 1):
            lines.append(f"  {i}. {item.implementation_intention}")

    return "\n".join(lines)
