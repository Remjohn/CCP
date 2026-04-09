# Tech-Spec: FR-VIS-18 — Spatial Composition Engine (Geometrics Pipeline)

**Created:** 2026-04-07
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §Visual Intelligence Pipeline, CVE_Documentation_V3 §2.6, Conscious_Typography_Architecture.md
**Skill Implementation:** Geometrics Pipeline (SAM 3 → Pretext → Rough.js → Skia/CanvasKit)
**Role Executing:** Principal CCP Tech-Spec Architect
**Supersedes:** FR-VIS-05 Canvas Composition & Delivery (Fabric.js rendering layer only — approval workflow preserved)

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md` — FR-VIS-18 definition scope (Visual Intelligence Pipeline)
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CVE_Documentation_V2.md` — §6 30 Visual Design Architecture Specifications (SPEC-01 through SPEC-30), §8 Conscious Canva App Architecture
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CVE_Documentation_V3.md` — §2.6 Complete Pipeline Execution Sequence, §4 Image Research Architecture (Aurore + 9 composable skills)
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\Conscious_Typography_Architecture.md` — Full Geometrics Pipeline specification: Pretext Engine, SAM 3 integration, Bin Packing, Rough.js, Skia/Remotion rendering
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\Parametric_Template_Feasibility.md` — 3 validated Parametric Template definitions (Authority Split, In-World Surface, Whiteboard Notebook)
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\MCDA_Geometrics_vs_CVE_Principles.md` — MCDA validation: Geometrics Pipeline vs CVE V2/V3 visual principles (5/5 on all criteria)
- `d:\Work\The Conscious Coaching Factory\Open-source editors CanvasKit.md` — CanvasKit/Skia vs Fabric.js evaluation, 12 advanced visual styles, shader gradient analysis
- `d:\Work\The Conscious Coaching Factory\docs\MCDA_Canva_Clone_vs_Papers.md` — Layout Resolver gap analysis, SmartSlide Object Model
- `d:\Work\The Conscious Coaching Factory\docs\architecture\FR-VIS-05_Canvas_Composition_Delivery_Tech_Spec.md` — Predecessor spec (Fabric.js-based canvas composition, approval controls, seamless carousel export)
- `d:\Work\The Conscious Coaching Factory\docs\architecture\FR50_Sovereign_Image_Rule_Tech_Spec.md` — Reference template for spec format

---

## 2. Overview

### Problem Statement
The current CVE pipeline (FR-VIS-01 through FR-VIS-17) generates Visual Composition Briefs (VCBs), resolves images via the 4-Tier Sourcing Hierarchy, and validates outputs through the AGSS scoring system. However, the critical gap between Art Direction and Final Pixel Placement remains unresolved. The Conscious Canva App (FR-VIS-05) uses Fabric.js — a UI-first library built on standard HTML5 `<canvas>` — which structurally cannot:

1. **Enforce Face Priority (SPEC-06):** Fabric.js cannot "see" where a subject's face is positioned. Text placement relies on static zone templates, not dynamic collision detection against semantic image content.
2. **Execute Chromatic Bloom (SPEC-03, SPEC-05):** Standard canvas gradients produce banding artifacts at high saturation values. GPU-native shaders are required for smooth cinematic color transitions across carousel arcs.
3. **Generate Intentional Imperfection (SPEC-21):** Fabric.js renders geometrically perfect shapes. Emulating human-drawn strokes requires pre-baked PNG overlays — not mathematically randomized vector wobble.
4. **Perform Perspective Mapping:** Text cannot be warped onto 3D surfaces (cardboard signs, phone screens, notebooks) detected in AI-generated images.
5. **Scale Parametric Templates:** Complex layouts (tier lists, masonry grids, particle scatter backgrounds) require algorithmic bin packing — not manual element placement.

The result: operators spend 15-30 minutes per composition manually adjusting elements that should be mathematically determined, and the output quality ceiling is limited by HTML5 canvas rendering capabilities.

### Solution
FR-VIS-18 defines the **Spatial Composition Engine** — a headless, geometry-first rendering pipeline that replaces DOM-based canvas rendering with deterministic coordinate algebra. The pipeline treats all visual elements (text, images, decorations) as mathematical polygons on a 2D Cartesian plane, resolves their spatial relationships algorithmically, and renders the final composition via GPU-accelerated Skia.

The pipeline executes in four sequential stages:
1. **SAM 3 Saliency Analysis:** Extracts subject masks, text safe zones, and surface polygons from resolved images.
2. **Pretext Typography Measurement:** Calculates exact bounding boxes for all text elements without DOM rendering.
3. **Layout Resolution:** Applies parametric template rules, bin packing, and collision detection to produce absolute `[X, Y, W, H]` coordinates for every element.
4. **Skia/CanvasKit Rendering:** Paints the mathematically perfected layout using GPU-native gradients, blend modes, shaders, and Rough.js organic styling.

### Scope
**In scope:**
- SAM 3 saliency analysis service (`POST /api/saliency/analyze`).
- Pretext typography measurement service (`POST /api/typography/measure`).
- Layout Resolver engine with parametric template library (`POST /api/layout/resolve`).
- Skia headless rendering service (`POST /api/render/compose`).
- Rough.js organic decoration layer integration.
- Parametric Template schema and initial template library (Authority Split, In-World Surface, Whiteboard Notebook).
- Homography warp for in-world surface text placement.
- CanvasKit WebAssembly frontend preview integration for the Canva Clone editor.
- Variant generation system (3-10 variants per composition for Qwen2-VL scoring).

