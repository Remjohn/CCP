# Spec Prompt: FR-ERA3-09 — Conscious Editor Mini App

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-09
SPEC_TITLE:      Conscious Editor Mini App
PHASE:           3 — Experience Mini Apps
SOURCE_PRD:      PRD-02, PRD-03
MAPPED_STORIES:  Phase3 Epic3 Stories 3.1 (Trigger-First Artifact Review), 3.2 (CMF Media Validation & Operator Review)
CBAR_MANDATES:   Phase3-M05 (Modular CMF Recovery Rule — single-word transcript correction must NOT trigger full NIM re-run or full audio re-record)
BACKEND_REL:     NEW Mini App (startapp=editor) — CONSUMES content_machine.py output artifacts, CONSUMES canvas_composition_service.py for visual rendering, CONSUMES abel_vcb_generator.py for visual prompts
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-09_Conscious_Editor_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> M-05 is the key engineering challenge: define GRANULAR re-render scopes. A transcript correction must re-render ONLY the affected caption/text layer — NOT re-run the NIM biometric pipeline, NOT trigger audio re-record. The spec must define the render scope taxonomy (full re-run vs. caption-only re-render vs. visual-only re-render).

---

## YOUR ROLE

You are the **Principal CCP Tech-Spec Architect**. Write specifications so precise that a senior engineer can implement without asking a single clarifying question. NOT a summarizer. NOT a planner. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK

**Step 1 — Protocol:** `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` — extract §2.1 stack, §2.2 routes, §2.3 tables, §2.4 services, §3 Pre-Flight, §4 Format, §3 CBAR note.
**Step 2 — PRD Modules:** Listed in SOURCE_PRD. Extract all modes, schemas, flows, quality gates, and BROWNFIELD ANALYSIS (NEW/EXISTING/OBSOLETE). **PROOF:** Quote exact FR definition.
**Step 3 — Phase Epic File:** `docs/architecture/april_updates/Phase[N]_*_Epics.md` — extract full AC + Primitive Quality Constraints for MAPPED_STORIES + all CBAR_MANDATES. **PROOF:** Quote first AC.
**Step 4 — CBAR Audit:** `docs/architecture/cbar_audits/CBAR_Audit_Phase[N]_*.md` — confirm mandates + Hallucination Purge corrections.
**Step 5 — Primitive YAMLs:** `primitives/experience/`. **PROOF:** Quote `id:` and `name:` from each YAML. **BANNED:** `EXP-TRB-*`.
**Step 6 — Backend Python Files:** Read each file in BACKEND_REL. **PROOF:** Quote real method signature.
**Step 7 — Test Patterns:** Read 2 files from `tests/integration/`. Section 10 must match pattern.

## PRE-WORK LOG (all 7 entries required before spec body)
```
1. PROTOCOL LOADED:   2. PRD LOADED:   3. EPIC LOADED:   4. CBAR LOADED:   5. PRIMITIVES:   6. BACKEND:   7. TESTS:
```

---

## SPEC FORMAT (10 sections, no exceptions, min 300 lines)

§1 Files Read (≥8) | §2 Overview (Problem/Solution/Scope) | §3 Context: 3.1 DEP-IDs, 3.2 Backend Integration (≥3 files), 3.3 Primitives (≥2 YAML-verified IDs), 3.4 CBAR Mandate Enforcement (ALL mandates), 3.5 Technical Decisions | §4 Implementation Plan (≥4 phases, ≥12 tasks) | §5 Output Schema (Pydantic v2, no Any) | §6 Fallback (circuit_breaker.py) | §7 Tasks | §8 AC (≥1 per story, each with FAILURE EXAMPLE + mandate ref) | §9 Dependencies | §10 Testing (≥3 unit + ≥2 integration, named)

**REJECTIONS:** Vague AC | No FAILURE EXAMPLE | EXP-TRB-* | Invented signatures | Generic tests | No §3.4 | Duplicate existing services | Pydantic Any | No DEP-IDs | No pre-work log

**Write Pre-Work Log first. Then write the spec. No permission needed. Write the spec.**
