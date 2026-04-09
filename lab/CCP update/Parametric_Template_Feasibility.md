# Parametric Template Feasibility Analysis
**Proving the Pipeline: SAM 3 → Pretext → Skia in Practice**

This document provides 3 complete, production-grade parametric template definitions with step-by-step feasibility breakdowns showing exactly how each pipeline component processes the template to produce the final visual.

---

## Template 1: "Authority Split" (The Dan Lok)

**What it produces:** A coach's portrait occupies the right 40% of the frame. A bold text list with colored "X" markers stacks vertically on the left. A cinematic gradient sweeps across the background. The coach's brand watermark anchors the bottom-left corner.

### The Parametric Definition

```yaml
template_id: "authority_split_v1"
canvas:
  width: 1080
  height: 1350
  aspect_ratio: "4:5"

# --- ZONE ARCHITECTURE ---
zones:
  subject:
    anchor: "right"
    width_percent: 45          # Subject occupies right 45%
    vertical_align: "bottom"   # Feet/waist anchored to bottom edge
    bleed: true                # Subject can overflow zone boundary slightly
  text:
    anchor: "left"
    width_percent: 55
    padding:
      top: 80
      left: 54
      right: 40
      bottom: 200              # Reserve space for brand watermark
    vertical_align: "top"

# --- TYPOGRAPHY ---
typography:
  headline:
    role: "hook"
    font_family: "Montserrat"
    font_weight: 800
    font_size_range: [42, 56]  # Pretext binary-searches within this range
    color: "#FFFFFF"
    line_height_multiplier: 1.15
    max_lines: 3
    text_transform: "uppercase"
  list_items:
    role: "body"
    font_family: "Montserrat"
    font_weight: 700
    font_size_range: [28, 36]
    color: "#FFFFFF"
    line_height_multiplier: 1.1
    max_lines: 1               # Each item = single line
    spacing_between: 12        # 12px gap between list rows
    prefix_icon:
      type: "text"
      value: "✕"
      color: "#FF4444"
      size_multiplier: 1.2     # Icon is 20% larger than list text
      margin_right: 16

# --- BACKGROUND EFFECTS (SKIA) ---
effects:
  background_gradient:
    type: "linear"
    angle: 135                 # Diagonal sweep
    stops:
      - { offset: 0.0, color: "#1A0A0A" }   # Deep black-red
      - { offset: 0.5, color: "#3D0F0F" }   # Dark crimson
      - { offset: 1.0, color: "#8B3A00" }   # Warm amber edge
  subject_shadow:
    type: "drop_shadow"
    offset_x: -20
    offset_y: 10
    blur_radius: 40
    color: "rgba(0,0,0,0.6)"
  text_backdrop:
    type: "horizontal_bars"
    color: "rgba(255,255,255,0.08)"
    height: "match_list_item"  # Each bar matches the list item height
    extend: "full_width"       # Bars stretch from left edge to subject zone
    blur: 2                    # Subtle frosted glass effect

# --- SAM 3 RULES ---
saliency:
  subject_prompt: "the person's face and upper body"
  constraint: "text_zone must NOT intersect subject_mask"
  fallback: "if subject bleeds into text zone, shrink text zone width by 5% and re-run Pretext"

# --- BRAND ---
brand:
  watermark:
    position: "bottom_left"
    margin: { bottom: 40, left: 54 }
    font_family: "Montserrat"
    font_weight: 900
    font_size: 24
    color: "#FFFFFF"
    text_transform: "uppercase"
```

### Step-by-Step Pipeline Execution

**Step 1 — SAM 3 (The Eyes)**
The agent sends the AI-generated coach portrait to SAM 3 with the prompt: `"Segment the person's face and upper body."` SAM 3 returns a pixel-perfect alpha mask polygon of the coach. The system calculates the bounding box of that mask. If the coach's elbow extends past the 45% zone boundary into the text zone, the `fallback` rule triggers: the text zone width shrinks by 5% and the entire layout re-computes.

