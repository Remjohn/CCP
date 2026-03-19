# FR-CBCS-14: Conscious Relationship Nurturing Architecture — Tech Spec

**Created:** 2026-03-18
**Status:** Ready for Development
**Architecture Reference:** CCP_CBCS_CPSC_V3 §F14, PRD §FR-CBCS-14

---

## 1. Files Read
- `docs/prd/prd.md`
- `lab/CCP update/CCP_CBCS_CPSC_V3.docx.md`

---

## 2. Overview

### Problem Statement
When 13 discrete psychological features operate independently (analyzing intimacy, detecting Search phases, logging change talk, and executing campaigns), they risk collision. A client might receive a Deep Disclosure prompt from the Daily Cycle on the exact same day a Counterfactual Activation Window fires from the Campaign Cycle. This results in disjointed, confusing communication that breaks immersion and feels "robotic".

### Solution
The Conscious Relationship Nurturing Architecture operates as the meta-level governance layer. It orchestrates all CBCS components across three distinct temporal cycles: the Daily Cycle, Weekly Cycle, and Campaign Cycle. It enforces global `Queue Locks` and rigorous 21-day `Commercial Cooldwons`, ensuring all 13 underlying features synthesize into a single, cohesive timeline.

### Scope
**In scope:**
- Instantiation of the `Conscious Relationship Nurturing Orchestrator` agent.
- Governance variables dictating Enum routing for DAILY / WEEKLY / CAMPAIGN states.
- The `Commercial Cooldown Gate` enforcing the mandatory 21-day wait between offers.

**Out of scope:**
- The NLP processing functions inside the sub-nodes (handled by FR-CBCS-01 through 13).
- Underlying messaging delivery hooks.

---

## 3. Context for Development

### Architecture Traceability
| DEP-ID | Name | Role | Produced By | Consumed By |
|---|---|---|---|---|
| `PROPOSED: DEP-ENG-070` | Interaction Queue Lock | Resolves Daily/Campaign collision | FR-CBCS-14 | All Generators |
| `PROPOSED: DEP-ENG-071` | Cooldown Log Verdict | Pass/Fail Gate payload | FR-CBCS-14 | Coach Broadcasts |

### Academic Grounding
- **Research Paper:** *Synthesis of Altman, Petty, Collins, and Zeelenberg.*
- **Mechanism:** Repeated interactions over time must build Cialdini's "Consistency." If the system demands deep intimacy today but then switches to sterile sales logic tomorrow, it generates "uncanny valley" dissonance, shattering the parasocial bond. The orchestrator is the psychological continuity driver preventing semantic collisions.

### Technical Decisions
- **Strict Cooldown:** Following *any* commercial invitation (accepted, ignored, or declined), a strict 21-day cooldown period is mathematically enforced globally.
- **Queue Interception:** All FR-CBCS node outbound messages route through the Orchestrator before dispatch. Hierarchy: Campaign Cycle $\rightarrow$ Weekly Reset $\rightarrow$ Daily Ritual.

---

## 4. Implementation Plan

### Stage 1: Variable Resolution Rules (Cycle State)
- **Agent:** `Conscious Relationship Nurturing Orchestrator`
- **Variable Resolution Rule:** The meta-state Enum `active_cycle` dictates which sub-system is permitted to message the client today.
  - **"CAMPAIGN"**: Evaluates `True` IF `search_phase_detections.status == 'CONFIRMED'` (FR-CBCS-06) OR `operator_manual_trigger == True`. Automatically generates `queue_lock_active = True`, suspending all standard Daily messages.
  - **"WEEKLY"**: Evaluates `True` IF `datetime.weekday() == 6` (Sunday) AND `active_cycle != 'CAMPAIGN'`. Triggers FR-CBCS-07 and FR-CBCS-04 background sweeps.
  - **"DAILY"**: Evaluates `True` globally IF neither of the above conditions matches. Allows FR10 Rituals and FR-CBCS-10 Deep Disclosure logic to run.

### Stage 2: Quality Gate Extension
**Quality Gate:** **The Commercial Cooldown Gate**
- **Triggered when:** ANY system (Automated Campaign, Broadcast Planner, UI Dashboard) attempts to dispatch a payload where `contains_offer == True`.
- **Exact Thresholds:**
  - `days_since_last_commercial_dispatch = (Current_UTC - MAX(offer_sent_timestamps))`
  - `Condition_1`: `days_since_last_commercial_dispatch > 21.00`
