# Dynamic Prosody Score Architecture
**Date:** 2026-05-01  
**Status:** Technical Architecture  
**Context:** Segment-level voice rendering, context adaptation, premium note generation

## 1. Core Thesis

Each audio note should be compiled like a score, not rendered like a preset.

That means every output needs:
- a base voice identity
- a context interpretation
- a segment plan
- target primitive values over time

## 2. Scoring Levels

### 2.1 Macro level
Whole-note intent:
- orient
- relieve
- validate
- invite
- redirect
- celebrate

### 2.2 Meso level
Thought-unit segmentation:
- usually every 2-5 seconds
- based on clause and rhetorical boundary, not fixed clock slices

### 2.3 Micro level
Word and phrase emphasis:
- key landings
- breaths
- tiny pauses
- targeted stress

## 3. Score Inputs

The score compiler should ingest:
- Voice DNA Core
- Voice Style State
- Voice Growth Delta
- message role
- audience state
- emotional target
- transcript structure
- sonic context

## 4. Target Formula

The conceptual formula is:

`render_state(t) = core + style + growth + context + segment_delta(t) + microvariation(t)`

Where:
- `core` preserves identity
- `style` reflects present mode
- `growth` introduces developmental refinement
- `context` adapts to task
- `segment_delta(t)` changes with the note
- `microvariation(t)` keeps the output alive without randomness

## 5. Why Segment Scoring Matters

Without segment scoring:
- notes feel flat
- emotion becomes generic
- every sentence sounds equally weighted
- the system becomes predictable

With segment scoring:
- tension can rise and release
- pauses can breathe intentionally
- intimacy can shift naturally
- the note feels directed

## 6. Output Structure

The compiler should emit a render packet per segment:
- text span
- emotional job
- family-level primitive targets
- emphasis words
- breath markers
- pause markers
- cadence intent

## 7. Final Principle

Premium voice notes are not a single mood.
They are a **controlled movement across time**.
