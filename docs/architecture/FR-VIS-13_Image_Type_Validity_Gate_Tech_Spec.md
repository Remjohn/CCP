# Tech-Spec: FR-VIS-13 — Image Type Validity Gate (Gate V-00)

**Created:** 2026-03-18
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §Visual Intelligence Pipeline, CVE_Documentation_V3 §9
**Skill Implementation:** `skills/visuals/gate_v00_image_type_validator.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md` — FR-VIS-13 definition (line 1040)
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CVE_Documentation_V3.md` — §9 Validation Gate Updates, full gate sequence V-00 through V-05
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CVE_Documentation_V2.md` — §8.3 Aspect Ratio & Format Specifications, §9.5 AGSS Scoring, §10.2 Character Drift Detection
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Visual Style Psychology in Coaching.md` — Style-Function Matrix, realism vs. stylization validation boundaries
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Cinematographic Emotional Grammar Framework Research.md` — Deterministic constraint validation principles, format-grammar coherence requirements
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Tribal Imageability and Cultural Half-Life.md` — Noun-image type congruence validation
- `d:\Work\The Conscious Coaching Factory\docs\architecture\FR50_Sovereign_Image_Rule_Tech_Spec.md` — Reference template for structure and depth

---

## 2. Overview

### Problem Statement
The Conscious Visual Engine's quality gate sequence (V-01 through V-05) validates visual outputs after image search or generation has already occurred. By the time Gate V-01 checks TIAR decay or Gate V-04 scores AGSS, the pipeline has already invested 10-15 minutes of RunningHub computation or multi-API image search cycles per slide. If the fundamental image type assignment was invalid from the start — a Ghibli illustration assigned to a carousel slide, an AI-generated portrait used for Observational Humor, a photographic image placed in a poll option zone — all downstream processing was wasted. The pipeline must catch image type violations before expensive sourcing and generation operations begin, not after they complete.

### Solution
FR-VIS-13 establishes **Gate V-00 (Image Type Validity)** — a pre-sourcing gate that runs *before* the standard 5-gate visual quality sequence. Gate V-00 takes Abel's completed VCB and cross-validates each slide's assigned `image_type` against the format and style scoping rules defined in FR-VIS-07 (Format & Aspect Ratio Enforcement) and FR-VIS-08 (Style Scoping). If any slide violates the rules, the entire VCB is returned to Abel for revision before Aurore begins image search or Paradoxe begins prompt compilation. This gate is the last checkpoint before the pipeline transitions from the planning phase (VCB assembly) to the production phase (image sourcing and generation). Nothing passes Gate V-00 without a valid image type assignment for every slide.

### Scope
**In scope:**
- Gate V-00 validation logic for all image type-to-format rules.
- Specific rule enforcement: carousel Ghibli prohibition, Observational Humor real-only mandate, named person Tier 1 requirement, poll graphic mandate, 1:1 format availability check.
- VCB rejection routing back to Abel with specific violation details.
- Position in the full gate sequence: V-00 → V-01 → V-02 → V-03 → V-04 → V-05.

**Out of scope:**
- Gates V-01 through V-05 (handled by their respective FR-VIS specs).
- Actual image sourcing or generation (handled by FR-VIS-09, FR-VIS-10, FR-VIS-03).
- The format and style constraint layers themselves (defined in FR-VIS-07 and FR-VIS-08; this gate validates against their outputs).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-VIS-005` | Visual Composition Brief Schema | INPUT — The completed VCB from Abel, containing per-slide `image_type` assignments. |
| `DEP-VIS-006` | Known Persons Registry | REFERENCE — Used to verify that slides referencing named persons have `image_type: "tier_1_real_person"`. |
| `DEP-ENG-041` | Receipt Chain Guard | AUDIT — Gate V-00 pass/fail result and violation details are hashed and recorded. |
| `FR-VIS-07` | Format & Aspect Ratio Enforcement | UPSTREAM — Provides the locked `format_constraint_envelope` (format type, aspect ratio). |
| `FR-VIS-08` | Style Scoping | UPSTREAM — Provides the sealed `style_constraint_directive` (permitted/prohibited styles, grammar system). |
| `FR-VIS-01` | VCB Generation (Abel) | FEEDBACK TARGET — Failed VCBs are returned to Abel with violation details for revision. |
| `FR-VIS-09` | Image Sourcing Hierarchy | DOWNSTREAM — Only begins after Gate V-00 passes. |
| `FR-VIS-03` | PSSL Prompt Compilation | DOWNSTREAM — Only begins after Gate V-00 passes. |

