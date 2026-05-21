from __future__ import annotations

from datetime import datetime
from typing import Any
from enum import Enum

from pydantic import BaseModel, Field


class BeatClusterType(str, Enum):
    rally = "rally"
    witness = "witness"
    reflection = "reflection"
    confrontation = "confrontation"


class ShotGrammarProfile(str, Enum):
    kinetic_escalation = "kinetic_escalation"
    intimate_observation = "intimate_observation"
    contemplative_pause = "contemplative_pause"
    pressure_lock = "pressure_lock"


class FirstFrameVerdict(str, Enum):
    pass_ = "PASS"
    fail = "FAIL"
    escalate = "ESCALATE"


class EpicMeaningVerdict(str, Enum):
    pass_ = "PASS"
    fail_flat_lighting = "FAIL_FLAT_LIGHTING"
    fail_corporate_aesthetic = "FAIL_CORPORATE_AESTHETIC"
    fail_generic_sonic_bed = "FAIL_GENERIC_SONIC_BED"
    fail_first_frame_weak = "FAIL_FIRST_FRAME_WEAK"
    escalate = "ESCALATE"


class ArcRenderJobStatus(str, Enum):
    planned = "planned"
    first_frame_blocked = "first_frame_blocked"
    preview_rendering = "preview_rendering"
    preview_failed = "preview_failed"
    full_rendering = "full_rendering"
    ready_for_composition = "ready_for_composition"
    released = "released"
    failed = "failed"


class TempoEnvelope(BaseModel):
    bpm_start: int = Field(..., ge=40, le=220)
    bpm_peak: int = Field(..., ge=40, le=220)
    bpm_end: int = Field(..., ge=40, le=220)
    silence_windows_ms: list[int] = Field(default_factory=list)


class ClusterShotDirective(BaseModel):
    camera_distance: str = Field(..., min_length=1, max_length=80)
    lighting_profile: str = Field(..., min_length=1, max_length=120)
    movement_profile: str = Field(..., min_length=1, max_length=120)
    transition_profile: str = Field(..., min_length=1, max_length=120)
    symbolic_environment: str = Field(..., min_length=1, max_length=160)


class DeterministicControlSpec(BaseModel):
    first_frame_spec_id: str = Field(..., min_length=1)
    conscious_pose_id: str = Field(..., min_length=1)
    conscious_smile_preset: str = Field(..., min_length=1)
    identity_lora_path: str = Field(..., min_length=1)
    gaze_rule: str = Field(..., min_length=1, max_length=120)


class BeatClusterPlan(BaseModel):
    cluster_id: str = Field(..., min_length=1)
    cluster_type: BeatClusterType
    order_index: int = Field(..., ge=0)
    start_ms: int = Field(..., ge=0)
    end_ms: int = Field(..., ge=1)
    shot_grammar: ShotGrammarProfile
    shot_directive: ClusterShotDirective
    tempo_envelope: TempoEnvelope
    deterministic_controls: DeterministicControlSpec
    narrative_purpose: str = Field(..., min_length=8, max_length=280)


class FirstFrameAuthorityCheck(BaseModel):
    check_id: str = Field(..., min_length=1)
    cluster_id: str = Field(..., min_length=1)
    verdict: FirstFrameVerdict
    authority_score: float = Field(..., ge=0.0, le=1.0)
    contrast_score: float = Field(..., ge=0.0, le=1.0)
    recognizability_score: float = Field(..., ge=0.0, le=1.0)
    anti_generic_flags: list[str] = Field(default_factory=list)
    checked_at: datetime


class EpicMeaningGateResult(BaseModel):
    gate_id: str = Field(..., min_length=1)
    job_id: str = Field(..., min_length=1)
    verdict: EpicMeaningVerdict
    blandness_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    failed_rules: list[str] = Field(default_factory=list)
    rationale: str = Field(..., min_length=8, max_length=400)
    checked_at: datetime


class CoalitionSpineInput(BaseModel):
    content_output_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    coach_acronym: str = Field(..., min_length=2, max_length=4)
    selected_format: str = Field(..., min_length=1, max_length=80)
    spine_text: str = Field(..., min_length=20)
    somatic_arc_type: str = Field(..., min_length=1, max_length=80)
    voice_dna_id: str = Field(..., min_length=1)


class ArcRenderManifest(BaseModel):
    manifest_id: str = Field(..., min_length=1)
    job_id: str = Field(..., min_length=1)
    content_output_id: str = Field(..., min_length=1)
    selected_format: str = Field(..., min_length=1, max_length=80)
    vcb_id: str = Field(..., min_length=1)
    beat_clusters: list[BeatClusterPlan] = Field(..., min_length=1)
    preview_image_paths: list[str] = Field(default_factory=list)
    render_target_path: str = Field(..., min_length=1)
    created_at: datetime


class ArcRenderJobRecord(BaseModel):
    job_id: str = Field(..., min_length=1)
    content_output_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    status: ArcRenderJobStatus
    selected_format: str = Field(..., min_length=1, max_length=80)
    beat_clusters: list[BeatClusterPlan] = Field(default_factory=list)
    first_frame_check: FirstFrameAuthorityCheck | None = None
    epic_meaning_gate: EpicMeaningGateResult | None = None
    manifest_id: str = Field(default="", max_length=120)
    composition_id: str = Field(default="", max_length=120)
    perceptual_plan: Any | None = None
    perceptual_report: Any | None = None
    preservation_report: Any | None = None
    created_at: datetime
    updated_at: datetime



class ArcRenderCreateRequest(BaseModel):
    coalition_spine: CoalitionSpineInput


class ArcRenderReleaseResult(BaseModel):
    job_id: str = Field(..., min_length=1)
    composition_id: str = Field(..., min_length=1)
    release_receipt_id: str = Field(..., min_length=1)
    released_at: datetime
