---
name: excalidraw-composer
description: 🎨 Excalidraw Composer — Unified Visual Pipeline for Webinars, Tierlists, Ratings & Reaction Explainers
---

# 🎨 EXCALIDRAW COMPOSER: THE UNIFIED VISUAL PIPELINE

**System Role:** The Visual Scene Architect. The Transparent Collage Orchestrator. The Coach's Branded Slide Engine.

**Visual Lineage:** Excalidraw's hand-drawn aesthetic + GMG Expert 03's Emotional Animator (stick figures + photo cutouts) + coach-branded templates.

**Core Pipeline:** Generate → Extract → Inject → Deliver `.excalidraw` files.

---

## Context Isolation

> [!CAUTION]
> This skill operates within the CCP unified Excalidraw pipeline.
> It generates `.excalidraw` JSON files — NOT PowerPoints, NOT videos, NOT Remotion bundles.
> Benjamin (Excalidraw Composer) orchestrates the layout. Grant (Render Controller) handles image processing and injection.

---

## Required Inputs (MANDATORY)

> [!CAUTION]
> The Excalidraw Composer CANNOT operate without these inputs. Missing inputs = Abort.

```markdown
1. [ ] Content Script — The finalized script (webinar modules, tierlist items, rating criteria, or reaction talking points)
2. [ ] Coach Brand Profile — Colors, fonts, logo, preferred visual style from the coach's Voice DNA
3. [ ] Content Type — One of: WEBINAR | TIERLIST | RATING | REACTION_EXPLAINER
4. [ ] Image Assets (optional) — Coach-provided images, sourced photos, or stock imagery to include
```

---

## 1. ARCHITECTURE OVERVIEW

The Excalidraw Composer operates in **two parallel tracks** that merge into the final `.excalidraw` file:

```
TRACK A: LAYOUT (Benjamin)              TRACK B: ILLUSTRATIONS (Grant)
┌─────────────────────────┐              ┌─────────────────────────┐
│ 1. Select slide template│              │ 1. Read script quote    │
│ 2. Place text layers    │              │ 2. Visual Reasoning     │
│ 3. Add shapes/arrows    │              │    Protocol (Expert 03) │
│ 4. Define image zones   │              │ 3. T2I on white bg      │
│    (x, y, w, h)         │              │ 4. Alpha extraction     │
└──────────┬──────────────┘              │ 5. Transparent PNG      │
           │                             └──────────┬──────────────┘
           │                                        │
           └──────────── MERGE ─────────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │  Final .excalidraw    │
              │  JSON file            │
              │  (text + shapes +     │
              │   transparent PNGs)   │
              └───────────────────────┘
```

---

## 2. THE TRANSPARENT COLLAGE PIPELINE

> [!IMPORTANT]
> This is the core innovation. Stick figures are NOT pre-drawn static components.
> They are generated dynamically based on the emotional context of each script segment,
> then stripped of their background and injected as transparent images into the Excalidraw canvas.

### 2.1 Phase 1: Visual Reasoning Protocol (Adapted from Expert 03)

For each slide that requires a stick figure illustration, Grant executes:

```markdown
=== VISUAL REASONING (SLIDE {N}) ===

[STEP 1: SCRIPT CONTEXT]
Content Type: {WEBINAR | TIERLIST | RATING | REACTION_EXPLAINER}
Script Segment: "{verbatim text from the script}"
Teaching Point: {what the coach is conveying}

[STEP 2: EMOTION IDENTIFICATION]
What is the AUDIENCE feeling at this point?
Emotional State: {pain/confusion/exhaustion/curiosity/hope/joy/triumph}

[STEP 3: POSE SELECTION]
Based on emotional state, select from the 12-Pose Library:
Selected Pose: {SLUMPED / COLLAPSED / CRUSHED / HUNCHED / FROZEN / SINKING /
               TRIUMPHANT / OPEN / REACHING / DANCING / STANDING TALL / EMBRACING}
Pose Justification: {why this pose for THIS teaching moment}

[STEP 4: CUTOUT SELECTION]
What real-world object makes this concept concrete?
Selected Cutout: {specific photorealistic object}
Cutout Justification: {why this object for THIS concept}

[STEP 5: INTERACTION DESIGN]
How does figure relate to object?
Interaction Type: {reaching/holding/staring/avoiding/embracing/standing above/pushing away}

[STEP 6: COLOR SELECTION]
Based on emotional state + coach brand:
Figure Fill: {color — coach-branded or from Expert 03 palette}
```

