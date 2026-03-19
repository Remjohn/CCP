# Tech-Spec: FR-VIS-01 — Visual Composition Brief Generation

**Created:** 2026-03-18
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §Visual Intelligence Pipeline, CVE_Documentation_V2 §3, §10.4, CVE_Documentation_V3 §3
**Skill Implementation:** `skills/visuals/abel_vcb_generator.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md` — FR-VIS-01 definition (line 1016)
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CVE_Documentation_V2.md` — §3 Abel's VCB Generation Architecture, §10.4 Gate C-09 PSSL Completeness Check, §8.3 Aspect Ratio Specifications
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CVE_Documentation_V3.md` — §3 Abel's 9-Step Decision Process (updated), §5 Updated Aspect Ratios, §4 Style Scoping
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Physiological State Specification Language.md` — PSSL formal grammar, bio-aesthetic evidence base, deterministic lighting instructions
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Carousel Physiological State Architecture Research.md` — Somatic arc types, GSR/HRV/fEMG biometrics, accumulation prohibition, semiotic injection positioning
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Gaze Cueing in Design Framework.md` — Zone assignment (Identity/Hook/Action), dual-vector gaze geometry, CBCS-indexed gaze direction
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Cinematographic Emotional Grammar Framework Research.md` — CEGF Color Architecture Matrix, CGCS coding scheme, lighting grammar temporal signals
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Tribal Imageability and Cultural Half-Life.md` — TIRS for noun-visual congruence pairing
- `d:\Work\The Conscious Coaching Factory\docs\architecture\FR50_Sovereign_Image_Rule_Tech_Spec.md` — Reference template for structure and depth

---

## 2. Overview

### Problem Statement
Every visual asset the Conscious Coaching Platform produces must be engineered, not decorated. The script's psychological intent — its somatic arc type, emotional trajectory, tribal vocabulary, and conversion function — must be deterministically translated into a complete Visual Composition Brief (VCB) that specifies every parameter downstream agents need: pixel dimensions, PSSL lighting grammar, saturation values, gaze geometry, tribal noun placement, handle bar positioning, and semantic conflict mappings. Without a deterministic VCB generation process, downstream agents (Paradoxe, Aurore, the Canva App) operate on ambiguous or incomplete instructions, producing visuals that look professionally composed but fail to trigger the specific physiological states the script was designed to evoke. The VCB is the contract between the script's psychological intent and the visual pipeline's deterministic execution.

### Solution
FR-VIS-01 defines Abel's (Visual Composition Planner) complete 9-step decision process for generating VCBs. Abel receives the finalized content output (DEP-ENG-011) with the locked format and style constraints (FR-VIS-07, FR-VIS-08), queries the TIAR for active tribal nouns (FR-VIS-02), and produces a complete VCB that specifies every parameter for every slide. The VCB must pass Gate C-09 (PSSL Completeness Check) before proceeding to prompt compilation. Gate C-09 validates 7 specific PSSL completeness rules — no VCB exits without full deterministic specification.

### Scope
**In scope:**
- Abel's 9-step VCB generation decision process.
- Per-slide PSSL parameter assignment (lighting_grammar, saturation_pct, head_rotation_degrees, pupil_position_ratio_pct, PAD environmental_grammar, chromatic_bloom_sequence).
- Gate C-09 (PSSL Completeness Check) — 7 validation rules.
- Integration with upstream constraints (FR-VIS-07 format, FR-VIS-08 style, FR-VIS-02 TIAR).

**Out of scope:**
- Prompt compilation from VCB (handled by FR-VIS-03).
- Image sourcing (handled by FR-VIS-09, FR-VIS-10).
- Visual validation post-generation (handled by FR-VIS-04).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-011` | Finalized Content Output | INPUT — Script with psychological routing, hook text, somatic arc type. |
| `DEP-ENG-016` | Psychological Routing Brief | INPUT — Emotional trajectory, mood state, conversion intent for the content piece. |
| `DEP-ENG-003` | Voice DNA | INPUT — Coach's tonal signature informing visual tone alignment. |
| `DEP-VIS-001` | Tribal Imagen Activation Registry | INPUT — Active tribal nouns injected via FR-VIS-02. |
| `DEP-VIS-002` | Visual Recipe Protocol Library | REFERENCE — 12 recipe protocols that define per-format composition templates. |
| `DEP-VIS-003` | Stage Set Emotional Architecture Library | REFERENCE — Stage set configurations mapped to emotional states. |
| `DEP-VIS-005` | Visual Composition Brief Schema | OUTPUT — The completed VCB. |
| `DEP-ENG-041` | Receipt Chain Guard | AUDIT — VCB generation stages are hashed and recorded. |
| `FR-VIS-07` | Format & Aspect Ratio Enforcement | UPSTREAM — Locked format_constraint_envelope (dimensions, aspect ratio). |
| `FR-VIS-08` | Style Scoping | UPSTREAM — Sealed style_constraint_directive (permitted styles, grammar system). |
| `FR-VIS-02` | TIAR Integration | UPSTREAM — Active noun vocabulary and blocked noun list. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Applied |
|---|---|---|---|
| **Physiological State Specification Language (PSSL)** | CCP Research Lab | 2026 | The PSSL provides the formal grammar for Abel's per-slide parameter assignment. Each PSSL field is not a creative suggestion — it is a deterministic instruction that maps to a measurable physiological response. `lighting_grammar: "golden hour lateral, temporal_signal: 4200K-4800K warm transition over 3s"` specifies a color temperature range that reliably activates the zygomaticus major (smile muscle) within 200ms of visual exposure. `saturation_pct: 72` specifies a saturation level calibrated to the optimal arousal point on the Yerkes-Dodson curve for the target mood state. Abel's role is to translate the script's psychological intent into these precise PSSL values. |
| **Carousel Physiological State Architecture** | CCP Research Lab | 2026 | The somatic arc type determines the sequence of PSSL states across slides. A Tension-Release arc requires the first 3 slides to progressively increase saturation (55% → 65% → 78%) and tighten shadow angles (45° → 30° → 15°), building physiological tension measured via GSR, then release on slide 4 with a saturation drop to 42% and shadow expansion to 60°. Abel must map each slide's position in the arc to the correct PSSL parameters. The accumulation prohibition rule (no completion imagery in accumulation slides) prevents premature tension release that would collapse the GSR build-up. |
| **Gaze Cueing in Design Framework** | CCP Research Lab | 2026 | Abel assigns `head_rotation_degrees` and `pupil_position_ratio_pct` per slide to engineer the Gaze Cueing Effect across three architectural zones: Identity Zone (coach recognition), Hook Zone (tribal noun / key concept), Action Zone (CTA / swipe prompt). For cold audiences (CBCS < 3), the character's gaze directs toward the Hook Zone (informational attention). For warm audiences (CBCS ≥ 7), gaze directs toward the Action Zone (conversion intent). Abel reads the CBCS score from the Psychological Routing Brief and applies the corresponding gaze vector. |
| **Cinematographic Emotional Grammar Framework** | CCP Research Lab | 2026 | The CEGF Color Architecture Matrix maps four mood states (Processing, Escape, Discovery, Status) to deterministic chromatic parameters. Abel uses the Psychological Routing Brief's mood designation to select the correct color architecture: Processing → cool desaturated (4500K, 35-50% sat), Escape → warm high-saturation (3200K, 70-85% sat), Discovery → neutral mid-saturation (5000K, 55-65% sat), Status → cool high-contrast (6000K+, 60-75% sat). `chromatic_bloom_sequence` specifies the color transition across slides, not per-slide static color. |
| **Tribal Imageability and Cultural Half-Life** | CCP Research Lab | 2026 | Abel pairs TIAR nouns with visual elements ensuring congruence: a text slide containing the tribal noun "Sunday night dread spiral" must be paired with visual elements that evoke the noun's concrete referent — dim lighting, isolation, indoor domestic setting — not abstract geometric patterns. Noun-visual incongruence reduces TIRS potency by 1.8-2.4 points because the audience's visual processing contradicts the text's semantic content, creating a cross-modal conflict that degrades engagement. |

