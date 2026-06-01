# Spec Prompt: FR-ERA3-35B Update — Content Benchmark Profiles for Presence-Weighted Living Commentary

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-35B
SPEC_TITLE:      Update Content Benchmark Profiles for Presence-Weighted Living Commentary
PHASE:           7 — Living Commentary & Coach Communication Stack
SOURCE_PRD:      PRD-02, PRD-03
MAPPED_STORIES:  Presence weighting integration, delivery quality scoring dimensions, Living Commentary format-specific benchmark cards, SSS integration bridge
CBAR_MANDATES:   Benchmark-Preserves-Delivery Rule, Format-Specific-Card Rule, Anti-Slop Benchmark Rule
BACKEND_REL:     UPDATE existing content benchmark profiles — MUST add presence weighting, delivery quality scoring dimensions, and Living Commentary format-specific benchmark cards
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-35B_Content_Benchmark_Profiles_Tech_Spec_UPDATED_FOR_LIVING_COMMENTARY.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This update extends the existing eval/scoring benchmark profile system to account for the fact that Living Commentary surfaces are performance-led. Static carousel benchmarks do not apply. The benchmark system must now score:
> - **delivery presence** (how much the coach's visible judgment carries the piece)
> - **delivery quality dimensions** (pause, transition, modulation, humor landing, etc.)
> - **format-specific criteria** per Living Commentary family
>
> Hard rule: this is a benchmark profile update, not a new scoring engine.

> [!IMPORTANT]
> **MANDATORY LIVING COMMENTARY SOURCE SET (7+ REFERENCE FILES):**
> - `lab/CCP APRIL Updates/05_Core_Experience/Living_Commentary_Realization_Layer_Source_of_Truth.md`
> - `lab/CCP APRIL Updates/01_Architecture_PRDs/Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md`
> - `docs/architecture/HANDOVER_CONSOLIDATION_BLUEPRINTS.md` (Master handover blueprint)
> - `docs/architecture/May 2026 UPDATES/Architectural_Audit_Trigger_First_Vision_Visual_Engines.md` (Pivots audit, Remotion mandate)
> - `docs/architecture/april_updates/FR-ERA3-35B_Content_Benchmark_Profiles_And_Card_Weighting_Bundles_Tech_Spec.md`
> - `docs/prd/modules/PRD_02_CCF_Content_Factory.md` (PRD Module)
> - `docs/prd/modules/PRD_03_CMF_Media_Factory.md` (PRD Module)

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-02`, `PRD-03`. **PROOF:** Quote lines establishing content quality and scoring expectations.
3. Master blueprints: `HANDOVER_CONSOLIDATION_BLUEPRINTS.md` and the pivots audit. **PROOF:** Quote references to presence-based coaching validation and video asset preservation.
4. Living Commentary source set: both doctrine docs. **PROOF:** Quote the delivery telemetry dimensions from the Roadmap (§4.4) and the SWOT weaknesses about delivery quality dependence.
5. Existing FR-ERA3-35B spec: read fully. **PROOF:** Quote the existing benchmark card schema and weighting model.
6. Existing backend: read scoring/eval card code files. **PROOF:** Quote real method signatures.
6. Existing test patterns: read 1 `tests/integration/` file covering eval or benchmark behavior.

**PRE-WORK LOG — required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 280 LINES

§1 Files Read (>=6) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=3 files) | §3.3 Benchmark profile contracts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=3 phases, >=10 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- This must be written as an **update spec**
- Define canonical schemas for:
  - `PresenceWeightProfile` — how much the coach's delivery presence is weighted in overall content quality scoring
  - `DeliveryQualityDimensions` — scored dimensions: pause quality, transition strength, emotional modulation, story retention, humor landing, objection clarity, close integrity, replay usefulness
  - `LivingCommentaryBenchmarkCard` — format-specific benchmark card with criteria per Living Commentary family (Quote, Comparison, Screenshot, Atmospheric, Cinematic Story, Animated Explainer)
- Define how presence weighting interacts with the Seminar Speaking Score (SSS) concept
- Define anti-slop benchmark criteria: reject "talking head with captions" degradation

**REJECTION:** No presence weighting | no delivery quality dimensions | no format-specific benchmark cards | no anti-slop criteria | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
