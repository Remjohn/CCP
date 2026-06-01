"""
FR-CA11-04 — Continuous Learning Path Builder Tests
=====================================================
Covers all 5 Acceptance Criteria:
  AC1: Auto-Classification — CCF script → registry entry with correct fields
  AC2: Journey Construction — 10 content pieces → DAG graphs with prereq edges
  AC3: Next-Content Recommendation — complete 3 nodes → correct successor
  AC4: Gating Respect — coping=1 → excludes content requiring coping≥2
  AC5: Cross-Pipeline Integration — CCF + V2WS + OBS → all in registry

Plus: model validation, DAG validation, coach isolation, SQL schema.
"""

from __future__ import annotations

import uuid
from typing import Any

import pytest

from src.ccp.models.ca11_models import (
    DIFFICULTY_LEVELS,
    DIFFICULTY_ORDER,
    LEARNING_CONTENT_TYPES,
    DifficultyLevel,
    JourneyEdge,
    JourneyNode,
    LearningContentType,
    LearningPathEntry,
    LearningProgressEntry,
    NextContentRecommendation,
    UnlockCondition,
)
from src.ccp.services.learning_path_builder import (
    AGENT_GABRIELLE,
    CONTEXT_PREMISE_DIMENSIONS,
    LEARNING_PATH_REGISTRY_SQL,
    LEARNING_PROGRESS_SQL,
    PIPELINE_CCF,
    PIPELINE_CMF,
    PIPELINE_CONTENT_TYPE_MAP,
    PIPELINE_OBS,
    PIPELINE_V2WS,
    ContentClassifier,
    JourneyConstructor,
    LearningPathBuilder,
    RecommendationEngine,
)


# ══════════════════════════════════════════════════════════════════════════════
# Fixtures
# ══════════════════════════════════════════════════════════════════════════════

COACH_ID = "uuid-coach-001"
COACH_ACRONYM = "JPR"
CLIENT_ID = "uuid-client-042"


def _make_prb(primary_dim: str, weight: float = 0.8) -> dict[str, Any]:
    """Create a Psychological Routing Brief with a primary dimension."""
    return {"active_dimensions": {primary_dim: weight}}


def _make_builder() -> LearningPathBuilder:
    return LearningPathBuilder(
        coach_acronym=COACH_ACRONYM,
        coach_id=COACH_ID,
    )


# ══════════════════════════════════════════════════════════════════════════════
# Test Constants & Enums
# ══════════════════════════════════════════════════════════════════════════════


class TestConstants:
    """Verify FR-CA11-04 constants and enums."""

    def test_content_type_count(self):
        assert len(LearningContentType) == 8

    def test_course_chapter_in_content_types(self):
        """CA11 Revision Decision 2: course_chapter must exist."""
        assert "course_chapter" in LEARNING_CONTENT_TYPES
        assert LearningContentType.COURSE_CHAPTER.value == "course_chapter"

    def test_difficulty_level_count(self):
        assert len(DifficultyLevel) == 3

    def test_difficulty_levels_set(self):
        assert DIFFICULTY_LEVELS == {"new", "developing", "loyal"}

    def test_difficulty_order(self):
        assert DIFFICULTY_ORDER[DifficultyLevel.NEW] == 0
        assert DIFFICULTY_ORDER[DifficultyLevel.DEVELOPING] == 1
        assert DIFFICULTY_ORDER[DifficultyLevel.LOYAL] == 2

    def test_context_premise_dimensions(self):
        assert len(CONTEXT_PREMISE_DIMENSIONS) == 12
        assert "fears" in CONTEXT_PREMISE_DIMENSIONS
        assert "transformation_triggers" in CONTEXT_PREMISE_DIMENSIONS


# ══════════════════════════════════════════════════════════════════════════════
# Test Models (DEP-ENG-074)
# ══════════════════════════════════════════════════════════════════════════════