### Technical Decisions
1. **9-Step Sequential Decision Process:** Abel's steps must execute sequentially, not in parallel, because each step depends on the output of the previous. Format determination (Step 1) constrains recipe selection (Step 2), which constrains PSSL assignment (Step 3). Parallelizing any steps would require speculative execution with rollback — unacceptable complexity for a deterministic pipeline.
2. **Gate C-09 as Internal Quality Gate:** Gate C-09 is not a separate agent — it is the final validation within Abel's own process. Abel assembles the VCB, then Abel's Gate C-09 module validates it. If the VCB fails C-09, Abel revises internally before emitting. This prevents unnecessary inter-agent communication overhead for fixable validation failures.
3. **PAD Environmental Grammar as Compound Field:** The PAD (Pleasure-Arousal-Dominance) environmental grammar is specified as three numeric scores (e.g., `P: 0.4, A: 0.7, D: 0.3`) that Paradoxe translates into environmental descriptors. Abel does not write environmental descriptions — Abel writes the PAD vector, and Paradoxe interprets it. This separation ensures Abel's decisions remain deterministic (numeric) and Paradoxe's prompt compilation remains creative (linguistic).

---

## 4. Implementation Plan

### Stage 1: Format Determination & Recipe Selection (Steps 1-2)
*Agent:* Abel (Visual Composition Planner)
*Inputs:* Finalized content output (DEP-ENG-011), locked `format_constraint_envelope` (FR-VIS-07), sealed `style_constraint_directive` (FR-VIS-08), Psychological Routing Brief (DEP-ENG-016).
*Outputs:* `selected_format`, `selected_recipe_id`, `slide_count`, `somatic_arc_type`.
*Failure Condition:* Recipe not found for format-style combination; Abel escalates to operator with `RECIPE_NOT_FOUND`.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. **Step 1 — Format Determination:** Abel reads the locked `format_constraint_envelope` from FR-VIS-07. The format is already locked — Abel does not determine it; Abel confirms it and extracts the format parameters (aspect ratio, slide count, bleed zone).
2. **Step 2 — Recipe Protocol Selection:** Abel queries the Visual Recipe Protocol Library (DEP-VIS-002) for recipes matching the locked format and the permitted styles from the style directive. Each recipe specifies a composition template: zone positions, text placement regions, image regions, handle bar position, and the somatic arc type (Tension-Release, Discovery-Revelation, Contrast-Resolution, Accumulation-Cliff). Abel selects the recipe that best matches the Psychological Routing Brief's mood state and conversion intent.

