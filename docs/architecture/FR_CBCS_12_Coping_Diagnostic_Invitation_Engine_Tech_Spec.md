# FR-CBCS-12: Coping-Diagnostic Invitation Engine — Tech Spec

**Created:** 2026-03-18
**Status:** Ready for Development
**Architecture Reference:** CCP_CBCS_CPSC_V3 §F12, PRD §FR-CBCS-12

---

## 1. Files Read
- `docs/prd/prd.md`
- `lab/CCP update/CCP_CBCS_CPSC_V3.docx.md`
- `lab/CVE + CPSC research papers/Disclosure, Attachment, and Conversion Architecture.md`

---

## 2. Overview

### Problem Statement
Standard funnels operate on a linear ascending model (Lead Magnet $\rightarrow$ Tripwire $\rightarrow$ Core Offer $\rightarrow$ High Ticket), assuming time equals readiness. However, if a client experiences a traumatic life event (dropping them to Information Coping Trajectory Position 1), pitching them a High Ticket Mastermind generates intense alienation and permanently severs the relationship, regardless of how long they've been on the list.

### Solution
The Coping-Diagnostic Invitation Engine acts as the final orchestrator for all commercial interactions (Day 0 of the Campaign Cycle). It completely severs the link between "time on list" and "offer shown." Instead, it dynamically maps the specific tier of product/invitation strictly against the client's current Coping Position (FR-CBCS-04), ensuring the friction and financial commitment of the offer never exceed the psychological capacity of the client.

### Scope
**In scope:**
- The logic router `commercial-matrix-gating-engine` mapping the 5 Coping positions to 5 Product Tiers.
- The `Commercial Matrix Routing Gate`.
- Outputting the exact `invitation_tier` String Enum.

**Out of scope:**
- Storing the products or processing payments (handled by Stripe/CRM integrations).
- Executing the 72-Hour Anchor Protocol (handled upstream by FR-CBCS-05).

---

## 3. Context for Development

### Architecture Traceability
| DEP-ID | Name | Role | Produced By | Consumed By |
|---|---|---|---|---|
| `PROPOSED: DEP-ENG-067` | Commercial Routing Verdict | Safely limits offer bounds | FR-CBCS-12 | FR53 |

### Academic Grounding
- **Research Paper:** *Readiness to Change and Information Processing* (Prochaska & DiClemente, 1983) + *Cognitive Load Theory* (Sweller, 1988).
- **Mechanism:** A client in state 1 (Deficiency) has zero available cognitive load. Asking them to make a complex $3,000 buying decision creates cognitive overload, triggering fight/flight/freeze. Matching the invitation (e.g., a simple, free downloaded guide) to their exact cognitive capacity ensures continual engagement without reactance.

### Technical Decisions
- **Hard Tier Binding:** The system enforces a strict 1-to-1 mapping via an array dictionary. No client in Position 1 can ever be sent an offer matching Tier 3 or Tier 4, completely stripping the LLM's capacity to hallucinate inappropriate upsells.

---

## 4. Implementation Plan

### Stage 1: Variable Resolution Rules (Tier Mapping)
- **Agent:** `commercial-matrix-gating-engine` (Python Policy Router)
- **Inputs:** 
  - `information_coping_trajectory` integer status (DEP-ID: `information_coping_trajectory` — Produced By: FR-CBCS-04)
  - `unified_identity_profile` (DEP-ID: `DEP-ENG-056` — Produced By: FR-CBCS-03)
  - `draft_campaign_offer` (DEP-ID: `DEP-ENG-053` — Produced By: FR53 Conversion Engine)

**Variable Resolution Rule (The Matrix):** The system resolves the specific String Enum `invitation_tier` mapping explicitly to the incoming Integer `coping_position`:
- **"DEFICIENCY_ESCAPE_ROUTE"**: Evaluates `True` IF `coping_position == 1`. (Logic: Suggests a free, low-friction micro-resource. Constraint: `Price <= $0`).
- **"ILL_INFORMED_BRIDGE"**: Evaluates `True` IF `coping_position == 2`. (Logic: Suggests introductory educational material. Constraint: `Price <= $49`).
- **"NEEDS_INJECTION_CATALYST"**: Evaluates `True` IF `coping_position == 3`. (Logic: Suggests intermediate challenge or cohort. Constraint: `Price <= $399`).
- **"INFORMATION_HEALTH_PARTNERSHIP"**: Evaluates `True` IF `coping_position == 4`. (Logic: Suggests flagship program or 1:1 consultation. Constraint: `Price <= $5000`).
- **"DONOR_MASTERY_PATH"**: Evaluates `True` IF `coping_position == 5`. (Logic: Suggests certification, mastermind, advocacy. Constraint: `No ceiling`).