class TestModels:
    """Verify DEP-ENG-074 LearningPathEntry schema."""

    def test_learning_path_entry_creation(self):
        entry = LearningPathEntry(
            asset_id="JP-CCF-20260324-005-SCRIPT",
            fingerprint_id="SKILL-RES-JP-DISC-PROM-NEW-20260324-005",
            coach_id=COACH_ID,
            content_type=LearningContentType.SCRIPT,
            topic_cluster="limiting_beliefs",
            difficulty_level=DifficultyLevel.DEVELOPING,
        )
        assert entry.content_id != ""
        assert entry.receipt_chain_guard.schema_ref == "DEP-ENG-041"

    def test_journey_node(self):
        node = JourneyNode(
            content_id="c1",
            asset_id="a1",
            title="Test",
            content_type=LearningContentType.VIDEO,
            difficulty_level=DifficultyLevel.NEW,
            topic_cluster="fears",
            sequence_position=0,
        )
        assert node.completed is False

    def test_journey_edge(self):
        edge = JourneyEdge(
            from_content_id="c1",
            to_content_id="c2",
        )
        assert edge.edge_type == "prerequisite"

    def test_learning_progress_entry(self):
        progress = LearningProgressEntry(
            client_id=CLIENT_ID,
            content_id="c1",
            journey_id="j1",
        )
        assert progress.completed_at != ""

    def test_next_content_recommendation(self):
        rec = NextContentRecommendation(
            content_id="c1",
            asset_id="a1",
            title="Test",
            content_type=LearningContentType.VIDEO,
            topic_cluster="fears",
            difficulty_level=DifficultyLevel.NEW,
        )
        assert rec.reason == "next_in_sequence"


# ══════════════════════════════════════════════════════════════════════════════
# Test Classification Logic
# ══════════════════════════════════════════════════════════════════════════════


class TestClassification:
    """Test Gabrielle's content classification engine."""

    def test_extract_topic_cluster_structured(self):
        prb = {"active_dimensions": {"fears": 0.9, "dreams": 0.3}}
        result = ContentClassifier.extract_topic_cluster(prb)
        assert result == "fears"

    def test_extract_topic_cluster_flat(self):
        prb = {"fears": 0.2, "hidden_beliefs": 0.8}
        result = ContentClassifier.extract_topic_cluster(prb)
        assert result == "hidden_beliefs"

    def test_extract_topic_cluster_empty(self):
        result = ContentClassifier.extract_topic_cluster({})
        assert result == "general"

    def test_map_difficulty_new(self):
        assert ContentClassifier.map_difficulty_level("new") == DifficultyLevel.NEW
        assert ContentClassifier.map_difficulty_level("cold") == DifficultyLevel.NEW
        assert ContentClassifier.map_difficulty_level("new_audience") == DifficultyLevel.NEW

    def test_map_difficulty_developing(self):
        assert ContentClassifier.map_difficulty_level("developing") == DifficultyLevel.DEVELOPING
        assert ContentClassifier.map_difficulty_level("warm") == DifficultyLevel.DEVELOPING

    def test_map_difficulty_loyal(self):
        assert ContentClassifier.map_difficulty_level("loyal") == DifficultyLevel.LOYAL
        assert ContentClassifier.map_difficulty_level("hot") == DifficultyLevel.LOYAL

    def test_map_difficulty_unknown_defaults_new(self):
        assert ContentClassifier.map_difficulty_level("unknown") == DifficultyLevel.NEW

    def test_infer_content_type_from_pipeline(self):
        assert ContentClassifier.infer_content_type(PIPELINE_CCF) == LearningContentType.SCRIPT
        assert ContentClassifier.infer_content_type(PIPELINE_V2WS) == LearningContentType.WEBINAR
        assert ContentClassifier.infer_content_type(PIPELINE_OBS) == LearningContentType.SESSION_RECAP
        assert ContentClassifier.infer_content_type(PIPELINE_CMF) == LearningContentType.COURSE_VIDEO

    def test_infer_content_type_explicit_override(self):
        result = ContentClassifier.infer_content_type(
            PIPELINE_CCF, explicit_type="course_chapter"
        )
        assert result == LearningContentType.COURSE_CHAPTER

    def test_full_classify(self):
        entry = ContentClassifier.classify(
            asset_id="JP-CCF-001",
            fingerprint_id="FP-001",
            coach_id=COACH_ID,
            pipeline_source=PIPELINE_CCF,
            psychological_routing_brief=_make_prb("dreams"),
            audience_maturity="developing",
            program_tag="90day-body",
        )
        assert entry.topic_cluster == "dreams"
        assert entry.difficulty_level == DifficultyLevel.DEVELOPING
        assert entry.content_type == LearningContentType.SCRIPT
        assert entry.program_tag == "90day-body"
        assert entry.coach_id == COACH_ID


