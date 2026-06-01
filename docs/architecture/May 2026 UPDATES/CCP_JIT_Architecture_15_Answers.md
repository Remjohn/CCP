# CCP Master Architecture: The 15 "Grill-Me" Questions

This living document tracks the core architectural decisions for the **Conscious Coaching Platform (CCP)**, specifically focusing on the JIT Skill Compiler, Subliminal Orchestration, and the execution loops. 

## ✅ RESOLVED QUESTIONS (The Foundation)

**1. Orchestration Topology**
*Question:* Should SFL functions be compiled into their own isolated micro-harnesses, or loaded as modules inside a single "Subliminal Orchestrator Harness"?
*Resolution:* **Single Subliminal Orchestrator**. We avoid state fragmentation and "waterfall agent orchestration." The main loop is "dumb" and deterministic, running one overarching execution flow.
*   **[AUDIT FACT]:** The `SubliminalOrchestrator` is not implemented in the codebase. There are no files or services acting as a unified subliminal overarching harness. Orchestration remains fragmented and is handled procedurally by distinct pipeline services.

*   **[EMILIO COMMENTARY]:** Yes this part is not implemented yet since it's should be part of our May Update implementation - We should check if our current specs prompts are ready write a specs that execute this layer. (I doubt it does now so this is probably something we need to elaborate with more precision). VERDICT: A Receipt documentation + Epic-Story file/s should be writen about this. (Possibly using 2 or 3 these reasoning methodologies TRIZ / MCDA / SWOT / CBAR- Constraint-Based Adversarial Reasoning/ RSCS_Recursive_Signal_Compression_Systems (CBAR and RSCS are our proprietary reasoning framework))

**2. JIT Execution Mechanism**
*Question:* Does the JIT Compiler generate temporary Python wrappers, or run through a parameter-driven runner?
*Resolution:* **SKILL.md Compilation**. The JIT Compiler doesn't generate Python; it outputs a completely static, highly-constrained `SKILL.md` text file. The Execution Agent (a generic parameter-driven runner) simply reads and executes this markdown instruction set.
*   **[AUDIT FACT]:** Partial implementation. The data models and components for `SKILL.md` compilation exist (e.g., `fingerprint_archive_models.py`, `adapter_registry_models.py`, `anti_draft_models.py`), but the execution agent (the generic parameter-driven runner that reads and executes `SKILL.md` dynamically) is entirely unbuilt.

*   **[EMILIO COMMENTARY]:** The current JIT Compiler is outdated. We wrote this in March and now we are in late may and a lot have changed since... The role of skills have changed because now we are not interested in writing content scripts because we DO NOT dictate what the coach will say but WE GUIDE them into the structure with the right questions based on the content archetype and context... so the output is not the final script but the detailed content brief that will be used into our Persuasive Speaking Program daily drips. It's important to consider the old documentation about this because is still very important but also noticed that is has to be rebuilt. VERDICT: A Receipt documentation + Epic-Story file/s should be writen about this. (Possibly using 2 or 3 these reasoning methodologies TRIZ / MCDA / SWOT / CBAR- Constraint-Based Adversarial Reasoning/ RSCS_Recursive_Signal_Compression_Systems (CBAR and RSCS are our proprietary reasoning framework))

**3. Guardrail Routing**
*Question:* How do we split responsibility between DSPy Assertions and Pydantic validators?
*Resolution:* **Two-Tier System**. Pydantic enforces hard structural/invariant boundaries at the Python layer. DSPy Assertions handle cognitive/qualitative retries inside the LLM generation loop.
*   **[AUDIT FACT]:** DSPy integration exists in `orchestration_dichotomy.py` and `archetype_container_runtime.py` to enforce typed structural outputs. However, the cognitive/qualitative retries via `dspy.Assert` or `dspy.Suggest` are completely absent from the codebase. Only Pydantic hard constraints are enforced.

