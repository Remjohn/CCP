# Tech-Spec: FR-ERA3-09 - Conscious Editor Mini App
**Created:** 2026-05-11
**Status:** Ready for Development
**Version:** 1.0 (ERA3 - CBAR-Hardened)
**Phase:** 3 - Experience Mini Apps
**Architecture Reference:** ERA3_Tech_Spec_Writing_Protocol.md Section 7

## Pre-Work Log

<!-- UPDATED: Added Wave 0 SDA grounding and exact proof of where baseline review stops short of semantic-direction drift analysis. -->

```
1. PROTOCOL LOADED:   Section 2.2 confirms new Mini App routes extend `src/ccp/api/main.py`, Section 2.3 confirms
                      Supabase tables extend `src/ccp/scripts/setup_supabase.py`, Section 5.3 reserves
                      `startapp=editor` for the Conscious Editor Mini App, and the protocol requires CBAR
                      mandates to be made explicit rather than implied.
2. PRD LOADED:        PRD-02 exact architecture definition: "CCF does not write from nothing. It compiles from
                      activated truth." Brownfield requirement: "Enforce the Trigger-First execution flow
                      (signal -> provocation -> reaction -> primitive distillation -> compilation) across all
                      content pipelines, physically preventing blank-page generative 'prompting'." PRD-02 also
                      states: "Elevate Archetypes (e.g., Achievement Story, Myth Debunk, Observational Humor)
                      into first-class runtime containers. The compiler must structure the meaning into these
                      archetypes before any downstream media format (carousel, video) is selected."
                      PRD-03 exact architecture definition: "The Conscious Media Factory is the visual and sonic
                      rendering arm of CCP. It does not decide what the coach means. It decides how that meaning
                      becomes perceptible..." and "CCF compiles the meaning. CMF renders the felt experience of
                      that meaning." PRD-03 also marks `[OBSOLETE] Coach-Facing CMF Editor (FR-VID-10)` for
                      removal under the Two-Touchpoint Discipline.
3. EPIC LOADED:       Phase 3 Epic 3 exact FR line: "FR-ERA3-09 (Conscious Editor): The backstage artifact
                      compiler enforcing Trigger-First Execution, Archetype Container Routing, and Operator Review
                      for CMF media validation." Story 3.1 first AC: "Given I have recorded a reaction or
                      coaching voice note, When the CCF meaning compiler finishes processing, Then I am presented
                      with the semantic artifact, structured into its Archetype Container (e.g., Myth Debunk,
                      Achievement Story), before any visual format is applied." Story 3.2 adds side-by-side
                      editable transcript review plus caption-only rerender without audio re-record or NIM re-run.
4. CBAR LOADED:       Phase3-M05 confirmed from the Phase 3 audit. Exact rewrite demand: "The Conscious Editor
                      MUST allow the coach to manually edit the raw JSON/text transcript layer in the browser
                      without having to re-record the audio or re-run the heavy biometric NIM pipeline." The
                      hallucination purge also corrects `EXP-SAF-002` from the false label "Sovereign Control" to
                      the real registry name "Possible-Win Scarcity".
5. PRIMITIVES:        `experience_primitive_id: "EXP-PER-003"` / `canonical_name: "Cumulative Investment"`
                      `experience_primitive_id: "EXP-SAF-002"` / `canonical_name: "Possible-Win Scarcity"`
6. BACKEND:           `src/ccp/services/content_machine.py` - `async def process_session(self, session_report: dict[str, Any], coach_id: str, coach_acronym: str = "CCH") -> ContentMachineResult`
                      `src/ccp/services/canvas_composition_service.py` - `def create_composition(self, vcb_id: str, template_id: str, slide_count: int, dimensions: dict[str, Any], handle_bar: dict[str, Any], text_content: dict[int, dict[str, str]] | None = None, content_output_id: str | None = None) -> CanvasComposition`
                      `src/ccp/services/canvas_composition_service.py` - `def request_regeneration(self, composition_id: str, slide_index: int, revision_note: str) -> tuple[CanvasComposition, RegenerationRequest]`
                      `src/ccp/services/abel_vcb_generator.py` - `def generate(self, inp: VCBGenerationInput) -> VisualCompositionBrief`
7. TESTS:             `tests/integration/test_cpsc_fr52_webinar_brief.py` and
                      `tests/integration/test_ca11_fr16_studio_block.py` both use typed fixtures, helper builders,
                      scenario-oriented test classes, direct field assertions, and local async wrappers instead of
                      generic smoke-test patterns.
8. EXISTING SPEC RE-READ: The exact baseline gap is in Section 2.2, which defines the second tier as `media_validation` for "CMF preview, transcript correction, slide-scoped recovery, and operator approval." That proves the current editor review stops at transcript/media validation and does not yet surface invariant loss, representation-geometry drift, archetypal incoherence, hard-negative adjacency, or directional-integrity flags.
9. WAVE 0 PRD RE-READ:
   - `PRD_02_CCF_Content_Factory.md` Wave 0 additions confirm the runtime now includes `directional integrity validation` after `archetype container` and before final JIT/render handoff.
   - `PRD_03_CMF_Media_Factory.md` Wave 0 additions confirm CMF must preserve active invariant field, admissible representation geometry, and downstream directional integrity rather than only rendering emotional intensity.
10. MANDATORY SDA SOURCE SET RE-READ:
   - `lab/semantic_discernment_architecture_content_engine_v_1.md`
   - `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md`
   - `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md`
   - `lab/CCP APRIL Updates/05_Core_Experience/Matrix of Edging.md`
11. SDA IMPLEMENTATION FR RE-READ:
   - `FR-ERA3-20_SDA_Ontology_And_Registry_Tech_Spec.md`
   - `FR-ERA3-21_SDA_Query_And_Crosswalk_Service_Tech_Spec.md`
   - `FR-ERA3-22_Directional_Integrity_Engine_Tech_Spec.md`
   These establish that the editor must consume SDA packets and reports; it must not become a new validator engine.
```

## 1. Files Read

