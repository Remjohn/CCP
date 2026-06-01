# Tech-Spec: FR35 — Unified Excalidraw Pipeline & Transparent Collage (DEP-ENG-030)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v4.0 / Unified PRD v3.1)
**Architecture Reference:** Architecture_Synthesis_Report, PRD §6.6.4
**Skill Implementation:** `skills/visual/excalidraw-composer/SKILL.md`, `commands/v2ws-render.md`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\prd TO UPDATE.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\Architecture_Synthesis_Report.md`

---

## 2. Overview

### Problem Statement
In traditional AI content generation pipelines, text output (LLM) and visual output (T2I) remain stubbornly isolated. A system might generate a great script and a great image, but integrating them natively into a branded, cohesive presentation slide requires tedious manual Figma/Canva manipulation. Furthermore, AI image generators produce flat, square `.jpeg`/`.png` files with embedded backgrounds, forcing coaches to use ugly grid layouts instead of dynamic, overlapping visual storytelling.

### Solution
FR35 defines the **Unified Excalidraw Pipeline (DEP-ENG-030)**, orchestrated by Benjamin (The Excalidraw Composer) and Grant (Render Controller). The CCP standardizes *all* long-form visual outputs (Webinars, Tierlists, Ratings, Reactions) into a single delivery format: native `.excalidraw` JSON. This allows Benjamin to arrange text, shapes, and images programmatically mapped to the coach's brand hex codes. Crucially, the system utilizes the **Transparent Collage Pipeline (FR19a)**. It generates emotion-driven AI stick figures on pure white backgrounds, runs an automated alpha-extraction to strip the background, and injects the resulting transparent PNG directly onto the Excalidraw canvas to float naturally alongside the text.

### Scope
**In scope:**
- Stage 1: Generative Layout Parsing (Benjamin).
- Stage 2: The Visual Reasoning Protocol (Emotion & Object mapping).
- Stage 3: The Transparent Collage Pipeline (T2I + Alpha Extraction by Grant).
- Stage 4: Unified `.excalidraw` JSON Assembly.

**Out of scope:**
- T2I prompt generation, stick figure illustration generation, and alpha-extraction (owned by FR36). # REVISED: Excluding generative asset logic explicitly to honor boundary with FR36.
- Rendering the `.excalidraw` file to `.mp4` video. The pipeline yields the presentation deck.
- The base scripts (Webinars vs. Tierlists are generated upstream by Artisan; Benjamin only renders).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-030` | Unified Excalidraw Payload | OUTPUT — The finalized visual presentation file containing branded UI shapes, script text, and transparent AI collages. |
| Benjamin | Excalidraw Composer | AGENT — Organizes the layout, translating semantic scripts into spatial coordinates. |
| Grant | Render Controller | AGENT — Controls the T2I engines and the Alpha Extraction layer. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Multimedia Learning (Spatial Contiguity Principle)** | Richard Mayer | 2001 | Students learn better when corresponding words and pictures are presented near each other rather than far from each other on the page or screen. By using a programmatic JSON canvas, Benjamin can dynamically adjust the X/Y coordinates of the transparent stick figures to physically point at or overlap the specific text they are reacting to, optimizing cognitive integration. |
| **Object Masking via Thresholding** | Otsu / General CV | 1979 | Alpha extraction works flawlessly when foreground-background variance is maximized. By prompting Midjourney/Dall-E to specifically generate stick figures on absolute `#FFFFFF` backgrounds, the alpha mask algorithm requires zero heuristic guessing to achieve a pixel-perfect transparent cutout. |

### Technical Decisions
1. **The GMG Expert 03 Inheritance:** The Transparent Collage Pipeline inherits exactly from the GMG Expert 03 visual consistency standards. The stick figures must use uniform stroke colors, lack complex borders, and maintain persistent illustration styles to prevent visual jarring between sequential slides.
2. **Text-Layer Independence:** Instead of rendering text *into* the PNGs directly (which LLMs are notoriously bad at), Benjamin renders the image separately from the text, placing them side-by-side using the native Excalidraw `text` node structure. This ensures perfect typography scaling and allows the coach to fix typos gracefully without regenerating the AI image.

---

## 4. Implementation Plan

### Stage 1: Generative Layout Parsing
*Script:* `skills/visual/excalidraw-composer/SKILL.md` (Benjamin)
*Inputs:* Approved JSON Script (e.g., from V2WS or Tierlist pipeline).
*Outputs:* `Spatial_Layout_Map` (Coordinate arrays).
*Failure Condition:* Benjamin assigns X/Y coordinates that overlap text blocks over each other.
*Receipt Write:* Write Receipt Block per FR47 `Receipt_Block_N.json` schema: `{ receipt_id, previous_receipt_hash, input_payload_hash, output_payload_hash, stage_name, timestamp, agent_name }` # REVISED: Standardizing receipt format across all specs per FR47 cryptographic schema.

