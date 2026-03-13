# Tech-Spec: FR11 — Activation Event Seed Construction

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v3.1)
**Architecture Reference:** §Context_Premise_Trigger_Matching_Layer Part 4 Component 2, §Trigger-First Engine Architecture v3.0 Part 2
**Skill Implementation:** `skills/ccf/production/activation-seed-builder/SKILL.md`

---

## Overview

### Problem Statement

The Four-Axis Structural Matching Engine (FR10) confirms the coordinates of structural congruence between a coach's formative experience (Trigger Map, DEP-LIB-002) and an audience's L3 pain (Context Premise Map, DEP-ENG-006). However, knowing *where* the overlap exists is not enough to produce biological authenticity in the resulting content. 

If the system hands the coach a topic to speak about (e.g., "The audience is feeling financial shame because of institutional failure"), the coach will engage in **semantic synthesis**. They will construct a narrative filtered through their current "Working Self" (Conway 2005) and social context, prioritizing coherence and professional messaging over raw episodic truth. The resulting content will be conceptually accurate but neurologically sterile.

To achieve **episodic invocation** — forcing the coach back into the original autonoetic consciousness of their formative experience (Tulving 1985) — the system must open a memory reconsolidation window (Nader 2000). This requires an activation event that simultaneously anchors into the coach's specific sensory reality, speaks the audience's exact L3 tribal language sub-cortically, and articulates the precise structural match. Furthermore, if this event is not phrased within an evocative architecture, the coach will simply agree with it rather than activating their dual-layer encoding.

### Solution

FR11 implements the **Activation Event Seed Construction** pipeline. It takes confirmed four-axis matches from FR10 and synthesizes them into precise invocation events.

An Activation Event Seed is constructed from three mandatory elements:
1. **The Coach's Event-Specific Knowledge (ESK) Anchor:** Sensory-perceptual records from the specific moment of trigger formation.
2. **The Audience's L3 Tribal Language:** A minimum of 3 verified tribal terms that failed the genericness test (FR9 Law 3).
3. **The Structural Congruence Point:** The exact intersection of the four matched axes (Moral Foundation, Coping Pattern, Agency Attribution, Temporal Position).

These three elements are forged into an evocative question using the **DARN-CAT architecture** (Miller & Rollnick Motivational Interviewing), specifically targeting the **Taking Steps** (behavioral specificity) and **Reasons** (moral foundation surfacing) dimensions. The system enforces strict Language Drift Prevention to ensure the seed is not abstracted or translated out of the tribe's native dialect before transmission to the Telegram Elicitation Protocol.

**Output artifacts:**
- `intelligence/matching/{theme_slug}_activation_seeds.json` — The final array of validated, DARN-CAT-formatted activation seeds ready for the Telegram Elicitation Protocol.

### Scope

**In scope:**
- Ingestion of confirmed or strong four-axis matches from FR10.
- ESK anchor extraction and quality grading (full vs. degraded).
- Tribal language retrieval and 3-term minimum validation (Language Drift Prevention).
- Structural congruence point articulation.
- DARN-CAT evocative question formulation (Taking Steps and Reasons dimensions).
- Serialization of the Activation Event Seed into the `activation_events` payload.

**Out of scope:**
- The Four-Axis Structural Matching Engine (FR10 — upstream producer).
- Extraction of Emotional DNA and Trigger Maps (FR4/FR5 — upstream producers).
- Audience Empathy Agent theme generation (FR9 — upstream producer).
- Telegram Elicitation Protocol (downstream consumer — execution of the seed).

---

## Context for Development

### Architecture Traceability

| DEP-ID | Name | Role in This Pipeline |
|---|---|---|
| `DEP-LIB-002` | Trigger Map | INPUT (via FR10 Match) — Source of the `origin.akb_level` (ESK) and sensory anchors required for Element 1 |
| `DEP-ENG-006` | Context Premise Map | INPUT (via FR10 Match or FR9 output) — Source of the verified L3 tribal language terms required for Element 2 |
| `DEP-ENG-010` | Four-Axis Match Object | INPUT — The confirmed or strong structural intersections defining Element 3 |
| `DEP-ENG-011` | Activation Event Seed | OUTPUT — The final DARN-CAT formulated invocation prompt |

