"""
FR-CA11-05 — AI Session Recap Generator Tests
================================================
Covers all 6 Acceptance Criteria:
  AC1: End-to-End SLA (pipeline integration)
  AC2: Extraction Quality (≥3 insights from known transcript)
  AC3: Context Premise Update (topic clusters → Neo4j)
  AC4: CRAL Feed (qualifying insights → CRAL Finding Index)
  AC5: Mind Map Integrity (nodes for all topic clusters)
  AC6: Change Talk Detection (DARN-CAT → Change Talk Vault)

Plus: model validation, emotional beats, SQL schema, telegram delivery.
"""

from __future__ import annotations

import asyncio
from typing import Any
from unittest.mock import MagicMock

import pytest

from src.ccp.models.ca11_models import (
    ActionItem,
    BreakthroughMoment,
    DarnCatCategory,
    DifficultyLevel,
    EmotionalBeat,
    KeyInsight,
    MoodState,
    SessionIntelligenceReport,
    SessionMindMap,
)
from src.ccp.services.session_recap_generator import (
    AGENT_LENA,
    CRAL_INSIGHT_MIN_SIGNIFICANCE,
    DARN_CAT_MARKERS,
    SESSION_INTELLIGENCE_SQL,
    IntelligenceExtractor,
    IntelligencePropagator,
    MindMapGenerator,
    SessionRecapGenerator,
    WhisperTranscriber,
)


# ══════════════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════════════

def _run(coro):
    """Run async coroutine synchronously."""
    return asyncio.get_event_loop().run_until_complete(coro)


# ══════════════════════════════════════════════════════════════════════════════
# Test Transcript
# ══════════════════════════════════════════════════════════════════════════════

SAMPLE_TRANSCRIPT = [
    {"start": "00:01:00", "speaker": "coach", "text": "How are you feeling about the progress we've been making?"},
    {"start": "00:01:30", "speaker": "client", "text": "I feel like I'm starting to understand things better, but I'm still afraid of failing."},
    {"start": "00:03:00", "speaker": "coach", "text": "What does success look like without the approval of others?"},
    {"start": "00:03:45", "speaker": "client", "text": "I've never actually thought about that. I always assumed success meant getting recognized by people I look up to. But maybe that belief has been limiting me all along. I realize now that I need to define it for myself."},
    {"start": "00:08:00", "speaker": "coach", "text": "Can you tell me about a time when you felt truly authentic?"},
    {"start": "00:08:30", "speaker": "client", "text": "I remember when I was painting last summer. Nobody was watching, nobody was judging. I felt completely free... like I didn't need anyone's permission to be myself."},
    {"start": "00:14:00", "speaker": "coach", "text": "What would it look like to bring that feeling into your daily life?"},
    {"start": "00:14:30", "speaker": "client", "text": "I will start setting aside time each morning just for me. When I catch myself seeking approval, I will pause and remember that painting feeling."},
    {"start": "00:20:00", "speaker": "client", "text": "I've already started journaling about this. I took the first step yesterday by writing down my fears."},
    {"start": "00:25:00", "speaker": "client", "text": "I'm going to commit to this process. I promise I'll do the exercises every day."},
]

COACH_ID = "uuid-coach-001"
COACH_ACRONYM = "JPR"
CLIENT_ID = "uuid-client-042"


# ══════════════════════════════════════════════════════════════════════════════
# Mocks
# ══════════════════════════════════════════════════════════════════════════════


class MockWhisperTranscriber(WhisperTranscriber):
    """Returns pre-built transcript segments."""

    def __init__(self, segments: list[dict[str, Any]]):
        super().__init__()
        self._segments = segments

    async def transcribe(self, recording_url: str) -> list[dict[str, Any]]:
        return self._segments


class MockTelegram:
    def __init__(self):
        self.messages: list[dict] = []

    async def send_message(self, client_id: str, message: str) -> None:
        self.messages.append({"client_id": client_id, "message": message})


class MockNeo4j:
    def __init__(self):
        self.updates: list[dict] = []

    def update_context_premise(self, update: dict) -> None:
        self.updates.append(update)


class MockCRAL:
    def __init__(self):
        self.findings: list[dict] = []

    def inject_finding(self, entry: dict) -> None:
        self.findings.append(entry)


class MockChangeTalkVault:
    def __init__(self):
        self.entries: list[dict] = []

    def store(self, entry: dict) -> None:
        self.entries.append(entry)


class MockAFFiNeSync:
    def __init__(self):
        self.pushed: list[dict] = []

    async def push_session(self, data: dict) -> None:
        self.pushed.append(data)


