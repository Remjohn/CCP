"""
Phase 2B — CVE Visual Engine Models
FR-VIS-13: Image Type Validity Gate (Gate V-00)

Every field is traced to an explicit spec instruction in
FR-VIS-13_Image_Type_Validity_Gate_Tech_Spec.md.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


# ─────────────────────────────────────────────────────
# ENUMS — Spec Section 4, Stage 1 (valid image types)
# ─────────────────────────────────────────────────────

class ImageType(str, Enum):
    """Valid image types per FR-VIS-13 §4 Stage 1 Step 3."""
    TIER_1_REAL_PERSON = "tier_1_real_person"
    TIER_2_STOCK_ENVIRONMENTAL = "tier_2_stock_environmental"
    TIER_2_STOCK_CONTEXTUAL = "tier_2_stock_contextual"
    TIER_2_STOCK_ABSTRACT = "tier_2_stock_abstract"
    TIER_3_AI_REALISTIC = "tier_3_ai_realistic"
    TIER_4_AI_GHIBLI = "tier_4_ai_ghibli"
    GRAPHIC_VECTOR = "graphic_vector"
    ANIMATED_GIF = "animated_gif"


class ImpliedStyle(str, Enum):
    """Implied visual styles per FR-VIS-13 §4 Stage 3 mapping table."""
    REAL_PHOTOGRAPHY_ONLY = "real_photography_only"
    SEMI_REALISTIC_DIGITAL = "semi_realistic_digital"
    CINEMATIC_COLOR_GRADED = "cinematic_color_graded"
    GHIBLI_ILLUSTRATION = "ghibli_illustration"
    VECTOR_FLAT = "vector_flat"
    GRAPHIC_VECTOR = "graphic_vector"
    ANIMATED = "animated"


class GateV00Verdict(str, Enum):
    """Gate V-00 verdict outcomes per FR-VIS-13 §4 Stage 4."""
    GATE_V00_PASS = "GATE_V00_PASS"
    GATE_V00_FAIL = "GATE_V00_FAIL"
    GATE_V00_ESCALATE = "GATE_V00_ESCALATE"


class ViolationType(str, Enum):
    """All 10 error types per FR-VIS-13 §7 Task 8."""
    CAROUSEL_GHIBLI_VIOLATION = "CAROUSEL_GHIBLI_VIOLATION"
    OBSERVATIONAL_HUMOR_AI_VIOLATION = "OBSERVATIONAL_HUMOR_AI_VIOLATION"
    NAMED_PERSON_TIER_VIOLATION = "NAMED_PERSON_TIER_VIOLATION"
    POLL_PHOTOGRAPHIC_VIOLATION = "POLL_PHOTOGRAPHIC_VIOLATION"
    ASPECT_RATIO_FORMAT_VIOLATION = "ASPECT_RATIO_FORMAT_VIOLATION"
    STYLE_IMAGE_TYPE_CONFLICT = "STYLE_IMAGE_TYPE_CONFLICT"
    MANDATORY_STYLE_CONFLICT = "MANDATORY_STYLE_CONFLICT"
    MISSING_IMAGE_TYPE = "MISSING_IMAGE_TYPE"
    INVALID_IMAGE_TYPE = "INVALID_IMAGE_TYPE"
    LEGACY_VCB_UPGRADE_REQUIRED = "LEGACY_VCB_UPGRADE_REQUIRED"


class OperatorReviewStatus(str, Enum):
    """Status for escalated compositions per FR-VIS-13 §4 Stage 4 Step 3."""
    PENDING_OPERATOR_REVIEW = "PENDING_OPERATOR_REVIEW"


class FormatAdapterError(str, Enum):
    """Error types for the visual format constraint adapter per FR-VIS-07 §7 Task 5."""
    FORMAT_NOT_RECOGNIZED = "FORMAT_NOT_RECOGNIZED"
    REGISTRY_INTEGRITY_ERROR = "REGISTRY_INTEGRITY_ERROR"
    MISSING_CONTENT_FORMAT = "MISSING_CONTENT_FORMAT"
    DIMENSION_OVERRIDE_VIOLATION = "DIMENSION_OVERRIDE_VIOLATION"
    LEGACY_FORMAT_DERIVATION = "LEGACY_FORMAT_DERIVATION"


class StyleScopeError(str, Enum):
    """Error types for the style scoping adapter per FR-VIS-08 §7 Task 6."""
    STYLE_VIOLATION = "STYLE_VIOLATION"
    SATURATION_VIOLATION = "SATURATION_VIOLATION"
    GRAMMAR_SYSTEM_MISMATCH = "GRAMMAR_SYSTEM_MISMATCH"
    DIRECTIVE_TAMPERING_DETECTED = "DIRECTIVE_TAMPERING_DETECTED"
    LEGACY_STYLE_DEFAULT = "LEGACY_STYLE_DEFAULT"
    FORMAT_NOT_IN_MATRIX = "FORMAT_NOT_IN_MATRIX"


# ─────────────────────────────────────────────────────
# CONSTANTS — Spec Section 4
# ─────────────────────────────────────────────────────

# FR-VIS-13 §4 Stage 4 Step 3: max 2 revision cycles before escalation
MAX_REVISION_CYCLES: int = 2

# FR-VIS-13 §4 Stage 2 Rule V00-R01: carousel format prefixes
CAROUSEL_FORMAT_PREFIXES: tuple[str, ...] = ("carousel_",)

# FR-VIS-13 §4 Stage 2 Rule V00-R02: observational humor formats
OBSERVATIONAL_HUMOR_FORMATS: frozenset[str] = frozenset({
    "single_observational_humor",
    "single_observational_humor_square",
})

# FR-VIS-13 §4 Stage 2 Rule V00-R02: allowed image types for obs humor
OBSERVATIONAL_HUMOR_ALLOWED_TYPES: frozenset[str] = frozenset({
    ImageType.TIER_1_REAL_PERSON.value,
    ImageType.TIER_2_STOCK_ENVIRONMENTAL.value,
    ImageType.TIER_2_STOCK_CONTEXTUAL.value,
    ImageType.TIER_2_STOCK_ABSTRACT.value,
})

# FR-VIS-13 §4 Stage 2 Rule V00-R04: poll formats
POLL_FORMATS: frozenset[str] = frozenset({
    "poll_archetypical",
    "poll_stereotypical",
    "poll_controversial_dilemma",
})

# FR-VIS-13 §4 Stage 2 Rule V00-R04: allowed image types for polls
POLL_ALLOWED_TYPES: frozenset[str] = frozenset({
    ImageType.GRAPHIC_VECTOR.value,
    ImageType.TIER_3_AI_REALISTIC.value,
})

# FR-VIS-13 §4 Stage 2 Rule V00-R05: formats that allow 1:1 aspect ratio
SQUARE_ALLOWED_FORMATS: frozenset[str] = frozenset({
    "single_tweet_quote",
    "single_supervisual",
    "single_conceptual_contrast_simultaneous",
    "single_observational_humor_square",
})

# FR-VIS-13 §4 Stage 3: Image Type → Implied Style mapping
IMAGE_TYPE_TO_IMPLIED_STYLES: dict[str, list[str]] = {
    ImageType.TIER_1_REAL_PERSON.value: [
        ImpliedStyle.REAL_PHOTOGRAPHY_ONLY.value,
    ],
    ImageType.TIER_2_STOCK_ENVIRONMENTAL.value: [
        ImpliedStyle.REAL_PHOTOGRAPHY_ONLY.value,
    ],
    ImageType.TIER_2_STOCK_CONTEXTUAL.value: [
        ImpliedStyle.REAL_PHOTOGRAPHY_ONLY.value,
    ],
    ImageType.TIER_2_STOCK_ABSTRACT.value: [
        ImpliedStyle.REAL_PHOTOGRAPHY_ONLY.value,
        ImpliedStyle.GRAPHIC_VECTOR.value,
    ],
    ImageType.TIER_3_AI_REALISTIC.value: [
        ImpliedStyle.SEMI_REALISTIC_DIGITAL.value,
        ImpliedStyle.CINEMATIC_COLOR_GRADED.value,
    ],
    ImageType.TIER_4_AI_GHIBLI.value: [
        ImpliedStyle.GHIBLI_ILLUSTRATION.value,
    ],
    ImageType.GRAPHIC_VECTOR.value: [
        ImpliedStyle.VECTOR_FLAT.value,
    ],
    ImageType.ANIMATED_GIF.value: [
        ImpliedStyle.ANIMATED.value,
    ],
}

# FR-VIS-13 §4 Stage 1 Step 3: valid image type strings
VALID_IMAGE_TYPE_VALUES: frozenset[str] = frozenset(
    member.value for member in ImageType
)


# ─────────────────────────────────────────────────────
# INPUT MODELS — Spec Section 4 Stages 1-3
# ─────────────────────────────────────────────────────

class VCBSlideAssignment(BaseModel):
    """A single slide's assignment from Abel's VCB.

    Per FR-VIS-13 §4 Stage 1 Steps 3-5: each slide has an image_type,
    optional named_person_reference, and aspect_ratio_template.
    """
    slide_index: int = Field(..., ge=0, description="Zero-based slide index")
    image_type: Optional[str] = Field(
        default=None,
        description="Image type assignment from Abel. None triggers MISSING_IMAGE_TYPE.",
    )
    named_person_reference: Optional[str] = Field(
        default=None,
        description="Named person referenced on this slide (e.g. 'Brené Brown'). "
                    "Non-null triggers V00-R03 check.",
    )
    aspect_ratio_template: str = Field(
        default="4:5",
        description="Aspect ratio template for this slide.",
    )


class PerSlideDimension(BaseModel):
    """Per-slide pixel dimensions per FR-VIS-07 §5 Format_Constraint_Envelope.json."""
    slide_index: int = Field(..., ge=0, description="Zero-based slide index")
    width_px: int = Field(..., gt=0, description="Exact pixel width for this slide")
    height_px: int = Field(..., gt=0, description="Exact pixel height for this slide")


class FormatRegistryEntry(BaseModel):
    """A single entry in the Format_Constraint_Registry per FR-VIS-07 §5."""
    width_px: int = Field(..., gt=0, description="Exact pixel width (e.g. 1080)")
    height_px: int = Field(..., gt=0, description="Exact pixel height (e.g. 1350)")
    aspect_ratio: str = Field(..., description="Human-readable ratio (e.g. '4:5')")
    dpi: int = Field(default=72, gt=0, description="Dots per inch (72 digital, 300 print)")
    color_space: str = Field(default="sRGB", description="Color space for export")
    bleed_zone_px: int = Field(default=0, ge=0, description="Edge bleed for carousel stitch alignment")


class FormatConstraintEnvelope(BaseModel):
    """Sealed format constraint from FR-VIS-07.

    Per FR-VIS-07 §4 Stage 2: the adapter assembles a locked envelope
    containing exact pixel dimensions, aspect ratio, DPI, color space,
    and bleed zone for every slide in the composition.

    Per FR-VIS-13 §3: Gate V-00 consumes the envelope for aspect ratio
    and format validation.

    All dimensional fields default to None for backward compatibility
    with FR-VIS-13 tests that only need content_format and aspect_ratio.
    """
    envelope_id: str = Field(
        default_factory=lambda: f"FCE-{uuid4().hex[:8].upper()}",
        description="Unique identifier for this format constraint envelope.",
    )
    content_format: str = Field(
        ...,
        description="Content format identifier (e.g. 'carousel_dopamine_cliff', "
                    "'single_observational_humor', 'poll_archetypical').",
    )
    aspect_ratio: str = Field(
        default="4:5",
        description="Locked aspect ratio (4:5, 9:16, or 1:1).",
    )
    total_slides: int = Field(
        ..., ge=1,
        description="Total number of slides in this composition.",
    )
    # ── FR-VIS-07 dimensional fields (all optional for backward compat) ──
    width_px: Optional[int] = Field(
        default=None, gt=0,
        description="Exact pixel width (e.g. 1080). Set by VIS-07 adapter.",
    )
    height_px: Optional[int] = Field(
        default=None, gt=0,
        description="Exact pixel height (e.g. 1350). Set by VIS-07 adapter.",
    )
    dpi: Optional[int] = Field(
        default=None, gt=0,
        description="Dots per inch (72 for digital, 300 for print-ready).",
    )
    color_space: Optional[str] = Field(
        default=None,
        description="Color space (always 'sRGB' for digital social delivery).",
    )
    bleed_zone_px: Optional[int] = Field(
        default=None, ge=0,
        description="Edge bleed for carousel stitch alignment (40px carousels, 0px singles).",
    )
    per_slide_dimensions: Optional[list[PerSlideDimension]] = Field(
        default=None,
        description="Array of per-slide {slide_index, width_px, height_px}.",
    )
    seal_hash: Optional[str] = Field(
        default=None,
        description="SHA-256 hash of the assembled envelope for immutability enforcement.",
    )
    receipt_chain_block: Optional[str] = Field(
        default=None,
        description="Receipt chain block ID for this envelope emission.",
    )
    timestamp_utc: Optional[str] = Field(
        default=None,
        description="ISO 8601 UTC timestamp of envelope creation.",
    )


class StyleConstraintDirective(BaseModel):
    """Sealed style constraint directive from FR-VIS-08.

    Per FR-VIS-08 §4: the style scoping adapter evaluates the content_format
    against the Style_Scope_Matrix and emits a directive specifying permitted,
    prohibited, and mandatory styles plus grammar system routing.

    Per FR-VIS-13 §3: Gate V-00 consumes the directive for style cross-validation.

    All FR-VIS-08-specific fields default to None for backward compatibility
    with FR-VIS-13 tests.
    """
    directive_id: str = Field(
        default_factory=lambda: f"SCD-{uuid4().hex[:8].upper()}",
        description="Unique identifier for this style constraint directive.",
    )
    permitted_styles: list[str] = Field(
        default_factory=list,
        description="Styles permitted for this composition.",
    )
    prohibited_styles: list[str] = Field(
        default_factory=list,
        description="Styles explicitly prohibited for this composition.",
    )
    mandatory_style: Optional[str] = Field(
        default=None,
        description="If set, this style MUST be used. Overrides permitted_styles.",
    )
    grammar_system: Optional[str] = Field(
        default=None,
        description="Grammar system: 'cinematic', 'illustrated', 'documentary', or 'hybrid'.",
    )
    # ── FR-VIS-08 fields (all optional for backward compat) ──
    content_format: Optional[str] = Field(
        default=None,
        description="The content format this directive applies to.",
    )
    content_output_id: Optional[str] = Field(
        default=None,
        description="Content output ID for traceability.",
    )
    format_constraint_envelope_id: Optional[str] = Field(
        default=None,
        description="ID of the format constraint envelope from FR-VIS-07.",
    )
    saturation_ceiling_pct: Optional[int] = Field(
        default=None, ge=0, le=100,
        description="Maximum saturation percentage (e.g. 35 for Worst Case Scenario).",
    )
    saturation_floor_pct: Optional[int] = Field(
        default=None, ge=0, le=100,
        description="Minimum saturation percentage (e.g. 20 for Worst Case Scenario).",
    )
    seal_hash: Optional[str] = Field(
        default=None,
        description="SHA-256 hash for immutability enforcement.",
    )
    receipt_chain_block: Optional[str] = Field(
        default=None,
        description="Receipt chain block ID for this directive emission.",
    )
    timestamp_utc: Optional[str] = Field(
        default=None,
        description="ISO 8601 UTC timestamp of directive creation.",
    )


class VCBInput(BaseModel):
    """Complete VCB input to Gate V-00.

    Per FR-VIS-13 §4 Stage 1: the completed VCB from Abel containing
    per-slide image_type assignments plus format and style constraints.
    """
    vcb_id: str = Field(..., description="Visual Composition Brief ID")
    content_output_id: str = Field(..., description="Content Output ID from DEP-ENG-011")
    coach_acronym: str = Field(..., min_length=2, max_length=4, description="ADR-01 coach scope")
    slides: list[VCBSlideAssignment] = Field(
        ..., min_length=1,
        description="Per-slide assignments from Abel.",
    )
    format_envelope: FormatConstraintEnvelope = Field(
        ...,
        description="Sealed format constraint from FR-VIS-07.",
    )
    style_directive: StyleConstraintDirective = Field(
        ...,
        description="Sealed style constraint from FR-VIS-08.",
    )
    revision_count: int = Field(
        default=0, ge=0,
        description="Number of times this VCB has been returned to Abel for revision. "
                    "Per FR-VIS-13 §4 Stage 4: >= 2 triggers escalation.",
    )


# ─────────────────────────────────────────────────────
# OUTPUT MODELS — Spec Section 5
# ─────────────────────────────────────────────────────

class SlideValidationSummary(BaseModel):
    """Per-slide validation result per FR-VIS-13 §5 output schema."""
    slide_index: int = Field(..., ge=0)
    image_type: Optional[str] = Field(default=None)
    format_check: str = Field(default="PASS", pattern=r"^(PASS|FAIL)$")
    style_check: str = Field(default="PASS", pattern=r"^(PASS|FAIL)$")


class GateV00Violation(BaseModel):
    """A single violation entry per FR-VIS-13 §5 Gate_V00_Violation_Report.json."""
    rule_id: str = Field(..., description="Rule ID (e.g. 'V00-R01')")
    slide_index: int = Field(..., ge=0, description="Zero-based slide index")
    assigned_image_type: Optional[str] = Field(
        default=None,
        description="The image_type that was assigned to the violating slide.",
    )
    violation_type: str = Field(
        ...,
        description="Violation type enum value.",
    )
    explanation: str = Field(
        ...,
        description="Human-readable explanation of the violation.",
    )
    suggested_correction: str = Field(
        ...,
        description="Suggested corrective action for Abel.",
    )


class GateV00Result(BaseModel):
    """Gate V-00 complete result per FR-VIS-13 §5 Gate_V00_Result.json."""
    gate_id: str = Field(
        default_factory=lambda: f"V00-{uuid4().hex[:12].upper()}",
        description="Unique gate execution ID.",
    )
    content_output_id: str = Field(..., description="Content Output ID")
    content_format: str = Field(..., description="Content format from envelope")
    verdict: str = Field(..., description="GATE_V00_PASS | GATE_V00_FAIL | GATE_V00_ESCALATE")
    revision_count: int = Field(default=0, ge=0)
    violations: list[GateV00Violation] = Field(default_factory=list)
    slide_validation_summary: list[SlideValidationSummary] = Field(default_factory=list)
    format_envelope_id: str = Field(..., description="ID of the format constraint envelope used")
    style_directive_id: str = Field(..., description="ID of the style constraint directive used")
    receipt_chain_block: str = Field(
        default="",
        description="Receipt chain block ID for this gate execution.",
    )
    timestamp_utc: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO 8601 UTC timestamp of gate execution.",
    )
    operator_review_status: Optional[str] = Field(
        default=None,
        description="Set to PENDING_OPERATOR_REVIEW on escalation.",
    )
    violation_history: Optional[list[list[GateV00Violation]]] = Field(
        default=None,
        description="Full violation history from all revision attempts (on escalation only).",
    )


# ─────────────────────────────────────────────────────
# FR-VIS-07 INPUT/OUTPUT MODELS
# ─────────────────────────────────────────────────────

class ContentOutputInput(BaseModel):
    """Upstream content output from DEP-ENG-011 consumed by VIS-07 adapter.

    Per FR-VIS-07 §4 Stage 1: the adapter receives the finalized content
    output package and extracts the content_format field.
    """
    content_output_id: str = Field(
        ...,
        description="Content Output ID from script compilation (DEP-ENG-011).",
    )
    content_format: Optional[str] = Field(
        default=None,
        description="Format designation set during script compilation. None triggers "
                    "legacy fallback via recipe_id cross-reference.",
    )
    slide_count: int = Field(
        ..., ge=1,
        description="Number of slides in the composition.",
    )
    recipe_id: Optional[str] = Field(
        default=None,
        description="Legacy recipe ID for backward compatibility cross-reference. "
                    "Per FR-VIS-07 §6: if content_format is missing, "
                    "recipe_id → content_format derivation is attempted.",
    )
    coach_acronym: str = Field(
        ..., min_length=2, max_length=4,
        description="ADR-01 coach scope identifier.",
    )


class FormatAdapterResult(BaseModel):
    """Output of the visual format constraint adapter per FR-VIS-07 §5.

    Contains either a sealed format_constraint_envelope (on success)
    or an error payload (on rejection).
    """
    success: bool = Field(
        ...,
        description="True if envelope was assembled successfully.",
    )
    envelope: Optional[FormatConstraintEnvelope] = Field(
        default=None,
        description="The sealed format constraint envelope. None on error.",
    )
    error_type: Optional[str] = Field(
        default=None,
        description="Error type from FormatAdapterError enum. None on success.",
    )
    error_detail: Optional[str] = Field(
        default=None,
        description="Human-readable error explanation. None on success.",
    )
    content_output_id: Optional[str] = Field(
        default=None,
        description="The content output ID from the input (for error traceability).",
    )
    warnings: list[str] = Field(
        default_factory=list,
        description="Non-fatal warnings (e.g. LEGACY_FORMAT_DERIVATION).",
    )
    receipt_chain_block: str = Field(
        default="",
        description="Receipt chain block ID for this adapter execution.",
    )
    timestamp_utc: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO 8601 UTC timestamp of adapter execution.",
    )


# ─────────────────────────────────────────────────────
# FR-VIS-07 LEGACY RECIPE → FORMAT MAPPING
# Per FR-VIS-07 §6 Backward Compatibility
# ─────────────────────────────────────────────────────

RECIPE_ID_TO_FORMAT: dict[str, str] = {
    "RCP-CAROUSEL-DOPAMINE-CLIFF-001": "carousel_dopamine_cliff",
    "RCP-CAROUSEL-LISTICLE-001": "carousel_listicle",
    "RCP-CAROUSEL-TIMELINE-001": "carousel_timeline",
    "RCP-CAROUSEL-COMPARISON-001": "carousel_comparison",
    "RCP-SINGLE-OBS-HUMOR-001": "single_observational_humor",
    "RCP-SINGLE-WORST-CASE-001": "single_worst_case",
    "RCP-SINGLE-CONTRAST-001": "single_conceptual_contrast",
    "RCP-POLL-ARCHETYPICAL-001": "poll_archetypical",
    "RCP-POLL-STEREOTYPICAL-001": "poll_stereotypical",
    "RCP-POLL-DILEMMA-001": "poll_controversial_dilemma",
    "RCP-SINGLE-TWEET-QUOTE-001": "single_tweet_quote",
    "RCP-SINGLE-SUPERVISUAL-001": "single_supervisual",
    "RCP-SINGLE-CONTRAST-SIM-001": "single_conceptual_contrast_simultaneous",
    "RCP-SINGLE-OBS-HUMOR-SQ-001": "single_observational_humor_square",
    "RCP-NINE-GRID-001": "nine_grid_accumulation",
}


# ─────────────────────────────────────────────────────
# FR-VIS-08 STYLE SCOPING MODELS
# ─────────────────────────────────────────────────────

class StyleParameters(BaseModel):
    """Style-specific parameters per FR-VIS-08 §5 Style_Scope_Matrix entry."""
    saturation_ceiling_pct: Optional[int] = Field(
        default=None, ge=0, le=100,
        description="Maximum saturation percentage (e.g. 35 for Worst Case).",
    )
    saturation_floor_pct: Optional[int] = Field(
        default=None, ge=0, le=100,
        description="Minimum saturation percentage (e.g. 20 for Worst Case).",
    )
    grammar_system: str = Field(
        ...,
        description="Grammar system: 'cinematic', 'illustrated', 'documentary', or 'hybrid'.",
    )


class StyleScopeMatrixEntry(BaseModel):
    """A single entry in the Style_Scope_Matrix per FR-VIS-08 §5."""
    permitted_styles: list[str] = Field(
        ..., min_length=1,
        description="Styles permitted for this content format.",
    )
    prohibited_styles: list[str] = Field(
        default_factory=list,
        description="Styles explicitly prohibited for this content format.",
    )
    mandatory_style: Optional[str] = Field(
        default=None,
        description="If set, this style MUST be used.",
    )
    style_parameters: StyleParameters = Field(
        ...,
        description="Format-specific style parameters.",
    )


class StyleValidationResult(BaseModel):
    """Result of pre-Abel style validation per FR-VIS-08 §4 Stage 3."""
    valid: bool = Field(
        ...,
        description="True if the style assignment passes all checks.",
    )
    error_type: Optional[str] = Field(
        default=None,
        description="Error type from StyleScopeError enum. None on success.",
    )
    error_detail: Optional[str] = Field(
        default=None,
        description="Human-readable error explanation. None on success.",
    )
    content_format: Optional[str] = Field(
        default=None,
        description="The content format being validated.",
    )
    assigned_style: Optional[str] = Field(
        default=None,
        description="The style Abel attempted to assign.",
    )
    permitted_styles: list[str] = Field(
        default_factory=list,
        description="Styles that would have been accepted.",
    )


# ─────────────────────────────────────────────────────
# SUGGESTED CORRECTIONS — Spec Section 8 (AC1-AC4)
# ─────────────────────────────────────────────────────

SUGGESTED_CORRECTIONS: dict[str, str] = {
    ViolationType.CAROUSEL_GHIBLI_VIOLATION.value: (
        "Change image_type to 'tier_3_ai_realistic' or 'tier_2_stock_contextual'"
    ),
    ViolationType.OBSERVATIONAL_HUMOR_AI_VIOLATION.value: (
        "Change image_type to 'tier_1_real_person' or 'tier_2_stock_contextual'"
    ),
    ViolationType.NAMED_PERSON_TIER_VIOLATION.value: (
        "Change image_type to 'tier_1_real_person'"
    ),
    ViolationType.POLL_PHOTOGRAPHIC_VIOLATION.value: (
        "Change image_type to 'graphic_vector' or 'tier_3_ai_realistic'"
    ),
    ViolationType.ASPECT_RATIO_FORMAT_VIOLATION.value: (
        "Change aspect_ratio to '4:5' or '9:16', or change content_format to an "
        "approved 1:1 format (single_tweet_quote, single_supervisual, "
        "single_conceptual_contrast_simultaneous, single_observational_humor_square)"
    ),
    ViolationType.STYLE_IMAGE_TYPE_CONFLICT.value: (
        "Change image_type to one whose implied style is not prohibited by the style directive"
    ),
    ViolationType.MANDATORY_STYLE_CONFLICT.value: (
        "Change image_type to one whose implied style matches the mandatory style directive"
    ),
    ViolationType.MISSING_IMAGE_TYPE.value: (
        "Add a valid image_type field to this slide"
    ),
    ViolationType.INVALID_IMAGE_TYPE.value: (
        "Replace with a valid image_type from the approved enum"
    ),
    ViolationType.LEGACY_VCB_UPGRADE_REQUIRED.value: (
        "Reprocess VCB with current schema that includes mandatory image_type assignment per slide"
    ),
}


# ─────────────────────────────────────────────────────
# FR-VIS-02 TIAR INTEGRATION MODELS
# ─────────────────────────────────────────────────────

# §4 Stage 1 Step 4: TIRS thresholds and decay stage partitioning
TIRS_IN_DISTRIBUTION_MIN: float = 7.0
TIRS_EXPIRED_MAX: float = 5.0
MIN_TIAR_NOUNS_PER_TEXT_SLIDE: int = 3


class DecayStage(str, Enum):
    """Noun lifecycle decay stages per FR-VIS-02 §2 / TIAR research."""
    IN_DISTRIBUTION = "in_distribution"
    TRIBAL_POTENTIAL = "tribal_potential"
    DECAY_APPROACHING = "decay_approaching"
    EXPIRED = "expired"


class TIARAdapterError(str, Enum):
    """Error types for the TIAR adapter per FR-VIS-02 §7."""
    NOUN_EXPIRED_SINCE_SCRIPT = "NOUN_EXPIRED_SINCE_SCRIPT"
    TIAR_CACHE_STALE = "TIAR_CACHE_STALE"
    TIAR_STALE_DOWNSTREAM = "TIAR_STALE_DOWNSTREAM"
    TIAR_NOT_INITIALIZED = "TIAR_NOT_INITIALIZED"
    TIAR_VALIDATION_MISSING = "TIAR_VALIDATION_MISSING"
    EXPIRED_NOUN_IN_TEXT = "EXPIRED_NOUN_IN_TEXT"


class TIARNounEntry(BaseModel):
    """A single noun entry from the TIAR per FR-VIS-02 §5."""
    noun: str = Field(
        ...,
        description="The tribal noun phrase (may be multi-word).",
    )
    tirs_score: float = Field(
        ..., ge=0.0, le=10.0,
        description="Tribal Imageability Rating Scale score (0-10).",
    )
    decay_stage: DecayStage = Field(
        ...,
        description="Current lifecycle stage.",
    )
    last_measured_date: Optional[str] = Field(
        default=None,
        description="ISO date of last TIRS measurement.",
    )
    usage_count_30d: Optional[int] = Field(
        default=None, ge=0,
        description="Usage count in the last 30 days.",
    )
    shannon_entropy: Optional[float] = Field(
        default=None,
        description="Shannon entropy of usage distribution.",
    )
    is_emerging: bool = Field(
        default=False,
        description="True if decay_stage is tribal_potential.",
    )
    decay_warning: bool = Field(
        default=False,
        description="True if decay_stage is decay_approaching.",
    )
    expired_since: Optional[str] = Field(
        default=None,
        description="ISO date when the noun was marked expired.",
    )


class TIARInjectionResult(BaseModel):
    """Result of upstream TIAR injection per FR-VIS-02 §5."""
    injection_id: str = Field(
        default_factory=lambda: f"TIAR-INJ-{uuid4().hex[:8].upper()}",
        description="Unique identifier for this injection.",
    )
    coach_id: str = Field(
        ...,
        description="Coach identifier.",
    )
    tribe_id: str = Field(
        default="default",
        description="Tribe identifier.",
    )
    query_timestamp_utc: str = Field(
        ...,
        description="ISO timestamp of the TIAR query.",
    )
    active_noun_vocabulary: list[TIARNounEntry] = Field(
        default_factory=list,
        description="Nouns that are in_distribution, tribal_potential, or decay_approaching.",
    )
    blocked_noun_list: list[TIARNounEntry] = Field(
        default_factory=list,
        description="Expired nouns that must not appear in text.",
    )
    vocabulary_size_active: int = Field(
        default=0,
        description="Count of active vocabulary nouns.",
    )
    vocabulary_size_blocked: int = Field(
        default=0,
        description="Count of blocked nouns.",
    )
    cache_status: str = Field(
        default="FRESH",
        description="'FRESH' or 'TIAR_CACHE_STALE'.",
    )
    receipt_chain_block: Optional[str] = Field(
        default=None,
        description="Receipt chain block ID.",
    )


class NounAuditEntry(BaseModel):
    """Per-noun audit data within a slide per FR-VIS-02 §5."""
    noun: str = Field(
        ...,
        description="The noun found in the text.",
    )
    tirs_score: Optional[float] = Field(
        default=None,
        description="Current TIRS score (None if not in registry).",
    )
    decay_stage: Optional[DecayStage] = Field(
        default=None,
        description="Current decay stage (None if not in registry).",
    )
    position_in_text: Optional[int] = Field(
        default=None, ge=0,
        description="Character offset in the slide text.",
    )
    last_measured_date: Optional[str] = Field(
        default=None,
        description="ISO date of last TIRS measurement.",
    )
    status: str = Field(
        default="NOUN_ACTIVE",
        description="One of: NOUN_ACTIVE, NOUN_DECAY_WARNING, NOUN_EXPIRED_SINCE_SCRIPT, NOUN_NOT_IN_REGISTRY.",
    )


class SlideNounAudit(BaseModel):
    """Per-slide noun audit per FR-VIS-02 §5."""
    slide_index: int = Field(
        ..., ge=0,
        description="Slide index (0-based).",
    )
    nouns_found: list[NounAuditEntry] = Field(
        default_factory=list,
        description="All TIAR nouns found in this slide's text.",
    )
    nouns_not_in_registry: list[str] = Field(
        default_factory=list,
        description="Generic nouns not in the TIAR (informational).",
    )
    violations: list[str] = Field(
        default_factory=list,
        description="NOUN_EXPIRED_SINCE_SCRIPT violation strings.",
    )
    warnings: list[str] = Field(
        default_factory=list,
        description="NOUN_DECAY_WARNING strings.",
    )


class NounDecayAudit(BaseModel):
    """Complete noun decay audit for VPO per FR-VIS-02 §5."""
    audit_id: str = Field(
        default_factory=lambda: f"TIAR-AUD-{uuid4().hex[:8].upper()}",
        description="Unique identifier for this audit.",
    )
    content_output_id: str = Field(
        ...,
        description="Content output ID from the composition.",
    )
    slide_audits: list[SlideNounAudit] = Field(
        default_factory=list,
        description="Per-slide audit entries.",
    )
    total_tiar_nouns: int = Field(
        default=0,
        description="Total TIAR nouns found across all slides.",
    )
    total_active: int = Field(
        default=0,
        description="Total active (in_distribution + tribal_potential) nouns.",
    )
    total_decay_warning: int = Field(
        default=0,
        description="Total decay_approaching nouns.",
    )
    total_expired: int = Field(
        default=0,
        description="Total expired nouns detected.",
    )
    receipt_chain_block: Optional[str] = Field(
        default=None,
        description="Receipt chain block ID.",
    )


class TIARValidationResult(BaseModel):
    """Result of downstream TIAR re-validation per FR-VIS-02 §4 Stage 2."""
    valid: bool = Field(
        ...,
        description="True if no expired nouns found in the VCB.",
    )
    noun_decay_audit: Optional[NounDecayAudit] = Field(
        default=None,
        description="Complete per-slide noun decay audit.",
    )
    expired_nouns: list[str] = Field(
        default_factory=list,
        description="Nouns that expired between script generation and VCB finalization.",
    )
    replacement_nouns: list[TIARNounEntry] = Field(
        default_factory=list,
        description="Active replacement nouns offered for expired ones.",
    )
    error_type: Optional[str] = Field(
        default=None,
        description="Error type from TIARAdapterError. None on success.",
    )
    error_detail: Optional[str] = Field(
        default=None,
        description="Human-readable error explanation.",
    )
    tiar_status: str = Field(
        default="TIAR_VALID",
        description="'TIAR_VALID', 'TIAR_DECAY_DETECTED', 'TIAR_NOT_INITIALIZED', etc.",
    )
    cache_status: str = Field(
        default="FRESH",
        description="'FRESH', 'TIAR_CACHE_STALE', or 'TIAR_STALE_DOWNSTREAM'.",
    )
    warnings: list[str] = Field(
        default_factory=list,
        description="Non-blocking warnings.",
    )


# ═══════════════════════════════════════════════════════════════
# FR-VIS-09  —  Image Sourcing Hierarchy  (Phase 2B, Spec 5)
# ═══════════════════════════════════════════════════════════════

# ── constants ──
ADEQUACY_RELEVANCE_THRESHOLD: float = 0.7
"""Stock image must score ≥ 0.7 relevance to be accepted (§3)."""

MIN_RESOLUTION_PX: int = 1080
"""Stock image shortest edge must be ≥ 1080 px (§3)."""

BATCH_ESCALATION_THRESHOLD: float = 0.5
"""> 50 % of slides PENDING_HUMAN_REVIEW → entire composition escalated (§4 Stage 3)."""

TIER4_PERMITTED_FORMATS: frozenset[str] = frozenset({
    "carousel_conceptual_contrast",
    "carousel_supervisual",
    "supervisual",
    "conceptual_contrast",
})
"""Only these formats may route slides to Tier 4 Ghibli LoRA (§4 Stage 1)."""

COMPATIBLE_LICENSES: frozenset[str] = frozenset({
    "creative_commons",
    "editorial",
    "licensed_stock",
    "unsplash_license",
    "pexels_license",
    "pixabay_license",
})
"""Acceptable license types for Tier-2 stock imagery (§4 Stage 2)."""


class SourceTier(str, Enum):
    """Four-tier image sourcing cascade per §2."""
    TIER_1_REAL_PERSON = "tier_1_real_person"
    TIER_2_STOCK = "tier_2_stock"
    TIER_3_AI_REALISTIC = "tier_3_ai_realistic"
    TIER_4_AI_GHIBLI = "tier_4_ai_ghibli"


class SlideResolutionStatus(str, Enum):
    """Per-slide resolution status per §4 Stage 3."""
    RESOLVED = "RESOLVED"
    PENDING_AI_GENERATION = "PENDING_AI_GENERATION"
    PENDING_HUMAN_REVIEW = "PENDING_HUMAN_REVIEW"
    PENDING_OPERATOR_REVIEW = "PENDING_OPERATOR_REVIEW"


class ImageSourcingError(str, Enum):
    """Error types emitted by the sourcing hierarchy."""
    INCOMPLETE_VCB = "INCOMPLETE_VCB"
    STOCK_SEARCH_FAILED = "STOCK_SEARCH_FAILED"
    STOCK_BELOW_THRESHOLD = "STOCK_BELOW_THRESHOLD"
    NAMED_PERSON_NOT_FOUND = "NAMED_PERSON_NOT_FOUND"
    TIER4_FORMAT_NOT_PERMITTED = "TIER4_FORMAT_NOT_PERMITTED"
    AI_GENERATION_FAILED = "AI_GENERATION_FAILED"
    BATCH_ESCALATION = "BATCH_ESCALATION"
    RESOLUTION_BELOW_MIN = "RESOLUTION_BELOW_MIN"
    LICENSE_INCOMPATIBLE = "LICENSE_INCOMPATIBLE"
    LEGACY_SOURCING_DEFAULT = "LEGACY_SOURCING_DEFAULT"


class TierRoutingEntry(BaseModel):
    """Per-slide tier routing decision — Stage 1 output (§4 Stage 1)."""
    slide_index: int = Field(
        ..., ge=0,
        description="Zero-based slide index in the VCB.",
    )
    image_type: str = Field(
        ...,
        description="Slide image_type from VCB (validated by Gate V-00).",
    )
    named_person_reference: Optional[str] = Field(
        default=None,
        description="Named person reference — non-null routes to Tier 1.",
    )
    initial_tier: SourceTier = Field(
        ...,
        description="First tier to attempt for this slide.",
    )
    fallback_tiers: list[SourceTier] = Field(
        default_factory=list,
        description="Ordered list of fallback tiers if initial tier fails.",
    )
    format_permits_tier4: bool = Field(
        default=False,
        description="True if the content format permits Tier 4 Ghibli.",
    )


class StockSearchResult(BaseModel):
    """Result of a Tier-2 stock image search attempt (§4 Stage 2)."""
    attempted: bool = Field(
        default=False,
        description="Whether a stock search was attempted.",
    )
    best_relevance_score: float = Field(
        default=0.0,
        description="Best relevance score from stock search results.",
    )
    resolution_px: Optional[str] = Field(
        default=None,
        description="Resolution of the best match (e.g. '2400x3200').",
    )
    licensing_type: Optional[str] = Field(
        default=None,
        description="License type of the best match.",
    )
    reason_accepted: Optional[str] = Field(
        default=None,
        description="Reason the image was accepted (if accepted).",
    )
    reason_rejected: Optional[str] = Field(
        default=None,
        description="Reason the image was rejected (if rejected).",
    )
    source_api: Optional[str] = Field(
        default=None,
        description="API that produced the best result (unsplash, pexels, etc.).",
    )


class SlideResolution(BaseModel):
    """Per-slide image resolution result — Stage 2 output (§4 Stage 2)."""
    slide_index: int = Field(
        ..., ge=0,
        description="Zero-based slide index.",
    )
    image_type: str = Field(
        ...,
        description="Original image_type from VCB.",
    )
    resolved_tier: Optional[int] = Field(
        default=None, ge=1, le=4,
        description="Final resolved tier (1-4), or None if pending.",
    )
    status: SlideResolutionStatus = Field(
        ...,
        description="Resolution status for this slide.",
    )
    image_url: Optional[str] = Field(
        default=None,
        description="Resolved image URL, or None if not yet available.",
    )
    source_api: Optional[str] = Field(
        default=None,
        description="API source (unsplash, pexels, serper, runninghub, etc.).",
    )
    relevance_score: Optional[float] = Field(
        default=None,
        description="Relevance score for the resolved image.",
    )
    resolution_px: Optional[str] = Field(
        default=None,
        description="Image resolution (e.g. '2400x3200').",
    )
    licensing_type: Optional[str] = Field(
        default=None,
        description="License type for the resolved image.",
    )
    search_terms_used: list[str] = Field(
        default_factory=list,
        description="Search terms derived from VCB tribal nouns + PAD modifiers.",
    )
    stock_search_result: Optional[StockSearchResult] = Field(
        default=None,
        description="Stock search attempt details (for audit).",
    )
    ai_generation_queued: bool = Field(
        default=False,
        description="True if slide has been queued for AI generation.",
    )
    provenance: dict = Field(
        default_factory=dict,
        description="Provenance metadata (pssl_mood, tribal_nouns, etc.).",
    )
    error_type: Optional[str] = Field(
        default=None,
        description="Error type if resolution failed.",
    )
    error_detail: Optional[str] = Field(
        default=None,
        description="Human-readable error explanation.",
    )


class ResolutionSummary(BaseModel):
    """Aggregate counts by tier and status (§5)."""
    tier_1_resolved: int = Field(default=0)
    tier_2_resolved: int = Field(default=0)
    tier_3_pending_generation: int = Field(default=0)
    tier_4_pending_generation: int = Field(default=0)
    pending_human_review: int = Field(default=0)
    pending_operator_review: int = Field(default=0)


class ImageResolutionMap(BaseModel):
    """Complete image resolution map — Stage 3 output (§5)."""
    resolution_map_id: str = Field(
        ...,
        description="Unique ID for this resolution map (IRM-{acronym}-{date}-{seq}).",
    )
    vcb_id: str = Field(
        ...,
        description="Source VCB ID.",
    )
    content_output_id: str = Field(
        ...,
        description="Content output ID.",
    )
    content_format: Optional[str] = Field(
        default=None,
        description="Content format from VCB (for Tier 4 gating).",
    )
    total_slides: int = Field(
        ..., ge=1,
        description="Total slides in the VCB.",
    )
    resolution_summary: ResolutionSummary = Field(
        default_factory=ResolutionSummary,
        description="Aggregate tier/status counts.",
    )
    per_slide_resolution: list[SlideResolution] = Field(
        default_factory=list,
        description="Per-slide resolution details.",
    )
    batch_escalated: bool = Field(
        default=False,
        description="True if >50% of slides are PENDING_HUMAN_REVIEW.",
    )
    legacy_sourcing_warning: bool = Field(
        default=False,
        description="True if VCB was missing per-slide image_type fields.",
    )
    receipt_chain_block: Optional[str] = Field(
        default=None,
        description="Receipt chain block ID for this map.",
    )
    timestamp_utc: Optional[str] = Field(
        default=None,
        description="ISO-8601 UTC timestamp.",
    )


# ═══════════════════════════════════════════════════════════════
# FR-VIS-12  —  Known Persons Registry  (Phase 2B, Spec 6)
# ═══════════════════════════════════════════════════════════════

# ── constants ──
REPETITION_WINDOW_DAYS: int = 56
"""8-week (56-day) rolling non-repetition window for person images (§3)."""


class PersonRole(str, Enum):
    """Character Lexicon role per FR0C."""
    HERO = "Hero"
    ENEMY = "Enemy"
    MENTOR = "Mentor"
    WILDCARD = "Wildcard"


class KnownPersonsError(str, Enum):
    """Error types emitted by the Known Persons Registry adapter."""
    PERSON_NOT_IN_REGISTRY = "PERSON_NOT_IN_REGISTRY"
    CONTEXT_VIOLATION = "CONTEXT_VIOLATION"
    REPETITION_VIOLATION = "REPETITION_VIOLATION"
    ALL_IMAGES_IN_WINDOW = "ALL_IMAGES_IN_WINDOW"
    REGISTRY_QUERY_TIMEOUT = "REGISTRY_QUERY_TIMEOUT"
    IMAGE_URL_BROKEN = "IMAGE_URL_BROKEN"
    AI_GENERATION_PROHIBITED = "AI_GENERATION_PROHIBITED"
    LICENSING_EXPIRED = "LICENSING_EXPIRED"


# ── context routing rules ──
CONTEXT_ROUTING_RULES: dict[str, dict[str, list[str]]] = {
    PersonRole.HERO.value: {
        "permitted": [
            "aspirational", "inspirational", "authority", "success",
            "wisdom", "transformation", "aspirational_transformation",
        ],
        "prohibited": [
            "negative_example", "failure", "cautionary_tale", "ridicule",
            "cautionary_negative",
        ],
    },
    PersonRole.ENEMY.value: {
        "permitted": [
            "cautionary_tale", "negative_exemplar", "contrast",
            "cautionary_negative", "negative_example",
        ],
        "prohibited": [
            "aspirational", "heroic", "wisdom", "endorsement",
            "aspirational_transformation", "inspirational",
        ],
    },
    PersonRole.MENTOR.value: {
        "permitted": [
            "wisdom", "teaching", "guidance", "reflection", "legacy",
            "aspirational_transformation", "inspirational",
        ],
        "prohibited": [
            "negative_example", "failure", "competition", "confrontation",
            "cautionary_negative",
        ],
    },
    PersonRole.WILDCARD.value: {
        "permitted": [],   # All contexts permitted
        "prohibited": [],  # No prohibitions (but must not imply brand endorsement)
    },
}


class CanonicalImage(BaseModel):
    """A single canonical image for a known person (§5)."""
    image_id: str = Field(
        ...,
        description="Unique image ID (KPR-IMG-###).",
    )
    source_url: Optional[str] = Field(
        default=None,
        description="Original source URL.",
    )
    r2_cached_url: Optional[str] = Field(
        default=None,
        description="Cloudflare R2 cached URL.",
    )
    licensing_type: str = Field(
        default="unknown",
        description="License type (Editorial, Creative Commons, etc.).",
    )
    licensing_source: Optional[str] = Field(
        default=None,
        description="Where the license was obtained.",
    )
    licensing_expiry: Optional[str] = Field(
        default=None,
        description="License expiry date (ISO-8601) or None for perpetual.",
    )
    resolution_px: Optional[str] = Field(
        default=None,
        description="Image resolution (e.g. '2400x3600').",
    )
    aspect_ratio: Optional[str] = Field(
        default=None,
        description="Aspect ratio (e.g. '2:3').",
    )


class ImageUsageLogEntry(BaseModel):
    """Single usage log entry for a canonical image (§5)."""
    image_id: str = Field(
        ...,
        description="The canonical image ID used.",
    )
    used_date: str = Field(
        ...,
        description="ISO-8601 date when the image was used.",
    )
    content_output_id: str = Field(
        ...,
        description="Content output that used this image.",
    )


class KnownPersonRegistryEntry(BaseModel):
    """Complete registry entry for a named person (§5)."""
    registry_entry_id: str = Field(
        ...,
        description="Unique registry entry ID (KPR-###-NAME).",
    )
    person_name: str = Field(
        ...,
        description="Full name of the person.",
    )
    person_role: PersonRole = Field(
        ...,
        description="Role from Character Lexicon (Hero/Enemy/Mentor/Wildcard).",
    )
    coach_id: str = Field(
        ...,
        description="Coach ID this entry belongs to.",
    )
    canonical_images: list[CanonicalImage] = Field(
        default_factory=list,
        description="List of canonical images for this person.",
    )
    context_routing_rules: Optional[dict[str, list[str]]] = Field(
        default=None,
        description="Permitted/prohibited context overrides (defaults to role rules).",
    )
    usage_log: list[ImageUsageLogEntry] = Field(
        default_factory=list,
        description="Historical usage log for repetition window tracking.",
    )
    added_by_operator: Optional[str] = Field(default=None)
    added_date: Optional[str] = Field(default=None)
    last_verified_date: Optional[str] = Field(default=None)
    registry_status: str = Field(default="ACTIVE")


class ContextValidationResult(BaseModel):
    """Result of context-appropriateness validation (§4 Stage 2)."""
    valid: bool = Field(
        ...,
        description="True if context is appropriate for this person's role.",
    )
    person_name: str = Field(default="")
    person_role: str = Field(default="")
    slide_context: str = Field(default="")
    violation_detail: Optional[str] = Field(
        default=None,
        description="Human-readable violation explanation.",
    )
    permitted_contexts: list[str] = Field(default_factory=list)


class RepetitionCheckResult(BaseModel):
    """Result of 8-week non-repetition window check (§4 Stage 3)."""
    clear: bool = Field(
        ...,
        description="True if selected image is outside the repetition window.",
    )
    selected_image_id: Optional[str] = Field(
        default=None,
        description="ID of the selected image (if any is clear).",
    )
    last_used_date: Optional[str] = Field(default=None)
    days_since_last_use: Optional[int] = Field(default=None)
    window_days: int = Field(default=REPETITION_WINDOW_DAYS)
    all_in_window: bool = Field(
        default=False,
        description="True if ALL canonical images are within the window.",
    )
    error_type: Optional[str] = Field(default=None)


class ResolvedPersonImage(BaseModel):
    """Final resolved person image delivered to Aurore (§5)."""
    resolution_id: str = Field(...)
    person_name: str = Field(...)
    person_role: str = Field(...)
    slide_index: int = Field(..., ge=0)
    content_output_id: str = Field(...)
    selected_image: Optional[CanonicalImage] = Field(default=None)
    context_validation: Optional[ContextValidationResult] = Field(default=None)
    repetition_check: Optional[RepetitionCheckResult] = Field(default=None)
    sourcing_tier: str = Field(default="tier_1_real_person")
    source_type: str = Field(
        default="known_persons_registry",
        description="'known_persons_registry' or 'serper_fallback'.",
    )
    pending_registry_addition: bool = Field(
        default=False,
        description="True if this was a SERPER fallback requiring operator addition.",
    )
    error_type: Optional[str] = Field(default=None)
    error_detail: Optional[str] = Field(default=None)
    receipt_chain_block: Optional[str] = Field(default=None)
    timestamp_utc: Optional[str] = Field(default=None)


# ---------------------------------------------------------------------------
# FR-VIS-10: Multi-API Image Search
# ---------------------------------------------------------------------------

# Ranking weights (§4 Stage 3)
RELEVANCE_WEIGHT: float = 0.40
TRIBAL_ALIGNMENT_WEIGHT: float = 0.30
COLOR_MATCH_WEIGHT: float = 0.20
LICENSING_WEIGHT: float = 0.10

# Dispatch configuration
API_STAGGER_MS: int = 100
API_TIMEOUT_SECONDS: int = 10
RUNNINGHUB_TIMEOUT_SECONDS: int = 600
MIN_SEARCH_RESOLUTION_PX: int = 1080

# Exponential backoff schedule for RunningHub polling (seconds)
RUNNINGHUB_POLL_SCHEDULE: list[int] = [5, 10, 20, 40, 60]


class SkillId(str, Enum):
    """The 9 composable image search skills (§4 Stage 2)."""
    UNSPLASH = "SKILL-IMG-001"
    PEXELS = "SKILL-IMG-002"
    PIXABAY = "SKILL-IMG-003"
    GIPHY = "SKILL-IMG-004"
    SERPER_GENERAL = "SKILL-IMG-005"
    SERPER_KNOWN_PERSON = "SKILL-IMG-006"
    RUNNINGHUB_REALISTIC = "SKILL-IMG-007"
    RUNNINGHUB_GHIBLI = "SKILL-IMG-008"
    PHOTO_DECK = "SKILL-IMG-009"


# Environment variable names mapped to each skill
SKILL_ENV_KEYS: dict[str, str] = {
    SkillId.UNSPLASH: "UNSPLASH_ACCESS_KEY",
    SkillId.PEXELS: "PEXELS_API_KEY",
    SkillId.PIXABAY: "PIXABAY_API_KEY",
    SkillId.GIPHY: "GIPHY_API_KEY",
    SkillId.SERPER_GENERAL: "SERPER_API_KEY",
    SkillId.SERPER_KNOWN_PERSON: "SERPER_API_KEY",
}

# Licensing hierarchy for scoring (higher = better)
LICENSING_SCORES: dict[str, float] = {
    "creative_commons": 1.0,
    "editorial": 0.8,
    "unsplash_license": 0.7,
    "pexels_license": 0.7,
    "pixabay_license": 0.7,
    "giphy_license": 0.5,
    "unknown": 0.0,
}

# Tier-to-skill mapping (stock / AI generation / internal)
TIER_SKILL_MAP: dict[str, list[str]] = {
    "tier_2_stock": [
        SkillId.UNSPLASH,
        SkillId.PEXELS,
        SkillId.PIXABAY,
        SkillId.GIPHY,
        SkillId.SERPER_GENERAL,
    ],
    "tier_3_ai_realistic": [SkillId.RUNNINGHUB_REALISTIC],
    "tier_3_ai_ghibli": [SkillId.RUNNINGHUB_GHIBLI],
    "tier_1_photo_deck": [SkillId.PHOTO_DECK],
    "tier_1_known_person": [SkillId.SERPER_KNOWN_PERSON],
}


class MultiAPISearchError(str, Enum):
    """Error types for FR-VIS-10 multi-API search."""
    MISSING_API_KEY = "MISSING_API_KEY"
    ALL_APIS_UNAVAILABLE = "ALL_APIS_UNAVAILABLE"
    API_TIMEOUT = "API_TIMEOUT"
    NO_RESULTS_FOUND = "NO_RESULTS_FOUND"
    RESOLUTION_FILTER_EXHAUSTED = "RESOLUTION_FILTER_EXHAUSTED"
    NORMALIZATION_ERROR = "NORMALIZATION_ERROR"
    INVALID_TIER = "INVALID_TIER"


class SearchOrientation(str, Enum):
    """Image orientation preference."""
    LANDSCAPE = "landscape"
    PORTRAIT = "portrait"
    SQUARISH = "squarish"


class SearchRequest(BaseModel):
    """Standardized search request submitted by Aurore (§4 Stage 1)."""
    search_id: str = Field(...)
    slide_index: int = Field(..., ge=0)
    search_terms: list[str] = Field(
        ...,
        min_length=1,
        description="Tribal-noun-derived visual descriptors.",
    )
    orientation: Optional[str] = Field(default=None)
    color_filter: Optional[str] = Field(
        default=None,
        description="Hex color filter, e.g. '#FF5733'.",
    )
    resolution_minimum_px: int = Field(default=MIN_SEARCH_RESOLUTION_PX, ge=1)
    licensing_filter: Optional[str] = Field(default=None)
    source_tier: str = Field(
        ...,
        description="Tier key from TIER_SKILL_MAP.",
    )
    coach_acronym: str = Field(
        ...,
        min_length=2,
        max_length=4,
        description="ADR-01 coach scope.",
    )
    # For AI generation (Tier 3)
    compiled_prompt: Optional[str] = Field(
        default=None,
        description="PSSL-compiled prompt for RunningHub skills.",
    )
    reference_image_base64: Optional[str] = Field(default=None)
    lora_model_path: Optional[str] = Field(default=None)
    # For Known Person (Tier 1)
    person_name: Optional[str] = Field(default=None)


class NormalizedSearchResult(BaseModel):
    """Common schema for all API responses after normalization (§4 Stage 3)."""
    result_id: str = Field(...)
    source_skill: str = Field(...)
    source_api: str = Field(...)
    image_url: str = Field(...)
    thumbnail_url: Optional[str] = Field(default=None)
    width_px: int = Field(..., ge=1)
    height_px: int = Field(..., ge=1)
    aspect_ratio: Optional[str] = Field(default=None)
    licensing_type: str = Field(default="unknown")
    licensing_restrictions: Optional[str] = Field(default=None)
    photographer: Optional[str] = Field(default=None)
    relevance_score: float = Field(default=0.0, ge=0.0, le=1.0)
    resolution_adequate: bool = Field(default=False)
    color_match_score: float = Field(default=0.0, ge=0.0, le=1.0)
    tribal_noun_alignment: float = Field(default=0.0, ge=0.0, le=1.0)
    combined_score: float = Field(default=0.0, ge=0.0, le=1.0)


class RankedResult(BaseModel):
    """A search result with its rank position (§5)."""
    rank: int = Field(..., ge=1)
    result_id: str = Field(...)
    source_skill: str = Field(...)
    source_api: str = Field(...)
    image_url: str = Field(...)
    combined_score: float = Field(default=0.0, ge=0.0, le=1.0)
    selected: bool = Field(default=False)


class RunningHubTaskStatus(BaseModel):
    """Status of a RunningHub generation task (§4 Stage 2, SKILL-IMG-007/008)."""
    task_id: str = Field(...)
    status: str = Field(
        ...,
        description="'pending' | 'processing' | 'completed' | 'failed'.",
    )
    status_url: Optional[str] = Field(default=None)
    output_url: Optional[str] = Field(default=None)
    poll_count: int = Field(default=0, ge=0)
    elapsed_seconds: float = Field(default=0.0, ge=0.0)
    error_detail: Optional[str] = Field(default=None)


class MultiAPISearchResponse(BaseModel):
    """Full response from multi_api_image_search.py (§5)."""
    search_id: str = Field(...)
    slide_index: int = Field(..., ge=0)
    search_terms: list[str] = Field(default_factory=list)
    orientation: Optional[str] = Field(default=None)
    color_filter: Optional[str] = Field(default=None)
    resolution_minimum_px: int = Field(default=MIN_SEARCH_RESOLUTION_PX)
    skills_dispatched: list[str] = Field(default_factory=list)
    skills_succeeded: list[str] = Field(default_factory=list)
    skills_failed: list[str] = Field(default_factory=list)
    skills_failed_reasons: dict[str, str] = Field(default_factory=dict)
    skills_skipped: list[str] = Field(default_factory=list)
    skills_skipped_reasons: dict[str, str] = Field(default_factory=dict)
    total_results_raw: int = Field(default=0, ge=0)
    total_results_after_filtering: int = Field(default=0, ge=0)
    ranked_results: list[RankedResult] = Field(default_factory=list)
    receipt_chain_block: Optional[str] = Field(default=None)
    timestamp_utc: Optional[str] = Field(default=None)
    error_type: Optional[str] = Field(default=None)
    error_detail: Optional[str] = Field(default=None)


# ---------------------------------------------------------------------------
# FR-VIS-11: In-App Image Search Panel
# ---------------------------------------------------------------------------

# Debounce interval for search bar (milliseconds)
SEARCH_DEBOUNCE_MS: int = 500


class SearchPanelTab(str, Enum):
    """Source tabs available in the Image Search Panel (§4 Stage 1)."""
    ALL = "all"
    STOCK_PHOTOS = "stock_photos"
    GIFS = "gifs"
    AI_GENERATE = "ai_generate"
    PHOTO_DECK = "photo_deck"


class SwapSourceType(str, Enum):
    """Source types for manually placed images (§4 Stage 3)."""
    MANUAL_OVERRIDE_STOCK = "manual_override_stock"
    MANUAL_OVERRIDE_AI = "manual_override_ai"
    MANUAL_OVERRIDE_PHOTO_DECK = "manual_override_photo_deck"
    MANUAL_UPLOAD = "manual_upload"


class ImageSearchPanelError(str, Enum):
    """Errors specific to the in-app search panel."""
    SEARCH_UNAVAILABLE = "SEARCH_UNAVAILABLE"
    PLACEMENT_FAILED = "PLACEMENT_FAILED"
    SLOT_NOT_SELECTED = "SLOT_NOT_SELECTED"
    HISTORY_WRITE_FAILED = "HISTORY_WRITE_FAILED"
    STYLE_FILTER_VIOLATION = "STYLE_FILTER_VIOLATION"
    UNAUTHORIZED_PHOTO_DECK = "UNAUTHORIZED_PHOTO_DECK"


class StyleDirectiveFilter(BaseModel):
    """Style directive filter applied to search results (§4 Stage 2)."""
    permitted_styles: list[str] = Field(default_factory=list)
    hidden_sources: list[str] = Field(default_factory=list)


class OriginalImageInfo(BaseModel):
    """Info about the image being replaced in a swap."""
    url: str = Field(...)
    source_type: str = Field(default="")
    source_api: Optional[str] = Field(default=None)


class ReplacementImageInfo(BaseModel):
    """Info about the replacement image in a swap."""
    url: str = Field(...)
    source_type: str = Field(...)
    source_api: Optional[str] = Field(default=None)


class AssetHistoryEntry(BaseModel):
    """A single manual swap record in the Asset History Table (§4 Stage 3)."""
    swap_id: str = Field(...)
    composition_id: str = Field(...)
    slide_index: int = Field(..., ge=0)
    original_image: OriginalImageInfo = Field(...)
    replacement_image: ReplacementImageInfo = Field(...)
    operator_id: str = Field(...)
    swap_reason: Optional[str] = Field(
        default=None,
        description="Optional text explaining why the operator overrode.",
    )
    swap_timestamp_utc: str = Field(...)
    receipt_chain_block: Optional[str] = Field(default=None)


class ImageSlotPlacement(BaseModel):
    """Result of placing an image into a canvas slot (§4 Stage 2)."""
    placement_id: str = Field(...)
    slide_index: int = Field(..., ge=0)
    image_url: str = Field(...)
    source_type: str = Field(...)
    r2_storage_url: Optional[str] = Field(
        default=None,
        description="Cloudflare R2 URL after download.",
    )
    resolution_warning: bool = Field(
        default=False,
        description="True if resolution < 1080px shortest edge.",
    )
    warning_message: Optional[str] = Field(default=None)
    success: bool = Field(default=True)
    error_type: Optional[str] = Field(default=None)


class SearchPanelState(BaseModel):
    """Full state of the Image Search Panel (§5)."""
    panel_session_id: str = Field(...)
    composition_id: str = Field(...)
    coach_acronym: str = Field(
        ...,
        min_length=2,
        max_length=4,
        description="ADR-01 coach scope.",
    )
    current_search_query: Optional[str] = Field(default=None)
    active_tab: str = Field(default=SearchPanelTab.ALL)
    style_directive_filter: Optional[StyleDirectiveFilter] = Field(default=None)
    results_displayed: int = Field(default=0, ge=0)
    results_filtered_out: int = Field(default=0, ge=0)
    total_swaps_this_session: int = Field(default=0, ge=0)
    resolution_warnings_shown: int = Field(default=0, ge=0)
    error_type: Optional[str] = Field(default=None)
    error_detail: Optional[str] = Field(default=None)


# ════════════════════════════════════════════════════════════════════════
# FR-VIS-01 — Visual Composition Brief Generation
# ════════════════════════════════════════════════════════════════════════

# ---- Constants ----

MAX_INTERNAL_REVISIONS: int = 3
"""Gate C-09 allows at most 3 internal revision cycles before escalation."""

MIN_TIAR_NOUNS_PER_TEXT_SLIDE: int = 3
"""Each text slide must contain ≥ 3 concrete TIAR nouns (C09-R03)."""

SEMIOTIC_INJECTION_EARLIEST_RATIO: float = 0.6
"""Semiotic injection must be placed in the latter third (≥ 60 %) of 4+ slide sequences."""

SEMIOTIC_INJECTION_MIN_SLIDES: int = 4
"""Semiotic injection rule only applies to sequences with 4+ slides."""

# Mood → CEGF Color Architecture saturation anchors (low, peak, release)
MOOD_SATURATION_ANCHORS: dict[str, tuple[int, int, int]] = {
    "Processing":  (35, 50, 35),
    "Escape":      (70, 85, 50),
    "Discovery":   (55, 65, 45),
    "Status":      (60, 75, 50),
}

# Mood → color-temperature range (Kelvin low, Kelvin high)
MOOD_COLOR_TEMPERATURE: dict[str, tuple[int, int]] = {
    "Processing":  (4500, 5000),
    "Escape":      (3200, 3800),
    "Discovery":   (5000, 5500),
    "Status":      (6000, 6500),
}

# CBCS thresholds for gaze-zone routing
GAZE_CBCS_COLD_THRESHOLD: int = 3
"""CBCS < 3 → gaze toward Hook Zone."""
GAZE_CBCS_WARM_THRESHOLD: int = 7
"""CBCS ≥ 7 → gaze toward Action Zone."""

# Gaze zone horizontal pupil ranges (% of frame width)
GAZE_ZONE_RANGES: dict[str, tuple[float, float]] = {
    "Identity":  (10.0, 30.0),
    "Hook":      (35.0, 45.0),
    "Action":    (70.0, 85.0),
}

# Completion imagery descriptors for accumulation prohibition audit
COMPLETION_IMAGERY_KEYWORDS: frozenset[str] = frozenset({
    "checkmark", "check mark", "finish line", "trophy",
    "celebration", "medal", "award", "completion",
    "finished", "winner", "victory", "confetti",
})


# ---- Enums ----

class SomaticArcType(str, Enum):
    """Somatic arc types from Carousel Physiological State Architecture."""
    TENSION_RELEASE = "tension_release"
    DISCOVERY_REVELATION = "discovery_revelation"
    CONTRAST_RESOLUTION = "contrast_resolution"
    ACCUMULATION_CLIFF = "accumulation_cliff"


class MoodState(str, Enum):
    """CEGF Color Architecture Matrix mood states."""
    PROCESSING = "Processing"
    ESCAPE = "Escape"
    DISCOVERY = "Discovery"
    STATUS = "Status"


class GazeTargetZone(str, Enum):
    """Gaze Cueing Framework architectural zones."""
    IDENTITY = "Identity"
    HOOK = "Hook"
    ACTION = "Action"


class SemanticConflictType(str, Enum):
    """Tags for text-visual semantic conflicts."""
    INTENTIONAL_TENSION = "intentional_tension"
    INTENTIONAL_CONTRAST = "intentional_contrast"
    CONFLICT_ERROR = "conflict_error"


class GateC09Rule(str, Enum):
    """The 7 Gate C-09 validation rules."""
    C09_R01_LIGHTING_TEMPORAL = "C09-R01_lighting_temporal"
    C09_R02_SATURATION_NUMERIC = "C09-R02_saturation_numeric"
    C09_R03_TIAR_COVERAGE = "C09-R03_tiar_coverage"
    C09_R04_GAZE_GEOMETRY = "C09-R04_gaze_geometry"
    C09_R05_PAD_SCORES = "C09-R05_pad_scores"
    C09_R06_INCOMPLETE_ARTIFACT = "C09-R06_incomplete_artifact"
    C09_R07_SEMIOTIC_POSITION = "C09-R07_semiotic_position"


class GateC09Verdict(str, Enum):
    """Possible outcomes from Gate C-09."""
    PASS = "PASS"
    FAIL = "FAIL"
    ESCALATED = "ESCALATED"


class VCBError(str, Enum):
    """Error codes for VCB generation failures."""
    RECIPE_NOT_FOUND = "RECIPE_NOT_FOUND"
    PSSL_RESOLUTION_FAILURE = "PSSL_RESOLUTION_FAILURE"
    TIAR_COVERAGE_INSUFFICIENT = "TIAR_COVERAGE_INSUFFICIENT"
    GATE_C09_EXCEEDED_REVISIONS = "GATE_C09_EXCEEDED_REVISIONS"
    LEGACY_ROUTING_DEFAULT = "LEGACY_ROUTING_DEFAULT"
    FORMAT_ENVELOPE_MISSING = "FORMAT_ENVELOPE_MISSING"
    STYLE_DIRECTIVE_MISSING = "STYLE_DIRECTIVE_MISSING"
    INVALID_COACH_ACRONYM = "INVALID_COACH_ACRONYM"


class AccumulationAuditStatus(str, Enum):
    """Result of the accumulation prohibition audit."""
    CLEAN = "CLEAN"
    VIOLATION_DETECTED = "VIOLATION_DETECTED"
    AUTO_CORRECTED = "AUTO_CORRECTED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


# ---- Models ----

class PADVector(BaseModel):
    """Pleasure-Arousal-Dominance environmental grammar (§4 Stage 2)."""
    P: float = Field(..., ge=-1.0, le=1.0, description="Pleasure score.")
    A: float = Field(..., ge=-1.0, le=1.0, description="Arousal score.")
    D: float = Field(..., ge=-1.0, le=1.0, description="Dominance score.")


class PSSLBlock(BaseModel):
    """Per-slide Physiological State Specification Language parameters (§4 Stage 2)."""
    lighting_grammar: str = Field(
        ...,
        description="Lighting grammar with temporal_signal and shadow spec.",
    )
    saturation_pct: int = Field(..., ge=0, le=100)
    head_rotation_degrees: float = Field(..., ge=-90.0, le=90.0)
    pupil_position_ratio_pct: float = Field(..., ge=0.0, le=100.0)
    pad_environmental_grammar: PADVector = Field(...)
    chromatic_bloom_sequence: list[str] = Field(
        ...,
        min_length=1,
        description="Color transitions, e.g. '#2D1B69→#FF6B35 ease 2s'.",
    )
    incomplete_tribal_artifact: Optional[str] = Field(
        default=None,
        description="Required non-null for tension/accumulation slides.",
    )


class TribalNounAssignment(BaseModel):
    """A single TIAR noun placement on a slide (§4 Stage 3)."""
    noun: str = Field(..., min_length=1)
    position: str = Field(
        ...,
        description="Text region: hook_text, overlay_text, body_text, subtext.",
    )
    congruent_visual_element: str = Field(
        ...,
        description="Visual element description ensuring noun-visual congruence.",
    )


class HandleBarConfig(BaseModel):
    """Coach handle bar visibility and position (§4 Stage 4, Step 5)."""
    visible: bool = Field(...)
    position: Optional[str] = Field(
        default=None,
        description="Always 'top_locked' when visible, null otherwise.",
    )


class SemanticConflict(BaseModel):
    """A tagged text-visual semantic conflict (§4 Stage 4, Step 6)."""
    conflict_type: str = Field(...)
    element_a: str = Field(...)
    element_b: str = Field(...)
    purpose: str = Field(
        ...,
        description="Why this conflict exists (e.g. reinforce stagnation).",
    )


class AccumulationAudit(BaseModel):
    """Result of the accumulation prohibition audit (§4 Stage 4, Step 7)."""
    arc_type: str = Field(...)
    accumulation_slides: list[int] = Field(default_factory=list)
    completion_imagery_detected: bool = Field(default=False)
    violating_slides: list[int] = Field(
        default_factory=list,
        description="Slide indices that contain prohibited completion imagery.",
    )
    audit_status: str = Field(default=AccumulationAuditStatus.NOT_APPLICABLE)


class SemioticInjection(BaseModel):
    """Semiotic injection positioning (§4 Stage 4, Step 8)."""
    injection_slide_index: int = Field(..., ge=0)
    total_slides: int = Field(..., ge=1)
    position_valid: bool = Field(...)
    injection_element: Optional[str] = Field(
        default=None,
        description="Description of the symbolic crystallization moment.",
    )


class PerSlideAssignment(BaseModel):
    """Complete specification for one slide in the VCB (§5)."""
    slide_index: int = Field(..., ge=0)
    slide_type: str = Field(...)
    image_type: str = Field(...)
    pssl: PSSLBlock = Field(...)
    tribal_noun_assignments: list[TribalNounAssignment] = Field(default_factory=list)
    handle_bar: HandleBarConfig = Field(...)
    semantic_conflicts: list[SemanticConflict] = Field(default_factory=list)
    named_person_reference: Optional[str] = Field(default=None)


class GateC09CheckResult(BaseModel):
    """Result for a single Gate C-09 rule check."""
    rule: str = Field(...)
    passed: bool = Field(...)
    detail: Optional[str] = Field(default=None)


class GateC09Result(BaseModel):
    """Aggregate Gate C-09 validation result (§4 Stage 5)."""
    verdict: str = Field(default=GateC09Verdict.PASS)
    checks: list[GateC09CheckResult] = Field(default_factory=list)
    revision_count: int = Field(default=0, ge=0, le=MAX_INTERNAL_REVISIONS)
    escalated: bool = Field(default=False)
    violations: list[str] = Field(
        default_factory=list,
        description="Rule IDs that failed.",
    )


class VCBGenerationInput(BaseModel):
    """Input envelope for the VCB generator (§4 Stage 1)."""
    content_output_id: str = Field(...)
    coach_acronym: str = Field(
        ...,
        min_length=2,
        max_length=4,
        description="ADR-01 coach scope.",
    )
    content_format: str = Field(
        ...,
        description="Locked format from FR-VIS-07 FormatConstraintEnvelope.",
    )
    format_envelope_id: str = Field(...)
    style_directive_id: str = Field(...)
    visual_style: str = Field(...)
    mood_state: str = Field(default=MoodState.PROCESSING)
    cbcs_score: int = Field(default=4, ge=1, le=10)
    somatic_arc_type: str = Field(default=SomaticArcType.TENSION_RELEASE)
    slide_count: int = Field(..., ge=1, le=20)
    recipe_id: Optional[str] = Field(default=None)
    active_nouns: list[str] = Field(default_factory=list)
    blocked_nouns: list[str] = Field(default_factory=list)
    voice_dna_id: Optional[str] = Field(default=None)
    has_psychological_routing_brief: bool = Field(default=True)


class VisualCompositionBrief(BaseModel):
    """The complete Visual Composition Brief output (DEP-VIS-005, §5)."""
    vcb_id: str = Field(...)
    content_output_id: str = Field(...)
    coach_acronym: str = Field(
        ...,
        min_length=2,
        max_length=4,
        description="ADR-01 coach scope.",
    )
    content_format: str = Field(...)
    selected_recipe_id: str = Field(...)
    somatic_arc_type: str = Field(...)
    slide_count: int = Field(..., ge=1, le=20)
    format_envelope_id: str = Field(...)
    style_directive_id: str = Field(...)
    visual_style: str = Field(...)
    mood_state: str = Field(...)
    cbcs_score: int = Field(..., ge=1, le=10)
    per_slide_assignments: list[PerSlideAssignment] = Field(...)
    accumulation_audit: AccumulationAudit = Field(...)
    semiotic_injection: Optional[SemioticInjection] = Field(default=None)
    gate_c09_result: GateC09Result = Field(...)
    tiar_validation_timestamp: Optional[str] = Field(default=None)
    receipt_chain_block: Optional[str] = Field(default=None)
    timestamp_utc: str = Field(...)
    warnings: list[str] = Field(
        default_factory=list,
        description="Non-fatal warnings (e.g. LEGACY_ROUTING_DEFAULT).",
    )


# ════════════════════════════════════════════════════════════════════════
# FR-VIS-03 — PSSL Prompt Compilation (Paradoxe)
# ════════════════════════════════════════════════════════════════════════

# ---- Constants ----

REFERENCE_IMAGE_STRENGTH_DEFAULT: float = 0.85
"""Identity-preserving reference image strength (0–1)."""

REFERENCE_IMAGE_STRENGTH_HIGH: float = 0.95
"""Used on character-drift retry for tighter identity lock."""

RUNNINGHUB_INITIAL_BACKOFF_S: int = 5
"""First polling interval after RunningHub task creation."""

RUNNINGHUB_MAX_BACKOFF_S: int = 60
"""Cap on exponential backoff interval."""

RUNNINGHUB_TIMEOUT_TOTAL_S: int = 600
"""10-minute absolute timeout for a single generation task."""

# Saturation descriptor ranges
SATURATION_RANGES: list[tuple[int, int, str]] = [
    (0, 20, "deeply desaturated, almost monochrome"),
    (21, 40, "muted, restrained color palette"),
    (41, 60, "moderate, naturalistic saturation"),
    (61, 80, "vivid, rich color depth"),
    (81, 100, "hyper-saturated, intense chromatic presence"),
]

# Default anti-generic constraints (universal)
UNIVERSAL_ANTI_GENERIC: str = (
    "Avoid: generic stock photography, perfectly symmetrical compositions, "
    "sterile lighting, posed expressions, corporate aesthetics, "
    "pure white backgrounds, clip art style elements, text that looks pasted on."
)

# Enemy typology → visual anti-patterns
ENEMY_ANTI_PATTERNS: dict[str, str] = {
    "hustle culture": (
        "Avoid: glorified overwork imagery, '24/7 grind' aesthetics, "
        "red-eye coffee shots, aggressive motivational poster compositions, "
        "neon-on-black typography."
    ),
    "toxic positivity": (
        "Avoid: forced smiles, aggressive motivational slogans, "
        "neon color palettes, 'just be happy' aesthetics, "
        "perfectly manicured environments."
    ),
    "corporate blandness": (
        "Avoid: sterile office lighting, posed corporate headshots, "
        "generic handshake imagery, white-backdrop stock photography, "
        "symmetrical boardroom compositions."
    ),
    "scarcity marketing": (
        "Avoid: countdown timer imagery, aggressive urgency cues, "
        "flashing red elements, manufactured panic aesthetics, "
        "manipulative scarcity visuals."
    ),
}

# Default imperfection specification
DEFAULT_IMPERFECTION_SPEC: str = (
    "Apply subtle intentional imperfections: micro-asymmetry in facial features "
    "(0.5-1.5% deviation), natural skin texture variations (pores, slight unevenness), "
    "minor environmental imperfections (slightly crooked object, dust motes in light beams, "
    "one wilting leaf). These prevent the 'too perfect' uncanny effect."
)


# ---- Enums ----

class PSSLCompilationError(str, Enum):
    """Error codes for the Paradoxe PSSL compiler."""
    PSSL_TRANSLATION_MISSING = "PSSL_TRANSLATION_MISSING"
    GENERATION_FAILED = "GENERATION_FAILED"
    REFERENCE_IMAGE_INVALID = "REFERENCE_IMAGE_INVALID"
    PENDING_HUMAN_REVIEW = "PENDING_HUMAN_REVIEW"
    LEGACY_PSSL_PARTIAL = "LEGACY_PSSL_PARTIAL"
    POLLING_TIMEOUT = "POLLING_TIMEOUT"
    PAYLOAD_ASSEMBLY_FAILED = "PAYLOAD_ASSEMBLY_FAILED"
    INVALID_COACH_ACRONYM = "INVALID_COACH_ACRONYM"


class PollingStatus(str, Enum):
    """RunningHub task polling states."""
    POLLING = "POLLING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    TIMEOUT = "TIMEOUT"
    PENDING_HUMAN_REVIEW = "PENDING_HUMAN_REVIEW"


class GrammarSystem(str, Enum):
    """Style grammar systems from FR-VIS-08."""
    CINEMATIC = "cinematic"
    ILLUSTRATED = "illustrated"
    DOCUMENTARY = "documentary"


# ---- Models ----

class SaturationTranslation(BaseModel):
    """Result of numeric saturation → descriptive mapping."""
    saturation_pct: int = Field(..., ge=0, le=100)
    descriptor: str = Field(...)
    full_text: str = Field(
        ...,
        description="Complete prompt fragment for this saturation level.",
    )


class GazeCompilation(BaseModel):
    """Compiled gaze geometry directives (§4 Stage 1)."""
    head_rotation_degrees: float = Field(...)
    head_direction_text: str = Field(
        ...,
        description="'left' or 'right' of center.",
    )
    pupil_position_ratio_pct: float = Field(...)
    pupil_direction_text: str = Field(...)
    compiled_text: str = Field(...)


class AntiGenericConstraints(BaseModel):
    """Assembled negative-prompt constraints (§4 Stage 2)."""
    enemy_typology: Optional[str] = Field(default=None)
    enemy_anti_pattern: Optional[str] = Field(default=None)
    universal_constraints: str = Field(default=UNIVERSAL_ANTI_GENERIC)
    compiled_text: str = Field(...)


class ReferenceImageConfig(BaseModel):
    """Reference image configuration for RunningHub payload (§4 Stage 3)."""
    has_reference: bool = Field(default=False)
    reference_source: Optional[str] = Field(default=None)
    character_id: Optional[str] = Field(default=None)
    strength: float = Field(default=REFERENCE_IMAGE_STRENGTH_DEFAULT)
    lora_model_path: Optional[str] = Field(default=None)
    is_ghibli: bool = Field(default=False)


class RunningHubPayload(BaseModel):
    """Assembled RunningHub task payload (§4 Stage 4)."""
    workflow_id: str = Field(...)
    prompt_text: str = Field(...)
    anti_generic_text: str = Field(...)
    imperfection_text: str = Field(default=DEFAULT_IMPERFECTION_SPEC)
    reference_image_config: ReferenceImageConfig = Field(
        default_factory=ReferenceImageConfig,
    )
    submitted: bool = Field(default=False)
    task_id: Optional[str] = Field(default=None)
    polling_status: str = Field(default=PollingStatus.POLLING)
    current_backoff_seconds: int = Field(default=RUNNINGHUB_INITIAL_BACKOFF_S)


class CompiledPromptPayload(BaseModel):
    """Complete output of Paradoxe's compilation for one slide (§5)."""
    compilation_id: str = Field(...)
    vcb_id: str = Field(...)
    slide_index: int = Field(..., ge=0)
    coach_acronym: str = Field(
        ...,
        min_length=2,
        max_length=4,
        description="ADR-01 coach scope.",
    )
    grammar_system: str = Field(default=GrammarSystem.CINEMATIC)
    compiled_prompt_text: str = Field(...)
    anti_generic_constraints: AntiGenericConstraints = Field(...)
    imperfection_spec: str = Field(default=DEFAULT_IMPERFECTION_SPEC)
    reference_image: ReferenceImageConfig = Field(
        default_factory=ReferenceImageConfig,
    )
    runninghub_payload: RunningHubPayload = Field(...)
    receipt_chain_block: Optional[str] = Field(default=None)
    timestamp_utc: str = Field(...)
    warnings: list[str] = Field(default_factory=list)


