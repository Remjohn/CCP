# Tech-Spec: FR-VIS-07 — Format & Aspect Ratio Enforcement

**Created:** 2026-03-18
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §Visual Intelligence Pipeline, CVE_Documentation_V2 §8.3, CVE_Documentation_V3 §5
**Skill Implementation:** `skills/visuals/visual_format_constraint_adapter.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md` — FR-VIS-07 definition (lines 1028)
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CVE_Documentation_V2.md` — §8.3 Aspect Ratio & Format Specifications, §8 Conscious Canva App Architecture
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CVE_Documentation_V3.md` — §5 Updated Aspect Ratios, §4 Style Scoping Updates
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Carousel Physiological State Architecture Research.md` — Aspect ratio → GSR arousal coupling, slide dimension → cognitive load relationship
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Cinematographic Emotional Grammar Framework Research.md` — Frame composition constraints, CGCS deterministic formatting rules
- `d:\Work\The Conscious Coaching Factory\docs\architecture\FR50_Sovereign_Image_Rule_Tech_Spec.md` — Reference template for structure and depth

---

## 2. Overview

### Problem Statement
The Conscious Visual Engine produces visual assets across multiple content formats — carousels, single images, polls, 9-grids, tweet quotes, supervisuals — each requiring specific pixel dimensions and aspect ratios. Without a deterministic pre-production constraint layer, downstream agents (Abel, Paradoxe, Aurore) risk generating compositions in incorrect dimensions, producing assets that are clipped by platform rendering engines, violate physiological arousal coupling calibrated to specific aspect ratios, or force expensive post-generation reformatting that degrades visual quality. Instagram's rendering engine crops non-compliant ratios unpredictably, destroying carefully engineered gaze geometry and zone positioning.

### Solution
FR-VIS-07 establishes the `visual-format-constraint-adapter` — a deterministic pre-production gate that fires **before any other style selection, recipe protocol, or image sourcing logic**. It reads the format designation from the upstream script output (DEP-ENG-011) and emits a locked `format_constraint_envelope` containing the exact pixel dimensions, aspect ratio, DPI, and color space for every slide in the composition. No downstream agent may override these locked values. The adapter acts as an architectural hard boundary: if a format is not in the approved registry, the pipeline halts with an explicit rejection — it does not guess or approximate.

### Scope
**In scope:**
- The `visual-format-constraint-adapter` constraint injection logic.
- The `Format_Constraint_Registry` mapping every approved content format to its locked dimensional specification.
- Validation logic rejecting unrecognized format designations.
- Integration with Abel's VCB generation (FR-VIS-01) as a mandatory upstream dependency.

