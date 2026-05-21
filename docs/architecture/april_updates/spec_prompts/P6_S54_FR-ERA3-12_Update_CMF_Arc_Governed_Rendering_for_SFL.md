# Spec Prompt: FR-ERA3-12 Update - CMF Arc Governed Rendering for SFL

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-12
SPEC_TITLE:      Update CMF Arc Governed Rendering for SFL
PHASE:           6 - SFL Runtime Integration
SOURCE_PRD:      PRD-02, PRD-03
MAPPED_STORIES:  SFL Wave 2 render propagation - perceptual render preservation, composition depth rendering, variation-aware visual/temporal realization, scoring-card and audit-surface readiness
CBAR_MANDATES:   Render-Preserves-Meaning Rule, Composition-Depth Render Rule, Variation-Aliveness Rule, No-Dead-Polish Rule, SFL Subordinate-to-SDA Rule
BACKEND_REL:     UPDATE existing CMF rendering runtime - MUST consume archetype/runtime outputs and remain interoperable with FR-ERA3-25/26/27 without swallowing evaluator ownership
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-12_CMF_Arc_Governed_Rendering_Tech_Spec_UPDATED_FOR_SFL.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This is an update spec for CMF rendering, not a new media engine.
>
> The purpose is to define how rendering preserves or realizes:
> - subliminal function intent
> - composition depth profiles
> - repetition with variation
> - rhythmic structure
> - strategic ambiguity
> - asymmetry / resonance / salience variation
>
> It must explain how these affect:
> - script rendering
> - video rendering
> - frame selection
> - score-card and audit-board surfaces
>
> Hard rule: CMF should realize SFL, not redefine it.

> [!IMPORTANT]
> **MANDATORY SFL SOURCE SET - READ IN EVERY SFL INTEGRATION SPEC SESSION:**
> - `lab/subliminal_function_layer_for_ccp_v_1.md`
> - `lab/phase0_eval_card_scoring_model_v_1.md`
> - `lab/ccp_biological_orchestration_model_v_1.md`
> - `lab/OmniShotCut Holistic Relational Shot Boundary.md`
> - `docs/prd/modules/PRD_02_CCF_Content_Factory.md`
> - `docs/prd/modules/PRD_03_CMF_Media_Factory.md`
> - `docs/architecture/april_updates/FR-ERA3-12_CMF_Arc_Governed_Rendering_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-25_Subliminal_Function_Library_And_Taxonomy_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-27_Perceptual_Influence_Evaluator_Tech_Spec.md`

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-02`, `PRD-03`. **PROOF:** Quote the exact lines that establish CCF->CMF handoff and render responsibility.
3. SFL source set: all mandatory docs above. **PROOF:** Quote one concrete structural claim from each file.
4. Existing FR specs: read `FR-ERA3-12`, `FR-ERA3-25`, and `FR-ERA3-27`. **PROOF:** Quote the render/evaluator responsibilities from each.
5. Existing backend references: read real files for render services, composition, frame export, video analysis, or media result contracts. **PROOF:** Quote real method signatures.
6. Existing models: read render-result / visual / media / packet model files.
7. Existing test patterns: read 2 `tests/integration/` files covering render or media pipeline behavior.
8. Video-structure precedent: read the OmniShotCut note and state how shot / transition / temporal relations should inform but not fully dominate CMF rendering.

**PRE-WORK LOG - required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 320 LINES

§1 Files Read (>=9) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=4 files) | §3.3 Render packets / media contracts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=4 phases, >=14 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- This must be written as an **update spec**
- Define canonical schemas for:
  - `RenderPerceptualPlan`
  - `CompositionDepthRenderProfile`
  - `VariationRenderHints`
  - `RenderPreservationReport`
  - `TemporalCraftHints`
- Define how CMF realizes:
  - SFL function stacks
  - composition depth profiles
  - variation profiles
  - video-structure hints
- Explicitly cover:
  - single image outputs
  - carousel outputs
  - reel / short-form video outputs
  - scoring-card / audit-board compatible outputs

**REJECTION:** CMF redefines SFL | no render contract for composition depth | no variation-aware rendering | no PDF/card output awareness | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