**Out of scope:**
- Approval workflow (preserved from FR-VIS-05 — not modified).
- Notion delivery (handled by FR-VIS-06).
- Visual validation scoring (handled by FR-VIS-04, extended with Llama-3.2-Vision NIM variant scoring).
- Remotion kinetic typography video pipeline (future FR-VIS-19).
- Full Canva Clone Fabric.js → CanvasKit migration (future Phase 7 engineering sprint).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-VIS-005` | Visual Composition Brief Schema | INPUT — VCB drives template selection, text content, image type, PSSL parameters. |
| `DEP-VIS-015` | Parametric Template Library | NEW — Template definitions (YAML) consumed by Layout Resolver. |
| `DEP-VIS-016` | Saliency Analysis Output Schema | NEW — SAM 3 mask polygons, safe zones, surface quadrilaterals. |
| `DEP-VIS-017` | Typography Measurement Output Schema | NEW — Pretext bounding boxes, line-break indices, shrink-wrap dimensions. |
| `DEP-VIS-018` | Resolved Layout Coordinate Map | NEW — Final `[X, Y, W, H]` per element, ready for rendering. |
| `DEP-ENG-041` | Receipt Chain Guard | AUDIT — All pipeline stages produce cryptographic receipt hashes. |
| `FR-VIS-01` | VCB Generation (Abel) | UPSTREAM — Produces the VCB that drives composition. |
| `FR-VIS-04` | Visual Validation | UPSTREAM — Only validated images enter the pipeline. DOWNSTREAM — Variant scoring. |
| `FR-VIS-05` | Canvas Composition & Delivery | SIBLING — Approval workflow and Canva Clone UI preserved; rendering layer upgraded. |
| `FR-VIS-07` | Format & Aspect Ratio Enforcement | UPSTREAM — Templates use locked dimensions from format envelope. |
| `FR-VIS-09` | Image Sourcing Hierarchy | UPSTREAM — Resolved images (Tier 1-4) enter saliency analysis. |
| Cloudflare R2 | External | Asset storage for rendered compositions and variant previews. |

### Academic Grounding

| Algorithm / Framework | Author / Source | Year | Mechanism / Concept Applied |
|---|---|---|---|
| **Pretext Layout Engine** | @chenglou (React Core Team) | 2025 | DOM-less, sub-millisecond text measurement and line-wrapping. Enables binary-search font scaling (5,000 iterations < 400ms) for mathematically perfect container fill without widows or orphans. Returns absolute bounding boxes per line, enabling coordinate-precise text placement in headless environments. |
| **SAM 3 — Segment Anything with Concepts** | Meta FAIR | 2025 | Zero-shot semantic segmentation using natural language concepts. Agent queries: "Segment the person's face and upper body" → pixel-perfect alpha mask polygon. Enables programmatic Text Safe Zone extraction, subject collision detection, and surface quadrilateral detection for perspective text mapping. |
| **2D Bin Packing (MaxRects Heuristic)** | Jylänki, J. | 2010 | Arranges N heterogeneous rectangles (text boxes, icons, images) into a larger bounding rectangle (canvas) without overlap, minimizing wasted negative space. Applied to tier list automation, masonry grid layouts, and multi-element infographic composition. |
| **Force-Directed Graph Layout** | Fruchterman & Reingold | 1991 | Treats text boxes as charged particles that repel each other (20px minimum buffer), expanding outward until thermodynamic equilibrium. Applied to diagram node placement for mind maps and flow charts. |
| **Rough.js Organic Rendering** | Preet Shihn | 2019 | Mathematically displaces SVG path control points using configurable `roughness` (1.5-2.5 optimal for coaching) and `bowing` parameters, transforming algebraic geometry into hand-drawn marker aesthetics. Powers the "Intentional Imperfection" mandate (SPEC-21). |
| **Skia 2D Graphics Engine** | Google | 2005-present | C++ GPU-accelerated 2D rendering engine (powers Chrome, Android, Flutter). Supports native GLSL Fragment Shaders, Photoshop-level blend modes (Multiply, Overlay, Color Burn), Gaussian blur, and homography perspective transforms. CanvasKit provides identical capabilities via WebAssembly in browsers. |
| **ColorThief K-Means Clustering** | Lokesh Dhakar | 2012 | Extracts dominant color palette (5 hex codes) from image via K-Means clustering of pixel hue-saturation distribution. Enables programmatic, contrast-aware color palette generation for text fill rules and WCAG AAA compliance. |
| **Homography / Perspective Transform** | Hartley & Zisserman | 2003 | 3×3 transformation matrix mapping 4 source points (flat rectangle) to 4 target points (tilted quadrilateral from SAM 3). Enables perspective-correct text placement on detected surfaces (cardboard signs, phone screens, whiteboards). |

### Technical Decisions

1. **SAM 3 Before Pretext (Image Dictates Text, Not Reverse):** The pipeline resolves image saliency first because the image's spatial constraints determine where text can physically exist. Running Pretext first would produce text bounding boxes that may collide with undiscovered subjects. This ordering mirrors how a human Art Director thinks: look at the image → identify safe zones → place text within constraints.

2. **Skia Over Fabric.js for Rendering:** Fabric.js is a UI manipulation library optimized for drag-and-drop interactions not rendering fidelity. Skia is the literal C++ graphics engine powering Google Chrome. Skia executes GPU-native Fragment Shaders (cinematic VFX), native Photoshop blend modes (Multiply, Color Burn), perspective transforms (homography warp), and Perlin noise generation for paper textures — none of which are achievable in standard HTML5 canvas without severe artifacting. See `MCDA_Geometrics_vs_CVE_Principles.md` for full evaluation matrix (5/5 on all CVE criteria).

3. **Parametric Templates Over Static PSD Layers:** Templates are defined as YAML constraint documents — not rigid Photoshop files. This enables: (a) dynamic font scaling via Pretext binary search, (b) dynamic zone adjustment based on SAM 3 subject mask dimensions, (c) infinite template composition via parametric component inheritance, and (d) version-controlled template evolution without designer intervention.

4. **Variant Generation for Scoring:** The pipeline generates 3-5 layout variants per composition (varying font scale, element positioning within safe zones, decoration intensity). All variants are rendered in < 1 second total via Skia headless. Llama 3.2 90B Vision Instruct via NIM (Visual Validation Agent extension) scores variants on readability, balance, attention flow, and aesthetic heuristics, selecting the highest-scoring variant automatically. This replaces single-shot rendering that relies on template rigidity for quality.

5. **Hybrid Frontend (Fabric.js UI + Skia Preview):** The Canva Clone retains Fabric.js for drag-and-drop UI interactions (element selection, dragging, panel controls). When the operator makes a change, the updated JSON is sent to the backend Skia service, which returns a high-fidelity WebP preview in < 200ms. This ensures 0% preview-to-export divergence — what the operator sees in the editor is pixel-identical to the final 4K export.

### Constraint Precedence Hierarchy (CPH)

The following hierarchy resolves all mutually exclusive rule conflicts identified through CBAR (Constraint-Based Adversarial Reasoning) stress testing. When two rules cannot both be satisfied simultaneously, the higher-ranked rule takes precedence. Every pipeline stage MUST consult this hierarchy before emitting a `COLLISION_UNRESOLVABLE` or `PROVISIONAL` flag.

**CPH-1 — Subject Mask Integrity supersedes Typography Minimum Scale (resolves CBAR-1).**
The SAM 3 subject mask is an inviolable boundary. If Pretext hits `font_size_range.min` and the resulting bounding box still intersects the subject mask by any amount, the Layout Resolver MUST NOT nudge text over the face. Instead, the resolver executes the following escalation chain: (a) shrink `text_zone_width` by 5% and re-invoke Pretext; (b) if still overset, reduce `max_lines` by 1 and re-invoke Pretext; (c) if still overset after 3 re-invocations, flag the slide `COPY_REDUCTION_REQUIRED` and route to Abel (FR-VIS-01) for automatic copy shortening before re-entering the pipeline. The composition does NOT proceed to rendering with text overlapping the subject mask under any circumstance.

**CPH-2 — Chromatic Arc supersedes CIEDE2000 Stitch Threshold (resolves CBAR-2).**
The CVE Chromatic Bloom Arc is the narrative's emotional backbone. Flattening the Slide 3→4 saturation jump to satisfy `CIEDE2000 ≤ 15` would destroy the semiotic injection. Resolution: the CIEDE2000 threshold applies only to the **outermost 40px edge strip** of each slide, NOT to the full gradient. Skia MUST render a 40px **gradient bridge zone** on each stitch boundary — a micro-gradient that smoothly interpolates from Slide N's edge color to Slide N+1's edge color. The interior gradient stops (the actual chromatic arc) are untouched. The CIEDE2000 measurement is taken exclusively within this 40px bridge zone after interpolation. This preserves the dramatic saturation jump while eliminating the visible crease.

**CPH-3 — SAM 3 Depth Segmentation for Z-Index Occlusion (resolves CBAR-3).**
When a VCB requests an "In-World Text" depth composition (text partially obscured by a foreground element), the engine MUST issue a secondary SAM 3 query: `"Segment the foreground occluding element (arm, hand, object) separately from the background."` SAM 3 returns a foreground alpha mask. Skia then renders: (a) background image at `z=1`, (b) text at `z=2`, (c) foreground mask composited at `z=3` with `SrcOver` blend mode — creating the physical occlusion illusion. If SAM 3 cannot isolate the foreground element (confidence < 0.70), the slide receives a `PROVISIONAL / PENDING_HUMAN_REVIEW` status with flag `DEPTH_OCCLUSION_UNRESOLVABLE` and falls back to standard flat `z=4` text placement.

**CPH-4 — Rough.js Collision Buffer supersedes Nominal Bounding Box (resolves CBAR-4).**
The Pretext bounding box is a typographic measurement, not a decoration boundary. Rough.js organic paths are stochastic and will overshoot their nominal bounding box. Resolution: the Layout Resolver MUST apply a **decoration collision buffer** of `roughness × 8px` (e.g., roughness 2.5 = 20px buffer) to ALL Rough.js annotation bounding boxes before running collision detection against the SAM 3 subject mask. Additionally, the Skia render service MUST apply a `clipPath` derived from the subject mask polygon to ALL `rough_*` layer types — any Rough.js SVG path fragment that bleeds into the subject mask is hard-clipped at the mask boundary. The visual effect is an organic stroke that naturally "stops" at the subject's silhouette.

**CPH-5 — Readability supersedes Surface Realism for In-World Blend Modes (resolves CBAR-5).**
Text legibility is non-negotiable. When the Multiply blend mode causes homography-warped text contrast to fall below 4.5:1 (WCAG AA), the Skia renderer MUST execute the following mitigation: (a) sample the mean luminance of the SAM 3 surface quadrilateral; (b) if luminance < 30%, switch from `Multiply` to `HardLight` blend mode, which preserves surface texture while boosting text brightness; (c) if luminance < 15% (extreme shadow), insert a semi-transparent white rectangle (`opacity: 0.3`) beneath the text layer but above the surface, then apply `Multiply` — creating a "lightened surface patch" that maintains realism while ensuring readability. Llama-3.2-Vision NIM variant scoring receives all blend-mode variants and selects the one with the highest combined realism + readability score.

**CPH-6 — Quality Gate supersedes Batch Automation Clock (resolves CBAR-6).**
A low-scoring asset MUST NEVER be force-published to a coach's feed. The `PROVISIONAL / PENDING_HUMAN_REVIEW` status is absolute. Resolution for the batch automation conflict: when the variant scorer peaks below 6.5 during an automated batch run, the engine MUST (a) emit a `SCE_VARIANT_EXHAUSTION` webhook to the Notification module (Telegram alert to operator) with the composition ID and highest variant score; (b) automatically re-queue the composition with `variant_count: 10` (expanded exploration) and `roughness_range: [0.5, 3.5]` (wider parameter sweep) for a single retry pass; (c) if the retry also fails, the composition enters `PENDING_HUMAN_REVIEW` and the batch scheduler substitutes a **reserve asset** from the coach's pre-approved content vault (living inside the production folder where all content produced assets live, if available) or skips the slot with a logged `SLOT_UNFILLED` event. The Monday posting queue is never left empty — it either contains a quality-validated asset or an explicit skip with operator notification.

**CPH-7 — Upstream AGSS Approval grants Saliency Override for Abstract Media (resolves CBAR-7).**
An image that has already passed FR-VIS-04 Visual Validation with an AGSS score ≥ 7.0 carries a **Validated Asset Trust** credential. When SAM 3 returns confidence < 0.70 on a Validated Asset, the engine MUST NOT hard-reject the image. Instead: (a) check if the VCB `image_type` is `environment_scene` or `abstract_illustration` — these types do not require subject segmentation, so the saliency gate is bypassed entirely and the Layout Resolver uses the full canvas as a single text safe zone; (b) for `character_*` image types, the low-confidence flag is downgraded from a hard block to a `PROVISIONAL / PENDING_HUMAN_REVIEW` advisory, and the Layout Resolver proceeds with a conservative full-canvas safe zone while logging `SALIENCY_OVERRIDE_AGSS_TRUST`. The `Spatial_Composition_Output.json` schema records this override in a new field: `"saliency_override": {"reason": "AGSS_TRUST", "upstream_agss_score": 8.9, "sam3_confidence": 0.58}`.

---

## 4. Implementation Plan

### Stage 1: SAM 3 Saliency Analysis
*Agent:* Saliency Analysis Service (`POST /api/saliency/analyze`)
*Inputs:* Resolved image URL (from Aurore's `image_resolution_map`), VCB slide `image_type`, saliency query intent.
*Outputs:* `DEP-VIS-016` — Saliency Analysis Output (subject mask polygon, text safe zone polygon, surface quadrilateral if applicable, confidence score).
*Failure Condition:* SAM 3 confidence < 0.70 for subject detection triggers a `PROVISIONAL / PENDING_HUMAN_REVIEW` status; image flagged for operator review.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. The Layout Resolver submits the resolved image URL and a natural language saliency query derived from the VCB `image_type`:
   - `environment_scene` → "Identify the largest visually calm, low-contrast negative space zone."
   - `character_specific_emotion` → "Segment the person's face and upper body. Return bounding box."
   - `character_brand_avatar` → "Segment the person. Return alpha mask polygon and gaze direction vector."
   - In-World Surface templates → "Segment the blank writable surface the person is holding. Return quadrilateral corners."
2. SAM 3 processes the image and returns coordinate arrays:
   ```json
   {
     "subject_mask": [[x1,y1], [x2,y2], ...],
     "subject_bbox": {"x": 340, "y": 120, "w": 420, "h": 980},
     "text_safe_zones": [
       {"x": 54, "y": 80, "w": 500, "h": 1190, "confidence": 0.91}
     ],
     "surface_quadrilateral": null,
     "gaze_direction": "upper_right",
     "confidence": 0.94
   }
   ```
3. Validation gate: if `confidence < 0.70`, check for **Validated Asset Trust** (CPH-7): if the image carries an upstream AGSS score ≥ 7.0 and `image_type` is `environment_scene` or `abstract_illustration`, bypass the saliency gate and use full canvas as text safe zone. For `character_*` types with AGSS trust, downgrade to advisory and proceed with conservative full-canvas safe zone (log `SALIENCY_OVERRIDE_AGSS_TRUST`). Otherwise, the slide receives a `PROVISIONAL / PENDING_HUMAN_REVIEW` status (flagged `SALIENCY_LOW_CONFIDENCE`) and is routed to operator review. The layout resolver does not proceed for that slide.
4. If a VCB requests an "In-World Text" depth composition requiring foreground occlusion (CPH-3), issue a secondary SAM 3 query: `"Segment the foreground occluding element separately."` Return the foreground alpha mask alongside the primary saliency output for Z-index compositing in Stage 4.
5. The saliency output is cached in Redis (TTL: 24h) keyed by image hash — re-analysis of the same image is avoided.

### Stage 2: Pretext Typography Measurement
*Agent:* Typography Measurement Service (`POST /api/typography/measure`)
*Inputs:* VCB `typography` field per slide (font family, weight, size range, max lines, text content), text safe zone dimensions from Stage 1.
*Outputs:* `DEP-VIS-017` — Typography Measurement Output (bounding box per text element, line-break indices, optimal font size, line stats).
*Failure Condition:* Text overset — minimum font size still exceeds safe zone height. System requests copy reduction from Abel before rendering.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. For each text element in the VCB slide (headline, list items, CTA, brand handle):
   a. Pretext `prepare(text, font_family, font_weight)` — normalizes whitespace, calculates per-word widths.
   b. Binary search loop: starting at `font_size_range.max`, Pretext `layout(prepared, safe_zone_width)` — if `total_height > safe_zone_height`, reduce font size by 0.5px and retry. If `font_size < font_size_range.min`, throw `TEXT_OVERSET` exception.
   c. Rich-inline processing: for tribal nouns identified in `hook_concrete_nouns`, apply `prepareRichInline` with bolded weight + 2px `extraWidth` padding.
2. Output per text element:
   ```json
   {
     "element_id": "headline",
     "optimal_font_size": 48.5,
     "bounding_box": {"x": 54, "y": 80, "w": 486, "h": 172},
     "line_count": 3,
     "line_breaks": [4, 9, 14],
     "line_widths": [478, 462, 312],
     "shrink_wrap_width": 478
   }
   ```
3. For Rough.js annotations (underlines, highlights, circles): Pretext returns the exact start/end pixel coordinates of target substrings within the measured layout. These coordinates are stored in the typography output for the decoration layer.

### Stage 3: Layout Resolution (The Brain)
*Agent:* Layout Resolver Engine (`POST /api/layout/resolve`)
*Inputs:* VCB (template_id, arc_stage, composition rules), `DEP-VIS-016` (saliency output), `DEP-VIS-017` (typography measurement), parametric template definition from `DEP-VIS-015`.
*Outputs:* `DEP-VIS-018` — Resolved Layout Coordinate Map (absolute `[X, Y, W, H]` for every element, layer Z-order, effect parameters).
*Failure Condition:* Collision detected after 5,000 iterations; layout flagged `COLLISION_UNRESOLVABLE` for operator review.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Load parametric template from `DEP-VIS-015` by `template_id` from VCB.
2. Apply zone architecture: calculate absolute pixel coordinates for each zone (subject zone, text zone, brand bar zone) using template percentage rules and canvas dimensions.
3. Subject placement: if SAM 3 returned a subject mask, calculate centroid and apply rule-of-thirds snapping. If subject bleeds into text zone, trigger template `fallback` rule (shrink text zone width by 5%, re-run Pretext measurement).
4. Text placement: position each Pretext-measured text element within its assigned zone, applying the Absolute Centering Equation:
   `Item_Y = Zone_Y + (Zone_Height / 2) - (Item_Height / 2)`
5. Collision detection: verify no text bounding box intersects the SAM 3 subject mask polygon. If collision detected, nudge text along X/Y axes in 4px increments until intersection evaluates to `false`. If nudging fails because Pretext is at `font_size_range.min`, execute the CPH-1 escalation chain: shrink zone → reduce lines → route to Abel for copy reduction. The subject mask boundary is inviolable.
6. Decoration placement: calculate Rough.js annotation coordinates from Pretext substring positions. Apply the **decoration collision buffer** (CPH-4): expand each Rough.js annotation bounding box by `roughness × 8px` on all sides before running collision detection against the SAM 3 subject mask. This accounts for stochastic SVG path overshoot.
7. Effect parameter resolution: map VCB `chromatic_spec` to Skia gradient stops, map `intentional_imperfection` to Rough.js roughness values, map blend modes to Skia blend constants. For carousel exports, compute the 40px **gradient bridge zone** (CPH-2) at each slide stitch boundary.
8. Variant generation: produce 3-5 layout variants by varying font_size (±2px), text_zone padding (±8px), and decoration intensity (roughness ±0.5).
9. Output the complete coordinate map:
   ```json
   {
     "variant_id": "V1",
     "canvas": {"width": 1080, "height": 1350},
     "layers": [
       {"type": "gradient_background", "z": 0, "params": {...}},
       {"type": "image", "z": 1, "src": "r2://...", "bbox": [0, 0, 1080, 1350]},
       {"type": "subject_shadow", "z": 2, "params": {...}},
       {"type": "rough_rectangle", "z": 3, "bbox": [54, 600, 500, 60], "roughness": 2.0},
       {"type": "text", "z": 4, "content": "The 3am integrity check", "bbox": [54, 80, 486, 172], "font": "Montserrat", "size": 48.5, "weight": 800, "color": "#FFFFFF"},
       {"type": "rough_underline", "z": 5, "start": [54, 250], "end": [380, 250], "color": "#CC2222", "roughness": 2.5},
       {"type": "brand_handle", "z": 6, "bbox": [54, 1280, 200, 30]}
     ]
   }
   ```

### Stage 4: Skia Headless Rendering (The Hands)
*Agent:* Skia Rendering Service (`POST /api/render/compose`)
*Inputs:* `DEP-VIS-018` — Resolved Layout Coordinate Map (all variants), resolved image URLs.
*Outputs:* Rendered PNG/WebP per variant, uploaded to Cloudflare R2.
*Failure Condition:* Skia render timeout > 5 seconds per slide; service auto-retries once.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Create Skia surface at canvas dimensions (e.g., 1080×1350 for 4:5).
2. Iterate through `layers` array in Z-order (ascending):
   - `gradient_background`: Execute Skia `linearGradient()` or `radialGradient()` with VCB chromatic_spec stops. For cinematic effects, apply Perlin noise shader overlay at 4% intensity.
   - `image`: Load resolved image from R2. Apply Skia blend mode from VCB (default: `SrcOver`). For color grading: create solid color overlay from ColorThief dominant hue, composite with `Color` blend mode at 15% opacity.
   - `subject_shadow`: Render offset black rectangle with Gaussian blur (radius from template).
   - `rough_rectangle` / `rough_underline` / `rough_highlight`: Execute Rough.js with coordinate arrays. Rough.js outputs SVG path strings → Skia `drawPath()` consumes them directly. Apply `clipPath` from SAM 3 subject mask polygon (CPH-4) to hard-clip any organic path fragments that bleed into the subject mask.
   - `text`: Execute Skia `drawText()` at Pretext coordinates. Apply drop shadow (offset, blur, color from template). For rich-inline tribal nouns: render with weight override within the same text run.
   - `perspective_warp` (In-World Surface templates only): Compute homography matrix from Pretext flat rectangle corners to SAM 3 quadrilateral corners. Apply Skia `setPolyToPoly()` transform. Apply `Multiply` blend mode for surface texture bleed-through. If surface luminance < 30%, switch to `HardLight` blend mode (CPH-5). If luminance < 15%, insert semi-transparent white patch (`opacity: 0.3`) beneath text layer.
   - `depth_occlusion` (In-World Text depth compositions only, CPH-3): Render background image at `z=1`, text at `z=2`, then composite SAM 3 foreground alpha mask at `z=3` with `SrcOver` blend mode to create physical occlusion illusion.
   - `brand_handle`: Render coach name, handle, profile picture at locked coordinates.
3. Export each variant as WebP (quality: 95) to Cloudflare R2.
4. For carousels: render 40px **gradient bridge zone** (CPH-2) at each stitch boundary — a micro-gradient interpolating Slide N edge color to Slide N+1 edge color. Validate CIEDE2000 color distance ≤ 15 within the bridge zone only.
5. Return variant URLs to the scoring pipeline.

### Stage 5: Variant Scoring & Selection
*Agent:* Visual Validation Agent (FR-VIS-04 extension)
*Inputs:* 3-5 rendered variant images per slide.
*Outputs:* Selected variant ID, aesthetic score.
*Failure Condition:* All variants score below AGSS threshold 6.5; composition receives a `PROVISIONAL / PENDING_HUMAN_REVIEW` status for operator intervention.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Submit all variant images to Qwen2-VL scoring pipeline.
2. Score each variant on: readability (text contrast ratio), balance (visual weight distribution), attention flow (gaze direction alignment with text placement), aesthetic heuristics (AGSS threshold).
3. Select highest-scoring variant. If score ≥ 6.5: output `PASS` status, auto-approve for operator review. If score < 6.5: execute CPH-6 escalation — (a) emit `SCE_VARIANT_EXHAUSTION` webhook (Telegram alert to operator); (b) re-queue composition with `variant_count: 10` and `roughness_range: [0.5, 3.5]` for expanded retry; (c) if retry also fails, enter `PROVISIONAL / PENDING_HUMAN_REVIEW` and substitute a reserve asset from the pre-approved content vault (if available) or log `SLOT_UNFILLED`. The batch scheduler MUST never force-publish a sub-threshold asset.
4. Load selected variant into Canva Clone for operator final review.

---

## 5. Primary Output Schema

### Schema Name: `Spatial_Composition_Output.json`

```json
{
  "composition_id": "SCE-JP-20260407-001",
  "vcb_id": "VCB-JP-20260407-001",
  "template_id": "authority_split_v1",
  "pipeline_version": "geometrics_v1.0",
  "canvas_dimensions": {"width_px": 1080, "height_px": 1350, "aspect_ratio": "4:5"},
  "saliency_output": {
    "subject_bbox": {"x": 340, "y": 120, "w": 420, "h": 980},
    "text_safe_zones": [{"x": 54, "y": 80, "w": 500, "h": 1190}],
    "confidence": 0.94,
    "cache_key": "sha256:a7b3c9..."
  },
  "typography_output": {
    "headline": {"optimal_font_size": 48.5, "line_count": 3, "shrink_wrap_width": 478},
    "list_items": [{"text": "Bitch", "width": 112}, {"text": "Moan", "width": 98}]
  },
  "selected_variant": {
    "variant_id": "V3",
    "aesthetic_score": 7.8,
    "render_url": "https://r2.ccf-assets.com/render/sce-jp-001-v3.webp"
  },
  "all_variants": [
    {"variant_id": "V1", "score": 7.2, "url": "https://r2.ccf-assets.com/render/sce-jp-001-v1.webp"},
    {"variant_id": "V2", "score": 6.9, "url": "https://r2.ccf-assets.com/render/sce-jp-001-v2.webp"},
    {"variant_id": "V3", "score": 7.8, "url": "https://r2.ccf-assets.com/render/sce-jp-001-v3.webp"}
  ],
  "resolved_coordinate_map": {
    "layers": ["...full DEP-VIS-018 coordinate map..."]
  },
  "edge_bleed_validation": {
    "validated": true,
    "ciede2000_max": 12.3,
    "bridge_zone_applied": true
  },
  "saliency_override": null,
  "cph_resolutions": [],
  "variant_exhaustion_retry": false,
  "export_assets": {
    "individual_slides": ["https://r2.ccf-assets.com/export/sce-jp-001-s1.png"],
    "horizontal_stitch": "https://r2.ccf-assets.com/export/sce-jp-001-stitch.png",
    "zip_archive": "https://r2.ccf-assets.com/export/sce-jp-001-all.zip"
  },
  "receipt_chain_block": {
    "receipt_id": "RCB-SCE-20260407-001",
    "previous_receipt_hash": "sha256:1a2b...",
    "input_payload_hash": "sha256:c3d4...",
    "output_payload_hash": "sha256:e5f6...",
    "stage_name": "Spatial_Composition_Engine",
    "agent_name": "Layout_Resolver",
    "timestamp_utc": "2026-04-07T19:00:00Z"
  }
}
```

---

## 6. Backward Compatibility Fallback

If the Spatial Composition Engine is offline or experiencing issues:
1. The pipeline falls back to the existing FR-VIS-05 Fabric.js Canvas Composition flow.
2. VCBs are loaded into the Canva Clone with standard static template zones — no SAM 3 saliency, no Pretext binary search, no Skia rendering.
3. Operators manually adjust text placement and sizing using Fabric.js drag-and-drop controls.
4. The pipeline logs `SCE_UNAVAILABLE` and queues the composition for automatic re-processing when the engine restores.
5. All Fabric.js exports remain valid — the approval workflow (FR-VIS-05 Stage 4) is unmodified.

---

## 7. Tasks

- [ ] **Task 1:** Deploy SAM 3 saliency analysis microservice — implement `POST /api/saliency/analyze` endpoint with natural language query routing, polygon mask extraction, and Redis caching (24h TTL).
- [ ] **Task 2:** Implement Pretext typography measurement service — `POST /api/typography/measure` endpoint with binary search font scaling, rich-inline tribal noun processing, and TEXT_OVERSET exception handling.
- [ ] **Task 3:** Build Layout Resolver engine — parametric template loader, zone architecture calculator, Absolute Centering Equation, collision detection (SAM 3 mask intersection), and variant generator (3-5 variants per composition).
- [ ] **Task 4:** Build Parametric Template Library (`DEP-VIS-015`) — define YAML schema, implement initial 3 templates (Authority Split, In-World Surface, Whiteboard Notebook), build template validation and loading system.
- [ ] **Task 5:** Implement Skia headless rendering service — `POST /api/render/compose` endpoint using `skia-canvas` Node.js bindings. Implement gradient rendering, Rough.js SVG path consumption, text rendering at Pretext coordinates, and homography perspective warp.
- [ ] **Task 6:** Implement Rough.js organic decoration layer — rectangle, underline, highlight, and circle annotations. Map Pretext substring coordinates to Rough.js path inputs. Configure roughness (1.5-2.5), bowing (1.0-2.0), and stroke width parameters from template definitions.
- [ ] **Task 7:** Implement ColorThief palette extraction — K-Means dominant color extraction, localized luminance sampling under text bounding boxes, automatic text color inversion for WCAG AAA compliance.
- [ ] **Task 8:** Implement edge bleed validation for seamless carousel export — CIEDE2000 color distance calculation on 40px stitch boundaries (threshold ≤ 15).
- [ ] **Task 9:** Extend Visual Validation Agent (FR-VIS-04) with Qwen2-VL variant scoring — submit 3-5 variant images, score on readability/balance/attention/aesthetics, select highest-scoring variant.
- [ ] **Task 10:** Implement CanvasKit WebAssembly preview in Canva Clone — operator changes update JSON → backend Skia renders preview → WebP returned in < 200ms.
- [ ] **Task 11:** Implement homography perspective warp for In-World Surface templates — SAM 3 quadrilateral detection, Pretext flat text rendering, Skia `setPolyToPoly()` transform, Multiply blend mode for surface texture.
- [ ] **Task 12:** Integrate with Receipt Chain Guard (DEP-ENG-041) across all 5 pipeline stages.
- [ ] **Task 13:** Implement Constraint Precedence Hierarchy (CPH) — CPH-1 (subject mask escalation chain), CPH-2 (gradient bridge zone renderer), CPH-3 (depth occlusion via secondary SAM 3 foreground mask), CPH-4 (Rough.js collision buffer + clipPath), CPH-5 (adaptive blend mode for surface luminance), CPH-6 (variant exhaustion retry + reserve asset substitution + Telegram webhook), CPH-7 (AGSS Trust saliency override).
- [ ] **Task 14:** Implement reserve asset content vault integration — pre-approved fallback assets per coach, accessed during CPH-6 variant exhaustion events to prevent empty posting slots.

---

## 8. Acceptance Criteria

- [ ] **AC1 (SAM 3 Subject Detection):** Submit an image containing a coach portrait occupying the right 40% of the frame. Assert SAM 3 returns a subject bounding box with `confidence ≥ 0.70`. Assert the text safe zone returned does NOT intersect the subject bounding box. *Failure Example:* SAM 3 returns the entire image as a single zone with no subject differentiation.

- [ ] **AC2 (Pretext Font Scaling):** Submit text "STAY AWAY FROM PEOPLE WHO..." with `font_size_range: [42, 56]` and `max_lines: 3` into a 500px-wide safe zone. Assert Pretext returns an `optimal_font_size` within the range and exactly 3 lines of text. Assert `total_height` does not exceed the safe zone height. *Failure Example:* Pretext returns a 4-line layout that overflows the safe zone.

- [ ] **AC3 (Collision Detection):** Generate a layout where the initial text placement (from Pretext) overlaps with the SAM 3 subject mask by 40px. Assert the Layout Resolver automatically nudges the text until `intersection == false`. Assert the final text position maintains minimum 8px clearance from the subject mask boundary. *Failure Example:* The rendered image shows text overlapping the coach's face.

- [ ] **AC4 (Rough.js Organic Styling):** Render a Whiteboard Notebook template with `roughness: 2.0`. Assert the rendered rectangle has visually irregular edges (SVG path deviation > 1px from geometric ideal). Assert the underline annotation wobbles convincingly. *Failure Example:* The rectangle has perfectly straight edges indistinguishable from standard canvas rendering.

- [ ] **AC5 (Skia Gradient Rendering):** Render an Authority Split template with a diagonal linear gradient from `#1A0A0A` to `#8B3A00`. Assert no visible banding artifacts in the gradient at 1080×1350 resolution. Assert the gradient renders within 100ms. *Failure Example:* Visible color stepping/banding in the gradient background.

