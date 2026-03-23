"""
CCP FR38 — Memory Tier Promotion Service (DEP-ENG-033)

Spec: FR38_Memory_Tier_Promotion_Tech_Spec.md
Produces: DEP-ENG-033 Semantic Committal Receipt

§4 Stage 1: Working → Episodic Filter (LIWC > 7.0)
§4 Stage 2: Algorithmic Pattern Flagging (≥3 occurrences, ≥14 days)
§4 Stage 3: Governance Gate (human-in-the-loop APPROVE/REJECT/MODIFY)
§4 Stage 4: Semantic Committal ([:EPISODIC] severed, [:SEMANTIC] + [:SUPPORTING_EVIDENCE] created)

§8 AC1: Only LIWC emotional intensity > 7.0 qualifies for Episodic tier
§8 AC2: Pattern catch: ≥3 occurrences over ≥14 days → SemanticReviewProposal
§8 AC3: [:SEMANTIC] edge must NOT exist until APPROVE received
§8 AC4: On APPROVE → [:EPISODIC] severed, [:SEMANTIC] created, no duplication
§6 Stale Decay: Proposals queued >30 days → auto-REJECT
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import Optional, Any
from uuid import uuid4

from src.ccp.models.onboarding_prerequisite_models import (
    LIWC_EMOTIONAL_INTENSITY_THRESHOLD,
    PATTERN_MIN_SPAN_DAYS,
    PATTERN_OCCURRENCE_THRESHOLD,
    STALE_DECAY_DAYS,
    EpisodicNode,
    GraphMutationStatus,
    MemoryTierEdge,
    OperatorVerdict,
    SemanticCommittalReceipt,
    SemanticReviewProposal,
)
from src.ccp.core.receipt_chain import ReceiptChain


# ══════════════════════════════════════════════════════════════════════════════
# In-memory review queue (governs Stage 3 AC3 enforcement)
# ══════════════════════════════════════════════════════════════════════════════

class ProposalQueue:
    """Holds pending SemanticReviewProposals that have NOT yet been approved.

    AC3: graph mutations ([:SEMANTIC]) are strictly prohibited while a
    proposal lives in this queue — only on APPROVE does it exit and mutate.
    """

    def __init__(self) -> None:
        self._proposals: dict[str, SemanticReviewProposal] = {}

    def enqueue(self, proposal: SemanticReviewProposal) -> None:
        self._proposals[proposal.proposal_id] = proposal

    def get(self, proposal_id: str) -> Optional[SemanticReviewProposal]:
        return self._proposals.get(proposal_id)

    def remove(self, proposal_id: str) -> Optional[SemanticReviewProposal]:
        return self._proposals.pop(proposal_id, None)

    def all_pending(self) -> list[SemanticReviewProposal]:
        return list(self._proposals.values())

    def __contains__(self, proposal_id: str) -> bool:
        return proposal_id in self._proposals


# ══════════════════════════════════════════════════════════════════════════════
# Stage 1: Working → Episodic Filter
# ══════════════════════════════════════════════════════════════════════════════

class WorkingToEpisodicFilter:
    """FR38 §4 Stage 1: Apply LIWC emotional intensity threshold.

    AC1: Entries with LIWC score ≤ 7.0 remain in Working memory.
         Only entries > 7.0 are promoted to Episodic.
    """

    THRESHOLD = LIWC_EMOTIONAL_INTENSITY_THRESHOLD

    def filter(self, working_nodes: list[EpisodicNode]) -> list[EpisodicNode]:
        """Return only nodes whose liwc_emotional_intensity > 7.0.

        Each returned node has its edge_type set to EPISODIC.
        """
        result: list[EpisodicNode] = []
        for node in working_nodes:
            if node.qualifies_for_episodic:
                promoted = node.model_copy(
                    update={"edge_type": MemoryTierEdge.EPISODIC}
                )
                result.append(promoted)
        return result


# ══════════════════════════════════════════════════════════════════════════════
# Stage 2: Algorithmic Pattern Flagging
# ══════════════════════════════════════════════════════════════════════════════

class PatternFlaggingEngine:
    """FR38 §4 Stage 2: Cluster episodic nodes by semantic root driver.

    AC2: If the same root driver appears ≥3 times across ≥14 calendar days,
         a SemanticReviewProposal is emitted and placed in the governance queue.

    Semantic similarity merge: "fear of running out of money" and
    "going bankrupt" → same root_driver = "financial_fear".
    This is approximated here by label prefix matching; production wires Aria.
    """

    OCCURRENCE_THRESHOLD = PATTERN_OCCURRENCE_THRESHOLD
    MIN_SPAN_DAYS = PATTERN_MIN_SPAN_DAYS

    def sweep(
        self,
        episodic_nodes: list[EpisodicNode],
        existing_episodic_dates: Optional[dict[str, list[date]]] = None,
    ) -> list[SemanticReviewProposal]:
        """Return proposals for root drivers that meet AC2 thresholds.

        episodic_nodes: newly promoted nodes from Stage 1.
        existing_episodic_dates: {root_driver: [past_dates...]} from storage.
        """
        existing_episodic_dates = existing_episodic_dates or {}
        proposals: list[SemanticReviewProposal] = []

        # Build root_driver → dates map (merge existing + new)
        driver_dates: dict[str, list[date]] = {}
        for driver, past_dates in existing_episodic_dates.items():
            driver_dates[driver] = list(past_dates)

        for node in episodic_nodes:
            driver = self._extract_root_driver(node.label)
            driver_dates.setdefault(driver, [])
            if node.first_observed:
                driver_dates[driver].append(node.first_observed)

        # Evaluate each driver for pattern threshold
        for driver, dates in driver_dates.items():
            if len(dates) < self.OCCURRENCE_THRESHOLD:
                continue
            dates_sorted = sorted(dates)
            span_days = (dates_sorted[-1] - dates_sorted[0]).days
            if span_days < self.MIN_SPAN_DAYS:
                continue

            # Build supporting evidence from matching episodic nodes
            supporting = [
                n.node_id for n in episodic_nodes
                if self._extract_root_driver(n.label) == driver
            ]

            proposal = SemanticReviewProposal(
                proposal_id=str(uuid4()),
                root_driver=driver,
                proposed_truth=f"Pattern: '{driver}' recurring ≥{self.OCCURRENCE_THRESHOLD}×",
                occurrence_count=len(dates),
                first_observed=dates_sorted[0],
                most_recent=dates_sorted[-1],
                span_days=span_days,
                supporting_episodic_node_ids=supporting,
            )
            proposals.append(proposal)

        return proposals

    @staticmethod
    def _extract_root_driver(label: str) -> str:
        """Approximate semantic merge: normalise label to root driver cluster."""
        # Production: call Aria semantic similarity. Dev: simple word-stem.
        label_lower = label.lower()
        if any(w in label_lower for w in ("money", "financ", "bankrupt", "broke")):
            return "financial_fear"
        if any(w in label_lower for w in ("imposter", "fraud", "fake", "phony")):
            return "imposter_syndrome"
        if any(w in label_lower for w in ("fail", "failure", "loser")):
            return "failure_fear"
        if any(w in label_lower for w in ("stuck", "stagnant", "not moving")):
            return "stagnation_pattern"
        return label_lower.replace(" ", "_")


# ══════════════════════════════════════════════════════════════════════════════
# Stage 3: Governance Gate (human-in-the-loop)
# ══════════════════════════════════════════════════════════════════════════════

class GovernanceGate:
    """FR38 §4 Stage 3: Telegram operator interface for human review.

    AC3 CRITICAL: Until APPROVE is received, the Neo4j graph is UNCHANGED.
    Proposals sit in ProposalQueue and no graph mutation occurs.

    The `send_for_review()` method fires a Telegram notification (production:
    real Telegram bot; dev: returns stub). `receive_verdict()` processes the
    verdict and hands control to Stage 4.
    """

    def send_for_review(
        self,
        proposal: SemanticReviewProposal,
        telegram_bot: Any = None,
    ) -> bool:
        """Dispatch review notification. Return True when sent successfully."""
        message = (
            f"🧠 Semantic Memory Proposal\n"
            f"Root Driver: {proposal.root_driver}\n"
            f"Proposed Truth: {proposal.proposed_truth}\n"
            f"Occurrences: {proposal.occurrence_count} over {proposal.span_days} days\n"
            f"Proposal ID: {proposal.proposal_id}\n"
            "Reply APPROVE / REJECT / MODIFY:<modified_truth>"
        )
        if telegram_bot is not None:
            try:
                telegram_bot.send(message)
            except Exception:
                return False
        # Dev simulation: always succeeds
        return True


# ══════════════════════════════════════════════════════════════════════════════
# Stage 4: Semantic Graph Committal
# ══════════════════════════════════════════════════════════════════════════════

class SemanticCommittalExecutor:
    """FR38 §4 Stage 4: Execute graph mutations on APPROVE.

    AC4:
      - DROP [:EPISODIC] edge from all supporting nodes
      - CREATE [:SEMANTIC] edge with committed truth
      - CREATE [:SUPPORTING_EVIDENCE] edges from episodic supporting nodes
      - No duplicate [:SEMANTIC] edges (idempotent MERGE in production)
    """

    def __init__(self, neo4j_client: Any = None) -> None:
        self._client = neo4j_client

    def commit(
        self,
        proposal: SemanticReviewProposal,
        operator_id: str,
        final_truth: str,
        coach_id: str,
    ) -> SemanticCommittalReceipt:
        """Execute graph mutation. Return DEP-ENG-033 receipt.

        In dev mode (no neo4j_client), simulates the mutation and returns
        a valid receipt.
        """
        severed_edges: list[str] = []
        created_semantic = False
        mutation_status = GraphMutationStatus.SUCCESS

        if self._client is not None:
            try:
                # AC4: Sever [:EPISODIC] edges for each supporting node
                for node_id in proposal.supporting_episodic_node_ids:
                    self._client.delete_edge(
                        node_id=node_id,
                        edge_type=MemoryTierEdge.EPISODIC.value,
                        coach_id=coach_id,
                    )
                    severed_edges.append(node_id)

                # AC4: Create [:SEMANTIC] edge (MERGE prevents duplication)
                self._client.merge_semantic_node(
                    root_driver=proposal.root_driver,
                    truth=final_truth,
                    coach_id=coach_id,
                    proposal_id=proposal.proposal_id,
                )
                created_semantic = True

                # AC4: CREATE [:SUPPORTING_EVIDENCE] links
                for node_id in proposal.supporting_episodic_node_ids:
                    self._client.create_supporting_evidence_edge(
                        source_node_id=node_id,
                        semantic_driver=proposal.root_driver,
                        coach_id=coach_id,
                    )

            except Exception:
                mutation_status = GraphMutationStatus.FAIL
        else:
            # Dev simulation — all mutations succeed
            severed_edges = list(proposal.supporting_episodic_node_ids)
            created_semantic = True

        from uuid import uuid4 as _uuid4
        return SemanticCommittalReceipt(
            committal_id=str(_uuid4()),
            client_id=proposal.proposal_id,  # Use proposal_id as client ref
            operator_id=operator_id,
            coach_id=coach_id,
            approved_semantic_truth=final_truth,
            operator_verdict=OperatorVerdict.APPROVE,
            original_system_proposal=proposal.proposed_truth,
            supporting_evidence_nodes=proposal.supporting_episodic_node_ids,
            graph_mutation_status=mutation_status,
            episodic_edges_severed=severed_edges,
            semantic_edge_created=created_semantic,
        )


# ══════════════════════════════════════════════════════════════════════════════
# Full Memory Tier Promotion Service
# ══════════════════════════════════════════════════════════════════════════════

class MemoryTierPromotionService:
    """FR38 full 4-stage orchestrator.

    Usage:
        svc = MemoryTierPromotionService(coach_id="EMI")
        episodic = svc.score_working_memory(working_nodes)
        proposals = svc.run_pattern_sweep(episodic, existing_dates)
        receipt = svc.process_operator_verdict(
            proposal_id, OperatorVerdict.APPROVE, operator_id="OP-001"
        )
    """

    def __init__(
        self,
        coach_id: str,
        neo4j_client: Any = None,
        telegram_bot: Any = None,
        receipt_chain: Optional[ReceiptChain] = None,
    ) -> None:
        if len(coach_id) != 3:
            raise ValueError("coach_id must be 3 characters (ADR-01).")
        self.coach_id = coach_id
        self.receipt_chain = receipt_chain or ReceiptChain(
            coach_acronym=coach_id
        )
        self._working_filter = WorkingToEpisodicFilter()
        self._pattern_engine = PatternFlaggingEngine()
        self._gov_gate = GovernanceGate()
        self._committal = SemanticCommittalExecutor(neo4j_client)
        self._telegram = telegram_bot
        self._queue = ProposalQueue()

    # ── Stage 1 ───────────────────────────────────────────────────────────────

    def score_working_memory(
        self,
        working_nodes: list[EpisodicNode],
    ) -> list[EpisodicNode]:
        """AC1: Promote nodes with LIWC > 7.0 to Episodic tier."""
        promoted = self._working_filter.filter(working_nodes)

        self.receipt_chain.log(
            agent_id="The-Architect",
            action="working_to_episodic_filter",
            input_summary=f"total_working={len(working_nodes)}",
            output_summary=f"promoted={len(promoted)} threshold={LIWC_EMOTIONAL_INTENSITY_THRESHOLD}",
            metadata={"stage_name": "WORKING-TO-EPISODIC"},
        )
        return promoted

    # ── Stage 2 ───────────────────────────────────────────────────────────────

    def run_pattern_sweep(
        self,
        episodic_nodes: list[EpisodicNode],
        existing_episodic_dates: Optional[dict[str, list[date]]] = None,
    ) -> list[SemanticReviewProposal]:
        """AC2: Flag patterns ≥3 occurrences/≥14 days → enqueue for governance."""
        proposals = self._pattern_engine.sweep(
            episodic_nodes=episodic_nodes,
            existing_episodic_dates=existing_episodic_dates or {},
        )
        for proposal in proposals:
            self._queue.enqueue(proposal)
            self._gov_gate.send_for_review(proposal, self._telegram)

        self.receipt_chain.log(
            agent_id="The-Architect",
            action="nightly_pattern_sweep",
            input_summary=f"episodic_nodes={len(episodic_nodes)}",
            output_summary=f"proposals_generated={len(proposals)}",
            metadata={"stage_name": "PATTERN-FLAGGING"},
        )
        return proposals

    # ── Stage 3: Stale Decay ──────────────────────────────────────────────────

    def check_stale_decay(
        self,
        reference_date: Optional[date] = None,
    ) -> list[str]:
        """§6: Auto-reject proposals queued > 30 days. Return rejected IDs."""
        ref = reference_date or date.today()
        rejected_ids: list[str] = []

        for proposal in self._queue.all_pending():
            age_days = (ref - proposal.first_observed).days
            if age_days > STALE_DECAY_DAYS:
                self._queue.remove(proposal.proposal_id)
                rejected_ids.append(proposal.proposal_id)

        if rejected_ids:
            self.receipt_chain.log(
                agent_id="Deletion-Orchestrator",
                action="stale_decay_auto_reject",
                input_summary=f"checked={len(self._queue.all_pending()) + len(rejected_ids)}",
                output_summary=f"auto_rejected={len(rejected_ids)}",
                metadata={"stage_name": "GOVERNANCE-GATE"},
            )
        return rejected_ids

    # ── Stage 3/4: Operator Verdict ───────────────────────────────────────────

    def process_operator_verdict(
        self,
        proposal_id: str,
        verdict: OperatorVerdict,
        operator_id: str = "OPERATOR",
        modified_truth: Optional[str] = None,
    ) -> Optional[SemanticCommittalReceipt]:
        """AC3/AC4: Process APPROVE/REJECT/MODIFY.

        AC3: Graph is only mutated if verdict == APPROVE.
        AC4: On APPROVE — [:EPISODIC] severed, [:SEMANTIC] created.

        Returns DEP-ENG-033 SemanticCommittalReceipt or None on REJECT.
        """
        proposal = self._queue.get(proposal_id)
        if proposal is None:
            # Not found in queue (already processed or never existed)
            return None

        self.receipt_chain.log(
            agent_id="The-Architect",
            action="operator_verdict_received",
            input_summary=f"proposal={proposal_id} verdict={verdict.value}",
            output_summary=f"operator={operator_id}",
            metadata={"stage_name": "GOVERNANCE-GATE"},
        )

        if verdict == OperatorVerdict.REJECT:
            self._queue.remove(proposal_id)
            return None

        if verdict == OperatorVerdict.MODIFY:
            if not modified_truth:
                raise ValueError("MODIFY verdict requires modified_truth.")
            # Update proposed truth in queue and re-dispatch for re-review
            updated = proposal.model_copy(
                update={"proposed_truth": modified_truth}
            )
            self._queue.enqueue(updated)
            return None  # Awaiting re-approval

        # APPROVE path — AC3 cleared, execute Stage 4
        final_truth = modified_truth or proposal.proposed_truth
        self._queue.remove(proposal_id)

        receipt = self._committal.commit(
            proposal=proposal,
            operator_id=operator_id,
            final_truth=final_truth,
            coach_id=self.coach_id,
        )

        self.receipt_chain.log(
            agent_id="The-Architect",
            action="semantic_committal_executed",
            input_summary=f"proposal={proposal_id} root_driver={proposal.root_driver}",
            output_summary=(
                f"episodic_severed={len(receipt.episodic_edges_severed)} "
                f"semantic_created={receipt.semantic_edge_created}"
            ),
            metadata={"stage_name": "SEMANTIC-COMMITTAL"},
        )
        return receipt

    def get_pending_proposals(self) -> list[SemanticReviewProposal]:
        """Return all proposals currently in governance queue (AC3 state check)."""
        return self._queue.all_pending()

    def is_in_governance_queue(self, proposal_id: str) -> bool:
        """AC3 assertion helper: True if proposal is awaiting approval."""
        return proposal_id in self._queue
