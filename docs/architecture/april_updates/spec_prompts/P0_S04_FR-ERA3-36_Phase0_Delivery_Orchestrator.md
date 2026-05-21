# Spec Prompt: FR-ERA3-36 - Phase-0 Delivery Orchestrator

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-36
SPEC_TITLE:      Phase-0 Delivery Orchestrator
PHASE:           0 - Trial Phase-0 Commercial Runtime
SOURCE_PRD:      PRD-02, PRD-03, PRD-09
MAPPED_STORIES:  24h max proof-package delivery, shared runtime production flow, sequential asset release, proof-to-payment handoff
CBAR_MANDATES:   24h Delivery Readiness Rule, Sequential-Wow Delivery Rule, Shared-Workspace-First Rule, No-Full-Container-Before-Payment Rule, Proof-Before-Explanation Rule
BACKEND_REL:     NEW orchestration runtime - MUST consume existing content/media/render infrastructure where possible instead of re-inventing production pipelines
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-36_Phase0_Delivery_Orchestrator_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This spec defines the runtime that turns a validated Phase-0 prospect packet into a deliverable package within `24h max`.
>
> Minimum package orchestration scope:
> - audit
> - PDF audit package
> - audit explainer video
> - preview assets
> - produced explainers
> - cinematic proof artifact
> - optional meme / carousel support
> - delivery sequencing
> - payment-link attachment
>
> The orchestrator must assume the upstream audit/runtime can start from different content source types:
> - single image post + caption
> - multiple images / carousel post + caption
> - reel / short-form video + caption

> [!IMPORTANT]
> **MANDATORY PHASE-0 SOURCE SET - READ IN EVERY PHASE-0 SPEC SESSION:**
> - `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`
> - `docs/prd/modules/PRD_02_CCF_Content_Factory.md`
> - `docs/prd/modules/PRD_03_CMF_Media_Factory.md`
> - `lab/CCP APRIL Updates/Fladlien_Sales_Insights.md`
> - `lab/ccp_biological_orchestration_model_v_1.md`
> - `lab/CCP APRIL Updates/01_Architecture_PRDs/CCP_System_Documentation.md`

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-09`, `PRD-02`, `PRD-03`. **PROOF:** Quote the exact lines that establish proof-package sequencing, content compiler role, and media/render responsibilities.
3. Phase-0 source set: all mandatory docs above. **PROOF:** Quote one concrete structural claim from each file.
4. Existing backend references: read real files related to content generation, rendering, artifact export, orchestration, and receipts. **PROOF:** Quote real method signatures.
5. Existing models: read manifest/export/artifact/result model files.
6. Existing test patterns: read 2 `tests/integration/` files covering pipeline orchestration or export patterns.
7. Existing delivery sequencing doctrine: confirm the intended order for Phase-0 asset release and how the orchestrator should preserve it.

**PRE-WORK LOG - required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 320 LINES

§1 Files Read (>=9) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=4 files) | §3.3 Packets / runtime results | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=4 phases, >=14 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define canonical schemas for:
  - `Phase0DeliveryPlan`
  - `Phase0DeliveryRun`
  - `Phase0OutputBundle`
  - `Phase0SequenceStep`
  - `Phase0RenderRequest`
  - `Phase0DeliveryReceipt`
- The orchestrator must explicitly support downstream production of:
  - PDF audits from canonical audit payloads
  - audit explainer videos built from scoring cards
  - reviewable preview bundles before payment handoff
- Define the sequential delivery model explicitly
- Define what is generated automatically vs what can require operator review
- Preserve shared-runtime economics and low setup overhead
- Define fail-closed / partial-delivery behavior if one asset family cannot be produced
- Preserve handoff to payment / upgrade runtime at the end of the sequence

**REJECTION:** vague pipeline | no delivery sequence | assumes bespoke per-client production each time | no 24h SLA handling | no partial-failure law | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
