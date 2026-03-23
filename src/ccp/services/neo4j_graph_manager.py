"""
CCP FR6 — Neo4j Graph Manager (Phase B7) (Unit 8)
Neo4j graph ontology persistence for the Context Premise Map.

Spec reference: FR6 Tech Spec §Phase B7
  14 node types: Frustration, Want, Dream, Fear, Suspicion, Insecurity,
    EnvyFeeling, Enemy, CopingMechanism, HiddenBelief, EmotionalTrigger,
    SuccessMarker, Segment, HermeneuticalGap
  8 relationship types: TRIGGERS, CONTRADICTS, FUELS, MASKS, VIOLATES,
    BELONGS_TO, AT_DEPTH, RESONATES_WITH

Isolation constraint: Each coach's graph operates in a dedicated Neo4j
database or labeled graph partition. Zero cross-coach queries. (ADR-01)

Performance requirement: Graph read <500ms per query. (AC10)

Architecture: Uses dependency injection for Neo4j driver. The models and
service contracts are implemented here; the actual Neo4j driver is injected.
"""

import time
from typing import Any, Optional, Protocol

from src.ccp.models.tribe_profile_models import (
    AudienceSegment,
    CopingMechanismDimension,
    CopingMechanismEntry,
    ContextPremiseDimension,
    DepthLevel,
    DepthStratifiedEntry,
    EmotionalMode,
    EmotionalTriggerDimension,
    EmotionalTriggerEntry,
    GraphNode,
    GraphRelationship,
    HermeneuticalGapMarker,
    Neo4jNodeType,
    Neo4jRelationshipType,
    TribeProfileDistilled,
)


