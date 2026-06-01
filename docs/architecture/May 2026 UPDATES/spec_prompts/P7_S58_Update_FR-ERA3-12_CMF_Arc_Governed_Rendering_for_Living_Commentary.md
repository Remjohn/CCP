# Spec Prompt: FR-ERA3-12 Update — CMF Arc Governed Rendering for Living Commentary

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-12
SPEC_TITLE:      Update CMF Arc Governed Rendering for Living Commentary
PHASE:           7 — Living Commentary & Coach Communication Stack
SOURCE_PRD:      PRD-02, PRD-03
MAPPED_STORIES:  Living Commentary realization engine integration, motion grammar and layering adoption, sound cue and atmosphere doctrine, Living Still composition, format-family render configs
CBAR_MANDATES:   Render-Preserves-Meaning Rule, Composition-Depth Render Rule, No-Dead-Polish Rule, SFL Subordinate-to-SDA Rule, Anti-Slop Guardrail Rule
BACKEND_REL:     UPDATE existing CMF rendering runtime — MUST use Remotion Node.js backend + @remotion/skia and the Complete Editing Session payload. MUST consume Living Commentary realization families, motion grammar, sound cue doctrine, and Living Still compositions without creating a separate engine
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-12_CMF_Arc_Governed_Rendering_Tech_Spec_UPDATED_FOR_LIVING_COMMENTARY.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This update folds three originally proposed standalone specs into the existing CMF rendering runtime:
> - `FR-ERA3-58` Living Commentary Realization Engine
> - `FR-ERA3-59` Living Commentary Motion Grammar And Layering
> - `FR-ERA3-60` Living Commentary Sound Cue And Atmosphere
>
> Living Commentary is a **realization layer**, not a new archetype system. The CMF renderer must learn to realize existing archetypes through coach-led, reaction-first, voice-first, atmosphere-rich surfaces.
>
> Hard rule: Living Commentary is an extension of CMF rendering. Do NOT create a separate engine.
>
> **REMOTION + COMPLETE EDITING SESSION CONTEXT:**
> The legacy C++ Skia sidecar and python-based CMF queues are fully deprecated. All vertical video and static compositions are rendered on the backend via Remotion Node.js + `@remotion/skia`. The generation payload must be structured around the Complete Editing Session state wrapper to preserve all research and asset states.

> [!IMPORTANT]
> **MANDATORY LIVING COMMENTARY SOURCE SET (9+ REFERENCE FILES):**
> - `lab/CCP APRIL Updates/05_Core_Experience/Living_Commentary_Realization_Layer_Source_of_Truth.md`
> - `lab/CCP APRIL Updates/01_Architecture_PRDs/Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md`
> - `docs/architecture/HANDOVER_CONSOLIDATION_BLUEPRINTS.md` (Master handover record)
> - `docs/architecture/May 2026 UPDATES/Architectural_Audit_Trigger_First_Vision_Visual_Engines.md` (Pivots audit, Remotion mandate)
> - `docs/architecture/april_updates/FR-ERA3-12_CMF_Arc_Governed_Rendering_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-12_CMF_Arc_Governed_Rendering_Tech_Spec_UPDATED_FOR_SFL.md`
> - `docs/architecture/april_updates/FR-ERA3-17_Voice_Prompt_Engine_Tech_Spec.md`
> - `docs/prd/modules/PRD_02_CCF_Content_Factory.md` (PRD Module)
> - `docs/prd/modules/PRD_03_CMF_Media_Factory.md` (PRD Module)

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-02`, `PRD-03`. **PROOF:** Quote the exact lines that establish CCF→CMF handoff and render responsibility.
3. Master blueprints: `HANDOVER_CONSOLIDATION_BLUEPRINTS.md` and the pivots audit. **PROOF:** Quote the Remotion Node.js mandate, Complete Editing Session wrapper, and synthetic voice ban.
4. Living Commentary source set: both mandatory docs above. **PROOF:** Quote the 7-layer composition model, the motion vocabulary list, the sound doctrine rules, and the memetic sound cue moderation law (1 per 30 seconds).
5. Existing FR-ERA3-12 specs: read both the original and SFL-updated versions. **PROOF:** Quote the render pipeline stages and schema names.
- Pre-work must require reading: existing CMF render services, Remotion Node.js rendering backend and @remotion/skia composition templates, SFL-updated spec, voice prompt engine spec. **PROOF:** Quote the render pipeline stages and schema names.
6. Voice Prompt Engine: read FR-ERA3-17. **PROOF:** Quote how sound/voice assets are currently managed.
7. Existing backend references: read real files for CMF render services, Remotion composition pipelines, and session schemas. **PROOF:** Quote real method signatures or template exports.
7. Existing models: read render-result, visual, media, and packet model files.
8. Existing test patterns: read 2 `tests/integration/` files covering render or media pipeline behavior.

**PRE-WORK LOG — required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 350 LINES

§1 Files Read (>=9) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=4 files) | §3.3 Living Commentary render contracts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=4 phases, >=14 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- This must be written as an **update spec** extending the existing CMF renderer
- Define canonical schemas for:
  - `LivingCommentaryRealizationPlan` — the master render plan for a Living Commentary piece
  - `MotionGrammarProfile` — allowed motion vocabulary (parallax, 2.5D layering, slow push-in, drift, selective floating, light pulse, shadow pass, atmospheric particles, film grain, controlled flicker, hand-drawn reveal) plus banned motions (hyperactive pop-ins, zoom spam, excessive bounce, emoji explosions, kinetic text overload)
  - `SoundCueTimeline` — punctuation, atmosphere, timing reinforcement, emotional continuity, memetic cue slots with moderation rules
  - `LivingStillCompositionSpec` — selective-motion composition starting from a still field
  - `FormatFamilyRenderConfig` — per-family config for Quote, Comparison, Screenshot, Atmospheric, Cinematic Story, and Animated Explainer Living Commentary families
- Define the 7-layer composition model:
  1. background climate
  2. mid-background field objects
  3. screenshot / quote / comparison object
  4. supporting marks and icons
  5. coach body
  6. coach head / gesture emphasis
  7. foreground accent or text
- Define how sound cue doctrine integrates with FR-ERA3-17 Voice Prompt Engine as a dependency (not the owner)
- Define anti-motion-overload guardrails
- Define memetic sound cue moderation: max 1 meaningful cue per 30 seconds unless the surface is explicitly comedy-dense
- **MUST define the Internal Prototype Routing Layer:** Introduce the `is_internal_prototype=True` flag for rendering Internal Carousel Prototypes that are routed back to the coach as pre-recording learning material rather than published externally.

**REJECTION:** Treats Living Commentary as a separate engine rather than CMF extension | no motion grammar schema | no sound cue timeline | no Living Still composition spec | no format family configs | no 7-layer model | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
