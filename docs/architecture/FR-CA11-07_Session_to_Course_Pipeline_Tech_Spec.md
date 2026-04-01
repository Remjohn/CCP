# Tech-Spec: FR-CA11-07 — Session-to-Course Auto Pipeline

**Created:** 2026-03-24
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / PRD Update v2.0 — Capability Area 11)
**Architecture Reference:** PRD-Update-CA11 §4.2
**Skill Implementation:** `skills/strategy/session-to-course/SKILL.md`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md` (FR32 Atlas Roadmap, FR-CBCS-04 ICT Mapper)
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd-update-CA11-quad-platform.md`

---

## 2. Overview

### Problem Statement
Coaches deliver 4-8 coaching sessions per week. Each contains structured pedagogical content — explanations, exercises, frameworks — but this expertise dies after the session ends. The client gets a 60-minute call; the coach gets nothing reusable. Creating a course from sessions requires a coach to re-record, re-structure, and re-edit — duplicating effort that already happened live.

### Solution
FR-CA11-07 converts a **series of OBS-recorded coaching sessions** into a **structured, drip-fed course** delivered through the client's AFFiNE workspace and Telegram. Multiple Session Intelligence Reports (FR-CA11-05) are grouped by topic cluster, sequenced chronologically with chapter timestamps, and delivered as a learning journey calibrated to the client's Atlas roadmap rhythm (4+1+2 structure). The coach never sits down to "create a course" — their sessions retroactively become the course.

### Scope
**In scope:**
- Grouping multiple Session Intelligence Reports into course chapters.
- Chapter creation with timestamps linking to key moments.
- Drip-fed delivery via Telegram + AFFiNE workspace.
- Drip schedule calibration to Atlas roadmap (active days / reflection days / rest days).

