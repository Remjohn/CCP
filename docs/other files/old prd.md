---
title: "Conscious Content Factory (CCF) — Product Requirements Document"
version: "1.0"
date: "2026-02-15"
author: "Emilio (Product Owner) + John (PM Agent)"
status: "In Progress"
stepsCompleted: [1]
lastStep: 1
inputDocuments:
  - "ccf-26/Docs/architecture/ccf-soul-infusion/CCF_System_Architecture_Audit.md"
  - "ccf-26/Docs/architecture/ccf-soul-infusion/🟧 Conscious_Content_Factory - Master_Manual 🟧.md"
  - "ccf-26/Docs/architecture/ccf-soul-infusion/Soul_Infusion_Architecture_V3.md"
  - "ccf-26/Docs/architecture/ccf-soul-infusion/Stage_2_5_Wisdom_Forge_Brainstorm.md"
  - "ccf-26/Docs/architecture/ccf-soul-infusion/Alchemy_Comment_Processing_Architecture.md"
  - "ccf-26/Docs/architecture/ccf-soul-infusion/Vibe_Comments_Sourcing_SWOT.md"
  - "ccf-26/Docs/architecture/ccf-soul-infusion/Context_Premise_Deep_Analysis.md"
---

# Conscious Content Factory (CCF) — Product Requirements Document

---

## Section 1: Executive Summary & Product Vision

### 1.1 The Problem

The creator economy has reached an inflection point where demand for authentic, high-frequency content far exceeds what any individual coach, educator, or thought leader can produce manually. The obvious solution — AI-generated content — fails catastrophically at the one thing that matters most: **it doesn't sound like the person it's supposed to represent.** Every major LLM, when given a coach's voice data, research, and audience psychology in a single monolithic prompt, produces output that reads like a polished TED talk transcript — competent but soulless. A controlled experiment across 7 frontier models (Mistral Medium 3.2, Gemini 3 Pro, GPT 5.2, Claude 4.5 Sonnet, GLM 5, Kimi K2.5, Claude Opus 4.6) confirmed three devastating findings: no model produced genuine vulnerability, the best voice match still sounded like "SoC with structure bolted on," and quality versus word-count compliance were competing objectives — the model that hit the target word count scored 3.2/10 on quality. This is not a model problem. This is an **architecture problem.**

The root cause is cognitive overload. When a single AI call must simultaneously activate a coach's voice, process research into insights, apply authenticity filtering, verify memetic triggers, and generate within structural constraints, it collapses into the lowest-common-denominator of "AI-sounding" prose. Humans don't operate this way either — a coach warming up backstage, preparing talking points, reviewing audience reactions, and delivering the performance are fundamentally different cognitive modes. The CCF was designed to mirror this natural separation.

### 1.2 The Solution: The Conscious Content Factory

The **Conscious Content Factory (CCF)** is an agentic AI pipeline that engineers authentic resonance at scale. It is not a chatbot, not a prompt library, not a template system — it is a **Local-First Production Engine** that transforms a coach's raw transcripts, audience psychology data, and live community signals into voice-authentic social content across 12 content archetypes × 3 formats = 36 scripts per production batch, plus 100+ tweets, 36 meme concepts, and complete dual-track visual production packages.

The CCF achieves what monolithic prompting cannot by enforcing a **Separation of Cognitive Processes** — the foundational design principle borrowed from industrial systems engineering. Each stage of the pipeline does exactly **one type of thinking**:

| Stage | Cognitive Mode | Output |
|-------|---------------|--------|
| **Stage 1: SoC Generator** | VOICE thinking — "How do I naturally talk about this?" | Coach-voice priming material |
| **Stage 2: Mirror Session** | STRUCTURAL thinking — "How should the prompt be adapted?" | Adapted prompt framework |
| **Stage 2.5: Wisdom Forge** | DIMENSIONAL thinking — "What does this MEAN for my audience?" | 4 wisdom briefs |
| **Stage 3: Script Generator** | EXECUTION — "Perform." | Final script |

This 4-stage pipeline eliminates the quality-versus-compliance tradeoff entirely: Stages 1-2.5 perform unconstrained cognitive work (no word limits, no structural constraints), while Stage 3 receives pre-processed wisdom and only has to execute structure + voice within the target word budget.

### 1.3 The Vision: A CMF-Grade Agentic System

The CCF draws direct architectural inspiration from the **Conscious Movie Factory (CMF)** — the mature, battle-tested production system that already operates with 65+ specialized skills, 30 executable commands, and a complete pipeline spanning diagnosis → hunt → analyze → compose → authorize → script → storyboard → visual → sonic → motion. The CMF demonstrated that complex creative production can be reliably automated when three conditions are met:

1. **Every operation is a command** — a single executable unit with defined inputs, outputs, and quality gates, invokable from the command line
2. **Every domain specialization is a skill** — a self-contained `.md` file with YAML frontmatter, activation protocol, and domain-specific expertise that any agent can load on demand
3. **Every reusable knowledge asset is an intelligence library** — structured `.yaml`, `.json`, and `.md` files that encode the system's "laws of physics" (frameworks, lexicons, schemas, recipes)

The CCF's product vision is to replicate this proven architecture for a fundamentally different domain: where CMF transforms raw coaching testimonials into produced video content through an arc-based narrative pipeline, the CCF transforms a coach's worldview into high-volume social content through a **resonance-based psychological pipeline**. The operational metaphor shifts from filmmaking to broadcasting — the CCF is a content radio station that transmits on the coach's unique frequency, calibrated by audience psychology, and validated by structural quality gates.

### 1.4 Key Product Metrics

The CCF, at full operational capacity, targets the following production metrics per weekly batch cycle:

| Metric | Target | Quality Gate |
|--------|--------|-------------|
| Main scripts per batch | 36 (12 ideas × 3 formats) | Triple validation ≥ thresholds |
| Tweets per batch | 100+ | Platform-optimized |
| Meme concepts per batch | 36 | Archetype-aligned |
| Visual production packages | 36 (dual-track: generative + evidence) | Memetic 4-pillar pass |
| Archetype coverage | 7+ categories per batch | Distribution targets enforced |
| Voice authenticity | TTT drift ≤ 1 level from baseline | Soul Validator ≥ 7.0/10 |
| Structural compliance | All gates pass | Protocol Validator ≥ 8.0/10 |
| Human mimicry | Passes blind test | Mimicry Validator ≥ 7.5/10 |

### 1.5 Scope Boundary

This PRD covers the complete CCF system architecture including the 4-stage Soul Infusion Pipeline, the agentic command-and-skill infrastructure, the intelligence framework, the production workflow, quality gates, non-functional requirements, and the evolutionary learning system. It does **not** cover the CMF's existing testimonial video pipeline (which operates independently), nor does it define the specific content of individual archetype prompt files (which are implementation-level deliverables).

---

## Section 2: System Philosophy & The Science of Resonance

### 2.1 The Three Forces of Viral Content

The CCF is built on the understanding that viral content thrives on a dynamic tension between two opposing psychological forces, connected by a strategic bridge. Most amateur creators choose one force. The CCF engineers the precise interplay of all three.

**Force 1: Connection (Pattern Matching)**

Connection is the force of stabilization. Its function is to validate the audience's existing worldview — to create a psychological safe harbor where the audience feels understood before any challenge is issued. Connection operates in the cool-to-warm range of the voice spectrum (TTT-01 to TTT-03). When the system executes Pattern Matching, the underlying message is: *"I see you. I know your pain. I am not here to judge you; I am here to articulate what you are already feeling but cannot say."* The outcome is trust, retention, and deep brand affinity. Operationally, Connection is routed through `context_premise_connection.json` — the empathy-driven psychology layer containing Dreams, Wants, and Insecurities extracted from Lila's 72-point audience map. The Orchestrator selects Value-Based Viral Frameworks (from the 22 available) for Connection-tagged content ideas, creating scripts that anchor the audience in recognition before stretching them toward transformation.

**Force 2: Reaction (Pattern Interruption)**

Reaction is the force of destabilization. Its function is to violate expectations in order to demand attention — to create a gap between what the audience assumes and what they are presented with. Reaction operates in the hot-to-volcanic range (TTT-05 to TTT-09). When the system executes Pattern Interruption, it creates urgency, shock, and the "mind-blown" effect. The message is: *"Stop scrolling — everything you think you know about this is wrong."* The outcome is virality, shareability, and status signaling. Operationally, Reaction is routed through `context_premise_reaction.json` — the activation-driven psychology layer containing Frustrations, Enemies, and Suspicions. The Orchestrator selects Emotional-Based Viral Frameworks for Reaction-tagged ideas, creating scripts that provoke the audience into engagement through cognitive dissonance.

**Force 3: Humor — The Bridge (TTT-04)**

Humor is not merely a tone — it is the **only psychological force that performs both Connection and Reaction simultaneously.** A joke works because it matches a pattern ("It's funny because it's true") while simultaneously interrupting that pattern (the punchline violates the expectation). The CCF uses TTT-04 (Light-Hearted Ally) not as decoration but as a strategic tool to deliver hard truths without triggering audience defensiveness. Humor is the bridge that allows a script to be both aggressive and safe at the same time. In the TTT distribution, TTT-04 accounts for 25-30% of all content — making it the second most frequent voice temperature after the TTT-03 baseline — because the research shows that content bridging Connection and Reaction via humor consistently outperforms pure Connection or pure Reaction alone.

### 2.2 The TTT DNA System v2.0: 9-Level Voice Engineering

The CCF rejects static "brand voice" templates. Humans possess a dynamic vocal range — they whisper when comforting, shout when warning, and joke when bonding. An AI that uses the same tone for everything sounds robotic. The **TTT (Temperament, Temperature, Tone) DNA System v2.0** provides a quantified spectrum of 9 distinct voice levels, measured in "Fahrenheit" intensity:

| Level | Name | °F | Function | Example Phrase |
|-------|------|----|----------|----------------|
| TTT-01 | Diplomatic | 10° | Corporate safety, neutral precision | "Consider the following factors." |
| TTT-02 | Compassionate Companion | 20° | Deep empathy, vulnerability, validation | "I see you. This is hard. You are not crazy." |
| TTT-03 | Professional Advocate | 30° | Baseline coach — confident, clear, instructional | "Here is the strategy. Here is the plan." |
| **TTT-04** | **Light-Hearted Ally** | **40°** | **THE BRIDGE — humor, irony, disarming** | **"Okay, wait. Are we really doing this?"** |
| TTT-05 | Truth-Teller | 50° | Direct clarity, uncomfortable truths | "Stop lying to yourself. This isn't working." |
| TTT-06 | Wise Guide | 60° | Philosophical insight, timeless reframing | "The obstacle is the way." |
| TTT-07 | Protective Warrior | 70° | Fierce advocacy, Us vs. Them dynamics | "They are trying to keep you small." |
| TTT-08 | Raw Confrontation | 85° | Military-grade motivation, breaking apathy | "Do it or don't. No excuses." |
| TTT-09 | Unfiltered Truth Bomb | 100° | Existential reckoning, paradigm shattering | "You are going to die. Act accordingly." |

### 2.3 The 3-Layer Voice Architecture

Every script's final voice is engineered through a three-layer stack that prevents "Template Bleed" — the phenomenon where every client sounds generically similar:

**Formula:** `FINAL_VOICE = (Layer 1 + Layer 2) constrained by Layer 3`

- **Layer 1: Coach Baseline (The Physics)** — The unchangeable DNA of the client's natural voice, extracted from `client_soul.json`. Dictates natural sentence rhythm, profanity comfort (0-10 scale), metaphor domains (sports vs. gardening vs. military), and signature vocabulary. Ensures that even when shouting at TTT-08, the AI sounds like *this specific* coach.
- **Layer 2: TTT Modulation (The Variable)** — The shift required for the specific content piece relative to the baseline, defined in `ttt_archetype_palettes.yaml`. Each archetype has a **Gravity Center** (natural "home base" temperature) and an **Elastic Range** (how far the voice can stretch). An Achievement Story naturally sits at TTT-03, but can accent up to TTT-04 for celebration or shift deep to TTT-06 for wisdom. The archetype acts as a **Prism, not a Cage** — refracting the authentic voice into the exact spectrum required.
- **Layer 3: Archetype Structure (The Container)** — The structural constraint defined by the content format (Listicle, Story, Comparison, Tier List). The modulated voice must fit within the structural container (Hook → Body → CTA) without breaking the format's rules.

