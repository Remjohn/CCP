# CCP Sprint Backlog

**Derived from:** [CCP_User_Stories.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/prd/CCP_User_Stories.md) (39 stories)  
**Architecture:** [CCP_Technical_Architecture.md](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/CCP_Technical_Architecture.md)  
**Sprint Duration:** 2 weeks each  
**Critical Path:** Sprint 1 → 2 → 3 → 4 (Genesis → CCF Pipeline → CBCS → Notion Delivery)

**Task Format:** Each task includes the target file/component, what exactly gets built, and which story it satisfies. Tasks marked 🔒 are blockers for downstream tasks.

---

## Sprint 1: Foundation & Coach Genesis

*Goal: A coach can be onboarded and exist in the system with a complete identity profile. All shared infrastructure is in place.*

**Stories covered:** 1.1, 1.2, 1.3, 1.4, 6.5 (partial)

### Infrastructure

| # | Task | Target | Story | Blocker |
|---|---|---|---|---|
| 1.01 | **Scaffold coach repo file structure** — Create the canonical directory layout: `skills/`, `commands/`, `intelligence/`, `production/`, `config/`, `logs/`. Write a `scaffold_coach.py` script that generates this from a template. | `scripts/scaffold_coach.py` | 6.5 | 🔒 |
| 1.02 | **Create `coach_registry.json` schema** — Define the JSON schema: coach acronym (3-char), coach ID (`CCC-0000`), `next_client_id` counter, NOTION_TOKEN reference, Supabase bucket path, creation date. Write a Pydantic model for validation. | `config/coach_registry.json` + `models/coach_registry.py` | 1.3 | 🔒 |
| 1.03 | **Create `coach_soul.json` schema** — Define the full profile schema: `voice_dna` (TTT baseline), `coaching_philosophy`, `tribe_archetype`, `ideal_client`, `leadership_scores` (12 dimensions), `content_tone`, `humor_style`, metadata (version, timestamps). Write a Pydantic model. | `models/coach_soul.py` | 1.4 | 🔒 |
| 1.04 | **Set up Supabase schema** — Create tables: `receipt_chain` (immutable audit log), `asset_registry` (Universal Asset IDs), `person_registry` (Person IDs). Create Storage buckets: `sacred-audio/`, `voice-notes/`, `coach-photos/`, `visual-assets/`. | `scripts/setup_supabase.py` | 6.5 | 🔒 |
| 1.05 | **Set up Docker template** — Create a `Dockerfile` and `docker-compose.yml` for a single-coach instance: Python 3.11+, FastAPI, Redis, Neo4j, `.env` template with all required credentials. | `docker/Dockerfile`, `docker-compose.yml` | 6.5 | 🔒 |
| 1.06 | **Implement Receipt Chain logger** — A Python module that writes immutable entries to the `receipt_chain` Supabase table. Fields: timestamp, agent_id, action, input_hash, output_hash, asset_id, decision_rationale. Every subsequent module imports this. | `core/receipt_chain.py` | 6.1 | 🔒 |
| 1.07 | **Implement Universal Asset ID generator** — A Python module that generates `AAAA-CCC-MM-YY-XXXX` IDs. Includes the 34-code type registry, collision check against Supabase `asset_registry`, and batch generation support. | `core/asset_id.py` | 7.2 | 🔒 |

### Sacred Audio & Voice DNA

| # | Task | Target | Story | Blocker |
|---|---|---|---|---|
| 1.08 | **Build Sacred Audio ingestion endpoint** — FastAPI route that receives Telegram voice messages/file uploads, validates format (OGG/MP3/M4A), stores in Supabase Storage with `SAUD` Asset ID, and returns confirmation. | `api/sacred_audio.py` | 1.1 | |
| 1.09 | **Integrate Groq transcription** — A wrapper function that takes a Supabase audio URL, sends it to Groq for transcription, returns the transcript text. Handles rate limits and retries. | `services/groq_transcriber.py` | 1.2 | |
| 1.10 | **Build TTT baseline extractor** — Takes Sacred Audio transcripts + any coach public content from research. Extracts: sentence rhythm patterns, metaphor frequency, vocabulary fingerprint, emotional peak markers, pause cadence. Outputs the `voice_dna` section of `coach_soul.json`. | `services/ttt_extractor.py` | 1.2 | |

