"""
CCP FR13 — Client Context Premise Map Pipeline (DEP-ENG-030)

Spec: FR13_Client_Context_Premise_Map_Tech_Spec.md
Produces: DEP-ENG-028 (extraction), DEP-ENG-029 (Cypher manifest), DEP-ENG-030 (graph)

§4 Stage 1: 12-Dimensional Extraction (Aria)
§4 Stage 2: Cypher Graph Mapping (Atlas)
§4 Stage 3: Neo4j Hypergraph Commit (ADR-01 guarded)
§4 Stage 4: Right-to-be-Forgotten Purge

ADR-01: Each coach has a strictly isolated single-tenant Neo4j instance.
        Using a global/blank NEO4J_URI is a security fault (AC2).

§6 Fallback: Neo4j offline → Supabase JSONB flat storage + graph_sync_pending=True.
"""

from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from typing import Any, Optional, Protocol

from src.ccp.models.onboarding_prerequisite_models import (
    ClientContextExtraction,
    ContextDimension,
    ContextEdgeProposal,
    ContextRelationship,
    CypherQuery,
    CypherTransactionManifest,
    DepthLevel,
    ExtractedContextNode,
    GraphCommitResult,
    GraphCommitVerdict,
    PurgeReceipt,
)
from src.ccp.core.receipt_chain import ReceiptChain


# ══════════════════════════════════════════════════════════════════════════════
# Protocols (dependency injection — testable without live DB)
# ══════════════════════════════════════════════════════════════════════════════

class Neo4jClientProtocol(Protocol):
    """Abstract Neo4j bolt client used by Stage 3."""

    def run_transaction(self, queries: list[str], coach_id: str) -> dict[str, Any]:
        """Execute ordered Cypher queries in a single transaction.
        Returns: {'status': 'SUCCESS'|'PROVISIONAL'|'FAIL', 'nodes': int, 'edges': int}
        """
        ...

    def run_purge(self, coach_id: str) -> dict[str, Any]:
        """Drop all nodes and the database container for this coach.
        Returns: {'remaining_count': int, 'voice_dna_purged': bool, ...}
        """
        ...


class SupabaseClientProtocol(Protocol):
    """Abstract Supabase client used by fallback path."""

    def upsert_jsonb(self, table: str, coach_id: str, payload: dict[str, Any]) -> bool:
        """Write a JSONB record to the given table."""
        ...


class TenantCredentialVaultProtocol(Protocol):
    """ADR-01: Coach-specific credential resolver.

    AC2: If this returns None (blank/global URI), the pipeline must
    raise IsolationFaultError — never silently connect to a shared DB.
    """

    def get_neo4j_uri(self, coach_id: str) -> Optional[str]:
        """Return the coach's isolated NEO4J_URI or None if not provisioned."""
        ...

    def get_neo4j_password(self, coach_id: str) -> Optional[str]:
        """Return the coach's isolated NEO4J_PASSWORD or None."""
        ...


# ══════════════════════════════════════════════════════════════════════════════
# Exceptions
# ══════════════════════════════════════════════════════════════════════════════

class IsolationFaultError(RuntimeError):
    """AC2: Raised when pipeline attempts to use a global/blank NEO4J_URI.

    Spec: 'If the pipeline attempts to initialize a Neo4j connection using a
    global or blank database URI string... the pipeline intentionally crashes
    with a severe isolation security fault.'
    """
    def __init__(self, coach_id: str) -> None:
        super().__init__(
            f"ISOLATION SECURITY FAULT: No coach-specific NEO4J_URI found for "
            f"coach '{coach_id}'. Refusing to connect to a shared or default database. "
            f"ADR-01 violation prevented."
        )


class ExtractionInsufficientError(ValueError):
    """FR13 §4 Stage 1 Failure: < 2 valid entities extracted."""
    def __init__(self, count: int) -> None:
        super().__init__(
            f"Extraction yielded {count} entities — minimum 2 required. "
            "Stage 1 FAIL: insufficient context premise data."
        )


class OrphanNodeError(ValueError):
    """FR13 AC3: Raised when a proposed Cypher manifest contains orphaned nodes."""
    def __init__(self, orphaned_ids: list[str]) -> None:
        super().__init__(
            f"CYPHER TOPOLOGY FAIL: Orphaned nodes detected — {orphaned_ids}. "
            "Every node must have at least one relationship edge. Manifest rejected."
        )


