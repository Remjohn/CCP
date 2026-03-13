# Tech-Spec: FR42 — Publer Automated Performance Sync (DEP-ENG-037)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v4.0 / Unified PRD v3.1)
**Architecture Reference:** CE_Data_Infrastructure_v1.0, PRD FR42
**Skill Implementation:** `skills/orchestration/publer_sync.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\prd TO UPDATE.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CE_Data_Infrastructure_v1.0.docx.md`

---

## 2. Overview

### Problem Statement
An AI production system that doesn't ingest its own performance data operates in a completely open loop—producing volume without compounding intelligence. If coaches must manually copy/paste TikTok reach or LinkedIn engagement rates back into the system, the data simply won't be collected, leading to system stagnation and the eventual failure of the Content Factory.

### Solution
FR42 defines the **Publer Automated Performance Sync (DEP-ENG-037)**. By connecting each coach's social platforms to a centralized Publer workspace, a Python background worker automates the entire feedback lifecycle via 4 core triggers. It schedules the post, confirms publication, and automatically ingests live metrics at the 48-hour, 7-day, and 30-day marks. These metrics are written directly to the Supabase `content_performance` table and surfaced on the coach's Notion dashboard, permanently closing the learning loop.

### Scope
**In scope:**
- The 4 automation triggers (Scheduling, Publication Confirmation, 48h Sync, 7/30-day Snapshots).
- The `content_performance` Supabase database schema.
- Notion API synchronization.
- Publer API implementation rules.

**Out of scope:**
- The actual *evaluation* of the data. (This handles pure retrieval; FR43 handles the Data Analyst Agent evaluation).
- Video rendering. (The file URL is assumed to be ready in Supabase).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-037` | Publer Sync Workflows | OUTPUT — The 4 sub-routines managing the data lifecycle. |
| Supabase `videos` table | Content Queue | INPUT — Where the script/video asset waits for scheduling. |
| Supabase `fingerprint_archive` | Archive Key | DEPENDENCY — `Universal_Asset_ID` links the raw asset to its performance metrics. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Closed-Loop System Dynamics** | Forrester | 1961 | Establishes that without continuous, high-fidelity feedback loops, complex systems drift into chaotic output over time. This data infrastructure explicitly closes the loop, shifting the CCP from an open-loop generator to a closed-loop learner. |

### Technical Decisions
1. **Single Point of Authentication:** Platforms (TikTok, IG, LinkedIn) constantly update API requirements and geographical limits. By routing *all* activity through Publer, the CCP maintains one stable REST API integration, outsourcing platform API maintenance entirely.
2. **Deterministic Milestones:** Performance data is inherently a moving target. To accurately evaluate "what worked," the Data Analyst needs fixed horizons, which is why the background worker grabs explicit snapshots at 48h, 7d, and 30d, rather than just continuously overwriting a "current reach" integer.

---

## 4. Implementation Plan

### Stage 1: Trigger 1 — Content Scheduling
*Component:* Sync Action 1
*Trigger:* Supabase Webhook: `videos.status = READY_TO_PUBLISH`
*Action:*
1. Parses `Universal_Asset_ID`, `video_file_url`, `caption`, and platform targets.
2. Calls `POST https://app.publer.com/api/v1/post`.
3. Receives `scheduled_post_id`.
4. Writes `publer_post_id` and `scheduled_at` back to the Supabase `videos` row.
*Failure Condition:* Publer rejects the media URL due to format. The script catches the error and flags `status = FAILED_TO_SCHEDULE`.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

### Stage 2: Trigger 2 — Publication Confirmation
*Component:* Sync Action 2
*Trigger:* Publer Webhook: Post Status changes to `PUBLISHED`
*Action:*
1. Receives `platform_post_id`, `published_url`, and `published_at` timestamp.
2. Updates Supabase `videos` row mapping the `.publer_post_id`.
3. Calls Notion API to create a new row in the Coach's "Published Content" database, prepopulating the URL and status.
*Failure Condition:* Notion API is down; creation row is queued in a retry loop to prevent data desync.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

### Stage 3: Trigger 3 — 48-Hour Performance Retrieval
*Component:* Sync Action 3 (CRON)
*Trigger:* Scheduled to run every 6 hours.
*Action:*
1. Queries Supabase: `SELECT * FROM videos WHERE published_at < NOW() - 48h AND first_insights_collected = false`
2. Iterates over results, calling `GET /api/v1/analytics/post_insights?post_id={publer_post_id}`.
3. Inserts a new row into the Supabase `content_performance` table.
4. Updates `videos.first_insights_collected = true`.
5. Pushes the metrics to the specific row in the Notion "Published Content" database.
*Failure Condition:* Post was deleted natively on the platform. Publer returns 404. The script flags `is_active = false` and halts tracking.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

### Stage 4: Trigger 4 — 7-Day & 30-Day Snapshots
*Component:* Sync Action 4 (CRON)
*Trigger:* Scheduled daily.
*Action:*
1. Queries Supabase for posts published exactly 7 days ago AND 30 days ago.
2. Calls the Publer Post Insights endpoint for each.
3. Mutates the Supabase `content_performance` table, specifically updating the JSONB sub-columns `day_7_snapshot` and `day_30_snapshot`.
4. Notion is updated with the `7-Day Score` (Engagement Rate).
*Failure Condition:* API Rate limit exceeded (100 req / 2 min). The script applies a 120-second wait block and retries the batch.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

