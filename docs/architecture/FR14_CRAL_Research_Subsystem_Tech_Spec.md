# Tech-Spec: FR14 — CRAL 9-Skill Research Subsystem (OODA & Diagonal Method)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v4.0)
**Architecture Reference:** PRD §Layer 1, CRAL_Documentation_V1
**Skill Implementation:** `skills/ccf/research/cral-orchestrator/`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CRAL_Documentation_V1.docx.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CCP_Evolution_Architecture_Report_V4.docx.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCBS\SKILL_AUTHORING_GUIDE_V4.md`

---

## 2. Overview

### Problem Statement
Prior research architectures within the CCP suffered from the *statistical centroid failure*. Systems were fed generic prompts to execute broad domain research in advance. The language model then retrieved the synthesized average of everything known about the topic, resulting in content that was factually accurate but emotionally sterile. Research arrived in a uniform, encyclopedic register that produced persuasion (activating audience resistance) rather than discovery (activating neural coupling).

### Solution
FR14 implements the Conscious Research Alchemy Lab (CRAL) — an autonomous 9-skill research engine operating on the **Diagonal Research Method**. Controlled by an **OODA Orchestrator** (Observe, Orient, Decide, Act), CRAL does not run batch research. It executes 7 sequentially dependent moments (M1–M7). Each Moment executor is governed by a strict **Human Evidence Bias** ensuring that findings are anchored not in abstract statistics, but in a culturally verified, named human being whose story vibrates at the specific emotional register required for that stage of content assembly.

### Scope
**In scope:**
- Stage 1: The Research Orchestrator Agent (OODA loop).
- Stage 2: The Research Planner (JIT Skill Compiler).
- Stage 3: The 7 Moment Executor Skills (M1 to M7).
- Stage 4: CRAL Finding Index (`DEP-ENG-021`) Assembly and Forwarding.
- Quality gates enforcing the Human Evidence Bias parameter.
- Cryptographic Receipt Chain Guard monitoring.

**Out of scope:**
- The Telegram Intake execution mapping (upstream).
- The Archetype Assembler execution (downstream consumer of the index).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-005` | Trigger Profile | INPUT — Authentic context initiating M2 |
| `DEP-ENG-016` | Mood Context Routing | INPUT — Resolves the cognitive environment for M3 |
| [PROPOSED] `DEP-ENG-022` | Session Research Plan | INTERMEDIATE — The Orchestrator's initial firing map to drive the sequence |
| `DEP-ENG-021` | CRAL Finding Index | OUTPUT — The final 7-object array containing structured findings for the Assembler |

*Note: `DEP-ENG-022` (Session Research Plan) is PROPOSED as requested in the CRAL documentation Phase 1 roadmap.*

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Diagonal Research Method / Spiral Curriculum** | Bruner | 1960 | Research does not cycle through new topics; it sequentially deepens on the *same* topic across changing emotional registers. (L1 → L2 → L3 collision). |
| **Grounded Theory (Iterative Sampling)** | Glaser & Strauss | 1967 | Research sequence is strictly determinative. M7 cannot be researched ahead of M3 because the specific tribal anchor required at M7 depends entirely on what the previous emotion registers established. |
| **Human Evidence Bias / Neural Coupling** | Hasson | 2010 | Neural synchronization between communicators requires narrative structure anchored in specific, identifiable human subjects rather than statistical aggregates. |
| **Information Gap Theory (Productive Anomaly)** | Loewenstein | 1994 | M5 (Surprising) must target the specific "Zone of Curiosity" violation based exactly on what M3 established the audience wrongly predicts. |

### Technical Decisions
1. **Agent vs. Skill Separation:** The Research Orchestrator is classified as an **Agent** because it contains an open-ended OODA loop, manages dependency state routing dynamically, and handles error recovery. The 7 Moment Executors are passive **Skills** governed by strict 240-word signal contracts; they have no loop reasoning.
2. **Previous-Finding Exclusion Constraint:** To prevent horizontal research collapse (gathering identical facts under different framings), the Research Planner JIT compiler dynamically injects all *previous* moment findings into the LLM system prompt for the *current* moment, instructing the model to mathematically exclude overlapping data.
3. **No Celebrities Limit:** The Human Evidence bias algorithm enforces a cultural proximity radius check, programmatically rejecting entities mathematically defined as celebrities/macro-influencers to guarantee tribal resonance over parasocial distance.

