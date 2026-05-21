# Tech-Spec: FR-ERA3-12 - CMF Arc-Governed Rendering (OmniShotCut)
**Created:** 2026-05-11
<!-- UPDATED: version bump for SDA Representation Geometry governance integration -->
**Updated:** 2026-05-13
**Status:** Ready for Development
**Version:** 1.1 (ERA3 - CBAR-Hardened + SDA Representation Geometry)
**Phase:** 4 - Pipelines & Engines
**Architecture Reference:** ERA3_Tech_Spec_Writing_Protocol.md Section 7

## Pre-Work Log

```
1. PROTOCOL LOADED:   Section 2.2 confirms new endpoints extend `src/ccp/api/main.py`, Section 2.3 confirms
                      schema changes extend `src/ccp/scripts/setup_supabase.py`, Section 3 requires explicit
                      mapping to existing services before introducing new ones, and the CBAR note requires
                      mandate enforcement to be named directly in Section 3 instead of implied.
2. PRD LOADED:        PRD-03 exact brownfield definition: "CMF must transition from generic "montage"
                      compilation to Arc-Governed Rendering. Media assembly must respect narrative geometry
                      (e.g., Witness, Rally, Reflection) using Beat Clusters as visual translation units."
                      PRD-03 Section 5.1 states: "The strongest idea in the CMF pipeline is that media assembly
                      is governed by narrative arc, not by generic montage logic." Section 5.2 adds: "Beat
                      clusters are the bridge between script meaning and media construction." PRD-03 also
                      states: "The visual control layer exists because media pipelines fail when identity, pose,
                      gaze, and expression are left to chance. ConsciousPose, ConsciousSmile, Identity LoRA, and
                      First Frame Composer together create a deterministic scaffold inside the visual generative
                      stack."
3. EPIC LOADED:       Phase 4 exact FR line: "FR-ERA3-12 (CMF Arc-Governed Rendering): The deterministic visual
                      and sonic assembly engine utilizing Beat Clusters to translate meaning into premium media
                      (PRD-03)." Story 2.1 first AC: "Given a Coalition Script Spine from CCF, When it enters
                      the Narrative Rendering Model, Then it translates the meaning into specific Beat Clusters,
                      applying distinct shot grammar and music tempo for the assigned arc (e.g., Rally, Witness,
                      Reflection), And the Deterministic Control Layer enforces Cinematic Meaning visual grammar:
                      high-contrast lighting, cinematic pacing, intense sonic beds, First Frame Composer hooks,
                      ConsciousPose, and Identity LoRA, And no output is released unless it passes the Epic
                      Meaning Framing quality gate, which rejects flat, brightly lit, corporate-aesthetic renders."
4. CBAR LOADED:       Phase4-M02 confirmed from the Phase 4 audit. Exact rewrite demand: "The `Narrative
                      Rendering Model` must explicitly map the `Coalition Script Spine` to Epic Meaning visual
                      grammar." The UX failure scenario is a "bland, brightly lit, corporate SaaS tutorial video
                      with generic stock music." The hallucination purge also corrects the primitive from false
                      `EXP-TRB-004` to real `EXP-TRS-004`.
5. PRIMITIVES:        `experience_primitive_id: "EXP-TRS-004"` / `canonical_name: "Epic Meaning Framing (The
                      Crusade Narrative)"`
                      `experience_primitive_id: "EXP-PER-003"` / `canonical_name: "Cumulative Investment"`
6. BACKEND:           `src/ccp/services/abel_vcb_generator.py` - `def generate(self, inp: VCBGenerationInput) -> VisualCompositionBrief`
                      `src/ccp/services/canvas_composition_service.py` - `def create_composition(self, vcb_id: str, template_id: str, slide_count: int, dimensions: dict[str, Any], handle_bar: dict[str, Any], text_content: dict[int, dict[str, str]] | None = None, content_output_id: str | None = None) -> CanvasComposition`
                      `src/ccp/services/canvas_composition_service.py` - `def request_regeneration(self, composition_id: str, slide_index: int, revision_note: str) -> tuple[CanvasComposition, RegenerationRequest]`
                      `src/ccp/services/canvas_composition_service.py` - `def approve(self, composition_id: str) -> CanvasComposition`
                      `src/ccp/services/format_governance_engine.py` - `def apply_format_governance(self, scored_traits: list[ScoredTrait]) -> list[ScoredTrait]`
7. TESTS:             `tests/integration/test_cpsc_fr52_webinar_brief.py` and
                      `tests/integration/test_ca11_fr16_studio_block.py` both use helper builders, scenario-
                      oriented test classes, direct field assertions, and concrete status checks. Section 10
                      follows the same pattern instead of generic pipeline smoke tests.
8. SDA LOADED:        All four mandatory SDA source documents read. Content Engine v1 Section 6
                      defines Representation Geometry; Section 7 defines Hard Negatives; Section 9
                      defines Direction vs Magnitude. Artifact Taxonomy v1 Section 5.1.2 defines
                      Representation Geometry canonical ontology with encoding axes, authority
                      structure, fear weighting, manipulation risks, and drift risks; Section 5.5.1
                      defines Directional Integrity Policy; Section 5.7.7 defines runtime scalar
                      fields including symbolic_density and trajectory_risk. Perceptual Primitives
                      Architecture Law 7 and Matrix of Edging Section 12 both mandate anti-centroid
                      protection at every handoff. PRD-03 Section 3.3A confirms CMF inherits SDA
                      doctrine and must preserve Invariant Field, Archetypal Geometry, admissible
                      Representation Geometry, and downstream Directional Integrity.
9. SDA PROOF:         Existing spec v1.0 gates (FirstFrameAuthorityGate, EpicMeaningGate,
                      RenderReleaseGate) operate only on aesthetic anti-patterns. They contain ZERO
                      reference to Representation Geometry, Invariant Field, symbolic_density, hard-
                      negative adjacency, or Directional Integrity. A render that is cinematic but
                      distorts invariant gravity into fake epicness, prestige theater, or coercive
                      aspiration coding would pass all v1.0 gates. This update closes that gap.