*   **[EMILIO COMMENTARY]:** Well first of all our generation loops need to be more clearly defined. What are our generation loops strategies. Will they change based on workflows and pipelines. What failure looks like. Are they centroind based or edging based if so on which level... lab\CCP APRIL Updates\05_Core_Experience\Matrix of Edging.md I don't see the Matrix of Edging referenced enough but it is very important philosophy for us... so it should definely integrate our V5 CCP System documentation... because if we are building an orchestration layer without one of our core phisolophy we will start having outputs that do not truly satisy us. So the edging need to be considered and definitely we should talk about that when it comes to building Assertions and Validators... because especially a lot of validators flags risk to become centroid agents and we do not want that... they should validate edging too (when applicable). VERDICT: A Receipt documentation + Epic-Story file/s should be writen about this. (Possibly using 2 or 3 these reasoning methodologies TRIZ / MCDA / SWOT / CBAR- Constraint-Based Adversarial Reasoning/ RSCS_Recursive_Signal_Compression_Systems (CBAR and RSCS are our proprietary reasoning framework))


**4. Adversarial Testing & Anti-Drafts**
*Question:* Should SFL negative operations be validated using a dedicated "Adversarial SFL Harness"?
*Resolution:* **Yes, hunting the "Closest to the Truth" failure mode.** The Adversarial harness specifically targets the Level 3 Coach-Specific failure mode—the output that looks superficially perfect but lacks authentic psychological depth.
*   **[AUDIT FACT]:** Implemented. The codebase contains `anti_draft_models.py` and an `AntiDraftCalibrator` (`anti_draft_calibrator.py`) which explicitly targets the Level 3 Coach-Specific failure mode, ensuring generated text avoids superficially correct but hollow "closest to the truth" patterns.

*   **[EMILIO COMMENTARY]:** This is genuinely great news although I would like to know which pipelines and modules are currently using this? So if none then definetely we should write how this implemented into our harnesses. VERDICT: A Receipt documentation + Epic-Story file/s should be writen about this. (Possibly using 2 or 3 these reasoning methodologies TRIZ / MCDA / SWOT / CBAR- Constraint-Based Adversarial Reasoning/ RSCS_Recursive_Signal_Compression_Systems (CBAR and RSCS are our proprietary reasoning framework))

**5. Context Memory State**
*Question:* In a multi-turn coaching session, where does short-term memory live?
*Resolution:* **Hybrid**. Local RLM Workspace handles high-speed, short-term session counters. Neo4j handles long-term relationship and meaning extraction.
*   **[AUDIT FACT]:** Neo4j graph database integration is extensively implemented across 23 files (e.g., `aria_processor.py`, `ca11_models.py`) for long-term relational memory. However, the high-speed local RLM (Recursive Language Model) Workspace for short-term session counters is unbuilt. 

*   **[EMILIO COMMENTARY]:** I mean what do you mean by multiturn coaching session?? Also yep RLM is not implemented yet and we should check where and in exactly which pipelines it actually make sense to integrate an RLM. But I would think of integratiing in recursive coaching loops, since we need multiple iterations... especially I think this is relevant for our compositions and evaluations... it can extremely valuable to manage well short-term memory and long term memory too because successful states could become useful for future succesful agentic implementations. So VERDICT: A Receipt documentation + Epic-Story file/s should be writen about this. (Possibly using 2 or 3 these reasoning methodologies TRIZ / MCDA / SWOT / CBAR- Constraint-Based Adversarial Reasoning/ RSCS_Recursive_Signal_Compression_Systems (CBAR and RSCS are our proprietary reasoning framework)) 

**6. Maturity Gating**
*Question:* Should Harness templates be version-controlled without breaking existing skills?
*Resolution:* **Immutable Compilation**. Archetype Design Brief Templates are gated (Draft -> Tested -> Stable). Once a `SKILL.md` is compiled from a template, it is locked. Upgrading the template does not break previously compiled skills.
*   **[AUDIT FACT]:** Unbuilt. While Archetype templates exist, there is no programmatic maturity gating tracking the `Draft -> Tested -> Stable` promotion lifecycle or any compilation locks preventing regression in the codebase.