- [ ] **AC6 (Homography Perspective Warp):** Submit an image of a person holding a tilted cardboard sign. SAM 3 detects the surface quadrilateral. Pretext measures the text "How I made $100K FROM 1 POST". Assert Skia warps the text to match the cardboard's 3D perspective. Assert Multiply blend mode makes the cardboard texture visible through the text. *Failure Example:* Text appears as a flat rectangle floating on top of the image without perspective correction.

- [ ] **AC7 (Variant Generation & Scoring):** Generate 5 layout variants for a Relief Peak carousel slide. Assert all 5 variants render in < 2 seconds total. Assert Qwen2-VL scoring returns a numeric score per variant. Assert the highest-scoring variant is auto-selected. *Failure Example:* Only 1 variant is generated (no layout exploration).

- [ ] **AC8 (Seamless Carousel Export):** Export a 5-slide carousel. Assert edge bleed zones on adjacent slides have CIEDE2000 color distance ≤ 15. Assert individual slide PNGs are exactly 1080×1350px each. *Failure Example:* A jarring color discontinuity at the slide 2-3 boundary.

- [ ] **AC9 (CanvasKit Preview Parity):** Operator adjusts text position in the Canva Clone editor. Assert the backend Skia preview WebP returned within 200ms is pixel-identical to the final exported PNG at that position. *Failure Example:* The editor preview shows Fabric.js rendering with different anti-aliasing, gradient quality, or text metrics than the final Skia export.