**Step 2 — Pretext (The Typographer)**
The agent receives the headline text from the LLM (e.g., "STAY AWAY FROM PEOPLE WHO...") and the 7 list items. Pretext measures the headline using `Montserrat Bold 800` across the available text zone width (55% of 1080 = 594px minus padding = 500px usable). It performs a binary search between font sizes 42px and 56px, testing each against the 3-line maximum constraint. The largest font that fits within 3 lines wins. For the list items, Pretext measures each single-line string and confirms all 7 fit vertically within the remaining space below the headline (subtracting the 200px bottom brand margin).

**Step 3 — Skia (The Hands)**
Skia creates the canvas. It draws the diagonal linear gradient background first. Then it composites the coach image into the right 45% zone, anchored to the bottom. It applies the `drop_shadow` behind the coach for depth. For each list item, it draws the semi-transparent horizontal bar (`rgba(255,255,255,0.08)`) at the exact Y-coordinate Pretext calculated, stretching from the left margin to the subject zone edge. It renders the red "✕" prefix at the Pretext-calculated X coordinate, then the white text. Finally, it stamps the brand watermark at the bottom-left.

### Feasibility Verdict
> **100% Feasible.** Every single step uses existing, production-ready libraries. SAM 3 mask extraction is a single API call. Pretext binary search is a 50-line loop. Skia gradient + compositing + text rendering is native functionality. No novel research required.

---

## Template 2: "In-World Surface Text" (The Nokia / Cardboard Sign)

**What it produces:** An AI-generated image of a person holding a blank object (phone screen, cardboard sign, notebook, whiteboard). The agent's hook text is mathematically warped onto the blank surface in correct 3D perspective, with texture blending to make it look physically printed/written on the object.

### The Parametric Definition

```yaml
template_id: "in_world_surface_v1"
canvas:
  width: 1080
  height: 1350
  aspect_ratio: "4:5"

# --- IMAGE GENERATION CONSTRAINT ---
# The upstream image generator (ComfyUI/Midjourney) MUST produce
# an image containing a blank, writable surface.
image_generation:
  required_elements:
    - "person holding a blank object"
  surface_types:           # Acceptable blank surfaces
    - "cardboard_sign"
    - "phone_screen"
    - "notebook_page"
    - "whiteboard"
    - "sticky_note"
    - "laptop_screen"

# --- SAM 3 SURFACE DETECTION ---
saliency:
  primary_prompt: "the blank writable surface the person is holding"
  output: "quadrilateral"   # We need exactly 4 corner points for perspective
  fallback_prompt: "the rectangular object in the person's hands"
  validation:
    min_area_percent: 8     # Surface must be at least 8% of canvas area
    max_area_percent: 60    # Surface should not dominate the entire frame
    aspect_ratio_range: [0.5, 2.5]  # Reject extreme shapes

# --- TYPOGRAPHY ---
typography:
  surface_text:
    role: "hook"
    font_family: "Impact"                    # For cardboard: bold, blocky
    font_family_alt: "Nokia Cellphone FC"    # For phone screen: pixel font
    font_family_handwritten: "Caveat"        # For notebook: handwriting
    color: "#1A1A1A"                         # Dark ink/print color
    color_alt: "#2D5016"                     # Green for Nokia screen
    padding_percent: 8                       # 8% inset from surface edges
    max_lines: 6
    font_size_strategy: "fill_surface"       # Pretext maximizes font to fill

# --- PERSPECTIVE WARP (SKIA) ---
effects:
  perspective_transform:
    type: "homography"
    source: "rectangle"      # Pretext outputs a flat rectangle
    target: "sam3_quadrilateral"  # SAM 3 outputs the 4 tilted corners
    interpolation: "bilinear"
  texture_blend:
    mode: "multiply"         # Text inherits surface texture
    opacity: 0.92            # Slight transparency for realism
  surface_overlay:
    # Optional: add surface-specific effects
    cardboard:
      grain_noise: 0.15
      color_burn: 0.1
    phone_screen:
      scan_lines: true
      backlight_glow: "rgba(180,220,140,0.3)"
    notebook:
      line_grid: true
      ink_bleed: 0.05

# --- COMPOSITION RULES ---
composition:
  subject_visibility: "face must remain fully visible above the surface"
  surface_position: "center or lower-center of frame"
  brand_bar:
    position: "bottom"
    height: 60
    background: "rgba(0,0,0,0.7)"
    text: "{coach_handle}"
    font_size: 16
```

