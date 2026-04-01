# Feature Brief: Full Stack Recording / Streaming Studio

*Feature ID: FB-STUDIO-03*  
*Parent MCDA: MCDA IV §III, §IV*  
*Date: 2026-03-25*  
*Status: Brainstorm → Pending Spec*  
*Replaces: FR-CA11-13 (OBS Recording Controller), FR-CA11-14 (Excalidraw OBS Overlay)*

---

## 1. Problem Statement

The current CA11 architecture depends on OBS Studio as an external desktop application for all recording and streaming workflows. This creates three structural problems:

1. **Context switching:** The coach must leave AFFiNE, open OBS, configure scenes, manage WebSocket connections, and manually trigger post-production pipelines.
2. **No intelligence integration:** OBS has zero awareness of the CCP data layer — it doesn't know which script the coach is recording, what visual assets are assigned, which client group the content targets, or what CMF editorial template should process the recording.
3. **Local dependency:** OBS runs on the coach's machine. If their laptop dies, their entire recording setup is lost. No cloud-native workflow exists.

---

## 2. Solution Overview

Build the **CCP Studio Block** — a native BlockSuite plugin within the AFFiNE clone that provides integrated recording, streaming, teleprompter, and asset management capabilities directly inside the coaching workspace. The Studio eliminates OBS as a required dependency and connects recording to the CCP intelligence layer natively.

---

## 3. Core Components

### 3.1 AFFiNE Studio Block (Frontend — React/BlockSuite Plugin)

**Location:** `ccp-blocks/studio-block/` in the AFFiNE fork repository.

**Activation:** Coach types `/studio` in any AFFiNE page, or clicks the Studio icon in the page toolbar.

**UI Layout:**

```
┌───────────────────────────────────────────────────────────────────────────┐
│  CCP STUDIO                                                 [X Close]    │
├──────────────────────────┬────────────────────────────────────────────────┤
│                          │  📝 SCRIPT / TELEPROMPTER                      │
│   🎥 PREVIEW             │  ─────────────────────────────────────────     │
│                          │  [Auto-scrolling text from current AFFiNE     │
│   ┌─────────────────┐   │   page or selected script page]                │
│   │                 │   │                                                │
│   │   Webcam Feed   │   │  Speed: [▬▬▬▬░░░░░] 2.5 w/s                   │
│   │   (+ guest PiP  │   │  Font: [24px ▼]  Mirror: [Off ▼]              │
│   │    if active)    │   │                                                │
│   │                 │   │  ─────────────────────────────────────────     │
│   └─────────────────┘   │  📎 VISUAL ASSETS                              │
│                          │  ┌──────┐ ┌──────┐ ┌──────┐                  │
│   Mode: [YouTube ▼]     │  │ Img1 │ │ Img2 │ │ Exc1 │                  │
│   Quality: [1080p ▼]    │  └──────┘ └──────┘ └──────┘                  │
│                          │                                                │
│   ⏺ REC   ⏸ PAUSE      │  🖼 THUMBNAIL PREVIEW                          │
│   ⏱ 00:00:00            │  ┌──────────────┐                             │
│                          │  │ [Thumbnail]  │  [Edit in Canva →]          │
│   🔴 STREAM [Off ▼]     │  └──────────────┘                             │
│   Destinations:          │                                                │
│   ☑ YouTube Live         │  ─────────────────────────────────────────     │
│   ☐ Facebook Live        │  🔊 SOUNDBOARD                                │
│   ☐ Custom RTMP          │  [🥁 SFX1] [😂 SFX2] [👏 SFX3]               │
│                          │  [😱 SFX4] [🔔 SFX5]                          │
│   👥 GUEST               │  ─────────────────                            │
│   [Invite Guest →]       │  🎵 [▶ Intro] [▶ Outro]                      │
│   Status: No guest       │  [▶ Celebration] [▶ Sad/Dramatic]             │
│                          │  [⚙ Customize Audio →]                        │
└──────────────────────────┴────────────────────────────────────────────────┘
```

