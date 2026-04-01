# Tech-Spec: FR-CA11-13 — OBS Recording Pipeline Controller

> ⚠️ **RETIRED — 2026-03-25**
> This spec has been superseded by **FR-CA11-16 (CCP Studio Block — Full Stack Recording & Streaming)**. The OBS WebSocket integration (ADR-06) is retired per **ADR-07 (Native CCP Studio Block)**. OBS remains available as an optional fallback for power users but is no longer architecturally required. The `obs_controller.py` tool is **DEPRECATED**.
>
> **Replacement Spec:** `FR-CA11-16_CCP_Studio_Block_Tech_Spec.md`
> **Decision Record:** MCDA IV (CCP Studio Integration Analysis, score: 442 vs 225 baseline)

**Created:** 2026-03-24
**Status:** ~~Ready for Development~~ **RETIRED**
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / PRD Update v2.0 — Capability Area 11)
**Architecture Reference:** ~~PRD-Update-CA11 §4.5, ADR-06~~ → ADR-06 RETIRED, see ADR-07
**Skill Implementation:** ~~`tools/obs_controller.py`~~ → **DEPRECATED**
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd-update-CA11-quad-platform.md`

---

## 2. Overview

### Problem Statement
OBS Studio is the industry-standard open-source recording and streaming tool used by coaches for live sessions, webinars, and content recording. But it requires manual operation — the coach must sit at their computer to start/stop recording, switch scenes, and manage overlays. This creates friction: during a coaching session, the coach's attention should be on the client, not on navigating OBS UI elements.

### Solution
FR-CA11-13 implements `obs_controller.py` — a Python tool that communicates with OBS Studio's WebSocket API (v5) to provide programmatic control over recording. Telegram bot commands (`/record-start`, `/record-stop`, `/scene [name]`) give the coach remote control from their phone. Post-recording, the controller triggers the Session Intelligence pipeline (FR-CA11-05) by uploading the recording to S3. The tool integrates with the Pi Extensions framework (`DamageControl` for connection failures, `TillDone` for pipeline completion).

### Scope
**In scope:**
- OBS WebSocket API v5 client implementation.
- Recording control: start, stop, status.
- Scene switching.
- Browser source injection (for Excalidraw overlays, FR-CA11-14).
- Telegram bot command handlers (`/record-start`, `/record-stop`, `/scene`).
- Post-recording S3 upload and pipeline trigger.

**Out of scope:**
- OBS installation and configuration (coach responsibility + setup documentation).
- Session Intelligence extraction (FR-CA11-05).
- Content machine pipeline (FR-CA11-08).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| OBS Studio WebSocket API v5 | External API | TARGET — OBS exposes WebSocket server (native since OBS v28+). |
| FR-CA11-05 (Session Recap) | Session Intelligence Pipeline | CONSUMER — Triggered post-recording. |
| `DamageControl` (Pi Extension) | Error Recovery | INTEGRATION — Handles WebSocket connection failures. |
| `TillDone` (Pi Extension) | Completion Enforcement | INTEGRATION — Ensures post-recording pipeline completes. |

### Academic Grounding

| Framework | Author | Year | Mechanism |
|---|---|---|---|
| **Reduced Cognitive Load** | Sweller | 1988 | Removing OBS UI interaction from the coaching session reduces extraneous cognitive load, letting the coach allocate all working memory to the client. |

### Technical Decisions
1. **WebSocket over REST:** OBS v28+ ships with a native WebSocket server (port 4455 by default). No plugin installation required. WebSocket provides: bi-directional communication (receive events like recording-stopped), low latency (<50ms local), and persistent connection.
2. **obs-websocket-js Protocol:** Using the `obs-websocket-js` protocol specification (open standard) implemented in Python via `websockets` library. The protocol handles authentication (SHA-256 challenge-response), request/response correlation, and event subscription.
3. **S3 Upload Post-Recording:** When recording stops, OBS writes the file to a local directory. `obs_controller.py` monitors the recording output directory (configured per coach). Upon detecting a new recording file, it uploads to S3 and fires the Session Intelligence pipeline. This avoids the need for real-time streaming to S3.

---

## 4. Implementation Plan

### Stage 1: WebSocket Client
*Agent:* System Operator
*Inputs:* OBS WebSocket API v5 specification.
*Outputs:* `obs_controller.py` with core methods.

**Steps:**
1. Implement `OBSController` class with methods:
   - `connect(host, port, password)` → WebSocket connection with SHA-256 auth.
   - `start_recording()` → sends `StartRecord` request.
   - `stop_recording()` → sends `StopRecord` request. Returns recording file path.
   - `get_recording_status()` → sends `GetRecordStatus` request. Returns recording state + duration.
   - `switch_scene(scene_name)` → sends `SetCurrentProgramScene` request.
   - `set_browser_source(source_name, url)` → sends `SetInputSettings` request to update browser source URL.
   - `disconnect()` → clean WebSocket close.
2. Implement event listener for `RecordStateChanged` events.
3. Implement connection resilience: auto-reconnect on WebSocket drop (5 attempts, exponential backoff).

### Stage 2: Telegram Bot Commands
*Agent:* CBCS Bot Handler
*Inputs:* Coach Telegram commands.
*Outputs:* OBS actions + confirmation messages.

**Steps:**
1. Register Telegram bot commands:
   - `/record-start` → calls `start_recording()`. Responds with "Recording started ⏺️".
   - `/record-stop` → calls `stop_recording()`. Responds with "Recording stopped. Processing session recap... ⏱️".
   - `/scene [name]` → calls `switch_scene(name)`. Responds with "Switched to [name] 🎬".
   - `/record-status` → calls `get_recording_status()`. Responds with current state + duration.
2. Commands require coach authentication (validated against `coach_config` Telegram user ID).

### Stage 3: Post-Recording Pipeline Trigger
*Agent:* `obs_controller.py` / `TillDone`
*Inputs:* Recording file from OBS output directory.
*Outputs:* S3 upload + Session Intelligence pipeline trigger.

**Steps:**
1. On `RecordStateChanged` → `OBS_WEBSOCKET_OUTPUT_STOPPED` event:
   - Read the recording file path from the event payload.
   - Upload to S3: `s3://{coach_acronym}/sessions/{session_id}.mp4`.
   - Create `session_intelligence` record in Supabase (status: `PENDING_TRANSCRIPTION`).
   - Write Receipt Chain Guard entry per FR47 DEP-ENG-041 schema after saving the `session_intelligence` record.
   - Fire FR-CA11-05 pipeline trigger.
