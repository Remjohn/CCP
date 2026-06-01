# Spec Prompt: FR-ERA3-50E — Expressive Memory Bank And Proof Archive

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-50E
SPEC_TITLE:      Expressive Memory Bank And Proof Archive
PHASE:           7 — Living Commentary & Coach Communication Stack
SOURCE_PRD:      PRD-02 (CCF), PRD-05 (CBCS Law28)
MAPPED_STORIES:  Story bank, proof bank, testimonial bank, analogy bank, humor bank, future-image bank, objection bank, phrase bank, cultural reference bank, change_talk_vault bridge, MemoryFolder bridge
CBAR_MANDATES:   Bridge-Existing-Systems Rule, Memory-Feeds-Compilers Rule, No-Empty-Formula Rule
BACKEND_REL:     NEW memory store — MUST bridge to existing change_talk_vault, MemoryFolder, learning-path, and CBCS evidence logic without duplicating their storage
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-50E_Expressive_Memory_Bank_And_Proof_Archive_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This is a NEW spec, but bridge-oriented. Existing systems already store some expressive material (change_talk_vault, MemoryFolder, learning-path records, CBCS evidence). This spec unifies access to all expressive material through a single query surface.
>
> The Jim Rohn insight is critical here: communication begins before speaking. If the system has no lived or sourced expressive material, it will fall back to empty formulas. This memory bank prevents that.
>
> Memory bank families: stories, proof artifacts, testimonials, analogies, screenshots, comparisons, signature phrases, cultural references, humor material, future-image material, objection material.

> [!IMPORTANT]
> **MANDATORY LIVING COMMENTARY SOURCE SET (8 REFERENCE FILES):**
> - `lab/CCP APRIL Updates/05_Core_Experience/Living_Commentary_Realization_Layer_Source_of_Truth.md`
> - `lab/CCP APRIL Updates/01_Architecture_PRDs/Living_Commentary_Spec_Roadmap_And_Workflow_Inventory.md`
> - `docs/architecture/HANDOVER_CONSOLIDATION_BLUEPRINTS.md` (Master handover blueprint)
> - `docs/architecture/May 2026 UPDATES/Architectural_Audit_Trigger_First_Vision_Visual_Engines.md` (Pivots audit, Complete Editing Session and Remotion mandate)
> - `src/ccp/services/` (scan for change_talk_vault, memory_folder, learning_path, evidence files)
> - `docs/prd/modules/PRD_02_CCF_Content_Factory.md` (PRD Module)
> - `docs/prd/modules/PRD_05_CBCS_Law28.md` (PRD Module)
> - `docs/architecture/FR_CBCS_01_Change_Talk_Vault_Tech_Spec.md`

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-02`, `PRD-05`. **PROOF:** Quote lines on content intelligence and coaching evidence.
3. Master blueprints: `HANDOVER_CONSOLIDATION_BLUEPRINTS.md` and the pivots audit. **PROOF:** Quote details about Expressive Memory and static assets query layers within editing sessions.
4. Living Commentary source set: both doctrine docs. **PROOF:** Quote the memory bank section from Roadmap §4.3 and §4.4.
5. Existing memory systems: scan `src/ccp/services/` and `src/ccp/models/` for change_talk_vault, MemoryFolder, learning_path, evidence-related files. **PROOF:** Quote real method signatures and model schemas.
6. Existing CBCS evidence logic: read relevant CBCS service files. **PROOF:** Quote how evidence is currently stored and retrieved.
6. Existing test patterns: read 1 `tests/integration/` file covering memory or evidence behavior.

**PRE-WORK LOG — required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 300 LINES

§1 Files Read (>=5) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=3 files) | §3.3 Memory bank contracts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=4 phases, >=12 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define canonical schemas for:
  - `ExpressiveMemoryBank` — unified query surface across all memory families
  - `MemoryEntry` — id, family, content, source, tags, primitive_coalition, created_at, last_used_at, usage_count
  - `StoryBank` — curated stories with emotional arc tags
  - `ProofBank` — receipts, results, metrics, screenshots
  - `TestimonialBank` — client/community testimonials with permission status
  - `AnalogyBank` — reusable analogies mapped to communication modules
  - `HumorBank` — humor material with context tags and landing history
  - `FutureImageBank` — future-picture material for hope and commitment modules
  - `ObjectionBank` — captured objections with response pairings (bridges to FR-ERA3-50F)
  - `PhraseBank` — signature phrases and cultural references
- Define how the memory bank feeds into:
  - Content compilers (CCF/CMF)
  - Speaking practice systems (FR-ERA3-48)
  - Webinar module compilation (FR-ERA3-49)
  - Objection intelligence (FR-ERA3-50F)
- Define bridges to existing storage: change_talk_vault → StoryBank, MemoryFolder → general archive, learning-path → ProofBank

**REJECTION:** Duplicates existing storage systems | no unified query surface | no bridge to change_talk_vault / MemoryFolder | fewer than 6 memory families | no downstream consumer mapping | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