# ══════════════════════════════════════════════════════════════════════════════
# AC1: Auto-Classification
# ══════════════════════════════════════════════════════════════════════════════


class TestAutoClassification:
    """AC1: Generate CCF script → registry entry with correct fields."""

    def test_classify_ccf_script(self):
        builder = _make_builder()
        entry = builder.classify_content(
            asset_id="JP-CCF-20260324-005-SCRIPT",
            fingerprint_id="SKILL-RES-JP-DISC-PROM-NEW-20260324-005",
            pipeline_source=PIPELINE_CCF,
            psychological_routing_brief=_make_prb("hidden_beliefs"),
            audience_maturity="developing",
        )
        assert entry.topic_cluster == "hidden_beliefs"
        assert entry.difficulty_level == DifficultyLevel.DEVELOPING
        assert entry.content_type == LearningContentType.SCRIPT
        assert entry.coach_id == COACH_ID

    def test_classify_adds_to_registry(self):
        builder = _make_builder()
        builder.classify_content(
            asset_id="A1",
            fingerprint_id="FP1",
            pipeline_source=PIPELINE_CCF,
            psychological_routing_brief=_make_prb("fears"),
            audience_maturity="new",
        )
        assert len(builder.get_registry()) == 1


# ══════════════════════════════════════════════════════════════════════════════
# AC2: Journey Construction
# ══════════════════════════════════════════════════════════════════════════════


class TestJourneyConstruction:
    """AC2: 10 content pieces across 3 topic clusters → 3 journey DAGs."""

    def _build_10_content_pieces(self) -> LearningPathBuilder:
        builder = _make_builder()
        # Topic 1: fears (4 pieces — new, new, developing, loyal)
        for i, mat in enumerate(["new", "new", "developing", "loyal"]):
            builder.classify_content(
                asset_id=f"FEARS-{i}",
                fingerprint_id=f"FP-F-{i}",
                pipeline_source=PIPELINE_CCF,
                psychological_routing_brief=_make_prb("fears"),
                audience_maturity=mat,
            )
        # Topic 2: dreams (3 pieces)
        for i, mat in enumerate(["new", "developing", "loyal"]):
            builder.classify_content(
                asset_id=f"DREAMS-{i}",
                fingerprint_id=f"FP-D-{i}",
                pipeline_source=PIPELINE_V2WS,
                psychological_routing_brief=_make_prb("dreams"),
                audience_maturity=mat,
            )
        # Topic 3: hidden_beliefs (3 pieces)
        for i, mat in enumerate(["new", "developing", "developing"]):
            builder.classify_content(
                asset_id=f"HB-{i}",
                fingerprint_id=f"FP-HB-{i}",
                pipeline_source=PIPELINE_OBS,
                psychological_routing_brief=_make_prb("hidden_beliefs"),
                audience_maturity=mat,
            )
        return builder

    def test_10_entries_in_registry(self):
        builder = self._build_10_content_pieces()
        assert len(builder.get_registry()) == 10

    def test_3_journeys_created(self):
        builder = self._build_10_content_pieces()
        journeys = builder.construct_journeys()
        assert len(journeys) == 3

    def test_journey_has_prerequisite_edges(self):
        builder = self._build_10_content_pieces()
        journeys = builder.construct_journeys()
        for journey_id, nodes, edges in journeys:
            # Each journey with N nodes has N-1 edges
            assert len(edges) == len(nodes) - 1

    def test_dag_is_valid(self):
        builder = self._build_10_content_pieces()
        journeys = builder.construct_journeys()
        for _, _, edges in journeys:
            assert JourneyConstructor.validate_dag(edges) is True

    def test_difficulty_ordering(self):
        """NEW content comes before DEVELOPING which comes before LOYAL."""
        builder = self._build_10_content_pieces()
        journeys = builder.construct_journeys()
        for _, nodes, _ in journeys:
            sorted_nodes = sorted(nodes, key=lambda n: n.sequence_position)
            for i in range(len(sorted_nodes) - 1):
                curr_order = DIFFICULTY_ORDER[sorted_nodes[i].difficulty_level]
                next_order = DIFFICULTY_ORDER[sorted_nodes[i + 1].difficulty_level]
                assert curr_order <= next_order

    def test_journey_ids_assigned_back(self):
        builder = self._build_10_content_pieces()
        builder.construct_journeys()
        for entry in builder.get_registry():
            assert entry.journey_id is not None
            assert entry.sequence_position is not None