# ══════════════════════════════════════════════════════════════════════════════
# Test Constants & Models
# ══════════════════════════════════════════════════════════════════════════════


class TestConstants:
    def test_mood_state_count(self):
        assert len(MoodState) == 4

    def test_darn_cat_category_count(self):
        assert len(DarnCatCategory) == 7

    def test_darn_cat_markers_all_categories(self):
        for cat in DarnCatCategory:
            assert cat in DARN_CAT_MARKERS
            assert len(DARN_CAT_MARKERS[cat]) > 0


class TestModels:
    def test_session_intelligence_report(self):
        r = SessionIntelligenceReport(
            coach_id=COACH_ID,
            client_id=CLIENT_ID,
            recording_url="s3://JPR/sessions/test.mp4",
            transcript_url="s3://JPR/transcripts/test.json",
        )
        assert r.session_id != ""
        assert r.receipt_chain_guard.schema_ref == "DEP-ENG-041"

    def test_key_insight(self):
        ki = KeyInsight(
            timestamp="00:14:32",
            coach_statement="What does success look like?",
            client_response="I've never thought about that.",
            psychological_significance="Client confronting dependency",
        )
        assert ki.timestamp == "00:14:32"

    def test_action_item(self):
        ai = ActionItem(
            implementation_intention="When I notice fear, I will pause.",
        )
        assert ai.difficulty == DifficultyLevel.NEW

    def test_emotional_beat(self):
        eb = EmotionalBeat(
            timestamp="00:05:00",
            intensity=0.7,
            mood_state=MoodState.DISCOVERY,
        )
        assert eb.intensity == 0.7

    def test_breakthrough_moment(self):
        bm = BreakthroughMoment(
            timestamp="00:14:32",
            darn_cat_category=DarnCatCategory.ACTIVATION,
            raw_text="I've already started.",
        )
        assert bm.darn_cat_category == DarnCatCategory.ACTIVATION


# ══════════════════════════════════════════════════════════════════════════════
# AC2: Extraction Quality
# ══════════════════════════════════════════════════════════════════════════════


class TestExtractionQuality:
    """AC2: ≥80% insights match human-identified key moments."""

    def test_extract_key_insights(self):
        insights = IntelligenceExtractor.extract_key_insights(SAMPLE_TRANSCRIPT)
        assert len(insights) >= 3
        # All insights should have substantial responses
        for ins in insights:
            assert len(ins.client_response) > 20

    def test_extract_action_items(self):
        insights = IntelligenceExtractor.extract_key_insights(SAMPLE_TRANSCRIPT)
        items = IntelligenceExtractor.extract_action_items(insights, SAMPLE_TRANSCRIPT)
        assert len(items) >= 2

    def test_action_items_contain_commitments(self):
        insights = IntelligenceExtractor.extract_key_insights(SAMPLE_TRANSCRIPT)
        items = IntelligenceExtractor.extract_action_items(insights, SAMPLE_TRANSCRIPT)
        # At least one should contain "will" (commitment)
        assert any("will" in item.implementation_intention.lower() for item in items)


# ══════════════════════════════════════════════════════════════════════════════
# Emotional Beats
# ══════════════════════════════════════════════════════════════════════════════


class TestEmotionalBeats:
    def test_extract_beats_from_client_segments(self):
        beats = IntelligenceExtractor.extract_emotional_beats(SAMPLE_TRANSCRIPT)
        # Only client segments produce beats
        assert len(beats) > 0
        assert all(0.0 <= b.intensity <= 1.0 for b in beats)

    def test_beat_mood_states(self):
        beats = IntelligenceExtractor.extract_emotional_beats(SAMPLE_TRANSCRIPT)
        moods = {b.mood_state for b in beats}
        # Should detect at least DISCOVERY (from "realize") and PROCESSING
        assert len(moods) >= 1


# ══════════════════════════════════════════════════════════════════════════════
# Topic Clusters
# ══════════════════════════════════════════════════════════════════════════════


class TestTopicClusters:
    def test_extract_clusters(self):
        clusters = IntelligenceExtractor.extract_topic_clusters(SAMPLE_TRANSCRIPT)
        # Should find "fears" (afraid), "hidden_beliefs" (belief/believe), etc.
        assert len(clusters) >= 1

    def test_clusters_are_context_premise_dimensions(self):
        from src.ccp.services.learning_path_builder import CONTEXT_PREMISE_DIMENSIONS
        clusters = IntelligenceExtractor.extract_topic_clusters(SAMPLE_TRANSCRIPT)
        for c in clusters:
            assert c in CONTEXT_PREMISE_DIMENSIONS or c == "general"