### 3.2 Recording Engine

**Technology:** Browser `MediaRecorder` API via WebRTC.

| API | Purpose | Specification |
|---|---|---|
| `navigator.mediaDevices.getUserMedia()` | Webcam + microphone capture | Video: H.264, 1080p30 or 720p30 |
| `navigator.mediaDevices.getDisplayMedia()` | Screen/slide capture (for YouTube/Course modes) | Same codec, composited with webcam via `<canvas>` |
| `MediaRecorder` | Encodes the composited stream | Output: WebM (VP8/VP9) or MP4 (H.264) |
| `canvas.captureStream()` | Composites webcam + screen + overlay into single stream | 30fps target |

**Quality tiers:**

| Mode | Resolution | Bitrate | Rationale |
|---|---|---|---|
| Shorts / Vertical | 1080×1920 (9:16) | 8 Mbps | **Mandatory 1080p** — mobile screens expose quality issues |
| YouTube Long-Form | 1920×1080 (16:9) | 5-8 Mbps | Selectable 1080p/720p — AWS cost consideration |
| Webinar / Stream | 1920×1080 (16:9) | 4-6 Mbps | Selectable — streaming bandwidth constraint |
| Course Video | 1920×1080 (16:9) | 5-8 Mbps | Selectable — matches YouTube long-form |
| Loom-Style Quick | 1280×720 (16:9) | 3 Mbps | 720p sufficient for quick messages |

**Output handling:** On "Stop Recording," the Studio Block takes the recorded video Blob, generates a pre-signed S3 upload URL via the CCP FastAPI backend (`POST /studio/upload-url`), and uploads directly from the browser. No intermediate local storage.

### 3.3 Teleprompter Component

**Implementation:** React component within the Studio Block. ~200 lines of TypeScript.

**Features:**

| Feature | Implementation |
|---|---|
| Text source | Current AFFiNE page content (default) OR selected page via `/teleprompter [page-link]` |
| Auto-scroll | CSS `animation: scroll linear` with adjustable `animation-duration` |
| Speed control | Slider mapping to words-per-second (range: 1.0 – 5.0 w/s) |
| Font size | Dropdown: 18px, 24px, 32px, 48px |
| Mirror mode | CSS `transform: scaleX(-1)` for physical teleprompter glass |
| Script selection | Schedule-aware: surfaces scripts from current week's batch in priority order |
| Pause/Resume | Click to pause scroll, click again to resume |

### 3.4 Streaming Engine (Backend — TribeNest Extraction)

**Source:** Extracted from `github.com/Remjohn/tribenest` streaming module.

**Deployment:** Standalone Docker container (`ccp-stream-service`) on AWS EC2/ECS.

**Architecture:**

```
AFFiNE Studio Block (browser)
    ↓ WebSocket (MediaRecorder chunks)
ccp-stream-service (Node.js/Express)
    ├─→ RTMP Mux → YouTube Live
    ├─→ RTMP Mux → Facebook Live
    ├─→ RTMP Mux → Custom RTMP endpoint
    └─→ S3 parallel recording (VOD archive)
```

**Protocol:** The browser sends `MediaRecorder` data chunks via WebSocket to `ccp-stream-service`. The service repackages the incoming WebM/H264 stream into RTMP and pushes to configured destinations. Simultaneously, it writes the raw stream to S3 for VOD archival.

**Stream health:** The service pushes metrics back to the Studio Block UI via the same WebSocket: bitrate, frame drops, connection status per destination, viewer count (where available via platform API).

### 3.5 Asset Panel

**Purpose:** Display visual assets assigned to the current script for easy reference during recording.

**Data source:** The AFFiNE page's attached media (images, Excalidraw embed blocks, CVE Canva compositions). The Studio Block reads the page's block tree and surfaces all media elements in the asset panel.

**Interaction:** Coach can click an asset to display it full-screen over the recording canvas (for screen recording modes). This replaces OBS scene switching — instead of switching between "webcam" and "slides" scenes, the coach clicks an asset and it appears in the recording.

