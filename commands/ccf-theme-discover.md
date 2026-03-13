---
name: ccf-theme-discover
description: Discover and score 12 content themes from soul + tribe intersection
---

# /ccf-theme-discover {client_name}

// turbo-all

> **SKILLS_BASE:** `ccf-26/skills/ccf/`
> **SKILL:** `setup/theme-discovery/SKILL.md`

**Objective:** Discover 12 content themes by intersecting `soul_values.json` and `tribe_profile.json`, producing `content_themes.json`.

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul + tribe outputs exist", status: "pending" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Theme Discovery SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: INGEST - Load soul_values.json + tribe_profile.json", status: "pending" },
    { id: "step-4", description: "STEP 4: GENERATE - Score 36 theme candidates", status: "pending" },
    { id: "step-5", description: "STEP 5: SELECT - Pick top 12 themes with archetype mapping", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_themes.json + SETUP_COMPLETE.md", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Distribution + archetype coverage gates", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Mark setup_complete in config.yaml", status: "pending" }
  ]
});
```

**DO NOT PROCEED until you have called `write_todos` above.**

---

## 📋 Step Execution Protocol (MANDATORY)

> [!CAUTION]
> **You MUST call `write_todos` at EVERY step transition.**
> This is not optional. Skipping todo updates = workflow failure.

**For EACH step:** START → `in_progress` → Execute → Verify → `completed`

---

## STEP 1: PRE-FLIGHT

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul + tribe outputs exist", status: "in_progress" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Theme Discovery SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: INGEST - Load soul_values.json + tribe_profile.json", status: "pending" },
    { id: "step-4", description: "STEP 4: GENERATE - Score 36 theme candidates", status: "pending" },
    { id: "step-5", description: "STEP 5: SELECT - Pick top 12 themes with archetype mapping", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_themes.json + SETUP_COMPLETE.md", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Distribution + archetype coverage gates", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Mark setup_complete in config.yaml", status: "pending" }
] });
```

| Check | Path | If Missing |
|-------|------|------------|
| 1 | `config.yaml → sessions.setup.soul_extract.status == "complete"` | STOP → Run `/ccf-soul-extract` |
| 2 | `config.yaml → sessions.setup.tribe_extract.status == "complete"` | STOP → Run `/ccf-tribe-extract` |
| 3 | `intelligence/soul/soul_values.json` | STOP → Missing output |
| 4 | `intelligence/tribe/tribe_profile.json` | STOP → Missing output |

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul + tribe outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Theme Discovery SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: INGEST - Load soul_values.json + tribe_profile.json", status: "pending" },
    { id: "step-4", description: "STEP 4: GENERATE - Score 36 theme candidates", status: "pending" },
    { id: "step-5", description: "STEP 5: SELECT - Pick top 12 themes with archetype mapping", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_themes.json + SETUP_COMPLETE.md", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Distribution + archetype coverage gates", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Mark setup_complete in config.yaml", status: "pending" }
] });
```

---

## STEP 2: LOAD SKILL

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul + tribe outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Theme Discovery SKILL.md", status: "in_progress" },
    { id: "step-3", description: "STEP 3: INGEST - Load soul_values.json + tribe_profile.json", status: "pending" },
    { id: "step-4", description: "STEP 4: GENERATE - Score 36 theme candidates", status: "pending" },
    { id: "step-5", description: "STEP 5: SELECT - Pick top 12 themes with archetype mapping", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_themes.json + SETUP_COMPLETE.md", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Distribution + archetype coverage gates", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Mark setup_complete in config.yaml", status: "pending" }
] });
```

1. Read: `ccf-26/skills/ccf/setup/theme-discovery/SKILL.md`
2. Read: `ccf-26/skills/ccf/research/archetype-mapping/SKILL.md` (for archetype categories)

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul + tribe outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Theme Discovery SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load soul_values.json + tribe_profile.json", status: "pending" },
    { id: "step-4", description: "STEP 4: GENERATE - Score 36 theme candidates", status: "pending" },
    { id: "step-5", description: "STEP 5: SELECT - Pick top 12 themes with archetype mapping", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_themes.json + SETUP_COMPLETE.md", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Distribution + archetype coverage gates", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Mark setup_complete in config.yaml", status: "pending" }
] });
```

---

## STEP 3: INGEST

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul + tribe outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Theme Discovery SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load soul_values.json + tribe_profile.json", status: "in_progress" },
    { id: "step-4", description: "STEP 4: GENERATE - Score 36 theme candidates", status: "pending" },
    { id: "step-5", description: "STEP 5: SELECT - Pick top 12 themes with archetype mapping", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_themes.json + SETUP_COMPLETE.md", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Distribution + archetype coverage gates", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Mark setup_complete in config.yaml", status: "pending" }
] });
```

