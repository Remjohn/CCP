# Primitive Codification Refresh Implementation Plan

## Purpose

This plan fixes the current gap between:

- the updated modular CCP PRDs
- the primitive codification skill and family templates
- the already-written meaning primitives

The current problem is not the primitive idea itself. The problem is that the codification workflow was authored against older, less precise CCP architecture, so many examples, contexts, and use cases are now too shallow, too generic, or too legacy-biased.

The objective is to make primitive codification use the modular PRDs as the active source of truth and to raise the example standard so primitives become usable for current CCP feature design, content generation, product experience design, evaluation, and future agent retrieval.

---

## Current State

### Written Primitive Inventory

Only meaning primitives are currently written.

- `_golden`: `1`
- `design_business`: `14`
- `humor_distortion`: `39`
- `narrative_structure`: `13`
- `performance_delivery`: `10`
- `persuasion`: `35`
- `psychological_diagnostics`: `12`
- `referral_trust_transfer`: `9`
- `visual_sonic_guidance`: `12`
- `voice_audio_intimacy`: `12`

Meaning primitive YAML total: `157`

Not yet written:

- `connection`: `0`
- `contrast`: `0`
- `explanation_translation`: `0`
- `story_discovery`: `0`
- all experience primitive YAML families: `0`

### Root Cause Summary

1. The codification skill did not require loading `docs/prd/modules/PRD_INDEX.md` and relevant modular PRDs.
2. The templates still enforced only `2` examples, which is too weak for current CCP specificity.
3. Existing examples often name generic "content creation" or "the app" rather than current CCP modules and surfaces.
4. The workflow did not require one source-book example plus multiple CCP use cases.
5. There is no backfill process yet for already-written meaning primitives.

---

## Target State

Every primitive codification workflow must:

1. Read the source audit and source book.
2. Read `PRD_INDEX.md`.
3. Read the relevant modular PRDs for the primitive's family and CCP surface.
4. Produce examples that include:
   - `1` book-grounded mechanism example
   - `4` CCP use cases grounded in current CCP modules
5. Name actual CCP surfaces:
   - `CCF`
   - `CMF`
   - `CVE`
   - `CBCS`
   - `Conscious Reactions`
   - `V2WS`
   - `CPSC`
   - `Telegram`
   - `AFFiNE`
   - `church/community`
6. Stop using generic example phrasing.
7. Be auditable against the modular PRDs and current architecture.

---

## Scope

### In Scope

- `skills/primitives/SKILL_Primitive_YAML_Codification.md`
- all family templates under `skills/primitives/templates`
- all existing meaning primitive YAMLs under `primitives/meaning`
- future experience primitive codification workflow
- primitive quality-control rules and validation checks

### Out of Scope

- rewriting the modular PRDs themselves
- redesigning the primitive registries again
- rewriting audits
- writing experience primitive YAMLs immediately

---

## Workstreams

## Workstream 1: Skill-Level Source-of-Truth Fix

### Goal

Make the codification skill itself impossible to use without current PRD context.

### Required Changes

1. Add mandatory PRD loading discipline to:
   - read `docs/prd/modules/PRD_INDEX.md`
   - read relevant module set before writing a primitive
2. Replace the current example rule:
   - from: `at least 2 examples`
   - to: `1 book example + 4 CCP use cases`
3. Add explicit ban on vague CCP contexts such as:
   - "content creation"
   - "the app"
   - "a coach could use this"
4. Update schema comments so examples are structurally expected to follow this rule.
5. Update pre-save validation checklist accordingly.

### Status

Partially started. The skill file has already been patched at the source-loading layer, but the full refresh is not complete yet.

---

## Workstream 2: Template Normalization

### Goal

Make every family template point to the correct PRDs and enforce the same example quality standard.

### Files

Meaning templates:

- `TEMPLATE_meaning_design_business.md`
- `TEMPLATE_meaning_humor_distortion.md`
- `TEMPLATE_meaning_narrative_structure.md`
- `TEMPLATE_meaning_performance_delivery.md`
- `TEMPLATE_meaning_persuasion.md`
- `TEMPLATE_meaning_psychological_diagnostics.md`
- `TEMPLATE_meaning_referral_trust_transfer.md`
- `TEMPLATE_meaning_supplemental_gaps.md`
- `TEMPLATE_meaning_visual_sonic_guidance.md`
- `TEMPLATE_meaning_voice_audio_intimacy.md`

Experience templates:

- `TEMPLATE_experience_trigger_timing.md`
- `TEMPLATE_experience_friction_ability.md`
- `TEMPLATE_experience_trust_branding.md`
- `TEMPLATE_experience_feedback_scoring.md`
- `TEMPLATE_experience_progression_replay.md`
- `TEMPLATE_experience_social_referral.md`
- `TEMPLATE_experience_safe_failure_recovery.md`
- `TEMPLATE_experience_personalization_identity.md`

### Required Changes

Each template must:

1. Load the codification skill.
2. Load the correct golden example.
3. Load the appropriate registry spec section.
4. Load `PRD_INDEX.md`.
5. Load the relevant modular PRD module set for that family.
6. Replace the checklist item `At least 2 examples` with the new standard.
7. Explicitly instruct the writer to include:
   - `1` book-native or book-mechanism example
   - `4` CCP use cases
8. Use current CCP language in the anti-generic enforcement text.

### Family-to-PRD Routing

#### Meaning families

- `design_business`:
  - `PRD_01`, `PRD_02`, `PRD_03`, `PRD_04`, `PRD_06`, `PRD_07`, `PRD_08`
- `humor_distortion`:
  - `PRD_02`, `PRD_03`, `PRD_04`, `PRD_05`, `PRD_06`, `PRD_07`, `PRD_08`
- `narrative_structure`:
  - `PRD_02`, `PRD_03`, `PRD_04`, `PRD_05`, `PRD_06`, `PRD_07`, `PRD_08`
- `performance_delivery`:
  - `PRD_03`, `PRD_04`, `PRD_05`, `PRD_06`, `PRD_07`, `PRD_08`
- `persuasion`:
  - `PRD_02`, `PRD_04`, `PRD_05`, `PRD_06`, `PRD_07`, `PRD_08`, `PRD_09`
- `psychological_diagnostics`:
  - `PRD_04`, `PRD_05`, `PRD_06`, `PRD_07`, `PRD_08`, `PRD_09`
- `referral_trust_transfer`:
  - `PRD_04`, `PRD_05`, `PRD_06`, `PRD_08`, `PRD_09`
- `visual_sonic_guidance`:
  - `PRD_02`, `PRD_03`, `PRD_04`, `PRD_06`, `PRD_07`, `PRD_08`
- `voice_audio_intimacy`:
  - `PRD_02`, `PRD_03`, `PRD_04`, `PRD_05`, `PRD_06`, `PRD_07`, `PRD_08`, `PRD_09`

#### Experience families

- `trigger_timing`:
  - `PRD_04`, `PRD_05`, `PRD_06`, `PRD_07`, `PRD_08`, `PRD_09`
- `friction_ability`:
  - `PRD_04`, `PRD_05`, `PRD_06`, `PRD_07`, `PRD_09`
- `trust_branding`:
  - `PRD_03`, `PRD_04`, `PRD_06`, `PRD_07`, `PRD_08`, `PRD_09`
- `feedback_scoring`:
  - `PRD_04`, `PRD_05`, `PRD_06`, `PRD_07`, `PRD_08`, `PRD_09`
- `progression_replay`:
  - `PRD_04`, `PRD_05`, `PRD_06`, `PRD_07`, `PRD_08`, `PRD_09`
- `social_referral`:
  - `PRD_04`, `PRD_05`, `PRD_06`, `PRD_08`, `PRD_09`
- `safe_failure_recovery`:
  - `PRD_04`, `PRD_05`, `PRD_06`, `PRD_07`, `PRD_08`, `PRD_09`
- `personalization_identity`:
  - `PRD_04`, `PRD_05`, `PRD_06`, `PRD_07`, `PRD_08`, `PRD_09`