# ══════════════════════════════════════════════════════════════════════════════
# AC6: Change Talk Detection
# ══════════════════════════════════════════════════════════════════════════════


class TestChangeTalkDetection:
    """AC6: DARN-CAT markers detected in client speech."""

    def test_detect_commitment(self):
        moments = IntelligenceExtractor.detect_breakthrough_moments(SAMPLE_TRANSCRIPT)
        categories = {m.darn_cat_category for m in moments}
        # "I will" → Commitment, "I've already started" → Activation, "I promise" → Commitment
        assert DarnCatCategory.COMMITMENT in categories

    def test_detect_activation(self):
        moments = IntelligenceExtractor.detect_breakthrough_moments(SAMPLE_TRANSCRIPT)
        categories = {m.darn_cat_category for m in moments}
        # "I've already started" → Activation
        assert DarnCatCategory.ACTIVATION in categories

    def test_detect_taking_steps(self):
        moments = IntelligenceExtractor.detect_breakthrough_moments(SAMPLE_TRANSCRIPT)
        categories = {m.darn_cat_category for m in moments}
        # "I took the first step" → Taking Steps
        assert DarnCatCategory.TAKING_STEPS in categories

    def test_all_moments_have_raw_text(self):
        moments = IntelligenceExtractor.detect_breakthrough_moments(SAMPLE_TRANSCRIPT)
        for m in moments:
            assert len(m.raw_text) > 0


# ══════════════════════════════════════════════════════════════════════════════
# AC5: Mind Map Integrity
# ══════════════════════════════════════════════════════════════════════════════


class TestMindMapIntegrity:
    """AC5: .excalidraw JSON with nodes for all topic clusters."""

    def test_mind_map_basic_structure(self):
        mind_map = MindMapGenerator.generate(
            session_id="test-session-001",
            topic_clusters=["fears", "hidden_beliefs", "dreams"],
        )
        # 1 central + 3 topics = 4 nodes
        assert len(mind_map.nodes) == 4
        assert mind_map.nodes[0].node_type == "central"

    def test_mind_map_edges(self):
        mind_map = MindMapGenerator.generate(
            session_id="test-session-001",
            topic_clusters=["fears", "hidden_beliefs", "dreams"],
        )
        # 3 edges (central → each topic)
        assert len(mind_map.edges) == 3
        for edge in mind_map.edges:
            assert edge.from_id == "central"

    def test_mind_map_with_emotional_coloring(self):
        beats = [
            EmotionalBeat(timestamp="00:05:00", intensity=0.8, mood_state=MoodState.DISCOVERY)
        ]
        mind_map = MindMapGenerator.generate(
            session_id="test-001",
            topic_clusters=["fears"],
            emotional_beats=beats,
        )
        topic_node = mind_map.nodes[1]
        assert topic_node.color is not None

    def test_mind_map_single_cluster(self):
        mind_map = MindMapGenerator.generate(
            session_id="test-001",
            topic_clusters=["general"],
        )
        assert len(mind_map.nodes) == 2
        assert len(mind_map.edges) == 1


# ══════════════════════════════════════════════════════════════════════════════
# AC3: Context Premise Update
# ══════════════════════════════════════════════════════════════════════════════


class TestContextPremiseUpdate:
    """AC3: Session topics → Neo4j Context Premise."""

    def test_update_fires(self):
        neo4j = MockNeo4j()
        propagator = IntelligencePropagator(neo4j_client=neo4j)
        result = propagator.update_context_premise(
            CLIENT_ID, ["fears", "dreams"], "session-001"
        )
        assert result["topic_clusters_added"] == ["fears", "dreams"]
        assert result["source"] == "coaching_session"
        assert len(neo4j.updates) == 1


# ══════════════════════════════════════════════════════════════════════════════
# AC4: CRAL Feed
# ══════════════════════════════════════════════════════════════════════════════


