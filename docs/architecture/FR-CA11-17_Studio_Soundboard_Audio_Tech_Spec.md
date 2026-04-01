# Tech-Spec: FR-CA11-17 — Studio Soundboard & Programmable Audio

**Created:** 2026-03-25
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / PRD Update v2.0 — Capability Area 11)
**Architecture Reference:** PRD-Update-CA11 §4.5 (FR-CA11-17), ADR-07
**Skill Implementation:** `ccp-blocks/studio-block/components/Soundboard.tsx`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd-update-CA11-quad-platform.md` (§4.5 FR-CA11-17)
- `d:\Work\The Conscious Coaching Factory\docs\features\FB_Full_Stack_Recording_Streaming.md` (§3.7)

---

## 2. Overview

### Problem Statement
Recording and streaming sessions lack atmosphere. Without sound effects, intros, victory music, or comedic audio cues, live streams feel flat and fail to create the emotional peaks and valleys that drive engagement and memorability. Coaches currently have no way to trigger audio reactions during recordings or streams.

### Solution
FR-CA11-17 adds a **live soundboard** to the CCP Studio Block with 5 programmable SFX buttons and 4 programmable music buttons. All audio is mixed via the Web Audio API into the recording/stream output. Coaches customize their sounds from an S3-hosted library or upload their own. Settings persist per coach profile.

### Scope
**In scope:**
- 5 programmable SFX slots with default sounds and customization.
- 4 music buttons (intro, outro, celebration, sad/dramatic).
- Web Audio API mixing pipeline (voice + SFX + music).
- S3 audio library browsing and selection.
- Coach audio upload (MP3/WAV, max 10 seconds for SFX, max 60 seconds for music).
- `studio_preferences` table for per-coach persistence.
- Volume control per slot, fade in/out transitions.

**Out of scope:**
- Recording/streaming engine (FR-CA11-16).
- Custom music generation (future enhancement).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-070` | Soundboard Component | UI — React component with SFX + music buttons. |
| `DEP-ENG-071` | Audio Mixer Pipeline | CORE — Web Audio API graph: mic → GainNode + SFX/Music → GainNode → destination. |
| `DEP-ENG-072` | Audio Library Browser | UI — S3 bucket browser for selecting sounds from the pre-loaded library. |
| `DEP-ENG-073` | Audio Preferences Model | DATA — `studio_preferences` JSONB config per coach. |
| `DEP-ENG-061` | Recording Engine (FR-CA11-16) | UPSTREAM — Soundboard output feeds into the MediaRecorder/WebSocket stream. |

### Academic Grounding

| Framework | Author | Year | Mechanism |
|---|---|---|---|
| **Peak-End Rule** | Kahneman | 1993 | Streams are remembered by their emotional peaks and ending. Celebration music at winner reveals and dramatic SFX at surprising moments create memorable peaks. |
| **Sonic Branding** | Jackson | 2003 | Consistent audio cues (intro jingle, victory fanfare) create brand association. The coach's audio identity becomes as recognizable as their visual identity. |

### Technical Decisions
1. **Web Audio API (not HTML5 Audio):** Web Audio API provides sample-accurate timing, gain control, and the ability to merge multiple audio streams into a single destination. HTML5 `<audio>` elements cannot be mixed into a MediaRecorder or WebSocket stream.
2. **Pre-loaded AudioBuffer:** SFX files are pre-fetched and decoded into `AudioBuffer` objects on Studio load. This ensures zero-latency playback when the coach clicks a button (no network fetch delay).
3. **Single Music Track Policy:** Only one music track plays at a time. Clicking a new music button stops the current track with a 500ms fade-out, then starts the new track with a 500ms fade-in.

---

## 4. Implementation Plan