### Full Gate Sequence

| Gate | Name | Stage | Purpose |
|---|---|---|---|
| **V-00** | **Image Type Validity** | **Pre-Sourcing** | **Validates image type assignments against format/style rules before any sourcing or generation** |
| V-01 | TIAR Decay Check | Pre-Sourcing | Validates tribal nouns are not expired |
| V-02 | PSSL Completeness (C-09) | Pre-Sourcing | Validates all PSSL fields are present and numeric |
| V-03 | Accumulation Prohibition Audit | Pre-Sourcing | Validates no completion imagery in accumulation slides |
| V-04 | Visual Validation Post-Generation | Post-Generation | AGSS scoring, authenticity checks, drift detection |
| V-05 | Receipt Chain Confirmation | Post-Generation | Cryptographic integrity of the full receipt chain |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Applied |
|---|---|---|---|
| **Visual Style Psychology in Coaching** | CCP Research Lab | 2026 | The Style-Function Matrix establishes measurable cognitive dissonance when visual styles violate format expectations. Participants exposed to Ghibli-illustrated carousel slides showed a 31% reduction in dwell time compared to cinematic-styled carousels, because the illustration style activated narrative transportation processing while the carousel's sequential format demanded analytical processing. Gate V-00 prevents this dissonance by catching style-format mismatches before production. |
| **Cinematographic Emotional Grammar Framework** | CCP Research Lab | 2026 | The CGCS coding scheme requires format-grammar coherence. A prompt compiled using cinematic grammar (lighting ratios, shadow angles) for an image_type of "ghibli_illustration" produces visual artifacts — realistic lighting on flat-shaded characters creates an uncanny valley effect. Gate V-00 ensures the image_type assignment is congruent with the grammar_system specified by the style directive, preventing downstream prompt compilation from operating on incompatible parameters. |
| **Tribal Imageability and Cultural Half-Life** | CCP Research Lab | 2026 | Named person references require Tier 1 (real person photo) image types to maintain TIRS potency. When a named figure is rendered as AI-generated or illustrated, their tribal imageability score drops by 1.4-2.1 TIRS points because the audience's recognition system detects the synthetic representation and downgrades the figure's authority weight. Gate V-00 enforces the Tier 1 mandate for named person slides. |

### Technical Decisions
1. **Gate V-00 Runs First in the Sequence:** This is the cheapest gate (pure JSON validation, no API calls, no ML inference) but catches the most expensive errors (invalid image types that would waste 10+ minutes of RunningHub processing per slide). Running it first maximizes the cost-savings of the gate sequence.
2. **VCB Rejection, Not Slide-Level Correction:** When Gate V-00 detects a violation, the entire VCB is returned to Abel, not just the offending slide. This is because image type decisions are often correlated across slides in a composition — if Abel assigned Ghibli to slide 3 of a carousel, there may be visual consistency assumptions (shared color palette, matched line weight) baked into slides 1, 2, 4, and 5 that also need revision. Correcting only the offending slide risks visual incoherence.
3. **Maximum 2 Revision Cycles:** If Abel's revised VCB fails Gate V-00 a second time, the composition is escalated to `PENDING_OPERATOR_REVIEW` with the full rejection log. This prevents infinite revision loops where Abel oscillates between invalid assignments because the content fundamentally requires a format change, not a style adjustment.

---

## 4. Implementation Plan

