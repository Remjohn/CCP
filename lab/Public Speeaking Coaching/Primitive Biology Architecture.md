# Primitive Biology Architecture

## Status

This document is the **source of truth** for how primitives should be integrated into the Conscious Coaching Platform.

Its purpose is to prevent 3 failure modes:

1. treating primitives as vague words inside prompts
2. over-agentifying primitives into noisy runtime actors
3. flattening unlike primitives into one generic schema

The governing goal is clear:

**primitives should give CCP more taste, discernment, and precision at the right time without adding noise to the context.**

---

## Core Decision

The correct architecture is **not**:

- primitives as independent sub-agents
- primitives as mere Python tools
- primitives as static labels in a prompt library

The correct architecture is:

**primitives as encoded expressive units that are selectively activated, transcribed, composed, executed, validated, and updated through feedback.**

The best biological metaphor is therefore:

`DNA -> expression control -> RNA -> synthesis -> behavior -> selection`

This gives us the right balance between:

- stable ontology
- JIT intelligence orchestration
- recursive reasoning
- validator-driven quality control
- future SFT / DPO / RL integration

---

## V2 refinement

This second version sharpens the biology model with 4 important distinctions:

1. `DNA is more stable than RNA`
2. `DNA is double-stranded while RNA is single-stranded`
3. `DNA stays protected in the nucleus while RNA travels outward for execution`
4. `DNA language and RNA language should not be identical`

These distinctions matter because they help us separate:

- ontology from expression
- truth from local adaptation
- canonical definition from execution instruction
- central governance from edge synthesis

---

## Why DNA/RNA is better than “agents” or “cells” alone

The earlier `cell` metaphor was directionally useful because primitives are not inert. They have conditions, effects, compatibilities, and failure modes.

But `DNA/RNA` is more precise for system design.

Why:

- DNA stores possibility without forcing expression
- expression depends on context, not just existence
- the same encoded unit can produce different outcomes in different environments
- regulation matters as much as the code itself
- some information becomes active, most stays silent
- outputs are selected by survival or performance, not intention alone

That maps almost perfectly to CCP.

A primitive should exist as **encoded capability** inside the platform.
It should only become active when:

- the audience state fits
- the archetype fits
- the mood fits
- the medium fits
- the risk tolerance fits
- the goal requires it

This is exactly what we want from CCP:

**precision without unnecessary context expansion.**

---

## The 4 new governing laws

### Law 1. Registry Stability Law

Primitive ontology must change much more slowly than runtime expression logic.

That means:

- registry changes are rare
- registry changes are reviewed
- registry changes are versioned
- generators cannot casually mutate ontology

The registry is sovereign.
It should behave like protected DNA, not live improvisation.

### Law 2. Double-Strand Law

Every primitive must be defined by both:

- what it is structurally
- what it is expected to do behaviorally

This is crucial.
If we define primitives only by structure, they become theory.
If we define them only by outcome, they become vague optimization targets.

The primitive must therefore have 2 strands:

- `Structural strand`
- `Effect strand`

### Law 3. Expression Translation Law

Ontology language and execution language must be different.

Primitive definitions should stay formal, canonical, and durable.
Primitive expression instructions should stay compact, local, and actionable.

So:

- DNA language = stable ontology language
- RNA language = short expression language

This prevents the runtime from carrying giant philosophical payloads.

### Law 4. Nucleus Protection Law

The registry should remain centralized and protected, while expression plans travel outward to local generators.

This means the system should preserve a clear boundary between:

- central truth
- local synthesis

That is how CCP avoids ontology drift across CCF, CMF, CBCS, CVE, Telegram, and V2WS.

---

## The official CCP biological mapping

### 1. DNA = Primitive Registry

This is the canonical ontology.

It stores:

- primitive identity
- family
- formal definition
- mechanism
- activation conditions
- suppression conditions
- ethical risks
- compatibility rules
- evaluator bindings
- training bindings

DNA is stable.
It should change slowly and deliberately.