```

## 1. Files Read

| # | File | Version/Date | Purpose |
|---|---|---|---|
| 1 | `docs/architecture/april_updates/spec_prompts/P4_S22_FR-ERA3-12_CMF_Arc_Governed_Rendering.md` | 2026-05-11 | Assignment prompt, Beat Cluster requirement, and M-02 rendering gate |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Loaded 2026-05-11 | Required backend mapping, schema extension points, and CBAR formatting rules |
| 3 | `docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | 2026-05-10 | Epic 2 story, first AC, primitive constraint text, and mandate definition |
| 4 | `docs/architecture/cbar_audits/CBAR_Audit_Phase4_Pipelines_and_Engines.md` | 2026-05-10 | Phase4-M02 rewrite demand and primitive correction log |
| 5 | `docs/prd/modules/PRD_03_CMF_Media_Factory.md` | v6.0, 2026-05-06 | Arc-governed rendering doctrine, Beat Clusters, deterministic control layer, and brownfield boundaries |
| 6 | `docs/architecture/FR-VIS-16_First_Frame_Composer_Tech_Spec.md` | 2026-03-30 | Existing First Frame Composer contract that this spec consumes as a gate, not a rewrite |
| 7 | `lab/OmniShotCut Holistic Relational Shot Boundary.md` | Research note | Shot-boundary grouping reference for cluster-aware transition and segment boundary planning |
| 8 | `primitives/experience/trust_branding/EXP-TRS-004.yaml` | Codified registry | Verified governing primitive for Epic Meaning Framing |
| 9 | `primitives/experience/personalization_identity/EXP-PER-003.yaml` | Codified registry | Verified supporting primitive for identity continuity and recognizability |
| 10 | `src/ccp/services/abel_vcb_generator.py` | Existing service | VCB generation boundary and Gate C-09 visual planning contract |
| 11 | `src/ccp/services/canvas_composition_service.py` | Existing service | Composition assembly, regeneration, and approval boundary |
| 12 | `src/ccp/services/format_governance_engine.py` | Existing service | Existing format-allocation boundary that supplies format decisions upstream of rendering |
| 13 | `src/ccp/models/visual_engine_models.py` | Existing models | `SomaticArcType`, `PSSLBlock`, `GateC09Result`, `VisualCompositionBrief`, and anti-generic constants |
| 14 | `src/ccp/api/main.py` | 1.0.0 | FastAPI extension point for new rendering routes |
| 15 | `src/ccp/core/receipt_chain.py` | Current | Immutable render-stage audit logging |
| 16 | `src/ccp/core/circuit_breaker.py` | Current | Failure halt and blocked-release contract |
| 17 | `src/ccp/scripts/setup_supabase.py` | Current | Schema bootstrap extension point |
| 18 | `src/ccp/sidecars/skia-renderer/` | Current directory boundary | Target sidecar integration boundary for final assembly and render execution |
| 19 | `tests/integration/test_cpsc_fr52_webinar_brief.py` | Existing | Integration-test structure and helper style |
| 20 | `tests/integration/test_ca11_fr16_studio_block.py` | Existing | Async orchestration pattern and concrete field assertions |
<!-- UPDATED: SDA mandatory source set added per P6_S41 update prompt -->
| 21 | `lab/semantic_discernment_architecture_content_engine_v_1.md` | 2026-05-12 | SDA core framework: existential invariants, representation geometry, hard negatives, directional integrity, and layered discernment architecture |
| 22 | `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md` | 2026-05-12 | SDA artifact taxonomy: canonical ontology classes, runtime execution packets, validation policies, invariant gravity / activation intensity / resonance multiplier separation, and pipeline placement |
| 23 | `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md` | 2026-05-02 | Perceptual primitives: anti-centroid law, coalition signatures, candidate survival, and edge product formation |
| 24 | `lab/CCP APRIL Updates/05_Core_Experience/Matrix of Edging.md` | 2026-05-03 | Matrix of Edging: anti-centroid doctrine, tension selection vs delivery separation, and coalition fatality detection |

## 2. Overview

### 2.1 Problem Statement

The repo already contains important CMF pieces. `AbelVCBGenerator.generate(...)` can produce a `VisualCompositionBrief`. `CanvasCompositionService` can assemble and approve compositions. `FormatGovernanceEngine` can decide which formats deserve exercise versus showcase treatment. `visual_engine_models.py` already codifies anti-generic constraints and Gate C-09.

What is still missing is the rendering interpreter that sits between meaning and media and makes narrative geometry executable.

That gap produces four concrete failures:

- scripts can still be rendered as generic montage instead of arc-specific pacing
- VCB planning can remain slide-correct while the output still looks emotionally wrong
- the pipeline can move into full render before the scroll-stop first frame is proven authoritative
- a render can technically succeed while still failing the Crusade Narrative because it looks flat, bright, sterile, or corporate
<!-- UPDATED: fifth failure mode added for SDA representation-geometry gap -->
- a render can be cinematic and visually intense while silently mutating the source invariant gravity into fake epicness, prestige theater, coercive aspiration coding, or manipulative symbolic density — passing all aesthetic gates while corrupting semantic direction

Epic 2 is explicitly about closing that gap. The system needs a deterministic Narrative Rendering Model that transforms a Coalition Script Spine into Beat Clusters, uses those clusters to drive shot grammar and music tempo, rejects corporate-looking outputs before the full render path wastes time and trust, and preserves SDA Representation Geometry so that render intensification never silently mutates meaning direction.

### 2.2 Solution

This spec introduces a new backend pipeline, `CMFArcGovernedRenderingPipeline`, with OmniShotCut-inspired shot-boundary awareness and a mandatory pre-render quality gate.

The pipeline adds six orchestration layers on top of the existing CMF services:

- `NarrativeRenderingModel` to convert Coalition Script Spine inputs into Beat Clusters
- `BeatClusterPlanner` to assign shot grammar, transition profile, and tempo map for Rally, Witness, Reflection, and Confrontation arcs
- `DeterministicControlResolver` to attach First Frame Composer, ConsciousPose, ConsciousSmile, and Identity LoRA directives to each cluster
- `FirstFrameAuthorityGate` to reject weak first-frame specs before expensive render work starts
- `EpicMeaningGate` to reject flat, brightly lit, corporate-aesthetic render plans and first-frame previews
<!-- UPDATED: RepresentationDriftGate added for SDA representation-geometry governance -->
- `RepresentationDriftGate` to verify that render-time visual and sonic choices preserve the source artifact's Invariant Field, Representation Geometry, and Directional Integrity — blocking renders that are visually premium but semantically corrupt
- `SkiaRenderManifestBuilder` plus `SkiaRenderSidecarBridge` to hand approved manifests to the Skia sidecar for actual assembly

This is not a generic editor and not a rewrite of Abel or Canvas. It is the narrative-to-render coordination layer that makes those existing systems obey the arc and preserve the semantic direction of the source meaning.

### 2.3 Scope

**In scope:**

- new Narrative Rendering Model service
- Beat Cluster planning for Rally, Witness, Reflection, and Confrontation modes
- shot grammar, transition spacing, and tempo-map generation per cluster
- mandatory First Frame Composer pre-render validation
- Epic Meaning quality gate with explicit corporate-aesthetic rejection
- deterministic control binding for ConsciousPose, ConsciousSmile, and Identity LoRA
- Skia sidecar render manifest generation and sidecar handoff contract
- database persistence for render jobs, cluster plans, gate results, and manifests
- pipeline routes for create/get/retry/release actions
- receipt logging and circuit-breaker halts
<!-- UPDATED: SDA representation-geometry governance scope added -->
- SDA Representation Geometry preservation: representation drift checks before render release
- symbolic-density preservation across render intensification
- hard-negative adjacency detection on visual and sonic choices
- explicit separation of premium render amplification from semantic corruption

