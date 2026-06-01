# FR-ERA3-12 — CMF Arc-Governed Rendering Tech Spec
## UPDATED FOR LIVING COMMENTARY

| Field | Value |
|---|---|
| **Spec ID** | FR-ERA3-12 |
| **Version** | 3.0 (ERA3 Architecture — Living Commentary Realization Integration) |
| **Phase** | 7 — Living Commentary & Coach Communication Stack |
| **Source PRD** | PRD-02 (CCF Content Factory), PRD-03 (CMF Media Factory) |
| **Status** | DRAFT |
| **Created** | 2026-05-24 |
| **Supersedes** | FR-ERA3-12 v1.0 (base), FR-ERA3-12 v2.0 (SFL update) |
| **Absorbs** | FR-ERA3-58, FR-ERA3-59, FR-ERA3-60 (Living Commentary standalone specs are NOT written — folded here) |

> [!IMPORTANT]
> This spec is an **UPDATE** to the existing CMF Arc-Governed Rendering pipeline. Living Commentary is a **realization layer extension** of the CMF renderer — NOT a separate engine. All existing arc-governed rendering behavior (beat clusters, gates, SFL packets) is preserved and extended.

> [!IMPORTANT]
> **RENDERING BACKEND PIVOT:** The legacy C++ Skia sidecar (`src/ccp/sidecars/skia-renderer/`) and Python-based CMF queues are **formally deprecated**. All vertical video and static compositions are rendered via **Remotion Node.js + `@remotion/skia`** (CanvasKit WebAssembly). The generation payload is structured around the **Complete Editing Session** state wrapper.

---

## 1. Files Read (Pre-Work Log)

### 1.1 Protocol
- **`docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`** — Loaded. 10-section format, CBAR mandate enforcement, existing backend integration requirements confirmed.

### 1.2 Source PRDs

**PRD-02 (CCF Content Factory):**
> "CCF compiles the meaning. CMF renders the felt experience of that meaning." (PRD-03 line 46, cross-referenced in PRD-02)
> "This module therefore defines the content factory as a compiler, not a creator in the consumer-tool sense. It is the source-of-truth content spine for the wider platform: CMF renders its scripts and shot logic" (PRD-02 line 56)
> "CCF is not the final media renderer. It emits content source artifacts that downstream systems can transform." (PRD-02 line 130)
> "CMF should treat CCF artifacts as authoritative meaning packets. It may reinterpret visually and sonically, but it should not overwrite the coalition logic without explicit validator approval." (PRD-02 line 994)

**PRD-03 (CMF Media Factory):**
> "The Conscious Media Factory is the visual and sonic rendering arm of CCP. It does not decide what the coach means. It decides how that meaning becomes perceptible, cinematic, memorable, and emotionally legible" (PRD-03 line 40)
> Seven Runtime Layers: L1 Meaning Intake → L2 Narrative Rendering Model → L3 Prompt and Asset Composition → L4 Deterministic Control Layer → L5 Generation Layer → L6 Assembly Layer → L7 Validation and Benchmarking (PRD-03 lines 107-116)
> "Beat clusters are the bridge between script meaning and media construction." (PRD-03 line 320)
> "FFmpeg / Remotion assembly layer" listed as major infrastructure component (PRD-03 line 420)

### 1.3 Master Blueprints

**HANDOVER_CONSOLIDATION_BLUEPRINTS.md:**
> **Remotion Mandate:** "A centralized Node.js Remotion server consumes the depth-aware layers. We natively integrate React Native Skia (via CanvasKit WebAssembly) inside Remotion to handle deep pixel math and parallax displacement, while using standard React to keep text animation highly intentional and sparse (e.g., using Rough Notation)." (line 24)
> **Complete Editing Session:** "To ensure intelligent orchestration and zero data loss, every lesson initiates a stateful 'Editing Session' wrapper. This holds all CRAL research, VIE assets, and transcripts in one payload." (line 33)
> **Synthetic Voice Ban:** "Human transformation requires trust; trust requires biological authenticity. The use of synthetic AI voice generation (e.g., ElevenLabs clones) to deliver the coach's message is strictly and permanently prohibited." (line 31)
> **Legacy Deprecation:** "The legacy standalone Python Skia sidecar (`src/ccp/services/cmf_arc_governed_rendering.py`) is to be deleted." (line 115)

**Architectural_Audit_Trigger_First_Vision_Visual_Engines.md:**
> **Remotion Mandate:** "The standalone C++/Python Skia sidecar is formally deprecated. The engine must be centralized into a Remotion Node.js server utilizing `@remotion/skia`." (line 160)
> **VIE Reversal:** "Our visual intelligence is extremely valuable, hyper-sophisticated, and absolutely critical for the 'Living Still' and Parallax compositional mechanics that define our premium aesthetic." (line 88)
> **Hybrid Pipeline:** GENERATE (VIE/LoRA) → MASK & DEPTH (SAM3/PRETEXT) → COMPOSE (Remotion + @remotion/skia) (lines 90-97)
> **4 Vertical Video Formats:** Cinematic Story Commentary, 2D Avatar/Animated Explainer, Living Commentary Reactions, Conscious Reactions Editing (lines 66-80)

### 1.4 Living Commentary Source Set

**Living_Commentary_Realization_Layer_Source_of_Truth.md (1179 lines):**
> **7-Layer Composition Model (lines 384-397):**
> 1. background climate | 2. mid-background field objects | 3. screenshot / quote / comparison object | 4. supporting marks and icons | 5. coach body | 6. coach head / gesture emphasis | 7. foreground accent or text

> **Allowed Motion Vocabulary (lines 359-373):** parallax depth, 2.5D layering, slow push-in, drift, selective floating, light pulse, shadow pass, atmospheric particles, film grain, controlled flicker, hand-drawn reveal

> **Banned Motion Vocabulary (lines 374-383):** hyperactive pop-ins, generic social media zoom spam, excessive bounce, overly literal emoji explosions, default trend animations, kinetic text overload, transitions that outrun the voice

> **Memetic Sound Cue Moderation Law (lines 429-471):** "generally 1 meaningful cue per 30 seconds maximum unless the surface is explicitly comedy-dense" — "never use them to compensate for weak judgment" — "use them only when they reinforce a reveal, contrast, joke, or reaction beat"

> **6 Format Families (lines 247-353):** Quote, Comparison, Screenshot, Atmospheric, Cinematic Story, Animated Explainer — each with distinct ingredient sets and realization rules.

> **Living Still (lines 129-148):** "start from a still image or still field → introduce selective life → preserve clarity → avoid overload"

**Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md (1183 lines):**
> **FR-ERA3-58, 59, 60 Original Scoping (lines 1045-1093):** FR-ERA3-58 (Realization Engine), FR-ERA3-59 (Motion Grammar & Layering), FR-ERA3-60 (Sound Cue & Atmosphere) — all three are now folded into this update.
> **CMF Integration Points (lines 344-351):** "Living Commentary render family, Living Still / parallax / 2.5D / ambient motion grammar, object-timed text and sonic punctuation, reduced dependence on slide-like reel assumptions"

### 1.5 Existing FR-ERA3-12 Specs

**FR-ERA3-12 v1.0 (Base — 619 lines):**
> **6 Orchestration Layers:** NarrativeRenderingModel → BeatClusterPlanner → DeterministicControlResolver → FirstFrameAuthorityGate → EpicMeaningGate → SkiaRenderManifestBuilder + SkiaRenderSidecarBridge
> **Schemas:** `BeatClusterType`, `ShotGrammarProfile`, `TempoEnvelope`, `ClusterShotDirective`, `DeterministicControlSpec`, `BeatClusterPlan`, `FirstFrameAuthorityCheck`, `EpicMeaningGateResult`, `CoalitionSpineInput`, `ArcRenderManifest`, `ArcRenderJobRecord`
> **Gate Thresholds:** FirstFrame: authority≥0.72, contrast≥0.65, recognizability≥0.70. EpicMeaning: blandness≤0.15.

**FR-ERA3-12 v2.0 (SFL Update — 739 lines):**
> **SFL Additions:** `RenderPerceptualPlan`, `CompositionDepthRenderProfile`, `VariationRenderHints`, `TemporalCraftHints`, `RenderPreservationReport`, `ScoreCardRenderBundle`, `AuditBoardRenderBundle`
> **Updated Flow:** archetype output → SubliminalFunctionStackPacket → CompositionDepthRenderProfile → VariationRenderHints → TemporalCraftHints → RenderPerceptualPlan → realization → RenderPreservationReport

