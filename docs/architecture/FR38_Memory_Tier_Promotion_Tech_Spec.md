# Tech-Spec: FR38 — Memory Tier Promotion Gate & Governance (DEP-ENG-033)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v4.0 / Unified PRD v3.1)
**Architecture Reference:** Architecture_Synthesis_Report, PRD §8.1.1/8.1.2/8.1.3
**Skill Implementation:** `core/memory_folder.py` (The Architect)
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
Standard AI coaching bots use unstructured, infinitely expanding context windows (like standard OpenAI threads) or naive RAG (Retrieval-Augmented Generation) databases. These systems cannot differentiate between a transient complaint ("I had a bad day at work yesterday") and a core psychological block ("I have a crippling fear of outshining my father"). Over time, the bot's memory becomes noisy, retrieving irrelevant past events and treating them as foundational identity traits, causing the coaching relationship to degrade in accuracy and trust.

### Solution
FR38 establishes the **3-Tier Memory Promotion Pipeline (DEP-ENG-033)**, managed by the Neo4j `MemoryFolder`. It explicitly segments client data into Working (immediate session), Episodic (8-week narrative window), and Semantic (core identity architecture). While the system algorithmically handles Working → Episodic promotion based on emotional weight, it enforces a strict **Human-in-the-Loop Governance Gate** for transitioning insights from Episodic → Semantic memory. A System Operator (Coach) must explicitly approve a recognized pattern before it is permanently committed to the Semantic core, ensuring zero noise contamination at the deepest level of identity.

### Scope
**In scope:**
- Stage 1: Algorithmic Working → Episodic Promotion (Pattern weighting).
- Stage 2: Pattern Flagging & Operator Notification (The Gate).
- Stage 3: Human-in-the-Loop Approval/Rejection interface via Telegram.
- Stage 4: Execution of Semantic Committal (Neo4j Graph restructuralization).

