---
title: "The Conscious Coaching Platform (CCP) — Unified Technical Architecture"
version: "5.0"
status: "Active / Engineering Blueprint"
author: "BMAD Architect"
last_updated: "2026-03-18"
schema_version: "v4"
---

# CCP Unified Technical Architecture

This document serves as the master engineering blueprint for the Conscious Coaching Platform (CCP). It translates the high-level PRD requirements into strict, deterministic implementation constraints using the BMAD micro-file architecture philosophy. 

**Architectural Paradigm:** The CCP is a multi-agent, single-tenant, cloud-native **Trigger-First Operating System**. It abandons descriptive LLM prompting in favor of Just-In-Time (JIT) Skill Compilation, deterministic execution dependencies, and rigorous psychological routing.

---

## 1. Architectural Principles & Architecture Decision Records (ADRs)

The following ADRs mandate the foundational technical decisions across all sub-systems (CCF, CBCS, V²WS, Tierlist). **No component may be designed in violation of these ADRs.**

*   **ADR-01: Single-Tenant Isolated Cloud-Native Instances.**
    *   *Constraint:* No shared databases or agent environments across coaches. Every coach receives a dedicated code repository and cloud instance.
    *   *Justification:* Voice DNA (`coach_soul.json`) and Neo4j Context Premises contain highly sensitive psycho-emotional data. Absolute isolation prevents cross-coach contamination.
*   **ADR-02: Zero-UI Delivery Layer (Notion).**
    *   *Constraint:* All system-to-coach delivery (Content Calendars, Client Intelligence dashboards, VPOs) must occur autonomously via Notion API.
    *   *Justification:* Minimizes UX/UI engineering overhead and respects the "Never Outshine the Master" principle.
*   **ADR-03: Invisible App Paradigm (Telegram).**
    *   *Constraint:* The CBCS client interface operates entirely via Telegram Voice Notes and Text. No native mobile applications.
    *   *Justification:* Zero download friction for end-users. The intelligence layers (12 agents, `InteractComp`, `SoulResonance`) operate invisibly behind a standard messaging interface.
*   **ADR-04: JIT Skill Compilation over Monolithic Prompts.**
    *   *Constraint:* System Prompts are forbidden. All generative instructions must be dynamically compiled from atomized modular skills via the Dependency Registry and Adapter Registry at runtime.
    *   *Justification:* Eliminates statistical centroid drift and prompt degradation, ensuring outputs structurally match the coach's 3D Voice DNA.
*   **ADR-05: Mandatory Primitive Loading & Internal Evals.**
    *   *Constraint:* No technical specification, JIT compilation, or output validation pipeline may rely on LLM intuition for quality control. **Primitive YAMLs MUST be loaded into context** as the deterministic standard of quality.
    *   *Justification:* Primitives (e.g., `PRM-STR-008.yaml`) contain specific, float-based geometry and dual-source verified knowledge. They are the only acceptable baseline for internal Evals. If an evaluation pipeline evaluates an output without first loading the targeted primitive schema, the evaluation is considered hallucinated and invalid.

---

## 2. System Topology: The 7-Layer Architecture

Data flows upward from Research to Intuition; execution flows horizontally across sub-systems.

### Layer 1: Deep Research (CRAL - Conscious Research Alchemy Lab)
*   **Purpose:** Enforces the **Human Evidence Bias** by generating research grounded in verifiable reality rather than LLM hallucination.
*   **Components:** 
    *   `OODA Orchestrator`: Observes pipeline dependencies, decides when to fire Planners.
    *   `Research Planner JIT Skill`: Compiles rigid constraints for execution.
    *   `The Diagonal (M1-M7)`: Seven strictly sequenced research moments (`M1 RELEVANT` → `M2 BELIEVABLE` → `M3 UNDENIABLE` → `M4 RESONANT` → `M5 SURPRISING` → `M6 IRREFUTABLE` → `M7 RELATABLE`).
*   **Integrations:** Firecrawl/Tavily for forum scraping, Trend analysis APIs.

