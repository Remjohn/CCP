# Tech-Spec: FR-CA11-18 — Conscious Social Scheduling & Performance Analysis

**Created:** 2026-03-25
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / PRD Update v2.0 — Capability Area 11)
**Architecture Reference:** PRD-Update-CA11 §4.5 (FR-CA11-18), ADR-07
**Skill Implementation:** `tools/social_scheduler.py` + self-hosted scheduler (Postiz/Mixpost Docker)
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd-update-CA11-quad-platform.md` (§4.5 FR-CA11-18)
- `d:\Work\The Conscious Coaching Factory\docs\features\FB_Conscious_Social_Scheduling.md` (FB-STUDIO-01)

---

## 2. Overview

### Problem Statement
The current CCP architecture relies on Publer (FR43) as an external SaaS for social media scheduling. This creates three problems: (1) performance data stays in Publer's database — CRAL agents can't access engagement metrics for evidence-based content optimization, (2) no data sovereignty — Publer's API rate limits and pricing control our access to our own data, (3) no native workflow integration — content from the CMF Pipeline must be manually uploaded to Publer.

### Solution
FR-CA11-18 replaces Publer with a self-hosted open-source social media scheduler (Postiz or Mixpost) running as a Docker container on AWS. A FastAPI integration layer (`social_scheduler.py`) connects the CMF Pipeline outputs to the scheduler, handles post queuing, and ingests engagement metrics back into Supabase for CRAL feedback loops. An AFFiNE "Social Media OS" template renders performance dashboards.

### Scope
**In scope:**
- Self-hosted scheduler deployment (Docker on AWS).
- `social_scheduler.py` integration layer (CMF→scheduler and scheduler→Supabase).
- Performance metric ingestion (6h/24h/48h/168h collection cycles).
- AFFiNE Social Media OS template (performance dashboards, best content, comparisons).
- CRAL feedback loop (performance data feeds content optimization).

**Out of scope:**
- Social media API authentication (handled by scheduler's native OAuth flows).
- Content creation (handled by CMF Pipeline).
- Paid ad management.

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-075` | Scheduler Deployment | INFRASTRUCTURE — Self-hosted Docker container on AWS. |
| `DEP-ENG-076` | Post Queuing Integration | INTEGRATION — `social_scheduler.py` pushes CMF outputs to scheduler API. |
| `DEP-ENG-077` | Performance Ingestion | DATA — Polls scheduler API for engagement metrics, stores in Supabase. |
| `DEP-ENG-078` | Social Media OS Template | UI — AFFiNE workspace template for performance visualization. |
| `DEP-ENG-079` | CRAL Feedback Loop | INTELLIGENCE — Performance data feeds CRAL evidence pool for content strategy. |
| `DEP-ENG-041` | Receipt Chain Guard | INTEGRATION — Receipt written on successful post publish. |

### Academic Grounding

| Framework | Author | Year | Mechanism |
|---|---|---|---|
| **CRAL Evidence Hierarchy** | CCP Internal | 2025 | Social performance metrics are Tier 2 evidence (behavioral outcome data). They feed back into the CRAL evidence pool to shift content strategy toward what demonstrably works. |
| **Feedback Loop Closure** | Meadows (Systems Thinking) | 2008 | Without closing the loop from content creation → audience response → strategy adjustment, the system operates open-loop. Performance tracking closes this loop with quantitative data. |

### Technical Decisions
1. **Postiz over Mixpost:** Both are open-source, self-hosted. Decision should be made at deployment time based on: number of supported platforms, API completeness, community activity. Both support the required platforms (Instagram, YouTube, TikTok, LinkedIn, X).
2. **Polling over Webhooks for Metrics:** Social platforms don't push engagement metrics via webhooks. `social_scheduler.py` polls the scheduler API on a schedule (6h, 24h, 48h, 168h post-publish) and writes results to Supabase.
3. **Best-Performing Content Highlighting:** Posts that exceed 2x the coach's rolling average engagement score are flagged as "top performers" in the AFFiNE dashboard. CRAL agents can reference these when planning future content batches.

