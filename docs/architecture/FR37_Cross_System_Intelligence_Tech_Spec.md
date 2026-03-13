# Tech-Spec: FR37 — Cross-System Intelligence Routing (Sunday Bot Meeting) (DEP-ENG-032)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v4.0 / Unified PRD v3.1)
**Architecture Reference:** Architecture_Synthesis_Report, PRD §Cross-System
**Skill Implementation:** `management/orchestrator.py` (Vidye), `CCF/core/context_engine.py` (Aria)
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
In traditional business models, 1-on-1 coaching operations and Marketing/Content operations are completely siloed. A coach might spend all week putting out fires regarding "imposter syndrome" in client DMs, but the content system blindly publishes a pre-scheduled marketing post about "time management." This creates a massive disconnect. The audience feels the content is tone-deaf to their current reality, and the coach's live intelligence is wasted. Marketing becomes a guessing game based on demographics rather than real-time clinical data.

### Solution
FR37 defines **Cross-System Intelligence Routing (DEP-ENG-032)**, operationalized via the weekly **Sunday Bot Meeting**. This is the circulatory system of the CCP. It connects the Conscious Bot Coaching System (CBCS) directly to the Content Creation Factory (CCF). Every Sunday at 23:00 UTC, Agent Vidye (The Orchestrator) scans the Neo4j `MemoryFolder` of all active coaching clients to detect high-frequency behavioral patterns and Level-3 (L3) pain points that emerged in Telegram that week. She compiles this into an aggregate payload and hands it to Agent Aria (Context Engine). Aria uses this live intelligence to overwrite the `Context Premise` for the entire upcoming week's content production cycle.

### Scope
**In scope:**
- Stage 1: The `MemoryFolder` Aggregation Sweep (Vidye).
- Stage 2: Frequency & Density Analysis (Pattern Recognition).
- Stage 3: The Handoff (The Sunday Bot Meeting).
- Stage 4: CCF `Context_Premise` Base Overwrite.

