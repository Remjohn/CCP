---
name: ccf-blueprint
description: Generate content blueprints by fusing soul + tribe + themes + research
---

# /ccf-blueprint {client_name}

// turbo-all

> **SKILLS_BASE:** `ccf-26/skills/ccf/`
> **SKILL:** `research/blueprint-orchestrator/SKILL.md`

**Objective:** Fuse soul, tribe, themes, and research into 12 content blueprints, each mapped to a viral framework archetype.

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify ALL research outputs exist", status: "pending" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Blueprint Orchestrator SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: INGEST - Load all intelligence layers", status: "pending" },
    { id: "step-4", description: "STEP 4: FUSE - 3-Layer Fusion per blueprint", status: "pending" },
    { id: "step-5", description: "STEP 5: MAP - Assign viral framework archetype per blueprint", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_blueprints.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - 3-layer fusion completeness", status: "pending" },
    { id: "step-8", description: "STEP 8: H1 DISTILLATION GATE - Run blueprint-distiller 4-Law audit", status: "pending" },
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
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify ALL research outputs exist", status: "in_progress" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Blueprint Orchestrator SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: INGEST - Load all intelligence layers", status: "pending" },
    { id: "step-4", description: "STEP 4: FUSE - 3-Layer Fusion per blueprint", status: "pending" },
    { id: "step-5", description: "STEP 5: MAP - Assign viral framework archetype per blueprint", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_blueprints.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - 3-layer fusion completeness", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

| Check | Path | If Missing |
|-------|------|------------|
| 1 | `intelligence/soul/soul_values.json` | STOP → Run `/ccf-soul-extract` |
| 2 | `intelligence/tribe/tribe_profile.json` | STOP → Run `/ccf-tribe-extract` |
| 3 | `intelligence/themes/content_themes.json` | STOP → Run `/ccf-theme-discover` |
| 4 | `research/fresh/` (≥1 brief) | STOP → Run `/ccf-research-fresh` |
| 5 | `research/deep/` (≥1 brief) | STOP → Run `/ccf-research-deep` |

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify ALL research outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Blueprint Orchestrator SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: INGEST - Load all intelligence layers", status: "pending" },
    { id: "step-4", description: "STEP 4: FUSE - 3-Layer Fusion per blueprint", status: "pending" },
    { id: "step-5", description: "STEP 5: MAP - Assign viral framework archetype per blueprint", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_blueprints.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - 3-layer fusion completeness", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 2: LOAD SKILL

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify ALL research outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Blueprint Orchestrator SKILL.md", status: "in_progress" },
    { id: "step-3", description: "STEP 3: INGEST - Load all intelligence layers", status: "pending" },
    { id: "step-4", description: "STEP 4: FUSE - 3-Layer Fusion per blueprint", status: "pending" },
    { id: "step-5", description: "STEP 5: MAP - Assign viral framework archetype per blueprint", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_blueprints.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - 3-layer fusion completeness", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

1. Read: `ccf-26/skills/ccf/research/blueprint-orchestrator/SKILL.md`
2. Read: `ccf-26/skills/ccf/research/archetype-mapping/SKILL.md` (22 viral frameworks)

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify ALL research outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Blueprint Orchestrator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load all intelligence layers", status: "pending" },
    { id: "step-4", description: "STEP 4: FUSE - 3-Layer Fusion per blueprint", status: "pending" },
    { id: "step-5", description: "STEP 5: MAP - Assign viral framework archetype per blueprint", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_blueprints.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - 3-layer fusion completeness", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 3: INGEST

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify ALL research outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Blueprint Orchestrator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load all intelligence layers", status: "in_progress" },
    { id: "step-4", description: "STEP 4: FUSE - 3-Layer Fusion per blueprint", status: "pending" },
    { id: "step-5", description: "STEP 5: MAP - Assign viral framework archetype per blueprint", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_blueprints.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - 3-layer fusion completeness", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

Load ALL intelligence layers:
1. `soul_values.json` — coach voice DNA, TTT baseline
2. `tribe_profile.json` — 12 context premise dimensions
3. `content_themes.json` — 12 selected themes with archetypes
4. All `{theme_id}_fresh_brief.md` from `research/fresh/`
5. All `{theme_id}_deep_brief.md` from `research/deep/`

> [!CAUTION]
> **Context Window Guard:** Do NOT load all 24 briefs simultaneously. Process each blueprint sequentially, loading only the 2 briefs (fresh + deep) for the current theme.

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify ALL research outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Blueprint Orchestrator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load all intelligence layers", status: "completed" },
    { id: "step-4", description: "STEP 4: FUSE - 3-Layer Fusion per blueprint", status: "pending" },
    { id: "step-5", description: "STEP 5: MAP - Assign viral framework archetype per blueprint", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_blueprints.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - 3-layer fusion completeness", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 4: FUSE (3-Layer Fusion Protocol)

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify ALL research outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Blueprint Orchestrator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load all intelligence layers", status: "completed" },
    { id: "step-4", description: "STEP 4: FUSE - 3-Layer Fusion per blueprint", status: "in_progress" },
    { id: "step-5", description: "STEP 5: MAP - Assign viral framework archetype per blueprint", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_blueprints.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - 3-layer fusion completeness", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

> [!IMPORTANT]
> **The 3-Layer Fusion is the CCF's core IP.** Every blueprint must demonstrate the intersection of all three layers. A blueprint that skips any layer is REJECTED.

| Layer | Source | Contribution |
|-------|--------|-------------|
| **Author Soul** | `soul_values.json` | Voice DNA, values, TTT, perspective |
| **Tribe Soul** | `tribe_profile.json` | Dimensions, cultural artifacts, transformation |
| **Research** | Fresh + Deep briefs | Temporal urgency + timeless wisdom |

**Fusion output per blueprint:** `content_idea`, `fusion_statement`, `hook_direction`, `body_strategy`, `cta_direction`, `three_part_vulnerability_move` (FELT → DID → RESULTS).

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify ALL research outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Blueprint Orchestrator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load all intelligence layers", status: "completed" },
    { id: "step-4", description: "STEP 4: FUSE - 3-Layer Fusion per blueprint", status: "completed" },
    { id: "step-5", description: "STEP 5: MAP - Assign viral framework archetype per blueprint", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_blueprints.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - 3-layer fusion completeness", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 5: MAP (Archetype Assignment)

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify ALL research outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Blueprint Orchestrator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load all intelligence layers", status: "completed" },
    { id: "step-4", description: "STEP 4: FUSE - 3-Layer Fusion per blueprint", status: "completed" },
    { id: "step-5", description: "STEP 5: MAP - Assign viral framework archetype per blueprint", status: "in_progress" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_blueprints.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - 3-layer fusion completeness", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

For each blueprint, confirm or refine archetype from `content_themes.json`:
- Match against 22 viral frameworks
- Verify archetype FITS content (don't force mismatch)
- Load corresponding prompt from `ccf-26/Script Prompts/`

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify ALL research outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Blueprint Orchestrator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load all intelligence layers", status: "completed" },
    { id: "step-4", description: "STEP 4: FUSE - 3-Layer Fusion per blueprint", status: "completed" },
    { id: "step-5", description: "STEP 5: MAP - Assign viral framework archetype per blueprint", status: "completed" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_blueprints.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - 3-layer fusion completeness", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 6: EMIT

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify ALL research outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Blueprint Orchestrator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load all intelligence layers", status: "completed" },
    { id: "step-4", description: "STEP 4: FUSE - 3-Layer Fusion per blueprint", status: "completed" },
    { id: "step-5", description: "STEP 5: MAP - Assign viral framework archetype per blueprint", status: "completed" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_blueprints.json", status: "in_progress" },
    { id: "step-7", description: "STEP 7: VALIDATE - 3-layer fusion completeness", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

**CREATE FILE:** `output/batches/batch_001/blueprints/content_blueprints.json`

Schema per blueprint: `blueprint_id`, `theme_id`, `content_idea`, `archetype`, `ttt_assignment`, `fusion_statement`, `layers` (author_soul, tribe_soul, research_fusion), `hook_direction`, `body_strategy`, `cta_direction`, `three_part_vulnerability_move` (felt_it, did_it_anyway, results), `context_premise_dimensions_targeted`, `fresh_brief_ref`, `deep_brief_ref`.

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify ALL research outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Blueprint Orchestrator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load all intelligence layers", status: "completed" },
    { id: "step-4", description: "STEP 4: FUSE - 3-Layer Fusion per blueprint", status: "completed" },
    { id: "step-5", description: "STEP 5: MAP - Assign viral framework archetype per blueprint", status: "completed" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_blueprints.json", status: "completed" },
    { id: "step-7", description: "STEP 7: VALIDATE - 3-layer fusion completeness", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 7: VALIDATE

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify ALL research outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Blueprint Orchestrator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load all intelligence layers", status: "completed" },
    { id: "step-4", description: "STEP 4: FUSE - 3-Layer Fusion per blueprint", status: "completed" },
    { id: "step-5", description: "STEP 5: MAP - Assign viral framework archetype per blueprint", status: "completed" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_blueprints.json", status: "completed" },
    { id: "step-7", description: "STEP 7: VALIDATE - 3-layer fusion completeness", status: "in_progress" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

| # | Gate | Requirement | If Fail |
|---|------|-------------|---------|
| 1 | 12 blueprints | Exactly 12 in output | Generate missing |
| 2 | 3-layer fusion | EVERY blueprint has all 3 layers | Fill missing |
| 3 | Vulnerability move | EVERY blueprint has FELT/DID/RESULTS | Add (Alchemy P1) |
| 4 | Archetype fit | Each archetype fits content | Reassign |
| 5 | Specificity | content_idea is specific, not generic | Rewrite |
| 6 | Research refs | Both fresh and deep refs exist | Fix paths |
| 7 | TTT diversity | ≥4 different TTT levels across 12 | Recalibrate |
| 8 | JSON valid | Parses without error | Fix |

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify ALL research outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Blueprint Orchestrator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load all intelligence layers", status: "completed" },
    { id: "step-4", description: "STEP 4: FUSE - 3-Layer Fusion per blueprint", status: "completed" },
    { id: "step-5", description: "STEP 5: MAP - Assign viral framework archetype per blueprint", status: "completed" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_blueprints.json", status: "completed" },
    { id: "step-7", description: "STEP 7: VALIDATE - 3-layer fusion completeness", status: "completed" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 8: H1 DISTILLATION GATE

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify ALL research outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Blueprint Orchestrator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load all intelligence layers", status: "completed" },
    { id: "step-4", description: "STEP 4: FUSE - 3-Layer Fusion per blueprint", status: "completed" },
    { id: "step-5", description: "STEP 5: MAP - Assign viral framework archetype per blueprint", status: "completed" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_blueprints.json", status: "completed" },
    { id: "step-7", description: "STEP 7: VALIDATE - 3-layer fusion completeness", status: "completed" },
    { id: "step-8", description: "STEP 8: H1 DISTILLATION GATE - Run blueprint-distiller 4-Law audit", status: "in_progress" },
    { id: "step-9", description: "STEP 9: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

> [!CAUTION]
> **MANDATORY GATE — Pipeline blocks if this fails.**

1. Read FULL: `ccf-26/skills/ccf/distillation/blueprint-distiller/SKILL.md`
2. Execute 4-Phase Audit on `content_blueprints.json`:
   - Law 1: Narrative Saturation Audit (saturation sentence, coach+tribe+contradiction)
   - Law 2: Mode Classification Audit (mode_primary per blueprint, batch balance)
   - Law 3: Collapse Test Audit (≥10/12 collapse-resistant)
   - Law 4: Downstream Utility Audit (downstream_routing tags for SoC + Art Director)
3. **CREATE FILE:** `research/H1_DISTILLATION_RECEIPT.md`

**IF FAIL:** Return to STEP 4 (FUSE) — regenerate failing blueprints with specific remediation from receipt.
**IF PASS:** Continue to STEP 9.

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify ALL research outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Blueprint Orchestrator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load all intelligence layers", status: "completed" },
    { id: "step-4", description: "STEP 4: FUSE - 3-Layer Fusion per blueprint", status: "completed" },
    { id: "step-5", description: "STEP 5: MAP - Assign viral framework archetype per blueprint", status: "completed" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_blueprints.json", status: "completed" },
    { id: "step-7", description: "STEP 7: VALIDATE - 3-layer fusion completeness", status: "completed" },
    { id: "step-8", description: "STEP 8: H1 DISTILLATION GATE - Run blueprint-distiller 4-Law audit", status: "completed" },
    { id: "step-9", description: "STEP 9: CHECKPOINT - Update config.yaml", status: "pending" }
] });
```

---

## STEP 9: CHECKPOINT

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify ALL research outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Blueprint Orchestrator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load all intelligence layers", status: "completed" },
    { id: "step-4", description: "STEP 4: FUSE - 3-Layer Fusion per blueprint", status: "completed" },
    { id: "step-5", description: "STEP 5: MAP - Assign viral framework archetype per blueprint", status: "completed" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_blueprints.json", status: "completed" },
    { id: "step-7", description: "STEP 7: VALIDATE - 3-layer fusion completeness", status: "completed" },
    { id: "step-8", description: "STEP 8: H1 DISTILLATION GATE - Run blueprint-distiller 4-Law audit", status: "completed" },
    { id: "step-9", description: "STEP 9: CHECKPOINT - Update config.yaml", status: "in_progress" }
] });
```

Update `config.yaml`: `sessions.research.blueprint.status = "complete"`, `current_batch: "batch_001"`

**OUTPUT (25-35 words):**
```
✅ BLUEPRINT GENERATION COMPLETE
- Blueprints: 12 generated
- All with 3-layer fusion + vulnerability moves
- H1 Distillation Receipt: ✅ PASS
- NEXT: /ccf-vibe-comments {client_name}
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify ALL research outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Blueprint Orchestrator SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load all intelligence layers", status: "completed" },
    { id: "step-4", description: "STEP 4: FUSE - 3-Layer Fusion per blueprint", status: "completed" },
    { id: "step-5", description: "STEP 5: MAP - Assign viral framework archetype per blueprint", status: "completed" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_blueprints.json", status: "completed" },
    { id: "step-7", description: "STEP 7: VALIDATE - 3-layer fusion completeness", status: "completed" },
    { id: "step-8", description: "STEP 8: H1 DISTILLATION GATE - Run blueprint-distiller 4-Law audit", status: "completed" },
    { id: "step-9", description: "STEP 9: CHECKPOINT - Update config.yaml", status: "completed" }
] });
```

---

## 🔗 NEXT: `/ccf-vibe-comments {client_name}`
