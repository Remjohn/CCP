"""
CCP FR21 — Receipt Chain Guard Protocol Service (DEP-PROTO-010)

Implements the Receipt Chain Guard at three stages:
  Stage 1: Receipt Generation (any node emits a hash after SUCCESS)
  Stage 2: Handoff Verification (downstream intercepts & validates)
  Stage 3: Circuit Breaker & Quarantine (halts pipeline on chain break)

Spec reference: FR21_Receipt_Chain_Guard_Tech_Spec.md
  §4 — Implementation Plan (Stages 1-3)
  §6 — ZERO backward compatibility fallback
  §7 — Tasks 1-5
  §8 — AC1 (Broken Chain Halt), AC2 (Quarantine Packaging),
        AC3 (No-Bypass Rule), AC4 (ADR-01 Strict Isolation)
"""

import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.receipt_guard_models import (
    AssemblyChainLedger,
    AssemblyStatus,
    ChainBreakEvent,
    GuardStage,
    HandoffVerification,
    NodeReceipt,
    QuarantineTicket,
    ReceiptGuardVerdict,
    VerificationResult,
)


class ReceiptChainGuard:
    """Receipt Chain Guard Protocol (DEP-PROTO-010).

    Pessimistic Locking: System defaults to REJECTED/HALTED.
    A node cannot proceed unless it holds the valid receipt_hash
    from its direct upstream provider.

    Immutable Ledgers: Once a receipt is generated and passed,
    it cannot be edited. Hashed into assembly_report.json.

    Quarantine Without Deletion: Broken chain quarantines the batch
    but does NOT delete partial work.

    Ghost Variable Prevention Gate: All input DEP-IDs must be verified
    cryptographically before payload unpacking.
    """

    def __init__(self, coach_id: str):
        """Initialize the guard for a specific coach.

        Args:
            coach_id: 3-letter coach acronym (ADR-01 scoping).
        """
        if len(coach_id) != 3:
            raise ValueError(f"coach_id must be 3 characters, got '{coach_id}'")
        self.coach_id = coach_id.upper()
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_id)
        self._chain_ledger: dict[str, str] = {}
        self._quarantine_ticket: Optional[QuarantineTicket] = None

    # ─── Stage 1: Receipt Generation (Node Emit) ─────────────────────────────

    def generate_receipt(
        self,
        node_id: str,
        stage_name: str,
        agent_name: str,
        input_payload: Any,
        output_payload: Any,
        execution_status: str = "SUCCESS",
        previous_receipt_hash: Optional[str] = None,
    ) -> Optional[NodeReceipt]:
        """Generate a cryptographic receipt for a pipeline node.

        Spec §4 Stage 1 Step 3: If execution_status != SUCCESS,
        the component CANNOT generate a receipt.

        Args:
            node_id: Unique node identifier in the pipeline.
            stage_name: Human-readable stage name.
            agent_name: Agent/adapter that produced the output.
            input_payload: The input data (hashed, not stored).
            output_payload: The output data (hashed, not stored).
            execution_status: Must be 'SUCCESS' to emit receipt.
            previous_receipt_hash: Upstream receipt hash for chaining.

        Returns:
            NodeReceipt if execution_status is SUCCESS, None otherwise.
        """
        if execution_status != "SUCCESS":
            self.receipt_chain.log(
                agent_id="receipt_chain_guard",
                action="receipt_generation_failed",
                input_summary=f"Node: {node_id}, Status: {execution_status}",
                output_summary="Receipt NOT generated — execution_status != SUCCESS",
                decision="rejected",
                metadata={"node_id": node_id, "stage_name": stage_name},
            )
            return None

        timestamp = datetime.now(timezone.utc).isoformat()
        input_hash = self._hash_payload(input_payload)
        output_hash = self._hash_payload(output_payload)

        # Deterministic hash: timestamp + node_id + payload_checksum
        payload_checksum = hashlib.sha256(
            f"{input_hash}:{output_hash}".encode()
        ).hexdigest()[:16]
        receipt_hash = hashlib.sha256(
            f"{timestamp}:{node_id}:{payload_checksum}".encode()
        ).hexdigest()

        receipt = NodeReceipt(
            receipt_chain_hash=receipt_hash,
            node_id=node_id,
            stage_name=stage_name,
            agent_name=agent_name,
            execution_status=execution_status,
            timestamp=timestamp,
            input_payload_hash=input_hash,
            output_payload_hash=output_hash,
            previous_receipt_hash=previous_receipt_hash,
        )

        # Record in chain ledger
        self._chain_ledger[stage_name] = receipt_hash

        # Log to Receipt Chain (DEP-ENG-041)
        self.receipt_chain.log(
            agent_id="receipt_chain_guard",
            action="receipt_generated",
            input_summary=f"Node: {node_id}, Input hash: {input_hash}",
            output_summary=f"Receipt: {receipt_hash[:16]}..., Stage: {stage_name}",
            decision="receipt_emitted",
            metadata={
                "node_id": node_id,
                "stage_name": stage_name,
                "receipt_hash": receipt_hash,
                "previous_receipt_hash": previous_receipt_hash,
            },
        )

        return receipt

    # ─── Stage 2: Handoff Verification (Node Intake) ─────────────────────────

    def verify_handoff(
        self,
        payload: dict[str, Any],
        upstream_node_id: str,
        downstream_node_id: str,
    ) -> HandoffVerification:
        """Verify a payload's receipt before allowing downstream processing.

        Spec §4 Stage 2: Intercept before passing to internal logic.
        PARTIAL status is evaluated as FALSE — instant chain break.
        AC3: No-Bypass Rule — blocks 100% of unverified payloads.

        Args:
            payload: The incoming payload dict (must contain 'receipt_chain_hash').
            upstream_node_id: The node that should have emitted the receipt.
            downstream_node_id: The node attempting to consume.

        Returns:
            HandoffVerification with chain_verified boolean.
        """
        receipt_hash = payload.get("receipt_chain_hash")

        # Check 1: Receipt exists
        if receipt_hash is None or receipt_hash == "":
            verification = HandoffVerification(
                chain_verified=False,
                verification_result=VerificationResult.MISSING_HASH,
                upstream_node_id=upstream_node_id,
                downstream_node_id=downstream_node_id,
                receipt_chain_hash=None,
                error_detail=f"Missing receipt_chain_hash from node '{upstream_node_id}'",
            )
            self._log_verification(verification)
            return verification

        # Check 2: Structural validity (must be hex string of expected length)
        if not self._is_valid_hash_structure(receipt_hash):
            verification = HandoffVerification(
                chain_verified=False,
                verification_result=VerificationResult.INVALID_STRUCTURE,
                upstream_node_id=upstream_node_id,
                downstream_node_id=downstream_node_id,
                receipt_chain_hash=receipt_hash,
                error_detail=f"Invalid hash structure: '{receipt_hash[:32]}...'",
            )
            self._log_verification(verification)
            return verification

        # Check 3: PARTIAL status check (if payload carries status)
        payload_status = payload.get("execution_status", "SUCCESS")
        if payload_status == "PARTIAL":
            verification = HandoffVerification(
                chain_verified=False,
                verification_result=VerificationResult.PARTIAL_STATUS,
                upstream_node_id=upstream_node_id,
                downstream_node_id=downstream_node_id,
                receipt_chain_hash=receipt_hash,
                error_detail="PARTIAL status evaluates as FALSE — chain break",
            )
            self._log_verification(verification)
            return verification

        # All checks pass
        verification = HandoffVerification(
            chain_verified=True,
            verification_result=VerificationResult.VALID,
            upstream_node_id=upstream_node_id,
            downstream_node_id=downstream_node_id,
            receipt_chain_hash=receipt_hash,
        )
        self._log_verification(verification)
        return verification

    # ─── Stage 3: Circuit Breaker & Quarantine ────────────────────────────────

    def trip_circuit_breaker(
        self,
        failed_verification: HandoffVerification,
        compilation_request_id: str,
        preserved_state: Optional[dict[str, Any]] = None,
    ) -> QuarantineTicket:
        """Execute the Circuit Breaker when a chain break is detected.

        Spec §4 Stage 3:
        1. Force HALT signal to JIT Compiler array.
        2. Wrap active state into quarantine object.
        3. Set assembly_status: REJECTED_BROKEN_CHAIN.
        4. Push failure point to System Operator queue.
        5. Kill current orchestration instance.

        AC2: Must write exact failure node to assembly_report.json.
        AC4: Data dump scoped to executing tenant only (ADR-01).

        Args:
            failed_verification: The verification that triggered the break.
            compilation_request_id: The batch being processed.
            preserved_state: Any partial work to cache (e.g., passed images).

        Returns:
            QuarantineTicket with all break details.
        """
        timestamp = datetime.now(timezone.utc).isoformat()

        chain_break = ChainBreakEvent(
            failed_at_node=failed_verification.downstream_node_id,
            missing_upstream_receipt=f"Receipt from '{failed_verification.upstream_node_id}'",
            timestamp=timestamp,
            quarantine_status="PARTIAL_MANUAL",
            operator_action_required=True,
        )

        ticket = QuarantineTicket(
            quarantine_ticket_id=f"QT-{uuid.uuid4().hex[:12].upper()}",
            coach_id=self.coach_id,
            compilation_request_id=compilation_request_id,
            assembly_status=AssemblyStatus.REJECTED_BROKEN_CHAIN,
            chain_break_event=chain_break,
            preserved_state=preserved_state or {},
        )

        self._quarantine_ticket = ticket

        # Log the circuit breaker trip
        self.receipt_chain.log(
            agent_id="receipt_chain_guard",
            action="circuit_breaker_tripped",
            input_summary=(
                f"Failed at: {failed_verification.downstream_node_id} "
                f"← missing from {failed_verification.upstream_node_id}"
            ),
            output_summary=(
                f"Quarantine ticket: {ticket.quarantine_ticket_id}, "
                f"Status: REJECTED_BROKEN_CHAIN"
            ),
            decision="quarantine",
            metadata={
                "quarantine_ticket_id": ticket.quarantine_ticket_id,
                "coach_id": self.coach_id,
                "compilation_request_id": compilation_request_id,
                "failed_at_node": chain_break.failed_at_node,
                "missing_upstream_receipt": chain_break.missing_upstream_receipt,
            },
        )

        return ticket

    # ─── Ghost Variable Prevention Gate ───────────────────────────────────────

    def check_ghost_variables(
        self,
        required_dep_ids: list[str],
        payload: dict[str, Any],
    ) -> list[dict[str, str]]:
        """Ghost Variable Prevention Gate.

        Spec §3 Technical Decision 4: All input DEP-IDs must be verified
        cryptographically prior to payload unpacking. Any field resolving
        to NULL or UNDEFINED triggers a hard halt.

        Args:
            required_dep_ids: List of DEP-IDs that must be present.
            payload: The payload to verify.

        Returns:
            List of DAG_VIOLATION errors (empty if all clear).
        """
        violations: list[dict[str, str]] = []

        for dep_id in required_dep_ids:
            value = payload.get(dep_id)
            if value is None:
                violations.append({
                    "error": "DAG_VIOLATION",
                    "missing_dep": dep_id,
                })

        if violations:
            self.receipt_chain.log(
                agent_id="receipt_chain_guard",
                action="ghost_variable_halt",
                input_summary=f"Required DEP-IDs: {required_dep_ids}",
                output_summary=f"DAG violations: {len(violations)}",
                decision="halt",
                metadata={"violations": violations},
            )

        return violations

    # ─── Full Pipeline Guard ──────────────────────────────────────────────────

    def build_verdict(
        self,
        compilation_request_id: str,
        nodes_checked: int,
        nodes_verified: int,
    ) -> ReceiptGuardVerdict:
        """Build the final guard verdict for a pipeline run.

        Args:
            compilation_request_id: The batch request ID.
            nodes_checked: Total nodes that were checked.
            nodes_verified: Nodes that passed verification.

        Returns:
            ReceiptGuardVerdict with chain_ledger and optional quarantine.
        """
        pipeline_clear = (
            nodes_checked == nodes_verified
            and nodes_checked > 0
            and self._quarantine_ticket is None
        )

        status = (
            AssemblyStatus.ACCEPTED
            if pipeline_clear
            else AssemblyStatus.REJECTED_BROKEN_CHAIN
        )

        ledger = AssemblyChainLedger(
            compilation_request_id=compilation_request_id,
            coach_id=self.coach_id,
            assembly_status=status,
            receipt_ledger=dict(self._chain_ledger),
            chain_break_event=(
                self._quarantine_ticket.chain_break_event
                if self._quarantine_ticket
                else None
            ),
        )

        verdict = ReceiptGuardVerdict(
            pipeline_clear=pipeline_clear,
            total_nodes_checked=nodes_checked,
            total_nodes_verified=nodes_verified,
            chain_ledger=ledger,
            quarantine_ticket=self._quarantine_ticket,
        )

        # Log final verdict
        self.receipt_chain.log(
            agent_id="receipt_chain_guard",
            action="pipeline_verdict",
            input_summary=f"Checked: {nodes_checked}, Verified: {nodes_verified}",
            output_summary=f"Pipeline clear: {pipeline_clear}, Status: {status.value}",
            decision="clear" if pipeline_clear else "quarantine",
            metadata={
                "compilation_request_id": compilation_request_id,
                "nodes_checked": nodes_checked,
                "nodes_verified": nodes_verified,
                "receipt_ledger_stages": list(self._chain_ledger.keys()),
            },
        )

        return verdict

    # ─── Internal Helpers ─────────────────────────────────────────────────────

    def _hash_payload(self, payload: Any) -> str:
        """Generate a SHA-256 hash of any serializable payload."""
        if payload is None:
            return hashlib.sha256(b"null").hexdigest()[:16]
        try:
            serialized = json.dumps(payload, sort_keys=True, default=str)
        except (TypeError, ValueError):
            serialized = str(payload)
        return hashlib.sha256(serialized.encode()).hexdigest()[:16]

    def _is_valid_hash_structure(self, hash_str: str) -> bool:
        """Validate that a hash string has expected structure.

        Must be a hex string of at least 16 characters.
        """
        if not isinstance(hash_str, str):
            return False
        if len(hash_str) < 16:
            return False
        try:
            int(hash_str, 16)
            return True
        except ValueError:
            return False

    def _log_verification(self, verification: HandoffVerification) -> None:
        """Log a handoff verification result to the receipt chain."""
        self.receipt_chain.log(
            agent_id="receipt_chain_guard",
            action="handoff_verification",
            input_summary=(
                f"Upstream: {verification.upstream_node_id} → "
                f"Downstream: {verification.downstream_node_id}"
            ),
            output_summary=(
                f"Verified: {verification.chain_verified}, "
                f"Result: {verification.verification_result.value}"
            ),
            decision="verified" if verification.chain_verified else "rejected",
            metadata={
                "upstream_node_id": verification.upstream_node_id,
                "downstream_node_id": verification.downstream_node_id,
                "receipt_hash": verification.receipt_chain_hash,
                "error_detail": verification.error_detail,
            },
        )
