# CCP Studio Block — Architecture Analysis & Recommendation

## The Vision
Replace the OBS-dependent `FR-CA11-13` (Recording Controller) and `FR-CA11-14` (Live Overlay) with a native **CCP Studio** integrated directly into the AFFiNE clone. The Studio handles all recording, streaming, and teleprompter workflows — eliminating the need for coaches to leave the Coaching OS.

---

## Source Repos Evaluated

| Repo | Stack | Relevance | Verdict |
|---|---|---|---|
| **TribeNest** (yours) | Node/Express + Next.js + Vite + PostgreSQL + Redis | ⭐ High — live streaming/restreaming, social mgmt | **PRIMARY BASE** — you own it, stack-aligned |
| **Cap** (CapSoftware) | Rust + Tauri + SolidStart + MySQL + AGPLv3 | Medium — Loom-style recording | **BORROW LOGIC** — WebRTC recording patterns only |
| **QPrompt** | C++ / Qt / QML / GPL3 | Low — teleprompter only | **SKIP** — wrong stack, rebuild in React (trivial) |

---

## The 5 Recording Modes

Each mode follows the same lifecycle: **Draft → Script + Assets → Record → Auto-Edit Pipeline**

### Mode 1: YouTube Long-Form (6-8 min)
- **Input:** Script page in AFFiNE + visual assets (images/Excalidraw diagrams)
- **Recording:** Webcam + screen/slides composition. Teleprompter overlay on coach's screen
- **Post-Record:** Upload → CMF Editor pipeline (`FR-CA11-12` triggers FFmpeg + Remotion)
- **Output:** Edited `.mp4` delivered to AFFiNE Content Library

### Mode 2: Shorts / Vertical (< 60s)
- **Input:** Short script (optional teleprompter)
- **Recording:** Webcam only, vertical aspect ratio (9:16)
- **Post-Record:** Upload → CMF Editor pipeline (short-form editorial template)
- **Output:** Vertical `.mp4` + auto-generated captions

### Mode 3: Webinar (Live Stream)
- **Input:** Presentation visual assets + script + webinar brief (`FR52`)
- **Recording:** Webcam + slide deck composition **+ RTMP stream** to YouTube/Telegram/custom
- **Post-Record:** Full recording saved → Session Recap pipeline (`FR-CA11-05`)
- **Output:** VOD recording + course chapter extraction (`FR-CA11-07`)

### Mode 4: Course Video
- **Input:** Course chapter script (`FR-CA11-07`) + visual assets + Excalidraw diagrams
- **Recording:** Same as YouTube but with editorial template `course_video`
- **Post-Record:** Upload → CMF pipeline with course-specific intro/outro/chapter markers
- **Output:** Branded course video → dripped to client workspaces via `FR-CA11-03`

### Mode 5: Loom-style Quick Message
- **Input:** No script — spontaneous recording
- **Recording:** Webcam bubble + screen capture (Cap-style)
- **Post-Record:** Upload → transcription only (no full edit pipeline)
- **Output:** Shareable link + transcript in AFFiNE page

---

## Architecture: What Goes Where

### Layer 1: AFFiNE Studio Block (Frontend — React/BlockSuite)
A custom BlockSuite block (`ccp-blocks/studio-block/`) that renders the recording UI:

- **Webcam preview** — `navigator.mediaDevices.getUserMedia()` (standard WebRTC)
- **Screen/slide capture** — `navigator.mediaDevices.getDisplayMedia()` (standard WebRTC)
- **Teleprompter overlay** — React component that takes AFFiNE page text, renders it in large scrolling format with adjustable speed. Pure CSS animation — no external dependency needed
- **Asset panel** — Side panel showing the visual assets (images, Excalidraw diagrams) assigned to this script, with drag-to-timeline ordering
- **Thumbnail preview** — Shows the CVE Canva Clone thumbnail template for the content being recorded
- **Recording controls** — Start/Stop/Pause buttons, format selector (landscape/vertical/stream), timer

### Layer 2: TribeNest Streaming Core (Backend — Node.js)
Extracted from your own TribeNest repo and adapted:

- **RTMP ingest server** — receives the browser's MediaRecorder stream via WebSocket, repackages to RTMP
- **Multi-destination restreaming** — YouTube Live, Facebook Live, Telegram (via RTMPS endpoints)
- **Recording storage** — parallel recording to S3 during live stream
- **Stream health monitoring** — bitrate, frame drops, connection status (pushed back to Studio Block UI)

### Layer 3: CCP Pipeline Orchestrator (Backend — Python/FastAPI)
Already built — this is the existing CA11 infrastructure:

- **`POST /studio/upload`** — receives completed recording blob, stores in S3
- **Pipeline trigger** — based on `recording_mode`, dispatches to the correct CMF editorial template
- **Receipt chain** — `DEP-ENG-041` receipt written on upload completion

---

## What Changes in the Spec Architecture

| Current Spec | Action | Replacement |
|---|---|---|
| `FR-CA11-13` OBS Recording Controller | **REPLACE** | `FR-CA11-13` CCP Studio Block (Recording + Teleprompter) |
| `FR-CA11-14` Excalidraw Live OBS Overlay | **MERGE INTO** | Absorbed into Studio Block's asset panel |
| `FR-CA11-12` Course Video CMF Pipeline | **KEEP** | Unchanged — still the post-production backend |
| `FR-CA11-05` Session Recap Generator | **KEEP** | Still triggered by webinar recordings |

> [!IMPORTANT]
> The OBS WebSocket dependency (`ADR-06`) is retired. OBS remains available as an optional fallback for advanced users, but is no longer architecturally required.

---

## Build Sequence Impact

**Step 19 in `PROMPT_Spec_Build.md` changes from:**
```
Step 19: CA11 Video + OBS Layer
         FR-CA11-12, FR-CA11-13, FR-CA11-14
```
**To:**
```
Step 19: CA11 Video + Studio Layer
         FR-CA11-12 → Course Video CMF Pipeline (unchanged)
         FR-CA11-13 → CCP Studio Block (Recording + Teleprompter + Streaming)
         FR-CA11-14 → RETIRED (merged into FR-CA11-13 Studio Block)
```

---

## Key Technical Decisions Required

1. **WebRTC vs. Native Recording:** Browser `MediaRecorder` API caps at ~720p/30fps reliably. For 1080p+ course videos, do we accept browser-quality or require a lightweight Electron/Tauri wrapper for native capture? (*Recommendation: Start browser-only, add native capture later if quality is insufficient.*)

2. **RTMP Streaming:** TribeNest's streaming backend needs extraction from its monorepo into a standalone microservice. The RTMP ingest should run as a separate Docker container alongside AFFiNE. (*This is a 2-3 day extraction task.*)

3. **Teleprompter Source:** Should the teleprompter always pull from the current AFFiNE page, or should there be a dedicated "script" field? (*Recommendation: Use the current page content by default, but allow `/teleprompter [page-link]` to specify a different source.*)

4. **Thumbnail Integration:** Should the thumbnail preview be a live Canva Clone embed or a static preview image? (*Recommendation: Static preview sourced from CVE pipeline output, with a "Edit in Canva" deep link.*)
