# Tech-Spec: FR-ERA3-25 — AR Overlay Capture Pipeline
**Status:** Ready for Development | **Version:** 1.0 (ERA3 — CBAR-Hardened)

**Created:** 2026-05-13

---

## Pre-Work Log

1. **PROTOCOL LOADED:** `ERA3_Tech_Spec_Writing_Protocol.md` §2.1 confirms Pydantic v2 under `src/ccp/models/`, §2.2 confirms FastAPI route integration, §5.1 confirms Mini App separation doctrine with `startapp` routing.
2. **PRD LOADED:** PRD-06 defines 10 Content Creation Experience Mini Apps that require camera-based interactive recording for content generation. PRD-03 defines CMF rendering pipeline that consumes recorded artifacts.
3. **EPIC LOADED:** Phase 2 Epic 6 (High-Pressure Recall) and Epic 5 (Ranking & Sorting) both imply visual overlays framing the coach's face during recording. Story 6.1 AC explicitly requires visible letter display and timer during capture.
4. **CBAR AUDIT LOADED:** Phase2-M02 (Background Upload), Phase2-M03 (Streaming Audio SLA), Phase2-M04 (Earned Export Gate), Phase2-M07 (Client-Side Timing). Phase1-M03 (Primer Screen Rule) governs camera permission gating.
5. **PRIMITIVES LOADED:** `EXP-FRC-006 "Hypnosedation Reframing"` (timer must not induce panic); `EXP-TRS-001 "Visceral Hooking"` (premium visual quality); `EXP-FBK-001 "RIM Feedback Discipline"` (immediate round feedback); `EXP-FBK-004 "Signature Moment"` (visual payoff on state transitions).
6. **BACKEND FILES READ:** `src/ccp/api/sacred_audio.py` — existing upload contract; `src/ccp/core/receipt_chain.py` — immutable logging; `src/ccp/services/dpa_engine.py` — palette resolution; `src/ccp/api/main.py` — router registration.
7. **TEST PATTERN:** Read `tests/integration/test_ca11_fr15_dpa_engine.py`; direct pytest, deterministic helpers, local `_run()` helper.

---

## 1. Files Read

