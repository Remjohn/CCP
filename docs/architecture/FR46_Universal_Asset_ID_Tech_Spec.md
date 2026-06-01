# Tech-Spec: FR46 — Universal Asset & Person ID System (DEP-ENG-040)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §10, CCP_Technical_Architecture.md §10.4-10.5
**Skill Implementation:** `skills/utils/id_generator.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\prd TO UPDATE.md`
- `d:\Work\The Conscious Coaching Factory\docs\architecture\CCP_Technical_Architecture.md`

---

## 2. Overview

### Problem Statement
An AI ecosystem consisting of 65 distinct agents across multiple pipelines (CCF, CBCS, V2WS) generates thousands of intermediate variables, script drafts, visual files, and performance logs. If an asset is named `final_script_v2.md` and stored in Supabase, and a performance report in Notion references "The Sunday Burnout Post," there is zero programmatic traceability. When the Data Analyst Agent attempts to map engagement back to the original psychological premise, the chain is broken. Similarly, if a client interacts on Telegram as `@user123` but is logged in Notion as "John Doe," the memory graphs collapse.

### Solution
FR46 establishes the **Universal Asset & Person ID System (DEP-ENG-040)**. It enforces a strict, deterministic, human-readable identifier for *every* artifact and *every* human in the CCP. All storage layers (Notion, Supabase, Neo4j, Receipt Chain, Amazon S3) must index data using these keys.

### Scope
**In scope:**
- Generation logic for the Universal Asset ID (`{COACH_ACRONYM}-{PIPELINE}-{DATE}-{SEQUENCE}-{FORMAT}`).
- Generation logic for the Person ID (`PID-{COACH_ACRONYM}-{SEQUENCE}`).
- The Supabase Sequence Registry maintaining the incremental counters.