**Out of scope:**

- replacing `AbelVCBGenerator` as the VCB planner
- replacing `CanvasCompositionService` as the composition approval engine
- redefining `FormatGovernanceEngine` or weekly allocation logic
- training Identity LoRA models or authoring ConsciousPose / ConsciousSmile libraries
- rebuilding First Frame Composer; this spec consumes it as an upstream gate
- inventing a coach-facing editor surface

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Component | Source | Responsibility |
|---|---|---|---|
| DEP-CMF-001 | `CMFArcGovernedRenderingPipeline` | FR-ERA3-12 | Top-level pipeline that coordinates cluster planning, deterministic controls, quality gates, and sidecar handoff |
| DEP-CMF-002 | `NarrativeRenderingModel` | Story 2.1 | Converts Coalition Script Spine input into a typed render plan with Beat Clusters |
| DEP-CMF-003 | `BeatClusterPlanner` | Story 2.1 | Produces cluster sequence, shot grammar, tempo curve, and transition budget for Rally, Witness, Reflection, and Confrontation |
| DEP-CMF-004 | `OmniShotBoundaryPlanner` | Story 2.1 | Uses shot-boundary-aware transition windows to keep cuts aligned to cluster pressure rather than arbitrary timing |
| DEP-CMF-005 | `DeterministicControlResolver` | Story 2.1 / M-02 | Resolves First Frame Composer spec, ConsciousPose, ConsciousSmile, and Identity LoRA directives before generation |
| DEP-CMF-006 | `FirstFrameAuthorityGate` | Story 2.1 / M-02 | Mandatory pre-render gate that blocks execution if the first-frame plan lacks authority or looks generic |
| DEP-CMF-007 | `EpicMeaningGate` | Phase4-M02 | Rejects flat, bright, sterile, corporate-aesthetic renders before release |
| DEP-CMF-008 | `ArcSonicBedPlanner` | Story 2.1 | Maps each Beat Cluster to tempo, silence windows, and sonic intensity rules |
| DEP-CMF-009 | `ArcGovernedVCBAugmentor` | FR-ERA3-12 | Enriches `VCBGenerationInput` with beat-cluster and control-layer directives for Abel |
| DEP-CMF-010 | `SkiaRenderManifestBuilder` | FR-ERA3-12 | Produces deterministic render manifest for the Skia sidecar |
| DEP-CMF-011 | `SkiaRenderSidecarBridge` | FR-ERA3-12 | Writes manifests, triggers render jobs, reads preview output, and records sidecar status |
| DEP-CMF-012 | `RenderReleaseGate` | Story 2.1 / M-02 | Ensures only Epic-meaning-approved artifacts can move into composition approval |
| DEP-CMF-013 | `ArcRenderApiRouter` | FR-ERA3-12 | FastAPI route layer for pipeline job creation, status checks, retry, and release |
| DEP-CMF-014 | `ArcRenderReceiptBridge` | FR-ERA3-12 | Receipt logging for cluster planning, first-frame check, gate pass/fail, sidecar launch, and release |
<!-- UPDATED: SDA representation-geometry governance components added -->
| DEP-CMF-015 | `RepresentationDriftGate` | PRD-03 §3.3A / SDA | Evaluates whether render-time visual and sonic choices preserve the source Invariant Field, Representation Geometry, and Directional Integrity. Blocks releases where render amplification has silently mutated meaning direction. |
| DEP-CMF-016 | `SymbolicDensityPreserver` | SDA Content Engine §9 | Verifies that render intensification preserves symbolic density (semantic magnitude) without collapsing it into generic epicness or inflating it into prestige theater. |
| DEP-CMF-017 | `HardNegativeAdjacencyChecker` | SDA Content Engine §7 | Detects when visual or sonic choices are deceptively close to valid rendering but have drifted into known hard-negative patterns (fake epicness, coercive aspiration, manipulative symbolic coding). |

### 3.2 Existing Backend Integration

| File | Path | How This Spec Uses It |
|---|---|---|
| `abel_vcb_generator.py` | `src/ccp/services/abel_vcb_generator.py` | `generate(...)` remains the canonical VCB generation boundary. This spec enriches its inputs with cluster-aware directives instead of replacing its planning logic. |
| `canvas_composition_service.py` | `src/ccp/services/canvas_composition_service.py` | `create_composition(...)` assembles the approved render output into a composition; `request_regeneration(...)` is used when a specific cluster preview fails; `approve(...)` remains the final composition-approval boundary. |
| `format_governance_engine.py` | `src/ccp/services/format_governance_engine.py` | The pipeline consumes existing upstream format allocation decisions. It does not invent new format-selection logic. |
| `visual_engine_models.py` | `src/ccp/models/visual_engine_models.py` | Reuses `SomaticArcType`, `PSSLBlock`, `GateC09Result`, `GateC09Verdict`, `VisualCompositionBrief`, and the `UNIVERSAL_ANTI_GENERIC` / enemy anti-pattern constants. |
| `FR-VIS-16_First_Frame_Composer_Tech_Spec.md` | Existing architecture contract | Provides the pre-existing first-frame composition responsibility this spec consumes as a gate input. |
| `src/ccp/sidecars/skia-renderer/` | Sidecar boundary | Receives the approved arc-governed render manifest. This spec defines the contract and queue semantics for that directory boundary. |
| `main.py` | `src/ccp/api/main.py` | Registers new render routes and extends `/health` with arc-render dependency readiness. |
| `receipt_chain.py` | `src/ccp/core/receipt_chain.py` | Logs plan generation, first-frame verdicts, sidecar launch, gate rejection, regeneration, and release decisions. |
| `circuit_breaker.py` | `src/ccp/core/circuit_breaker.py` | Blocks full pipeline execution when first-frame authority or Epic Meaning gate fails. |
| `setup_supabase.py` | `src/ccp/scripts/setup_supabase.py` | Adds durable tables for render jobs, cluster plans, gate results, first-frame checks, and manifests. |

**Existing models and rules reused directly:**

- `GateC09Result` for Abel-side visual-planning validation
- `UNIVERSAL_ANTI_GENERIC` for baseline anti-generic constraints
- `ENEMY_ANTI_PATTERNS["corporate blandness"]` as a named rejection source for M-02
- `CompositionStatus` and approval flow from `CanvasCompositionService`

**New API routes introduced by this spec:**