### Onboarding Pipeline

| # | Task | Target | Story | Blocker |
|---|---|---|---|---|
| 1.11 | **Build 5-Layer Research Cascade for coach** — Before the onboarding meeting, research the coach's public presence: social media, website, podcast appearances. Output a structured research brief that pre-fills the interview guide. | `services/coach_research.py` | 1.3 | |
| 1.12 | **Build Kimya elicitation processor** — Takes the operator's interview transcript (text or audio), extracts coaching philosophy, core message, ideal client profile, signature frameworks, competitive positioning. Populates `coach_soul.json` identity fields. | `agents/kimya/elicitation_processor.py` | 1.3, 1.4 | |
| 1.13 | **Build Leadership Trait Scorer** — Analyzes Sacred Audio signals + onboarding interview to score 12 leadership dimensions (Deep Empathy, Authentic Vulnerability, Embodied Confidence, etc.). Outputs `leadership_scores` in `coach_soul.json`. | `agents/minister_identity/trait_scorer.py` | 1.4 | |
| 1.14 | **Wire Genesis Pipeline command** — The `ccf-init` command that orchestrates: Sacred Audio upload → Groq transcription → TTT extraction → Coach research → Kimya elicitation → Leadership scoring → `coach_soul.json` finalization → Receipt Chain logging. | `commands/ccf_init.py` | 1.1–1.4 | |

**Sprint 1 Deliverable:** Run `ccf-init` for a test coach → get a complete `coach_soul.json` with voice DNA, leadership scores, coaching philosophy, and a registered coach ID.

---

## Sprint 2: CCF Content Production Pipeline

*Goal: The weekly content pipeline produces 36 validated scripts in the coach's voice.*

**Stories covered:** 3.1, 3.4, 3.5, 3.6, 3.7, 3.8

### Research & Ideation

| # | Task | Target | Story | Blocker |
|---|---|---|---|---|
| 2.01 | **Build Stream of Consciousness capture** — Takes coach's topic suggestions (from Telegram or operator input) and processes them into structured topic seeds. Stores with `SUGG` Asset ID. | `services/soc_capture.py` | 3.2 | |
| 2.02 | **Build `ccf-analyze` command** — Runs research pipeline (DEEP/FRESH), generates `ideas.json` with 36 content ideas across 14 formats. Applies leadership trait scoring to format assignment (weak traits → exercise, strong traits → showcase). | `commands/ccf_analyze.py` | 3.1, 3.4 | 🔒 |
| 2.03 | **Implement Boredom Ban checker** — Queries the 8-week rolling window of published themes/angles/metaphors. Flags any proposed idea that overlaps. Returns constraint instructions for the generator ("avoid X, Y, Z"). | `core/boredom_ban.py` | 3.7 | 🔒 |

### Content Generation

| # | Task | Target | Story | Blocker |
|---|---|---|---|---|
| 2.04 | **Build script generator core** — Takes an idea from `ideas.json` + `coach_soul.json` + research context. Produces a draft script using the visual recipe archetype rules. Applies TTT calibration. | `agents/script_generator/generate.py` | 3.4, 3.5 | |
| 2.05 | **Implement Contrastive Anti-Draft pipeline** — For each script: (1) Flash model generates the anti-draft with full context, (2) System extracts 5 failure points, (3) Pro model generates the real draft with anti-draft + failure analysis as negative anchor. | `services/contrastive_draft.py` | 3.5 | |
| 2.06 | **Build Humor Agent** — Generates humor pieces (tweets, memes, humor-angle scripts). Accesses vibe comments, humor style DB. Produces ironic/absurd/awkwardly relatable angles. Passes Vibe Check (reject generic AI humor). | `agents/humor_agent/generate.py` | 3.6 | |
| 2.07 | **Build Tweet Meteorologist Agent** — Forecasts digital conversation weather: sentiment climate, viral trends, meme explosions, narrative shifts. Outputs timely angle recommendations for the Humor Agent. | `agents/tweet_meteorologist/forecast.py` | 3.6 | |

### Validation & Governance

