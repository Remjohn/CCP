---
type: architecture-source-of-truth
author: Codex synthesis for CCP
date: 2026-05-02
status: Source of Truth
dependencies:
  - D:\Work\The Conscious Coaching Factory\lab\CCP APRIL Updates\Perceptual_Primitives_Architecture.md
  - D:\Work\The Conscious Coaching Factory\lab\CCP APRIL Updates\Primitive_Conscious_Orchestration_Architecture.md
  - D:\Work\The Conscious Coaching Factory\lab\Public Speeaking Coaching\Primitive Biology Architecture.md
  - D:\Work\The Conscious Coaching Factory\skills\ccf\orchestration\ccf-batch\SKILL.md
  - D:\Work\The Conscious Coaching Factory\docs\prompts_archetypes (1).md
---

# Primitive Packets and Registry Spec

> Current status:
> this file now acts as a `bridge document` for the older combined architecture.
>
> The registry layer is being separated into:
>
> - [Meaning_Primitive_Registry_Spec.md](</D:/Work/The Conscious Coaching Factory/lab/CCP APRIL Updates/Meaning_Primitive_Registry_Spec.md>)
> - [Experience_Primitive_Registry_Spec.md](</D:/Work/The Conscious Coaching Factory/lab/CCP APRIL Updates/Experience_Primitive_Registry_Spec.md>)
> - [Primitive_Crosswalk_Map.md](</D:/Work/The Conscious Coaching Factory/lab/CCP APRIL Updates/Primitive_Crosswalk_Map.md>)
>
> This file remains useful for the current packet contracts, but it should no longer be treated as the long-term home for both registries.

## 1. Purpose

This document defines the first production-ready specification for the primitive layer discussed in:

- [Perceptual_Primitives_Architecture.md](</D:/Work/The Conscious Coaching Factory/lab/CCP APRIL Updates/Perceptual_Primitives_Architecture.md>)
- [Primitive_Conscious_Orchestration_Architecture.md](</D:/Work/The Conscious Coaching Factory/lab/CCP APRIL Updates/Primitive_Conscious_Orchestration_Architecture.md>)
- [Primitive Biology Architecture.md](</D:/Work/The Conscious Coaching Factory/lab/Public Speeaking Coaching/Primitive Biology Architecture.md>)

It has 3 jobs:

1. define the packets the system should emit at each stage
2. define the base schema for storing primitives in a sovereign registry
3. define a canonical primitive catalog grounded in the audit library already produced inside CCP

This is not yet the final mathematical implementation.
It is the first clean, production-facing contract for:

- broad signal extraction
- primitive candidate generation
- coalition formation
- edge-product emergence
- routing into the official CCF execution lattice

Important boundary:

This document is primarily a spec for `meaning / content / expression primitives`.
It does **not** fully cover the newer `experience / adoption / UX` primitives emerging from the `09_Experience_Engineering` audit shelf.

Those experience primitives belong in the same broad architecture universe, but they should not be flattened blindly into the same registry logic as if they were only content-generation moves.

---

## 2. The Official Sequence

The correct production sequence is:

`CRAL / research field -> PrimarySignalPacket -> provocation / coach inbox -> authenticated coach response -> PrimitiveCandidatePacket[] -> CoalitionSignature -> EdgeProductPacket -> CCFRoutingRecommendation -> blueprint / execution`

This keeps the upstream and downstream layers distinct:

- `pre-trigger` finds the strongest broad signal
- `post-trigger` forms sharper primitive coalitions from truth-rich material

---

## 3. Packet Specifications

## 3.1 PrimarySignalPacket

This is the pre-trigger packet.
It exists to help the system bring something charged but not overly narrow to the coach inbox.

```yaml
packet_type: PrimarySignalPacket
packet_version: 1
signal_id: string
source_refs: [string]
topic_scope: string
timeliness_window: string

signal_summary: string
pressure_cue: string
why_it_matters_now: string
coach_reaction_hypothesis: string

evidence_anchors:
  - source_ref: string
    quote_or_fact: string
    support_type: enum[quote, trend, contradiction, scene, mechanism, tribal_cue]

signal_axes:
  relevance: float
  charge: float
  timeliness: float
  coach_proximity: float
  openness_for_surprise: float
  oversteer_risk: float

permitted_prompt_shapes:
  - enum[question, reflection, tension_prompt, contrast_prompt, observation_prompt]

disallowed_prompt_shapes:
  - enum[over_narrow_theory_dump, thesis_imposition, conclusion_stuffing]

recommended_tone:
  warmth: float
  directness: float
  challenge: float
  mystery: float

selection_notes: string
```

### Governing rule

The first signal should be:

- specific enough to produce reaction
- broad enough to leave room for authentic surprise

### Primary signal score

```text
PrimarySignalScore =
  (0.28 * relevance) +
  (0.24 * charge) +
  (0.18 * timeliness) +
  (0.15 * coach_proximity) +
  (0.15 * openness_for_surprise)
  - (0.20 * oversteer_risk)
```

---

## 3.2 PrimitiveCandidatePacket

This is the post-trigger packet emitted after the coach has responded and the response is authenticated.

```yaml
packet_type: PrimitiveCandidatePacket
packet_version: 1
candidate_id: string
source_material_ref: string
primitive_id: string
primitive_name: string
family: string

source_mode: enum[native, latent, JIT_completable]
candidate_text: string
candidate_summary: string
evidence_trace:
  - source_span: string
    rationale: string

activation_scores:
  evidence_fidelity: float
  emotional_charge: float
  recognizability: float
  tribal_density: float
  freshness: float
  completion_cost: float
  speakability: float
  execution_potential: float

surface_affinity:
  text: float
  voice: float
  visual: float
  sonic: float
  webinar: float
  telegram: float

survival_flags:
  supported: boolean
  emotionally_live: boolean
  safe_to_complete: boolean
  routing_viable: boolean

notes: string
```

### Candidate survival score

```text
CandidateSurvivalScore =
  (0.22 * evidence_fidelity) +
  (0.18 * emotional_charge) +
  (0.14 * recognizability) +
  (0.10 * tribal_density) +
  (0.09 * freshness) +
  (0.09 * speakability) +
  (0.18 * execution_potential)
  - (0.12 * completion_cost)
```

Only candidates above threshold should flow into coalition formation.

---

## 3.3 CoalitionSignature

This is the central measurable object.
It is not only a list of primitives. It is the weighted geometry of the surviving set.

```yaml
packet_type: CoalitionSignature
packet_version: 1
coalition_id: string
source_batch_ref: string
candidate_ids: [string]

dominant_primitives:
  - primitive_id: string
    weight: float

supporting_primitives:
  - primitive_id: string
    weight: float

family_ratios:
  psychological_diagnostics: float
  connection: float
  contrast: float
  performance: float
  persuasion: float
  narrative_structure: float
  story_discovery: float
  explanation_translation: float
  visual_sonic_guidance: float

interaction_notes:
  synergies: [string]
  tensions: [string]
  redundancies: [string]

coalition_scores:
  coherence: float
  charge: float
  novelty: float
  truth_density: float
  routeability: float
  flattening_susceptibility: float

coalition_summary: string
```

### Coalition value score

```text
CoalitionValue =
  (0.22 * coherence) +
  (0.22 * charge) +
  (0.15 * novelty) +
  (0.20 * truth_density) +
  (0.21 * routeability)
  - (0.20 * flattening_susceptibility)
```

### Coalition fatality indicators

A coalition should be marked `fatal` or `unstable` when any of the following happen:

- coherence is low
- charge is high but routeability is low
- truth density is weak relative to novelty
- redundancies dominate the active set
- flattening susceptibility is high

---

## 3.4 EdgeProductPacket

The edge product is the emergent force that the coalition becomes.
It is not the basis itself.

```yaml
packet_type: EdgeProductPacket
packet_version: 1
edge_product_id: string
coalition_id: string

edge_label: string
edge_summary: string
edge_type: enum[recognition, humor_exposure, transformation_pressure, mechanism_reveal, empathy_rotation, authority_sharpening]

emergent_properties:
  pattern_break: float
  belonging: float
  tension: float
  surprise: float
  memorability: float
  challenge_force: float

delivery_requirements:
  needs_story: boolean
  needs_proof: boolean
  needs_tribal_detail: boolean
  needs_visualization: boolean
  needs_voice_intimacy: boolean

anti_flattening_notes: string
```

---

## 3.5 CCFRoutingRecommendation

This packet maps the coalition/edge layer into the official CCF execution lattice.

