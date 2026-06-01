# Tech-Spec: FR-ERA3-16 (Living Commentary Update) — Archetype Container Runtime for Living Commentary Bundles
**Created:** 2026-05-24
**Status:** DRAFT
**Version:** 3.0 (ERA3 — Living Commentary Bundle Integration)
**Phase:** 7 — Living Commentary & Coach Communication Stack
**Source PRD:** PRD-02 (CCF Content Factory), PRD-06 (Conscious Reactions)
**Architecture Reference:** `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
**Base Spec:** `docs/architecture/april_updates/FR-ERA3-16_Archetype_Container_Runtime_Tech_Spec.md` v1.0
**Supersedes:** FR-ERA3-16 v1.0 (base), FR-ERA3-16 v2.0 (SFL update)
**Absorbs:** FR-ERA3-62 (Living Commentary Archetype Mapping And Output Bundles — NOT written as standalone; folded here)

> [!IMPORTANT]
> This spec is an **UPDATE** to the existing Archetype Container Runtime. The doctrine is: **keep the archetypes, change the realization grammar.** This spec does NOT create new archetypes. It adds delivery recipe resolution and Living Commentary output bundle routing to existing archetype containers.
>
> Hard rule: do NOT create a new archetype ontology.

> [!IMPORTANT]
> **RENDERING BACKEND PIVOT:** All downstream visual composition is rendered via **Remotion Node.js + `@remotion/skia`** (CanvasKit WebAssembly). The archetype container routing must output directly into the **Complete Editing Session** state wrapper. The weekly package template must align chronologically with the Trigger-First execution sequence (Carousel → 3 Voice Notes → Record) so that no visual assets or research context is lost.

---

## Pre-Work Log

```text
1. PROTOCOL LOADED:   ERA3_Tech_Spec_Writing_Protocol.md. 10-section format, CBAR mandate enforcement, 
                      existing backend integration, min 320 lines. Pre-work log with verbatim quotes required.

2. PRD-02 LOADED:     docs/prd/modules/PRD_02_CCF_Content_Factory.md. Exact runtime law: 
                      "Elevate Archetypes (e.g., Achievement Story, Myth Debunk, Observational Humor) into 
                      first-class runtime containers. The compiler must structure the meaning into these 
                      archetypes *before* any downstream media format (carousel, video) is selected."
                      Archetype routing = L6: "Routing and Formatting — Select the right content archetype, 
                      format family, and delivery role."
                      CCF as compiler: "CCF is not the final media renderer. It emits content source 
                      artifacts that downstream systems can transform."

3. PRD-06 LOADED:     docs/prd/modules/PRD_06_Conscious_Reactions.md. Orchestration handoff: "Every 
                      successful Conscious Reaction is automatically routed to the CCF pipeline. The system 
                      applies the Edge Extraction protocols (defined in PRD-02) to identify the most potent 
                      15-second 'hook' within the 2-minute reaction."

4. BLUEPRINTS LOADED: HANDOVER_CONSOLIDATION_BLUEPRINTS.md. Complete Editing Session: "every lesson 
                      initiates a stateful 'Editing Session' wrapper. This holds all CRAL research, VIE 
                      assets, and transcripts in one payload." Remotion mandate: "A centralized Node.js 
                      Remotion server consumes the depth-aware layers."

5. AUDIT LOADED:      Architectural_Audit_Trigger_First_Vision_Visual_Engines.md. Remotion mandate: "The 
                      standalone C++/Python Skia sidecar is formally deprecated. The engine must be 
                      centralized into a Remotion Node.js server utilizing @remotion/skia."

6. SOURCE LOADED:     Living_Commentary_Realization_Layer_Source_of_Truth.md. MCDA ranked archetype table 
                      (§9.2): Comparison Breakdown (193), Challenger/Frame Breaker (191), Myth Debunk (188), 
                      Authority Proof Stack (186), Wrong Way/Right Way (184), Relief Peak (182), Persuasive 
                      Tweets (181), Ranked Take (179), Core Educator (176), Observational Humor (174), 
                      Transformation Story (171), Case Study Breakdown (168), Witness Story (165).
                      Weekly package logic (§10): "1 cinematic story + 2 animated explainers + 2 quote 
                      commentary + 1 comparison/reaction + 1 atmospheric = 7 pieces from one 45-60 min 
                      interview." Commercial ladder: $29.99 = 7 videos, $39.99 = program access, $99.99 = 
                      program + 32 videos. Core law: "the package is not multiple random posts. It is 
                      multiple realizations of the same underlying source truth."
                      Per-archetype delivery behavior (§7.4): Challenger = "intrigue + authority + objection 
                      softening + reframe → sharper contrast, faster reveal, stronger first-frame tension."
                      Authority Proof Stack = "authority + proof + identification + future trust → real-world 
                      receipts, stable camera, less decorative motion."
                      Witness Story = "identification + story + permission to be seen + hope → slower drift, 
                      softer audio, wider space, fewer text interruptions."
                      Comparison Breakdown = "positioning + contrast + decision guidance + 
                      close-through-clarity → binary composition, object separation, check/cross coding."

7. ROADMAP LOADED:    Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md. W2 execution loop: 
                      "45-60 minute interview → source truth extraction → archetype routing → weekly package 
                      assembly → review → deployment."

8. FR-ERA3-16 v1 LOADED: Original 780-line spec. ArchetypeContainerRuntimeService.compile() accepts 
                      CoachResponseCapturePacket + CoalitionInputs + mood_context + evidence_bundle. Returns 
                      CCFRoutingRecommendation with ArchetypeContainerManifest or ActionableRejectionPayload. 
                      6 archetype choices: ARC-MYTH-DEBUNK, ARC-ACH-STORY, ARC-OBS-HUMOR, ARC-WITNESS, 
                      ARC-CONTRAST, ARC-COMP.

9. FR-ERA3-16 v2 LOADED: SFL update 674-line spec. Added SubliminalFunctionStackPacket, 
                      CompositionDepthPacket, VariationProfileBinding, ArchetypeSflExecutionContract, 
                      ArchetypeVariationDecision. SflBindingStatus enum. Backward compatible.

10. FR-ERA3-35B LOADED: Content Benchmark Profiles spec. Canonical 7 visible score vocabulary: Humanity, 
                      Presence, Trust, Memorability, Resonance, Signal, AI Slop Risk. Archetype score 
                      bundles keyed by ArchetypeChoice × ContentType. Score deltas within [-0.3, +0.3].

11. FR-ERA3-35C LOADED: Eval Card System spec. EvalCard, EvalCardBoard, EvalBoardLayout. Cards carry 
                      overall score, visible stats, verdict block. Boards support layouts: single_card_detail, 
                      audit_spread, before_after_comparison, shareable_summary.

12. FR-ERA3-12 v3 LOADED: CMF Arc-Governed Rendering Living Commentary spec. 6 format families: Quote, 
                      Comparison, Screenshot, Atmospheric, Cinematic Story, Animated Explainer. 7-layer 
                      composition model. MotionGrammarProfile, SoundCueTimeline, LivingStillCompositionSpec, 
                      FormatFamilyRenderConfig, RemotionRenderPayload, CompleteEditingSessionRef.

13. BACKEND LOADED:   src/ccp/services/archetype_container_runtime.py — 
                      ArchetypeContainerRuntimeService.__init__(supabase_client, receipt_chain, 
                      research_synthesis, psych_routing). compile(capture, coalition, mood_context, 
                      evidence_bundle, sfl_function_stack, composition_depth, variation_profile) -> 
                      CCFRoutingRecommendation. ArchetypeSelectionMatrix.select(coalition, mood_context) -> 
                      ArchetypeChoice. AntiCentroidValidator.validate(sentences) -> list[SentenceAuditRecord].

14. MODELS LOADED:    src/ccp/models/archetype_container_runtime_models.py — RuntimeStatus, SimilarityBand, 
                      ArchetypeChoice (6 values), SentenceAuditRecord, CoalitionInputs, 
                      CoachResponseCapturePacket, ContainerIntensityProfile, ArchetypeContainerManifest, 
                      ActionableRejectionPayload, CCFRoutingRecommendation, SflBindingStatus, 
                      CompositionDepthClass, SflFunctionBinding, SubliminalFunctionStackPacket, 
                      CompositionDepthPacket, VariationProfileBinding, ArchetypeVariationDecision, 
                      ArchetypeSflExecutionContract.