| # | File | Version/Date | Purpose |
|---|---|---|---|
| 1 | `docs/architecture/april_updates/spec_prompts/P3_S17_FR-ERA3-09_Conscious_Editor.md` | 2026-05-11 | Assignment prompt, mandate framing, output target, and rerender-scope requirement |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Loaded 2026-05-11 | Mandatory stack, route, table, service, and CBAR formatting requirements |
| 3 | `docs/architecture/april_updates/Phase3_Experience_Mini_Apps_Epics.md` | 2026-05-10 | Epic 3 stories, AC, and M-05 wording |
| 4 | `docs/architecture/cbar_audits/CBAR_Audit_Phase3_Experience_Mini_Apps.md` | 2026-05-10 | CBAR rewrite requirement and hallucination purge corrections |
| 5 | `docs/prd/modules/PRD_02_CCF_Content_Factory.md` | v6.0, 2026-05-06 | Trigger-First doctrine, Archetype Container Routing, operator review, and artifact auditability |
| 6 | `docs/prd/modules/PRD_03_CMF_Media_Factory.md` | v6.0, 2026-05-06 | CMF rendering boundary, arc-governed media rules, deterministic control layer, and obsolete editor warning |
| 7 | `primitives/experience/personalization_identity/EXP-PER-003.yaml` | Codified registry | Verified primitive for cumulative ownership and export governance |
| 8 | `primitives/experience/safe_failure_recovery/EXP-SAF-002.yaml` | Codified registry | Verified primitive for modular recovery and non-catastrophic failure handling |
| 9 | `src/ccp/services/content_machine.py` | Existing service | Meaning compiler entrypoint and artifact emission boundary |
| 10 | `src/ccp/services/canvas_composition_service.py` | Existing service | Composition assembly, slide regeneration, export, and operator-approval boundary |
| 11 | `src/ccp/services/abel_vcb_generator.py` | Existing service | VCB generation boundary for visual prompt orchestration |
| 12 | `src/ccp/models/ca11_models.py` | Existing models | `SessionContentPiece`, `ContentMachineArray`, and `ContentMachineResult` shapes |
| 13 | `src/ccp/models/visual_engine_models.py` | Existing models | `VisualCompositionBrief`, `RegenerationRequest`, `CanvasComposition`, and composition status enums |
| 14 | `src/ccp/api/main.py` | 1.0.0 | FastAPI router registration and `/health` extension point |
| 15 | `src/ccp/core/receipt_chain.py` | Current | Immutable lineage and operator audit events |
| 16 | `src/ccp/core/circuit_breaker.py` | Current | Crisis halt and guarded fallback contract |
| 17 | `src/ccp/scripts/setup_supabase.py` | Current | Schema bootstrap extension point |
| 18 | `tests/integration/test_cpsc_fr52_webinar_brief.py` | Existing | Integration-test structure and receipt assertions |
| 19 | `tests/integration/test_ca11_fr16_studio_block.py` | Existing | Async scenario layout and schema-constant assertions |
| 20 | `lab/OmniShotCut Holistic Relational Shot Boundary.md` | Research note | Reference for shot-boundary-aware editor review and scoped media corrections |
| 21 | `lab/semantic_discernment_architecture_content_engine_v_1.md` | SDA source | Directional-integrity doctrine, representation geometry, and hard-negative review requirements |
| 22 | `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md` | SDA source | Canonical artifact roles for Directional Integrity Reports, Hard Negative Evaluation Reports, and review projections |
| 23 | `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md` | SDA source | Confirms editor must review emergent artifacts and edge products, not invent new primitive scoring |
| 24 | `lab/CCP APRIL Updates/05_Core_Experience/Matrix of Edging.md` | SDA source | Confirms edge products and broad signals are upstream; the editor only reviews resulting drift evidence |
| 25 | `docs/architecture/april_updates/FR-ERA3-20_SDA_Ontology_And_Registry_Tech_Spec.md` | Wave 1 SDA foundation | Canonical ontology / grammar lookup boundary |
| 26 | `docs/architecture/april_updates/FR-ERA3-21_SDA_Query_And_Crosswalk_Service_Tech_Spec.md` | Wave 1 SDA foundation | Canonical query / crosswalk access boundary |
| 27 | `docs/architecture/april_updates/FR-ERA3-22_Directional_Integrity_Engine_Tech_Spec.md` | Wave 1 SDA foundation | Validator output contract consumed by editor review mode |

## 2. Overview

<!-- UPDATED: Added SDA drift review as a projection layer while preserving artifact-first review and rerender boundaries. -->

### 2.1 Problem Statement

The repo now has strong upstream and downstream pieces, but it still lacks the backstage surface that connects them into a coach-usable review flow. `ContentMachinePipeline.process_session(...)` can compile meaning from authenticated voice evidence. `AbelVCBGenerator.generate(...)` can create a `VisualCompositionBrief`. `CanvasCompositionService` can assemble, regenerate, and export compositions. What does not yet exist is the operator surface that lets a coach inspect those artifacts in the right order and recover from minor CMF defects without catastrophic reruns.

That gap creates four failures:

- coaches can still be dropped into media review without first seeing the semantic artifact in its archetype container
- CMF review can drift into a generic editor experience that PRD-03 explicitly deprecates
- one typo in a caption can force an excessive recovery path if rerender scope is not formalized
- there is no explicit lineage chain proving that rendered media still points back to the original voice note rather than a fresh generative rewrite
- semantic-direction drift can remain invisible even when transcript and media technically match

Epic 3 is directly targeting those failures. Story 3.1 requires an archetype-first, no-blank-page artifact review tier. Story 3.2 requires a side-by-side transcript and media validation tier with scoped, possible-win recovery. The engineering challenge is not just UI. It is defining which layers can be reworked without invalidating upstream truth.

### 2.2 Solution

This spec introduces `startapp=editor` as the Conscious Editor Mini App. The Mini App is a backstage artifact compiler and operator review surface, not a new meaning engine, not a new scoring engine, and not a full CMF workstation. It consumes existing CCP services and adds missing orchestration and review layers:

- `EditorArtifactResolver` to load the semantic artifact before any visual format review
- `TranscriptRevisionManager` to persist coach-authored transcript corrections as a revision set rather than replacing source evidence
- `ScopedRerenderOrchestrator` to route changes into the smallest valid render scope
- `LineageAuditProjector` to expose a readable chain from source recording to export artifact
- `SdaDriftReviewProjector` to surface reviewer-visible invariant loss, representation-geometry drift, archetypal incoherence, hard-negative adjacency, and directional-integrity flags from upstream SDA reports
- `EditorSdaReportBridge` to consume `DirectionalIntegrityReport` and `HardNegativeEvaluationReport` outputs without recomputing them locally

The Conscious Editor is therefore a two-tier experience:

1. `artifact_review` tier for Trigger-First, archetype-container inspection
2. `media_validation` tier for CMF preview, transcript correction, reviewer-visible SDA drift review, slide-scoped recovery, and operator approval

### 2.3 Scope

**In scope:**

- `startapp=editor` Telegram Mini App scaffold and routing
- semantic artifact review before media review
- explicit archetype container projection using `ContentMachineResult.output`
- anti-centroid / coalition-signature warning projection when available in upstream artifacts
- reviewer-visible SDA drift projection when upstream reports are available
- side-by-side transcript JSON/text editor for Story 3.2
- rerender-scope taxonomy and deterministic routing logic
- caption-only rerender path with no audio re-record and no NIM rerun
- visual-only rerender path for slide or composition defects
- full lineage projection from source voice recording through CMF export
- receipt logging, health checks, and circuit-breaker fallback

**Out of scope:**

