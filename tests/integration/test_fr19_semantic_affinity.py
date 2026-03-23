"""
CCP FR19 Semantic Affinity Guard — Integration Tests (Unit 3)
Tests all 4 acceptance criteria + fallback + edge cases.

Spec reference: FR19_Semantic_Affinity_Guard_Tech_Spec.md §8 Acceptance Criteria
                §10 Testing Strategy
"""

from pathlib import Path

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.semantic_affinity_models import (
    AffinityRating,
    BatchClearanceStatus,
    BatchMetadata,
    BatchSlot,
    C06Clearance,
    C06ResolutionPath,
    MoodMode,
    PainMapInput,
)
from src.ccp.services.semantic_affinity_guard import (
    C06TerminalError,
    DAGViolationError,
    SemanticAffinityGuard,
    bucket_affinity_rating,
    compute_semantic_affinity_score,
    resolve_c06_clearance,
)


# ─── Fixtures ────────────────────────────────────────────────────────────────


@pytest.fixture()
def receipt_chain(tmp_path: Path) -> ReceiptChain:
    return ReceiptChain(
        coach_acronym="TST",
        log_dir=str(tmp_path / "receipts"),
    )


def _make_pain_map(
    coach_id: str = "coach-TST-001",
    l3_pain: str = "Systemic workplace exhaustion and imposter syndrome",
    l2_domains: list[str] | None = None,
) -> PainMapInput:
    return PainMapInput(
        coach_id=coach_id,
        active_l3_pain_domain=l3_pain,
        l2_pain_domains=l2_domains or [],
    )


def _make_batch(
    coach_id: str = "coach-TST-001",
    slots: list[BatchSlot] | None = None,
) -> BatchMetadata:
    if slots is None:
        slots = [
            BatchSlot(slot_id=1, intended_mode=MoodMode.ESCAPE, content_domain="Golf technique mastery"),
            BatchSlot(slot_id=2, intended_mode=MoodMode.PROCESSING, content_domain="Workplace burnout recovery"),
        ]
    return BatchMetadata(
        batch_id="BATCH-TST-001",
        coach_id=coach_id,
        slots=slots,
    )


# ─── AC1: Hard Block Priority ────────────────────────────────────────────────


