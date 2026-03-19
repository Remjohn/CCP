# Tech-Spec: FR24 — Autonomous Weekly CCF Pipeline v3.1 (DEP-PROTO-014)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 3.1 
**Architecture Reference:** PRD §Weekly Pipeline, JIT_Skill_Compiler_Architecture
**Skill Implementation:** `orchestration/ccf-weekly/` & `orchestration/ccf-batch/`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\JIT_Skill_Compiler_Architecture.docx.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\prd TO UPDATE.md`

---

## 2. Overview

### Problem Statement
In architectures migrating from single-script prompting to mass-production pipelines, human intervention points create catastrophic bottlenecks. The CCP must produce 36 finalized scripts spanning 14 distinct content formats per coach within a tight weekly production window. If the transition between RAG deep research, provocation engineering, emotional DNA extraction, and JIT Compilation requires manual CLI orchestration, volume scalability is unachievable, and the system fails its core operational mandate.

### Solution
FR24 formalizes the **Autonomous Weekly CCF Pipeline v3.1 (DEP-PROTO-014)**. This protocol governs the Master Orchestrator (Agent: Alex) in coordinating the execution of 65 distinct agents across the 5 Phases of the Trigger-First Architecture. The engine programmatically fires sequence commands (`ccf-radar` -> `ccf-trigger-match` -> `ccf-soc` -> `ccf-visual-assets`), managing the RAG memory buffers, error retries (`TillDone`), and asynchronous parallel compilation (via `TeamOrchestrator`).

### Scope
**In scope:**
- Stage 1: Phase A (Discovery & Tracking).
- Stage 2: Phase B (Trigger-First Ideation).
- Stage 3: Phase C (Research Briefs & Core Script Assembly).
- Stage 4: Phase D (Visual Direction & Critic Validation).
- Receipts logging per phase.

**Out of scope:**
- Initial `ccf-init` Genesis onboarding.
- Direct posting to social media algorithms.

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Command | Name | Role in This Pipeline |
|---|---|---|
| `ccf-weekly` | Weekly Production Script | EXECUTION — The root CRON-driven command that kicks off the 5-phase orchestration loop. |
| `Alex` | Content Orchestrator Agent | AGENT — The master controller executing conditional logic between commands. |
| `DEP-ENG-022` | CRAL Session Research Plan | INPUT — Read during Phase A discovery to guide trend extraction. |
| `trigger_map.json` | Coach Permanent Triggers | INPUT — Cross-referenced during Phase B to generate the coach's prompt. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Selective Accuracy in Memory** | Kensinger | 2007 | High arousal emotional events trigger highly selective narrative encoding. Used to justify the v3.1 pipeline inversion: finding the coach's trigger *before* selecting the topic theme. |
| **Agent Skill Networking** | Liang et al. | 2026 | Composable agent networking allows deep parallel execution without losing coherence when explicitly governed by state protocols. |

### Technical Decisions
1. **The v3.1 Inversion (Trigger-First):** The orchestrator no longer gathers trending internet topics and asks the coach to respond. Phase B now executes `ccf-trigger-match` first—mapping audience L3 pain to the coach's `trigger_map.json` to find structural overlaps. Topical trends are subordinated to authentic triggers.
2. **DamageControl Infinite Loop Breaker:** The `DamageControl` Pi Extension operates inside the Async Batch window. To prevent infinite internal retry loops blocking the scheduled chron job, the maximum retry depth for `DamageControl` is capped at `max_retry_depth=3`. If CRAL logic or gate failure forces a fourth retry, the job is killed, marked `FAILED_UNRECOVERABLE`, and escalated to the System Operator.
3. **Ghost Variable Prevention Gate:** All input sources [DEP-ID] must be verified cryptographically prior to payload unpacking. Any field resolving to NULL or UNDEFINED triggers a hard compiler pipeline halt. The error schema emitted is: `{ "error": "DAG_VIOLATION", "missing_dep": "[DEP-ID]" }`
4. **JSON Contract Absolute Boundary:** Cross-department communication relies strictly on JSON payloads. To prevent parser ambiguities, the `TeamOrchestrator` implements `pydantic`/`zod` strict schema validation at the memory bus boundary. If a generated mapping field contains an ambiguous array struct or violates the type schema, the bus throws an instantaneous `SCHEMA_TYPE_ERROR` before the downstream agent receives the message.
5. **Rolling Deployment Patch Mutex:** The Pi Coding Agent manages deployments across the fleet of single-tenant instances. When an architectural core patch is deployed, the `Global_Write_Mutex` locks new weekly batch invocations. The maximum safe deployment window for a rolling pipeline patch is strictly 2 hours. Unpatched instances attempting to process `ccf-weekly` are held in `PENDING_UPGRADE` until the mutex unlocks.

---

## 4. Implementation Plan

### Stage 1: Phase A — Discovery & Trigger Matching
*Agent Name:* Alex (Master Orchestrator) calling Adele & Divine
*Inputs:* `DEP-ENG-022` (CRAL Index), `trigger_map.json`, `tribe_soul.json`.
*Outputs:* `final_theme_selection.md`, `trigger_matching_candidates.json`
*Failure Condition:* `ccf-radar` fails to pull API trends resulting in an empty state vector.
*Receipt Write:* Per FR47 DEP-ENG-041 schema — # REVISED: Standardized receipt format.
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'DISCOVERY-AND-TRIGGER-MATCHING',
  agent_name: 'Alex-Adele-Divine',
  timestamp }

**Steps:**
1. Alex invokes `ccf-radar` (Adele) to scan Google Trends + Firecrawl via `InteractComp`.
2. Alex invokes the NEW v3.1 step: `ccf-trigger-match`. This module executes a 2-axis structural mapping (MFT + Temporal) between the extracted trend vectors and the coach's `trigger_map.json`.
3. Alex invokes `ccf-question` (Lila) to formulate the exact provocation keys targeting the coach's DARN-CAT dimensions.
4. Output is formatted into an 80-word Telegram Provocation and sent to the Coach.

*(Pipeline pauses asynchronously waiting for Coach Audio Note)*

### Stage 2: Phase B — Authenticity Gate & Research Synthesis
*Agent Name:* Alex calling Valeriane, Lionel, & Maeva
*Inputs:* Coach Voice Note (Telegram Webhook).
*Outputs:* `coach_authentic_transcript.json`, 40-page RAG library (`ccf-raw-research`).
*Failure Condition:* Coach's audio note fails the LIWC-22 Authenticity Gate (<0.6 threshold).
*Receipt Write:* Per FR47 DEP-ENG-041 schema — # REVISED: Standardized receipt format.
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'AUTHENTICITY-GATE-RESEARCH',
  agent_name: 'Alex-Valeriane-Lionel-Maeva',
  timestamp }

**Steps:**
1. The Voice Agent transcribes the incoming audio (`core/transcription.py`).
2. Alex runs the `LIWC-22 Authenticity Gate` evaluating 7 authenticity markers. If the coach sounds generic or "performed," the system immediately rejects the audio and asks them to re-record with more edge.
   - On LIWC-22 rejection: # REVISED: Added missing rejection receipt block
     Receipt Write: Per FR47 DEP-ENG-041 schema —
     { stage_name: 'VOICE-NOTE-QUARANTINE',
       rejection_reason: 'LIWC_BELOW_THRESHOLD',
       coach_id, session_id, timestamp }
     Flag coach via Telegram re-record request.
     Pipeline halts at this stage until re-submission.
3. If `<PASS>`, Alex triggers `ccf-raw-research` (Lionel) and `ccf-research-deep` utilizing the new Authentic Transcript as the grounding context for the RAG search.

### Stage 3: Phase C — JIT Compilation Mass-Assembly
*Agent Name:* Alex calling `ccf-produce` and `ccf-generate`
*Inputs:* `ideas.json`, `archetype_assignments.json`
*Outputs:* 36 Finalized `SKILL.md` variations across 14 archetypes.
*Failure Condition:* Generation agent Emilio crashes due to context window limits during batch generation.
*Receipt Write:* Per FR47 DEP-ENG-041 schema — # REVISED: Standardized receipt format.
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'JIT-COMPILATION-MASS-ASSEMBLY',
  agent_name: 'Alex-ccf-produce-ccf-generate',
  timestamp }

**Steps:**
1. Alex invokes `ccf-analyze` (Emilio) yielding exactly 12 Core Ideas mapped through `PatternWeaver`. **(Epsilon-Greedy Routing Floor: The weighting algorithm enforces a hard `<0.05>` probability floor. This guarantees a 5% random-chance selection rate for testing underperforming structural mechanisms against future audience drift.)**
2. Alex invokes `ccf-eroll-plan` delegating format assignments.
3. Alex hands the orchestration loop to the `TeamOrchestrator` extension, fanning out horizontally. It invokes `ccf-soc` (Charlotte) and `ccf-generate` (Script Artisan) to execute the JIT compilation rules across all 36 slots in parallel.
4. **C-11 Persona Masking Gate:** Before the TeamOrchestrator dispatches any JSON payload to the API executing layer, the payload must pass through Gate C-11. This gate executes an aggressive regex scrub across all prompt fields, stripping the 65 agent names (e.g., `Emilio`, `Charlotte`) and roleplay instructions (e.g., `Act as`, `You are an expert`). Any hit results in an orchestration HALT. The API receives ONLY the unadorned JSON state array to permanently prevent centroid architectural drift.
5. Validates all Anti-Draft constraints (FR22).

### Stage 3B: Novelty Validation (Agent Grâce) # REVISED: Inserted Agent Grace Novelty check
*Agent:* Grâce (Boredom Ban Enforcer)
*Input:* Compiled SKILL.md output from Stage 3
*Output:* NOVELTY_PASS or NOVELTY_FAIL verdict
*Failure Condition:* Thematic, structural, or semantic repetition detected within 8-week rolling window
*Receipt Write:* Per FR47 DEP-ENG-041 schema —
{ stage_name: 'NOVELTY-VALIDATE',
  agent: 'Grace', input_payload_hash, 
  output_payload_hash, timestamp }

**Logic:**
- PASS → proceed to Stage 4 Validation (FR26)
- FAIL → route to TillDone rewrite cycle
  If TillDone fails 3 iterations → see Stage 3C below

### Stage 3C: Reference Template Fallback # REVISED: Inserted Fallback protocol
*Trigger:* Script fails 3 TillDone iterations
*Agent:* JIT Compiler Orchestrator
*Action:*
1. Query FR23 Fingerprint Archive for the most recent AUTHENTICATED script matching this slot's archetype AND mood_state classification
2. Retrieve that script as the slot's output
3. Set generation_status: REFERENCE_FALLBACK in the Skill Fingerprint ID for this slot
4. Proceed to Stage 4 Validation — batch count maintained at 36
*Receipt Write:* Per FR47 DEP-ENG-041 schema —
{ stage_name: 'REFERENCE-FALLBACK',
  fallback_fingerprint_id, slot_id, timestamp }

### Stage 4: Phase D — Visual Routing & Critic Validation
*Agent Name:* Alex calling Abel, Paradoxe, and the Validation Triad (Sophia, Marcus, Chen)
*Inputs:* 36 compiled scripts.
*Outputs:* `visual_prompts.json`, Validated Batch File.
*Failure Condition:* Marcus (Protocol Validator) rejects a script for violating the 30-Day Season Mandate, and 3 rewrite attempts all fail.
*Receipt Write:* Per FR47 DEP-ENG-041 schema — # REVISED: Standardized receipt format.
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'VISUAL-ROUTING-CRITIC-VALIDATION',
  agent_name: 'Alex-Abel-Paradoxe-Triad',
  timestamp }

**Steps:**
1. Alex invokes `ccf-visual-assets` (Aurore + Paradoxe) generating specific DALL-E / Excalidraw JSON payloads mapped to the script beats. **(Authoritative TIAR Override: Abel's downstream TIAR query is absolute authority. If a tribal noun bleaches mid-flight, Gate V-01 halts Abel, logs `LATE_STAGE_BLEACHING`, and routes only that specific sentence back to Emilio for a micro-replace.)**
2. Alex invokes `ccf-validate` feeding the batch into the Critic subsystem.
3. **The Validation Triad:**
   - *Sophia* (Soul Validator): Checks TTT drift against `coach_soul.json` (>85% alignment).
   - *Marcus* (Protocol Validator): Checks compliance with the current 30-Day Movement Season (e.g. *The Forge* vs *The Water*).
   - *Chen* (Mimicry Validator): Employs zero-shot scoring to detect AI template bleed (<5% allowed).
4. **Gate V-00a (Narrative Arc Conformation):** Sophia maps the iRAV emotional peaks of the generated text to deduce the actual utilized structure. She compares this measured trajectory against the `arc_type` declared by the orchestrator in Block A. If there is a mismatch (e.g., text is *Tension-Release* but declared *Contrast-Resolution*), Abel halts. The script is rejected to `TillDone` for a structural rewrite. Visual production NEVER commences on misaligned arcs.
5. If `<FAIL>`, trigger `TillDone` rewrite. If `<PASS>`, append to the `ccf-batch` archive.

---

## 5. Primary Output Schema (The Final Batch Payload)

**Stewardship Escalation Protocols (Output hooks):**
1. *Neo4j Conflict Hook:* If PatternWeaver synthesizes a connection that contradicts an existing L3 Context Premise in the Neo4j graph during output packaging, it NEVER overwrites the graph. It generates an `Aria Conflict Hook`, pausing compilation and requiring human arbitration via Telegram.

**Schema Name:** `weekly_production_batch_v3.json`

```json
{
  "production_week": "2026-W11",
  "coach_id": "EMI",
  "trigger_match_score": 0.88,
  "authenticity_liwc_composite": 0.74,
  "season_mandate": "THE_FORGE",
  "receipt_chain_ledger": {
    "phase_A_discovery": "hash_a_123...",
    "phase_B_research": "hash_b_456...",
    "phase_C_generation": "hash_c_789...",
    "phase_D_validation": "hash_d_012..."
  },
  "outputs": {
    "total_generated": 36,
    "formats_utilized": 14,
    "scripts": [
      {
        "skill_id": "SKILL-STORY01-EMI-P-PRV-DEV-20260315-001",
        "archetype": "Achievement Story",
        "validation_scores": {
          "sophia_ttt": 0.92,
          "marcus_protocol": 1.0,
          "chen_mimicry": 0.02
        },
        "file_path": "/outputs/W11/STORY01_EMI.md"
      }
    ]
  }
}
```

---

## 6. Backward Compatibility Fallback
If `trigger_map.json` is missing or unreadable when Phase A kicks off (i.e. if the coach has not undergone the v3.1 Genesis extractor), Alex catches the exception during `ccf-trigger-match`. The system logs `[PIPELINE V3.0 DEGRADATION]`, skips the Trigger-Match requirement, skips the LIWC-22 Voice Gate step, and falls back to legacy v3.0 logic: using `ccf-question` to directly ask the coach about trending topics pulled from RAG.

---

## 7. Tasks

- [ ] **Task 1:** Build the `ccf-weekly` Python CLI macro-script that handles asynchronous shell calls to the underlying CCF commands, ensuring it pauses its own thread execution while waiting for the Telegram Voice API to return.
- [ ] **Task 2:** Introduce the `Validation Triad` logic inside the `ccf-validate` script, reading the environment variable `CURRENT_SEASON_MANDATE` to arm Marcus's strict behavioral constraints.
- [ ] **Task 3:** Wire the `LIWC-22 Authenticity Gate` into the `core/recording-director.py` interceptor, rejecting wavs that score below 0.6 and utilizing the Telegram API to ping the user with the rejection feedback.
- [ ] **Task 4:** Enhance the `TeamOrchestrator` extension within `ccf-produce` to manage the parallel generation of the 36 variants without choking the LLM API rate limits.
- [ ] **Task 5:** Enforce the Receipt Chain Guard at the conclusion of all 4 major Pipeline Phases.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Trigger-First Verification):** Starting the `ccf-weekly` command for a coach with a valid `trigger_map.json` correctly inserts `ccf-trigger-match` before forming the final provocation question. *Failure Example:* The orchestrator ignores the map and just asks the coach to "talk about the current Google Trend", losing the authentic anchor.
- [ ] **AC2 (Mass Validation Triad):** During Phase D validation, the orchestrator detects 4 scripts that fail Chen's Mimicry check (>5% generic AI artifacts). It successfully triggers `TillDone` to rewrite those specific 4 scripts while preserving the other 32. *Failure Example:* The orchestrator drops the 4 bad scripts entirely, resulting in 32 outputs instead of 36.
- [ ] **AC3 (Asynchronous Wait-State):** Between Phase A and Phase B, the orchestration thread gracefully suspends, successfully resuming its state state 4 hours later when the Coach finally sends the Telegram audio note. *Failure Example:* The process times out after 60 seconds and kills the weekly run, requiring manual system restart.
- [ ] **AC4 (ADR-01 Strict Isolation):** During the Phase C batch generation involving 65 distinct agents, ZERO cross-buffer contamination occurs. Coach A's output variables are securely verified against their namespace before saving. *Failure Example:* Emilio accidentally uses Coach B's L3 pain points to write Coach A's script because the `TeamOrchestrator` shared the local RAM memory block.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| `trigger_map.json` | Upstream | Required for v3.1 execution. |
| Telegram Webhook API | External | Enables asynchronous communication back and forth during Phase B. |
| All 65 underlying CCF scripts | Downstream | All command-line tools `ccf-xxx` must be executable and return integer exit codes. |
| `TillDone` Extension | Internal | Error retry framework logic. |
| Receipt Chain Guard | Infrastructure | Non-negotiable sequence auditing. |

---

## 10. Testing Strategy

### Unit Tests
- **Validation Triad Test:** Pipe an intentionally generic, AI-written script to the `ccf-validate` module. Assert Chen (Mimicry) flags it >0.05 and the command returns a non-zero exit code. Pipe an authentic, messy script to it; assert it passes.
- **LIWC-22 Threshold Test:** Feed an audio transcript that is purely "listicle marketing speak." Assert the authenticity threshold evaluates to `<0.6` and throws the Rejection object.

### Integration Tests
- **End-to-End Synthetic Run:** Create a mock Telegram Webhook endpoint. Trigger `ccf-weekly --test-mode` to simulate the full 5 phases using GPT-4o-mini to reduce cost. Assert that the pipeline successfully halts at Phase B, waits for the mock API response, resumes, and ultimately outputs a verified `weekly_production_batch_v3.json` containing 36 valid `.md` file paths.
- **Rate Limit Queueing Test:** Force the `TeamOrchestrator` to generate all 36 scripts at precisely the same millisecond. Assert the internal queue manages the API backoff delays without dropping a single task.

### Safety Tests (ADR-01 Quarantine Security)
- **Concurrent Pipeline Check:** Start `ccf-weekly` for Emilio and Maria within 5 seconds of each other. Verify the master process explicitly silos the `MemoryFolder` extension instances, ensuring Adele pulls separate Google Trends and Jordan writes separate deep-analysis documents.
