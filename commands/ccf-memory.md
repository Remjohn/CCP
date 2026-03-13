---
name: ccf-memory
description: "Coach Voice Memory — Agentic Learning System that integrates Trigger Mapping feedback and Voice DNA evolution."
---

# /ccf-memory {mode} {client_name}

// turbo-all

> **SKILLS_BASE:** `ccf-26/skills/ccf/`
> **SKILL:** `content/memory-engine/SKILL.md`
> **TEMPLATE:** `ccf-26/templates/coach_memory_template.json`

**Modes:**
- `update` — Post-elicitation learning incorporating LIWC-22 Trigger Feedback
- `feedback` — Log post-publication content performance
- `report` — Output Voice DNA and Trigger Evolution metrics

---

## 🎯 STEP 0: INITIALIZE HARNESS

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "PRE-FLIGHT: Validate inputs and determine execution path", status: "pending" },
    { id: "step-2", description: "LOAD MEMORY: Load base memory files and Trigger/LIWC matrices", status: "pending" },
    { id: "step-3", description: "EXECUTE MODE: Run Agentic processes (Chain-of-Draft updates/feedback loops)", status: "pending" },
    { id: "step-4", description: "SAVE & CHECKPOINT: Export memory, update trigger_map flags, checkpoint systems", status: "pending" }
  ]
});
```

---

## STEP 1: PRE-FLIGHT (Validation Constraints)

Mark step-1 `in_progress`.

**Determine mode from parameters:**

| Mode | Required Input | If Missing |
|------|---------------|------------|
| `update` | `coach_soc_batch.md` for current week | STOP → Run `/ccf-elicit` first |
| `feedback` | At least 1 published week in `performance_log` | WARN → First week, nothing to review yet |
| `report` | `coach_memory.json` exists | STOP → Run `update` first |

Mark step-1 `completed`.

---

## STEP 2: LOAD MEMORY (Harness Initialization)

Mark step-2 `in_progress`.

1. **IF** `intelligence/memory/coach_memory.json` exists → Load it
   **ELSE** → Copy template → Save as `intelligence/memory/coach_memory.json`
2. Load: `intelligence_library/trigger_map.json` (if exists)
3. Load: `intelligence/weekly/{week_id}/liwc_scoring_rubric.json` (if exists)
4. Load: `logs/ccf_experience_pool.json` (MATRL Experience Pool)

Mark step-2 `completed`.

---

## STEP 3: EXECUTE MODE

Mark step-3 `in_progress`.

### If mode = `update`:
**Agentic Processing (Chain-of-Draft Enforcement):**
1. Spawn `Memory_Extraction_Agent`. Provide top 3 historical memory updates from MATRL pool.
2. The agent MUST extract updates in strict 5-word logic bullets before expanding metadata:
   - Voice DNA (phrases, tics, stories)
   - Session Intelligence (archetype resonance)
3. **Trigger Architecture Feedback Loop (Item 13):**
   IF `trigger_map.json` AND `liwc_scoring_rubric.json` exist:
   - For each response in `coach_soc_batch.md`:
     1. Retrieve matching `trigger_id` using metadata.
     2. Score raw transcript against LIWC-22 rubric markers → Compute composite Authenticity (0.0-1.0).
     3. Append score and timestamp to `trigger_map.triggers[trigger_id].activation_history[]`.
     4. Update `staleness_tracking.last_activation_date`.
     5. **Degradation Check:** IF 3 consecutive scores < 0.5 on same trigger → Flag trigger as "degrading" (requires re-verification).
     6. **Dormancy Check:** IF trigger has 0 activations in >8 weeks → Flag as "dormant".

### If mode = `feedback`:
**Turn-Level Performance Scoring:**
1. Present most recent week's published themes.
2. Collect empirical performance data (engagement, velocity, audience feedback).
3. If output failed, explicitly evaluate component steps using **Difference Rewards** simulation to identify the failing sub-agent (e.g., Theme Generator vs Script Artisan).
4. Update `performance_log` and `performance_log.patterns`.
5. Post failing records to MATRL False Negatives library to guide future context injection.

### If mode = `report`:
1. Generate formatted Voice Memory & Trigger Diagnostic Report.
2. Include: Degrading/Dormant Trigger status, LIWC-22 average scores, signature phrase changes, story bank inventory.

Mark step-3 `completed`.

---

## STEP 4: SAVE & CHECKPOINT

Mark step-4 `in_progress`.

- **WRITE:** `intelligence/memory/coach_memory.json`
- **WRITE:** `intelligence_library/trigger_map.json` (Apply activation histories and flag updates)
- **WRITE:** `logs/ccf_experience_pool.json` (Add new MATRL entries)

```
✅ MEMORY ENGINE {MODE} COMPLETE (Week {week_id})

UPDATE mode:
- Extracted bullet concepts: {N}
- Trigger activations tracked: {N}
- Triggers flagged (degrading/dormant): {N}

FEEDBACK mode:
- Performance records logged: {N}
- Difference Rewards computed: {yes/no}

REPORT mode:
- Report generated: intelligence/memory/voice_memory_report.md
```

Mark step-4 `completed`.

---

## 🔗 USAGE

```bash
# After elicitation (auto-called by /ccf-weekly):
/ccf-memory update {client_name}

# After content is published (manual):
/ccf-memory feedback {client_name}

# Anytime — see how much we've learned:
/ccf-memory report {client_name}
```
