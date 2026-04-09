from __future__ import annotations

import uuid
from typing import Any, Dict, List, Literal, Optional, Tuple, Union
from pydantic import BaseModel, Field

# ── Enums and Types ───────────────────────────────────────────────────────────

SaliencyOverrideReason = Literal["AGSS_TRUST"]
VariantExhaustionStatus = Literal["PENDING_HUMAN_REVIEW", "REQUEUED", "RESOLVED_WITH_RESERVE"]

class CPHResolutionType(BaseModel):
    rule: str
    detail: str

# ── SAM 3 Saliency Analysis Output (DEP-VIS-016) ───────────────────────────────

class CoordinateBox(BaseModel):
    x: float
    y: float
    w: float
    h: float
    confidence: Optional[float] = None

class SaliencyAnalysisOutput(BaseModel):
    subject_mask: Optional[List[Tuple[float, float]]] = Field(
        None, description="Polygon mapping the subject, format: [[x1, y1], [x2, y2], ...]"
    )
    subject_bbox: Optional[CoordinateBox] = None
    text_safe_zones: List[CoordinateBox] = Field(default_factory=list)
    surface_quadrilateral: Optional[List[Tuple[float, float]]] = None
    gaze_direction: Optional[str] = None
    confidence: float
    cache_key: str
    foreground_mask: Optional[List[Tuple[float, float]]] = Field(
        None, description="Secondary mask used for depth occlusion (CPH-3)"
    )

# ── Pretext Typography Measurement Output (DEP-VIS-017) ─────────────────────────

class TextMeasurement(BaseModel):
    element_id: str
    optimal_font_size: float
    bounding_box: CoordinateBox
    line_count: int
    line_breaks: List[int]
    line_widths: List[float]
    shrink_wrap_width: float
    # Start and end coordinates for rough annotations mapped to substrings
    annotation_coordinates: Optional[Dict[str, List[Tuple[float, float]]]] = None

class TypographyMeasurementOutput(BaseModel):
    measurements: Dict[str, TextMeasurement]
    is_overset: bool = False

# ── Parametric Template Schema (DEP-VIS-015) ──────────────────────────────────

class TemplateZone(BaseModel):
    zone_type: Literal["subject", "text", "brand_bar", "full_canvas"]
    x_pct: float
    y_pct: float
    w_pct: float
    h_pct: float

class ParametricTemplate(BaseModel):
    template_id: str
    zones: Dict[str, TemplateZone]
    roughness_range: Tuple[float, float] = (1.5, 2.5)
    fallback_rules: List[str] = Field(default_factory=list)

# ── Resolved Layout Coordinate Map (DEP-VIS-018) ──────────────────────────────

class LayoutLayer(BaseModel):
    type: Literal["gradient_background", "image", "subject_shadow", "rough_rectangle", "rough_underline", "rough_highlight", "rough_circle", "text", "perspective_warp", "depth_occlusion", "brand_handle"]
    z: int
    bbox: Optional[List[float]] = None # [x, y, w, h]
    params: Optional[Dict[str, Any]] = None
    src: Optional[str] = None
    content: Optional[str] = None
    font: Optional[str] = None
    size: Optional[float] = None
    weight: Optional[int] = None
    color: Optional[str] = None
    roughness: Optional[float] = None
    start: Optional[Tuple[float, float]] = None
    end: Optional[Tuple[float, float]] = None

class ResolvedLayoutMap(BaseModel):
    variant_id: str
    canvas: Dict[str, int] # {"width": 1080, "height": 1350}
    layers: List[LayoutLayer]

# ── Full Primary Output Schema ────────────────────────────────────────────────

class VariantScoreInfo(BaseModel):
    variant_id: str
    score: float
    url: str

class SaliencyOverrideInfo(BaseModel):
    reason: SaliencyOverrideReason
    upstream_agss_score: float
    sam3_confidence: float

class EdgeBleedInfo(BaseModel):
    validated: bool
    ciede2000_max: float
    bridge_zone_applied: bool

class ExportInfo(BaseModel):
    individual_slides: List[str] = Field(default_factory=list)
    horizontal_stitch: Optional[str] = None
    zip_archive: Optional[str] = None

class SpatialCompositionOutput(BaseModel):
    composition_id: str
    vcb_id: str
    template_id: str
    pipeline_version: str = "geometrics_v1.0"
    canvas_dimensions: Dict[str, Union[int, str]]
    saliency_output: SaliencyAnalysisOutput
    typography_output: TypographyMeasurementOutput
    selected_variant: VariantScoreInfo
    all_variants: List[VariantScoreInfo]
    resolved_coordinate_map: ResolvedLayoutMap
    edge_bleed_validation: EdgeBleedInfo
    saliency_override: Optional[SaliencyOverrideInfo] = None
    cph_resolutions: List[CPHResolutionType] = Field(default_factory=list)
    variant_exhaustion_retry: bool = False
    export_assets: ExportInfo
    receipt_chain_block: Optional[Dict[str, Any]] = None