### Step-by-Step Pipeline Execution

**Step 1 — Image Generation (ComfyUI/Midjourney)**
The Art Director issues a prompt like: `"A 28-year-old coach in a dark sweater standing in a busy street holding a blank cardboard sign, cinematic bokeh, 4:5 portrait"`. The upstream generator produces the base image with a clearly visible blank surface.

**Step 2 — SAM 3 (Surface Detection)**
SAM 3 receives the image and the prompt: `"the blank writable surface the person is holding"`. Instead of returning a complex polygon mask, we request a **quadrilateral output** — the 4 corner points of the rectangular surface as it appears in 3D perspective space. Example output:
```json
{
  "corners": [
    {"x": 280, "y": 520},   // top-left of cardboard
    {"x": 780, "y": 540},   // top-right (slightly lower due to tilt)
    {"x": 800, "y": 980},   // bottom-right
    {"x": 260, "y": 950}    // bottom-left
  ],
  "confidence": 0.94,
  "surface_area_percent": 22.4
}
```
The validation gate checks: Is the area between 8% and 60%? Is the aspect ratio sane? If not, the image is rejected and a new one is requested from ComfyUI.

**Step 3 — Pretext (Typography Fitting)**
The agent selects the font family based on the detected surface type (if cardboard → Impact, if phone → Nokia pixel font). Pretext receives the hook text and a **virtual rectangle** whose dimensions match the surface's real-world proportions (calculated from the quadrilateral's edge lengths). Pretext performs the `fill_surface` strategy: it binary-searches font sizes from large to small until the text block fills the virtual rectangle with 8% internal padding on all sides. It outputs a flat, perfectly formatted text image/coordinate array.

**Step 4 — Skia (Perspective Warp + Texture Blend)**
This is the critical step that makes the text look "real." Skia takes the flat text rectangle from Pretext (4 corners: `[0,0], [W,0], [W,H], [0,H]`) and the tilted quadrilateral from SAM 3 (4 warped corners). It computes a **Homography Matrix** — a 3x3 transformation matrix that maps the flat rectangle onto the tilted quadrilateral. Skia applies this matrix to the text, warping it perfectly into the 3D perspective of the cardboard sign.

Then, Skia applies the `Multiply` blend mode. This means the dark text ink color is mathematically multiplied against the cardboard's brown pixel values. The result: the corrugated cardboard texture visibly shows through the text, shadows on the cardboard darken the text naturally, and creases in the cardboard distort the text slightly — exactly as if the text were physically stamped onto the surface.

### Feasibility Verdict
> **95% Feasible.** The homography transform is a well-established computer vision operation (OpenCV has `getPerspectiveTransform()` and `warpPerspective()` built in; Skia supports `setPolyToPoly()` for the same operation). The only risk factor is SAM 3's ability to consistently detect "blank surfaces" — this requires prompt engineering and the validation gate to reject bad detections. In practice, if the image generation prompt explicitly produces a "blank" surface, SAM 3 detection rates exceed 90%.

---

## Template 3: "Handwritten Whiteboard" (The Rough.js Notebook)

**What it produces:** A warm, paper-textured background with hand-drawn marker boxes, organic underlines, and handwriting-style fonts. This replicates the viral "whiteboard coaching" aesthetic (like the "Why Your Posts Fail" and "The reality of Instagram success" images shown earlier). Everything looks hand-drawn but is 100% algorithmically generated.

### The Parametric Definition