# ════════════════════════════════════════════════════════════════════════
# FR-VIS-05 — Canvas Composition & Delivery
# ════════════════════════════════════════════════════════════════════════

# ---- Constants ----

EDGE_BLEED_PX: int = 40
"""Overlap pixels on each side of a carousel stitch boundary."""

CIEDE2000_MAX_DISTANCE: float = 15.0
"""Maximum CIEDE2000 color distance between adjacent edge bleed zones."""

HANDLE_BAR_POSITION: str = "top_locked"
"""Fixed position of the Coach Handle Bar component."""

# ---- Enums ----


class CompositionStatus(str, Enum):
    """Lifecycle states of a Canva composition."""
    ASSEMBLING = "ASSEMBLING"
    READY_FOR_REVIEW = "READY_FOR_REVIEW"
    APPROVED = "APPROVED"
    MANUALLY_EDITED_APPROVED = "MANUALLY_EDITED_APPROVED"
    REGENERATION_REQUESTED = "REGENERATION_REQUESTED"
    CANVA_APP_UNAVAILABLE = "CANVA_APP_UNAVAILABLE"


class ApprovalAction(str, Enum):
    """Operator approval actions (Customization G)."""
    APPROVE_AND_PUBLISH = "APPROVE_AND_PUBLISH"
    REQUEST_REGENERATION = "REQUEST_REGENERATION"
    EDIT_AND_APPROVE = "EDIT_AND_APPROVE"