It should also be treated as a **nucleus-bound layer**:

- curated
- version-controlled
- minimally editable
- protected from ad hoc runtime rewriting

The registry is not a sandbox.
It is constitutional infrastructure.

### 2. Epigenetics = Runtime context

This is the live regulation layer.

It includes:

- mood state
- archetype
- coach voice DNA
- audience maturity
- context premise
- trigger type
- platform
- time horizon
- content surface
- conversational layer
- risk / sensitivity

Epigenetics determines what is expressible now.

A primitive may exist in the registry and still be inactive because the current state should suppress it.

### 3. Transcription = JIT expression planning

This is where encoded possibility becomes an active plan.

The system reads:

- primitive registry
- runtime context
- audience evidence
- research findings
- current objective

And produces a typed artifact:

`Primitive_Expression_Plan`

This is the most important runtime object in the whole architecture.

It should answer:

- which primitives should fire
- why these primitives were selected
- how strongly they should be expressed
- in what order they should appear
- on which surface they should manifest
- what risks should be constrained

This is where DSPy and recursive reasoning are highly valuable.

### 4. RNA = Active expression instructions

Once the plan is chosen, the selected primitives become short, structured instructions that downstream generators can execute.

This is not long philosophy.
This is compact actionable expression logic.

RNA should be treated as:

- temporary
- context-bound
- disposable
- regenerable

It is not truth.
It is local expression.

Example:

- `Use Tribal Reference at medium strength in opening line`
- `Create What-Is / What-Could-Be contrast in beat 2`
- `Use Auditory POV shift at emotional turn`
- `Reserve STAR peak for final third`

RNA must stay compact because it is the translation layer between strategy and generation.

### 5. Ribosome = Execution stack

This is the generation layer that converts instructions into outputs:

- CCF scripts
- CMF visual briefs
- CVE compositions
- Telegram responses
- V2WS modules
- Sonic Sommelier / Sonic Scribe briefs
- roleplay or coaching dialogue

The ribosome does not decide ontology.
It synthesizes outputs from already-regulated instructions.

### 6. Proteins = Observable content behaviors

These are the actual produced behaviors in the output:

- a hook
- a reframe
- a mirrored sentence
- a contradiction turn
- a visual focal path
- a pause
- a sonic motif
- a closing line

This is what users actually encounter.

### 7. Immune System = Validators

These protect the organism from bad expression.

Validators should check:

- resonance
- surprise
- feeling
- coherence
- ethics
- coach fidelity
- audience fit
- anti-slop
- medium fit

The validator layer determines whether primitive expression was healthy, weak, excessive, manipulative, or off-target.

### 8. Selection Pressure = Real-world outcomes

This is the feedback layer.

Reality updates the system through:

- coach approval
- save/share behavior
- retention
- reply depth
- click behavior
- conversion
- emotional response
- revision burden
- publish / reject decisions

This is what lets the architecture evolve instead of remaining theoretical.

---

## Double-strand primitive design

The strongest implication of the DNA metaphor is that a primitive should be modeled as a double-stranded object.

### Strand A. Structural strand

This defines what the primitive is made of.

Examples:

- its family
- its cues
- its formal mechanism
- its compositional role
- its activation and suppression conditions

### Strand B. Effect strand

This defines what the primitive is expected to change in the audience or the interaction.

Examples:

- trust lift
- surprise lift
- feeling lift
- memory lift
- action lift
- misuse risk

Without the structural strand, the primitive becomes a motivational slogan.
Without the effect strand, it becomes an inert taxonomy label.

CCP needs both.

### Example: Tribal Reference

Structural strand:

- in-group language
- symbolic cues
- culturally loaded phrases
- identity-specific frames

Effect strand:

- increases belonging
- lowers social distance
- increases recognition
- may raise exclusion risk if mismatched

### Example: What Is / What Could Be

Structural strand:

- alternating present/future contrast
- tension gap between current state and desired state
- explicit movement architecture

Effect strand:

