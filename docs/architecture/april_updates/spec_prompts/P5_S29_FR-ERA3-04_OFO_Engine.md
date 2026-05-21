# Spec Prompt: FR-ERA3-04 — OFO Engine (Object First Outreach)

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-04
SPEC_TITLE:      OFO Engine (Object First Outreach)
PHASE:           5 — Growth
SOURCE_PRD:      PRD-09
MAPPED_STORIES:  Phase5 Epic2 Stories 2.1 (4-Asset Proof Package Delivery), 2.2 (Stealth Course Accountability Hook)
CBAR_MANDATES:   Phase5-M03 (OFO Ego-Defense Rule — audit must use Crusade Narrative framing, positioned as defending coach's legacy, NOT clinical criticism), Phase5-M04 (Inline Capture Hook — full Hook Cycle must complete within single Telegram session, no deferred scheduling)
BACKEND_REL:     NEW service — no existing backend handles OFO. CONSUMES content_machine.py for asset generation, CONSUMES trait_scoring_engine.py for public content biometric analysis, CONSUMES abel_vcb_generator.py for visual assets.
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-04_OFO_Engine_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> The 4-asset package: Carousel, Storytelling Video, Reels Explainer, Animated Video Audit. M-03 governs the Animated Video Audit framing — must use Epic Meaning language, positioning the platform as defending the coach's authority against algorithmic compression. M-04 is the conversion engine: the Hook Cycle (trigger→action→reward→investment) must complete in a single session.

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all 7 steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` — §2 backend, §3 Pre-Flight, §4 Format
2. PRD Modules (SOURCE_PRD) — BROWNFIELD NEW/EXISTING/OBSOLETE. **PROOF:** Quote exact FR definition.
3. Phase Epic: `docs/architecture/april_updates/Phase5_Growth_Epics.md` — full AC + Primitive Constraints + CBAR Mandates. **PROOF:** Quote first AC.
4. CBAR Audit: `docs/architecture/cbar_audits/CBAR_Audit_Phase5_Growth.md` — confirm mandates + corrections.
5. Primitives: `primitives/experience/` — **PROOF:** Quote `id:` + `name:`. **BANNED:** `EXP-TRB-*`.
6. Backend Python Files — **PROOF:** Quote real method signature.
7. Test Files `tests/integration/` (read 2) — Section 10 matches pattern.

**PRE-WORK LOG — all 7 required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 300 LINES

§1 Files Read (≥8) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (≥3 files) | §3.3 Primitives (≥2 YAML IDs) | §3.4 CBAR Mandates (ALL) | §3.5 Technical Decisions | §4 Plan (≥4 phases, ≥12 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (≥1/story + FAILURE EXAMPLE + mandate) | §9 Dependencies | §10 Testing (≥3 unit + ≥2 integration named)

**REJECTION:** Vague AC | No FAILURE EXAMPLE | EXP-TRB-* | Invented signatures | Generic tests | No §3.4 | Pydantic Any | No DEP-IDs | No pre-work log

**Write pre-work log. Then write spec. No permission needed.**