```yaml
packet_type: CCFRoutingRecommendation
packet_version: 1
routing_id: string
coalition_id: string
edge_product_id: string

trigger_expression_angle: string

recommended_frameworks:
  - framework_name: string
    fit_score: float

recommended_persuasive_angles:
  - angle_name: string
    fit_score: float

recommended_content_archetypes:
  - archetype_name: string
    fit_score: float

recommended_family_distribution:
  storytelling: float
  listicle: float
  case_study: float
  comparison: float
  myth_and_scam: float
  tier_list: float
  core_formats: float

recommended_surface_bias:
  text: float
  voice: float
  visual: float
  sonic: float

disallowed_routes:
  - route_name: string
    reason: string

summary_reasoning: string
```

---

## 3.6 CoalitionBenchmarkRecord

This record is the memory object that allows CCP to learn which coalitions actually survive execution.

```yaml
packet_type: CoalitionBenchmarkRecord
packet_version: 1
benchmark_id: string
coalition_id: string
route_id: string
coach_id: string
context_id: string

execution_result:
  blueprint_quality: float
  script_strength: float
  voice_fidelity: float
  validation_pass_rate: float
  publish_readiness: float

outcome_metrics:
  hook_strength: float
  retention_quality: float
  conversion_signal: float
  audience_recognition_signal: float
  coach_alignment_signal: float

failure_modes:
  - fatality_type: string
    severity: float

operator_notes: string
```

---

## 4. Primitive Registry Base Schema

Every primitive in the registry should inherit from the same base schema.

```yaml
primitive_id: string
canonical_name: string
aliases: [string]
family: enum[
  psychological_diagnostics,
  connection,
  contrast,
  humor_distortion,
  performance_delivery,
  persuasion,
  narrative_structure,
  story_discovery,
  explanation_translation,
  visual_sonic_guidance
]

source_audits: [string]
summary: string
core_move: string
why_it_works: string

phase_fit:
  pre_trigger: float
  post_trigger: float
  generation: float
  revision: float
  delivery: float

surface_fit:
  text: float
  voice: float
  visual: float
  sonic: float
  webinar: float
  telegram: float

goal_bias:
  connection: float
  surprise: float
  tension: float
  clarity: float
  memorability: float
  persuasion: float

trigger_conditions: [string]
suppression_conditions: [string]
misuse_modes: [string]
synergizes_with: [string]
conflicts_with: [string]

notes: string
```

---

## 5. Family Taxonomy

The registry should not stay flat.
The current audit material strongly supports these top-level families.

### 5.1 Connection

Primitives that build trust, belonging, warmth, recognition, and social location.

### 5.2 Contrast

Primitives that create gap, oscillation, inversion, tension, and directional movement.

### 5.3 Humor Distortion

Primitives that alter scale, frame, expectation, embodiment, or focus to produce high-attention pattern breaks.

### 5.4 Performance and Delivery

Primitives that determine how the message is felt in live language, voice, timing, vulnerability, and perceived spontaneity.

### 5.5 Persuasion

Primitives that shape argument, trust sequence, motivational movement, and audience guidance.

### 5.6 Narrative Structure

Primitives that give content movement, turn logic, scene logic, beats, stakes, and transformation.

### 5.7 Story Discovery

Primitives that help find truth-rich material before content assembly begins.

### 5.8 Explanation and Translation

Primitives that compress, translate, reveal, or stage insight so the audience can actually metabolize it.

### 5.9 Visual and Sonic Guidance

Primitives that govern what the eye, ear, or nervous system prioritizes.

### 5.10 Psychological Diagnostics and Internal-State Engineering

Primitives that map the client's internal operating scripts, conflict patterns, ego states, and biological stress architecture.

### 5.11 Experience Engineering Is a Parallel Registry, Not a Flat Family Add-On

The `09_Experience_Engineering` audits produced a different primitive class.

These primitives often do **not** govern:

- what the coach says
- what edge is extracted
- what story structure is formed

They govern:

- why the coach enters the experience
- whether the app feels credible
- whether the action path feels easy
- whether the score feels meaningful
- whether the user shares
- whether the user comes back
- whether the challenge converts

Examples:

- `Context-Aware System Triggers`
- `Zero-Thought Onboarding`
- `RIM Feedback`
- `Signature Moment`
- `Social Treasures + Group Quests`
- `Behavioral Forgiveness`
- `Cumulative Investment`

These should therefore be modeled as a **parallel registry domain** rather than squeezed into one of the current meaning-oriented families.

The recommended model is:

- `Meaning Primitive Registry`
  This document. It governs research, coach response, content assembly, edge products, and routing.

- `Experience Primitive Registry`
  A sibling registry for Mini App flow, Telegram timing, trust architecture, scoring rituals, social propagation, replay logic, and adoption acceleration.

- `Voice Experience Subdomain`
  A later specialization for voice-note, score reveal, sonic trust, and prosodic coaching touchpoints when experience primitives need audio-specific contracts.

The reason for the split is architectural hygiene.

If we mix these domains too early, we lose the ability to distinguish:

- content strength from experience strength
- coach truth extraction from user adoption
- rhetorical quality from onboarding quality
- edge magnitude from retention quality

### Recommended Experience Primitive Base Schema

```yaml
experience_primitive_id: string
canonical_name: string
aliases: [string]

experience_family: enum[
  trigger_timing,
  friction_ability,
  trust_branding,
  feedback_scoring,
  progression_replay,
  social_referral,
  safe_failure_recovery,
  personalization_identity
]

mechanic_role: enum[
  loop,
  state,
  moment,
  accent,
  safeguard
]

moment_role: enum[
  notification,
  topic_brief,
  entry,
  record,
  score_reveal,
  share_prompt,
  comeback,
  challenge_transition,
  continuity,
  upgrade
]

source_audits: [string]
summary: string
core_move: string
why_it_works: string

experience_stage_fit:
  entry: float
  activation: float
  recording: float
  scoring: float
  social_spread: float
  recovery: float
  retention: float
  conversion: float

surface_fit:
  telegram_message: float
  mini_app: float
  score_card: float
  share_asset: float
  voice_prompt: float
  push_nudge: float

user_state_effects:
  confidence: float
  urgency: float
  clarity: float
  safety: float
  status: float
  belonging: float
  curiosity: float
  replay_desire: float

activation_conditions: [string]
suppression_conditions: [string]
misuse_modes: [string]
synergizes_with: [string]
conflicts_with: [string]

experience_metrics:
  entry_rate: float
  react_rate: float
  completion_rate: float
  share_rate: float
  comeback_rate: float
  day7_retention: float
  upgrade_signal: float

notes: string
```

### Recommended Experience Packets

Later, the experience registry should likely emit sibling packets such as:

- `ExperienceTriggerPacket`
- `ExperienceActivationPlan`
- `ExperienceMomentPacket`
- `ExperienceOutcomeRecord`

Those should sit beside, not inside, `PrimarySignalPacket` and `PrimitiveCandidatePacket`.

---

## 6. Canonical Primitive Registry Extracted From the Audits

The list below is the first large pass of canonical primitives drawn from the audit library discussed in the current architecture work.

Where two books clearly describe the same mechanism, the registry should keep:

- one canonical primitive
- one or more source aliases

The catalog below keeps source traceability while still aiming for canonical clarity.

Important reading rule:

- high MCDA primitives usually deserve earlier implementation priority
- lower MCDA primitives should not be discarded automatically

Some lower-scoring primitives still matter because they function as:

- `safeguards`
- `accent moves`
- `moment-shapers`
- `recovery primitives`
- `premium finishing primitives`

So the registry should be scanned not only by score, but also by implementation role.

## 6.1 Humor Distortion Primitives

### PRM-HUM-009 Reference Funny Filter
Source: `Audit_How_to_Write_Funny_Characters.md`
MCDA: `195/200`
Core move: sweeten the character with shared references that make the audience recognize themselves.

### PRM-HUM-037 Hyper-Specificity Anchoring
Source: `Audit_The_Serious_Guide_to_Joke_Writing_CCP.md`
MCDA: `195/200`
Core move: move away from generic nouns into narrow, lived, detailed material.

### PRM-HUM-031 The Mix
Source: `Audit_The_NEW_Comedy_Bible_Documentation.md`
MCDA: `191/200`
Core move: force two distant domains into one surprising analogy system.

### PRM-HUM-036 Directed Emotional Stance
Source: `Audit_The_Serious_Guide_to_Joke_Writing_CCP.md`
MCDA: `190/200`
Core move: choose the emotional attitude first so the material has charge.

### PRM-HUM-025 Analogy Bridge
Source: `Audit_The_Elements_of_Humor_CCP.md`
MCDA: `188/200`
Core move: translate a heavy or abstract truth into a vivid familiar comparison.