**Out of scope:**
- Style scoping rules (handled by FR-VIS-08).
- Image type validity checks (handled by FR-VIS-13 / Gate V-00).
- Canvas export slicing logic (handled by FR-VIS-05).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-011` | Finalized Content Output | INPUT — Provides the `content_format` designation from upstream script compilation. |
| `DEP-VIS-002` | Visual Recipe Protocol Library | DOWNSTREAM CONSUMER — Receives the locked `format_constraint_envelope` and selects recipes within dimensional constraints. |
| `DEP-VIS-005` | Visual Composition Brief Schema | DOWNSTREAM CONSUMER — VCB must embed the format envelope; Abel cannot override locked dimensions. |
| `DEP-ENG-041` | Receipt Chain Guard | AUDIT — Cryptographic hash of the format envelope is written at constraint injection. |
| `visual-format-constraint-adapter` | Format Constraint Adapter | TOOL — The executable adapter that performs format lookup, validation, and envelope emission. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Applied |
|---|---|---|---|
| **Carousel Physiological State Architecture** | CCP Research Lab | 2026 | The 4:5 aspect ratio (1080×1350px) was validated against GSR arousal measurements during vertical scroll behavior. Taller-than-wide frames increase dwell time by 18-23% compared to 1:1 frames because the user's thumb must traverse more vertical distance, creating a micro-commitment loop. The 9:16 format used for polls exploits full-bleed immersion, suppressing peripheral visual competition and channeling attention into the binary choice zone. Each aspect ratio is not arbitrary — it is a physiological engagement tool. |
| **Cinematographic Emotional Grammar Framework** | CCP Research Lab | 2026 | The CGCS coding scheme specifies that frame composition must be deterministic before any lighting or color grammar is applied. A prompt compiled for a 4:5 frame uses fundamentally different vertical composition rules (rule of thirds with 3 horizontal bands) than a 1:1 frame (central focus with radial symmetry). Locking the format before prompt compilation prevents the Cinematographic Grammar from being applied to the wrong compositional grid, which would produce visually incoherent results. |

### Technical Decisions
1. **Pre-Production Firing Order:** The format constraint adapter fires as the absolute first operation in the visual pipeline — before style scoping (FR-VIS-08), before Gate V-00 (FR-VIS-13), before TIAR queries (FR-VIS-02), before Abel's VCB generation (FR-VIS-01). This is because every downstream decision depends on knowing the exact pixel canvas dimensions. A recipe selected for 4:5 is invalid for 1:1. A PSSL prompt compiled for 1080×1350 produces garbage when rendered at 1080×1080.
2. **Immutable Envelope Pattern:** The adapter emits a `format_constraint_envelope` that is cryptographically sealed via DEP-ENG-041. Downstream agents receive a read-only copy. If any agent attempts to modify dimensions, the Receipt Chain Guard detects the hash mismatch and halts the pipeline. This prevents "creative overrides" that would produce platform-incompatible assets.
3. **Explicit Rejection over Fallback:** If the upstream `content_format` designation does not match any entry in the `Format_Constraint_Registry`, the adapter rejects with `FORMAT_NOT_RECOGNIZED` and halts processing. It does not approximate to the "closest" format. An unrecognized format indicates an upstream compilation error — guessing dimensions would produce an asset that looks correct in the Canva App but gets clipped or distorted on the target platform.

---

## 4. Implementation Plan

### Stage 1: Format Designation Extraction
*Agent:* `visual-format-constraint-adapter`
*Inputs:* `content_output_id` (from DEP-ENG-011), `content_format` string, `slide_count` integer.
*Outputs:* Validated `content_format` string or `FORMAT_NOT_RECOGNIZED` rejection.
*Failure Condition:* Missing or null `content_format` field in upstream output; adapter rejects with explicit error and halts pipeline.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. The adapter receives the finalized content output package from DEP-ENG-011.
2. Extracts the `content_format` field — a string enum value set during script compilation (e.g., `carousel_dopamine_cliff`, `single_observational_humor`, `poll_archetypical`, `nine_grid_accumulation`, `single_tweet_quote`, `single_supervisual`, `single_conceptual_contrast`, `carousel_listicle`, `carousel_timeline`, `carousel_comparison`, `single_worst_case`, `single_conceptual_contrast_simultaneous`).
3. Validates the extracted format against the `Format_Constraint_Registry` (see §5).
4. If the format is not found in the registry, emits `FORMAT_NOT_RECOGNIZED` with the invalid format string, the `content_output_id`, and a timestamp. Pipeline halts.
5. If the format is found, proceeds to Stage 2.

### Stage 2: Constraint Envelope Assembly
*Agent:* `visual-format-constraint-adapter`
*Inputs:* Validated `content_format` string, `slide_count` integer, `Format_Constraint_Registry` lookup result.
*Outputs:* `format_constraint_envelope` JSON object (see §5).
*Failure Condition:* Registry entry missing required fields (width_px, height_px, aspect_ratio, dpi, color_space); adapter rejects with `REGISTRY_INTEGRITY_ERROR`.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Looks up the `content_format` in the `Format_Constraint_Registry` and retrieves the locked dimensional specification.
2. Validates that all required fields are present and non-null: `width_px`, `height_px`, `aspect_ratio`, `dpi`, `color_space`, `bleed_zone_px`.
3. Assembles the `format_constraint_envelope` containing:
   - `content_output_id` — traceability back to upstream.
   - `content_format` — the validated format string.
   - `width_px` — exact pixel width (e.g., 1080).
   - `height_px` — exact pixel height (e.g., 1350).
   - `aspect_ratio` — human-readable ratio string (e.g., `4:5`).
   - `dpi` — dots per inch for export (always 72 for digital, 300 for print-ready).
   - `color_space` — always `sRGB` for digital social delivery.
   - `bleed_zone_px` — edge bleed for carousel stitch alignment (40px for carousels, 0px for singles).
   - `slide_count` — number of slides in the composition.
   - `per_slide_dimensions` — array of `{slide_index, width_px, height_px}` for each slide (uniform for standard formats, potentially variable for hybrid formats).
4. Generates a SHA-256 hash of the assembled envelope.
5. Writes the hash to the Receipt Chain Guard (DEP-ENG-041).
6. Emits the sealed `format_constraint_envelope` downstream.

### Stage 3: Downstream Injection
*Agent:* `visual-format-constraint-adapter`
*Inputs:* Sealed `format_constraint_envelope`.
*Outputs:* Envelope delivered to Abel (FR-VIS-01 / VCB generation) and logged for all downstream consumers.
*Failure Condition:* Downstream agent reports dimension mismatch against sealed envelope; Receipt Chain Guard detects hash discrepancy and halts pipeline.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. The sealed envelope is injected into Abel's VCB generation context as a mandatory read-only parameter.
2. Abel's 9-step VCB process (FR-VIS-01) reads the envelope at Step 1 (format determination) and uses the locked dimensions for all subsequent PSSL parameter assignments, zone positioning, and layout decisions.
3. The envelope is also forwarded to:
   - Paradoxe (FR-VIS-03) — prompt compilation uses exact pixel dimensions for composition directives.
   - Aurore (FR-VIS-09/10) — image search queries include resolution constraints from the envelope.
   - Conscious Canva App (FR-VIS-05) — template loading uses the locked dimensions.
4. Any downstream agent that attempts to modify `width_px` or `height_px` triggers a Receipt Chain Guard violation via hash mismatch detection.

---

## 5. Primary Output Schema

### Schema Name: `Format_Constraint_Registry`

```json
{
  "carousel_dopamine_cliff":     { "width_px": 1080, "height_px": 1350, "aspect_ratio": "4:5", "dpi": 72, "color_space": "sRGB", "bleed_zone_px": 40 },
  "carousel_listicle":           { "width_px": 1080, "height_px": 1350, "aspect_ratio": "4:5", "dpi": 72, "color_space": "sRGB", "bleed_zone_px": 40 },
  "carousel_timeline":           { "width_px": 1080, "height_px": 1350, "aspect_ratio": "4:5", "dpi": 72, "color_space": "sRGB", "bleed_zone_px": 40 },
  "carousel_comparison":         { "width_px": 1080, "height_px": 1350, "aspect_ratio": "4:5", "dpi": 72, "color_space": "sRGB", "bleed_zone_px": 40 },
  "single_observational_humor":  { "width_px": 1080, "height_px": 1350, "aspect_ratio": "4:5", "dpi": 72, "color_space": "sRGB", "bleed_zone_px": 0 },
  "single_worst_case":           { "width_px": 1080, "height_px": 1350, "aspect_ratio": "4:5", "dpi": 72, "color_space": "sRGB", "bleed_zone_px": 0 },
  "single_conceptual_contrast":  { "width_px": 1080, "height_px": 1350, "aspect_ratio": "4:5", "dpi": 72, "color_space": "sRGB", "bleed_zone_px": 0 },
  "poll_archetypical":           { "width_px": 1080, "height_px": 1920, "aspect_ratio": "9:16", "dpi": 72, "color_space": "sRGB", "bleed_zone_px": 0 },
  "poll_stereotypical":          { "width_px": 1080, "height_px": 1920, "aspect_ratio": "9:16", "dpi": 72, "color_space": "sRGB", "bleed_zone_px": 0 },
  "poll_controversial_dilemma":  { "width_px": 1080, "height_px": 1920, "aspect_ratio": "9:16", "dpi": 72, "color_space": "sRGB", "bleed_zone_px": 0 },
  "single_tweet_quote":          { "width_px": 1080, "height_px": 1080, "aspect_ratio": "1:1", "dpi": 72, "color_space": "sRGB", "bleed_zone_px": 0 },
  "single_supervisual":          { "width_px": 1080, "height_px": 1080, "aspect_ratio": "1:1", "dpi": 72, "color_space": "sRGB", "bleed_zone_px": 0 },
  "single_conceptual_contrast_simultaneous": { "width_px": 1080, "height_px": 1080, "aspect_ratio": "1:1", "dpi": 72, "color_space": "sRGB", "bleed_zone_px": 0 },
  "single_observational_humor_square": { "width_px": 1080, "height_px": 1080, "aspect_ratio": "1:1", "dpi": 72, "color_space": "sRGB", "bleed_zone_px": 0 },
  "nine_grid_accumulation":      { "width_px": 1080, "height_px": 1350, "aspect_ratio": "4:5", "dpi": 72, "color_space": "sRGB", "bleed_zone_px": 0 }
}
```

### Schema Name: `Format_Constraint_Envelope.json`

```json
{
  "envelope_id": "FCE-JP-20260318-001",
  "content_output_id": "CO-JP-20260318-012-CAROUSEL",
  "content_format": "carousel_dopamine_cliff",
  "width_px": 1080,
  "height_px": 1350,
  "aspect_ratio": "4:5",
  "dpi": 72,
  "color_space": "sRGB",
  "bleed_zone_px": 40,
  "slide_count": 7,
  "per_slide_dimensions": [
    { "slide_index": 0, "width_px": 1080, "height_px": 1350 },
    { "slide_index": 1, "width_px": 1080, "height_px": 1350 },
    { "slide_index": 2, "width_px": 1080, "height_px": 1350 },
    { "slide_index": 3, "width_px": 1080, "height_px": 1350 },
    { "slide_index": 4, "width_px": 1080, "height_px": 1350 },
    { "slide_index": 5, "width_px": 1080, "height_px": 1350 },
    { "slide_index": 6, "width_px": 1080, "height_px": 1350 }
  ],
  "seal_hash": "a3f8c9d2e1b4a7f6c3d9e0b1a2f5c8d7e4b3a6f9c2d1e0b5a8f7c4d3e2b1a0",
  "receipt_chain_block": "RCB-VIS07-20260318-001",
  "timestamp_utc": "2026-03-18T01:33:20Z"
}
```

---

## 6. Backward Compatibility Fallback

If the upstream content output (DEP-ENG-011) was compiled by an older pipeline version that does not include a `content_format` field, the adapter attempts a secondary extraction:
1. Reads the `recipe_id` field from the content output.
2. Cross-references the `recipe_id` against the Visual Recipe Protocol Library (DEP-VIS-002) to derive the implied format.
3. If the cross-reference succeeds, the derived format is used and a `LEGACY_FORMAT_DERIVATION` warning is logged.
4. If the cross-reference fails (recipe not found or recipe does not specify a format), the adapter emits `FORMAT_NOT_RECOGNIZED` and halts. It does not default to 1:1 or any "safe" ratio. The pipeline must be recompiled with the updated upstream output structure.

---

## 7. Tasks

- [ ] **Task 1:** Create the `Format_Constraint_Registry` as a versioned JSON configuration file at `config/visual_pipeline/format_constraint_registry.json`. Populate all 15 format entries with exact pixel dimensions, aspect ratios, DPI, color space, and bleed zone values per the PRD specification.
- [ ] **Task 2:** Write `visual_format_constraint_adapter.py` — the adapter that reads `content_format` from DEP-ENG-011, validates against the registry, and assembles the sealed `format_constraint_envelope`.
- [ ] **Task 3:** Implement the SHA-256 envelope sealing mechanism and integrate with Receipt Chain Guard (DEP-ENG-041) for cryptographic hash write at every stage.
- [ ] **Task 4:** Implement the legacy `recipe_id` → `content_format` cross-reference fallback for backward compatibility with older pipeline versions.
- [ ] **Task 5:** Add the `FORMAT_NOT_RECOGNIZED` and `REGISTRY_INTEGRITY_ERROR` error types to the pipeline's error taxonomy, including structured error payloads with `content_output_id`, invalid format string, and timestamp.
- [ ] **Task 6:** Write the downstream injection interface — ensure Abel (FR-VIS-01), Paradoxe (FR-VIS-03), Aurore (FR-VIS-09/10), and Canva App (FR-VIS-05) all receive the sealed envelope as a read-only dependency.
- [ ] **Task 7:** Implement the hash mismatch detection guard — if any downstream agent writes a VCB or prompt with dimensions differing from the sealed envelope, the Receipt Chain Guard triggers a `DIMENSION_OVERRIDE_VIOLATION` and halts the pipeline.

---

## 8. Acceptance Criteria

- [ ] **AC1 (4:5 Carousel Lock):** Submit a `content_format: carousel_dopamine_cliff` with `slide_count: 7`. Assert the adapter emits an envelope with `width_px: 1080`, `height_px: 1350`, `aspect_ratio: "4:5"`, `bleed_zone_px: 40`, and exactly 7 entries in `per_slide_dimensions`, each at 1080×1350. *Failure Example:* The adapter emits 1080×1080 because a developer assumed carousels are square, or `bleed_zone_px` is missing.
- [ ] **AC2 (9:16 Poll Lock):** Submit `content_format: poll_archetypical`. Assert the envelope contains `width_px: 1080`, `height_px: 1920`, `aspect_ratio: "9:16"`, `bleed_zone_px: 0`. *Failure Example:* The adapter applies the carousel bleed zone (40px) to a poll, creating a 1040×1880 effective canvas.
- [ ] **AC3 (1:1 Square Lock):** Submit `content_format: single_tweet_quote`. Assert `width_px: 1080`, `height_px: 1080`, `aspect_ratio: "1:1"`. *Failure Example:* The adapter defaults to 4:5 because the format string is "single_*" and a developer pattern-matched on "single" → 4:5.
- [ ] **AC4 (Unrecognized Format Rejection):** Submit `content_format: "story_vertical_fullscreen"` — a format that does not exist in the registry. Assert the adapter halts with `FORMAT_NOT_RECOGNIZED` and does NOT produce a fallback envelope. *Failure Example:* The adapter defaults to 1:1 and silently continues, producing an asset that gets cropped on Instagram.
- [ ] **AC5 (Immutability Enforcement):** After the adapter emits a sealed 4:5 envelope, have Abel write a VCB with `width_px: 1080, height_px: 1080` (attempting to override to square). Assert the Receipt Chain Guard detects the hash mismatch and triggers `DIMENSION_OVERRIDE_VIOLATION`. *Failure Example:* Abel's override propagates downstream, Paradoxe compiles a prompt for a square frame, but the Canva App template is 4:5, creating a composition with a 270px black bar at the bottom.
- [ ] **AC6 (Legacy Fallback):** Submit a content output with no `content_format` field but with `recipe_id: "RCP-CAROUSEL-LISTICLE-001"`. Assert the adapter derives `carousel_listicle` via cross-reference, emits the correct 4:5 envelope, and logs a `LEGACY_FORMAT_DERIVATION` warning. *Failure Example:* The adapter crashes on the missing field instead of attempting the cross-reference.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| DEP-ENG-011 (Finalized Content Output) | Internal | Upstream source of `content_format` and `slide_count`. |
| DEP-VIS-002 (Visual Recipe Protocol Library) | Internal | Cross-reference for legacy fallback; downstream consumer of format constraints. |
| DEP-ENG-041 (Receipt Chain Guard) | Internal | Cryptographic envelope sealing and hash mismatch detection. |
| FR-VIS-01 (VCB Generation) | Internal | Primary downstream consumer — Abel's format determination step reads the locked envelope. |
| FR-VIS-03 (PSSL Prompt Compilation) | Internal | Downstream consumer — Paradoxe uses pixel dimensions for composition directives. |
| FR-VIS-05 (Canvas Composition) | Internal | Downstream consumer — Canva App template loading uses locked dimensions. |
| FR-VIS-08 (Style Scoping) | Internal | Parallel constraint — fires after format locking to apply style rules within the locked format. |
| FR-VIS-13 (Image Type Validity Gate) | Internal | Downstream gate — Gate V-00 validates image types against the locked format. |

---

## 10. Testing Strategy

### Unit Tests
- **Registry Completeness:** Load `format_constraint_registry.json` and assert all 15 format entries contain non-null values for `width_px`, `height_px`, `aspect_ratio`, `dpi`, `color_space`, and `bleed_zone_px`.
- **Envelope Assembly:** Provide a mock content output with `content_format: "carousel_timeline"` and `slide_count: 5`. Assert the assembled envelope has exactly 5 entries in `per_slide_dimensions`, each at 1080×1350, with `bleed_zone_px: 40`.
- **Hash Determinism:** Assemble the same envelope twice with identical inputs. Assert both produce identical SHA-256 hashes. Then modify `slide_count` by 1 and assert the hash changes.

### Integration Tests
- **Full Pipeline Lock:** Submit a `carousel_dopamine_cliff` content output through the complete visual pipeline (VIS-07 → VIS-01 → VIS-03 → VIS-05). Assert the Canva App template loads with 1080×1350 dimensions and the exported PNG measures exactly 1080×1350 pixels per slide.
- **Cross-Format Validation:** Submit one asset of each aspect ratio type (4:5, 9:16, 1:1). Assert each produces the correct pixel dimensions through to Canva App export.

### Safety Tests (ADR-01 Quarantine Security)
- **Injection Resistance:** Inject `content_format: "carousel_dopamine_cliff; DROP TABLE format_registry;"` into the content output. Assert the adapter treats the entire string as a single lookup key, fails to match in the registry, and emits `FORMAT_NOT_RECOGNIZED` without executing any embedded commands.
- **Envelope Tampering:** Intercept the sealed envelope between VIS-07 and VIS-01. Modify `height_px` from 1350 to 1080. Assert the Receipt Chain Guard detects the hash mismatch at Abel's VCB generation stage and halts with `DIMENSION_OVERRIDE_VIOLATION`.
