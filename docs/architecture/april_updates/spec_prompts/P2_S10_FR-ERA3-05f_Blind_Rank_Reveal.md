# Spec Prompt: FR-ERA3-05f — Blind Rank Reveal Mini App

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-05f
SPEC_TITLE:      Blind Rank Reveal Mini App
PHASE:           2 — Conscious Reactions
SOURCE_PRD:      PRD-06
MAPPED_STORIES:  Phase2 Epic5 Story 5.2 (Blind Rank Reveal Defense)
CBAR_MANDATES:   No direct Phase2 CBAR mandate — inherits CORE. EXP-SAF-002 (Possible-Win Scarcity) governs engineered tension from irreversible choices.
BACKEND_REL:     NEW Mini App (startapp=react_blind_rank) — CONSUMES FR-ERA3-05-CORE engine
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-05f_Blind_Rank_Reveal_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> The irreversibility mechanic (item 1 ranked permanently before item 2 reveals) is a pure frontend state machine — once a slot is assigned it is LOCKED. The spec must define the state machine formally. The humor/tension comes from visible regret when later items reveal poorly-fitting slots.

---

## YOUR ROLE

You are the **Principal CCP Tech-Spec Architect**. You write engineering specifications that real developers build from. Your output must be so precise that a senior backend engineer can implement the feature without asking a single clarifying question. You are NOT a summarizer. You are NOT a planner. **You write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (DO THIS BEFORE WRITING A SINGLE LINE)

**Step 1 — Master Protocol:** `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
Extract: backend stack (§2.1), API routes (§2.2), DB tables (§2.3), services per PRD (§2.4), Pre-Flight (§3), 10-Section Format (§4), CBAR format (§3 note).

**Step 2 — Source PRD Modules:** Files in SOURCE_PRD.
Extract: ALL modes, schemas, flows, quality gates. From `## ERA 3 BROWNFIELD ANALYSIS`: NEW / EXISTING / OBSOLETE.
**PROOF REQUIRED:** Quote the exact FR definition for this spec from the PRD.

**Step 3 — Phase Epic File:** `docs/architecture/april_updates/Phase[N]_*_Epics.md`
Extract: Full AC and Primitive Quality Constraints for each story in MAPPED_STORIES. Extract each CBAR Mandate in CBAR_MANDATES.
**PROOF REQUIRED:** Quote exact AC from first mapped story.

**Step 4 — CBAR Audit File:** `docs/architecture/cbar_audits/CBAR_Audit_Phase[N]_*.md`
Confirm applicable mandates. Check Hallucination Purge for corrected primitive IDs.

**Step 5 — Primitive YAMLs:** Load PRIMARY YAML for each family from `primitives/experience/`.
**PROOF REQUIRED:** Quote `id:` and `name:` from each YAML. **BANNED:** `EXP-TRB-*` prefix.

**Step 6 — Existing Backend Files:** Read each Python file in BACKEND_REL from `src/ccp/services/`.
**PROOF REQUIRED:** Quote the actual method signature.

**Step 7 — Test Patterns:** Read 2 files from `tests/integration/`. Section 10 must follow same pattern.

---

## PRE-WORK LOG (REQUIRED BEFORE SPEC BODY)

```
1. PROTOCOL LOADED:   [cite one specific fact from §2]
2. PRD LOADED:        [quote exact FR definition]
3. EPIC LOADED:       [quote first AC from first mapped story]
4. CBAR AUDIT LOADED: [name mandates confirmed]
5. PRIMITIVES LOADED: [list each ID and name from YAML]
6. BACKEND FILES READ:[list each Python file + method signature quoted]
7. TEST PATTERN:      [name test files read + pytest pattern]
```

If any entry is missing, you MUST NOT proceed.

---

## SPEC FORMAT — 10 SECTIONS, NO EXCEPTIONS

```
# Tech-Spec: [SPEC_ID] — [SPEC_TITLE]
**Status:** Ready for Development | **Version:** 1.0 (ERA3 — CBAR-Hardened)

## 1. Files Read
## 2. Overview (2.1 Problem Statement | 2.2 Solution | 2.3 Scope In/Out)
## 3. Context for Development
   3.1 Architecture Traceability (DEP-ID table)
   3.2 Existing Backend Integration (File | Path | How Used) — min 3 existing files
   3.3 ADR-05 Primitives (ID | Name | Family | Constraint) — YAML-verified only
   3.4 CBAR Mandate Enforcement (Mandate | Phase-M# | Story | Implementation Mechanism)
   3.5 Technical Decisions (Decision | Rationale | Alternative Rejected | Why)
## 4. Implementation Plan (min 4 phases, min 12 checkbox tasks with exact file paths)
## 5. Primary Output Schema (Pydantic v2, fully typed, no Any, extends existing models)
## 6. Backward Compatibility Fallback (circuit_breaker.py pattern)
## 7. Tasks (sprint-ready checkboxes, exact file paths)
## 8. Acceptance Criteria (Given/When/Then, min 1 per story, each with FAILURE EXAMPLE + mandate ref)
## 9. Dependencies (Internal table + External table)
## 10. Testing Strategy (named unit tests + named integration tests + manual QA checklist)
```

---

## REJECTION LIST

Vague AC | Missing FAILURE EXAMPLE | EXP-TRB-* prefix | Invented method signatures | Generic test strategy | Missing §3.4 | New service duplicating existing | Pydantic Any | Missing DEP-IDs | Pre-work log absent

## MINIMUMS: §1≥8 files | §3.2≥3 files | §3.3≥2 YAML IDs | §3.4 ALL mandates | §4≥12 tasks | §5≥1 typed model | §8≥1 AC/story with FAILURE EXAMPLE | §10≥3 unit+2 integration tests | Total≥300 lines

---

**Write the Pre-Work Log first. Then write the spec. Do not ask for permission. Write the spec.**
