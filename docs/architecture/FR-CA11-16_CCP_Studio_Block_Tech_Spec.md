# Tech-Spec: FR-CA11-16 — CCP Studio Block (Full Stack Recording & Streaming)

**Created:** 2026-03-25
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / PRD Update v2.0 — Capability Area 11)
**Architecture Reference:** PRD-Update-CA11 §4.5, ADR-07
**Skill Implementation:** `ccp-blocks/studio-block/` (React/TypeScript, AFFiNE BlockSuite plugin)
**Role Executing:** Principal CCP Tech-Spec Architect
**Replaces:** FR-CA11-13 (OBS Recording Controller), FR-CA11-14 (Excalidraw Live OBS Overlay)

---

## 1. Files Read

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd-update-CA11-quad-platform.md` (§4.5 FR-CA11-16, ADR-07)
- `d:\Work\The Conscious Coaching Factory\docs\features\FB_Full_Stack_Recording_Streaming.md` (FB-STUDIO-03)
- `d:\Work\The Conscious Coaching Factory\MCDA_CCP_Studio_Integration.md` (MCDA IV)

---

## 2. Overview

### Problem Statement
CA11's original architecture (ADR-06) required OBS Studio as an external desktop application for all recording and streaming. This created three structural problems: (1) context switching — coach leaves AFFiNE to manage OBS, (2) no intelligence integration — OBS is unaware of scripts, assets, or CMF templates, (3) local dependency — the recording setup dies with the coach's laptop. MCDA IV scored the native Studio approach at 442 vs OBS baseline at 225.

### Solution
FR-CA11-16 implements the **CCP Studio Block** — a native AFFiNE BlockSuite plugin that provides integrated webcam/screen recording, RTMP streaming, teleprompter, and visual asset management directly inside the coaching workspace. The coach activates it with `/studio` in any AFFiNE page. Recordings upload directly to S3 and trigger the appropriate CMF Pipeline editorial template. Streaming uses a TribeNest-extracted microservice for WebSocket→RTMP relay.

### Scope
**In scope:**
- BlockSuite plugin registration and lifecycle.
- 5 recording modes (YouTube, Shorts, Webinar, Course, Loom).
- WebRTC capture (webcam, screen, canvas compositing).
- MediaRecorder encoding (H.264/VP9, 720p/1080p).
- Teleprompter component (auto-scroll, speed control, mirror mode).
- Asset panel (display visual assets from current AFFiNE page on recording canvas).
- S3 upload with pre-signed URLs.
- CMF Pipeline trigger on recording completion.
- Streaming via ccp-stream-service (WebSocket→RTMP).

**Out of scope:**
- Soundboard & programmable audio (FR-CA11-17).
- Guest join / WebRTC multi-party (FR-CA11-21).
- Stream overlay / Trivianar display (FR-CA11-22).
- Post-production CMF pipeline logic (existing CMF specs).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-060` | Studio Block Plugin Registration | FOUNDATION — BlockSuite custom block registration in AFFiNE fork. |
| `DEP-ENG-061` | Recording Engine | CORE — WebRTC capture + MediaRecorder encoding + canvas compositing. |
| `DEP-ENG-062` | Teleprompter Component | UI — Auto-scrolling script display synced to AFFiNE page content. |
| `DEP-ENG-063` | Asset Panel | UI — Visual asset browser reading current page's block tree for media elements. |
| `DEP-ENG-064` | S3 Upload Handler | OUTPUT — Pre-signed URL generation + chunked upload with resume. |
| `DEP-ENG-065` | CMF Pipeline Trigger | INTEGRATION — POST to CMF endpoint with recording mode + editorial template selection. |
| `DEP-ENG-066` | Streaming WebSocket Client | INTEGRATION — Sends MediaRecorder chunks to ccp-stream-service for RTMP relay. |
| `DEP-ENG-041` | Receipt Chain Guard | INTEGRATION — Receipt written on upload completion. |
| FR-CA11-02 | AFFiNE Sync Service | DOWNSTREAM — Recording metadata pushed to coach workspace via affine_sync.py. |

### Academic Grounding

| Framework | Author | Year | Mechanism |
|---|---|---|---|
| **Cognitive Load Theory** | Sweller | 1988 | Eliminating OBS (a separate application with its own mental model) reduces extraneous cognitive load. The coach's working memory stays allocated to content creation, not tool management. |
| **Flow State Conditions** | Csikszentmihalyi | 1990 | Single-context recording (no app switching) reduces flow-state interruption. The teleprompter keeps the coach "in the zone" by removing the cognitive burden of memorizing scripts. |
| **Technology Acceptance Model** | Davis | 1989 | Perceived ease of use (recording from within the workspace they already use) drives adoption. OBS required a separate learning curve that suppressed adoption among non-technical coaches. |

