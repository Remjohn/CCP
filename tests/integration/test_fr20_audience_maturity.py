"""
CCP FR20 Audience Maturity Lifecycle — Integration Tests (Unit 5)
Tests all 4 acceptance criteria + fallback + edge cases.

Spec reference: FR20_Audience_Maturity_Lifecycle_Tech_Spec.md §8 Acceptance Criteria
                §10 Testing Strategy
"""

from pathlib import Path

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.audience_maturity_models import (
    AudienceMaturityCohort,
    BatchAllocation,
    BroadenAndBuildStatus,
    ClassificationMethod,
    DepthPermission,
    EngagementSignals,
    TMTFunctionAllowed,
)
from src.ccp.services.audience_maturity_adapter import AudienceMaturityAdapter
from src.ccp.services.audience_maturity_engine import (
    AudienceMaturityEngine,
    classify_cohort,
    resolve_profile_fields,
)
from src.ccp.pipelines.audience_maturity_pipeline import AudienceMaturityPipeline


# ─── Fixtures ────────────────────────────────────────────────────────────────


@pytest.fixture()
def receipt_chain(tmp_path: Path) -> ReceiptChain:
    return ReceiptChain(
        coach_acronym="TST",
        log_dir=str(tmp_path / "receipts"),
    )


def _signals(
    coach_id: str = "coach-TST-001",
    save_to_share: float | None = None,
    dm_vuln: float | None = None,
    age_weeks: float = 1.0,
) -> EngagementSignals:
    return EngagementSignals(
        coach_id=coach_id,
        save_to_share_ratio=save_to_share,
        dm_vulnerability_ratio=dm_vuln,
        account_age_weeks=age_weeks,
    )


# ─── AC1: Behavioral Override Rule ───────────────────────────────────────────


