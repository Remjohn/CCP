# Product Requirements Document: April Updates — Sovereign Telegram Mini App Ecosystem

**Author:** John (BMAD PM Agent)
**Date:** 2026-05-02
**Target Scope:** 48-Hour Full Launch Architecture
**Status:** In Progress (Part 1)

---

## 1. Executive Summary

The Conscious Coaching Platform (CCP) is facing a critical inflection point. The R&D phase is over. We have successfully engineered the most psychologically advanced, agentic coaching infrastructure in the world—a system capable of synthesizing a coach's 3D Voice DNA, applying 4-Mood Psychological Routing, and generating visually stunning, neuro-calibrated assets through the JIT Skill Compiler. 

However, the platform currently lacks the commercial scaffolding required to survive. It is a zero-revenue engine burning computational resources. The "April Updates" represent the final, non-negotiable transition from theoretical capability to a commercial, B2B2C Sovereign Telegram Mini App Ecosystem. We are not launching a "Minimum Viable Product" (MVP); we are launching a complete, mathematically bounded, high-fidelity platform capable of generating immediate revenue through frictionless acquisition and metered usage.

The core objective of the April Updates is twofold:
1.  **Frictionless Acquisition (Show Before Selling):** Utilize our automated Content Trinity generation to prove undeniable value to coaches upfront, breaking through the "AI is a commodity" illusion.
2.  **Scaled Monetization (B2B2C):** Transition from flat-rate SaaS to a dynamic, user-metered billing architecture that monetizes the end-clients interacting with our coaches inside Telegram.

To achieve this, we are fundamentally altering the client interaction layer—moving away from brittle Telegram webhooks and purely asynchronous voice notes, into a high-performance, WebSocket-driven Next.js frontend operating inside the `Telegram.WebApp` shell. This enables synchronous, sub-second interactions (Interactive Trivianar) and WebRTC-bridged 1-on-1 sessions (The Roleplay Engine) while preserving the "Invisible App" paradigm.

---

## 2. Strategic Imperatives & The CBAR Framework

The April Updates are governed by the Constraint-Based Adversarial Reasoning (CBAR) pricing optimization experiment conducted in early April 2026. The economic context is brutal: AI editing tools are ubiquitous, trust in marketing agencies is zero, and traditional sales calls create fatal friction for our target demographic (Holistic and Transformation Coaches).

### 2.1 The "Show Before Selling" Mandate
Coaches believe content creation should be practically free. To combat this, we do not sell "content." We sell *Performance and Presence Training* via the Jim Rohn AI Voice Coach Engine. The actual content (Carousels/Shorts) is framed as the free, automatic byproduct of their training.

Furthermore, we bypass the need for portfolios or sales calls by scraping a coach's pre-existing public footage (YouTube/IG), running it through our Sovereign Visual Research Engine (SVRE), and delivering a watermarked "Content Trinity" (Cinematic Short, Branded Carousel, Meme) directly to their DMs. The proof is undeniable because it features their face, perfectly edited, before we ever ask for a dollar.

### 2.2 The Frictionless Tripwire Pricing Model
The pricing architecture is designed to capture market share through psychological continuity, utilizing the `.95` suffix to create seamless transitions across tiers.

1.  **The Tripwire ($16.95): The Broke-Test.** The coach pays $16.95 to unlock the un-watermarked Content Trinity we already produced for them. At $16.95, refusing to buy a world-class branded asset of yourself feels like choosing a "broke" identity. It bypasses rational comparison shopping.
2.  **Tier 1 ($39.95/Week): Voice Coach + Content.** The anchor tier. Provides weekly training sessions with the Jim Rohn Voice Engine, automatically cutting those sessions into 9 branded assets per week (3 Shorts, 3 Carousels, 3 Memes). Weekly billing reduces "SaaS Fatigue."
3.  **Tier 2 ($49.95/Week): Full Authority Engine.** For just $10 more per week, the coach unlocks the CCP Platform Access, Tier-List Reaction formats, and the right to onboard their own clients.