| # | Task | Target | Story | Blocker |
|---|---|---|---|---|
| 2.08 | **Build Minister of Identity (inline)** — Runs during generation. Checks every script against `coach_soul.json` voice DNA. Flags drift > 15%. Provides specific correction instructions. | `agents/minister_identity/validate_inline.py` | 3.5 | |
| 2.09 | **Build Minister of Relevance (inline)** — Runs during generation. Checks content against tribe archetype signals and audience resonance data. Flags off-target content. | `agents/minister_relevance/validate_inline.py` | 3.1 | |
| 2.10 | **Build Minister of Timing (inline)** — Runs during generation. Checks content against the 4-layer seasonal influence stack (Macro/Meso/Micro/Pinnacle). Flags off-season content. | `agents/minister_timing/validate_inline.py` | 3.1 | |
| 2.11 | **Build Validation Team gate** — Sequential: Sophia (Content Strategist) → Marcus (Protocol Validator) → Chen (Soul Validator). Each pass/fail with reasons. Failed pieces enter TillDone rewrite loop (max 3 retries). | `services/validation_team.py` | 3.1 | 🔒 |
| 2.12 | **Build Operator review queue** — After validation, content enters a review queue. Operator can approve, reject (with reason), or edit. Edits are logged in Receipt Chain (original + edited versions). | `services/operator_review.py` | 3.8 | |
| 2.13 | **Wire `ccf-weekly` command** — Orchestrates the full 19-command pipeline: SOC → analyze → research → generate (×36, parallelized) → anti-draft → ministers → validate → review queue. Receipt Chain logs every step. | `commands/ccf_weekly.py` | 3.1 | |

### Content Cadence

| # | Task | Target | Story | Blocker |
|---|---|---|---|---|
| 2.14 | **Implement ContentCadence Extension** — Tracks monthly production count per coach. Auto-pauses `ccf-weekly` when limit reached. Warns before starting if quota insufficient for full batch. | `extensions/content_cadence.py` | 3.3 | |

**Sprint 2 Deliverable:** Run `ccf-weekly` for a test coach → 36 validated scripts across 14 formats, all passing TTT < 15% drift, Boredom Ban, and Validation Team gate.

---

## Sprint 3: CBCS Real-Time Coaching Engine

*Goal: Clients interact with the coaching bot via Telegram and receive personalized, coach-voiced responses.*

**Stories covered:** 2.1, 2.2, 2.3, 2.4, 2.5, 5.1

### Core Bot Infrastructure

| # | Task | Target | Story | Blocker |
|---|---|---|---|---|
| 3.01 | **Build Telegram webhook handler** — FastAPI endpoint receiving Telegram updates. Deduplicates via Redis. Routes to appropriate handler (text, voice, command). Responds within 2s P95. | `api/telegram_webhook.py` | 2.1 | 🔒 |
| 3.02 | **Build Vidye router (CBCS mode)** — Routes incoming client messages to the correct handler: ritual response, journal entry, voice note, crisis signal, general question. Uses Gemini Flash for fast classification. | `agents/vidye/cbcs_router.py` | 2.1 | 🔒 |
| 3.03 | **Initialize Neo4j Context Premise schema** — Create node types (User, Fear, Enemy, Dream, Ally, Victory, Pattern) and relationship types (TRIGGERS, OVERCOMES, CONNECTED_TO) with emotional_weight properties. Write Cypher setup script. | `scripts/setup_neo4j.py` | 5.1 | 🔒 |

### Client Interaction Flows

| # | Task | Target | Story | Blocker |
|---|---|---|---|---|
| 3.04 | **Build ritual delivery scheduler** — Creates daily accountability messages within the coach-configured time window. Messages reference the client's current Context Premise (specific fears, boundaries, victories). TTT calibrated to coach voice. | `services/ritual_scheduler.py` | 2.1 | |
| 3.05 | **Build journaling prompt generator** — Generates 2-3 weekly prompts based on the client's emotional arc and recent interactions. Applies Boredom Ban (no prompt archetype repeats within 3 weeks). | `services/journal_prompts.py` | 2.2 | |
| 3.06 | **Build Aria voice note processor** — Receives client voice note → Groq transcription → entity extraction. Updates Context Premise graph (Fears, Enemies, Dreams, Allies, Victories, Patterns). Triggers pattern alerts as Notion comments. | `agents/aria/voice_processor.py` | 2.3 | |
| 3.07 | **Build dormancy recovery engine** — Detects silence after configurable threshold (default: 72h). Escalation ladder: Day 3 gentle nudge → Day 5 past victory callback → Day 7 direct question → Day 10 coach notification. All messages TTT-calibrated. | `services/dormancy_recovery.py` | 2.4 | |
| 3.08 | **Build Circuit Breaker** — First-pass crisis keyword detection on every incoming message. On trigger: halt automation for this client, notify coach via Telegram within 10s with flagged message + context, log in Receipt Chain. Resume only on coach reset. | `core/circuit_breaker.py` | 2.5 | 🔒 |

