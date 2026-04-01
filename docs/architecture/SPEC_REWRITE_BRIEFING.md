# Spec Rewrite Briefing — CCP Studio Architectural Pivot

**For:** Tech-Writer Agent (Paige) or Spec Architect Agent  
**Date:** 2026-03-25  
**Priority:** HIGH — These spec rewrites are blocking Phase 4 Studio build execution (Steps 21–23)  
**Context:** The PRD (`docs/prd/prd-update-CA11-quad-platform.md`) has been updated to reflect the CCP Studio pivot. The existing spec files in `docs/architecture/` are now partially obsolete and need rewriting.

---

## 1. What Changed and Why

### The Pivot: OBS → Native CCP Studio Block

**ADR-06 (OBS WebSocket Integration) has been RETIRED** and replaced by **ADR-07 (Native CCP Studio Block).**

Previously, CA11 §4.5 defined two OBS-dependent FRs:
- FR-CA11-13: OBS Recording Pipeline Controller (`obs_controller.py`)
- FR-CA11-14: Excalidraw Live OBS Annotation Overlay

These assumed OBS Studio running on the coach's local machine, controlled remotely via WebSocket commands from Telegram. This created three structural problems:
1. **Context switching** — coach leaves AFFiNE to manage a separate desktop application
2. **No intelligence integration** — OBS has zero awareness of CCP data layer (scripts, assets, CMF templates)
3. **Local dependency** — coach's recording setup dies with their laptop

The replacement is a **native AFFiNE BlockSuite plugin** (`ccp-blocks/studio-block/`) that embeds recording, streaming, teleprompter, soundboard, guest join, and interactive Trivianar overlay directly inside the coaching workspace. The MCDA IV analysis scored this at **442 vs 225 baseline** across 6 strategic amplifiers.

### Additionally, three new subsystems were added:
1. **Interactive Trivianar Engine** — Telegram-based live trivia/polls/qualifying questions during streams
2. **Conscious Social Scheduling** — Self-hosted scheduler replacing Publer (FR43)
3. **Studio Soundboard, Guest Join, and Stream Overlay** — atmospheric audio + remote guest participation + stream visuals

---

## 2. Specs That Need Action

### Specs to Mark as RETIRED (preserve for historical reference — do NOT delete)

| File | Reason |
|---|---|
| `FR-CA11-13_OBS_Recording_Controller_Tech_Spec.md` | **RETIRED.** `obs_controller.py` is deprecated. FR-CA11-13 is superseded by FR-CA11-16 (CCP Studio Block). Mark as retired at the top of the file, do NOT delete — preserve for historical reference. |
| `FR-CA11-14_Excalidraw_Live_OBS_Overlay_Tech_Spec.md` | **RETIRED.** Excalidraw overlay is now an asset panel feature inside the Studio Block (FR-CA11-16). Mark as retired, do NOT delete. |

### Specs to CREATE (New)