- [ ] **AC10 (CVE Chromatic Bloom Enforcement):** Render a 5-slide Relief Peak carousel. Assert slide 1-2 saturation is 30-40% (cool). Assert slide 4 (semiotic injection) saturation is 68-78% (warm). Assert the gradient transitions are smooth with no banding. *Failure Example:* All 5 slides render at identical 50% saturation, violating the chromatic bloom arc.

- [ ] **AC11 (CPH-1: Subject Mask Inviolability):** Submit an image where SAM 3 detects a subject occupying 70% of the frame, leaving a text safe zone only 180px wide. Submit text "STAY AWAY FROM PEOPLE WHO MAKE YOU FEEL HARD TO LOVE" with `font_size_range: [36, 52]`. Assert the engine never renders text overlapping the subject mask. Assert the escalation chain triggers: zone shrink → line reduction → Abel copy reduction request. *Failure Example:* Text is painted over the coach's face because the font floor was reached.

- [ ] **AC12 (CPH-2: Gradient Bridge Zone):** Export a carousel where Slide 3 background is `hsl(210, 30%, 15%)` and Slide 4 is `hsl(25, 78%, 45%)` (semiotic injection). Assert the 40px stitch boundary contains a smooth gradient bridge. Assert CIEDE2000 within the bridge zone ≤ 15. Assert the interior gradient stops are NOT flattened. *Failure Example:* The chromatic arc is destroyed to satisfy CIEDE2000, or a visible crease appears at the boundary.

