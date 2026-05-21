# Spec Prompt: FR-ERA3-26 â€” Subliminal Function Query and Profile Service

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-26
SPEC_TITLE:      Subliminal Function Query and Profile Service
PHASE:           6 â€” SFL Foundation
SOURCE_PRD:      PRD-02, PRD-08
MAPPED_STORIES:  Wave0 SFL adoption â€” runtime lookup, function-stack assembly, primitive/SDA/SFL boundary preservation
CBAR_MANDATES:   Anti-Centroid Law preservation, Deterministic profile assembly, No-Function-Hallucination Rule, Primitive/SDA/SFL boundary rule, Failure-closed profile resolution
BACKEND_REL:     NEW service â€” CONSUMES FR-ERA3-25 function taxonomy, INTEROPS with FR-ERA3-06 primitive registry and FR-ERA3-20 SDA ontology via maintained crosswalks
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-26_Subliminal_Function_Query_And_Profile_Service_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This service must resolve:
> - function families
> - function definitions
> - archetype-aligned function profiles
> - representation-geometry-aligned function profiles
> - surface constraint profiles
> - runtime `SubliminalFunctionStackPacket` assembly
>
> It is not a content generator. It is not an evaluator. It is a deterministic lookup and profile-assembly service.

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
> There is no dedicated Phase 6 epic file yet. Use the SFL source set and `MAPPED_STORIES` as the story source. In Section 3.4, write `SFL Governance Constraints` if no formal `PhaseX-M#` table applies.

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-02`, `PRD-08`. **PROOF:** Quote the exact runtime-law and primitive-boundary lines relevant to this service.
3. SFL source set: all 6 mandatory docs above. **PROOF:** Quote one concrete profile-assembly or function-stack relevant claim from each.
4. Existing backend files: read `FR-ERA3-06`, `FR-ERA3-20`, and real registry/query service files in `src/ccp/services/` and `src/ccp/models/`. **PROOF:** Quote real method signatures.
5. Primitive YAMLs: read at least 2 meaning + 2 experience YAMLs.
6. Tests: read 2 `tests/integration/` files covering query services or deterministic resolution patterns.
7. Confirm crosswalk expectations between primitives, geometries, surfaces, and function families.

**PRE-WORK LOG â€” required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 300 LINES

Use the standard Era 3 10-section format. Section 5 must define complete Pydantic models for query request, query response, function profile, and runtime packet assembly payloads.

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define query surfaces for:
  - by family
  - by function id
  - by primitive crosswalk
  - by representation geometry crosswalk
  - by archetype / container profile
  - by delivery surface constraint profile
- Define deterministic `SubliminalFunctionStackPacket` assembly
- Define fallback behavior when:
  - crosswalk evidence is partial
  - profile conflict exists
  - only family-level match exists
- Preserve clean boundaries:
  - no evaluator logic
  - no ontology ownership
  - no primitive ownership duplication
- Include cache, versioning, and targeted reload expectations if the substrate is maintained locally

**REJECTION:** Query service that invents functions at runtime | evaluator logic mixed into lookup | no deterministic profile assembly | no failure-closed fallback | duplication of FR-ERA3-06 or FR-ERA3-20 responsibilities | missing crosswalk design

**Write the pre-work log. Then write the spec. No permission needed.**