### Stage 2: PSSL Parameter Assignment (Step 3)
*Agent:* Abel (Visual Composition Planner)
*Inputs:* Selected recipe, Psychological Routing Brief (DEP-ENG-016), Stage Set Emotional Architecture Library (DEP-VIS-003), somatic arc type.
*Outputs:* Per-slide PSSL parameter block for every slide in the composition.
*Failure Condition:* PSSL field cannot be resolved from routing brief (e.g., mood state not found in CEGF Color Architecture Matrix); Abel logs `PSSL_RESOLUTION_FAILURE` and uses the neutral Processing mood as safe default.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Per-Slide PSSL Fields (all mandatory):**

| Field | Type | Example | Source |
|---|---|---|---|
| `lighting_grammar` | String (with temporal signal and shadow spec) | `"golden hour lateral, temporal_signal: 4200K-4800K over 3s, shadow: 30° key, fill ratio 2:1"` | CEGF Color Architecture Matrix + somatic arc position |
| `saturation_pct` | Integer (0-100) | `72` | CEGF + somatic arc tension curve |
| `head_rotation_degrees` | Float (-90 to 90) | `15.0` | Gaze Cueing Framework + CBCS score |
| `pupil_position_ratio_pct` | Float (0-100, horizontal %) | `65.0` | Gaze Cueing Framework + target zone |
| `pad_environmental_grammar` | Object {P, A, D} (-1.0 to 1.0) | `{"P": 0.4, "A": 0.7, "D": 0.3}` | Psychological Routing Brief mood state |
| `chromatic_bloom_sequence` | Array of hex+transition | `["#2D1B69→#FF6B35 ease 2s", "#FF6B35→#1A1A2E ease 1.5s"]` | CEGF + somatic arc color trajectory |
| `incomplete_tribal_artifact` | String or null | `"half-drawn circle"` | Required non-null for tension/accumulation slides |

