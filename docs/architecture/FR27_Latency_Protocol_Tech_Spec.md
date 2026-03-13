# Tech-Spec: FR27 — Daily Accountability Rituals & <2s Latency Protocol (DEP-PROTO-017)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v4.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §CBCS, §7.5 (CBCS Pipeline), Architecture_Synthesis_Report
**Skill Implementation:** `CBCS/backend/ingress.py`, `core/graph.py`
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
In traditional automated coaching portals, users log into a web dashboard, fill out a form, and wait for a batch-processed email response. This heavy friction destroys daily habit formation. If the core CCP interaction moves to a native messaging app (Telegram) to simulate intimacy, the system *must* respond with the cadence of a human texting back. If a user texts their "coach" about a moment of anxiety and waits 15 seconds for an LLM to generate a ritual, the conversational illusion breaks, exposing the automation and rupturing trust.

### Solution
FR27 defines the **<2s Latency Protocol (DEP-PROTO-017)** for Daily Accountability Rituals. It operates entirely as a real-time event-driven webhook pipeline via FastAPI. By aggressively paring down the synchronous LangGraph critical path, utilizing the `ModelRouter` to aggressively defer heavy generative tasks to background queues, and leveraging micro-models (Gemini Flash / Groq) for routing decisions, the system guarantees a P95 end-to-end response latency of under 2 seconds. <2s felt latency via Ghost Typing UX masking. <2700ms technical end-to-end latency. # REVISED: Aligned non-functional limit with Decision 1.

### Scope
**In scope:**
- Stage 1: Fast Ingress & Crisis Pre-Scan (The 100ms Gate).
- Stage 2: The Critical Path (Role/State/Intent Routing).
- Stage 3: Low-Latency Generation (Artisan Execution).
- Model-tiering strategies via `ModelRouter`.