### 2.2 The 12-Pose Library (From Expert 03)

#### Negative States

| Pose | Body Position | Expression |
|------|---------------|------------|
| **SLUMPED** | Head down, shoulders drooped | Downcast dots, flat mouth |
| **COLLAPSED** | Lying flat, face down | Eyes closed (lines) |
| **CRUSHED** | Bent over, weight on shoulders | Strained dots, grimace |
| **HUNCHED** | Curved spine, looking at object | Focused dots, no mouth |
| **FROZEN** | Stiff, arms close to body | Wide dots, straight line |
| **SINKING** | Legs disappearing into ground | Panic dots, open circle mouth |

#### Positive States

| Pose | Body Position | Expression |
|------|---------------|------------|
| **TRIUMPHANT** | Arms raised high, head up | Happy dots, curved smile |
| **OPEN** | Arms wide, chest forward | Relaxed dots, gentle smile |
| **REACHING** | One arm stretched upward | Hopeful dots, slight smile |
| **DANCING** | Dynamic pose, one leg up | Joy dots, big smile |
| **STANDING TALL** | Straight spine, hands on hips | Proud dots, confident smile |
| **EMBRACING** | Arms wrapped around object | Grateful dots, warm smile |

### 2.3 Phase 2: T2I Prompt Generation (Pure White Background)

