# Sovereign NIM Integration MCDA: Agentic Reasoning & Script Generation Models

This plan outlines the creation of the 3200-3400 word Multi-Criteria Decision Analysis (MCDA) documentation. The goal is to evaluate the 5 identified open-source models (Qwen 3.5 397B, gemma4-31b-Opus-4.6-reasoning, GLM-5 Turbo, Kimi-K2-Thinking, Kimi-K2.5) and assign them specific roles within the CCP ecosystem—specifically for the **JIT Skill Compiler Architecture**, while strictly adhering to the **Sovereign AWS + Nvidia NIM container model**.

## User Review Required

> [!IMPORTANT]
> Please review the proposed **Role Assignments** for each model based on their benchmark analytics before I proceed to draft the full 3200+ word MCDA. Generating the document will be extremely detailed, so determining the correct architectural alignment now is critical.

## Proposed Changes 

### The MCDA Evaluation Criteria
To evaluate these models from first principles, I will map their benchmark strengths directly to the **JIT Skill Compiler Architectural Mandates**:

1. **Instruction Following & Constraint Adherence:** Critical for avoiding Mandate M4 (TTT violations) and honoring Mandate M7 (Anti-Draft Level 1/2/3).
2. **Semantic Repulsion:** The ability to avoid the "statistical centroid"—specifically avoiding purple prose, positivity bias, and amateurish constructions.
3. **Cognitive Architecture (Thinking Protocols):** Evaluating the use of Chain-of-Draft, Interleaved Thinking, and Preserved Thinking (as highlighted in the GLM-5 paper).
4. **VRAM Economics & Batched Compute:** Adhering to the newly established Cold Start Physics and CRON-triggered pre-warm model on AWS EC2 G5/P4d instances via Nvidia NIM.
5. **Creative Resonance:** Strength in Show-Don't-Tell, emotional depth, pacing, and dialogue (critical for specific archetypes like Discovery or Storytelling).

### Model Role Hypotheses & Strategy

Based on the provided benchmark images and technical documents, here is the proposed integration strategy for the MCDA:

1. **GLM-5 Turbo (zai-org/GLM-5.1)**
   - **Data Profile:** Highest pacing (1.0), best at avoiding purple prose (0.65), avoids positivity bias, solid instruction following (0.25). Features "Interleaved Thinking" and "Preserved Thinking" native architectural traits.
   - **Proposed Ecosystem Role: The Critic Subagent (Pass 2) & The Assembler.**
   - **Justification:** Because of its high instruction following and strong semantic repulsion against purple prose/positivity bias, GLM-5 is mathematically optimal for evaluating Drafts against the 3-Level Anti-Draft Architecture. It will not hallucinate emotions and will strictly verify the Forbidden Vocabulary List.

2. **Kimi-K2.5 (moonshotai/Kimi-K2.5)**
   - **Data Profile:** Perfect Descriptive Imagery (1.0), extraordinary Creativity (0.9), elegant prose. *However*, catastrophic Instruction Following (-1.0) and poor coherence.
   - **Proposed Ecosystem Role: Emilio Generation Agent (Pass 1 - Draft ONLY).**
   - **Justification:** It produces vivid, non-amateurish raw material. It cannot be trusted to follow the SPR constraint ordering or negative space logic perfectly on its own, meaning it *must* be heavily policed by the GLM-5 Critic in Pass 2. It acts as the raw creative engine.

3. **Kimi-K2-Thinking (moonshotai/Kimi-K2-Thinking)**
   - **Data Profile:** Perfect Pacing (1.0), high creativity, good Emotional Depth (0.45), but struggles massively with Purple Prose (-1.0).
   - **Proposed Ecosystem Role: Emotional DNA Extractor & CRAL Connector.**
   - **Justification:** Since it thinks specifically to establish pacing and depth, it's best utilized in Tier 1 / Tier 2 Orchestration to map CRAL moments (M2-M7) into emotional narratives, before final compilation. 

4. **Qwen 3.5 397B A17B**
   - **Data Profile:** Unmatched Show-Don't-Tell (1.0), excellent Dialogue (0.6), but very poor sentence flow (-1.0) and negative instruction following. Massive VRAM footprint.
   - **Proposed Ecosystem Role: The Sovereign Visual Research Engine (SVRE) & Deep Offline Synthesis.**
   - **Justification:** This MoE leviathan is too expensive for single-token JIT script assembly. However, its immense reasoning and visual capability make it optimal for Scheduled Pre-Warm Deep Batching—verifying visuals, scoring SVRE outputs, or running heavy offline data processing.

5. **gemma4-31b-Opus-4.6-reasoning**
   - **Data Profile:** High creativity (1.0), solid emotional depth. Extremely lightweight.
   - **Proposed Ecosystem Role: Psychological Routing Engine & Builder Engine.**
   - **Justification:** Its fast inference and decent instruction following make it perfect for rapid Phase 1 logic tasks, such as generating the `psych_routing_brief.json` (DEP-ENG-016) and evaluating Audience Maturity.



6. **Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive**
   - **Data Profile:** 35B dense model, lobotomized safety filters, 3B active parameters per token.
   - **Proposed Ecosystem Role: Escape-Mode Generator (Comedy & Raw Truth)**
   - **Justification:** Avoids the 'statistical centroid' of safe HR corporate humor. Since it has no boundaries, it creates explosive drafts for specific archetypes. Evaluated and sanitized down by GLM-5 Turbo in Pass 2.
### Final Document Structure
The 3200-3400 word MCDA will be structured as follows:
- **I. Executive Summary & First Principles:** Sovereign AWS Architecture + The Vibe-to-Agentic Paradigm Shift.
- **II. Baseline Analysis of 5 Foundation Models:** Deep dive into the radar charts and their statistical meaning.
- **III. The Engine Matrix:** Specific assignments for the JIT Compiler Pipeline (Draft, Critic, Synthesis, Routing).
- **IV. Agentic Engineering Workflows:** How GLM-5's Interleaved/Preserved thinking rewires the Critic Subagent.
- **V. Infrastructure & Batch-Economics:** NIM Deployment strategies and VRAM limits for running a 397B parameter model alongside a 31B and Kimi architectures.
- **VI. The Anti-Draft Simulation:** How Kimi-K2.5 Draft vs. GLM-5 Critic interplay functions. 

## Open Questions

- Do you agree with using **GLM-5 Turbo** as the strict Critic (Pass 2) and **Kimi-K2.5** as the untamed Generator (Pass 1) for the Draft/Critic/Synthesis loop?
- For **Qwen 3.5 397B A17B**, given the extreme VRAM costs, do you approve of relegating it solely to offline, asynchronous deep-batch workloads rather than real-time script generation?

## Verification Plan
1. The user provides approval of the model role-mapping hypothesis.
2. I will write the final `MCDA_Sovereign_NIM_Writing_Reasoning_Models.md` artifact (3200-3400 words) using rigorous academic and system-architecture formatting.
