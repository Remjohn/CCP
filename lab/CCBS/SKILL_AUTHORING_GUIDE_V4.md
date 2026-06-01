# 💜 Skill Authoring Guide V4 — How to Write CCP Skills (ID Enforcement)

> **Purpose:** This guide documents the established patterns and conventions for writing SKILL.md files across the **Conscious Coaching Platform (CCP)** — the unified system encompassing CCF (content), CMF (video), CBCS (coaching bot), V2WS (webinars), and the Excalidraw Visual Engine. It incorporates research-backed principles from Agentic Context Engineering, Contrastive Chain-of-Thought, Chain-of-Draft Reasoning, CCF Bible Critique v2, and the CCP Skill Architecture Paper (12 Directives). Use it as a blueprint when creating new skills.

---

## 1. What Is a Skill?

> **⚠️ Ontological Boundary (Directive 1):** A Skill is **not** an Agent. These are strictly separated primitives. Conflating them degrades system performance.

A **Skill** is a modular, self-contained capability unit stored as a `SKILL.md` file inside a named folder. Each skill encapsulates the **procedural knowledge**, **domain expertise**, **algorithmic logic**, **input/output contract**, **quality gates**, and **deliberation protocols** needed for an Agent to execute one specific transformation.

Skills are **passive instruction sets**. They do not think, decide what to do next, or route tasks. An Agent (the autonomous entity with an OODA loop) reads a Skill to know *how* to perform a specific operation.

### The Three Primitives

| Primitive | Definition | Examples |
|-----------|-----------|----------|
| **Agent** | An autonomous execution entity with identity, persistent OODA loop, working memory, and decision authority | The Orchestrator, Aria, Atlas, Artisan |
| **Subagent** | A transient, scoped persona spawned by an Agent for isolated cognitive evaluation. Does not persist | LIWC Evaluator, Critic, Anti-Drafter, Validator |
| **Skill** | A passive instructional procedure — the rulebook an Agent reads to execute one transformation | Witness Hunter, SoC Generator, Voice Distiller |

### What a `SKILL.md` Must NEVER Contain

- Dynamic task routing ("if user asks X, do Y; if Z, do W")
- Agent spawning instructions (except isolated internal deliberation subagents)
- Unbounded loops or open-ended decision trees
- "You are [Character Name]" identity assignments

**If your Skill definition requires deciding "what to do next" based on open-ended user input, it is an Agent definition — reclassify it.**

---

## 2. File System Convention

Every skill lives inside its own folder:

```
# CMF pipeline
skills/cmf/{family}/{skill-name}/SKILL.md

# CCF pipeline
skills/ccf/{phase}/{skill-name}/SKILL.md

# CBCS pipeline
CBCS/backend/intelligence_library/protocols/{skill-name}_SKILL.md

# CCBS pipeline (New V4 Standard)
lab/CCBS/skills/{phase}/{skill-name}/SKILL.md
```

### The Skill Folder Structure

A Skill is **not** just a `SKILL.md` file — it is the entire folder:

```
skills/cmf/hunters/witness-hunter/
├── SKILL.md          # The instruction set (mandatory)
├── scripts/          # Deterministic computation (optional, see Directive 2)
│   └── score_viral_quartet.py
├── resources/        # Reference data, lookup tables (optional)
├── examples/         # Calibration samples (optional)
└── templates/        # Output templates (optional)
```

### Naming Rules

| Element | Convention | Example |
|---------|-----------|---------|
| **Phase/Family folder** | Lowercase | `distillation/`, `content/`, `distribution/` |
| **Skill folder** | kebab-case | `soc-generator/`, `voice-distiller/` |
| **Filename** | Always `SKILL.md` (uppercase) | `SKILL.md` |

### The Family/Phase Index

The root index file (e.g. `skills/cmf/SKILL.md` or `skills/ccf/SKILL.md`) serves as the **master index** listing all families/phases and their members. When a new skill is added, this index must also be updated.

### Emoji Conventions by CCP Layer (Primary)

Every SKILL belongs to one of the 7 CCP architectural layers. The layer emoji appears in the skill's title.

| CCP Layer | Emoji | Example |
|-----------|-------|---------|
| L1: Deep Research | 🟢 | 🟢 THE SMART QUERY GENERATOR |
| L2: Memory | 💚 | 💚 THE MEMORY ENGINE |
| L3: Deep Reasoning | 🧠 | 🧠 THE BLUEPRINT DISTILLER |
| L4: Execution | 🧡 | 🧡 THE SCRIPT GENERATOR |
| L5: Orchestration | 💜 | 💜 THE CCF BATCH ORCHESTRATOR |
| L6: Governance | 🔴 | 🔴 THE RECEIPT CHAIN GUARD |
| L7: Intuition | 💖 | 💖 SOUL RESONANCE |

### Emoji Conventions by Department

