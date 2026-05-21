# MCDA Audit: Text Fine-Tuning & Activation Steering (Batch 4/4)

**Date:** April 15, 2026
**Focus:** Enhancing the Sovereign Agentic Harness, Activation Steering precision (CCV), SLM Orchestration, and CA11 alignment.

## Executive Summary
This final batch of literature introduces the most advanced steering architectures to date, moving beyond simple static vectors into dynamic, router-based coordination and layer-selective interventions. It introduces RISER for orchestrating multiple cognitive primitives, SV-RAG for efficient multipage retrieval using MLLM hidden states, and Selective Steering for avoiding coherence collapse—giving CCP a blueprint for building a highly resilient, deterministic Cognitive Control Vehicle (CCV).

## Synthesized Papers & Core Findings

### 1. RISER: Orchestrating Latent Reasoning Skills for Adaptive Activation Steering
*   **Core Premise:** Moves away from single, static steering vectors. RISER trains a lightweight router to dynamically select and compose multiple latent cognitive primitives (e.g., math reasoning, ethical alignment) based on the input, applying them as activation interventions.
*   **CCV/Harness Integration:** **The Ultimate CCV Router.** RISER perfectly mirrors the need of the Conscious Coaching Platform. Instead of statically forcing "strict CA11 framework" or "Jim Rohn tone" onto the model, we can treat these as distinct, composable cognitive primitives. We will build a CCV Router that dynamically blends "Empathy", "CA11 Structural Rigidity", and "Socratic Questioning" based on the exact user prompt.

### 2. Selective Steering: Norm-Preserving Control Through Discriminative Layer Selection
*   **Core Premise:** Highlights that steering at non-discriminative layers causes generation collapse and norm distortion. It proposes applying norm-preserving rotations only at specific layers where the contrastive features (e.g., harmless vs. harmful) show opposite-signed alignment.
*   **CCV/Harness Integration:** **Critical stability upgrade.** Previously, activation steering risked breaking the SLMs. We must adopt Selective Steering's layer-selection algorithm. When forcing CA11 structural behaviors on the Qwen-3/4B models, we will mathematically identify only the susceptible layers, preventing the model from collapsing into repetitive loops during agentic reasoning.

### 3. SV-RAG: LoRA-Contextualizing Adaptation of MLLMs for Long Document Understanding
*   **Core Premise:** Proposes using the hidden states of MLLMs themselves as an efficient retriever for long documents, optimizing the process via dual LoRA adapters (one for retrieval, one for QA).
*   **CCV/Harness Integration:** Extremely relevant for the Trivianar and Long-Context user history. CCP can use a dual-LoRA setup on our base Qwen models: one LoRA adapter dedicated completely to retrieving the client's past history, and another for generating the coaching response, drastically reducing the token cost.

### 4. The Rogue Scalpel: Activation Steering Compromises LLM Safety
*   **Core Premise:** Demonstrates that, much like LoRA, activation steering can easily serve as an attack vector, precisely disabling safety guardrails and leading to catastrophic behavior.
*   **CCV/Harness Integration:** **OODA Loop Threat Mitigation.** The Sovereign Harness must explicitly isolate the steering vectors from user-injected text. If a user inputs text that mathematically aligns with an inverse-vector, it could disable the CA11 structural restrictions. We must scrub user input context before calculating steering application.

### 5. Steer2Edit & Scaling Embeddings
*   **Core Premise:** Demonstrates the value of transitioning from mere steering to component-level editing, and scaling embedding dimensionality over scaling expert counts.
*   **CCV/Harness Integration:** Further validates that for SLMs, massive embedding/contextual architectures and precise component editing will yield higher RoI than simply switching to larger models or relying purely on MoE architectures.

## MCDA Strategic Integration Plan (Batch 4)

1.  **Draft the RISER Router Blueprint:** Update the CCP Architecture Brief to include a lightweight meta-router. This router will analyze incoming Telegram messages and emit an intervention mask, activating the required coaching skills (e.g., empathy, probing, reframing) in activation space.
2.  **Integrate Layer-Selective Steering:** Halt all global steering experiments. Transition all CCV steering mechanisms over to the Selective Steering norm-preserving protocol, ensuring zero coherence collapse on the 4B SLMs.
3.  **Evaluate SV-RAG for User Memory:** Begin prototyping the Dual-LoRA approach for retrieving user history, treating past sessions as the "long document" described in the SV-RAG paper.

## Next Actions
- Process complete. All batches analyzed.
- Move remaining valid papers to the `relevant` folder.
