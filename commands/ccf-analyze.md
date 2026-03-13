---
name: ccf-analyze
description: Script analysis — multi-dimensional quality scoring
---

# /ccf-analyze {client_name} --blueprint {blueprint_id}

// turbo-all

> **SKILLS_BASE:** `ccf-26/skills/ccf/`
> **SKILL:** `validation/script-analyst/SKILL.md`
> **MODEL:** Use validation model (gemini-2.5-flash)
> **TEMPERATURE:** 0.1

**Objective:** Analyze the generated script across 7 CCF scoring dimensions, producing an `analysis_report.json`.

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify generated script exists", status: "pending" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Analyst SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: INGEST - Load script + soul + vibe_comments", status: "pending" },
    { id: "step-4", description: "STEP 4: ANALYZE - Score across 7 dimensions", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write analysis_report.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - All dimensions present + scored", status: "pending" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "pending" }
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
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify generated script exists", status: "in_progress" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Analyst SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: INGEST - Load script + soul + vibe_comments", status: "pending" },
    { id: "step-4", description: "STEP 4: ANALYZE - Score across 7 dimensions", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write analysis_report.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - All dimensions present + scored", status: "pending" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

| Check | Path | If Missing |
|-------|------|------------|
| 1 | `output/batches/batch_001/scripts/{blueprint_id}_generated_script.md` | STOP → Run `/ccf-generate` |
| 2 | `output/batches/batch_001/scripts/{blueprint_id}_reasoning_log.json` | WARN → Proceed without |
| 3 | `intelligence/soul/soul_values.json` | STOP |
| 4 | `research/vibe_comments/vibe_comments_processed.json` | STOP |

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify generated script exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Analyst SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: INGEST - Load script + soul + vibe_comments", status: "pending" },
    { id: "step-4", description: "STEP 4: ANALYZE - Score across 7 dimensions", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write analysis_report.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - All dimensions present + scored", status: "pending" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 2: LOAD SKILL

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify generated script exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Analyst SKILL.md", status: "in_progress" },
    { id: "step-3", description: "STEP 3: INGEST - Load script + soul + vibe_comments", status: "pending" },
    { id: "step-4", description: "STEP 4: ANALYZE - Score across 7 dimensions", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write analysis_report.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - All dimensions present + scored", status: "pending" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

1. Read: `ccf-26/skills/ccf/validation/script-analyst/SKILL.md`
2. Load Alchemy Principles for compliance checking

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify generated script exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Analyst SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load script + soul + vibe_comments", status: "pending" },
    { id: "step-4", description: "STEP 4: ANALYZE - Score across 7 dimensions", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write analysis_report.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - All dimensions present + scored", status: "pending" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 3: INGEST

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify generated script exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Analyst SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load script + soul + vibe_comments", status: "in_progress" },
    { id: "step-4", description: "STEP 4: ANALYZE - Score across 7 dimensions", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write analysis_report.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - All dimensions present + scored", status: "pending" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

1. Load the generated script
2. Load `soul_values.json` (for voice fidelity comparison)
3. Load `vibe_comments_processed.json` (for tribe alignment check)
4. Load `{blueprint_id}_reasoning_log.json` if available

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify generated script exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Analyst SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load script + soul + vibe_comments", status: "completed" },
    { id: "step-4", description: "STEP 4: ANALYZE - Score across 7 dimensions", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write analysis_report.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - All dimensions present + scored", status: "pending" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 4: ANALYZE — Score 7 Dimensions

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify generated script exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Analyst SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load script + soul + vibe_comments", status: "completed" },
    { id: "step-4", description: "STEP 4: ANALYZE - Score across 7 dimensions", status: "in_progress" },
    { id: "step-5", description: "STEP 5: EMIT - Write analysis_report.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - All dimensions present + scored", status: "pending" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

| # | Dimension | Scoring Guide |
|---|-----------|---------------|
| 1 | **Voice Fidelity** | 10=indistinguishable, 5=recognizable, 1=generic |
| 2 | **Emotional Arc** | 10=perfect TTT calibration, 5=mostly right, 1=flat |
| 3 | **Vulnerability** | 10=uncomfortably real, 5=present but generic, 1=absent |
| 4 | **Alchemy Compliance** | Score = principles met (0-10) |
| 5 | **Research Integration** | 10=seamless, 5=present but forced, 1=absent |
| 6 | **Hook Strength** | 10=impossible to scroll past, 5=interesting, 1=generic |
| 7 | **CTA Power** | 10=feels like a movement, 5=okay ending, 1=marketing CTA |

For each: Score (1-10), Justification (1-2 sentences), Improvement suggestion (if < 8).

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify generated script exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Analyst SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load script + soul + vibe_comments", status: "completed" },
    { id: "step-4", description: "STEP 4: ANALYZE - Score across 7 dimensions", status: "completed" },
    { id: "step-5", description: "STEP 5: EMIT - Write analysis_report.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - All dimensions present + scored", status: "pending" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 5: EMIT

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify generated script exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Analyst SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load script + soul + vibe_comments", status: "completed" },
    { id: "step-4", description: "STEP 4: ANALYZE - Score across 7 dimensions", status: "completed" },
    { id: "step-5", description: "STEP 5: EMIT - Write analysis_report.json", status: "in_progress" },
    { id: "step-6", description: "STEP 6: VALIDATE - All dimensions present + scored", status: "pending" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

**CREATE FILE:** `output/batches/batch_001/analysis/{blueprint_id}_analysis_report.json`

Composite = average of all 7 dimensions. ≥7.5 → PASS, 6.0-7.4 → REVIEW, <6.0 → FAIL (Phoenix Loop).

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify generated script exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Analyst SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load script + soul + vibe_comments", status: "completed" },
    { id: "step-4", description: "STEP 4: ANALYZE - Score across 7 dimensions", status: "completed" },
    { id: "step-5", description: "STEP 5: EMIT - Write analysis_report.json", status: "completed" },
    { id: "step-6", description: "STEP 6: VALIDATE - All dimensions present + scored", status: "pending" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 6: VALIDATE

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify generated script exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Analyst SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load script + soul + vibe_comments", status: "completed" },
    { id: "step-4", description: "STEP 4: ANALYZE - Score across 7 dimensions", status: "completed" },
    { id: "step-5", description: "STEP 5: EMIT - Write analysis_report.json", status: "completed" },
    { id: "step-6", description: "STEP 6: VALIDATE - All dimensions present + scored", status: "in_progress" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

| # | Gate | Requirement | If Fail |
|---|------|-------------|---------|
| 1 | All 7 dimensions | No missing scores | Score missing |
| 2 | Justifications | Each has 1-2 sentences | Add detail |
| 3 | Composite calculated | Average of all 7 | Recalculate |
| 4 | Recommendation set | PASS, REVIEW, or FAIL | Set |
| 5 | JSON valid | Parses without error | Fix |

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify generated script exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Analyst SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load script + soul + vibe_comments", status: "completed" },
    { id: "step-4", description: "STEP 4: ANALYZE - Score across 7 dimensions", status: "completed" },
    { id: "step-5", description: "STEP 5: EMIT - Write analysis_report.json", status: "completed" },
    { id: "step-6", description: "STEP 6: VALIDATE - All dimensions present + scored", status: "completed" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 7: CHECKPOINT

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify generated script exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Analyst SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load script + soul + vibe_comments", status: "completed" },
    { id: "step-4", description: "STEP 4: ANALYZE - Score across 7 dimensions", status: "completed" },
    { id: "step-5", description: "STEP 5: EMIT - Write analysis_report.json", status: "completed" },
    { id: "step-6", description: "STEP 6: VALIDATE - All dimensions present + scored", status: "completed" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "in_progress" }
] });
```

**OUTPUT:**
```
✅ SCRIPT ANALYSIS COMPLETE ({blueprint_id})
- Composite: {N}/10
- Recommendation: {PASS|REVIEW|FAIL}
- Voice: {N}/10 | Hook: {N}/10 | Vulnerability: {N}/10
- NEXT: /ccf-validate {client_name} --blueprint {blueprint_id}
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify generated script exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Analyst SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load script + soul + vibe_comments", status: "completed" },
    { id: "step-4", description: "STEP 4: ANALYZE - Score across 7 dimensions", status: "completed" },
    { id: "step-5", description: "STEP 5: EMIT - Write analysis_report.json", status: "completed" },
    { id: "step-6", description: "STEP 6: VALIDATE - All dimensions present + scored", status: "completed" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "completed" }
] });
```

---

## 🔗 NEXT: `/ccf-validate {client_name} --blueprint {blueprint_id}`
