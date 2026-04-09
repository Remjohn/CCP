// =============================================================================
// FR-VID-13 — Zustand Store (Central State Management)
// Implements DEP-VID-033: Studio Project State
// Referenced by all 6 panels and Gate O
// =============================================================================

import { create } from "zustand";
import {
  type CharacterPackage,
  type AnimationClipLibrary,
  type AnimationClip,
  type RemotionManifest,
  type ManifestBeat,
  type BPMAnalysisResult,
  type AnimationManifestPatch,
  type ManifestPatchOperation,
  type BoneOverrideKeyframe,
  type LipSyncKeyframe,
  type TargetFormat,
  type SceneId,
  type PlaybackSpeed,
  type QuantizeLevel,
  type FrameExportJob,
  FORMAT_DIMENSIONS,
} from "./types";

// ---------------------------------------------------------------------------
// Store Shape
// ---------------------------------------------------------------------------
export interface StudioState {
  // --- Character ---
  characterPackage: CharacterPackage | null;
  loadCharacterPackage: (pkg: CharacterPackage) => void;

  // --- Clip Library ---
  clipLibrary: AnimationClipLibrary | null;
  loadClipLibrary: (lib: AnimationClipLibrary) => void;
  clipSearchQuery: string;
  setClipSearchQuery: (q: string) => void;
  clipCategoryFilter: string | null;
  setClipCategoryFilter: (cat: string | null) => void;

  // --- Manifest ---
  manifest: RemotionManifest | null;
  loadManifest: (m: RemotionManifest) => void;

  // --- Beat Selection ---
  selectedBeatIndex: number;
  selectBeat: (idx: number) => void;
  getSelectedBeat: () => ManifestBeat | null;

  // --- Bone Selection ---
  selectedBone: string | null;
  selectBone: (name: string | null) => void;

  // --- Target Format ---
  targetFormat: TargetFormat;
  setTargetFormat: (f: TargetFormat) => void;

  // --- Playback ---
  isPlaying: boolean;
  currentFrame: number;
  loopBeat: boolean;
  loopAll: boolean;
  playbackSpeed: PlaybackSpeed;
  play: () => void;
  pause: () => void;
  stop: () => void;
  setCurrentFrame: (f: number) => void;
  stepForward: () => void;
  stepBackward: () => void;
  toggleLoopBeat: () => void;
  toggleLoopAll: () => void;
  setPlaybackSpeed: (s: PlaybackSpeed) => void;

  // --- Volume ---
  voiceoverVolume: number;
  musicVolume: number;
  setVoiceoverVolume: (v: number) => void;
  setMusicVolume: (v: number) => void;

  // --- BPM ---
  bpmData: BPMAnalysisResult | null;
  loadBPMData: (data: BPMAnalysisResult) => void;

  // --- Layer Visibility ---
  layerVisibility: Record<string, boolean>;
  toggleLayerVisibility: (layerName: string) => void;
  layerOpacity: Record<string, number>;
  setLayerOpacity: (layerName: string, opacity: number) => void;
  layerOrder: string[];
  reorderLayers: (from: number, to: number) => void;

  // --- Patch Operations ---
  patchOperations: ManifestPatchOperation[];
  addPatchOperation: (op: ManifestPatchOperation) => void;
  clearPatchOperations: () => void;
  reviewNotes: string;
  setReviewNotes: (notes: string) => void;

  // --- Clip Swap (Unit 2) ---
  swapClipOnBeat: (beatIndex: number, newClipId: string) => void;

  // --- Scene Swap ---
  swapSceneOnBeat: (beatIndex: number, newSceneId: SceneId) => void;

  // --- Bone Override (Unit 5) ---
  setBoneKeyframe: (beatIndex: number, boneName: string, frame: number, rotation: number) => void;
  clearBoneKeyframe: (beatIndex: number, boneName: string, frame: number) => void;
  resetBoneOverrides: (beatIndex: number, boneName: string) => void;

