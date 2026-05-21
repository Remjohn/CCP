# Spec Prompt: FR-ERA3-35B - Content Benchmark Profiles and Card Weighting Bundles

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-35B
SPEC_TITLE:      Content Benchmark Profiles and Card Weighting Bundles
PHASE:           0 - Trial Phase-0 Commercial Runtime
SOURCE_PRD:      PRD-02, PRD-03, PRD-09
MAPPED_STORIES:  content-type-specific scoring, archetype-specific weighting, modality-aware benchmarks, consistent audit comparisons across images/carousels/reels
CBAR_MANDATES:   No-One-Score-Fits-All Rule, Archetype-Aware Scoring Rule, Multimodal-Benchmark Rule, Content-Type Weighting Rule, Internal Consistency Rule
BACKEND_REL:     NEW benchmark-profile substrate - MUST sit between eval registry and card/audit rendering rather than duplicating either
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-35B_Content_Benchmark_Profiles_And_Card_Weighting_Bundles_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This spec defines how canonical evals are weighted differently by:
> - content type
> - structural archetype
> - card role
>
> Minimum content types:
> - single image post + caption
> - multiple images / carousel + caption
> - reel / short-form video + caption
>
> Minimum weighting outputs:
> - content benchmark profiles
> - archetype-specific score bundles
> - card-type weighting bundles

> [!IMPORTANT]
> **MANDATORY EVAL SOURCE SET - READ IN EVERY EVAL SPEC SESSION:**
> - `lab/phase0_eval_card_scoring_model_v_1.md`
> - `docs/prd/modules/PRD_02_CCF_Content_Factory.md`
> - `docs/prd/modules/PRD_03_CMF_Media_Factory.md`
> - `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`
> - `lab/OmniShotCut Holistic Relational Shot Boundary.md`
> - `lab/subliminal_function_layer_for_ccp_v_1.md`

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-02`, `PRD-03`, `PRD-09`. **PROOF:** Quote the exact lines that establish content compiler logic, media/render logic, and proof-package commercial logic.
3. Eval source set: all mandatory docs above. **PROOF:** Quote one concrete structural claim from each file.
4. Existing backend references: read real files related to content archetypes, rendering, evaluation, or benchmark patterns. **PROOF:** Quote real method signatures.
5. Existing models: read model files relevant to archetypes, packets, manifests, or evaluation outputs.
6. Existing test patterns: read 2 `tests/integration/` files covering pipeline scoring, media, or evaluation behavior.
7. Video-structure precedent: confirm how OmniShotCut should inform benchmark dimensions for reels without taking over the whole scoring system.

**PRE-WORK LOG - required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 320 LINES

§1 Files Read (>=9) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=3 files) | §3.3 Benchmark artifact classes | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=4 phases, >=14 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define canonical schemas for:
  - `ContentBenchmarkProfile`
  - `ArchetypeScoreBundle`
  - `CardWeightingBundle`
  - `VisibleScoreWeightMap`
  - `PenaltyAdjustmentMap`
  - `ModalitySupportProfile`
- Explicitly support:
  - single image post + caption
  - carousel + caption
  - reel + caption
- Define how card types can emphasize the same visible scores differently without changing the canonical score vocabulary
- Define overall-score weighting and cap logic
- Define how video-mode bundles can incorporate:
  - script semantics
  - key frames
  - shot transitions
  - temporal coherence

**REJECTION:** same weighting for all formats | no archetype differentiation | no reel structure dimensions | no overall-score law | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
