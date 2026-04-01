"""
Visual Control Layer — Shared Models
FR-VIS-14 through FR-VIS-17

Shared Pydantic models, enums, constants, and error types for the
Visual Control Layer (Phase 6).
"""

from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field

from core.commercial_models import build_receipt, compute_receipt_hash


# =====================================================
#  Constants
# =====================================================

EXPRESSION_CHANNEL_COUNT = 28
ENROLLMENT_CODE_LENGTH = 8
LORA_WEIGHT_BUDGET_MAX = 1.50
IDENTITY_LORA_DEFAULT_WEIGHT = 0.65
CONSCIOUS_SMILE_DEFAULT_WEIGHT = 0.80
CONTROLNET_DEFAULT_STRENGTH = 0.85
IDENTITY_SCORE_THRESHOLD = 0.85
EXPRESSION_NEUTRALITY_THRESHOLD = 0.10
STYLE_FLEXIBILITY_MIN_PASS = 3
MAX_TRAINING_RETRIES = 3
CLIP_DEDUP_THRESHOLD = 0.92
ANTI_DRAFT_SATURATION_THRESHOLD = 40
ANTI_DRAFT_KELVIN_THRESHOLD = 5500

# Receipt Stage Names
RECEIPT_STAGE_EXPRESSION_PARSE = "EXPRESSION_PARSE"
RECEIPT_STAGE_PRESET_RESOLVE = "PRESET_RESOLVE"
RECEIPT_STAGE_POSE_RESOLVE = "POSE_RESOLVE"
RECEIPT_STAGE_COMPOSITION_RESOLVE = "COMPOSITION_RESOLVE"
RECEIPT_STAGE_LORA_TRAINING_START = "LORA_TRAINING_START"
RECEIPT_STAGE_LORA_TRAINING_COMPLETE = "LORA_TRAINING_COMPLETE"
RECEIPT_STAGE_LORA_DEPLOY = "LORA_DEPLOY"
RECEIPT_STAGE_PHOTO_CURATION = "PHOTO_CURATION"
RECEIPT_STAGE_FFC_COMPOSE = "FFC_COMPOSE"
RECEIPT_STAGE_ANTI_DRAFT_CHECK = "ANTI_DRAFT_CHECK"


# =====================================================
#  FR-VIS-14: ConsciousSmile Expression Channels
# =====================================================

class TrainingPhase(int, Enum):
    CORE = 1
    EXTENDED = 2
    REFINEMENT = 3


class ChannelStatus(str, Enum):
    PENDING = "pending"
    TRAINED = "trained"
    VALIDATED = "validated"
    PRODUCTION = "production"


class ExpressionChannel(BaseModel):
    """Single expression channel definition — maps to conscious_smile_channels table."""
    channel_id: str  # 'CH01'...'CH28'
    channel_name: str  # 'smile_duchenne'
    facs_action_units: str | None = None  # 'AU6 + AU12'
    arkit_blendshapes: list[str] = Field(default_factory=list)
    somatic_target: str = ""
    mood_state_affinity: dict[str, float] = Field(default_factory=dict)
    min_intensity: float = 0.0
    max_intensity: float = 1.0
    training_phase: int = 1
    confusion_pairs: list[str] = Field(default_factory=list)
    status: ChannelStatus = ChannelStatus.PENDING


class ExpressionPreset(BaseModel):
    """Named emotion preset — maps to expression_presets table."""
    preset_name: str  # 'warm_confidence'
    display_name: str  # 'Warm Confidence'
    channel_values: dict[str, float]  # {"smile": 0.6, "eye_squint": 0.4}
    mood_state_affinity: str | None = None
    prompt_string: str = ""  # 'expression: smile 0.6, eye_squint 0.4'


class ExpressionSpec(BaseModel):
    """Expression specification embedded in VCB (§5 Primary Output Schema)."""
    mode: str = "preset"  # 'preset' or 'manual'
    preset_name: str | None = None
    channel_overrides: dict[str, float] = Field(default_factory=dict)
    adapter_weight: float = CONSCIOUS_SMILE_DEFAULT_WEIGHT
    adapter_file: str = "/efs/ccp-models/adapters/conscious_smile_v1.safetensors"