### Layer 2: Memory
*   **Purpose:** Hybrid storage of relational psychographics, semantic history, and blob text.
*   **Components:** 
    *   `Neo4j Hypergraph`: Maps Context Premises (Fears, Enemies, Dreams, Hidden Beliefs) as graph nodes and edges (`(Story)-[:RESONATES_WITH]->(Archetype)`).
    *   `Supabase (PostgreSQL)`: Relational data, user configs, content performance matrices. Includes V5 extensions (CMM, Story Archive, Humor Registry, CPR).
    *   `coach_soul.json`: 3D Voice DNA stored in the single-tenant file system.

### Layer 3: Deep Reasoning
*   **Purpose:** Multi-criteria deliberation prior to code execution or generation.
*   **Components:** 
    *   `MCDA (Multi-Criteria Decision Analysis)`: Agents synthetically score potential outputs.
    *   `Context Reasoning Phase 1`: Q1 (Story Archive eligibility), Q2 (CMM layer weighting), Q3 (Humor precedent check). Outputs logged to `DEP-ENG-025`.

### Layer 4: Execution (JIT Skill Compiler)
*   **Purpose:** The central logic engine dynamically assembling scripts, responses, and visual prompts.
*   **Components:** 
    *   **Agent Workforce:** 65 specifically named agents organized into 6 departments (Perception, Strategy, Expression, Validation, Management, Setup).
    *   **JIT Skill Compiler (CCSB):** (Detailed in Section 4).

### Layer 5: Orchestration (The Pi Harness)
*   **Purpose:** TypeScript Pi Coding Agent running 11 deterministic extension scripts.
*   **Components:** 7 Operational Extensions (`InteractComp`, `DamageControl`, etc.) and 4 Intuition Extensions (`SoulResonance`, `PatternWeaver`, etc.). (Detailed in Section 6).

### Layer 6: Governance
*   **Purpose:** Mathematical constraints over generation logic.
*   **Components:** 
    *   `Receipt Chain Guard`: Halts the batch if any dependency receipt goes missing.
    *   `Semantic Affinity Guard`: Blocks "Escape Mode" content lacking low-affinity entry points.
    *   `Boredom Ban`: Enforces rolling 8-week mechanism uniqueness on humor.

### Layer 7: Intuition
*   **Purpose:** Context-aware aesthetic and thematic enhancement.
*   **Components:** `Memetic Engine` (14-architecture humor generator) and scheduled Intuition Extensions.

---

## 3. Storage & Schema Specifications

### 3.1. Supabase (PostgreSQL) Requirements
V5 capabilities require non-negotiable migrations before the first production session.
*   `cultural_memory_map` (PK: `cmm_id`): JSONB payload containing 7 layers (Formative Texts, Collective Wound History, Industry Mythology, Generational Signature, Linguistic Templates, Aspirational Archetype, Enemy Typology) => `DEP-ENG-023`.
*   `coach_story_archive` (PK: `story_id`): Enforces the Hartian 5-element schema (named protagonist, tribal markers, moment of contact, internal shift, verifiable outcome) => `DEP-ENG-024`.
*   `humor_mechanism_registry` (PK: `registry_id`): Logs successfully deployed humor arcs to ensure compliance with the Boredom Ban.
*   `context_performance_registry` (PK: `registry_id`): Maps context selection rationale against public performance metrics (Likes, Retweets, Saves) => `DEP-ENG-025`.

### 3.2. Neo4j Hypergraph (Context Premises)
*   Must support concurrent reads (from CBCS) and writes (from Aria/MemoryFolder extensions).
*   Enforces a strict 12-dimensional ontology for routing the coach's Context Premise into the generated assets.

---

## 4. JIT Skill Compiler (CCSB) Blueprint

The CCSB replaces LLM-prompted text generators with a 7-component deterministic translation layer.

1.  **Dependency Registry v4.0:** 
    *   Maintains 46+ `DEP IDs` across Engine Outputs, Libraries, and Data.
    *   **Ghost Variable Rule:** If a skill references a data source without an explicit `DEP ID` attached, compilation HALTS. No inline variable hacking.
