# Tech-Spec: FR-CA11-15 — Contextual Branding Engine with Dynamic Palette Adaptation (DPA)

**Created:** 2026-03-25
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / PRD Update v2.0 — Capability Area 11)
**Architecture Reference:** PRD-Update-CA11 §4.4, DEP-ENG-018 (Mood Context Map), DEP-ENG-016 (Psychological Routing Brief)
**Skill Implementation:** `tools/dpa_engine.py`, `skills/perception/palette-selector/SKILL.md`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

- `d:\Work\The Conscious Coaching Factory\Adele Kasaku branding.json`
- `d:\Work\The Conscious Coaching Factory\branding\Amy branding.json`
- `d:\Work\The Conscious Coaching Factory\lab\Color Psychology for Video Automation.md` (Valdez-Mehrabian PAD Regression)
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Color Psychology in Flyer Design.md` (Elliot-Maier Color-in-Context)
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Design Fluency and Aesthetic-Usability Research.md` (Reber-Schwarz-Winkielman)
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Visual Style Psychology in Coaching.md` (Style-Function Matrix)
- `d:\Work\The Conscious Coaching Factory\lab\Neurocinematics for Social Media.md` (ISC & Editing Structure)
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md` (DEP-ENG-003 Voice DNA, DEP-ENG-016 Psych Routing, DEP-ENG-018 Mood Context)

---

## 2. Overview

### Problem Statement
The CCP currently generates a `branding.json` per coach containing a **static** color system — primary, secondary, accent — extracted from the coach's website by the branding agent. This palette is applied uniformly across all visual outputs: flyers, carousel slides, Excalidraw diagrams, AFFiNE workspace themes, video overlays, and Telegram assets.

This is scientifically wrong.

The Valdez-Mehrabian PAD regression model (1994) proves that the emotional impact of color is driven by **saturation and brightness** — not hue. The Elliot-Maier Color-in-Context Theory (2012) proves that the same hue produces **opposite psychological responses** depending on context. The Labrecque-Milne color-value congruence research (2012) proves that warm colors are perceived as appropriate for hedonic content while cool colors are appropriate for utilitarian content, and **mismatched** color temperatures reduce conversion intent.

A rose-branded coach posting a "Gritty Determination" piece in full rose pink triggers high Pleasure + low Dominance (PAD: P+0.65, D-0.40) — the exact **opposite** of Gritty Determination's target vector (P-0.15, D+0.75). The content's chromatic atmosphere fights its psychological intent. The viewer's limbic system receives the color signal 25ms before reading a single word (Max Planck neuro-temporal research) — the wrong mood is set before the message arrives.

### Solution
FR-CA11-15 introduces the **Dynamic Palette Adaptation (DPA) Engine** — a dual-layer branding system that separates **brand identity** (constant recognition signals) from **content mood** (contextual emotional color). The DPA Engine:

1. **Preserves brand recognition** through locked structural tokens (typography, logo, spacing, watermark placement) — the "Processing Fluency Layer" that triggers the Reber-Schwarz-Winkielman trust response.
2. **Adapts chromatic palette per content piece** using PAD-targeted mood palettes — the "Emotional Congruency Layer" that ensures color temperature matches the content's psychological intent.
3. **Selectively deploys brand hue** when it is congruent with the target PAD vector — the brand color is not banned, it is contextually appropriate.

The `branding.json` schema is extended with a new `moodPalettes` section. The DPA Engine (`dpa_engine.py`) receives the content's mood state from DEP-ENG-018 and the archetype from the Psychological Routing Brief (DEP-ENG-016), computes the target PAD vector, selects the congruent mood palette, and injects it into the visual pipeline alongside the locked brand identity tokens.

### Scope
**In scope:**
- Extended `branding.json` schema with dual-layer architecture.
- `dpa_engine.py` — palette selection engine using PAD target vectors.
- Integration with CCF Expression pipeline (flyers, carousels, video color grading).
- Integration with CVE Canva App (template color injection).
- Integration with AFFiNE workspace theming (FR-CA11-01).
- Brand hue congruence scoring (when to use vs. override the brand color).