class TrainingRunRow(BaseModel):
    """Expression training run — maps to expression_training_runs table."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    run_id: str = ""
    training_phase: int = 1
    channels_trained: list[str] = Field(default_factory=list)
    dataset_image_count: int = 0
    triplet_count: int | None = None
    base_model: str = "FLUX 2 Dev FP16"
    lora_rank: int = 64
    lora_alpha: int = 128
    learning_rate: float = 1e-4
    training_steps: int = 0
    gpu_type: str = "A100-80GB"
    training_hours: float | None = None
    output_file_path: str = ""
    output_file_size_mb: float | None = None
    eval_channel_accuracy: float | None = None
    eval_identity_preservation: float | None = None
    eval_confusion_separation: float | None = None
    status: str = "running"
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: datetime | None = None
    receipt_chain_block: str | None = None


class WeightBudgetResult(BaseModel):
    """Result of LoRA weight budget check."""
    total_weight: float
    identity_weight: float
    adapter_weight: float
    within_budget: bool
    warning: str | None = None


# =====================================================
#  FR-VIS-15: ConsciousPose Body Language Library
# =====================================================

class PoseLayer(str, Enum):
    BODY = "body"
    HANDS = "hands"
    GAZE = "gaze"
    SCENE = "scene"
    MOOD_VISUAL = "mood_visual"
    PROPS = "props"
    MULTI_CHARACTER = "multi_character"


class RenderStatus(str, Enum):
    PENDING = "pending"
    RENDERING = "rendering"
    RENDERED = "rendered"
    VALIDATED = "validated"
    PRODUCTION = "production"


class SourceLibrary(str, Enum):
    PRODUCTION = "production"
    EXPANSION = "expansion"


class CompositionType(str, Enum):
    ARCHETYPE_DEFAULT = "archetype_default"
    MEMETIC_RECIPE = "memetic_recipe"
    CUSTOM = "custom"
    CAMPAIGN = "campaign"


class PoseAtom(BaseModel):
    """Single pose atom — maps to conscious_pose_atoms table."""
    cp_id: str  # 'CP-B-001'
    layer: PoseLayer
    subcategory: str = ""
    position_name: str = ""
    display_name: str | None = None
    signal: str = ""
    mood_fit: list[str] = Field(default_factory=list)
    archetype_fit: list[str] = Field(default_factory=list)
    mirror_neuron_target: str | None = None
    bvt_function: str | None = None
    scene_constraint: str | None = None
    controlnet_depth_path: str | None = None
    controlnet_openpose_path: str | None = None
    controlnet_normal_path: str | None = None
    has_rendered_assets: bool = False
    render_status: RenderStatus = RenderStatus.PENDING
    source_library: SourceLibrary = SourceLibrary.PRODUCTION


class PoseComposition(BaseModel):
    """Multi-layer pose composition — maps to conscious_pose_compositions table."""
    composition_id: str  # 'COMP-EDUCATOR-DEFAULT-001'
    composition_name: str = ""
    composition_type: CompositionType = CompositionType.CUSTOM
    body_cp_id: str | None = None
    hands_cp_id: str | None = None
    gaze_cp_id: str | None = None
    scene_cp_id: str | None = None
    mood_visual_cp_id: str | None = None
    props_cp_id: str | None = None
    multi_char_cp_id: str | None = None
    archetype_family: str | None = None
    humor_architecture: str | None = None
    composed_asset_path: str | None = None
    is_pre_rendered: bool = False


class PoseSpec(BaseModel):
    """Pose specification embedded in VCB (§5 Primary Output Schema)."""
    body: str | None = None
    hands: str | None = None
    gaze: str | None = None
    scene: str | None = None
    mood_visual: str | None = None
    props: str | None = None
    multi_character: str | None = None
    composition_id: str | None = None
    controlnet_depth: str | None = None
    controlnet_openpose: str | None = None
    controlnet_strength: float = CONTROLNET_DEFAULT_STRENGTH


class ManifestEntry(BaseModel):
    """Single entry in the ControlNet manifest."""
    cp_id: str
    file_path: str
    file_type: str  # 'depth', 'openpose', 'normal', 'preview'
    checksum: str | None = None
    file_size_bytes: int | None = None


# =====================================================
#  FR-VIS-17: Identity LoRA Training Pipeline
# =====================================================

class LoRAStatus(str, Enum):
    TRAINING = "training"
    VALIDATING = "validating"
    ACTIVE = "active"
    RETIRED = "retired"
    FAILED = "failed"


class TrainingJobStatus(str, Enum):
    QUEUED = "queued"
    CURATING = "curating"
    TRAINING = "training"
    VALIDATING = "validating"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


class CurationResult(BaseModel):
    """Result of photo curation pipeline."""
    accepted_count: int = 0
    rejected_count: int = 0
    rejected_reasons: list[dict[str, str]] = Field(default_factory=list)
    curated_photos: list[dict[str, str]] = Field(default_factory=list)
    trigger_token: str = ""


class IdentityLoRAEntry(BaseModel):
    """Identity LoRA registry entry — maps to identity_lora_registry table."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    coach_id: str = ""
    lora_version: int = 1
    trigger_token: str = ""  # 'ccp_audrey'
    file_path: str = ""
    file_size_mb: float | None = None
    lora_rank: int = 24
    lora_alpha: int = 48
    training_steps: int = 0
    reference_photo_count: int = 0
    identity_score: float = 0.0
    style_flexibility_score: float | None = None
    expression_neutrality: float | None = None
    conscious_smile_compatible: bool = False
    inference_weight: float = IDENTITY_LORA_DEFAULT_WEIGHT
    status: LoRAStatus = LoRAStatus.TRAINING
    trained_at: datetime | None = None
    deployed_at: datetime | None = None
    retired_at: datetime | None = None
    receipt_chain_block: str | None = None