### PRM-HUM-010 High-Contrast Conflict
Source: `Audit_How_to_Write_Funny_Characters.md`
MCDA: `185/200`
Core move: cast a character into a setting or opposition where their nature clashes hard.

### PRM-HUM-030 Setup-Premise-Payoff Architecture
Source: `Audit_The_NEW_Comedy_Bible_Documentation.md`
MCDA: `185/200`
Core move: organize the joke or idea around attitude-bearing premise logic before the release.

### PRM-HUM-035 Associative Web
Source: `Audit_The_Serious_Guide_to_Joke_Writing_CCP.md`
MCDA: `185/200`
Core move: spread laterally through idea associations until something fresh appears.

### PRM-HUM-032 Rule of Three
Sources: `Audit_The_NEW_Comedy_Bible_Documentation.md`, `Audit_Talk_Like_TED_Carmine_Gallo.md`
MCDA: `182/200` from `Audit_The_NEW_Comedy_Bible_Documentation.md`; `184/200` from `AUDIT_Talk_Like_TED_Carmine_Gallo.md`
Core move: establish pattern, establish pattern, break pattern.

### PRM-HUM-002 Irreducible Truth / Subtext Payload
Sources: `Audit_How_to_Write_Funny_CCP.md`, `Audit_How_to_Write_Funny_Characters.md`
MCDA: `182/200` from `Audit_How_to_Write_Funny_CCP.md`; `175/200` from `Audit_How_to_Write_Funny_Characters.md`
Core move: use humor as delivery for a deeper bitter truth rather than as empty decoration.

### PRM-HUM-014 Joyous Communication
Source: `Audit_Mastering_Stand-Up_CCP.md`
MCDA: `180/200`
Core move: let the message feel like delighted human broadcast rather than duty.

### PRM-HUM-001 Dual-Processor Cognitive Engine
Source: `Audit_How_to_Write_Funny_CCP.md`
MCDA: `178/200`
Core move: split generation from censorship by separating clown-state production from editor-state refinement.

### PRM-HUM-029 Act-Out
Source: `Audit_The_NEW_Comedy_Bible_Documentation.md`
MCDA: `178/200`
Core move: shift from description into embodied live scene.

### PRM-HUM-016 Setup-Punchline Temporal Architecture
Source: `Audit_Mastering_Stand-Up_CCP.md`
MCDA: `176/200`
Core move: engineer time-based release through setup, delay, and collision.

### PRM-HUM-017 Attitude-Emotion Binding
Source: `Audit_Mastering_Stand-Up_CCP.md`
MCDA: `176/200`
Core move: attach a clear emotional attitude to the line so the audience feels intent, not just meaning.

### PRM-HUM-040 Radical Observational Truth
Source: `Audit_The_Serious_Guide_to_Joke_Writing_CCP.md`
MCDA: `175/200`
Core move: start from the deeply true observation before trying to embellish it.

### PRM-HUM-018 Working Backward Methodology
Source: `Audit_Mastering_Stand-Up_CCP.md`
MCDA: `172/200`
Core move: begin with what the audience must feel or receive, then reverse-engineer the path.

### PRM-HUM-021 Irony Inversion
Sources: `Audit_The_Elements_of_Humor_CCP.md`, `Audit_The_Serious_Guide_to_Joke_Writing_CCP.md`
MCDA: `172/200` from `Audit_The_Elements_of_Humor_CCP.md`; `160/200` from `Audit_The_Serious_Guide_to_Joke_Writing_CCP.md`
Core move: expose the gap between what should happen and what actually happens.

### PRM-HUM-003 Filter Constraints
Source: `Audit_How_to_Write_Funny_CCP.md`
MCDA: `171/200`
Core move: distort material through constrained funny filters rather than vague comedic intention.

### PRM-HUM-005 Absolute Verisimilitude
Source: `Audit_How_to_Write_Funny_CCP.md`
MCDA: `171/200`
Core move: keep the world micro-coherent so absurdity lands as believable rather than sloppy.

### PRM-HUM-007 Production Over-Saturation
Source: `Audit_How_to_Write_Funny_CCP.md`
MCDA: `170/200`
Core move: generate enough variants that quality emerges through selection rather than first-pass hope.

### PRM-HUM-034 Comedy Buddy
Source: `Audit_The_NEW_Comedy_Bible_Documentation.md`
MCDA: `168/200`
Core move: use dialectical punch-up through a second intelligence instead of solo generation.

### PRM-HUM-015 Persona Sculpting Protocol
Source: `Audit_Mastering_Stand-Up_CCP.md`
MCDA: `165/200`
Core move: let identity be shaped against audience response rather than declared in abstraction.

### PRM-HUM-026 Misplaced Focus
Source: `Audit_The_Elements_of_Humor_CCP.md`
MCDA: `165/200`
Core move: obsess over the wrong detail so the audience auto-corrects and laughs at the distortion.

### PRM-HUM-028 Authentic Topic Extraction
Source: `Audit_The_NEW_Comedy_Bible_Documentation.md`
MCDA: `163/200`
Core move: mine pain, weirdness, and fear as the real entry point for humor.

### PRM-HUM-019 Struggle Principle
Source: `Audit_Mastering_Stand-Up_CCP.md`
MCDA: `161/200`
Core move: make struggle visible so likability rises through vulnerability.

### PRM-HUM-011 Archetype Shorthand
Source: `Audit_How_to_Write_Funny_Characters.md`
MCDA: `160/200`
Core move: use a culturally familiar archetype to reduce explanation cost and accelerate comprehension.

### PRM-HUM-023 Tribal Reference
Source: `Audit_The_Elements_of_Humor_CCP.md`
MCDA: `160/200`
Core move: use in-group references that instantly create belonging and recognition.

### PRM-HUM-038 Expectation Reversal
Source: `Audit_The_Serious_Guide_to_Joke_Writing_CCP.md`
MCDA: `160/200`
Core move: let the expected frame harden, then pivot it.

### PRM-HUM-020 Thought Moment Illusion
Source: `Audit_Mastering_Stand-Up_CCP.md`
MCDA: `158/200`
Core move: inject human-seeming spontaneity, asymmetry, and live-thought texture.

### PRM-HUM-033 Dialogue Joke
Source: `Audit_The_NEW_Comedy_Bible_Documentation.md`
MCDA: `158/200`
Core move: reconstruct the conversation as it should have happened so the rebuttal lands cleanly.

### PRM-HUM-006 Temporal Resolution Delay
Source: `Audit_How_to_Write_Funny_CCP.md`
MCDA: `156/200`
Core move: hold the funny or revealing part until the latest viable position.

### PRM-HUM-024 Metahumor and Frame Breaking
Source: `Audit_The_Elements_of_Humor_CCP.md`
MCDA: `154/200`
Core move: comment on the frame itself to create a second-level release.

### PRM-HUM-004 Contrastive Extreme Polarization
Source: `Audit_How_to_Write_Funny_CCP.md`
MCDA: `150/200`
Core move: heighten semantic distance to sharpen the anomaly and force attention.

### PRM-HUM-008 Character Funny Filter
Source: `Audit_How_to_Write_Funny_Characters.md`
MCDA: `145/200`
Core move: create laughter by making the character act predictably according to a clear trait rule.

### PRM-HUM-022 Character Mask
Source: `Audit_The_Elements_of_Humor_CCP.md`
MCDA: `145/200`
Core move: borrow a persona or role to create safer distance for sharper truths.

### PRM-HUM-039 What-If Sandbox
Source: `Audit_The_Serious_Guide_to_Joke_Writing_CCP.md`
MCDA: `145/200`
Core move: explore absurd extrapolations safely to reveal overlooked truths.

### PRM-HUM-027 Hyperbolic Scaling
Source: `Audit_The_Elements_of_Humor_CCP.md`
MCDA: `138/200`
Core move: stretch scale beyond normal bounds to intensify a truth.

### PRM-HUM-012 Two-Dimensional Representation Strategy
Source: `Audit_How_to_Write_Funny_Characters.md`
MCDA: `135/200`
Core move: compress a comic persona into a narrow representational function instead of full realism.

### PRM-HUM-013 Intuiting Method
Source: `Audit_How_to_Write_Funny_Characters.md`
MCDA: `110/200`
Core move: observe real humans and translate their strange live traits into material.

## 6.2 Persuasion and Public-Speaking Primitives

### PRM-PRS-028 Throughline
Source: `AUDIT_TED_Talks_Chris_Anderson.md`
MCDA: `196/200`
Core move: carry one coherent line through the whole experience.

