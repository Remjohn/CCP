# Spec Prompt: FR-ERA3-05-CORE — UPDATE: Core Reaction Engine for SDA

> **READY TO PASTE — SPEC UPDATE.** Copy into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:          FR-ERA3-05-CORE
SPEC_TITLE:       UPDATE: Core Reaction Engine for SDA
PHASE:            6 — Existing Spec Updates
SOURCE_PRD:       PRD-06
EXISTING_FILE:    docs/architecture/april_updates/FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec.md
OUTPUT_FILE:      docs/architecture/april_updates/FR-ERA3-05-CORE_Core_Reaction_Engine_Tech_Spec_UPDATED.md
```

## CHANGES REQUIRED

Update the core reaction engine spec so topic selection, scoring, mode routing, and post-score branching become SDA-aware. The revised spec must add:

- invariant-field awareness for topic/charge selection
- representation-geometry awareness for authority, status, and redemption framing
- directional-integrity and hard-negative touchpoints before publication or escalation
- loop-awareness so repeated reaction play does not drift into synthetic conflict or status addiction

Do not rewrite the whole reaction engine. This is a targeted semantic-governance update.

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
3. Read `PRD-06`, including the Wave 0 SDA additions.
4. Read the full mandatory SDA source set listed above.
5. **PROOF:** Quote the section in the existing spec that currently optimizes for charge/score without explicit SDA direction control.

---

## UPDATE FORMAT

Output the COMPLETE revised spec file. Do NOT output just the changed sections — output the whole file.
Mark all changed sections with `<!-- UPDATED: [reason] -->` HTML comments so changes are traceable.
Do NOT change anything outside the `CHANGES_REQUIRED` scope listed above.

## REJECTION

Rewriting all reaction modes from scratch | No invariant-field touchpoints | No status/belonging framing rules | No hard-negative / integrity gate references

**Write the revised spec. No permission needed.**
