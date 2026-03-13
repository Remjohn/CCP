---
name: ccf-tribe-extract
description: Extract audience tribe profile from community data and social signals
---

# /ccf-tribe-extract {client_name}

// turbo-all

> **SKILLS_BASE:** `ccf-26/skills/ccf/`
> **SKILL:** `setup/tribe-soul-extraction/SKILL.md`

**Objective:** Analyze audience data to produce `tribe_profile.json` — the psychological map of the coach's tribe.

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul extraction complete", status: "pending" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Tribe Soul Extraction SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: INGEST - Load audience data and social signals", status: "pending" },
    { id: "step-4", description: "STEP 4: REASON - Execute tribe mapping across 12 dimensions", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write tribe_profile.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Dimension completeness + tribe specificity", status: "pending" },
    { id: "step-7", description: "STEP 7: H9/H11 DISTILLATION GATE - Run tribe-distiller", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "pending" }
  ]
});
```

**DO NOT PROCEED until you have called `write_todos` above.**

---

## 📋 Step Execution Protocol (MANDATORY)

> [!CAUTION]
> **You MUST call `write_todos` at EVERY step transition.**
> This is not optional. Skipping todo updates = workflow failure.

**For EACH step, follow this pattern:**

1. **START STEP:** Update todo status to `in_progress`
2. **EXECUTE:** Perform the step actions
3. **VALIDATE:** Verify outputs exist
4. **COMPLETE STEP:** Update todo status to `completed`

---

## STEP 1: PRE-FLIGHT

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul extraction complete", status: "in_progress" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Tribe Soul Extraction SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: INGEST - Load audience data and social signals", status: "pending" },
    { id: "step-4", description: "STEP 4: REASON - Execute tribe mapping across 12 dimensions", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write tribe_profile.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Dimension completeness + tribe specificity", status: "pending" },
    { id: "step-7", description: "STEP 7: H9/H11 DISTILLATION GATE - Run tribe-distiller", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "pending" }
  ]
});
```

**ACTIONS:**

| Check | Path | If Missing |
|-------|------|------------|
| 1 | `config.yaml → sessions.setup.soul_extract.status == "complete"` | STOP → Run `/ccf-soul-extract` first |
| 2 | `intelligence/soul/soul_values.json` | STOP → Run `/ccf-soul-extract` first |
| 3 | `raw/audience/` (≥1 file) | WARN → Will infer tribe from soul_values + business materials |

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul extraction complete", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Tribe Soul Extraction SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: INGEST - Load audience data and social signals", status: "pending" },
    { id: "step-4", description: "STEP 4: REASON - Execute tribe mapping across 12 dimensions", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write tribe_profile.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Dimension completeness + tribe specificity", status: "pending" },
    { id: "step-7", description: "STEP 7: H9/H11 DISTILLATION GATE - Run tribe-distiller", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "pending" }
  ]
});
```

---

## STEP 2: LOAD SKILL

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul extraction complete", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Tribe Soul Extraction SKILL.md", status: "in_progress" },
    { id: "step-3", description: "STEP 3: INGEST - Load audience data and social signals", status: "pending" },
    { id: "step-4", description: "STEP 4: REASON - Execute tribe mapping across 12 dimensions", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write tribe_profile.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Dimension completeness + tribe specificity", status: "pending" },
    { id: "step-7", description: "STEP 7: H9/H11 DISTILLATION GATE - Run tribe-distiller", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "pending" }
  ]
});
```

**ACTIONS:**

1. Read: `ccf-26/skills/ccf/setup/tribe-soul-extraction/SKILL.md`
2. Also read: `ccf-26/skills/ccf/setup/audience-empathy/SKILL.md` (supplementary)
3. Load `soul_values.json` — tribe must resonate with coach's soul

> [!IMPORTANT]
> **CONSTRAINT:** The tribe profile must be calibrated against the coach's soul values. A tribe that doesn't resonate with the coach is misidentified.

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul extraction complete", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Tribe Soul Extraction SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load audience data and social signals", status: "pending" },
    { id: "step-4", description: "STEP 4: REASON - Execute tribe mapping across 12 dimensions", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write tribe_profile.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Dimension completeness + tribe specificity", status: "pending" },
    { id: "step-7", description: "STEP 7: H9/H11 DISTILLATION GATE - Run tribe-distiller", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "pending" }
  ]
});
```

---

## STEP 3: INGEST (I-R-E-V-C Phase I)

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul extraction complete", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Tribe Soul Extraction SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load audience data and social signals", status: "in_progress" },
    { id: "step-4", description: "STEP 4: REASON - Execute tribe mapping across 12 dimensions", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write tribe_profile.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Dimension completeness + tribe specificity", status: "pending" },
    { id: "step-7", description: "STEP 7: H9/H11 DISTILLATION GATE - Run tribe-distiller", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "pending" }
  ]
});
```

