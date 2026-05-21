# Sovereign NIM Integration MCDA: Agentic Reasoning & Script Generation Models
**Document Authority:** CCP Engineering Division & Conscious Architect University
**Framework Revision:** v1.3 (Sovereign Architecture Alignment w/ Kimi Swarm & M2.7)
**Evaluated Models:** Qwen 3.5 397B A17B, Gemma 4 31B IT, Z.AI GLM 5 Turbo, MiniMax M2.7, moonshotai/Kimi-K2, moonshotai/Kimi-K2.5 

## I. Executive Summary
The transition from a reliant, third-party API wrapper paradigm into a Sovereign Agentic Computing model is the central thesis of the modern Conscious Coaching Platform (CCP). As dictated by **Launch Manual: Unit 3.1 (The Wrapper Trap vs. The Harness)** and the finalized **CCP PRD**, all cognitive compute must be internalized via self-hosted Nvidia NIM containers on AWS EC2. 

The purpose of this Multi-Criteria Decision Analysis (MCDA) is to critically evaluate six state-of-the-art open-weights foundation models against the rigorous demands of the **JIT Skill Compiler Architecture** and the **Script Generation Skill Type Guide v1.0**. We are not simply evaluating which model writes the "best" output; we are identifying the precise architectural compatibility of each model within a multi-agent assembly pipeline consisting of Intent Classification, Data Operations (Pass 1), Swarm Orchestration, the Heavy Critic Evaluation (Pass 2), and Synthesis (Pass 3). 

This analysis synthesizes core telemetry from 17 specific framework mandates and technical papers—including the newly integrated MiniMax M2.7 Self-Evolution capabilities and Kimi's Swarm & Multimodal architectures—to recommend the definitive foundational stack for the Conscious Architect University deployment.

> [!CAUTION]
> Utilizing a single model for both generation and evaluation constitutes a violation of **System Architecture First Principles**. Doing so leads to confirmation bias, wherein a model rubber-stamps its own cognitive load drift patterns. The architecture requires specialized, heterogeneous models for Draft and Critic roles.

---

## II. Axiomatic Constraints and Referenced Architecture
This MCDA grounds its analysis entirely within the boundary conditions of the following defining CCP OS documents:

1. **The CCP PRD (v2.0 Update):** Establishes the AWS EC2 + Nvidia NIM container infrastructure, completely deprecating proxy-API services.
2. **JIT_Skill_Compiler_Architecture.docx.md:** Defines the engine that transforms Archetype Templates into SKILL.md executables via the Draft-Critic-Synthesis loop.
3. **Script_Generation_Skill_Type_Guide_v1.docx.md:** Provides the exact authoring doctrine for script skills (Mandate M7 "Law of the Negative Anchor").
4. **GLM-5 from Vibe Coding to Agentic Engineering:** Introduces "Interleaved Thinking" and "Preserved Thinking" paradigms.
5. **Kimi_K2_and_K2.5_Agentic_Harness.md:** Establishes Proactive Context Management (Swarm) and Zero-UI tool execution mandates.
6. **MiniMax_m27_Self_Evolution_Harness.md:** Deploys the Heavy Critic Node utilizing unsupervised recursive reflection.
7. **Launch Manual: Unit 3.1 / 3.2:** Explicit anti-wrapper directives and dynamic constraint generation.
8. **Launch Manual: Unit 12.2 CRON Scheduling:** The Batch Clock and Cold Start Physics logic.
9. **Sovereign_Visual_Research_Engine.md (SVRE):** Mandates specific throughput speeds for visual scoring.
10. **Sovereign_CRAL_Research_Engine.md (CRAL):** Requires precise instruction following to map M1-M7 Moments.
11. **Contrastive Chain-of-Thought Prompting (Ling et al., 2023):** Defines the Level 1 Anti-Draft requirements.
12. **SkillNet Paradigm (Liang et al., 2026):** Establishes that formalizing skills as composable assets improves execution.
13. **Broaden-and-Build Theory / Mood Management Theory:** Psychometric basis for transitioning audiences across Processing/Escape Modes computationally.
14. **Evolving PSN (Shi et al., 2025):** The Deployment Quarantine Rule governing failures.

---

## III. Benchmark Topography vs. JIT Compiler Mandates

The **JIT Skill Compiler** relies on semantic constraint satisfaction rather than unrestricted creative generation. A model must receive a highly complex block of data—including the Level 3 Coach-Specific Anti-Draft (Forbidden Vocabulary List), the PRD's TTT requirements, and the CRAL mapping (M2_BELIEVABLE, M5_SURPRISING)—and execute it flawlessly.

### 1. Z.AI GLM 5 Turbo (GLM-5.1)
**Profile Analysis:**
- **Strengths:** Pacing (1.0), Avoids Purple Prose (0.65), Show-Don't-Tell (0.35), Instruction Following (0.25).
- **Weaknesses:** Descriptive Imagery (-1.0), Avoids Amateurish Prose (-0.7).
- **Architectural Advantages:** GLM-5 features natively embedded "Interleaved Thinking" allowing the model to perform background reasoning chains *between* logic evaluations, alongside "Preserved Thinking" for state retention across multiple turns.