  // --- Lip Sync (Unit 4) ---
  toggleLipSync: (beatIndex: number) => void;
  lipSyncKeyframes: Record<number, LipSyncKeyframe[]>; // keyed by beat index
  setLipSyncKeyframes: (beatIndex: number, keyframes: LipSyncKeyframe[]) => void;

  // --- Export ---
  exportJobs: FrameExportJob[];
  addExportJob: (job: FrameExportJob) => void;
  updateExportJob: (jobId: string, update: Partial<FrameExportJob>) => void;

  // --- Force Auth Mode (§7 Backward Compatibility) ---
  forceAuthMode: boolean;
  setForceAuthMode: (v: boolean) => void;

  // --- Generate Manifest Patch (Unit 5 output: DEP-VID-037) ---
  generateManifestPatch: () => AnimationManifestPatch;
}

// ---------------------------------------------------------------------------
// Store Implementation
// ---------------------------------------------------------------------------
export const useStudioStore = create<StudioState>((set, get) => ({
  // --- Character ---
  characterPackage: null,
  loadCharacterPackage: (pkg) => {
    const visibility: Record<string, boolean> = {};
    const opacity: Record<string, number> = {};
    const order: string[] = [];
    for (const layer of pkg.layers) {
      visibility[layer.name] = true;
      opacity[layer.name] = 1.0;
      order.push(layer.name);
    }
    set({
      characterPackage: pkg,
      layerVisibility: visibility,
      layerOpacity: opacity,
      layerOrder: order,
    });
  },

  // --- Clip Library ---
  clipLibrary: null,
  loadClipLibrary: (lib) => set({ clipLibrary: lib }),
  clipSearchQuery: "",
  setClipSearchQuery: (q) => set({ clipSearchQuery: q }),
  clipCategoryFilter: null,
  setClipCategoryFilter: (cat) => set({ clipCategoryFilter: cat }),

  // --- Manifest ---
  manifest: null,
  loadManifest: (m) => set({ manifest: m, selectedBeatIndex: 0 }),

  // --- Beat Selection ---
  selectedBeatIndex: 0,
  selectBeat: (idx) => set({ selectedBeatIndex: idx, currentFrame: 0 }),
  getSelectedBeat: () => {
    const { manifest, selectedBeatIndex } = get();
    if (!manifest) return null;
    return manifest.beats[selectedBeatIndex] ?? null;
  },

  // --- Bone Selection ---
  selectedBone: null,
  selectBone: (name) => set({ selectedBone: name }),

  // --- Target Format ---
  targetFormat: "9:16",
  setTargetFormat: (f) => set({ targetFormat: f }),

  // --- Playback ---
  isPlaying: false,
  currentFrame: 0,
  loopBeat: true,
  loopAll: false,
  playbackSpeed: 1,
  play: () => set({ isPlaying: true }),
  pause: () => set({ isPlaying: false }),
  stop: () => set({ isPlaying: false, currentFrame: 0 }),
  setCurrentFrame: (f) => set({ currentFrame: Math.max(0, f) }),
  stepForward: () => set((s) => ({ currentFrame: s.currentFrame + 1 })),
  stepBackward: () => set((s) => ({ currentFrame: Math.max(0, s.currentFrame - 1) })),
  toggleLoopBeat: () => set((s) => ({ loopBeat: !s.loopBeat })),
  toggleLoopAll: () => set((s) => ({ loopAll: !s.loopAll })),
  setPlaybackSpeed: (s) => set({ playbackSpeed: s }),

  // --- Volume ---
  voiceoverVolume: 0.8,
  musicVolume: 0.3,
  setVoiceoverVolume: (v) => set({ voiceoverVolume: v }),
  setMusicVolume: (v) => set({ musicVolume: v }),

  // --- BPM ---
  bpmData: null,
  loadBPMData: (data) => set({ bpmData: data }),

  // --- Layer Visibility ---
  layerVisibility: {},
  toggleLayerVisibility: (layerName) =>
    set((s) => ({
      layerVisibility: {
        ...s.layerVisibility,
        [layerName]: !s.layerVisibility[layerName],
      },
    })),
  layerOpacity: {},
  setLayerOpacity: (layerName, opacity) =>
    set((s) => ({
      layerOpacity: {
        ...s.layerOpacity,
        [layerName]: Math.max(0, Math.min(1, opacity)),
      },
    })),
  layerOrder: [],
  reorderLayers: (from, to) =>
    set((s) => {
      const order = [...s.layerOrder];
      const [moved] = order.splice(from, 1);
      order.splice(to, 0, moved);
      return { layerOrder: order };
    }),

  // --- Patch Operations ---
  patchOperations: [],
  addPatchOperation: (op) =>
    set((s) => {
      // Deduplicate: if same path exists, replace; else append
      const existing = s.patchOperations.findIndex((p) => p.path === op.path);
      if (existing >= 0) {
        const updated = [...s.patchOperations];
        updated[existing] = op;
        return { patchOperations: updated };
      }
      return { patchOperations: [...s.patchOperations, op] };
    }),
  clearPatchOperations: () => set({ patchOperations: [] }),
  reviewNotes: "",
  setReviewNotes: (notes) => set({ reviewNotes: notes }),

  // --- Clip Swap (Unit 2) ---
  swapClipOnBeat: (beatIndex, newClipId) => {
    const { manifest, addPatchOperation } = get();
    if (!manifest) return;
    // Update local manifest
    const updatedBeats = [...manifest.beats];
    if (updatedBeats[beatIndex]) {
      updatedBeats[beatIndex] = {
        ...updatedBeats[beatIndex],
        character_overlay: {
          ...updatedBeats[beatIndex].character_overlay,
          animation_primary: newClipId,
        },
      };
      set({ manifest: { ...manifest, beats: updatedBeats } });
      // Record patch operation
      addPatchOperation({
        op: "replace",
        path: `/beats/${beatIndex}/character_overlay/animation_primary`,
        value: newClipId,
      });
    }
  },

  // --- Scene Swap ---
  swapSceneOnBeat: (beatIndex, newSceneId) => {
    const { manifest, addPatchOperation } = get();
    if (!manifest) return;
    const updatedBeats = [...manifest.beats];
    if (updatedBeats[beatIndex]) {
      updatedBeats[beatIndex] = {
        ...updatedBeats[beatIndex],
        character_overlay: {
          ...updatedBeats[beatIndex].character_overlay,
          scene_id: newSceneId,
        },
      };
      set({ manifest: { ...manifest, beats: updatedBeats } });
      addPatchOperation({
        op: "replace",
        path: `/beats/${beatIndex}/character_overlay/scene_id`,
        value: newSceneId,
      });
    }
  },

  // --- Bone Override (Unit 5) ---
  setBoneKeyframe: (beatIndex, boneName, frame, rotation) => {
    const { manifest, addPatchOperation } = get();
    if (!manifest) return;
    const updatedBeats = [...manifest.beats];
    const beat = updatedBeats[beatIndex];
    if (!beat) return;

    const overrides = { ...(beat.character_overlay.bone_overrides || {}) };
    const boneKFs = [...(overrides[boneName] || [])];
    const existingIdx = boneKFs.findIndex((kf) => kf.frame === frame);
    if (existingIdx >= 0) {
      boneKFs[existingIdx] = { ...boneKFs[existingIdx], frame, rotation };
    } else {
      boneKFs.push({ frame, rotation });
    }
    boneKFs.sort((a, b) => a.frame - b.frame);
    overrides[boneName] = boneKFs;

    updatedBeats[beatIndex] = {
      ...beat,
      character_overlay: {
        ...beat.character_overlay,
        bone_overrides: overrides,
      },
    };
    set({ manifest: { ...manifest, beats: updatedBeats } });
    addPatchOperation({
      op: "replace",
      path: `/beats/${beatIndex}/character_overlay/bone_overrides`,
      value: overrides,
    });
  },

  clearBoneKeyframe: (beatIndex, boneName, frame) => {
    const { manifest, addPatchOperation } = get();
    if (!manifest) return;
    const updatedBeats = [...manifest.beats];
    const beat = updatedBeats[beatIndex];
    if (!beat || !beat.character_overlay.bone_overrides) return;

    const overrides = { ...beat.character_overlay.bone_overrides };
    const boneKFs = (overrides[boneName] || []).filter((kf) => kf.frame !== frame);
    if (boneKFs.length === 0) {
      delete overrides[boneName];
    } else {
      overrides[boneName] = boneKFs;
    }

    updatedBeats[beatIndex] = {
      ...beat,
      character_overlay: {
        ...beat.character_overlay,
        bone_overrides: Object.keys(overrides).length > 0 ? overrides : undefined,
      },
    };
    set({ manifest: { ...manifest, beats: updatedBeats } });
    addPatchOperation({
      op: "replace",
      path: `/beats/${beatIndex}/character_overlay/bone_overrides`,
      value: Object.keys(overrides).length > 0 ? overrides : null,
    });
  },

  resetBoneOverrides: (beatIndex, boneName) => {
    const { manifest, addPatchOperation } = get();
    if (!manifest) return;
    const updatedBeats = [...manifest.beats];
    const beat = updatedBeats[beatIndex];
    if (!beat || !beat.character_overlay.bone_overrides) return;

    const overrides = { ...beat.character_overlay.bone_overrides };
    delete overrides[boneName];

    updatedBeats[beatIndex] = {
      ...beat,
      character_overlay: {
        ...beat.character_overlay,
        bone_overrides: Object.keys(overrides).length > 0 ? overrides : undefined,
      },
    };
    set({ manifest: { ...manifest, beats: updatedBeats } });
    addPatchOperation({
      op: "replace",
      path: `/beats/${beatIndex}/character_overlay/bone_overrides`,
      value: Object.keys(overrides).length > 0 ? overrides : null,
    });
  },

  // --- Lip Sync (Unit 4) ---
  toggleLipSync: (beatIndex) => {
    const { manifest, addPatchOperation } = get();
    if (!manifest) return;
    const updatedBeats = [...manifest.beats];
    const beat = updatedBeats[beatIndex];
    if (!beat) return;
    const newVal = !beat.character_overlay.lip_sync_enabled;
    updatedBeats[beatIndex] = {
      ...beat,
      character_overlay: {
        ...beat.character_overlay,
        lip_sync_enabled: newVal,
      },
    };
    set({ manifest: { ...manifest, beats: updatedBeats } });
    addPatchOperation({
      op: "replace",
      path: `/beats/${beatIndex}/character_overlay/lip_sync_enabled`,
      value: newVal,
    });
  },
  lipSyncKeyframes: {},
  setLipSyncKeyframes: (beatIndex, keyframes) =>
    set((s) => ({
      lipSyncKeyframes: { ...s.lipSyncKeyframes, [beatIndex]: keyframes },
    })),

  // --- Export ---
  exportJobs: [],
  addExportJob: (job) => set((s) => ({ exportJobs: [...s.exportJobs, job] })),
  updateExportJob: (jobId, update) =>
    set((s) => ({
      exportJobs: s.exportJobs.map((j) => (j.job_id === jobId ? { ...j, ...update } : j)),
    })),

  // --- Force Auth Mode ---
  forceAuthMode: false,
  setForceAuthMode: (v) => set({ forceAuthMode: v }),

  // --- Generate Manifest Patch (DEP-VID-037 output) ---
  generateManifestPatch: (): AnimationManifestPatch => {
    const state = get();
    const now = new Date().toISOString();
    const patchId = `PATCH-${state.characterPackage?.character_id?.split("-")[1] ?? "UNK"}-${now.slice(0, 10).replace(/-/g, "")}-${String(Math.floor(Math.random() * 999)).padStart(3, "0")}`;

    return {
      patch_id: patchId,
      base_manifest_id: state.manifest?.manifest_id ?? "UNKNOWN",
      character_id: state.characterPackage?.character_id ?? "UNKNOWN",
      operator: "jean-pierre",
      target_format: state.targetFormat,
      timestamp: now,
      bpm_sync_enabled: state.bpmData !== null,
      bpm_tempo: state.bpmData?.tempo_bpm ?? null,
      operations: [...state.patchOperations],
      review_notes: state.reviewNotes,
    };
  },
}));