15. TESTS LOADED:     test_frera316_archetype_runtime_compile.py — TestAC1SuccessfulContainerization, 
                      TestAC4EvidenceConflictBlock. test_frera316_actionable_rejection_loop.py — 
                      TestAC2ActionableRejection, TestAC3TriggerGuardReroute. 
                      test_frera316_sfl_integration.py — SFL crosswalk, manual binding, compile.

16. BENCHMARK MODELS: src/ccp/models/benchmark_profile_models.py — ContentType, CardRole, 
                      VisibleScoreKey, VisibleScoreWeightMap, PenaltyAdjustmentMap, ArchetypeScoreBundle, 
                      CardWeightingBundle, OverallScoreComputation.
                      src/ccp/models/phase0_eval_card_models.py — EvalCardFace, EvalCard, EvalCardBoard, 
                      EvalBoardLayout, CardVerdictBlock, CardThemeProjection.
```

---

## 1. Files Read

| # | File | Purpose |
|---|------|---------|
| 1 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory spec format, CBAR mandate enforcement |
| 2 | `docs/prd/modules/PRD_02_CCF_Content_Factory.md` | Archetype routing doctrine, compiler law, meaning/experience plane separation |
| 3 | `docs/prd/modules/PRD_06_Conscious_Reactions.md` | Orchestration handoff, Edge Extraction, self-translation principle |
| 4 | `docs/architecture/HANDOVER_CONSOLIDATION_BLUEPRINTS.md` | Complete Editing Session wrapper, Remotion mandate, synthetic voice ban |
| 5 | `docs/architecture/May 2026 UPDATES/Architectural_Audit_Trigger_First_Vision_Visual_Engines.md` | Remotion centralization, VIE reversal, hybrid pipeline |
| 6 | `lab/CCP APRIL Updates/05_Core_Experience/Living_Commentary_Realization_Layer_Source_of_Truth.md` | MCDA archetype ranking, weekly package logic, per-archetype delivery recipes, commercial ladder |
| 7 | `lab/CCP APRIL Updates/01_Architecture_PRDs/Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md` | W2 execution loop, workflow inventory, spec consolidation map |
| 8 | `docs/architecture/april_updates/FR-ERA3-16_Archetype_Container_Runtime_Tech_Spec.md` | Base v1.0 runtime — compile, reject, select, route |
| 9 | `docs/architecture/april_updates/FR-ERA3-16_Archetype_Container_Runtime_Tech_Spec_UPDATED_FOR_SFL.md` | v2.0 SFL update — function stack, composition depth, variation binding |
| 10 | `docs/architecture/april_updates/FR-ERA3-35B_Content_Benchmark_Profiles_And_Card_Weighting_Bundles_Tech_Spec.md` | Score vocabulary, archetype score bundles, benchmark resolution chain |
| 11 | `docs/architecture/april_updates/FR-ERA3-35C_Eval_Card_System_And_Shareable_Audit_Board_Tech_Spec.md` | Eval card faces, board layouts, verdict blocks |
| 12 | `docs/architecture/april_updates/FR-ERA3-12_CMF_Arc_Governed_Rendering_Tech_Spec_UPDATED_FOR_LIVING_COMMENTARY.md` | FR-ERA3-12 v3.0 — Living Commentary render configs, format families, Remotion manifest |
| 13 | `src/ccp/services/archetype_container_runtime.py` | Existing compile, select, validate implementation |
| 14 | `src/ccp/models/archetype_container_runtime_models.py` | Existing Pydantic models including SFL extensions |
| 15 | `src/ccp/api/archetype_runtime.py` | Existing FastAPI routes: compile, inspect, rerecord |
| 16 | `src/ccp/models/benchmark_profile_models.py` | Scoring models, archetype score bundles |
| 17 | `src/ccp/models/phase0_eval_card_models.py` | Eval card face, board, and layout models |
| 18 | `src/ccp/services/format_governance_engine.py` | FormatGovernanceEngine.apply_format_governance(), compute_weekly_allocation() |
| 19 | `tests/integration/test_frera316_archetype_runtime_compile.py` | Existing compile test patterns |
| 20 | `tests/integration/test_frera316_actionable_rejection_loop.py` | Existing rejection test patterns |
| 21 | `tests/integration/test_frera316_sfl_integration.py` | Existing SFL integration test patterns |

---

## 2. Overview

### 2.1 Problem Statement

FR-ERA3-16 v1.0 established the archetype container runtime with six deterministic jobs: validate, evidence-check, anti-centroid, reject, select, and route. FR-ERA3-16 v2.0 added SFL consumption (function stacks, composition depth, variation profiles). Both versions are correct and remain the structural foundation.

However, the archetype container runtime does not yet know about **Living Commentary** — the realization layer that transforms compiled archetype containers into premium weekly video packages. Without this update:

1. **No delivery recipe resolution** — the runtime selects an archetype (`ARC-MYTH-DEBUNK`, `ARC-CONTRAST`, etc.) but cannot tell downstream systems which communication modules dominate, what order they appear in, what emotional temperature they carry, or which Living Commentary format family best realizes the archetype.

2. **No weekly package template** — the system has no canonical definition of how a single 45-60 minute interview yields 7 distinct video pieces (1 cinematic story + 2 animated explainers + 2 quote commentary + 1 comparison/reaction + 1 atmospheric).

3. **No MCDA-ranked deployment order** — all 13 archetypes are treated equally. The MCDA analysis proves that Comparison Breakdown (193), Challenger (191), and Myth Debunk (188) gain disproportionately more from living realization than Witness Story (165) or Case Study Breakdown (168). The runtime should know this.

4. **No archetype-to-format-family mapping** — the runtime emits `authorized_render_targets` as generic strings (`"short_form_video"`, `"carousel"`) but cannot specify which Living Commentary format families the archetype prefers.

5. **No commercial ladder integration** — the $29.99 / $39.99 / $99.99 tiers depend on weekly package composition, but the runtime has no pricing tier awareness in its bundle output.

### 2.2 Solution

This update spec extends the existing `ArchetypeContainerRuntimeService` and `ArchetypeContainerManifest` with four new capabilities:

1. **`ArchetypeDeliveryRecipe`** — defines which communication modules dominate a given archetype, what order they appear in, what emotional temperature they carry, and what realization layer best fits. Each archetype gets a typed recipe, not a prose description.

2. **`WeeklyPackageTemplate`** — the canonical definition of a weekly video package: how many pieces, which format families, which archetypes dominate which slots, and which commercial tier the package satisfies.

3. **`ArchetypeToLivingCommentaryMapping`** — routes archetype containers to their preferred Living Commentary format families, with MCDA-ranked priority ordering.

4. **`ArchetypeDeliveryRecipeCompiler`** — resolves which recipe applies to a given archetype + coalition + interview context, compiles the delivery recipe into a structured output, and emits a `LivingCommentaryBundleManifest` that downstream systems (FR-ERA3-12 CMF, Remotion) can consume.

The archetype container remains a structural container, not a style blob. Delivery recipes are resolved *after* archetype selection succeeds — they are a downstream enrichment, not a selection input.

### 2.3 Scope

**In scope:**

- New Pydantic models for delivery recipes, weekly package templates, archetype-to-LC mappings, and bundle manifests
- Extension of `ArchetypeContainerManifest` with delivery recipe and bundle fields
- Extension of `ArchetypeContainerRuntimeService.compile()` to resolve delivery recipes post-selection
- `ArchetypeDeliveryRecipeCompiler` as a new sub-service within the runtime
- MCDA-ranked archetype mapping with all 13 archetypes and their scores
- Weekly package template definition with commercial tier alignment
- Per-archetype delivery recipe behavior (module order, emotional temperature, motion hints, format family preferences)
- Complete Editing Session reference in bundle manifests
- Supabase persistence for delivery recipes and bundle manifests
- Updated acceptance criteria and test coverage

**Out of scope:**

- Rewriting the base anti-centroid, evidence-gate, or selection-matrix logic (FR-ERA3-16 v1.0)
- Rewriting the SFL consumption logic (FR-ERA3-16 v2.0)
- Implementing the CMF Living Commentary rendering itself (FR-ERA3-12 v3.0)
- Implementing the Remotion Node.js server (infra)
- Creating new archetype types — the 6 `ArchetypeChoice` values remain unchanged
- Voice prompt engine changes (FR-ERA3-17)
- VIE asset generation (upstream)

---

## 3. Context for Development

### 3.1 Architecture Traceability (DEP-IDs)

Existing DEP-ACR-001 through DEP-ACR-012 from v1.0 and v2.0 remain unchanged.

| DEP-ID | Payload / Data Object | Source | Responsibility |
|---|---|---|---|
| DEP-ACR-013 | `ArchetypeDeliveryRecipe` | FR-ERA3-16 v3 | Per-archetype communication module sequence, emotional temperature, and realization preferences |
| DEP-ACR-014 | `WeeklyPackageTemplate` | FR-ERA3-16 v3 | Canonical 7-piece weekly package definition with format family assignments |
| DEP-ACR-015 | `ArchetypeToLivingCommentaryMapping` | FR-ERA3-16 v3 | MCDA-ranked mapping of archetypes to preferred LC format families |
| DEP-ACR-016 | `LivingCommentaryBundleManifest` | FR-ERA3-16 v3 | Compiled bundle output for a single archetype container, ready for CMF consumption |
| DEP-ACR-017 | `WeeklyPackageSlot` | FR-ERA3-16 v3 | Individual slot within a weekly package (format family + archetype + recipe reference) |
| DEP-ACR-018 | `CommercialTierAlignment` | FR-ERA3-16 v3 | Pricing tier metadata attached to bundle output |
| DEP-ACR-019 | `DeliveryRecipeStep` | FR-ERA3-16 v3 | Individual step within a delivery recipe (module + weight + order) |

### 3.2 Existing Backend Integration (≥4 files)

| File | Path | How This Update Uses It |
|---|---|---|
| `archetype_container_runtime.py` | `src/ccp/services/archetype_container_runtime.py` | **EXTENDS** with `ArchetypeDeliveryRecipeCompiler` sub-service. After successful compile, `compile()` now resolves the delivery recipe and emits a `LivingCommentaryBundleManifest` on the manifest. New method: `resolve_delivery_recipe(archetype: ArchetypeChoice, coalition: CoalitionInputs, editing_session_id: str | None) -> ArchetypeDeliveryRecipe`. New method: `compile_bundle_manifest(manifest: ArchetypeContainerManifest, recipe: ArchetypeDeliveryRecipe) -> LivingCommentaryBundleManifest`. |
| `archetype_container_runtime_models.py` | `src/ccp/models/archetype_container_runtime_models.py` | **EXTENDS** with new models: `ArchetypeDeliveryRecipe`, `DeliveryRecipeStep`, `WeeklyPackageTemplate`, `WeeklyPackageSlot`, `ArchetypeToLivingCommentaryMapping`, `LivingCommentaryBundleManifest`, `CommercialTierAlignment`, `MCDAArchetypeRanking`, `ArchetypeMCDAEntry`, `DeliveryRecipeBindingStatus`. Existing `ArchetypeContainerManifest` gains `delivery_recipe`, `bundle_manifest`, and `delivery_recipe_binding_status` optional fields. Existing `CCFRoutingRecommendation` gains `delivery_recipe_binding_status` field. |
| `format_governance_engine.py` | `src/ccp/services/format_governance_engine.py` | **CONSUMES** `FormatGovernanceEngine.compute_weekly_allocation()` to validate that weekly package template slot counts align with the 36-format weekly governance budget. `apply_format_governance()` is consulted to verify that the recipe's format family preferences are within governance constraints. |
| `benchmark_profile_models.py` | `src/ccp/models/benchmark_profile_models.py` | **READS** `ArchetypeScoreBundle` to cross-reference MCDA rankings with benchmark score emphasis — ensuring that archetypes ranked higher by MCDA also receive scoring emphasis aligned with their Living Commentary realization strengths. |
| `phase0_eval_card_models.py` | `src/ccp/models/phase0_eval_card_models.py` | **READS** `EvalCardFace` and `EvalCardBoard` — bundle manifests include a `benchmark_eval_hint` field that suggests which eval card layout is appropriate for the bundle's archetype + format family combination. |
| `receipt_chain.py` | `src/ccp/core/receipt_chain.py` | **CONSUMES** `ReceiptChain.log()` for delivery recipe resolution, bundle manifest compilation, and weekly package slot assignment events. |
| `main.py` | `src/ccp/api/main.py` | **EXTENDS** with new Living Commentary bundle routes. |
| `setup_supabase.py` | `src/ccp/scripts/setup_supabase.py` | **EXTENDS** with new tables: `archetype_delivery_recipes`, `weekly_package_templates`, `lc_bundle_manifests`. |

### 3.3 Delivery Recipe Contracts

The archetype runtime now supports two output paths that share the same compile pipeline but diverge after archetype selection:

```
PATH A — Standard Archetype Output (existing v1.0 + v2.0):
  compile → validate → evidence-check → anti-centroid → select → manifest
  → CCFRoutingRecommendation (with SFL binding if available)

