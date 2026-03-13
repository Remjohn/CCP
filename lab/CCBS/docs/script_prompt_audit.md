# The Last Mile Problem: Script Prompts vs. Trigger-First Architecture

**CCF Architecture Audit — Prompt Consumption Layer**

*Cross-reference: CCF Bible Critique v2 × 90 Script Prompts × Trigger-First Engine (Phase 10 + 10.1) × Distribution Skills × Component Library*

---

## Executive Problem Statement

The Trigger-First Engine rebuilt the CCF pipeline from the root: emotional DNA extraction, 4-axis structural matching, LIWC-22 authentication gates, seed construction with ESK anchors, tribal language enforcement, and a closed LIWC feedback loop. The upstream pipeline is now architecturally sound — it produces precision seeds from the intersection of the coach's formative experience and the audience's current L3 reality.

But the seeds arrive at the generation layer — the 90 Script Prompts in `Script Prompts/` — and encounter a system that was designed before any of this existed. The prompts still receive `{content_idea}` as their primary input. They still assign role-characters ("Channel the voice of a seasoned expert"). They still use single-layer priming. They still validate quality with post-hoc checklists the model self-assesses. They do not ingest seeds, authentication certificates, tribal terms, 3-layer voice DNA, or structural congruence points.

The upstream system grows precision seeds. The downstream system plants them in generic soil. This document details 24 specific lessons from cross-referencing the CCF Bible Critique v2 against the current prompts and the Trigger-First architecture, then specifies what must change.

---

## Prompt Taxonomy and Obsolescence Analysis

The `Script Prompts/` folder contains **90 files** across 7 categories:

| Category | Count | Examples | Status |
|:---------|:------|:---------|:-------|
| **Story Archetypes (Generative)** | 16 | Achievement, Transformation, Discovery, Joy, Relief | Active — needs rewrite |
| **Story Archetypes (Interview Framework)** | 16 | Achievement Interview, Curiosity Interview, Romance Interview | **Likely obsolete** |
| **Myth/Listicle Archetypes** | 18 | Disgusting Myth, Fear-Anxiety Listicle, Shocking Listicle | Active — needs rewrite |
| **Script Archetypes** | 10 | Authority Tier List, Nostalgia Reaction, Outrage Reaction, Worst Case | Active — needs rewrite |
| **Poll/Comparison/Case Study** | 16 | Controversial Dilemma Poll, FOMO Case Study, Funny Comparison | Active — needs rewrite |
| **Tweet/Meme Archetypes** | 8 | Persuasive Tweets, Thought Whisperer, Benign Violation Meme | Active — needs rewrite |
| **Utility Prompts** | 6 | SoC Agent, Content Hook, Caption prompts, Hero Journey Visual | Active — needs rewrite |

### The 16 Interview Frameworks Are Obsolete

The Interview Framework prompts were designed to generate interview question sequences that extract stories from the coach. Their purpose: "generate a completely customized interview guide" with phases like "Goal Archaeology," "Struggle Archaeology," and "Breakthrough Archaeology."

The Trigger-First Engine replaced this entire function. Coach material is now extracted through:

1. **Activation Event Designer** — constructs precision elicitation events from 4-axis matched seeds with ESK anchors
2. **Provocation Generator** — formats events as Telegram-deliverable prompts with tribal language enforcement
3. **Coach Elicitation Engine** — processes voice note responses with LIWC-22 authentication gating and dual failure mode diagnostics

The interview frameworks extract stories from *topics*. The Trigger-First Engine extracts material from *structural congruence points*. The elicitation method is fundamentally different — sensory-specific activation events that generate prediction error (Nader reconsolidation), not interview questions that surface narrative. The 16 Interview Framework prompts can be archived. They served their purpose in the pre-trigger-first architecture.

**Remaining active prompts: 74.** These are the prompts that require the architectural rewrite.

### The 22 Enhanced Viral Frameworks Are Not Properly Mapped

The `🧠 The 22 Enhanced Viral Frameworks.md` defines the strategic source of truth: 22 frameworks split into a Value-Based Engine (11 frameworks) and an Emotional-Based Engine (11 frameworks). Each framework specifies a psychological trigger, purpose, implementation patterns, emotional outcome, and viral mechanics.

The 90 Script Prompts are supposed to be the execution layer of these frameworks. But the relationship is broken:

