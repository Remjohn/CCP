"""FR-CA11-15 — Contextual Branding Engine with Dynamic Palette Adaptation (DPA).

Dual-layer branding system:
  Layer 1 (Locked):  Brand identity tokens — typography, logo, spacing.
  Layer 2 (Dynamic): PAD-targeted mood palettes per content piece.

Uses Valdez-Mehrabian PAD regression, Elliot-Maier Color-in-Context Theory,
and Labrecque-Milne colour-value congruence to select mood-congruent palettes.
"""
from __future__ import annotations

import math
from typing import Any, Optional, Protocol

from src.ccp.models.ca11_models import (
    ArchetypePADTarget,
    BrandHueAnalysis,
    DPAResult,
    MoodPalette,
    MoodPaletteColors,
    OverrideMode,
    PADVector,
    ResolvedPalette,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BHCS_THRESHOLD = 0.65
MAX_PAD_DISTANCE = math.sqrt(3 * (2.0 ** 2))  # max Euclidean in [-1,1]^3
WCAG_AA_CONTRAST_MIN = 4.5

DEFAULT_MOOD_PALETTES: dict[str, dict[str, Any]] = {
    "escape": {
        "description": "Warm neutrals, low tension.",
        "kelvin_range": "2700K-3200K",
        "target_pad": {"P": 0.70, "A": -0.40, "D": -0.30},
        "colors": {
            "background_primary": "#F5F0E8",
            "background_gradient": "linear-gradient(180deg, #F5F0E8 0%, #EDE5D8 100%)",
            "accent": "#D4A574",
            "text_primary": "#3D3630",
            "text_secondary": "#87796A",
            "overlay": "rgba(245, 240, 232, 0.85)",
        },
    },
    "processing": {
        "description": "Cool foundation, high contrast.",
        "kelvin_range": "5000K-6500K",
        "target_pad": {"P": 0.25, "A": 0.55, "D": 0.45},
        "colors": {
            "background_primary": "#1A2332",
            "background_gradient": "linear-gradient(180deg, #1A2332 0%, #0F1722 100%)",
            "accent": "#5A8FA8",
            "text_primary": "#F0F4F8",
            "text_secondary": "#A0B4C0",
            "overlay": "rgba(26, 35, 50, 0.90)",
        },
    },
    "discovery": {
        "description": "Energetic mid-warmth.",
        "kelvin_range": "3000K-4000K",
        "target_pad": {"P": 0.75, "A": 0.85, "D": -0.20},
        "colors": {
            "background_primary": "#FFF5F0",
            "background_gradient": "linear-gradient(135deg, #FFF5F0 0%, #FFE8DC 100%)",
            "accent": "#E8657A",
            "text_primary": "#2D1F1A",
            "text_secondary": "#8B5E4D",
            "overlay": "rgba(255, 245, 240, 0.80)",
        },
    },
    "status": {
        "description": "Premium dark. Exclusivity, luxury.",
        "kelvin_range": "dark_premium",
        "target_pad": {"P": 0.10, "A": 0.20, "D": 0.85},
        "colors": {
            "background_primary": "#0D0D0D",
            "background_gradient": "linear-gradient(180deg, #0D0D0D 0%, #1A1A1A 100%)",
            "accent": "#C9A96E",
            "text_primary": "#F5F0E8",
            "text_secondary": "#8A7D6A",
            "overlay": "rgba(13, 13, 13, 0.95)",
        },
    },
}

DEFAULT_ARCHETYPE_TARGETS: dict[str, dict[str, Any]] = {
    "personal_low": {"pad": {"P": -0.65, "A": -0.70, "D": 0.30}, "mood_base": "processing", "saturation_shift": -0.35},
    "hopeful": {"pad": {"P": 0.80, "A": 0.10, "D": -0.45}, "mood_base": "escape", "saturation_shift": 0.10},
    "gritty_determination": {"pad": {"P": -0.15, "A": 0.35, "D": 0.75}, "mood_base": "processing", "saturation_shift": -0.20},
    "playful_pop": {"pad": {"P": 0.75, "A": 0.85, "D": -0.20}, "mood_base": "discovery", "saturation_shift": 0.30},
    "graphic_novel": {"pad": {"P": -0.10, "A": 0.15, "D": 0.85}, "mood_base": "status", "saturation_shift": -0.40},
    "soft_pastel": {"pad": {"P": 0.85, "A": -0.55, "D": -0.65}, "mood_base": "escape", "saturation_shift": -0.15},
    "relief_peak": {"pad": {"P": 0.80, "A": -0.30, "D": -0.40}, "mood_base": "escape", "saturation_shift": 0.05},
    "worst_case_scenario": {"pad": {"P": -0.50, "A": 0.60, "D": 0.50}, "mood_base": "processing", "saturation_shift": -0.30},
    "observational_humor": {"pad": {"P": 0.60, "A": 0.40, "D": -0.10}, "mood_base": "discovery", "saturation_shift": 0.15},
    "urgent_alert": {"pad": {"P": -0.35, "A": 0.90, "D": 0.25}, "mood_base": "discovery", "saturation_shift": 0.40},
}

# ---------------------------------------------------------------------------
# SQL
# ---------------------------------------------------------------------------

RESOLVED_PALETTE_SQL = """
CREATE TABLE IF NOT EXISTS resolved_palettes (
    resolved_palette_id TEXT PRIMARY KEY,
    coach_id            TEXT NOT NULL,
    content_archetype   TEXT NOT NULL,
    mood_state          TEXT NOT NULL,
    bhcs                REAL NOT NULL,
    brand_hue_used      BOOLEAN NOT NULL DEFAULT false,
    override_active     BOOLEAN NOT NULL DEFAULT false,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""

# ---------------------------------------------------------------------------
# Protocols
# ---------------------------------------------------------------------------


class BrandingLoaderProtocol(Protocol):
    async def load_branding(self, coach_id: str) -> dict[str, Any]: ...


# ---------------------------------------------------------------------------
# PAD Math
# ---------------------------------------------------------------------------


def euclidean_distance(a: PADVector, b: PADVector) -> float:
    return math.sqrt((a.P - b.P) ** 2 + (a.A - b.A) ** 2 + (a.D - b.D) ** 2)


def compute_bhcs(brand_pad: PADVector, target_pad: PADVector) -> float:
    """Brand Hue Congruence Score: 1 - (distance / max_distance)."""
    dist = euclidean_distance(brand_pad, target_pad)
    return max(0.0, min(1.0, 1.0 - (dist / MAX_PAD_DISTANCE)))


# ---------------------------------------------------------------------------
# Hex Colour Utilities
# ---------------------------------------------------------------------------


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def rgb_to_hsl(r: int, g: int, b: int) -> tuple[float, float, float]:
    r1, g1, b1 = r / 255, g / 255, b / 255
    mx, mn = max(r1, g1, b1), min(r1, g1, b1)
    l = (mx + mn) / 2
    if mx == mn:
        h = s = 0.0
    else:
        d = mx - mn
        s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
        if mx == r1:
            h = (g1 - b1) / d + (6 if g1 < b1 else 0)
        elif mx == g1:
            h = (b1 - r1) / d + 2
        else:
            h = (r1 - g1) / d + 4
        h /= 6
    return (h, s, l)


def hsl_to_rgb(h: float, s: float, l: float) -> tuple[int, int, int]:
    if s == 0:
        v = int(round(l * 255))
        return (v, v, v)

    def hue2rgb(p, q, t):
        t = t % 1
        if t < 1 / 6:
            return p + (q - p) * 6 * t
        if t < 1 / 2:
            return q
        if t < 2 / 3:
            return p + (q - p) * (2 / 3 - t) * 6
        return p

    q = l * (1 + s) if l < 0.5 else l + s - l * s
    p = 2 * l - q
    return (
        int(round(hue2rgb(p, q, h + 1 / 3) * 255)),
        int(round(hue2rgb(p, q, h) * 255)),
        int(round(hue2rgb(p, q, h - 1 / 3) * 255)),
    )


def rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02x}{g:02x}{b:02x}"


def apply_saturation_shift(hex_color: str, shift: float) -> str:
    """Shift the saturation of a hex colour by `shift` (clamped 0-1)."""
    r, g, b = hex_to_rgb(hex_color)
    h, s, l = rgb_to_hsl(r, g, b)
    s = max(0.0, min(1.0, s + shift))
    r2, g2, b2 = hsl_to_rgb(h, s, l)
    return rgb_to_hex(r2, g2, b2)


def relative_luminance(hex_color: str) -> float:
    """WCAG 2.1 relative luminance."""
    r, g, b = hex_to_rgb(hex_color)

    def linearize(v: int) -> float:
        c = v / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def contrast_ratio(hex_bg: str, hex_fg: str) -> float:
    """WCAG contrast ratio between two hex colours."""
    l1 = relative_luminance(hex_bg)
    l2 = relative_luminance(hex_fg)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


# ---------------------------------------------------------------------------
# DPA Engine
# ---------------------------------------------------------------------------


class DPAEngine:
    """Dynamic Palette Adaptation Engine."""

    def __init__(
        self,
        branding_loader: BrandingLoaderProtocol | None = None,
        mood_palettes: dict[str, dict[str, Any]] | None = None,
        archetype_targets: dict[str, dict[str, Any]] | None = None,
    ) -> None:
        self._loader = branding_loader
        self._moods = mood_palettes or DEFAULT_MOOD_PALETTES
        self._archetypes = archetype_targets or DEFAULT_ARCHETYPE_TARGETS

    async def resolve(
        self,
        coach_id: str,
        content_archetype: str,
        audience_mood_state: str = "",
        brand_hue_analysis: BrandHueAnalysis | None = None,
        override_mode: OverrideMode = OverrideMode.adaptive,
        identity_tokens: dict[str, Any] | None = None,
    ) -> DPAResult:
        # 1. Look up archetype target
        arch_data = self._archetypes.get(content_archetype)
        if not arch_data:
            return DPAResult(success=False, error=f"Unknown archetype: {content_archetype}")

        target = ArchetypePADTarget(
            pad=PADVector(**arch_data["pad"]),
            mood_base=arch_data["mood_base"],
            saturation_shift=arch_data.get("saturation_shift", 0.0),
        )

        # 2. Select base mood palette
        mood_key = audience_mood_state if audience_mood_state in self._moods else target.mood_base
        mood_data = self._moods.get(mood_key)
        if not mood_data:
            return DPAResult(success=False, error=f"Unknown mood palette: {mood_key}")

        base_colors = MoodPaletteColors(**mood_data["colors"])
        kelvin_range = mood_data.get("kelvin_range", "")

        # 3. Compute BHCS
        bhcs = 0.0
        brand_hue_used = False
        if brand_hue_analysis:
            bhcs = compute_bhcs(brand_hue_analysis.inherent_pad, target.pad)

        # 4. Override mode
        if override_mode == OverrideMode.brand_saturated:
            if brand_hue_analysis:
                base_colors.accent = brand_hue_analysis.primary_hue
                brand_hue_used = True
            resolved = ResolvedPalette(
                coach_id=coach_id,
                content_archetype=content_archetype,
                audience_mood_state=mood_key,
                target_pad=target.pad,
                bhcs=bhcs,
                brand_hue_used=True,
                identity=identity_tokens or {},
                palette=base_colors,
                kelvin_range=kelvin_range,
                saturation_adjustment=0.0,
                override_active=True,
            )
            return DPAResult(success=True, resolved=resolved)

        # 5. Adaptive mode: apply saturation shift
        shifted_accent = apply_saturation_shift(base_colors.accent, target.saturation_shift)

        # 6. BHCS check — use brand hue if congruent
        if bhcs > BHCS_THRESHOLD and brand_hue_analysis:
            shifted_accent = brand_hue_analysis.primary_hue
            brand_hue_used = True

        final_colors = MoodPaletteColors(
            background_primary=base_colors.background_primary,
            background_gradient=base_colors.background_gradient,
            accent=shifted_accent,
            text_primary=base_colors.text_primary,
            text_secondary=base_colors.text_secondary,
            overlay=base_colors.overlay,
        )

        resolved = ResolvedPalette(
            coach_id=coach_id,
            content_archetype=content_archetype,
            audience_mood_state=mood_key,
            target_pad=target.pad,
            bhcs=round(bhcs, 4),
            brand_hue_used=brand_hue_used,
            identity=identity_tokens or {},
            palette=final_colors,
            kelvin_range=kelvin_range,
            saturation_adjustment=target.saturation_shift,
        )
        return DPAResult(success=True, resolved=resolved)

    def validate_wcag_contrast(self, palette: MoodPaletteColors) -> bool:
        """AC7 — Ensure background-to-text contrast meets WCAG AA (4.5:1)."""
        return contrast_ratio(palette.background_primary, palette.text_primary) >= WCAG_AA_CONTRAST_MIN