class CanvasCompositionError(str, Enum):
    """Error codes for the Canvas Composition service."""
    TEMPLATE_NOT_FOUND = "TEMPLATE_NOT_FOUND"
    WEBHOOK_TASK_MISMATCH = "WEBHOOK_TASK_MISMATCH"
    EDGE_BLEED_VIOLATION = "EDGE_BLEED_VIOLATION"
    EXPORT_DIMENSION_MISMATCH = "EXPORT_DIMENSION_MISMATCH"
    CANVA_APP_UNAVAILABLE = "CANVA_APP_UNAVAILABLE"
    INVALID_COACH_ACRONYM = "INVALID_COACH_ACRONYM"
    NOTION_SYNC_FAILED = "NOTION_SYNC_FAILED"
    XSS_CONTENT_DETECTED = "XSS_CONTENT_DETECTED"


# ---- Models ----


class CompositionDimensions(BaseModel):
    """Pixel dimensions and aspect ratio for a composition."""
    width_px: int = Field(..., gt=0)
    height_px: int = Field(..., gt=0)
    aspect_ratio: str = Field(...)


class CompositionHandleBar(BaseModel):
    """Coach Handle Bar component specification (Customization D)."""
    visible: bool = Field(default=True)
    position: str = Field(default=HANDLE_BAR_POSITION)
    coach_name: str = Field(...)
    coach_handle: str = Field(...)
    profile_picture_url: Optional[str] = Field(default=None)
    logo_url: Optional[str] = Field(default=None)