**Out of scope:**
- Weekly cc-batch production (this operates on a permitted 4-hour batch SLA).
- Heavy RAG vector updates (moved to background async tasks).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-PROTO-017` | <2s Latency Protocol | LOGIC — Performance mandate governing the CBCS LangGraph. |
| `ModelRouter` | LLM Tiering Extension | LOGIC — Directs simple classification prompts to lightning-fast models. |
| `ingress.py` | FastAPI Webhook | INFRA — Primary HTTP receiver from the Telegram Bot API. |
| Liliane | Guardian Agent | AGENT — Executes the critical <100ms Tier-1 crisis scan. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Conversational Turn-Taking** | Sacks et al. | 1974 | In natural human conversation, gap times between turns average 200ms. Delays exceeding 2 seconds are universally interpreted cross-culturally as hesitation, cognitive overload, or socially disjointed interaction. Sub-2s latency is not a technical "nice to have"; it is a psychological requirement for the illusion of presence. |

### Technical Decisions
1. **The Asynchronous Offload (Graph Updates):** Writing heavy relationship vectors to the Neo4j Knowledge Graph takes 300-800ms. In the CBCS pipeline, this write is *never* on the critical path. The system responds to the Telegram user immediately based on Working Memory, while Azaria (Memory Curator) updates the Episodic Memory graph in a detached background worker.
2. **Model Router Tiering:** Agent Vidye (Orchestrator/State Router) requires zero creative generation; he merely selects 1 of 5 state paths (Classify: Is the user answering a ritual, asking a question, or experiencing a crisis?). This task is hard-coded to `Gemini 1.5 Flash` (or Groq equivalents) yielding inference times <300ms. `Gemini 1.5 Pro` is locked strictly to Artisan (The Master Copywriter) for the final response generation.

---

## 4. Implementation Plan

### Stage 1: Ingress & Crisis Pre-Scan (Target: <150ms)
*Script:* `ingress.py` -> `core/circuit_breaker.py`
*Agent Name:* Liliane (The Guardian)
*Inputs:* Raw Telegram JSON Payload.
*Outputs:* `crisis_check=PASS/FAIL`
*Failure Condition:* Network timeout connecting to Telegram webhook.
*Receipt Write:* Per FR47 DEP-ENG-041 schema — # REVISED: Standardized receipt format.
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'INGRESS-CRISIS-SCAN',
  agent_name: 'Liliane-Guardian',
  timestamp }

**Steps:**
1. FastAPI endpoint `/webhook` receives the Telegram JSON event and offloads it immediately from the web server thread to a high-priority queue.
2. `RoleRegistry` resolves the unique `chat_id` via a Redis memory cache (*not* a slow DB lookup) to load the active User Profile.
3. Liliane runs the *Tier 1 Local Regex Scan*. This does NOT hit an LLM. It scans the payload string against a local dictionary of 500 crisis/self-harm keywords.
4. If `<FAIL>`, bypass the entire graph and instantly return the hardcoded localized Crisis Protocol response via Telegram API.

### Stage 2: Context & Intent Routing (Target: <2700ms Tech Limit) # REVISED: Aligned latency cap
*Script:* `core/state.py`
*Agent Names:* Aria (Synthesizer) + Vidye (Orchestrator)
*Inputs:* Parsed User Text, Redis User State.
*Outputs:* `active_graph_node` parameter.
*Failure Condition:* LLM API endpoint timeout mapping state.
*Receipt Write:* Per FR47 DEP-ENG-041 schema — # REVISED: Standardized receipt format.
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'CONTEXT-INTENT-ROUTING',
  agent_name: 'Aria-Vidye',
  timestamp }

**Stage 2 Latency Architecture:** # REVISED: Updated specific budget allocation vs Ghost Typing
- T=0ms: Voice note received by ingress.py
- T=0ms: Ghost Typing indicator activated immediately (UX layer — coach sees typing indicator before any processing begins)
- T=0–2500ms: Aria executes 12-dimension Context Extraction (<2500ms SLA)
- T=2500ms: Vidye receives extraction output and executes routing (<200ms)
- T=2700ms: Response dispatched to coach
- Felt latency: <2s (masked by Ghost Typing)
- Technical latency: <2700ms end-to-end

### Stage 3: Low-Latency Assembly & Delivery (Target: <1200ms)
*Script:* `core/artisan.py` -> `core/telegram.py`
*Agent Names:* Assembler (Strategist) -> Artisan (Copywriter)
*Inputs:* Routed Intent, `coach_soul.json` TTT baselines.
*Outputs:* Formatted Telegram message dispatched via API.
*Failure Condition:* Generation payload exceeds max tokens, stalling generation time past the 2s barrier.
*Receipt Write:* Per FR47 DEP-ENG-041 schema — # REVISED: Standardized receipt format.
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'ASSEMBLY-AND-DELIVERY',
  agent_name: 'Artisan',
  timestamp }

**Steps:**
1. Assembler loads the specific Ritual structure from local memory based on Vidye's routing.
2. Artisan (using `Gemini 1.5 Pro` locked to a strict `max_output_tokens: 150` limit) writes the personalized response fusing the 6-Beat Conscious Arc with the Coach's TTT baseline.
3. The string is passed to `core/telegram.py` which executes the outward HTTP POST to the Telegram API.
4. The moment the HTTP 200 OK is received from Telegram, the HTTP response to the user's interaction point is closed, completing the <2s loop.

### Stage 4: Background Offload (Asynchronous)
*Script:* `core/graph_db.py`
*Agent Name:* Azaria
*Inputs:* Interaction Log.
*Outputs:* Updated Neo4j Graph Edges.
*Execution:* Post-Delivery.

**Steps:**
1. A celery/background worker picks up the interaction receipt.
2. Azaria updates the 8-week Episodic Memory vectors in Supabase and the structural edges in Neo4j.
3. This adds 0ms to the user-facing latency.
*Receipt Write:* Per FR47 DEP-ENG-041 schema — # REVISED: Added missing Stage 4 receipt.
{ stage_name: 'CBCS-RESPONSE-DISPATCH',
  coach_id, session_id,
  input_payload_hash, output_payload_hash,
  timestamp }

---

## 5. Primary Output Schema (ModelRouter Config Mapping)

**Schema Name:** `model_execution_tier_map.yaml` (Consumed by `<2s Latency Protocol)

```yaml
# DEP-PROTO-017 Execution Tiers

tasks:
  - agent: "Liliane"
    function: "circuit_breaker"
    model_tier: "LOCAL_REGEX_ONLY"
    max_latency_budget_ms: 100

  - agent: "Vidye"
    function: "intent_classification"
    model_tier: "FAST_CLASSIFICATION" # Gemini 1.5 Flash
    max_output_tokens: 15
    max_latency_budget_ms: 300

  - agent: "Aria"
    function: "context_extraction"
    model_tier: "FAST_CLASSIFICATION" # Gemini 1.5 Flash
    max_output_tokens: 150
    max_latency_budget_ms: 400

  - agent: "Artisan"
    function: "copy_generation"
    model_tier: "HEAVY_REASONING" # Gemini 1.5 Pro
    system_instruction: "CONCISE_SMS_MODE"
    max_output_tokens: 150 # Critical constraint to prevent verbose generation lag
    max_latency_budget_ms: 1000

global_fail_safe:
  fallback_model: "FAST_CLASSIFICATION"
  timeout_trigger_ms: 1800
```

