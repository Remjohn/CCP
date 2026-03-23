"""
CCP FR20 — Audience Maturity Pipeline Orchestrator

End-to-end pipeline:
  Stage 1 → COHORT-CLASSIFICATION
  Stage 2 → PROFILE-RESOLUTION
  Stage 3 → ADAPTER-COMPILATION-INJECTION

All three receipt writes are handled by the underlying engine and adapter.
The pipeline adds a top-level orchestration receipt for traceability.

Spec reference: FR20_Audience_Maturity_Lifecycle_Tech_Spec.md §4
"""

from __future__ import annotations

from dataclasses import dataclass

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.audience_maturity_models import (
    AudienceMaturityProfile,
    EngagementSignals,
)
from src.ccp.services.audience_maturity_adapter import AudienceMaturityAdapter
from src.ccp.services.audience_maturity_engine import AudienceMaturityEngine


# ─── Constants ────────────────────────────────────────────────────────────────

AGENT_PIPELINE = "Audience-Maturity-Pipeline"
STAGE_ORCHESTRATE = "AM-PIPELINE-ORCHESTRATE"


# ─── Pipeline Result ─────────────────────────────────────────────────────────


@dataclass(frozen=True)
class AudienceMaturityPipelineResult:
    """Complete result from the audience maturity pipeline run."""
    profile: AudienceMaturityProfile
    block_b_constraints: str
    constraint_list: list[str]


# ─── Pipeline ─────────────────────────────────────────────────────────────────


class AudienceMaturityPipeline:
    """Orchestrates the full FR20 lifecycle: classify → resolve → adapt.

    ADR-01 enforced: coach_id in EngagementSignals scopes all operations.
    Receipt Chain Guard writes at each stage (delegated to engine + adapter).
    """

    def __init__(self, receipt_chain: ReceiptChain) -> None:
        self._rc = receipt_chain
        self._engine = AudienceMaturityEngine(receipt_chain)
        self._adapter = AudienceMaturityAdapter(receipt_chain)

    def run(self, signals: EngagementSignals) -> AudienceMaturityPipelineResult:
        """Execute the full audience maturity pipeline.

        Args:
            signals: DEP-ENG-042 engagement signal feed.

        Returns:
            AudienceMaturityPipelineResult with profile, constraint strings,
            and formatted Block B section.
        """
        # Stages 1 + 2 — classification + matrix expansion (with receipt writes)
        profile = self._engine.evaluate(signals)

        # Stage 3 — Adapter 8 compilation injection (with receipt write)
        constraint_list = self._adapter.compile_constraints(profile)
        block_b = self._adapter.format_block_b_section(profile)

        # Top-level orchestration receipt
        self._rc.log(
            agent_id=AGENT_PIPELINE,
            action=STAGE_ORCHESTRATE,
            input_summary=f"coach={signals.coach_id} age_wk={signals.account_age_weeks}",
            output_summary=(
                f"profile_id={profile.profile_id} "
                f"cohort={profile.cohort_classification.value} "
                f"method={profile.classification_method.value} "
                f"constraints={len(constraint_list)}"
            ),
            metadata={
                "profile_id": profile.profile_id,
                "tenant_id": profile.tenant_id,
                "cohort": profile.cohort_classification.value,
                "method": profile.classification_method.value,
            },
        )

        return AudienceMaturityPipelineResult(
            profile=profile,
            block_b_constraints=block_b,
            constraint_list=constraint_list,
        )