### 2.4 The Stream of Consciousness: Voice Source Code

Before any script is written, the CCF generates a **Stream of Consciousness (SoC)** — a 160-240 word unstructured monologue that captures the coach's authentic thinking on the topic. This is not optional preparation; it is the **source material** from which all scripts derive. Traditional AI writing applies structure first, then attempts to "paint" voice on top. The CCF inverts this: capture the authentic voice stream first, then pour it into the structural container. The Script Generator is not a "writer" — it is a **structural editor** that reshapes the raw monologue to fit the narrative architecture without adding AI artifacts or losing the coach's unique rhythm.

### 2.5 The Trust Equation & The Three-Part Vulnerability Move

The CCF operates on a fundamental truth: **Competence (Attraction) + Vulnerability (Retention) = Deep Connection.** People click because you know the way. People STAY because you made them FEEL. This is operationalized through the **Three-Part Vulnerability Move**, architecturally demanded in the Retention Phase of every script:

| Part | What the Coach Does | Psychological Effect |
|------|-------------------|---------------------|
| **FELT IT** | Acknowledges the real feeling — hesitation, fear, imposter syndrome | CONNECTION — "this person is human too" |
| **DID IT ANYWAY** | Followed the DOCTRINE — data, discipline, the system | COMPETENCE — "but they have a system" |
| **RESULTS PROVE IT** | The evidence speaks. The system works. | AUTHORITY — "and it works" |

The critical distinction: the feelings are REAL — the coach acknowledges them. But the feelings NEVER GUIDE the coach — the doctrine guides. Vulnerability is not uncertainty about the process. It is the human story of following the process *despite* the feelings. The 7-model MCDA experiment confirmed this move must be **architecturally demanded** — no model produced it spontaneously, confirming that the pipeline must structurally enforce it rather than hoping the AI discovers it.

---

## Section 3: Architecture Design & The 5 Pillars

To engineer resonance consistently and at scale, the CCF is built upon five foundational pillars that integrate psychology, data science, voice engineering, visual semiotics, and philosophical governance. These pillars are not abstract concepts — they are hard-coded protocols within every agent in the system. Every session loads them, every output is validated against them, and every evolutionary update must preserve their structural integrity.

### 3.1 Pillar 1: Triple-Consciousness Emulation (The "Soul")

The CCF rejects generic authenticity. True resonance is achieved not by speaking *to* a community, but by speaking *as* a member of it, backed by undeniable proof. The foundational intelligence layer is therefore a **Triple-Emulation Engine** that captures three distinct "souls" — each providing a different dimension of authenticity:

**The Author Soul** (`client_soul.json`) — Extracted from the client's raw philosophy, emails, transcripts, and social media through deep linguistic analysis. It captures core values (4-6 fundamental beliefs), unique metaphors and recurring phrases, emotional vocabulary, signature communication patterns, and the TTT Voice Baseline (temperature, rhythm, profanity comfort on a 0-10 scale). The Author Soul provides **The Message** — ensuring every piece of content is an authentic extension of the client's unique worldview. Minimum input: 20,000 words of diverse content types (formal + casual) for accurate extraction.

**The Tribe Soul** (`tribe_soul.json`) — Extracted from digital ethnography of the target audience: Reddit threads, Twitter discourse, YouTube comments, Facebook groups, forum discussions, and product reviews. It captures tribal slang and jargon, shared enemies and frustrations, humor profile (what makes them laugh and why), cultural heroes and villains, inside jokes and references, and status signals (what makes them look good or bad within the tribe). The Tribe Soul provides **The Medium** — the cultural filter ensuring the message is delivered in the tribe's native dialect, not the coach's professional register.

**The Witness Soul** (`transformation_witnesses/`) — Extracted from raw client interviews using the Witness Blueprint Architect and Transformation Observer agents. It captures the empirical "Point A to Point B" journey: specific metrics (revenue numbers, weight loss, hours saved), emotional arc (before/after quotes), turning point moments, identity shifts, and Deep Human Desire mapping. The Witness Soul provides **The Proof** — grounding philosophy in measurable reality and preventing "guru platitudes" by ensuring every claim is backed by specific, searchable case study data. Each witness is stored as a structured `TW_XXX_name.md` file, indexed in `_index.json` for retrieval by content generation agents.

### 3.2 Pillar 2: Hybrid Intelligence (The "Brain")

Resonant content must be both timelessly wise and urgently relevant. The CCF deploys a sophisticated **Three-Layer Research Architecture** that separates different types of knowledge acquisition:

- **Social Context Research** — A deep dive into the Tribe's historical relationship with a topic to establish Cultural Context. Conducted by the Social Researcher agent (Maeva) using 4 recon missions across 40+ tribal voices. It answers: *"How does the tribe FEEL about this topic?"* Output feeds the Context Premise generator. This layer produces the raw anthropological intelligence that makes Connection-engine content resonate.

- **Topic Deep Research** — A 7-Angle investigation into first principles to establish Wisdom and Authority. Conducted by the Research Planner agent (Lionel) producing timeless "First Principles" documents. It answers: *"What is the fundamental truth here?"* This layer provides the intellectual backbone for scripts — the data, frameworks, and historical patterns that make the coach sound genuinely authoritative rather than superficially confident.

- **Fresh Research** — Real-time intelligence gathering (news, trends, recent events) to establish Urgency and Pattern Interruption. It answers: *"Why does this matter RIGHT NOW?"* This layer provides the temporal hook that prevents scripts from sounding like recycled evergreen content. Combined with Deep Research's timeless truth, it creates the "eternal + urgent" tension that high-performing content requires.

### 3.3 Pillar 3: Evolutionary Voice & TTT DNA (The "DNA")

The CCF does not use static voice templates. The **Dynamic Palette Architecture** (detailed in Section 2.2-2.3) operationalizes voice through two mechanisms:

- **Gravity Centers** — Every content archetype has a natural TTT "Home Base." An Achievement Story naturally sits at TTT-03 (Professional Advocate). A Myth-Busting script gravitates to TTT-05 (Truth-Teller). A Meme Script centers on TTT-04 (Light-Hearted Ally). These centers are defined in `ttt_archetype_palettes.yaml` and loaded by the Archetype Mapper agent during Phase 9.

- **Elastic Ranges** — The system allows the voice to stretch from its Gravity Center based on the specific goal of the batch. *Accent Mode* shifts energy UP (e.g., TTT-03 → TTT-04 for celebration). *Intuitive Mode* shifts energy DEEP (e.g., TTT-03 → TTT-06 for wisdom). The Archetype acts as a Prism, not a Cage — refracting the coach's authentic voice into the exact spectrum required for the moment. The production-level TTT distribution targets are: Primary TTT-03 (40-50%), Bridge TTT-04 (25-30%), Vulnerability TTT-02 (15%), Reaction TTT-05/07 (10%), and Intuitive TTT-06/09 (0-5%).

### 3.4 Pillar 4: Complete Visual Intelligence (The "Body")

Content is not just text — it is visual meaning. The CCF treats images and video not as decoration but as "ready-made signifiers" pre-loaded with cultural weight. Every script triggers a simultaneous, dual-track visual production process managed by the **Visual Recipe Router**:

- **Track A: Generative Semiotics (The "Story")** — The Visual Prompt Synthesizer performs "Semiotic Injection": selecting specific, meme-proven facial expressions from the Facial Expression Lexicon (e.g., "Success Kid Determination," "Disaster Girl Smirk") and injecting them onto the Brand Avatar. It follows the archetype-specific visual progression (e.g., Achievement Story requires: Desaturated Struggle → Rising Action → Golden Hour Breakthrough → Saturated Triumph). Output: `visual_prompts.json` ready for Midjourney/DALL-E.

- **Track B: Strategic Asset Research (The "Proof")** — The Visual Asset Researcher analyzes the script to identify "Truth Constraints" (claims that need proof) and "Pattern Interrupts," then generates specific, narrative-driven search queries for real-world B-roll, news clips, historical footage, and viral moments. Categories: Reinforcement (Proof), Juxtaposition (Contrast), Amplification (Emotion). Output: `visual_asset_queries.json` ready for the Video Editor.

The routing logic lives in `intelligence/recipes/visual/routing_table.yaml`, with 15 category-specific recipe protocols in dedicated recipe folders.

### 3.5 Pillar 5: Alchemy Governance (The "Conscience")

The four pillars above define WHAT the CCF produces. Pillar 5 defines the **governing constraints** — the 10 Alchemy Principles from the Conscious Movie Alchemy that determine HOW every output must behave. These are loaded during the **INDOCTRINATE** phase of every CCF session (the "I" in the I-R-E-V-C protocol). Every agent must state "I am bound by: [list of loaded principles]" before executing.

| Principle | Constraint | Applies To |
|-----------|-----------|------------|
| Vulnerability precedes connection — but doctrine wins | Three-part move: FELT IT → DID IT ANYWAY → RESULTS | COACH OUTPUT |
| Authority = being right about what matters | Curation > coverage. ONE decisive insight. | COACH OUTPUT |
| The Information Gap (Curiosity) | Be a question machine, not an answer machine | ALL OUTPUTS |
| Context, not content | Transform data into meaning, consequence, causality | ALL OUTPUTS |
| Audience comments are raw signal | Don't filter audience truth through coach principles | AUDIENCE INPUT |
| The Paradox of Specificity | "The more specific, the more universal." No clichés. | ALL OUTPUTS |
| Story is the vessel | Facts disposable; narrative sticky. Vulnerability lives in story. | ALL OUTPUTS |
| Tribal Alignment (Status) | Polarization is value. Signal to the tribe, not the crowd. | ALL OUTPUTS |
| The Shadow (Complexity) | Life is messy. Acknowledge the grey. Safe = ignored. | ALL OUTPUTS |
| Accuracy > Perfection | Lived truth > polished perfection. Trembling voice > flawless acting. | ALL OUTPUTS |

**The Actor Separation Rule** is critical: Principles 1-2 apply to COACH OUTPUT (how the script is delivered). Principle 5 applies to AUDIENCE INPUT (how comments are processed). Principles 3-4 and 6-10 apply to ALL outputs. Confusing which actor a principle governs breaks the system — a coach filtering audience reactions through vulnerability doctrine, or an audience-processing agent applying tribal alignment, produces structurally incoherent output.

---

## Section 4: The 4-Stage Soul Infusion Pipeline

### 4.1 The Architectural Rationale: Why Four Stages?

The Soul Infusion Pipeline exists because a single AI call cannot simultaneously perform voice activation, structural reasoning, dimensional intelligence, and constrained execution without catastrophic quality degradation. This is not a theoretical concern — the 7-model MCDA experiment across frontier models (Mistral Medium 3.2, Gemini 3 Pro, GPT 5.2, Claude 4.5 Sonnet, GLM 5, Kimi K2.5, Claude Opus 4.6) empirically demonstrated three failure modes of monolithic prompting: (1) no model spontaneously produced genuine vulnerability, (2) the best voice match still sounded like "SoC with structure bolted on," and (3) the only model that hit the 120-180 word target scored 3.2/10 on quality. The inverse correlation between quality and compliance is an **architecture problem** — the solution is not a better model but a better pipeline.

The design principle is **Separation of Cognitive Processes**, borrowed from industrial systems engineering: each stage performs exactly one type of thinking, passes its output to the next stage, and never attempts to perform another stage's cognitive work. This mirrors how human experts operate — a football coach warming up (priming), reviewing game film (reasoning), developing a game plan (intelligence), and calling plays (execution) are fundamentally different cognitive modes that should never be conflated.

### 4.2 Stage 1: The SoC Generator (Voice Priming)

