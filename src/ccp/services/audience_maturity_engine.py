"""
CCP FR20 — Audience Maturity Lifecycle Engine (DEP-ENG-017)

2-stage classifier + matrix expander:
  Stage 1 — Behavioral Cohort Classification (behavioral override → calendar fallback)
  Stage 2 — DEP-ENG-017 Profile Resolution (deterministic matrix expansion)

Academic grounding:
    Fredrickson & Joiner 2002 — Broaden-and-Build Theory
    Greenberg et al. 1986 / Burke 2010 — Terror Management Theory

Spec reference: FR20_Audience_Maturity_Lifecycle_Tech_Spec.md §4 Stages 1-2
"""

from __future__ import annotations

import time
import uuid

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.audience_maturity_models import (
    AudienceMaturityCohort,
    AudienceMaturityProfile,
    BatchAllocation,
    BroadenAndBuildStatus,
    ClassificationMethod,
    DepthPermission,
    EngagementSignals,
    TMTFunctionAllowed,
    BATCH_ALLOCATION_MATRIX,
    BROADEN_BUILD_MATRIX,
    DEPTH_PERMISSION_MATRIX,
    TMT_FUNCTION_MATRIX,
)


# ─── Constants ────────────────────────────────────────────────────────────────

AGENT_LIFECYCLE_ENGINE = "Maturity-Lifecycle-Engine"

STAGE_CLASSIFY = "COHORT-CLASSIFICATION"
STAGE_RESOLVE = "PROFILE-RESOLUTION"

# Behavioral thresholds — spec §4 Stage 1 Decision Logic
LOYAL_SAVE_TO_SHARE_MIN: float = 2.0
LOYAL_DM_VULN_MIN: float = 0.15
DEVELOPING_SAVE_TO_SHARE_MIN: float = 1.0

# Calendar thresholds — spec §4 Stage 1 fallback
LOYAL_WEEKS_MIN: float = 16.0
DEVELOPING_WEEKS_MIN: float = 4.0


# ─── Stage 1: Behavioral Cohort Classification ───────────────────────────────


def classify_cohort(
    signals: EngagementSignals,
) -> tuple[AudienceMaturityCohort, ClassificationMethod]:
    """Determine cohort from behavioral signals, falling back to calendar age.

    Spec §4 Stage 1 Decision Logic — behavioral checks FIRST:
      1. save_to_share > 2.0 AND dm_vulnerability > 0.15 → Loyal (override)
      2. save_to_share > 1.0 → Developing (override)
      3. account_age > 16wks → Loyal (calendar)
      4. account_age > 4wks → Developing (calendar)
      5. else → New

    Spec §6 Fallback: signals entirely missing → default New + CALENDAR_FALLBACK_DEFAULT.

    Returns:
        (cohort, classification_method)
    """
    has_behavioral = (
        signals.save_to_share_ratio is not None
        and signals.dm_vulnerability_ratio is not None
    )

    if has_behavioral:
        assert signals.save_to_share_ratio is not None
        assert signals.dm_vulnerability_ratio is not None

        # Behavioral override — spec §3 Technical Decision 1
        if (
            signals.save_to_share_ratio > LOYAL_SAVE_TO_SHARE_MIN
            and signals.dm_vulnerability_ratio > LOYAL_DM_VULN_MIN
        ):
            return AudienceMaturityCohort.LOYAL, ClassificationMethod.BEHAVIORAL_OVERRIDE

        if signals.save_to_share_ratio > DEVELOPING_SAVE_TO_SHARE_MIN:
            return AudienceMaturityCohort.DEVELOPING, ClassificationMethod.BEHAVIORAL_OVERRIDE

    # Calendar fallback — spec §4 Stage 1 else-if chain
    method = (
        ClassificationMethod.CALENDAR_FALLBACK
        if has_behavioral
        else ClassificationMethod.CALENDAR_FALLBACK_DEFAULT
    )

    if signals.account_age_weeks > LOYAL_WEEKS_MIN:
        return AudienceMaturityCohort.LOYAL, method

    if signals.account_age_weeks > DEVELOPING_WEEKS_MIN:
        return AudienceMaturityCohort.DEVELOPING, method

    return AudienceMaturityCohort.NEW, method