### 1.6 Voice Prompt Engine (FR-ERA3-17 — 805 lines)
> **7-Layer Engine:** VoicePromptDecisionResolver → VoicePromptComposer → VoiceDNAAlignmentBridge → SonicBedResolver → ConsciousVoiceSynthesisAdapter → SonicPrestigeGate → VoicePromptDispatchCoordinator
> **Sound Management:** `SonicBedProfile` (bed_id, emotional_job, fade_in_ms, fade_out_ms, target_gain, duration_ceiling_seconds). Beds from controlled job-specific registry, not random library tracks.
> **Integration:** FR-ERA3-17 owns voice prompt sonic beds. FR-ERA3-12 owns Living Commentary sonic atmosphere and cue timelines. These are separate but parallel concerns.

### 1.7 Existing Backend Code

**CMF Services Read:**
- `src/ccp/services/cmf_arc_governed_rendering.py` — `CMFArcGovernedRenderingPipeline` with methods: `create_job()`, `run_epic_meaning_gate()`, `build_manifest()`, `release()`, `generate_audit_bundles()`, `build_render_perceptual_plan()`
- `src/ccp/services/course_video_cmf.py` — `CourseVideoPipeline.execute()`, `RenderEngineProtocol`, `VisualAidAssembler`
- `src/ccp/services/format_governance_engine.py` — `FormatGovernanceEngine.apply_format_governance()`, `compute_weekly_allocation()`
- `src/ccp/services/abel_vcb_generator.py` — `AbelVCBGenerator.generate()` (9-step pipeline)
- `src/ccp/services/saliency_analysis_service.py` — `SaliencyAnalysisService.analyze()`

**Models Read:**
- `src/ccp/models/cmf_arc_render_models.py` — 157 lines, all base schemas
- `src/ccp/models/cmf_sfl_render_models.py` — 168 lines, all SFL schemas
- `src/ccp/models/spatial_engine_models.py` — 132 lines, spatial composition
- `src/ccp/models/visual_engine_models.py` — 2545 lines, 50+ visual classes
- `src/ccp/models/conscious_editor_models.py` — 179 lines, editor session models

**No Remotion files exist in `src/`** — the Remotion backend is net-new infrastructure.

### 1.8 Existing Test Patterns

**`tests/integration/test_fr_era3_12_cmf_arc_governed_rendering.py` (74 lines):**
- `TestArcRenderJobStopsBeforeFullRenderWhenFirstFrameGateFails.test_corporate_flag_blocks_job()`
- `TestReleaseHandoffCreatesCompositionAfterDualGatePass.test_dual_gate_pass_allows_release()`
- `TestReleaseHandoffCreatesCompositionAfterDualGatePass.test_release_denied_without_first_frame()`

**`tests/integration/test_fr_era3_12_cmf_sfl_rendering.py` (201 lines):**
- `test_sfl_render_planning_success()` — creates job with SFL structures
- `test_sfl_render_preservation_downgrade()` — high synthetic smoothness triggers DOWNGRADE
- `test_course_video_temporal_hints_success()` — renders course video with temporal hints

---

## 2. Overview

### 2.1 Problem

The CMF Arc-Governed Rendering pipeline (v1.0 + v2.0/SFL) currently renders content archetypes as visual compositions using the legacy Skia sidecar. It does not know about:

1. **Living Commentary format families** — six distinct realization surfaces (Quote, Comparison, Screenshot, Atmospheric, Cinematic Story, Animated Explainer) that require coach-led, reaction-first, voice-first rendering
2. **Motion grammar** — a controlled vocabulary of allowed/banned motions that prevents the "hyperactive pop-in" aesthetic degradation common in commoditized social content
3. **Sound cue doctrine** — punctuation, atmosphere, timing reinforcement, and memetic cue moderation rules that make commentary feel alive without becoming noisy
4. **Living Still composition** — the selective-motion philosophy where depth is created by introducing minimal life into a still field
5. **7-layer composition depth** — a structured layer stack that gives parallax and spatial authority without full 3D environments
6. **Remotion Node.js backend** — the legacy Skia sidecar is deprecated; all rendering must target the centralized Remotion + `@remotion/skia` server
7. **Internal Prototype Routing** — pre-recording carousel prototypes routed to the coach as learning material, not published externally

### 2.2 Solution

Extend the existing `CMFArcGovernedRenderingPipeline` with:

- A **Living Commentary realization planning layer** that sits between the existing SFL perceptual plan and the render manifest builder
- **Format-family render configs** that govern how each of the 6 Living Commentary families is realized (ingredients, motion intensity, sound doctrine, layer composition)
- A **motion grammar engine** that validates motion choices against the allowed/banned vocabulary and enforces anti-overload guardrails
- A **sound cue timeline builder** that integrates with FR-ERA3-17 as a consumer (not owner) of sonic assets, enforcing the 1-per-30s memetic moderation law
- A **Living Still composition resolver** that starts from still fields and introduces selective life
- A **Remotion manifest builder** replacing the `SkiaRenderManifestBuilder` + `SkiaRenderSidecarBridge` with a `RemotionManifestBuilder` + `RemotionServerBridge`
- A **Complete Editing Session integration layer** that reads from and writes to the session payload
- An **Internal Prototype Router** that marks `is_internal_prototype=True` renders for coach-only consumption

### 2.3 Scope

**IN SCOPE:** Living Commentary realization planning, motion grammar validation, sound cue timeline, Living Still composition, format family configs, Remotion backend bridge, Complete Editing Session integration, internal prototype routing, extension of all existing gates (FirstFrame, EpicMeaning) to evaluate Living Commentary surfaces.

**OUT OF SCOPE:** Archetype Container Runtime changes (FR-ERA3-16), voice prompt engine changes (FR-ERA3-17 owns its own sonic beds), VIE asset generation (upstream), SAM3 masking (upstream), coach recording (Studio Block), content benchmark profiles (FR-ERA3-35B), eval card system (FR-ERA3-35C).

---

## 3. Context for Development

### 3.1 Architecture Traceability (DEP-IDs)

| DEP-ID | Data Object | Source | Consumer |
|---|---|---|---|
| DEP-CMF-001 | `CoalitionSpineInput` | CCF / Upstream | `NarrativeRenderingModel` |
| DEP-CMF-002 | `BeatClusterPlan` | `NarrativeRenderingModel` | `BeatClusterPlanner` |
| DEP-CMF-003 | `DeterministicControlSpec` | `DeterministicControlResolver` | Render manifest |
| DEP-CMF-004 | `FirstFrameAuthorityCheck` | `FirstFrameAuthorityGate` | Release gate |
| DEP-CMF-005 | `TempoEnvelope` | `ArcSonicBedPlanner` | Render manifest |
| DEP-CMF-006 | `EpicMeaningGateResult` | `EpicMeaningGate` | Release gate |
| DEP-CMF-007 | `ArcRenderManifest` | `RemotionManifestBuilder` | Remotion server |
| DEP-CMF-008 | `ArcRenderJobRecord` | `CMFArcGovernedRenderingPipeline` | All consumers |
| DEP-CMF-SFL-012-01 | `RenderPerceptualPlan` | SFL stack | Render planning |
| DEP-CMF-SFL-012-05 | `RenderPreservationReport` | Post-render | Audit trail |
| **DEP-CMF-LC-001** | `LivingCommentaryRealizationPlan` | Living Commentary planner | Remotion manifest |
| **DEP-CMF-LC-002** | `MotionGrammarProfile` | Motion grammar engine | Layer composition |
| **DEP-CMF-LC-003** | `SoundCueTimeline` | Sound cue builder | Remotion audio mix |
| **DEP-CMF-LC-004** | `LivingStillCompositionSpec` | Living Still resolver | Layer composition |
| **DEP-CMF-LC-005** | `FormatFamilyRenderConfig` | Config registry | All LC render paths |
| **DEP-CMF-LC-006** | `CompositionLayerStack` | Layer assembler | Remotion composition |
| **DEP-CMF-LC-007** | `MotionOverloadAudit` | Anti-overload engine | Gate system |
| **DEP-CMF-LC-008** | `InternalPrototypeRoutingDecision` | Prototype router | Delivery coordinator |
| **DEP-CMF-LC-009** | `RemotionRenderPayload` | Manifest builder | Remotion Node.js server |
| **DEP-CMF-LC-010** | `CompleteEditingSessionRef` | Session wrapper | All render paths |

### 3.2 Existing Backend Integration (≥4 files)

