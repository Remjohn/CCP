# CCF Script Prompt Dependencies: The V3 Trigger-First Engine Inventory

**38 Dependencies mapped across WHAT · WHEN · WHY · WHERE · HOW**

*Cross-referenced: 4 Engine Docs × 15 CCF Skills × CBCS Intelligence Library × Extracted Lexicons & Orchestration Layers*

---

## Architecture Upgrade Note (V3 Shift)

> [!WARNING]
> This inventory has been purged of legacy V2 "Topic-First" and "Role-Play" components. Items like the `ttt_matrix`, `character_lexicon`, `facial_expression_lexicon`, and generic `persuasion_layers` have been deleted. They violate the CCP V3 architecture (Trigger-First Engine, CSIP v3.0, CCF Bible v2). The system now runs exclusively on Emotional DNA, Context Premise, and 3-Layer SPR.

## The Problem This Document Solves

Before rebuilding even one Script Prompt, we need a precise map of every upstream system, data structure, protocol, and library the prompts depend on. Removing the deprecated V2 ghosts leaves us with **38 distinct structural dependencies**.

---

## Category 1: Upstream Engine Outputs & Raw Data Assets (15 Items)

These are the dynamic structures produced per-project, per-theme, or per-week. They are the raw material that the Prompts consume.

### 1. The Structural Congruence Point
**WHAT:** The precise coordinate where the audience's current L3 pain and the coach's formative experience map to the same position. Contains `trigger_expression_angle` and `seed_esk_anchors`.
**WHEN:** Phase 3 (Pre-Generation). Injected as the absolute first content anchor.
**WHY:** Required for episodic memory (autonoetic) activation rather than topic semantic generation.
**WHERE:** Produced by Trigger Matching Layer limits. Currently in V3 (`disgusting-myth`).
**HOW:** Evaluates axes 1-4. The prompt constructs FROM this point outward.

