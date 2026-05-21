# Spec Prompt: FR-ERA3-25 â€” Subliminal Function Library and Taxonomy

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-25
SPEC_TITLE:      Subliminal Function Library and Taxonomy
PHASE:           6 â€” SFL Foundation
SOURCE_PRD:      PRD-02, PRD-08
MAPPED_STORIES:  Wave0 SFL adoption â€” SFL doctrine note, PRD-02 runtime extension, PRD-08 primitive/SFL boundary preservation
CBAR_MANDATES:   Anti-Centroid Law preservation, ADR-05 primitive traceability, Role-before-Schema Rule, No-Flat-120 Rule, Function-vs-Metric Separation Rule, SFL Subordinate-to-SDA Rule
BACKEND_REL:     NEW sibling function substrate â€” MUST remain separate from FR-ERA3-06 Primitive Registry and FR-ERA3-20 SDA Ontology, but interoperable with both via maintained crosswalks
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-25_Subliminal_Function_Library_And_Taxonomy_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This is the canonical source-of-truth spec for the Subliminal Function Layer (`SFL`) substrate. It must define:
> - canonical function families
> - function definitions
> - what becomes a metric
> - what becomes a policy
> - what becomes an adversarial perceptual failure asset
> - what is explicitly NOT a canonical registry object
>
> Hard rule: do **not** turn the 120 associations into 120 flat canonical rows.

> [!IMPORTANT]
> **MANDATORY SFL SOURCE SET â€” READ IN EVERY SFL SPEC SESSION:**
> - `lab/subliminal_function_layer_for_ccp_v_1.md`
> - `lab/Subliminal Functions for Agentic Content Architecture.md`
> - `lab/120 subliminal associations Chat.md`
> - `lab/semantic_discernment_architecture_content_engine_v_1.md`
> - `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md`
> - `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md`

> [!WARNING]
> **TRACEABILITY NOTE:**
> There is no dedicated Phase 6 epic file yet. For this spec, Step 3 of the normal prompt flow is replaced by the SFL source set above plus the `MAPPED_STORIES` items. In Section 3.4, use `SFL Governance Constraints` if no formal `PhaseX-M#` mandate exists.

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` â€” Â§2 backend, Â§3 Pre-Flight, Â§4 Format
2. Source PRDs: `PRD-02`, `PRD-08` â€” especially the Wave 0 SDA additions already in place. **PROOF:** Quote the exact lines that establish runtime SDA integration and primitive-boundary separation.
3. SFL source set: all 6 mandatory SFL docs above. **PROOF:** Quote one concrete structural claim from each file.
4. Existing registry/backend references: read `FR-ERA3-06`, `FR-ERA3-20`, and any real `src/ccp/services/` / `src/ccp/models/` files relevant to maintained registries or library-style substrates. **PROOF:** Quote real method signatures.
5. Primitive YAMLs: read at least 2 experience YAMLs and 2 meaning YAMLs to preserve ADR-05 traceability expectations. **PROOF:** Quote `id:` + `name:`. **BANNED:** `EXP-TRB-*`.
6. Existing test patterns: read 2 `tests/integration/` files that cover registry, query, or taxonomy service patterns.
7. Existing SDA implementation: confirm how `FR-ERA3-20` distinguished canonical, runtime, policy, and adversarial assets, and preserve that discipline for SFL.

**PRE-WORK LOG â€” required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 300 LINES

Â§1 Files Read (â‰¥8) | Â§2 Overview | Â§3.1 DEP-IDs | Â§3.2 Backend (â‰¥3 files) | Â§3.3 Primitives / SFL artifacts | Â§3.4 Governance Constraints | Â§3.5 Technical Decisions | Â§4 Plan (â‰¥4 phases, â‰¥12 tasks) | Â§5 Schema (Pydantic v2, no Any) | Â§6 Fallback | Â§7 Tasks | Â§8 AC (with FAILURE EXAMPLE) | Â§9 Dependencies | Â§10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define canonical schemas for:
  - `SubliminalFunctionFamily`
  - `SubliminalFunctionDefinition`
  - `FunctionFamilyCompressionRule`
  - `PrimitiveToFunctionFamilyCrosswalk`
  - `RepresentationGeometryToFunctionProfileCrosswalk`
- Explicitly define which SFL artifacts are:
  - canonical families
  - callable function definitions
  - runtime packets
  - metrics
  - policies
  - adversarial assets
- Compress the 120 associations into stable families rather than preserving them as flat rows
- Preserve the distinction between:
  - `covert suggestion`, `soft control`, `hidden intention` as potentially valid aligned function families
  - `over-optimization`, `false depth` as failure assets / validator targets
- Preserve clean separation from:
  - primitive registry ownership
  - SDA ontology ownership
  - downstream evaluator ownership

**REJECTION:** Flat 120-row design | Treating all terms as registry items | No function-vs-metric separation | No crosswalk discipline | No proof that SFL remains subordinate to SDA | invented method signatures | EXP-TRB-* | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