### Stage 1: VCB Image Type Extraction
*Agent:* `gate_v00_image_type_validator.py`
*Inputs:* Completed VCB from Abel (DEP-VIS-005), sealed `format_constraint_envelope` (FR-VIS-07), sealed `style_constraint_directive` (FR-VIS-08).
*Outputs:* Per-slide `image_type` array extracted for validation.
*Failure Condition:* VCB missing `image_type` field on any slide; gate fails with `MISSING_IMAGE_TYPE` and returns VCB to Abel.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Gate V-00 receives the completed VCB from Abel.
2. Extracts the `per_slide_assignments` array from the VCB.
3. For each slide, extracts the `image_type` field. Valid image types are: `tier_1_real_person`, `tier_2_stock_environmental`, `tier_2_stock_contextual`, `tier_2_stock_abstract`, `tier_3_ai_realistic`, `tier_4_ai_ghibli`, `graphic_vector`, `animated_gif`.
4. If any slide is missing the `image_type` field or contains a value not in the valid enum list, the gate immediately fails with `MISSING_IMAGE_TYPE` or `INVALID_IMAGE_TYPE` and returns the VCB to Abel.
5. Also extracts `named_person_reference` (string or null) and `aspect_ratio_template` (string) from each slide for downstream rule checks.

### Stage 2: Format-Image Type Cross-Validation
*Agent:* `gate_v00_image_type_validator.py`
*Inputs:* Per-slide `image_type` array, `format_constraint_envelope` (locked format and aspect ratio).
*Outputs:* Per-slide `format_validation_result` array (PASS/FAIL with violation details).
*Failure Condition:* Any slide fails format-image type validation; gate collects all violations before returning to Abel (does not halt on first failure — collects all violations for batch correction).
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Rules Enforced:**

| Rule ID | Rule | Applies To | Violation Response |
|---|---|---|---|
| `V00-R01` | Carousel slides cannot use `tier_4_ai_ghibli` or any illustrated image type | All carousel formats (`carousel_*`) | `CAROUSEL_GHIBLI_VIOLATION` |
| `V00-R02` | Observational Humor slides must use `tier_1_real_person` or `tier_2_stock_*` — never AI-generated types | `single_observational_humor`, `single_observational_humor_square` | `OBSERVATIONAL_HUMOR_AI_VIOLATION` |
| `V00-R03` | Named person slides (non-null `named_person_reference`) must use `tier_1_real_person` | Any format containing a named person reference | `NAMED_PERSON_TIER_VIOLATION` |
| `V00-R04` | Poll option zone slides must use `graphic_vector` or `tier_3_ai_realistic` — never photographic types | `poll_archetypical`, `poll_stereotypical`, `poll_controversial_dilemma` | `POLL_PHOTOGRAPHIC_VIOLATION` |
| `V00-R05` | 1:1 aspect ratio templates are only available for approved formats | `single_tweet_quote`, `single_supervisual`, `single_conceptual_contrast_simultaneous`, `single_observational_humor_square` | `ASPECT_RATIO_FORMAT_VIOLATION` |

**Steps:**
1. For each slide, checks the `image_type` against the `content_format` from the format envelope.
2. Applies all applicable rules from the table above.
3. Collects all violations into a `violations` array — does not halt on first failure.
4. If `violations` array is empty, format validation passes.
5. If `violations` array is non-empty, proceeds to Stage 3 (Style Cross-Validation) to collect any additional violations before returning the complete violation report to Abel.

### Stage 3: Style-Image Type Cross-Validation
*Agent:* `gate_v00_image_type_validator.py`
*Inputs:* Per-slide `image_type` array, `style_constraint_directive` (permitted/prohibited styles, grammar_system).
*Outputs:* Per-slide `style_validation_result` array (PASS/FAIL with violation details).
*Failure Condition:* Image type implies a style that is prohibited by the style directive.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Image Type → Implied Style Mapping:**

| Image Type | Implied Style |
|---|---|
| `tier_1_real_person` | `real_photography_only` |
| `tier_2_stock_environmental` | `real_photography_only` |
| `tier_2_stock_contextual` | `real_photography_only` |
| `tier_2_stock_abstract` | `real_photography_only` OR `graphic_vector` |
| `tier_3_ai_realistic` | `semi_realistic_digital` OR `cinematic_color_graded` |
| `tier_4_ai_ghibli` | `ghibli_illustration` |
| `graphic_vector` | `vector_flat` |
| `animated_gif` | `animated` (validated separately) |