---

## 4. Implementation Plan

### Stage 1: Scheduler Deployment
*Agent:* Infrastructure
*Outputs:* Running Postiz/Mixpost instance on AWS.
*DEP-ID:* `DEP-ENG-075`

**Steps:**
1. Evaluate Postiz and Mixpost for: platform support (Instagram, YouTube, TikTok, LinkedIn, X), API documentation, Docker image quality.
2. Deploy chosen scheduler as Docker container on AWS EC2 via Dockploy.
3. Configure OAuth connections for each social platform.
4. Verify manual post creation and scheduling works via the scheduler's native UI.

### Stage 2: Post Queuing Integration
*Agent:* `Sofia` (Social Performance Analyst)
*Inputs:* CMF Pipeline output (post-ready content: caption, media URLs, hashtags, platform targets).
*Outputs:* Scheduled posts in the scheduler's queue.
*DEP-ID:* `DEP-ENG-076`

**Steps:**
1. Build `social_scheduler.py` FastAPI service with endpoint: `POST /social/queue { coach_id, content_id, caption, media_urls, platforms, scheduled_time }`.
2. On CMF Pipeline completion (when content passes Triple-Pass Validation Gate), automatically call `/social/queue` with the approved content.
3. Map CMF content types to platform requirements: max caption length, image/video format requirements, hashtag limits.
4. Store queued post in `social_posts` table with `status = 'scheduled'`.
5. On publish event (from scheduler webhook or polling): update `social_posts.status = 'published'`, write receipt to Receipt Chain Guard.

### Stage 3: Performance Metric Ingestion
*Agent:* `Sofia`
*Inputs:* Scheduler API engagement data.
*Outputs:* `social_performance` rows in Supabase.
*DEP-ID:* `DEP-ENG-077`

**Steps:**
1. Build scheduled ingestion task (cron or Celery beat): runs at 6h, 24h, 48h, 168h after each post's `published_at` timestamp.
2. For each published post: query scheduler API for engagement metrics (views, likes, shares, comments, saves, click-through rate).
3. Store metrics in `social_performance` table: one row per post per collection cycle.
4. Calculate rolling averages per coach per platform (30-day window) for baseline comparison.
5. Flag posts exceeding 2x rolling average as "top performers" (`is_top_performer = true`).

### Stage 4: AFFiNE Social Media OS Template
*Agent:* `Pierre` (AFFiNE Workspace Orchestrator)
*Inputs:* `social_posts` and `social_performance` data via AFFiNE Sync Service.
*Outputs:* AFFiNE workspace page with embedded dashboards.
*DEP-ID:* `DEP-ENG-078`

**Steps:**
1. Create AFFiNE template page: "Social Media OS" with sections:
   - **Post Calendar:** Calendar view of scheduled and published posts.
   - **Performance Dashboard:** Table/chart view of recent posts with engagement metrics.
   - **Top Performers:** Highlighted cards for posts flagged as top performers.
   - **Cross-Platform Comparison:** Side-by-side platform performance averages.
   - **Content Type Analysis:** Performance breakdown by content type (video, image, carousel, text).
2. Push template to each coach's workspace via AFFiNE Sync Service.
3. Schedule periodic sync (every 6 hours) to update dashboard data.

---

## 5. Data Model

```sql
CREATE TABLE social_posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    coach_id UUID NOT NULL REFERENCES coaches(id),
    content_id UUID, -- FK to CCF content/Fingerprint ID
    platform VARCHAR(30) NOT NULL, -- instagram, youtube, tiktok, linkedin, x
    caption TEXT,
    media_urls JSONB, -- [{url, type: image/video}]
    hashtags JSONB, -- ["#coaching", "#wellness"]
    scheduler_post_id VARCHAR(255), -- external ID from Postiz/Mixpost
    scheduled_at TIMESTAMP WITH TIME ZONE,
    published_at TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) DEFAULT 'draft', -- draft, scheduled, published, failed
    receipt_chain_id UUID REFERENCES receipt_chain(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE social_performance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID NOT NULL REFERENCES social_posts(id),
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    saves INTEGER DEFAULT 0,
    ctr DECIMAL(5,4) DEFAULT 0, -- click-through rate
    engagement_score DECIMAL(8,2) DEFAULT 0, -- weighted composite
    collection_cycle VARCHAR(10) NOT NULL, -- 6h, 24h, 48h, 168h
    is_top_performer BOOLEAN DEFAULT FALSE,
    collected_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_social_posts_coach ON social_posts(coach_id);
CREATE INDEX idx_social_posts_status ON social_posts(status);
CREATE INDEX idx_social_performance_post ON social_performance(post_id);
CREATE INDEX idx_social_performance_top ON social_performance(is_top_performer) WHERE is_top_performer = TRUE;
```

