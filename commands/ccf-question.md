---
name: ccf-question
description: "Weekly Subsystem 2 — Generate 5-7 provocation questions from friction points"
---

# /ccf-question {client_name}

// turbo-all

> **SKILLS_BASE:** `ccf-26/skills/ccf/`
> **SKILL:** `content/question-engineer/SKILL.md`

**Objective:** Convert Intelligence Radar friction points into 5-7 provocation questions using 4 archetypes, matched to Coach triggers. Output: `provocation_questions.json`.

---

## 🎯 STEP 0: INITIALIZE TODOS

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify intelligence_radar.json exists", status: "pending" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Question Engineer SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: MAP - Match friction points to archetypes via trigger archive", status: "pending" },
    { id: "step-4", description: "STEP 4: GENERATE - Write 5-7 provocation questions", status: "pending" },
    { id: "step-5", description: "STEP 5: MIX - Validate archetype distribution", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write provocation_questions.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Quality gates on specificity + trigger mapping", status: "pending" },
    { id: "step-8", description: "STEP 8: H0 DISTILLATION GATE - Run question-distiller 4-Law audit", status: "pending" },
    { id: "step-9", description: "STEP 9: CHECKPOINT - Update config.yaml", status: "pending" }
  ]
});
```

---

## STEP 1: PRE-FLIGHT

Mark step-1 `in_progress`.

| Check | Path | If Missing |
|-------|------|------------|
| 1 | `intelligence/weekly/{week_id}/intelligence_radar.json` | STOP → Run `/ccf-radar` |
| 2 | `intelligence/project_context.json` | STOP → Run `/ccf-pillar-build` |

**Determine week_id** from the most recent `intelligence_radar.json`.

Mark step-1 `completed`.

---

## STEP 2: LOAD SKILL

Read FULL: `ccf-26/skills/ccf/content/question-engineer/SKILL.md`
Internalize: 4 archetypes, construction protocol, calibration rules, mix requirements.

---

## STEP 3: MAP — Friction Points to Archetypes

For each friction point in `intelligence_radar.json`:
1. Check `trigger_archive_match` field
2. Map to archetype (recurring_sermon→CONTRARIAN, origin_wound→VULNERABILITY, etc.)
3. Rank by potential reaction intensity
4. Select top 5-7 for question generation

---

## STEP 4: GENERATE — Write Questions

For each selected friction point:
1. Load the corresponding pillar's Layer 6 + Layer 7 data
2. Construct the question using the archetype template
3. Add video stimulus if available
4. Calibrate intensity based on market sophistication level

---

## STEP 5: MIX — Validate Distribution

| Archetype | Min | Max | Actual |
|-----------|:---:|:---:|:------:|
| Contrarian | 2 | 5 | |
| Vulnerability Probe | 1 | 2 | |
| Compassion Mirror | 1 | 2 | |
| Shadow Explorer | 0 | 1 | |

If mix is invalid → swap questions to meet requirements.

---

## STEP 6: EMIT

**CREATE FILE:** `intelligence/weekly/{week_id}/provocation_questions.json`

---

## STEP 7: VALIDATE

- [ ] 5-7 questions generated
- [ ] Archetype mix valid
- [ ] Each question references specific friction point
- [ ] No generic questions
- [ ] Each question has trigger_target from Layer 7

---

## STEP 8: H0 DISTILLATION GATE

Mark step-8 `in_progress`.

> [!CAUTION]
> **MANDATORY GATE — Pipeline blocks if this fails.**

1. Read FULL: `ccf-26/skills/ccf/distillation/question-distiller/SKILL.md`
2. Execute 4-Phase Audit on `provocation_questions.json`:
   - Law 1: Saturation Audit (3 checks)
   - Law 2: Mode Diversity Audit (T/V/R + archetype mix)
   - Law 3: Compression Audit (≥50% multi-mode)
   - Law 4: Unpredictability Gate Audit (4 checks per question)
3. **CREATE FILE:** `intelligence/weekly/{week_id}/H0_DISTILLATION_RECEIPT.md`

**IF FAIL:** Return to STEP 4 (GENERATE) — regenerate failing questions with specific remediation from receipt.
**IF PASS:** Continue to STEP 9.

Mark step-8 `completed`.

---

## STEP 9: CHECKPOINT

```
✅ QUESTION ENGINEER COMPLETE (Week {week_id})
- Questions: {N}
- Archetypes: {distribution}
- H0 Distillation Receipt: ✅ PASS
- NEXT: /ccf-elicit {client_name}
```

---

## 🔗 NEXT: `/ccf-elicit {client_name}`