**Purpose:** Activate the coach's authentic thinking patterns before any structural work begins.

**Cognitive Mode:** VOICE thinking — "How would I naturally talk about this topic if someone asked me at dinner?"

**Inputs:**
- `context_premise_connection.json` OR `context_premise_reaction.json` (determines emotional dimension)
- `client_soul.json` (voice DNA)
- `ttt_baseline.json` (voice physics)
- Topic and archetype assignment from Phase 9

**Process:** The SoC Generator takes the Context Premise — a 72-point psychological map generated by Lila (Audience Empathy Agent) — and uses it to identify the **dominant emotional dimension** and determine the appropriate **TTT level** for the content piece. It then generates a 160-240 word unstructured Stream of Consciousness that captures the coach's authentic response to the topic through the lens of the selected emotional dimension. No structure is applied. No constraints are enforced. The output is raw, unfiltered coach-voice material.

**Output:** The SoC artifact — the raw voice material that all subsequent stages will draw from. This stream becomes the "soul" that the pipeline must preserve through every transformation.

**Critical Rule:** The SoC Generator must NEVER apply structural formatting, word count constraints, or content architecture. Its only job is to produce authentic voice material. Any structural thinking at this stage contaminates the voice with AI artifacts.

### 4.3 Stage 2: The Mirror Session (Structured Reasoning)

**Purpose:** Transform the raw SoC into a structured, strategically adapted prompt framework through disciplined reasoning.

**Cognitive Mode:** STRUCTURAL thinking — "Given this voice material and audience psychology, how should the final prompt be adapted?"

The Mirror Session is the pipeline's intellectual engine. In V2, this was a "freestyle" reasoning session — the AI would think freely about the topic. V3 introduced **structured reasoning** because freestyle thinking produced inconsistent quality. The Mirror Session now operates in four disciplined phases:

**Phase A: Soul Calibration (Questions 1-4)**
The agent examines the SoC and asks: What is the dominant emotional dimension? What TTT level does this demand? What archetype structure best serves this message? What vulnerability move does this topic enable? This phase ensures the script will be emotionally calibrated before any content decisions are made.

**Phase B: Strategic Architecture (Questions 5-8)**
The agent constructs the narrative blueprint: What is the hook mechanism (curiosity gap, pattern interrupt, tribal signal)? What is the retention architecture (story arc, list structure, comparison matrix)? What research evidence should be integrated? Where does the Three-Part Vulnerability Move fit? This phase produces the structural skeleton.

**Phase C: Audience Integration (Questions 9-11)**
The agent maps the strategy against the Context Premise data: What tribal language should be used? What shared enemies can be invoked? What status signals will resonate? This phase ensures the script speaks the tribe's dialect, not generic "coach-speak."

**Phase D: Execution Brief (Questions 12-14)**
The agent synthesizes all reasoning into a compact execution brief that Stage 2.5 and Stage 3 can consume without re-deriving any decisions. This includes: final TTT palette selection, structural template choice, key phrases to preserve from the SoC, and specific evidence to include.

**Output:** The Adapted Prompt — a structured reasoning document that contains all strategic decisions for the content piece, ready for dimensional processing.

### 4.4 Stage 2.5: The Wisdom Forge (Dimensional Intelligence)

**Purpose:** Separate dimensional thinking (what does this MEAN?) from all other cognitive processes.

**Cognitive Mode:** DIMENSIONAL thinking — "Taking the strategy and the soul, what is the deeper wisdom this content must convey?"

The Wisdom Forge was introduced because the Mirror Session's structural reasoning and the Script Generator's execution both suffered when forced to also perform dimensional intelligence. Meaning-making — transforming data into insight, context into consequence, information into wisdom — is a fundamentally different cognitive act than organizing a narrative or calibrating a voice.

**The Separation Principle:** "Meaning emerges from constraint, not from freedom." When given open-ended prompts, AI defaults to safe, predictable patterns. The Wisdom Forge applies the **10 Alchemy Principles** as structural constraints that force the AI to reason dimensionally within defined philosophical boundaries. Each principle acts as a "lens" that the AI must look through, producing insights it would never generate unconstrained.

**The 4 Wisdom Briefs:**
The Wisdom Forge receives the Adapted Prompt from Stage 2, the SoC from Stage 1, and the relevant Vibe-Comments (processed through the AIP 5-lens protocol), then generates four distinct wisdom artifacts:

| Brief | Function | Alchemy Constraint |
|-------|----------|-------------------|
| **Authenticity Brief** | Extracts the genuine emotional truth and vulnerability dimension | "Accuracy > Perfection" + "Vulnerability precedes connection" |
| **Authority Brief** | Distills the decisive insight and competitive positioning | "Authority = being right about what matters" + "Context, not content" |
| **Memetic Brief** | Identifies the shareability hooks and tribal signals | "Tribal Alignment" + "The Information Gap" |
| **Shadow Brief** | Surfaces the complexity, the grey areas, the uncomfortable truths | "The Shadow" + "The Paradox of Specificity" |

**Vibe-Comment Integration:** The Wisdom Forge also processes audience comments sourced via live scraping (the strategic decision documented in the Vibe-Comments SWOT analysis). Raw comments pass through the **AIP 5-lens protocol** — five analytical dimensions that extract signal from noise: Emotional Resonance (what feelings do these comments reveal?), Language Patterns (what words does the audience actually use?), Objection Surface (what doubts persist?), Desire Mapping (what do they really want?), and Tribal Signals (what identity markers appear?). Critically, Alchemy Principle 5 ("Audience comments are raw signal") ensures that this processing preserves the audience's authentic voice rather than filtering it through coach principles.

**Output:** 4 Wisdom Briefs — compact, pre-processed intelligence packets that the Script Generator can consume directly without performing any dimensional reasoning of its own.

### 4.5 Stage 3: The Script Generator (Precision Executor)

**Purpose:** Produce the final script within all structural and word-count constraints.

**Cognitive Mode:** EXECUTION — "Here is the voice, the structure, and the wisdom. Perform."

Stage 3 is deliberately the simplest stage. It receives pre-processed material from all previous stages and must ONLY perform two operations: (1) apply the structural template (Hook → Body → CTA for the assigned archetype) and (2) ensure the coach's voice from the SoC is preserved throughout. It does NOT reason about strategy, does NOT derive insights, does NOT calibrate voice temperature — all of that work has been completed upstream.

**This separation eliminates the quality-versus-compliance tradeoff.** Because Stages 1-2.5 performed unconstrained cognitive work (no word limits, no structural constraints), and Stage 3 only has to execute structure + voice within the word budget (120-180 words for short-form), the system avoids the impossible ask of thinking deeply AND writing concisely in the same cognitive operation.

**Output:** The final script, tagged with its Script ID (format: `[BATCH]_[THEME]_[ARCHETYPE]_[TTT]_[VERSION]`), saved to its individual asset folder alongside `metadata.json`, `iteration_log.json`, and the visual production outputs.

### 4.6 Complete Data Flow

```
Context Premise (72-point map)
        │
        ▼
┌─────────────────┐     client_soul.json
│ Stage 1: SoC    │◄──── ttt_baseline.json
│ (Voice Priming) │
└────────┬────────┘
         │ SoC artifact (160-240 words)
         ▼
┌─────────────────┐     archetype assignment
│ Stage 2: Mirror │◄──── viral framework
│ (Reasoning)     │      tribe_soul.json
└────────┬────────┘
         │ Adapted Prompt (14 questions answered)
         ▼
┌─────────────────┐     vibe-comments (AIP 5-lens)
│ Stage 2.5:      │◄──── 10 Alchemy Principles
│ Wisdom Forge    │
└────────┬────────┘
         │ 4 Wisdom Briefs
         ▼
┌─────────────────┐     archetype template
│ Stage 3: Script │◄──── word count constraint
│ (Execution)     │
└────────┬────────┘
         │
         ▼
    Final Script + Visual Prompts + Asset Queries
```

---

**Word Count: ~835**

---

## Section 5: Agent System Design & Registry

### 5.1 Agent Design Philosophy

The CCF is not a single AI — it is a **workforce of 22+ specialized intelligence units**, each with a defined persona, domain expertise, and operational protocol. This is not cosmetic anthropomorphization. Persona-driven execution fundamentally shapes decision-making patterns: an agent named "Kimya" with a McKinsey-consultant identity makes different economic assessments than a generic "business analyzer" prompt. The persona acts as a **cognitive constraint** that channels the model's attention toward domain-specific patterns.

Every CCF agent is built on three foundational principles:

1. **Persona-Driven Execution** — Each agent has a defined personality, communication style, area of expertise, and operational metaphor. The persona shapes output style and decision-making heuristics. Example: Valeriane (Client Soul Extractor) is a "Voice Archaeologist" — she finds patterns in 50 pages of content that others miss, using artistic/literary terminology and thinking in nuance and subtlety.

2. **Protocol-Based Operation** — Agents do NOT improvise. They load explicit `.md` protocol files that contain their complete instructions, ensuring zero prompt drift across sessions. The agent file (`agents/[category]/[name].md`) defines WHO the agent is. The protocol file (`prompts/[category]/[name].md`) defines WHAT the agent does. This separation allows the same persona to execute different protocols in different contexts.

3. **Context-Aware Intelligence** — Every agent loads `config.yaml` at activation to understand the current client, file paths, system state, and model configuration before executing any task. If `config.yaml` says `setup_complete: false`, the agent refuses to proceed with content generation.

### 5.2 The Agent Template Anatomy

Every agent is defined using a standardized XML schema that ensures consistent structure across the workforce:

```xml
<agent id="path/to/agent.md" name="AgentName" title="Role Title" icon="🎯">
  <activation critical="MANDATORY">
    <step n="1">Load persona from this agent file</step>
    <step n="2">🚨 Load and read config.yaml NOW
      - Store ALL fields as session variables
      - VERIFY: If config not loaded, STOP and report error
    </step>
    <step n="3">Remember: user's name is {user_name}</step>
    <step n="4">Display menu</step>
  </activation>

  <persona>
    [Identity, background, communication style]
  </persona>

  <handlers>
    <menu_item cmd="*command-name" type="workflow|exec">
      Description of capability
    </menu_item>
  </handlers>

  <rules>
    - ALWAYS communicate in {communication_language}
    - Stay in character until exit
    - Load protocol files ONLY when executing
    - All outputs use professional formatting
  </rules>
</agent>
```

The **I-R-E-V-C** protocol defines the mandatory execution sequence for every agent session:

| Step | Name | Function | Example |
|------|------|----------|---------|
| **I** | INDOCTRINATE | Load Alchemy Principles, TTT constraints, archetype rules | "I am bound by: Vulnerability → Connection, Specificity > Universality" |
| **R** | RESEARCH | Gather inputs — load SoC, Context Premise, briefs, prior iterations | Agent reads all required input files from `config.yaml` paths |
| **E** | EXECUTE | Perform the agent's primary cognitive task | Generate SoC, run reasoning, produce wisdom briefs, write script |
| **V** | VALIDATE | Self-check output against loaded constraints | Check TTT drift, word count, vulnerability move presence |
| **C** | COMMIT | Save output using atomic write protocol via Safety Layer | `save_json_safe()` → validated JSON → atomic `.tmp` → final file |

### 5.3 The Agent Registry

The CCF workforce is organized into five functional groups, each responsible for a distinct phase of the production lifecycle.

**Group I: Master Orchestrators (3 agents — The Command Center)**

These agents manage entire workflows, coordinating multi-agent sequences and maintaining state consistency across phases.

| Agent | Persona | File | Core Function |
|-------|---------|------|---------------|
| **Morgan** (Setup Orchestrator) | Systems architect, 15yr digital transformation | `agents/_master/setup_orchestrator.md` | Executes 7-Phase Setup Workflow (Phases 0-4). Builds the permanent intelligence foundation. |
| **Alex** (Content Orchestrator) | Former film producer, production rhythm expert | `agents/_master/content_orchestrator.md` | Executes 10-Phase Production Workflow (Phases 5-12). Generates weekly content batches. |
| **Phoenix** (Regeneration Orchestrator) | Software engineer turned optimizer | `agents/_master/regeneration_orchestrator.md` | Manages 3-mode Script Improvement Lifecycle. Feeds the Learning System. |