- increases desire
- increases discomfort with current reality
- increases forward motion
- may create aspiration inflation if overused

This double-strand model should become mandatory in the registry.

---

## Nucleus, cytoplasm, and edge execution

The location difference between DNA and RNA is useful for CCP architecture.

### Nucleus

This is where core truth stays:

- primitive registry
- ontology rules
- ethical boundaries
- interaction rules
- version history

This layer should be shared across the whole ecosystem.

### Cytoplasm

This is the orchestration environment where active plans are assembled:

- context loading
- epigenetic gating
- JIT reasoning
- DSPy transcription
- expression planning

This is where static possibility becomes local decision.

### Ribosomes / edge execution

This is where the plan becomes an output in a specific subsystem:

- CCF script generation
- CMF visual orchestration
- CVE perceptual composition
- Telegram response generation
- V2WS module composition
- Sonic Sommelier / Sonic Scribe execution

This separation is strategically important:

**truth stays centralized; expression travels outward.**

---

## DNA language vs RNA language

One of the most useful refinements is to separate the language of ontology from the language of execution.

### DNA language

DNA language should be:

- formal
- canonical
- stable
- system-readable
- versionable

Example:

`Tribal Reference = a connection primitive using in-group symbols, language, and identity cues to reduce social distance and increase belonging when authentic audience alignment is present.`

### RNA language

RNA language should be:

- compact
- local
- actionable
- surface-specific
- disposable after execution

Example:

`Opening line: use one tribe-native phrase and one lived cue to signal "I know this world" without slang overreach.`

This distinction matters because too many systems leak ontology directly into prompts.
That creates noise, repetition, and context bloat.

CCP should instead:

- store ontology centrally
- translate it into short local expression instructions
- discard the temporary expression layer after use

---

## Stability classes

Not all primitive-related objects should have the same stability.

### Class A: DNA-stable

Changes rarely.

Examples:

- primitive ids
- family definitions
- ethical red lines
- core mechanism definitions
- compatibility rules

### Class B: regulatory-stable

Changes occasionally as the architecture matures.

Examples:

- validator formulas
- interaction matrices
- epigenetic gating logic
- primitive scoring dimensions

### Class C: RNA-volatile

Changes every run.

Examples:

- expression plans
- angle reports
- hearing briefs
- closure plans
- primitive mixes

This stability hierarchy should shape implementation decisions, storage rules, and version control.

---

## What primitives are and are not

### Primitives are

- encoded expressive units
- typed human-state operators
- ingredients for reasoning, evaluation, and training
- composable pieces of taste and discernment
- activatable under conditions

### Primitives are not

- standalone creative personalities
- universal templates
- single prompt tags
- equal in structure or effect
- guaranteed to improve an output merely by being named

The key formulation is:

`primitive(context) -> expected_delta_in_human_state`

Human state here includes:

- attention
- trust
- curiosity
- tension
- recognition
- emotional vividness
- memorability
- action readiness

This is the level primitives should ultimately be optimized against.

---

## Why primitives should not be independent sub-agents

There will be strong temptation to make every primitive an “agent.”
That is usually a mistake.

If primitives become independent agents, we get:

- too much runtime chatter
- excessive latency
- diffuse accountability
- ontology drift
- prompt duplication
- creative committee syndrome

Primitives are too small and too foundational to become autonomous personalities.

They should mostly live as:

- registry objects
- expression logic
- validation targets
- training labels

Not actors.

---

## When agents do make sense

Agents are still useful, but at a different layer.

Good agent candidates are:

- `Perceptual_Angle_Finder`
- `Primitive_Mix_Selector`
- `Conversation_Layer_Matcher`
- `Narrative_Arc_Planner`
- `Visual_Attention_Planner`
- `Sonic_Hearing_Brief_Planner`
- `Primitive_Validator`

These agents are not primitives.
They are **regulatory organs** that inspect context and control expression.

So the rule is:

**primitives are genes, agents are regulators.**

---

## Where DSPy and Python tools fit