PATH B — Living Commentary Bundle Output (new v3.0):
  compile → validate → evidence-check → anti-centroid → select → manifest
  → ArchetypeDeliveryRecipeCompiler (NEW)
    → resolve_delivery_recipe() — maps archetype to recipe
    → resolve_format_family_preferences() — MCDA-ranked LC format mapping
    → compile_bundle_manifest() — assembles LivingCommentaryBundleManifest
  → CCFRoutingRecommendation (enriched with bundle manifest + recipe)
```

Path B activates when the compile request includes an `editing_session_id` (indicating the Complete Editing Session context is available) OR when the caller explicitly requests bundle resolution via `resolve_living_commentary_bundle=True`.

**MCDA-Ranked Archetype Table** (governs delivery recipe priority ordering):

| Rank | Archetype | MCDA Score / 200 | Living Commentary Benefit |
|---|---|---:|---|
| 1 | Comparison Breakdown | 193 | Contrast, verdict, and coach judgment intensify under living realization |
| 2 | Challenger / Frame Breaker | 191 | Strong for conviction, reframe energy, live-feeling authority |
| 3 | Myth Debunk | 188 | Screenshot, quote, line-by-line dismantling become stronger with commentary timing |
| 4 | Authority Proof Stack | 186 | Proof lands harder when interpreted live through receipts rather than static claims |
| 5 | Wrong Way / Right Way Contrast | 184 | Binary decision logic, objection correction, clear framing fit the layer well |
| 6 | Relief Peak | 182 | Physiological exhale and validation turn become stronger with subtle motion, sound, presence |
| 7 | Persuasive Tweets | 181 | Quote-sized truths become more premium when converted from static persuasion into living interpretation |
| 8 | Ranked Take / Ranked Claims | 179 | Strong for progressive reveal, selective emphasis, guided judgment |
| 9 | Core Educator / Explainer | 176 | Better when shifted from dead slides into voice-led minimal-motion explanation |
| 10 | Observational Humor | 174 | Timing, familiar sound cues, ambient realism make it more alive than static memes |
| 11 | Transformation Story | 171 | Strong if pacing is restrained and emotional turn given enough room |
| 12 | Case Study Breakdown | 168 | Gains authority and clarity but sometimes benefits from denser proof surfaces |
| 13 | Witness Story | 165 | Works well but demands authenticity discipline and careful editing restraint |

**Per-Archetype Delivery Recipe Behavior** (from Source of Truth §7.4):

| Archetype | Module Sequence | Realization Hints |
|---|---|---|
| **Challenger / Frame Breaker** | intrigue → authority → objection softening → reframe | Sharper contrast, faster reveal, stronger first-frame tension |
| **Authority Proof Stack** | authority → proof → identification → future trust | Real-world receipts, stable camera, less decorative motion |
| **Witness Story** | identification → story → permission to be seen → hope | Slower drift, softer audio, wider space, fewer text interruptions |
| **Comparison Breakdown** | positioning → contrast → decision guidance → close-through-clarity | Binary composition, object separation, check/cross coding |
| **Myth Debunk** | named false belief → persistence reason → coach proof → reframe | Screenshot-first, quote reveal, line-by-line annotation |
| **Relief Peak** | tension build → validation turn → exhale → hope | Subtle motion, warm atmosphere, minimal text, wide framing |
| **Persuasive Tweets** | quote reveal → interpretation → authority claim → close | Quote-card dominant, living still, Rough Notation highlight |

### 3.4 Governance Constraints

**Preserved from v1.0 + v2.0:**
- `Actionable Rejection Rule` — rejections include sentence-level evidence, similarity scores, coaching fixes
- `Anti-Centroid Collapse Rule` — terminal similarity ≥ 0.75 blocks compilation
- `Evidence-Before-Selection Rule` — evidence conflicts block before archetype selection
- `SFL Subordinate-to-SDA Rule` — SFL delivery packets do not override truth decisions
- `No-Flat-120 Rule` — function stacks use canonical SFL-FN-* IDs

**New Living Commentary Governance:**
- `No-New-Archetype-Ontology Rule` — the 6 `ArchetypeChoice` values are fixed. Delivery recipes describe *how* archetypes are realized, not *what* archetypes exist. No spec or implementation may add new `ArchetypeChoice` enum values without a formal ontology change proposal.
- `Archetype-Realization Separation Rule` — archetype selection is a structural/meaning decision. Delivery recipe resolution is a realization/format decision. They are sequential, not interleaved. A delivery recipe cannot override archetype selection.
- `Delivery-Recipe-Per-Archetype Rule` — every archetype MUST have a canonical delivery recipe. A compiled container without a delivery recipe is valid only if Living Commentary bundle resolution was not requested.
- `Weekly-Package-Source-Truth Rule` — "the package is not multiple random posts. It is multiple realizations of the same underlying source truth." (Source of Truth §10). Weekly package slots must trace back to the same interview session.
- `Commercial-Ladder-Alignment Rule` — bundle manifests must declare which commercial tier ($29.99 / $39.99 / $99.99) the output satisfies, so downstream billing and access control can enforce correctly.

**CBAR Mandate Enforcement:**

| Mandate | Source | Enforcement Mechanism |
|---|---|---|
| Phase4-M05: The Actionable Rejection Rule | Story 5.1 | Rejection payloads include exact failing sentences, similarity scores, coaching fixes — unchanged from v1.0 |
| Phase4-M04: The Frictionless Block Rule | Story 4.1 | Rejection reroutes back to trigger-first capture — unchanged from v1.0 |
| Phase4-M02: The Cinematic Meaning Rule | Story 2.1 | Success manifests now include delivery recipe with module sequence and realization hints, enriching the meaning preservation for CMF |
| Phase7-LC-01: The Delivery Recipe Rule | Living Commentary doctrine | Every archetype emits a typed `ArchetypeDeliveryRecipe` with module sequence, emotional temperature, and format family preferences |
| Phase7-LC-02: The Weekly Package Integrity Rule | Source of Truth §10 | Weekly packages are 7 pieces from one interview, not random assemblies |
| Phase7-LC-03: The MCDA Priority Rule | Source of Truth §9.2 | Delivery recipe resolution respects MCDA-ranked archetype scores for format family priority |

### 3.5 Technical Decisions

| # | Decision | Rationale |
|---|---|---|
| TD-1 | Delivery recipes are resolved *after* archetype selection, not during | Archetype selection is a meaning/force decision based on coalition, stance, evidence. Delivery recipe is a realization decision. Mixing them would violate the meaning/experience plane separation from PRD-02. |
| TD-2 | The 13-archetype MCDA table maps to the 6 existing `ArchetypeChoice` values via a many-to-one grouping | The MCDA lists 13 archetype variants, but the runtime uses 6 structural containers. Multiple MCDA variants map to the same structural container (e.g., both "Challenger" and "Authority Proof Stack" may use `ARC-MYTH-DEBUNK` or `ARC-CONTRAST`). The MCDA ranking informs *recipe selection within a container*, not new container types. |
| TD-3 | Weekly package templates are persisted configuration, not hardcoded | Package composition may evolve (e.g., adding an 8th piece). Persisted templates allow runtime updates without code deployment. |
| TD-4 | Commercial tier alignment is metadata, not business logic | The archetype runtime declares which tier a bundle satisfies. Billing enforcement belongs to the commercial ladder service (FR-ERA3-14). |
| TD-5 | `LivingCommentaryBundleManifest` is additive to `ArchetypeContainerManifest` | The manifest gains optional `delivery_recipe` and `bundle_manifest` fields. Existing v1.0 and v2.0 consumers receive the same manifest shape with `None` for LC fields. |
| TD-6 | Delivery recipe steps use communication module IDs from FR-ERA3-50A | Recipes reference canonical module IDs (e.g., `MOD-AUTHORITY`, `MOD-OBJECTION-SOFTENING`) rather than free-text descriptions, ensuring crosswalk integrity with the Communication Module Library. |
| TD-7 | Bundle manifest includes `editing_session_id` reference | All downstream Remotion rendering reads assets from the Complete Editing Session. The bundle manifest must carry this reference so CMF can resolve VIE backgrounds, SAM3 masks, and coach cutouts. |

---

## 4. Implementation Plan

### Phase 1 — Delivery Recipe Models & Persistence (Tasks 1-4)

**Task 1:** Add new enums and models to `src/ccp/models/archetype_container_runtime_models.py`: `DeliveryRecipeBindingStatus`, `EmotionalTemperature`, `LivingCommentaryFormatPreference`, `CommercialTier`, `DeliveryRecipeStep`, `ArchetypeDeliveryRecipe`, `ArchetypeMCDAEntry`, `MCDAArchetypeRanking`, `ArchetypeToLivingCommentaryMapping`, `CommercialTierAlignment`.

**Task 2:** Add new models to `src/ccp/models/archetype_container_runtime_models.py`: `WeeklyPackageSlot`, `WeeklyPackageTemplate`, `LivingCommentaryBundleManifest`.

**Task 3:** Extend `ArchetypeContainerManifest` with optional fields: `delivery_recipe: ArchetypeDeliveryRecipe | None`, `bundle_manifest: LivingCommentaryBundleManifest | None`, `delivery_recipe_binding_status: DeliveryRecipeBindingStatus`. Extend `CCFRoutingRecommendation` with `delivery_recipe_binding_status: DeliveryRecipeBindingStatus`.

**Task 4:** Extend `src/ccp/scripts/setup_supabase.py` with 3 new tables: `archetype_delivery_recipes`, `weekly_package_templates`, `lc_bundle_manifests`.

### Phase 2 — MCDA Ranking & Recipe Registry (Tasks 5-8)

**Task 5:** Create `MCDAArchetypeRankingRegistry` as a typed in-code registry containing all 13 MCDA-ranked archetype entries with their scores and benefit descriptions. Map each MCDA variant to one or more `ArchetypeChoice` values.

**Task 6:** Create `ArchetypeDeliveryRecipeRegistry` as a typed in-code registry mapping each `ArchetypeChoice` to its canonical delivery recipe (module sequence, emotional temperature, format family preferences, motion/sound hints). Seed with the 7 recipes defined in Source of Truth §7.4.

**Task 7:** Create `ArchetypeToLivingCommentaryMappingResolver` that maps `ArchetypeChoice` to a ranked list of preferred `LivingCommentaryFormatFamily` values (from FR-ERA3-12 v3.0), using MCDA scores to inform priority.

**Task 8:** Create `WeeklyPackageTemplateRegistry` with the canonical 7-piece template: 1 cinematic story + 2 animated explainers + 2 quote commentary + 1 comparison/reaction + 1 atmospheric. Include commercial tier alignment for $29.99 / $39.99 / $99.99.

### Phase 3 — Recipe Compiler Integration (Tasks 9-13)

**Task 9:** Implement `ArchetypeDeliveryRecipeCompiler` as a sub-service within `archetype_container_runtime.py`. Constructor takes `recipe_registry`, `mcda_registry`, `mapping_resolver`, `format_governance_engine`.

**Task 10:** Implement `resolve_delivery_recipe(archetype, coalition, mood_context)` — selects the canonical delivery recipe from the registry, adjusts emotional temperature based on mood context, validates format family preferences against format governance.

**Task 11:** Implement `resolve_format_family_preferences(archetype, recipe)` — returns a ranked list of Living Commentary format families for this archetype, using the MCDA mapping and the recipe's realization hints.

**Task 12:** Implement `compile_bundle_manifest(manifest, recipe, editing_session_id, commercial_tier)` — assembles a `LivingCommentaryBundleManifest` containing the delivery recipe, format preferences, weekly package slot assignment, commercial tier, and Complete Editing Session reference.

**Task 13:** Extend `ArchetypeContainerRuntimeService.compile()` to invoke `ArchetypeDeliveryRecipeCompiler` after successful archetype selection when `editing_session_id` is provided or `resolve_living_commentary_bundle=True`. Bind the recipe and bundle manifest to the container manifest.

### Phase 4 — API Routes & Receipt Chain (Tasks 14-17)

**Task 14:** Extend `POST /api/ccf/archetype-runtime/compile` to accept new optional fields: `editing_session_id: str | None`, `resolve_living_commentary_bundle: bool = False`, `commercial_tier: CommercialTier | None`.

**Task 15:** Add `GET /api/ccf/archetype-runtime/session/{session_id}/delivery-recipe` — returns the resolved `ArchetypeDeliveryRecipe` for inspection.

**Task 16:** Add `GET /api/ccf/archetype-runtime/session/{session_id}/bundle-manifest` — returns the compiled `LivingCommentaryBundleManifest`.

**Task 17:** Extend receipt chain events — add: `delivery_recipe_resolved`, `delivery_recipe_binding_skipped`, `bundle_manifest_compiled`, `weekly_package_slot_assigned`, `commercial_tier_aligned`, `format_family_preference_resolved`.

### Phase 5 — Verification & Integration Tests (Tasks 18-24)

**Task 18:** Unit tests for MCDA ranking registry — verify all 13 entries, scores, and ArchetypeChoice mappings.

**Task 19:** Unit tests for delivery recipe registry — verify all recipes contain valid module sequences and emotional temperatures.

**Task 20:** Unit tests for format family mapping — verify MCDA-ranked preferences for each archetype.

**Task 21:** Integration tests for recipe-bound compile — verify delivery recipe and bundle manifest appear on successful compile with editing session context.

**Task 22:** Integration tests for recipe-absent fallback — verify v1.0 and v2.0 behavior preserved when editing session not provided.

**Task 23:** Integration tests for weekly package template — verify 7-slot composition, commercial tier alignment, format family distribution.

**Task 24:** Non-regression tests confirming delivery recipe does not affect anti-centroid thresholds or SFL binding.

---

## 5. Primary Output Schema (Pydantic v2)

All models use `pydantic.BaseModel`. No `Any` types. All fields explicitly typed.

```python
# --- File: src/ccp/models/archetype_container_runtime_models.py ---
# --- ADDITIONS for v3.0 Living Commentary Bundle ---

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


