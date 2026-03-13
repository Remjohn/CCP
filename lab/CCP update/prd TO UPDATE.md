# Unified Conscious Coaching Platform (CCP) — Product Requirements Document

**Version:** 1.0 (Integration Phase)  
**Status:** DRAFT  
**Scope:** Integration of CCF, CBCS, V²WS, and Tierlist.  
**Author:** Mitano  
**Date:** 2026-02-27  

---

## Executive Summary

The **Conscious Coaching Platform (CCP)** is a unified intelligence infrastructure that transforms a coach’s raw expertise into a sovereign, multi-modal ecosystem. It is an isolated, cloud-native **Trigger-First Operating System**.

**The problem:** For years, coaching and content creation have existed in fragmented silos. The tools available are either monolithic prompts that strip away the coach's identity (resulting in soulless "AI slop") or disconnected apps where the coaching bot doesn't learn from content performance, and webinar scripts ignore the emotional cadence of 1-on-1 sessions. Every interaction starts from zero, wasting intelligence and breaking the coach's authentic voice.

**The vision:** The CCP solves this through absolute unification. It operates as a deterministic, **Trigger-First Engine** where nothing is generated in a vacuum. A user's emotional state triggers a real-time coaching ritual; a coaching insight triggers a webinar module; audience sentiment triggers a 14-format content batch. The entire ecosystem—spanning real-time interaction (CBCS), content production (CCF), visual strategy (Tierlist), and deep-dive education (V²WS)—is sustained by a single, shared intelligence loop.

**The outcome:** Output across every touchpoint that is structurally identical to master-level human craftsmanship, at scale, with zero hallucination.

### What Makes This Platform Sovereign

**Upstream Intelligence (CRAL).** The CCP abandons the flawed paradigm of prompting an LLM to "be creative." All generation is preceded by the **Conscious Research Alchemy Lab (CRAL)**. Our 9 specialized research skills act as the upstream foundation, guaranteeing that before a single word of a script or ritual is drafted, it is rooted in pre-validated, hyper-specific research frameworks (Deep Research, Fresh Sentiment, Psycho-Geographic Mapping).

**3-Dimensional Voice DNA.** The cardinal sin of AI is predictable generation. The CCP captures the coach's identity across three strict axes: **What** (Soul-Alignment and core message), **How** (Construction Mechanics and formatting constraints), and **Path** (Emotional Architecture and persuasion cadence). This 3D Voice DNA is fused into a **JIT (Just-In-Time) Skill Compilation** pipeline, ensuring the exact same coach's soul speaks through a 30-second Telegram voice note and a 90-minute webinar close.

**Deterministic Execution.** The system does not rely on "free-thinking" agentic loops for production. We utilize the **Conscious Cognitive Skill Builder (CCSB)** to turn chaotic generative tasks into rigid, predictable engineering. Complex coaching strategies are translated into structured Design Briefs and executed through the 8-component JIT Skill Compiler. The result is an impenetrable pipeline governed by a Dependency Registry and Adapter Registry—meaning the output is always 100% traceable, mathematically diverging from standard AI generation through our rigorous Anti-Draft constraints.

## Project Classification

**Technical Type:** Agentic Multi-System Platform (multi-agent orchestration across 5 merged sub-systems)  
**Domain:** Coaching / Ed-Tech / Creator Economy  
**Complexity:** HIGH  

- **65 named agents** across 6 departments (Perception, Strategy, Expression, Management, Safety, Setup)
- **147 skills/tools** across 10 families + 4 Python wrappers + 2 apps
- **49 pipeline elements** (28 CCF commands + 12 CBCS modules + 6 V²WS + 3 Tierlist)
- **4 distinct pipeline architectures** (command-based CCF, event-driven CBCS, sequential V²WS, hybrid Tierlist)
- **3-tier memory** with weekly evolution cycle
- **Real-time + batch** processing (CBCS <2s latency; CCF weekly production cycles)

---

## Success Criteria

### User Success

The coach's client follows their program, gets measurable results, and develops lasting habits. Specifically:

- **Program Adherence:** Users complete their assigned rituals at a rate of ≥80% per week, tracked via CBCS interaction logs and accountability check-ins (daily prompts + 2-3x/week journaling).
- **Habit Formation:** Users demonstrate consistent engagement patterns over 30+ days — the system detects habit consolidation through decreasing dormancy gaps and increasing self-initiated interactions.
- **Behavioral Results:** Users report tangible progress toward their coaching goals. Measured through periodic self-assessments (Atlas roadmap checkpoints) and coach-confirmed milestone completions.
- **Accountability Experience:** The proactive scheduling system (daily check-ins, journaling prompts, dormancy recovery) feels supportive, not robotic. Users respond to accountability nudges rather than ignoring them.

### Business Success

- **Coach Onboarding Target:** 24 coaches fully onboarded and producing content through the CCP within the first operational cycle.
- **Coach Retention:** Onboarded coaches continue using the platform weekly after initial setup — measured by weekly `ccf-weekly` pipeline execution and CBCS active user counts.
- **Cross-System Value:** Coaches experience the intelligence loop — coaching insights inform content, content performance data feeds back to coaching — as a tangible productivity advantage over disconnected tools.

### Technical Success

- **Progressive Engagement Growth:** Content produced by the CCP consistently generates more engagement over time for each coach. Measured by comparing engagement metrics (views, saves, shares, comments) across successive weekly production cycles. The system's learning loops (Sunday Bot Meeting, Real Time Tribe Relevance, Boredom Ban) must demonstrably improve content performance week-over-week.
- **Zero AI Detection:** Content passes the Mimicry Validator (Chen) at <5% AI detection rate. No coach's audience should ever suspect the content is AI-assisted.
- **Voice Consistency:** TTT drift stays below 15% across all outputs for each coach (Soul Validator threshold: >85% alignment to `coach_soul.json`).
- **System Reliability:** CBCS responds within <2s per message. CCF weekly pipeline completes without manual intervention. Receipt Chain Guard maintains unbroken audit trails.
- **Seasonal Alignment Score:** Content passes the 4-layer seasonal influence check (Macro 5%, Meso 8%, Micro 12%, Pinnacle 20%) with a timing_score ≥ 0.3 on at least 80% of ideas per cycle. (See CCP Technical Architecture §6.5)
- **Contrastive Distance Score:** Generated content maintains a contrastive distance of ≥ 0.5 from its archetype-specific anti-draft across all 36 weekly pieces. Content with low contrastive distance triggers TillDone rewrite. (See CCP Technical Architecture §5.3 Phase C)
- **Leadership Trait Coverage:** The coach's `leadership_scorecard.json` shows measurable improvement (≥5 points) in at least 2 weak traits within the first quarter of platform usage. No single trait dominates >25% of weekly format assignments. (See CCP Technical Architecture §6.6)
- **Notion Delivery Uptime:** `notion_sync.py` successfully pushes all weekly deliverables to the coach's Notion workspace with zero failed syncs. Asset IDs match across Notion, Supabase, and Receipt Chain. (See CCP Technical Architecture §8.3-8.4)

### Measurable Outcomes

| Metric | Target | Measurement |
|---|---|---|
| Coach onboarding | 24 coaches | Count of coaches with completed Genesis Pipeline |
| User ritual completion | ≥80% weekly | CBCS interaction logs / total scheduled rituals |
| User habit formation | 30-day streak | Decreasing dormancy gaps in state machine |
| Content engagement growth | Week-over-week increase | Average engagement per content batch (rolling 8-week comparison) |
| AI detection rate | <5% | Chen validator scores across all published content |
| Voice alignment | >85% | Sophia validator TTT drift scores per coach |
| CBCS response time | <2s | P95 latency from webhook receive to delivery |

## Product Scope

### Full Product — Not MVP

The CCP is **not** an MVP. All four sub-systems (CCF, CBCS, V²WS, Tierlist) have been tested and validated independently. The integration phase builds on proven components:

- **CCF** — 85 skills across 10 families, 28 commands, 26+ agents, battle-tested production pipeline
- **CBCS** — 12 agents, real-time Telegram bot, crisis detection, multi-ritual engine, live with users
- **V²WS** — 31 design papers defining the complete webinar architecture + Excalidraw-native visual pipeline
- **Tierlist** — Excalidraw-native rendering templates, functional prototype

### Integration Scope (What CCP Adds)

The CCP integration adds what each system could not do alone:

1. **Unified Memory Layer** — `MemoryFolder` extension connects all 5 systems to a shared 3-tier memory (Working → Episodic → Semantic)
2. **Shared Voice DNA** — `SoulResonance` extension ensures `coach_soul.json` calibrates every output across every system
3. **Cross-System Intelligence** — Coaching engagement data feeds content strategy; content performance feeds coaching personalization
4. **11 Pi Extensions** — The connective tissue (ModelRouter, SystemSelect, SoulResonance, etc.) that turns 5 separate tools into one platform
5. **Receipt Chain Guard** — Immutable audit trail across all pipeline executions
6. **Proactive Scheduling** — Unified scheduler for accountability, journaling, dormancy recovery, and weekly evolution cycles

### Future Extensions (Post-Integration)

- Multi-coach team dashboards and analytics
- Client-facing mobile app (beyond Telegram)
- White-label platform offering for coaching organizations
- Advanced voice synthesis (text-to-speech with TTT-calibrated prosody)
- Community features (tribe-to-tribe interactions)

---

## User Journeys

### Journey 1: Amara — Following the Program and Building Habits

**User Type:** Coach's Client (End User via Telegram)

Amara is a 34-year-old marketing manager who signed up for a coaching program to break her cycle of overwork and build healthier boundaries. She's tried apps before — they lasted a week. She's skeptical but committed because her coach, Nadia, genuinely understands her struggle.

Monday morning, 7:15 AM. Amara's phone buzzes with a Telegram message. It's not a generic "How are you feeling today?" — it's a message that references the specific boundary she set last week with her team lead, and asks how that conversation went. She pauses. *How does it know about that?* She replies honestly: she chickened out. Within seconds, a new ritual arrives — not a lecture, but a 90-second reflection exercise built around a story about a lion who mistook its cage for safety. The metaphor hits differently because it mirrors something Nadia said in their last session, in Nadia's exact voice cadence.

Wednesday evening, journaling prompt. It doesn't ask "What are you grateful for?" — it asks her to describe the moment this week where she felt the strongest pull to say yes when she meant no. Amara writes three paragraphs. She doesn't realize she's doing therapy homework.

Two weeks later, Amara notices something: she looks forward to the morning message. She's completed 12 of 14 rituals. On day 31, she has the conversation with her team lead. She messages the bot: "I did it." The response celebrates specifically what she did — not a template congratulations, but a callback to the lion metaphor. She screenshots it and sends it to her best friend.