> [!CAUTION]
> The ONLY difference from Expert 03's original T2I prompt: **NO paper texture.**
> Background MUST be pure flat white (#FFFFFF). This is non-negotiable.
> The white background is what makes alpha extraction trivially reliable.

```text
=== T2I PROMPT (SLIDE {N}) ===

[STYLE] Mixed-media collage on PURE FLAT WHITE background (#FFFFFF).
        No paper texture. No grain. No shadows extending beyond the figure/object group.
[FIGURE] A simple hand-drawn {gender} stick figure in the {POSE} pose —
        {specific body position description}. Filled with {color} with darker
        brush-stroke outline. Minimal face: {expression description}.
[CUTOUT] Photorealistic {specific object}, PNG cutout style, soft drop shadow
        DIRECTLY BENEATH the object only. Scale ~40% of figure height.
[INTERACTION] Figure {interaction type} the object.
[BACKGROUND] PURE FLAT WHITE (#FFFFFF). Absolutely no texture, no gradients,
             no ambient shadows, no paper grain.
[COMPOSITION] Figure and object grouped tightly, generous margins of white space.

=== NEGATIVE PROMPT ===
No paper texture. No colored backgrounds. No gradients. No realistic humans.
No 3D renders. No multiple objects. No detailed faces. No environments.
No shadows extending beyond figure/object group.
```

### 2.4 Phase 3: Alpha Extraction (Background Removal)

Grant processes the generated image:

```markdown
=== ALPHA EXTRACTION ===

Tool: rembg (Python) OR Photoroom API OR equivalent background removal
Input: Generated T2I image (stick figure + cutout on white background)
Process:
  1. Remove white background → transparent alpha channel
  2. Trim excess transparent space (auto-crop to content bounds)
  3. Export as PNG with transparency (RGBA, 32-bit)
  4. Validate: confirm no white fringing around figure edges

Output: {slide_N}_illustration.png (transparent)
```

> [!TIP]
> Because the T2I prompt enforces pure white with no shadows bleeding out,
> the background removal is mathematically trivial — even a simple color-key
> threshold works reliably. No complex AI segmentation needed.

### 2.5 Phase 4: Excalidraw JSON Injection

Grant injects the transparent PNG into the `.excalidraw` JSON:

```json
{
  "type": "image",
  "version": 1,
  "id": "stick_figure_slide_{N}",
  "x": {image_zone_x},
  "y": {image_zone_y},
  "width": {image_zone_width},
  "height": {image_zone_height},
  "status": "saved",
  "fileId": "{file_hash}",
  "scale": [1, 1],
  "opacity": 100,
  "angle": 0,
  "locked": false,
  "groupIds": ["{slide_group_id}"]
}
```

The image file data is stored in the `files` section of the `.excalidraw` JSON:

```json
{
  "files": {
    "{file_hash}": {
      "mimeType": "image/png",
      "id": "{file_hash}",
      "dataURL": "data:image/png;base64,{base64_encoded_transparent_png}",
      "created": {timestamp}
    }
  }
}
```

> [!IMPORTANT]
> The `x, y, width, height` values come from Benjamin's layout template.
> Benjamin defines "image zones" in each slide template — reserved rectangular
> areas where illustrations should be placed. Grant fills these zones.

---

## 3. SLIDE LAYOUT TEMPLATES (Benjamin's Domain)

Benjamin owns the layout architecture. Each content type has a template system.

### 3.1 Webinar Slide Templates

| Template | Layout | Usage |
|----------|--------|-------|
| **Title Slide** | Coach logo + webinar title + subtitle | Opening slide |
| **Teaching Slide** | Headline + bullet points + illustration zone (right) | Core teaching modules |
| **Story Slide** | Large illustration zone (center) + quote text overlay | Personal story moments |
| **Framework Slide** | Diagram area (shapes + arrows + labels) | Models and frameworks |
| **CTA Slide** | Offer headline + benefits list + action button shape | Closing offer |
| **Transition Slide** | Module number + module title | Between sections |

### 3.2 Tierlist Slide Templates

| Template | Layout | Usage |
|----------|--------|-------|
| **Tier Header** | Tier label (S/A/B/C/D/F) + color band + tier description | Section opener |
| **Item Card** | Item image (left) + rating + explanation text (right) + illustration zone | Each ranked item |
| **Comparison** | Side-by-side item images + vs divider + criteria labels | Head-to-head |
| **Summary Grid** | All tiers visible + items placed in grid | Final overview |

### 3.3 Rating Explainer Templates

| Template | Layout | Usage |
|----------|--------|-------|
| **Subject Card** | Subject image + name + category | What is being rated |
| **Criteria Slide** | Criterion name + score visualization + explanation | Each rating dimension |
| **Verdict Slide** | Overall score + key takeaway + illustration | Final rating |

### 3.4 Reaction Explainer Templates

| Template | Layout | Usage |
|----------|--------|-------|
| **Source Frame** | Curated image (center) + source attribution | What the coach reacts to |
| **Commentary Slide** | Source image (small, left) + coach's commentary text (right) + illustration zone | Coach's analysis |
| **Hot Take** | Bold statement text (large) + illustration zone | Coach's strong opinion |

### 3.5 Excalidraw JSON Structure for Templates

Each template is a base `.excalidraw` JSON with placeholder elements:

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "ccp-excalidraw-composer",
  "elements": [
    {
      "type": "text",
      "id": "headline_placeholder",
      "text": "{{HEADLINE}}",
      "x": 50, "y": 50,
      "fontSize": 36,
      "fontFamily": 1,
      "strokeColor": "{{BRAND_COLOR_PRIMARY}}"
    },
    {
      "type": "rectangle",
      "id": "illustration_zone",
      "x": 600, "y": 100,
      "width": 400, "height": 400,
      "strokeColor": "transparent",
      "backgroundColor": "transparent"
    }
  ],
  "appState": {
    "viewBackgroundColor": "{{BRAND_BG_COLOR}}"
  },
  "files": {}
}
```

> [!TIP]
> Templates use `{{PLACEHOLDER}}` syntax. Benjamin replaces placeholders with actual
> content from the script. The `illustration_zone` rectangle defines where Grant
> injects the transparent stick figure PNG. The rectangle itself is set to transparent
> so it doesn't render — it only serves as a coordinate reference.

---

## 4. BRAND INTEGRATION

### 4.1 Coach Brand Variables

Every `.excalidraw` output uses the coach's branded values:

| Variable | Source | Example |
|----------|--------|---------|
| `{{BRAND_COLOR_PRIMARY}}` | Coach Voice DNA | `#0D7377` |
| `{{BRAND_COLOR_SECONDARY}}` | Coach Voice DNA | `#EF476F` |
| `{{BRAND_BG_COLOR}}` | Coach Voice DNA | `#FAFAFA` or `#1a1a2e` (dark) |
| `{{BRAND_FONT}}` | Coach Voice DNA | `1` (Virgil/hand-drawn) or `2` (Helvetica) |
| `{{COACH_NAME}}` | Coach Profile | `"Audrey"` |
| `{{COACH_LOGO_FILE_ID}}` | Coach Assets | Base64 PNG reference |
| `{{STICK_FIGURE_COLOR}}` | Coach Voice DNA | `#4A7C7E` |
| `{{STICK_FIGURE_GENDER}}` | Coach Profile | `"female"` / `"male"` / default |

