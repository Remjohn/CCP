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
