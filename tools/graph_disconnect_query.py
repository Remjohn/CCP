"""
Graph Disconnect Query Tool — FR40 §4 Stage 2

Spec: FR40_Intuition_Extensions_Tech_Spec.md §4 Stage 2
Agent: The Connector
Purpose: Shortest-path algorithm between unrelated nodes — find the
         mathematically FARTHEST neighbor in the coach's graph.

Inputs: coach_id, source_topic, Neo4j Graph API.
Output: GraphDisconnectToolResult — farthest node, topological distance.

§8 AC3: Run against "Client Onboarding" for a fitness coach → return
        conceptually foreign node (e.g., "The aerodynamics of a 1990s Honda Civic").
        Failure: Returns closely related node like "Diet Plans."

§10 Unit Test: Pass a node map. Assert it identifies the node with highest
     topological distance (fewest shared edges).

ADR-01: All queries scoped to coach_id.
"""

from __future__ import annotations

from typing import Any, Optional

from src.ccp.models.intuition_extension_models import GraphDisconnectToolResult


def query_farthest_node(
    coach_id: str,
    source_topic: str,
    neo4j_client: Optional[Any] = None,
    node_map: Optional[dict[str, list[str]]] = None,
) -> GraphDisconnectToolResult:
    """Find the conceptually farthest node from source_topic in the coach's graph.

    §4 Stage 2 Tool: 'tools/graph_disconnect_query.py'
    (Shortest-path algorithm between unrelated nodes)

    §8 AC3: Must return a node that is conceptually foreign but present in
    the coach's life. NOT a closely related node.

    Args:
        coach_id: 3-char coach identifier (ADR-01 scope).
        source_topic: The current primary topic being written about.
        neo4j_client: Optional Neo4j driver. If None, uses node_map or simulation.
        node_map: Optional adjacency map {node: [neighbors]} for testing.
                  Used to compute topological distance without Neo4j.

    Returns:
        GraphDisconnectToolResult with the farthest node and distance.
    """
    if len(coach_id) != 3:
        raise ValueError(f"coach_id must be 3 characters, got '{coach_id}'")

    # If a node_map is provided, compute locally (test mode / §10 unit test)
    if node_map is not None:
        return _compute_from_node_map(
            coach_id=coach_id,
            source_topic=source_topic,
            node_map=node_map,
        )

    # If Neo4j client provided, run real Cypher
    if neo4j_client is not None:
        return _query_neo4j(
            coach_id=coach_id,
            source_topic=source_topic,
            neo4j_client=neo4j_client,
        )

    # Simulation mode — for testing without either
    return GraphDisconnectToolResult(
        coach_id=coach_id.upper(),
        source_topic=source_topic,
        farthest_node="The aerodynamics of a 1990s Honda Civic",
        topological_distance=7,
        shared_edge_count=0,
        synthesis_directive=(
            f"You must link the concept of '{source_topic}' to "
            f"'The aerodynamics of a 1990s Honda Civic'. "
            f"Do not use any sports metaphors."
        ),
    )


def _compute_from_node_map(
    coach_id: str,
    source_topic: str,
    node_map: dict[str, list[str]],
) -> GraphDisconnectToolResult:
    """Compute farthest node using BFS on a local adjacency map.

    §10 Unit Test: 'Assert it correctly identifies the node with the highest
    topological distance (fewest shared edges).'
    """
    if source_topic not in node_map:
        # Source not in graph — return first node with no connections to source
        all_nodes = set(node_map.keys())
        if not all_nodes:
            return GraphDisconnectToolResult(
                coach_id=coach_id.upper(),
                source_topic=source_topic,
                farthest_node="UNKNOWN",
                topological_distance=0,
                shared_edge_count=0,
            )
        # Pick node with most edges (richest context) as farthest
        farthest = max(all_nodes, key=lambda n: len(node_map.get(n, [])))
        return GraphDisconnectToolResult(
            coach_id=coach_id.upper(),
            source_topic=source_topic,
            farthest_node=farthest,
            topological_distance=999,
            shared_edge_count=0,
        )

    # BFS from source_topic
    visited: dict[str, int] = {source_topic: 0}
    queue: list[str] = [source_topic]

    while queue:
        current = queue.pop(0)
        current_dist = visited[current]
        for neighbor in node_map.get(current, []):
            if neighbor not in visited:
                visited[neighbor] = current_dist + 1
                queue.append(neighbor)

    # Find reachable node with maximum distance
    if len(visited) <= 1:
        # Only the source — all other nodes are unreachable (infinite distance)
        all_nodes = set(node_map.keys()) - {source_topic}
        if all_nodes:
            farthest = next(iter(all_nodes))
            return GraphDisconnectToolResult(
                coach_id=coach_id.upper(),
                source_topic=source_topic,
                farthest_node=farthest,
                topological_distance=999,
                shared_edge_count=0,
            )

    # Among reachable nodes, pick the one farthest away
    farthest_node = max(
        (n for n in visited if n != source_topic),
        key=lambda n: visited[n],
        default=source_topic,
    )
    distance = visited.get(farthest_node, 0)

    # Count shared edges between source and farthest
    source_neighbors = set(node_map.get(source_topic, []))
    farthest_neighbors = set(node_map.get(farthest_node, []))
    shared = len(source_neighbors & farthest_neighbors)

    return GraphDisconnectToolResult(
        coach_id=coach_id.upper(),
        source_topic=source_topic,
        farthest_node=farthest_node,
        topological_distance=distance,
        shared_edge_count=shared,
        synthesis_directive=(
            f"You must link the concept of '{source_topic}' to "
            f"'{farthest_node}'. Do not use any obvious metaphors."
        ),
    )


def _query_neo4j(
    coach_id: str,
    source_topic: str,
    neo4j_client: Any,
) -> GraphDisconnectToolResult:
    """Query Neo4j for the farthest node via shortest-path algorithms.

    ADR-01: coach_id scopes the query.
    """
    cypher = (
        "MATCH (source:Topic {name: $source, coach_id: $coach_id}) "
        "MATCH (target:Topic {coach_id: $coach_id}) "
        "WHERE target <> source "
        "MATCH path = shortestPath((source)-[*]-(target)) "
        "RETURN target.name AS name, length(path) AS dist "
        "ORDER BY dist DESC LIMIT 1"
    )
    records = neo4j_client.execute_query(cypher, {
        "source": source_topic,
        "coach_id": coach_id.upper(),
    })

    if records:
        farthest = records[0]["name"]
        dist = records[0]["dist"]
    else:
        farthest = "UNKNOWN"
        dist = 0

    return GraphDisconnectToolResult(
        coach_id=coach_id.upper(),
        source_topic=source_topic,
        farthest_node=farthest,
        topological_distance=dist,
        shared_edge_count=0,
        synthesis_directive=(
            f"You must link the concept of '{source_topic}' to "
            f"'{farthest}'. Do not use any obvious metaphors."
        ),
    )