**Steps:**
1. For each slide, maps the `image_type` to its implied visual style(s).
2. Checks the implied style(s) against the `permitted_styles` and `prohibited_styles` from the style directive.
3. If the implied style is in `prohibited_styles`, adds a `STYLE_IMAGE_TYPE_CONFLICT` violation specifying the slide index, the assigned `image_type`, the implied style, and the prohibited constraint.
4. If `mandatory_style` is set and the implied style does not match, adds a `MANDATORY_STYLE_CONFLICT` violation.
5. Merges style violations with format violations from Stage 2 into a unified `violations` array.

### Stage 4: Gate V-00 Verdict
*Agent:* `gate_v00_image_type_validator.py`
*Inputs:* Unified `violations` array from Stages 2 and 3, `revision_count` (number of times this VCB has been returned to Abel).
*Outputs:* `GATE_V00_PASS` (forward VCB to V-01) or `GATE_V00_FAIL` (return VCB to Abel with violation report) or `GATE_V00_ESCALATE` (forward to operator review).
*Failure Condition:* Second revision failure triggers escalation.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. If `violations` array is empty: emit `GATE_V00_PASS` and forward the VCB to Gate V-01 (TIAR Decay Check).
2. If `violations` array is non-empty and `revision_count < 2`:
   - Emit `GATE_V00_FAIL`.
   - Assemble a structured `violation_report` containing: `content_output_id`, `revision_count`, array of violations (each with `rule_id`, `slide_index`, `assigned_image_type`, `violation_type`, `explanation`, `suggested_correction`).
   - Return the VCB and violation report to Abel for revision.
   - Increment `revision_count`.
3. If `violations` array is non-empty and `revision_count >= 2`:
   - Emit `GATE_V00_ESCALATE`.
   - Flag the composition as `PENDING_OPERATOR_REVIEW` with the full violation history (both revision attempts and their violations).
   - Operator receives a structured notification with the composition ID, the violations, and Abel's revision attempts.
   - Pipeline does not proceed until operator manually resolves or overrides.

---

## 5. Primary Output Schema

### Schema Name: `Gate_V00_Result.json`

```json
{
  "gate_id": "V00-JP-20260318-001",
  "content_output_id": "CO-JP-20260318-012-CAROUSEL",
  "content_format": "carousel_dopamine_cliff",
  "verdict": "GATE_V00_PASS",
  "revision_count": 0,
  "violations": [],
  "slide_validation_summary": [
    { "slide_index": 0, "image_type": "tier_3_ai_realistic", "format_check": "PASS", "style_check": "PASS" },
    { "slide_index": 1, "image_type": "tier_2_stock_environmental", "format_check": "PASS", "style_check": "PASS" },
    { "slide_index": 2, "image_type": "tier_3_ai_realistic", "format_check": "PASS", "style_check": "PASS" },
    { "slide_index": 3, "image_type": "tier_2_stock_contextual", "format_check": "PASS", "style_check": "PASS" },
    { "slide_index": 4, "image_type": "tier_3_ai_realistic", "format_check": "PASS", "style_check": "PASS" },
    { "slide_index": 5, "image_type": "tier_2_stock_abstract", "format_check": "PASS", "style_check": "PASS" },
    { "slide_index": 6, "image_type": "tier_3_ai_realistic", "format_check": "PASS", "style_check": "PASS" }
  ],
  "format_envelope_id": "FCE-JP-20260318-001",
  "style_directive_id": "SCD-JP-20260318-001",
  "receipt_chain_block": "RCB-V00-20260318-001",
  "timestamp_utc": "2026-03-18T01:34:00Z"
}
```

### Schema Name: `Gate_V00_Violation_Report.json` (on failure)