### Stage 1: Audio Mixer Pipeline
*Inputs:* Coach microphone MediaStream (from FR-CA11-16's WebRTC capture).
*Outputs:* Merged audio destination feeding into MediaRecorder/WebSocket.
*DEP-ID:* `DEP-ENG-071`

**Steps:**
1. Create `AudioContext` on Studio Block initialization.
2. Create `MediaStreamSource` from coach's microphone stream.
3. Create voice `GainNode` (default volume: 1.0) → connect to `AudioContext.destination`.
4. Create SFX `GainNode` per slot (default volume: 0.8) → connect to same destination.
5. Create music `GainNode` (default volume: 0.5) → connect to same destination.
6. Route `AudioContext.destination` into the canvas stream's audio track (this merges voice + SFX + music into the recording/stream).

### Stage 2: SFX Slots
*Inputs:* S3 audio library URLs from `studio_preferences.sfx_slots`.
*Outputs:* 5 clickable SFX buttons in Studio UI.
*DEP-ID:* `DEP-ENG-070`

**Steps:**
1. Pre-fetch default SFX: drumroll, comedy horn, applause, record scratch, ding chime from `s3://ccp-assets/studio/sfx/defaults/`.
2. Decode each file into `AudioBuffer` via `audioContext.decodeAudioData()`.
3. On button click: create `AudioBufferSource`, connect to SFX GainNode, call `source.start()`.
4. On button click during playback: stop current playback, restart from beginning.
5. Each slot shows: emoji icon, custom label, mini volume slider.

### Stage 3: Music Buttons
*Inputs:* S3 music track URLs from `studio_preferences.music_tracks`.
*Outputs:* 4 music buttons (Intro, Outro, Celebration, Sad/Dramatic) + Stop button.

**Steps:**
1. Pre-fetch 4 default music tracks from `s3://ccp-assets/studio/music/defaults/`.
2. On music button click: check if another track is playing → if yes, fade out (500ms linear ramp to 0) → then start new track with fade in (500ms ramp from 0 to set volume).
3. Implement "Stop All Audio" button: immediately ramp all GainNodes to 0 over 100ms.
4. Music tracks loop: false (play once, stop at end).

### Stage 4: Customization UI & Persistence
*Inputs:* Coach interactions with "⚙ Customize Audio" panel.
*Outputs:* Updated `studio_preferences` row in Supabase.
*DEP-IDs:* `DEP-ENG-072`, `DEP-ENG-073`

**Steps:**
1. Build "Customize Audio" modal: tabbed interface (SFX Library, Music Library, Upload).
2. SFX Library tab: list S3 objects from `s3://ccp-assets/studio/sfx/` with preview playback.
3. Music Library tab: list S3 objects from `s3://ccp-assets/studio/music/` categorized by type.
4. Upload tab: drag-and-drop or file picker. Validate: MP3/WAV, max 10s (SFX) or 60s (music), max 5MB. Upload to `s3://ccp-assets/studio/custom/{coach_id}/`.
5. Save selections to `studio_preferences.sfx_slots` (JSONB) and `studio_preferences.music_tracks` (JSONB).
6. Write configuration-change receipt to the Receipt Chain Guard.

---

## 5. Data Model

```sql
CREATE TABLE studio_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    coach_id UUID NOT NULL UNIQUE REFERENCES coaches(id),
    sfx_slots JSONB DEFAULT '[
        {"slot": 1, "label": "Drumroll", "s3_url": "s3://ccp-assets/studio/sfx/defaults/drumroll.mp3", "volume": 0.8},
        {"slot": 2, "label": "Comedy Horn", "s3_url": "s3://ccp-assets/studio/sfx/defaults/comedy_horn.mp3", "volume": 0.8},
        {"slot": 3, "label": "Applause", "s3_url": "s3://ccp-assets/studio/sfx/defaults/applause.mp3", "volume": 0.8},
        {"slot": 4, "label": "Record Scratch", "s3_url": "s3://ccp-assets/studio/sfx/defaults/record_scratch.mp3", "volume": 0.8},
        {"slot": 5, "label": "Ding", "s3_url": "s3://ccp-assets/studio/sfx/defaults/ding.mp3", "volume": 0.8}
    ]',
    music_tracks JSONB DEFAULT '{
        "intro": {"s3_url": "s3://ccp-assets/studio/music/defaults/intro_upbeat.mp3", "volume": 0.5, "fade_ms": 500},
        "outro": {"s3_url": "s3://ccp-assets/studio/music/defaults/outro_warm.mp3", "volume": 0.5, "fade_ms": 500},
        "celebration": {"s3_url": "s3://ccp-assets/studio/music/defaults/celebration_fanfare.mp3", "volume": 0.6, "fade_ms": 500},
        "sad": {"s3_url": "s3://ccp-assets/studio/music/defaults/sad_dramatic.mp3", "volume": 0.5, "fade_ms": 500}
    }',
    guest_layout VARCHAR(20) DEFAULT 'pip',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 6. Tasks

- [ ] **Task 1:** Build Web Audio API mixer pipeline (AudioContext → GainNodes → destination merge).
- [ ] **Task 2:** Build `<Soundboard />` React component with 5 SFX buttons + 4 music buttons.
- [ ] **Task 3:** Implement SFX pre-fetch, AudioBuffer decode, click-to-play behavior.
- [ ] **Task 4:** Implement music fade-in/fade-out transitions (500ms linear ramp).
- [ ] **Task 5:** Build "Customize Audio" modal with S3 library browser and upload functionality.
- [ ] **Task 6:** Add `studio_preferences` table migration to Supabase.
- [ ] **Task 7:** Populate S3 default audio library (`s3://ccp-assets/studio/sfx/defaults/` and `s3://ccp-assets/studio/music/defaults/`).

---

## 7. Acceptance Criteria

- [ ] **AC1 (SFX Playback):** Click each of the 5 SFX buttons. Assert each plays a distinct sound effect mixed into the recording output.
- [ ] **AC2 (Music Fade):** Play intro music. Click celebration while intro is playing. Assert intro fades out (500ms) and celebration fades in (500ms). No audio overlap.
- [ ] **AC3 (Volume Control):** Set SFX slot 1 volume to 0.3. Play SFX. Assert output gain is ~30% of full volume (measured via `AnalyserNode`).
- [ ] **AC4 (Customization Persistence):** Change SFX slot 3 from "Applause" to a custom uploaded sound. Close and reopen Studio. Assert slot 3 loads the custom sound.
- [ ] **AC5 (Recording Integration):** Record a 30-second video. Play SFX at 10s and music at 20s. Assert the output video file contains all audio tracks mixed together.
- [ ] **AC6 (Stop All):** Play both SFX and music simultaneously. Click "Stop All." Assert all audio stops within 100ms.

---

## 8. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR-CA11-16 (Studio Block) | Internal | Soundboard integrates into the Studio Block's AudioContext and MediaRecorder. |
| S3 bucket: `ccp-assets` | Infrastructure | For storing default and custom audio libraries. |
| Supabase | Internal | For `studio_preferences` table. |

---

## 9. Testing Strategy

### Unit Tests
- **AudioBuffer Decode:** Load a test MP3 from S3. Assert `decodeAudioData()` produces a valid `AudioBuffer` with expected duration.
- **Fade Transition:** Trigger fade-out on a GainNode. Assert gain value reaches 0 within 500ms (±50ms).
- **JSONB Schema:** Validate `sfx_slots` and `music_tracks` JSONB conform to expected schema.

### Integration Tests
- **Full Audio Mix:** Record a 15-second video with: voice at 0-15s, SFX at 5s, music at 10s. Assert all three audio sources are present in the output file.
- **Customization Roundtrip:** Upload a custom SFX → save → reload Studio → assert custom SFX loads correctly.