**Out of scope:**
- Exposing PII (Personal Identifiable Information) or specific user quotes. The system performs strict anonymized aggregation to protect client privacy.
- The actual writing of the CCF content (this spec solely governs the *strategic routing* of the premise).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-032` | Cross-System Intelligence Payload | OUTPUT — The aggregated, anonymized strategic brief handed from the Coaching system to the Content system. |
| Vidye | The Orchestrator | AGENT — Scans the Neo4j graph for coaching patterns. |
| Aria | Context Engine | AGENT — Consumes the payload to set the CCF weekly premise. |
| `DEP-ENG-006` | Context Premise | READ + GRAPH APPEND (existing nodes never mutated) # REVISED: Output role changed to non-destructive append. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Grounded Theory in Qualitative Data** | Glaser & Strauss | 1967 | Instead of starting with a hypothesis (e.g., "my audience needs time management"), researchers collect data (client DMs), code for core concepts, and allow the actual theory/theme to emerge organically from the ground up. The Sunday Bot Meeting replicates this by forcing the CCF content engine to derive its weekly theme *only* from the empirical data of what clients actually struggled with that week. |

### Technical Decisions
1. **Neo4j Sub-Graph Queries:** Because client memory is stored in a Neo4j Knowledge Graph, Vidye does not have to read 10,000 strings of raw text. She runs a Cypher query targeted specifically at the `[EXPRESSED_PAIN]` and `[DEMONSTRATED_COPING_MECHANISM]` relationships established during the week, making the aggregation pipeline incredibly fast and computationally cheap.
2. **Anonymization by Design:** The Cypher query is restricted to pulling relation types and node categories. It is strictly forbidden from querying the `.raw_transcript` property of any node. This structurally guarantees no PII can leak into the marketing content engine.

---

## 4. Implementation Plan

### Stage 1: The MemoryFolder Aggregation Sweep
*Script:* `CBCS/management/orchestrator.py`
*Agent Name:* Vidye
*Inputs:* Neo4j Graph Database.
*Outputs:* Raw Frequency Tally.
*Failure Condition:* Neo4j connection times out during the aggregate sweep.
*Receipt Write:* Write Receipt Block per FR47 `Receipt_Block_N.json` schema: `{ receipt_id, previous_receipt_hash, input_payload_hash, output_payload_hash, stage_name, timestamp, agent_name }` # REVISED: Standardizing receipt format across all specs per FR47 cryptographic schema.

**Steps:**
1. A CRON job triggers `sunday_bot_meeting()` at Sunday 23:00 UTC.
2. Vidye connects to the Neo4j tenant database for the specific Coach.
3. Vidye executes the Cypher Aggregation Query:
   ```cypher
   MATCH (u:User)-[r:EXPRESSED_PAIN]->(p:PainPoint)
   WHERE r.timestamp >= datetime().truncate('week')
   RETURN p.category as Theme, count(r) as Frequency
   ORDER BY Frequency DESC LIMIT 5
   ```
4. Vidye repeats the query for `[DEMONSTRATED_COPING_MECHANISM]`.

### Stage 2: Density Analysis & Thematic Synthesis
*Script:* `CBCS/management/orchestrator.py` -> LLM
*Agent Name:* Vidye
*Inputs:* Frequency Tally.
*Outputs:* `Strategic_Brief_JSON`.
*Failure Condition:* LLM hallucinates a theme completely unrelated to the top 3 frequency hits.
*Receipt Write:* Write Receipt Block per FR47 `Receipt_Block_N.json` schema: `{ receipt_id, previous_receipt_hash, input_payload_hash, output_payload_hash, stage_name, timestamp, agent_name }` # REVISED: Standardizing receipt format across all specs per FR47 cryptographic schema.

**Steps:**
1. Vidye combines the top 5 Pain Points and top 5 Coping Mechanisms into a prompt structural array.
2. Vidye asks the LLM to synthesize the *Unified Meta-Theme* of the week. (e.g., Top Pain = "Fear of pacing", Top Coping = "Procrastination via over-planning" → Meta-Theme = "Action-Paralysis").
3. Vidye formats the output into the standard hand-off payload.

### Stage 3: The Handoff (The Meeting)
*Script:* `shared/message_bus.py`
*Inputs:* `Strategic_Brief_JSON`.
*Outputs:* Delivery Confirmation.
*Failure Condition:* The CCF system is offline and drops the payload.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Vidye securely pushes the payload via the shared Redis message bus (or direct Supabase API insertion) into the `ccf_weekly_strategy` table.
2. The payload status flag is set to `UNREAD_BY_ARIA`.

### Stage 4: Weekly Intelligence Node Injection # REVISED: Replaced entirely to prevent the destruction of DEP-ENG-006 graph.
*Script:* `CCF/core/context_engine.py`
*Agent Name:* Aria
*Inputs:* `Strategic_Brief_JSON` (`DEP-ENG-032`).
*Outputs:* Updated `Context_Premise` (`DEP-ENG-006`).
*Failure Condition:* Aria fails to parse the incoming JSON, reverting to a default/generic marketing premise.
*Receipt Write:* Write Receipt Block per FR47 `Receipt_Block_N.json` schema: `{ receipt_id, previous_receipt_hash, input_payload_hash, output_payload_hash, stage_name, timestamp, agent_name }`
*Additional Receipt Write:* `SUNDAY-INTEL-INJECT-{coach_id}-{week_epoch}` # REVISED: Added missing specific receipt format.

**Steps:**
1. Do NOT overwrite DEP-ENG-006. # REVISED: Non-destructive append logic enforced.
2. Create a new Neo4j node: `:WeeklyModifier`
   Properties: `{ modifier_id, coach_id, week_epoch, theme_slug, coping_pattern_detected, frequency_score, source: 'sunday_bot_meeting' }`
3. Create relationship: `(:WeeklyModifier)-[:WEEKLY_MODIFIER {week: epoch}]->(:EmotionalTrigger)` connecting to the relevant existing dimension nodes in the DEP-ENG-006 graph.
4. The 12-dimension ontology nodes are READ ONLY in this stage.

---

## 5. Primary Output Schema (DEP-ENG-032)

**Schema Name:** `sunday_bot_meeting_payload.json`

```json
{
  "routing_id": "SBM-2026-Week12",
  "coach_id": "EMI",
  "period": {
    "start": "2026-03-09T00:00:00Z",
    "end": "2026-03-15T23:59:59Z"
  },
  "aggregation_metrics": {
    "active_clients_analyzed": 142,
    "top_pain_points": [
      {"theme": "Imposter Syndrome", "frequency": 87},
      {"theme": "Boundary Guilt", "frequency": 42}
    ],
    "top_coping_mechanisms": [
      {"theme": "People Pleasing", "frequency": 91},
      {"theme": "Withdrawal/Silence", "frequency": 33}
    ]
  },
  "strategic_synthesis": {
    "recommended_meta_theme": "The Guilt of Setting Standards",
    "archetype_targeting_weight": "The Martyr"
  },
  "pii_leak_status": "CLEAN"
}
```

---

## 6. Backward Compatibility Fallback
If the CBCS system has less than 3 active coaching clients for a specific coach (e.g., they just launched the app), there is not enough statistical density to generate a valid cross-system theme. Vidye’s Cypher query returns `< 3`. Vidye gracefully aborts the Sunday Bot Meeting and does not write to the bus. Aria wakes up, finds no payload, and defaults to standard chronological theme rotation based on the overarching Brand DNA.

---

## 7. Tasks

- [ ] **Task 1:** Write the Neo4j Cypher aggregation logic in `orchestrator.py` ensuring it rigorously filters by `timestamp >= datetime().truncate('week')` and strictly excludes all string properties.
- [ ] **Task 2:** Build the LLM synthesis prompt for Vidye to successfully merge disparate pain and coping vectors into a single, cohesive `recommended_meta_theme`.
- [ ] **Task 3:** Implement the Shared Redis Message Bus (or Supabase connector) to bridge the architectural gap between the isolated CBCS Docker container and the CCF Docker container.
- [ ] **Task 4:** Modify `CCF/core/context_engine.py` (Aria) to poll the `ccf_weekly_strategy` table before executing any Monday generations, overriding the week's contextual context variables entirely.
- [ ] **Task 5:** Implement the `< 3` minimum threshold abort logic to prevent skewed statistical routing for brand-new coaches.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Data Aggregation Validation):** Populate the Neo4j test database with 10 dummy clients. Add 8 `[EXPRESSED_PAIN]` edges to "Burnout" and 2 edges to "Self-Sabotage". Run the SBM sweep. Assert the `top_pain_points` JSON array correctly ranks "Burnout" at index `0` with frequency `8`. *Failure Example:* The system counts node creation rather than relationship instances, skewing the data.
- [ ] **AC2 (PII Zero-Trust Gate):** Run the SBM sweep over a database containing user nodes loaded with names, emails, and sensitive journal texts. Assert that the resulting `DEP-ENG-032` JSON payload contains precisely 0 characters matching any known user PII string. *Failure Example:* The summary accidentally pulls a quote: "Like Jessica said, I'm just so tired", breaching HIPAA constraints across the system boundary.
- [ ] **AC3 (CCF Integration Override):** Dispatch a valid SBM payload recommending "The Guilt of Setting Standards." Run a CCF Tierlist generation on Monday. Assert that the resulting Tierlist script explicitly anchors its thematic hook to "guilt" and "standards" rather than the generic DNA default. *Failure Example:* Aria receives the payload but fails to prioritize it in the context hierarchy, allowing the prompt to default back to generic advice.
- [ ] **AC4 (Cross-Tenant Execution):** Run the Sunday Bot Meeting at 23:00 UTC. Assert that the system loops cleanly through every registered Coach tenant ID, generating distinct, isolated payloads for Coach A vs Coach B based entirely on their respective client databases. *Failure Example:* The system runs a global sweep of all clients across all coaches, giving a high-performance executive coach the metadata theme of the mommy-blogger coach.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| Neo4j Cypher API | Internal | Required for lightning-fast graph aggregation over 7-day windows. |
| Redis / Message Bus | Infrastructure | Required to breach the container wall between CBCS and CCF cleanly. |
| Receipt Chain Guard | Infrastructure | Non-negotiable sequence auditing. |

---

## 10. Testing Strategy

### Unit Tests
- **Threshold Integrity Test:** Run the SBM worker on a tenant with exactly 2 active users. Assert the system returns `[ABORT: INSUFFICIENT_N_COUNT]` and does not push a payload to the CCF bus.
- **Synthesis Logic Test:** Programmatically feed Vidye an impossible contradiction (Top Pain = "Can't gain weight", Top Coping = "Starving myself"). Assert the LLM can still generate a synthesized thematic bridge (e.g., "The Paradox of Control") without crashing the JSON schema.

### Integration Tests
- **The Container Bridge Test:** Spin up the CBCS worker and the CCF worker as isolated instances. Run the SBM execute command. Assert the payload successfully transverses the network boundary and successfully mutates the local memory state of the CCF Context Engine.

### Safety Tests (ADR-01 Quarantine Security)
- **Cypher Security Audit:** Execute a mock SQL-injection/Cypher-injection attempt through a user's raw Telegram transcript input (e.g., naming their coping mechanism `") DETACH DELETE MATCH (n)`). Assert the Neo4j driver strictly parametrizes the string sanitization and does not drop the graph during the Sunday aggregation.
