"""
CCP FR18 Psychological Routing Brief Generator — Integration Tests (Unit 5)
Tests all 4 acceptance criteria + fallback + edge cases.

Spec reference: FR18_Psychological_Routing_Brief_Tech_Spec.md §8 Acceptance Criteria
                §10 Testing Strategy
"""

import re
from pathlib import Path
from typing import Any

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.psych_routing_models import (
    ArousalDirection,
    AudienceArousalLevel,
    AudienceMaturityCohort,
    AudienceMaturityProfile,
    AudienceValencePolarity,
    ComparisonType,
    MoodContextMap,
    MoodStatePrimary,
    NEUTRAL_PROCESSING_PROXY_STATE,
    RegulatoryFrame,
    RegulatoryOrientation,
    SDTNeedPrimary,
    SemanticAffinityRisk,
    SequencingDependency,
    TMTFunction,
    ValenceDelivery,
)
from src.ccp.pipelines.psych_routing_pipeline import PsychRoutingBriefGenerator
from src.ccp.services.payload_masking_library import (
    PAYLOAD_MASKING_INSTRUCTIONS,
    get_payload_masking_instruction,
)
from src.ccp.services.psych_routing_engine import PsychVariableMatrix


# ─── Fixtures ────────────────────────────────────────────────────────────────


@pytest.fixture()
def receipt_chain(tmp_path: Path) -> ReceiptChain:
    return ReceiptChain(
        coach_acronym="TST",
        log_dir=str(tmp_path / "receipts"),
    )


@pytest.fixture()
def matrix() -> PsychVariableMatrix:
    return PsychVariableMatrix()


def _make_mood_context(
    mood: MoodStatePrimary = MoodStatePrimary.ESCAPE,
    arousal: AudienceArousalLevel = AudienceArousalLevel.LOW,
    valence: AudienceValencePolarity = AudienceValencePolarity.POSITIVE,
    regulatory: RegulatoryOrientation = RegulatoryOrientation.GAIN_SEEKING,
    risk: SemanticAffinityRisk = SemanticAffinityRisk.LOW,
    coach_id: str = "coach-TST-001",
) -> MoodContextMap:
    return MoodContextMap(
        mood_state_primary=mood,
        audience_arousal_level=arousal,
        audience_valence_polarity=valence,
        regulatory_orientation=regulatory,
        semantic_affinity_risk=risk,
        coach_id=coach_id,
    )


def _make_maturity(
    cohort: AudienceMaturityCohort = AudienceMaturityCohort.NEW,
    coach_id: str = "coach-TST-001",
) -> AudienceMaturityProfile:
    return AudienceMaturityProfile(
        maturity_cohort=cohort,
        coach_id=coach_id,
    )


# ─── AC1: Zillmann Arousal Modulator ─────────────────────────────────────────


class TestAC1ZillmannArousalModulator:
    """AC1: HIGH Arousal / Negative → arousal_direction = 'lowers'."""

    def test_high_arousal_negative_maps_to_lowers(self, matrix: PsychVariableMatrix) -> None:
        """Spec AC1: 'Given a DEP-ENG-018 state of "HIGH Arousal / Negative (Stressed)",
        the script returns the arousal_direction enum <lowers>.'
        Failure example: system routes <raises> causing high-energy hype to burnt-out reader.
        """
        mood_ctx = _make_mood_context(
            mood=MoodStatePrimary.PROCESSING,
            arousal=AudienceArousalLevel.HIGH,
            valence=AudienceValencePolarity.NEGATIVE,
        )
        maturity = _make_maturity()
        result = matrix.resolve(mood_ctx, maturity)

        assert result.arousal_direction == ArousalDirection.LOWERS, (
            f"AC1 FAIL: HIGH/Negative should map to 'lowers', got '{result.arousal_direction.value}'"
        )

    def test_low_arousal_maps_to_raises(self, matrix: PsychVariableMatrix) -> None:
        mood_ctx = _make_mood_context(
            mood=MoodStatePrimary.STATUS,
            arousal=AudienceArousalLevel.LOW,
        )
        result = matrix.resolve(mood_ctx, _make_maturity())
        assert result.arousal_direction == ArousalDirection.RAISES

    def test_discovery_overrides_high_arousal_to_maintains(
        self, matrix: PsychVariableMatrix
    ) -> None:
        """Discovery mode overrides any arousal level → maintains."""
        mood_ctx = _make_mood_context(
            mood=MoodStatePrimary.DISCOVERY,
            arousal=AudienceArousalLevel.HIGH,
        )
        result = matrix.resolve(mood_ctx, _make_maturity())
        assert result.arousal_direction == ArousalDirection.MAINTAINS

    def test_neutral_arousal_maps_to_maintains(self, matrix: PsychVariableMatrix) -> None:
        mood_ctx = _make_mood_context(
            mood=MoodStatePrimary.ESCAPE,
            arousal=AudienceArousalLevel.NEUTRAL,
        )
        result = matrix.resolve(mood_ctx, _make_maturity())
        assert result.arousal_direction == ArousalDirection.MAINTAINS