---

## 4. Implementation Plan

### Stage 1: Orchestrator Loop Initialization (Observe & Orient)
*Agent Name:* Research-Orchestrator
*Inputs:* `DEP-ENG-005` (Trigger Profile), `tribe_soul.json`, `coach_soul.json`.
*Outputs:* `[PROPOSED] DEP-ENG-022` (Session Research Plan).
*Failure Condition:* Missing `tribe_soul.json` or unauthenticated `DEP-ENG-005`.

**Steps:**
1. Observe global pipeline state for trigger initiation.
2. Validate required core dependencies present.
3. Orient the state matrix: Instantiate the OODA event listener for the 7 Moment dependency checks.
4. Output the `DEP-ENG-022` (Session Research Plan) establishing the sequence blueprint.
5. Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'STAGE-1-ORCHESTRATOR-INIT',
  agent_name: 'Research-Orchestrator',
  timestamp }

### Stage 2: Research Planner Directive Generation (JIT Compilation)
*Agent Name:* Research-Orchestrator (Invoking Planner Skill)
*Inputs:* Current `DEP-ENG-021` state (Previous findings), Target Moment ID.
*Outputs:* Compiled 40-60 Word Directive Text.
*Failure Condition:* Directive generated lacks target emotional register constraints.

**Logic Gate:**
- **Exact Threshold:** Planner output length must be `40 ≤ len(words) ≤ 60`. Must contain the string constraint `human_evidence_required`.
- **Verdict: PASS:** Directive adheres to limits. Proceed to Moment Execution.
- **Verdict: PROVISIONAL:** Directive is 65 words. Downstream: Pass to Executor but flag `verbosity_warning` to the CCP Admin dashboard.
- **Verdict: FAIL:** Directive < 40 words OR lacks human evidence string. Downstream: Abort execution for this moment, loop back to Planner for regeneration. Fails session after 3 retries.
- Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'STAGE-2-RESEARCH-PLANNER',
  agent_name: 'Research-Orchestrator',
  timestamp }

### Stage 3: The 7 Moment Executors (Execute Actions)
*Agent Name:* Research-Orchestrator (Invoking specific Moment Skills 1-7 sequentially)
*Inputs:* Planner Directive, Current Moment Config (Methodology).
*Outputs:* `moment_finding` (Appended to `DEP-ENG-021`).
*Failure Condition:* Output > 260 words, or fails the moment's distinct Quality Gate (e.g., M7 missing tribal recognized token).

**Execution Sequence (Dependency Driven):**
1. **M1 RELEVANT (Digital Ethnography):** Fires immediately. Target: The cultural NOW. Quality Gate: Source must be < 4 weeks old community discourse.
2. **M2 BELIEVABLE (Precision Journalism):** Fires post `DEP-ENG-005`. Target: Substantive anchor constraint. Quality Gate: Must contain named institutional source or primary filing.
3. **M3 UNDENIABLE (Behavioral Science):** Fires post `DEP-ENG-016` (Mood Routing). Target: Prediction gap identification. Quality Gate: Must cite a study/researcher documenting the systematic error.
4. **M4 RESONANT (Narrative Journalism):** Fires post archetype selection. Target: Story structure. Quality Gate: Must contain 5 elements (protagonist, status, contact moment, shift, outcome).
5. **M5 SURPRISING (Science Journalism):** Target: Surface violation of M3 prediction. Quality Gate: Must explicitly contradict the `M3 prediction gap` within optimal incongruity limits.
6. **M6 IRREFUTABLE (Investigative Journalism):** Target: Maximum source proximity. Quality Gate: Evidence must originate internally from the mechanism's creator/institution.
7. **M7 RELATABLE (Oral History):** Fires last. Target: Exact tribal frequency match. Quality Gate: Must contain verified vernacular extraction (slang/cultural syntax native to tribe).