| New FR | File to Create | Source Documents | Complexity |
|---|---|---|---|
| **FR-CA11-16** | `FR-CA11-16_CCP_Studio_Block_Tech_Spec.md` | PRD §4.5 (FR-CA11-16), `FB_Full_Stack_Recording_Streaming.md` (FB-STUDIO-03) §3.1-3.6 | HIGH — This is the largest spec. Covers: BlockSuite plugin architecture, 5 recording modes, WebRTC capture, MediaRecorder encoding, canvas compositing, teleprompter, asset panel, recording pipeline → S3 → CMF trigger chain. |
| **FR-CA11-17** | `FR-CA11-17_Studio_Soundboard_Audio_Tech_Spec.md` | PRD §4.5 (FR-CA11-17), `FB_Full_Stack_Recording_Streaming.md` §3.7 | MEDIUM — Web Audio API mixing, 5 SFX slots, 4 music buttons, S3 audio library, `studio_preferences` table, volume control, fade transitions. |
| **FR-CA11-18** | `FR-CA11-18_Social_Scheduling_Performance_Tech_Spec.md` | PRD §4.5 (FR-CA11-18), `FB_Conscious_Social_Scheduling.md` (FB-STUDIO-01) | MEDIUM — Self-hosted scheduler deployment (Postiz/Mixpost), `social_scheduler.py` integration layer, performance metric ingestion, AFFiNE Social Media OS template, CRAL feedback loop. |
| **FR-CA11-19** | `FR-CA11-19_Interactive_Trivianar_Engine_Tech_Spec.md` | PRD §4.5 (FR-CA11-19), `FB_Interactive_Trivianar_Engine.md` (FB-STUDIO-02) §3.1-3.6 | HIGH — Python/FastAPI microservice, Telegram Bot API, 6 game modes, qualifying question CBCS mapping, reaction stickers/GIF atmosphere, threaded media, leaderboard, data model (4 tables). |
| **FR-CA11-20** | `FR-CA11-20_Trivianar_Lead_Capture_Tech_Spec.md` | PRD §4.5 (FR-CA11-20), `FB_Interactive_Trivianar_Engine.md` §5 | LOW — Bot DM flow, `request_contact`, `trivia_leads` table, Conscious Nurturing Architecture entry point. |
| **FR-CA11-21** | `FR-CA11-21_Studio_Guest_Join_Tech_Spec.md` | PRD §4.5 (FR-CA11-21), `FB_Full_Stack_Recording_Streaming.md` §3.8 | MEDIUM — WebRTC peer-to-peer, signaling via ccp-stream-service, PiP/side-by-side compositing, `studio_guest_sessions` table, invite link generation. |
| **FR-CA11-22** | `FR-CA11-22_Stream_Overlay_Trivianar_Display_Tech_Spec.md` | PRD §4.5 (FR-CA11-22), `FB_Interactive_Trivianar_Engine.md` §4b | MEDIUM — React `<TriviaOverlay />`, Framer Motion animations, WebSocket event-driven, question display, leaderboard, winner reveal with `canvas-confetti`, DPA branding integration. |

### Specs That Need MINOR Updates (Not Rewrites)

| File | What to Update |
|---|---|
| `FR-CA11-05_AI_Session_Recap_Generator_Tech_Spec.md` | Change references from "OBS recording" to "CCP Studio recording." Update S3 trigger source from `obs_controller.py` upload to Studio Block pre-signed URL upload. The pipeline logic itself is unchanged. |
| `FR-CA11-08_Content_Machine_Pipeline_Tech_Spec.md` | Change "OBS session recording" references to "Studio session recording." Pipeline logic unchanged. |
| `FR-CA11-12_Course_Video_CMF_Pipeline_Tech_Spec.md` | Update recording source from OBS to CCP Studio Block. Add note that Course Video mode is one of the 5 Studio recording modes. |
| `FR-CA11-15_Contextual_Branding_Dynamic_PAD_Tech_Spec.md` | Add note that DPA branding now extends to the Stream Overlay (FR-CA11-22) — the Trivianar overlay renders in the coach's brand colors/fonts. |

---

## 3. Spec Template Structure

Follow the existing CCP tech spec structure (as seen in existing specs like `FR-CA11-01` through `FR-CA11-12`):

```markdown
# Tech-Spec: FR-CA11-XX — [Title]

**Created:** [date]
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / PRD Update v2.0 — Capability Area 11)
**Architecture Reference:** PRD-Update-CA11 §4.5, ADR-07
**Skill Implementation:** [tool/file path]
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read
[List of source documents consumed]

## 2. Overview
### Problem Statement
### Solution
### Scope (In/Out)

## 3. Context for Development
### Architecture Traceability (DEP-IDs)
### Academic Grounding
### Technical Decisions

## 4. Implementation Plan
### Tasks (checkbox format)
### Acceptance Criteria (Given/When/Then)

## 5. Data Model
### Tables (CREATE TABLE statements)

## 6. Additional Context
### Dependencies
### Testing Strategy
### Notes
```

---

## 4. Critical Source Documents to Read

Before writing any spec, the agent MUST read these documents in this order:

1. **PRD (updated):** `docs/prd/prd-update-CA11-quad-platform.md` — §4.5 (CCP Studio Platform) contains all FR definitions
2. **Feature Brief — Recording/Streaming:** `docs/features/FB_Full_Stack_Recording_Streaming.md` — Full technical detail for FR-CA11-16, FR-CA11-17, FR-CA11-21
3. **Feature Brief — Trivianar Engine:** `docs/features/FB_Interactive_Trivianar_Engine.md` — Full technical detail for FR-CA11-19, FR-CA11-20, FR-CA11-22
4. **Feature Brief — Social Scheduling:** `docs/features/FB_Conscious_Social_Scheduling.md` — Full technical detail for FR-CA11-18
5. **MCDA IV:** `MCDA_CCP_Studio_Integration.md` — Strategic rationale for the entire pivot
6. **Build Protocol:** `docs/architecture/PROMPT_Spec_Build.md` — Understand the DEP-ID system, Receipt Chain integration, and build ledger format
7. **Existing spec examples:** `docs/architecture/FR-CA11-01_Coach_Workspace_Provisioning_Tech_Spec.md` — Reference for format, depth, and traceability patterns

---

## 5. DEP-ID Allocation Guide

New specs must allocate DEP-IDs for their components. Use the following ranges:

| FR | DEP-ID Range | Notes |
|---|---|---|
| FR-CA11-16 (Studio Block) | `DEP-ENG-087` through `DEP-ENG-093` | Plugin, recording engine, teleprompter, asset panel, S3 upload, CMF trigger |
| FR-CA11-17 (Soundboard) | `DEP-ENG-094` through `DEP-ENG-098` | SFX slots, music buttons, audio mixer, S3 library, preferences |
| FR-CA11-18 (Social Scheduling) | `DEP-ENG-099` through `DEP-ENG-103` | Scheduler deployment, integration layer, performance ingestion, dashboard |
| FR-CA11-19 (Trivianar Engine) | `DEP-ENG-104` through `DEP-ENG-113` | Engine core, game modes, qualifying questions, reactions, threaded media, leaderboard |
| FR-CA11-20 (Lead Capture) | `DEP-ENG-114` through `DEP-ENG-116` | Bot DM flow, contact request, nurture entry |
| FR-CA11-21 (Guest Join) | `DEP-ENG-117` through `DEP-ENG-121` | WebRTC signaling, PiP compositing, invite link, guest controls |
| FR-CA11-22 (Stream Overlay) | `DEP-ENG-122` through `DEP-ENG-126` | Overlay component, question display, leaderboard, winner reveal, DPA integration |

---

## 6. Execution Order (Recommended)

Write specs in build dependency order:

1. **FR-CA11-16** (Studio Block) — Foundation; everything else depends on this
2. **FR-CA11-17** (Soundboard) — Extends Studio Block with audio
3. **FR-CA11-21** (Guest Join) — Extends Studio Block with WebRTC
4. **FR-CA11-19** (Trivianar Engine) — Independent Python service
5. **FR-CA11-20** (Lead Capture) — Extends Trivianar with lead flow
6. **FR-CA11-22** (Stream Overlay) — Combines Studio Block + Trivianar
7. **FR-CA11-18** (Social Scheduling) — Independent infrastructure

Then apply minor updates to FR-CA11-05, FR-CA11-08, FR-CA11-12, FR-CA11-15.

---

## 7. New Agent Assignments

These 3 new agents need to be referenced in their respective specs:

| Agent | Department | Relevant Specs |
|---|---|---|
| `Marco` (Trivianar Engine Operator) | Engagement | FR-CA11-19, FR-CA11-20, FR-CA11-22 |
| `Sofia` (Social Performance Analyst) | Strategy | FR-CA11-18 |
| `Diego` (Studio Session Conductor) | Production | FR-CA11-16, FR-CA11-17, FR-CA11-21 |

---

## 8. Quality Gates

Each spec must pass these checks before being marked "Ready for Development":

- [ ] All DEP-IDs allocated and non-overlapping
- [ ] All data model tables include `CREATE TABLE` statements
- [ ] Architecture traceability maps to PRD §4.5 FR definitions
- [ ] Academic grounding includes at least 1 relevant framework reference
- [ ] Acceptance criteria use Given/When/Then format
- [ ] Dependencies explicitly list upstream and downstream FRs
- [ ] Receipt Chain integration specified (how does this spec's output get receipted?)
- [ ] Testing strategy includes unit test scope, integration test scope, and manual verification

---

*End of Spec Rewrite Briefing. This document should be the FIRST file read by any agent tasked with writing the Phase 4 tech specs.*