# === NEW ENUMS (v3.0) ===

class DeliveryRecipeBindingStatus(str, Enum):
    RECIPE_BOUND = "recipe_bound"
    RECIPE_NOT_REQUESTED = "recipe_not_requested"
    RECIPE_UNAVAILABLE = "recipe_unavailable"


class EmotionalTemperature(str, Enum):
    """Emotional temperature governing a delivery recipe's overall tone."""
    ICE_COLD_AUTHORITY = "ice_cold_authority"
    WARM_INVITATION = "warm_invitation"
    HOT_CONVICTION = "hot_conviction"
    CONTROLLED_TENSION = "controlled_tension"
    GENTLE_PERMISSION = "gentle_permission"
    SHARP_CONTRAST = "sharp_contrast"
    QUIET_CONFIDENCE = "quiet_confidence"


class LivingCommentaryFormatPreference(str, Enum):
    """Maps to LivingCommentaryFormatFamily from FR-ERA3-12 v3.0."""
    QUOTE = "quote"
    COMPARISON = "comparison"
    SCREENSHOT = "screenshot"
    ATMOSPHERIC = "atmospheric"
    CINEMATIC_STORY = "cinematic_story"
    ANIMATED_EXPLAINER = "animated_explainer"


class CommercialTier(str, Enum):
    TIER_29_99 = "tier_29_99"
    TIER_39_99 = "tier_39_99"
    TIER_99_99 = "tier_99_99"


