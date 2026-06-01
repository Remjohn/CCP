# Tech-Spec: FR-CA11-02 — AFFiNE Sync Service (DEP-TOOL-060)

**Created:** 2026-03-24
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / PRD Update v2.0 — Capability Area 11)
**Architecture Reference:** PRD-Update-CA11 §4.1, ADR-05
**Skill Implementation:** `tools/affine_sync.py` (FastAPI service)
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md` (FR45 — Notion delivery, §Integration Perimeters)
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd-update-CA11-quad-platform.md`
- `d:\Work\The Conscious Coaching Factory\docs\architecture\FR46_Universal_Asset_ID_Tech_Spec.md`

---

## 2. Overview

### Problem Statement
`notion_sync.py` (FR45) pushes all compiled content to Notion via the Notion API. This API enforces a 3 requests/second rate limit — during a batch delivery of 36 weekly scripts × 5 visual assets each, the sync pipeline takes 60+ seconds and frequently hits rate errors. The Notion API also cannot: push to client-facing workspaces, sync real-time telemetry data, or deliver embedded Excalidraw canvases.

### Solution
FR-CA11-02 implements `affine_sync.py` — a **FastAPI-based webhook-driven sync service** that replaces `notion_sync.py` as the delivery pipeline. The service pushes CCP backend intelligence (compiled scripts, visual assets, telemetry aggregations, session recaps, learning path updates) to the coach's and client's AFFiNE workspaces. Because AFFiNE is self-hosted, there are zero API rate limits. The service maintains an event log in Supabase (`affine_sync_events`) extending the Receipt Chain Guard architecture.

### Scope
**In scope:**
- FastAPI service definition with webhook endpoints.
- Push logic for Content Calendar, Client Intelligence, Visual Assets, Session Archives.
- Idempotent write operations (duplicate pushes do not create duplicates).
- Event logging to Supabase for audit trail.

**Out of scope:**
- AFFiNE workspace provisioning (FR-CA11-01).
- Client workspace content gating logic (FR-CA11-03).
- OBS recording pipeline (FR-CA11-13).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `notion_sync.py` (FR45) | Legacy Delivery Script | SUPERSEDED — `affine_sync.py` replaces all Notion push operations. |
| Receipt Chain Guard (DEP-PROTO-008) | Audit Trail | EXTENDED — Sync events are recorded as receipt chain entries. |
| `DEP-ENG-020` | Fingerprint Archive Index | SOURCE — Every pushed asset carries its Fingerprint ID for traceability. |
| `DEP-ENG-040` | Universal Asset ID System | SOURCE — Every pushed content piece is indexed by its Universal Asset ID. |

### Technical Decisions
1. **FastAPI over simple Python script:** `notion_sync.py` is a procedural script. `affine_sync.py` is a persistent service with: `/push/content` (batch delivery), `/push/telemetry` (CBCS aggregations), `/push/session` (session recaps), `/push/learning-path` (content categorization), `/webhook/canva-approve` (CVE approval trigger). FastAPI provides automatic OpenAPI docs, async support, and structured error handling.
2. **Idempotency via Asset ID:** Every push operation uses the Universal Asset ID (DEP-ENG-040) as the idempotency key. If a push is retried (network failure, timeout), the service checks whether the Asset ID already exists in the target AFFiNE database. If yes, it updates the existing entry rather than creating a duplicate.
3. **Event Sourcing for Audit:** Every sync operation writes an event to `affine_sync_events` with: event_type, target workspace, payload hash (SHA-256), status (success/retry/failed), timestamp, and receipt_chain_id. This extends the Receipt Chain Guard to cover the delivery layer.

---

## 4. Implementation Plan

### Stage 1: FastAPI Service Scaffold
*Agent:* System Operator (initial build)
*Inputs:* Service requirements from PRD-Update-CA11.
*Outputs:* `affine_sync.py` FastAPI application, Dockerfile, docker-compose entry.

**Steps:**
1. Create FastAPI application with the following endpoints:
   - `POST /push/content` — Push compiled CCF/V2WS scripts + visual assets to Content Calendar.
   - `POST /push/telemetry` — Push CBCS aggregations (SPT distribution, ICT, Intimacy averages) to Client Intelligence Hub.
   - `POST /push/session` — Push session intelligence reports to Session Archive.
   - `POST /push/learning-path` — Push categorized content to Program Content Library.
   - `POST /webhook/canva-approve` — Receive CVE Canva App approval events, push VPO to Visual Production Console.
   - `GET /health` — Service health check.
2. Implement AFFiNE block creation/update using AFFiNE's GraphQL API or REST API (depending on self-hosted version).
3. Implement idempotency check: query AFFiNE database for existing entry with matching Asset ID before write.
4. Deploy as a Docker container alongside AFFiNE via Dockploy.

### Stage 2: Content Push Implementation
*Agent:* `Pierre` (AFFiNE Workspace Orchestrator) calls the service.
*Inputs:* `ContentPushPayload` (see schema below).
*Outputs:* AFFiNE database entry in Content Calendar.
*Failure Condition:* AFFiNE API unreachable → event logged as `RETRY`, DamageControl queues for exponential backoff (5s, 10s, 20s, 40s, max 5 retries). After 5 failures → `FAILED` status, System Operator notified.
*Receipt Write:* `affine_sync_events` table entry + Receipt Chain Guard.

**Steps:**
1. Receive payload from CCF pipeline orchestrator (Alex) after Triple-Pass Validation Gate clears.
2. Resolve target workspace ID from `coach_config.affine_workspace_id`.
3. Check idempotency: query Content Calendar for existing Universal Asset ID.
4. If not exists → create new database entry with all fields (script, visual URLs, posting notes, Voice DNA rationale, Leadership Farming notes, Fingerprint ID).
5. If exists → update existing entry (handles retry scenarios).
6. Write event to `affine_sync_events` with payload hash.
7. Write receipt to Receipt Chain Guard.