- replacing `content_machine.py` as the meaning compiler
- replacing `abel_vcb_generator.py` as the VCB generator
- replacing `canvas_composition_service.py` as the composition engine
- reviving the obsolete coach-facing CMF editor from PRD-03
- allowing arbitrary prompt-box authoring from blank state
- audio recapture UX beyond a final explicit `source_restart_required` escalation state
- downstream public publishing workflows beyond approval/export handoff
- recomputing SDA scores, invariant fields, or hard-negative evaluations inside the editor itself

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Component | Source FR | What It Does |
|---|---|---|---|
| DEP-CED-001 | `ConsciousEditorAppShell` | FR-ERA3-09 | Standalone Telegram Mini App loaded by `startapp=editor` |
| DEP-CED-002 | `EditorArtifactResolver` | Story 3.1 | Resolves one reviewable session into semantic, visual, and lineage payloads |
| DEP-CED-003 | `ArchetypeContainerProjection` | Story 3.1 | Projects compiled meaning into a coach-readable archetype-first artifact view |
| DEP-CED-004 | `ArtifactReadinessGate` | Story 3.1 | Blocks media review until semantic artifact exists and is source-linked |
| DEP-CED-005 | `TranscriptRevisionManager` | Story 3.2 / M-05 | Stores raw transcript revisions, diff metadata, author, and scope classification |
| DEP-CED-006 | `ScopedRerenderClassifier` | Story 3.2 / M-05 | Determines whether a requested change is caption-only, visual-only, composition-only, CMF-full, or source-restart |
| DEP-CED-007 | `ScopedRerenderOrchestrator` | Story 3.2 / M-05 | Executes the minimal valid rerender path against existing CCP services |
| DEP-CED-008 | `CompositionPatchAssembler` | Story 3.2 | Rebuilds caption/text overlays and composition text payloads without re-authoring meaning |
| DEP-CED-009 | `VisualRegenerationAdapter` | Story 3.2 | Bridges slide-specific visual changes into `request_regeneration(...)` |
| DEP-CED-010 | `LineageAuditProjector` | Story 3.2 | Produces source-to-export lineage for coach inspection and receipts |
| DEP-CED-011 | `OperatorReviewDecisionEngine` | Story 3.2 | Handles approve, edit-and-approve, regenerate, and escalate decisions |
| DEP-CED-012 | `ConsciousEditorApiBridge` | FR-ERA3-09 | Thin FastAPI route layer for session load, transcript patch, rerender, approval, and lineage reads |
| DEP-CED-013 | `ConsciousEditorAuditBridge` | FR-ERA3-09 | Logs revision, rerender, approval, failure, and escalation events to the Receipt Chain |
| DEP-CED-014 | `ShotBoundaryAssistProjection` | Story 3.2 | Optional shot-boundary hints for editors when a text issue maps to a specific segment or cut region |
| DEP-CED-015 | `EditorSdaReportBridge` | Wave 0 SDA adoption | Loads `DirectionalIntegrityReport`, `HardNegativeEvaluationReport`, and related SDA packets for a reviewable session without recalculating them |
| DEP-CED-016 | `SdaDriftReviewProjector` | P6_S48 update | Converts SDA reports into reviewer-visible invariant, geometry, archetype, hard-negative, and directional-integrity drift surfaces |
| DEP-CED-017 | `DriftAwareDecisionHints` | P6_S48 update | Translates consumed SDA drift signals into reviewer-facing rerender / escalate guidance while preserving human decision authority |

### 3.2 Existing Backend Integration

| File | Path | How This Spec Uses It |
|---|---|---|
| `content_machine.py` | `src/ccp/services/content_machine.py` | Consumes `ContentMachinePipeline.process_session(...)` outputs as the authoritative semantic artifact source. The editor never regenerates meaning from a blank text prompt. |
| `ca11_models.py` | `src/ccp/models/ca11_models.py` | Reuses `SessionContentPiece`, `ContentMachineArray`, `QueueStatus`, and `ContentMachineResult` as the canonical semantic artifact vocabulary. |
| `abel_vcb_generator.py` | `src/ccp/services/abel_vcb_generator.py` | Invokes `generate(...)` only when a change crosses the semantic-to-visual boundary and requires a new VCB. Transcript typo edits must not route here by default. |
| `visual_engine_models.py` | `src/ccp/models/visual_engine_models.py` | Reuses `VisualCompositionBrief`, `CanvasComposition`, `RegenerationRequest`, `CompositionStatus`, and `CanvasCompositionError` instead of inventing parallel editor-only models. |
| `canvas_composition_service.py` | `src/ccp/services/canvas_composition_service.py` | Uses `create_composition(...)` for text-layer rebuilds and composition reflow, `request_regeneration(...)` for visual-only slide recovery, and `approve(...)` / `edit_and_approve(...)` for operator completion. |
| `main.py` | `src/ccp/api/main.py` | Registers the Conscious Editor router and extends `/health` with editor readiness and dependencies state. |
| `receipt_chain.py` | `src/ccp/core/receipt_chain.py` | Writes immutable events for review load, transcript revision, rerender classification, rerender execution, approval, escalation, and fallback activation. |
| `circuit_breaker.py` | `src/ccp/core/circuit_breaker.py` | Halts approval/publish transitions when source integrity, crisis, or service integrity conditions fail. |
| `setup_supabase.py` | `src/ccp/scripts/setup_supabase.py` | Extends the canonical schema with editor-specific sessions, revisions, rerender jobs, and lineage records. |
| `FR-ERA3-22` outputs | `DirectionalIntegrityReport` / `HardNegativeEvaluationReport` | Consumed as review projections only; the editor shows drift and flags but does not recompute validator scores. |

**Existing tables consumed:**

- `person_registry` for coach identity resolution
- `asset_registry` for source audio, VCB, composition, and export asset pointers
- `receipt_chain` for immutable audit logs
- `content_performance` for downstream artifact joins after approval

**New editor tables introduced by this spec:**

- `conscious_editor_sessions` - one row per review session, keyed to source audio, content output, VCB, and composition
- `conscious_editor_transcript_revisions` - raw transcript JSON/text patches with diff metadata, author, and classification
- `conscious_editor_rerender_jobs` - queued and completed rerender actions with scope, dependency references, and status
- `conscious_editor_lineage_links` - normalized source-to-artifact chain for UI projection and receipt proof
- `conscious_editor_operator_decisions` - approval, edit-and-approve, regenerate, reject, and escalate decisions
- `conscious_editor_sda_reviews` - cached SDA review projections and source report references for artifact/media review sessions

**Existing API routes extended or called:**

- `GET /health` - extended with Conscious Editor readiness
- existing audio/session ingestion routes remain upstream inputs to the editor

**New API routes introduced by this spec:**

- `GET /api/editor/session/{editor_session_id}` - load a review session with semantic, media, and lineage payloads
- `GET /api/editor/session/{editor_session_id}/artifact` - fetch artifact-review tier payload only
- `GET /api/editor/session/{editor_session_id}/media` - fetch media-review tier payload only
- `GET /api/editor/session/{editor_session_id}/lineage` - fetch normalized lineage chain
- `GET /api/editor/session/{editor_session_id}/sda-review` - fetch reviewer-visible SDA drift projections only
- `POST /api/editor/session/{editor_session_id}/transcript-revisions` - create a new transcript revision set
- `POST /api/editor/session/{editor_session_id}/rerender` - classify and execute a rerender request
- `POST /api/editor/session/{editor_session_id}/approve` - approve current composition for export handoff
- `POST /api/editor/session/{editor_session_id}/edit-and-approve` - mark approved after manual editor-side interventions
- `POST /api/editor/session/{editor_session_id}/escalate` - mark as blocked and route to source restart or operator intervention queue