# === NEW MODELS (v3.0) ===

class DeliveryRecipeStep(BaseModel):
    """A single step in the archetype delivery recipe module sequence."""
    step_index: int = Field(..., ge=0, description="Zero-based order within the recipe")
    module_id: str = Field(..., min_length=1, description="Communication module ID from FR-ERA3-50A (e.g., MOD-AUTHORITY)")
    module_name: str = Field(..., min_length=1, description="Human-readable module name")
    weight: float = Field(..., ge=0.0, le=1.0, description="Relative dominance within the recipe")
    role_in_recipe: str = Field(..., min_length=1, description="What job this step does: opener, builder, turn, closer, etc.")
    expected_audience_effect: str = Field(..., min_length=1, description="Intended audience state shift")


class ArchetypeDeliveryRecipe(BaseModel):
    """Per-archetype delivery recipe — defines how an archetype is realized as Living Commentary."""
    recipe_id: str = Field(..., min_length=1)
    archetype_choice: ArchetypeChoice
    recipe_version: str = Field(default="1.0")
    module_sequence: list[DeliveryRecipeStep] = Field(..., min_length=2, max_length=8,
        description="Ordered communication module sequence")
    emotional_temperature: EmotionalTemperature
    format_family_preferences: list[LivingCommentaryFormatPreference] = Field(..., min_length=1,
        description="MCDA-ranked format family preferences, best-fit first")
    motion_intensity_hint: str = Field(..., min_length=1,
        description="Motion grammar guidance: e.g., 'minimal_drift', 'sharp_contrast_reveal'")
    sound_doctrine_hint: str = Field(..., min_length=1,
        description="Sound cue guidance: e.g., 'punctuation_dominant', 'atmospheric_bed_priority'")
    first_frame_tension: float = Field(..., ge=0.0, le=1.0,
        description="How much first-frame tension the recipe demands")
    text_interruption_budget: int = Field(..., ge=0, le=10,
        description="Max text overlay events per 60s for this archetype")
    realization_rationale: str = Field(..., min_length=1,
        description="Why this recipe fits this archetype — traces to Source of Truth §7.4")


class ArchetypeMCDAEntry(BaseModel):
    """A single entry in the MCDA-ranked archetype table."""
    mcda_rank: int = Field(..., ge=1, le=13)
    archetype_variant_name: str = Field(..., min_length=1, description="MCDA variant name (may be more specific than ArchetypeChoice)")
    mcda_score: int = Field(..., ge=0, le=200)
    archetype_choice_mapping: ArchetypeChoice = Field(..., description="Which ArchetypeChoice this variant maps to")
    living_commentary_benefit: str = Field(..., min_length=1, description="Why LC benefits this archetype")


class MCDAArchetypeRanking(BaseModel):
    """The complete MCDA-ranked archetype table for Living Commentary realization priority."""
    ranking_id: str = Field(default="MCDA-LC-RANKING-V1")
    entries: list[ArchetypeMCDAEntry] = Field(..., min_length=13, max_length=13,
        description="All 13 MCDA-ranked archetype entries")
    ranking_version: str = Field(default="1.0")
    source_document: str = Field(default="Living_Commentary_Realization_Layer_Source_of_Truth.md §9.2")


class ArchetypeToLivingCommentaryMapping(BaseModel):
    """Maps an archetype to its preferred Living Commentary format families."""
    mapping_id: str = Field(..., min_length=1)
    archetype_choice: ArchetypeChoice
    preferred_families: list[LivingCommentaryFormatPreference] = Field(..., min_length=1,
        description="Format families ranked by MCDA fit, best-fit first")
    mcda_score_range: tuple[int, int] = Field(...,
        description="(min_score, max_score) of MCDA variants mapped to this archetype")
    dominant_family: LivingCommentaryFormatPreference = Field(...,
        description="Primary format family for this archetype")
    secondary_family: LivingCommentaryFormatPreference | None = Field(default=None,
        description="Secondary format family for weekly package diversity")


class CommercialTierAlignment(BaseModel):
    """Pricing tier metadata for a Living Commentary bundle."""
    tier: CommercialTier
    video_count: int = Field(..., ge=1, description="Number of videos included in this tier")
    tier_price_usd: str = Field(..., min_length=1, description="Price string e.g., '29.99'")
    includes_program_access: bool = Field(default=False)
    includes_reaction_videos: bool = Field(default=False)
    reaction_video_count: int = Field(default=0, ge=0)


class WeeklyPackageSlot(BaseModel):
    """A single slot within the weekly package template."""
    slot_index: int = Field(..., ge=0, le=6, description="0-based position in the 7-slot package")
    format_family: LivingCommentaryFormatPreference
    slot_role: str = Field(..., min_length=1,
        description="Role: hero_cinematic, explainer_a, explainer_b, quote_a, quote_b, comparison_reaction, atmospheric")
    archetype_affinity: list[ArchetypeChoice] = Field(default_factory=list,
        description="Which archetypes best fill this slot")
    duration_hint_ms: tuple[int, int] = Field(...,
        description="(min_ms, max_ms) target duration for this slot")


