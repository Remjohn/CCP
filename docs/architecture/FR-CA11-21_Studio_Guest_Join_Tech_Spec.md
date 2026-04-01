# Tech-Spec: FR-CA11-21 — Studio Guest Join (WebRTC Multi-Party)

**Created:** 2026-03-25
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / PRD Update v2.0 — Capability Area 11)
**Architecture Reference:** PRD-Update-CA11 §4.5 (FR-CA11-21), ADR-07
**Skill Implementation:** `ccp-blocks/studio-block/components/GuestJoin.tsx` + `ccp-stream-service` signaling
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd-update-CA11-quad-platform.md` (§4.5 FR-CA11-21)
- `d:\Work\The Conscious Coaching Factory\docs\features\FB_Full_Stack_Recording_Streaming.md` (§3.8)

---

## 2. Overview

### Problem Statement
Coaches need to record testimonial videos, expert interviews, co-coaching hot-seats, and collaborative sessions with remote guests. The retired OBS approach had no native guest-join capability — coaches required separate tools (Zoom, Google Meet) recorded via screen capture, losing quality and control.

### Solution
FR-CA11-21 adds **guest join** capability to the CCP Studio Block via WebRTC peer-to-peer connection. The coach generates a time-limited invite link, the guest opens it in their browser (no app install), and their webcam/mic feed composites onto the recording canvas in PiP (picture-in-picture) or side-by-side layout.

### Scope
**In scope:**
- WebRTC peer-to-peer connection (coach ↔ guest via ccp-stream-service signaling).
- Invite link generation (time-limited, single-use tokens).
- Guest browser join page (webcam/mic permissions, connection flow).
- Canvas compositing (PiP overlay or side-by-side layout).
- Guest audio mixing via Web Audio API.
- Coach controls (mute guest, resize/reposition, switch layout, disconnect).
- `studio_guest_sessions` table.

**Out of scope:**
- Multi-guest (3+ guests) — post-MVP enhancement.
- Guest recording their own side independently.
- Guest access to AFFiNE workspace content.

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-093` | WebRTC Signaling Endpoint | INFRASTRUCTURE — ccp-stream-service `/signal` WebSocket endpoint for SDP/ICE exchange. |
| `DEP-ENG-094` | Guest Join Page | UI — Standalone HTML/React page for guest browser join (no app install). |
| `DEP-ENG-095` | Canvas Compositing (Guest) | CORE — Draws guest video onto the recording <canvas> in PiP or side-by-side. |
| `DEP-ENG-096` | Guest Audio Merge | AUDIO — Guest AudioStreamSource → GainNode → merge with coach audio. |
| `DEP-ENG-097` | Invite Link Generator | API — FastAPI endpoint for creating time-limited, single-use guest tokens. |
| `DEP-ENG-061` | Recording Engine (FR-CA11-16) | UPSTREAM — Guest compositing feeds into the same canvas that MediaRecorder captures. |

### Academic Grounding

| Framework | Author | Year | Mechanism |
|---|---|---|---|
| **Testimonial Social Proof** | Cialdini | 1984 | Video testimonials with the actual client visible create stronger social proof than text testimonials. Guest join enables authentic, co-present testimonial recording. |
| **Parasocial Relationship Enhancement** | Horton & Wohl | 1956 | Seeing the coach interact with a real guest creates stronger parasocial bonds than solo-to-camera content. |

### Technical Decisions
1. **WebRTC Peer-to-Peer (not SFU):** For 1-guest MVP, peer-to-peer WebRTC is simpler and lower latency than an SFU (Selective Forwarding Unit). Coach and guest exchange SDP offers directly. If multi-guest (3+) becomes needed, we'll migrate to Mediasoup/Janus SFU.
2. **STUN + TURN:** STUN (Session Traversal Utilities for NAT) handles most residential connections. TURN (Traversal Using Relays around NAT) via coturn on AWS handles corporate firewalls. Config: `iceServers: [{ urls: 'stun:stun.l.google.com:19302' }, { urls: 'turn:turn.ccp.aws.com:3478', username, credential }]`.
3. **Canvas Compositing (not <video> overlay):** Guest video is drawn onto the same `<canvas>` used for recording (FR-CA11-16). This ensures the guest is part of the MediaRecorder output without additional mixing.

---

## 4. Implementation Plan

### Stage 1: WebRTC Signaling
*DEP-ID:* `DEP-ENG-093`

**Steps:**
1. Add `/signal/{session_id}` WebSocket endpoint to `ccp-stream-service`.
2. Implement SDP exchange: coach sends `offer`, guest receives, guest generates `answer`, sends back.
3. Implement ICE candidate relay: trickle ICE candidates exchanged via the same WebSocket.
4. Deploy coturn (TURN server) on AWS: `docker run -d coturn/coturn` with TLS configured.

### Stage 2: Invite Link & Guest Page
*DEP-IDs:* `DEP-ENG-094`, `DEP-ENG-097`

**Steps:**
1. Add FastAPI endpoint: `POST /studio/guest-invite { session_id, coach_name }` → returns `{ invite_url, token, expires_at }`.
2. Token expires in 30 minutes. Single-use (deleted after first connection or expiry).
3. Build guest join page: `https://studio.consciouselite.com/join/{token}` — lightweight HTML/React page.
4. Guest page flow: Enter name → Request webcam/mic permissions → Show preview → Click "Join" → WebRTC connection established.
5. Store guest session in `studio_guest_sessions` table.
6. Write event receipt to Receipt Chain Guard upon successful connection (or token exhaustion).

