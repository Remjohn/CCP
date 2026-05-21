# Voice Finetuning and Adapter Strategy
**Date:** 2026-05-01  
**Status:** Training Strategy  
**Context:** Coach-specific priors, expressive fidelity, efficient training

## 1. Core Thesis

Fine-tuning is powerful, but only after the data and evaluation stack are ready.

The first tuning objective should not be "make it emotional."
It should be:
- preserve coach identity
- reduce drift
- improve coach-specific phrasing behavior
- support expressive retrieval more faithfully

## 2. Preferred Training Order

### Stage 1
No tuning yet.
Build:
- expressive memory bank
- primitive taxonomy
- score compiler
- evaluation framework

### Stage 2
Train coach-specific adapters or LoRAs on the primary model.

Focus on:
- timbre fidelity
- cadence fidelity
- phrase landing tendencies
- stable short-to-medium note rendering

### Stage 3
Train expressive state adapters only if needed.

Examples:
- reflective authority
- challenge mode
- celebratory warmth

These should be optional and evidence-driven.

### Stage 4
Apply preference optimization later if evaluation shows strong value.

## 3. Why Adapters Beat Full Finetunes Early

Adapters are better early because they are:
- cheaper
- easier to compare
- easier to version
- easier to revoke
- easier to route per coach

## 4. What Not To Tune First

Do not first tune for:
- exaggerated emotion
- cinematic sound
- gimmicky expressiveness
- sonic garnish

Tune first for:
- identity
- stability
- controlled responsiveness

## 5. Final Principle

Fine-tuning should follow ontology and evaluation, not replace them.
