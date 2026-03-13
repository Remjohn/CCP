---
name: ccf-adapt
description: "Mirror Session — upgrade base prompt through 14 SoC-informed questions"
---

# /ccf-adapt {client_name} --blueprint {blueprint_id}

// turbo-all

> **SKILLS_BASE:** `ccf-26/skills/ccf/`
> **SKILL:** `production/mirror-session/SKILL.md`
> **STAGE:** 2 of 4 (Strategic Refinement)
> **TEMPERATURE:** 0.7

**Objective:** Upgrade the base archetype prompt through a 14-question mirror session informed by SoC output, producing `{blueprint_id}_upgraded_prompt.md`.

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify SoC output + base prompt exist", status: "pending" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Mirror Session SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read SoC output + base prompt + vibe_comments", status: "pending" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles", status: "pending" },
    { id: "step-5", description: "STEP 5: MIRROR Phase 1 - Soul Questions (Q1-Q4)", status: "pending" },
    { id: "step-6", description: "STEP 6: MIRROR Phase 2 - Strategy Questions (Q5-Q9)", status: "pending" },
    { id: "step-7", description: "STEP 7: MIRROR Phase 3 - Integration Questions (Q10-Q12)", status: "pending" },
    { id: "step-8", description: "STEP 8: MIRROR Phase 4 - Calibration Questions (Q13-Q14)", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write upgraded_prompt.md", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
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
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify SoC output + base prompt exist", status: "in_progress" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Mirror Session SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read SoC output + base prompt + vibe_comments", status: "pending" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles", status: "pending" },
    { id: "step-5", description: "STEP 5: MIRROR Phase 1 - Soul Questions (Q1-Q4)", status: "pending" },
    { id: "step-6", description: "STEP 6: MIRROR Phase 2 - Strategy Questions (Q5-Q9)", status: "pending" },
    { id: "step-7", description: "STEP 7: MIRROR Phase 3 - Integration Questions (Q10-Q12)", status: "pending" },
    { id: "step-8", description: "STEP 8: MIRROR Phase 4 - Calibration Questions (Q13-Q14)", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write upgraded_prompt.md", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

| Check | Path | If Missing |
|-------|------|------------|
| 1 | `output/batches/batch_001/soc/{blueprint_id}_soc_output.json` | STOP → Run `/ccf-soc` |
| 2 | `output/batches/batch_001/blueprints/content_blueprints.json` | STOP → Run `/ccf-blueprint` |
| 3 | `research/vibe_comments/vibe_comments_processed.json` | STOP → Run `/ccf-vibe-comments` |
| 4 | Archetype prompt from `ccf-26/Script Prompts/` | STOP → Missing prompt file |

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify SoC output + base prompt exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Mirror Session SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read SoC output + base prompt + vibe_comments", status: "pending" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles", status: "pending" },
    { id: "step-5", description: "STEP 5: MIRROR Phase 1 - Soul Questions (Q1-Q4)", status: "pending" },
    { id: "step-6", description: "STEP 6: MIRROR Phase 2 - Strategy Questions (Q5-Q9)", status: "pending" },
    { id: "step-7", description: "STEP 7: MIRROR Phase 3 - Integration Questions (Q10-Q12)", status: "pending" },
    { id: "step-8", description: "STEP 8: MIRROR Phase 4 - Calibration Questions (Q13-Q14)", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write upgraded_prompt.md", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 2: LOAD SKILL

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify SoC output + base prompt exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Mirror Session SKILL.md", status: "in_progress" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read SoC output + base prompt + vibe_comments", status: "pending" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles", status: "pending" },
    { id: "step-5", description: "STEP 5: MIRROR Phase 1 - Soul Questions (Q1-Q4)", status: "pending" },
    { id: "step-6", description: "STEP 6: MIRROR Phase 2 - Strategy Questions (Q5-Q9)", status: "pending" },
    { id: "step-7", description: "STEP 7: MIRROR Phase 3 - Integration Questions (Q10-Q12)", status: "pending" },
    { id: "step-8", description: "STEP 8: MIRROR Phase 4 - Calibration Questions (Q13-Q14)", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write upgraded_prompt.md", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

1. Read: `ccf-26/skills/ccf/production/mirror-session/SKILL.md`

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify SoC output + base prompt exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Mirror Session SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read SoC output + base prompt + vibe_comments", status: "pending" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles", status: "pending" },
    { id: "step-5", description: "STEP 5: MIRROR Phase 1 - Soul Questions (Q1-Q4)", status: "pending" },
    { id: "step-6", description: "STEP 6: MIRROR Phase 2 - Strategy Questions (Q5-Q9)", status: "pending" },
    { id: "step-7", description: "STEP 7: MIRROR Phase 3 - Integration Questions (Q10-Q12)", status: "pending" },
    { id: "step-8", description: "STEP 8: MIRROR Phase 4 - Calibration Questions (Q13-Q14)", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write upgraded_prompt.md", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 3: LOAD CONTEXT

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify SoC output + base prompt exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Mirror Session SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read SoC output + base prompt + vibe_comments", status: "in_progress" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles", status: "pending" },
    { id: "step-5", description: "STEP 5: MIRROR Phase 1 - Soul Questions (Q1-Q4)", status: "pending" },
    { id: "step-6", description: "STEP 6: MIRROR Phase 2 - Strategy Questions (Q5-Q9)", status: "pending" },
    { id: "step-7", description: "STEP 7: MIRROR Phase 3 - Integration Questions (Q10-Q12)", status: "pending" },
    { id: "step-8", description: "STEP 8: MIRROR Phase 4 - Calibration Questions (Q13-Q14)", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write upgraded_prompt.md", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

1. Load SoC output: `{blueprint_id}_soc_output.json`
2. Load blueprint entry from `content_blueprints.json`
3. Load base archetype prompt from `ccf-26/Script Prompts/`
4. Load `vibe_comments_processed.json`
5. Load relevant research briefs (fresh + deep for this theme)

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify SoC output + base prompt exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Mirror Session SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read SoC output + base prompt + vibe_comments", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles", status: "pending" },
    { id: "step-5", description: "STEP 5: MIRROR Phase 1 - Soul Questions (Q1-Q4)", status: "pending" },
    { id: "step-6", description: "STEP 6: MIRROR Phase 2 - Strategy Questions (Q5-Q9)", status: "pending" },
    { id: "step-7", description: "STEP 7: MIRROR Phase 3 - Integration Questions (Q10-Q12)", status: "pending" },
    { id: "step-8", description: "STEP 8: MIRROR Phase 4 - Calibration Questions (Q13-Q14)", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write upgraded_prompt.md", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 4: INDOCTRINATE

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify SoC output + base prompt exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Mirror Session SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read SoC output + base prompt + vibe_comments", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles", status: "in_progress" },
    { id: "step-5", description: "STEP 5: MIRROR Phase 1 - Soul Questions (Q1-Q4)", status: "pending" },
    { id: "step-6", description: "STEP 6: MIRROR Phase 2 - Strategy Questions (Q5-Q9)", status: "pending" },
    { id: "step-7", description: "STEP 7: MIRROR Phase 3 - Integration Questions (Q10-Q12)", status: "pending" },
    { id: "step-8", description: "STEP 8: MIRROR Phase 4 - Calibration Questions (Q13-Q14)", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write upgraded_prompt.md", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

**State the 10 Alchemy Principles** (mandatory pre-mirror priming).

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify SoC output + base prompt exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Mirror Session SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read SoC output + base prompt + vibe_comments", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles", status: "completed" },
    { id: "step-5", description: "STEP 5: MIRROR Phase 1 - Soul Questions (Q1-Q4)", status: "pending" },
    { id: "step-6", description: "STEP 6: MIRROR Phase 2 - Strategy Questions (Q5-Q9)", status: "pending" },
    { id: "step-7", description: "STEP 7: MIRROR Phase 3 - Integration Questions (Q10-Q12)", status: "pending" },
    { id: "step-8", description: "STEP 8: MIRROR Phase 4 - Calibration Questions (Q13-Q14)", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write upgraded_prompt.md", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 5: MIRROR Phase 1 — Soul Questions (Q1-Q4)

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify SoC output + base prompt exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Mirror Session SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read SoC output + base prompt + vibe_comments", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles", status: "completed" },
    { id: "step-5", description: "STEP 5: MIRROR Phase 1 - Soul Questions (Q1-Q4)", status: "in_progress" },
    { id: "step-6", description: "STEP 6: MIRROR Phase 2 - Strategy Questions (Q5-Q9)", status: "pending" },
    { id: "step-7", description: "STEP 7: MIRROR Phase 3 - Integration Questions (Q10-Q12)", status: "pending" },
    { id: "step-8", description: "STEP 8: MIRROR Phase 4 - Calibration Questions (Q13-Q14)", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write upgraded_prompt.md", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

Answer Q1-Q4 from SoC output + soul_values:
- **Q1:** Core Value (which soul value is this content idea closest to?)
- **Q2:** What would the coach ACTUALLY say about this? (voice fidelity)
- **Q3:** What experience from the coach's life relates? (vulnerability move source)
- **Q4:** What would the coach NEVER say? (anti-patterns)

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify SoC output + base prompt exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Mirror Session SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read SoC output + base prompt + vibe_comments", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles", status: "completed" },
    { id: "step-5", description: "STEP 5: MIRROR Phase 1 - Soul Questions (Q1-Q4)", status: "completed" },
    { id: "step-6", description: "STEP 6: MIRROR Phase 2 - Strategy Questions (Q5-Q9)", status: "pending" },
    { id: "step-7", description: "STEP 7: MIRROR Phase 3 - Integration Questions (Q10-Q12)", status: "pending" },
    { id: "step-8", description: "STEP 8: MIRROR Phase 4 - Calibration Questions (Q13-Q14)", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write upgraded_prompt.md", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 6: MIRROR Phase 2 — Strategy Questions (Q5-Q9)

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify SoC output + base prompt exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Mirror Session SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read SoC output + base prompt + vibe_comments", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles", status: "completed" },
    { id: "step-5", description: "STEP 5: MIRROR Phase 1 - Soul Questions (Q1-Q4)", status: "completed" },
    { id: "step-6", description: "STEP 6: MIRROR Phase 2 - Strategy Questions (Q5-Q9)", status: "in_progress" },
    { id: "step-7", description: "STEP 7: MIRROR Phase 3 - Integration Questions (Q10-Q12)", status: "pending" },
    { id: "step-8", description: "STEP 8: MIRROR Phase 4 - Calibration Questions (Q13-Q14)", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write upgraded_prompt.md", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

Answer Q5-Q9 from SoC + research + vibe_comments:
- **Q5:** Hook Design (Information Gap strategy — Alchemy P3)
- **Q6:** Decisive Claim (One claim to stake — Alchemy P2)
- **Q7:** Research Evidence (What data supports this? — specifics only)
- **Q8:** Vulnerability Positioning (Where in the script? — Alchemy P1)
- **Q9:** Tribal Language (What vibe-comment phrases to weave in?)

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify SoC output + base prompt exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Mirror Session SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read SoC output + base prompt + vibe_comments", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles", status: "completed" },
    { id: "step-5", description: "STEP 5: MIRROR Phase 1 - Soul Questions (Q1-Q4)", status: "completed" },
    { id: "step-6", description: "STEP 6: MIRROR Phase 2 - Strategy Questions (Q5-Q9)", status: "completed" },
    { id: "step-7", description: "STEP 7: MIRROR Phase 3 - Integration Questions (Q10-Q12)", status: "pending" },
    { id: "step-8", description: "STEP 8: MIRROR Phase 4 - Calibration Questions (Q13-Q14)", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write upgraded_prompt.md", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 7: MIRROR Phase 3 — Integration Questions (Q10-Q12)

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify SoC output + base prompt exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Mirror Session SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read SoC output + base prompt + vibe_comments", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles", status: "completed" },
    { id: "step-5", description: "STEP 5: MIRROR Phase 1 - Soul Questions (Q1-Q4)", status: "completed" },
    { id: "step-6", description: "STEP 6: MIRROR Phase 2 - Strategy Questions (Q5-Q9)", status: "completed" },
    { id: "step-7", description: "STEP 7: MIRROR Phase 3 - Integration Questions (Q10-Q12)", status: "in_progress" },
    { id: "step-8", description: "STEP 8: MIRROR Phase 4 - Calibration Questions (Q13-Q14)", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write upgraded_prompt.md", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

Answer Q10-Q12:
- **Q10:** Shadow Integration (What complexity should be acknowledged? — Alchemy P9)
- **Q11:** Context Injection (What context transforms this from content to coaching? — Alchemy P4)
- **Q12:** CTA Direction (What action drives tribal belonging, NOT marketing?)

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify SoC output + base prompt exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Mirror Session SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read SoC output + base prompt + vibe_comments", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles", status: "completed" },
    { id: "step-5", description: "STEP 5: MIRROR Phase 1 - Soul Questions (Q1-Q4)", status: "completed" },
    { id: "step-6", description: "STEP 6: MIRROR Phase 2 - Strategy Questions (Q5-Q9)", status: "completed" },
    { id: "step-7", description: "STEP 7: MIRROR Phase 3 - Integration Questions (Q10-Q12)", status: "completed" },
    { id: "step-8", description: "STEP 8: MIRROR Phase 4 - Calibration Questions (Q13-Q14)", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write upgraded_prompt.md", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 8: MIRROR Phase 4 — Calibration Questions (Q13-Q14)

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify SoC output + base prompt exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Mirror Session SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read SoC output + base prompt + vibe_comments", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles", status: "completed" },
    { id: "step-5", description: "STEP 5: MIRROR Phase 1 - Soul Questions (Q1-Q4)", status: "completed" },
    { id: "step-6", description: "STEP 6: MIRROR Phase 2 - Strategy Questions (Q5-Q9)", status: "completed" },
    { id: "step-7", description: "STEP 7: MIRROR Phase 3 - Integration Questions (Q10-Q12)", status: "completed" },
    { id: "step-8", description: "STEP 8: MIRROR Phase 4 - Calibration Questions (Q13-Q14)", status: "in_progress" },
    { id: "step-9", description: "STEP 9: EMIT - Write upgraded_prompt.md", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

- **Q13:** Template Choice (Confirm or modify the assigned archetype)
- **Q14:** SoC Preservation (List exact phrases from SoC that MUST appear verbatim in final script)

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify SoC output + base prompt exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Mirror Session SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read SoC output + base prompt + vibe_comments", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles", status: "completed" },
    { id: "step-5", description: "STEP 5: MIRROR Phase 1 - Soul Questions (Q1-Q4)", status: "completed" },
    { id: "step-6", description: "STEP 6: MIRROR Phase 2 - Strategy Questions (Q5-Q9)", status: "completed" },
    { id: "step-7", description: "STEP 7: MIRROR Phase 3 - Integration Questions (Q10-Q12)", status: "completed" },
    { id: "step-8", description: "STEP 8: MIRROR Phase 4 - Calibration Questions (Q13-Q14)", status: "completed" },
    { id: "step-9", description: "STEP 9: EMIT - Write upgraded_prompt.md", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 9: EMIT

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify SoC output + base prompt exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Mirror Session SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read SoC output + base prompt + vibe_comments", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles", status: "completed" },
    { id: "step-5", description: "STEP 5: MIRROR Phase 1 - Soul Questions (Q1-Q4)", status: "completed" },
    { id: "step-6", description: "STEP 6: MIRROR Phase 2 - Strategy Questions (Q5-Q9)", status: "completed" },
    { id: "step-7", description: "STEP 7: MIRROR Phase 3 - Integration Questions (Q10-Q12)", status: "completed" },
    { id: "step-8", description: "STEP 8: MIRROR Phase 4 - Calibration Questions (Q13-Q14)", status: "completed" },
    { id: "step-9", description: "STEP 9: EMIT - Write upgraded_prompt.md", status: "in_progress" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

**CREATE FILE:** `output/batches/batch_001/adapted/{blueprint_id}_upgraded_prompt.md`

The upgraded prompt contains the base archetype template PLUS all 14 Q&A answers injected as context. This becomes the input for Stage 2.5 (Wisdom Forge).

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify SoC output + base prompt exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Mirror Session SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read SoC output + base prompt + vibe_comments", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles", status: "completed" },
    { id: "step-5", description: "STEP 5: MIRROR Phase 1 - Soul Questions (Q1-Q4)", status: "completed" },
    { id: "step-6", description: "STEP 6: MIRROR Phase 2 - Strategy Questions (Q5-Q9)", status: "completed" },
    { id: "step-7", description: "STEP 7: MIRROR Phase 3 - Integration Questions (Q10-Q12)", status: "completed" },
    { id: "step-8", description: "STEP 8: MIRROR Phase 4 - Calibration Questions (Q13-Q14)", status: "completed" },
    { id: "step-9", description: "STEP 9: EMIT - Write upgraded_prompt.md", status: "completed" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 10: CHECKPOINT

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify SoC output + base prompt exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Mirror Session SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read SoC output + base prompt + vibe_comments", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles", status: "completed" },
    { id: "step-5", description: "STEP 5: MIRROR Phase 1 - Soul Questions (Q1-Q4)", status: "completed" },
    { id: "step-6", description: "STEP 6: MIRROR Phase 2 - Strategy Questions (Q5-Q9)", status: "completed" },
    { id: "step-7", description: "STEP 7: MIRROR Phase 3 - Integration Questions (Q10-Q12)", status: "completed" },
    { id: "step-8", description: "STEP 8: MIRROR Phase 4 - Calibration Questions (Q13-Q14)", status: "completed" },
    { id: "step-9", description: "STEP 9: EMIT - Write upgraded_prompt.md", status: "completed" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "in_progress" }
] });
```

Update `config.yaml`: `sessions.production.{blueprint_id}.adapt.status = "complete"`

**OUTPUT:**
```
✅ MIRROR SESSION COMPLETE ({blueprint_id})
- 14 questions answered
- Upgraded prompt: adapted/{blueprint_id}_upgraded_prompt.md
- NEXT: /ccf-wisdom {client_name} --blueprint {blueprint_id}
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify SoC output + base prompt exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Mirror Session SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read SoC output + base prompt + vibe_comments", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles", status: "completed" },
    { id: "step-5", description: "STEP 5: MIRROR Phase 1 - Soul Questions (Q1-Q4)", status: "completed" },
    { id: "step-6", description: "STEP 6: MIRROR Phase 2 - Strategy Questions (Q5-Q9)", status: "completed" },
    { id: "step-7", description: "STEP 7: MIRROR Phase 3 - Integration Questions (Q10-Q12)", status: "completed" },
    { id: "step-8", description: "STEP 8: MIRROR Phase 4 - Calibration Questions (Q13-Q14)", status: "completed" },
    { id: "step-9", description: "STEP 9: EMIT - Write upgraded_prompt.md", status: "completed" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "completed" }
] });
```

---

## 🔗 NEXT: `/ccf-wisdom {client_name} --blueprint {blueprint_id}`