class CompositionSlot(BaseModel):
    """A single slide slot within a composition."""
    slide_index: int = Field(..., ge=0)
    text_populated: bool = Field(default=False)
    image_populated: bool = Field(default=False)
    image_source: Optional[str] = Field(default=None)
    image_r2_url: Optional[str] = Field(default=None)
    validation_verdict: Optional[str] = Field(default=None)


class EdgeBleedResult(BaseModel):
    """Result of edge bleed color validation between adjacent slides."""
    left_slide_index: int = Field(..., ge=0)
    right_slide_index: int = Field(..., ge=0)
    ciede2000_distance: float = Field(..., ge=0.0)
    threshold: float = Field(default=CIEDE2000_MAX_DISTANCE)
    result: str = Field(...)


class ExportAssets(BaseModel):
    """Export bundle for a completed composition."""
    individual_slides: list[str] = Field(default_factory=list)
    horizontal_stitch: Optional[str] = Field(default=None)
    zip_archive: Optional[str] = Field(default=None)


class RegenerationRequest(BaseModel):
    """Request to regenerate a specific slide via Paradoxe."""
    slide_index: int = Field(..., ge=0)
    revision_note: str = Field(...)
    vcb_id: str = Field(...)


class CanvasComposition(BaseModel):
    """Complete Canva composition object (§5)."""
    composition_id: str = Field(...)
    vcb_id: str = Field(...)
    content_output_id: Optional[str] = Field(default=None)
    template_id: str = Field(...)
    coach_acronym: str = Field(
        ...,
        min_length=2,
        max_length=4,
        description="ADR-01 coach scope.",
    )
    status: str = Field(...)
    dimensions: CompositionDimensions = Field(...)
    slide_count: int = Field(..., ge=1)
    handle_bar: CompositionHandleBar = Field(...)
    slots: list[CompositionSlot] = Field(default_factory=list)
    export_assets: ExportAssets = Field(default_factory=ExportAssets)
    approval_action: Optional[str] = Field(default=None)
    receipt_chain_block: Optional[str] = Field(default=None)
    timestamp_utc: str = Field(...)
    warnings: list[str] = Field(default_factory=list)

