---
name: ccf-radar
description: "Weekly Subsystem 1 — Run Intelligence Radar to find friction points across 4 rotated pillars"
---

# /ccf-radar {client_name}

// turbo-all

> **SKILLS_BASE:** `ccf-26/skills/ccf/`
> **SKILL:** `content/intelligence-radar/SKILL.md`
> **TOOLS:** `tools/google_trends_wrapper.py`, `tools/sentiment_wrapper.py`

**Objective:** Select 4 pillars via rotation algorithm, scan for trending signals, compute sentiment alignment, and output `intelligence_radar.json` with 24+ friction points. This is the first subsystem in the weekly content engine.

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify project_context.json exists", status: "pending" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Intelligence Radar SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: ROTATE - Run pillar rotation algorithm, select 4 pillars", status: "pending" },
    { id: "step-4", description: "STEP 4: SCAN - Execute multi-source sweep per pillar", status: "pending" },
    { id: "step-5", description: "STEP 5: SCORE - Compute sentiment alignment for friction points", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write intelligence_radar.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Minimum 6 friction points per pillar", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml + rotation metadata", status: "pending" }
  ]
});
```

---

## STEP 1: PRE-FLIGHT

Mark step-1 `in_progress`.

| Check | Path | If Missing |
|-------|------|------------|
| 1 | `intelligence/project_context.json` | STOP → Run `/ccf-pillar-build` |
| 2 | `config.yaml → sessions.setup.pillar_build.status == "complete"` | STOP → Run `/ccf-pillar-build` |
| 3 | `RAPIDAPI_KEY` environment variable | WARN → Virality Score defaults to 5 for all pillars |
| 4 | `MEANINGCLOUD_API_KEY` environment variable | WARN → Skip sentiment alignment scoring |

**Determine week_id:** Calculate from current date (e.g., `2026-W08`).
**Create output directory:** `intelligence/weekly/{week_id}/`

Mark step-1 `completed`.

---

## STEP 2: LOAD SKILL

Mark step-2 `in_progress`.

1. Read FULL: `ccf-26/skills/ccf/content/intelligence-radar/SKILL.md`
2. **Internalize:** Pillar Rotation Algorithm, Multi-Source Sweep protocol, Sentiment Alignment formula
3. Read `intelligence/project_context.json` — load all 12 pillars with their 7 layers

Mark step-2 `completed`.

---

## STEP 3: ROTATE — Select 4 Pillars

Mark step-3 `in_progress`.

**For each of 12 pillars, compute Selection Score:**

```
Selection Score = (Variety × 0.40) + (Virality × 0.35) + (Coach Energy × 0.25)
```

1. **Variety Score:** Check `rotation_metadata.last_used_week` vs current week
2. **Virality Score:** Use `tools/google_trends_wrapper.py interest "{keywords}"` for each pillar's `layer_5_cultural_hooks.google_trends_keywords`
3. **Coach Energy Score:** Check `weekly_history` for recent engagement data

**Present the rotation table:**

| Pillar | Variety | Virality | Energy | Total | Selected? |
|--------|:-------:|:--------:|:------:|:-----:|:---------:|
| pillar_01 | 10 | 7 | 5 | 7.95 | ✅ |
| ... | ... | ... | ... | ... | ... |

**Select top 4** (or 3 + 1 override if breaking news matches a pillar's news_triggers).

Mark step-3 `completed`.

---

## STEP 4: SCAN — Multi-Source Sweep

Mark step-4 `in_progress`.

**For EACH of the 4 selected pillars:**

### 4A: Temporal Relevance
- Use `web_search` with pillar's `google_trends_keywords` + "news today"
- Use `tools/google_trends_wrapper.py related "{keyword}"` for related queries
- Record: headline, source URL, date, relevance to pillar

### 4B: Cultural Relevance
- Use `web_search` with `"site:reddit.com/{subreddit}"` for each pillar's subreddits
- Search for trending discussion around pillar's hashtags
- Record: post title, engagement indicators, URL, sentiment tone

### 4C: Personal Relevance Cross-Reference
- For each temporal/cultural signal found, score against pillar's Layer 4:
  - Does it touch `primary_pain`? (+3)
  - Does it threaten `primary_desire`? (+3)
  - Does it activate `hidden_fear`? (+4)
  - Total personal relevance: 0-10

**Target:** 6-8 friction points per pillar (24-32 total).

Mark step-4 `completed`.

---

## STEP 5: SCORE — Sentiment Alignment

Mark step-5 `in_progress`.

**For top friction points per pillar:**

1. Use `tools/sentiment_wrapper.py analyze "{signal_text}"` on key signals
2. Compare sentiment result against pillar's `layer_6_contrarian_position.counter_stance`
3. Compute alignment: `|public_sentiment - coach_position| × emotional_intensity`
4. Score each friction point's sentiment alignment (0-10)

**If MEANINGCLOUD_API_KEY not available:**
- Use manual sentiment assessment based on language analysis
- Score based on obvious sentiment indicators (fear words, excitement words, etc.)

Mark step-5 `completed`.

---

## STEP 6: EMIT

Mark step-6 `in_progress`.

**CREATE FILE:** `intelligence/weekly/{week_id}/intelligence_radar.json`

Follow the output schema from the SKILL.md exactly:
- `week_id`, `scan_date`
- `selected_pillars` array with rotation scores + friction points per pillar
- Each friction point: id, signal, source_type, source_url, emotional_valence, relevance_score, sentiment_alignment, alignment_explanation, suggested_angle, trigger_archive_match
- `api_calls_made` tracking
- `total_friction_points` count

Mark step-6 `completed`.

---

## STEP 7: VALIDATE

Mark step-7 `in_progress`.

| # | Check | Pass/Fail |
|---|-------|-----------|
| 1 | 4 pillars selected | |
| 2 | Each pillar has ≥6 friction points | |
| 3 | Each friction point has source URL | |
| 4 | Each friction point has sentiment alignment score | |
| 5 | No duplicate friction points across pillars | |
| 6 | Valid JSON structure | |

Mark step-7 `completed`.

---

## STEP 8: CHECKPOINT

Mark step-8 `in_progress`.

1. Update `config.yaml`:
```yaml
sessions:
  weekly:
    "{week_id}":
      radar:
        status: "complete"
        timestamp: "{ISO date}"
        pillars_scanned: 4
        total_friction_points: {N}
```

2. Update `project_context.json`: Set `rotation_metadata.last_used_week` for each selected pillar.

**OUTPUT:**
```
✅ INTELLIGENCE RADAR COMPLETE (Week {week_id})
- Pillars scanned: {pillar names}
- Friction points found: {N} total
- Top friction: "{highest scoring signal}"
- NEXT: /ccf-question {client_name}
```

Mark step-8 `completed`.

---

## 🔗 NEXT: `/ccf-question {client_name}`