---

## 5. Primary Output Schema (DEP-ENG-037)

**Schema Name:** `content_performance_row_init.json` (Mapped to the Supabase Table insert)

```json
{
  "Universal_Asset_ID": "JP-CCF-20260312-001-CAROUSEL",
  "publer_post_id": "pub_998877",
  "platform": "instagram",
  "platform_post_url": "https://instagram.com/p/xhs8323",
  "published_at": "2026-03-12T14:00:00Z",
  "reach": 14500,
  "impressions": 16200,
  "saves": 450,
  "shares": 120,
  "comments": 45,
  "likes": 800,
  "video_views": 10200,
  "engagement_rate": 0.0975,
  "first_insights_at": "2026-03-14T14:00:00Z",
  "day_7_snapshot": null,
  "day_30_snapshot": null
}
```

---

## 6. Backward Compatibility Fallback
## 6. Backward Compatibility Fallback
If the Publer native API connection breaks (e.g., token expiration), the pipeline automatically alerts the System Operator via Telegram. The pipeline halts moving `READY_TO_PUBLISH` videos to the live state. Any pending performance snapshots are paused and added to a strict retry queue; because they query historical analytics, a 3-day outage will not result in permanent data loss, it merely delays the Data Analyst's weekly execution.

---

## 7. Tasks

- [ ] **Task 1:** Execute the Supabase database migrations to create the `content_performance` table and the `coach_config` table (housing Notion and Publer workspace ID maps).
- [ ] **Task 2:** Build Sync Action 1 (Scheduling POST) using HTTP Requests and Publer Bearer auth in Python.
- [ ] **Task 3:** Build Sync Action 2 (Publer Webhook receiver → Supabase `published_at` update → Notion API Page Create).
- [ ] **Task 4:** Build Sync Action 3 (48h Fetch CRON loop), mapping the output array variables (`reach`, `saves`, `shares`, `likes`, `comments`) to the Supabase Postgres insert payload.
- [ ] **Task 5:** Build Sync Action 4 (7/30-day Snapshot CRON loop), compiling the metrics into the required JSONB schema and updating the exact target row.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Scheduling Handshake):** Trigger a row update in Supabase `videos` to `READY_TO_PUBLISH`. Assert that the sync worker receives the webhook, successfully transmits it to Publer, and writes a valid `publer_post_id` back to the exact Supabase row within 5 seconds. *Failure Example:* The script fires the post to Publer, but fails to write the ID back to Supabase, permanently breaking the tracking link.
- [ ] **AC2 (Metric Mathematical Rollup):** Execute a fetch for Workflow 3 on an active post. Assert that the `engagement_rate` variable calculation accurately sums `(saves + shares + comments + likes) / reach` before writing the decimal to Supabase. *Failure Example:* The system calculates engagement using strictly likes, misrepresenting true algorithmic impact.
- [ ] **AC3 (Notion Page Genesis):** Fire a mocked "Publish Confirmed" webhook from Publer. Assert that the sync worker successfully creates a new row in the Coach's Notion "Published Content" database, and the ID maps correctly via the `coach_config` table. *Failure Example:* The post is assigned to the wrong coach's Notion workspace, violating ADR-01 multi-tenant architecture. 
- [ ] **AC4 (Idempotent DB Updates):** Fire the 7-Day snapshot CRON twice sequentially. Assert that the second run returns an `analyst_reviewed = false` bypass or identically overwrites the `day_7_snapshot` without duplicating the row in `content_performance`. *Failure Example:* Supabase creates duplicate performance rows for the same `Universal_Asset_ID`.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| Publer Workspace API | External | Requires the `Business` tier API key mapped to the CCP central server environment variables. |
| Supabase `fingerprint_archive` | Internal | Provides the crucial `Universal_Asset_ID` key linking narrative parameters to raw mathematical performance. |
| Notion Integration Token | External | Required for the pipeline to mutate the coach-facing dashboard pages. |

---

## 10. Testing Strategy

### Unit Tests
- **Formula Verification Test:** Submit a mock JSON array of analytics to the Pydantic data transformation block. Assert the output schema correctly translates Publer's proprietary naming conventions `{"reactions": 10}` to the CCP schema `{"likes": 10}`.

### Integration Tests
- **The Lifecycle Simulation:** Using a sandbox Publer workspace:
  1. Trigger Sync Action 1 with a mock video.
  2. Mock the publication confirmation webhook.
  3. Validate the Notion DB row appears.
  4. Artificially advance the server time by 48 hours and fire Sync Action 3. 
  5. Assert the Supabase table `content_performance` reflects the metrics fetched from the sandbox.

### Safety Tests (ADR-01 Quarantine Security)
- **Token Bleed Check:** Attempt to query a post using Coach A's `Workspace_ID` with Coach B's `Notion_Integration_Token`. Assert the Python router explicitly rejects the cross-contamination attempt before initiating the HTTP request.
