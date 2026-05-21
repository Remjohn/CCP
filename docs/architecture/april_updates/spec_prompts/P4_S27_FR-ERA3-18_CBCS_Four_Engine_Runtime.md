# Spec Prompt: FR-ERA3-18 — CBCS Four-Engine Runtime

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-18
SPEC_TITLE:      CBCS Four-Engine Runtime
PHASE:           4 — Pipelines & Engines
SOURCE_PRD:      PRD-05
MAPPED_STORIES:  Phase4 Epic7 Story 7.1 (Continuous Voice Evidence Routing)
CBAR_MANDATES:   Phase4-M07 (Long Loop Framing Rule — capacity track downgrades MUST be reframed by Relationship Engine against 14/30-day positive trend; raw downgrades are strictly banned)
BACKEND_REL:     TBD — must audit all FR_CBCS_*.py services (14 files in docs/architecture/) before writing. Key services: trait_scoring_engine.py, change_talk_vault.py, spt_stage_engine.py, identity_anchor_protocol.py, learning_path_builder.py, dynamic_journaling_engine.py.
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-18_CBCS_Four_Engine_Runtime_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> The four engines are PHYSICALLY SEPARATE services: Diagnostic Engine, Ritual Engine, Evidence Engine, Relationship Engine. M-07 requires the Relationship Engine to INTERCEPT all Diagnostic Engine downgrades before they reach the user — define the intercept architecture and the long-loop context retrieval. AUDIT all FR_CBCS_*.py files before speccing.

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (all 7 steps, cite evidence for each)

1. **Protocol** `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` — extract §2 backend, §3 Pre-Flight, §4 Format, §3 CBAR note
2. **PRD Modules** (SOURCE_PRD) — extract modes, schemas, flows, quality gates, BROWNFIELD NEW/EXISTING/OBSOLETE. **PROOF:** Quote exact FR definition.
3. **Phase Epic** `docs/architecture/april_updates/Phase[N]_*_Epics.md` — extract AC + Primitive Constraints for MAPPED_STORIES + all CBAR_MANDATES. **PROOF:** Quote first AC.
4. **CBAR Audit** `docs/architecture/cbar_audits/CBAR_Audit_Phase[N]_*.md` — confirm mandates + Hallucination Purge.
5. **Primitive YAMLs** `primitives/experience/` — **PROOF:** Quote `id:` and `name:`. **BANNED:** `EXP-TRB-*`.
6. **Backend Python Files** `src/ccp/services/` — **PROOF:** Quote real method signature.
7. **Test Files** `tests/integration/` (read 2) — Section 10 must match pattern.

**PRE-WORK LOG — all 7 entries required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 300 LINES

§1 Files Read (≥8) | §2 Overview (Problem/Solution/Scope) | §3.1 DEP-IDs | §3.2 Backend Integration (≥3 files) | §3.3 Primitives (≥2 YAML IDs) | §3.4 CBAR Mandates (ALL) | §3.5 Technical Decisions | §4 Plan (≥4 phases, ≥12 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (≥1/story + FAILURE EXAMPLE + mandate) | §9 Dependencies | §10 Testing (≥3 unit + ≥2 integration named)

**INSTANT REJECTION:** Vague AC | No FAILURE EXAMPLE | EXP-TRB-* | Invented signatures | Generic tests | No §3.4 | Duplicate existing | Pydantic Any | No DEP-IDs | No pre-work log

**Write pre-work log. Then write the spec. No permission needed.**