# ─── AC2: TMT Cohort Guard ────────────────────────────────────────────────────


class TestAC2TMTCohortGuard:
    """AC2: Processing + New cohort → tmt_function = insight_delivery."""

    def test_processing_new_cohort_gives_insight_delivery(
        self, matrix: PsychVariableMatrix
    ) -> None:
        """Spec AC2: 'Given mood_state Processing and audience cohort New (0-4wk),
        system calculates tmt_function as <insight_delivery>.'
        Failure: worldview_construction pushed onto day-1 followers.
        """
        mood_ctx = _make_mood_context(mood=MoodStatePrimary.PROCESSING)
        maturity = _make_maturity(cohort=AudienceMaturityCohort.NEW)
        result = matrix.resolve(mood_ctx, maturity)

        assert result.tmt_function == TMTFunction.INSIGHT_DELIVERY, (
            f"AC2 FAIL: Processing + New cohort should give insight_delivery, "
            f"got '{result.tmt_function.value}'"
        )

    def test_processing_loyal_cohort_gives_worldview_construction(
        self, matrix: PsychVariableMatrix
    ) -> None:
        mood_ctx = _make_mood_context(mood=MoodStatePrimary.PROCESSING)
        maturity = _make_maturity(cohort=AudienceMaturityCohort.LOYAL)
        result = matrix.resolve(mood_ctx, maturity)
        assert result.tmt_function == TMTFunction.WORLDVIEW_CONSTRUCTION

    def test_processing_developing_cohort_gives_insight_delivery(
        self, matrix: PsychVariableMatrix
    ) -> None:
        mood_ctx = _make_mood_context(mood=MoodStatePrimary.PROCESSING)
        maturity = _make_maturity(cohort=AudienceMaturityCohort.DEVELOPING)
        result = matrix.resolve(mood_ctx, maturity)
        assert result.tmt_function == TMTFunction.INSIGHT_DELIVERY

    def test_non_processing_mood_gives_tmt_none(self, matrix: PsychVariableMatrix) -> None:
        for mood in [MoodStatePrimary.ESCAPE, MoodStatePrimary.DISCOVERY, MoodStatePrimary.STATUS]:
            mood_ctx = _make_mood_context(mood=mood)
            result = matrix.resolve(mood_ctx, _make_maturity(cohort=AudienceMaturityCohort.LOYAL))
            assert result.tmt_function == TMTFunction.NONE, (
                f"Non-processing mood {mood.value} should give tmt_function=none, "
                f"got {result.tmt_function.value}"
            )


# ─── AC3: SDT Validation ─────────────────────────────────────────────────────