# ════════════════════════════════════════════════════════════════════════
# FR-VIS-04 — Visual Validation
# ════════════════════════════════════════════════════════════════════════

# ---- Constants ----

AGSS_THRESHOLD: float = 6.5
"""Minimum AGSS composite score for a PASS verdict."""

CHARACTER_DRIFT_THRESHOLD: float = 0.30
"""Maximum drift_score (0–1) before character drift failure."""

MAX_VALIDATION_RETRIES: int = 1
"""Each check type gets exactly one automated remediation attempt."""

# AGSS component weights (must sum to 1.0)
AGSS_WEIGHT_LIGHTING: float = 0.25
AGSS_WEIGHT_TEXTURE: float = 0.25
AGSS_WEIGHT_COMPOSITION: float = 0.25
AGSS_WEIGHT_EMOTION: float = 0.25


# ---- Enums ----

class ValidationVerdict(str, Enum):
    """Overall outcome of visual validation."""
    VALIDATED = "VALIDATED"
    REMEDIATION_IN_PROGRESS = "REMEDIATION_IN_PROGRESS"
    PENDING_HUMAN_REVIEW = "PENDING_HUMAN_REVIEW"
    VALIDATION_SERVICE_UNAVAILABLE = "VALIDATION_SERVICE_UNAVAILABLE"