### Academic Research Grounding

| Requirement | Framework | Key Insight | Lab Reference |
|---|---|---|---|
| **ESK Anchoring** (Element 1) | Conway (2005) Autobiographical Knowledge Base (AKB) | Only Event-Specific Knowledge (ESK) contains sensory-perceptual records. General Events (GE) and Lifetime Periods (LP) produce semantic summaries, not episodic retrieval. | [Memory Retrieval vs. Semantic Construction](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Trigger%20Map%20Flow/Memory%20Retrieval%20vs.%20Semantic%20Construction.md) |
| **Prediction Error** | Nader (2000) Memory Reconsolidation | Topic prompts do not labilize a trace. Specific ESK triggers generate the prediction error required to open the reconsolidation window, reconstructing the original emotional architecture. | [Memory Retrieval vs. Semantic Construction](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Trigger%20Map%20Flow/Memory%20Retrieval%20vs.%20Semantic%20Construction.md) |
| **Tribal Language** (Element 2) | Pennebaker LIWC-22 Authenticity | Abstracted or professionalized language shifts processing to the cortex. Exact L3 tribal language bypasses intellectual filters, achieving sub-cortical recognition (the "2am test"). | [Verified L3 Data Through Digital Ethnography](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/Context%20Premises/Verified%20L3%20Data%20Through%20Digital%20Ethnography.md) |
| **DARN-CAT Expression** | Miller & Rollnick (2012) Motivational Interviewing | "Taking Steps" demands behavioral specificity. "Reasons" forces the coach to express their driving moral foundation rather than just listing facts. | [Context_Premise_Trigger_Matching_Layer](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/CCP%20update/Context_Premise_Trigger_Matching_Layer.md) §Part 4 |

### Technical Decisions

| Decision | Rationale |
|---|---|
| **Reject seeds with < 3 verified tribal terms** | Language Drift Prevention. If the seed is constructed from audience L3 intelligence but rewritten into generic coaching language, the activation event loses its sub-cortical recognition signal. It becomes a prompt any marketer could have written. Seeds failing this gate must be reconstructed. |
| **Flag, but do not reject, GE/LP anchors** | An ESK anchor is mathematically necessary for autonoetic invocation. However, some coaches have unpolished Trigger Maps (`origin.akb_level` = `general_event`). The engine constructs the seed but flags it as `degraded_anchor`. The resulting content is expected to be thematic rather than biological, and the flag informs the feedback loop to request a deep-dive interview to harvest sensory anchors for that trigger. |
| **Enforce DARN-CAT "Taking Steps" or "Reasons" only** | Elements like "Desire" or "Need" lead the coach into theoretical or persuasive posturing. "Taking Steps" grounds them in specific actions they took during the ESK moment. "Reasons" grounds them in the moral foundation violation they experienced. Both force episodic grounding. |
| **Express the structural congruence point explicitly** | The seed does not just ask a question; it positions the coach in relation to the audience. "The audience is currently [X] because [Y]. You were in this exact position when [Z]..." This establishes the Clark & Brennan Common Ground required for neural coupling. |

---

## Implementation Plan

### Phase 1: INGESTION & VALIDATION

**Steps:**
1. Ingest the `match_results.json` payload generated by FR10.
2. Filter the array to process ONLY matches with `match_classification == "CONFIRMED"` or `match_classification == "STRONG"`. (Explicitly exclude `ADJACENT` matches).
3. **Graceful Exit Gate:** If the filtered array length is 0 (i.e., FR10 produced zero valid structural matches), abort seed construction. 
   - Write `status: graceful_exit_zero_matches` to the pipeline monitor.
   - Output an empty `activation_seeds.json` array with the `graceful_exit` flag explicitly set to `true`.
   - Pipeline skips to Telegram Elicitation fallback protocol (if configured) rather than throwing an error.