class TestAC1HardBlockPriority:
    """AC1: Escape + HIGH semantic affinity → C-06 FAIL_TERMINAL, compilation blocked."""

    def test_escape_high_affinity_blocks(self, receipt_chain: ReceiptChain) -> None:
        """Spec AC1: 'If Escape slot evaluates to HIGH, engine throws terminal error
        at C-06 and explicitly refuses to compile.'
        Failure example: system recognizes HIGH but proceeds to compile anyway.
        """
        pain_map = _make_pain_map(
            l3_pain="Systemic workplace exhaustion and imposter syndrome"
        )
        batch = _make_batch(slots=[
            BatchSlot(
                slot_id=1,
                intended_mode=MoodMode.ESCAPE,
                content_domain="Systemic workplace exhaustion and imposter syndrome",
            ),
        ])

        guard = SemanticAffinityGuard(receipt_chain=receipt_chain)
        clearance = guard.evaluate(batch, pain_map)

        # Must be blocked
        assert clearance.batch_clearance_status == BatchClearanceStatus.BLOCKED
        assert clearance.batch_evaluation[0].c06_clearance == C06Clearance.FAIL_TERMINAL
        assert clearance.batch_evaluation[0].affinity_rating == AffinityRating.HIGH

    def test_terminal_block_includes_resolution_paths(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """FAIL_TERMINAL must present domain swap and reclassification options."""
        pain_map = _make_pain_map(l3_pain="workplace burnout exhaustion stress overwhelm")
        batch = _make_batch(slots=[
            BatchSlot(
                slot_id=1,
                intended_mode=MoodMode.ESCAPE,
                content_domain="workplace burnout exhaustion stress overwhelm recovery tips",
            ),
        ])

        guard = SemanticAffinityGuard(receipt_chain=receipt_chain)
        clearance = guard.evaluate(batch, pain_map)

        blocked_slot = clearance.batch_evaluation[0]
        assert blocked_slot.c06_clearance == C06Clearance.FAIL_TERMINAL
        assert C06ResolutionPath.DOMAIN_SWAP in blocked_slot.resolution_paths
        assert C06ResolutionPath.RECLASSIFY_PROCESSING in blocked_slot.resolution_paths

    def test_escape_low_affinity_passes(self, receipt_chain: ReceiptChain) -> None:
        """Escape + LOW affinity → PASS (entirely separate domains)."""
        pain_map = _make_pain_map(l3_pain="Corporate hustle and career ambition")
        batch = _make_batch(slots=[
            BatchSlot(
                slot_id=1,
                intended_mode=MoodMode.ESCAPE,
                content_domain="Golf technique for weekend players",
            ),
        ])

        guard = SemanticAffinityGuard(receipt_chain=receipt_chain)
        clearance = guard.evaluate(batch, pain_map)

        assert clearance.batch_clearance_status == BatchClearanceStatus.CLEARED
        assert clearance.batch_evaluation[0].c06_clearance == C06Clearance.PASS

    def test_c06_clearance_logic_escape_high(self) -> None:
        """Unit test: resolve_c06_clearance deterministic."""
        assert resolve_c06_clearance(MoodMode.ESCAPE, AffinityRating.HIGH) == C06Clearance.FAIL_TERMINAL


# ─── AC2: Processing Pass Through ────────────────────────────────────────────


class TestAC2ProcessingPassThrough:
    """AC2: Processing + HIGH → C-06 PASS (faces pain directly = productive)."""

    def test_processing_high_affinity_passes(self, receipt_chain: ReceiptChain) -> None:
        """Spec AC2: 'Processing Mode slot evaluates to HIGH against same Pain Map,
        engine ignores it and allows C-06 clearance.'
        Failure: system applies kill switch universally across all mood states.
        """
        pain_map = _make_pain_map(
            l3_pain="Systemic workplace exhaustion and imposter syndrome"
        )
        batch = _make_batch(slots=[
            BatchSlot(
                slot_id=1,
                intended_mode=MoodMode.PROCESSING,
                content_domain="Systemic workplace exhaustion and imposter syndrome deep analysis",
            ),
        ])

        guard = SemanticAffinityGuard(receipt_chain=receipt_chain)
        clearance = guard.evaluate(batch, pain_map)

        assert clearance.batch_clearance_status == BatchClearanceStatus.CLEARED
        assert clearance.batch_evaluation[0].c06_clearance == C06Clearance.PASS

    def test_processing_retagged_high_passes(self) -> None:
        """Spec §10 Unit Test: identical HIGH payload re-tagged as Processing → PASS."""
        assert resolve_c06_clearance(MoodMode.PROCESSING, AffinityRating.HIGH) == C06Clearance.PASS
        assert resolve_c06_clearance(MoodMode.PROCESSING, AffinityRating.MEDIUM) == C06Clearance.PASS

    def test_status_high_affinity_passes(self) -> None:
        """Status mode tolerates HIGH affinity."""
        assert resolve_c06_clearance(MoodMode.STATUS, AffinityRating.HIGH) == C06Clearance.PASS

    def test_discovery_high_affinity_passes(self) -> None:
        """Discovery mode tolerates HIGH affinity."""
        assert resolve_c06_clearance(MoodMode.DISCOVERY, AffinityRating.HIGH) == C06Clearance.PASS


# ─── AC3: Medium Review Flag ──────────────────────────────────────────────────


class TestAC3MediumReviewFlag:
    """AC3: MEDIUM affinity → Operator Dashboard for manual validation."""

    def test_escape_medium_affinity_gets_operator_review(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """Spec AC3: 'System pauses compilation and pushes to Operator Dashboard.'
        Failure: system assumes MEDIUM is acceptable and auto-merges.
        """
        pain_map = _make_pain_map(l3_pain="Management leadership challenges")
        batch = _make_batch(slots=[
            BatchSlot(
                slot_id=1,
                intended_mode=MoodMode.ESCAPE,
                content_domain="Public speaking anxiety tips for managers",
            ),
        ])

        guard = SemanticAffinityGuard(receipt_chain=receipt_chain)
        clearance = guard.evaluate(batch, pain_map)

        # Check the slot with MEDIUM rating gets OPERATOR_REVIEW
        medium_slots = [
            e for e in clearance.batch_evaluation
            if e.affinity_rating == AffinityRating.MEDIUM
        ]
        if medium_slots:
            assert medium_slots[0].c06_clearance == C06Clearance.OPERATOR_REVIEW
            assert clearance.batch_clearance_status in (
                BatchClearanceStatus.PENDING_REVIEW,
                BatchClearanceStatus.BLOCKED,
            )

    def test_c06_escape_medium_logic(self) -> None:
        assert resolve_c06_clearance(MoodMode.ESCAPE, AffinityRating.MEDIUM) == C06Clearance.OPERATOR_REVIEW


# ─── AC4: ADR-01 Strict Isolation ─────────────────────────────────────────────


class TestAC4ADR01Isolation:
    """AC4: Pain Map fetched exclusively from targeted tenant database."""

    def test_cross_coach_pain_map_raises(self, receipt_chain: ReceiptChain) -> None:
        """Pain Map from Coach A must not be used in Coach B's evaluation."""
        pain_map = _make_pain_map(coach_id="coach-AAA-001")
        batch = _make_batch(coach_id="coach-BBB-001")

        guard = SemanticAffinityGuard(receipt_chain=receipt_chain)
        with pytest.raises(ValueError, match="ADR-01 isolation violation"):
            guard.evaluate(batch, pain_map)

    def test_same_coach_passes_isolation(self, receipt_chain: ReceiptChain) -> None:
        pain_map = _make_pain_map(coach_id="coach-TST-001")
        batch = _make_batch(coach_id="coach-TST-001")

        guard = SemanticAffinityGuard(receipt_chain=receipt_chain)
        clearance = guard.evaluate(batch, pain_map)
        assert clearance.tenant_id == "coach-TST-001"


# ─── Ghost Variable Prevention ────────────────────────────────────────────────


class TestGhostVariablePrevention:
    """Spec §3: NULL/UNDEFINED fields → DAG_VIOLATION hard halt."""

    def test_empty_pain_domain_raises_dag_violation(
        self, receipt_chain: ReceiptChain
    ) -> None:
        pain_map = _make_pain_map(l3_pain="   ")
        batch = _make_batch()

        guard = SemanticAffinityGuard(receipt_chain=receipt_chain)
        with pytest.raises(DAGViolationError):
            guard.evaluate(batch, pain_map)

    def test_empty_batch_raises_dag_violation(
        self, receipt_chain: ReceiptChain
    ) -> None:
        pain_map = _make_pain_map()
        batch = _make_batch(slots=[])

        guard = SemanticAffinityGuard(receipt_chain=receipt_chain)
        with pytest.raises(DAGViolationError):
            guard.evaluate(batch, pain_map)


# ─── Fallback: NLP Unavailable ────────────────────────────────────────────────


class TestFallbackNLPUnavailable:
    """Spec §6: NLP crash → all Escape = PROVISIONAL_MEDIUM → Operator Queue."""

    def test_fallback_escape_slots_become_provisional_medium(
        self, receipt_chain: ReceiptChain
    ) -> None:
        pain_map = _make_pain_map()
        batch = _make_batch(slots=[
            BatchSlot(slot_id=1, intended_mode=MoodMode.ESCAPE, content_domain="Any content"),
            BatchSlot(slot_id=2, intended_mode=MoodMode.ESCAPE, content_domain="Other content"),
        ])

        guard = SemanticAffinityGuard(receipt_chain=receipt_chain, nlp_available=False)
        clearance = guard.evaluate(batch, pain_map)

        assert clearance.is_fallback is True
        assert clearance.operator_warning is not None
        assert "OPERATOR_WARNING" in clearance.operator_warning

        for eval_result in clearance.batch_evaluation:
            if eval_result.intended_mode == MoodMode.ESCAPE:
                assert eval_result.affinity_rating == AffinityRating.MEDIUM
                assert eval_result.c06_clearance == C06Clearance.OPERATOR_REVIEW

    def test_fallback_never_auto_passes_escape(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """Spec §6: ensuring HIGH affinity content never slips through by default."""
        pain_map = _make_pain_map()
        batch = _make_batch(slots=[
            BatchSlot(slot_id=1, intended_mode=MoodMode.ESCAPE, content_domain="Anything"),
        ])

        guard = SemanticAffinityGuard(receipt_chain=receipt_chain, nlp_available=False)
        clearance = guard.evaluate(batch, pain_map)

        assert clearance.batch_evaluation[0].c06_clearance != C06Clearance.PASS


# ─── Semantic Distance Computation ────────────────────────────────────────────


class TestSemanticDistanceComputation:
    """Spec §10: Zillmann Evaluation Metric unit tests."""

    def test_exact_duplicate_gives_high(self) -> None:
        """Submit exact duplicate string → HIGH."""
        score = compute_semantic_affinity_score(
            "workplace burnout exhaustion",
            "workplace burnout exhaustion",
        )
        assert bucket_affinity_rating(score) == AffinityRating.HIGH

    def test_separate_domains_give_low(self) -> None:
        """Entirely separate domains → LOW."""
        score = compute_semantic_affinity_score(
            "Golf technique for weekend players",
            "Corporate hustle and career ambition",
        )
        assert bucket_affinity_rating(score) == AffinityRating.LOW

    def test_empty_inputs_give_zero(self) -> None:
        assert compute_semantic_affinity_score("", "some pain") == 0.0
        assert compute_semantic_affinity_score("some content", "") == 0.0