### 2. Voice DNA SPR (3-Layer)
**WHAT:** The structural fingerprint of the coach. Layer 1: mechanics/epistemics. Layer 2: Emotional Path / Trigger-to-Expression pathway. Layer 3: Leadership Elevation traits.
**WHEN:** Phase 3 (Voice Injection).
**WHY:** Separates *WHAT* (beliefs) from *HOW* (syntax) and *PATH* (emotions).
**WHERE:** [coach_soul.json](file:///d:/Work/The%20Conscious%20Coaching%20Factory/CBCS/backend/intelligence_library/coach_soul.json) via `voice-dna-profiler`.
**HOW:** Root-down extraction from the coach's authentic baseline.

### 3. Emotional DNA
**WHAT:** The stable, individual sequence by which the coach moves from trigger to cognitive appraisal to linguistic expression. Contains 10 stable variables including suppression patterns and bleeding signature.
**WHEN:** Phase 3 (Pre-Generation).
**WHY:** Provides generative logic for *why* a coach builds a sentence a certain way.
**WHERE:** [emotional_dna.json](file:///d:/Work/The%20Conscious%20Coaching%20Factory/CBCS/backend/intelligence_library/emotional_dna.json).
**HOW:** Cognitive Appraisal Theory extraction.

### 4. Negative Space Object
**WHAT:** The explicit per-coach boundary condition: forbidden vocabulary, tones, rhetorical moves.
**WHEN:** Phase 3. Consulted BEFORE positive DNA is loaded.
**WHY:** A creative doctrine that only specifies what to produce is half a doctrine. Prevents identity breaking and hallucinated voice drift.
**WHERE:** `coach_soul.json -> negative_space`.
**HOW:** 5-word explicit logic bans ("No numbered list formats").

### 5. Authentication Certificate
**WHAT:** LIWC-22 gating scores validating the authentic baseline of Voice Notes. Evaluates Dual-layer activation flag.
**WHEN:** Phase 3.
**WHY:** If the fidelity is HIGH, the LLM must preserve Exact Transcripts. If it is LOW, abort generation.
**WHERE:** Stage 4 Trigger Engine.
**HOW:** 7-marker scoring (first-person singular, hesitations, hedging shifts).

### 6. Context Premise Summary
**WHAT:** Depth-stratified psychological profile of the audience (L1/L2/L3). Reveals Hidden Beliefs and Coping Mechanisms.
**WHEN:** Phase 1 (Intelligence).
**WHY:** The system must match the structural congruence point at L3 (hidden beliefs).
**WHERE:** `context_premise_map.json`.
**HOW:** Application of the 4 Laws of Audience Research.

### 7. Audience Tribal Terms
**WHAT:** The exact in-group vocabulary extracted from L3 Context. 
**WHEN:** Phase 3 (Generation).
**WHY:** Tribal language carries sub-cortical recognition signals. Professional translation kills the viral signal.
**WHERE:** `tribe_soul.json`.
**HOW:** Passes the "genericness test" via NLP.

### 8. Tribe Soul Profile
**WHAT:** The extended audience intelligence reference. Stores core fears/desires and the RTTR (Real-Time Tribe Relevance) velocity factors.
**WHEN:** Continuous updating via Sentinels.
**WHY:** Content must hit specific cultural zeitgeists to maximize distribution.
**WHERE:** `tribe_soul.json` (1,088 bytes).
**HOW:** Evaluated via continuous interaction.

### 9. Identity Pillars
**WHAT:** The 4 core pillars defining the coach/brand (e.g., "The Fluid Integrator", "The Grounded Processor"), including their Shadow Distortions.
**WHEN:** Setup Phase.
**WHY:** Keeps the scripts aligned with overarching brand architecture, so a coach doesn't randomly adopt a contrasting positioning.
**WHERE:** `identity_pillars.yaml` (1,802 bytes).
**HOW:** Read by the blueprint-orchestrator.

### 10. Stream of Consciousness Batch (SoC)
**WHAT:** Raw extracted 720-800 word coach responses with conversational metadata.
**WHEN:** Phase 2 (Raw Material).
**WHY:** Asking downstream agents to extract raw voice from syntheses of syntheses fails. The SoC is the unadulterated foundation of truth.
**WHERE:** `coach_soc_batch.md`.
**HOW:** Elicited by the Trigger-First prompts. 

### 11. Project Context
**WHAT:** Project-specific constraints defining pillar layers, archetype triggers, and campaign logic.
**WHEN:** Loaded during generation and planning.
**WHY:** Provides temporal/campaign boundaries.
**WHERE:** `project_context.json`.
**HOW:** Consumed by `dynamic-theme-generator` and `question-distiller`.

### 12. Intelligence Radar
**WHAT:** Sourced friction points, trending topics, and specific temporal hooks mapped from the wild.
**WHEN:** Weekly Phase.
**WHY:** Gives the content the "temporal hook" required to pass Conscious Movie Alchemy gating.
**WHERE:** `intelligence_radar.json`.
**HOW:** Processed alongside `coach_soc_batch.md` for Dynamic Theme Generation.

### 13. Provocation Questions
**WHAT:** The specific, tense, vulnerable layered questions built to shatter the coach's identity mask.
**WHEN:** Weekly Distillation Layer.
**WHY:** Ordinary interview questions yield ordinary semantic answers. Provocation yields episodic memory.
**WHERE:** `provocation_questions.json`.
**HOW:** Validated by the `question-distiller` via 4 Laws of Distillation.

### 14. Validated Content
**WHAT:** The completed, authorized textual script output that forms the payload for E-Roll Asset Planners and the Art Director.
**WHEN:** Epic 5 Validation Handoff.
**WHY:** E-Roll researchers and Visual Orchestrators cannot operate on abstract ideas; they require the validated text to ensure matching visuals.
**WHERE:** `validation/verdicts/`.
**HOW:** Consumed by distribution capabilities.

### 15. Script Prompt Schema Definitions
**WHAT:** The formalized architectural structure defining what a valid Script is.
**WHEN:** Phase 3 validation.
**WHY:** Prevents schema drift and structural breakdown across 74 dynamic prompts.
**WHERE:** `script_prompt_schema.json` (12,547 bytes).
**HOW:** Validated continuously.

---

## Category 2: Component Library & Constraints (7 Items)

These libraries provide the root logic and structural format data for content rendering, now stripped of all legacy role-play artifacts.

### 16. Coach Soul (Unified Identity Kernel)
**WHAT:** The complete aggregation of `conscious_soul_values`, `voice_dna`, and `negative_space`.
**WHEN:** Setup / Base Layer.
**WHY:** Centralized truth prevents fragmentation.
**WHERE:** [coach_soul.json](file:///d:/Work/The%20Conscious%20Coaching%20Factory/CBCS/backend/intelligence_library/coach_soul.json) (14,740 bytes).
**HOW:** Consumed globally.

### 17. Trigger Map
**WHAT:** 5-7 primary triggers explicitly mapping Coach Pain to Audience Coping Patterns.
**WHEN:** Setup / Weekly sweep.
**WHY:** Enables the Intelligence radar to be predictive, rather than simply reactive.
**WHERE:** [trigger_map.json](file:///d:/Work/The%20Conscious%20Coaching%20Factory/CBCS/backend/intelligence_library/trigger_map.json) (6,896 bytes).
**HOW:** Extracted via MFQ-2 and Cognitive Appraisal formulas.

### 18. Story Formulas
**WHAT:** Causal structural sequences that govern logical flow without imposing fake personas.
**WHEN:** Phase 3.
**WHY:** Bible Critique Mandate 6: Replaces useless outline chunks with causal generation workflows.
**WHERE:** `story_formulas.yaml` (28,084 bytes).
**HOW:** Orchestrates hook/promise/resolve tensions.

### 19. Persuasive Angles
**WHAT:** The psychology layer defining 9 distinct rhetorical mechanisms (Throw Rocks at Enemies, Confirm Suspicions, etc.).
**WHEN:** Phase 3.
**WHY:** Controls the cognitive operation the LLM executes, replacing generic "be persuasive" prompts.
**WHERE:** `persuasive_angles.json` (8,895 bytes).
**HOW:** Substituted into generation templates.

### 20. Cognitive Distortion Definitions
**WHAT:** Taxonomy of distortions (catastrophizing, emotional reasoning) trapped inside audience L3 data.
**WHEN:** Phase 3 (Generation).
**WHY:** Naming the distortion specifically gives the content clinical precision and immense epistemic trust.
**WHERE:** `cognitive_distortion_definitions.yaml` (14,782 bytes).
**HOW:** Filtered via L3 analysis.

### 21. Identity Threat Taxonomy
**WHAT:** Classification of specific threats (competence, belonging, status, moral).
**WHEN:** Phase 2 (Trigger Match).
**WHY:** Ensures the content properly resolves the precise nature of the existential anxiety.
**WHERE:** `identity_threat_taxonomy.yaml` (13,066 bytes).
**HOW:** Matches trigger architecture to audience state.

### 22. SDT Markers (Self-Determination Theory)
**WHAT:** Markers tracking Autonomy, Competence, and Relatedness phrasing.
**WHEN:** Phase 3 (Completion criteria).
**WHY:** An audience needing competence given a belonging message won't convert. Ensures psychological need alignment.
**WHERE:** `sdt_markers.yaml` (7,214 bytes).
**HOW:** Completion requirement checking.

---

## Category 3: Sacred Protocols & Quality Gates (10 Items)

These are the operational laws and cognitive frameworks that prevent drift, enforce depth, and validate the output.

### 23. Research Synthesis Protocol (Deep/Fresh)
**WHAT:** Dual layer strategy: DEEP (investigative studies/authorities) and FRESH (current vibe bait/temporal hooks).
**WHEN:** Phase 2 (Research).
**WHY:** Prevents generic topic overviews, forcing mechanisms instead of opinions.
**WHERE:** Implemented via Analysts & `raw-deep/fresh` skills.
**HOW:** 7-angle analysis tagging mode + depth.

### 24. Authenticity Protocol (Soul-Alignment)
**WHAT:** Ensures the generated content strictly echoes the underlying values, metaphors, and worldview in `coach_soul`.
**WHEN:** Phase 3.
**WHY:** Baseline guarantee that opinions reflect actual coach stances.
**WHERE:** Woven as constraint logic.
**HOW:** Replaces loose Role-Play prompts.

### 25. Memetic Protocol
**WHAT:** The 4 pillars of virality: Immediate Comprehension, High-Arousal, Tribal Signal, Inherent Shareability.
**WHEN:** Phase 3 (Distribution content only).
**WHY:** Relegated exclusively to output content, avoiding corruption of upstream raw extraction formats.
**WHERE:** Embedded in generation templates.
**HOW:** Post-generation scoring mechanics.

### 26. Conscious Movie Alchemy
**WHAT:** 6-point evaluation matrix including Relevance, Emotional Depth, Specificity Paradox, and Shareability triggers.
**WHEN:** Phase 2 Theme Validation.
**WHY:** Reject generic themes before computationally expensive research phases run. 
**WHERE:** `dynamic-theme-generator`.
**HOW:** Threshold scoring (requires ≥ 5/6).

### 27. Late Binding Protocol
**WHAT:** The architectural separation isolating Structural Generation from Voice Injection.
**WHEN:** Governs macro pipeline sequence.
**WHY:** Prevents archetype performance regression and premature aesthetic corruption.
**WHERE:** System orchestration routing limits.
**HOW:** Loading SPR constraints exclusively in late-stage node flows.

### 28. Smart Mix Synthesis Protocol
**WHAT:** Translates validated scripts into 5 cross-platform Persona variations (Generational, Humor, Dramatic, Wildcard, Core) and intelligently fuses the best hooks/cores/outros.
**WHEN:** Phase 5 Distribution.
**WHY:** Avoids monotonic marketing by slicing content through distinct persona lenses, ultimately assembling a hyper-optimized script.
**WHERE:** `smart-mix/SKILL.md`.
**HOW:** Analyzes component strength and builds a final polished entity.

### 29. PRIMAL Felt Specificity Gate
**WHAT:** 6-factor visual reality gate ensuring explicit Physical Reality, Spatial relations, Implicit History, and Lighting psychology.
**WHEN:** Art Director Pre-Composition Check.
**WHY:** Prevents "stock image sludge". Image must feel intensely populated.
**WHERE:** `art-director/SKILL.md`.
**HOW:** Reject "She looks confused"; Demand "Hands gripping the counter, pausing mid-motion."

### 30. Visual Authenticity Gate
**WHAT:** 4-check system enforcing Universal Illustration, Brand Avatar correlation, Mapping, and Self-Recognition.
**WHEN:** Visual Architecture validation.
**WHY:** Validates that generated imagery reflects the exact moral/emotional foundation specified in `context_premise`.
**WHERE:** `art-director/SKILL.md`.
**HOW:** Binary checklists evaluated over produced outputs.

### 31. AIP 5-Lens Protocol (Vibe-Comments)
**WHAT:** Elaborate 5-stage comment processing (Specificity, Vulnerability, Constraint, Output, Integration) that breaks through conversational surface noise.
**WHEN:** Intelligence gathering phase.
**WHY:** Derives the "Prediction Error" required to create content that feels inexplicably telepathic to an audience.
**WHERE:** `vibe-comments/SKILL.md`.
**HOW:** Progressive adversarial refinement against confirmation bias.

### 32. I-R-E-V-C Session Protocol
**WHAT:** The universal `Ingest -> Reason -> Emit -> Validate -> Checkpoint` state-machine format required of every CCF Agent.
**WHEN:** Omnipresent across all skills.
**WHY:** Secures traceability, idempotent checkpointing, and clear accountability boundaries per Phase.
**WHERE:** Exists in every modern V3 Markdown Skill outline.
**HOW:** Rigid header sequence guiding execution.

## Category 4: V2WS Extrapolation Libraries (The Multimodal Physics) (6 Items)

The Conscious V2WS (Voice2WebinarSystem) operates on a "Reaction Paradigm" rather than a "Presentation Paradigm." The coach reacts to a pre-produced Stimulus Video. This requires a distinct set of multimodal intelligence files that govern timing, branding, and visual physics.

### 33. TTT System v3.0 (Visual & Timing Physics)
**WHAT:** The master definition of the 9 Temperament Levels expanded for multimodal control (cut velocity, transition topology, meme density, text overlay aggression).
**WHEN:** Phase 1 (Intelligence) and Phase 4 (Visual Production).
**WHY:** A TTT-09 "Truth Bomb" script cannot be paired with slow video cuts. This file forces the visual layer and script layer to dance to the same psychological beat.
**WHERE:** `ttt_system_v3.json`
**HOW:** The Script Architect writes staccato sentences when it reads TTT-07; the Cutter trims silence to 0.2s.

### 34. Brand DNA System (Functional Color Mapping)
**WHAT:** Translates aesthetic hex codes into neuro-linguistic functions (SIGNAL for action, STRUCTURE for safety, CANVAS for clarity).
**WHEN:** Phase 3 (Asset Generation) and Phase 4 (Assembly).
**WHY:** Prevents "Over-Branding." Hex codes are mapped to specific instructions so the automation knows *how* to use the color, not just *what* it is.
**WHERE:** `brand_DNA.json`
**HOW:** The Visual Director uses it to "Brand-Wash" generative image prompts (e.g., "A woman in a Slate-Grey jacket").

### 35. Reaction Timing Framework
**WHAT:** The temporal physics governing "Air Gaps" — how long the Stimulus Video must play before a pause, and the duration/type of pause based on TTT.
**WHEN:** Phase 3 (Scripting) and Phase 5 (Delivery).
**WHY:** In a Reaction Webinar, time is rigid. The Air Gaps must be pre-calculated so the Coach never talks over the video or suffers awkward silence.
**WHERE:** `reaction_timing_framework.yaml`
**HOW:** The Script Architect calculates Track A (Stimulus) and Track B (Reaction) intersections based on these temporal rules.

### 36. V2WS 72-Slide Modular Architecture
**WHAT:** The immutable spine of the webinar: Intro (Slides 1-12), Content (13-48), Transition (49-56), Close (57-72). Contains exact asset counts (12 Hooks, 6 Memes).
**WHEN:** Phase 3 (Scripting).
**WHY:** Prevents structural drift. Industrializes the creation of the asset by treating it as a proven formula rather than a blank canvas.
**WHERE:** `framework_72_slides.yaml` and Sub-Prompts (e.g., `INTRO-001_HOOK`).
**HOW:** The Script Architect is constrained to generating content only within this specific container logic.

### 37. Slide Design Physics
**WHAT:** The geometric laws of the visual presentation (e.g., "Maximum 12 words per slide," "Minimum 30% whitespace").
**WHEN:** Phase 4 (Assembly)
**WHY:** Prevents "Cognitive Drift." Slides that require reading distract from listening to the Coach's reaction.
**WHERE:** `slide_design_physics.yaml`
**HOW:** Evaluated by `visual_density_check.py` to reject non-compliant text overlays.

### 38. Humor Theory Selector (Meme Orchestrator)
**WHAT:** Rules mapping the 6 fixed meme slots to specific linguistic humor theories (Superiority, Relief, Incongruity, Benign Violation) based on the webinar's Reaction Archetype.
**WHEN:** Phase 2 (Asset Generation).
**WHY:** Selecting random memes breaks the tonal architecture. A "Vindication" webinar requires Superiority memes; an "Empathy" webinar requires Relief memes.
**WHERE:** `meme_orchestrator.yaml`
**HOW:** Controls the generation pipeline for the 6 visual meme assets.

---

## Cross-System Status Summary

| # | Dependency Category | Key Missing Artifacts / Status |
|:--|:-----------|:------------|
| 1 | **Data Dependencies (Engine Outputs)** | All 15 natively support V3 Trigger-First architecture. |
| 2 | **Component Library & Constraints** | Distilled down to 7 core files. Legacy role-play files purged. |
| 3 | **Protocols & Gates** | All 10 Gates enforce Negative Space and Trigger ceilings (no ghost variables anymore). |
| 4 | **V2WS Multimodal Physics** | The 6 multimodal files remain structurally solid for reaction paradigms. |

> [!CAUTION]
> **The structural count is now a lean 38 dependencies.** By purging the 7 outdated CBCS files (`ttt_matrix`, lexicons, etc.), we eliminate the "ghost variables" that were causing downstream LLM hallucinations. Prompts will now strictly construct from Emotional DNA and Context Premises.