### 3.6 Thumbnail Preview

**Source:** Thumbnail is already present in the AFFiNE content page (generated by CVE Canva Clone pipeline).

**Display:** Static preview image shown in the Studio Block for visual content identification.

**Action:** "Edit in Canva" deep link opens the CVE Canva Clone editor for the associated thumbnail template.

### 3.7 Live Soundboard

The Studio includes a **live soundboard** — clickable audio buttons that the coach triggers during recording or streaming to create atmosphere, energy shifts, and entertainment moments.

#### 5 Programmable SFX Slots

The coach has **5 programmable quick-fire sound effect buttons** visible in the Studio UI at all times:

| Slot | Default Sound | Use Case | Duration |
|---|---|---|---|
| SFX 1 | 🥁 Drumroll | Before trivia reveals, building suspense | 2-4s |
| SFX 2 | 😂 Comedy horn ("wah wah wah") | When someone gets an answer hilariously wrong | 1-2s |
| SFX 3 | 👏 Applause | After correct answers, after commitments, after guest insights | 3-5s |
| SFX 4 | 😱 Record scratch / gasp | Surprising reveals, plot twists in content | 1-2s |
| SFX 5 | 🔔 Ding / level-up chime | New round start, score milestones, achievement unlocks | 1s |

**Each slot is fully customizable:** The coach clicks "⚙ Customize Audio" to open the Sound Library panel, where they can:
- Browse from a **pre-loaded SFX library** (50+ royalty-free effects stored in S3: `s3://ccp-assets/studio/sfx/`)
- Upload their own sound effects (MP3/WAV, max 10 seconds)
- Preview before assigning
- Drag and drop onto any of the 5 slots
- Saved per coach profile in `studio_preferences` table

#### Music Buttons (4 Programmable Tracks)

In addition to SFX, the Studio has **4 music buttons** for longer audio tracks:

| Button | Purpose | Default Track | Duration |
|---|---|---|---|
| 🎵 **Intro** | Played at stream start / video intro | Upbeat, branded jingle | 10-30s |
| 🎵 **Outro** | Played at stream end / video outro | Warm, closing melody | 10-30s |
| 🎉 **Celebration** | Winner reveal, milestone moments, achievements | Triumphant fanfare + confetti trigger | 5-15s |
| 😢 **Sad/Dramatic** | Exaggerated comedic sympathy when someone fails | Over-the-top dramatic violin/piano | 5-10s |

**Music behavior:**
- Tracks play **over the stream audio** (mixed into the canvas audio track via Web Audio API `GainNode`)
- Coach can adjust music volume independently of voice via a mini-slider on each button
- Tracks fade in/out automatically (500ms linear fade) to avoid abrupt cuts
- Only one track plays at a time — clicking a new track stops the current one
- "Stop" button kills all audio immediately

**Customization flow:**
1. Coach clicks "⚙ Customize Audio" in the soundboard panel
2. Studio Music Library opens — showing categorized tracks:
   - Intro themes (10 options)
   - Outro themes (10 options)
   - Celebration tracks (10 options)
   - Dramatic/comedic tracks (10 options)
3. Coach previews, selects, and saves
4. Saved in `studio_preferences.audio_config` (JSONB)
5. Custom uploads stored in S3: `s3://ccp-assets/studio/music/{coach_id}/`

**Audio mixing (technical):**
```
Coach microphone → AudioContext.createMediaStreamSource()
                         ↓
                    GainNode (voice volume)
                         ↓
SFX/Music file → AudioContext.createBufferSource()
                         ↓
                    GainNode (music volume)
                         ↓
            AudioContext.destination → merged into MediaRecorder/WebSocket stream
```

### 3.8 Guest Join (Testimonials, Interviews, Co-Coaching)

The Studio supports **at least 1 remote guest** joining the recording or stream. This is critical for:
- **Testimonial videos:** Client shares their transformation story live
- **Interview recordings:** Coach interviews an expert or another coach
- **Co-coaching sessions:** Two coaches stream together to a shared community
- **Hot seat coaching:** Client joins live for a mini coaching demonstration

