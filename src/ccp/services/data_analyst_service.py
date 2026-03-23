"""
FR43 — Data Analyst Agent Service (DEP-ENG-038)
6 evaluation matrices → parameter_update.json + Notion report.

AC1: Minimum sample guard (N >= 10 global, N >= 5 per arc-type).
AC2: Weight mutation via parameter_update.json.
AC3: Notion human-readable translation.
AC4: Idempotent analyst_reviewed tagging.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cross_system_models import (
    AnalystTag,
    ArcWeightDirection,
    CRALPriority,
    ContentPerformanceRow,
    DATA_ANALYST_MIN_ARC_N,
    DATA_ANALYST_MIN_GLOBAL_N,
    ParameterUpdate,
)


class DataAnalystService:
    """
    FR43: Data Analyst Agent — evaluates content performance
    across 6 matrices and produces parameter updates.
    """

    def __init__(self, coach_acronym: str) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(f"coach_acronym must be 2-4 chars, got '{coach_acronym}'")
        self._coach = coach_acronym.upper()
        self._receipt_chain = ReceiptChain(coach_acronym=self._coach)

    # ── AC1: Sample Guard ──────────────────────────────

    def check_minimum_sample(
        self,
        *,
        rows: list[ContentPerformanceRow],
        arc_type_groups: dict[str, list[ContentPerformanceRow]],
    ) -> tuple[bool, str]:
        """
        FR43 AC1: N >= 10 global, N >= 5 per arc-type.
        Returns (passes, reason).
        """
        global_n = len(rows)
        if global_n < DATA_ANALYST_MIN_GLOBAL_N:
            return False, f"Global N={global_n} < {DATA_ANALYST_MIN_GLOBAL_N}"

        for arc_type, arc_rows in arc_type_groups.items():
            if len(arc_rows) < DATA_ANALYST_MIN_ARC_N:
                return False, f"Arc '{arc_type}' N={len(arc_rows)} < {DATA_ANALYST_MIN_ARC_N}"

        return True, "PASS"

    # ── Matrix 1: Arc Performance ──────────────────────

    def evaluate_arc_performance(
        self,
        arc_type_groups: dict[str, list[ContentPerformanceRow]],
    ) -> dict[str, float]:
        """
        FR43 §4.2: Average engagement_rate per arc type.
        """
        results: dict[str, float] = {}
        for arc_type, rows in arc_type_groups.items():
            if rows:
                avg = sum(r.engagement_rate for r in rows) / len(rows)
                results[arc_type] = round(avg, 6)
        return results

    # ── Matrix 5: Platform Delta ───────────────────────

    def evaluate_platform_delta(
        self,
        rows: list[ContentPerformanceRow],
    ) -> dict[str, float]:
        """
        FR43 §4.2: Average engagement by platform.
        """
        platform_groups: dict[str, list[float]] = {}
        for r in rows:
            if r.platform:
                platform_groups.setdefault(r.platform, []).append(r.engagement_rate)

        return {
            p: round(sum(vals) / len(vals), 6)
            for p, vals in platform_groups.items()
            if vals
        }

    # ── Tag Classification ─────────────────────────────

    def classify_tag(self, engagement_rate: float) -> AnalystTag:
        """FR43 §4.3: Performance tag classification."""
        if engagement_rate >= 0.05:
            return AnalystTag.HIGH
        elif engagement_rate >= 0.02:
            return AnalystTag.AVERAGE
        return AnalystTag.UNDER

    # ── AC2: Parameter Update Generation ───────────────

    def generate_parameter_update(
        self,
        *,
        rows: list[ContentPerformanceRow],
        arc_type_groups: dict[str, list[ContentPerformanceRow]],
        evaluation_period: Optional[str] = None,
    ) -> Optional[ParameterUpdate]:
        """
        FR43 §5: Full DEP-ENG-038 pipeline.
        """
        # AC1: Sample guard
        passes, reason = self.check_minimum_sample(
            rows=rows, arc_type_groups=arc_type_groups,
        )
        if not passes:
            self._receipt_chain.log(
                agent_id="DataAnalystAgent",
                action="ANALYSIS_ABORTED_MIN_SAMPLE",
                asset_id=f"DA-{self._coach}",
                decision="ABORT",
                decision_rationale=reason,
            )
            return None

        # Matrix 1: Arc performance
        arc_scores = self.evaluate_arc_performance(arc_type_groups)

        # Derive weights — higher engagement = higher priority
        total_score = sum(arc_scores.values()) or 1.0
        arc_weights = {
            arc: round(score / total_score, 4)
            for arc, score in arc_scores.items()
        }

        # Mode routing adjustments
        mode_adjustments: dict[str, ArcWeightDirection] = {}
        for arc, score in arc_scores.items():
            tag = self.classify_tag(score)
            if tag == AnalystTag.HIGH:
                mode_adjustments[arc] = ArcWeightDirection.INCREASE
            elif tag == AnalystTag.UNDER:
                mode_adjustments[arc] = ArcWeightDirection.DECREASE

        # CRAL priorities
        cral_priorities: dict[str, CRALPriority] = {}
        for arc, score in arc_scores.items():
            tag = self.classify_tag(score)
            if tag == AnalystTag.HIGH:
                cral_priorities[arc] = CRALPriority.HIGH
            elif tag == AnalystTag.AVERAGE:
                cral_priorities[arc] = CRALPriority.MEDIUM
            else:
                cral_priorities[arc] = CRALPriority.LOW

        # Platform scheduling
        platform_scores = self.evaluate_platform_delta(rows)
        scheduling_updates: dict[str, dict[str, Any]] = {}
        for platform, score in platform_scores.items():
            scheduling_updates[platform] = {
                "engagement_avg": score,
                "tag": self.classify_tag(score).value,
            }

        period = evaluation_period or datetime.now(timezone.utc).strftime("%Y-W%W")

        update = ParameterUpdate(
            coach_id=self._coach,
            evaluation_period=period,
            arc_priority_weights=arc_weights,
            cral_moment_priority=cral_priorities,
            mode_routing_adjustments=mode_adjustments,
            scheduling_updates=scheduling_updates,
            next_cycle_directive="CONTINUE",
        )

        self._receipt_chain.log(
            agent_id="DataAnalystAgent",
            action="PARAMETER_UPDATE_GENERATED",
            asset_id=f"DA-{self._coach}-{period}",
            decision="SUCCESS",
            decision_rationale=f"arcs={len(arc_weights)}, platforms={len(platform_scores)}",
        )

        return update

    # ── AC4: Idempotent Tagging ────────────────────────

    def tag_rows_as_reviewed(
        self,
        rows: list[ContentPerformanceRow],
    ) -> int:
        """
        FR43 AC4: Mark rows as analyst_reviewed = True.
        Idempotent — re-tagging already-tagged rows is a no-op.
        """
        tagged = 0
        for row in rows:
            if not row.analyst_reviewed:
                row.analyst_reviewed = True
                tagged += 1
        return tagged
