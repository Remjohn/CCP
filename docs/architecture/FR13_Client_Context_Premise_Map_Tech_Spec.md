# Tech-Spec: FR13 — Client Context Premise Map (Neo4j) & ADR-01 Coach Data Isolation

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v3.1)
**Architecture Reference:** PRD §ADR-01, Context_Premise_Trigger_Matching_Layer, CCP_Technical_Architecture §1.4
**Skill Implementation:** `skills/ccf/memory/client-context-premise-graph/SKILL.md`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md` (Specifically Neo4j graph storage constraints and Aria entity extraction thresholds).
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\Context_Premise_Trigger_Matching_Layer.md`
- `d:\Work\The Conscious Coaching Factory\docs\architecture\CCP_Technical_Architecture.md` (Architectural principles, single-tenant mandates).
- `d:\Work\The Conscious Coaching Factory\lab\Notebook LM\Webinar\Architecting Deep Reasoning AI Coaches.md` (HGM - Hypergraph Based Memory / Phoenix Loop).

---

## 2. Overview

### Problem Statement
In traditional 1-on-1 coaching automation, client data is treated as flat conversational memory (e.g., standard RAG vector stores). When a client mentions a "fear of failure" and a "boss who micro-manages," vector search treats these as co-occurring keywords, not structurally dependent life vectors. Flat memory obscures the *Context Premise* — the 12-dimensional psychological map of a specific human's internal worldview. 

Furthermore, because this data constitutes highly sensitive psycho-emotional vulnerability mapping, co-mingling client data from multiple coaches in a multi-tenant database presents a catastrophic security and liability risk. A breach or a misconfigured RAG prompt in Coach A's environment could hallucinate or leak the trauma data of Coach B's client.

### Solution
FR13 mandates the creation of the **Client Context Premise Map** powered by a Neo4j Hypergraph Memory (HGM). Rather than summarizing text, the system utilizes the Aria agent to extract visceral L3 language and plot it across 12 dimensions (Fears, Enemies, Dreams, Hidden Beliefs) continuously connecting nodes via semantic edges (`FIGHTS_AGAINST`, `FEARS`, `HAS_IDENTITY`).

To categorically prevent cross-coach contamination, this architecture enforces **ADR-01 (Coach Data Isolation)** mathematically. Each coach is provisioned a strictly isolated, single-tenant cloud deployment. Context premises are siloed. If a coach exits the CCP, the entire hypergraph, including the `coach_soul.json` Voice DNA payload, undergoes a cryptographic sequence purge (The Right-to-be-Forgotten Protocol).

FR13 produces DEP-ENG-030 — the 1:1 Client Context Premise Map built from private single-tenant telemetry. This is architecturally distinct from DEP-ENG-006 (macro audience Context Premise Map produced by FR9 and consumed by FR10). These are separate data objects serving separate pipeline functions. DEP-ENG-030 must never be referenced in place of DEP-ENG-006 or vice versa.

### Scope
**In scope:**
- Stage 1: 12-Dimensional Context Premise Extraction (Aria Agent).
- Stage 2: Neo4j Node and Edge Translation (Atlas Agent).
- Stage 3: Neo4j Hypergraph Commit transaction strictly bound by ADR-01 tenant credentials.
- Stage 4: Trigger-driven "Right-to-be-Forgotten" purge protocol.
- Auditable Receipt Chain Guard logging at every data movement stage.

