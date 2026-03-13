---
name: ccf-generate
description: "Stage 3: Script Generation — Precision execution of pre-decided strategy"
---

# /ccf-generate {client_name} --blueprint {blueprint_id}

// turbo-all

> **SKILLS_BASE:** `ccf-26/skills/ccf/`
> **SKILL:** `production/script-generator/SKILL.md`
> **STAGE:** 3 of 4 (Precision Execution)
> **TEMPERATURE:** 0.3

**Objective:** Generate the final script by applying structure + voice to the wisdom briefs. Stage 3 ONLY applies structure — NO new reasoning, NO new insights. All cognitive work was completed upstream.

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify wisdom briefs + upgraded prompt", status: "pending" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Generator SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: LOAD ARCHETYPE - Read specific archetype prompt", status: "pending" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + generation rules", status: "pending" },
    { id: "step-5", description: "STEP 5: EXECUTE - Generate script (Hook → Body → CTA)", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write generated_script.md + reasoning_log.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Red Flags + Humanity + Turing + word count", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
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
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify wisdom briefs + upgraded prompt", status: "in_progress" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Generator SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: LOAD ARCHETYPE - Read specific archetype prompt", status: "pending" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + generation rules", status: "pending" },
    { id: "step-5", description: "STEP 5: EXECUTE - Generate script (Hook → Body → CTA)", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write generated_script.md + reasoning_log.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Red Flags + Humanity + Turing + word count", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

| Check | Path | If Missing |
|-------|------|------------|
| 1 | `output/batches/batch_001/wisdom/{blueprint_id}_wisdom_briefs.json` | STOP → Run `/ccf-wisdom` |
| 2 | `output/batches/batch_001/adapted/{blueprint_id}_upgraded_prompt.md` | STOP → Run `/ccf-adapt` |
| 3 | `output/batches/batch_001/soc/{blueprint_id}_soc_output.json` | STOP → Run `/ccf-soc` |
| 4 | `intelligence/soul/soul_values.json` | STOP → Run `/ccf-soul-extract` |

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify wisdom briefs + upgraded prompt", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Generator SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: LOAD ARCHETYPE - Read specific archetype prompt", status: "pending" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + generation rules", status: "pending" },
    { id: "step-5", description: "STEP 5: EXECUTE - Generate script (Hook → Body → CTA)", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write generated_script.md + reasoning_log.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Red Flags + Humanity + Turing + word count", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 2: LOAD SKILL

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify wisdom briefs + upgraded prompt", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Generator SKILL.md", status: "in_progress" },
    { id: "step-3", description: "STEP 3: LOAD ARCHETYPE - Read specific archetype prompt", status: "pending" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + generation rules", status: "pending" },
    { id: "step-5", description: "STEP 5: EXECUTE - Generate script (Hook → Body → CTA)", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write generated_script.md + reasoning_log.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Red Flags + Humanity + Turing + word count", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

1. Read: `ccf-26/skills/ccf/production/script-generator/SKILL.md`

> [!CAUTION]
> **CRITICAL RULE:** Stage 3 is EXECUTION ONLY. The script generator must NOT:
> - Derive new insights (that was Stage 2.5)
> - Create new strategies (that was Stage 2)
> - Generate new voice material (that was Stage 1)
>
> It ONLY applies the archetype's structural template to the pre-decided content from Stages 1-2.5.

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify wisdom briefs + upgraded prompt", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Generator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD ARCHETYPE - Read specific archetype prompt", status: "pending" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + generation rules", status: "pending" },
    { id: "step-5", description: "STEP 5: EXECUTE - Generate script (Hook → Body → CTA)", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write generated_script.md + reasoning_log.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Red Flags + Humanity + Turing + word count", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 3: LOAD ARCHETYPE

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify wisdom briefs + upgraded prompt", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Generator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD ARCHETYPE - Read specific archetype prompt", status: "in_progress" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + generation rules", status: "pending" },
    { id: "step-5", description: "STEP 5: EXECUTE - Generate script (Hook → Body → CTA)", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write generated_script.md + reasoning_log.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Red Flags + Humanity + Turing + word count", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

1. Read the blueprint's assigned archetype from `content_blueprints.json`
2. Load the corresponding archetype prompt from `ccf-26/Script Prompts/`
3. Apply any modifications from the Mirror Session's Q13 (Template Choice)

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify wisdom briefs + upgraded prompt", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Generator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD ARCHETYPE - Read specific archetype prompt", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + generation rules", status: "pending" },
    { id: "step-5", description: "STEP 5: EXECUTE - Generate script (Hook → Body → CTA)", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write generated_script.md + reasoning_log.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Red Flags + Humanity + Turing + word count", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 4: INDOCTRINATE

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify wisdom briefs + upgraded prompt", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Generator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD ARCHETYPE - Read specific archetype prompt", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + generation rules", status: "in_progress" },
    { id: "step-5", description: "STEP 5: EXECUTE - Generate script (Hook → Body → CTA)", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write generated_script.md + reasoning_log.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Red Flags + Humanity + Turing + word count", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

**State the 10 Alchemy Principles** + Stage 3 execution rules:
1. "I will ONLY apply structure to pre-existing content."
2. "I will NOT create new insights, strategies, or voice material."
3. "All wisdom brief content will be preserved, not rewritten."
4. "SoC-preserved phrases (from Q14) will appear verbatim."
5. "Vulnerability move will appear at the structural position specified in Q8."

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify wisdom briefs + upgraded prompt", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Generator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD ARCHETYPE - Read specific archetype prompt", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + generation rules", status: "completed" },
    { id: "step-5", description: "STEP 5: EXECUTE - Generate script (Hook → Body → CTA)", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write generated_script.md + reasoning_log.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Red Flags + Humanity + Turing + word count", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 5: EXECUTE

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify wisdom briefs + upgraded prompt", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Generator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD ARCHETYPE - Read specific archetype prompt", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + generation rules", status: "completed" },
    { id: "step-5", description: "STEP 5: EXECUTE - Generate script (Hook → Body → CTA)", status: "in_progress" },
    { id: "step-6", description: "STEP 6: EMIT - Write generated_script.md + reasoning_log.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Red Flags + Humanity + Turing + word count", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

**Generate the script using the archetype structure:**

- **Hook (15-20 words):** Source Q5 + SoC hook examples + fresh research urgency. Must create Information Gap (P3).
- **Body (80-120 words):** Source all 4 wisdom briefs + SoC body + Q7. Vulnerability at Q8 position. ONE decisive claim (P2). Shadow nuance (P9).
- **CTA (15-25 words):** Source upgraded_prompt + SoC CTA + tribe connection. Natural conclusion, NOT marketing.

**Word Count Target: 120-180 words total**

> [!CAUTION]
> **PRESERVATION RULE:** Q14 SoC phrases MUST appear verbatim in the final script.

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify wisdom briefs + upgraded prompt", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Generator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD ARCHETYPE - Read specific archetype prompt", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + generation rules", status: "completed" },
    { id: "step-5", description: "STEP 5: EXECUTE - Generate script (Hook → Body → CTA)", status: "completed" },
    { id: "step-6", description: "STEP 6: EMIT - Write generated_script.md + reasoning_log.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Red Flags + Humanity + Turing + word count", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 6: EMIT

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify wisdom briefs + upgraded prompt", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Generator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD ARCHETYPE - Read specific archetype prompt", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + generation rules", status: "completed" },
    { id: "step-5", description: "STEP 5: EXECUTE - Generate script (Hook → Body → CTA)", status: "completed" },
    { id: "step-6", description: "STEP 6: EMIT - Write generated_script.md + reasoning_log.json", status: "in_progress" },
    { id: "step-7", description: "STEP 7: VALIDATE - Red Flags + Humanity + Turing + word count", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

**CREATE FILE 1:** `output/batches/batch_001/scripts/{blueprint_id}_generated_script.md`
**CREATE FILE 2:** `output/batches/batch_001/scripts/{blueprint_id}_reasoning_log.json`

Reasoning log includes: sources used, SoC phrases, vulnerability move details, alchemy checklist (all 10 principles).

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify wisdom briefs + upgraded prompt", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Generator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD ARCHETYPE - Read specific archetype prompt", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + generation rules", status: "completed" },
    { id: "step-5", description: "STEP 5: EXECUTE - Generate script (Hook → Body → CTA)", status: "completed" },
    { id: "step-6", description: "STEP 6: EMIT - Write generated_script.md + reasoning_log.json", status: "completed" },
    { id: "step-7", description: "STEP 7: VALIDATE - Red Flags + Humanity + Turing + word count", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 7: VALIDATE

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify wisdom briefs + upgraded prompt", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Generator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD ARCHETYPE - Read specific archetype prompt", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + generation rules", status: "completed" },
    { id: "step-5", description: "STEP 5: EXECUTE - Generate script (Hook → Body → CTA)", status: "completed" },
    { id: "step-6", description: "STEP 6: EMIT - Write generated_script.md + reasoning_log.json", status: "completed" },
    { id: "step-7", description: "STEP 7: VALIDATE - Red Flags + Humanity + Turing + word count", status: "in_progress" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

### Red Flags Check (Must score 0/10)

| Flag | Description | Detected? |
|------|-------------|-----------|
| RF1-RF10 | AI language, generic phrases, missing vulnerability, word count outside range | ❌ |

### Humanity Score (Must be ≥7/10)
### Turing Test (Must be 5/5)

### 4 Laws of Script Distillation (Must PASS all 4)

| Law | Test | Pass? |
|-----|------|-------|
| **L1: Depth Stratification** | Is the core insight at L2 (mechanism) or L3 (collision), NOT L1 (surface)? | |
| **L2: Temperature Dynamics** | Does the script contain ≥1 deliberate emotional temperature shift? | |
| **L3: Earned Reveal** | Is the "aha moment" EARNED through beats, not DECLARED with "here's what nobody tells you"? | |
| **L4: Specificity Gravity** | Is every sentence anchored to a specific finding, tribal reality, or coach belief? | |

> [!CAUTION]
> **HARD GATES:** Red Flags > 0 → REJECT and fix. Humanity < 7 → REJECT. Turing < 5 → REJECT. Any Law fails → REJECT. Word count outside 120-180 → REJECT.

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify wisdom briefs + upgraded prompt", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Generator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD ARCHETYPE - Read specific archetype prompt", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + generation rules", status: "completed" },
    { id: "step-5", description: "STEP 5: EXECUTE - Generate script (Hook → Body → CTA)", status: "completed" },
    { id: "step-6", description: "STEP 6: EMIT - Write generated_script.md + reasoning_log.json", status: "completed" },
    { id: "step-7", description: "STEP 7: VALIDATE - Red Flags + Humanity + Turing + word count", status: "completed" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 8: CHECKPOINT

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify wisdom briefs + upgraded prompt", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Generator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD ARCHETYPE - Read specific archetype prompt", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + generation rules", status: "completed" },
    { id: "step-5", description: "STEP 5: EXECUTE - Generate script (Hook → Body → CTA)", status: "completed" },
    { id: "step-6", description: "STEP 6: EMIT - Write generated_script.md + reasoning_log.json", status: "completed" },
    { id: "step-7", description: "STEP 7: VALIDATE - Red Flags + Humanity + Turing + word count", status: "completed" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "in_progress" }
] });
```

**OUTPUT:**
```
✅ SCRIPT GENERATED ({blueprint_id})
- Word count: {N} (120-180 target)
- Red Flags: 0/10
- Humanity: {N}/10
- Turing: {N}/5
- All 10 Alchemy Principles verified
- NEXT: /ccf-analyze {client_name} --blueprint {blueprint_id}
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify wisdom briefs + upgraded prompt", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Script Generator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD ARCHETYPE - Read specific archetype prompt", status: "completed" },
    { id: "step-4", description: "STEP 4: INDOCTRINATE - State Alchemy Principles + generation rules", status: "completed" },
    { id: "step-5", description: "STEP 5: EXECUTE - Generate script (Hook → Body → CTA)", status: "completed" },
    { id: "step-6", description: "STEP 6: EMIT - Write generated_script.md + reasoning_log.json", status: "completed" },
    { id: "step-7", description: "STEP 7: VALIDATE - Red Flags + Humanity + Turing + word count", status: "completed" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "completed" }
] });
```

---

## 🔗 NEXT: `/ccf-analyze {client_name} --blueprint {blueprint_id}`
