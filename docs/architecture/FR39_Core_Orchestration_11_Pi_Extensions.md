# Tech-Spec: FR39 — Core Orchestration (The 11 Pi Extensions) (DEP-ENG-034)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v4.0 / Unified PRD v3.1)
**Architecture Reference:** Architecture_Synthesis_Report, PRD §4.1, PRD Step 12
**Skill Implementation:** `extensions/` (Pi Coding Agent Harness)
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\prd TO UPDATE.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\Architecture_Synthesis_Report.md`
- `d:\Work\The Conscious Coaching Factory\lab\Notebook LM\ccf\Turning The Content Factory Into A Brain.md`
- `d:\Work\The Conscious Coaching Factory\lab\Notebook LM\ccf\From Vibe Coding To Agentic Engineering.md`

---

## 2. Overview

### Problem Statement
In a multi-agent system spanning the CCF (content generation), CBCS (1-on-1 text coaching), and V2WS (webinar generation), relying on a static Chat UI or naked LLM API calls results in rapid "context collapse" and "voice drift." Without rigid, programmatic control over the agent's internal read-execute-print loop, the LLM will hallucinate missing data, silently fail formatting rules, use the wrong persona for sub-tasks, and lose access to the underlying graph database.

### Solution
FR39 establishes the **11 Pi Extensions (DEP-ENG-034)** built within the Pi Coding Agent harness. These are TypeScript modules that intercept the LLM's cognition *mid-loop*. By providing explicit system hooks, these extensions enforce platform-wide structural integrity. They act as the connective tissue unifying the 3 distinct ecosystems, handling everything from hard ambiguity stops (`InteractComp`) and database writes (`MemoryFolder`) to LLM cost-optimization (`ModelRouter`) and subjective vibe-checking (`SoulResonance`).

### Scope
**In scope:**
- Development of the 7 Operational Extensions (Logic, DB, Routing).
- Development of the 4 Intuition Extensions (Synthesis, Re-framing, Tone).
- The Pi Extension Harness injection methodology (mid-loop execution).
- Receipt logging for every extension invocation.

**Out of scope:**
- Implementation logic for the 4 Intuition Extensions (SoulResonance, PatternWeaver, GhostContext, AncestralWisdom). These are fully specified in FR40. # REVISED: Added explicit exclusion of Intuition Extension logic to respect FR40 boundary.
- The internal prompts of the agents themselves (handled in separate Agent PRDs).
- The Neo4j server-side management (this spec covers the graph *writer* extension, not the DB infra).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-034` | The Pi Extension Suite | OUTPUT — The compiled suite of 11 TypeScript files installed in the core orchestrator. |
| Agent Harness | Pi Coding Agent | INFRASTRUCTURE — The execution environment that supports programmatic loop-interception. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Manifold Constrained Hyperconnections (MHC)** | GLM5 Research Team | 2025 | Establishes that LLMs suffer "vanishing gradients" (voice drift) when passing data through deep multi-agent pipelines. Pi extensions like `SystemSelect` and `SoulResonance` act as the "Doubly Stochastic Matrices" that mathematically constrain the agent's outputs to remain faithful to the coach's identity at every step. |
| **Deep Agent Memory Folding** | Various | 2024 | Proves that raw conversational history corrupts reasoning. The `MemoryFolder` extension implements the "Take a Breath" method, pausing the LLM to summarize Episodic memory and clear raw working context, preventing context collapse. |

### Technical Decisions
1. **Agentic Engineering vs. Vibe Coding:** The CCP explicitly rejects chat-based workflows. All 11 extensions are designed to enforce "system constraints" (e.g., `TillDone` refusing to let the LLM stop until an output schema matches) rather than relying on the LLM to "try its best."
2. **Separation of Operational and Intuition:** 7 extensions handle cold logic (routing, saving, parallelizing). 4 extensions are given dedicated sub-agents to handle "warm" logic (philosophical reframing, emotional resonance). This protects the logical pipeline from being polluted by creative hallucinations.
3. **TypeScript Implementation:** Extensions must be written in TypeScript/JavaScript to natively hook into the Pi Coding Agent's Node.js runtime environment.

---

## 4. Implementation Plan

### Phase 1: The 7 Operational Extensions

**1. `InteractComp` (The Ambiguity Gate)**
- *Input:* Task execution context.
- *Resolution Rule:* If ANY required `[DEP-ID]` variable is missing or empty, the extension sets `status=FAIL_AMBIGUITY`.
- *Action:* Instantly halts the execution loop. Throws an error to the user stating: "Cannot proceed. Missing input context. Refusing to hallucinate data."
- *Receipt Write:* Write Receipt Block per FR47 `Receipt_Block_N.json` schema: `{ receipt_id, previous_receipt_hash, input_payload_hash, output_payload_hash, stage_name, timestamp, agent_name }` # REVISED: Standardizing receipt format across all specs per FR47 cryptographic schema.

