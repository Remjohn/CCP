# Tech-Spec: FR49 — Automated Single-Tenant Deployment (DEP-ENG-043)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §System Operator, §ADR-01
**Skill Implementation:** `skills/infrastructure/pi_deployer/`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\prd TO UPDATE.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\Architecture_Synthesis_Report.md`

---

## 2. Overview

### Problem Statement
The Conscious Coaching Platform processes highly sensitive psychological data, proprietary intellectual property (the coach's Core Identity protocols), and clinical-grade conversation histories (via CBCS). If multiple coaches share the same Neo4j Graph Database or Supabase Vector Store, a prompt injection or routing error could accidentally leak Coach A's client suicide-risk transcripts into Coach B's content generation pipeline. Relying on Row-Level Security (RLS) alone across a shared namespace is considered an unacceptable operational risk for high-ticket clients. Furthermore, manually provisioning this infrastructure for every new client takes hours and introduces human error.

### Solution
FR49 establishes the **Automated Single-Tenant Deployment Protocol (DEP-ENG-043)** orchestrated by the Pi Coding Agent (the TypeScript-based meta-orchestrator). When a new coach is onboarded, the Pi agent executes a deterministic Infrastructure-as-Code (IaC) pipeline. It physically spins up a dedicated, mathematically isolated Postgres/Supabase instance, a dedicated Neo4j AuraDB instance, and provisions an isolated S3 storage bucket. Zero data is shared.

### Scope
**In scope:**
- The Pi Coding Agent execution script (`deploy_tenant_stack.ts`).
- Automated provisioning of Supabase projects via the Supabase Management API.
- Automated provisioning of Neo4j AuraDB instances via the Aura API.
- Automated generation and secure storage of the `coach_config` environment variables.

**Out of scope:**
- The actual creation of the Coach's Notion Workspace (handled manually via Template duplication).
- The billing and invoicing of the cloud infrastructure.

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-043` | Pi Deployer Script | OUTPUT — The programmatic Infrastructure-as-Code runner. |
| Supabase Mgmt API | Database Provisioner | DEPENDENCY — Creates the isolated relational & vector storage. |
| Neo4j Aura API | Graph Provisioner | DEPENDENCY — Creates the isolated Context Premise graph. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Architectural Isolation in Multi-Tenant AI** | Sandhu | 2023 | Establishes that logic-based isolation (RLS) fails frequently under complex LLM prompt injection attacks. Physical or namespace-level isolation (Single-Tenant Sandboxing) is the only mathematically provable way to prevent cross-contamination of RAG vectors in highly sensitive clinical/coaching environments. |

### Technical Decisions
1. **Pi Coding Agent (TypeScript) over Bash:** The PRD explicitly mandates moving away from "brittle Python CLI runners" to the TypeScript-based Pi Coding Agent. The management of complex, asynchronous deployment tasks (waiting for a database to provision, pinging for readiness, then running DDL schemas) demands a robust TS framework with async/await and typed API responses.
2. **True Tenant Isolation (ADR-01):** The overarching architecture strictly enforces ADR-01. Thus, the script cannot simply append `coach_name_` to a shared database table. It must issue a `POST /projects` command to Supabase to create an entirely decoupled silo.

---

## 4. Implementation Plan

### Stage 1: The Deployment Trigger & Parameter Registration
*Agent:* Pi Coding Agent (Orchestrator Mode)
*Inputs:* `coach_name`, `coach_acronym`, `admin_email`.
*Outputs:* Deployment Manifest JSON.
*Failure Condition:* Missing parameters prevent API execution.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. The System Operator runs `npx ccp-deploy --coach "Jean Pierre" --acro "JP" --email "x@y.com"`.
2. The Pi agent initializes the session and generates a secure password string for the new databases.
3. Formulates the deployment manifest object mapping the intended cloud regions (e.g., `us-east-1` for lowest latency to inference endpoints).

### Stage 2: Supabase (Relational & Vector) Provisioning
*Agent:* Pi Coding Agent
*Inputs:* Deployment Manifest.
*Outputs:* `Supabase_Project_ID`, `Supabase_Service_Key`.
*Failure Condition:* Supabase Management API times out or rate limits.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Execute `POST https://api.supabase.com/v1/projects` using the CCP Master Management Key.
2. Provide the `coach_name` and generated database password.
3. Enter a polling loop (`GET /v1/projects/{ref}`), pinging every 10 seconds until `status == "ACTIVE"`.
4. Wait for ACTIVE state, then POST the base schema (`schema.sql` containing `users`, `receipt_chain`, `fingerprint_archive`, `semantic_affinity`).
5. Extract the REST URL, Anon Key, and Service Role Key.

### Stage 3: Neo4j Aura DB (Graph) Provisioning
*Agent:* Pi Coding Agent
*Inputs:* Deployment Manifest.
*Outputs:* `Neo4j_URI`, `Neo4j_Username`, `Neo4j_Password`.
*Failure Condition:* Aura API fails to allocate the instance; pipeline must pause and alert operator.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Execute `POST https://api.neo4j.io/v1/instances` to spin up a new AuraDB Free/Basic tier tied to the master CCP account.
2. Receive the connection `URI` and the uniquely generated `password` in the immediate synchronous response.
3. Await instance routing (Neo4j DNS propagation takes ~1-3 minutes). Pi agent pings the bolt protocol until connection is established.
4. Execute the baseline index creations (e.g., `CREATE INDEX FOR (m:Memory) ON (m.id)`).

