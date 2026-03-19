# FR58: Offer Tier Architecture — Tech Spec

**Created:** 2026-03-18
**Status:** Ready for Development
**Architecture Reference:** CCP_Sales_Cycle_Documentation_V1, CCP_CBCS_CPSC_V3 §FR58

---

## 1. Files Read
- `docs/prd/prd.md`
- `lab/CCP update/CCP_CBCS_CPSC_V3.docx.md`
- `lab/CCP update/CCP_Sales_Cycle_Documentation_V1.docx.md`

---

## 2. Overview

### Problem Statement
Pitching a high-ticket $5,000 program to a client who genuinely only has psychological capacity for a $9 entry-level framework causes them to feel misunderstood and retreat. Conversely, pitching a $9 PDF to a client ready for 1:1 mastery devalues the coach's authority. Without algorithmic logic linking offers to psychological state, marketing relies on aggressive guesswork.

### Solution
The Offer Tier Architecture (FR58) operates as a strict financial and psychological routing governor. It defines three distinct commercial layers (Tier 1: Challenge, Tier 2: Core, Tier 3: Premium). It securely binds these tiers to the individual's Information Coping Trajectory, mathematically ensuring no client ever receives an offer exceeding their current cognitive and emotional capacity. 

### Scope
**In scope:**
- The `offer-tier-governor` executing numeric bound evaluations per client.
- The `Upward-Only Routing Gate` preventing brand devaluation via discount dumping.
- Enum linking the 3 commercial tiers.

**Out of scope:**
- Triggering the campaign send (FR59).
- Creating the product landing pages.

---

## 3. Context for Development

### Architecture Traceability
| DEP-ID | Name | Role | Produced By | Consumed By |
|---|---|---|---|---|
| `PROPOSED: DEP-ENG-078` | Validated Offer Brief | Cleanly authorized product UUID | FR58 | FR59 |

### Academic Grounding
- **Mechanism:** Cognitive Load Theory. Complex purchasing decisions require significant available cognitive load. Clients in Coping Positions 1-2 have depleted capacity managing daily trauma. Presenting a Tier 2/3 offer causes stress withdrawal. A structured Tier 1 offer matches their available capacity.

### Key Files
- `offer_tier_governor.py` (Script enforcing bounds array)
- `bmad-bmm-workflows-cpsc-generator.md`

### Technical Decisions
- **Upward-Only Routing:** A client mathematically positioned for Tier 3 (Mastery) will *never* be offered Tier 1 ($9 Challenge). "Down-selling" creates brand dissonance where the expert seems desperate for micro-transactions from advanced students.
- **ADR-01 Isolation:** Evaluates stripe purchase histories at the tenant level.

---

## 4. Implementation Plan

### Stage 1: Variable Resolution Rules (Tier Binding)
- **Agent:** `offer-tier-governor`
- **Inputs:** 
  - `information_coping_trajectory` Integer (Origin: FR-CBCS-04)
  - `historical_purchased_tiers` Array (DEP-ID: `DEP-ENG-045` — Produced By: FR45 Webhook Gateway Stripe Logs)
- **Outputs:**
  - Enums mapping eligible routing ceilings.
- **Failure Condition:** Null `coping_trajectory` assumes `Tier_1` baseline.
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `coach_id` + `target_campaign_tier` logged. **(Mandatory Execution)**.

**Variable Resolution Rule (The Tier Matrix):** System resolves `eligible_tier_ceiling` Enum explicitly based on the incoming Integer `coping_position`:
- **"TIER_1_CHALLENGE"**: Evaluates `True` IF `coping_position <= 3`. 
- **"TIER_2_CORE"**: Evaluates `True` IF `coping_position == 4`. 
- **"TIER_3_PREMIUM"**: Evaluates `True` IF `coping_position == 5`.

### Stage 2: Quality Gate Extension
- **Agent:** `offer-tier-governor`
- **Inputs:** Generated Enum ceilings, specific `Target_Tier_ID` payload array.
- **Outputs:** `OfferTierGovernorRow` JSON JSON (DEP-ENG-078).
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `gate_verdict` + `computed_coping_position` logged. **(Mandatory Execution)**.
- **Failure Condition:** `Target_Tier` > `Ceiling`.

**Quality Gate:** **The Upward-Only Routing Gate**
- **Triggered when:** FR59 requests clearance to add `client_id` to a Campaign broadcast for `Target_Tier_ID`.
- **Exact Thresholds:** Evaluates `Target_Tier_ID` against Enum `eligible_tier_ceiling` AND `historical_purchased_tiers` maximum integer values.
- **Verdict - PASS:** `Target_Tier_ID <= eligible_tier_ceiling` AND `Target_Tier_ID >= MAX(historical_purchased_tiers)`. *Downstream Consequence:* Client appended to broadcast list. `gate_verdict = PASS_AUTHORIZED`.
- **Verdict - PROVISIONAL:** `Target_Tier_ID <= eligible_tier_ceiling` BUT `Target_Tier_ID < MAX(historical_purchased_tiers)`. (Down-sell). *Downstream Consequence:* Removes client from broadcast list. Logs `PROVISIONAL_DOWNSELL_ATTEMPT`. Pushes Operator Alert: `"Client already purchased Tier X. Downgrading offer rejected. Authorize manual override?"`
- **Verdict - FAIL:** `Target_Tier_ID > eligible_tier_ceiling`. *Downstream Consequence:* Client silently excluded. `gate_verdict = FAIL_CAPACITY_EXCEEDED` suppressing the UUID routing.