2. `TillDone` monitors the Session Intelligence pipeline to ensure it completes within 10 minutes.
3. `DamageControl` handles: S3 upload failure (retry), pipeline trigger failure (retry + operator alert).

---

## 5. Primary Output Schema

**Data Object:** Recording Status Payload (`DEP-ENG-083` PROPOSED)

```json
{
  "recording_id": "uuid-recording-001",
  "coach_id": "uuid-coach-001",
  "session_id": "uuid-session-001",
  "recording_file": "s3://JP/sessions/uuid-session-001.mp4",
  "recording_duration_seconds": 3600,
  "obs_scenes_used": ["Main Camera", "Whiteboard", "Screen Share"],
  "recording_started_at": "2026-03-24T14:00:00Z",
  "recording_stopped_at": "2026-03-24T15:00:00Z",
  "pipeline_triggered": true,
  "pipeline_status": "PENDING_TRANSCRIPTION"
}
```

---

## 6. Backward Compatibility Fallback
OBS integration is entirely optional — coaches who don't use OBS lose zero functionality. All other CA11 features (AFFiNE workspace, learning paths, voice-to-lesson, accountability) operate independently. If the OBS WebSocket connection fails, the coach is notified via Telegram: "Could not connect to OBS. Please check that OBS is running and WebSocket is enabled."

---

## 7. Tasks

- [ ] **Task 1:** Write `obs_controller.py` with `OBSController` class and all core methods.
- [ ] **Task 2:** Implement WebSocket SHA-256 authentication per obs-websocket-js protocol.
- [ ] **Task 3:** Implement auto-reconnect with exponential backoff.
- [ ] **Task 4:** Add `/record-start`, `/record-stop`, `/scene`, `/record-status` Telegram bot commands.
- [ ] **Task 5:** Implement post-recording S3 upload and FR-CA11-05 pipeline trigger.
- [ ] **Task 6:** Wire `DamageControl` for S3 upload failures and `TillDone` for pipeline completion.
- [ ] **Task 7:** Write coach setup guide (enable OBS WebSocket, configure output directory, set password).

---

## 8. Acceptance Criteria

- [ ] **AC1 (Start Recording):** Send `/record-start` via Telegram. Assert OBS starts recording within 2 seconds. Assert Telegram confirmation received.
- [ ] **AC2 (Stop Recording):** Send `/record-stop`. Assert OBS stops recording. Assert recording file is uploaded to S3 within 60 seconds.
- [ ] **AC3 (Scene Switch):** Send `/scene Whiteboard`. Assert OBS switches to the Whiteboard scene. Assert Telegram confirmation received.
- [ ] **AC4 (Pipeline Trigger):** After recording stops, assert `session_intelligence` Supabase record is created and FR-CA11-05 pipeline is triggered.
- [ ] **AC5 (Connection Failure):** Disconnect OBS. Send `/record-start`. Assert Telegram error message: "Could not connect to OBS."
- [ ] **AC6 (Reconnection):** Disconnect and reconnect OBS. Assert controller automatically reconnects within 30 seconds.
- [ ] **AC7 (Authentication):** Non-coach Telegram user sends `/record-start`. Assert command is rejected.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| OBS Studio v28+ | External | Must be running on coach's machine with WebSocket enabled. |
| AWS S3 | Infrastructure | Recording file storage. |
| FR-CA11-05 (Session Recap) | Internal | Triggered post-recording. |
| `DamageControl` (Pi Extension) | Internal | Error recovery. |
| `TillDone` (Pi Extension) | Internal | Pipeline completion enforcement. |

---

## 10. Testing Strategy

### Unit Tests
- **WebSocket Protocol:** Mock OBS WebSocket server. Send `StartRecord`. Assert correct message format and auth handshake.
- **S3 Upload:** Mock S3. Assert file is uploaded with correct key and content type.

### Integration Tests
- **Full Lifecycle:** Start recording → wait 30s → stop recording → assert S3 upload → assert `session_intelligence` record → assert FR-CA11-05 trigger fires.

### Network Resilience Tests
- **WebSocket Drop:** Simulate WebSocket connection drop mid-recording. Assert auto-reconnect and recording state is maintained.
- **S3 Timeout:** Block S3. Assert retry with exponential backoff (3 attempts). Assert operator alert after 3 failures.
