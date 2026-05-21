# PROMPT: Generate the Era 3 Spec Writing Briefing

> **Purpose:** Paste this entire prompt into a CLEAN session to generate the definitive `ERA3_Spec_Writing_Briefing.md` — the single source of truth document that any spec-writer agent or human reads FIRST before writing any Era 3 Tech Spec.
>
> **Output File:** `docs/architecture/april_updates/ERA3_Spec_Writing_Briefing.md`

---

## YOUR TASK

You are the Principal CCP Spec Architect. Your job is to generate a comprehensive **Spec Writing Briefing** document that serves as the SINGLE ENTRY POINT for any agent or human tasked with writing Era 3 Tech Specs for the Conscious Coaching Platform (CCP).

This document replaces the obsolete `docs/architecture/SPEC_REWRITE_BRIEFING.md` (which covers the retired CA11 Studio pivot from March 2026).

---

## FILES YOU MUST READ (IN THIS ORDER)

Read ALL of the following files before generating the briefing. Do not skip any.

### 1. The Master Protocol (READ THIS FIRST)
```
docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md
```
This is the canonical spec writing protocol. It contains:
- The full existing backend architecture (§2) — 201 services, 45 models, 17 pipelines, 17 agents
- The mandatory 7-step Pre-Flight Checklist (§3) including CBAR mandate loading
- The 10-Section Spec Format (§4) with CBAR Mandate Enforcement
- The Mini App Separation Doctrine (§5) — 4 architectural categories for Conscious Reactions
- The Experience Primitive Family Keys (§5.2) — 8 families, 51 YAMLs
- The complete Execution Order (§7) — 34 specs across 6 phases with Pre-Flight and Backend Relationship columns
- The CBAR Mandate Summary (§8) — all 33 binding mandates
- The Key Reference Files (§9)

### 2. The 9 PRD Modules (Source of Truth for ALL specs)
```
docs/prd/modules/PRD_INDEX.md
docs/prd/modules/PRD_01_CCP_Platform_Strategy.md
docs/prd/modules/PRD_02_CCF_Content_Factory.md
docs/prd/modules/PRD_03_CMF_Media_Factory.md
docs/prd/modules/PRD_04_CVE_Experience_Design.md
docs/prd/modules/PRD_05_CBCS_Law28.md
docs/prd/modules/PRD_06_Conscious_Reactions.md
docs/prd/modules/PRD_07_V2WS_Webinar.md
docs/prd/modules/PRD_08_Conscious_Primitives.md
docs/prd/modules/PRD_09_CPSC_Silent_Referral.md
```
Each PRD module contains an `## ERA 3 BROWNFIELD ANALYSIS` section at the bottom that identifies what's NEW, what's EXISTING, and what's OBSOLETE. This is critical for understanding backend relationships.

### 3. The 5 CBAR-Hardened Phase Epic Files
```
docs/architecture/april_updates/Phase1_Infrastructure_Epics.md          — 7 CBAR Mandates
docs/architecture/april_updates/Phase2_Conscious_Reactions_Epics.md     — 7 CBAR Mandates
docs/architecture/april_updates/Phase3_Experience_Mini_Apps_Epics.md    — 7 CBAR Mandates
docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md   — 7 CBAR Mandates
docs/architecture/april_updates/Phase5_Growth_Epics.md                  — 5 CBAR Mandates
```
These contain the user stories, acceptance criteria, and CBAR mandates that every spec must enforce. Each spec maps to one or more stories in these files.

### 4. The 5 CBAR Audit Files (Adversarial Audit Trail)
```
docs/architecture/cbar_audits/CBAR_Audit_Phase1_Infrastructure.md
docs/architecture/cbar_audits/CBAR_Audit_Phase2_Conscious_Reactions.md
docs/architecture/cbar_audits/CBAR_Audit_Phase3_Experience_Mini_Apps.md
docs/architecture/cbar_audits/CBAR_Audit_Phase4_Pipelines_and_Engines.md
docs/architecture/cbar_audits/CBAR_Audit_Phase5_Growth.md
```

### 5. The CBAR Engine Protocol
```
docs/architecture/spec updates/CBAR_Constraint_Based_Adversarial_Reasoning.md
```

### 6. The Epic & Story Writing Protocol
```
docs/architecture/april_updates/ERA3_Epic_and_Story_Writing_Protocol.md
```