# ══════════════════════════════════════════════════════════════════════════════
# AC3: Next-Content Recommendation
# ══════════════════════════════════════════════════════════════════════════════


class TestNextContentRecommendation:
    """AC3: Complete 3 nodes → correct DAG successor recommended."""

    def _setup_journey(self):
        builder = _make_builder()
        for i, mat in enumerate(["new", "new", "developing", "loyal", "loyal"]):
            builder.classify_content(
                asset_id=f"REC-{i}",
                fingerprint_id=f"FP-REC-{i}",
                pipeline_source=PIPELINE_CCF,
                psychological_routing_brief=_make_prb("fears"),
                audience_maturity=mat,
            )
        journeys = builder.construct_journeys()
        journey_id = journeys[0][0]
        nodes = journeys[0][1]
        return builder, journey_id, nodes

    def test_first_recommendation_is_first_node(self):
        builder, journey_id, nodes = self._setup_journey()
        rec = builder.recommend_next(CLIENT_ID, journey_id)
        assert rec is not None
        assert rec.content_id == nodes[0].content_id

    def test_after_completing_3_nodes(self):
        builder, journey_id, nodes = self._setup_journey()
        # Complete first 3 nodes
        for i in range(3):
            builder.record_completion(CLIENT_ID, nodes[i].content_id, journey_id)
        rec = builder.recommend_next(CLIENT_ID, journey_id)
        assert rec is not None
        assert rec.content_id == nodes[3].content_id

    def test_all_completed_returns_none(self):
        builder, journey_id, nodes = self._setup_journey()
        for node in nodes:
            builder.record_completion(CLIENT_ID, node.content_id, journey_id)
        rec = builder.recommend_next(CLIENT_ID, journey_id)
        assert rec is None


# ══════════════════════════════════════════════════════════════════════════════
# AC4: Gating Respect
# ══════════════════════════════════════════════════════════════════════════════