*   **[EMILIO COMMENTARY]:** I don't think having fixed templates is necessarily good in production but I would keep an eye on successful ones but honestly I don't want to bias too much future implementation of skills compositions that should really remain just in time. I would rather understand the intelligence rather having them to be DUMB orchestrated. There is difference between dumple simplicity and dumbly orchestrated. Previously compiled skills are stored but and could be referenced but not necessarily. And here I would like to know like How are we going to make sure an agent use a Skill if it's not already built... so we just give to the agent the Archetype Design Brief skill... so here we are working in the Harness that build the Harness typical scenario. So the first layer is the harness being built. and once it's built then we move on and use the built harness for generation... which is also composed with other harnesses like the ones with primitives and SFL guidelines and guadrails. So basically this a manifestation of a modularly built harness. But yep we need to write a proper documentation on this and think about. VERDICT: A Receipt documentation + Epic-Story file/s should be writen about this. (Possibly using 2 or 3 these reasoning methodologies TRIZ / MCDA / SWOT / CBAR- Constraint-Based Adversarial Reasoning/ RSCS_Recursive_Signal_Compression_Systems (CBAR and RSCS are our proprietary reasoning framework))


**7. Cross-Pipeline Integration**
*Question:* Should we envision different JIT Compilers for CCF, CMF, CBCS, and V2WS (Voice2WebinarSystem)?
*Resolution:* **One Core Engine, Pipeline-Specific Adapters.** The compilation mechanics (Block A + B = C) are universal. The compiler just loads different Adapter Registries depending on the target pipeline.
*   **[AUDIT FACT]:** Implemented. The `AdapterRegistryV2Pipeline` and `adapter_registry_v2_models.py` exist, providing pipeline-specific adapters (e.g., CCF vs CMF) without cross-contamination.

*   **[EMILIO COMMENTARY]:** Yes we should absolutely envision different compilers because they are each different harnesses in my opinion. They will be composed by different modules, adapters... and have different epistemic priorities. So VERDICT: A Receipt documentation + Epic-Story file/s should be writen about this. (Possibly using 2 or 3 these reasoning methodologies TRIZ / MCDA / SWOT / CBAR- Constraint-Based Adversarial Reasoning/ RSCS_Recursive_Signal_Compression_Systems (CBAR and RSCS are our proprietary reasoning framework))

**8. Compiler Triggering (JIT vs Batch)**
*Question:* Does the Orchestrator check the Fingerprint Archive in real-time or run overnight batches?
*Resolution:* **True JIT**. The Orchestrator checks for a cached `SKILL.md` and compiles it in real-time immediately before execution if needed.
*   **[AUDIT FACT]:** Implemented. The `FingerprintArchiveEngine` (`fingerprint_archive_engine.py`) and associated models check for cached `SKILL.md` signatures to intercept execution in real-time.

*   **[EMILIO COMMENTARY]:** It truely need to be real-time as we the coaching lessons are prepared and content briefs are adapted especailly the Recording Preparation Brief which take the coach input and organize everything into a coherent Recording Elicitation Brief. Same with Personalized Lesson Drips generation. So actually we have daily batches to deliver actually I would say it's both. JIT when co-creatioin is happening and Batches compilering when delivering Drips. For V2WS scenarios is definitely a JIT scenario although highly structured because modules are foundamentally and proprietary the same because they are based on our Coaching Program. Same with the coach coaching program for their communities 30D-challenge this are adaptive under fixed constraints so the delivery is adaptive based on constraints but drips are batched. We cannot have 100000 generations JIT... for CBCS programs and challenges compilers work but they do it in batches. So we need so work to do on this one to make sure we can really optimize the JIT orchestration so that it does not ruin user experiences and coaching momentum. VERDICT: A Receipt documentation + Epic-Story file/s should be writen about this. (Possibly using 2 or 3 these reasoning methodologies TRIZ / MCDA / SWOT / CBAR- Constraint-Based Adversarial Reasoning/ RSCS_Recursive_Signal_Compression_Systems (CBAR and RSCS are our proprietary reasoning framework))

**9. Feedback Loop (SkillNet Integration)**
*Question:* How do we trace performance signals to promote Templates to "Stable"?
*Resolution:* **Social API Hooks**. We integrate directly with social media APIs (Facebook, Instagram, LinkedIn, TikTok, YouTube, X) to track views, comments, likes, and shares per video, closing the loop from output performance to template maturity.
*   **[AUDIT FACT]:** Unbuilt. There are no social media API integrations (Facebook, Instagram, LinkedIn, TikTok, X) in the codebase to track views, comments, likes, or shares, meaning the automated template promotion feedback loop cannot function.

