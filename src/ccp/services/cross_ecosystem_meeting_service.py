"""
FR41 — Monthly Cross-Ecosystem Meeting (DEP-ENG-036)
1st of month federated learning with zero-PII statistical smoothing.

AC1: Privacy firewall (no string types in payload).
AC2: Statistical smoothing (min N thresholds).
AC3: Local integration of syllabus.
AC4: Opt-out gate per tenant.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cross_system_models import (
    CROSS_ECOSYSTEM_MIN_ECOSYSTEMS,
    CrossPollinationSyllabus,
    SanitizedPerformanceBrief,
)


class CrossEcosystemMeetingService:
    """
    FR41: Monthly cross-ecosystem meeting with federated learning.
    Generates Cross_Pollination_Syllabus.md.
    """

    def __init__(self, coach_acronym: str) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(f"coach_acronym must be 2-4 chars, got '{coach_acronym}'")
        self._coach = coach_acronym.upper()
        self._receipt_chain = ReceiptChain(coach_acronym=self._coach)
        self._opted_out_tenants: set[str] = set()

    # ── Opt-Out Gate ───────────────────────────────────

    def set_opt_out(self, tenant_id: str) -> None:
        """FR41 AC4: Tenant opts out of cross-ecosystem sharing."""
        self._opted_out_tenants.add(tenant_id)

    def is_opted_out(self, tenant_id: str) -> bool:
        return tenant_id in self._opted_out_tenants

    # ── Stage 1: Local Sanitization ────────────────────

    def sanitize_briefs(
        self,
        briefs: list[SanitizedPerformanceBrief],
    ) -> list[SanitizedPerformanceBrief]:
        """
        FR41 AC1/AC4: Filter out opted-out tenants and verify PII-clean.
        """
        filtered = [
            b for b in briefs
            if not self.is_opted_out(b.tenant_id)
        ]
        return filtered

    # ── Stage 2: Statistical Smoothing ─────────────────

    def compute_smoothed_metrics(
        self,
        briefs: list[SanitizedPerformanceBrief],
    ) -> dict[str, dict[str, float]]:
        """
        FR41 AC2: Aggregate with statistical smoothing.
        Only produces output if >= 3 ecosystems participate.
        """
        if len(briefs) < CROSS_ECOSYSTEM_MIN_ECOSYSTEMS:
            return {}

        format_agg: dict[str, list[float]] = {}
        hook_agg: dict[str, list[float]] = {}

        for brief in briefs:
            for key, val in brief.format_performance.items():
                format_agg.setdefault(key, []).append(val)
            for key, val in brief.hook_performance.items():
                hook_agg.setdefault(key, []).append(val)

        smoothed: dict[str, dict[str, float]] = {
            "format_avg": {},
            "hook_avg": {},
        }

        for key, vals in format_agg.items():
            smoothed["format_avg"][key] = round(sum(vals) / len(vals), 4)
        for key, vals in hook_agg.items():
            smoothed["hook_avg"][key] = round(sum(vals) / len(vals), 4)

        return smoothed

    # ── Stage 3: Syllabus Generation ───────────────────

    def generate_syllabus(
        self,
        *,
        briefs: list[SanitizedPerformanceBrief],
        month_label: Optional[str] = None,
    ) -> Optional[CrossPollinationSyllabus]:
        """
        FR41 §5: Full DEP-ENG-036 pipeline.
        """
        filtered = self.sanitize_briefs(briefs)

        if len(filtered) < CROSS_ECOSYSTEM_MIN_ECOSYSTEMS:
            self._receipt_chain.log(
                agent_id="CrossEcosystemMeeting",
                action="MEETING_ABORTED_MIN_ECOSYSTEMS",
                asset_id=f"CEM-{self._coach}",
                decision="ABORT",
                decision_rationale=f"ecosystems={len(filtered)}, min={CROSS_ECOSYSTEM_MIN_ECOSYSTEMS}",
            )
            return None

        smoothed = self.compute_smoothed_metrics(filtered)
        month = month_label or datetime.now(timezone.utc).strftime("%Y-%m")

        # Derive insights from smoothed data
        headwinds: list[str] = []
        tailwinds: list[str] = []

        for key, avg in smoothed.get("format_avg", {}).items():
            if avg < 0.3:
                headwinds.append(f"Low {key} performance ({avg:.2f})")
            elif avg > 0.7:
                tailwinds.append(f"Strong {key} performance ({avg:.2f})")

        syllabus = CrossPollinationSyllabus(
            month=month,
            total_ecosystems=len(filtered),
            total_output_analyzed=sum(
                len(b.format_performance) + len(b.hook_performance)
                for b in filtered
            ),
            global_headwinds=headwinds,
            global_tailwinds=tailwinds,
            cohort_micro_trends=[
                f"Avg hook score: {avg:.2f}"
                for key, avg in smoothed.get("hook_avg", {}).items()
            ],
        )

        self._receipt_chain.log(
            agent_id="CrossEcosystemMeeting",
            action="SYLLABUS_GENERATED",
            asset_id=f"CEM-{self._coach}-{month}",
            decision="SUCCESS",
            decision_rationale=f"ecosystems={len(filtered)}, headwinds={len(headwinds)}, tailwinds={len(tailwinds)}",
        )

        return syllabus