#### Architecture

**Technology:** WebRTC peer-to-peer connection (same API used by Google Meet, Zoom).

```
Coach's browser (WebRTC Peer A)
    ↕ signaling via WebSocket (ccp-stream-service)
Guest's browser (WebRTC Peer B)
    ↓
Coach's canvas composites both feeds:
    ┌─────────────────────────────────┐
    │                       ┌───────┐ │
    │   Coach (main)        │ Guest │ │  ← Picture-in-Picture mode
    │                       │ (PiP) │ │
    │                       └───────┘ │
    └─────────────────────────────────┘
         OR
    ┌────────────────┬────────────────┐
    │                │                │
    │    Coach       │     Guest      │  ← Side-by-Side mode
    │                │                │
    └────────────────┴────────────────┘
```

**Guest join flow:**
1. Coach clicks "Invite Guest →" in the Studio UI
2. System generates a unique, time-limited guest link: `https://studio.conscious.coach/join/{session_token}`
3. Coach shares the link (via Telegram DM, email, or clipboard)
4. Guest opens the link → browser requests webcam/mic permission → WebRTC connection established
5. Guest's video appears in the Studio preview as a PiP overlay (default) or side-by-side (toggle)
6. Coach can switch layout during recording/stream
7. Guest audio is mixed into the stream via Web Audio API (same as soundboard mixing)
8. On disconnect, the guest feed gracefully fades out

**Guest controls (coach-side):**
- Mute guest audio (emergency mute)
- Resize/reposition guest video overlay
- Switch between PiP and Side-by-Side layout
- Disconnect guest

**Guest controls (guest-side):**
- Mute own microphone
- Toggle own camera
- Leave session

**Limitations:**
- MVP: 1 guest maximum (2-person call). Multi-guest (3+) is a post-MVP enhancement.
- Guest must use a modern browser (Chrome, Firefox, Edge) with WebRTC support.
- Guest's video quality matches the stream quality setting (1080p or 720p).
- Guest link expires after 24 hours or after the session ends.

---

## 4. The 5 Recording Modes — Pipeline Integration

Each mode determines the full post-production chain:

### Mode 1: YouTube Long-Form (6-8 min)

```
Record (webcam + screen/assets) → S3 upload
    → CMF Pipeline (editorial template: youtube_longform)
    → FFmpeg: intro/outro, captions, music bed
    → Remotion: branded overlays, transition effects
    → Output: edited .mp4 → AFFiNE Content Library
    → Scheduler: queued for YouTube upload at optimal time
    → Performance tracking: 6h collection cycle begins
```

### Mode 2: Shorts / Vertical (< 60s)

```
Record (webcam only, 9:16) → S3 upload
    → CMF Pipeline (editorial template: short_form_vertical)
    → FFmpeg: auto-captions (burnt-in), dynamic zoom
    → Output: vertical .mp4 → AFFiNE Content Library
    → Scheduler: queued for Instagram Reels + TikTok + YouTube Shorts
```

### Mode 3: Webinar / Live Stream

```
Stream (webcam + presentation assets + RTMP out) → parallel S3 recording
    → Interactive Trivianar Engine active during stream
    → Post-stream: Session Recap pipeline (FR-CA11-05)
    → Whisper STT → Lena extracts Session Intelligence Report
    → AFFiNE Session Archive + Telegram recap delivery
    → VOD → CMF Pipeline (webinar_vod template) → content multiplication
```

### Mode 4: Course Video

```
Record (webcam + Excalidraw diagrams + presentation) → S3 upload
    → CMF Pipeline (editorial template: course_video)
    → FFmpeg: chapter markers, branded intro/outro, caption overlay
    → Learning Path Agent (Gabrielle) categorizes → learning_path_registry
    → Output: course chapter .mp4 → client AFFiNE workspace (gated by program tag)
    → Drip schedule: Telegram drip per Atlas roadmap cadence
```

