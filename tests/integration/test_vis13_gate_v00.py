"""
FR-VIS-13 — Gate V-00: Image Type Validity Gate — Integration Tests
Phase 2B, CVE Visual Engine — spec 1 of 13

Tests cover all 7 Acceptance Criteria (AC1-AC7) plus safety tests
from FR-VIS-13 §8 and §10.

Every test traces to an explicit AC or test case in the spec.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.visual_engine_models import (
    CAROUSEL_FORMAT_PREFIXES,
    IMAGE_TYPE_TO_IMPLIED_STYLES,
    MAX_REVISION_CYCLES,
    OBSERVATIONAL_HUMOR_ALLOWED_TYPES,
    OBSERVATIONAL_HUMOR_FORMATS,
    POLL_ALLOWED_TYPES,
    POLL_FORMATS,
    SQUARE_ALLOWED_FORMATS,
    SUGGESTED_CORRECTIONS,
    VALID_IMAGE_TYPE_VALUES,
    FormatConstraintEnvelope,
    GateV00Result,
    GateV00Verdict,
    GateV00Violation,
    ImageType,
    OperatorReviewStatus,
    SlideValidationSummary,
    StyleConstraintDirective,
    VCBInput,
    VCBSlideAssignment,
    ViolationType,
)
from src.ccp.services.gate_v00_image_type_validator import GateV00ImageTypeValidator


# ─────────────────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────────────────


@pytest.fixture
def tmp_receipt_dir(tmp_path: Path) -> Path:
    """Create a temporary directory for receipt chain logs."""
    receipt_dir = tmp_path / "receipts"
    receipt_dir.mkdir()
    return receipt_dir


@pytest.fixture
def receipt_chain(tmp_receipt_dir: Path) -> ReceiptChain:
    """Create a ReceiptChain scoped to test coach."""
    return ReceiptChain(coach_acronym="TST", log_dir=str(tmp_receipt_dir))


@pytest.fixture
def validator(receipt_chain: ReceiptChain) -> GateV00ImageTypeValidator:
    """Create a GateV00ImageTypeValidator for testing."""
    return GateV00ImageTypeValidator(
        coach_acronym="TST",
        receipt_chain=receipt_chain,
    )


def _make_slide(
    index: int,
    image_type: str | None = "tier_3_ai_realistic",
    named_person: str | None = None,
    aspect_ratio: str = "4:5",
) -> VCBSlideAssignment:
    """Helper: create a single VCB slide assignment."""
    return VCBSlideAssignment(
        slide_index=index,
        image_type=image_type,
        named_person_reference=named_person,
        aspect_ratio_template=aspect_ratio,
    )


def _make_vcb(
    slides: list[VCBSlideAssignment],
    content_format: str = "carousel_dopamine_cliff",
    aspect_ratio: str = "4:5",
    permitted_styles: list[str] | None = None,
    prohibited_styles: list[str] | None = None,
    mandatory_style: str | None = None,
    revision_count: int = 0,
) -> VCBInput:
    """Helper: create a complete VCB input for testing."""
    return VCBInput(
        vcb_id=f"VCB-TST-{len(slides)}",
        content_output_id=f"CO-TST-001-{content_format.upper()[:10]}",
        coach_acronym="TST",
        slides=slides,
        format_envelope=FormatConstraintEnvelope(
            content_format=content_format,
            aspect_ratio=aspect_ratio,
            total_slides=len(slides),
        ),
        style_directive=StyleConstraintDirective(
            permitted_styles=permitted_styles or [],
            prohibited_styles=prohibited_styles or [],
            mandatory_style=mandatory_style,
        ),
        revision_count=revision_count,
    )


# ─────────────────────────────────────────────────────
# MODEL VALIDATION TESTS
# ─────────────────────────────────────────────────────


class TestVisualEngineModels:
    """Test model definitions and constants from visual_engine_models.py."""

    def test_valid_image_types_enum_has_8_members(self) -> None:
        """FR-VIS-13 §4 Stage 1 Step 3: 8 valid image types."""
        assert len(ImageType) == 8

    def test_valid_image_type_values_frozenset(self) -> None:
        """FR-VIS-13 §4 Stage 1: all 8 image types in the valid set."""
        expected = {
            "tier_1_real_person",
            "tier_2_stock_environmental",
            "tier_2_stock_contextual",
            "tier_2_stock_abstract",
            "tier_3_ai_realistic",
            "tier_4_ai_ghibli",
            "graphic_vector",
            "animated_gif",
        }
        assert VALID_IMAGE_TYPE_VALUES == expected

    def test_violation_type_enum_has_10_members(self) -> None:
        """FR-VIS-13 §7 Task 8: 10 error types."""
        assert len(ViolationType) == 10

    def test_implied_style_mapping_covers_all_image_types(self) -> None:
        """FR-VIS-13 §4 Stage 3: every image type has an implied style mapping."""
        for image_type in ImageType:
            assert image_type.value in IMAGE_TYPE_TO_IMPLIED_STYLES, (
                f"Missing implied style mapping for {image_type.value}"
            )

    def test_max_revision_cycles_is_2(self) -> None:
        """FR-VIS-13 §3 Technical Decision 3: max 2 revision cycles."""
        assert MAX_REVISION_CYCLES == 2

    def test_carousel_format_prefix(self) -> None:
        """FR-VIS-13 §4 Stage 2 V00-R01: carousel prefix matching."""
        assert "carousel_" in CAROUSEL_FORMAT_PREFIXES

    def test_observational_humor_formats(self) -> None:
        """FR-VIS-13 §4 Stage 2 V00-R02: obs humor format set."""
        assert "single_observational_humor" in OBSERVATIONAL_HUMOR_FORMATS
        assert "single_observational_humor_square" in OBSERVATIONAL_HUMOR_FORMATS

    def test_poll_formats(self) -> None:
        """FR-VIS-13 §4 Stage 2 V00-R04: poll format set."""
        assert "poll_archetypical" in POLL_FORMATS
        assert "poll_stereotypical" in POLL_FORMATS
        assert "poll_controversial_dilemma" in POLL_FORMATS

    def test_square_allowed_formats(self) -> None:
        """FR-VIS-13 §4 Stage 2 V00-R05: square format set."""
        assert SQUARE_ALLOWED_FORMATS == frozenset({
            "single_tweet_quote",
            "single_supervisual",
            "single_conceptual_contrast_simultaneous",
            "single_observational_humor_square",
        })

    def test_suggested_corrections_cover_all_violation_types(self) -> None:
        """FR-VIS-13 §8: every violation type has a suggested correction."""
        for vtype in ViolationType:
            assert vtype.value in SUGGESTED_CORRECTIONS, (
                f"Missing suggested correction for {vtype.value}"
            )


# ─────────────────────────────────────────────────────
# AC1: Carousel Ghibli Block
# FR-VIS-13 §8 AC1
# ─────────────────────────────────────────────────────


class TestAC1CarouselGhibliBlock:
    """AC1: Carousel slides cannot use tier_4_ai_ghibli."""

    def test_carousel_ghibli_on_slide_3_fails(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """FR-VIS-13 §8 AC1: VCB for carousel_dopamine_cliff with 7 slides.
        Slide 3 = tier_4_ai_ghibli. Assert CAROUSEL_GHIBLI_VIOLATION on slide 3,
        all other slides PASS."""
        slides = [
            _make_slide(0, "tier_3_ai_realistic"),
            _make_slide(1, "tier_2_stock_environmental"),
            _make_slide(2, "tier_3_ai_realistic"),
            _make_slide(3, "tier_4_ai_ghibli"),  # Violation
            _make_slide(4, "tier_3_ai_realistic"),
            _make_slide(5, "tier_2_stock_contextual"),
            _make_slide(6, "tier_3_ai_realistic"),
        ]
        vcb = _make_vcb(slides, content_format="carousel_dopamine_cliff")
        result = validator.validate(vcb)

        assert result.verdict == GateV00Verdict.GATE_V00_FAIL.value
        assert len(result.violations) == 1
        v = result.violations[0]
        assert v.violation_type == ViolationType.CAROUSEL_GHIBLI_VIOLATION.value
        assert v.slide_index == 3
        assert v.rule_id == "V00-R01"
        assert "tier_3_ai_realistic" in v.suggested_correction
        assert "tier_2_stock_contextual" in v.suggested_correction

        # All other slides pass
        for summary in result.slide_validation_summary:
            if summary.slide_index == 3:
                assert summary.format_check == "FAIL"
            else:
                assert summary.format_check == "PASS"

    def test_carousel_listicle_ghibli_fails(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """FR-VIS-13 §10 Unit Test V00-R01: carousel_listicle + tier_4_ai_ghibli."""
        slides = [
            _make_slide(0, "tier_2_stock_environmental"),
            _make_slide(1, "tier_4_ai_ghibli"),
            _make_slide(2, "tier_3_ai_realistic"),
        ]
        vcb = _make_vcb(slides, content_format="carousel_listicle")
        result = validator.validate(vcb)

        assert result.verdict == GateV00Verdict.GATE_V00_FAIL.value
        violations_r01 = [
            v for v in result.violations
            if v.violation_type == ViolationType.CAROUSEL_GHIBLI_VIOLATION.value
        ]
        assert len(violations_r01) == 1
        assert violations_r01[0].slide_index == 1

    def test_non_carousel_ghibli_passes(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """Ghibli is allowed on non-carousel single image formats."""
        slides = [_make_slide(0, "tier_4_ai_ghibli")]
        vcb = _make_vcb(
            slides,
            content_format="single_conceptual_contrast_simultaneous",
            permitted_styles=["ghibli_illustration"],
        )
        result = validator.validate(vcb)
        assert result.verdict == GateV00Verdict.GATE_V00_PASS.value


# ─────────────────────────────────────────────────────
# AC2: Observational Humor AI Block
# FR-VIS-13 §8 AC2
# ─────────────────────────────────────────────────────


class TestAC2ObservationalHumorAIBlock:
    """AC2: Observational Humor must use real/stock types only — never AI."""

    def test_obs_humor_ai_realistic_fails(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """FR-VIS-13 §8 AC2: single_observational_humor + tier_3_ai_realistic → FAIL."""
        slides = [_make_slide(0, "tier_3_ai_realistic")]
        vcb = _make_vcb(slides, content_format="single_observational_humor")
        result = validator.validate(vcb)

        assert result.verdict == GateV00Verdict.GATE_V00_FAIL.value
        assert len(result.violations) == 1
        assert result.violations[0].violation_type == (
            ViolationType.OBSERVATIONAL_HUMOR_AI_VIOLATION.value
        )

    def test_obs_humor_stock_contextual_passes(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """FR-VIS-13 §8 AC2: single_observational_humor + tier_2_stock_contextual → PASS."""
        slides = [_make_slide(0, "tier_2_stock_contextual")]
        vcb = _make_vcb(slides, content_format="single_observational_humor")
        result = validator.validate(vcb)
        assert result.verdict == GateV00Verdict.GATE_V00_PASS.value

    def test_obs_humor_ghibli_fails(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """FR-VIS-13 §4 Stage 2 V00-R02: Ghibli is AI-generated, fails obs humor."""
        slides = [_make_slide(0, "tier_4_ai_ghibli")]
        vcb = _make_vcb(slides, content_format="single_observational_humor")
        result = validator.validate(vcb)

        assert result.verdict == GateV00Verdict.GATE_V00_FAIL.value
        ai_violations = [
            v for v in result.violations
            if v.violation_type == ViolationType.OBSERVATIONAL_HUMOR_AI_VIOLATION.value
        ]
        assert len(ai_violations) >= 1

    def test_obs_humor_real_person_passes(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """tier_1_real_person is allowed for observational humor."""
        slides = [_make_slide(0, "tier_1_real_person")]
        vcb = _make_vcb(slides, content_format="single_observational_humor")
        result = validator.validate(vcb)
        assert result.verdict == GateV00Verdict.GATE_V00_PASS.value

    def test_obs_humor_square_format_also_checked(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """single_observational_humor_square also enforces V00-R02."""
        slides = [_make_slide(0, "tier_3_ai_realistic")]
        vcb = _make_vcb(slides, content_format="single_observational_humor_square")
        result = validator.validate(vcb)
        assert result.verdict == GateV00Verdict.GATE_V00_FAIL.value
        assert result.violations[0].violation_type == (
            ViolationType.OBSERVATIONAL_HUMOR_AI_VIOLATION.value
        )


# ─────────────────────────────────────────────────────
# AC3: Named Person Tier 1 Mandate
# FR-VIS-13 §8 AC3
# ─────────────────────────────────────────────────────


class TestAC3NamedPersonTier1Mandate:
    """AC3: Named person slides must use tier_1_real_person."""

    def test_named_person_ai_realistic_fails(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """FR-VIS-13 §8 AC3: named_person='Brené Brown' + tier_3_ai_realistic → FAIL."""
        slides = [
            _make_slide(0, "tier_3_ai_realistic"),
            _make_slide(1, "tier_3_ai_realistic"),
            _make_slide(2, "tier_3_ai_realistic", named_person="Brené Brown"),
        ]
        vcb = _make_vcb(slides, content_format="carousel_dopamine_cliff")
        result = validator.validate(vcb)

        assert result.verdict == GateV00Verdict.GATE_V00_FAIL.value
        named_violations = [
            v for v in result.violations
            if v.violation_type == ViolationType.NAMED_PERSON_TIER_VIOLATION.value
        ]
        assert len(named_violations) == 1
        assert named_violations[0].slide_index == 2
        assert "Brené Brown" in named_violations[0].explanation
        assert named_violations[0].suggested_correction == (
            "Change image_type to 'tier_1_real_person'"
        )

    def test_named_person_tier1_passes(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """Named person with tier_1_real_person passes V00-R03."""
        slides = [
            _make_slide(0, "tier_3_ai_realistic"),
            _make_slide(1, "tier_1_real_person", named_person="Simon Sinek"),
        ]
        vcb = _make_vcb(slides, content_format="carousel_dopamine_cliff")
        result = validator.validate(vcb)
        assert result.verdict == GateV00Verdict.GATE_V00_PASS.value

    def test_null_named_person_skips_check(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """Slides without named_person_reference skip V00-R03."""
        slides = [_make_slide(0, "tier_3_ai_realistic", named_person=None)]
        vcb = _make_vcb(slides, content_format="carousel_dopamine_cliff")
        result = validator.validate(vcb)
        assert result.verdict == GateV00Verdict.GATE_V00_PASS.value

    def test_empty_named_person_skips_check(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """Empty string named_person_reference also skips V00-R03."""
        slides = [_make_slide(0, "tier_3_ai_realistic", named_person="")]
        vcb = _make_vcb(slides, content_format="carousel_dopamine_cliff")
        result = validator.validate(vcb)
        assert result.verdict == GateV00Verdict.GATE_V00_PASS.value


# ─────────────────────────────────────────────────────
# AC4: Poll Zone Photographic Block
# FR-VIS-13 §8 AC4
# ─────────────────────────────────────────────────────


class TestAC4PollPhotographicBlock:
    """AC4: Poll option zones cannot use photographic types."""

    def test_poll_real_person_fails(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """FR-VIS-13 §8 AC4: poll_archetypical + tier_1_real_person → FAIL."""
        slides = [
            _make_slide(0, "tier_1_real_person"),
            _make_slide(1, "tier_1_real_person"),
        ]
        vcb = _make_vcb(slides, content_format="poll_archetypical", aspect_ratio="9:16")
        result = validator.validate(vcb)

        assert result.verdict == GateV00Verdict.GATE_V00_FAIL.value
        poll_violations = [
            v for v in result.violations
            if v.violation_type == ViolationType.POLL_PHOTOGRAPHIC_VIOLATION.value
        ]
        assert len(poll_violations) == 2  # Both slides fail

    def test_poll_graphic_vector_passes(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """FR-VIS-13 §8 AC4: poll_archetypical + graphic_vector → PASS."""
        slides = [
            _make_slide(0, "graphic_vector"),
            _make_slide(1, "graphic_vector"),
        ]
        vcb = _make_vcb(slides, content_format="poll_archetypical", aspect_ratio="9:16")
        result = validator.validate(vcb)
        assert result.verdict == GateV00Verdict.GATE_V00_PASS.value

    def test_poll_ai_realistic_passes(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """tier_3_ai_realistic is allowed for polls per V00-R04."""
        slides = [
            _make_slide(0, "tier_3_ai_realistic"),
            _make_slide(1, "tier_3_ai_realistic"),
        ]
        vcb = _make_vcb(slides, content_format="poll_stereotypical", aspect_ratio="9:16")
        result = validator.validate(vcb)
        assert result.verdict == GateV00Verdict.GATE_V00_PASS.value

    def test_poll_stock_types_fail(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """Stock photo types are photographic and fail poll check."""
        slides = [_make_slide(0, "tier_2_stock_environmental")]
        vcb = _make_vcb(
            slides, content_format="poll_controversial_dilemma", aspect_ratio="9:16"
        )
        result = validator.validate(vcb)
        assert result.verdict == GateV00Verdict.GATE_V00_FAIL.value
        assert result.violations[0].violation_type == (
            ViolationType.POLL_PHOTOGRAPHIC_VIOLATION.value
        )


# ─────────────────────────────────────────────────────
# AC5: Multi-Violation Collection
# FR-VIS-13 §8 AC5
# ─────────────────────────────────────────────────────


class TestAC5MultiViolationCollection:
    """AC5: Gate V-00 collects ALL violations in a single pass."""

    def test_three_simultaneous_violations(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """FR-VIS-13 §8 AC5: 3 violations on different slides in single report.
        Slide 0: carousel ghibli (V00-R01)
        Slide 3: named person tier violation (V00-R03)
        Slide 5: style conflict (STYLE_IMAGE_TYPE_CONFLICT via prohibited style)
        """
        slides = [
            _make_slide(0, "tier_4_ai_ghibli"),  # V00-R01 carousel ghibli
            _make_slide(1, "tier_3_ai_realistic"),
            _make_slide(2, "tier_2_stock_environmental"),
            _make_slide(3, "tier_3_ai_realistic", named_person="Tony Robbins"),  # V00-R03
            _make_slide(4, "tier_3_ai_realistic"),
            _make_slide(5, "tier_2_stock_abstract"),  # style conflict
            _make_slide(6, "tier_3_ai_realistic"),
        ]
        vcb = _make_vcb(
            slides,
            content_format="carousel_dopamine_cliff",
            prohibited_styles=["real_photography_only"],  # Conflicts with slide 5
        )
        result = validator.validate(vcb)

        assert result.verdict == GateV00Verdict.GATE_V00_FAIL.value

        # Must collect at least 3 violations in single pass
        assert len(result.violations) >= 3

        violation_types = {v.violation_type for v in result.violations}
        assert ViolationType.CAROUSEL_GHIBLI_VIOLATION.value in violation_types
        assert ViolationType.NAMED_PERSON_TIER_VIOLATION.value in violation_types
        assert ViolationType.STYLE_IMAGE_TYPE_CONFLICT.value in violation_types

    def test_does_not_halt_on_first_violation(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """FR-VIS-13 §4 Stage 2 Step 3: does not halt on first failure."""
        slides = [
            _make_slide(0, "tier_4_ai_ghibli"),  # V00-R01
            _make_slide(1, "tier_4_ai_ghibli"),  # V00-R01
            _make_slide(2, "tier_4_ai_ghibli"),  # V00-R01
        ]
        vcb = _make_vcb(slides, content_format="carousel_relief_peak")
        result = validator.validate(vcb)

        # All 3 slides should have violations, not just the first
        assert len(result.violations) == 3
        for i, v in enumerate(result.violations):
            assert v.slide_index == i


# ─────────────────────────────────────────────────────
# AC6: Escalation After 2 Failures
# FR-VIS-13 §8 AC6
# ─────────────────────────────────────────────────────


class TestAC6EscalationAfter2Failures:
    """AC6: Second failure triggers GATE_V00_ESCALATE + PENDING_OPERATOR_REVIEW."""

    def test_first_failure_returns_fail_not_escalate(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """revision_count=0, violations present → GATE_V00_FAIL."""
        slides = [_make_slide(0, "tier_4_ai_ghibli")]
        vcb = _make_vcb(
            slides, content_format="carousel_dopamine_cliff", revision_count=0
        )
        result = validator.validate(vcb)
        assert result.verdict == GateV00Verdict.GATE_V00_FAIL.value
        assert result.operator_review_status is None

    def test_second_attempt_still_fail(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """revision_count=1, violations present → GATE_V00_FAIL (one more try)."""
        slides = [_make_slide(0, "tier_4_ai_ghibli")]
        vcb = _make_vcb(
            slides, content_format="carousel_dopamine_cliff", revision_count=1
        )
        result = validator.validate(vcb)
        assert result.verdict == GateV00Verdict.GATE_V00_FAIL.value

    def test_third_attempt_escalates(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """FR-VIS-13 §8 AC6: revision_count=2, violations present → GATE_V00_ESCALATE."""
        slides = [_make_slide(0, "tier_4_ai_ghibli")]
        vcb = _make_vcb(
            slides, content_format="carousel_dopamine_cliff", revision_count=2
        )
        first_round_violations = [
            GateV00Violation(
                rule_id="V00-R01",
                slide_index=0,
                assigned_image_type="tier_4_ai_ghibli",
                violation_type=ViolationType.CAROUSEL_GHIBLI_VIOLATION.value,
                explanation="First attempt violation",
                suggested_correction="Change image_type",
            )
        ]
        result = validator.validate_with_revision_tracking(
            vcb, previous_violations=[first_round_violations]
        )

        assert result.verdict == GateV00Verdict.GATE_V00_ESCALATE.value
        assert result.operator_review_status == (
            OperatorReviewStatus.PENDING_OPERATOR_REVIEW.value
        )
        # Full violation history must be present
        assert result.violation_history is not None
        assert len(result.violation_history) >= 2  # At least 2 rounds of violations

    def test_full_revision_cycle_flow(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """FR-VIS-13 §4 Stage 4: complete revision cycle simulation.

        Round 1: fail (revision_count=0)
        Round 2: fail again (revision_count=1)
        Round 3: escalate (revision_count=2)
        """
        # Round 1
        slides_r1 = [_make_slide(0, "tier_4_ai_ghibli")]
        vcb_r1 = _make_vcb(
            slides_r1, content_format="carousel_dopamine_cliff", revision_count=0
        )
        result_r1 = validator.validate_with_revision_tracking(vcb_r1)
        assert result_r1.verdict == GateV00Verdict.GATE_V00_FAIL.value
        history = [list(result_r1.violations)]

        # Round 2: Abel "fixes" but introduces different violation
        slides_r2 = [
            _make_slide(0, "tier_3_ai_realistic", named_person="Gary Vee"),
        ]
        vcb_r2 = _make_vcb(
            slides_r2, content_format="carousel_dopamine_cliff", revision_count=1
        )
        result_r2 = validator.validate_with_revision_tracking(
            vcb_r2, previous_violations=history
        )
        assert result_r2.verdict == GateV00Verdict.GATE_V00_FAIL.value
        history.append(list(result_r2.violations))

        # Round 3: still broken → escalate
        slides_r3 = [
            _make_slide(0, "tier_3_ai_realistic", named_person="Gary Vee"),
        ]
        vcb_r3 = _make_vcb(
            slides_r3, content_format="carousel_dopamine_cliff", revision_count=2
        )
        result_r3 = validator.validate_with_revision_tracking(
            vcb_r3, previous_violations=history
        )
        assert result_r3.verdict == GateV00Verdict.GATE_V00_ESCALATE.value
        assert result_r3.operator_review_status == (
            OperatorReviewStatus.PENDING_OPERATOR_REVIEW.value
        )


# ─────────────────────────────────────────────────────
# AC7: Clean Pass
# FR-VIS-13 §8 AC7
# ─────────────────────────────────────────────────────


class TestAC7CleanPass:
    """AC7: Valid VCB passes Gate V-00 and is forwarded to V-01."""

    def test_valid_carousel_passes(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """FR-VIS-13 §8 AC7: carousel with valid types, no named persons → PASS."""
        slides = [
            _make_slide(0, "tier_3_ai_realistic"),
            _make_slide(1, "tier_2_stock_environmental"),
            _make_slide(2, "tier_3_ai_realistic"),
            _make_slide(3, "tier_2_stock_contextual"),
            _make_slide(4, "tier_3_ai_realistic"),
            _make_slide(5, "tier_2_stock_abstract"),
            _make_slide(6, "tier_3_ai_realistic"),
        ]
        vcb = _make_vcb(slides, content_format="carousel_dopamine_cliff")
        result = validator.validate(vcb)

        assert result.verdict == GateV00Verdict.GATE_V00_PASS.value
        assert len(result.violations) == 0
        assert len(result.slide_validation_summary) == 7

        # All slides PASS both checks
        for summary in result.slide_validation_summary:
            assert summary.format_check == "PASS"
            assert summary.style_check == "PASS"

    def test_valid_single_image_passes(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """Single image with valid type passes."""
        slides = [_make_slide(0, "tier_3_ai_realistic")]
        vcb = _make_vcb(slides, content_format="single_tweet_quote")
        result = validator.validate(vcb)
        assert result.verdict == GateV00Verdict.GATE_V00_PASS.value

    def test_valid_poll_passes(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """Poll with graphic_vector passes."""
        slides = [
            _make_slide(0, "graphic_vector"),
            _make_slide(1, "graphic_vector"),
        ]
        vcb = _make_vcb(
            slides, content_format="poll_archetypical", aspect_ratio="9:16"
        )
        result = validator.validate(vcb)
        assert result.verdict == GateV00Verdict.GATE_V00_PASS.value

    def test_null_named_person_does_not_crash(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """FR-VIS-13 §8 AC7 Failure Example: null named_person_reference must not crash."""
        slides = [
            _make_slide(0, "tier_3_ai_realistic", named_person=None),
            _make_slide(1, "tier_2_stock_environmental", named_person=None),
        ]
        vcb = _make_vcb(slides, content_format="carousel_relief_peak")
        result = validator.validate(vcb)
        assert result.verdict == GateV00Verdict.GATE_V00_PASS.value


# ─────────────────────────────────────────────────────
# STAGE 1: Extraction Tests
# FR-VIS-13 §4 Stage 1
# ─────────────────────────────────────────────────────


class TestStage1Extraction:
    """Stage 1: VCB Image Type Extraction validation."""

    def test_missing_image_type_fails(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """FR-VIS-13 §4 Stage 1 Step 4: missing image_type → MISSING_IMAGE_TYPE."""
        slides = [
            _make_slide(0, "tier_3_ai_realistic"),
            _make_slide(1, None),  # Missing
            _make_slide(2, "tier_3_ai_realistic"),
        ]
        vcb = _make_vcb(slides, content_format="carousel_dopamine_cliff")
        result = validator.validate(vcb)

        assert result.verdict == GateV00Verdict.GATE_V00_FAIL.value
        missing = [
            v for v in result.violations
            if v.violation_type == ViolationType.MISSING_IMAGE_TYPE.value
        ]
        assert len(missing) == 1
        assert missing[0].slide_index == 1

    def test_invalid_image_type_fails(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """FR-VIS-13 §4 Stage 1 Step 4: invalid value → INVALID_IMAGE_TYPE."""
        slides = [_make_slide(0, "not_a_valid_type")]
        vcb = _make_vcb(slides, content_format="carousel_dopamine_cliff")
        result = validator.validate(vcb)

        assert result.verdict == GateV00Verdict.GATE_V00_FAIL.value
        invalid = [
            v for v in result.violations
            if v.violation_type == ViolationType.INVALID_IMAGE_TYPE.value
        ]
        assert len(invalid) == 1

    def test_legacy_vcb_all_missing_types(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """FR-VIS-13 §6: Legacy VCB without any image_type fields
        → LEGACY_VCB_UPGRADE_REQUIRED."""
        slides = [
            _make_slide(0, None),
            _make_slide(1, None),
            _make_slide(2, None),
        ]
        vcb = _make_vcb(slides, content_format="carousel_dopamine_cliff")
        result = validator.validate(vcb)

        assert result.verdict == GateV00Verdict.GATE_V00_FAIL.value
        legacy = [
            v for v in result.violations
            if v.violation_type == ViolationType.LEGACY_VCB_UPGRADE_REQUIRED.value
        ]
        assert len(legacy) == 3  # One per slide


# ─────────────────────────────────────────────────────
# STAGE 3: Style Cross-Validation Tests
# FR-VIS-13 §4 Stage 3
# ─────────────────────────────────────────────────────


class TestStage3StyleCrossValidation:
    """Stage 3: Style-Image Type Cross-Validation."""

    def test_style_conflict_with_prohibited(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """FR-VIS-13 §4 Stage 3 Step 3: implied style in prohibited → STYLE_IMAGE_TYPE_CONFLICT."""
        slides = [_make_slide(0, "tier_4_ai_ghibli")]
        vcb = _make_vcb(
            slides,
            content_format="single_supervisual",
            prohibited_styles=["ghibli_illustration"],
        )
        result = validator.validate(vcb)

        assert result.verdict == GateV00Verdict.GATE_V00_FAIL.value
        style_violations = [
            v for v in result.violations
            if v.violation_type == ViolationType.STYLE_IMAGE_TYPE_CONFLICT.value
        ]
        assert len(style_violations) == 1

    def test_mandatory_style_mismatch(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """FR-VIS-13 §4 Stage 3 Step 4: mandatory_style not in implied → MANDATORY_STYLE_CONFLICT."""
        slides = [_make_slide(0, "tier_2_stock_environmental")]
        vcb = _make_vcb(
            slides,
            content_format="single_tweet_quote",
            mandatory_style="ghibli_illustration",
        )
        result = validator.validate(vcb)

        assert result.verdict == GateV00Verdict.GATE_V00_FAIL.value
        mandatory_violations = [
            v for v in result.violations
            if v.violation_type == ViolationType.MANDATORY_STYLE_CONFLICT.value
        ]
        assert len(mandatory_violations) == 1

    def test_mandatory_style_match_passes(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """Mandatory style matching implied style passes."""
        slides = [_make_slide(0, "tier_4_ai_ghibli")]
        vcb = _make_vcb(
            slides,
            content_format="single_supervisual",
            mandatory_style="ghibli_illustration",
        )
        result = validator.validate(vcb)
        assert result.verdict == GateV00Verdict.GATE_V00_PASS.value

    def test_no_style_constraints_passes(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """Empty style directive means no style constraints to violate."""
        slides = [_make_slide(0, "tier_3_ai_realistic")]
        vcb = _make_vcb(slides, content_format="single_tweet_quote")
        result = validator.validate(vcb)
        assert result.verdict == GateV00Verdict.GATE_V00_PASS.value


# ─────────────────────────────────────────────────────
# V00-R05: Aspect Ratio Format Tests
# FR-VIS-13 §4 Stage 2 V00-R05
# ─────────────────────────────────────────────────────


class TestV00R05AspectRatio:
    """V00-R05: 1:1 aspect ratio only for approved formats."""

    def test_square_on_unapproved_format_fails(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """1:1 on carousel format → ASPECT_RATIO_FORMAT_VIOLATION."""
        slides = [_make_slide(0, "tier_3_ai_realistic")]
        vcb = _make_vcb(
            slides, content_format="carousel_dopamine_cliff", aspect_ratio="1:1"
        )
        result = validator.validate(vcb)

        assert result.verdict == GateV00Verdict.GATE_V00_FAIL.value
        ar_violations = [
            v for v in result.violations
            if v.violation_type == ViolationType.ASPECT_RATIO_FORMAT_VIOLATION.value
        ]
        assert len(ar_violations) >= 1

    def test_square_on_approved_format_passes(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """1:1 on single_tweet_quote (approved) → PASS."""
        slides = [_make_slide(0, "tier_3_ai_realistic")]
        vcb = _make_vcb(
            slides, content_format="single_tweet_quote", aspect_ratio="1:1"
        )
        result = validator.validate(vcb)
        assert result.verdict == GateV00Verdict.GATE_V00_PASS.value

    def test_standard_aspect_ratios_skip_r05(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """4:5 and 9:16 never trigger V00-R05."""
        for ar in ["4:5", "9:16"]:
            slides = [_make_slide(0, "tier_3_ai_realistic")]
            vcb = _make_vcb(
                slides, content_format="carousel_dopamine_cliff", aspect_ratio=ar
            )
            result = validator.validate(vcb)
            ar_violations = [
                v for v in result.violations
                if v.violation_type == ViolationType.ASPECT_RATIO_FORMAT_VIOLATION.value
            ]
            assert len(ar_violations) == 0


# ─────────────────────────────────────────────────────
# RECEIPT CHAIN INTEGRATION TESTS
# FR-VIS-13 §4 Receipt Writes
# ─────────────────────────────────────────────────────


class TestReceiptChainIntegration:
    """Verify receipt chain writes at every stage per FR47 DEP-ENG-041."""

    def test_pass_writes_3_receipts(
        self, validator: GateV00ImageTypeValidator, tmp_receipt_dir: Path
    ) -> None:
        """Gate V-00 PASS writes 3 receipts: extraction, cross-validation, verdict."""
        slides = [_make_slide(0, "tier_3_ai_realistic")]
        vcb = _make_vcb(slides, content_format="carousel_dopamine_cliff")
        result = validator.validate(vcb)

        assert result.verdict == GateV00Verdict.GATE_V00_PASS.value
        assert result.receipt_chain_block != ""

        # Read receipt log files
        receipt_files = list(tmp_receipt_dir.glob("receipt_*.jsonl"))
        assert len(receipt_files) >= 1

        receipts = []
        for f in receipt_files:
            for line in f.read_text().strip().split("\n"):
                if line:
                    receipts.append(json.loads(line))

        assert len(receipts) == 3

        # Verify stage names
        actions = [r["action"] for r in receipts]
        assert "GATE_V00_EXTRACTION" in actions
        assert "GATE_V00_CROSS_VALIDATION" in actions
        assert "GATE_V00_VERDICT" in actions

        # Verify chain linking
        assert receipts[1]["parent_receipt_id"] == receipts[0]["receipt_id"]
        assert receipts[2]["parent_receipt_id"] == receipts[1]["receipt_id"]

    def test_fail_also_writes_3_receipts(
        self, validator: GateV00ImageTypeValidator, tmp_receipt_dir: Path
    ) -> None:
        """Gate V-00 FAIL also writes 3 receipts with proper chain."""
        slides = [_make_slide(0, "tier_4_ai_ghibli")]
        vcb = _make_vcb(slides, content_format="carousel_dopamine_cliff")
        result = validator.validate(vcb)

        assert result.verdict == GateV00Verdict.GATE_V00_FAIL.value

        receipt_files = list(tmp_receipt_dir.glob("receipt_*.jsonl"))
        receipts = []
        for f in receipt_files:
            for line in f.read_text().strip().split("\n"):
                if line:
                    receipts.append(json.loads(line))

        assert len(receipts) == 3
        # Verdict receipt must record the FAIL decision
        verdict_receipt = [r for r in receipts if r["action"] == "GATE_V00_VERDICT"][0]
        assert verdict_receipt["decision"] == GateV00Verdict.GATE_V00_FAIL.value


# ─────────────────────────────────────────────────────
# SAFETY TESTS
# FR-VIS-13 §10 Safety Tests (ADR-01 Quarantine Security)
# ─────────────────────────────────────────────────────


class TestSafetyTests:
    """Safety tests per FR-VIS-13 §10."""

    def test_image_type_injection_attack(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """FR-VIS-13 §10: SQL injection in image_type → INVALID_IMAGE_TYPE."""
        slides = [
            _make_slide(0, "tier_3_ai_realistic; SELECT * FROM users"),
        ]
        vcb = _make_vcb(slides, content_format="carousel_dopamine_cliff")
        result = validator.validate(vcb)

        assert result.verdict == GateV00Verdict.GATE_V00_FAIL.value
        invalid = [
            v for v in result.violations
            if v.violation_type == ViolationType.INVALID_IMAGE_TYPE.value
        ]
        assert len(invalid) == 1

    def test_coach_acronym_validation(self) -> None:
        """ADR-01: coach_acronym must be 2-4 characters."""
        with pytest.raises(ValueError, match="coach_acronym must be 2-4 characters"):
            GateV00ImageTypeValidator(coach_acronym="X")

        with pytest.raises(ValueError, match="coach_acronym must be 2-4 characters"):
            GateV00ImageTypeValidator(coach_acronym="TOOLONG")

    def test_output_schema_conformance(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """FR-VIS-13 §5: output conforms to Gate_V00_Result.json schema."""
        slides = [_make_slide(0, "tier_3_ai_realistic")]
        vcb = _make_vcb(slides, content_format="carousel_dopamine_cliff")
        result = validator.validate(vcb)

        # Verify all required fields present
        result_dict = result.model_dump()
        required_fields = {
            "gate_id", "content_output_id", "content_format", "verdict",
            "revision_count", "violations", "slide_validation_summary",
            "format_envelope_id", "style_directive_id", "receipt_chain_block",
            "timestamp_utc",
        }
        for field in required_fields:
            assert field in result_dict, f"Missing required field: {field}"

    def test_c11_persona_masking_no_agent_names_in_output(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """C-11 Persona Masking: agent names must not appear in output payloads."""
        slides = [_make_slide(0, "tier_4_ai_ghibli")]
        vcb = _make_vcb(slides, content_format="carousel_dopamine_cliff")
        result = validator.validate(vcb)

        result_json = result.model_dump_json()
        # C-11: Abel, Paradoxe, Aurore, Sophia, etc. must not appear
        agent_names = [
            "Abel", "Paradoxe", "Aurore", "Sophia", "Marcus", "Chen",
            "Cesare", "Charlotte", "Dilaya", "Emmanuel", "Kimya",
            "Morgan", "Valeriane",
        ]
        for name in agent_names:
            assert name not in result_json, (
                f"C-11 violation: agent name '{name}' found in output payload"
            )


# ─────────────────────────────────────────────────────
# EDGE CASES
# ─────────────────────────────────────────────────────


class TestEdgeCases:
    """Edge cases and boundary conditions."""

    def test_single_slide_vcb(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """VCB with a single slide processes correctly."""
        slides = [_make_slide(0, "tier_3_ai_realistic")]
        vcb = _make_vcb(slides, content_format="single_tweet_quote")
        result = validator.validate(vcb)
        assert result.verdict == GateV00Verdict.GATE_V00_PASS.value
        assert len(result.slide_validation_summary) == 1

    def test_animated_gif_type_accepted(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """animated_gif is a valid image type."""
        slides = [_make_slide(0, "animated_gif")]
        vcb = _make_vcb(slides, content_format="single_tweet_quote")
        result = validator.validate(vcb)
        # Should pass extraction (valid type), may or may not pass style check
        extraction_violations = [
            v for v in result.violations
            if v.violation_type in {
                ViolationType.MISSING_IMAGE_TYPE.value,
                ViolationType.INVALID_IMAGE_TYPE.value,
            }
        ]
        assert len(extraction_violations) == 0

    def test_multiple_rules_same_slide(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """A single slide can trigger multiple rules (e.g. R01 + style conflict)."""
        slides = [_make_slide(0, "tier_4_ai_ghibli")]
        vcb = _make_vcb(
            slides,
            content_format="carousel_dopamine_cliff",
            prohibited_styles=["ghibli_illustration"],
        )
        result = validator.validate(vcb)

        assert result.verdict == GateV00Verdict.GATE_V00_FAIL.value
        # Should have both carousel ghibli AND style conflict
        violation_types = {v.violation_type for v in result.violations}
        assert ViolationType.CAROUSEL_GHIBLI_VIOLATION.value in violation_types
        assert ViolationType.STYLE_IMAGE_TYPE_CONFLICT.value in violation_types

    def test_result_timestamp_is_utc_iso8601(
        self, validator: GateV00ImageTypeValidator
    ) -> None:
        """Timestamp must be ISO 8601 UTC."""
        slides = [_make_slide(0, "tier_3_ai_realistic")]
        vcb = _make_vcb(slides, content_format="carousel_dopamine_cliff")
        result = validator.validate(vcb)
        # Should parse without error
        from datetime import datetime
        dt = datetime.fromisoformat(result.timestamp_utc)
        assert dt is not None