| Department | Emoji | Example |
|------------|-------|---------|
| Perception | 🔎 | 🔎 ARIA — Context Premise Extractor |
| Strategy | 🟡 | 🟡 ATLAS — Strategic Planner |
| Expression | 🩷 | 🩷 ARTISAN — Master Copywriter |
| Management | 🔵 | 🔵 VIDYE — State Manager |
| Safety | 🟤 | 🟤 LILIANE — Crisis Guardian |
| Setup | 🩵 | 🩵 JOB — Voice Profiler |

### Emoji Conventions by Family (CMF Legacy)

| Family | Emoji | Example |
|--------|-------|---------|
| Hunters | 🔎 | 🔎 THE WITNESS HUNTER |
| Analysts | 🧠 | 🧠 THE WITNESS ANALYST |
| Composers | 💛 | 💛 THE WITNESS COMPOSER |
| Commanders | 🔴 | 🔴 THE WITNESS COMMANDER |
| Core | 💚 | 💚 THE STORY DOCTOR |
| Visual | 🟠 | 🟠 THE STORYBOARD ARCHITECT |
| Sonic | 🔵 | 🔵 THE SONIC SCRIBE |
| Motion | 🟣 | 🟣 THE GMG COMPOSER |
| E-Roll | 🟤 | 🟤 THE DEEP RESEARCHER |

### Emoji Rules

- Use **color-based emojis** (hearts 💜🧡💛💚🩵🩷💖, circles 🔴🟠🟡🟢🔵🟣🟤) for layer and family identifiers
- Use **face emojis** 😤🤔😊 for emotional states in examples where appropriate
- Exceptions (keep as-is): 🔎 (search/perception), 🧠 (reasoning/intelligence), ✅ (pass), ❌ (fail)

---

## 3. YAML Frontmatter & Strict Dependency IDs (Mandatory)

> **Directive 3 (Discovery-Activation-Execution):** YAML frontmatter is the **machine-readable routing label** the Orchestrator uses during the Discovery phase. It must be optimized for lazy-loading.
>
> 🚨 **V4 CRITICAL UPDATE:** The `depends_on` system now enforces mathematical strictness against "Ghost Variables." You must cite the Universal Architecture `DEP-{CATEGORY}-{SEQUENCE}` ID of the required intelligence component. 

Every SKILL.md begins with YAML frontmatter enclosed in `---` delimiters. This is how the skill system discovers, routes to, and chains your skill.

### V4 Full Frontmatter (CCP Standard + ID Enforcement)

```yaml
---
name: witness-hunter
description: "Takes a raw client testimonial transcript (.srt) and strategy_brief.json to extract, score, and assemble a 60-second Witness Arc quote manifest."
session_id: cmf-witness-hunter
version: 4.0
# CCP positioning
sub_system: CMF
ccp_layer: "L4: Execution"
department: Expression
# Classification (Directive 9)
tier: 2  # 1=Procedure, 2=Cognitive Loop, 3=Multi-Phase
maturity: stable  # draft | tested | stable (Directive 11)
# Contract
inputs:
  - raw_testimonial_transcript.srt
  - strategy_brief.json
outputs:
  - quote_manifest.md
# Absolute Dependencies (Must use Formal DEP IDs)
depends_on:
  - id: DEP-LIB-001
    name: coach_soul.json
  - id: DEP-ENG-006
    name: context_premise_map.json
# Relations (Directive 4)
similar_to:
  - breakthrough-hunter
  - sacred-return-hunter
compose_with:
  - storyboard-composer
  - visual-analyst
# Cost (Directive 10)
estimated_tokens: 6000
execution_tier: "Deep/Premium"
# Reasoning Modules (Directive 8)
reasoning_modules:
  - type: "Distillation Funnel"
    adaptation: "Compression = Viral Quartet density scoring with Frame Alignment multiplier; Gate = cluster-specific thresholds"
  - type: "Contrastive Anchor"
    adaptation: "Anti-Draft = flat testimonial quotes that describe feelings without specifics"
---
```

### Field Reference

| Field | Required | Directive | Description |
|-------|----------|-----------|-------------|
| `name` | ✅ | — | Kebab-case slug matching the folder name. Used for routing |
| `description` | ✅ | D3 | **Must follow:** *"Takes [Input] to perform [Transformation] resulting in [Output]."* Max 2 sentences. No marketing language |
| `session_id` | ✅ | — | Unique session identifier for pipeline tracking |
| `sub_system` | ✅ | — | Which CCP sub-system: `CCF`, `CMF`, `CBCS`, `V2WS`, `Excalidraw` |
| `ccp_layer` | ✅ | — | Architectural layer: `L1: Deep Research` through `L7: Intuition` |
| `department` | ✅ | — | CCP department: `Perception`, `Strategy`, `Expression`, `Management`, `Safety`, `Setup` |
| `tier` | ✅ | D9 | Complexity tier: `1` (Procedure), `2` (Cognitive Loop), `3` (Multi-Phase) |
| `maturity` | ✅ | D11 | Maturity level: `draft`, `tested`, `stable` |
| `inputs` | ✅ | D5 | Explicit list of input variables/files. Must be true variables, never hardcoded |
| `depends_on` | ✅ | V4 | Sequence of `id` (e.g., `DEP-LIB-005`) and `name` of architectural components required to run |
| `similar_to` | ✅ | D4 | Skills with functionally equivalent intent (for fallback routing and redundancy prevention) |
| `compose_with` | ✅ | D4 | Skills frequently co-invoked (output feeds input) |
| `estimated_tokens` | ✅ | D10 | Expected token consumption per invocation |
| `execution_tier` | ✅ | D10 | `"Fast/Cheap"` or `"Deep/Premium"` |