# ══════════════════════════════════════════════════════════════════════════════
# Stage 1: 12-Dimensional Extraction (Aria)
# ══════════════════════════════════════════════════════════════════════════════

class AriaExtractionAdapter:
    """Wraps Aria's output into DEP-ENG-028 (ClientContextExtraction).

    In production, Aria runs via PydanticAI and returns a structured ContextExtraction.
    This adapter translates that into the FR13 canonical schema.
    """

    def extract(
        self,
        session_reference: str,
        client_hash: str,
        coach_id: str,
        raw_transcript: str,
        aria_result: Optional[dict[str, Any]] = None,
    ) -> ClientContextExtraction:
        """Stage 1: Parse raw transcript into DEP-ENG-028.

        Args:
            raw_transcript: Session text. Must not be empty.
            aria_result: Optional pre-computed Aria output (for testing).
        """
        nodes: list[ExtractedContextNode] = []
        edges: list[ContextEdgeProposal] = []

        if aria_result:
            nodes, edges = self._translate_aria_result(
                client_hash, aria_result
            )
        else:
            # Simulation: minimal entity extraction for dev/test
            nodes, edges = self._simulate_extraction(client_hash, raw_transcript)

        return ClientContextExtraction(
            session_reference=session_reference,
            client_hash=client_hash,
            coach_id=coach_id,
            extracted_nodes=nodes,
            proposed_edges=edges,
        )

    def _translate_aria_result(
        self,
        client_hash: str,
        aria_result: dict[str, Any],
    ) -> tuple[list[ExtractedContextNode], list[ContextEdgeProposal]]:
        """Translate Aria's ContextExtraction model into FR13 node/edge lists."""
        nodes: list[ExtractedContextNode] = []
        edges: list[ContextEdgeProposal] = []
        entities = aria_result.get("entities", [])
        for i, entity in enumerate(entities):
            dimension_raw = entity.get("dimension", "Fear")
            # Map Aria's dimension names to FR13 ContextDimension enum
            dimension = self._map_dimension(dimension_raw)
            node_id = f"{dimension_raw.lower()}_{i}"
            node = ExtractedContextNode(
                node_id=node_id,
                dimension=dimension,
                raw_language=entity.get("name", entity.get("evidence_quote", "")),
                depth_level=DepthLevel(entity.get("depth", "L1")),
            )
            nodes.append(node)
            # Build edge from client to entity
            rel = self._map_relationship(dimension_raw)
            edges.append(ContextEdgeProposal(
                source_node=client_hash,
                target_node=node_id,
                relationship=rel,
                properties={"context": dimension_raw},
            ))
        return nodes, edges

    def _simulate_extraction(
        self,
        client_hash: str,
        transcript: str,
    ) -> tuple[list[ExtractedContextNode], list[ContextEdgeProposal]]:
        """Simulation mode: extract mock entities for dev/test."""
        text_lower = transcript.lower()
        nodes: list[ExtractedContextNode] = []
        edges: list[ContextEdgeProposal] = []

        # Simple heuristic: detect emotion-heavy language
        if any(word in text_lower for word in ["fear", "afraid", "terrified", "scared"]):
            node = ExtractedContextNode(
                node_id="fear_0",
                dimension=ContextDimension.FEAR,
                raw_language=transcript[:80],  # exact substring — never summarized
                depth_level=DepthLevel.L3,
            )
            nodes.append(node)
            edges.append(ContextEdgeProposal(
                source_node=client_hash,
                target_node="fear_0",
                relationship=ContextRelationship.FEARS,
                properties={"context": "Fear"},
            ))
        if any(word in text_lower for word in ["boss", "manager", "enemy", "hate"]):
            node = ExtractedContextNode(
                node_id="enemy_0",
                dimension=ContextDimension.ENEMY,
                raw_language=transcript[:80],
                depth_level=DepthLevel.L2,
            )
            nodes.append(node)
            edges.append(ContextEdgeProposal(
                source_node=client_hash,
                target_node="enemy_0",
                relationship=ContextRelationship.FIGHTS_AGAINST,
                properties={"context": "Enemy"},
            ))
        return nodes, edges

    @staticmethod
    def _map_dimension(raw: str) -> ContextDimension:
        mapping = {
            "Enemy": ContextDimension.ENEMY,
            "Dream": ContextDimension.DREAM,
            "Fear": ContextDimension.FEAR,
            "Identity": ContextDimension.IDENTITY,
            "Trigger": ContextDimension.EMOTIONAL_TRIGGER,
            "Resistance": ContextDimension.RESISTANCE_PATTERN,
            "Ritual": ContextDimension.RITUAL_AFFINITY,
            "Coach": ContextDimension.COACH_REFERENCE,
        }
        return mapping.get(raw, ContextDimension.FEAR)

    @staticmethod
    def _map_relationship(dimension: str) -> ContextRelationship:
        mapping = {
            "Enemy": ContextRelationship.FIGHTS_AGAINST,
            "Fear": ContextRelationship.FEARS,
            "Dream": ContextRelationship.CRAVES,
            "Identity": ContextRelationship.HAS_IDENTITY,
            "Trigger": ContextRelationship.RESONATES_WITH,
        }
        return mapping.get(dimension, ContextRelationship.FEARS)