**ACTIONS:**

1. Load all audience data from `raw/audience/`:
   - Reddit threads (highest priority — unfiltered tribal language)
   - YouTube comments, Instagram/TikTok comments, email testimonials
2. Load `soul_values.json` for cross-reference
3. Report: "Loaded {N} audience data files, {X} total comments/threads"

> [!NOTE]
> **Context Window Guard:** If audience data exceeds 60,000 words, prioritize Reddit threads and YouTube comments. Log excluded sources.

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul extraction complete", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Tribe Soul Extraction SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load audience data and social signals", status: "completed" },
    { id: "step-4", description: "STEP 4: REASON - Execute tribe mapping across 12 dimensions", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write tribe_profile.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Dimension completeness + tribe specificity", status: "pending" },
    { id: "step-7", description: "STEP 7: H9/H11 DISTILLATION GATE - Run tribe-distiller", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "pending" }
  ]
});
```

---

## STEP 4: REASON (I-R-E-V-C Phase R)

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul extraction complete", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Tribe Soul Extraction SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load audience data and social signals", status: "completed" },
    { id: "step-4", description: "STEP 4: REASON - Execute tribe mapping across 12 dimensions", status: "in_progress" },
    { id: "step-5", description: "STEP 5: EMIT - Write tribe_profile.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Dimension completeness + tribe specificity", status: "pending" },
    { id: "step-7", description: "STEP 7: H9/H11 DISTILLATION GATE - Run tribe-distiller", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "pending" }
  ]
});
```

**Map ALL 12 Context Premise dimensions:**

| # | Dimension | What to Extract |
|---|-----------|----------------|
| 1 | Frustrations | Daily irritants (verbatim quotes) |
| 2 | Wants | Superficial desires articulated openly |
| 3 | Dreams | Deep, unvoiced aspirations |
| 4 | Fears | Paralyzing anxieties |
| 5 | Suspicions | Doubts about industry/self |
| 6 | Insecurities | "Not enough" narratives |
| 7 | Envy | Jealousy pointing to desires |
| 8 | Enemies | External forces they oppose |
| 9 | Coping Mechanisms | How they avoid pain |
| 10 | Hidden Beliefs | Limiting assumptions as facts |
| 11 | Emotional Triggers | Words that bypass logic |
| 12 | Success Markers | What "making it" looks like |

**Additionally extract:** tribe slang, shared heroes, common enemies, humor style, platform behavior, transformation stories.

> [!CAUTION]
> **CONSTRAINT:** All tribe data must use VERBATIM quotes. Do NOT rephrase or sanitize community language.

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul extraction complete", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Tribe Soul Extraction SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load audience data and social signals", status: "completed" },
    { id: "step-4", description: "STEP 4: REASON - Execute tribe mapping across 12 dimensions", status: "completed" },
    { id: "step-5", description: "STEP 5: EMIT - Write tribe_profile.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Dimension completeness + tribe specificity", status: "pending" },
    { id: "step-7", description: "STEP 7: H9/H11 DISTILLATION GATE - Run tribe-distiller", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "pending" }
  ]
});
```

---

## STEP 5: EMIT (I-R-E-V-C Phase E)

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul extraction complete", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Tribe Soul Extraction SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load audience data and social signals", status: "completed" },
    { id: "step-4", description: "STEP 4: REASON - Execute tribe mapping across 12 dimensions", status: "completed" },
    { id: "step-5", description: "STEP 5: EMIT - Write tribe_profile.json", status: "in_progress" },
    { id: "step-6", description: "STEP 6: VALIDATE - Dimension completeness + tribe specificity", status: "pending" },
    { id: "step-7", description: "STEP 7: H9/H11 DISTILLATION GATE - Run tribe-distiller", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "pending" }
  ]
});
```

**CREATE FILE:** `intelligence/tribe/tribe_profile.json`

Schema must include:
- `demographic_sketch` — 2-3 sentences describing the typical tribe member
- `context_premise_dimensions` — all 12 dimensions each with `primary` (verbatim), `secondary` (verbatim), `pattern` (summary)
- `cultural_artifacts` — `tribe_slang[]`, `shared_heroes[]`, `common_enemies[]`, `humor_style`, `platform_behavior`
- `transformation_stories[]` — before/after with source
- `coach_tribe_resonance` — strongest alignment, potential friction with soul_values

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul extraction complete", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Tribe Soul Extraction SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load audience data and social signals", status: "completed" },
    { id: "step-4", description: "STEP 4: REASON - Execute tribe mapping across 12 dimensions", status: "completed" },
    { id: "step-5", description: "STEP 5: EMIT - Write tribe_profile.json", status: "completed" },
    { id: "step-6", description: "STEP 6: VALIDATE - Dimension completeness + tribe specificity", status: "pending" },
    { id: "step-7", description: "STEP 7: H9/H11 DISTILLATION GATE - Run tribe-distiller", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "pending" }
  ]
});
```

---

## STEP 6: VALIDATE (I-R-E-V-C Phase V)

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul extraction complete", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Tribe Soul Extraction SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load audience data and social signals", status: "completed" },
    { id: "step-4", description: "STEP 4: REASON - Execute tribe mapping across 12 dimensions", status: "completed" },
    { id: "step-5", description: "STEP 5: EMIT - Write tribe_profile.json", status: "completed" },
    { id: "step-6", description: "STEP 6: VALIDATE - Dimension completeness + tribe specificity", status: "in_progress" },
    { id: "step-7", description: "STEP 7: H9/H11 DISTILLATION GATE - Run tribe-distiller", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "pending" }
  ]
});
```