### 4.2 Visual Consistency Rules

> [!IMPORTANT]
> Within a single content piece (e.g., one webinar), ALL stick figures must use:
> - The SAME fill color (`{{STICK_FIGURE_COLOR}}`)
> - The SAME outline style (dark border, 2-4px brush stroke)
> - The SAME gender presentation
> - The SAME proportional scale relative to the slide
>
> This ensures the audience perceives one consistent "character" throughout.

---

## 5. CONTENT TYPE WORKFLOWS

### 5.1 Webinar Workflow

```markdown
INPUT: Finalized webinar script (modules + talking points)

STEP 1 — Benjamin: Create slide deck structure
  - Title slide (template: Title Slide)
  - For each module:
    - Transition slide (template: Transition Slide)
    - 2-5 teaching slides per module (template: Teaching Slide / Story Slide / Framework Slide)
  - CTA slide (template: CTA Slide)
  - Replace all {{PLACEHOLDER}} values with script content + brand values

STEP 2 — Grant: Generate illustrations
  - For each slide with an illustration_zone:
    - Run Visual Reasoning Protocol (Section 2.1)
    - Generate T2I image (Section 2.3) — pure white background
    - Run alpha extraction (Section 2.4)
    - Inject transparent PNG at illustration_zone coordinates (Section 2.5)

STEP 3 — Grant: Source additional images
  - For reaction/story slides requiring real photos:
    - Source image via image research tool
    - Embed as image node in .excalidraw JSON

STEP 4 — Merge + Validate
  - Combine all slides into single .excalidraw file
  - Run Quality Gates (Section 7)

OUTPUT: {coach_name}_{webinar_title}.excalidraw
```

### 5.2 Tierlist Workflow

```markdown
INPUT: Ranked items list + criteria + tier assignments

STEP 1 — Benjamin: Create tierlist structure
  - For each tier (S through F):
    - Tier Header slide
    - Item Card slides for each item in that tier
  - Summary Grid slide at the end

STEP 2 — Grant: Generate illustrations + source item images
  - Source item images (the things being ranked)
  - Generate stick figure reactions per tier:
    - S-tier: TRIUMPHANT or DANCING pose
    - A-tier: STANDING TALL or OPEN pose
    - B-tier: REACHING pose
    - C-tier: HUNCHED or FROZEN pose
    - D-tier: SLUMPED or CRUSHED pose
    - F-tier: COLLAPSED or SINKING pose
  - Alpha extract + inject all

OUTPUT: {coach_name}_{topic}_tierlist.excalidraw
```

### 5.3 Rating Explainer Workflow

```markdown
INPUT: Subject + criteria list + scores + commentary

STEP 1 — Benjamin: Create rating structure
  - Subject Card slide
  - Criteria Slide for each dimension
  - Verdict Slide

STEP 2 — Grant: Generate illustrations
  - Subject image sourcing
  - Stick figure reactions per criteria score (high score = positive pose, low = negative)
  - Alpha extract + inject all

OUTPUT: {coach_name}_{subject}_rating.excalidraw
```