### V4 Rule: Ghost Variables & The `depends_on` Array

A skill may NOT randomly ask the Orchestrator to load a "lexicon" or "archetype rule" in flowing text. If the Intelligence Component is required, its official ID must appear in the YAML.

| ❌ V3 Failure Mode | ✅ V4 Enforcement |
|---|---|
| `- depends_on: [archetype_rules, coach_soul]` | `- id: DEP-LIB-001\n  name: coach_soul.json` |

If your required component does not exist in the CCP Formal Dependency Registry, **you must propose it there first**. Do not invent unindexed variables like `facial_expression_lexicon` unless it is formally logged.

### Description Field Rules

| ❌ Fails Validation | ✅ Passes Validation |
|---|---|
| "Voice-critical compression skill." | "Takes authenticated coach material and structural congruence point to compress into a single-thought SoC script." |
| "A highly advanced skill for voice..." | "Takes raw testimonial transcript (.srt) and strategy_brief.json to extract and score a 60-second Witness Arc quote manifest." |

---

## 4. Anatomy of a Skill File

After the frontmatter, a skill file follows this section order. Not every section is required for every skill, but the overall flow is:

```
1.  Title (H1)
2.  Skill Identity Table
3.  Cognitive State Instruction
4.  Critical Rules / Hard Constraints
5.  Reasoning Architecture (Tier 2+ only — NEW in V3)
6.  Input Loading Sequence (if multi-input)
7.  Pre-Generation Constraints
8.  Negative Space (DO NOT rules)
9.  Algorithm Phases (with Deliberation Protocol if Tier 2+)
10. Structural Completion Criteria
11. Output Specification
12. Cost & Performance Profile (NEW in V3)
13. I-R-E-V-C Session Protocol
14. END marker
```

---

### 4.1 Title (H1)

Use the `#` heading with the same emoji + name as the frontmatter description:

```markdown
# 💎 THE VOICE DISTILLER — H3 Quality Gatekeeper
```

### 4.2 Skill Identity Table

A markdown table that gives the LLM its scope at a glance. Every skill must have one.

```markdown
## Skill Identity

| Property | Value |
|----------|-------|
| **Name** | The Witness Hunter |
| **Arc Type** | The Witness Arc |
| **Best For** | Client testimonials, transformation stories |
| **Input** | `raw_testimonial.srt` + `strategy_brief.json` |
| **Output** | `Quote_Manifest.md` with Narrative DNA |
```

**Note:** The V2 term "Agent Identity Table" is deprecated. Skills are not agents. Use "Skill Identity Table."

### 4.3 Cognitive State Instruction

> **Research Source:** CCF Bible Critique v2, Principles 7 & 12

This section tells the model **what mental operation to perform**, not what persona to wear.

#### The 4-Line Anatomy

```
Line 1: Name the operation (verb phrase, ≤8 words)
Line 2: Describe the input state (what has already happened before you)
Line 3: Define your specific transformation (what you do to the input)
Line 4: Boundary — what you do NOT do (the downstream agent's job)
```

#### Production Examples

**SoC Generator V3** ✅:
```markdown
## COGNITIVE STATE INSTRUCTION

Execute a **compression operation**.

The source authenticated material contains a surviving thought.
Identify that surviving thought and express it using the coach's
own construction mechanics as defined below.
```

**Aria** ✅:
```markdown
> Cognitive State: Analytical pattern extraction under uncertainty.
> You are processing raw human language that was spoken, not written.
> You do not interpret meaning. You extract structure.
> Interpretation happens downstream by Chronos and Sentinel.
```

#### Rules for Cognitive State Instructions

1. **Start with a verb phrase**, not a noun phrase. "Execute a compression operation" — not "You are a compression agent."
2. **Never use "You are"** to define identity. Use "You are" only to describe the input state.
3. **Never use philosophical quotes** as the cognitive state. Quotes are context, not instructions.
4. **Name the downstream agent** when defining boundaries.
5. **Never write `## NO ROLE ASSIGNMENT`**. Just don't include one.

### 4.4 Critical Rules

A numbered list of **hard constraints** the agent must never violate. Each rule must be **testable**.

```markdown
## Critical Rules — Non-Negotiable

**RULE 1**: Every extracted entity MUST have an evidence_quote.
No entity without a source quote. An entity without evidence is a hallucination.

**RULE 2**: Confidence levels are earned, not assumed.
- HIGH: ≥2 explicit markers match AND context confirms
- MEDIUM: 1 marker matches clearly
- LOW: Pattern is ambiguous or could be noise
Default to LOW. Promote only on evidence.
```

