---
type: architecture-source-of-truth
author: Codex synthesis for CCP
date: 2026-05-02
status: Source of Truth
dependencies:
  - D:\Work\The Conscious Coaching Factory\docs\prd\prd.md
  - D:\Work\The Conscious Coaching Factory\lab\CCP update\CRAL_Documentation_V1.docx.md
  - D:\Work\The Conscious Coaching Factory\lab\LoRa Activation Steering and Embegging papers\Text fine-tuning\1_Primary_CCV_Protocol\Matrix of Edging.md
  - D:\Work\The Conscious Coaching Factory\lab\CCP APRIL Updates\Primitive_Conscious_Orchestration_Architecture.md
  - D:\Work\The Conscious Coaching Factory\lab\Public Speeaking Coaching\Primitive Biology Architecture.md
  - D:\Work\The Conscious Coaching Factory\skills\ccf\orchestration\ccf-batch\SKILL.md
  - D:\Work\The Conscious Coaching Factory\docs\prompts_archetypes (1).md
  - D:\Work\The Conscious Coaching Factory\src\ccp\commands\ccf_analyze.py
---

# Perceptual Primitives Architecture

## 1. Purpose

This document replaces the earlier "attention layer before generation" framing with a more accurate CCP framing.

The old version was useful because it identified a real missing layer between research and writing. But it was still too close to generic content-theory language. It treated perceptual primitives mainly as angle detectors for script generation. That is not enough for CCP.

The correct role of this layer is upstream and two-stage:

1. before Trigger-First elicitation, it helps research locate the strongest broad primary signal that can make the coach react authentically
2. after the coach responds, it helps transform authenticated material into primitive candidates, coalition signatures, and executable CCF routing

So this architecture is not just "what the model notices before writing."

It is:

`research perception -> reaction design -> authentic extraction -> primitive composition -> coalition routing`

The goal is not to make the system cleverer in prose. The goal is to make it better at surfacing real charge without flattening it into centroid content.

---

## 2. Core Correction

The biggest correction is this:

**primitives are not edges.**

Primitives are closer to:

- encoded meaning spaces
- perception labs
- transformation operators
- candidate generators

Edges are not the atomic basis. Edges are emergent products that arise when primitive outputs interact with real CRAL evidence and later with authenticated coach response.

This matters because if we treat edges as primitives too early:

- we confuse products with basis units
- we build false coalitions out of already-combined effects
- we lose the ability to measure whether a coalition is truly strong or merely rhetorically plausible

The correct hierarchy is:

`CRAL evidence -> primitive spaces -> candidate survival -> coalition signature -> edge product -> CCF routing`

In this hierarchy:

- primitives are basis-like
- coalitions are field geometries
- edges are emergent products
- archetypes/frameworks/angles are downstream execution choices

---

## 3. The Two Edge Phases

The system should explicitly distinguish two different "edge" moments.

### Phase A: Pre-Trigger Broad Signal

This happens before the coach inbox.

Its purpose is not to find the final content edge. It is to find the strongest broad signal that can create authentic reaction.

This first signal must be:

- charged enough to provoke response
- timely enough to matter now
- broad enough not to over-steer the coach
- clean enough to preserve authentic input

It should function like a pressure cue, not like a conclusion.

The wrong move here is narrowness. If the pre-trigger signal is too specific, the coach ends up performing to the prompt instead of reacting from truth.

### Phase B: Post-Trigger Coalition Formation

This happens after the coach has responded and the material has passed authenticity or LIWC-like gating.

Its purpose is to:

- detect stronger primitive activations inside the coach's authentic language
- generate candidate transforms from those activations
- form coalitions from the surviving candidates
- route the coalition into the real CCF execution lattice

This second phase is where narrower structure is appropriate.

So the architecture should obey this law:

**the first edge should be broad enough to elicit truth; the second edge should be sharp enough to organize execution.**

---

## 4. The Actual Pipeline Position

This layer sits in two places relative to the current system.

### Relative to CRAL

CRAL already produces moment-specific research intelligence. That remains sovereign.

This architecture does not replace CRAL. It reads CRAL output as the evidence field from which latent potentials can be detected.

That means upstream perception should begin during or immediately after research, before the coach is provoked.

### Relative to Trigger-First

The current trigger-first batch spine in `ccf-batch` is already much closer to the desired system than the older `ccf_analyze.py` route.

The correct insertion points are:

- before `A4 Provocation Generation`: broad primary signal extraction from research and activation material
- around `A7 Blueprint Distillation`: post-response primitive and coalition formation

This means coalition logic should not replace Trigger-First.

It should improve:

- what we bring to the coach inbox
- what we do with the coach's response afterward

---

## 5. Primitive Spaces

A primitive space is a stable transformation lab that examines evidence for a specific kind of meaning potential.

Examples already grounded in existing audits include:

- `Irony Inversion`
- `Analogy Bridge`
- `What-Is / What-Could-Be`
- `Vulnerable Specificity`
- `Tribal Reference`
- `One-Sentence Lens`
- `Misplaced Focus`
- `Character Mask`
- `Decision-Change Arc`
- `Stakes as Personal Why`

These should not be treated as final scripts or content formats. They are better understood as stable operators that can probe evidence and propose candidates.

Each primitive space should be able to do four things:

1. detect native evidence already present
2. detect latent evidence that is almost present
3. propose JIT-completable transforms that remain faithful to the evidence field
4. reject unsupported invention

This gives us a much better distinction than simple found/not-found logic.

The right categories are:

- `native`
- `latent`
- `JIT-completable`
- `unsupported`

Only the last category should be killed immediately.

---

## 6. Candidate Generation and Survival

Each primitive space should generate multiple candidates from the same CRAL field or authenticated coach response.

For example:

- an `Irony Inversion` lab may propose 3 to 7 possible inversions
- a `What-Is / What-Could-Be` lab may propose 3 to 7 contrast trajectories
- a `Tribal Reference` lab may propose 3 to 7 possible resonance anchors

The system should not commit at primitive detection time. It should commit after candidate survival scoring.

Each candidate should be scored on:

- evidence fidelity
- emotional charge
- recognizability
- tribal density
- freshness
- completion cost
- speakability
- execution potential

This is where the "97% almost there" intuition becomes operational.

A candidate should survive not only when it is explicit, but also when it is strongly implied and cheaply completable without drifting away from the truth of the field.

This is essential because many strong pieces are not fully present in the research as literal sentences. They are present as high-potential semantic gradients.

---

## 7. Coalition Signature

The surviving candidates then form a coalition signature.

This is one of the most important measurable layers in the future architecture.

A coalition signature is not just a list of active primitives. It is the weighted geometry of the active candidate set.

It should capture:

- which primitive candidates survived
- their relative strengths
- their ratios across families
- their complementarity or overlap
- their likely execution force

This is stronger than only benchmarking:

- which archetype performs best
- which persuasive angle performs best
- which single edge performs best

Because coalition signatures let CCP learn:

- which mixtures produce the sharpest blueprints
- which mixtures work best for which coaches
- which mixtures route cleanly into which content architectures
- which research patterns reliably lead to stronger downstream outputs

In practical terms, the coalition signature should eventually be a benchmarkable object, not just a poetic description.

---

## 8. Edge Products

Once a coalition signature is formed, the actual edge product emerges.

This is the felt resulting tension or cutting force the audience will later encounter.

Examples:

- `Vulnerable Specificity + One-Sentence Lens + Tribal Reference`
  may yield a highly potent recognition edge

- `Irony Inversion + Character Mask + Misplaced Focus`
  may yield a strong humor or exposure edge

- `What-Is / What-Could-Be + Stakes as Personal Why + Decision-Change Arc`
  may yield a transformation-pressure edge

The key point is that the edge product is not the same as the primitive list.

It is what the primitive coalition becomes when composed.

That is why edges should be modeled as products, not as the first ontology layer.

---

## 9. Relation to the Official CCF Execution Lattice

Coalitions must not route into vague generic labels.

They must route into the actual CCF assembly system that already exists:

- Viral Frameworks
- Persuasive Angles
- Content Archetypes
- Archetype Families
- subcategories
- mood-state behavior
- CRAL moment usage

This is critical.

If coalition design stays abstract, it can become elegant but operationally useless. The coalition layer only matters if it improves the actual selection of:

- `trigger_expression_angle`
- content archetype family
- framework choice
- persuasive angle
- final structural execution path

So the route is not:

`coalition -> generic archetype`

It is:

`coalition -> official CCF routing stack`

This keeps the system compatible with the actual content engine rather than a theoretical parallel engine.

---

## 10. Coalition Fatality

Coalition fatality is the failure mode where a coalition looks promising at detection time but collapses when forced into real execution.

It manifests as:

- high local charge but poor route into the official CCF structures
- a hook with no valid body
- a sharp tension with weak proof support
- primitive redundancy that creates no new force
- primitive cancellation where one surviving candidate weakens another
- over-completion of a latent candidate beyond the evidence field
- flattening once a coalition is turned into generic prose

Coalition fatality is especially likely when:

- products are mistaken for primitives
- the first signal is too narrow
- evidence fidelity is ignored
- archetype/framework compatibility is assumed rather than tested

This is why coalition benchmarking matters.

A coalition should not only be judged by how interesting it sounds in theory, but by whether it survives downstream translation into actual CCF assets.

---

## 11. Mathematical Framing

This architecture benefits from mathematical representation, but it should start with geometry, not with decorative math.

The most relevant concepts are:

- vectors
- projections
- cosine / angle
- gradients
- interaction terms
- sparse activation
- graph support

### Why vectors matter

Primitive spaces can be treated as meaning directions or operators. Evidence fields can be treated as structured representations. Candidate activations can be projected, compared, and clustered.

### Why gradients matter

Gradients are the right mental model for latent potential.

