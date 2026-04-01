# Feature Brief: Conscious Social Scheduling & Performance Analysis

*Feature ID: FB-STUDIO-01*  
*Parent MCDA: MCDA IV §IX*  
*Date: 2026-03-25*  
*Status: Brainstorm → Pending Spec*

---

## 1. Problem Statement

The CCP generates content autonomously via the CCF pipeline and publishes via Publer (FR43). Publer is a one-way pipe: content exits, but **zero performance data returns**. CRAL agents and the CCF content strategy generate next week's scripts without ever knowing what worked this week. The system is flying blind on the most critical feedback signal in content marketing: audience response.

Additionally, Publer is a SaaS dependency — the coach's content schedule, posting history, and engagement data live on Publer's servers, violating the CCP's data sovereignty principle (ADR-01, ADR-05).

---

## 2. Solution Overview

Replace Publer with a **self-hosted open-source social media scheduler** (Postiz or Mixpost) running as a Docker container on the CCP AWS infrastructure. Build a native **AFFiNE "Social Media OS" template** as the coach-facing dashboard. Implement a **performance ingestion pipeline** that pulls engagement metrics from platform APIs and feeds them into CRAL for content strategy optimization.

---

## 3. Core Components

### 3.1 Self-Hosted Scheduler (Docker Container)

**Purpose:** Handle OAuth flows, token management, multi-platform API auth, format adaptation, and scheduled posting.

**Supported Platforms:** Instagram (Meta Business API), YouTube (Data API v3), TikTok (Content Posting API), LinkedIn (Share API), Facebook (Graph API), X/Twitter (API v2).

**Deployment:** Docker container on same EC2 instance or ECS cluster as TribeNest and AFFiNE. PostgreSQL database (shared Supabase instance or dedicated schema).

**Why not raw API integration:** Social media APIs are notoriously fragile — Instagram alone requires Meta Business verification, app review, and token refreshes every 60 days. Open-source schedulers have communities maintaining these integrations, amortizing the maintenance burden across thousands of users.

### 3.2 Performance Ingestion Pipeline

**Service:** `social_performance_collector.py` — Python cron job running every 6 hours.

**Data collected per post:**

| Metric | Source | Notes |
|---|---|---|
| `impressions` | Platform API | Total display count |
| `reach` | Platform API | Unique users reached |
| `likes` | Platform API | — |
| `comments` | Platform API | Count only (text stored separately) |
| `shares` | Platform API | Retweets, reposts, shares |
| `saves` | Platform API | Instagram saves, YouTube "Watch Later" |
| `watch_time_seconds` | Platform API | YouTube/TikTok video watch time |
| `click_through_rate` | Platform API | Link clicks / impressions |
| `engagement_rate` | Calculated | (likes + comments + shares + saves) / reach |

**Storage:** `content_performance` Supabase table. Primary key: `content_id` (UUID, FK to `fingerprint_archive`). Composite index on `(content_id, platform, collected_at)`.

**CRAL Integration:** Performance data is accessible to CRAL agents (FR12) as a new evidence source. The Expression Department agents (Julio, Cesare) receive weekly performance summaries alongside their CRAL research briefs, enabling data-driven content strategy adjustments.

### 3.3 AFFiNE "Social Media OS" Template

**Location:** Dedicated section in the coach's AFFiNE workspace (Section 9: Social Media Intelligence).

**Panels:**

| Panel | Data Source | Purpose |
|---|---|---|
| **Performance Dashboard** | `content_performance` table | Top-performing content this week/month sorted by composite engagement score |
| **Content Calendar** | Scheduler API + `affine_sync.py` | Visual grid: scheduled (orange), posted (green), draft (gray) with platform icons |
| **Platform Health** | Scheduler OAuth status | Connection status per account, token expiry warnings |
| **Intelligence Feed** | CRAL-generated insights | Natural language recommendations (e.g., *"Identity hooks outperform Problem hooks 3.2× on IG"*) |
| **Highlight Reel** | Top 5% `engagement_rate` | Auto-surfaced for CCF repurposing pipeline |
| **Hashtag & Timing** | Performance analytics | Best posting times per platform, top-performing hashtag clusters |