class WeeklyPackageTemplate(BaseModel):
    """Canonical weekly package template — 7 pieces from one 45-60 min interview."""
    template_id: str = Field(default="WPT-LC-V1")
    template_version: str = Field(default="1.0")
    interview_duration_range_minutes: tuple[int, int] = Field(default=(45, 60))
    total_pieces: int = Field(default=7, ge=7, le=7)
    slots: list[WeeklyPackageSlot] = Field(..., min_length=7, max_length=7,
        description="Exactly 7 slots defining the package composition")
    commercial_tiers: list[CommercialTierAlignment] = Field(..., min_length=3, max_length=3,
        description="$29.99 / $39.99 / $99.99 tier definitions")
    source_truth_law: str = Field(
        default="The package is not multiple random posts. It is multiple realizations of the same underlying source truth.",
        description="Core law from Source of Truth §10")


class LivingCommentaryBundleManifest(BaseModel):
    """Compiled Living Commentary bundle output for a single archetype container."""
    bundle_id: str = Field(..., min_length=1)
    runtime_session_id: str = Field(..., min_length=1)
    archetype_choice: ArchetypeChoice
    delivery_recipe: ArchetypeDeliveryRecipe
    format_family_preferences: list[LivingCommentaryFormatPreference] = Field(..., min_length=1)
    weekly_package_slot_index: int | None = Field(default=None, ge=0, le=6,
        description="Which slot in the weekly package this bundle fills, if assigned")
    mcda_rank: int = Field(..., ge=1, le=13, description="MCDA rank of the archetype variant")
    mcda_score: int = Field(..., ge=0, le=200)
    commercial_tier: CommercialTierAlignment | None = Field(default=None)
    editing_session_id: str | None = Field(default=None,
        description="FK to Complete Editing Session for downstream Remotion rendering")
    benchmark_eval_hint: str | None = Field(default=None,
        description="Suggested eval card layout for this archetype + format family combination")
    created_at: datetime
    bundle_valid: bool = Field(..., description="True if recipe + format preferences + slot assignment are valid")
```

### 5.2 Extended `ArchetypeContainerManifest` — new optional fields

```python
# Add to existing ArchetypeContainerManifest:
    delivery_recipe: ArchetypeDeliveryRecipe | None = None
    bundle_manifest: LivingCommentaryBundleManifest | None = None
    delivery_recipe_binding_status: DeliveryRecipeBindingStatus = DeliveryRecipeBindingStatus.RECIPE_NOT_REQUESTED
```

### 5.3 Extended `CCFRoutingRecommendation` — new field

```python
# Add to existing CCFRoutingRecommendation:
    delivery_recipe_binding_status: DeliveryRecipeBindingStatus = DeliveryRecipeBindingStatus.RECIPE_NOT_REQUESTED
