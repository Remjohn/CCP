---
type: architecture-brief
author: Winston (System Architect)
date: 2026-04-13
status: Final
dependencies:
  - d:\Work\The Conscious Coaching Factory\docs\prd\prd.md
  - d:\Work\The Conscious Coaching Factory\docs\prd\prd-update-CA11-quad-platform.md
  - d:\Work\The Conscious Coaching Factory\docs\prd\prd-update-how-we-got-here-svre-scre.md
  - d:\Work\The Conscious Coaching Factory\docs\prd\prd-update-visual-control-layer.md
  - d:\Work\The Conscious Coaching Factory\docs\prd\CMF_Pipeline_Documentation.md
  - d:\Work\The Conscious Coaching Factory\lab\CCP APRIL Updates\Law28_CBCS_Program_Architecture_Brief.md
  - d:\Work\The Conscious Coaching Factory\lab\growth_syntheses\Roleplay_Engine_TRIZ_MCDA_Synthesis.md
  - d:\Work\The Conscious Coaching Factory\lab\growth_syntheses\Trivianar_Mini_App_MCDA_Synthesis.md
  - d:\Work\The Conscious Coaching Factory\lab\growth_syntheses\Telegram_Mini_App_Virality_MCDA.md
project: Conscious Coaching Platform - The Mini App Ecosystem
length: ~3,400 words
---

# Architecture Brief: The Sovereign Telegram Mini App Ecosystem

## 1. Documentation Preamble
*Written by Winston, Senior System Architect.*

Let me be blunt: the coaching industry is plagued by fragile, over-engineered AI wrappers. As the Architect for this platform, I refuse to deploy "hype" infrastructure. We deploy boring, robust technology that operates with absolute mathematical certainty. 

Following the strategic directions of the Product Manager (John) and the Engineering Requirements of the Tech Writer (Paige), I have designed the backend architecture required to support the new Sovereign Telegram Mini App Ecosystem. 

The mandate here is strict:
1. **The Webhook Ban:** We are officially banning the use of Telegram Bot API webhooks for any synchronous event. Trivianar and Roleplay state will be managed exclusively via persistent WebSockets hitting our FastAPI transit layer. 
2. **The Maximum Export Limiter Architecture:** There is no "credit billing" or "metered billing" for AI generation. The platform operates on a strict Maximum Export Limiter. Each coach is hard-capped at 4 exports per week across 8 distinct SVRE content formats. 
3. **The Brownfield Constraint:** The `Context_Premise` Neo4j graph and the existing CPSC `cbcs_interaction_logs` in Supabase MUST NOT BE BROKEN. The new WebRTC Roleplay engine will inject biometric data as JSONB payloads into the existing tables.

This document serves as the absolute blueprint for deployment.

---

## 2. System Topology & Component Matrix

The CCP Mini App Ecosystem splits the architectural load across four entirely decoupled boundaries. We do not run monolithic servers. We run highly specialized transit nodes.

### Boundary 1: The Telegram Client (HTML5 Canvas)
The frontend is a standard Next.js (React) application loaded inside the `Telegram.WebApp` shell. 
- **Responsibility:** Rendering the DOM, capturing user inputs, maintaining WebSocket persistent handshakes, and housing the Daily.co WebRTC IFrames.
- **Constraints:** It holds absolutely zero secure caching. All state must consider the client as fundamentally compromised and untrustworthy.

### Boundary 2: FastAPI Transit Gateway (The Coordinator)
We deploy a fleet of stateless, horizontally scaled Python `FastAPI` nodes on AWS EC2 (behind Application Load Balancers).
- **Responsibility:** Managing the `wss://` (WebSocket) connections, verifying JWT tokens from Telegram, and acting as the traffic cop.
- **Constraints:** The FastAPI nodes do NOT execute heavy ML workloads. They do not write to PostgreSQL synchronously. They exist solely to route packets insanely fast.

### Boundary 3: The Pipecat/Modal Compute Cluster (AI Moderator)
When a 1-on-1 Roleplay starts, the FastAPI server triggers a serverless GPU instance via `Modal.com`. This instance boots a `Pipecat` Python worker.
- **Responsibility:** Connecting to the Daily.co WebRTC room as a standard participant. Routing the audio stream through the Nvidia NIM STT -> LLaMa-3 -> Riva TTS pipeline. 
- **Constraints:** The worker must have a hard `SIGKILL` timeout set to 1440 seconds (24 minutes) to enforce the psychological scarcity "Energy Bar" rule defined in the PRD, regardless of the API state.