### Stage 3: TIAR Query & Tribal Noun Pairing (Step 4)
*Agent:* Abel (Visual Composition Planner)
*Inputs:* TIAR `active_noun_vocabulary` and `blocked_noun_list` (from FR-VIS-02 downstream injection).
*Outputs:* Per-slide `tribal_noun_assignments` — which TIAR nouns appear in which text regions.
*Failure Condition:* Insufficient active nouns for minimum coverage (< 3 per text slide); Abel logs `TIAR_COVERAGE_INSUFFICIENT` and requests vocabulary expansion from TIAR adapter.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Abel receives the active noun vocabulary from FR-VIS-02.
2. For each text slide, Abel selects ≥ 3 concrete TIAR nouns that are congruent with the slide's visual elements and emotional state.
3. Abel checks that no expired noun appears in any text field.
4. Abel pairs each noun with a visual element specification ensuring noun-visual congruence (see Academic Grounding).

### Stage 4: Handle Bar, Semantic Conflict, Accumulation & Semiotic Injection (Steps 5-8)
*Agent:* Abel (Visual Composition Planner)
*Inputs:* Selected recipe, format, slide assignments, somatic arc type.
*Outputs:* Per-slide `handle_bar_config`, `semantic_conflict_spec`, `accumulation_audit_result`, `semiotic_injection_position`.
*Failure Condition:* Accumulation prohibition violated (completion imagery in accumulation slide); Abel auto-corrects and logs the correction.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. **Step 5 — Coach Handle Bar Decision:** Abel determines whether each slide includes the coach handle bar (profile picture, name, handle, logo). Handle bar is mandatory on slide 0 (cover) for all carousels. For single images: always present. For polls: present in header zone only. Position is locked to top — not movable.
2. **Step 6 — Semantic Conflict Specification:** Abel maps semantic conflicts between visual elements per slide. If slide 3's text says "breaking free" but the image shows a person in a confined space, the semantic conflict is intentional (tension-building). If unintentional, Abel flags it for correction. Each conflict is tagged as `intentional_tension`, `intentional_contrast`, or `conflict_error`.
3. **Step 7 — Accumulation Prohibition Audit:** For somatic arcs using accumulation (Accumulation-Cliff), Abel verifies that no accumulation slide (slides before the cliff) contains completion imagery — checkmarks, finish lines, trophy images, celebration poses. These would prematurely release the tension that the accumulation arc is building. Violating slides are flagged for revision.
4. **Step 8 — Semiotic Injection Positioning:** For sequences with 4+ slides, Abel positions the semiotic injection element (the moment of symbolic meaning crystallization) in the latter third of the sequence. For a 7-slide carousel, semiotic injection occurs on slide 5 or 6 — never on slides 1 or 2. This ensures the audience has built sufficient contextual scaffolding before the pivotal symbolic moment arrives.

### Stage 5: Tribal Noun-Visual Congruent Pairing & Gate C-09 (Step 9 + Validation)
*Agent:* Abel (Visual Composition Planner) + Gate C-09 module
*Inputs:* Completed VCB draft, all per-slide assignments from Stages 1-4.
*Outputs:* `GATE_C09_PASS` (VCB emitted to downstream pipeline) or `GATE_C09_FAIL` (VCB returned to Abel Stage 2 for internal revision).
*Failure Condition:* VCB fails Gate C-09 validation; Abel revises internally. Maximum 3 internal revisions before escalation.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Gate C-09 Validation Rules:**

| Rule | Validation | Failure Response |
|---|---|---|
| C09-R01 | All `lighting_grammar` fields contain a `temporal_signal` specification | Return to Stage 2 — lighting grammar incomplete |
| C09-R02 | All `saturation_pct` values are numeric integers (0-100) | Return to Stage 2 — non-numeric saturation |
| C09-R03 | All text slides contain ≥ 3 concrete TIAR nouns (`in_distribution` or `tribal_potential`) | Return to Stage 3 — insufficient TIAR coverage |
| C09-R04 | All character slides have numeric `head_rotation_degrees` AND `pupil_position_ratio_pct` | Return to Stage 2 — gaze geometry incomplete |
| C09-R05 | All slides have PAD scores (P, A, D each between -1.0 and 1.0) | Return to Stage 2 — PAD missing |
| C09-R06 | All tension/accumulation slides have non-null `incomplete_tribal_artifact` | Return to Stage 4 — accumulation prohibition incomplete |
| C09-R07 | Semiotic injection is NOT on slide 1 or 2 of 4+ slide sequences | Return to Stage 4 — semiotic positioning error |

---

## 5. Primary Output Schema

### Schema Name: `Visual_Composition_Brief.json` (DEP-VIS-005)

