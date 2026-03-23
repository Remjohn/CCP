"""
CCP FR21 — Receipt Chain Guard Protocol Models (DEP-PROTO-010)

Pydantic models for the Receipt Chain Guard protocol layer.
FR21 defines WHEN and HOW receipt writes occur across all pipeline stages.
The physical receipt infrastructure (DEP-ENG-041) is in receipt_chain.py.

Spec reference: FR21_Receipt_Chain_Guard_Tech_Spec.md
  §4 — Stage 1: Receipt Generation (Node Emit)
  §4 — Stage 2: Handoff Verification (Node Intake)
  §4 — Stage 3: Circuit Breaker & Quarantine
  §5 — assembly_report_chain_ledger.json schema
"""

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


# ─── Enumerations ─────────────────────────────────────────────────────────────

class AssemblyStatus(str, Enum):
    """Assembly status states for the pipeline."""

    ACCEPTED = "ACCEPTED"
    HALTED = "HALTED"
    REJECTED_BROKEN_CHAIN = "REJECTED_BROKEN_CHAIN"
    PARTIAL_MANUAL = "PARTIAL_MANUAL"
    FAILED_UNRECOVERABLE = "FAILED_UNRECOVERABLE"


class GuardStage(str, Enum):
    """Receipt Chain Guard pipeline stages."""

    RECEIPT_GENERATION = "RECEIPT-GENERATION"
    HANDOFF_VERIFICATION = "HANDOFF-VERIFICATION"
    CIRCUIT_BREAKER_QUARANTINE = "CIRCUIT-BREAKER-QUARANTINE"


class VerificationResult(str, Enum):
    """Result of a handoff verification check."""

    VALID = "VALID"
    MISSING_HASH = "MISSING_HASH"
    INVALID_STRUCTURE = "INVALID_STRUCTURE"
    PARTIAL_STATUS = "PARTIAL_STATUS"


# ─── Receipt Generation Models ────────────────────────────────────────────────

class NodeReceipt(BaseModel):
    """A receipt emitted by a pipeline node after successful execution.

    Spec §4 Stage 1: Component generates a deterministic hash containing
    timestamp + node_id + payload_checksum.
    """

    receipt_chain_hash: str = Field(
        ...,
        description="SHA-256 hash: timestamp + node_id + payload_checksum",
    )
    node_id: str = Field(
        ...,
        description="Unique identifier for the pipeline node (e.g., 'builder_engine_step_1')",
    )
    stage_name: str = Field(
        ...,
        description="Human-readable stage name for the receipt ledger",
    )
    agent_name: str = Field(
        ...,
        description="Agent or adapter that generated this receipt",
    )
    execution_status: str = Field(
        default="SUCCESS",
        description="Must be SUCCESS for receipt to be valid",
    )
    timestamp: str = Field(
        ...,
        description="ISO 8601 UTC timestamp of receipt generation",
    )
    input_payload_hash: str = Field(
        default="",
        description="SHA-256 hash of the input payload",
    )
    output_payload_hash: str = Field(
        default="",
        description="SHA-256 hash of the output payload",
    )
    previous_receipt_hash: Optional[str] = Field(
        default=None,
        description="Hash of the upstream node's receipt (chain link)",
    )


# ─── Handoff Verification Models ──────────────────────────────────────────────

class HandoffVerification(BaseModel):
    """Result of a Stage 2 handoff verification check.

    Spec §4 Stage 2: Downstream agent intercepts payload before internal logic.
    PARTIAL status evaluates as FALSE — instant chain break.
    """

    chain_verified: bool = Field(
        ...,
        description="True only if receipt_chain_hash is present, structurally valid, and status is SUCCESS",
    )
    verification_result: VerificationResult
    upstream_node_id: str = Field(
        ...,
        description="The node ID that should have emitted the receipt",
    )
    downstream_node_id: str = Field(
        ...,
        description="The node ID attempting to consume the payload",
    )
    receipt_chain_hash: Optional[str] = Field(
        default=None,
        description="The hash that was verified (None if missing)",
    )
    error_detail: Optional[str] = Field(
        default=None,
        description="Human-readable error detail when verification fails",
    )


