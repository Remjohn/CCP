---
name: ccf-research-fresh
description: Browser-verified temporal intelligence gathering for discovered themes
---

# /ccf-research-fresh {client_name}

// turbo-all

> **SKILLS_BASE:** `ccf-26/skills/ccf/`
> **PROTOCOL:** `research/fresh-analysts/_FRESH_RESEARCH_PROTOCOL.md`
> **SKILL:** `research/fresh-analysts/{archetype}/SKILL.md`
> **QUERY GENERATOR:** `research/smart-query-generator/SKILL.md`

**Objective:** Gather browser-verified, real-time research data for each content theme — the "this just happened" intelligence layer. Every claim must be backed by a REAL URL obtained via `web_search`.

> [!IMPORTANT]
> ## H7 UPSTREAM DEPENDENCY
> **Run `/ccf-raw-research {client_name}` FIRST.** This command expects `research/raw-fresh/{blueprint_id}_raw_fresh_research.md` to exist.
> If the RAW dossier is available, analysts consume it (V2.1 mode — preserving `novelty_class`, `surprise_score`, `recency_grade`, `mode`, `vibe_bait` metadata).
> If the RAW dossier is missing, the command falls back to V2.0 (original browser-search-based research).

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify setup + themes + BROWSER ACCESS", status: "pending" },
    { id: "step-2", description: "STEP 2: LOAD CONTEXT - Read themes, blueprints, soul, tribe", status: "pending" },
    { id: "step-3", description: "STEP 3: LOAD PROTOCOL - Read _FRESH_RESEARCH_PROTOCOL.md", status: "pending" },
    { id: "step-4", description: "STEP 4: FOR EACH THEME - Generate queries → Browser search → Verify URLs", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write {blueprint_id}_fresh_research.md per theme", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Recency + URL verification + forbidden terms", status: "pending" },
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

## STEP 1: PRE-FLIGHT & BROWSER CHECK

**EXECUTE:** `write_todos` with STEP 1 as `in_progress`

### 1A. Verify Prerequisites

| Check | Path | If Missing |
|-------|------|------------|
| 1 | `config.yaml → setup_complete == true` | STOP → Complete setup phase first |
| 2 | `intelligence/themes/content_themes.json` | STOP → Run `/ccf-theme-discover` |
| 3 | `intelligence/tribe/tribe_profile.json` | STOP → Run `/ccf-tribe-extract` |
| 4 | `intelligence/soul/soul_values.json` | STOP → Run `/ccf-soul-extract` |
| 5 | `research/content_blueprints.json` | STOP → Run `/ccf-blueprint` |

### 1B. BROWSER CAPABILITY CHECK

> [!CAUTION]
> ## 🚨 MANDATORY BROWSER TEST
> This command REQUIRES `web_search` for real-time intelligence.
> **DO NOT proceed without browser access.**

**Test your browser access NOW:**

```javascript
web_search("latest research 2026")
// → If this works, continue
// → If this fails, STOP and inform user
```

**EXECUTE:** `write_todos` with STEP 1 as `completed` only if browser works

---

## STEP 2: LOAD CONTEXT

**EXECUTE:** `write_todos` with STEP 2 as `in_progress`

1. Parse `content_themes.json` — extract all 12 themes
2. For each theme, note: `theme_id`, `title`, `tribe_dimension_addressed`, `content_angle`
3. Parse `content_blueprints.json` — get archetype assignment per blueprint
4. Load `soul_values.json` — for Tone Emulation in brief writing
5. Load `tribe_profile.json` — for tribal framing of search queries

**EXECUTE:** `write_todos` with STEP 2 as `completed`

---

## STEP 3: LOAD PROTOCOL & SKILLS

**EXECUTE:** `write_todos` with STEP 3 as `in_progress`

### 3A. Load shared protocol

📚 **READ:** `ccf-26/skills/ccf/research/fresh-analysts/_FRESH_RESEARCH_PROTOCOL.md`

This protocol defines the 6-phase execution model you MUST follow for each theme.

### 3B. Load Smart Query Generator

📚 **READ:** `ccf-26/skills/ccf/research/smart-query-generator/SKILL.md`

This skill generates targeted search queries. Set `mode = "fresh"`.

### 3C. Identify archetype-specific skills

For each blueprint, note the archetype. The matching skill is at:
`ccf-26/skills/ccf/research/fresh-analysts/{archetype}/SKILL.md`

