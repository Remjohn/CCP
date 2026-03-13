---
stepsCompleted: [1]
inputDocuments: [
  "C:/Users/Mitano/.gemini/antigravity/brain/d2fa065a-161c-494d-a6d5-b605390c1a7a/CCP_Unified_Architecture_MCDA.md"
]
session_topic: 'Brownfield Asset Audit for CCP'
session_goals: 'Determine KEEP/UPGRADE/REPLACE/ADD for existing CCF, CBCS, and V²WS assets'
selected_approach: ''
techniques_used: []
ideas_generated: []
context_file: 'd:/Work/The Conscious Coaching Factory/bmad/.bmad/bmm/data/project-context-template.md'
---

# CCP Brainstorming Session: Brownfield Asset Audit

## Session Overview

**Topic:** Brownfield Asset Audit for CCP (CCF + CBCS + V²WS)
**Goals:** Determine KEEP/UPGRADE/REPLACE/ADD for existing CCF, CBCS, and V²WS assets to build the unified Pi-native orchestration architecture.

### Context Guidance

This brainstorming session focuses on the CCP infrastructure rebuild, specifically addressing:
- **Technical Approaches:** How we wire the 12 CBCS Python agents, 28 CCF commands, and 87 skills under the new Pi Coding Agent harness.
- **Technical Risks:** Avoiding the accidental overwrite of existing, working IP (like the 72-slide V²WS engine or the sacred coach voice notes).

### Session Setup
_User selected AI-Recommended techniques approach and approved the custom sequence._

## Technique Selection

**Approach:** AI-Recommended Techniques
**Analysis Context:** Brownfield Asset Audit for CCP with focus on determining KEEP/UPGRADE/REPLACE/ADD for existing CCF, CBCS, and V²WS assets.

**Recommended Techniques:**
- **Constraint Mapping:** Identifies the unchangeable IP boundaries vs. areas ripe for Pi-native upgrade.
- **Solution Matrix:** The core evaluation grid to definitively categorize every CCP asset into KEEP, UPGRADE, REPLACE, ADD.
- **Decision Tree Mapping:** Maps architectural paths for UPGRADE/ADD items to define PM and Architect requirements.

**AI Rationale:** The constraint is strict protection of existing operational IP (V²WS + voice notes). A methodical, structured approach ensures thorough analysis before attempting orchestration redesign.

## Technique Execution Results

### 1. Constraint Mapping
**Focus:** Identify unchangeable boundaries.
**Key Insights:**
- There are no absolute "do not touch" boundaries out of stubbornness; everything must be tested as part of the holistic system.
- The 3 years of accumulated intellectual property (skills, commands, script prompts) are highly valuable assets. Any removal or radical change requires a *valid, testable reason*.
- Keeping the coach brand fresh, up-to-date, and relevant is a massive priority. Voice transcripts are the primary vehicle for preserving and evolving the coach's authentic DNA.

### 2. Solution Matrix (Idea Generation & Categorization)
**Focus:** Evaluate components against KEEP/UPGRADE/REPLACE/ADD.

**Component 1: The Weekly Production Engine (`ccf-weekly`)**
- **First Principle Insight:** The purpose of the engine is to compress the coach's effort into a 15-20 minute window, not just to generate content.
- **System Thinking:** "Agentic operations" does not mean anarchy. We need the reliable structure of a weekly pipeline to maintain the time constraint, but with added intelligence.
- **Decision:** **UPGRADE.** We keep the rigid weekly sequence (Mon-Sun), but we upgrade the execution loop so agents can pause, self-reflect, and fix quality gate failures dynamically before bothering the human manager.

**Component 2: The 12 CBCS Python Agents (Aria, Kimya, Atlas, etc.)**
- **First Principle Insight:** Effectiveness (getting nuanced, perfect content that requires zero coach edits) is more important than pure computational efficiency (saving API tokens).
- **System Thinking:** A "Board of Directors" model where a Recruiter dynamically selects experts based on the specific task. The agents remain strictly indoctrinated by their individual `SKILL.md` protocols.
- **Decision:** **UPGRADE.** Move from static, hard-coded agent calls to dynamic recruitment (the MATRL academic framework). This adds a reasoning step before execution but drastically improves the precision of the output.