class TestAC3SDTValidation:
    """AC3: Discovery mood → sdt_need_primary = competence."""

    def test_discovery_gives_competence(self, matrix: PsychVariableMatrix) -> None:
        """Spec AC3: 'Given mood_state Discovery, system unequivocally returns
        sdt_need_primary: <competence>.'
        Failure: returning <relatedness> forcing emotional connection piece when
        format requires competence-building observation.
        """
        mood_ctx = _make_mood_context(mood=MoodStatePrimary.DISCOVERY)
        result = matrix.resolve(mood_ctx, _make_maturity())

        assert result.sdt_need_primary == SDTNeedPrimary.COMPETENCE, (
            f"AC3 FAIL: Discovery should give competence, got '{result.sdt_need_primary.value}'"
        )

    def test_all_sdt_mappings(self, matrix: PsychVariableMatrix) -> None:
        """Verify 1:1 SDT binding for all 4 mood states."""
        expected = {
            MoodStatePrimary.ESCAPE: SDTNeedPrimary.RELIEF,
            MoodStatePrimary.DISCOVERY: SDTNeedPrimary.COMPETENCE,
            MoodStatePrimary.STATUS: SDTNeedPrimary.AUTONOMY,
            MoodStatePrimary.PROCESSING: SDTNeedPrimary.RELATEDNESS,
        }
        for mood, expected_sdt in expected.items():
            mood_ctx = _make_mood_context(mood=mood)
            result = matrix.resolve(mood_ctx, _make_maturity())
            assert result.sdt_need_primary == expected_sdt, (
                f"SDT mapping: {mood.value} → expected {expected_sdt.value}, "
                f"got {result.sdt_need_primary.value}"
            )


# ─── AC4: ADR-01 Strict Isolation ────────────────────────────────────────────


