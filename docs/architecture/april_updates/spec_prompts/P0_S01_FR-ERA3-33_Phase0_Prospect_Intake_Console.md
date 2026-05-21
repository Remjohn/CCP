# Spec Prompt: FR-ERA3-33 - Phase-0 Prospect Intake Console

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-33
SPEC_TITLE:      Phase-0 Prospect Intake Console
PHASE:           0 - Trial Phase-0 Commercial Runtime
SOURCE_PRD:      PRD-01, PRD-04, PRD-09
MAPPED_STORIES:  Trial Phase-0 intake normalization, free-proof-to-paid activation bridge, shared pre-container intake workflow, 12-packages-per-day operator throughput support
CBAR_MANDATES:   Human-First Proof Rule, No-Full-Container-Before-Payment Rule, Shared-Workspace-First Rule, Typed Prospect Packet Rule, 24h Delivery Readiness Rule, Payment-Bridge Readiness Rule
BACKEND_REL:     NEW intake surface - MUST interoperate with existing Telegram/AFFiNE architecture, billing rails, and artifact pipelines without requiring full per-coach container provisioning
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-33_Phase0_Prospect_Intake_Console_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This spec defines the intake console for the Trial Phase-0 runtime. It must gather and normalize the minimum viable prospect context needed to deliver the `$29.99` first-proof package without full custom container setup.
>
> Minimum required input domains:
> - interview / video / voice files
> - transcript
> - voice DNA source inputs
> - voice cloning source inputs
> - 2D avatar image references
> - target audience
> - Guardian-derived business intelligence
> - optional existing content URLs / references
>
> The intake model must also explicitly support these audit target families:
> - single image post + caption
> - multiple images post + caption
> - reel / short video + caption

> [!IMPORTANT]
> **MANDATORY PHASE-0 SOURCE SET - READ IN EVERY PHASE-0 SPEC SESSION:**
> - `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`
> - `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md`
> - `docs/prd/modules/PRD_04_CVE_Experience_Design.md`
> - `lab/CCP APRIL Updates/Fladlien_Sales_Insights.md`
> - `lab/ccp_biological_orchestration_model_v_1.md`
> - `lab/CCP APRIL Updates/01_Architecture_PRDs/CCP_System_Documentation.md`

> [!WARNING]
> **TRACEABILITY NOTE:**
> There is no dedicated Phase-0 epic file yet. For this spec, Step 3 of the normal prompt flow is replaced by the Phase-0 source set above plus the `MAPPED_STORIES` items. In Section 3.4, use `Phase-0 Governance Constraints` if no formal `PhaseX-M#` mandate exists.

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` - §2 backend, §3 Pre-Flight, §4 Format
2. Source PRDs: `PRD-09`, `PRD-01`, `PRD-04`. **PROOF:** Quote the exact lines that establish the `$29.99` bridge, Telegram-native commercial flow, and experience / proof surface requirements.
3. Phase-0 source set: all 6 mandatory docs above. **PROOF:** Quote one concrete structural claim from each file.
4. Existing backend references: read real files for FastAPI app entry, billing/payment integration, upload/asset storage patterns, and Telegram/AFFiNE ingress patterns. **PROOF:** Quote real method signatures.
5. Existing models: read relevant packet / artifact / upload models under `src/ccp/models/`.
6. Existing test patterns: read 2 `tests/integration/` files that cover intake, upload, or API surface patterns.
7. Existing artifact lineage / receipt precedent: confirm how receipts and packet lineage are currently represented and how Phase-0 intake should preserve them.

**PRE-WORK LOG - required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 300 LINES

§1 Files Read (>=8) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=3 files) | §3.3 PRDs / packets / artifacts | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=4 phases, >=12 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define a canonical `Phase0ProspectPacket`
- Define typed intake schemas for:
  - uploaded media sources
  - transcript sources
  - voice DNA source refs
  - voice clone source refs
  - avatar refs
  - target audience profile
  - guardian business-intelligence bundle
  - audit target content type
  - caption / copy attachment
  - missing-input states
- Define operator flow for:
  - create prospect record
  - upload or attach inputs
  - validate readiness
  - handoff to audit / delivery runtime
- Preserve the rule that this is a **shared pre-container workspace**, not full custom coach-container provisioning
- Explicitly state how intake prepares but does not yet require:
  - fine-tuning
  - custom container installation
  - long-lived coach deployment

**REJECTION:** vague upload flow | untyped packet model | assuming full container provisioning | no 24h-readiness state | no payment-bridge awareness | invented method signatures | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
