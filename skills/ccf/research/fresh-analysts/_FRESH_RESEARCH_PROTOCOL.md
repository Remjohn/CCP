---
name: Fresh Research Protocol V2.1 (Laws-Governed Analyst)
description: Browser-verified real-time research protocol — consumes H7 RAW dossier
phase: research
version: 2.1
---

# 📋 FRESH RESEARCH PROTOCOL V2.1 — Laws-Governed Analyst

> [!IMPORTANT]
> ## H7 RAW Research Integration (V2.1)
> As of V2.1, the Fresh Analyst receives a **pre-researched 4000-word RAW dossier** from H7 (`raw-fresh-research/SKILL.md`).
> Each finding in the RAW dossier carries: `novelty_class`, `surprise_score`, `recency_grade`, `mode`, `vibe_bait`, and `temporal_leverage` metadata.
> **Your job as analyst:** Distill the 4000-word dossier into a 1000-1200 word brief **preserving these metadata fields.**
> If the H7 RAW dossier is not available, fall back to the original V2.0 protocol below.

> [!CAUTION]
> ## 🚨 CRITICAL BROWSER REQUIREMENT
> This protocol REQUIRES `web_search` or `read_url_content` tools.
> **DO NOT hallucinate URLs.** Every URL must come from a REAL browser search.
> If you cannot access browser tools, STOP and inform the user.

---

## Protocol Overview

This protocol standardizes how ALL fresh analyst skills gather real-time intelligence. Every fresh analyst MUST follow these 6 phases before applying their archetype-specific analysis logic.

```
PHASE 1: Context Load → PHASE 2: Query Generation → PHASE 3: Browser Execution
→ PHASE 4: URL Verification → PHASE 5: Archetype Synthesis → PHASE 6: Output
```

---

## PHASE 1: CONTEXT LOAD

Load these files to ground research in the client's identity:

| # | File | Extract | If Missing |
|---|------|---------|------------|
| 1 | `config.yaml` | Client name, setup status | STOP |
| 2 | `intelligence/soul/soul_values.json` | Emotional vocabulary, signature metaphors, pacing | STOP → Run `/ccf-soul-extract` |
| 3 | `intelligence/tribe/tribe_profile.json` | Core anxieties, shared heroes, cultural artifacts, tribe slang | STOP → Run `/ccf-tribe-extract` |
| 4 | `intelligence/themes/content_themes.json` | Content theme being researched | STOP → Run `/ccf-theme-discover` |
| 5 | `research/content_blueprints.json` | Blueprint with archetype assignment | STOP → Run `/ccf-blueprint` |

**Key Extraction:**
```
From soul_values.json:
  → emotional_vocabulary (positive + negative word lists)
  → signature_metaphors (for tone emulation)
  → core_values (for alignment filtering)

From tribe_profile.json:
  → core_anxieties (what keeps tribe awake)
  → shared_heroes (who tribe admires)
  → cultural_artifacts (objects, rituals, references)
  → tribe_slang (authentic language)

From content_themes.json:
  → theme being researched (title, tribe_dimension_addressed, content_angle)

From content_blueprints.json:
  → blueprint_id, archetype, content_frameworks_used
```

---

## PHASE 2: QUERY GENERATION

> [!IMPORTANT]
> Load the Smart Query Generator skill FIRST:
> `ccf-26/skills/ccf/research/smart-query-generator/SKILL.md`

### Generate 5-8 Targeted Search Queries (Trigger Ammunition - Item 19)

For the current theme + mapped trigger combination, analysts DO NOT search for general topic support. They must query exclusively for **Trigger Ammunition** — real-time events, news, or data that validate or escalate the specific tension of the assigned `trigger_id`. Generate queries that target:

| Query Type | Focus | Temporal Constraint |
|:-----------|:------|:-------------------|
| **Breaking News** | Latest developments in theme domain | < 14 days |
| **Recent Study** | Academic/industry research published recently | < 6 months |
| **Expert Opinion** | Named expert commentary on theme topic | < 3 months |
| **Trend Signal** | Emerging pattern or shift in the domain | < 30 days |
| **Tribal Impact** | How this affects the specific tribe | < 30 days |
| **Contrarian Data** | Evidence that challenges mainstream view | < 6 months |
| **Case Study** | Real-world example proving the concept | < 12 months |

### Query Construction Rules

1. **Use natural language** — optimized for semantic search
2. **Include tribal language** — use tribe_slang terms when relevant
3. **Add temporal markers** — "2025", "2024", "recent", "latest"
4. **Name specific entities** — coaches, brands, publications the tribe follows
5. **Target authoritative sources** — academic journals, industry reports, named experts

**Output:** Array of 5-8 search queries with strategic annotations:
```json
{
  "queries": [
    {
      "query": "intermittent fasting 2025 study metabolic health results",
      "type": "recent_study",
      "expected_output": "2-3 URLs with specific data points"
    }
  ]
}
```

---

## PHASE 3: BROWSER EXECUTION

> [!CAUTION]
> You MUST use `web_search` for EVERY query. Do NOT skip this step.
> Do NOT generate URLs from memory or training data.

### Research Loop