*   **[EMILIO COMMENTARY]:** So There's potentially stable but I prefer data to help making the final decision but still with reasoning and context with the right MCDA methodology so decisions are always weighted and not absolute because parameters and conditions are always changing. But yep we'll telemetry to make sure we keep measuring and interpret meauring with multidimensional hypothesis that should be confirmed a certain number of time to increase their weigth in our evaluations. So VERDICT: A Receipt documentation + Epic-Story file/s should be writen about this. (Possibly using 2 or 3 these reasoning methodologies TRIZ / MCDA / SWOT / CBAR- Constraint-Based Adversarial Reasoning/ RSCS_Recursive_Signal_Compression_Systems (CBAR and RSCS are our proprietary reasoning framework))

**10. Adapter Registry Conflict Resolution**
*Question:* What happens if adapters inject conflicting constraints?
*Resolution:* **Pipeline Isolation (No Conflict)**. CBCS, CCF, CMF, etc., are strictly isolated pipelines. Adapters from different pipelines are never loaded together in the JIT Compiler, making cross-pipeline adapter conflicts impossible by design.
*   **[AUDIT FACT]:** Implemented. Conflict resolution is achieved via strict pipeline isolation managed within the Adapter Registry models, ensuring CBCS and CMF adapters are never loaded into the same compilation context.

*   **[EMILIO COMMENTARY]:** So each harnesses has its own validation rules that should run in isolation based on their own priciples. So external adapter are going to compete. Specialized results outputs can't challenged in their own enviroment of operationalization. VERDICT: A Receipt documentation + Epic-Story file/s should be writen about this. (Possibly using 2 or 3 these reasoning methodologies TRIZ / MCDA / SWOT / CBAR- Constraint-Based Adversarial Reasoning/ RSCS_Recursive_Signal_Compression_Systems (CBAR and RSCS are our proprietary reasoning framework))

---

## 🟡 OPEN QUESTIONS (The Next Frontier)

These questions remain open to finalize the structural integrity of the system.

**11. Negative Space Saturation**
*Question:* How do we prevent the Forbidden Vocabulary List from paralyzing the LLM?
*Resolution:* **Performance-Based Pattern Pruning**. We don't just list obvious words; we extract patterns of "the closest but obviously AI space" by comparing AI output against actual human coach performance and context from our Persuasive Speaking Program daily drips.
*   **[AUDIT FACT]:** Unbuilt. "Performance-Based Pattern Pruning" and the dynamic extraction of forbidden vocabulary patterns from daily drips do not exist in the codebase. Negative constraints still rely on static lists rather than empirical human performance data.

*   **[EMILIO COMMENTARY]:** Negative constraints need to be dynamic as well... bacause language is always adaptively changing. Meaning it has the DNA but it adapts based on each situation. VERDICT: A Receipt documentation + Epic-Story file/s should be writen about this. (Possibly using 2 or 3 these reasoning methodologies TRIZ / MCDA / SWOT / CBAR- Constraint-Based Adversarial Reasoning/ RSCS_Recursive_Signal_Compression_Systems (CBAR and RSCS are our proprietary reasoning framework))

**12. Subagent Scoping (The Critic)**
*Question:* What models run the internal evaluation loops?
*Resolution:* **Open-Source Stack exclusively**. The pipeline relies on powerful open-source models: Mistral Medium 3.5, Qwen 3.6 (35B/27B), Qwen 3.5 (397B), MoonshotAI Kimi K2.6, DeepSeek-V4-Pro, and MiniMax M2.7.
*   **[AUDIT FACT]:** Unbuilt. While there are a few hardcoded prompt references to Mistral and Qwen (`ttt_pattern_registry.py`, `aurore_v2.py`), there is no generic routing system or local deployment architecture running the specified open-source stack (Mistral Medium, Qwen 35B, MoonshotAI, DeepSeek, MiniMax) for internal evaluation loops.

