# Tech-Spec: FR36 — Context-Aware Stick Figure Illustrations (DEP-ENG-031)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v4.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §FR19a, Architecture_Synthesis_Report
**Skill Implementation:** `skills/visual/excalidraw-composer/SKILL.md`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\prd TO UPDATE.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\Architecture_Synthesis_Report.md`
- `GMG Expert 03 Visual Consistency Standards` (Knowledge Base)

---

## 2. Overview

### Problem Statement
Standard AI image generators (Midjourney, Dall-E) produce static, rectangular images with embedded backgrounds. While this works for standard blog posts, it completely fractures the immersion of an interactive, white-labeled presentation deck (like Excalidraw slides). The background of the image clashes with the background of the slides. Furthermore, AI struggles to maintain aesthetic consistency across 20 slides, often jumping between hyper-realism, 3D renders, and cartoon sketches in the same presentation.

### Solution
FR36 defines the **Context-Aware Stick Figure Illustration Generator (DEP-ENG-031)**, operating via the **Transparent Collage Pipeline**. Adapted from the proven `GMG Expert 03` emotional animator skill, this engine generates isolated, highly expressive stick figures interacting with photorealistic props. By strictly enforcing a pure white (`#FFFFFF`) background in the prompt, the Render Controller (Grant) can execute a programmatic alpha-extraction (background removal). The resulting transparent PNG is injected directly into the Excalidraw JSON canvas, allowing dynamic, emotionally intelligent characters to float natively over any background color or text without rectangular boxing.

### Scope
**In scope:**
- Stage 1: The Visual Reasoning Protocol (Emotion & Object mapping).
- Stage 2: T2I Generation constrained by GMG Expert 03 Consistency Standards.
- Stage 3: Alpha Extraction (Background Stripping via `rembg`).
- Stage 4: Injection of the isolated Base64 PNG into Excalidraw JSON format.

**Out of scope:**
- Native Excalidraw JSON composition and slide injection (owned by FR35). # REVISED: Added explicit exclusion of downstream consumer responsibilities per Architect decision.
- Generating fully animated `.mp4` stick figures.
- Generating textual typography directly inside the `PNG` (text is handled by Benjamin via JSON, not Grant via pixels).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-031` | Transparent Stick Figure Collage | OUTPUT — The Base64 string of the alpha-extracted PNG containing the character and object. |
| Grant | Render Controller | AGENT — Executes the Visual Reasoning Protocol, fires the T2I API, and runs the mask script. |
| `GMG Expert 03` | Emotional Animator Skill | REFERENCE — Provides the stylistic constraints to ensure cross-slide visual continuity. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Otsu’s Method (Global Thresholding)** | Nobuyuki Otsu | 1979 | Background removal algorithms require high variance between the foreground and background to avoid edge fraying. By mathematically forcing the LLM to output absolute `#FFFFFF` and avoiding any soft drop-shadows on the floor, Otsu thresholding identifies the background layer with near 100% accuracy, creating a pixel-perfect transparency mask. |

### Technical Decisions
1. **GMG Expert 03 Constraints:** The system hardcodes constraints into the T2I prompt: The stick figure must maintain a uniform color/duotone across all slides, must use dark borders (never yellow/neon), and must maintain consistent anatomical abstraction (e.g., dot eyes vs. detailed faces).
2. **The "Prop" Anchor:** A stick figure alone cannot convey complex coaching metaphors. The prompt engine forces the inclusion of one highly detailed, photorealistic "prop" (e.g., "a shattered mirror"). This stylistic collision (simple stick figure + realistic prop) creates a distinct, recognizable aesthetic brand.

---

## 4. Implementation Plan

### Stage 1: The Visual Reasoning Protocol
*Script:* `commands/v2ws-render.md` -> Grant
*Inputs:* Script Segment (`"Stop letting your fear of rejection build a prison around you."`)
*Outputs:* `Visual_Prompt_JSON` (Emotion, Pose, Prop).
*Failure Condition:* Grant hallucinates a complex multi-character scene instead of a solitary stick figure.
*Receipt Write:* Write Receipt Block per FR47 `Receipt_Block_N.json` schema: `{ receipt_id, previous_receipt_hash, input_payload_hash, output_payload_hash, stage_name, timestamp, agent_name }` # REVISED: Standardizing receipt format across all specs per FR47 cryptographic schema.