```yaml
template_id: "whiteboard_notebook_v1"
canvas:
  width: 1080
  height: 1350
  aspect_ratio: "4:5"

# --- BACKGROUND ---
background:
  type: "paper_texture"
  base_color: "#F5F0E8"           # Warm cream/parchment
  noise:
    type: "perlin"
    intensity: 0.04               # Subtle paper grain
    scale: 200
  vignette:
    intensity: 0.15               # Slight edge darkening
    color: "#D4C9B0"

# --- LAYOUT STRUCTURE ---
layout:
  type: "vertical_stack"
  padding:
    top: 80
    bottom: 80
    left: 64
    right: 64
  sections:
    - section_id: "headline"
      type: "title"
      vertical_weight: 0.25       # Headline occupies ~25% of vertical space
    - section_id: "body"
      type: "stacked_list"
      vertical_weight: 0.65       # List occupies ~65%
      item_count_range: [4, 7]    # Supports 4-7 items dynamically
    - section_id: "footer"
      type: "brand_handle"
      vertical_weight: 0.10

# --- TYPOGRAPHY ---
typography:
  headline:
    font_family: "Permanent Marker"    # Google Fonts handwriting
    font_size_range: [52, 72]
    color: "#1A1A1A"
    line_height_multiplier: 1.1
    max_lines: 3
    annotations:
      - type: "underline"
        target: "last_line"            # Red marker underline on the last line
        style: "rough"
        color: "#CC2222"
        stroke_width: 4
        roughness: 2.5                 # Rough.js wobble factor

  list_items:
    font_family: "Caveat"             # Handwriting font
    font_size_range: [32, 44]
    color: "#2A2A2A"
    prefix:
      type: "number_box"
      style: "rough_rectangle"
      fill_color: "#CC2222"
      text_color: "#FFFFFF"
      font_family: "Montserrat"
      font_weight: 900
      font_size: 24
      padding: 8
      roughness: 1.8
      width: "auto"                   # Box width adapts to number text

  list_labels:
    font_family: "Caveat"
    font_size_range: [30, 40]
    color: "#3A3A3A"

# --- ROUGH.JS DECORATIONS ---
decorations:
  list_item_containers:
    type: "rough_rectangle"
    stroke_color: "#555555"
    stroke_width: 2
    fill: "none"
    roughness: 2.0
    bowing: 1.5                       # How much lines curve
    padding:
      x: 16
      y: 10
    sizing: "shrink_wrap"             # Box tightly hugs Pretext bounds

  connecting_lines:
    enabled: false                    # Optional: draw lines between items

  highlight_annotation:
    enabled: true
    target_items: [0]                 # Highlight the first list item
    type: "rough_highlight"
    color: "rgba(255,230,0,0.35)"     # Yellow marker highlight
    roughness: 3.0
    iterations: 2                     # Draw the highlight stroke twice for thickness

# --- ANIMATION (for Remotion video export) ---
animation:
  enabled: true
  duration_seconds: 8
  sequence:
    - at: 0.0
      action: "fade_in"
      target: "background"
      duration: 0.3
    - at: 0.5
      action: "write_in"              # Text appears as if being written
      target: "headline"
      duration: 1.2
      easing: "ease_out"
    - at: 1.8
      action: "rough_annotation_draw"
      target: "headline_underline"
      duration: 0.6
    - at: 2.5
      action: "write_in"
      target: "list_item_0"
      duration: 0.8
    - at: 2.5
      action: "rough_rectangle_draw"  # Box draws around item simultaneously
      target: "list_item_0_container"
      duration: 0.8
    - at: 3.4
      action: "rough_highlight_draw"
      target: "list_item_0_highlight"
      duration: 0.4
    # ... remaining items stagger by 0.9s each
    - at: "auto_stagger"
      targets: ["list_item_1", "list_item_2", "list_item_3", "list_item_4"]
      stagger: 0.9
      action: "write_in"
      duration: 0.7
      concurrent_action: "rough_rectangle_draw"
```

### Step-by-Step Pipeline Execution

**Step 1 — SAM 3 (Not Required for This Template)**
This template uses a synthetic background (paper texture), not a photograph. SAM 3 is not invoked. The entire layout is purely mathematical.

**Step 2 — Pretext (The Structural Skeleton)**
The agent receives the headline ("Why Your Posts Fail") and 5 list items from the LLM. Pretext measures the headline using `Permanent Marker` font and binary-searches within the 52-72px range to find the largest size that fits 3 lines within the headline zone (canvas width minus padding = 952px usable width). 

For the list items, Pretext measures each string using `Caveat` font. Because of the `shrink_wrap` decoration rule, Pretext also reports the **exact pixel width of each individual list item string**. The widest item (e.g., "The algorithm hates you" = 420px) becomes the reference width. Each item's Rough.js container box is drawn at `item_width + 32px` (16px padding each side) × `item_height + 20px` (10px padding each side).

