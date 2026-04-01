"""
CCP FR-CA11-04 — Continuous Learning Path Builder
DEP-ENG-074 PROPOSED

Agent: Gabrielle (Learning Path Agent, Strategy Department)

Auto-classifies every content piece from CCP pipelines (CCF, V²WS,
CBCS, OBS, CMF) by topic cluster, difficulty level, and program tag.
Content is organized into DAG-based learning journeys. Next-content
recommendations respect coping/atlas gating.

Spec reference: FR-CA11-04_Learning_Path_Builder_Tech_Spec.md
  §4 — Stage 1: Registry Table & Classification Logic
  §4 — Stage 2: Journey Construction (DAG)
  §4 — Stage 3: Next-Content Recommendation
  §5 — DEP-ENG-074 PROPOSED (LearningPathEntry)
  §6 — Backward Compatibility: classification failure fallback
  §7 — Tasks 1-7
  §8 — AC1-AC5

Architecture references:
  ADR-01: Single-Tenant Isolated Cloud-Native Instances
  DEP-ENG-006: Context Premise Map (topic clusters)
  DEP-ENG-017: Audience Maturity Profile (difficulty levels)
  DEP-ENG-020: Fingerprint Archive Index (traceability)
  DEP-ENG-040: Universal Asset ID (content linking)
  DEP-ENG-041: Receipt Chain Guard (mandatory on mutations)
  FR-CA11-03: Client Workspace (displays learning paths — Noémie)
"""

from __future__ import annotations

import hashlib
import json
import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.ca11_models import (
    DIFFICULTY_ORDER,
    DifficultyLevel,
    JourneyEdge,
    JourneyNode,
    LearningContentType,
    LearningPathEntry,
    LearningProgressEntry,
    NextContentRecommendation,
    ReceiptChainGuardRef,
    UnlockCondition,
)

logger = logging.getLogger(__name__)

# ── Constants ─────────────────────────────────────────────────────────────────

AGENT_GABRIELLE = "Gabrielle"

# Context Premise Map dimensions (DEP-ENG-006) for topic cluster mapping
CONTEXT_PREMISE_DIMENSIONS: list[str] = [
    "fears", "enemies", "dreams", "hidden_beliefs",
    "daily_frustrations", "identity_crisis", "secret_desires",
    "misconceptions", "failure_stories", "success_stories",
    "role_models", "transformation_triggers",
]

# Pipeline source identifiers
PIPELINE_CCF = "ccf"
PIPELINE_V2WS = "v2ws"
PIPELINE_OBS = "obs"
PIPELINE_CBCS = "cbcs"
PIPELINE_CMF = "cmf"

# Content type mapping from pipeline source
PIPELINE_CONTENT_TYPE_MAP: dict[str, LearningContentType] = {
    PIPELINE_CCF: LearningContentType.SCRIPT,
    PIPELINE_V2WS: LearningContentType.WEBINAR,
    PIPELINE_OBS: LearningContentType.SESSION_RECAP,
    PIPELINE_CBCS: LearningContentType.VOICE_LESSON,
    PIPELINE_CMF: LearningContentType.COURSE_VIDEO,
}


# ── SQL Schemas ───────────────────────────────────────────────────────────────
# Task 1 & Task 2

LEARNING_PATH_REGISTRY_SQL = """
CREATE TABLE IF NOT EXISTS learning_path_registry (
    content_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id TEXT NOT NULL,
    fingerprint_id TEXT NOT NULL,
    coach_id UUID NOT NULL,
    content_type TEXT NOT NULL
        CHECK (content_type IN (
            'script', 'video', 'voice_lesson', 'webinar',
            'session_recap', 'diagram', 'course_video', 'course_chapter'
        )),
    topic_cluster TEXT NOT NULL,
    difficulty_level TEXT NOT NULL
        CHECK (difficulty_level IN ('new', 'developing', 'loyal')),
    program_tag TEXT,
    journey_id UUID,
    sequence_position INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    unlock_condition JSONB,
    receipt_hash TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_lpr_coach_id ON learning_path_registry(coach_id);
CREATE INDEX IF NOT EXISTS idx_lpr_journey_id ON learning_path_registry(journey_id);
CREATE INDEX IF NOT EXISTS idx_lpr_topic ON learning_path_registry(topic_cluster);
"""

