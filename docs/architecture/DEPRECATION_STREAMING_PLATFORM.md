# Deprecation & Decommissioning Specification: Streaming Platform & Real-Time Broadcast Subsystems

**Created:** 2026-05-21  
**Status:** Approved for Deprecation  
**Version:** 1.0  
**Domain:** Workspace / Studio / Commercial  
**Reference Specs:** `FR-CA11-16`, `FR-CA11-21`, `FR-CA11-22`, `FR-CA11-13`, `FR-CA11-14`

---

## 1. Executive Summary

As part of the Era 3 structural consolidation of the Conscious Coaching Platform (CCP), all active **real-time live streaming, multi-party guest join, and OBS Studio-based streaming workflows** are officially deprecated and decommissioned. 

The business model and operational focus have shifted away from synchronous broadcasting and RTMP distribution. Instead, all media creation is consolidated into asynchronous, client-side, high-performance recording (Loom-style) using the native browser APIs within the AFFiNE workspace plugin (`loom_quick` mode).

This document serves as the formal specification for decommissioning the streaming infrastructure, disabling signaling endpoints, removing dependencies, and restructuring downstream databases.

---

## 2. Decommissioned Technical Specifications

The following technical specifications are retired in their entirety and moved to `DEPRECATED` status in the system registries:

| Spec ID | Document Name | Deprecation Context / Rationale |
| :--- | :--- | :--- |
| **FR-CA11-21** | `FR-CA11-21_Studio_Guest_Join_Tech_Spec.md` | **RETIRED:** Decommissions WebRTC multi-party / peer-to-peer guest join. Remote guest recordings are no longer supported inside the Studio block. |
| **FR-CA11-22** | `FR-CA11-22_Stream_Overlay_Trivianar_Display_Tech_Spec.md` | **RETIRED:** Decommissions real-time stream overlay rendering matrices and dynamic client interaction widgets. |
| **FR-CA11-13** | `FR-CA11-13_OBS_Recording_Controller_Tech_Spec.md` | **RETIRED:** OBS WebSocket control integration is fully defunct. |
| **FR-CA11-14** | `FR-CA11-14_Excalidraw_Live_OBS_Overlay_Tech_Spec.md` | **RETIRED:** Live drawing overlays to OBS virtual outputs are fully defunct. |

---

## 3. Infrastructure & Service Decommissioning

### A. `ccp-stream-service` (Docker Microservice)
*   **Action:** Terminate and delete the `ccp-stream-service` repository and delete its Docker configurations.
*   **Details:** The Node.js `node-media-server` instance responsible for consuming WebM/H264 WebSocket streams, repackaging them to RTMP, and pushing them to external platforms (YouTube Live, Facebook Live, Twitch) is fully retired.
*   **Infrastructure Impact:** Terminate all running ECS tasks/EC2 instances associated with `ccp-stream-service`. Remove the security groups and load balancers routing port `1935` (RTMP) and `8000` (WebSocket signaling).

### B. STUN/TURN (coturn) Server Deployment
*   **Action:** Deprovision the AWS coturn TURN server.
*   **Details:** NAT traversal servers running `coturn` on port `3478` for peer-to-peer WebRTC connections between coach and remote guests are no longer required.
*   **Infrastructure Impact:** Terminate coturn container instances and reclaim elastic IP addresses.

---

## 4. API Endpoints & Routes Disabling

All streaming, broadcasting, and signaling endpoints must be removed from `src/ccp/api/` or disabled (returning `410 Gone` if queried by legacy clients):

1.  `POST /studio/broadcast/signal` (Signaling for WebRTC/SFU block broadcasting) -> **REMOVE**
2.  `POST /studio/guest-invite` (Invite link generation and token allocation) -> **REMOVE**
3.  `/ws/stream/{session_id}` (WebSocket chunk transport server) -> **REMOVE**
4.  `/signal/{session_id}` (WebRTC guest SDP/ICE signaling channel) -> **REMOVE**

---

## 5. Database Schema Restructuring (Supabase)

### A. Table Drop
The `studio_guest_sessions` table is dropped from the active PostgreSQL migration schemas:
```sql
DROP TABLE IF EXISTS studio_guest_sessions;
```

### B. Table Modification (`studio_sessions`)
All streaming-related columns in `studio_sessions` are deprecated. Any new schemas must drop these columns, and existing databases should migrate by running:
```sql
ALTER TABLE studio_sessions 
  DROP COLUMN IF EXISTS is_stream,
  DROP COLUMN IF EXISTS stream_destinations;
```

---

## 6. Restructuring of the Studio Block (`FR-CA11-16`)

The active plugin code (`ccp-blocks/studio-block/`) is restricted strictly to client-side video composition and recording:
*   **Loom-Style Only:** Only solo camera, screen capture, and composited camera+screen canvas layouts are supported.
*   **Client-Side MediaRecorder:** The browser's native `MediaRecorder` encodes WebM/VP9 chunks locally.
*   **Direct-to-S3:** Chunks are temporarily kept in browser storage (IndexedDB) and uploaded directly to S3 upon stop/pause, bypassing any intermediate streaming relay servers.
