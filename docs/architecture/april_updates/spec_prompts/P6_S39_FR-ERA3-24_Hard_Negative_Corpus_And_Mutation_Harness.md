# Spec Prompt: FR-ERA3-24 — Hard Negative Corpus and Mutation Harness

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-24
SPEC_TITLE:      Hard Negative Corpus and Mutation Harness
PHASE:           6 — SDA Foundation
SOURCE_PRD:      PRD-02, PRD-03, PRD-06, PRD-07, PRD-09
MAPPED_STORIES:  Wave0 SDA Adoption — CCF integrity, CMF representation preservation, Reaction governance, Webinar integrity, Commercial trust transfer integrity
CBAR_MANDATES:   Deceptive-adjacency detection, Failure-closed validation, Benchmark realism, No black-and-white “bad label” simplification
BACKEND_REL:     NEW adversarial eval asset layer — CONSUMED by FR-ERA3-22, later referenced by FR-ERA3-16 / 12 / 05-CORE / 03 / 04 / 09
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-24_Hard_Negative_Corpus_And_Mutation_Harness_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This spec must define hard negatives as contrastive evaluation artifacts, not as glossary-style “bad output” descriptions. It must support:
> - positive anchor
> - deceptive near-neighbor
> - divergence axes
> - expected validator outcomes
> - mutation suite
>
> The mutation harness must stress the validator across compression, CTA translation, surface shift, intensity shift, and other semantically dangerous transformations.

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
2. Source PRDs: `PRD-02`, `PRD-03`, `PRD-06`, `PRD-07`, `PRD-09`. **PROOF:** Quote the exact Wave 0 SDA additions.
3. SDA source set: all 4 mandatory docs above. **PROOF:** Quote one hard-negative / recursive-adversarial claim from each relevant SDA doc.
4. Existing backend files: read validator, pipeline, or scoring services that would consume adversarial eval outputs. **PROOF:** Quote real method signatures.
5. Primitive YAMLs: read at least 2 meaning + 2 experience YAMLs to maintain ADR-05 style grounding.
6. Tests: read 2 existing integration tests with benchmark/assertion patterns.
7. Confirm from the taxonomy file that `HardNegative` is an adversarial evaluation asset, not a canonical ontology row.

**PRE-WORK LOG — required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 300 LINES

Use the standard Era 3 10-section format.

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define:
  - hard-negative corpus object model
  - mutation stress suite model
  - expected validator-outcome model
- Include corpus ingestion, indexing, provenance, and versioning rules
- Include runtime evaluation hooks for FR-ERA3-22
- Explicitly model deceptive adjacency rather than binary “good/bad” labels
- Define how benchmark cases are expanded over time without corrupting the canonical ontology

**REJECTION:** Treating hard negatives as moral labels | No mutation suite | No divergence-axis modeling | No validator-expected outcomes | No provenance/versioning | No runtime consumer mapping

**Write the pre-work log. Then write the spec. No permission needed.**