# ─── Stage 2: Matrix Expansion ───────────────────────────────────────────────


def resolve_profile_fields(
    cohort: AudienceMaturityCohort,
) -> tuple[BatchAllocation, DepthPermission, TMTFunctionAllowed, BroadenAndBuildStatus]:
    """Deterministic matrix lookup — spec §4 Stage 2.

    No LLM estimation permitted once cohort is resolved.

    Returns:
        (batch_allocation, depth_permission, tmt_function_allowed, broaden_and_build_status)
    """
    return (
        BATCH_ALLOCATION_MATRIX[cohort],
        DEPTH_PERMISSION_MATRIX[cohort],
        TMT_FUNCTION_MATRIX[cohort],
        BROADEN_BUILD_MATRIX[cohort],
    )


# ─── Orchestrated Engine ─────────────────────────────────────────────────────


class AudienceMaturityEngine:
    """2-stage Audience Maturity Lifecycle Engine.

    Stage 1: classify cohort from EngagementSignals
    Stage 2: expand cohort → full DEP-ENG-017 profile

    ADR-01 enforced via coach_id scoping on EngagementSignals.
    """

    def __init__(self, receipt_chain: ReceiptChain) -> None:
        self._rc = receipt_chain

    def evaluate(self, signals: EngagementSignals) -> AudienceMaturityProfile:
        """Run the full lifecycle evaluation pipeline.

        Args:
            signals: DEP-ENG-042 engagement signal feed (may have None fields for fallback).

        Returns:
            AudienceMaturityProfile (DEP-ENG-017)
        """
        # ── Stage 1: Cohort classification ──
        cohort, method = classify_cohort(signals)

        r1 = self._rc.log(
            agent_id=AGENT_LIFECYCLE_ENGINE,
            action=STAGE_CLASSIFY,
            input_summary=f"coach={signals.coach_id} age_wk={signals.account_age_weeks} "
                          f"sts={signals.save_to_share_ratio} dmv={signals.dm_vulnerability_ratio}",
            output_summary=f"cohort={cohort.value} method={method.value}",
            metadata={
                "stage_name": STAGE_CLASSIFY,
                "cohort": cohort.value,
                "method": method.value,
            },
        )

        # ── Stage 2: Matrix expansion ──
        batch_alloc, depth, tmt, broaden = resolve_profile_fields(cohort)

        r2 = self._rc.log(
            agent_id=AGENT_LIFECYCLE_ENGINE,
            action=STAGE_RESOLVE,
            parent_receipt_id=r1.receipt_id,
            input_summary=f"cohort={cohort.value}",
            output_summary=(
                f"batch={batch_alloc.model_dump()} depth={depth.value} "
                f"tmt={tmt.value} broaden={broaden.value}"
            ),
            metadata={
                "stage_name": STAGE_RESOLVE,
                "batch_allocation": batch_alloc.model_dump(),
                "depth_permission": depth.value,
                "tmt_function_allowed": tmt.value,
                "broaden_and_build_status": broaden.value,
            },
        )

        profile_id = f"AM-{int(time.time())}-{uuid.uuid4().hex[:6]}"

        return AudienceMaturityProfile(
            profile_id=profile_id,
            receipt_chain_hash=r2.receipt_id,
            tenant_id=signals.coach_id,
            last_evaluation_epoch=int(time.time()),
            cohort_classification=cohort,
            classification_method=method,
            batch_allocation=batch_alloc,
            depth_permission=depth,
            tmt_function_allowed=tmt,
            broaden_and_build_status=broaden,
        )
