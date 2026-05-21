# MCDA Audit: Text Fine-Tuning & Activation Steering (Batch 3/4)

**Date:** April 15, 2026
**Focus:** Enhancing the Sovereign Agentic Harness, Activation Steering precision (CCV), SLM Orchestration, and CA11 alignment.

## Executive Summary
This third batch of literature focuses intensively on the actual mechanics and limitations of Low-Rank Adaptation (LoRA) compared to Full Fine-Tuning (FFT), alongside advanced steering mechanisms like KV Cache Steering and CASAL. The synthesis reveals critical vulnerabilities in relying solely on standard LoRA for deep reasoning acquisition, while simultaneously presenting high-efficiency alternatives for amortized learning and on-the-fly SLM reasoning induction.

## Synthesized Papers & Core Findings

### 1. Hallucination reduction with CASAL (Contrastive Activation Steering For Amortized Learning)
*   **Core Premise:** Introduces CASAL, an amortized learning approach to contrastive activation steering that reduces hallucinations without the computational overhead of continuous test-time intervention.
*   **CCV/Harness Integration:** **Critical for CCV Signal vs. Noise.** CASAL offers a pathway to pre-compute or amortize the steering vectors used to dampen hallucinated "noise" (e.g., generic cheerleader coaching) and amplify structural "signal" (e.g., rigid CA11 framework adherence) in SLMs during the rigorous validation phase.

### 2. KV Cache Steering for Inducing Reasoning in Small Language Models
*   **Core Premise:** By manipulating the KV cache during generation, reasoning capabilities (like chain-of-thought) can be induced in SLMs that typically struggle with multi-step logic.
*   **CCV/Harness Integration:** **Transformative for the SLM Orchestration Matrix.** Instead of relying solely on larger models (Gemma 4 31B) for reasoning, we can employ KV Cache Steering on Qwen 3-4B models to force deterministic reasoning paths during the Builder/Critic loops without needing a massive fine-tuning dataset.

### 3. LoRA Fine-Tuning Efficiently Undoes Safety
*   **Core Premise:** Demonstrates how easily LoRA fine-tuning can bypass or degrade safety alignments and RLHF protections baked into base models.
*   **CCV/Harness Integration:** **Security/Alignment Warning.** In the context of CCP, this means LoRA can quickly un-align an SLM from the strict CA11 guidelines if the tuning data isn't perfectly curated. It necessitates a rigid deterministic oversight layer (RISER) to govern LoRA-tuned outputs.

### 4. LoRA Land: 310 Fine-tuned LLMs
*   **Core Premise:** A large-scale empirical study benchmarking hundreds of LoRA models, revealing patterns in where LoRA succeeds (domain adaptation) and where it fails (deep reasoning acquisition).
*   **CCV/Harness Integration:** Provides empirical grounding for our model routing strategy. LoRA is validated for tone/style (human emulation in Gemma 4) but confirmed weak for novel logic, reinforcing the need for steering and JIT compilers.

### 5. LoRA Learns Less and Forgets Less
*   **Core Premise:** LoRA causes significantly less catastrophic forgetting than FFT, but also struggles to internalize fundamentally new knowledge that isn't functionally present in the base model's pre-training.
*   **CCV/Harness Integration:** **Architectural Pillar.** Dictates our training partition: We cannot use LoRA to teach the SLMs entirely new CA11 ontological frameworks. We must use RAG/Context-injection for the knowledge, and use LoRA *only* to adapt the stylistic expression and formatting of that knowledge.

### 6. LoRA vs Full Fine-tuning: An Illusion of Equivalence
*   **Core Premise:** Punctures the myth that LoRA can achieve parity with FFT for complex tasks. LoRA operates primarily in a low-rank subspace that restricts complex multi-dimensional capability acquisition.
*   **CCV/Harness Integration:** **Validation of the Dual-Stack Approach.** We must discard the idea that a heavily LoRA-tuned 4B model will rival a 31B model for complex reasoning. It mandates the "Base 31B for heavy logic + LoRA 4B for simple routing/formatting" Sovereign stack.

### 7. LoRA+: Efficient Low Rank Adaptation of Large Models
*   **Core Premise:** Explores optimizations to the LoRA architecture (like different learning rates for A and B matrices) to improve feature learning efficiency.
*   **CCV/Harness Integration:** A pure optimization protocol to be added to the CCP Training scripts to maximize the yield of our limited GPU/compute budget when prepping SLMs.

## MCDA Strategic Integration Plan (Batch 3)

1.  **Adopt "Knowledge via RAG, Style via LoRA" Rule:** Formally document in the Architectural Brief that LoRA will *not* be used to teach models the CCV Framework. LoRA is restricted to stylistic adaptation and output formatting.
2.  **Prototype KV Cache Reasoning:** Initiate a test branch integrating KV Cache Steering on the Qwen-3/4B Critic agents to force step-by-step reasoning during Builder/Critic evaluation.
3.  **Implement CASAL Amortization:** For hallucination reduction (specifically preventing the model from inventing non-CA11 coaching modalities), deploy amortized contrastive vectors to speed up inference compared to standard dynamic steering.

## Next Actions
- Process Batch 4.
- Move Batch 3 files to the `relevant` folder.