### 3.3 ADR-05 Primitives

| Primitive ID | Name | Family | Constraint Applied |
|---|---|---|---|
| `EXP-PER-003` | Cumulative Investment | personalization_identity | The artifact review tier must feel like the coach is reviewing something that came from their own accrued voice evidence and prior identity stack, not generic AI output. Lineage, coalition signature, and anti-centroid warnings must be exposed as trust-building evidence. |
| `EXP-SAF-002` | Possible-Win Scarcity | safe_failure_recovery | Recovery paths must be scoped and winnable. A one-word caption correction is a small fix and must remain a small fix in the system architecture. |

Under SDA review mode, these primitives now also constrain how the editor presents drift:
- `EXP-PER-003` means drift projections must feel like fidelity safeguards over the coach's authored meaning, not external algorithmic scolding.
- `EXP-SAF-002` means reviewer-visible drift must map to understandable recovery options rather than overwhelming operators with abstract semantic alarms.

### 3.4 CBAR Mandate Enforcement

| Mandate | Phase-M# | Story | Implementation Mechanism |
|---|---|---|---|
| Modular CMF Recovery Rule | Phase3-M05 | Story 3.2 | `ScopedRerenderClassifier` classifies each operator change into the smallest valid scope. `TranscriptRevisionManager` persists coach edits separately from source evidence. `ScopedRerenderOrchestrator` blocks any accidental fallback to full NIM or audio recapture for typo-class fixes. |

<!-- UPDATED: Added the editor-side consumption rule for SDA drift without turning the editor into a validator. -->

**Wave 0 SDA review invariant**

The Conscious Editor must consume SDA review evidence when it exists, but it must not become a new semantic scoring engine. Therefore:

- drift flags are **projected** from upstream SDA reports
- rerender and escalation recommendations are **advisory review surfaces**
- pass/fail validation ownership remains in `FR-ERA3-22`
- the editor may display drift, suggest scope, and block approval only when a consumed upstream report already marks the artifact as non-pass or review-required

**Formal rerender taxonomy required by M-05**

| Scope Key | Trigger | Reused Inputs | Service Calls | Forbidden Work |
|---|---|---|---|---|
| `caption_text_patch` | Single-word or text-only correction that does not alter semantic intent | existing source audio, existing transcript timing map, existing `ContentMachineResult`, existing `VisualCompositionBrief`, existing composition assets | update revision row, rebuild text payload, call `create_composition(...)` or targeted composition patch flow with updated `text_content` | no `process_session(...)`, no `generate(...)`, no NIM rerun, no audio re-record |
| `composition_reflow` | Text length or placement change requiring layout recompute but not new visuals | same as above plus existing slide imagery | rebuild text payload and composition export | no source rerun, no VCB rerun, no slide image regeneration unless overflow persists after deterministic reflow |
| `visual_slide_regeneration` | Slide-specific visual defect where meaning and transcript remain valid | existing source audio, existing semantic artifact, existing VCB, revision note, selected slide index | call `request_regeneration(composition_id, slide_index, revision_note)` | no source rerun, no transcript discard, no global composition reset |
| `cmf_full_regen_from_compiled_meaning` | Meaning artifact remains valid but visual direction must be recomputed across slides | existing source audio, existing semantic artifact, possibly refreshed VCB input derived from same approved meaning | call `generate(...)`, then rebuild composition | no audio re-record, no Trigger-First bypass, no raw blank-prompt authoring |
| `source_restart_required` | Source evidence itself is invalid, meaning is untrustworthy, or transcript correction materially changes the claim beyond safe patch boundaries | none reused beyond audit history | explicit operator escalation only | automatic reruns, silent source replacement, or hidden meaning rewrite |

**Hard decision rules**

| Condition | Required Scope |
|---|---|
| spelling, punctuation, casing, or subtitle wording change with unchanged timestamps and unchanged meaning | `caption_text_patch` |
| transcript wording change causes line-wrap, safe-area overflow, or caption timing box reflow only | `composition_reflow` |
| transcript remains valid but a slide image is wrong, off-brand, or visually failed | `visual_slide_regeneration` |
| operator explicitly changes the visual concept enough that the current VCB is invalid, while core meaning remains valid | `cmf_full_regen_from_compiled_meaning` |
| operator disputes semantic truth, source attribution, or audio authenticity | `source_restart_required` |

**M-05 invariant**

The editor must treat transcript revisions as layer patches, not source replacement. A transcript patch can update downstream caption surfaces while the original source audio and original upstream session evidence remain immutable in lineage.

### 3.5 Technical Decisions

| Decision | Choice | Reason |
|---|---|---|
| Editor positioning | Review/recovery Mini App, not full editor | PRD-03 explicitly deprecates a broad coach-facing CMF editor under Two-Touchpoint Discipline |
| First visible surface | Semantic artifact before media preview | Required by Story 3.1 and PRD-02 Trigger-First / Archetype-first routing |
| Upstream truth model | Original source audio and first-pass transcript stay immutable | Required for auditability, lineage proof, and safe patching |
| Edit persistence model | Append-only revision rows with diff metadata | Prevents hidden overwrites and makes possible-win recovery measurable |
| Rerender classification | Deterministic rules plus explicit operator override to larger scopes | Prevents accidental expensive reruns while still allowing controlled escalation |
| VCB invalidation threshold | Only visual-concept changes trigger VCB regeneration | `abel_vcb_generator.generate(...)` must not be used for typo fixes |
| Shot-boundary support | Assistive overlay only | OmniShotCut is informative for segment-localized review, but not a reason to add a full shot-detection pipeline into editor MVP |
| SDA review ownership | Consume external reports only | Prevents the editor from drifting into a duplicate validator engine |
| Drift review presentation | Reviewer-visible projection cards plus approval gating | Human reviewers need clear drift visibility without raw validator internals overwhelming the workflow |
| Approval policy | Upstream non-pass SDA report can block approval | Keeps editor decisions aligned with Wave 0 SDA doctrine while preserving human rerender judgment |

## 4. Implementation Plan

<!-- UPDATED: Added SDA report ingestion and drift projection work while preserving existing artifact-first review and rerender flow. -->

### Phase 1 - Session Backbone and Artifact Review

| Task ID | Task | Output |
|---|---|---|
| P1-T1 | Add `startapp=editor` route wiring in `src/ccp/api/main.py` | Mini App becomes addressable and health-reportable |
| P1-T2 | Create `conscious_editor_sessions` schema in `setup_supabase.py` | Canonical review-session persistence |
| P1-T3 | Implement `EditorArtifactResolver` | Session lookup that joins source audio, semantic artifact, VCB, and composition |
| P1-T4 | Implement `ArtifactReadinessGate` | Blocks media tier until `ContentMachineResult.success=True` and `output` exists |
| P1-T5 | Implement `ArchetypeContainerProjection` | Story 3.1 payload with archetype container, content pieces, queue state, and warnings |
| P1-T6 | Emit artifact-review receipt events | Immutable proof that review began at meaning, not media |
| P1-T7 | Implement `EditorSdaReportBridge` | Loads upstream SDA packets and reports into the editor session without recomputation |