**Out of scope:**
- The actual creation of Notion pages (handled by FR45).
- The actual storage of the files in S3 (handled by the respective compilation pipelines).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-040` | ID Generation Utility | TOOL — Called by the Orchestrator at the exact moment of asset genesis or client onboarding. |
| Supabase `id_sequences` | The Counter Registry | DEPENDENCY — Ensures the `{SEQUENCE}` integers never duplicate, even across parallel agent threads. |
| The Receipt Chain Guard | Transaction Log | DEPENDENCY — Every receipt in the chain binds to the Asset ID. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Data Provenance in Distributed Systems** | Halpern | 2003 | Establishes that mathematical certainty in distributed systems requires immutable lineage keys assigned at the point of origin. Without origin keys, downstream agents cannot deterministically prove what data they are evaluating. |

### Technical Decisions
1. **Human Readable over UUIDv4:** While UUIDv4 (`123e4567-e89b-12d3...`) is perfect for primary database keys, coaches need to interact with the Notion dashboard. An ID like `JP-CCF-20260312-001-CAROUSEL` allows a human to instantly understand the tenant, pipeline, date, and format without running a database query. Both are used (UUIDs for foreign keys, Universal IDs for semantic tracking).
2. **Centralized Sequence Atomicity:** Because 11 Pi Extensions might be running multiple parallel team agents, querying a local `.txt` file for the "next sequence number" will cause race conditions and ID collisions. The sequence counter *must* be an atomic transaction in Supabase.

---

## 4. Implementation Plan

### Stage 1: Person ID (PID) Generation
*Agent:* Genesis Orchestrator / Vidye (CBCS)
*Inputs:* `coach_acronym`, `is_coach` (boolean).
*Outputs:* `Person_ID` string.
*Failure Condition:* Supabase transaction fails, halting client onboarding to prevent untracked interaction data.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Determine trigger context: 
   - If Genesis Phase (onboarding the Coach): `SEQUENCE = 0000`. 
   - If CBCS (onboarding a new Telegram Client): Query Supabase `id_sequences` table for the Coach's current `client_count`.
2. Execute an atomic `INCREMENT` on the `client_count`.
3. Format output: `PID-{COACH_ACRONYM}-{SEQUENCE}` (e.g., `PID-JP-042`).
4. Write the PID to the `users` table and return it to the calling agent.

### Stage 2: Universal Asset ID Generation
*Agent:* Morgan/Alex (Pipeline Orchestrators)
*Inputs:* `coach_acronym`, `pipeline_type`, `format_tag`.
*Outputs:* `Asset_ID` string.
*Failure Condition:* Orchestrator fails to generate ID before the Research Planner begins Phase 1, breaking the entire Receipt Chain tracking link.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. The Orchestrator calls `id_generator.py` at the very beginning of a compilation cycle (e.g., when a script draft is initialized).
2. **Resolution Rules for Input Variables:**
   - `{COACH_ACRONYM}`: Sourced from `coach_config` (e.g., `JP` for Jean Pierre).
   - `{PIPELINE}`: Enum `[CCF, CBCS, V2WS, TIER]`. Sourced from the Orchestrator's active session state.
   - `{DATE}`: `YYYYMMDD` of the current UTC server time.
   - `{FORMAT}`: Enum `[CAROUSEL, REEL, SCRIPT, DECK, RITUAL, AUDIO]`. Sourced from the initial content strategy directive.
3. Query Supabase `id_sequences` for the specific combination of `{COACH_ACRONYM}` + `{DATE}`. Execute an atomic `INCREMENT` for the daily output counter.
4. Format output: `{COACH_ACRONYM}-{PIPELINE}-{DATE}-{SEQUENCE}-{FORMAT}` (e.g., `JP-CCF-20260312-001-CAROUSEL`).
5. Provide this ID to the memory layer as the anchor for the session.

### Stage 3: Enforcement & Propagation
*Agent:* `TillDone` Pi Extension / All Output Agents
*Inputs:* `Asset_ID` or `Person_ID`.
*Outputs:* Validated Data Payloads.
*Failure Condition:* An agent attempts to write a file or an entry without utilizing the generated ID, triggering an immediate `DamageControl` quarantine.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. The `TillDone` checklist compiler physically verifies the ID prefix.
2. If `notion_sync.py` executes (FR45), it writes the Asset ID into the Notion Page Properties.
3. If the Data Analyst Evaluates performance (FR43), it joins performance data using the Asset ID.

---

## 5. Primary Output Schema (DEP-ENG-040)

**Schema Name:** `id_generation_payload.json`

```json
{
  "transaction_timestamp": "2026-03-13T08:50:00Z",
  "coach_id": "uuid-0099-8877",
  "assigned_person_id": "PID-JP-042",
  "assigned_asset_id": "JP-CCF-20260313-001-CAROUSEL",
  "id_metadata": {
    "pipeline": "CCF",
    "format": "CAROUSEL",
    "daily_sequence": "001"
  }
}
```

---

## 6. Backward Compatibility Fallback
If the central Supabase `id_sequences` table fails to respond (preventing atomic incrementation), the `id_generator.py` script automatically falls back to generating a pseudo-sequence using the last 4 digits of the current UNIX timestamp integer. E.g., `JP-CCF-20260312-8492-CAROUSEL`. This temporarily breaks the clean `001, 002, 003` aesthetic but guarantees mathematically that asset generation is not paralyzed by a database timeout, maintaining full tracker functionality. 

---

## 7. Tasks

- [ ] **Task 1:** Create the Supabase `id_sequences` table to track independent `client_count` per coach, and `daily_asset_count` per coach/date. Must use Postgres atomic increments.
- [ ] **Task 2:** Write `id_generator.py` to handle the `generate_person_id(coach_id)` function.
- [ ] **Task 3:** Write `id_generator.py` to handle the `generate_asset_id(coach_id, pipeline, format)` function.
- [ ] **Task 4:** Refactor the Orchestrator kickoff sequence (in all pipelines: CCF, V2WS, CBCS) to instantly call `id_generator.py` and mount the returned value to the global session state object.
- [ ] **Task 5:** Refactor `notion_sync.py` (FR45) to ensure it pulls this ID from the session state and injects it into the Notion API property block.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Atomic Incrementation):** Execute 5 parallel requests to `generate_asset_id` for the same Coach and Date exactly simultaneously. Assert the sequence returns `001, 002, 003, 004, 005` with zero collisions. *Failure Example:* Two parallel agents receive `JP-CCF-20260312-001-CAROUSEL`, causing an overwrite in the storage bucket.
- [ ] **AC2 (Format Enum Guard):** Attempt to generate an Asset ID with the format string `RANDOM_STRING`. Assert the system rejects the call, throws a `ValueError`, and demands a valid enum. *Failure Example:* The ID generates as `JP-CCF-20260312-001-RANDOM_STRING`, breaking downstream regex parsers.
- [ ] **AC3 (Coach Zero Assignment):** Trigger genesis onboarding. Assert the coach is assigned `PID-{ACRONYM}-0000`. Trigger a new client. Assert the client is assigned `PID-{ACRONYM}-0001`. *Failure Example:* The coach is assigned `001` or a standard UUID, causing clinical graph queries to fail to identify the master tenant.
- [ ] **AC4 (Fallback Extrication):** Manually block outgoing network access to Supabase. Request an Asset ID. Assert the system gracefully returns a UNIX timestamp based fallback sequence (e.g. `8492`) instead of crashing the pipeline. *Failure Example:* The orchestrator throws an unhandled `ConnectionTimeout` and drops the compiled asset.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| Supabase `id_sequences` | Internal | Required for atomic transaction locks to prevent sequence collisions. |
| Pipeline Orchestrators | Internal | The actors relying on this script to mint the IDs before they do any actual work. |

---

## 10. Testing Strategy

### Unit Tests
- **Format String Verification:** Pass valid arguments `('JP', 'CBCS', 'RITUAL')`. Assert the generator perfectly outputs `JP-CBCS-[TODAY]-001-RITUAL`. Test the padding logic ensuring `1` becomes `001`.

### Integration Tests
- **The Lifecycle Trace:**
  1. Mint a new Asset ID.
  2. Pass it through a mocked compilation pipeline.
  3. Validate that the mocked `Receipt Chain` logs reference the exact Asset ID.
  4. Validate that the Notion Sync payload output includes the exact Asset ID.
  
### Safety Tests (ADR-01 Quarantine Security)
- **Tenant Prefix Violation:** Modify the session state of Coach A to request an ID on behalf of Coach B. Assert that the underlying `id_generator.py` validates the request key against the `coach_config` context, rejecting the spoof and maintaining physical tenant tracking isolation.
