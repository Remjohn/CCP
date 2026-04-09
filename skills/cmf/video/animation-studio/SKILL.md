# SKILL — Animation Studio (FR-VID-13)

```yaml
skill_id: "SKILL-VID-013"
skill_name: "animation_studio"
skill_family: "video_animation"
composable: true
applicable_when: "Pipeline stage = character animation review and adjustment"
```

## Purpose

The Animation Studio skill enables operators to review, adjust, and export 2D skeletal character animations within the CCP video pipeline. It is the human adjustment layer between the AnimationDirectorAgent's automatic clip selections and the final Remotion render (FR-VID-08).

The studio is NOT an animation authoring tool. Clips are authored offline in OpenToonz/Synfig/Spine. The studio provides the 10-15% human refinement: clip swaps, bone tweaks (5-15°), timing adjustments, lip sync toggles, and multi-format scene composition.

## Skill Path

`skills/cmf/video/animation-studio/SKILL.md`

## Implementation Modules

- **Frontend:** `apps/animation-studio/` (Next.js 14 + PixiJS v8 + DragonBonesJS)
- **Backend API:** `apps/animation-studio/api/main.py` (FastAPI)
- **Backend Services:**
  - `apps/animation-studio/services/bpm_service.py` — BPM detection (librosa)
  - `apps/animation-studio/services/lip_sync_service.py` — Audio amplitude → b_jaw rotation
  - `apps/animation-studio/services/frame_export_service.py` — Headless PNG frame export
  - `apps/animation-studio/services/clip_import_service.py` — Spine/Lottie/BVH → DragonBones conversion
- **Gate O:** `apps/animation-studio/app/gate-o.ts` — 6 executable validation functions

## DEP-VIDs

| DEP-VID | Name | Direction | Schema |
|---------|------|-----------|--------|
| DEP-VID-035 | Character Package | INPUT | `schemas/dep_vid_035_character_package.schema.json` |
| DEP-VID-036 | Animation Clip Library | REFERENCE | `schemas/dep_vid_036_clip_library.schema.json` |
| DEP-VID-037 | Animation Manifest Patch | OUTPUT | `schemas/dep_vid_037_manifest_patch.schema.json` |
| DEP-VID-038 | Character Frame Export | OUTPUT | `schemas/dep_vid_038_frame_export.schema.json` |
| DEP-VID-032 | Character Pose Export | OUTPUT | `schemas/dep_vid_032_pose_export.schema.json` |
| DEP-VID-033 | Studio Project State | INTERNAL | `schemas/dep_vid_033_studio_state.schema.json` |
| DEP-VID-034 | BPM Analysis Result | INPUT | `schemas/dep_vid_034_bpm_analysis.schema.json` |
| DEP-VID-002 | Remotion Video Manifest | INPUT/OUTPUT | Defined in FR-VID-01 |

## Pipeline Stages

| # | Stage Name | Agent | Receipt |
|---|-----------|-------|---------|
| 1 | STUDIO_CANVAS_INIT | animation_studio | ✅ |
| 2 | STUDIO_TIMELINE_INIT | animation_studio | ✅ |
| 3 | BPM_SYNC_APPLY | animation_studio | ✅ |
| 4 | LIP_SYNC_GENERATE | lip_sync_engine | ✅ |
| 5 | BONE_OVERRIDE | animation_studio | ✅ |
| 6 | CHARACTER_FRAME_EXPORT | animation_render_service | ✅ |
| 7 | SCENE_COMPOSITION | animation_studio | ✅ |
| 8 | CLIP_LIBRARY_IMPORT | library_importer | ✅ |

---

## Gate O — Pre-Session Constraint Network (Animation Studio Integrity Assurance)

**Executable Module:** `apps/animation-studio/app/gate-o.ts`
**Orchestrator Function:** `runGateO()`

Before opening a studio session, the agent must answer ALL 6 questions.
If ANY answer is NO, the agent must resolve the issue before presenting the editor.

### Q1: Character Package Completeness

**Function:** `validateCharacterPackage(pkg)`
**Condition:** `pkg.layers.length > 0 && pkg.skeleton.bones.length >= 15 && pkg.skeleton.root_bone !== null`
**Failure:** Returns `false` with diagnostic identifying missing layers or insufficient bones.

### Q2: Manifest Character Overlay

**Function:** `validateManifestCharacterOverlay(manifest, forceAuthMode)`
**Condition:** Every beat has `character_overlay.animation_primary` AND `character_overlay.scene_id` populated.
**Exception:** If `forceAuthMode === true`, bypass check and allow §7 fallback logic (character authoring mode).
**Failure:** Returns `false` with diagnostic identifying which beat is missing overlay fields.

### Q3: Clip Library Availability

**Function:** `validateClipLibrary(manifest, library, forceAuthMode)`
**Condition:** `Set(manifest clip IDs).difference(Set(library clip IDs))` is empty.
**Failure:** Returns `false` listing clips referenced in manifest but missing from library.

### Q4: Audio Asset Presence

**Function:** `validateAudioPresence(voiceoverUrl, musicUrl)` (async)
**Condition:** HEAD requests to both voiceover and music URLs return HTTP 200/206.
**Failure:** Returns `false` with diagnostic identifying which audio file is inaccessible.

### Q5: Format Specification

**Function:** `validateFormatSpecification(format)`
**Condition:** Format is one of `["9:16", "1:1", "16:9", "4:5"]`. Defaults to `"9:16"` if null.
**Failure:** Returns `false` if format is an unrecognized string.

### Q6: Export Pipeline Ready

**Function:** `validateExportPipelineReady(exportServiceUrl)` (async)
**Condition:** GET `/api/export/health` returns HTTP 200 within 5 seconds.
**Note:** Per spec, Q6 failure displays a warning rather than blocking the editor. The function returns `passed: true` with a warning diagnostic if the service is unreachable.

---

## Backward Compatibility (§7)

If the manifest was generated by a pipeline version without `character_overlay` fields:
1. Studio opens in **character authoring mode**.
2. All beats default to `animation_primary: "idle_breathe"` and `scene_id: "SC-01"`.
3. A `LEGACY_MANIFEST_NO_CHARACTER` warning banner is displayed.
4. Export still works — the operator's selections become the initial overlay fields in a new manifest patch.

## Scene Presets

8 canonical scenes (SC-01 through SC-08) × 4 formats (9:16, 1:1, 16:9, 4:5).
See `apps/animation-studio/app/scene-presets.ts` for the full matrix.

## Safety Limits (§11)

- **Max layers per character:** 50
- **Max package size:** 200 MB
- **Max frames per beat:** 3,600 (2.5 minutes at 24 FPS)
- **Concurrent session lock:** Second instance gets `MANIFEST_LOCKED` warning → read-only mode
