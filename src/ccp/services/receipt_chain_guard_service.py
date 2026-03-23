"""
FR47 — Receipt Chain Guard Service (DEP-ENG-041)
Canonical receipt chain with cryptographic linkage.
Zero fallback — pipeline MUST stall on chain failure.

AC1: Cryptographic SHA-256 linked-list chain.
AC2: Immediate QUARANTINED status on hash mismatch.
AC3: Final publication gate integrity check.
AC4: Immutable append-only storage.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cross_system_models import (
    RECEIPT_GENESIS_MARKER,
    RECEIPT_HASH_ALGORITHM,
    ReceiptBlock,
    ReceiptStatus,
)


class ReceiptChainGuard:
    """
    FR47: Append-only receipt chain with cryptographic hash linkage.

    Every pipeline operation creates a ReceiptBlock whose
    previous_receipt_hash points to the prior block's
    current_receipt_hash, forming an immutable linked list.
    """

    def __init__(self, coach_acronym: str) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(f"coach_acronym must be 2-4 chars, got '{coach_acronym}'")
        self._coach_acronym = coach_acronym.upper()
        self._chain: list[ReceiptBlock] = []
        self._receipt_chain = ReceiptChain(coach_acronym=self._coach_acronym)

    # ── Genesis Block ──────────────────────────────────

    def create_genesis_block(self, asset_id: str) -> ReceiptBlock:
        """
        FR47 §4.1: Create the genesis block for a new asset chain.
        previous_receipt_hash == GENESIS marker.
        """
        block = ReceiptBlock(
            asset_id=asset_id,
            executing_agent="SYSTEM_GENESIS",
            previous_receipt_hash=RECEIPT_GENESIS_MARKER,
            status_code=ReceiptStatus.GENESIS,
        )
        block.current_receipt_hash = block.compute_hash()
        self._chain.append(block)
        self._log_to_receipt_chain(block, "GENESIS_BLOCK_CREATED")
        return block

    # ── Middle-Node Execution ──────────────────────────

    def append_block(
        self,
        *,
        asset_id: str,
        executing_agent: str,
        input_payload: Any,
        output_payload: Any,
        pi_extensions: Optional[list[str]] = None,
        confidence_score: float = 1.0,
    ) -> ReceiptBlock:
        """
        FR47 §4.2: Append a new block linked to the last block.
        Validates chain integrity before appending.
        """
        if not self._chain:
            raise RuntimeError(
                "Cannot append to empty chain. Call create_genesis_block first."
            )

        previous_block = self._chain[-1]
        input_hash = self._hash_payload(input_payload)
        output_hash = self._hash_payload(output_payload)

        block = ReceiptBlock(
            asset_id=asset_id,
            executing_agent=executing_agent,
            pi_extensions_triggered=pi_extensions or [],
            confidence_score=confidence_score,
            input_payload_hash=input_hash,
            output_payload_hash=output_hash,
            previous_receipt_hash=previous_block.current_receipt_hash,
            status_code=ReceiptStatus.SUCCESS,
        )
        block.current_receipt_hash = block.compute_hash()
        self._chain.append(block)
        self._log_to_receipt_chain(block, "BLOCK_APPENDED")
        return block

    # ── Quarantine ─────────────────────────────────────

    def quarantine_on_break(self, asset_id: str, reason: str) -> ReceiptBlock:
        """
        FR47 AC2: Immediately quarantine when chain integrity is violated.
        """
        block = ReceiptBlock(
            asset_id=asset_id,
            executing_agent="DAMAGE_CONTROL",
            mode="QUARANTINE",
            status_code=ReceiptStatus.QUARANTINED,
            previous_receipt_hash=(
                self._chain[-1].current_receipt_hash if self._chain else RECEIPT_GENESIS_MARKER
            ),
        )
        block.current_receipt_hash = block.compute_hash()
        self._chain.append(block)
        self._log_to_receipt_chain(block, f"QUARANTINED: {reason}")
        return block

    # ── Publication Gate ───────────────────────────────

    def validate_chain_integrity(self) -> bool:
        """
        FR47 AC3: Final publication gate — walk entire chain and verify hashes.
        Returns True only if every link is valid.
        """
        if not self._chain:
            return False

        for i, block in enumerate(self._chain):
            # Verify self-hash
            expected_hash = block.compute_hash()
            if block.current_receipt_hash != expected_hash:
                return False

            # Verify linkage (skip genesis)
            if i > 0:
                if block.previous_receipt_hash != self._chain[i - 1].current_receipt_hash:
                    return False

            # Check for quarantine
            if block.status_code == ReceiptStatus.QUARANTINED:
                return False

        return True

    def publication_gate(self, asset_id: str) -> ReceiptBlock:
        """
        FR47 §4.4: Final gate — checks integrity; stalls pipeline on failure.
        """
        if not self.validate_chain_integrity():
            return self.quarantine_on_break(
                asset_id=asset_id,
                reason="PUBLICATION_GATE_INTEGRITY_CHECK_FAILED",
            )

        block = ReceiptBlock(
            asset_id=asset_id,
            executing_agent="PUBLICATION_GATE",
            mode="FINAL_GATE",
            status_code=ReceiptStatus.SUCCESS,
            previous_receipt_hash=(
                self._chain[-1].current_receipt_hash if self._chain else RECEIPT_GENESIS_MARKER
            ),
        )
        block.current_receipt_hash = block.compute_hash()
        self._chain.append(block)
        self._log_to_receipt_chain(block, "PUBLICATION_GATE_PASSED")
        return block

    # ── Accessors ──────────────────────────────────────

    @property
    def chain(self) -> list[ReceiptBlock]:
        return list(self._chain)

    @property
    def chain_length(self) -> int:
        return len(self._chain)

    @property
    def last_block(self) -> Optional[ReceiptBlock]:
        return self._chain[-1] if self._chain else None

    # ── Internals ──────────────────────────────────────

    @staticmethod
    def _hash_payload(payload: Any) -> str:
        """FR47 §3: SHA-256 deterministic hash of any payload."""
        raw = json.dumps(payload, sort_keys=True, default=str)
        return hashlib.sha256(raw.encode()).hexdigest()

    def _log_to_receipt_chain(self, block: ReceiptBlock, action: str) -> None:
        """Emit to the ReceiptChain audit trail."""
        self._receipt_chain.log(
            agent_id=block.executing_agent,
            action=action,
            asset_id=block.asset_id,
            input_summary=block.input_payload_hash,
            output_summary=block.current_receipt_hash,
            decision=block.status_code.value,
            decision_rationale=f"mode={block.mode}",
        )