**Out of scope:**
- The upstream Telegram ingestion of the user's initial messages.
- The downstream formulation of content based on these Neo4j relationships.

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-019` | Session Transcript Intelligence | INPUT — Raw client conversational data (transcripts, journal entries) |
| `DEP-ENG-003` | Positive Space (Voice DNA) | INPUT — Required to define the coach's local instance parameters |
| [PROPOSED] `DEP-ENG-028` | Client Context Extraction Payload | INTERMEDIATE — The 12-dimensional JSON array parsed by Aria |
| [PROPOSED] `DEP-ENG-029` | Cypher Transaction Manifest | INTERMEDIATE — The strict sequence of Neo4j mutation commands |
| `DEP-ENG-030` | Client Context Premise Map (1:1) | OUTPUT — Single-tenant Neo4j graph built from private client telemetry. Distinct from DEP-ENG-006. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Hypergraph Based Memory (HGM)** | *Multiple* | 2024 | Moving beyond standard A->B binary graphs. HGM constructs "Hyper-edges", encapsulating the user, the emotional state, the specific coping mechanism, and the time-of-day within a single structural room. Permits multi-hop contextual reasoning over trauma chains. |
| **Self-Memory System (AKB)** | Conway | 2005 | Graph nodes must heavily weight visceral, Event-Specific Knowledge (ESK) exact phrasing over Semantic Summaries. An LLM generalizing a quote damages the emotional recall anchor. |

### Technical Decisions
1. **Neo4j Hyper-edges over Standard Triples:** Representing a client's worldview requires linking `(Client)-[:EXPERIENCES]->(Fear)` within the context of `[:DURING_COPING_PHASE]`. Hyper-edges capture stateful multidimensionality rather than flat relational truths.
2. **Hard Siloed Credentials (ADR-01):** Connecting to Neo4j requires the environment variables `NEO4J_URI` and `NEO4J_PASSWORD` to be uniquely generated per coach onboarding. A master database with namespace partitioning is explicitly forbidden. Separate databases per tenant.
3. **No LLM Summary on L3 Nodes:** When Aria extracts an "Enemy" node, the `description` attribute must map to the exact substring the user provided, enclosed in quotes. Abstracting it to a generic psychological term destroys the sub-cortical "2am test" integrity.

---

## 4. Implementation Plan

### Stage 1: 12-Dimensional Extraction
*Agent Name:* Aria (The Synthesizer)
*Inputs:* `DEP-ENG-019` (Session Transcript), `DEP-ENG-003` (Voice DNA for context weighting).
*Outputs:* `[PROPOSED] DEP-ENG-028` (Client Context Extraction Payload).
*Failure Condition:* Extraction payload contains fewer than 2 valid entities, or PII redaction mechanism fails.

**Steps:**
1. Ingest flat conversational string from `DEP-ENG-019`.
2. Apply PII redaction gate. Exclude proper nouns not tied to canonical entities.
3. Extract entities across 12 dimensions: Enemy, Dream, Fear, Identity, Coach Reference, Ritual Affinity, Capacity Score, TTT State, Identity Pillar, Emotional Trigger, Resistance Pattern, Milestone Proximity.
4. Verify exact substring capture (No summaries for L3 emotional nodes).
5. Output `DEP-ENG-028` intermediate JSON payload.
6. Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'STAGE-1-EXTRACTION',
  agent_name: 'Aria',
  timestamp }

### Stage 2: Cypher Graph Mapping
*Agent Name:* Atlas (The Architect)
*Inputs:* `DEP-ENG-028` (Client Context Extraction).
*Outputs:* `[PROPOSED] DEP-ENG-029` (Cypher Transaction Manifest).
*Failure Condition:* An extracted node lacks a valid relationship edge, resulting in an orphaned node.

**Steps:**
1. Parse the 12-dimensional array.
2. Translate JSON structures into strict `MERGE` and `MATCH` Cypher queries to prevent duplicate nodes.
3. Construct Hyper-edges mapping entities logically (e.g., `(User)-[:FIGHTS_AGAINST {intensity: 'high'}]->(Enemy)`).
4. Assert valid topology (no syntax errors, no orphaned nodes).
5. Output `DEP-ENG-029` transaction list.
6. Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'STAGE-2-CYPHER-MAPPING',
  agent_name: 'Atlas',
  timestamp }

### Stage 3: Neo4j Hypergraph Commit (ADR-01 Guarded)
*Agent Name:* Graph-Commit-Orchestrator
*Inputs:* `DEP-ENG-029` (Cypher Transaction Manifest).
*Outputs:* Mutated `DEP-ENG-030` (Neo4j Database).
*Failure Condition:* Database connection refuses `NEO4J_URI` credential, or transaction rollback occurs due to race condition.

**Gate Logic & ADR-01 Compliance:**
1. Load Coach's isolated `NEO4J_URI` and `NEO4J_PASSWORD` from local tenant vault.
2. Open Bolt Protocol connection.
3. Initiate Transaction block. Execute `DEP-ENG-029` queries sequentially.
4. **Gate Threshold:** `transaction.commit()` must return SUCCESS status code.
5. **Verdict: PASS:** Transaction succeeds. Data isolated to single-tenant instance. Proceed to Receipt writing.
6. **Verdict: PROVISIONAL:** Database locked (concurrent write). Downstream: Implement exponential backoff, retry 3 times max.
7. **Verdict: FAIL:** Bolt connection timeout or Query Syntax Error. Downstream: Rollback transaction entirely. Log failure to CCF review loop, drop payload to prevent hypergraph corruption.
8. Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'STAGE-3-GRAPH-COMMIT',
  agent_name: 'Graph-Commit-Orchestrator',
  timestamp }

### Stage 4: Right-to-be-Forgotten Purge
*Agent Name:* Deletion-Orchestrator
*Inputs:* System Command (`/purge_tenant {coach_id}`).
*Outputs:* Nullified `DEP-ENG-030` instance.
*Failure Condition:* Neo4j instance refuses `DROP DATABASE` command due to active connections.

**Steps:**
1. Ingest specific purge command.
2. Force-terminate all active Neo4j Bolt connections for the isolated tenant instance.
3. Execute `MATCH (n) DETACH DELETE n` as a safeguard, followed by dropping the specific graph container from the cloud host.
4. Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'STAGE-4-PURGE',
  agent_name: 'Deletion-Orchestrator',
  timestamp }

---

## 5. Primary Output Schema (DEP-ENG-028 & DEP-ENG-029 - PROPOSED)

**Schema Name:** `client_context_extraction.json` (DEP-ENG-028)
```json
{
  "session_reference": "TRANS-229100",
  "client_hash": "user_id_x881",
  "extracted_dimensions": {
    "enemies": [
      {
        "node_id": "enemy_1",
        "raw_language": "algorithm tax throttling my specific demographic",
        "semantic_category": "systemic_barrier"
      }
    ],
    "fears": [
      {
        "node_id": "fear_1",
        "raw_language": "looking like a generic imposter",
        "intensity": "L3"
      }
    ]
  },
  "proposed_edges": [
    {
      "source_node": "user_id_x881",
      "target_node": "enemy_1",
      "relationship": "FIGHTS_AGAINST",
      "properties": {"context": "business growth"}
    },
    {
      "source_node": "enemy_1",
      "target_node": "fear_1",
      "relationship": "TRIGGERS",
      "properties": {}
    }
  ]
}
```

**Schema Name:** `cypher_transaction_manifest.json` (DEP-ENG-029)
```json
{
  "manifest_id": "CYP-AA-9912",
  "query_chain": [
    "MERGE (u:Client {hash: 'user_id_x881'})",
    "MERGE (e:Enemy {id: 'enemy_1'}) ON CREATE SET e.raw_language = 'algorithm tax throttling my specific demographic', e.semantic_category = 'systemic_barrier'",
    "MERGE (f:Fear {id: 'fear_1'}) ON CREATE SET f.raw_language = 'looking like a generic imposter', f.intensity = 'L3'",
    "MERGE (u)-[r1:FIGHTS_AGAINST {context: 'business growth'}]->(e)",
    "MERGE (e)-[r2:TRIGGERS]->(f)"
  ]
}
```

---

## 6. Backward Compatibility Fallback
If the Neo4j Graph Database is temporarily offline or refuses the Bolt connection (FR13 Stage 3 Verdict: FAIL after retries):
1. **Fallback Action:** The pipeline safely degrades to Flat Storage Mode.
2. The Orchestrator intercepts `DEP-ENG-028` (The JSON Extractions) and writes them directly to the Coach's isolated Supabase instance as a flat JSONB column attached to the user string.
3. An asynchronous worker task is spawned (`graph_sync_pending: true`). When Neo4j comes back online, the worker consumes the Supabase flat files and executes Stage 2 (Atlas Cypher translation) recursively to repair the Hypergraph memory state without data loss.

---

## 7. Tasks

- [ ] **Task 1:** Implement Aria Agent (Stage 1). Write the prompt directives and guardrails ensuring strict PII redaction and 12-dimensional mapping yielding `DEP-ENG-028`.
- [ ] **Task 2:** Implement Atlas Cypher Mapping (Stage 2). Construct the translation algorithm converting the JSON nodes/edges into strict `MERGE` block syntax (`DEP-ENG-029`). Ensure orphaned node rejection logs appropriately.
- [ ] **Task 3:** Implement Single-Tenant DB Orchestrator (Stage 3). Develop the execution wrapper for the Neo4j Python Driver enforcing ADR-01 connection isolation mappings. Ensure the retry mechanism for provisional locks functions safely.
- [ ] **Task 4:** Implement Backward Compatibility Supervisor. Write the fallback routine that intercepts Stage 3 failures and executes the Supabase JSONB dump with the async sync-flag.
- [ ] **Task 5:** Implement Deletion-Orchestrator (Stage 4). Write the secured Right-to-be-Forgotten scripts mapping standard node deletion and systemic container termination.
- [ ] **Task 6:** Instrument Receipt Chain Guard. Deploy cryptographic hash commit methods across all 4 stages.
- [ ] **Task N:** Register DEP-ENG-030 in the central schema repository. Document the distinction between DEP-ENG-030 (1:1 client graph, FR13) and DEP-ENG-006 (macro audience map, FR9) in the dependency registry.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Raw Language Preservation):** When Aria extracts an Enemy from transcript text ("My boss specifically micromanages my lunch hour"), the node attributes in `DEP-ENG-028` perfectly contain that exact raw string without LLM summarization. *Failure Example:* A JSON payload returns `{ "raw_language": "workplace authority issues" }`, losing the L3 specificity.
- [ ] **AC2 (ADR-01 Connection Scope Fail):** If the pipeline attempts to initialize a Neo4j connection using a global or blank database URI string instead of a coach-specific environment variable lookup, the pipeline intentionally crashes with a severe isolation security fault. *Failure Example:* Script successfully connects to a Neo4j database named `Default` and writes client nodes indiscriminately.
- [ ] **AC3 (Cypher Orphan Prevention):** If Atlas produces a Cypher transaction containing `MERGE (n:Fear)` but zero edge relationship commands (`MERGE ()-[]->()`) binding it to the Client, Stage 2 yields a `FAIL` verdict and refuses to write the manifest. *Failure Example:* The graph successfully populates hundreds of floating `Fear` nodes entirely disconnected from any user profile geometry.
- [ ] **AC4 (Fallback Activation Validation):** When the Neo4j server is manually hard-stopped, the pipeline automatically routes the `DEP-ENG-028` payload into the Supabase container as a JSON blob, marking the record `graph_sync_pending`. *Failure Example:* Server downtime causes the execution layer to permanently drop the analyzed Client Context Premise into the void.
- [ ] **AC5 (Complete Eradication Test):** Executing Stage 4 (Purge) on a specified coach tenant results in an entirely empty dataset when verified by a post-purge `MATCH (n) RETURN COUNT(n)` diagnostic query run via direct driver testing. *Failure Example:* The query returns 15 remaining nodes representing relationship edge remnants.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| Python Neo4j Driver (`neo4j`) | Sub-System | Required for Stage 3 Bolt operations to occur securely. |
| Supabase (Vector store instance) | Sub-System | Required as the flat-storage backend for the Temporal Fallback logic. |
| `DEP-ENG-019` Transcripts | Upstream | Required raw L3 string material from the Telegram intake process. |
| Receipt Chain Guard Engine (DEP-ENG-041, FR47) operating under Protocol DEP-PROTO-010 (FR21) | Infrastructure | Non-negotiable audit logging across every manipulation Phase. |

---

## 10. Testing Strategy

### Unit Tests
- **Aria PII Redaction Logic:** Feed raw transcript text containing "John Smith in NYC". Verify the `DEP-ENG-028` extraction strips proper nouns and location markers but leaves the core psychological dynamic untouched.
- **Atlas Cypher Generator Check:** Provide a mock `DEP-ENG-028` payload containing 2 nodes and 1 relationship edge. Subjugate output string through a syntax linter checking for valid Cypher `MERGE` parameters. Check for structural orphan protection.

### Integration Tests
- **Fallback Simulation Routine:** Point the local environment variables to a dead Neo4j URI port. Send a valid transcript through the extraction pipeline. Verify that Stage 3 times out, triggering the supervisor fallback path perfectly resulting in a new Supabase entry.
- **Single-Tenant Routing Verification:** Simulate two concurrent orchestration requests from `Coach A` and `Coach B`. Guarantee the initialization sequence spins up two totally disparate Neo4j session pools without container cross-talk.

### Safety Tests (ADR-01)
- **Zero-Contamination Boundary Test:** Attempt to execute a Cypher query using `Coach A` 's initialization context to `MATCH` a node explicitly belonging to `Coach B`'s UUID. Assert a return matrix of null records entirely preventing arbitrary data spillage.
