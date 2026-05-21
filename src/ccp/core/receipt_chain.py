"""
CCP Receipt Chain Logger
Task 1.06 — Immutable audit trail for every agent action in the system.

Every module that performs a meaningful action (generation, validation,
delivery, memory promotion) MUST log through this module. The Receipt
Chain is append-only and provides full provenance traceability.

Usage:
    from src.ccp.core.receipt_chain import ReceiptChain, ReceiptEntry

    rc = ReceiptChain(coach_acronym="NDL")
    rc.log(
        agent_id="minister_identity",
        action="validate_voice_drift",
        asset_id="SCRP-NDL-03-26-A7K2",
        input_summary="Script draft for carousel post",
        output_summary="TTT drift: 8.2% — PASSED",
        decision="approved",
        metadata={"drift_score": 0.082, "threshold": 0.15}
    )
"""

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field


class ReceiptEntry(BaseModel):
    """A single immutable entry in the Receipt Chain."""

    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO 8601 UTC timestamp",
    )
    coach_acronym: str = Field(..., min_length=3, max_length=3)
    agent_id: str = Field(..., description="Agent or module that performed the action")
    action: str = Field(..., description="What was done (e.g. 'generate_script', 'validate_ttt')")
    asset_id: Optional[str] = Field(
        default=None,
        description="Universal Asset ID of the artifact involved",
    )
    person_id: Optional[str] = Field(
        default=None,
        description="Person ID of the client involved (if applicable)",
    )
    input_hash: str = Field(
        default="",
        description="SHA-256 hash of the input data",
    )
    output_hash: str = Field(
        default="",
        description="SHA-256 hash of the output data",
    )
    input_summary: str = Field(
        default="",
        description="Human-readable summary of input (for quick scanning)",
    )
    output_summary: str = Field(
        default="",
        description="Human-readable summary of output/result",
    )
    decision: Optional[str] = Field(
        default=None,
        description="Decision made: approved, rejected, flagged, promoted, etc.",
    )
    decision_rationale: Optional[str] = Field(
        default=None,
        description="Why the decision was made (for audit trail)",
    )
    parent_receipt_id: Optional[str] = Field(
        default=None,
        description="ID of the parent receipt (for chain linking)",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional structured data (scores, thresholds, config)",
    )
    receipt_id: str = Field(
        default="",
        description="Unique ID for this receipt entry (auto-generated)",
    )

    @property
    def payload(self) -> dict[str, Any]:
        """Alias payload property for compatibility with test assertions targeting metadata."""
        res = self.model_dump()
        for k, v in self.metadata.items():
            if k not in res:
                res[k] = v
        res["metadata"] = self.metadata
        return res

    @payload.setter
    def payload(self, value: dict[str, Any]) -> None:
        self.metadata = value

    def model_post_init(self, __context: Any) -> None:
        """Generate receipt_id from content hash after initialization."""
        if not self.receipt_id:
            content = f"{self.timestamp}:{self.agent_id}:{self.action}:{self.asset_id}"
            self.receipt_id = hashlib.sha256(content.encode()).hexdigest()[:16]
        if self.input_summary and not self.input_hash:
            self.input_hash = hashlib.sha256(
                self.input_summary.encode()
            ).hexdigest()[:16]
        if self.output_summary and not self.output_hash:
            self.output_hash = hashlib.sha256(
                self.output_summary.encode()
            ).hexdigest()[:16]