1. Parse `soul_values.json` — extract core values, TTT baseline, metaphor domains
2. Parse `tribe_profile.json` — extract all 12 context premise dimensions + cultural artifacts
3. Identify the **intersection zones** — where coach values meet tribe needs

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul + tribe outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Theme Discovery SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load soul_values.json + tribe_profile.json", status: "completed" },
    { id: "step-4", description: "STEP 4: GENERATE - Score 36 theme candidates", status: "pending" },
    { id: "step-5", description: "STEP 5: SELECT - Pick top 12 themes with archetype mapping", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_themes.json + SETUP_COMPLETE.md", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Distribution + archetype coverage gates", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Mark setup_complete in config.yaml", status: "pending" }
] });
```

---

## STEP 4: GENERATE

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul + tribe outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Theme Discovery SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load soul_values.json + tribe_profile.json", status: "completed" },
    { id: "step-4", description: "STEP 4: GENERATE - Score 36 theme candidates", status: "in_progress" },
    { id: "step-5", description: "STEP 5: SELECT - Pick top 12 themes with archetype mapping", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_themes.json + SETUP_COMPLETE.md", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Distribution + archetype coverage gates", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Mark setup_complete in config.yaml", status: "pending" }
] });
```

**Generate 36 theme candidates** (3× the final count) by crossing:
- Coach core values (4-6) × tribe dimensions (12) = candidate pool
- Score each candidate on 4 criteria:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Soul Alignment | 30% | How strongly the theme connects to coach's core values |
| Tribe Resonance | 30% | How urgently the tribe needs this content |
| Content Differentiation | 20% | How unique this angle is compared to competitors |
| Production Feasibility | 20% | Can the 4-stage pipeline produce quality output? |

Each candidate gets a composite score (0-10).

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul + tribe outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Theme Discovery SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load soul_values.json + tribe_profile.json", status: "completed" },
    { id: "step-4", description: "STEP 4: GENERATE - Score 36 theme candidates", status: "completed" },
    { id: "step-5", description: "STEP 5: SELECT - Pick top 12 themes with archetype mapping", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_themes.json + SETUP_COMPLETE.md", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Distribution + archetype coverage gates", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Mark setup_complete in config.yaml", status: "pending" }
] });
```

---

## STEP 5: SELECT

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul + tribe outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Theme Discovery SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load soul_values.json + tribe_profile.json", status: "completed" },
    { id: "step-4", description: "STEP 4: GENERATE - Score 36 theme candidates", status: "completed" },
    { id: "step-5", description: "STEP 5: SELECT - Pick top 12 themes with archetype mapping", status: "in_progress" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_themes.json + SETUP_COMPLETE.md", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Distribution + archetype coverage gates", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Mark setup_complete in config.yaml", status: "pending" }
] });
```

**Select top 12 themes from 36 candidates**, enforcing:

> [!IMPORTANT]
> **Distribution Rules (MANDATORY):**
> - Min 7 different archetype categories across 12 themes
> - No single archetype category > 3 themes
> - At least 2 themes Top-of-Funnel, 2 Bottom-of-Funnel
> - No themes with composite scores < 6.0

For each selected theme, assign:
1. **Primary archetype** (from the 22 viral frameworks)
2. **TTT assignment** (emotional temperature)
3. **Funnel position** (awareness / consideration / conversion)

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul + tribe outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Theme Discovery SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load soul_values.json + tribe_profile.json", status: "completed" },
    { id: "step-4", description: "STEP 4: GENERATE - Score 36 theme candidates", status: "completed" },
    { id: "step-5", description: "STEP 5: SELECT - Pick top 12 themes with archetype mapping", status: "completed" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_themes.json + SETUP_COMPLETE.md", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Distribution + archetype coverage gates", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Mark setup_complete in config.yaml", status: "pending" }
] });
```

---

## STEP 6: EMIT

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul + tribe outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Theme Discovery SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load soul_values.json + tribe_profile.json", status: "completed" },
    { id: "step-4", description: "STEP 4: GENERATE - Score 36 theme candidates", status: "completed" },
    { id: "step-5", description: "STEP 5: SELECT - Pick top 12 themes with archetype mapping", status: "completed" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_themes.json + SETUP_COMPLETE.md", status: "in_progress" },
    { id: "step-7", description: "STEP 7: VALIDATE - Distribution + archetype coverage gates", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Mark setup_complete in config.yaml", status: "pending" }
] });
```

**CREATE FILE 1:** `intelligence/themes/content_themes.json`