# ══════════════════════════════════════════════════════════════════════════════
# Stage 2: Cypher Graph Mapping (Atlas)
# ══════════════════════════════════════════════════════════════════════════════

class AtlasCypherMapper:
    """Translates DEP-ENG-028 into DEP-ENG-029 (CypherTransactionManifest).

    Spec: 'Uses MERGE and MATCH Cypher to prevent duplicate nodes.
    Assert valid topology (no syntax errors, no orphaned nodes).' (FR13 §4 Stage 2)
    """

    def build_manifest(
        self, extraction: ClientContextExtraction
    ) -> CypherTransactionManifest:
        """Stage 2: Build CypherTransactionManifest from ClientContextExtraction.

        Raises:
            OrphanNodeError: If any node has no edge binding it to the client (AC3).
        """
        if extraction.has_orphaned_nodes:
            orphaned = [
                n.node_id
                for n in extraction.extracted_nodes
                if not self._has_edge(n.node_id, extraction.proposed_edges)
            ]
            raise OrphanNodeError(orphaned)

        queries: list[CypherQuery] = []
        seq = 0

        # 1. MERGE the client node
        queries.append(CypherQuery(
            sequence=seq,
            cypher=f"MERGE (u:Client {{hash: '{extraction.client_hash}'}})",
            node_ids_referenced=[extraction.client_hash],
        ))
        seq += 1

        # 2. MERGE each entity node
        for node in extraction.extracted_nodes:
            safe_raw = re.sub(r"'", "\\'", node.raw_language)
            queries.append(CypherQuery(
                sequence=seq,
                cypher=(
                    f"MERGE (n:{node.dimension.value} {{id: '{node.node_id}'}}) "
                    f"ON CREATE SET n.raw_language = '{safe_raw}', "
                    f"n.depth = '{node.depth_level.value}'"
                ),
                node_ids_referenced=[node.node_id],
            ))
            seq += 1

        # 3. MERGE each relationship edge
        for edge in extraction.proposed_edges:
            props = ", ".join(f"{k}: '{v}'" for k, v in edge.properties.items())
            props_str = f" {{{props}}}" if props else ""
            queries.append(CypherQuery(
                sequence=seq,
                cypher=(
                    f"MERGE (src {{id: '{edge.source_node}'}})-"
                    f"[:{edge.relationship.value}{props_str}]->"
                    f"(tgt {{id: '{edge.target_node}'}})"
                ),
                node_ids_referenced=[edge.source_node, edge.target_node],
            ))
            seq += 1

        return CypherTransactionManifest(
            manifest_id=f"CYP-{uuid.uuid4().hex[:8].upper()}",
            coach_id=extraction.coach_id,
            source_session_reference=extraction.session_reference,
            query_chain=queries,
            orphan_check_passed=True,
            topology_valid=True,
        )

    @staticmethod
    def _has_edge(node_id: str, edges: list[ContextEdgeProposal]) -> bool:
        return any(
            e.source_node == node_id or e.target_node == node_id for e in edges
        )


# ══════════════════════════════════════════════════════════════════════════════
# Stage 3: Neo4j Hypergraph Commit (ADR-01 guarded)
# ══════════════════════════════════════════════════════════════════════════════