### PRM-PRS-001 Strong Title as Idea Architecture
Source: `AUDIT_Confessions_of_a_Public_Speaker_Scott_Berkun.md`
MCDA: `194/200`
Core move: compress the whole idea into a title-level center of gravity before building.

### PRM-PRS-015 What-Is / What-Could-Be Contrast Engine
Sources: `AUDIT_Resonate_Nancy_Duarte.md`, `AUDIT DataStory Illuminate Nancy Duarte.md`
MCDA: `194/200` from `AUDIT_Resonate_Nancy_Duarte.md`; `189/200` from `AUDIT DataStory Illuminate Nancy Duarte.md`
Core move: alternate present reality and possible reality so the gap becomes emotionally active.

### PRM-PRS-022 65/25/10 Pathos Allocation
Source: `AUDIT_Talk_Like_TED_Carmine_Gallo.md`
MCDA: `194/200`
Core move: calibrate emotional load rather than treating passion as an accident.

### PRM-PRS-017 Big Idea Formulation Protocol
Source: `AUDIT_Resonate_Nancy_Duarte.md`
MCDA: `192/200`
Core move: reduce the whole communication to one transferable idea worthy of being remembered.

### PRM-PRS-002 Tension-and-Release Narrative Engine
Source: `AUDIT_Confessions_of_a_Public_Speaker_Scott_Berkun.md`
MCDA: `191/200`
Core move: hold attention by alternating pressure and relief.

### PRM-PRS-008 Warmth-Before-Competence Sequencing
Source: `AUDIT_HBRs_10_Must_Reads_on_Public_Speaking_Harvard_Business_Review.md`
MCDA: `190/200`
Core move: establish human safety before making status claims.

### PRM-PRS-009 Inciting Incident
Source: `AUDIT_HBRs_10_Must_Reads_on_Public_Speaking_Harvard_Business_Review.md`
MCDA: `190/200`
Core move: begin with the event that makes the rest of the communication necessary.

### PRM-PRS-030 Connection Before Content
Source: `AUDIT_TED_Talks_Chris_Anderson.md`
MCDA: `190/200`
Core move: win permission and trust before teaching.

### PRM-PRS-012 Motivating Language Theory Triad
Source: `AUDIT_HBRs_10_Must_Reads_on_Public_Speaking_Harvard_Business_Review.md`
MCDA: `188/200`
Core move: use direction, empathy, and meaning as three distinct motivation channels.

### PRM-PRS-016 Audience-as-Hero Inversion
Source: `AUDIT_Resonate_Nancy_Duarte.md`
MCDA: `188/200`
Core move: let the audience carry the transformational center while the presenter becomes guide.

### PRM-PRS-024 18-Minute Cognitive Load Constraint
Source: `AUDIT_Talk_Like_TED_Carmine_Gallo.md`
MCDA: `188/200`
Core move: respect hard limits of attention and use soft breaks to recover capacity.

### PRM-PRS-029 Idea-Building as Gift Architecture
Source: `AUDIT_TED_Talks_Chris_Anderson.md`
MCDA: `188/200`
Core move: reconstruct the idea inside the listener's mind as an act of generosity.

### PRM-PRS-003 Audience-First Preparation Protocol
Source: `AUDIT_Confessions_of_a_Public_Speaker_Scott_Berkun.md`
MCDA: `186/200`
Core move: design from objection, audience need, and biological reception first.

### PRM-PRS-011 Conger Four-Step Persuasion Architecture
Source: `AUDIT_HBRs_10_Must_Reads_on_Public_Speaking_Harvard_Business_Review.md`
MCDA: `186/200`
Core move: sequence credibility, shared ground, vivid evidence, and emotional appeal deliberately.

### PRM-PRS-020 Audience Journey Map
Source: `AUDIT_Resonate_Nancy_Duarte.md`
MCDA: `186/200`
Core move: define the movement from current state to desired state before scripting.

### PRM-PRS-023 Emotionally Competent Stimulus
Source: `AUDIT_Talk_Like_TED_Carmine_Gallo.md`
MCDA: `186/200`
Core move: deliberately plant one emotionally vivid moment that brands the message into memory.

### PRM-PRS-034 Curiosity Ignition
Source: `AUDIT_TED_Talks_Chris_Anderson.md`
MCDA: `184/200`
Core move: open the audience's prediction loop before trying to close it.

### PRM-PRS-018 S.T.A.R. Moment Architecture
Source: `AUDIT_Resonate_Nancy_Duarte.md`
MCDA: `182/200`
Core move: design a sharp memorable peak that reorganizes attention and memory.

### PRM-PRS-026 Multisensory Delivery Architecture
Source: `AUDIT_Talk_Like_TED_Carmine_Gallo.md`
MCDA: `182/200`
Core move: stack visual, auditory, and felt signals for stronger retention.

### PRM-PRS-031 Explanation Engine
Source: `AUDIT_TED_Talks_Chris_Anderson.md`
MCDA: `182/200`
Core move: make complex content traversable without insulting intelligence.

### PRM-PRS-032 Uncanny Valley Warning
Source: `AUDIT_TED_Talks_Chris_Anderson.md`
MCDA: `182/200`
Core move: avoid over-prepared artificiality that makes delivery feel inhuman.

### PRM-PRS-005 Logos-Ethos-Pathos Persuasion Triad
Source: `AUDIT_Confessions_of_a_Public_Speaker_Scott_Berkun.md`
MCDA: `181/200`
Core move: balance logic, credibility, and emotion instead of over-relying on one.

### PRM-PRS-004 10-Minute Attention Architecture
Source: `AUDIT_Confessions_of_a_Public_Speaker_Scott_Berkun.md`
MCDA: `180/200`
Core move: structure attention in reset-sized blocks so drift does not accumulate.

### PRM-PRS-010 Four Intents of Authentic Delivery
Source: `AUDIT_HBRs_10_Must_Reads_on_Public_Speaking_Harvard_Business_Review.md`
MCDA: `180/200`
Core move: define delivery intent rather than merely content correctness.

### PRM-PRS-019 Three-Channel Contrast System
Source: `AUDIT_Resonate_Nancy_Duarte.md`
MCDA: `180/200`
Core move: build contrast at content, emotional, and delivery layers simultaneously.

### PRM-PRS-025 Passion-as-Contagion Engine
Source: `AUDIT_Talk_Like_TED_Carmine_Gallo.md`
MCDA: `180/200`
Core move: let perceived passion transfer state across the audience.

### PRM-PRS-013 Narrative Coherence Architecture
Source: `AUDIT_HBRs_10_Must_Reads_on_Public_Speaking_Harvard_Business_Review.md`
MCDA: `178/200`
Core move: make identity stories internally legible and emotionally credible.

### PRM-PRS-021 AI-Era Presence Imperative
Source: `AUDIT_Resonate_Nancy_Duarte.md`
MCDA: `178/200`
Core move: use visible human presence and preparation as a defense against genericity.

### PRM-PRS-033 Five Talk Tools as Modular Palette
Source: `AUDIT_TED_Talks_Chris_Anderson.md`
MCDA: `178/200`
Core move: combine explanation, story, example, humor, and visual form as a toolkit rather than a single mode.

### PRM-PRS-006 Eating-the-Microphone Failure Taxonomy
Source: `AUDIT_Confessions_of_a_Public_Speaker_Scott_Berkun.md`
MCDA: `176/200`
Core move: diagnose common over-performance behaviors that destroy trust.

### PRM-PRS-027 Authenticity Imperative
Source: `AUDIT_Talk_Like_TED_Carmine_Gallo.md`
MCDA: `176/200`
Core move: stay in the narrow zone where preparation amplifies rather than falsifies selfhood.

### PRM-PRS-014 Berinato Data-Story Visualization Matrix
Source: `AUDIT_HBRs_10_Must_Reads_on_Public_Speaking_Harvard_Business_Review.md`
MCDA: `174/200`
Core move: choose visual form based on the story the data must carry.

### PRM-PRS-007 Teaching as Compassion
Source: `AUDIT_Confessions_of_a_Public_Speaker_Scott_Berkun.md`
MCDA: `172/200`
Core move: treat explanation as care rather than display.

## 6.3 Story Discovery and Narrative Structure Primitives

### PRM-STR-013 Change Choreography
Source: `AUDIT DataStory Illuminate Nancy Duarte.md`
MCDA: `194/200`
Core move: use stories, speeches, symbols, and ceremony as designed transformation moments.

### PRM-STR-006 Unsilenced Voice
Source: `AUDIT Bird by Bird Anne Lamott.md`
MCDA: `192/200`
Core move: remove borrowed permission and recover owned voice.