| Existing File | Integration Point |
|---|---|
| `src/ccp/services/cmf_arc_governed_rendering.py` | **EXTENDS** `CMFArcGovernedRenderingPipeline` with Living Commentary planning layer, Remotion manifest builder, and internal prototype routing. Methods extended: `create_job()` gains `living_commentary_config` and `editing_session_id` params. New methods: `plan_living_commentary()`, `build_remotion_manifest()`, `route_internal_prototype()`. |
| `src/ccp/models/cmf_arc_render_models.py` | **EXTENDS** with new `LivingCommentaryRealizationPlan`, `MotionGrammarProfile`, `SoundCueTimeline`, `LivingStillCompositionSpec`, `FormatFamilyRenderConfig`, `CompositionLayerStack`, `MotionOverloadAudit`, `InternalPrototypeRoutingDecision`, `RemotionRenderPayload` models. Existing `ArcRenderJobRecord` gains `living_commentary_plan_id`, `editing_session_id`, `is_internal_prototype` fields. Existing `BeatClusterPlan` gains `motion_grammar_profile_id` and `sound_cue_slots` fields. |
| `src/ccp/services/format_governance_engine.py` | **CONSUMES** `FormatGovernanceEngine.apply_format_governance()` to resolve which format family governs the Living Commentary render. |
| `src/ccp/services/abel_vcb_generator.py` | **CONSUMES** `AbelVCBGenerator.generate()` for VCB generation — augmented with Living Commentary layer depth hints via `ArcGovernedVCBAugmentor`. |
| `src/ccp/services/course_video_cmf.py` | **CONSUMES** `CourseVideoPipeline.execute()` for Animated Explainer format family when the surface is educational. |
| `src/ccp/services/saliency_analysis_service.py` | **CONSUMES** `SaliencyAnalysisService.analyze()` for screenshot/quote panel saliency in layer 3 composition. |
| `src/ccp/models/cmf_sfl_render_models.py` | **READS** all SFL schemas — `RenderPerceptualPlan`, `CompositionDepthRenderProfile`, `VariationRenderHints`, `TemporalCraftHints` feed into Living Commentary planning. |
| `src/ccp/models/visual_engine_models.py` | **READS** `SomaticArcType`, `PSSLBlock`, `GateC09Result`, `UNIVERSAL_ANTI_GENERIC` for gate enforcement. |
| `src/ccp/core/receipt_chain.py` | **CONSUMES** `ReceiptChain.log()` for all gate verdicts, render events, and prototype routing decisions. |
| `src/ccp/core/circuit_breaker.py` | **CONSUMES** for pipeline failure protection. |
| `src/ccp/api/main.py` | **EXTENDS** with new Living Commentary render routes. |
| `src/ccp/scripts/setup_supabase.py` | **EXTENDS** with new tables: `cmf_living_commentary_plans`, `cmf_motion_grammar_profiles`, `cmf_sound_cue_timelines`, `cmf_living_still_specs`, `cmf_format_family_configs`, `cmf_remotion_payloads`. |

### 3.3 Living Commentary Render Contracts

The CMF renderer now supports **two render paths** that share the same pipeline but diverge at the realization planning stage:

```
PATH A — Standard Arc-Governed Rendering (existing):
  CoalitionSpineInput → NarrativeRenderingModel → BeatClusterPlanner
  → DeterministicControlResolver → FirstFrameAuthorityGate
  → EpicMeaningGate → RemotionManifestBuilder → RemotionServerBridge

PATH B — Living Commentary Realization (new):
  CoalitionSpineInput + FormatFamilyRenderConfig
  → NarrativeRenderingModel → BeatClusterPlanner
  → LivingCommentaryRealizationPlanner (NEW)
    → MotionGrammarResolver (NEW)
    → SoundCueTimelineBuilder (NEW)
    → LivingStillCompositionResolver (NEW)
    → CompositionLayerStackAssembler (NEW)
  → DeterministicControlResolver (existing, extended)
  → FirstFrameAuthorityGate (existing, extended for LC surfaces)
  → EpicMeaningGate (existing, extended for LC surfaces)
  → MotionOverloadGate (NEW)
  → RemotionManifestBuilder (NEW, replaces SkiaRenderManifestBuilder)
  → RemotionServerBridge (NEW, replaces SkiaRenderSidecarBridge)
  → InternalPrototypeRouter (NEW, optional)
```

**The 7-Layer Composition Model** (governs all Living Commentary surfaces):

| Layer | Name | Z-Depth | Content | Motion Budget |
|---|---|---|---|---|
| 1 | Background Climate | 0.0 | Atmospheric gradient, ambient texture, grain | Slow drift, light pulse only |
| 2 | Mid-Background Field Objects | 0.15 | Environmental objects, scene-setting imagery | Subtle parallax, ≤2px/frame |
| 3 | Screenshot / Quote / Comparison Object | 0.35 | The proof object, headline, quote card, comparison layout | Static or hand-drawn reveal only |
| 4 | Supporting Marks & Icons | 0.50 | Check marks, crosses, arrows, callout lines | Appear-on-beat, no bounce |
| 5 | Coach Body | 0.70 | Coach cutout (SAM3 masked), posed or reactive | Natural sway, no artificial animation |
| 6 | Coach Head / Gesture Emphasis | 0.85 | Head tilt, hand gesture overlay, gaze direction | Gesture-synced, ≤1 emphasis per 5s |
| 7 | Foreground Accent / Text | 1.0 | Caption text, Rough Notation highlights, brand marks | Rough Notation reveal only, no kinetic text |

### 3.4 Governance Constraints

**Preserved from v1.0 + v2.0:**
- `Render-Preserves-Meaning Rule` — CMF may reinterpret visually but never silently re-author the meaning
- `Composition-Depth Render Rule` — surfaces must exhibit depth, not flat montage
- `No-Dead-Polish Rule` — polish without meaning is rejected
- `SFL Subordinate-to-SDA Rule` — SFL packets inform but don't override SDA
- `Anti-Slop Guardrail Rule` — AI-generated genericness is gated out

**New Living Commentary Governance:**
- `Motion Grammar Compliance Rule` — every motion event must be drawn from the allowed vocabulary; banned motions cause immediate gate failure
- `Memetic Cue Moderation Rule` — max 1 meaningful memetic sound cue per 30 seconds (except comedy-dense surfaces at 1 per 10 seconds per Conscious Reactions format)
- `Living Still Priority Rule` — composition starts from a still field; motion is introduced selectively, never as a default
- `Voice-First Rendering Rule` — the coach's authentic recorded voice is the temporal master; all motion and sound cue timing syncs to voice beats, not the reverse
- `Anti-Motion-Overload Rule` — total motion events per 15-second window must not exceed the format family's `max_motion_events_per_15s` threshold
- `Internal Prototype Isolation Rule` — renders with `is_internal_prototype=True` must never enter the public delivery queue

**CBAR Mandate Enforcement:**

| Mandate | Source | Enforcement Mechanism |
|---|---|---|
| Phase4-M02: The Cinematic Meaning Rule | Epic 2, Story 2.1 | `EpicMeaningGate` rejects flat/corporate renders; extended to validate Living Commentary depth and atmosphere |
| Phase4-M06: The Sonic Prestige Rule | Epic 6, Story 6.1 | Sound cue timeline must use controlled palette; no random stock beds; memetic cue moderation enforced |
| Phase4-M05: The Actionable Rejection Rule | Epic 5, Story 5.1 | Gate rejections include specific remediation guidance (which layer lacks depth, which motion violates grammar) |
| Phase4-M02 (extended): Render-Preserves-Meaning | Epic 2 | `RenderPreservationReport` extended with Living Commentary dimensions |

### 3.5 Technical Decisions

| # | Decision | Rationale |
|---|---|---|
| TD-1 | Living Commentary is a realization path within `CMFArcGovernedRenderingPipeline`, not a separate engine | Prevents architectural fragmentation. The existing pipeline already has the right orchestration (gates, manifests, receipt chain). Living Commentary adds a planning layer and extends the manifest, not the pipeline skeleton. |
| TD-2 | Remotion Node.js + `@remotion/skia` replaces `SkiaRenderSidecarBridge` | Mandated by `HANDOVER_CONSOLIDATION_BLUEPRINTS.md` line 115. Centralizes rendering, enables React composition model, supports Rough Notation natively. |
| TD-3 | `RemotionRenderPayload` carries `CompleteEditingSessionRef` | The Complete Editing Session is the source of all assets (CRAL research, VIE backgrounds, SAM3 masks, coach cutouts). The Remotion server reads assets from the session, not from standalone URLs. |
| TD-4 | Sound cue timeline is owned by CMF, not FR-ERA3-17 | FR-ERA3-17 owns voice prompt sonic beds (1:1 with emotional jobs). CMF owns atmospheric and memetic sound cue timelines for rendered content. They consume different sonic assets from different registries. |
| TD-5 | Motion grammar is validated at planning time AND at manifest time (dual gate) | Planning-time validation catches vocabulary violations early. Manifest-time `MotionOverloadGate` catches cumulative overload that emerges from composition assembly. |
| TD-6 | Format family configs are persisted, not hardcoded | Configs evolve as new Living Commentary families emerge. Persisted configs allow runtime updates without code deployment. |
| TD-7 | Internal Prototype Routing uses `is_internal_prototype=True` flag on `ArcRenderJobRecord` | Prototypes are rendered using the same pipeline (ensuring visual fidelity) but routed to the coach's preview queue instead of the public delivery system. |

