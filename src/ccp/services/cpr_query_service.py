"""
CCP FR44 — Context Performance Registry Query Service (DEP-ENG-045)

Spec: FR44_Context_Performance_Registry_Tech_Spec.md
Extends: DEP-ENG-045 ContextPerformanceRegistry (already in v5_models.py)
         + context_reasoning_layer.py (load_performance_registry, query methods)

§4 Stage 1: Registry Init (coach_id-scoped, loads from Supabase)
§4 Stage 2: Context Selection with Rationale (AC1: rationale non-empty)
§4 Stage 3: Performance Handshake (engagement × 1.2 baseline rule)
§4 Stage 4: Rule Refinement (N≥50 outperforming rows → override eligible)

§8 AC1: ContextSelectionObject.selection_rationale must be non-empty
§8 AC2: N<5 → confidence_score=0.2 (sparse data fallback)
§8 AC3: engagement_rate > 1.2× coach_baseline → outperformed_default=True
§8 AC4: N≥50 outperforming same context params → override_eligible=True

NOTE: Does NOT re-implement ContextPerformanceRegistry model (v5_models.py)
      or context_reasoning_layer.py confidence methods.
"""

from __future__ import annotations

from typing import Optional, Any
from uuid import uuid4

from src.ccp.models.onboarding_prerequisite_models import (
    CPR_OUTPERFORM_MULTIPLIER,
    CPR_RULE_OVERRIDE_THRESHOLD,
    CPR_SPARSE_THRESHOLD,
    ContextCombination,
    ContextSelectionObject,
    CPRQueryResult,
    PerformanceHandshakeResult,
)
from src.ccp.core.receipt_chain import ReceiptChain


# ══════════════════════════════════════════════════════════════════════════════
# Stage 1: Registry Initialiser (ADR-01)
# ══════════════════════════════════════════════════════════════════════════════

class CPRRegistryInitialiser:
    """FR44 §4 Stage 1: Load the per-coach ContextPerformanceRegistry.

    ADR-01: Each coach has their own scoped registry. No cross-coach reads.
    Delegates actual loading to context_reasoning_layer.load_performance_registry().
    """

    def __init__(self, supabase_client: Any = None) -> None:
        self._client = supabase_client

    def load(self, coach_id: str) -> dict[str, Any]:
        """Load registry rows for coach_id. Returns dict keyed by moment_id.

        Production: SELECT * FROM context_performance_registry WHERE coach_id=?
        Dev: returns empty dict (registry will be sparse → AC2 fallback).
        """
        if self._client is None:
            return {}
        try:
            result = (
                self._client.table("context_performance_registry")
                .select("*")
                .eq("coach_id", coach_id)
                .execute()
            )
            rows = result.data or []
            return {row["moment_id"]: row for row in rows}
        except Exception:
            return {}


# ══════════════════════════════════════════════════════════════════════════════
# Stage 2: Context Selection with Rationale
# ══════════════════════════════════════════════════════════════════════════════

class ContextSelectionEngine:
    """FR44 §4 Stage 2: Query registry for matching context; enforce AC1/AC2.

    AC1: selection_rationale must be non-empty (enforced by model validator).
    AC2: N<5 matching rows → confidence_score=0.2 (sparse data mode).
    """

    def query(
        self,
        registry_rows: dict[str, Any],
        moment_id: str,
        regulatory_frame: str,
        selection_rationale: str,
        context_combination: Optional[ContextCombination] = None,
    ) -> CPRQueryResult:
        """Return CPRQueryResult for the given moment × regulatory frame.

        Matches on moment_id AND regulatory_frame. Counts outperforming rows
        (outperformed_default=True). Confidence computed by model validator.
        """
        # Filter matching rows
        matched: list[dict[str, Any]] = [
            row
            for row in registry_rows.values()
            if row.get("moment_id") == moment_id
            and row.get("regulatory_frame") == regulatory_frame
        ]
        outperforming: list[dict[str, Any]] = [
            row for row in matched if row.get("outperformed_default") is True
        ]

        # Build ContextSelectionObject — model validator enforces non-empty rationale
        selection_object = ContextSelectionObject(
            moment_id=moment_id,
            regulatory_frame=regulatory_frame,
            selection_rationale=selection_rationale,
            context_combination=context_combination
            or ContextCombination(
                context_labels=[moment_id],
                regulatory_frame=regulatory_frame,
            ),
        )

        return CPRQueryResult(
            query_id=str(uuid4()),
            moment_id=moment_id,
            regulatory_frame=regulatory_frame,
            selection_object=selection_object,
            matched_sessions=len(matched),
            outperforming_sessions=len(outperforming),
            # confidence_score computed by model validator in CPRQueryResult
        )

    def write_selection_object(
        self,
        selection_object: ContextSelectionObject,
        coach_id: str,
        supabase_client: Any = None,
    ) -> bool:
        """Persist a ContextSelectionObject to the registry. Return True on success."""
        if supabase_client is None:
            return True  # Dev simulation: always succeeds
        try:
            supabase_client.table("context_performance_registry").upsert(
                {
                    "coach_id": coach_id,
                    "moment_id": selection_object.moment_id,
                    "regulatory_frame": selection_object.regulatory_frame,
                    "selection_rationale": selection_object.selection_rationale,
                    "context_labels": selection_object.context_combination.context_labels
                    if selection_object.context_combination
                    else [],
                }
            ).execute()
            return True
        except Exception:
            return False


