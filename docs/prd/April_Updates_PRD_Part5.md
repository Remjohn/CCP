# Product Requirements Document: April Updates — Sovereign Telegram Mini App Ecosystem

**Status:** In Progress (Part 5 - User Journeys & Failure Modes)

---

## 10. Advanced User Journeys

To understand how the April Updates fundamentally alter the Conscious Coaching Platform, we must trace the exact execution paths of our primary users.

### 10.1 Journey A: The Cold Acquisition (Coach Perspective)
*Targeting the "Show Before Selling" Mandate (FR-APR-03, FR-APR-01, FR-APR-10)*

**The Scenario:** Sarah is a high-ticket holistic coach. She is exhausted by AI marketing tools and has zero intent to buy another SaaS product. She clicks a Facebook ad that simply says: *"Are you pacing your videos correctly? Find out for free."*

1.  **The Trigger:** Sarah clicks the link, opening our Telegram Bot. She sends the `/audit_me` command followed by a link to her recent Instagram Reel.
2.  **The Audit (FR-APR-03):** The backend immediately downloads the video. The Biometric Extraction agent (via Deepgram) analyzes the audio. It detects a 23% drop in pacing after the 40-second mark and a high density of filler words.
3.  **The "Show Before Selling" (FR-APR-10):** Without asking Sarah, the SVRE (Visual Research Engine) pipeline kicks in. It takes the transcription, applies the "Witness Arc" storytelling framework, and generates a Cinematic Short, a Branded Carousel, and a Meme Hook. 
4.  **The Delivery:** Within 4 minutes, Sarah receives a Telegram message: *"Sarah, your pacing drops by 23% right when you make your core claim. This signals a lack of conviction. We fixed it. Here is a cinematic edit of your video, plus a carousel and a meme. They are watermarked."*
5.  **The Tripwire (FR-APR-01):** Sarah is shocked by the quality. The bot continues: *"To remove the watermarks and download these assets right now, pay $16.95."* She clicks the Stripe checkout link. The FastAPI backend validates the payment, updates the `coach_subscriptions` table, and delivers the clean assets.
6.  **The Upsell:** The receipt page fires the final hook: *"Want this done 9 times a week, plus weekly voice training to fix your pacing? Upgrade to the $39.95/week Voice Coach Engine."* She upgrades. The Redis limiters initialize her 4-export/week limits.

### 10.2 Journey B: The 5k-User Interactive Broadcast (Client Perspective)
*Targeting the Interactive Trivianar & Mini App Ecosystem (FR-APR-04, FR-APR-06)*

**The Scenario:** Marcus is a follower of Coach Sarah. He receives a Telegram broadcast inviting him to a live "Belief System Audit" event at 8 PM.

1.  **The Handshake (FR-APR-04):** At 8 PM, Marcus clicks the "Join Live" inline button in Telegram. The Next.js React application opens natively inside the Telegram UI. The `initData` is instantly validated by FastAPI, establishing a persistent `wss://` WebSocket connection. No login screen is ever shown.
2.  **The Trivianar (FR-APR-06):** Coach Sarah appears on screen (WebRTC broadcast). She asks: *"What is the primary emotion holding you back right now? A) Anger, B) Fear, C) Apathy."*
3.  **The UDP Flood:** Marcus, along with 4,999 other users, taps option "B". His React app sends the JSON payload over the WebSocket. FastAPI drops it into the Redis `LPUSH` queue.
4.  **The Sub-Second Update:** 500ms later, the Celery sweep aggregates the 5,000 answers. The WebSocket broadcasts the result: *"62% Fear, 28% Anger, 10% Apathy."* The Next.js DOM re-renders instantly, showing the moving progress bars.
5.  **The B2B2C Metering (FR-APR-01):** Because Marcus interacted with the bot, the system executes a `SADD` command into Redis (`active_clients:sarah:may`). Since he is a new active user this month, a background task quietly pings the Stripe Metered Usage API, adding $3.90 to Sarah's monthly bill.

### 10.3 Journey C: The High-Pressure Sales Roleplay (Coach Training)
*Targeting the WebRTC Roleplay Engine & Voice-First Orchestration (FR-APR-05, FR-APR-07)*

**The Scenario:** Coach Sarah is preparing to close a $10,000 client. She needs live, high-pressure practice. She uses the `/roleplay_init` command.