class ReceiptChain:
    """Append-only audit log for a coach instance.

    Supports two storage backends:
    - File system (JSON Lines format) — always available, zero dependencies
    - Supabase (receipt_chain table) — when configured, for queryable access

    The file system log is the source of truth. Supabase is a sync target.
    """

    def __init__(
        self,
        coach_acronym: str,
        log_dir: Optional[str] = None,
        supabase_client: Optional[Any] = None,
    ):
        self.coach_acronym = coach_acronym.upper()
        self.supabase = supabase_client

        # Default log directory: coach instance logs/receipt_chain/
        if log_dir:
            self.log_dir = Path(log_dir)
        else:
            self.log_dir = Path(f"coaches/{self.coach_acronym}/logs/receipt_chain")

        self.log_dir.mkdir(parents=True, exist_ok=True)

    def _get_log_file(self) -> Path:
        """Get the current day's log file (one file per day for manageability)."""
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        return self.log_dir / f"receipt_{today}.jsonl"

    def log(
        self,
        agent_id: str = "system",
        action: str = "generic_action",
        asset_id: Optional[str] = None,
        person_id: Optional[str] = None,
        input_summary: str = "",
        output_summary: str = "",
        decision: Optional[str] = None,
        decision_rationale: Optional[str] = None,
        parent_receipt_id: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
        coach_acronym: Optional[str] = None,
        payload: Optional[dict[str, Any]] = None,
    ) -> ReceiptEntry:
        """Log a new entry to the Receipt Chain.

        Returns the created ReceiptEntry with its generated receipt_id.
        """
        if payload is not None:
            if metadata is None:
                metadata = {}
            metadata.update(payload)

        entry = ReceiptEntry(
            coach_acronym=coach_acronym.upper() if coach_acronym else self.coach_acronym,
            agent_id=agent_id,
            action=action,
            asset_id=asset_id,
            person_id=person_id,
            input_summary=input_summary,
            output_summary=output_summary,
            decision=decision,
            decision_rationale=decision_rationale,
            parent_receipt_id=parent_receipt_id,
            metadata=metadata or {},
        )

        # Write to file (append-only JSONL)
        log_file = self._get_log_file()
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(entry.model_dump_json() + "\n")

        # Sync to Supabase if configured
        if self.supabase:
            self._sync_to_supabase(entry)

        return entry

    def _sync_to_supabase(self, entry: ReceiptEntry) -> None:
        """Push a receipt entry to the Supabase receipt_chain table."""
        try:
            self.supabase.table("receipt_chain").insert(
                entry.model_dump()
            ).execute()
        except Exception as e:
            # Supabase sync failure should never block the pipeline
            # Log to stderr but don't raise
            import sys
            print(
                f"[ReceiptChain] Supabase sync failed for {entry.receipt_id}: {e}",
                file=sys.stderr,
            )

    def query(
        self,
        agent_id: Optional[str] = None,
        action: Optional[str] = None,
        asset_id: Optional[str] = None,
        date: Optional[str] = None,
        limit: int = 100,
    ) -> list[ReceiptEntry]:
        """Query receipt entries from local log files.

        Args:
            agent_id: Filter by agent
            action: Filter by action type
            asset_id: Filter by asset
            date: Filter by date (YYYY-MM-DD). If None, searches all files.
            limit: Maximum entries to return

        Returns:
            List of matching ReceiptEntry objects, newest first.
        """
        entries: list[ReceiptEntry] = []

        # Determine which files to search
        if date:
            files = [self.log_dir / f"receipt_{date}.jsonl"]
        else:
            files = sorted(self.log_dir.glob("receipt_*.jsonl"), reverse=True)

        for log_file in files:
            if not log_file.exists():
                continue
            with open(log_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    entry = ReceiptEntry.model_validate_json(line)

                    # Apply filters
                    if agent_id and entry.agent_id != agent_id:
                        continue
                    if action and entry.action != action:
                        continue
                    if asset_id and entry.asset_id != asset_id:
                        continue

                    entries.append(entry)
                    if len(entries) >= limit:
                        return entries

        return entries

    def get_provenance(self, asset_id: str) -> list[ReceiptEntry]:
        """Get the full provenance chain for an asset.

        Returns all receipt entries related to this asset,
        ordered chronologically (oldest first).
        """
        entries = self.query(asset_id=asset_id, limit=1000)
        return sorted(entries, key=lambda e: e.timestamp)

    def chain_length(self) -> int:
        """Count total entries across all log files."""
        count = 0
        for log_file in self.log_dir.glob("receipt_*.jsonl"):
            with open(log_file, "r", encoding="utf-8") as f:
                count += sum(1 for line in f if line.strip())
        return count