- `POST /api/cmf/arc-render/jobs`
- `GET /api/cmf/arc-render/jobs/{job_id}`
- `POST /api/cmf/arc-render/jobs/{job_id}/retry-first-frame`
- `POST /api/cmf/arc-render/jobs/{job_id}/request-regeneration`
- `POST /api/cmf/arc-render/jobs/{job_id}/release`
- `GET /api/cmf/arc-render/health`

**New persistence tables introduced by this spec:**

- `cmf_arc_render_jobs`
- `cmf_beat_cluster_plans`
- `cmf_first_frame_checks`
- `cmf_epic_meaning_gate_results`
- `cmf_render_manifests`
<!-- UPDATED: SDA representation-drift gate results table added -->
- `cmf_representation_drift_results`

### 3.3 ADR-05 Primitives

| Primitive ID | Name | Family | Constraint Applied |
|---|---|---|---|
| `EXP-TRS-004` | Epic Meaning Framing (The Crusade Narrative) | trust_branding | Governing primitive. Every artifact must feel like a movement-defining statement, not a corporate explainer. This drives lighting, shot grammar, sonic force, and release gating. |
| `EXP-PER-003` | Cumulative Investment | personalization_identity | Supporting primitive. Identity continuity, coach recognizability, and signature presence must persist across clusters through Identity LoRA and deterministic control bindings. |

### 3.4 CBAR Mandates

| Mandate | Story | Required Behavior | Implementation Mechanism |
|---|---|---|---|
| Phase4-M02 - The Cinematic Meaning Rule | Epic 2 Story 2.1 | The pipeline must translate Coalition Script Spine meaning into high-contrast, intense visual grammar and reject flat, bright, sterile, corporate renders before release. | `FirstFrameAuthorityGate` evaluates the first-frame plan before generation. `EpicMeaningGate` evaluates both plan-time and preview-time signals. `RepresentationDriftGate` evaluates whether render intensification has preserved or corrupted the source Invariant Field and Representation Geometry. `RenderReleaseGate` blocks release until all three gates pass. |

**M-02 anti-patterns explicitly forbidden:**

- flat, even lighting across all key frames
- pure white or sterile office backgrounds used as default visual environments
- symmetrical corporate-headshot composition as the first-frame pattern
- generic stock-music beds with no arc-specific tempo or silence logic
- visual pacing that ignores Beat Cluster shifts and cuts on arbitrary intervals
- releasing a render because it is technically complete even though it fails Crusade intensity
<!-- UPDATED: SDA representation-geometry anti-patterns added -->

**SDA representation-geometry anti-patterns explicitly forbidden (v1.1):**

These anti-patterns differ from the aesthetic anti-patterns above. They catch renders that are visually premium but semantically corrupt:

- transforming earned authority into coercive authority through visual power coding (dark thrones, dominance framing, submission-implying camera angles)
- inflating genuine vulnerability into spectacle vulnerability through over-dramatic lighting, slow-motion tears, or emotional exploitation framing
- converting authentic belonging into cultic belonging through exclusionary visual language, in-group prestige cues, or fear-weighted loyalty signaling
- replacing authentic transcendence with prestige theater through luxury aesthetics, status signaling, or aspirational lifestyle imagery disconnected from the source truth
- flattening symbolic density into generic epicness by substituting source-specific metaphors with stock cinematic tropes (epic sunsets, mountain summits, soaring eagles)
- silently raising fear weighting in sonic choices through manipulative urgency, artificial scarcity cues, or anxiety-inducing sound design not present in the source invariant field
- using hard-negative-adjacent visual or sonic patterns that pass aesthetic quality but distort the directional integrity of the source meaning

### 3.5 Technical Decisions

| Decision | Choice | Why |
|---|---|---|
| Beat unit | Beat Clusters are first-class persisted artifacts | PRD-03 says they are the bridge between meaning and media construction. |
| First gate timing | First Frame Composer check runs before full render | Prompt and Epic 2 both require it as a mandatory pre-render gate. |
| Release gate | Two-stage gate: plan-time then preview-time | Some failures are obvious from the plan; others only appear in the first-frame preview. |
| Sidecar handoff | File-backed deterministic manifest | The Skia sidecar boundary exists as a render-execution layer; a manifest preserves determinism and auditability. |
| Abel integration | Augment input, do not fork generator | `generate(...)` already owns the VCB contract. |
| Canvas integration | Use composition and regeneration boundaries as-is | Existing composition lifecycle is already defined and auditable. |
| Preview strategy | Render first-frame preview and cluster-preview snapshots before full export | This catches corporate-aesthetic drift early and cheaply. |
| Format governance dependency | Consume selected format rather than recalculate it | `FormatGovernanceEngine` already governs format allocation. |
<!-- UPDATED: SDA representation-geometry technical decisions added -->
| Representation drift gate | `RepresentationDriftGate` runs after `EpicMeaningGate` as a third gate layer | Aesthetic gates catch ugly renders; the drift gate catches semantically corrupt but visually premium renders. These are architecturally different failure modes. |
| Symbolic density measurement | Compare source invariant field symbolic density against render-time symbolic density | PRD-03 §3.3A says CMF must interpret Invariant Gravity as a constraint on what symbolic exaggeration is permissible. Density preservation is that constraint made measurable. |
| Hard-negative adjacency | Check render visual/sonic choices against known SDA hard-negative patterns | SDA Content Engine §7 defines hard negatives as deceptively close failures. CMF must detect when a render is structurally adjacent to validity while corrupting trajectory. |
| Amplification vs corruption boundary | CMF is allowed to intensify and symbolize, but not to silently mutate invariant gravity | PRD-03 §3.3A explicitly states this. The gate must distinguish premium intensification from semantic corruption. |

## 4. Plan

### Phase 1 - Models and Persistence

| Task # | Task | Output |
|---|---|---|
| 1 | Create `src/ccp/models/cmf_arc_render_models.py` | Pydantic v2 models for clusters, gates, manifests, jobs, and release results |
| 2 | Extend `src/ccp/scripts/setup_supabase.py` | New tables, indexes, status enums, and uniqueness constraints |
| 3 | Add repository helpers | SQL read/write layer for jobs, cluster plans, first-frame checks, and gate results |

### Phase 2 - Narrative-to-Render Planning

| Task # | Task | Output |
|---|---|---|
| 4 | Implement `NarrativeRenderingModel` | Coalition Script Spine to Beat Cluster plan transformation |
| 5 | Implement `BeatClusterPlanner` | Cluster shot grammar, cluster durations, transition style, and tempo curves |
| 6 | Implement `OmniShotBoundaryPlanner` | Shot-boundary-aware transition and boundary window planning |
| 7 | Implement `ArcSonicBedPlanner` | Sonic intensity, silence windows, and tempo map per cluster |
| 8 | Implement `ArcGovernedVCBAugmentor` | Cluster-enriched `VCBGenerationInput` before Abel invocation |

### Phase 3 - Deterministic Controls and Gates

