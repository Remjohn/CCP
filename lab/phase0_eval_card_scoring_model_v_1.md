---
type: architecture-source-of-truth
author: Codex synthesis for CCP
date: 2026-05-19
status: Proposed Source of Truth
dependencies:
  - D:\Work\The Conscious Coaching Factory\docs\prd\modules\PRD_01_CCP_Platform_Strategy.md
  - D:\Work\The Conscious Coaching Factory\docs\prd\modules\PRD_02_CCF_Content_Factory.md
  - D:\Work\The Conscious Coaching Factory\docs\prd\modules\PRD_09_CPSC_Silent_Referral.md
  - D:\Work\The Conscious Coaching Factory\lab\subliminal_function_layer_for_ccp_v_1.md
  - D:\Work\The Conscious Coaching Factory\lab\ccp_biological_orchestration_model_v_1.md
  - D:\Work\The Conscious Coaching Factory\lab\OmniShotCut Holistic Relational Shot Boundary.md
---

# Phase-0 Eval Card Scoring Model

## 1. Purpose

This note defines the scoring language for the Phase-0 audit stack.

Its job is to prevent three failure modes:

1. generic content-marketing scorecards
2. internal eval sprawl with no stable public surface
3. pretty audit cards that are disconnected from canonical CCP judgment

The governing principle is:

**the eval system is canonical; the card system is the visible game layer on top of it.**

---

## 2. The Main UI Scores

Every visible audit card should expose:

- a large content thumbnail
- one overall score from `0-99`
- six main visible scores from `0-99`
- one negative warning score from `0-99`

The final visible score set is:

1. `Humanity`
2. `Presence`
3. `Trust`
4. `Memorability`
5. `Resonance`
6. `Signal`

Separate warning score:

7. `AI Slop Risk`

These labels are intentionally simple.
They should be understandable without knowing internal CCP jargon.

---

## 3. Why These Scores

### 3.1 Humanity

Question:

- does this feel like a real person with lived experience?

### 3.2 Presence

Question:

- does this person feel worth paying attention to?

This is where:

- aura
- confidence
- charisma
- conviction
- delivery magnetism
- energetic clarity

become measurable.

### 3.3 Trust

Question:

- do I believe this signal and does it feel earned?

### 3.4 Memorability

Question:

- will this survive beyond the scroll?

### 3.5 Resonance

Question:

- did this emotionally and symbolically land?

### 3.6 Signal

Question:

- does this cut through noise with sharp identity and non-generic specificity?

`Signal` replaces abstract terms like `Distinction`.
It is simpler, faster, and more intuitive.

### 3.7 AI Slop Risk

Question:

- how strongly does this feel flattened, over-smoothed, generic, fake-deep, or statistically familiar?

This remains separate because:

- high slop risk can poison otherwise decent scores
- users understand a danger score quickly
- it makes the audit more entertaining and more honest

---

## 4. Internal Metric Clusters

The visible scores are not raw categories.
They are weighted projections of deeper internal metrics.

### 4.1 Humanity Cluster

Internal metrics:

- lived experience density
- process transparency
- emotional specificity
- human texture
- non-synthetic rhythm
- selective imperfection
- vulnerability realism

### 4.2 Presence Cluster

Internal metrics:

- conviction density
- aura intensity
- energetic stability
- delivery magnetism
- authority embodiment
- confidence clarity
- speaker charge preservation

### 4.3 Trust Cluster

Internal metrics:

- proof density
- visible reality anchors
- credibility congruence
- non-performative authority
- consistency with prior signal
- dignity preservation
- semantic integrity carry-through

### 4.4 Memorability Cluster

Internal metrics:

- phrase compression
- symbolic recall
- contrast retention
- identity imprinting
- pattern stickiness
- hook persistence
- image recall strength

### 4.5 Resonance Cluster

Internal metrics:

- emotional charge
- subtext depth
- symbolic weight
- atmosphere coherence
- identity recognition
- tension carry
- felt relevance

### 4.6 Signal Cluster

Internal metrics:

- anti-genericity
- opinion sharpness
- worldview clarity
- niche specificity
- personality signature
- perceptual distinctiveness
- anti-centroid integrity

### 4.7 AI Slop Risk Cluster

Internal metrics:

- dead polish
- false depth risk
- over-smoothing
- synthetic authority cues
- statistical familiarity
- template dependence
- generic rhythm dependence

---

## 5. Hidden Support Clusters

Not every important metric should be visible on the card face.

The system should also maintain hidden support clusters that feed weighting logic:

- `Structure`
  - archetype fidelity
  - sequencing
  - narrative gravity
  - pacing coherence
- `Actionability`
  - next-step clarity
  - motivational pull
  - behavioral readiness
- `Visual Proof`
  - reality anchoring in imagery
  - screenshot / frame proof strength
- `Caption Alignment`
  - caption-to-image or caption-to-video coherence
- `Temporal Craft`
  - transition coherence
  - shot continuity
  - scene salience distribution

These should often shape visible scores without always being visible themselves.

For example:

- `Actionability` can influence `Trust`, `Presence`, and `Signal`
- `Structure` can influence `Memorability`, `Resonance`, and `Trust`
- `Temporal Craft` can influence `Presence`, `Memorability`, and `AI Slop Risk`

---

## 6. Card Types and Weighting

All cards share the same visible score vocabulary.

But the weighting changes by:

- content type
- structural archetype
- commercial role

### 6.1 Content-Type Baselines

#### Single image post + caption

Heavier on:

- Signal
- Trust
- Memorability
- Humanity

#### Carousel + caption

Heavier on:

- Memorability
- Trust
- Resonance
- Structure support

#### Reel + caption

Heavier on:

- Presence
- Humanity
- Resonance
- Memorability
- Temporal craft support

### 6.2 Archetype-Specific Bundles

Examples:

#### Reaction reel

Heavier on:

- Presence
- Signal
- Resonance
- Humanity

#### Explainer reel

Heavier on:

- Trust
- Signal
- Memorability
- Presence

#### Cinematic story reel

Heavier on:

- Resonance
- Humanity
- Memorability
- Trust

#### Proof carousel

Heavier on:

- Trust
- Memorability
- Humanity
- Signal

#### Conversion image post

Heavier on:

- Trust
- Signal
- Presence
- AI Slop Risk control

---

## 7. Overall Score Logic

The `overall_score` must not be a naive arithmetic average.

It should be:

- weighted by card type
- adjusted by content type
- penalized by AI slop risk
- optionally gated by hard failures

Example law:

- strong visible scores cannot fully compensate for very high `AI Slop Risk`
- very weak `Trust` or `Humanity` should cap the top-end score for human-first surfaces
- high `Presence` without `Trust` should not create false greatness

This preserves credibility.

---

## 8. Multimodal Audit Implications

The audit engine must support:

- `single image post + caption`
- `multiple images / carousel + caption`
- `reel / short-form video + caption`

### 8.1 Image Posts

The image audit should score:

- screenshot / frame proof quality
- visual authority cues
- visual genericity risk
- caption-image coherence

### 8.2 Carousels

The carousel audit should score:

- slide sequence logic
- frame-to-frame proof movement
- visual narrative progression
- caption interaction

### 8.3 Reels

The reel audit should score:

- script meaning
- key-frame and key-shot quality
- shot transitions
- pacing
- temporal coherence
- caption-to-video alignment

The OmniShotCut note is useful here as a structural reference for:

- shot segmentation
- intra-shot relations
- inter-shot relations
- discontinuity detection

It should inform the future video-structure analysis layer rather than replace CCP-specific evaluation.

---

## 9. Card Design Law

Cards should feel like:

- premium scouting cards
- easy to compare
- easy to screenshot
- easy to share
- slightly entertaining

They should not feel like:

- enterprise dashboard widgets
- tarot cards
- childish game toys

Each card should include:

- large thumbnail image
- overall score
- card type
- six visible scores
- AI slop risk
- one-line verdict
- one-line fix or upgrade direction

---

## 10. Spec Implications

This note implies three supporting specs before or alongside the Audit Intelligence Engine:

1. `FR-ERA3-35A Eval Registry and Scoring Taxonomy`
2. `FR-ERA3-35B Content Benchmark Profiles and Card Weighting Bundles`
3. `FR-ERA3-35C Eval Card System and Shareable Audit Board`

Then:

4. `FR-ERA3-35 Audit Intelligence Engine`

That order is important because:

- the audit engine should consume canonical evals
- benchmark profiles should define weighting logic
- the card system should expose the scores cleanly

The audit engine should not invent its own evaluation language ad hoc.

---

## 11. Final Law

The eval system should optimize for:

- trust
- humanity
- presence
- signal
- resonance
- memorability

because in the AI-saturated market:

- polish is abundant
- expertise imitation is cheap
- meaning is scarce
- trust is scarce
- human signal is scarce

The visible card system should therefore answer:

**does this content create subconscious certainty, not just readable output?**
