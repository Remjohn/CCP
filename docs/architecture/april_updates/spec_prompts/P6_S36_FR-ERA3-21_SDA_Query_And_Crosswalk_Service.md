# Spec Prompt: FR-ERA3-21 — SDA Query and Crosswalk Service

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-21
SPEC_TITLE:      SDA Query and Crosswalk Service
PHASE:           6 — SDA Foundation
SOURCE_PRD:      PRD-02, PRD-08
MAPPED_STORIES:  Wave0 SDA Adoption — PRD-02 SDA packet/runtime stack, PRD-08 primitive/SDA sibling-infrastructure doctrine
CBAR_MANDATES:   Anti-Centroid Law preservation, ADR-05 primitive traceability, Primitive/SDA separation, Crosswalk determinism, No speculative registry duplication
BACKEND_REL:     NEW sibling query layer — MUST interoperate with FR-ERA3-06 Primitive Registry Query Service but MUST NOT absorb SDA into the primitive registry boundary
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-21_SDA_Query_And_Crosswalk_Service_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This spec defines the operational query layer for SDA artifacts plus the explicit crosswalk objects that bridge:
> - primitive -> invariant
> - edge product -> content species
> - archetype container -> archetypal geometry
>
> The service must remain a sibling to the primitive registry service. It is not allowed to turn SDA into "more primitives."

> [!IMPORTANT]
> **MANDATORY SDA SOURCE SET — READ IN EVERY SDA SPEC SESSION:**
> - `lab/semantic_discernment_architecture_content_engine_v_1.md`
> - `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md`
> - `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md`
> - `lab/CCP APRIL Updates/05_Core_Experience/Matrix of Edging.md`

> [!WARNING]
> **TRACEABILITY NOTE:**
> There is no dedicated Phase 6 epic file yet. Use the Wave 0 PRD additions and the SDA source set as the story source. In Section 3.4, write `SDA Governance Constraints` if no formal `PhaseX-M#` table applies.

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-02`, `PRD-08` — quote the exact SDA packet/crosswalk language added in Wave 0.
3. SDA source set: all 4 mandatory docs above. **PROOF:** Quote one crosswalk-relevant claim from each.
4. Existing registry/query backend: read files used by FR-ERA3-06 and any current registry/query infrastructure. **PROOF:** Quote real method signatures and route patterns.
5. Primitive YAMLs: read at least 2 real YAMLs to preserve ID integrity.
6. Models/routes/tests: read relevant `src/ccp/models/`, `src/ccp/api/`, and 2 `tests/integration/` files for query service patterns.
7. Confirm the difference between canonical ontology, crosswalk object, and runtime packet from the taxonomy file.

**PRE-WORK LOG — required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 300 LINES

Use the standard Era 3 10-section format. Section 3.2 must cite real Python files and exact integration points.

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define query surfaces for:
  - canonical SDA ontology
  - structural grammar objects
  - crosswalk objects
- Define API/request/response models for:
  - primitive-to-invariant resolution
  - archetype-to-geometry resolution
  - edge-to-species resolution
- Define cache, fallback, and version-consistency rules
- Explicitly state which runtime objects are queryable and which must be computed elsewhere
- Preserve FR-ERA3-06 boundary by naming what stays primitive-only
- Include lineage/provenance in responses

**REJECTION:** Merging SDA into primitive registry | No crosswalk provenance | Querying derived/runtime objects as if canonical by default | Generic “search” wording | No fallback rules | EXP-TRB-* | invented endpoints

**Write the pre-work log. Then write the spec. No permission needed.**
