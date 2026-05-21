# Voice Primitive Taxonomy v1
**Date:** 2026-05-01  
**Status:** Technical Taxonomy  
**Context:** Internal voice control basis, prosody modeling, combinatorial variation

## 1. Core Thesis

We do not need 108 public sliders.
We likely do need a rich internal basis.

The correct design is:
- a structured primitive taxonomy
- grouped into families
- capable of combinatorial variation
- translatable into render-time targets

## 2. Primitive Families

### 2.1 Temporal Primitives
- base speaking rate
- local acceleration
- local deceleration
- clause compression
- clause stretch
- beat spacing

### 2.2 Pause Primitives
- pause density
- pause length
- pause placement confidence
- reflective pause hold
- tension pause
- relief pause

### 2.3 Breath Primitives
- breath audibility
- breath softness
- breath frequency
- recovery breath
- intimate breath presence
- energized breath push

### 2.4 Pitch / Contour Primitives
- pitch center
- pitch spread
- upward lift
- downward landing
- contour stability
- contour volatility

### 2.5 Resonance / Timbre Primitives
- brightness
- darkness
- warmth
- dryness
- edge
- softness

### 2.6 Articulation Primitives
- articulation sharpness
- consonant punch
- vowel openness
- phrase clipping
- phrase smoothing
- lexical precision

### 2.7 Emphasis Primitives
- emphasis density
- emphasis strength
- emphasis contrast
- keyword landing
- delayed emphasis
- repeated emphasis

### 2.8 Intimacy / Contact Primitives
- audience-of-one closeness
- public broadcast distance
- invitational directness
- commanding directness
- confessional openness
- observational remove

### 2.9 Tension / Release Primitives
- tension entry
- pressure hold
- controlled fracture
- easing slope
- relief landing
- recovery softness

### 2.10 Narrative / Broadcast Primitives
- hook intensity
- middle stability
- turn point clarity
- final cadence
- memory-peak charge
- call-to-action authority

## 3. Why Families Matter

Families prevent chaos.

Instead of 108 disconnected controls, we get:
- understandable organization
- family-level defaults
- combinatorial flexibility
- easier future evaluation

## 4. Combinatorial Variation

The goal is not raw quantity.
The goal is **structured variation**.

If each family contains multiple controlled states, combinations can generate thousands of expressive profiles without becoming random.

## 5. Operational Rule

A runtime score should rarely manipulate all primitives independently.
Instead, it should:
- set family-level intentions
- refine only the most relevant subprimitives
- preserve coherence with Voice DNA Core

## 6. Final Principle

The taxonomy should be rich enough to support premium expression, but organized enough that evaluation and learning remain tractable.