**This journey reveals requirements for:**
- CBCS real-time ritual delivery (<2s)
- Proactive daily accountability scheduling (coach-program-configurable)
- Journaling prompts (2-3x/week)
- Dormancy recovery (if she goes silent)
- Emotional continuity across sessions (Episodic Memory → SoulResonance)
- Voice consistency (Nadia's voice, not generic AI)
- Crisis detection (Circuit Breaker if she expresses distress)

### Journey 2: Coach Nadia — Onboarding, Content, and Notion Command Center

**User Type:** Coach (Power User)

Nadia is a certified life coach with 180 Instagram followers and 12 active clients. She's great one-on-one but struggles with content. She spends Sundays writing posts that get 15 likes. She heard about the CCP from a colleague who tripled her engagement in two months.

**Onboarding (Day 1-3):** Nadia runs `ccf-init` and answers Kimya's elicitation questions about her coaching philosophy, her ideal client, and her core message. She uploads three audio recordings of her best coaching sessions — the ones where clients cried because something finally clicked. The system extracts her voice DNA: she's warm but direct, uses animal metaphors instinctively, and her emotional peaks always involve a pause before the pivotal sentence. `coach_soul.json` is born. She receives her coach ID: `NDL-0000`.

**First Production Week:** Nadia runs `ccf-weekly`. She doesn't write anything. The system produces 36 scripts across 14 formats — threads, carousels, reels scripts, meme concepts — all in her voice. She opens Notion. Her Content Calendar has 36 new entries — each one color-coded 🟢 for on-schedule. She clicks the first script. At the top: her own voice note clip from the Sacred Audio session, and a "Why This Post" section that says *"This came from something you said about boundaries — your words: 'They know. They've always known. They just keep the mirror face-down.'"* She reads the script below. *That sounds like me on a good day.* She changes Status from Draft to Approved — and that single click triggers the distribution pipeline. She reviews, tweaks two scripts (the system was slightly too formal in one thread), and publishes. Her carousel about "The 3 Boundaries Your Therapist Won't Tell You About" gets 847 likes — her previous best was 43.

**Managing Clients in Notion:** Nadia opens the Client Intelligence database. She sees 12 rows. Amara's row glows 🟢 — ritual streak at 14 days. But James's row is 🔴 — 9 days silent. She clicks into James's page, flips to the Voice Journal tab, and re-listens to his last message from 10 days ago. She reads the pattern alert in the comments: *"Authority figures trigger shutdown responses (3rd occurrence)."* She understands the silence now. She reaches out directly — not because a system told her to, but because the profile gave her the insight to act on her own instinct.

**Week 8 and beyond:** The system has learned. Her engagement data feeds back into theme discovery. The topics that get saved (not just liked) shape next week's content direction. She uploads 15 photos to her Personal Branding Photo Deck in Notion — tagged by mood and setting — so the system uses her real face for quote cards instead of generic stock imagery. Her audience grew from 180 to 2,400 followers. More importantly, 6 new coaching clients came from content alone. Nadia hasn't written a single post manually since onboarding. She spends her Sundays with her family.

**This journey reveals requirements for:**
- Genesis Pipeline (8 commands, sequential onboarding + leadership trait scoring)
- Sacred Audio processing (voice DNA extraction)
- CCF Weekly Production Pipeline (19 commands, automated — includes 3 embedded governance ministers)
- Content performance tracking → feedback loop (Sunday Bot Meeting)
- Validation Team gate (Sophia/Marcus/Chen triple-pass)
- Embedded Governance Ministers (Identity, Relevance, Timing — see CCP Technical Architecture §6.5)
- Progressive engagement growth (the core technical success metric)
- Notion Delivery Layer (Content Calendar, Client Intelligence, Photo Deck — see §8.3)
- Universal Asset ID & Person ID tracking (see §8.4)
- Dashboard UX (conditional color, tabbed layouts, database buttons — see Design Spec)

### Journey 3: Mitano — Building the System, Monitoring Health

**User Type:** System Operator / Admin

Mitano is the architect and operator of the CCP. He doesn't use the platform as a coach — he builds it, maintains it, onboards coaches, and monitors system health. His day involves agent development, pipeline debugging, and quality assurance.

**Morning:** Mitano checks the Receipt Chain Guard logs. One chain broke overnight — Marcus (Protocol Validator) flagged a malformed script that didn't have the correct beat count. He investigates: the `script-generator` skill received an incomplete archetype assignment. He traces it back to `ccf-analyze` producing a malformed `ideas.json` for coach #17. He patches the validation rule in Emilio's skill and re-runs the batch.

**Midday:** A new coach (coach #19) needs onboarding. Mitano runs the Genesis Pipeline, monitors each step, and verifies that `coach_soul.json` was populated correctly from the Sacred Audio upload. He spot-checks the TTT baseline — the new coach has an unusually high Witness score, which means the system will naturally produce more reflective content. He adjusts nothing; the system adapts.

**Weekly:** Sunday Bot Meeting results arrive. Azaria (Memory Curator) promoted 4 new patterns to Semantic Memory. One pattern: coach #8's audience responds disproportionately to "failure confession" content. This gets tagged as a tribal archetype signal and will influence theme discovery for coach #8's next production cycle. Mitano reviews the promotions, approves them, and checks the system-wide engagement trend. 18 of 24 coaches showed week-over-week engagement growth. The 6 who didn't are new onboards still in their first 3 weeks.

**This journey reveals requirements for:**
- Receipt Chain Guard monitoring UI/logs
- Pipeline debugging and re-run capabilities
- Coach onboarding management
- Sunday Bot Meeting review interface
- System-wide analytics dashboard
- Agent skill editing and maintenance workflow
- Memory promotion approval flow

### Journey 4: Kévin — Discovering the Coach Through Content

**User Type:** Coach's Audience (Potential Client)

Kévin is a 28-year-old software developer struggling with impostor syndrome at his new job. He's scrolling Instagram at midnight when he sees a carousel: "Why Your Best Work Terrifies You — And What That Actually Means." It's from Nadia, a coach he's never heard of. The first slide hooks him because it describes his exact internal monologue during standup meetings. By slide 4, he's screenshot-sharing it to his group chat.

He visits Nadia's profile. Every post feels like the same person talking — not the usual "motivational speaker on Monday, corporate coach on Wednesday" inconsistency he sees everywhere. He reads a thread about a client who went from dreading presentations to volunteering for them. It doesn't feel like a testimonial — it feels like a story someone actually lived. He saves it.

Over three weeks, Kévin consumes 20+ pieces of Nadia's content. The memes make him laugh. The threads make him think. The reels make him feel seen. He doesn't know that 65 agents produced this content, that a Boredom Ban ensured none of it repeated, or that `InteractComp` adjusted the topic selection based on engagement patterns from people like him. He just knows that this coach *gets it*.

He DMs Nadia: "Do you take new clients?" She does. Kévin becomes client #13. Three months later, he's presenting at a company all-hands and thinking about that lion metaphor.

**This journey reveals requirements for:**
- CCF multi-format content production (14 formats)
- Voice consistency across all format types (tweets, carousels, reels, memes)
- Boredom Ban (no content repetition over 8 weeks)
- InteractComp (audience engagement signal processing)
- Tribe distillation (content calibrated to audience archetypes)
- Content-to-coaching conversion funnel (content → DM → client)
- Cross-system loop: Kévin's engagement data → informs Nadia's content → he becomes a coaching client → CBCS learns his patterns

### Journey Requirements Summary

| Capability Area | Journey 1 (Client) | Journey 2 (Coach) | Journey 3 (Operator) | Journey 4 (Audience) |
|---|---|---|---|---|
| Real-time ritual delivery | ✅ | | | |
| Proactive scheduling | ✅ | | | |
| Voice consistency | ✅ | ✅ | | ✅ |
| Crisis detection | ✅ | | | |
| Sacred Audio processing | | ✅ | | |
| Genesis Pipeline | | ✅ | ✅ | |
| Weekly Production Pipeline | | ✅ | | ✅ |
| Validation Team gate | | ✅ | ✅ | |
| Progressive engagement | | ✅ | ✅ | ✅ |
| Receipt Chain monitoring | | | ✅ | |
| Memory promotion | | | ✅ | |
| System analytics | | | ✅ | |
| Multi-format content | | ✅ | | ✅ |
| Boredom Ban | | ✅ | | ✅ |
| InteractComp signals | | | | ✅ |
| Tribe distillation | | | | ✅ |
| Content → client conversion | | | | ✅ |

---


## Innovation & Novel Patterns

> **3 years of daily iteration.** The innovations below did not arrive in a single moment of insight. They are the result of compounded intelligence layers — each one discovered through real-world testing, failure, and rebuilding. The CCP is not a v1 product; it is the unification of battle-tested systems whose individual innovations have already proven themselves independently.

### CCF — Content Engine Breakthroughs

1. **Context Premises (The Psychological Map)** — The core innovation is the extraction and mapping of the user's *Context Premise* — a 12-dimensional psychological map of their internal battlefield (Fears, Enemies, Dreams, Hidden Beliefs). Extracted via Aria from unstructured voice data and stored as a graph ontology in **Neo4j**, we do not store abstract summaries; we store visceral, emotional language. Content generation doesn't start from a blank prompt; it starts by querying this hyper-personalized psychological graph.

2. **TTT — Voice Engineering (Temperature, Temperament, Tone)** — Not a style guide. A measurable, 3-axis voice calibration framework that quantifies how a coach communicates. Temperature = emotional intensity. Temperament = disposition pattern. Tone = linguistic register. Every output is measured against the coach's TTT baseline — drift >15% triggers rejection.

3. **Voice DNA Extraction & Soul Infusion** — Sacred Audio recordings from real coaching sessions are analyzed to extract the coach's unique speech patterns: their signature metaphors, their emotional peaks, their pause cadence, their storytelling rhythm. This becomes `coach_soul.json` — the biological DNA that infuses every output with the coach's authentic voice.

4. **Separate DEEP & FRESH Research Tracks** — Research is not a single pass. The system runs two parallel intelligence streams: DEEP research (perennial principles, emotional truths, audience psychology) and FRESH research (trending topics, current events, real-time platform dynamics). Content that combines timeless depth with timely relevance consistently outperforms.

5. **Research Analysts Specialized by Content Archetype** — Each content archetype (The Educator, The Challenger, The Storyteller, etc.) has a dedicated research analyst sub-agent (Ketsia, Sarah, Chiara, Noemie, Rafael, Estelle) who processes raw research through the lens of that specific archetype. The same research material produces fundamentally different content depending on which archetype processes it.

6. **Emotional Triggers-Based Content Archetypes** — Content archetypes are not format categories (carousel, reel, thread). They are *emotional trigger* categories — each one engineered to activate a specific psychological response in the audience. The archetype determines the emotional journey before format is even considered.

7. **12-Month Seasonal Governance (The Breathing Calendar)** — The validation layer follows a 12-month seasonal calendar where each month has a governing archetype (Architect, Lover, Seed, Warrior, etc.) that shapes validator expectations — not content topics, but the *vibe* of what passes. Four threshold months (Mar, Jun, Sep, Dec) trigger dual-lens validation. A 4-layer influence stack (Macro 5%, Meso 8%, Micro 12%, Pinnacle 20%) ensures the system reads annual trends, monthly seasons, weekly events, and rare high-impact moments simultaneously.

8. **Contrastive Anti-Drafting (The Architectural Immune System)** — Every content piece is generated twice: first by a less capable model that receives the *full* production context (SOC, voice DNA, tribe soul) and tries its best to sound like the coach. It fails authentically — producing robotic voice imitation, forced patterns, mechanical metaphors. This failure becomes the contrastive anchor. The premium model then receives the anti-draft alongside a 5-point precision directive identifying exactly *how* it fails. 14 archetype-specific failure profiles ensure each visual recipe gets its own calibrated negative anchor.

9. **Leadership Trait Scoring (The Coach Development Engine)** — The Minister of Identity scores each coach across 12 Leadership Traits (Deep Empathy, Authentic Vulnerability, Embodied Confidence, etc.) using signal sources from Sacred Audio, TTT baseline, and tribe extraction. The resulting `leadership_scorecard.json` informs format assignment: weak traits get more exercise, strong traits get more showcase. The system doesn't just produce content — it actively develops the coach into a stronger leader.

10. **Notion Delivery Layer (Never Outshine the Master)** — All coach-facing deliverables are delivered autonomously through Notion — not a custom app. Four databases (Content Calendar, Client Intelligence, Webinar & Tierlist Assets, Personal Branding Photo Deck) surface clean output with zero system visibility. Every content piece includes the coach's original voice note, a "Why This Post" section tracing the idea to their own words, and Leadership Farming notes. The Universal Asset ID (`AAAA-CCC-MM-YY-XXXX`) and Person ID (`CCC-NNNN`) systems provide full lifecycle traceability across all platforms. The Sovereign Image Rule ensures the coach's face is always real photographs — AI imagery represents client scenarios only. The [Notion Coach Dashboard Design Spec](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/Notion_Coach_Dashboard_Design_Spec.md) defines 24 UX techniques across 7 layers — conditional color, layout builder, tabbed layouts, automations with webhooks, smart formulas, database buttons, and structural polish — to ensure the workspace feels like the coach's own, not a tool's output. (See CCP Technical Architecture §8.3-8.4)

### V²WS — Webinar Engineering Breakthroughs

**Modular Webinar Architecture (Jason Fladlien Method)** — Webinar scripts are not written as monolithic outlines. They are constructed module-by-module, based on intensive study of Jason Fladlien's methodology, rebuilt as individual prompt modules with real examples. Each module applies its own TTT calibration (voice engineering for presentations). Every slide is engineered as a **HOOK** — not a presentation slide, a hook.

**From Sequential to Agentic** — Previously, webinar modules were assembled sequentially. Now, agents have access to real-time audience data and sentiment analysis, allowing dynamic module selection and emphasis adjustment based on who is actually watching. The modular precision remains, but execution is now intelligent.

### HUMOR — The Strategic Weapon

**Discovery:** In the early days of CCF, the breakthrough realization was that the only categories of AI-generated content consistently beating native human content in engagement are **memes and funny videos**. Humor is the ultimate AI-slop antidote — audiences will forgive imperfect production for genuine laughter.

**Application in coaching:** You can't do silly dances in the coaching niche. But you can deploy *strategic humor* — the kind that makes a profound point while making someone laugh. This is where the **Memetic Engine** becomes the CCP's secret weapon.

**Implementation:**
- Every content batch produces **tweets + memes** alongside serious scripts — this was already the case in the previous n8n system. Humor posts are native to every production cycle, not an afterthought.
- Humor is natively integrated into **visual content** (Tierlist, memes, social cards) and **webinars** (slide hooks, comedic analogies, pattern interrupts).
- The Boredom Ban enforces humor variety — the same joke format can't repeat within 8 weeks.

### CBCS — The Invisible App Paradigm

**The Bet:** 5-6 months ago, the intuition crystallized: AI is going to flood the market with coaching apps. Every competitor will build their own app. But people don't want another app — they want to use the tools they already use.

**The Innovation:** The lowest cognitive load possible is **voice notes in Telegram**. Users talk to the system thinking it's just a normal agent — a conversation in an app they already have. They don't know about the incredible layers of intelligence behind every response: the `InteractComp` interaction model, the `AtlasRoadmap` journey tracker, the `SoulResonance` voice calibration, the `CircuitBreaker` crisis protocol, the 12 specialized agents processing every single message.

**Why this wins:** Zero download friction. Zero onboarding friction. Zero app-switching cost. The invisible app is architecturally invisible but functionally the most sophisticated coaching intelligence on the market.

### Internal Methodology Innovations

**Distillation Funnel & The 4 Laws** — The system doesn't just generate content. Raw intelligence passes through a structured distillation process governed by 4 laws that progressively refine broad research into coach-specific, audience-calibrated, emotionally triggering content premises. Each law eliminates a category of generic output.

**MCDA & Micro-Drafting for Creative Agents** — Every agent involved in creative writing uses Multi-Criteria Decision Analysis (MCDA) to evaluate output against multiple dimensions simultaneously (emotional impact, voice alignment, novelty, archetype fit). Combined with micro-drafting — generating and scoring small content fragments before assembling full pieces — this ensures that creative quality is not left to chance.

### Validation & Competitive Landscape

**No direct competitor unifies all 5 systems.** Existing tools address individual pieces:
- Coaching bots exist (ManyChat, generic ChatGPT wrappers) — but none embed voice DNA or emotional continuity
- Content automation exists (Jasper, Copy.ai) — but none enforce consciousness archetypes or MCDA scoring
- Webinar tools exist (Loom, Descript) — but none use modular hook-per-slide architecture with audience sentiment

**The CCP's moat is compounded intelligence:** 3 years of iteration means the system's rules, constraints, and quality gates are the product of thousands of real-world content cycles. A competitor would need to not just replicate the architecture, but also the learning encoded in every skill, prompt, and validation rule.

---

## Agentic Ecosystem Specific Requirements

### Architecture Paradigm: Isolated Cloud-Native Instances

While the CCP functions conceptually like a B2B platform for coaches, its technical architecture is intentionally **not a monolithic SaaS**. To ensure absolute data privacy, uncompromising voice DNA fidelity, and unbounded agentic autonomy, the system uses an isolated deployment model:

- **Single-Tenant Repositories:** Every coach on the platform gets their own dedicated code repository. There is no shared `users` table or shared agent environment.
- **Dedicated Cloud Instances:** Each coach's ecosystem runs in an isolated cloud environment.
- **Pi Coding Agent Orchestration:** The deployment, maintenance, and execution of these individual coach ecosystems are managed globally by the Pi Coding Agent, which acts as the meta-orchestrator across all isolated instances.

### Data Isolation & Memory Model

Because each coach operates in a separate repo and cloud instance:
- **Graph Database Isolation:** Each coach has a dedicated Neo4j instance / graph schema storing their specific clients' Context Premises. There is zero risk of cross-pollination between coach audiences.
- **Vector Isolation:** RAG embeddings for the coach's Sacred Audio and Content Library are completely firewalled. `coach_soul.json` applies only to that specific instance.
- **Memory Integrity:** Sunday Bot Meeting promotions (Episodic → Semantic memory) happen per coach. The system learns what works for Coach A's audience without incorrectly assuming it will work for Coach B's audience.

### Processing Cadence & Scalability

An agentic ecosystem requires mastering two distinctly different processing paradigms within the same cloud instance:

1. **Real-Time Stream (CBCS):**
   - **Requirement:** Sub-2-second latency.
   - **Trigger:** Discord/Telegram webhook payloads from client voice notes.
   - **Execution:** Synchronous routing by ModelRouter, fast entity extraction by Aria, immediate hook generation.

2. **Asynchronous Batch (CCF/V²WS):**
   - **Requirement:** Uninterrupted long-running workflows.
   - **Trigger:** Scheduled Cron jobs (`ccf-weekly` via GitHub Actions or cloud scheduler) or manual operator trigger.
   - **Execution:** Parallelized multi-agent drafting, complex MCDA loops, sequential validation protocols (Marcus → Sophia → Chen). Can take 10+ minutes per batch.

### Integration Perimeters

The system's boundaries are defined by its primary I/O channels:
- **Client Input / Output:** Telegram API (voice notes in, multimedia rituals out).
- **Coach Output:** Telegram bot (for immediate alerts) and integrated social media publishing APIs (auto-posting to Instagram, Twitter, LinkedIn).
- **Operator Command:** CLI execution (for Mitano) and programmatic triggers via the Pi Coding Agent.
- **Visual Rendering:** Unified Excalidraw pipeline for all visual content — Tierlists, Webinars, Ratings, and Reaction Explainers. One tool, one set of branded templates, one rendering process.

### Reliability & Auditability

In an autonomous agent ecosystem, logging is not for debugging — it is for governance.
- **Receipt Chain Guard:** Every agent interaction, API call, and validation decision MUST be immutably recorded. If a bad script is published or an inappropriate ritual is sent, the operator must be able to trace the exact LLM prompt, context window, and agent decision tree that produced it.
- **Circuit Breaker:** The system must have a hard-coded, zero-latency override layer that detects crisis keywords (self-harm, abuse) and immediately halts the agentic loop, escalating to a human coach channel.

---

## Project Scoping & Phased Development

### Scope Philosophy: The "Integration MVP"

As defined in the Success Criteria, the CCP is **not a traditional MVP**. The core value engines — CCF (content), CBCS (coaching), V²WS (webinars), and Tierlist (visuals) — have already been built, tested, and validated over 3 years of iteration. 

Therefore, the "MVP" for the CCP is an **Integration MVP**. The goal of Phase 1 is not to build new generative features, but to build the *connective tissue* (the 11 Pi Extensions) that allows these 5 systems to share memory, voice, and data autonomously.

### Phase 1: Integration & Memory Unification (Current Scope)

The immediate development focus is wiring the existing systems together into a single agentic ecosystem per coach:

- **Core Capability:** Deploying the 11 Pi Extensions (ModelRouter, SystemSelect, MemoryFolder, InteractComp, etc.).
- **Data Unification:** Implementing the Neo4j graph database for Context Premise storage and ensuring all 5 systems read/write to the same user map.
- **Voice Unification:** Implementing `coach_soul.json` (Voice DNA extracted from Sacred Audio) across CCF, CBCS, and V²WS so the coach sounds identical everywhere.
- **Governance:** Deploying Receipt Chain Guard for auditability and Circuit Breaker for crisis management.
- **Goal:** 24 coaches successfully onboarded and running the integrated system.

### Phase 2: Autonomous Growth & Multi-Modal Output (Next Scope)

Once the systems share a brain, Phase 2 expands what the brain can do:

- **Visual Content Automation:** Fully activating the unified Excalidraw pipeline across all visual formats (Tierlists, Webinar slides, Ratings, Reaction Explainers). Integrating stick figure LoRAs for relatable, coach-branded visual assets.
- **Proactive Intelligence:** Enabling the system to suggest new coaching rituals based on aggregate audience data from CCF.
- **Coach Analytics UI:** A dedicated web dashboard (Next.js) for the coach to view their clients' Context Premise graphs, engagement metrics, and system health.

### Phase 3: Platform Expansion (Vision Scope)

- **White-Labeling:** The ability to spin up CCP instances for large coaching organizations under their own branding.
- **Voice Synthesis:** Advanced TTS integration so the coach's actual audio voice reads the generated scripts.
- **Community Orchestration:** Agents facilitating interactions *between* the coach's clients based on shared Context Premises (Tribe-to-Tribe matching).

### Risk Mitigation Strategy

| Risk Area | Risk Description | Mitigation Approach |
|---|---|---|
| **Technical** | LLM latency (specifically for CBCS sub-2s requirement) | Utilize ModelRouter to map low-latency tasks to fast models (Groq/MiniMax) and complex tasks to heavy models. |
| **Logic** | Hallucination degrading the Context Premise map | Strict enforcement of Entity Extraction protocols (Aria) and Marcus (Protocol Validator) checking all writes. |
| **Integrity** | AI slop creeping into the content | The Validation Team (Sophia/Marcus/Chen) triple-pass gate; immediate rejection of TTT drift >15%. |

---

## Functional Requirements 

### Coach Onboarding & Identity Capture

- FR1: Coaches can capture and submit Sacred Audio recordings natively via a Telegram chat conversation (no external upload interface — Telegram IS the interface).
- FR2: The system can extract and store the coach's Voice DNA (TTT baseline) from submitted Sacred Audio.
- FR3: The System Operator conducts the onboarding elicitation — proactively researching the coach's public presence and running a structured first-meeting protocol to capture coaching philosophy, core message, and ideal client profile. The coach provides zero-friction input; all heavy lifting is done by the operator.
- FR4: The system can generate the foundational `coach_soul.json` profile based on onboarding inputs.

### Audience Interaction & Behavioral Tracking (CBCS)

- FR5: End Users (clients) can receive and respond to daily accountability rituals natively via Telegram (voice or text).
- FR6: The system can deliver personalized journaling prompts 2-3x per week based on the end user's current progress.
- FR7: The system can parse unstructured voice notes from end users to extract and update their specific Context Premise (Fears, Enemies, Dreams).
- FR8: The system can trigger dormancy recovery protocols autonomously when an end user goes silent.
- FR9: The system can detect crisis keywords (self-harm, severe distress) and immediately halt agentic automation, triggering human escalation via the Circuit Breaker. The Coach is notified via Telegram and can respond to the end user directly.

### Content Generation & Publishing (CCF)

- FR10: The System Operator triggers the weekly content generation pipeline (`ccf-weekly`). The process always starts with research and guided questioning, never raw generation.
- FR10a: Coaches can natively suggest topics for future batches via Telegram. Suggested topics enter the standard research pipeline before generation.
- FR10b: The system tracks monthly content generation limits per coach via a dedicated **ContentCadence Extension**. When the monthly limit is reached, the weekly trigger is automatically paused until the next cycle.
- FR11: The system can autonomously generate content across 14 formats (including threads, carousels, reels scripts, and memes).
- FR12: The system applies the coach's Voice DNA to all generated content to ensure TTT consistency (drift <15%).
- FR13: The system natively integrates strategic humor (tweets + memes) into every content batch regardless of the content archetype chosen — powered by the **Humor Agent** and the **Tweet Meteorologist Agent**.
- FR13a: The **Humor Agent** can access vibe comments, humor style databases, and propose setups, plot twists, ironic/absurd/awkwardly relatable angles that pass the Vibe Check (not AI-generic humor).
- FR13b: The **Tweet Meteorologist Agent** can forecast digital conversation weather — tracking sentiment climate, outrage waves, viral trend spikes, meme explosions, narrative shifts, and attention cycles — to inform timely, culturally relevant humor and tweet angles.
- FR14: The system enforces a Boredom Ban constraint to prevent thematic repetition over an 8-week rolling window.
- FR15: The System Manager reviews, edits, and approves generated content prior to publication. Coaches do not review content — the System Manager has the expertise to judge what will perform.
- FR16: Coaches publish approved content manually to their own social media platforms. This is intentional: publishing is the coach's primary touchpoint for audience connection (**Vibe-Baiting** strategy). There is no auto-publish.

### Webinar & Visual Asset Automation (V²WS & Tierlist)

- FR17: Coaches can participate in webinar script creation via two modes:
  - **YOLO Mode (5 Questions → Full Delivery):** The coach answers 5 focused questions about (1) what actionable thing they want to teach, (2) who the audience is, (3) what the offer at the end is, (4) key stories/examples they want included, (5) tone/energy level. The system runs the full pipeline — DEEP/FRESH research, module construction, script writing — and delivers a **branded `.excalidraw` file** with module scripts embedded as text layers. The coach opens the file, reviews it, and records live. Exports to PDF/PPTX natively if needed.
  - **Interactive Mode (via Telegram):** A guided, module-by-module BMAD-style collaborative session. The coach is interviewed about their actionable teaching topic first (Stream of Consciousness capture). The system writes one module at a time, waits for the coach's approval, then proceeds to the next. The agent has full access to the Intelligence Library and Memory to make powerful context-aware suggestions. At the end, the coach uploads any image assets they have, and the system compiles the full set of branded Excalidraw slides.
- FR17a: Both modes always start with the coach's teaching intent — the specific actionable thing the coach wants to teach is the foundation before any research or generation begins.
- FR17b: Webinar scripts pass through the 4 Distillation stages and are subject to the Boredom Ban — prompts and module structures cannot be reused identically across webinars.
- FR17c: The system generates branded, coach-ready **`.excalidraw` files** as the unified visual delivery format — for webinars, tierlists, ratings, and reaction explainers. The hand-drawn Excalidraw aesthetic feels natively coach-made (not corporate PowerPoint). Coaches open the file and hit record.
- FR18: The system can dynamically adjust webinar module selection based on real-time aggregate audience sentiment and Context Premises.
- FR19: The system uses a **unified Excalidraw pipeline** for all visual long-form content — Tierlists, Ratings, Webinar slides, and Reaction Explainers (8-10 minute videos where the coach comments live over the visuals). Same branded templates, same rendering process, same agent.
- FR19a: The system uses a **Transparent Collage Pipeline** for emotionally-aware stick figure illustrations — adapted from the proven GMG Expert 03 (Emotional Animator) skill. The pipeline: (1) The Visual Reasoning Protocol reads the script quote, identifies the emotion, selects the pose and photo cutout object. (2) The T2I prompt generates the stick figure + real-object collage on a **pure white background (#FFFFFF)**. (3) Grant runs **alpha extraction** (background removal) to produce a transparent PNG. (4) The transparent PNG is injected as an `image` node into the `.excalidraw` JSON, floating natively on the canvas. This preserves infinite emotional context-awareness while solving scene integration — no static library, no ugly rectangular backgrounds.
- FR20: The system uses **images over videos** for all reaction-style content. Images are easier to source, classify, and maintain the coach's attention flow. No external video content is embedded — the coach IS the video, reacting to curated visual frames.

### Cross-System Intelligence & Memory

- FR21: The system can map and store individual end user Context Premises as an interconnected graph structure (Neo4j).
- FR22: The system can route aggregate end user interaction data (from CBCS) to inform the next cycle of content strategy (CCF).
- FR23: The system can route content engagement performance (from social platforms) to personalize coaching interactions.
- FR24: Each coach ecosystem designates one representative agent that participates in the **Monthly Cross-Ecosystem Meeting**. This meeting shares what is working and what is not across all 24 coach ecosystems. First meeting scheduled: April 1, 2026.
- FR24a: Within each coach ecosystem, the system can autonomously promote recognized psychological patterns from Working → Episodic → Semantic memory on a continuous basis.

### System Operator & Governance

- FR25: The System Operator can continuously view Receipt Chain logs charting every agent interaction, API call, and validation decision.
- FR26: The System Operator can trace the exact prompt, context window, and decision tree responsible for any piece of published output.
- FR27: The System Operator can manage the global agent roster, updating prompt strategies, skills, and tools across the ecosystem.
- FR28: The System Operator can review and explicitly approve or reject automated Semantic memory promotions.
- FR29: The System Operator (via Pi Coding Agent) can spin up, securely isolate, and manage new single-tenant cloud instances for onboarding new coaches.

### Notion Delivery Layer & Asset Tracking

- FR30: The system autonomously delivers all validated content (scripts, visuals, posting notes, voice clips, Leadership Farming notes) to the coach's Notion workspace via `notion_sync.py`, with zero manual intervention after pipeline completion.
- FR30a: Each content page delivered to Notion includes 7 structured sections: Coach Voice Note (audio block), Why This Post (origin trace), Leadership Farming (trait development), Script, Coach Photo (real, from Branding Deck), Visual Assets (AI-generated client scenarios), and Posting Notes.
- FR31: Every artifact produced by the CCP carries a Universal Asset ID (`AAAA-CCC-MM-YY-XXXX`) — 34 asset type codes spanning CCF, V²WS, Tierlist, CBCS, coach identity, and governance. IDs are unique, human-readable, and traceable across Notion, Supabase, Receipt Chain, and file storage.
- FR31a: Every person in the CCP carries a Person ID (`CCC-NNNN`) — coach = `CCC-0000`, clients numbered sequentially. Person IDs are assigned during Genesis (coach) or CBCS onboarding (client) and stored in `coach_registry.json`.
- FR32: The coach's Notion workspace applies conditional color rules (overdue alerts, client engagement heat, sentiment flags, seasonal alignment, photo freshness) and smart formulas (countdown pulse, progress bars, engagement heat, resonance hits) to surface intelligence visually without charts or external tools.
- FR32a: Content pages use tabbed layouts (Script/Visuals/Metrics) and client pages use tabbed layouts (Profile/Sessions/Voice Journal) to provide multiple perspectives without scrolling.
- FR33: Coaches can upload real photographs to a Personal Branding Photo Deck database in Notion, tagged by mood, setting, and format. The system uses these photos for quote cards and carousel covers. The Sovereign Image Rule prohibits AI-generated imagery of the coach — AI images represent client scenarios only.
- FR34: When a coach changes a content piece's Status from Draft to Approved in Notion, a webhook automation triggers the distribution pipeline. No external app or manual publish step is required.

---

## Non-Functional Requirements

### Performance

| Context | Requirement | Metric |
|---|---|---|
| CBCS message response | End-to-end latency from webhook receive to Telegram delivery | **<2 seconds** (P95) |
| Aria entity extraction | Context Premise update after voice note processing | **<5 seconds** including Groq transcription |
| CCF batch pipeline | Full `ccf-weekly` execution (research → generation → validation → approval queue) | **Tolerates 10-30 minutes** per batch — no user is waiting |
| V²WS Excalidraw generation | Excalidraw Composer generates branded `.excalidraw` slide deck per webinar | **<5 minutes** per complete deck |
| ModelRouter decision | Model selection and routing per request | **<100ms** overhead |
| Memory query | Neo4j Context Premise graph read for personalization | **<500ms** per query |

### Security & Data Privacy

- **Voice Recording Encryption:** All Sacred Audio files and client voice notes are encrypted at rest (AES-256) and in transit (TLS 1.3). Voice data is the most sensitive asset — it contains raw emotional vulnerability.
- **Context Premise Isolation:** Each coach's Neo4j graph is fully isolated. There is zero shared infrastructure between coach instances. A breach in one coach's environment cannot expose another coach's client data.
- **Coach IP Protection:** `coach_soul.json` and all TTT calibration data constitute the coach's intellectual property. If a coach leaves the platform, their Voice DNA profile and all derived content models are purged from the system within 30 days.
- **Client Data Retention:** End user journal entries, voice transcriptions, and ritual interaction logs are retained only for the duration of the coaching engagement + 90 days. Clients can request deletion at any time.
- **Agent Prompt Security:** System prompts, SKILL.md files, and the Intelligence Library are never exposed to end users. The CBCS presents as a natural coaching conversation — internal architecture is invisible.

### Reliability & Governance

- **Receipt Chain Integrity:** The Receipt Chain Guard maintains a 100% unbroken audit trail for every pipeline execution. If a chain link breaks (validation failure, API timeout), the entire batch is quarantined — never partially published.
- **Circuit Breaker Latency:** Crisis detection fires within **<500ms** of keyword detection. This is a hard-coded, non-negotiable priority — no LLM reasoning delay is acceptable for safety escalation.
- **Zero Silent Failures:** If an agent fails (LLM timeout, malformed output, validation rejection), the system logs the failure with full context AND notifies the System Operator. No failure is silently swallowed.
- **Backup & Recovery:** Coach ecosystems are backed up daily. Full system recovery from backup must be achievable within **<4 hours**.
- **Uptime Target:** CBCS (real-time coaching) targets **99.5% uptime**. CCF/V²WS (batch processing) can tolerate scheduled maintenance windows.

### Integration Resilience

- **Telegram API:** The primary I/O channel. Must handle rate limits gracefully (Telegram limits: 30 messages/second per bot). Implement exponential backoff and message queuing.
- **Neo4j:** Graph database must support concurrent reads (CBCS querying Context Premise) and writes (Aria updating entities) without deadlocks. Connection pooling required.
- **Social Media APIs:** Publishing integrations (Instagram, Twitter/X, LinkedIn) must handle API deprecation and rate limit changes without breaking the pipeline. Failures queue for retry, never lose content.
- **Excalidraw:** All visual rendering pipelines (Tierlists, Webinars, Ratings, Reactions) must be idempotent — if a render fails, re-running produces identical `.excalidraw` output without side effects. Template integrity validated before delivery.
- **LLM Provider Resilience:** ModelRouter must support failover between LLM providers (e.g., if Groq is down, fall back to an alternative fast-inference provider for Aria extraction).

### Skipped Categories (With Rationale)

- **Accessibility:** Not applicable. All end user interaction is via Telegram (voice notes + text). Telegram itself handles accessibility. No custom UI to make accessible.
- **Scalability:** Not applicable in the traditional sense. Each coach runs an isolated cloud instance. Scaling means spinning up more instances (linear, not exponential). No shared database bottleneck.

---

## Section 1: Mission & Foundational Frameworks

### The CCP Mandate
The Conscious Coaching Platform (CCP) is not a collection of scripts; it is a unified, agentic operating system designed to merge five previously distinct entities:
1. **CCF (Conscious Content Factory):** The content generation engine.
2. **CBCS (Conscious Business Coaching System):** The coaching intelligence and strategy engine.
3. **V²WS (Viral Virtual Webinar System):** The webinar generation and distribution engine.
4. **Unified Excalidraw Visual Engine:** The single visual pipeline for all coach-facing content — Tierlists, Webinar slides, Ratings, and Reaction Explainers. Branded templates with a hand-drawn aesthetic that feels natively coach-made.

The mandate of the CCP is to unify these systems across a shared memory layer so that coaching insights naturally birth webinars, webinars feedback into content, and content data informs coaching strategy. The goal is to build a system that produces output indistinguishable from a master coach working at peak intuition.

### The Cardinal Sin: Sounding AI
*Definition: "Sounding AI" refers to content that is structured predictably, relies on linguistic clichés (e.g., "in a world where," "unlock your potential"), lacks emotional variance, and is devoid of the specific, messy, irreducible uniqueness of human experience.*  
**Why this matters:** The algorithm and the human brain both penalize predictable repetition (boredom) and reward novelty (Curiosity). If the CCP produces output that sounds like an LLM, it fails entirely. The entire architectural stack is designed backward from the singular objective of preventing this cardinal sin.

### Conscious Movement Alchemy
*Definition: A framework of 14 Principles (e.g., The Hero's Journey integration, The Shadow Concept, Emotional Resonance) that govern how narratives are structured to elicit genuine human connection rather than passive consumption.*  
**Why this matters:** We do not treat these 14 Principles as raw instructions to feed into an LLM prompt. Instructions are forgotten context; they lead to average outputs. Instead, these principles are embedded as *Constraints* and *Laws* within the system's governance and execution architecture. They form the biological DNA of the CCP's operation.

### The BMAD Development Framework
*Definition: BMad Method Module (BMM) is the agile, agentic development philosophy we are using to construct the CCP. It relies on specific agent personas (PM, Architect, Scrum Master) to plan (PRD/tech-spec), solution (architecture), and implement (sprint-driven story execution) sequentially.*  
**Why this matters:** A system this complex cannot be built "greenfield" by randomly writing scripts. It requires a surgical Standard Operating Procedure (SOP) where every single file, skill, command, and agent is explicitly audited and given a mandate (CREATE The system is the product of its architecture, not just its prompts.

---

## Section 2: The 7-Layer Unified Architecture

To achieve the CCP Mandate and avoid the Cardinal Sin, the platform operates across a 7-tier biological hierarchy. Data flows upward from the lowest levels (Research) to the highest levels (Intuition), and execution flows horizontally across the subsystems.

```text
7. INTUITION Layer       (Emergent Sparks & Novelty Synthesis)
          ↑
6. GOVERNANCE Layer      (The Laws, Constraints, Draft & Receipt Chains)
          ↑
5. ORCHESTRATION Layer   (The Pi Agent Harness & Extension Teams)
          ↑
4. EXECUTION Layer       (The specialized Agents, Skills, Tools, Libraries, and Prompts)
          ↑
3. DEEP REASONING Layer  (Micro-drafting, MCDA synthesis, Scenario Testing, Collapse Checking)
          ↑
2. MEMORY Layer          (Conscious / Subconscious Graph, Coach Sacred Audio, and the Neo4j Hypergraph Memory)
          ↑
1. DEEP RESEARCH Layer   (Signal Ingestion, Real Time Tribe Relevance, Audience Truths, Vibe comments, Market Reality, Trends, and realtime Radar Sweeps)
```

### Layer 1: Relevant Deep Research (The Signal Ground)
*Definition: The programmatic and agentic collection of raw, verified market data, target audience truths, competitor positioning, and trend signals. This relies heavily on **Real Time Tribe Relevance**—a triangulated metric combining Coach Inputs + Audience Inputs + Fresh Research.*  
**Why this matters:** As identified in the MCDA Content Resonance Principles, *first-party data > third-party noise*. We cannot build intuition on top of LLM hallucinations. The Distillation Laws must be applied *during* research, not just during content creation. This layer is the foundation; it generates the raw materials that ensure the system is rooted in reality.  
**Components:** Firecrawl radar sweeps, Google Trends wrappers, Telegram vibe ingestion, raw audience interviews, and raw audience feedback.

### Layer 2: Memory (The Subconscious & Conscious Data)
*Definition: A hybrid storage system leveraging dual technologies: Supabase for blob/flat storage (drafts, outputs) and a Neo4j Hypergraph Memory (HGM) for relational, semantic understanding between concepts.*  
**Why this matters:** A unified system requires shared context. If a coach mentions a breakthrough in a voice note, the webinar system needs to inherently "know" it.  
**Strict Rule:** *Sacred Coach Voice Audio* acts as the primary episodic memory. It is ingested purely and is *never folded or compressed* to save context limits, preserving the coach's irreducible uniqueness.

### Layer 3: Deep Reasoning (The Testing Ground)
*Definition: The layer where the system pauses raw execution to synthesize and test hypotheses. Crucially, **MCDA (Multi-Criteria Decision Analysis) must be performed here before any Receipts are written or artifacts are finalized**.*  
**Why this matters:** The difference between a script and an intelligent agent is the ability to reason. By forcing the system to step back, run an MCDA to weigh trade-offs, test its own logic, and verify its assumptions (e.g., the H1 Collapse Test) *before* it generates the final output, we guarantee depth and eliminate shallow, reactive generation.

### Layer 4: Execution (The Specialized Workforce)
*Definition: The atomic units of work that actually execute the logic. This layer requires strict definitions for its components:*
- **Agents:** The primary personas executing a workflow (e.g., PM, Architect).
- **Sub-agents:** Specialized, temporary personas invoked during the adaptation stage for highly specific tasks. *Crucial function: Sub-agents are explicitly responsible for rewriting, auditing, and adapting executive prompts dynamically.* Multiple sub-agents will be defined in this PRD.
- **Example Sub-agent (The Insider):** A specialized audience-representative agent. She is not a domain expert, but she is highly self-conscious and possesses the closest access to real-time audience data and vibe comments. Her singular job is the **"Vibe Pass"**—killing anything awkward, generic, or "AI cringe" before it proceeds.
- **Skills:** True reasoning workflows that require non-deterministic thinking.
- **Tools:** Disguised Python functions doing deterministic, procedural work (e.g., API calls, DB writes).
- **Libraries & Configs:** The YAML/JSON files that store the intelligence matrices.
- **Executive Prompts:** The final compiled instructions sent to the LLM context window.

**Why this matters:** Monolithic prompts cause "Brevity Bias" and context collapse. By atomizing the workforce into specific skills, tools, sub-agents, and tight prompts, we protect the context window and ensure agents stay focused on one specific job.  
**Baseline Components:** The current state includes 12 CBCS expert agents and 72 CCF skills/tools. *However*, this PRD will explicitly define the net-new Agents, Skills, Tools, and Extensions required to fully execute CCF, V²WS, and the Tierlist generator.

### Layer 5: Orchestration (The Harness)
*Definition: The TypeScript-based Pi Coding Agent framework that manages the execution layer. It orchestrates "Agent Teams" (parallel execution) and "Agent Chains" (sequential execution).*  
**Why this matters:** Rigid Python CLI runners break when a step fails. The Pi harness provides dynamic, self-correcting pathways. Instead of "run script 1, then script 2," it uses extensions like `TillDone` and `DamageControl` to navigate complexity and recover from errors gracefully.

### Layer 6: Governance (The Law)
*Definition: The deterministic, unforgiving rules that govern the entire system. This includes the YAML Constitution (recruitment rules), the Receipt Chain Guard (dependency verification), the Credit System (self-esteem ledger), and the Boredom Ban.*  
**Why this matters:** *Constraints > Instructions.* If you tell an LLM "don't be boring," it will fail. If you build a Governance layer that literally halts the pipeline if a "Staleness Flag" is detected or a dependency receipt is missing, you mathematically eliminate the possibility of generic output.

### Layer 7: Intuition (The Emergent Spark)
*Definition: Four specific capabilities—SoulResonance, PatternWeaver, GhostContext, and AncestralWisdom—that synthesize disparate data points to create genuine surprise or revelation. These extensions require their own dedicated under-the-hood **skills, tools, and sub-agents** to process the intuition spark into tangible outputs.*  
**Why this matters:** Intuition cannot be forced; it is the consequence of the lower six layers operating flawlessly. These extensions are only triggered contextually (e.g., when the Governance layer detects an Information Gap is closing, or a story is stale). This layer is responsible for breaking autopilot and ensuring the content consistently violates expectations in a profound way.

---

## Section 3: Source Inventory (The Baseline)

Before surgical modifications can be made in the subsequent sections, we must establish the exact baseline of the existing infrastructure. This inventory details what currently exists in the `d:\Work\The Conscious Coaching Factory` repository.

### 3.1 The CCF Execution Inventory
The legacy Content Factory is the most populated module, currently operating via Python-based CLI runners.

**Skill Families (10 directories, 72 total skills):**
- `content` (7 skills)
- `distillation` (6 skills, including the new Tribe Distiller)
- `distribution` (17 skills)
- `eroll` (15 skills)
- `orchestration` (4 skills)
- `production` (4 skills)
- `research` (93 files - Note: some are data vs skills)
- `setup` (6 skills)
- `validation` (4 skills)
- `visual-recipes` (14 skills)

**Procedural Tools (Python Scripts):**
- `firecrawl_wrapper.py` (Web scraping / Radar)
- `google_trends_wrapper.py` (Search velocity)
- `sentiment_wrapper.py` (Basic NLP)
- `transcribe_voice.py` (Local Whisper ingestion)

**Tool Applications:**
- `tierlist-app/` (React/Excalidraw foundation)
- `telegram-tierlist-bot/` (Ingestion endpoint)

**Commands / Pipelines (28 Scripts):**
Includes `ccf-research-deep.md`, `ccf-raw-research.md`, `ccf-blueprint.md`, `ccf-soc.md`, `ccf-visual.md`, `ccf-wisdom.md`, `ccf-generate.md`, etc.

### 3.2 The CBCS Agent Inventory
The Coaching System currently defines 12 expert agent personas across 5 departments. Note: Some of these agent concepts overlap with CCF orchestration concepts and will be resolved in Section 5.
1. Perception Dept: *The Radar, The Truth Seeker, The Data Miner*
2. Strategy Dept: *The Blueprint, The Mastermind, The Optimizer*
3. Expression Dept: *The Storyteller, The Voice, The Visual Director*
4. Validation Dept: *The Critic, The Fact Checker, The Alignment Guard*

### 3.3 The V²WS Inventory
Currently, the Viral Virtual Webinar System exists **purely as conceptual documentation** (31 architectural docs). 
- **Current State:** Zero execution code. Zero designated agents.
- **Action Required:** The PRD must write explicit mandates to CREATE the pipeline, tools, sub-agents, and skills required to bring V²WS into the Execution Layer, powered by the PPTX-native WebinarComposer.

### 3.4 Governance & Prompts
- **Archetype Prompts:** 92 raw prompts stored in `intelligence/`.
- **Implementation Laws:** 15 Hyper-Docs (`H0` to `H15`) defining the Distillation Laws.
- **Receipt Chain Guard:** `receipt_chain_guard.md` (Dual-enforcement map).
- **Draft Protocol:** `draft_protocol.md` (3-phase micro-test rules).

*(This baseline serves as the "Before" state. Sections 4-8 will define the specific CREATE, EDIT, KEEP, and MERGE operations for every component to build the Unified CCP.)*

---

## Section 4: The Pi Extension Stack (The Orchestrators)

To move away from brittle Python CLI runners, the CCP relies on the Pi Coding Agent (TypeScript) as its primary execution harness. The logic inside Pi is governed by *Extensions*—plugins that override default LLM behaviors and inject structural determinism (Operational Extensions) or emergent synthesis (Intuition Extensions).

Below is the definitive mandate for the 11 required extensions.

### 4.1 The 7 Operational Extensions
These extensions manage control flow, memory, and error recovery.

#### 1. `InteractComp` (The Ambiguity Gate)
- **Status:** `[CREATE]`
- **Replaces:** Blind execution of `ccf-generate.md` prompts.
- **Hook Point:** `pre_flight` (before any chain or team starts).
- **Exact Behavior:** Scans the incoming coach request and parameters against the Required Inputs Schema. If data is missing (e.g., Target Audience missing, Archetype blank), it *halts* and prompts the Coach for clarification via the CLI/UI. It refuses to let the agent guess critical missing context.
- **Data Dependencies:** Reads from `Layer 1 (Deep Research)` to check if gaps can be filled autonomously before bothering the coach.

#### 2. `MemoryFolder` (The Graph Writer)
- **Status:** `[CREATE]`
- **Replaces:** Static file saving in `.ccf_outputs/`.
- **Hook Point:** `post_task` (after any approved execution).
- **Exact Behavior:** Takes the output generated in Working Memory (Layers 3 & 4) and writes it to Layer 2 (Neo4j HGM & Supabase). It identifies keywords, audience triggers, and story elements, mapping them as relational edges (e.g., `(Story)-[:RESONATES_WITH]->(Archetype)`).
- **Data Dependencies:** Writes exclusively to `Layer 2 (Memory)`.

#### 3. `DamageControl` (The Self-Correction Loop)
- **Status:** `[CREATE]`
- **Replaces:** Pipeline crash when a script fails.
- **Hook Point:** `on_receipt_fail` or `on_exception`.
- **Exact Behavior:** When a Governance receipt (e.g., Code format, formatting constraint) fails, or a Python tool throws an error, Pi catches it. `DamageControl` isolates the error, feeds the traceback to the specific agent, and instructs a single retry focusing *only* on the failure. 
- **Touches Components:** Integrates with the `receipt_chain_guard.md`.

#### 4. `ModelRouter` (The Optimizer)
- **Status:** `[CREATE]`
- **Replaces:** Hardcoded model selection in Python scripts.
- **Hook Point:** `pre_task`.
- **Exact Behavior:** Dynamically selects the Gemini model based on task type via the Gemini subscription integrated with Pi:
  - **Gemini 3.1 Pro High** → Deep Reasoning tasks (MCDA synthesis, Collapse Tests, Draft Protocol evaluations)
  - **Gemini 3.1 Pro Low** → Thinking tasks (Blueprint generation, Script Composition, Strategy drafting)
  - **Gemini 3 Flash** → Fast procedural tasks (formatting, schema validation, receipt checks)
- **Touches Components:** Integrates with all CCF skills, CBCS agents, and future V²WS agents.

#### 5. `TillDone` (The Assurance Engine)
- **Status:** `[CREATE]`
- **Replaces:** Premature stopping of agents before complex tasks finish.
- **Hook Point:** `step_loop`.
- **Exact Behavior:** Enforces deterministic completion. It overrides the LLM's natural tendency to summarize or stop early by appending `CONTINUE` and tracking checklist completion until the exact schema requirements are met fully.

#### 6. `TeamOrchestrator` (The Parallel Manager)
- **Status:** `[CREATE]`
- **Replaces:** Linear, sequential execution scripts (e.g., `ccf-research-deep.md`).
- **Hook Point:** `on_workflow_start`.
- **Exact Behavior:** When a task involves debate or gathering multiple perspectives (e.g., generating Tierlist criteria), it spawns multiple agents simultaneously to run in parallel, then uses the *Architect* agent to synthesize the results.

#### 7. `SystemSelect` (The Persona Swapper)
- **Status:** `[CREATE]`
- **Replaces:** Injecting massive persona descriptions into every prompt.
- **Hook Point:** `on_agent_switch`.
- **Exact Behavior:** Dynamically swaps system prompts based on the required Department and Role defined in the YAML Constitution, loading only the necessary constraints for that specific step.

### 4.2 The 4 Intuition Extensions (The Emergent Sparks)
These extensions are not hardcoded into daily workflows. They monitor system state and fire automatically when the Governance Layer (Layer 6) detects staleness, monotony, or a lack of dimensional contrast.

*Critically, each Intuition Extension requires its own dedicated infrastructure to function:*
- **A Sub-agent:** The specialized persona that executes the intuition spark and rewrites the Executive Prompt.
- **A Skill (SKILL.md):** The reasoning workflow the sub-agent follows.
- **A Tool (Python):** The data retrieval or graph query function the sub-agent calls.

#### 8. `SoulResonance`
- **Status:** `[CREATE]`
- **Trigger Conditions:** The Boredom Ban detects emotional flatness, or the T/V/R ratio is unbalanced.
- **Dedicated Infrastructure:**
  - Sub-agent: `[CREATE]` **The Resonance Seeker** — mines emotional charge from Sacred Audio and audience data.
  - Skill: `[CREATE]` `skills/ccf/intuition/soul-resonance/SKILL.md`
  - Tool: `[CREATE]` `tools/soul_resonance_query.py` (Neo4j query for emotionally-tagged nodes)
- **Behaviors:**
  1. **Vibe Pass Rewrite:** Triggers The Insider to run an MCDA Vibe Pass, forcing a rewrite of the executive prompt to demand a visceral, emotionally contrasting analogy pulled from the coach's Sacred Audio (Layer 2).
  2. **Emotional Polarity Injection:** When content is stuck in one emotional register (e.g., all motivational, all analytical), injects the opposite pole — vulnerability into strength pieces, dark humor into serious pieces — to create dimensional contrast.
  3. **Tribe Mirror Check:** Cross-references the emotional language of the output against the Real Time Tribe Relevance data to verify the emotional register actually matches how the target audience *speaks and feels*, not how the coach assumes they do.
  4. **Sacred Moment Surfacing:** Scans the coach's voice note archive for raw, unscripted emotional moments (pauses, laughter, frustration) and injects those specific moments as narrative anchors, ensuring the content carries the coach's *actual* energy, not a sanitized version.

#### 9. `PatternWeaver`
- **Status:** `[CREATE]`
- **Trigger Conditions:** Staleness Flags indicate stories/metaphors reused 3+ times, or the Information Gap in the draft is closing (predictable conclusion).
- **Dedicated Infrastructure:**
  - Sub-agent: `[CREATE]` **The Connector** — finds unexpected links between disconnected graph nodes.
  - Skill: `[CREATE]` `skills/ccf/intuition/pattern-weaver/SKILL.md`
  - Tool: `[CREATE]` `tools/graph_disconnect_query.py` (Neo4j shortest-path-between-unrelated-nodes)
- **Behaviors:**
  1. **Cross-Domain Synthesis:** Searches the Neo4j Graph for completely disconnected nodes (e.g., a jazz improvisation concept and a sales funnel metric) and forces the Execution Layer to synthesize a novel, unexpected connection that the audience has never encountered.
  2. **Temporal Pattern Detection:** Scans coach data across different time periods (early career vs. now) to identify how the coach's own thinking has evolved on a topic, creating a "then vs. now" narrative tension that feels authentic.
  3. **Contradiction Mining:** Finds paradoxes within the coach's own philosophy (e.g., "I believe in patience" but "I also believe in urgency") and surfaces them as powerful content angles — the honest contradiction is more compelling than a polished consistent message.
  4. **Adjacent Industry Transplant:** Pulls proven frameworks from industries completely outside the coach's domain (e.g., applying restaurant kitchen brigade systems to team management) and forces the content to make the case for why this foreign framework applies.

#### 10. `GhostContext`
- **Status:** `[CREATE]`
- **Trigger Conditions:** The Draft Protocol detects an absence of the Shadow Concept, or the content reads as purely positive/aspirational without acknowledging structural limitations.
- **Dedicated Infrastructure:**
  - Sub-agent: `[CREATE]` **The Shadow Miner** — specializes in finding what's unsaid, feared, or deliberately avoided.
  - Skill: `[CREATE]` `skills/ccf/intuition/ghost-context/SKILL.md`
  - Tool: `[CREATE]` `tools/ghost_context_scan.py` (Scans historical outputs + audience complaints for recurring blind spots)
- **Behaviors:**
  1. **Industry Dark Truth Injection:** Injects the uncomfortable, unsaid realities of the coach's industry into the context window, forcing the agent to address the elephant in the room instead of writing a "safe" aspirational post.
  2. **Audience Fear Mapping:** Pulls from vibe comments and audience feedback to surface what the target audience is *afraid to admit* — the real objection they have but won't say out loud — and forces the content to name it directly.
  3. **Historical Failure Pattern:** Retrieves past failures, rejected drafts, or strategies that didn't work from the Memory Layer and uses them as cautionary context, preventing the agent from repeating patterns that have already proven ineffective.
  4. **Counter-Narrative Generation:** Identifies what the mainstream consensus says about a topic, then forces the agent to articulate why the coach's data or experience *disproves* the mainstream — creating genuine thought leadership rather than echo-chamber content.

#### 11. `AncestralWisdom`
- **Status:** `[CREATE]`
- **Trigger Conditions:** The Coach Echo Test fails (agent parrots coach phrasing without adding strategic value), or the content lacks first-principles grounding.
- **Dedicated Infrastructure:**
  - Sub-agent: `[CREATE]` **The Philosopher** — re-frames messages through foundational frameworks and timeless principles.
  - Skill: `[CREATE]` `skills/ccf/intuition/ancestral-wisdom/SKILL.md`
  - Tool: `[CREATE]` `tools/framework_cross_reference.py` (Maps coach statements against CMA principles, MCDA matrices, and philosophical frameworks)
- **Behaviors:**
  1. **CMA Framework Re-framing:** Cross-references the coach's raw input with the 14 Principles of Conscious Movement Alchemy and the 7 Content Resonance Principles, demanding a profound re-framing that elevates the message from "advice" to "principle."
  2. **First Principles Decomposition:** Takes the coach's surface-level message and strips it down to its irreducible truth — the atomic claim that cannot be further reduced — then rebuilds the content upward from that foundation, ensuring depth.
  3. **Philosophical Lens Rotation:** Views the same coach message through 3 different philosophical lenses (e.g., Stoic discipline, Eastern non-attachment, Behavioral Economics) and selects the lens that creates the most surprising resonance with the target audience's worldview.
  4. **Legacy Pattern Recognition:** Connects the coach's current insight to historical or timeless wisdom patterns (e.g., "What you're describing is what Sun Tzu called..." or "This maps to the Pareto principle because..."), giving the content gravitas and intellectual depth that transcends trend cycles.

---

## Section 5: Unified Agent Roster & Architecture

This section defines the complete agent manifest for the CCP. Every agent — existing, new, merged, or renamed — is listed with its mandate, department, memory access, and the Pi extension that orchestrates it. The roster is organized by Department, not by subsystem, because the CCP is ONE system.

### 5.1 CBCS Agents (Existing — 12 Agents, 6 Departments)

These agents currently exist as Python classes (`pydantic_ai.Agent`) with dedicated `_SKILL.md` protocols in `CBCS/backend/intelligence_library/protocols/`. Their current model (`GroqModel llama-3.3-70b-versatile`) will be replaced by `ModelRouter` (Gemini models).

#### Perception Department
| Agent | Code Name | File | SKILL.md | Mandate | CCP Role (Actual from SKILL.md) |
|---|---|---|---|---|---|
| **Aria** | The Synthesizer | `perception/aria.py` | `aria_SKILL.md` | `[EDIT]` | **Context Premise Extractor.** First-pass analysis of raw user text (assessments, journals, voice transcriptions). Extracts 12 dimensions: Enemy, Dream, Fear, Identity, Coach Reference, Ritual Affinity, Capacity Score, TTT State, Identity Pillar, Emotional Trigger, Resistance Pattern, Milestone Proximity. Outputs structured `ContextExtraction` JSON with Neo4j relationship types (`FIGHTS_AGAINST`, `CRAVES`, `FEARS`, `HAS_IDENTITY`). 5 Quality Gates (min entity count, PII redaction, TTT required, evidence grounding, no hallucinated entities). |
| **Remgion** | The Researcher | `perception/remgion.py` | `remgion_SKILL.md` | `[RENAME + EDIT]` | *(Renamed from Lionel to avoid conflict with CCF's Lionel — Research Library Architect.)* **First Principles Research & Fact Provider.** RAG agent querying Supabase vector store. Separates knowledge into Deep (timeless, 10+ year shelf life) and Fresh (cultural, 6-12 months). Every claim must be cited. Conflict resolution: Deep > Fresh. Outputs `ResearchPackage` JSON with citations, data points, and first-principles backing. |
| **Tshala** | The Sentinel | `perception/tshala.py` | `tshala_SKILL.md` | `[RENAME + EDIT]` | *(Renamed from Maeva to avoid conflict with CCF's Maeva — Theme Social Researcher.)* **External Sentiment & Trend Scanner.** Uses Tavily API to scan social media, forums, news for topics the tribe cares about. Weekly Monday scans. Constructs queries from `tribe_soul.json` keywords. Scores sentiment (-1 to +1), identifies trends by frequency × intensity, detects Cultural Moment opportunities (HOT/WARM/COLD urgency). Outputs `SentimentReport` JSON. |

#### Strategy Department
| Agent | Code Name | File | SKILL.md | Mandate | CCP Role (Actual from SKILL.md) |
|---|---|---|---|---|---|
| **Tshilanda** | The Configurator | `setup/tshilanda.py` | `tshilanda_SKILL.md` | `[RENAME + EDIT]` | *(Renamed from Kimya to avoid conflict with CCF's Kimya — Business Analyst.)* **Coach Onboarding & Pantry Configuration.** Analyzes coach's business model (revenue model, price points, client journey), maps high-ticket offers to Success Markers, personalizes the ritual library, configures Voice DNA (from Job), sets Pantry Logic Rules (escalation paths, notification thresholds, content format preferences). Outputs `PantryConfig` JSON. Activated on new coach registration or quarterly review. |
| **Atlas** | The Strategic Planner | `strategy/atlas.py` | `atlas_SKILL.md` | `[EDIT]` | **30-Day Ritual Roadmap Architect.** Takes Aria's `ContextExtraction` + user profile + ritual library. Classifies user into Capacity Tracks (Recovery/Foundation/Growth/Momentum/Peak). Builds 4-week framework with 4+1+2 structure (4 active, 1 reflection, 2 rest). Progressive intensity (+10%/week). Milestone checkpoints at Day 7/14/21/28. Anti-patterns enforced (never escalate Recovery in first 14 days). |
| **Assembler** | The Ritual Strategist | `strategy/assembler.py` | `assembler_SKILL.md` | `[KEEP]` | **Ritual Selection & Assembly.** Takes Aria's entities + available rituals + user profile. Performs weighted scoring to surgically match the user's internal state to the right ritual. "The wrong ritual at the wrong time is worse than none." Outputs `RitualSelection` with scoring rationale, persuasion layer, and assembly instructions. *(Note: Name "Assembler" is accurate — it assembles the ritual strategy, not content. No rename needed.)* |

#### Expression Department
| Agent | Code Name | File | SKILL.md | Mandate | CCP Role (Actual from SKILL.md) |
|---|---|---|---|---|---|
| **Artisan** | The Master Copywriter | `expression/artisan.py` | `artisan_SKILL.md` | `[EDIT]` | **Personalized Script Generation Engine.** Transforms generic ritual scripts into deeply personal, spoken-word-ready scripts. Uses the 6-Beat Conscious Arc (Hook → Pain Mirror → Reframe → Ritual Intro → Action Call → Close). Calibrates per Identity Pillar (Challenger/Nurturer/Maker/Explorer/Rebel) × TTT state. Integrates Remgion's facts and Tshala's sentiment. 13-point quality rubric (entity grounding, TTT compliance, banned phrases, authenticity score ≥7/10). 50 unique tone presets (5 Identity × 10 TTT). |
| **Voice Agent** | The Audio Director | `expression/voice_agent.py` | `voice_agent_SKILL.md` | `[EDIT]` | **Script-to-Audio Conversion Director.** Takes Artisan's script + Job's Voice DNA + TTT state. Maps TTT codes to exact audio parameters (speed 0.80-1.15, pitch, breathiness, stability). Inserts disfluency tokens (`<breath>`, `<pause:short>`, `<emphasis>`, `<slow>`, `<whisper>`) for natural human sound. Per-beat prosody modifiers. Outputs TTS-ready `AudioDirective` JSON. |

#### Management Department
| Agent | Code Name | File | SKILL.md | Mandate | CCP Role (Actual from SKILL.md) |
|---|---|---|---|---|---|
| **Vidye** | The Orchestrator | `management/vidye.py` | `vidye_SKILL.md` | `[RENAME + EDIT]` | *(Renamed from Emilio to avoid conflict with CCF's Emilio — Idea Orchestrator.)* **State Manager & Logic Router.** Air traffic controller — first node in every user interaction graph. Decision tree: checks dormancy (3/5/10/30 day thresholds), routes audio to Aria, pre-scans for crisis (→ Liliane), checks context availability (→ Assembler or Aria). Manages full state machine (ONBOARDING → ACTIVE → AT_RISK → DORMANT → LAPSED → CHURNED). Dormancy recovery templates by status level. |

#### Safety Department
| Agent | Code Name | File | SKILL.md | Mandate | CCP Role (Actual from SKILL.md) |
|---|---|---|---|---|---|
| **Liliane** | The Guardian | `safety/liliane.py` | `liliane_SKILL.md` | `[EDIT]` | **Sentiment Monitor & Crisis Circuit Breaker.** 3-tier risk assessment: Tier 1 pre-scan (<100ms keyword check for suicide/self-harm), Tier 2 sentiment analysis (-1.0 to +1.0 with trend tracking), Tier 3 crisis protocol (acknowledge, no advice, empathy by identity pillar, localized crisis resources, coach Telegram alert, hold state). Key principle: "100 false positives > 1 missed crisis." |

#### Setup Department
| Agent | Code Name | File | SKILL.md | Mandate | CCP Role (Actual from SKILL.md) |
|---|---|---|---|---|---|
| **Job** | The Voice Profiler | `setup/job.py` | `job_SKILL.md` | `[RENAME + EDIT]` | *(Renamed from Valeriane to avoid conflict with CCF's Valeriane — Client Soul Extractor.)* **Voice DNA & Coach Soul Builder.** Analyzes coach's raw content across 7 layers: Metaphor Catalogue, Sentence Architecture, Emotional Vocabulary, Profanity Profile, Cultural References, Signature Expressions (≥3 occurrences), TTT Baseline Calculation. Outputs `coach_soul.json` (renamed from `client_soul.json`) — the coach's linguistic fingerprint. Min 10 content pieces or 5,000 words. |
| **Beleshay** | The Cultural Anthropologist | `setup/beleshay.py` | `beleshay_SKILL.md` | `[RENAME + EDIT]` | *(Renamed from Dilaya to avoid conflict with CCF's Dilaya — Tribe Soul Extractor.)* **Tribe Soul Builder.** Analyzes community interactions across 8 cultural layers: Tribal Language (slang), Shared Enemies, Cultural Heroes, Tribal Rituals, Identity Markers, Collective Pain Points, Aspiration Signals, Communication Style. Outputs `tribe_soul.json` — the tribe's cultural DNA. Evidence-grounded (≥3 citations per finding). Monthly refresh + triggered by Tshala shift detection. |

### 5.2 CCF Agents (Existing — 26+ Agents, 5 Groups)

These agents exist as markdown persona files in the CCF ecosystem (see Master Manual Section 7). They load `config.yaml` at activation + a dedicated protocol `.md` file. In the CCP, they will be re-implemented as Pi-harness-compatible agents orchestrated by extensions.

#### Group I: Master Orchestrators (3)
| Agent | CCF Code Name | Role | File | Protocol | Mandate |
|---|---|---|---|---|---|
| **Morgan** | Setup Orchestrator | The Architect of First Impressions | `_master/setup_orchestrator.md` | `setup_orchestrator_protocol.md` | `[EDIT]` | Executes the 7-phase setup workflow. Coordinates Kimya → Dr. Lisa → Emmanuel → Valeriane/Dilaya → Barbara → Lionel → David sequentially. |
| **Alex** | Content Orchestrator | The Weekly Production Director | `_master/content_orchestrator.md` | `content_orchestrator_protocol.md` | `[EDIT]` | Executes the 10-phase production workflow. Coordinates Divine → Maeva/Lila → Emilio → Lionel → Emmanuel → Analyst → Artisan → Visual Trinity → Validators. |
| **Phoenix** | Regeneration Orchestrator | The Iteration Master | `_master/regeneration_orchestrator.md` | `regeneration_orchestrator_protocol.md` | `[EDIT]` | Manages the Script Improvement Lifecycle: Mode A (Regenerate), Mode B (Improve), Mode C (Modify). Generates Improvement Notes and feeds learning system. |

#### Group II: Setup Intelligence Team (8)
| Agent | Role | Phase | Mandate | Key Output |
|---|---|---|---|---|
| **Kimya** | Business Analyst (Economic Architect) | Phase 0 | `[KEEP]` | `01_business_canvas.md` — Economic Engine, Unique Mechanism, Transformation Map |
| **Dr. Lisa** | Witness Blueprint Architect (Transformation Cartographer) | Phase 0.5 | `[KEEP]` | `_witness_blueprint.json` + `_interview_protocol.md` |
| **Emmanuel** | Strategy Architect (Trust Engineer) | Phase 1 | `[KEEP]` | `02_content_strategy.md` — 7-11-4 Trust Architecture, Market Sophistication |
| **Valeriane** | Client Soul Extractor (Voice Archaeologist) | Phase 2A | `[KEEP]` | `03_client_soul.json` + `03b_ttt_baseline.json` — Voice DNA, TTT Baseline |
| **Dilaya** | Tribe Soul Extractor (Digital Ethnographer) | Phase 2B | `[KEEP]` | `04_tribe_soul.json` — Tribal Slang, Enemies, Heroes, Humor Profile |
| **Barbara** | Transformation Observer (Story Archaeologist) | Phase 2C | `[KEEP]` | `TW_XXX_[Name].md` — Measurable proof, emotional arc, soundbite database |
| **Lionel** | Research Library Architect (Timeless Truth Excavator) | Phase 3 | `[KEEP]` | `research_library/*.md` — 7-Angle deep research (30-40 pages per pillar) |
| **David** | Character Strategist (Visual Identity Architect) | Phase 4 | `[KEEP]` | `05_brand_avatar.md` — Visual DNA, avatar semiotics |

#### Group III: Content Intelligence Team (10+)
| Agent | Role | Phase | Mandate | Key Output |
|---|---|---|---|---|
| **Divine** | Theme Discoverer (Cultural Radar) | Phase 5 | `[KEEP]` | `final_selection.md` — 36 themes scored, top 2 selected (1 Connection + 1 Reaction) |
| **Maeva** | Theme Social Researcher (Digital Historian) | Phase 6 | `[KEEP]` | `[theme]_social_research.md` — 30-40 pages of tribal archaeological research |
| **Lila** | Audience Empathy Synthesizer (Psychological Cartographer) | Phase 6.5 | `[KEEP]` | `context_premise_connection.json` + `context_premise_reaction.json` — 6 segments × 12 dimensions |
| **Emilio** | Idea Orchestrator (Viral Alchemist) | Phase 7 | `[KEEP]` | `ideas.json` — 12 viral concepts fused from Context Premise × 22 Viral Frameworks |
| **Emmanuel** | Archetype Mapper (Format Strategist) | Phase 9 | `[KEEP]` | `archetype_assignments.json` — 3 formats per idea (36 total), TTT Palette assigned |
| **Jordan** (The Analyst) | Research Brief Writer (Knowledge Translator) | Phase 10 | `[KEEP]` | `idea_XXX_brief.md` — 1,600-word soul-aligned briefs |
| **Charlotte** (Stream Generator) | Voice Channeler | Phase 11A | `[KEEP]` | `streams/*.md` — 160-240 word raw monologues (voice first, structure second) |
| **Cesare** (Script Artisan) | Structural Editor (Voice-Preserving Architect) | Phase 11B | `[KEEP]` | `scripts/validated/[SCRIPT_ID]/` — 36 scripts sculpted from streams |
| **Julio** (Tweet Factory) | Micro-Content Specialists (3 sub-agents) | Phase 11C | `[KEEP]` | `tweets.json` — 100+ tweets across 3 TTT layers |
| **Adam** (Meme Engine) | Visual Humor Architect | Phase 11D | `[KEEP]` | `memes.json` — 36 meme concepts using formal humor theory |

#### Group IV: Visual Intelligence Team (3)
| Agent | Role | Phase | Mandate | Key Output |
|---|---|---|---|---|
| **Abel** (Visual Recipe Router) | Strategic Director (Traffic Controller) | Phase 11E | `[KEEP]` | Routing decisions — Dual Track / Generative Primary / Asset Primary |
| **Paradoxe** (Visual Prompt Synthesizer) | Semiotic Engineer | Phase 11E Track A | `[KEEP]` | `visual_prompts.json` — Midjourney/DALL-E ready prompts with Facial Expression Lexicon |
| **Aurore** (Visual Asset Researcher) | Evidence Hunter | Phase 11E Track B | `[KEEP]` | `visual_asset_queries.json` — Real-world B-roll, news clips, viral moments |

#### Group V: Validation Team (3)
| Agent | Role | Phase | Mandate |
|---|---|---|---|
| **Sophia** | Soul Validator — TTT Drift Detection | Phase 12 | `[KEEP]` | Validates voice authenticity against `client_soul.json` baseline |
| **Marcus** | Protocol Validator — Structural Compliance | Phase 12 | `[KEEP]` | Validates archetype structure, beat compliance, format rules |
| **Chen** | Mimicry Validator — Human Voice Authenticity | Phase 12 | `[KEEP]` | Detects AI artifacts, template bleed, generic phrasing |

### 5.3 New CCP Agents (To Be Created)

These agents do not yet exist in the codebase. Each requires a Python class, a SKILL.md, and integration with the Pi harness.

#### CCP-Specific New Agents
| Agent | Code Name | Department | Mandate | CCP Role | Memory Access |
|---|---|---|---|---|---|
| **Azaria** (The Memory Curator) | Sunday Archivist | Management | `[CREATE]` | Runs during the Sunday Bot Meeting. Promotes Working Memory edges to Semantic Memory (hyper-edges) based on the 3-week consistency rule. Reads ALL tiers; writes to Semantic. | Full (R/W all tiers) |
| **Sophie** (The Tribe Distiller) | Soul Psychologist | Perception | `[CREATE]` | Builds Soul Tribe Profiles from raw audience research. Applies the 4 Laws of Tribe Profile Distillation. Skill already exists at `skills/ccf/distillation/tribe-distiller/SKILL.md`. | Reads Layer 1; writes Layer 2 |
| **Adele** (The Radar Operator) | Pulse Check | Perception | `[CREATE]` | Runs continuous background radar sweeps (Firecrawl + Google Trends) and flags significant shifts in Real Time Tribe Relevance. Feeds the `InteractComp` extension with freshness data. | Reads/writes Layer 1 |
| **Grâce** (The Draft Tester) | Micro-Lab | Reasoning | `[CREATE]` | Executes the Draft Protocol's 3-phase micro-testing. Receives a micro-draft, runs the Collapse Test, 7-words extraction, and Boredom Ban checks before passing to full generation. | Reads Layer 2/3; writes Layer 3 |

#### V²WS New Agents
| Agent | Code Name | Department | Mandate | CCP Role | Memory Access |
|---|---|---|---|---|---|
| **Alessandro** (The Webinar Architect) | Stage Builder | Strategy | `[CREATE]` | Designs the full webinar structure (hook sequence, transition points, CTA placement) from the coach's content blueprints. Maps to the Excalidraw module-by-module template. | Reads Layer 2/3 |
| **Elene** (The Slide Composer) | Deck Smith | Expression | `[CREATE]` | Generates individual slide content, visual directives, and speaker notes for each webinar segment. Works in parallel via `TeamOrchestrator`. | Reads Layer 3/4 |
| **Benjamin** (The Excalidraw Composer) | Deck Builder | Expression | `[CREATE]` | Orchestrates the unified Excalidraw pipeline — generating branded `.excalidraw` files for all visual content (webinars, tierlists, ratings, reactions) with image assets, stick figure illustrations, and module scripts as text layers. | Reads Layer 4 |

#### Tierlist & Visual Content Agents
| Agent | Code Name | Department | Mandate | CCP Role | Memory Access |
|---|---|---|---|---|---|
| **Gerard** (The Rating Engine) | Tier Judge | Strategy | `[CREATE]` | Generates criteria-based tier rankings for any topic based on coach expertise and audience relevance. Feeds the unified Excalidraw pipeline. | Reads Layer 1/2/3 |
| **Grant** (The Render Controller) | Frame Master | Expression | `[CREATE]` | Manages the unified Excalidraw rendering queue for ALL visual content (tierlists, webinars, ratings, reaction explainers). Handles asset resolution, image sourcing, alpha extraction (background removal) for generated stick figures, and transparent PNG injection into `.excalidraw` JSON. Ensures visual consistency across all outputs. | Reads Layer 4 |

### 5.4 Sub-Agents (Specialized, Temporary Personas)

Sub-agents are invoked dynamically during the adaptation stage. They do NOT run autonomously — they are called by extensions or primary agents when a specific micro-task requires a distinct perspective.

| Sub-Agent | Invoked By | Mandate | Primary Function |
|---|---|---|---|
| **Ketsia** (The Insider) | `SoulResonance`, `TeamOrchestrator` | `[CREATE]` | Audience representative. Runs the Vibe Pass. Kills anything awkward, generic, or AI-cringe. Has closest access to real-time audience data. |
| **Sarah** (The Resonance Seeker) | `SoulResonance` | `[CREATE]` | Mines emotional charge from Sacred Audio and audience data. Rewrites executive prompts for emotional polarity. |
| **Chiara** (The Connector) | `PatternWeaver` | `[CREATE]` | Finds unexpected cross-domain links between disconnected graph nodes. Forces novel synthesis. |
| **Noemie** (The Shadow Miner) | `GhostContext` | `[CREATE]` | Specializes in surfacing what's unsaid, feared, or deliberately avoided. Injects counter-narratives. |
| **Rafael** (The Philosopher) | `AncestralWisdom` | `[CREATE]` | Re-frames messages through foundational frameworks and timeless principles. Applies first-principles decomposition. |
| **Estelle** (The Adaptor) | `SystemSelect`, any chain | `[CREATE]` | Rewrites executive prompts during the adaptation stage of any pipeline. Adjusts tone, depth, and constraints dynamically based on the current MODE (T/V/R). |

### 5.5 Intelligence Library (Existing Configs — EDIT All)

These YAML/JSON files in `CBCS/backend/intelligence_library/` serve as the brain's configuration:

| File | Format | Mandate | CCP Role |
|---|---|---|---|
| `coach_soul.json` | JSON | `[RENAME + EDIT]` | Coach Soul profile schema (renamed from `client_soul.json`). Extend to include Sacred Audio metadata pointers. |
| `tribe_soul.json` | JSON | `[EDIT]` | Tribe Soul profile schema. Extend to include Real Time Tribe Relevance fields. |
| `identity_pillars.yaml` | YAML | `[EDIT]` | Core identity constraints. Integrate with YAML Constitution rules. |
| `persuasion_layers.yaml` | YAML | `[EDIT]` | Persuasion strategy configs. Map to T/V/R mode system. |
| `story_formulas.yaml` | YAML | `[EDIT]` | Story template library. Add `deployment_count` and `staleness_flag` per H10 fix. |
| `ttt_matrix.yaml` | YAML | `[EDIT]` | Text/Tone/Temperature calibration matrix. Connect to `ModelRouter` for dynamic selection. |
| `context_premise_map.json` | JSON | `[EDIT]` | Context-to-premise mapping. Extend for V²WS webinar contexts. |

### 5.6 Naming Conflict Resolution Summary

6 CBCS agents were renamed to eliminate cross-system confusion. CCF agents retain their original Master Manual names.

| Original Name | System | New CBCS Name | Reason |
|---|---|---|---|
| Kimya | CBCS → CCF conflict | **Tshilanda** | CCF Kimya = Business Analyst; CBCS Tshilanda = Pantry Configurator |
| Valeriane | CBCS → CCF conflict | **Job** | CCF Valeriane = Client Soul Extractor; CBCS Job = CBCS Voice Profiler |
| Dilaya | CBCS → CCF conflict | **Beleshay** | CCF Dilaya = Tribe Soul Extractor; CBCS Beleshay = CBCS Tribe Soul Builder |
| Maeva | CBCS → CCF conflict | **Tshala** | CCF Maeva = Theme Social Researcher; CBCS Tshala = Real-time Sentinel |
| Lionel | CBCS → CCF conflict | **Remgion** | CCF Lionel = Research Library Architect; CBCS Remgion = RAG Fact Provider |
| Emilio | CBCS → CCF conflict | **Vidye** | CCF Emilio = Idea Orchestrator; CBCS Vidye = State Manager & Router |

### 5.7 Agent Count Summary

| Category | Existing | New | Total |
|---|---|---|---|
| CBCS Primary Agents | 12 | 0 | 12 |
| CCF Agents (from Master Manual) | 26 | 0 | 26 |
| CCP New Agents | 0 | 4 | 4 |
| V²WS New Agents | 0 | 3 | 3 |
| Tierlist New Agents | 0 | 2 | 2 |
| Sub-Agents | 0 | 6 | 6 |
| **TOTAL** | **38** | **15** | **53** |

---

## Section 6: Skill & Tool Reclassification

This section maps every existing skill and tool in the CCP codebase to the 7-layer architecture, its owning agent, and its mandate. Skills are SKILL.md protocol files that define *what* an agent does. Tools are Python scripts that provide *capabilities* (API wrappers, data processing). In the CCP, every skill must be owned by exactly one agent and mapped to exactly one architectural layer.

### 6.1 CCF Skills (85 SKILL.md Files — 10 Families)

All CCF skills live in `skills/ccf/`. They are the executable instructions that CCF agents load during their activation protocol.

#### 6.1.1 Setup Family (6 Skills) — Layer 2: Memory

These skills run once during client onboarding (`ccf-setup`). They build the permanent intelligence foundation.

| Skill | Path | Owning Agent (CCF) | Layer | Mandate |
|---|---|---|---|---|
| `client-soul-extraction` | `setup/client-soul-extraction/` | Valeriane | Memory | `[EDIT]` — Rename output to `coach_soul.json`. Add Sacred Audio metadata pointers. |
| `tribe-soul-extraction` | `setup/tribe-soul-extraction/` | Dilaya | Memory | `[EDIT]` — Add Real Time Tribe Relevance fields. Connect to Tshala's CBCS `SentimentReport`. |
| `audience-empathy` | `setup/audience-empathy/` | Lila | Memory | `[KEEP]` — 12-dimension Context Premise generation. Already aligned. |
| `philosophy-brief` | `setup/philosophy-brief/` | Emmanuel | Memory | `[KEEP]` — Strategic philosophy extraction for content strategy. |
| `pillar-builder` | `setup/pillar-builder/` | Emmanuel | Memory | `[KEEP]` — Content pillar identification and structuring. |
| `theme-discovery` | `setup/theme-discovery/` | Divine | Memory | `[EDIT]` — Connect to `MemoryFolder` for theme history tracking (novelty scoring). |

#### 6.1.2 Research Family (11 Sub-Families, ~90 Skills) — Layer 1: Relevant Deep Research

The largest family. Contains the intelligence-gathering skills that feed every downstream agent.

| Sub-Family | Path | Count | Owning Agent(s) | Layer | Mandate |
|---|---|---|---|---|---|
| `raw-deep-research` | `research/raw-deep-research/` | 1 | Lionel | Deep Research | `[KEEP]` — 7-Angle Deep Research execution. |
| `raw-fresh-research` | `research/raw-fresh-research/` | 1 | Maeva | Deep Research | `[KEEP]` — Real-time news/trends gathering. |
| `deep-analysts` | `research/deep-analysts/` | ~45 | Lionel → The Analyst | Deep Research | `[KEEP]` — One analyst per archetype×emotion (e.g., `achievement-story`, `fomo-case-study`, `shocking-listicle`). Generates archetype-specific deep research angles. |
| `fresh-analysts` | `research/fresh-analysts/` | ~45 | Maeva → The Analyst | Deep Research | `[KEEP]` — Mirror of deep-analysts but for current/fresh intelligence per archetype. |
| `smart-query-generator` | `research/smart-query-generator/` | 1 | Lionel | Deep Research | `[EDIT]` — Add Tavily API integration. Connect to `InteractComp` for freshness scoring. |
| `strategy-director` | `research/strategy-director/` | 1 | Emmanuel | Deep Research | `[KEEP]` — Research strategy coordination. |
| `vibe-comments` | `research/vibe-comments/` | 1 | Maeva / Lila | Deep Research | `[EDIT]` — Connect to Real Time Tribe Relevance. Feed `MemoryFolder` with audience signal data. |
| `archetype-mapping` | `research/archetype-mapping/` | 1 | Emmanuel | Deep Research | `[KEEP]` — Maps ideas to optimal archetype formats. |
| `blueprint-orchestrator` | `research/blueprint-orchestrator/` | 1 | Alex (Content Orchestrator) | Orchestration | `[EDIT]` — Integrate with `TeamOrchestrator` extension for parallel execution. |
| `critic` | `research/critic/` | 1 | Sophia / Marcus / Chen | Governance | `[EDIT]` — Connect to Receipt Chain Guard. Formalize as validation gate. |
| `visual-asset-curator` | `research/visual-asset-curator/` | 1 | Visual Asset Researcher | Deep Research | `[KEEP]` — Evidence-based visual asset curation. |

#### 6.1.3 Content Family (7 Skills) — Layer 3: Deep Reasoning

Skills for ideation, questioning, and strategic content intelligence.

| Skill | Path | Owning Agent(s) | Layer | Mandate |
|---|---|---|---|---|
| `coach-elicitation` | `content/coach-elicitation/` | Valeriane / Kimya | Reasoning | `[EDIT]` — Connect to Sacred Audio extraction pipeline. |
| `dynamic-theme-generator` | `content/dynamic-theme-generator/` | Divine | Reasoning | `[EDIT]` — Integrate with `MemoryFolder` for 8-week novelty history. |
| `intelligence-radar` | `content/intelligence-radar/` | Maeva / Divine | Reasoning | `[EDIT]` — Feed `InteractComp` extension. Connect to Firecrawl + Google Trends wrappers. |
| `memory-engine` | `content/memory-engine/` | Alex (Orchestrator) | Memory | `[EDIT]` — Migrate to unified `MemoryFolder` extension. Current implementation to be deprecated. |
| `question-engineer` | `content/question-engineer/` | Lila | Reasoning | `[KEEP]` — Generates probing audience questions. Feeds Context Premise. |
| `recording-director` | `content/recording-director/` | Voice Agent (CCF equivalent) | Expression | `[EDIT]` — Connect to TTS pipeline and Sacred Audio system. |
| `script-architect` | `content/script-architect/` | Cesare (Script Artisan) | Reasoning | `[KEEP]` — Master script structure logic. |

#### 6.1.4 Distillation Family (6 Skills) — Layer 3: Deep Reasoning

Skills that apply the 4 Laws of Distillation to transform raw data into structured intelligence.

| Skill | Path | Owning Agent(s) | Layer | Mandate |
|---|---|---|---|---|
| `blueprint-distiller` | `distillation/blueprint-distiller/` | Emmanuel | Reasoning | `[KEEP]` — Distills strategy blueprints from raw analysis. |
| `research-distiller` | `distillation/research-distiller/` | Jordan (The Analyst) | Reasoning | `[KEEP]` — Distills 40-page research into 1,600-word briefs. |
| `question-distiller` | `distillation/question-distiller/` | Lila | Reasoning | `[KEEP]` — Distills audience questions from raw empathy data. |
| `tribe-distiller` | `distillation/tribe-distiller/` | Sophie (The Tribe Distiller) | Memory | `[EDIT]` — Already upgraded with 4 Laws of Tribe Distillation. Connect to `MemoryFolder`. |
| `visual-distiller` | `distillation/visual-distiller/` | Abel (Visual Recipe Router) | Reasoning | `[KEEP]` — Distills visual strategy from script analysis. |
| `voice-distiller` | `distillation/voice-distiller/` | Valeriane | Reasoning | `[EDIT]` — Connect output to `coach_soul.json` (renamed from `client_soul.json`). |

#### 6.1.5 E-Roll Family (14 Skills) — Layer 4: Execution

Archetype-specific production planners. Each E-Roll skill plans the visual/audio roll for one content format.

| Skill | Path | Owning Agent | Layer | Mandate |
|---|---|---|---|---|
| `storytelling-planner` | `eroll/storytelling-planner/` | Script Artisan | Execution | `[KEEP]` |
| `case-study-planner` | `eroll/case-study-planner/` | Script Artisan | Execution | `[KEEP]` |
| `comparison-planner` | `eroll/comparison-planner/` | Script Artisan | Execution | `[KEEP]` |
| `listicle-planner` | `eroll/listicle-planner/` | Script Artisan | Execution | `[KEEP]` |
| `debunking-myths-planner` | `eroll/debunking-myths-planner/` | Script Artisan | Execution | `[KEEP]` |
| `dopamine-cliff-planner` | `eroll/dopamine-cliff-planner/` | Script Artisan | Execution | `[KEEP]` |
| `relief-peak-planner` | `eroll/relief-peak-planner/` | Script Artisan | Execution | `[KEEP]` |
| `observational-humor-planner` | `eroll/observational-humor-planner/` | Adam (Meme Engine) | Execution | `[KEEP]` |
| `archetypical-poll-planner` | `eroll/archetypical-poll-planner/` | Emilio | Execution | `[KEEP]` |
| `stereotypical-poll-planner` | `eroll/stereotypical-poll-planner/` | Emilio | Execution | `[KEEP]` |
| `controversial-dilemma-planner` | `eroll/controversial-dilemma-planner/` | Emilio | Execution | `[KEEP]` |
| `visual-timeline-planner` | `eroll/visual-timeline-planner/` | Paradoxe (Visual Prompt Synthesizer) | Execution | `[KEEP]` |
| `worst-case-planner` | `eroll/worst-case-planner/` | Script Artisan | Execution | `[KEEP]` |
| `conceptual-contrast-planner` | `eroll/conceptual-contrast-planner/` | Script Artisan | Execution | `[KEEP]` |
| `asset-researcher` | `eroll/asset-researcher/` | Aurore (Visual Asset Researcher) | Execution | `[KEEP]` |

#### 6.1.6 Distribution Family (3 Core + 14 Visual Recipes) — Layer 4: Execution / Layer 7: Expression

Skills for final output formatting and visual production.

| Skill | Path | Owning Agent | Layer | Mandate |
|---|---|---|---|---|
| `art-director` | `distribution/art-director/` | Abel (Visual Recipe Router) | Expression | `[EDIT]` — Integrate with H12 Visual Recipe MODE overrides. |
| `orchestrator` | `distribution/orchestrator/` | Alex (Content Orchestrator) | Orchestration | `[EDIT]` — Connect to `TeamOrchestrator` extension for parallel visual generation. |
| `smart-mix` | `distribution/smart-mix/` | Alex | Expression | `[EDIT]` — Integrate with `SystemSelect` for dynamic format selection. |

**Visual Recipes (14 archetype-specific recipes):**

| Recipe | Path | Owning Agent | Layer | Mandate |
|---|---|---|---|---|
| `storytelling-archetypes` | `distribution/visual-recipes/storytelling-archetypes/` | Paradoxe (Visual Prompt Synthesizer) | Expression | `[EDIT]` — Add H12 per-recipe MODE overrides. |
| `case-study` | `distribution/visual-recipes/case-study/` | Paradoxe (Visual Prompt Synthesizer) | Expression | `[EDIT]` — Add proof-evidence emphasis. |
| `comparison-archetypes` | `distribution/visual-recipes/comparison-archetypes/` | Paradoxe (Visual Prompt Synthesizer) | Expression | `[KEEP]` |
| `conceptual-contrast` | `distribution/visual-recipes/conceptual-contrast/` | Paradoxe (Visual Prompt Synthesizer) | Expression | `[KEEP]` |
| `debunking-myths-scams` | `distribution/visual-recipes/debunking-myths-scams/` | Paradoxe (Visual Prompt Synthesizer) | Expression | `[KEEP]` |
| `dopamine-cliff-carousel` | `distribution/visual-recipes/dopamine-cliff-carousel/` | Paradoxe (Visual Prompt Synthesizer) | Expression | `[KEEP]` |
| `listicle` | `distribution/visual-recipes/listicle/` | Paradoxe (Visual Prompt Synthesizer) | Expression | `[KEEP]` |
| `observational-humor` | `distribution/visual-recipes/observational-humor/` | Paradoxe (Visual Prompt Synthesizer) | Expression | `[KEEP]` |
| `relief-peak-carousel` | `distribution/visual-recipes/relief-peak-carousel/` | Paradoxe (Visual Prompt Synthesizer) | Expression | `[KEEP]` |
| `stereotypical-poll` | `distribution/visual-recipes/stereotypical-poll/` | Paradoxe (Visual Prompt Synthesizer) | Expression | `[KEEP]` |
| `the-archetypical-poll` | `distribution/visual-recipes/the-archetypical-poll/` | Paradoxe (Visual Prompt Synthesizer) | Expression | `[KEEP]` |
| `the-controversial-dilemma-poll` | `distribution/visual-recipes/the-controversial-dilemma-poll/` | Paradoxe (Visual Prompt Synthesizer) | Expression | `[KEEP]` |
| `visual-timeline` | `distribution/visual-recipes/visual-timeline/` | Paradoxe (Visual Prompt Synthesizer) | Expression | `[KEEP]` |
| `worst-case-scenario` | `distribution/visual-recipes/worst-case-scenario/` | Paradoxe (Visual Prompt Synthesizer) | Expression | `[KEEP]` |

#### 6.1.7 Production Family (4 Skills) — Layer 4: Execution / Layer 7: Expression

Direct creative output generation.

| Skill | Path | Owning Agent | Layer | Mandate |
|---|---|---|---|---|
| `script-generator` | `production/script-generator/` | Cesare (Script Artisan) | Execution | `[EDIT]` — Integrate 6-Beat Conscious Arc from CBCS Artisan. Merge TTT modulation logic. |
| `soc-generator` | `production/soc-generator/` | Charlotte (Stream Generator) | Expression | `[KEEP]` — Stream of Consciousness generation. Voice-first pipeline. |
| `mirror-session` | `production/mirror-session/` | Alex (triggered by Phoenix) | Execution | `[EDIT]` — Already upgraded with H14 architecture (WATCH → MIRROR → CHALLENGE → CRYSTALLIZE). |
| `wisdom-forge` | `production/wisdom-forge/` | Lionel / Jordan (The Analyst) | Reasoning | `[EDIT]` — Already upgraded with H15 architecture (MINE → FORGE → TEMPER + Boredom Ban). |

#### 6.1.8 Orchestration Family (4 Skills) — Layer 5: Orchestration

Pipeline coordination and batch management skills.

| Skill | Path | Owning Agent | Layer | Mandate |
|---|---|---|---|---|
| `ccf-batch` | `orchestration/ccf-batch/` | Alex | Orchestration | `[EDIT]` — Integrate with `TeamOrchestrator` extension. Add Receipt Chain checkpoints. |
| `ccf-multi-theme` | `orchestration/ccf-multi-theme/` | Alex / Divine | Orchestration | `[EDIT]` — Connect to `MemoryFolder` for cross-theme novelty checks. |
| `ccf-produce` | `orchestration/ccf-produce/` | Alex | Orchestration | `[EDIT]` — Add `TillDone` extension integration for retry logic. |
| `ccf-report` | `orchestration/ccf-report/` | Phoenix | Orchestration | `[EDIT]` — Connect to Learning System for evolutionary metrics. |

#### 6.1.9 Root CCF Skill (1)

| Skill | Path | Purpose | Mandate |
|---|---|---|---|
| `ccf/SKILL.md` | `skills/ccf/SKILL.md` | Master CCF system prompt. Defines the I-R-E-V-C protocol and 10 Alchemy Principles. Loaded by all CCF agents at session start. | `[EDIT]` — Integrate 7-layer architecture references. Add Pi Extension hooks. |

### 6.2 CBCS Agent Protocols (12 SKILL.md Files)

These live in `CBCS/backend/intelligence_library/protocols/`. Each is a dedicated operational protocol for one CBCS agent.

| Protocol | Owning Agent (CCP Name) | Layer | Mandate |
|---|---|---|---|
| `aria_SKILL.md` | Aria (The Synthesizer) | Perception | `[EDIT]` — File stays as-is, agent name unchanged. |
| `lionel_SKILL.md` | Remgion (The Researcher) | Deep Research | `[RENAME → `remgion_SKILL.md`]` — Update all internal references. |
| `maeva_SKILL.md` | Tshala (The Sentinel) | Deep Research | `[RENAME → `tshala_SKILL.md`]` — Update Tavily API integration. |
| `kimya_SKILL.md` | Tshilanda (The Configurator) | Memory | `[RENAME → `tshilanda_SKILL.md`]` — Update PantryConfig references. |
| `atlas_SKILL.md` | Atlas (The Strategic Planner) | Execution | `[EDIT]` — Add `MemoryFolder` milestone tracking. |
| `assembler_SKILL.md` | Assembler (The Ritual Strategist) | Execution | `[KEEP]` — Already accurate. |
| `artisan_SKILL.md` | Artisan (The Master Copywriter) | Expression | `[EDIT]` — Update cross-references to Remgion/Tshala. |
| `voice_agent_SKILL.md` | Voice Agent (The Audio Director) | Expression | `[EDIT]` — Update reference to Job's Voice DNA. |
| `emilio_SKILL.md` | Vidye (The Orchestrator) | Orchestration | `[RENAME → `vidye_SKILL.md`]` — Update state machine references. |
| `liliane_SKILL.md` | Liliane (The Guardian) | Governance | `[EDIT]` — Add Receipt Chain Guard integration. |
| `valeriane_SKILL.md` | Job (The Voice Profiler) | Memory | `[RENAME → `job_SKILL.md`]` — Update output to `coach_soul.json`. |
| `dilaya_SKILL.md` | Beleshay (The Cultural Anthropologist) | Memory | `[RENAME → `beleshay_SKILL.md`]` — Update Tshala trigger references. |

### 6.3 Tools (Python Scripts & Applications)

These are executable scripts in `tools/` that provide external capabilities (API access, data processing).

| Tool | File | Type | Owning Agent(s) | Layer | Mandate |
|---|---|---|---|---|---|
| **Firecrawl Wrapper** | `tools/firecrawl_wrapper.py` | API wrapper | Maeva (CCF), Tshala (CBCS), Adele (Radar Operator) | Deep Research | `[EDIT]` — Connect to `InteractComp` extension. Add rate limiting and caching. |
| **Google Trends Wrapper** | `tools/google_trends_wrapper.py` | API wrapper | Divine, Adele (Radar Operator) | Deep Research | `[EDIT]` — Add Real Time Tribe Relevance scoring. Feed `MemoryFolder`. |
| **Sentiment Wrapper** | `tools/sentiment_wrapper.py` | Data processor | Tshala (CBCS), Maeva (CCF) | Deep Research | `[EDIT]` — Integrate with Tshala's `SentimentReport` JSON output. |
| **Voice Transcriber** | `tools/transcribe_voice.py` | Audio processor | Voice Agent (CBCS), recording-director (CCF) | Perception | `[EDIT]` — Connect to Sacred Audio pipeline. Feed Aria for context extraction. |
| **Tierlist App** | `tools/tierlist-app/` | Web application | Gerard (Rating Engine) | Expression | `[EDIT]` — Integrate with Excalidraw rendering. Connect to `SystemSelect`. |
| **Telegram Tierlist Bot** | `tools/telegram-tierlist-bot/` | Bot interface | Gerard (Rating Engine) | Expression | `[EDIT]` — Connect to CCP pipeline for automated tierlist generation. |

### 6.4 Skills-to-Layer Architecture Map

Summary view of how all skills distribute across the 7-layer architecture:

| Layer | Skills Count | Primary Families |
|---|---|---|
| **L1: Perception** | 1 | `transcribe_voice.py` |
| **L2: Memory** | 8 | Setup (6), tribe-distiller, voice-distiller |
| **L3: Deep Reasoning** | 15 | Content (7), Distillation (6), wisdom-forge, script-architect |
| **L4: Execution** | 22 | E-Roll (14), Production (3), atlas, assembler, research analysts |
| **L5: Orchestration** | 6 | Orchestration (4), blueprint-orchestrator, distribution/orchestrator |
| **L6: Governance** | 4 | research/critic, Minister of Identity (cmd 7.5), Minister of Relevance (cmd 10.5), Minister of Timing (cmd 15.5) |
| **L7: Expression** | 18 | Visual Recipes (14), soc-generator, art-director, smart-mix, recording-director |
| **L1: Deep Research** | ~94 | Research (deep-analysts ×45, fresh-analysts ×45, raw-research ×2, smart-query, vibe-comments) |
| **Cross-Layer Tools** | 6 | Python wrappers (4) + Apps (2) |

### 6.5 V²WS Skills & Assets (31 Design Papers — All `[CREATE]` as SKILL.md)

The V²WS (Visual² Webinar System) assets live in `Conscious V²WS Papers/`. These are detailed design documents — NOT yet converted to SKILL.md format. Each must be transformed into a Pi-harness-compatible skill owned by a V²WS agent.

#### 6.5.1 Webinar Module Papers (17 — Structural Blueprints)

| Paper | File | Target Skill | Owning Agent | Layer | Mandate |
|---|---|---|---|---|---|
| **HOOK** | `INTRO-001_HOOK.md` | `v2ws/intro/hook` | Alessandro (Webinar Architect) | Execution | `[CREATE]` |
| **Positioning & Authority** | `INTRO-002_Positioning.md` | `v2ws/intro/authority` | Alessandro (Webinar Architect) | Execution | `[CREATE]` |
| **Hope Creation** | `INTRO-003_Hope.md` | `v2ws/intro/hope` | Alessandro (Webinar Architect) | Execution | `[CREATE]` |
| **Intrigue Creation** | `INTRO-004_Intrigue.md` | `v2ws/intro/intrigue` | Alessandro (Webinar Architect) | Execution | `[CREATE]` |
| **Micro-Commitment Builder** | `INTRO-005_Micro-Commitment.md` | `v2ws/intro/micro-commit` | Alessandro (Webinar Architect) | Execution | `[CREATE]` |
| **Intro Objections** | `INTRO-006_Objections.md` | `v2ws/intro/objections` | Alessandro (Webinar Architect) | Execution | `[CREATE]` |
| **Clearly Defined Outcome** | `CONTENT-01_CDO.md` | `v2ws/content/outcome-framework` | Elene (Slide Composer) | Execution | `[CREATE]` |
| **Step Transformation** | `CONTENT-02_Step.md` | `v2ws/content/step-transformation` | Elene (Slide Composer) | Execution | `[CREATE]` |
| **Bridge to Selling** | `TRANSITION-01_Bridge.md` | `v2ws/transition/bridge` | Alessandro (Webinar Architect) | Execution | `[CREATE]` |
| **Momentum Builder** | `TRANSITION-02_Momentum.md` | `v2ws/transition/momentum` | Alessandro (Webinar Architect) | Execution | `[CREATE]` |
| **Recap Reinforcer** | `TRANSITION-03_Recap.md` | `v2ws/transition/recap` | Alessandro (Webinar Architect) | Execution | `[CREATE]` |
| **Information Close** | `CLOSE-01_Information.md` | `v2ws/close/information` | Alessandro (Webinar Architect) | Expression | `[CREATE]` |
| **Old Habits Close** | `CLOSE-02_Old_Habits.md` | `v2ws/close/old-habits` | Alessandro (Webinar Architect) | Expression | `[CREATE]` |
| **Pain Relief Close** | `CLOSE-03_Pain_Relief.md` | `v2ws/close/pain-relief` | Alessandro (Webinar Architect) | Expression | `[CREATE]` |
| **Do Nothing Close** | `CLOSE-04_Do_Nothing.md` | `v2ws/close/do-nothing` | Alessandro (Webinar Architect) | Expression | `[CREATE]` |
| **Offer** | `CLOSE-05_Offer.md` | `v2ws/close/offer` | Alessandro (Webinar Architect) | Expression | `[CREATE]` |
| **Close Objections** | `CLOSE-06_Objections.md` | `v2ws/close/objections` | Alessandro (Webinar Architect) | Expression | `[CREATE]` |

#### 6.5.2 Intelligence & Production Papers (9 — Creative Systems)

| Paper | File | Target Skill | Owning Agent | Layer | Mandate |
|---|---|---|---|---|---|
| **Research Planning Engine** | `RESEARCH PLANNING ENGINE_.md` | `v2ws/research/planning-engine` | Lionel (CCF) | Deep Research | `[CREATE]` |
| **Deep Research Analyst** | `DEEP RESEARCH ANALYST_.md` | `v2ws/research/deep-analyst` | Lionel (CCF) | Deep Research | `[CREATE]` |
| **Fresh Research Analyst** | `FRESH RESEARCH ANALYST_.md` | `v2ws/research/fresh-analyst` | Maeva (CCF) | Deep Research | `[CREATE]` |
| **Visual Hook Architect** | `VISUAL HOOK ARCHITECT.md` | `v2ws/visual/hook-architect` | Elene (Slide Composer) | Expression | `[CREATE]` |
| **TTT × Visual Hook Integration** | `TTT × VISUAL HOOK.md` | `v2ws/visual/ttt-hook-integration` | Elene (Slide Composer) | Expression | `[CREATE]` |
| **TTT System (V²WS Edition)** | `TEMPERAMENT TEMPERATURE TONE.md` | `v2ws/voice/ttt-system` | Voice Agent (CCF equiv.) | Expression | `[CREATE]` |
| **Meme Orchestrator** | `MEME ORCHESTRATOR.md` | `v2ws/meme/orchestrator` | Meme Engine (CCF) | Expression | `[CREATE]` |
| **V²WS SOP** | `V²WS - Standard Operating Procedure.md` | `v2ws/orchestration/sop` | Alessandro (Webinar Architect) | Orchestration | `[CREATE]` |
| **V²WS README** | `README.md (V²WS).md` | Reference doc (not a skill) | — | — | `[KEEP]` as documentation |

#### 6.5.3 V²WS Data Files (2)

| File | Type | Purpose | Mandate |
|---|---|---|---|
| `V²WS HOOKS Workflow.json` | JSON | Workflow state machine for hook generation pipeline | `[EDIT]` — Convert to Pi-harness-compatible pipeline config. |
| **4 Meme Theory Papers** | MD | Benign Violation, Incongruity, Relief, Superiority theory templates for webinar memes | `[CREATE]` — Convert to `v2ws/meme/` skill family (4 skills). |

### 6.6 Tierlist & Excalidraw Skills & Tools (All `[EDIT]` or `[CREATE]`)

#### 6.6.1 Tierlist App (Existing — Vite + React + Excalidraw)

| Component | Path | Type | Purpose | Mandate |
|---|---|---|---|---|
| `App.jsx` | `tools/tierlist-app/src/App.jsx` | React component | Main tierlist UI layout | `[EDIT]` — Connect to CCP pipeline input. |
| `ExcalidrawCanvas.jsx` | `tools/tierlist-app/src/components/ExcalidrawCanvas.jsx` | React component | Excalidraw rendering canvas for tier visualizations | `[EDIT]` — Add programmatic tier generation from Rating Engine JSON. |
| `vite.config.js` | `tools/tierlist-app/vite.config.js` | Build config | Vite bundler configuration | `[KEEP]` |
| `index.html` | `tools/tierlist-app/index.html` | Entry point | HTML shell | `[KEEP]` |

#### 6.6.2 Telegram Tierlist Bot (Existing — Python)

| Component | Path | Type | Purpose | Mandate |
|---|---|---|---|---|
| `bot.py` | `tools/telegram-tierlist-bot/bot.py` | Python | Telegram bot entry point | `[EDIT]` — Connect to CCP pipeline for automated triggers. |
| `generator.py` | `tools/telegram-tierlist-bot/generator.py` | Python | Tier ranking content generation | `[EDIT]` — Integrate with Gerard (Rating Engine) agent output. |
| `formatter.py` | `tools/telegram-tierlist-bot/formatter.py` | Python | Output formatting for Telegram delivery | `[EDIT]` — Add Excalidraw rendering integration. |
| `scheduler.py` | `tools/telegram-tierlist-bot/scheduler.py` | Python | Automated scheduling for tier posts | `[EDIT]` — Connect to `TeamOrchestrator` extension for coordination. |

#### 6.6.3 Excalidraw BMAD Workflows (4 — Reference Templates)

| Workflow | Path | Purpose | Mandate |
|---|---|---|---|
| `create-excalidraw-dataflow` | `bmad/bmad-bmm-workflows-create-excalidraw-dataflow.md` | Data flow diagram generation | `[KEEP]` as reference — available for Grant (Render Controller). |
| `create-excalidraw-diagram` | `bmad/bmad-bmm-workflows-create-excalidraw-diagram.md` | General diagram generation | `[KEEP]` as reference. |
| `create-excalidraw-flowchart` | `bmad/bmad-bmm-workflows-create-excalidraw-flowchart.md` | Flowchart generation | `[KEEP]` as reference. |
| `create-excalidraw-wireframe` | `bmad/bmad-bmm-workflows-create-excalidraw-wireframe.md` | Wireframe generation | `[KEEP]` as reference. |

#### 6.6.4 Excalidraw Composer (Unified Visual Pipeline — To Be Created)

| Skill | Path | Purpose | Mandate |
|---|---|---|---|
| `excalidraw-composer` | `skills/visual/excalidraw-composer/SKILL.md` | Unified Excalidraw visual generation for all content types (webinars, tierlists, ratings, reactions) using branded templates, image assets, and the Transparent Collage Pipeline (emotion-driven AI stick figures with alpha extraction → transparent PNG → Excalidraw injection) | `[CREATE]` — Design the unified Excalidraw generation pipeline for Benjamin (Excalidraw Composer) and Grant (Render Controller). |

### 6.7 Skills-to-Layer Architecture Map (Updated)

| Layer | Skills Count | Primary Families |
|---|---|---|
| **L1: Perception** | 1 | `transcribe_voice.py` |
| **L2: Memory** | 8 | Setup (6), tribe-distiller, voice-distiller |
| **L3: Deep Reasoning** | 15 | Content (7), Distillation (6), wisdom-forge, script-architect |
| **L4: Execution** | 39 | E-Roll (14), Production (3), atlas, assembler, V²WS modules (17), research analysts |
| **L5: Orchestration** | 7 | Orchestration (4), blueprint-orchestrator, distribution/orchestrator, V²WS SOP |
| **L6: Governance** | 1 | research/critic |
| **L7: Expression** | 28 | Visual Recipes (14), V²WS visual/close (10), soc-generator, art-director, smart-mix, recording-director |
| **L1: Deep Research** | ~97 | Research (deep-analysts ×45, fresh-analysts ×45, raw-research ×2, V²WS research ×3, smart-query, vibe-comments) |
| **Cross-Layer Tools** | 14 | Python wrappers (4), Tierlist App (4 components), Telegram Bot (4 scripts), Excalidraw workflows (4) |

### 6.8 Skill Count Summary (Final)

| Category | Count | Mandate Breakdown |
|---|---|---|
| CCF Skills (10 families) | 85 | 60 `[KEEP]`, 24 `[EDIT]`, 1 `[CREATE]` |
| CBCS Protocols | 12 | 2 `[KEEP]`, 4 `[EDIT]`, 6 `[RENAME + EDIT]` |
| V²WS Papers → Skills | 31 | 1 `[KEEP]` (README), 1 `[EDIT]`, 29 `[CREATE]` |
| Tierlist/Excalidraw | 12 | 6 `[KEEP]`, 6 `[EDIT]` |
| Excalidraw Composer | 1 | 1 `[CREATE]` |
| Tools (Python) | 6 | 0 `[KEEP]`, 6 `[EDIT]` |
| **TOTAL** | **147** | |

---

## Section 7: Command & Pipeline Full Wiring

This section maps every existing command in `commands/` to its pipeline, owning agent, skills invoked, extensions triggered, and receipt chain gates. Commands are the user-facing entry points that trigger agent pipelines.

### 7.1 CCF Genesis Pipeline (One-Time Setup — 7 Commands)

Run once per coach onboarding. Executes sequentially. Morgan (Setup Orchestrator) coordinates.

| # | Command | File | Owning Agent | Skills Invoked | Extensions Triggered | Receipt Gate |
|---|---|---|---|---|---|---|
| 1 | `ccf-init` | `commands/ccf-init.md` | Morgan | Root `ccf/SKILL.md` | — | Creates `config.yaml` + workspace structure |
| 2 | `ccf-elicit` | `commands/ccf-elicit.md` | Kimya (CCF) + Valeriane (CCF) | `coach-elicitation` | `SoulResonance` | → `01_business_canvas.md` |
| 3 | `ccf-soul-extract` | `commands/ccf-soul-extract.md` | Valeriane (CCF) | `client-soul-extraction`, `voice-distiller` | `SoulResonance` | → `coach_soul.json` + `ttt_baseline.json` |
| 4 | `ccf-tribe-extract` | `commands/ccf-tribe-extract.md` | Dilaya (CCF) | `tribe-soul-extraction` | `InteractComp` | → `tribe_soul.json` |
| 5 | `ccf-pillar-build` | `commands/ccf-pillar-build.md` | Emmanuel | `pillar-builder` | — | → Content pillars defined |
| 6 | `ccf-philosophy-brief` | `commands/ccf-philosophy-brief.md` | Emmanuel | `philosophy-brief` | — | → Philosophy framework |
| 7 | `ccf-blueprint` | `commands/ccf-blueprint.md` | Emmanuel | `blueprint-distiller`, `blueprint-orchestrator` | — | → `02_content_strategy.md` |

### 7.2 CCF Weekly Production Pipeline (Recurring — 16 Commands)

Run weekly/bi-weekly. Alex (Content Orchestrator) coordinates production. Phoenix (Regeneration Orchestrator) handles iteration.

#### Phase A: Discovery & Research (5 commands)

| # | Command | File | Owning Agent | Skills Invoked | Extensions | Receipt Gate |
|---|---|---|---|---|---|---|
| 8 | `ccf-theme-discover` | `commands/ccf-theme-discover.md` | Divine | `theme-discovery`, `dynamic-theme-generator` | `MemoryFolder` (novelty check) | → `final_selection.md` (2 themes) |
| 9 | `ccf-radar` | `commands/ccf-radar.md` | Adele (Radar Operator) | `intelligence-radar` | `InteractComp` | → Real-time trend data |
| 10 | `ccf-raw-research` | `commands/ccf-raw-research.md` | Lionel (CCF) | `raw-deep-research`, `raw-fresh-research` | — | → 30-40 page research library |
| 11 | `ccf-research-deep` | `commands/ccf-research-deep.md` | Lionel → Jordan | `deep-analysts/*` (×45 variants) | — | → Archetype-specific deep analysis |
| 12 | `ccf-research-fresh` | `commands/ccf-research-fresh.md` | Maeva (CCF) → Jordan | `fresh-analysts/*` (×45 variants) | `InteractComp` | → Current/trending intelligence |

#### Phase B: Ideation & Mapping (4 commands)

| # | Command | File | Owning Agent | Skills Invoked | Extensions | Receipt Gate |
|---|---|---|---|---|---|---|
| 13 | `ccf-vibe-comments` | `commands/ccf-vibe-comments.md` | Maeva + Lila | `vibe-comments` | `InteractComp`, `MemoryFolder` | → Audience signal data |
| 14 | `ccf-question` | `commands/ccf-question.md` | Lila | `question-engineer`, `question-distiller` | — | → Context Premise JSON |
| 15 | `ccf-analyze` | `commands/ccf-analyze.md` | Emilio (CCF) | `archetype-mapping` | `PatternWeaver` | → `ideas.json` (12 ideas) |
| 16 | `ccf-eroll-plan` | `commands/ccf-eroll-plan.md` | Emmanuel (Archetype Mapper) | E-Roll planners (×14) | — | → `archetype_assignments.json` |

#### Phase C: Research Briefs & Production (6 commands)

| # | Command | File | Owning Agent | Skills Invoked | Extensions | Receipt Gate |
|---|---|---|---|---|---|---|
| 17 | `ccf-eroll-research` | `commands/ccf-eroll-research.md` | Aurore (Visual Asset Researcher) | `asset-researcher` | — | → Visual asset queries |
| 18 | `ccf-soc` | `commands/ccf-soc.md` | Charlotte (Stream Generator) | `soc-generator` | `SoulResonance` | → 36 streams (voice-first) |
| 18.5 | `ccf-anti-draft` | `commands/ccf-anti-draft.md` | Fast Model (e.g. Gemini Flash) | `anti-draft-generator` | `ContrastiveAnchor` | → 36 generic AI drafts (anti-targets) |
| 19 | `ccf-generate` | `commands/ccf-generate.md` | Cesare (Script Artisan) | `script-generator` | `SoulResonance`, `GhostContext` | → 36 validated scripts (violently rejecting anti-drafts) |
| 20 | `ccf-wisdom` | `commands/ccf-wisdom.md` | Lionel + Jordan | `wisdom-forge` | `AncestralWisdom` | → Wisdom-enriched content |
| 21 | `ccf-adapt` | `commands/ccf-adapt.md` | Estelle (The Adaptor) | — | `SystemSelect`, `SoulResonance` | → MODE-adapted executive prompts |

#### Phase D: Visual Production & Validation (4 commands)

| # | Command | File | Owning Agent | Skills Invoked | Extensions | Receipt Gate |
|---|---|---|---|---|---|---|
| 22 | `ccf-visual` | `commands/ccf-visual.md` | Abel (Visual Recipe Router) | `visual-distiller`, `art-director` | `TeamOrchestrator` | → Visual routing decisions |
| 23 | `ccf-visual-assets` | `commands/ccf-visual-assets.md` | Aurore + Paradoxe | Visual recipes (×14) | `TeamOrchestrator` | → `visual_prompts.json` + `visual_asset_queries.json` |
| 24 | `ccf-validate` | `commands/ccf-validate.md` | Sophia + Marcus + Chen | `research/critic` | `TillDone` | → Validation scores + improvement notes |

#### Phase E: Orchestration & Memory (4 commands)

| # | Command | File | Owning Agent | Skills Invoked | Extensions | Receipt Gate |
|---|---|---|---|---|---|---|
| 25 | `ccf-batch` | `commands/ccf-batch.md` | Alex | `ccf-batch` orchestration | `TeamOrchestrator`, `TillDone` | → Full batch output |
| 26 | `ccf-weekly` | `commands/ccf-weekly.md` | Alex | `ccf-produce`, `ccf-report` | All extensions | → Weekly production cycle |
| 27 | `ccf-memory` | `commands/ccf-memory.md` | Azaria (Memory Curator) | `memory-engine` → `MemoryFolder` | `MemoryFolder` | → Memory promotion log |
| 28 | `ccf-tierlist` | `commands/ccf-tierlist.md` | Gerard (Rating Engine) | Tierlist App + Telegram Bot | `SystemSelect` | → Tierlist visual output |

### 7.3 V²WS Pipeline (To Be Created — 6 New Commands)

These commands do not yet exist. Alessandro (Webinar Architect) coordinates. Based on the 31 V²WS design papers.

| # | Command | File | Owning Agent | Skills to Create | Extensions | Receipt Gate |
|---|---|---|---|---|---|---|
| V1 | `v2ws-init` | `commands/v2ws-init.md` | Alessandro | `v2ws/orchestration/sop` | — | `[CREATE]` — Workspace + config |
| V2 | `v2ws-research` | `commands/v2ws-research.md` | Lionel + Maeva (CCF) | `v2ws/research/*` (3 skills) | `InteractComp` | `[CREATE]` — Webinar research pack |
| V3 | `v2ws-structure` | `commands/v2ws-structure.md` | Alessandro | `v2ws/intro/*` (6) + `v2ws/transition/*` (3) | `SoulResonance` | `[CREATE]` — Full webinar structure |
| V4 | `v2ws-slides` | `commands/v2ws-slides.md` | Elene (Slide Composer) | `v2ws/content/*` (2) + `v2ws/visual/*` (2) | `TeamOrchestrator` | `[CREATE]` — Slide deck + directives |
| V5 | `v2ws-close` | `commands/v2ws-close.md` | Alessandro | `v2ws/close/*` (6 skills) | `SoulResonance` | `[CREATE]` — Close sequence |
| V6 | `v2ws-render` | `commands/v2ws-render.md` | Benjamin (Excalidraw Composer) + Grant | `excalidraw-composer` | `TillDone` | `[CREATE]` — Branded `.excalidraw` slide deck with module scripts |

### 7.4 Tierlist Pipeline (Partially Existing — 2 New Commands)

Gerard (Rating Engine) and Grant (Render Controller) coordinate. `ccf-tierlist` exists; 2 new commands needed.

| # | Command | File | Owning Agent | Skills/Tools | Extensions | Receipt Gate |
|---|---|---|---|---|---|---|
| T1 | `ccf-tierlist` | `commands/ccf-tierlist.md` | Gerard | `generator.py`, Tierlist App | `SystemSelect` | `[EDIT]` — Existing, needs CCP wiring |
| T2 | `tierlist-render` | `commands/tierlist-render.md` | Grant | `ExcalidrawCanvas.jsx` | `TillDone` | `[CREATE]` — Visual output |
| T3 | `tierlist-publish` | `commands/tierlist-publish.md` | Gerard + Grant | `bot.py`, `formatter.py`, `scheduler.py` | `TeamOrchestrator` | `[CREATE]` — Telegram delivery |

### 7.5 CBCS Pipeline (Existing — Event-Driven, Real-Time)

Unlike CCF (command-based), CBCS is a **real-time Telegram webhook pipeline**. Entry point: `ingress.py` → FastAPI `/webhook` endpoint. Vidye (State Manager) routes every message.

#### User Flow (Telegram → Ritual Delivery)

Triggered by every user message via Telegram webhook. Runs in `<2s` target latency.

| Step | Module | Owning Agent (CCP Name) | Function | Extensions |
|---|---|---|---|---|
| 1. **Webhook Receive** | `ingress.py` | — | FastAPI receives Telegram update, validates secret token, offloads to background task | — |
| 2. **Role Resolution** | `ingress.py → RoleRegistry` | — | Resolves `chat_id` → coach/user/unknown. Cache-first, Supabase fallback | — |
| 3. **State Check** | `core/state.py` | Vidye (Orchestrator) | Checks dormancy thresholds (3/5/10/30 days), routes accordingly | — |
| 4. **Crisis Pre-Scan** | `core/circuit_breaker.py` | Liliane (Guardian) | Tier 1 keyword scan (<100ms). If triggered → crisis protocol, skip all else | — |
| 5. **Transcription** | `core/transcription.py` | — | If voice message → `transcribe_voice.py` → text | — |
| 6. **Context Extraction** | `core/aria.py` | Aria (Synthesizer) | 12-dimension extraction from raw text | `SoulResonance` |
| 7. **Research Lookup** | `core/lionel.py` | Remgion (Researcher) | RAG query to Supabase vector store for facts/citations | — |
| 8. **Sentiment Scan** | `core/maeva.py` | Tshala (Sentinel) | Tavily API scan for real-time context (if scheduled) | `InteractComp` |
| 9. **Ritual Selection** | `core/assembler.py` | Assembler (Strategist) | Weighted scoring → best ritual match | — |
| 10. **Roadmap Check** | `core/atlas.py` | Atlas (Planner) | Validates selection against 30-day roadmap position | `MemoryFolder` |
| 11. **Script Generation** | `core/artisan.py` | Artisan (Copywriter) | 6-Beat Conscious Arc personalization | `SoulResonance`, `GhostContext` |
| 12. **Audio Directive** | `core/voice.py` | Voice Agent (Audio Director) | TTT → prosody mapping → `AudioDirective` JSON | — |
| 13. **Delivery** | `core/telegram.py` | — | Send script + audio via Telegram Bot API | — |

#### Coach Flow (Coach Message → Pipeline Trigger)

Triggered when a coach sends a message. Routes to `coach_graph` subgraph.

| Step | Module | Function |
|---|---|---|
| 1. **Coach Listening** | `ingress.py → _route_to_coach_graph` | Buffers coach messages, resolves intent |
| 2. **Content Ideation** | `core/coach_graph.py` | Coach requests content ideas → triggers CCF mini-pipeline |
| 3. **Pipeline Trigger** | `core/coach_graph.py` | Coach triggers batch production → hands off to CCF commands |
| 4. **User Monitor** | `core/analytics.py` | Coach queries user engagement/progress data |

#### System Flow (Scheduled / Background)

CBCS is not purely reactive. Proactive scheduled events are **coach-program-configurable** via `PantryConfig`.

| Step | Module | Owning Agent | Schedule | Type |
|---|---|---|---|---|
| **Accountability Check-In** | `core/scheduler.py` → `core/artisan.py` | Atlas + Artisan | **Daily** (configurable per coach program) | Proactive — sends personalized accountability prompt based on roadmap position |
| **Journaling Prompt** | `core/scheduler.py` → `core/artisan.py` | Atlas + Artisan | **2-3x/week** (configurable per coach program) | Proactive — sends journal prompt calibrated to current ritual and TTT state |
| **Dormancy Recovery** | `core/scheduler.py` → `core/state.py` | Vidye (Orchestrator) | Triggered at 3/5/10/30 day dormancy thresholds | Proactive — escalating re-engagement sequence |
| **Ritual Reminder** | `core/scheduler.py` → `core/telegram.py` | Atlas | Per-ritual schedule (morning/evening/custom) | Proactive — time-based ritual nudges |
| **Sentiment Sweep** | `core/scheduler.py` → `core/maeva.py` | Tshala (Sentinel) | Weekly Monday scans | Background |
| **Onboarding** | `scripts/run_onboarding.py` | Tshilanda (Configurator) | On new coach registration | Event-triggered |
| **Assessment** | `api/assessment.py` + `core/assessment.py` | Aria | On user assessment submission | Event-triggered |
| **Analytics** | `api/analytics.py` | — | On-demand API | On-demand |
| **Graph Updates** | `core/graph.py` + `core/graph_db.py` | — | After every interaction | Background |
| **Sunday Bot Meeting** | `core/scheduler.py` | Azaria (Memory Curator) | Weekly Sunday | Background — memory promotion + learning loop |

#### CBCS Core Modules Summary

| Module | File | Purpose | Mandate |
|---|---|---|---|
| `ingress.py` | `CBCS/backend/ingress.py` | Webhook + role routing | `[EDIT]` — Add Pi extension hooks |
| `main.py` | `CBCS/backend/main.py` | FastAPI app entry | `[EDIT]` — Add `ModelRouter` init |
| `state.py` | `CBCS/backend/core/state.py` | State machine management | `[EDIT]` — Connect to `MemoryFolder` |
| `graph.py` | `CBCS/backend/core/graph.py` | LangGraph pipeline definition | `[EDIT]` — Integrate Pi extensions as graph nodes |
| `graph_db.py` | `CBCS/backend/core/graph_db.py` | Neo4j graph operations | `[EDIT]` — Add hyper-edge support for `MemoryFolder` |
| `circuit_breaker.py` | `CBCS/backend/core/circuit_breaker.py` | Crisis detection | `[KEEP]` — Already hardcoded safety |
| `scheduler.py` | `CBCS/backend/core/scheduler.py` | Cron-based task scheduling | `[EDIT]` — Add Sunday Bot Meeting, ccf-weekly triggers |
| `telegram.py` | `CBCS/backend/core/telegram.py` | Telegram Bot API client | `[KEEP]` |
| `skill_loader.py` | `CBCS/backend/core/skill_loader.py` | SKILL.md protocol loader | `[EDIT]` — Support renamed SKILL.md files |
| `intelligence.py` | `CBCS/backend/core/intelligence.py` | Intelligence library loader | `[EDIT]` — Load `coach_soul.json` (renamed) |
| `cli_runner.py` | `CBCS/backend/core/cli_runner.py` | CLI test harness | `[EDIT]` — Add CCF command integration |
| `setup_agents.py` | `CBCS/backend/core/setup_agents.py` | Agent initialization | `[EDIT]` — Use renamed agent files |

### 7.6 Pipeline Dependency Graph

```
CCF GENESIS (one-time):
  ccf-init → ccf-elicit → ccf-soul-extract → ccf-tribe-extract → ccf-pillar-build → ccf-philosophy-brief → ccf-blueprint

CCF WEEKLY PRODUCTION (recurring):
  ccf-theme-discover ─┬─→ ccf-radar
                       ├─→ ccf-raw-research → ccf-research-deep ─┐
                       └─→ ccf-vibe-comments                     │
                                                                  ├─→ ccf-research-fresh
                                                                  ↓
  ccf-question → ccf-analyze → ccf-eroll-plan → ccf-eroll-research
                                                        ↓
  ccf-soc → ccf-generate → ccf-wisdom → ccf-adapt
                                            ↓
  ccf-visual → ccf-visual-assets → ccf-validate
                                       ↓
  ccf-batch → ccf-weekly → ccf-memory

CBCS (real-time, per-message):
  Telegram webhook → Role Resolution → State Check → Crisis Pre-Scan
      ↓ (if user)                                    ↓ (if crisis)
  Aria → Remgion → Assembler → Atlas → Artisan → Voice → Deliver
      ↓ (if coach)
  Coach Listening → Content Ideation | Pipeline Trigger | User Monitor

V²WS (to create):
  v2ws-init → v2ws-research → v2ws-structure → v2ws-slides → v2ws-close → v2ws-render

TIERLIST:
  ccf-tierlist → tierlist-render → tierlist-publish
```

### 7.7 Command & Pipeline Count Summary

| Pipeline | Type | Existing | New | Total |
|---|---|---|---|---|
| CCF Genesis | Command-based | 7 | 0 | 7 |
| CCF Weekly Production | Command-based | 16 | 0 | 16 |
| CCF Orchestration | Command-based | 5 | 0 | 5 |
| CBCS | Event-driven (real-time) | 12 modules | 0 | 12 |
| V²WS | Command-based | 0 | 6 | 6 |
| Tierlist | Command-based | 1 | 2 | 3 |
| **TOTAL** | | **41** | **8** | **49** |

---

## Section 8: Memory, Governance & Intelligence Ecosystem

This section defines the memory architecture, governance mechanisms, learning loops, and external integration points that make the CCP a self-evolving system rather than a static pipeline.

### 8.1 Memory Architecture (3-Tier + MemoryFolder Extension)

All CCP memory lives in the `MemoryFolder` extension (Pi Extension #5). Three tiers with distinct lifecycles:

#### 8.1.1 Tier 1: Working Memory (Per-Session, Volatile)

| Property | Value |
|---|---|
| **Scope** | Single pipeline run or conversation session |
| **Lifetime** | Discarded at session end unless promoted |
| **Storage** | In-memory (LangGraph state) |
| **Contents** | Current context premise, draft scripts, intermediate analysis, RAG results |
| **Written by** | Every agent during execution |
| **Read by** | All downstream agents in same session |
| **Promotion Rule** | Survives only if Azaria (Memory Curator) marks it during Sunday Bot Meeting |

#### 8.1.2 Tier 2: Episodic Memory (Per-Interaction, Persistent)

| Property | Value |
|---|---|
| **Scope** | Individual user interactions and content runs |
| **Lifetime** | Persistent. Pruned after 8 weeks if not referenced |
| **Storage** | Supabase (vector store) + Neo4j (graph edges) |
| **Contents** | Completed rituals, user responses, engagement metrics, content performance data |
| **Written by** | CBCS after ritual delivery; CCF after content validation |
| **Read by** | Atlas (roadmap), Assembler (ritual weighting), Adele (trend detection) |
| **Promotion Rule** | If a pattern appears 3+ times across 3 weeks → promoted to Semantic by Azaria |

#### 8.1.3 Tier 3: Semantic Memory (Permanent, Structural)

| Property | Value |
|---|---|
| **Scope** | Cross-session coach/tribe intelligence |
| **Lifetime** | Permanent — never auto-pruned |
| **Storage** | Neo4j (hyper-edges), Supabase (embeddings), `coach_soul.json` / `tribe_soul.json` |
| **Contents** | Coach voice DNA, tribal archetypes, validated content patterns, TTT baselines, Sacred Audio fingerprints |
| **Written by** | Azaria (Sunday promotion), Valeriane/Dilaya (setup extraction) |
| **Read by** | All agents via `SoulResonance` extension |
| **Integrity Rule** | Any write to Semantic Memory must be co-signed by Receipt Chain Guard |

#### 8.1.4 Memory Flow Diagram

```
Working Memory (volatile)
    ↓ (3-week consistency rule)
Episodic Memory (persistent, 8-week window)
    ↓ (pattern detected 3+ times)
Semantic Memory (permanent)
    ↑
  Sunday Bot Meeting (Azaria reviews + promotes)
```

### 8.2 Governance Layer

#### 8.2.1 Receipt Chain Guard

Every pipeline step produces a receipt. Receipts are immutable, append-only, and form the audit trail.

| Property | Value |
|---|---|
| **Architecture** | Defined in `docs/architecture/receipt_chain_guard.md` |
| **Receipt Format** | `{agent, timestamp, input_hash, output_hash, extension_triggered, mode, confidence}` |
| **Chain** | Each receipt references `previous_receipt_hash` → linked list |
| **Validation** | Liliane (Guardian) can audit any chain. Broken chains flag production halt. |
| **Storage** | Supabase `receipt_chain` table |
| **Owning Agent** | Liliane (Guardian) — reads all; writes chain metadata |

#### 8.2.2 Circuit Breaker (Crisis Protocol)

| Tier | Trigger | Response Time | Action |
|---|---|---|---|
| **Tier 1** | Keyword scan (suicide, self-harm, crisis vocabulary) | <100ms | Immediate crisis resource delivery. All other agents suspended. |
| **Tier 2** | Sentiment analysis flags (extreme distress pattern) | <500ms | Warm handoff message + escalation log |
| **Tier 3** | Dormancy + re-engagement failure (30-day threshold) | Scheduled | Coach notification + account status update |
| **Ownership** | Liliane (Guardian) — hardcoded, never overridable, never adaptive |

#### 8.2.3 Validation Team Gate & 30-Day Movement Seasons

Every CCF content output must pass through the Validation Team before delivery. The Protocol Validator is governed by a **30-Day Movement Season**. Marcus does not enforce the same exact tone forever; his validation mandate rotates every 30 days.

**The 4 Rotational Mandates (Season of the Movement):**
1. **Deconstruction (The Sword):** High friction. Calling out the Enemy. Breaking false beliefs.
2. **The Forge (The Shield):** Discipline, rituals, behavioral change, hard actionable steps.
3. **The Mirror (The Water):** Vulnerability, deep introspection, coach-led storytelling.
4. **The Tribe (The Fire):** Grace, community connection, celebrating wins, "We" over "I."

| Validator | Name | Check | Threshold |
|---|---|---|---|
| **Soul Validator** | Sophia | TTT drift detection against `coach_soul.json` baseline | >85% alignment |
| **Protocol Validator** | Marcus | Structural compliance against current 30-Day Season Mandate | 100% compliance |
| **Mimicry Validator** | Chen | Human voice authenticity (AI artifacts, template bleed, generic phrasing) | <5% AI detection |
| **Gate Rule** | All 3 must pass. If any fails → `TillDone` extension triggers rewrite loop (max 3 iterations). |

#### 8.2.4 Boredom Ban (Novelty Enforcement)

| Property | Value |
|---|---|
| **Rule** | No theme, metaphor, or structural pattern may repeat within 8 weeks |
| **Enforcer** | Grâce (Draft Tester) + `MemoryFolder` history lookup |
| **Window** | 8-week sliding window checked against Episodic Memory |
| **Applied at** | Draft Protocol phase (before full generation), Theme Discovery, Wisdom Forge |
| **Penalty** | Flagged content auto-rejected. Agent must generate novel alternative. |

### 8.3 Intelligence Ecosystem (Learning Loops)

#### 8.3.1 Sunday Bot Meeting (Weekly Evolution Cycle)

| Step | Agent | Action |
|---|---|---|
| 1. **Memory Audit** | Azaria (Memory Curator) | Reviews all Working Memory edges from past week |
| 2. **Pattern Detection** | Azaria + Chiara (Connector) | Identifies recurring patterns, cross-domain links |
| 3. **Promotion Decision** | Azaria | Promotes consistent patterns (3+ occurrences) to Semantic Memory |
| 4. **Performance Report** | Phoenix (Regeneration Orchestrator) | Generates weekly evolution metrics (content engagement, ritual completion rates) |
| 5. **Strategy Adjustment** | Atlas | Updates 30-day roadmaps based on new intelligence |
| 6. **CCF Feedback** | Alex (Content Orchestrator) | Feeds engagement data back to content pipeline for next week's themes |

#### 8.3.2 Real Time Tribe Relevance (Continuous)

| Component | Agent | Frequency |
|---|---|---|
| **Google Trends Monitoring** | Adele (Radar Operator) | Continuous background sweeps |
| **Firecrawl Scraping** | Adele + Tshala | On-demand per research cycle |
| **Sentiment Analysis** | Tshala (Sentinel) | Weekly + on-demand |
| **InteractComp Scoring** | `InteractComp` extension | Every research phase — calculates freshness decay |
| **Output** | Updated `tribe_soul.json` relevance scores → feeds theme discovery + vibe comments |

#### 8.3.3 Sacred Audio Pipeline

| Step | Agent | Output |
|---|---|---|
| 1. **Transcription** | Voice Agent | Raw text from coach recordings |
| 2. **Voice DNA Extraction** | Job (Voice Profiler) | TTT baseline, speech patterns, emotional markers |
| 3. **Soul Resonance Fingerprint** | Sarah (Resonance Seeker) | Emotional charge map — which topics ignite the coach |
| 4. **Integration** | Valeriane (CCF) | Written to `coach_soul.json` Semantic Memory |
| **Trigger** | Any `SoulResonance` extension call reads this data for voice calibration |

### 8.4 External Integration Points

| Service | Purpose | Used By | Protocol | Mandate |
|---|---|---|---|---|
| **Supabase** | Vector store (embeddings), SQL (configs, receipts), Auth | All agents | REST API + Python client | `[EDIT]` — Add `receipt_chain` table, `MemoryFolder` tables |
| **Neo4j** | Knowledge graph (entities, relationships, hyper-edges) | Azaria, Atlas, Chiara | Bolt protocol | `[EDIT]` — Add hyper-edge schema for Semantic Memory |
| **Tavily API** | Real-time web search | Tshala, Adele, Remgion | REST API | `[KEEP]` — Already integrated |
| **Firecrawl API** | Deep web scraping | Adele, Maeva (CCF) | REST API | `[EDIT]` — Add rate limiting + caching via `InteractComp` |
| **Google Trends API** | Trend detection + freshness scoring | Adele, Divine | REST API | `[EDIT]` — Add tribe relevance scoring |
| **Telegram Bot API** | User/coach message delivery | CBCS pipeline, Tierlist bot | Webhook + REST | `[KEEP]` |
| **Excalidraw JSON API** | Unified visual content generation (webinars, tierlists, ratings, reactions) | Benjamin (Excalidraw Composer), Grant | JSON `.excalidraw` format | `[CREATE]` — Excalidraw Composer Skill to be built |
| **Excalidraw** | Diagram/tierlist rendering | Gerard, Grant | React component | `[EDIT]` — Add programmatic JSON input |
| **Gemini API** | LLM inference (Pro, Flash) | All agents via `ModelRouter` | REST API | `[EDIT]` — Wire through `ModelRouter` extension |

### 8.5 Environment Variables

| Variable | Service | Required By |
|---|---|---|
| `GOOGLE_API_KEY` | Gemini API | All agents (via `ModelRouter`) |
| `TAVILY_API_KEY` | Tavily search | Tshala, Adele, Remgion |
| `SUPABASE_URL` | Supabase | All persistent storage |
| `SUPABASE_KEY` | Supabase | All persistent storage |
| `NEO4J_URI` | Neo4j | Graph operations |
| `NEO4J_PASSWORD` | Neo4j | Graph operations |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot API | CBCS, Tierlist bot |
| `TELEGRAM_SECRET_TOKEN` | Webhook validation | `ingress.py` |
| `FIRECRAWL_API_KEY` | Firecrawl | Adele, Maeva (CCF) |

---

## Appendix B: Trigger\-First Architecture \(CCP v3\.1\)

### Overview

**Paradigm Shift:** From topic\-first to trigger\-first content generation\.

The previous architecture \(v3\.0\) selected topics based on audience relevance and trending friction, then asked the coach to respond\. The coach's trigger architecture — what they cannot stop responding to — was an implicit byproduct, not a design input\.

**v3\.1 inverts this\.** The system first maps the coach's permanent trigger architecture \(Emotional DNA\) and the audience's deepest pain layer \(L3\), then finds where those two maps share structural coordinates\. Content topics are selected because they activate real coach triggers at points of genuine overlap with audience reality — not because they are trending or topically relevant\.

_Research Foundation: Scherer CPM \(2009\), Lazarus Appraisal Theory \(1991\), Haidt MFQ\-2 \(2012/2023\), Barrett Constructionism \(2017\), Pennebaker LIWC\-22 \(2022\), Conway Self\-Memory System \(2005\), Tedeschi \& Calhoun PTG \(2004\), Nader Reconsolidation \(2000\), Miller \& Rollnick MI \(2012\), Clark \& Brennan Common Ground \(1991\), Tulving Episodic\-Semantic Taxonomy \(1972\), Hatfield Emotional Contagion \(1993\), Cooperrider Appreciative Inquiry \(1987\), Kahan IPC \(2017\), Frankl Logotherapy \(1946\), McAdams Narrative Identity \(2001\), Schiffrin Discourse Markers \(1987\), Kensinger Selective Accuracy \(2007\)\._

### 5\-Stage Engine Pipeline

| Stage | Component | What It Does |
| \-\-\- | \-\-\- | \-\-\- |
| 1 | Trigger Matching Layer | 2\-axis structural matching \(MFT \+ Temporal Position\) between audience L3 pain and coach triggers |
| 2 | Activation Event Designer | Converts matched seeds into ESK\-targeting retrieval keys using DARN\-CAT dimensions |
| 3 | Provocation Generator | Formats activation events into ≤80\-word Telegram prompts \+ builds LIWC\-22 authenticity rubric |
| 4 | LIWC\-22 Authenticity Gate | Scores voice note responses against 7 authenticity markers \(0\.6 composite threshold\) |
| 5 | Trigger Architecture Update | Feeds authenticity scores back to trigger\_map → activation\_history for compound learning |

### New Components

**Configs \(3\):**
- `intelligence_library/emotional_dna.json` — 10\-variable Emotional DNA profile
- `intelligence_library/trigger_map.json` — Permanent trigger architecture with PTG assessment
- `intelligence_library/coach_soul.json` v3\.1 — 3\-layer Voice DNA SPR \+ Negative Space Object

**Setup Skills \(3\):**
- `skills/ccf/setup/emotional\-dna\-extraction/` — Extracts V1\-V10 from corpus
- `skills/ccf/setup/trigger\-map\-builder/` — Maps triggers with Conway AKB \+ Tedeschi PTG
- `skills/ccf/setup/voice\-dna\-profiler/` — 60\-variable stylometry \+ 3\-layer SPR

**Content Skills \(3\):**
- `skills/ccf/content/trigger\-matching\-layer/` — Structural congruence engine
- `skills/ccf/content/activation\-event\-designer/` — ESK retrieval key constructor
- `skills/ccf/content/provocation\-generator/` — Telegram prompt \+ LIWC rubric

**Commands \(2\):**
- `/ccf\-trigger\-extract` — Genesis pipeline \(runs once per coach, 17 steps\)
- `/ccf\-trigger\-match` — Weekly pipeline insert \(11 steps, between Radar and Question\)

**Modified Existing Components \(6\):**
- `audience\-empathy` — Added `trigger_matching_candidates` L3 extraction per segment
- `intelligence\-radar` — Added `trigger_activation_score` re\-ranking \(60% weight\)
- `question\-engineer` — Added trigger\-first mode with DARN\-CAT \+ ESK targeting
- `recording\-director` — Added LIWC\-22 post\-recording authenticity check
- `soc\-generator` — Upgraded to v5\.1 \(3\-layer SPR \+ Negative Space \+ Mandates 1/3/4/5\)
- `ccf\-weekly` — Pipeline inversion \(STEP 2b trigger\-match \+ STEP 5a authenticity gate\)

### The 8 Mandates \(Prompt Doctrine\)

| \# | Mandate | Implementation |
| \-\-\- | \-\-\- | \-\-\- |
| 1 | Cognitive State, Not Role\-Character | All new skills use `Cognitive State` in SYSTEM MESSAGE |
| 2 | No Surface\-Level Descriptors | Emotional DNA extracted at depth \(Scherer/Lazarus/Barrett\) |
| 3 | Construction Constraints Replace Validation | Pre\-generation constraints in every skill |
| 4 | Negative Space Before Positive | Negative Space Object built BEFORE Layer 1 Voice DNA |
| 5 | Three\-Layer Priming | Universal invocation → Emotional path → Leadership elevation |
| 6 | Generative Not Descriptive | Skills instruct construction, not describe ideal output |
| 7 | Evidence\-Grounded Variables | Every extraction variable requires corpus citation |
| 8 | Correct Build Order | Emotional DNA → Trigger Map → Voice DNA → Prompts |

### Weekly Pipeline \(v3\.1\)

```
Pre-flight → RADAR (+trigger scoring) → TRIGGER-MATCH (NEW) → QUESTION (trigger-first mode)
→ WAIT → ELICIT → AUTHENTICITY (LIWC-22, NEW) → LEARN (+trigger update) → THEME → RESEARCH
→ SCRIPT → RECORD (+LIWC rubric)
```

The pipeline is fully backward\-compatible\. If `trigger_map.json` does not exist, STEP 2b is skipped and the system falls back to legacy question generation\.

---

**END OF CCP UNIFIED PRD v1\.0**

*Total documented: 9 sections, 65\+ named agents, 153 skills/tools, 51 pipeline elements, 3\-tier memory, 4 governance mechanisms, 3 learning loops, 9 external integrations, 18 scientific research frameworks\.*