### PRM-STR-008 Data Point of View
Source: `AUDIT DataStory Illuminate Nancy Duarte.md`
MCDA: `192/200`
Core move: force data to carry a stance, a consequence, and a next move.

### PRM-STR-019 Narrative Stepping Stones
Source: `AUDIT How to Tell a Story Meg Bowles.md`
MCDA: `190/200`
Core move: break the journey into usable units that still preserve movement.

### PRM-STR-023 Goal-Opposition-Stakes Spine
Source: `AUDIT Screenwriting Architecture Trottier Snyder Schechter.md`
MCDA: `189/200`
Core move: organize movement around desire, obstruction, and consequence.

### PRM-STR-026 Scene Engineering
Source: `AUDIT Screenwriting Architecture Trottier Snyder Schechter.md`
MCDA: `188/200`
Core move: give every local unit a purpose, motion, and polarity.

### PRM-STR-011 Humanize Information
Source: `AUDIT DataStory Illuminate Nancy Duarte.md`
MCDA: `187/200`
Core move: attach character, conflict, and relatable scale to otherwise abstract information.

### PRM-STR-015 Stakes as the Personal Why
Source: `AUDIT How to Tell a Story Meg Bowles.md`
MCDA: `187/200`
Core move: define what is truly at stake internally and externally.

### PRM-STR-018 One-Sentence Lens
Source: `AUDIT How to Tell a Story Meg Bowles.md`
MCDA: `186/200`
Core move: compress the heart of the story into one guiding sentence.

### PRM-STR-024 Beat Architecture
Source: `AUDIT Screenwriting Architecture Trottier Snyder Schechter.md`
MCDA: `186/200`
Core move: sequence emotional thresholds rather than wandering through information.

### PRM-STR-020 Vulnerable Specificity
Source: `AUDIT How to Tell a Story Meg Bowles.md`
MCDA: `185/200`
Core move: use concrete vulnerable detail to magnify feeling and trust.

### PRM-STR-009 Audience-State Empathy and Stage Diagnosis
Source: `AUDIT DataStory Illuminate Nancy Duarte.md`
MCDA: `184/200`
Core move: detect where the audience is in the journey before choosing tone or instruction.

### PRM-STR-025 Theme as Argument
Source: `AUDIT Screenwriting Architecture Trottier Snyder Schechter.md`
MCDA: `184/200`
Core move: let the content stage a worldview claim and pressure-test it.

### PRM-STR-001 Bird-by-Bird Framing
Source: `AUDIT Bird by Bird Anne Lamott.md`
MCDA: `183/200`
Core move: reduce scale until truth can be approached without overwhelm.

### PRM-STR-016 Anecdote-to-Story Conversion
Source: `AUDIT How to Tell a Story Meg Bowles.md`
MCDA: `182/200`
Core move: turn a recounting into a real story by showing meaning, shift, and consequence.

### PRM-STR-021 Promise of the Premise
Source: `AUDIT Screenwriting Architecture Trottier Snyder Schechter.md`
MCDA: `182/200`
Core move: make the premise promise a definite audience experience, then cash it.

### PRM-STR-014 Memory Mining Through Story Seeds
Source: `AUDIT How to Tell a Story Meg Bowles.md`
MCDA: `180/200`
Core move: locate small but alive memory fragments before trying to force grand narrative.

### PRM-STR-027 Dual-Track Transformation
Source: `AUDIT Screenwriting Architecture Trottier Snyder Schechter.md`
MCDA: `180/200`
Core move: bind outer events and inner identity change together.

### PRM-STR-002 Shitty First Drafts
Source: `AUDIT Bird by Bird Anne Lamott.md`
MCDA: `179/200`
Core move: separate access from evaluation so material can surface before judgment kills it.

### PRM-STR-005 Moral Point of View
Source: `AUDIT Bird by Bird Anne Lamott.md`
MCDA: `179/200`
Core move: make sure the piece stands for something beyond surface competence.

### PRM-STR-010 Recommendation Trees
Source: `AUDIT DataStory Illuminate Nancy Duarte.md`
MCDA: `178/200`
Core move: support claims with what/why/how branching logic rather than data piles.

### PRM-STR-017 Decision-Change Arc
Source: `AUDIT How to Tell a Story Meg Bowles.md`
MCDA: `178/200`
Core move: track the choice that changed the path and the self.

### PRM-STR-022 Sympathy Engineering
Source: `AUDIT Screenwriting Architecture Trottier Snyder Schechter.md`
MCDA: `176/200`
Core move: build audience bonding before challenge or complexity intensifies.

### PRM-STR-007 Writing as Gift
Source: `AUDIT Bird by Bird Anne Lamott.md`
MCDA: `175/200`
Core move: frame communication as offering rather than display.

### PRM-STR-004 Broccoli vs KFKD
Source: `AUDIT Bird by Bird Anne Lamott.md`
MCDA: `173/200`
Core move: distinguish living intuition from inner-noise distortion.

### PRM-STR-012 Reveal Design
Source: `AUDIT DataStory Illuminate Nancy Duarte.md`
MCDA: `171/200`
Core move: control order of exposure so understanding feels staged and earned.

### PRM-STR-003 Polaroid Development Model
Source: `AUDIT Bird by Bird Anne Lamott.md`
MCDA: `163/200`
Core move: let the scene or truth come into focus gradually instead of demanding instant clarity.

## 6.4 Psychological Diagnostics Primitives

This family was also too thin before.
It now reflects more of the `05_Psychology_and_Communication` shelf because diagnosis, self-state mapping, and conversational regulation are core CCP capabilities, not optional theory.

### PRM-PSY-007 Identification Builds the Bridge
Source: `AUDIT_Jim_Rohn_Communication_Guides.md`
MCDA: `196/200`
Core move: establish felt similarity and shared reality before attempting persuasion, correction, or challenge.

### PRM-PSY-008 Attack the Problem Without Attacking the Person
Source: `AUDIT_Jim_Rohn_Communication_Guides.md`
MCDA: `193/200`
Core move: preserve dignity and alliance by separating the human from the issue under discussion.

### PRM-PSY-001 Matching Principle
Source: `AUDIT_Supercommunicators.md`
MCDA: `192/200`
Core move: detect the active conversation layer (practical, emotional, social) before responding.

### PRM-PSY-002 Looping for Understanding
Source: `AUDIT_Supercommunicators.md`
MCDA: `192/200`
Core move: prove comprehension back to the speaker to biologically regulate their nervous system.

### PRM-PSY-003 Narrative Script Flipping
Source: `AUDIT_The_Psychology_Workbook_for_Writers.md`
MCDA: `192/200`
Core move: detect the rigid internal script and rotate it into a more usable behavioral reality.

### PRM-PSY-004 Stress Pot Regulator
Source: `AUDIT_I_havent_been_entirely_honest_with_you.md`
MCDA: `190/200`
Core move: actively monitor and manage the biological stress load of the client before applying pressure.

### PRM-PSY-005 Play as Physiological Medicine
Source: `AUDIT_I_havent_been_entirely_honest_with_you.md`
MCDA: `190/200`
Core move: use play, relief, and physiological lightness as real intervention technology rather than optional mood support.

### PRM-PSY-006 Deep Questions
Source: `AUDIT_Supercommunicators.md`
MCDA: `190/200`
Core move: use vulnerability-shaped questions to move a conversation from surface exchange into meaningful connection.

### PRM-PSY-009 Inner Critic Externalisation
Source: `AUDIT_I_havent_been_entirely_honest_with_you.md`
MCDA: `188/200`
Core move: name and objectify the self-attacking voice so it can be challenged instead of obeyed.

### PRM-PSY-010 Pre-Conversation Architecture
Source: `AUDIT_Supercommunicators.md`
MCDA: `188/200`
Core move: prepare the conditions of the conversation before speaking so the interaction starts in a better state.

### PRM-PSY-011 Drama Triangle Rotation
Source: `AUDIT_The_Psychology_Workbook_for_Writers.md`
MCDA: `188/200`
Core move: detect rescuer-victim-persecutor dynamics and rotate the role structure before it hardens.

### PRM-PSY-012 Ego State Switching
Source: `AUDIT_The_Psychology_Workbook_for_Writers.md`
MCDA: `187/200`
Core move: recognize the Transactional Analysis state (Parent, Adult, Child) and guide it to Adult-to-Adult.

### PRM-PSY-013 Chameleon Protocol: Language as Identity
Source: `AUDIT_Born_a_Crime.md`
MCDA: `186/200`
Core move: calibrate linguistic identity (register, diction, cultural reference) so the audience recognizes you as a peer before evaluating your content.