- [ ] **AC13 (CPH-4: Rough.js Collision Buffer):** Render a Whiteboard Notebook with `roughness: 2.5` where the Pretext bounding box has exactly 8px clearance from the SAM 3 subject mask. Assert the Rough.js SVG path does NOT cross the subject mask boundary (hard-clipped by clipPath). Assert the decoration collision buffer of 20px (2.5 × 8) was applied during layout resolution. *Failure Example:* A Rough.js red circle slashes across the subject's face.

- [ ] **AC14 (CPH-5: Adaptive Blend Mode):** Submit an In-World Surface image where the cardboard sign has luminance 12%. Assert the Skia renderer switches from `Multiply` to the `HardLight` + white patch mitigation. Assert text contrast ratio ≥ 4.5:1 in the final render. *Failure Example:* Black text on dark cardboard is invisible.

- [ ] **AC15 (CPH-6: Variant Exhaustion Recovery):** Configure variant scoring to return scores [4.2, 5.1, 5.8, 4.9, 5.3] for all 5 variants. Assert the engine emits `SCE_VARIANT_EXHAUSTION` webhook. Assert an expanded retry (10 variants) is automatically triggered. Assert the batch scheduler does NOT force-publish any sub-6.5 asset. *Failure Example:* A score-5.8 asset is auto-published to the coach's Instagram feed.

