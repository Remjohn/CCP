---
name: ccf-eroll-research
description: CCF E-Roll Asset Research — Execute browser searches from asset plan and produce verified manifest
---

# /ccf-eroll-research {project_id}

// turbo-all

> **SKILLS_BASE:** `skills/ccf/eroll/`
> **Usage:** `Read commands/ccf-eroll-research.md and execute for project "01_CCF_CalorieMythBuster"`

**Objective:** Execute browser-based research for each asset in the E-Roll plan, validate all URLs, and produce a verified `_eroll_asset_manifest.json`.

> [!CAUTION]
> ## 🚨 CRITICAL BROWSER REQUIREMENT
> This command REQUIRES `web_search` and `read_url_content` tools.
> **DO NOT hallucinate URLs.** Every URL must be obtained from REAL browser searches.
> If you cannot access browser tools, STOP and inform the user.

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify asset plan + browser check", status: "pending" },
    { id: "step-2", description: "STEP 2: LOAD RESEARCHER - Read asset-researcher SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: EXECUTE RESEARCH - Browser search for each asset in plan", status: "pending" },
    { id: "step-4", description: "STEP 4: VALIDATE URLs - Verify every URL via read_url_content", status: "pending" },
    { id: "step-5", description: "STEP 5: SOUL ALIGNMENT - Check assets match conscious_soul_values", status: "pending" },
    { id: "step-6", description: "STEP 6: OUTPUT - Write _eroll_asset_manifest.json", status: "pending" }
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

## STEP 1: PRE-FLIGHT & BROWSER CHECK

**EXECUTE:** `write_todos` with STEP 1 as `in_progress`

### 1A. Verify Input Files

| # | File | Path | If Missing |
|---|------|------|------------|
| 1 | **Asset Plan** | `{project_id}_eroll_asset_plan.json` | STOP → Run `/ccf-eroll-plan` first |
| 2 | **Soul Values** | `conscious_soul_values.json` | Proceed with plan context only — flag `[MISSING_DATA]` |

### 1B. Read Asset Plan Summary

```
From _eroll_asset_plan.json extract:
  → archetype (which recipe this plan serves)
  → planning_strategy (e.g., EVIDENCE_CHAIN, CONTRAST_SPLIT)
  → total_assets_needed (how many searches to execute)
  → Each asset's: id, query_strategy, context_from_content, priority
```

### 1C. Browser Capability Check

**⚠️ MANDATORY: Test your browser access NOW:**

```javascript
web_search("test search query")
// → If this works, continue
// → If this fails, STOP and inform user
```

**OUTPUT (20-40 words):**
```
STEP 1 COMPLETE:
- Asset plan loaded: {filename}
- Archetype: {archetype}
- Total assets to research: {N}
- Browser access: ✅
```

**EXECUTE:** `write_todos` with STEP 1 as `completed`

---

## STEP 2: LOAD RESEARCHER SKILL

**EXECUTE:** `write_todos` with STEP 2 as `in_progress`

**ACTIONS:**
1. Read the FULL skill file: `skills/ccf/eroll/asset-researcher/SKILL.md`
2. Do NOT summarize, do NOT skip sections
3. Internalize:
   - **The 5 Query Strategy Formulas** — How to construct queries for each strategy type:
     - `evidence` → `[claim] + [source type] + [authority marker]`
     - `cultural_reference` → `[cultural element] + [tribe context] + [visual medium]`
     - `environmental` → `[setting descriptor] + [time/place markers] + [photography/documentary]`
     - `symbolic` → `[concept] + [iconic representation] + [visual medium]`
     - `contrast` → `[Side A] + "versus" OR "compared to" + [Side B]`
   - **Execution Protocol** — Check suggested sources → construct query → search → validate → refine
   - **Soul Alignment Validation** — How to verify assets match tribe values
   - **Error Handling** — Dead links, unresolvable queries, missing critical assets

**OUTPUT (20-30 words):**
```
STEP 2 COMPLETE:
- Skill loaded: asset-researcher
- Query formulas internalized: 5
- Execution protocol: ready
```

**EXECUTE:** `write_todos` with STEP 2 as `completed`

---

## STEP 3: EXECUTE RESEARCH

**EXECUTE:** `write_todos` with STEP 3 as `in_progress`

> [!CAUTION]
> **FOR EACH ASSET in the plan, execute the search loop below.**
> Process assets in PRIORITY ORDER: `critical` first, then `important`, then `nice_to_have`.
> DO NOT skip any asset. DO NOT hallucinate URLs.

### 3A. RESEARCH LOOP

```
FOR EACH asset in _eroll_asset_plan.json (sorted by priority):

  1. READ asset.query_strategy
  2. CONSTRUCT query using the matching formula from the researcher skill:
     
     IF query_strategy == "evidence":
       query = "[asset.context_from_content topic] + [study|fact-check|statistics] + [Forbes|Harvard|WHO]"
     
     IF query_strategy == "cultural_reference":
       query = "[asset.context cultural element] + [tribe context from soul_values] + [photography|documentary]"
     
     IF query_strategy == "environmental":
       query = "[asset.description setting] + [time/place markers] + [photography|aesthetic]"
     
     IF query_strategy == "symbolic":
       query = "[asset.description concept] + [iconic|symbol|archetype] + [visual|photography]"
     
     IF query_strategy == "contrast":
       query = "[Side A] versus [Side B] + [comparison|before after]"
  
  3. CHECK suggested_sources first (if any exist in the plan):
     FOR url in asset.suggested_sources:
       read_url_content({ url: url })
       IF valid and relevant → add to findings

  4. EXECUTE: web_search(query)
  
  5. RECORD top 2-3 results:
     - url
     - title
     - relevance_note (why this result matches the asset need)
  
  6. IF results are poor (0 relevant results):
     - REFINE query using conscious_soul_values for additional context
     - web_search(refined_query)
     - Record results from second attempt
```