---

## 4. Implementation Plan

### Phase 1 — Living Commentary Models & Persistence (Tasks 1-5)

**Task 1:** Create `src/ccp/models/cmf_living_commentary_models.py` with all new Pydantic v2 models: `LivingCommentaryRealizationPlan`, `MotionGrammarProfile`, `SoundCueTimeline`, `LivingStillCompositionSpec`, `FormatFamilyRenderConfig`, `CompositionLayerStack`, `CompositionLayer`, `MotionEvent`, `SoundCueSlot`, `MotionOverloadAudit`, `InternalPrototypeRoutingDecision`, `RemotionRenderPayload`, `CompleteEditingSessionRef`.

**Task 2:** Extend `src/ccp/models/cmf_arc_render_models.py` — add `living_commentary_plan_id: str | None`, `editing_session_id: str | None`, `is_internal_prototype: bool = False`, `remotion_payload_id: str | None` to `ArcRenderJobRecord`. Add `motion_grammar_profile_id: str | None` and `sound_cue_slots: list[str] | None` to `BeatClusterPlan`.

**Task 3:** Extend `src/ccp/scripts/setup_supabase.py` — add 6 new tables: `cmf_living_commentary_plans`, `cmf_motion_grammar_profiles`, `cmf_sound_cue_timelines`, `cmf_living_still_specs`, `cmf_format_family_configs`, `cmf_remotion_payloads`.

**Task 4:** Create repository helpers in `src/ccp/services/` for Living Commentary plan CRUD operations.

**Task 5:** Seed format family config records for all 6 families (Quote, Comparison, Screenshot, Atmospheric, Cinematic Story, Animated Explainer) with initial thresholds.

### Phase 2 — Living Commentary Realization Planning (Tasks 6-10)

**Task 6:** Implement `LivingCommentaryRealizationPlanner` in `src/ccp/services/cmf_arc_governed_rendering.py` — consumes `CoalitionSpineInput` + `FormatFamilyRenderConfig` + `BeatClusterPlan[]`, produces `LivingCommentaryRealizationPlan`. Uses LLM prompt contract (JSON-mode) to resolve: which format family, which layers carry meaning, which motion vocabulary entries are appropriate per cluster, where sound cues should fall relative to voice beats.

**Task 7:** Implement `MotionGrammarResolver` — validates every proposed `MotionEvent` against the allowed vocabulary, rejects banned motions, computes per-layer motion intensity scores, produces `MotionGrammarProfile`. Vocabulary is typed as an enum, not free-text.

**Task 8:** Implement `SoundCueTimelineBuilder` — builds `SoundCueTimeline` from beat cluster boundaries, voice beat timestamps, and format family sound doctrine. Enforces memetic cue moderation (1 per 30s default, 1 per 10s for comedy-dense). Categorizes cues into: `punctuation`, `atmosphere`, `timing_reinforcement`, `emotional_continuity`, `memetic`.

**Task 9:** Implement `LivingStillCompositionResolver` — takes the base still field (VIE-generated background plate from Complete Editing Session) and computes selective motion assignments per layer. Outputs `LivingStillCompositionSpec` with: `still_field_asset_id`, `selective_motion_layers` (which layers get motion and what type), `motion_budget_total`, `parallax_displacement_px`.

**Task 10:** Implement `CompositionLayerStackAssembler` — assembles the 7-layer `CompositionLayerStack` from VIE assets, SAM3 masks, coach cutout, proof objects, and text overlays. Each `CompositionLayer` carries: `layer_index`, `z_depth`, `asset_ref`, `motion_events`, `opacity`, `blend_mode`.

### Phase 3 — Remotion Backend Integration (Tasks 11-14)

**Task 11:** Implement `RemotionManifestBuilder` — replaces `SkiaRenderManifestBuilder`. Produces `RemotionRenderPayload` containing: Remotion composition ID, frame-by-frame layer stack, motion keyframes, sound cue timeline, Rough Notation annotations, `@remotion/skia` displacement maps, and `CompleteEditingSessionRef`. Output format is a JSON manifest that the Remotion Node.js server can consume via `renderMedia()` or `renderStill()`.

**Task 12:** Implement `RemotionServerBridge` — replaces `SkiaRenderSidecarBridge`. HTTP client that posts `RemotionRenderPayload` to the centralized Remotion Node.js server endpoint. Handles: async render job submission, progress polling, output retrieval, error handling with circuit breaker. Supports both `renderMedia` (video) and `renderStill` (carousel frames, internal prototypes).

**Task 13:** Create Remotion composition templates in `src/remotion/compositions/` — one per format family:
- `LivingCommentaryQuote.tsx` — quote field + coach cutout + emphasis reveals
- `LivingCommentaryComparison.tsx` — dual objects + check/cross + coach judgment
- `LivingCommentaryScreenshot.tsx` — screenshot panel + callout + coach interpretation
- `LivingCommentaryAtmospheric.tsx` — softer field + ambient motion + fewer text objects
- `LivingCommentaryCinematicStory.tsx` — layered stills + memory objects + emotional pacing
- `LivingCommentaryAnimatedExplainer.tsx` — 2D avatar/cutout + Excalidraw strokes + timed sequences

**Task 14:** Implement `CompleteEditingSessionAdapter` — reads VIE-generated assets, SAM3 masks, coach cutouts, CRAL research, and transcript data from the Complete Editing Session payload. Provides typed accessors for all asset categories the Remotion manifest builder needs.

### Phase 4 — Gate Extensions & Anti-Overload (Tasks 15-18)

**Task 15:** Extend `FirstFrameAuthorityGate` — add Living Commentary surface-specific checks: layer 3 proof object must be legible (for Quote/Comparison/Screenshot families), coach cutout layer must be present and properly masked, background climate layer must have atmospheric depth. Existing thresholds (authority≥0.72, contrast≥0.65, recognizability≥0.70) remain.

**Task 16:** Extend `EpicMeaningGate` — add Living Commentary depth validation: at minimum 4 of 7 layers must carry meaningful content (no empty layers except for Atmospheric family which may use 3). Sonic bed must include format-appropriate atmosphere. Blandness threshold remains ≤0.15.

**Task 17:** Implement `MotionOverloadGate` (NEW) — validates cumulative motion intensity across all layers per 15-second window. Thresholds per family:
- Quote: ≤4 motion events per 15s
- Comparison: ≤5 motion events per 15s
- Screenshot: ≤3 motion events per 15s
- Atmospheric: ≤3 motion events per 15s
- Cinematic Story: ≤6 motion events per 15s
- Animated Explainer: ≤8 motion events per 15s

Produces `MotionOverloadAudit` with pass/fail per window and remediation hints.

**Task 18:** Implement `InternalPrototypeRouter` — checks `is_internal_prototype` flag on `ArcRenderJobRecord`. If `True`: render uses `renderStill` (static carousel frames), output is routed to coach preview queue (not public delivery), receipt chain logs prototype delivery, no format governance weekly allocation is consumed. The prototype is a pre-recording learning material carousel rendered by Remotion.

### Phase 5 — API Routes & Receipt Chain (Tasks 19-22)

**Task 19:** Extend `POST /api/cmf/arc-render/jobs` — accept new optional fields: `format_family: LivingCommentaryFormatFamily | None`, `editing_session_id: str | None`, `is_internal_prototype: bool = False`. When `format_family` is provided, the job enters Path B (Living Commentary).

**Task 20:** Add `POST /api/cmf/arc-render/jobs/{job_id}/living-commentary-plan` — returns the `LivingCommentaryRealizationPlan` for inspection/debugging.

**Task 21:** Add `GET /api/cmf/arc-render/jobs/{job_id}/remotion-payload` — returns the `RemotionRenderPayload` for the Remotion server.

**Task 22:** Extend receipt chain events — add: `living_commentary_plan_created`, `motion_grammar_validated`, `motion_overload_gate_passed`, `motion_overload_gate_failed`, `sound_cue_timeline_built`, `remotion_manifest_submitted`, `remotion_render_started`, `remotion_render_completed`, `internal_prototype_routed`.

### Phase 6 — Verification & Integration Tests (Tasks 23-26)

**Task 23:** Integration tests for Living Commentary realization planning — test all 6 format families produce valid plans with correct layer stacks and motion budgets.