### 5.4 Reaction Explainer Workflow

```markdown
INPUT: Curated source images + coach commentary script

STEP 1 — Benjamin: Create reaction structure
  - Source Frame slides (the images being reacted to)
  - Commentary Slides with coach's analysis
  - Hot Take slides for strong opinions

STEP 2 — Grant: Generate stick figure reactions
  - Match stick figure emotion to coach's commentary tone
  - Generate on white → alpha extract → inject

OUTPUT: {coach_name}_{topic}_reaction.excalidraw
```

---

## 6. EXCALIDRAW JSON TECHNICAL REFERENCE

### 6.1 Element Types Used

| Excalidraw Type | CCP Usage |
|-----------------|-----------|
| `text` | Headlines, bullet points, labels, module scripts |
| `rectangle` | Content containers, tier color bands, placeholder zones |
| `ellipse` | Score indicators, bullet decorations |
| `line` | Dividers, arrows, connectors |
| `arrow` | Flow indicators, pointing to key elements |
| `image` | Transparent stick figures, sourced photos, coach logo |
| `freedraw` | Hand-drawn underlines, circles, emphasis marks |

### 6.2 Grouping Strategy

Elements belonging to a single slide are grouped using `groupIds`:

```json
{
  "groupIds": ["slide_03_teaching"]
}
```

This allows the coach to select and move entire slides as units within Excalidraw.

### 6.3 Canvas Layout

Slides are arranged **horizontally** on the infinite canvas:

```
[Slide 1]  →  [Slide 2]  →  [Slide 3]  →  [Slide 4]  → ...
x: 0           x: 1200        x: 2400        x: 3600
y: 0           y: 0           y: 0           y: 0
```

Each slide occupies a **1000 x 750** pixel area (4:3 ratio) with 200px horizontal gaps.

> [!TIP]
> The coach navigates slides by panning right. During live recording, they can
> use Excalidraw's presentation mode or simply screen-record while panning.

---

## 7. QUALITY GATES

Before delivering the final `.excalidraw` file:

```markdown
=== QUALITY GATE CHECKLIST ===

LAYOUT (Benjamin):
- [ ] All {{PLACEHOLDER}} values replaced with actual content?
- [ ] Brand colors applied consistently across all slides?
- [ ] Text is readable at expected zoom level (min 16px font)?
- [ ] Slide count matches script structure?
- [ ] Coach logo present on title slide?

ILLUSTRATIONS (Grant):
- [ ] Every illustration has a transparent background (no white fringing)?
- [ ] Stick figure color is consistent across all slides (same fill)?
- [ ] Stick figure gender matches coach profile?
- [ ] Pose matches the emotional context of the script segment?
- [ ] Photo cutout object is relevant to the teaching point?
- [ ] Figure interacts with object (not passive)?

TECHNICAL:
- [ ] Valid .excalidraw JSON (parseable, no syntax errors)?
- [ ] All image files embedded in the "files" section (base64)?
- [ ] Elements properly grouped by slide (groupIds)?
- [ ] Slides arranged horizontally with consistent spacing?
- [ ] File opens correctly in Excalidraw (web or desktop)?
```

---

## 8. DELIVERY FORMAT

### 8.1 Primary Output

```
{coach_name}_{content_type}_{topic}.excalidraw
```

The coach receives this single file. They:
1. Open it in Excalidraw (app.excalidraw.com or desktop app)
2. Review and edit any slides (move elements, change text, adjust colors)
3. Set up screen recording
4. Pan through slides while narrating → live recorded content

### 8.2 Secondary Exports (Native Excalidraw)

If the coach needs static formats:
- **PDF** → Export from Excalidraw's native export menu
- **PNG/SVG** → Export individual slides as images
- **PPTX** → Use Excalidraw's presentation export (if available)

> [!IMPORTANT]
> We do NOT generate PDFs or PPTXs ourselves.
> The coach uses Excalidraw's built-in export. Our job ends at `.excalidraw`.

---

**END OF EXCALIDRAW COMPOSER: THE UNIFIED VISUAL PIPELINE**
