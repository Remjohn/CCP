# Tech-Spec: FR15 — Scheduled Monitor Agent (Autonomous M1 Triggering)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0)
**Architecture Reference:** CCP_Architecture_V5.0 §10.1, PRD §Layer 1
**Skill Implementation:** `skills/ccf/proactive/scheduled-monitor/`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CCP_Architecture_V5.0.docx.md` (Specifically Section 10: Scheduled Production Flow)
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CRAL_Documentation_V1.docx.md`

---

## 2. Overview

### Problem Statement
In previous architecture versions, the content production pipeline was strictly reactive. It required the coach to generate a "trigger" from a blank slate via a Telegram voice note. This placed the cognitive burden of identifying cultural relevance entirely on the human operator, often leading to generic topics or reduced production velocity because the coach didn't know "what to talk about today."

### Solution
FR15 implements the **Scheduled Monitor Agent**. Operating on a configurable daily cadence, this agent autonomously monitors the coach's community discourse, platform trending topics, and semantic affinity signals (the same source hierarchy as CRAL's M1 RELEVANT skill). When it detects a new, measurable cultural tension, it synthesizes an observation and proactively messages the coach via Telegram. The coach's unfiltered response to this specific observation becomes the formal session input (Trigger), shifting the CCP from a reactive tool to a proactive creative partner.

### Scope
**In scope:**
- Stage 1: The Scheduled Monitor Agent execution loop (Daily Cron).
- Stage 2: M1-equivalent Cultural Tension Extraction and Assessment.
- Stage 3: Telegram Proactive Messaging & Coach Prompting.
- Stage 4: Coach Response Ingestion and routing to the standard Triger Authentication (`DEP-ENG-005`).
- Cryptographic Receipt Chain Guard checks at each transition.

