

**CONSCIOUS ELITE**

Integration & Intelligence Architecture

**Data Infrastructure**

**Documentation v1.0**

| Version: 1.0 | Status: Specification | Date: March 2026 |
| :---- | :---- | :---- |

| Covers: Publer API · Notion Dashboard · Data Analyst Agent | Depends on: Supabase · n8n · CCP Fingerprint Archive |
| :---- | :---- |

*Three integrated layers: automated performance retrieval, coach-facing intelligence dashboard,*

*and a data analyst agent that converts production volume into compound learning.*

March 2026  ·  Conscious Elite Engineering

# **I  System Overview — The Data Intelligence Layer**

**The production pipeline generates data at every stage.** A script is compiled — that's data. A video is published — that's data. An audience responds — that's data. A coach's client checks in via Telegram — that's data. Without a layer that collects, evaluates, and surfaces this data intelligently, every agent in the pipeline is working harder to produce outputs that compound less than they should.

This document specifies three components that together form the Data Intelligence Layer:

| Component | Function | Value |
| ----- | ----- | ----- |
| **Publer Integration** | Automated performance retrieval from all published content across all platforms | Closes the learning loop. Performance data returns to the Fingerprint Archive without any manual action from the coach or the operator. |
| **Notion Coach Dashboard** | Coach-facing intelligence surface showing content performance, client activity, and system health | Gives the coach visibility without giving them complexity. Everything they need to see — nothing they need to operate. |
| **Data Analyst Agent** | Scheduled evaluation agent that processes accumulated performance data and generates strategic intelligence reports | Converts raw metrics into actionable direction. The agent that makes all other agents smarter over time. |

## **The Compound Intelligence Principle**

Each piece of content the system produces should make the next piece better. That only happens if performance data is captured, evaluated, and fed back into the production parameters. Without the Data Intelligence Layer, the system produces at volume but does not improve with volume. The Fingerprint Archive exists to enable this loop — but the loop only closes if data flows in automatically and is evaluated systematically.

| Without the Data Intelligence Layer: Agents produce at volume Performance data stays on the platform No feedback into production parameters Volume × 0 compound learning \= noise at scale With the Data Intelligence Layer: Performance data returns automatically via Publer API Coach sees results in Notion without leaving their workspace Data Analyst Agent evaluates patterns weekly Production parameters update based on what actually works Volume × compound learning \= improving system |
| :---- |

# **II  Publer Integration — Automated Performance Retrieval**

**Publer is the single integration point for the entire content distribution and performance layer.** The coach's Instagram, LinkedIn, TikTok, and all other platforms connect once through Publer's standard OAuth flow. After that connection, your API key handles everything — scheduling, publishing, and analytics retrieval — without ever touching the platform APIs directly.

## **2.1  What the Integration Does**

| Capability | What It Means Operationally |
| ----- | ----- |
| **Scheduled Publishing** | Content assembled by the CMF pipeline is scheduled via Publer API. The coach never logs into a platform manually. |
| **Post Registration** | At the moment of publishing, Publer returns the platform post\_id and the published URL. These are written back to the Fingerprint Archive row for that output\_id. |
| **Automatic Insights Sync** | Publer syncs performance analytics every 24 hours automatically. You can also trigger a manual sync via API call for fresher data at any time. |
| **Per-Post Metrics** | The Post Insights endpoint returns: reach, impressions, engagement rate, saves, shares, comments, likes, video views, profile visits triggered by the post. |
| **Hashtag Analysis** | Aggregate performance by hashtag — which tags are delivering reach versus which are decorative. |
| **Best Times to Post** | Day/hour heatmap per account derived from historical performance. The Data Analyst Agent reads this to update Publer scheduling parameters. |
| **Multi-Platform** | Facebook, Instagram, LinkedIn, TikTok, Pinterest, YouTube, Threads, Bluesky — all intermediated by Publer. No geographic TikTok API issues. No per-platform authentication. |

## **2.2  API Credentials & Workspace Setup**

| Authentication: Authorization: Bearer-API YOUR\_API\_TOKEN Publer-Workspace-Id: YOUR\_WORKSPACE\_ID Content-Type: application/json Base URL: https://app.publer.com/api/v1 Rate Limit: 100 requests per 2 minutes per user Plan Required: Business (lifetime deal already covers this) |
| :---- |