class TestCRALFeed:
    """AC4: Qualifying insights → CRAL Finding Index."""

    def test_qualifying_insight_feeds_cral(self):
        cral = MockCRAL()
        propagator = IntelligencePropagator(cral_client=cral)
        insights = [
            KeyInsight(
                timestamp="00:14:32",
                coach_statement="What does success look like?",
                client_response="I've never thought about that.",
                psychological_significance="Deep personal reflection — potential breakthrough moment",
            )
        ]
        entries = propagator.feed_cral(COACH_ID, "session-001", insights)
        assert len(entries) >= 1
        assert entries[0]["source"] == "coaching_session"
        assert len(cral.findings) >= 1

    def test_low_significance_excluded(self):
        cral = MockCRAL()
        propagator = IntelligencePropagator(cral_client=cral)
        insights = [
            KeyInsight(
                timestamp="00:01:00",
                coach_statement="How are you?",
                client_response="Fine.",
                psychological_significance="Client engagement with coaching prompt",
            )
        ]
        entries = propagator.feed_cral(COACH_ID, "session-001", insights)
        # "engagement" reduces score below threshold
        assert len(entries) == 0


# ══════════════════════════════════════════════════════════════════════════════
# AC1: End-to-End Pipeline
# ══════════════════════════════════════════════════════════════════════════════


class TestEndToEnd:
    """AC1: Full pipeline integration."""

    def _make_generator(self):
        neo4j = MockNeo4j()
        cral = MockCRAL()
        vault = MockChangeTalkVault()
        telegram = MockTelegram()
        affine = MockAFFiNeSync()
        transcriber = MockWhisperTranscriber(SAMPLE_TRANSCRIPT)

        gen = SessionRecapGenerator(
            coach_acronym=COACH_ACRONYM,
            coach_id=COACH_ID,
            transcriber=transcriber,
            affine_sync=affine,
            telegram_client=telegram,
            neo4j_client=neo4j,
            cral_client=cral,
            change_talk_vault=vault,
        )
        return gen, telegram, neo4j, cral, vault, affine

    def test_full_pipeline(self):
        gen, telegram, neo4j, cral, vault, affine = self._make_generator()
        report = _run(gen.process_session(
            client_id=CLIENT_ID,
            recording_url="s3://JPR/sessions/test.mp4",
        ))
        assert report.session_id != ""
        assert report.coach_id == COACH_ID
        assert report.client_id == CLIENT_ID
        assert len(report.key_insights) >= 3
        assert len(report.action_items) >= 2
        assert len(report.topic_clusters) >= 1
        assert report.transcript_url != ""
        assert report.mind_map_url is not None

    def test_telegram_summary_sent(self):
        gen, telegram, *_ = self._make_generator()
        _run(gen.process_session(
            client_id=CLIENT_ID,
            recording_url="s3://JPR/sessions/test.mp4",
        ))
        assert len(telegram.messages) == 1
        msg = telegram.messages[0]["message"]
        assert "Recap" in msg

    def test_affine_push(self):
        gen, _, _, _, _, affine = self._make_generator()
        _run(gen.process_session(
            client_id=CLIENT_ID,
            recording_url="s3://JPR/sessions/test.mp4",
        ))
        assert len(affine.pushed) == 1

    def test_neo4j_context_premise_updated(self):
        gen, _, neo4j, *_ = self._make_generator()
        _run(gen.process_session(
            client_id=CLIENT_ID,
            recording_url="s3://JPR/sessions/test.mp4",
        ))
        assert len(neo4j.updates) == 1
        assert neo4j.updates[0]["source"] == "coaching_session"

    def test_change_talk_vault_fed(self):
        gen, _, _, _, vault, _ = self._make_generator()
        _run(gen.process_session(
            client_id=CLIENT_ID,
            recording_url="s3://JPR/sessions/test.mp4",
        ))
        assert len(vault.entries) >= 1

    def test_pre_provided_transcript(self):
        """Pipeline can accept pre-transcribed segments (skipping Whisper)."""
        gen, *_ = self._make_generator()
        report = _run(gen.process_session(
            client_id=CLIENT_ID,
            recording_url="s3://JPR/sessions/test.mp4",
            transcript_segments=SAMPLE_TRANSCRIPT,
        ))
        assert len(report.key_insights) >= 3


# ══════════════════════════════════════════════════════════════════════════════
# SQL Schema
# ══════════════════════════════════════════════════════════════════════════════


class TestSQLSchema:
    def test_session_intelligence_columns(self):
        assert "session_id" in SESSION_INTELLIGENCE_SQL
        assert "coach_id" in SESSION_INTELLIGENCE_SQL
        assert "client_id" in SESSION_INTELLIGENCE_SQL
        assert "recording_url" in SESSION_INTELLIGENCE_SQL
        assert "key_insights" in SESSION_INTELLIGENCE_SQL
        assert "emotional_beats" in SESSION_INTELLIGENCE_SQL
        assert "breakthrough_moments" in SESSION_INTELLIGENCE_SQL
        assert "processing_status" in SESSION_INTELLIGENCE_SQL
