"""
FR37 — Cross-System Intelligence Routing (DEP-ENG-032)
Sunday 23:00 UTC weekly intelligence aggregation.
Anonymization, NON-DESTRUCTIVE append to DEP-ENG-006.

AC1: Data aggregation from MemoryFolder sweep.
AC2: PII zero-trust (no raw_transcript in output).
AC3: CCF integration override (append-only :WeeklyModifier nodes).
AC4: Cross-tenant execution with coach-scoped isolation.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cross_system_models import (
    DORMANCY_MIN_CLIENTS_FOR_SBM,
    PainPointFrequency,
    SBMAggregationMetrics,
    SBMStrategicSynthesis,
    SundayBotMeetingPayload,
)


class CrossSystemIntelligenceService:
    """
    FR37: Weekly intelligence routing — Sunday Bot Meeting.
    Aggregates MemoryFolder data, anonymizes, appends to graph.
    """

    def __init__(self, coach_acronym: str) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(f"coach_acronym must be 2-4 chars, got '{coach_acronym}'")
        self._coach = coach_acronym.upper()
        self._receipt_chain = ReceiptChain(coach_acronym=self._coach)

    # ── Stage 1: Aggregation Sweep ─────────────────────

    def aggregate_memory_folders(
        self,
        *,
        client_data: list[dict[str, Any]],
    ) -> Optional[SBMAggregationMetrics]:
        """
        FR37 AC1/§6: Aggregate client data.
        Aborts if <3 active clients.
        """
        active_count = len(client_data)
        if active_count < DORMANCY_MIN_CLIENTS_FOR_SBM:
            self._receipt_chain.log(
                agent_id="CrossSystemIntelligence",
                action="SBM_ABORTED_MIN_CLIENTS",
                asset_id=f"SBM-{self._coach}",
                decision="ABORT",
                decision_rationale=f"active_clients={active_count}, min={DORMANCY_MIN_CLIENTS_FOR_SBM}",
            )
            return None

        # Aggregate pain points
        pain_freq: dict[str, int] = {}
        coping_freq: dict[str, int] = {}

        for client in client_data:
            for pp in client.get("pain_points", []):
                pain_freq[pp] = pain_freq.get(pp, 0) + 1
            for cm in client.get("coping_mechanisms", []):
                coping_freq[cm] = coping_freq.get(cm, 0) + 1

        top_pain = sorted(pain_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        top_coping = sorted(coping_freq.items(), key=lambda x: x[1], reverse=True)[:5]

        return SBMAggregationMetrics(
            active_clients_analyzed=active_count,
            top_pain_points=[
                PainPointFrequency(theme=t, frequency=f) for t, f in top_pain
            ],
            top_coping_mechanisms=[
                PainPointFrequency(theme=t, frequency=f) for t, f in top_coping
            ],
        )

    # ── Stage 2: Density Analysis ──────────────────────

    def synthesize_strategy(
        self,
        metrics: SBMAggregationMetrics,
    ) -> SBMStrategicSynthesis:
        """
        FR37 §4.2: Density analysis and thematic synthesis.
        """
        meta_theme = "General Wellness"
        if metrics.top_pain_points:
            meta_theme = metrics.top_pain_points[0].theme

        return SBMStrategicSynthesis(
            recommended_meta_theme=meta_theme,
            archetype_targeting_weight="balanced",
        )

    # ── Stage 3: Anonymization Check ───────────────────

    def verify_pii_clean(self, payload: SundayBotMeetingPayload) -> bool:
        """
        FR37 AC2: PII zero-trust verification.
        No raw_transcript strings in the output.
        """
        payload_str = payload.model_dump_json()
        pii_keywords = ["raw_transcript", "email", "phone_number", "address"]
        for keyword in pii_keywords:
            if keyword in payload_str.lower():
                return False
        return True

    # ── Full Pipeline ──────────────────────────────────

    def run_sunday_bot_meeting(
        self,
        *,
        client_data: list[dict[str, Any]],
        period_start: Optional[str] = None,
        period_end: Optional[str] = None,
    ) -> Optional[SundayBotMeetingPayload]:
        """
        FR37 §5: Full DEP-ENG-032 pipeline.
        """
        # Stage 1: Aggregation
        metrics = self.aggregate_memory_folders(client_data=client_data)
        if metrics is None:
            return None

        # Stage 2: Synthesis
        synthesis = self.synthesize_strategy(metrics)

        now = datetime.now(timezone.utc)
        period = {
            "start": period_start or now.strftime("%Y-%m-%d"),
            "end": period_end or now.strftime("%Y-%m-%d"),
        }

        payload = SundayBotMeetingPayload(
            coach_id=self._coach,
            period=period,
            aggregation_metrics=metrics,
            strategic_synthesis=synthesis,
        )

        # Stage 3: PII check
        is_clean = self.verify_pii_clean(payload)
        payload.pii_leak_status = "CLEAN" if is_clean else "CONTAMINATED"

        self._receipt_chain.log(
            agent_id="CrossSystemIntelligence",
            action="SBM_COMPLETE",
            asset_id=payload.routing_id,
            decision="SUCCESS" if is_clean else "PII_CONTAMINATED",
            decision_rationale=f"clients={metrics.active_clients_analyzed}, theme={synthesis.recommended_meta_theme}",
        )

        return payload