### 2.3 The B2B2C Metered Economy
The true revenue scale of the platform lies downstream. Once a coach reaches Tier 2, they invite their audience into their sovereign Telegram bot. The CCP tracks these active end-users (via Redis unique sets) and automatically bills the Coach **$3.90 per active user, per month**. The editing is the Trojan Horse; the B2B2C metering is the sovereign platform.

---

## 3. The 4-Track Feature Architecture (The 10 Updates)

To execute this commercial transition within 48 hours, the engineering effort is decomposed into 10 explicit Technical Specifications, grouped into 4 execution tracks. 

### Track A: The Revenue Core (Foundation)
The system must be able to securely handle money and enforce limits before any generative features are turned on. 

*   **FR-APR-01: B2B2C Metered Billing Architecture.** The Stripe integration. Relies on Redis hash tracking rather than PostgreSQL to enforce highly concurrent limits and accurately count unique active Telegram users for the $3.90/user surcharge.
*   **FR-APR-04: Telegram Mini App Platform.** The UI/UX foundation. A Next.js React application injected into the Telegram WebApp shell. Replaces HTTP polling with secure JWT-hashed WebSocket connections, dropping latency from 1200ms to 40ms.

### Track B: Acquisition & Engagement Engines
The features required to attract coaches and keep their end-users addicted to the platform.

*   **FR-APR-03: Speaker Audit Engine (Top of Funnel).** The automated acquisition machine. A biometric audit tool that analyzes a coach's raw video link, scores interrupt frequency and pacing, and presents them with the $16.95 Content Trinity solution.
*   **FR-APR-02: 30-Day Challenge Funnel Engine.** Converts raw social attention into bounded, gamified cohorts, moving audiences from passive observers to active participants.
*   **FR-APR-05: WebRTC Roleplay Engine.** A 2-Human + 1-AI (Moderator) synchronous environment built on Daily.co and Pipecat. Features a brutal 1440-second (24-minute) hard stop to enforce psychological scarcity.
*   **FR-APR-06: Interactive Trivianar.** Mass-scale live debate events supporting 5k+ concurrent users, utilizing Redis LPUSH queues to bypass Postgres row locks and WebSockets for sub-second DOM updates.

### Track C: Orchestration & Intelligence
Refining how the AI is controlled, ensuring we never fall back into unpredictable "black box" generation.

*   **FR-APR-08: The Orchestration Dichotomy.** A strict architectural rule: Unstructured LLM reasoning is moved entirely into DSPy/Pydantic bounded sub-agents. The core pipeline is governed by deterministic FastAPI logic, not AI instruction.
*   **FR-APR-07: Voice-First Orchestration Engine.** Moving beyond text generation to incorporate strict voice synthesis (Jim Rohn persona via Riva TTS), running parallel to the core loop.
*   **FR-APR-09: 28-Command Telegram Intelligence Suite.** Expanding the `InteractComp` boundary to support 28 explicit slash commands (e.g., `/tierlist`, `/audit`) in Telegram for immediate, frictionless workflow triggering.

### Track D: Platform Governance
*   **FR-APR-10: Content Trinity Maximum Export Limiter.** The mathematical enforcement of the B2B pricing. A strict ceiling (e.g., 4 exports/week). No overages, no "credit buying" loopholes. Controlled via Redis to prevent concurrent generation bypasses.
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
# Product Requirements Document: April Updates — Sovereign Telegram Mini App Ecosystem

**Status:** In Progress (Part 3)

---

## 6. Track C: Orchestration & Intelligence (Wave 3 Execution & Control)

With the acquisition and engagement engines operational, we must ensure the core intelligence layer remains perfectly predictable, deterministic, and free from unstructured LLM hallucinations.

### 6.1 FR-APR-08: The Orchestration Dichotomy
This is the most critical backend architectural shift in the April Updates. We are formally abandoning the "Agent Swarm" illusion where LLMs chat with each other to make system decisions.