> [!NOTE]
> There are 41 fresh analyst skills. Load each one ONLY when processing its theme.

**EXECUTE:** `write_todos` with STEP 3 as `completed`

---

## STEP 4: RESEARCH (Per Theme — 12 Total)

**EXECUTE:** `write_todos` with STEP 4 as `in_progress`

> [!CAUTION]
> **CONTEXT WINDOW:** Process themes SEQUENTIALLY. Complete one theme fully before starting the next.

### For EACH theme (12 total), follow the FRESH RESEARCH PROTOCOL:

**Phase 1 — Context:** Load the theme + its blueprint + archetype
**Phase 2 — Query Generation:** Use Smart Query Generator (mode=fresh) → 5-8 queries
**Phase 3 — Browser Execution:**

```
FOR EACH query:
  1. Execute: web_search("{query text}")
  2. Extract 2-3 REAL URLs from results
  3. Record: URL, title, date, relevance
  4. If < 2 results, reformulate and retry ONCE
```

**Phase 4 — URL Verification:**

```javascript
FOR EACH url in findings:
  read_url_content({ url: "{url}" })
  // VALID → extract key data point
  // INVALID → search for replacement
```

**Phase 5 — Archetype Synthesis:**

Load the archetype-specific fresh analyst skill:
`ccf-26/skills/ccf/research/fresh-analysts/{archetype}/SKILL.md`

Apply its specific analysis logic using ONLY the verified data from Phase 4.
Apply Tone Emulation from soul_values.json.

> [!IMPORTANT]
> **FORBIDDEN TERMS** — If ANY of these appear in output, the brief FAILS:
> `[General Culture]`, `[Various]`, `[Research indicates]` (without citation), `N/A`, `example.com`

**Phase 6 — Emit:** Write the structured brief (see protocol for template)

### Progress Tracking

Update todos after each theme:
```
Themes processed: {N}/12 | URLs verified: {count} | Briefs written: {count}
```

**EXECUTE:** `write_todos` with STEP 4 as `completed` after all 12 themes

---

## STEP 5: EMIT — Verify All Files Created

**EXECUTE:** `write_todos` with STEP 5 as `in_progress`

Verify that 12 files exist in `research/fresh/`:

| # | Blueprint | File | Status |
|---|-----------|------|--------|
| 1 | BP-001 | `BP-001_{archetype}_fresh_research.md` | ✅/❌ |
| 2 | BP-002 | `BP-002_{archetype}_fresh_research.md` | ✅/❌ |
| ... | ... | ... | ... |
| 12 | BP-012 | `BP-012_{archetype}_fresh_research.md` | ✅/❌ |

If any are missing, generate them now.

**EXECUTE:** `write_todos` with STEP 5 as `completed`

---

## STEP 6: VALIDATE

**EXECUTE:** `write_todos` with STEP 6 as `in_progress`

| # | Gate | Requirement | If Fail |
|---|------|-------------|---------|
| 1 | Recency | All data points have verifiable dates < 30 days | Remove stale data |
| 2 | Specificity | Specific numbers, dates, named people | Add specifics |
| 3 | Source verification | Every URL was obtained via `web_search` | Remove hallucinated URLs |
| 4 | URL validity | Every URL verified with `read_url_content` | Replace invalid URLs |
| 5 | Forbidden terms | Zero instances of placeholder text | Rewrite with real data |
| 6 | Tribe framing | Impact section references tribe_profile | Add context |
| 7 | Voice alignment | Brief reads in coach's voice | Apply Tone Emulation |
| 8 | Completeness | 12 brief files created | Generate missing |
| 9 | Minimum URLs | At least 8 verified URLs per brief | Search for more |

**EXECUTE:** `write_todos` with STEP 6 as `completed`

---

## STEP 7: CHECKPOINT

**EXECUTE:** `write_todos` with STEP 7 as `in_progress`

Update `config.yaml`: `sessions.research.fresh.status = "complete"`

**OUTPUT (25-35 words):**
```
✅ FRESH RESEARCH COMPLETE (Browser-Verified)
- Briefs: 12 generated
- Total verified URLs: {count}
- Browser searches executed: {count}
- NEXT: /ccf-research-deep {client_name}
```

**EXECUTE:** `write_todos` with STEP 7 as `completed`

---

## 🔗 NEXT: `/ccf-research-deep {client_name}`