class TestAC1BehavioralOverride:
    """AC1: Calendar says New, but behavioral depth says Loyal → Loyal wins."""

    def test_2_week_account_high_engagement_becomes_loyal(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """Spec AC1: 'Coach account age = 2 weeks, save_to_share_ratio = 2.5
        → cohort_classification = <Loyal>.'
        Failure: engine outputs <New> because calendar overrides behavioral spike.
        """
        signals = _signals(
            age_weeks=2.0,
            save_to_share=2.5,
            dm_vuln=0.20,
        )
        engine = AudienceMaturityEngine(receipt_chain)
        profile = engine.evaluate(signals)

        assert profile.cohort_classification == AudienceMaturityCohort.LOYAL
        assert profile.classification_method == ClassificationMethod.BEHAVIORAL_OVERRIDE

    def test_behavioral_developing_override(self) -> None:
        """save_to_share > 1.0 but < 2.0 → Developing override (1 week account)."""
        signals = _signals(age_weeks=1.0, save_to_share=1.5, dm_vuln=0.05)
        cohort, method = classify_cohort(signals)
        assert cohort == AudienceMaturityCohort.DEVELOPING
        assert method == ClassificationMethod.BEHAVIORAL_OVERRIDE

    def test_behavioral_loyal_requires_both_thresholds(self) -> None:
        """save_to_share > 2.0 but dm_vuln < 0.15 → NOT Loyal override (falls to Developing)."""
        signals = _signals(age_weeks=1.0, save_to_share=2.5, dm_vuln=0.10)
        cohort, method = classify_cohort(signals)
        # dm_vuln too low for Loyal but save_to_share > 1.0 → Developing
        assert cohort == AudienceMaturityCohort.DEVELOPING
        assert method == ClassificationMethod.BEHAVIORAL_OVERRIDE

    def test_calendar_loyal_for_old_low_engagement(self) -> None:
        """Spec §10 Priority Override Test: age=300wk, save_to_share=0.5 → calendar Loyal."""
        signals = _signals(age_weeks=300, save_to_share=0.5, dm_vuln=0.01)
        cohort, method = classify_cohort(signals)
        assert cohort == AudienceMaturityCohort.LOYAL
        assert method == ClassificationMethod.CALENDAR_FALLBACK

    def test_day_2_high_engagement_becomes_loyal(self) -> None:
        """Spec §10: age=2 days (0.29wk), save_to_share=2.1, dm_vuln=0.20 → Loyal."""
        signals = _signals(age_weeks=0.29, save_to_share=2.1, dm_vuln=0.20)
        cohort, method = classify_cohort(signals)
        assert cohort == AudienceMaturityCohort.LOYAL
        assert method == ClassificationMethod.BEHAVIORAL_OVERRIDE


# ─── AC2: TMT Isolation ──────────────────────────────────────────────────────


class TestAC2TMTIsolation:
    """AC2: Developing cohort must get insight_delivery_only."""

    def test_developing_gets_insight_delivery(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """Spec AC2: 'Given Developing, tmt_function_allowed = <insight_delivery_only>.'
        Failure: leaks <worldview_construction_permitted> into adapter.
        """
        signals = _signals(age_weeks=8.0, save_to_share=0.3, dm_vuln=0.02)
        engine = AudienceMaturityEngine(receipt_chain)
        profile = engine.evaluate(signals)

        assert profile.cohort_classification == AudienceMaturityCohort.DEVELOPING
        assert profile.tmt_function_allowed == TMTFunctionAllowed.INSIGHT_DELIVERY_ONLY

    def test_new_gets_insight_delivery(self) -> None:
        _, _, tmt, _ = resolve_profile_fields(AudienceMaturityCohort.NEW)
        assert tmt == TMTFunctionAllowed.INSIGHT_DELIVERY_ONLY

    def test_loyal_gets_worldview_construction(self) -> None:
        _, _, tmt, _ = resolve_profile_fields(AudienceMaturityCohort.LOYAL)
        assert tmt == TMTFunctionAllowed.WORLDVIEW_CONSTRUCTION_PERMITTED


# ─── AC3: Batch Allocation Math ──────────────────────────────────────────────


class TestAC3BatchAllocationMath:
    """AC3: Loyal → exact {P:50, E:20, D:15, S:15}."""

    def test_loyal_batch_allocation_exact(self, receipt_chain: ReceiptChain) -> None:
        """Spec AC3: 'Given <Loyal>, batch_allocation = Processing:50, Escape:20,
        Discovery:15, Status:15.'
        Failure: system modifies percentages randomly for 'variety'.
        """
        signals = _signals(age_weeks=20.0, save_to_share=0.3, dm_vuln=0.01)
        engine = AudienceMaturityEngine(receipt_chain)
        profile = engine.evaluate(signals)

        assert profile.cohort_classification == AudienceMaturityCohort.LOYAL
        assert profile.batch_allocation == BatchAllocation(
            processing=50, escape=20, discovery=15, status=15,
        )

    def test_new_batch_allocation_exact(self) -> None:
        alloc, _, _, _ = resolve_profile_fields(AudienceMaturityCohort.NEW)
        assert alloc == BatchAllocation(processing=10, escape=40, discovery=30, status=20)

    def test_developing_batch_allocation_exact(self) -> None:
        alloc, _, _, _ = resolve_profile_fields(AudienceMaturityCohort.DEVELOPING)
        assert alloc == BatchAllocation(processing=25, escape=35, discovery=20, status=20)

    def test_all_allocations_sum_to_100(self) -> None:
        for cohort in AudienceMaturityCohort:
            alloc, _, _, _ = resolve_profile_fields(cohort)
            total = alloc.processing + alloc.escape + alloc.discovery + alloc.status
            assert total == 100, f"{cohort.value} allocation sums to {total}"


# ─── AC4: ADR-01 Strict Isolation ─────────────────────────────────────────────


class TestAC4ADR01Isolation:
    """AC4: Tenant isolation — each coach scoped to own signals."""

    def test_different_coaches_get_different_profiles(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """Coach A (Loyal engagement) and Coach B (New) produce isolated profiles."""
        signals_a = _signals(coach_id="coach-AAA", age_weeks=2.0, save_to_share=2.5, dm_vuln=0.20)
        signals_b = _signals(coach_id="coach-BBB", age_weeks=1.0, save_to_share=0.1, dm_vuln=0.01)

        engine = AudienceMaturityEngine(receipt_chain)
        profile_a = engine.evaluate(signals_a)
        profile_b = engine.evaluate(signals_b)

        assert profile_a.tenant_id == "coach-AAA"
        assert profile_b.tenant_id == "coach-BBB"
        assert profile_a.cohort_classification == AudienceMaturityCohort.LOYAL
        assert profile_b.cohort_classification == AudienceMaturityCohort.NEW

    def test_tenant_id_propagated_to_profile(
        self, receipt_chain: ReceiptChain
    ) -> None:
        signals = _signals(coach_id="coach-XYZ-999", age_weeks=5.0)
        engine = AudienceMaturityEngine(receipt_chain)
        profile = engine.evaluate(signals)
        assert profile.tenant_id == "coach-XYZ-999"


# ─── Fallback: No Engagement Signals ──────────────────────────────────────────


class TestFallbackNoSignals:
    """Spec §6: No behavioral data → default New + CALENDAR_FALLBACK_DEFAULT."""

    def test_no_signals_defaults_to_new(self, receipt_chain: ReceiptChain) -> None:
        signals = _signals(age_weeks=1.0, save_to_share=None, dm_vuln=None)
        engine = AudienceMaturityEngine(receipt_chain)
        profile = engine.evaluate(signals)

        assert profile.cohort_classification == AudienceMaturityCohort.NEW
        assert profile.classification_method == ClassificationMethod.CALENDAR_FALLBACK_DEFAULT
        assert profile.tmt_function_allowed == TMTFunctionAllowed.INSIGHT_DELIVERY_ONLY

    def test_no_signals_old_account_uses_calendar(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """No behavioral data, but 20-week account → calendar Loyal."""
        signals = _signals(age_weeks=20.0, save_to_share=None, dm_vuln=None)
        engine = AudienceMaturityEngine(receipt_chain)
        profile = engine.evaluate(signals)

        assert profile.cohort_classification == AudienceMaturityCohort.LOYAL
        assert profile.classification_method == ClassificationMethod.CALENDAR_FALLBACK_DEFAULT


# ─── Matrix Consistency ──────────────────────────────────────────────────────


class TestMatrixConsistency:
    """Spec §10: Every cohort resolves all 5 fields without exception."""

    @pytest.mark.parametrize("cohort", list(AudienceMaturityCohort))
    def test_all_cohorts_resolve(self, cohort: AudienceMaturityCohort) -> None:
        alloc, depth, tmt, broaden = resolve_profile_fields(cohort)
        assert isinstance(alloc, BatchAllocation)
        assert isinstance(depth, DepthPermission)
        assert isinstance(tmt, TMTFunctionAllowed)
        assert isinstance(broaden, BroadenAndBuildStatus)

    def test_depth_permission_mapping(self) -> None:
        _, depth, _, _ = resolve_profile_fields(AudienceMaturityCohort.NEW)
        assert depth == DepthPermission.SURFACE
        _, depth, _, _ = resolve_profile_fields(AudienceMaturityCohort.DEVELOPING)
        assert depth == DepthPermission.MID
        _, depth, _, _ = resolve_profile_fields(AudienceMaturityCohort.LOYAL)
        assert depth == DepthPermission.FULL

    def test_broaden_and_build_mapping(self) -> None:
        _, _, _, bb = resolve_profile_fields(AudienceMaturityCohort.NEW)
        assert bb == BroadenAndBuildStatus.NOT_YET_SEEDED
        _, _, _, bb = resolve_profile_fields(AudienceMaturityCohort.DEVELOPING)
        assert bb == BroadenAndBuildStatus.ACTIVE
        _, _, _, bb = resolve_profile_fields(AudienceMaturityCohort.LOYAL)
        assert bb == BroadenAndBuildStatus.MATURE


# ─── Adapter 8 Injection ─────────────────────────────────────────────────────


class TestAdapter8Injection:
    """Spec §10 Integration: Adapter injects depth constraints into Block B."""

    def test_surface_constraint_present(self, receipt_chain: ReceiptChain) -> None:
        """Spec §10: Block B contains 'depth_permission is currently <Surface>'."""
        signals = _signals(age_weeks=1.0, save_to_share=None, dm_vuln=None)
        pipeline = AudienceMaturityPipeline(receipt_chain)
        result = pipeline.run(signals)

        assert "depth_permission is currently <Surface>" in result.block_b_constraints

    def test_loyal_worldview_constraint(self, receipt_chain: ReceiptChain) -> None:
        signals = _signals(age_weeks=20.0, save_to_share=3.0, dm_vuln=0.25)
        pipeline = AudienceMaturityPipeline(receipt_chain)
        result = pipeline.run(signals)

        assert "worldview_construction_permitted" in result.block_b_constraints
        assert "depth_permission is currently <Full>" in result.block_b_constraints

    def test_constraint_count(self, receipt_chain: ReceiptChain) -> None:
        """Adapter emits exactly 5 constraint strings."""
        signals = _signals(age_weeks=1.0)
        pipeline = AudienceMaturityPipeline(receipt_chain)
        result = pipeline.run(signals)

        assert len(result.constraint_list) == 5


# ─── Pipeline Integration ────────────────────────────────────────────────────


class TestPipelineIntegration:
    """Full pipeline end-to-end."""

    def test_full_pipeline_new_cohort(self, receipt_chain: ReceiptChain) -> None:
        signals = _signals(age_weeks=1.0)
        pipeline = AudienceMaturityPipeline(receipt_chain)
        result = pipeline.run(signals)

        p = result.profile
        assert p.cohort_classification == AudienceMaturityCohort.NEW
        assert p.batch_allocation.processing == 10
        assert p.batch_allocation.escape == 40
        assert p.depth_permission == DepthPermission.SURFACE
        assert p.tmt_function_allowed == TMTFunctionAllowed.INSIGHT_DELIVERY_ONLY
        assert p.broaden_and_build_status == BroadenAndBuildStatus.NOT_YET_SEEDED
        assert result.block_b_constraints.startswith("## Pre-Generation Constraints")

    def test_full_pipeline_loyal_override(self, receipt_chain: ReceiptChain) -> None:
        signals = _signals(age_weeks=2.0, save_to_share=2.5, dm_vuln=0.20)
        pipeline = AudienceMaturityPipeline(receipt_chain)
        result = pipeline.run(signals)

        p = result.profile
        assert p.cohort_classification == AudienceMaturityCohort.LOYAL
        assert p.classification_method == ClassificationMethod.BEHAVIORAL_OVERRIDE
        assert p.batch_allocation.processing == 50
        assert p.depth_permission == DepthPermission.FULL