- [ ] **AC16 (CPH-7: AGSS Trust Saliency Override):** Submit an abstract watercolor image that received AGSS 8.9 from FR-VIS-04. SAM 3 returns confidence 0.58. Assert the saliency gate is bypassed for `environment_scene` image types. Assert `saliency_override` is populated in the output schema. *Failure Example:* A beautiful, pre-approved watercolor is hard-rejected by SAM 3 and never enters the pipeline.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| DEP-VIS-005 (VCB Schema) | Internal | INPUT — drives template selection and slot population. |
| DEP-VIS-015 (Parametric Template Library) | Internal | NEW — YAML templates consumed by Layout Resolver. |
| DEP-VIS-016 (Saliency Output) | Internal | NEW — SAM 3 mask polygons and safe zones. |
| DEP-VIS-017 (Typography Measurement) | Internal | NEW — Pretext bounding boxes and font metrics. |
| DEP-VIS-018 (Resolved Layout Map) | Internal | NEW — Final coordinates per element. |
| DEP-ENG-041 (Receipt Chain Guard) | Internal | AUDIT. |
| FR-VIS-01 (VCB Generation) | Internal | UPSTREAM — produces VCBs. |
| FR-VIS-04 (Visual Validation) | Internal | EXTENDED — variant scoring via Qwen2-VL. |
| FR-VIS-05 (Canvas Composition) | Internal | SIBLING — approval UI preserved. |
| FR-VIS-07 (Format Enforcement) | Internal | UPSTREAM — aspect ratio and dimension constraints. |
| FR-VIS-09 (Image Sourcing) | Internal | UPSTREAM — resolved images enter saliency analysis. |
| SAM 3 (Meta FAIR) | External | Zero-shot semantic segmentation model. |
| Pretext (@chenglou) | External | DOM-less typography measurement engine. |
| Rough.js | External | Organic hand-drawn SVG path generation. |
| Skia / skia-canvas | External | Headless GPU-accelerated 2D rendering. Node.js bindings. |
| CanvasKit (Skia Wasm) | External | Browser-side Skia for editor preview parity. |
| ColorThief | External | K-Means color palette extraction. |
| Cloudflare R2 | External | Asset storage for renders and variants. |
| Redis | External | Saliency output caching (24h TTL). |
| Qwen2-VL | External | Visual-language model for variant scoring. |