**Out of scope:**
- Individual session processing (FR-CA11-05).
- Course video rendering (FR-CA11-12 — that's the visual production layer).
- Learning path DAG construction (FR-CA11-04 — that's the categorization layer).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| FR-CA11-05 (Session Recap) | Session Intelligence Reports | SOURCE — Each session recap becomes a course chapter candidate. |
| FR-CA11-04 (Learning Path Builder) | Journey Construction | CONSUMER — Course chapters are registered as learning path content. |
| FR32 (Atlas Roadmap) | 4+1+2 Structure | CONSTRAINT — Drip schedule respects active/reflection/rest day structure. |
| `Gabrielle` (Learning Path Agent) | Course Assembly | AGENT — Groups sessions, builds chapter structure, schedules drips. |

### Technical Decisions
1. **Automatic Grouping by Topic Cluster:** Sessions are grouped using the `topic_clusters` field from Session Intelligence Reports. Sessions sharing ≥2 topic clusters are candidates for the same course.
2. **Drip = Atlas Calendar:** Drips fire on the client's active days (Mon-Thu in default 4+1+2). No drip on reflection days (to avoid cognitive overload during integration). No drip on rest days (respecting recovery).
3. **Chapter ≠ Full Session:** A chapter is a curated subset of a session — specifically the key insights and action items extracted by `Lena`, not a 60-minute replay. This respects the client's time while preserving the pedagogical value.

---

## 4. Implementation Plan

### Stage 1: Course Assembly
*Agent:* `Gabrielle` (Learning Path Agent)
*Inputs:* Multiple Session Intelligence Reports for the same coach.
*Outputs:* Course definition (ordered chapters with timestamps).

**Steps:**
1. Query `session_intelligence` for all sessions belonging to a coach.
2. Group by overlapping `topic_clusters` (sessions sharing ≥2 clusters form a course candidate).
3. Order sessions chronologically within each group.
4. For each session in the group, extract chapter content: title (from session's primary topic), key timestamps, curated insights, action items.
5. Store course definition in `learning_path_registry` with `content_type = course_chapter`.

### Stage 2: Drip Schedule Configuration
*Agent:* `Gabrielle` + `Atlas`
*Inputs:* Client's current `atlas_roadmap` (4-week calendar), course chapter count.
*Outputs:* Drip schedule (specific dates/times for each chapter delivery).

**Steps:**
1. Query client's Atlas roadmap for active days in the current 4-week cycle.
2. Map course chapters to active days sequentially (1 chapter per active day).
3. Set drip time to client's preferred notification time (from CBCS preference profile).
4. Store drip schedule in Supabase `drip_schedule` table.

### Stage 3: Drip Delivery
*Agent:* Scheduled cron + Telegram bot + `affine_sync.py`
*Inputs:* Drip schedule trigger.
*Outputs:* Telegram message + AFFiNE content block.

**Steps:**
1. Cron checks `drip_schedule` for today's drips.
2. For each due drip: send chapter snippet via Telegram (key insight + action item + link to full lesson in AFFiNE).
3. Push full chapter content to client's AFFiNE Learning Library (via `affine_sync.py`).
4. Update `learning_progress` table with `delivered_at` timestamp.
5. If client engages with the Telegram drip (clicks link, responds), update `learning_progress` with `engaged_at`.
6. Write Receipt Chain Guard entry per FR47 DEP-ENG-041 schema.

---

## 5. Primary Output Schema

**Data Object:** Course Definition Document (`DEP-ENG-077` PROPOSED)

```json
{
  "course_id": "uuid-course-001",
  "coach_id": "uuid-coach-001",
  "title": "Breaking the Approval Cycle — A 5-Session Journey",
  "topic_clusters": ["external_validation", "self_worth", "boundaries"],
  "chapters": [
    {
      "chapter_number": 1,
      "session_id": "uuid-session-003",
      "title": "Recognizing the Pattern",
      "key_timestamps": ["00:14:32", "00:28:15"],
      "key_insight": "External validation creates dependency, not confidence.",
      "action_item": "When I catch myself seeking approval, I will pause and write down what I actually want."
    }
  ],
  "total_chapters": 5,
  "drip_schedule": {
    "client_id": "uuid-client-042",
    "chapter_delivery_dates": ["2026-03-25", "2026-03-26", "2026-03-27", "2026-03-28", "2026-04-01"],
    "delivery_time": "09:00",
    "timezone": "Europe/Paris"
  }
}
```

---

## 6. Backward Compatibility Fallback
If course assembly fails (insufficient sessions, no topic cluster overlap), the individual Session Intelligence Reports remain accessible as standalone content in the coach's AFFiNE workspace. No data is lost — the sessions simply aren't grouped into a course. The system logs the failure reason and retries when new sessions are added.

---

## 7. Tasks

- [ ] **Task 1:** Implement topic-cluster-based session grouping algorithm in `Gabrielle`.
- [ ] **Task 2:** Create Supabase `drip_schedule` table.
- [ ] **Task 3:** Implement drip schedule calculator (Atlas roadmap integration).
- [ ] **Task 4:** Implement drip delivery cron job (Telegram + AFFiNE push).
- [ ] **Task 5:** Track engagement on drip messages (`learning_progress` update).

---

## 8. Acceptance Criteria

- [ ] **AC1 (Auto-Grouping):** Record 5 sessions covering overlapping topics. Assert `Gabrielle` groups them into a course.
- [ ] **AC2 (Drip Scheduling):** Assert drip schedule aligns with client's Atlas roadmap active days (no drips on reflection/rest days).
- [ ] **AC3 (Telegram Delivery):** Assert Telegram drip contains chapter snippet + AFFiNE link.
- [ ] **AC4 (AFFiNE Delivery):** Assert full chapter content appears in client's Learning Library on drip day.
- [ ] **AC5 (Engagement Tracking):** Client clicks drip link. Assert `learning_progress` records `engaged_at`.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR-CA11-05 (Session Recap) | Internal | Source of Session Intelligence Reports. |
| FR-CA11-04 (Learning Path Builder) | Internal | Course chapters registered in learning paths. |
| FR32 (Atlas Roadmap) | Internal | Drip schedule calibration. |
| FR-CA11-02 (AFFiNE Sync) | Internal | AFFiNE delivery. |

---

## 10. Testing Strategy

### Unit Tests
- **Grouping Algorithm:** Pass 8 sessions with known topic clusters. Assert correct grouping (3 courses: 3+3+2 sessions).

### Integration Tests
- **Full Lifecycle:** Record 3 sessions → generate recaps → auto-group into course → schedule drips → deliver Day 1 drip → verify Telegram + AFFiNE.
