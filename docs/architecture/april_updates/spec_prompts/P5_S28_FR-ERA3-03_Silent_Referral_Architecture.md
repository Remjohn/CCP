# Spec Prompt: FR-ERA3-03 — Silent Referral Architecture

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-03
SPEC_TITLE:      Silent Referral Architecture
PHASE:           5 — Growth
SOURCE_PRD:      PRD-09
MAPPED_STORIES:  Phase5 Epic1 Stories 1.1 (Shareable Score Object Generation), 1.2 (Vote Then React Escalation)
CBAR_MANDATES:   Phase5-M01 (Verifiable Artifact Rule — User Cards MUST include backend cryptographic hash binding session ID + timestamp + biometric data), Phase5-M02 (Earned Escalation Rule — recording prompt CANNOT appear before Ephemeral Win-State is delivered)
BACKEND_REL:     NEW referral mechanism — CONSUMES conversion_sequence_router.py (FR53) for timing via dormancy gates, READS lead_capture_service.py (FR-CA11-20) cooldown state, CONSUMES offer_tier_governor.py
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-03_Silent_Referral_Architecture_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> M-01 requires cryptographic verification: define the hash algorithm, what data is signed (session_id + timestamp + biometric_hash), and how the receiver's landing page validates the signature. M-02 requires the Ephemeral Win-State to be a mandatory prerequisite state — the recording prompt is gated behind a confirmed win-state delivery event, not just a time delay.

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