1.  **The Boot Sequence:** FastAPI hits the Modal.com API, waking up a "cold" Pipecat Python container. Within 1.5 seconds, a Daily.co WebRTC room is generated and the link is sent to Sarah.
2.  **The AI Moderator (FR-APR-05):** Sarah invites her peer coach, David, into the room. They begin the roleplay. The Pipecat container sits silently in the room as a hidden participant.
3.  **The Intervention (FR-APR-07):** David gives a difficult objection: *"I just don't have the time for this right now."* Sarah freezes. 7 seconds of dead air pass. The Pipecat container detects the VAD silence threshold breach. The quantized LLaMa-3 model evaluates the context and triggers the Riva TTS engine. 
4.  **The Voice Command:** The AI Moderator speaks into the room with the synthesized voice of Jim Rohn: *"Sarah, you lost the frame. He gave you a time objection, but it's a priority objection. Use the 'Mirror' technique. Go."*
5.  **The Brutal Cutoff:** The roleplay continues intensely. At exactly 23 minutes and 55 seconds, the AI Moderator interrupts: *"Final 5 seconds. Hold the frame."* At exactly 1440 seconds, the Celery task fires `DELETE /v1/rooms/[id]`. The WebRTC room collapses. The Next.js frontend catches the disconnect and routes them to the biometric summary page. Sarah is left wanting more—the Zeigarnik Effect is achieved.

---

## 11. Anti-Drafting & Failure Mode Protocols

We cannot assume the infrastructure will work perfectly under load. The April Updates include strict failure protocols to ensure the platform degrades gracefully rather than crashing catastrophically.

### 11.1 The Corporate Firewall Block (WebSockets)
**The Threat:** A user attempting to join the Trivianar is on a corporate VPN that blocks UDP traffic and `wss://` WebSocket protocols.
**The Fallback (FR-APR-04):** The Next.js frontend implements a 2500ms timeout on `socket.onopen`. If the WebSocket fails to establish within that window, the React context provider catches the error and instantly downgrades the transport protocol to an Axios-based HTTP Long-Polling or Server-Sent Events (SSE) loop. The user experiences ~600ms latency instead of ~40ms, but they are not disconnected from the event.

### 11.2 The Stripe Webhook Desync
**The Threat:** The Stripe API goes down, or our server drops the `payment_failed` webhook, allowing a coach to continue generating content without paying.
**The Fallback (FR-APR-01):** The system does not rely purely on push webhooks. The `reset_export_limits.py` cron job (which runs every Sunday at 23:59 UTC) executes a synchronous `GET` request to the Stripe API for every active `coach_id` *before* allocating the new weekly 4-export limits into Redis. If Stripe reports the subscription as `past_due`, the limits are set to 0.

### 11.3 The LLM Schema Hallucination
**The Threat:** The LLM powering the Speaker Audit Engine (FR-APR-03) hallucinates the JSON structure, returning text instead of the required `biometric_analysis` object, which would crash the Next.js frontend.
**The Fallback (FR-APR-08):** Because all unstructured LLM logic is wrapped in DSPy/Pydantic validation, the `TillDone` Pi Extension catches the `PydanticValidationError`. The extension automatically appends the stack trace to the prompt and forces the LLM to retry. If it fails 3 times, the system returns a pre-cached, generic error payload (e.g., "Audit currently processing, check back in 5 minutes") to the user, preventing a raw JSON parsing error in the DOM.

### 11.4 The Redis Memory Overflow (Trivianar)
**The Threat:** During a 5,000-user Trivianar, the Redis `LPUSH` queue grows faster than the Celery worker can sweep it, causing a memory overflow on the EC2 instance.
**The Fallback (FR-APR-06):** The Redis queue for Trivianar responses is configured with an `LTRIM` policy, capped at 15,000 items. If the queue hits the ceiling, the oldest (stale) responses are dropped. Furthermore, the Next.js frontend employs a debounce function on the answer buttons to prevent users from spam-clicking and generating artificial UDP floods.

---

## 12. Final Execution Mandate

The documentation is complete. The 10 Technical Specifications outlined in this PRD govern the 48-hour launch. 
No feature creep is permitted. 
No LLM "auto-fixing" is permitted outside the DSPy boundaries. 
Execution must follow the architectural constraints defined above.

**End of Document.**