| ℹ  API token is generated in Publer Settings → Access & Login → API Keys. Store it in Supabase as an encrypted environment variable — never hardcode it in n8n workflows. |
| :---- |

**Client workspace setup:** Each coach's social accounts should be connected to your Publer workspace — not their own separate Publer accounts. This means one API token covers all clients. If a coach has their own Publer account, invite them to a shared workspace or have them connect their accounts to yours. This is a one-time onboarding step per coach.

## **2.3  The Four Automated Triggers**

The entire Publer integration runs on four n8n workflow triggers. No manual steps after initial client onboarding.

### **Trigger 1 — Content Scheduling**

| 01  Supabase webhook fires when videos.status \= READY\_TO\_PUBLISH 02  n8n receives webhook payload with output\_id, video\_file\_url, caption, platform targets 03  n8n calls POST /api/v1/post to schedule via Publer 04  Publer returns scheduled\_post\_id and scheduled\_time 05  n8n writes publer\_post\_id \+ scheduled\_at back to Supabase videos row 06  Fingerprint Archive record now has full publication reference |
| :---- |

### **Trigger 2 — Publication Confirmation**

| 01  Publer webhook fires when post status changes to PUBLISHED 02  n8n receives platform\_post\_id \+ published\_url \+ published\_at 03  n8n updates Supabase: videos.published\_at, videos.platform\_post\_url 04  n8n also creates Notion Dashboard entry for this post (see Section III) 05  Post is now live and traceable in the Fingerprint Archive |
| :---- |

### **Trigger 3 — 48-Hour Performance Retrieval**

| 01  n8n scheduled job runs every 6 hours 02  Queries Supabase for posts where published\_at \< NOW() \- 48h AND first\_insights\_collected \= false 03  For each qualifying post: calls GET /api/v1/analytics/post\_insights?post\_id={publer\_post\_id} 04  Writes metrics to Supabase: reach, impressions, saves, shares, comments, likes, video\_views 05  Sets first\_insights\_collected \= true 06  Pushes updated metrics to Notion Dashboard for that coach |
| :---- |

### **Trigger 4 — 7-Day & 30-Day Performance Snapshots**

| 01  n8n scheduled job runs daily 02  Queries Supabase for posts at exactly 7 days and 30 days since published\_at 03  Calls Post Insights endpoint for updated metrics at each milestone 04  Writes day\_7\_metrics and day\_30\_metrics to Supabase 05  Triggers Data Analyst Agent evaluation cycle if 7-day snapshot (see Section IV) 06  Updates Notion Dashboard with snapshot data |
| :---- |

## **2.4  Key API Endpoints**

| Endpoint | Method | Used For |
| ----- | ----- | ----- |
| /api/v1/post | POST | Schedule a new post. Pass platform targets, caption, media URLs, scheduled time. |
| /api/v1/analytics/post\_insights | GET | Per-post metrics. Filter by date range, sort by metric, paginate. Core retrieval endpoint. |
| /api/v1/analytics/charts | GET | Aggregate analytics charts. Used by Data Analyst Agent for trend analysis. |
| /api/v1/analytics/hashtags | GET | Hashtag performance aggregation. Identifies which tags drive real reach vs decorative. |
| /api/v1/analytics/best\_times | GET | Day/hour posting heatmap. Data Analyst Agent reads this to update scheduling parameters. |
| /api/v1/me | GET | Validate credentials. Run on system startup to confirm API token is active. |
| /api/v1/workspaces | GET | List workspaces and connected accounts. Used to map coach\_id to workspace\_id at onboarding. |

## **2.5  Supabase Schema — Performance Data Tables**

| Table: content\_performance output\_id          UUID        FK → fingerprint\_archive.output\_id publer\_post\_id     VARCHAR     Publer internal post identifier platform           VARCHAR     instagram | linkedin | tiktok | etc platform\_post\_url  TEXT        Direct URL to published post published\_at       TIMESTAMP   When post went live reach              INTEGER     Unique accounts reached impressions        INTEGER     Total views including repeat saves              INTEGER     Saves / bookmarks shares             INTEGER     Shares / reposts / sends comments           INTEGER     Comment count likes              INTEGER     Like count video\_views        INTEGER     Video view count (if video) engagement\_rate    DECIMAL     (saves+shares+comments+likes)/reach first\_insights\_at  TIMESTAMP   When 48h snapshot was collected day\_7\_snapshot     JSONB       Full metrics object at 7 days day\_30\_snapshot    JSONB       Full metrics object at 30 days created\_at         TIMESTAMP   Auto updated\_at         TIMESTAMP   Auto |
| :---- |

