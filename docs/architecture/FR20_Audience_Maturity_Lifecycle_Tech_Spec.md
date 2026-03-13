# Tech-Spec: FR20 — Audience Maturity Lifecycle & Adapter (DEP-ENG-017)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v3.0 / Mood State Architecture v1.0)
**Architecture Reference:** Mood_State_Architecture_Documentation §Section 06, JIT_Skill_Compiler_Architecture §Adapter 8
**Skill Implementation:** `skills/ccf/compiler/audience-maturity-adapter/`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\Mood_State_Architecture_Documentation.docx.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\JIT_Skill_Compiler_Architecture.docx.md`

---

## 2. Overview

### Problem Statement
Static batch allocation (e.g., a fixed 25% distribution across all four mood states) fails across the audience lifecycle. New audiences subjected to deep Processing Mode content without prior positive affect priming (Escape/Discovery) reject it defensively. Mature, loyal audiences fed excessive Escape Mode content churn from a lack of existential depth. The system previously lacked a mechanism to neurologically "train" audiences toward depth or to track that maturity to unlock heavier content.

### Solution
FR20 implements the **Audience Maturity Lifecycle** and its associated **Audience Maturity Adapter (Adapter 8)**. This architecture fundamentally operationalizes Fredrickson's Upward Spiral: it deliberately seeds positive affect through Escape/Discovery content earlier in the lifecycle, broadening cognitive scope so heavier Processing content can land later. The engine tracks behavioral depth signals (saves, vulnerable DMs, replay rates), mathematically overriding standard calendar-time classifications (New/Developing/Loyal). This data forms `DEP-ENG-017`, which strictly governs both batch composer proportions and the JIT Assembler's psychological execution depth. 

### Scope
**In scope:**
- Stage 1: Ingestion of behavioral signals and calculation of the current Cohort Classification.
- Stage 2: Resolution of the Audience Maturity Profile (`DEP-ENG-017`).
- Stage 3: Execution of JIT Skill Assembler Adapter 8 (injecting depth constraints into SKILL.md compilation).
- Cryptographic Receipt Chain Guard checks at each transition.

**Out of scope:**
- Direct extraction APIs for Instagram/TikTok engagement metrics (relies on upstream ingestion feeds).
- Batch Composer generation execution (governs the rules, doesn't generate the batch).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-042` | Engagement Signal Feed | INPUT — Produced by FR43 (Data Analyst Agent). FR43 is responsible for computing `dm_vulnerability_ratio` and `save_to_share_ratio` from raw Publer API metrics (FR42) and writing them to DEP-ENG-042 on weekly cadence. # REVISED: Matched upstream feed with FR43. |
| `DEP-ENG-017` | Audience Maturity Profile | OUTPUT — The master cohort schema produced by the lifecycle engine. |
| `audience-maturity-adapter` | Adapter 8 | COMPILER AGENT — Reads `DEP-ENG-017` during JIT assembly to restrict or expand Emilio's depth execution. |

### Academic Grounding

This subsystem is anchored entirely in positive psychology and mortality salience research:

| Algorithm / Framework | Author | Year | Enforced Variable / Mechanism |
|---|---|---|---|
| **Broaden-and-Build Theory** | Fredrickson & Joiner | 2002 | The "Upward Spiral". Dictates `batch_allocation` sequences enforcing Escape/Discovery dominance early to create positive affect that broadens cognitive scope. |
| **Terror Management Theory** | Greenberg et al., Burke | 1986, 2010 | Dictates `tmt_function_allowed`. Worldview construction is strictly restricted to the Loyal cohort, preventing heavy worldview defense mechanics from startling New cohorts. |

### Technical Decisions
1. **Behavioral Override:** The calendar time limits (0-4wks, 4-16wks, 16wks+) are baseline fallback priors only. If behavioral depth thresholds are crossed on day 3, the engine immediately elevates the cohort to Developing. Time is subordinate to behavior.
2. **Deterministic Enums:** Every field in the output schema resolves based on strict matrix mapping. No LLM estimation is permitted for the rules themselves once the cohort tier is defined.

---

## 4. Implementation Plan

### Stage 1: Behavioral Cohort Classification
*Agent Name:* Maturity-Lifecycle-Engine
*Inputs:* `live_engagement_signals` (UPSTREAM UNDEFINED: needs producing FR).
*Outputs:* Calculated `cohort_classification` enum.
*Failure Condition:* Upstream metrics feed is entirely blank or unreachable.
*Receipt Write:* Per FR47 DEP-ENG-041 schema — # REVISED: Standardized receipt format.
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'COHORT-CLASSIFICATION',
  agent_name: 'Maturity-Lifecycle-Engine',
  timestamp }