| Task # | Task | Output |
|---|---|---|
| 9 | Implement `DeterministicControlResolver` | First Frame, pose, expression, and LoRA bindings |
| 10 | Implement `FirstFrameAuthorityGate` | Mandatory scroll-stop authority validation before render |
| 11 | Implement `EpicMeaningGate` | Corporate-aesthetic rejection logic at plan-time and preview-time |
| 12 | Implement `RenderReleaseGate` | Blocks full render release until both gates pass |

<!-- UPDATED: SDA representation-geometry implementation phase added -->
### Phase 4 - SDA Representation Geometry Governance

| Task # | Task | Output |
|---|---|---|
| 13 | Implement `SymbolicDensityPreserver` | Measurement logic for pre- vs post-render symbolic density |
| 14 | Implement `HardNegativeAdjacencyChecker` | Contrastive evaluation against SDA hard-negative definitions |
| 15 | Implement `RepresentationDriftGate` | Pre-release validation blocking semantic corruption |

### Phase 5 - Sidecar and Composition Execution

| Task # | Task | Output |
|---|---|---|
| 16 | Implement `SkiaRenderManifestBuilder` | Deterministic sidecar manifest file generation |
| 17 | Implement `SkiaRenderSidecarBridge` | Sidecar job submission, polling, and preview artifact retrieval |
| 18 | Integrate `CanvasCompositionService` | Approved render output to composition assembly and release |

### Phase 6 - API and Verification

| Task # | Task | Output |
|---|---|---|
| 16 | Add FastAPI router module | Create/get/retry/regenerate/release routes |
| 17 | Register routes and health check | `main.py` integration and dependency readiness |
| 18 | Add receipt-chain events | Full stage-by-stage auditability |
| 19 | Add unit tests | Planning, gate logic, and manifest structure verification |
| 20 | Add integration tests | M-02 enforcement and sidecar/composition flow verification |

## 5. Schema

**New model file:** `src/ccp/models/cmf_arc_render_models.py`

```python
from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class BeatClusterType(str, Enum):
    rally = "rally"
    witness = "witness"
    reflection = "reflection"
    confrontation = "confrontation"


class ShotGrammarProfile(str, Enum):
    kinetic_escalation = "kinetic_escalation"
    intimate_observation = "intimate_observation"
    contemplative_pause = "contemplative_pause"
    pressure_lock = "pressure_lock"


class FirstFrameVerdict(str, Enum):
    pass_ = "PASS"
    fail = "FAIL"
    escalate = "ESCALATE"


class EpicMeaningVerdict(str, Enum):
    pass_ = "PASS"
    fail_flat_lighting = "FAIL_FLAT_LIGHTING"
    fail_corporate_aesthetic = "FAIL_CORPORATE_AESTHETIC"
    fail_generic_sonic_bed = "FAIL_GENERIC_SONIC_BED"
    fail_first_frame_weak = "FAIL_FIRST_FRAME_WEAK"


class ArcRenderJobStatus(str, Enum):
    planned = "planned"
    first_frame_blocked = "first_frame_blocked"
    preview_rendering = "preview_rendering"
    preview_failed = "preview_failed"
    full_rendering = "full_rendering"
    ready_for_composition = "ready_for_composition"
    representation_drift_blocked = "representation_drift_blocked"
    released = "released"
    failed = "failed"


class TempoEnvelope(BaseModel):
    bpm_start: int = Field(..., ge=40, le=220)
    bpm_peak: int = Field(..., ge=40, le=220)
    bpm_end: int = Field(..., ge=40, le=220)
    silence_windows_ms: list[int] = Field(default_factory=list)


class ClusterShotDirective(BaseModel):
    camera_distance: str = Field(..., min_length=1, max_length=80)
    lighting_profile: str = Field(..., min_length=1, max_length=120)
    movement_profile: str = Field(..., min_length=1, max_length=120)
    transition_profile: str = Field(..., min_length=1, max_length=120)
    symbolic_environment: str = Field(..., min_length=1, max_length=160)


class DeterministicControlSpec(BaseModel):
    first_frame_spec_id: str = Field(..., min_length=1)
    conscious_pose_id: str = Field(..., min_length=1)
    conscious_smile_preset: str = Field(..., min_length=1)
    identity_lora_path: str = Field(..., min_length=1)
    gaze_rule: str = Field(..., min_length=1, max_length=120)


class BeatClusterPlan(BaseModel):
    cluster_id: str = Field(..., min_length=1)
    cluster_type: BeatClusterType
    order_index: int = Field(..., ge=0)
    start_ms: int = Field(..., ge=0)
    end_ms: int = Field(..., ge=1)
    shot_grammar: ShotGrammarProfile
    shot_directive: ClusterShotDirective
    tempo_envelope: TempoEnvelope
    deterministic_controls: DeterministicControlSpec
    narrative_purpose: str = Field(..., min_length=8, max_length=280)


class FirstFrameAuthorityCheck(BaseModel):
    check_id: str = Field(..., min_length=1)
    cluster_id: str = Field(..., min_length=1)
    verdict: FirstFrameVerdict
    authority_score: float = Field(..., ge=0.0, le=1.0)
    contrast_score: float = Field(..., ge=0.0, le=1.0)
    recognizability_score: float = Field(..., ge=0.0, le=1.0)
    anti_generic_flags: list[str] = Field(default_factory=list)
    checked_at: datetime


class EpicMeaningGateResult(BaseModel):
    gate_id: str = Field(..., min_length=1)
    job_id: str = Field(..., min_length=1)
    verdict: EpicMeaningVerdict
    failed_rules: list[str] = Field(default_factory=list)
    rationale: str = Field(..., min_length=8, max_length=400)
    checked_at: datetime


class RepresentationDriftVerdict(str, Enum):
    pass_ = "PASS"
    fail_symbolic_collapse = "FAIL_SYMBOLIC_COLLAPSE"
    fail_prestige_inflation = "FAIL_PRESTIGE_INFLATION"
    fail_coercive_coding = "FAIL_COERCIVE_CODING"
    fail_hard_negative_match = "FAIL_HARD_NEGATIVE_MATCH"


class RepresentationDriftGateResult(BaseModel):
    gate_id: str = Field(..., min_length=1)
    job_id: str = Field(..., min_length=1)
    verdict: RepresentationDriftVerdict
    source_symbolic_density: float = Field(..., ge=0.0, le=1.0)
    render_symbolic_density: float = Field(..., ge=0.0, le=1.0)
    detected_drifts: list[str] = Field(default_factory=list)
    rationale: str = Field(..., min_length=8, max_length=400)
    checked_at: datetime


class CoalitionSpineInput(BaseModel):
    content_output_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    coach_acronym: str = Field(..., min_length=2, max_length=4)
    selected_format: str = Field(..., min_length=1, max_length=80)
    spine_text: str = Field(..., min_length=20)
    somatic_arc_type: str = Field(..., min_length=1, max_length=80)
    voice_dna_id: str = Field(..., min_length=1)


class ArcRenderManifest(BaseModel):
    manifest_id: str = Field(..., min_length=1)
    job_id: str = Field(..., min_length=1)
    content_output_id: str = Field(..., min_length=1)
    selected_format: str = Field(..., min_length=1, max_length=80)
    vcb_id: str = Field(..., min_length=1)
    beat_clusters: list[BeatClusterPlan] = Field(..., min_length=1)
    preview_image_paths: list[str] = Field(default_factory=list)
    render_target_path: str = Field(..., min_length=1)
    created_at: datetime


class ArcRenderJobRecord(BaseModel):
    job_id: str = Field(..., min_length=1)
    content_output_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    status: ArcRenderJobStatus
    selected_format: str = Field(..., min_length=1, max_length=80)
    beat_clusters: list[BeatClusterPlan] = Field(default_factory=list)
    first_frame_check: FirstFrameAuthorityCheck | None = None
    epic_meaning_gate: EpicMeaningGateResult | None = None
    representation_drift_gate: RepresentationDriftGateResult | None = None
    manifest_id: str = Field(default="", max_length=120)
    composition_id: str = Field(default="", max_length=120)
    created_at: datetime
    updated_at: datetime


class ArcRenderCreateRequest(BaseModel):
    coalition_spine: CoalitionSpineInput


class ArcRenderReleaseResult(BaseModel):
    job_id: str = Field(..., min_length=1)
    composition_id: str = Field(..., min_length=1)
    release_receipt_id: str = Field(..., min_length=1)
    released_at: datetime
```

