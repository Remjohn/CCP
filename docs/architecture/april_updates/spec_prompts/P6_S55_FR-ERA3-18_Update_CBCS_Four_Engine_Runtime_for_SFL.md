# Spec Prompt: FR-ERA3-18 Update - CBCS Four Engine Runtime for SFL

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-18
SPEC_TITLE:      Update CBCS Four Engine Runtime for SFL
PHASE:           6 - SFL Runtime Integration
SOURCE_PRD:      PRD-05, PRD-08
MAPPED_STORIES:  SFL Wave 2 CBCS propagation - perceptual effect awareness in speaking/accountability loops, recommendation quality, audit-to-coaching continuity, human-first voice-note refinement
CBAR_MANDATES:   Human-First Coaching Rule, Voice-Feels-Alive Rule, No-Synthetic-Coach-Tone Rule, SFL Subordinate-to-SDA Rule, Recommendation-From-Effects Rule
BACKEND_REL:     UPDATE existing CBCS runtime - MUST consume SFL/eval outputs without recomputing foundational ownership locally
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-18_CBCS_Four_Engine_Runtime_Tech_Spec_UPDATED_FOR_SFL.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This update should make CBCS aware of:
> - perceptual effects
> - visible score families
> - card-based audit outputs
> - speaking / accountability prescriptions that arise from perceptual weaknesses
>
> The goal is not to turn CBCS into a rendering engine.
> The goal is to let CBCS consume and act on the SFL/audit stack intelligently.

> [!IMPORTANT]
> **MANDATORY SFL SOURCE SET - READ IN EVERY SFL INTEGRATION SPEC SESSION:**
> - `lab/subliminal_function_layer_for_ccp_v_1.md`
> - `lab/phase0_eval_card_scoring_model_v_1.md`
> - `docs/prd/modules/PRD_05_CBCS_Law28.md`
> - `docs/prd/modules/PRD_08_Conscious_Primitives.md`
> - `docs/architecture/april_updates/FR-ERA3-18_CBCS_Four_Engine_Runtime_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-27_Perceptual_Influence_Evaluator_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-35_Audit_Intelligence_Engine_Tech_Spec.md`
> - `lab/ccp_biological_orchestration_model_v_1.md`

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-05`, `PRD-08`. **PROOF:** Quote the exact lines that establish CBCS runtime purpose, voice-note quality, and primitive boundaries.
3. SFL source set: all mandatory docs above. **PROOF:** Quote one concrete structural claim from each file.
4. Existing FR specs: read `FR-ERA3-18`, `FR-ERA3-27`, and `FR-ERA3-35`. **PROOF:** Quote the relevant evaluator/report consumption responsibilities.
5. Existing backend references: read real files for CBCS coaching, scoring, recommendation, or note generation logic. **PROOF:** Quote real method signatures.
6. Existing models: read report / score / coaching-result / recommendation models.
7. Existing test patterns: read 2 `tests/integration/` files covering CBCS/runtime evaluation behavior.
8. Existing biological/runtime doctrine: confirm how CBCS should consume delivery/effect outputs rather than try to recompute truth ownership.

**PRE-WORK LOG - required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 320 LINES

§1 Files Read (>=9) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=4 files) | §3.3 Report / recommendation contracts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=4 phases, >=14 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- This must be written as an **update spec**
- Define canonical schemas for:
  - `PerceptualEffectSummary`
  - `CbcsPerceptualRecommendation`
  - `VisibleScoreCarryover`
  - `VoiceNotePerceptualGuidance`
  - `AccountabilityPerceptualPrescription`
- Define how CBCS consumes:
  - visible score families
  - audit prescriptions
  - perceptual weakness / strength signals
  - SFL-aware evaluator outputs
- Explicitly define how this affects:
  - speaking guidance
  - accountability loops
  - live reaction recommendations
  - trust/humanity/presence improvement pathways

**REJECTION:** CBCS re-runs the whole eval stack locally | no recommendation contracts | no card/audit awareness | no human-first voice-note implication | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