### Stage 3: Telemetry Push Implementation
*Agent:* Scheduled cron (daily) or triggered by CBCS weekly cycle.
*Inputs:* Aggregated CBCS telemetry from Supabase.
*Outputs:* Updated Client Intelligence Hub in coach's AFFiNE workspace.

**Steps:**
1. Query Supabase for aggregated data: SPT stage distribution, tribe-level ICT breakdown, average Intimacy Index, engagement heatmap data.
2. Push aggregated (anonymized) data to the Client Intelligence Hub database in AFFiNE.
3. Trigger Excalidraw progress chart re-render if data has changed (FR-CA11-09).

---

## 5. Primary Output Schema

**Data Object:** Content Push Payload (`DEP-ENG-072` PROPOSED)

```json
{
  "asset_id": "JP-CCF-20260324-001-CAROUSEL",
  "coach_id": "uuid-coach-001",
  "fingerprint_id": "SKILL-ACH-JP-PROC-PROM-DEV-20260324-001",
  "content": {
    "script_markdown": "## The Mirror Effect\n...",
    "posting_notes": "Best posted Tuesday 9AM. Use hashtags: ...",
    "why_this_post": "Built from your voice note about...",
    "leadership_farming": "This post exercises Authentic Vulnerability (score: 7.2)."
  },
  "visual_assets": [
    {
      "slide_number": 1,
      "image_url": "https://r2.consciouselite.com/JP/assets/slide_001.png",
      "agss_score": 7.8,
      "tiar_nouns": ["inner compass", "sovereign leader"]
    }
  ],
  "voice_note_url": "https://r2.consciouselite.com/JP/audio/trigger_20260324.mp3",
  "receipt_chain_guard": { "schema_ref": "DEP-ENG-041" }
}
```

---

## 6. Backward Compatibility Fallback
During migration: `affine_sync.py` and `notion_sync.py` run in parallel. The CCF pipeline orchestrator (Alex) calls both. Content is delivered to both Notion and AFFiNE. The parallel operation continues until the System Operator explicitly retires `notion_sync.py` after confirming all coaches have migrated. A feature flag `DELIVERY_TARGET` in `coach_config` (values: `BOTH`, `AFFINE_ONLY`, `NOTION_ONLY`) controls routing per coach.

---

## 7. Tasks

- [ ] **Task 1:** Create `affine_sync.py` FastAPI scaffold with all 6 endpoints.
- [ ] **Task 2:** Implement AFFiNE GraphQL/REST API client for database reads/writes.
- [ ] **Task 3:** Create Supabase `affine_sync_events` table (event_id UUID, event_type, target_workspace_id, payload_hash, status, timestamp, receipt_chain_id).
- [ ] **Task 4:** Implement idempotency check using Universal Asset ID lookup.
- [ ] **Task 5:** Implement exponential backoff retry logic (DamageControl integration).
- [ ] **Task 6:** Add `DELIVERY_TARGET` feature flag column to `coach_config` table.
- [ ] **Task 7:** Wire CCF pipeline orchestrator (Alex) to call `affine_sync.py` after Triple-Pass Validation.
- [ ] **Task 8:** Dockerize `affine_sync.py` and add to Dockploy compose stack.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Content Push):** Push a test content payload. Assert the entry appears in the coach's AFFiNE Content Calendar with correct Asset ID, script, visual URLs, and Fingerprint ID.
- [ ] **AC2 (Idempotency):** Push the same payload twice. Assert only one entry exists in AFFiNE (not a duplicate).
- [ ] **AC3 (Event Logging):** Push a payload. Assert `affine_sync_events` table contains an entry with correct `event_type`, `payload_hash` (SHA-256 matches), and `status = success`.
- [ ] **AC4 (Retry Logic):** Block AFFiNE API. Push a payload. Assert 5 retry attempts with exponential backoff. Assert `affine_sync_events` logs `RETRY` entries. Unblock API. Assert payload is delivered on next retry.
- [ ] **AC5 (Dual Delivery):** Set `DELIVERY_TARGET = BOTH`. Push content. Assert entry exists in both Notion and AFFiNE.
- [ ] **AC6 (Receipt Chain):** Push a payload. Assert Receipt Chain Guard contains a valid receipt with the sync event's `receipt_chain_id`.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| AFFiNE self-hosted instance | Infrastructure | Must be running. |
| FR-CA11-01 (Workspace Provisioning) | Internal | Workspace must exist before sync can push to it. |
| FR46 (Universal Asset ID) | Internal | All content pushed is indexed by Asset ID. |
| Receipt Chain Guard (DEP-PROTO-008) | Internal | Extended with sync event receipts. |
| CCF Pipeline Orchestrator (Alex) | Internal | Primary caller of the sync service. |

---

## 10. Testing Strategy

### Unit Tests
- **Payload Validation:** Pass malformed payloads (missing `asset_id`, invalid `coach_id`). Assert `422 Unprocessable Entity` with specific error messages.
- **Hash Computation:** Pass known payload. Assert SHA-256 hash matches expected value.

### Integration Tests
- **End-to-End Content Delivery:** Run a mocked CCF batch. Assert all 36 scripts appear in AFFiNE Content Calendar with correct metadata.
- **Telemetry Push:** Push aggregated CBCS data. Assert Client Intelligence Hub in AFFiNE updates with correct SPT distribution.

### Safety Tests
- **Cross-Tenant Push Rejection:** Attempt to push content for Coach A to Coach B's workspace. Assert the service validates `coach_id` against `workspace_id` ownership and rejects the push with `403 Forbidden`.
