---
name: ccf-wisdom
description: "Stage 2.5: Wisdom Forge — generate 4 wisdom briefs per blueprint"
---

# /ccf-wisdom {client_name} --blueprint {blueprint_id}

// turbo-all

> **SKILLS_BASE:** `ccf-26/skills/ccf/`
> **SKILL:** `production/wisdom-forge/SKILL.md`
> **STAGE:** 2.5 of 4 (Insight Synthesis)
> **TEMPERATURE:** 0.5

**Objective:** Generate 4 wisdom briefs (Authenticity, Authority, Memetic, Shadow) for the blueprint, producing `{blueprint_id}_wisdom_briefs.json`.

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify adapted prompt + research exist", status: "pending" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Wisdom Forge SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read all inputs for fusion", status: "pending" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + forge rules", status: "pending" },
    { id: "step-5", description: "STEP 5: FORGE Brief 1 - Authenticity Brief", status: "pending" },
    { id: "step-6", description: "STEP 6: FORGE Brief 2 - Authority Brief", status: "pending" },
    { id: "step-7", description: "STEP 7: FORGE Brief 3 - Memetic Brief", status: "pending" },
    { id: "step-8", description: "STEP 8: FORGE Brief 4 - Shadow Brief", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write wisdom_briefs.json", status: "pending" },
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
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify adapted prompt + research exist", status: "in_progress" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Wisdom Forge SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read all inputs for fusion", status: "pending" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + forge rules", status: "pending" },
    { id: "step-5", description: "STEP 5: FORGE Brief 1 - Authenticity Brief", status: "pending" },
    { id: "step-6", description: "STEP 6: FORGE Brief 2 - Authority Brief", status: "pending" },
    { id: "step-7", description: "STEP 7: FORGE Brief 3 - Memetic Brief", status: "pending" },
    { id: "step-8", description: "STEP 8: FORGE Brief 4 - Shadow Brief", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write wisdom_briefs.json", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

| Check | Path | If Missing |
|-------|------|------------|
| 1 | `output/batches/batch_001/adapted/{blueprint_id}_upgraded_prompt.md` | STOP → Run `/ccf-adapt` |
| 2 | `output/batches/batch_001/soc/{blueprint_id}_soc_output.json` | STOP → Run `/ccf-soc` |
| 3 | `intelligence/soul/soul_values.json` | STOP |
| 4 | Research briefs (fresh + deep for this theme) | STOP |

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify adapted prompt + research exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Wisdom Forge SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read all inputs for fusion", status: "pending" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + forge rules", status: "pending" },
    { id: "step-5", description: "STEP 5: FORGE Brief 1 - Authenticity Brief", status: "pending" },
    { id: "step-6", description: "STEP 6: FORGE Brief 2 - Authority Brief", status: "pending" },
    { id: "step-7", description: "STEP 7: FORGE Brief 3 - Memetic Brief", status: "pending" },
    { id: "step-8", description: "STEP 8: FORGE Brief 4 - Shadow Brief", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write wisdom_briefs.json", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 2: LOAD SKILL

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify adapted prompt + research exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Wisdom Forge SKILL.md", status: "in_progress" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read all inputs for fusion", status: "pending" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + forge rules", status: "pending" },
    { id: "step-5", description: "STEP 5: FORGE Brief 1 - Authenticity Brief", status: "pending" },
    { id: "step-6", description: "STEP 6: FORGE Brief 2 - Authority Brief", status: "pending" },
    { id: "step-7", description: "STEP 7: FORGE Brief 3 - Memetic Brief", status: "pending" },
    { id: "step-8", description: "STEP 8: FORGE Brief 4 - Shadow Brief", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write wisdom_briefs.json", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

1. Read: `ccf-26/skills/ccf/production/wisdom-forge/SKILL.md`

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify adapted prompt + research exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Wisdom Forge SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read all inputs for fusion", status: "pending" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + forge rules", status: "pending" },
    { id: "step-5", description: "STEP 5: FORGE Brief 1 - Authenticity Brief", status: "pending" },
    { id: "step-6", description: "STEP 6: FORGE Brief 2 - Authority Brief", status: "pending" },
    { id: "step-7", description: "STEP 7: FORGE Brief 3 - Memetic Brief", status: "pending" },
    { id: "step-8", description: "STEP 8: FORGE Brief 4 - Shadow Brief", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write wisdom_briefs.json", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 3: LOAD CONTEXT

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify adapted prompt + research exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Wisdom Forge SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read all inputs for fusion", status: "in_progress" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + forge rules", status: "pending" },
    { id: "step-5", description: "STEP 5: FORGE Brief 1 - Authenticity Brief", status: "pending" },
    { id: "step-6", description: "STEP 6: FORGE Brief 2 - Authority Brief", status: "pending" },
    { id: "step-7", description: "STEP 7: FORGE Brief 3 - Memetic Brief", status: "pending" },
    { id: "step-8", description: "STEP 8: FORGE Brief 4 - Shadow Brief", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write wisdom_briefs.json", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

Load: upgraded prompt, SoC output, soul_values, tribe_profile, fresh brief, deep brief, vibe_comments.

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify adapted prompt + research exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Wisdom Forge SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read all inputs for fusion", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + forge rules", status: "pending" },
    { id: "step-5", description: "STEP 5: FORGE Brief 1 - Authenticity Brief", status: "pending" },
    { id: "step-6", description: "STEP 6: FORGE Brief 2 - Authority Brief", status: "pending" },
    { id: "step-7", description: "STEP 7: FORGE Brief 3 - Memetic Brief", status: "pending" },
    { id: "step-8", description: "STEP 8: FORGE Brief 4 - Shadow Brief", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write wisdom_briefs.json", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 4: INDOCTRINATE

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify adapted prompt + research exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Wisdom Forge SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read all inputs for fusion", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + forge rules", status: "in_progress" },
    { id: "step-5", description: "STEP 5: FORGE Brief 1 - Authenticity Brief", status: "pending" },
    { id: "step-6", description: "STEP 6: FORGE Brief 2 - Authority Brief", status: "pending" },
    { id: "step-7", description: "STEP 7: FORGE Brief 3 - Memetic Brief", status: "pending" },
    { id: "step-8", description: "STEP 8: FORGE Brief 4 - Shadow Brief", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write wisdom_briefs.json", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

**State the 10 Alchemy Principles** + Wisdom Forge rules:
1. "Each brief is 100-200 words max."
2. "Each brief must contain at least 1 verbatim SoC phrase."
3. "Each brief addresses a DIFFERENT dimension of script quality."
4. "Briefs are INSTRUCTIONS for Stage 3, not content themselves."

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify adapted prompt + research exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Wisdom Forge SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read all inputs for fusion", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + forge rules", status: "completed" },
    { id: "step-5", description: "STEP 5: FORGE Brief 1 - Authenticity Brief", status: "pending" },
    { id: "step-6", description: "STEP 6: FORGE Brief 2 - Authority Brief", status: "pending" },
    { id: "step-7", description: "STEP 7: FORGE Brief 3 - Memetic Brief", status: "pending" },
    { id: "step-8", description: "STEP 8: FORGE Brief 4 - Shadow Brief", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write wisdom_briefs.json", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 5: FORGE Brief 1 — Authenticity Brief

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify adapted prompt + research exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Wisdom Forge SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read all inputs for fusion", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + forge rules", status: "completed" },
    { id: "step-5", description: "STEP 5: FORGE Brief 1 - Authenticity Brief", status: "in_progress" },
    { id: "step-6", description: "STEP 6: FORGE Brief 2 - Authority Brief", status: "pending" },
    { id: "step-7", description: "STEP 7: FORGE Brief 3 - Memetic Brief", status: "pending" },
    { id: "step-8", description: "STEP 8: FORGE Brief 4 - Shadow Brief", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write wisdom_briefs.json", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

**Focus:** Voice fidelity + vulnerability move. Sources: SoC output, Q1-Q4, soul_values. Must include the three-part vulnerability move (FELT → DID → RESULTS). 100-200 words.

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify adapted prompt + research exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Wisdom Forge SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read all inputs for fusion", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + forge rules", status: "completed" },
    { id: "step-5", description: "STEP 5: FORGE Brief 1 - Authenticity Brief", status: "completed" },
    { id: "step-6", description: "STEP 6: FORGE Brief 2 - Authority Brief", status: "pending" },
    { id: "step-7", description: "STEP 7: FORGE Brief 3 - Memetic Brief", status: "pending" },
    { id: "step-8", description: "STEP 8: FORGE Brief 4 - Shadow Brief", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write wisdom_briefs.json", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 6: FORGE Brief 2 — Authority Brief

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify adapted prompt + research exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Wisdom Forge SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read all inputs for fusion", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + forge rules", status: "completed" },
    { id: "step-5", description: "STEP 5: FORGE Brief 1 - Authenticity Brief", status: "completed" },
    { id: "step-6", description: "STEP 6: FORGE Brief 2 - Authority Brief", status: "in_progress" },
    { id: "step-7", description: "STEP 7: FORGE Brief 3 - Memetic Brief", status: "pending" },
    { id: "step-8", description: "STEP 8: FORGE Brief 4 - Shadow Brief", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write wisdom_briefs.json", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

**Focus:** ONE decisive claim + research evidence. Sources: Deep brief, Q6-Q7, fresh brief. Must contain specific data with source attribution. 100-200 words.

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify adapted prompt + research exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Wisdom Forge SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read all inputs for fusion", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + forge rules", status: "completed" },
    { id: "step-5", description: "STEP 5: FORGE Brief 1 - Authenticity Brief", status: "completed" },
    { id: "step-6", description: "STEP 6: FORGE Brief 2 - Authority Brief", status: "completed" },
    { id: "step-7", description: "STEP 7: FORGE Brief 3 - Memetic Brief", status: "pending" },
    { id: "step-8", description: "STEP 8: FORGE Brief 4 - Shadow Brief", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write wisdom_briefs.json", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 7: FORGE Brief 3 — Memetic Brief

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify adapted prompt + research exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Wisdom Forge SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read all inputs for fusion", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + forge rules", status: "completed" },
    { id: "step-5", description: "STEP 5: FORGE Brief 1 - Authenticity Brief", status: "completed" },
    { id: "step-6", description: "STEP 6: FORGE Brief 2 - Authority Brief", status: "completed" },
    { id: "step-7", description: "STEP 7: FORGE Brief 3 - Memetic Brief", status: "in_progress" },
    { id: "step-8", description: "STEP 8: FORGE Brief 4 - Shadow Brief", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write wisdom_briefs.json", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

**Focus:** Hook + shareable structure + tribal language. Sources: Vibe comments, Q5 + Q9, tribe_profile. Must include a hook strategy + tribal phrases. 100-200 words.

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify adapted prompt + research exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Wisdom Forge SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read all inputs for fusion", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + forge rules", status: "completed" },
    { id: "step-5", description: "STEP 5: FORGE Brief 1 - Authenticity Brief", status: "completed" },
    { id: "step-6", description: "STEP 6: FORGE Brief 2 - Authority Brief", status: "completed" },
    { id: "step-7", description: "STEP 7: FORGE Brief 3 - Memetic Brief", status: "completed" },
    { id: "step-8", description: "STEP 8: FORGE Brief 4 - Shadow Brief", status: "pending" },
    { id: "step-9", description: "STEP 9: EMIT - Write wisdom_briefs.json", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 8: FORGE Brief 4 — Shadow Brief

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify adapted prompt + research exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Wisdom Forge SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read all inputs for fusion", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + forge rules", status: "completed" },
    { id: "step-5", description: "STEP 5: FORGE Brief 1 - Authenticity Brief", status: "completed" },
    { id: "step-6", description: "STEP 6: FORGE Brief 2 - Authority Brief", status: "completed" },
    { id: "step-7", description: "STEP 7: FORGE Brief 3 - Memetic Brief", status: "completed" },
    { id: "step-8", description: "STEP 8: FORGE Brief 4 - Shadow Brief", status: "in_progress" },
    { id: "step-9", description: "STEP 9: EMIT - Write wisdom_briefs.json", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

**Focus:** Complexity, nuance, what-could-go-wrong. Sources: Q10, deep brief contrarian angle, tribe_profile objections. Must honor Alchemy P9 (acknowledge complexity). 100-200 words.

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify adapted prompt + research exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Wisdom Forge SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read all inputs for fusion", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + forge rules", status: "completed" },
    { id: "step-5", description: "STEP 5: FORGE Brief 1 - Authenticity Brief", status: "completed" },
    { id: "step-6", description: "STEP 6: FORGE Brief 2 - Authority Brief", status: "completed" },
    { id: "step-7", description: "STEP 7: FORGE Brief 3 - Memetic Brief", status: "completed" },
    { id: "step-8", description: "STEP 8: FORGE Brief 4 - Shadow Brief", status: "completed" },
    { id: "step-9", description: "STEP 9: EMIT - Write wisdom_briefs.json", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 9: EMIT

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify adapted prompt + research exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Wisdom Forge SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read all inputs for fusion", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + forge rules", status: "completed" },
    { id: "step-5", description: "STEP 5: FORGE Brief 1 - Authenticity Brief", status: "completed" },
    { id: "step-6", description: "STEP 6: FORGE Brief 2 - Authority Brief", status: "completed" },
    { id: "step-7", description: "STEP 7: FORGE Brief 3 - Memetic Brief", status: "completed" },
    { id: "step-8", description: "STEP 8: FORGE Brief 4 - Shadow Brief", status: "completed" },
    { id: "step-9", description: "STEP 9: EMIT - Write wisdom_briefs.json", status: "in_progress" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

**CREATE FILE:** `output/batches/batch_001/wisdom/{blueprint_id}_wisdom_briefs.json`

Schema: 4 briefs (authenticity, authority, memetic, shadow), each with `brief_text`, `word_count`, `soc_phrases_used[]`, `alchemy_principles_addressed[]`.

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify adapted prompt + research exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Wisdom Forge SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read all inputs for fusion", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + forge rules", status: "completed" },
    { id: "step-5", description: "STEP 5: FORGE Brief 1 - Authenticity Brief", status: "completed" },
    { id: "step-6", description: "STEP 6: FORGE Brief 2 - Authority Brief", status: "completed" },
    { id: "step-7", description: "STEP 7: FORGE Brief 3 - Memetic Brief", status: "completed" },
    { id: "step-8", description: "STEP 8: FORGE Brief 4 - Shadow Brief", status: "completed" },
    { id: "step-9", description: "STEP 9: EMIT - Write wisdom_briefs.json", status: "completed" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 10: CHECKPOINT

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify adapted prompt + research exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Wisdom Forge SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read all inputs for fusion", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + forge rules", status: "completed" },
    { id: "step-5", description: "STEP 5: FORGE Brief 1 - Authenticity Brief", status: "completed" },
    { id: "step-6", description: "STEP 6: FORGE Brief 2 - Authority Brief", status: "completed" },
    { id: "step-7", description: "STEP 7: FORGE Brief 3 - Memetic Brief", status: "completed" },
    { id: "step-8", description: "STEP 8: FORGE Brief 4 - Shadow Brief", status: "completed" },
    { id: "step-9", description: "STEP 9: EMIT - Write wisdom_briefs.json", status: "completed" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "in_progress" }
] });
```

Update `config.yaml`: `sessions.production.{blueprint_id}.wisdom.status = "complete"`

**OUTPUT:**
```
✅ WISDOM FORGE COMPLETE ({blueprint_id})
- Briefs: 4/4 generated
- Word counts: Auth {N}, Authority {N}, Memetic {N}, Shadow {N}
- NEXT: /ccf-generate {client_name} --blueprint {blueprint_id}
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify adapted prompt + research exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Wisdom Forge SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD CONTEXT - Read all inputs for fusion", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + forge rules", status: "completed" },
    { id: "step-5", description: "STEP 5: FORGE Brief 1 - Authenticity Brief", status: "completed" },
    { id: "step-6", description: "STEP 6: FORGE Brief 2 - Authority Brief", status: "completed" },
    { id: "step-7", description: "STEP 7: FORGE Brief 3 - Memetic Brief", status: "completed" },
    { id: "step-8", description: "STEP 8: FORGE Brief 4 - Shadow Brief", status: "completed" },
    { id: "step-9", description: "STEP 9: EMIT - Write wisdom_briefs.json", status: "completed" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Update config.yaml", status: "completed" }
] });
```

---

## 🔗 NEXT: `/ccf-generate {client_name} --blueprint {blueprint_id}`