---

## 6. Tasks

- [ ] **Task 1:** Evaluate and select scheduler (Postiz vs Mixpost). Deploy Docker container on AWS.
- [ ] **Task 2:** Build `social_scheduler.py` with `POST /social/queue` endpoint.
- [ ] **Task 3:** Wire CMF Pipeline completion → auto-queue to social scheduler.
- [ ] **Task 4:** Build performance metric ingestion (cron: 6h/24h/48h/168h polling).
- [ ] **Task 5:** Build top performer detection (2x rolling average threshold).
- [ ] **Task 6:** Build AFFiNE Social Media OS template page.
- [ ] **Task 7:** Wire AFFiNE Sync Service to push social performance data to coach workspace.
- [ ] **Task 8:** Add `social_posts` and `social_performance` table migrations to Supabase.
- [ ] **Task 9:** Build `Sofia` agent persona YAML (Social Performance Analyst) in the Strategy Department.

---

## 7. Acceptance Criteria

- [ ] **AC1 (Auto-Queue):** CMF Pipeline produces an approved post. Assert the post appears in the social scheduler's queue within 30 seconds.
- [ ] **AC2 (Multi-Platform):** Queue a post for Instagram + YouTube + LinkedIn. Assert 3 separate scheduled items exist in the scheduler.
- [ ] **AC3 (Publish Tracking):** Scheduler publishes a post. Assert `social_posts.status` = `'published'` and `published_at` is populated.
- [ ] **AC4 (Metric Ingestion):** Publish a test post. Wait 6h (or mock). Assert `social_performance` row exists with `collection_cycle = '6h'` and non-null engagement metrics.
- [ ] **AC5 (Top Performer):** Create 10 posts with baseline engagement. Create 1 post with 3x average engagement. Assert `is_top_performer = true` on the outlier.
- [ ] **AC6 (Dashboard Render):** Open the Social Media OS page in AFFiNE. Assert all 5 sections render with correct data.
- [ ] **AC7 (Receipt Chain):** Publish a post. Assert receipt is written to Receipt Chain Guard.

---

## 8. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| CMF Pipeline | Internal (existing) | Provides post-ready content for queuing. Must emit a completion event. |
| AFFiNE Sync Service (FR-CA11-02) | Internal | Pushes social performance data to coach workspace. |
| AWS EC2/ECS | Infrastructure | For hosting scheduler Docker container. |
| Supabase | Internal | For `social_posts` and `social_performance` tables. |
| Social platform OAuth credentials | External | Required for each platform (Instagram, YouTube, etc.). |

---

## 9. Testing Strategy

### Unit Tests
- **Post Queuing:** Mock scheduler API. Call `/social/queue` with valid payload. Assert correct API call to scheduler.
- **Top Performer Detection:** Insert 10 posts with known engagement scores. Insert 1 outlier at 3x. Assert `is_top_performer` flag.
- **Engagement Score Calculation:** Verify weighted engagement score formula produces expected results.

### Integration Tests
- **Full Queue→Publish→Ingest Flow:** Queue a post → verify scheduler receives it → mock publish → verify `social_posts` status update → mock metrics → verify `social_performance` row.
- **AFFiNE Dashboard Sync:** Create 5 social performance records. Trigger AFFiNE sync. Assert Social Media OS page data matches.