### Technical Decisions
1. **Browser WebRTC over Native Capture:** The browser's `MediaRecorder` API (WebRTC) is the MVP recording engine. This eliminates native app dependencies and enables cross-platform compatibility. If 1080p quality proves insufficient on certain browsers, a lightweight Electron/Tauri wrapper is the escalation path.
2. **Canvas Compositing for Multi-Source:** When recording webcam + screen simultaneously (YouTube, Course modes), both feeds are drawn onto a `<canvas>` element via `drawImage()`. The canvas's output stream (`canvas.captureStream(30)`) is what MediaRecorder encodes. This enables future overlay compositing (Trivianar display, guest PiP) without architectural changes.
3. **Pre-Signed S3 Upload:** Recordings upload directly from the browser to S3 via pre-signed URLs generated by the CCP FastAPI backend. No intermediate server storage. Chunked upload with resume handles connection interruptions.
4. **TribeNest Extraction for Streaming:** The streaming component is extracted from `github.com/Remjohn/tribenest` into a standalone Docker microservice (`ccp-stream-service`). This avoids bundling RTMP repackaging logic into the browser plugin.

---

## 4. Implementation Plan

### Stage 1: Plugin Registration & UI Shell
*Agent:* `Diego` (Studio Session Conductor)
*Inputs:* AFFiNE fork BlockSuite plugin API.
*Outputs:* `ccp-blocks/studio-block/` registered as `/studio` block type.
*DEP-ID:* `DEP-ENG-060`

**Steps:**
1. Create `ccp-blocks/studio-block/` directory in the AFFiNE fork with standard BlockSuite plugin structure.
2. Register the block as a custom type in AFFiNE's BlockSuite registry. Activation via `/studio` command.
3. Build the UI shell: left panel (preview + controls), right panel (teleprompter + assets + thumbnail).
4. Implement recording mode selector dropdown: YouTube Long-Form, Shorts/Vertical, Webinar/Stream, Course Video, Loom Quick.
5. Implement quality selector: 1080p (default), 720p. Shorts mode locks to 1080p.

### Stage 2: Recording Engine (WebRTC + MediaRecorder)
*Agent:* `Diego`
*Inputs:* Recording mode, quality setting.
*Outputs:* Recorded video blob (WebM or MP4).
*DEP-ID:* `DEP-ENG-061`

**Steps:**
1. Implement webcam capture: `navigator.mediaDevices.getUserMedia({ video: { width: 1920, height: 1080 }, audio: true })`.
2. Implement screen capture: `navigator.mediaDevices.getDisplayMedia({ video: { width: 1920, height: 1080 } })`.
3. Build canvas compositing layer: create `<canvas>` element, draw webcam + screen via `requestAnimationFrame` loop with `ctx.drawImage()`.
4. Configure MediaRecorder: `new MediaRecorder(canvas.captureStream(30), { mimeType: 'video/webm;codecs=vp9', videoBitsPerSecond: 8_000_000 })`.
5. Implement recording controls: Start → `mediaRecorder.start(1000)` (1s chunks), Pause → `mediaRecorder.pause()`, Stop → `mediaRecorder.stop()`.
6. Implement periodic chunk saves to S3 (every 30 seconds) for crash recovery.
7. Handle aspect ratio modes: 16:9 (default) vs 9:16 (Shorts mode — swap width/height).

### Stage 3: Teleprompter Component
*Agent:* `Diego`
*Inputs:* Current AFFiNE page content (via BlockSuite API) or user-selected page.
*Outputs:* Auto-scrolling text overlay in the Studio right panel.
*DEP-ID:* `DEP-ENG-062`

**Steps:**
1. Build React component `<Teleprompter />` in `ccp-blocks/studio-block/components/`.
2. Text source: read current AFFiNE page's text blocks via BlockSuite API. Strip non-text blocks (images, embeds).
3. Implement auto-scroll: CSS `transform: translateY()` animated via `requestAnimationFrame`.
4. Speed control slider: range 1.0–5.0 words-per-second, mapped to scroll velocity.
5. Font size dropdown: 18px, 24px, 32px, 48px.
6. Mirror mode toggle: `transform: scaleX(-1)` for physical teleprompter glass.
7. Click-to-pause/resume scroll.
8. Script selection: list AFFiNE pages tagged as "scripts" from the current workspace.

### Stage 4: Asset Panel
*Agent:* `Diego`
*Inputs:* Current AFFiNE page's block tree.
*Outputs:* Clickable thumbnail grid of visual assets.
*DEP-ID:* `DEP-ENG-063`

