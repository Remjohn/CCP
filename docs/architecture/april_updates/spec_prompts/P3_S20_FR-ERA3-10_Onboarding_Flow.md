# Spec Prompt: FR-ERA3-10 — Zero-Config Onboarding Flow Mini App

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-10
SPEC_TITLE:      Zero-Config Onboarding Flow Mini App
PHASE:           3 — Experience Mini Apps
SOURCE_PRD:      PRD-01, PRD-04
MAPPED_STORIES:  Phase3 Epic6 Story 6.1 (Audit-to-Challenge Conversion)
CBAR_MANDATES:   Phase3-M07 (Auth-Free Benchmark Rule — benchmark teaser score MUST be delivered BEFORE any registration, email, or auth gate)
BACKEND_REL:     NEW Mini App — first-touch experience before any reaction mode. CONSUMES trait_scoring_engine.py for 60-second baseline audit. CONSUMES offer_tier_governor.py for post-reveal Lead Magnet surfacing.
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-10_Onboarding_Flow_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> M-07 is absolute: the dopamine hit (benchmark score) must precede ANY commercial ask. The spec must define the anonymous Mini App session model (no Telegram identity required for audit). The flow is: tap link → 60-second voice audit → immediate score reveal (anonymous) → Lead Magnet offer → optional registration. Define the state machine and data persistence model for anonymous-to-registered transition.

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