### PRM-PSY-014 Trojan Horse Narrative: Comedy as Bypass
Source: `AUDIT_Born_a_Crime.md`
MCDA: `178/200`
Core move: use humor to bypass cognitive resistance before delivering a challenging or painful truth.

### PRM-PSY-015 Outsider Advantage: Marginality as Strategy
Source: `AUDIT_Born_a_Crime.md`
MCDA: `178/200`
Core move: leverage an outsider perspective to make the audience's invisible constraints and systemic assumptions visible to them.

### PRM-PSY-016 Systemic Subversion Model
Source: `AUDIT_Born_a_Crime.md`
MCDA: `184/200`
Core move: reframe a personal story to make it a diagnostic lens of a broken system rather than merely a biographical event.

### PRM-PSY-017 Empathy Inversion
Source: `AUDIT_Born_a_Crime.md`
MCDA: `182/200`
Core move: force the listener to experience the emotional reality of the opposition or system before passing judgment.

### PRM-PSY-018 Layered Narrative Architecture
Source: `AUDIT_Born_a_Crime.md`
MCDA: `176/200`
Core move: teach structural insights implicitly through story sequencing rather than explicit lecturing.

### PRM-PSY-019 Resilience Reframe
Source: `AUDIT_Born_a_Crime.md`
MCDA: `186/200`
Core move: transform vulnerability from victimhood into authority by demonstrating the agency and insight built from the failure.

### PRM-PSY-020 The Paradox of Value (Singular Path Mechanism)
Source: `AUDIT_One_to_Many_Jason_Fladlien.md`
MCDA: `194/200`
Core move: artificially restrict options to provide one clear, easy route to the desired outcome, destroying decision fatigue.

### PRM-PSY-021 Knowing vs. Feeling (Emotional Context)
Source: `AUDIT_One_to_Many_Jason_Fladlien.md`
MCDA: `181/200`
Core move: shift the speaker's responsibility from information delivery to state management.

### PRM-PSY-022 The Iterative Filter (Spew and Whittle)
Source: `AUDIT_One_to_Many_Jason_Fladlien.md`
MCDA: `179/200`
Core move: dump information without censorship, then ruthlessly delete anything not serving the Singular Path.

### PRM-PSY-023 Audience Ecological Checks
Source: `AUDIT_One_to_Many_Jason_Fladlien.md`
MCDA: `177/200`
Core move: systematically review content to ensure it does not violate the internal emotional ecosystem of the audience.

### PRM-PSY-024 Universal Webinar Emotion Palette
Source: `AUDIT_One_to_Many_Jason_Fladlien.md`
MCDA: `188/200`
Core move: deliberately orchestrate specific neurotransmitter cascades (Fear, Enthusiasm, Safety) at precise moments in the narrative arc.

### PRM-PSY-025 Clearly Defined Outcome Formula
Source: `AUDIT_One_to_Many_Jason_Fladlien.md`
MCDA: `185/200`
Core move: define the premise using a rigid Audience + Feeling + Result formula that passes the 60-minute test.

### PRM-PSY-026 Instant Gratification Hook
Source: `AUDIT_One_to_Many_Jason_Fladlien.md`
MCDA: `183/200`
Core move: provide a micro-result achievable immediately to bridge the trust gap before a long-term promise.

## 6.5 Acting and Performance Primitives

This family also needed real expansion.
Performance primitives are not just stagecraft. They help CCP produce believable delivery, real-time emotional grounding, and anti-robotic speaking behavior across recordings, reactions, webinars, and coaching.

### PRM-ACT-001 Superobjective
Source: `AUDIT_Steal_the_Show_Michael_Port.md`
MCDA: `194/200`
Core move: define the singular overarching desire driving the performance.

### PRM-ACT-002 Magic As If / Particularisation
Source: `AUDIT Sanford Meisner on Acting.md`
MCDA: `192/200`
Core move: substitute a personal emotional trigger into the performance to generate authentic reaction.

### PRM-ACT-003 Pinch and Ouch
Source: `AUDIT Sanford Meisner on Acting.md`
MCDA: `190/200`
Core move: let real stimulus justify real response so delivery feels caused rather than performed.

### PRM-ACT-010 Body Language Calibration
Source: `AUDIT Posing Portrait Adler Knight Valenzuela.md`
MCDA: `190/200`
Core move: align micro-expressions, posture, gaze, and gesture precisely with the narrative intent.

### PRM-ACT-004 Three-Act Contrast Architecture
Source: `AUDIT_Steal_the_Show_Michael_Port.md`
MCDA: `189/200`
Core move: organize the performance around a meaningful contrastive movement instead of flat informational flow.

### PRM-ACT-005 Backstory Architecture
Source: `AUDIT_Steal_the_Show_Michael_Port.md`
MCDA: `189/200`
Core move: anchor authority and emotional credibility in a coherent owned personal history.

### PRM-ACT-006 Preparation / Pre-State Self-Stimulation
Source: `AUDIT Sanford Meisner on Acting.md`
MCDA: `184/200`
Core move: intentionally enter the right emotional and physiological pre-state before the first word is spoken.

### PRM-ACT-007 Yes, And Generative Engine
Source: `AUDIT_Steal_the_Show_Michael_Port.md`
MCDA: `184/200`
Core move: expand live thought and expression by accepting the offered reality and building on it.

### PRM-ACT-008 The Bottom Line
Source: `AUDIT_Acting_for_the_Camera_Barr.md`
MCDA: `180/200`
Core move: assign one driving force to the moment so the performance has a clear directional center.

### PRM-ACT-009 Repetition Game / Anti-Intellectual Contact
Source: `AUDIT Sanford Meisner on Acting.md`
MCDA: `176/200`
Core move: break overthinking by forcing contact with the live stimulus instead of retreating into preplanned output.

## 6.6 Design and Business Primitives

This section was previously underpowered.
It now includes a fuller extract from the `06_Design_and_Business` shelf, including graphic-design primitives, because these are not optional polish moves. They help determine how content is perceived, trusted, navigated, and adopted.

### PRM-BUS-001 Perception and Behavioral Guidance as a Unified Stack
Source: `AUDIT_Design_Is_Storytelling_Ellen_Lupton.md`
MCDA: `199/200`
Core move: design visuals, flows, and action cues as one integrated attention-and-behavior system.

### PRM-BUS-002 Emotional Journey Mapping and Peak-End Memory
Source: `AUDIT_Design_Is_Storytelling_Ellen_Lupton.md`
MCDA: `196/200`
Core move: structure the emotional path of an experience so the remembered ending compounds trust and action.

### PRM-BUS-003 Narrative Arc as the Structural Backbone
Source: `AUDIT_Design_Is_Storytelling_Ellen_Lupton.md`
MCDA: `194/200`
Core move: give the user experience a meaningful progression rather than a flat sequence of disconnected assets.

### PRM-BUS-004 Design for Lived Use, Not Abstract Intent
Source: `AUDIT Beautiful Users Ellen Lupton.md`
MCDA: `194/200`
Core move: optimize every artifact for the real user state, real device, and real moment of use rather than idealized design theory.

### PRM-BUS-005 FEPS Benefit Translation
Source: `AUDIT Book Yourself Solid Michael Port.md`
MCDA: `194/200`
Core move: translate features into functional, emotional, physical, and spiritual benefits so value is experienced, not merely described.

### PRM-BUS-006 Hierarchy as Semantic Attention Routing
Source: `AUDIT Thinking with Type Graphic Design Ellen Lupton.md`
MCDA: `192/200`
Core move: route the eye and mind toward what matters first, second, and third through explicit visual and semantic hierarchy.

### PRM-BUS-007 Social Media as Relationship Infrastructure
Source: `AUDIT Book Yourself Solid Michael Port.md`
MCDA: `192/200`
Core move: treat distribution as ongoing relational trust-building, not one-shot promotion.

### PRM-BUS-008 Invitation-Based Sales Cycle Design
Source: `AUDIT Book Yourself Solid Michael Port.md`
MCDA: `190/200`
Core move: replace aggressive conversion pressure with progressively sized invitations that feel natural and dignity-preserving.

### PRM-BUS-009 Dignity Reduces Friction Better Than Force
Source: `AUDIT Beautiful Users Ellen Lupton.md`
MCDA: `189/200`
Core move: reduce hesitation by preserving the user's dignity instead of overpowering them with urgency or coercion.

### PRM-BUS-010 The Grid as Program, Not Prison
Source: `AUDIT Thinking with Type Graphic Design Ellen Lupton.md`
MCDA: `188/200`
Core move: use invisible structural systems to create scalable consistency without flattening expressive variation.

### PRM-BUS-011 Red Velvet Rope Policy
Source: `AUDIT Book Yourself Solid Michael Port.md`
MCDA: `188/200`
Core move: explicitly disqualify bad fits to instantly compound trust with good fits.