### 7. The Previous Specs (for format reference ONLY — these are retired/superseded)
```
docs/architecture/april_updates/previous specs/FR-APR-*.md   (9 files — superseded by ERA3 format)
```

### 8. Legacy Spec Examples (for understanding existing backend patterns ONLY)
Scan these to understand the spec depth and traceability patterns used in the codebase, but do NOT use their format — use the ERA3 10-section format:
```
docs/architecture/FR-CA11-01_Coach_Workspace_Provisioning_Tech_Spec.md  (format reference)
docs/architecture/FR61_Jim_Rohn_Voice_Coach_Engine_Tech_Spec.md         (deepest existing spec)
```

### 9. Existing Backend Architecture Reference
```
src/ccp/api/main.py                    — FastAPI entry point
src/ccp/models/                        — 45+ Pydantic model files
src/ccp/services/                      — 201+ service files
src/ccp/pipelines/                     — 17 pipeline files
src/ccp/agents/                        — 17 agent files
src/ccp/scripts/setup_supabase.py      — Database schema
src/ccp/scripts/setup_neo4j.py         — Graph schema
tests/integration/                     — 88 existing tests
```

### 10. Experience Primitives Registry
```
primitives/experience/                 — 51 experience primitive YAMLs across 8 families
primitives/meaning/                    — 192+ meaning primitive YAMLs
```

---

## OUTPUT STRUCTURE

Generate the file `docs/architecture/april_updates/ERA3_Spec_Writing_Briefing.md` with the following structure. This is the definitive document. It must be comprehensive enough that a spec-writer agent with NO prior context can read it and produce a correct spec.

```markdown
# Era 3 Spec Writing Briefing — Conscious Coaching Platform

> [!CAUTION]
> **This document is the MANDATORY first read for ANY agent or human writing Era 3 Tech Specs.**
> It supersedes the retired `SPEC_REWRITE_BRIEFING.md` (CA11 Studio pivot, March 2026).

## 1. What Is Era 3 and Why It Matters
- Brief context: The CCP is a Telegram-native coaching OS
- Era 3 = Mini App architecture + behavioral primitives + CBAR-hardened epics
- 34 specs across 6 phases, 33 binding CBAR mandates
- The platform has a fully built Python/FastAPI backend (201 services, 45 models) — specs EXTEND, not reinvent

## 2. The Spec Writing Pipeline (Step-by-Step)
Walk through the exact sequence a spec writer follows:
1. Read THIS briefing
2. Read the ERA3_Tech_Spec_Writing_Protocol.md (the master protocol)
3. Identify which Phase and Spec number you are writing
4. Execute the 7-step Pre-Flight Checklist from the protocol
5. Write the spec using the 10-Section Format
6. Self-audit against CBAR mandates
7. Submit for review

## 3. Source Documents Hierarchy
A table showing the document hierarchy and what to extract from each:
- PRD Modules (functional requirements + brownfield analysis)
- Phase Epic Files (user stories + CBAR mandates + primitive constraints)
- CBAR Audit Files (adversarial audit trail + hallucination correction logs)
- ERA3 Protocol (backend architecture + spec format + execution order)
- Primitive Registry YAMLs (behavioral constraints)

## 4. The 34 Specs — Master Inventory
A comprehensive table of ALL 34 specs across 6 phases, with columns:
- Spec #, FR ID, Title, Source PRD, Phase Epic File, Mapped Story IDs, CBAR Mandates to Enforce, Backend Relationship (NEW/CONSUMES/REPLACES/READS), Status (Not Started / In Progress / Complete)

Pull this data from §7 of the ERA3_Tech_Spec_Writing_Protocol.md and cross-reference with the Phase Epic files to add the Story ID and CBAR Mandate columns.

## 5. The 33 CBAR Mandates — Quick Reference
Pull the full mandate summary table from §8 of the ERA3_Tech_Spec_Writing_Protocol.md.
Add a "Spec(s) Affected" column showing which FR-ERA3-XX spec(s) each mandate applies to.

## 6. The 10-Section Spec Format (with CBAR integration)
The exact template a spec writer copies and fills in, pulled from §4 of the protocol but expanded with:
- Detailed instructions for each section
- Example of what a CBAR Mandate Enforcement subsection looks like
- Example of what an Acceptance Criteria item with CBAR reference looks like

## 7. The 7-Step Pre-Flight Checklist
Pull from §3 of the protocol. For each step, add the specific file paths the writer should load.

## 8. Experience Primitive Families — Quick Reference
Pull the 8-family table from §5.2 of the protocol.
Add: the YAML directory path for each family so the writer can load them.

## 9. Mini App Architecture Categories
Pull from §5.1 of the protocol — the 4 categories (Reaction Modes, User Roles, Options/Mechanics, Content Creation Experiences) with their startapp IDs.

## 10. Execution Order & Dependencies
Pull the Phase 1-6 execution order from §7 of the protocol.
Add dependency arrows showing which specs must be written before others.

## 11. Existing Backend Quick Reference
A condensed version of §2 from the protocol — the stack summary, existing API routes, database schema, and key services grouped by PRD module. Just enough for the spec writer to know what exists.

## 12. Anti-Slop Mandate
State the following rules explicitly:
- No hallucinated primitive IDs — every EXP-* ID must be verified against the YAML registry
- No speculative architecture — every service, model, and route must trace to an existing backend file or be explicitly marked NEW
- No CBAR mandate gaps — every spec must declare its applicable mandates
- No format deviations — all specs follow the 10-section format exactly
- The corrected primitive prefix is `EXP-TRS-*` (Trust & Status), NOT `EXP-TRB-*` (hallucinated)
- Phase 2 Epics file uses an older format — mandates are at the bottom, not the top

## 13. Quality Gates
A checklist that every spec must pass before being marked "Ready for Development":
- [ ] Section 1 lists ALL files read (PRD + Epic + primitives + existing code)
- [ ] Section 3 includes "CBAR Mandate Enforcement" subsection
- [ ] Section 3 includes "Existing Backend Integration" subsection with exact Python file paths
- [ ] Section 3 references specific primitive YAML IDs (not family names)
- [ ] Section 8 Acceptance Criteria include FAILURE EXAMPLES and CBAR mandate references
- [ ] All primitive IDs verified against YAML registry (no EXP-TRB-* prefix)
- [ ] All CBAR mandates from the mapped Epic stories are declared and enforced
- [ ] Backend relationship is explicit (NEW/CONSUMES/REPLACES/READS + file paths)
- [ ] New endpoints are added to existing FastAPI app, not a separate service (unless justified)
- [ ] New models follow existing Pydantic pattern
- [ ] Testing strategy references existing pytest patterns in tests/integration/

## 14. File Paths — Complete Reference
A master table of EVERY file referenced in this briefing with its absolute path and purpose.
```