# **III  Notion Coach Dashboard — Intelligence Surface**

**The Notion Dashboard is not a reporting tool.** It is the coach's operational intelligence surface — the single place where everything they need to see about their content, their clients, and their system is visible without requiring them to log into multiple platforms, ask questions, or manually pull data.

The coach should never need to ask "how did that video perform?" or "what are my clients doing this week?" The dashboard answers both questions automatically, in real time, every time they open Notion.

## **3.1  Dashboard Architecture — Five Databases**

| Database | What It Contains | Who Writes It | Coach Uses It To |
| ----- | ----- | ----- | ----- |
| **Content Library** | All CCP-generated scripts, their compilation metadata, arc type, mood routing, CRAL coverage status | n8n writes from Supabase scripts table on AUTHORIZED status | Review scripts before recording, access past scripts, track what's been used |
| **Published Content** | All published posts with platform, published date, thumbnail, caption, and live performance metrics | n8n writes on publication confirmation \+ updates every 48h from Publer API | See what's live, track performance, identify high-performers at a glance |
| **Content Performance** | Performance analytics per post: reach, saves, shares, engagement rate, 7-day and 30-day snapshots | n8n writes from Publer Post Insights endpoint on schedule | Understand what content is working, identify patterns, see which arcs perform best |
| **Client Activity** | CBCS client data: active clients per coach, check-in rates, streak data, last interaction, compliance scores | n8n writes from Supabase CBCS tables on daily sync | Monitor client engagement, identify at-risk clients, see who needs attention |
| **System Intelligence** | Weekly Data Analyst Agent reports: performance trends, top-performing content, scheduling recommendations, pattern analysis | Data Analyst Agent writes directly to Notion via API after each evaluation cycle | Receive strategic direction without needing to analyse raw data |

## **3.2  Published Content Database — Core Fields**

This is the most-used database. The coach opens this first. Every published piece is a row.

| Field | Type | Content |
| ----- | ----- | ----- |
| Title | Title | Auto-generated from script hook line. Identifies the content instantly. |
| Platform | Select | Instagram | LinkedIn | TikTok | YouTube — with platform icon |
| Arc Type | Select | The 13 CMF arc or CCP archetype that generated this piece. Critical for pattern analysis. |
| Status | Select | Scheduled | Published | Performance Collected | Analyst Reviewed |
| Published Date | Date | Auto-populated from Publer publication confirmation. |
| Reach | Number | Auto-updated from Publer Post Insights every 48h. |
| Saves | Number | The virality signal. Saves indicate content worth returning to. |
| Shares | Number | Reach amplification signal. Shares push content beyond existing audience. |
| Engagement Rate | Formula | (saves+shares+comments+likes)/reach — calculated field. The quality signal. |
| 7-Day Score | Number | Engagement rate at day 7 snapshot. Comparable across all content. |
| Performance Tag | Select — auto | HIGH PERFORMER | AVERAGE | UNDER-PERFORMER — set by Data Analyst Agent |
| Script Link | Relation | Links to the Content Library row for the script that generated this piece. |
| Post URL | URL | Direct link to live post on platform. |
| Output ID | Text | Fingerprint Archive output\_id. The traceability key. |

## **3.3  Notion API Integration — n8n Workflow**

| 01  n8n receives publication confirmation from Publer webhook 02  Calls Notion API: POST /v1/pages to create row in Published Content database 03  Populates Title, Platform, Arc Type, Status=Published, Published Date, Post URL, Output ID 04  Every 48h: n8n fetches Publer Post Insights → calls PATCH /v1/pages/{page\_id} to update metrics 05  Every 7 days: n8n updates 7-Day Score field from Publer day\_7\_snapshot 06  Data Analyst Agent writes Performance Tag after each evaluation cycle 07  Coach opens Notion. Everything is already there. |
| :---- |

## **3.4  Notion API Credentials**

