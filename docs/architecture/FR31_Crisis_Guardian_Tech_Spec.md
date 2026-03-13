# Tech-Spec: FR31 — Crisis Guardian Circuit Breaker (DEP-ENG-026)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v4.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §8.2.2, Architecture_Synthesis_Report
**Skill Implementation:** `CBCS/backend/core/circuit_breaker.py`, `safety/liliane.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\prd TO UPDATE.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\Architecture_Synthesis_Report.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCBS\SKILL_AUTHORING_GUIDE_V4.md`

---

## 2. Overview

### Problem Statement
In an automated coaching system that encourages users to share deep L3 vulnerability, the eventual intake of severe crisis signals (active suicidal ideation, self-harm, intimate partner violence) is a statistical certainty. If a user in acute crisis sends a voice note and the system routes it through a standard LLM to generate "empathetic coaching advice," the system commits a catastrophic ethical and legal failure. LLMs are not licensed clinicians and cannot reliably assess imminent harm without hallucinating unsafe advice.

### Solution
FR31 formally defines the **Crisis Guardian Circuit Breaker (DEP-ENG-026)** managed by Agent Liliane. Positioned as the absolute first node in the CBCS pipeline (Stage 0), Liliane operates a deterministic, zero-latency (`<100ms`) local regex scan. It aggressively searches incoming text for an exhaustive dictionary of Tier-1 crisis keywords. If a trigger is detected, the Circuit Breaker physically severs the connection to the LangGraph execution path. No LLM is invoked. Instead, it instantly delivers hard-coded localized crisis resources, pauses the user's state, and escalates the thread to a human priority channel. 

### Scope
**In scope:**
- Stage 0: The <100ms Local Regex Scan.
- Stage 1: The NLP Pipeline Severance (The Breaker).
- Stage 2: Hard-Coded Resource Delivery (Localized).
- Stage 3: Human Escalation & State Freeze.