### Mode 5: Loom-Style Quick

```
Record (webcam bubble + screen) → S3 upload
    → Whisper STT transcription only (no CMF editorial)
    → Output: raw .webm + transcript → AFFiNE page attachment
    → Shareable link generated
```

---

## 5. CCP Integration Points

| System | Integration | Direction |
|---|---|---|
| **AFFiNE BlockSuite** | Studio Block plugin registered as custom block type | Native |
| **CMF Pipeline** | Recording mode selects editorial template | Studio → CMF |
| **TribeNest Streaming** | WebSocket stream relay + RTMP restreaming | Studio → TribeNest |
| **Trivianar Engine** | Stream session context enables trivia activation | Studio → Trivianar |
| **AFFiNE Sync Service** | Completed recordings pushed to appropriate workspace sections | CMF → AFFiNE |
| **Receipt Chain** | `DEP-ENG-041` receipt on upload completion | Bidirectional |
| **Learning Path Agent** | Course videos auto-categorized and placed in learning journeys | CMF → Gabrielle |
| **Atlas (FR32)** | Course video drip schedule respects 4+1+2 cadence | Gabrielle → Atlas |
| **Session Intelligence** | Webinar/stream recordings processed for Session Recap | Studio → Lena |
| **Social Scheduler** | Post-edited content queued for social media publishing | CMF → Scheduler |

---

## 6. Data Model

### New Tables

```sql
-- Studio recording sessions
CREATE TABLE studio_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    coach_id UUID NOT NULL REFERENCES coaches(id),
    source_page_id VARCHAR(255), -- AFFiNE page that was being recorded
    recording_mode VARCHAR(30) NOT NULL, -- youtube, shorts, webinar, course, loom
    aspect_ratio VARCHAR(5) NOT NULL, -- 16:9 or 9:16
    resolution VARCHAR(10) NOT NULL, -- 1080p or 720p
    s3_recording_url TEXT,
    s3_vod_url TEXT, -- for streams, the archived VOD
    duration_seconds INTEGER,
    is_stream BOOLEAN DEFAULT FALSE,
    stream_destinations JSONB, -- [{platform, rtmp_url, status}]
    cmf_pipeline_template VARCHAR(50), -- which CMF editorial template was triggered
    cmf_job_id UUID, -- FK to CMF pipeline execution
    receipt_chain_id UUID REFERENCES receipt_chain(id),
    status VARCHAR(20) DEFAULT 'recording', -- recording, uploading, processing, complete, failed
    started_at TIMESTAMP WITH TIME ZONE NOT NULL,
    ended_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Studio audio preferences (soundboard + music config per coach)
CREATE TABLE studio_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    coach_id UUID NOT NULL UNIQUE REFERENCES coaches(id),
    sfx_slots JSONB DEFAULT '[]', -- [{slot: 1, label: "Drumroll", s3_url: "...", volume: 0.8}]
    music_tracks JSONB DEFAULT '{}', -- {intro: {s3_url, volume, fade_ms}, outro: {...}, celebration: {...}, sad: {...}}
    guest_layout VARCHAR(20) DEFAULT 'pip', -- pip or side_by_side
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Guest join sessions
CREATE TABLE studio_guest_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES studio_sessions(id),
    guest_name VARCHAR(255),
    guest_email VARCHAR(255),
    join_token VARCHAR(64) NOT NULL UNIQUE,
    token_expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    layout_mode VARCHAR(20) DEFAULT 'pip', -- pip or side_by_side
    joined_at TIMESTAMP WITH TIME ZONE,
    left_at TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) DEFAULT 'invited', -- invited, connected, disconnected
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Stream viewer analytics (for webinar mode)
CREATE TABLE stream_analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES studio_sessions(id),
    peak_viewers INTEGER DEFAULT 0,
    total_unique_viewers INTEGER DEFAULT 0,
    avg_watch_duration_seconds INTEGER DEFAULT 0,
    trivia_participation_rate DECIMAL(5,4), -- participants / viewers
    telegram_messages_count INTEGER DEFAULT 0,
    commitment_responses_count INTEGER DEFAULT 0,
    leads_captured INTEGER DEFAULT 0,
    collected_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 7. Technical Specifications

| Aspect | Specification |
|---|---|
| **Frontend** | React + TypeScript, BlockSuite plugin API |
| **Webcam/Screen** | WebRTC (getUserMedia + getDisplayMedia) |
| **Encoding** | MediaRecorder API (VP9/H264), canvas compositing at 30fps |
| **Upload** | Pre-signed S3 URL, chunked upload with resume |
| **Streaming Service** | Node.js/Express (extracted from TribeNest), RTMP mux |
| **Stream Protocol** | WebSocket (browser → service) → RTMP (service → destinations) |
| **Deployment** | Docker container on AWS EC2/ECS |
| **Teleprompter** | React component, CSS scroll animation, ~200 lines |
| **Latency** | < 3s glass-to-glass for RTMP streaming |
| **Max resolution** | 1080p30 (browser MediaRecorder limit) |
| **Soundboard** | Web Audio API (AudioContext, GainNode, BufferSource) |
| **Audio mixing** | Voice + SFX + Music merged via AudioContext.destination |
| **Guest join** | WebRTC peer-to-peer, signaling via ccp-stream-service WebSocket |
| **Guest capacity** | 1 guest (MVP), expandable to 3+ post-MVP |
| **Audio library** | S3: `s3://ccp-assets/studio/sfx/` and `s3://ccp-assets/studio/music/` |