### Phase 2 - Transcript Revision and Scoped Recovery

| Task ID | Task | Output |
|---|---|---|
| P2-T1 | Create `conscious_editor_transcript_revisions` schema | Append-only transcript patch storage |
| P2-T2 | Implement `TranscriptRevisionManager` | Diff calculation, author stamping, and raw JSON/text snapshot persistence |
| P2-T3 | Implement `ScopedRerenderClassifier` | Formal scope selection logic for M-05 |
| P2-T4 | Implement `CompositionPatchAssembler` | Rebuild caption payloads from latest approved revision without re-authoring meaning |
| P2-T5 | Add transcript-edit API route | Browser saves revisions directly to backend |
| P2-T6 | Add rerender API route | Revision-to-scope-to-job orchestration |
| P2-T7 | Implement `SdaDriftReviewProjector` | Reviewer-visible projections for invariant loss, representation drift, archetypal incoherence, hard-negative adjacency, and directional-integrity flags |

### Phase 3 - Media Validation and Visual Regeneration

| Task ID | Task | Output |
|---|---|---|
| P3-T1 | Create `conscious_editor_rerender_jobs` schema | Status tracking for scoped rerender work |
| P3-T2 | Implement `ScopedRerenderOrchestrator` | Executes minimal valid rerender path |
| P3-T3 | Implement `VisualRegenerationAdapter` | Bridges slide-level fixes into `request_regeneration(...)` |
| P3-T4 | Add composition reflow support | Handles text-overflow and safe-area recompute |
| P3-T5 | Implement media-review payload | Side-by-side preview, transcript, statuses, revision history, and SDA drift review projections |
| P3-T6 | Emit rerender receipts with scope key | Audit trail proves whether recovery stayed modular |
| P3-T7 | Add drift-aware decision hints | Reviewer-visible guidance connecting drift type to likely rerender or escalation path |

### Phase 4 - Lineage, Decisions, and Fallbacks

| Task ID | Task | Output |
|---|---|---|
| P4-T1 | Create `conscious_editor_lineage_links` schema | Normalized lineage chain |
| P4-T2 | Implement `LineageAuditProjector` | Human-readable source-to-export proof |
| P4-T3 | Create `conscious_editor_operator_decisions` schema | Persistent approval and escalation log |
| P4-T4 | Implement `OperatorReviewDecisionEngine` | Approve, edit-and-approve, regenerate, escalate paths |
| P4-T5 | Integrate `circuit_breaker.py` checks | Crisis/source-integrity stop conditions |
| P4-T6 | Extend `/health` and write integration tests | Deployment readiness and regression safety |
| P4-T7 | Persist SDA review snapshots | Makes drift review auditable and stable across rerender iterations |

## 5. Output Schema

<!-- UPDATED: Added reviewer-facing SDA drift projections and source report references while keeping validation ownership external. -->

All new schemas below use Pydantic v2 style and avoid `Any`. These are specification-level contracts; exact file placement may vary between `src/ccp/models/` and route-layer DTO modules.

