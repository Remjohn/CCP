---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
parentPRD: d:\Work\The Conscious Coaching Factory\docs\prd\prd.md
updateType: brownfield-capability-extension
inputDocuments:
  - d:\Work\The Conscious Coaching Factory\docs\prd\prd.md
  - d:\Work\The Conscious Coaching Factory\CCP_System_Documentation.md
  - d:\Work\The Conscious Coaching Factory\MCDA_AFFiNE_Integration_Analysis.md
  - d:\Work\The Conscious Coaching Factory\MCDA_14_AFFiNE_Power_Integrations.md
  - d:\Work\The Conscious Coaching Factory\MCDA_15_Cross_Platform_Workflows.md
  - d:\Work\The Conscious Coaching Factory\Offline_Field_Acceleration_Protocol.md
  - d:\Work\The Conscious Coaching Factory\CMF_Pipeline_Documentation.md
workflowType: 'prd-update'
lastStep: 11
project_name: 'Conscious Coaching Platform — Quad-Platform Intelligence Layer'
user_name: 'Emilio'
date: '2026-03-24T17:25:39+01:00'
capabilityArea: 11
---

# PRD Update — Capability Area 11: The Sovereign Coaching Operating System

## Quad-Platform Intelligence Layer (AFFiNE × Excalidraw × CCP Studio × Telegram × CVE Canva Clone)

**Author:** Emilio  
**Date:** 2026-03-24T17:25:39+01:00  
**PRD Version:** 2.0.0 (Brownfield Extension of Parent PRD v1.0)  
**Parent Document:** `docs/prd/prd.md` (Capability Areas 0–10)  
**Classification:** STRATEGIC INFRASTRUCTURE — Delivery Layer Replacement + Cross-Platform Content Automation

---

## 1. Executive Summary

This PRD update introduces **Capability Area 11** — the Quad-Platform Intelligence Layer — to the Conscious Coaching Platform. It formally retires **ADR-02** (Notion as Zero-UI Delivery Layer) and replaces the Notion dependency with a self-hosted, thin-forked instance of **AFFiNE** — rebranded and deployed as the **Conscious Elite OS**, the coach-facing and client-facing sovereign workspace.

The update integrates four open-source platforms — AFFiNE (the brain), Excalidraw (the eyes), CCP Studio (the mouth — native recording/streaming/interactive experiences), and Telegram (the nervous system) — alongside the existing CVE Canva Clone (Conscious Canva App) as the visual asset compositor. Together, these form a closed-loop autonomous content-and-coaching infrastructure that converts a single coaching interaction into structured knowledge, visual assets, personalized learning journeys, and revenue intelligence — with zero manual orchestration.

This is not a feature addition. It is the **delivery layer transformation** — the last mile that makes 3 years of backend engineering visible to coaches and their clients.

### Why Now

The existing PRD documents a 76-agent, 180-skill, 10-capability-area architecture that is functionally sovereign in intelligence but **delivery-dependent on Notion**. Notion is a third-party SaaS with no API control over:

- Client-facing workspace branding
- Real-time database sync with CCP telemetry (Neo4j, Supabase)
- Gated learning content delivery based on program tags
- Per-client visual progress boards
- OBS recording pipeline integration
- Embedded Excalidraw collaboration surfaces

AFFiNE, as a self-hosted open-source platform (AGPL-3.0, BlockSuite CRDT engine, YJS collaboration, OctoBase Rust storage), provides sovereign control over all six. The MCDA analysis scored AFFiNE at **85.1%** vs. Notion's **54.7%** across 8 weighted criteria.

### What This Changes in the Parent PRD

| Parent PRD Element | Change |
|---|---|
| **ADR-02** | RETIRED. Notion replaced by self-hosted AFFiNE (thin fork). |
| **ADR-06** | RETIRED. OBS WebSocket integration replaced by native CCP Studio (ADR-07). |
| **FR45** (Notion delivery) | Superseded by FR-CA11-01 through FR-CA11-04 (AFFiNE Workspace Sync). |
| **FR35** (Excalidraw pipeline) | Extended by FR-CA11-10 through FR-CA11-12 (embedded Excalidraw + visual delivery). |
| **FR43** (Publer scheduling) | Superseded by FR-CA11-18 (Conscious Social Scheduling). |
| **FR-CA11-13/14** (OBS) | Superseded by FR-CA11-16 through FR-CA11-22 (CCP Studio Platform). |
| **Integration Perimeters table** | Extended with AFFiNE, CCP Studio, Trivianar Engine, Social Scheduler channels. |
| **Non-Functional Requirements** | Extended with AFFiNE uptime, AFFiNE backup, streaming latency targets. |
| **Layer 7 Architecture** | Extended: Delivery Layer splits into Coach Workspace + Client Workspace + Studio. |
| **Section 9.8** (Notion Dashboard) | Superseded by AFFiNE workspace schema (FR-CA11-01). |
| **Agent Roster** | Extended with 7 new agents (Capability Area 11 workforce). |
| **Tool Stack** | Extended with `affine_sync.py`, `ccp-studio-block`, `trivianar_engine.py`, `social_scheduler.py`. |

---

## 2. Architecture Decision Record — ADR-05: AFFiNE Over Notion

> **This ADR formally retires ADR-02.**