| # | File | Why It Was Read |
|---|---|---|
| 1 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Required structure, stack, route pattern |
| 2 | `docs/architecture/april_updates/Phase2_Conscious_Reactions_Epics.md` | Story 6.1, 5.1-5.4 visual overlay requirements |
| 3 | `docs/architecture/april_updates/Phase1_Infrastructure_Epics.md` | Phase1-M03 Primer Screen Rule for camera permission |
| 4 | `docs/architecture/april_updates/FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | Shared session, upload, scoring contracts |
| 5 | `docs/architecture/april_updates/FR-ERA3-08_Mini_App_Host_Shell_Tech_Spec.md` | Permission gating, shell bootstrap, surface routing |
| 6 | `docs/architecture/april_updates/FR-ERA3-05g_Alphabet_Challenge_Tech_Spec.md` | First consumer of overlay pipeline — Rosco ring layout |
| 7 | `primitives/experience/friction_ability/EXP-FRC-006.yaml` | Timer reframing constraint |
| 8 | `primitives/experience/trust_branding/EXP-TRS-001.yaml` | Premium visual quality mandate |
| 9 | `primitives/experience/feedback_scoring/EXP-FBK-001.yaml` | Immediate feedback constraint |
| 10 | `primitives/experience/feedback_scoring/EXP-FBK-004.yaml` | Signature moment visual payoff |
| 11 | `src/ccp/api/sacred_audio.py` | Existing upload contract and validation |
| 12 | `src/ccp/services/dpa_engine.py` | Palette resolution for overlay theming |
| 13 | `src/ccp/core/receipt_chain.py` | Immutable audit logging |
| 14 | `src/ccp/api/main.py` | Router registration pattern |

## 2. Overview

### 2.1 Problem Statement

Every Conscious Reactions Mini App (05a–05j) currently specifies audio-only capture with flat UI interaction. No spec defines how to:

- activate the coach's camera and render their face as the visual anchor
- composite interactive game overlays (letter rings, tier rows, timers, question cards) on top of the live camera feed
- capture the composite result (face + overlay) as a single video recording for CMF export
- play synchronized sound effects (timer ticks, transition swooshes, success/fail stings) during the experience
- stream live overlay interaction state to the backend for AI host awareness and post-session analysis

Without this pipeline, every reaction mode produces an audio file and a score — not the viral-ready, game-show-quality vertical video content that drives TikTok/Reels/Shorts engagement. The platform loses its visual identity and the coach's face — its most valuable content asset — is never captured.

### 2.2 Solution

Build a shared AR Overlay Capture Pipeline as a cross-cutting frontend module inside `tools/miniapp-host-shell/src/overlay/`. The pipeline provides:

1. **Camera Layer**: `getUserMedia({ video: true, audio: true })` rendered as a PixiJS v8 `VideoSource` texture filling the canvas background
2. **Overlay Layer**: PixiJS v8 WebGL stage where each reaction mode mounts its specific visual layout (Rosco ring, tier rows, elimination grid, question cards) themed by DPA `ResolvedPalette`
3. **Sound Layer**: Howler.js audio sprite engine for low-latency sound cues synchronized to overlay state transitions
4. **Capture Layer**: `canvas.captureStream(30)` merged with microphone audio track via `MediaRecorder`, producing 9:16 vertical video (720×1280 minimum, 1080×1920 target)
5. **Interaction Journal**: Structured JSON event stream emitted at meaningful state transitions for AI host awareness

Each reaction mode spec consumes this pipeline as a shared dependency. Mode-specific logic (timing, scoring, semantic validation) remains in the mode spec. The overlay pipeline owns rendering, capture, sound, and interaction journaling.

### 2.3 Scope In / Out

**In Scope**

- PixiJS v8 overlay renderer with camera background texture
- Composite video capture pipeline (canvas + audio → MediaRecorder)
- Howler.js sound sprite engine with mode-specific audio packs
- Overlay transition manager for animated state changes
- Overlay interaction journal for AI host awareness
- 9:16 vertical content capture with adaptive resolution
- iOS Safari MP4 / Android WebM format detection
- Backend ingestor for overlay interaction events
- DPA-themed overlay elements

**Out of Scope**

- Face tracking / face-aware AR effects (future Banuba/DeepAR integration — see Technical Decisions)
- Mode-specific game logic (owned by each mode spec)
- CMF rendering pipeline internals (owned by FR-ERA3-12)
- Audio-only NIM scoring pipeline (owned by CORE)

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Component | Source | Purpose |
|---|---|---|---|
| DEP-OVR-001 | `OverlayRenderer` | This spec | PixiJS v8 engine compositing camera feed + mode-specific game overlay |
| DEP-OVR-002 | `CompositeCaptureService` | This spec | `canvas.captureStream()` + `MediaRecorder` pipeline producing 9:16 video |
| DEP-OVR-003 | `OverlaySoundEngine` | This spec | Howler.js integration for transition/timer/feedback audio sprites |
| DEP-OVR-004 | `OverlayTransitionManager` | This spec | Animated transitions between rounds/questions/reveals via PixiJS tweens |
| DEP-OVR-005 | `OverlayInteractionJournal` | This spec | Structured JSON event emitter for AI host awareness |
| DEP-OVR-006 | `OverlayModeAdapter` | This spec | Interface that each reaction mode implements to register its visual layout |
| DEP-OVR-007 | `AdaptiveResolutionManager` | This spec | Detects device capability and selects 720p or 1080p canvas resolution |
| DEP-OVR-008 | `OverlayInteractionIngestor` | This spec | Backend service receiving interaction journal events |

### 3.2 Existing Backend Integration

| File | Path | How Used |
|---|---|---|
| `sacred_audio.py` | `src/ccp/api/sacred_audio.py` | **PATTERN REFERENCE** — upload contract extended for video media (`sacred-media` namespace) |
| `DPAEngine` | `src/ccp/services/dpa_engine.py` | **CONSUMED** — `ResolvedPalette` themes all overlay elements (colors, gradients, typography) |
| `ReceiptChain` | `src/ccp/core/receipt_chain.py` | **CONSUMED** — logs capture start/stop, format fallback, resolution adaptation, journal persistence |
| `api.main` | `src/ccp/api/main.py` | **EXTENDED** — registers overlay interaction ingestor endpoint |
| `MiniAppHostShell` | `tools/miniapp-host-shell/` | **EXTENDED** — overlay modules live inside the shared shell workspace |

### 3.3 ADR-05 Primitives

| ID | Name | Family | Constraint |
|---|---|---|---|
| `EXP-FRC-006` | Hypnosedation Reframing | friction_ability | Timer overlays must increase focus, not panic. Progress bars use neutral depleting glow, not flashing red alarms. |
| `EXP-TRS-001` | Visceral Hooking | trust_branding | Overlay visuals must feel premium. DPA palette injection is mandatory — no generic gray UI elements in the captured video. |
| `EXP-FBK-001` | RIM Feedback Discipline | feedback_scoring | Round result feedback (pass/fail color change, sound sting) must appear within the same frame as the state transition. |
| `EXP-FBK-004` | Signature Moment | feedback_scoring | Key moments (letter snap into ring, tier placement, elimination strike) must have satisfying visual payoff with synchronized sound. |

### 3.4 CBAR Mandate Enforcement

| Mandate | Phase-M# | Story | Implementation Mechanism |
|---|---|---|---|
| The Primer Screen Rule | Phase1-M03 | Story 1.3 | Camera permission must be gated by `PrimerScreenComposer` from FR-ERA3-08 before `getUserMedia()` is called. The overlay pipeline must NOT call `getUserMedia()` directly — it receives the granted stream from the shell. |
| The Background Upload Rule | Phase2-M02 | Story 1.2 | Composite video upload uses the same `upload_status="pending_background"` contract as CORE audio. The user is never blocked waiting for video upload. |
| The Streaming Audio SLA | Phase2-M03 | Story 1.3 | Audio track from `getUserMedia` is STILL streamed to NIM in 10-second chunks for scoring, independent of composite video capture. Video capture does not replace audio streaming. |
| The Earned Export Gate | Phase2-M04 | Story 2.1 | Composite video is subject to the same biometric/anti-centroid gates as audio artifacts. A visually captured session does not bypass quality gates. |

### 3.5 Technical Decisions

| Decision | Rationale | Alternative Rejected | Why Rejected |
|---|---|---|---|
| PixiJS v8 for overlay rendering | WebGL/WebGPU-capable 2D engine, handles video textures natively, MIT license, zero recurring cost | Raw Canvas 2D API | Insufficient animation/transition performance for game-show quality overlays |
| Howler.js for sound design | Cross-browser, audio sprite support, auto-fallback to HTML5 Audio, low-latency playback | Tone.js | Over-engineered for sound effect playback; Tone.js is for music synthesis |
| Start without face tracking SDK | The Rosco-style overlay does not require face tracking — camera feed is a background texture. Avoids Banuba/DeepAR licensing cost until face-aware effects are validated as necessary | Integrate Banuba from day one | Adds annual enterprise licensing cost before validating that face tracking improves engagement metrics |
| 9:16 vertical canvas at 720×1280 default | Matches TikTok/Reels/Shorts native format; 720p is stable on mid-range mobile devices | 1080×1920 default | Causes frame drops on lower-end devices; adaptive upgrade to 1080p when device supports it |
| `canvas.captureStream(30)` + `MediaRecorder` | Standard browser APIs, no external recording SDK needed, supported on both iOS Safari and Android Chrome | Server-side re-rendering from raw camera + interaction journal | Adds infrastructure cost and latency; client-side composite is sufficient for social media quality |
| Dual-track capture (audio to NIM + video to sacred-media) | Preserves the existing streaming audio scoring pipeline while adding video capture as a parallel track | Replace audio streaming with video-only capture | Breaks the 3-second scoring SLA — NIM scores audio, not video |
| Interaction journal emits on state transitions only, not every frame | 30fps event streams would overwhelm the WebSocket channel and backend | Per-frame event emission | Creates 30× the data volume with no scoring value; state transitions capture all meaningful moments |

## 4. Implementation Plan

### Phase 1 — Data Contracts

- [ ] Create `src/ccp/models/overlay_capture_models.py`
- [ ] Define `OverlayInteractionEvent`, `CompositeCaptureMetadata`, `OverlayModeConfig`, `AdaptiveResolutionProfile`
- [ ] Define `OverlayCaptureStatus` and `OverlayMediaFormat` enums

### Phase 2 — Overlay Renderer and Capture

- [ ] Create `tools/miniapp-host-shell/src/overlay/OverlayRenderer.js`
- [ ] Create `tools/miniapp-host-shell/src/overlay/CompositeCaptureService.js`
- [ ] Create `tools/miniapp-host-shell/src/overlay/AdaptiveResolutionManager.js`
- [ ] Create `tools/miniapp-host-shell/src/overlay/OverlayModeAdapter.js` (interface)

### Phase 3 — Sound and Transitions

- [ ] Create `tools/miniapp-host-shell/src/overlay/OverlaySoundEngine.js`
- [ ] Create `tools/miniapp-host-shell/src/overlay/OverlayTransitionManager.js`
- [ ] Create `tools/miniapp-host-shell/public/audio/` directory with mode-specific audio sprite packs

### Phase 4 — Interaction Journal and Backend

- [ ] Create `tools/miniapp-host-shell/src/overlay/OverlayInteractionJournal.js`
- [ ] Create `src/ccp/services/overlay_interaction_ingestor.py`
- [ ] Create `src/ccp/api/overlay_interaction_api.py`
- [ ] Register the router in `src/ccp/api/main.py`
- [ ] Add receipt logging for capture events through `src/ccp/core/receipt_chain.py`

### Phase 5 — Verification

- [ ] Add `tests/unit/test_overlay_interaction_journal.py`
- [ ] Add `tests/integration/test_era3_fr25_overlay_capture.py`
- [ ] Add manual QA scenarios in Section 10

## 5. Primary Output Schema

```python
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class OverlayMediaFormat(str, Enum):
    WEBM_VP9 = "video/webm;codecs=vp9"
    MP4_H264 = "video/mp4;codecs=avc1"