**Steps:**
1. Benjamin consumes the upstream array of "Modules" or "Tiers."
2. Determines canvas strategy (e.g., horizontal slide sequence for Webinars OR vertical scrolling canvas for Tierlists).
3. Calculates bounding boxes using the Coach's brand hex codes payload for stroke/fill colors.

### Stage 2: Visual Reasoning Protocol
*Script:* `commands/v2ws-render.md` (Grant)
*Inputs:* Script Segment (e.g., "This mistake will cost you your marriage.")
*Outputs:* `Visual_Prompt_Object` (Emotion + Object).
*Failure Condition:* Fails to identify a core emotion, defaulting to "neutral".
*Receipt Write:* Write Receipt Block per FR47 `Receipt_Block_N.json` schema: `{ receipt_id, previous_receipt_hash, input_payload_hash, output_payload_hash, stage_name, timestamp, agent_name }` # REVISED: Standardizing receipt format across all specs per FR47 cryptographic schema.

**Steps:**
1. For each slide, Grant scans the semantic text.
2. Extracts the primary emotion (e.g., "Devastation", "Epiphany", "Frustration").
3. Selects a real-world object to anchor the stick figure (e.g., "A shattered hourglass").
4. Generates the T2I Prompt: *"A simple expressive stick figure showing Devastation, holding a highly detailed real-world shattered hourglass. Pure white background #FFFFFF. High contrast."*

### Stage 3: Illustration Asset Ingestion # REVISED: Replaced entirely to fix FR35 vs FR36 bounding.
*Script:* `core/render_engine.py` (Grant)
*Inputs:* `DEP-ENG-031` (Transparent PNG payload from FR36).
*Outputs:* Mapped Image object ready for injection.
*Failure Condition:* Fails to load or decode the Base64 string from the FR36 payload.
*Receipt Write:* Write Receipt Block per FR47 `Receipt_Block_N.json` schema: `{ receipt_id, previous_receipt_hash, input_payload_hash, output_payload_hash, stage_name, timestamp, agent_name }`
*Additional Receipt Write:* `EXCALIDRAW-ASSET-INJECT-{asset_id}-{timestamp}` # REVISED: Added missing specific receipt format.

**Steps:** # REVISED: Removed native T2I generation and Alpha Mask. FR35 is consumer only now.
1. Read the Base64 transparent PNG string from the FR36 output payload.
2. Inject directly as an image node into the `.excalidraw` JSON at the coordinates specified by the active slide template.

### Stage 4: Excalidraw JSON Assembly
*Script:* `tools/excalidraw_compiler.py` (Benjamin)
*Inputs:* `Spatial_Layout_Map`, `Text_Strings`, `Base64_Transparent_PNGs`.
*Outputs:* `DEP-ENG-030` (`.excalidraw` JSON file).
*Failure Condition:* JSON invalidation breaking Excalidraw import parser.
*Receipt Write:* Write Receipt Block per FR47 `Receipt_Block_N.json` schema: `{ receipt_id, previous_receipt_hash, input_payload_hash, output_payload_hash, stage_name, timestamp, agent_name }` # REVISED: Standardizing receipt format across all specs per FR47 cryptographic schema.

**Steps:**
1. Benjamin initializes the `{ "type": "excalidraw", "elements": [] }` schema.
2. Loops through the `Spatial_Layout_Map`.
3. Injects the branded rectangles and typography nodes using coordinates.
4. Injects the `"type": "image"` schema nodes referencing the alpha-extracted Base64 strings, positioning them seamlessly next to the text.
5. Saves and dispatches the payload via Telegram.

---

## 5. Primary Output Schema (DEP-ENG-030)