| Authentication: Authorization: Bearer YOUR\_NOTION\_TOKEN Notion-Version: 2022-06-28 Content-Type: application/json Setup: Create a Notion Integration at notion.so/my-integrations Generate Internal Integration Token Share each dashboard database with the integration (Connections → Add integration) Store the Integration Token and each Database ID in Supabase environment variables Map coach\_id → notion\_workspace\_id in Supabase coach\_config table |
| :---- |

| ℹ  Each coach gets their own Notion workspace or a dedicated page in your master workspace. The database IDs will be different per coach — store them in the coach\_config table in Supabase so n8n knows which database to write to for each coach's content. |
| :---- |

# **IV  The Data Analyst Agent — Compound Intelligence**

**Processing data without evaluating it is making agents work harder to produce noise faster.** The Data Analyst Agent is the component that converts production volume into compound learning. It is not a reporting tool. It is an evaluation system that reads accumulated performance data, identifies patterns, generates strategic direction, and updates production parameters — so that every week the system is making better decisions than the week before.

## **4.1  The Core Problem It Solves**

| Without the Data Analyst Agent: *"The system produced 40 videos this month. Some performed well. Some didn't. We don't know which arcs work for which audiences. We don't know which CRAL moments drove saves vs shares. We don't know which CCP archetypes perform in Status Mode vs Escape Mode. We produce the same way next month regardless of what happened this month."* With the Data Analyst Agent: *"The system produced 40 videos this month. The agent evaluated all 40 against their 7-day performance snapshots. It identified that Achievement Story × Prevention Frame is driving 3× average saves for this coach's audience. It identified that M7\_RELATABLE tribal recognition is the highest-leverage CRAL moment for this niche. It updated the CCP compilation priority weights accordingly. Next month's production starts from this intelligence, not from zero."* |
| :---- |

## **4.2  Agent Architecture**

The Data Analyst Agent runs on a weekly evaluation cycle. It is triggered automatically by n8n when a threshold of new 7-day performance snapshots have been collected. It operates in three phases:

### **Phase 1 — Data Preparation**

**What it does:** Pulls all performance data from the last evaluation period. Structures it for analysis. Identifies data quality issues before analysis begins.

| 01  Query Supabase: SELECT all content\_performance WHERE day\_7\_snapshot IS NOT NULL AND analyst\_reviewed \= false 02  Join with fingerprint\_archive to get: output\_id, archetype, mood\_state, regulatory\_frame, cral\_coverage\_status, cral\_degraded\_phases 03  Join with scripts to get: arc\_type, trigger\_category, coach\_id 04  Validate data completeness: flag any rows missing platform, reach, or arc metadata 05  Structure into evaluation payload: group by coach\_id, then by arc\_type, then by mood\_state 06  Check minimum sample threshold: require ≥5 data points per arc before drawing conclusions 07  Output: structured evaluation\_payload.json ready for Phase 2 |
| :---- |

### **Phase 2 — Pattern Evaluation**

**What it does:** Applies evaluation frameworks to the structured data. Identifies what is working, what is underperforming, and why.

| Evaluation Framework | Question It Answers | Output |
| ----- | ----- | ----- |
| **Arc Performance Matrix** | Which narrative arcs (CMF 13-arc system \+ CCP archetypes) are producing above-average engagement for this coach's audience? | Ranked arc performance table. Identifies top 3 performing arcs and bottom 3\. Recommendation: increase/decrease production frequency per arc. |
| **CRAL Moment Impact Analysis** | Which CRAL moment findings (M1-M7) correlate with above-average saves? Which correlate with above-average shares? | CRAL moment impact scores per moment per metric. Updates DEP-ENG-021 priority weights for this coach's trigger categories. |
| **Psychological Mode Analysis** | Which mood state × regulatory frame combinations are producing the highest engagement rate? Are there combinations that consistently underperform? | Mode performance matrix. Recommendation: adjust CCP compilation routing weights for this coach. |
| **Platform Comparison** | Is the same content performing differently across platforms? Are there platform-specific patterns in what drives saves vs shares? | Platform delta report. Identifies whether content needs platform-specific optimisation or whether the current cross-posting strategy is sound. |
| **CRAL Degradation Impact** | Do posts where CRAL coverage was PARTIAL or ABSENT perform worse than COMPLETE coverage posts? How much worse? | Quantified CRAL degradation cost. The economic argument for running full CRAL sessions rather than degraded ones. |
| **Timing Analysis** | Are there day/hour patterns in the performance data that differ from the current Publer scheduling configuration? | Scheduling adjustment recommendations. Calls Publer Best Times endpoint to validate against platform-confirmed data. |