```json
{
  "vcb_id": "VCB-JP-20260318-012",
  "content_output_id": "CO-JP-20260318-012-CAROUSEL",
  "content_format": "carousel_dopamine_cliff",
  "selected_recipe_id": "RCP-CAROUSEL-DOPAMINE-CLIFF-003",
  "somatic_arc_type": "tension_release",
  "slide_count": 7,
  "format_envelope_id": "FCE-JP-20260318-001",
  "style_directive_id": "SCD-JP-20260318-001",
  "visual_style": "cinematic_color_graded",
  "per_slide_assignments": [
    {
      "slide_index": 0,
      "slide_type": "hook_cover",
      "image_type": "tier_3_ai_realistic",
      "pssl": {
        "lighting_grammar": "golden hour lateral, temporal_signal: 4200K-4800K warm transition over 3s, shadow: 30° key angle, fill ratio 2:1",
        "saturation_pct": 65,
        "head_rotation_degrees": 15.0,
        "pupil_position_ratio_pct": 65.0,
        "pad_environmental_grammar": { "P": 0.3, "A": 0.7, "D": 0.4 },
        "chromatic_bloom_sequence": ["#2D1B69→#FF6B35 ease 2s"],
        "incomplete_tribal_artifact": null
      },
      "tribal_noun_assignments": [
        { "noun": "the 5am alarm defeat", "position": "hook_text", "congruent_visual_element": "dimly lit bedroom, alarm clock glow" },
        { "noun": "Sunday night dread spiral", "position": "overlay_text", "congruent_visual_element": "couch corner, laptop open, dark window" },
        { "noun": "client ghost", "position": "subtext", "congruent_visual_element": "empty chair across desk" }
      ],
      "handle_bar": { "visible": true, "position": "top_locked" },
      "semantic_conflicts": [],
      "named_person_reference": null
    },
    {
      "slide_index": 1,
      "slide_type": "tension_build_1",
      "image_type": "tier_2_stock_contextual",
      "pssl": {
        "lighting_grammar": "overcast diffused, temporal_signal: 5200K-5600K neutral hold, shadow: 45° key angle, fill ratio 3:1",
        "saturation_pct": 55,
        "head_rotation_degrees": -10.0,
        "pupil_position_ratio_pct": 45.0,
        "pad_environmental_grammar": { "P": -0.2, "A": 0.5, "D": 0.2 },
        "chromatic_bloom_sequence": ["#1A1A2E→#2D1B69 ease 1.5s"],
        "incomplete_tribal_artifact": "half-finished to-do list"
      },
      "tribal_noun_assignments": [
        { "noun": "revenue plateau confession", "position": "body_text", "congruent_visual_element": "flat graph line, stagnant water" },
        { "noun": "launch anxiety loop", "position": "hook_text", "congruent_visual_element": "circular pathway, hamster wheel" },
        { "noun": "the 5am alarm defeat", "position": "subtext", "congruent_visual_element": "crumpled bedsheets" }
      ],
      "handle_bar": { "visible": false, "position": null },
      "semantic_conflicts": [
        { "conflict_type": "intentional_tension", "element_a": "revenue plateau confession (text)", "element_b": "flat graph line (visual)", "purpose": "reinforce stagnation feeling" }
      ],
      "named_person_reference": null
    }
  ],
  "accumulation_audit": {
    "arc_type": "tension_release",
    "accumulation_slides": [1, 2, 3],
    "completion_imagery_detected": false,
    "audit_status": "CLEAN"
  },
  "semiotic_injection": {
    "injection_slide_index": 5,
    "total_slides": 7,
    "position_valid": true,
    "injection_element": "crystallization moment — symbolic transformation visual"
  },
  "gate_c09_result": "PASS",
  "gate_c09_checks": {
    "C09-R01_lighting_temporal": "PASS",
    "C09-R02_saturation_numeric": "PASS",
    "C09-R03_tiar_coverage": "PASS",
    "C09-R04_gaze_geometry": "PASS",
    "C09-R05_pad_scores": "PASS",
    "C09-R06_incomplete_artifact": "PASS",
    "C09-R07_semiotic_position": "PASS"
  },
  "tiar_validation_timestamp": "2026-03-18T01:36:00Z",
  "receipt_chain_block": "RCB-VCB-20260318-012",
  "timestamp_utc": "2026-03-18T01:36:30Z"
}
```

---