### 3.4 Publishing Flow (No Posting Buttons)

```
CCF generates content → pushed to AFFiNE Content Calendar
        ↓
Coach reviews in AFFiNE → Approve / Edit / Reject
        ↓
On Approve → affine_sync.py triggers scheduler API
        ↓
Scheduler queues content at optimal time (FR43 engagement math)
        ↓
Post published → 6h later → performance data ingested
        ↓
Data feeds CRAL → next week's CCF batch is smarter
```

**Override:** A "Post Now" button exists for spontaneous content. This is the ONLY button in the social media flow.

---

## 4. Data Model

### New Tables

```sql
-- Content performance metrics (one row per platform per collection)
CREATE TABLE content_performance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content_id UUID NOT NULL REFERENCES fingerprint_archive(id),
    platform VARCHAR(20) NOT NULL, -- instagram, youtube, tiktok, linkedin, facebook, twitter
    impressions INTEGER DEFAULT 0,
    reach INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    saves INTEGER DEFAULT 0,
    watch_time_seconds INTEGER DEFAULT 0,
    click_through_rate DECIMAL(5,4) DEFAULT 0,
    engagement_rate DECIMAL(5,4) DEFAULT 0,
    collected_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Scheduler sync events (audit log)
CREATE TABLE scheduler_sync_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content_id UUID NOT NULL,
    action VARCHAR(20) NOT NULL, -- scheduled, posted, failed, cancelled
    platform VARCHAR(20) NOT NULL,
    scheduled_for TIMESTAMP WITH TIME ZONE,
    posted_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    receipt_chain_id UUID REFERENCES receipt_chain(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 5. CCP Integration Points

| System | Integration | Direction |
|---|---|---|
| **CCF Pipeline** | Content approved → scheduler queues | CCP → Scheduler |
| **CRAL** | Performance data as evidence source | Scheduler → CCP |
| **AFFiNE Sync Service** | Social Media OS template data push | CCP → AFFiNE |
| **Receipt Chain** | `DEP-ENG-041` receipt on publish completion | Bidirectional |
| **Fingerprint Archive** | Content ID links performance to source content | FK reference |
| **FR43** | Engagement math logic reused for optimal timing | Internal |

---

## 6. Migration from Publer

| Phase | Action | Duration |
|---|---|---|
| 1 | Deploy self-hosted scheduler, connect OAuth accounts | 1 day |
| 2 | Parallel run: Publer + self-hosted scheduler (same content) | 1 week |
| 3 | Validate posting quality and timing across platforms | 1 week |
| 4 | Retire `publer_sync.py`, activate `scheduler_sync.py` | 1 day |
| 5 | Deploy performance ingestion pipeline | 1 day |
| 6 | Activate AFFiNE Social Media OS template | 1 day |

**Total migration:** ~2.5 weeks with parallel validation.

---

## 7. Success Criteria

| Criterion | Target | Measurement |
|---|---|---|
| Publer retirement | 100% posting via self-hosted scheduler | `publer_sync.py` call count drops to 0 |
| Performance data coverage | ≥95% of published content has performance data within 24h | `content_performance` table completeness |
| CRAL integration | Performance insights appear in ≥80% of weekly CRAL briefs | CRAL output audit |
| Content strategy improvement | 15% increase in average engagement rate within 60 days | `content_performance` trend analysis |

---

## 8. Risks

| Risk | Mitigation |
|---|---|
| Platform API rate limits | Batch collection every 6h, not per-minute polling |
| OAuth token expiry | Automated refresh + AFFiNE Platform Health panel alerts coach |
| Self-hosted scheduler maintenance | Use actively maintained OSS project (Postiz: 400+ stars, monthly releases) |
| Performance data inconsistency | Idempotent collection (same content_id + platform + collected_at = upsert) |

---

*End of Feature Brief FB-STUDIO-01.*