### Boundary 4: Daily.co / AWS S3 (A/V Hardware & Capture)
We do not build our own WebRTC stun/turn servers. We buy reliability. 
- **1-on-1 Roleplay:** Routed entirely through Daily.co's infrastructure for peer-to-peer security.
- **Trivianar Debate Co-Hosting:** Handled via Daily.co or native Telegram WebRTC splits. Crucially, the Transit Layer is responsible for capturing the raw H.264 video streams of BOTH co-hosts simultaneously. These `.mp4` chunks are continuously streamed to an AWS S3 bucket for internal interaction tracking. (The SVRE pipeline connects exclusively to Daily Mini App Recordings for automated editing, not live streams).

---

## 3. Database Architecture & Schema Evolutions

To support the B2B2C metering model and the new synchronous engines without destroying our CA11 architecture, we are utilizing an asymmetric read/write topology between Redis and PostgreSQL (Supabase).

### 3.1 The Maximum Export Limiter Schema (Redis)
The PRD mandates that coaches have a strict limit of 4 exports per week per content type, AND a global cap of 8 total exports across all types, with absolutely no "credit billing" overflow. Because this tracking must be highly concurrent (across the SVRE clusters), we use Redis hash tracking instead of PostgreSQL.

**The Redis Bucket Pattern:**
Key: `export_limits:{coach_id}:{iso_week_string}`

```json
{
  "total_weekly_count": 8,       // At limit, ALL new requests return 429 Limit Exceeded
  "shorts_reels": 3,
  "long_video_reactions": 4,     // At limit for this type, request returns 429 Limit Exceeded
  "long_carousels": 1,
  "short_carousels": 0,
  "memes": 0,
  "polls": 0,
  "hot_takes": 0,
  "super_visuals_ghibli": 0
}
```
**Reset Protocol:** A scheduled background worker (`reset_export_limits.py`) sweeps these buckets at 23:59 UTC every Sunday. If a backend SVRE node requests an export, the FastAPI server runs a MULTI/EXEC transaction to check both `total_weekly_count` < 8 and the specific format count < 4. If either is exceeded, the request is actively rejected.

### 3.2 The Brownfield Fix: `cbcs_interaction_logs`
The WebRTC Roleplay Engine generates biometric scores (Conviction Density, Interrupt Frequency, Pace). Rather than creating a new siloed database, we append a JSONB structure to the *existing* core table.

```json
// Example JSONB Payload injected into the 'interaction_metadata' column
{
  "module_type": "webRtc_roleplay",
  "room_id": "dl_xyz123",
  "biometric_score": {
    "interrupt_frequency": 4,
    "wpm_average": 145,
    "mood_state_resonance_compliance": 0.88,
    "objection_handling_flag": "PASSED"
  },
  "opponent_id": "external_guest_55"
}
```
*Why this matters:* The CPSC Conversion Engine (Capability Area 9) already knows how to read `cbcs_interaction_logs`. By forcing the WebRTC data into this exact schema, the sales intelligence agents can *immediately* use Roleplay performance metrics to decide if a client is ready for a high-ticket invitation without rewriting the AI prompt logic.

### 3.3 The Trivianar Redis Queue
Trivianar involves 5,000 users clicking buttons simultaneously. PostgreSQL will collapse under 5,000 UDP insert locks within 200ms. 
We bypass Postgres entirely for transient state.

**Redis LPUSH Schema:**
When user `U1` clicks Answer `B` on Question `4`, the WebSocket hits FastAPI. FastAPI executes:
`LPUSH trivianar:responses:Q4 "{user_id: 'U1', answer: 'B', ts: 1712950000}"`

This Redis operation takes `~0.1ms`. 
A Python Celery worker runs `BRPOP` on the queue. Every 500ms, it compiles the thousands of responses, validates the correct answer, and executes a *single* `BULK INSERT` into PostgreSQL for permanent storage. 

---

## 4. Network Protocol Definitions: The WebSocket Shift

The shift from Telegram's traditional webhook model to native WebSockets inside the Mini App is profound. It drops latency from 1,200ms down to 40ms.

### 4.1 The Secure Handshake
Because Mini Apps are web clients, they are vulnerable. We must securely identify the user without requiring them to log in (to preserve the frictionless B2B viral loop).

1. The user opens the Mini App. The Telegram API provides `window.Telegram.WebApp.initData`.
2. The React app opens the WebSocket: `new WebSocket('wss://api.consciouscoaching.com/v1/ws')`.
3. The *very first payload* sent must be the `initData` string.
4. The FastAPI server validates the cryptographic hash of `initData` using the Telegram Bot Token (which resides safely on the server). 
5. If valid, the connection moves to state `ESTABLISHED`. If invalid, `socket.close(1008, "Policy Violation")`.