## 6. Backward Compatibility Fallback

If the upstream Finalized Content Output (DEP-ENG-011) does not include a Psychological Routing Brief (DEP-ENG-016) — e.g., older pipeline version — Abel applies a neutral default routing:
1. Mood state defaults to `Processing` (safest for visual tone — cool, neutral, analytical).
2. CBCS score defaults to `4` (mid-range, moderate engagement depth).
3. Gaze direction defaults to Hook Zone (informational attention, appropriate for unknown audience depth).
4. A `LEGACY_ROUTING_DEFAULT` warning is logged in the VCB and Receipt Chain.
5. The VCB is valid but suboptimal — it will produce visually coherent but psychologically unoptimized content.

---

## 7. Tasks

- [ ] **Task 1:** Write `abel_vcb_generator.py` implementing the complete 9-step sequential decision process.
- [ ] **Task 2:** Implement the recipe protocol selection logic — query DEP-VIS-002 for recipes matching the locked format + permitted styles, rank by mood state alignment.
- [ ] **Task 3:** Implement the PSSL parameter assignment engine — map Psychological Routing Brief mood states to CEGF Color Architecture Matrix values, compute somatic arc tension curves for per-slide saturation, lighting, and PAD progression.
- [ ] **Task 4:** Implement the gaze geometry engine — compute `head_rotation_degrees` and `pupil_position_ratio_pct` based on CBCS score and target zone (Identity/Hook/Action) per slide.
- [ ] **Task 5:** Implement the tribal noun-visual congruence pairing — validate that each TIAR noun's text placement is paired with a visually congruent element specification.
- [ ] **Task 6:** Implement the coach handle bar decision logic — format-specific rules for visibility, position (always top-locked), and presence per slide.
- [ ] **Task 7:** Implement the semantic conflict specification logic — detect and tag intentional vs. unintentional text-visual conflicts per slide.
- [ ] **Task 8:** Implement the accumulation prohibition audit — scan accumulation slides for completion imagery descriptors (checkmarks, finish lines, trophies, celebration poses) and flag violations.
- [ ] **Task 9:** Implement the semiotic injection positioning logic — validate position is in the latter third of 4+ slide sequences.
- [ ] **Task 10:** Implement Gate C-09 as an internal validation module with all 7 rules (C09-R01 through C09-R07), maximum 3 internal revision cycles, and escalation on persistent failure.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Full VCB Generation):** Submit a finalized content output for a 7-slide `carousel_dopamine_cliff` with mood `Escape` and CBCS `6`. Assert Abel produces a complete VCB with 7 per-slide assignments, each containing all mandatory PSSL fields, ≥ 3 TIAR nouns on text slides, handle bar on slide 0, semiotic injection on slide 5 or 6, and Gate C-09 PASS. *Failure Example:* Abel produces a VCB with `saturation_pct: "high"` instead of a numeric value, failing C09-R02.
- [ ] **AC2 (Somatic Arc Saturation Curve):** For a Tension-Release arc across 7 slides, assert slides 0-3 show progressively increasing `saturation_pct` (e.g., 55 → 60 → 68 → 78) and slides 4-6 show decreasing saturation (e.g., 78 → 52 → 42). *Failure Example:* All 7 slides have identical `saturation_pct: 65`, producing a flat emotional arc with no tension or release.
- [ ] **AC3 (Gaze Geometry — Cold Audience):** Submit content with CBCS `2` (cold). Assert `pupil_position_ratio_pct` is directed toward the Hook Zone (approximately 35-45% horizontal position). *Failure Example:* Gaze is directed toward the Action Zone for a cold audience that hasn't built enough trust for a CTA — producing a "pushy" visual that repels rather than attracts.
- [ ] **AC4 (Gaze Geometry — Warm Audience):** Submit content with CBCS `8` (warm). Assert `pupil_position_ratio_pct` is directed toward the Action Zone (approximately 70-85% horizontal position). *Failure Example:* Gaze is directed toward the Hook Zone for a warm audience that already knows the concept — producing a redundant attention flow that misses the conversion opportunity.
- [ ] **AC5 (Accumulation Prohibition):** Submit a VCB with `somatic_arc_type: "accumulation_cliff"` and add a checkmark icon to slide 3 (an accumulation slide). Assert the accumulation prohibition audit detects the completion imagery and flags the violation. *Failure Example:* A checkmark on slide 3 prematurely signals "task complete," collapsing the accumulation tension that slide 4's cliff depends on.
- [ ] **AC6 (Semiotic Injection Position):** Submit a 6-slide carousel. Assert semiotic injection is placed on slide 4 or 5 (latter third of 6). Attempt to place it on slide 1. Assert Gate C-09 fails with C09-R07. *Failure Example:* Semiotic injection on slide 1 delivers the symbolic crystallization moment before the audience has built the contextual scaffolding to understand it — the symbol falls flat.
- [ ] **AC7 (Gate C-09 Full Validation):** Submit a VCB that violates C09-R01 (missing temporal signal in lighting grammar), C09-R03 (only 1 TIAR noun on slide 2), and C09-R05 (missing PAD on slide 4). Assert Gate C-09 detects all 3 violations and Abel revises internally. Verify the revised VCB passes all 7 rules. *Failure Example:* Gate C-09 reports only C09-R01, Abel fixes it, resubmits, and then C09-R03 is caught — requiring 3 revision cycles instead of 1.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| DEP-ENG-011 (Finalized Content Output) | Internal | Primary input — script, hook text, arc type. |
| DEP-ENG-016 (Psychological Routing Brief) | Internal | Mood state, CBCS score, conversion intent. |
| DEP-ENG-003 (Voice DNA) | Internal | Tonal signature for visual tone alignment. |
| DEP-VIS-001 (TIAR) | Internal | Active tribal nouns via FR-VIS-02 adapter. |
| DEP-VIS-002 (Visual Recipe Protocol Library) | Internal | 12 recipe protocols for format-style composition templates. |
| DEP-VIS-003 (Stage Set Emotional Architecture Library) | Internal | Stage set configurations for PAD-driven environmental settings. |
| DEP-VIS-005 (VCB Schema) | Internal | Output schema for the completed VCB. |
| DEP-ENG-041 (Receipt Chain Guard) | Internal | Audit — all stages hashed and recorded. |
| FR-VIS-07 (Format & Aspect Ratio Enforcement) | Internal | Upstream — locked format envelope. |
| FR-VIS-08 (Style Scoping) | Internal | Upstream — sealed style directive. |
| FR-VIS-02 (TIAR Integration) | Internal | Upstream — active noun vocabulary. |
| FR-VIS-03 (PSSL Prompt Compilation) | Internal | Downstream — Paradoxe consumes the VCB. |
| FR-VIS-13 (Image Type Validity Gate) | Internal | Gate V-00 validates image types before Aurore begins sourcing. |

