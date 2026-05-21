# MOSS + Voxtral Model Strategy
**Date:** 2026-05-01  
**Status:** Technical Strategy  
**Context:** Coach voice generation, CBCS, Voice Speaking Program, interview-driven corpus building

## 1. Core Answer

We should **not** try to merge MOSS and Voxtral into one live blended output path at the start.

That would likely:
- increase complexity too early
- double debugging burden
- split fine-tuning effort
- create evaluation noise
- slow down the learning loop

The better strategy is:

1. choose one primary rendering backbone
2. use the other as a benchmark and research comparator
3. only introduce dual-model routing if evaluation data proves a real advantage

## 2. Recommended Strategy

### 2.1 Primary research/control backbone: `MOSS-TTS`

Use MOSS as the main voice generation backbone for the first serious architecture phase because it better supports:
- controllable structure
- duration control
- long-form research
- coach-specific identity preservation
- mathematically grounded runtime control layers

MOSS fits our desire to build:
- a Voice DNA base manifold
- a transformation layer
- segment-level prosody scoring
- render-time evaluation and correction

### 2.2 Expressivity benchmark and possible future production route: `Voxtral`

Use Voxtral as:
- a listening benchmark
- a human-preference benchmark
- a reference-conditioned expressivity benchmark
- a possible short-form production candidate later

Voxtral is especially valuable for testing:
- emotional realism
- prompt-reference expressivity transfer
- shorter premium voice-note performance
- latency-sensitive experiences

## 3. What We Should Not Do

Do not start with:
- dual fine-tuning both models in parallel
- blending outputs from both models into one clip
- maintaining two full production render stacks before evaluation criteria are stable
- training two adapter families before we know what the controller really needs

This would create false complexity.

## 4. The Correct Use of Both Models

The best use of both models is sequential and comparative:

### Phase A
- Build the memory bank
- Build the primitive ontology
- Build the scoring and evaluation layer
- Render primarily with MOSS

### Phase B
- Render the same controlled test set with Voxtral
- Compare human preference, emotional accuracy, drift, identity fit, and segment fidelity

### Phase C
- If Voxtral clearly wins in a narrow domain, use it selectively

Examples of selective use:
- Voxtral for short expressive broadcasts
- MOSS for longer coaching reflections
- MOSS for voice pedagogy demonstrations
- Voxtral for rapid pre-interview or challenge voice-note UX tests

That is not "combined rendering."
It is **evidence-based routing**.

## 5. Model-Routing Principle

The routing rule should be:

**one score, one renderer, one evaluation packet**

Meaning:
- a note is compiled once
- rendered by one chosen model
- evaluated against target metrics

This preserves clean testing.

If we later support both models, the routing logic should be explicit:

- use MOSS when control precision matters most
- use Voxtral when expressive naturalness wins clearly on short-form human evals

## 6. Fine-Tuning Rule

Do not fine-tune both models first.

Fine-tune only after:
- the expressive memory bank exists
- the primitive ontology is usable
- the evaluation packet is stable
- the benchmark corpus is ready

Then:
- fine-tune the primary model first
- compare against untuned Voxtral
- only tune the second model if there is a strong strategic reason

## 7. Final Recommendation

The correct answer is:

**use both models strategically, but not symmetrically.**

That means:
- `MOSS` first as the main controllable system
- `Voxtral` second as the expressive benchmark and possible selective route

This gives us:
- less wasted effort
- cleaner experimentation
- better measurement
- faster learning

The moat is not "we use two models."
The moat is:

**we know exactly why a model is being used, for which task, with which control layer, and how to measure whether it actually performs better.**