**First Principles Integration:**
As a **Semantic Logic Gatekeeper**, GLM-5 is utilized alongside the Heavy Critic to measure exact semantic distance. Because GLM-5 Turbo naturally avoids the positivity biases typical of generic AI, it aggressively flags drafts that hallucinate inspiration or rely on "try harder" platitudes. 

### 2. MoonshotAI: Kimi K2.5 (Multimodal Diagnostic & Swarm)
**Profile Analysis:**
- **Strengths:** Agent Swarm Orchestration (1.0), Dense Multimodal Ingestion (0.9), Descriptive Imagery (0.9), Parallel Subagent Execution (0.85).
- **Weaknesses:** Unconstrained Token Burn Risk (-0.9), Instruction Following without caps (-0.8).

**First Principles Integration:**
Kimi K2.5 radically shifts the paradigm from sequential draft generation to **Proactive Context Management**. Instead of dumping data into an ever-expanding window and risking prompt dropout, K2.5 leverages its native Agent Swarm architecture to parallelize generation and evaluation. When parsing dense client inputs (such as Roleplay Speaking Audits via MoonViT-3D), K2.5 spawns dedicated subagents for distinct psychometric evaluations, effectively eliminating Brevity Bias. In the JIT pipeline, it acts as the **Multimodal Diagnostics & Swarm Evaluator**, ingesting complex media and maintaining independent logic shards before merging them.

### 3. MoonshotAI: Kimi K2 (Data Operations Node)
**Profile Analysis:**
- **Strengths:** Tool Execution Determinism (1.0), Zero-UI Compliance (1.0), JSON/MD Schema Fidelity (0.95).
- **Weaknesses:** Avoids Purple Prose (-1.0) [if used for creative script generation], Coherence (-0.55).

**First Principles Integration:**
Trained via the MuonClip optimizer and heavily post-trained on executable sandboxes, Kimi K2 exhibits zero loss-spike stability, translating to peerless reliability in programmatic environments. It operates purely as the **Data Operations Node**. K2 strictly adheres to the Zero-UI mandate, executing `write_todos()` and producing pristine, unpolluted JSON/Markdown payloads without conversational hallucination. It manages the mechanical execution of drafts, file tree mutation, and system memory folding, acting as the deterministic backend of the Harness. 

### 4. MiniMax M2.7 (Heavy Critic Node)
**Profile Analysis:**
- **Strengths:** Recursive Reflection (1.0), Voice DNA Consistency (0.95), Diagnostic Evolution (0.9).
- **Weaknesses:** Cold-Start Inference Latency (-0.7).

**First Principles Integration:**
MiniMax M2.7 is injected as the ecosystem's **Heavy Critic Node**. Leveraging its native unsupervised self-evolution capability (Analyze -> Plan -> Scaffold -> Evaluate), M2.7 is heavily weaponized to aggressively score Kimi outputs against the Semantic Pointer Register (SPR). It prevents Identity Dilution across long-horizon executions and ensures that any generated content adheres perfectly to the Voice DNA of the injected coach persona before marking a batch as complete.

### 5. Qwen 3.5 397B A17B (Z.AI)
**First Principles Integration:**
Qwen 3.5 is a 397 Billion parameter Mixture-of-Experts Leviathan. Deploying this inside a transactional, JIT web-request loop violates the **VRAM Economics & Batched Compute** fundamentals. However, Qwen's unmatched capability in understanding structure (Show-Don't-Tell) makes it the ultimate engine for **Scheduled Deep Batching** operations. It parses massive legacy datasets and unstructured text offline for the Sovereign CRAL Search Engine but is strictly omitted from live script compilation loops.

### 6. Google: Gemma 4 31B IT
**First Principles Integration:**
Gemma 4 31B is the agile, high-throughput utility knife of the ecosystem. Fitting comfortably on a single G5.xlarge, it serves the **Design Brief Builder Engine (Phase 1 Compiler)** by handling rapid, deterministic logic formatting—such as mapping CRITICAL tier DEP IDs or validating JSON schemas—thereby freeing larger models for purely cognitive loads.

---

## IV. The Synthesized Engine Matrix (MCDA Implementation)
Based on the systemic requirements of the JIT Skill Compiler and the psychometric constraints of the models, the CCP OS is hereby architected to use a heterogeneous, interlocking NIM deployment map.

> [!IMPORTANT]
> The JIT Script generation must never be treated as a single inference call. The system operates as a chain across precisely assigned structural nodes.

### Stage 1: The Design Brief Builder Engine (Intent & Framing) 
**Deployed Model:** Gemma 4 31B IT
**Infrastructure footprint:** NIM Container on AWS G5.2xlarge (Single GPU)
**Logic Role:** When an archetype is requested, Gemma 4 is instantiated to quickly load the Block A invariant constraints, scrape the registry, and inject the runtime parameters. Because its instruction-following is very fast, it passes Gate 1 by identifying missing DEP references seamlessly.

