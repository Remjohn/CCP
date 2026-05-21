# Spec Prompt: FR-ERA3-08 — Mini App Host Shell

> **READY TO PASTE.** Copy this entire file into a clean session. Fill in nothing — the spec assignment is complete.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-08
SPEC_TITLE:      Mini App Host Shell
PHASE:           1 — Infrastructure
SOURCE_PRD:      PRD-01, PRD-04
MAPPED_STORIES:  Phase1 Epic1 Stories 1.1 (Secure Web App Initialization), 1.2 (Global DPA Theme Resolution), 1.3 (Dynamic Surface Routing)
CBAR_MANDATES:   Phase1-M01 (Optimistic Render Rule), Phase1-M02 (Zero-Network Theme Rule), Phase1-M03 (Primer Screen Rule)
BACKEND_REL:     NEW frontend — CONSUMES dpa_engine.py via DPAEngine.resolve(), uses Telegram.WebApp SDK (NOT telegram_webhook.py)
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-08_Mini_App_Host_Shell_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT** (read before pre-work):
> This is the HOST SHELL — a Vite+React frontend container. It is NOT a backend service. It uses the Telegram.WebApp JavaScript SDK. New endpoints are NOT added to main.py — this spec produces frontend code in tools/ or a new mini-app directory. The DPA ResolvedPalette is injected via the startapp URL parameter, not fetched at runtime.

---

## YOUR ROLE

You are the **Principal CCP Tech-Spec Architect**. You write engineering specifications that real developers build from. Your output must be so precise that a senior backend engineer can implement the feature without asking a single clarifying question. You are NOT a summarizer. You are NOT a planner. **You write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (DO THIS BEFORE WRITING A SINGLE LINE)

Read the following files IN ORDER. Confirm each by citing a specific fact in your Pre-Work Log. If you cannot read a file, STOP and report it — do not invent its contents.

**Step 1 — Master Protocol:** `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
Extract: backend stack (§2.1), API routes (§2.2), DB tables (§2.3), services per PRD module (§2.4), Pre-Flight Checklist (§3), 10-Section Format (§4), CBAR Mandate Enforcement format (§3 note).

**Step 2 — Source PRD Modules:** Files listed in SOURCE_PRD above.
Extract: ALL modes, schemas, integration flows, quality gates. From `## ERA 3 BROWNFIELD ANALYSIS`: what is NEW, EXISTING, OBSOLETE.
**PROOF REQUIRED:** Quote the exact FR definition for this spec from the PRD.

**Step 3 — Phase Epic File:** `docs/architecture/april_updates/Phase[N]_*_Epics.md`
Extract: Full Acceptance Criteria and Primitive Quality Constraints for each story in MAPPED_STORIES. Extract each CBAR Mandate listed in CBAR_MANDATES.
**PROOF REQUIRED:** Quote the exact acceptance criteria from the first mapped story.

**Step 4 — CBAR Audit File:** `docs/architecture/cbar_audits/CBAR_Audit_Phase[N]_*.md`
Confirm applicable mandates and check the Hallucination Purge section for corrected primitive IDs.

**Step 5 — Primitive YAMLs:** Load the PRIMARY primitive YAML for each family in the spec from `primitives/experience/`.
**PROOF REQUIRED:** Quote the `id:` and `name:` field from each YAML cited.
**BANNED PREFIX:** `EXP-TRB-*` does NOT exist. Any spec generating this prefix is immediately rejected.

**Step 6 — Existing Backend Files:** Read every Python file listed in BACKEND_REL from `src/ccp/services/`.
**PROOF REQUIRED:** Quote the actual method signature. Do not invent method names.

**Step 7 — Test Patterns:** Read 2 files from `tests/integration/`. Your Section 10 must follow the same pytest pattern.

---

## PRE-WORK LOG (REQUIRED BEFORE SPEC BODY)

```
1. PROTOCOL LOADED:   [cite one specific fact from §2 of the Protocol]
2. PRD LOADED:        [quote the exact FR definition from the PRD]
3. EPIC LOADED:       [quote the first acceptance criterion from the first mapped story]
4. CBAR AUDIT LOADED: [name the applicable mandates confirmed]
5. PRIMITIVES LOADED: [list each ID and name as read from YAML]
6. BACKEND FILES READ:[list each Python file + one method signature quoted]
7. TEST PATTERN:      [name the test files read + describe the pytest pattern]
```

If any entry is missing, you MUST NOT proceed.

---

## SPEC FORMAT — NON-NEGOTIABLE