class Neo4jDriverProtocol(Protocol):
    """Protocol for Neo4j driver injection.
    Production: neo4j Python driver.
    Testing: in-memory mock."""

    def run_query(
        self,
        query: str,
        parameters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Execute a Cypher query and return results."""
        ...

    def close(self) -> None:
        """Close the driver connection."""
        ...


class InMemoryNeo4jDriver:
    """In-memory Neo4j driver mock for testing and development.
    Stores nodes and relationships in Python dictionaries.
    Per-coach isolation enforced by coach_id filtering."""

    def __init__(self) -> None:
        self.nodes: list[dict[str, Any]] = []
        self.relationships: list[dict[str, Any]] = []
        self._closed = False

    def run_query(
        self,
        query: str,
        parameters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Simulate Cypher query execution."""
        params = parameters or {}

        # Simple query simulation for common patterns
        if "CREATE" in query.upper():
            if "node_type" in params:
                self.nodes.append(params)
            elif "relationship_type" in params:
                self.relationships.append(params)
            return [{"created": True}]

        if "MATCH" in query.upper():
            coach_id = params.get("coach_id", "")
            node_type = params.get("node_type", "")
            results = [
                n for n in self.nodes
                if n.get("coach_id") == coach_id
                and (not node_type or n.get("node_type") == node_type)
            ]
            return results

        if "DELETE" in query.upper():
            coach_id = params.get("coach_id", "")
            self.nodes = [
                n for n in self.nodes if n.get("coach_id") != coach_id
            ]
            self.relationships = [
                r for r in self.relationships if r.get("coach_id") != coach_id
            ]
            return [{"deleted": True}]

        return []

    def close(self) -> None:
        self._closed = True


class Neo4jGraphManager:
    """FR6 Phase B7: Neo4j Graph Ontology Persistence.

    Manages the Context Premise graph for a single coach.
    Per-coach isolation enforced at every query level (ADR-01).

    AC9: Cross-coach queries MUST return empty. Critical security violation.
    AC10: Graph read <500ms per query.
    """

    # Dimension name → Neo4j node type mapping
    DIMENSION_NODE_MAP: dict[str, Neo4jNodeType] = {
        "frustrations": Neo4jNodeType.FRUSTRATION,
        "wants": Neo4jNodeType.WANT,
        "dreams": Neo4jNodeType.DREAM,
        "fears": Neo4jNodeType.FEAR,
        "suspicions": Neo4jNodeType.SUSPICION,
        "insecurities": Neo4jNodeType.INSECURITY,
        "envy_feelings": Neo4jNodeType.ENVY_FEELING,
        "enemies": Neo4jNodeType.ENEMY,
        "coping_mechanism": Neo4jNodeType.COPING_MECHANISM,
        "hidden_beliefs": Neo4jNodeType.HIDDEN_BELIEF,
        "emotional_triggers": Neo4jNodeType.EMOTIONAL_TRIGGER,
        "success_markers": Neo4jNodeType.SUCCESS_MARKER,
    }

    def __init__(
        self,
        coach_id: str,
        coach_acronym: str,
        driver: Optional[Neo4jDriverProtocol] = None,
    ):
        self.coach_id = coach_id
        self.coach_acronym = coach_acronym.upper()
        self.driver: Neo4jDriverProtocol = driver or InMemoryNeo4jDriver()

    # ──────────────────────────────────────────────────────────
    # Node Creation
    # ──────────────────────────────────────────────────────────

    def _create_node(self, node: GraphNode) -> str:
        """Create a single node in the graph. Returns node_id."""
        node.coach_id = self.coach_id
        if not node.node_id:
            import hashlib
            content = f"{self.coach_id}:{node.node_type.value}:{node.text[:50]}"
            node.node_id = hashlib.sha256(content.encode()).hexdigest()[:16]

        self.driver.run_query(
            "CREATE (n:{label} $props)",
            parameters={
                "node_type": node.node_type.value,
                "coach_id": self.coach_id,
                "node_id": node.node_id,
                "text": node.text,
                "depth_level": node.depth_level.value if node.depth_level else None,
                "mode": node.mode.value if node.mode else None,
                "intensity": node.intensity.value if node.intensity else None,
                "source_evidence": node.source_evidence,
                "provenance_score": node.provenance_score,
            },
        )
        return node.node_id

    def _create_relationship(self, rel: GraphRelationship) -> None:
        """Create a relationship between two nodes."""
        self.driver.run_query(
            "MATCH (a), (b) WHERE a.node_id = $source AND b.node_id = $target "
            "CREATE (a)-[r:{rel_type} $props]->(b)",
            parameters={
                "relationship_type": rel.relationship_type.value,
                "coach_id": self.coach_id,
                "source": rel.source_node_id,
                "target": rel.target_node_id,
                **rel.properties,
            },
        )

    # ──────────────────────────────────────────────────────────
    # Dimension Population
    # ──────────────────────────────────────────────────────────

    def populate_dimension(
        self,
        dimension_name: str,
        entries: list[DepthStratifiedEntry],
    ) -> list[str]:
        """Populate a single dimension's nodes in the graph.
        Returns list of created node_ids."""
        node_type = self.DIMENSION_NODE_MAP.get(dimension_name)
        if not node_type:
            return []

        node_ids: list[str] = []
        for entry in entries:
            node = GraphNode(
                node_type=node_type,
                coach_id=self.coach_id,
                text=entry.text,
                depth_level=entry.depth,
                mode=entry.mode,
                intensity=entry.intensity,
                source_evidence=entry.source,
                provenance_score=entry.provenance_score,
            )

            # Extended fields for specific types
            if isinstance(entry, EmotionalTriggerEntry):
                node.activation_keywords = entry.activation_keywords
                node.moral_foundation = entry.moral_foundation
            elif isinstance(entry, CopingMechanismEntry):
                node.trajectory_position = entry.trajectory_position

            node_id = self._create_node(node)
            node_ids.append(node_id)

        return node_ids

    def populate_segments(
        self,
        segments: list[AudienceSegment],
    ) -> list[str]:
        """Populate audience segment nodes."""
        node_ids: list[str] = []
        for seg in segments:
            node = GraphNode(
                node_type=Neo4jNodeType.SEGMENT,
                coach_id=self.coach_id,
                segment_id=seg.segment_id,
                dhd_label=seg.dhd_label,
                regulatory_focus=seg.regulatory_focus,
                coping_stage=seg.coping_stage,
                reconsolidation_readiness=seg.reconsolidation_readiness,
            )
            node_id = self._create_node(node)
            node_ids.append(node_id)
        return node_ids

    def populate_hermeneutical_gaps(
        self,
        gaps: list[HermeneuticalGapMarker],
    ) -> list[str]:
        """Populate hermeneutical gap marker nodes."""
        node_ids: list[str] = []
        for gap in gaps:
            node = GraphNode(
                node_type=Neo4jNodeType.HERMENEUTICAL_GAP,
                coach_id=self.coach_id,
                text=gap.text,
                detection_method=gap.detection_method,
                confidence_score=gap.confidence,
            )
            node_id = self._create_node(node)
            node_ids.append(node_id)
        return node_ids

    # ──────────────────────────────────────────────────────────
    # Relationship Inference
    # ──────────────────────────────────────────────────────────

    def infer_relationships(
        self,
        profile: TribeProfileDistilled,
        node_registry: dict[str, list[str]],
    ) -> list[GraphRelationship]:
        """Infer and create relationships between nodes.

        Relationship types per spec §Phase B7:
        - TRIGGERS: Fear → CopingMechanism
        - CONTRADICTS: HiddenBelief → Want
        - FUELS: Enemy → EmotionalTrigger
        - MASKS: SuccessMarker → Insecurity
        - VIOLATES: EmotionalTrigger → MoralFoundation
        - BELONGS_TO: * → Segment
        - AT_DEPTH: * → DepthLevel
        """
        relationships: list[GraphRelationship] = []

        # TRIGGERS: Fear → CopingMechanism
        fear_ids = node_registry.get("fears", [])
        coping_ids = node_registry.get("coping_mechanism", [])
        for f_id in fear_ids:
            for c_id in coping_ids:
                rel = GraphRelationship(
                    relationship_type=Neo4jRelationshipType.TRIGGERS,
                    source_node_id=f_id,
                    target_node_id=c_id,
                )
                self._create_relationship(rel)
                relationships.append(rel)

        # CONTRADICTS: HiddenBelief → Want
        belief_ids = node_registry.get("hidden_beliefs", [])
        want_ids = node_registry.get("wants", [])
        for b_id in belief_ids:
            for w_id in want_ids:
                rel = GraphRelationship(
                    relationship_type=Neo4jRelationshipType.CONTRADICTS,
                    source_node_id=b_id,
                    target_node_id=w_id,
                )
                self._create_relationship(rel)
                relationships.append(rel)

        # FUELS: Enemy → EmotionalTrigger
        enemy_ids = node_registry.get("enemies", [])
        trigger_ids = node_registry.get("emotional_triggers", [])
        for e_id in enemy_ids:
            for t_id in trigger_ids:
                rel = GraphRelationship(
                    relationship_type=Neo4jRelationshipType.FUELS,
                    source_node_id=e_id,
                    target_node_id=t_id,
                )
                self._create_relationship(rel)
                relationships.append(rel)

        # MASKS: SuccessMarker → Insecurity
        success_ids = node_registry.get("success_markers", [])
        insecurity_ids = node_registry.get("insecurities", [])
        for s_id in success_ids:
            for i_id in insecurity_ids:
                rel = GraphRelationship(
                    relationship_type=Neo4jRelationshipType.MASKS,
                    source_node_id=s_id,
                    target_node_id=i_id,
                )
                self._create_relationship(rel)
                relationships.append(rel)

        return relationships

    # ──────────────────────────────────────────────────────────
    # Full Graph Population
    # ──────────────────────────────────────────────────────────

    def populate_full_graph(
        self,
        profile: TribeProfileDistilled,
    ) -> dict[str, Any]:
        """Populate the complete Neo4j graph from a distilled profile.

        Returns summary of nodes and relationships created.
        """
        start_time = time.time()
        node_registry: dict[str, list[str]] = {}

        # Populate all 12 base dimensions
        for dim_name in [
            "frustrations", "wants", "dreams", "fears", "suspicions",
            "insecurities", "envy_feelings", "enemies",
            "hidden_beliefs", "success_markers",
        ]:
            dim: ContextPremiseDimension = getattr(profile, dim_name)
            ids = self.populate_dimension(dim_name, dim.entries)
            node_registry[dim_name] = ids

        # Coping mechanism (extended)
        coping_ids = self.populate_dimension(
            "coping_mechanism", profile.coping_mechanism.entries,
        )
        node_registry["coping_mechanism"] = coping_ids

        # Emotional triggers (extended)
        trigger_ids = self.populate_dimension(
            "emotional_triggers", profile.emotional_triggers.entries,
        )
        node_registry["emotional_triggers"] = trigger_ids

        # Segments
        segment_ids = self.populate_segments(profile.segments)
        node_registry["segments"] = segment_ids

        # Hermeneutical gaps
        gap_ids = self.populate_hermeneutical_gaps(
            profile.psychometric_extensions.hermeneutical_gap_markers,
        )
        node_registry["hermeneutical_gaps"] = gap_ids

        # Infer relationships
        relationships = self.infer_relationships(profile, node_registry)

        elapsed_ms = (time.time() - start_time) * 1000

        total_nodes = sum(len(ids) for ids in node_registry.values())
        return {
            "total_nodes": total_nodes,
            "total_relationships": len(relationships),
            "node_registry": {k: len(v) for k, v in node_registry.items()},
            "elapsed_ms": elapsed_ms,
        }

    # ──────────────────────────────────────────────────────────
    # Isolation & Safety (AC9)
    # ──────────────────────────────────────────────────────────

    def query_nodes(
        self,
        node_type: Optional[Neo4jNodeType] = None,
    ) -> list[dict[str, Any]]:
        """Query nodes for THIS coach only. AC9: per-coach isolation.
        Cross-coach queries MUST return empty — critical security violation."""
        return self.driver.run_query(
            "MATCH (n) WHERE n.coach_id = $coach_id RETURN n",
            parameters={
                "coach_id": self.coach_id,
                "node_type": node_type.value if node_type else "",
            },
        )

    def purge_coach_data(self) -> dict[str, Any]:
        """Delete ALL graph data for this coach.
        Called when coach exits platform (ADR-01 secure purge)."""
        result = self.driver.run_query(
            "MATCH (n) WHERE n.coach_id = $coach_id DETACH DELETE n",
            parameters={"coach_id": self.coach_id},
        )
        return {"purged": True, "coach_id": self.coach_id}

    def close(self) -> None:
        """Close the Neo4j driver connection."""
        self.driver.close()