```json
{
  "gate_id": "V00-JP-20260318-002",
  "content_output_id": "CO-JP-20260318-015-CAROUSEL",
  "content_format": "carousel_dopamine_cliff",
  "verdict": "GATE_V00_FAIL",
  "revision_count": 1,
  "violations": [
    {
      "rule_id": "V00-R01",
      "slide_index": 3,
      "assigned_image_type": "tier_4_ai_ghibli",
      "violation_type": "CAROUSEL_GHIBLI_VIOLATION",
      "explanation": "Carousel slides cannot use Ghibli/illustrated image types. Slide 3 was assigned 'tier_4_ai_ghibli' but carousels require cinematic or semi-realistic styles only.",
      "suggested_correction": "Change image_type to 'tier_3_ai_realistic' or 'tier_2_stock_contextual'"
    },
    {
      "rule_id": "V00-R03",
      "slide_index": 5,
      "assigned_image_type": "tier_3_ai_realistic",
      "violation_type": "NAMED_PERSON_TIER_VIOLATION",
      "explanation": "Slide 5 references named person 'Tony Robbins' but uses 'tier_3_ai_realistic'. Named person slides must use 'tier_1_real_person' to source licensed real photographs.",
      "suggested_correction": "Change image_type to 'tier_1_real_person'"
    }
  ],
  "slide_validation_summary": [
    { "slide_index": 0, "image_type": "tier_3_ai_realistic", "format_check": "PASS", "style_check": "PASS" },
    { "slide_index": 1, "image_type": "tier_2_stock_environmental", "format_check": "PASS", "style_check": "PASS" },
    { "slide_index": 2, "image_type": "tier_3_ai_realistic", "format_check": "PASS", "style_check": "PASS" },
    { "slide_index": 3, "image_type": "tier_4_ai_ghibli", "format_check": "FAIL", "style_check": "FAIL" },
    { "slide_index": 4, "image_type": "tier_3_ai_realistic", "format_check": "PASS", "style_check": "PASS" },
    { "slide_index": 5, "image_type": "tier_3_ai_realistic", "format_check": "PASS", "style_check": "FAIL" },
    { "slide_index": 6, "image_type": "tier_3_ai_realistic", "format_check": "PASS", "style_check": "PASS" }
  ],
  "format_envelope_id": "FCE-JP-20260318-002",
  "style_directive_id": "SCD-JP-20260318-002",
  "receipt_chain_block": "RCB-V00-20260318-002",
  "timestamp_utc": "2026-03-18T01:34:15Z"
}
```

---

## 6. Backward Compatibility Fallback

If Abel's VCB was generated by an older pipeline version that does not include per-slide `image_type` fields:
1. Gate V-00 detects the missing `image_type` fields.
2. The gate does NOT attempt to infer image types from other VCB fields (recipe_id, visual_style, etc.). Inference introduces ambiguity that could result in invalid sourcing.
3. Instead, the gate returns the VCB to Abel with a `LEGACY_VCB_UPGRADE_REQUIRED` status, instructing Abel to reprocess the VCB with the current schema that includes mandatory `image_type` assignment per slide.
4. If Abel is also running an older version that cannot assign `image_type`, the composition is escalated to `PENDING_OPERATOR_REVIEW` with a clear message: "VCB schema version does not support image type validation. Manual image type assignment required."

---

## 7. Tasks