class GraphCommitOrchestrator:
    """ADR-01-guarded Neo4j commit with Supabase fallback.

    Spec: FR13 §4 Stage 3.
    AC2: If vault returns None for NEO4J_URI → IsolationFaultError immediately.
    §6 Fallback: On FAIL after retries → Supabase JSONB + graph_sync_pending=True.
    """

    MAX_RETRIES = 3

    def __init__(
        self,
        credential_vault: TenantCredentialVaultProtocol,
        neo4j_client: Optional[Neo4jClientProtocol] = None,
        supabase_client: Optional[SupabaseClientProtocol] = None,
    ) -> None:
        self.vault = credential_vault
        self.neo4j = neo4j_client
        self.supabase = supabase_client

    def commit(
        self,
        manifest: CypherTransactionManifest,
        receipt_chain: Optional[ReceiptChain] = None,
    ) -> GraphCommitResult:
        """Stage 3: Execute the Cypher manifest against the coach's isolated DB.

        AC2: IsolationFaultError on blank/global URI.
        §6: On FAIL → Supabase fallback.
        """
        coach_id = manifest.coach_id

        # ADR-01 credential check
        neo4j_uri = self.vault.get_neo4j_uri(coach_id)
        if not neo4j_uri or neo4j_uri.strip() == "":
            raise IsolationFaultError(coach_id)

        result = GraphCommitResult(
            coach_id=coach_id,
            manifest_id=manifest.manifest_id,
            verdict=GraphCommitVerdict.FAIL,
        )

        if self.neo4j is None:
            # No client injected — simulation mode
            result.verdict = GraphCommitVerdict.PASS
            result.nodes_written = len(manifest.query_chain)
            result.committed_at = datetime.now(timezone.utc)
            return result

        cypher_strings = [q.cypher for q in manifest.query_chain]
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                outcome = self.neo4j.run_transaction(cypher_strings, coach_id)
                status = outcome.get("status", "FAIL")
                if status == "SUCCESS":
                    result.verdict = GraphCommitVerdict.PASS
                    result.nodes_written = outcome.get("nodes", 0)
                    result.edges_written = outcome.get("edges", 0)
                    result.committed_at = datetime.now(timezone.utc)
                    break
                elif status == "PROVISIONAL":
                    result.verdict = GraphCommitVerdict.PROVISIONAL
                    result.retry_count = attempt
                    # Exponential backoff (simulated — caller handles actual wait)
                    continue
                else:
                    result.verdict = GraphCommitVerdict.FAIL
                    result.error_detail = outcome.get("error")
                    break
            except Exception as exc:
                result.error_detail = str(exc)
                if attempt == self.MAX_RETRIES:
                    break

        if result.verdict == GraphCommitVerdict.FAIL:
            result = self._activate_fallback(manifest, result)

        if receipt_chain:
            receipt_chain.log(
                agent_id="Graph-Commit-Orchestrator",
                action="neo4j_hypergraph_commit",
                input_summary=f"Manifest {manifest.manifest_id} — {len(cypher_strings)} queries",
                output_summary=f"Verdict: {result.verdict.value} | nodes: {result.nodes_written}",
                metadata={"stage_name": "STAGE-3-GRAPH-COMMIT"},
            )
        return result

    def _activate_fallback(
        self,
        manifest: CypherTransactionManifest,
        result: GraphCommitResult,
    ) -> GraphCommitResult:
        """§6 Fallback: Write DEP-ENG-028 to Supabase JSONB + flag for async sync."""
        if self.supabase:
            payload = manifest.model_dump(mode="json")
            success = self.supabase.upsert_jsonb(
                "context_premise_fallback",
                manifest.coach_id,
                payload,
            )
            result.graph_sync_pending = True
            result.supabase_fallback_used = success
        return result


# ══════════════════════════════════════════════════════════════════════════════
# Stage 4: Right-to-be-Forgotten Purge
# ══════════════════════════════════════════════════════════════════════════════

class DeletionOrchestrator:
    """Implements the RTBF cryptographic sequence purge.

    Spec: FR13 §4 Stage 4 / AC5
    Input: /purge_tenant {coach_id} system command.
    Output: PurgeReceipt with remaining_node_count = 0 (AC5).
    """

    def __init__(
        self,
        neo4j_client: Optional[Neo4jClientProtocol] = None,
    ) -> None:
        self.neo4j = neo4j_client

    def purge(
        self,
        coach_id: str,
        purge_command: str,
        receipt_chain: Optional[ReceiptChain] = None,
    ) -> PurgeReceipt:
        """Stage 4: Terminate all connections, detach-delete all nodes, drop DB."""
        if self.neo4j:
            outcome = self.neo4j.run_purge(coach_id)
            remaining = outcome.get("remaining_count", 0)
            voice_dna_purged = outcome.get("voice_dna_purged", False)
            connections_terminated = outcome.get("connections_terminated", False)
            database_dropped = outcome.get("database_dropped", False)
        else:
            # Simulation mode
            remaining = 0
            voice_dna_purged = True
            connections_terminated = True
            database_dropped = True

        receipt = PurgeReceipt(
            coach_id=coach_id,
            purge_command=purge_command,
            remaining_node_count=remaining,
            voice_dna_purged=voice_dna_purged,
            connections_terminated=connections_terminated,
            database_dropped=database_dropped,
        )

        if receipt_chain:
            receipt_chain.log(
                agent_id="Deletion-Orchestrator",
                action="rtbf_purge",
                input_summary=f"Purge command: {purge_command}",
                output_summary=f"Remaining nodes: {remaining} | Complete: {receipt.complete_eradication_verified}",
                metadata={"stage_name": "STAGE-4-PURGE"},
            )
        return receipt


