# Product Requirements Document: April Updates — Sovereign Telegram Mini App Ecosystem

**Status:** In Progress (Part 2)

---

## 4. Track A: The Revenue Core (Wave 1 Foundation)

Before any generative intelligence is scaled to the public, the platform must be mathematically bounded by a metered commerce engine. 

### 4.1 FR-APR-01: B2B2C Metered Billing Architecture
The platform fundamentally rejects the "AI API wrapper" business model (where users pay for tokens). We operate a hybrid SaaS + Usage model. 

**Business Rules:**
*   **The SaaS Floor:** Coaches pay a weekly subscription ($39.95 for Tier 1, $49.95 for Tier 2) via Stripe.
*   **The B2B2C Meter:** Coaches are charged $3.90 per month for every unique active client interacting with their sovereign Telegram bot.
*   **Zero Credit Loopholes:** We do not sell "credits" for generation. The system enforces a strict 4-export/week limit per content format.

**Technical Execution:**
*   **Redis-Backed State:** PostgreSQL row locks are too slow for concurrent generation limits. All export limits (`export_limits:{coach_id}`) and unique active users (`active_clients:{coach_id}:{month}`) are tracked in Redis using `HINCRBY` and `SADD` atomic operations.
*   **Stripe Usage API Synchronization:** A background Celery worker periodically synchronizes the Redis set counts with the Stripe Metered Usage API, ensuring the coach is automatically billed on their monthly anniversary without manual intervention.

### 4.2 FR-APR-04: Telegram Mini App UI/UX Platform
The existing CBCS relies on standard Telegram text and voice note chats. This is excellent for low-friction journaling but cannot support the interactive visual elements required for Trivianar or WebRTC. We are upgrading the delivery mechanism to the Telegram Mini App ecosystem.

**Business Rules:**
*   **The Invisible App:** Users still do not download anything from an App Store. They click a button in their Telegram chat, and a rich HTML5 Canvas application opens natively within the app shell.
*   **Zero Login Friction:** Users are authenticated automatically via Telegram's cryptographic payload. No passwords, no magic links.

**Technical Execution:**
*   **Next.js React Frontend:** A lightweight, high-performance DOM renderer tailored to the `Telegram.WebApp` SDK, automatically syncing with the user's native theme variables (Light/Dark mode).
*   **The WebSocket Paradigm:** We are banning Telegram webhooks for synchronous events. The React app establishes a persistent `wss://` WebSocket connection directly to a scalable FastAPI Transit Gateway. This reduces interaction latency from ~1200ms to ~40ms.
*   **Secure Handshake:** The WebSocket connection is authenticated using the HMAC-SHA-256 hash of the `window.Telegram.WebApp.initData` string, completely eliminating impersonation vectors.

---

## 5. Track B: Acquisition & Engagement Engines (Wave 2)

Once the foundation is secure, we deploy the engines responsible for top-of-funnel acquisition (getting coaches onto the platform) and deep engagement (keeping their clients addicted to the process).

### 5.1 FR-APR-03: Speaker Audit Engine
This is the automated acquisition machine designed to achieve an 80% close rate without a single human sales call.

**Business Rules:**
*   **Zero-Friction Intake:** The coach simply provides a link to an existing YouTube video or Instagram reel. No uploading required.
*   **The Audit Trap:** The system analyzes their performance, presenting them with objective, biometric flaws in their delivery (e.g., "Your interrupt frequency is 12% higher than the top 1% of speakers," "Your pacing drops significantly after the 40-second mark").
*   **The "Show Before Selling" Solution:** Alongside the critique, the engine automatically generates and presents the "Content Trinity" (A cinematic short, a carousel, and a meme) cut from their own footage, completely watermarked. 
*   **The Close:** To remove the watermarks and unlock the assets, they pay the frictionless $16.95 tripwire fee, which immediately upsells them into the $39.95/week Jim Rohn Voice Coach Engine to fix the flaws identified in the audit.

**Technical Execution:**
*   **Biometric Extraction:** Integration with Deepgram or local Whisper models to map Voice Activity Detection (VAD), calculating words-per-minute and conversational pacing over time.
*   **Automated Pipeline Trigger:** Kicks off the SVRE (Sovereign Visual Research Engine) pipeline to automatically process the video through the CMF (Content Trinity) generators.

### 5.2 FR-APR-02: 30-Day Challenge Funnel Engine
Attention is useless if it is not bounded into a cohort. The Challenge Funnel converts passive social media scrolling into active Telegram engagement.

**Business Rules:**
*   **Gamified Cohorts:** Users join a specific 30-day challenge (e.g., "The 30-Day Speaker Transformation").
*   **Daily Rituals:** The Telegram bot delivers automated daily prompts, tracking streaks and completion rates. 
*   **Psychological Gating:** Progression is not guaranteed. If a user fails to engage, the system does not passively let them stay. It triggers re-engagement warnings and, if ignored, kicks them from the active cohort to maintain tribe exclusivity and urgency.

**Technical Execution:**
*   **State Machine Progression:** Managed by the `AtlasRoadmap` agent, which tracks the user's day-by-day state, verifying completion conditions before unlocking the next day's payload.
*   **AFFiNE Visualization Sync:** Client progress (streaks, energy ratings) is visually rendered into Excalidraw charts and pushed to their secure AFFiNE dashboard (leveraging the FR-CA11-09 architecture).

### 5.3 FR-APR-05: WebRTC Roleplay Engine
The crown jewel of the Tier 2 offering. A synchronous, high-pressure environment for sales and communication training.

**Business Rules:**
*   **The 2-Human + 1-AI Room:** Two human participants engage in a live roleplay. An AI Moderator listens silently, only interrupting when conversational flow breaks (e.g., 6 seconds of dead air) or an objection is fumbled.
*   **Psychological Scarcity (The Energy Bar):** Sessions are brutally capped at 1440 seconds (24 minutes). When the timer expires, the room is destroyed immediately. This Zeigarnik Effect prevents burnout and forces participants to return the next day.

**Technical Execution:**
*   **Daily.co Bridging:** We leverage Daily.co's infrastructure for peer-to-peer WebRTC video/audio to ensure rock-solid performance.
*   **Pipecat / Modal.com:** The AI Moderator is a serverless Python `Pipecat` instance hosted on Modal.com for sub-1.5s cold boots. It routes the WebRTC audio stream through an Nvidia NIM STT -> local quantized LLaMa-3 context evaluator -> Riva TTS pipeline to achieve human-like (<800ms) conversational latency.

### 5.4 FR-APR-06: Interactive Trivianar
Webinars are dead; passive viewership leads to churn. The Trivianar is a mass-scale interactive debate and trivia event.

**Business Rules:**
*   **Mass Synchronization:** Up to 5,000 users answer psychological or coaching-related questions simultaneously. 
*   **Real-time Consequence:** The coach sees the aggregate answers instantly and can pivot the discussion based on the audience's actual beliefs, not just chat spam.

**Technical Execution:**
*   **Redis LPUSH Architecture:** PostgreSQL cannot handle 5,000 simultaneous UDP insert locks. When a user clicks an answer, the FastAPI WebSocket gateway drops the payload into a Redis `LPUSH` queue (~0.1ms latency). 
*   **Asynchronous Bulk Insert:** A Celery worker sweeps the Redis queue every 500ms, aggregates the results, broadcasts the updated state back to all WebSocket clients, and executes a single bulk insert into PostgreSQL for permanent storage.