**2. `MemoryFolder` (The Graph Writer / Context clearer)**
- *Input:* Session token count. 
- *Resolution Rule:* If context > `4000 tokens` OR task is complete, trigger fold.
- *Action:* Summarizes the last N steps into Working Memory, executes a Supabase write, and drops the raw history from the context window.
- *Receipt Write:* Write Receipt Block per FR47 `Receipt_Block_N.json` schema: `{ receipt_id, previous_receipt_hash, input_payload_hash, output_payload_hash, stage_name, timestamp, agent_name }` # REVISED: Standardizing receipt format across all specs per FR47 cryptographic schema.

**3. `DamageControl` (The Self-Healing Loop)**
- *Input:* API Error Code or JSON Parse Error.
- *Resolution Rule:* If execution fails, intercept the red-print error before it crashes the factory.
- *Action:* Feed the exact error trace back into the LLM as a system message: `Action failed with trace [X]. Fix the syntax and retry.` Limits to 3 retries.
- *Receipt Write:* Write Receipt Block per FR47 `Receipt_Block_N.json` schema: `{ receipt_id, previous_receipt_hash, input_payload_hash, output_payload_hash, stage_name, timestamp, agent_name }` # REVISED: Standardizing receipt format across all specs per FR47 cryptographic schema.

**4. `ModelRouter` (The Optimizer)**
- *Input:* Task Type metadata tag.
- *Resolution Rule:* 
  - If `Task == Strategy/Reasoning` → Route to `gpt-4o` (or equivalent ultra-high reasoning).
  - If `Task == Drafting/Formatting` → Route to `gpt-4o-mini` (or equivalent fast/cheap).
- *Action:* Hot-swaps the underlying LLM mid-loop.
- *Receipt Write:* Write Receipt Block per FR47 `Receipt_Block_N.json` schema: `{ receipt_id, previous_receipt_hash, input_payload_hash, output_payload_hash, stage_name, timestamp, agent_name }` # REVISED: Standardizing receipt format across all specs per FR47 cryptographic schema.

**5. `TillDone` (The Assurance Engine)**
- *Input:* A defined JSON schema or file path target.
- *Resolution Rule:* If the LLM attempts to output `[FINISHED]` but the schema is invalid or the file is missing, set `status=INCOMPLETE`.
- *Action:* Appends the system prompt: `Requirement not met. Continue.` Forcing the LLM to keep iterating.
- *Receipt Write:* Write Receipt Block per FR47 `Receipt_Block_N.json` schema: `{ receipt_id, previous_receipt_hash, input_payload_hash, output_payload_hash, stage_name, timestamp, agent_name }` # REVISED: Standardizing receipt format across all specs per FR47 cryptographic schema.

**6. `TeamOrchestrator` (The Parallel Manager)**
- *Input:* A multi-perspective directive (e.g., "Argue this point").
- *Resolution Rule:* Spawns parallel LLM threads.
- *Action:* Triggers 3 identical agents with different temperature variables to generate multiple drafts simultaneously (DraftRL implementation).
- *Receipt Write:* Write Receipt Block per FR47 `Receipt_Block_N.json` schema: `{ receipt_id, previous_receipt_hash, input_payload_hash, output_payload_hash, stage_name, timestamp, agent_name }` # REVISED: Standardizing receipt format across all specs per FR47 cryptographic schema.

**7. `SystemSelect` (The Persona Swapper)**
- *Input:* The `/system @[Persona]` slash command.
- *Resolution Rule:* Overwrites the current system prompt with the requested YAML constitution.
- *Action:* Allows a single agent to cycle through Scout → Planner → Builder → Critic hats without losing context.
- *Receipt Write:* Write Receipt Block per FR47 `Receipt_Block_N.json` schema: `{ receipt_id, previous_receipt_hash, input_payload_hash, output_payload_hash, stage_name, timestamp, agent_name }` # REVISED: Standardizing receipt format across all specs per FR47 cryptographic schema.

### Phase 2: Intuition Extension Activation # REVISED: Replaced entirely to defer logic execution to FR40.
- The Governance Layer detects staleness, emotional flatness, or structural monotony in the production queue
- When detected, emits an activation signal to FR40 (Intuition Extensions Orchestrator)
- This spec owns the detection trigger only
- Execution logic is owned by FR40
- Receipt Write: `INTUITION-TRIGGER-{signal_type}-{timestamp}` # REVISED: Added specific receipt write for the activation signal.