# ══════════════════════════════════════════════════════════════════════════════
# Full 4-Stage Pipeline
# ══════════════════════════════════════════════════════════════════════════════

class ClientContextPremisePipeline:
    """FR13 full pipeline orchestrator.

    Stages:
        1. Aria extraction → DEP-ENG-028
        2. Atlas Cypher mapping → DEP-ENG-029
        3. Neo4j commit → DEP-ENG-030
        (4. Purge — triggered separately via purge())
    """

    def __init__(
        self,
        coach_id: str,
        credential_vault: TenantCredentialVaultProtocol,
        neo4j_client: Optional[Neo4jClientProtocol] = None,
        supabase_client: Optional[SupabaseClientProtocol] = None,
        receipt_chain: Optional[ReceiptChain] = None,
    ) -> None:
        if len(coach_id) != 3:
            raise ValueError("coach_id must be 3 characters (ADR-01).")
        self.coach_id = coach_id
        self.receipt_chain = receipt_chain or ReceiptChain(coach_acronym=coach_id)
        self.extractor = AriaExtractionAdapter()
        self.mapper = AtlasCypherMapper()
        self.committer = GraphCommitOrchestrator(
            credential_vault=credential_vault,
            neo4j_client=neo4j_client,
            supabase_client=supabase_client,
        )
        self.deleter = DeletionOrchestrator(neo4j_client=neo4j_client)

    def run(
        self,
        session_reference: str,
        client_hash: str,
        raw_transcript: str,
        aria_result: Optional[dict[str, Any]] = None,
    ) -> tuple[ClientContextExtraction, CypherTransactionManifest, GraphCommitResult]:
        """Execute Stages 1–3.

        Returns:
            (DEP-ENG-028, DEP-ENG-029, DEP-ENG-030)

        Raises:
            ExtractionInsufficientError: < 2 entities extracted.
            OrphanNodeError: Orphaned node in Cypher manifest.
            IsolationFaultError: Blank/global NEO4J_URI (ADR-01 violation).
        """
        # Stage 1
        extraction = self.extractor.extract(
            session_reference=session_reference,
            client_hash=client_hash,
            coach_id=self.coach_id,
            raw_transcript=raw_transcript,
            aria_result=aria_result,
        )
        if len(extraction.extracted_nodes) < 2:
            raise ExtractionInsufficientError(len(extraction.extracted_nodes))

        self.receipt_chain.log(
            agent_id="Aria",
            action="context_premise_extraction",
            input_summary=f"session={session_reference} transcript_len={len(raw_transcript)}",
            output_summary=f"nodes={len(extraction.extracted_nodes)} edges={len(extraction.proposed_edges)}",
            metadata={"stage_name": "STAGE-1-EXTRACTION"},
        )

        # Stage 2
        manifest = self.mapper.build_manifest(extraction)

        self.receipt_chain.log(
            agent_id="Atlas",
            action="cypher_mapping",
            input_summary=f"nodes={len(extraction.extracted_nodes)}",
            output_summary=f"manifest={manifest.manifest_id} queries={len(manifest.query_chain)}",
            metadata={"stage_name": "STAGE-2-CYPHER-MAPPING"},
        )

        # Stage 3
        commit_result = self.committer.commit(
            manifest, receipt_chain=self.receipt_chain
        )

        return extraction, manifest, commit_result

    def purge(self, purge_command: str) -> PurgeReceipt:
        """Execute Stage 4 — Right-to-be-Forgotten."""
        return self.deleter.purge(
            coach_id=self.coach_id,
            purge_command=purge_command,
            receipt_chain=self.receipt_chain,
        )