### Client Onboarding

| # | Task | Target | Story | Blocker |
|---|---|---|---|---|
| 3.09 | **Build CBCS client onboarding flow** — When a new client messages the bot: assign Person ID (`CCC-NNNN`), create Neo4j node, create Notion Client Intelligence page, run initial context extraction from first message. | `services/client_onboarding.py` | 7.3, 5.1 | |
| 3.10 | **Build SoulResonance emotional continuity** — Maintains session-to-session emotional continuity. Before generating any response, loads the client's recent emotional arc from Episodic Memory. Ensures callbacks to previous interactions feel natural, not mechanical. | `services/soul_resonance.py` | 2.1 | |

**Sprint 3 Deliverable:** A test client messages the Telegram bot → receives daily rituals, journaling prompts, and contextual responses in the coach's voice. Crisis detection works. Dormancy recovery triggers after silence.

---

## Sprint 4: Notion Delivery Layer

*Goal: All content and client intelligence appears in Notion automatically, styled and interactive.*

**Stories covered:** 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 3.9

### Core Sync Engine

| # | Task | Target | Story | Blocker |
|---|---|---|---|---|
| 4.01 | **Build `notion_sync.py` core** — Python wrapper using the `notion-client` SDK. Handles authentication, rate limiting (3 req/s), retry logic, and error reporting. | `services/notion_sync.py` | 7.1 | 🔒 |
| 4.02 | **Build content page builder** — Creates a Content Calendar entry with the 7 structured sections: 🎙️ Voice Note (audio block), 💡 Why This Post, 🌱 Leadership Farming, 📄 Script, 📸 Coach Photo, 🖼️ Visual Assets, 📋 Posting Notes. Uses callout blocks, toggles, dividers, colored text — not plain paragraphs. | `services/notion_content_builder.py` | 7.1 | |
| 4.03 | **Build client page builder** — Creates/updates Client Intelligence entries. Surfaces the psychological profile as clean narrative. Populates properties: Person ID, Status, Ritual Streak, Sentiment Trend. Adds pattern alerts as comments. | `services/notion_client_builder.py` | 7.1 | |
| 4.04 | **Build audio block handler** — Takes a Supabase Storage URL for a voice note/Sacred Audio clip. Creates a Notion audio embed block. Handles OGG format. Adds transcript as a toggle block below the audio. | `services/notion_audio.py` | 7.1 | |

### Database Setup

| # | Task | Target | Story | Blocker |
|---|---|---|---|---|
| 4.05 | **Build Notion workspace provisioner** — Creates the 4 databases in a coach's Notion workspace: Content Calendar, Client Intelligence, Webinar & Tierlist Assets, Personal Branding Photo Deck. Sets all properties, views, and default sorts. | `scripts/setup_notion_workspace.py` | 6.5, 7.4 | 🔒 |
| 4.06 | **Configure conditional color rules** — Apply rules across all databases: Content Calendar (🔴 overdue, 🟢 on-schedule, 🟡 tomorrow, 🔵 seasonal match), Client Intelligence (🟢 engaged, 🔴 dormant, 🟡 declining), Photo Deck (🔴 overused). | Manual Notion UI setup + documentation | 7.4 | |
| 4.07 | **Configure tabbed layouts** — Content pages: Script / Visuals / Metrics tabs. Client pages: Profile / Sessions / Voice Journal tabs. | Manual Notion UI setup + documentation | 7.4 | |
| 4.08 | **Build Notion formula properties** — Implement formulas: Countdown Pulse (days until publish → emoji indicator), Progress Bar (milestone ratio → emoji bar), Engagement Heat (streak → text label), Seasonal Indicator (month → color emoji). | Notion formula definitions (documented) | 7.4 | |

### Automation & Webhooks

