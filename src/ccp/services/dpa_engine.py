import math
import uuid
from typing import Any, Optional
from enum import Enum

from src.ccp.models.ca11_models import (
    ArchetypePADTarget,
    BrandHueAnalysis,
    DPAResult,
    MoodPaletteColors,
    OverrideMode,
    PADVector,
    ResolvedPalette,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BHCS_THRESHOLD = 0.65
WCAG_AA_CONTRAST_MIN = 4.5
MAX_PAD_DISTANCE = math.sqrt(12.0)

DEFAULT_MOOD_PALETTES = {
    "escape": {
        "description": "Warm neutrals, low tension. For audiences seeking rest and comfort.",
        "kelvin_range": "2700K-3200K",
        "target_pad": {"P": 0.70, "A": -0.40, "D": -0.30},
        "colors": {
            "background_primary": "#F5F0E8",
            "background_gradient": "linear-gradient(180deg, #F5F0E8 0%, #EDE5D8 100%)",
            "accent": "#D4A574",
            "text_primary": "#3D3630",
            "text_secondary": "#87796A",
            "overlay": "rgba(245, 240, 232, 0.85)",
        }
    },
    "processing": {
        "description": "Cool foundation, high contrast. For analytical depth and trust.",
        "kelvin_range": "5000K-6500K",
        "target_pad": {"P": 0.25, "A": 0.55, "D": 0.45},
        "colors": {
            "background_primary": "#1A2332",
            "background_gradient": "linear-gradient(180deg, #1A2332 0%, #0F1722 100%)",
            "accent": "#5A8FA8",
            "text_primary": "#F0F4F8",
            "text_secondary": "#A0B4C0",
            "overlay": "rgba(26, 35, 50, 0.90)",
        }
    },
    "discovery": {
        "description": "Energetic mid-warmth. For approach motivation and curiosity.",
        "kelvin_range": "3000K-4000K",
        "target_pad": {"P": 0.75, "A": 0.85, "D": -0.20},
        "colors": {
            "background_primary": "#FFF5F0",
            "background_gradient": "linear-gradient(135deg, #FFF5F0 0%, #FFE8DC 100%)",
            "accent": "#E8657A",
            "text_primary": "#2D1F1A",
            "text_secondary": "#8B5E4D",
            "overlay": "rgba(255, 245, 240, 0.80)",
        }
    },
    "status": {
        "description": "Premium dark. Exclusivity, luxury, intimacy.",
        "kelvin_range": "dark_premium",
        "target_pad": {"P": 0.10, "A": 0.20, "D": 0.85},
        "colors": {
            "background_primary": "#0D0D0D",
            "background_gradient": "linear-gradient(180deg, #0D0D0D 0%, #1A1A1A 100%)",
            "accent": "#C9A96E",
            "text_primary": "#F5F0E8",
            "text_secondary": "#8A7D6A",
            "overlay": "rgba(13, 13, 13, 0.95)",
        }
    }
}

DEFAULT_ARCHETYPE_TARGETS = {
    "personal_low": {
        "pad": {"P": -0.65, "A": -0.70, "D": 0.30},
        "mood_base": "processing",
        "saturation_shift": -0.35
    },
    "hopeful": {
        "pad": {"P": 0.80, "A": 0.10, "D": -0.45},
        "mood_base": "escape",
        "saturation_shift": 0.10
    },
    "gritty_determination": {
        "pad": {"P": -0.15, "A": 0.35, "D": 0.75},
        "mood_base": "processing",
        "saturation_shift": -0.20
    },
    "playful_pop": {
        "pad": {"P": 0.75, "A": 0.85, "D": -0.20},
        "mood_base": "discovery",
        "saturation_shift": 0.30
    },
    "graphic_novel": {
        "pad": {"P": -0.10, "A": 0.15, "D": 0.85},
        "mood_base": "status",
        "saturation_shift": -0.40
    },
    "soft_pastel": {
        "pad": {"P": 0.85, "A": -0.55, "D": -0.65},
        "mood_base": "escape",
        "saturation_shift": -0.15
    },
    "relief_peak": {
        "pad": {"P": 0.80, "A": -0.30, "D": -0.40},
        "mood_base": "escape",
        "saturation_shift": 0.05
    },
    "worst_case_scenario": {
        "pad": {"P": -0.50, "A": 0.60, "D": 0.50},
        "mood_base": "processing",
        "saturation_shift": -0.30
    },
    "observational_humor": {
        "pad": {"P": 0.60, "A": 0.40, "D": -0.10},
        "mood_base": "discovery",
        "saturation_shift": 0.15
    },
    "urgent_alert": {
        "pad": {"P": -0.35, "A": 0.90, "D": 0.25},
        "mood_base": "discovery",
        "saturation_shift": 0.40
    }
}

RESOLVED_PALETTE_SQL = """
CREATE TABLE IF NOT EXISTS resolved_palettes (
    resolved_palette_id UUID PRIMARY KEY,
    coach_id VARCHAR(255) NOT NULL,
    content_archetype VARCHAR(255) NOT NULL,
    audience_mood_state VARCHAR(255),
    target_pad JSONB NOT NULL,
    bhcs FLOAT NOT NULL,
    brand_hue_used BOOLEAN NOT NULL,
    identity JSONB NOT NULL,
    palette JSONB NOT NULL,
    kelvin_range VARCHAR(50),
    saturation_adjustment FLOAT NOT NULL,
    override_active BOOLEAN NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
"""

# ---------------------------------------------------------------------------
# Math & Conversion Utilities
# ---------------------------------------------------------------------------

def euclidean_distance(a: PADVector, b: PADVector) -> float:
    return math.sqrt((a.P - b.P) ** 2 + (a.A - b.A) ** 2 + (a.D - b.D) ** 2)

def compute_bhcs(brand_pad: PADVector, target_pad: PADVector) -> float:
    dist = euclidean_distance(brand_pad, target_pad)
    return max(0.0, min(1.0, 1.0 - (dist / MAX_PAD_DISTANCE)))

def hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    hex_str = hex_str.lstrip("#")
    if len(hex_str) == 3:
        hex_str = "".join(c * 2 for c in hex_str)
    return int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)

def rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02X}{g:02X}{b:02X}"

def rgb_to_hsl(r: int, g: int, b: int) -> tuple[float, float, float]:
    rf, gf, bf = r / 255.0, g / 255.0, b / 255.0
    cmax = max(rf, gf, bf)
    cmin = min(rf, gf, bf)
    diff = cmax - cmin
    
    l = (cmax + cmin) / 2.0
    
    if diff == 0:
        s = 0.0
        h = 0.0
    else:
        if l < 0.5:
            s = diff / (cmax + cmin)
        else:
            s = diff / (2.0 - cmax - cmin)
            
        if cmax == rf:
            h = (gf - bf) / diff + (6.0 if gf < bf else 0.0)
        elif cmax == gf:
            h = (bf - rf) / diff + 2.0
        else:
            h = (rf - gf) / diff + 4.0
        h *= 60.0
        
    return h, s, l

def hsl_to_rgb(h: float, s: float, l: float) -> tuple[int, int, int]:
    h = h % 360.0
    if s == 0.0:
        val = int(round(l * 255.0))
        return val, val, val
        
    c = (1.0 - abs(2.0 * l - 1.0)) * s
    x = c * (1.0 - abs((h / 60.0) % 2.0 - 1.0))
    m = l - c / 2.0
    
    if 0.0 <= h < 60.0:
        rf, gf, bf = c, x, 0.0
    elif 60.0 <= h < 120.0:
        rf, gf, bf = x, c, 0.0
    elif 120.0 <= h < 180.0:
        rf, gf, bf = 0.0, c, x
    elif 180.0 <= h < 240.0:
        rf, gf, bf = 0.0, x, c
    elif 240.0 <= h < 300.0:
        rf, gf, bf = x, 0.0, c
    else:
        rf, gf, bf = c, 0.0, x
        
    r = int(round((rf + m) * 255.0))
    g = int(round((gf + m) * 255.0))
    b = int(round((bf + m) * 255.0))
    return max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))