**Out of scope:**
- Branding agent website extraction (existing pipeline — unchanged).
- Voice DNA (DEP-ENG-003 — text tone, not visual color).
- Content generation (CCF scripts, CBCS prompts — unaffected).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in DPA |
|---|---|---|
| `DEP-ENG-016` | Psychological Routing Brief | SOURCE — Determines the content archetype (WCS, OH, RP, Hero, Discovery, etc.) which maps to a PAD target vector. |
| `DEP-ENG-018` | Mood Context Map | SOURCE — Determines the audience's current mood state (Escape, Processing, Discovery, Status) which selects the base Kelvin profile. |
| FR-VIS-05 (Canva App) | Visual Composition Engine | CONSUMER — Receives the selected mood palette for template rendering. |
| FR-CA11-01 (Coach Workspace) | AFFiNE Theming | CONSUMER — Receives the brand identity tokens for workspace chrome. |
| FR-CA11-12 (Course Video CMF) | Video Color Grading | CONSUMER — Receives the target PAD vector for ambient color grading. |
| `Abel` (Visual Prompt Architect) | Prompt Engineering | CONSUMER — Uses PAD target to select color descriptors for image generation prompts. |

### Academic Grounding

| Framework | Author(s) | Year | Key Finding for DPA |
|---|---|---|---|
| **PAD Affective Model** | Valdez & Mehrabian | 1994 | Pleasure = f(Brightness), Arousal = f(Saturation), Dominance = f(1/Brightness). Hue is the *least* important emotional driver. |
| **Color-in-Context Theory** | Elliot & Maier | 2012 | Color meanings are not fixed. The same red signals danger in achievement contexts and attraction in mating contexts. Context determines chromatic meaning. |
| **Color-Value Congruence** | Labrecque & Milne | 2012 | Warm colors increase engagement for hedonic content; cool colors increase engagement for utilitarian content. Mismatched temperature reduces conversion. |
| **Processing Fluency** | Reber, Schwarz & Winkielman | 2004 | Aesthetic consistency triggers subconscious trust ("this feels right"). Recognition = structure (fonts, layout, logo), not surface color. |
| **25ms Chromatic Advantage** | Max Planck Institute | 2013 | Color is processed 25ms faster than shape, 150ms faster than text. Color sets the psychological mode *before* the message is read. |
| **Neuro-Temporal Receptive Windows** | Hasson et al. | 2008 | Structured visual sequences synchronize neural responses across viewers. Color grading transitions signal emotional shifts. |

### Technical Decisions

1. **Brand Identity = Structural Tokens (LOCKED):** Typography (font families, weights, scale), spacing system, border radius, shadow definitions, logo placement rules, and watermark configuration are **never modified** per content piece. These elements build the processing fluency that the Reber-Schwarz-Winkielman research proves triggers trust. The viewer's brain recognizes the coach's "visual grammar" subconsciously.

2. **Content Color = PAD-Driven Palettes (DYNAMIC):** Background colors, gradient directions, accent tints, overlay colors, and text highlight colors are selected per content piece based on the PAD target vector. The DPA Engine computes the optimal palette from pre-calibrated mood palette templates.

3. **Brand Hue Congruence Score:** Before applying a mood palette, the DPA Engine calculates a "Brand Hue Congruence Score" (BHCS) — how well the coach's brand hue fits the target PAD vector. If BHCS > 0.65 (the hue's inherent PAD vector is within tolerance of the target), the brand hue is used as the mood palette's accent color. If BHCS < 0.65, a PAD-appropriate alternative is substituted. This means a rose brand color *is* used for Discovery/Escape content (where it's congruent) but *not* for Gritty Determination content (where it contradicts the target).

4. **Coach Override = Opt-In Maximum Brand Saturation:** Some coaches will insist on brand color everywhere. The system supports an `override_mode: brand_saturated` flag that forces brand colors on all content — but this flag exists with a documented warning in the coach onboarding flow explaining the psychological cost. The system defaults to `adaptive` mode.

---

## 4. Implementation Plan

### Stage 1: Extended `branding.json` Schema
*Agent:* System Operator / Branding Agent (`Colette`)
*Inputs:* Existing `branding.json` structure.
*Outputs:* Extended schema with `brandIdentity` and `moodPalettes` sections.