**Supabase tables to add in `setup_supabase.py`:**

| Table | Key Columns | Constraints |
|---|---|---|
| `cmf_arc_render_jobs` | `job_id`, `content_output_id`, `coach_id`, `selected_format`, `status`, `manifest_id`, `composition_id`, `created_at`, `updated_at` | unique(`content_output_id`, `selected_format`), index on `coach_id`, index on `status` |
| `cmf_beat_cluster_plans` | `cluster_id`, `job_id`, `cluster_type`, `order_index`, `start_ms`, `end_ms`, `shot_grammar`, `cluster_json` | unique(`job_id`, `order_index`), check `end_ms > start_ms`, index on `job_id` |
| `cmf_first_frame_checks` | `check_id`, `job_id`, `cluster_id`, `verdict`, `authority_score`, `contrast_score`, `recognizability_score`, `anti_generic_flags`, `checked_at` | unique(`job_id`, `cluster_id`), index on `verdict` |
| `cmf_epic_meaning_gate_results` | `gate_id`, `job_id`, `verdict`, `failed_rules`, `rationale`, `checked_at` | unique(`job_id`), index on `verdict` |
| `cmf_representation_drift_results` | `gate_id`, `job_id`, `verdict`, `source_symbolic_density`, `render_symbolic_density`, `detected_drifts`, `checked_at` | unique(`job_id`), index on `verdict` |
| `cmf_render_manifests` | `manifest_id`, `job_id`, `vcb_id`, `render_target_path`, `manifest_json`, `created_at` | unique(`job_id`), index on `vcb_id` |

**New route contracts:**

- `POST /api/cmf/arc-render/jobs` accepts `ArcRenderCreateRequest` and returns `ArcRenderJobRecord`
- `GET /api/cmf/arc-render/jobs/{job_id}` returns `ArcRenderJobRecord`
- `POST /api/cmf/arc-render/jobs/{job_id}/retry-first-frame` re-runs `FirstFrameAuthorityGate` after deterministic control adjustment
- `POST /api/cmf/arc-render/jobs/{job_id}/request-regeneration` triggers targeted cluster regeneration through existing composition and render boundaries
- `POST /api/cmf/arc-render/jobs/{job_id}/release` returns `ArcRenderReleaseResult`

**Required gate rules:**

| Gate | Rule | Failure Result |
|---|---|---|
| `FirstFrameAuthorityGate` | `authority_score >= 0.72` and `contrast_score >= 0.65` and `recognizability_score >= 0.70` | job status `first_frame_blocked` |
| `FirstFrameAuthorityGate` | no anti-generic flag may contain `corporate aesthetics`, `sterile lighting`, or `posed expressions` | job status `first_frame_blocked` |
| `EpicMeaningGate` | preview must not resemble `corporate blandness` anti-patterns | job status `preview_failed` |
| `EpicMeaningGate` | sonic bed must include cluster-specific tempo envelope or intentional silence windows | job status `preview_failed` |
| `RepresentationDriftGate` | render visual/sonic choices must not match SDA hard-negative profiles | job status `representation_drift_blocked` |
| `RepresentationDriftGate` | absolute difference between `source_symbolic_density` and `render_symbolic_density` must be < 0.25 | job status `representation_drift_blocked` |
| `RenderReleaseGate` | `FirstFrameAuthorityGate`, `EpicMeaningGate`, and `RepresentationDriftGate` must all pass | release denied with 409 |

**Render state machine:**

| Current State | Event | Next State | Allowed |
|---|---|---|---|
| `planned` | first-frame gate pass | `preview_rendering` | yes |
| `planned` | first-frame gate fail | `first_frame_blocked` | yes |
| `first_frame_blocked` | retry-first-frame pass | `preview_rendering` | yes |
| `preview_rendering` | Epic Meaning gate fail | `preview_failed` | yes |
| `preview_rendering` | Epic Meaning gate pass | `full_rendering` | yes |
| `preview_failed` | regeneration requested | `preview_rendering` | yes |
| `full_rendering` | render + composition complete | `ready_for_composition` | yes |
| `ready_for_composition` | drift gate fail | `representation_drift_blocked` | yes |
| `ready_for_composition` | drift gate pass + release | `released` | yes |
| `ready_for_composition` | release without gate pass | `failed` | no - reject |

## 6. Fallback

| Failure | Detection | Pipeline Behavior | System Action |
|---|---|---|---|
| Abel VCB generation fails | `generate(...)` raises or returns invalid Gate C-09 result | stop before sidecar handoff | write failure receipt, mark job `failed` |
| First frame is weak | `FirstFrameAuthorityGate` fails thresholds | full render never starts | mark `first_frame_blocked`, persist anti-generic flags |
| Preview looks corporate | `EpicMeaningGate` fails | block full render release | mark `preview_failed`, require regeneration or control adjustment |
<!-- UPDATED: SDA drift gate fallback added -->
| Render mutates meaning | `RepresentationDriftGate` fails hard-negative or density checks | block release of visually successful render | mark `representation_drift_blocked`, flag specific semantic corruption |
| Skia sidecar unavailable | sidecar path missing or manifest execution timeout | do not mark job render-complete | keep job `failed` or retryable depending on timeout class |
| Cluster-specific preview drift | one cluster fails but others pass | allow targeted regeneration, not full pipeline reset | use cluster-level revision note and rerender request |
| Composition approval not reached | render assets exist but composition not approved | artifact remains internal | no external release path is opened |