- [ ] **Task 1:** Write `gate_v00_image_type_validator.py` implementing the 5-rule validation engine (V00-R01 through V00-R05) with per-slide violation collection.
- [ ] **Task 2:** Implement the Image Type → Implied Style mapping table and the style cross-validation logic that checks implied styles against the sealed style directive from FR-VIS-08.
- [ ] **Task 3:** Build the structured `Gate_V00_Violation_Report` assembly logic, including `suggested_correction` generation for each rule violation type.
- [ ] **Task 4:** Implement the 2-revision-cycle escalation mechanism — track `revision_count` per VCB, escalate to `PENDING_OPERATOR_REVIEW` on the third failure, and assemble the full violation history for operator review.
- [ ] **Task 5:** Integrate Gate V-00 into the gate sequence as the first gate — ensure it fires before V-01 (TIAR Decay) and that a V-00 failure halts the entire downstream sequence.
- [ ] **Task 6:** Write the Abel feedback interface — the structured violation report format that Abel parses to understand which slides failed, which rules were violated, and what corrective actions are suggested.
- [ ] **Task 7:** Implement Receipt Chain Guard integration — hash the Gate V-00 result (pass or fail) and write to DEP-ENG-041 at every stage.
- [ ] **Task 8:** Add `CAROUSEL_GHIBLI_VIOLATION`, `OBSERVATIONAL_HUMOR_AI_VIOLATION`, `NAMED_PERSON_TIER_VIOLATION`, `POLL_PHOTOGRAPHIC_VIOLATION`, `ASPECT_RATIO_FORMAT_VIOLATION`, `STYLE_IMAGE_TYPE_CONFLICT`, `MANDATORY_STYLE_CONFLICT`, `MISSING_IMAGE_TYPE`, `INVALID_IMAGE_TYPE`, and `LEGACY_VCB_UPGRADE_REQUIRED` error types to the pipeline's error taxonomy.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Carousel Ghibli Block):** Create a VCB for `carousel_dopamine_cliff` with 7 slides. Assign `image_type: "tier_4_ai_ghibli"` to slide 3. Assert Gate V-00 fails with `CAROUSEL_GHIBLI_VIOLATION` on slide 3 and all other slides pass. Assert the violation report includes `suggested_correction: "Change image_type to 'tier_3_ai_realistic' or 'tier_2_stock_contextual'"`. *Failure Example:* Gate V-00 passes the VCB, Paradoxe compiles a Ghibli prompt for slide 3, RunningHub generates a Ghibli illustration, and the resulting carousel has 6 cinematic slides and 1 illustrated slide — visually jarring and psychologically incoherent.
- [ ] **AC2 (Observational Humor AI Block):** Create a VCB for `single_observational_humor` with `image_type: "tier_3_ai_realistic"`. Assert Gate V-00 fails with `OBSERVATIONAL_HUMOR_AI_VIOLATION`. Change to `image_type: "tier_2_stock_contextual"`. Assert Gate V-00 passes. *Failure Example:* An AI-generated "candid" photo is used for Observational Humor, and the audience immediately detects the synthetic quality, commenting "this looks AI" and destroying the post's engagement.
- [ ] **AC3 (Named Person Tier 1 Mandate):** Create a VCB with `named_person_reference: "Brené Brown"` on slide 2 and `image_type: "tier_3_ai_realistic"`. Assert Gate V-00 fails with `NAMED_PERSON_TIER_VIOLATION` and `suggested_correction: "Change image_type to 'tier_1_real_person'"`. *Failure Example:* RunningHub generates a semi-realistic AI image of someone vaguely resembling Brené Brown, and the coach publishes it — creating a legal liability and reputational risk.
- [ ] **AC4 (Poll Zone Photographic Block):** Create a VCB for `poll_archetypical` with option zone slides using `image_type: "tier_1_real_person"`. Assert Gate V-00 fails with `POLL_PHOTOGRAPHIC_VIOLATION`. Change to `image_type: "graphic_vector"`. Assert pass. *Failure Example:* Two photographic portraits are used in a poll's option zones, and the visual weight of one photo's composition (better lighting, more attractive subject) biases votes toward that option, undermining the poll's engagement function.
- [ ] **AC5 (Multi-Violation Collection):** Create a VCB with 3 simultaneous violations: slide 1 has a Ghibli carousel violation, slide 4 has a named person tier violation, slide 6 has a style conflict. Assert Gate V-00 returns all 3 violations in a single report, not halting after the first. *Failure Example:* Gate V-00 reports only the first violation, Abel fixes slide 1, resubmits, and Gate V-00 then reports slide 4 — requiring 3 revision cycles instead of 1.
- [ ] **AC6 (Escalation After 2 Failures):** Submit a VCB that fails Gate V-00. Abel revises and resubmits. The revised VCB also fails. Assert the second failure emits `GATE_V00_ESCALATE` with `PENDING_OPERATOR_REVIEW` status and the full violation history. *Failure Example:* Abel enters an infinite revision loop, repeatedly failing Gate V-00, and the pipeline is stuck in a cycle with no human oversight.
- [ ] **AC7 (Clean Pass):** Create a VCB for `carousel_dopamine_cliff` with all slides using `tier_3_ai_realistic` or `tier_2_stock_*` types, no named person references. Assert Gate V-00 emits `GATE_V00_PASS` and the VCB is forwarded to Gate V-01. *Failure Example:* Gate V-00 throws an exception on a valid VCB because the validator crashes on null `named_person_reference` fields.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR-VIS-07 (Format & Aspect Ratio Enforcement) | Internal | UPSTREAM — Provides the locked format_constraint_envelope used for format-image type cross-validation. |
| FR-VIS-08 (Style Scoping) | Internal | UPSTREAM — Provides the sealed style_constraint_directive used for style-image type cross-validation. |
| FR-VIS-01 (VCB Generation) | Internal | FEEDBACK TARGET — Failed VCBs are returned to Abel with violation details. |
| DEP-VIS-005 (VCB Schema) | Internal | INPUT — The completed VCB containing per-slide `image_type` assignments. |
| DEP-VIS-006 (Known Persons Registry) | Internal | REFERENCE — Determines whether a slide references a named person requiring Tier 1 sourcing. |
| DEP-ENG-041 (Receipt Chain Guard) | Internal | AUDIT — Gate V-00 results are hashed and recorded. |
| Gate V-01 (TIAR Decay Check) | Internal | DOWNSTREAM — Only fires after Gate V-00 passes. |
| Gate V-02 (PSSL Completeness / C-09) | Internal | DOWNSTREAM — Only fires after V-00 and V-01 pass. |
| FR-VIS-09 (Image Sourcing Hierarchy) | Internal | DOWNSTREAM — Aurore only begins sourcing after Gate V-00 confirms all image types are valid. |