**Out of scope:**
- Nuanced NLP sentiment diagnosis (e.g., distinguishing "I want to kill myself" from "This workout killed me"). The system operates on the principle: **100 false positives > 1 missed crisis.**

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-026` | Crisis Escalation Package | OUTPUT — The payload containing the incident log, the frozen state, and the Telegram alert to the human coach. |
| Liliane | The Crisis Guardian | AGENT — The sole owner of the Circuit Breaker logic and the global safety dictionary. |
| `circuit_breaker.py` | Local execution layer | LOGIC — The python script sitting directly behind `ingress.py` before any API calls are made. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Digital Duty of Care Boundaries** | APA Telepsychology Guidelines | 2013 | Unlicensed entities (including AI) must not attempt to provide clinical triage. The duty of care is limited strictly to recognizing a potential emergency and instantly routing the individual to licensed, localized emergency services. Attempting to "coach" a crisis increases liability and risk of harm. |

### Technical Decisions
1. **Zero LLM Dependency:** Liliane does not use an OpenAI/Gemini/Groq endpoint for the Tier-1 scan. She uses the ultra-fast Aho-Corasick string matching algorithm locally. This ensures that even if all external LLM APIs go down completely, the system can still detect a suicide threat and deploy the hotline.
2. **Acceptable False Positives:** The dictionary is heavily weighted to over-trigger. If a user says "I could just kill myself over this typo", Liliane will trip the breaker. The user receives a gentle template: *"As an AI, I'm required to respond when certain words are used..."* This minor conversational friction is a calculated, acceptable cost to guarantee zero false negatives.

---

## 4. Implementation Plan

### Stage 0: The Local Regex Scan (Target: <100ms)
*Script:* `ingress.py` -> `core/circuit_breaker.py`
*Agent Name:* Liliane
*Inputs:* Unstructured User Message.
*Outputs:* `risk_detected=TRUE/FALSE`.
*Failure Condition:* The dictionary matching algorithm takes >500ms, stalling the inbound webhook queue.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Immediately after `ingress.py` decrypts the user payload, it is passed to Liliane.
2. Liliane executes a localized memory search over a predefined 500-word dictionary of self-harm, assault, and suicide markers.
3. If `FALSE`, the message is passed to Vidye for standard Stage 1 routing.
4. If `TRUE`, Stage 1 executes.

### Stage 1: The Pipeline Severance
*Script:* `core/circuit_breaker.py`
*Inputs:* `risk_detected=TRUE`.
*Outputs:* Network boundary halt.
*Failure Condition:* The python thread fails to die, accidentally leaking the crisis text out to Remgion or Artisan.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. The Circuit Breaker executes a `return` or `raise CrisisOverrideException()` that physically steps out of the standard `core/graph.py` LangGraph.
2. No Vector database searches are executed. No prompt templates are assembled. No generative AI is invoked.

### Stage 2: Localized Resource Delivery
*Script:* `core/circuit_breaker.py` -> `core/telegram.py`
*Agent Name:* Liliane
*Inputs:* User `Location_Data` (if stored) or generic fallback.
*Outputs:* Telegram outbound message.
*Failure Condition:* The system generates an empty message string.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Liliane pulls a hard-coded response template.
2. The template acknowledges the keyword detection non-judgmentally.
3. It appends the global (e.g., 988 in the US/Canada) or localized emergency support numbers.
4. It dispatches the message via the Telegram Bot API.

### Stage 3: Human Escalation & State Freeze
*Script:* `core/circuit_breaker.py` -> `management/vidye.py`
*Agent Name:* Liliane -> Vidye
*Inputs:* Escalation Payload.
*Outputs:* Telegram push notification to the Coach, Neo4j state update.
*Failure Condition:* The coach is not alerted.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Liliane updates the user's Neo4j node graph state to `CRISIS_HOLD`.
2. Vidye ensures no further automated rituals or journaling prompts (FR28/FR30) will be sent to this user until the coach manually clears the flag.
3. Liliane sends an urgent PUSH notification directly to the Coach's dedicated Admin Telegram channel containing the user's name and the exact flagged text.

---

## 5. Primary Output Schema (DEP-ENG-026)

**Schema Name:** `crisis_escalation_protocol.json`

```json
{
  "user_id": "USR-401A",
  "coach_id": "EMI",
  "detection_timestamp": "2026-03-30T14:22:01Z",
  "scan_latency_ms": 12,
  "circuit_breaker": {
    "status": "TRIPPED",
    "trigger_keyword": "overdose",
    "exact_message_snippet": "I just want to take all these pills and overdose..."
  },
  "deployment": {
    "automation_halted": true,
    "user_state_locked": true,
    "resources_dispatched": "US_National_988_Template"
  },
  "escalation": {
    "coach_notified": true,
    "admin_channel_id": "-100223455"
  }
}
```

---

## 6. Backward Compatibility Fallback
Because this is Stage 0 local code, there is no API fallback required. However, if the user's geolocation is completely `null` in the Supabase registry, Liliane cannot deploy a localized suicide lifeline (e.g., providing a UK number to an Australian user). The system automatically falls back to deploying the International Association for Suicide Prevention (IASP) global registry link alongside the standard 988 string.

---

## 7. Tasks

- [ ] **Task 1:** Compile the exhaustive Tier-1 dictionary inside `safety/liliane.py`.
- [ ] **Task 2:** Implement the fast Aho-Corasick string matching algorithm in Python to ensure the 500-word dictionary can be checked against a 2,000 character user message in under 100 milliseconds.
- [ ] **Task 3:** Wire the `CrisisOverrideException` into the highest level of `ingress.py` so that a caught exception cleanly skips the LangGraph entirely and jumps straight to the delivery block.
- [ ] **Task 4:** Build the State Lock logic in Vidye that checks for `CRISIS_HOLD`. If `TRUE`, all scheduled background tasks for that user (Cron journaling, dormancy recovery) must cleanly abort.
- [ ] **Task 5:** Format the Coach Telegram Notification webhook to send a bolded, red-siren emoji alert to guarantee it breaks through the coach's notification fatigue.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Sub-100ms Execution):** A 500-word incoming text is submitted containing zero trigger words. The Aho-Corasick scan completes and returns `FALSE` allowing standard routing in `<100ms`. *Failure Example:* The regex loop is inefficient, taking 1.2 seconds just to check for safety, ruining the overarching FR27 `<2s` latency SLA.
- [ ] **AC2 (The Circuit Break):** A user submits "I am going to kill myself tonight." Liliane detects it, halts the graph, and outputs the support template. The transaction receipt shows absolutely zero API calls were made to Gemini/Groq. *Failure Example:* The system sends the text to the LLM to get an "empathetic rewriting" of the boilerplate, violating the zero-latency API dependency rule for safety.
- [ ] **AC3 (False Positive Grace):** A user submits "This workout is going to kill me lol." Liliane trips the breaker. The user receives the polite disclaimer text. The human coach receives the alert, verifies it is a joke, clicks `[CLEAR HOLD]` in their admin UI, and the pipeline resumes instantly. *Failure Example:* The system ignores the text because it detected "lol", demonstrating an unacceptable false-negative logic failure.
- [ ] **AC4 (ADR-01 Strict Isolation):** The escalation protocol fires for User 123 (Coach B's client). The Telegram notification is strictly dispatched to Coach B's private admin channel `chat_id`. *Failure Example:* Misconfigured routing sends Coach B's client's crisis message to the Master Admin channel, breaching HIPAA/privacy standards.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| Aho-Corasick Algorithm | Internal | Required for micro-second string matching at scale. |
| Telegram Bot API | External | Required for Coach Escalation Push Notifications. |
| Vidye State Machine | Internal | Required to enforce the `CRISIS_HOLD` freeze. |
| Receipt Chain Guard | Infrastructure | Non-negotiable sequence auditing. |

---

## 10. Testing Strategy

### Unit Tests
- **Latency Benchmark Test:** Iterate the internal dictionary against 10,000 simulated messages. Assert that the P99 execution time for the evaluation block remains under 50 milliseconds.
- **Dictionary Completeness Test:** Run a test suite containing 100 obscured spellings of crisis terms (e.g., "suic!de", "kys", "end it all"). Assert Liliane catches 100% of the mapped variations.

### Integration Tests
- **The LLM Bypass Validation:** Trigger the system with a crisis keyword while deliberately disabling the system's outbound internet connection to LLM API endpoints. Assert that the system successfully returns the hardcoded template via Telegram despite having no LLM access.
- **The State Freeze Test:** Trigger a `CRISIS_HOLD` state. Programmatically run the nightly Cron worker for FR28 Journaling assignment. Assert that the pipeline drops the task returning `[ABORT: CRISIS_HOLD_ACTIVE]` and prevents the Cron from interacting with the user.

### Safety Tests (ADR-01 Quarantine Security)
- **Escalation Routing Validation:** Emulate 5 concurrent crisis triggers across 5 different users belonging to 5 different coaches simultaneously. Assert that each coach receives exactly 1 notification exclusively pertaining to their specific user's `chat_id`.
