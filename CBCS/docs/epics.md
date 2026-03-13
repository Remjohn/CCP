# CBCS - Epic Breakdown

**Author:** Emilio
**Date:** 2025-12-02
**Project Level:** MVP
**Target Scale:** 10,000 Users

---

## Overview

This document provides the complete epic and story breakdown for the **Conscious Behavioral Change System (CBCS)**, decomposing the requirements from the [PRD](./prd/index.md) into implementable stories. It integrates the technical decisions from the [Architecture Document](./architecture/index.md) to ensure every story is implementation-ready.

**Living Document Notice:** This is the initial version. It will be updated after UX Design and Architecture workflows add interaction and technical details to stories.

### Epics Summary
The development roadmap is structured around thirteen sequential Epics, mimicking the biological evolution of a digital organism:

1.  **Epic 1: The Nervous System (Ingress & Cognitive Pipeline)** - Establishing the event-driven backbone (FastAPI, Redis, LangGraph).
2.  **Epic 2: The Senses & Memory (Noise Detector & Graph)** - Building the assessment engine and Context Premise map (Neo4j).
3.  **Epic 3: The Soul & Logic (Intelligence Library)** - Implementing the static psychological kernel (YAML Configuration).
4.  **Epic 4: The Brain (Neuro-Persuasion Engine)** - Activating the reasoning agents (Assembler, Artisan) and strategy logic.
5.  **Epic 5: The Voice (Generative Media Layer)** - Enabling high-fidelity audio synthesis (IndexTTS-2) and delivery.
6.  **Epic 6: The Awareness (Research & Relevance)** - Connecting the system to the external world (Maeva, Lionel).
7.  **Epic 7: The Control (Coach Dashboard)** - Building the "Master Composer" interface for the coach.
8.  **Epic 8: The Survival (Economics & Security)** - Implementing payments, cost controls, and privacy/safety protocols.

> **CCP Integration (Feb 2026):** The following epics extend CBCS into the **Conscious Coach Platform (CCP)**, unifying CCF + CMF + CBCS.

9.  **Epic 9: The Coach Role System (Identity & Routing)** ✅ - Role-based routing at Ingress, Coach LangGraph subgraph, Supabase migration.
10. **Epic 10: The Scheduler (Proactive Intelligence)** - APScheduler for automated weekly coach rhythm.
11. **Epic 11: The Bridge (CCF/CMF CLI Integration)** ⏳ - CLI Session Runner, pipeline sequencing, automated content pipelines.
12. **Epic 12: The Evolution (CBCS Protocol Upgrade)** - Rewriting agent protocols to CCF/CMF SKILL.md quality standard.
13. **Epic 13: The Colony (Per-Coach Cloning & Deployment)** - Docker Compose isolation, per-coach intelligence libraries.


---

## Functional Requirements Inventory

| ID | Requirement Name | Description |
| :--- | :--- | :--- |
| **FR 1.1** | Intelligence Repository Structure | File-based repository for YAML/JSON configuration (Identity Pillars, TTT Matrix, Persuasion Layers). |
| **FR 1.2** | Runtime Injection | Pydantic AI injection of configuration files into agent dependency contexts. |
| **FR 2.1** | Setup Agents (Coach Onboarding) | Agents (Kimya, Valeriane, Dilaya) to extract Coach's methodology and Tribe's soul data. |
| **FR 2.2** | User Assessment (Soul Data Mapping) | Web-based psychometric intake to map the 12-dimensional Context Premise into Neo4j. |
| **FR 2.3** | Atlas (Program Architect) | Agent to dynamically assemble a 30-day ritual roadmap based on Capacity and Identity. |
| **FR 3.1** | The Assembler (Strategist) | Agent to select the optimal strategy (Ritual, Persuasion Layer, Story Formula) from the Pantry. |
| **FR 3.2** | 4-Dimensional Component Logic | Logic to adapt rituals based on Level, Identity Fit, Goal Fit, and Implementation. |
| **FR 3.3** | 9 Layers of Persuasion | Implementation of the 9 specific persuasion logic structures (e.g., The Challenger). |
| **FR 3.4** | The Artisan (Copywriter) | Agent to generate text scripts using MiniMax-M2, adhering to TTT syntax rules. |
| **FR 4.1** | Maeva (Social Researcher) | Agent to scan social media for tribe sentiment and generate reports. |
| **FR 4.2** | Lionel (Deep Researcher) | Agent to conduct deep research on themes using Google Search/Tavily. |
| **FR 4.3** | Relevance Injection | Logic to prioritize research inputs and override standard curriculum with current events. |
| **FR 5.1** | Adaptive Primer (Morning Loop) | Delivery of "Vision Implant" audio at 08:00 AM with specific TTT modulation. |
| **FR 5.2** | Evidence Capture (Voice Journaling) | Transcription (Groq) and analysis (Aria) of user voice notes to update the graph. |
| **FR 5.3** | Evening Reflection Loop | Logic to handle ritual completion (Confirmation Bias) or failure (Compassionate Retrieval). |
| **FR 6.1** | The Pantry (Component Manager) | Dashboard interface for tagging and managing rituals (4-Dimensional Tags). |
| **FR 6.2** | Cohort Vibe Visualization | Dashboard visualization (Word Cloud) of aggregate client sentiment. |
| **FR 7.1** | Stripe Connect Integration | Automated split payments ($95 Coach / $5 Platform) and provisioning. |
| **FR 7.2** | Cost Circuit Breaker | Monitoring of token/GPU usage via Langfuse and enforcement of Economy Mode. |
| **FR 7.3** | Glass Wall Privacy | Encryption of audio, ephemeral processing, and PII redaction before graph storage. |

---

## FR Coverage Map

*See end of document for detailed matrix.*

---

## Epic Structure Plan

### Epic 1: The Nervous System (Ingress & Cognitive Pipeline)
*   **User Value:** As a user, I can send messages to the bot and get an immediate "listening" status, ensuring I feel heard even before the AI replies.
*   **PRD Coverage:** FR 5.1 (Adaptive Primer), FR 5.2 (Evidence Capture).
*   **Technical Context:** FastAPI Webhooks, Redis Listening Window, LangGraph State Machine, Groq Transcription.
*   **Dependencies:** None (Foundation).