```python
from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class EditorTier(str, Enum):
    artifact_review = "artifact_review"
    media_validation = "media_validation"


class RerenderScope(str, Enum):
    caption_text_patch = "caption_text_patch"
    composition_reflow = "composition_reflow"
    visual_slide_regeneration = "visual_slide_regeneration"
    cmf_full_regen_from_compiled_meaning = "cmf_full_regen_from_compiled_meaning"
    source_restart_required = "source_restart_required"


class EditorSessionStatus(str, Enum):
    pending_artifact = "pending_artifact"
    artifact_ready = "artifact_ready"
    media_ready = "media_ready"
    rerender_in_progress = "rerender_in_progress"
    ready_for_approval = "ready_for_approval"
    approved = "approved"
    escalated = "escalated"
    blocked = "blocked"


class OperatorDecision(str, Enum):
    approve = "approve"
    edit_and_approve = "edit_and_approve"
    request_regeneration = "request_regeneration"
    escalate = "escalate"


class TranscriptSourceKind(str, Enum):
    raw_engine_output = "raw_engine_output"
    operator_revision = "operator_revision"


class LineageNodeType(str, Enum):
    source_audio = "source_audio"
    transcript = "transcript"
    semantic_artifact = "semantic_artifact"
    visual_composition_brief = "visual_composition_brief"
    canvas_composition = "canvas_composition"
    export_bundle = "export_bundle"


class DriftSeverity(str, Enum):
    info = "info"
    warning = "warning"
    blocking = "blocking"


class DirectionalIntegrityDecision(str, Enum):
    pass_ = "PASS"
    review = "REVIEW"
    fail = "FAIL"


class TranscriptTokenPatch(BaseModel):
    token_index: int = Field(..., ge=0)
    original_text: str = Field(..., min_length=1)
    revised_text: str = Field(..., min_length=1)
    start_ms: int = Field(..., ge=0)
    end_ms: int = Field(..., ge=0)
    semantic_change_flag: bool = Field(default=False)


class TranscriptRevision(BaseModel):
    revision_id: str = Field(..., min_length=1)
    editor_session_id: str = Field(..., min_length=1)
    source_kind: TranscriptSourceKind = Field(...)
    author_person_id: str = Field(..., min_length=1)
    revision_note: str = Field(default="")
    revised_plaintext: str = Field(..., min_length=1)
    revised_json_payload: str = Field(..., min_length=2)
    token_patches: list[TranscriptTokenPatch] = Field(default_factory=list)
    requires_timing_reflow: bool = Field(default=False)
    created_at_utc: str = Field(..., min_length=1)


class ScopedRerenderDecision(BaseModel):
    decision_id: str = Field(..., min_length=1)
    editor_session_id: str = Field(..., min_length=1)
    revision_id: str = Field(..., min_length=1)
    scope: RerenderScope = Field(...)
    rationale: str = Field(..., min_length=1)
    affected_slide_indices: list[int] = Field(default_factory=list)
    requires_vcb_refresh: bool = Field(default=False)
    requires_audio_rerecord: bool = Field(default=False)
    requires_nim_rerun: bool = Field(default=False)
    created_at_utc: str = Field(..., min_length=1)


class SdaDriftFlag(BaseModel):
    flag_id: str = Field(..., min_length=1)
    severity: DriftSeverity = Field(...)
    drift_type: Literal[
        "invariant_loss",
        "representation_geometry_drift",
        "archetypal_incoherence",
        "hard_negative_adjacency",
        "directional_integrity"
    ] = Field(...)
    title: str = Field(..., min_length=1)
    summary: str = Field(..., min_length=1)
    affected_slide_indices: list[int] = Field(default_factory=list)
    reviewer_guidance: str = Field(..., min_length=1)


class SdaReviewProjection(BaseModel):
    report_id: str = Field(..., min_length=1)
    source_content_output_id: str = Field(..., min_length=1)
    directional_integrity_decision: DirectionalIntegrityDecision = Field(...)
    invariant_preservation_score: float | None = Field(default=None, ge=0.0, le=1.0)
    representation_drift_score: float | None = Field(default=None, ge=0.0, le=1.0)
    hard_negative_adjacency_score: float | None = Field(default=None, ge=0.0, le=1.0)
    trajectory_risk_score: float | None = Field(default=None, ge=0.0, le=1.0)
    flags: list[SdaDriftFlag] = Field(default_factory=list)
    approval_blocked: bool = Field(default=False)


class EditorArtifactSummary(BaseModel):
    content_output_id: str = Field(..., min_length=1)
    session_id: str = Field(..., min_length=1)
    coach_id: str = Field(..., min_length=1)
    archetype_container: str = Field(..., min_length=1)
    content_piece_ids: list[str] = Field(default_factory=list)
    coalition_signature: str | None = Field(default=None)
    anti_centroid_warnings: list[str] = Field(default_factory=list)
    trigger_first_verified: bool = Field(default=True)
    sda_review: SdaReviewProjection | None = Field(default=None)


class MediaReviewSummary(BaseModel):
    vcb_id: str = Field(..., min_length=1)
    composition_id: str = Field(..., min_length=1)
    composition_status: str = Field(..., min_length=1)
    slide_count: int = Field(..., ge=1)
    transcript_revision_id: str | None = Field(default=None)
    editable_transcript_enabled: bool = Field(default=True)
    latest_scope: RerenderScope | None = Field(default=None)
    export_ready: bool = Field(default=False)
    sda_review: SdaReviewProjection | None = Field(default=None)


class LineageNode(BaseModel):
    node_id: str = Field(..., min_length=1)
    node_type: LineageNodeType = Field(...)
    referenced_id: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    parent_node_id: str | None = Field(default=None)
    created_at_utc: str = Field(..., min_length=1)


class EditorLineageGraph(BaseModel):
    editor_session_id: str = Field(..., min_length=1)
    root_source_audio_asset_id: str = Field(..., min_length=1)
    nodes: list[LineageNode] = Field(default_factory=list)
    trigger_first_chain_verified: bool = Field(default=True)
    source_restart_required: bool = Field(default=False)


class ConsciousEditorSession(BaseModel):
    editor_session_id: str = Field(..., min_length=1)
    tier: EditorTier = Field(...)
    status: EditorSessionStatus = Field(...)
    coach_id: str = Field(..., min_length=1)
    source_audio_asset_id: str = Field(..., min_length=1)
    content_output_id: str | None = Field(default=None)
    vcb_id: str | None = Field(default=None)
    composition_id: str | None = Field(default=None)
    artifact_summary: EditorArtifactSummary | None = Field(default=None)
    media_summary: MediaReviewSummary | None = Field(default=None)
    lineage: EditorLineageGraph | None = Field(default=None)
    latest_sda_report_id: str | None = Field(default=None)
    created_at_utc: str = Field(..., min_length=1)
    updated_at_utc: str = Field(..., min_length=1)


class CreateTranscriptRevisionRequest(BaseModel):
    revised_plaintext: str = Field(..., min_length=1)
    revised_json_payload: str = Field(..., min_length=2)
    revision_note: str = Field(default="")
    token_patches: list[TranscriptTokenPatch] = Field(default_factory=list)


class CreateTranscriptRevisionResponse(BaseModel):
    revision: TranscriptRevision = Field(...)
    scope_decision: ScopedRerenderDecision = Field(...)


class ExecuteRerenderRequest(BaseModel):
    revision_id: str = Field(..., min_length=1)
    operator_override_scope: RerenderScope | None = Field(default=None)
    operator_reason: str = Field(default="")


class ExecuteRerenderResponse(BaseModel):
    decision: ScopedRerenderDecision = Field(...)
    resulting_status: EditorSessionStatus = Field(...)
    refreshed_media_summary: MediaReviewSummary | None = Field(default=None)
    refreshed_sda_review: SdaReviewProjection | None = Field(default=None)


class OperatorDecisionRequest(BaseModel):
    decision: OperatorDecision = Field(...)
    decision_note: str = Field(default="")


class OperatorDecisionResponse(BaseModel):
    editor_session_id: str = Field(..., min_length=1)
    decision: OperatorDecision = Field(...)
    resulting_status: EditorSessionStatus = Field(...)
    receipt_event_id: str = Field(..., min_length=1)
```

**Schema notes**

- `revised_json_payload` is stored as a validated JSON string to preserve original transcript structure without relying on untyped freeform blobs in the API contract.
- `requires_audio_rerecord` and `requires_nim_rerun` must remain `False` for every `caption_text_patch`, `composition_reflow`, and `visual_slide_regeneration` decision.
- `LineageNode.parent_node_id` is sufficient for a linear audit chain. A DAG is not required for MVP.
- `SdaReviewProjection` is a reviewer-facing projection over consumed upstream reports. The editor must not mutate SDA scores or synthesize new validator decisions locally.

## 6. Fallback and Failure Handling

<!-- UPDATED: Added SDA review-source fallback handling and approval gating behavior for consumed non-pass reports. -->

The editor must integrate with `src/ccp/core/circuit_breaker.py` and define failure handling that preserves truth boundaries.

### 6.1 Fallback States

| Failure Case | Detection | Fallback Behavior |
|---|---|---|
| `ContentMachineResult.success=False` | artifact load fails | session remains `pending_artifact`; media tier is unavailable; operator sees compile error summary and retry metadata |
| missing source audio lineage | source asset link absent | session becomes `blocked`; approval and rerender routes return a lineage-integrity error |
| transcript revision cannot be parsed | malformed JSON/text structure | reject revision save; keep prior approved transcript active |
| composition patch fails | caption rebuild or export patch error | mark rerender job failed, preserve previous composition, allow retry |
| slide regeneration fails | `request_regeneration(...)` returns error or timeout | keep prior slide asset, show retry or escalate action |
| VCB regeneration fails | `generate(...)` fails for a valid full-CMF request | keep prior VCB/composition active and surface non-destructive failure |
| crisis or integrity halt | `circuit_breaker.py` trip condition | block approve/export and move session to `blocked` or `escalated` |
| SDA report unavailable | upstream report missing or stale | render artifact/media review without synthesized scores, mark drift review unavailable, and block only if upstream policy explicitly requires the report |
| consumed SDA report is non-pass | `DirectionalIntegrityReport.decision in {REVIEW, FAIL}` | surface reviewer-visible drift flags, block approval, and steer operator toward rerender or escalation instead of silent publish |

### 6.2 Circuit Breaker Integration

The Conscious Editor must call the circuit breaker before these transitions:

- `approve`
- `edit_and_approve`
- `cmf_full_regen_from_compiled_meaning`
- `source_restart_required`