2.  **Adapter Registry v2.0:** 
    *   Mandatory: `coach-soul-adapter` (Positive voice), `negative-space-loader-adapter` (Drift patterns), `irevc-adapter` (LIWC metrics), `context-premise-adapter` (Graph context), `psych-routing-adapter` (Mood/Trajectory).
    *   Conditional: `payload-masking-adapter`, `audience-maturity-adapter`.
3.  **Phase 1: Design Brief Builder Engine (with Step 3.5):** 
    *   Verifies dependencies, loads the Context Premise (`DEP-ENG-006`), generates the Psychological Routing Brief (`DEP-ENG-016`). 
    *   *Step 3.5 Synthesis Protocol:* Evaluates the generated CRAL Finding Index (`DEP-ENG-021`) against the active Archetype Schema. Flags conflicts to operator.
4.  **Phase 2: JIT Skill Assembler v2.0:** 
    *   Tier 0: Pre-flight checks (C-01 to C-10). Non-negotiable rejection of hardcoded TTT (Temperature, Temperament, Tone) in `C-08`.
    *   Tier 1 & Tier 2: Adapter logic injected into isolated memory sectors.
    *   Tier 3: Sequential block-by-block text assembly.
    *   Post-Assembly: Surface gates (SG-01 to SG-08) and Psychological checks (PC-01 to PC-05).
5.  **Container Module Library:** 
    *   Defines the 7 Archetype Family boundaries. Enforces Ecological Adaptation to social platforms and applies the Mood State Interaction Matrix.
6.  **Fingerprint Archive:** 
    *   Systematic traceability via ID Schema: `SKILL-{ARCH_ID}-{COACH_ID}-{MOOD}-{REG_FRAME}-{COHORT}-{YYYYMMDD}-{SEQ}`.
7.  **Anti-Draft Intelligence (3-Levels):** 
    *   **Level 1 (Archetype):** Pre-written generic failure modes from the Container Library.
    *   **Level 2 (Mode):** Statistical Centroid Anchor from `CRAL M3`.
    *   **Level 3 (Coach):** The `coach_soul.json` Negative Space (DEP-ENG-004) dictates personal forbidden vocabulary and semantic drift.

---

## 5. Sub-System Executions (Capability Areas)

### 5.1. Capability Area 0: Pre-Production Intelligence (Guardian Agent)
The Guardian Agent securely dictates the pipeline's initialization parameters.
*   **Sequence:** FR0A (Biz Intel) → FR0B (Tribe Soul) → FR0C (Lexicon) → FR0D (Semiotics) → FR0E (Brand Avatars).
*   **Verdict Logic:** Each stage must return `AUTHENTICATED`. If `PROVISIONAL`, human operator approves. If `FAILED`, Genesis halts.
*   **Stewardship Mode:** Ongoing weekly drift checks against the Lexicon and Campaign fatigue.

### 5.2. CCF (Conscious Content Factory) & V²WS (Webinar System)
*   **CCF Execution:** Cron-job batch production leveraging the full CRAL 9-skill diagonal. Uses the **Semantic Affinity Guard (DEP-PROTO-011)** to block combinations of HIGH affinity subjects with an audience currently in ESCAPE mode to prevent psychological harm.
*   **V²WS Execution:** Modular assembly (Jason Fladlien method) where every slide is engineered as a "HOOK". Transitions from sequential builds to real-time agentic audience-sentiment adjustments.

### 5.3. Capability Area 9: Conscious Persuasion Sales Cycle (CPSC)
Transforms relationship accumulation into temporal conversion triggers.
*   **Change Talk Vault:** DARN-CAT commitments are stored and mirrored back systematically during invitations (Motivational Interviewing logic).
*   **Social Penetration Depth Gauge:** Tracks position across 4 stages (Orientation → Exploratory → Affective → Stable). Commercial touchpoints strictly require `SPT stage >= Affective` and `Telegram Intimacy Index >= 0.4`.
*   **72-Hour Identity Anchor Protocol:** Day 1 (Reflection), Day 2 (Micro-commitment), Day 3 (Counterfactual Activation with genuine temporal accuracy). No manufactured scarcity permitted.