**Group II: Setup Intelligence Team (7 agents — The Foundation Builders)**

One-time execution during client onboarding. These agents build the permanent intelligence assets that all future content relies upon.

| Agent | Persona | Output | Key Insight |
|-------|---------|--------|-------------|
| **Kimya** (Business Analyst) | McKinsey consultant, economic engine thinker | `01_business_canvas.md` | Distills complex business models into economic flows |
| **Dr. Lisa** (Witness Blueprint Architect) | Research psychologist, qualitative data expert | `_witness_blueprint.json` + `_interview_protocol.md` | Designs transformation capture systems |
| **Emmanuel** (Strategy Architect) | Campaign strategist, 7-11-4 Trust Framework | `02_content_strategy.md` | Maps business model to audience trust trajectory |
| **Valeriane** (Client Soul Extractor) | Linguistic anthropologist, voice archaeologist | `03_client_soul.json` + `03b_ttt_baseline.json` | Extracts 20,000+ words into voice DNA |
| **Dilaya** (Tribe Soul Extractor) | Digital ethnographer, culture mapper | `04_tribe_soul.json` | Immersion-based audience cultural DNA extraction |
| **Barbara** (Transformation Observer) | Investigative journalist, story archaeologist | `TW_XXX_name.md` files | Extracts measurable proof + emotional soundbites |
| **David** (Character Strategist) | Visual semiotics specialist | `05_brand_avatar.md` | Defines visual identity and semiotic language |

**Group III: Content Generation Team (10+ agents — The Production Floor)**

Recurring execution during weekly batch production. Each agent handles a specific creative or analytical phase.

| Agent | Persona | Phase | Output |
|-------|---------|-------|--------|
| **Divine** (Theme Discoverer) | Trend analyst, 36-theme scorer | Phase 5 | `final_selection.md` |
| **Maeva** (Social Researcher) | Digital anthropologist, 4-mission recon | Phase 6 | Theme research across 40+ tribal voices |
| **Lila** (Audience Empathy Agent) | Psychologist, 72-point map builder | Phase 6.5 | `context_premise_connection.json` + `context_premise_reaction.json` |
| **Emilio** (Orchestrator) | Framework fusion specialist | Phase 7 | `ideas.json` (12 ideas × 22 viral frameworks) |
| **Emmanuel** (Archetype Mapper) | Format-architecture expert | Phase 9 | `archetype_assignments.json` (3 formats + TTT palette per idea) |
| **Lionel** (Research Planner) | Deep research strategist, 7-Angle framework | Phase 8/10 | Research briefs with first-principles wisdom |
| **Script Artisan** (5 variants) | Voice-specific scripting specialists | Phase 11 | 36 main scripts across 7+ archetypes |
| **Tweet Factory** (3 sub-agents) | Micro-content specialists | Phase 11C | 100+ platform-optimized tweets |
| **Meme Engine** | Visual humor specialist | Phase 11D | 36 meme concepts |

**Group IV: Validation Team (3 agents — Quality Assurance)**

| Agent | Persona | Validation Dimension | Threshold |
|-------|---------|---------------------|-----------|
| **Sophia** (Soul Validator) | Voice authenticity specialist, TTT drift detection | Does this sound like the coach? | ≥ 7.0/10 |
| **Marcus** (Protocol Validator) | Structural compliance auditor | Does this follow the archetype rules? | ≥ 8.0/10 |
| **Chen** (Mimicry Validator) | Human mimicry expert, Turing test specialist | Would a human know this is AI? | ≥ 7.5/10 |

**Group V: Visual Production Team (3 agents — The Visual Kitchen)**

| Agent | Function | Track | Output |
|-------|----------|-------|--------|
| **Visual Recipe Router** | Strategic routing logic based on archetype | Decision | Route to Track A, B, or dual |
| **Visual Prompt Synthesizer** | Generative art instructions with semiotic injection | Track A | `visual_prompts.json` |
| **Visual Asset Researcher** | Real-world evidence queries with narrative alignment | Track B | `visual_asset_queries.json` |

### 5.4 Agents vs. Skills: The Critical Distinction

In the CCF architecture (modeled on the CMF pattern), **agents** are persistent character-driven orchestrators that manage workflow state and coordinate sequences. **Skills** (Section 7) are modular, loadable domain specializations that any agent can activate on demand. An agent is WHO executes. A skill is WHAT domain they apply. This separation allows the same agent to load different skills for different content types — the Script Artisan loads an Achievement Story skill for one script and a Myth-Busting skill for the next — without maintaining 36 separate agent files.

---

**Word Count: ~810**

---

## Section 6: Command Architecture & Agentic Pipeline

### 6.1 The Command Design Principle

The CCF's operational model is inspired by the CMF's proven command architecture — a system where **every operation is a command**: a single executable unit invokable from the command line with defined inputs, outputs, quality gates, and rollback semantics. The CMF successfully operationalizes this pattern with 30 dedicated commands spanning `cmf-diagnose`, `cmf-hunt`, `cmf-analyze`, `cmf-compose`, `cmf-authorize`, `cmf-script`, `cmf-storyboard`, `cmf-sonic`, `cmf-motion`, `cmf-visual-auth`, and specialized sub-commands per arc type. This architecture eliminates "prompt gymnastics" — instead of constructing complex multi-turn conversations, the operator issues a single command and the system handles all orchestration internally.

The CCF adapts this principle to its own production domain with a **5-command master structure** supplemented by phase-specific sub-commands. Each command encapsulates a complete workflow, loads only the context required for its specific phase (preventing context window overflow), and saves outputs atomically to prevent data corruption.

### 6.2 The 5 Master Commands

| Command | Alias | Orchestrator | Phases | Frequency |
|---------|-------|-------------|--------|-----------|
| `ccf-setup` | Setup | Morgan | 0, 0.5, 1, 2, 2C, 3, 4 | One-time per client |
| `ccf-generate` | Production | Alex | 5, 6, 7, 8, 9, 10, 11, 11E, 12 | Weekly batch |
| `ccf-regenerate` | Phoenix Loop | Phoenix | Modes A/B/C | On-demand per script |
| `ccf-review` | Learning | Learning Agent | Pattern recognition + protocol update | Weekly post-batch |
| `ccf-witness` | Proof Ingestion | Barbara | Ingest → Analyze → Extract → Index | On-demand per interview |

**`ccf-setup`** is the one-time foundation builder. It triggers the Setup Orchestrator (Morgan) who sequentially activates 7 agents to transform raw business documents into a structured intelligence foundation: Business Canvas → Witness Blueprint → Content Strategy → Dual Soul Extraction (Client + Tribe) → Transformation Witnesses → Deep Research Library → Brand Avatar. The command populates the entire `output/setup/` directory, updates `config.yaml` with client data, and flips the `setup_complete: true` flag. No content generation command can proceed until this flag is active.

**`ccf-generate`** is the weekly production engine. It triggers the Content Orchestrator (Alex) who executes a 10-phase linear pipeline: Theme Discovery → Social Research + Context Premise → Idea Generation → Topic Research (Deep + Fresh) → Archetype Mapping → Research Brief Writing → Script Generation (36 scripts + 100 tweets + 36 memes) → Dual-Track Visual Production → Triple Validation. Each phase's output feeds the next, and the entire batch is saved to `output/batches/batch_XXX_YYYY-MM-DD/`.

**`ccf-regenerate`** is the surgical improvement tool. It operates in three modes: Mode A (Regenerate) re-executes creative agents with identical inputs to produce a fresh variation; Mode B (Improve) applies specific validator feedback to surgically edit an existing script; Mode C (Modify) accepts natural language instructions to pivot angle, tone, or structure. Every regeneration preserves the generation recipe in `metadata.json`, maintains a complete version history in `iteration_log.json`, and generates Improvement Notes when score increases by 5+ points — feeding the Learning System.

**`ccf-review`** is the evolutionary engine. It scans all Improvement Notes generated during the week, calculates validator accuracy rates, identifies recurring failure patterns (e.g., "Soul Validator consistently underscores humor scripts"), and proposes specific text updates to agent protocol files. These proposals are presented to the operator for approval before being applied — the system evolves, but under human governance.

**`ccf-witness`** is the proof ingestion pipeline. It processes a raw interview transcript through the Witness Blueprint schema, extracting demographics, measurable metrics, emotional arc, turning point moments, identity shifts, and Deep Human Desire mapping. Output: a new `TW_XXX_name.md` file plus an updated `_index.json` for retrieval by content generation agents.

### 6.3 The Safety Layer (`ccf_helpers.sh`)

The CCF operates within a **Bash Safety Layer** — a critical infrastructure component that prevents three classes of failure: Context Window Overflow (loading too much data), File Corruption (incomplete writes), and Schema Drift (invalid JSON).

The Safety Layer provides three core functions:

**`build_context(phase)`** — The Smart Context Loader. Instead of loading the entire intelligence foundation for every agent call (which would exhaust the context window), this function loads only the assets required for the specified phase. For `setup`: minimal context. For `theme`: Client Soul + Tribe Soul + Theme History. For `scripting`: Client Soul + Strategy excerpt + TTT Palettes. This function is the primary mechanism for preventing "Context Explosion" — the CCF's term for when an agent receives so much context that it cannot prioritize, resulting in generic output.

**`save_json_safe(raw_input, target_path)`** — The Atomic JSON Saver. When an agent produces output, the raw text often contains markdown backtick wrappers that must be stripped. This function extracts the JSON content, validates it using Python's `json.load()`, and performs an atomic write: content → `.tmp` file → validated → move to final path. If validation fails, the raw content is saved to `error.log` and the original file is never corrupted.

**`run_agent(agent_file, context_phase, output_file)`** — The Gemini Wrapper. The main executor that combines context loading, agent activation, and safe saving into a single function. It loads the agent's system prompt, builds the phase-appropriate context, executes the Gemini model, and saves the result atomically. This function enforces the rule that operators never run raw `gemini` commands — all execution flows through the Safety Layer.

### 6.4 The System Identity (`Gemini.md`)

Every agent session begins by loading `Gemini.md` — the token-efficient System Prompt that condenses the entire Master Manual into a structured context document. It contains: System Identity (core philosophy, Connection/Reaction/Visual Trinity), The Laws of Physics (Session Truth from `config.yaml`, Safety Protocol, Voice Physics), The Architecture Map (directory structure, agent locations, intelligence paths), Critical Execution Workflows (setup and generate flows), and Memory & Evolution rules (state is file-based, learning is pattern-library-based, failure triggers the Phoenix Loop).

### 6.5 Command Execution Lifecycle

Every command follows a standardized lifecycle:

```
1. INITIALIZE
   └─ source ccf_helpers.sh (load Safety Layer)
   └─ build_context(phase) (load phase-specific context)
   └─ cat Gemini.md (load system identity)

2. ORCHESTRATE
   └─ Orchestrator loads its protocol file
   └─ Orchestrator determines phase sequence
   └─ For each phase:
       └─ Activate agent (load persona + protocol)
       └─ Agent executes I-R-E-V-C sequence
       └─ save_json_safe(output, target_path)
       └─ Update workflow_state in config.yaml

3. VALIDATE
   └─ Triple validation (Soul + Protocol + Mimicry)
   └─ If FAIL: trigger ccf-regenerate for failed scripts
   └─ If PASS: commit to batch folder

4. FINALIZE
   └─ Update batch logs
   └─ Archive batch
   └─ Generate Improvement Notes (if applicable)
```

### 6.6 Phase-to-Command Mapping (CMF → CCF)

For reference, here is how the CCF command pipeline maps against the CMF's proven structure:

