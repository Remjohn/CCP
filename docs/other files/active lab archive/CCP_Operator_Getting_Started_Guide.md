# CCP Operator Getting-Started Guide
### The Conscious Coaching Platform — From Build to First Live Session

**Version:** 1.0 · **Date:** 2026-03-20 · **Build Status:** ALL PHASES COMPLETE ✅ (1,913 tests passing)

---

## 1. What You Just Built — The 30-Second Overview

The Conscious Coaching Platform (CCP) is a **multi-agent, single-tenant, cloud-native Trigger-First Operating System** that automates premium content creation, client relationship intelligence, and conversion systems for professional coaches. It is **not** a generic SaaS — every coach gets a fully isolated instance with their own code repository, databases, and agent environment.

The system is divided into **six capability pillars:**

| Pillar | What It Does | Key Sub-System |
|--------|-------------|----------------|
| **CCF** (Conscious Content Factory) | Weekly batch production of 36+ psychologically-routed scripts | JIT Skill Compiler (CCSB) |
| **CVE** (Conscious Visual Engine) | Post-script visual generation using 7 neurological design pillars | Abel → Aurore → Paradoxe → RunningHub → Canva App |
| **V²WS** (Webinar System) | Modular webinar generation — every slide engineered as a HOOK | YOLO Mode + Interactive Mode → Excalidraw JSON |
| **Tierlist** (Video Generators) | Weekly tier list & rating video ideas sent to coaches via Telegram | Vite+React frontend + Telegram bot + Excalidraw pipeline |
| **CBCS** (Conscious Bot Coaching System) | Client relationship intelligence via Telegram voice notes | 14 psychological protocols (SPT, DARN-CAT, ELM, CASA) |
| **CPSC** (Conscious Persuasion Sales Cycle) | Ethical conversion through temporal triggers and identity anchoring | Campaign Orchestrator (Samuel) + 72-Hour Protocol |

**What touches what:** CRAL (research) feeds CCF (scripts) feeds CVE (visuals), while CBCS (client intel) feeds back into CCF routing and triggers CPSC conversion windows. Everything delivers to the coach via **Notion** (zero-UI) and to clients via **Telegram** (invisible app).

---

## 2. Your Codebase — Full Folder Map