### 5.4. Capability Area 10: Conscious Visual Engine (CVE)
Post-script deterministic visual generation based on 7 neurological design pillars.
*   **Multi-Agent Orchestration:** `Abel` (Visual Composition Brief/PSSL) → `Aurore` (Image Research against 5 APIs) → `Paradoxe` (Prompt compiler) → `RunningHub` (AI execution) → `Visual Validation Agent` (AGSS scoring) → `Conscious Canva App` (Assembly) → `Notion` (Sync).
*   **Four-Tier Image Hierarchy:** (1) Real Photos → (2) Stock Photos → (3) Realistic AI → (4) Ghibli Style AI. Stock search MUST fail before AI execution begins.
*   **PSSL Definition:** Parameters enforce exact Kelvin temperatures, Gaze Vectors, PAD emotion scores, intentional imperfections, and the Six-Word Hook Law.

---

## 6. Execution Harness & Security Infrastructure

The pipeline relies on the `Pi Coding Agent` using 11 TypeScript Extensions. Python is restricted to isolated worker scripts (e.g., `firecrawl_wrapper.py`).

### 6.1. Core Extensions
*   `InteractComp` (Pre-Flight): Scans inputs against the Required Schema. Will halt execution and prompt the user rather than allowing models to hallucinate missing required data.
*   `DamageControl` (On-Error): Captures pipeline errors. Feeds tracebacks directly to the responsible sub-agent for a single focused retry in isolation. Prevents system-wide ungraceful exits.
*   `ModelRouter` (Optimizer): Routes reasoning to Gemini Pro High, Script composition to Pro Low, and Schema validation to Gemini Flash.
*   `TillDone` (Task Integrity): Enforces checklist completion and validates schemas against JSON artifacts.

### 6.2. Security Constraints
*   **Circuit Breaker Protocol:** 500ms hard-coded threshold for detecting crisis keywords in the CBCS voice notes. Halts AI execution and triggers operator escalation immediately.
*   **Receipt Chain Guard:** Every data mutation or cross-agent transfer must emit a signed JSON receipt. A missing receipt results in `Batch Quarantine`.

---

## 7. The 14-Step Non-Negotiable Build Sequence

To construct or rebuild instances of the CCP, the following dependency sequence is structurally mandatory.

#### Phase 1-A: Core Infrastructure
1.  **Dependency Registry v4.0** (All 46+ URLs and data sources initialized).
2.  **Coach Genesis Pipeline** (Initial transcript ingestion -> Voice DNA extraction -> `coach_soul.json`).
3.  **`framework_archetype_mapping.yaml` Upgrade** (Add the 8 mandatory psychological classification fields per archetype).
4.  **5-Stage Psychological Routing Flow** (Hook LIWC-22 detection to Mood Context Maps).
5.  **3D Voice DNA Wiring** (Attach Positive Space, Negative Space, and Emotional DNA to the Adapter Registry).

#### Phase 1-B: JIT Compiler Full Activation
6.  **Container Module Library** (Define the 7 archetype boundaries).
7.  **Adapter Registry v2.0** (Code the 8 mandatory and conditional adapters).
8.  **Design Brief Builder & Step 3.5** (Assemble the CRAL conflict resolution logic).
9.  **JIT Skill Assembler v2.0** (Implement the 4-tier assembly validation gates).
10. **Fingerprint Archive + Anti-Draft** (Wire Level 1/2/3 anchors into the Critic Sub-Agent).

#### Phase 1-C: Intelligence & Orchestration
11. **CRAL 9-Skill Subsystem** (Code the Python/Firecrawl logic for M1-M7).
12. **11 Pi Extensions (TypeScript)** (Deploy the execution harness).
13. **V5 Per-Coach Gates** (Initialize Neo4j CMM, Story Archive, Humor Registry, and Performance Registry).
14. **V²WS + Data Integration** (Final integrations with Excalidraw, Publer, and Notion APIs).

---

*This document is the absolute source of truth for all engineering, architectural decisions, and agent deployments within the CCF, CBCS, CPSC, and CVE paradigms.*