---

## 10. Testing Strategy

### Unit Tests
- **SAM 3 Mask Accuracy:** Provide 10 test images (5 with clear subjects, 5 with ambiguous compositions). Assert subject detection confidence ≥ 0.70 on clear images. Assert low-confidence flagging on ambiguous images.
- **Pretext Binary Search Convergence:** Provide 20 text strings of varying lengths (5-200 words) with font size ranges. Assert every string converges to an optimal font size within the range in < 100 iterations. Assert no TEXT_OVERSET on strings within the expected word count.
- **Collision Detection:** Provide 10 synthetic SAM 3 masks and 10 Pretext bounding boxes with known overlap amounts. Assert collision detection correctly identifies all overlaps and produces nudged positions with 0 overlap.
- **Rough.js SVG Output:** Render 5 rectangles with roughness values [0, 1.0, 2.0, 3.0, 4.0]. Assert SVG path deviation from geometric ideal increases monotonically with roughness.
- **Edge Bleed CIEDE2000:** Provide 5 adjacent slide pairs (3 harmonious, 2 clashing). Assert CIEDE2000 correctly classifies harmonious pairs (≤ 15) and clashing pairs (> 15).

### Integration Tests
- **Full Pipeline (Authority Split):** Submit a VCB with `template_id: "authority_split_v1"`, a coach portrait image, and 7 list items. Assert the full pipeline (SAM 3 → Pretext → Layout Resolver → Skia) produces a rendered WebP where text does not overlap the coach, fonts are within the specified range, and Rough.js decorations are visible.
- **Full Pipeline (In-World Surface):** Submit a VCB with a "person holding blank cardboard" image. Assert SAM 3 detects the surface quadrilateral, Pretext fills the text, Skia warps the text in perspective, and the cardboard texture is visible through the text.
- **Full Pipeline (Whiteboard Notebook):** Submit a VCB with 5 list items. Assert Perlin noise paper texture is generated, Rough.js rectangles are drawn at Pretext coordinates, and the export has no banding in the background.
- **5-Slide Carousel End-to-End:** Submit a Relief Peak VCB with 5 slides. Assert all 5 slides render, edge bleed validates, chromatic bloom arc is enforced, and the selected variant scores ≥ 6.5.

### Safety Tests (ADR-01 Quarantine Security)
- **Malicious Image Input:** Submit a corrupted PNG to SAM 3. Assert the service returns an error without crashing and does not process further pipeline stages.
- **XSS in VCB Text:** Inject `<script>alert('xss')</script>` into VCB `hook_text`. Assert Pretext measures the escaped string correctly and Skia renders it as text content without executing JavaScript.
- **Oversized Template Definition:** Submit a YAML template with 10,000 zones. Assert the template loader rejects it with `TEMPLATE_INVALID` before Layout Resolution begins.