### Epic 2: The Senses & Memory (Noise Detector & Graph)
*   **User Value:** As a user, I can complete an assessment that feels deeply personal, and the system "remembers" my specific fears and dreams in future conversations.
*   **PRD Coverage:** FR 2.1 (Setup Agents), FR 2.2 (User Assessment), FR 5.2 (Evidence Capture).
*   **Technical Context:** Neo4j Graph Schema, Pydantic AI Entity Extraction, Next.js Assessment Form.
*   **Dependencies:** Epic 1 (Ingress).

### Epic 3: The Soul & Logic (Intelligence Library)
*   **User Value:** As a coach, I can define my methodology (Archetypes, Voice) once, and trust the AI will never deviate from it.
*   **PRD Coverage:** FR 1.1 (Repo Structure), FR 1.2 (Runtime Injection).
*   **Technical Context:** YAML Configuration Files, Pydantic Dependency Injection.
*   **Dependencies:** Epic 1 (Core Pipeline).

### Epic 4: The Brain (Neuro-Persuasion Engine)
*   **User Value:** As a user, I receive advice that is perfectly timed and tailored to my specific psychological state (e.g., "Tough Love" when I'm stuck).
*   **PRD Coverage:** FR 3.1 (Assembler), FR 3.2 (4D Logic), FR 3.3 (Persuasion Layers), FR 3.4 (Artisan).
*   **Technical Context:** MiniMax-M2 Chain of Thought, Strategy Objects, Story Formulas.
*   **Dependencies:** Epic 2 (Graph), Epic 3 (Library).

### Epic 5: The Voice (Generative Media Layer)
*   **User Value:** As a user, I hear my coach's actual voice (cloned) speaking to me with genuine emotion, making the advice feel real.
*   **PRD Coverage:** FR 5.1 (Adaptive Primer), FR 5.3 (Reflection Loop).
*   **Technical Context:** IndexTTS-2 on Runpod, TTT Modulation, Async Delivery Queue.
*   **Dependencies:** Epic 4 (Script Generation).

### Epic 6: The Awareness (Research & Relevance)
*   **User Value:** As a user, the AI references current events and my specific "Tribe" culture, so it doesn't feel like a generic bot.
*   **PRD Coverage:** FR 4.1 (Maeva), FR 4.2 (Lionel), FR 4.3 (Relevance Injection).
*   **Technical Context:** Tavily API, Google Search API, Weekly Research Loop.
*   **Dependencies:** Epic 4 (Assembler Integration).

### Epic 7: The Control (Coach Dashboard)
*   **User Value:** As a coach, I can see the "Vibe" of my entire cohort at a glance and intervene manually if someone is struggling.
*   **PRD Coverage:** FR 6.1 (Pantry), FR 6.2 (Cohort Vibe).
*   **Technical Context:** Next.js Dashboard, D3.js Visualization, Supabase Realtime.
*   **Dependencies:** Epic 2 (Graph Data).

### Epic 8: The Survival (Economics & Security)
*   **User Value:** As a business, I can scale to 10k users without going bankrupt or leaking data.
*   **PRD Coverage:** FR 7.1 (Stripe), FR 7.2 (Circuit Breaker), FR 7.3 (Privacy).
*   **Technical Context:** Stripe Connect, Langfuse, RLS, Encryption.
*   **Dependencies:** Epic 1 (Auth), Epic 5 (Cost Drivers).

---

## Epic 1: The Nervous System (Ingress & Cognitive Pipeline)

**Goal:** To establish the fundamental ability of the system to "Hear," "Transcribe," and "Think" within the constraints of a real-time chat interface. This Epic focuses on the **FastAPI** webhook architecture, the **Redis** "Listening Window," and the structured reasoning engine.

### Story 1.1: The High-Concurrency Telegram Webhook

As a System,
I want to receive high-volume messages from Telegram via a webhook endpoint that immediately acknowledges receipt,
So that I do not trigger Telegram's retry logic while processing heavy AI workloads.

**Acceptance Criteria:**

**Given** a POST request from the Telegram Bot API
**When** the request arrives at `/webhooks/telegram`
**Then** the system must cryptographically verify the `X-Telegram-Bot-Api-Secret-Token` header against the environment variable.
**And** if valid, it must return a `200 OK` status code within **200ms**.
**And** the payload processing (parsing, routing) must be spawned as a **FastAPI BackgroundTask**.
**And** invalid signatures must return `403 Forbidden`.

**Technical Notes:**
*   **Architecture:** Ingress Layer (FastAPI).
*   **Constraint:** The "200ms Rule" is critical to prevent "Ghost Loops."
*   **Implementation:** Use `fastapi.BackgroundTasks` to offload logic.

### Story 1.2: The "Listening Window" Buffer (Redis)

As a Client,
I want to be able to send five rapid-fire messages (a "stream of consciousness") without the bot interrupting me after the first sentence,
So that I feel heard rather than managed.

**Acceptance Criteria:**

**Given** a new message arrives from `user_id`
**When** the user is in the `Listening` state
**Then** the message payload is appended to a **Redis List** key `buffer:{user_id}`.
**And** a "Silence Timer" is set/reset for **90 seconds**.
**And** the system sends a "Typing..." action to Telegram every 4 seconds.
**And** the generative pipeline is ONLY triggered when the timer expires OR the buffer hits a hard limit (e.g., 5 minutes).

**Technical Notes:**
*   **Architecture:** Redis Buffering Layer.
*   **Logic:** Implement a "Debounce" pattern using Redis Keyspace Notifications or a Celery/Arq worker.

### Story 1.3: LangGraph State Machine Initialization

As a Developer,
I want a persistent state machine that tracks where the user is in their journey (Sleep, Priming, Active),
So that the system can handle multi-turn conversations and long-running workflows.

**Acceptance Criteria:**

**Given** a user interaction
**When** the system initializes
**Then** it must load the user's state from **Supabase** (checkpoints).
**And** the **LangGraph** definition must support cyclic transitions: `Sleep -> Priming -> Listening -> Analyzing -> Strategizing -> Speaking -> Sleep`.
**And** it must support "Interrupts" for Human-in-the-Loop overrides (Crisis Mode).

**Technical Notes:**
*   **Architecture:** Cognitive Core (LangGraph).
*   **Persistence:** Use `AsyncPostgresSaver` with Supabase.

### Story 1.4: Pydantic AI Agent Foundation

As a Developer,
I want a base Agent class that enforces strict schema validation on all LLM outputs,
So that the system never hallucinates invalid JSON or dangerous advice.

**Acceptance Criteria:**

**Given** an agent request (e.g., "Select Strategy")
**When** the LLM generates a response
**Then** **Pydantic AI** must validate the output against a specific Pydantic Model (e.g., `InterventionStrategy`).
**And** if validation fails, it must automatically retry with an error prompt up to 3 times.
**And** the agent must have the **Intelligence Library** injected into its dependency context.

**Technical Notes:**
*   **Architecture:** Cognitive Core (Pydantic AI).
*   **Model:** MiniMax-M2 via API.

### Story 1.5: Long-Audio Transcription via Groq

As a Client,
I want to send a 15-minute voice note venting about my day,
So that I can process my emotions without hitting file size limits or waiting minutes for a reply.

**Acceptance Criteria:**

**Given** a voice note (OGG/OPUS) from Telegram
**When** the file is received
**Then** the binary stream is piped directly to **Groq API** (Whisper Large v3).
**And** the transcription completes in under **5 seconds** for a 10-minute file.
**And** the raw transcript is returned to the pipeline.
**And** the audio data is wiped from memory (Ephemeral Processing).

**Technical Notes:**
*   **Architecture:** Perception Engine (Groq).
*   **Privacy:** No disk writes for raw audio in this step.

---

## Epic 2: The Senses & Memory (Noise Detector & Graph)

**Goal:** To build the "Memory" of the system. This Epic focuses on the Assessment Engine and the **Neo4j** integration that maps the **Context Premise**.

### Story 2.0: Coach Onboarding & Soul Extraction

As a System,
I want to ingest the Coach's historical content and business model,
So that I can clone their genius and speak with their voice.

**Acceptance Criteria:**

**Given** a set of Coach assets (Videos, Emails)
**When** the onboarding pipeline runs
**Then** **Kimya** must extract the "Unique Mechanism" and "Promise".
**And** **Valeriane** must analyze the content to build `client_soul.json` (Metaphors, TTT Baseline).
**And** **Dilaya** must scrape the target audience's digital footprint to build `tribe_soul.json`.
**And** these profiles must be stored in the Intelligence Library.

**Technical Notes:**
*   **Architecture:** Setup Agents.
*   **Output:** JSON Configuration Files.

### Story 2.1: The Baseline Assessment Web App

As a User,
I want to complete a deep psychological intake via a frictionless web interface,
So that the system understands my specific context and constraints.

**Acceptance Criteria:**

**Given** a unique tokenized link sent in Telegram
**When** the user accesses the web form (Next.js)
**Then** the form must capture the 12 dimensions of the **Context Premise** (Frustrations, Wants, Dreams, Fears, etc.).
**And** upon submission, the system must calculate the `Capacity_Score` (0-100).
**And** the system must identify the dominant **Identity Pillar** based on linguistic patterns.
**And** the data must be stored in **Supabase** (User Profile) and **Neo4j** (Graph Nodes).

**Technical Notes:**
*   **Architecture:** Next.js Frontend + Supabase Backend.
*   **Integration:** Trigger Neo4j ingestion on form submit.

### Story 2.2: Context Premise Graph Construction

As a System,
I want to parse assessment data into a graph structure,
So that the Agent can query specific relationships between the user and their psychological blockers.

**Acceptance Criteria:**

**Given** raw text input from the assessment
**When** the ingestion process runs
**Then** **Aria (The Synthesizer)** must parse the text into Nodes and Edges.
**And** it must create `(User)-[:FIGHTS_AGAINST]->(Enemy)` relationships.
**And** it must create `(User)-[:CRAVES]->(Dream)` relationships.
**And** the graph schema must support all 12 Context Premise dimensions.

**Technical Notes:**
*   **Architecture:** Neo4j Graph Database.
*   **Logic:** Use Pydantic AI for Entity Extraction before Cypher insertion.

### Story 2.3: The Voice Journaling Extraction Pipeline

As a System,
I want to extract structured data from unstructured daily voice journals,
So that the psychological map evolves over time as the user changes.

**Acceptance Criteria:**

**Given** a daily journal transcript from Groq
**When** **Aria** analyzes the text
**Then** she must identify new entities (e.g., "I felt strong" -> Identity Signal).
**And** she must identify **Context Shifts** (e.g., "Not scared of boss" -> Decrease Fear Intensity).
**And** she must update the **Neo4j** graph properties (e.g., `intensity` score on Edges).
**And** this updated data must be available for **The Assembler** immediately.

**Technical Notes:**
*   **Architecture:** Agentic Pipeline (Phase 1).
*   **Model:** MiniMax-M2 for semantic analysis.

---

## Epic 3: The Soul & Logic (Intelligence Library)

**Goal:** To define the static psychological laws that govern the system. This prevents the AI from hallucinating its own coaching methodology.

### Story 3.1: The Library File System

As a Developer,
I want a centralized repository of YAML configuration files,
So that I can update the coaching methodology without deploying new code.

**Acceptance Criteria:**

**Given** the `/backend/intelligence_library/` directory
**When** the application starts
**Then** it must validate the existence and schema of:
*   `identity_pillars.yaml` (7 Archetypes)
*   `ttt_matrix.yaml` (9 Voice Levels)
*   `persuasion_layers.yaml` (9 Strategies)
*   `story_formulas.yaml` (16 Narrative Structures)
*   `context_premise_map.json` (12 Dimensions)

**Technical Notes:**
*   **Architecture:** Static Configuration.
*   **Validation:** Use Pydantic models to validate YAML structure on startup.

### Story 3.2: Runtime Injection via Pydantic AI

As a System,
I want to inject these configuration files into the Agent's dependency context at runtime,
So that the LLM is constrained by the specific definitions of the Intelligence Library.

**Acceptance Criteria:**

**Given** an agent instantiation (e.g., The Assembler)
**When** the agent is called
**Then** the `AgentDeps` object must contain the parsed content of the Intelligence Library.
**And** the System Prompt must explicitly reference these files (e.g., "Consult the persuasion_layers...").
**And** the Agent must fail to start if dependencies are missing.

**Technical Notes:**
*   **Architecture:** Pydantic AI Dependency Injection.
*   **Security:** Ensure prompt injection cannot override these constraints.

---

## Epic 4: The Brain (Neuro-Persuasion Engine)

**Goal:** To build the "Brain" that decides *how* to speak to the user. This Epic focuses on **The Assembler** (Strategist) and **The Artisan** (Copywriter).

### Story 4.1: The Dynamic Assembler (Lego Block Selection)

As a System,
I want to select the correct "Ritual Variant" based on the user's real-time state,
So that I never assign a task that is too hard (Burnout) or too easy (Boredom).

**Acceptance Criteria:**

**Given** a user state (Capacity, Identity, Pain Point)
**When** **The Assembler** runs its strategy loop
**Then** it must query **Supabase** and **Neo4j** to find the optimal Ritual.
**And** it must apply **Hue 1 (Capacity)**: If Capacity < 30, force "Micro-Habit".
**And** it must apply **Hue 2 (Identity)**: Match Identity Pillar to Voice Wrapper.
**And** it must apply **Hue 3 (Goal)**: Match Primary Pain to Goal Fit.
**And** the output must be a single `InterventionStrategy` object.

**Technical Notes:**
*   **Architecture:** The Assembler Agent.
*   **Logic:** Multi-stage filtering query.

### Story 4.2: The Story Insight Formula Synthesis

As a System,
I want to construct the "Vision Implant" script using proven persuasion architecture,
So that the message triggers "Hot Cognition."

**Acceptance Criteria:**

**Given** an `InterventionStrategy`
**When** **The Assembler** selects the narrative structure
**Then** it must choose one of the **16 Story Insight Formulas** based on the Context Premise.
**And** it must inject specific nouns from Neo4j into the formula slots (e.g., `[Enemy]` -> "The Corporate Grind").
**And** the generated script structure must follow: Validation -> Bias Trigger -> Vision Implant.

**Technical Notes:**
*   **Architecture:** The Assembler + Neo4j.
*   **Data:** `story_formulas.yaml`.

### Story 4.3: The "Challenger" Logic Implementation

As a Coach,
I want the AI to use Reverse Psychology on rebellious users,
So that I can bypass their resistance to authority.

**Acceptance Criteria:**

**Given** the user is a "Rebel" and is "Stuck"
**When** **The Assembler** selects the **"Challenger"** persuasion layer
**Then** **The Artisan** must generate a script using **Reverse Psychology**.
**And** it MUST NOT say "I bet you can't."
**And** it MUST say: "Maybe you are comfortable letting [Enemy] win..."
**And** it must enforce **TTT-08 (Raw Confrontation)** syntax (short sentences, zero hedging).

**Technical Notes:**
*   **Architecture:** The Artisan Agent.
*   **Prompting:** Few-shot prompting with negative constraints.

---

## Epic 5: The Voice (Generative Media Layer)

**Goal:** To establish the "Mouth" of the system. This Epic focuses on high-fidelity voice synthesis and the **"Vision Implant"** delivery.

### Story 5.1: IndexTTS-2 Host Configuration (Runpod)

As a Coach,
I want the AI to speak with my exact prosody and breathiness,
So that the client suspends disbelief and feels they are talking to me.

**Acceptance Criteria:**

**Given** a text script and a TTT Style Parameter
**When** the request is sent to the Runpod inference endpoint
**Then** the system must load the Coach's cloned voice weights.
**And** it must modulate the audio based on TTT:
*   **TTT-02:** Speed 0.85x, Breathiness High.
*   **TTT-08:** Speed 1.1x, Breathiness Low.
**And** it must return a high-fidelity WAV/MP3 file.

**Technical Notes:**
*   **Architecture:** IndexTTS-2 (Self-Hosted).
*   **Infrastructure:** Runpod Serverless GPU.

### Story 5.2: The "Keep-Warm" Scheduler

As a User,
I want the voice note to arrive quickly after I see the "Recording..." status,
So that the interaction feels conversational.

**Acceptance Criteria:**

**Given** the "Peak Window" (07:00 AM - 10:00 AM Client Time)
**When** the scheduler runs
**Then** it must ping the GPU endpoint every **4 minutes**.
**And** this must prevent the container from spinning down (Cold Start avoidance).
**And** latency for generation must remain under **15 seconds**.

**Technical Notes:**
*   **Architecture:** Cron Job / Celery Beat.
*   **Cost:** Balance keep-warm costs vs. latency requirements.

### Story 5.3: The Instruction Block Delay Queue

As a Client,
I want to listen to the emotional support message before I see the logistical task,
So that I don't feel overwhelmed by a "To-Do" list immediately.

**Acceptance Criteria:**

**Given** a generated Voice Note and an Instruction Block (Text)
**When** the delivery sequence begins
**Then** the system must send the Voice Note first.
**And** it must wait exactly **3000ms** (3 seconds).
**And** then it must send the Instruction Block.
**And** this delay must be managed by a reliable queue (Redis/BullMQ).

**Technical Notes:**
*   **Architecture:** Redis Delay Queue.
*   **Psychology:** Availability Heuristic enforcement.

### Story 5.4: The Evening Reflection Loop

As a System,
I want to check if the user completed their ritual and respond appropriately,
So that I can reinforce success or remove shame from failure.

**Acceptance Criteria:**

**Given** the 07:00 PM trigger
**When** the system checks `ritual_completion_status`
**Then** IF complete: **The Artisan** generates a "Confirmation Bias" message.
**And** IF incomplete: **Liliane (Empathy Agent)** generates a "Compassionate Retrieval" message.
**And** Liliane must use the "Justify Past Failures" persuasion layer to extract the Reason for Failure (RFF).

**Technical Notes:**
*   **Architecture:** Daily Cybernetic Loop (State 4).
*   **Logic:** Conditional branching in LangGraph.

---

## Epic 6: The Awareness (Research & Relevance)

**Goal:** To ensure the system feels "Alive" and culturally plugged-in.

### Story 6.1: The Social Researcher (Maeva)

As a System,
I want to know what my Soul Tribe is talking about this week,
So that I can reference it in my coaching.

**Acceptance Criteria:**

**Given** a list of sources in `tribe_soul.json`
**When** **Maeva** runs her weekly scan
**Then** she must scrape specific subreddits and forums.
**And** she must output a "Sentiment Report" identifying the top 3 emotional themes.
**And** this report must be stored in the Intelligence Library for the week.

**Technical Notes:**
*   **Architecture:** Research Engine (Maeva).
*   **Tools:** Tavily API, Reddit API.

### Story 6.2: The Deep Researcher (Lionel)

As a Coach,
I want the AI to use deep facts and history to support its advice,
So that I sound like an expert, not a cheerleader.

**Acceptance Criteria:**

**Given** a "Theme of the Week"
**When** **Lionel** runs his deep dive
**Then** he must execute searches across the **7 Planning Dimensions** (Historical, Contrarian, Scientific, etc.).
**And** he must produce a "Fact Bank" with citations.
**And** this data must be available to **The Artisan**.

**Technical Notes:**
*   **Architecture:** Research Engine (Lionel).
*   **Tools:** Google Search API.

### Story 6.3: Relevance Injection Logic

As a System,
I want to override the standard curriculum when a major event occurs,
So that I don't seem tone-deaf to the user's reality.

**Acceptance Criteria:**

**Given** a "Zeitgeist Context Object" from Maeva/Lionel
**When** **The Assembler** generates the daily strategy
**Then** it must check the relevance threshold of current events.
**And** if high relevance (e.g., Market Crash), it must swap the standard Ritual for a "Crisis Management" intervention.
**And** it must reference the specific event in the script.

**Technical Notes:**
*   **Architecture:** Relevance Loop.
*   **Logic:** Priority Queue in LangGraph.

---

## Epic 7: The Control (Coach Dashboard)

**Goal:** To provide the Coach with the "Pantry" to store ingredients and the "Lens" to view the cohort.

### Story 7.1: The Component Pantry UI

As a Coach,
I want to upload and tag ritual content easily,
So that the AI knows when to use it for specific user types.

**Acceptance Criteria:**

**Given** the Coach Dashboard
**When** the Coach uploads a video/audio file
**Then** the system must prompt for **4-Dimensional Tags** (Level, Identity Fit, Goal Fit).
**And** the file must be stored in **Supabase Storage**.
**And** the metadata must be saved to the `ritual_library` table.
**And** the system must warn if "Gaps" exist in the pantry coverage.

**Technical Notes:**
*   **Architecture:** Next.js Dashboard.
*   **UX:** Drag-and-drop interface.

### Story 7.2: The "Cohort Vibe" Word Cloud

As a Coach,
I want to see the aggregate mood of my clients,
So that I can intuitively understand the group's energy without reading 500 transcripts.

**Acceptance Criteria:**

**Given** the dashboard home screen
**When** the page loads
**Then** the system must query **Neo4j** for the last 24 hours of client journals.
**And** it must extract high-frequency emotional keywords.
**And** it must render a **Word Cloud** (D3.js).
**And** clicking a word must filter the client list.

**Technical Notes:**
*   **Architecture:** Pydantic AI Analysis + D3.js.
*   **Performance:** Cache the aggregation result.

### Story 7.3: Atlas (The Program Architect)

As a System,
I want to automatically build a 30-day schedule for a new user,
So that the Coach doesn't have to manually assign 30 videos.

**Acceptance Criteria:**

**Given** a new user with `Capacity_Score` and `Identity_Pillar`
**When** **Atlas** activates
**Then** it must traverse the **Pantry** to select a sequence of 30 rituals.
**And** IF Capacity is Low: Week 1 = "Micro-Habits".
**And** IF Capacity is High: Week 1 = "Standard".
**And** the schedule must be saved to `user_program` table in Supabase.

**Technical Notes:**
*   **Architecture:** Atlas Agent.
*   **Algorithm:** Deterministic selection logic.

---

## Epic 8: The Survival (Economics & Security)

**Goal:** To ensure the business model works and the data is safe.

### Story 8.1: Stripe Connect Split Payments

As a Platform,
I want to automatically take $5.00 from every client subscription,
So that I can pay for the GPU costs without invoicing the Coach manually.

**Acceptance Criteria:**

**Given** a user purchase
**When** the payment is processed via **Stripe Connect**
**Then** the transaction must be a Destination Charge.
**And** $95 must go to the Coach, $5 to the Platform.
**And** the `payment_intent.succeeded` webhook must trigger user provisioning.

**Technical Notes:**
*   **Architecture:** Economic Layer.
*   **Integration:** Stripe API.

### Story 8.2: Cost Circuit Breaker (Langfuse)

As a Business,
I want to limit the AI usage of "Power Users" who chat excessively,
So that they don't erode the profit margin.

**Acceptance Criteria:**

**Given** a user interaction
**When** the system processes the request
**Then** **Langfuse** must track the cumulative cost (Tokens + GPU).
**And** IF cost > $4.00/month: Transition user to `Economy_Mode`.
**And** `Economy_Mode` must bypass IndexTTS-2 (Text Only).

**Technical Notes:**
*   **Architecture:** Langfuse Monitoring.
*   **Logic:** Middleware check.



---

## FR Coverage Matrix

| FR ID | Requirement Name | Covered By Story |
| :--- | :--- | :--- |
| **FR 1.1** | Intelligence Repository Structure | Story 3.1 |
| **FR 1.2** | Runtime Injection | Story 3.2 |
| **FR 2.1** | Setup Agents (Coach Onboarding) | Story 2.0 |
| **FR 2.2** | User Assessment (Soul Data Mapping) | Story 2.1 |
| **FR 2.3** | Atlas (Program Architect) | Story 7.3 |
| **FR 3.1** | The Assembler (Strategist) | Story 4.1 |
| **FR 3.2** | 4-Dimensional Component Logic | Story 4.1 |
| **FR 3.3** | 9 Layers of Persuasion | Story 4.3 |
| **FR 3.4** | The Artisan (Copywriter) | Story 4.3 |
| **FR 4.1** | Maeva (Social Researcher) | Story 6.1 |
| **FR 4.2** | Lionel (Deep Researcher) | Story 6.2 |
| **FR 4.3** | Relevance Injection | Story 6.3 |
| **FR 5.1** | Adaptive Primer (Morning Loop) | Story 5.1, 5.3 |
| **FR 5.2** | Evidence Capture (Voice Journaling) | Story 1.5, 2.3 |
| **FR 5.3** | Evening Reflection Loop | Story 5.4 |
| **FR 6.1** | The Pantry (Component Manager) | Story 7.1 |
| **FR 6.2** | Cohort Vibe Visualization | Story 7.2 |
| **FR 7.1** | Stripe Connect Integration | Story 8.1 |
| **FR 7.2** | Cost Circuit Breaker | Story 8.2 |
| **FR 7.3** | Glass Wall Privacy | Story 8.3 |

---

---

# CCP Integration Epics (9–13)

> **Context:** In February 2026, the CBCS backend was selected (via Multi-Criteria Decision Analysis, score 8.65/10) as the foundation for the **Conscious Coach Platform (CCP)** — a unified system integrating CCF (Conscious Content Factory), CMF (Conscious Movie Factory), and CBCS into a single per-coach platform. The following epics extend the original 8 CBCS epics to deliver this unified vision.
>
> **Architecture Document:** See [CCP Unified Architecture](./CCP_unified_architecture.md) for the full MCDA, technology glossary, and prompt quality analysis that informed these epics.

---

## Epic 9: The Coach Role System (Identity & Routing)

*   **User Value:** As a coach, I interact with the same Telegram bot my clients use, but I see a completely different experience — content ideas, pipeline controls, and user monitoring instead of rituals.
*   **PRD Coverage:** FR 2.1 (Coach Onboarding — extended), FR 6.1 (Pantry — via Telegram), FR 6.2 (Cohort Vibe — via Telegram).
*   **Technical Context:** Role-based routing at Ingress layer, Supabase `role` column, Coach LangGraph subgraph.
*   **Dependencies:** Epic 1 (Ingress), Epic 2 (Profiles).

### Story 9.1: Coach Registry & Migration ✅

As a System,
I want to distinguish between coach and user Telegram accounts at the ingress layer,
So that messages are routed to the correct processing pipeline.

**Acceptance Criteria:**

**Given** a Telegram message from a registered chat_id
**When** the ingress layer processes it
**Then** the `RoleRegistry` must resolve the chat_id to a role (`coach`, `user`, or `unknown`).
**And** coach messages must be routed to `coach_graph`, user messages to the existing `graph`.
**And** the `profiles` table must include a `role` column with CHECK constraint.

**Technical Notes:**
*   **Architecture:** Ingress Layer (FastAPI) + Supabase Migration.
*   **Implementation:** `RoleRegistry` class in `ingress.py` with in-memory cache + Supabase fallback.
*   **Migration:** `002_coach_role_system.sql` — adds `role` column, `coach_configs`, `coach_content_ideas`, `user_activity_log` tables.
*   **Status:** ✅ Implemented.

### Story 9.2: Coach State Extension ✅

As a Developer,
I want the LangGraph state to carry coach-specific context (config, content workflow, monitoring state),
So that the coach subgraph can make informed routing decisions.

**Acceptance Criteria:**

**Given** a coach interaction
**When** the state is initialized
**Then** `AgentState` must include `role`, `coach_config` (CoachConfig TypedDict), `generated_ideas`, `selected_idea_index`, and `monitored_users`.
**And** `CoachConfig` must contain schedule fields (interview_day, ideas_day, recording_day), content preferences, and archetype ordering.

**Technical Notes:**
*   **Architecture:** Core State (`state.py`).
*   **Implementation:** Extended `AgentState` with `CoachConfig`, `ContentIdea` TypedDicts.
*   **Status:** ✅ Implemented.

### Story 9.3: Coach LangGraph Subgraph ✅

As a Coach,
I want to interact with the bot naturally — selecting ideas, triggering pipelines, checking users — through a unified conversational interface,
So that I don't need separate tools for each workflow.

**Acceptance Criteria:**

**Given** a coach message
**When** the coach subgraph processes it
**Then** intent classification must route to one of 5 nodes: `content_ideation`, `pipeline_trigger`, `user_monitor`, `idea_selection`, or `general_response`.
**And** emoji replies (1️⃣, 2️⃣, 3️⃣) must be recognized as idea selections.
**And** voice transcriptions must be classified as `interview` intent and route to content ideation.

**Technical Notes:**
*   **Architecture:** Coach Cognitive Core (`coach_graph.py`).
*   **Implementation:** 6-node LangGraph with conditional edges based on intent classifier.
*   **Status:** ✅ Implemented.

---

## Epic 10: The Scheduler (Proactive Intelligence)

*   **User Value:** As a coach, I receive automated messages on a predictable schedule — interview prompts on Monday, content ideas on Thursday, recording prep on Saturday — without having to remember anything.
*   **PRD Coverage:** FR 5.1 (Adaptive Primer — extended to coach), FR 5.4 (Evening Reflection — extended to coach check-ins).
*   **Technical Context:** APScheduler with AsyncIOScheduler, Supabase-backed job store, per-coach timezone support.
*   **Dependencies:** Epic 9 (Coach Role System).

### Story 10.1: APScheduler Integration

As a System,
I want a persistent, timezone-aware scheduler that survives server restarts,
So that proactive messages are never missed.

**Acceptance Criteria:**

**Given** the FastAPI application lifecycle
**When** the server starts
**Then** APScheduler must initialize with `AsyncIOScheduler` and a Supabase-backed job store.
**And** it must restore previously scheduled jobs on restart.
**And** it must support per-coach timezone offsets for delivery timing.

**Technical Notes:**
*   **Architecture:** Scheduler Layer (replacing the basic keep-warm-only scheduler).
*   **Dependencies:** `apscheduler>=3.10`, `pytz`.
*   **Status:** 🔲 Not started.

### Story 10.2: Coach Schedule Configuration

As a Coach,
I want to configure my weekly rhythm (interview day, ideas day, recording day),
So that the bot adapts to my preferred schedule.

**Acceptance Criteria:**

**Given** a `coach_configs` record in Supabase
**When** the scheduler reads the config
**Then** it must create cron triggers for: interview prompt (e.g., Monday 09:00), ideas delivery (e.g., Thursday 09:00), recording prep (e.g., Saturday 09:00).
**And** the coach must be able to update the schedule via Telegram commands.

**Technical Notes:**
*   **Architecture:** `coach_configs` table + Scheduler.
*   **Status:** 🔲 Not started.

### Story 10.3: Heartbeat Messages

As a Coach,
I want to receive contextually appropriate proactive messages at scheduled times,
So that the bot drives my weekly content creation rhythm.

**Acceptance Criteria:**

**Given** a scheduled trigger fires
**When** the scheduler invokes the coach graph
**Then**:
- **Monday:** "🎤 It's interview day! Record your weekly voice note when ready."
- **Thursday:** 3 content ideas generated from weekly themes + archetype prompts.
- **Saturday:** Recording prep package (script + visual prompts + instructions).
**And** each message must reference the coach's specific context (current week, selected idea).

**Technical Notes:**
*   **Architecture:** Scheduler → Coach Graph entry point.
*   **Status:** 🔲 Not started.

---

## Epic 11: The Bridge (CCF/CMF CLI Integration)

*   **User Value:** As a coach, the system automatically produces my weekly content themes and video production packages without me learning any command-line tools.
*   **PRD Coverage:** New FR — Content Pipeline Orchestration.
*   **Technical Context:** CLI Session Runner spawning Gemini CLI processes, file-system state passing, output monitoring.
*   **Dependencies:** Epic 9 (Coach Role System), Epic 10 (Scheduler).

> **Design Decision:** CCF and CMF commands (300+ prompt files) remain as CLI-driven markdown executed by Gemini CLI. We do NOT wrap them as Pydantic AI tools. CBCS acts as coordinator/scheduler; Gemini CLI is the creative executor.

### Story 11.1: CLI Session Runner ✅

As a System,
I want to programmatically spawn Gemini CLI sessions that execute CCF/CMF commands unchanged,
So that the 300+ battle-tested prompt files continue to work exactly as designed.

**Acceptance Criteria:**

**Given** a `CLISessionConfig` (command name, project_id, workspace_root, expected_outputs)
**When** `cli_runner.run_session()` is called
**Then** the runner must spawn `gemini -p "Read commands/{command}.md and execute for project '{project_id}'"`.
**And** it must wait for completion with a configurable timeout (default 600s).
**And** it must collect output files (read small text files, return paths for large files).
**And** it must return a `CLISessionResult` with success/failure, duration, and output file contents.

**Technical Notes:**
*   **Architecture:** CLI Runner (`cli_runner.py`).
*   **Implementation:** `asyncio.create_subprocess_exec` with timeout, output collection, error handling.
*   **Status:** ✅ Implemented.

### Story 11.2: Pipeline Sequencing ✅

As a System,
I want to run multi-step CMF pipelines (diagnose → hunt → analyze → compose) in sequence,
So that each step's output files are available as input for the next step.

**Acceptance Criteria:**

**Given** a list of `CLISessionConfig` objects
**When** `cli_runner.run_pipeline()` is called
**Then** sessions must execute sequentially with 2s pause between steps.
**And** if `stop_on_failure=True`, the pipeline must halt on the first failed session.
**And** pipeline presets must be available for CMF Phase 1A (4 steps) and CCF Weekly (1 step).

**Technical Notes:**
*   **Architecture:** CLI Runner (`cli_runner.py`).
*   **Implementation:** `build_cmf_phase1a_pipeline()` and `build_ccf_weekly_pipeline()` preset builders.
*   **Status:** ✅ Implemented.

### Story 11.3: CCF Weekly Trigger

As a Coach,
I want the weekly content pipeline to run automatically and deliver themes to me,
So that I always have fresh, research-backed content ideas.

**Acceptance Criteria:**

**Given** a scheduled weekly trigger (e.g., Wednesday 02:00 AM)
**When** the scheduler fires
**Then** the CLI Runner must spawn `ccf-weekly` for the coach's project.
**And** upon completion, it must read `dynamic_content_themes.json`.
**And** the themes must be passed to the content ideation node for idea generation.

**Technical Notes:**
*   **Architecture:** Scheduler → CLI Runner → Coach Graph.
*   **Dependencies:** Story 10.1, Story 11.1.
*   **Status:** 🔲 Not started.

### Story 11.4: CMF Pipeline Trigger

As a Coach,
I want to trigger the full CMF video production pipeline via a Telegram command,
So that I can go from raw interview to final video without touching the command line.

**Acceptance Criteria:**

**Given** a coach message containing "run pipeline" or similar
**When** the coach graph routes to `pipeline_trigger`
**Then** the CLI Runner must spawn CMF Phase 1A pipeline (diagnose → hunt → analyze → compose).
**And** the coach must receive progress updates as each step completes.
**And** upon completion, the final `premise_analysis.json` must be delivered via Telegram.

**Technical Notes:**
*   **Architecture:** Coach Graph → CLI Runner.
*   **Dependencies:** Story 9.3, Story 11.1.
*   **Status:** 🔲 Not started (node exists as placeholder in `coach_graph.py`).

---

## Epic 12: The Evolution (CBCS Protocol Upgrade)

*   **User Value:** As a user, I receive responses that are dramatically more detailed, contextually appropriate, and psychologically precise.
*   **PRD Coverage:** All FR 3.x (Assembler, Artisan, Persuasion Layers) — quality upgrade.
*   **Technical Context:** Rewriting CBCS agent protocols from 3KB flat markdown to 30KB+ SKILL.md format with 7-layer prompt architecture.
*   **Dependencies:** Epic 3 (Intelligence Library), Epic 4 (Brain).

> **Prompt Quality Gap:** CBCS protocols are ~3KB with basic `{format_string}` injection. CCF/CMF skills are 30KB+ with YAML frontmatter, explicit constraints, quality gates, verbatim mode, and scene-level granularity. The 10x quality gap must be closed before CCP goes live.

### Story 12.1: SKILL.md Format Adoption

As a Developer,
I want a CBCS-specific SKILL.md template that matches CCF/CMF quality standards,
So that all CBCS agent interactions use the proven 7-layer prompt architecture.

**Acceptance Criteria:**

**Given** the CCF/CMF SKILL.md format
**When** adapted for CBCS
**Then** the template must include: YAML frontmatter (name, description, version, agent), identity section, priming block, role definition, sacred protocols, variable tables, quality gates.
**And** it must enforce CBCS-specific constraints (TTT compliance, Intelligence Library reference, PII redaction).

**Technical Notes:**
*   **Architecture:** Protocol template design.
*   **Status:** 🔲 Not started.

### Story 12.2: Aria Skill Rewrite

As a System,
I want Aria's entity extraction to use a production-quality SKILL.md with explicit extraction rules,
So that entity classification accuracy matches the precision of CMF arc hunters.

**Acceptance Criteria:**

**Given** a voice note transcript
**When** Aria processes it using the new SKILL.md
**Then** entity extraction must follow explicit rules for each of the 12 Context Premise dimensions.
**And** quality gates must enforce minimum entity confidence scores.
**And** extraction must include `[!CAUTION]` blocks for edge cases (ambiguous entities, sarcasm detection).

**Technical Notes:**
*   **Architecture:** Aria Agent upgrade.
*   **Target:** Upgrade from ~3KB to 15KB+ with quality gates.
*   **Status:** 🔲 Not started.

### Story 12.3: Assembler & Artisan Skill Rewrites

As a System,
I want the Assembler and Artisan agents to use production-quality SKILL.md files,
So that strategy selection and script generation match CCF/CMF quality standards.

**Acceptance Criteria:**

**Given** the current 3KB Assembler and Artisan protocols
**When** rewritten as SKILL.md files
**Then** the Assembler must include explicit scoring rubrics for strategy selection (weighted criteria, not gut feel).
**And** the Artisan must include narrative constraints (sentence length by TTT level, banned phrases, mandatory formula adherence).
**And** both must include 13+ point validation rubrics matching CMF quality gates.

**Technical Notes:**
*   **Architecture:** Assembler + Artisan Agent upgrades.
*   **Status:** 🔲 Not started.

---

## Epic 13: The Colony (Per-Coach Cloning & Deployment)

*   **User Value:** As a coach, I have my own isolated instance with my own API keys, intelligence library, and production data — no cross-contamination.
*   **PRD Coverage:** FR 7.3 (Glass Wall — extended to multi-coach isolation).
*   **Technical Context:** Docker Compose with per-coach environment files, read-only shared mounts, coach-specific volumes.
*   **Dependencies:** All previous Epics.

### Story 13.1: Docker Compose Template

As a DevOps Engineer,
I want a Docker Compose template that spins up a complete coach instance,
So that onboarding a new coach is a single `docker compose up` command.

**Acceptance Criteria:**

**Given** a coach's `.env` file and `intelligence_library/` directory
**When** `docker compose up` runs
**Then** it must start: FastAPI backend, Redis, and scheduler.
**And** shared code (skills, commands) must be mounted read-only.
**And** coach-specific data (intelligence library, production output) must be mounted read-write.
**And** the coach's Telegram bot token must be isolated from other instances.

**Technical Notes:**
*   **Architecture:** Docker deployment.
*   **Status:** 🔲 Not started.

### Story 13.2: Intelligence Library Mount Strategy

As a Coach,
I want to tune the psychological methodology for my specific audience,
So that the AI uses my language, my metaphors, and my framework — not a generic one.

**Acceptance Criteria:**

**Given** a per-coach intelligence library (tuned YAML files)
**When** the Docker container starts
**Then** it must mount the coach's `intelligence_library/` at `/backend/intelligence_library/`.
**And** shared system prompts must be mounted read-only from the master codebase.
**And** the coach can override specific YAML files without forking the entire library.

**Technical Notes:**
*   **Architecture:** Volume mount strategy.
*   **Status:** 🔲 Not started.

---

## CCP FR Coverage Matrix (Epics 9–13)

| FR ID | Requirement Name | Covered By Story |
| :--- | :--- | :--- |
| **FR 9.1** | Coach Role Resolution | Story 9.1 |
| **FR 9.2** | Coach State Management | Story 9.2 |
| **FR 9.3** | Coach Conversational Interface | Story 9.3 |
| **FR 10.1** | Persistent Scheduling | Story 10.1 |
| **FR 10.2** | Coach Schedule Configuration | Story 10.2 |
| **FR 10.3** | Proactive Messaging | Story 10.3 |
| **FR 11.1** | CLI Session Spawning | Story 11.1 |
| **FR 11.2** | Pipeline Sequencing | Story 11.2 |
| **FR 11.3** | Automated Weekly Pipeline | Story 11.3 |
| **FR 11.4** | Video Pipeline Trigger | Story 11.4 |
| **FR 12.1** | SKILL.md Protocol Standard | Story 12.1 |
| **FR 12.2** | Aria Quality Upgrade | Story 12.2 |
| **FR 12.3** | Assembler/Artisan Quality Upgrade | Story 12.3 |
| **FR 13.1** | Per-Coach Isolation | Story 13.1 |
| **FR 13.2** | Coach-Specific Intelligence | Story 13.2 |

---