4. Validate upstream data for selected matches:
   - Ensure `elements.esk_anchor.sensory_details` exists (from FR5 `trigger_map.json`).
   - Ensure the source FR9 Context Premise segment is available to pull verified `tribal_terms[]`.
5. Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'PHASE-1-INGEST',
  agent_name: 'Activation-Seed-Builder',
  timestamp }

---

### Phase 2: ELEMENT SYNTHESIS

For each valid match, assemble the three core elements required for seed construction.

#### Element 1: ESK Anchor Extraction
1. Examine the matched coach trigger in the Trigger Map (DEP-LIB-002).
2. Look for `origin.akb_level`.
3. If `esk` (Event-Specific Knowledge): Extract `origin.sensory_anchors` and set `anchor_quality: "full"`.
4. If `general_event` or `lifetime_period`: Extract available context but set `anchor_quality: "degraded"`. Add flag: `requires_esk_harvesting`.

#### Element 2: L3 Tribal Language Selection
1. Access the specific audience segment(s) involved in the FR10 match (within the FR9 Context Premise).
2. Gather all verified `tribal_terms` from the categories that contributed to the structural match (Hidden Beliefs, Emotional Triggers, Coping Mechanisms, Enemies/Suspicions).
3. Select a minimum of 3 terms that contextually align with the structural congruence point.

#### Element 3: Structural Congruence Point Articulation
1. Read the FR10 axis scores for the match.
2. Formulate a declarative statement combining the four axes:
   * **Moral Foundation:** The shared violation (e.g., "betrayal of institutional care").
   * **Coping Pattern:** The shared defense mechanism (e.g., "seeking validation through hyper-independence").
   * **Agency Attribution:** The shared enemy (e.g., "blaming the algorithm").
   * **Temporal Position:** The audience's pre-PTG state vs. the coach's post-PTG anchor.

---

### Phase 3: DARN-CAT FORMULATION (The Prompt Engine)

Pass the three synthesized elements into the prompt generator to yield the Activation Event Seed in DARN-CAT architecture.

**The Prompt Schema:**

1. **The Grounding Statement (Element 3 & Element 2):** Define the audience's exact position using their language.
   * *Example:* "Your audience is currently exhausted because they feel entirely responsible for their stalling growth (Internal Agency), even though the system is rigged against them (Liberty/Oppression violation). They are caught in a cycle of [tribal term 1] and [tribal term 2], trying to [tribal term 3] their way out (Coping Pattern)."
2. **The Episodic Bridge (Element 3 & Element 1):** Connect their position to the coach's specific ESK memory.
   * *Example:* "You were standing in this exact intersection when you [ESK Sensory Anchor: e.g., received that email from the publisher in your kitchen at 3 AM]."
3. **The Evocative Question (DARN-CAT Taking Steps / Reasons):** End with an invocation that forces autonoetic retrieval.
   * *Taking Steps Example:* "When you felt that specific betrayal in your kitchen, what was the very first physical step you took to break the [tribal term 1] cycle before your 'path out' was clear?"
   * *Reasons Example:* "In that specific moment, why was the violation of [tribal term 2] more painful than the failure itself?"

---

### Phase 4: LANGUAGE DRIFT PREVENTION (Gate 2)

**Steps:**
1. Post-generation, analyze the `question_text` string of the constructed Activation Event Seed.
2. Perform a string matching/NLP evaluation against the FR9 Context Premise verified tribal terms registry for that segment.
3. Count the exact (or structurally equivalent) verified terms present in the output text.
4. **Logic Gate:**
   - If count ≥ 3: `language_drift: false`. Proceed to Phase 5.
   - If count == 1 or 2: `language_drift: warning`. Flag the seed, but proceed to Phase 5.
   - If count == 0: `language_drift: critical`. Reject the seed. Loop back to Phase 3 and regenerate with an explicit overriding instruction to inject the target tribal terms. Output failure if regeneration fails 3 times.
5. Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'PHASE-4-LANGUAGE-DRIFT-GATE',
  agent_name: 'Activation-Seed-Builder',
  timestamp }

---

### Phase 5: SEED SERIALIZATION & EMIT

**Steps:**
1. Compile the verified seed into the `DEP-ENG-011` schema.
2. Determine `priority_rank` based on: (1) FR10 match score, (2) `anchor_quality` (full > degraded), (3) tribal term count.
3. Output `intelligence/matching/{theme_slug}_activation_seeds.json`.
4. Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'PHASE-5-EMIT',
  agent_name: 'Activation-Seed-Builder',
  timestamp }
5. Fire ready-state webhook for downstream Telegram Elicitation Protocol consumption.

**Seed Output JSON Schema:**

```json
{
  "seed_id": "SEED-{theme_slug}-{trigger_id}-{segment_id}",
  "match_classification": "CONFIRMED",
  "match_score": 4.0,
  "priority_rank": 1,
  "elements": {
    "esk_anchor": {
      "akb_level": "esk",
      "sensory_details": ["3 AM kitchen", "publisher email on iPhone"],
      "anchor_quality": "full"
    },
    "tribal_language": {
      "extracted_terms": ["shadow banning", "algorithm tax", "hustle guilt"],
      "verified_count": 3,
      "language_drift_status": "passed"
    },
    "structural_congruence_point": "Both coach and audience experience algorithm tax (attribution) violating fairness (moral), triggering hustle guilt (coping)."
  },
  "activation_event": {
    "darn_cat_dimension": "taking_steps",
    "prompt_text": "Your audience is feeling blocked by the 'algorithm tax' and trapped in 'hustle guilt'. You were in this exact position when you read that publisher email in your kitchen at 3 AM, dealing with the exact same 'shadow banning' fear. When you felt that betrayal, what was the very first step you took to break the cycle before your PTG resolution was clear?",
    "tribal_terms_used": ["algorithm tax", "hustle guilt", "shadow banning"]
  },
  "flags": {
    "degraded_anchor": false,
    "language_drift_risk": false
  }
}
```

---

## Tasks

- [ ] **Task 1:** Implement Phase 1 Ingestion Logic. Parse FR10 `match_results.json` and isolate `CONFIRMED` and `STRONG` matches. Ensure `ADJACENT` matches are completely dropped from the queue. Implement the Graceful Exit state if the queue is empty, logging the graceful exit state and producing an empty output JSON. Log Receipt Chain.
- [ ] **Task 2:** Implement Element 1 Extraction. Map the coach trigger ID to the Trigger Map (DEP-LIB-002). Pull `sensory_anchors` and evaluate `akb_level`. Set `anchor_quality` flag (`full` vs `degraded`).
- [ ] **Task 3:** Implement Element 2 Extraction. Map the matched audience segment to the FR9 Context Premise. Extract L3 tribal terms from structurally relevant categories (Enemies, Coping, Emotional Triggers, Hidden Beliefs).
- [ ] **Task 4:** Implement Element 3 Articulation. Write the logic that translates FR10 axis scores into a coherent structural congruence array (Moral + Coping + Agency + Temporal).
- [ ] **Task 5:** Build the Prompt Engine (Phase 3). Implement the prompt generation template utilizing DARN-CAT "Taking Steps" and "Reasons" dimensional structures, assembling Elements 1, 2, and 3 into the final text.
- [ ] **Task 6:** Implement the Language Drift Prevention Gate (Phase 4). Scan the generated `prompt_text` for the verified L3 tribal terms. Implement the ≥3 pass, 1-2 warning, 0 reject-and-regenerate logic.
- [ ] **Task 7:** Implement Seed Priority Ranking. Sort the final array of valid seeds by FR10 Match Score (primary), Anchor Quality (secondary), and Tribal Term Count (tertiary).
- [ ] **Task 8:** Serialize Output (Phase 5). Generate `intelligence/matching/{theme_slug}_activation_seeds.json` matching the specified JSON schema.

---

## Acceptance Criteria