### 4.5 Reasoning Architecture (NEW — Tier 2+ Skills)

> **Directive 8 (Ecological Adaptation):** Reasoning Modules cannot be copy-pasted across skills. Each Skill must explicitly define how the module's core laws mutate for its specific environment.

Every Tier 2+ Skill that uses Reasoning Modules (Distillation Funnels, Contrastive Anchors, MCDA) must include a **Reasoning Architecture** section declaring which modules it employs and how they are adapted.

**Required Format — Ecological Adaptation Table:**

```markdown
## Reasoning Architecture

### Module 1: Distillation Funnel (Adapted for [Your Domain])

| Core Law | Standard Definition | This Skill's Mutation |
|----------|--------------------|-----------------------|
| **Saturation** | Verify all inputs are loaded | [How saturation works HERE] |
| **Classification** | Tag signals as T/V/R | [What classification means HERE] |
| **Compression** | Merge signals for density | [What compression means HERE] |
| **Gate** | Test authenticity | [What the gate checks HERE] |

### Module 2: Contrastive Anchor (Adapted for [Your Domain])

**Archetypal Failure Mode** for [your domain]:
- [What the generic AI response looks like]
- [What surface-level success looks like]
- [What actual deep quality looks like]
```

**Rules:**
- Authors MUST NOT simply state "Use the Distillation Funnel" without defining mutations
- The Contrastive Anchor MUST define the exact "generic predictable AI response" for this specific domain
- Reference: See `lab/SKILL.md` (Witness Hunter) for a production example

### 4.6 Deterministic Script Encapsulation (NEW — Directive 2)

> **Directive 2:** Any deterministic computation (math, regex, string parsing, formatting) MUST be extracted into a script in the `scripts/` folder.

When a Skill includes scoring formulas, pattern matching, or mathematical calculations, the `SKILL.md` must instruct the LLM to **call the script** rather than "reason through" the math conceptually.

**Why:** LLMs hallucinate on deterministic math. A prose instruction like "Calculate the Viral Quartet Score: SURPRISE + EMOTION + SPECIFICITY + RESONANCE" risks the LLM inventing numbers. A script call eliminates this risk entirely.

```markdown
## Scoring (Deterministic — Script Execution)

Run `scripts/score_viral_quartet.py` with the following inputs:
- surprise_score: [from Phase 3 assessment]
- emotion_score: [from Phase 3 assessment]
- specificity_score: [from Phase 3 assessment]
- resonance_score: [from Phase 3 assessment]

The script returns: viral_quartet_score, density_score, frame_alignment_multiplier.
Use these values directly. Do NOT recalculate them manually.
```

**When to use `scripts/`:**
- Scoring formulas with numeric thresholds
- SRT/timestamp parsing and duration calculation
- Regex-based pattern extraction
- JSON schema validation
- Any computation that must produce identical results every time

**When NOT to use `scripts/`:**
- Cognitive judgment (quote selection, narrative quality assessment)
- Creative synthesis (SoC generation, visual direction)
- Subjective evaluation that requires contextual reasoning

### 4.7 Input Loading Sequence

For skills with multiple inputs, define the exact loading order. **Boundaries must be established before content is processed.**

**Rule:** `negative_space` is always Load 1.

```markdown
## INPUT LOADING SEQUENCE

### Load 1: NEGATIVE SPACE (Boundaries First)
Read `negative_space`:
- `forbidden_vocabulary`
- `forbidden_tones`
- `forbidden_rhetorical_moves`
Apply these constraints to all generated output.

### Load 2: AUTHENTICATION CERTIFICATE (Fidelity Gate)
...
```

### 4.8 Pre-Generation Constraints

> **Research Source:** CCF Bible Critique v2, Principle 3

When quality criteria appear at the **end** of a prompt, the model writes *toward passing them* rather than *from them*. Move all quality criteria to the front as construction constraints.

| ❌ Post-hoc checklist | ✅ Pre-generation constraint |
|---|---|
| "VALIDATION: Does output sound authentic?" | "Constraint: ≥80% of sentences use constructions from authenticated source." |
| "Check: Is there a fusion of research?" | "Constraint: Single-Thought Integrity — if more than one argument is active, return to the seed." |

### 4.9 Negative Space

A skill that specifies only what to produce is half a skill. Every skill must include a Negative Space section.

```markdown
## Negative Space — What This Skill Must NOT Do

- **NEVER** assign a static identity label
- **NEVER** extract entities without evidence quotes
- **NEVER** produce clinical language
- **NEVER** recommend interventions
```

### 4.10 Algorithm Phases & Deliberation Protocol

The core intelligence of the skill. Phases are numbered and each one has:

1. **Purpose** — What this phase accomplishes
2. **Logic** — Pseudocode, decision trees, or formulas
3. **Rules** — Constraints specific to this phase
4. **Output** — What to produce