class AuthenticityCheck(str, Enum):
    """The three mandatory authenticity binary checks."""
    EXPRESSION_NATURALNESS = "expression_naturalness"
    FACIAL_PROPORTION = "facial_proportion"
    SKIN_TEXTURE = "skin_texture"


class ValidationFailureType(str, Enum):
    """Categories of validation failure for remediation routing."""
    AGSS_BELOW_THRESHOLD = "AGSS_BELOW_THRESHOLD"
    AUTHENTICITY_EXPRESSION = "AUTHENTICITY_EXPRESSION"
    AUTHENTICITY_PROPORTION = "AUTHENTICITY_PROPORTION"
    AUTHENTICITY_TEXTURE = "AUTHENTICITY_TEXTURE"
    CHARACTER_DRIFT = "CHARACTER_DRIFT"


class RemediationAction(str, Enum):
    """Actions taken during remediation."""
    ENHANCED_IMPERFECTION = "ENHANCED_IMPERFECTION"
    INCREASED_REF_STRENGTH = "INCREASED_REF_STRENGTH"
    PENDING_HUMAN_REVIEW = "PENDING_HUMAN_REVIEW"
    NONE = "NONE"


class VisualValidationError(str, Enum):
    """Error codes for the Visual Validation Agent."""
    INVALID_IMAGE_FORMAT = "INVALID_IMAGE_FORMAT"
    VISION_API_ERROR = "VISION_API_ERROR"
    VALIDATION_SERVICE_UNAVAILABLE = "VALIDATION_SERVICE_UNAVAILABLE"
    REMEDIATION_EXHAUSTED = "REMEDIATION_EXHAUSTED"
    INVALID_COACH_ACRONYM = "INVALID_COACH_ACRONYM"