### 4.2 Trivianar Sub-Second Event Routing
Once `ESTABLISHED`, the transit layer is bi-directional.
When the Coach clicks "Show Next Question", the Coach Dashboard fires an authenticated REST POST to FastAPI.
FastAPI loops through the `ConnectionManager` dictionary:
```python
async def broadcast_question(question_payload: dict, room_id: str):
    for client_ws in active_connections[room_id]:
        await client_ws.send_json({"event": "NEW_QUESTION", "data": question_payload})
```
This bypasses Long-Polling HTTP limitations entirely. The 400 clients receive the JSON payload, and React maps it to the DOM instantly.

### 4.3 WebRTC Failover (The "Corporate Firewall" Problem)
WebSockets are occasionally blocked by restrictive B2B corporate firewalls. 
If the React client fails `socket.onopen` after 2500ms, it must natively failover to an Axios-based `Server-Sent Events (SSE)` or Long-Polling loop to ensure the Trivianar is never inaccessible. However, if strict WebRTC UDP layers are blocked, the Daily.co Roleplay Engine will fail. The UI must aggressively present a "Network Restriction Detected - Please disconnect from VPN" warning.

---

## 5. The Ai Moderator: Pipecat & NIM Deployment

The Roleplay Engine requires a 2-Human + 1-AI Room. The AI must mimic human latency to feel like a real Moderator, meaning we require "Voice-to-Voice" latency under 800ms. Standard OpenAI REST APIs (which run 2.5 seconds) are architecturally disqualified.

### 5.1 The Orchestrator
We use `Pipecat` running inside `Modal.com`. Modal allows us to keep GPU containers "warm" on standby, booting the Python environment in under 1.5 seconds when the Coach hits "Start Roleplay".

### 5.2 The Pipeline
1. **STT (Speech to Text):** Deepgram WebSockets or local Nvidia Whisper (running on the Modal container).
2. **Context Evaluator:** A local, quantized explicit LLM (e.g., `Llama-3-8B-Instruct`). It holds the *System Prompt* defining the 24-minute limit, the objection-handling rules, and the PRD's Mood State Resonance map.
3. **TTS (Text to Speech):** ElevenLabs WebSockets (for ultra-high fidelity) or Nvidia Riva. 

### 5.3 The Execution Strategy
The Pipecat worker acts "deaf" while the human participants are talking, analyzing the VAD (Voice Activity Detection) metrics for *Interrupt Frequency*.
It only speaks when:
- **Condition A (Intervention):** A silence threshold of >6 seconds is breaches during a tense Roleplay.
- **Condition B (Conclusion):** The backend timer registers `T = 1420 seconds`. The Pipecat worker receives an out-of-band Redis Pub/Sub signal from the FastAPI orchestrator containing the `HARD_STOP_IMMINENT` payload. The Pipecat worker triggers the TTS generation for the Exit Phrase.

---

## 6. Systemic Scarcity: The 24-Minute Energy Bar Enforcement

The PRD mandates the 24-Minute Energy Bar to prevent burnout and engineer daily habit loops (The Zeigarnik Effect). This must be enforced with mathematical cruelty at the infrastructure layer, independent of frontend clock drift.

### 6.1 The Disconnect Protocol
1. When the Daily.co room is generated, FastAPI logs `room_created_at = NOW()` and schedules an asynchronous Celery task: `destroy_room.apply_async(args=[room_id], countdown=1440)`.
2. At precisely 24 minutes, the Celery task fires, hitting the Daily.co API `DELETE /v1/rooms/[room_id]`.
3. Daily.co's infrastructure handles the forcible disconnection of all WebRTC peers. The React frontend recognizes the `left-meeting` event gracefully.

### 6.2 The Speaking Audit Qualification Protocol
Upon disconnection, the Mini App executes `router.push('/summary')`. 
At this point, the backend pauses the delivery of the biometric feedback. The user is presented with the 3 Pre-Qualification Prompts (Coach? Audience? Challenges?). These responses are sent back over the WebSocket. If the answers fit the target demographic, the backend triggers the `generate_invitation` event and the UI flashes the "Join the Speaking Audit Law 28 Challenge" CTA. If not, the flow ends gracefully with no offer.

---

## 7. Next Steps for Implementation

The architecture is complete. We have abandoned brittle LLM prompting for the backend and embraced deterministic data routing, strictly adhering to the Product Brief's business model (Coach-Pays metering) and the PRD's UI constraints.

The engineering department is now authorized to execute the following pipeline:
1. Initialize the Next.js Telegram Mini App repository.
2. Build the FastAPI + Redis WebSocket gateway (including the `HINCRBY` export limits).
3. Engineer the Pipecat Modal container for the Jim Rohn Voice Engine and WebRTC S3 capture logic.
4. Establish the AFFiNE user dashboard resource sync commands.

---
*End of CCP Update Architecture Brief*