---

## 5. Primary Output Schema (DEP-ENG-034)

**Schema Name:** `pi_extension_execution_log.json`

```json
{
  "execution_id": "PI-EXT-8899",
  "pipeline_stage": "Phase_2_Assembly",
  "timestamp": "2026-03-14T08:00:00Z",
  "extensions_fired": [
    {
      "extension_name": "SystemSelect",
      "action": "Swapped to @Critic Persona",
      "result": "SUCCESS"
    },
    {
      "extension_name": "InteractComp",
      "action": "Ambiguity Check",
      "result": "PASS"
    },
    {
      "extension_name": "TillDone",
      "action": "Schema validation",
      "result": "FAIL - RE-PROMPTING AGENT"
    }
  ],
  "latency_ms": 1450
}
```

---

## 6. Backward Compatibility Fallback
If the Pi Coding Agent harness experiences a catastrophic runtime error and cannot load extensions, the system defaults to **Waterfall Mode**. All Intuition extensions are bypassed, `ModelRouter` defaults to a single static model, and the pipeline executes sequentially. A severe dashboard alert is triggered: `WARNING: Operating without system constraints. Output resonance degradation likely.`

---

## 7. Tasks

- [ ] **Task 1:** Write the TypeScript scaffolding for the Pi Extension library `extensions/ccp_core/`.
- [ ] **Task 2:** Implement the `InteractComp` exact-match string validator to halt on missing `[DEP-ID]` values cleanly.
- [ ] **Task 3:** Write the `ModelRouter` regex to parse task IDs and hot-swap API endpoints dynamically.
- [ ] **Task 4:** Build the `MemoryFolder` token counter logic and the Supabase REST API `POST` hook.
- [ ] **Task 5:** Implement the `TillDone` JSON Schema validator loop.
- [ ] **Task 6:** Wrap the 4 Intuition extensions into discrete, headless sub-agent API call functions.

---

## 8. Acceptance Criteria

- [ ] **AC1 (InteractComp Gate):** Submit a prompt with a missing `coach_brand.json` variable. Assert the extension halts execution with `status=FAIL_AMBIGUITY` and does *not* make an LLM API call. *Failure Example:* The LLM generates a generic, unbranded brand identity, polluting the context window.
- [ ] **AC2 (TillDone Retries):** Submit a task requiring a 5-key JSON output. Mock the LLM returning only 4 keys. Assert `TillDone` intercepts the JSON, detects the missing key, feeds the error back to the LLM, and successfully returns a 5-key JSON on retry 2. *Failure Example:* The pipeline crashes downstream because the compiler tries to parse a missing key.
- [ ] **AC3 (SystemSelect Swap):** Send the command `/system @Editor`. Assert the Pi harness completely purges the previous "Writer" system instructions and loads the "Editor" instructions while maintaining the conversation history. *Failure Example:* The agent becomes confused, merging writer and editor guidelines and outputting schizophrenic text.
- [ ] **AC4 (DamageControl Handling):** Mock a 500 error from the Anthropic/OpenAI API. Assert `DamageControl` catches the timeout, waits 3 seconds, and retries gracefully without dropping the user's session. *Failure Example:* The script throws an uncaught exception and the Node.js server crashes entirely.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| Pi Coding Agent | External/Core | The Node.js execution harness that standardizes these extensions. |
| Zod / JSON Schema | Internal | Required by `TillDone` + `InteractComp` for rigorous output validation. |
| Supabase `pgvector` | External | DB Target for the `MemoryFolder` storage writes. |

---

## 10. Testing Strategy

### Unit Tests
- **Token Folding Math:** Test `MemoryFolder`. Mock an input of 4,005 tokens. Assert the folding logic triggers. Mock an input of 3,995 tokens. Assert it bypasses.
- **Model Routing Logic:** Pass a task labeled `[FORMAT_ONLY]` to `ModelRouter`. Assert it requests a `mini/flash` model endpoint to save costs.

### Integration Tests
- **The Extension Cascade Stack:** Run a pipeline that purposefully triggers a swap (`SystemSelect`), generates a faulty output, gets caught (`TillDone`), retries internally (`DamageControl`), succeeds, and writes to the DB (`MemoryFolder`). Assert the `pi_extension_execution_log` shows all 4 extensions firing in their correct sequence without terminal failure.

### Safety Tests (ADR-01 Quarantine Security)
- **Memory Contamination Check:** When `MemoryFolder` writes to the graph, heavily assert that the `Tenant_ID` cannot be overwritten or altered by the LLM summarizing the text. The LLM must not be allowed to define the structural DB path, only the payload.