- **Verdict - PASS:** `Condition_1` is `True`. *Downstream Consequence:* Campaign dispatch permitted.
- **Verdict - PROVISIONAL:** `days_since_last_commercial_dispatch <= 21.00` AND `days_since_last_commercial_dispatch > 14.00` BUT the client explicitly sent a message natively triggering `liwc_scores.info_seeking > 0.1` regarding the product. *Downstream Consequence:* The system overrides the freeze because the client asked for information. Draft pushed to Operator Review queue flagged `"Cooldown Override Request: Client Initiated"`.
- **Verdict - FAIL:** `Condition_1` is `False` (without explicit client query). *Downstream Consequence:* Payload instantly blocked. Write exception `ERROR: 21-Day Cooldown Violation Attempted`. System refuses connection to Telegram webhook.
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `client_id` + `cooldown_gate_verdict` written to APM logs to create an immutable record of gate operations.

### Stage 3: Resolution Rules for Output Schema
The JSON payload explicitly logs the routing status for every systemic ping:
- `orchestration_id`: `uuid.uuid4()`.
- `client_id` / `coach_id`: Synchronous passage mapped.
- `active_cycle`: Populated precisely by Stage 1 Enum Logic ("DAILY" | "WEEKLY" | "CAMPAIGN").
- `queue_lock_active`: Boolean. Automatically evaluated `True` if `active_cycle == 'CAMPAIGN'`, isolating the client from FR10 generic messages.
- `cooldown_gate_verdict`: Driven explicitly by Stage 2 ("PASS" | "PROVISIONAL_OVERRIDE" | "FAIL_COOLDOWN_ACTIVE").
- `cooldown_expiry_timestamp`: Target UTC marker for exactly Day 21, Hour 0, Minute 0 post-offer.
- `last_executed_node`: String trace (e.g., `"FR-CBCS-05"`).
- `computation_timestamp`: `datetime.now(timezone.utc).isoformat()`.

---

## 5. Primary Output Schema

```typescript
type RelationshipCycleLog = {
  orchestration_id: string; // uuid4 primary key
  client_id: string; // uuid4
  coach_id: string; // uuid4 (ADR-01 boundary)
  active_cycle: "DAILY" | "WEEKLY" | "CAMPAIGN";
  queue_lock_active: boolean; 
  cooldown_gate_verdict: "PASS" | "PROVISIONAL_OVERRIDE" | "FAIL_COOLDOWN_ACTIVE";
  cooldown_expiry_timestamp: string; // ISO8601
  last_executed_node: string; 
  computation_timestamp: string; // ISO8601
};
```

---

## 6. Backward Compatibility Fallback
For legacy FR53/FR54 structures executing from traditional CSV List CRM layers:
- The Orchestrator wraps the final Telegram Gateway endpoint. If a legacy mass-email tool attempts a `/broadcast` containing an offer to 100 people, the Orchestrator loop dynamically parses `days_since_last_commercial_dispatch` per ID.
- If 40 clients are within the 21-day freeze, the gateway silently drops those 40 payloads, passing 60 through, preventing the legacy tool from aggressively spamming the tribe and violating the architecture.

---

## 7. Tasks
- [ ] **Task 1: Master Orchestrator** - Implement `conscious_nurturing_orchestrator.py` embedding the explicit `active_cycle` execution routing hierarchy mapping CAMPAIGN > WEEKLY > DAILY states.
- [ ] **Task 2: Queue Lock Enforcement** - Inject `if not queue_lock_active:` logical blocks into all FR10 Daily Ritual generation nodes.
- [ ] **Task 3: Cooldown Gate Triggers** - Deploy the POST transaction interceptor mathematically asserting the `> 21.00` float float logic against all outbound arrays.

---

## 8. Acceptance Criteria
- [ ] **AC1 (Hard Cooldown Gate Execution):** Given `days_since_last = 18.00`, system executes a broadcast command. Orchestrator MUST evaluate `FAIL_COOLDOWN_ACTIVE`. **Failure Example:** Legacy broadcast script bypasses the Orchestrator check entirely, blasting a client during their 21-day psychological recovery period.
- [ ] **AC2 (Provisional Consent Override):** Given `days_since = 15.00` BUT client sent a query `"What does module 2 cover?"` mapping `info_seeking = 0.15`. Orchestrator MUST evaluate `PROVISIONAL_OVERRIDE` pushing draft to Operator instead of hard failing. **Failure Example:** Bot denies a hot lead information they directly requested out of blind algorithmic rigidity.
- [ ] **AC3 (Queue Locking Hierarchy):** While `active_cycle = CAMPAIGN`, FR10 attempts to push a standard Daily quote. Orchestrator MUST evaluate `queue_lock_active = True`, quietly dropping the Daily quote payload. **Failure Example:** Client receives "Here's a quote on peace!" and "Did you see my offer?" within 12 seconds of each other.