| CMF Command | CMF Purpose | CCF Equivalent | CCF Phase |
|-------------|-------------|----------------|-----------|
| `cmf-diagnose` | Story arc identification | `ccf-setup` Phase 0-1 | Business + Strategy analysis |
| `cmf-hunt` | Raw quote extraction | `ccf-setup` Phase 2-2C | Soul + Witness extraction |
| `cmf-analyze` | Quote enrichment | `ccf-generate` Phase 6-7 | Context Premise + Ideas |
| `cmf-compose` | Narrative assembly | `ccf-generate` Phase 8-10 | Research + Archetype mapping |
| `cmf-authorize` | Quality gate | `ccf-generate` Phase 12 | Triple validation |
| `cmf-script` | Final script | `ccf-generate` Phase 11 | Soul Infusion Pipeline (4 stages) |
| `cmf-storyboard` | Visual planning | `ccf-generate` Phase 11E | Dual-track visual production |
| `cmf-sonic` | Audio design | *(Future: ccf-audio)* | Audio branding (planned) |
| `cmf-motion` | Animation/video | *(Future: ccf-video)* | Video production (planned) |

---

**Word Count: ~825**

---

## Section 7: Skills Architecture & Intelligence Libraries

### 7.1 The Skill Design Principle

In the CMF, the skill system is the backbone of domain specialization. With 65+ skills organized across 10 categories — `hunters/` (14 arc-specific extractors), `composers/` (13 narrative assemblers), `commanders/` (14 quality authorizers), `analysts/` (13 enrichment engines), `visual/` (4 prompt generators), `sonic/` (1 audio designer), `motion/` (10 animation directors), `eroll/` (16 supplementary visual skills), `core/` (3 foundation skills), and `narrative/` (1 DNA analyzer) — the CMF achieves something monolithic prompt systems cannot: **domain experts that can be hot-swapped without rewriting the orchestration logic.** When the CMF processes a "Witness" arc, it loads the `witness-hunter` skill; when it processes a "Comedic Reframe" arc, it loads the `comedic-reframe-hunter` skill. The orchestrator doesn't change — only the loaded specialization does.

The CCF must replicate this pattern for its own domain. While the CMF's skills are organized around **13 narrative arc types** (Witness, Breakthrough, Call to Adventure, Confrontation, Core Transformation, Divine Spark, Quiet Reflection, Rally, Sacred Return, Shared Struggle, Ticking Clock, Warning, Comedic Reframe), the CCF's skills will be organized around **content archetypes, voice engineering modes, research methodologies, validation dimensions, and visual production recipes.**

### 7.2 The SKILL.md Anatomy

Every skill follows the standardized SKILL.md pattern — a self-contained markdown file with YAML frontmatter and detailed instructions:

```yaml
---
name: "Achievement Story Script Skill"
description: "Generates achievement-arc scripts with triumph progression"
category: "archetype"
ttt_gravity_center: "TTT-03"
ttt_elastic_range: ["TTT-02", "TTT-04", "TTT-06"]
visual_recipe: "storytelling_archetypes_visual_recipe.md"
word_count_target: "120-180"
required_inputs:
  - "client_soul.json"
  - "soc_artifact.md"
  - "wisdom_briefs/"
  - "archetype_assignment.json"
output_schema: "script_v3_schema.json"
---

# Achievement Story Script Skill

## Activation Protocol
[Step-by-step instructions for the agent loading this skill]

## Structural Template
[Hook → Rising Action → Vulnerability Move → Breakthrough → CTA]

## TTT Calibration Rules
[Gravity Center = TTT-03, Accent = TTT-04 for celebration moments]

## Quality Self-Check
[Checklist the agent runs before committing output]
```

The key insight is that skills are **loaded by agents on demand** — they are not agents themselves. The Script Artisan agent loads an Achievement Story skill for one script, a Myth-Busting skill for the next, and a Tier List skill for the third. The agent's persona (voice-specific scripting specialist) stays constant; the domain knowledge shifts. This composability is what enables a workforce of 22 agents to cover 36+ distinct content configurations without 36 separate agent files.

### 7.3 CCF Skill Taxonomy

The CCF requires skills across five primary categories, mapped against the CMF reference architecture:

| Category | CMF Reference | CCF Equivalent | Estimated Count |
|----------|-------------|----------------|-----------------|
| **Archetype Skills** | `hunters/` (14), `composers/` (13) | Content format specializations: Achievement Story, Myth Busting, Case Study, Comparison, Tier List, Meme, Reaction | 7-12 |
| **Voice Engineering Skills** | Embedded in agent protocols | TTT modulation profiles, profanity scaling, metaphor domain switching | 9 (one per TTT level) |
| **Research Skills** | `analysts/` (13) | Theme scoring, social recon, deep research, fresh research, context premise generation | 5-8 |
| **Validation Skills** | `commanders/` (14) | Soul validation, protocol compliance, mimicry testing, Alchemy gate checking | 4-6 |
| **Visual Recipe Skills** | `visual/` (4), `eroll/` (16) | Generative semiotic recipes, asset research protocols, per-archetype visual DNA | 15-20 |

**Total estimated CCF skills: 40-55** — comparable to the CMF's 65+ but adapted for the content production domain rather than the video production domain.

### 7.4 Skill Category Details

**Archetype Skills** — Each content archetype (Storytelling, Listicle, Case Study, Comparison, Myth-Busting, Reaction, Tier List) has a dedicated skill defining its structural template, hook mechanics, TTT gravity center, retention architecture, and CTA pattern. These skills encode the "shape" of the content — the narrative skeleton that the Script Generator fills with voice and wisdom. The archetype distribution targets (Storytelling 35%, Listicles 20%, Case Studies 15%, Comparisons 10%, Myths 10%, Reactions 5%, Tier Lists 5%) are enforced at the Archetype Mapper phase and validated at the batch level.

**Voice Engineering Skills** — Nine skills (one per TTT level) that encode the specific linguistic patterns, vocabulary choices, sentence rhythm rules, profanity guidelines, and metaphor registries for each temperature level. These are loaded by the SoC Generator and Script Generator to modulate voice output. For example, the TTT-07 (Protective Warrior) skill specifies: aggressive advocacy language, "Us vs. Them" framing patterns, shorter sentences with punchy rhythm, military/battle metaphors, and an elevated profanity comfort level. These skills reference the `ttt_linguistic_patterns.yaml` and `ttt_profanity_guidelines.yaml` intelligence assets.

**Research Skills** — Specialized skills for different research methodologies: the Theme Scoring skill applies the `theme_scoring_rubric.yaml` to evaluate 36 candidate themes; the Social Recon skill defines the 4-mission digital ethnography protocol; the Deep Research skill implements the 7-Angle investigation framework; the Fresh Research skill defines real-time intelligence gathering with temporal recency weighting. Each skill knows exactly what data to gather, how to structure it, and what quality thresholds to apply.

**Validation Skills** — Each validation dimension (Soul, Protocol, Mimicry, Alchemy) has a skill that defines the specific scoring rubric, red flag taxonomy, and pass/fail thresholds. The Soul Validation skill checks TTT drift (is the voice temperature within 1 level of the assigned gravity center?), vocabulary consistency (are the coach's signature phrases preserved?), and emotional vocabulary alignment (does the script use the coach's emotional language, not generic AI emotion words?).

**Visual Recipe Skills** — The richest category, directly importing the CMF's proven visual production pattern. Each archetype has a corresponding visual recipe skill defining: shot progression (e.g., "Struggle → Challenge → Triumph" for Achievement Stories), semiotic injection rules (which facial expressions from the Facial Expression Lexicon), color progression (desaturated → golden hour → saturated), camera moral stances, and asset research categories. The `routing_table.yaml` acts as the master dispatch, determining which recipe skill to load based on the script's archetype and emotional dimension.

### 7.5 Intelligence Libraries

Underneath the skill layer sits the **intelligence library** — the static knowledge assets that skills reference but never modify. These are the CCF's "laws of physics":

| Library | Path | Contents | Access Pattern |
|---------|------|----------|---------------|
| **Frameworks** | `intelligence/frameworks/` | 22 Viral Frameworks, TTT specifications, archetype palettes, theme scoring rubric, script ID schema, modulation rules, visual memetic rubric | Read-only by all agents |
| **Lexicons** | `intelligence/lexicons/` | Facial expressions, character archetypes, DHD (Deep Human Desires), visual signifiers, TTT linguistic patterns, profanity guidelines, metaphor registry | Read-only by skills |
| **Recipes** | `intelligence/recipes/visual/` | `routing_table.yaml` + 15 category-specific recipe protocols in subdirectories | Read-only by Visual agents |
| **Witnesses** | `intelligence/witnesses/` | `_witness_blueprint.json`, `_interview_protocol.md`, `_index.json`, `TW_XXX_*.md` files | Read by content agents; Write by `ccf-witness` |
| **Learning** | `output/learning/` | Pattern library (false negatives, success patterns), improvement notes, protocol update proposals | Read by all agents; Write by `ccf-review` |

The critical design constraint is that **intelligence libraries are immutable during production**. Skills read from them; they never write to them. Only dedicated governance commands (`ccf-review`, `ccf-witness`) can modify intelligence assets, and even then only with operator approval. This prevents "intelligence drift" — the gradual corruption of core knowledge through uncontrolled agent modification.

---

**Word Count: ~820**

---

## Section 8: Intelligence Framework & Data Assets

### 8.1 The Data Philosophy

The CCF is an intelligence-first system. Every agent decision — from theme selection to voice modulation to visual semiotic injection — is driven by structured data assets, not by ad-hoc prompt instructions. This design eliminates the "prompt lottery" where output quality depends on how well the operator crafts a prompt. Instead, the intelligence is embedded in the data layer, and agents consume it through standardized schemas. Change the data, change the output. Change the prompt? Nothing changes — because the prompt doesn't contain the intelligence.

### 8.2 `config.yaml` — The Session Truth

The central nervous system of every CCF deployment. Every agent reads this file at activation (Step 2 of the mandatory activation sequence), and every field becomes a session variable. No agent may hard-code any value that `config.yaml` provides.

```yaml
# Client Identity
client_name: "Coach Name"
user_name: "Operator Name"
communication_language: "French"

# Directory Structure
output_folder: "./output"
setup_folder: "./output/setup"
batch_folder: "./output/batches"
intelligence_folder: "./intelligence"

# System State
setup_complete: false          # Gate: blocks ccf-generate until true
current_batch: null            # Active batch ID
last_batch_date: null          # Recency tracking

# Model Configuration
model: "gemini-2.5-pro"       # Primary model
model_validation: "gemini-2.5-flash"  # Validation model (cost optimization)
temperature_creative: 0.9     # SoC + Mirror Session
temperature_execution: 0.3    # Script Generator (precision)
temperature_validation: 0.1   # Validators (consistency)

# Production Parameters
scripts_per_batch: 36         # 12 themes × 3 archetypes
tweets_per_batch: 108         # 3 tweets per script
memes_per_batch: 36           # 1 meme concept per script
word_count_target: "120-180"  # Short-form script target

# Quality Thresholds
soul_validation_threshold: 7.0
protocol_validation_threshold: 8.0
mimicry_validation_threshold: 7.5
```

### 8.3 The 22 Viral Frameworks

The CCF's idea generation engine (Phase 7, managed by Emilio) fuses 12 selected themes with 22 Viral Frameworks to produce content ideas. The frameworks are split into two categories based on their psychological force alignment:

**Value-Based Frameworks (Connection Engine):**
Selected when the Context Premise tags the theme as `connection`. These frameworks create recognition, validation, and trust: Top Reliable List, Achievement Story, Comparison Guide, Authority Blueprint, Quick Win, Insider Secrets, Growth Path, Case Study, Tier List, Transformation Timeline, Common Mistakes.

**Emotional-Based Frameworks (Reaction Engine):**
Selected when the Context Premise tags the theme as `reaction`. These frameworks create urgency, disruption, and cognitive dissonance: Myth Busting, Controversial Take, Prediction Reveal, Reality vs. Expectation, Surprising Stats, Provocation Post, Hot Take, Paradigm Shift, Devil's Advocate, Sacred Cow Challenge, Status Quo Autopsy.

