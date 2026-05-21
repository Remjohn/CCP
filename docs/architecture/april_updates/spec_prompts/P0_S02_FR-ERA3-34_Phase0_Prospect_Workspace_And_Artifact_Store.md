# Spec Prompt: FR-ERA3-34 - Phase-0 Prospect Workspace and Artifact Store

> **READY TO PASTE.** Copy this entire file into a clean session.

---

## SPEC ASSIGNMENT

```
SPEC_ID:         FR-ERA3-34
SPEC_TITLE:      Phase-0 Prospect Workspace and Artifact Store
PHASE:           0 - Trial Phase-0 Commercial Runtime
SOURCE_PRD:      PRD-01, PRD-09
MAPPED_STORIES:  Shared pre-container prospect workspace, artifact lineage and status preservation, 24h max delivery support, no-custom-container-before-continuity discipline
CBAR_MANDATES:   Shared-Workspace-First Rule, No-Full-Container-Before-Payment Rule, Artifact-Lineage Rule, 24h Delivery Readiness Rule, Human-Review Recovery Rule
BACKEND_REL:     NEW shared workspace substrate - MUST reuse existing storage, receipt, packet, and state-management patterns where possible
OUTPUT_FILE:     docs/architecture/april_updates/FR-ERA3-34_Phase0_Prospect_Workspace_And_Artifact_Store_Tech_Spec.md
```

> [!IMPORTANT]
> **SPEC-SPECIFIC CONTEXT:**
> This spec defines the shared Phase-0 workspace and artifact store used before any dedicated coach container exists. It must support one prospect package lifecycle end-to-end:
> - intake artifacts
> - audit artifacts
> - preview artifacts
> - produced proof assets
> - payment handoff artifacts
> - upgrade handoff metadata

> [!IMPORTANT]
> **MANDATORY PHASE-0 SOURCE SET - READ IN EVERY PHASE-0 SPEC SESSION:**
> - `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`
> - `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md`
> - `lab/CCP APRIL Updates/Fladlien_Sales_Insights.md`
> - `lab/ccp_biological_orchestration_model_v_1.md`
> - `lab/CCP APRIL Updates/01_Architecture_PRDs/CCP_System_Documentation.md`

---

## YOUR ROLE

Principal CCP Tech-Spec Architect. Write specifications so precise a senior engineer can implement without one clarifying question. NOT a summarizer. **Write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (cite evidence for all steps before proceeding)

1. Protocol: `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
2. Source PRDs: `PRD-09`, `PRD-01`. **PROOF:** Quote the exact lines that establish Trial Phase-0 and the commercial bridge.
3. Phase-0 source set: all mandatory docs above. **PROOF:** Quote one concrete structural claim from each file.
4. Existing backend references: read real files for storage, artifact state, receipts, lineage, and any workspace provisioning precedent. **PROOF:** Quote real method signatures.
5. Existing models: read artifact / manifest / packet / receipt models.
6. Existing test patterns: read 2 `tests/integration/` files related to storage, state transitions, or receipts.
7. Existing deployment boundaries: confirm which infrastructure currently assumes full coach containerization and where Phase-0 must remain lighter-weight.

**PRE-WORK LOG - required before spec body or STOP.**

---

## FORMAT: 10 SECTIONS, MIN 300 LINES

§1 Files Read (>=8) | §2 Overview | §3.1 DEP-IDs | §3.2 Backend (>=3 files) | §3.3 Packets / artifacts / stores | §3.4 Governance Constraints | §3.5 Technical Decisions | §4 Plan (>=4 phases, >=12 tasks) | §5 Schema (Pydantic v2, no Any) | §6 Fallback | §7 Tasks | §8 AC (with FAILURE EXAMPLE) | §9 Dependencies | §10 Testing

---

## NON-NEGOTIABLE OUTPUT REQUIREMENTS

- Define canonical schemas for:
  - `Phase0WorkspaceRecord`
  - `Phase0ArtifactRecord`
  - `Phase0ArtifactManifest`
  - `Phase0WorkspaceStatus`
  - `Phase0ReadinessState`
  - `Phase0UpgradeBridgeState`
- Define artifact states across:
  - uploaded
  - normalized
  - audit-ready
  - preview-ready
  - delivered
  - payment-unlocked
  - upgraded / handed-off
- Preserve receipt-chain and lineage expectations
- Explicitly define how this workspace remains:
  - shared
  - pre-container
  - bounded
  - safe to delete / migrate later
- Define migration path from Phase-0 workspace to full coach container after continuity conversion

**REJECTION:** vague storage story | no lifecycle state machine | no migration law | assumes full tenancy too early | no artifact lineage | missing failure examples

**Write the pre-work log. Then write the spec. No permission needed.**