---

## 8. OBS Retirement Path

| Phase | Action | Duration |
|---|---|---|
| 1 | Deploy Studio Block in AFFiNE staging | 1 week |
| 2 | Test all 5 recording modes with sample scripts | 1 week |
| 3 | Deploy TribeNest streaming service | 3 days |
| 4 | Test streaming to YouTube Live + Telegram link | 3 days |
| 5 | Parallel run: OBS + Studio available simultaneously | 2 weeks |
| 6 | Retire `obs_controller.py`, update `PROMPT_Spec_Build.md` | 1 day |

**OBS remains available** as optional fallback for coaches who want advanced scenes/transitions. But it is no longer architecturally required — `ADR-06` (OBS WebSocket) is superseded by `ADR-07` (Native CCP Studio).

---

## 9. Success Criteria

| Criterion | Target | Measurement |
|---|---|---|
| OBS retirement | 100% of new recordings via Studio Block within 30 days of launch | `studio_sessions` count vs. `obs_controller` call count |
| Recording quality | ≥95% of recordings pass CMF quality gate on first attempt | CMF pipeline rejection rate |
| Streaming reliability | ≥99% uptime for TribeNest streaming service | CloudWatch metrics |
| Post-production latency | CMF pipeline completes within 15 minutes of upload | `studio_sessions.status` transition timestamps |
| Coach adoption | ≥3 recordings per coach per week within 60 days | `studio_sessions` frequency analysis |

---

## 10. Risks

| Risk | Mitigation |
|---|---|
| Browser MediaRecorder quality ceiling | Start with browser-quality; evaluate Electron native capture wrapper if 1080p is insufficient |
| WebSocket streaming latency | Deploy TribeNest service in same AWS region as AFFiNE; target < 3s glass-to-glass |
| Browser tab crash during long recording | Implement periodic chunk saves to S3 (every 30s) for recovery |
| TribeNest extraction complexity | The streaming module is relatively self-contained within the monorepo; estimate 2-3 days extraction |
| Guest WebRTC NAT traversal | Use TURN server (coturn on AWS) for guests behind restrictive firewalls; STUN handles most cases |
| Audio sync drift | Web Audio API timestamp synchronization; 500ms fade transitions mask minor drift |
| SFX/Music copyright | Pre-loaded library uses royalty-free assets only; coach uploads are their responsibility |

---

*End of Feature Brief FB-STUDIO-03.*
