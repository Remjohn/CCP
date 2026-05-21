# Spec Prompt: FR-ERA3-14 — B2B2C Commercial Ladder & Stealth Course

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-14
SPEC_TITLE:      B2B2C Commercial Ladder & Stealth Course
PHASE:           5 — Growth
SOURCE_PRD:      PRD-09
MAPPED_STORIES:  Phase5 Epic3 Story 3.1 (Stealth Course Transition)
CBAR_MANDATES:   Phase5-M05 (1-Tap Paywall Rule — ALL continuity upgrades MUST use native Telegram 1-tap payment infrastructure via Apple Pay/Google Pay; external browser redirect strictly banned)
BACKEND_REL:     NEW service — CONSUMES offer_tier_governor.py for tier eligibility, CONSUMES FR-ERA3-02 (In-Chat Payments) for 1-tap checkout, CONSUMES learning_path_builder.py for Stealth Course unlock progression
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-14_Stealth_Course_Commercial_Ladder_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> The Stealth Course mechanic: advanced FR61 insights are locked behind Tier 1 (.99/mo) as the user hits the Structure Adaptive Layer boundary. M-05 mandates 1-tap payment — the cognitive effort must equal swiping a flashcard. This spec builds on FR-ERA3-02 (Payments) — do not re-specify the payment flow, reference it. Define the Stealth Course unlock state machine and tier gate logic.

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