DSPy should sit in the **transcription layer**, not the ontology layer.

That means DSPy is ideal for producing typed artifacts like:

- `PerceptualAnglesReport`
- `PrimitiveExpressionPlan`
- `NarrativeTensionMap`
- `ConversationMatchReport`
- `ClosurePlan`
- `VisualAttentionPlan`
- `HearingBrief`

Python tools are best used for:

- schema enforcement
- validation pipelines
- receipt generation
- score aggregation
- feature extraction
- labeling workflows
- analytics and outcome tracking

So the clean separation is:

- ontology = registry
- reasoning = DSPy / recursive language modules
- enforcement = Python tools
- synthesis = generation model
- judgment = validators

---

## The official CCP primitive stack

### Layer 0. Signal features

These are the smallest observable cues.

Examples:

- expectation mismatch
- identity cue
- emotional disclosure
- status pressure
- taboo marker
- unresolved question
- intimacy marker
- focal contrast
- sonic density shift

These are closer to atoms.

### Layer 1. Primitive units

These are the canonical expressive operators.

Examples:

- Tribal Reference
- Irony Inversion
- Matching Principle
- Throughline
- Pinch and Ouch
- STAR Moment
- Auditory Point of View

These are the DNA units the registry stores.

### Layer 2. Primitive compounds

These are combinations that reliably work together.

Examples:

- `Connection Before Content + Tribal Reference`
- `What Is / What Could Be + Throughline`
- `Trojan Horse Narrative + Empathy Inversion`
- `Backstory Architecture + Auditory POV`

These compounds are much closer to lived output chemistry than isolated primitives.

### Layer 3. Expression recipes

These are surface-specific plans.

Examples:

- Discovery-mode CCF hook recipe
- Processing-mode Telegram reflection recipe
- CVE carousel focal-path recipe
- CMF tension-release sonic recipe

This is where JIT orchestration should operate.

### Layer 4. Validators and outcome loops

These determine:

- whether the recipe was expressed well
- whether it fit the situation
- whether it actually worked

This is where primitives stop being theory and become infrastructure.

---

## The most important new object: Primitive Expression Plan

This should become a first-class artifact in CCP.

Suggested schema:

```yaml
plan_id: string
surface: enum
goal_profile:
  connection: 0-1
  surprise: 0-1
  feeling: 0-1
  clarity: 0-1
  memorability: 0-1
  action_readiness: 0-1

context_snapshot:
  mood_state: string
  archetype: string
  audience_maturity: string
  trigger_type: string
  platform: string
  coach_voice: string

selected_primitives:
  - primitive_id: string
    role: hook|bridge|turn|peak|close|perceptual_support
    intensity: low|medium|high
    confidence: 0-1
    rationale: string
    constraints: [string]

interaction_notes:
  synergies: [string]
  conflicts_avoided: [string]

validator_targets:
  resonance_floor: 0-1
  surprise_floor: 0-1
  clarity_floor: 0-1
  ethics_floor: 0-1
```

This object is the bridge between ontology and output.

Without it, primitive integration will remain fuzzy.

---

## Registry schema upgrade for v2

The registry should now explicitly store both strands.

Suggested direction:

```yaml
primitive_id: string
name: string
family: enum
stability_class: dna_stable|regulatory_stable|rna_volatile

structural_strand:
  summary: string
  cues: [string]
  mechanism: string
  sequence_roles: [string]
  activation_conditions: [string]
  suppression_conditions: [string]

effect_strand:
  connection_lift: 0-1
  surprise_lift: 0-1
  feeling_lift: 0-1
  memory_lift: 0-1
  action_lift: 0-1
  misuse_risk: 0-1

translation_rules:
  dna_language: string
  rna_templates: [string]

ethics:
  red_lines: [string]
  overexpression_symptoms: [string]
  vulnerable_context_warnings: [string]
```

This is better than a single flat descriptive schema because it preserves the double-strand model and the translation model at the data level.

---

## What gets stored in weights vs prompts vs tools

