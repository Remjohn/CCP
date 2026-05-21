# Spec Prompt: FR58 — UPDATE: Offer Tier Governor Tier Definitions

> **READY TO PASTE — SPEC UPDATE.** Copy into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:          FR58
SPEC_TITLE:       UPDATE: Offer Tier Governor Tier Definitions
PHASE:            6 — Existing Spec Updates
SOURCE_PRD:       PRD-09
EXISTING_FILE:    docs/architecture/FR58_Offer_Tier_Architecture_Tech_Spec.md
OUTPUT_FILE:      docs/architecture/FR58_Offer_Tier_Architecture_Tech_Spec_UPDATED.md
```

## CHANGES REQUIRED

Align OfferTierGovernor tier ceiling values with the canonical 4-tier pricing model: Tier 0 ( Proof Layer), Tier 1 (.99 Speaking & Learning), Tier 2 (.99 Coach OS), Tier 3 (.99 Elite). Update the eligibility check logic to use new ceiling values. Remove legacy tier definitions. Add the Loyalty Unlock flow reference (from Phase1-M06 Stored Value Rule) for high-investment Free Tier users.

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