---

## 6. Backward Compatibility Fallback
If the LLM provider experiences an acute degradation (e.g., API P95 latency spikes to 4 seconds), the `ModelRouter` monitors internal round-trip times per component. If `max_latency_budget_ms` is breached on Stage 2 (Routing), the system implements the **"Ghost Typing" Fallback**. The orchestrator immediately dispatches a Telegram typing indicator API call (`sendChatAction: typing`) back to the user to visually buy an extra 3 seconds of psychological tolerance before the user perceives the bot as broken or unresponsive. 

---

## 7. Tasks

- [ ] **Task 1:** Reconfigure `ingress.py` to utilize Redis for instantaneous `chat_id` lookup, moving the slow Supabase query to a fallback read.
- [ ] **Task 2:** Audit the LangGraph structure built in `core/graph.py` to ensure Remgion's heavy vector search (RAG) is conditional, bypassed entirely for simple intent classifications.
- [ ] **Task 3:** Implement the `ModelRouter` interface to dynamically switch between Flash/Pro model endpoints based on the `model_execution_tier_map.yaml` configuration.
- [ ] **Task 4:** Force a hard generation stop in Artisan's prompt constraints, capping generation output to 150 tokens max. This enforces SMS-sized responses and mechanically prevents the LLM from taking >1s to stream a massive wall of text.
- [ ] **Task 5:** Abstract all Neo4j Graph Updates (`graph_db.py`) into asynchronous `asyncio.create_task()` background calls that do not block the HTTP return in `main.py`.

---

## 8. Acceptance Criteria

- [ ] **AC1 (The Sub-2s Guarantee):** A simulated user sends short text: "I did the journaling prompt." The system processes State, Role, Artisan copy, and fires the Telegram POST in `<1.90` seconds, exactly as tracked in the Receipt metric. *Failure Example:* The system writes the interaction summary to Neo4j synchronously, stalling the delivery edge and completing the transaction in 3.4 seconds.
- [ ] **AC2 (The 100ms Gate):** A simulated user sends text containing a Tier-1 crisis keyword. Liliane detects it via Local Regex and dispatches the localized crisis resource link to the Telegram API in `<150ms`. No LLM was invoked. *Failure Example:* The system sends the crisis string to an LLM to evaluate intent, taking 800ms and adding fatal cloud failure risk to a life-safety protocol.
- [ ] **AC3 (Latency Fallback Grace):** Force the Gemini API latency mock testing tool to hang for 2.5 seconds. The pipeline monitors the delay, issues a `sendChatAction: typing` command at the 1800ms mark, and successfully delivers the eventual response. *Failure Example:* The system silently hangs for 4.5 seconds without updating the user's UI.
- [ ] **AC4 (ADR-01 Strict Isolation):** During the Redis memory cache retrieval in Stage 2, the pipeline securely accesses the Session ID explicitly mapped to Coach B. *Failure Example:* The cache collision returns Coach A's TTT baseline for a user that works with Coach B.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| `ModelRouter` Extension | Internal | Handles LLM tier switching to preserve latency. |
| Telegram Bot API | External | Webhook ingress + delivery edge. |
| Redis Cache | Infrastructure | Needed for 0ms lookup mapping users to active contexts. |
| Receipt Chain Guard | Infrastructure | Non-negotiable sequence auditing. |

---

## 10. Testing Strategy

### Unit Tests
- **Model Router Tier Validation:** Programmatically request `intent_classification` from the Model Router. Assert it returns the API client configured for Gemini 1.5 Flash (not Pro). 
- **Crisis Local Regex Check:** Send a payload string with 150 benign words and 1 hidden dictionary crisis word. Assert the function breaks immediately and returns `FAIL` in under 15ms.

### Integration Tests
- **P95 Stress Test:** Fire 50 concurrent webhooks at `main.py` simulating 50 users interacting across 10 different coaches simultaneously. Track the `LAT-DELIVERY` receipts. Assert that the P95 latency across all 50 resolutions remains firmly under 2000ms.
- **Background Task Verification:** Fire a single interaction event. Assert that the HTTP request returning 200 OK completes in `<2s`, but that 5 seconds later, checking the Neo4j database reveals the new relationship edge was successfully resolved in the background.

### Safety Tests (ADR-01 Quarantine Security)
- **Redis Namespace Segregation:** Simulate 2 concurrent inbound message from User Y (Coach B) and User X (Coach A). Assert that the pipeline properly silos the `coach_soul.json` loads. Ensure that a high-volume load request does not accidentally overwrite the Redis cache pointer globally.