| | |
|---|---|
| **Decision** | Self-hosted AFFiNE (thin fork, branded as "Conscious Elite") replaces Notion as the coach and client delivery layer. |
| **Alternative Retired** | Notion as zero-UI delivery layer (ADR-02) |
| **Why Notion Is Retired** | Notion cannot: (1) deliver client-facing branded workspaces, (2) sync real-time with CCP telemetry databases, (3) gate learning content by program/level tags, (4) embed Excalidraw canvases for live collaboration, (5) trigger OBS recording pipelines, (6) run custom AFFiNE blocks for CCP-specific intelligence surfaces. Notion's API rate limits (3 requests/second) also throttle the `notion_sync.py` pipeline during batch delivery. |
| **Why AFFiNE** | Open-source (AGPL-3.0). Self-hosted Docker deployment. BlockSuite CRDT engine enables real-time collaboration. YJS protocol enables multiplayer editing. OctoBase (Rust) provides local-first offline capability. Custom block development via BlockSuite plugins. Full theme/branding control via CSS overlay. No API rate limits on self-hosted instance. |
| **Thin Fork Strategy** | Fork upstream AFFiNE → apply CCP brand theme (CSS + logo + custom blocks) → maintain `upstream/main` remote for upstream merge compatibility. Custom code lives exclusively in the `ccp-theme/` and `ccp-blocks/` directories. Zero modifications to core engine files. |
| **Dual-Layer Data Model** | **Document Layer:** AFFiNE's native OctoBase (CRDT) stores all workspace content (pages, databases, kanban boards, embedded media). **Telemetry Layer:** CCP's existing Supabase (PostgreSQL) + Neo4j store all behavioral intelligence (Context Premises, Change Talk, coping trajectories, CPSC campaign data). A custom **FastAPI Sync Service** bridges events between the two layers via webhooks. |
| **Trade-off Accepted** | Self-hosting adds operational overhead (backups, SSL, upgrades). Mitigated by Dockploy (Docker orchestration on AWS EC2) and `affine_backup.py` daily automated backup script. Upstream divergence risk mitigated by thin fork discipline — no core engine modifications. |
| **Migration Path** | Phase 1: Deploy AFFiNE alongside Notion (parallel operation). Phase 2: Migrate coach dashboard schema to AFFiNE workspace templates. Phase 3: Retire `notion_sync.py`, activate `affine_sync.py`. Phase 4: Onboard first coach with AFFiNE-only delivery. |

---

## 3. ADR-06: OBS WebSocket Integration Strategy [RETIRED — Superseded by ADR-07]

> **⚠️ ADR-06 is RETIRED.** The OBS WebSocket integration (FR-CA11-13, FR-CA11-14) has been replaced by the native CCP Studio Block (ADR-07). OBS remains available as an optional fallback for power users but is no longer architecturally required. See MCDA IV (CCP Studio Integration Analysis, score: 442 vs 225 baseline) for the full decision rationale.

| | |
|---|---|
| **Original Decision** | OBS Studio integrated via WebSocket API (v5). |
| **Retirement Date** | 2026-03-25 |
| **Replacement** | ADR-07: Native CCP Studio Block (see below). |
| **Migration** | FR-CA11-13 → FR-CA11-16 (Full Stack Recording/Streaming). FR-CA11-14 → absorbed into FR-CA11-16 asset overlay panel. |

---

## 3b. ADR-07: Native CCP Studio Block

| | |
|---|---|
| **Decision** | Replace OBS with a native AFFiNE BlockSuite plugin (CCP Studio Block) that integrates recording, streaming, teleprompter, soundboard, guest join, and interactive experiences directly inside the coaching workspace. |
| **Why Native** | (1) Zero context-switching — coach records from within AFFiNE, not a separate app. (2) Intelligence-aware — Studio knows which script, assets, and CMF template to use. (3) Cloud-native — recordings upload to S3 directly, no local file management. (4) Interactive — bidirectional Telegram Trivianar Engine activates during streams. (5) Social distribution — post-production outputs connect directly to the Social Scheduling engine. |
| **Technology** | Browser WebRTC (MediaRecorder API, getUserMedia, getDisplayMedia). Canvas compositing for multi-source recording. Web Audio API for soundboard mixing. WebSocket relay to TribeNest streaming microservice for RTMP restreaming. |
| **Streaming Architecture** | TribeNest extraction: standalone Docker microservice (`ccp-stream-service`) on AWS. Browser sends MediaRecorder chunks via WebSocket → service repackages to RTMP → pushes to YouTube Live / Facebook Live / Custom RTMP. Parallel S3 recording for VOD. |
| **Guest Join** | WebRTC peer-to-peer. Coach generates invite link → guest joins in browser → PiP or side-by-side compositing. MVP: 1 guest. Critical for testimonial recordings, interviews, hot-seat coaching. |
| **OBS Fallback** | OBS remains available as optional external tool. Power users who need advanced scenes/transitions can continue using OBS. But OBS is not architecturally required — `obs_controller.py` is deprecated. |
| **Trade-off Accepted** | Browser MediaRecorder has a quality ceiling (1080p30 max, codec limitations). If quality proves insufficient, a lightweight Electron/Tauri wrapper may be required for native capture. Stream latency target is <3s glass-to-glass via WebSocket→RTMP. |

---

## 4. Functional Requirements — Capability Area 11

### 4.1 AFFiNE Coach Workspace (The Sovereign Dashboard)

- **FR-CA11-01 (Coach Workspace Provisioning):** The system can provision a fully branded AFFiNE workspace for each coach during Genesis Pipeline (Step 2). The workspace is deployed from a master template containing pre-configured pages, databases, and navigation structure that mirrors the retired Notion dashboard schema (Section 9.8 of parent PRD). The workspace includes 8 standard sections: Command Center (pipeline status), Content Calendar (weekly scripts + visual assets), Client Intelligence Hub (anonymized SPT/ICT/Intimacy aggregations), CPSC Campaign Console (campaign performance + Loom Reports), CRAL Evidence Vault (searchable research findings), Guardian Agent Console (Genesis status + Stewardship alerts), Visual Production Console (VPO previews + Canva App links), and Program Content Library (gated course material). The master template is version-controlled in the AFFiNE fork repository. Each coach workspace is isolated — zero cross-coach data leakage, consistent with ADR-01 (single-tenant architecture). *(Supersedes: FR45. Source: Parent PRD §9.8, MCDA I)*

- **FR-CA11-02 (AFFiNE Sync Service):** The system can synchronize CCP backend intelligence to AFFiNE workspace databases via a custom FastAPI-based **AFFiNE Sync Service** (`affine_sync.py`). The service replaces `notion_sync.py` and operates via webhook-driven event propagation. When the CCF pipeline completes a batch (Receipt Chain confirmed), the Sync Service pushes: script content, visual asset URLs (from Cloudflare R2), posting notes, Voice DNA rationale ("Why This Post"), Leadership Farming notes, and Fingerprint IDs to the coach's AFFiNE Content Calendar database. The service also pushes CBCS telemetry aggregations (anonymized SPT distribution, tribe-level ICT, Intimacy Index averages) to the Client Intelligence Hub. Push operations are idempotent — duplicate pushes do not create duplicate entries. The Sync Service maintains an event log in Supabase (`affine_sync_events`) for audit traceability, extending the existing Receipt Chain Guard architecture. *(Supersedes: FR45. Source: Parent PRD §Integration Perimeters)*

