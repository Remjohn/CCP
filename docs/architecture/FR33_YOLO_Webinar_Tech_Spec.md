# Tech-Spec: FR33 — V2WS YOLO Mode Webinar Generation (DEP-ENG-028)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v4.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §V2WS Pipeline
**Skill Implementation:** `CCF/commands/ccf-v2ws.md`, `CCF/generators/excalidraw_compiler.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\prd TO UPDATE.md`

---

## 2. Overview

### Problem Statement
Constructing a high-converting webinar typically requires weeks of structural outlining, slide design, and scriptwriting. When a coach identifies an immediate market opportunity or an acute audience pain point (e.g., a relevant cultural event dropping on a Tuesday), they cannot wait 3 weeks to deploy a training. They need a rapid-deployment mechanism that bypasses standard lengthy CCF planning phases but retains the rigorous psychological structure of the Voice DNA and Context Premise.

### Solution
FR33 formally defines **YOLO Mode within the V2WS (Visual Vault Webinar System) Pipeline (DEP-ENG-028)**. This protocol collapses the 5-stage webinar creation process into a single, chained, autonomous execution loop. The System Operator inputs exactly 5 structured constraints (Topic, Audience, Offer, Stories, Tone). The system then autonomously executes DEEP/FRESH research to validate the topic, generates the module structures, writes the script, and compiles the final output directly into a branded `.excalidraw` file where slide visuals and speaker notes are embedded as native text layers for instant recording.

### Scope
**In scope:**
- Stage 1: The 5-Variable Intake Vector.
- Stage 2: Autonomous DEEP/FRESH Research execution.
- Stage 3: Generative AI module construction & script writing (Emilio/Artisan).
- Stage 4: Native `.excalidraw` JSON compilation (Visual + Text integration).

**Out of scope:**
- Rendering the `.excalidraw` to a `.mp4` video (this strictly prepares the presentation deck for human recording).
- Updating the standalone `coach_soul.json` (YOLO Mode consumes DNA but does not alter baseline state).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-028` | V2WS YOLO Payload | OUTPUT — The final `.excalidraw` structured JSON file containing the presentation and script. |
| `ccf-v2ws` | CCF Command | INVOCATION — The command-line entry point validating the 5 input parameters. |
| Emilio | Idea Orchestrator | AGENT — Constructs the structural flow based on the 5 variables + Context Premise. |
| `excalidraw_compiler.py` | Generator Engine | LOGIC — Translates structured webinar beats into specific Excalidraw JSON canvas coordinates. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Cognitive Load Theory in Multimedia Learning** | Richard Mayer | 2001 | To minimize extraneous cognitive load, the delivery of learning material must integrate text and visuals spatially (Spatial Contiguity Principle). Having the coach read a script on a separate screen while clicking slides causes delivery friction. YOLO mode compiles the speaker script directly into off-canvas `.excalidraw` text layers directly adjacent to the visual frames, optimizing the coach's recording interface. |

### Technical Decisions
1. **The Excalidraw Compilation:** Rather than generating a markdown script and a separate folder of images, the system physically writes the `JSON` schema of an `.excalidraw` file. It instantiates pre-branded boxes (using the coach's hex codes) and places the final presentation script floating immediately outside the camera-capture bounding box of the slide frame. 
2. **Autonomous Execution Bypass:** In standard mode, CCF pauses between modules to ask for human approval. In YOLO Mode, the system's `approval_gate` flags are hard-set to `bypass=true`. The system will not stop running until the `excalidraw` file is rendered.

---

## 4. Implementation Plan

### Stage 1: The 5-Variable Intake Validation
*Script:* `commands/ccf-v2ws.md` (CLI entry point)
*Inputs:* The 5 CLI Arguments.
*Outputs:* Validated `YoloIntake` JSON.
*Failure Condition:* The operator omits one of the 5 mandatory fields.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. System receives the CLI input containing:
   - `actionable_lesson_thesis`
   - `target_audience_segment`
   - `final_offer_cta`
   - `key_stories_array`
   - `tone_energy_constraint`
2. Validates lengths and types. Fails out if incomplete.

### Stage 2: Autonomous DEEP/FRESH Execution
*Script:* `core/research.py`
*Agent Name:* Remgion (Researcher)
*Inputs:* `actionable_lesson_thesis`, `Context_Premise` (L3 Pain Map).
*Outputs:* `Research_Silo` JSON.
*Failure Condition:* Internet timeout on the Tavily/Google Scholar APIs.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Remgion executes a rapid contextual search pulling two vectors:
   - `DEEP`: Academic/Psychological validation of the `thesis`.
   - `FRESH`: A recent cultural/news hook (within 7 days) related to the `thesis` to anchor the introduction.

### Stage 3: Module & Script Generation (Chained)
*Script:* `core/generator.py`
*Agent Name:* Emilio (Structure) → Artisan (Copy)
*Inputs:* `YoloIntake`, `Research_Silo`, `Voice_DNA`.
*Outputs:* `Webinar_Master_Script` JSON (Slide x Script pairings).
*Failure Condition:* Artisan breaches the `<150` word limit per slide.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Emilio maps a standard 5-part webinar flow (Hook → Problem Expansion → Paradigm Shift → The Method → The Offer).
2. Artisan generates the exact spoken script for each slide, locking the voice strictly to the `tone_energy_constraint` provided.
3. Artisan generates visual instructions for each slide (e.g., "[Visual: 3 overlapping circles showing X, Y, Z]").

### Stage 4: Native Excalidraw Compilation
*Script:* `tools/excalidraw_compiler.py`
*Inputs:* `Webinar_Master_Script`, Coach Brand Config (Hex codes).
*Outputs:* `DEP-ENG-028` (Final `.excalidraw` file).
*Failure Condition:* System generates invalid JSON syntax breaking the Excalidraw import parser.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. The script traverses the JSON array.
2. For each module, it generates a `rectangle` element representing the Slide boundary (1920x1080 proportion).
3. It maps the visual instructions into internal text/shape layers inside the boundary.
4. It maps the *spoken script* into a `text` element positioned at coordinate `x: boundary.x + 2000` (off-canvas right), formatting it as a teleprompter note.
5. Saves file locally as `[DATE]_YOLO_Webinar_[Topic].excalidraw`.

---

## 5. Primary Output Schema (DEP-ENG-028)

**Schema Name:** `v2ws_excalidraw_payload.json` *(Note: This follows the official Excalidraw schema spec)*

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "ccf_yolo_pipeline",
  "elements": [
    {
      "type": "rectangle",
      "version": 1,
      "versionNonce": 12345,
      "x": 0,
      "y": 0,
      "width": 1920,
      "height": 1080,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "#ffffff",
      "groupIds": ["slide_1"]
    },
    {
      "type": "text",
      "x": 2000,
      "y": 0,
      "text": "SPEAKER NOTES:\nWelcome everyone. Today we tackle [Problem]. I want you to remember...",
      "fontSize": 36,
      "fontFamily": 1,
      "textAlign": "left",
      "strokeColor": "#000000",
      "groupIds": ["slide_1_notes"]
    }
    // ... loops for all modules
  ],
  "appState": {
    "viewBackgroundColor": "#fafafa"
  }
}
```

