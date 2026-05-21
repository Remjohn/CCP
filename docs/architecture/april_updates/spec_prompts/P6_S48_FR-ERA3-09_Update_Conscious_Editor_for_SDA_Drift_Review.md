# Spec Prompt: FR-ERA3-09 — UPDATE: Conscious Editor for SDA Drift Review

> **READY TO PASTE — SPEC UPDATE.** Copy into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:          FR-ERA3-09
SPEC_TITLE:       UPDATE: Conscious Editor for SDA Drift Review
PHASE:            6 — Existing Spec Updates
SOURCE_PRD:       PRD-03, PRD-02
EXISTING_FILE:    docs/architecture/april_updates/FR-ERA3-09_Conscious_Editor_Tech_Spec.md
OUTPUT_FILE:      docs/architecture/april_updates/FR-ERA3-09_Conscious_Editor_Tech_Spec_UPDATED.md
```

## CHANGES REQUIRED

Update the Conscious Editor spec so review mode can explicitly surface SDA drift, not only transcript/media mismatches. The revised spec must add reviewer-visible projections for:

- invariant loss or mutation
- representation-geometry drift
- archetypal incoherence
- hard-negative adjacency risk
- directional-integrity flags

The editor must remain an artifact-first review surface. Do not turn it into a separate scoring engine. It should consume SDA reports and expose drift clearly enough for human correction and rerender decisions.

> [!IMPORTANT]
> **MANDATORY SDA SOURCE SET — READ IN EVERY SDA SPEC SESSION:**
> - `lab/semantic_discernment_architecture_content_engine_v_1.md`
> - `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md`
> - `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md`
> - `lab/CCP APRIL Updates/05_Core_Experience/Matrix of Edging.md`

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. This is an UPDATE to an EXISTING spec, not a new spec. Your output is a revised version of the existing file with targeted changes applied.

---

## MANDATORY PRE-WORK

1. Read the EXISTING SPEC FILE listed in `EXISTING_FILE`.
2. Read the Master Protocol.
3. Read `PRD-03` and `PRD-02`, including their Wave 0 SDA additions.
4. Read the full mandatory SDA source set listed above.
5. **PROOF:** Quote the exact section in the existing spec where review currently stops short of semantic-direction drift analysis.

---

## UPDATE FORMAT

Output the COMPLETE revised spec file. Do NOT output just the changed sections — output the whole file.
Mark all changed sections with `<!-- UPDATED: [reason] -->` HTML comments so changes are traceable.
Do NOT change anything outside the `CHANGES_REQUIRED` scope listed above.

## REJECTION

Turning the editor into a new validator engine | No reviewer-facing drift surfaces | No explicit consumption of SDA reports | Changing unrelated rerender taxonomy logic

**Write the revised spec. No permission needed.**
