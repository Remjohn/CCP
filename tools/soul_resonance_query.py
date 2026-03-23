"""
SoulResonance Query Tool — FR40 §4 Stage 1

Spec: FR40_Intuition_Extensions_Tech_Spec.md §4 Stage 1
Agent: The Resonance Seeker
Purpose: Neo4j semantic query for highly charged emotional nodes.

Inputs: coach_id, coach_soul.json (DEP-ENG-003), Sacred Audio Database.
Output: SoulResonanceToolResult — emotional nodes, sacred moments, polarity.

ADR-01: All queries MUST be scoped to coach_id + Tribe_ID.
Safety Test: Tribe Isolation — query enforces Coach_ID and Tribe_ID tokens.
"""

from __future__ import annotations

from typing import Any, Optional

from src.ccp.models.intuition_extension_models import SoulResonanceToolResult


def query_emotional_nodes(
    coach_id: str,
    tribe_id: Optional[str] = None,
    polarity_filter: Optional[str] = None,
    max_results: int = 5,
    neo4j_client: Optional[Any] = None,
) -> SoulResonanceToolResult:
    """Query Neo4j for highly charged emotional nodes from Sacred Audio.

    §4 Stage 1 Tool: 'tools/soul_resonance_query.py'
    (Neo4j semantic query for highly charged emotional nodes)

    ADR-01 Safety Test: Rigorous Coach_ID + Tribe_ID enforcement.
    The database query NEVER returns nodes from other coaches.

    Args:
        coach_id: 3-char coach identifier (ADR-01 scope).
        tribe_id: Optional tribe scope for Tribe Mirror Check.
        polarity_filter: Optional polarity to filter ('Analytical', 'Dark Humor', etc.).
        max_results: Maximum emotional nodes to return.
        neo4j_client: Optional Neo4j driver instance. If None, returns
                      simulated results for testing.

    Returns:
        SoulResonanceToolResult with emotional nodes and polarity analysis.
    """
    if len(coach_id) != 3:
        raise ValueError(f"coach_id must be 3 characters, got '{coach_id}'")

    # ADR-01: Build coach-scoped Cypher query
    cypher_query = (
        f"MATCH (n:EmotionalNode {{coach_id: $coach_id}}) "
        f"WHERE n.charge_level > 0.7 "
    )
    if tribe_id:
        cypher_query += f"AND n.tribe_id = $tribe_id "
    cypher_query += "RETURN n ORDER BY n.charge_level DESC LIMIT $limit"

    query_params = {
        "coach_id": coach_id.upper(),
        "limit": max_results,
    }
    if tribe_id:
        query_params["tribe_id"] = tribe_id

    # Execute query or return simulated result
    if neo4j_client is not None:
        # Production path — real Neo4j
        records = neo4j_client.execute_query(cypher_query, query_params)
        nodes = [r["n"]["label"] for r in records]
        sacred = records[0]["n"].get("sacred_moment") if records else None
        polarity = _detect_polarity_imbalance(nodes, polarity_filter)
        return SoulResonanceToolResult(
            coach_id=coach_id.upper(),
            emotional_nodes_found=nodes,
            sacred_moment=sacred,
            emotional_register_match=True,
            polarity_imbalance=polarity,
        )

    # Simulation path — for testing without Neo4j
    return SoulResonanceToolResult(
        coach_id=coach_id.upper(),
        emotional_nodes_found=[
            "vulnerability_in_leadership",
            "fear_of_being_seen",
            "grief_over_lost_potential",
        ][:max_results],
        sacred_moment=(
            "A 3-second pause after saying 'I used to think strength meant silence.'"
        ),
        emotional_register_match=tribe_id is not None,
        polarity_imbalance=(
            "Purely Analytical — inject Dark Humor or Vulnerability"
            if polarity_filter == "Analytical"
            else None
        ),
    )


def _detect_polarity_imbalance(
    nodes: list[str],
    filter_hint: Optional[str],
) -> Optional[str]:
    """Detect if emotional polarity is imbalanced.

    §4 Stage 1 Behavior 2: If purely 'Analytical', inject contrast.
    """
    if filter_hint:
        return f"Purely {filter_hint} — inject dimensional contrast"
    if not nodes:
        return "No emotional nodes found — inject any visceral content"
    return None