class TestGatingRespect:
    """AC4: Client at coping=1 → no content requiring coping≥2."""

    def test_gated_content_excluded(self):
        builder = _make_builder()
        # Entry 0: no gating (unlocked at coping=0)
        builder.classify_content(
            asset_id="GATED-0",
            fingerprint_id="FP-G-0",
            pipeline_source=PIPELINE_CCF,
            psychological_routing_brief=_make_prb("fears"),
            audience_maturity="new",
            unlock_condition=UnlockCondition(min_coping_position=0, min_atlas_week=0),
        )
        # Entry 1: requires coping≥2
        builder.classify_content(
            asset_id="GATED-1",
            fingerprint_id="FP-G-1",
            pipeline_source=PIPELINE_CCF,
            psychological_routing_brief=_make_prb("fears"),
            audience_maturity="developing",
            unlock_condition=UnlockCondition(min_coping_position=2, min_atlas_week=0),
        )
        journeys = builder.construct_journeys()
        journey_id = journeys[0][0]
        nodes = journeys[0][1]

        # Complete first node
        builder.record_completion(CLIENT_ID, nodes[0].content_id, journey_id)

        # Recommend at coping=1 → should NOT recommend entry 1
        rec = builder.recommend_next(
            CLIENT_ID, journey_id, coping_position=1, atlas_week=0
        )
        assert rec is None  # Entry 1 is gated, nothing else available

    def test_gated_content_accessible_when_condition_met(self):
        builder = _make_builder()
        builder.classify_content(
            asset_id="GATED-0",
            fingerprint_id="FP-G-0",
            pipeline_source=PIPELINE_CCF,
            psychological_routing_brief=_make_prb("fears"),
            audience_maturity="new",
            unlock_condition=UnlockCondition(min_coping_position=0, min_atlas_week=0),
        )
        builder.classify_content(
            asset_id="GATED-1",
            fingerprint_id="FP-G-1",
            pipeline_source=PIPELINE_CCF,
            psychological_routing_brief=_make_prb("fears"),
            audience_maturity="developing",
            unlock_condition=UnlockCondition(min_coping_position=2, min_atlas_week=0),
        )
        journeys = builder.construct_journeys()
        journey_id = journeys[0][0]
        nodes = journeys[0][1]

        builder.record_completion(CLIENT_ID, nodes[0].content_id, journey_id)

        # Recommend at coping=2 → SHOULD recommend
        rec = builder.recommend_next(
            CLIENT_ID, journey_id, coping_position=2, atlas_week=0
        )
        assert rec is not None
        assert rec.asset_id == "GATED-1"


# ══════════════════════════════════════════════════════════════════════════════
# AC5: Cross-Pipeline Integration
# ══════════════════════════════════════════════════════════════════════════════


class TestCrossPipelineIntegration:
    """AC5: CCF + V2WS + OBS → all in registry with correct content_type."""

    def test_ccf_hook(self):
        builder = _make_builder()
        scripts = [
            {
                "asset_id": f"CCF-{i}",
                "fingerprint_id": f"FP-CCF-{i}",
                "psychological_routing_brief": _make_prb("fears"),
                "audience_maturity": "new",
            }
            for i in range(3)
        ]
        entries = builder.on_ccf_batch_complete(scripts)
        assert len(entries) == 3
        assert all(e.content_type == LearningContentType.SCRIPT for e in entries)

    def test_v2ws_hook(self):
        builder = _make_builder()
        entry = builder.on_v2ws_complete({
            "asset_id": "V2WS-1",
            "fingerprint_id": "FP-V2WS-1",
            "psychological_routing_brief": _make_prb("dreams"),
            "audience_maturity": "developing",
        })
        assert entry.content_type == LearningContentType.WEBINAR

    def test_obs_hook(self):
        builder = _make_builder()
        entry = builder.on_obs_recap({
            "asset_id": "OBS-1",
            "fingerprint_id": "FP-OBS-1",
            "psychological_routing_brief": _make_prb("identity_crisis"),
            "audience_maturity": "loyal",
        })
        assert entry.content_type == LearningContentType.SESSION_RECAP

    def test_all_pipelines_in_registry(self):
        builder = _make_builder()
        builder.on_ccf_batch_complete([{
            "asset_id": "CCF-MIX",
            "fingerprint_id": "FP-CCF-MIX",
            "psychological_routing_brief": _make_prb("fears"),
            "audience_maturity": "new",
        }])
        builder.on_v2ws_complete({
            "asset_id": "V2WS-MIX",
            "fingerprint_id": "FP-V2WS-MIX",
            "psychological_routing_brief": _make_prb("dreams"),
            "audience_maturity": "developing",
        })
        builder.on_obs_recap({
            "asset_id": "OBS-MIX",
            "fingerprint_id": "FP-OBS-MIX",
            "psychological_routing_brief": _make_prb("hidden_beliefs"),
            "audience_maturity": "loyal",
        })
        registry = builder.get_registry()
        assert len(registry) == 3
        types = {e.content_type for e in registry}
        assert types == {
            LearningContentType.SCRIPT,
            LearningContentType.WEBINAR,
            LearningContentType.SESSION_RECAP,
        }


