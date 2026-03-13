---
name: ccf-trigger-match
description: "Weekly Pipeline — Runs trigger matching + activation event design between Radar and Question"
---

# /ccf-trigger-match {client_name} --week {week_id}

// turbo-all

> **SKILLS_BASE:** `ccf-26/skills/ccf/`
> **SKILLS:**
> - `content/trigger-matching-layer/SKILL.md`
> - `content/activation-event-designer/SKILL.md`
> - `content/provocation-generator/SKILL.md`
> **PHASE:** Weekly (inserted between /ccf-radar and /ccf-question)

**Objective:** Match audience L3 pain to coach trigger architecture, design ESK-targeting activation events, and generate trigger-first provocation questions with LIWC-22 scoring rubric.

> [!IMPORTANT]
> **PIPELINE POSITION:** This command runs AFTER `/ccf-radar` and BEFORE `/ccf-question`. It replaces topic-based question generation with trigger-first activation event design. The output (`provocation_questions.json`) is format-compatible with the existing pipeline — downstream commands (`/ccf-elicit`, `/ccf-theme-discover`) consume it without modification.

---

## 🎯 STEP 0: INITIALIZE TODOS

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify trigger_map + emotional_dna + radar output", status: "pending" },
    { id: "step-2", description: "STEP 2: LOAD SKILL 1 - Read Trigger Matching Layer SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: MATCH - Run 2-axis structural matching (MFT + Temporal)", status: "pending" },
    { id: "step-4", description: "STEP 4: VALIDATE SEEDS - PTG safety gate + MFT coherence check", status: "pending" },
    { id: "step-5", description: "STEP 5: LOAD SKILL 2 - Read Activation Event Designer SKILL.md", status: "pending" },
    { id: "step-6", description: "STEP 6: DESIGN - Construct ESK-targeting activation events", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE EVENTS - ESK score + prediction error check", status: "pending" },
    { id: "step-8", description: "STEP 8: LOAD SKILL 3 - Read Provocation Generator SKILL.md", status: "pending" },
    { id: "step-9", description: "STEP 9: GENERATE - Format Telegram provocations + build LIWC rubric", status: "pending" },
    { id: "step-10", description: "STEP 10: VALIDATE PROVOCATIONS - Word count + tone + no-leading check", status: "pending" },
    { id: "step-11", description: "STEP 11: CHECKPOINT - Final status + delivery summary", status: "pending" }
  ]
});
```

---

## STEP 1: PRE-FLIGHT

Mark step-1 `in_progress`.

| Check | Path | If Missing |
|-------|------|------------|
| 1 | `intelligence_library/trigger_map.json` with ≥ 2 triggers | STOP → Run `/ccf-trigger-extract` first |
| 2 | `intelligence_library/emotional_dna.json` with `extraction_status.confidence` ≥ 0.5 | STOP → Run `/ccf-trigger-extract` first |
| 3 | `intelligence/weekly/{week_id}/intelligence_radar.json` | STOP → Run `/ccf-radar` first |
| 4 | `intelligence/context_premises/` with `trigger_matching_candidates` | WARN → Matching will use radar data only |
| 5 | `intelligence_library/coach_soul.json` with `pipeline_ready: true` | WARN → Proceed with available data |

Mark step-1 `completed`.

---

## STEP 2: LOAD SKILL 1 — Trigger Matching Layer

Mark step-2 `in_progress`.

Read FULL: `ccf-26/skills/ccf/content/trigger-matching-layer/SKILL.md`

**Internalize:**
- Clark & Brennan Common Ground Theory (3 levels)
- 2-axis matching: Moral Foundation + Temporal Position
- Seed construction format
- PTG gate and MFT coherence constraints

Mark step-2 `completed`.

---

## STEP 3: MATCH — Structural Congruence

Mark step-3 `in_progress`.

Execute Trigger Matching Layer protocol:
1. Extract audience structural data (L3 only)
2. Axis 1: Moral Foundation matching (exact = 1.0, secondary = 0.6, adjacent = 0.3)
3. Axis 2: Temporal Position matching (audience inside + coach completed = valid)
4. Construct seeds for all valid 2-axis matches
5. Bind intelligence fuel from radar output
6. Rank by composite score

**Output:** In-memory seed array (not yet written to file)

Mark step-3 `completed`.

---

## STEP 4: VALIDATE SEEDS

Mark step-4 `in_progress`.

| Check | Gate | If Fail |
|-------|------|---------|
| PTG Safety | No `raw_unresolved` triggers in seeds | Remove violating seeds |
| MFT Coherence | Every seed has matching moral foundation | Remove incoherent seeds |
| Minimum Viable | ≥ 2 valid seeds | WARN — limited activation possible |
| Evidence | Every seed has audience + coach provenance | Remove unattributed seeds |

**WRITE:** `intelligence/weekly/{week_id}/trigger_matched_seeds.json`

Mark step-4 `completed`.

---

## STEP 5: LOAD SKILL 2 — Activation Event Designer

Mark step-5 `in_progress`.

Read FULL: `ccf-26/skills/ccf/content/activation-event-designer/SKILL.md`

**Internalize:**
- Tulving ESK targeting, Conway AKB hierarchy
- Nader reconsolidation prediction error requirement
- DARN-CAT 7-dimension taxonomy
- OARS session architecture
- Cooperrider Appreciative Inquiry retrieval direction
- Kahan IPC bypass mechanism

Mark step-5 `completed`.

---

## STEP 6: DESIGN — Activation Events

Mark step-6 `in_progress`.

Select top 5-7 seeds and for each:
1. Phase 1: Mechanism Extraction (mechanism, not topic)
2. Phase 2: Sensory Anchoring (ESK-level specificity)
3. Phase 3: DARN-CAT Dimension Selection (2-3 dimensions per event)
4. Phase 4: Event Construction (Context + Retrieval Key + Safety Signal)

**Output:** In-memory activation event array

Mark step-6 `completed`.

---

## STEP 7: VALIDATE EVENTS

Mark step-7 `in_progress`.

| Check | Threshold | If Fail |
|-------|-----------|---------|
| ESK Targeting Score | ≥ 6/10 per event | Redesign with more sensory anchors |
| Prediction Error Score | ≥ 5/10 per event | Add more specificity to mechanism |
| Mechanism Not Topic | Pass/fail per event | Refine until mechanism-level |
| Retrieval Direction | Peak-first per event | Reframe toward peak |

**WRITE:** `intelligence/weekly/{week_id}/activation_events.json`

Mark step-7 `completed`.

---

## STEP 8: LOAD SKILL 3 — Provocation Generator

Mark step-8 `in_progress`.

Read FULL: `ccf-26/skills/ccf/content/provocation-generator/SKILL.md`

**Internalize:**
- LIWC-22 7-marker authenticity scoring rubric
- Telegram formatting constraints (≤ 80 words)
- Conversational tone, no-leading, front-loaded specificity
- Hatfield Emotional Contagion validity

Mark step-8 `completed`.

---

## STEP 9: GENERATE — Provocations + LIWC Rubric

Mark step-9 `in_progress`.

For each activation event:
1. Format as Telegram message (Context + Question + Safety Bridge)
2. Tag with question archetype (reality_check / sacred_rage / hidden_insight / paradigm_shift)
3. Verify ≤ 80 words
4. Sequence for delivery

Build LIWC-22 scoring rubric (7 markers with weights and thresholds).

**WRITE:** `intelligence/weekly/{week_id}/provocation_questions.json`
**WRITE:** `intelligence/weekly/{week_id}/liwc_scoring_rubric.json`

Mark step-9 `completed`.

---

## STEP 10: VALIDATE PROVOCATIONS

Mark step-10 `in_progress`.

| Check | Requirement | If Fail |
|-------|------------|---------|
| Word count | Every provocation ≤ 80 words | Trim — never add |
| Tone | Conversational, not academic | Rewrite in coach register |
| No leading | No expected answers in prompt | Remove directing language |
| Front-loading | Specific detail in first sentence | Restructure |
| ESK preserved | Activation event integrity maintained | Redesign if key diluted |
| Format compatibility | Output format matches existing `provocation_questions.json` schema | Adjust structure |

Mark step-10 `completed`.

---

## STEP 11: CHECKPOINT

Mark step-11 `in_progress`.

Update `config.yaml`:
```yaml
sessions:
  weekly:
    "{week_id}":
      trigger_match:
        status: "complete"
        timestamp: "{ISO date}"
        seeds_matched: {N}
        activation_events: {N}
        provocations_generated: {N}
        avg_esk_score: {N}
        liwc_rubric: "generated"
```

**FINAL OUTPUT:**
```
✅ TRIGGER-FIRST MATCHING COMPLETE (Week {week_id})

🌉 Structural Matching:
- Seeds matched: {N}
- Axis 1 (MFT) matches: {N}
- Axis 2 (Temporal) validated: {N}
- Intelligence fuel bindings: {N}

🔥 Activation Events:
- Events designed: {N}
- Avg ESK targeting: {N}/10
- Avg prediction error: {N}/10
- DARN-CAT dimensions used: {list}

📡 Provocations:
- Questions formatted: {N}
- Avg word count: {N}
- Archetype distribution: {breakdown}
- LIWC rubric: ✅ Generated (gate threshold: 0.6)

📋 Ready for coach delivery (Telegram)

💡 NEXT: Deliver questions to coach → Wait for voice notes → /ccf-elicit {client_name}
```

Mark step-11 `completed`.

---

## 🔗 NEXT: Deliver questions → `/ccf-elicit {client_name} --week {week_id}`