**Task 24:** Integration tests for motion grammar — test that banned motions are rejected, allowed motions pass, overload thresholds trigger gate failure.

**Task 25:** Integration tests for sound cue moderation — test 1-per-30s rule, comedy-dense exception, empty timeline for atmospheric-dominant surfaces.

**Task 26:** Integration tests for Remotion manifest generation — test that `RemotionRenderPayload` is valid JSON, contains all 7 layers, references Complete Editing Session assets, and includes sound cue timeline.

---

## 5. Primary Output Schema (Pydantic v2)

All models use `pydantic.BaseModel`. No `Any` types. All fields explicitly typed.

```python
# --- File: src/ccp/models/cmf_living_commentary_models.py ---

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


# === ENUMS ===

class LivingCommentaryFormatFamily(str, Enum):
    QUOTE = "quote"
    COMPARISON = "comparison"
    SCREENSHOT = "screenshot"
    ATMOSPHERIC = "atmospheric"
    CINEMATIC_STORY = "cinematic_story"
    ANIMATED_EXPLAINER = "animated_explainer"


class MotionVocabularyEntry(str, Enum):
    """Allowed motion vocabulary — the ONLY motions permitted in Living Commentary."""
    PARALLAX_DEPTH = "parallax_depth"
    TWO_POINT_FIVE_D_LAYERING = "2.5d_layering"
    SLOW_PUSH_IN = "slow_push_in"
    DRIFT = "drift"
    SELECTIVE_FLOATING = "selective_floating"
    LIGHT_PULSE = "light_pulse"
    SHADOW_PASS = "shadow_pass"
    ATMOSPHERIC_PARTICLES = "atmospheric_particles"
    FILM_GRAIN = "film_grain"
    CONTROLLED_FLICKER = "controlled_flicker"
    HAND_DRAWN_REVEAL = "hand_drawn_reveal"


class BannedMotionType(str, Enum):
    """Banned motion types — presence of any triggers immediate gate failure."""
    HYPERACTIVE_POP_IN = "hyperactive_pop_in"
    ZOOM_SPAM = "zoom_spam"
    EXCESSIVE_BOUNCE = "excessive_bounce"
    EMOJI_EXPLOSION = "emoji_explosion"
    DEFAULT_TREND_ANIMATION = "default_trend_animation"
    KINETIC_TEXT_OVERLOAD = "kinetic_text_overload"
    TRANSITION_OUTRUNNING_VOICE = "transition_outrunning_voice"


class SoundCueCategory(str, Enum):
    PUNCTUATION = "punctuation"
    ATMOSPHERE = "atmosphere"
    TIMING_REINFORCEMENT = "timing_reinforcement"
    EMOTIONAL_CONTINUITY = "emotional_continuity"
    MEMETIC = "memetic"


class CompositionLayerIndex(int, Enum):
    BACKGROUND_CLIMATE = 1
    MID_BACKGROUND_FIELD = 2
    PROOF_OBJECT = 3
    SUPPORTING_MARKS = 4
    COACH_BODY = 5
    COACH_HEAD_GESTURE = 6
    FOREGROUND_ACCENT = 7


class MotionOverloadVerdict(str, Enum):
    PASS = "pass"
    FAIL_OVERLOADED = "fail_overloaded"
    WARN_NEAR_THRESHOLD = "warn_near_threshold"


class PrototypeRoutingDecision(str, Enum):
    ROUTE_TO_COACH_PREVIEW = "route_to_coach_preview"
    ROUTE_TO_DELIVERY = "route_to_delivery"


# === CORE MODELS ===

class MotionEvent(BaseModel):
    """A single motion event assigned to a composition layer."""
    event_id: str = Field(..., description="Unique motion event identifier")
    layer_index: CompositionLayerIndex
    motion_type: MotionVocabularyEntry
    start_ms: int = Field(..., ge=0)
    end_ms: int = Field(..., ge=0)
    intensity: float = Field(..., ge=0.0, le=1.0, description="0.0=stillness, 1.0=maximum allowed")
    displacement_px: float = Field(default=0.0, ge=0.0, le=20.0, description="Max pixel displacement for parallax/drift")
    easing: str = Field(default="ease-in-out", description="CSS easing function name")


class SoundCueSlot(BaseModel):
    """A single sound cue placed on the timeline."""
    slot_id: str = Field(..., description="Unique cue slot identifier")
    category: SoundCueCategory
    cue_asset_id: str = Field(..., description="Reference to controlled sonic asset registry")
    start_ms: int = Field(..., ge=0)
    duration_ms: int = Field(..., ge=0)
    gain_db: float = Field(default=-12.0, description="Gain relative to voice track")
    fade_in_ms: int = Field(default=100, ge=0)
    fade_out_ms: int = Field(default=200, ge=0)
    beat_cluster_id: str = Field(..., description="Which beat cluster this cue belongs to")
    is_memetic: bool = Field(default=False, description="True if this is a culturally familiar memetic cue")
    reinforces: str = Field(default="", description="What this cue reinforces: reveal, contrast, joke, reaction_beat")


class CompositionLayer(BaseModel):
    """A single layer in the 7-layer composition stack."""
    layer_index: CompositionLayerIndex
    z_depth: float = Field(..., ge=0.0, le=1.0)
    asset_ref: str = Field(..., description="Asset ID from Complete Editing Session or VIE output")
    asset_type: str = Field(..., description="background_plate, coach_cutout, proof_object, text_overlay, mark, accent")
    motion_events: list[MotionEvent] = Field(default_factory=list)
    opacity: float = Field(default=1.0, ge=0.0, le=1.0)
    blend_mode: str = Field(default="normal")
    rough_notation_annotations: list[str] = Field(default_factory=list, description="Rough Notation annotation IDs for text layers")
    skia_displacement_map_ref: str | None = Field(default=None, description="@remotion/skia displacement map asset for parallax layers")


class CompositionLayerStack(BaseModel):
    """The complete 7-layer composition for a Living Commentary render."""
    stack_id: str
    job_id: str
    layers: list[CompositionLayer] = Field(..., min_length=3, max_length=7, description="3-7 layers depending on format family")
    total_duration_ms: int = Field(..., ge=0)
    canvas_width: int = Field(default=1080, description="Vertical video width")
    canvas_height: int = Field(default=1920, description="Vertical video height")
    fps: int = Field(default=30)


class MotionGrammarProfile(BaseModel):
    """Motion grammar validation result for a Living Commentary render."""
    profile_id: str
    job_id: str
    format_family: LivingCommentaryFormatFamily
    allowed_motions_used: list[MotionVocabularyEntry]
    banned_motions_detected: list[BannedMotionType] = Field(default_factory=list)
    per_layer_intensity: dict[str, float] = Field(..., description="CompositionLayerIndex name → average intensity 0.0-1.0")
    total_motion_events: int = Field(..., ge=0)
    max_events_per_15s_window: int = Field(..., ge=0)
    max_events_per_15s_threshold: int = Field(..., ge=0)
    grammar_valid: bool = Field(..., description="True if no banned motions and within overload threshold")
    violations: list[str] = Field(default_factory=list, description="Human-readable violation descriptions")
    validated_at: datetime


class SoundCueTimeline(BaseModel):
    """Complete sound cue timeline for a Living Commentary render."""
    timeline_id: str
    job_id: str
    format_family: LivingCommentaryFormatFamily
    cues: list[SoundCueSlot]
    total_duration_ms: int = Field(..., ge=0)
    memetic_cue_count: int = Field(..., ge=0)
    memetic_cue_min_spacing_ms: int = Field(default=30000, description="30s default, 10s for comedy-dense")
    memetic_spacing_violations: list[str] = Field(default_factory=list)
    atmosphere_bed_asset_id: str | None = Field(default=None, description="Continuous atmosphere bed underneath cues")
    is_comedy_dense: bool = Field(default=False, description="If True, memetic cue spacing relaxed to 10s")
    timeline_valid: bool


class LivingStillCompositionSpec(BaseModel):
    """Living Still composition — selective motion on a still field."""
    spec_id: str
    job_id: str
    still_field_asset_id: str = Field(..., description="VIE-generated background plate from Editing Session")
    selective_motion_layers: list[CompositionLayerIndex] = Field(..., description="Which layers receive selective motion")
    motion_budget_total: int = Field(..., ge=0, le=15, description="Max total motion events across all layers")
    parallax_displacement_px: float = Field(default=4.0, ge=0.0, le=12.0, description="Max parallax shift in pixels")
    grain_intensity: float = Field(default=0.15, ge=0.0, le=0.5, description="Film grain overlay intensity")
    ambient_particle_density: float = Field(default=0.1, ge=0.0, le=0.4, description="Particle density for atmospheric layers")
    camera_drift_speed_px_per_s: float = Field(default=1.5, ge=0.0, le=5.0, description="Slow camera drift speed")
    flicker_frequency_hz: float = Field(default=0.3, ge=0.0, le=1.0, description="Light flicker frequency")
    starts_from_full_stillness: bool = Field(default=True, description="Must start from complete stillness for at least 500ms")


class FormatFamilyRenderConfig(BaseModel):
    """Per-family render config for Living Commentary format families."""
    config_id: str
    format_family: LivingCommentaryFormatFamily
    display_name: str
    required_layers: list[CompositionLayerIndex] = Field(..., description="Which layers MUST be populated")
    optional_layers: list[CompositionLayerIndex] = Field(default_factory=list)
    max_motion_events_per_15s: int = Field(..., ge=1, le=12)
    memetic_cue_spacing_ms: int = Field(default=30000, description="Min spacing between memetic sound cues")
    sonic_atmosphere_required: bool = Field(default=True)
    proof_object_required: bool = Field(default=False, description="True for Quote, Comparison, Screenshot families")
    coach_cutout_required: bool = Field(default=True)
    rough_notation_allowed: bool = Field(default=True)
    living_still_priority: bool = Field(default=True, description="True = start from still, introduce selective life")
    typical_duration_range_ms: tuple[int, int] = Field(default=(30000, 90000), description="(min_ms, max_ms)")
    ingredient_description: str = Field(..., description="Human-readable description of visual ingredients")


class CompleteEditingSessionRef(BaseModel):
    """Reference to the Complete Editing Session payload."""
    session_id: str
    coach_id: str
    lesson_id: str
    cral_research_ref: str | None = Field(default=None, description="CRAL research asset path")
    vie_background_plates: list[str] = Field(default_factory=list, description="VIE-generated background plate asset IDs")
    sam3_masks: list[str] = Field(default_factory=list, description="SAM3 segmentation mask asset IDs")
    coach_cutout_asset_id: str | None = Field(default=None, description="Coach cutout from SAM3 masking")
    coach_video_asset_id: str | None = Field(default=None, description="Raw authentic coach video recording")
    coach_audio_asset_id: str | None = Field(default=None, description="Extracted authentic coach audio")
    transcript_ref: str | None = Field(default=None, description="Transcription asset path")
    carousel_frames: list[str] = Field(default_factory=list, description="Pre-rendered static carousel frame IDs")
    drafting_voice_notes: list[str] = Field(default_factory=list, description="3 voice note asset IDs from drafting session")


class LivingCommentaryRealizationPlan(BaseModel):
    """Master render plan for a Living Commentary piece — the central artifact of this spec."""
    plan_id: str
    job_id: str
    format_family: LivingCommentaryFormatFamily
    format_config_id: str = Field(..., description="FK to FormatFamilyRenderConfig")
    editing_session_ref: CompleteEditingSessionRef
    layer_stack: CompositionLayerStack
    motion_grammar: MotionGrammarProfile
    sound_cue_timeline: SoundCueTimeline
    living_still_spec: LivingStillCompositionSpec | None = Field(default=None, description="Present for Living Still surfaces")
    beat_cluster_ids: list[str] = Field(..., description="Beat clusters from upstream arc planning")
    sfl_perceptual_plan_id: str | None = Field(default=None, description="FK to RenderPerceptualPlan if SFL-aware")
    is_internal_prototype: bool = Field(default=False)
    archetype_id: str | None = Field(default=None, description="Archetype container reference")
    primitive_coalition_ids: list[str] = Field(default_factory=list, description="Governing primitive IDs")
    created_at: datetime
    plan_valid: bool = Field(..., description="True if motion grammar + sound cue + layer stack all valid")


class RemotionRenderPayload(BaseModel):
    """Payload sent to the centralized Remotion Node.js server."""
    payload_id: str
    job_id: str
    remotion_composition_id: str = Field(..., description="Which Remotion composition template to use (e.g., LivingCommentaryQuote)")
    layer_stack_json: str = Field(..., description="Serialized CompositionLayerStack")
    motion_keyframes_json: str = Field(..., description="Per-layer motion keyframe data for @remotion/skia")
    sound_cue_timeline_json: str = Field(..., description="Serialized SoundCueTimeline")
    rough_notation_config_json: str = Field(default="{}", description="Rough Notation highlight annotations")
    skia_displacement_maps: list[str] = Field(default_factory=list, description="@remotion/skia displacement map asset refs")
    editing_session_ref: CompleteEditingSessionRef
    render_mode: str = Field(..., description="'renderMedia' for video, 'renderStill' for static frames")
    output_format: str = Field(default="mp4", description="mp4, webm, or png (for stills)")
    fps: int = Field(default=30)
    width: int = Field(default=1080)
    height: int = Field(default=1920)
    duration_ms: int = Field(..., ge=0)
    created_at: datetime


class MotionOverloadAudit(BaseModel):
    """Result of the MotionOverloadGate validation."""
    audit_id: str
    job_id: str
    verdict: MotionOverloadVerdict
    windows_evaluated: int = Field(..., ge=0)
    max_events_in_any_window: int = Field(..., ge=0)
    threshold: int = Field(..., ge=0)
    overloaded_windows: list[dict[str, int]] = Field(default_factory=list, description="[{start_ms, end_ms, event_count}]")
    remediation_hints: list[str] = Field(default_factory=list)
    audited_at: datetime


class InternalPrototypeRoutingDecision(BaseModel):
    """Decision record for internal prototype routing."""
    decision_id: str
    job_id: str
    is_internal_prototype: bool
    routing_decision: PrototypeRoutingDecision
    render_mode: str = Field(..., description="'renderStill' for prototypes, 'renderMedia' for production")
    coach_preview_queue_id: str | None = Field(default=None)
    receipt_chain_block: str | None = Field(default=None)
    decided_at: datetime
```