**Steps:**
1. Read current page's BlockSuite block tree. Filter for: image blocks, Excalidraw embed blocks, CVE Canva composition blocks.
2. Render filtered assets as a thumbnail grid in the Studio right panel.
3. On click: display the asset full-screen on the recording canvas (overlay layer above webcam).
4. On click again: dismiss overlay, return to webcam-only view.
5. This replaces OBS scene switching — no need for "webcam scene" vs "slides scene."

### Stage 5: S3 Upload & CMF Pipeline Trigger
*Agent:* `Diego`
*Inputs:* Recorded video blob, recording mode.
*Outputs:* S3 URL, CMF job ID.
*DEP-IDs:* `DEP-ENG-064`, `DEP-ENG-065`

**Steps:**
1. On "Stop Recording": request pre-signed S3 upload URL from CCP backend: `POST /studio/upload-url { recording_mode, coach_id, file_size }`.
2. Upload video blob to S3 via chunked PUT.
3. On upload completion: `POST /studio/complete { s3_url, recording_mode, coach_id, source_page_id, duration }`.
4. Backend determines CMF pipeline template based on recording mode:
   - `youtube_longform` → full editorial pipeline (intro/outro, captions, music bed, branded overlays).
   - `short_form_vertical` → auto-captions, dynamic zoom.
   - `webinar_vod` → session recap extraction + content multiplication.
   - `course_video` → chapter markers, captions, Excalidraw diagrams.
   - `loom_quick` → Whisper transcription only, no CMF editorial.
5. Backend creates `studio_sessions` row and triggers the CMF pipeline.
6. Write receipt to Receipt Chain Guard (`DEP-ENG-041`).

### Stage 6: Streaming Engine (ccp-stream-service)
*Agent:* Infrastructure team
*Inputs:* MediaRecorder chunks via WebSocket.
*Outputs:* RTMP streams to configured destinations + parallel S3 VOD archive.
*DEP-ID:* `DEP-ENG-066`

**Steps:**
1. Extract streaming module from TribeNest monorepo (`github.com/Remjohn/tribenest`) into standalone `ccp-stream-service` repository.
2. Dockerize: Node.js/Express app with WebSocket server + `node-media-server` for RTMP repackaging.
3. Implement WebSocket endpoint: `/ws/stream/{session_id}` — accepts MediaRecorder chunks from Studio Block.
4. Implement RTMP muxer: repackage incoming WebM/H264 chunks into RTMP and push to configured destinations (YouTube Live, Facebook Live, Custom RTMP).
5. Implement parallel S3 writer: simultaneously write raw stream data to S3 for VOD archival.
6. Push stream health metrics back to Studio Block via same WebSocket: bitrate, frame drops, connection status per destination, viewer count.
7. Deploy Docker container on AWS EC2/ECS. Configure with environment variables for RTMP destinations.

---

## 5. Primary Output Schema

**Data Object:** Studio Session Record

```json
{
  "transaction_timestamp": "2026-03-25T22:00:00Z",
  "session_id": "uuid-studio-001",
  "coach_id": "uuid-coach-001",
  "source_page_id": "affine-page-uuid-001",
  "recording_mode": "youtube_longform",
  "aspect_ratio": "16:9",
  "resolution": "1080p",
  "s3_recording_url": "s3://ccp-recordings/coach-001/2026-03-25/session-001.webm",
  "s3_vod_url": null,
  "duration_seconds": 480,
  "is_stream": false,
  "stream_destinations": [],
  "cmf_pipeline_template": "youtube_longform",
  "cmf_job_id": "uuid-cmf-job-001",
  "status": "processing",
  "receipt_chain_guard": { "schema_ref": "DEP-ENG-041" }
}
```

---

## 6. Data Model

```sql
CREATE TABLE studio_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    coach_id UUID NOT NULL REFERENCES coaches(id),
    source_page_id VARCHAR(255),
    recording_mode VARCHAR(30) NOT NULL,
    aspect_ratio VARCHAR(5) NOT NULL,
    resolution VARCHAR(10) NOT NULL,
    s3_recording_url TEXT,
    s3_vod_url TEXT,
    duration_seconds INTEGER,
    is_stream BOOLEAN DEFAULT FALSE,
    stream_destinations JSONB,
    cmf_pipeline_template VARCHAR(50),
    cmf_job_id UUID,
    receipt_chain_id UUID REFERENCES receipt_chain(id),
    status VARCHAR(20) DEFAULT 'recording',
    started_at TIMESTAMP WITH TIME ZONE NOT NULL,
    ended_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_studio_sessions_coach ON studio_sessions(coach_id);
CREATE INDEX idx_studio_sessions_status ON studio_sessions(status);
```

---

## 7. Tasks

