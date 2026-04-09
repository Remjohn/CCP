// =============================================================================
// FR-VID-13 — CCP Animation Studio Type Definitions
// All types trace to §5 Primary Output Schemas and §3 Architecture Traceability
// =============================================================================

// --- DEP-VID-035: Character Package (§5 Schema B) ---
export interface CharacterLayer {
  name: string;
  png_url: string;
  bone: string;
  z_order: number;
}

export interface CharacterBone {
  name: string;
  parent: string | null;
  x: number;
  y: number;
  rotation: number;
}

export interface CharacterSkeleton {
  format: "dragonbones";
  bone_count: number;
  root_bone: string;
  bones: CharacterBone[];
}

export interface CharacterPackage {
  character_id: string;
  display_name: string;
  layers: CharacterLayer[];
  skeleton: CharacterSkeleton;
  skins_available: string[];
  render_dimensions: { width: number; height: number };
}

// --- DEP-VID-036: Animation Clip Library (§5 Schema D) ---
export interface AnimationClip {
  clip_id: string;
  name: string;
  category: "Emotions" | "Gestures" | "Loops" | "Interactions" | "Scenes";
  duration_frames: number;
  affected_bones: string[];
  thumbnails: { gif: string };
  source: "native" | "imported";
  original_format?: "spine" | "lottie" | "bvh";
}

export interface AnimationClipLibrary {
  library_id: string;
  version: string;
  character_base: string;
  clips: AnimationClip[];
  last_updated: string;
}

// --- DEP-VID-037: Animation Manifest Patch (§5 Schema A) ---
export interface ManifestPatchOperation {
  op: "replace" | "add" | "remove";
  path: string;
  value?: unknown;
}

export interface AnimationManifestPatch {
  patch_id: string;
  base_manifest_id: string;
  character_id: string;
  operator: string;
  target_format: TargetFormat;
  timestamp: string;
  bpm_sync_enabled: boolean;
  bpm_tempo: number | null;
  operations: ManifestPatchOperation[];
  review_notes: string;
}

// --- DEP-VID-034: BPM Analysis Result (§5 Schema C) ---
export interface BPMAnalysisResult {
  analysis_id: string;
  music_file: string;
  tempo_bpm: number;
  confidence: number;
  beat_times_sec: number[];
  subdivisions: {
    quarter: number[];
    eighth: number[];
    sixteenth: number[];
  };
  timestamp: string;
}

// --- DEP-VID-033: Studio Project State (§5 Schema E) ---
export interface StudioProjectState {
  session_token: string;
  selected_beat_index: number;
  selected_bone: string | null;
  target_format: TargetFormat;
  playback_state: {
    is_playing: boolean;
    current_frame: number;
    loop_beat: boolean;
  };
  unsaved_patch: AnimationManifestPatch | null;
  volume_levels: {
    voiceover: number;
    music: number;
  };
}

// --- Target Format (§2 Scope: Multi-format output) ---
export type TargetFormat = "9:16" | "1:1" | "16:9" | "4:5";

export const FORMAT_DIMENSIONS: Record<TargetFormat, { width: number; height: number }> = {
  "9:16": { width: 1080, height: 1920 },
  "1:1": { width: 1080, height: 1080 },
  "16:9": { width: 1920, height: 1080 },
  "4:5": { width: 1080, height: 1350 },
};

export const CAROUSEL_DIMENSIONS: Record<TargetFormat, { width: number; height: number }> = {
  "9:16": { width: 2160, height: 3840 },
  "1:1": { width: 2048, height: 2048 },
  "16:9": { width: 3840, height: 2160 },
  "4:5": { width: 2048, height: 2560 },
};

// --- Scene Composition (§4 Stage 7) ---
export type SceneId = "SC-01" | "SC-02" | "SC-03" | "SC-04" | "SC-05" | "SC-06" | "SC-07" | "SC-08";

export interface ScenePreset {
  position: "center" | "bottom-right" | "left" | "right" | "top-right" | "off-left";
  scale_pct: number;
  y_pct: number;
}

export type SceneFormatMatrix = Record<SceneId, Record<TargetFormat, ScenePreset>>;

// --- Beat (from DEP-VID-002 manifest with character_overlay extension) ---
export interface BoneOverrideKeyframe {
  frame: number;
  rotation?: number;
  x?: number;
  y?: number;
  scaleX?: number;
  scaleY?: number;
}

export interface CharacterOverlay {
  animation_primary: string;
  animation_loops?: string[];
  scene_id: SceneId;
  bone_overrides?: Record<string, BoneOverrideKeyframe[]>;
  lip_sync_enabled?: boolean;
}

export interface ManifestBeat {
  beat_index: number;
  beat_type: string;
  arc_stage: string;
  start_frame: number;
  duration_frames: number;
  background_url?: string;
  voiceover_url?: string;
  music_url?: string;
  character_overlay: CharacterOverlay;
  transition_type?: "crossfade" | "cut" | "push";
}

export interface RemotionManifest {
  manifest_id: string;
  project_id: string;
  fps: number;
  beats: ManifestBeat[];
}

// --- Receipt Chain (§Receipt Chain Implementation) ---
export interface PipelineReceipt {
  receipt_id: string;
  previous_receipt_hash: string;
  input_payload_hash: string;
  output_payload_hash: string;
  stage_name: string;
  agent_name: string;
  timestamp: string;
}

// --- Lip Sync Keyframe (§4 Stage 4) ---
export interface LipSyncKeyframe {
  frame: number;
  bone: "b_jaw";
  rotation: number;
}

// --- Clip Import Bone Maps (§4 Stage 8) ---
export interface BoneMap {
  [externalBoneName: string]: string; // maps to CCP canonical bone name
}

// --- Export Job (§4 Stage 6) ---
export type ExportJobStatus = "queued" | "processing" | "completed" | "failed";

export interface FrameExportJob {
  job_id: string;
  character_id: string;
  beat_index: number;
  target_format: TargetFormat;
  scene_id: SceneId;
  status: ExportJobStatus;
  total_frames: number;
  frames_rendered: number;
  output_path: string;
  error?: string;
}

// --- Transport (§8 Task 18) ---
export type PlaybackSpeed = 0.25 | 0.5 | 1 | 1.5 | 2;

// --- Quantize Level (§4 Stage 3) ---
export type QuantizeLevel = "quarter" | "eighth" | "sixteenth";