**Out of scope:**
- The downstream M2-M7 CRAL execution (handled by FR14).
- The Telegram Bot infrastructure setup (assumed existing from CBCS).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-023` | Cultural Memory Map | INPUT — Provides the established tribal context for the Monitor to measure "new" tension against. |
| `semantic_affinity` | Audience Signals | INPUT — Database table providing rising domains in audience attention. |
| `DEP-ENG-005` | Trigger Profile | OUTPUT — The final authenticated trigger object generated from the coach's response to the agent. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Information Foraging Theory / High-Scent Directives** | Pirolli & Card | 1999 | A specific trigger (the agent's observation) functions as a high-scent directive, penetrating much deeper into a coach's memory/perspective than a generic "what's on your mind?" prompt. |
| **Sensemaking Theory (Enacted Environments)** | Weick | 1995 | The trigger enacts the research environment. By providing the cultural tension *first*, the agent provides a coherent environment for the coach's certainty to have immediate meaning. |

### Technical Decisions
1. **Separation from CRAL Orchestrator:** The Scheduled Monitor Agent is an independent, lightweight chron-triggered entity. It is *not* the CRAL Orchestrator. It acts as the initiator *for* the CRAL pipeline.
2. **"New" Tension Definition:** The agent must compare current discourse against the `DEP-ENG-023` Cultural Memory Map to ensure it is prompting the coach with *novel* tensions, rather than repeatedly flagging chronic, already-addressed issues.
3. **ADR-01 Coach Isolation:** The agent runs in a strict single-tenant context. It only scrapes sources identified in the specific coach's `tribe_soul.json` and only cross-references that coach's `DEP-ENG-023` and `semantic_affinity` records. No cross-coach trend aggregation is permitted.

---

## 4. Implementation Plan

### Stage 1: Daily Monitor Initialization & Source Scraping
*Agent Name:* Scheduled-Monitor-Agent
*Inputs:* `tribe_soul.json`, `semantic_affinity` DB table.
*Outputs:* Raw discourse payload.
*Failure Condition:* API scraping limits reached or `tribe_soul.json` inaccessible.

**Steps:**
1. Cron job fires (e.g., 08:00 local coach time).
2. Agent reads `tribe_soul.json` to identify target community forums, subreddits, and specific competitor/industry channels.
3. Agent queries the `semantic_affinity` table for rising audience domains over the last 48 hours.
4. Executes targeted scraping/API calls to gather the last 24-48 hours of discourse.
5. Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'STAGE-1-MONITOR-INIT',
  agent_name: 'Scheduled-Monitor-Agent',
  timestamp }

### Stage 2: Cultural Tension Extraction & Assessment Gate
*Agent Name:* Scheduled-Monitor-Agent
*Inputs:* Raw discourse payload, `DEP-ENG-023` (Cultural Memory Map).
*Outputs:* `tension_observation_object`.
*Failure Condition:* No tension identified that exceeds the novelty/delta threshold compared to `DEP-ENG-023`.

**Logic Gate:**
- **Exact Threshold:** The extracted topic must show a >15% frequency spike in the raw payload compared to its historical baseline in `DEP-ENG-023`.
- **Verdict: PASS:** A novel, high-frequency cultural tension is identified. Proceed to Stage 3.
- **Verdict: PROVISIONAL:** Tension identified, but frequency spike is marginal (10-15%). Downstream: Proceed to Stage 3, but flag the observation as "weak signal" in the Telegram prompt phrasing.
- **Verdict: FAIL:** No novel tension identified (Discourse is static). Downstream: Abort the daily prompt. Do not message the coach. Write a `silent_abort` log.
- Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'STAGE-2-ASSESSMENT',
  agent_name: 'Scheduled-Monitor-Agent',
  timestamp }

### Stage 3: Telegram Proactive Prompt Generation
*Agent Name:* Scheduled-Monitor-Agent
*Inputs:* `tension_observation_object`.
*Outputs:* Telegram Message Payload.
*Failure Condition:* Generated message lacks the required 3-part structure (Observation, Summary, Question).

**Steps:**
1. The Agent formats the tension into a highly specific message using the strict 3-part structure:
   - Part 1: "I am seeing a lot of conversation in your community about [Specific Cultural Tension]."
   - Part 2: "Three practitioners/users I tracked are taking these positions: [Summary]."
   - Part 3: "Does this connect to something you have been thinking about for your audience?"
2. Hand off the payload to the Telegram Bot API dispatcher.
3. Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'STAGE-3-MONITOR-PROMPT',
  agent_name: 'Scheduled-Monitor-Agent',
  timestamp }

### Stage 4: Coach Response Ingestion & Session Initiation
*Agent Name:* Telegram-Intake-Router
*Inputs:* Coach Telegram Response (Voice or Text), `tension_observation_object`.
*Outputs:* `DEP-ENG-005` (Trigger Profile), CRAL Initiation Signal.
*Failure Condition:* Coach response is too short (< 15 words) or explicitly declines the prompt ("Not today").

**Steps:**
1. Await coach reply. Timeout after 12 hours (expires the daily prompt).
2. Upon receipt, if voice, route through Whisper transcription.
3. **Execution Fork:**
   - If response is an explicit decline/opt-out: Log `session_aborted_by_coach`, terminate flow.
   - If response is valid: Combine the `tension_observation_object` (serving as a pre-populated M1 foundation) with the coach's unfiltered response.
4. Route the combined payload to the standard Trigger Authentication module to generate `DEP-ENG-005`.
5. Emit signal to the CRAL Orchestrator to commence M2-M7 research sequence.
6. Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'STAGE-4-MONITOR-INGEST',
  agent_name: 'Telegram-Intake-Router',
  timestamp }

---

## 5. Primary Output Schema (DEP-ENG-005 Extension)

Because the Scheduled Monitor Agent serves as the initiator, the resulting `DEP-ENG-005` (Trigger Profile) contains an extended context block reflecting the system-generated M1 foundation.

**Schema Name:** `trigger_profile_system_initiated.json`

```json
{
  "trigger_id": "TRIG-20260313-001",
  "coach_tenant_id": "coach_88ab",
  "receipt_chain_hash": "monitor_e2e_77bcee1...",
  "initiation_type": "system_proactive",
  "system_observation": {
    "identified_tension": "Algorithm taxation impacting minority creators",
    "source_domain": "HustleCulture Subreddit",
    "frequency_delta": "+22% spike 48h",
    "prompt_delivered_at": "2026-03-13T08:00:00Z"
  },
  "coach_response": {
    "response_type": "voice_transcription",
    "raw_text": "Yes, absolutely. I was just talking to a client about this yesterday. They are terrified that the new feed rules mean their engagement is permanently capped regardless of quality.",
    "extracted_mechanism": "Systemic algorithmic throttling",
    "emotional_register": "Fear-Anxiety / Frustration"
  },
  "authentication_status": "CONFIRMED_READY_FOR_M2"
}
```

---

## 6. Backward Compatibility Fallback
If the Scheduled Monitor Agent fails to execute (e.g., cron job failure, Reddit/platform API outage), the system gracefully degrades to the **V4.0 Reactive Intake Mode**:
1. No proactive Telegram message is sent.
2. The Telegram Bot remains online in listening mode.
3. The coach must initiate the session manually by sending a voice note from a blank slate.
4. The system detects the manual initiation, flags `initiation_type: user_reactive_fallback`, and routes exactly as the legacy system did (requiring CRAL to run M1 RELEVANT from scratch since no pre-computation occurred).

---

## 7. Tasks

- [ ] **Task 1:** Implement the `Scheduled-Monitor-Agent` daily Cron trigger and source scraping module tied to `tribe_soul.json` targets.
- [ ] **Task 2:** Implement the Tension Assessment Logic Gate (Stage 2). Build the mathematical comparison engine that diffs the scraped frequency against `DEP-ENG-023` to determine true novelty. 
- [ ] **Task 3:** Implement the Telegram message formatter enforcing the rigid 3-part structural prompt. Integrate with the existing CBCS Telegram Bot dispatcher.
- [ ] **Task 4:** Refactor the Trigger Authentication module to accept the combined payload (System Observation + Coach Response) and output the extended `DEP-ENG-005` schema.
- [ ] **Task 5:** Inject Receipt Chain Guard writes at Stages 1, 2, 3, and 4. Enforce ADR-01 Coach Graph Isolation ensuring the monitor only scrapes domains relevant to the specified tenant.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Novelty Gate Enforcement):** If the agent scrapes a topic that is already heavily indexed in `DEP-ENG-023` (e.g., a chronic issue with no >15% recent spike), the Stage 2 gate returns `FAIL` and silent-aborts the daily message. *Failure Example:* The agent messages the coach about "imposter syndrome" every single day because it's always talked about, failing to identify actual breaking cultural *tensions*.
- [ ] **AC2 (Strict Prompt Formatting):** The Telegram message payload must contain the exact phrased structure: Observation, Specific Practitioner Summaries, and the closing question. *Failure Example:* The LLM generates a generic "Hey, anything you want to post about today?" bypassing the intelligent context delivery entirely.
- [ ] **AC3 (Coach Decline Handling):** If the coach responds "No" or "I'm travelling today", the Telegram intake router correctly classifies the response as an opt-out, logs the abort, and prevents the creation of a corrupted `DEP-ENG-005`. *Failure Example:* The system treats "Not today" as the topic mechanism and attempts to run CRAL M2-M7 research finding the origin of the phrase "Not today".
- [ ] **AC4 (ADR-01 Isolation):** The Scheduled Monitor Agent strictly limits its target scraping array to the URLs/domains listed in the active coach's `tribe_soul.json`. *Failure Example:* 
 The agent uses a global trending topics API (like Twitter top 10) and prompts an executive leadership coach about a trending pop-culture meme completely irrelevant to their tribe.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| `tribe_soul.json` | Upstream | Defines the scraping targets for the agent. |
| `DEP-ENG-023` (CMM) | Upstream | Baseline for calculating the cultural novelty delta. |
| `semantic_affinity` table | Upstream | Provides rising attention domains. |
| Telegram API | Infrastructure | Required for proactive message delivery and response intake. |
| Receipt Chain Guard Engine (DEP-ENG-041, FR47) operating under Protocol DEP-PROTO-010 (FR21) | Infrastructure | Non-negotiable sequence auditing. |

---

## 10. Testing Strategy

### Unit Tests
- **Novelty Assessment Logic:** Mock a raw discourse payload containing a topic with a simulated 18% frequency spike against a mock `DEP-ENG-023`. Assert the gate evaluates to `PASS`. Run again with an 8% spike, asserting `FAIL` and silent abort.
- **Prompt Structure Validation:** Run the prompt generation function and assert via regex that the 3 required structural components (Observation, Summary, Question) are present in the exact requested order.

### Integration Tests
- **Telegram Router to Trigger Auth:** Simulate a Telegram webhook payload containing the coach's text response. Assert that the Intake Router successfully combines it with the `tension_observation_object` and that the output `DEP-ENG-005` perfectly matches the schema requirements.
- **Cron to E2E Flow:** Trigger the cron scheduled function manually in a staging environment. Verify the full chain: Scrape → Assess → Prompt → (Simulate Coach Reply) → Authenticate `DEP-ENG-005` → Fire webhook to CRAL Orchestrator.

### Safety Tests (ADR-01 & Receipt Isolation)
- **Tenant Scraping Boundary Check:** Configure `Coach_A` with exclusively LinkedIn targeting in `tribe_soul`, and `Coach_B` with exclusively Reddit targeting. Execute the monitor agent. Assert that `Coach_A` execution logs show exactly 0 requests to Reddit domains, verifying absolute tenant data boundary parameters.