### **Phase 3 — Intelligence Output**

**What it does:** Converts evaluation findings into three outputs: a coach-facing report written in plain language, a system-facing parameter update written in structured data, and a production directive for the next cycle.

### **Output A — Notion Intelligence Report**

Written directly to the System Intelligence database in the coach's Notion workspace. Written in plain language — no jargon, no data tables. The coach reads this to understand what is working and what the system is doing about it.

| Report Structure: What performed best this week — top 3 pieces with plain-language explanation of why What the audience responded to most — the pattern underneath the performance, described in human terms What the system is adjusting — what production parameters are changing next cycle and why What to record next — specific content direction for the upcoming recording session Client activity summary — CBCS engagement highlights and any clients needing attention |
| :---- |

### **Output B — Parameter Update Payload**

Written to Supabase as a structured JSON object. Read by the CCP compilation pipeline and the CMF arc router on the next production cycle. This is how performance data changes what gets produced next.

| parameter\_update.json structure: {   "coach\_id": "coach\_xxx",   "evaluation\_period": "2026-W11",   "arc\_priority\_weights": {     "Achievement\_Story": 1.4,  // increase — above average saves     "Myth\_Debunk": 0.7,        // decrease — underperforming     "Transformation\_Arc": 1.1  // maintain   },   "cral\_moment\_priority": {     "M7\_RELATABLE": "HIGH",    // top saves driver     "M2\_BELIEVABLE": "HIGH",   // top shares driver     "M1\_RELEVANT": "MEDIUM"   },   "mode\_routing\_adjustments": {     "Processing\_Prevention": "INCREASE",     "Status\_Promotion": "DECREASE"   },   "scheduling\_updates": {     "instagram": {"optimal\_days": \["TUE","THU"\], "optimal\_hours": \[8,19\]},     "linkedin": {"optimal\_days": \["MON","WED"\], "optimal\_hours": \[7,12\]}   },   "next\_cycle\_directive": "Prioritise Achievement Story x Prevention Frame."   "cral\_investment\_recommendation": "Full CRAL sessions showing 2.3x saves lift vs PARTIAL" } |
| :---- |

### **Output C — Fingerprint Archive Update**

Marks all evaluated posts with analyst\_reviewed \= true in Supabase. Sets Performance Tag in Notion (HIGH PERFORMER / AVERAGE / UNDER-PERFORMER). Writes evaluation\_period to each content\_performance row so the next agent knows which data has already been evaluated and does not re-process it.

## **4.3  Agent Trigger Conditions**

| Trigger | Condition |
| ----- | ----- |
| **Weekly Evaluation Cycle** | n8n scheduled job fires every Monday 06:00. Checks Supabase for ≥10 new 7-day snapshots since last evaluation. If threshold met: fires agent. If not met: waits until next week. |
| **New Coach Threshold** | For coaches in first 30 days: lower threshold of ≥5 posts. Early data is valuable even at lower volume. |
| **Manual Trigger** | Operator can trigger evaluation manually via Supabase function call. Used when a specific campaign concludes and immediate analysis is needed. |
| **Minimum Data Guard** | Agent will not run if total posts across all coaches \< 15\. No pattern detection is valid at very low sample sizes. Agent outputs "Insufficient data" and schedules retry. |

## **4.4  The Compound Learning Loop — Closed**

With all three components in place, the compound learning loop is fully closed for the first time:

| 01  CCP compiles skill using current arc\_priority\_weights and cral\_moment\_priority 02  CMF produces video using authorized script 03  Publer publishes and returns platform\_post\_id 04  Publer API returns performance metrics at 48h, 7 days, 30 days 05  n8n writes all metrics to Supabase content\_performance table 06  n8n updates Notion Published Content database in real time 07  Data Analyst Agent evaluates weekly — identifies what is working and why 08  Agent writes parameter\_update.json to Supabase 09  CCP reads updated weights on next compilation cycle 10  Next piece of content is produced with intelligence from all previous performance 11  System improves with every production cycle — not despite volume, because of it |
| :---- |

# **V  Implementation Sequence**

The three components are implemented in dependency order. Publer integration first — it generates the data. Notion Dashboard second — it surfaces the data. Data Analyst Agent third — it evaluates the data. Each component is independently valuable and does not require the next to function.

| Step | Action | Outcome | Time Estimate |
| ----- | ----- | ----- | ----- |
| **1** | Create Supabase content\_performance table with full schema from Section II.5 | Data store ready to receive Publer metrics | 30 minutes |
| **2** | Validate Publer API credentials. Test GET /api/v1/me. Confirm all coach accounts are connected to your workspace. | Confirmed API access across all client accounts | 1 hour |
| **3** | Build n8n Trigger 1 (Content Scheduling). Connect Supabase webhook on videos.status \= READY\_TO\_PUBLISH → Publer POST /api/v1/post. | Content scheduling automated end to end | 2 hours |
| **4** | Build n8n Trigger 2 (Publication Confirmation). Publer webhook → Supabase update \+ Notion row creation. | Every published post appears in Notion automatically | 2 hours |
| **5** | Create Notion databases: Content Library, Published Content, Content Performance, Client Activity, System Intelligence. Define all fields from Section III.2. | Coach dashboard structure ready | 3 hours |
| **6** | Build n8n Trigger 3 (48-hour Performance Retrieval). Scheduled job → Publer Post Insights → Supabase \+ Notion update. | Performance data flowing automatically without manual action | 2 hours |
| **7** | Build n8n Trigger 4 (7-day and 30-day snapshots). Add milestone detection and snapshot writing to Supabase and Notion. | Complete performance timeline per post | 1 hour |
| **8** | Build Data Analyst Agent Phase 1 (Data Preparation). Supabase queries, join logic, evaluation payload construction. | Clean structured data ready for analysis | 4 hours |
| **9** | Build Data Analyst Agent Phase 2 (Pattern Evaluation). Six evaluation frameworks. Parameter update JSON generation. | System can identify what works and update production parameters | 8 hours |
| **10** | Build Data Analyst Agent Phase 3 (Intelligence Output). Notion report writer. Parameter update writer to Supabase. Fingerprint Archive tagging. | Full compound learning loop closed | 4 hours |

| ⚠  Do not build the Data Analyst Agent before you have at least 2 weeks of real performance data in Supabase. An agent that evaluates empty or near-empty data produces misleading recommendations. Steps 1-7 first. Run the pipeline. Collect real data. Then build Steps 8-10. |
| :---- |

# **VI  Coach Onboarding — Connecting a New Client**

Every new coach requires a one-time onboarding sequence. After this sequence completes, the coach never needs to interact with the technical infrastructure again. Everything surfaces in their Notion workspace automatically.

| 01  Coach connects their social accounts to your Publer workspace via OAuth (10 minutes, one-time) 02  You note their Publer workspace\_id — add to Supabase coach\_config table 03  Create coach's Notion workspace or dedicated Notion page 04  Duplicate the dashboard template — create all 5 databases for this coach 05  Note each database ID — add to Supabase coach\_config alongside workspace\_id 06  Add coach record to Supabase: coach\_id, name, notion\_workspace\_id, publer\_workspace\_id 07  Run validation: trigger one test post through the pipeline, confirm it appears in Notion 08  Coach receives Notion access — their dashboard is live |
| :---- |

**coach\_config table schema:**

| coach\_id                    UUID PRIMARY KEY coach\_name                  VARCHAR publer\_workspace\_id         VARCHAR notion\_workspace\_id         VARCHAR notion\_content\_library\_db   VARCHAR    Database ID notion\_published\_content\_db VARCHAR    Database ID notion\_performance\_db       VARCHAR    Database ID notion\_client\_activity\_db   VARCHAR    Database ID notion\_intelligence\_db      VARCHAR    Database ID onboarded\_at                TIMESTAMP active                      BOOLEAN    DEFAULT true |
| :---- |

——

**Data Infrastructure Documentation v1.0**  
Publer Integration  ·  Notion Dashboard  ·  Data Analyst Agent  
*March 2026  ·  Conscious Elite Engineering*