# ---- Models ----

class AGSSComponentScores(BaseModel):
    """Individual AGSS component scores (§4 Stage 1)."""
    lighting_naturalism: float = Field(..., ge=0.0, le=10.0)
    texture_authenticity: float = Field(..., ge=0.0, le=10.0)
    compositional_coherence: float = Field(..., ge=0.0, le=10.0)
    emotional_believability: float = Field(..., ge=0.0, le=10.0)


class AGSSResult(BaseModel):
    """Aggregate AGSS scoring result (§4 Stage 1)."""
    composite_score: float = Field(..., ge=0.0, le=10.0)
    components: AGSSComponentScores = Field(...)
    threshold: float = Field(default=AGSS_THRESHOLD)
    result: str = Field(...)


class AuthenticityResult(BaseModel):
    """Result of the 3 binary authenticity checks (§4 Stage 2)."""
    expression_naturalness: str = Field(...)
    facial_proportion: str = Field(...)
    skin_texture: str = Field(...)
    overall_result: str = Field(...)


class CharacterDriftResult(BaseModel):
    """Result of character drift detection (§4 Stage 3)."""
    reference_image_used: bool = Field(default=False)
    reference_character_id: Optional[str] = Field(default=None)
    drift_score: float = Field(default=0.0, ge=0.0, le=1.0)
    threshold: float = Field(default=CHARACTER_DRIFT_THRESHOLD)
    result: str = Field(...)