| # | Task | Target | Story | Blocker |
|---|---|---|---|---|
| 4.09 | **Build webhook receiver for Notion status changes** — FastAPI endpoint that receives Notion automation webhooks when a coach changes Status from Draft → Approved. Triggers the distribution pipeline for that Asset ID. | `api/notion_webhook.py` | 7.6 | |
| 4.10 | **Build distribution pipeline** — Receives an approved Asset ID. Generates posting-ready files, attaches posting notes, updates Receipt Chain, marks Notion status as "Ready to Post." Notifies coach via Notion notification. | `services/distribution.py` | 7.6, 3.9 | |
| 4.11 | **Build Photo Deck sync** — When a coach uploads a photo to the Photo Deck database, assign a `PHOT` Asset ID, upload to Supabase Storage, and track usage count. Enforce the Sovereign Image Rule (block AI coach imagery). | `services/photo_deck_sync.py` | 7.5 | |

### Posting Support

| # | Task | Target | Story | Blocker |
|---|---|---|---|---|
| 4.12 | **Build posting notes generator** — For each approved piece, generate platform-specific posting instructions: optimal time, hashtag suggestions, caption variants, engagement prompts. Attach to the Notion content page's Posting Notes section. | `services/posting_notes.py` | 3.9 | |

**Sprint 4 Deliverable:** Run `ccf-weekly` → content appears in the coach's Notion Content Calendar with all 7 sections, conditional colors, and tabbed layouts. Coach changes status → webhook triggers distribution.

---

## Sprint 5: Intelligence Loops & V2WS

*Goal: Data flows between CCF and CBCS, making both smarter. Webinar pipeline works.*

**Stories covered:** 5.2, 5.3, 5.5, 4.1, 4.4, 6.2, 6.3, 6.4

### Intelligence

| # | Task | Target | Story | Blocker |
|---|---|---|---|---|
| 5.01 | **Build Sunday Bot Meeting aggregator** — Runs weekly. Aggregates patterns across all of a coach's clients: dominant fears, breakthrough themes, friction points. Outputs a signal summary for `ccf-analyze`. | `services/sunday_bot_meeting.py` | 5.2 | |
| 5.02 | **Build engagement feedback ingestion** — Captures content engagement metrics (saves, shares, comments) per content piece. Tags high-performing themes as "resonance markers" in the coach profile. Feeds into next content cycle. | `services/engagement_feedback.py` | 5.3 | |
| 5.03 | **Build Azaria memory promoter** — Evaluates patterns by frequency, consistency, and impact. Flags promotion candidates for Operator review with evidence and confidence scores. Handles approve/reject/defer workflow. | `agents/azaria/memory_promoter.py` | 5.5, 6.4 | |

### V2WS Webinar Pipeline

| # | Task | Target | Story | Blocker |
|---|---|---|---|---|
| 5.04 | **Build YOLO mode webinar intake** — Receives 5 coach answers (teach what, audience, offer, stories, tone). Runs DEEP/FRESH research. Generates module-by-module webinar script. | `commands/v2ws_yolo.py` | 4.1 | |
| 5.05 | **Build webinar module generator** — Generates individual webinar modules using the Jason Fladlien method. Each slide is a HOOK. Applies TTT calibration and Boredom Ban. | `agents/webinar_generator/module.py` | 4.1 | |
| 5.06 | **Build Excalidraw compiler** — Takes generated modules + visual assets. Compiles into a branded `.excalidraw` file with text layers and image nodes. Exports to PDF/PPTX if needed. | `services/excalidraw_compiler.py` | 4.4 | |
| 5.07 | **Build Transparent Collage Pipeline** — Visual Reasoning Protocol → T2I prompt (white bg) → alpha extraction (background removal) → transparent PNG → inject as `image` node in `.excalidraw` JSON. | `services/transparent_collage.py` | 4.4 | |

### Operations

| # | Task | Target | Story | Blocker |
|---|---|---|---|---|
| 5.08 | **Build provenance tracer** — Given any Asset ID, returns the full chain: source data → research → generation prompt → agent output → validation decisions → edits → final version. Queries Receipt Chain + file system. | `services/provenance_tracer.py` | 6.2 | |
| 5.09 | **Build agent config manager** — Operator can edit any agent's SKILL.md, prompt template, or tool config. Changes are versioned, logged, and take effect on the next pipeline run. Rollback support. | `services/agent_config.py` | 6.3 | |

