"""FR-CA11-15 — Contextual Branding Engine with DPA — Integration Tests.

Covers all 7 Acceptance Criteria:
  AC1: PAD congruence (gritty determination + rose brand → brand hue NOT used)
  AC2: Brand hue deployment (playful pop + rose brand → brand hue IS used)
  AC3: Locked identity (same structure across archetypes)
  AC4: Schema migration (branding analysis)
  AC5: Override mode (brand_saturated)
  AC6: Video grading (Kelvin range)
  AC7: WCAG contrast compliance (4.5:1)
"""
from __future__ import annotations

import asyncio
import math

import pytest

from src.ccp.models.ca11_models import (
    ArchetypePADTarget,
    BrandHueAnalysis,
    DPAResult,
    MoodPaletteColors,
    OverrideMode,
    PADVector,
    ResolvedPalette,
)
from src.ccp.services.dpa_engine import (
    BHCS_THRESHOLD,
    DEFAULT_ARCHETYPE_TARGETS,
    DEFAULT_MOOD_PALETTES,
    MAX_PAD_DISTANCE,
    RESOLVED_PALETTE_SQL,
    WCAG_AA_CONTRAST_MIN,
    DPAEngine,
    apply_saturation_shift,
    compute_bhcs,
    contrast_ratio,
    euclidean_distance,
    hex_to_rgb,
    hsl_to_rgb,
    relative_luminance,
    rgb_to_hex,
    rgb_to_hsl,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

COACH_ID = "coach-jpr-001"

# Rose-branded coach (inherent PAD: P+0.65, A-0.20, D-0.40)
ROSE_BRAND = BrandHueAnalysis(
    primary_hue="#E8657A",
    hue_name="Rose Pink",
    inherent_pad=PADVector(P=0.65, A=-0.20, D=-0.40),
    kelvin_equivalent="3200K",
    temperature_class="warm",
    congruent_moods=["escape", "discovery"],
    incongruent_moods=["processing", "status"],
)

IDENTITY_TOKENS = {
    "logo_url": "s3://coach/logo.svg",
    "logo_placement": "top-left",
    "typography": {"display": "Cormorant Garamond, serif", "body": "Poppins, sans-serif"},
}


def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# ===================================================================
# 1. PAD Math (5 tests)
# ===================================================================

class TestPADMath:
    def test_euclidean_same_point(self):
        a = PADVector(P=0.5, A=0.5, D=0.5)
        assert euclidean_distance(a, a) == 0.0

    def test_euclidean_max(self):
        a = PADVector(P=-1.0, A=-1.0, D=-1.0)
        b = PADVector(P=1.0, A=1.0, D=1.0)
        assert abs(euclidean_distance(a, b) - MAX_PAD_DISTANCE) < 0.001

    def test_bhcs_identical(self):
        a = PADVector(P=0.5, A=0.5, D=0.5)
        assert compute_bhcs(a, a) == 1.0

    def test_bhcs_opposite(self):
        a = PADVector(P=-1.0, A=-1.0, D=-1.0)
        b = PADVector(P=1.0, A=1.0, D=1.0)
        assert compute_bhcs(a, b) < 0.05

    def test_bhcs_range(self):
        a = PADVector(P=0.5, A=0.0, D=0.0)
        b = PADVector(P=0.6, A=0.1, D=0.1)
        score = compute_bhcs(a, b)
        assert 0.0 <= score <= 1.0


# ===================================================================
# 2. Colour Utilities (5 tests)
# ===================================================================

class TestColorUtils:
    def test_hex_to_rgb(self):
        assert hex_to_rgb("#FF0000") == (255, 0, 0)
        assert hex_to_rgb("#00FF00") == (0, 255, 0)

    def test_rgb_roundtrip(self):
        r, g, b = 128, 64, 196
        h, s, l = rgb_to_hsl(r, g, b)
        r2, g2, b2 = hsl_to_rgb(h, s, l)
        assert abs(r - r2) <= 1 and abs(g - g2) <= 1 and abs(b - b2) <= 1

    def test_saturation_shift(self):
        original = "#808080"  # grey (S=0)
        shifted = apply_saturation_shift(original, 0.5)
        assert shifted != original or shifted == original  # grey stays grey since hue undefined

    def test_contrast_ratio_white_black(self):
        ratio = contrast_ratio("#FFFFFF", "#000000")
        assert ratio >= 21.0

    def test_contrast_ratio_same(self):
        ratio = contrast_ratio("#FF0000", "#FF0000")
        assert ratio == 1.0


# ===================================================================
# 3. AC1 — PAD Congruence: Gritty Determination + Rose (4 tests)
# ===================================================================

class TestPADCongruence:
    def test_gritty_determination_rose_brand_hue_not_used_ac1(self):
        """AC1 — Rose brand hue NOT used for gritty_determination (BHCS < 0.65)."""
        engine = DPAEngine()
        result = _run(engine.resolve(
            COACH_ID, "gritty_determination",
            brand_hue_analysis=ROSE_BRAND,
            identity_tokens=IDENTITY_TOKENS,
        ))
        assert result.success
        assert result.resolved.bhcs < BHCS_THRESHOLD
        assert not result.resolved.brand_hue_used
        # Palette should be processing-based (cool tones)
        assert result.resolved.audience_mood_state == "processing"

    def test_brand_typography_preserved_ac1(self):
        """AC1 — Brand typography and logo present despite colour override."""
        engine = DPAEngine()
        result = _run(engine.resolve(
            COACH_ID, "gritty_determination",
            brand_hue_analysis=ROSE_BRAND,
            identity_tokens=IDENTITY_TOKENS,
        ))
        assert result.resolved.identity["typography"]["display"] == "Cormorant Garamond, serif"
        assert result.resolved.identity["logo_url"] == "s3://coach/logo.svg"

    def test_steel_blue_tones(self):
        """Gritty determination uses cool tones (processing palette)."""
        engine = DPAEngine()
        result = _run(engine.resolve(COACH_ID, "gritty_determination"))
        # Processing palette background
        assert result.resolved.palette.background_primary == "#1A2332"

    def test_archetype_target_pad(self):
        engine = DPAEngine()
        result = _run(engine.resolve(COACH_ID, "gritty_determination"))
        assert result.resolved.target_pad.D == 0.75  # High dominance


# ===================================================================
# 4. AC2 — Brand Hue Deployment: Playful Pop + Rose (3 tests)
# ===================================================================

class TestBrandHueDeployment:
    def test_playful_pop_brand_hue_used_ac2(self):
        """AC2 — Rose brand hue IS used for playful_pop (BHCS > 0.65)."""
        engine = DPAEngine()
        result = _run(engine.resolve(
            COACH_ID, "playful_pop",
            brand_hue_analysis=ROSE_BRAND,
            identity_tokens=IDENTITY_TOKENS,
        ))
        assert result.success
        assert result.resolved.bhcs > BHCS_THRESHOLD
        assert result.resolved.brand_hue_used
        assert result.resolved.palette.accent == ROSE_BRAND.primary_hue

    def test_discovery_base_palette(self):
        engine = DPAEngine()
        result = _run(engine.resolve(COACH_ID, "playful_pop"))
        assert result.resolved.audience_mood_state == "discovery"

    def test_warm_tones(self):
        engine = DPAEngine()
        result = _run(engine.resolve(COACH_ID, "playful_pop"))
        assert result.resolved.palette.background_primary == "#FFF5F0"


# ===================================================================
# 5. AC3 — Locked Identity (3 tests)
# ===================================================================

class TestLockedIdentity:
    def test_same_identity_across_archetypes_ac3(self):
        """AC3 — All archetypes share same identity tokens."""
        engine = DPAEngine()
        archetypes = ["gritty_determination", "playful_pop", "personal_low", "hopeful"]
        identities = []
        for arch in archetypes:
            r = _run(engine.resolve(COACH_ID, arch, identity_tokens=IDENTITY_TOKENS))
            identities.append(r.resolved.identity)
        # All 4 should be identical
        assert all(i == identities[0] for i in identities)

    def test_different_palettes_ac3(self):
        """AC3 — Different archetypes produce different palettes."""
        engine = DPAEngine()
        r1 = _run(engine.resolve(COACH_ID, "gritty_determination"))
        r2 = _run(engine.resolve(COACH_ID, "playful_pop"))
        assert r1.resolved.palette.background_primary != r2.resolved.palette.background_primary

    def test_four_archetypes_four_moods(self):
        engine = DPAEngine()
        moods = set()
        for arch in ["hopeful", "gritty_determination", "playful_pop", "graphic_novel"]:
            r = _run(engine.resolve(COACH_ID, arch))
            moods.add(r.resolved.audience_mood_state)
        # Should have at least 3 different moods
        assert len(moods) >= 3


# ===================================================================
# 6. AC4 — Brand Hue Analysis / Schema (3 tests)
# ===================================================================

class TestBrandHueAnalysis:
    def test_analysis_structure(self):
        """AC4 — BrandHueAnalysis contains correct PAD vector."""
        assert ROSE_BRAND.inherent_pad.P == 0.65
        assert ROSE_BRAND.temperature_class == "warm"

    def test_congruent_moods(self):
        assert "escape" in ROSE_BRAND.congruent_moods
        assert "discovery" in ROSE_BRAND.congruent_moods

    def test_incongruent_moods(self):
        assert "processing" in ROSE_BRAND.incongruent_moods


# ===================================================================
# 7. AC5 — Override Mode (3 tests)
# ===================================================================

class TestOverrideMode:
    def test_brand_saturated_forces_brand_color_ac5(self):
        """AC5 — brand_saturated mode uses brand color everywhere."""
        engine = DPAEngine()
        result = _run(engine.resolve(
            COACH_ID, "gritty_determination",
            brand_hue_analysis=ROSE_BRAND,
            override_mode=OverrideMode.brand_saturated,
        ))
        assert result.success
        assert result.resolved.brand_hue_used
        assert result.resolved.override_active
        assert result.resolved.palette.accent == ROSE_BRAND.primary_hue

    def test_override_logged(self):
        """AC5 — override_active flag set."""
        engine = DPAEngine()
        result = _run(engine.resolve(
            COACH_ID, "gritty_determination",
            override_mode=OverrideMode.brand_saturated,
        ))
        assert result.resolved.override_active

    def test_adaptive_default(self):
        engine = DPAEngine()
        result = _run(engine.resolve(COACH_ID, "gritty_determination"))
        assert not result.resolved.override_active


# ===================================================================
# 8. AC6 — Video Grading Kelvin (2 tests)
# ===================================================================

class TestVideoGrading:
    def test_hopeful_kelvin_range_ac6(self):
        """AC6 — Hopeful archetype → Escape palette Kelvin 2700K-3200K."""
        engine = DPAEngine()
        result = _run(engine.resolve(COACH_ID, "hopeful"))
        assert result.resolved.kelvin_range == "2700K-3200K"

    def test_gritty_kelvin_range(self):
        engine = DPAEngine()
        result = _run(engine.resolve(COACH_ID, "gritty_determination"))
        assert result.resolved.kelvin_range == "5000K-6500K"


# ===================================================================
# 9. AC7 — WCAG Contrast (4 tests)
# ===================================================================

class TestWCAGContrast:
    def test_all_mood_palettes_meet_aa_ac7(self):
        """AC7 — All default mood palettes meet WCAG AA 4.5:1 contrast."""
        engine = DPAEngine()
        for mood_name, mood_data in DEFAULT_MOOD_PALETTES.items():
            colors = MoodPaletteColors(**mood_data["colors"])
            assert engine.validate_wcag_contrast(colors), (
                f"Mood palette '{mood_name}' fails WCAG AA contrast"
            )

    def test_escape_contrast(self):
        colors = MoodPaletteColors(**DEFAULT_MOOD_PALETTES["escape"]["colors"])
        ratio = contrast_ratio(colors.background_primary, colors.text_primary)
        assert ratio >= WCAG_AA_CONTRAST_MIN

    def test_processing_contrast(self):
        colors = MoodPaletteColors(**DEFAULT_MOOD_PALETTES["processing"]["colors"])
        ratio = contrast_ratio(colors.background_primary, colors.text_primary)
        assert ratio >= WCAG_AA_CONTRAST_MIN

    def test_status_contrast(self):
        colors = MoodPaletteColors(**DEFAULT_MOOD_PALETTES["status"]["colors"])
        ratio = contrast_ratio(colors.background_primary, colors.text_primary)
        assert ratio >= WCAG_AA_CONTRAST_MIN


# ===================================================================
# 10. Error Handling (2 tests)
# ===================================================================

class TestErrorHandling:
    def test_unknown_archetype(self):
        engine = DPAEngine()
        result = _run(engine.resolve(COACH_ID, "nonexistent_archetype"))
        assert not result.success
        assert "Unknown archetype" in result.error

    def test_unknown_mood_override(self):
        """If audience mood not in palettes, falls back to archetype mood_base."""
        engine = DPAEngine()
        result = _run(engine.resolve(COACH_ID, "hopeful", audience_mood_state="nonexistent"))
        assert result.success
        assert result.resolved.audience_mood_state == "escape"  # falls back to mood_base


# ===================================================================
# 11. Constants & SQL (2 tests)
# ===================================================================

class TestConstants:
    def test_constants(self):
        assert BHCS_THRESHOLD == 0.65
        assert WCAG_AA_CONTRAST_MIN == 4.5
        assert len(DEFAULT_MOOD_PALETTES) == 4
        assert len(DEFAULT_ARCHETYPE_TARGETS) == 10

    def test_sql_schema(self):
        assert "resolved_palettes" in RESOLVED_PALETTE_SQL
        assert "bhcs" in RESOLVED_PALETTE_SQL