**Steps:**
1. Restructure `branding.json` into two top-level sections:
   - `brandIdentity`: Locked structural tokens (typography, spacing, borderRadius, shadows, logo, watermark).
   - `moodPalettes`: Four base palettes keyed to DEP-ENG-018 mood states (Escape, Processing, Discovery, Status) + content archetype overlays.
2. Add `padTargets` section mapping content archetypes to target PAD vectors (from the Valdez-Mehrabian archetype table in the Color Psychology for Video Automation paper).
3. Add `brandHueAnalysis` section containing the brand's primary hue decomposed into its inherent PAD vector (computed once at onboarding).
4. Add `override_mode` field (values: `adaptive` [default], `brand_saturated`).

**Extended Schema:**

```json
{
  "brandIdentity": {
    "logo": {
      "url": "s3://coach/logo.svg",
      "placement": "top-left",
      "minClearSpace": "16px",
      "watermarkOpacity": 0.08
    },
    "typography": {
      "display": { "fontFamily": "Cormorant Garamond, serif", "weights": { "bold": 700 } },
      "heading": { "fontFamily": "Cormorant Garamond, serif", "weights": { "semibold": 600, "medium": 500 } },
      "body": { "fontFamily": "Poppins, sans-serif", "weights": { "regular": 400, "medium": 500 } },
      "scale": { "h1": "2rem", "h2": "1.5rem", "h3": "1.25rem", "body": "1rem", "small": "0.875rem" },
      "lineHeight": { "tight": "1.25", "normal": "1.5", "relaxed": "1.75" }
    },
    "structuralTokens": {
      "spacing": { "xs": "0.25rem", "sm": "0.5rem", "md": "1rem", "lg": "1.5rem", "xl": "2rem" },
      "borderRadius": { "sm": "0.125rem", "md": "0.375rem", "lg": "0.5rem", "xl": "0.75rem", "full": "9999px" },
      "shadows": {
        "sm": "0 1px 2px 0 rgb(0 0 0 / 0.05)",
        "md": "0 4px 6px -1px rgb(0 0 0 / 0.1)",
        "lg": "0 10px 15px -3px rgb(0 0 0 / 0.1)"
      }
    }
  },

  "brandHueAnalysis": {
    "primaryHue": "#B5CCC4",
    "hueName": "Sage Mint",
    "inherentPAD": { "P": 0.55, "A": -0.30, "D": -0.25 },
    "kelvinEquivalent": "4500K",
    "temperatureClass": "cool_neutral",
    "congruentMoods": ["escape", "processing"],
    "incongruentMoods": ["discovery_high_energy", "status_luxury"]
  },

  "moodPalettes": {
    "escape": {
      "description": "Warm neutrals, low tension. For audiences seeking rest and comfort.",
      "kelvinRange": "2700K-3200K",
      "targetPAD": { "P": 0.70, "A": -0.40, "D": -0.30 },
      "background": { "primary": "#F5F0E8", "gradient": "linear-gradient(180deg, #F5F0E8 0%, #EDE5D8 100%)" },
      "accent": "#D4A574",
      "text": { "primary": "#3D3630", "secondary": "#87796A" },
      "overlay": "rgba(245, 240, 232, 0.85)"
    },
    "processing": {
      "description": "Cool foundation, high contrast. For analytical depth and trust.",
      "kelvinRange": "5000K-6500K",
      "targetPAD": { "P": 0.25, "A": 0.55, "D": 0.45 },
      "background": { "primary": "#1A2332", "gradient": "linear-gradient(180deg, #1A2332 0%, #0F1722 100%)" },
      "accent": "#5A8FA8",
      "text": { "primary": "#F0F4F8", "secondary": "#A0B4C0" },
      "overlay": "rgba(26, 35, 50, 0.90)"
    },
    "discovery": {
      "description": "Energetic mid-warmth. For approach motivation and curiosity.",
      "kelvinRange": "3000K-4000K",
      "targetPAD": { "P": 0.75, "A": 0.85, "D": -0.20 },
      "background": { "primary": "#FFF5F0", "gradient": "linear-gradient(135deg, #FFF5F0 0%, #FFE8DC 100%)" },
      "accent": "#E8657A",
      "text": { "primary": "#2D1F1A", "secondary": "#8B5E4D" },
      "overlay": "rgba(255, 245, 240, 0.80)"
    },
    "status": {
      "description": "Premium dark. Exclusivity, luxury, intimacy.",
      "kelvinRange": "dark_premium",
      "targetPAD": { "P": 0.10, "A": 0.20, "D": 0.85 },
      "background": { "primary": "#0D0D0D", "gradient": "linear-gradient(180deg, #0D0D0D 0%, #1A1A1A 100%)" },
      "accent": "#C9A96E",
      "text": { "primary": "#F5F0E8", "secondary": "#8A7D6A" },
      "overlay": "rgba(13, 13, 13, 0.95)"
    }
  },

  "archetypePADTargets": {
    "personal_low": { "P": -0.65, "A": -0.70, "D": 0.30, "moodBase": "processing", "saturationShift": -0.35 },
    "hopeful": { "P": 0.80, "A": 0.10, "D": -0.45, "moodBase": "escape", "saturationShift": 0.10 },
    "gritty_determination": { "P": -0.15, "A": 0.35, "D": 0.75, "moodBase": "processing", "saturationShift": -0.20 },
    "playful_pop": { "P": 0.75, "A": 0.85, "D": -0.20, "moodBase": "discovery", "saturationShift": 0.30 },
    "graphic_novel": { "P": -0.10, "A": 0.15, "D": 0.85, "moodBase": "status", "saturationShift": -0.40 },
    "soft_pastel": { "P": 0.85, "A": -0.55, "D": -0.65, "moodBase": "escape", "saturationShift": -0.15 },
    "relief_peak": { "P": 0.80, "A": -0.30, "D": -0.40, "moodBase": "escape", "saturationShift": 0.05 },
    "worst_case_scenario": { "P": -0.50, "A": 0.60, "D": 0.50, "moodBase": "processing", "saturationShift": -0.30 },
    "observational_humor": { "P": 0.60, "A": 0.40, "D": -0.10, "moodBase": "discovery", "saturationShift": 0.15 },
    "urgent_alert": { "P": -0.35, "A": 0.90, "D": 0.25, "moodBase": "discovery", "saturationShift": 0.40 }
  },

  "override_mode": "adaptive"
}
```