class OverlayCaptureStatus(str, Enum):
    IDLE = "idle"
    RECORDING = "recording"
    PAUSED_BACKGROUNDED = "paused_backgrounded"
    STOPPED = "stopped"
    FAILED_RECOVERABLE = "failed_recoverable"


class AdaptiveResolutionProfile(BaseModel):
    width: int = Field(default=720, ge=360)
    height: int = Field(default=1280, ge=640)
    frame_rate: int = Field(default=30, ge=15, le=60)
    video_bitrate_bps: int = Field(default=4_000_000, ge=1_000_000, le=8_000_000)
    media_format: OverlayMediaFormat = Field(...)
    device_tier: Literal["low", "mid", "high"] = Field(default="mid")
    resolution_downgraded: bool = Field(default=False)


class OverlayInteractionEvent(BaseModel):
    event_type: Literal[
        "overlay_mounted",
        "capture_started",
        "round_state_change",
        "transition_played",
        "sound_cue_played",
        "capture_stopped",
        "resolution_adapted",
        "capture_failed",
    ] = Field(...)
    session_id: str = Field(...)
    timestamp_ms: int = Field(..., ge=0)
    round_index: int | None = Field(default=None, ge=1)
    from_state: str | None = Field(default=None)
    to_state: str | None = Field(default=None)
    overlay_elements: dict = Field(default_factory=dict, description="Mode-specific visible element state snapshot")
    capture_state: dict = Field(default_factory=dict, description="Current recording health: fps, resolution, audio level")
    receipt_id: str | None = Field(default=None)