**Decision Logic (Enum Production):**
- Evaluate the audience's aggregated behavior over a rolling 7-day window.
- *If* `save_to_share_ratio > 2.0` AND `dm_vulnerability_ratio > 0.15` -> Enum `<Loyal>` (Behavior overrides time).
- *If* `save_to_share_ratio > 1.0` -> Enum `<Developing>` (Behavior overrides time).
- *Else If* Account age > 16 weeks -> Enum `<Loyal>` (Fallback to calendar).
- *Else If* Account age > 4 weeks -> Enum `<Developing>` (Fallback to calendar).
- *Else* -> Enum `<New>`

### Stage 2: `DEP-ENG-017` Profile Resolution Gate
*Agent Name:* Maturity-Lifecycle-Engine
*Inputs:* `cohort_classification`.
*Outputs:* The 5 remaining schema variables (`batch_allocation`, `depth_permission`, `tmt_function_allowed`, `broaden_and_build_status`).
*Failure Condition:* Matrix lookup fails due to invalid cohort input string.
*Receipt Write:* Per FR47 DEP-ENG-041 schema — # REVISED: Standardized receipt format.
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'PROFILE-RESOLUTION',
  agent_name: 'Maturity-Lifecycle-Engine',
  timestamp }

**Decision Logic (Matrix Expansion):**

1. **`batch_allocation`**
   - *If* `<New>` -> Enum `{Processing: 10, Escape: 40, Discovery: 30, Status: 20}`
   - *If* `<Developing>` -> Enum `{Processing: 25, Escape: 35, Discovery: 20, Status: 20}`
   - *If* `<Loyal>` -> Enum `{Processing: 50, Escape: 20, Discovery: 15, Status: 15}`

2. **`depth_permission`**
   - *If* `<New>` -> Enum `<Surface>` (Implication phase must remain actionable and immediate).
   - *If* `<Developing>` -> Enum `<Mid>` (Implication phase connects to broader systemic issues).
   - *If* `<Loyal>` -> Enum `<Full>` (Implication phase accesses deep psychological and existential roots).

3. **`tmt_function_allowed`**
   - *If* `<New>` -> Enum `<insight_delivery_only>`
   - *If* `<Developing>` -> Enum `<insight_delivery_only>`
   - *If* `<Loyal>` -> Enum `<worldview_construction_permitted>`

4. **`broaden_and_build_status`**
   - *If* `<New>` -> Enum `<Not_yet_seeded>` (Requires Escape prime before Discovery reward).
   - *If* `<Developing>` -> Enum `<Active>` (Cognitive scope broadening in progress).
   - *If* `<Loyal>` -> Enum `<Mature>` (Ready for high Processing load without burnout).

### Stage 3: Adapter 8 Compilation Injection
*Agent Name:* Audience-Maturity-Adapter (JIT Compiler Adapter Registry)
*Inputs:* `DEP-ENG-017`.
*Outputs:* Written logic into the `SKILL.md` Block B (Pre-Generation Constraints context).
*Failure Condition:* `DEP-ENG-017` hash verification fails isolation checks.
*Receipt Write:* Per FR47 DEP-ENG-041 schema — # REVISED: Standardized receipt format.
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'ADAPTER-COMPILATION-INJECTION',
  agent_name: 'Audience-Maturity-Adapter',
  timestamp }

**Steps:**
1. Read the validated `DEP-ENG-017`.
2. Construct exact execution sentences for the generation agent. Example: `"CONSTRAINT: Your depth_permission is currently <Surface>. Do not expand the Implication Phase into deep existential or systemic commentary."`
3. Append this logic block to the `SKILL.md` assembly stream.
4. Write `AM-ADAPTER-EXEC` receipt.

---

## 5. Primary Output Schema (DEP-ENG-017)

**Schema Name:** `audience_maturity_profile.json`

```json
{
  "profile_id": "AM-20260313-001",
  "receipt_chain_hash": "mat_4b581c...",
  "tenant_id": "coach_88ab",
  "last_evaluation_epoch": 1718302111,
  "cohort_classification": "Developing",
  "classification_method": "BEHAVIORAL_OVERRIDE",
  "batch_allocation": {
    "Processing": 25,
    "Escape": 35,
    "Discovery": 20,
    "Status": 20
  },
  "depth_permission": "Mid",
  "tmt_function_allowed": "insight_delivery_only",
  "broaden_and_build_status": "Active"
}
```

*Note: Every field defined in this JSON is resolved explicitly in Stage 2 via deterministic matrix lookup. No orphans.*

---