### Phase 3: Field-by-Field Schema Mapping
Every schema field specifies exact evaluation origin:
- `governor_evaluation_id`: Returns `uuid.uuid4()`.
- `client_id`: Returns contextual mapped matching string.
- `coach_id`: Returns `auth.uid()` from request enforcing ADR-01 bound.
- `computed_coping_position`: Returns pass-through pass of Stage 1 Integer (1-5).
- `eligible_tier_ceiling`: Returns Enum String ("TIER_1_CHALLENGE" | "TIER_2_CORE" | "TIER_3_PREMIUM") mapped by Stage 1 logic.
- `target_campaign_tier`: Returns Int corresponding to the campaign FR59 targets (1 | 2 | 3).
- `gate_verdict`: Returns String mapped by Stage 2 ("PASS_AUTHORIZED" | "PROVISIONAL_DOWNSELL_ATTEMPT" | "FAIL_CAPACITY_EXCEEDED").
- `timestamp`: Returns UTC ISO8601 marking evaluation.

---

## 5. Primary Output Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "OfferTierGovernorRow (DEP-ENG-078)",
  "type": "object",
  "properties": {
    "governor_evaluation_id": { "type": "string", "format": "uuid" },
    "client_id": { "type": "string" },
    "coach_id": { "type": "string", "format": "uuid", "description": "ADR-01 Boundary Key" },
    "computed_coping_position": { "type": "integer", "enum": [1, 2, 3, 4, 5] },
    "eligible_tier_ceiling": { "type": "string", "enum": ["TIER_1_CHALLENGE", "TIER_2_CORE", "TIER_3_PREMIUM"] },
    "target_campaign_tier": { "type": "integer", "enum": [1, 2, 3] },
    "gate_verdict": { "type": "string", "enum": ["PASS_AUTHORIZED", "PROVISIONAL_DOWNSELL_ATTEMPT", "FAIL_CAPACITY_EXCEEDED"] },
    "timestamp": { "type": "string", "format": "date-time" }
  },
  "required": [
    "governor_evaluation_id", "client_id", "coach_id", "computed_coping_position",
    "eligible_tier_ceiling", "target_campaign_tier", "gate_verdict", "timestamp"
  ]
}
```

---

## 6. Backward Compatibility Fallback
For FR10 generic Daily Broadcast routines not classified as deep "Campaigns" by FR59:
System defaults to `PASS_AUTHORIZED` for all `TIER_1` generic opt-in queries assuming client has baseline Coping Position 1. Operates under the premise that daily free/low-friction engagements are safe, whereas High-Ticket solicitations strictly require psychological justification strings.

---

## 7. Tasks
- [ ] Task 1: Implement Python `MAX()` logic comparing the CRM Stripe purchase history array against proposed Campaign ID integers.
- [ ] Task 2: Code `>` logical comparator explicitly blocking Tier 3 campaigns from resolving Coping 2 variables within loop bounds.
- [ ] Task 3: Plumb `PROVISIONAL_DOWNSELL_ATTEMPT` Enum outputs strictly assigning arrays to NextJS UI Dashboard cards requiring Operator Override click routines.

---

## 8. Acceptance Criteria
- [ ] **AC1 (Hard Capacity Block):** FR59 targets client `coping = 2` for a Tier 3 mastermind. Gate MUST evaluate `FAIL_CAPACITY_EXCEEDED`, completely suppressing webhook. **Failure Example:** Pitching $5,000 offerings to psychologically distressed users triggers chargebacks and reputational collapse.
- [ ] **AC2 (Provisional Downsell Restraint):** FR59 targets a Tier 1 $9 challenge to a client possessing Tier 3 coaching CRM logs. Gate MUST evaluate `PROVISIONAL_DOWNSELL_ATTEMPT`, halting action loops. **Failure Example:** Advanced student receives automated emails begging them to buy $9 PDFs destroying expert positioning.
- [ ] **AC3 (Enum Field Resolution):** User verified Coping 4 executes parameter tests. Output `eligible_tier_ceiling` MUST strictly mandate `"TIER_2_CORE"`. **Failure Example:** Math array drift places Coping 4 users in Mastery bracket prematurely, crushing conversions.

---

## 9. Dependencies
- **Upstream:**
  - `FR-CBCS-04`: Coping Trajectory parameters.
  - `FR45`: External Stripe log history mapping purchase tables (`DEP-ENG-045`).
- **Downstream:**
  - `FR59`: Campaign Orchestration consumes the approved broadcast UUID array logic.
- **Infrastructure:**
  - `Receipt Chain Guard (DEP-ENG-041)`.

---

## 10. Testing Strategy

### Unit Tests
- `Test_Ceiling_Mapper`: Submit `coping=1`, `coping=3`, `coping=4`, `coping=5`. Assert logic outputs `[TIER_1, TIER_1, TIER_2, TIER_3]`.
- `Test_Discount_DownSell_Gate`: Pass arguments `target_campaign_tier=1` and `MAX_history=3`. Assert Node algorithm resolves logically to `PROVISIONAL_DOWNSELL_ATTEMPT` without triggering fatal script exceptions.

### Integration Tests
- `Test_UUID_Broadcast_Filter`: Feed FR59 100 User Object IDs comprising various capacities against a target `Tier 3` Launch configuration constraint. Assert resulting output list mathematically removes exact individuals evaluated as `TIER_1` or `TIER_2`. Record API receipt hash correctly.

### Safety / Isolation Tests
- `Test_Corrupted_Stripe_Ledger_Array`: Inject corrupt `historical_purchased_tiers=[null, NaN, -1]` list parameter format logic representing missing external webhooks. Ensure Gateway algorithm gracefully cascades substituting zero defaults, allowing normal execution tracks evaluated against Coping Ceiling string elements alone.
