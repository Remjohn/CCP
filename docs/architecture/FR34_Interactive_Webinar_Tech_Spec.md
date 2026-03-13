# Tech-Spec: FR34 — V²WS Interactive Mode & Excalidraw Compilation (DEP-ENG-029)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v4.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §V²WS Pipeline
**Skill Implementation:** `CBCS/backend/core/coach_graph.py`, `tools/excalidraw_compiler.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\prd TO UPDATE.md`

---

## 2. Overview

### Problem Statement
YOLO Mode (FR33) trades precision for speed, executing a webinar generator blind to human feedback until the final render. However, for a flagship Masterclass or high-ticket sales webinar, the coach requires editorial control over the narrative structure *while* it is being built. If an AI generates a 60-minute presentation simultaneously and misses the mark on Module 2, the entire subsequent arc is poisoned. Rerunning a massive prompt is computationally expensive, slow, and deeply frustrating for the operator.

### Solution
FR34 defines the **Interactive Mode BMAD Workflow (DEP-ENG-029)** natively executed via Telegram. This protocol forces a *Build-Measure-Adjust-Deploy* loop. It begins with the coach dumping unstructured thought via voice note (Stream of Consciousness). Agent Emilio (Structure) builds the outline. The system then enters a rigorous "Wait-For-Approval" execution lock, generating exactly *one* module at a time. The coach can accept the module, request structural pivots, or inject new anecdotes. Only after the final module is approved does the system execute the `excalidraw_compiler` to render the branded presentation slide deck.

### Scope
**In scope:**
- Stage 1: Stream of Consciousness (SoC) Intake & Structural Outline.
- Stage 2: The Step-and-Lock Generation Loop (Module by Module).
- Stage 3: Asset receipt (Telegram image uploads mapping to specific slides).
- Stage 4: Native `.excalidraw` JSON compilation encompassing all approved modules.