### Stage 3: Canvas Compositing & Audio
*DEP-IDs:* `DEP-ENG-095`, `DEP-ENG-096`

**Steps:**
1. On WebRTC `track` event (remote stream received): create `<video>` element from guest stream (hidden DOM).
2. In the `requestAnimationFrame` loop (FR-CA11-16 Stage 2): draw guest video onto canvas.
3. **PiP Layout:** Guest video drawn as 25% size oval/rectangle in bottom-right corner. Coach video fills remaining space.
4. **Side-by-Side Layout:** Canvas split 50/50. Coach on left, guest on right.
5. Coach UI: "Switch Layout" button toggles PiP ↔ Side-by-Side. "Resize" slider for PiP (15%-35% of canvas).
6. Guest audio: create `MediaStreamSource` from guest stream → `GainNode` → merge into AudioContext (same as soundboard merge point).
7. Coach controls: Mute Guest button (ramps guest GainNode to 0), Disconnect Guest button (closes WebRTC connection).

---

## 5. Data Model

```sql
CREATE TABLE studio_guest_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES studio_sessions(id),
    guest_name VARCHAR(255) NOT NULL,
    join_token VARCHAR(64) NOT NULL UNIQUE,
    token_expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    layout_mode VARCHAR(20) DEFAULT 'pip', -- pip, side_by_side
    status VARCHAR(20) DEFAULT 'pending', -- pending, connected, disconnected
    connected_at TIMESTAMP WITH TIME ZONE,
    disconnected_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_guest_sessions_token ON studio_guest_sessions(join_token);
CREATE INDEX idx_guest_sessions_session ON studio_guest_sessions(session_id);
```

---

## 6. Tasks

- [ ] **Task 1:** Add `/signal/{session_id}` WebSocket endpoint to ccp-stream-service for WebRTC signaling.
- [ ] **Task 2:** Deploy coturn (TURN server) on AWS with TLS.
- [ ] **Task 3:** Build `POST /studio/guest-invite` endpoint (token generation, expiry).
- [ ] **Task 4:** Build guest join page (`/join/{token}` — webcam/mic permissions, name entry, WebRTC connection).
- [ ] **Task 5:** Build canvas compositing for guest video (PiP + side-by-side layouts).
- [ ] **Task 6:** Build guest audio merge via Web Audio API.
- [ ] **Task 7:** Build coach controls (mute, resize, layout switch, disconnect).
- [ ] **Task 8:** Add `studio_guest_sessions` table migration to Supabase.

---

## 7. Acceptance Criteria

- [ ] **AC1 (Invite Link):** Generate an invite link. Assert token is unique, expires in 30 minutes.
- [ ] **AC2 (Guest Connect):** Guest opens invite link → grants webcam/mic → clicks Join → assert WebRTC connection established, guest video visible on coach's canvas.
- [ ] **AC3 (PiP Layout):** With guest connected, assert guest video renders as 25% overlay in bottom-right corner.
- [ ] **AC4 (Side-by-Side):** Switch to side-by-side layout. Assert canvas splits 50/50 with coach left, guest right.
- [ ] **AC5 (Audio Merge):** Guest speaks. Assert guest audio is present in the recording output alongside coach voice and soundboard.
- [ ] **AC6 (Mute Guest):** Click "Mute Guest." Assert guest audio is silenced. Guest video remains visible.
- [ ] **AC7 (Disconnect):** Click "Disconnect Guest." Assert WebRTC connection closed, guest video removed from canvas.
- [ ] **AC8 (Token Expiry):** Wait 31 minutes. Try to use expired token. Assert error: "This invite link has expired."
- [ ] **AC9 (TURN Fallback):** Block STUN (simulate corporate firewall). Assert connection succeeds via TURN relay.
- [ ] **AC10 (Recording Integrity):** Record 30 seconds with guest. Stop. Assert output video contains both coach and guest video/audio.

---

## 8. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR-CA11-16 (Studio Block) | Internal | Guest compositing extends Studio Block's canvas and AudioContext. |
| ccp-stream-service | Internal | Hosts the WebRTC signaling endpoint. |
| coturn (TURN server) | Infrastructure | For NAT traversal behind firewalls. |
| Supabase | Internal | For `studio_guest_sessions` table. |

---

## 9. Testing Strategy

### Unit Tests
- **Token Generation:** Assert tokens are 64-char hex strings, unique, with correct 30-min expiry.
- **Layout Computation:** Test PiP coordinates (guest at 25% in bottom-right) and side-by-side (50/50 split) for 16:9 and 9:16 canvases.

### Integration Tests
- **Full Guest Flow:** Generate invite → guest connects → verify WebRTC data channel → verify canvas compositing → disconnect → verify cleanup.
- **TURN Relay:** Block direct connectivity. Assert TURN relay connection succeeds.

### Manual Verification
- **Video Quality:** Guest joins from a different network. Verify guest video quality is acceptable (720p minimum, no excessive artifacts).
- **Audio Sync:** Verify guest audio is in sync with guest video (no lip-sync drift > 100ms).