- **FR-CA11-03 (Client Workspace Provisioning):** The system can provision a client-facing AFFiNE workspace for each CBCS member, gated by their coaching program enrollment. When a new client is onboarded via the CBCS Telegram bot (FR27), the system automatically creates a client workspace from a program-specific template. The workspace contains: a personalized dashboard (current Capacity Track, streak data, next ritual), a learning content library (program-tagged course videos and materials), a progress journal (synced from CBCS Telegram interactions), and a resource hub (lead magnets, worksheets, Excalidraw diagrams). **Content gating** is enforced by program tags and client progression level — a client in Week 2 of "90-Day Body Transformation" sees different course videos than a client in Week 8. The gating logic queries the client's `coping_trajectory` and `atlas_roadmap` Supabase tables via the Sync Service. Client workspaces are read-only for CCP-managed content sections (preventing accidental deletion of course materials) and read-write for personal sections (journal, notes, goal tracking). *(Source: MCDA II #1, User requirement)*

- **FR-CA11-04 (Continuous Learning Path Builder):** The system can automatically organize coach-generated content into structured, categorized learning journeys within the client's AFFiNE workspace. When a coach generates content through any CCP pipeline — CCF scripts, V²WS webinar recordings, voice notes transcribed via CBCS, OBS session recordings — a dedicated **Learning Path Agent** (`Gabrielle`) categorizes each piece by: topic cluster (extracted from Context Premise Map), difficulty level (derived from Audience Maturity classification), program tag (from coach's program structure), and content type (video, text, audio, diagram). The agent maintains a `learning_path_registry` Supabase table that maps every content piece to its position in one or more learning journeys. Client workspaces display learning paths as visual timelines — each node is a content piece, with completed nodes highlighted and the next recommended piece surfaced prominently. The learning path updates automatically as new content is generated — the coach never manually "creates a course." The course creates itself from the coach's natural production. *(Source: MCDA III #W7, User requirement)*

### 4.2 Cross-Platform Content Intelligence Workflows