class TestAC4ADR01Isolation:
    """AC4: Engine reads DEP-ENG-017 exclusively from coach's private isolated storage."""

    def test_cross_coach_mood_context_raises(self, receipt_chain: ReceiptChain) -> None:
        """Coach A's MoodContextMap must not be used in Coach B's pipeline run."""
        coach_a_mood = _make_mood_context(coach_id="coach-AAA-001")
        maturity_b = _make_maturity(coach_id="coach-BBB-001")

        # Pipeline scoped to Coach B
        generator = PsychRoutingBriefGenerator(
            coach_id="coach-BBB-001",
            receipt_chain=receipt_chain,
        )

        # Coach A's mood context supplied to Coach B's pipeline → should raise
        with pytest.raises(ValueError, match="ADR-01 isolation violation"):
            generator.generate(
                mood_context=coach_a_mood,
                maturity_profile=maturity_b,
            )

    def test_cross_coach_maturity_profile_raises(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """Coach A's AudienceMaturityProfile must not be used in Coach B's pipeline."""
        mood_b = _make_mood_context(coach_id="coach-BBB-001")
        maturity_a = _make_maturity(coach_id="coach-AAA-001")

        generator = PsychRoutingBriefGenerator(
            coach_id="coach-BBB-001",
            receipt_chain=receipt_chain,
        )

        with pytest.raises(ValueError, match="ADR-01 isolation violation"):
            generator.generate(
                mood_context=mood_b,
                maturity_profile=maturity_a,
            )

    def test_matching_coach_id_passes_isolation(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """Same coach_id on all inputs → ADR-01 passes, brief generated."""
        mood = _make_mood_context(coach_id="coach-TST-001")
        maturity = _make_maturity(coach_id="coach-TST-001")

        generator = PsychRoutingBriefGenerator(
            coach_id="coach-TST-001",
            receipt_chain=receipt_chain,
        )
        brief = generator.generate(mood_context=mood, maturity_profile=maturity)

        assert brief.coach_id == "coach-TST-001"
        assert not brief.is_fallback


# ─── Fallback: Neutral Processing Proxy State ─────────────────────────────────


class TestFallbackNeutralProcessingProxyState:
    """Spec §6: DEP-ENG-018 unavailable → Neutral Processing Proxy State triggered."""

    def test_fallback_triggered_when_mood_context_none(
        self, receipt_chain: ReceiptChain
    ) -> None:
        generator = PsychRoutingBriefGenerator(
            coach_id="coach-TST-001",
            receipt_chain=receipt_chain,
        )
        brief = generator.generate(mood_context=None, maturity_profile=None)

        assert brief.is_fallback is True
        assert brief.operator_warning is not None
        assert "OPERATOR_WARNING" in brief.operator_warning

    def test_fallback_brief_is_valid_dep_eng_016(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """Fallback must still produce a fully valid DEP-ENG-016 object."""
        generator = PsychRoutingBriefGenerator(
            coach_id="coach-TST-001",
            receipt_chain=receipt_chain,
        )
        brief = generator.generate()

        assert brief.routing_id.startswith("PRB-")
        assert brief.psychological_classification is not None
        assert brief.payload_masking_instruction != ""
        assert brief.receipt_chain_hash != ""

    def test_fallback_uses_processing_mode(self, receipt_chain: ReceiptChain) -> None:
        """Spec §6: fallback state = Processing (Neutral Processing Proxy)."""
        generator = PsychRoutingBriefGenerator(
            coach_id="coach-TST-001",
            receipt_chain=receipt_chain,
        )
        brief = generator.generate()

        assert brief.psychological_classification.mood_state_primary == MoodStatePrimary.PROCESSING

    def test_fallback_regulatory_is_promotion(self, receipt_chain: ReceiptChain) -> None:
        """Spec §6: Regulatory = 'promotion' in fallback state."""
        generator = PsychRoutingBriefGenerator(
            coach_id="coach-TST-001",
            receipt_chain=receipt_chain,
        )
        brief = generator.generate()

        assert brief.psychological_classification.regulatory_frame == RegulatoryFrame.PROMOTION


# ─── Matrix Edge Cases ────────────────────────────────────────────────────────


class TestMatrixEdgeCases:
    """Spec §10 Unit Tests: 8 mock states spanning all edge cases."""

    def test_escape_low_arousal(self, matrix: PsychVariableMatrix) -> None:
        ctx = _make_mood_context(mood=MoodStatePrimary.ESCAPE, arousal=AudienceArousalLevel.LOW)
        result = matrix.resolve(ctx, _make_maturity())

        assert result.arousal_direction == ArousalDirection.RAISES
        assert result.valence_delivery == ValenceDelivery.POSITIVE
        assert result.sdt_need_primary == SDTNeedPrimary.RELIEF
        assert result.sequencing_dependency == SequencingDependency.INDEPENDENT
        assert result.comparison_type == ComparisonType.NONE
        assert result.tmt_function == TMTFunction.NONE

    def test_status_developing_cohort(self, matrix: PsychVariableMatrix) -> None:
        ctx = _make_mood_context(mood=MoodStatePrimary.STATUS)
        maturity = _make_maturity(cohort=AudienceMaturityCohort.DEVELOPING)
        result = matrix.resolve(ctx, maturity)

        assert result.sdt_need_primary == SDTNeedPrimary.AUTONOMY
        assert result.comparison_type == ComparisonType.WORLDVIEW_VALIDATION
        assert result.valence_delivery == ValenceDelivery.MIXED
        assert result.tmt_function == TMTFunction.NONE

    def test_status_new_cohort(self, matrix: PsychVariableMatrix) -> None:
        ctx = _make_mood_context(mood=MoodStatePrimary.STATUS)
        maturity = _make_maturity(cohort=AudienceMaturityCohort.NEW)
        result = matrix.resolve(ctx, maturity)

        assert result.comparison_type == ComparisonType.UPWARD_ASSIMILATION

    def test_discovery_sequencing_dependency(self, matrix: PsychVariableMatrix) -> None:
        ctx = _make_mood_context(mood=MoodStatePrimary.DISCOVERY)
        result = matrix.resolve(ctx, _make_maturity())

        assert result.sequencing_dependency == SequencingDependency.REQUIRES_POSITIVE_PRIME

    def test_processing_high_arousal(self, matrix: PsychVariableMatrix) -> None:
        ctx = _make_mood_context(
            mood=MoodStatePrimary.PROCESSING, arousal=AudienceArousalLevel.HIGH
        )
        result = matrix.resolve(ctx, _make_maturity(cohort=AudienceMaturityCohort.NEW))

        assert result.arousal_direction == ArousalDirection.LOWERS
        assert result.valence_delivery == ValenceDelivery.EUDAIMONIC
        assert result.sdt_need_primary == SDTNeedPrimary.RELATEDNESS
        assert result.tmt_function == TMTFunction.INSIGHT_DELIVERY

    def test_threat_avoidant_gives_prevention_frame(
        self, matrix: PsychVariableMatrix
    ) -> None:
        ctx = _make_mood_context(regulatory=RegulatoryOrientation.THREAT_AVOIDANT)
        result = matrix.resolve(ctx, _make_maturity())
        assert result.regulatory_frame == RegulatoryFrame.PREVENTION


# ─── Payload Masking Library ──────────────────────────────────────────────────


class TestPayloadMaskingLibrary:
    """Spec §10 Integration Test: Payload Masking String regression."""

    def test_all_four_mood_states_have_instructions(self) -> None:
        for mood in MoodStatePrimary:
            instruction = get_payload_masking_instruction(mood)
            assert len(instruction) > 30, (
                f"Payload masking instruction for {mood.value} is too short: {instruction!r}"
            )

    def test_escape_instruction_contains_required_literal(self) -> None:
        """Spec §10 'Payload Masking String Test': literal string must be present.

        Spec: 'Use regex matching to verify the explicit literal string
        "The truth is the punchline, not the lesson" is present.'
        """
        instruction = get_payload_masking_instruction(MoodStatePrimary.ESCAPE)
        assert re.search(
            r"The truth is the punchline, not the lesson",
            instruction,
        ), (
            f"ESCAPE instruction missing required literal. Got: {instruction!r}"
        )

    def test_escape_instruction_contains_escape_mode_header(self) -> None:
        instruction = get_payload_masking_instruction(MoodStatePrimary.ESCAPE)
        assert "ESCAPE collision mode" in instruction

    def test_discovery_instruction_references_competence(self) -> None:
        instruction = get_payload_masking_instruction(MoodStatePrimary.DISCOVERY)
        assert "competent" in instruction.lower() or "discovery" in instruction.lower()


# ─── Pipeline Integration ─────────────────────────────────────────────────────


class TestPipelineIntegration:
    """Spec §10 Integration Test: Full brief injection flow."""

    def test_brief_written_to_output_dir(
        self, tmp_path: Path, receipt_chain: ReceiptChain
    ) -> None:
        output_dir = tmp_path / "routing_briefs"
        generator = PsychRoutingBriefGenerator(
            coach_id="coach-TST-001",
            receipt_chain=receipt_chain,
            output_dir=output_dir,
        )
        mood = _make_mood_context(coach_id="coach-TST-001")
        maturity = _make_maturity(coach_id="coach-TST-001")
        brief = generator.generate(mood_context=mood, maturity_profile=maturity)

        brief_path = output_dir / "psych_routing_brief.json"
        assert brief_path.exists()

        import json
        data = json.loads(brief_path.read_text())
        assert data["routing_id"] == brief.routing_id

    def test_three_receipts_written(
        self, tmp_path: Path, receipt_chain: ReceiptChain
    ) -> None:
        """3 receipt writes per pipeline run (Stage 1, 2, 3)."""
        import glob

        generator = PsychRoutingBriefGenerator(
            coach_id="coach-TST-001",
            receipt_chain=receipt_chain,
        )
        generator.generate()

        receipt_files = glob.glob(str(tmp_path / "receipts" / "*.jsonl"))
        assert len(receipt_files) >= 1

        total_lines = sum(
            sum(1 for line in open(f) if line.strip())
            for f in receipt_files
        )
        assert total_lines >= 3, f"Expected ≥3 receipt entries, found {total_lines}"

    def test_full_brief_schema_valid(
        self, receipt_chain: ReceiptChain
    ) -> None:
        """Brief produced is a fully valid DEP-ENG-016 schema object."""
        generator = PsychRoutingBriefGenerator(
            coach_id="coach-TST-001",
            receipt_chain=receipt_chain,
        )
        mood = _make_mood_context(
            mood=MoodStatePrimary.DISCOVERY,
            arousal=AudienceArousalLevel.HIGH,
            coach_id="coach-TST-001",
        )
        maturity = _make_maturity(
            cohort=AudienceMaturityCohort.DEVELOPING,
            coach_id="coach-TST-001",
        )
        brief = generator.generate(mood_context=mood, maturity_profile=maturity)

        # Structural validation
        assert brief.routing_id.startswith("PRB-")
        assert brief.receipt_chain_hash != ""
        assert brief.psychological_classification.mood_state_primary == MoodStatePrimary.DISCOVERY
        assert brief.psychological_classification.sdt_need_primary == SDTNeedPrimary.COMPETENCE
        assert brief.psychological_classification.sequencing_dependency == SequencingDependency.REQUIRES_POSITIVE_PRIME
        assert brief.psychological_classification.tmt_function == TMTFunction.NONE
        assert brief.payload_masking_instruction != ""
        assert brief.is_fallback is False
        assert brief.operator_warning is None