Instead of asking:

- is this edge fully present?

we ask:

- which local transformation yields the steepest valid increase in charge while staying faithful to the evidence?

This is exactly the right geometry for JIT-completable candidates.

### Why interaction terms matter

Coalitions are not simple sums.

Some primitive combinations amplify each other.
Some cancel each other.
Some produce a qualitatively different result.

So coalition value should eventually include interaction terms, not just additive weights.

### Why graphs still matter

Vectors should not replace graph structure.

CCP already benefits from graph-like context premise logic because relationships are causal and associative, not merely similar.

The right architecture is:

`structured evidence + graph relations + vectorized retrieval/benchmarking`

not pure embeddings.

---

## 12. Value of Vectorization

Yes, there is strong value in vectorizing parts of this system.

The most useful vectorization targets are:

- CRAL findings by moment
- context premise L3 segments
- primitive candidate outputs
- coalition signatures
- historical blueprint signatures
- proven execution exemplars

Vectorization is especially useful for:

- memory
- retrieval
- similarity search
- "almost there" candidate detection
- coalition benchmarking
- route recommendation

But vectorization should not replace:

- named evidence
- trigger maps
- citations
- authenticated coach input
- structured CRAL findings

The best model is hybrid:

- symbolic where causal specificity matters
- graph-based where relational memory matters
- vectorized where retrieval and geometric comparison matter

---

## 13. Recursive Language Models

Recursive language-model behavior is not irrelevant here, but it should not become the center of the architecture.

What matters most is bounded recursion in specific layers:

- candidate generation refinement
- candidate survival review
- coalition repair
- route comparison when multiple executions are plausible

What should be avoided is a vague open recursive content loop that dissolves CCP's determinism.

So the correct use of recursion is local and typed:

- refine candidate transforms
- compare coalition alternatives
- repair fatal coalitions
- improve route selection

The right recursion object is not "write again until it feels good."

It is:

- `generate candidates`
- `score`
- `select`
- `repair if needed`
- `route`

That keeps the system precise.

---

## 14. Comparison With the Existing Idea Process

The current codebase contains two idea-generation patterns.

### Pattern A: Older direct idea generation

`ccf_analyze.py` generates `ideas.json` largely from:

- coach soul
- topic suggestions
- leadership traits
- boredom-ban constraints
- direct model ideation

This is workable, but it is structurally shallow relative to the newer CCP architecture.

### Pattern B: Trigger-first batch orchestration

The `ccf-batch` flow is stronger because it already uses:

- trigger matching
- intelligence radar
- activation-event design
- provocation generation
- coach elicitation
- authentication logic
- emotional-state to archetype mapping
- blueprint distillation

This is the right backbone for coalition integration.

The best insertion points are:

- before provocation generation: broad primary signal extraction
- inside blueprint distillation: primitive candidate and coalition formation

So the answer is:

**do not replace the current trigger-first spine with coalition logic.**

Use coalition logic to upgrade the quality of:

- the prompt that reaches the coach
- the blueprint that comes out of the coach response

---

## 15. Design Laws

The system should obey these laws.

### Law 1. Broad-first law

The first signal must be broad enough to elicit truth and narrow enough to provoke reaction.

### Law 2. Basis-before-product law

Primitives should be modeled before edges. Products should not be mistaken for basis units.

### Law 3. Survival law

Candidates must survive evidence scoring before they influence execution.

### Law 4. Coalition-over-isolate law

The strongest outputs usually come from weighted coalitions, not isolated primitives.

### Law 5. Routing law

Coalitions must route into the official CCF execution lattice, not into generic labels.

### Law 6. Hybrid-memory law

Vectors help, but they do not replace symbolic structure, graph memory, or named evidence.

### Law 7. Anti-centroid law

The system must protect charge from flattening at every handoff.

---

## 16. Recommended First Implementation

The first implementation should stay modest and measurable.

### Step 1

Define a small registry of high-value primitive spaces already grounded in audits.

### Step 2

For pre-trigger research, generate a `PrimarySignalPacket` that captures:

- signal summary
- evidence anchors
- timely pressure
- probable reaction value
- room-for-coach-surprise

### Step 3

For post-trigger analysis, generate a `PrimitiveCandidatePacket` set from authenticated coach material.

### Step 4

Score candidates for survival and form a `CoalitionSignature`.

### Step 5

Benchmark coalition signatures against downstream blueprint quality and execution success.

This gives CCP a real measurable intermediate layer without forcing a full rewrite of the current system.

---

## 17. Final Position

The mature view is this:

Perceptual primitives are not merely attention tricks before writing. They are the stable meaning spaces through which CCP perceives researched reality, elicits cleaner truth from the coach, transforms that truth into stronger coalition signatures, and routes those signatures into the actual CCF execution system.

Or more compactly:

**research finds the field, broad signals make the coach speak, primitive spaces generate candidates, coalitions organize force, edge products emerge from composition, and the official CCF lattice turns that force into content.**
