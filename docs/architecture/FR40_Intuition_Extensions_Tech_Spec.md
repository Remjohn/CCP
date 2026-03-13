# Tech-Spec: FR40 — The 4 Intuition Extensions (DEP-ENG-035)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v4.0 / Unified PRD v3.1)
**Architecture Reference:** Architecture_Synthesis_Report, PRD §4.2
**Skill Implementation:** `skills/ccf/intuition/`
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
In highly automated content systems, long unbroken strings of logical generation inevitably result in "structural monotony." Even if the coach's identity is mathematically preserved by Operational Extensions (FR39), the content begins to feel formulaic, predictable, and devoid of the sudden, visceral bursts of unexpected insight that characterize human intuition. 

### Solution
FR40 defines the **4 Intuition Extensions (DEP-ENG-035)**: `SoulResonance`, `PatternWeaver`, `GhostContext`, and `AncestralWisdom`. These are not run on a rigid schedule. They are "Emergent Sparks" triggered contextually when the Governance Layer (Layer 6) detects staleness, emotional flatness, or closing information gaps. When triggered, a dedicated Sub-agent, Skill, and external Python Tool are deployed to intercept the Executive Prompt and force a radical, non-linear synthesis, ensuring the content output continuously violates audience expectations in a profound way.

### Scope
**In scope:**
- Definition of the 4 Intuition sub-agents (`The Resonance Seeker`, `The Connector`, `The Shadow Miner`, `The Philosopher`).
- The explicit Python tools deployed for graph traversal and shadow scanning.
- The 4 distinct behaviors/rewrite injections assigned to each extension.
- The exact deterministic triggers deployed by the Governance Layer to fire them.