# ══════════════════════════════════════════════════════════════════════════════
# Stage 3: Performance Handshake
# ══════════════════════════════════════════════════════════════════════════════

class PerformanceHandshakeExecutor:
    """FR44 §4 Stage 3: Update registry with engagement outcome.

    AC3: engagement_rate > CPR_OUTPERFORM_MULTIPLIER × coach_baseline
         → outperformed_default=True.
    """

    def apply(
        self,
        universal_asset_id: str,
        moment_id: str,
        regulatory_frame: str,
        engagement_rate: float,
        saves: int,
        shares: int,
        coach_baseline_engagement: float,
        supabase_client: Any = None,
    ) -> PerformanceHandshakeResult:
        """Compute outperformance and persist to registry.

        Returns PerformanceHandshakeResult; outperformed_default determined by
        the model's determine_outperformance validator (1.2× rule).
        """
        handshake = PerformanceHandshakeResult(
            universal_asset_id=universal_asset_id,
            moment_id=moment_id,
            regulatory_frame=regulatory_frame,
            engagement_rate=engagement_rate,
            saves=saves,
            shares=shares,
            coach_baseline_engagement=coach_baseline_engagement,
            # outperformed_default computed by model validator
        )

        # Persist the result
        if supabase_client is not None:
            try:
                supabase_client.table("context_performance_registry").upsert(
                    {
                        "universal_asset_id": universal_asset_id,
                        "moment_id": moment_id,
                        "regulatory_frame": regulatory_frame,
                        "engagement_rate": engagement_rate,
                        "saves": saves,
                        "shares": shares,
                        "outperformed_default": handshake.outperformed_default,
                    }
                ).execute()
            except Exception:
                pass  # Non-fatal; result already computed

        return handshake


# ══════════════════════════════════════════════════════════════════════════════
# Stage 4: Rule Refinement Eligibility
# ══════════════════════════════════════════════════════════════════════════════

class RuleRefinementEligibilityChecker:
    """FR44 §4 Stage 4: Determine if context params have enough outperforming data.

    AC4: N ≥ CPR_RULE_OVERRIDE_THRESHOLD (50) outperforming rows for the same
    moment_id × regulatory_frame → override_eligible=True.
    """

    THRESHOLD = CPR_RULE_OVERRIDE_THRESHOLD

    def check(
        self,
        registry_rows: dict[str, Any],
        moment_id: str,
        regulatory_frame: str,
    ) -> bool:
        """Return True if ≥50 rows with outperformed_default=True exist."""
        count = sum(
            1
            for row in registry_rows.values()
            if row.get("moment_id") == moment_id
            and row.get("regulatory_frame") == regulatory_frame
            and row.get("outperformed_default") is True
        )
        return count >= self.THRESHOLD


# ══════════════════════════════════════════════════════════════════════════════
# Full CPR Query Service
# ══════════════════════════════════════════════════════════════════════════════