**Business Rules:**
*   **Absolute Determinism:** The platform must execute perfectly 10,000 times out of 10,000. We cannot allow a stray LLM token generation to crash the pipeline or bill a client incorrectly.
*   **The Orchestration Split:** Control logic (routing, billing, state transitions) is explicitly divorced from generative logic (writing scripts, analyzing sentiment).

**Technical Execution:**
*   **FastAPI / Python Control:** The core loops, webhooks, and database queries are hard-coded in Python. 
*   **DSPy & Pydantic Boundaries:** Unstructured LLM reasoning is strictly bounded inside DSPy modules. The output of any LLM call must be forced into a strict Pydantic JSON schema before it is allowed back into the Python control loop. If the LLM hallucinates an invalid schema, the `TillDone` Pi Extension catches it and forces a retry, entirely isolated from the main system state.

### 6.2 FR-APR-07: Voice-First Orchestration Engine
Text-based generative outputs are becoming commoditized. The premium coaching experience demands voice.

**Business Rules:**
*   **The Jim Rohn Standard:** Output isn't just transcribed text; it is delivered with the prosody, pacing, and gravitas of a master orator. 
*   **Seamless Delivery:** Voice generation runs parallel to the core loop so that the user receives an audio response in Telegram without waiting 30 seconds for rendering.

**Technical Execution:**
*   **Riva TTS / ElevenLabs:** Integration with ultra-low-latency Text-to-Speech endpoints (e.g., Nvidia Riva for local hosting, ElevenLabs WebSocket API for premium tiers).
*   **Prosody Mapping:** The generation agents do not just output words; they output SSML (Speech Synthesis Markup Language) or proprietary pacing tags (e.g., `<pause duration="1.5s"/>`) derived from the Coach's 3D Voice DNA to ensure the AI speaks with the coach's exact emotional cadence.

### 6.3 FR-APR-09: 28-Command Telegram Intelligence Suite
The `InteractComp` boundary currently handles conversational intent. We need a faster, deterministic way for coaches to trigger exact platform functions without relying on the LLM to guess what they want.

**Business Rules:**
*   **Slash Command Dominance:** Coaches and users can type explicit commands (e.g., `/start_challenge`, `/audit_me`, `/billing_status`) directly into the Telegram bot to bypass conversation and instantly trigger an action.
*   **Frictionless Workflow Triggering:** Binds complex, multi-agent workflows to a single user action.

**Technical Execution:**
*   **Aiogram Routing Expansion:** The existing Telegram ingress router is updated to handle 28 specific `MessageHandlers` mapping directly to FastAPI endpoint triggers, completely bypassing the LangGraph reasoning engine for known, deterministic requests.

---

## 7. Track D: Platform Governance

### 7.1 FR-APR-10: Content Trinity Maximum Export Limiter
The architectural enforcer of the B2B2C business model. We do not sell compute; we sell value. 

**Business Rules:**
*   **The Absolute Ceiling:** The platform hard-caps a coach at 4 exports per week for any specific format (e.g., 4 Shorts, 4 Carousels), and an absolute global cap of 8 exports total across all formats.
*   **No Exceptions:** If a coach hits their limit, they cannot buy "more credits." They must upgrade their tier or wait until the weekly Sunday reset. This enforces discipline and prevents the platform from being treated as a spam generator.

**Technical Execution:**
*   **Redis `MULTI/EXEC` Blocks:** (Covered in FR-APR-01). The Limiter acts as the final gatekeeper before any SVRE (Visual Research) or CCF (Content Factory) pipeline executes. If the Redis `HINCRBY` transaction violates the limit, the pipeline returns an HTTP 429 and aborts instantly.

---

## 8. Development Timeline & The 48-Hour Execution Protocol

The transition from R&D to MVP requires ruthless prioritization. 

**Hour 0-12: Foundation (Track A)**
*   Deploy the Redis Limiters.
*   Wire the Stripe Webhooks.
*   Launch the Next.js Telegram Mini App shell with WebSocket handshake.

