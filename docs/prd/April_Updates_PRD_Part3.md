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