### Stage 2: Data Operations & System Tool Executor
**Deployed Model:** Kimi K2
**Infrastructure footprint:** NIM Container on AWS G5.12xlarge 
**Logic Role:** As the definitive tool-use and markup execution agent, K2 guarantees 100% compliance with zero-UI operations. K2 executes Neo4j queries, constructs the precise JSON payloads, and handles physical file tree mutations to ensure system formatting remains uncorrupted by conversational AI habits.

### Stage 3: Multimodal Diagnostics & Swarm Orchestration (Pass 1)
**Deployed Model:** Kimi K2.5
**Infrastructure footprint:** NIM Container on AWS P4d.12xlarge
**Logic Role:** Tasked strictly with complex ingestion, Draft Generation, or media processing. When a rich media (Roleplay Audit) or an extremely massive text block arrives, K2.5 chunks execution into parallel sub-agents to bypass linear context dropout limits. It leverages its 1.0 imagery score to generate dense, vivid output.

### Stage 4: The Heavy Critic Subagent & Anti-Draft Evaluator (Pass 2)
**Deployed Model:** MiniMax M2.7 (Supported cross-validation by GLM-5 Turbo)
**Infrastructure footprint:** NIM Container on AWS P4d.24xlarge (during scheduled batch CRON windows)
**Logic Role:** M2.7 receives the raw Swarm and K2 outputs. Utilizing recursive self-reflection, M2.7 executes the **Emotional DNA Integration Test**. GLM-5 Turbo runs adjacently to apply "Interleaved Thinking" gap-checks on negative semantic distances. 
- *If a violation is caught:* M2.7 instantly generates a `critic_report.json` with an explicit failure diagnosis (e.g., "Violation of Anti-Draft Level 2: Escape Mode overlap") and passes instructions back to Stage 2 for modification.

### Stage 5: Orchestration & Offline CRAL Synthesis
**Deployed Model:** Qwen 3.5 397B A17B
**Infrastructure footprint:** NIM Container on ASG-triggered Spot Instance (P4d.24xlarge)
**Logic Role:** Executes deep batch context parsing for SVRE/CRAL batch processing and historical data formatting purely offline due to severe token VRAM costs.

---

## V. Context Windows and VRAM Economics 

### The CRON Scheduling Batch Protocol (Unit 12.2 Alignment)
To enforce the **First Principles of Batch Economics**, the CCP Platform Architecture relies on the "Two-Clock System":
1. **The Asynchronous Event Queue (SQS/Redis):** User interactions on the frontend, Telegram ingestion, and AFFiNE data entry are queued entirely asynchronously. 
2. **The Pre-Warm Event Horizon:** At 02:00 UTC (Weekly Coach Content Batch), the EventBridge Scheduler executes Terraform protocols to spin up the required AWS EC2 instances. 
3. **Container Hydration:** The Nvidia NIM containers for Kimi K2.5, MiniMax M2.7, and GLM-5 Turbo are loaded from AWS ECR into the warmed GPU VRAM.
4. **Execution Burst:** All `compilation_request_id` tasks are fired sequentially across the heterogeneous pipeline mapping. 
5. **Termination:** Upon `assembly_report.json = COMPLETE`, instances are aggressively terminated to halt the compute meter.

### Economic Routing Exceptions (Gemma 4 31B)
While Kimi and M2.7 require heavy A100 clusters, Gemma 4 31B acts as the permanent "Sovereign Watchdog," sitting in small, persistent spot fleets to catch routine routing JSON tasks that require instantaneous deterministic turnaround.

---

## VI. Graceful Degradation in Sovereign Clouds
The final evaluation dimension maps to Mandate M1: graceful failure protocols defined extensively in **Evolving PSN (Shi et al., 2025)**.

1. **Hallucination Vectors in Kimi:** 
   Given unbounded creativity, an unmonitored Kimi K2.5 experiencing a context-drop will seamlessly invent verifiable evidence anchors—fabricating data timestamps and masquerading the output as authoritative. To prevent this, K2 is utilized strictly to provide programmatic guardrails on K2.5’s output.
   
2. **Self-Regulatory Fallbacks in M2.7 & GLM-5:** 
   MiniMax M2.7 and GLM-5 possess deep introspective reflection loops. If an adapter detects missing dependencies (e.g., DEP-ENG-004 is absent), these models halt execution and write a `deployment_status: PARTIAL_MANUAL` output, formally quarantining the request to preserve truth values.
   
3. **Deterministic Guardrails in Gemma 4:** 
   As the Builder Engine orchestrator, Gemma 4 guarantees binary catch logic, dependably triggering fallback codeblocks (DEP-PROTO-011) if the risk delta reaches unacceptable margins prior to hitting the expensive multi-agent execution pipeline.

### Final Verification Check 
By deploying these six models exactly according to their psychometric weaknesses and strengths—anchoring the unbridled capability of Kimi K2.5 Swarms under the brutal recursive criticism of MiniMax M2.7 and GLM-5—the CCP platform shifts from monolithic API-wrapper fragility into mathematically rigorous, sovereign redundancy.

**END OF DOCUMENT** 
*Conscious Architect University & CCP Engineering Division · April 2026*
