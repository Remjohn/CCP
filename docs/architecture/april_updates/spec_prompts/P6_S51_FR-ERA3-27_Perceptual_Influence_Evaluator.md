# Spec Prompt: FR-ERA3-27 â€” Perceptual Influence Evaluator

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-27
SPEC_TITLE:      Perceptual Influence Evaluator
PHASE:           6 â€” SFL Foundation
SOURCE_PRD:      PRD-02, PRD-03, PRD-05, PRD-06, PRD-09
MAPPED_STORIES:  Wave0 SFL adoption â€” perceptual effect scoring, influence alignment, proof-without-false-depth, human congruence, memorability and signal-density evaluation
CBAR_MANDATES:   Anti-Centroid Law preservation, Direction-before-polish rule, Human-congruence priority, False-depth rejection, Failure-closed evaluator discipline
BACKEND_REL:     NEW evaluator â€” CONSUMES FR-ERA3-25 function taxonomy, CONSUMES FR-ERA3-26 profile service, INTEROPS with FR-ERA3-22 Directional Integrity Engine without swallowing it
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-27_Perceptual_Influence_Evaluator_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This evaluator answers:
> - how perceptually alive is this artifact?
> - how much memorability / symbolic density / human congruence is present?
> - how aligned are the active influence mechanics with the brand and surface?
> - does the artifact slip into false depth, dead polish, or synthetic smoothness?
>
> It is not a semantic ontology validator and must not duplicate FR-ERA3-22.

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
2. Source PRDs: all modules listed in `SOURCE_PRD`. **PROOF:** Quote the exact Wave 0 lines most relevant to human-first proof, reaction quality, and commercial trust transfer.
3. SFL source set: all 6 mandatory docs above. **PROOF:** Quote one concrete evaluator-relevant claim from each.
4. Existing backend files: read `FR-ERA3-22`, `trait_scoring_engine.py`, `semantic_affinity_guard.py`, `content_machine.py`, `conversion_sequence_router.py`, and any other real service this evaluator would gate or inform. **PROOF:** Quote real method signatures.
5. Primitive YAMLs: read at least 2 meaning + 2 experience YAMLs.
6. Tests: read 2 `tests/integration/` files covering evaluator or failure-closed service patterns.
7. Confirm the distinction between semantic validity, perceptual potency, and commercial alignment.

**PRE-WORK LOG â€” required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 300 LINES

Use the standard Era 3 10-section format. Section 5 must define complete Pydantic models for evaluator request, evidence, metric bundle, decision bundle, and evaluator report payloads.

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define score dimensions for:
  - `cognitive_imprint_score`
  - `symbolic_density_score`
  - `human_congruence_score`
  - `contrast_clarity_score`
  - `memorability_pressure`
  - `overexplanation_risk_score`
  - `synthetic_smoothness_score`
- Define pass / review / fail or equivalent decision states
- Define how influence-alignment interacts with:
  - brand posture
  - representation geometry
  - content archetype
  - commercial surface sensitivity
- Define how this evaluator interops with FR-ERA3-22 instead of duplicating it
- Define failure-closed downgrade behavior when perceptual evidence is missing or contradictory

**REJECTION:** Generic “quality” scoring | duplicated semantic-direction logic from FR-ERA3-22 | no metric bundle | no false-depth handling | no human-congruence dimension | no failure examples | no downgrade policy

**Write the pre-work log. Then write the spec. No permission needed.**
