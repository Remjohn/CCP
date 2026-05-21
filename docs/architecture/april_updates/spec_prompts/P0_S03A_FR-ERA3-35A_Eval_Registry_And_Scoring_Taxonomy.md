# Spec Prompt: FR-ERA3-35A - Eval Registry and Scoring Taxonomy

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-35A
SPEC_TITLE:      Eval Registry and Scoring Taxonomy
PHASE:           0 - Trial Phase-0 Commercial Runtime
SOURCE_PRD:      PRD-01, PRD-02, PRD-09
MAPPED_STORIES:  canonical internal eval list, score consistency across audits, visible-card score foundation, pre-delivery internal scoring discipline
CBAR_MANDATES:   Canonical-Eval-First Rule, No-Ad-Hoc-Scoring Rule, Human-Signal-Over-Polish Rule, Internal-Before-External Scoring Rule, Typed-Eval-Registry Rule
BACKEND_REL:     NEW evaluation substrate - MUST become the canonical scoring backbone for audits, internal QA, and future optimization loops
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-35A_Eval_Registry_And_Scoring_Taxonomy_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This spec defines the canonical internal eval registry beneath the card system and the audit engine.
>
> It must support:
> - visible score families:
>   - Humanity
>   - Presence
>   - Trust
>   - Memorability
>   - Resonance
>   - Signal
>   - AI Slop Risk
> - deeper internal metric clusters and hidden support clusters
> - normalized `0-99` scoring
> - use across internal scoring, prospect audits, and later benchmark memory

> [!IMPORTANT]
> **MANDATORY EVAL SOURCE SET - READ IN EVERY EVAL SPEC SESSION:**
> - `lab/phase0_eval_card_scoring_model_v_1.md`
> - `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md`
> - `docs/prd/modules/PRD_02_CCF_Content_Factory.md`
> - `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`
> - `lab/subliminal_function_layer_for_ccp_v_1.md`
> - `lab/ccp_biological_orchestration_model_v_1.md`

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-01`, `PRD-02`, `PRD-09`. **PROOF:** Quote the exact lines that establish anti-slop, compiler truth, and the commercial proof doctrine.
3. Eval source set: all mandatory docs above. **PROOF:** Quote one concrete structural claim from each file.
4. Existing backend references: read real files related to scoring, benchmarking, evaluation models, or report generation. **PROOF:** Quote real method signatures.
5. Existing models: read score/report/evaluation-related model files under `src/ccp/models/`.
6. Existing test patterns: read 2 `tests/integration/` files covering scoring, evaluation, or registry/query patterns.
7. Existing packet/receipt precedent: confirm how the eval registry should participate in later receipt and benchmark memory flows.

**PRE-WORK LOG - required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 320 LINES

§1 Files Read (>=9) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=3 files) | §3.3 Eval artifact classes | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=4 phases, >=14 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define canonical schemas for:
  - `EvalDefinition`
  - `EvalCluster`
  - `VisibleScoreFamily`
  - `HiddenSupportCluster`
  - `EvalMeasurement`
  - `EvalScoreProjection`
  - `EvalPenaltyRule`
- The spec must separate:
  - internal eval metrics
  - visible score families
  - hidden support clusters
  - penalty / cap rules
- The visible score families must remain:
  - Humanity
  - Presence
  - Trust
  - Memorability
  - Resonance
  - Signal
  - AI Slop Risk
- Define how all scores normalize to `0-99`
- Define how this registry supports internal pre-delivery scoring before prospect-facing audits

**REJECTION:** flat vague score list | no visible-vs-hidden distinction | no normalization law | no penalty logic | no internal-first scoring rule | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