*   **[EMILIO COMMENTARY]:** So we will always change models but overall we are going to host our opensource models on AWS. Since we will also be using custom models and LoRAs. VERDICT: A Receipt documentation + Epic-Story file/s should be writen about this. (Possibly using 2 or 3 these reasoning methodologies TRIZ / MCDA / SWOT / CBAR- Constraint-Based Adversarial Reasoning/ RSCS_Recursive_Signal_Compression_Systems (CBAR and RSCS are our proprietary reasoning framework))

**13. Telemetry & The "Failure Receipt"**
*Question:* How do we handle and log Block C Validation failures?
*Resolution:* **Dead-Letter Queue (DLQ) & JSON Receipts**. Best Practice: The Orchestrator catches the exception to prevent halting. It generates a JSON Failure Receipt containing `timestamp`, `target_pipeline`, `archetype_id`, and `critic_reasoning`, which is logged to Neo4j/RLM for observability while the JIT Compiler immediately triggers an autonomous retry.
*   **[AUDIT FACT]:** Unbuilt. There is no `FailureReceipt` object, Dead-Letter Queue (DLQ), or mechanism for the orchestrator to catch validation exceptions without halting. Failures currently raise standard Python exceptions or log to the `ReceiptChain`, but do not trigger autonomous DLQ retries.

*   **[EMILIO COMMENTARY]:** Honestly I need more education on this because I do understand what failure mode like DLQ is... but I would say halting could be solved recursevely in my opinion.  But let's think about it and write VERDICT: A Receipt documentation + Epic-Story file/s should be writen about this. (Possibly using 2 or 3 these reasoning methodologies TRIZ / MCDA / SWOT / CBAR- Constraint-Based Adversarial Reasoning/ RSCS_Recursive_Signal_Compression_Systems (CBAR and RSCS are our proprietary reasoning framework))


**14. Cross-Pollination of Intelligence**
*Question:* Are templates siloed between CCF (Written) and CMF (Video)?
*Resolution:* **No Silos (Precursor Architecture)**. Archetypes produce *ingredients* that produce skills JIT. Written content (CCF) is never published as standalone scripts; it serves entirely as the coaching practice/recording precursor for the final Video (CMF). They are intrinsically linked.
*   **[AUDIT FACT]:** Structural only. The models map textual schemas as precursors for audio/visual rendering, but there is no explicit CCF-to-CMF unified execution pipe that forces text to act solely as a recording precursor.

*   **[EMILIO COMMENTARY]:** This Pipelines are not built yet. Everything regarding the harneses pipelines, slash commands etc... need to be built. so let's plan about it. VERDICT: A Receipt documentation + Epic-Story file/s should be writen about this. (Possibly using 2 or 3 these reasoning methodologies TRIZ / MCDA / SWOT / CBAR- Constraint-Based Adversarial Reasoning/ RSCS_Recursive_Signal_Compression_Systems (CBAR and RSCS are our proprietary reasoning framework))


**15. User Hand-off (Quarantine UX)**
*Question:* What is the UX for a "PARTIAL_MANUAL" quarantine?
*Resolution:* **Autonomous Self-Healing**. There is no manual UX intervention. The system is robust enough to handle missing inputs via agentic resolution and automatic retries. The agents solve it themselves.
*   **[AUDIT FACT]:** Partial implementation. Quarantine state models exist (`phase0_workspace_models.py`, `receipt_guard_models.py`), but the autonomous self-healing agentic retry loops that resolve missing variables without manual intervention are unbuilt.

*   **[EMILIO COMMENTARY]:** This is not built but I would curious actually to have an audit of why even this could happen we actually build code and harnesses around this to make failure impossible. This is why we use code and not just text based prompts. Because we also actually if possible want to avoid recursive loops if they can easily be solved with code. so let applyi this VERDICT: A Receipt documentation + Epic-Story file/s should be writen about this. (Possibly using 2 or 3 these reasoning methodologies TRIZ / MCDA / SWOT / CBAR- Constraint-Based Adversarial Reasoning/ RSCS_Recursive_Signal_Compression_Systems (CBAR and RSCS are our proprietary reasoning framework))

