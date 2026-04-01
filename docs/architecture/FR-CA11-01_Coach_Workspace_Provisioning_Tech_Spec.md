# Tech-Spec: FR-CA11-01 — Coach Workspace Provisioning (AFFiNE Sovereign Dashboard)

**Created:** 2026-03-24
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / PRD Update v2.0 — Capability Area 11)
**Architecture Reference:** PRD-Update-CA11 §4.1, ADR-05, Parent PRD §9.8
**Skill Implementation:** `tools/affine_workspace_provisioner.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd-update-CA11-quad-platform.md`
- `d:\Work\The Conscious Coaching Factory\MCDA_AFFiNE_Integration_Analysis.md`

---

## 2. Overview

### Problem Statement
The parent PRD (v1.0) delivers all coach intelligence through Notion via `notion_sync.py` (FR45). Notion is a third-party SaaS that cannot: (1) support custom branding per coach, (2) embed Excalidraw canvases natively, (3) sync real-time with CCP telemetry databases without hitting 3 req/s API rate limits, (4) deliver client-facing workspaces with gated content. The coach workspace is the primary interaction surface — if it feels like a generic tool rather than a sovereign branded environment, coach stickiness collapses.

### Solution
FR-CA11-01 provisions a **fully branded AFFiNE workspace** for each coach during the Genesis Pipeline (Step 2). The workspace is deployed from a version-controlled master template and contains all 8 standard sections that previously existed in the Notion Dashboard (Section 9.8 of parent PRD), now running on a self-hosted AFFiNE instance with zero API rate limits, full theme control, and native CRDT collaboration.

### Scope
**In scope:**
- AFFiNE master workspace template definition (8 sections).
- Workspace provisioning automation (called during Genesis Pipeline).
- Brand theme application per coach (CSS tokens, logo, color palette from `coach_soul.json`).
- Workspace isolation enforcement (ADR-01 compliance).

