"""
CCP Provenance Tracer
Task 5.08 — Full chain-of-custody for any Asset ID.

Given any Asset ID, returns the complete provenance chain:
  source data → research → generation prompt → agent output →
  validation decisions → operator edits → final version

Queries: Receipt Chain (JSONL/Supabase) + file system artifacts.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

from src.ccp.core.receipt_chain import ReceiptChain


class ProvenanceStep(BaseModel):
    """A single step in the provenance chain."""

    timestamp: str
    agent_id: str
    action: str
    input_summary: str = ""
    output_summary: str = ""
    decision: str = ""
    decision_rationale: str = ""
    metadata: dict = Field(default_factory=dict)


class ProvenanceReport(BaseModel):
    """Full provenance chain for an asset."""

    asset_id: str
    coach_acronym: str
    total_steps: int
    chain: list[ProvenanceStep]
    first_seen: str
    last_modified: str
    agents_involved: list[str]
    current_status: str


class ProvenanceTracer:
    """Trace the full provenance chain for any asset."""

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)

    def trace(self, asset_id: str) -> ProvenanceReport:
        """Trace the complete provenance for an asset.

        Args:
            asset_id: Universal Asset ID to trace

        Returns:
            Full ProvenanceReport with every step
        """
        # Query Receipt Chain for all entries related to this asset
        all_entries = self._query_chain(asset_id)

        if not all_entries:
            return ProvenanceReport(
                asset_id=asset_id,
                coach_acronym=self.coach_acronym,
                total_steps=0,
                chain=[],
                first_seen="never",
                last_modified="never",
                agents_involved=[],
                current_status="not_found",
            )

        # Sort by timestamp
        all_entries.sort(key=lambda e: e.get("timestamp", ""))

        # Build the chain
        chain = []
        agents = set()
        for entry in all_entries:
            step = ProvenanceStep(
                timestamp=entry.get("timestamp", ""),
                agent_id=entry.get("agent_id", "unknown"),
                action=entry.get("action", "unknown"),
                input_summary=entry.get("input_summary", ""),
                output_summary=entry.get("output_summary", ""),
                decision=entry.get("decision", ""),
                decision_rationale=entry.get("decision_rationale", ""),
                metadata=entry.get("metadata", {}),
            )
            chain.append(step)
            agents.add(step.agent_id)

        # Determine current status from last entry
        last = chain[-1]
        status_map = {
            "approved": "approved_pending_delivery",
            "completed": "completed",
            "rejected": "rejected",
            "edited": "edited_pending_review",
            "requires_rewrite": "in_rewrite_loop",
            "crisis_halt": "halted",
        }
        current_status = status_map.get(last.decision, last.decision)

        return ProvenanceReport(
            asset_id=asset_id,
            coach_acronym=self.coach_acronym,
            total_steps=len(chain),
            chain=chain,
            first_seen=chain[0].timestamp,
            last_modified=chain[-1].timestamp,
            agents_involved=sorted(agents),
            current_status=current_status,
        )

    def _query_chain(self, asset_id: str) -> list[dict]:
        """Query the Receipt Chain for all entries related to an asset."""
        log_dir = Path(f"coaches/{self.coach_acronym}/logs")
        if not log_dir.exists():
            return []

        entries = []
        for log_file in log_dir.glob("receipt_chain*.jsonl"):
            with open(log_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                        if entry.get("asset_id") == asset_id:
                            entries.append(entry)
                        # Also check metadata for related asset references
                        if asset_id in json.dumps(entry.get("metadata", {})):
                            if entry not in entries:
                                entries.append(entry)
                    except json.JSONDecodeError:
                        continue

        return entries

    def format_report(self, report: ProvenanceReport) -> str:
        """Format a provenance report as human-readable text."""
        lines = [
            f"PROVENANCE REPORT: {report.asset_id}",
            f"Coach: {report.coach_acronym}",
            f"Status: {report.current_status}",
            f"Total steps: {report.total_steps}",
            f"Agents: {', '.join(report.agents_involved)}",
            f"First seen: {report.first_seen}",
            f"Last modified: {report.last_modified}",
            "",
            "CHAIN:",
        ]

        for i, step in enumerate(report.chain, 1):
            lines.append(f"  [{i}] {step.timestamp}")
            lines.append(f"      Agent: {step.agent_id}")
            lines.append(f"      Action: {step.action}")
            if step.input_summary:
                lines.append(f"      Input: {step.input_summary}")
            if step.output_summary:
                lines.append(f"      Output: {step.output_summary}")
            if step.decision:
                lines.append(f"      Decision: {step.decision}")
            if step.decision_rationale:
                lines.append(f"      Rationale: {step.decision_rationale}")
            lines.append("")

        return "\n".join(lines)
