"""
FR-VIS-07 — Format & Aspect Ratio Enforcement — Integration Tests
Phase 2B, CVE Visual Engine — spec 2 of 13

Tests cover all 6 Acceptance Criteria (AC1-AC6) plus registry completeness,
envelope assembly, hash determinism, and safety tests from FR-VIS-07 §8 and §10.

Every test traces to an explicit AC or test case in the spec.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.visual_engine_models import (
    ContentOutputInput,
    FormatAdapterError,
    FormatAdapterResult,
    FormatConstraintEnvelope,
    FormatRegistryEntry,
    PerSlideDimension,
    RECIPE_ID_TO_FORMAT,
)
from src.ccp.services.visual_format_constraint_adapter import (
    DEFAULT_REGISTRY_PATH,
    VisualFormatConstraintAdapter,
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
def adapter(receipt_chain: ReceiptChain) -> VisualFormatConstraintAdapter:
    """Create a VisualFormatConstraintAdapter for testing."""
    return VisualFormatConstraintAdapter(
        coach_acronym="TST",
        receipt_chain=receipt_chain,
        registry_path=DEFAULT_REGISTRY_PATH,
    )


def _make_input(
    content_format: str | None = "carousel_dopamine_cliff",
    slide_count: int = 7,
    recipe_id: str | None = None,
    content_output_id: str = "CO-TST-001",
) -> ContentOutputInput:
    """Helper: create a ContentOutputInput for testing."""
    return ContentOutputInput(
        content_output_id=content_output_id,
        content_format=content_format,
        slide_count=slide_count,
        recipe_id=recipe_id,
        coach_acronym="TST",
    )


# ─────────────────────────────────────────────────────
# REGISTRY COMPLETENESS TESTS
# FR-VIS-07 §10 Unit Tests
# ─────────────────────────────────────────────────────


class TestRegistryCompleteness:
    """FR-VIS-07 §10: Load registry and assert all entries are valid."""

    def test_registry_has_15_formats(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """FR-VIS-07 §5: exactly 15 format entries in registry."""
        registry = adapter.get_registry()
        assert len(registry) == 15

    def test_all_entries_have_required_fields(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """FR-VIS-07 §10 Unit Test: every entry has non-null required fields."""
        registry = adapter.get_registry()
        for format_name, entry in registry.items():
            assert entry.width_px > 0, f"{format_name} missing width_px"
            assert entry.height_px > 0, f"{format_name} missing height_px"
            assert entry.aspect_ratio != "", f"{format_name} missing aspect_ratio"
            assert entry.dpi > 0, f"{format_name} missing dpi"
            assert entry.color_space != "", f"{format_name} missing color_space"
            assert entry.bleed_zone_px >= 0, f"{format_name} missing bleed_zone_px"

    def test_all_carousel_formats_have_bleed_40(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """FR-VIS-07 §5: carousel formats have bleed_zone_px=40."""
        registry = adapter.get_registry()
        carousel_formats = [k for k in registry if k.startswith("carousel_")]
        assert len(carousel_formats) >= 4  # At least 4 carousel formats
        for fmt in carousel_formats:
            assert registry[fmt].bleed_zone_px == 40, (
                f"{fmt} should have bleed_zone_px=40"
            )

    def test_all_single_formats_have_bleed_0(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """FR-VIS-07 §5: single image formats have bleed_zone_px=0."""
        registry = adapter.get_registry()
        single_formats = [
            k for k in registry
            if k.startswith("single_") or k.startswith("poll_") or k.startswith("nine_")
        ]
        for fmt in single_formats:
            assert registry[fmt].bleed_zone_px == 0, (
                f"{fmt} should have bleed_zone_px=0"
            )

    def test_all_formats_use_srgb(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """FR-VIS-07 §5: all digital social formats use sRGB color space."""
        registry = adapter.get_registry()
        for fmt, entry in registry.items():
            assert entry.color_space == "sRGB", f"{fmt} should use sRGB"

    def test_all_formats_use_72_dpi(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """FR-VIS-07 §5: all digital formats use 72 DPI."""
        registry = adapter.get_registry()
        for fmt, entry in registry.items():
            assert entry.dpi == 72, f"{fmt} should use 72 DPI"

    def test_aspect_ratio_groupings(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """FR-VIS-07 §5: verify aspect ratio → pixel dimension mapping."""
        registry = adapter.get_registry()
        for fmt, entry in registry.items():
            if entry.aspect_ratio == "4:5":
                assert entry.width_px == 1080 and entry.height_px == 1350, (
                    f"{fmt}: 4:5 should be 1080x1350"
                )
            elif entry.aspect_ratio == "9:16":
                assert entry.width_px == 1080 and entry.height_px == 1920, (
                    f"{fmt}: 9:16 should be 1080x1920"
                )
            elif entry.aspect_ratio == "1:1":
                assert entry.width_px == 1080 and entry.height_px == 1080, (
                    f"{fmt}: 1:1 should be 1080x1080"
                )
            else:
                pytest.fail(f"{fmt} has unexpected aspect_ratio: {entry.aspect_ratio}")


# ─────────────────────────────────────────────────────
# AC1: 4:5 Carousel Lock
# FR-VIS-07 §8 AC1
# ─────────────────────────────────────────────────────


class TestAC1CarouselLock:
    """AC1: Carousel format emits correct 4:5 envelope with bleed."""

    def test_carousel_dopamine_cliff_7_slides(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """FR-VIS-07 §8 AC1: carousel_dopamine_cliff, 7 slides.
        Assert 1080x1350, 4:5, bleed_zone_px=40, 7 per-slide entries."""
        inp = _make_input("carousel_dopamine_cliff", slide_count=7)
        result = adapter.adapt(inp)

        assert result.success is True
        env = result.envelope
        assert env is not None
        assert env.width_px == 1080
        assert env.height_px == 1350
        assert env.aspect_ratio == "4:5"
        assert env.bleed_zone_px == 40
        assert env.dpi == 72
        assert env.color_space == "sRGB"
        assert env.total_slides == 7
        assert env.per_slide_dimensions is not None
        assert len(env.per_slide_dimensions) == 7
        for psd in env.per_slide_dimensions:
            assert psd.width_px == 1080
            assert psd.height_px == 1350

    def test_carousel_listicle_5_slides(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """Another carousel format with different slide count."""
        inp = _make_input("carousel_listicle", slide_count=5)
        result = adapter.adapt(inp)

        assert result.success is True
        env = result.envelope
        assert env is not None
        assert env.width_px == 1080
        assert env.height_px == 1350
        assert env.bleed_zone_px == 40
        assert len(env.per_slide_dimensions) == 5

    def test_carousel_timeline(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """carousel_timeline also 4:5 with bleed."""
        inp = _make_input("carousel_timeline", slide_count=4)
        result = adapter.adapt(inp)
        assert result.success is True
        assert result.envelope.bleed_zone_px == 40

    def test_carousel_comparison(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """carousel_comparison also 4:5 with bleed."""
        inp = _make_input("carousel_comparison", slide_count=3)
        result = adapter.adapt(inp)
        assert result.success is True
        assert result.envelope.bleed_zone_px == 40


# ─────────────────────────────────────────────────────
# AC2: 9:16 Poll Lock
# FR-VIS-07 §8 AC2
# ─────────────────────────────────────────────────────


class TestAC2PollLock:
    """AC2: Poll format emits correct 9:16 envelope without bleed."""

    def test_poll_archetypical(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """FR-VIS-07 §8 AC2: poll_archetypical → 1080x1920, 9:16, bleed=0."""
        inp = _make_input("poll_archetypical", slide_count=2)
        result = adapter.adapt(inp)

        assert result.success is True
        env = result.envelope
        assert env is not None
        assert env.width_px == 1080
        assert env.height_px == 1920
        assert env.aspect_ratio == "9:16"
        assert env.bleed_zone_px == 0

    def test_poll_stereotypical(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """poll_stereotypical also 9:16."""
        inp = _make_input("poll_stereotypical", slide_count=2)
        result = adapter.adapt(inp)
        assert result.success is True
        assert result.envelope.height_px == 1920

    def test_poll_controversial_dilemma(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """poll_controversial_dilemma also 9:16."""
        inp = _make_input("poll_controversial_dilemma", slide_count=2)
        result = adapter.adapt(inp)
        assert result.success is True
        assert result.envelope.aspect_ratio == "9:16"

    def test_poll_no_carousel_bleed(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """FR-VIS-07 §8 AC2 Failure Example: poll must NOT have 40px bleed."""
        inp = _make_input("poll_archetypical", slide_count=2)
        result = adapter.adapt(inp)
        assert result.envelope.bleed_zone_px == 0, (
            "Poll must not have carousel bleed zone applied"
        )


# ─────────────────────────────────────────────────────
# AC3: 1:1 Square Lock
# FR-VIS-07 §8 AC3
# ─────────────────────────────────────────────────────


class TestAC3SquareLock:
    """AC3: Square formats emit correct 1:1 envelope."""

    def test_single_tweet_quote(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """FR-VIS-07 §8 AC3: single_tweet_quote → 1080x1080, 1:1."""
        inp = _make_input("single_tweet_quote", slide_count=1)
        result = adapter.adapt(inp)

        assert result.success is True
        env = result.envelope
        assert env is not None
        assert env.width_px == 1080
        assert env.height_px == 1080
        assert env.aspect_ratio == "1:1"

    def test_single_supervisual(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """single_supervisual also 1:1."""
        inp = _make_input("single_supervisual", slide_count=1)
        result = adapter.adapt(inp)
        assert result.success is True
        assert result.envelope.height_px == 1080

    def test_single_conceptual_contrast_simultaneous(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """single_conceptual_contrast_simultaneous also 1:1."""
        inp = _make_input("single_conceptual_contrast_simultaneous", slide_count=1)
        result = adapter.adapt(inp)
        assert result.success is True
        assert result.envelope.aspect_ratio == "1:1"

    def test_single_observational_humor_square(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """single_observational_humor_square also 1:1."""
        inp = _make_input("single_observational_humor_square", slide_count=1)
        result = adapter.adapt(inp)
        assert result.success is True
        assert result.envelope.width_px == 1080
        assert result.envelope.height_px == 1080

    def test_square_not_defaulting_to_4_5(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """FR-VIS-07 §8 AC3 Failure Example: single_* must NOT default to 4:5."""
        inp = _make_input("single_tweet_quote", slide_count=1)
        result = adapter.adapt(inp)
        assert result.envelope.aspect_ratio != "4:5", (
            "single_tweet_quote must be 1:1, not 4:5"
        )


# ─────────────────────────────────────────────────────
# AC4: Unrecognized Format Rejection
# FR-VIS-07 §8 AC4
# ─────────────────────────────────────────────────────


class TestAC4UnrecognizedFormatRejection:
    """AC4: Unrecognized format → FORMAT_NOT_RECOGNIZED, no fallback."""

    def test_unknown_format_halts(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """FR-VIS-07 §8 AC4: story_vertical_fullscreen → FORMAT_NOT_RECOGNIZED."""
        inp = _make_input("story_vertical_fullscreen", slide_count=1)
        result = adapter.adapt(inp)

        assert result.success is False
        assert result.error_type == FormatAdapterError.FORMAT_NOT_RECOGNIZED.value
        assert result.envelope is None

    def test_unknown_format_no_fallback_envelope(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """FR-VIS-07 §8 AC4 Failure Example: no fallback to 1:1."""
        inp = _make_input("reel_vertical_cinematic", slide_count=1)
        result = adapter.adapt(inp)
        assert result.success is False
        assert result.envelope is None

    def test_empty_string_format(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """Empty content_format string triggers MISSING_CONTENT_FORMAT."""
        inp = _make_input("", slide_count=1)
        result = adapter.adapt(inp)
        assert result.success is False
        assert result.error_type == FormatAdapterError.MISSING_CONTENT_FORMAT.value

    def test_null_format_without_recipe_id(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """Null content_format with no recipe_id → MISSING_CONTENT_FORMAT."""
        inp = _make_input(None, slide_count=1)
        result = adapter.adapt(inp)
        assert result.success is False
        assert result.error_type == FormatAdapterError.MISSING_CONTENT_FORMAT.value


# ─────────────────────────────────────────────────────
# AC5: Immutability Enforcement
# FR-VIS-07 §8 AC5
# ─────────────────────────────────────────────────────


class TestAC5ImmutabilityEnforcement:
    """AC5: Dimension override detected via seal hash mismatch."""

    def test_seal_hash_present(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """Sealed envelope must have a non-empty seal_hash."""
        inp = _make_input("carousel_dopamine_cliff", slide_count=7)
        result = adapter.adapt(inp)
        assert result.success is True
        assert result.envelope.seal_hash is not None
        assert len(result.envelope.seal_hash) == 64  # SHA-256 hex

    def test_seal_hash_verifies_cleanly(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """Clean envelope passes seal verification."""
        inp = _make_input("carousel_dopamine_cliff", slide_count=7)
        result = adapter.adapt(inp)
        assert VisualFormatConstraintAdapter.verify_seal(result.envelope) is True

    def test_tampered_envelope_fails_verification(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """FR-VIS-07 §8 AC5: modify height_px → seal verification fails."""
        inp = _make_input("carousel_dopamine_cliff", slide_count=7)
        result = adapter.adapt(inp)

        # Tamper: change height to 1080 (attempting square override)
        tampered = result.envelope.model_copy()
        tampered.height_px = 1080
        assert VisualFormatConstraintAdapter.verify_seal(tampered) is False

    def test_dimension_override_detection(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """FR-VIS-07 §8 AC5: downstream agent writes 1080x1080 on 4:5 envelope."""
        inp = _make_input("carousel_dopamine_cliff", slide_count=7)
        result = adapter.adapt(inp)

        violation = adapter.check_dimension_override(
            sealed_envelope=result.envelope,
            downstream_width=1080,
            downstream_height=1080,
            downstream_agent="abel_vcb",
        )
        assert violation is not None
        assert "DIMENSION_OVERRIDE_VIOLATION" in violation
        assert "1080x1080" in violation
        assert "1080x1350" in violation

    def test_matching_dimensions_no_violation(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """Correct dimensions → no violation."""
        inp = _make_input("carousel_dopamine_cliff", slide_count=7)
        result = adapter.adapt(inp)

        violation = adapter.check_dimension_override(
            sealed_envelope=result.envelope,
            downstream_width=1080,
            downstream_height=1350,
            downstream_agent="abel_vcb",
        )
        assert violation is None


# ─────────────────────────────────────────────────────
# AC6: Legacy Fallback
# FR-VIS-07 §8 AC6
# ─────────────────────────────────────────────────────


class TestAC6LegacyFallback:
    """AC6: Legacy recipe_id → content_format cross-reference."""

    def test_recipe_id_derives_carousel_listicle(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """FR-VIS-07 §8 AC6: no content_format but recipe_id derives carousel_listicle."""
        inp = _make_input(
            content_format=None,
            slide_count=5,
            recipe_id="RCP-CAROUSEL-LISTICLE-001",
        )
        result = adapter.adapt(inp)

        assert result.success is True
        env = result.envelope
        assert env is not None
        assert env.content_format == "carousel_listicle"
        assert env.width_px == 1080
        assert env.height_px == 1350
        assert env.aspect_ratio == "4:5"

        # Must have LEGACY_FORMAT_DERIVATION warning
        assert len(result.warnings) >= 1
        assert any("LEGACY_FORMAT_DERIVATION" in w for w in result.warnings)

    def test_recipe_id_derives_poll(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """recipe_id for poll derives correct 9:16 format."""
        inp = _make_input(
            content_format=None,
            slide_count=2,
            recipe_id="RCP-POLL-ARCHETYPICAL-001",
        )
        result = adapter.adapt(inp)
        assert result.success is True
        assert result.envelope.aspect_ratio == "9:16"

    def test_unknown_recipe_id_fails(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """Unknown recipe_id → FORMAT_NOT_RECOGNIZED."""
        inp = _make_input(
            content_format=None,
            slide_count=1,
            recipe_id="RCP-UNKNOWN-FORMAT-999",
        )
        result = adapter.adapt(inp)
        assert result.success is False
        assert result.error_type == FormatAdapterError.FORMAT_NOT_RECOGNIZED.value

    def test_recipe_id_mapping_covers_all_15_formats(self) -> None:
        """All 15 registry formats have a corresponding recipe_id mapping."""
        assert len(RECIPE_ID_TO_FORMAT) == 15
        # Every mapped format should be a valid registry format
        with open(DEFAULT_REGISTRY_PATH, "r", encoding="utf-8") as f:
            registry_data = json.load(f)["formats"]
        for recipe_id, fmt in RECIPE_ID_TO_FORMAT.items():
            assert fmt in registry_data, (
                f"Recipe {recipe_id} maps to {fmt} but it's not in the registry"
            )


# ─────────────────────────────────────────────────────
# ENVELOPE ASSEMBLY TESTS
# FR-VIS-07 §10 Unit Tests
# ─────────────────────────────────────────────────────


class TestEnvelopeAssembly:
    """FR-VIS-07 §10: Envelope assembly tests."""

    def test_per_slide_dimensions_count_matches_slide_count(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """FR-VIS-07 §10: mock content output with carousel_timeline, 5 slides.
        Assert exactly 5 entries in per_slide_dimensions."""
        inp = _make_input("carousel_timeline", slide_count=5)
        result = adapter.adapt(inp)

        assert result.success is True
        assert len(result.envelope.per_slide_dimensions) == 5
        for i, psd in enumerate(result.envelope.per_slide_dimensions):
            assert psd.slide_index == i
            assert psd.width_px == 1080
            assert psd.height_px == 1350

    def test_envelope_has_envelope_id(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """Envelope must have a unique envelope_id starting with FCE-."""
        inp = _make_input("single_tweet_quote", slide_count=1)
        result = adapter.adapt(inp)
        assert result.envelope.envelope_id.startswith("FCE-")

    def test_envelope_has_timestamp(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """Envelope must have a timestamp_utc."""
        inp = _make_input("single_tweet_quote", slide_count=1)
        result = adapter.adapt(inp)
        assert result.envelope.timestamp_utc is not None
        # Should parse as ISO 8601
        from datetime import datetime
        dt = datetime.fromisoformat(result.envelope.timestamp_utc)
        assert dt is not None


# ─────────────────────────────────────────────────────
# HASH DETERMINISM TESTS
# FR-VIS-07 §10 Unit Tests
# ─────────────────────────────────────────────────────


class TestHashDeterminism:
    """FR-VIS-07 §10: Hash determinism tests."""

    def test_identical_inputs_produce_different_envelope_ids(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """Two adapter runs produce different envelope IDs (UUID-based)."""
        inp = _make_input("carousel_dopamine_cliff", slide_count=7)
        result1 = adapter.adapt(inp)
        result2 = adapter.adapt(inp)
        assert result1.envelope.envelope_id != result2.envelope.envelope_id

    def test_modified_slide_count_changes_hash(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """FR-VIS-07 §10: modify slide_count by 1 → hash changes."""
        inp7 = _make_input("carousel_dopamine_cliff", slide_count=7)
        inp8 = _make_input("carousel_dopamine_cliff", slide_count=8)
        result7 = adapter.adapt(inp7)
        result8 = adapter.adapt(inp8)
        assert result7.envelope.seal_hash != result8.envelope.seal_hash


# ─────────────────────────────────────────────────────
# RECEIPT CHAIN INTEGRATION
# FR-VIS-07 §4 Receipt Writes
# ─────────────────────────────────────────────────────


class TestReceiptChainIntegration:
    """Verify receipt chain writes at every stage."""

    def test_success_writes_3_receipts(
        self,
        adapter: VisualFormatConstraintAdapter,
        tmp_receipt_dir: Path,
    ) -> None:
        """Successful adapt writes 3 receipts: extraction, assembly, injection."""
        inp = _make_input("carousel_dopamine_cliff", slide_count=7)
        result = adapter.adapt(inp)
        assert result.success is True

        receipt_files = list(tmp_receipt_dir.glob("receipt_*.jsonl"))
        receipts = []
        for f in receipt_files:
            for line in f.read_text().strip().split("\n"):
                if line:
                    receipts.append(json.loads(line))

        assert len(receipts) == 3
        actions = [r["action"] for r in receipts]
        assert "VIS07_FORMAT_EXTRACTION" in actions
        assert "VIS07_ENVELOPE_ASSEMBLY" in actions
        assert "VIS07_DOWNSTREAM_INJECTION" in actions

        # Verify chain linking
        assert receipts[1]["parent_receipt_id"] == receipts[0]["receipt_id"]
        assert receipts[2]["parent_receipt_id"] == receipts[1]["receipt_id"]

    def test_failure_writes_1_receipt(
        self,
        adapter: VisualFormatConstraintAdapter,
        tmp_receipt_dir: Path,
    ) -> None:
        """Failed extraction writes 1 receipt (extraction only, then halts)."""
        inp = _make_input("unknown_format", slide_count=1)
        result = adapter.adapt(inp)
        assert result.success is False

        receipt_files = list(tmp_receipt_dir.glob("receipt_*.jsonl"))
        receipts = []
        for f in receipt_files:
            for line in f.read_text().strip().split("\n"):
                if line:
                    receipts.append(json.loads(line))

        assert len(receipts) == 1
        assert receipts[0]["action"] == "VIS07_FORMAT_EXTRACTION"


# ─────────────────────────────────────────────────────
# SAFETY TESTS
# FR-VIS-07 §10 Safety Tests
# ─────────────────────────────────────────────────────


class TestSafetyTests:
    """Safety tests per FR-VIS-07 §10."""

    def test_injection_resistance(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """FR-VIS-07 §10: SQL injection in content_format → FORMAT_NOT_RECOGNIZED."""
        inp = _make_input(
            "carousel_dopamine_cliff; DROP TABLE format_registry;",
            slide_count=7,
        )
        result = adapter.adapt(inp)
        assert result.success is False
        assert result.error_type == FormatAdapterError.FORMAT_NOT_RECOGNIZED.value

    def test_envelope_tampering_detected(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """FR-VIS-07 §10: intercept envelope, modify height → hash mismatch."""
        inp = _make_input("carousel_dopamine_cliff", slide_count=7)
        result = adapter.adapt(inp)

        # Tamper with the envelope
        result.envelope.height_px = 1080  # Change 1350 → 1080

        # Seal verification detects tampering
        assert VisualFormatConstraintAdapter.verify_seal(result.envelope) is False

    def test_coach_acronym_validation(self) -> None:
        """ADR-01: coach_acronym must be 2-4 characters."""
        with pytest.raises(ValueError, match="coach_acronym must be 2-4 characters"):
            VisualFormatConstraintAdapter(coach_acronym="X")

    def test_c11_persona_masking(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """C-11 Persona Masking: agent names must not appear in output."""
        inp = _make_input("carousel_dopamine_cliff", slide_count=7)
        result = adapter.adapt(inp)
        result_json = result.model_dump_json()
        agent_names = [
            "Abel", "Paradoxe", "Aurore", "Sophia", "Marcus", "Chen",
            "Cesare", "Charlotte", "Dilaya", "Emmanuel", "Kimya",
            "Morgan", "Valeriane",
        ]
        for name in agent_names:
            assert name not in result_json, (
                f"C-11 violation: agent name '{name}' found in output"
            )


# ─────────────────────────────────────────────────────
# CROSS-FORMAT VALIDATION
# FR-VIS-07 §10 Integration Tests
# ─────────────────────────────────────────────────────


class TestCrossFormatValidation:
    """FR-VIS-07 §10: one asset of each aspect ratio type."""

    def test_all_three_aspect_ratios(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """Submit one format from each aspect ratio group, verify dimensions."""
        test_cases = [
            ("carousel_dopamine_cliff", "4:5", 1080, 1350),
            ("poll_archetypical", "9:16", 1080, 1920),
            ("single_tweet_quote", "1:1", 1080, 1080),
        ]
        for fmt, expected_ar, expected_w, expected_h in test_cases:
            inp = _make_input(fmt, slide_count=1)
            result = adapter.adapt(inp)
            assert result.success is True, f"Failed for {fmt}"
            assert result.envelope.aspect_ratio == expected_ar
            assert result.envelope.width_px == expected_w
            assert result.envelope.height_px == expected_h

    def test_nine_grid_format(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """nine_grid_accumulation is 4:5 per registry."""
        inp = _make_input("nine_grid_accumulation", slide_count=9)
        result = adapter.adapt(inp)
        assert result.success is True
        assert result.envelope.aspect_ratio == "4:5"
        assert result.envelope.width_px == 1080
        assert result.envelope.height_px == 1350
        assert len(result.envelope.per_slide_dimensions) == 9


# ─────────────────────────────────────────────────────
# EDGE CASES
# ─────────────────────────────────────────────────────


class TestEdgeCases:
    """Edge cases and boundary conditions."""

    def test_single_slide_composition(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """Single-slide composition produces 1 per_slide entry."""
        inp = _make_input("single_worst_case", slide_count=1)
        result = adapter.adapt(inp)
        assert result.success is True
        assert len(result.envelope.per_slide_dimensions) == 1
        assert result.envelope.per_slide_dimensions[0].slide_index == 0

    def test_result_includes_content_output_id(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """Result traces back to the upstream content_output_id."""
        inp = _make_input(
            "carousel_dopamine_cliff",
            slide_count=7,
            content_output_id="CO-JP-20260318-012",
        )
        result = adapter.adapt(inp)
        assert result.content_output_id == "CO-JP-20260318-012"

    def test_error_result_includes_content_output_id(
        self, adapter: VisualFormatConstraintAdapter
    ) -> None:
        """Error result also traces back to content_output_id."""
        inp = _make_input(
            "bogus_format",
            slide_count=1,
            content_output_id="CO-ERR-001",
        )
        result = adapter.adapt(inp)
        assert result.success is False
        assert result.content_output_id == "CO-ERR-001"