This distinction matters a lot.

### Keep in registry / explicit data

- primitive definitions
- family membership
- risks
- compatibility rules
- evaluator mappings
- approved examples

### Keep in JIT reasoning

- which primitives should fire now
- strength and ordering
- contextual suppression
- medium translation

### Keep in validators

- did the primitive appear
- did it fit
- did it overfire
- did it create the intended effect

### Train into weights later

- audience knowledge modeling habits
- archetype-specific primitive mixes
- coach-specific expression tendencies
- anti-slop pattern discrimination
- surface-specific expression fluency

### Use steering for

- contrast detection
- tension detection
- contradiction salience
- perceptual emphasis

This lets us avoid forcing every primitive into one technical mechanism.

---

## Official integration principle

Primitive integration should happen in this order:

### 1. Registry
Define the ontology correctly.

### 2. Validators
Make primitive expression measurable.

### 3. Receipts
Capture outputs with primitive labels and scores.

### 4. JIT expression planning
Select and compose primitives at runtime.

### 5. Training
Use stable receipt data for SFT, DPO, reward models, and steering.

This order is non-negotiable.

If we skip measurement and go straight to training, we will fossilize weak ontology into the model.

---

## The CCP rule for context hygiene

One of the strongest reasons to adopt this biology architecture is context hygiene.

The system should not dump primitive philosophy into every prompt.
Instead:

- store primitives in the registry
- activate only relevant ones
- transcribe them into compact expression plans
- execute only what is needed

This is how we preserve precision without noise.

The architecture should therefore optimize for:

- minimum active primitive set
- maximum contextual relevance
- explicit suppression of unnecessary primitives
- short expression instructions

That is the biological advantage:

**most genes stay silent most of the time.**

That is exactly how CCP should behave.

---

## The ethics layer

Primitive power without regulation becomes manipulation.

So every primitive must include:

- misuse modes
- overexpression symptoms
- audience vulnerability risks
- ethical red lines

Examples:

- Tribal Reference can create belonging or exclusion
- Irony Inversion can reveal truth or create smugness
- What-Is / What-Could-Be can inspire or overinflate aspiration
- Trojan Horse Narrative can teach elegantly or bypass consent in manipulative ways

Therefore ethics is not an add-on validator.
It is part of the primitive registry itself.

---

## Immediate implications for CCP subsystems

### CCF

Use primitives mainly for:

- hooks
- tension logic
- surprise
- belonging
- coherence
- closure

### CBCS / Telegram / Roleplay

Use primitives mainly for:

- conversation layer matching
- recognition
- reflection
- challenge timing
- emotional containment

### CMF / CVE

Use primitives mainly for:

- perceptual pathing
- visual emphasis
- sonic emphasis
- emotional pacing
- memory peaks

### V2WS

Use primitives mainly for:

- throughline
- mentor/hero dynamics
- movement from current state to transformed state
- designed peak moments
- memorable endings

---

## Final law

The law of this architecture is:

**primitives do not exist to add more language to the system.**

They exist to improve:

- selection
- expression
- discernment
- validation
- training

The moment primitive integration adds verbosity without improving taste, timing, and felt impact, it is failing.

So the permanent standard is:

**Does this primitive architecture help CCP create stronger connection, cleaner surprise, deeper feeling, better memory, and more precise action at the right time with less noise?**

If yes, keep it.
If not, cut it.

---

## Final architecture statement

CCP should treat primitives as a **biological intelligence layer**:

- encoded in a stable registry
- activated by context
- transcribed into compact plans
- executed by generators
- judged by validators
- selected by outcomes
- refined through training

That is the architecture most likely to make primitives useful across the entire engine without turning them into prompt clutter or agentic chaos.

In v2, the strongest summary is:

**the Primitive Registry is CCP’s protected nucleus, primitives are double-stranded encoded units, runtime context acts epigenetically, DSPy transcribes local expression plans, generators synthesize outputs at the edge, and validators plus outcomes decide which expressions deserve to survive.**