**Schema Name:** `unified_excalidraw_payload.json`

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "ccp_benjamin_unified",
  "elements": [
    {
      "type": "rectangle",
      "x": 0,
      "y": 0,
      "width": 1920,
      "height": 1080,
      "backgroundColor": "#f9fafb",
      "strokeColor": "#111827",
      "groupIds": ["slide_1"]
    },
    {
      "type": "text",
      "text": "The 3 Pillars of Burnout",
      "fontSize": 48,
      "fontFamily": 1,
      "textAlign": "center",
      "x": 960,
      "y": 200,
      "strokeColor": "#111827"
    },
    {
      "type": "image",
      "version": 1,
      "versionNonce": 54321,
      "x": 400,
      "y": 400,
      "width": 800,
      "height": 600,
      "fileId": "collage_image_01",
      "status": "pending"
    }
  ],
  "appState": {
    "viewBackgroundColor": "#ffffff"
  },
  "files": {
    "collage_image_01": {
      "mimeType": "image/png",
      "id": "collage_image_01",
      "dataURL": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA..."
    }
  }
}
```

---

## 6. Backward Compatibility Fallback
If the Alpha Extractor (`rembg`) fails due to a dependency error or a T2I background hallucination (the background wasn't pure white), Benjamin falls back to placing the image inside a styled container box. Instead of an ugly float, it wraps the `image` node in a `rectangle` node with a heavy drop shadow and a caption, ensuring the layout remains aesthetically polished despite the loss of transparency.

---

## 7. Tasks

- [ ] **Task 1:** Build the `Visual Reasoning Protocol` inside Grant's logic to reliably parse a single emotion and a contrasting real-world object from an arbitrary script text block.
- [ ] **Task 2:** Update the T2I prompting schema to strictly enforce the `"pure absolute #FFFFFF white background. no gradients. no shadows"` negative prompting constraints required for alpha extraction.
- [ ] **Task 3:** Integrate a Python background-removal library (e.g., `rembg` using U-2-Net) capable of performing sub-second local alpha extraction on incoming T2I files.
- [ ] **Task 4:** Expand the `excalidraw_compiler.py` to handle the `files` object dictionary required to embed binary data into the `.excalidraw` schema correctly.
- [ ] **Task 5:** Map Coach-Specific JSON Brand configurations (Font Family, Background Hex, Accent Hex) directly into the Benjamin coordinate layout generator.

---

## 8. Acceptance Criteria

- [ ] **AC1 (The Transparent Collage):** Feed a script line about "anxiety" to the pipeline. Grant generates a stick figure holding a fraying rope on a white background. The pipeline extracts the background. Assert that the final base64 image array contains `RGBA` values where the edge boundary pixels possess `alpha < 10`, confirming a clean, transparent cutout. *Failure Example:* The system outputs a standard JPEG with a white bounding box, breaking the seamless design.
- [ ] **AC2 (Unified Cross-Format Export):** Feed the pipeline an explicitly formatted `Tierlist_JSON` array. Benjamin successfully routes it to a vertical scrolling Excalidraw Layout. Feed it a `V2WS_JSON` array. Benjamin successfully routes it to a horizontal slide sequence Layout. *Failure Example:* Benjamin hard-codes logic specifically to Webinar layouts, causing a Tierlist generation to bizarrely stack 6 tiers horizontally off-screen.
- [ ] **AC3 (Brand Consistency):** Connect the pipeline to Coach B's tenant (Brand Hex: `#FF5733`). Run a generation. Assert that `100%` of stroke and background metadata objects in the JSON payload correspond exclusively to Coach B's color palette. *Failure Example:* The system defaults to standard black and white grids, failing the white-label requirement.
- [ ] **AC4 (Excalidraw Native Embedding):** Render the final file. Drop it into `excalidraw.com`. Double click a text node. Assert that the text is fully editable natively by the human operator. *Failure Example:* The system rasterizes the entire layout into a single uneditable flat image file inside the Excalidraw canvas.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| T2I Engine | External | Required for generating the raw stick figure matrix. |
| `rembg` (U-2-Net) | Internal | Required for programmatic local alpha-masking. |
| `coach_brand.json` | Database | Required to inform all Excalidraw styling metadata. |
| Receipt Chain Guard | Infrastructure | Non-negotiable sequence auditing. |

---

## 10. Testing Strategy

### Unit Tests
- **Alpha Masking Stress Test:** Run the `rembg` Python script over 100 generated T2I stick figures. Calculate the histogram frequency of white pixels remaining post-process. Assert that total white-background pixel retention is `<1%` with no foreground destruction.
- **Brand Hex Override Test:** Inject mock `{ "primary_color": "random_hex_string" }` definitions into Benjamin's payload. Assert that the resulting `.excalidraw` JSON perfectly matches the injected string dynamically.

### Integration Tests
- **Generator to Composer E2E:** Spin up Artisan to write a 3-part script. Direct output via LangGraph to Benjamin and Grant. Assert the system completes the sequence—writing, T2I generation, extraction, layout, and `.excalidraw` file save—without throwing a threading timeout or JSON syntax schema exception.

### Safety Tests (ADR-01 Quarantine Security)
- **Tenant Asset Segregation:** Execute a generation for Coach A. Assert that at no point in the `tmp/` alpha-extraction pipeline are Coach A's generated image assets exposed globally via URL, nor saved with deterministic file names that Coach B could intercept. All intermediate PNGs must be instantly overwritten or protected by cryptographically secure hashing.