### PRM-BUS-013 Journey Architecture and Threshold Design
Source: `AUDIT_Design_Is_Storytelling_Ellen_Lupton.md`
MCDA: `184/200`
Core move: shape experience around psychologically meaningful entries, pivots, and completions rather than frictionless sameness.

### PRM-BUS-012 Typography as Voice, Not Decoration
Source: `AUDIT Thinking with Type Graphic Design Ellen Lupton.md`
MCDA: `182/200`
Core move: make type act as a nonverbal extension of tone, authority, warmth, and persona.

### PRM-BUS-014 Affordance as Behavioral Invitation
Source: `AUDIT Beautiful Users Ellen Lupton.md`
MCDA: `176/200`
Core move: make the next action feel obvious, available, and behaviorally inviting before explanation is required.

## 6.7 Photography and Sound Design Primitives

This section also needed expansion.
Photography, composition, and sound-design primitives are not minor downstream garnish. They govern perception, salience, trust, atmosphere, and anti-slop quality across CMF, Conscious Reactions, CBCS, webinars, and premium brand surfaces.

### PRM-VSG-001 Composition is Eye-Path Engineering
Source: `AUDIT The Photographers Eye Michael Freeman.md`
MCDA: `198/200`
Core move: deliberately control the viewer's scan path so attention moves in the intended sequence.

### PRM-VSG-002 Workflow Creates Aesthetics
Source: `AUDIT Designing Sound Beck Kalinak.md`
MCDA: `198/200`
Core move: treat repeatable process design as the source of reliable aesthetic quality rather than relying on isolated taste moments.

### PRM-VSG-003 Intent Should Govern Style, Not the Reverse
Source: `AUDIT The Photographers Eye Michael Freeman.md`
MCDA: `196/200`
Core move: let the communication goal decide visual and sonic treatment instead of defaulting to fashionable styling.

### PRM-VSG-004 Silence as a Positive Narrative Device
Source: `AUDIT Sound Design for Short Radio Broadcasting.md`
MCDA: `196/200`
Core move: use silence as active meaning, pacing, and emotional pressure rather than as empty absence.

### PRM-VSG-005 Visual Emphasis Must Be Intentional
Source: `AUDIT Posing Portrait Adler Knight Valenzuela.md`
MCDA: `196/200`
Core move: force a clearly dominant attention target so every visual knows what it is asking the viewer to notice first.

### PRM-VSG-006 Polyphony and Controlled Density
Source: `AUDIT Designing Sound Beck Kalinak.md`
MCDA: `195/200`
Core move: allow layered sonic richness without sacrificing intelligibility by actively budgeting density.

### PRM-VSG-007 Order Must Be Imposed on Chaos
Source: `AUDIT The Photographers Eye Michael Freeman.md`
MCDA: `194/200`
Core move: reduce clutter and ambiguity by selecting, excluding, and structuring what the viewer or listener perceives.

### PRM-VSG-008 Character Coherence Beats Isolated Beauty
Source: `AUDIT Posing Portrait Adler Knight Valenzuela.md`
MCDA: `194/200`
Core move: make every visual cue agree on the same emotional and narrative thesis instead of optimizing for prettiness alone.

### PRM-VSG-009 Process Itself Can Be Systematized
Source: `AUDIT The Photographers Eye Michael Freeman.md`
MCDA: `193/200`
Core move: convert artistic judgment into a repeatable composition workflow that can drive prompting, curation, and QA.

### PRM-VSG-010 The Invisible Medium / Imagination as Compute
Source: `AUDIT Sound Design for Short Radio Broadcasting.md`
MCDA: `193/200`
Core move: let sound trigger the listener's imagination so the audience co-creates the missing world internally.

### PRM-VSG-011 Sound as Attention Architecture
Source: `AUDIT Designing Sound Beck Kalinak.md`
MCDA: `192/200`
Core move: treat sonic layers as routing devices that direct focus, meaning, and emotional emphasis.

### PRM-VSG-012 The Frame Is an Active Meaning Device
Source: `AUDIT The Photographers Eye Michael Freeman.md`
MCDA: `191/200`
Core move: use edges, crop, aspect ratio, and breathing room to change what the subject means.

### PRM-VSG-013 Sound World Architecture
Source: `AUDIT Sound Design Harrison Lawrence Murch.md`
MCDA: `190/200`
Core move: define the acoustic world deliberately so all sonic elements feel like they belong to one authored system.

### PRM-VSG-014 Playback Context Is Part of the Composition
Source: `AUDIT Designing Sound Beck Kalinak.md`
MCDA: `190/200`
Core move: design with the actual listening environment and device reality in mind, especially phone-first consumption.

### PRM-VSG-015 Composition as Attention Routing
Source: `AUDIT Photography Story Composition Beales Freeman Barthes.md`
MCDA: `192/200`
Core move: deliberately route attention so the viewer knows what to notice first, second, and third.

### PRM-VSG-016 Light and Color as Emotional Architecture
Source: `AUDIT Photography Story Composition Beales Freeman Barthes.md`
MCDA: `186/200`
Core move: turn a scene from inert description into mood, tension, or aspiration using light and color.

### PRM-VSG-017 Character, Location, Event
Source: `AUDIT Photography Story Composition Beales Freeman Barthes.md`
MCDA: `182/200`
Core move: ensure the image always contains a specific narrative triad (character, location, event) instead of being a generic pose.

### PRM-VSG-018 Sequence Over Single Image
Source: `AUDIT Photography Story Composition Beales Freeman Barthes.md`
MCDA: `178/200`
Core move: build meaning across multiple frames (carousels, reels) rather than relying on one static visual.

### PRM-VSG-019 Story Gap as Visual Engine
Source: `AUDIT Photography Story Composition Beales Freeman Barthes.md`
MCDA: `171/200`
Core move: leave enough ambiguity or unresolved tension in the image that the viewer is forced to infer the larger reality.

### PRM-VSG-020 Perspective and Layering as Meaning
Source: `AUDIT Photography Story Composition Beales Freeman Barthes.md`
MCDA: `167/200`
Core move: use depth, foreground framing, and perspective to imply psychological relationship and scale.

### PRM-VSG-021 Punctum, Air, and Felt Truth
Source: `AUDIT Photography Story Composition Beales Freeman Barthes.md`
MCDA: `160/200`
Core move: include an arresting detail, flaw, or trace of time that gives the image a feeling of lived reality rather than sterile perfection.

### PRM-VSG-022 Selective Focus as Meaning Control
Source: `AUDIT The Filmmakers Eye Gustavo Mercado.md`
MCDA: `191/200`
Core move: use shallow or deep focus to determine what remains cognitively dominant and what lingers as contextual pressure.

### PRM-VSG-023 Lens Choice as Emotional Syntax
Source: `AUDIT The Filmmakers Eye Gustavo Mercado.md`
MCDA: `188/200`
Core move: use focal length (wide vs telephoto) to imply different emotional relationships between subjects, environments, and viewers.

### PRM-VSG-024 Space as Psychological Relationship
Source: `AUDIT The Filmmakers Eye Gustavo Mercado.md`
MCDA: `183/200`
Core move: manipulate perspective to convert geography into psychology, making a space feel trapping, expanding, or exposing.

### PRM-VSG-025 Intangibles and Optical Personality
Source: `AUDIT The Filmmakers Eye Gustavo Mercado.md`
MCDA: `178/200`
Core move: use optical imperfections like texture, flare, or vignetting to imply history, realism, and documentary presence.

### PRM-VSG-026 Image Systems, Not Isolated Shots
Source: `AUDIT The Filmmakers Eye Gustavo Mercado.md`
MCDA: `176/200`
Core move: design visuals in relation to their neighbors, establishing a norm and breaking it to communicate psychological shifts.

### PRM-VSG-027 Movement Perception Through Lens Behavior
Source: `AUDIT The Filmmakers Eye Gustavo Mercado.md`
MCDA: `169/200`
Core move: alter the felt velocity and tension of an action through focal length and spacing rather than just blur.

### PRM-VSG-028 Distortion as Subjectivity
Source: `AUDIT The Filmmakers Eye Gustavo Mercado.md`
MCDA: `160/200`
Core move: use optical warping intentionally to communicate altered perception, psychological fracture, or unreality.

### PRM-VSG-029 Density / Clarity Budgeting
Source: `AUDIT Sound Design Harrison Lawrence Murch.md`
MCDA: `188/200`
Core move: intentionally manage the density of sound layers so the core signal remains perfectly clear without losing richness.