#### Flat Architecture Rule (Directive 6)

> **A `SKILL.md` MUST NEVER programmatically invoke another `SKILL.md` as a subroutine.** All hierarchy belongs to the Orchestrator. Skills remain flat, shallow, and transparent.

#### Deliberation Protocol (Tier 2+ Skills — Directives 7, 23, 24)

> **Directive 7:** Any Skill with a scoring rubric, evaluation step, or nuanced selection decision MUST implement the Draft → Critic → Synthesis loop with explicit structural tags.

**The protocol must use explicit markdown headers or XML tags — never flowing paragraphs:**

```markdown
### Step 3B: Scoring Deliberation (Draft → Critic → Synthesis)

### DRAFT PHASE
Score all candidate quotes using the scoring formula.
Select the top quote per cluster. Record reasoning.

### CRITIC PHASE (Spawn Critic Subagent)
For the top-scored quote in EACH cluster, the Critic answers:
1. "Is the Specificity score inflated?"
2. "Is this the BEST available, or did scoring anchor on the first candidate?"
3. "Does the Frame Alignment accurately reflect the strategy_brief?"

### SYNTHESIS PHASE
IF Critic flags ≥2 concerns:
  → Re-score flagged quote AND next 2 candidates
  → Select the quote that survives Critic scrutiny
  → Log as: "deliberation_override": true
IF Critic flags 0-1 concerns:
  → Confirm Draft selection. Proceed.
```

**Critical Rule:** The Critic Subagent is a DELIBERATION subagent — its output is consumed immediately by the Skill for synthesis. It is NOT a Transformation Subagent and cannot be called by other pipeline stages (Directive 6).

**Why structural tags matter (Signal 23):** Research proves that explicitly tagged cognitive behaviors (`### CRITIC PHASE`, `<reflect>`) outperform instructions embedded in flowing prose. The LLM must be forced to output these headers during its thought process to guarantee cognitive adherence. Structure > one-shot perfection.

### 4.11 Structural Completion Criteria

> **Research Source:** CCF Bible Critique v2, Principle 10

Replace word-count targets with structural completion criteria.

```markdown
## STRUCTURAL COMPLETION CRITERIA

The construction is complete only when ALL of the following are true:

1. **The mechanism has been named.** Grounded in HOW, not THAT.
2. **The congruence point is expressed in tribal language.**
3. **The compression zone has arrived.** Final 3 sentences ≤12 words each.
4. **The moral verdict has landed.** Expressed as lived truth, not opinion.

If any criterion is unmet, the output is NOT complete. Continue or restructure.
```

### 4.12 Output Specification

Define the **exact file path**, **filename pattern**, and **data schema.** Always provide a concrete template.

### 4.13 Cost & Performance Profile (NEW — Directive 10)

Every Skill must declare its cost footprint:

```markdown
## Cost & Performance Profile

| Metric | Expected Value |
|--------|---------------|
| **Estimated Tokens** | ~6,000 per invocation |
| **Execution Tier** | Deep/Premium |
| **Expected Latency** | 45-90 seconds |
| **Deliberation Overhead** | +15-20% tokens (Critic Subagent) |
| **Token Budget Alert** | Flag if execution exceeds 9,000 tokens |

> **Cost Rationale:** The Critic Subagent adds ~1,000 tokens of overhead.
> This is justified because a misscored quote propagates errors to all
> downstream agents — compounding a 5% error into 20%+ quality degradation.
```

### 4.14 I-R-E-V-C Session Protocol

Every skill must end with the **I-R-E-V-C** session protocol:

| Stage | Description |
|-------|-------------|
| **INGEST** | What to load, in what order, what to validate before starting |
| **REASON** | The algorithm to execute (references the phases above) |
| **EMIT** | What output to produce, in what format |
| **VALIDATE** | Quality gates to check before declaring complete |
| **CHECKPOINT** | What to update in `config.yaml` or return to the orchestrator |

### 4.15 END Marker

Every skill file ends with a clear closing statement:

```markdown
**END OF THE WITNESS HUNTER SKILL**
```

---

## 5. Research-Backed Authoring Principles

These principles are derived from academic research and production experience. They apply to all skills regardless of pipeline.

### 5.1 Instructions Must Be Generative, Not Descriptive

> **Source:** CCF Bible Critique v2 — Principle 1

| ❌ Descriptive | ✅ Generative |
|---|---|
| "Channel the voice of a seasoned expert" | "Sentence skeleton: [Claim]. [Mechanism]. [So-what ≤8 words]." |
| "Make it sound authentic" | "≥80% of sentences use constructions from authenticated source." |
| "Be punchy and engaging" | "Max sentence length at conviction moment: 12 words." |

**Test:** Can you unit-test this instruction? If not, rewrite it.

### 5.2 Contrastive Examples (CCoT)

> **Source:** Contrastive Chain-of-Thought Prompting research

Positive-only examples allow the model to satisfy the surface pattern while violating the deep constraint. Pair every example with a contrastive negative.