| Problem | Evidence |
|:--------|:---------|
| **No formal link between framework and prompt** | No prompt references its parent framework by ID. No prompt ingests framework metadata (psychological trigger, emotional outcome, viral mechanics). |
| **Prompt proliferation beyond framework scope** | 90 prompts for 22 frameworks = prompts have multiplied independently. Story archetypes (Achievement, Curiosity, Joy, etc.) map to Framework 12 (Emotional Triggers) but have no formal binding. |
| **Framework metadata is locked in prose** | The 22 frameworks contain structured data (psychological triggers, implementation patterns, emotional outcomes) trapped in a markdown file. No YAML or JSON version exists. No skill or prompt can programmatically consume this data. |
| **Missing frameworks** | Some frameworks (e.g., Framework 5: Combinations/Intersection, Framework 14: Broad Appeal/Universal Resonance) have NO corresponding Script Prompt at all. |
| **Duplicate coverage** | Framework 6 (Comparison & Contrast) and Framework 19 (Conceptual Contrasts) overlap — and there are 5+ comparison prompts in the folder. |

**The fix:** Create a `content_archetypes.json` or `content_archetypes.yaml` registry file that:
- Maps each of the 22 frameworks to its corresponding SKILL.md prompt(s)
- Contains the framework metadata in machine-readable format (psychological trigger, emotional outcome, viral mechanics, implementation patterns)
- Is consumed by the `blueprint-distiller` to select the correct prompt SKILL based on emotional state + framework match
- Eliminates orphan prompts and fills coverage gaps

### Distribution Skills Have No Archetype Source of Truth

Three distribution-layer skills reference archetypes but have no structured source to consume:

| Skill | Archetype Reference | The Gap |
|:------|:-------------------|:--------|
| **Art Director** | `content_archetype` appears as input (line 78, 117). Mentions 4 visual categories: Single Frame, Comparison, Sequential, Instructional | `content_archetype` is a ghost variable — referenced but never supplied by any upstream skill. The 4 categories don't map to the 22 Frameworks. |
| **Orchestrator** | Zero archetype awareness | Loops over AUTHORIZED scripts, dispatches to Smart Mix + Art Director. Doesn't know what archetype each script IS. |
| **Smart Mix** | Zero archetype awareness | Uses "5 persona versions" (Standard, Generational, Humor, Dramatic, Wildcard) — synthesis personas, not content archetypes. Doesn't know what framework the content came from. |

The root cause: no `content_archetypes.json` exists anywhere in the system. The Art Director's "analyze the content_archetype" instruction references a variable that was never formally populated by any upstream skill. The blueprint-distiller selects which archetype prompt to use but doesn't write the framework metadata to a structured field the distribution layer can consume.

### Existing Component Library — Already Built, Never Wired

Two archetype reference documents were discovered that contain exactly the structured data the system needs:

**`🟨 Archetype JSON.md`** — A 77-entry cross-mapping table:
- Maps each Framework (Practical Value, Target Curiosity, Emotional Triggers, etc.) to every compatible Archetype (Listicles, Storytelling, Polls, etc.)
- Each entry has: `ID`, `Framework Name`, `Archetype Name`, `Priority Level` (1-10), `Usage Notes`, `Persuasive Angles`
- This IS the selection logic the distribution layer needs — but it's trapped in escaped JSON inside a markdown file

**`prompts_archetypes (1).md`** — The complete 5-layer component library:

| Layer | Content | Current Status |
|:------|:--------|:---------------|
| **I. 22 Viral Frameworks** | Strategy layer — identical to frameworks doc | ❌ Not in JSON |
| **II. 9 Persuasive Angles** | Psychology layer — Allay Fears, Encourage Dreams, Justify Failures, Confirm Suspicions, Throw Rocks, Problem Amplification, Favorable Evidence, Black & White, The Challenger | ❌ Not referenced in ANY current skill |
| **III. Content Archetypes** | Format layer — 8 categories (Listicles ×7, Storytelling ×16, Case Studies ×6, Comparisons ×5, Myths ×6, Tier Lists ×7, Reactions ×4, Memes ×4) + Core Formats ×8 | ❌ Not in JSON |
| **IV. Archetype Palettes** | Voice engineering — TTT gravity tables mapping each archetype to Base Gravity, Accent Layer, and Intuitive Layer with specific TTT levels (TTT-02 through TTT-09) | ❌ Not in JSON, not consumed by any skill |
| **V. Witness Integration** | Proof injection — rules for injecting transformation witness data into specific archetype slots (Before/Turning Point/After components) | ❌ Not wired to generation layer |

