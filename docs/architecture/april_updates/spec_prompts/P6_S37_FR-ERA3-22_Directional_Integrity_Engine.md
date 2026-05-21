# Spec Prompt: FR-ERA3-22 — Directional Integrity Engine

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-22
SPEC_TITLE:      Directional Integrity Engine
PHASE:           6 — SDA Foundation
SOURCE_PRD:      PRD-02, PRD-03, PRD-04, PRD-05, PRD-06, PRD-07, PRD-09
MAPPED_STORIES:  Wave0 SDA Adoption across CCF, CMF, CVE, CBCS, Reactions, Webinar, and Commercial integrity sections
CBAR_MANDATES:   Anti-Centroid Law preservation, Direction-over-polish rule, Representation drift detection, Failure-closed validation, Hard-negative adjacency awareness
BACKEND_REL:     NEW engine — CONSUMES FR-ERA3-20 ontology, CONSUMES FR-ERA3-21 crosswalks, LATER EXTENDED by FR-ERA3-16 / 12 / 18 / 05-CORE / 03 / 04 / 09
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-22_Directional_Integrity_Engine_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This is the core validator that answers: "Did the artifact preserve the intended semantic direction?" It must evaluate:
> - invariant preservation
> - representation geometry drift
> - archetypal coherence
> - species-hypothesis fit
> - hard-negative adjacency
>
> It is not a style checker, not a sentiment checker, and not a generic safety classifier.

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
2. Source PRDs: all modules listed in `SOURCE_PRD`. **PROOF:** Quote the exact Wave 0 integrity additions from at least PRD-03, PRD-05, PRD-06, and PRD-09.
3. SDA source set: all 4 mandatory docs above. **PROOF:** Quote one concrete validator-relevant claim from each.
4. Existing backend files: read `content_machine.py`, `canvas_composition_service.py`, `trait_scoring_engine.py`, `conversion_sequence_router.py`, and any other real service this validator would gate. **PROOF:** Quote real method signatures.
5. Primitive YAMLs: read at least 2 meaning + 2 experience YAMLs.
6. Tests: read 2 `tests/integration/` files covering gated or failure-closed services.
7. Confirm the taxonomy distinctions between policy, packet, and adversarial asset.

**PRE-WORK LOG — required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 300 LINES

Use the standard Era 3 10-section format. Section 5 must define complete Pydantic models for integrity request, evidence, decision, and report payloads.

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define the engine input contract and output report
- Define pass / review / fail states
- Include explicit score dimensions for:
  - invariant preservation
  - representation drift
  - hard-negative adjacency
  - trajectory risk
- Define where this engine blocks execution versus emits advisory drift
- Define service integration patterns for CCF, CMF, CBCS, Reactions, Webinar, and Commercial flows
- Include failure-closed fallback behavior via existing circuit-breaker patterns

**REJECTION:** Generic “semantic quality” language | No pass/fail thresholds | No hard-negative hook | No failure-closed behavior | No downstream integration map | invented scoring dimensions with no lineage

**Write the pre-work log. Then write the spec. No permission needed.**