```json
{
  "content_themes": {
    "batch_id": "batch_001",
    "generated": "{ISO date}",
    "total_candidates_scored": 36,
    "themes": [
      {
        "theme_id": "T01",
        "title": "[Theme Title]",
        "soul_alignment_score": 8.5,
        "tribe_resonance_score": 9.0,
        "differentiation_score": 7.5,
        "feasibility_score": 8.0,
        "composite_score": 8.3,
        "primary_archetype": "[Archetype Name]",
        "ttt_assignment": "TTT-XX",
        "funnel_position": "awareness|consideration|conversion",
        "content_angle": "[2 sentences describing the unique angle]",
        "tribe_dimension_addressed": "[primary dimension from context premise]"
      }
    ]
  }
}
```

**CREATE FILE 2:** `SETUP_COMPLETE.md` — Summary of setup phase completion

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul + tribe outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Theme Discovery SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load soul_values.json + tribe_profile.json", status: "completed" },
    { id: "step-4", description: "STEP 4: GENERATE - Score 36 theme candidates", status: "completed" },
    { id: "step-5", description: "STEP 5: SELECT - Pick top 12 themes with archetype mapping", status: "completed" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_themes.json + SETUP_COMPLETE.md", status: "completed" },
    { id: "step-7", description: "STEP 7: VALIDATE - Distribution + archetype coverage gates", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Mark setup_complete in config.yaml", status: "pending" }
] });
```

---

## STEP 7: VALIDATE

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul + tribe outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Theme Discovery SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load soul_values.json + tribe_profile.json", status: "completed" },
    { id: "step-4", description: "STEP 4: GENERATE - Score 36 theme candidates", status: "completed" },
    { id: "step-5", description: "STEP 5: SELECT - Pick top 12 themes with archetype mapping", status: "completed" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_themes.json + SETUP_COMPLETE.md", status: "completed" },
    { id: "step-7", description: "STEP 7: VALIDATE - Distribution + archetype coverage gates", status: "in_progress" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Mark setup_complete in config.yaml", status: "pending" }
] });
```

| # | Gate | Requirement | If Fail |
|---|------|-------------|---------|
| 1 | 12 themes | Exactly 12 in output | Add/remove |
| 2 | Archetype coverage | ≥7 different archetypes | Swap to diversify |
| 3 | No dominance | No archetype > 3 themes | Swap |
| 4 | Funnel coverage | ≥2 awareness + ≥2 conversion | Reassign |
| 5 | Score floor | All composites ≥ 6.0 | Replace low-scoring |
| 6 | JSON valid | Parses without error | Fix |
| 7 | TTT diversity | ≥4 different TTT levels | Recalibrate |

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul + tribe outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Theme Discovery SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load soul_values.json + tribe_profile.json", status: "completed" },
    { id: "step-4", description: "STEP 4: GENERATE - Score 36 theme candidates", status: "completed" },
    { id: "step-5", description: "STEP 5: SELECT - Pick top 12 themes with archetype mapping", status: "completed" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_themes.json + SETUP_COMPLETE.md", status: "completed" },
    { id: "step-7", description: "STEP 7: VALIDATE - Distribution + archetype coverage gates", status: "completed" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Mark setup_complete in config.yaml", status: "pending" }
] });
```

---

## STEP 8: CHECKPOINT

**EXECUTE THIS NOW:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul + tribe outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Theme Discovery SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load soul_values.json + tribe_profile.json", status: "completed" },
    { id: "step-4", description: "STEP 4: GENERATE - Score 36 theme candidates", status: "completed" },
    { id: "step-5", description: "STEP 5: SELECT - Pick top 12 themes with archetype mapping", status: "completed" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_themes.json + SETUP_COMPLETE.md", status: "completed" },
    { id: "step-7", description: "STEP 7: VALIDATE - Distribution + archetype coverage gates", status: "completed" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Mark setup_complete in config.yaml", status: "in_progress" }
] });
```

Update `config.yaml`: `sessions.setup.theme_discover.status = "complete"`, `setup_complete: true`

**OUTPUT (25-35 words):**
```
✅ THEME DISCOVERY COMPLETE — SETUP PHASE FINISHED
- Themes: 12 selected from 36 candidates
- Archetypes: {N} represented
- TTT range: TTT-{min} to TTT-{max}
- NEXT: /ccf-research-fresh {client_name}
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({ todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul + tribe outputs exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Theme Discovery SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load soul_values.json + tribe_profile.json", status: "completed" },
    { id: "step-4", description: "STEP 4: GENERATE - Score 36 theme candidates", status: "completed" },
    { id: "step-5", description: "STEP 5: SELECT - Pick top 12 themes with archetype mapping", status: "completed" },
    { id: "step-6", description: "STEP 6: EMIT - Write content_themes.json + SETUP_COMPLETE.md", status: "completed" },
    { id: "step-7", description: "STEP 7: VALIDATE - Distribution + archetype coverage gates", status: "completed" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Mark setup_complete in config.yaml", status: "completed" }
] });
```

---

## 🔗 SETUP PHASE COMPLETE → Research Phase:
- `/ccf-research-fresh {client_name}`
- `/ccf-research-deep {client_name}`