class CompositeCaptureMetadata(BaseModel):
    session_id: str = Field(...)
    coach_id: str = Field(...)
    resolution: AdaptiveResolutionProfile = Field(...)
    capture_status: OverlayCaptureStatus = Field(...)
    started_at: datetime | None = Field(default=None)
    stopped_at: datetime | None = Field(default=None)
    duration_ms: int = Field(default=0, ge=0)
    blob_size_bytes: int = Field(default=0, ge=0)
    upload_status: Literal[
        "pending_background",
        "uploading",
        "uploaded",
        "failed_retryable",
    ] = Field(default="pending_background")
    interaction_event_count: int = Field(default=0, ge=0)
    audio_track_present: bool = Field(default=True)
    video_track_present: bool = Field(default=True)


class OverlayModeConfig(BaseModel):
    mode_key: str = Field(..., min_length=1, description="e.g. react_alphabet, react_tierlist")
    overlay_layout: Literal[
        "rosco_ring",
        "tier_rows",
        "rank_slots",
        "elimination_grid",
        "question_card",
        "split_screen",
        "generic_overlay",
    ] = Field(...)
    sound_pack: str = Field(default="default", description="Audio sprite pack identifier")
    camera_position: Literal["background_fill", "pip_corner", "split_half"] = Field(default="background_fill")
    requires_face_tracking: bool = Field(default=False)
    target_aspect_ratio: Literal["9:16", "16:9", "1:1"] = Field(default="9:16")