---

## 6. Backward Compatibility Fallback
If the Excalidraw schema parser updates and breaks the Python generator library (`excalidraw_compiler.py` throws JSON errors), the pipeline gracefully downgrades to a standard markdown markdown export. Stage 4 aborts, and the engine writes `[DATE]_YOLO_Webinar.md` containing formatted tables mapping `Slide Content` on the left and `Speaker Script` on the right.

---

## 7. Tasks

- [ ] **Task 1:** Build the `ccf-v2ws` CLI command forcing the mandatory 5-question prompt sequence before pipeline initiation.
- [ ] **Task 2:** Update `core/research.py` to support `YOLO_MODE` flag, bypassing human approval gates and passing directly to generator agent upon returning the DEEP/FRESH results.
- [ ] **Task 3:** Create the webinar structural template map in `Emilio_SKILL.md` (Hook → Problem → Paradigm → Method → Offer).
- [ ] **Task 4:** Refine Artisan's prompt to restrict output per slide to 150 words to prevent overflowing the Excalidraw text boundary constraints.
- [ ] **Task 5:** Write the `excalidraw_compiler.py` mathematically plotting X/Y coordinates to lay out 10-20 slides horizontally spaced 500px apart, appending speaker notes to the right of each frame.

---

## 8. Acceptance Criteria

- [ ] **AC1 (The 5-Input Gate):** The operator runs `ccf-v2ws` and only provides 4 of the variables, skipping "Offer". The CLI cleanly rejects execution explicitly demanding the `final_offer_cta` parameter. *Failure Example:* System accepts partial inputs and hallucinates a generic offer at the end of the script that the coach cannot fulfill.
- [ ] **AC2 (End-to-End Continuity):** In YOLO Mode, after the 5 inputs are provided, the system does not pause to request human approval for the research results or the module outlines. It runs straight through to the `.excalidraw` file generation. *Failure Example:* The CLI hangs on Stage 2 asking `[Y/N]` to approve the FRESH research hook, defeating the "YOLO rapid-deployment" mandate.
- [ ] **AC3 (Excalidraw Syntax Verification):** The generated `.excalidraw` file is drag-and-dropped into the official web browser version of Excalidraw.com. Assert that it opens instantly without throwing a "corrupt file" error. *Failure Example:* The compiler forgets to iterate the `id` field for the JSON elements, causing the Excalidraw visualizer to crash.
- [ ] **AC4 (Spatial Contiguity Delivery):** Opening the generated file, the `SPEAKER NOTES` text element is positioned exclusively outside the `1920x1080` bounding box of the slide presentation. *Failure Example:* The speaker script is accidentally generated *inside* the slide box, forcing the coach to manually move walls of text before recording.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| `Excalidraw Schema` | External | Output must strictly match their open-source JSON spec. |
| ModelRouter | Internal | Required to route to complex reasoning models for script generation. |
| DEEP/FRESH Research | Upstream | Required to anchor the script in reality before generation. |
| Receipt Chain Guard | Infrastructure | Non-negotiable sequence auditing. |

---

## 10. Testing Strategy

### Unit Tests
- **Excalidraw Coordinate Math:** Generate a 5-slide JSON output. Assert mathematically that `Slide_2.x` is precisely `Slide_1.x + 1920 + 500` to prevent visual overlapping.
- **Param Length Constraint:** Run Artisan script generation over a complex concept. Assert that the returned string for the speaker notes is `<150` words to fit comfortably in the designated UI space.

### Integration Tests
- **The YOLO Bypass Test:** Mock a full pipeline execution. Assert that the terminal stdout contains exactly 0 `[Action Required]` input prompts between Stage 1 (Intake) and Stage 4 (Compilation).
- **The Fallback Path:** Deliberately corrupt the Excalidraw JSON compiler library. Run YOLO mode. Assert the system successfully catches the format exception and outputs the `.md` markdown script table without irrecoverably stalling.

### Safety Tests (ADR-01 Quarantine Security)
- **Brand Hex Contamination:** Run YOLO compilation for Coach A. Assert the compiled background/stroke colors strictly pull from Coach A's `coach_brand.json` configuration block, ensuring Coach B's color palette never bleeds into Coach A's deliverables.