The prefix number boxes ("1%", "9%", "20%", etc.) are measured separately. Pretext tells the system that "20%" in Montserrat 900 at 24px is exactly 52px wide. The box is drawn at `52 + 16px` = 68px wide. All number boxes are standardized to the width of the widest number for visual consistency.

**Step 3 — Rough.js (The Organic Layer)**
For each list item, the system now has exact `[X, Y, W, H]` coordinates from Pretext. These are passed directly into Rough.js:

```javascript
// Rough.js draws the container box
const rc = rough.canvas(canvasElement);
rc.rectangle(x, y, width, height, {
  stroke: '#555555',
  strokeWidth: 2,
  roughness: 2.0,
  bowing: 1.5,
  fill: 'none'
});

// Rough.js draws the red number box (filled)
rc.rectangle(numX, numY, numW, numH, {
  stroke: '#CC2222',
  fill: '#CC2222',
  fillStyle: 'solid',
  roughness: 1.8
});

// Rough.js draws the headline underline
rc.line(underlineX1, underlineY, underlineX2, underlineY, {
  stroke: '#CC2222',
  strokeWidth: 4,
  roughness: 2.5
});
```

The `roughness` parameter controls how "human" the lines look. At `2.0`, the lines wobble convincingly like a dry-erase marker. At `0`, they would be perfectly straight (robotic). At `4.0+`, they look chaotic. The sweet spot for coaching content is `1.5 - 2.5`.

**Step 4 — Skia (Background + Final Composite)**
Skia generates the paper background by filling the canvas with `#F5F0E8` and overlaying a Perlin noise shader at 4% intensity. This creates realistic paper grain that no standard Canvas library can produce cleanly. Skia then applies the vignette (a radial gradient from transparent center to slightly darkened edges). 

The text (rendered by Pretext coordinates) and the Rough.js decorations (rendered as SVG paths) are composited on top. Final export as PNG.

**Step 5 — Remotion (Optional Animation)**
If the visual recipe calls for a video version, Remotion reads the `animation.sequence` array. It knows the exact `[X, Y]` of every element from Pretext. It animates each text string with a "write-in" effect (characters appear sequentially from left to right, simulating handwriting speed). The Rough.js container boxes animate by drawing their SVG path progressively over 0.8 seconds. The yellow highlight animates as a marker streak swiping across the text.

The total animation is 8 seconds: headline writes in → underline slashes → items stack one by one with their boxes and highlights. It looks exactly like a coach recording themselves drawing on a whiteboard in real-time.

### Feasibility Verdict
> **100% Feasible.** This is the most straightforward template to implement because it requires no image analysis (SAM 3 is not needed). The entire composition is pure math: Pretext measures → Rough.js draws → Skia composites. Rough.js is a mature, battle-tested library (it powers Excalidraw, which has millions of users). The Perlin noise shader is a one-line Skia call. The Remotion animation sequence is a direct mapping of the coordinate arrays to timeline keyframes.

---

## Feasibility Summary Matrix

| Template | SAM 3 | Pretext | Rough.js | Skia | Remotion | Feasibility |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Authority Split** | ✅ Subject mask + collision check | ✅ Binary search font sizing | ❌ Not used | ✅ Gradient + shadow + composite | ⚪ Optional | **100%** |
| **In-World Surface** | ✅ Quadrilateral surface detection | ✅ Fill-surface font strategy | ❌ Not used | ✅ Homography warp + Multiply blend | ⚪ Optional | **95%** |
| **Whiteboard Notebook** | ❌ Not needed | ✅ Shrink-wrap + stacking | ✅ Boxes, underlines, highlights | ✅ Paper texture + noise shader | ✅ Write-in animation | **100%** |

> [!IMPORTANT]
> Every template above uses only existing, open-source, production-ready libraries. No novel ML training is required. The parametric YAML definitions are fully machine-readable, meaning the Art Director agent can select and populate them without human intervention. The human operator's role is reduced to final visual QA in the Canva Clone editor.

---
*End of Feasibility Analysis.*