- [ ] **Task 1:** Create `ccp-blocks/studio-block/` plugin structure in AFFiNE fork. Register `/studio` command.
- [ ] **Task 2:** Build Studio UI shell (left panel: preview + controls, right panel: teleprompter + assets).
- [ ] **Task 3:** Implement webcam + screen capture via WebRTC (`getUserMedia`, `getDisplayMedia`).
- [ ] **Task 4:** Build canvas compositing layer for multi-source recording.
- [ ] **Task 5:** Implement MediaRecorder encoding with configurable quality/aspect ratio.
- [ ] **Task 6:** Build `<Teleprompter />` component with auto-scroll, speed, font size, mirror, pause.
- [ ] **Task 7:** Build Asset Panel: read BlockSuite block tree, render thumbnails, click-to-overlay.
- [ ] **Task 8:** Build S3 upload handler (pre-signed URL from backend, chunked upload with resume).
- [ ] **Task 9:** Build CMF pipeline trigger: `POST /studio/complete` with mode→template mapping.
- [ ] **Task 10:** Extract TribeNest streaming core into `ccp-stream-service` Docker container.
- [ ] **Task 11:** Build WebSocket→RTMP muxer + parallel S3 VOD archive in ccp-stream-service.
- [ ] **Task 12:** Build `Diego` agent persona YAML (Studio Session Conductor) in the Production Department.
- [ ] **Task 13:** Add `studio_sessions` table migration to Supabase.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Plugin Registration):** Type `/studio` in an AFFiNE page. Assert Studio Block renders with preview + controls + teleprompter panels.
- [ ] **AC2 (Webcam Recording):** Select YouTube mode, 1080p. Start recording. Assert MediaRecorder produces a valid video blob with 1920×1080 resolution.
- [ ] **AC3 (Shorts Aspect Ratio):** Select Shorts mode. Assert canvas is 1080×1920 (9:16). Assert 720p option is disabled (1080p mandatory).
- [ ] **AC4 (Teleprompter Scroll):** Load a page with 500 words. Start teleprompter at 2.5 w/s. Assert text scrolls completely in ~200 seconds (±10%).
- [ ] **AC5 (Asset Overlay):** Open a page with 3 images. Click an image in the asset panel. Assert it appears on the recording canvas overlay. Click again. Assert it disappears.
- [ ] **AC6 (S3 Upload):** Stop a recording. Assert blob is uploaded to S3. Assert `studio_sessions` row exists with `status = 'uploading'` then `'processing'`.
- [ ] **AC7 (CMF Trigger):** Stop a YouTube-mode recording. Assert CMF pipeline receives a job with `template = 'youtube_longform'`.
- [ ] **AC8 (Streaming):** Select Webinar mode. Start stream with YouTube Live RTMP URL. Assert ccp-stream-service receives chunks. Assert YouTube Live dashboard shows incoming stream.
- [ ] **AC9 (Crash Recovery):** Kill browser tab during a 2-minute recording. Assert at least 60 seconds of video is recoverable from S3 chunk saves.
- [ ] **AC10 (Receipt Chain):** Complete a recording. Assert receipt is written to Receipt Chain Guard with correct `session_id` and `s3_recording_url`.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| AFFiNE self-hosted instance | Infrastructure | BlockSuite plugin API must be accessible for custom block registration. |
| AFFiNE fork repository | Code | Studio Block lives in `ccp-blocks/studio-block/` — requires fork to be set up. |
| TribeNest streaming module | Code | Source for ccp-stream-service extraction. |
| AWS EC2/ECS | Infrastructure | For deploying ccp-stream-service Docker container. |
| S3 bucket | Infrastructure | For recording storage. Bucket: `ccp-recordings`. |
| CCP FastAPI backend | Internal | For pre-signed URL generation and CMF pipeline trigger. |
| CMF Pipeline | Internal (existing) | Receives recording mode + S3 URL for editorial processing. |
| Receipt Chain Guard (DEP-ENG-041) | Internal | Receipt written on upload completion. |

---

## 10. Testing Strategy

### Unit Tests
- **Canvas Compositing:** Mock 2 video streams (webcam + screen). Assert canvas draws both at correct positions for each mode (16:9, 9:16).
- **Mode→Template Mapping:** Assert each recording mode maps to the correct CMF pipeline template.
- **Teleprompter Speed:** Assert scroll velocity matches words-per-second setting (±5%).

### Integration Tests
- **Full Recording Flow:** Start recording in YouTube mode → record 10 seconds → stop → assert S3 upload → assert CMF trigger → assert `studio_sessions` row with `status = 'complete'`.
- **Full Streaming Flow:** Start stream → send 10 seconds of chunks → stop → assert RTMP output received by mock RTMP server → assert VOD file in S3.

### Browser Compatibility Tests
- **Chrome 120+:** Assert 1080p recording at 30fps with H.264 codec.
- **Firefox 120+:** Assert recording with VP9 codec (Firefox may not support H.264 in MediaRecorder).
- **Edge:** Assert parity with Chrome (Chromium-based).