- [ ] **AC1 (Match Filtration):** The system successfully loads an FR10 match payload and explicitly excludes all matches marked `ADJACENT` or `NO_MATCH`. Seed construction only occurs for `CONFIRMED` and `STRONG` match values.
- [ ] **AC2 (ESK Anchor Evaluation):** A coach trigger mapping to an `esk` origin AKB level is correctly tagged with `anchor_quality: "full"`. A general event mapped trigger is tagged `anchor_quality: "degraded"` but successfully produces a seed.
- [ ] **AC3 (Structural Output):** The generated JSON output successfully articulates the `structural_congruence_point` text, proving the overlap between the coach's V3/V5/Moral profile and the audience's enemies/coping mechanics.
- [ ] **AC4 (DARN-CAT Enforcement):** The resulting `prompt_text` can be validated as either a "Taking Steps" or "Reasons" architectural question, demanding a specific behavioral or moral response regarding the sensory anchor context.
- [ ] **AC5 (Language Drift Rejection):** If the prompt generation engine outputs an Activation Event Seed containing 0 verified L3 tribal terms, the system rejects the output and triggers a regeneration loop.
- [ ] **AC6 (Language Drift Verification):** The final JSON payload accurately calculates the `tribal_term_count` in the resulting prompt and logs the exact terms used inside `activation_event.tribal_terms_used[]`.
- [ ] **AC8 (Graceful Exit):** Upon ingesting a `match_results.json` file that contains 0 valid structural matches (all matches evaluating to ADJACENT or NO_MATCH), the engine gracefully aborts `SEED CONSTRUCT` processes, writes a `graceful_exit_zero_matches` state to the pipeline logs, and emits an empty array with the `graceful_exit: true` flag set, rather than timing out or throwing an error format.
- [ ] **AC9 (Receipt Chain Auditing):** The system successfully submits cryptographically verified receipts to the Receipt Chain Guard at Phase 1 Ingest, Phase 4 Language Drift Validation, and Phase 5 Final Emit.

---

## Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR10 Four-Axis Engine | Upstream producer | Provides the confirmed `match_results.json` and axis scores |
| FR5 Trigger Map (DEP-LIB-002) | Data Source | Provides the specific `origin` sensory anchors for the triggers matched in FR10 |
| FR9 Context Premise (DEP-ENG-006) | Data Source | Provides the verified L3 tribal language registry |
| Telegram Elicitation Protocol | Downstream consumer | The delivery mechanism that will present this seed to the coach |
| Receipt Chain Guard Engine (DEP-ENG-041, FR47) operating under Protocol DEP-PROTO-010 (FR21) | Infrastructure | Handles receipt storage for verification tracking at Ingest, Gate Pass, and Emit |

---

## Testing Strategy

### Unit Tests
- **Anchor Grading Logic:** Test input trigger with `akb_level: "general_event"` -> assert `anchor_quality === "degraded"`. Test input with `akb_level: "esk"` -> assert `anchor_quality === "full"`.
- **Match Ingestion:** Feed a payload of 1 CONFIRMED, 1 STRONG, and 2 ADJACENT matches. Assert the pipeline processes exactly 2 seeds and drops the 2 adjacent matches.
- **Language Drift Scanning:** Feed a mocked prompt string "They are struggling with hustle guilt." with a term registry of `["hustle guilt", "shadow ban", "grind"]`. Assert `verified_count === 1` and status is `warning`. Feed a prompt string with 0 matches. Assert status is `critical` and reject triggered.

### Integration Tests
- **Full Seed Generation:** Provide a mocked FR10 match object, a mocked Trigger Map entry (with 2 sensory anchors), and a mocked FR9 segment (with 5 tribal terms). Execute pipeline. Assert the output JSON matches the schema, contains a DARN-CAT prompt, and successfully incorporated the sensory anchors and ≥3 tribal terms.
- **DARN-CAT Prompt Override Loop:** Force the prompt engine to fail the language drift test by omitting terms. Assert the system loops, applies the override injection prompt, and issues a passing seed on the subsequent attempt.