class TrainingJobRow(BaseModel):
    """Identity LoRA training job — maps to identity_lora_training_jobs table."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    job_id: str = ""
    coach_id: str = ""
    target_version: int = 1
    reference_photos: list[dict[str, str]] = Field(default_factory=list)
    training_config: dict[str, Any] = Field(default_factory=dict)
    gpu_type: str = "A100-80GB"
    training_duration_hours: float | None = None
    attempt_number: int = 1
    validation_report: dict[str, Any] | None = None
    status: TrainingJobStatus = TrainingJobStatus.QUEUED
    error_message: str | None = None


class ValidationReport(BaseModel):
    """5-metric validation report for Identity LoRA."""
    identity_score: float = 0.0
    style_flexibility_pass: int = 0  # out of 5
    expression_neutrality: float = 0.0
    background_independence: float = 0.0
    conscious_smile_compatible: bool = False
    passed: bool = False
    failure_reasons: list[str] = Field(default_factory=list)


# =====================================================
#  FR-VIS-16: First Frame Composer (Iris)
# =====================================================

class OutputFormat(str, Enum):
    SHORT_VIDEO = "short_video"
    CAROUSEL = "carousel"
    THUMBNAIL = "thumbnail"
    FLYER = "flyer"
    WEBINAR = "webinar"
    STORY = "story"
    POLL = "poll"
    EMAIL = "email"


class CBCSTier(str, Enum):
    COLD = "cold"        # 0-3
    WARM = "warm"        # 4-7
    HOT = "hot"          # 8-10


class AntiDraftLevel(str, Enum):
    LEVEL_1_STOCK = "level_1_stock_thumbnail"
    LEVEL_2_FORMAT = "level_2_format_specific"


class FormatConstraints(BaseModel):
    """Format-specific visual constraints."""
    dimensions: str  # '1080x1920'
    face_position_rule: str  # 'top_40_pct', 'centered', 'rule_of_thirds_left', etc.
    text_zone: str  # 'bottom_30_pct', 'opposite_third', etc.
    face_required: bool = True


class FirstFrameSpec(BaseModel):
    """Complete first frame specification (§5 `first_frame_spec.json`)."""
    spec_id: str = Field(default_factory=lambda: f"FFS-{str(uuid.uuid4())[:8].upper()}")
    coach_id: str = ""
    output_format: OutputFormat = OutputFormat.SHORT_VIDEO
    dimensions: str = "1080x1920"
    mood_state: str = ""
    cbcs_tier: CBCSTier = CBCSTier.COLD
    body_cp_id: str | None = None
    hands_cp_id: str | None = None
    gaze_cp_id: str | None = None
    scene_cp_id: str | None = None
    mood_visual_cp_id: str | None = None
    props_cp_id: str | None = None
    expression_spec: dict[str, Any] = Field(default_factory=dict)
    text_headline: str | None = None
    text_position: str | None = None
    text_font_treatment: str | None = None
    controlnet_depth_path: str | None = None
    controlnet_openpose_path: str | None = None
    identity_lora_path: str = ""
    adapter_path: str = "/efs/ccp-models/adapters/conscious_smile_v1.safetensors"
    negative_prompt: str | None = None
    reasoning: dict[str, str] = Field(default_factory=dict)
    anti_draft_passed: bool = True
    routed_to: str | None = None
    receipt_chain_block: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AntiDraftResult(BaseModel):
    """Result of anti-draft constraint check."""
    passed: bool = True
    level: AntiDraftLevel | None = None
    violation_reason: str | None = None
    suggestion: str | None = None


# =====================================================
#  Shared Errors
# =====================================================

class VisualPipelineError(Exception):
    """Base error for Visual Control Layer."""
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")