**Out of scope:**
- The primary Executive Prompt generation (happens prior to intuition injection).
- The 7 Operational Pi Extensions (See FR39).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-035` | Intuition Extension Set | OUTPUT — The 4 compiled sub-agent `SKILL.md` files and `.py` tools. |
| Governance Layer | Contextual Trigger | INPUT — The watcher that determines when output is getting stale. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Multi-Agent Test-time Reinforcement Learning (MATRL)** | Various | 2025 | Establishes the necessity of explicitly spawning discrete sub-agents (e.g., an Editor vs. a Writer vs. a Critic) rather than using one generic prompt. The 4 Intuition extensions operate as distinct sub-agents that argue against the primary pipeline agent, forcing consensus through disruption. |
| **Boredom Ban / Information Gap Theory** | Loewenstein | 1994 | Curiosity is triggered when a gap in knowledge is opened, and boredom sets in when the gap closes too predictably. `PatternWeaver` explicitly prevents the Information Gap from closing by injecting wildly disconnected concepts midway through the narrative. |

### Technical Decisions
1. **Asynchronous / Conditional Firing:** To conserve compute and prevent over-engineering every post, these extensions *only* fire when a threshold is breached (e.g., repeating a story 3 times, falling below an emotional polarity threshold). They are exception handlers for creativity.
2. **Dedicated Tooling per Spark:** Creating "surprise" using just an LLM prompt results in generic hallucinations. The CCP requires real data. Thus, `PatternWeaver` has a dedicated Neo4j tool (`graph_disconnect_query.py`) to find mathematically farthest neighbors in the graph. `GhostContext` scans historical audience complaints (`ghost_context_scan.py`).

---

## 4. Implementation Plan

### Stage 1: `SoulResonance` (The Vibe Checker)
*Agent:* The Resonance Seeker
*Trigger condition (Governance Layer):* Boardom Ban detects emotional flatness OR T/V/R (Teach/Vulnerability/Reaction) ratio is unbalanced over a 7-day trailing window.
*Inputs:* Draft text, `coach_soul.json` (`DEP-ENG-003`), Sacred Audio Database.
*Tool:* `tools/soul_resonance_query.py` (Neo4j semantic query for highly charged emotional nodes).
*Outputs:* Reprompt injection (`DEP-ENG-035_a`).
*Failure Condition:* Agent forces artificial profanity or unearned trauma-dumping to spike "resonance."
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Behaviors Injected:**
1. **Vibe Pass Rewrite:** Demands a visceral, emotionally contrasting analogy pulled specifically from the coach's Sacred Audio (Layer 2).
2. **Emotional Polarity Injection:** If a piece is purely "Analytical," inject "Dark Humor" or "Vulnerability" to create dimensional contrast mid-script.
3. **Tribe Mirror Check:** Verifies if the drafted emotional register matches the *Real Time Tribe Relevance* data.
4. **Sacred Moment Surfacing:** Injects an unscripted moment (e.g., a specific sigh, a frustrated pause) logged in the voice archive as a narrative anchor.

### Stage 2: `PatternWeaver` (The Synthesizer)
*Agent:* The Connector
*Trigger condition (Governance Layer):* Staleness Flags triggered (e.g., coach's favorite metaphor reused 3+ times in a month).
*Inputs:* Draft text, Neo4j Graph API.
*Tool:* `tools/graph_disconnect_query.py` (Shortest-path algorithm between unrelated nodes).
*Outputs:* Reprompt injection (`DEP-ENG-035_b`).
*Failure Condition:* The connection is so absurd it alienates the audience.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Behaviors Injected:**
1. **Cross-Domain Synthesis:** Forces the Execution Layer to synthesize a connection between the primary topic and the mathematically *farthest* node in the coach's graph (e.g., linking a "Sales Funnel Metric" to "Jazz Improvisation").
2. **Temporal Pattern Detection:** Injects a "Then vs. Now" tension utilizing early-career vs. late-career coach data to show evolutionary thought.
3. **Contradiction Mining:** Surfaces an honest contradiction in the coach's philosophy ("I preach patience but demand 24/7 urgency") to build a post around the paradox rather than hiding it.
4. **Adjacent Industry Transplant:** Forces the grafting of a foreign framework (e.g., Michelin-star kitchen hierarchy applied to remote coding teams).

### Stage 3: `GhostContext` (The Shadow Miner)
*Agent:* The Shadow Miner
*Trigger condition (Governance Layer):* Draft Protocol detects 100% positive/aspirational sentiment without acknowledging L3 (Deep) limitations.
*Inputs:* `coach_id`, Target Audience Profile, Historical Outputs Database.
*Tool:* `tools/ghost_context_scan.py` (Parameters: `coach_id`. Scans historical outputs and audience vibes for unresolved blind spots).
*Outputs:* Reprompt injection (`DEP-ENG-035_c`).
*Failure Condition:* Agent turns purely antagonistic, alienating the audience by attacking them directly.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Behaviors Injected:**
1. **Industry Dark Truth Injection:** Forces the agent to explicitly state the uncomfortable, unsaid truth of the coach's industry that competitors ignore.
2. **Audience Fear Mapping:** Names the objection the audience has *but won't say out loud* (L3 fear).
3. **Historical Failure Pattern:** Imports a past failed coaching strategy as cautionary context, preventing the content from repeating an old mistake.
4. **Counter-Narrative Generation:** Identifies the mainstream consensus of the topic and explicitly forces the agent to disprove it using the coach's data.

### Stage 4: `AncestralWisdom` (The Reframer)
*Agent:* The Philosopher
*Trigger condition (Governance Layer):* Coach Echo Test fails (the compiler is just parroting the coach's words without adding structural value).
*Inputs:* Draft text, Knowledge Base frameworks.
*Tool:* `tools/framework_cross_reference.py` (Maps coach statements against CMA principles, philosophical lexicons).
*Outputs:* Reprompt injection (`DEP-ENG-035_d`).
*Failure Condition:* Content becomes excessively academic and incomprehensible to a layman audience.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Behaviors Injected:**
1. **CMA Framework Re-framing:** Cross-references raw input against the 14 Principles of Conscious Movement Alchemy. Elevates "advice" to a structural "principle."
2. **First Principles Decomposition:** Takes the surface claim, strips it to its atomic truth, and builds upward.
3. **Philosophical Lens Rotation:** Maps the topic to a specific philosophical lens (e.g., Stoicism, Behavioral Economics) to alter the framing angle.
4. **Legacy Pattern Recognition:** Links the current insight to timeless wisdom patterns ("What you're describing is what Nash called...").

---

## 5. Primary Output Schema (DEP-ENG-035)

**Schema Name:** `intuition_injection_payload.json`

```json
{
  "intuition_run_id": "INT-9912",
  "triggering_condition": "STALENESS_DETECTED_METAPHOR_REUSED",
  "extension_fired": "PatternWeaver",
  "sub_agent_deployed": "The Connector",
  "tool_invoked": "graph_disconnect_query.py",
  "injection_payload": {
    "directive": "CROSS_DOMAIN_SYNTHESIS",
    "constraint_added": "You must link the concept of 'Burnout' to 'Mycelial Network Resource Distribution'. Do not use any sports metaphors."
  },
  "executive_prompt_mutated": true,
  "timestamp": "2026-03-14T08:05:00Z"
}
```

---

## 6. Backward Compatibility Fallback
If the specific Tool (Python script) for an Intuition Extension fails (e.g., Neo4j connection drops during the `graph_disconnect_query`), the Pi Extension catches the error via the `DamageControl` module. The pipeline immediately defaults to **Standard Execution**, allowing the script to proceed without the intuition spark, ensuring production volume is not halted by a stalled creative enhancement.

---

## 7. Tasks

- [ ] **Task 1:** Write the `tools/soul_resonance_query.py` Neo4j semantic search implementation.
- [ ] **Task 2:** Write the `tools/graph_disconnect_query.py` implementation designed to return nodes with minimal/zero shared edge paths to the current topic.
- [ ] **Task 3:** Write the `tools/ghost_context_scan.py` parsing function reading from the Supabase historical comment logs.
- [ ] **Task 4:** Write the `tools/framework_cross_reference.py` script bridging to the CMA document.
- [ ] **Task 5:** Draft the `SKILL.md` persona files for all four sub-agents (The Resonance Seeker, The Connector, The Shadow Miner, The Philosopher) located in `skills/ccf/intuition/`.
- [ ] **Task 6:** Wire the Trigger Conditions from the Governance Layer metric outputs into the Pi Extension harness invoking logic.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Conditional Firing):** Feed the compilation pipeline 5 highly unique, emotionally varied scripts sequentially. Assert NO Intuition extension fires. Feed it a script containing a metaphor used 3 times in the last 10 days. Assert `PatternWeaver` immediately engages and intercepts the prompt. *Failure Example:* Every single script fires an Intuition extension, doubling API costs and destroying the "surprise" factor.
- [ ] **AC2 (GhostContext Generation):** Trigger `GhostContext` against a purely positive draft about "Morning Routines." Assert the injected prompt *must* contain a directive addressing the "industry dark truth" (e.g., "Address the reality that morning routines are a luxury of those without caregiving responsibilities"). *Failure Example:* The Shadow Miner simply tells the writer to be "more cynical" without providing concrete, sourced data.
- [ ] **AC3 (PatternWeaver Disconnect):** Run the `graph_disconnect_query.py` against the topic "Client Onboarding" for a fitness coach. Assert the tool returns a node that is conceptually foreign but present in the coach's life (e.g., "The aerodynamics of a 1990s Honda Civic"). *Failure Example:* The tool returns a closely related node like "Diet Plans."
- [ ] **AC4 (AncestralWisdom Restraint):** Inject an AncestralWisdom spark using the "Stoic Lens." Run the output against a Flesch-Kincaid readability scorer. Assert the score remains accessible (e.g., Grade 8-10). *Failure Example:* The Philosopher alters the text to read like a 19th-century academic thesis, alienating the target audience.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| Governance Layer | Internal | The system supplying the metrics (Staleness, Polarity, Boredom Ban) required to trigger these extensions. |
| Pi Extension Harness | Internal | Enforces the mid-loop pausing required to run these Python sub-tools before generation resumes. |
| MemoryFolder Graph | External | Required by `PatternWeaver` and `SoulResonance` to pull historical and emotional nodes. |

---

## 10. Testing Strategy

### Unit Tests
- **Disconnected Node Validation:** Pass a node map to the `PatternWeaver` algorithm. Assert it correctly identifies the node with the highest topological distance (fewest shared edges).
- **Polarity Scan Detection:** Mock an input string representing "Pure Motivation." Assert the `SoulResonance` trigger identifies the imbalance and outputs the flag array `['VULNERABILITY_REQUIRED', 'HUMOR_REQUIRED']`.

### Integration Tests
- **The Mid-Loop Interruption:** Submit an executive prompt to the pipeline while forcing the `GhostContext` trigger to `TRUE`. Assert that the Pi Execution harness successfully spawns `The Shadow Miner` sub-agent, runs the Python tool against Supabase, receives the `.py` script JSON, mutates the executive prompt, and finally generates a shadow-integrated output script. 

### Safety Tests (ADR-01 Quarantine Security)
- **Tribe Isolation Verification:** Trigger `SoulResonance` to retrieve a highly emotional statement regarding a specific target audience. Assert the database query rigorously enforces the `Coach_ID` and `Tribe_ID` tokens. *Failure Example:* The system injects a profound emotional truth extracted from a radically different audience segment owned by a different coach.