LEARNING_PROGRESS_SQL = """
CREATE TABLE IF NOT EXISTS learning_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID NOT NULL,
    content_id UUID NOT NULL REFERENCES learning_path_registry(content_id),
    journey_id UUID NOT NULL,
    completed_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(client_id, content_id)
);

CREATE INDEX IF NOT EXISTS idx_lp_client ON learning_progress(client_id);
CREATE INDEX IF NOT EXISTS idx_lp_journey ON learning_progress(journey_id);
"""


# ══════════════════════════════════════════════════════════════════════════════
# Unit 3 — Classification Logic (Gabrielle)
# ══════════════════════════════════════════════════════════════════════════════


class ContentClassifier:
    """Gabrielle's classification engine.

    Extracts topic cluster from Context Premise Map dimensions
    and maps difficulty level from Audience Maturity Profile.
    """

    @staticmethod
    def extract_topic_cluster(
        psychological_routing_brief: dict[str, Any],
    ) -> str:
        """Extract primary topic cluster from a Psychological Routing Brief.

        The PRB is generated during content creation and contains the
        active Context Premise Map dimensions. We pick the highest-weight
        dimension as the topic cluster.

        If no valid dimension found, falls back to 'general'.
        """
        if not psychological_routing_brief:
            return "general"

        dimensions = psychological_routing_brief.get("active_dimensions", {})
        if not dimensions:
            # Try flat key lookup
            best_dim = "general"
            best_weight = 0.0
            for dim in CONTEXT_PREMISE_DIMENSIONS:
                weight = psychological_routing_brief.get(dim, 0.0)
                if isinstance(weight, (int, float)) and weight > best_weight:
                    best_weight = weight
                    best_dim = dim
            return best_dim

        # Structured format: {"dimension": weight}
        best_dim = "general"
        best_weight = 0.0
        for dim, weight in dimensions.items():
            if dim in CONTEXT_PREMISE_DIMENSIONS and weight > best_weight:
                best_weight = weight
                best_dim = dim
        return best_dim

    @staticmethod
    def map_difficulty_level(
        audience_maturity: str,
    ) -> DifficultyLevel:
        """Map Audience Maturity Profile (FR20) to difficulty level.

        Mapping:
          new_audience / cold → DifficultyLevel.NEW
          developing / warm → DifficultyLevel.DEVELOPING
          loyal / hot → DifficultyLevel.LOYAL

        Falls back to NEW if unrecognized.
        """
        maturity_lower = audience_maturity.strip().lower()
        mapping: dict[str, DifficultyLevel] = {
            "new": DifficultyLevel.NEW,
            "new_audience": DifficultyLevel.NEW,
            "cold": DifficultyLevel.NEW,
            "developing": DifficultyLevel.DEVELOPING,
            "warm": DifficultyLevel.DEVELOPING,
            "loyal": DifficultyLevel.LOYAL,
            "hot": DifficultyLevel.LOYAL,
        }
        return mapping.get(maturity_lower, DifficultyLevel.NEW)

    @staticmethod
    def infer_content_type(
        pipeline_source: str,
        explicit_type: Optional[str] = None,
    ) -> LearningContentType:
        """Infer content type from pipeline source.

        CA11 Revision Decision 2: course_chapter is a valid content type.
        """
        if explicit_type:
            try:
                return LearningContentType(explicit_type)
            except ValueError:
                pass

        return PIPELINE_CONTENT_TYPE_MAP.get(
            pipeline_source,
            LearningContentType.SCRIPT,
        )

    @staticmethod
    def classify(
        asset_id: str,
        fingerprint_id: str,
        coach_id: str,
        pipeline_source: str,
        psychological_routing_brief: dict[str, Any],
        audience_maturity: str,
        program_tag: Optional[str] = None,
        explicit_content_type: Optional[str] = None,
        unlock_condition: Optional[UnlockCondition] = None,
    ) -> LearningPathEntry:
        """Full classification pipeline — produces a LearningPathEntry."""
        topic_cluster = ContentClassifier.extract_topic_cluster(
            psychological_routing_brief
        )
        difficulty_level = ContentClassifier.map_difficulty_level(
            audience_maturity
        )
        content_type = ContentClassifier.infer_content_type(
            pipeline_source, explicit_content_type
        )
        return LearningPathEntry(
            asset_id=asset_id,
            fingerprint_id=fingerprint_id,
            coach_id=coach_id,
            content_type=content_type,
            topic_cluster=topic_cluster,
            difficulty_level=difficulty_level,
            program_tag=program_tag,
            unlock_condition=unlock_condition,
        )


