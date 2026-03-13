---
name: ccf-eroll-plan
description: CCF E-Roll Asset Planning — Route to archetype-specific planner and generate asset plan
---

# /ccf-eroll-plan {ARCHETYPE} {CONTENT_TOPIC} [--project {PROJECT_FOLDER}]

// turbo-all

> **SKILLS_BASE:** `skills/ccf/eroll/`
> **Usage:** `Read commands/ccf-eroll-plan.md and execute for archetype "debunking-myths" with content "Why calorie counting doesn't work"`
> **With project:** `Read commands/ccf-eroll-plan.md and execute for archetype "debunking-myths" with content "Why calorie counting doesn't work" --project "production/Coach Adele/01_CCF_CalorieMythBuster"`

**Objective:** Route to the correct archetype-specific E-Roll planner skill and generate a research-grounded `_eroll_asset_plan.json`.

> [!IMPORTANT]
> This command does NOT require browser access. It plans what to research — the actual browser research happens in `/ccf-eroll-research`.

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Parse arguments + verify inputs", status: "pending" },
    { id: "step-2", description: "STEP 2: ROUTE ARCHETYPE - Select planner skill from routing table", status: "pending" },
    { id: "step-3", description: "STEP 3: LOAD SKILL - Read the matched planner SKILL.md completely", status: "pending" },
    { id: "step-4", description: "STEP 4: EXECUTE PLAN - Run planner algorithm → _eroll_asset_plan.json", status: "pending" },
    { id: "step-5", description: "STEP 5: VALIDATE - Confirm asset plan quality gates", status: "pending" }
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

> [!IMPORTANT]
> **Validation Gate:** Before marking a step `completed`, verify:
> - Output file exists (if applicable)
> - Output matches expected schema
> - No error messages encountered

---

## STEP 1: PRE-FLIGHT

**EXECUTE:** `write_todos` with STEP 1 as `in_progress`

### 1A. Parse Arguments

| Argument | Source | Required |
|:---------|:-------|:---------|
| `{ARCHETYPE}` | User's command | ✅ Yes |
| `{CONTENT_TOPIC}` | User's command | ✅ Yes |
| `{PROJECT_FOLDER}` | User's `--project` flag | Optional |

### 1B. Load Context Files

**If `{PROJECT_FOLDER}` is provided:**

| # | File | Path | If Missing |
|---|------|------|------------|
| 1 | `validated_content` | `{PROJECT_FOLDER}/validated_content.json` | Use `{CONTENT_TOPIC}` directly |
| 2 | `conscious_soul_values` | `{PROJECT_FOLDER}/conscious_soul_values.json` | Infer from content — flag `[MISSING_DATA]` |
| 3 | `character_lexicon` | `{PROJECT_FOLDER}/character_lexicon.json` | Use generic character — flag `[MISSING_DATA]` |
| 4 | `deep_briefs/` | `{PROJECT_FOLDER}/deep_briefs/` | Proceed without — planner handles gracefully |

**If no project folder:**

```
Use {CONTENT_TOPIC} directly:
  validated_content = {CONTENT_TOPIC}
  conscious_soul_values = Infer from content topic (tribe, values, enemies)
  character_lexicon = Not loaded (planner will use "generic" flag)
  deep_briefs = Not loaded
```

**OUTPUT (20-40 words):**
```
STEP 1 COMPLETE:
- Archetype: {ARCHETYPE}
- Content: {CONTENT_TOPIC}
- Project: {PROJECT_FOLDER or "none"}
- Context files loaded: {count}/4
```

**EXECUTE:** `write_todos` with STEP 1 as `completed`

---

## STEP 2: ROUTE ARCHETYPE

**EXECUTE:** `write_todos` with STEP 2 as `in_progress`

### ARCHETYPE ROUTING TABLE

| `{ARCHETYPE}` Value | Planner Skill Path |
|:---------------------|:-------------------|
| `storytelling-archetypes` | `skills/ccf/eroll/storytelling-planner/SKILL.md` |
| `dopamine-cliff-carousel` | `skills/ccf/eroll/dopamine-cliff-planner/SKILL.md` |
| `relief-peak-carousel` | `skills/ccf/eroll/relief-peak-planner/SKILL.md` |
| `case-study` | `skills/ccf/eroll/case-study-planner/SKILL.md` |
| `listicle` | `skills/ccf/eroll/listicle-planner/SKILL.md` |
| `visual-timeline` | `skills/ccf/eroll/visual-timeline-planner/SKILL.md` |
| `debunking-myths` | `skills/ccf/eroll/debunking-myths-planner/SKILL.md` |
| `controversial-dilemma-poll` | `skills/ccf/eroll/controversial-dilemma-planner/SKILL.md` |
| `comparison-archetypes` | `skills/ccf/eroll/comparison-planner/SKILL.md` |
| `conceptual-contrast` | `skills/ccf/eroll/conceptual-contrast-planner/SKILL.md` |
| `archetypical-poll` | `skills/ccf/eroll/archetypical-poll-planner/SKILL.md` |
| `stereotypical-poll` | `skills/ccf/eroll/stereotypical-poll-planner/SKILL.md` |
| `observational-humor` | `skills/ccf/eroll/observational-humor-planner/SKILL.md` |
| `worst-case-scenario` | `skills/ccf/eroll/worst-case-planner/SKILL.md` |