```

## 6. Backward Compatibility Fallback

| Failure Condition | Fallback Behavior |
|---|---|
| `getUserMedia` video denied or unavailable | Fall back to audio-only capture. Overlay renders without camera background (solid DPA-themed gradient). Interaction journal and sound engine remain active. `video_track_present=false` in metadata. |
| `canvas.captureStream()` unsupported | Fall back to audio-only recording via existing CORE path. Log degradation receipt. The interactive overlay still renders for the live experience but is not captured as video. |
| `MediaRecorder` format not supported | Detect via `MediaRecorder.isTypeSupported()`. Try `video/mp4` first on iOS, `video/webm;codecs=vp9` on Android/Desktop. If neither works, fall back to audio-only. |
| Device cannot sustain 720p at 30fps | `AdaptiveResolutionManager` drops to 540×960 at 24fps. Logs `resolution_downgraded=true` in metadata. |
| App backgrounded during recording | Pause capture, persist interaction journal to local storage. On foreground resume, attempt stream reinitialization. If stream is unrecoverable, finalize with partial capture and `capture_status="paused_backgrounded"`. |
| Howler.js audio context blocked | Sound engine requires user gesture to initialize. If blocked, overlay continues without sound cues. `sound_enabled=false` logged in journal. |

## 7. Tasks

### Backend

- [ ] Add `src/ccp/models/overlay_capture_models.py`
- [ ] Add `src/ccp/services/overlay_interaction_ingestor.py`
- [ ] Add `src/ccp/api/overlay_interaction_api.py`
- [ ] Register the router in `src/ccp/api/main.py`
- [ ] Add receipt logging for capture lifecycle events through `src/ccp/core/receipt_chain.py`
- [ ] Extend `sacred-audio` storage namespace to `sacred-media` for video blobs

### Frontend

- [ ] Create `tools/miniapp-host-shell/src/overlay/OverlayRenderer.js`
- [ ] Create `tools/miniapp-host-shell/src/overlay/CompositeCaptureService.js`
- [ ] Create `tools/miniapp-host-shell/src/overlay/AdaptiveResolutionManager.js`
- [ ] Create `tools/miniapp-host-shell/src/overlay/OverlaySoundEngine.js`
- [ ] Create `tools/miniapp-host-shell/src/overlay/OverlayTransitionManager.js`
- [ ] Create `tools/miniapp-host-shell/src/overlay/OverlayInteractionJournal.js`
- [ ] Create `tools/miniapp-host-shell/src/overlay/OverlayModeAdapter.js`
- [ ] Add `tools/miniapp-host-shell/public/audio/` with default audio sprite packs

### Testing

- [ ] Add unit tests for format detection, resolution adaptation, and journal schema validation
- [ ] Add integration tests for capture pipeline lifecycle and backend ingestor
- [ ] Add manual QA for iOS Safari vs Android Chrome format handling

## 8. Acceptance Criteria

### AC-25A — Camera Feed Must Render as Overlay Background

**CBAR Mandate Enforced:** Phase1-M03 — The Primer Screen Rule
**Primitive Reference:** `EXP-TRS-001`

**Given** the user grants camera permission through the Primer Screen,
**When** the overlay renderer mounts,
**Then** the camera feed fills the canvas background at the target aspect ratio,
**And** overlay elements render on top of the camera feed,
**And** the coach's face remains the visual anchor.

**FAILURE EXAMPLE:** The overlay renders on a black background with no camera feed because `getUserMedia` was called before the Primer Screen completed. The coach sees a dark void instead of their face. This is a spec violation.

### AC-25B — Composite Video Must Capture Face + Overlay Together

**Primitive Reference:** `EXP-TRS-001`, `EXP-FBK-004`

**Given** the overlay is rendering with camera background,
**When** recording starts,
**Then** `CompositeCaptureService` produces a single video blob containing both the camera feed and all overlay elements,
**And** the output is 9:16 vertical at 720×1280 minimum,
**And** the audio track contains the coach's voice.

**FAILURE EXAMPLE:** The recorded video contains only the camera feed without the Rosco ring, timers, or score elements. The export looks like a raw selfie video instead of a branded game-show experience. This is a spec violation.

### AC-25C — Sound Cues Must Synchronize with Overlay Transitions

**Primitive Reference:** `EXP-FBK-004`, `EXP-FRC-006`

**Given** a state transition occurs in the overlay,
**When** the transition plays,
**Then** the corresponding sound cue fires within the same animation frame,
**And** timer sounds follow the Hypnosedation Reframing constraint (focused drill, not panic alarm).

**FAILURE EXAMPLE:** The letter ring advances but the transition sound plays 400ms later, creating a disconnected, low-quality feel. Or the timer uses an aggressive alarm that triggers performance anxiety. This is a spec violation.

### AC-25D — Video Upload Must Not Block the User

**CBAR Mandate Enforced:** Phase2-M02 — The Background Upload Rule

**Given** the composite recording is complete,
**When** the user finalizes the session,
**Then** the UI returns immediately with `upload_status="pending_background"`,
**And** the video blob uploads asynchronously,
**And** the user proceeds to scoring without waiting.

**FAILURE EXAMPLE:** The user finishes a 2-minute Alphabet Challenge and the app blocks on a 50MB video upload spinner. This is a spec violation.

### AC-25E — Interaction Journal Must Stream State Transitions to Backend

**Given** the overlay is active,
**When** a meaningful state change occurs (round start, answer captured, timeout, transition),
**Then** the `OverlayInteractionJournal` emits a structured `OverlayInteractionEvent`,
**And** the event is delivered to the backend ingestor via the existing WebSocket channel or queued for batch submission,
**And** per-frame emission is explicitly forbidden to prevent channel flooding.

**FAILURE EXAMPLE:** The journal emits 30 events per second (one per frame), overwhelming the WebSocket channel and degrading scoring performance. This is a spec violation.

## 9. Dependencies

### Internal

| Dependency | Type | Why Required |
|---|---|---|
| `FR-ERA3-08_Mini_App_Host_Shell_Tech_Spec.md` | Shared spec dependency | Camera permission gating via `PrimerScreenComposer`, shell bootstrap |
| `FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md` | Shared spec dependency | Audio streaming, scoring, upload contracts |
| `src/ccp/services/dpa_engine.py` | Existing visual service | DPA palette for overlay theming |
| `src/ccp/api/main.py` | Existing API composition | Router registration |
| `src/ccp/core/receipt_chain.py` | Existing audit infrastructure | Capture lifecycle receipts |
| `src/ccp/api/sacred_audio.py` | Existing upload pattern | Extended for `sacred-media` video blobs |

### External

| Dependency | Type | Why Required |
|---|---|---|
| PixiJS v8 | Frontend rendering library (MIT) | WebGL overlay rendering with video texture support |
| Howler.js | Frontend audio library (MIT) | Low-latency sound sprite playback |
| Telegram Mini App runtime | Client platform | Required launch surface |
| Browser `getUserMedia()` | Client camera/mic API | Camera feed and audio capture |
| Browser `canvas.captureStream()` | Client capture API | Composite video stream generation |
| Browser `MediaRecorder` | Client recording API | Video blob creation |

## 10. Testing Strategy

### Unit Tests

- `tests/unit/test_overlay_capture_models.py::test_adaptive_resolution_profile_defaults_to_720p`
- `tests/unit/test_overlay_capture_models.py::test_media_format_detection_ios_vs_android`
- `tests/unit/test_overlay_interaction_journal.py::test_event_emits_on_state_transition_not_per_frame`
- `tests/unit/test_overlay_interaction_journal.py::test_event_schema_validates_all_required_fields`

### Integration Tests

- `tests/integration/test_era3_fr25_overlay_capture.py::test_interaction_ingestor_persists_events`
- `tests/integration/test_era3_fr25_overlay_capture.py::test_capture_metadata_links_to_reaction_session`
- `tests/integration/test_era3_fr25_overlay_capture.py::test_sacred_media_upload_contract_matches_sacred_audio_pattern`

### Test Pattern Notes

- Follow the deterministic helper style from `test_ca11_fr15_dpa_engine.py`
- Use explicit fixtures for `OverlayModeConfig` and `AdaptiveResolutionProfile`
- Use a local `_run()` helper if async service calls are exercised

### Manual QA Checklist

1. Launch any overlay-enabled mode and verify camera feed renders as canvas background at 9:16.
2. Complete a challenge session and verify the exported video contains both face and overlay elements.
3. Test on iOS Safari and verify MP4 format is auto-selected.
4. Test on Android Chrome and verify WebM format is auto-selected.
5. Force a low-end device simulation and verify resolution drops to 720×1280 without crashing.
6. Verify sound cues play in sync with overlay transitions.
7. Deny camera permission and verify graceful fallback to audio-only with gradient background.
8. Background the app during recording and verify partial capture recovery on foreground.
9. Verify interaction journal events arrive at the backend ingestor with correct schema.
10. Finalize a session and verify video upload does not block the scoring flow.