### Stage 2: Quality Gate Extension
**Quality Gate:** **The Commercial Matrix Routing Gate**
- **Triggered when:** FR53 (Day 0) logic attempts to pair a crafted copy sequence with an actual URL/Product object.
- **Exact Thresholds:** Evaluates the `product.price` associated with the `draft_campaign_offer` against the constraints mapped in Stage 1.
- **Verdict - PASS:** The paired `product.price` is `<=` the ceiling constraint dictating the client's current `invitation_tier` enum. *Downstream Consequence:* The payload commits and dispatches to Telegram.
- **Verdict - PROVISIONAL:** The paired `product.price` exceeds the ceiling by exactly 1 tier level. (e.g., Pitching a `$199` Catalyst product to a Position 2 client whose ceiling is `$49`). *Downstream Consequence:* The script intercepts and blocks auto-send. It queues the sequence in the Operator Dashboard flagged explicitly: `"Aggressive Upsell Detected. Target is Position 2."` Requires Operator button click to send.
- **Verdict - FAIL:** The paired `product.price` exceeds the ceiling by 2 or more tier levels. (e.g., Pitching a $5000 mastermind to a Position 2 client). *Downstream Consequence:* The system executes a `Hard Reject` block. It drops the sequence entirely. Returns a severe log `Matrix Violation: Endangering Client Safety`.
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `client_id` + `gate_verdict` written to the APM log upon routing conclusion.

### Stage 3: Resolution Rules for Output Schema
The JSON payload explicitly outputs the routing validations:
- `routing_id`: `uuid.uuid4()`.
- `client_id` / `coach_id`: Synchronous mapping maintaining ADR-01 isolation.
- `computed_coping_position`: Integer pass-through from `FR-CBCS-04`.
- `invitation_tier`: Evaluated via the exact Dictionary Mapping described in Stage 1 strings.
- `target_product_price`: Float numeric extraction from the `draft_campaign_offer` webhook payload.
- `gate_verdict`: "PASS" | "PROVISIONAL" | "FAIL_VIOLATION" driving action.
- `timestamp`: UTC ISO8601 logging the exact moment of computation.

---

## 5. Primary Output Schema

```typescript
type CommercialRoutingVerdictRow = {
  routing_id: string; // uuid4
  client_id: string; // uuid4
  coach_id: string; // uuid4 (ADR-01 boundary)
  computed_coping_position: 1 | 2 | 3 | 4 | 5;
  invitation_tier: "DEFICIENCY_ESCAPE_ROUTE" | "ILL_INFORMED_BRIDGE" | "NEEDS_INJECTION_CATALYST" | "INFORMATION_HEALTH_PARTNERSHIP" | "DONOR_MASTERY_PATH";
  target_product_price: number; // Float
  gate_verdict: "PASS" | "PROVISIONAL" | "FAIL_VIOLATION";
  timestamp: string; // ISO8601
};
```

---

## 6. Backward Compatibility Fallback
System overrides are occasionally required for specific "Open Cart" calendar launches (Capability Area 10). 
- If a global broadcast explicitly marks a payload `override_matrix = true` (only accessible by Coach Admin via `CCF Planner`), the system downgrades the `FAIL_VIOLATION` to `PROVISIONAL`, allowing the operator to force the send while explicitly acknowledging the psychological mismatch.

---

## 7. Tasks
- [ ] **Task 1: Matrix Mapping** - Code the Python dictionary in `matrix_router.py` strictly binding integers 1-5 to the 5 `invitation_tier` String Enums. 
- [ ] **Task 2: Dynamic Ceiling Limits** - Create the evaluation function converting those Enums into the floating point `>=` logic determining PASS vs FAIL (`Limit_$0`, `Limit_$49`, `Limit_$399`, etc).
- [ ] **Task 3: CCF Pipeline Insertion** - Slot this verification `Quality Gate` linearly between the FR53 Text Generation loop and the Webhook API dispatch node.

---

## 8. Acceptance Criteria
- [ ] **AC1 (Hard Matrix Enforcement):** A system attempting to send a `$997` offer to a client in Coping Position 1. Script evaluates bounds: `$997  > Ceiling($0) by 3 Tiers`. Gate MUST evaluate `FAIL_VIOLATION` and permanently block dispatch. **Failure Example:** The LLM's persuasive copy bypasses safety rules and emails a distressed client an overwhelmingly expensive program, creating a chargeback risk.
- [ ] **AC2 (Provisional Escort Routing):** System attempts a `$99` offer payload targeting a Coping Position 2 client. Evaluates bounds: `$99 > Ceiling($49) by 1 Tier`. Gate MUST evaluate `PROVISIONAL` routing strictly to the UI Dashboard. **Failure Example:** The system auto-sends the upsell, annoying a client who is functionally unready for increased friction.
- [ ] **AC3 (Enum Integrity):** A `coping_position` of `4` parsed synchronously MUST map into the `invitation_tier` output exactly as `"INFORMATION_HEALTH_PARTNERSHIP"`. **Failure Example:** Off-by-one array mapping index error routes Position 4 to the `$399` ceiling string causing false blockades for high-ticket clients.