> [!CAUTION]
> If `{ARCHETYPE}` does not match any entry above, **STOP** and ask the user which archetype they want. DO NOT guess. DO NOT use a fallback.

**ACTIONS:**
1. Match `{ARCHETYPE}` against the routing table
2. Record the matched skill path
3. Verify the skill file exists on disk

**OUTPUT (20-30 words):**
```
STEP 2 COMPLETE:
- Matched archetype: {ARCHETYPE}
- Planner skill: {skill path}
- File exists: ✅
```

**EXECUTE:** `write_todos` with STEP 2 as `completed`

---

## STEP 3: LOAD SKILL

**EXECUTE:** `write_todos` with STEP 3 as `in_progress`

**ACTIONS:**
1. Read the FULL skill file from Step 2 (do NOT summarize, do NOT skip sections)
2. Internalize:
   - **Key Principle** — The soul of this archetype's research
   - **Critical Rules** — Hard constraints
   - **Scene Structure** — How many scenes, what each scene needs
   - **Research Questions** — The exact questions to answer (Phase 2)
   - **Planning Strategy** — The strategy name (e.g., `EVIDENCE_CHAIN`, `CONTRAST_SPLIT`)
   - **Output Schema** — The `_eroll_asset_plan.json` structure
   - **Validation Checklist** — What to verify after generation

**OUTPUT (30-50 words):**
```
STEP 3 COMPLETE:
- Skill loaded: {name from YAML}
- Planning strategy: {strategy name}
- Research questions: {count}
- Scenes: {count}
- Archetype: {archetype}
```

**EXECUTE:** `write_todos` with STEP 3 as `completed`

---

## STEP 4: EXECUTE PLAN

**EXECUTE:** `write_todos` with STEP 4 as `in_progress`

### 4A. Run the Planner's Algorithm

Follow the loaded skill's phases in order:

1. **PHASE 1: CONTEXT LOADING** — Apply the inputs from Step 1 to the skill's context requirements
2. **PHASE 2: VISUAL RESEARCH QUESTIONS** — Answer each question by analyzing `validated_content` + `conscious_soul_values`
3. **PHASE 3: ASSET PLAN GENERATION** — Build the asset entries following the skill's logic

### 4B. Generate Output File

**CREATE FILE:** `{PROJECT_FOLDER}/{project_id}_eroll_asset_plan.json`

If no project folder: print JSON to console.

The JSON MUST match the loaded skill's output schema exactly. Required fields for every asset:

| Field | Required | Verify |
|:------|:---------|:-------|
| `id` | ✅ | Unique per asset |
| `scene` | ✅ | Maps to archetype's scene structure |
| `asset_type` | ✅ | From skill's vocabulary |
| `description` | ✅ | NOT generic — contains tribal/cultural specificity |
| `query_strategy` | ✅ | One of: `evidence`, `cultural_reference`, `environmental`, `symbolic`, `contrast` |
| `context_from_content` | ✅ | Traced to `validated_content` |
| `soul_alignment` | ✅ | Links to `conscious_soul_values` |
| `priority` | ✅ | `critical`, `important`, or `nice_to_have` |

**OUTPUT (50-80 words):**
```
STEP 4 COMPLETE:
- Asset plan generated: {filename}
- Total assets: {count}
- Priority distribution: {critical: N, important: N, nice_to_have: N}
- Query strategies used: {list}
```

**EXECUTE:** `write_todos` with STEP 4 as `completed`

---

## STEP 5: VALIDATE

**EXECUTE:** `write_todos` with STEP 5 as `in_progress`

**RUN THESE 7 VALIDATION CHECKS:**

| # | Check | Requirement | Result |
|---|-------|-------------|--------|
| 1 | Asset count | Matches archetype's expected range | ✅/❌ |
| 2 | All scenes covered | Every scene in the archetype has ≥1 asset | ✅/❌ |
| 3 | Query strategies set | No empty `query_strategy` fields | ✅/❌ |
| 4 | Soul alignment present | Every asset has a `soul_alignment` value | ✅/❌ |
| 5 | No generic descriptions | No descriptions contain "happy person", "generic", or stock language | ✅/❌ |
| 6 | Priority assigned | At least 1 asset is "critical" | ✅/❌ |
| 7 | Context traced | Every `context_from_content` references actual content | ✅/❌ |

**IF ANY CHECK FAILS:** Rewrite the failing asset(s) before proceeding.
**IF ALL PASS:**

```
✅ CCF E-ROLL ASSET PLAN COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Archetype:         {ARCHETYPE}
Content:           {CONTENT_TOPIC}
Planning Strategy: {strategy name}
Total Assets:      {N}
Scenes Covered:    {N}/{N}
All Validations:   ✅ PASSED (7/7)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Output: {project_id}_eroll_asset_plan.json
```

**EXECUTE:** `write_todos` with STEP 5 as `completed`

---

## 🔗 NEXT COMMAND

`/ccf-eroll-research {project_id}`

> This command takes the asset plan and executes browser-based research to find verified URLs for each asset.

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

**END OF CCF-EROLL-PLAN COMMAND**