---

## Workstream 3: Existing Meaning Primitive Backfill

### Goal

Bring the already-written `157` meaning primitives up to the new standard.

### Why This Is Necessary

Even if the templates are fixed, the current YAML library will still contain legacy examples. Agents reading old primitives will keep inheriting weak or stale CCP contexts.

### Backfill Strategy

Run a structured refresh across all written meaning primitives.

For each YAML:

1. Keep the primitive ID, canonical name, and source audit block unless clearly wrong.
2. Re-check against the source book if `why_it_works` looks audit-only or shallow.
3. Replace the example block with:
   - `1` book-grounded example
   - `4` CCP use cases
4. Make sure CCP examples cite current modules and real product surfaces.
5. Check trigger/suppression conditions for legacy wording.
6. Recheck synergy IDs only if the family relationships look stale.

### Backfill Order

Recommended order by impact:

1. `persuasion` `35`
2. `humor_distortion` `39`
3. `narrative_structure` `13`
4. `voice_audio_intimacy` `12`
5. `visual_sonic_guidance` `12`
6. `psychological_diagnostics` `12`
7. `design_business` `14`
8. `performance_delivery` `10`
9. `referral_trust_transfer` `9`

Rationale:

- `persuasion`, `humor`, and `narrative` drive high volumes of script behavior.
- `voice`, `visual`, and `design` affect media treatment and premium quality.
- `psychological diagnostics` and `referral` govern fit, continuity, and spread.

---

## Workstream 4: Validation and Linting

### Goal

Prevent this drift from recurring.

### Required Controls

Add a primitive QA pass with at least these checks:

1. Example count check:
   - exactly `1` book example minimum
   - at least `4` CCP use cases
2. PRD naming check:
   - CCP examples must mention actual module surfaces
3. Generic phrase check:
   - flag phrases like:
     - "a coach could use this"
     - "in content creation"
     - "in the app"
4. Missing surface check:
   - if a primitive clearly belongs to `Conscious Reactions`, `CBCS`, or `V2WS` but examples never name those surfaces, flag it
5. Optional later:
   - family-specific example validators
   - YAML linter for example prefix conventions such as `BOOK:` and `CCP:`

### Output

A lightweight validation script or checklist that can be run before committing new primitives.

---

## Workstream 5: Experience Primitive Readiness

### Goal

Ensure experience primitive writing starts with the corrected workflow instead of repeating the same drift.

### Required Actions

1. Finish the skill and template refresh first.
2. Do not write experience YAMLs until all experience templates are updated.
3. Start experience codification only after:
   - PRD routing is in place
   - example requirements are upgraded
   - validation checks are active

This prevents a second cleanup cycle later.

---

## Deliverables

### Phase 1

- updated `SKILL_Primitive_YAML_Codification.md`
- updated all `18` family templates

### Phase 2

- complete inventory report for all written meaning families
- refresh plan per family with counts and status

### Phase 3

- updated meaning YAMLs in priority order
- validation checklist or script

### Phase 4

- experience template readiness confirmed
- experience codification can begin

---

## Acceptance Criteria

This project is considered fixed when:

1. Every primitive template requires modular PRD loading.
2. Every primitive template requires:
   - `1` book-grounded example
   - `4` CCP use cases
3. Existing written meaning primitives are refreshed family by family.
4. CCP examples explicitly reflect current architecture rather than generic language.
5. A validator or checklist exists to stop regression.

---

## Recommended Execution Order

1. Finish the skill file update.
2. Patch all family templates.
3. Run a quick scan to confirm every template mentions:
   - `PRD_INDEX.md`
   - relevant modules
   - `1` book example + `4` CCP use cases
4. Backfill written meaning families in the priority order above.
5. Add validation/linting.
6. Only then resume primitive writing at scale.

---

## Immediate Next Action

Complete Workstream 1 and Workstream 2 first.

Reason:

There is no point refreshing existing primitives while the upstream skill and templates are still capable of generating the same shallow structure again.
