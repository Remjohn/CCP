# Spec Prompt: FR-COM-01 — UPDATE: Pricing Tier Update (.99/.99)

> **READY TO PASTE — SPEC UPDATE.** Copy into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:          FR-COM-01
SPEC_TITLE:       UPDATE: Pricing Tier Update (.99/.99)
PHASE:            6 — Existing Spec Updates
SOURCE_PRD:       PRD-09
EXISTING_FILE:    docs/architecture/FR-COM-01_AFFiNE_Billing_Credit_System_Tech_Spec.md
OUTPUT_FILE:      docs/architecture/FR-COM-01_AFFiNE_Billing_Credit_System_Tech_Spec_UPDATED.md
```

## CHANGES REQUIRED

Update all pricing references to match the canonical 4-tier model:  (Proof Layer), .99/mo (Speaking & Learning Tier 1), .99/mo (Coach OS Tier 2), .99/mo (Elite Tier 3). Remove ALL legacy free trial references. Remove ALL legacy SaaS pricing references. Update the offer_tier_governor integration to use the new tier ceiling values.

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