---

## 6. Backward Compatibility & Fallback

### 6.1 Render Path Coexistence

Jobs created **without** a `format_family` field continue to use Path A (standard arc-governed rendering). The `LivingCommentaryRealizationPlanner` is only invoked when `format_family` is present. All existing tests pass without modification.

### 6.2 Remotion Migration Fallback

During the transition period while the Remotion Node.js server is being deployed:
- If `RemotionServerBridge.submit()` returns `503 Service Unavailable`, the job enters `render_pending_remotion` status
- Jobs in `render_pending_remotion` are retried via exponential backoff (max 3 retries over 15 minutes)
- If all retries fail, the job is marked `failed_remotion_unavailable` and a receipt chain event is logged
- **No fallback to legacy Skia sidecar** — the sidecar is deprecated and must not be used as a safety net

### 6.3 Complete Editing Session Missing Assets

If the Complete Editing Session payload is missing expected assets:
- Missing VIE background plates → use solid color gradient from DPA palette as layer 1
- Missing SAM3 masks → coach cutout layer (5) is omitted; minimum layer count reduced by 1
- Missing coach audio → job cannot proceed (voice-first rendering rule); status `blocked_missing_audio`
- Missing proof objects (for Quote/Comparison/Screenshot) → job cannot proceed; status `blocked_missing_proof`

### 6.4 SFL Interoperability

When both SFL (`RenderPerceptualPlan`) and Living Commentary (`LivingCommentaryRealizationPlan`) are present:
- SFL `CompositionDepthRenderProfile` weights are used to modulate Living Still parallax intensity
- SFL `VariationRenderHints` inform which layers receive asymmetry
- SFL `TemporalCraftHints` inform sound cue placement timing
- Living Commentary motion grammar takes precedence over SFL variation hints if they conflict
- `RenderPreservationReport` is extended with Living Commentary dimensions: `motion_grammar_preserved`, `sound_cue_doctrine_preserved`, `living_still_integrity_preserved`, `layer_depth_preserved`

---

## 7. Tasks