### Stage 4: Environment Bonding & Handoff
*Agent:* Pi Coding Agent
*Inputs:* All keys from Stage 2 and Stage 3.
*Outputs:* Stored `coach_config` record.
*Failure Condition:* Keys are lost in memory, requiring total instance tear-down.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. The Pi Agent connects to the *Master Management Supabase Instance* (the only centralized database in the CCP, strictly used for routing, totally devoid of client data).
2. It writes a new row to the `tenant_registry` table containing `[coach_acronym, Supabase_URL, Supabase_Key, Neo4j_URI, Neo4j_Key]`.
3. When the Content Orchestrator runs a cycle for "JP" in the future, it looks up "JP" in the `tenant_registry`, unpacks these keys into memory, and connects exclusively to JP's silo.
4. Alerts the System Operator: `DEPLOYMENT COMPLETE: {coach_name} infrastructure isolated and active.`

---

## 5. Primary Output Schema (DEP-ENG-043)

**Schema Name:** `tenant_registry_row.json` (Stored securely in the Master DB)

```json
{
  "tenant_id": "uuid-0011-2233",
  "coach_name": "Jean Pierre",
  "coach_acronym": "JP",
  "deployment_date": "2026-03-13T10:00:00Z",
  "status": "ACTIVE",
  "infrastructure": {
    "supabase": {
      "project_ref": "abcdefghijklmno",
      "rest_url": "https://abcdef.supabase.co",
      "service_role_key": "eyJhbGci..."
    },
    "neo4j": {
      "uri": "neo4j+s://xyz.databases.neo4j.io",
      "username": "neo4j",
      "password_vault_id": "secret_manager_uuid_8899"
    }
  }
}
```

---

## 6. Backward Compatibility Fallback
If the automated IaC pipeline is broken due to external API changes (e.g., Supabase updates their v1 Management API), the Pi Coding Agent exits gracefully and outputs a manual playbook (`.txt` file). This playbook contains the exact SQL payload and Neo4j Cypher commands required. The System Operator can manually log into the web portals, click "Create Project", and run the payloads to achieve the exact same architectural result without being blocked by automation failure.

---

## 7. Tasks

- [ ] **Task 1:** Provision the CCP Master Management Key for Supabase and the Neo4j Aura API credentials. Store these securely in the Pi Agent's root `.env` file.
- [ ] **Task 2:** Write the `deploy_tenant_stack.ts` Pi Agent script logic for Stage 2 (Supabase POST creation and DB polling).
- [ ] **Task 3:** Write the TypeScript logic for Stage 3 (Neo4j Aura instance creation and schema initialization).
- [ ] **Task 4:** Write the Stage 4 binding logic that securely inserts the generated keys into the Master `tenant_registry` table.
- [ ] **Task 5:** Build the SQL initialization block (`schema.sql`) containing the table declarations for `users`, `receipt_chain`, `fingerprint_archive`, and `content_performance`. The Pi Agent must execute this against the newly created Supabase instance before declaring it ACTIVE.

---

## 8. Acceptance Criteria

- [ ] **AC1 (End-to-End Orchestration):** Run the CLI command `npx ccp-deploy --coach "Test" --acro "TST"`. Assert that within 5 minutes, a new Supabase project and Neo4j instance physically exist in the respective web dashboards, and the master `tenant_registry` holds the correct connection strings. *Failure Example:* The script hangs infinitely waiting for Neo4j DNS.
- [ ] **AC2 (Namespace Decoupling Check):** Extract the Supabase Service Key generated for "TST". Use it to attempt to query the `receipt_chain` table for "JP". Assert the API rejects the request entirely (or returns a 404/Empty set), proving strict physical isolation. *Failure Example:* The "TST" key successfully accesses "JP"'s data, violating ADR-01.
- [ ] **AC3 (Schema Injection):** Following a successful deployment, use the newly generated Supabase key to query `SELECT * FROM fingerprint_archive LIMIT 1;`. Assert the query executes cleanly (returning 0 rows), proving the tables were successfully initialized. *Failure Example:* The query returns `relation "fingerprint_archive" does not exist` because the IaC script failed to run the setup DDL.
- [ ] **AC4 (Idempotency Guard):** Run the deploy command for `acro "JP"` twice. Assert the script detects the existing `JP` registry entry and aborts with a `TENANT_EXISTS` error rather than overwriting the production keys or spinning up duplicate, unlinked databases. *Failure Example:* The system spins up a second database, stranding the old data.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| Supabase Management API | External | Must be enabled on the primary workspace in the Supabase Dashboard. |
| Neo4j Aura API | External | Requires an Enterprise or Professional tier account to spawn programmatic instances. |
| Master Registry DB | Internal | The sole centralized database acting as the `switchboard` for the 11 Pi Extensions. |

---

## 10. Testing Strategy

### Unit Tests
- **Manifest Generator Guard:** Run the deploy init function without providing `--acro`. Assert the Pi Agent immediately throws a validation error demanding the 2-4 character string.

### Integration Tests
- **Dry-Run Mode:** Execute the script with a `--dry-run` flag. Assert that the script successfully authenticates against the Supabase and Neo4j APIs, prints the API requests it *would* make, but does not actually create any infrastructure.

### Safety Tests (ADR-01 Quarantine Security)
- **Credential Storage Audit:** Extract the `tenant_registry_row.json` payload. Assert that the `service_role_key` and Neo4j passwords are not printed to standard console output at any point during execution, and are only transmitted over TLS directly to the master database.