**Hard-stop rules:**

- No full render may start if the first-frame authority check fails.
- No artifact may be released if the Epic Meaning gate fails even once on the latest preview.
<!-- UPDATED: SDA release gate rule added -->
- No artifact may be released if the Representation Drift gate detects a hard-negative adjacency or unallowable symbolic density collapse.
- No fallback may substitute generic stock music to satisfy a missing sonic plan.
- No fallback may downgrade to generic montage timing when cluster timing cannot be resolved.

## 7. Tasks

1. Create [src/ccp/models/cmf_arc_render_models.py](D:/Work/The Conscious Coaching Factory/src/ccp/models/cmf_arc_render_models.py) with the job, cluster, gate, and manifest models from Section 5.
2. Extend [src/ccp/scripts/setup_supabase.py](D:/Work/The Conscious Coaching Factory/src/ccp/scripts/setup_supabase.py) with the five new tables and indexes.
3. Add `ArcRenderRepository` in [src/ccp/services/](D:/Work/The Conscious Coaching Factory/src/ccp/services/) for job, cluster, gate, and manifest persistence.
4. Add `NarrativeRenderingModel` to translate Coalition Script Spine inputs into typed Beat Cluster plans.
5. Add `BeatClusterPlanner` to generate cluster ordering, shot grammar, and duration envelopes.
6. Add `OmniShotBoundaryPlanner` to compute cluster-aligned cut windows and prevent arbitrary montage timing.
7. Add `ArcSonicBedPlanner` to generate tempo maps and silence windows per cluster.
8. Add `ArcGovernedVCBAugmentor` to enrich `VCBGenerationInput` before calling Abel.
9. Add `DeterministicControlResolver` to bind First Frame, ConsciousPose, ConsciousSmile, and Identity LoRA directives.
10. Add `FirstFrameAuthorityGate` to score authority, contrast, recognizability, and anti-generic violations before render.
11. Add `EpicMeaningGate` to inspect preview outputs and reject corporate-aesthetic artifacts.
<!-- UPDATED: SDA representation-geometry tasks added and subsequent tasks renumbered -->
12. Add `SymbolicDensityPreserver` to calculate semantic magnitude delta before and after rendering.
13. Add `HardNegativeAdjacencyChecker` to evaluate render choices against SDA known-corruption patterns.
14. Add `RepresentationDriftGate` to run density and adjacency checks as a mandatory pre-release layer.
15. Add `SkiaRenderManifestBuilder` to serialize approved plans into a sidecar manifest.
16. Add `SkiaRenderSidecarBridge` to submit sidecar jobs and poll preview/full-render status.
17. Integrate [src/ccp/services/canvas_composition_service.py](D:/Work/The Conscious Coaching Factory/src/ccp/services/canvas_composition_service.py) for composition creation, regeneration, and approval handoff.
18. Add a new FastAPI router module under [src/ccp/api/](D:/Work/The Conscious Coaching Factory/src/ccp/api/) for render job lifecycle endpoints.
19. Register the router and health readiness checks in [src/ccp/api/main.py](D:/Work/The Conscious Coaching Factory/src/ccp/api/main.py).
20. Extend [src/ccp/core/receipt_chain.py](D:/Work/The Conscious Coaching Factory/src/ccp/core/receipt_chain.py) integration calls for every gate and release transition.
21. Add unit tests for cluster planning, first-frame gating, Epic Meaning gate, and Representation Drift gate rule evaluation.
22. Add integration tests for blocked-first-frame jobs, preview rejection, semantic corruption rejection, cluster regeneration, and release handoff.

## 8. Acceptance Criteria

### Story 2.1 - Narrative Geometry Translation

**AC1 - Beat Cluster Translation**

- Given a Coalition Script Spine from CCF
- When it enters the Narrative Rendering Model
- Then the pipeline produces explicit Beat Clusters with ordered cluster types and per-cluster shot grammar
- And the cluster set must include arc-appropriate pacing directives for Rally, Witness, Reflection, or Confrontation rather than a generic montage template

**AC2 - Deterministic Control Layer Enforcement**

- Given a Beat Cluster plan exists
- When deterministic controls are resolved
- Then each cluster carries First Frame, ConsciousPose, ConsciousSmile, and Identity LoRA directives
- And no cluster may proceed to preview rendering without a valid deterministic control spec

**AC3 - Mandatory First Frame Gate**

- Given a render job is created
- When the first-frame authority check runs
- Then the full render path remains blocked until the first-frame plan passes authority, contrast, and recognizability thresholds
- And any detected `corporate aesthetics` or `sterile lighting` anti-generic flag forces `first_frame_blocked`

**AC4 - Epic Meaning Gate**

- Given a first-frame preview or cluster preview is available
- When the Epic Meaning gate evaluates the output
- Then the gate rejects flat, brightly lit, corporate-aesthetic renders
- And the job cannot move to release until the latest preview passes

**AC5 - Sonic Arc Integrity**

- Given Beat Clusters define the render plan
- When the sonic bed is assigned
- Then the tempo and silence treatment align to cluster type and arc intensity
- And generic stock-bed fallback without cluster-specific tempo logic is forbidden

**AC6 - Release Requires Gate Compliance**

- Given the sidecar completes rendering and composition assets exist
- When release is requested
- Then release succeeds only if the first-frame gate, Epic Meaning gate, and Representation Drift gate all passed on the latest version
- And the release decision is written to `receipt_chain`

<!-- UPDATED: SDA representation-geometry ACs added -->
**AC7 - Symbolic Density Preservation**

- Given a render plan creates intense visual or sonic amplification
- When the `SymbolicDensityPreserver` compares source to render
- Then the absolute delta between source symbolic density and render symbolic density must be < 0.25
- And any collapse into generic epicness or inflation into prestige theater forces `representation_drift_blocked`

**AC8 - Hard-Negative Adjacency Defense**

- Given a completed preview or render artifact
- When the `HardNegativeAdjacencyChecker` evaluates the output
- Then any structural match against defined SDA hard-negative profiles (fake epicness, coercive aspiration, cultic belonging) triggers a fail
- And the artifact is blocked from release even if it passes all aesthetic quality thresholds

**Failure Example**