It must also check the latest consumed SDA report before:

- `approve`
- `edit_and_approve`

If the latest consumed report is `REVIEW` or `FAIL`, the editor must not override that result silently. It may still allow human inspection, transcript correction, rerender, or explicit escalation.

If the breaker is open, the editor must:

- prevent publish-side approval actions
- preserve current artifacts without deletion
- write a receipt event indicating blocked transition and reason
- surface an operator-readable recovery banner instead of a generic 500 response

### 6.3 Non-Destructive Guarantee

No rerender failure may delete:

- original source audio references
- original first-pass transcript payload
- prior successful composition assets
- prior approved transcript revision rows

Fallback behavior is always additive and reversible at the job layer, even when the visual output is not immediately fixable.

## 7. Tasks

<!-- UPDATED: Added concrete tasks for SDA report ingestion and drift review projection. -->

1. Add editor router registration and `startapp=editor` health exposure in [main.py](/D:/Work/The Conscious Coaching Factory/src/ccp/api/main.py).
2. Extend [setup_supabase.py](/D:/Work/The Conscious Coaching Factory/src/ccp/scripts/setup_supabase.py) with the five new `conscious_editor_*` tables and indexes on `editor_session_id`, `composition_id`, and `source_audio_asset_id`.
3. Add editor domain models in `src/ccp/models/` using the Section 5 schema contracts.
4. Implement `EditorArtifactResolver` with joins to source asset, `ContentMachineResult`, `VisualCompositionBrief`, and `CanvasComposition`.
5. Implement `ArchetypeContainerProjection` to render semantic artifact review ahead of media review.
6. Implement `TranscriptRevisionManager` with append-only revision persistence and diff capture.
7. Implement `ScopedRerenderClassifier` using the Section 3.4 taxonomy and invariant rules.
8. Implement `CompositionPatchAssembler` to rebuild `text_content` payloads for caption-only and reflow scopes.
9. Implement `ScopedRerenderOrchestrator` to route caption-only, reflow, visual-only, and full-CMF recovery through the correct services.
10. Implement `VisualRegenerationAdapter` to call `request_regeneration(...)` with slide-local context and revision notes.
11. Implement `LineageAuditProjector` and persist normalized lineage rows for every reviewable session.
12. Implement operator decision routes for approve, edit-and-approve, regenerate, and escalate.
13. Add receipt-chain writes for every revision save, rerender classification, rerender execution, approval, and fallback.
14. Add circuit-breaker checks before approval and source-escalation actions.
15. Add `/health` readiness checks for editor tables, dependent services, and route registration.
16. Write unit and integration tests matching existing typed scenario patterns.
17. Add `conscious_editor_sda_reviews` persistence plus report-reference joins for review sessions.
18. Implement `EditorSdaReportBridge` to ingest `DirectionalIntegrityReport` and `HardNegativeEvaluationReport` artifacts.
19. Implement reviewer-visible drift cards for invariant loss, representation-geometry drift, archetypal incoherence, hard-negative adjacency, and directional-integrity flags.
20. Gate approval on consumed non-pass SDA reports without turning the editor into a new scoring engine.

## 8. Acceptance Criteria

<!-- UPDATED: Added reviewer-facing SDA drift acceptance without altering existing rerender taxonomy. -->

### Story 3.1 - Trigger-First Artifact Review

**AC-3.1-A**

- Given a coach has recorded a reaction or coaching voice note
- When `ContentMachinePipeline.process_session(...)` completes successfully
- Then `GET /api/editor/session/{editor_session_id}/artifact` returns a payload whose primary object is `EditorArtifactSummary`
- And the payload exposes the `archetype_container` before any composition preview URL or export asset
- And the UI contains no blank prompt-box authoring surface
- Mandate ref: Story 3.1, PRD-02 Trigger-First Execution, PRD-02 Archetype Container Routing
- Failure example: the session opens directly on a video player with no semantic artifact view and no archetype label

**AC-3.1-B**

- Given an artifact review session is loaded
- When the artifact payload contains coalition signature or anti-centroid validation data
- Then the editor shows those trust signals in the review tier instead of hiding them behind a later publish step
- Mandate ref: `EXP-PER-003` Cumulative Investment
- Failure example: the coach sees polished copy but no evidence it came from their authenticated voice history

**AC-3.1-C**

- Given an artifact review session is loaded and upstream SDA reports exist for the artifact
- When the editor returns the artifact-review payload
- Then the payload includes reviewer-visible drift projections for invariant loss or mutation, representation-geometry drift, archetypal incoherence, hard-negative adjacency, and directional-integrity flags
- And those projections are clearly marked as consumed review evidence rather than locally recomputed scores
- Failure example: the artifact review tier exposes archetype and lineage but hides a blocking directional-integrity report until after export approval

### Story 3.2 - CMF Media Validation and Operator Review

**AC-3.2-A**

- Given an artifact has valid semantic output plus a reviewable `CanvasComposition`
- When the coach opens `GET /api/editor/session/{editor_session_id}/media`
- Then the response includes both `MediaReviewSummary` and the latest transcript revision payload
- And the UI renders a side-by-side media panel plus editable transcript JSON/text panel
- Mandate ref: Story 3.2
- Failure example: the transcript is displayed as read-only text or hidden behind a separate admin tool

**AC-3.2-B**

- Given a coach fixes a misspelled word in a caption transcript
- When the revision is saved and rerendered
- Then the resulting `ScopedRerenderDecision.scope` is `caption_text_patch` or `composition_reflow`
- And `requires_audio_rerecord=False`
- And `requires_nim_rerun=False`
- And the prior source audio, semantic artifact, VCB, and composition lineage remain linked
- Mandate ref: Phase3-M05, `EXP-SAF-002`
- Failure example: the system forces a full audio re-record, reruns NIM, or silently regenerates meaning from scratch for a one-word fix

**AC-3.2-C**

- Given the transcript remains correct but one slide image is visually wrong
- When the coach requests a slide fix
- Then the resulting `ScopedRerenderDecision.scope` is `visual_slide_regeneration`
- And the system calls `request_regeneration(composition_id, slide_index, revision_note)` for only the affected slide
- And the rest of the composition remains intact
- Mandate ref: Story 3.2, M-05 modular recovery
- Failure example: a single slide issue deletes the whole composition or restarts every slide render

**AC-3.2-D**

- Given a coach is reviewing the final artifact
- When they inspect lineage
- Then the UI displays a readable chain back to the original voice recording through transcript, semantic artifact, VCB, and composition
- And the operator can see whether a displayed caption came from raw engine output or a later operator revision
- Mandate ref: Story 3.2, PRD-02 human auditability
- Failure example: the final media can be approved without any source proof or revision history

**AC-3.2-E**

- Given a media review session has an upstream `DirectionalIntegrityReport` with `REVIEW` or `FAIL`
- When the operator opens `GET /api/editor/session/{editor_session_id}/media`
- Then the media-review surface includes a visible SDA drift panel with the consumed decision, human-readable drift flags, and reviewer guidance tied to rerender or escalation actions
- And approval actions remain blocked until the artifact is rerendered or escalated
- Failure example: the operator can approve export even though the consumed report already marks the artifact as directionally unsafe

