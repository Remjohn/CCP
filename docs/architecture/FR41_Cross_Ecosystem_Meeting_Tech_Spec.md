# Tech-Spec: FR41 — Monthly Cross-Ecosystem Meeting (DEP-ENG-036)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v4.0 / Unified PRD v3.1)
**Architecture Reference:** Architecture_Synthesis_Report, PRD FR24
**Skill Implementation:** `management/cross_ecosystem_orchestrator.py`
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
The CCP operates completely isolated, single-tenant ecosystems (Graph databases, memory models, LLM contexts) for each of its 24+ coaches to ensure strict data privacy and IP protection. However, this isolation creates "knowledge silos." If Coach A's ecosystem discovers that "7-step carousel posts" currently suffer a 40% drop in algorithmic reach, Coach B's ecosystem remains ignorant of this platform shift and will continue generating sub-optimal formats until its own clients explicitly complain.

### Solution
FR41 establishes the **Monthly Cross-Ecosystem Meeting (DEP-ENG-036)**. On the 1st of every month, an Orchestrator Agent spawns a secure, temporary virtual environment. Each of the 24 isolated coach ecosystems delegates one "Representative Agent" (The Analyst) to join this meeting. The representatives submit highly aggregated, strictly sanitized performance metrics—sharing macro patterns, format velocities, and structural hook success rates. The Orchestrator synthesizes these into a single `Cross_Pollination_Syllabus` which is distributed back to all 24 ecosystems, allowing the entire CCP to evolve its baseline strategies simultaneously without ever sharing a single piece of PII or Coach IP.

### Scope
**In scope:**
- The Data Aggregation and Sanitization Protocol (preventing data leakage).
- The Multi-Agent orchestration ring (The Meeting itself).
- The generation and distribution of the `Cross_Pollination_Syllabus`.
- Receipt chain logging for cross-tenant data boundaries.