| # | Task | Files | Depends On | Est. |
|---|---|---|---|---|
| 1 | Create `cmf_living_commentary_models.py` | `src/ccp/models/` | — | 2d |
| 2 | Extend `cmf_arc_render_models.py` with LC fields | `src/ccp/models/` | T1 | 0.5d |
| 3 | Add 6 new Supabase tables | `src/ccp/scripts/` | T1 | 1d |
| 4 | Repository helpers for LC plan CRUD | `src/ccp/services/` | T3 | 1d |
| 5 | Seed 6 format family configs | `src/ccp/scripts/` | T3 | 0.5d |
| 6 | `LivingCommentaryRealizationPlanner` | `src/ccp/services/` | T1, T5 | 3d |
| 7 | `MotionGrammarResolver` | `src/ccp/services/` | T1 | 2d |
| 8 | `SoundCueTimelineBuilder` | `src/ccp/services/` | T1 | 2d |
| 9 | `LivingStillCompositionResolver` | `src/ccp/services/` | T1 | 2d |
| 10 | `CompositionLayerStackAssembler` | `src/ccp/services/` | T1, T9 | 2d |
| 11 | `RemotionManifestBuilder` | `src/ccp/services/` | T1, T10 | 2d |
| 12 | `RemotionServerBridge` | `src/ccp/services/` | T11 | 2d |
| 13 | Remotion composition templates (6) | `src/remotion/compositions/` | T11 | 4d |
| 14 | `CompleteEditingSessionAdapter` | `src/ccp/services/` | T1 | 1d |
| 15 | Extend `FirstFrameAuthorityGate` | `src/ccp/services/` | T6, T10 | 1d |
| 16 | Extend `EpicMeaningGate` | `src/ccp/services/` | T6, T10 | 1d |
| 17 | `MotionOverloadGate` | `src/ccp/services/` | T7 | 1d |
| 18 | `InternalPrototypeRouter` | `src/ccp/services/` | T12 | 1d |
| 19 | Extend API routes | `src/ccp/api/` | T6, T12, T18 | 1d |
| 20 | LC plan inspection route | `src/ccp/api/` | T19 | 0.5d |
| 21 | Remotion payload route | `src/ccp/api/` | T19 | 0.5d |
| 22 | Receipt chain events (9 new events) | `src/ccp/core/` | T6-T18 | 1d |
| 23 | Integration tests: LC planning (6 families) | `tests/integration/` | T6 | 2d |
| 24 | Integration tests: motion grammar | `tests/integration/` | T7, T17 | 1d |
| 25 | Integration tests: sound cue moderation | `tests/integration/` | T8 | 1d |
| 26 | Integration tests: Remotion manifest | `tests/integration/` | T11, T12 | 1d |

**Total: 26 tasks across 6 phases. Estimated: ~35 engineering days.**

---

## 8. Acceptance Criteria

### AC-12-LC.1: Format Family Resolution
**GIVEN** a `CoalitionSpineInput` with a `selected_format` that maps to a Living Commentary format family
**WHEN** `CMFArcGovernedRenderingPipeline.create_job()` is called with `format_family=LivingCommentaryFormatFamily.QUOTE`
**THEN** the job enters Path B, a `LivingCommentaryRealizationPlan` is created with `format_family="quote"`, and the `FormatFamilyRenderConfig` for Quote is loaded with `proof_object_required=True`.

**FAILURE EXAMPLE:** A job is created with `format_family="quote"` but the planner loads the Atmospheric config (which has `proof_object_required=False`), resulting in a render without the quote field in layer 3. This violates `Phase4-M02: The Cinematic Meaning Rule` — the quote IS the meaning.

---

### AC-12-LC.2: 7-Layer Composition Stack
**GIVEN** a Living Commentary realization plan for the Comparison format family
**WHEN** the `CompositionLayerStackAssembler` produces the layer stack
**THEN** the stack contains at minimum layers 1 (background climate), 3 (comparison object), 5 (coach body), and 7 (foreground accent). Each layer has valid `z_depth` values in ascending order. The `canvas_width` is 1080 and `canvas_height` is 1920.

**FAILURE EXAMPLE:** The assembler produces a stack with only 2 layers (coach cutout + text), rendering a flat talking-head-with-captions. This violates the `Composition-Depth Render Rule` and produces the exact commoditized aesthetic Living Commentary exists to prevent.

---

### AC-12-LC.3: Motion Grammar Compliance
**GIVEN** a motion grammar profile with proposed `MotionEvent` entries
**WHEN** `MotionGrammarResolver.validate()` processes the events
**THEN** all events use only `MotionVocabularyEntry` types. Any presence of `BannedMotionType` (hyperactive pop-ins, zoom spam, excessive bounce, emoji explosions, kinetic text overload, transitions outrunning voice) causes immediate `grammar_valid=False` with violation descriptions.

**FAILURE EXAMPLE:** A render plan includes `zoom_spam` on the proof object layer to "make it pop." The `MotionGrammarResolver` returns `grammar_valid=True` because the validator only checked layer names, not motion types. The render produces generic social media aesthetic. This violates the `Motion Grammar Compliance Rule`.

---

### AC-12-LC.4: Motion Overload Gate
**GIVEN** a Living Commentary render with the Screenshot format family (`max_motion_events_per_15s=3`)
**WHEN** the `MotionOverloadGate` evaluates a 15-second window containing 5 motion events
**THEN** the gate returns `MotionOverloadVerdict.FAIL_OVERLOADED` with `overloaded_windows` listing the specific window and `remediation_hints` suggesting which low-priority events to remove.

**FAILURE EXAMPLE:** The gate passes a Screenshot render with 8 motion events in a single 15-second window because the threshold check uses total duration instead of per-window evaluation. The render looks hyperactive and violates the `Anti-Motion-Overload Rule`.

---

### AC-12-LC.5: Memetic Sound Cue Moderation
**GIVEN** a `SoundCueTimeline` for a non-comedy-dense surface with `memetic_cue_min_spacing_ms=30000`
**WHEN** the timeline contains two memetic cues spaced 15 seconds apart
**THEN** the timeline is marked `timeline_valid=False` with `memetic_spacing_violations` listing the specific cues and their actual spacing.

**FAILURE EXAMPLE:** A Cinematic Story render contains 4 memetic cues in 60 seconds (one every 15 seconds). The validator passes because it only counts total cues, not spacing. The render sounds like a meme compilation, not a cinematic story. This violates the `Memetic Cue Moderation Rule` and `Phase4-M06: The Sonic Prestige Rule`.

---

### AC-12-LC.6: Living Still Priority
**GIVEN** a Living Commentary render for the Atmospheric format family
**WHEN** the `LivingStillCompositionResolver` produces the `LivingStillCompositionSpec`
**THEN** `starts_from_full_stillness=True`, `motion_budget_total ≤ 15`, `parallax_displacement_px ≤ 12.0`, and at most 3 layers receive selective motion. The composition begins with 500ms of complete stillness before any motion is introduced.

**FAILURE EXAMPLE:** An Atmospheric render starts with immediate parallax on all 7 layers at maximum intensity. There is no moment of stillness. The viewer's eye has no entry point. This violates the `Living Still Priority Rule` — composition must start from a still field and introduce selective life.

---

### AC-12-LC.7: Remotion Manifest Validity
**GIVEN** a completed `LivingCommentaryRealizationPlan` that passes all gates
**WHEN** `RemotionManifestBuilder.build()` produces a `RemotionRenderPayload`
**THEN** the payload contains: valid `remotion_composition_id` matching the format family, serialized `CompositionLayerStack` as JSON, motion keyframes for `@remotion/skia`, serialized `SoundCueTimeline`, `CompleteEditingSessionRef` with valid `session_id`, and `render_mode` set to `renderMedia` (video) or `renderStill` (prototypes).

**FAILURE EXAMPLE:** The manifest builder produces a payload without `editing_session_ref`, causing the Remotion server to fail when trying to resolve VIE background plate assets. This violates TD-3 — all assets must be referenced through the Complete Editing Session.

---

### AC-12-LC.8: Internal Prototype Routing
**GIVEN** a job with `is_internal_prototype=True`
**WHEN** the `InternalPrototypeRouter` evaluates the job
**THEN** `render_mode` is forced to `renderStill`, the output is routed to `coach_preview_queue_id` (never public delivery), and a receipt chain event `internal_prototype_routed` is logged. The prototype does NOT consume a weekly format allocation from `FormatGovernanceEngine`.

**FAILURE EXAMPLE:** An internal prototype render is sent to the public delivery queue and counted against the coach's weekly content allocation. The coach's audience sees an unfinished learning prototype as published content. This violates the `Internal Prototype Isolation Rule`.

---

### AC-12-LC.9: Voice-First Temporal Mastering
**GIVEN** a Living Commentary render with coach authentic audio
**WHEN** sound cues and motion events are timed
**THEN** all `SoundCueSlot.start_ms` values align to voice beat boundaries (extracted from transcript timestamps). All `MotionEvent.start_ms` values synchronize to voice emphasis points. The coach's authentic voice track is the temporal master — no motion or sound cue may start before the voice beat it reinforces.

**FAILURE EXAMPLE:** A sound cue is placed at t=5000ms but the corresponding voice emphasis beat occurs at t=5800ms. The cue precedes the voice, creating a "pre-emptive" feel that undermines the voice-first doctrine. This violates the `Voice-First Rendering Rule`.