**Sprint 5 Deliverable:** Sunday Bot Meeting outputs feed into `ccf-analyze`. YOLO mode webinar produces a complete `.excalidraw` file. Provenance tracer works for any Asset ID.

---

## Sprint 6: Polish, Interactive Modes & Scale

*Goal: Remaining P2/P3 stories, interactive webinar mode, cross-ecosystem meeting, and full integration testing.*

**Stories covered:** 4.2, 4.3, 4.5, 5.4, 2.1 (refinements)

### Interactive Webinar Mode

| # | Task | Target | Story | Blocker |
|---|---|---|---|---|
| 6.01 | **Build Interactive Mode webinar session** — Guided via Telegram, module-by-module. Coach describes teaching intent → system writes one module → coach approves/redirects → next module. Full Intelligence Library access for agent suggestions. | `commands/v2ws_interactive.py` | 4.2 | |
| 6.02 | **Build dynamic module adjuster** — Aggregates audience Context Premises to rank webinar modules by theme relevance. Adjusts module emphasis for current audience. Logs reasoning. | `services/module_adjuster.py` | 4.3 | |

### Cross-Ecosystem & Refinements

| # | Task | Target | Story | Blocker |
|---|---|---|---|---|
| 6.03 | **Build Monthly Cross-Ecosystem Meeting** — Anonymized intelligence sharing across coach ecosystems: format performance patterns, engagement trends, recovery strategies. Summary output for Operator. | `services/cross_ecosystem_meeting.py` | 5.4 | |
| 6.04 | **Build Resonance Hit formula connector** — Cross-references content themes against client patterns using Notion formulas. Where matches exist, adds `🟣 RESONANCE HIT` indicators to both Content Calendar and Client Intelligence. | `services/resonance_connector.py` | 7.4 | |
| 6.05 | **Refine ritual delivery with Resonance Hits** — When a content piece matches a client's active pattern, the ritual delivery can reference it: "Your coach just wrote something about this — have you seen it?" | `services/ritual_resonance.py` | 5.3 | |
| 6.06 | **Full integration test suite** — End-to-end: Genesis → `ccf-weekly` → Notion delivery → CBCS client interaction → Sunday Bot Meeting → next `ccf-weekly` with intelligence feedback. Verify Receipt Chain integrity across all steps. | `tests/integration/full_cycle_test.py` | All | |

**Sprint 6 Deliverable:** Full system cycle works end-to-end. Interactive webinar mode functional. Cross-ecosystem meeting runs for all coaches. All conditional colors, formulas, and tabbed layouts verified in Notion.

---

## Sprint Dependency Graph

```
Sprint 1 (Genesis) ────────┬──→ Sprint 2 (CCF Pipeline)
                           │         │
                           │         ├──→ Sprint 4 (Notion Delivery)
                           │         │         │
                           ├──→ Sprint 3 (CBCS) ──→ Sprint 5 (Intelligence + V2WS)
                           │                              │
                           └──────────────────────────────→ Sprint 6 (Polish + Integration)
```

## Total Task Count

| Sprint | Tasks | Duration | Focus |
|---|---|---|---|
| Sprint 1 | 14 | 2 weeks | Foundation + Genesis |
| Sprint 2 | 14 | 2 weeks | CCF Production Pipeline |
| Sprint 3 | 10 | 2 weeks | CBCS Coaching Engine |
| Sprint 4 | 12 | 2 weeks | Notion Delivery Layer |
| Sprint 5 | 9 | 2 weeks | Intelligence + V2WS |
| Sprint 6 | 6 | 2 weeks | Polish + Integration |
| **Total** | **65** | **12 weeks** | **Full CCP v1.0** |

## Blocker Chain

The following tasks must complete before anything downstream can start:

```
1.01 (scaffold) → 1.06 (receipt chain) → 1.07 (asset ID) → ALL generation tasks
1.02 (registry) → 1.14 (genesis cmd) → 2.02 (ccf-analyze) → 2.04+ (generation)
1.03 (soul schema) → 1.10 (TTT) → 1.14 (genesis) → ALL content tasks
3.01 (webhook) → 3.02 (router) → ALL CBCS interaction tasks
3.03 (neo4j) → 3.06 (aria) → 3.04 (rituals)
4.01 (notion core) → 4.02-4.04 (builders) → 4.05 (provisioner)
```
