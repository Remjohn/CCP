# Spec Prompt: FR-ERA3-17 — Voice Prompt Engine

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-17
SPEC_TITLE:      Voice Prompt Engine
PHASE:           4 — Pipelines & Engines
SOURCE_PRD:      PRD-04
MAPPED_STORIES:  Phase4 Epic6 Story 6.1 (Emotional Job Routing)
CBAR_MANDATES:   Phase4-M06 (Sonic Prestige Rule — ALL voice prompts must use ConsciousVoice TTS model or pre-recorded human coach audio; generic robotic TTS strictly banned)
BACKEND_REL:     TBD — must audit soundboard_service.py and engagement_feedback.py before writing. The 6 emotional jobs are: Orient, Relieve, Validate, Invite, Redirect, Celebrate.
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-17_Voice_Prompt_Engine_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> M-06: Generic TTS fallback is explicitly banned — spec must define queue-and-retry or pre-recorded fallback strategy when ConsciousVoice is unavailable. The VoicePromptPacket must select EXACTLY ONE emotional job per prompt — combining jobs is a critical UX failure. Define the job-selection state machine. AUDIT soundboard_service.py first.

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