*Note: ADR-01 Coach Isolation dictates that the `DEP-ENG-021` index built here resides exclusively in the single-tenant coach directory space.*

### Stage 4: Assembly and Forward Passing
*Agent Name:* Research-Orchestrator
*Inputs:* Array of 7 `moment_findings`.
*Outputs:* `DEP-ENG-021` (CRAL Finding Index).
*Failure Condition:* Array length < 7.

**Steps:**
1. OODA loop detects all 7 moments have reported SUCCESS.
2. Compile individual finding JSON objects into the consolidated `DEP-ENG-021` schema.
3. Apply final `use_at` downstream mapping addresses for the Archetype Assembler.
4. Fire ready-state webhook.
5. Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'STAGE-4-INDEX-EMIT',
  agent_name: 'Research-Orchestrator',
  timestamp }

---

## 5. Primary Output Schema (DEP-ENG-021)

**Schema Name:** `cral_finding_index.json`

```json
{
  "session_id": "CRAL-SESSION-20260313",
  "coach_tenant_id": "coach_88ab",
  "receipt_chain_hash": "cral_e2e_39abff2...",
  "findings": [
    {
      "moment_id": "M1_RELEVANT",
      "emotional_register": "cultural_urgency",
      "source_discipline": "digital_ethnography",
      "human_evidence_target": "verified_community_member",
      "finding_content": "The HustleCulture subreddit pivoted over the last 14 days from 'burnout recovery' to 'algorithm taxation,' specifically led by user @BuilderDev detailing how the new feed changes directly throttle minority creators.",
      "use_at_address": "hook_context_layer",
      "quality_gate_status": "PASS"
    },
    {
      "moment_id": "M7_RELATABLE",
      "emotional_register": "tribal_recognition",
      "source_discipline": "oral_history",
      "human_evidence_target": "ordinary_tribe_member",
      "finding_content": "When they talk about this, they don't say 'systemic inequity.' They use the exact phrase 'doing the shadow ban shuffle.' Confirmed from three separate TikTok creators under 1K followers in the design space discussing feed drops.",
      "use_at_address": "recognition_layer",
      "quality_gate_status": "PASS"
    }
  ]
}
```

---

## 6. Backward Compatibility Fallback
If the CRAL subsystem encounters an API routing failure to search tools (e.g., Tavily limit exceeded), the OODA Orchestrator triggers an emergency truncation state:
1. Halt the sequential M1-M7 crawl.
2. Execute a single, condensed "Standing Trigger Intelligence" pull. This searches the localized, pre-cached Coach memory for previous M2 (Believable) and M6 (Irrefutable) anchors attached to this specific trigger.
3. Emit a degraded `DEP-ENG-021` containing only historical M2 and M6 records, with the flag `fallback_mode_invoked: true`. The downstream Assembler adapts logic for a less nuanced, but still factually grounded, content output.

---

## 7. Tasks