### Stage 2: DPA Engine Implementation
*Agent:* System Operator
*Inputs:* Extended `branding.json`, content archetype (from DEP-ENG-016), audience mood state (from DEP-ENG-018).
*Outputs:* Resolved palette (JSON) ready for injection into visual pipelines.

**Steps:**
1. Implement `dpa_engine.py` with the following pipeline:

```
Input: coach_id, content_archetype, audience_mood_state
  │
  ├── 1. Load coach's branding.json
  │
  ├── 2. Look up archetypePADTargets[content_archetype]
  │      → target PAD vector + moodBase + saturationShift
  │
  ├── 3. Select moodPalettes[moodBase] as the base palette
  │
  ├── 4. Apply saturationShift to base palette colors
  │      (HSL manipulation: shift S component by saturationShift)
  │
  ├── 5. Compute Brand Hue Congruence Score (BHCS):
  │      BHCS = 1 - (euclidean_distance(brandHueAnalysis.inherentPAD, targetPAD) / max_distance)
  │      If BHCS > 0.65: inject brand hue as accent color
  │      If BHCS <= 0.65: use mood palette's default accent
  │
  ├── 6. Merge brandIdentity (locked) + resolved mood palette (dynamic)
  │      into a single "resolved_palette" JSON
  │
  └── Output: resolved_palette
```

2. Expose as FastAPI endpoint: `POST /palette/resolve`
   - Request: `{ "coach_id": "uuid", "content_archetype": "gritty_determination", "audience_mood_state": "processing" }`
   - Response: `resolved_palette` JSON with all tokens needed by visual pipelines.

### Stage 3: Pipeline Integration
*Agent:* System Operator + Visual Pipeline Agents
*Inputs:* `resolved_palette` from DPA Engine.
*Outputs:* Visual assets rendered with contextually appropriate colors.

