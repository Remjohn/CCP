# Tech-Spec: FR-CA11-09 — Accountability Check-in System with AFFiNE Visualization

**Created:** 2026-03-24
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / PRD Update v2.0 — Capability Area 11)
**Architecture Reference:** PRD-Update-CA11 §4.3
**Skill Implementation:** `tools/excalidraw_embed.py`, `skills/perception/accountability-visualizer/SKILL.md`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md` (FR27-FR32 CBCS, FR-CBCS-01 through FR-CBCS-14)
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd-update-CA11-quad-platform.md`

---

## 2. Overview

### Problem Statement
The CBCS delivers daily accountability prompts via Telegram (FR27) and processes responses through the agent swarm (Aria, Miriam, Change Talk Detector). But clients receive no visual feedback on their progress. A client completing 28 days of rituals sees the same Telegram interface as a client on Day 1. There's no visual "proof of growth" — no streaks, no milestone charts, no trend lines. This absence of visual reinforcement weakens the accountability loop because humans are visual creatures — abstract behavioral data needs to be *seen* to feel real.

### Solution
FR-CA11-09 extends the existing CBCS accountability loop with a visual feedback layer. Daily Telegram check-in data (energy ratings, habit completion, mood state) is stored in the client's AFFiNE workspace dashboard, and weekly **Excalidraw progress charts** are auto-rendered by `Benjamin` and embedded in the client's AFFiNE Progress Board. Every response simultaneously feeds: (a) the Neo4j Context Premise graph, (b) CPSC readiness calculations, (c) tribe-level ICT distribution, and (d) the client's visual progress dashboard.

### Scope
**In scope:**
- Daily check-in data → AFFiNE client dashboard sync.
- Weekly Excalidraw progress chart generation.
- Progress chart embedding in client's AFFiNE workspace.
- Milestone badge system (7-day streak, 14-day streak, 30-day completion).

**Out of scope:**
- CBCS prompt delivery (FR27-FR32 — already built).
- Context Premise extraction (FR29 — already built).
- Change Talk detection (FR-CBCS-01 — already built).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| FR27 (CBCS Telegram Prompts) | Daily Ritual Delivery | SOURCE — Check-in responses are the raw input. |
| FR-CBCS-09 (Habit Architecture) | Implementation Intentions | CONTEXT — Habit completion data tracked per client. |
| `Benjamin` (Excalidraw Composer) | Visual Pipeline | AGENT — Renders progress charts as `.excalidraw` JSON. |
| `excalidraw_embed.py` | Chart Generation Tool | TOOL — Converts behavioral data into Excalidraw chart structures. |

### Academic Grounding

| Framework | Author | Year | Mechanism |
|---|---|---|---|
| **Progress Principle** | Amabile & Kramer | 2011 | Of all motivators, the single most powerful is making progress in meaningful work. Visual progress tracking amplifies this effect by making incremental gains tangible. |
| **Streak Psychology** | Cialdini (Commitment & Consistency) | 2001 | Once a streak is established, the psychological cost of breaking it increases — visible streaks become self-reinforcing commitment devices. |

### Technical Decisions
1. **Excalidraw over Chart.js:** Progress charts are rendered as `.excalidraw` JSON rather than static images because they can be embedded in AFFiNE (FR-CA11-10) as interactive objects, and they maintain brand consistency with all other CCP visual outputs.
2. **Weekly Rendering + Daily Data:** Data is collected daily but charts render weekly (Sunday night batch). This avoids visual noise from day-to-day fluctuations while providing meaningful trend visibility.

---

## 4. Implementation Plan

### Stage 1: Daily Data Collection
*Agent:* Existing CBCS agent swarm (Aria, Miriam)
*Inputs:* Client's daily check-in response (Telegram).
*Outputs:* Behavioral data point in `accountability_data` Supabase table.

**Steps:**
1. Atlas sends daily ritual prompt via Telegram (existing behavior).
2. Client responds with energy rating (1-10), habit completion (boolean per habit), mood note (free text).
3. Aria extracts structured data; Miriam runs LIWC-22 analysis (existing behavior).
4. Write behavioral data point to `accountability_data` table: `client_id`, `date`, `energy_rating`, `habits_completed` (JSON array), `mood_state`, `streak_count`, `liwc_markers` (JSON).
5. Push daily summary to client's AFFiNE dashboard (via `affine_sync.py`).

### Stage 2: Weekly Chart Generation
*Agent:* `Benjamin` (Excalidraw Composer) via `excalidraw_embed.py`
*Inputs:* 7 days of `accountability_data` for a client.
*Outputs:* `.excalidraw` JSON progress chart.