The structured data EXISTS. It was designed. But it was never:
- Converted to actual machine-readable JSON/YAML
- Wired to the `blueprint-distiller` (which selects archetypes)
- Wired to the Art Director (which needs `content_archetype`)
- Wired to the distribution skills (which are archetype-blind)
- Updated for the Trigger-First Engine (no seed, tribal terms, 3-layer SPR)

---

## 24 Lessons: What the Bible Critique Reveals When Read Against the Trigger-First Engine

### Section A — The Doctrine's Core Violations (Lessons 1-7)

**Lesson 1 — Instructions must be generative, not descriptive.** Every Script Prompt includes role assignments: "You are 'The Trusted Authority'" (Top Reliable List), "You are a whistleblower" (Disgusting Myth), "You are the 'Authentic Voice Synthesizer'" (SoC). The Bible Critique proves these find the model's statistical centroid of the assigned role. Two different models with different architectures produced structurally identical outputs when given the same role. The fix is cognitive state instructions — descriptions of what mental operation is executing. "Compression after decision" is a cognitive state that produces specific sentence construction properties. "Seasoned expert" is a character that produces a performance. Every prompt needs this replacement.

**Lesson 2 — Three-Layer Priming is entirely absent.** The Critique identifies that single-layer priming (aesthetic word clusters like "revolting revelations, sickening scams, visceral reactions") activates the correct emotional register but shapes it as *genre*, not *coach*. The emotional gravity field lands on the investigative journalist archetype because that is the statistical center of disgust-content. Layer 2 (Coach Emotional Path — how *this* coach travels through the activated emotion, from voice_dna_spr emotional mechanics) and Layer 3 (Leadership Elevation Trigger — which of the 12 Attractive Leader Traits this format activates at this coach's peak expression) do not exist in any of the 74 active prompts. This is the single most impactful gap because it means the generation layer has no mechanism to shape the emotional container to the individual coach.

**Lesson 3 — Post-hoc quality validation creates performative writing.** Every prompt ends with "BUILT-IN QUALITY VALIDATION" checklists: "Does this sound like a real person talking, not an AI writing?" (SoC), "Does this genuinely create a visceral feeling of disgust?" (Disgusting Myth). Wei et al. (2022) demonstrated that models write *toward* visible criteria at the end of a prompt. The checklist is satisfied performatively. The model does not and cannot self-validate whether its output sounds like a real person. The fix: move these to pre-generation construction constraints that shape the output structurally before the first word is generated. "You are following one thought. If at any point you have more than one argument active simultaneously, you have left the thought. Return." — that is a constraint the model can enforce during generation.

**Lesson 4 — The Authenticity Protocol describes mechanics without explaining them.** "Weave their signature metaphors throughout the narrative" tells the model to *place* metaphors. Not *when* the metaphor arrives (at the end of a build, as compression after expansion), not *what precedes it* (the accumulation of evidence that makes the metaphor feel inevitable), not *what follows it* (the silence, the period, the drop in sentence length). Without mechanical deployment rules, metaphors appear decoratively — placed rather than emerging from the construction logic. The distinction sounds academic. In output, it is the difference between "this person uses good metaphors" and "this person's metaphors arrive exactly when they must."

**Lesson 5 — Template structure as section checklist destroys causal sequencing.** "Hook → Value Promise → Listicle Core → CTA" appears in most prompts as a section form. The GLM-5 output exposed this by labeling sections "NUMBER ONE, NUMBER TWO, NUMBER THREE" — the model announcing its template awareness. The test for a genuine construction sequence: if the sections can be reordered without meaningfully changing the output, they are boxes, not causation. Each section should explicitly create the conditions the next section requires. The hook creates a specific tension. The value promise redirects that tension. The core resolves through that redirection. If any step can be swapped, the structure is a form.

**Lesson 6 — Role performance regression is a law.** By request 40 in a 97-step pipeline where different agents have been assigned "The Trusted Authority," "A sharp-witted Journalist," "A whistleblower," and "The Authentic Voice Synthesizer," the coach's voice has been filtered through at least seven archetype distributions. Anthropic's 2024 persona stability research and DeepMind's 2025 findings both document drift toward archetype centroid within 3-5 generations. The aggregated output is a committee of archetypes, not a person. Cognitive state instructions persist across pipeline stages because logical operations are more stable than aesthetic associations.

**Lesson 7 — Validation checklists contain non-computable items.** "Does the tribal language feel natural, not forced?" is not a binary logical operation a model can execute. "Is the voice indistinguishable from the client's authentic comedic style?" is not computable. Quality theater produces checkmarks without quality. The replacement: binary, model-executable checks tied to encoded constraints. "Does every sentence in the compression zone contain ≤12 words?" — that is computable.

### Section B — What Dies at the Prompt Boundary (Lessons 8-14)

**Lesson 8 — Seeds have no soil in the generation layer.** The upstream pipeline constructs `structural_congruence_point` objects: the exact coordinates where the audience's current experience and the coach's formative experience share the same map position. The Script Prompts receive `{content_idea}` — a topic string. The entire trigger-matching architecture — the 4-axis matching, the seed construction, the ESK anchor — evaporates before reaching the generation layer. The content is not constructed FROM the congruence point. It is constructed from a topic, decorated with values.

**Lesson 9 — Tribal language dies at the prompt boundary.** We enforced ≥3 verified tribal terms through the pipeline: seed → activation event → provocation → voice note. But the Script Prompts do not know tribal terms exist. The generation layer uses whatever vocabulary the model's prior distribution suggests for this topic and role combination. The audience's exact in-group terms — the language that carries the sub-cortical recognition signal (Clark & Brennan, 1991) — are absent from the final output that the audience actually reads.

**Lesson 10 — The authentication certificate is not consumed.** Every voice note transcription has an `authentication_certificate` with a composite LIWC score, per-marker breakdown, and `dual_layer_activation_detected` flag. No Script Prompt checks it, reads it, or adjusts generation behavior based on it. Material authenticated as dual-layer activated (both original encoding and PTG path simultaneously present) should be treated with significantly more fidelity than material that passed the gate at 0.42. The generation layer cannot distinguish between them.

**Lesson 11 — Voice DNA's 3-layer SPR is not injected.** The Voice DNA system produces a 3-layer SPR: Layer 1 (construction mechanics — sentence skeletons, discourse marker positions, rhythm patterns), Layer 2 (emotional path mechanics — how the coach travels from activation to expression), Layer 3 (leadership elevation triggers — peak expression of specific traits). The Script Prompts still use the monolithic `{Conscious_Soul_Values}` — a flat values object that conflates soul-alignment, voice-replication, and emotional resonance into one mechanism. The Critique's Principle 12 identifies this conflation as the deepest architectural flaw.

**Lesson 12 — Emotional DNA is invisible to the generation layer.** The 10-variable Emotional DNA profile drives trigger matching, archetype selection, and activation event design upstream. The Script Prompts do not receive it. The coach's appraisal sequence, coping potential pattern, norm compatibility threshold, and trigger specificity threshold — the mechanics that differentiate *this* coach from *every other* coach in the same domain — are not available to the agent writing the final script. The generation layer knows what the coach believes. It does not know how the coach's emotional architecture processes belief into expression.

**Lesson 13 — Collision DNA has no representation.** The structural congruence point — the precise overlap between coach formative experience and audience current reality — should be the generation anchor. The Script Prompt should construct FROM the congruence point, through the emotional path, using the construction mechanics. Instead, it constructs from `{content_idea}` and decorates with `{Conscious_Soul_Values}`. The collision between coach and audience — the entire thesis of the Trigger-First Engine — is not architecturally present in the generation layer.

**Lesson 14 — Negative Space is absent.** Zero prompts contain what the coach must NOT produce. The `negative_space` object from `coach_soul.json` exists but is only consumed by the `coach-elicitation` engine's probe generator sub-agent. The 74 active Script Prompts have no boundary conditions. Content can drift past the coach's identity edges — adopting tonal registers, vocabulary classes, or rhetorical moves this coach would never use — with no structural mechanism to prevent it. The Negative Space Object must be loaded BEFORE positive DNA in every prompt.

### Section C — Answering Your Direct Questions (Lessons 15-20)

**Lesson 15 — The 3-Part Priming is NOT implemented in any downstream production skill.** The SoC generator, the dynamic-theme-generator, and all 74 active Script Prompts use single-layer priming only. Layer 2 (Coach Emotional Path) and Layer 3 (Leadership Elevation Trigger) exist as concepts in the Critique and as extractable data in the pipeline (voice_dna_spr + emotional_dna), but zero downstream skills consume them as priming layers.

**Lesson 16 — You are not overthinking it. The prompts are ~60% aligned.** The 60% that works: soul-alignment (correct beliefs, correct values, correct moral position). The 40% that is missing: voice-replication at construction level (how sentences are built, not what words are used), emotional resonance (the coach's specific path through the activated emotion), and structural coupling (content built from the same map position as the audience's L3 pain). The 40% gap is not polish. It is the entire Trigger-First thesis absent from the generation layer.

**Lesson 17 — Use Skills, not templates.** Templates are static forms. Skills are instruction sets with I-R-E-V-C protocols, inputs, pre-generation constraints, validation gates, and checkpoint logging. The Script Prompts must become SKILL.md files because they need to: (a) INGEST upstream data — seed, authentication certificate, voice_dna_spr, emotional_dna, tribal terms, negative space; (b) enforce pre-generation constraints — tribal language fidelity, causal sequencing, negative space boundaries; (c) execute structural validation — binary model-executable checks; and (d) produce machine-readable output with provenance tracking. A markdown template cannot enforce any of this.

**Lesson 18 — Deep Reasoning IS needed for creative prompts, but applied to construction logic.** Deep reasoning in upstream skills operates on structural logic (LIWC scoring, 4-axis matching, appraisal variable comparison). In creative prompts, deep reasoning operates on construction logic — the causal chain that produces the output. What emotional state is the coach in? (from authentication_certificate). What structural congruence point are we building from? (from seed). What does this coach's emotional path through this activation look like? (from emotional_dna + voice_dna_spr Layer 2). What construction mechanics apply at each energy level? (from voice_dna_spr Layer 1). This is reasoning — just applied to creative materials rather than scoring algorithms.

**Lesson 19 — The Memetic Protocol belongs at the prompt layer, not the SoC layer.** The four memetic pillars (Immediate Comprehension, High-Arousal Emotion, Tribal Signal, Inherent Shareability) are research-validated and should be preserved. But they belong in the 74 active Script Prompts (public-facing content generation), not in the SoC generator (source material). Testing source material for standalone viral potential is a category error identified by the Critique's Principle 9. The Script Prompts are the correct architectural location for the Memetic Protocol.

**Lesson 20 — Fixed word count targets are counterproductive.** "120-180 words" appears in most prompts. DeepMind's 2025 findings document word count constraints as among the lowest-priority instructions in long-context scenarios for 2026 models. The replacement: structural completion criteria. "The construction is complete when: the mechanism has been named, the congruence point has been expressed in tribal language, the compression zone has arrived, and the moral verdict has landed." Structural logic survives model capability increases. Numeric limits do not.

### Section D — The Architectural Inversion (Lessons 21-24)

**Lesson 21 — The DNA layers need to be the SOIL, not decorations.** Currently: `{content_idea}` is the seed, `{Conscious_Soul_Values}` is the soil, and Voice/Emotional DNA are referenced decoratively if at all. The required inversion: `{structural_congruence_point}` is the seed, `{voice_dna_spr}` (3-layer) is the soil, `{emotional_dna}` is the root system, and `{content_idea}` is merely the classification tag. The content grows FROM the congruence point, THROUGH the emotional path, USING the construction mechanics, WITHIN the archetype container. Not the other way around.

**Lesson 22 — The archetype containers are topic-shaped, not trigger-shaped.** We inverted archetype selection upstream to be driven by emotional state. But the archetype prompt templates still frame around "present information about {content_idea}" rather than "construct from the structural congruence point between coach and audience." The container must be reshaped so the seed fits naturally — so the trigger-first material is the content's foundation, not an addition to a topic-based frame.

**Lesson 23 — The SoC Agent specification is outdated.** The SoC prompt specifies "160-240 words" and uses the old input variables (`{content_idea}`, `{Conscious_Soul_Values}`, `{character_lexicon}`). The upstream SoC generator skill was upgraded to v6.1 with authenticated ESK material as the primary source, 720-800 word output, and trigger-first source hierarchy. The Script Prompt for the SoC Agent does not reflect any of these changes.

**Lesson 24 — Mandate 8's dependency is now satisfied.** The Critique's eighth mandate states: "Build the Emotional DNA extraction layer before rebuilding the 92 prompts." That dependency is resolved. The extraction layer is built — Emotional DNA, Voice DNA 3-layer SPR, trigger architecture, 4-axis matching, seed construction, and LIWC authentication all exist as populated input objects. The prompts CAN now be rebuilt because every input they need is available upstream. The sequence barrier is cleared.

---

## What Must Change: The Phase 11 Architecture

| Component | Current State | Required State |
|:----------|:-------------|:---------------|
| **File format** | 90 markdown templates (74 active, 16 obsolete) | 74 SKILL.md files with I-R-E-V-C protocol |
| **Archetype data** | Trapped in prose markdown (`🟨 Archetype JSON.md`, `prompts_archetypes (1).md`) | 4 JSON files: `content_archetypes.json`, `archetype_palettes.json`, `persuasive_angles.json`, `framework_archetype_map.json` |
| **Distribution skills** | Archetype-blind (Art Director has ghost variable, Orchestrator/Smart Mix have zero archetype awareness) | All 3 consume `content_archetypes.json`; Art Director receives archetype + visual category + TTT palette |
| **Primary input** | `{content_idea}` (topic string) | `{structural_congruence_point}` (from seed) |
| **Voice input** | `{Conscious_Soul_Values}` (flat dump) | 3 separate inputs: `{conscious_soul_values}` + `{voice_dna_spr}` L1+L2+L3 |
| **Priming** | Single-layer (aesthetic word cluster) | 3-layer (universal emotion + coach emotional path + leadership elevation) |
| **Instructions** | Role assignments | Cognitive state instructions |
| **Template structure** | Section checklists | Causal construction sequences |
| **Quality validation** | Post-hoc checklists | Pre-generation constraints |
| **Negative space** | Absent | `{negative_space}` from `coach_soul.json` loaded first |
| **Tribal language** | Absent | `{audience_tribal_terms}` from seed injected |
| **Authentication** | Absent | `{authentication_certificate}` consulted |
| **Persuasive angles** | Exist in docs but zero skills consume them | `persuasive_angles.json` consumed per-archetype |
| **TTT voice palette** | Exist in docs but zero skills consume them | `archetype_palettes.json` injects TTT gravity per archetype |
| **Word count** | Fixed targets | Structural completion criteria |
| **Deep reasoning** | Not present | Construction logic applied |

### Recommended Execution Order

1. **Convert `🟨 Archetype JSON.md`** to actual `framework_archetype_map.json` in `intelligence_library/` — clean JSON with the 77-entry cross-mapping (Framework → Archetype → Priority → Persuasive Angles)
2. **Extract Archetype Palettes** from `prompts_archetypes (1).md` into `archetype_palettes.json` — TTT gravity tables per archetype (Base Gravity, Accent Layer, Intuitive Layer)
3. **Extract the 9 Persuasive Angles** into `persuasive_angles.json` — the psychology layer absent from the entire current pipeline
4. **Archive the 16 Interview Framework prompts** — document the deprecation reason (Trigger-First Engine replaces interview-based elicitation)
5. **Audit prompt-to-framework mapping** — identify orphan prompts, missing coverage, and duplicate implementations against the 22 frameworks + 77-entry cross-map
6. **Wire JSON files** to `blueprint-distiller`, `art-director`, `orchestrator`, and `smart-mix` — so distribution skills receive archetype metadata, visual category, TTT palette, and persuasive angle
7. **Define the New Script Prompt Skill Architecture** — the standardized SKILL.md template encoding all 8 mandates from the Bible Critique + Trigger-First inputs + archetype metadata consumption
8. **Build two reference implementations** — rewrite the SoC Agent and the Disgusting Myth as full SKILL.md files to establish the pattern
9. **Batch-convert the remaining prompts** — applying the established pattern, consolidating where frameworks overlap, filling coverage gaps

> [!IMPORTANT]
> The prompts are not broken. They produce soul-aligned content reliably. The gap is between structurally correct and *actually this person speaking from the exact territory the audience is currently living in*. That gap is the distance between professional empathy and neural coupling. The Trigger-First Engine closed it upstream. The Script Prompts are the last mile where it reopens.

---

*CCF Architecture Audit — v2.0 — March 2026*
*Updated: Distribution skills gap, component library discovery, 9-step Phase 11 roadmap*
