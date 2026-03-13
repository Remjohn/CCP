---
name: ccf-vibe-comments
description: Generate audience-intelligence processed vibe comments for script calibration
---

# /ccf-vibe-comments {client_name}

// turbo-all

> **SKILLS_BASE:** `ccf-26/skills/ccf/`
> **SKILL:** `research/vibe-comment-processor/SKILL.md`
> **TEMPERATURE:** 0.5

**Objective:** Process raw audience comments through the AIP 5-lens protocol to produce `vibe_comments_processed.json` — the audience intelligence that calibrates scripts.

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify audience data + soul/tribe outputs", status: "pending" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Vibe Comment Processor SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: INGEST - Load raw audience comments + tribe_profile", status: "pending" },
    { id: "step-4", description: "STEP 4: PROCESS - Apply AIP 5-Lens Protocol", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write vibe_comments_processed.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Completeness + Alchemy alignment", status: "pending" },
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
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify audience data + soul/tribe outputs", status: "in_progress" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Vibe Comment Processor SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: INGEST - Load raw audience comments + tribe_profile", status: "pending" },
    { id: "step-4", description: "STEP 4: PROCESS - Apply AIP 5-Lens Protocol", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write vibe_comments_processed.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Completeness + Alchemy alignment", status: "pending" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

| Check | Path | If Missing |
|-------|------|------------|
| 1 | `raw/audience/` (≥1 file with comments) | STOP → Need audience data |
| 2 | `intelligence/soul/soul_values.json` | STOP → Run `/ccf-soul-extract` |
| 3 | `intelligence/tribe/tribe_profile.json` | STOP → Run `/ccf-tribe-extract` |

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify audience data + soul/tribe outputs", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Vibe Comment Processor SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: INGEST - Load raw audience comments + tribe_profile", status: "pending" },
    { id: "step-4", description: "STEP 4: PROCESS - Apply AIP 5-Lens Protocol", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write vibe_comments_processed.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Completeness + Alchemy alignment", status: "pending" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 2: LOAD SKILL

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify audience data + soul/tribe outputs", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Vibe Comment Processor SKILL.md", status: "in_progress" },
    { id: "step-3", description: "STEP 3: INGEST - Load raw audience comments + tribe_profile", status: "pending" },
    { id: "step-4", description: "STEP 4: PROCESS - Apply AIP 5-Lens Protocol", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write vibe_comments_processed.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Completeness + Alchemy alignment", status: "pending" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

1. Read: `ccf-26/skills/ccf/research/vibe-comment-processor/SKILL.md`

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify audience data + soul/tribe outputs", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Vibe Comment Processor SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load raw audience comments + tribe_profile", status: "pending" },
    { id: "step-4", description: "STEP 4: PROCESS - Apply AIP 5-Lens Protocol", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write vibe_comments_processed.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Completeness + Alchemy alignment", status: "pending" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 3: INGEST

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify audience data + soul/tribe outputs", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Vibe Comment Processor SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load raw audience comments + tribe_profile", status: "in_progress" },
    { id: "step-4", description: "STEP 4: PROCESS - Apply AIP 5-Lens Protocol", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write vibe_comments_processed.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Completeness + Alchemy alignment", status: "pending" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

1. Load ALL audience comment files from `raw/audience/`
2. Load `tribe_profile.json` for cultural context calibration
3. Report: "Loaded {N} comments from {M} sources"

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify audience data + soul/tribe outputs", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Vibe Comment Processor SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load raw audience comments + tribe_profile", status: "completed" },
    { id: "step-4", description: "STEP 4: PROCESS - Apply AIP 5-Lens Protocol", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write vibe_comments_processed.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Completeness + Alchemy alignment", status: "pending" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 4: PROCESS (AIP 5-Lens Protocol)

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify audience data + soul/tribe outputs", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Vibe Comment Processor SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load raw audience comments + tribe_profile", status: "completed" },
    { id: "step-4", description: "STEP 4: PROCESS - Apply AIP 5-Lens Protocol", status: "in_progress" },
    { id: "step-5", description: "STEP 5: EMIT - Write vibe_comments_processed.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Completeness + Alchemy alignment", status: "pending" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

**Before processing, state the 10 Alchemy Principles** (mandatory priming).

**Apply 5 AIP Lenses to the comment corpus:**

| Lens | What to Extract |
|------|----------------|
| 1. Engagement | What topics get most views/likes/shares? |
| 2. Needs | What problems do commenters describe? |
| 3. Language | What exact phrases/slang do they use? |
| 4. Objections | What pushback appears? What do they resist? |
| 5. Desires | What do they want to feel/achieve/become? |

**For each lens:** Extract top patterns + verbatim quote examples.

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify audience data + soul/tribe outputs", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Vibe Comment Processor SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load raw audience comments + tribe_profile", status: "completed" },
    { id: "step-4", description: "STEP 4: PROCESS - Apply AIP 5-Lens Protocol", status: "completed" },
    { id: "step-5", description: "STEP 5: EMIT - Write vibe_comments_processed.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Completeness + Alchemy alignment", status: "pending" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 5: EMIT

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify audience data + soul/tribe outputs", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Vibe Comment Processor SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load raw audience comments + tribe_profile", status: "completed" },
    { id: "step-4", description: "STEP 4: PROCESS - Apply AIP 5-Lens Protocol", status: "completed" },
    { id: "step-5", description: "STEP 5: EMIT - Write vibe_comments_processed.json", status: "in_progress" },
    { id: "step-6", description: "STEP 6: VALIDATE - Completeness + Alchemy alignment", status: "pending" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

**CREATE FILE:** `research/vibe_comments/vibe_comments_processed.json`

Schema: 5 lenses, each with `patterns[]` (pattern name + frequency + verbatim quotes) and `top_insight`.

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify audience data + soul/tribe outputs", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Vibe Comment Processor SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load raw audience comments + tribe_profile", status: "completed" },
    { id: "step-4", description: "STEP 4: PROCESS - Apply AIP 5-Lens Protocol", status: "completed" },
    { id: "step-5", description: "STEP 5: EMIT - Write vibe_comments_processed.json", status: "completed" },
    { id: "step-6", description: "STEP 6: VALIDATE - Completeness + Alchemy alignment", status: "pending" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 6: VALIDATE

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify audience data + soul/tribe outputs", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Vibe Comment Processor SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load raw audience comments + tribe_profile", status: "completed" },
    { id: "step-4", description: "STEP 4: PROCESS - Apply AIP 5-Lens Protocol", status: "completed" },
    { id: "step-5", description: "STEP 5: EMIT - Write vibe_comments_processed.json", status: "completed" },
    { id: "step-6", description: "STEP 6: VALIDATE - Completeness + Alchemy alignment", status: "in_progress" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

| # | Gate | Requirement | If Fail |
|---|------|-------------|---------|
| 1 | All 5 lenses | Each lens has ≥2 patterns | Fill missing |
| 2 | Verbatim quotes | EXACT copies from source | Fix paraphrased |
| 3 | JSON valid | Parses without error | Fix syntax |
| 4 | Alchemy alignment | Patterns connect to ≥5 Alchemy Principles | Add connections |
| 5 | Tribe coherence | Patterns match tribe_profile | Cross-reference |

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify audience data + soul/tribe outputs", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Vibe Comment Processor SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load raw audience comments + tribe_profile", status: "completed" },
    { id: "step-4", description: "STEP 4: PROCESS - Apply AIP 5-Lens Protocol", status: "completed" },
    { id: "step-5", description: "STEP 5: EMIT - Write vibe_comments_processed.json", status: "completed" },
    { id: "step-6", description: "STEP 6: VALIDATE - Completeness + Alchemy alignment", status: "completed" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 7: CHECKPOINT

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify audience data + soul/tribe outputs", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Vibe Comment Processor SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load raw audience comments + tribe_profile", status: "completed" },
    { id: "step-4", description: "STEP 4: PROCESS - Apply AIP 5-Lens Protocol", status: "completed" },
    { id: "step-5", description: "STEP 5: EMIT - Write vibe_comments_processed.json", status: "completed" },
    { id: "step-6", description: "STEP 6: VALIDATE - Completeness + Alchemy alignment", status: "completed" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "in_progress" }
] });
```

Update `config.yaml`: `sessions.research.vibe_comments.status = "complete"`

**OUTPUT (25-35 words):**
```
✅ VIBE COMMENTS PROCESSED
- Lenses: 5/5 complete
- Patterns: {N} total across all lenses
- Verbatim quotes: {N}
- NEXT: /ccf-soc OR /ccf-batch {client_name}
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify audience data + soul/tribe outputs", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Vibe Comment Processor SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load raw audience comments + tribe_profile", status: "completed" },
    { id: "step-4", description: "STEP 4: PROCESS - Apply AIP 5-Lens Protocol", status: "completed" },
    { id: "step-5", description: "STEP 5: EMIT - Write vibe_comments_processed.json", status: "completed" },
    { id: "step-6", description: "STEP 6: VALIDATE - Completeness + Alchemy alignment", status: "completed" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml", status: "completed" }
] });
```

---

## 🔗 NEXT: `/ccf-soc {client_name} --blueprint {blueprint_id}` OR `/ccf-batch {client_name}`