**Steps:**
1. **CCF Flyer/Carousel Pipeline:** Before `Abel` generates visual prompts, call `POST /palette/resolve`. Inject the resolved palette's `background`, `accent`, and `text` colors into the VCB (Visual Composition Brief). `Abel` uses these colors as prompt descriptors (e.g., "cool steel-blue background, desaturated tones, high contrast").
2. **CVE Canva App:** The Canva App's template system reads the resolved palette and applies it to the composition's background, text, and accent layers. Brand typography and logo placement remain locked.
3. **CMF Video Grading:** The `kelvinRange` from the resolved palette is passed to the CMF sound design engine and color grading LUT selector. Course videos (FR-CA11-12) and short-form clips use the target Kelvin range for ambient color temperature.
4. **AFFiNE Workspace Theming (FR-CA11-01):** The brandIdentity tokens (typography, spacing, border-radius) are applied to the AFFiNE workspace chrome. Mood palettes are NOT applied to the workspace — the workspace uses a neutral, high-fluency theme with brand accent colors for interactive elements only.
5. **Excalidraw Diagrams (FR-CA11-09, FR-CA11-10):** Progress charts and concept diagrams use the resolved palette's accent color for data visualization. Brand typography is applied to labels.

---

## 5. Primary Output Schema

**Data Object:** Resolved Palette Schema (`DEP-ENG-085` PROPOSED)

**Resolved Palette (Output of `POST /palette/resolve`):**

```json
{
  "resolved_palette_id": "uuid-palette-001",
  "coach_id": "uuid-coach-001",
  "content_archetype": "gritty_determination",
  "audience_mood_state": "processing",
  "target_PAD": { "P": -0.15, "A": 0.35, "D": 0.75 },
  "bhcs": 0.42,
  "brand_hue_used": false,

  "identity": {
    "logo_url": "s3://coach/logo.svg",
    "logo_placement": "top-left",
    "watermark_opacity": 0.08,
    "typography": {
      "display": "Cormorant Garamond, serif",
      "body": "Poppins, sans-serif"
    }
  },

  "palette": {
    "background": { "primary": "#1A2332", "gradient": "linear-gradient(180deg, #1A2332 0%, #0F1722 100%)" },
    "accent": "#5A8FA8",
    "text": { "primary": "#F0F4F8", "secondary": "#A0B4C0" },
    "overlay": "rgba(26, 35, 50, 0.90)",
    "kelvin_range": "5000K-6500K",
    "saturation_adjustment": -0.20
  }
}
```

**When BHCS > 0.65 (brand hue is congruent):**

```json
{
  "content_archetype": "playful_pop",
  "bhcs": 0.78,
  "brand_hue_used": true,
  "palette": {
    "background": { "primary": "#FFF5F0" },
    "accent": "#B5CCC4",
    "text": { "primary": "#2D1F1A" }
  }
}
```

---

## 6. Backward Compatibility Fallback

1. **Override Mode:** Coaches who prefer uniform branding set `override_mode: brand_saturated`. All content uses brand colors. The system logs a `BRANDING_OVERRIDE_ACTIVE` warning in the Fingerprint Archive so the Data Analyst (FR43) can compare performance of adaptive vs. saturated content.
2. **Schema Migration:** Existing `branding.json` files (Adele Kasaku format, Amy format) are auto-migrated by extracting `colors`/`colorSystem` → `brandIdentity` and generating default `moodPalettes` using the Valdez-Mehrabian table. The `brandHueAnalysis` is computed once from the primary color's HSL values.
3. **DPA Failure:** If `dpa_engine.py` is unavailable, the pipeline falls back to the brand's primary color system (existing behavior). No content is blocked.

---

## 7. Tasks

- [ ] **Task 1:** Design and validate the extended `branding.json` schema (dual-layer architecture).
- [ ] **Task 2:** Write `dpa_engine.py` with palette resolution pipeline (PAD target lookup, mood palette selection, saturation shift, BHCS calculation).
- [ ] **Task 3:** Implement `POST /palette/resolve` FastAPI endpoint.
- [ ] **Task 4:** Write schema migration script for existing `branding.json` files (Adele Kasaku format → extended format).
- [ ] **Task 5:** Wire DPA Engine into CCF flyer/carousel pipeline (inject resolved palette into VCB before `Abel`).
- [ ] **Task 6:** Wire DPA Engine into CVE Canva App template system.
- [ ] **Task 7:** Wire DPA Engine into CMF video color grading LUT selector.
- [ ] **Task 8:** Compute `brandHueAnalysis` for all existing coach brand files.
- [ ] **Task 9:** Document coach-facing explanation of adaptive vs. brand_saturated modes for onboarding flow.

