# Tech-Spec: FR-VIS-08 — Style Scoping

**Created:** 2026-03-18
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §Visual Intelligence Pipeline, CVE_Documentation_V2 §8, CVE_Documentation_V3 §4
**Skill Implementation:** `skills/visuals/visual_format_constraint_adapter.py` (style scoping extension)
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md` — FR-VIS-08 definition (line 1030)
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CVE_Documentation_V2.md` — §8 Visual Style Architecture, §8.1 Style Selection Logic, §9 Paradoxe Prompt Compilation
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CVE_Documentation_V3.md` — §4 Updated Style Scoping Rules, §5 Format-Style Intersection Matrix
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Visual Style Psychology in Coaching.md` — Style-Function Matrix, TII-indexed style selection, realism vs. stylization psychological impact
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Cinematographic Emotional Grammar Framework Research.md` — Lighting and color grammar dependency on visual style, CGCS incompatibility between illustrated and cinematic grammar systems
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Tribal Imageability and Cultural Half-Life.md` — Style congruence with tribal noun potency, illustrated styles and imageability inflation
- `d:\Work\The Conscious Coaching Factory\docs\architecture\FR50_Sovereign_Image_Rule_Tech_Spec.md` — Reference template for structure and depth

---

## 2. Overview

### Problem Statement
The Conscious Visual Engine supports multiple visual styles — cinematic color-graded, semi-realistic digital, Ghibli illustration, and real photography. Each style carries a distinct psychological contract with the audience: cinematic realism signals authenticity and authority; Ghibli illustration signals identity play and tribal belonging; real photography signals documentary truth. When styles are applied to incorrect formats, the psychological contract is violated. A Ghibli-illustrated carousel destroys the somatic arc tension that requires cinematic continuity across slides. An AI-generated image used for Observational Humor breaks the documentary authenticity that makes the humor land as "real." Without a deterministic style-to-format constraint layer, Abel's recipe protocol selection may produce visually coherent but psychologically incoherent compositions — the colors look right, but the audience's unconscious processing rejects the visual as incongruent with the content's emotional intent.

### Solution
FR-VIS-08 extends the `visual-format-constraint-adapter` with a style scoping enforcement layer. After format and aspect ratio constraints are locked (FR-VIS-07), the style scoping layer evaluates the `content_format` against a deterministic `Style_Scope_Matrix` and emits a `style_constraint_directive` that specifies which visual styles are permitted, prohibited, and mandatory for the given format. This directive fires before Abel's recipe protocol selection, preventing invalid style assignments at the earliest possible pipeline stage. The matrix is not a suggestion layer — it is a hard architectural boundary. If Abel attempts to assign a style outside the directive's `permitted_styles` array, the VCB is rejected before it reaches Gate C-09.

### Scope
**In scope:**
- The `Style_Scope_Matrix` mapping every content format to its permitted, prohibited, and mandatory visual styles.
- The style constraint injection logic within the `visual-format-constraint-adapter`.
- Pre-Abel validation rejecting VCBs with invalid style assignments.
- Saturation ceiling enforcement for Worst Case Scenario format.