**AC-3.2-F**

- Given the artifact remains transcript-correct and visually aligned at a surface level
- When the consumed SDA review indicates archetypal incoherence or hard-negative adjacency risk
- Then the editor must show that drift explicitly instead of pretending transcript/media parity is sufficient
- And the reviewer can decide between `cmf_full_regen_from_compiled_meaning` and `source_restart_required` based on the surfaced guidance
- Failure example: the editor shows "all clear" because captions match slides while a hard-negative near-neighbor risk remains hidden

## 9. Dependencies

<!-- UPDATED: Added mandatory SDA report-producing dependencies for drift review mode. -->

| Dependency Type | Name | Why It Matters |
|---|---|---|
| Upstream service | `ContentMachinePipeline.process_session(...)` | Supplies the semantic artifact required for Story 3.1 |
| Upstream model | `ContentMachineResult` / `ContentMachineArray` / `SessionContentPiece` | Canonical semantic-artifact structure |
| Visual prompt service | `AbelVCBGenerator.generate(...)` | Required only for full-CMF regeneration from existing compiled meaning |
| Composition service | `CanvasCompositionService.create_composition(...)` | Required for caption patching and composition reflow |
| Composition service | `CanvasCompositionService.request_regeneration(...)` | Required for visual-only slide regeneration |
| Composition service | `CanvasCompositionService.approve(...)` / `edit_and_approve(...)` | Required for operator completion paths |
| Shared models | `VisualCompositionBrief`, `CanvasComposition`, `RegenerationRequest`, `CompositionStatus` | Prevent editor-side model drift |
| Audit infrastructure | `receipt_chain.py` | Required to prove lineage, revisions, and operator decisions |
| Safety infrastructure | `circuit_breaker.py` | Required to halt invalid approvals or broken source states |
| Database bootstrap | `setup_supabase.py` | Required to create editor tables and indexes |
| Mini App routing | `main.py` | Required to expose `startapp=editor` and API routes |
| Research assist | OmniShotCut reference | Optional shot-localization guidance for future segment-level review UX |
| SDA foundation | `FR-ERA3-20_SDA_Ontology_And_Registry_Tech_Spec.md` | Supplies canonical ontology/grammar references consumed by upstream reports |
| SDA query layer | `FR-ERA3-21_SDA_Query_And_Crosswalk_Service_Tech_Spec.md` | Supplies canonical lookup/crosswalk references used by upstream drift reports |
| SDA validator | `FR-ERA3-22_Directional_Integrity_Engine_Tech_Spec.md` | Produces the directional-integrity and hard-negative reports projected by the editor |

**Dependency constraints**

- The editor may consume CMF outputs, but it may not become a new prompt authoring source.
- `generate(...)` is not a default retry tool for transcript edits.
- `request_regeneration(...)` is slide-scoped by design and must stay slide-scoped in editor orchestration.
- The editor may project SDA drift, but it may not recalculate validator scores, ontology matches, or hard-negative evaluations locally.

## 10. Testing Strategy

<!-- UPDATED: Added explicit unit/integration coverage for consumed SDA drift projections and approval gating. -->

The testing pattern must follow the typed, scenario-first structure already used in:

- [test_cpsc_fr52_webinar_brief.py](/D:/Work/The Conscious Coaching Factory/tests/integration/test_cpsc_fr52_webinar_brief.py)
- [test_ca11_fr16_studio_block.py](/D:/Work/The Conscious Coaching Factory/tests/integration/test_ca11_fr16_studio_block.py)

### 10.1 Unit Tests

| Test Name | Purpose |
|---|---|
| `test_scoped_rerender_classifier_returns_caption_patch_for_single_word_fix` | Verifies that typo-class revisions stay in `caption_text_patch` and explicitly set both rerun flags to `False` |
| `test_scoped_rerender_classifier_returns_composition_reflow_for_wrap_only_change` | Verifies that longer subtitle text causing layout overflow upgrades only to `composition_reflow` |
| `test_scoped_rerender_classifier_returns_visual_regeneration_for_slide_only_defect` | Verifies that a visual complaint with unchanged transcript routes to `visual_slide_regeneration` |
| `test_transcript_revision_manager_preserves_original_source_payload` | Verifies append-only revision storage and original transcript immutability |
| `test_lineage_audit_projector_emits_source_to_export_chain_in_order` | Verifies node ordering and parent references for audit display |
| `test_sda_drift_review_projector_maps_consumed_report_into_flags` | Verifies that upstream SDA reports are converted into reviewer-visible drift flags without recomputation |
| `test_editor_blocks_approval_when_consumed_directional_integrity_is_non_pass` | Verifies the editor gates approval on consumed `REVIEW` / `FAIL` reports |

### 10.2 Integration Tests

| Test Name | Purpose |
|---|---|
| `test_editor_artifact_review_returns_archetype_before_media_preview` | End-to-end load of a session with successful `ContentMachineResult` proving Story 3.1 ordering |
| `test_editor_transcript_typo_fix_rerenders_without_nim_or_audio_restart` | End-to-end save of a transcript revision, rerender execution, and assertions that scope stays modular under M-05 |
| `test_editor_slide_regeneration_keeps_other_slots_and_lineage_intact` | End-to-end visual-only recovery against one slide while preserving the remaining composition and lineage rows |
| `test_editor_media_review_surfaces_consumed_sda_drift_flags` | End-to-end load proving reviewer-visible invariant / geometry / hard-negative drift projections appear in the media tier |
| `test_editor_non_pass_sda_report_forces_rerender_or_escalation_before_approval` | End-to-end proof that approval is blocked when the consumed directional-integrity report is non-pass |

### 10.3 Test Data Requirements

- fixture with source audio asset, `ContentMachineResult`, `VisualCompositionBrief`, and `CanvasComposition`
- transcript fixture containing token timestamps and one intentional typo
- composition fixture with at least three slides so slide-local recovery can be asserted
- receipt-chain assertions for revision save, scope classification, and approval transitions
- upstream `DirectionalIntegrityReport` fixture with both `PASS` and `REVIEW` / `FAIL` variants
- upstream `HardNegativeEvaluationReport` fixture with at least one adjacency warning mapped to a reviewer flag

### 10.4 Mandatory Assertions

Every M-05 integration test must assert all of the following:

- returned `scope` equals the expected modular scope
- `requires_audio_rerecord` is `False`
- `requires_nim_rerun` is `False`
- prior source audio asset ID is unchanged
- prior semantic artifact ID is unchanged
- prior VCB ID is unchanged for caption-only and composition-reflow cases
- receipt chain contains a rerender classification event with the selected scope key

### 10.5 Non-Goals for Testing

The test suite for this spec does not need to:

- benchmark OmniShotCut itself
- validate the internals of NIM
- retest `content_machine.py` extraction quality
- duplicate canvas rendering engine snapshot suites that belong to CMF service tests