### 3B. FINDINGS TABLE

Build this table as you research:

| Asset ID | Priority | Query Strategy | Query Used | URL 1 | URL 2 | URL 3 | Status |
|----------|----------|----------------|------------|-------|-------|-------|--------|
| ASSET_01 | critical | evidence | {actual query} | [REAL] | [REAL] | - | ✅ |
| ASSET_02 | critical | cultural_ref | {actual query} | [REAL] | [REAL] | [REAL] | ✅ |
| ... | ... | ... | ... | ... | ... | ... | ... |

**Target:** At minimum 2 verified URLs per asset, 3 for `critical` priority assets.

**OUTPUT (50-80 words):**
```
STEP 3 COMPLETE:
- Assets researched: {N}/{total}
- Total URLs found: {count}
- Critical assets: {N} (all with 3+ URLs: ✅/❌)
- Queries refined: {count}
- Failed searches: {count}
```

**EXECUTE:** `write_todos` with STEP 3 as `completed`

---

## STEP 4: VALIDATE URLs

**EXECUTE:** `write_todos` with STEP 4 as `in_progress`

> [!CAUTION]
> **EVERY URL must be validated using `read_url_content`.**
> Dead links MUST be replaced with new searches.

### 4A. Validation Loop

```
FOR EACH url in findings table:
  read_url_content({ url: url })
  IF returns content → mark as ✅ VALID
  IF returns error → mark as ❌ DEAD → search for replacement
```

### 4B. URL Validation Report

| # | Asset | URL | Status | Replacement (if dead) |
|---|-------|-----|--------|----------------------|
| 1 | ASSET_01 | [URL] | ✅ Valid | - |
| 2 | ASSET_01 | [URL] | ❌ 404 | [New URL from new search] |
| ... | ... | ... | ... | ... |

**EXECUTE:** `write_todos` with STEP 4 as `completed`

---

## STEP 5: SOUL ALIGNMENT CHECK

**EXECUTE:** `write_todos` with STEP 5 as `in_progress`

**For each asset's found URLs, verify:**

| Check | Question | Action if Fail |
|:------|:---------|:---------------|
| Tribe resonance | Would THIS specific audience recognize/relate to this imagery? | Refine with tribe-specific qualifiers |
| Cultural accuracy | Does the imagery match the tribe's geographic/cultural context? | Search again with cultural specificity |
| Emotional match | Does the imagery trigger the intended emotional response? | Flag for manual review |
| Value alignment | Does the content contradict any `conscious_soul_values`? | REJECT and replace |

**OUTPUT (30-50 words):**
```
STEP 5 COMPLETE:
- Assets checked: {N}
- Aligned: {N}
- Flagged for review: {N}
- Replaced: {N}
```

**EXECUTE:** `write_todos` with STEP 5 as `completed`

---

## STEP 6: OUTPUT MANIFEST

**EXECUTE:** `write_todos` with STEP 6 as `in_progress`

**CREATE FILE:** `{project_id}_eroll_asset_manifest.json`

```json
{
  "project_id": "{project_id}",
  "archetype": "{archetype from plan}",
  "planning_strategy": "{strategy from plan}",
  "generated_at": "{ISO timestamp}",
  "source_plan": "{project_id}_eroll_asset_plan.json",
  "total_assets": {N},
  "total_verified_urls": {N},
  "assets": [
    {
      "id": "ASSET_01",
      "scene": "{scene from plan}",
      "asset_type": "{type from plan}",
      "query_strategy": "{strategy used}",
      "query_used": "{actual search query}",
      "priority": "critical",
      "verified_urls": [
        {
          "url": "https://example.com/real-article",
          "title": "Article Title",
          "relevance": "Why this URL matches the asset need",
          "validated": true
        }
      ],
      "soul_alignment": "{verification note}",
      "status": "complete"
    }
  ],
  "research_stats": {
    "total_searches_executed": {N},
    "total_urls_found": {N},
    "urls_validated": {N},
    "urls_replaced": {N},
    "soul_alignment_flags": {N}
  }
}
```

**FINAL OUTPUT:**

```
✅ CCF E-ROLL ASSET MANIFEST COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Archetype:           {ARCHETYPE}
Planning Strategy:   {strategy}
Assets Researched:   {N}/{N}
Total Verified URLs: {N}
Soul Alignment:      {N}/{N} passed
Dead Links Replaced: {N}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Files:
├── {project_id}_eroll_asset_plan.json (input)
└── {project_id}_eroll_asset_manifest.json (output)

Ready for visual production engine.
```

**EXECUTE:** `write_todos` with STEP 6 as `completed`

---

## 🔗 NEXT STEPS

These E-Roll assets feed into the visual production pipeline alongside T2I outputs from `/ccf-visual`:

```
ccf-visual output   ──► T2I character scenes  ─┐
                                                ├──► Final Visual Package
This command output  ──► Verified E-Roll assets ─┘
```

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

**END OF CCF-EROLL-RESEARCH COMMAND**