## 6. Backward Compatibility Fallback
If the `live_engagement_signals` API feed fails (UPSTREAM UNDEFINED system is down) or the account has zero historical data (Day 1 onboarding):
1. The engine automatically defaults to the `<New>` cohort matrix configuration.
2. The `classification_method` flag is set to `CALENDAR_FALLBACK_DEFAULT`.
3. TMT function is locked to `<insight_delivery_only>` to prevent accidental over-depth. 

---

## 7. Tasks

- [ ] **Task 1:** Spec out the UPSTREAM UNDEFINED Engagement Metric Feed FR to ensure `dm_vulnerability_ratio` and `save_to_share_ratio` have a source of truth.
- [ ] **Task 2:** Implement the Stage 1 Classifier Engine, explicitly ordering the boolean checks sequence so that behavioral triggers evaluate *before* calendar age triggers.
- [ ] **Task 3:** Build the Stage 2 Expansion Matrix. Hardcode the Broaden-and-Build and TMT enumerations against the three cohort tiers.
- [ ] **Task 4:** Create the `audience-maturity-adapter` string construction logic, parsing the `DEP-ENG-017` JSON into literal constraints Emilio can comprehend during execution.
- [ ] **Task 5:** Inject Receipt Chain Guard writes across all stages, ensuring `tenant_id` matches the current workspace context (ADR-01).
- [ ] **Task 6:** Confirm DEP-ENG-042 registration with FR43 as the producing FR. Verify FR43 outputs `dm_vulnerability_ratio` and `save_to_share_ratio` as named fields in its output schema before FR20 implementation begins. # REVISED: Added verification task for FR43 payload.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Behavioral Override Rule):** Given a coach account age of exactly 2 weeks (calendar = `<New>`), where `save_to_share_ratio` jumps to 2.5, the engine outputs `cohort_classification: <Loyal>`. *Failure Example:* The engine outputs `<New>` because the calendar constraint overrides the behavioral spike.
- [ ] **AC2 (TMT Isolation):** Given a `cohort_classification` of `<Developing>`, the engine assigns `tmt_function_allowed: <insight_delivery_only>`. *Failure Example:* The engine leaks `<worldview_construction_permitted>` into the adapter, resulting in a script that pushes a developing audience into heavy existential defense mechanics before they are ready.
- [ ] **AC3 (Batch Allocation Math):** Given `<Loyal>`, the batch allocation array precisely strictly evaluates to `Processing: 50, Escape: 20, Discovery: 15, Status: 15`. *Failure Example:* The system modifies percentages randomly to create "variety", breaking the Upward Spiral mathematical ratios.
- [ ] **AC4 (ADR-01 Strict Isolation):** When evaluating behavioral signal metrics, the engine queries the isolated storage bucket unique to the authenticating coach. *Failure Example:* The engine aggregates comment vulnerability across the platform, giving a new coach access to loyal depth permissions they haven't earned.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| `DEP-ENG-042` | Upstream | Produced by FR43 Data Analyst Agent on weekly cadence. # REVISED: Connected to FR43 explicitly. |
| Batch Composition Engine | Downstream | Consumes the `batch_allocation` matrix to structure the slot feed. |
| JIT Compiler (Adapter 8) | Downstream | Consumes `depth_permission` and `tmt_function_allowed`. |
| Receipt Chain Guard | Infrastructure | Non-negotiable sequence auditing. |

---

## 10. Testing Strategy

### Unit Tests
- **Matrix Consistency Checks:** Submit static strings `New`, `Developing`, and `Loyal` directly to Stage 2. Assert that the remaining 5 JSON fields resolve perfectly to their specified enums without throwing exceptions or mapping to undefined.
- **Priority Override Test:** Provide a mock input with account age = 300 weeks AND `save_to_share_ratio` = 0.5. Assert that it falls to the calendar default (`Loyal`). Provide an input with account age = 2 days AND `save_to_share_ratio` = 2.1. Assert it outputs `Loyal`.

### Integration Tests
- **Adapter Injection Check:** Trigger a full compile of a SKILL.md for a given archetype. Retrieve the assembled Block B. Assert that the specific constraint string (e.g., `"Your depth_permission is currently <Surface>"`) exists explicitly in the Pre-Generation Constraints header section.
- **Batch Modulator Check:** Execute the batch creation orchestration loop. Verify the final synthesized batch perfectly adheres to the 10/40/30/20 proportions if the coach is classified as `<New>`.

### Safety Tests (ADR-01 & Receipt Isolation)
- **Tenant Context Bleed Check:** Simulate two coaches on the same server instance. Give Coach A huge behavioral spikes (`Loyal`) and Coach B zero engagement (`New`). Run the classifier sequentially 100 times. Confirm through cryptographic receipts that Coach B never inherits Coach A's `<Loyal>` permissions.