```
FOR EACH query in generated_queries:
  1. Execute: web_search("{query text}")
  2. Extract 2-3 REAL URLs from search results
  3. Record: URL, title, date published, relevance score
  4. If search returns < 2 results, reformulate query and retry ONCE
```

### Findings Tracker

Build this table as you search:

| Q# | Query Type | Search Used | URL 1 | URL 2 | URL 3 | Date |
|----|-----------|-------------|-------|-------|-------|------|
| 1 | Breaking news | {actual query} | [REAL URL] | [REAL URL] | - | {date} |
| 2 | Recent study | {actual query} | [REAL URL] | [REAL URL] | [REAL URL] | {date} |
| ... | | | | | | |

**Target:** 12-18 verified URLs total (2-3 per query)

---

## PHASE 4: URL VERIFICATION

> [!CAUTION]
> Every URL in Phase 3 MUST be verified before use.

### Verification Loop

```javascript
FOR EACH url in findings:
  read_url_content({ url: "{url}" })
  // If returns content → Mark VALID, extract key data point
  // If returns error  → Mark INVALID, search for replacement
```

### Forbidden Terms (Auto-Reject)

If ANY of these appear in your output, the research brief FAILS:

- `[General Culture]`
- `[Verified in Tribe Soul]`
- `[Various]`
- `[Various studies show]`
- `[Research indicates]` (without specific citation)
- `N/A`
- `example.com`
- Any URL you did NOT get from `web_search`

---

## PHASE 5: ARCHETYPE SYNTHESIS

**NOW execute the archetype-specific analyst logic from the loaded skill.**

The analyst receives ONLY verified data from Phases 3-4. It must:

1. **Filter by relevance** — Keep only data that serves the archetype's emotional goal
2. **Apply Tone Emulation** — Write in the coach's voice using soul_values.json:
   - Match `emotional_vocabulary`
   - Use `signature_metaphors` naturally
   - Respect `profanity_level` (0-5)
   - Match `rhythm_pattern` (sentence length and pacing)
3. **Frame through tribe lens** — Every insight must answer: "Why should THIS tribe care?"
4. **Cite every claim** — Every data point must reference a verified URL

---

## PHASE 6: OUTPUT

**CREATE FILE:** `research/fresh/{blueprint_id}_{archetype}_fresh_research.md`

### Required Structure

```markdown
# Fresh Research Brief: {THEME_TITLE}

**Blueprint:** {blueprint_id}
**Archetype:** {archetype_name}
**Generated:** {ISO timestamp}
**Recency Window:** < 30 days
**Verified URLs:** {count}

---

## Intelligence Summary (150 words max)

{Coach-voiced summary of key findings}

---

## Verified Data Points

| # | Data Point | Source | Verified URL | Date | Recency |
|---|-----------|--------|--------------|------|---------|
| 1 | {Specific fact/stat} | {Publication} | [REAL URL] | {date} | ✅ < 30d |
| 2 | {Expert quote} | {Expert name, title} | [REAL URL] | {date} | ✅ < 30d |
| ... | | | | | |

---

## Expert Voices

| Expert | Title/Affil | Quote | Verified URL |
|--------|-------------|-------|--------------|
| {Name} | {Title} | "{Direct quote}" | [REAL URL] |

---

## Trend Signals

| Signal | Evidence | Tribe Impact | Source |
|--------|----------|--------------|--------|
| {Pattern} | {Data} | {Why tribe cares} | [REAL URL] |

---

## Content Hook Potential

{1-2 sentences: How this data creates urgency for the content piece}

---

## Research Sources Index

1. [{Title}]({URL}) — Retrieved: {date}
2. ...
```

---

## VALIDATION GATES

| # | Gate | Requirement | If Fail |
|---|------|-------------|---------|
| 1 | **Recency** | All data points have verified dates < 30 days | Remove stale data, search again |
| 2 | **Specificity** | Specific numbers, dates, named people | Add specifics or remove |
| 3 | **Source verification** | Every URL was obtained via `web_search` | Remove hallucinated URLs |
| 4 | **URL validity** | Every URL verified with `read_url_content` | Replace invalid URLs |
| 5 | **Forbidden terms** | Zero instances of forbidden placeholder text | Rewrite with real data |
| 6 | **Tribe framing** | Impact section references tribe_profile | Add tribal context |
| 7 | **Voice alignment** | Brief reads in coach's voice, not generic researcher | Apply Tone Emulation |
| 8 | **Minimum URLs** | At least 8 verified URLs per brief | Search for more |

---

## HANDOFF

The fresh research brief feeds into:
- **`ccf-research-deep`** — Deep analyst inherits the fresh context
- **`ccf-generate`** — Script generator uses fresh data for temporal hooks

---

**END OF FRESH RESEARCH PROTOCOL V2.1**

---

## V2.1 — Preserved Metadata in Analyst Output

When consuming H7 RAW dossier, the analyst brief MUST include per finding:
- `novelty_class`: NOVEL / CONFIRMING / CONTRADICTING
- `surprise_score`: 0 or 1
- `recency_grade`: HOT / WARM / COOL
- `mode`: T/V/R
- `vibe_bait`: YES/NO + description
- `temporal_leverage`: why timing matters NOW