**Component 3: The 87 CCF Content Skills (Alchemy, Layered Questions, etc.)**
- **First Principle Insight:** The 3 years of IP represent proven psychological and narrative constraints (e.g., 4 Laws of Layered Questions). We want agents to focus their reasoning on *strategy*, not on remembering *how* to execute a rule.
- **System Thinking:** If an agent has to read an 8-page prompt to remember how to format a hook, its context window is flooded. If the skill is a modular Tool, the agent only worries about the *what*, while the Tool handles the *how*.
- **Decision:** **UPGRADE.** Convert the massive text prompts into Pi-native modular Tools/Functions. This allows agents to work as a Team (Board of Directors) while using the 87 Skills as high-precision Tools, maximizing both focus and bounded creativity.

### 3. Architectural Terminology Clarification
During the brainstorm, we clarified the exact differences between these core concepts:
- **Expertise:** The human knowledge (e.g., Jason Fladlien's webinar psychology or the 14 Alchemy principles). It is abstract.
- **Skills (The "What"):** The written documentation of that expertise. In our system, these are the `.md` files (like `SKILL.md`) that contain the rules, constraints, and tone.
- **Tools (The "How"):** Executable computer code. A tool actually *does* something (e.g., a function that searches the web, or a function that strictly formats a script into 4 paragraphs). 
- **Intelligence Library:** The folder or database where all the *Skills* and Coach Voice Notes live. It is the "long-term memory" or library the agents read from.
- **Language for Tools:** **Python**, because the 12 CBCS expert agents are built in Python (using LangGraph/LangChain). The Pi Coding Agent (TypeScript) acts as the overall harness/manager, but the specific tools the agents use should be native to their Python environment.

### 4. Decision Tree Mapping (Architecture & Orchestration)
**Focus:** Map architectural paths for how Pi manages the Board, the Library, and the Tools.

**The Orchestration Flow:**
1. **Pi Coding Agent (The Harness):** Receives the user request (e.g., "Write a V²WS webinar").
2. **The Recruiter (Python Manager):** Pi calls the Python manager, which analyzes the request and dynamically recruits the required Board of Directors (e.g., Aria and Kimya).
3. **The Library (Memory):** Aria and Kimya immediately fetch their specific `SKILL.md` files and the relevant "Sacred Voice Notes" from the Intelligence Library.
4. **The Tools (Action):** The agents use Python Tools to execute the creative logic systematically.

**How Creative Assets Become Tools:**
Tools are not just for structured data; they are the *engines* of creativity. A tool doesn't "write" the joke; the tool *forces* the agent's creativity through a specific psychological constraint.

**The 7 Ultimate CCP Tools:**
1. `fetch_sacred_voice(topic)`: Semantically searches the raw, unfolded coach transcripts and injects pure, unaltered Stream of Consciousness into the agent's context.
2. `calibrate_ttt(text, ttt_level)`: Takes baseline text and strictly enforces the vocabulary constraints of the 6 Temperature Temperament Tone levels (e.g., converting L1 Diplomatic to L6 Truth Bomb).
3. `apply_humor_theory(theory_type, concept)`: For V²WS memes. The agent inputs a topic, and the tool forces the output through one of the 4 strict humor structures (Relief, Incongruity, Superiority, Benign Violation).
4. `generate_layered_questions(tension_level)`: Implements the CCF Distillation Funnel. The tool programmatically ensures the 4 Laws (Saturation, Emotion, Compression, Unpredictability) are met.
5. `generate_v2ws_visual_hook(narrative_arc_stage)`: Takes a script moment and generates the highly complex 150-word Midjourney/DALL-E prompt optimized for 4:3 aspect ratio hooks based on the hero's journey.
6. `insert_sfx_cues(script, emotion_map)`: Scans an output script and programmatically inserts explicit V²WS sound effect markers (e.g., `[SFX: Inception BWAAA]`, `[SFX: Cash Register]`) at peak emotional moments.
7. `verify_alchemy_gates(content)`: An evaluation tool that acts as a quality gate, returning true/false based on whether the generated content successfully hits the 14 Alchemy principles (e.g., `vulnerability_present == true`).

**How Tools are Defined and Executed:**
- **Execution:** We use native LLM "Function Calling." The agent (LLM) predicts the arguments, the orchestration framework (LangGraph for Python, Pi for TypeScript) pauses the LLM, executes the actual code on the machine, and feeds the response back to the agent.
- **Format:** Tools are NOT yaml or md files. They are actual code.
**How Tools are Defined and Executed:**
  - In **TypeScript (Pi)**: Defined as a `.ts` function utilizing a Zod schema to enforce argument structure.
  - In **Python (CBCS Agents)**: Defined as a `.py` function with a `@tool` decorator, using Pydantic schemas for strict argument validation and a docstring to explain the tool to the agent.
- **The Prompt Hierarchy (Where the 700 lines go):** The detailed instructions do *not* get deleted. They are redistributed to maximize agent focus:
  1. **The Core `SKILL.md` (Strategy - ~150 lines):** Keeps the "Why" and the "When". Defines the coach's tone, the fundamental goal, and when to use which tool.
  2. **The Tool Schema (Structure - ~100 lines):** The Zod/Pydantic definitions contain detailed descriptions for every single argument (e.g., `tension_level: "Must be one of 3 states based on the Alchemy principles..."`). The LLM reads these deeply when deciding what to pass to the tool.
  3. **The Tool's Internal System Prompt (Execution - ~450 lines):** When the agent calls a tool (like `generate_v2ws_visual_hook`), the *Tool itself* might spin up a sub-agent or a chain with the full 450-line hyper-specific prompt to execute that single, microscopic task perfectly. 
- **Decision:** **UPGRADE.** We do not delete the instructions. We chunk the 700-line monolithic prompts into this 3-part hierarchy (Skill -> Schema -> Tool Internal Prompt) so the Chief Agent doesn't have to hold all 700 lines in its head while managing the overall workflow.

---

## Session 1: Component Hierarchy — Per-Genre Taxonomy

**Goal:** Classify all 72 CCF skills into their true species: True Skill, Disguised Tool, Script Prompt, or Skill+Tool Pair.

### Classification Framework
| If the SKILL.md... | Species | Action |
|---------------------|---------|--------|
| Requires reasoning, judgment, or creativity using psychological constraints | **True Skill** | Stays as `.md`, loaded into agent context |
| Contains binary checks, counting, or deterministic data transformation | **Disguised Tool** | Becomes a Python function with Pydantic schema |
| Contains a fixed structure with fill-in-the-blank templates | **Script Prompt** | Template stays as prompt, schema becomes Tool |
| Contains both reasoning AND procedural logic | **Skill + Tool Pair** | Split: reasoning stays in Skill, procedure becomes Tool |

### Per-Genre Results

| Genre | Skills | True Skill | Disguised Tool | Script Prompt | Skill+Tool |
|-------|--------|-----------|---------------|--------------|------------|
| Setup (6) | soul-extraction, tribe-extraction, pillar-builder, philosophy-brief, audience-empathy, theme-discovery | 5 | 0 | 0 | 1 |
| Content (7) | question-engineer, intelligence-radar, script-architect, coach-elicitation, dynamic-theme-gen, memory-engine, recording-director | 4 | 1 | 0 | 2 |
| Research (9) | raw-fresh, raw-deep, smart-query, blueprint-orch, critic, strategy-dir, vibe-comments, visual-asset, archetype-mapping | 4 | 2 | 0 | 3 |
| Distillation (5) | blueprint-distiller, question-distiller, research-distiller, visual-distiller, voice-distiller | 0 | **5** | 0 | 0 |
| Production (4) | wisdom-forge, soc-generator, mirror-session, script-generator | **4** | 0 | 0 | 0 |
| Orchestration (4) | ccf-batch, ccf-produce, ccf-multi-theme, ccf-report | 0 | **4** | 0 | 0 |
| Distribution (3) | art-director, orchestrator, smart-mix | 1 | 1 | 0 | 1 |
| Validation (4) | boss-will, phoenix-loop, script-analyst, script-commander | 1 | **3** | 0 | 0 |
| Visual Recipes (14) | 14 archetype recipes (dopamine-cliff, storytelling, etc.) | 0 | 0 | **14** | 0 |
| Eroll (16) | 16 planners (storytelling, case-study, etc.) | 0 | 0 | 0 | **16** |
| **TOTAL** | **72** | **~19** | **~16** | **~14** | **~23** |

### Key Insights
1. **Production is the creative heart** — all 4 skills are True Skills requiring deep reasoning
2. **Distillation and Orchestration are 100% procedural** — all should become Python Tools
3. **Visual Recipes are 100% Script Prompts** — fixed archetype templates with fill-in-blank structure
4. **Eroll planners are all hybrids** — scene structures are templates, query generation is creative
5. **The Prompt Hierarchy (3-part split)** prevents loss of detailed instructions: Strategy (~150 lines) → Schema (~100 lines) → Tool Internal Prompt (~450 lines)

---

## Session 2: Pi Harness — 11 Extensions Architecture

**Goal:** Design the Pi extension stack and establish Team vs. Chain orchestration patterns.

### First Principle
The Agent Harness = the operating system. LLM = brain. Pi = body. Extensions = organs. Pi replaces `cli_runner.py` (404 lines) with a fully customizable orchestration layer.

### Orchestration Patterns
- **Agent Team** (parallel, coordinator synthesizes) → Research phase, intelligence gathering
- **Agent Chain** (sequential pipeline, output feeds next) → Production pipeline, validation gates
- Both patterns are used in CCP — smart routing per use case

### The 11-Extension Stack

**Operational Extensions (1-7):**

| # | Extension | Hook | Purpose |
|---|-----------|------|---------|
| 1 | InteractComp | `onInput` | Ambiguity gate — forces clarification before work starts |
| 2 | MemoryFolder | `onAgentEnd` | Context compression — voice notes NEVER fold |
| 3 | DamageControl | `onError` + `onToolCall` | Self-correction loop — Phoenix Loop at harness level |
| 4 | ModelRouter | session config | Per-task model selection (cheap for gates, expensive for creative) |
| 5 | TillDone | `onInput` + widget | Deterministic task completion — replaces `write_todos` JS |
| 6 | TeamOrchestrator | YAML config | Agent Teams (parallel) + Chains (sequential) |
| 7 | SystemSelect | `/system` command | Persona swapping — one Pi session becomes any CBCS agent |

**Intuition Extensions (8-11):**

| # | Extension | Intuition Layer | Definition |
|---|-----------|----------------|------------|
| 8 | **SoulResonance** | Emotional Memory | Searches by emotional signature, not keyword. Cross-system: CBCS coaching + CCF content + V²WS webinars all benefit from spotting emotional patterns |
| 9 | **PatternWeaver** | Cross-Domain Synthesis | Manufactures SURPRISE by connecting unrelated data. Also REMEMBERS which types of surprise and cross-domain connections worked and WHY |
| 10 | **GhostContext** | Unconscious Processing | Forces deeper Context Premises — surfaces emerging historical patterns that are present but not explicitly discussed. The subconscious of the system |
| 11 | **AncestralWisdom** | Expressed Intuition | The synthesis of 8+9+10 — takes raw intuition and converts it into words, ideas, and actions. "When intuition becomes naked" — the moment insight is articulated |

### Key Insight: The Intuition Hierarchy
AncestralWisdom is NOT independent from the other 3. It is the **expression layer** that depends on them:
- SoulResonance provides the emotional raw material
- PatternWeaver finds the hidden connections
- GhostContext surfaces what wasn't asked for
- **AncestralWisdom converts all of this into language** — the moment intuition stops being a feeling and becomes a creative output

### The Emergent Intuition Principle
**"These extensions cannot be forced — they grow with data."**

The 4 Intuition Extensions are NOT features you "switch on." They are **emergent capabilities** that mature as the relational graph accumulates data over time:
- **Week 1-4:** SoulResonance can only echo what it has. Limited emotional memory. Basic pattern matching.
- **Week 5-12:** PatternWeaver starts finding cross-domain connections. GhostContext begins surfacing emerging patterns.
- **Week 13+:** AncestralWisdom has enough data to convert intuition into articulated language. The system starts "knowing" things.
- **Month 6+:** The system has built a subconscious. It manufactures surprise reliably. It anticipates the coach's reactions.

### The Business Moat
**"Build the Consciousness by building the Subconscious first."**

This is the client retention architecture:
1. The system builds **Subconscious** first (SoulResonance + PatternWeaver + GhostContext accumulating data passively)
2. Over time, the Subconscious matures into **Consciousness** (AncestralWisdom expressing intuition)
3. The longer a coach works with the system, the more **irreplaceable** it becomes
4. Switching to a competitor means losing months/years of accumulated intuition
5. This is NOT lock-in through inconvenience — it's lock-in through **genuine intelligence that grows with the relationship**

### Data Infrastructure
All 4 Intuition Extensions are **relational graph data** (Neo4j HGM):
- Not flat tables, not JSON files
- Hyper-edges connecting emotional states, content performance, coaching outcomes, tribal behaviors
- The graph IS the subconscious — nodes are memories, edges are connections, hyper-edges are intuitions

---

## Session 3: Unified Memory Layer — CCF ↔ CBCS ↔ V²WS

**Goal:** Design the shared memory architecture connecting all 3 subsystems + the Intuition Extensions.

### 3-Tier Memory Architecture
| Tier | Stores | Lifespan | Storage |
|------|--------|----------|---------|
| **Working Memory** | Current task scratchpad | Dies after task | In-context window |
| **Episodic Memory** | Coach DNA, voice notes, sessions | Permanent (sacred) | Supabase files + Neo4j pointers |
| **Semantic Memory** | Learned patterns, intuitions, performance | Grows over time | Neo4j HGM hyper-edges |

### 3 Architectural Decisions

**Decision 1: Voice Notes = Supabase with Neo4j Pointers**
Raw voice files live in Supabase (sacred, never compressed). Neo4j holds metadata pointers (emotion tags, timestamps, topic tags). SoulResonance queries Neo4j to FIND relevant moments, then fetches the actual transcript from Supabase.

**Decision 2: Memory Curator Agent**
A dedicated Memory Curator agent runs at the end of each week (Sunday Bot Meeting). It distills what was actually learned from the week's agent runs, filters noise, and writes validated insights to Semantic Memory. Not every agent writes to memory — only the Curator writes, ensuring quality.

**Decision 3: Hyper-Edges Are Data-Driven Only**
"Numbers don't lie." A regular edge gets promoted to a hyper-edge ONLY when quantitative performance data supports the connection:
- Content engagement metrics (saves, shares, comments)
- Coaching outcomes (behavior change, follow-up rates)
- Webinar metrics (drop-off, conversion, clip rate)
- No intuition without evidence. The subconscious is built on measured truth.

### Unified Graph Schema (Neo4j HGM)
```
COACH (center node)
├── EPISODIC: voice transcripts, coaching sessions, soul values
│   (Supabase files, Neo4j pointers with emotion + topic tags)
├── SEMANTIC: learned patterns from performance data
│   (Memory Curator writes weekly, data-driven only)
└── HYPER-EDGES: multi-node intuitions promoted by numbers
    (e.g., [heated + generational_poverty + TTT-05 + storytelling + Week14 → saves:847])
```

---

## Session 4: HGM + ACE — The Evolution Engine

**Goal:** Design how data grows into hyper-edges AND how SKILL.md files evolve over time.

### HGM: Hyper-Edge Promotion (Data-Driven)

**The Self-Esteem Principle:**
The system does NOT optimize for external vanity metrics (saves, shares, likes). It builds **Self-Esteem** through positive feedback loops from INTERNAL approval:
- Coach approves output (zero edits = highest reward)
- Manager (system owner) approves
- Sunday Board Meeting assessment

**Hyper-Edge Maturity Model:**
```
OBSERVATION (1x)  → "This happened once"            → regular edge
PATTERN    (3x+) → "This keeps happening"           → promoted to hyper-edge
INTUITION  (7x+) → "The system knows this reliably" → AncestralWisdom acts on it
```

### The Credit System — Two Types of Feedback

| Type | What It Is | System Response |
|------|-----------|----------------|
| **Testing/Trial Feedback** | Coach edits, adjustments, preferences discovered during normal production | LEARNING signal — no penalty. ACE patches the SKILL.md with the new knowledge |
| **Red Flag Rejection** | Output is lazy, generic, cliché, AI-sounding, or "safe average" | PENALTY signal — credit deducted. Triggers investigation: which agent, which skill, what went wrong |

**What Gets Penalized:**
- Generic output that any AI could write
- Cliché language, safe average phrasing
- Lazy reasoning that skips the 4 Laws or doesn't engage with coach DNA
- Output that "sounds AI" — the cardinal sin

**What NEVER Gets Penalized:**
- Creative risks that didn't land (the coach pushes back but appreciates the attempt)
- Novel cross-domain connections that need refinement
- Experimentation with new archetypes or TTT levels

**Core Principle:** "All we are doing is NOT sound AI and avoid safe average."

### ACE: SKILL.md Evolution Protocol

**How a SKILL.md evolves after each weekly cycle:**
1. Sunday Bot Meeting runs → Memory Curator collects approval/rejection data
2. Testing feedback → MODULAR PATCH added to the SKILL.md (additive, never delete)
3. Red flag rejections → investigation of which skill clause failed → targeted fix
4. Every patch is versioned. If updated skill produces WORSE results → rollback
5. Require 3 consecutive weeks of consistent data before making permanent changes

**ACE Safeguards:**
- **Anti-Brevity Bias:** Never shorten instructions. Add "LEARNED" clauses instead
- **Anti-Context Collapse:** Modular patches, not full rewrites. Version control on every change
- **Anti-Drift:** 3-week consistency rule prevents knee-jerk reactions from one bad week

---

## Session 5: MATRL + Flow GRPO — Dynamic Recruitment + Learning

**Goal:** Design dynamic agent recruitment and the reinforcement learning loop.

### MATRL: 3-Stage Recruitment Protocol

**Stage 1 — Team Formation via YAML Constitution Rules**
The Recruiter is NOT an agent — it's the Pi TeamOrchestrator (Extension #6) executing deterministic YAML rules. Constraints over improvisation. After Sunday meetings, new laws can be proposed and existing constraints reinforced.

```yaml
# YAML Constitution — Agent Recruitment Rules
recruitment_rules:
  perception_only:
    trigger: "task_type in [sentiment, context_extraction]"
    team: [aria, lionel, maeva]
  perception_strategy:
    trigger: "task_type in [ritual_selection, coaching_response]"
    team: [aria, assembler, atlas]
  full_stack:
    trigger: "task_type in [full_coaching_session]"
    team: [aria, assembler, artisan, voice_agent]
  safety_override:
    trigger: "safety_flag == true"
    inject: [liliane]  # added to ANY team
```

**Stage 2 — Experience Injection**
Inject hyper-edges (~200 tokens) for procedural work. Full winning examples (~2000 tokens) for creative work. Context budget adapts per task type.

**Stage 3 — Credit Assignment (Self-Esteem Ledger)**
- Approval = Self-Esteem + (credit per agent based on contribution)
- Testing feedback = LEARNING (no penalty, ACE patches skill)
- Red Flag = INVESTIGATION + PENALTY on specific agent/skill
- Never penalize creativity. Always penalize laziness and AI-sounding output.

### Flow GRPO: Sunday Learning Loop
```
SUNDAY BOT MEETING
├── Collect: approvals, rejections, coach edits
├── Memory Curator → writes to Neo4j (hyper-edges if data-driven)
├── ACE Evolution → SKILL.md patches (if 3-week threshold met)
├── Flow GRPO → reinforces winning reasoning patterns, penalizes drift
└── YAML Constitution → propose new recruitment laws, reinforce constraints
```

**Key Principle:** Constraints and reinforcing constraints = best way to get results. The YAML Constitution evolves just like SKILL.md files — through data-driven proposals after Sunday meetings.

---

## Session 6: Distillation Laws Audit & 8 Fixes

**Goal:** Audit all 29 hypothesis documents (H0-H15) for signal vs. noise, then execute every fix immediately.

### Audit Verdict
The 4-Law framework is **SIGNAL — not noise, not over-engineering**. It channels reasoning from "did we follow the process?" to "did the output actually resonate?"

Two architectural generations identified:
- **Gen 1 (H0-H13):** Mature — paired implementation + analysis docs, 130-383 lines each, 5 micro-hypotheses, validation receipts
- **Gen 2 (H14-H15):** Compact — 47-line design docs without implementation depth

MCDA alignment: **6.5/7 principles fully embodied** by the laws.

### The 8 Fixes Executed

| # | Fix | What Changed |
|:--|:----|:------------|
| 1 | H1 Collapse Test | 3-step protocol: remove T → remove V → remove R → each must be load-bearing |
| 2 | H10 Story Overuse | `deployment_count`, `staleness_flag`, PatternWeaver trigger when all stories stale |
| 3 | H12 Per-Recipe MODE | 8 archetype-specific MODE override tables + Visual Novelty Protocol |
| 4 | Tribe Distiller | **NEW** `tribe-distiller/SKILL.md` — Soul Tribe Psychologist (213 lines) |
| 5 | Receipt Chain | **NEW** `architecture/receipt_chain_guard.md` — dual enforcement (Extension + per-command) |
| 6 | Draft Protocol | **NEW** `architecture/draft_protocol.md` — 3-phase micro-test + micro-breakthrough log |
| 7 | H14 Upgrade | Mirror Session laws: 47 → 200+ lines (full architecture with MH tests + receipt) |
| 8 | H15 Upgrade | Wisdom Forge laws: 47 → 250+ lines (full architecture + Boredom Ban Protocol) |

### Key Decision: H7→H6 Independence is INTENTIONAL
Deep research and fresh research remain independent sources. The juxtaposition/confirmation happens organically at the script composer level. This is a feature, not a gap.

### Boredom Ban Protocol (Lives in H15)
4 checks after generating wisdom briefs:
1. **Déjà Vu Detection** — same combo of insights as last 10 cycles?
2. **Coach Echo Test** — would the coach say "I already know all this"?
3. **Surprise Presence** — is there something unexpected in the data?
4. **Novelty Ratio** — novel elements must outnumber repeated elements per brief

### 6 Intuition Trigger Points Across the Pipeline

| Where | Extension | When It Fires |
|:------|:----------|:-------------|
| H10 Story Inventory | PatternWeaver | All stories in a mode are stale |
| H12 Visual Recipes | SoulResonance | Same framing 3+ consecutive pieces |
| H15 Shadow missing | GhostContext | Can't find contradiction or limitation |
| H15 No surprise | SoulResonance | All briefs are echo chambers |
| H15 Coach echo | AncestralWisdom | Zero new insights for the coach |
| H15 Gap type repeated | PatternWeaver | Same gap type > 3x in last 10 pieces |

---

## Session 7: Integration — The Unified CCP Architecture

**Goal:** Synthesize all 6 sessions into one architectural view. Answer: "How does everything connect?"

### The 5-Layer CCP Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 5: INTUITION (Emergent — grows with data)                │
│  SoulResonance │ PatternWeaver │ GhostContext │ AncestralWisdom  │
│  ← Activated when system detects boredom, monotony, or stuckness│
│  ← Fed by micro-breakthrough log + performance data             │
│  ← NOT forced — they mature with accumulated relational data    │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 4: GOVERNANCE (Deterministic — rules-based)              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │ YAML         │  │ Receipt      │  │ 4 Laws of Content    │   │
│  │ Constitution │  │ Chain Guard  │  │ Distillation (H0-H15)│   │
│  │ (recruitment)│  │ (dual layer) │  │ + Boredom Ban        │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
│  + Self-Esteem Credit System + ACE SKILL.md Evolution           │
│  + Draft Protocol (micro-test before full generation)           │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 3: ORCHESTRATION (Pi Coding Agent — TypeScript)          │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  7 Operational Extensions                                 │  │
│  │  InteractComp → MemoryFolder → DamageControl → ModelRouter│  │
│  │  → TillDone → TeamOrchestrator → SystemSelect             │  │
│  └───────────────────────────────────────────────────────────┘  │
│  Agent Teams (parallel: research) + Chains (sequential: produce)│
├─────────────────────────────────────────────────────────────────┤
│  LAYER 2: EXECUTION (Python Agents + Skills + Tools)            │
│  ┌─────────────┐  ┌────────────────┐  ┌──────────────────────┐ │
│  │  12 CBCS     │  │  72 CCF Skills  │  │  7 Ultimate Tools   │ │
│  │  Agents      │  │  (~19 True Skill │  │  fetch_sacred_voice │ │
│  │  (5 depts)   │  │   ~16 Tool       │  │  calibrate_ttt      │ │
│  │              │  │   ~14 Prompt     │  │  apply_humor_theory  │ │
│  │              │  │   ~23 Hybrid)    │  │  generate_questions  │ │
│  └─────────────┘  └────────────────┘  └──────────────────────┘ │
│  92 Archetype Prompts + 28 Commands + Intelligence Library      │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 1: MEMORY (3-Tier — Neo4j HGM + Supabase)               │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │  Working     │  │  Episodic     │  │  Semantic            │   │
│  │  (task ctx)  │  │  (voice DNA,  │  │  (learned patterns,  │   │
│  │  Dies w/task │  │   sacred SoC) │  │   hyper-edges)       │   │
│  └─────────────┘  └──────────────┘  └──────────────────────┘   │
│  Voice Notes = Supabase + Neo4j pointers (NEVER folded)         │
│  Hyper-edges = data-driven only (1x observe → 3x pattern → 7x) │
│  Memory Curator writes weekly — single writer, quality gate     │
└─────────────────────────────────────────────────────────────────┘
```

### How the Layers Connect

**The Vertical Flow: Request → Output**

```
USER REQUEST arrives at Layer 3 (Pi)
  ↓
InteractComp (Ext #1) → ambiguity check → clarify if needed
  ↓
TeamOrchestrator (Ext #6) reads YAML Constitution (Layer 4)
  → recruits the right agent team (not all 12 — only the needed ones)
  ↓
Receipt Chain Guard (Layer 4) → pre-flight check
  → does this stage have all upstream receipts?
  → AUTHENTICATED or PROVISIONAL? → proceed or block
  ↓
Agents (Layer 2) execute, loading SKILL.md + calling Tools
  → Draft Protocol fires: micro-draft 1 element → test → expand
  → 4 Laws gate every output (Saturation → Mode → Compression → Gate)
  ↓
Boredom Ban (Layer 4) checks for déjà vu, echo, surprise absence
  → triggers Intuition Extensions (Layer 5) when stuck
  ↓
Output validated → Receipt generated → downstream stages unlocked
  ↓
Memory Curator (Sunday) writes learnings to Layer 1
  → ACE patches SKILL.md files with 3-week consistency rule
  → Credit System updates Self-Esteem ledger
  → Hyper-edges promoted if data supports
```

### The Horizontal Flow: Data Across Subsystems

```
CCF (Content)  ←→  CBCS (Coaching)  ←→  V²WS (Webinar)
     ↑                    ↑                    ↑
     └────── SHARED MEMORY (Layer 1) ──────────┘
              Neo4j hyper-edges connect:
              - Coach voice DNA (used by all 3)
              - Tribe profiles (content + coaching + webinar)
              - Performance data (what works WHERE)
              - Story inventory (shared across content formats)
     
     └────── SHARED GOVERNANCE (Layer 4) ──────────┘
              - Receipt chain spans all 3 subsystems
              - YAML Constitution recruits agents for ANY task type
              - Credit system tracks performance across ALL outputs
              - Boredom Ban applies to content, coaching, and webinar
     
     └────── SHARED INTUITION (Layer 5) ──────────┘
              - PatternWeaver finds connections ACROSS subsystems
              - A coaching insight feeds content creation
              - A webinar conversion pattern informs coaching strategy
              - A content performance signal improves webinar hooks
```

### The Receipt Chain Dependency Graph (Complete)

```
SETUP PHASE                    RESEARCH PHASE                    PRODUCTION PHASE
─────────────                  ──────────────                    ─────────────────
H8  (Soul Values)──────┐      H0  (Questions)                   H3  (SoC Voice)──────┐
                       ↓       ↓                                                      ↓
H10 (Philosophy)──────┐H9     H1  (Blueprints)──────────────┐   H14 (Mirror)──────────↓
                      ↓ ↓      ↓                            ↓                         ↓
H11 (Audience)───────→H9      H6  (Deep Research)          H3   H15 (Wisdom Forge)────↓
                       ↓                                          ↓                    ↓
                       ↓       H7  (Fresh Research)         ──→ H15                    ↓
VISUAL PHASE           ↓       [INDEPENDENT by design]                            Script
─────────────          ↓                                                          Generator
H9  (Tribe)──────→ H12 (Visual Recipes) → Art Director
                 → H13 (Visual Assets)  → H5 (Visual Prompts)

Every arrow = a receipt requirement
Every node = a receipt producer
H7→H6 gap = INTENTIONAL (juxtaposition at script composer)
```

### What Session 7 Integrates That Didn't Exist Before

| From Session | Architecture Element | How It Integrates |
|:------------|:--------------------|:------------------|
| Session 1 | ~19 True Skills, ~16 Tools, ~14 Prompts, ~23 Hybrids | Layer 2 — each type loads differently (context vs. function call vs. template) |
| Session 2 | 7 Operational + 4 Intuition Extensions | Layer 3 (Operational) + Layer 5 (Intuition) |
| Session 3 | 3-tier memory (Working/Episodic/Semantic) | Layer 1 — Supabase + Neo4j HGM |
| Session 4 | Hyper-edge promotion + Credit System + ACE evolution | Layer 4 (Governance) + Layer 1 (Memory) |
| Session 5 | YAML Constitution + Sunday Learning Loop | Layer 4 (Governance) |
| Session 6 | Receipt Chain + Draft Protocol + Boredom Ban + Intuition Triggers | Layer 4 (Governance) + Layer 5 (Intuition) |

### The 3 Principles That Hold It Together

1. **Constraints > Instructions.** Every layer enforces constraints (YAML rules, receipt chains, law gates, boredom checks) rather than relying on instructions that LLMs can drift from.

2. **Data > Intuition > Action.** Layer 1 accumulates data → Layer 5 emergent intuition matures → Layer 2 agents act on it. Intuition is never forced — it grows when the data supports it.

3. **Novelty = Awareness. Boredom = Autopilot.** The system optimizes for surprise, not safety. Every governance layer includes a boredom check. Every intuition extension breaks monotony. The cardinal sin is producing output that "sounds AI."