# ══════════════════════════════════════════════════════════════════════════════
# Coach Isolation (Safety Test)
# ══════════════════════════════════════════════════════════════════════════════


class TestCoachIsolation:
    """Cross-tenant safety: Coach A's content cannot enter Coach B's path."""

    def test_own_coach_entry_validates(self):
        builder = _make_builder()
        entry = builder.classify_content(
            asset_id="A1",
            fingerprint_id="FP1",
            pipeline_source=PIPELINE_CCF,
            psychological_routing_brief=_make_prb("fears"),
            audience_maturity="new",
        )
        assert builder.validate_coach_isolation(entry) is True

    def test_other_coach_entry_rejected(self):
        builder = _make_builder()
        foreign_entry = LearningPathEntry(
            asset_id="FOREIGN-1",
            fingerprint_id="FP-FOREIGN",
            coach_id="other-coach-id",
            content_type=LearningContentType.SCRIPT,
            topic_cluster="fears",
            difficulty_level=DifficultyLevel.NEW,
        )
        assert builder.validate_coach_isolation(foreign_entry) is False


# ══════════════════════════════════════════════════════════════════════════════
# DAG Validation
# ══════════════════════════════════════════════════════════════════════════════


class TestDAGValidation:
    """Verify DAG construction produces valid acyclic graphs."""

    def test_valid_dag(self):
        edges = [
            JourneyEdge(from_content_id="a", to_content_id="b"),
            JourneyEdge(from_content_id="b", to_content_id="c"),
        ]
        assert JourneyConstructor.validate_dag(edges) is True

    def test_cycle_detected(self):
        edges = [
            JourneyEdge(from_content_id="a", to_content_id="b"),
            JourneyEdge(from_content_id="b", to_content_id="c"),
            JourneyEdge(from_content_id="c", to_content_id="a"),
        ]
        assert JourneyConstructor.validate_dag(edges) is False

    def test_empty_dag(self):
        assert JourneyConstructor.validate_dag([]) is True


# ══════════════════════════════════════════════════════════════════════════════
# SQL Schema
# ══════════════════════════════════════════════════════════════════════════════


class TestSQLSchema:
    """Verify SQL schemas for learning_path_registry and learning_progress."""

    def test_registry_table_columns(self):
        assert "content_id" in LEARNING_PATH_REGISTRY_SQL
        assert "asset_id" in LEARNING_PATH_REGISTRY_SQL
        assert "fingerprint_id" in LEARNING_PATH_REGISTRY_SQL
        assert "coach_id" in LEARNING_PATH_REGISTRY_SQL
        assert "content_type" in LEARNING_PATH_REGISTRY_SQL
        assert "topic_cluster" in LEARNING_PATH_REGISTRY_SQL
        assert "difficulty_level" in LEARNING_PATH_REGISTRY_SQL
        assert "journey_id" in LEARNING_PATH_REGISTRY_SQL
        assert "course_chapter" in LEARNING_PATH_REGISTRY_SQL

    def test_progress_table_columns(self):
        assert "client_id" in LEARNING_PROGRESS_SQL
        assert "content_id" in LEARNING_PROGRESS_SQL
        assert "journey_id" in LEARNING_PROGRESS_SQL
        assert "completed_at" in LEARNING_PROGRESS_SQL