---

## 8. Acceptance Criteria

- [ ] **AC1 (PAD Congruence):** Generate a "Gritty Determination" flyer for a rose-branded coach. Assert the flyer uses steel-blue/desaturated tones (BHCS < 0.65 → brand hue NOT used as accent). Assert brand typography and logo are present.
- [ ] **AC2 (Brand Hue Deployment):** Generate a "Discovery/Playful Pop" flyer for the same rose-branded coach. Assert the flyer uses warm rose tones (BHCS > 0.65 → brand hue IS used as accent).
- [ ] **AC3 (Locked Identity):** Compare 4 flyers across 4 different archetypes for the same coach. Assert all 4 share identical typography, logo placement, spacing, and watermark. Assert all 4 have *different* background colors and accent tones.
- [ ] **AC4 (Schema Migration):** Migrate Adele Kasaku's `branding.json`. Assert the extended schema contains all 4 mood palettes and a computed `brandHueAnalysis` with correct inherent PAD vector.
- [ ] **AC5 (Override Mode):** Set `override_mode: brand_saturated`. Generate a "Gritty Determination" flyer. Assert the brand's primary color is used everywhere. Assert `BRANDING_OVERRIDE_ACTIVE` is logged in the Fingerprint Archive.
- [ ] **AC6 (Video Grading):** Generate a course video (FR-CA11-12) with archetype "Hopeful". Assert the video's ambient color temperature falls within the Escape palette's Kelvin range (2700K-3200K).
- [ ] **AC7 (25ms Compliance):** For each resolved palette, assert the background-to-text contrast ratio meets WCAG 2.1 AA minimum (4.5:1). This ensures processing fluency is not broken by low-contrast mood palettes.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| DEP-ENG-016 (Psychological Routing Brief) | Internal | Provides content archetype for PAD target lookup. |
| DEP-ENG-018 (Mood Context Map) | Internal | Provides audience mood state for base palette selection. |
| FR-VIS-05 (Canva App) | Internal | Consumer of resolved palette. |
| FR-CA11-01 (Coach Workspace) | Internal | Consumer of brand identity tokens. |
| FR-CA11-12 (Course Video CMF) | Internal | Consumer of Kelvin range for color grading. |
| Valdez-Mehrabian PAD Model (1994) | External/Academic | Source of PAD regression equations. |
| Elliot-Maier Color-in-Context Theory (2012) | External/Academic | Theoretical basis for contextual color application. |
| Labrecque-Milne Color-Value Congruence (2012) | External/Academic | Empirical basis for warm/cool temperature matching. |

---

## 10. Testing Strategy

### Unit Tests
- **BHCS Calculation:** Pass known brand hue PAD vectors and target PAD vectors. Assert BHCS values match expected Euclidean distance scores.
- **Saturation Shift:** Pass a base palette + saturation shift value. Assert HSL S-component is correctly modified for all palette colors.
- **WCAG Contrast:** For each mood palette, assert all background-text pairs meet >= 4.5:1 contrast ratio.

### Integration Tests
- **Full Pipeline (CCF):** Trigger a CCF weekly pipeline for a test coach with archetype "Personal Low" → assert DPA Engine is called → assert resolved palette has cool, desaturated tones → assert final flyer uses resolved palette colors with brand typography.
- **Full Pipeline (CMF Video):** Trigger a course video with archetype "Hopeful" → assert Kelvin range is 2700K-3200K → assert video's dominant color temperature is within range.

### A/B Performance Tests
- **Adaptive vs. Saturated:** Over a 4-week period for a test coach, produce 50% of content with `adaptive` mode and 50% with `brand_saturated` mode. Compare engagement metrics (likes, shares, saves, click-through) between the two groups. Assert `adaptive` mode produces statistically significant higher engagement on content archetypes where BHCS < 0.65.

### Expert Review
- **Color Psychology Audit:** First 10 resolved palettes are reviewed against the Valdez-Mehrabian archetype table to ensure PAD target alignment. Any palette producing a PAD error > 0.20 in any dimension triggers a calibration review.
