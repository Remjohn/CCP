# First Frame Composer — The Missing Visual Agent

> **Status:** Proposed Architecture · **Replaces:** `✨ ADVANCED CONTENT HOOK GENERATION PROMPT.md` (100% obsolete)

---

## 1. THE STRATEGIC QUESTION: RECIPES vs LIBRARY

### Answer: Recipes Die. The Library + A Composer Agent Lives.

Static recipes (the old 65-hook file) are **training wheels**. They exist because when you have no library, you need pre-composed combinations to even get started. Now that we have:

- **298 composable pose atoms** across 7 catalogs
- **28 expression channels** with parametric control
- **Mood State routing** (4 states × 8 variables)
- **Memetic Engine** (14 humor architectures)
- **CVE pillars** (gaze vectors, compression, color temperature)

...static recipes are a **ceiling, not a floor**. They limit the composer to 38 pre-approved combinations when the library supports **millions** of valid compositions.

### What Replaces Recipes

A **Composer Agent** that queries the library at runtime based on the Psychological Routing Brief. It doesn't need recipes because it has:

1. **Constraints** (from Mood State + Archetype + CBCS tier + CVE pillars)
2. **Atoms** (from ConsciousPose + ConsciousSmile libraries)
3. **Composition rules** (from the schema's layer compatibility matrix)

The agent COMPOSES, it doesn't SELECT from a pre-made list.

---

## 2. THE OLD HOOK PROMPT: AUTOPSY

The `✨ ADVANCED CONTENT HOOK GENERATION PROMPT.md` fails on every criterion:

| Criterion | Old Prompt | CCP Standard |
|:----------|:-----------|:-------------|
| Architecture integration | None — standalone generic prompt | Must consume DEP-ENG-016 Psychological Routing Brief |
| Mood State awareness | Zero | 4 states × 8 variables × audience maturity clamping |
| Visual specification | Zero | ConsciousPose CP-IDs + ConsciousSmile 28-ch recipes |
| Anti-draft protection | None | 3-level contrastive architecture (Ling et al., 2023) |
| Gaze architecture | None | CVE gaze vectors (Frischen et al., 2007) |
| Expression control | "Trigger mirror neuron response" (no mechanism) | FACS AU-mapped 28 channels with parametric values |
| Research grounding | "Vulnerability is the new credibility" (pop wisdom) | 14 peer-reviewed sources in the Mood State Architecture alone |
| Repeatability | Zero — every run is different | Deterministic via ControlNet + LoRA + FACS |

**Verdict:** This file should be archived as historical. It cannot be upgraded — the gap is architectural.

---

## 3. THE GAP: NO FIRST FRAME AGENT EXISTS

Every content format needs a **First Frame** — the visual composition that determines whether a human stops scrolling. Zero agents in the current pipeline own this:

| Format | First Frame = | Who Owns It Now | Problem |
|:-------|:-------------|:----------------|:--------|
| **Short-form video** (Reel/TikTok) | Frame 1 of video + text overlay | Nobody — CAC/GMG compose ALL frames equally | No frame is optimized for the scroll-stop trigger |
| **Carousel** | Slide 1 cover image + headline | Nobody | No agent produces carousel covers at all |
| **Thumbnail** (YouTube/webinar) | Static image with face + text | Nobody | Thumbnails are improvised |
| **Flyer/poster** | Full composition | Nobody | No agent handles static promotional visuals |
| **Story** (IG/FB) | Opening frame | Nobody | Same gap as video |
| **Poll/quiz visual** | The preview image | Nobody | Crowdpurr visuals are default templates |
| **Email header** | Hero image | Nobody | Generic stock or none |
| **Webinar cover** | Registration page hero | Nobody | Generic event template |

**The First Frame is the most ROI-critical visual in the entire pipeline** — and it has zero dedicated engineering.

---

## 4. FIRST FRAME COMPOSER — AGENT SPECIFICATION

### Agent Identity

| Property | Value |
|:---------|:------|
| **Name** | First Frame Composer (FFC) |
| **Type** | Visual Composition Agent |
| **Role** | Compose the scroll-stop First Frame for ANY content format |
| **Consumes** | DEP-ENG-016 (Psych Brief) + ConsciousPose library + ConsciousSmile channels + Beat Cluster |
| **Produces** | `first_frame_spec.json` — deterministic ControlNet composition |
| **Works Before** | CAC Composer, GMG Composer, Carousel Builder, Thumbnail Renderer |
| **Works After** | Beat Cluster generation, Visual Researcher |

### Why It's a Separate Agent (Not Part of CAC/GMG)

1. **CAC** composes editorial photography scenes — ALL frames are equal, no frame is "the hook"
2. **GMG** composes abstract animations — the First Frame is just the Last Frame reversed
3. **Carousels** have no visual agent at all
4. **Thumbnails** have no visual agent at all

The First Frame is a **cross-format concern** that sits ABOVE format-specific composers.

### Input Requirements

```
REQUIRED:
  1. beat_cluster.json — Concept + VCP + Core Emotion
  2. compressed_anchor.txt — Coach identity (50-60 words)
  3. psych_routing_brief.json (DEP-ENG-016) — Mood State + 8 variables
  4. output_format — video | carousel | thumbnail | flyer | story | poll | webinar
  5. cbcs_tier — cold | warm | hot

OPTIONAL:
  6. visual_schema.json — If available (grounded environments)
  7. memetic_intent — If humor beat (BVT architecture ID)
```

### Output: `first_frame_spec.json`

```json
{
  "format": "carousel_cover",
  "dimensions": "1080x1350",
  "composition": {
    "body": "CP-B-003",
    "hands": "CP-H-006",
    "gaze": "CP-G-026",
    "expression": {
      "lip_bite": 0.3,
      "eye_squint": 0.5,
      "smirk": 0.4,
      "nostril_flare": 0.15
    },
    "scene": "CP-S-001",
    "mood_visual": "CP-MV-025",
    "props": null,
    "multi_character": null
  },
  "text_overlay": {
    "headline": "She didn't leave because she stopped loving him.",
    "position": "bottom_third",
    "font_treatment": "bold_serif_white_shadow",
    "text_size_ratio": 0.12
  },
  "controlnet_assets": [
    "CP-B-003_CP-H-006_CP-G-026_CP-S-001_v01_depth.png",
    "CP-B-003_CP-H-006_CP-G-026_CP-S-001_v01_openpose.png"
  ],
  "identity_lora": "{coach_id}_identity_v1.safetensors",
  "expression_adapter": "conscious_smile_v1.safetensors",
  "expression_weights": {
    "lip_bite": 0.3,
    "eye_squint": 0.5,
    "smirk": 0.4,
    "nostril_flare": 0.15
  },
  "negative_prompt": "No studio lighting. No white background. No generic smile. No stock photo.",
  "reasoning": {
    "mood_state": "Escape",
    "cbcs_tier": "cold",
    "gaze_rationale": "Cold CBCS → direct under-brow (CP-G-026) to create immediate parasocial intimacy without earned trust. Smolder bypasses cognitive evaluation.",
    "expression_rationale": "Lip bite + smirk = desire + knowing. Scroll-stop through biological attention anchor (ASFW).",
    "text_rationale": "Curiosity gap via relationship hook. 'She' = universal third-person entry. 'Didn't leave because stopped loving' = violation of expected frame (BVT)."
  }
}
```

### Composition Decision Engine

The FFC doesn't use recipes. It runs this decision tree against the Psychological Routing Brief:

```
STEP 1: FORMAT CONSTRAINTS
  video → 9:16, face must be in top 40% (text overlay below)
  carousel → 4:5 or 1:1, face can be centered
  thumbnail → 16:9, face LEFT or RIGHT third, text opposite
  flyer → variable, full-body permitted
  webinar → 16:9, professional framing, Status mood bias

STEP 2: MOOD STATE → VISUAL ENERGY
  Processing → CP-MV-001..006, warm tones, gaze: direct contemplative
  Escape → CP-MV-007..012, light/bright OR neon, gaze: playful/provocative
  Discovery → CP-MV-013..018, cool-to-warm transition, gaze: wide eyes
  Status → CP-MV-019..024, premium/editorial, gaze: chin-up confident

STEP 3: CBCS TIER → GAZE VECTOR
  Cold (0-3) → Averted 20-30° OR provocative direct (smolder/wink)
  Warm (4-7) → Near-direct 5-10° off-axis
  Hot (8-10) → Direct with downward chin, confident invitation

STEP 4: TEXT HOOK → PSYCHOLOGICAL MECHANISM
  Pull from beat_cluster VCP + concept.core_emotion
  Apply regulatory_frame:
    Promotion → "What becomes possible"
    Prevention → "What's at risk"
  Apply BVT if memetic_intent present:
    Violation text + Benignness visual (or inverse)

STEP 5: EXPRESSION → EMOTIONAL PAYLOAD
  Query ConsciousSmile 28-ch presets matching:
    mood_state + core_emotion + memetic_intent
  If intimate content → enable lip_bite, nostril_flare, neck_tension
  If humor → enable wink, smirk, eye_roll, tongue_peek
  If authority → enable chin_raise, brow_furrow, lip_press

STEP 6: COMPOSE & OUTPUT
  Assemble first_frame_spec.json
  Resolve ControlNet asset IDs
  Validate all CP-IDs exist in production library
  Output to format-specific pipeline
```

### Format-Specific Output Routing

| Format | FFC Output Goes To | What Happens Next |
|:-------|:-------------------|:-----------------|
| Video | CAC/GMG Composer receives first_frame_spec as Frame 1 constraint | Remaining frames composed around the established visual anchor |
| Carousel | Carousel Builder receives cover spec | Interior slides follow consistent visual language |
| Thumbnail | Thumbnail Renderer (ComfyUI workflow) | Direct ControlNet generation |
| Flyer | Static composition pipeline | Direct generation |
| Webinar | Event page builder | Hero image generation |
| Poll/Quiz | Crowdpurr visual template | Overlay composition |

### Anti-Draft for First Frames

The FFC has its own 2-level anti-draft (no Level 3 coach-specific since this is visual, not text):

**Level 1 — Stock Thumbnail Anti-Draft:**
> Generic coaching thumbnail: Woman smiling at camera in studio lighting, arms crossed confidently, clean white background, bold red text saying "5 SECRETS TO SUCCESS." WHY THIS FAILS: Studio lighting = no CVE compliance. Generic smile = no emotional contagion specificity. Arms crossed = defensive, not inviting. White background = default, not mood-routed. Text is clickbait structure without psychological mechanism.

**Level 2 — Format-Specific Anti-Draft:**
> Carousel cover that looks like every other coaching carousel: Solid color background with text only, no human face, generic Canva template feeling. WHY THIS FAILS: No face = no emotional contagion trigger. No gaze vector = no attention anchoring. Template aesthetic = platform blindness (users have learned to scroll past this pattern).

---

## 5. WHAT THIS MEANS FOR THE PIPELINE

### Before FFC (Current State)

```
Beat Cluster → VCP → CAC/GMG Composers → ALL frames equal → Post-production picks thumbnail
```

**Problem:** The scroll-stop frame is an afterthought picked in post.

### After FFC (Proposed)

```
Beat Cluster → VCP → FIRST FRAME COMPOSER → first_frame_spec.json
                                                    ↓
                                     ┌──────────────┼──────────────┐
                                     ↓              ↓              ↓
                              CAC/GMG Composers  Carousel Builder  Thumbnail Renderer
                              (Frame 1 locked)   (Cover locked)    (Direct output)
```

**Result:** The most important visual in the pipeline is engineered FIRST, not discovered last.

### Old Files Disposition

| File | Action |
|:-----|:-------|
| `✨ ADVANCED CONTENT HOOK GENERATION PROMPT.md` | **ARCHIVE** — 100% obsolete, zero architectural integration |
| `🟨 VISUAL HOOKS RECIPES 🟨.md` | **ARCHIVE** — replaced by ConsciousPose library + FFC composition engine |
| `visual_hooks_mcda_audit.md` (artifact) | **KEEP** — the 38 upgraded hooks serve as FFC composition presets (not recipes, but validated starting points the agent can reference) |