**Out of scope:**
- Aspect ratio and pixel dimension enforcement (handled by FR-VIS-07).
- Image sourcing tier selection (handled by FR-VIS-09).
- Gate V-00 image type validation (handled by FR-VIS-13).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-VIS-002` | Visual Recipe Protocol Library | DOWNSTREAM CONSUMER — Recipe selection must occur within the style directive's `permitted_styles` boundary. |
| `DEP-VIS-005` | Visual Composition Brief Schema | DOWNSTREAM CONSUMER — VCB `visual_style` field must match the style directive. |
| `DEP-ENG-011` | Finalized Content Output | INPUT — Provides the `content_format` designation. |
| `DEP-ENG-041` | Receipt Chain Guard | AUDIT — Style directive hash is sealed and tracked. |
| `FR-VIS-07` | Format & Aspect Ratio Enforcement | UPSTREAM DEPENDENCY — Format must be locked before style scoping can evaluate format-style intersection. |
| `visual-format-constraint-adapter` | Format Constraint Adapter | TOOL — Extended with style scoping logic. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Applied |
|---|---|---|---|
| **Visual Style Psychology in Coaching** | CCP Research Lab | 2026 | The Style-Function Matrix establishes that visual style is not an aesthetic preference but a psychological contract. Cinematic realism activates the "documentary processing" neural pathway — audiences evaluate cinematic images as evidence rather than decoration. Ghibli/illustrated styles activate the "transportation" pathway — audiences process illustrated images as identity narratives rather than factual claims. Applying the wrong style to the wrong format creates a processing conflict: the audience's prefrontal cortex expects evidence (because the content format is a carousel teaching a concept) but receives illustration (which triggers narrative transportation), and the resulting cognitive dissonance reduces engagement by 23-31% (measured via dwell time degradation). |
| **Tribal Imageability and Cultural Half-Life** | CCP Research Lab | 2026 | Illustrated styles (Ghibli, watercolor, vector) inflate the imageability rating of concrete nouns by 0.8-1.2 TIRS points because illustration removes the noise of photographic complexity, isolating the noun as a symbolic icon. This inflation is beneficial for Conceptual Contrast and Supervisuals (where the goal is symbolic identity recognition) but harmful for carousels (where the goal is somatic arc engagement through realistic tension building). Using illustration in carousels produces an artificially "easy" visual that fails to generate the physiological friction required for desire compounding. |
| **Cinematographic Emotional Grammar Framework** | CCP Research Lab | 2026 | The CGCS coding scheme specifies two fundamentally incompatible grammar systems: (A) Cinematic Grammar — lighting ratios, shadow angles, color temperature, depth of field, bokeh — which produces emotional responses through naturalistic visual processing. (B) Illustrated Grammar — line weight, saturation curves, stylization level, flatness — which produces emotional responses through symbolic recognition. A single composition cannot use both grammar systems simultaneously without creating visual incoherence. The style scoping layer ensures each format is locked to the correct grammar system before any prompt compilation begins. |

### Technical Decisions
1. **Style Scoping Fires After Format Locking:** Style rules depend on knowing the content format. A "single image" could be a Supervisual (Ghibli permitted) or an Observational Humor piece (Ghibli prohibited). The format must be resolved first (FR-VIS-07) before the style matrix can be evaluated.
2. **Mandatory vs. Permitted Distinction:** Some formats have a mandatory style (Observational Humor MUST use real photography). Others have a permitted set (Conceptual Contrast may use cinematic OR Ghibli). The directive differentiates these to prevent Abel from treating "permitted" as "mandatory" and always choosing the first option.
3. **Saturation Ceiling as Style Parameter:** Worst Case Scenario's 20-35% saturation maximum is encoded as a style parameter within the directive, not as a separate PSSL constraint. This ensures the saturation ceiling is checked at the style scoping stage, before Abel assigns PSSL parameters — preventing the situation where Abel assigns 70% saturation to a Worst Case Scenario slide and Gate C-09 catches it only after significant computational work has been wasted.

---

## 4. Implementation Plan

### Stage 1: Style Matrix Evaluation
*Agent:* `visual-format-constraint-adapter` (style scoping extension)
*Inputs:* `content_format` (from locked format_constraint_envelope via FR-VIS-07), `Style_Scope_Matrix` configuration.
*Outputs:* `style_constraint_directive` JSON object.
*Failure Condition:* `content_format` not found in Style_Scope_Matrix (should never occur if FR-VIS-07 validated the format, but defensive check remains).
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Receives the sealed `format_constraint_envelope` from FR-VIS-07.
2. Extracts the `content_format` string.
3. Looks up the format in the `Style_Scope_Matrix` (see §5).
4. Retrieves the `permitted_styles` array, `prohibited_styles` array, `mandatory_style` (or null), and `style_parameters` object for the format.
5. Assembles the `style_constraint_directive`.

### Stage 2: Saturation Ceiling Injection
*Agent:* `visual-format-constraint-adapter` (style scoping extension)
*Inputs:* `style_constraint_directive`, format-specific style parameters from the matrix.
*Outputs:* Directive enriched with `saturation_ceiling_pct` (if applicable) and `style_grammar_system` designation.
*Failure Condition:* Style parameter references a grammar system not supported by the current Paradoxe version; directive logged with `GRAMMAR_SYSTEM_MISMATCH` warning.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. If the format specifies a `saturation_ceiling_pct` (e.g., Worst Case Scenario: 20-35%), this value is embedded in the directive as a hard constraint.
2. The `style_grammar_system` field is set based on the permitted styles:
   - If only cinematic/semi-realistic styles are permitted: `grammar_system: "cinematic"`.
   - If Ghibli/illustrated styles are permitted: `grammar_system: "illustrated"` (or `"hybrid"` if both cinematic and illustrated are in the permitted set).
   - If only real photography is mandatory: `grammar_system: "documentary"` — no prompt compilation occurs for this format; images are sourced, not generated.
3. The directive is sealed with a SHA-256 hash and written to the Receipt Chain Guard.

### Stage 3: Pre-Abel Style Validation Gate
*Agent:* `visual-format-constraint-adapter` (style scoping extension)
*Inputs:* Abel's preliminary VCB draft (specifically the `visual_style` field assignment).
*Outputs:* `STYLE_VALID` (continue) or `STYLE_VIOLATION` (reject VCB back to Abel with the specific constraint that was violated).
*Failure Condition:* Abel assigns a prohibited style; VCB is rejected with a structured error specifying the prohibited style, the format, and the permitted alternatives.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. After Abel completes the VCB draft, the adapter intercepts the `visual_style` field before Gate C-09.
2. Compares `visual_style` against the `permitted_styles` array in the directive.
3. If `mandatory_style` is set and `visual_style` does not match: reject with `STYLE_VIOLATION — mandatory style is '{mandatory_style}', received '{visual_style}'`.
4. If `visual_style` is in the `prohibited_styles` array: reject with `STYLE_VIOLATION — style '{visual_style}' is prohibited for format '{content_format}'. Permitted: {permitted_styles}`.
5. If the format specifies `saturation_ceiling_pct` and Abel's PSSL parameters include `saturation_pct` above the ceiling: reject with `SATURATION_VIOLATION — maximum {ceiling}%, received {actual}%`.
6. If all checks pass: emit `STYLE_VALID` and forward the VCB to Gate C-09.

---

## 5. Primary Output Schema

### Schema Name: `Style_Scope_Matrix`

```json
{
  "carousel_dopamine_cliff": {
    "permitted_styles": ["cinematic_color_graded", "semi_realistic_digital"],
    "prohibited_styles": ["ghibli_illustration", "watercolor", "vector_flat", "real_photography_only"],
    "mandatory_style": null,
    "style_parameters": { "saturation_ceiling_pct": null, "grammar_system": "cinematic" }
  },
  "carousel_listicle": {
    "permitted_styles": ["cinematic_color_graded", "semi_realistic_digital"],
    "prohibited_styles": ["ghibli_illustration", "watercolor", "vector_flat", "real_photography_only"],
    "mandatory_style": null,
    "style_parameters": { "saturation_ceiling_pct": null, "grammar_system": "cinematic" }
  },
  "carousel_timeline": {
    "permitted_styles": ["cinematic_color_graded", "semi_realistic_digital"],
    "prohibited_styles": ["ghibli_illustration", "watercolor", "vector_flat", "real_photography_only"],
    "mandatory_style": null,
    "style_parameters": { "saturation_ceiling_pct": null, "grammar_system": "cinematic" }
  },
  "carousel_comparison": {
    "permitted_styles": ["cinematic_color_graded", "semi_realistic_digital"],
    "prohibited_styles": ["ghibli_illustration", "watercolor", "vector_flat", "real_photography_only"],
    "mandatory_style": null,
    "style_parameters": { "saturation_ceiling_pct": null, "grammar_system": "cinematic" }
  },
  "single_observational_humor": {
    "permitted_styles": ["real_photography_only"],
    "prohibited_styles": ["ghibli_illustration", "watercolor", "vector_flat", "cinematic_color_graded", "semi_realistic_digital"],
    "mandatory_style": "real_photography_only",
    "style_parameters": { "saturation_ceiling_pct": null, "grammar_system": "documentary" }
  },
  "single_observational_humor_square": {
    "permitted_styles": ["real_photography_only"],
    "prohibited_styles": ["ghibli_illustration", "watercolor", "vector_flat", "cinematic_color_graded", "semi_realistic_digital"],
    "mandatory_style": "real_photography_only",
    "style_parameters": { "saturation_ceiling_pct": null, "grammar_system": "documentary" }
  },
  "single_worst_case": {
    "permitted_styles": ["cinematic_color_graded"],
    "prohibited_styles": ["ghibli_illustration", "watercolor", "vector_flat", "real_photography_only", "semi_realistic_digital"],
    "mandatory_style": "cinematic_color_graded",
    "style_parameters": { "saturation_ceiling_pct": 35, "saturation_floor_pct": 20, "grammar_system": "cinematic" }
  },
  "single_conceptual_contrast": {
    "permitted_styles": ["cinematic_color_graded", "semi_realistic_digital", "ghibli_illustration"],
    "prohibited_styles": ["watercolor", "vector_flat", "real_photography_only"],
    "mandatory_style": null,
    "style_parameters": { "saturation_ceiling_pct": null, "grammar_system": "hybrid" }
  },
  "single_conceptual_contrast_simultaneous": {
    "permitted_styles": ["cinematic_color_graded", "semi_realistic_digital", "ghibli_illustration"],
    "prohibited_styles": ["watercolor", "vector_flat", "real_photography_only"],
    "mandatory_style": null,
    "style_parameters": { "saturation_ceiling_pct": null, "grammar_system": "hybrid" }
  },
  "single_supervisual": {
    "permitted_styles": ["cinematic_color_graded", "semi_realistic_digital", "ghibli_illustration"],
    "prohibited_styles": ["watercolor", "vector_flat", "real_photography_only"],
    "mandatory_style": null,
    "style_parameters": { "saturation_ceiling_pct": null, "grammar_system": "hybrid" }
  },
  "poll_archetypical": {
    "permitted_styles": ["semi_realistic_digital", "vector_flat"],
    "prohibited_styles": ["ghibli_illustration", "real_photography_only", "cinematic_color_graded"],
    "mandatory_style": null,
    "style_parameters": { "saturation_ceiling_pct": null, "grammar_system": "cinematic" }
  },
  "poll_stereotypical": {
    "permitted_styles": ["semi_realistic_digital", "vector_flat"],
    "prohibited_styles": ["ghibli_illustration", "real_photography_only", "cinematic_color_graded"],
    "mandatory_style": null,
    "style_parameters": { "saturation_ceiling_pct": null, "grammar_system": "cinematic" }
  },
  "poll_controversial_dilemma": {
    "permitted_styles": ["semi_realistic_digital", "vector_flat"],
    "prohibited_styles": ["ghibli_illustration", "real_photography_only", "cinematic_color_graded"],
    "mandatory_style": null,
    "style_parameters": { "saturation_ceiling_pct": null, "grammar_system": "cinematic" }
  },
  "single_tweet_quote": {
    "permitted_styles": ["cinematic_color_graded", "semi_realistic_digital"],
    "prohibited_styles": ["ghibli_illustration", "real_photography_only", "watercolor", "vector_flat"],
    "mandatory_style": null,
    "style_parameters": { "saturation_ceiling_pct": null, "grammar_system": "cinematic" }
  },
  "nine_grid_accumulation": {
    "permitted_styles": ["cinematic_color_graded", "semi_realistic_digital"],
    "prohibited_styles": ["ghibli_illustration", "watercolor", "vector_flat", "real_photography_only"],
    "mandatory_style": null,
    "style_parameters": { "saturation_ceiling_pct": null, "grammar_system": "cinematic" }
  }
}
```

### Schema Name: `Style_Constraint_Directive.json`

```json
{
  "directive_id": "SCD-JP-20260318-001",
  "content_output_id": "CO-JP-20260318-012-CAROUSEL",
  "content_format": "carousel_dopamine_cliff",
  "permitted_styles": ["cinematic_color_graded", "semi_realistic_digital"],
  "prohibited_styles": ["ghibli_illustration", "watercolor", "vector_flat", "real_photography_only"],
  "mandatory_style": null,
  "saturation_ceiling_pct": null,
  "saturation_floor_pct": null,
  "grammar_system": "cinematic",
  "format_constraint_envelope_id": "FCE-JP-20260318-001",
  "seal_hash": "b7e2d4c9f1a5b8e3d6c0f2a4b7e1d3c6f0a5b8e2d4c7f1a3b6e0d2c5f8a1b4",
  "receipt_chain_block": "RCB-VIS08-20260318-001",
  "timestamp_utc": "2026-03-18T01:33:25Z"
}
```

---

## 6. Backward Compatibility Fallback

If an older pipeline version does not produce a `content_format` that maps to the Style_Scope_Matrix (e.g., a legacy format string like `"carousel"` without the subtype), the adapter applies a conservative default:
1. **For any unresolved carousel format:** Applies the most restrictive carousel constraint set — `permitted_styles: ["cinematic_color_graded", "semi_realistic_digital"]`, all illustrated styles prohibited.
2. **For any unresolved single image format:** Applies `permitted_styles: ["cinematic_color_graded", "semi_realistic_digital"]` — excludes Ghibli to prevent accidental illustrated output.
3. A `LEGACY_STYLE_DEFAULT` warning is logged with the unresolved format string and the conservative default applied.
4. The conservative default never includes `real_photography_only` or `ghibli_illustration` — these require explicit format resolution to apply.

---

## 7. Tasks

- [ ] **Task 1:** Create the `Style_Scope_Matrix` as a versioned JSON configuration file at `config/visual_pipeline/style_scope_matrix.json`. Populate all 15 format entries with `permitted_styles`, `prohibited_styles`, `mandatory_style`, and `style_parameters` per the PRD specification and CVE documentation.
- [ ] **Task 2:** Extend `visual_format_constraint_adapter.py` with the style scoping evaluation logic. The style scoping stage fires immediately after format locking (Stage 2 of FR-VIS-07), reading the locked format from the envelope and evaluating the style matrix.
- [ ] **Task 3:** Implement the saturation ceiling/floor injection for Worst Case Scenario format — embed `saturation_ceiling_pct: 35` and `saturation_floor_pct: 20` in the directive, ensuring these values are enforced before PSSL parameter assignment.
- [ ] **Task 4:** Implement the `grammar_system` designation logic — map each permitted style set to the correct grammar system (`cinematic`, `illustrated`, `documentary`, or `hybrid`). Paradoxe uses this to select the correct prompt compilation template.
- [ ] **Task 5:** Write the Pre-Abel Style Validation Gate — intercept Abel's preliminary VCB draft and validate the `visual_style` field against the sealed directive before forwarding to Gate C-09.
- [ ] **Task 6:** Add `STYLE_VIOLATION`, `SATURATION_VIOLATION`, and `GRAMMAR_SYSTEM_MISMATCH` error types to the pipeline's error taxonomy with structured payloads including the violated constraint, the assigned value, and the permitted alternatives.
- [ ] **Task 7:** Implement the legacy conservative default fallback for unresolved format subtypes.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Carousel Ghibli Prohibition):** Submit `content_format: carousel_dopamine_cliff`. Have Abel attempt to assign `visual_style: ghibli_illustration` to the VCB. Assert the Pre-Abel Style Validation Gate rejects with `STYLE_VIOLATION — style 'ghibli_illustration' is prohibited for format 'carousel_dopamine_cliff'. Permitted: ['cinematic_color_graded', 'semi_realistic_digital']`. *Failure Example:* Abel's VCB passes through with Ghibli style, Paradoxe compiles an illustrated prompt, and the resulting carousel has flat, stylized characters that break the somatic arc's tension-building function.
- [ ] **AC2 (Observational Humor Real-Only Mandate):** Submit `content_format: single_observational_humor`. Assert the directive contains `mandatory_style: "real_photography_only"` and `grammar_system: "documentary"`. Have Abel attempt to assign `visual_style: semi_realistic_digital`. Assert rejection with `STYLE_VIOLATION — mandatory style is 'real_photography_only', received 'semi_realistic_digital'`. *Failure Example:* An AI-generated semi-realistic image is used for an Observational Humor post, and the audience immediately recognizes it as synthetic, destroying the documentary authenticity that makes the humor land.
- [ ] **AC3 (Worst Case Saturation Ceiling):** Submit `content_format: single_worst_case`. Have Abel assign `saturation_pct: 55` in the PSSL parameters. Assert rejection with `SATURATION_VIOLATION — maximum 35%, received 55%`. Then submit `saturation_pct: 28`. Assert acceptance. *Failure Example:* A Worst Case Scenario image is generated with vivid, saturated colors, undermining the desaturated cinematic dread that the format requires.
- [ ] **AC4 (Conceptual Contrast Ghibli Permission):** Submit `content_format: single_conceptual_contrast`. Have Abel assign `visual_style: ghibli_illustration`. Assert the directive permits this style and the VCB passes validation. *Failure Example:* The style scoping layer incorrectly prohibits Ghibli for Conceptual Contrast because a developer hardcoded "Ghibli is always prohibited."
- [ ] **AC5 (Grammar System Routing):** Submit three formats: `single_observational_humor`, `carousel_dopamine_cliff`, `single_supervisual`. Assert the directives emit `grammar_system: "documentary"`, `grammar_system: "cinematic"`, and `grammar_system: "hybrid"` respectively. *Failure Example:* All three emit "cinematic", causing Paradoxe to compile naturalistic prompts for an Observational Humor piece that should use zero AI generation.
- [ ] **AC6 (Poll Style Constraint):** Submit `content_format: poll_archetypical`. Assert `permitted_styles` includes `semi_realistic_digital` and `vector_flat` but excludes `real_photography_only` and `ghibli_illustration`. *Failure Example:* A photographic image is used in a poll option zone, creating a visual weight imbalance that biases user votes toward the photographed option.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR-VIS-07 (Format & Aspect Ratio Enforcement) | Internal | UPSTREAM — Format must be locked before style rules can be evaluated. |
| DEP-VIS-002 (Visual Recipe Protocol Library) | Internal | Downstream — Recipe selection is constrained to styles within the directive's `permitted_styles`. |
| DEP-ENG-011 (Finalized Content Output) | Internal | Upstream — Source of `content_format` designation. |
| DEP-ENG-041 (Receipt Chain Guard) | Internal | Audit — Style directive hash is sealed and tracked. |
| FR-VIS-01 (VCB Generation) | Internal | Downstream — Abel's `visual_style` assignment must pass the Pre-Abel Style Validation Gate. |
| FR-VIS-03 (PSSL Prompt Compilation) | Internal | Downstream — Paradoxe uses `grammar_system` to select the correct prompt template. |
| FR-VIS-09 (Image Sourcing Hierarchy) | Internal | Downstream — `real_photography_only` mandate routes Aurore to Tier 1-2 only; `ghibli_illustration` routes to Tier 4. |
| FR-VIS-13 (Image Type Validity Gate) | Internal | Downstream — Gate V-00 cross-validates image types against the style directive. |

---

## 10. Testing Strategy

### Unit Tests
- **Matrix Completeness:** Load `style_scope_matrix.json` and assert all 15 format entries contain non-null `permitted_styles` (array with ≥1 entry), `prohibited_styles` (array), `mandatory_style` (string or null), and `style_parameters` (object with `grammar_system`).
- **Mutual Exclusivity Check:** For every format entry, assert that no style appears in both `permitted_styles` and `prohibited_styles` simultaneously.
- **Mandatory Consistency Check:** For every format where `mandatory_style` is non-null, assert that `mandatory_style` is present in `permitted_styles` and absent from `prohibited_styles`.
- **Saturation Boundary:** For `single_worst_case`, assert `saturation_ceiling_pct: 35` and `saturation_floor_pct: 20`. Test boundary values: 19% → reject (below floor), 20% → accept, 35% → accept, 36% → reject (above ceiling).

### Integration Tests
- **Full Style Enforcement Pipeline:** Submit a `carousel_comparison` content output. Assert the style directive emits `grammar_system: "cinematic"`. Have Abel draft a VCB with `visual_style: "cinematic_color_graded"`. Assert acceptance. Have Abel redraft with `visual_style: "ghibli_illustration"`. Assert rejection. Validate the rejection logs include the specific constraint violated.
- **Supervisual Ghibli Flow:** Submit `single_supervisual`. Assign `visual_style: "ghibli_illustration"`. Assert the directive permits it, the VCB passes validation, and Paradoxe receives `grammar_system: "hybrid"` (or "illustrated" if only Ghibli is selected).

### Safety Tests (ADR-01 Quarantine Security)
- **Style Injection Resistance:** Inject `visual_style: "ghibli_illustration'; DROP TABLE styles;"` into Abel's VCB draft. Assert the adapter treats the entire string as a single style lookup, fails to match in `permitted_styles`, and emits `STYLE_VIOLATION` without executing any embedded commands.
- **Directive Tampering Detection:** Intercept the sealed `style_constraint_directive` between VIS-08 and Abel. Add `"ghibli_illustration"` to `permitted_styles`. Assert the Receipt Chain Guard detects the hash mismatch and halts with `DIRECTIVE_TAMPERING_DETECTED`.