**Out of scope:**
- Generating synthetic images using Midjourney/Dall-E (the coach supplies their own images if needed).
- Changing the Excalidraw output schema (shares the exact engine with FR33).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-029` | Interactive V²WS Assembly | OUTPUT — The incremental module drafts and the final `.excalidraw` presentation file. |
| Emilio | Idea Orchestrator | AGENT — Organizes the Stream of Consciousness into a logical webinar 5-part structure. |
| Artisan | Script Copywriter | AGENT — Expands the outline into the spoken script, one module at a time. |
| `coach_graph.py` | State Graph | LOGIC — The LangGraph node architecture that enforces the `interrupt_before=["approval"]` blocking mechanism. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Human-in-the-Loop (HITL) Iterative Refinement** | Various (HCI / AI Alignment) | 2020+ | LLM reasoning degrades linearly over massive output windows. By enforcing algorithmic pauses (HITL breakpoints) at the module boundary, the system resets its context vector, dramatically reducing hallucination drift and ensuring the coach's intent steers the generation locally rather than just globally. |

### Technical Decisions
1. **Telegram-Native Operation:** The coach does not log into a web dashboard for this. They communicate with the bot via Telegram voice notes or text. The system responds with the drafted module text in-app. The coach replies *"Approved"* or *"Change the story about the client in Madrid."* This aligns with the 'frictionless executive' design philosophy.
2. **LangGraph State Interrupts:** The entire process is managed via `LangGraph`, utilizing the `interrupt_before` paradigm. The graph executes a `Generate_Module_[X]` node and physically suspends execution, saving the state to Postgres, until the webhook receives the human approval boolean to transition to `Generate_Module_[X+1]`.

---

## 4. Implementation Plan

### Stage 1: Stream of Consciousness (SoC) Intake
*Script:* `core/coach_graph.py`
*Agent Name:* Emilio
*Inputs:* Unstructured Coach Voice Note.
*Outputs:* `Webinar_Outline` JSON.
*Failure Condition:* Emilio fails to divide the unstructured dump into distinct, logical modules.
*Receipt Write:* Write Receipt Block per FR47 `Receipt_Block_N.json` schema: `{ receipt_id, previous_receipt_hash, input_payload_hash, output_payload_hash, stage_name, timestamp, agent_name }` # REVISED: Standardizing receipt format across all specs per FR47 cryptographic schema.

**Steps:**
1. Coach triggers the workflow via Telegram: `/v2ws_interactive`.
2. Coach submits a 3-5 minute voice note brain dump of what they want to teach.
3. Emilio transcribes and parses the SoC, generating a 5-Part Outline (Hook, Problem, Paradigm, Method, Offer).
4. System sends the Outline to Telegram. State machine enters `WAITING_FOR_OUTLINE_APPROVAL`.

### Stage 2: The Step-and-Lock Generation Loop
*Script:* `core/coach_graph.py`
*Agent Name:* Artisan
*Inputs:* `Webinar_Outline`, Coach Feedback, Current Module Index.
*Outputs:* Drafted Module text.
*Failure Condition:* Artisan generates Module 3 while the system is still waiting for approval on Module 2.
*Receipt Write:* Write Receipt Block per FR47 `Receipt_Block_N.json` schema: `{ receipt_id, previous_receipt_hash, input_payload_hash, output_payload_hash, stage_name, timestamp, agent_name }` # REVISED: Standardizing receipt format across all specs per FR47 cryptographic schema.

**Steps:**
1. Upon Outline approval, the Graph transitions to `Node_Generate_Module_1`.
2. Artisan generates the script and slide visuals for Module 1.
3. System sends Module 1 text to Telegram. State transitions to `WAITING_FOR_MOD_1_APPROVAL`.
4. Before advancing to the next module, Artisan queries the Intelligence Library (DEP-LIB-001, DEP-LIB-002, DEP-ENG-006) for structural pivot suggestions relevant to the current module's emotional register and audience depth permission. Suggestions are surfaced to the operator as optional — not blocking. Operator may accept, reject, or ignore. # REVISED: Added explicit Intelligence Library query per Architect decision.
5. Receipt Write: `WEBINAR-INTEL-QUERY-{module_number}-{timestamp}` # REVISED: Added explicit receipt write for the structural query.
6. If Coach replies with feedback, Graph routes to `Node_Revise_Module_1`.
7. If Coach replies "Approved," Graph transitions to `Node_Generate_Module_2`.
8. This loops until all modules defined in the outline are `APPROVED`.

### Stage 3: Image Asset Receipt
*Script:* `core/telegram.py` -> `core/coach_graph.py`
*Inputs:* `Photos` uploaded via Telegram.
*Outputs:* Base64 image strings mapped to specific slides.
*Failure Condition:* Coach uploads a PDF instead of an image.
*Receipt Write:* Write Receipt Block per FR47 `Receipt_Block_N.json` schema: `{ receipt_id, previous_receipt_hash, input_payload_hash, output_payload_hash, stage_name, timestamp, agent_name }` # REVISED: Standardizing receipt format across all specs per FR47 cryptographic schema.

**Steps:**
1. Following final module approval, the system prompts: *"Any specific images or diagrams to include? Upload them now, referencing the slide number (e.g., 'Slide 4'). If none, type 'Skip'."*
2. System intercepts Telegram photo payloads, converts them to `Base64`, and maps them to the `Webinar_Master_Script` JSON array.

### Stage 4: Excalidraw Compilation
*Script:* `tools/excalidraw_compiler.py`
*Inputs:* `Webinar_Master_Script` (Fully Approved).
*Outputs:* `DEP-ENG-029` (The `.excalidraw` file dispatched to Telegram).
*Failure Condition:* Excalidraw JSON syntax is invalid.
*Receipt Write:* Write Receipt Block per FR47 `Receipt_Block_N.json` schema: `{ receipt_id, previous_receipt_hash, input_payload_hash, output_payload_hash, stage_name, timestamp, agent_name }` # REVISED: Standardizing receipt format across all specs per FR47 cryptographic schema.

**Steps:**
1. Compiler executes identical logic to FR33 (YOLO Mode), generating spatial boundary boxes for slides and locating speaker notes to the right of the frame.
2. If Base64 images were provided in Stage 3, the compiler uses the Excalidraw `image` element schema to embed them directly into the target slide rectangle.
3. The `.excalidraw` file is saved and attached cleanly back to the Coach via the Telegram bot as a downloadable document.

---

## 5. Primary Output Schema (DEP-ENG-029)

**Schema Name:** `interactive_v2ws_state.json` *(This tracks the active state before final compilation into the Excalidraw schema)*

```json
{
  "session_id": "V2WS-20260314-A",
  "coach_id": "EMI",
  "current_phase": "MODULE_ASSEMBLY",
  "active_module_index": 2,
  "outline_approved": true,
  "modules": [
    {
      "index": 1,
      "title": "The Hook",
      "status": "APPROVED",
      "script_content": "Welcome everyone...",
      "asset_base64": null
    },
    {
      "index": 2,
      "title": "The Paradigm Shift",
      "status": "WAITING_ON_COACH",
      "script_content": "Here is why your previous attempts failed...",
      "asset_base64": null
    }
  ],
  "excalidraw_payload_ready": false
}
```

---

## 6. Backward Compatibility Fallback
If the Telegram Bot API drops an incoming message during a `WAITING_FOR_APPROVAL` state, leaving the LangGraph indefinitely hanging, the system runs a 12-hour cron sweep on stale graphs. If a graph is stale for >12 hours, it alerts the coach: *"I haven't heard back on Module 2. Should we resume where we left off, or abort this webinar build?"* This ensures state locks do not indefinitely consume database/memory resources.

---

## 7. Tasks

- [ ] **Task 1:** Implement the LangGraph configuration in `core/coach_graph.py` establishing the strict `interrupt_before` nodes matching the 5-part module loop.
- [ ] **Task 2:** Build the Telegram webhook parser capable of interpreting conversational coach replies (e.g., "Looks good!", "Let's change the intro") and translating them into binary `APPROVED` / `REVISION_REQUIRED` routing commands for the state machine.
- [ ] **Task 3:** Configure the Telegram Photo intercept hook. It must capture compressed Telegram images, run a prompt to ask the coach which slide to assign it to, and encode the binary payload into `Base64`.
- [ ] **Task 4:** Expand the `excalidraw_compiler.py` to support the insertion of `image` JSON objects inside specific `rectangle` bounding boxes.
- [ ] **Task 5:** Write the Telegram dispatch function that successfully uploads the finalized `.excalidraw` file format back to the chat as an arbitrary document (not an image).

---

## 8. Acceptance Criteria

- [ ] **AC1 (The Algorithmic Stop):** Stage 1 completes. Emilio outputs the outline. Assert that the underlying Python execution thread physically halts and yields back to the event loop, taking 0% CPU, while waiting for the Telegram webhook to receive the approval string. *Failure Example:* The system ignores the interrupt and rapidly hallucinates all 5 modules before the coach can verify the outline premise.
- [ ] **AC2 (Revision Routing):** Module 2 is drafted. Coach replies, "Make it punchier." Assert that the LangGraph routes to the `Revise_Module` node, regenerating strictly Module 2 without altering the previously approved Module 1. *Failure Example:* The revision prompt accidentally triggers a full regeneration from scratch, erasing the approved Module 1 script.
- [ ] **AC3 (Image Embedding):** The coach uploads a jpg diagram for Slide 3. Assert the compiled `.excalidraw` file contains a valid `"type": "image"` block and correctly binds the binary data to the `fileId` dictionary required by the Excalidraw spec. *Failure Example:* The compiler inserts a markdown `![image](url)` syntax into a text box instead of natively embedding the actual visual asset in the canvas.
- [ ] **AC4 (ADR-01 Strict Isolation):** Coach A and Coach B trigger `/v2ws_interactive` simultaneously. Assert that LangGraph instantiates two completely separate Thread IDs bound to their specific tenant scope. *Failure Example:* State bleeds cross-tenant, causing Coach A to receive Coach B's Module 3 draft in their Telegram feed.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| LangGraph State Management | Internal | Crucial for the `interrupt_before` human-in-the-loop requirement. |
| Telegram Bot API | External | Required for the conversational UX and document transfer. |
| MemoryFolder | Internal | Required by Artisan to inject L3 pain contextual suggestions. |
| Receipt Chain Guard | Infrastructure | Non-negotiable sequence auditing. |

---

## 10. Testing Strategy

### Unit Tests
- **Telegram Sentiment Parser:** Feed 50 variations of human approval ("yes", "y", "lgtm", "looks good", "ship it") into the intent classifier. Assert 100% resolve to the `APPROVED` boolean trigger. Feed 50 variations of feedback ("no", "change this", "too wordy"). Assert 100% resolve to `REVISION_REQUIRED`.
- **Excalidraw Image Schema:** Generate a dummy Base64 string. Pass it to the compiler. Assert the output strictly matches the `{ "type": "image", "fileId": string, "files": { ... } }` schema structure required by Excalidraw v2.

### Integration Tests
- **The State Graph Lifecycle:** Programmatically execute the LangGraph thread. Feed it an intake -> assert node stops. Feed an approval -> assert node advances to Mod 1. Feed a revision -> assert node loops. Feed an approval -> assert node advances to Mod 2. Verify all transitions function without deadlocking.
- **The Stale Sweep Test:** Manually create a PostgreSQL state checkpoint locked in `WAITING_FOR_MOD_1` with a timestamp exactly 13 hours old. Initiate the `stale_sweep_cron`. Assert it successfully identifies the thread and triggers the Telegram re-engagement payload.

### Safety Tests (ADR-01 Quarantine Security)
- **Thread Sandboxing:** Spin up two identical Interactive Mode sessions under the same coach tenant. Send an approval command to Thread A. Assert that Thread B remains correctly locked in `WAITING_FOR_APPROVAL` and state data does not collide across parallel sessions within the same tenancy.