```

### 5.4 Extended Compile Request

```json
{
  "coach_response_capture": { "..." },
  "coalition_inputs": { "..." },
  "mood_context": { "..." },
  "evidence_bundle": { "..." },
  "sfl_function_stack": { "..." },
  "composition_depth": { "..." },
  "variation_profile": { "..." },
  "editing_session_id": "EDIT-SESSION-001",
  "resolve_living_commentary_bundle": true,
  "commercial_tier": "tier_29_99"
}
```

### 5.5 New Supabase DDL

```sql
CREATE TABLE IF NOT EXISTS archetype_delivery_recipes (
    recipe_id               TEXT PRIMARY KEY,
    archetype_choice        TEXT NOT NULL,
    recipe_version          TEXT NOT NULL DEFAULT '1.0',
    recipe_json             JSONB NOT NULL,
    emotional_temperature   TEXT NOT NULL,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS weekly_package_templates (
    template_id             TEXT PRIMARY KEY,
    template_version        TEXT NOT NULL DEFAULT '1.0',
    template_json           JSONB NOT NULL,
    total_pieces            INTEGER NOT NULL DEFAULT 7,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS lc_bundle_manifests (
    bundle_id               TEXT PRIMARY KEY,
    runtime_session_id      TEXT NOT NULL,
    archetype_choice        TEXT NOT NULL,
    recipe_id               TEXT NOT NULL REFERENCES archetype_delivery_recipes(recipe_id),
    editing_session_id      TEXT,
    mcda_rank               INTEGER NOT NULL,
    mcda_score              INTEGER NOT NULL,
    commercial_tier         TEXT,
    bundle_json             JSONB NOT NULL,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE archetype_container_manifests
    ADD COLUMN IF NOT EXISTS delivery_recipe_id TEXT REFERENCES archetype_delivery_recipes(recipe_id),
    ADD COLUMN IF NOT EXISTS bundle_manifest_id TEXT REFERENCES lc_bundle_manifests(bundle_id),
    ADD COLUMN IF NOT EXISTS delivery_recipe_binding_status TEXT NOT NULL DEFAULT 'recipe_not_requested';
```

---

## 6. Backward Compatibility Fallback

All v1.0 and v2.0 behavior is preserved unchanged. Living Commentary bundle fields are additive and optional.

### 6.1 Bundle Resolution Not Requested

If the compile request does not include `editing_session_id` and `resolve_living_commentary_bundle` is `False` (default):

- `delivery_recipe_binding_status = RECIPE_NOT_REQUESTED`
- `delivery_recipe` and `bundle_manifest` are both `None` on the manifest
- All v1.0 and v2.0 manifest fields are present and valid
- Downstream CMF receives the standard manifest shape

### 6.2 Recipe Registry Unavailable

If the delivery recipe registry cannot resolve a recipe for the selected archetype:

- `delivery_recipe_binding_status = RECIPE_UNAVAILABLE`
- Compile still succeeds — the archetype container is fully valid without a recipe
- Receipt chain logs `delivery_recipe_binding_skipped` with reason `registry_unavailable`
- CMF receives a standard manifest and must operate without delivery recipe guidance

### 6.3 Editing Session Not Found

If `editing_session_id` is provided but the Complete Editing Session cannot be resolved:

- Bundle manifest is still compiled but with `editing_session_id = None`
- A warning receipt is logged: `editing_session_ref_missing`
- The bundle is marked `bundle_valid = False` because downstream Remotion rendering needs the session

### 6.4 Delivery Recipe Does Not Affect Rejection Thresholds

Anti-centroid rejection remains at `similarity_score >= 0.75`. Delivery recipe resolution occurs *after* archetype selection — if the take is rejected, no recipe is resolved. Recipe binding status has no influence on whether a take is accepted or rejected.

### 6.5 Existing v1.0 and v2.0 Tests Must Continue Passing

All existing integration tests (`test_frera316_archetype_runtime_compile.py`, `test_frera316_actionable_rejection_loop.py`, `test_frera316_sfl_integration.py`) must pass without modification. New LC parameters default to `None` / `False`.

---

## 7. Tasks

### Model Extension

- [ ] Add `DeliveryRecipeBindingStatus` enum
- [ ] Add `EmotionalTemperature` enum
- [ ] Add `LivingCommentaryFormatPreference` enum
- [ ] Add `CommercialTier` enum
- [ ] Add `DeliveryRecipeStep` model
- [ ] Add `ArchetypeDeliveryRecipe` model
- [ ] Add `ArchetypeMCDAEntry` model
- [ ] Add `MCDAArchetypeRanking` model
- [ ] Add `ArchetypeToLivingCommentaryMapping` model
- [ ] Add `CommercialTierAlignment` model
- [ ] Add `WeeklyPackageSlot` model
- [ ] Add `WeeklyPackageTemplate` model
- [ ] Add `LivingCommentaryBundleManifest` model

### Manifest Extension

- [ ] Extend `ArchetypeContainerManifest` with delivery recipe optional fields
- [ ] Extend `CCFRoutingRecommendation` with `delivery_recipe_binding_status`

### Registries

- [ ] Create `MCDAArchetypeRankingRegistry` with all 13 entries
- [ ] Create `ArchetypeDeliveryRecipeRegistry` with canonical recipes for all 6 `ArchetypeChoice` values
- [ ] Create `ArchetypeToLivingCommentaryMappingResolver`
- [ ] Create `WeeklyPackageTemplateRegistry` with 7-slot template and 3 commercial tiers

### Service Extension

- [ ] Create `ArchetypeDeliveryRecipeCompiler` sub-service
- [ ] Implement `resolve_delivery_recipe(archetype, coalition, mood_context)`
- [ ] Implement `resolve_format_family_preferences(archetype, recipe)`
- [ ] Implement `compile_bundle_manifest(manifest, recipe, editing_session_id, commercial_tier)`
- [ ] Extend `compile()` to invoke recipe compiler when LC bundle requested

### Persistence

- [ ] Add `archetype_delivery_recipes` table
- [ ] Add `weekly_package_templates` table
- [ ] Add `lc_bundle_manifests` table
- [ ] Add delivery recipe columns to `archetype_container_manifests` table

### API Routes

- [ ] Extend `POST /api/ccf/archetype-runtime/compile` with new optional params
- [ ] Add `GET /api/ccf/archetype-runtime/session/{session_id}/delivery-recipe`
- [ ] Add `GET /api/ccf/archetype-runtime/session/{session_id}/bundle-manifest`

### Receipt Chain

- [ ] Add receipt entries for `delivery_recipe_resolved`, `delivery_recipe_binding_skipped`, `bundle_manifest_compiled`, `weekly_package_slot_assigned`, `commercial_tier_aligned`, `format_family_preference_resolved`

### Testing

- [ ] Add unit tests for MCDA ranking registry (13 entries, score validation)
- [ ] Add unit tests for delivery recipe registry (valid module sequences, temperatures)
- [ ] Add unit tests for format family mapping (MCDA-ranked preferences)
- [ ] Add integration tests for recipe-bound compile
- [ ] Add integration tests for recipe-absent fallback
- [ ] Add integration tests for weekly package template (7 slots, tier alignment)
- [ ] Add non-regression tests confirming delivery recipe does not affect anti-centroid
- [ ] Update existing tests to confirm backward compatibility

---

## 8. Acceptance Criteria

### AC-LC-1 — Recipe-bound compile emits delivery recipe and bundle manifest

**Given** a valid compile request with `editing_session_id` provided and `resolve_living_commentary_bundle=True`,
**When** the runtime compiles successfully (archetype selected),
**Then** `ArchetypeContainerManifest.delivery_recipe` is populated with a valid `ArchetypeDeliveryRecipe`,
**And** `ArchetypeContainerManifest.bundle_manifest` is populated with a valid `LivingCommentaryBundleManifest`,
**And** `delivery_recipe_binding_status == RECIPE_BOUND`,
**And** the recipe's `module_sequence` contains at least 2 steps with valid `module_id` references,
**And** the recipe's `emotional_temperature` is one of the 7 canonical temperatures,
**And** the recipe's `format_family_preferences` is non-empty and ranks Living Commentary format families.

**FAILURE EXAMPLE:** The runtime accepts the LC bundle request but emits `delivery_recipe = None` with `delivery_recipe_binding_status = RECIPE_BOUND`. That contradicts the binding status claim and leaves CMF without realization guidance, violating Phase7-LC-01.

**Mandate:** Phase7-LC-01: The Delivery Recipe Rule.

### AC-LC-2 — MCDA-ranked archetype mapping is complete and scored

**Given** the MCDA archetype ranking registry is initialized,
**When** a consumer queries all entries,
**Then** exactly 13 entries are returned,
**And** each entry has a valid `mcda_score` between 0 and 200,
**And** each entry maps to one of the 6 `ArchetypeChoice` values,
**And** entries are ordered by `mcda_rank` from 1 (highest) to 13 (lowest),
**And** the top 3 entries are: Comparison Breakdown (193), Challenger / Frame Breaker (191), Myth Debunk (188).

**FAILURE EXAMPLE:** The registry returns only 6 entries (one per `ArchetypeChoice`) instead of 13 MCDA variants. That collapses the MCDA granularity and loses the per-variant benefit analysis, violating Phase7-LC-03.

**Mandate:** Phase7-LC-03: The MCDA Priority Rule.

### AC-LC-3 — Weekly package template defines exactly 7 slots with commercial tier alignment

**Given** the weekly package template is loaded,
**When** the template is validated,
**Then** it contains exactly 7 `WeeklyPackageSlot` entries,
**And** the slots distribute as: 1 cinematic story + 2 animated explainers + 2 quote commentary + 1 comparison/reaction + 1 atmospheric,
**And** exactly 3 `CommercialTierAlignment` entries exist: $29.99 (7 videos), $39.99 (program access), $99.99 (program + 32 videos),
**And** `source_truth_law` is populated with the canonical law from Source of Truth §10.

**FAILURE EXAMPLE:** The template defines 5 slots (missing the atmospheric and one explainer) because "most coaches only need 5 videos." That breaks the weekly package integrity law and under-serves coaches who paid for the full package, violating Phase7-LC-02.

**Mandate:** Phase7-LC-02: The Weekly Package Integrity Rule.

### AC-LC-4 — Delivery recipe does not affect anti-centroid rejection thresholds

**Given** a transcript with generic consensus sentences that triggers anti-centroid rejection,
**When** the compile request includes `resolve_living_commentary_bundle=True` and a valid `editing_session_id`,
**Then** the runtime still rejects with `status=rejected_actionable`,
**And** the rejection threshold remains `similarity_score >= 0.75`,
**And** no delivery recipe is resolved (recipe resolution occurs after selection),
**And** `delivery_recipe_binding_status` is not set to `RECIPE_BOUND`.

**FAILURE EXAMPLE:** The runtime sees the LC bundle request and relaxes the anti-centroid threshold to 0.85 because "Living Commentary can make generic content look premium." That violates the truth-before-delivery law: meaning decisions cannot be softened by realization preferences.

**Mandate:** Phase4-M05: The Actionable Rejection Rule (preserved).

### AC-LC-5 — Per-archetype delivery recipe contains the correct module sequence

**Given** a successful compile with archetype `ARC-MYTH-DEBUNK` and LC bundle requested,
**When** the delivery recipe is resolved,
**Then** the recipe's `module_sequence` follows the Myth Debunk pattern: named false belief → persistence reason → coach proof → reframe,
**And** `emotional_temperature` is appropriate (e.g., `SHARP_CONTRAST` or `HOT_CONVICTION`),
**And** `first_frame_tension >= 0.7` (myth debunks demand high first-frame authority),
**And** `motion_intensity_hint` references screenshot-first or quote-reveal mechanics.

**FAILURE EXAMPLE:** The runtime resolves a delivery recipe for `ARC-MYTH-DEBUNK` with the module sequence `identification → story → hope` (which is the Witness Story recipe). That would produce gentle, inviting content when the archetype demands sharp, evidence-led dismantling — a fundamental realization mismatch.

**Mandate:** Phase7-LC-01: The Delivery Recipe Rule + Archetype-Realization Separation Rule.

### AC-LC-6 — Bundle manifest includes Complete Editing Session reference

**Given** a successful LC-bound compile with `editing_session_id="EDIT-SESSION-001"`,
**When** the `LivingCommentaryBundleManifest` is compiled,
**Then** `bundle_manifest.editing_session_id == "EDIT-SESSION-001"`,
**And** the manifest is marked `bundle_valid = True`,
**And** downstream systems can use this ID to resolve VIE backgrounds, SAM3 masks, and coach cutouts from the Complete Editing Session payload.

**FAILURE EXAMPLE:** The bundle manifest is compiled without an `editing_session_id` even though one was provided in the request. The downstream Remotion server then fails to locate the coach cutout and VIE backgrounds, producing a black-screen render. That breaks the Complete Editing Session contract.

**Mandate:** Remotion backend rendering mandate from HANDOVER_CONSOLIDATION_BLUEPRINTS.md.

### AC-LC-7 — No new archetype ontology is created

**Given** any modification to the archetype runtime models or registry,
**When** the `ArchetypeChoice` enum is inspected,
**Then** it contains exactly 6 values: `ARC-MYTH-DEBUNK`, `ARC-ACH-STORY`, `ARC-OBS-HUMOR`, `ARC-WITNESS`, `ARC-CONTRAST`, `ARC-COMP`,
**And** no new enum values have been added,
**And** the 13 MCDA variants map to these 6 existing choices via `ArchetypeMCDAEntry.archetype_choice_mapping`.

**FAILURE EXAMPLE:** A developer adds `ARC-CHALLENGER`, `ARC-AUTHORITY-PROOF`, `ARC-RELIEF-PEAK` as new `ArchetypeChoice` values to match the MCDA table. That creates a new archetype ontology with 9+ values, breaking all downstream consumers and violating the No-New-Archetype-Ontology Rule.

**Mandate:** No-New-Archetype-Ontology Rule.

### AC-LC-8 — Existing v1.0 and v2.0 behavior is preserved

**Given** a valid compile request with NO LC-related inputs (v1.0/v2.0 shape),
**When** the runtime compiles,
**Then** the result matches v1.0/v2.0 behavior exactly,
**And** `delivery_recipe_binding_status == RECIPE_NOT_REQUESTED`,
**And** `delivery_recipe` and `bundle_manifest` are both `None`,
**And** all existing acceptance criteria (AC1-AC6 from v1.0, AC-SFL-1 through AC-SFL-6 from v2.0) continue to pass.

**FAILURE EXAMPLE:** The runtime crashes or returns a validation error because `editing_session_id` is `None` and the recipe compiler expects it. That breaks backward compatibility with all existing callers.

**Mandate:** Backward compatibility mandate.

---

## 9. Dependencies

### Internal Services

| Dependency | Type | Use |
|---|---|---|
| `FR-ERA3-16 v1.0` | Base spec | All existing runtime logic preserved |
| `FR-ERA3-16 v2.0` | Previous update | All SFL binding logic preserved |
| `FR-ERA3-12 v3.0` | Downstream consumer | CMF Living Commentary renderer consumes `ArchetypeDeliveryRecipe` and `LivingCommentaryBundleManifest` to select format family and apply realization rules |
| `FR-ERA3-14 Stealth Course Commercial Ladder` | Adjacent spec | Commercial tier alignment ($29.99 / $39.99 / $99.99) must be consistent with the stealth course pricing model |
| `FR-ERA3-35B Content Benchmark Profiles` | Read dependency | MCDA rankings cross-referenced with benchmark score emphasis for archetype + content type combinations |
| `FR-ERA3-35C Eval Card System` | Read dependency | Bundle manifests suggest eval card layouts for archetype + format family combinations |
| `FR-ERA3-50A Communication Module Library` | Read dependency | Delivery recipe steps reference canonical module IDs from the communication module library |
| `FormatGovernanceEngine` | Existing service | Validates that weekly package template slot counts align with the 36-format weekly governance budget |
| `ReceiptChain` | Existing core | Extended with delivery recipe and bundle manifest receipt entries |
| `ResearchSynthesisProtocol` | Existing service | Evidence conflict pass — unchanged from v1.0 |
| `PsychVariableMatrix` | Existing service | Mood classification — unchanged from v1.0 |

### Internal Models

| Dependency | Type | Use |
|---|---|---|
| `archetype_container_runtime_models.py` | Extended | 13 new models, 2 extended models, 4 new enums |
| `benchmark_profile_models.py` | Read-only | `ArchetypeScoreBundle` for MCDA cross-reference |
| `phase0_eval_card_models.py` | Read-only | `EvalCardFace`, `EvalBoardLayout` for eval hint resolution |
| `cmf_living_commentary_models.py` | Read-only | `LivingCommentaryFormatFamily` for format preference alignment |
| Supabase | Existing infra | 3 new tables, 3 new columns on existing table |

### External

| Library | Version | Purpose |
|---|---|---|
| `pydantic` | v2.x | Typed model definitions |

---

## 10. Testing Strategy

### 10.1 Unit Tests

#### `test_frera316_mcda_ranking_registry.py`

- `test_registry_contains_exactly_13_entries`
- `test_entries_ordered_by_rank_ascending`
- `test_top_three_are_comparison_challenger_myth_debunk`
- `test_all_entries_map_to_valid_archetype_choice`
- `test_scores_range_from_165_to_193`

#### `test_frera316_delivery_recipe_registry.py`

- `test_all_six_archetype_choices_have_recipes`
- `test_myth_debunk_recipe_has_correct_module_sequence`
- `test_witness_story_recipe_has_gentle_permission_temperature`
- `test_challenger_recipe_has_high_first_frame_tension`
- `test_recipe_module_ids_reference_canonical_mod_prefix`
- `test_recipe_format_preferences_are_non_empty`

#### `test_frera316_format_family_mapping.py`

- `test_comparison_archetype_prefers_comparison_format`
- `test_myth_debunk_prefers_screenshot_or_quote_format`
- `test_witness_story_prefers_atmospheric_or_cinematic_format`
- `test_all_archetypes_have_at_least_one_format_preference`

#### `test_frera316_weekly_package_template.py`

- `test_template_has_exactly_7_slots`
- `test_template_has_exactly_3_commercial_tiers`
- `test_slot_distribution_matches_doctrine`
- `test_tier_29_99_has_7_videos`
- `test_tier_99_99_has_32_videos_and_program_access`
- `test_source_truth_law_is_populated`

### 10.2 Integration Tests

#### `tests/integration/test_frera316_lc_recipe_bound_compile.py`

Scenario class: `TestACLC1RecipeBoundCompile`

- Build valid capture + coalition + mood + evidence + SFL (full v2.0 shape) + `editing_session_id` + `resolve_living_commentary_bundle=True`.
- Assert `status == compiled`.
- Assert `delivery_recipe_binding_status == RECIPE_BOUND`.
- Assert `container_manifest.delivery_recipe` is populated with valid `ArchetypeDeliveryRecipe`.
- Assert `container_manifest.bundle_manifest` is populated with valid `LivingCommentaryBundleManifest`.
- Assert `delivery_recipe.module_sequence` has at least 2 steps.
- Assert `bundle_manifest.mcda_rank` is between 1 and 13.

Scenario class: `TestACLC8RecipeAbsentFallback`

- Build valid capture + coalition (v1.0 shape, no LC inputs).
- Assert `status == compiled`.
- Assert `delivery_recipe_binding_status == RECIPE_NOT_REQUESTED`.
- Assert `delivery_recipe is None`.
- Assert `bundle_manifest is None`.
- Assert all v1.0 and v2.0 manifest fields present and valid.

#### `tests/integration/test_frera316_lc_delivery_recipe.py`

Scenario class: `TestACLC5PerArchetypeRecipe`

- For each `ArchetypeChoice`, build a valid compile with LC bundle.
- Assert recipe is resolved and has appropriate emotional temperature.
- Assert `ARC-MYTH-DEBUNK` recipe has high first_frame_tension (>= 0.7).
- Assert `ARC-WITNESS` recipe has low first_frame_tension (<= 0.4).

Scenario class: `TestACLC4RecipeDoesNotAffectRejection`

- Feed generic consensus transcript + `resolve_living_commentary_bundle=True`.
- Assert `status == rejected_actionable`.
- Assert `similarity_score >= 0.75`.
- Assert `delivery_recipe` is `None` on the rejection.

#### `tests/integration/test_frera316_lc_bundle_manifest.py`

Scenario class: `TestACLC6BundleSessionReference`

- Build compile with `editing_session_id="EDIT-SESSION-TEST"`.
- Assert `bundle_manifest.editing_session_id == "EDIT-SESSION-TEST"`.
- Assert `bundle_manifest.bundle_valid == True`.

Scenario class: `TestACLC7NoNewOntology`

- Assert `ArchetypeChoice` enum has exactly 6 values.
- Assert `MCDAArchetypeRanking` has 13 entries.
- Assert all 13 entries map to one of the 6 existing choices.

#### `tests/integration/test_frera316_weekly_package.py`

Scenario class: `TestACLC3WeeklyPackage`

- Load the weekly package template.
- Assert 7 slots, 3 tiers.
- Assert slot format families match: 1 cinematic + 2 explainer + 2 quote + 1 comparison + 1 atmospheric.
- Assert $29.99 tier = 7 videos, $99.99 tier = 32 videos with program access.

### 10.3 Non-Regression Expectations

- No existing v1.0 or v2.0 test may break when LC parameters are absent.
- No test may accept a delivery recipe without at least 2 module sequence steps.
- No test may allow delivery recipe resolution to change rejection thresholds.
- No test may accept an `ArchetypeChoice` enum with more than 6 values.
- No test may accept a weekly package template with fewer or more than 7 slots.
- No test may accept a commercial tier alignment that contradicts the $29.99 / $39.99 / $99.99 pricing.
- No test may accept a bundle manifest marked `bundle_valid=True` without an `editing_session_id`.
- No test may accept a delivery recipe whose module IDs are free-text instead of canonical `MOD-*` references.