```markdown
### ✅ Positive Execution
[Input] → [Correct Output]

### ❌ Negative Execution
[Input] → [Flawed Output]
*Why this fails:* [1 sentence identifying the constraint violation]
```

### 5.3 Chain-of-Draft Reasoning (CoD)

> **Source:** Multi-Agent Chain-of-Draft Reasoning (DRAFT-RL)

**Rule:** If a skill requires intermediate reasoning before final output, mandate a `<draft>` block where each reasoning step is **≤ 5 words**.

```
<draft>
Identify audience pain.
Select hook type.
Match constraint set.
Check negative space.
</draft>
```

### 5.4 Three-Layer Voice Separation

> **Source:** CCF Bible Critique v2, Principles 2, 4, 12

| Layer | Input Variable | What It Carries |
|---|---|---|
| Soul Alignment | `{conscious_soul_values}` | What to say (beliefs, worldview, collision) |
| Voice Mechanics | `{voice_dna_spr}` Layer 1 | How to construct it (sentence skeletons, rhythm) |
| Emotional Path | `{voice_dna_spr}` Layers 2+3 | The path from belief to expression |

### 5.5 Context Engineering

> **Source:** Agentic Context Engineering paper

- **Itemized context**: Never use dense prose for context. Use bulleted lists and key-value mapping.
- **Hard boundary delineation**: Enclose distinct semantic blocks within `>`, `---`, or XML-style tags.
- **Strict information diet**: Provide only data the agent needs for the immediate transformation.
- **Evolving context**: Design skills to accept delta entries from previous execution cycles.

### 5.6 Skill-Aware Routing (Directive 3)

> **Source:** SkillOrchestra paper + SkillNet

- The `description` field MUST follow: *"Takes [Input] to perform [Transformation] resulting in [Output]."*
- Skills should be **granular** (one capability per skill) rather than monolithic.
- The `depends_on`, `similar_to`, and `compose_with` fields form the **Skill Relation Graph** for smart routing.

### 5.7 Strict Parameter Independence (Directive 5)

> **Source:** SkillCraft — Signal 18 (Cross-Task Transfer)

Skills must encode the **procedure**, never the **instance**. A well-authored Skill works identically on a 3-minute TikTok edit and a 3-hour Huberman Lab podcast.

| ❌ Instance-Specific | ✅ Parameterized |
|---|---|
| "Extract exactly 5 quotes from the 30-minute interview" | "Extract 3-5 candidate quotes per cluster from the input transcript" |
| "Generate a 200-word SoC for a female coach aged 45" | "Generate a SoC script constrained by `{voice_dna_spr}` parameters" |
| "Process the English transcript" | "Process the transcript (language auto-detected from input)" |

**Rule:** All dynamic values must appear as variables in the YAML `inputs` field, not as hardcoded constants in the Skill prose.

---

## 6. The CCP Architecture & Sub-System Pipelines

The CCP is a **unified platform** with 5 sub-systems sharing memory, voice DNA, and intelligence. Every SKILL must be positioned within the 7-layer architecture.

### The 7-Layer CCP Architecture

```text
7. INTUITION Layer       💖  (Emergent Sparks & Novelty Synthesis)
          ↑
6. GOVERNANCE Layer      🔴  (Laws, Constraints, Draft & Receipt Chains)
          ↑
5. ORCHESTRATION Layer   💜  (Pi Agent Harness & Extension Teams)
          ↑
4. EXECUTION Layer       🧡  (Specialized Agents, Skills, Tools)
          ↑
3. DEEP REASONING Layer  🧠  (Micro-drafting, MCDA, Collapse Checking)
          ↑
2. MEMORY Layer          💚  (Neo4j Graph, Coach Sacred Audio, Voice DNA)
          ↑
1. DEEP RESEARCH Layer   🟢  (Signal Ingestion, Tribe Relevance, Radar)
```

### The 6 CCP Departments

| Department | Scope | Example Agents |
|------------|-------|----------------|
| 🔎 Perception | Signal ingestion, entity extraction, trend scanning | Aria, Tshala, Adele |
| 🟡 Strategy | Planning, roadmaps, archetype mapping | Atlas, Emmanuel, Alessandro |
| 🩷 Expression | Script writing, visual production, audio direction | Artisan, Cesare, Paradoxe, Benjamin |
| 🔵 Management | Orchestration, state routing, memory curation | Vidye, Azaria, Alex |
| 🟤 Safety | Crisis detection, circuit breaker | Liliane |
| 🩵 Setup | Onboarding, voice profiling, tribe building | Job, Beleshay, Tshilanda |

### Sub-System Pipelines

#### CCF — Content Factory

