"""
FR27 — <2s Latency Protocol Service (DEP-PROTO-017)
4-stage pipeline: Ingress & Crisis → Context & Intent → Assembly → Background.

AC1: Sub-1.90s total response time (P95).
AC2: Sub-150ms crisis gate.
AC3: Ghost Typing fallback at 1800ms.
AC4: ADR-01 Redis isolation per coach.
"""

from __future__ import annotations

import time
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cross_system_models import (
    CrisisCheckResult,
    GHOST_TYPING_TRIGGER_MS,
    LATENCY_P95_BUDGET_MS,
    LatencyReceipt,
    ModelExecutionTier,
    ModelTier,
    ModelTierMap,
    TECH_LATENCY_CAP_MS,
)


# ── Default Model Tier Map ────────────────────────────
# FR27 §5: model_execution_tier_map.yaml equivalent

DEFAULT_TIER_MAP = ModelTierMap(
    tasks=[
        ModelExecutionTier(
            agent="Liliane",
            function="crisis_scan",
            model_tier=ModelTier.LOCAL_REGEX_ONLY,
            max_output_tokens=1,
            max_latency_budget_ms=100,
        ),
        ModelExecutionTier(
            agent="Vidye",
            function="context_intent_routing",
            model_tier=ModelTier.FAST_CLASSIFICATION,
            max_output_tokens=50,
            max_latency_budget_ms=800,
        ),
        ModelExecutionTier(
            agent="Aria",
            function="context_extraction",
            model_tier=ModelTier.HEAVY_REASONING,
            max_output_tokens=150,
            max_latency_budget_ms=1500,
        ),
        ModelExecutionTier(
            agent="Artisan",
            function="response_generation",
            model_tier=ModelTier.HEAVY_REASONING,
            max_output_tokens=150,
            max_latency_budget_ms=1200,
        ),
        ModelExecutionTier(
            agent="Azaria",
            function="background_graph_update",
            model_tier=ModelTier.FAST_CLASSIFICATION,
            max_output_tokens=50,
            max_latency_budget_ms=5000,
        ),
    ]
)


class LatencyProtocolService:
    """
    FR27: <2s Latency Protocol orchestrator.

    Stage 1: Ingress & Crisis Pre-Scan (<150ms)
    Stage 2: Context & Intent Routing (<2700ms tech)
    Stage 3: Assembly & Delivery (<1200ms)
    Stage 4: Background Offload (async, no latency gate)
    """

    def __init__(
        self,
        coach_acronym: str,
        tier_map: Optional[ModelTierMap] = None,
    ) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(f"coach_acronym must be 2-4 chars, got '{coach_acronym}'")
        self._coach = coach_acronym.upper()
        self._receipt_chain = ReceiptChain(coach_acronym=self._coach)
        self._tier_map = tier_map or DEFAULT_TIER_MAP
        self._stage_receipts: list[LatencyReceipt] = []

    # ── Stage 1: Ingress & Crisis Pre-Scan ─────────────

    def stage_1_ingress_crisis_scan(
        self,
        *,
        session_id: str,
        raw_message: str,
        crisis_scan_fn: Any = None,
    ) -> LatencyReceipt:
        """
        FR27 Stage 1: Local regex crisis pre-scan.
        Must complete in <150ms. Zero LLM calls.
        """
        start = time.perf_counter_ns()

        crisis_detected = False
        if crisis_scan_fn:
            crisis_detected, _, _ = crisis_scan_fn(raw_message)

        elapsed_ms = int((time.perf_counter_ns() - start) / 1_000_000)

        receipt = LatencyReceipt(
            coach_id=self._coach,
            session_id=session_id,
            stage_name="INGRESS-CRISIS-SCAN",
            agent_name="Liliane",
            latency_ms=elapsed_ms,
            crisis_check=CrisisCheckResult.FAIL if crisis_detected else CrisisCheckResult.PASS,
        )
        self._stage_receipts.append(receipt)
        self._log_stage(receipt)
        return receipt

    # ── Stage 2: Context & Intent Routing ──────────────

    def stage_2_context_intent_routing(
        self,
        *,
        session_id: str,
        context_payload: dict[str, Any],
    ) -> LatencyReceipt:
        """
        FR27 Stage 2: Context extraction + intent routing.
        Tech budget: <2700ms.
        """
        start = time.perf_counter_ns()

        # Simulated routing — in production, Vidye + Aria execute here
        _ = context_payload  # consumed by routing agents

        elapsed_ms = int((time.perf_counter_ns() - start) / 1_000_000)

        receipt = LatencyReceipt(
            coach_id=self._coach,
            session_id=session_id,
            stage_name="CONTEXT-INTENT-ROUTING",
            agent_name="Vidye+Aria",
            latency_ms=elapsed_ms,
        )
        self._stage_receipts.append(receipt)
        self._log_stage(receipt)
        return receipt

    # ── Stage 3: Assembly & Delivery ───────────────────

    def stage_3_assembly_delivery(
        self,
        *,
        session_id: str,
        response_text: str = "",
    ) -> LatencyReceipt:
        """
        FR27 Stage 3: Response assembly.
        Tech budget: <1200ms.
        """
        start = time.perf_counter_ns()

        # Ghost typing check
        total_elapsed = self.total_pipeline_latency_ms()
        ghost_typing = total_elapsed >= GHOST_TYPING_TRIGGER_MS

        elapsed_ms = int((time.perf_counter_ns() - start) / 1_000_000)

        receipt = LatencyReceipt(
            coach_id=self._coach,
            session_id=session_id,
            stage_name="ASSEMBLY-AND-DELIVERY",
            agent_name="Artisan",
            latency_ms=elapsed_ms,
            ghost_typing_triggered=ghost_typing,
        )
        self._stage_receipts.append(receipt)
        self._log_stage(receipt)
        return receipt

    # ── Stage 4: Background Offload ────────────────────

    def stage_4_background_offload(
        self,
        *,
        session_id: str,
    ) -> LatencyReceipt:
        """
        FR27 Stage 4: Async background operations (graph updates).
        No latency gate — fire and forget.
        """
        receipt = LatencyReceipt(
            coach_id=self._coach,
            session_id=session_id,
            stage_name="CBCS-RESPONSE-DISPATCH",
            agent_name="Azaria",
            latency_ms=0,  # async, not measured
        )
        self._stage_receipts.append(receipt)
        self._log_stage(receipt)
        return receipt

    # ── Latency Queries ────────────────────────────────

    def total_pipeline_latency_ms(self) -> int:
        """Sum of all non-background stage latencies."""
        return sum(
            r.latency_ms for r in self._stage_receipts
            if r.stage_name != "CBCS-RESPONSE-DISPATCH"
        )

    def is_within_budget(self) -> bool:
        """FR27 AC1: sub-2s total."""
        return self.total_pipeline_latency_ms() < LATENCY_P95_BUDGET_MS

    @property
    def stage_receipts(self) -> list[LatencyReceipt]:
        return list(self._stage_receipts)

    @property
    def tier_map(self) -> ModelTierMap:
        return self._tier_map

    # ── Internals ──────────────────────────────────────

    def _log_stage(self, receipt: LatencyReceipt) -> None:
        self._receipt_chain.log(
            agent_id=receipt.agent_name,
            action=receipt.stage_name,
            asset_id=receipt.session_id,
            decision=receipt.crisis_check.value,
            decision_rationale=f"latency={receipt.latency_ms}ms, ghost={receipt.ghost_typing_triggered}",
        )