**Steps:**
1. Grant scans the provided script line.
2. It identifies the core emotional register (e.g., `Anxiety/Paralysis`).
3. It selects an allegorical prop (e.g., `a heavy iron cage`).
4. It dictates the pose (e.g., `sitting inside, hugging knees`).

### Stage 2: T2I Collage Generation
*Script:* `commands/v2ws-render.md` -> External API
*Inputs:* `Visual_Prompt_JSON`, `Coach_Brand_Config`.
*Outputs:* Raw `<image.jpg>` (with white background).
*Failure Condition:* The T2I engine generates a patterned or colored background, ruining the downstream alpha mask.
*Receipt Write:* Write Receipt Block per FR47 `Receipt_Block_N.json` schema: `{ receipt_id, previous_receipt_hash, input_payload_hash, output_payload_hash, stage_name, timestamp, agent_name }` # REVISED: Standardizing receipt format across all specs per FR47 cryptographic schema.

**Steps:**
1. Grant maps the variables into the master T2I template:
   `"A simple stick figure showing [Emotion], [Pose]. The figure is interacting with a highly detailed, photorealistic [Prop]. Stick figure is drawn in [Color]. No shadows on the floor. Background must be ABSOLUTE PURE WHITE #FFFFFF. Collage art style."`
2. Grant sends the prompt to Dall-E 3 / Midjourney via the respective API.
3. The image is downloaded temporarily to `/tmp/render_{id}.jpg`.

### Stage 3: Alpha Extraction (Background Removal)
*Script:* `core/render_engine.py` (Local Python)
*Inputs:* Raw `<image.jpg>`.
*Outputs:* Transparent `<image.png>` (`DEP-ENG-031` Base64).
*Failure Condition:* The `rembg` engine accidentally deletes the stick figure's white torso because the boundary contrast was too low.
*Receipt Write:* Write Receipt Block per FR47 `Receipt_Block_N.json` schema: `{ receipt_id, previous_receipt_hash, input_payload_hash, output_payload_hash, stage_name, timestamp, agent_name }` # REVISED: Standardizing receipt format across all specs per FR47 cryptographic schema.

**Steps:**
1. Grant passes the file to a local python script running `rembg` (U-2-Net architecture).
2. The script processes the image, converting all `#FFFFFF` and near-white pixels to `alpha=0`.
3. The script applies a 1-pixel edge dilation to prevent white-halo fringing.
4. The output is encoded into a Base64 string for JSON transit.
5. The temporary file in `/tmp/` is deleted (ADR-01 compliance).

### Stage 4: DEP-ENG-031 Emit # REVISED: Replaced entirely. Removed Excalidraw injection logic to respect boundary.
*Output:* `DEP-ENG-031` — Base64 transparent PNG string.
*Action:* Serialize the alpha-extracted PNG as Base64.
*Write:* Write to the dependency layer for FR35 consumption.
*Failure Condition:* Base64 serialization fails or output string is empty → halt and alert operator.
*Receipt Write:* `COLLAGE-EMIT-{asset_id}-{timestamp}` # REVISED: Added missing specific receipt format.

---

## 5. Primary Output Schema (DEP-ENG-031)

**Schema Name:** `transparent_collage_base64.txt` # REVISED: Output is now a raw Base64 string payload, not an Excalidraw-wrapped JSON schema.

```text
data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAgAAAAIACAYAAAD...
```

---

## 6. Backward Compatibility Fallback
If the alpha extraction engine (`rembg`) fails due to a dependency crash, Grant catches the error. Rather than failing the webinar generation or outputting a PNG with a jagged, broken background, Grant gracefully skips the masking phase. The image remains a standard flat JPEG. Grant passes a flag back to Benjamin `{"transparency_failed": true}`. Benjamin catches this flag and draws a physical, branded picture-frame `rectangle` around the JPEG in Excalidraw to make the white background look like an intentional polaroid design choice.

