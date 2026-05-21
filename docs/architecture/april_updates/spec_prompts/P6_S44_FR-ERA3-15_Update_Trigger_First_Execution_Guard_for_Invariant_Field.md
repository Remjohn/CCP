# Spec Prompt: FR-ERA3-15 — UPDATE: Trigger-First Execution Guard for Invariant Field

> **READY TO PASTE — SPEC UPDATE.** Copy into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:          FR-ERA3-15
SPEC_TITLE:       UPDATE: Trigger-First Execution Guard for Invariant Field
PHASE:            6 — Existing Spec Updates
SOURCE_PRD:       PRD-02
EXISTING_FILE:    docs/architecture/april_updates/FR-ERA3-15_Trigger_First_Execution_Guard_Tech_Spec.md
OUTPUT_FILE:      docs/architecture/april_updates/FR-ERA3-15_Trigger_First_Execution_Guard_Tech_Spec_UPDATED.md
```

## CHANGES REQUIRED

Update the trigger-first guard so broad-primary-signal extraction is explicitly SDA-aware. The revised spec must:

- connect trigger blocking and reroute logic to `Existential Invariant` pressure
- distinguish broad-signal extraction from final edge-product formation
- define how the guard passes forward invariant-field evidence rather than only capture-required status
- preserve the existing “block becomes trigger” behavior while making it semantically smarter

Do not re-specify the whole trigger-first mechanism. This is a semantic-upgrade pass.

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
3. Read `PRD-02`, especially the updated runtime law.
4. Read the full mandatory SDA source set listed above.
5. **PROOF:** Quote the exact section in the existing spec where broad signal / trigger logic should now become invariant-aware.

---

## UPDATE FORMAT

Output the COMPLETE revised spec file. Do NOT output just the changed sections — output the whole file.
Mark all changed sections with `<!-- UPDATED: [reason] -->` HTML comments so changes are traceable.
Do NOT change anything outside the `CHANGES_REQUIRED` scope listed above.

## REJECTION

Replacing trigger-first with generic SDA theory | No broad-signal/invariant link | No handoff payload update | Breaking the existing blocked-capture-required flow

**Write the revised spec. No permission needed.**
