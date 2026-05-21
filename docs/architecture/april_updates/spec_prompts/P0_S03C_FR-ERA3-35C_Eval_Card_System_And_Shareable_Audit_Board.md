# Spec Prompt: FR-ERA3-35C - Eval Card System and Shareable Audit Board

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-35C
SPEC_TITLE:      Eval Card System and Shareable Audit Board
PHASE:           0 - Trial Phase-0 Commercial Runtime
SOURCE_PRD:      PRD-01, PRD-04, PRD-09
MAPPED_STORIES:  FIFA-style score cards, shareable audit surfaces, entertaining but serious eval presentation, internal and prospect-facing score visualization
CBAR_MANDATES:   Easy-To-Understand Surface Rule, No-Jargon-On-Card Rule, Canonical-Evals-Underneath Rule, Shareable-Audit Rule, Marketing-Object-Without-Lying Rule
BACKEND_REL:     NEW presentation substrate - MUST consume canonical evals and benchmark bundles instead of inventing new scores at render time
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-35C_Eval_Card_System_And_Shareable_Audit_Board_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This spec defines the visible card system for audits.
>
> It should feel closer to:
> - premium scouting cards
> - FIFA Ultimate Team familiarity
> - easy comparison
> - screenshot-ready boards
>
> Not:
> - enterprise dashboard clutter
> - jargon-heavy eval panels
> - decorative pseudo-game fluff

> [!IMPORTANT]
> **MANDATORY EVAL SOURCE SET - READ IN EVERY EVAL SPEC SESSION:**
> - `lab/phase0_eval_card_scoring_model_v_1.md`
> - `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md`
> - `docs/prd/modules/PRD_04_CVE_Experience_Design.md`
> - `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`
> - `lab/CCP APRIL Updates/Fladlien_Sales_Insights.md`
> - `lab/subliminal_function_layer_for_ccp_v_1.md`

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-01`, `PRD-04`, `PRD-09`. **PROOF:** Quote the exact lines that establish human-first surfaces, experience design expectations, and proof-package commercial logic.
3. Eval source set: all mandatory docs above. **PROOF:** Quote one concrete structural claim from each file.
4. Existing backend references: read real files related to media presentation, audit/report output, or board/card rendering if present. **PROOF:** Quote real method signatures.
5. Existing models: read report/output/result model files that a card layer would consume.
6. Existing test patterns: read 2 `tests/integration/` files covering rendered outputs, API surfaces, or board/state patterns.
7. Presentation law: confirm how the card surface remains easy to understand while still grounded in canonical evals beneath it.

**PRE-WORK LOG - required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 320 LINES

§1 Files Read (>=9) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=3 files) | §3.3 Card / board artifact classes | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=4 phases, >=14 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define canonical schemas for:
  - `EvalCard`
  - `EvalCardFace`
  - `EvalCardStatLine`
  - `EvalCardBoard`
  - `EvalBoardLayout`
  - `CardThumbnailAsset`
  - `CardVerdictBlock`
- The visible stat vocabulary must remain:
  - Humanity
  - Presence
  - Trust
  - Memorability
  - Resonance
  - Signal
  - AI Slop Risk
- The card must expose:
  - big thumbnail
  - overall score `0-99`
  - visible score stats `0-99`
  - card type / role
  - one-line verdict
  - one-line fix or direction
- The board system must support:
  - single-card detail
  - audit board spread
  - before/after comparison board
  - shareable screenshot-ready layout

**REJECTION:** jargon-heavy score surface | new scores invented at render time | no clear thumbnail-first design | no board layouts | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