- **FR-CA11-05 (AI Session Recap Generator):** The system can convert a CCP Studio recording into a structured session recap delivered to both the coach's AFFiNE workspace and the client's Telegram within 10 minutes of session end. The pipeline: (1) Studio Block uploads the recording to S3 via pre-signed URL on recording stop, (2) Whisper STT transcription via NVIDIA NIM container, (3) CCP agent (`Lena`, Session Intelligence Analyst) extracts key insights, action items, emotional beats, and topic clusters from the transcript, (4) AFFiNE Sync Service pushes the structured recap to the coach's Session Archive database, (5) Telegram bot sends a formatted summary (key takeaways + action items) to the client. The recap includes a "Session Mind Map" — an auto-generated Excalidraw diagram showing the conversation's topic flow, rendered via the existing Transparent Collage Pipeline (FR36) and embedded as an image in both AFFiNE and Telegram. The transcript and all extracted intelligence feed into the client's Context Premise graph (Neo4j) and the CRAL evidence pool, compounding the system's intelligence with every coaching session. *(Source: MCDA III #W6)*

- **FR-CA11-06 (Voice Note → Course Material Pipeline):** The system can convert a coach's Telegram voice note into a formatted lesson page in AFFiNE with an auto-generated Excalidraw concept diagram. The pipeline: (1) Coach sends a voice note to the CCP Telegram bot with the `/lesson` command prefix, (2) Whisper transcription, (3) the Learning Path Agent (`Gabrielle`) structures the transcript into a lesson format (title, key takeaways, detailed explanation, practical exercise) using the coach's Voice DNA (DEP-ENG-003) for tone consistency, (4) an Excalidraw concept diagram is auto-generated from the lesson's topic clusters using Benjamin (The Excalidraw Composer), (5) the lesson page + diagram are pushed to the coach's AFFiNE Content Library and tagged for the appropriate learning path. The coach's barrier to creating educational content drops to 90 seconds of talking into their phone. The system handles structuring, visualization, categorization, and delivery. *(Source: MCDA III #W11)*

- **FR-CA11-07 (Session-to-Course Auto Pipeline):** The system can convert a series of recorded coaching sessions (via CCP Studio) into a structured drip-fed course delivered through the client's AFFiNE workspace and Telegram. The pipeline: (1) Multiple Studio session recordings are transcribed and structured by `Lena` (FR-CA11-05), (2) the Learning Path Agent groups related sessions by topic cluster and chronological progression, (3) each session becomes a "chapter" with timestamps linking to key moments, (4) the Telegram bot delivers daily/weekly course drips — a snippet from the relevant chapter with a link to the full lesson in the client's AFFiNE workspace. The drip schedule is calibrated to the client's Atlas roadmap (4+1+2 structure) — active learning on active days, reflection prompts on reflection days, no drips on rest days. The coach never sits down to "create a course." Their coaching sessions automatically become structured learning material. *(Source: MCDA III #W7)*

- **FR-CA11-08 (Live Coaching → Content Machine Pipeline):** The system can extract 10+ content assets from a single coaching session recording. The pipeline: (1) Studio session recording is transcribed (Whisper/NIM), (2) `Lena` extracts the full Session Intelligence Report (recap, action items, topic clusters, emotional beats), (3) the CCF Expression Department agents (`Julio` for micro-content, `Cesare` for scripts) receive the Session Intelligence Report as a content source alongside the standard CRAL research, (4) Julio extracts 5-8 content snippets (Telegram-ready insight cards, Instagram caption drafts, short-form video script candidates) from the session's key moments, (5) Cesare evaluates the session's insights against the current weekly CCF batch, flagging any that qualify as Content Calendar entries. All extracted content passes through the standard Triple-Pass Validation Gate (Sophia/Marcus/Chen) and Receipt Chain Guard before delivery to AFFiNE. The coach's 60-minute call retroactively becomes the most productive content creation session of their week — without them doing anything different. *(Source: MCDA III #W1)*

### 4.3 Client Accountability & Intelligence Workflows

- **FR-CA11-09 (Accountability Check-in System with AFFiNE Visualization):** The system can deliver daily accountability prompts via Telegram, store responses in AFFiNE client databases, and auto-render Excalidraw progress charts. The pipeline: (1) Atlas (FR32) sends the daily ritual prompt via Telegram at the client's configured time, (2) client response is processed by the CBCS agent swarm (Aria extracts Context Premise updates, Miriam runs LIWC-22 analysis, the Change Talk Detector scans for commitment language), (3) behavioral data (energy rating, habit completion, mood state) is stored in the client's AFFiNE workspace dashboard via the Sync Service, (4) weekly, the system auto-renders an Excalidraw progress chart (line graph with streaks, trends, milestone badges) via Benjamin and embeds it in the client's AFFiNE Progress Board. Every response simultaneously feeds: (a) the Neo4j Context Premise graph, (b) the CPSC readiness calculations, (c) the tribe-level ICT distribution that drives CCF content strategy. The accountability loop is not just a retention tool — it is the primary intelligence collection mechanism for the entire commercial architecture. *(Source: MCDA III #W2)*

### 4.4 Visual Asset Production Integration

- **FR-CA11-10 (Excalidraw Embedded Workspace):** The system can embed Excalidraw canvases as native blocks within AFFiNE coach and client workspaces. Using BlockSuite's custom block API, the CCP fork registers an `excalidraw-embed` block type that renders a full Excalidraw canvas inline within any AFFiNE page. The canvas loads from a JSON state stored in AFFiNE's CRDT document layer. Coaches can view and interact with Excalidraw diagrams (tier lists, mind maps, visual recaps, progress charts, webinar slides) directly within their workspace without switching applications. The embed block supports read-only mode (for client workspaces viewing delivered assets) and edit mode (for coaches collaborating on visual content). Canvas state changes are persisted via YJS CRDT sync. *(Source: MCDA II #Excalidraw Resolution, ADR-04 parent PRD)*

- **FR-CA11-11 (CVE Canva Clone → AFFiNE Delivery):** The existing Conscious Canva App (FR-VIS-05) now delivers approved visual compositions directly to the coach's AFFiNE Visual Production Console instead of Notion. The `POST /api/compositions/approve` endpoint triggers `affine_sync.py` (replacing `notion_sync.py`) to push: individual slide PNGs, horizontal stitch image, ZIP download link, VPO metadata (TIAR decay audit, AGSS scores, Receipt Chain status, Fingerprint ID), and the "Why This Visual Was Built This Way" rationale. The Canva App's Approval Controls remain unchanged — Approve, Request Regeneration, Edit and Approve — but all delivery targets are AFFiNE workspace databases. *(Extends: FR-VIS-05, FR-VIS-06)*

- **FR-CA11-12 (Course Video Generation via CMF Pipeline):** The system can generate 5-10 minute learning/course videos using the existing CMF (Conscious Media Factory) pipeline, triggered by a coach's Telegram bot command (`/course-video`). Unlike short-form CMF clips (which require retention-edited B-rolls every 3-5 seconds), course videos use a simplified editorial template: clean captions, real image assets from the CVE image sourcing hierarchy (FR-VIS-09), Excalidraw diagrams rendered as visual aids, and mood-scored ambient audio from the CMF sound design engine. The Learning Path Agent (`Gabrielle`) categorizes completed course videos and pushes them to the appropriate learning journey in the client's AFFiNE workspace. The coach's voice note or session recording provides the raw material; the CMF pipeline handles production; the Learning Path Agent handles organization and delivery. *(Source: CMF Pipeline Documentation, User requirement)*

### 4.5 CCP Studio Platform [Replaces OBS Integration Layer — ADR-07]

> **Note:** This section replaces the former §4.5 (OBS Integration Layer, FR-CA11-13/14). OBS is retired as a required dependency per ADR-07. The following FRs define the native CCP Studio Block and its associated subsystems.

- **FR-CA11-13 [RETIRED]:** ~~OBS Recording Pipeline Controller~~ — Superseded by FR-CA11-16. The `obs_controller.py` tool is deprecated. OBS WebSocket integration is available as optional fallback only.

- **FR-CA11-14 [RETIRED]:** ~~Excalidraw Live OBS Annotation Overlay~~ — The Excalidraw overlay functionality is absorbed into FR-CA11-16's asset panel, which allows coaches to click-to-display Excalidraw diagrams and visual assets directly on the recording canvas without OBS scene switching.

- **FR-CA11-16 (CCP Studio Block — Full Stack Recording & Streaming):** The system provides a native AFFiNE BlockSuite plugin (`ccp-blocks/studio-block/`) that enables integrated recording, streaming, teleprompter, and asset management directly inside the coaching workspace. The Studio Block is activated by typing `/studio` in any AFFiNE page. It supports 5 recording modes: (1) YouTube Long-Form (1080p/720p, 16:9, webcam+screen+assets), (2) Shorts/Vertical (1080p mandatory, 9:16, webcam-only), (3) Webinar/Live Stream (RTMP restreaming via TribeNest extraction to YouTube Live/Facebook Live/Custom RTMP with parallel S3 VOD archive), (4) Course Video (webcam+Excalidraw diagrams+presentation), (5) Loom-Style Quick (720p, webcam bubble+screen, no CMF editorial). Each recording mode triggers its designated CMF Pipeline editorial template on upload completion. The teleprompter component auto-scrolls AFFiNE page content with adjustable speed (1.0–5.0 w/s), font size, and mirror mode. The asset panel surfaces visual assets from the current AFFiNE page for click-to-display during recording. The streaming engine is extracted from TribeNest (`ccp-stream-service` Docker container on AWS) — browser sends MediaRecorder chunks via WebSocket, service repackages to RTMP. *(Source: MCDA IV §III-IV, FB-STUDIO-03. Replaces: FR-CA11-13, FR-CA11-14)*

- **FR-CA11-17 (Studio Soundboard & Programmable Audio):** The Studio Block includes a live soundboard with 5 programmable SFX slots (default: drumroll, comedy horn, applause, record scratch, level-up chime) and 4 programmable music buttons (intro, outro, celebration, sad/dramatic). All sounds are customizable from an S3-hosted royalty-free audio library or coach uploads. Audio is mixed via Web Audio API (AudioContext + GainNode) — voice, SFX, and music are independently volume-controlled and merged into the MediaRecorder/WebSocket stream. Tracks fade in/out automatically (500ms linear). Only one music track plays at a time. Settings are saved per coach in `studio_preferences` (JSONB). *(Source: FB-STUDIO-03 §3.7)*

- **FR-CA11-18 (Conscious Social Scheduling & Performance Analysis):** The system provides a self-hosted social media scheduling and performance tracking engine, replacing the Publer dependency (FR43). Architecture: a self-hosted open-source scheduler (Postiz or Mixpost, Docker on AWS) with a CCP integration layer. The scheduler receives post-ready content from the CMF Pipeline via API, queues it for optimal-time publishing across Instagram, YouTube, TikTok, LinkedIn, and X (Twitter). Post-publish, the scheduler collects engagement metrics (views, likes, shares, comments, saves, CTR) over 6/24/48/168-hour collection cycles and stores them in `social_performance` (Supabase). An AFFiNE "Social Media OS" template renders performance dashboards, best-performing content cards, and cross-platform comparisons. CRAL agents receive performance feedback to optimize future content strategy. *(Source: MCDA IV §IX, FB-STUDIO-01)*

- **FR-CA11-19 (Interactive Trivianar Engine):** The system provides a stateless Python/FastAPI microservice (~560 lines) that delivers live trivia, polls, qualifying assessments, and microcommitment prompts through the Telegram Bot API during CCP Studio livestreams. Game modes: Countdown Trivia (speed-scored), Team Mode, Multi-Round, Points Wagering, Survivor, Live Polls. **Qualifying Questions** are dual-purpose — surface layer is entertainment, hidden layer maps responses to CBCS behavioral model parameters via `cbcs_mapping` JSON. The engine includes a Reaction Stickers & GIF Atmosphere Layer (pre/post-question reactions from customizable S3 media pools) and Threaded Media (question images/videos sent as thread replies to keep main chat clean). A Stream Overlay Layer (React component) renders question displays with countdown bars, color-coded answer distribution, leaderboard slide-ins, and winner reveal animations with confetti on the stream canvas. All responses are permanently stored and processed by CBCS agents (ICT Mapper, Change Talk Vault) asynchronously. *(Source: MCDA IV §X, FB-STUDIO-02)*

- **FR-CA11-20 (Trivianar Lead Generation Viral Loop):** The Trivianar Engine captures leads from non-member participants who join Telegram trivia sessions via member invitations. Data capture: `user.id`, `user.first_name` (automatic on group join), phone number via `request_contact` in bot DM (post-stream, consent-required), email via conversational prompt. Every lead arrives with behavioral data attached (trivia scores, qualifying question CBCS mappings, participation frequency). Leads enter the Conscious Nurturing Architecture (FR-CBCS-14) with a warm start — partial coping trajectory estimated before first 1:1 interaction. 21-day commercial cooldown enforced before any CPSC conversion evaluation. *(Source: MCDA IV §XI, FB-STUDIO-02 §5)*

- **FR-CA11-21 (Studio Guest Join):** The Studio Block supports at least 1 remote guest joining a recording or stream via WebRTC peer-to-peer connection. Coach generates a time-limited invite link, guest opens in browser → webcam/mic permission → WebRTC connection via `ccp-stream-service` signaling. Guest video composites onto the stream canvas in PiP (picture-in-picture) or side-by-side layout (coach-switchable). Guest audio mixed via Web Audio API. Coach controls: mute guest, resize/reposition, switch layout, disconnect. Use cases: testimonial videos, expert interviews, co-coaching sessions, hot-seat demonstrations. MVP: 1 guest maximum; multi-guest (3+) is post-MVP. *(Source: FB-STUDIO-03 §3.8)*

- **FR-CA11-22 (Studio Stream Overlay & Trivianar Display):** During webinar/live stream mode, the Studio Block renders a semi-transparent React overlay (`<TriviaOverlay />`) on the stream canvas, driven by WebSocket events from the Trivianar Engine. Overlay components: (1) Question display with countdown bar and color-coded answer distribution bars, (2) Leaderboard panel (slides in from right) showing top 5 participants, (3) Winner reveal animation (sequential 3rd→2nd→1st with confetti via `canvas-confetti`). The overlay uses Framer Motion for transitions and is automatically DPA-branded (FR-CA11-15) to match the coach's visual identity. *(Source: FB-STUDIO-02 §4b, FB-STUDIO-03)*

---

## 5. New Agent Roster (Capability Area 11)

| Agent | Department | Mandate |
|---|---|---|
| `Gabrielle` (Learning Path Agent) | Strategy | Categorizes all content by topic cluster, difficulty, program tag. Maintains `learning_path_registry`. Builds and updates structured learning journeys in client AFFiNE workspaces. |
| `Lena` (Session Intelligence Analyst) | Perception | Processes Studio/OBS session recordings. Extracts key insights, action items, emotional beats, topic clusters. Produces Session Intelligence Reports that feed CCF, CRAL, and CPSC. |
| `Pierre` (AFFiNE Workspace Orchestrator) | Management | Manages workspace provisioning (coach + client), template deployment, and AFFiNE Sync Service coordination. Handles workspace lifecycle (creation, archival, deletion on coach exit). |
| `Noémie` (Content Gating Agent) | Strategy | Enforces program-based content gating rules in client workspaces. Queries `coping_trajectory` and `atlas_roadmap` to determine content visibility per client. Updates access rules as client progresses. |
| `Marco` (Trivianar Engine Operator) | Engagement | Manages the Interactive Trivianar Engine during livestreams. Orchestrates question sequencing, leaderboard computation, reaction atmosphere, and qualifying question CBCS mapping delivery to ICT agents. |
| `Sofia` (Social Performance Analyst) | Strategy | Ingests social media performance metrics from the Conscious Social Scheduler. Identifies top-performing content patterns, feeds insights back to CRAL for evidence-based content optimization. Renders performance dashboards in AFFiNE Social Media OS. |
| `Diego` (Studio Session Conductor) | Production | Manages CCP Studio Block lifecycle: recording mode orchestration, stream health monitoring, soundboard state, guest join signaling, and post-recording CMF pipeline trigger coordination. |

**Updated Agent Count:** 76 → **83 named agents** across 6 departments.  
**Updated Capability Areas:** 10 → **11**.

---

## 6. New Tool Stack (Capability Area 11)

| Tool | Purpose |
|---|---|
| `affine_sync.py` | FastAPI-based sync service replacing `notion_sync.py`. Webhook-driven event propagation from CCP backend to AFFiNE workspaces. Idempotent push operations. Event log in Supabase. |
| ~~`obs_controller.py`~~ | **DEPRECATED.** OBS WebSocket API (v5) controller. Retained as optional fallback only. Superseded by CCP Studio Block. |
| `excalidraw_embed.py` | Utility for generating Excalidraw JSON states (progress charts, mind maps, concept diagrams) from CCP data structures. |
| `learning_path_builder.py` | Maintains `learning_path_registry` table. Categorizes content, builds journey timelines, calculates next-recommended content per client. |
| `affine_backup.py` | Daily automated backup of AFFiNE Docker volumes to S3. Retention: 30 days rolling. |
| `ccp-blocks/studio-block/` | React/TypeScript AFFiNE BlockSuite plugin. Contains: webcam/screen capture, teleprompter, soundboard, asset panel, guest join, stream overlay, Trivianar display. |
| `trivianar_engine.py` | Python/FastAPI microservice. Telegram Bot API integration for live trivia, polls, qualifying questions, microcommitments, reaction atmosphere, leaderboard. |
| `social_scheduler.py` | FastAPI integration layer connecting CMF Pipeline outputs to self-hosted social scheduler (Postiz/Mixpost). Handles post queuing, publish triggers, performance metric ingestion. |
| `ccp-stream-service` | Node.js/Express Docker container. WebSocket→RTMP relay (TribeNest extraction). Handles multi-destination streaming, S3 VOD archive, WebRTC guest signaling, stream health metrics. |

---

## 7. New Data Infrastructure

| Table | Primary Key | Purpose |
|---|---|---|
| `learning_path_registry` | `content_id` (UUID) | Maps every content piece to its position in learning journeys. Fields: `content_type`, `topic_cluster`, `difficulty_level`, `program_tag`, `journey_id`, `sequence_position`, `created_at`. |
| `affine_sync_events` | `event_id` (UUID) | Audit log for all AFFiNE sync operations. Fields: `event_type`, `target_workspace_id`, `payload_hash`, `status`, `timestamp`, `receipt_chain_id`. |
| `session_intelligence` | `session_id` (UUID) | Stores Session Intelligence Reports from Studio/OBS recordings. Fields: `recording_url`, `transcript_url`, `key_insights`, `action_items`, `topic_clusters`, `emotional_beats`, `coach_id`, `client_id`. |
| `studio_sessions` | `id` (UUID) | CCP Studio recording sessions. Fields: `coach_id`, `source_page_id`, `recording_mode`, `resolution`, `s3_recording_url`, `s3_vod_url`, `is_stream`, `stream_destinations`, `cmf_pipeline_template`, `status`. |
| `studio_preferences` | `id` (UUID) | Per-coach soundboard and audio configuration. Fields: `sfx_slots` (JSONB), `music_tracks` (JSONB), `guest_layout`. |
| `studio_guest_sessions` | `id` (UUID) | Guest join sessions for Studio recordings/streams. Fields: `session_id`, `guest_name`, `join_token`, `layout_mode`, `status`. |
| `stream_analytics` | `id` (UUID) | Webinar/stream viewer analytics. Fields: `session_id`, `peak_viewers`, `total_unique_viewers`, `trivia_participation_rate`, `leads_captured`. |
| `trivia_questions` | `id` (UUID) | Trivia questions generated by CRAL agents. Fields: `surface_text`, `answer_options` (JSONB with `cbcs_mapping`), `correct_answer`, `dimension`, `difficulty`, `time_limit_seconds`. |
| `trivia_responses` | `id` (UUID) | One row per user per question. Fields: `user_id`, `question_id`, `stream_id`, `answer`, `is_correct`, `score`, `response_time_ms`, `team_id`. |
| `trivia_leaderboard` | `(user_id, coach_id)` | Materialized leaderboard. Fields: `total_score`, `games_played`, `win_count`, `current_streak`, `longest_streak`. |
| `trivia_leads` | `id` (UUID) | Leads captured from trivia viral loop. Fields: `telegram_user_id`, `phone_number`, `email`, `referred_by_user_id`, `cbcs_initial_assessment` (JSONB), `nurture_status`. |
| `social_posts` | `id` (UUID) | Social media post tracking. Fields: `coach_id`, `content_id`, `platform`, `scheduled_at`, `published_at`, `status`. |
| `social_performance` | `id` (UUID) | Engagement metrics per post. Fields: `post_id`, `views`, `likes`, `shares`, `comments`, `saves`, `ctr`, `collection_cycle`, `collected_at`. |

---

## 8. Non-Functional Requirements Extension

### Performance

| Context | Requirement | Rationale |
|---|---|---|
| AFFiNE Sync push | Batch delivery to AFFiNE workspace: **<30 seconds** for full weekly content calendar | Self-hosted instance eliminates Notion's 3 req/s rate limit. |
| ~~OBS WebSocket command~~ | ~~Start/stop recording latency: <200ms~~ | **Superseded by CCP Studio Block.** |
| Studio recording start | Recording/streaming initiation: **<500ms** from button click | Browser WebRTC setup time. |
| Streaming latency | Glass-to-glass: **<3 seconds** for RTMP restreaming | WebSocket→RTMP relay via ccp-stream-service. |
| Trivianar response | Button click to leaderboard update: **<200ms** | Telegram webhook + PostgreSQL INSERT. |
| Session Intelligence Report | Transcript + extraction complete: **<10 minutes** post-recording | Client and coach expect near-immediate session recap. |
| Learning Path update | Content categorization + workspace push: **<60 seconds** per content piece | New content should appear in client workspace as soon as it's approved. |
| Social performance ingestion | Engagement metrics collected: **6h / 24h / 48h / 168h** post-publish | Scheduler API polling cycles. |
| Excalidraw progress chart render | Weekly chart generation: **<30 seconds** per client | Batch rendering of charts for all clients within maintenance window. |

### Reliability

- **AFFiNE Uptime Target:** 99.5% (matching CBCS uptime). Coach workspace is the primary interaction surface — downtime directly impacts coach trust.
- **AFFiNE Backup:** Daily automated backup to S3 via `affine_backup.py`. Full recovery from backup achievable within **<2 hours**.
- **CCP Studio Recording Resilience:** If a Studio Block recording fails mid-session (browser crash, network drop), the IndexedDB chunk buffer retains all 5-second Blobs recorded up to the failure point. On next Studio Block load, the system detects orphaned chunks and offers recovery upload to S3. Recording pipeline failure is non-blocking for all other CCP operations. OBS is available as an optional fallback for power users but is not architecturally required (ADR-06 RETIRED, see ADR-07).

### Security

- **Client Workspace Isolation:** Each client workspace is provisioned as an isolated AFFiNE workspace. No client can access another client's workspace. Coach can view all client workspaces via the Coach Workspace aggregation view.
- **Content Gating Enforcement:** Program-tagged content is gated at the workspace template level — content blocks that are not yet unlocked do not exist in the client's workspace (not hidden, absent). This prevents URL manipulation bypasses.

---

## 9. Updated Integration Perimeters

| Channel | Direction | Integration | Notes |
|---|---|---|---|
| **AFFiNE** | System ↔ Coach/Client | Content Calendar, Client Intelligence, Visual Assets, Learning Paths, Session Archives, Social Media OS | Via `affine_sync.py`. Replaces `notion_sync.py`. Self-hosted Docker on AWS EC2. |
| **CCP Studio Block** | Coach → System | Recording, streaming, teleprompter, soundboard, guest join | Native AFFiNE BlockSuite plugin. WebRTC + Web Audio API. Replaces OBS. |
| **ccp-stream-service** | System → External | RTMP restreaming to YouTube Live, Facebook Live, Custom RTMP | Docker container on AWS. WebSocket→RTMP relay. TribeNest extraction. |
| **Trivianar Engine** | System ↔ Telegram | Live trivia, polls, qualifying questions, reactions, leaderboard | Python/FastAPI microservice. Telegram Bot API webhooks. |
| **Social Scheduler** | System → Social Platforms | Post queuing, publishing, performance metric collection | Self-hosted Postiz/Mixpost. API integration layer via `social_scheduler.py`. |
| ~~**OBS Studio**~~ | ~~System → Coach Machine~~ | ~~Recording control, scene switching~~ | **DEPRECATED.** Optional fallback only. Superseded by CCP Studio Block. |
| **Excalidraw (Embedded)** | System → AFFiNE | Progress charts, mind maps, concept diagrams, session recaps | Via BlockSuite custom `excalidraw-embed` block. JSON state in CRDT layer. |
| **Telegram** | Client ↔ CBCS | Voice notes, rituals, accountability prompts, session recaps, course drips, Trivianar interactions | Extended with `/studio`, `/lesson`, `/join-trivia` commands. |
| **CVE Canva App** | System → AFFiNE | Visual composition delivery | Output target changed from Notion to AFFiNE via `affine_sync.py`. App internals unchanged. |
| **CMF Pipeline** | System → AFFiNE/Telegram | Course video generation, learning content delivery | Extended with Studio recording mode triggers. Output delivered to client AFFiNE workspace. |

---

## 10. Phased Build Sequence

### Phase 1: AFFiNE Core (Weeks 1-4)

| Step | What Gets Built | Depends On |
|---|---|---|
| 11.1 | Fork AFFiNE → Apply CCP brand theme (CSS overlay + logo + color tokens) | Nothing |
| 11.2 | Deploy AFFiNE Docker on AWS EC2 via Dockploy + SSL + domain | 11.1 |
| 11.3 | Build `affine_sync.py` (FastAPI Sync Service) + `affine_sync_events` table | 11.2 |
| 11.4 | Build coach workspace master template (8 sections) | 11.2 |
| 11.5 | Migrate FR45 delivery from `notion_sync.py` to `affine_sync.py` | 11.3 + 11.4 |

### Phase 2: Client Workspace + Learning Paths (Weeks 5-8)

| Step | What Gets Built | Depends On |
|---|---|---|
| 11.6 | Build client workspace template (dashboard, journal, resources) + content gating logic | 11.5 |
| 11.7 | Build `learning_path_builder.py` + `learning_path_registry` table | 11.6 |
| 11.8 | Build Learning Path Agent (`Gabrielle`) + Content Gating Agent (`Noémie`) | 11.7 |
| 11.9 | Build Voice Note → Course Material pipeline (FR-CA11-06) | 11.7 + 11.8 |
| 11.10 | Build Accountability Check-in → AFFiNE visualization pipeline (FR-CA11-09) | 11.6 + FR32 |

### Phase 3: OBS + Excalidraw + Course Video (Weeks 9-12)

| Step | What Gets Built | Depends On |
|---|---|---|
| 11.11 | Build `obs_controller.py` + Telegram `/record-*` commands | Existing CBCS |
| 11.12 | Build Session Intelligence Analyst (`Lena`) + `session_intelligence` table | 11.11 |
| 11.13 | Build AI Session Recap Generator pipeline (FR-CA11-05) | 11.12 |
| 11.14 | Build Excalidraw embed block (BlockSuite custom block) | 11.2 |
| 11.15 | Build Course Video Generation via CMF pipeline (FR-CA11-12) | 11.8 + CMF Pipeline |
| 11.16 | Build Session-to-Course Auto Pipeline (FR-CA11-07) | 11.12 + 11.8 |
| 11.17 | Build Live Session → Content Machine pipeline (FR-CA11-08) | 11.12 + CCF |
| 11.18 | Build Excalidraw Live OBS Annotation Overlay (FR-CA11-14) | 11.11 + 11.14 |

### Phase 4: CCP Studio Platform (Weeks 13-18)

| Step | What Gets Built | Depends On |
|---|---|---|
| 11.19 | Build CCP Studio Block (React/BlockSuite plugin: webcam, screen, teleprompter, asset panel) | 11.2 |
| 11.20 | Extract TribeNest streaming core → `ccp-stream-service` Docker container | Nothing |
| 11.21 | Build soundboard + programmable audio (Web Audio API mixing, S3 audio library) | 11.19 |
| 11.22 | Build guest join (WebRTC peer-to-peer, signaling via ccp-stream-service) | 11.19 + 11.20 |
| 11.23 | Build Trivianar Engine (Python/FastAPI, Telegram Bot API, reaction atmosphere, threaded media) | Existing CBCS |
| 11.24 | Build stream overlay (React `<TriviaOverlay />`, question/leaderboard/winner animations) | 11.19 + 11.23 |
| 11.25 | Build Trivia lead capture viral loop (bot DM flow, contact request, nurture pipeline entry) | 11.23 |
| 11.26 | Deploy self-hosted social scheduler (Postiz/Mixpost Docker) + `social_scheduler.py` integration | Nothing |
| 11.27 | Build AFFiNE Social Media OS template (performance dashboards, content cards) | 11.26 + 11.2 |
| 11.28 | Integrate Studio recording outputs → CMF Pipeline editorial templates | 11.19 + CMF Pipeline |
| 11.29 | Retire `obs_controller.py`, update `PROMPT_Spec_Build.md`, deprecate ADR-06 | 11.19 verified |

---

## 11. Risk Mitigation Matrix Extension

| Risk | Description | Mitigation |
|---|---|---|
| **AFFiNE Upstream Divergence** | Thin fork diverges from upstream, making future merges impossible | Thin fork discipline: custom code only in `ccp-theme/` and `ccp-blocks/`. Monthly upstream rebase. Automated merge conflict detection CI. |
| **Self-Hosting Operational Overhead** | Managing Docker, SSL, backups, upgrades manually | Dockploy handles Docker orchestration. `affine_backup.py` automates daily S3 backups. Let's Encrypt auto-renews SSL. Monthly upgrade playbook (test on staging → promote to prod). |
| ~~**OBS Local Dependency**~~ | ~~OBS must run on coach's machine~~ | **RETIRED RISK.** CCP Studio Block eliminates the OBS dependency entirely. OBS is optional fallback only. |
| **Browser MediaRecorder Quality Ceiling** | Browser-based recording capped at 1080p30, codec limitations | Start with browser quality; evaluate Electron/Tauri native capture wrapper if insufficient. Shorts mode (1080p mandatory) is the most demanding — test first. |
| **WebSocket Streaming Latency** | >3s glass-to-glass latency degrades live experience | Deploy ccp-stream-service in same AWS region as AFFiNE. WebSocket chunk size optimization. Fallback: direct RTMP from browser via Wowza-style relay. |
| **Guest WebRTC NAT Traversal** | Guest behind corporate firewall can't establish peer connection | TURN server (coturn on AWS) for restrictive firewalls. STUN handles most residential cases. |
| **Trivianar Concurrency** | 500+ simultaneous trivia responses overwhelm PostgreSQL | Redis queue (`LPUSH trivia_responses:{question_id}`) drains into batch INSERT. Each webhook = atomic INSERT, no read-modify-write patterns. |
| **Audio Sync Drift** | Soundboard SFX/music drifts from voice track over long streams | Web Audio API timestamp synchronization. 500ms fade transitions mask minor drift. |
| **Social Scheduler Uptime** | Self-hosted scheduler goes down, posts don't publish | Docker health checks + auto-restart. Queue persistence (posts don't vanish on restart). Monitoring via CloudWatch. |
| **Content Gating Bypass** | Client manipulates workspace to access locked content | Gating by absence (content blocks don't exist until unlocked), not by hiding. No URL to share. New content blocks are provisioned by the Sync Service when the client reaches the gating threshold. |
| **AFFiNE CRDT Conflict Resolution** | Concurrent edits from coach + Sync Service cause CRDT merge conflicts | Sync Service writes are tagged with `system` authorship and operate on system-owned database blocks (not free-text pages). Coach edits and system pushes target different block namespaces — they never write to the same CRDT node. |
| **Course Video Quality @ Scale** | CMF pipeline optimized for short-form; 5-10 min course videos untested | Course video template uses simplified editorial rules (no retention B-rolls, just captions + images + diagrams). First 50 course videos manually reviewed before autonomous production enabled. |

---

## 12. Success Criteria Extension

| Criterion | Target | Measurement |
|---|---|---|
| **Notion Retirement** | 100% of coach delivery migrated to AFFiNE within 60 days of Phase 1 completion | `notion_sync.py` call count drops to 0 in Supabase logs. |
| **OBS Retirement** | 100% of new recordings via CCP Studio Block within 30 days of Phase 4 launch | `studio_sessions` count vs. `obs_controller` call count. |
| **Client Workspace Activation** | ≥80% of CBCS members access their AFFiNE workspace at least 2× per week | AFFiNE analytics + Sync Service event logs. |
| **Learning Path Completion** | Clients progress through ≥3 learning path nodes per 30-day period | `learning_path_registry` completion events. |
| **Session Recap Delivery** | 100% of Studio-recorded sessions produce a recap within 10 minutes | `session_intelligence` table timestamps. |
| **Content Multiplication Ratio** | Each coaching session produces ≥8 downstream content assets | Fingerprint Archive cross-reference: session recording ID → derived content count. |
| **Course Video Production** | First 10 course videos produced and categorized within 2 weeks of Phase 3 launch | `learning_path_registry` entries with `content_type = course_video`. |
| **Stream Engagement** | ≥60% of live viewers participate in at least one trivia round | `trivia_responses` count / stream viewer count. |
| **Trivia CBCS Intelligence** | Qualifying questions update ≥40% of participant coping trajectories per stream | ICT Mapper update log post-stream. |
| **Lead Capture Rate** | ≥25% of new trivia group joiners share contact via bot DM | `trivia_leads` creation rate. |
| **Social Performance Tracking** | 100% of published posts have engagement metrics collected within 7 days | `social_performance` table coverage. |
| **Recording Quality** | ≥95% of Studio recordings pass CMF quality gate on first attempt | CMF pipeline rejection rate. |
| **Streaming Reliability** | ≥99% uptime for ccp-stream-service | CloudWatch metrics. |

---

*End of PRD Update — Capability Area 11. This document extends the parent PRD (v1.0, Capability Areas 0–10) and should be read as an addendum. All FRs, ADRs, and architectural mandates from the parent PRD remain in force unless explicitly superseded above.*