---

## CRITICAL CONSTRAINTS

1. **DO NOT invent information.** Every fact must come from the files you read. If a file doesn't exist or you can't read it, say so explicitly.

2. **DO NOT use the old CA11 spec format** (`FR-CA11-XX`). The new format is `FR-ERA3-XX` with the 10-section structure.

3. **DO NOT reference the retired `SPEC_REWRITE_BRIEFING.md`** as current — reference it only as the superseded predecessor.

4. **The 34 specs are defined in §7 of the ERA3_Tech_Spec_Writing_Protocol.md.** Do not invent new spec IDs.

5. **The 33 CBAR mandates are defined in §8 of the ERA3_Tech_Spec_Writing_Protocol.md** and in the 5 Phase Epic files. Cross-reference both.

6. **Status of ALL 34 specs is "Not Started"** — zero ERA3 specs have been written yet. The `previous specs/FR-APR-*.md` files are superseded predecessors, not current specs.

7. **The document must be self-contained enough** that a spec writer can read ONLY this briefing + the master protocol and know exactly what to do. No hunting through conversation logs.

8. **Primitive ID integrity:** The CBAR audits revealed systemic hallucination of the `EXP-TRB-*` prefix. The correct prefix is `EXP-TRS-*` (Trust & Status family). The briefing must warn about this.

9. **Mark the old `docs/architecture/SPEC_REWRITE_BRIEFING.md` as RETIRED** at the top of the new document, explicitly stating it is superseded.

---

## TONE & FORMAT

- Write as a PM/Architect briefing a senior engineering team
- Use tables heavily — they are more scannable than prose
- Use GitHub-style alerts (`[!CAUTION]`, `[!IMPORTANT]`, `[!WARNING]`) for critical rules
- Keep prose concise — prefer bullet points and structured data
- The document should be approximately 400-600 lines
- Use relative file paths from the workspace root (`docs/...`, `src/...`, `primitives/...`)
