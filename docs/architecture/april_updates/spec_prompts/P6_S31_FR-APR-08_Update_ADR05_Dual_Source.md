# Spec Prompt: FR-APR-08 — UPDATE: Add ADR-05 + Dual-Source Mandate

> **READY TO PASTE — SPEC UPDATE.** Copy into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:          FR-APR-08
SPEC_TITLE:       UPDATE: Add ADR-05 + Dual-Source Mandate
PHASE:            6 — Existing Spec Updates
SOURCE_PRD:       PRD-08
EXISTING_FILE:    docs/architecture/april_updates/previous specs/FR-APR-08_Orchestration_Dichotomy_Tech_Spec.md
OUTPUT_FILE:      docs/architecture/april_updates/FR-APR-08_Orchestration_Dichotomy_Tech_Spec_UPDATED.md
```

## CHANGES REQUIRED

Add primitive-loading mandate (ADR-05) to the existing orchestration spec. Every orchestration decision must reference specific primitive YAML IDs, not primitive family names. Add a new Section 3.3 ADR-05 Primitives table if one does not exist. Add a Dual-Source Validation requirement: every primitive invoked must be validated against both the YAML registry and the PRD module source.

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. This is an UPDATE to an EXISTING spec, not a new spec. Your output is a revised version of the existing file with targeted changes applied.

---

## MANDATORY PRE-WORK

1. Read the EXISTING SPEC FILE listed in EXISTING_FILE above. Understand its full structure before touching it.
2. Read the Master Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
3. Read the Source PRD module for context on what changed.
4. **PROOF:** Quote the specific section in the existing spec that needs updating.

---

## UPDATE FORMAT

Output the COMPLETE revised spec file. Do NOT output just the changed sections — output the whole file.
Mark all changed sections with `<!-- UPDATED: [reason] -->` HTML comments so changes are traceable.
Do NOT change anything outside the CHANGES_REQUIRED scope listed above.

## REJECTION: Changing sections not in scope | Removing existing DEP-IDs | Breaking existing AC | Omitting unchanged content

**Write the revised spec. No permission needed.**
