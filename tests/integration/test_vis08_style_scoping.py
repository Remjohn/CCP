"""
FR-VIS-08 — Style Scoping — Integration Tests
Phase 2B, CVE Visual Engine — spec 3 of 13

Tests cover all 6 Acceptance Criteria (AC1-AC6) plus matrix completeness,
mutual exclusivity, mandatory consistency, saturation boundaries, seal
verification, directive tampering detection, legacy fallback, injection
resistance, and receipt chain integration from FR-VIS-08 §8 and §10.

Every test traces to an explicit AC or test case in the spec.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Optional

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.visual_engine_models import (
    FormatConstraintEnvelope,
    StyleConstraintDirective,
    StyleParameters,
    StyleScopeError,
    StyleScopeMatrixEntry,
    StyleValidationResult,
)
from src.ccp.services.style_scope_adapter import (
    DEFAULT_MATRIX_PATH,
    StyleScopeAdapter,
)


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
def adapter(receipt_chain: ReceiptChain) -> StyleScopeAdapter:
    """Create a StyleScopeAdapter for testing."""
    return StyleScopeAdapter(
        coach_acronym="TST",
        receipt_chain=receipt_chain,
        matrix_path=DEFAULT_MATRIX_PATH,
    )


def _make_envelope(
    content_format: str = "carousel_dopamine_cliff",
    envelope_id: str = "FCE-TST-001",
    total_slides: int = 1,
) -> FormatConstraintEnvelope:
    """Helper: create a FormatConstraintEnvelope with minimal required fields."""
    return FormatConstraintEnvelope(
        envelope_id=envelope_id,
        content_format=content_format,
        total_slides=total_slides,
    )


# ═════════════════════════════════════════════════════
# SECTION 1: MATRIX COMPLETENESS — FR-VIS-08 §10
# ═════════════════════════════════════════════════════


class TestMatrixCompleteness:
    """Verify the style_scope_matrix.json has all 15 entries and structural integrity."""

    def test_matrix_loads_15_formats(self, adapter: StyleScopeAdapter) -> None:
        """§10: Load matrix and assert all 15 format entries are present."""
        matrix = adapter.get_matrix()
        assert len(matrix) == 15, f"Expected 15 formats, got {len(matrix)}"

    def test_matrix_all_formats_present(self, adapter: StyleScopeAdapter) -> None:
        """§10: Assert every expected format key exists in the matrix."""
        expected_formats = {
            "carousel_dopamine_cliff",
            "carousel_listicle",
            "carousel_timeline",
            "carousel_comparison",
            "single_observational_humor",
            "single_observational_humor_square",
            "single_worst_case",
            "single_conceptual_contrast",
            "single_conceptual_contrast_simultaneous",
            "single_supervisual",
            "poll_archetypical",
            "poll_stereotypical",
            "poll_controversial_dilemma",
            "single_tweet_quote",
            "nine_grid_accumulation",
        }
        matrix = adapter.get_matrix()
        assert set(matrix.keys()) == expected_formats

    def test_matrix_all_entries_have_required_fields(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """§10: Every entry has non-null permitted_styles (≥1), prohibited_styles,
        mandatory_style (string or null), and style_parameters with grammar_system."""
        matrix = adapter.get_matrix()
        for fmt, entry in matrix.items():
            assert len(entry.permitted_styles) >= 1, (
                f"{fmt}: permitted_styles must have ≥1 entry"
            )
            assert isinstance(entry.prohibited_styles, list), (
                f"{fmt}: prohibited_styles must be a list"
            )
            assert entry.style_parameters is not None, (
                f"{fmt}: style_parameters must not be None"
            )
            assert entry.style_parameters.grammar_system in (
                "cinematic", "illustrated", "documentary", "hybrid"
            ), f"{fmt}: invalid grammar_system '{entry.style_parameters.grammar_system}'"


class TestMutualExclusivity:
    """§10: No style appears in both permitted_styles and prohibited_styles."""

    def test_no_overlap_between_permitted_and_prohibited(
        self, adapter: StyleScopeAdapter
    ) -> None:
        matrix = adapter.get_matrix()
        for fmt, entry in matrix.items():
            overlap = set(entry.permitted_styles) & set(entry.prohibited_styles)
            assert len(overlap) == 0, (
                f"{fmt}: styles {overlap} appear in both permitted and prohibited"
            )


class TestMandatoryConsistency:
    """§10: Mandatory style is in permitted_styles and absent from prohibited_styles."""

    def test_mandatory_in_permitted(self, adapter: StyleScopeAdapter) -> None:
        matrix = adapter.get_matrix()
        for fmt, entry in matrix.items():
            if entry.mandatory_style is not None:
                assert entry.mandatory_style in entry.permitted_styles, (
                    f"{fmt}: mandatory_style '{entry.mandatory_style}' not in permitted_styles"
                )

    def test_mandatory_not_in_prohibited(self, adapter: StyleScopeAdapter) -> None:
        matrix = adapter.get_matrix()
        for fmt, entry in matrix.items():
            if entry.mandatory_style is not None:
                assert entry.mandatory_style not in entry.prohibited_styles, (
                    f"{fmt}: mandatory_style '{entry.mandatory_style}' found in prohibited_styles"
                )


# ═════════════════════════════════════════════════════
# SECTION 2: AC1 — CAROUSEL GHIBLI PROHIBITION
# FR-VIS-08 §8 AC1
# ═════════════════════════════════════════════════════


class TestAC1CarouselGhibliProhibition:
    """AC1: Carousel formats must reject Ghibli illustration."""

    def test_carousel_dopamine_cliff_ghibli_rejected(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """AC1 primary: carousel_dopamine_cliff + ghibli_illustration → STYLE_VIOLATION."""
        env = _make_envelope("carousel_dopamine_cliff")
        directive, error, warnings = adapter.scope(env, "CO-TST-AC1-001")
        assert directive is not None
        assert error is None

        result = adapter.validate_style_assignment(
            directive, "ghibli_illustration"
        )
        assert result.valid is False
        assert result.error_type == StyleScopeError.STYLE_VIOLATION.value
        assert "ghibli_illustration" in (result.error_detail or "")
        assert "prohibited" in (result.error_detail or "").lower()

    def test_carousel_dopamine_cliff_cinematic_accepted(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """AC1 inverse: carousel_dopamine_cliff + cinematic_color_graded → accepted."""
        env = _make_envelope("carousel_dopamine_cliff")
        directive, error, warnings = adapter.scope(env, "CO-TST-AC1-002")
        assert directive is not None
        result = adapter.validate_style_assignment(
            directive, "cinematic_color_graded"
        )
        assert result.valid is True

    def test_carousel_dopamine_cliff_semi_realistic_accepted(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """AC1: carousel_dopamine_cliff + semi_realistic_digital → accepted."""
        env = _make_envelope("carousel_dopamine_cliff")
        directive, error, _ = adapter.scope(env, "CO-TST-AC1-003")
        assert directive is not None
        result = adapter.validate_style_assignment(
            directive, "semi_realistic_digital"
        )
        assert result.valid is True

    @pytest.mark.parametrize("carousel_format", [
        "carousel_listicle",
        "carousel_timeline",
        "carousel_comparison",
    ])
    def test_all_carousel_formats_reject_ghibli(
        self, adapter: StyleScopeAdapter, carousel_format: str
    ) -> None:
        """AC1 extension: all carousel formats prohibit ghibli."""
        env = _make_envelope(carousel_format)
        directive, error, _ = adapter.scope(env, f"CO-TST-AC1-{carousel_format}")
        assert directive is not None
        result = adapter.validate_style_assignment(
            directive, "ghibli_illustration"
        )
        assert result.valid is False
        assert result.error_type == StyleScopeError.STYLE_VIOLATION.value

    def test_ac1_error_message_includes_permitted_alternatives(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """AC1 §8: error must include permitted alternatives."""
        env = _make_envelope("carousel_dopamine_cliff")
        directive, _, _ = adapter.scope(env, "CO-TST-AC1-MSG")
        assert directive is not None
        result = adapter.validate_style_assignment(
            directive, "ghibli_illustration"
        )
        assert "cinematic_color_graded" in (result.error_detail or "")
        assert "semi_realistic_digital" in (result.error_detail or "")


# ═════════════════════════════════════════════════════
# SECTION 3: AC2 — OBSERVATIONAL HUMOR REAL-ONLY MANDATE
# FR-VIS-08 §8 AC2
# ═════════════════════════════════════════════════════


class TestAC2ObsHumorRealOnlyMandate:
    """AC2: Observational Humor must use real_photography_only with documentary grammar."""

    def test_obs_humor_directive_mandatory_real_photography(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """AC2: directive has mandatory_style: 'real_photography_only'."""
        env = _make_envelope("single_observational_humor")
        directive, error, _ = adapter.scope(env, "CO-TST-AC2-001")
        assert directive is not None
        assert error is None
        assert directive.mandatory_style == "real_photography_only"

    def test_obs_humor_directive_grammar_documentary(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """AC2: grammar_system must be 'documentary'."""
        env = _make_envelope("single_observational_humor")
        directive, _, _ = adapter.scope(env, "CO-TST-AC2-002")
        assert directive is not None
        assert directive.grammar_system == "documentary"

    def test_obs_humor_semi_realistic_rejected(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """AC2 primary: semi_realistic_digital → STYLE_VIOLATION."""
        env = _make_envelope("single_observational_humor")
        directive, _, _ = adapter.scope(env, "CO-TST-AC2-003")
        assert directive is not None
        result = adapter.validate_style_assignment(
            directive, "semi_realistic_digital"
        )
        assert result.valid is False
        assert result.error_type == StyleScopeError.STYLE_VIOLATION.value
        assert "mandatory" in (result.error_detail or "").lower()
        assert "real_photography_only" in (result.error_detail or "")

    def test_obs_humor_real_photography_accepted(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """AC2: real_photography_only → accepted."""
        env = _make_envelope("single_observational_humor")
        directive, _, _ = adapter.scope(env, "CO-TST-AC2-004")
        assert directive is not None
        result = adapter.validate_style_assignment(
            directive, "real_photography_only"
        )
        assert result.valid is True

    def test_obs_humor_square_same_mandate(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """AC2 extension: square variant has same real-only mandate."""
        env = _make_envelope("single_observational_humor_square")
        directive, _, _ = adapter.scope(env, "CO-TST-AC2-005")
        assert directive is not None
        assert directive.mandatory_style == "real_photography_only"
        assert directive.grammar_system == "documentary"

    def test_obs_humor_cinematic_rejected(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """AC2: cinematic_color_graded → STYLE_VIOLATION (mandatory is real_photography_only)."""
        env = _make_envelope("single_observational_humor")
        directive, _, _ = adapter.scope(env, "CO-TST-AC2-006")
        assert directive is not None
        result = adapter.validate_style_assignment(
            directive, "cinematic_color_graded"
        )
        assert result.valid is False


# ═════════════════════════════════════════════════════
# SECTION 4: AC3 — WORST CASE SATURATION CEILING
# FR-VIS-08 §8 AC3
# ═════════════════════════════════════════════════════


class TestAC3WorstCaseSaturationCeiling:
    """AC3: single_worst_case has saturation floor=20, ceiling=35."""

    def test_worst_case_saturation_55_rejected(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """AC3 primary: saturation_pct=55 → SATURATION_VIOLATION."""
        env = _make_envelope("single_worst_case")
        directive, _, _ = adapter.scope(env, "CO-TST-AC3-001")
        assert directive is not None
        assert directive.saturation_ceiling_pct == 35
        assert directive.saturation_floor_pct == 20

        result = adapter.validate_style_assignment(
            directive, "cinematic_color_graded", saturation_pct=55
        )
        assert result.valid is False
        assert result.error_type == StyleScopeError.SATURATION_VIOLATION.value
        assert "35%" in (result.error_detail or "")
        assert "55%" in (result.error_detail or "")

    def test_worst_case_saturation_28_accepted(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """AC3 primary: saturation_pct=28 → accepted (between 20 and 35)."""
        env = _make_envelope("single_worst_case")
        directive, _, _ = adapter.scope(env, "CO-TST-AC3-002")
        assert directive is not None
        result = adapter.validate_style_assignment(
            directive, "cinematic_color_graded", saturation_pct=28
        )
        assert result.valid is True

    def test_worst_case_saturation_boundary_20_accepted(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """§10 boundary: saturation_pct=20 → accepted (at floor)."""
        env = _make_envelope("single_worst_case")
        directive, _, _ = adapter.scope(env, "CO-TST-AC3-003")
        assert directive is not None
        result = adapter.validate_style_assignment(
            directive, "cinematic_color_graded", saturation_pct=20
        )
        assert result.valid is True

    def test_worst_case_saturation_boundary_35_accepted(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """§10 boundary: saturation_pct=35 → accepted (at ceiling)."""
        env = _make_envelope("single_worst_case")
        directive, _, _ = adapter.scope(env, "CO-TST-AC3-004")
        assert directive is not None
        result = adapter.validate_style_assignment(
            directive, "cinematic_color_graded", saturation_pct=35
        )
        assert result.valid is True

    def test_worst_case_saturation_boundary_19_rejected(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """§10 boundary: saturation_pct=19 → rejected (below floor)."""
        env = _make_envelope("single_worst_case")
        directive, _, _ = adapter.scope(env, "CO-TST-AC3-005")
        assert directive is not None
        result = adapter.validate_style_assignment(
            directive, "cinematic_color_graded", saturation_pct=19
        )
        assert result.valid is False
        assert result.error_type == StyleScopeError.SATURATION_VIOLATION.value
        assert "20%" in (result.error_detail or "")

    def test_worst_case_saturation_boundary_36_rejected(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """§10 boundary: saturation_pct=36 → rejected (above ceiling)."""
        env = _make_envelope("single_worst_case")
        directive, _, _ = adapter.scope(env, "CO-TST-AC3-006")
        assert directive is not None
        result = adapter.validate_style_assignment(
            directive, "cinematic_color_graded", saturation_pct=36
        )
        assert result.valid is False
        assert result.error_type == StyleScopeError.SATURATION_VIOLATION.value
        assert "35%" in (result.error_detail or "")

    def test_worst_case_mandatory_style_cinematic(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """AC3 extension: worst case has mandatory_style=cinematic_color_graded."""
        env = _make_envelope("single_worst_case")
        directive, _, _ = adapter.scope(env, "CO-TST-AC3-007")
        assert directive is not None
        assert directive.mandatory_style == "cinematic_color_graded"

    def test_worst_case_no_saturation_provided_accepts(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """If saturation_pct is not provided, saturation check is skipped."""
        env = _make_envelope("single_worst_case")
        directive, _, _ = adapter.scope(env, "CO-TST-AC3-008")
        assert directive is not None
        result = adapter.validate_style_assignment(
            directive, "cinematic_color_graded"
        )
        assert result.valid is True


# ═════════════════════════════════════════════════════
# SECTION 5: AC4 — CONCEPTUAL CONTRAST GHIBLI PERMISSION
# FR-VIS-08 §8 AC4
# ═════════════════════════════════════════════════════


class TestAC4ConceptualContrastGhibliPermission:
    """AC4: single_conceptual_contrast permits ghibli_illustration."""

    def test_conceptual_contrast_ghibli_accepted(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """AC4 primary: ghibli_illustration → accepted."""
        env = _make_envelope("single_conceptual_contrast")
        directive, _, _ = adapter.scope(env, "CO-TST-AC4-001")
        assert directive is not None
        assert "ghibli_illustration" in directive.permitted_styles
        result = adapter.validate_style_assignment(
            directive, "ghibli_illustration"
        )
        assert result.valid is True

    def test_conceptual_contrast_cinematic_accepted(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """AC4: cinematic_color_graded also accepted."""
        env = _make_envelope("single_conceptual_contrast")
        directive, _, _ = adapter.scope(env, "CO-TST-AC4-002")
        assert directive is not None
        result = adapter.validate_style_assignment(
            directive, "cinematic_color_graded"
        )
        assert result.valid is True

    def test_conceptual_contrast_semi_realistic_accepted(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """AC4: semi_realistic_digital also accepted."""
        env = _make_envelope("single_conceptual_contrast")
        directive, _, _ = adapter.scope(env, "CO-TST-AC4-003")
        assert directive is not None
        result = adapter.validate_style_assignment(
            directive, "semi_realistic_digital"
        )
        assert result.valid is True

    def test_conceptual_contrast_watercolor_rejected(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """AC4: watercolor is prohibited for conceptual contrast."""
        env = _make_envelope("single_conceptual_contrast")
        directive, _, _ = adapter.scope(env, "CO-TST-AC4-004")
        assert directive is not None
        result = adapter.validate_style_assignment(
            directive, "watercolor"
        )
        assert result.valid is False

    def test_conceptual_contrast_grammar_hybrid(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """AC4 extension: grammar_system must be 'hybrid'."""
        env = _make_envelope("single_conceptual_contrast")
        directive, _, _ = adapter.scope(env, "CO-TST-AC4-005")
        assert directive is not None
        assert directive.grammar_system == "hybrid"

    def test_conceptual_contrast_simultaneous_also_permits_ghibli(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """AC4 extension: simultaneous variant also permits ghibli."""
        env = _make_envelope("single_conceptual_contrast_simultaneous")
        directive, _, _ = adapter.scope(env, "CO-TST-AC4-006")
        assert directive is not None
        assert "ghibli_illustration" in directive.permitted_styles
        result = adapter.validate_style_assignment(
            directive, "ghibli_illustration"
        )
        assert result.valid is True


# ═════════════════════════════════════════════════════
# SECTION 6: AC5 — GRAMMAR SYSTEM ROUTING
# FR-VIS-08 §8 AC5
# ═════════════════════════════════════════════════════


class TestAC5GrammarSystemRouting:
    """AC5: Correct grammar_system emitted for each format class."""

    def test_obs_humor_grammar_documentary(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """AC5: single_observational_humor → grammar_system: 'documentary'."""
        env = _make_envelope("single_observational_humor")
        directive, _, _ = adapter.scope(env, "CO-TST-AC5-001")
        assert directive is not None
        assert directive.grammar_system == "documentary"

    def test_carousel_grammar_cinematic(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """AC5: carousel_dopamine_cliff → grammar_system: 'cinematic'."""
        env = _make_envelope("carousel_dopamine_cliff")
        directive, _, _ = adapter.scope(env, "CO-TST-AC5-002")
        assert directive is not None
        assert directive.grammar_system == "cinematic"

    def test_supervisual_grammar_hybrid(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """AC5: single_supervisual → grammar_system: 'hybrid'."""
        env = _make_envelope("single_supervisual")
        directive, _, _ = adapter.scope(env, "CO-TST-AC5-003")
        assert directive is not None
        assert directive.grammar_system == "hybrid"

    @pytest.mark.parametrize("carousel_format", [
        "carousel_dopamine_cliff",
        "carousel_listicle",
        "carousel_timeline",
        "carousel_comparison",
    ])
    def test_all_carousels_emit_cinematic(
        self, adapter: StyleScopeAdapter, carousel_format: str
    ) -> None:
        """AC5 extension: all carousel formats → cinematic grammar."""
        env = _make_envelope(carousel_format)
        directive, _, _ = adapter.scope(env, f"CO-TST-AC5-{carousel_format}")
        assert directive is not None
        assert directive.grammar_system == "cinematic"

    @pytest.mark.parametrize("poll_format", [
        "poll_archetypical",
        "poll_stereotypical",
        "poll_controversial_dilemma",
    ])
    def test_all_polls_emit_cinematic(
        self, adapter: StyleScopeAdapter, poll_format: str
    ) -> None:
        """AC5 extension: all poll formats → cinematic grammar."""
        env = _make_envelope(poll_format)
        directive, _, _ = adapter.scope(env, f"CO-TST-AC5-{poll_format}")
        assert directive is not None
        assert directive.grammar_system == "cinematic"


# ═════════════════════════════════════════════════════
# SECTION 7: AC6 — POLL STYLE CONSTRAINT
# FR-VIS-08 §8 AC6
# ═════════════════════════════════════════════════════


class TestAC6PollStyleConstraint:
    """AC6: Poll formats permit semi_realistic_digital and vector_flat,
    prohibit real_photography_only and ghibli_illustration."""

    def test_poll_archetypical_permitted_styles(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """AC6 primary: permitted includes semi_realistic_digital and vector_flat."""
        env = _make_envelope("poll_archetypical")
        directive, _, _ = adapter.scope(env, "CO-TST-AC6-001")
        assert directive is not None
        assert "semi_realistic_digital" in directive.permitted_styles
        assert "vector_flat" in directive.permitted_styles

    def test_poll_archetypical_prohibited_styles(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """AC6 primary: prohibited includes real_photography_only and ghibli_illustration."""
        env = _make_envelope("poll_archetypical")
        directive, _, _ = adapter.scope(env, "CO-TST-AC6-002")
        assert directive is not None
        assert "real_photography_only" in directive.prohibited_styles
        assert "ghibli_illustration" in directive.prohibited_styles

    def test_poll_semi_realistic_accepted(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """AC6: semi_realistic_digital → accepted."""
        env = _make_envelope("poll_archetypical")
        directive, _, _ = adapter.scope(env, "CO-TST-AC6-003")
        assert directive is not None
        result = adapter.validate_style_assignment(
            directive, "semi_realistic_digital"
        )
        assert result.valid is True

    def test_poll_vector_flat_accepted(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """AC6: vector_flat → accepted."""
        env = _make_envelope("poll_archetypical")
        directive, _, _ = adapter.scope(env, "CO-TST-AC6-004")
        assert directive is not None
        result = adapter.validate_style_assignment(
            directive, "vector_flat"
        )
        assert result.valid is True

    def test_poll_ghibli_rejected(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """AC6: ghibli_illustration → rejected."""
        env = _make_envelope("poll_archetypical")
        directive, _, _ = adapter.scope(env, "CO-TST-AC6-005")
        assert directive is not None
        result = adapter.validate_style_assignment(
            directive, "ghibli_illustration"
        )
        assert result.valid is False
        assert result.error_type == StyleScopeError.STYLE_VIOLATION.value

    def test_poll_real_photography_rejected(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """AC6: real_photography_only → rejected."""
        env = _make_envelope("poll_archetypical")
        directive, _, _ = adapter.scope(env, "CO-TST-AC6-006")
        assert directive is not None
        result = adapter.validate_style_assignment(
            directive, "real_photography_only"
        )
        assert result.valid is False

    @pytest.mark.parametrize("poll_format", [
        "poll_stereotypical",
        "poll_controversial_dilemma",
    ])
    def test_other_poll_formats_same_constraints(
        self, adapter: StyleScopeAdapter, poll_format: str
    ) -> None:
        """AC6 extension: all poll variants share the same style constraints."""
        env = _make_envelope(poll_format)
        directive, _, _ = adapter.scope(env, f"CO-TST-AC6-{poll_format}")
        assert directive is not None
        assert "semi_realistic_digital" in directive.permitted_styles
        assert "vector_flat" in directive.permitted_styles
        assert "ghibli_illustration" in directive.prohibited_styles
        assert "real_photography_only" in directive.prohibited_styles


# ═════════════════════════════════════════════════════
# SECTION 8: SEAL VERIFICATION & DIRECTIVE ASSEMBLY
# ═════════════════════════════════════════════════════


class TestSealVerification:
    """Directive SHA-256 seal integrity per FR-VIS-08 §4 Stage 2."""

    def test_directive_has_seal_hash(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """Sealed directive must have a non-None seal_hash."""
        env = _make_envelope("carousel_dopamine_cliff")
        directive, _, _ = adapter.scope(env, "CO-TST-SEAL-001")
        assert directive is not None
        assert directive.seal_hash is not None
        assert len(directive.seal_hash) == 64  # SHA-256 hex

    def test_seal_verifies_on_untampered_directive(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """Untampered directive passes seal verification."""
        env = _make_envelope("carousel_dopamine_cliff")
        directive, _, _ = adapter.scope(env, "CO-TST-SEAL-002")
        assert directive is not None
        assert StyleScopeAdapter.verify_seal(directive) is True

    def test_seal_fails_on_tampered_permitted_styles(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """§10 Safety: Adding to permitted_styles after sealing → seal mismatch."""
        env = _make_envelope("carousel_dopamine_cliff")
        directive, _, _ = adapter.scope(env, "CO-TST-SEAL-003")
        assert directive is not None
        # Tamper: add ghibli to permitted_styles
        directive.permitted_styles.append("ghibli_illustration")
        assert StyleScopeAdapter.verify_seal(directive) is False

    def test_seal_fails_on_tampered_grammar_system(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """Changing grammar_system after sealing → seal mismatch."""
        env = _make_envelope("carousel_dopamine_cliff")
        directive, _, _ = adapter.scope(env, "CO-TST-SEAL-004")
        assert directive is not None
        directive.grammar_system = "illustrated"
        assert StyleScopeAdapter.verify_seal(directive) is False

    def test_seal_deterministic_same_input(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """Same format + same content_output_id → different directive IDs but
        seal re-computation is valid for each."""
        env = _make_envelope("single_worst_case")
        d1, _, _ = adapter.scope(env, "CO-TST-SEAL-DET-001")
        d2, _, _ = adapter.scope(env, "CO-TST-SEAL-DET-002")
        assert d1 is not None and d2 is not None
        assert StyleScopeAdapter.verify_seal(d1) is True
        assert StyleScopeAdapter.verify_seal(d2) is True

    def test_seal_none_returns_false(self) -> None:
        """A directive with seal_hash=None fails verification."""
        directive = StyleConstraintDirective(
            permitted_styles=["cinematic_color_graded"],
            seal_hash=None,
        )
        assert StyleScopeAdapter.verify_seal(directive) is False


# ═════════════════════════════════════════════════════
# SECTION 9: LEGACY FALLBACK — FR-VIS-08 §6
# ═════════════════════════════════════════════════════


class TestLegacyFallback:
    """§6: Unresolved formats get conservative default with LEGACY_STYLE_DEFAULT warning."""

    def test_legacy_carousel_unknown_subtype(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """§6.1: Unresolved carousel format → conservative carousel default."""
        env = _make_envelope("carousel_unknown_subtype")
        directive, error, warnings = adapter.scope(env, "CO-TST-LEGACY-001")
        assert directive is not None
        assert error is None
        assert len(warnings) == 1
        assert "LEGACY_STYLE_DEFAULT" in warnings[0]
        assert "carousel_unknown_subtype" in warnings[0]
        # Conservative: cinematic + semi-realistic permitted, no ghibli/real
        assert "cinematic_color_graded" in directive.permitted_styles
        assert "semi_realistic_digital" in directive.permitted_styles
        assert "ghibli_illustration" in directive.prohibited_styles
        assert "real_photography_only" in directive.prohibited_styles

    def test_legacy_single_unknown_subtype(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """§6.2: Unresolved single format → conservative single default."""
        env = _make_envelope("single_unknown_subtype")
        directive, error, warnings = adapter.scope(env, "CO-TST-LEGACY-002")
        assert directive is not None
        assert error is None
        assert len(warnings) == 1
        assert "LEGACY_STYLE_DEFAULT" in warnings[0]
        assert "cinematic_color_graded" in directive.permitted_styles

    def test_legacy_poll_unknown_subtype(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """§6.2: Unresolved poll format → conservative default (treated as single/default)."""
        env = _make_envelope("poll_unknown_subtype")
        directive, error, warnings = adapter.scope(env, "CO-TST-LEGACY-003")
        assert directive is not None
        assert error is None
        assert len(warnings) == 1
        assert "LEGACY_STYLE_DEFAULT" in warnings[0]

    def test_completely_unrecognized_format(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """§6: Truly unrecognized format prefix → None directive, error."""
        env = _make_envelope("video_reel_something")
        directive, error, warnings = adapter.scope(env, "CO-TST-LEGACY-004")
        assert directive is None
        assert error == StyleScopeError.FORMAT_NOT_IN_MATRIX.value

    def test_legacy_default_excludes_ghibli_and_real(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """§6.4: Conservative default never includes real_photography_only or ghibli."""
        env = _make_envelope("carousel_brand_new")
        directive, _, warnings = adapter.scope(env, "CO-TST-LEGACY-005")
        assert directive is not None
        assert "ghibli_illustration" not in directive.permitted_styles
        assert "real_photography_only" not in directive.permitted_styles
        assert "ghibli_illustration" in directive.prohibited_styles
        assert "real_photography_only" in directive.prohibited_styles


# ═════════════════════════════════════════════════════
# SECTION 10: SAFETY TESTS — FR-VIS-08 §10
# ═════════════════════════════════════════════════════


class TestSafetyInjectionResistance:
    """§10 Safety: Style injection resistance."""

    def test_sql_injection_in_style_name(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """§10: Injected SQL in visual_style → treated as single string lookup, rejected."""
        env = _make_envelope("carousel_dopamine_cliff")
        directive, _, _ = adapter.scope(env, "CO-TST-SAFE-001")
        assert directive is not None
        malicious_style = "ghibli_illustration'; DROP TABLE styles;"
        result = adapter.validate_style_assignment(directive, malicious_style)
        assert result.valid is False
        assert result.error_type == StyleScopeError.STYLE_VIOLATION.value

    def test_empty_style_name_rejected(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """Empty string is not in any permitted_styles."""
        env = _make_envelope("carousel_dopamine_cliff")
        directive, _, _ = adapter.scope(env, "CO-TST-SAFE-002")
        assert directive is not None
        result = adapter.validate_style_assignment(directive, "")
        assert result.valid is False

    def test_whitespace_style_name_rejected(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """Whitespace-only style is not in any permitted_styles."""
        env = _make_envelope("carousel_dopamine_cliff")
        directive, _, _ = adapter.scope(env, "CO-TST-SAFE-003")
        assert directive is not None
        result = adapter.validate_style_assignment(directive, "   ")
        assert result.valid is False


class TestDirectiveTamperingDetection:
    """§10 Safety: Directive tampering detection via seal hash."""

    def test_tampering_detected_adding_style(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """§10: Add ghibli to permitted_styles → seal mismatch detected."""
        env = _make_envelope("carousel_dopamine_cliff")
        directive, _, _ = adapter.scope(env, "CO-TST-TAMP-001")
        assert directive is not None
        original_seal = directive.seal_hash
        directive.permitted_styles.append("ghibli_illustration")
        assert StyleScopeAdapter.verify_seal(directive) is False
        assert directive.seal_hash == original_seal  # hash wasn't updated

    def test_tampering_detected_removing_prohibited(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """§10: Removing a prohibited style → seal mismatch."""
        env = _make_envelope("carousel_dopamine_cliff")
        directive, _, _ = adapter.scope(env, "CO-TST-TAMP-002")
        assert directive is not None
        directive.prohibited_styles.remove("ghibli_illustration")
        assert StyleScopeAdapter.verify_seal(directive) is False

    def test_tampering_detected_changing_mandatory(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """§10: Changing mandatory_style → seal mismatch."""
        env = _make_envelope("single_observational_humor")
        directive, _, _ = adapter.scope(env, "CO-TST-TAMP-003")
        assert directive is not None
        directive.mandatory_style = "ghibli_illustration"
        assert StyleScopeAdapter.verify_seal(directive) is False

    def test_tampering_detected_changing_saturation(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """§10: Changing saturation ceiling → seal mismatch."""
        env = _make_envelope("single_worst_case")
        directive, _, _ = adapter.scope(env, "CO-TST-TAMP-004")
        assert directive is not None
        directive.saturation_ceiling_pct = 100
        assert StyleScopeAdapter.verify_seal(directive) is False


# ═════════════════════════════════════════════════════
# SECTION 11: RECEIPT CHAIN INTEGRATION
# ═════════════════════════════════════════════════════


class TestReceiptChainIntegration:
    """Receipt chain writes per DEP-ENG-041."""

    def test_scope_writes_two_receipts(
        self, adapter: StyleScopeAdapter, receipt_chain: ReceiptChain
    ) -> None:
        """scope() writes Stage 1 (matrix eval) + Stage 2 (directive assembly) receipts."""
        initial_count = receipt_chain.chain_length()
        env = _make_envelope("carousel_dopamine_cliff")
        directive, _, _ = adapter.scope(env, "CO-TST-RCH-001")
        assert directive is not None
        assert receipt_chain.chain_length() == initial_count + 2

    def test_validate_writes_receipt(
        self, adapter: StyleScopeAdapter, receipt_chain: ReceiptChain
    ) -> None:
        """validate_style_assignment() writes a Stage 3 receipt."""
        env = _make_envelope("carousel_dopamine_cliff")
        directive, _, _ = adapter.scope(env, "CO-TST-RCH-002")
        assert directive is not None
        count_before = receipt_chain.chain_length()
        adapter.validate_style_assignment(directive, "cinematic_color_graded")
        assert receipt_chain.chain_length() == count_before + 1

    def test_directive_has_receipt_chain_block(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """Directive receipt_chain_block populated after scope()."""
        env = _make_envelope("carousel_dopamine_cliff")
        directive, _, _ = adapter.scope(env, "CO-TST-RCH-003")
        assert directive is not None
        assert directive.receipt_chain_block is not None
        assert len(directive.receipt_chain_block) > 0

    def test_receipt_entries_contain_action_names(
        self, adapter: StyleScopeAdapter, receipt_chain: ReceiptChain
    ) -> None:
        """Receipt entries reference VIS08 stage action names."""
        env = _make_envelope("single_supervisual")
        directive, _, _ = adapter.scope(env, "CO-TST-RCH-004")
        assert directive is not None
        adapter.validate_style_assignment(directive, "ghibli_illustration")
        all_entries = receipt_chain.query(agent_id="style_scope_adapter", limit=100)
        actions = [e.action for e in all_entries]
        assert "VIS08_STYLE_MATRIX_EVAL" in actions
        assert "VIS08_DIRECTIVE_ASSEMBLY" in actions
        assert "VIS08_PRE_ABEL_VALIDATION" in actions


# ═════════════════════════════════════════════════════
# SECTION 12: DIRECTIVE FIELD COMPLETENESS
# ═════════════════════════════════════════════════════


class TestDirectiveFieldCompleteness:
    """Verify all directive fields are correctly populated."""

    def test_directive_has_content_format(
        self, adapter: StyleScopeAdapter
    ) -> None:
        env = _make_envelope("single_tweet_quote")
        directive, _, _ = adapter.scope(env, "CO-TST-FIELD-001")
        assert directive is not None
        assert directive.content_format == "single_tweet_quote"

    def test_directive_has_content_output_id(
        self, adapter: StyleScopeAdapter
    ) -> None:
        env = _make_envelope("single_tweet_quote")
        directive, _, _ = adapter.scope(env, "CO-TST-FIELD-002")
        assert directive is not None
        assert directive.content_output_id == "CO-TST-FIELD-002"

    def test_directive_has_format_constraint_envelope_id(
        self, adapter: StyleScopeAdapter
    ) -> None:
        env = _make_envelope("nine_grid_accumulation", envelope_id="FCE-TEST-99")
        directive, _, _ = adapter.scope(env, "CO-TST-FIELD-003")
        assert directive is not None
        assert directive.format_constraint_envelope_id == "FCE-TEST-99"

    def test_directive_has_timestamp_utc(
        self, adapter: StyleScopeAdapter
    ) -> None:
        env = _make_envelope("carousel_dopamine_cliff")
        directive, _, _ = adapter.scope(env, "CO-TST-FIELD-004")
        assert directive is not None
        assert directive.timestamp_utc is not None
        assert len(directive.timestamp_utc) > 0

    def test_directive_has_unique_id(
        self, adapter: StyleScopeAdapter
    ) -> None:
        env = _make_envelope("carousel_dopamine_cliff")
        d1, _, _ = adapter.scope(env, "CO-TST-FIELD-005A")
        d2, _, _ = adapter.scope(env, "CO-TST-FIELD-005B")
        assert d1 is not None and d2 is not None
        assert d1.directive_id != d2.directive_id


# ═════════════════════════════════════════════════════
# SECTION 13: FULL PIPELINE INTEGRATION — FR-VIS-08 §10
# ═════════════════════════════════════════════════════


class TestFullPipelineIntegration:
    """§10 Integration: Complete scope → validate flows."""

    def test_carousel_comparison_full_flow(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """§10: carousel_comparison → cinematic grammar → cinematic accepted → ghibli rejected."""
        env = _make_envelope("carousel_comparison")
        directive, error, _ = adapter.scope(env, "CO-TST-FP-001")
        assert directive is not None
        assert error is None
        assert directive.grammar_system == "cinematic"

        # Cinematic accepted
        result_ok = adapter.validate_style_assignment(
            directive, "cinematic_color_graded"
        )
        assert result_ok.valid is True

        # Ghibli rejected
        result_fail = adapter.validate_style_assignment(
            directive, "ghibli_illustration"
        )
        assert result_fail.valid is False

    def test_supervisual_ghibli_full_flow(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """§10: single_supervisual → hybrid grammar → ghibli accepted."""
        env = _make_envelope("single_supervisual")
        directive, _, _ = adapter.scope(env, "CO-TST-FP-002")
        assert directive is not None
        assert directive.grammar_system == "hybrid"
        result = adapter.validate_style_assignment(
            directive, "ghibli_illustration"
        )
        assert result.valid is True

    def test_tweet_quote_cinematic_flow(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """single_tweet_quote → cinematic grammar → cinematic accepted."""
        env = _make_envelope("single_tweet_quote")
        directive, _, _ = adapter.scope(env, "CO-TST-FP-003")
        assert directive is not None
        assert directive.grammar_system == "cinematic"
        result = adapter.validate_style_assignment(
            directive, "cinematic_color_graded"
        )
        assert result.valid is True

    def test_nine_grid_flow(
        self, adapter: StyleScopeAdapter
    ) -> None:
        """nine_grid_accumulation → cinematic grammar → cinematic/semi_realistic accepted."""
        env = _make_envelope("nine_grid_accumulation")
        directive, _, _ = adapter.scope(env, "CO-TST-FP-004")
        assert directive is not None
        assert directive.grammar_system == "cinematic"
        assert adapter.validate_style_assignment(
            directive, "cinematic_color_graded"
        ).valid is True
        assert adapter.validate_style_assignment(
            directive, "semi_realistic_digital"
        ).valid is True
        assert adapter.validate_style_assignment(
            directive, "ghibli_illustration"
        ).valid is False


# ═════════════════════════════════════════════════════
# SECTION 14: ADR-01 COACH ACRONYM ENFORCEMENT
# ═════════════════════════════════════════════════════


class TestADR01CoachAcronym:
    """ADR-01: coach_acronym must be 2-4 characters."""

    def test_valid_2_char_acronym(
        self, receipt_chain: ReceiptChain
    ) -> None:
        adapter = StyleScopeAdapter(
            coach_acronym="JP", receipt_chain=receipt_chain
        )
        assert adapter.coach_acronym == "JP"

    def test_valid_4_char_acronym(
        self, receipt_chain: ReceiptChain
    ) -> None:
        adapter = StyleScopeAdapter(
            coach_acronym="JPGR", receipt_chain=receipt_chain
        )
        assert adapter.coach_acronym == "JPGR"

    def test_1_char_acronym_rejected(
        self, receipt_chain: ReceiptChain
    ) -> None:
        with pytest.raises(ValueError, match="2-4 characters"):
            StyleScopeAdapter(
                coach_acronym="J", receipt_chain=receipt_chain
            )

    def test_5_char_acronym_rejected(
        self, receipt_chain: ReceiptChain
    ) -> None:
        with pytest.raises(ValueError, match="2-4 characters"):
            StyleScopeAdapter(
                coach_acronym="JPGRS", receipt_chain=receipt_chain
            )