**Out of scope:**
- Any sharing of Coach Voice DNA (`coach_soul.json`), Trigger Maps, or specific client semantic memory. This is strictly a macro-performance and formatting sync.

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-036` | Cross-Pollination Syllabus | OUTPUT — The sanitized macro-trend report distributed to all isolated graphs. |
| The Global Orchestrator | Sync Manager | AGENT — The central referee that accepts sanitized reports, synthesizes them, and builds the syllabus. |
| Data Analyst Agent | The Representative | AGENT — The per-tenant agent that queries its local Publer analytics and strips PII before speaking. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Federated Learning Systems** | McMahan | 2017 | Demonstrates how decentralized edge devices (in our case, isolated Coach graphs) can collaboratively learn a shared prediction model without ever exchanging raw local data. The CCP uses "Federated Prompting" rather than federated neural weights. |
| **Differential Privacy guarantees** | Dwork | 2006 | Provides the theoretical basis for ensuring that the global output (The Syllabus) cannot be reverse-engineered to reveal the specific input of any single Coach graph. |

### Technical Decisions
1. **Zero-PII Payload Rule:** The Representative Agent is mathematically barred from submitting strings of content to the meeting. It may only submit structured categorical data and numerical distributions (e.g., `"Hook_Structure_Dilemma": {"success_rate": 0.88, "n_trials": 15}`).
2. **Synchronous Virtual Execution:** The meeting occurs as a synchronous LangGraph multi-agent run. This ensures all 24 agents submit their data, wait for the global synthesis, and write the result back to their local Neo4j `MemoryFolder` simultaneously on the 1st of the month.
3. **Opt-Out Mechanism:** A Coach Organization can flag their tenant variable `CROSS_ECOSYSTEM_PARTICIPATION = FALSE`, excluding them from data sharing (but also preventing them from receiving the global syllabus).

---

## 4. Implementation Plan

### Stage 1: Local Aggregation & Sanitization (Pre-Meeting)
*Agent:* The Data Analyst (Per-Tenant)
*Inputs:* Local `Publer_Performance_Metrics`, `Local_MemoryFolder`.
*Outputs:* `Sanitized_Performance_Brief.json`.
*Failure Condition:* The brief accidentally includes a specific coach quote or client name, violating single-tenancy isolation.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. At 00:00 UTC on the 1st of the month, the Data Analyst agent in every tenant queries the last 30 days of performance data.
2. It aggregates data strictly by *Category*: Format Type (Carousel, Reel, Plain Text), Hook Structure (Dilemma, Contrarian, Question), and Structural Rhythm (Pacing).
3. The Agent executes the **Isolator Script**: It drops all text string variables (`transcripts`, `scripts`, `voice_notes`).
4. It outputs an anonymized JSON payload representing pure mechanism performance.

### Stage 2: The Multi-Agent Summit (The Meeting)
*Agent:* The Global Orchestrator
*Inputs:* Array of `Sanitized_Performance_Brief.json` (from all active tenants).
*Outputs:* Raw Multi-Agent Meeting Transcript.
*Failure Condition:* Orchestrator fails to map conflicting data (e.g., Coach A says Carousels failed, Coach B says they succeeded).
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. The Orchestrator queries `tenant_registry` to dynamically determine the total number of active ecosystems participating (`N`).
2. The Orchestrator initiates a LangGraph thread.
3. It ingests all `N` payloads and runs a statistical smoothing filter to identify universally true trends (e.g., "Across 85% of ecosystems, 5-second Hook pacing outperformed 3-second pacing").
4. If distinct cohorts emerge (e.g., B2B coaches succeeded with heavy analysis, B2C coaches failed), the Orchestrator maps those correlations.

### Stage 3: Syllabus Generation & Distribution
*Agent:* The Global Orchestrator
*Inputs:* Processed Meeting Transcript.
*Outputs:* `Cross_Pollination_Syllabus.md` (`DEP-ENG-036`).
*Failure Condition:* The Syllabus is formatted generically and the local orchestrators ignore it.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. The Orchestrator generates a structured Markdown document. It contains 3 sections:
   - **Global Tailwind:** Universally successful formats to adopt.
   - **Global Headwind:** Deteriorating strategies to abandon.
   - **Cohort Micro-Trends:** Specific adjustments based on coach maturity level.
2. The Orchestrator executes localized API POST requests (scaled dynamically to `N` tenants based on the `tenant_registry` array), injecting the document into the `/receive_intelligence` webhook of every active ecosystem.

### Stage 4: Local Integration
*Agent:* CCBS Skill Builder (Per-Tenant)
*Inputs:* `Cross_Pollination_Syllabus.md`.
*Outputs:* Updated local pipeline constraints.
*Failure Condition:* The CCBS updates a `SKILL.md` prompt violating the coach's core Voice DNA just to chase a trend.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. The local tenant receives the syllabus.
2. The CCBS reads the Global Headwind (e.g., "Stop using Question Hooks").
3. It updates the `skills/ccf/script-artisan/SKILL.md` generation rules to mathematically penalize Question Hooks for the upcoming month.
4. The global intelligence has safely influenced local output generation without breaching the tenant wall.

---

## 5. Primary Output Schema (DEP-ENG-036)

**Schema Name:** `cross_pollination_syllabus.md`

```markdown
# Monthly Cross-Ecosystem Intelligence: April 2026
**Generated By:** Global Orchestrator
**Data Sources:** Anonymized Ecosystems
**Total Output Analyzed:** 732 discrete posts

## Global Headwinds (Cease Execution)
- **Format:** High-density text graphics (Canva templates).
- **Stat:** 41% drop in audience retention across 19 ecosystems.
- **Action:** Instruct Excalidraw Render Controller to increase whitespace minimums by 20%.

## Global Tailwinds (Increase Execution)
- **Format:** Real-object transparent collage anchors.
- **Stat:** 22% higher 'Save' metric velocity when stick-figures interact with a photorealistic prop.
- **Action:** Escalate Transparent Collage Pipeline frequency.