def apply_saturation_shift(hex_color: str, shift: float) -> str:
    if not hex_color.startswith("#"):
        return hex_color
    try:
        r, g, b = hex_to_rgb(hex_color)
        h, s, l = rgb_to_hsl(r, g, b)
        s = max(0.0, min(1.0, s + shift))
        r2, g2, b2 = hsl_to_rgb(h, s, l)
        return rgb_to_hex(r2, g2, b2)
    except Exception:
        return hex_color

def relative_luminance(hex_color: str) -> float:
    try:
        r, g, b = hex_to_rgb(hex_color)
    except Exception:
        return 0.0
    components = []
    for val in (r, g, b):
        srgb = val / 255.0
        if srgb <= 0.03928:
            components.append(srgb / 12.92)
        else:
            components.append(((srgb + 0.055) / 1.055) ** 2.4)
    return 0.2126 * components[0] + 0.7152 * components[1] + 0.0722 * components[2]

def contrast_ratio(hex_a: str, hex_b: str) -> float:
    l1 = relative_luminance(hex_a)
    l2 = relative_luminance(hex_b)
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)


# ---------------------------------------------------------------------------
# DPA Engine
# ---------------------------------------------------------------------------

class DPAEngine:
    """Dynamic Palette Adaptation (DPA) Engine."""

    async def resolve(
        self,
        coach_id: str,
        content_archetype: str,
        audience_mood_state: str = "",
        brand_hue_analysis: Optional[BrandHueAnalysis] = None,
        override_mode: OverrideMode = OverrideMode.adaptive,
        identity_tokens: Optional[dict[str, Any]] = None,
    ) -> DPAResult:
        """Resolve the dynamic color palette based on Valdez-Mehrabian PAD targets."""
        if content_archetype not in DEFAULT_ARCHETYPE_TARGETS:
            return DPAResult(success=False, error=f"Unknown archetype: {content_archetype}")
            
        arch = DEFAULT_ARCHETYPE_TARGETS[content_archetype]
        target_pad = PADVector(**arch["pad"])
        mood_base = arch["mood_base"]
        sat_shift = arch["saturation_shift"]
        
        # Decide which mood palette to use
        selected_mood = mood_base
        if audience_mood_state and audience_mood_state in DEFAULT_MOOD_PALETTES:
            selected_mood = audience_mood_state
            
        mood_palette = DEFAULT_MOOD_PALETTES[selected_mood]
        kelvin_range = mood_palette["kelvin_range"]
        
        # Apply saturation shifts to base colors
        base_colors = mood_palette["colors"]
        shifted_colors = {}
        for key, val in base_colors.items():
            if key == "accent" and isinstance(val, str) and val.startswith("#"):
                shifted_colors[key] = apply_saturation_shift(val, sat_shift)
            else:
                shifted_colors[key] = val
                
        # Brand Hue Congruence Score
        bhcs = 0.0
        if brand_hue_analysis is not None:
            bhcs = compute_bhcs(brand_hue_analysis.inherent_pad, target_pad)
            
        # Determine if brand hue should be used
        override_active = (override_mode == OverrideMode.brand_saturated)
        brand_hue_used = False
        
        if brand_hue_analysis is not None:
            if override_active:
                brand_hue_used = True
            else:
                brand_hue_used = (bhcs > BHCS_THRESHOLD)
                
        # Apply brand hue if selected
        if brand_hue_used and brand_hue_analysis is not None:
            shifted_colors["accent"] = brand_hue_analysis.primary_hue
            
        # Create MoodPaletteColors object
        resolved_colors = MoodPaletteColors(**shifted_colors)
        
        # Build ResolvedPalette
        resolved = ResolvedPalette(
            coach_id=coach_id,
            content_archetype=content_archetype,
            audience_mood_state=selected_mood,
            target_pad=target_pad,
            bhcs=bhcs,
            brand_hue_used=brand_hue_used,
            identity=identity_tokens or {},
            palette=resolved_colors,
            kelvin_range=kelvin_range,
            saturation_adjustment=sat_shift,
            override_active=override_active,
        )
        
        return DPAResult(success=True, resolved=resolved)

    def validate_wcag_contrast(self, colors: MoodPaletteColors) -> bool:
        """Validate background-to-text contrast ratio meets WCAG AA 4.5:1."""
        ratio = contrast_ratio(colors.background_primary, colors.text_primary)
        return ratio >= WCAG_AA_CONTRAST_MIN
