# MCDA: Text Fine-Tuning & LoRA Optimization (Batch 1/4)

**Context:** Evaluating the first 13 research papers (out of 52) regarding LoRA training, Activation Steering, and Fine-tuning. The goal is to determine their utility for the Conscious Coaching Platform (CCP) and the Conscious Coaching Video (CCV) pipeline (especially the CMF Beat Cluster and Agentic Reasoning).

## 1. Evaluation Criteria (Weights)
- **LoRA/Fine-Tuning Efficacy (35%):** Relevance to optimizing LoRA strategies, mitigating forgetting, and tuning Small Language Models (SLMs).
- **Activation/Representation Steering (30%):** Applicability to sovereign agentic control, behavioral shaping, and mitigating overconfidence without full retraining.
- **CCV/CMF Video & Audio Synergy (20%):** Relevance to the current CMF Beat Cluster, visual narrative continuity, and audio-video rhythmic alignment.
- **Creative/Scripting Impact (15%):** Usefulness for generative writing, coaching dialogue, and platform specific tasks (e.g., humor, tone).

---

## 2. Paper Scoring & Audit

### 1. A Unified Study of LoRA Variants Taxonomy
- **Relevance:** High
- **Score:** 88/100
- **Rationale:** Deep dive into LoRA variants. Crucial for establishing our foundational fine-tuning plan for CCP sovereign instances. 
- **Action:** KEEP

### 2. ALIVE ANIMATE YOUR WORLD WITH LIFELIKE
- **Relevance:** Medium-High
- **Score:** 75/100
- **Rationale:** Pertains to visual animation and lifelike dynamics. Will be useful for the CMF phase.
- **Action:** KEEP

### 3. ALLoRA Adaptive Learning Rate Mitigates
- **Relevance:** High
- **Score:** 90/100
- **Rationale:** Directly addresses LoRA training inefficiencies and catastrophic forgetting. Essential for sustained CCP optimization.
- **Action:** KEEP

### 4. ASA Training-Free Representation Engineering for Tool-Calling Agents
- **Relevance:** High
- **Score:** 85/100
- **Rationale:** Agent steering for tool-handling without retraining aligns perfectly with CCP's Sovereign Agentic Harness.
- **Action:** KEEP

### 5. Activation Steering for Accent Adaptation in Speech Foundation Models
- **Relevance:** Medium
- **Score:** 65/100
- **Rationale:** Potentially relevant to the Jim Rohn / Audrey Voice engines, but specific to accent adaptation.
- **Action:** KEEP (File under Audio/Speech optimizations)

### 6. Activation Steering for Accent-Neutralized Zero-Shot Text-To-Speech
- **Relevance:** Medium
- **Score:** 62/100
- **Rationale:** Same as above. Good for zero-shot Voice synthesis protocols in the pipeline.
- **Action:** KEEP (File under Audio/Speech optimizations)

### 7. BottleHumor Self-Informed Humor Explanation using the Information Bottleneck Principle
- **Relevance:** Low
- **Score:** 20/100
- **Rationale:** Specialized in humor explanation rather than narrative generation or agent reasoning. Does not align with immediate CCV or CCP priorities.
- **Action:** DISCARD

### 8. CFunModel A Funny Language Model Capable of Chinese Humor Generation and Processing
- **Relevance:** Low
- **Score:** 15/100
- **Rationale:** Domain-specific (Chinese Humor), fundamentally unsuited to CCP's current requirements.
- **Action:** DISCARD

### 9. Can Good Writing Be Generative Expert-Level AI Writing
- **Relevance:** High
- **Score:** 80/100
- **Rationale:** Important for generative script writing, coaching narratives, and maintaining the “mythos” of expert CA11 output.
- **Action:** KEEP

### 10. CleanComedy Creating Friendly Humor through Generative Techniques
- **Relevance:** Low
- **Score:** 25/100
- **Rationale:** Dataset/generation focused on "friendly humor". Too niche and distracting for the Sovereign Coaching stack.
- **Action:** DISCARD

### 11. Combinatorial Controlled Variation (Claude Mythos & Activation Steering)
- **Relevance:** Critical
- **Score:** 98/100
- **Rationale:** Lays the explicit groundwork for CCV framework, blending prompting + latent structure + activation steering. The blueprint for avoiding "brain damage" while retaining precision control.
- **Action:** KEEP (Core Reference)

### 12. Controlling Large Language Model Agents with Entropic Activation Steering
- **Relevance:** Critical
- **Score:** 95/100
- **Rationale:** EAST methodology mitigates agent overconfidence and explicitly enforces exploration via representation-space modifications. Central to building the deterministic OODA loop agents.
- **Action:** KEEP (Core Reference)

### 13. CutClaw Agentic Hours-Long Video Editing via Music Synchronization
- **Relevance:** Critical
- **Score:** 95/100
- **Rationale:** Highly aligned with the CMF Beat Cluster phase. Proposes an agent-based model to edit video strictly to a rhythmic music timeline. The exact solution proposed for combining dialogue/vision/music matching in NIS/CMF. 
- **Action:** KEEP (Core Reference)

---

## 3. Execution Directives
Based on the scoring above:
- **Folders Created:** `relevant` and `not_relevant` in `D:\Work\The Conscious Coaching Factory\lab\LoRa Activation Steering and Embegging papers\Text fine-tuning`
- **Kept (Relevant):** Papers 1, 2, 3, 4, 5, 6, 9, 11, 12, 13
- **Discarded (Not Relevant):** Papers 7, 8, 10