## Structural Observations
- The "Contrarian Dilemma" hook structure is demonstrating exhaustion in B2B cohorts. Shift to "Mechanism Teardown" hooks for Q2.
```

---

## 6. Backward Compatibility Fallback
If the Global Orchestrator fails to execute due to a server failure, or if a tenant's API is unavailable during the sync window, the tenant gracefully ignores the meeting. The `CCBS` relies entirely on its local `Context_Performance_Registry` (CPR). The system functions perfectly in isolation; it merely loses the "hive mind" acceleration for that specific month until the next scheduled meeting.

---

## 7. Tasks

- [ ] **Task 1:** Write the `Data_Analyst` sanitization script explicitly filtering out all string-types before the API payload is built, utilizing Pydantic models to force strict schema adherence.
- [ ] **Task 2:** Set up the isolated Global Orchestrator Lambda/Cloud function that can securely receive dynamic arrays of active tenant API calls simultaneously.
- [ ] **Task 3:** Write the LangGraph statistical synthesis logic that averages out the performance booleans and identifies true macro-trends.
- [ ] **Task 4:** Create the local tenant webhook `/api/v1/intelligence_sync` to receive the output Syllabus markdown.
- [ ] **Task 5:** Write the update subroutine in the `CCBS` that parses the markdown and mathematically applies the weights to the active content generation templates.

---

## 8. Acceptance Criteria

- [ ] **AC1 (The Privacy Firewall):** Unit test the `Data_Analyst` payload compiler. Inject a local variable `client_name = "Sarah Jenkins"`. Assert the compiled JSON payload explicitly returns `None` or drops the key prior to transmission. *Failure Example:* PII is submitted to the Global Orchestrator, violating ADR-01 and destroying HIPAA/privacy trust.
- [ ] **AC2 (Smoothing Logic):** Mock `N` payloads simulating multiple ecosystems. Assert the Orchestrator identifies the mathematical centroid and publishes the trend, correctly ignoring the statistical noise of the minority. *Failure Example:* The Orchestrator surfaces contradicting instructions in the final syllabus.
- [ ] **AC3 (Local Integration):** Push a mock Syllabus indicating "Stop using Question Hooks." Trigger a CCF generation run on a local tenant. Assert the trace logs show the `Script Artisan` system prompt actively appending the rule: `Avoid Question Hooks`. *Failure Example:* The Syllabus arrives but is treated as passive reading material rather than an architectural constraint modifier.
- [ ] **AC4 (Opt-Out Gate):** Set `Tenant_07_CROSS_ECOSYSTEM_PARTICIPATION = FALSE`. Trigger the monthly sync. Assert Tenant 07 neither transmits data nor receives the Syllabus, remaining perfectly isolated. *Failure Example:* The Orchestrator forces Tenant 07 to participate despite the flag.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| Publer Analytics API | External | The ground-truth data source each Data Analyst uses to determine what is actually working. |
| Secure Webhook Handlers | Infrastructure | Bridging the air-gap between the isolated tenant environments and the Global central processing node. |
| Pydantic | Internal | Essential for ensuring the strict typing required to prevent rogue string (PII) data from escaping the tenant. |

---

## 10. Testing Strategy

### Unit Tests
- **Pydantic Model Validation:** Create a `PerformanceData` Pydantic model that strictly disallows `str` types in its nested dictionaries (only allowing floats indicating performance). Assert it rejects a payload attempting to pass a string quote.

### Integration Tests
- **The Month-End Sync Simulation:** Run a mocked environment with 3 tenant containers and 1 orchestrator container. Trigger the sync cron. Assert:
  1. All 3 containers emit sanitized JSON.
  2. The Orchestrator container ingests all 3 successfully.
  3. The Orchestrator writes the Markdown file.
  4. The Orchestrator fires 3 successful POST requests delivering the file back to the containers.

### Safety Tests (ADR-01 Quarantine Security)
- **Tenant IP Spoofing Prevention:** Ensure the `/intelligence_sync` endpoint requires a unique, secure asymmetric handshake per tenant. If a malicious script attempts to submit fake performance data masquerading as Tenant 14, the orchestrator must reject the payload based on a mismatched cryptographic signature.