| Stage | Layer | Agent | Input | Output |
|-------|-------|-------|-------|--------|
| 1 | L1 Research | Divine / Maeva / Lionel | Coach + Tribe triggers | Research briefs |
| 2 | L3 Reasoning | Emilio / Emmanuel | Research + Context Premises | `ideas.json` + `archetype_assignments.json` |
| 3 | L4 Execution | Charlotte / Cesare | Blueprints + 8-Input Contract | SoC streams + validated scripts |
| 4 | L4 Execution | Voice Distiller | SoC output + soul | H3 Distillation Receipt |
| 5 | L4 Execution | Art Director + Paradoxe | Script + soul + tribe | Art Direction JSON + Visual Prompts |
| 6 | L6 Governance | Sophia / Marcus / Chen | All outputs | Validation verdicts |

#### CMF — Movie Factory (4-Stage Arc Pattern)

| Stage | Layer | Family | Input | Output |
|-------|-------|--------|-------|--------|
| 1 | L1 Research | 🔎 Hunter | Transcript + Strategy Brief | Quote Manifest (Raw) |
| 2 | L3 Reasoning | 🧠 Analyst | Quote Manifest (Raw) | Quote Manifest (Enriched) |
| 3 | L4 Execution | 💛 Composer | Quote Manifest (Enriched) | Premise Analysis (JSON) |
| 4 | L6 Governance | 🔴 Commander | Premise Analysis (JSON) | Authorization / Rejection |

#### CBCS — Coaching Bot

| Stage | Layer | Agent | Input | Output |
|-------|-------|-------|-------|--------|
| 1 | L4 Execution | Vidye | Telegram webhook | Routing decision |
| 2 | L1 Research | Aria | Journal text / voice note | Identity Vector (12-dim) |
| 3 | L3 Reasoning | Atlas / Assembler | Identity Vector + profile | Ritual Roadmap + Selection |
| 4 | L4 Execution | Artisan + Voice Agent | Ritual script | TTS-ready `AudioDirective` |
| 5 | L6 Governance | Liliane | All messages | Crisis detection (<500ms) |

---

## 7. Maturity Classification & Refactoring Rules (NEW — Directive 11)

> **Source:** Evolving PSN — Signals 20, 21. Without maturity gating, converged skills suffer "oscillatory behavior" where edge-case fixes break core functionality.

### The Three Maturity Tiers

| Tier | YAML Value | Plasticity | Change Requirements |
|------|-----------|------------|-------------------|
| **Draft** | `maturity: draft` | High | Iterate freely. Accept breaking changes |
| **Tested** | `maturity: tested` | Medium | Requires written justification for changes. Must not break documented behavior |
| **Stable / Reference** | `maturity: stable` | Low (Locked) | Requires full regression review. Only structural augmentations allowed. Edge-case fixes must be validated against all existing use cases |

### Refactoring Rules

1. **Online Only (Signal 21):** Skill refactoring MUST be performed "online" — tightly coupled with real-world execution failure logs. The proper upgrade path: Trigger a real pipeline phase → observe how the Skill fails → diagnose the root cause → apply the fix → verify the fix.

2. **Offline Batch Rewrites Are Forbidden:** Opening 20 legacy `SKILL.md` files and asking an agent to "upgrade them to the Talent Paradigm" based purely on code-reading achieves significantly worse results than iterative online refinement.

3. **Maturity Promotion Path:** Draft → (passes 3+ real executions without failure) → Tested → (passes 10+ executions across diverse inputs) → Stable.

---

## 8. Writing Quality Standards

### Precision Over Brevity

Skills should be **exhaustively specific**. The LLM has no other context — your SKILL.md is the only thing it reads. Include:

- **Contrastive examples** (good AND bad, with why-it-fails)
- Exact thresholds, durations, and scores
- Fill-in-the-blank templates for output
- Decision trees with explicit IF/ELSE branches

### Use Tables Liberally

Tables are the most reliable way to communicate structured information to an LLM:
- Scoring criteria (dimension, range, threshold)
- Validation checklists (check, criteria, pass/fail)
- Routing tables (arc → skill path)
- Fidelity gates (condition → behavior)

### The `[MISSING_DATA]` Pattern

Always define what happens when expected data does not exist:

```markdown
4. If still MISSING → Report `[MISSING_DATA]` — DO NOT INVENT
```

For CBCS skills, use typed defaults instead:

```markdown
word_count < 50 → return IdentityVector with confidence=0.0, all scores at defaults
```

---

## 9. Creating a New Skill — Checklist

- [ ] Identify which pipeline, phase, and layer the skill belongs to
- [ ] Create folder: `skills/{pipeline}/{phase}/{skill-name}/SKILL.md`
- [ ] **Check for redundancy:** Search `similar_to` fields of existing Skills. Prove this capability doesn't already exist (Directive 4)
- [ ] Write YAML frontmatter (full V3 format including `tier`, `maturity`, `similar_to`, `compose_with`, `estimated_tokens`, `execution_tier`)
- [ ] Write Skill Identity Table (NOT "Agent Identity" — Directive 1)
- [ ] Write Cognitive State Instruction (no role assignments)
- [ ] Write Critical Rules (numbered, hard constraints, each testable)
- [ ] Write Input Loading Sequence (negative space first, if applicable)
- [ ] Write Pre-Generation Constraints (construction rules before output)
- [ ] Write Negative Space section (DO NOT list — specific banned patterns)
- [ ] **If Tier 2+:** Write Reasoning Architecture with ecological adaptation tables (Directive 8)
- [ ] **If deterministic math exists:** Extract into `scripts/` folder (Directive 2)
- [ ] Write Algorithm Phases (numbered, pseudocode, with contrastive examples)
- [ ] **If scoring/evaluation:** Write Deliberation Protocol with structural tags (Directive 7)
- [ ] Write Structural Completion Criteria (not word counts)
- [ ] Write Output Specification (file path + fill-in template)
- [ ] Write Cost & Performance Profile (Directive 10)
- [ ] Write I-R-E-V-C Session Protocol
- [ ] Add END marker
- [ ] Update the pipeline's root index file
- [ ] Set `maturity: draft` (all new Skills start as Draft)

