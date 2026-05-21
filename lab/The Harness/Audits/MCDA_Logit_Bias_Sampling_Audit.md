# MCDA Audit: Logit Bias & Constrained Sampling Architectures

**Date:** April 16, 2026
**Target Batch:** `lab\LoRa Activation Steering and Embegging papers\Text fine-tuning`
**Focus:** Analyzing exact sampling mechanics, logit-space injection, and decoding optimizations for the Sovereign NIM transit layer.

---

## 🟢 Approved for Integration (Scores >80/100)

### 1. Limits of n-gram Style Control for LLMs via Logit-Space Injection
- **Score:** 91/100
- **Key Finding:** Attempting to inject writing style into an LLM by positively shifting the logits at decoding time is extremely fragile; it collapses into incoherence if the control parameter $λ$ moves past $0.1$. The paper concludes that parameter-efficient fine-tuning (LoRA) is strictly superior for style control.
- **CCP Application (Critical Rule Validation):** This mathematically proves our architectural boundary. We must use **LoRA / Activation Steering** to inject the "Voice DNA" (positive control). We use **Logit Bias** *strictly* as a negative mask (e.g. setting $bias=-100$ for words like "apologize" or "AI"). We never use it to induce style.

### 2. FlashSampling: Fast and Memory-Efficient Exact Sampling
- **Score:** 89/100
- **Key Finding:** During autoregressive decoding, sampling from the logit tensor usually triggers massive memory traffic across the GPU. FlashSampling fuses the sampling directly into the LM-head matrix multiplication, never materializing the logits tensor in HBM. This yields up to a 19% reduction in decode latency in vLLM.
- **CCP Application:** We must configure our vLLM / NIM deployment parameters to utilize fused FlashSampling. This is critical for keeping our Pipecat WebRTC response times to the `<800ms` strict requirement when the Voice engine is active.

### 3. Logits-Based Finetuning
- **Score:** 85/100
- **Key Finding:** Standard Supervised Fine-Tuning (SFT) forces the model to fit a single ground-truth token, ignoring the rich probability distribution of other valid linguistic choices. By training on the soft probability distribution (logits) of a teacher model, SLMs learn significantly better syntactic diversity.
- **CCP Application:** When fine-tuning our localized Qwen-3B models using the Gemma-4-31B logic, we must use Logit distillation rather than flat text dataset pairs.

---

## 🔴 Excluded / Rejected (Scores <80/100)

### 4. AMU-Tuning: Effective Logit Bias for CLIP-based Few-shot Learning
- **Score:** 30/100
- **Reason:** Explicitly designed for CLIP vision models (image alignment). We are optimizing LLM and text-based generative pipelines. Not relevant to the Sovereign Harness text orchestrator.

### 5. Kernel-Smith: A Unified Recipe for Evolutionary Kernel Optimization
- **Score:** 45/100
- **Reason:** Covers raw Evolutionary CUDA kernel optimization using LLMs. While interesting for low-level NVIDIA engineers, CCP operators rely on deployed vLLM/NIM containers. We do not write custom CUDA kernels.

### 6. Quamba2 & Sparsified State-Space Models (SSMs)
- **Score:** 40/100
- **Reason:** Both of these papers optimize **State Space Models (like Mamba)**. Our entire deterministic pipeline is built on the Transformer architecture (Qwen, LLaMa, Gemma) leveraging KV Cache techniques. Mamba optimizations are incompatible with our stack.

---

## Curriculum Impact (Chapter 05 & 06)

I will loop **FlashSampling** explicitly into **Chapter 05 (AWS Foundations + Nvidia NIM)** right alongside our KV Cache rules. It perfectly solves the decoding latency bottleneck. 

I will map the **Fragility of Positive Logit Injection** to **Chapter 06 (Harness Engineering)** to formalize the rule: *Logit Bias is for negative constraints only; LoRA is for positive style.*