class CPRQueryService:
    """FR44 full 4-stage orchestrator.

    Usage:
        svc = CPRQueryService(coach_id="EMI", supabase_client=client)
        result = svc.query_registry("MOMENT-001", "autonomy", "Coach chose this")
        handshake = svc.apply_performance_handshake(
            universal_asset_id="ASSET-001",
            moment_id="MOMENT-001",
            regulatory_frame="autonomy",
            engagement_rate=0.05,
            saves=12,
            shares=3,
            coach_baseline_engagement=0.04,
        )
        eligible = svc.check_override_eligible("MOMENT-001", "autonomy")
    """

    def __init__(
        self,
        coach_id: str,
        supabase_client: Any = None,
        receipt_chain: Optional[ReceiptChain] = None,
    ) -> None:
        if len(coach_id) != 3:
            raise ValueError("coach_id must be 3 characters (ADR-01).")
        self.coach_id = coach_id
        self._supabase = supabase_client
        self.receipt_chain = receipt_chain or ReceiptChain(
            coach_acronym=coach_id
        )
        self._initialiser = CPRRegistryInitialiser(supabase_client)
        self._selector = ContextSelectionEngine()
        self._handshake = PerformanceHandshakeExecutor()
        self._rule_checker = RuleRefinementEligibilityChecker()

        # Stage 1: Load registry on init
        self._registry: dict[str, Any] = {}
        self._load_registry()

    def _load_registry(self) -> None:
        """Stage 1: Load per-coach registry rows."""
        self._registry = self._initialiser.load(self.coach_id)
        self.receipt_chain.log(
            agent_id="Atlas",
            action="registry_init",
            input_summary=f"coach_id={self.coach_id}",
            output_summary=f"rows_loaded={len(self._registry)}",
            metadata={"stage_name": "REGISTRY-INIT"},
        )

    def refresh_registry(self) -> None:
        """Reload registry (e.g., after handshake writes)."""
        self._load_registry()

    # ── Stage 2 ───────────────────────────────────────────────────────────────

    def query_registry(
        self,
        moment_id: str,
        regulatory_frame: str,
        selection_rationale: str,
        context_combination: Optional[ContextCombination] = None,
    ) -> CPRQueryResult:
        """Stage 2: Query registry for best matching context.

        AC1: selection_rationale non-empty → enforced by ContextSelectionObject.
        AC2: N<5 → confidence_score=0.2 (sparse data mode).
        """
        result = self._selector.query(
            registry_rows=self._registry,
            moment_id=moment_id,
            regulatory_frame=regulatory_frame,
            selection_rationale=selection_rationale,
            context_combination=context_combination,
        )

        self.receipt_chain.log(
            agent_id="Atlas",
            action="context_selection_query",
            input_summary=(
                f"moment={moment_id} frame={regulatory_frame} "
                f"rationale_len={len(selection_rationale)}"
            ),
            output_summary=(
                f"matched={result.matched_sessions} "
                f"confidence={result.confidence_score} "
                f"sparse_mode={result.is_sparse_data}"
            ),
            metadata={"stage_name": "CONTEXT-SELECTION"},
        )
        return result

    def write_selection(
        self,
        selection_object: ContextSelectionObject,
    ) -> bool:
        """Persist a ContextSelectionObject to the registry."""
        success = self._selector.write_selection_object(
            selection_object=selection_object,
            coach_id=self.coach_id,
            supabase_client=self._supabase,
        )
        return success

    # ── Stage 3 ───────────────────────────────────────────────────────────────

    def apply_performance_handshake(
        self,
        universal_asset_id: str,
        moment_id: str,
        regulatory_frame: str,
        engagement_rate: float,
        saves: int = 0,
        shares: int = 0,
        coach_baseline_engagement: float = 0.03,
    ) -> PerformanceHandshakeResult:
        """Stage 3: Record engagement outcome and compute outperformance.

        AC3: engagement_rate > 1.2 × coach_baseline → outperformed_default=True.
        """
        handshake = self._handshake.apply(
            universal_asset_id=universal_asset_id,
            moment_id=moment_id,
            regulatory_frame=regulatory_frame,
            engagement_rate=engagement_rate,
            saves=saves,
            shares=shares,
            coach_baseline_engagement=coach_baseline_engagement,
            supabase_client=self._supabase,
        )

        self.receipt_chain.log(
            agent_id="Atlas",
            action="performance_handshake",
            input_summary=(
                f"asset={universal_asset_id} engagement={engagement_rate} "
                f"baseline={coach_baseline_engagement}"
            ),
            output_summary=(
                f"outperformed={handshake.outperformed_default} "
                f"multiplier_applied={CPR_OUTPERFORM_MULTIPLIER}"
            ),
            metadata={"stage_name": "PERFORMANCE-HANDSHAKE"},
        )
        return handshake

    # ── Stage 4 ───────────────────────────────────────────────────────────────

    def check_override_eligible(
        self,
        moment_id: str,
        regulatory_frame: str,
    ) -> bool:
        """Stage 4: AC4 — return True if ≥50 outperforming rows exist."""
        # Refresh before checking in case new handshakes were written
        self.refresh_registry()

        eligible = self._rule_checker.check(
            registry_rows=self._registry,
            moment_id=moment_id,
            regulatory_frame=regulatory_frame,
        )

        self.receipt_chain.log(
            agent_id="Atlas",
            action="rule_refinement_eligibility_check",
            input_summary=f"moment={moment_id} frame={regulatory_frame}",
            output_summary=f"override_eligible={eligible} threshold={CPR_RULE_OVERRIDE_THRESHOLD}",
            metadata={"stage_name": "RULE-REFINEMENT"},
        )
        return eligible

    def compute_confidence(
        self,
        matched_sessions: int,
        outperforming_sessions: int = 0,
    ) -> float:
        """AC2/AC3 confidence helper (delegates to model logic for consistency).

        Returns 0.2 if matched_sessions < 5; else 0.8 if any outperforming.
        """
        if matched_sessions < CPR_SPARSE_THRESHOLD:
            return 0.2
        if outperforming_sessions > 0:
            return 0.8
        return 0.5