---

## 10. Testing Strategy

### Unit Tests
- **PSSL Parameter Completeness:** Provide a 7-slide carousel recipe with mood `Escape`. Assert all 7 slides have non-null `lighting_grammar` (with temporal signal), numeric `saturation_pct`, numeric `head_rotation_degrees`, numeric `pupil_position_ratio_pct`, valid PAD object, and non-empty `chromatic_bloom_sequence`.
- **Somatic Arc Curve:** For a `tension_release` arc with 7 slides, assert saturation values form a curve: increasing for the tension phase, decreasing for the release phase. Validate the peak slide has the highest saturation.
- **Gate C-09 Rule Isolation:** For each of the 7 C09 rules, provide a VCB that violates only that single rule. Assert the gate catches the violation and only that violation.

### Integration Tests
- **End-to-End VCB Generation:** Submit a finalized content output through FR-VIS-07 → FR-VIS-08 → FR-VIS-02 → FR-VIS-01. Assert the VCB passes Gate C-09, contains all mandatory fields, and its format/style match the upstream constraints.
- **TIAR Integration:** Submit content with 5 active TIAR nouns and 2 expired nouns. Assert the VCB contains only active nouns and at least 3 per text slide.

### Safety Tests (ADR-01 Quarantine Security)
- **PSSL Injection:** Inject `lighting_grammar: "golden hour; rm -rf /"` into a test routing brief. Assert Abel's PSSL assignment engine treats the entire string as a lighting descriptor, does not execute any embedded commands, and the resulting VCB contains the verbatim (sanitized) string.
- **VCB Tampering Detection:** After Gate C-09 passes, modify a VCB slide's `saturation_pct` from 72 to 99. Assert the Receipt Chain Guard detects the hash mismatch at the next downstream stage (Paradoxe's prompt compilation).