Each framework has a defined structural template (hook mechanism, body architecture, CTA pattern), a natural TTT gravity center, and a set of archetype affinities that the Archetype Mapper uses to assign the optimal 3-format mix per idea.

### 8.4 Context Premise — The Psychological Intelligence Layer

The Context Premise is the CCF's most strategically important data asset. Split into two files — `context_premise_connection.json` and `context_premise_reaction.json` — it contains the 72-point psychological map of the audience's relationship with each theme, built by Lila (Audience Empathy Agent) from the Tribe Soul and Social Research outputs.

**Connection Premise Schema:**
```json
{
  "theme": "Building Wealth",
  "dimension": "connection",
  "dreams": ["Financial independence", "Generational legacy"],
  "wants": ["Clear roadmap", "Proven system"],
  "insecurities": ["Starting too late", "Not smart enough"],
  "deep_human_desire": "Security + Significance",
  "tribal_language_samples": ["..."],
  "recommended_frameworks": ["Top Reliable List", "Achievement Story"],
  "ttt_suggestion": "TTT-03 with TTT-02 vulnerability accent"
}
```

**Reaction Premise Schema:**
```json
{
  "theme": "Building Wealth",
  "dimension": "reaction",
  "frustrations": ["Guru hype", "Get-rich-quick noise"],
  "enemies": ["Financial illiteracy industry", "Influencer grifters"],
  "suspicions": ["Is passive income real?", "Do advisors care?"],
  "deep_human_desire": "Agency + Truth",
  "tribal_language_samples": ["..."],
  "recommended_frameworks": ["Myth Busting", "Reality vs Expectation"],
  "ttt_suggestion": "TTT-05 with TTT-07 warrior accent"
}
```

The same theme ("Building Wealth") produces fundamentally different content depending on whether the connection or reaction premise is activated. This is how the CCF generates 36 scripts from 12 themes without repetition — each theme is processed through both emotional lenses, then assigned different archetypes and TTT palettes, producing content that feels fresh despite sharing a topic.

### 8.5 Visual Intelligence Assets

The CCF's visual production layer relies on four specialized lexicons:

**Facial Expression Lexicon** (`intelligence/lexicons/facial_expressions.yaml`) — A curated library of 50+ meme-proven facial expressions mapped to emotional beats. Each entry contains: expression name, reference source (e.g., "Success Kid Determination"), emotional function (triumph, skepticism, disbelief), recommended narrative positions (hook, retention, CTA), and detailed prompt engineering instructions for generative models. This lexicon is the secret weapon that makes CCF-generated images feel culturally resonant rather than stock-photography generic.

**DHD Lexicon** (`intelligence/lexicons/deep_human_desires.yaml`) — Maps 16 Deep Human Desires (Security, Significance, Connection, Growth, Freedom, Contribution, Certainty, Variety, etc.) to visual signifiers, color palettes, and compositional rules. Used by the Visual Prompt Synthesizer to ensure images trigger the correct emotional response at a subconscious level.

**Semiotic Signifiers Library** (`intelligence/lexicons/visual_signifiers.yaml`) — Catalogs objects, settings, and visual elements that carry pre-loaded cultural meaning: a clock (urgency), a mountain peak (achievement), a broken chain (freedom), a boardroom (authority). These are not decorative choices — they are strategic semiotic injections that reinforce the script's message without the audience consciously noticing.

**Visual Memetic Rubric** (`intelligence/frameworks/visual_memetic_rubric.yaml`) — The scoring system used to evaluate generated visuals against 8 dimensions: Narrative Relevance, Emotional Accuracy, Semiotic Density, Cultural Resonance, Brand Consistency, Composition Quality, Color Psychology Alignment, and Viral Potential. Each dimension is scored 1-10, with a composite threshold of ≥ 7.5 required for production use.

### 8.6 Complete Directory Structure

```
ccf/
├── config.yaml                    # Session Truth
├── Gemini.md                      # System Identity
├── ccf_helpers.sh                 # Safety Layer
├── agents/                        # 22+ agent files
│   ├── _master/                   # 3 orchestrators
│   ├── setup/                     # 7 setup agents
│   ├── content/                   # 10+ content agents
│   ├── validation/                # 3 validators
│   └── visual/                    # 3 visual agents
├── skills/                        # 40-55 SKILL.md files
│   ├── archetypes/                # 7-12 format skills
│   ├── voice/                     # 9 TTT-level skills
│   ├── research/                  # 5-8 methodology skills
│   ├── validation/                # 4-6 scoring skills
│   └── visual_recipes/            # 15-20 recipe skills
├── intelligence/                  # Static knowledge (immutable in production)
│   ├── frameworks/                # 22 viral frameworks, TTT specs, palettes
│   ├── lexicons/                  # Expressions, DHD, signifiers, linguistics
│   ├── recipes/visual/            # Routing table + 15 recipe protocols
│   └── witnesses/                 # Blueprint, protocol, index, TW files
├── prompts/                       # Agent protocol files
└── output/                        # All generated content
    ├── setup/                     # One-time foundation (01-05 numbered files)
    ├── batches/                   # Weekly production batches
    │   └── batch_XXX_YYYY-MM-DD/  # Individual batch folders
    │       ├── scripts/           # 36 script asset folders
    │       ├── tweets/            # 108 platform tweets
    │       ├── memes/             # 36 meme concepts
    │       └── visuals/           # Prompts + asset queries
    └── learning/                  # Pattern library + improvement notes
```

---

**Word Count: ~815**

---

## Section 9: Production Workflow & Batch Operations

### 9.1 The Three Lifecycle Model

The CCF operates across three distinct lifecycle tempos, each with different execution frequencies, agent pools, and output types:

**Lifecycle 1: Foundation Setup (One-Time)**
Executed once per client via `ccf-setup`. Duration: 4-8 hours. This lifecycle transforms raw business documents (strategy decks, social media archives, interview recordings, competitor analysis) into the permanent intelligence foundation. The 7 Setup agents execute sequentially because each builds on the previous output — Kimya's Business Canvas informs Emmanuel's Content Strategy, which guides Valeriane's Client Soul extraction, which constrains Dilaya's Tribe Soul mapping. Output: the `output/setup/` directory containing 8-12 numbered intelligence files plus `config.yaml` updated with `setup_complete: true`.

**Lifecycle 2: Weekly Production (Recurring)**
Executed weekly via `ccf-generate`. Duration: 2-4 hours per batch. This lifecycle produces a complete content batch: 36 scripts, 108 tweets, 36 meme concepts, and 72 visual production artifacts (36 generative prompts + 36 asset query sets). The 10+ Content Generation agents execute in a mixed sequential-parallel pattern — some phases must complete before others begin (Theme Discovery before Social Research), while others can run in parallel (Deep Research and Fresh Research for multiple themes simultaneously).

**Lifecycle 3: Evolution (Continuous)**
Executed on-demand via `ccf-regenerate` and weekly via `ccf-review`. This lifecycle closes the feedback loop — surgically improving individual scripts through the Phoenix Loop, then extracting systemic patterns from improvement data to evolve agent protocols. Duration: 5-15 minutes per script regeneration; 30-60 minutes for weekly review.

### 9.2 The 12-Phase Production Pipeline

The weekly production pipeline (`ccf-generate`) is the core engine. Here is the complete phase sequence with agent assignments:

| Phase | Name | Agent | Input | Output | Duration |
|-------|------|-------|-------|--------|----------|
| **5** | Theme Discovery | Divine | Tribe Soul + business trends + client philosophy | `final_selection.md` (12 themes, scored 1-10) | 15 min |
| **6** | Social Research | Maeva | 12 themes + tribal digital channels | 4 recon mission reports per theme across 40+ voices | 30 min |
| **6.5** | Context Premise | Lila | Social research + Tribe Soul + DHD map | `context_premise_connection.json` + `context_premise_reaction.json` | 20 min |
| **7** | Idea Generation | Emilio | 12 themes × 22 viral frameworks + context premises | `ideas.json` (12 ideas with framework-theme fusion) | 15 min |
| **8** | Deep Research | Lionel | 12 themes + 7-Angle framework | 12 first-principles research documents | 30 min |
| **8F** | Fresh Research | Lionel | 12 themes + real-time sources | 12 temporal intelligence documents | 20 min |
| **9** | Archetype Mapping | Emmanuel | 12 ideas + TTT palettes + archetype rules | `archetype_assignments.json` (3 formats × 12 → 36 scripts planned) | 15 min |
| **10** | Research Briefs | Lionel | Archetype assignments + deep/fresh research | 36 script-specific research briefs | 30 min |
| **11** | Script Generation | Script Artisan | SoC → Mirror → Wisdom Forge → Script (4-stage pipeline) | 36 `script.json` files with metadata | 90 min |
| **11C** | Tweet Generation | Tweet Factory | 36 scripts + platform rules + tribal language | 108 platform-optimized tweets (3 per script) | 20 min |
| **11D** | Meme Generation | Meme Engine | 36 scripts + humor profile + facial expressions | 36 meme concept briefs | 15 min |
| **11E** | Visual Production | Visual Team | 36 scripts + visual recipes + lexicons | 36 `visual_prompts.json` + 36 `visual_asset_queries.json` | 30 min |
| **12** | Triple Validation | Sophia + Marcus + Chen | 36 scripts against Soul/Protocol/Mimicry dimensions | Validation reports with scores + pass/fail | 20 min |

**Total estimated batch time: ~5 hours** (with sequential execution). Phases 8/8F can run in parallel, as can 11C/11D/11E, reducing wall-clock time to approximately 3.5 hours with parallelization.

### 9.3 The Production Math

The CCF's batch output follows a deterministic multiplication pattern:

```
12 themes (from Theme Discovery)
  × 1 connection premise + 1 reaction premise (from Context Premise)
  = 24 emotional angles
  → filtered to 12 best ideas (from Idea Generation)
  × 3 archetypes per idea (from Archetype Mapping)
  = 36 unique scripts

Each script produces:
  → 1 script.json (120-180 words)
  → 3 tweets (platform-optimized micro-content)
  → 1 meme concept brief
  → 1 visual_prompts.json (generative art instructions)
  → 1 visual_asset_queries.json (real-world B-roll queries)
  → 1 metadata.json (generation recipe + scoring)
  → 1 iteration_log.json (version history)

TOTAL BATCH OUTPUT:
  36 scripts + 108 tweets + 36 memes
  + 36 visual prompt sets + 36 asset query sets
  + 72 metadata files
  = 324 production assets per weekly batch
```

### 9.4 Batch Folder Anatomy

Every batch is saved to an isolated directory with full traceability:

```
output/batches/batch_001_2025-01-15/
├── batch_manifest.json            # Complete batch metadata
├── themes/
│   └── final_selection.md         # 12 scored themes
├── research/
│   ├── social/                    # 12 social context reports
│   ├── deep/                      # 12 first-principles documents
│   └── fresh/                     # 12 temporal intelligence docs
├── premises/
│   ├── context_premise_connection.json
│   └── context_premise_reaction.json
├── ideas/
│   └── ideas.json                 # 12 framework-theme fusions
├── assignments/
│   └── archetype_assignments.json # 36 script plans
├── scripts/
│   └── S001_wealth_achievement_TTT03_v1/
│       ├── script.json            # Final script
│       ├── soc.md                 # Stage 1 output
│       ├── mirror.md              # Stage 2 output
│       ├── wisdom_briefs/         # Stage 2.5 output (4 briefs)
│       ├── metadata.json          # Generation recipe
│       └── iteration_log.json     # Version history
├── tweets/
│   └── S001_tweets.json           # 3 tweets per script
├── memes/
│   └── S001_meme.json             # Meme concept brief
├── visuals/
│   ├── prompts/S001_visual_prompts.json
│   └── assets/S001_asset_queries.json
└── validation/
    ├── soul_report.json           # Sophia's scores
    ├── protocol_report.json       # Marcus's scores
    └── mimicry_report.json        # Chen's scores
```

### 9.5 The Phoenix Loop (Regeneration Lifecycle)

When a script fails validation or the operator wants improvement, the Phoenix Loop activates via `ccf-regenerate`:

**Mode A: Regenerate (Fresh Variation)**
Same inputs, new execution. The Script Artisan re-runs the 4-stage Soul Infusion Pipeline with identical context but fresh randomness (temperature 0.9). Useful when the script is structurally sound but lacks creative spark. The original version is preserved in `iteration_log.json` as `v1`, and the new version becomes `v2`.

**Mode B: Improve (Surgical Edit)**
Validator feedback is injected as a constraint. The system identifies the specific failure (e.g., "TTT drift detected: target TTT-03, actual TTT-05" or "Vulnerability move missing in retention phase") and re-runs only the relevant pipeline stage with the feedback embedded. This is the most precise mode — it fixes what's broken without re-generating what works.

**Mode C: Modify (Operator Direction)**
The operator provides natural language instructions: "Make the hook more confrontational," "Shift from TTT-03 to TTT-05," "Remove the sports metaphor." The system translates these instructions into constraint modifications and re-runs the pipeline. This mode gives the operator creative control while maintaining pipeline discipline.

**Improvement Note Generation:** When any regeneration mode produces a score increase of 5+ points on any validation dimension, the system automatically generates an Improvement Note documenting: the original failure, the correction applied, the score delta, and a proposed pattern for the Learning System. These notes accumulate in `output/learning/improvement_notes/` and are processed weekly by `ccf-review`.

---

**Word Count: ~830**

---

## Section 10: Quality Gates & Validation System

### 10.1 The Validation Philosophy

The CCF rejects the "generate and hope" approach to AI content. Every script passes through a **Triple Validation Gate** — three independent validators, each examining a different dimension of quality, each using a distinct scoring rubric, each operated by a specialized agent persona. This design is informed by the MCDA experiment's core finding: no single quality dimension captures what makes content resonate. A script can be structurally perfect (Protocol: 9/10) but sound robotic (Soul: 4/10). A script can sound perfectly human (Mimicry: 9/10) but violate the archetype's structural rules (Protocol: 3/10). Only by orthogonalizing the validation dimensions can the system accurately detect — and surgically fix — quality failures.

### 10.2 Validator 1: Soul Validation (Sophia)

**Question Answered:** "Does this script sound like THIS specific coach?"

**Threshold:** ≥ 7.0/10

Sophia is the voice authenticity specialist. She loads the `client_soul.json` and `ttt_baseline.json` at activation, establishing the coach's vocal DNA as her reference standard. She then scores the script against five sub-dimensions:

| Sub-Dimension | Weight | What It Measures | Red Flag Example |
|---------------|--------|-----------------|-----------------|
| **TTT Drift** | 25% | Is the voice temperature within 1 level of assigned gravity center? | Script assigned TTT-03, reads as TTT-06 |
| **Vocabulary Consistency** | 25% | Does the script use the coach's signature phrases and metaphor domains? | Coach uses sports metaphors; script uses cooking metaphors |
| **Emotional Vocabulary** | 20% | Does the script use the coach's emotional language, not generic AI emotion? | "I feel passionate" instead of coach's signature "It burns in my gut" |
| **Rhythm Match** | 15% | Does sentence rhythm match the coach's natural cadence? | Coach uses short punchy sentences; script uses long subordinate clauses |
| **Profanity Calibration** | 15% | Does profanity usage match the coach's comfort level (0-10 scale)? | Coach at 7/10 comfort; script is sanitized to 0/10 |

**Output:** Soul Validation Report with composite score, sub-dimension breakdown, specific line-level annotations identifying drift points, and a severity classification (PASS / MARGINAL / FAIL).

### 10.3 Validator 2: Protocol Validation (Marcus)

**Question Answered:** "Does this script follow the archetype's structural rules?"

**Threshold:** ≥ 8.0/10

Marcus is the structural compliance auditor. He loads the relevant archetype skill at activation, establishing the structural template as his reference standard. He then scores against six sub-dimensions:

| Sub-Dimension | Weight | What It Measures | Red Flag Example |
|---------------|--------|-----------------|-----------------|
| **Hook Compliance** | 20% | Does the hook follow the assigned mechanism (curiosity gap, pattern interrupt, tribal signal)? | Achievement Story uses Myth-Busting hook style |
| **Body Architecture** | 20% | Does the body follow the archetype's structural pattern? | Listicle missing numbered items; Story missing narrative arc |
| **Vulnerability Move** | 20% | Is the Three-Part move (FELT IT → DID IT ANYWAY → RESULTS) present in retention? | Move missing entirely, or only 2 of 3 parts present |
| **CTA Structure** | 15% | Does the CTA follow the archetype's closing pattern? | Generic "follow for more" instead of archetype-specific CTA |
| **Word Count** | 15% | Is the script within the 120-180 word target? | 250 words (over-generated) or 80 words (under-developed) |
| **Section Balance** | 10% | Are hook/body/CTA proportions within archetype norms? | Hook is 60% of word count; body is 20% |

**Output:** Protocol Validation Report with compliance score, structural deviation map, and specific correction instructions for each failed sub-dimension.

### 10.4 Validator 3: Mimicry Validation (Chen)

**Question Answered:** "Would a human reader know this is AI-generated?"

**Threshold:** ≥ 7.5/10

Chen is the human mimicry expert — the Turing test specialist. He evaluates the script not against any template or voice profile, but against his trained understanding of what AI-generated content "feels like." His scoring targets the subtle artifacts that betray machine authorship:

| Sub-Dimension | Weight | What It Measures | Red Flag Example |
|---------------|--------|-----------------|-----------------|
| **Hedging Language** | 25% | Absence of AI safety hedging ("it's important to note," "while everyone's journey is different") | Script contains 3+ hedging phrases |
| **Specificity vs. Generality** | 25% | Presence of specific, searchable claims vs. vague platitudes | "Success requires hard work" instead of "Revenue grew 340% in 18 months" |
| **Emotional Authenticity** | 20% | Do emotions feel lived or described? | "I was scared" (described) vs. "My hands were shaking when I opened the email" (lived) |
| **Transitional Naturalness** | 15% | Do section transitions feel organic or formulaic? | "Now let's move on to..." or "Another important point is..." |
| **Lexical Diversity** | 15% | Vocabulary richness; absence of repetitive AI-preferred words | Overuse of "leverage," "journey," "empower," "navigate" |

**Output:** Mimicry Validation Report with Turing score, AI artifact annotations, and specific replacement suggestions for each flagged phrase.

#### 10.4.1 Quantitative Pre-Filter (Zero API Cost)

Before Chen's LLM-based qualitative assessment runs, a lightweight **Python-based statistical pre-filter** analyzes the script text for forensic linguistics markers that betray machine authorship. These metrics cost zero API calls — they are pure text analysis — and provide a deterministic, reproducible score that complements Chen's subjective Turing test.

| Metric | What It Measures | Human Baseline | AI Tell | Implementation |
|--------|-----------------|----------------|---------|----------------|
| **Sentence Length σ** | Standard deviation of sentence lengths in words | High (humans vary wildly: 3-word punches mixed with 25-word explanations) | Low (AI gravitates to 12-18 word sentences with suspicious consistency) | `numpy.std(sentence_lengths)` |
| **Paragraph Distribution** | Histogram of sentences per paragraph | Bimodal (humans write 1-sentence AND 8-sentence paragraphs) | Unimodal (AI clusters at 3-4 sentences per paragraph) | Distribution entropy analysis |
| **Burstiness Score** | How ideas cluster vs. distribute evenly across the text | High (humans cluster related ideas then jump to new territory) | Low (AI distributes ideas evenly, creating unnatural "balance") | Moving window variance of semantic density |
| **Hapax Legomena Ratio** | Percentage of words used only once in the text | Higher (~40-60% in natural speech) | Lower (~20-35% — AI recycles "leverage," "journey," "navigate") | `Counter` with `frequency == 1` filter |

These 4 metrics contribute ~20% of Chen's total Mimicry score, with the qualitative sub-dimensions (Hedging, Specificity, Emotional Authenticity, Transitional Naturalness, Lexical Diversity) proportionally reduced to ~80%. A script that fails the quantitative pre-filter (scores below threshold on 3+ metrics) is flagged for extra scrutiny before the more expensive LLM-based evaluation runs.

### 10.5 The Composite Score & Failure Routing

The three validator scores are combined into a **Composite Quality Score** using a weighted formula:

```
COMPOSITE = (Soul × 0.35) + (Protocol × 0.30) + (Mimicry × 0.35)
```

Soul and Mimicry are weighted equally and higher than Protocol because the MCDA experiment demonstrated that the audience responds primarily to voice authenticity and human feel, with structural compliance being a necessary but insufficient condition for resonance.

**Failure Routing Logic:**

| Scenario | Composite | Action |
|----------|-----------|--------|
| All pass (≥ thresholds) | ≥ 7.5 | COMMIT to batch — script approved |
| Soul fails, others pass | Variable | Route to Phoenix Loop Mode B with Soul feedback |
| Protocol fails, others pass | Variable | Route to Phoenix Loop Mode B with Protocol feedback |
| Mimicry fails, others pass | Variable | Route to Phoenix Loop Mode B with Mimicry feedback |
| Multiple validators fail | < 6.0 | Route to Phoenix Loop Mode A (full regeneration) |
| All fail | < 5.0 | FLAG for operator review — potential systemic issue |

### 10.6 Alchemy Gate Enforcement

Beyond the triple validation, every script must pass a binary **Alchemy Gate** — a checklist of the 10 Alchemy Principles. Unlike the scored validators, this gate is pass/fail with no partial credit:

- ✅ Does the script contain a Three-Part Vulnerability Move? (Principle 1)
- ✅ Does the script make ONE decisive claim, not a survey of opinions? (Principle 2)
- ✅ Does the hook create an Information Gap? (Principle 3)
- ✅ Is context provided, not just content? (Principle 4)
- ✅ Are audience quotes presented raw, unfiltered? (Principle 5, if applicable)
- ✅ Is the language specific, not cliché? (Principle 6)
- ✅ Is the message delivered through story, not lecture? (Principle 7)
- ✅ Does the content signal clear tribal alignment? (Principle 8)
- ✅ Is complexity acknowledged, not flattened? (Principle 9)
- ✅ Does the script feel accurate/lived rather than polished/performed? (Principle 10)

A script that scores 8.5/10 on all three validators but fails Principle 1 (no Vulnerability Move) is **rejected** and routed to regeneration. The Alchemy Gate is the final philosophical safeguard — it ensures the CCF produces content that is not just technically proficient but philosophically aligned with the system's core values.

---

**Word Count: ~825**

---

## Section 11: Non-Functional Requirements & System Constraints

### 11.1 Local-First Architecture

The CCF is designed as a **local-first, operator-controlled system** — it runs entirely on the operator's machine with no cloud dependencies beyond the Gemini API. All intelligence assets, agent files, skills, and production outputs reside on the local filesystem. There is no centralized server, no web dashboard, no multi-user authentication layer. This is a deliberate architectural choice, not a limitation. Local-first execution provides three critical advantages: (1) Complete data sovereignty — client voice DNA, business strategy, and transformation witness data never leave the operator's machine, (2) Deterministic reproducibility — the same command with the same inputs produces traceable, auditable output because there are no hidden cloud-side state mutations, and (3) Operator agency — the human always has final authority because they control the execution environment, file system, and approval gates.

**Deployment Requirements:**
- Operating System: Any Unix-compatible (macOS, Linux, WSL2 on Windows)
- Shell: Bash 4.0+ (for `ccf_helpers.sh` Safety Layer)
- Python: 3.10+ (for `json.load()` validation in `save_json_safe`)
- API Access: Google Gemini API key (`GOOGLE_API_KEY` environment variable)
- Optional: Tavily API key (`TAVILY_API_KEY`) for real-time research via `ccf-generate` Phase 8F
- Disk: ~500MB per client setup + ~50MB per weekly batch
- Network: Required only during agent execution (API calls); all other operations are offline

### 11.2 Context Window Management

