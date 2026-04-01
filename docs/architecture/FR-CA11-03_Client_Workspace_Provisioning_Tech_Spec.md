# Tech-Spec: FR-CA11-03 — Client Workspace Provisioning (Gated Learning Environment)

**Created:** 2026-03-24
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / PRD Update v2.0 — Capability Area 11)
**Architecture Reference:** PRD-Update-CA11 §4.1, ADR-05, Parent PRD ADR-01
**Skill Implementation:** `tools/affine_client_workspace.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md` (FR27-FR32, CBCS onboarding)
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd-update-CA11-quad-platform.md`
- `d:\Work\The Conscious Coaching Factory\MCDA_14_AFFiNE_Power_Integrations.md`

---

## 2. Overview

### Problem Statement
The parent PRD delivers coaching intelligence to clients exclusively via Telegram (CBCS). Clients have no persistent workspace — no course library, no progress dashboard, no journal archive, no visual milestone tracking. When a coach sells a program, the "content delivery" is scattered across Telegram messages, Google Drive links, and manual email attachments. There is no branded, structured environment where a client can access their entire coaching journey in one place.

### Solution
FR-CA11-03 provisions a **client-facing AFFiNE workspace** for each CBCS member, automatically created upon Telegram bot onboarding (FR27). The workspace is program-specific (template varies by coaching program), content-gated (visibility controlled by program tags and client progression level), and branded with the coach's theme (not a generic CCP look).

### Scope
**In scope:**
- Client workspace template construction (per coaching program).
- Automatic provisioning triggered by CBCS Telegram onboarding.
- Content gating logic (query `coping_trajectory` + `atlas_roadmap` for visibility rules).
- Read-only enforcement on CCP-managed content sections; read-write on personal sections.

**Out of scope:**
- Content categorization into learning paths (FR-CA11-04).
- Session recap delivery (FR-CA11-05).
- Visual progress chart generation (FR-CA11-09).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| CBCS Onboarding (FR27) | Telegram Client Registration | TRIGGER — Client workspace provisioned upon successful CBCS onboarding. |
| `coping_trajectory` (Supabase) | Information Coping Trajectory | SOURCE — Coping position determines content unlock gates. |
| `atlas_roadmap` (Supabase) | 4-Week Ritual Roadmap | SOURCE — Week/phase position determines time-based content access. |
| `Noémie` (Content Gating Agent) | Content Visibility Controller | AGENT — Evaluates gating rules and provisions unlocked content blocks. |

### Academic Grounding

| Framework | Author | Year | Mechanism |
|---|---|---|---|
| **Self-Determination Theory** | Deci & Ryan | 2000 | Client autonomy (having "their own" workspace) + competence (seeing progress) + relatedness (feeling connected to the coach's environment) drive intrinsic motivation. |
| **Zone of Proximal Development** | Vygotsky | 1978 | Gating content by progression level ensures clients access material at the edge of their current capability — not too easy (boredom), not too advanced (overwhelm). |

### Technical Decisions
1. **Gating by Absence, Not Hiding:** Content blocks that are not yet unlocked do not exist in the client's workspace. They are provisioned by the Sync Service when the client reaches the gating threshold. This prevents URL manipulation, DOM inspection, or any other bypass vector.
2. **Program-Specific Templates:** Each coaching program (e.g., "90-Day Body Transformation", "Leadership Mastery") gets its own client workspace template with different sections, content structure, and gating rules. Templates are stored in `ccp-blocks/templates/client_{program_id}.json`.
3. **Coach Theme Inheritance:** Client workspaces inherit the coach's CSS theme (from FR-CA11-01) — the client sees the *coach's* brand, not the CCP platform brand. This strengthens the parasocial bond (FR-CBCS-11).

---

## 4. Implementation Plan

### Stage 1: Client Template Construction
*Agent:* System Operator + Coach (collaborative, per-program)
*Inputs:* Coach's program structure, content inventory.
*Outputs:* `client_{program_id}.json` AFFiNE workspace template.

**Steps:**
1. For each coaching program, construct a template with 4 root sections:
   - **My Dashboard:** Current Capacity Track, streak data, next scheduled ritual, Intimacy Index (hidden numeric, shown as "Connection Level" progress bar).
   - **Learning Library:** Program-tagged content organized by module/week. Each content block has metadata: `program_tag`, `unlock_condition` (coping_position + atlas_week), `content_type`.
   - **My Journal:** Client's personal journal entries synced from CBCS Telegram interactions. Read-write. Chronological.
   - **Resources:** Lead magnets, worksheets, Excalidraw diagrams, downloadable assets. Read-only for CCP-managed content.
2. Export template as JSON and commit to `ccp-blocks/templates/client_{program_id}.json`.

### Stage 2: Provisioning Engine
*Agent:* `Pierre` (AFFiNE Workspace Orchestrator)
*Inputs:* `client_id` (from Telegram onboarding), `coach_id`, `program_id`.
*Outputs:* Client workspace with `client_workspace_id` registered in Supabase `cbcs_clients` table.
*Failure Condition:* AFFiNE unreachable → workspace creation queued. Client continues on Telegram-only (existing behavior). No functionality loss — workspace is additive.
*Receipt Write:* `Receipt_CA11_03.json` → Receipt Chain Guard.

**Steps:**
1. CBCS onboarding completes (FR27) → Vidye fires provisioning event.
2. `Pierre` selects the correct program template based on `program_id`.
3. Create AFFiNE workspace from template.
4. Apply coach's CSS theme (inherited from FR-CA11-01).
5. Execute initial content gating: query `coping_trajectory` and `atlas_roadmap` for the client. Provision only content blocks whose `unlock_condition` is met.
6. Register `client_workspace_id` in `cbcs_clients` table.
7. Send Telegram message to client: "Your personal coaching space is ready! [Link]."

### Stage 3: Content Gating Engine
*Agent:* `Noémie` (Content Gating Agent)
*Inputs:* Client's `coping_trajectory` update event, `atlas_roadmap` progression event.
*Outputs:* Newly provisioned content blocks in client workspace.
*Failure Condition:* Gating logic error → content remains locked. Fail-safe: never unlock prematurely; log error, alert operator.

**Steps:**
1. Subscribe to Supabase change events on `coping_trajectory` and `atlas_roadmap` tables (filtered by `client_id`).
2. When a change is detected: query all content blocks in the program template whose `unlock_condition` is now met but not yet provisioned.
3. For each newly eligible block: call AFFiNE API to create the block in the client's workspace.
4. Send Telegram notification: "New content unlocked in your coaching space! 🎉"
5. Log unlock event to `affine_sync_events`.

---

## 5. Primary Output Schema

**Data Object:** Client Workspace Provisioning Payload (`DEP-ENG-073` PROPOSED)

```json
{
  "client_id": "uuid-client-042",
  "coach_id": "uuid-coach-001",
  "program_id": "90day-body-transformation",
  "workspace_id": "affine-ws-client-042",
  "workspace_url": "https://os.consciouselite.com/ws/affine-ws-client-042",
  "theme_inherited_from": "coach_theme_JP.css",
  "sections_provisioned": ["dashboard", "journal", "resources"],
  "learning_library_blocks_unlocked": 3,
  "learning_library_blocks_total": 24,
  "gating_snapshot": {
    "coping_position": 2,
    "atlas_week": 1,
    "capacity_track": "Foundation"
  },
  "receipt_chain_guard": { "schema_ref": "DEP-ENG-041" }
}
```

---

## 6. Backward Compatibility Fallback
Client workspace is entirely additive — it does not replace Telegram CBCS delivery. If AFFiNE workspace provisioning fails, the client continues receiving all rituals, prompts, and coaching interactions via Telegram as before. The workspace is a value-add layer, not a replacement for the real-time coaching loop.

---

## 7. Tasks

- [ ] **Task 1:** Design client workspace template for a reference coaching program. Export as JSON.
- [ ] **Task 2:** Write `affine_client_workspace.py` with `provision_client_workspace(client_id, coach_id, program_id)` function.
- [ ] **Task 3:** Implement content gating engine in `Noémie` agent: Supabase event subscription + unlock logic.
- [ ] **Task 4:** Add `client_workspace_id` column to Supabase `cbcs_clients` table.
- [ ] **Task 5:** Wire CBCS onboarding (Vidye) to trigger `Pierre` for client workspace provisioning.
- [ ] **Task 6:** Build `Noémie` agent persona YAML (Content Gating Agent) in the Strategy Department.
- [ ] **Task 7:** Implement Telegram notification for workspace creation and content unlocks.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Provisioning on Onboarding):** Onboard a test client via CBCS Telegram bot. Assert an AFFiNE workspace is created with the correct program template and coach theme applied.
- [ ] **AC2 (Content Gating):** Provision a client at coping position 1, atlas week 1. Assert only Week 1 content blocks exist in Learning Library (not hidden — absent).
- [ ] **AC3 (Progressive Unlock):** Update the test client's coping position to 3. Assert new content blocks are provisioned in the Learning Library within 60 seconds.
- [ ] **AC4 (Read-Only Enforcement):** Attempt to edit a CCP-managed content block via AFFiNE API using client credentials. Assert the write is rejected.
- [ ] **AC5 (Cross-Client Isolation):** Client A attempts to access Client B's workspace URL. Assert 403 Forbidden.
- [ ] **AC6 (Telegram-Only Fallback):** Block AFFiNE API. Onboard a client. Assert CBCS operates normally via Telegram with no errors. Assert workspace creation is queued for retry.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR-CA11-01 (Coach Workspace) | Internal | Coach workspace must exist (client inherits theme). |
| FR27 (CBCS Telegram Onboarding) | Internal | Triggers client workspace provisioning. |
| FR-CBCS-04 (ICT Mapper) | Internal | `coping_trajectory` table provides content gating data. |
| FR32 (Atlas Roadmap) | Internal | `atlas_roadmap` table provides progression gating data. |
| Supabase change subscriptions | Infrastructure | Required for real-time gating trigger. |

---

## 10. Testing Strategy

### Unit Tests
- **Gating Logic:** Mock `coping_trajectory = 2`, `atlas_week = 3`. Assert exactly the correct content blocks are marked as "unlockable" for a reference program template with known gating rules.

### Integration Tests
- **Full Lifecycle:** Onboard client → provision workspace → update coping position → assert unlock → update atlas week → assert unlock. Validate each step produces correct AFFiNE state and Supabase logs.

### Safety Tests
- **Premature Unlock Prevention:** Attempt to directly call the unlock API with a coping_position the client hasn't achieved. Assert the unlock is rejected and the incident is logged.