**Hour 12-24: Acquisition (Track B, Part 1)**
*   Deploy the Speaker Audit Engine (FR-APR-03) to open the top-of-funnel.
*   Deploy the 30-Day Challenge Funnel (FR-APR-02) to capture the inbound traffic.

**Hour 24-36: Engagement & Control (Track B, Part 2 & Track C)**
*   Stand up the Modal.com Pipecat instance for the WebRTC Roleplay Engine (FR-APR-05).
*   Implement the Trivianar Redis LPUSH queues (FR-APR-06).
*   Enforce the DSPy/Pydantic Orchestration Dichotomy boundaries (FR-APR-08).

**Hour 36-48: Polish & Governance (Track D & Remaining C)**
*   Activate the Voice-First TTS routing (FR-APR-07).
*   Map the 28 Telegram Slash Commands (FR-APR-09).
*   Strictly test the Maximum Export Limiter boundary conditions (FR-APR-10).
*   **Launch.**

---

*End of April Updates Technical Specification & Strategy Document.*
# Product Requirements Document: April Updates — Sovereign Telegram Mini App Ecosystem

**Status:** In Progress (Part 4 - Technical Deep Dive & Schemas)

---

## 9. Data Schemas & API Contracts

To ensure absolute determinism across the 48-hour launch, the data structures connecting the Next.js Mini App, the FastAPI Gateway, and the backend Supabase/Redis instances must be strictly defined. Ambiguity in these JSON structures will crash the JIT compiler.

### 9.1 The WebRTC Roleplay Biometric Payload (FR-APR-05)
When a 1440-second Roleplay session concludes, the Pipecat Modal instance does not merely send a text summary. It must inject a structured biometric analysis into the *existing* `cbcs_interaction_logs` table in Supabase. This ensures the CPSC (Sales Engine) can instantly read roleplay performance without requiring new database queries.

**Schema (JSONB format for `interaction_metadata` column):**
```json
{
  "module_type": "webRtc_roleplay",
  "room_id": "dl_x789_alpha",
  "duration_seconds": 1440,
  "termination_reason": "scarcity_timeout",
  "biometric_score": {
    "interrupt_frequency": 4,
    "wpm_average": 145,
    "mood_state_resonance_compliance": 0.88,
    "objection_handling_flag": "PASSED"
  },
  "opponent_id": "external_guest_55",
  "ai_moderator_interventions": 2
}
```

### 9.2 Trivianar Redis Fast-Queue Schema (FR-APR-06)
During a live Trivianar, 5,000 users clicking answers generates a massive UDP flood. The React Native Mini App sends this payload via WebSocket to FastAPI, which executes an `LPUSH` into Redis.

**Schema (WebSocket Payload -> Redis `LPUSH`):**
```json
{
  "event_type": "TRIVIANAR_SUBMISSION",
  "data": {
    "room_id": "tv_epoch_101",
    "question_id": "q_04",
    "user_id": "telegram_uid_998877",
    "selected_answer_id": "ans_b",
    "reaction_time_ms": 1204,
    "timestamp_utc": "2026-05-02T20:45:00Z"
  }
}
```
*Architecture Note:* A Celery worker (`trivianar_sweep.py`) pops these payloads every 500ms, calculates the aggregate percentages (e.g., "45% chose A, 55% chose B"), and broadcasts the updated `TRIVIANAR_STATE` back to the active WebSockets to trigger DOM re-renders in the Next.js shell.

### 9.3 Speaker Audit Output Specification (FR-APR-03)
The top-of-funnel acquisition engine must return a brutal, mathematically precise critique of the coach's video submission. 