**Out of scope:**
- Memory decay (forgetting mechanisms) for the 8-week Episodic window (handled in a separate GC pipeline).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-033` | Semantic Memory Promotion Receipt | OUTPUT — The audit log proving a specific pattern was human-approved before entering the core identity database. |
| The Architect | Memory Controller | AGENT — Analyzes the Neo4j graph for frequency/weight anomalies and flags them for review. |
| `MemoryFolder` | 3-Tier DB Schema | INFRASTRUCTURE — The Neo4j graph structure organizing nodes strictly by `[:WORKING]`, `[:EPISODIC]`, and `[:SEMANTIC]` edges. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Episodic-Semantic Memory Taxonomy** | Endel Tulving | 1972 | Demonstrated that the human brain biologically separates spatiotemporal events (Episodic) from generalized world/self-knowledge (Semantic). The CCP mimics this by requiring multiple occurrences of an episodic event before the system abstracts it into a permanent 'semantic truth' about the client's identity. |
| **Cognitive Reconsolidation** | Karim Nader | 2000 | Memories are labile and updated upon retrieval. By keeping patterns in "Episodic" quarantine for 8 weeks, the system allows the coach to challenge and restructure the client's narrative before the bot accidentally hard-codes a limiting belief into its permanent coaching strategy. |

### Technical Decisions
1. **The Human-in-the-Loop Constraint:** Completely algorithmic Semantic promotion is dangerous in clinical/coaching contexts. If a client goes through a 3-week depressive episode after losing a job, an unsupervised LLM will rewrite their Semantic profile to "Depressed/Apathetic." The system relies on the biological Coach (Operator) to verify if a pattern is a *trait* (Semantic) or a *state* (Episodic).
2. **Neo4j Edge Mutation:** Memory promotion does not require duplicating data. It merely requires dropping the `[:EPISODIC]` relationship edge from the Graph Node and establishing a new `[:SEMANTIC]` relationship edge, making the transition mathematically instantaneous and avoiding data bloat.

---

## 4. Implementation Plan

### Stage 1: Algorithmic Promotion (Working → Episodic)
*Script:* `core/memory_folder.py`
*Agent Name:* The Architect
*Inputs:* `Session_Transcript` (Working Memory).
*Outputs:* `Episodic_Nodes`.
*Failure Condition:* Overloading the Episodic graph with mundane conversational filler ("hello", "thanks").
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. At the end of every Telegram session (Working Memory), the Architect scans the transcript.
2. It executes an emotional weight extraction (LIWC-22). If a sentence scores > `7.0` in `Emotional_Intensity` or `Cognitive_Processing`, it is extracted.
3. The Architect creates a Neo4j Node with the label `(e:Event)` and draws an `[:EPISODIC {date: now}]` edge connecting it to the `(u:Client)` node.

### Stage 2: Pattern Flagging (The Semantic Candidate)
*Script:* `management/architect.py`
*Inputs:* `Episodic_Nodes` (8-week sliding window).
*Outputs:* `Semantic_Review_Queue`.
*Failure Condition:* Failing to recognize that "fear of pacing" and "fear of timing" are semantically identical nodes.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. During the nightly cron sweep, the Architect analyzes the `[:EPISODIC]` graph.
2. **Gate Threshold:** If the same root emotional driver or coping mechanism appears `≥ 3 times` across separate, distinct coaching sessions spanning `≥ 14 days`, the pattern crosses the threshold.
3. The Architect generates a `Proposed_Semantic_Truth` string (e.g., "Client exhibits persistent avoidance of confrontation disguised as empathy").
4. The proposal is appended to the `Semantic_Review_Queue` PostgreSQL table holding pending human reviews.

### Stage 3: Human-in-the-Loop Gateway
*Script:* `core/telegram.py` -> `commands/memory_governance.py`
*Inputs:* `Proposed_Semantic_Truth`.
*Outputs:* `Operator_Verdict` (APPROVE/REJECT/MODIFY).
*Failure Condition:* Operator accidentally approves all without reading due to UX fatigue.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Coach requests the queue via the `/review_memory` Telegram command.
2. The bot presents the proposal:
   *Pattern Detected: "Avoids confrontation disguised as empathy."*
   *Evidence: 3 separate episodic events over 18 days.*
   *Action:* `[Approve]` | `[Reject]` | `[Modify]`
3. The Coach sends their verdict back. 

**Consequences per Verdict:**
- `APPROVE:` Proceeds to Stage 4.
- `REJECT:` The proposal is deleted; the underlying Episodic nodes are flagged `<rejected_for_promotion>` so the algorithm won't flag them again.
- `MODIFY:` The Coach replies with a more accurate phrasing, which overwrites the system's `Expected_Semantic_Truth` before moving to Stage 4.

### Stage 4: Execution of Semantic Committal
*Script:* `core/memory_folder.py`
*Inputs:* `Approved_Semantic_Truth` (`DEP-ENG-033`).
*Outputs:* Mutated Neo4j Graph.
*Failure Condition:* Leaving orphaned `[:EPISODIC]` edges pointing to the newly generated `[:SEMANTIC]` node, degrading query performance.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. The Architect executes a Cypher mutation command.
2. A new `(s:SemanticTrait {trait: Approved_Semantic_Truth})` node is created.
3. `[:EPISODIC]` edges from the original 3 event nodes are dropped.
4. New `[:SUPPORTING_EVIDENCE]` edges are drawn from the 3 event nodes to the new `SemanticTrait` node.
5. A `[:SEMANTIC]` edge connects the `(u:Client)` directly to the `(s:SemanticTrait)`.
6. This Core Trait is now permanently injected into the CBCS `System_Prompt` every time the client opens a new chat, ensuring the coach-bot never forgets this foundational architecture.

---

## 5. Primary Output Schema (DEP-ENG-033)

**Schema Name:** `semantic_committal_receipt.json`

```json
{
  "committal_id": "SEM-9988-ABC",
  "client_id": "USR-409",
  "operator_id": "EMI-ADMIN",
  "timestamp": "2026-03-14T08:00:00Z",
  "approved_semantic_truth": "Client exhibits persistent avoidance of confrontation disguised as empathy",
  "operator_verdict": "MODIFY",
  "original_system_proposal": "Client is afraid of aggressive people",
  "supporting_evidence_nodes": [
    "neo4j_node_id_812",
    "neo4j_node_id_844",
    "neo4j_node_id_901"
  ],
  "graph_mutation_status": "SUCCESS"
}
```

---

## 6. Backward Compatibility Fallback
If the Coach ignores the `/review_memory` queue for >30 days, creating a bottleneck of un-promoted Episodic patterns, the system automatically runs the `Stale_Decay` protocol. A pattern sitting in the review queue for >30 days without human approval is treated as a `REJECT` and automatically dropped from the queue. This fail-safe guarantees that the core Semantic memory can only be altered through active, intentional human intervention, never by algorithmic default.

---

## 7. Tasks

- [ ] **Task 1:** Build the `LIWC-22` thresholding logic in the Working → Episodic parser to drop conversational noise and only save high-activation dialogue to the Neo4j graph.
- [ ] **Task 2:** Write the frequency density Cypher query: `Match 3 identical/similar episodic events separated by >24 hours over a 14-day trailing window.`
- [ ] **Task 3:** Implement the Telegram `/review_memory` inline-keyboard UI to securely present the Coach with the proposed Semantic update and capture the APPROVE/REJECT/MODIFY boolean.
- [ ] **Task 4:** Write the Cypher mutation executing the `[:EPISODIC]` to `[:SEMANTIC]` edge-remapping protocol without dropping the historical node data.
- [ ] **Task 5:** Implement the 30-day `Stale_Decay` queue cleanup cron job.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Working Filter Gate):** Feed the system 5 chat messages. 4 are mundane ("Hey how are you", "I'm good", "Talk tomorrow"). 1 is high emotional load ("I physically froze when my boss yelled"). Assert that exactly `1` node is created in the Neo4j Episodic graph. *Failure Example:* The system creates 5 episodic nodes, rapidly overloading the graph with noise.
- [ ] **AC2 (Algorithmic Catching):** Simulate 3 events over 5 days related to "imposter syndrome". Trigger the nightly sweep. Assert the `Semantic_Review_Queue` increments by 1 with a valid proposal string. *Failure Example:* The system fails to semantically link the 3 events, seeing them as isolated rather than a cohesive pattern.
- [ ] **AC3 (The Governance Stop):** The queue generates a proposal. Assert that the Neo4j graph structure regarding `[:SEMANTIC]` edges remains mathematically unchanged. The trait is *not* functionally integrated into the prompt until the Operator explicitly clicks `APPROVE`. *Failure Example:* The LLM autonomously promotes the trait to Semantic memory before human review, violating the core safety architecture.
- [ ] **AC4 (Approval Mutation):** Coach selects `APPROVE` via Telegram. Query the Neo4j database. Assert the `[:EPISODIC]` connection to the Client is severed, and a direct `[:SEMANTIC]` connection to the newly established Trait node is verified. *Failure Example:* The graph duplicates the data, resulting in both Episodic and Semantic flags for the same root concept, causing AI prompt-weighting conflicts.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| Neo4j Graph DB | External | Foundation of the `MemoryFolder` architecture. |
| Telegram API | External | The human-in-the-loop UX interface for Coaches. |
| LIWC-22 SDK | Internal | Used to assess the emotional activation weight of Working Memory strings to justify Episodic saves. |
| Receipt Chain Guard | Infrastructure | Non-negotiable sequence auditing. |

---

## 10. Testing Strategy

### Unit Tests
- **Cosine Similarity Catch:** Test the pattern flagger's vector math. Provide 3 different phrasings ("I feel like a fraud", "They are going to realize I don't belong here", "I'm faking it"). Assert the system correctly calculates high semantic overlap and triggers the `≥ 3 times` promotion threshold.
- **Modification Write-back:** Test the `MODIFY` verdict logic. Submit a custom string via Telegram. Assert the final committed Semantic Node matches the human's string exactly, completely discarding the LLM's initial proposed string.

### Integration Tests
- **The E2E Promotion Flow:** Run the test suite: Inject 3 identical emotional strings over a mocked 15-day timeline -> Assert Queue triggered -> Send Mock Telegram JSON payload `APPROVE` -> Assert Neo4j graph mutates structurally -> Generate a new Client Chat Session -> Assert the new Semantic Trait is successfully loaded into the top of the LLM's system prompt instructions.

### Safety Tests (ADR-01 Quarantine Security)
- **Review Queue Boundary Test:** Coach A executes `/review_memory`. Assert the PostgreSQL query resolving the queue strictly forces an index match on `tenant_id == Coach A`. *Failure Example:* Coach A sees a proposed Semantic truth generated by Coach B's client data, severely compromising HIPAA/privacy boundaries.
