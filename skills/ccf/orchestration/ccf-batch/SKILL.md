---
name: "Batch Orchestrator"
description: "Two-phase weekly cycle: Phase A extracts authenticated material via Trigger-First Engine, Phase B generates 12 blueprints from that material."
session_id: ccf-batch
phase: orchestration
ccp_layer: Orchestration (L5)
pi_extensions: [TeamOrchestrator, ReceiptChainGuard]
inputs:
  - config.yaml
  - intelligence_library/trigger_map.json (if exists — cold-start fallback if absent)
  - intelligence_library/emotional_dna.json
  - intelligence_library/coach_soul.json
outputs:
  - All Phase A extraction artifacts
  - All Phase B production artifacts for all 12 blueprints
  - batch_report.json
depends_on: [trigger-matching-layer]
---

# ccf-batch — Two-Phase Trigger-First Batch Orchestrator

> **Version:** CCP v3.1 — Trigger-First Engine Integration
> **Architecture:** Two-phase weekly cycle (Extraction → Production)
> **Causal Direction:** Emotional DNA → Trigger → Intelligence Fuel → Activation → Authentication → Archetype → Generation

## Purpose
Orchestrate the full CCF weekly pipeline as a two-phase cycle. **Phase A (Extraction Cycle)** activates the coach's trigger architecture and captures authenticated material. **Phase B (Production Cycle)** generates 12 content pieces from that authenticated material. The pipeline is trigger-first: the coach's permanent emotional fires determine WHAT is created; intelligence and format are secondary.

## Usage
```
ccf-batch --project <path>
```

## Pre-Flight Check

```
1. Read config.yaml
2. Check for trigger_map.json in intelligence_library/
3. IF trigger_map.json EXISTS AND contains >= 3 verified triggers:
   → Set pipeline_mode = "TRIGGER_FIRST"
   → Log: "🔥 Trigger-First mode — {n} verified triggers loaded"
4. ELSE:
   → Set pipeline_mode = "TOPIC_FIRST_FALLBACK"
   → Log: "⚠️ Cold-start fallback — insufficient verified triggers. Running topic-first."
   → Skip Phase A Steps 1-3. Jump to legacy intelligence-radar → topic elicitation flow.
5. Check for resume points (partially completed batches)
```

---

## Phase A: Extraction Cycle (Trigger-First)

*This phase runs ONCE per week. It produces the authenticated material that Phase B consumes. The coach interacts via Telegram between Steps 4 and 5.*

### Step A1: Trigger Matching
```
1. Call: trigger-matching-layer --week {week_id}
2. Inputs: emotional_dna.json + trigger_map.json + audience Context Premise (L3 segments)
3. Outputs: activation_seeds.json (4-axis matched seeds ranked by composite score)
4. Gate: At least 2 seeds with all 4 axes >= 0.3 threshold
5. Log: "Seeds produced: {n}, 4-axis matches: {m}"
```

### Step A2: Intelligence Radar (Fuel Mode)
```
1. Call: intelligence-radar --week {week_id} --mode trigger_fuel
2. Inputs: activation_seeds.json + trigger_map.json
3. Behavior: Scores friction points by trigger_activation_score (PRIMARY key)
   - Only friction points with trigger_activation_score >= 5.0 pass
   - Cultural relevance and temporal velocity are SECONDARY tiebreakers
4. Outputs: intelligence_radar.json (fuel-scored, with trigger_matched_moral_foundation tags)
5. Log: "Friction points scanned: {n}, trigger-matched: {m}, discarded: {d}"
```

### Step A3: Activation Event Design
```
1. Call: activation-event-designer --week {week_id}
2. Inputs: activation_seeds.json + intelligence_radar.json (fuel-scored)
3. Behavior: Binds intelligence fuel to seeds → designs sensory-specific activation events
   - Each event contains temporal sharpening data from radar friction points
   - DARN-CAT dimension selection per seed characteristics
4. Outputs: activation_events.json (5-7 events with ESK targeting scores)
5. Log: "Events designed: {n}, avg prediction_error_score: {avg}"
```