```
The Conscious Coaching Factory/
│
├── src/ccp/                          ← THE CORE APPLICATION
│   ├── models/          (42 files)   — Pydantic data models for every sub-system
│   ├── services/        (176 files)  — Business logic (adapters, engines, validators, agents)
│   ├── pipelines/       (15 files)   — End-to-end orchestration flows (Genesis, Weekly, CRAL, etc.)
│   ├── extensions/      (1 file)     — Content cadence extension
│   ├── agents/                       — Agent orchestration configs
│   ├── api/                          — FastAPI endpoints (main:app on port 8000)
│   ├── commands/                     — CLI command handlers
│   ├── core/                         — Shared utilities, config loading, base classes
│   ├── scripts/                      — Automation scripts
│   └── tools/                        — Internal tool integrations
│
├── skills/                           ← JIT SKILL FILES (the "micro-prompts")
│   ├── ccf/
│   │   ├── content/                  — Content generation skills
│   │   ├── distillation/             — Voice DNA distillation skills
│   │   ├── distribution/             — Platform distribution skills
│   │   ├── eroll/                    — E-Roll research skills
│   │   ├── orchestration/            — Pipeline orchestration skills
│   │   ├── production/               — Batch production skills
│   │   ├── research/                 — CRAL research skills (M1-M7)
│   │   ├── setup/                    — Genesis & onboarding skills
│   │   ├── validation/               — Quality gate skills
│   │   └── visual-recipes/           — Visual composition templates
│   ├── v2ws/                         ← V²WS WEBINAR SKILLS (9 areas)
│   │   ├── close/                    — Webinar closing sequences
│   │   ├── content/                  — Core webinar content modules
│   │   ├── intro/                    — Opening hooks
│   │   ├── meme/                     — Memetic engagement integration
│   │   ├── orchestration/            — Webinar flow orchestration
│   │   ├── research/                 — Webinar topic research
│   │   ├── transition/               — Slide transition logic
│   │   ├── visual/                   — Webinar visual composition
│   │   └── voice/                    — Voice/tone matching for webinars
│   └── visual/
│       └── excalidraw-composer/      — Excalidraw assembly skill (20KB SKILL.md)
│
├── config/
│   └── visual_pipeline/              — Format constraints + style scope matrices (JSON)
│
├── coaches/                          ← PER-COACH DATA (16 coaches currently registered)
│   ├── AAA/, BBB/, JP/, MAR/...      — Each coach gets their own isolated directory
│   └── [COACH_ID]/
│       ├── coach_soul.json           — 3D Voice DNA (Positive Space + Negative Space + Emotional DNA)
│       ├── trigger_map.json          — Extracted trigger map
│       └── leadership_scorecard.json — Leadership trait profile
│
├── tools/                            ← UTILITY SCRIPTS & STANDALONE APPS
│   ├── firecrawl_wrapper.py          — Forum scraping for CRAL research
│   ├── transcribe_voice.py           — Whisper audio transcription
│   ├── sentiment_wrapper.py          — Sentiment analysis utility
│   ├── google_trends_wrapper.py      — Trend data fetching
│   ├── archetype_registry.py         — 7-archetype family registry
│   ├── telegram-tierlist-bot/        ← TIERLIST TELEGRAM BOT
│   │   ├── bot.py                    — CLI entry point (--coach, --dry-run, --test)
│   │   ├── generator.py              — Idea generation via OpenRouter + archetypes
│   │   ├── formatter.py              — Telegram message formatting
│   │   └── scheduler.py              — Cron-like daily delivery scheduler
│   └── tierlist-app/                 ← TIERLIST VITE+REACT FRONTEND
│       ├── src/App.jsx               — Main React UI component
│       ├── dist/                     — Pre-built production bundle
│       └── package.json              — Vite + React dependencies
│
├── tests/integration/                ← 1,913 INTEGRATION TESTS (all passing)
│
├── docker/
│   ├── Dockerfile                    — Python 3.11-slim + ffmpeg
│   └── docker-compose.yml            — CCP app + Redis + Neo4j stack
│
├── docs/                             ← ARCHITECTURE & PRD DOCUMENTATION
│   ├── architecture/                 — Tech specs, stress test, build guides
│   └── prd/                          — Product Requirements Document
│
├── .env                              ← API KEYS (16 services configured)
├── requirements.txt                  ← Python dependencies (12 packages)
└── RUN_PIPELINE.ps1                  ← PowerShell pipeline runner (for CMF Pipeline)
```

---

## 3. External Systems & API Setup

Your `.env` file already contains keys for 16 services. Here is what each one powers and what needs external setup:

### 3.1 Databases (Docker-Provisioned)

| Service | Port | Purpose | Setup Action |
|---------|------|---------|--------------|
| **Neo4j 5 Community** | `7474` (browser), `7687` (Bolt) | Context Premise hypergraph, relationship mapping | Change default password from `changeme`. Install APOC plugin (auto-configured in compose). |
| **Redis 7** | `6379` | Receipt chain caching, quarantine state, Aurore API response caching | No setup required — runs out of the box. |
| **Supabase (PostgreSQL)** | External | Relational data, user configs, content performance matrices | You need a Supabase project. Add `SUPABASE_URL` and `SUPABASE_KEY` to `.env`. Run the 4 mandatory V5 migrations: `cultural_memory_map`, `coach_story_archive`, `humor_mechanism_registry`, `context_performance_registry`. |

### 3.2 AI/LLM Services

| Key in `.env` | Service | Used By |
|---------------|---------|---------|
| `GROQ_API_KEY` | Groq (Whisper) | Sacred Audio transcription (FR2) |
| `OPENROUTER_API_KEY` | OpenRouter | Multi-model routing (ModelRouter extension) |
| `KIMI_API_KEY` | Kimi/Moonshot | Supplementary reasoning |
| `NVIDIA_API_KEY` | NVIDIA NIM | RunningHub AI image generation |
| `HUGGINGFACE_ACCESS_TOKEN` | HuggingFace | Model weights for sentiment/LIWC analysis |

### 3.3 Research & Media APIs