- A coach records a passionate defense of their category.
- The pipeline creates a technically valid render with even office lighting, a centered smiling headshot, symmetrical layout, and generic royalty-free background music.
- The composition exports successfully and the artifact is marked ready without any first-frame or Epic Meaning rejection.
- This is a spec failure. It violates Story 2.1, Phase4-M02, `EXP-TRS-004`, and the specific CBAR rejection of bland corporate SaaS rendering.
<!-- UPDATED: SDA failure example added -->
- Alternatively, the pipeline creates a highly cinematic, dramatic render with heavy shadows, soaring trailer music, and a dominating low-angle shot. It looks extremely premium, but it has mutated the coach's genuine vulnerability into a power-signaling prestige trope. It passes the Epic Meaning Gate, but fails the `RepresentationDriftGate` for Hard-Negative Adjacency. The system incorrectly releases it because the third gate was ignored. This is also a spec failure.

**Mandate Proof**

- Phase4-M02 is satisfied only if the pipeline can block execution before full render on first-frame weakness and block release after preview on Epic Meaning failure.
- SDA PRD-03 §3.3A is satisfied only if the pipeline blocks release when semantic direction has been mutated, proving that premium rendering is completely decoupled from representation drift.
- Merely adding cinematic language to prompt text without an enforced gate is not compliance.

## 9. Dependencies

| Dependency | Type | Why It Matters |
|---|---|---|
| `src/ccp/services/abel_vcb_generator.py` | Existing service | Canonical VCB generation contract and Gate C-09 planner |
| `src/ccp/services/canvas_composition_service.py` | Existing service | Existing composition assembly, regeneration, and approval boundary |
| `src/ccp/services/format_governance_engine.py` | Existing service | Supplies upstream format-selection outcomes so rendering does not re-solve format eligibility |
| `src/ccp/models/visual_engine_models.py` | Existing models | Existing anti-generic constraints, arc types, and VCB-related models |
| `docs/architecture/FR-VIS-16_First_Frame_Composer_Tech_Spec.md` | Existing architecture contract | Defines the first-frame responsibility consumed by the new gate |
| `src/ccp/sidecars/skia-renderer/` | Sidecar execution boundary | Required execution target for manifest-based rendering |
| `src/ccp/api/main.py` | Existing API gateway | Router registration and health check extension point |
| `src/ccp/scripts/setup_supabase.py` | Existing schema bootstrap | Durable job, gate, and manifest persistence |
| `src/ccp/core/receipt_chain.py` | Cross-system infrastructure | Immutable stage-by-stage rendering audit trail |
| `src/ccp/core/circuit_breaker.py` | Cross-system infrastructure | Hard-stop protection when quality or integrity gates fail |
| Upstream Coalition Script Spine emission | Upstream content dependency | The pipeline cannot start without a valid meaning artifact from CCF |
<!-- UPDATED: SDA documentation dependencies added -->
| `semantic_discernment_architecture_content_engine_v_1.md` | Core Architecture Rulebook | Defines Hard Negatives and Symbolic Density requirements for gates |
| `semantic_discernment_architecture_artifact_taxonomy_v_1.md` | Core Architecture Taxonomy | Defines the canonical ontology for Representation Geometry |
| `Perceptual_Primitives_Architecture.md` | Architecture Ruleset | Law 7 Anti-centroid law mandates protection of charge |
| `Matrix of Edging.md` | Architecture Ruleset | Section 12 Anti-Centroid Doctrine dictates tension vs delivery separation |

## 10. Testing Strategy

### Unit Tests

| Test Name | File | What It Verifies |
|---|---|---|
| `test_beat_cluster_planner_assigns_distinct_shot_grammar_per_arc` | `tests/unit/test_cmf_arc_governed_rendering.py` | Rally, Witness, Reflection, and Confrontation plans do not collapse into one generic timing profile |
| `test_first_frame_authority_gate_blocks_corporate_aesthetic_plan` | `tests/unit/test_cmf_arc_governed_rendering.py` | `FirstFrameAuthorityGate` rejects sterile-lighting and corporate-aesthetic anti-generic flags |
| `test_epic_meaning_gate_rejects_flat_preview_even_when_render_is_complete` | `tests/unit/test_cmf_arc_governed_rendering.py` | a technically complete preview can still fail M-02 |
| `test_manifest_builder_preserves_cluster_order_and_control_specs` | `tests/unit/test_cmf_arc_governed_rendering.py` | sidecar manifest serialization keeps deterministic ordering and control bindings |
<!-- UPDATED: SDA representation-geometry unit tests added -->
| `test_representation_drift_gate_rejects_hard_negative_match` | `tests/unit/test_cmf_arc_governed_rendering.py` | verifies hard-negative adjacency triggers block even if lighting/aesthetic is premium |
| `test_symbolic_density_preserver_flags_collapse` | `tests/unit/test_cmf_arc_governed_rendering.py` | verifies a delta > 0.25 between source and render density triggers semantic block |

### Integration Tests

| Test Name | File | What It Verifies |
|---|---|---|
| `test_arc_render_job_stops_before_full_render_when_first_frame_gate_fails` | `tests/integration/test_fr_era3_12_cmf_arc_governed_rendering.py` | M-02 pre-render gate enforcement |
| `test_preview_rejection_blocks_release_for_corporate_aesthetic_output` | `tests/integration/test_fr_era3_12_cmf_arc_governed_rendering.py` | preview-time Epic Meaning rejection blocks release despite technical completion |
| `test_cluster_regeneration_retries_only_failed_cluster_not_entire_job` | `tests/integration/test_fr_era3_12_cmf_arc_governed_rendering.py` | scoped rerender behavior for failed cluster previews |
| `test_release_handoff_creates_canvas_composition_after_triple_gate_pass` | `tests/integration/test_fr_era3_12_cmf_arc_governed_rendering.py` | successful job flows into `CanvasCompositionService` only after all three gates pass |
<!-- UPDATED: SDA semantic corruption integration test added -->
| `test_release_blocked_by_semantic_corruption_despite_premium_aesthetic` | `tests/integration/test_fr_era3_12_cmf_arc_governed_rendering.py` | representation drift rules can block a visually premium release |

### Test Pattern Notes

- Follow the helper-driven structure used in `test_cpsc_fr52_webinar_brief.py`.
- Follow the explicit status and field assertion style used in `test_ca11_fr16_studio_block.py`.
- Assert concrete `job.status`, `verdict`, `failed_rules`, `cluster_type`, and `receipt action` values rather than only checking response codes.
- Include one direct assertion that `UNIVERSAL_ANTI_GENERIC` or the corporate-blandness anti-pattern text triggered the rejection path.

### Minimum Verification Bar Before Merge

- all unit tests in the new arc-render module pass
- all new integration tests pass
- at least one integration test proves a job is blocked before full render on first-frame failure
- at least one integration test proves a completed preview is still blocked from release on M-02 failure
<!-- UPDATED: SDA semantic corruption merge verification added -->
- at least one integration test proves a visually premium but semantically corrupt preview is blocked from release
- health checks report Skia sidecar, Abel, and Canvas dependencies clearly