# ══════════════════════════════════════════════════════════════════════════════
# Unit 4 — Journey Construction (DAG)
# ══════════════════════════════════════════════════════════════════════════════


class JourneyConstructor:
    """Builds learning journey DAGs from registry entries.

    Groups content by topic_cluster, orders by difficulty_level
    then created_at, and creates prerequisite edges.

    In production, stores to Neo4j. Here, operates on in-memory
    data structures with the same logic.
    """

    @staticmethod
    def group_by_topic(
        entries: list[LearningPathEntry],
    ) -> dict[str, list[LearningPathEntry]]:
        """Group registry entries by topic cluster."""
        groups: dict[str, list[LearningPathEntry]] = {}
        for entry in entries:
            groups.setdefault(entry.topic_cluster, []).append(entry)
        return groups

    @staticmethod
    def order_within_topic(
        entries: list[LearningPathEntry],
    ) -> list[LearningPathEntry]:
        """Order entries within a topic by difficulty then created_at.

        Difficulty order: new (0) → developing (1) → loyal (2).
        Within same difficulty: chronological by created_at.
        """
        return sorted(
            entries,
            key=lambda e: (
                DIFFICULTY_ORDER.get(e.difficulty_level, 0),
                e.created_at,
            ),
        )

    @staticmethod
    def build_journey(
        topic_cluster: str,
        entries: list[LearningPathEntry],
        coach_id: str,
    ) -> tuple[str, list[JourneyNode], list[JourneyEdge]]:
        """Build a journey DAG for a topic cluster.

        Returns (journey_id, nodes, edges).
        Edges enforce: FOUNDATIONS → DEVELOPING → LOYAL ordering.
        """
        journey_id = str(uuid.uuid4())
        ordered = JourneyConstructor.order_within_topic(entries)

        nodes: list[JourneyNode] = []
        edges: list[JourneyEdge] = []

        for pos, entry in enumerate(ordered):
            node = JourneyNode(
                content_id=entry.content_id,
                asset_id=entry.asset_id,
                title=f"{entry.topic_cluster}:{entry.content_type.value}:{pos}",
                content_type=entry.content_type,
                difficulty_level=entry.difficulty_level,
                topic_cluster=entry.topic_cluster,
                sequence_position=pos,
            )
            nodes.append(node)

            # Assign journey metadata back to entry
            entry.journey_id = journey_id
            entry.sequence_position = pos

            # Create prerequisite edge from previous node
            if pos > 0:
                prev_entry = ordered[pos - 1]
                edge = JourneyEdge(
                    from_content_id=prev_entry.content_id,
                    to_content_id=entry.content_id,
                )
                edges.append(edge)

        return journey_id, nodes, edges

    @staticmethod
    def build_all_journeys(
        entries: list[LearningPathEntry],
        coach_id: str,
    ) -> list[tuple[str, list[JourneyNode], list[JourneyEdge]]]:
        """Build journey DAGs for all topic clusters.

        Returns list of (journey_id, nodes, edges) tuples.
        """
        groups = JourneyConstructor.group_by_topic(entries)
        journeys: list[tuple[str, list[JourneyNode], list[JourneyEdge]]] = []
        for topic, topic_entries in groups.items():
            journey = JourneyConstructor.build_journey(
                topic, topic_entries, coach_id
            )
            journeys.append(journey)
        return journeys

    @staticmethod
    def validate_dag(edges: list[JourneyEdge]) -> bool:
        """Validate that edges form a valid DAG (no cycles).

        Uses topological sort via Kahn's algorithm.
        """
        from collections import defaultdict, deque

        in_degree: dict[str, int] = defaultdict(int)
        adj: dict[str, list[str]] = defaultdict(list)
        nodes: set[str] = set()

        for edge in edges:
            adj[edge.from_content_id].append(edge.to_content_id)
            in_degree[edge.to_content_id] += 1
            nodes.add(edge.from_content_id)
            nodes.add(edge.to_content_id)

        # Ensure all nodes are in in_degree
        for n in nodes:
            in_degree.setdefault(n, 0)

        queue = deque(n for n in nodes if in_degree[n] == 0)
        visited = 0

        while queue:
            node = queue.popleft()
            visited += 1
            for neighbor in adj[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return visited == len(nodes)


# ══════════════════════════════════════════════════════════════════════════════
# Unit 5 — Next-Content Recommendation Engine
# ══════════════════════════════════════════════════════════════════════════════


class RecommendationEngine:
    """Recommends next content in a learning journey.

    Traverses the DAG, finds completed nodes, returns the first
    uncompleted node whose prerequisites are all complete.
    Respects coping/atlas gating.
    """

    @staticmethod
    def get_completed_ids(
        progress: list[LearningProgressEntry],
        journey_id: str,
    ) -> set[str]:
        """Extract completed content IDs for a journey."""
        return {
            p.content_id for p in progress
            if p.journey_id == journey_id
        }

    @staticmethod
    def find_next(
        nodes: list[JourneyNode],
        edges: list[JourneyEdge],
        completed_ids: set[str],
        coping_position: int = 0,
        atlas_week: int = 0,
        entries_by_id: Optional[dict[str, LearningPathEntry]] = None,
    ) -> Optional[NextContentRecommendation]:
        """Find the next recommended content in the journey.

        Algorithm:
        1. Build adjacency and prerequisite maps.
        2. For each node in sequence order:
           a. Skip if already completed.
           b. Check all prerequisites are completed.
           c. Check gating conditions if unlock_condition present.
           d. If all checks pass, return this node as recommendation.
        """
        # Build prerequisite map: node → set of prerequisite nodes
        prereqs: dict[str, set[str]] = {}
        for edge in edges:
            prereqs.setdefault(edge.to_content_id, set()).add(
                edge.from_content_id
            )

        # Sort nodes by sequence position
        sorted_nodes = sorted(nodes, key=lambda n: n.sequence_position)

        for node in sorted_nodes:
            if node.content_id in completed_ids:
                continue

            # Check prerequisites
            node_prereqs = prereqs.get(node.content_id, set())
            if not node_prereqs.issubset(completed_ids):
                continue

            # Check gating if entry data available
            if entries_by_id and node.content_id in entries_by_id:
                entry = entries_by_id[node.content_id]
                if entry.unlock_condition:
                    uc = entry.unlock_condition
                    if (
                        coping_position < uc.min_coping_position
                        or atlas_week < uc.min_atlas_week
                    ):
                        continue

            return NextContentRecommendation(
                content_id=node.content_id,
                asset_id=node.asset_id,
                title=node.title,
                content_type=node.content_type,
                topic_cluster=node.topic_cluster,
                difficulty_level=node.difficulty_level,
                reason="next_in_sequence",
            )

        return None


# ══════════════════════════════════════════════════════════════════════════════
# Unit 6 — Main Service (LearningPathBuilder)
# ══════════════════════════════════════════════════════════════════════════════


class LearningPathBuilder:
    """Gabrielle — orchestrates the full learning path pipeline.

    - Receives content from CCP pipelines (CCF, V²WS, OBS, CBCS, CMF)
    - Classifies content using ContentClassifier
    - Stores in learning_path_registry (Supabase)
    - Constructs journey DAGs (Neo4j)
    - Recommends next content for clients
    - Writes receipts for all mutations
    """

    def __init__(
        self,
        coach_acronym: str,
        coach_id: str,
        supabase_client: Any = None,
        neo4j_client: Any = None,
        receipt_chain: Optional[ReceiptChain] = None,
    ):
        self.coach_acronym = coach_acronym.upper()
        self.coach_id = coach_id
        self._supabase = supabase_client
        self._neo4j = neo4j_client
        self._receipt_chain = receipt_chain or ReceiptChain(
            coach_acronym=self.coach_acronym
        )
        self._classifier = ContentClassifier()
        self._journey_constructor = JourneyConstructor()
        self._recommendation_engine = RecommendationEngine()

        # In-memory registry (mirrors Supabase for service lifetime)
        self._registry: list[LearningPathEntry] = []
        # In-memory journeys: journey_id → (nodes, edges)
        self._journeys: dict[str, tuple[list[JourneyNode], list[JourneyEdge]]] = {}
        # In-memory progress
        self._progress: list[LearningProgressEntry] = []

    def classify_content(
        self,
        asset_id: str,
        fingerprint_id: str,
        pipeline_source: str,
        psychological_routing_brief: dict[str, Any],
        audience_maturity: str,
        program_tag: Optional[str] = None,
        explicit_content_type: Optional[str] = None,
        unlock_condition: Optional[UnlockCondition] = None,
    ) -> LearningPathEntry:
        """Classify a content piece and add to the registry (AC1).

        Cross-tenant safety: coach_id is always self.coach_id.
        """
        entry = self._classifier.classify(
            asset_id=asset_id,
            fingerprint_id=fingerprint_id,
            coach_id=self.coach_id,
            pipeline_source=pipeline_source,
            psychological_routing_brief=psychological_routing_brief,
            audience_maturity=audience_maturity,
            program_tag=program_tag,
            explicit_content_type=explicit_content_type,
            unlock_condition=unlock_condition,
        )
        self._registry.append(entry)

        # Persist to Supabase
        self._persist_registry_entry(entry)

        # Write receipt
        self._write_receipt(
            action="classify_content",
            asset_id=entry.asset_id,
            payload=entry,
        )

        logger.info(
            "[%s] Classified content: %s → topic=%s difficulty=%s type=%s",
            AGENT_GABRIELLE,
            asset_id,
            entry.topic_cluster,
            entry.difficulty_level.value,
            entry.content_type.value,
        )
        return entry

    def construct_journeys(self) -> list[tuple[str, list[JourneyNode], list[JourneyEdge]]]:
        """Build all journey DAGs from current registry entries (AC2).

        Groups by topic cluster, orders by difficulty + created_at,
        creates prerequisite edges.
        """
        journeys = self._journey_constructor.build_all_journeys(
            self._registry, self.coach_id
        )

        for journey_id, nodes, edges in journeys:
            self._journeys[journey_id] = (nodes, edges)

            # Persist to Neo4j
            self._persist_journey(journey_id, nodes, edges)

            # Write receipt per journey
            self._write_receipt(
                action="construct_journey",
                asset_id=f"JOURNEY-{journey_id[:8]}",
                payload={
                    "journey_id": journey_id,
                    "node_count": len(nodes),
                    "edge_count": len(edges),
                },
            )

        logger.info(
            "[%s] Constructed %d journeys from %d registry entries",
            AGENT_GABRIELLE,
            len(journeys),
            len(self._registry),
        )
        return journeys

    def recommend_next(
        self,
        client_id: str,
        journey_id: str,
        coping_position: int = 0,
        atlas_week: int = 0,
    ) -> Optional[NextContentRecommendation]:
        """Recommend next content for a client in a journey (AC3, AC4).

        Respects:
        - Prerequisite edges (AC3)
        - Coping/atlas gating (AC4)
        """
        if journey_id not in self._journeys:
            return None

        nodes, edges = self._journeys[journey_id]
        completed_ids = self._recommendation_engine.get_completed_ids(
            self._progress, journey_id
        )

        # Build entries_by_id for gating check
        entries_by_id = {e.content_id: e for e in self._registry}

        return self._recommendation_engine.find_next(
            nodes=nodes,
            edges=edges,
            completed_ids=completed_ids,
            coping_position=coping_position,
            atlas_week=atlas_week,
            entries_by_id=entries_by_id,
        )

    def record_completion(
        self,
        client_id: str,
        content_id: str,
        journey_id: str,
    ) -> LearningProgressEntry:
        """Record client completion of a content piece."""
        progress = LearningProgressEntry(
            client_id=client_id,
            content_id=content_id,
            journey_id=journey_id,
        )
        self._progress.append(progress)
        return progress

    def validate_coach_isolation(
        self, entry: LearningPathEntry
    ) -> bool:
        """Validate that entry belongs to this coach (ADR-01 cross-tenant safety)."""
        return entry.coach_id == self.coach_id

    def get_registry(self) -> list[LearningPathEntry]:
        """Return all registry entries."""
        return list(self._registry)

    def get_journeys(
        self,
    ) -> dict[str, tuple[list[JourneyNode], list[JourneyEdge]]]:
        """Return all journey DAGs."""
        return dict(self._journeys)

    # ── Pipeline Integration Hooks (Unit 6 / Task 7) ─────────────────────

    def on_ccf_batch_complete(
        self,
        scripts: list[dict[str, Any]],
    ) -> list[LearningPathEntry]:
        """Hook: CCF batch completion → classify all scripts (AC5)."""
        entries = []
        for script in scripts:
            entry = self.classify_content(
                asset_id=script["asset_id"],
                fingerprint_id=script["fingerprint_id"],
                pipeline_source=PIPELINE_CCF,
                psychological_routing_brief=script.get(
                    "psychological_routing_brief", {}
                ),
                audience_maturity=script.get("audience_maturity", "new"),
                program_tag=script.get("program_tag"),
            )
            entries.append(entry)
        return entries

    def on_v2ws_complete(
        self, webinar: dict[str, Any]
    ) -> LearningPathEntry:
        """Hook: V²WS webinar completion → classify (AC5)."""
        return self.classify_content(
            asset_id=webinar["asset_id"],
            fingerprint_id=webinar["fingerprint_id"],
            pipeline_source=PIPELINE_V2WS,
            psychological_routing_brief=webinar.get(
                "psychological_routing_brief", {}
            ),
            audience_maturity=webinar.get("audience_maturity", "new"),
            program_tag=webinar.get("program_tag"),
        )

    def on_obs_recap(
        self, recap: dict[str, Any]
    ) -> LearningPathEntry:
        """Hook: OBS session recap (FR-CA11-05) → classify (AC5)."""
        return self.classify_content(
            asset_id=recap["asset_id"],
            fingerprint_id=recap["fingerprint_id"],
            pipeline_source=PIPELINE_OBS,
            psychological_routing_brief=recap.get(
                "psychological_routing_brief", {}
            ),
            audience_maturity=recap.get("audience_maturity", "new"),
            program_tag=recap.get("program_tag"),
        )

    def on_voice_lesson(
        self, lesson: dict[str, Any]
    ) -> LearningPathEntry:
        """Hook: CBCS voice note lesson (FR-CA11-06) → classify."""
        return self.classify_content(
            asset_id=lesson["asset_id"],
            fingerprint_id=lesson["fingerprint_id"],
            pipeline_source=PIPELINE_CBCS,
            psychological_routing_brief=lesson.get(
                "psychological_routing_brief", {}
            ),
            audience_maturity=lesson.get("audience_maturity", "new"),
            program_tag=lesson.get("program_tag"),
        )

    # ── Internal Persistence Stubs ────────────────────────────────────────

    def _persist_registry_entry(self, entry: LearningPathEntry) -> None:
        """Persist entry to Supabase learning_path_registry table."""
        if self._supabase is not None:
            self._supabase.insert_registry_entry(entry.model_dump(mode="json"))

    def _persist_journey(
        self,
        journey_id: str,
        nodes: list[JourneyNode],
        edges: list[JourneyEdge],
    ) -> None:
        """Persist journey DAG to Neo4j."""
        if self._neo4j is not None:
            self._neo4j.store_journey(
                journey_id=journey_id,
                nodes=[n.model_dump(mode="json") for n in nodes],
                edges=[e.model_dump(mode="json") for e in edges],
            )

    def _write_receipt(
        self, action: str, asset_id: str, payload: Any
    ) -> str:
        """Write receipt to Receipt Chain Guard (DEP-ENG-041)."""
        if hasattr(payload, "model_dump"):
            data = payload.model_dump(mode="json")
        else:
            data = payload if isinstance(payload, dict) else str(payload)

        payload_hash = hashlib.sha256(
            json.dumps(data, sort_keys=True, default=str).encode()
        ).hexdigest()

        entry = self._receipt_chain.log(
            agent_id=AGENT_GABRIELLE,
            action=action,
            asset_id=asset_id,
            input_summary=f"Learning path payload hash: {payload_hash}",
            output_summary=f"Content classified/journey constructed",
            decision="classified",
            metadata={"schema_ref": "DEP-ENG-041"},
        )
        return entry.receipt_id