---

## 10. Testing Strategy

### Unit Tests
- **Rule V00-R01 (Carousel Ghibli):** Provide a mock VCB with `content_format: "carousel_listicle"` and one slide with `image_type: "tier_4_ai_ghibli"`. Assert the validator returns `CAROUSEL_GHIBLI_VIOLATION` for that slide.
- **Rule V00-R02 (Observational Humor AI):** Provide a mock VCB with `content_format: "single_observational_humor"` and `image_type: "tier_3_ai_realistic"`. Assert `OBSERVATIONAL_HUMOR_AI_VIOLATION`. Change to `"tier_2_stock_contextual"`. Assert PASS.
- **Rule V00-R03 (Named Person):** Provide a slide with `named_person_reference: "Simon Sinek"` and `image_type: "tier_3_ai_realistic"`. Assert `NAMED_PERSON_TIER_VIOLATION`. Change to `"tier_1_real_person"`. Assert PASS.
- **Rule V00-R04 (Poll Photographic):** Provide `content_format: "poll_stereotypical"` with `image_type: "tier_1_real_person"`. Assert `POLL_PHOTOGRAPHIC_VIOLATION`. Change to `"graphic_vector"`. Assert PASS.
- **Violation Collection:** Provide a VCB with 5 slides, 3 containing violations on different rules. Assert the validator returns all 3 violations in a single pass, not halting after the first.

### Integration Tests
- **Full Gate Sequence Flow:** Submit a valid VCB through Gate V-00. Assert `GATE_V00_PASS`. Verify the VCB is forwarded to Gate V-01 and the Receipt Chain contains the V-00 pass hash.
- **Revision Cycle Test:** Submit an invalid VCB. Assert V-00 fails and returns to Abel. Submit a revised VCB from Abel. Assert V-00 re-evaluates. If the revision passes, verify V-01 receives it. If the revision fails, verify `revision_count` incremented.
- **Escalation Test:** Submit a VCB that fails V-00 twice. Assert `GATE_V00_ESCALATE` is emitted, `PENDING_OPERATOR_REVIEW` status is set, and the operator notification contains the full violation history from both revision attempts.

### Safety Tests (ADR-01 Quarantine Security)
- **Image Type Injection:** Inject `image_type: "tier_3_ai_realistic; SELECT * FROM users"` into a VCB slide. Assert the validator treats it as an `INVALID_IMAGE_TYPE` (not in the valid enum), rejects the slide, and does not execute any embedded commands.
- **Gate Bypass Attempt:** Attempt to submit a VCB directly to Gate V-01 without passing through Gate V-00. Assert the pipeline detects the missing V-00 receipt chain block and rejects the VCB with `GATE_SEQUENCE_VIOLATION`.