**Steps:**
1. Sunday night batch: query `accountability_data` for each active client's past 7 days.
2. `excalidraw_embed.py` generates chart structure:
   - **Line Graph:** Energy rating over 7 days (X=day, Y=rating).
   - **Streak Counter:** Current consecutive completion streak with milestone badges (🥉 7-day, 🥈 14-day, 🥇 30-day).
   - **Habit Grid:** Matrix of habits × days with completion indicators (✅/❌).
   - **Mood Trend:** Excalidraw freehand-style line showing emotional trajectory.
3. `Benjamin` renders the chart using CCP-branded colors from the coach's theme.
4. Chart JSON is stored in S3 and pushed to client's AFFiNE Progress Board via `affine_sync.py`.

### Stage 3: Milestone Badge System
*Agent:* `Noémie` (Content Gating Agent — extended with milestone logic)
*Inputs:* `streak_count` from `accountability_data`.
*Outputs:* Badge assignment + Telegram celebration message + AFFiNE badge display.

**Steps:**
1. After each daily check-in, check `streak_count` against milestone thresholds (7, 14, 21, 30, 60, 90).
2. On milestone hit: send celebration message via Telegram (using coach's Voice DNA tone).
3. Add badge to client's AFFiNE dashboard.
4. If streak breaks: reset counter, send gentle re-engagement prompt (not punitive).

---

## 5. Primary Output Schema

**Data Object:** Accountability Visual Chart Payload (`DEP-ENG-079` PROPOSED)

```json
{
  "client_id": "uuid-client-042",
  "weekly_chart": {
    "chart_url": "s3://JP/excalidraw/progress_uuid-client-042_week12.json",
    "week_number": 12,
    "energy_trend": [7, 6, 8, 7, 9, 8, 7],
    "habits_completed_rate": 0.85,
    "current_streak": 23,
    "milestone_badges": ["7_day", "14_day", "21_day"],
    "mood_trajectory": "ascending"
  },
  "daily_data_point": {
    "date": "2026-03-24",
    "energy_rating": 8,
    "habits_completed": ["meditation", "journaling"],
    "habits_missed": ["exercise"],
    "mood_state": "Discovery",
    "streak_count": 23
  }
}
```

---

## 6. Backward Compatibility Fallback
If Excalidraw chart generation fails, the daily data is still collected and stored in Supabase. The AFFiNE dashboard shows raw data in a table view (fallback). Charts are queued for retry on next batch. Telegram CBCS loop is unaffected in any failure scenario.

---

## 7. Tasks

- [ ] **Task 1:** Create Supabase `accountability_data` table.
- [ ] **Task 2:** Write `excalidraw_embed.py` chart generation functions (line graph, habit grid, streak counter, mood trend).
- [ ] **Task 3:** Build progress chart template for `Benjamin` (CCP-branded, responsive to coach theme).
- [ ] **Task 4:** Wire daily CBCS check-in completion to `accountability_data` write + AFFiNE sync.
- [ ] **Task 5:** Implement Sunday night batch cron for weekly chart generation.
- [ ] **Task 6:** Implement milestone badge system with Telegram delivery.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Daily Data Capture):** Client completes a check-in via Telegram. Assert `accountability_data` entry is created with correct energy, habits, mood.
- [ ] **AC2 (Weekly Chart):** After 7 days of data, trigger chart generation. Assert `.excalidraw` JSON contains line graph, habit grid, streak counter, and mood trend.
- [ ] **AC3 (Milestone Badge):** Client reaches 7-day streak. Assert Telegram celebration message is sent and badge appears in AFFiNE dashboard.
- [ ] **AC4 (Streak Reset):** Client misses a day. Assert streak counter resets and re-engagement prompt fires (not punitive).
- [ ] **AC5 (AFFiNE Dashboard Sync):** Assert daily data point appears in client's AFFiNE dashboard within 60 seconds of check-in completion.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR27-FR32 (CBCS) | Internal | Daily ritual delivery is the input source. |
| FR-CA11-03 (Client Workspace) | Internal | Dashboard and Progress Board must exist. |
| FR-CA11-02 (AFFiNE Sync) | Internal | Push mechanism. |
| `Benjamin` (Excalidraw Composer) | Internal | Chart rendering. |

---

## 10. Testing Strategy

### Unit Tests
- **Chart Generation:** Pass 7 days of known data. Assert chart JSON has correct nodes, edges, and color values.
- **Streak Calculation:** Test streak across 30 days with 2 breaks. Assert correct streak counts after each day.

### Integration Tests
- **28-Day Simulation:** Simulate 28 days of check-ins for a test client. Assert 4 weekly charts generated, milestones fired at 7/14/21 days, AFFiNE dashboard updated daily.