class RemediationRecord(BaseModel):
    """Record of a remediation attempt (§4 Stage 4)."""
    failure_type: str = Field(...)
    action_taken: str = Field(...)
    retry_number: int = Field(..., ge=1)
    details: Optional[str] = Field(default=None)


class VisualValidationResult(BaseModel):
    """Complete validation output for one slide (§5)."""
    validation_id: str = Field(...)
    vcb_id: str = Field(...)
    slide_index: int = Field(..., ge=0)
    coach_acronym: str = Field(
        ...,
        min_length=2,
        max_length=4,
        description="ADR-01 coach scope.",
    )
    image_url: Optional[str] = Field(default=None)
    agss: AGSSResult = Field(...)
    authenticity: AuthenticityResult = Field(...)
    character_drift: CharacterDriftResult = Field(...)
    overall_verdict: str = Field(...)
    retry_count: int = Field(default=0, ge=0)
    remediations: list[RemediationRecord] = Field(default_factory=list)
    receipt_chain_block: Optional[str] = Field(default=None)
    timestamp_utc: str = Field(...)
    warnings: list[str] = Field(default_factory=list)


# ════════════════════════════════════════════════════════════════════════
# FR-VIS-06 — Notion Visual Content Card
# ════════════════════════════════════════════════════════════════════════

# ---- Enums ----


class VPOSyncStatus(str, Enum):
    """Delivery status of a Visual Production Output card."""
    SYNCED = "SYNCED"
    DELAYED_SYNC = "DELAYED_SYNC"
    SYNC_FAILED = "SYNC_FAILED"
    QUEUED = "QUEUED"
    R2_FALLBACK = "R2_FALLBACK"


class NotionCardError(str, Enum):
    """Error codes for the Notion Visual Content Card service."""
    MISSING_UPSTREAM_DATA = "MISSING_UPSTREAM_DATA"
    NOTION_API_FAILURE = "NOTION_API_FAILURE"
    R2_UPLOAD_FAILURE = "R2_UPLOAD_FAILURE"
    INVALID_COACH_ACRONYM = "INVALID_COACH_ACRONYM"
    FINGERPRINT_MISMATCH = "FINGERPRINT_MISMATCH"
    TEMPLATE_RATIONALE_MISSING = "TEMPLATE_RATIONALE_MISSING"


class LeadershipTrait(str, Enum):
    """Leadership traits exercised by visual content."""
    OBSERVER = "Observer"
    PROVOCATEUR = "Provocateur"
    SHEPHERD = "Shepherd"
    ARCHITECT = "Architect"
    MIRROR = "Mirror"


# ---- Models ----


class CardHeader(BaseModel):
    """Section 1 — Card Header."""
    universal_asset_id: str = Field(...)
    recipe_name: str = Field(...)
    production_status: str = Field(...)
    date: str = Field(...)
    visual_style: str = Field(...)


class SlidePreview(BaseModel):
    """Single slide preview entry."""
    slide_index: int = Field(..., ge=0)
    url: str = Field(...)


class PreviewAssets(BaseModel):
    """Section 2 — Preview."""
    content_type: str = Field(default="carousel")
    horizontal_stitch_url: Optional[str] = Field(default=None)
    slide_previews: list[SlidePreview] = Field(default_factory=list)
    zip_download_url: Optional[str] = Field(default=None)


class PostingRecommendation(BaseModel):
    """Posting day/time recommendation."""
    day: str = Field(...)
    time: str = Field(...)
    rationale: str = Field(...)


class ContentReadyToCopy(BaseModel):
    """Section 3 — Content Ready to Copy."""
    hook_text: str = Field(...)
    full_caption: str = Field(default="")
    hashtags: str = Field(default="")
    posting_recommendation: Optional[PostingRecommendation] = Field(default=None)


class WhyThisVisual(BaseModel):
    """Section 4 — Why This Visual Was Built This Way."""
    arc_type_explanation: str = Field(...)
    tiar_noun_rationale: str = Field(default="")
    style_rationale: str = Field(default="")
    tribal_function: str = Field(default="")


class LeadershipFarmingNote(BaseModel):
    """Section 5 — Leadership Farming Note."""
    trait: str = Field(...)
    development_context: str = Field(...)


class TIARDecayEntry(BaseModel):
    """TIAR noun decay row in Technical Audit."""
    noun: str = Field(...)
    tirs_score: float = Field(..., ge=0.0, le=10.0)
    decay_stage: str = Field(...)
    last_measured: str = Field(...)


class AGSSAuditEntry(BaseModel):
    """AGSS score row in Technical Audit."""
    slide_index: int = Field(..., ge=0)
    composite: float = Field(..., ge=0.0, le=10.0)
    lighting: float = Field(..., ge=0.0, le=10.0)
    texture: float = Field(..., ge=0.0, le=10.0)
    composition: float = Field(..., ge=0.0, le=10.0)
    emotion: float = Field(..., ge=0.0, le=10.0)


class AuthenticityAuditEntry(BaseModel):
    """Authenticity check row in Technical Audit."""
    slide_index: int = Field(..., ge=0)
    expression: str = Field(...)
    proportion: str = Field(...)
    skin_texture: str = Field(...)


class TechnicalAudit(BaseModel):
    """Section 6 — Technical Audit (collapsed)."""
    collapsed: bool = Field(default=True)
    tiar_decay_status: list[TIARDecayEntry] = Field(default_factory=list)
    agss_scores: list[AGSSAuditEntry] = Field(default_factory=list)
    authenticity_checks: list[AuthenticityAuditEntry] = Field(default_factory=list)
    receipt_chain_status: str = Field(default="VALID")
    receipt_chain_blocks: list[str] = Field(default_factory=list)
    fingerprint_id: Optional[str] = Field(default=None)
    asset_history: list[str] = Field(default_factory=list)


class VPONotionCard(BaseModel):
    """Complete Visual Production Output Notion Card (§5)."""
    vpo_id: str = Field(...)
    universal_asset_id: str = Field(...)
    notion_page_id: Optional[str] = Field(default=None)
    coach_id: str = Field(...)
    coach_acronym: str = Field(
        ...,
        min_length=2,
        max_length=4,
        description="ADR-01 coach scope.",
    )
    card_header: CardHeader = Field(...)
    preview_assets: PreviewAssets = Field(...)
    content_ready_to_copy: ContentReadyToCopy = Field(...)
    why_this_visual: WhyThisVisual = Field(...)
    leadership_farming_note: LeadershipFarmingNote = Field(...)
    technical_audit: TechnicalAudit = Field(...)
    sync_status: str = Field(default=VPOSyncStatus.QUEUED.value)
    r2_fallback_url: Optional[str] = Field(default=None)
    receipt_chain_block: Optional[str] = Field(default=None)
    timestamp_utc: str = Field(...)
    warnings: list[str] = Field(default_factory=list)