- [ ] **Task 1:** Implement the `Research-Orchestrator` Agent containing the rigid OODA loop state machine subscribing to dependency resolution events.
- [ ] **Task 2:** Implement the Research Planner JIT Skill module. Enforce the compilation mechanics ensuring previous findings are hardcoded into the subsequent LLM prompt constraint list (Previous-Finding Exclusion).
- [ ] **Task 3:** Implement the M1 RELEVANT Skill (Digital Ethnography). Lock source hierarchy to forums/discourse < 4 weeks old.
- [ ] **Task 4:** Implement M2 BELIEVABLE and M3 UNDENIABLE Skills. Enforce the M3 requirement to explicitly map Kahneman/Tversky prediction errors against M2 anchors.
- [ ] **Task 5:** Implement M4 RESONANT and M5 SURPRISING Skills. M4 requires strict regex checking for the 5-element narrative structure. M5 must calculate optimal incongruity.
- [ ] **Task 6:** Implement M6 IRREFUTABLE and M7 RELATABLE Skills. M6 restricted to internal institutional sources. M7 restricted to vernacular vocabulary extraction.
- [ ] **Task 7:** Register `DEP-ENG-022` and structure the serialization mechanics for `DEP-ENG-021`. Inject Receipt Chain Guard writes at Stages 1, 2, 3, and 4.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Planner Strict Generation):** If the Research Planner generates a directive containing 28 words, the system rejects it, logs the sub-limit failure, and attempts regeneration. *Failure Example Implementation:* Planner pushes a 15-word directive forward, resulting in M2 returning generic garbage statistics instead of a named event.
- [ ] **AC2 (Grounded Dependency Firing):** The Orchestrator refuses to instantiate M7 until M1-M6 have returned successful `PASS` quality gates and have written their hashes to the `DEP-ENG-021` index state. *Failure Example Implementation:* The orchestrator fires all 7 moments simultaneously as a batch prompt, completely destroying the iterative diagonal path.
- [ ] **AC3 (Human Evidence Gate - Celebrity Rejection):** If M4 identifies a story where the protagonist maps to a systemic entity tagged `is_celebrity == true` (e.g., Elon Musk), the M4 Quality Gate returns `FAIL` and mandates regeneration targeting a local/vernacular entity. *Failure Example Implementation:* M4 outputs a story about Steve Jobs, destroying tribal neural coupling due to parasocial distancing.
- [ ] **AC4 (240-Word Signal Contract):** Any Moment Executor producing a finding block containing 350 words immediately trips a length limit exception, forcing the distillation toolchain to rewrite the prompt. *Failure Example Implementation:* M6 dumps an unedited 800-word SEC 10-K filing text block into the index, flooding the downstream Assembler context window.
- [ ] **AC5 (ADR-01 Coach Graph Isolation):** The final emitted `DEP-ENG-021` index is cryptographically signed and stored strictly within the path parameters mapped to `coach_tenant_id`. *Failure Example Implementation:* An M4 resonant story gathered for Coach A is accidentally cached into the global index and utilized verbatim by Coach B.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| `DEP-ENG-005` (Trigger Profile) | Upstream | Required condition for M2 execution. |
| `DEP-ENG-016` (Mood Router) | Upstream | Required parameter constraint for M3 execution. |
| Tavily / Web APIs | System | Required for live ethnographic/journalistic scraping. |
| Receipt Chain Guard Engine (DEP-ENG-041, FR47) operating under Protocol DEP-PROTO-010 (FR21) | Infrastructure | Non-negotiable sequence auditing. |

---

## 10. Testing Strategy

### Unit Tests
- **Planner Constraint Validation:** Inject a live state object containing previous M2 findings. Guarantee the generated M3 directive string explicitly instructs the subagent: `"DO NOT return findings repeating [M2 Target]."`.
- **M4 Narrative Gate Test:** Provide a paragraph containing only 3 of 5 narrative elements (missing outcome and status details). Verify the regex/LLM validation gateway catches the `FAIL` condition accurately.

### Integration Tests
- **Diagonal Flow Integrity:** Mock the dependency fulfillment signal for `tribe_soul`. Assert that the OODA loop successfully fires M1, waits for completion, updates state, and holds M2 in queue until `DEP-ENG-005` is injected by the test runner.
- **Search Tool API Failure Simulation:** Manually sever the outbound network connection to the Tavily/Search API endpoints mid-session (during M4). Track the orchestrator event loop catching the HTTP timeout and perfectly cascading into the Backward Compatibility Fallback sequence to retrieve cached Standing Trigger Intelligence.

### Safety Tests (ADR-01 & Receipt Isolation)
- **Cross-Tenant OODA Isolation:** Spin up two simultaneous Research Orchestrators mapped to `Coach_A` and `Coach_B`. Analyze global cache and Receipt Chain hashes to guarantee `Coach_A`'s M1 ethnographic search term execution never shares memory pointers or state objects with `Coach_B`'s timeline.