---

## 7. Tasks

- [ ] **Task 1:** Build the LLM reasoning payload inside Grant's logic `commands/v2ws-render.md` to reliably extract exactly 1 Emotion, 1 Pose, and 1 Real-World Prop from arbitrary coaching script segments.
- [ ] **Task 2:** Hardcode the critical negative prompts (`"no gradients, no floor shadows, no background objects, pure white #FFFFFF"`) into the master T2I string execution sequence.
- [ ] **Task 3:** Deploy the Python `rembg` library within the local environment, writing a wrapper script that accepts a file path, strips the background, and returns the Base64 sequence in under 3 seconds.
- [ ] **Task 4:** Implement the 1-pixel edge dilation (defringing) logic inside the python wrapper to prevent the stick figures from having nasty white outlines when placed on dark excalidraw backgrounds.
- [ ] **Task 5:** Write the fallback `"polaroid"` frame generation logic in Benjamin's compilation step if the `transparency_failed` flag is thrown.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Visual Reasoning Protocol):** Feed Grant the script line: "You are setting your money on fire." Grant outputs `Emotion: Recklessness`, `Pose: standing`, `Prop: a burning pile of 100 dollar bills`. *Failure Example:* Grant outputs `Prop: none`, resulting in a boring, non-metaphorical generic stick figure.
- [ ] **AC2 (GMG 03 Visual Adherence):** Generate 5 images across a single webinar session. Assert that the core stick figure hex code (`#111827`) is identical across all 5 generated images. *Failure Example:* Image 1 has a blue stick figure, Image 2 has a red stick figure, violating the visual consistency guidelines and fracturing presentation continuity.
- [ ] **AC3 (Clean Alpha Masking):** Generate the T2I image. Run the background extractor. Overlay the resulting PNG on a pure `#000000` (black) test canvas. Execute an automated pixel-scan along the edge boundary of the stick figure. Assert there are 0 solid white (`#FFFFFF`) pixels remaining on the outer edge. *Failure Example:* Fringing is detected, making it obvious to the audience that the image was poorly cut out from a white background.
- [ ] **AC4 (Fallback Grace):** Introduce a simulated failure in the `rembg` library. Run the generation. Assert the final Excalidraw JSON still renders the image successfully, but places it inside a styled rectangle frame with a thick stroke instead of floating. *Failure Example:* The JSON compiler crashes, deleting the visual entirely and leaving a blank space on the slide.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| T2I Engine | External | Dall-E 3 / Midjourney for generative base layer. |
| `rembg` (U-2-Net) | Internal | Crucial for programmatically generating transparency without human intervention. |
| GMG Expert 03 Guidelines | Architecture | Required to inform the negative prompts and style locks. |
| Receipt Chain Guard | Infrastructure | Non-negotiable sequence auditing. |

---

## 10. Testing Strategy

### Unit Tests
- **Background Variance Test:** Programmatically generate 50 T2I images using the hardcoded prompt. Run an automated color variance check on the four corners of every image. Assert 100% of the tested pixels return `#FFFFFF`, proving the LLM is reliably suppressing messy background generations.
- **Base64 String Integrity:** Validate the output base64 strings against a standard Image magic decoder. Assert the bytes correspond to a valid PNG header format.

### Integration Tests
- **The End-to-End Render Loop:** Trigger the `Visual Reasoning Protocol` with a sample sentence. Allow it to hit the T2I API, download to `/tmp`, alpha-extract, encode to JSON, and load into a virtual Excalidraw instance. Assert the final bounding box size corresponds correctly to the aspect ratio of the generated image.

### Safety Tests (ADR-01 Quarantine Security)
- **Local Sandbox Clearance:** Execute the pipeline. Allow the `/tmp/` file to be created. Assert that the moment the Base64 json is generated, the `<image.jpg>` and `<image.png>` files on local disk are permanently deleted. *Failure Example:* Images pile up in a global `/tmp/` folder, allowing Coach A to potentially query or see Coach B's generated visual metaphors.