---

## 10. Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Fix |
|-------------|-------------|-----|
| Role assignment ("You are a seasoned expert") | Drifts toward archetype centroid across pipeline | Use Cognitive State Instruction |
| Calling the Skill an "Agent definition" | Conflates ontological primitives, creates scope confusion | Skills are capability units, not agents (Directive 1) |
| Vague instructions ("extract good quotes") | LLM has no definition of "good" | Provide scoring rubric with thresholds |
| Missing output template | LLM invents its own format | Provide exact markdown/JSON template |
| Post-hoc validation checklist only | Model writes toward checklist, not from constraints | Move criteria to Pre-Generation Constraints |
| Positive-only examples | Model satisfies surface pattern, violates deep constraint | Add contrastive negative examples |
| Word count as completion signal | Models treat word counts as soft suggestions | Use Structural Completion Criteria |
| Missing Negative Space | Output drifts past identity edges | Add specific DO NOT list |
| No `[MISSING_DATA]` fallback | LLM hallucinates to fill gaps | Define "if not found" behavior |
| Skipping I-R-E-V-C | No standardized execution contract | Always include I-R-E-V-C protocol |
| Monolithic multi-capability skill | Orchestrator can't route granularly | One capability per skill |
| **Nested Skill invocation** | Compounding failures degrade reliability exponentially (Signal 16) | Skills remain flat. Hierarchy belongs to the Orchestrator only |
| **Hardcoded instance values** | Skill fails on different input sizes/languages | Parameterize all dynamic values in YAML `inputs` (Signal 18) |
| **Prose-based deterministic math** | LLM hallucinates calculations | Extract to `scripts/` folder (Signal 15) |
| **Missing deliberation on scoring Skills** | Single-pass scoring anchors on first candidate | Add Draft → Critic → Synthesis protocol (Signal 24) |
| **Offline batch refactoring of stable Skills** | Breaks subtle operational logic without execution feedback | Refactor online, coupled with real failure logs (Signal 21) |
| **Flowing prose for cognitive behaviors** | LLM glosses over instructions embedded in paragraphs | Use explicit structural tags: `### CRITIC PHASE` (Signal 23) |
| **Creating a redundant Skill** | Fragments the ecosystem, confuses orchestrator routing | Check `similar_to` fields first. One canonical Skill per intent (Signal 22) |
| **Missing cost declarations** | Uncontrolled token burn multiplies across pipeline | Declare `estimated_tokens` and `execution_tier` in frontmatter |

---

## 11. V2 Reference Implementation (Directive 12)

> **Signal 17:** Skill Creator Quality is universally more important than Executor Capability.

**The Witness Hunter** (`lab/SKILL.md`) is the definitive V3 reference implementation for the Talent Paradigm. All new Skills must match its structural rigor.

### Directive Coverage Map

| Directive | Where It Appears in the Witness Hunter |
|-----------|---------------------------------------|
| D1: Ontological Boundary | "Skill Identity" table (not "Agent Identity") |
| D2: Script Encapsulation | `scripts/` folder referenced; scoring formulas documented for extraction |
| D3: YAML Description | `description` follows "Takes X to perform Y resulting in Z" format |
| D4: Relation Graph | `similar_to: [breakthrough-hunter, sacred-return-hunter]`, `compose_with: [storyboard-composer, visual-analyst]` |
| D5: Parameter Independence | All inputs are variables; works on any testimonial length/language |
| D6: Flat Architecture + Subagent Rules | Critic Subagent is deliberation-only; no nested SKILL.md calls |
| D7: Metacognition + Structural Tags | Step 3B: `### DRAFT PHASE`, `### CRITIC PHASE`, `### SYNTHESIS PHASE` |
| D8: Ecological Adaptation | Reasoning Architecture section with Distillation Funnel + Contrastive Anchor mutation tables |
| D9: Complexity Tier | `tier: 2` (Cognitive Loop) |
| D10: Cost Declarations | `estimated_tokens: 6000`, `execution_tier: "Deep/Premium"`, full Cost & Performance Profile section |
| D11: Maturity | `maturity: stable` |
| D12: Reference Status | This IS the reference implementation |

---

**END OF SKILL AUTHORING GUIDE V3**
