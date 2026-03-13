---
name: ccf-validate
description: "Stage 4: Triple validation + Alchemy Gate for generated scripts"
---

# /ccf-validate {client_name} --blueprint {blueprint_id}

// turbo-all

> **SKILLS_BASE:** `ccf-26/skills/ccf/`
> **SKILL:** `validation/script-validator/SKILL.md`
> **MODEL:** Use validation model (gemini-2.5-flash)
> **TEMPERATURE:** 0.1

**Objective:** Run the triple validation pipeline: Analysis Review → Red Flag Scan → Alchemy Gate. This is the FINAL quality checkpoint before output.

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify analysis_report + script exist", status: "pending" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Validator SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: VALIDATION 1 - Analysis Review (7 dimensions check)", status: "pending" },
    { id: "step-4", description: "STEP 4: VALIDATION 2 - Red Flag Scan (10 anti-patterns)", status: "pending" },
    { id: "step-5", description: "STEP 5: VALIDATION 3 - Humanity Score (authenticity check)", status: "pending" },
    { id: "step-6", description: "STEP 6: ALCHEMY GATE - 10-principle binary compliance", status: "pending" },
    { id: "step-7", description: "STEP 7: DECISION - PASS, REVIEW, FAIL, or PHOENIX", status: "pending" },
    { id: "step-8", description: "STEP 8: EMIT - Write validation_report.json", status: "pending" },
    { id: "step-9", description: "STEP 9: CHECKPOINT - Update config.yaml", status: "pending" }
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
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify analysis_report + script exist", status: "in_progress" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Validator SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: VALIDATION 1 - Analysis Review (7 dimensions check)", status: "pending" },
    { id: "step-4", description: "STEP 4: VALIDATION 2 - Red Flag Scan (10 anti-patterns)", status: "pending" },
    { id: "step-5", description: "STEP 5: VALIDATION 3 - Humanity Score (authenticity check)", status: "pending" },
    { id: "step-6", description: "STEP 6: ALCHEMY GATE - 10-principle binary compliance", status: "pending" },
    { id: "step-7", description: "STEP 7: DECISION - PASS, REVIEW, FAIL, or PHOENIX", status: "pending" },
    { id: "step-8", description: "STEP 8: EMIT - Write validation_report.json", status: "pending" },
    { id: "step-9", description: "STEP 9: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

| Check | Path | If Missing |
|-------|------|------------|
| 1 | `scripts/{blueprint_id}_generated_script.md` | STOP → Run `/ccf-generate` |
| 2 | `analysis/{blueprint_id}_analysis_report.json` | STOP → Run `/ccf-analyze` |
| 3 | `intelligence/soul/soul_values.json` | STOP |

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify analysis_report + script exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Validator SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: VALIDATION 1 - Analysis Review (7 dimensions check)", status: "pending" },
    { id: "step-4", description: "STEP 4: VALIDATION 2 - Red Flag Scan (10 anti-patterns)", status: "pending" },
    { id: "step-5", description: "STEP 5: VALIDATION 3 - Humanity Score (authenticity check)", status: "pending" },
    { id: "step-6", description: "STEP 6: ALCHEMY GATE - 10-principle binary compliance", status: "pending" },
    { id: "step-7", description: "STEP 7: DECISION - PASS, REVIEW, FAIL, or PHOENIX", status: "pending" },
    { id: "step-8", description: "STEP 8: EMIT - Write validation_report.json", status: "pending" },
    { id: "step-9", description: "STEP 9: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 2: LOAD SKILL

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify analysis_report + script exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Validator SKILL.md", status: "in_progress" },
    { id: "step-3", description: "STEP 3: VALIDATION 1 - Analysis Review (7 dimensions check)", status: "pending" },
    { id: "step-4", description: "STEP 4: VALIDATION 2 - Red Flag Scan (10 anti-patterns)", status: "pending" },
    { id: "step-5", description: "STEP 5: VALIDATION 3 - Humanity Score (authenticity check)", status: "pending" },
    { id: "step-6", description: "STEP 6: ALCHEMY GATE - 10-principle binary compliance", status: "pending" },
    { id: "step-7", description: "STEP 7: DECISION - PASS, REVIEW, FAIL, or PHOENIX", status: "pending" },
    { id: "step-8", description: "STEP 8: EMIT - Write validation_report.json", status: "pending" },
    { id: "step-9", description: "STEP 9: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

1. Read: `ccf-26/skills/ccf/validation/script-validator/SKILL.md`

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify analysis_report + script exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Validator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: VALIDATION 1 - Analysis Review (7 dimensions check)", status: "pending" },
    { id: "step-4", description: "STEP 4: VALIDATION 2 - Red Flag Scan (10 anti-patterns)", status: "pending" },
    { id: "step-5", description: "STEP 5: VALIDATION 3 - Humanity Score (authenticity check)", status: "pending" },
    { id: "step-6", description: "STEP 6: ALCHEMY GATE - 10-principle binary compliance", status: "pending" },
    { id: "step-7", description: "STEP 7: DECISION - PASS, REVIEW, FAIL, or PHOENIX", status: "pending" },
    { id: "step-8", description: "STEP 8: EMIT - Write validation_report.json", status: "pending" },
    { id: "step-9", description: "STEP 9: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 3: VALIDATION 1 — Analysis Review

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify analysis_report + script exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Validator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: VALIDATION 1 - Analysis Review (7 dimensions check)", status: "in_progress" },
    { id: "step-4", description: "STEP 4: VALIDATION 2 - Red Flag Scan (10 anti-patterns)", status: "pending" },
    { id: "step-5", description: "STEP 5: VALIDATION 3 - Humanity Score (authenticity check)", status: "pending" },
    { id: "step-6", description: "STEP 6: ALCHEMY GATE - 10-principle binary compliance", status: "pending" },
    { id: "step-7", description: "STEP 7: DECISION - PASS, REVIEW, FAIL, or PHOENIX", status: "pending" },
    { id: "step-8", description: "STEP 8: EMIT - Write validation_report.json", status: "pending" },
    { id: "step-9", description: "STEP 9: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

Review analysis_report dimensions. All 7 must be ≥7 to pass. Any <7 → flag for improvement.

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify analysis_report + script exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Validator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: VALIDATION 1 - Analysis Review (7 dimensions check)", status: "completed" },
    { id: "step-4", description: "STEP 4: VALIDATION 2 - Red Flag Scan (10 anti-patterns)", status: "pending" },
    { id: "step-5", description: "STEP 5: VALIDATION 3 - Humanity Score (authenticity check)", status: "pending" },
    { id: "step-6", description: "STEP 6: ALCHEMY GATE - 10-principle binary compliance", status: "pending" },
    { id: "step-7", description: "STEP 7: DECISION - PASS, REVIEW, FAIL, or PHOENIX", status: "pending" },
    { id: "step-8", description: "STEP 8: EMIT - Write validation_report.json", status: "pending" },
    { id: "step-9", description: "STEP 9: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 4: VALIDATION 2 — Red Flag Scan

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify analysis_report + script exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Validator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: VALIDATION 1 - Analysis Review (7 dimensions check)", status: "completed" },
    { id: "step-4", description: "STEP 4: VALIDATION 2 - Red Flag Scan (10 anti-patterns)", status: "in_progress" },
    { id: "step-5", description: "STEP 5: VALIDATION 3 - Humanity Score (authenticity check)", status: "pending" },
    { id: "step-6", description: "STEP 6: ALCHEMY GATE - 10-principle binary compliance", status: "pending" },
    { id: "step-7", description: "STEP 7: DECISION - PASS, REVIEW, FAIL, or PHOENIX", status: "pending" },
    { id: "step-8", description: "STEP 8: EMIT - Write validation_report.json", status: "pending" },
    { id: "step-9", description: "STEP 9: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

Scan for 10 Red Flags (RF1-RF10): AI language, generic phrasing, missing vulnerability move, filler words, lecture tone, etc. Target: 0 red flags.

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify analysis_report + script exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Validator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: VALIDATION 1 - Analysis Review (7 dimensions check)", status: "completed" },
    { id: "step-4", description: "STEP 4: VALIDATION 2 - Red Flag Scan (10 anti-patterns)", status: "completed" },
    { id: "step-5", description: "STEP 5: VALIDATION 3 - Humanity Score (authenticity check)", status: "pending" },
    { id: "step-6", description: "STEP 6: ALCHEMY GATE - 10-principle binary compliance", status: "pending" },
    { id: "step-7", description: "STEP 7: DECISION - PASS, REVIEW, FAIL, or PHOENIX", status: "pending" },
    { id: "step-8", description: "STEP 8: EMIT - Write validation_report.json", status: "pending" },
    { id: "step-9", description: "STEP 9: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 5: VALIDATION 3 — Humanity Score

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify analysis_report + script exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Validator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: VALIDATION 1 - Analysis Review (7 dimensions check)", status: "completed" },
    { id: "step-4", description: "STEP 4: VALIDATION 2 - Red Flag Scan (10 anti-patterns)", status: "completed" },
    { id: "step-5", description: "STEP 5: VALIDATION 3 - Humanity Score (authenticity check)", status: "in_progress" },
    { id: "step-6", description: "STEP 6: ALCHEMY GATE - 10-principle binary compliance", status: "pending" },
    { id: "step-7", description: "STEP 7: DECISION - PASS, REVIEW, FAIL, or PHOENIX", status: "pending" },
    { id: "step-8", description: "STEP 8: EMIT - Write validation_report.json", status: "pending" },
    { id: "step-9", description: "STEP 9: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

Score 1-10: "Would a human scroll-stopping in their feed believe a person wrote this?" Must be ≥7- to pass. Check: Natural rhythm, conversational tone, imperfections left intact, perspective is singular and specific (not generic advice).

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify analysis_report + script exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Validator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: VALIDATION 1 - Analysis Review (7 dimensions check)", status: "completed" },
    { id: "step-4", description: "STEP 4: VALIDATION 2 - Red Flag Scan (10 anti-patterns)", status: "completed" },
    { id: "step-5", description: "STEP 5: VALIDATION 3 - Humanity Score (authenticity check)", status: "completed" },
    { id: "step-6", description: "STEP 6: ALCHEMY GATE - 10-principle binary compliance", status: "pending" },
    { id: "step-7", description: "STEP 7: DECISION - PASS, REVIEW, FAIL, or PHOENIX", status: "pending" },
    { id: "step-8", description: "STEP 8: EMIT - Write validation_report.json", status: "pending" },
    { id: "step-9", description: "STEP 9: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 6: ALCHEMY GATE

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify analysis_report + script exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Validator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: VALIDATION 1 - Analysis Review (7 dimensions check)", status: "completed" },
    { id: "step-4", description: "STEP 4: VALIDATION 2 - Red Flag Scan (10 anti-patterns)", status: "completed" },
    { id: "step-5", description: "STEP 5: VALIDATION 3 - Humanity Score (authenticity check)", status: "completed" },
    { id: "step-6", description: "STEP 6: ALCHEMY GATE - 10-principle binary compliance", status: "in_progress" },
    { id: "step-7", description: "STEP 7: DECISION - PASS, REVIEW, FAIL, or PHOENIX", status: "pending" },
    { id: "step-8", description: "STEP 8: EMIT - Write validation_report.json", status: "pending" },
    { id: "step-9", description: "STEP 9: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

Binary check (PASS/FAIL) for each of the 10 Alchemy Principles:

| P# | Principle | ✅/❌ | Evidence |
|----|-----------|-------|----------|
| P1-P10 | Each principle | Binary | Specific line reference |

**Gate Threshold:** ≥8/10 → PASS. 6-7/10 → REVIEW. <6/10 → FAIL (Phoenix Loop).

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify analysis_report + script exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Validator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: VALIDATION 1 - Analysis Review (7 dimensions check)", status: "completed" },
    { id: "step-4", description: "STEP 4: VALIDATION 2 - Red Flag Scan (10 anti-patterns)", status: "completed" },
    { id: "step-5", description: "STEP 5: VALIDATION 3 - Humanity Score (authenticity check)", status: "completed" },
    { id: "step-6", description: "STEP 6: ALCHEMY GATE - 10-principle binary compliance", status: "completed" },
    { id: "step-7", description: "STEP 7: DECISION - PASS, REVIEW, FAIL, or PHOENIX", status: "pending" },
    { id: "step-8", description: "STEP 8: EMIT - Write validation_report.json", status: "pending" },
    { id: "step-9", description: "STEP 9: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 7: DECISION

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify analysis_report + script exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Validator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: VALIDATION 1 - Analysis Review (7 dimensions check)", status: "completed" },
    { id: "step-4", description: "STEP 4: VALIDATION 2 - Red Flag Scan (10 anti-patterns)", status: "completed" },
    { id: "step-5", description: "STEP 5: VALIDATION 3 - Humanity Score (authenticity check)", status: "completed" },
    { id: "step-6", description: "STEP 6: ALCHEMY GATE - 10-principle binary compliance", status: "completed" },
    { id: "step-7", description: "STEP 7: DECISION - PASS, REVIEW, FAIL, or PHOENIX", status: "in_progress" },
    { id: "step-8", description: "STEP 8: EMIT - Write validation_report.json", status: "pending" },
    { id: "step-9", description: "STEP 9: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

| Result | Criteria | Action |
|--------|----------|--------|
| **PASS** | Composite ≥7.5 AND RF=0 AND Humanity≥7 AND Alchemy≥8/10 | → Final output |
| **REVIEW** | One gate marginal | → Flag for human review |
| **FAIL** | Any hard gate failed | → Phoenix Loop (re-generate) |
| **PHOENIX** | >2 failures on same blueprint | → Abort, flag for manual |

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify analysis_report + script exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Validator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: VALIDATION 1 - Analysis Review (7 dimensions check)", status: "completed" },
    { id: "step-4", description: "STEP 4: VALIDATION 2 - Red Flag Scan (10 anti-patterns)", status: "completed" },
    { id: "step-5", description: "STEP 5: VALIDATION 3 - Humanity Score (authenticity check)", status: "completed" },
    { id: "step-6", description: "STEP 6: ALCHEMY GATE - 10-principle binary compliance", status: "completed" },
    { id: "step-7", description: "STEP 7: DECISION - PASS, REVIEW, FAIL, or PHOENIX", status: "completed" },
    { id: "step-8", description: "STEP 8: EMIT - Write validation_report.json", status: "pending" },
    { id: "step-9", description: "STEP 9: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 8: EMIT

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify analysis_report + script exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Validator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: VALIDATION 1 - Analysis Review (7 dimensions check)", status: "completed" },
    { id: "step-4", description: "STEP 4: VALIDATION 2 - Red Flag Scan (10 anti-patterns)", status: "completed" },
    { id: "step-5", description: "STEP 5: VALIDATION 3 - Humanity Score (authenticity check)", status: "completed" },
    { id: "step-6", description: "STEP 6: ALCHEMY GATE - 10-principle binary compliance", status: "completed" },
    { id: "step-7", description: "STEP 7: DECISION - PASS, REVIEW, FAIL, or PHOENIX", status: "completed" },
    { id: "step-8", description: "STEP 8: EMIT - Write validation_report.json", status: "in_progress" },
    { id: "step-9", description: "STEP 9: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

**CREATE FILE:** `output/batches/batch_001/validation/{blueprint_id}_validation_report.json`

Schema: `triple_validation` (analysis, red_flags, humanity), `alchemy_gate` (10 principles), `decision` (PASS/REVIEW/FAIL/PHOENIX), `composite_score`, `phoenix_loop_count`.

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify analysis_report + script exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Validator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: VALIDATION 1 - Analysis Review (7 dimensions check)", status: "completed" },
    { id: "step-4", description: "STEP 4: VALIDATION 2 - Red Flag Scan (10 anti-patterns)", status: "completed" },
    { id: "step-5", description: "STEP 5: VALIDATION 3 - Humanity Score (authenticity check)", status: "completed" },
    { id: "step-6", description: "STEP 6: ALCHEMY GATE - 10-principle binary compliance", status: "completed" },
    { id: "step-7", description: "STEP 7: DECISION - PASS, REVIEW, FAIL, or PHOENIX", status: "completed" },
    { id: "step-8", description: "STEP 8: EMIT - Write validation_report.json", status: "completed" },
    { id: "step-9", description: "STEP 9: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 9: CHECKPOINT

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify analysis_report + script exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Validator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: VALIDATION 1 - Analysis Review (7 dimensions check)", status: "completed" },
    { id: "step-4", description: "STEP 4: VALIDATION 2 - Red Flag Scan (10 anti-patterns)", status: "completed" },
    { id: "step-5", description: "STEP 5: VALIDATION 3 - Humanity Score (authenticity check)", status: "completed" },
    { id: "step-6", description: "STEP 6: ALCHEMY GATE - 10-principle binary compliance", status: "completed" },
    { id: "step-7", description: "STEP 7: DECISION - PASS, REVIEW, FAIL, or PHOENIX", status: "completed" },
    { id: "step-8", description: "STEP 8: EMIT - Write validation_report.json", status: "completed" },
    { id: "step-9", description: "STEP 9: CHECKPOINT - Update config.yaml", status: "in_progress" }
] });
```

**OUTPUT:**
```
✅ VALIDATION COMPLETE ({blueprint_id})
- Decision: {PASS|REVIEW|FAIL}
- Composite: {N}/10
- Red Flags: {N}/10
- Humanity: {N}/10
- Alchemy: {N}/10
- NEXT: Move to final delivery or Phoenix Loop
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify analysis_report + script exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Validator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: VALIDATION 1 - Analysis Review (7 dimensions check)", status: "completed" },
    { id: "step-4", description: "STEP 4: VALIDATION 2 - Red Flag Scan (10 anti-patterns)", status: "completed" },
    { id: "step-5", description: "STEP 5: VALIDATION 3 - Humanity Score (authenticity check)", status: "completed" },
    { id: "step-6", description: "STEP 6: ALCHEMY GATE - 10-principle binary compliance", status: "completed" },
    { id: "step-7", description: "STEP 7: DECISION - PASS, REVIEW, FAIL, or PHOENIX", status: "completed" },
    { id: "step-8", description: "STEP 8: EMIT - Write validation_report.json", status: "completed" },
    { id: "step-9", description: "STEP 9: CHECKPOINT - Update config.yaml", status: "completed" }
] });
```

---

## 🔗 NEXT: `/ccf-batch {client_name}` (for remaining blueprints)