**Schema (Audit Report Payload):**
```json
{
  "audit_id": "aud_001_sigma",
  "target_video_url": "https://youtube.com/watch?v=...",
  "biometric_analysis": {
    "filler_word_density_percent": 18.4,
    "pacing_decay_variance": "high",
    "eye_contact_break_frequency": 12
  },
  "psychological_routing_suggestion": "Escape Mode / Downward Comparison",
  "content_trinity_preview_urls": [
    "s3://ccp/previews/short_watermarked.mp4",
    "s3://ccp/previews/carousel_watermarked.pdf",
    "s3://ccp/previews/meme_watermarked.png"
  ],
  "tripwire_checkout_url": "https://pay.stripe.com/buy/..."
}
```

### 9.4 The 28-Command Slash Architecture (FR-APR-09)
The `InteractComp` agent boundary is expanded. Instead of relying purely on natural language understanding, users can trigger exact deterministic workflows using Telegram slash commands. The FastAPI router maps these directly to Celery tasks.

**Core Command Mapping Table:**
| Command | Caller | Action Triggered | Latency Target |
|---|---|---|---|
| `/start_challenge` | Client | Initializes FR-APR-02 state machine for the user. | < 200ms |
| `/audit_me [url]` | Coach | Kicks off FR-APR-03 biometric video analysis. | < 500ms (Async Return) |
| `/trivianar_join` | Client | Opens Next.js WebApp, establishes WS handshake. | < 100ms |
| `/roleplay_init` | Coach | Boots the Modal.com Pipecat instance, creates Daily.co room. | < 1500ms |
| `/billing_status` | Coach | Queries Stripe API + Redis limits, returns current usage. | < 300ms |
| `/export_trinity` | Coach | Fires FR-APR-10 limits check. If passed, triggers generation. | < 400ms |

### 9.5 The Redis Export Limiter Architecture (FR-APR-01 & FR-APR-10)
To enforce the "No Credit Loopholes" rule, the export limiter must be atomically secure.

**Redis Keyspace Structure:**
*   `export_limits:{coach_id}:{iso_week}` -> **Hash** (Tracks the 4/week limit per format).
*   `active_clients:{coach_id}:{iso_month}` -> **Set** (Tracks unique Telegram IDs for the $3.90/user B2B2C charge).
*   `trivianar_state:{room_id}` -> **JSON** (Holds the current question, timer, and aggregate answers for the live game).

**The HINCRBY Transaction Block (`redis_limits.py`):**
Whenever a coach requests a visual asset or script export, FastAPI executes the following Lua script or `MULTI/EXEC` block:
```python
async def check_and_increment_limit(coach_id: str, format_type: str) -> bool:
    # 1. WATCH the key to prevent race conditions
    # 2. HGET total_weekly_count
    # 3. HGET {format_type}
    # 4. IF total >= 8 OR format >= 4 -> UNWATCH, Return False
    # 5. MULTI
    # 6. HINCRBY total_weekly_count 1
    # 7. HINCRBY {format_type} 1
    # 8. EXEC -> Return True
```

### 9.6 DSPy & Pydantic Boundaries (FR-APR-08)
To prevent the "Statistical Centroid Failure," LLMs must not make routing decisions. They must only execute defined tasks and return structured data.

**The DSPy Signature Example (For generating a Meme Hook):**
```python
import dspy
from pydantic import BaseModel, Field

class MemeHookSchema(BaseModel):
    setup_text: str = Field(max_length=40)
    punchline_text: str = Field(max_length=30)
    v_code: str = Field(description="Violation Type (V1-V4)")
    r_code: str = Field(description="Resolution Domain (R1-R3)")

class GenerateMemeHook(dspy.Signature):
    """Generates a concise, psychologically targeted meme hook based on the active Context Premise."""
    context_premise = dspy.InputField()
    target_mood_state = dspy.InputField()
    
    # The output MUST conform to the Pydantic schema
    output: MemeHookSchema = dspy.OutputField()
```
*Architectural Law:* If the `output` does not pass Pydantic validation, the DSPy `Assert` framework forces the LLM to retry up to 3 times with the validation error appended to the prompt. If it fails 3 times, the pipeline throws a `PydanticValidationError` and triggers the `DamageControl` Pi Extension, rather than passing hallucinated data to the next step.
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
