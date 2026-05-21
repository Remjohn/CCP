"""OFO Engine Models — FR-ERA3-04.
OFOAssetPackage, CrusadeNarrativeAudit (with Phase5-M03 validator),
AssetReference, OFOConversionEvent, OFOTargetState, InsufficientSignalError."""
from __future__ import annotations
import re
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator


# ── Error Types ──

class InsufficientSignalError(Exception):
    """Raised when TraitScoringEngine cannot confidently score the ingested media."""
    pass


class OFOPackageIncompleteError(Exception):
    """Raised when the OFO pipeline fails to generate all 4 required assets (AC1)."""
    pass


# ── Enums ──

class OFOTargetState(str, Enum):
    """Redis-backed state machine for Telegram delivery (§4 Phase 4 Step 15)."""
    IDLE = "IDLE"
    PACKAGE_GENERATING = "PACKAGE_GENERATING"
    PACKAGE_DELIVERED = "PACKAGE_DELIVERED"
    AWAITING_CORRECTION = "AWAITING_CORRECTION"
    CORRECTION_RECEIVED = "CORRECTION_RECEIVED"
    STEALTH_COURSE_ENTERED = "STEALTH_COURSE_ENTERED"


class OFOAssetType(str, Enum):
    """The 4 strict asset classifications in the OFO Proof Package."""
    CAROUSEL = "carousel"
    STORYTELLING_VIDEO = "storytelling_video"
    REELS_EXPLAINER = "reels_explainer"
    ANIMATED_AUDIT = "animated_audit"


# ── Constants ──

REDIS_STATE_TTL_SECONDS: int = 900  # 15 minutes
REDIS_KEY_TEMPLATE: str = "target:{telegram_id}:state"

# Phase5-M03 required themes (at least 2 must be present)
CRUSADE_REQUIRED_THEMES: list[str] = [
    r"algorithm", r"compression", r"flattening",
    r"legacy", r"defend", r"protect",
]
CRUSADE_MIN_THEME_MATCHES: int = 2

# Phase5-M03 forbidden clinical critique words
CRUSADE_FORBIDDEN_WORDS: list[str] = [
    r"\bpoor\b", r"\bweak\b", r"\bbad\b", r"needs improvement", r"\binadequate\b",
]

# Deterministic fallback templates for Crusade Narrative (§4 Phase 3 Step 10)
CRUSADE_FALLBACK_TEMPLATES: dict[str, str] = {
    "embodied_confidence": (
        "The algorithm has been compressing your natural physical authority — flattening "
        "the very qualities that make you compelling on stage. Your legacy of embodied "
        "presence is being eroded by platform compression. We're here to defend that legacy "
        "and protect what makes your coaching irreplaceable."
    ),
    "vocal_resonance": (
        "Social media algorithms are systematically flattening the depth and richness of "
        "your vocal signature. The compression artifacts destroy the resonance that your "
        "audience trusts. We're building a defense against this algorithmic erosion to "
        "protect and restore your true vocal legacy."
    ),
    "baseline_discovery": (
        "The heavy compression of the social media platform has destroyed the natural "
        "acoustic signature we need to analyze your true vocal legacy. The algorithm's "
        "flattening makes it impossible to defend what's uniquely yours. Record a clean "
        "60-second voice note directly into Telegram to establish your true acoustic baseline "
        "so we can protect your authentic authority."
    ),
    "default": (
        "The algorithm is compressing your authentic authority and flattening the qualities "
        "that define your coaching legacy. We're here to defend against this systematic "
        "erosion and protect what makes you irreplaceable."
    ),
}

# Inline capture button label (Phase5-M04)
INLINE_CAPTURE_BUTTON_LABEL: str = "Fix This Metric Now"
INLINE_CAPTURE_CALLBACK: str = "ofo_fix_metric"


# ── Models ──

class AssetReference(BaseModel):
    """A single asset within the 4-Asset Proof Package."""
    asset_id: str = Field(..., description="Universal asset identifier")
    asset_url: str = Field(..., description="S3/CDN URL for the rendered asset")
    asset_type: OFOAssetType = Field(
        ...,
        description="The strict classification of the visual asset.",
    )


class CrusadeNarrativeAudit(BaseModel):
    """The voiceover script for the Animated Video Audit.

    Phase5-M03: Must use Epic Meaning Framing (EXP-TRS-004).
    Validator enforces ideological keyword presence and bans clinical critique.
    """
    transcript: str = Field(
        ...,
        description="The voiceover script for the Animated Video Audit. Must strictly use Epic Meaning Framing.",
    )
    detected_flaw: str = Field(
        ...,
        description="The primary biometric negative metric identified (e.g., 'Embodied Confidence').",
    )
    biometric_score: float = Field(
        ..., ge=0.0, le=10.0,
        description="The raw biometric score for the detected flaw (0-10 scale).",
    )

    @field_validator("transcript")
    @classmethod
    def validate_crusade_narrative(cls, v: str) -> str:
        """Enforces CBAR Phase5-M03 (OFO Ego-Defense Rule).

        The transcript must contain words indicating an external algorithmic enemy
        rather than a personal failing to prevent triggering target ego-defense.
        """
        lower_v = v.lower()

        # Mandate the inclusion of thematic ideological keywords
        matches = sum(1 for theme in CRUSADE_REQUIRED_THEMES if re.search(theme, lower_v))
        if matches < CRUSADE_MIN_THEME_MATCHES:
            raise ValueError(
                "Transcript fails the Crusade Narrative mandate (Phase5-M03). "
                "It must explicitly frame the critique against the algorithm or system, not the user."
            )

        # Explicitly ban clinical, negative critique terminology
        for forbidden in CRUSADE_FORBIDDEN_WORDS:
            if re.search(forbidden, lower_v):
                raise ValueError(
                    f"Transcript contains forbidden clinical critique word: '{forbidden}'. "
                    "This violates Phase5-M03."
                )

        return v


class OFOAssetPackage(BaseModel):
    """The complete 4-Asset Proof Package (AC1)."""
    target_id: str = Field(..., description="The OFO target coach identifier")
    generated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    carousel: AssetReference
    storytelling_video: AssetReference
    reels_explainer: AssetReference
    animated_audit: AssetReference
    audit_data: CrusadeNarrativeAudit


class OFOConversionEvent(BaseModel):
    """Hook Cycle telemetry model (Phase5-M04 compliance tracking)."""
    target_id: str = Field(...)
    telegram_session_id: str = Field(...)
    audio_correction_asset_id: str = Field(...)
    hook_cycle_latency_ms: int = Field(
        ...,
        description="Time delta between audit delivery and correction receipt. Used to track Phase5-M04 compliance.",
    )
    conversion_successful: bool = Field(default=True)


class OFOIngestionResult(BaseModel):
    """Result of ingesting a target's public media."""
    target_id: str = Field(...)
    source_url: str = Field(...)
    normalized_audio_path: Optional[str] = Field(default=None)
    normalized_video_path: Optional[str] = Field(default=None)
    duration_seconds: Optional[float] = Field(default=None)
    ingestion_successful: bool = Field(default=True)
    error: Optional[str] = Field(default=None)