Output the file only. Use this 10-section structure exactly. No merging, no skipping, no additions.

```
# Tech-Spec: [SPEC_ID] — [SPEC_TITLE]
**Created:** [date]
**Status:** Ready for Development
**Version:** 1.0 (ERA3 Architecture — CBAR-Hardened)
**Phase:** [PHASE]
**Architecture Reference:** ERA3_Tech_Spec_Writing_Protocol.md §7

## 1. Files Read
List EVERY file loaded with specific version or date. Proves the spec is grounded.

## 2. Overview
### 2.1 Problem Statement — What breaks without this spec? State the concrete failure mode.
### 2.2 Solution — One paragraph. What this builds and why it solves the problem.
### 2.3 Scope — In scope (bullet list) | Out of scope (bullet list, be ruthless)

## 3. Context for Development
### 3.1 Architecture Traceability — DEP-ID | Component | Source FR | What It Does
### 3.2 Existing Backend Integration — File | Path | How This Spec Uses It
   List EVERY existing Python file, DB table, and API route this spec extends or calls.
### 3.3 ADR-05 Primitives — Primitive ID | Name | Family | Constraint Applied
   ONLY primitives verified in the YAML registry.
### 3.4 CBAR Mandate Enforcement — Mandate | Phase-M# | Story Origin | Implementation Mechanism
   For each mandate: state the specific architectural decision that enforces it.
### 3.5 Technical Decisions — Decision | Rationale | Alternative Rejected | Why Rejected

## 4. Implementation Plan — Numbered phases, min 4, min 12 checkbox tasks referencing exact file paths.

## 5. Primary Output Schema — Pydantic v2 models. Fully typed. No Any. Extends existing src/ccp/models/ files.

## 6. Backward Compatibility Fallback — Graceful degradation. Reference circuit_breaker.py pattern.

## 7. Tasks — Sprint-ready checkbox list with exact file paths: create X in Y, modify Z in W.

## 8. Acceptance Criteria — Given/When/Then. Min 1 per mapped story. Each MUST include:
   - CBAR Mandate enforced (if applicable)
   - FAILURE EXAMPLE (concrete rejected state)
   - Measurable pass condition (SLA, threshold, boolean)

## 9. Dependencies
### Internal — Service/Spec | Dependency Type | What This Spec Needs From It
### External — API/Library | Version | Purpose

## 10. Testing Strategy
### Unit Tests — exact test file path + describe block + test name per critical function
### Integration Tests — modeled on named existing test file from tests/integration/
### Manual Verification — step-by-step QA checklist
```

---

## ANTI-LAZINESS ENFORCEMENT — IMMEDIATE REJECTION LIST

| Failure Mode | Example |
|---|---|
| Vague AC | "The Mini App loads correctly" — REJECTED |
| Missing FAILURE EXAMPLE | Any AC without one is incomplete |
| Hallucinated primitive IDs | Any `EXP-TRB-*` prefix or unverified ID |
| Invented method signatures | Calling a method name not found in the actual Python file |
| Generic testing strategy | "Write unit tests for all functions" — REJECTED |
| Missing Section 3.4 | Spec without CBAR Mandate Enforcement table |
| Reinventing existing services | New auth when telegram_webhook.py already handles Telegram identity |
| Pydantic `Any` types | `field: Any` in any output schema |
| Missing DEP-IDs | New components without allocated DEP-IDs |
| Pre-work log missing | Spec submitted without the 7-point log |

## MINIMUM DEPTH REQUIREMENTS

| Section | Minimum |
|---|---|
| Section 1 — Files Read | ≥ 8 files |
| Section 3.2 — Backend Integration | ≥ 3 existing files with real paths |
| Section 3.3 — Primitives | ≥ 2 verified IDs from YAML |
| Section 3.4 — CBAR Mandates | ALL mandates in CBAR_MANDATES covered |
| Section 4 — Implementation Plan | ≥ 4 phases, ≥ 12 checkbox tasks |
| Section 5 — Output Schema | ≥ 1 complete Pydantic model, fully typed |
| Section 8 — Acceptance Criteria | ≥ 1 AC per mapped story with FAILURE EXAMPLE |
| Section 10 — Testing | ≥ 3 named unit tests, ≥ 2 named integration tests |
| Total spec length | ≥ 300 lines |

---

## FINAL INSTRUCTION

Write the Pre-Work Log first. Do not proceed to the spec until all 7 steps are complete with cited evidence. Then write the spec in a single continuous output. Do not ask for permission. Do not summarize what you are about to do. **Write the spec.**
