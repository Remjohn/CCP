# CCF v3.0 — Full Pipeline Vision & Gap Analysis

> **Version:** v3.0 Vision Document
> **Date:** 2026-02-24
> **Purpose:** Define the complete ideal CCF weekly content cycle, map every step to existing commands/skills, identify what still needs to be built, and recommend infrastructure for multi-agent collaboration.

---

## Executive Summary

The CCF v3.0 pipeline is a **weekly recurring engine** that transforms 15 minutes of a coach's voice notes into a full week of publication-ready scripts. Unlike the previous documentation which treated the system as a static batch processor, this document describes the living, learning, self-improving cycle that runs every week for every coach.

The pipeline has 8 phases, operates with a **Manager-in-the-Loop** validation architecture, maintains a persistent **Content Bank** database, and culminates in a **Sunday Bot Meeting** where each coach's AI agent critiques its own performance and learns from the manager's feedback.

---

## Phase 1: Intelligence Radar (Monday)

**Goal:** Scan the internet for viral content opportunities aligned with this coach's pillars.

An agent sweeps Google Trends, social signals, and competitor content across the coach's 4 active content pillars (selected by rotation algorithm). It identifies friction points — topics where audience pain is high but existing content quality is low.

| Component | Status | File |
|-----------|--------|------|
| Radar Skill | ✅ EXISTS | `skills/ccf/content/intelligence-radar/SKILL.md` |
| Radar Command | ✅ EXISTS | [commands/ccf-radar.md](file:///d:/Work/The%20Conscious%20Movie%20Factory%20December/ccf-26/commands/ccf-radar.md) |
| Firecrawl Wrapper | ✅ EXISTS | [tools/firecrawl_wrapper.py](file:///d:/Work/The%20Conscious%20Movie%20Factory%20December/tools/firecrawl_wrapper.py) |

**Output:** `intelligence/weekly/{week_id}/intelligence_radar.json`

---

## Phase 2: Coach Provocation (Monday-Tuesday)

**Goal:** Transform radar insights into provocative questions that elicit the coach's authentic, unrehearsed reactions.

The Question Engineer takes the friction points from Phase 1 and generates 5-7 provocation questions designed to trigger the coach's unfiltered opinion. These are not interview questions — they are emotional catalysts engineered to extract vulnerability, confrontation, and recognition from the coach. After generation, the questions are delivered to the coach via Telegram (or WhatsApp), and the system pauses until voice notes arrive.

| Component | Status | File |
|-----------|--------|------|
| Question Engineer Skill | ✅ EXISTS | [skills/ccf/content/question-engineer/SKILL.md](file:///d:/Work/The%20Conscious%20Movie%20Factory%20December/ccf-26/skills/ccf/content/question-engineer/SKILL.md) |
| Question Command | ✅ EXISTS | [commands/ccf-question.md](file:///d:/Work/The%20Conscious%20Movie%20Factory%20December/ccf-26/commands/ccf-question.md) |
| Question Distiller | ✅ EXISTS | [skills/ccf/distillation/question-distiller/SKILL.md](file:///d:/Work/The%20Conscious%20Movie%20Factory%20December/ccf-26/skills/ccf/distillation/question-distiller/SKILL.md) |
| Telegram Delivery Bot | ⚠️ PARTIAL | `tools/telegram-tierlist-bot/` exists but needs coach-facing question delivery mode |

**Output:** `intelligence/weekly/{week_id}/provocation_questions.json`
**⏸️ PAUSE:** System waits for coach voice notes (5-15 min total recording time).

---

## Phase 3: Voice Elicitation + Memory Update (Tuesday-Wednesday)

**Goal:** Transcribe the coach's voice notes, extract key phrases and emotional peaks, and update the persistent Memory Engine with new voice DNA.

When the coach drops audio files into the project folder, the Elicitation Engine transcribes them, tags responses by source question, and extracts the raw Stream of Consciousness material. Immediately after, the Memory Engine scans the new material to accumulate signature phrases, story bank entries, metaphor libraries, and session intelligence — ensuring the system gets smarter with every interaction.

| Component | Status | File |
|-----------|--------|------|
| Elicitation Skill | ✅ EXISTS | [skills/ccf/content/coach-elicitation/SKILL.md](file:///d:/Work/The%20Conscious%20Movie%20Factory%20December/ccf-26/skills/ccf/content/coach-elicitation/SKILL.md) |
| Elicitation Command | ✅ EXISTS | [commands/ccf-elicit.md](file:///d:/Work/The%20Conscious%20Movie%20Factory%20December/ccf-26/commands/ccf-elicit.md) |
| Memory Engine Skill | ✅ EXISTS | `skills/ccf/content/memory-engine/SKILL.md` |
| Memory Command | ✅ EXISTS | [commands/ccf-memory.md](file:///d:/Work/The%20Conscious%20Movie%20Factory%20December/ccf-26/commands/ccf-memory.md) |

**Output:** `intelligence/weekly/{week_id}/coach_soc_batch.md` + Updated `coach_memory.json`

---

## Phase 4: Theme Generation + Blueprint Selection (Wednesday)

**Goal:** Generate content themes from the coach's responses, then produce 48 content blueprints and auto-select the best 8.

The Dynamic Theme Generator takes each voice note response and generates a distinct content theme (typically 4 themes per week). For each theme, 12 content blueprints are generated across different archetype formats — producing **4 themes × 12 blueprints = 48 total blueprints**. An automatic ranking system then selects the **top 8 blueprints** based on viral potential, soul alignment, and tribal resonance scores.

| Component | Status | File |
|-----------|--------|------|
| Theme Generator Skill | ✅ EXISTS | `skills/ccf/content/dynamic-theme-generator/SKILL.md` |
| Blueprint Orchestrator | ✅ EXISTS | [skills/ccf/research/blueprint-orchestrator/SKILL.md](file:///d:/Work/The%20Conscious%20Movie%20Factory%20December/ccf-26/skills/ccf/research/blueprint-orchestrator/SKILL.md) |
| Blueprint Command | ✅ EXISTS | [commands/ccf-blueprint.md](file:///d:/Work/The%20Conscious%20Movie%20Factory%20December/ccf-26/commands/ccf-blueprint.md) |
| Blueprint Distiller | ✅ EXISTS | [skills/ccf/distillation/blueprint-distiller/SKILL.md](file:///d:/Work/The%20Conscious%20Movie%20Factory%20December/ccf-26/skills/ccf/distillation/blueprint-distiller/SKILL.md) |
| **Auto-Select Top 8** | 🔴 MISSING | Needs: `skills/ccf/orchestration/blueprint-ranker/SKILL.md` |

> [!WARNING]
> **GAP: Blueprint Ranker.** Currently, all 12 blueprints per theme flow into production. We need a new `blueprint-ranker` skill that scores all 48 blueprints and selects the top 8 based on a weighted scoring formula (viral potential × soul alignment × tribal resonance × research depth availability). This prevents wasting API calls on low-potential blueprints.

**Output:** `content_blueprints.json` (48 total, 8 selected for production)

---

## Phase 5: Research Layer (Wednesday-Thursday)

**Goal:** For each of the 8 selected blueprints, execute deep and fresh research to provide evidence-backed ammunition for script writing.

This phase runs 4 parallel research tracks per blueprint: RAW Deep Research (4000 words, investigative), RAW Fresh Research (4000 words, temporal), then the analyst distillers compress each into focused 1000-1200 word briefs. The Firecrawl wrapper is authorized for terminal-level URL scraping during the RAW phases.

| Component | Status | File |
|-----------|--------|------|
| Raw Deep Research Skill | ✅ EXISTS | [skills/ccf/research/raw-deep-research/SKILL.md](file:///d:/Work/The%20Conscious%20Movie%20Factory%20December/ccf-26/skills/ccf/research/raw-deep-research/SKILL.md) |
| Raw Fresh Research Skill | ✅ EXISTS | [skills/ccf/research/raw-fresh-research/SKILL.md](file:///d:/Work/The%20Conscious%20Movie%20Factory%20December/ccf-26/skills/ccf/research/raw-fresh-research/SKILL.md) |
| Research Command | ✅ EXISTS | [commands/ccf-raw-research.md](file:///d:/Work/The%20Conscious%20Movie%20Factory%20December/ccf-26/commands/ccf-raw-research.md) |
| Deep Analyst Command | ✅ EXISTS | [commands/ccf-research-deep.md](file:///d:/Work/The%20Conscious%20Movie%20Factory%20December/ccf-26/commands/ccf-research-deep.md) |
| Fresh Analyst Command | ✅ EXISTS | [commands/ccf-research-fresh.md](file:///d:/Work/The%20Conscious%20Movie%20Factory%20December/ccf-26/commands/ccf-research-fresh.md) |
| Research Distiller | ✅ EXISTS | [skills/ccf/distillation/research-distiller/SKILL.md](file:///d:/Work/The%20Conscious%20Movie%20Factory%20December/ccf-26/skills/ccf/distillation/research-distiller/SKILL.md) |
| Smart Query Generator | ✅ EXISTS | [skills/ccf/research/smart-query-generator/SKILL.md](file:///d:/Work/The%20Conscious%20Movie%20Factory%20December/ccf-26/skills/ccf/research/smart-query-generator/SKILL.md) |

**Per Blueprint:** 4 requests (RAW deep + RAW fresh + analyst deep + analyst fresh)
**For 8 Blueprints:** 32 requests total

**Output:** `{blueprint_id}_deep_brief.md` + `{blueprint_id}_fresh_brief.md` per blueprint

---

## The Archetype Prompt Library — 92 Templates (`Script Prompts/`)

> [!IMPORTANT]
> Scripts are **never** generated from thin air. Every script is structured by a specific archetype prompt template loaded from `ccf 26/Script Prompts/`. When the Blueprint Orchestrator assigns an archetype to a blueprint, it references this library. When Stage 3 (Script Generator) executes, it loads the corresponding prompt as its structural skeleton.

### Storytelling Archetypes (30 templates)
Each story type has both a **Generative** variant (for AI-only production) and an **Interview Framework** variant (for coach-recorded content):

| Emotion | Generative | Interview |
|---------|-----------|-----------|
| Achievement | ✅ | ✅ |
| Anticipation | ✅ | ✅ |
| Connection | ✅ | ✅ |
| Curiosity | ✅ | ✅ |
| Cuteness | ✅ | ✅ |
| Discovery | ✅ | ✅ |
| Empowerment | ✅ | ✅ |
| Inspiration | ✅ | ✅ |
| Joy | ✅ | ✅ |
| Longing | ✅ | ✅ |
| Nostalgia | ✅ | ✅ |
| Recognition | ✅ | ✅ |
| Relief | ✅ | ✅ |
| Romance | ✅ | ✅ |
| Surprise | ✅ | ✅ |
| Transformation | ✅ | ✅ (new) |

### Tier Lists (4 templates)
Authority, Relatable, Controversial, Red Flag — each 25-35KB, the most detailed prompt templates in the library.

### Reaction Scripts (3 templates)
Nostalgia Reaction, Outrage Reaction, Validation Reaction.

### Carousels (2 templates)
Dopamine Cliff Carousel, Relief Peak Carousel.

### Listicles (7 templates)
Curiosity-Intriguing, Fear-Anxiety, Funny Relatable, Hope & Inspiration, Nostalgia, Outrageous, Shocking.

### Case Studies (6 templates)
FOMO, Inspirational, Intriguing, Relatable, Social Proof-Testimonial, Surprising.

### Comparisons (5 templates)
Funny Relatable, Nostalgia, Outrageous, Shocking, Surprising.

### Polls (4 templates)
Archetypical Poll, Stereotypical Poll, Controversial Dilemma Poll, Would You Rather.

### Myths/Debunking (5 templates)
Curiosity/Intrigue, Disgusting, Empowering, Indignation, Schadenfreude.

### Captions (3 templates)
Descriptive/Explanatory, Instructional/Advisory, Reflective/Insightful.

### Visual Prompts (3 templates)
Hero Journey, Hero's Journey (variant), Visual Timeline, Worst Case Scenario Visual.

### Tweets & Memes (7 templates)
Persuasive Tweets, Data-Visualizer Tweet, Thought Whisperer Tweet, plus 4 humor theory memes (Benign Violation, Incongruity, Relief Theory, Superiority Theory).

### Utility Prompts (5 templates)
Advanced Content Hook Generation, Coach's Stream of Consciousness Template, Observational Humor & Wisdom Extraction, Spare Persuasion Priming Activation, Standard Voice Writing Guide.

### Standalone Scripts (2 templates)
The Top Reliable List (Generative Script), The Conceptual Contrast Script, The Worst Case Scenario Script.

### How It Connects to the Pipeline
1. **Phase 4 (Blueprint):** The Blueprint Orchestrator assigns each of the 48 blueprints an archetype from this library (e.g., `The Curiosity Story (Generative)` or `The Dopamine Cliff Carousel`).
2. **Phase 6, Stage 2 (Mirror Session):** Q13 confirms or modifies the assigned archetype.
3. **Phase 6, Stage 3 (Script Generator):** The corresponding prompt file is loaded as the structural template. The generator applies the wisdom briefs and SoC material *within* the archetype's skeleton — it does not invent structure.

---

## Phase 6: Script Production — The 4-Stage Engine (Thursday-Friday)

**Goal:** For each of the 8 selected blueprints, run the full 4-stage temperature-descending production pipeline.

Each blueprint flows through 4 stages sequentially. No blueprint can advance to the next stage until the current stage's distillation gate passes.

### Stage 1: Stream of Consciousness (Temperature 0.9)
Voice priming — generates authentic, messy SoC material that sounds like the coach's internal monologue. Governed by the Voice Distiller (4 Laws of Voice Distillation).

### Stage 2: Mirror Session (Temperature 0.7)
14-question strategic adaptation that upgrades the base prompt using SoC output, soul values, and research. Governed by 4 Laws of Mirror Adaptation (H14).

### Stage 2.5: Wisdom Forge (Temperature 0.5)
Generates 4 wisdom briefs (Authenticity, Authority, Memetic, Shadow) that provide dimensional tension for the script generator. Governed by 4 Laws of Wisdom Filtration (H15).

### Stage 3: Script Generation (Temperature 0.3)
Precision execution — applies the archetype structure to the wisdom briefs. No new reasoning allowed. Governed by 4 Laws of Script Distillation.

| Component | Status | File |
|-----------|--------|------|
| SoC Generator | ✅ EXISTS | `skills/ccf/production/soc-generator/SKILL.md` |
| Mirror Session | ✅ EXISTS | `skills/ccf/production/mirror-session/SKILL.md` |
| Wisdom Forge | ✅ EXISTS | `skills/ccf/production/wisdom-forge/SKILL.md` |
| Script Generator | ✅ EXISTS | `skills/ccf/production/script-generator/SKILL.md` |
| Voice Distiller | ✅ EXISTS | `skills/ccf/distillation/voice-distiller/SKILL.md` |
| All 4 Commands | ✅ EXISTS | `ccf-soc`, `ccf-adapt`, `ccf-wisdom`, `ccf-generate` |

**Per Blueprint:** 5 requests (SoC + voice-distiller gate + mirror + wisdom + generate)
**For 8 Blueprints:** 40 requests total

**Output:** `{blueprint_id}_generated_script.md` per blueprint

---

## Phase 7: Manager Review + Content Bank (Friday-Saturday)

**Goal:** Notify the Manager via Telegram, receive validation decisions, and route scripts to the Content Bank or Archive with feedback learning.

### 7a. Telegram Notification to Manager
When all 8 scripts are generated, the system sends a **Telegram message to the Manager** (NOT the coach) containing a summary of each script with its theme, archetype, hook, key stats, and a link/preview. The Manager reviews and marks each script as: **APPROVE**, **REVISE**, or **REJECT**.

### 7b. Conditional Branching
- **APPROVED scripts →** Run the Script Analyst + Script Commander validation chain, then deposit into the **Content Bank** database.
- **REVISE scripts →** Re-enter Stage 3 (Script Generator) with the Manager's revision notes injected as constraints. Re-generate, then re-validate.
- **REJECTED scripts →** Archive with the Manager's feedback. The feedback is registered and the Commander's validation rules are updated, ensuring future scripts learn from this rejection.

### 7c. Content Bank & Publishing Schedule
The Content Bank is a persistent database of all validated, publication-ready scripts. Each week, the **top 8 scripts** from the Content Bank (ranked by quality score, freshness, and theme diversity) are packaged as recording guides and sent to the coach as that week's recording batch.

| Component | Status | Notes |
|-----------|--------|-------|
| Script Analyst | ✅ EXISTS | `skills/ccf/validation/script-analyst/SKILL.md` |
| Script Commander | ✅ EXISTS | `skills/ccf/validation/script-commander/SKILL.md` |
| Phoenix Loop | ✅ EXISTS | `skills/ccf/validation/phoenix-loop/SKILL.md` |
| Boss Will | ✅ EXISTS | `skills/ccf/validation/boss-will/SKILL.md` |
| **Telegram Manager Bot** | 🔴 MISSING | Needs: `tools/telegram-manager-bot/` — sends script previews, receives APPROVE/REVISE/REJECT |
| **Content Bank Database** | 🔴 MISSING | Needs: `tools/content-bank/` — persistent JSON/SQLite store of validated scripts with quality scores |
| **Archive + Feedback Logger** | 🔴 MISSING | Needs: `skills/ccf/validation/feedback-learner/SKILL.md` — registers rejection patterns and updates Commander rules |
| **Content Scheduler** | 🔴 MISSING | Needs: `skills/ccf/orchestration/content-scheduler/SKILL.md` — selects top 8 from Content Bank per week |
| **Recording Guide Generator** | ✅ EXISTS | `skills/ccf/content/recording-director/SKILL.md` |

> [!IMPORTANT]
> **GAP: Manager Bot + Content Bank + Feedback Learner + Content Scheduler.** These 4 components form the adaptive learning backbone of the system. Without them, the pipeline is a one-shot generator. With them, it becomes a self-improving engine that gets better every week based on your operational feedback.

---

## Phase 8: Sunday Bot Meeting (Weekly Retrospective)

**Goal:** Every Sunday, each coach's AI agent holds a structured performance review meeting. The bots critique their own week's output, analyze which published content performed well or poorly, learn from the data, and produce a weekly validation report for the Commander.

### Meeting Structure
1. **Performance Data Ingestion:** Each bot loads that week's published content metrics (views, engagement, saves, shares) from the coach's social analytics.
2. **Self-Critique Round:** Each bot identifies its top 3 performing scripts and bottom 3, analyzing WHY each succeeded or failed based on the 16-law framework.
3. **Pattern Recognition:** Bots identify recurring patterns — which archetypes perform best for this coach, which themes resonate, which hooks drive the most engagement.
4. **Commander Update:** The weekly insights are compiled into a validation report that the Commander accesses before validating future scripts.
5. **Manager Review:** Before the bots finalize their reports, the Manager provides an overall take on the meeting — adding human context the bots cannot observe (audience sentiment, brand direction shifts, upcoming launches).

| Component | Status | Notes |
|-----------|--------|-------|
| **Meeting Orchestrator** | 🔴 MISSING | Needs: `skills/ccf/orchestration/sunday-meeting/SKILL.md` |
| **Performance Ingester** | 🔴 MISSING | Needs: `skills/ccf/content/performance-tracker/SKILL.md` — pulls social analytics |
| **Weekly Validation Report** | 🔴 MISSING | Needs: `skills/ccf/validation/weekly-report/SKILL.md` |
| Memory Engine | ✅ EXISTS | Can be extended to store performance patterns |
| Report Skill | ✅ EXISTS | `skills/ccf/orchestration/ccf-report/SKILL.md` |

---

## Telegram vs Discord: Where Should the Bots Meet?

Both platforms offer free Bot APIs. Here is the honest comparison for this specific use case:

| Criterion | Telegram | Discord |
|-----------|----------|---------|
| **Bot API Cost** | Free | Free |
| **Group Size** | Up to 200,000 members | Up to 500,000 in a server |
| **Threading** | Limited (reply chains only) | Full thread support per channel |
| **Role-Based Channels** | ❌ No native channels | ✅ Unlimited channels per role/coach |
| **Bot-to-Bot Communication** | Hacky (bots can't easily see other bots) | Native (bots can read any channel they have access to) |
| **Rich Embeds** | Basic markdown only | Full embeds with fields, colors, and thumbnails |
| **Webhook Support** | Basic | Extremely robust |
| **File Sharing** | ✅ Good | ✅ Good |
| **Manager Already Uses** | ✅ Yes (Telegram in active use) | ❓ Unknown |
| **Multi-Agent Meeting Viability** | ⚠️ Possible but clunky | ✅ Purpose-built for this |

### Recommendation: **Discord for Bot Meetings, Telegram for Manager Notifications**

Use a **hybrid approach**:
- **Telegram** remains the manager-facing notification channel (script previews, approval requests, weekly summaries). You already use it, it's fast, and it's on your phone.
- **Discord** becomes the backend "war room" where the coach bots hold their Sunday meetings. Discord's channel architecture is ideal for this: one channel per coach (`#coach-adele`, `#coach-matthis`), one `#weekly-meeting` channel where all bots post their retrospectives, and a `#commander-updates` channel where validation rule changes are logged. Discord threads allow structured, multi-turn bot conversations without message collision.

A free Discord server with a single bot application (hosting via Oracle Cloud free tier or Railway free tier) can handle all of this at zero cost.

---

## Complete Request Count Estimate (Per Week, Per Coach)

| Phase | Requests |
|-------|----------|
| 1. Intelligence Radar | 1 |
| 2. Question Generation | 1 |
| 3. Elicitation + Memory | 2 |
| 4. Theme Generation + 48 Blueprints + Ranking | 3 |
| 5. Research (8 blueprints × 4 research passes) | 32 |
| 6. Production (8 blueprints × 5 stages) | 40 |
| 7. Validation (8 blueprints × 2 validation passes) | 16 |
| 8. Sunday Meeting + Report | 2 |
| **TOTAL PER WEEK PER COACH** | **~97 requests** |

---

## Full Gap Summary — What Needs to Be Built

| Priority | Component | Type | Purpose |
|----------|-----------|------|---------|
| 🔴 P0 | `telegram-manager-bot` | Tool | Send script previews to Manager, receive APPROVE/REVISE/REJECT |
| 🔴 P0 | `content-bank` | Tool/DB | Persistent store of validated scripts with quality scores and scheduling |
| 🔴 P0 | `feedback-learner` | Skill | Register rejection patterns, update Commander validation rules adaptively |
| 🔴 P0 | `content-scheduler` | Skill | Select top 8 from Content Bank each week for coach recording |
| 🟡 P1 | `blueprint-ranker` | Skill | Score 48 blueprints, auto-select top 8 for production |
| 🟡 P1 | `sunday-meeting` | Skill | Orchestrate weekly bot retrospective meeting |
| 🟡 P1 | `performance-tracker` | Skill | Ingest social analytics for published content |
| 🟡 P1 | `weekly-report` | Skill | Generate weekly validation report for Commander |
| 🟢 P2 | Discord bot infrastructure | Tool | Free server setup for multi-agent meeting channels |
| 🟢 P2 | Telegram question delivery mode | Tool | Extend existing tierlist bot to deliver provocation questions to coach |