| Key in `.env` | Service | Used By |
|---------------|---------|---------|
| `FIRECRAWL_API_KEY` | Firecrawl | Forum scraping for CRAL research (M1-M7) |
| `SERPAPI_KEY` + `SERPER_API_KEY` | SerpAPI / Serper | Web search for Human Evidence Bias |
| `PEXELS_API_KEY` | Pexels | CVE four-tier image sourcing (Tier 2: Stock) |
| `UNSPLASH_ACCESS_KEY` | Unsplash | CVE image sourcing |
| `PIXABAY_API_KEY` | Pixabay | CVE image sourcing |
| `GIPHY_API_KEY` | Giphy | Animated content sourcing |

### 3.4 Delivery & Integration (Require Manual Setup)

| Service | Status | What You Need |
|---------|--------|---------------|
| **Notion API** | ❌ Not yet in `.env` | Create a Notion integration at [notion.so/my-integrations](https://notion.so/my-integrations). Add `NOTION_API_KEY` and `NOTION_DATABASE_ID` to `.env`. Share target databases with the integration. |
| **Telegram Bot** | ❌ Not yet in `.env` | Create a bot via [@BotFather](https://t.me/BotFather). Add `TELEGRAM_BOT_TOKEN` to `.env`. This powers CBCS (client-facing) and Guardian Agent alerts. |
| **Publer** | ❌ Not yet in `.env` | Create a Publer account and generate API credentials. Add `PUBLER_API_KEY` to `.env`. Used for scheduled posting via n8n triggers (FR42). |
| **RunPod** | ✅ In `.env` | Already configured (`RUNPOD_API_KEY`). Used for GPU-accelerated AI image generation via RunningHub. |

---

## 4. V²WS, Excalidraw & Tierlist — The Video/Webinar Pipeline

These are the systems that turn scripts into **visual presentation assets** — webinar decks, tier list videos, and animated Excalidraw canvases.

### 4.1 V²WS — Webinar Generation System

V²WS has **two modes**, both outputting native `.excalidraw` JSON:

| Mode | Service | How It Works |
|------|---------|-------------|
| **YOLO Mode** (FR33) | `v2ws_yolo_service.py` | Zero-pause: 5 inputs → 5-part script (Hook → Problem → Paradigm Shift → Method → Offer) → Excalidraw with 1920×1080 slides + speaker notes outside viewport. No approval gates. |
| **Interactive Mode** (FR34) | `v2ws_interactive_service.py` | Telegram BMAD-style: real-time audience-sentiment adjustments, operator approval between sections. |

V²WS has **9 dedicated skill areas** under `skills/v2ws/`: intro, content, meme, research, transition, close, visual, voice, and orchestration — each containing JIT-compiled micro-prompts for modular webinar assembly (Jason Fladlien method).

### 4.2 Excalidraw Pipeline (Benjamin)

The Excalidraw pipeline is the **shared rendering layer** that both V²WS and Tierlist use:

| Component | Service | What It Does |
|-----------|---------|-------------|
| **Unified Excalidraw** (FR35) | `unified_excalidraw_service.py` | Cross-format layout engine — handles **horizontal** (webinar slides) and **vertical** (tierlist scrolling) layouts. Enforces brand stroke/fill colors and native editable text. |
| **Transparent Collage** (FR36) | `transparent_collage_pipeline_service.py` | Generates stick figure + photorealistic prop images via T2I → alpha extraction with 1-pixel edge dilation. Falls back to polaroid frame on transparency failure. |
| **Excalidraw Compiler** | `excalidraw_compiler.py` | Low-level JSON assembly for `.excalidraw` format |
| **Composer Skill** | `skills/visual/excalidraw-composer/SKILL.md` | 20KB JIT skill defining the agentic assembly protocol |

### 4.3 Tierlist — Video Idea Generator

The Tierlist system is a **standalone application** that connects to the CCF weekly pipeline:

| Component | Location | What It Does |
|-----------|----------|-------------|
| **Telegram Bot** | `tools/telegram-tierlist-bot/` | Reads `dynamic_content_themes.json` from the weekly pipeline → generates 3 tier list / rating video ideas via OpenRouter → sends to coach on their configured day (default: Thursday 9:00 AM) |
| **React Frontend** | `tools/tierlist-app/` | Vite + React app for visual tierlist rendering (pre-built in `dist/`) |

**To test the Tierlist bot:**
```powershell
# Dry run (no Telegram, just preview)
python tools/telegram-tierlist-bot/bot.py --coach "JP" --dry-run

# Live send
python tools/telegram-tierlist-bot/bot.py --coach "JP"

# Start scheduled delivery (runs daily, sends on configured day)
python tools/telegram-tierlist-bot/scheduler.py
```

> [!NOTE]
> The Tierlist bot requires its own `.env` in `tools/telegram-tierlist-bot/` with `TELEGRAM_BOT_TOKEN` and `OPENROUTER_API_KEY`. Copy from `.env.example` in that directory.

---

## 5. The CVE (Conscious Visual Engine) — Is the Canva Clone Built?

**Short answer: The backend pipeline is fully built. The Canva clone frontend is NOT yet integrated.**

Here is the current CVE status:

| Component | Status | What Exists |
|-----------|--------|-------------|
| Abel (Visual Composition Brief) | ✅ BUILT | `abel_vcb_generator.py` — generates 9-step VCB with PSSL parameters |
| Aurore (Image Research) | ✅ BUILT | `aurore_image_sourcing.py` + `multi_api_image_search.py` — 5 API search across Pexels/Unsplash/Pixabay |
| Paradoxe (Prompt Compiler) | ✅ BUILT | `paradoxe_pssl_compiler.py` — compiles Kelvin temps, gaze vectors, PAD scores |
| Visual Validation (AGSS) | ✅ BUILT | `visual_validation_agent.py` — authenticity scoring and drift detection |
| Canvas Composition & Delivery | ✅ BUILT (Backend) | `canvas_composition_service.py` and `canvas_api.py` — router and service layer for canvas assembly |
| **Conscious Canva App (Frontend)** | ✅ BUILT | The Canva clone (Next.js + Fabric.js) is fully cloned into `canva-app/` and wired to the CCP backend, running on port 3000 |
| Notion Visual Content Card | ✅ BUILT | `notion_visual_content_card.py` — VPO delivery with "Why This Visual" rationale |

---

## 6. The 4 Must-Read Documents from `lab/CCP update/`

Out of 31 files in this folder, these four give you the deepest operational understanding:

| # | Document | Why Read It | Size |
|---|----------|-------------|------|
| 1 | [CCP_Architecture_V5.0.docx.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/CCP%20update/CCP_Architecture_V5.0.docx.md) | **The Bible.** The most complete single document describing V5 architecture, all sub-systems, agent workforce (65 agents across 6 departments), and the JIT Skill Compiler in full detail. | 112 KB |
| 2 | [CCP_CBCS_CPSC_V3.docx.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/CCP%20update/CCP_CBCS_CPSC_V3.docx.md) | **The Relationship Engine.** Explains the 14 CBCS protocols (Social Penetration, DARN-CAT, Transportation Score, etc.) and how CPSC conversion triggers work. Essential for testing the Telegram bot. | 63 KB |
| 3 | [CVE_Documentation_V3.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/CCP%20update/CVE_Documentation_V3.md) | **The Visual Brain.** Complete CVE pipeline: Abel's 9-step decision process, PSSL parameters, four-tier image hierarchy, AGSS validation scoring, and the Canva App assembly spec. | 66 KB |
| 4 | [JIT_Skill_Compiler_Architecture.docx.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/CCP%20update/JIT_Skill_Compiler_Architecture.docx.md) | **How scripts actually get written.** The 7-component CCSB blueprint, Dependency Registry, Adapter Registry, the 4-tier assembly, Surface Gates (SG-01 to SG-08), and Anti-Draft Intelligence. This is what makes or breaks content quality. | 49 KB |

> [!TIP]
> Read them in this exact order: **#4 → #1 → #3 → #2**. Start with how the compiler works (the engine), then how the whole system orchestrates around it, then visuals, then the client relationship layer.

---

## 7. Standard Operating Procedure — First Live Test

### Phase A: Environment Setup (30 minutes)

```powershell
# 1. Clone to test machine (if deploying fresh)
git clone https://github.com/Remjohn/CCP.git
cd CCP

# 2. Copy your .env file with all API keys
# Ensure these are added/updated:
#   SUPABASE_URL, SUPABASE_KEY
#   NOTION_API_KEY, NOTION_DATABASE_ID
#   TELEGRAM_BOT_TOKEN
#   NEO4J_PASSWORD (change from 'changeme')

# 3. Start the Docker stack
docker-compose -f docker/docker-compose.yml up -d

# 4. Verify all 3 containers are running
docker ps
# Expected: ccp (8000), redis (6379), neo4j (7474+7687)

# 5. Access Neo4j Browser → http://localhost:7474
# Login with neo4j / [your NEO4J_PASSWORD]
# Verify APOC is loaded: RETURN apoc.version()

# 6. Install Python dependencies (for local dev/testing)
pip install -r requirements.txt

# 7. Run the full regression test suite
python -m pytest tests/ -v
# Expected: 1,913 tests passing, 0 failures
```

### Phase B: Coach Genesis — Your First Coach (1-2 hours)

This is the **most critical step**. The entire system is anchored on the Voice DNA extracted during Genesis.

1. **Prepare sacred audio:** Collect 45-90 minutes of the coach's raw, unscripted speaking (podcasts, live workshops, coaching calls). The more emotionally varied, the better.
2. **Trigger Genesis Pipeline:** Run the FR1 orchestration command sequence (8 commands: Genesis Init → Sacred Audio Ingestion → Voice DNA Extraction → Emotional DNA → Trigger Map → Tribe Profile → Leadership Scorecard → Genesis Certificate).
3. **Verify `coach_soul.json`:** After Genesis, check the coach's directory under `coaches/[COACH_ID]/`. The file must contain:
   - **Positive Space:** Rhythm patterns, register vocabulary, semantic hooks
   - **Negative Space:** ≥15 exact forbidden strings across 4 categories (Gate PC-03 enforces this)
   - **Emotional DNA:** 10-variable profile from LIWC-22 analysis
4. **Genesis Certificate:** Must show `AUTHENTICATED` status. If `PROVISIONAL`, manually review and approve. If `FAILED`, Genesis halts — review the specific failing stage.

### Phase C: First Weekly Batch — Content Production (2-3 hours)

1. **Configure the batch:** Set target archetypes, mood states, and cohort maturity levels in the pipeline config.
2. **Run the weekly pipeline:** This triggers the full CRAL → CCSB → CCF → CVE chain.
3. **Monitor the Receipt Chain:** Every pipeline stage emits a signed JSON receipt. A missing receipt triggers `Batch Quarantine` — check the operator dashboard for the specific stage that failed.
4. **Review output in Notion:** If Notion API is configured, scripts and visual assets auto-sync. Otherwise, check the local output directory.

### Phase D: Telegram Bot — CBCS Activation

1. **Start the Telegram bot** with the configured `TELEGRAM_BOT_TOKEN`.
2. **Send a test voice note** as a simulated client.
3. **Verify the Circuit Breaker** responds in <500ms to crisis keywords.
4. **Check the Social Penetration Depth Gauge** initializes at `Orientation` stage for new clients.

---

## 8. Critical Safety Systems to Know

Before you test anything, understand these three non-negotiable guardrails:

| System | What It Does | What Triggers It |
|--------|-------------|-----------------|
| **Circuit Breaker** | Halts all AI execution in <500ms and escalates to human operator | Crisis keywords detected in Telegram voice notes |
| **Receipt Chain Guard** | Quarantines entire batch if any data mutation lacks a cryptographic receipt | Missing `receipt_chain_hash` on any pipeline stage output |
| **L3 Minimum Depth Threshold** | Blocks content generation if the coach's Negative Space has <15 exact forbidden strings | Gate PC-03 fires `L3_INSUFFICIENT_DEPTH` halt |

> [!CAUTION]
> **Never bypass these gates.** They exist because LLMs regress to statistical centroids when missing constraints. A "working" pipeline that produces generic content is worse than a halted pipeline — it silently destroys the coach's brand identity.

---

## 9. What's Next — The Remaining Integration Work

| Priority | Task | Effort |
|----------|------|--------|
| 🔴 HIGH | Add `SUPABASE_URL`, `SUPABASE_KEY`, `NOTION_API_KEY`, `TELEGRAM_BOT_TOKEN` to `.env` | 15 min |
| 🔴 HIGH | Run V5 Supabase migrations (4 tables) | 30 min |
| 🟡 MEDIUM | Configure Publer API for automated social posting | 1 hour |
| 🟢 LOW | Set up n8n for Publer webhook triggers (FR42) | 2-3 hours |
| 🟢 LOW | Deploy to cloud (single-tenant instance per ADR-01) | Variable |

---

*This document is your operator's manual. The architecture documents are the engineering blueprints. Start with Genesis, verify with tests, and expand from there. The system is designed to halt loudly rather than fail silently — trust the gates.*