### PRM-VSG-030 Listener Custody / Greatest-Impact Thinking
Source: `AUDIT Sound Design Harrison Lawrence Murch.md`
MCDA: `186/200`
Core move: take custody of the listener's ear by ensuring the most important sound is always the easiest to hear.

### PRM-VSG-031 Negative Space / Silence Control
Source: `AUDIT Sound Design Harrison Lawrence Murch.md`
MCDA: `183/200`
Core move: use the absence of sound dynamically to create tension, reveal context, or pace an emotional shift.

### PRM-VSG-032 Reason-for-Everything Verification
Source: `AUDIT Sound Design Harrison Lawrence Murch.md`
MCDA: `180/200`
Core move: interrogate every sonic choice to ensure it earns its place in the arrangement and serves the primary narrative intent.

### PRM-VSG-033 Encoded vs Embodied Sound Routing
Source: `AUDIT Sound Design Harrison Lawrence Murch.md`
MCDA: `178/200`
Core move: balance intellectual sound cues (encoded meaning) with visceral sound cues (embodied feeling) for total impact.

### PRM-VSG-034 Motif / Foreshadowing Map
Source: `AUDIT Sound Design Harrison Lawrence Murch.md`
MCDA: `175/200`
Core move: structure repeating sonic signatures across an experience so the ear learns the language and anticipates the payoff.

## 6.8 Voice and Audio Intimacy Primitives

This family needed the biggest correction.
Voice intimacy, ear-writing, broadcast clarity, and acoustic trust are central to CCP, CBCS, and Conscious Reactions. Four entries was not a serious representation of the audit shelf.

### PRM-VOC-001 Write for the Distracted Ear
Source: `AUDIT Better Broadcast Writing Greg Dobbs.md`
MCDA: `197/200`
Core move: write so the message remains clear and memorable even when heard once in imperfect attention conditions.

### PRM-VOC-002 Audience-of-One Intimacy
Source: `AUDIT Finding Your Voice Rob Quicke.md`
MCDA: `196/200`
Core move: speak directly to a single imagined listener to create psychological closeness.

### PRM-VOC-003 Writing for the Ear, Not the Eye
Source: `AUDIT Finding Your Voice Rob Quicke.md`
MCDA: `194/200`
Core move: draft content specifically for spoken rhythm, breathing cadence, and auditory processing.

### PRM-VOC-004 Proofread Aloud as Broadcast Validation
Source: `AUDIT Better Broadcast Writing Greg Dobbs.md`
MCDA: `193/200`
Core move: test every spoken line aloud before shipping it so dead phrasing and synthetic rhythm are caught early.

### PRM-VOC-005 R.E.A.L. Audio Quality Gate
Source: `AUDIT Finding Your Voice Rob Quicke.md`
MCDA: `191/200`
Core move: validate that audio feels relatable, engaging, authentic, and liberating before adding more polish.

### PRM-VOC-006 Start Strong, End Strong
Source: `AUDIT Better Broadcast Writing Greg Dobbs.md`
MCDA: `191/200`
Core move: maximize the first and last lines because they disproportionately shape emotion, memory, and continuation.

### PRM-VOC-007 The Theatre of the Mind
Source: `AUDIT Interviewing for Radio.md`
MCDA: `185/200`
Core move: use sound and speech to make the listener visualize the scene instead of merely receiving information.

### PRM-VOC-008 Lead-In and Tag Architecture
Source: `AUDIT Better Broadcast Writing Greg Dobbs.md`
MCDA: `184/200`
Core move: make the opening orientation and closing handoff structurally deliberate rather than improvised.

### PRM-VOC-009 Sensory Scene Anchoring
Source: `AUDIT Finding Your Voice Rob Quicke.md`
MCDA: `183/200`
Core move: use vivid sensory cues to build the theater of the mind for the listener.

### PRM-VOC-010 The Edited Essence
Source: `AUDIT Interviewing for Radio.md`
MCDA: `180/200`
Core move: compress aggressively until only the most signal-rich spoken material remains.

### PRM-VOC-012 The Silent Facilitator
Source: `AUDIT Interviewing for Radio.md`
MCDA: `174/200`
Core move: create better spoken output by listening actively and intervening minimally so the subject's real signal can surface.

### PRM-VOC-011 Microphonic Intimacy and Spatial Proximity
Source: `AUDIT Sound Design for Short Radio Broadcasting.md`
MCDA: `173/200`
Core move: use proximity, mic feel, and acoustic nearness to increase disclosure, trust, and warmth.

## 6.9 Referral and Trust-Transfer Primitives

### PRM-REF-001 Partner Over Source
Source: `AUDIT Mitano Referral Leverage CCP Referral Magnitude.md`
MCDA: `193/200`
Core move: select operating partners with shared upside rather than passive link-sharers.

### PRM-REF-007 Commercial Reframe Architecture
Source: `AUDIT Mitano Referral Leverage CCP Referral Magnitude.md`
MCDA: `193/200`
Core move: change the prospect's understanding of their problem before pitching a solution.

### PRM-REF-006 Preemptive Value Shaping
Source: `AUDIT Mitano Referral Leverage CCP Referral Magnitude.md`
MCDA: `192/200`
Core move: deliver insight before the prospect enters commodity-comparison mode.

### PRM-REF-002 Trust-Transfer Ladder
Source: `AUDIT Mitano Referral Leverage CCP Referral Magnitude.md`
MCDA: `191/200`
Core move: stage the introduction so the guest experiences value (interview, output, benchmark) before any ask.

### PRM-REF-005 Recipient-Centric Relationship Artifact Design
Source: `AUDIT Mitano Referral Leverage CCP Referral Magnitude.md`
MCDA: `191/200`
Core move: deliver proof outputs that make the recipient feel proud, avoiding overt platform branding.

### PRM-REF-003 Hidden Asset Mining
Source: `AUDIT Mitano Referral Leverage CCP Referral Magnitude.md`
MCDA: `189/200`
Core move: convert byproducts like interview footage and benchmark data into primary acquisition tools.

### PRM-REF-004 Piggyback Distribution
Source: `AUDIT Mitano Referral Leverage CCP Referral Magnitude.md`
MCDA: `188/200`
Core move: leverage the partner's existing audience trust rather than building from zero.

### PRM-REF-008 Message-to-Role Resonance Mapping
Source: `AUDIT Mitano Referral Leverage CCP Referral Magnitude.md`
MCDA: `187/200`
Core move: translate the same core capability differently for the coach, the audience, and the partner.

### PRM-REF-009 Constructive Tension Control
Source: `AUDIT Mitano Referral Leverage CCP Referral Magnitude.md`
MCDA: `182/200`
Core move: apply enough pressure to force a decision without breaking the underlying trust.

## 6.10 Registry Notes on Duplicates and Merge Rules

The following should be treated as same-core or near-same-core primitives unless later benchmarking proves they need full separation:

- `Rule of Three` and `Triadic Pattern Disruption`
- `What-Is / What-Could-Be` across `Resonate` and `DataStory`
- `Irreducible Truth` and `Subtext as Core Payload`
- `Expectation Reversal` and some uses of `Irony Inversion`
- `Hyper-Specificity Anchoring` and `Vulnerable Specificity` should remain separate for now
  - one is a detail-anchor primitive
  - one is an emotional amplification primitive

---

## 7. Minimal Implementation Recommendation

The first implementation pass should not try to operationalize all primitives at once.

### Phase 1

Build the packet layer:

- `PrimarySignalPacket`
- `PrimitiveCandidatePacket`
- `CoalitionSignature`
- `CCFRoutingRecommendation`

### Phase 2

Operationalize a small high-value primitive set:

- `Irony Inversion`
- `Tribal Reference`
- `What-Is / What-Could-Be`
- `One-Sentence Lens`
- `Vulnerable Specificity`
- `Analogy Bridge`
- `Strong Title as Idea Architecture`
- `Throughline`
- `Stakes as the Personal Why`
- `Connection Before Content`

### Phase 3

Begin coalition benchmarking rather than only archetype benchmarking.

That is where the actual moat begins:

- not only which archetype wins
- not only which framework wins
- but which primitive geometries survive reality best

---

## 8. Final Position

The primitive layer should not be treated as a poetic inspiration shelf.

It should become:

- a packet-producing perception layer
- a sovereign registry of typed expressive units
- a coalition-learning benchmark system
- an upstream force multiplier for both trigger design and content routing

The most important conclusion is this:

**the audits already contain enough usable primitive material to build a real registry now.**

What was missing was not source richness.
What was missing was the production contract that tells CCP:

- how to store primitives
- how to activate them
- how to test them
- how to combine them
- and how to learn from the coalitions they form