**Out of scope:**
- Client workspace provisioning (handled by FR-CA11-03).
- Data synchronization (handled by FR-CA11-02).
- AFFiNE deployment/hosting (infrastructure concern, handled by Dockploy).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-003` | Voice DNA (Positive Space) | SOURCE — Brand personality tokens (color palette associations, lexical identity) inform workspace personalization. |
| `DEP-ENG-050` | Business Intelligence Summary | SOURCE — Coach's business name, tagline, and service tiers populate workspace header. |
| Genesis Pipeline (Step 2) | Coach Onboarding | TRIGGER — Workspace provisioning fires after Genesis Clearance Certificate is issued. |
| `affine_sync.py` (FR-CA11-02) | AFFiNE Sync Service | CONSUMER — All downstream sync operations target the workspace created by this FR. |

### Academic Grounding

| Framework | Author | Year | Mechanism |
|---|---|---|---|
| **Never Outshine the Master** | Greene (48 Laws) | 1998 | The coach's workspace must feel like *theirs*, not a tool's output. The brand theme must reflect the coach's visual identity, not the CCP platform's. |
| **Cognitive Ownership Effect** | Pierce et al. | 2003 | Users who perceive digital spaces as "theirs" (through branding, customization, and control) develop stronger psychological attachment and higher retention rates. |

### Technical Decisions
1. **Master Template as Git-Controlled JSON:** The 8-section workspace template is stored as an AFFiNE-compatible JSON export in the AFFiNE fork repository (`ccp-blocks/templates/coach_workspace_master.json`). This ensures version control, rollback capability, and consistency across all coach instances.
2. **CSS Theme Overlay per Coach:** Each coach's brand tokens (primary color, accent color, logo URL, font preference) are extracted from `coach_soul.json` voice DNA aesthetics and `DEP-ENG-050` business summary. These tokens are injected as CSS custom properties into the AFFiNE instance's theme layer at provisioning time, stored per workspace in `coach_theme_{ACRONYM}.css`.
3. **Workspace Isolation via AFFiNE Multi-Workspace:** Each coach gets a separate AFFiNE workspace (not separate pages in a shared workspace). This enforces the ADR-01 single-tenant isolation principle at the workspace level. The AFFiNE Sync Service routes to the correct workspace using the coach's UUID.

---

## 4. Implementation Plan

### Stage 1: Master Template Construction
*Agent:* System Operator (manual, one-time)
*Inputs:* Parent PRD §9.8 Notion Dashboard Schema.
*Outputs:* `coach_workspace_master.json` (AFFiNE export format).
*Failure Condition:* Template does not contain all 8 required sections → provisioneer rejects template during validation.

**Steps:**
1. Construct the AFFiNE workspace template with the following 8 root pages:
   - **Command Center:** Pipeline status indicators (batch_status, v2ws_status). Kanban board with `In Progress`, `Review`, `Published` columns.
   - **Content Calendar:** Database view with columns: Asset ID, Script Preview, Visual Assets, Posting Notes, Voice Note (embed), "Why This Post" rationale, Leadership Farming notes, Fingerprint ID, Status.
   - **Client Intelligence Hub:** Aggregated SPT distribution chart (Excalidraw embed), tribe-level ICT histogram, Intimacy Index averages, anonymized engagement heatmap.
   - **CPSC Campaign Console:** Campaign performance history database, Loom Report archive, client segmentation view by coping position.
   - **CRAL Evidence Vault:** Searchable database of CRAL findings indexed by Moment (M1-M7), coach theme, and usage status.
   - **Guardian Agent Console:** Genesis Clearance Certificate status card, Stewardship Report timeline, Signal Monitoring alerts (Lexicon Drift, Cultural Evolution, Campaign Fatigue).
   - **Visual Production Console:** VPO delivery database with slide previews, AGSS scores, TIAR decay audit, Receipt Chain status, Canva App deep links.
   - **Program Content Library:** Hierarchical content library organized by learning journey, with program tags and client visibility rules metadata.
2. Export the template as JSON and commit to `ccp-blocks/templates/coach_workspace_master.json`.
3. Validate that the template can be imported into a clean AFFiNE instance without errors.

### Stage 2: Theme Token Extraction
*Agent:* `Pierre` (AFFiNE Workspace Orchestrator)
*Inputs:* `coach_soul.json` (DEP-ENG-003), `coach_business_summary.json` (DEP-ENG-050), `coach_config.json`.
*Outputs:* `coach_theme_{ACRONYM}.css`.
*Failure Condition:* Missing brand tokens → fallback to CCP default theme. Coach warned via Telegram.

**Steps:**
1. Extract brand tokens from `coach_soul.json`: primary emotional color (mapped from dominant Mood State affinity → CSS `--ccp-primary`), accent color (from secondary Mood State → `--ccp-accent`).
2. Extract business tokens from `DEP-ENG-050`: business name (→ workspace title), tagline (→ workspace subtitle), logo URL (→ `--ccp-logo-url`).
3. Generate `coach_theme_{ACRONYM}.css` with all CSS custom properties.
4. Deploy theme file to the AFFiNE instance's static assets directory.

### Stage 3: Workspace Provisioning
*Agent:* `Pierre` (AFFiNE Workspace Orchestrator)
*Inputs:* `coach_workspace_master.json`, `coach_theme_{ACRONYM}.css`, `coach_id` (UUID).
*Outputs:* Provisioned AFFiNE workspace with unique `workspace_id`.
*Failure Condition:* AFFiNE API unreachable → provisioning queued for retry. Genesis Pipeline does not halt (workspace is not blocking for initial Voice DNA extraction).
*Receipt Write:* `Receipt_CA11_01.json` → Receipt Chain Guard.

**Steps:**
1. Call AFFiNE workspace creation API with template import.
2. Apply coach theme CSS overlay to the new workspace.
3. Register `workspace_id` in Supabase `coach_config` table (new column: `affine_workspace_id`).
4. Send confirmation to coach via Telegram: "Your workspace is ready. [Link]."
5. Write provisioning receipt to Receipt Chain Guard.

---

## 5. Primary Output Schema

**Data Object:** Coach Workspace Provisioning Payload (`DEP-ENG-071` PROPOSED)

```json
{
  "transaction_timestamp": "2026-03-24T18:00:00Z",
  "coach_id": "uuid-coach-001",
  "coach_acronym": "JP",
  "workspace_id": "affine-ws-uuid-001",
  "workspace_url": "https://os.consciouselite.com/ws/affine-ws-uuid-001",
  "theme_file": "coach_theme_JP.css",
  "template_version": "1.0.0",
  "sections_provisioned": [
    "command_center",
    "content_calendar",
    "client_intelligence_hub",
    "cpsc_campaign_console",
    "cral_evidence_vault",
    "guardian_agent_console",
    "visual_production_console",
    "program_content_library"
  ],
  "receipt_chain_guard": { "schema_ref": "DEP-ENG-041" }
}
```

---

## 6. Backward Compatibility Fallback
During the migration period (Phase 1 parallel operation), both `notion_sync.py` and `affine_sync.py` operate simultaneously. If AFFiNE workspace provisioning fails, the system falls back to the existing Notion dashboard schema (FR45) with a degradation flag logged in Supabase. The coach receives both Notion and AFFiNE delivery until full migration is confirmed.

---

## 7. Tasks

- [ ] **Task 1:** Design and build the 8-section master workspace template in AFFiNE. Export as JSON. Commit to `ccp-blocks/templates/`.
- [ ] **Task 2:** Write `affine_workspace_provisioner.py` with `provision_coach_workspace(coach_id)` function.
- [ ] **Task 3:** Write theme token extraction logic that reads `coach_soul.json` and `DEP-ENG-050` to generate CSS custom properties.
- [ ] **Task 4:** Add `affine_workspace_id` column to Supabase `coach_config` table.
- [ ] **Task 5:** Wire workspace provisioning into Genesis Pipeline (post-Genesis Clearance Certificate).
- [ ] **Task 6:** Build `Pierre` agent persona YAML (AFFiNE Workspace Orchestrator) in the Management Department.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Template Integrity):** Provision a new workspace from the master template. Assert all 8 root sections exist and contain the correct database schemas.
- [ ] **AC2 (Theme Application):** Provision a workspace with a test coach's brand tokens (primary=#2E86AB, accent=#F18F01). Assert the workspace renders with the correct colors in the browser.
- [ ] **AC3 (Isolation Enforcement):** Provision 2 workspaces for Coach A and Coach B. Assert Coach A's workspace URL returns 403 when accessed with Coach B's authentication token.
- [ ] **AC4 (Receipt Chain Integration):** Provision a workspace. Assert `Receipt_CA11_01.json` exists in the Receipt Chain with the correct `workspace_id`.
- [ ] **AC5 (Fallback Graceful Degradation):** Block AFFiNE API. Trigger provisioning. Assert the system falls back to Notion delivery (FR45) and logs a degradation flag.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| AFFiNE self-hosted instance | Infrastructure | Must be deployed via Dockploy before provisioning can execute. |
| Genesis Pipeline (FR-GA) | Internal | Provisioning fires post-Genesis Clearance. |
| `coach_soul.json` (DEP-ENG-003) | Internal | Provides brand personality tokens for theme extraction. |
| `coach_business_summary.json` (DEP-ENG-050) | Internal | Provides business name, tagline, logo for workspace branding. |
| Supabase `coach_config` | Internal | Extended with `affine_workspace_id` column. |

---

## 10. Testing Strategy

### Unit Tests
- **Template Validation:** Load `coach_workspace_master.json`, assert 8 root sections present, assert all database schemas match expected column definitions.
- **Theme Generation:** Pass mock `coach_soul.json` with known color values. Assert generated CSS contains correct `--ccp-primary` and `--ccp-accent` values.

### Integration Tests
- **Full Provisioning Flow:** Execute `provision_coach_workspace("test-coach-001")`. Assert workspace exists in AFFiNE, theme is applied, workspace_id is registered in Supabase, receipt is written.
- **Genesis Pipeline Wire-Up:** Run a full Genesis Pipeline mock. Assert workspace provisioning fires after Genesis Clearance Certificate and before any content delivery.

### Safety Tests (ADR-01 Isolation)
- **Cross-Tenant Access Attempt:** Attempt to access Coach A's AFFiNE workspace API endpoints using Coach B's credentials. Assert 403 Forbidden.
