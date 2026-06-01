# Spec Prompt: FR39 Update — Pi Extension Harness for SCRE And SVRE Operations

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR39 (Pi Extension Harness)
SPEC_TITLE:      Update Pi Extension Harness for SCRE And SVRE Operational Extensions
PHASE:           7 — Living Commentary & Coach Communication Stack
SOURCE_PRD:      PRD-02 (CCF), PRD-03 (CMF)
MAPPED_STORIES:  Research packet compiler extension, source convergence extension, visual resolution compiler extension, image/commentary output routing extension
CBAR_MANDATES:   Update-Not-Replace Rule, Extension-Consumes-Not-Owns Rule
BACKEND_REL:     UPDATE existing Pi Extension Harness — MUST use the Complete Editing Session payload. MUST add SCRE and SVRE operational extensions that consume existing CRAL, Aurore, and SVRE code without duplicating their ownership. The VisualResolutionCompilerExtension must operate asynchronously as a Visual Intelligence Engine (VIE) asset feeder, outputting visual assets to the Complete Editing Session for Remotion backend rendering.
OUTPUT_FILE:     docs/architecture/april_updates/FR39_Pi_Extension_Harness_Tech_Spec_UPDATED_FOR_SCRE_SVRE.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This is the third Pi harness update. It folds `FR-ERA3-53` (Pi SCRE And SVRE Operational Extensions) into the existing harness.
>
> These extensions make the Pi pipeline operationally complete for research compilation (SCRE) and visual resolution (SVRE) by wiring existing CRAL, Aurore, and SVRE services as pipeline extensions.
>
> **ASYNCHRONOUS VIE ASSET FEEDING:**
> Rather than a synchronous execution step, visual resolution compiled by SVRE must serve as an asynchronous VIE asset feeder. It populates components, displacement coordinates, and segments inside the Complete Editing Session to feed the Remotion backend asynchronously.

> [!IMPORTANT]
> **MANDATORY LIVING COMMENTARY SOURCE SET (10+ REFERENCE FILES):**
> - `lab/CCP APRIL Updates/05_Core_Experience/Living_Commentary_Realization_Layer_Source_of_Truth.md`
> - `lab/CCP APRIL Updates/01_Architecture_PRDs/Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md`
> - `docs/architecture/HANDOVER_CONSOLIDATION_BLUEPRINTS.md` (Master handover blueprint)
> - `docs/architecture/May 2026 UPDATES/Architectural_Audit_Trigger_First_Vision_Visual_Engines.md` (Pivots audit, Complete Editing Session and VIE mandate)
> - `src/ccp/services/pi_extension_harness.py` (Local Code Reference)
> - `docs/prd/modules/PRD_02_CCF_Content_Factory.md` (PRD Module)
> - `docs/prd/modules/PRD_03_CMF_Media_Factory.md` (PRD Module)
> - `docs/architecture/Sovereign_CRAL_Research_Engine_TechSpec_V1.md`
> - `docs/architecture/Sovereign_Visual_Research_Engine_TechSpec_V1.md`
> - `src/ccp/services/` (Local Service Directory)

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-02`, `PRD-03`. **PROOF:** Quote lines on research and visual resolution pipeline expectations.
3. Master blueprints: `HANDOVER_CONSOLIDATION_BLUEPRINTS.md` and the pivots audit. **PROOF:** Quote references to asynchronous asset feeding and SVRE image scoring.
4. Living Commentary source set: both doctrine docs. **PROOF:** Quote Wave D FR-ERA3-53 purpose from Roadmap §5.
5. **Existing code — CRITICAL:** Read `src/ccp/services/pi_extension_harness.py`. **PROOF:** Quote real method signatures.
6. Existing CRAL/Aurore/SVRE code: scan `src/ccp/services/` for research and visual resolution files. **PROOF:** Quote real method signatures.
6. Existing test patterns: read 1 `tests/integration/` file covering research or visual resolution behavior.

**PRE-WORK LOG — required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 280 LINES

§1 Files Read (>=5) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=3 files) | §3.3 Extension contracts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=3 phases, >=10 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- This must be written as an **update spec**
- Define extension stage schemas for:
  - `ResearchPacketCompilerExtension` — compiles SCRE research packets from source signals
  - `SourceConvergenceExtension` — merges multiple source signals into unified research context
  - `VisualResolutionCompilerExtension` — resolves SVRE visual output from research and archetype context
  - `ImageCommentaryOutputRoutingExtension` — routes final image/commentary outputs to appropriate deployment surfaces
- Each extension must:
  - declare its dependency on upstream CRAL/Aurore/SVRE services
  - define input/output contracts
  - never duplicate the upstream service's ownership
- Must reference existing code patterns from `pi_extension_harness.py` and CRAL/SVRE files

**REJECTION:** Extensions duplicate CRAL/SVRE ownership | no input/output contracts | no dependency declarations | treats as greenfield | no real code references | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