| # | Gate | Requirement | If Fail |
|---|------|-------------|---------|
| 1 | JSON valid | Parses without error | FIX syntax |
| 2 | Dimensions | ≥8 of 12 mapped with verbatim quotes | Extract more |
| 3 | Cultural artifacts | Slang ≥3, heroes ≥1, enemies ≥1 | Dig deeper |
| 4 | Verbatim check | Primary quotes exact copies from source | Replace paraphrased |
| 5 | Coach resonance | References soul_values.json | Cross-reference |
| 6 | No AI artifacts | Zero "leverage", "optimize", "moreover" | Replace |
| 7 | Specificity | Not generic — specific to THIS tribe | Add cultural detail |

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul extraction complete", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Tribe Soul Extraction SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load audience data and social signals", status: "completed" },
    { id: "step-4", description: "STEP 4: REASON - Execute tribe mapping across 12 dimensions", status: "completed" },
    { id: "step-5", description: "STEP 5: EMIT - Write tribe_profile.json", status: "completed" },
    { id: "step-6", description: "STEP 6: VALIDATE - Dimension completeness + tribe specificity", status: "completed" },
    { id: "step-7", description: "STEP 7: H9/H11 DISTILLATION GATE - Run tribe-distiller", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "pending" }
  ]
});
```

---


---

## STEP 7: H9/H11 DISTILLATION GATE

Mark step-7 `in_progress`.

> [!CAUTION]
> **MANDATORY GATE — Pipeline blocks if this fails.**

1. Read FULL: `ccf-26/skills/ccf/distillation/tribe-distiller/SKILL.md`
2. Execute 4-Phase Audit on `tribe_profile.json`:
   - Law 1: Verbatim Artifacts Audit
   - Law 2: "Not Us" Boundary Audit
   - Law 3: Pain-to-Mode Mapping Audit
   - Law 4: Tribal Authenticity Gate
3. **CREATE FILE:** `intelligence/tribe/H9_DISTILLATION_RECEIPT.md`

**IF FAIL:** Return to STEP 4 (REASON) — re-execute extraction focusing on specific evidence gaps from receipt.
**IF PASS:** Continue to STEP 8.

Mark step-7 `completed`.


## STEP 8: CHECKPOINT (I-R-E-V-C Phase C)

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul extraction complete", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Tribe Soul Extraction SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load audience data and social signals", status: "completed" },
    { id: "step-4", description: "STEP 4: REASON - Execute tribe mapping across 12 dimensions", status: "completed" },
    { id: "step-5", description: "STEP 5: EMIT - Write tribe_profile.json", status: "completed" },
    { id: "step-6", description: "STEP 6: VALIDATE - Dimension completeness + tribe specificity", status: "completed" },
    { id: "step-7", description: "STEP 7: H9/H11 DISTILLATION GATE - Run tribe-distiller", status: "completed" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "in_progress" }
  ]
});
```

Update `config.yaml`: `sessions.setup.tribe_extract.status = "complete"`

**OUTPUT:**
```
✅ TRIBE EXTRACTION COMPLETE
- Dimensions: {N}/12 mapped
- Cultural artifacts: {N} slang, {N} heroes, {N} enemies
- File: tribe_profile.json
- NEXT: /ccf-theme-discover {client_name}
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul extraction complete", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Tribe Soul Extraction SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load audience data and social signals", status: "completed" },
    { id: "step-4", description: "STEP 4: REASON - Execute tribe mapping across 12 dimensions", status: "completed" },
    { id: "step-5", description: "STEP 5: EMIT - Write tribe_profile.json", status: "completed" },
    { id: "step-6", description: "STEP 6: VALIDATE - Dimension completeness + tribe specificity", status: "completed" },
    { id: "step-7", description: "STEP 7: H9/H11 DISTILLATION GATE - Run tribe-distiller", status: "completed" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "completed" }
  ]
});
```

---

## 🔗 NEXT: `/ccf-theme-discover {client_name}`
