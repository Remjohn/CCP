# Spec Prompt: FR-ERA3-28 â€” Perceptual Failure Corpus and Contrast Harness

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-28
SPEC_TITLE:      Perceptual Failure Corpus and Contrast Harness
PHASE:           6 â€” SFL Foundation
SOURCE_PRD:      PRD-02, PRD-03, PRD-06, PRD-09
MAPPED_STORIES:  Wave0 SFL adoption â€” negative-space adversarial boundary for false depth, dead polish, synthetic smoothness, over-optimization, and misaligned proof packaging
CBAR_MANDATES:   Anti-Centroid Law preservation, Negative-space boundary hardening, False-depth rejection, Synthetic-authority detection, Adversarial contrast discipline
BACKEND_REL:     NEW adversarial asset harness â€” CONSUMES FR-ERA3-25 taxonomy and FR-ERA3-27 evaluator, STAYS DISTINCT from FR-ERA3-24 hard-negative corpus while interoperating with it
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-28_Perceptual_Failure_Corpus_And_Contrast_Harness_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This spec must define the adversarial negative-space substrate for SFL. It should model contrastive perceptual failures such as:
> - false depth
> - dead polish
> - synthetic smoothness
> - overresolved meaning
> - synthetic authority inflation
> - empty motivationality with premium aesthetics
>
> It is not a generic content moderation system and it is not a duplicate of FR-ERA3-24 semantic hard negatives.

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
2. Source PRDs: all modules listed in `SOURCE_PRD`. **PROOF:** Quote the exact trust / proof / human-first lines most relevant to perceptual negative-space failures.
3. SFL source set: all 6 mandatory docs above. **PROOF:** Quote one concrete negative-space or adversarial-boundary claim from each.
4. Existing backend files: read `FR-ERA3-24`, `FR-ERA3-27` if available, plus any real corpus / evaluator / guardrail service patterns in `src/ccp/services/`. **PROOF:** Quote real method signatures.
5. Primitive YAMLs: read at least 2 meaning + 2 experience YAMLs.
6. Tests: read 2 `tests/integration/` files covering corpus, mutation, contrastive, or evaluator-harness patterns.
7. Confirm the distinction between semantic hard negatives and perceptual failure assets.

**PRE-WORK LOG â€” required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 300 LINES

Use the standard Era 3 10-section format. Section 5 must define complete Pydantic models for contrastive case, mutation suite, failure label bundle, evaluator expectation bundle, and harness report payloads.

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define corpus objects for:
  - `FalseDepthContrastCase`
  - `DeadPolishContrastCase`
  - `SyntheticAuthorityContrastCase`
  - `OverresolvedMeaningCase`
  - `EmptyMotivationalSmoothnessCase`
- Define mutation operations relevant to perceptual deadness, such as:
  - over-smoothing
  - implication stripping
  - symbolic flattening
  - rhythm normalization
  - proof inflation
- Define how the harness interoperates with, but does not merge into, FR-ERA3-24 semantic hard negatives
- Define expected evaluator outcomes and downgrade/block behavior
- Define how contrast cases are versioned, curated, and expanded over time

**REJECTION:** treating perceptual failures as semantic hard negatives with no distinction | no mutation suite | no corpus versioning | generic “bad example” prose instead of structured contrast cases | no evaluator expectations | no failure-closed rules

**Write the pre-work log. Then write the spec. No permission needed.**
