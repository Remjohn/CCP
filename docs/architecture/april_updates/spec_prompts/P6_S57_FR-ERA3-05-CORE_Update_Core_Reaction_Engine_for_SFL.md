# Spec Prompt: FR-ERA3-05-CORE Update - Core Reaction Engine for SFL

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-05-CORE
SPEC_TITLE:      Update Core Reaction Engine for SFL
PHASE:           6 - SFL Runtime Integration
SOURCE_PRD:      PRD-06, PRD-08
MAPPED_STORIES:  SFL Wave 3 reaction propagation - reaction scoring enriched by presence/resonance/signal effects, anti-slop detection in reactions, card-style reaction benchmarking alignment
CBAR_MANDATES:   Reaction-Feels-Human Rule, Presence-Over-Flat-Engagement Rule, No-Dead-Polish Rule, SFL Subordinate-to-SDA Rule, Human-First-Competition Rule
BACKEND_REL:     UPDATE existing CORE reaction runtime - MUST consume SFL/eval outputs and remain aligned with the visible score system without collapsing into pure gamification
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec_UPDATED_FOR_SFL.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This update should enrich the reaction engine so it can reason with:
> - Humanity
> - Presence
> - Trust
> - Memorability
> - Resonance
> - Signal
> - AI Slop Risk
>
> It must not reduce reaction quality to vanity engagement or shallow point-scoring.
>
> Hard rule: reaction benchmarking should help train real human authority, not optimize for generic dopamine formatting.

> [!IMPORTANT]
> **MANDATORY SFL SOURCE SET - READ IN EVERY SFL INTEGRATION SPEC SESSION:**
> - `lab/subliminal_function_layer_for_ccp_v_1.md`
> - `lab/phase0_eval_card_scoring_model_v_1.md`
> - `docs/prd/modules/PRD_06_Conscious_Reactions.md`
> - `docs/prd/modules/PRD_08_Conscious_Primitives.md`
> - `docs/architecture/april_updates/FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-27_Perceptual_Influence_Evaluator_Tech_Spec.md`
> - `docs/architecture/april_updates/FR-ERA3-35A_Eval_Registry_And_Scoring_Taxonomy_Tech_Spec.md`
> - `lab/ccp_biological_orchestration_model_v_1.md`

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-06`, `PRD-08`. **PROOF:** Quote the exact lines that establish reaction scoring purpose and primitive-layer boundaries.
3. SFL source set: all mandatory docs above. **PROOF:** Quote one concrete structural claim from each file.
4. Existing FR specs: read `FR-ERA3-05-CORE`, `FR-ERA3-27`, and `FR-ERA3-35A`. **PROOF:** Quote the scoring/evaluator responsibilities from each.
5. Existing backend references: read real files for reaction scoring, benchmarking, or routing logic. **PROOF:** Quote real method signatures.
6. Existing models: read reaction score, benchmark, and result models.
7. Existing test patterns: read 2 `tests/integration/` files covering reaction scoring or evaluation behavior.
8. Existing visible-score doctrine: confirm how reaction benchmarking should align with the card score language without flattening deeper internal metrics.

**PRE-WORK LOG - required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 320 LINES

§1 Files Read (>=9) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=4 files) | §3.3 Reaction score / benchmark contracts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=4 phases, >=14 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- This must be written as an **update spec**
- Define canonical schemas for:
  - `ReactionPerceptualScore`
  - `ReactionVisibleScoreSummary`
  - `ReactionPresenceSignal`
  - `ReactionSlopRiskState`
  - `ReactionBenchmarkCarryover`
- Define how the reaction engine uses:
  - visible score families
  - perceptual evaluator outputs
  - anti-slop detection
  - presence/resonance/signal weighting
- Explicitly define how reaction scoring differs from:
  - generic engagement scoring
  - pure content-marketing metrics
  - shallow gamification loops

**REJECTION:** reaction engine becomes engagement bait optimizer | no presence/humanity scoring role | no anti-slop logic | no visible/internal score distinction | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