### Step A4: Provocation Generation
```
1. Call: provocation-generator --week {week_id}
2. Inputs: activation_events.json + emotional_dna.json + coach_soul.json
3. Behavior: Converts activation events into Telegram-ready voice note prompts
   - Each prompt ≤ 80 words, specific detail front-loaded
   - LIWC-22 scoring rubric generated alongside
4. Outputs: provocation_questions.json + liwc_scoring_rubric.json
5. Log: "Provocations generated: {n}, delivery sequence set"
6. ⏸️ PAUSE — Deliver provocations to coach via Telegram. Await voice note responses.
```

### Step A5: Coach Elicitation (LIWC Authentication Gate)
```
1. Call: coach-elicitation --week {week_id}
2. Inputs: raw/voice_notes/{week_id}/ + provocation_questions.json + liwc_scoring_rubric.json
3. Behavior:
   - Transcribe voice notes (Whisper)
   - Run LIWC-22 Turn-Level Scoring per response
   - Score < 0.4 → HALT (flag as "Semantic Performance", do not pass downstream)
   - Score >= 0.4 → Pass with authentication_certificate attached
   - Score >= 0.6 → PROMOTE trigger in trigger_map.json (verification)
4. Outputs: coach_soc_batch.md (authenticated transcriptions with certificates)
5. Gate: At least 5 authenticated segments (LIWC >= 0.4)
6. Log: "Transcriptions: {n}, authenticated: {m}, rejected: {r}, avg LIWC: {avg}"
```

### Step A6: Emotional State → Archetype Mapping
```
1. For each authenticated segment in coach_soc_batch.md:
   a. Read authentication_certificate → LIWC profile shape
   b. Read trigger_map.json → moral foundation activated
   c. Read transcript → TTT band
   d. Classify dominant emotional state
   e. Map to archetype family via emotional-state-to-archetype table
   f. TTT compatibility filter: can this coach occupy this archetype's temperature?
2. Outputs: emotional_state_archetype_map.json
3. Log: "Segments mapped: {n}, archetype families: {unique_families}"
```

### Step A7: Blueprint Distillation (Trigger-Sourced)
```
1. Call: blueprint-distiller --week {week_id} --mode trigger_first
2. Inputs: emotional_state_archetype_map.json + activation_seeds.json + coach_soc_batch.md
3. Behavior: Produces 12 blueprints where:
   - Each blueprint specifies: activation_seed_id, authenticated_voice_note_id,
     emotional_state_classification, archetype_match, trigger_mechanism_specification,
     audience_l3_congruence_point
   - content_idea replaced by trigger_expression_angle
4. Outputs: content_blueprints.json (trigger-sourced, 12 blueprints)
5. Log: "Blueprints: 12, trigger-sourced: {n}, fallback-sourced: {12-n}"
```

### Step A8: Research Distillation (Trigger Ammunition)
```
1. Call: research-distiller --week {week_id} --mode trigger_ammunition
2. Inputs: content_blueprints.json + trigger_mechanism_specification per blueprint
3. Behavior: DEEP/FRESH research scored by mechanism_sharpening_score (PRIMARY)
   - "Does this evidence sharpen the specific mechanism that fired the coach's trigger?"
   - NOT "Is this relevant to the topic?"
4. Outputs: research_briefs.json (per-blueprint, mechanism-scored)
5. Log: "Briefs: 12, avg mechanism_sharpening_score: {avg}"
```

**Phase A Complete.** All downstream production receives trigger-sourced, LIWC-authenticated material.

---

## Phase B: Production Cycle (Per-Blueprint)

*Unchanged in structure. Each blueprint runs through the generation pipeline. But inputs are now grounded in authenticated material from Phase A.*

### Step B1: Sequential Blueprint Execution
```
For blueprint in content_blueprints.json[0..11]:

  1. Log: "Blueprint {i+1}/12: {blueprint.trigger_expression_angle}"
  2. Call: ccf-produce --blueprint {blueprint.id}
     - soc-generator receives authenticated ESK material (not topic premise)
     - mirror-session operates on trigger-sourced archetype (not topic-selected)
     - script-generator receives full provenance chain
  3. Wait for completion
  4. Capture result:
     - AUTHORIZED → increment authorized_count
     - REJECTED (remediated, then passed) → increment remediated_count
     - ESCALATED (Phoenix Loop exhausted) → increment escalated_count
  5. Checkpoint batch progress
  6. Log: "Blueprint {i+1}/12: {result} ({duration})"

  IMPORTANT: Do NOT parallelize blueprint execution.
  Mirror Session (Stage 2) requires isolated reasoning per archetype.
```

