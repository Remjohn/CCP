---
name: ccf-batch
description: Batch orchestration — run the 4-stage production pipeline across all blueprints
---

# /ccf-batch {client_name}

// turbo-all

> **Objective:** Orchestrate the full CCF production pipeline across all 12 blueprints in `content_blueprints.json`. Runs Stages 1-4 sequentially per blueprint: SoC → Adapt → Wisdom → Generate → Analyze → Validate.

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify all pre-production outputs", status: "pending" },
    { id: "step-2", description: "STEP 2: LOAD BLUEPRINTS - Parse content_blueprints.json", status: "pending" },
    { id: "step-3", description: "STEP 3: EXECUTE PIPELINE - Run 4-stage pipeline per blueprint", status: "pending" },
    { id: "step-4", description: "STEP 4: REPORT - Emit batch summary", status: "pending" },
    { id: "step-5", description: "STEP 5: CHECKPOINT - Update config.yaml", status: "pending" }
  ]
});
```

**DO NOT PROCEED until you have called `write_todos` above.**

---

## 📋 Step Execution Protocol (MANDATORY)

> [!CAUTION]
> **You MUST call `write_todos` at EVERY step transition.**

**For EACH step:** START → `in_progress` → Execute → Verify → `completed`

---

## STEP 1: PRE-FLIGHT

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify all pre-production outputs", status: "in_progress" },
    { id: "step-2", description: "STEP 2: LOAD BLUEPRINTS - Parse content_blueprints.json", status: "pending" },
    { id: "step-3", description: "STEP 3: EXECUTE PIPELINE - Run 4-stage pipeline per blueprint", status: "pending" },
    { id: "step-4", description: "STEP 4: REPORT - Emit batch summary", status: "pending" },
    { id: "step-5", description: "STEP 5: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

| Check | Path | If Missing |
|-------|------|------------|
| 1 | `output/batches/batch_001/blueprints/content_blueprints.json` | STOP → Run `/ccf-blueprint` |
| 2 | `intelligence/soul/soul_values.json` | STOP → Run `/ccf-soul-extract` |
| 3 | `intelligence/tribe/tribe_profile.json` | STOP → Run `/ccf-tribe-extract` |
| 4 | `research/vibe_comments/vibe_comments_processed.json` | STOP → Run `/ccf-vibe-comments` |
| 5 | `research/fresh/` (12 briefs) | STOP → Run `/ccf-research-fresh` |
| 6 | `research/deep/` (12 briefs) | STOP → Run `/ccf-research-deep` |

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify all pre-production outputs", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD BLUEPRINTS - Parse content_blueprints.json", status: "pending" },
    { id: "step-3", description: "STEP 3: EXECUTE PIPELINE - Run 4-stage pipeline per blueprint", status: "pending" },
    { id: "step-4", description: "STEP 4: REPORT - Emit batch summary", status: "pending" },
    { id: "step-5", description: "STEP 5: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 2: LOAD BLUEPRINTS

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify all pre-production outputs", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD BLUEPRINTS - Parse content_blueprints.json", status: "in_progress" },
    { id: "step-3", description: "STEP 3: EXECUTE PIPELINE - Run 4-stage pipeline per blueprint", status: "pending" },
    { id: "step-4", description: "STEP 4: REPORT - Emit batch summary", status: "pending" },
    { id: "step-5", description: "STEP 5: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

1. Parse `content_blueprints.json` — extract all 12 blueprint IDs
2. Check for any already-completed blueprints (resume support)
3. Build execution queue: skip completed, queue remaining

Report: "Batch queue: {N} blueprints to process ({M} already complete)"

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify all pre-production outputs", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD BLUEPRINTS - Parse content_blueprints.json", status: "completed" },
    { id: "step-3", description: "STEP 3: EXECUTE PIPELINE - Run 4-stage pipeline per blueprint", status: "pending" },
    { id: "step-4", description: "STEP 4: REPORT - Emit batch summary", status: "pending" },
    { id: "step-5", description: "STEP 5: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 3: EXECUTE PIPELINE

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify all pre-production outputs", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD BLUEPRINTS - Parse content_blueprints.json", status: "completed" },
    { id: "step-3", description: "STEP 3: EXECUTE PIPELINE - Run 4-stage pipeline per blueprint", status: "in_progress" },
    { id: "step-4", description: "STEP 4: REPORT - Emit batch summary", status: "pending" },
    { id: "step-5", description: "STEP 5: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

**FOR EACH BLUEPRINT in execution queue, run the 4-stage pipeline:**

| Stage | Command | What It Does |
|-------|---------|-------------|
| 1 | `/ccf-soc` | Stream of Consciousness generation |
| 2 | `/ccf-adapt` | Mirror Session (14 questions) |
| 2.5 | `/ccf-wisdom` | Wisdom Forge (4 briefs) |
| 3 | `/ccf-generate` | Script generation |
| 3.5 | `/ccf-analyze` | 7-dimension analysis |
| 4 | `/ccf-validate` | Triple validation + Alchemy Gate |

> [!IMPORTANT]
> **Sequential execution REQUIRED.** Each blueprint must complete all 4 stages before moving to the next. This prevents context contamination between blueprints.

> [!CAUTION]
> **Context Window Management:** After every 3 blueprints, emit a progress checkpoint. If approaching context limits, STOP and report progress — the batch can be resumed.

**Progress tracking per blueprint:**
```
Blueprint {N}/12: {blueprint_id}
  Stage 1 (SoC): ✅ | Stage 2 (Adapt): ✅ | Stage 2.5 (Wisdom): ✅
  Stage 3 (Generate): ✅ | Stage 3.5 (Analyze): ✅ | Stage 4 (Validate): ✅
  Result: PASS ✅
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify all pre-production outputs", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD BLUEPRINTS - Parse content_blueprints.json", status: "completed" },
    { id: "step-3", description: "STEP 3: EXECUTE PIPELINE - Run 4-stage pipeline per blueprint", status: "completed" },
    { id: "step-4", description: "STEP 4: REPORT - Emit batch summary", status: "pending" },
    { id: "step-5", description: "STEP 5: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 4: REPORT

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify all pre-production outputs", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD BLUEPRINTS - Parse content_blueprints.json", status: "completed" },
    { id: "step-3", description: "STEP 3: EXECUTE PIPELINE - Run 4-stage pipeline per blueprint", status: "completed" },
    { id: "step-4", description: "STEP 4: REPORT - Emit batch summary", status: "in_progress" },
    { id: "step-5", description: "STEP 5: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

**CREATE FILE:** `output/batches/batch_001/batch_summary.json`

Schema: `total_blueprints`, `completed`, `passed`, `review`, `failed`, `phoenix_loops`, `average_composite_score`, per-blueprint status array.

**OUTPUT:**
```
✅ BATCH COMPLETE ({client_name})
- Blueprints: {N}/12 processed
- Passed: {N} | Review: {N} | Failed: {N}
- Average Composite: {N}/10
- Phoenix Loops: {N}
- Scripts in: output/batches/batch_001/scripts/
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify all pre-production outputs", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD BLUEPRINTS - Parse content_blueprints.json", status: "completed" },
    { id: "step-3", description: "STEP 3: EXECUTE PIPELINE - Run 4-stage pipeline per blueprint", status: "completed" },
    { id: "step-4", description: "STEP 4: REPORT - Emit batch summary", status: "completed" },
    { id: "step-5", description: "STEP 5: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 5: CHECKPOINT

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify all pre-production outputs", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD BLUEPRINTS - Parse content_blueprints.json", status: "completed" },
    { id: "step-3", description: "STEP 3: EXECUTE PIPELINE - Run 4-stage pipeline per blueprint", status: "completed" },
    { id: "step-4", description: "STEP 4: REPORT - Emit batch summary", status: "completed" },
    { id: "step-5", description: "STEP 5: CHECKPOINT - Update config.yaml", status: "in_progress" }
] });
```

Update `config.yaml`:
- `sessions.batch.batch_001.status = "complete"`
- `sessions.batch.batch_001.scripts_produced = {N}`
- `sessions.batch.batch_001.pass_rate = "{N}%"`

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify all pre-production outputs", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD BLUEPRINTS - Parse content_blueprints.json", status: "completed" },
    { id: "step-3", description: "STEP 3: EXECUTE PIPELINE - Run 4-stage pipeline per blueprint", status: "completed" },
    { id: "step-4", description: "STEP 4: REPORT - Emit batch summary", status: "completed" },
    { id: "step-5", description: "STEP 5: CHECKPOINT - Update config.yaml", status: "completed" }
] });
```

---

## 🔗 DONE — All scripts in `output/batches/batch_001/scripts/`