---

### AC-12-LC.10: Existing Gate Backward Compatibility
**GIVEN** a standard (non-Living Commentary) arc render job without `format_family`
**WHEN** the job is processed by the pipeline
**THEN** the existing `FirstFrameAuthorityGate` and `EpicMeaningGate` behavior is unchanged. Existing thresholds (authority≥0.72, contrast≥0.65, recognizability≥0.70, blandness≤0.15) apply. No Living Commentary planning is invoked. All existing integration tests pass without modification.

**FAILURE EXAMPLE:** A standard arc render job fails the `EpicMeaningGate` because the gate now checks for Living Commentary layer depth (minimum 4 of 7 layers) — a check that should only apply to Living Commentary surfaces. This is a regression that violates backward compatibility.

---

## 9. Dependencies

### 9.1 Internal Service Dependencies

| Service | Dependency Type | What This Spec Needs |
|---|---|---|
| `CMFArcGovernedRenderingPipeline` | EXTENDS | Add Living Commentary planning layer, Remotion manifest builder, prototype routing |
| `AbelVCBGenerator` | CONSUMES | `generate()` for VCB generation — augmented with LC layer depth hints |
| `FormatGovernanceEngine` | CONSUMES | `apply_format_governance()` for weekly allocation (excludes prototypes) |
| `SaliencyAnalysisService` | CONSUMES | `analyze()` for proof object saliency in layer 3 |
| `CourseVideoPipeline` | CONSUMES | `execute()` for Animated Explainer when surface is educational |
| `ReceiptChain` | CONSUMES | `log()` for all gate verdicts and render events |
| `CircuitBreaker` | CONSUMES | Pipeline failure protection |
| `DPAEngine` | CONSUMES | `resolve()` for brand-consistent color palette in layers 1, 4, 7 |

### 9.2 Upstream Spec Dependencies

| Spec | What It Provides |
|---|---|
| FR-ERA3-16 (Archetype Container Runtime) | Archetype → format family mapping, delivery recipes |
| FR-ERA3-17 (Voice Prompt Engine) | Sonic bed registry (FR-ERA3-17 owns voice beds; this spec owns content sound cues) |
| FR-ERA3-35B (Content Benchmark Profiles) | Presence-weighted scoring dimensions for Living Commentary |
| FR-ERA3-35C (Eval Card System) | Living Commentary eval cards |
| FR-ERA3-25 (SFL Functions) | `SubliminalFunctionStackPacket` for SFL-aware rendering |
| FR-ERA3-27 (Perceptual Scoring) | `PerceptualInfluenceReport` for SFL perceptual plan |

### 9.3 Infrastructure Dependencies

| Component | Status | Requirement |
|---|---|---|
| **Remotion Node.js Server** | NET NEW | Centralized server with `renderMedia()` and `renderStill()` APIs. Must support `@remotion/skia` CanvasKit WebAssembly. Must accept `RemotionRenderPayload` via HTTP POST. |
| **Complete Editing Session Store** | NET NEW (defined in Handover Blueprints) | Stateful session storage for CRAL research, VIE assets, SAM3 masks, coach recordings. Must support `CompleteEditingSessionRef` lookups by `session_id`. |
| **Controlled Sonic Asset Registry** | NET NEW | Registry of approved sound cue assets categorized by `SoundCueCategory`. Memetic cues must be tagged. No random stock tracks. |
| **VIE Background Plate Generator** | EXISTING (reversed deprecation) | VIE generates background plates stored in Complete Editing Session. |
| **SAM3 Masking Pipeline** | EXISTING | SAM3 masks coach cutout and produces depth maps for `@remotion/skia` displacement. |

---

## 10. Testing Strategy

### 10.1 Unit Tests (following existing `pytest` patterns)

| Test Module | Coverage |
|---|---|
| `test_living_commentary_models.py` | All Pydantic model validation — required fields, enum constraints, value ranges, banned type detection |
| `test_motion_grammar_resolver.py` | Allowed vocabulary acceptance, banned motion rejection, per-layer intensity calculation |
| `test_sound_cue_timeline_builder.py` | Cue placement, memetic spacing validation, comedy-dense exception, empty timeline for atmosphere-only |
| `test_living_still_resolver.py` | Still field priority, motion budget limits, parallax displacement bounds |
| `test_format_family_configs.py` | All 6 config records load correctly, threshold values match spec |

### 10.2 Integration Tests (in `tests/integration/`)

**`test_fr_era3_12_living_commentary_planning.py`:**
```python
class TestLivingCommentaryRealizationPlanningByFormatFamily:
    """Test that all 6 format families produce valid realization plans."""
    
    def test_quote_family_produces_plan_with_proof_object(self):
        # Create job with format_family=QUOTE
        # Assert plan has layer 3 (proof object) populated
        # Assert motion grammar valid
        # Assert sound cue timeline valid
        pass

    def test_comparison_family_produces_dual_object_layout(self):
        # Assert layer 3 contains dual objects
        # Assert check/cross marks in layer 4
        pass

    def test_screenshot_family_requires_screenshot_panel(self):
        # Assert layer 3 contains screenshot asset
        # Assert max_motion_events_per_15s == 3 (lowest threshold)
        pass

    def test_atmospheric_family_allows_reduced_layers(self):
        # Assert minimum 3 layers (not 4)
        # Assert softer motion budget
        pass

    def test_cinematic_story_family_uses_layered_stills(self):
        # Assert multiple VIE plates in layers 1-2
        # Assert emotional pacing in sound cue timeline
        pass

    def test_animated_explainer_routes_to_course_video_when_educational(self):
        # Assert CourseVideoPipeline.execute() is called for educational content
        pass
```

**`test_fr_era3_12_motion_grammar_gate.py`:**
```python
class TestMotionGrammarGateRejectsBannedMotions:
    def test_zoom_spam_causes_immediate_failure(self):
        # Include ZOOM_SPAM in motion events
        # Assert grammar_valid == False
        # Assert violation message mentions "zoom_spam"
        pass

    def test_emoji_explosion_causes_immediate_failure(self):
        pass

class TestMotionOverloadGateEnforcesPerWindowThreshold:
    def test_screenshot_family_blocks_above_3_events_per_15s(self):
        pass

    def test_cinematic_story_allows_up_to_6_events_per_15s(self):
        pass
```

**`test_fr_era3_12_sound_cue_moderation.py`:**
```python
class TestMemeticCueModeration:
    def test_two_memetic_cues_within_30s_fails_validation(self):
        pass

    def test_comedy_dense_allows_10s_spacing(self):
        pass

    def test_atmosphere_cues_not_counted_as_memetic(self):
        pass
```

**`test_fr_era3_12_remotion_manifest.py`:**
```python
class TestRemotionManifestGeneration:
    def test_manifest_contains_all_7_layers_for_comparison(self):
        pass

    def test_manifest_references_editing_session(self):
        pass

    def test_prototype_uses_render_still_mode(self):
        pass

class TestInternalPrototypeRouting:
    def test_prototype_never_enters_public_delivery(self):
        pass

    def test_prototype_does_not_consume_weekly_allocation(self):
        pass
```

### 10.3 Non-Regression Requirements

- No existing test in `test_fr_era3_12_cmf_arc_governed_rendering.py` may fail after this update
- No existing test in `test_fr_era3_12_cmf_sfl_rendering.py` may fail after this update
- Standard (non-LC) jobs must not invoke any Living Commentary planning code
- `FirstFrameAuthorityGate` thresholds for non-LC jobs remain unchanged
- `EpicMeaningGate` layer-count checks must only apply to LC jobs
- All `BannedMotionType` entries must trigger failure — a test that passes with a banned motion type is itself a test failure

### 10.4 Summary

This update extends the CMF Arc-Governed Rendering pipeline from an SFL-aware realization engine into a **Living Commentary-aware, Remotion-native realization engine**. It folds FR-ERA3-58 (Realization Engine), FR-ERA3-59 (Motion Grammar & Layering), and FR-ERA3-60 (Sound Cue & Atmosphere) into the existing pipeline as a planning layer extension, not a separate engine. The 7-layer composition model, motion grammar vocabulary, sound cue doctrine with memetic moderation, Living Still philosophy, and format-family render configs give the CMF renderer the vocabulary to produce coach-led, atmosphere-rich, voice-first content that cannot be commoditized. The Remotion Node.js + `@remotion/skia` backend and Complete Editing Session integration bring the rendering infrastructure into alignment with the May 2026 architectural pivot. The Internal Prototype Routing Layer ensures pre-recording carousels reach the coach as learning material without polluting the public delivery queue.

---

*End of spec. Version 3.0. Living Commentary is a CMF extension, not a separate engine.*