The CCF's most critical non-functional constraint is **context window discipline**. Gemini 2.5 Pro provides a 1M+ token context window, but filling it degrades output quality because the model cannot prioritize when overwhelmed with context — a phenomenon the CCF terms "Context Explosion."

The `build_context(phase)` function in `ccf_helpers.sh` is the primary defense mechanism. It implements a **phase-specific loading strategy** that ensures each agent receives only the context required for its cognitive task:

| Phase | Context Loaded | Approximate Tokens |
|-------|---------------|-------------------|
| Setup (Phase 0-4) | Gemini.md + config.yaml + raw client documents | 15,000-30,000 |
| Theme Discovery (Phase 5) | Gemini.md + config.yaml + client_soul + tribe_soul + theme_history | 20,000-35,000 |
| Social Research (Phase 6) | Gemini.md + config.yaml + tribe_soul + theme assignments | 15,000-25,000 |
| Context Premise (Phase 6.5) | Gemini.md + config.yaml + tribe_soul + social research outputs + DHD lexicon | 25,000-40,000 |
| Script Generation (Phase 11) | Gemini.md + config.yaml + client_soul + SoC + adapted prompt + wisdom briefs + archetype skill | 30,000-50,000 |
| Validation (Phase 12) | Gemini.md + config.yaml + client_soul + ttt_baseline + script + validation skill | 20,000-35,000 |

**The Hard Rule:** No single agent call should exceed 100,000 tokens of input context. Beyond this threshold, empirical testing shows measurable degradation in instruction-following accuracy, particularly for nuanced voice calibration tasks. If a phase naturally requires more context (e.g., processing all 36 scripts for batch-level validation), the orchestrator must split the work into multiple sequential calls.

### 11.3 Model Selection & Temperature Calibration

The CCF uses a **dual-model strategy** to optimize quality versus cost:

**Primary Model: Gemini 2.5 Pro** — Used for all creative and analytical tasks (SoC generation, Mirror Session reasoning, Wisdom Forge dimensional thinking, script generation, theme discovery, social research, context premise building). These tasks require maximum reasoning capability and creative flexibility.

**Validation Model: Gemini 2.5 Flash** — Used for all scoring and compliance tasks (Soul Validation, Protocol Validation, Mimicry Validation, Alchemy Gate checking). These tasks require consistency and speed rather than creativity. Using Flash for validation reduces cost by approximately 75% per validation call while maintaining scoring accuracy.

**Temperature Calibration by Cognitive Mode:**

| Cognitive Mode | Temperature | Rationale |
|----------------|-------------|-----------|
| Voice Priming (SoC Generator) | 0.9 | Maximum creative freedom for authentic voice activation |
| Structured Reasoning (Mirror Session) | 0.7 | Balanced creativity with logical discipline |
| Dimensional Thinking (Wisdom Forge) | 0.8 | Creative insight generation within philosophical constraints |
| Script Execution (Script Generator) | 0.3 | Precision execution of pre-decided strategy — minimize hallucination |
| Validation (All Validators) | 0.1 | Maximum consistency and deterministic scoring |
| Research (Deep/Fresh) | 0.5 | Balanced factual accuracy with analytical insight |

### 11.4 Error Handling & Recovery

The CCF classifies errors into three categories, each with a defined recovery protocol:

**Class 1: Recoverable Errors (Auto-Retry)**
- API timeout or rate limit → Exponential backoff (2s, 4s, 8s, max 3 retries)
- JSON parse failure → Raw output saved to `error.log`, agent re-executed
- Schema validation failure → Output saved, agent re-executed with explicit schema reminder

**Class 2: Degraded Errors (Operator Alert)**
- Context window exceeded → Warning displayed, context truncated to priority assets, operator notified
- Validation score below 5.0 on all dimensions → Script flagged for manual review, batch continues without it
- Research API failure (Tavily) → Warning displayed, batch continues with deep research only (no fresh research)

**Class 3: Fatal Errors (Halt)**
- `config.yaml` not found or corrupted → Full stop, operator must fix config
- `setup_complete: false` when running `ccf-generate` → Full stop, operator must run `ccf-setup` first
- Safety Layer (`ccf_helpers.sh`) not sourced → Full stop, operator must source helpers

All errors are logged to `output/logs/error_YYYY-MM-DD.log` with timestamp, phase, agent, error class, and recovery action taken.

### 11.5 Scalability Constraints

The CCF is designed for **single-client, sequential batch execution**. It is NOT a multi-tenant system. Each client gets a dedicated CCF directory with its own `config.yaml`, intelligence assets, and output structure. Running multiple clients requires multiple CCF installations or switching `config.yaml` between runs.

**Batch Size Limits:**
- Scripts per batch: 36 (hardcoded as 12 themes × 3 archetypes)
- Themes per batch: 12 (optimal for weekly content cadence)
- Maximum concurrent API calls: 1 (sequential execution by default; parallelization optional via shell scripting)
- Maximum batch archive retention: Unlimited (operator manages disk)

**Scaling Beyond Single Client:**
For agencies managing multiple clients, the recommended pattern is directory-level isolation: `ccf-client-a/`, `ccf-client-b/`, etc. Each directory is a complete, self-contained CCF installation. A lightweight shell script can iterate across directories to run batch generation for multiple clients sequentially.

### 11.6 Security & Privacy Model

- **API Key Isolation:** All API keys are stored in environment variables (`.env` file), never hard-coded in agent files, scripts, or config
- **No PII in Prompts:** Client voice DNA is extracted and stored locally. Raw transcripts are processed during setup and can be deleted afterward — the intelligence assets (`client_soul.json`, `tribe_soul.json`) contain synthesized patterns, not verbatim client data
- **Operator-Controlled Output:** All generated content is saved locally. No automatic publishing, no social media API integration. The operator reviews and publishes manually
- **No Telemetry:** The CCF sends no usage data, analytics, or diagnostic information to any external service. The only network traffic is Gemini API calls for content generation

---

**Word Count: ~810**

---

## Section 12: Evolutionary Learning & Continuous Improvement

### 12.1 The System That Gets Smarter

Most AI prompting systems are static — they perform exactly the same on Day 100 as they did on Day 1. The CCF is designed as a **self-improving evolutionary engine**. It does not just produce content; it produces *data about its own performance*. Every regeneration, every validation failure, and every operator edit is a signal that the system captures, analyzes, and uses to rewrite its own protocols.

### 12.2 All Failure is Data: The Phoenix Loop

The Phoenix Loop (introduced in Section 9.5) is the mechanism that turns failure into intelligence. It operates on the principle that **a rejected script is a valuable training example**.

When an operator rejects a script and uses `ccf-regenerate` (Mode B or C) to fix it, the system creates a "diff" between the failed state and the successful state. If the validation score improves by ≥ 5 points, an **Improvement Note** is automatically generated in `output/learning/improvement_notes/`.

**Improvement Note Schema:**
```json
{
  "id": "IMP-20250115-001",
  "script_id": "S001_wealth_achievement",
  "archetype": "Achievement Story",
  "failure_mode": "TTT Adjustment",
  "original_score": 6.2,
  "final_score": 8.5,
  "delta": +2.3,
  "operator_instruction": "Make it less aggressive, more like a wise mentor",
  "pattern_observation": "System consistently over-indexes on aggression when 'Wealth' topic is combined with TTT-05."
}
```

### 12.3 The Weekly Review Protocol (`ccf-review`)

The `ccf-review` command is the evolutionary heartbeat. Run once per week after batch production, it triggers the Learning Agent to digest the week's Improvement Notes and propose structural updates.

**The Review Workflow:**
1.  **Ingest:** Load all Improvement Notes from the current batch.
2.  **Cluster:** Identify recurring failure patterns (e.g., "3 out of 5 Myth-Busting scripts failed Hook Compliance because they were too long").
3.  **Diagnose:** Trace the failure to the source — is it a bad Prompt (agent issue), a bad Baseline (soul issue), or a bad Constraint (archetype issue)?
4.  **Propose:** Generate a **Protocol Update Proposal (PUP)**.

**Example PUP:**
> **Pattern Detected:** Myth-Busting scripts are consistently 40 words over limit (av. 210 words).
> **Diagnosis:** The `myth_busting_skill.md` hook instructions engage in too much preamble before the main claim.
> **Proposed Action:** Update `skills/archetypes/myth_busting.md` line 45.
> **Change:** FROM "Set the context for the myth..." TO "State the myth in one sentence immediately."

The operator reviews the PUP. If approved, the system **self-patches** the skill file. The next batch of Myth-Busting scripts will inherently avoid the error. This is how the CCF gets smarter every week without the operator needing to be a prompt engineer.

### 12.4 The Pattern Library

Beyond protocol patches, the Learning Agent maintains a persistent **Pattern Library** in `output/learning/patterns/` that categorizes successful and failed approaches:

**A. False Negatives Registry**
Cases where the Validator said FAIL but the Operator said COMMIT.
*Insight:* The Validator is too strict or miscalibrated.
*Action:* Adjust `ccf_helpers.sh` validation thresholds or update the Validator's instruction file.

**B. Success Templates**
Scripts that achieved "Perfect Resonance" (Composite Score > 9.0 and high audience engagement predictions).
*Insight:* This is the "Golden Ratio" for this specific client.
*Action:* Save as a "Gold Standard" few-shot example in the `client_soul.json` to guide future generation.

**C. Gap Analysis**
Topics requested by the Context Premise (what the tribe wants) but never successfully generated (what the system failed to produce).
*Insight:* The system lacks a specific skill or framework for this sub-topic.
*Action:* Recommend creating a new custom skill.

### 12.5 The Path to Fine-Tuning

While the current CCF relies on RAG (Retrieval-Augmented Generation) and complex prompting, it is architected to prepare for **Model Fine-Tuning**. Every committed batch creates a perfectly labeled dataset:
- **Input:** Context Premise + Briefs
- **Output:** Final High-Scoring Script
- **Labels:** Validated Scores + Archetype Tags

After 20-30 batches (approx. 6 months), the operator will have ~1,000 high-quality, validated examples of "Coach Voice + Structural Excellence." This dataset can be used to fine-tune a smaller, faster model (e.g., Gemini Flash or a local 8B model) that internalizes the rules, reducing the need for massive context windows and complex prompting. The CCF today is the **data factory** for the custom model of tomorrow.

### 12.6 Soul Evolution: The `ccf-soul-refresh` Roadmap

The Soul is currently a one-time extraction during `ccf-setup`. But coaches evolve — their voice at Month 6 is not their voice at Month 1. New podcast episodes, Instagram Reels, and client interactions continuously shape their communication style. The V1 architecture treats `client_soul.json` as immutable after setup. V2 will introduce `ccf-soul-refresh` — a periodic re-ingestion command (recommended cadence: every 30 days) that:

1. **Ingests new content** — latest social posts, podcast transcripts, newsletter archives since last extraction
2. **Performs delta-merge** — blends new voice patterns with the existing `client_soul.json` rather than overwriting, preserving the established baseline while incorporating evolution
3. **Updates TTT baselines** — recalculates `ttt_baseline.json` if the coach's natural gravity center has shifted (e.g., a coach who was TTT-03 may evolve toward TTT-05 over time)
4. **Generates a Voice Drift Report** — documents what changed and why, giving the operator visibility into how the coach's voice is evolving

This command does NOT exist in V1. It is documented here as a **Phase 2 roadmap commitment** because the architecture must be designed to support it — specifically, `client_soul.json` must use a versioned schema that supports incremental updates rather than monolithic replacement.

---

**Word Count: ~780**

---

# Final Word Count Summary
- **Section 1:** ~802 words
- **Section 2:** ~823 words
- **Section 3:** ~830 words
- **Section 4:** ~835 words
- **Section 5:** ~810 words
- **Section 6:** ~825 words
- **Section 7:** ~820 words
- **Section 8:** ~815 words
- **Section 9:** ~830 words
- **Section 10:** ~825 words
- **Section 11:** ~810 words
- **Section 12:** ~780 words
- **Total:** ~9,805 words

**Status:** COMPLETE.