# ─── Circuit Breaker / Quarantine Models ──────────────────────────────────────

class ChainBreakEvent(BaseModel):
    """Records the exact failure point when the chain breaks.

    Spec §5: chain_break_event in assembly_report_chain_ledger.json.
    AC2: Must write the exact failure node to assembly_report.json.
    """

    failed_at_node: str = Field(
        ...,
        description="The exact node where the chain broke (e.g., 'assembler_tier_1_mandatory')",
    )
    missing_upstream_receipt: str = Field(
        ...,
        description="The receipt that was expected but missing or invalid",
    )
    timestamp: str = Field(
        ...,
        description="ISO 8601 UTC timestamp of the break event",
    )
    quarantine_status: str = Field(
        default="PARTIAL_MANUAL",
        description="Status for operator: PARTIAL_MANUAL",
    )
    operator_action_required: bool = Field(
        default=True,
        description="Whether manual operator intervention is needed",
    )


class QuarantineTicket(BaseModel):
    """Quarantine data wrapper when a chain break occurs.

    Spec §4 Stage 3: Wrap the active state into a quarantine object.
    AC4: Must be scoped to the executing tenant's UUID (ADR-01).
    """

    quarantine_ticket_id: str = Field(
        ...,
        description="Unique ID for the quarantine ticket",
    )
    coach_id: str = Field(
        ...,
        min_length=3,
        max_length=3,
        description="ADR-01: Coach acronym scoping this quarantine",
    )
    compilation_request_id: str = Field(
        ...,
        description="The batch/compilation request that was interrupted",
    )
    assembly_status: AssemblyStatus = Field(
        default=AssemblyStatus.REJECTED_BROKEN_CHAIN,
    )
    chain_break_event: ChainBreakEvent
    preserved_state: dict[str, Any] = Field(
        default_factory=dict,
        description="Cached partial work (e.g., passed images from Gate V-00)",
    )
    dag_violation: Optional[dict[str, str]] = Field(
        default=None,
        description="Ghost Variable Prevention Gate error: {'error': 'DAG_VIOLATION', 'missing_dep': '[DEP-ID]'}",
    )


# ─── Assembly Report Chain Ledger ─────────────────────────────────────────────

class AssemblyChainLedger(BaseModel):
    """The receipt_ledger section of assembly_report_chain_ledger.json.

    Spec §5: Archives the cryptographic chain for the Fingerprint Archive.
    Each key is a stage name, each value is the receipt hash.
    """

    compilation_request_id: str
    coach_id: str = Field(..., min_length=3, max_length=3)
    assembly_status: AssemblyStatus
    receipt_ledger: dict[str, str] = Field(
        default_factory=dict,
        description="Stage name → receipt_chain_hash mapping",
    )
    chain_break_event: Optional[ChainBreakEvent] = Field(
        default=None,
        description="Only present if assembly_status is HALTED or REJECTED_BROKEN_CHAIN",
    )


# ─── Guard Verdict ────────────────────────────────────────────────────────────

class ReceiptGuardVerdict(BaseModel):
    """Overall verdict from the Receipt Chain Guard for a pipeline run.

    Combines the chain ledger integrity check with the guard's final decision.
    """

    pipeline_clear: bool = Field(
        ...,
        description="True only if ALL receipts in the chain are verified",
    )
    total_nodes_checked: int = Field(default=0)
    total_nodes_verified: int = Field(default=0)
    chain_ledger: AssemblyChainLedger
    quarantine_ticket: Optional[QuarantineTicket] = Field(
        default=None,
        description="Present only if pipeline_clear is False",
    )
    ghost_variable_violations: list[dict[str, str]] = Field(
        default_factory=list,
        description="List of DAG_VIOLATION errors from Ghost Variable Prevention Gate",
    )