### Step B2: Generate Batch Report
```json
{
  "batch_id": "...",
  "project": "Coach Adele / W07",
  "pipeline_mode": "TRIGGER_FIRST",
  "timestamp_start": "...",
  "timestamp_end": "...",
  "phase_a_metrics": {
    "seeds_produced": 8,
    "four_axis_matches": 6,
    "friction_points_scanned": 42,
    "trigger_matched_friction_points": 18,
    "activation_events_designed": 7,
    "voice_notes_received": 7,
    "liwc_authenticated": 6,
    "liwc_rejected": 1,
    "avg_liwc_score": 0.72
  },
  "phase_b_metrics": {
    "total": 12,
    "authorized": 10,
    "remediated": 1,
    "escalated": 1,
    "trigger_activation_coverage": 0.83,
    "avg_authenticity_parity_score": 0.88
  },
  "per_blueprint": [
    {
      "blueprint_id": "...",
      "trigger_expression_angle": "...",
      "source": "trigger_first | fallback_topic",
      "activation_seed_id": "seed_003",
      "liwc_score": 0.74,
      "archetype_match": "...",
      "result": "AUTHORIZED",
      "validation_scores": {},
      "authenticity_parity_delta": 0.08,
      "token_usage": {},
      "duration_s": 480,
      "distribution_outputs": []
    }
  ],
  "totals": {
    "total_duration_s": 5760,
    "total_tokens_in": 1800000,
    "total_tokens_out": 300000,
    "estimated_cost_usd": 25.40
  }
}
```

### Step B3: Finalize
```
1. Save batch_report.json to project root
2. Update config.yaml: sessions.orchestration.batch.status = "complete"
3. Print summary to console
4. Log trigger_activation_coverage to experience pool for MATRL trending
```

---

## Parallelism Strategy

**Phase A runs STRICTLY sequentially.** Each step's output is a causal prerequisite for the next. Trigger matching must complete before intelligence scanning. Intelligence must complete before activation design. Activation events must be delivered and responded to before elicitation.

**Phase B: Do NOT parallelize blueprint execution.** Mirror Session requires isolated reasoning per archetype.

**The only parallelism allowed is within blueprint distribution** (tweets + visuals can run in parallel since they read from the same script but produce independent outputs).

---

## Error Handling
- If Phase A produces fewer than 5 authenticated segments, warn and attempt to fill remaining blueprints with topic-first fallback material
- If a blueprint fails at any stage, the Phoenix Loop handles remediation
- If Phoenix Loop exhausts all 3 modes, the blueprint is marked ESCALATED
- ESCALATED blueprints do NOT block remaining blueprints
- All errors are logged in batch_report.json for human review

---

## I-R-E-V-C Session Protocol

### INGEST
- Load config.yaml, trigger_map.json, emotional_dna.json, coach_soul.json
- Check for resume point
- Determine pipeline_mode (TRIGGER_FIRST or TOPIC_FIRST_FALLBACK)

### REASON
- Phase A: Execute extraction cycle (Steps A1-A8) — produces authenticated blueprints
- Phase B: For each blueprint (sequential): call ccf-produce
- Track results: AUTHORIZED / REMEDIATED / ESCALATED

### EMIT
- batch_report.json with Phase A metrics + Phase B per-blueprint results
- All production artifacts for all 12 blueprints
- Updated trigger_map.json (promotions from LIWC verification)

### VALIDATE
- All Phase A gates passed (seeds >= 2, authenticated segments >= 5)
- All 12 blueprints processed (none skipped unless ESCALATED)
- batch_report.json is complete
- trigger_activation_coverage >= 0.50 (cold-start) or >= 0.80 (steady-state)
- Token usage and cost are calculated

### CHECKPOINT
- Update config.yaml with batch completion status
- Log: pipeline_mode, trigger_activation_coverage, avg_liwc_score
