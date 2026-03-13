---
name: ccf-pillar-build
description: "Build 12 content pillars with 7 discovery layers — the foundation of CCF v2.5's dynamic content engine"
---

# /ccf-pillar-build {client_name}

// turbo-all

> **SKILLS_BASE:** `ccf-26/skills/ccf/`
> **SKILL:** `setup/pillar-builder/SKILL.md`
> **TEMPLATE:** `ccf-26/templates/project_context_template.json`

**Objective:** Build 12 Content Pillars with 7 Discovery Layers from existing coach and tribe intelligence. Output: `project_context.json` — the intelligence substrate that feeds every weekly subsystem.

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul + tribe outputs exist", status: "pending" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Pillar Builder SKILL.md + template", status: "pending" },
    { id: "step-3", description: "STEP 3: INGEST - Parse soul_values + tribe_profile + transcripts", status: "pending" },
    { id: "step-4", description: "STEP 4: DESIGN - Generate 12 pillar names and strategic coverage", status: "pending" },
    { id: "step-5", description: "STEP 5: POPULATE - Fill all 7 layers for each pillar", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write project_context.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Run structural + semantic + coverage gates", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
  ]
});
```

**DO NOT PROCEED until you have called `write_todos` above.**

---

## 📋 Step Execution Protocol (MANDATORY)

> [!CAUTION]
> **You MUST call `write_todos` at EVERY step transition.**
> This is not optional. Skipping todo updates = workflow failure.

**At the START of each step:** Update that step's status to `in_progress`
**At the END of each step:** Update that step's status to `completed`
**Always include ALL steps** (completed + current + pending) in every `write_todos` call.

---

## STEP 1: PRE-FLIGHT

Mark step-1 `in_progress`.

| Check | Path | If Missing |
|-------|------|------------|
| 1 | `config.yaml → sessions.setup.soul_extract.status == "complete"` | STOP → Run `/ccf-soul-extract` |
| 2 | `config.yaml → sessions.setup.tribe_extract.status == "complete"` | STOP → Run `/ccf-tribe-extract` |
| 3 | `intelligence/soul/soul_values.json` | STOP → Run `/ccf-soul-extract` |
| 4 | `intelligence/tribe/tribe_profile.json` | STOP → Run `/ccf-tribe-extract` |
| 5 | `raw/transcripts/` (optional) | WARN → Proceed without Layer 7 deep extraction |

Mark step-1 `completed`.

---

## STEP 2: LOAD SKILL + TEMPLATE

Mark step-2 `in_progress`.

1. Read FULL: `ccf-26/skills/ccf/setup/pillar-builder/SKILL.md`
2. Read FULL: `ccf-26/templates/project_context_template.json`
3. **Internalize** the 7-layer schema — each layer's purpose and downstream feed
4. **Internalize** the quality gates — structural, semantic, and coverage validation

Mark step-2 `completed`.

---

## STEP 3: INGEST

Mark step-3 `in_progress`.

Execute the SKILL.md Phase 1 (INGEST) protocol:

1. Parse `soul_values.json` → Extract coach values, expertise, philosophical positions, metaphors, voice patterns
2. Parse `tribe_profile.json` → Extract audience pains, desires, heroes, enemies, language, life stage
3. If transcripts exist → Scan for emotional peaks, repeated phrases, personal stories, anger triggers
4. **Build intersection map:** Where coach expertise meets audience need = pillar candidates

Mark step-3 `completed`.

---

## STEP 4: DESIGN — 12 Pillar Names

Mark step-4 `in_progress`.

**Generate 12 unique pillar names** following the SKILL.md Pillar Design Rules:

- Each pillar: specific enough for focused content, broad enough for 50+ themes
- No two pillars: >30% topic overlap
- Coverage: ≥3 Top-of-Funnel, ≥3 Bottom-of-Funnel, ≥2 bridge pillars
- Each pillar: clear connection to coach's current offer

**Present the 12 pillars as a numbered list with:**
- Pillar name
- One-sentence description
- Funnel position (ToFu / MoFu / BoFu / Bridge)
- Primary coach expertise connection

Mark step-4 `completed`.

---

## STEP 5: POPULATE — All 7 Layers

Mark step-5 `in_progress`.

**For EACH of the 12 pillars, populate ALL 7 layers** following the SKILL.md Phase 2 (REASON) protocol.

> [!CAUTION]
> **Layer 7 (Trigger Archive):** If you do not have transcript evidence for a specific trigger, mark it as `"needs_coach_input": true` with description `"[PENDING — requires coach interview]"`. NEVER fabricate personal experiences.

**Work through pillars sequentially.** For each pillar:
1. Layer 1: Assess market sophistication level (1-5) + implication
2. Layer 2: Identify 2-4 Adjacent Worlds with connections and keywords
3. Layer 3: Name 2-4 Key Voices (≥1 friction voice) with search keywords
4. Layer 4: Map Emotional Landscape (pain, desire, hidden_fear) with DHD
5. Layer 5: Populate Cultural Hooks (seasonal, hashtags, subreddits, trends, news)
6. Layer 6: Define Contrarian Position (mainstream → counter → enemy → phrase)
7. Layer 7: Populate Trigger Archive from available evidence

Mark step-5 `completed`.

---

## STEP 6: EMIT

Mark step-6 `in_progress`.

**CREATE FILE:** `intelligence/project_context.json`

- Load the template from `ccf-26/templates/project_context_template.json`
- Populate `project` metadata from config.yaml
- Populate `brand_identity` from soul_values + tribe_profile
- Insert all 12 populated pillars into `content_pillars` array
- Set `rotation_config` defaults: 4 pillars/week, 2-week cooldown
- Initialize `weekly_history` as empty array

**Ensure valid JSON** — no trailing commas, proper escaping, all brackets matched.

Mark step-6 `completed`.

---

## STEP 7: VALIDATE

Mark step-7 `in_progress`.

Execute ALL quality gate checks from the SKILL.md Phase 4 (VALIDATE):

**Structural Validation:**
| # | Check | Pass/Fail |
|---|-------|-----------|
| 1 | 12 pillars present with unique IDs | |
| 2 | All 7 layers populated per pillar | |
| 3 | No empty strings in Layers 1-6 | |
| 4 | Market Sophistication levels are 1-5 | |
| 5 | Each pillar has ≥2 Adjacent Worlds | |
| 6 | Each pillar has ≥2 Key Voices (≥1 friction) | |
| 7 | Emotional Landscape has 3 complete sub-fields | |
| 8 | Cultural Hooks has ≥2 entries per sub-field | |
| 9 | Contrarian Position has all 4 sub-fields | |

**Semantic Validation:**
| # | Check | Pass/Fail |
|---|-------|-----------|
| 1 | No duplicate Contrarian counter_stances | |
| 2 | Adjacent Worlds are genuinely adjacent | |
| 3 | Key Voices are real, searchable people | |
| 4 | Emotional descriptions are specific | |
| 5 | No vocabulary blacklist terms in content | |

**Coverage Validation:**
| # | Check | Pass/Fail |
|---|-------|-----------|
| 1 | ≥3 Top-of-Funnel pillars | |
| 2 | ≥3 Bottom-of-Funnel pillars | |
| 3 | ≥2 bridge pillars | |
| 4 | All 12 connect to coach's offer | |

> [!CAUTION]
> **If ANY structural validation fails → FIX before proceeding.**
> Semantic and coverage failures are WARNINGs — log them but continue.

Mark step-7 `completed`.

---

## STEP 8: CHECKPOINT

Mark step-8 `in_progress`.

Update `config.yaml`:
```yaml
sessions:
  setup:
    pillar_build:
      status: "complete"
      timestamp: "{ISO date}"
      pillars_count: 12
      layers_complete: [1, 2, 3, 4, 5, 6]
      layers_pending_coach_input: [7]
      pending_triggers: {count}
```

**OUTPUT (30-40 words):**
```
✅ PILLAR BUILD COMPLETE
- Client: {client_name}
- Pillars: 12 (7 layers each)
- Layer 7 status: {N} triggers populated, {M} pending coach input
- Quality: {passed}/{total} gates passed
- NEXT: /ccf-radar {client_name}
```

Mark step-8 `completed`.

---

## 🔗 NEXT: `/ccf-radar {client_name}`
