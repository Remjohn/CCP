# Conscious Visual Engine (CVE) — System Documentation V2.0

**Author:** Emilio  
**Date:** 2026-03-17  
**Version:** 2.0  
**Status:** Architecture Specification — Integration Draft  
**Feeds Into:** PRD Update, Tech Spec, Skill Templates, Conscious Canva App Build

---

## Document Purpose

This document specifies the complete architecture of the Conscious Visual Engine (CVE) — the visual execution layer of the Conscious Coaching Platform (CCP). It is written to serve four simultaneous purposes: to update the existing PRD, to drive the technical specification for the Conscious Canva App, to define the RunningHub API integration contracts, and to specify the SKILL.md templates and agent behaviors required to operationalize visual production at 36 pieces per week per coach.

This is not a design theory document. Every section resolves to a buildable system component — an agent, a registry entry, a validation gate, an API contract, or a template schema.

---

## Section 1 — CVE Position in the CCP Architecture

### 1.1 The Sixth System

The CCP currently operates five integrated systems: the Content Factory (CCF), the Invisible Coaching App (CBCS), the Webinar System (V2WS), the Tierlist, and the Notion Delivery Layer. The CVE is the sixth system — it does not replace any existing system. It extends the CCF by adding a complete visual production pipeline downstream of script validation.

The architectural position is precise:

```
CCF Pipeline → Script Validation (Triple-Pass Gate) → [Visual Production Flag SET]
                                                              ↓
                                              CVE Visual Composition Planning
                                                              ↓
                                              Conscious Canva App (Template Layer)
                                                              ↓
                                              RunningHub API (Render Execution)
                                                              ↓
                                              Notion Delivery (Coach Approval)
```

The CVE does not operate independently. It activates only after a script has passed the Triple-Pass Validation Gate (Sophia, Marcus, Chen) and has been flagged for visual production. The script is the upstream authority. The visual serves the script — never the reverse.

### 1.2 What the CVE Produces

The CVE produces three output types:

**Type 1 — Carousel Compositions:** Multi-slide vertical sequences in 4:5 format (1080×1350px). Built from the carousel-eligible Visual Recipe Protocols and rendered through RunningHub. Visual styles available for carousels: cinematic color-graded and semi-realistic digital only.

**Type 2 — Single Image Compositions:** Standalone visual posts in 4:5 format (1080×1350px) for standard single images, or 9:16 format (1080×1920px) for polls. Includes memes, tweet-style quotes, observational humor, worst-case scenario frames, polls, and supervisuals. Ghibli and illustrated styles are available only for single image compositions.

**Type 3 — Visual Brief Exports:** For script types assigned to short-form video (Case Studies, Myth Debunking, Tier Lists, Reaction content), the CVE produces a structured art direction document — scene-by-scene composition guidance for the coach's recording setup or a video editor. No rendered image is produced.

### 1.3 The Sovereign Image Rule Extension

The existing PRD Sovereign Image Rule (AI-generated visual elements may only represent abstract client scenarios or metaphorical concepts — the coach's face is never artificially generated) is extended by the CVE with three additions:

**Extension A:** AI-generated avatar characters and real coach photography exist in separate content tracks and never appear in the same visual composition.

**Extension B:** Real coach photography is sourced exclusively from the Personal Branding Photo Deck in Notion. If no suitable photo exists for the required emotional register, the system generates a photo session recommendation — it does not substitute AI generation.

**Extension C:** When real photography is used, the PSSL parameters for lighting grammar, chromatic specification, and environmental grammar function as production direction specifications for the photography session — not as AI generation parameters. The PSSL serves the entire visual pipeline, including real photography art direction.

### 1.4 Agent Roles in the CVE

- **Abel** (existing Visual Recipe Router) → upgraded to Visual Composition Planner — Section 3
- **Paradoxe** (existing Visual Prompt Synthesizer) → upgraded to PSSL Prompt Compiler — Section 7
- **Visual Validation Agent** (new) — post-generation quality gate — Section 10

---

## Section 2 — The Script-to-Visual Production Flow

### 2.1 Trigger Conditions

Visual production is triggered when a script has passed all three validation gates AND its archetype maps to a visual output type. The Visual Production Flag is set in the Finalized Content Output (DEP-ENG-011):

```json
{
  "asset_id": "CCFA-C01-03-26-0042",
  "visual_production_flag": true,
  "visual_output_type": "carousel",
  "recipe_protocol_id": "relief_peak_carousel_recipe",
  "script_archetype": "recognition_story",
  "coaching_segment": "conscious_business",
  "mood_state": "escape",
  "tii_score": 45,
  "arc_type": "tension_release"
}
```

### 2.2 The Full Script JSON Package

The visual system receives the complete production context that built the script — not just the script text. This is what makes visual-linguistic congruence possible.

```json
{
  "asset_id": "CCFA-C01-03-26-0042",
  "script_text": "...",
  "script_components": {
    "archetype_id": "relief_peak_carousel_recipe",
    "emotional_angle": "validation_relief",
    "arc_type": "tension_release",
    "hook_text": "The 3am integrity check",
    "hook_concrete_nouns": ["3am", "integrity"],
    "slide_texts": ["...", "...", "...", "...", "..."],
    "cta_text": "..."
  },
  "psychological_routing": {
    "mood_state": "escape",
    "arousal_direction": "descending",
    "valence_target": "positive",
    "regulatory_frame": "prevention",
    "tii_score": 45
  },
  "cral_findings": {
    "m1_relevant": "...",
    "m4_resonant": "...",
    "m7_relatable": "..."
  },
  "tribal_context": {
    "coaching_segment": "conscious_business",
    "active_tribal_nouns": ["resonance", "integrity", "threshold", "wholeness"],
    "enemy_typology": "performative success culture",
    "audience_recognition_context": "late-stage burnout from values misalignment"
  },
  "voice_dna_ref": "DEP-ENG-003",
  "fingerprint_id": "FP-20260317-0042"
}
```

### 2.3 Format-to-Recipe Routing

The routing table maintained in DEP-VIS-002:

| Script Archetype | Visual Output Type | Aspect Ratio | Recipe Protocol |
|---|---|---|---|
| Relief Peak | Carousel | 4:5 | `relief_peak_carousel_recipe` |
| Dopamine Cliff | Carousel | 4:5 | `dopamine_cliff_recipe` |
| Curiosity Listicle | Carousel | 4:5 | `listicle_visual_recipe` |
| Funny Relatable Listicle | Carousel | 4:5 | `listicle_visual_recipe` |
| Nostalgia Listicle | Carousel | 4:5 | `listicle_visual_recipe` |
| Fear-Anxiety Listicle | Carousel | 4:5 | `listicle_visual_recipe` |
| Hope & Inspiration Listicle | Carousel | 4:5 | `listicle_visual_recipe` |
| Outrageous Listicle | Carousel | 4:5 | `listicle_visual_recipe` |
| Visual Timeline | Carousel | 4:5 | `visual_timeline_recipe` |
| Comparison (single contrast) | Single Image | 4:5 | `comparison_archetypes_recipe` |
| Comparison (multiple contrasts) | Carousel | 4:5 | `comparison_archetypes_recipe` |
| Conceptual Contrast (simultaneous) | Single Image | 4:5 | `conceptual_contrast_recipe` |
| Conceptual Contrast (transformational) | Carousel | 4:5 | `conceptual_contrast_recipe` |
| Observational Humor | Single Image | 4:5 | `observational_humor_recipe` |
| Worst Case Scenario | Single Image | 4:5 | `worst_case_scenario_recipe` |
| Tweet-Style Quote | Single Image | 4:5 | `tweet_quote_recipe` |
| Stereotypical Poll | Single Image | 9:16 | `poll_visual_recipe` |
| Archetypical Poll | Single Image | 9:16 | `archetypical_poll_recipe` |
| Controversial Dilemma Poll | Single Image | 9:16 | `controversial_dilemma_poll_recipe` |
| Would You Rather | Single Image | 9:16 | `poll_visual_recipe` |
| 9-Grid Accumulation | Single Image (grid) | 4:5 | `nine_grid_recipe` |
| Dopamine Cliff + 9-Grid | Single Image (grid) | 4:5 | `nine_grid_recipe` |
| Case Study | Visual Brief Export | — | Video-only format |
| Myth Debunking | Visual Brief Export | — | Video-only format |
| Recognition Story Reel | Visual Brief Export | — | Video-only format |
| Tier List Hybrid | Visual Brief Export | — | Video-only format |

### 2.4 Visual Style Assignment by Format

Visual style is not assigned by TII score alone — it is constrained first by format type:

**Carousels (all types):** Cinematic color-graded or semi-realistic digital only. Ghibli and illustrated styles are never used in carousels.

**Single Image — Standard (4:5):** Cinematic color-graded, semi-realistic digital, or Ghibli/illustrated supervisual — determined by archetype and TII score. See style assignment rules in Section 5.

**Single Image — Polls (9:16):** Graphic/vector illustration or semi-realistic digital. No photorealistic cinematic for polls — the format requires high graphic readability at phone screen size.

**Visual Brief Exports:** No image generation. Written art direction document only.

### 2.5 Pipeline Execution Sequence

1. Visual Production Flag set in DEP-ENG-011
2. Abel receives full script JSON package
3. Abel confirms arc type match against recipe protocol
4. Abel generates full Visual Composition Brief (VCB) — all PSSL parameters per slide
5. PSSL Completeness Gate (C-09) validates all required fields
6. Photo Deck query if real photography required
7. Conscious Canva App loads recipe template, pre-populates content slots from VCB
8. Paradoxe compiles RunningHub-ready prompt strings per slide
9. RunningHub API executes image generation per slide requiring AI generation
10. Visual Validation Agent scores outputs (AGSS threshold + authenticity checklist)
11. Approved assets placed into canvas layer slots
12. Canvas composition assembled and available for operator editing
13. Operator approves, requests regeneration, or edits and approves
14. Receipt Chain confirmed, VPO record created
15. Notion delivery — complete visual content card pushed to coach workspace

---

## Section 3 — The Visual Composition Planning Agent (Abel Upgraded)

### 3.1 Agent Specification

**Agent Name:** Abel (upgraded)
**Previous Role:** Visual Recipe Router
**New Role:** Visual Composition Planner
**Department:** Expression Department
**Reads From:** DEP-ENG-011 (Full Script JSON Package), DEP-VIS-001 (Tribal Imagen Registry), DEP-VIS-002 (Visual Recipe Protocol Library), DEP-VIS-003 (Stage Set Emotional Architecture Library), DEP-VIS-004 (Brand Character Reference Archive), DEP-ENG-016 (Psychological Routing Brief), DEP-ENG-003 (Voice DNA), DEP-ENG-007 (Tribe Intelligence)
**Writes To:** DEP-VIS-005 (Visual Composition Brief)
**Cannot:** Generate final user-facing text, trigger RunningHub directly, access Tier 0 dependencies

### 3.2 Abel's Decision Process

**Step 1 — Arc Type Confirmation**
Abel reads `arc_type` from the script package and confirms it matches the recipe protocol's documented arc. Mismatch flags for operator review before proceeding.

**Step 2 — Format and Aspect Ratio Assignment**
Abel confirms visual output type (carousel vs single image vs visual brief export) and sets aspect ratio from the routing table in DEP-VIS-002. All carousels: 4:5. Standard single images: 4:5. Poll single images: 9:16.

**Step 3 — Semiotic Injection Position**
Abel determines the semiotic injection slide using the latter-third positioning principle: the emotional climax — facial expression injection, maximum chromatic intensity, identity declaration — belongs in the latter third of the sequence. The exact position within that range is determined by arc type and story logic:

- Tension-Release: semiotic injection at the exhale moment — typically the penultimate slide
- Accumulation-Cliff: semiotic injection at the cliff moment — typically slide 4 of 5 or slide 5 of 7
- Discovery-Revelation: semiotic injection at the revelation — typically the second-to-last slide
- Contrast-Resolution: semiotic injection at the resolution slide

The principle is: not the midpoint, not the last slide, the latter third. Story logic determines position within that range.

**Step 4 — Visual Style Assignment**
Abel assigns visual style based on format constraint first, then archetype override rules, then TII score:

Format constraint (binding):
- Carousel format → cinematic or semi-realistic only
- Poll single image → graphic/vector or semi-realistic only
- Standard single image → any style permitted

Archetype override (applied after format constraint):
- Worst Case Scenario → desaturated cinematic realism always
- Observational Humor → Ghibli/illustrated always (single image only)
- Fear-anxiety emotional angle → desaturated cinematic always

TII score applied only when no override and format permits:
- TII < 25 → cinematic color-graded
- TII 26-70 → semi-realistic digital
- TII > 70 → Ghibli/illustrated (single image) or semi-realistic (carousel)

**Step 5 — PSSL Parameter Generation Per Slide**
Abel generates all PSSL parameters per slide: somatic target state, lighting grammar, chromatic specification, character specification, environmental grammar, and typography specification.

**Step 6 — Tribal Noun + Visual Congruent Pairing**
For every text slide, Abel pairs each tribal concrete noun with a specific visual congruent — the exact scene element that fires dual-coding simultaneity. The pairing must be specific, not categorical.

**Step 7 — Stage Set Selection**
Abel queries DEP-VIS-003 using PAD score requirements per slide position, selecting stage sets with the highest tribal specificity for the coaching segment.

**Step 8 — Template Assignment**
Abel assigns the template ID from DEP-VIS-002 based on recipe protocol × visual style × aspect ratio.

**Step 9 — Coach Handle Bar Decision**
For 4:5 single image formats: coach handle bar component is INCLUDED by default.
For carousel final slide: coach handle bar component is INCLUDED.
For carousel interior slides (1 through n-1): coach handle bar NOT included.
For polls (9:16): coach handle bar NOT included — insufficient space.

### 3.3 Visual Composition Brief Schema (DEP-VIS-005)

The VCB is Abel's complete output. The schema per composition:

```json
{
  "vcb_id": "VCB-20260317-0042",
  "asset_id": "CCFA-C01-03-26-0042",
  "fingerprint_id": "FP-20260317-0042",
  "recipe_protocol": "relief_peak_carousel_recipe",
  "visual_output_type": "carousel",
  "arc_type": "tension_release",
  "total_slides": 5,
  "semiotic_injection_slide": 4,
  "semiotic_injection_rationale": "Tension-Release arc — exhale fires on penultimate slide after full tension build",
  "visual_style": "semi_realistic_digital",
  "aspect_ratio": "4:5",
  "canvas_dimensions": "1080x1350",
  "coaching_segment": "conscious_business",
  "tii_score": 45,
  "template_id": "TPL-RELIEF-PEAK-SEMI-001",
  "runninghub_workflow_id": "RH-WF-CAROUSEL-SEMI-001",
  "coach_handle_bar": {
    "final_slide": true,
    "interior_slides": false
  },
  "slides": [
    {
      "slide_number": 1,
      "arc_stage": "tension",
      "somatic_target": {
        "corrugator_state": "active",
        "zygomaticus_state": "suppressed",
        "scr_target": "elevated"
      },
      "lighting_grammar": "Overhead institutional fluorescent — 11pm temporal signal. Single cool-white source from above, no fill, hard shadows beneath eyes and chin. Subject reads as isolated within the environment.",
      "chromatic_spec": {
        "foundation_hue": "#2C3E50",
        "accent_hue": "#7F8C8D",
        "saturation_pct": 35,
        "saturation_direction": "stable",
        "temperature_direction": "cool"
      },
      "character_spec": {
        "head_rotation_degrees": 15,
        "head_rotation_direction": "right",
        "pupil_position_ratio_pct": 20,
        "pupil_direction": "right",
        "gaze_target_zone": "upper_right_text_zone",
        "expression": "suppressed_exhaustion_authentic",
        "expression_congruence_check": "eye_mouth_congruent",
        "skin_texture": "visible_pore_detail_required",
        "intentional_asymmetry": "left_eyebrow_2mm_higher"
      },
      "environmental_grammar": {
        "light_quality_signal": "11pm_institutional",
        "spatial_density": 9,
        "temporal_signal": "stillness_late_night",
        "world_color_temp_kelvin": 4200,
        "subject_frame_height_ratio_pct": 40,
        "pad_scores": {"pleasure": 3, "arousal": 5, "dominance": 2}
      },
      "typography": {
        "arc_stage": "tension",
        "font_category": "serif",
        "font_weight": 800,
        "primary_text": "The 3am integrity check",
        "primary_word_count": 5,
        "secondary_text": null,
        "body_copy": "PROHIBITED"
      },
      "tribal_noun_visual_congruent": {
        "noun": "3am",
        "visual_congruent": "Phone screen visible showing timestamp 03:14, draft email open — send button visible but untouched, cursor blinking in message body"
      },
      "incomplete_tribal_artifact": null,
      "first_person_pov": false,
      "intentional_imperfection": "Slightly askew notebook at desk edge — not repositioned",
      "semantic_conflict_spec": {
        "aspirational_state": "values-led entrepreneur operating from integrity",
        "depicted_reality": "draft email written from fear of losing the client rather than from values"
      },
      "accumulation_prohibition_passed": true
    }
  ]
}
```

---

## Section 4 — The Tribal Imagen Activation Registry (TIAR)

### 4.1 Registry Specification

**Dependency ID:** DEP-VIS-001
**Format:** Supabase JSONB
**Queried By:** Abel (pre-composition), Script Generation Skills (pre-generation, upstream)
**Update Cadence:** Human-curated quarterly TIRS validation, with CRAL-triggered updates when new tribal language patterns emerge from research cycles

The TIAR is the living lexical database that guarantees every concrete noun used in visual hooks and text elements carries currently active tribal imageability. It is curated through the existing CRAL research infrastructure — not through automated corpus analysis of AI-generated content. The tribal language intelligence comes from the same human evidence bias that governs all CRAL research.

### 4.2 TIAR Data Structure

```json
{
  "noun_id": "TIAR-CBS-042",
  "noun": "threshold",
  "coaching_segment": "conscious_business",
  "tirs_scores": {
    "tribal_specificity": 6.4,
    "affective_charge": 6.8,
    "dictionary_exclusivity": 5.9,
    "composite_score": 6.37
  },
  "decay_stage": "in_distribution",
  "decay_flag": null,
  "visual_congruent_mappings": [
    {
      "scene_grammar": "Character positioned at a literal boundary — doorway, edge of a platform, foot of a staircase — one foot committed to crossing, the other still behind. The body is mid-transition.",
      "emotional_register": "transformation_anticipation",
      "arc_stages_applicable": ["tension_build", "semiotic_climax"]
    },
    {
      "scene_grammar": "Two environments visible simultaneously — one familiar and slightly dark, one new and lit differently. Character's gaze directed toward the new environment.",
      "emotional_register": "discovery",
      "arc_stages_applicable": ["resolution_exhale"]
    }
  ],
  "replacement_candidates": ["liminal", "crossing", "edge_moment"],
  "last_cral_validation": "2026-02-01",
  "activation_history": {
    "uses_last_30_days": 4,
    "performance_avg_save_rate": 0.087
  }
}
```

### 4.3 Decay Stage Classifications

| Decay Stage | Signal | Action | System Behavior |
|---|---|---|---|
| Tribal Potential | Emerging in tribal CRAL research | Flag for validation | Queue for TIRS scoring |
| In-Distribution | Active, culturally specific | Full approval | Approved for all visual recipe use |
| Bleaching Onset | Appearing in adjacent corporate contexts | Monitor | Yellow flag in Abel's query |
| Mainstream Dilution | Generic usage widespread | Deprecate | Red flag — replaced in new productions |
| Terminal Obsolescence | Corporate adoption complete | Expired | Hard block on all new productions |

Decay stage is assigned by the System Operator using CRAL research signal — real named human examples of the word being used in non-tribal contexts, not automated corpus entropy scores.

### 4.4 Upstream Integration: Script Generation Skills

The TIAR's most important integration point is upstream — inside Script Generation Skill templates, not inside the visual pipeline. Concrete nouns must be selected with tribal charge at the script generation stage.

```yaml
# Pre-generation TIAR query — mandatory before hook generation
tiar_query:
  target_segment: "{{coaching_segment}}"
  required_decay_status: ["in_distribution", "tribal_potential"]
  output: "active_noun_list"

hook_generation_instruction: |
  Generate the hook for this {{archetype}} script.
  Required vocabulary — minimum 3 concrete nouns from this active tribal list:
  {{active_noun_list}}
  Explicitly EXCLUDE these expired terms:
  {{expired_noun_list}}
```

### 4.5 Four Coaching Segment Noun Libraries

**Conscious Business Coaches:** resonance, integrity, congruence, wholeness, threshold, emergence, embodied, alignment, sovereignty, discernment

**High-Performance Executive Coaches:** leverage, constraint, bottleneck, throughput, compounding, capacity, flywheel, friction, iteration, scalable

**Healing and Transformation Coaches:** window_of_tolerance, dysregulation, nervous_system, rupture, breakthrough, somatic, activation, completion, witnessing, attunement

**Financial Freedom Coaches:** spreadsheet, dividend, constraint, timeline, compounding, net_worth, cash_flow, asset, leverage, iteration

---

## Section 5 — The 12 Visual Recipe Protocol Library

### 5.1 Library Overview

**Dependency ID:** DEP-VIS-002
**Format:** YAML
**Queried By:** Abel (template assignment), Conscious Canva App (template loading), RunningHub integration (workflow ID mapping)

### 5.2 Recipe Protocol Specifications

#### RECIPE-001: Relief Peak Carousel

```yaml
protocol_id: "relief_peak_carousel_recipe"
format: "carousel"
aspect_ratio: "4:5"
canvas_dimensions: "1080x1350"
visual_styles_permitted: ["cinematic_color_graded", "semi_realistic_digital"]
arc_type: "tension_release"
slide_count:
  minimum: 4
  default: 5
  maximum: 6
semiotic_injection_position: "latter_third — exhale moment, typically penultimate slide"
chromatic_bloom:
  slides_1_to_2: {saturation_pct: "30-40", temperature: "cool_dominant"}
  slide_climax: {saturation_pct: "68-78", temperature: "warm_entry — first warm light in sequence"}
  slides_final: {saturation_pct: "60-68", temperature: "warm_stable"}
pad_requirements:
  struggle_slides: {pleasure: "2-4", arousal: "4-6", dominance: "1-3"}
  resolution_slides: {pleasure: "6-7", arousal: "2-3", dominance: "6-7"}
typography_arc:
  tension: {category: "serif", weight: "700-900"}
  build: {category: "sans_serif_medium", weight: "500-600"}
  climax: {category: "sans_serif_bold", weight: "700"}
  resolution: {category: "sans_serif_light", weight: "300-400", tracking: "+3pct"}
first_person_pov_slides: [1, 2]
semiotic_injection: "climax_slide_only"
accumulation_prohibition: false
peak_end_priority:
  peak_slide: "semiotic_injection_slide"
  end_slide_standalone_required: true
coach_handle_bar: "final_slide_only"
template_ids:
  semi_realistic: "TPL-RELIEF-PEAK-SEMI-001"
  cinematic: "TPL-RELIEF-PEAK-CINE-001"
runninghub_workflow_ids:
  semi_realistic: "RH-WF-CAROUSEL-SEMI-001"
  cinematic: "RH-WF-CAROUSEL-CINE-001"
```

#### RECIPE-002: Dopamine Cliff Carousel

```yaml
protocol_id: "dopamine_cliff_recipe"
format: "carousel"
aspect_ratio: "4:5"
canvas_dimensions: "1080x1350"
visual_styles_permitted: ["cinematic_color_graded", "semi_realistic_digital"]
arc_type: "accumulation_cliff"
slide_count:
  minimum: 5
  default: 6
  maximum: 7
accumulation_slides: "slides_1_through_3_minimum"
cliff_slide_position: "slide_4_minimum — latter_third principle"
chromatic_bloom:
  accumulation: {saturation_pct: "55-90", temperature: "warm_progressive", direction: "increasing_per_slide"}
  cliff: {saturation_pct: "15-25", temperature: "cold_shock", direction: "maximum_drop"}
  resolution: {saturation_pct: "62-70", temperature: "warm_stable"}
accumulation_prohibition:
  enabled: true
  prohibited_elements:
    - "completed_metrics_or_dashboards"
    - "testimonials_showing_finished_results"
    - "after_photography_any_kind"
    - "awards_certificates_achievements"
    - "environmental_completeness_organized_clean"
    - "static_authority_poses_composed_stillness"
  required_elements:
    - "motion_vector_toward_goal_not_arrival"
    - "approach_state_in_progress"
coach_handle_bar: "final_slide_only"
template_ids:
  semi_realistic: "TPL-DOPAMINE-CLIFF-SEMI-001"
  cinematic: "TPL-DOPAMINE-CLIFF-CINE-001"
runninghub_workflow_ids:
  default: "RH-WF-CAROUSEL-CLIFF-001"
```

#### RECIPE-003: 9-Grid Accumulation

```yaml
protocol_id: "nine_grid_recipe"
format: "single_image_grid"
aspect_ratio: "4:5"
canvas_dimensions: "1080x1350"
visual_styles_permitted: ["semi_realistic_digital", "cinematic_color_graded"]
arc_type: "accumulation_wanting"
grid_layout: "3x3"
grid_rule: "all_9_frames_show_wanting_without_completion — same prohibition list as Dopamine Cliff"
label_position: "center_frame_text_only — minimal, 1-2 words maximum"
accumulation_prohibition: true
coach_handle_bar: false
template_ids:
  default: "TPL-9GRID-001"
runninghub_workflow_ids:
  default: "RH-WF-GRID9-001"
```

#### RECIPE-004: Listicle Visual

```yaml
protocol_id: "listicle_visual_recipe"
format: "carousel"
aspect_ratio: "4:5"
canvas_dimensions: "1080x1350"
visual_styles_permitted: ["cinematic_color_graded", "semi_realistic_digital"]
subtypes: ["curiosity_intriguing", "funny_relatable", "nostalgia", "outrageous", "fear_anxiety", "hope_inspiration"]
arc_type: "discovery_revelation"
slide_count:
  minimum: 3
  default: 5
  maximum: 6
semiotic_injection_position: "latter_third — revelation moment, typically second-to-last slide"
zeigarnik_requirement: "tribe_specific_incomplete_artifact_on_tension_slides"
climactic_item_rule: "most_powerful_item_at_semiotic_injection_position — not saved for last"
mood_setter_rule: "slide_1_establishes_complete_emotional_world_before_list_items_begin"
note: "funny_relatable subtype — humor mechanism specified via Memetic Engine, visual style is semi_realistic, NOT Ghibli"
coach_handle_bar: "final_slide_only"
template_ids:
  base: "TPL-LISTICLE-001"
runninghub_workflow_ids:
  default: "RH-WF-LISTICLE-001"
```

#### RECIPE-005: Visual Timeline

```yaml
protocol_id: "visual_timeline_recipe"
format: "carousel"
aspect_ratio: "4:5"
canvas_dimensions: "1080x1350"
visual_styles_permitted: ["cinematic_color_graded", "semi_realistic_digital"]
arc_type: "discovery_revelation"
slide_count:
  minimum: 7
  default: 8
  maximum: 9
semiotic_injection_position: "latter_third — climax moment in timeline progression"
chronological_color_arc: "environment_color_temperature_tracks_timeline — past slides cooler, present warmer, future warmest"
coach_handle_bar: "final_slide_only"
template_ids:
  default: "TPL-TIMELINE-001"
runninghub_workflow_ids:
  default: "RH-WF-TIMELINE-001"
```

#### RECIPE-006: Comparison

```yaml
protocol_id: "comparison_archetypes_recipe"
format:
  single_contrast: "single_image"
  multiple_contrasts: "carousel"
aspect_ratio: "4:5"
canvas_dimensions: "1080x1350"
visual_styles_permitted: ["cinematic_color_graded", "semi_realistic_digital"]
arc_type: "contrast_resolution"
slide_count_carousel:
  minimum: 2
  default: "one_slide_per_contrast_pair_plus_resolution"
  maximum: "no_hard_limit — determined_by_number_of_comparisons"
gaze_architecture_rule: "FACE PRIORITY TRAP PREVENTION — when two characters appear in the same frame, Side A character gaze toward upper center, Side B character gaze toward lower center. Creates X-pattern not collision. NEVER both characters facing center simultaneously."
background_primary_signal_rule: "Background color carries primary emotional differentiation between the two states — not character expression alone. Background processes 25ms before character."
coach_handle_bar:
  single_image: true
  carousel_final_slide: true
  carousel_interior_slides: false
template_ids:
  single_image: "TPL-COMPARISON-SINGLE-001"
  carousel: "TPL-COMPARISON-CAROUSEL-001"
runninghub_workflow_ids:
  default: "RH-WF-COMPARISON-001"
```

#### RECIPE-007: Conceptual Contrast

```yaml
protocol_id: "conceptual_contrast_recipe"
format:
  philosophical_simultaneous: "single_image"
  transformational_sequential: "carousel"
aspect_ratio: "4:5"
canvas_dimensions: "1080x1350"
visual_styles_permitted: ["cinematic_color_graded", "semi_realistic_digital"]
arc_type: "contrast_resolution"
format_selection_rule: "Simultaneous activation is more powerful than sequential argument for philosophical recognition — use single image. Transformation requiring sequential understanding — use carousel."
background_primary_signal_rule: "Background color carries the primary emotional differentiation — not character expression alone."
coach_handle_bar:
  single_image: true
  carousel_final_slide: true
template_ids:
  simultaneous: "TPL-CONTRAST-SINGLE-001"
  sequential: "TPL-CONTRAST-CAROUSEL-001"
runninghub_workflow_ids:
  default: "RH-WF-CONTRAST-001"
```

#### RECIPE-008: Observational Humor

```yaml
protocol_id: "observational_humor_recipe"
format: "single_image"
aspect_ratio: "4:5"
canvas_dimensions: "1080x1350"
visual_style: "ghibli_illustration OR cartoon_stylization — REQUIRED regardless of TII"
style_rationale: "Stylization creates psychological safety for benign violation perception. Realism removes the safety buffer — the humor mechanism fails."
arc_type: "benign_violation_recognition"
slide_count: 1
fluency_priority: "maximum — micro-smile must activate before text is read"
coach_handle_bar: true
template_ids:
  ghibli: "TPL-OBS-HUMOR-GHIBLI-001"
  cartoon: "TPL-OBS-HUMOR-CARTOON-001"
runninghub_workflow_ids:
  ghibli: "RH-WF-SINGLE-GHIBLI-001"
```

#### RECIPE-009: Worst Case Scenario

```yaml
protocol_id: "worst_case_scenario_recipe"
format: "single_image"
aspect_ratio: "4:5"
canvas_dimensions: "1080x1350"
visual_style: "desaturated_cinematic_realism — REQUIRED regardless of TII"
style_rationale: "Credibility of the possible must be maintained for fear-reality mechanism. Stylization allows viewer to dismiss scenario as fantasy — mechanism fails. Dual signal: fear from content + micro-smile from fluency fires simultaneously. Fluency specification is MORE critical here than any other recipe."
arc_type: "fear_recognition"
slide_count: 1
saturation_spec: "desaturated — 20-35% maximum"
fluency_priority: "maximum"
coach_handle_bar: true
template_ids:
  default: "TPL-WCS-CINE-001"
runninghub_workflow_ids:
  default: "RH-WF-SINGLE-CINE-DESAT-001"
```

#### RECIPE-010: Poll Visuals

```yaml
protocols:
  - "poll_visual_recipe"
  - "archetypical_poll_recipe"
  - "controversial_dilemma_poll_recipe"
  - "would_you_rather_recipe"
format: "single_image"
aspect_ratio: "9:16"
canvas_dimensions: "1080x1920"
visual_styles_permitted: ["graphic_vector_illustration", "semi_realistic_digital"]
arc_type: "contrast_recognition"
note: "All poll variants are single image. Archetypical Poll is NOT a carousel. Poll format requires high graphic readability at phone screen size in vertical format."
face_priority_trap_rule: "Applied when two character options appear — gaze vectors must not create mutual collision"
coach_handle_bar: false
note_handle: "9:16 format has insufficient space for coach handle bar — omitted on all poll formats"
template_ids:
  stereotypical: "TPL-POLL-STEREO-001"
  archetypical: "TPL-POLL-ARCH-001"
  dilemma: "TPL-POLL-DILEMMA-001"
  would_you_rather: "TPL-POLL-WYR-001"
runninghub_workflow_ids:
  default: "RH-WF-POLL-001"
```

#### RECIPE-011: Tweet-Style Quote

```yaml
protocol_id: "tweet_quote_recipe"
format: "single_image"
aspect_ratio: "4:5"
canvas_dimensions: "1080x1350"
visual_styles_permitted: ["cinematic_color_graded", "semi_realistic_digital"]
arc_type: "identity_declaration"
slide_count: 1
text_dominant: true
note: "Text is the primary visual element. Background and character serve the text — not the reverse. Maximum visual simplicity to maximize fluency."
coach_handle_bar: true
template_ids:
  default: "TPL-TWEET-QUOTE-001"
runninghub_workflow_ids:
  default: "RH-WF-SINGLE-QUOTE-001"
```

#### VIDEO RECIPE PROTOCOLS (Visual Brief Export Only)

```yaml
video_only_formats:
  - "case_study_recipe"
  - "debunking_myths_scams_recipe"
  - "recognition_story_reel_recipe"
  - "tier_list_hybrid_recipe"
  - "reaction_recipe"

output_type: "visual_brief_export"
no_image_generation: true
output_format: "structured_art_direction_document"
document_contains:
  - "scene_by_scene_composition_brief"
  - "lighting_grammar_per_scene"
  - "character_position_and_expression_per_scene"
  - "b_roll_guidance"
  - "text_overlay_specification_per_scene"
  - "color_grading_direction"
note: "Case Studies and Myth Debunking are video formats. No carousel or single image production occurs for these archetypes."
```

---

## Section 6 — The 30 Visual Design Architecture Specifications

Each specification names: the mechanism, the production failure if ignored, the system component enforcing it, and the pipeline integration point.

### Group A — Lighting and Chromatic Grammar

**SPEC-01 — Cinematographic Lighting Grammar**

*Mechanism:* Lighting direction, Kelvin temperature, and shadow opacity must be specified simultaneously as a unified grammar — not isolated variables. A 3000K CCT at 750 lux produces the lowest measurable mental workload. 6500K increases alertness but risks visual fatigue. The light-from-above neurological bias is universal but modulated by reading direction — right-to-left readers show reversed lateral lighting bias, making the upper-left key light convention culturally non-universal.

*Production failure if ignored:* Brief reads "warm cinematic feel" — RunningHub samples the center of its training distribution and produces the coaching photography average.

*System enforcement:* Abel populates the `lighting_grammar` field using natural language cinematographic description for every slide. Paradoxe validates completeness before compiling the RunningHub prompt. Gate C-09 rejects any VCB slide with a lighting_grammar field containing only adjectives and no temporal signal or shadow specification.

*Integration point:* VCB lighting_grammar field → Paradoxe prompt compilation → RunningHub prompt string

---

**SPEC-02 — Color Assignment by Archetype Angle**

*Mechanism:* Elliot and Maier's color-in-context research proves the same hue produces opposite motivational responses depending on semantic framing. Red in achievement contexts fires avoidance motivation. Orange fires approach motivation AND moral norm violation signal — the correct color for indignation-angle content. Red is reserved exclusively for fear-anxiety angles where avoidance IS the intended response.

*Production failure if ignored:* Debunking Myths content uses red for urgency. Viewer's nervous system reads "I am failing" rather than "wrong is being named." Engagement damaged before content is processed.

*System enforcement:* DEP-VIS-002 specifies color-angle rules per recipe. Abel reads both recipe protocol AND emotional angle from the script JSON before setting chromatic spec. Color selection is never a standalone decision.

*Integration point:* Script JSON emotional_angle → Abel color-angle lookup in DEP-VIS-002 → VCB chromatic_spec → RunningHub prompt

---

**SPEC-03 — Chromatic Bloom Sequence**

*Mechanism:* Background color processes 25ms before shape, face, or text in a static image. In a carousel, this creates a pre-cognitive emotional arc running parallel to the content arc. Transitioning from achromatic to chromatic stimuli elicits significantly greater prefrontal and orbitofrontal cortex activation than the reverse. The body reads the color arc before the eyes reach the words.

*Production failure if ignored:* Random color assignments per slide. The viewer's body receives contradictory pre-cognitive loading. The peak lands flat because the body was not pre-loaded into the right state.

*System enforcement:* Every carousel recipe protocol in DEP-VIS-002 includes a `chromatic_bloom` specification — saturation percentage and temperature direction per slide position. Abel writes `saturation_pct` and `saturation_direction` as required numeric fields per slide.

*Integration point:* DEP-VIS-002 chromatic_bloom spec → VCB chromatic_spec per slide → Paradoxe → RunningHub prompt

---

**SPEC-04 — Accumulation: Wanting Without Completion**

*Mechanism:* The mesolimbic wanting pathway and the opioid liking pathway operate independently. Wanting activates on approach toward reward. Once arrival is shown, liking's satiety mechanism fires and desire habituates. High-aspiration stimuli maintain sustained Late Positive Potential (LPP) ERP amplitudes specifically when showing approach, not completion. A single completion image collapses the entire LPP build that preceded it.

*Production failure if ignored:* A client testimonial on slide 2 of the Dopamine Cliff shows a completed success story. Desire habituates immediately. The cliff lands against a body no longer in approach state.

*System enforcement:* The Accumulation Prohibition Checklist (`accumulation_prohibition_audit`) is a required VCB field for all Dopamine Cliff and 9-Grid compositions. Prohibited elements list is hardcoded in DEP-VIS-002 and cannot be overridden. Gate C-09 validates no prohibited elements appear in any accumulation slide's visual congruent specifications.

*Integration point:* DEP-VIS-002 prohibition list → Abel VCB checklist execution → Gate C-09 validation → PSSL Completeness Gate blocks VCBs with failed audit

---

**SPEC-05 — Chromatic Bloom: Saturation as Numbered Specification**

*Mechanism:* Saturation is a numbered specification in the VCB, not a mood description. Each slide receives a specific saturation percentage based on its arc stage. High saturation (85-90%) is reserved for the accumulation peak and the semiotic injection slide. Desaturation (15-25%) signals the cliff or maximum emotional restriction. Resolution returns to warm stable 62-68%.

*Production failure if ignored:* Designer estimates "vibrant" for peak slides. Actual saturation is 65% because the estimation was made against the previous slide, not against the arc specification. The peak fails to land with full physiological impact.

*System enforcement:* Saturation percentage is a required numeric field in the VCB `chromatic_spec`. Non-numeric values fail Gate C-09. Post-generation, the Visual Validation Agent verifies saturation alignment using image analysis.

*Integration point:* VCB chromatic_spec.saturation_pct → Paradoxe → RunningHub prompt parameter

---

### Group B — Somatic Architecture

**SPEC-06 — Arc Type as Foundational Brief Decision**

*Mechanism:* Four carousel arcs produce distinct biometric trajectories: Tension-Release (A-process tension then B-process HRV increase), Discovery-Revelation (sustained Beta + progressive GSR peaks), Contrast-Resolution (corrugator activation then zygomaticus activation), Accumulation-Cliff (escalating LPP then acute GSR spike at cliff). Everything — lighting, color, typography, PAD scores, chromatic bloom — derives from the declared arc type.

*Production failure if ignored:* Visual parameters are selected by recipe convention without arc type confirmation. The somatic arc collapses into incoherence.

*System enforcement:* Arc type is the first field Abel reads from the script JSON package. Mismatch with recipe protocol triggers an operator flag before composition proceeds. Arc type is a required field in the VCB with no default value.

*Integration point:* Script JSON arc_type → Abel confirmation check against DEP-VIS-002 → VCB arc_type → all downstream parameter generation

---

**SPEC-07 — Environmental Grammar for Somatic Recognition**

*Mechanism:* Damasio's somatic marker hypothesis confirms environments trigger body-memory through environmental grammar — the syntax of light quality, spatial density, and temporal signals — not surface similarity. An 11pm kitchen triggers somatic recognition because overhead institutional light + high object density + temporal stillness matches the autobiographical body-memory of late-night problem-solving. This fires measurably different SCR signatures than intellectual recognition.

*Production failure if ignored:* Stage set is specified as "coaching struggle scene" — AI generates a stock-photography tired person against a white background. Intellectual recognition fires but somatic recognition does not. The Relief Peak never reaches full physiological depth.

*System enforcement:* Abel queries DEP-VIS-003 using PAD score requirements, not aesthetic categories. Every stage set specification in the VCB must include all five grammar parameters: light quality (time-of-day signal), spatial density (object count), temporal signal, world color temperature, and subject-to-frame height ratio.

*Integration point:* PAD score requirements → DEP-VIS-003 library query → VCB environmental_grammar fields → Paradoxe → RunningHub prompt

---

**SPEC-08 — PAD Framework: All Three Dimensions Required**

*Mechanism:* The PAD (Pleasure-Arousal-Dominance) framework's Dominance dimension is the most underspecified element in coaching visual content. High-dominance environments communicate the subject controls the world. Low-dominance environments communicate the subject is contained by the world. Menzies' pictorial architecture principle — subordinating the human figure to the larger graphic structure — is the validated mechanism for environments that feel psychologically inevitable. AI-generated environments fail specifically on Dominance.

*Production failure if ignored:* Struggle slides accidentally place the coach in high-dominance environments because "it looks professional." The body reads authority and control where it should read overwhelm and restriction.

*System enforcement:* DEP-VIS-003 contains PAD scores for every stage set. Abel specifies PAD target ranges per slide position in the VCB. Stage set selection from DEP-VIS-003 filters exclusively by PAD range match — not by aesthetic similarity.

*Integration point:* Recipe protocol PAD requirements → Abel PAD range specification → DEP-VIS-003 library filter → VCB environmental_grammar.pad_scores

---

**SPEC-09 — Tribe-Specific Incompleteness**

*Mechanism:* The Zeigarnik Effect only creates persistent cognitive tension when the incomplete task is personally relevant. Generic visual incompleteness produces mild visual interest. Tribal incompleteness — an artifact the viewer has a specific embodied relationship with, left unfinished — activates working memory persistence because their cognitive system recognizes the task as genuinely unresolved. The open loop is felt, not observed.

*Production failure if ignored:* Tension slides show generic incompleteness signals — an unfinished diagram, a blurred future. Visual metaphors, not tribal artifacts. No persistent pull toward the next slide.

*System enforcement:* Abel populates `incomplete_tribal_artifact` for every tension slide using tribal context from the script JSON + DEP-ENG-007. The field cannot be null for tension slides — null triggers a Gate C-09 failure.

*Integration point:* Script JSON tribal_context → Abel tribal artifact query → VCB incomplete_tribal_artifact field → Paradoxe → RunningHub scene composition

---

**SPEC-10 — Semiotic Injection: Latter Third Positioning**

*Mechanism:* The emotional climax — facial expression injection, maximum chromatic intensity, identity declaration — belongs in the latter third of the sequence, not the midpoint. This is supported by three converging research principles: the Peak-End Rule (peak moment determines remembered experience disproportionately), micro-commitment investment (the body is more physiologically receptive after accumulated swipe investment), and Opponent Process Theory (tension needs sufficient build before the B-process fires). The precise position within the latter third is determined by arc type and story logic, not by formula.

Arc type positioning:
- Tension-Release: exhale moment — typically penultimate slide
- Accumulation-Cliff: cliff moment — typically slide 4 of 5, or slide 5 of 7
- Discovery-Revelation: revelation — typically second-to-last slide
- Contrast-Resolution: resolution slide

*Production failure if ignored:* Emotional climax placed at the midpoint. The peak fires before the body has accumulated sufficient investment. Physiological impact is reduced.

*System enforcement:* Abel determines semiotic_injection_slide using arc type + story logic, and records the rationale in `semiotic_injection_rationale` field of the VCB. The field includes both the slide number and the reason — not a formula output. Gate C-09 checks that semiotic_injection_slide is not the first or second slide of any sequence with 4+ slides.

*Integration point:* VCB arc_type + slide count → Abel positioning decision → VCB semiotic_injection_slide + rationale → Paradoxe expression injection trigger

---

**SPEC-11 — Peak-End Rule: Two Priority Slides**

*Mechanism:* The remembered experience of a carousel is determined by the most intense moment (the peak) and the final moment (the end). Duration neglect means intermediate slides are almost irrelevant to remembered quality. A 9-slide carousel with a powerful peak and weak final slide is remembered worse than a 5-slide carousel with a strong peak and strong final slide.

*Production failure if ignored:* The carousel is optimized for information flow. The final slide is a generic CTA template. The remembered experience is "follow me for more content." No save behavior. No DM.

*System enforcement:* DEP-VIS-002 marks the peak slide (semiotic injection position) and the final slide with `peak_end_rule_priority: HIGH`. Abel adds this flag to both slides in the VCB. The final slide receives `standalone_validity: true` and `screenshot_shareable: true` flags — both must be achievable from the VCB specification before production proceeds.

*Integration point:* VCB slide flags → Paradoxe priority specification → RunningHub → Visual Validation Agent screenshot_shareable check

---

**SPEC-12 — Corrugator as Semantic Conflict Signal**

*Mechanism:* The corrugator supercilii activates specifically in response to goal-relevant vs. goal-irrelevant information conflict — situations where what the viewer wants and what they are seeing are in tension. This fires when the viewer's aspirational self-identity is confronted by the depicted reality. Semantic conflict produces sharper, more personally resonant corrugator activation than visual content that merely depicts difficulty.

*Production failure if ignored:* Struggle slides are dark and difficult visually, producing mild corrugator activation through negative valence alone. A semantically conflicting image — showing the exact gap between tribal identity aspiration and current reality — produces the specific corrugator response that creates persistent tension and drives swipe continuation.

*System enforcement:* Abel populates `semantic_conflict_spec` in the VCB for every tension slide: naming both the viewer's aspirational state AND the reality depicted. Paradoxe uses this to compose the scene brief — the conflict is specified, not left to chance.

*Integration point:* Script JSON tribal_context.audience_recognition_context → Abel semantic conflict specification → VCB semantic_conflict_spec → Paradoxe scene composition

---

### Group C — Typography and Processing Systems

**SPEC-13 — Typography-Arc Synchronization**

*Mechanism:* Font weight communicates arousal level independently of semantic content. Bold weights prime corrugator activation. Light weights activate processing fluency and prime the zygomaticus micro-smile. Fonts approximating the 1/f spatial frequency distribution minimize visual fatigue and maximize the fluency response — applicable specifically to resolution slides.

*Production failure if ignored:* Bold serif used throughout the entire carousel for "brand consistency." Resolution slide delivers the exhale content in the same high-arousal typographic register as tension slides. The body never receives the fluency signal. The exhale doesn't happen.

*System enforcement:* Typography specification in the VCB is derived from arc stage per slide — not brand guidelines. Arc stage → typography mapping is hardcoded in DEP-VIS-002. Brand-consistent typography applies only to elements outside the primary text zone.

*Integration point:* VCB arc_stage per slide → DEP-VIS-002 typography mapping → VCB typography field → Paradoxe → Canva App text layer specification

---

**SPEC-14 — Processing Fluency: Resolution Slide Font Requirements**

*Mechanism:* Processing fluency triggers zygomaticus major activation below conscious awareness. This physiological response is misattributed to the content — the viewer feels the brand is more trustworthy and likeable without knowing why. Resolution slides must maximize fluency signal to complete the physiological exhale.

*Production failure if ignored:* Decorative serif font used on resolution slides for visual consistency. Processing disfluency fires mild corrugator response. The physiological exhale never completes.

*System enforcement:* Resolution arc stage slides receive mandatory font requirements in VCB typography field. Gate C-09 checks resolution slides specifically for font_weight ≤ 500 and font_category "sans_serif." Resolution slides specifying weight > 500 fail the completeness check and require revision.

*Integration point:* VCB arc_stage "resolution" flag → Gate C-09 weight check → Canva App text layer → final composition

---

**SPEC-15 — Six-Word Law with Concrete Noun Requirement**

*Mechanism:* Paivio's Dual Coding Theory requires concrete nouns to activate both verbal and imagery systems simultaneously. Abstract words only fire the verbal system. The 6-word law is not just a word count — it requires minimum 3 of 6 words to be concrete nouns or action verbs activating dual-coding. Ghost nouns ("freedom," "purpose," "impact") count as words but do not count toward the concrete noun requirement.

*Production failure if ignored:* Hook text reads "Our happiness is primarily based on our gratitude." Nine words, zero dual-coding activation. Behavioral recognition at best.

*System enforcement:* TIAR query returns only concrete nouns with active decay status. Script generation skills receive these as required vocabulary. VCB typography primary_text field has a `primary_word_count` maximum of 6 and a `concrete_noun_count` minimum of 3. Gate C-09 validates this ratio. Any primary text failing the ratio is flagged for revision before RunningHub execution.

*Integration point:* TIAR active noun list → Script Generation Skill injection → Script JSON hook_concrete_nouns → Abel VCB validation → Gate C-09

---

### Group D — Linguistic-Visual Congruence System

**SPEC-16 — Tribal Noun + Visual Congruent Pairing**

*Mechanism:* Identity-level recognition — the "I know you" response that drives saves and DMs — requires simultaneous activation of both the verbal system (tribal noun) and the imagery system (congruent visual element). When both fire simultaneously, the response is identity-level recognition ("that is exactly who I am"). Neither the word alone nor the image alone produces the identity-level Gamma ignition. The pairing does.

*Production failure if ignored:* Text says "the 3am spiral." Visual shows a generic stressed person at a laptop with morning light. Noun fires correctly. Visual fires generic "stressed person" recognition. No dual-coding simultaneity. Post performs adequately but never creates the "how did they know?" response.

*System enforcement:* Abel populates `tribal_noun_visual_congruent` pairs for every text slide. The congruent description must be a scene grammar specification — the exact environmental and compositional elements that match the noun's tribal meaning. Any congruent description containing the words "generic," "typical," "standard," or "person looking" fails Gate C-09 and requires revision.

*Integration point:* TIAR visual_congruent_mappings → Abel pairing generation → VCB tribal_noun_visual_congruent → Paradoxe → RunningHub environmental composition

---

**SPEC-17 — TIRS Integration Upstream in Script Generation Skills**

*Mechanism:* The TIAR's primary integration point is inside Script Generation Skills — not inside the visual pipeline. Concrete nouns must be selected with tribal charge at script generation. The visual pipeline's TIAR query is a confirmation check, not the first point of tribal validation. This architectural decision is what makes script-visual congruence coherent — both are built from the same tribal vocabulary.

*Production failure if ignored:* Script generation proceeds without TIAR query. Script uses "freedom," "abundance," "authentic" — high-entropy expired nouns. The visual recipe builds perfect congruents for expired vocabulary. The content performs adequately and moves no one.

*System enforcement:* Script Generation Skill YAML templates include mandatory `tiar_query` pre-generation step. Active and expired noun lists are injected into hook generation instructions. Receipt Chain Guard logs the TIAR query result as part of the script compilation audit trail.

*Integration point:* Script Generation Skill YAML → TIAR query → active/expired noun list injection → script hook → script JSON hook_concrete_nouns → Abel confirmation

---

### Group E — Character and Cast Systems

**SPEC-18 — Gaze Geometry: Dual-Vector Specification**

*Mechanism:* Langton's research established the joint attention mechanism requires two congruent signals simultaneously: iris eccentricity (pupil position within visible iris) AND face eccentricity (feature position within head contour). In stylized illustration, large simplified eyes make iris eccentricity ambiguous. A head turned 20° left with centered pupils reads as looking forward. The mechanism fails silently.

*Production failure if ignored:* Character described as "looking toward the hook text" with head turned left. Illustration character has pupils drawn centered in large eyes. Joint attention mechanism fails. The viewer's eye does not transfer to the text zone. The hook is invisible.

*System enforcement:* Abel populates two required character_spec fields: `head_rotation_degrees` (numeric) and `pupil_position_ratio_pct` (numeric). "Looking toward the text" is not valid — rejected by Gate C-09. For illustrated styles, Paradoxe's prompt includes: "pupils clearly offset toward the specified edge of the visible iris area, not centered."

*Integration point:* VCB character_spec.head_rotation_degrees + pupil_position_ratio_pct → Paradoxe → RunningHub character generation prompt

---

**SPEC-19 — Character Consistency via Image Reference Architecture**

*Mechanism:* AI image editing models can reproduce a specific face from a reference image with high fidelity, maintaining identity-critical features across different environments and expressions. AI-generated faces are more consistently reproduced than real photographs because they lack authentic micro-variation. Identity-critical features (iris color and shape, eyebrow geometry, facial proportions, skin texture approach) must never vary. Identity-neutral features (background, lighting, pose) vary freely per recipe and arc stage.

*Production failure if ignored:* Every generation session produces subtle character drift. Across 36 pieces per week, the cast never quite looks the same. Parasocial attachment formation never builds.

*System enforcement:* DEP-VIS-004 stores the canonical reference image per cast character. Abel includes the reference image URL in the VCB character_spec. RunningHub receives the reference image alongside the prompt. Gate C-09 rejects any VCB slide with a named character missing a DEP-VIS-004 reference URL.

*Integration point:* DEP-VIS-004 reference archive → Abel VCB character_spec.reference_url → RunningHub API reference_image parameter

---

**SPEC-20 — Avatar Authenticity: Eight-Feature Hierarchy**

*Mechanism:* A 508-participant study identified eight micro-level visual cues predicting AI portrait authenticity, ranked by predictive strength. Facial features dominate: Expression Naturalness (eye-mouth congruence), Facial Proportion (geometric reasonableness), Skin Texture (pore-level detail). "Perfect" AI visuals are perceived as less trustworthy than "imperfect but plausible" ones. Intentional asymmetry and visible imperfection signal "real world."

*Production failure if ignored:* Smooth, symmetrical, technically perfect avatar images trigger a sub-threshold "constructed" somatic marker. Trust formation slows without the coach consciously identifying why.

*System enforcement:* Abel populates three mandatory authenticity parameters in VCB character_spec: `expression_congruence_check` (eye-mouth congruent — not just mouth), `skin_texture` (visible pore detail required — "smooth" invalid), `intentional_asymmetry` (one specific asymmetry named). Post-generation, the Visual Validation Agent runs a 6-point authenticity checklist. Failures at items 1-3 trigger regeneration.

*Integration point:* VCB character_spec authenticity params → Paradoxe → RunningHub → Visual Validation Agent post-generation check → regeneration loop or approval

---

**SPEC-21 — Documentary Authenticity Effect**

*Mechanism:* "Perfect" AI visuals paradoxically signal "constructed" through their very perfection. Minor authentic imperfections activate somatic markers signaling "this is from a real world" before any conscious evaluation. Intentional imperfection is a trust architecture specification, not a quality failure.

*Production failure if ignored:* All compositions generated at maximum technical quality. The somatic marker "constructed" fires below conscious threshold. Trust formation slows across the entire feed.

*System enforcement:* VCB contains a required `intentional_imperfection` field per slide. For cinematic realism: one named environmental irregularity. For illustration: intentional line weight variation, one less-resolved element. "None" is not a valid value. Paradoxe incorporates the imperfection specification into the RunningHub prompt.

*Integration point:* VCB intentional_imperfection field → Paradoxe → RunningHub prompt → Visual Validation Agent imperfection confirmation

---

**SPEC-22 — Visual Style Selection by Format and Relationship Stage**

*Mechanism:* Style is constrained first by format (carousels cannot use Ghibli — cinematic or semi-realistic only), then by archetype override rules (Worst Case Scenario always cinematic; Observational Humor always Ghibli for single image), then by TII score. At low TII (cold audience), Fogg's credibility research confirms photorealism fulfills the authentication contract. At high TII (warm audience), illustrated stylization facilitates deeper transportation and identity projection.

*Production failure if ignored:* Ghibli style applied to a carousel. The illustration grammar's psychological safety mechanism — which works in single image by creating a complete emotional world the viewer enters simultaneously — breaks across sequential carousel slides because it reduces the somatic recognition that tension slides require.

*System enforcement:* Format constraint check runs first in Abel's style selection. Carousel format → cinematic or semi-realistic only, regardless of TII or any other parameter. This constraint is hardcoded and cannot be overridden.

*Integration point:* VCB visual_output_type format constraint → Abel style selection → VCB visual_style field → template selection in DEP-VIS-002 → RunningHub workflow ID

---

### Group F — Production Quality Gates

**SPEC-23 — First-Person POV Architecture**

*Mechanism:* First-person perspective elicits stronger somatic presence and higher SCR elevation than third-person in high-fidelity imagery. It eliminates the observer and places the viewer inside the experience. Used specifically on struggle slides to amplify pain-state recognition that powers the Relief Peak arc.

*Production failure if ignored:* Struggle slides use third-person perspective — viewer watches a stressed person. Intellectual recognition fires. Somatic recognition does not. The Relief Peak builds on an intellectual foundation, not a somatic one.

*System enforcement:* DEP-VIS-002 specifies `first_person_pov_slides` per recipe protocol. Abel includes `first_person_pov: true/false` per slide in the VCB. When true, Paradoxe switches to first-person composition directives: hands in frame at bottom, subject environmental elements at eye level, no full-body character visible.

*Integration point:* DEP-VIS-002 first_person_pov_slides → VCB per-slide flag → Paradoxe composition directive → RunningHub camera perspective specification

---

**SPEC-24 — Aspect Ratio as Social Contract**

*Mechanism:* The Visual Grammar framework establishes image format creates an Interpersonal Metafunction — a social relationship contract. Portrait 4:5 creates intimacy and scale dominance (image enters personal space — the dominant format for coaching content). 9:16 creates full-screen immersion appropriate for poll binary choices. The 4:5 format is the default for all coaching content because the coach handle bar at the top and the full composition in the remaining space creates the correct proportional relationship between the brand signal and the content.

*Production failure if ignored:* Square format used for intimate emotional disclosure. The equal proportional relationship creates a peer dynamic when the content requires the image to address the viewer directly. 9:16 used for a complex carousel — the format loses the horizontal pan grammar.

*System enforcement:* Abel assigns `aspect_ratio` from the routing table in DEP-VIS-002. 4:5 is the default for carousels and standard single images. 9:16 is the mandatory format for all poll variants. No other aspect ratios are currently in the CVE template library.

*Integration point:* DEP-VIS-002 routing table → Abel aspect_ratio assignment → VCB aspect_ratio → Canva App canvas configuration → RunningHub output dimensions

---

**SPEC-25 — Cultural Color Architecture**

*Mechanism:* Color-in-context research was conducted on Western cohorts. The leftward lighting bias is reversed for right-to-left readers. White signals mourning in East Asian cultural contexts. Red signals fortune in Chinese contexts. Yellow signals wealth and fertility in West African contexts. Green signals sacred authority in Islamic contexts. These are documented differences in emotional meaning through lifetime exposure — not surface cultural variations.

*Production failure if ignored:* The color architecture matrix built on Western norms is applied to a coach with a predominantly West African diaspora audience. "White for clarity" triggers mourning associations. The physiological architecture built carefully in lighting and typography is undermined at the color layer.

*System enforcement:* DEP-ENG-002 (Audience Avatar) contains `primary_cultural_context`. Abel reads this before setting chromatic_spec. DEP-VIS-003 contains four cultural color profiles per mood state. Profile selection uses `primary_cultural_context` as the lookup key. Western profile is one of four equally valid options — not the default.

*Integration point:* DEP-ENG-002 cultural context → Abel profile selection → DEP-VIS-003 cultural color profiles → VCB chromatic_spec

---

**SPEC-26 — Motoric Vampire Effect: Seamless Swipe Imperative**

*Mechanism:* Counter-intuitive or friction-introducing gestures divert cognitive resources from content processing to motor control management — measurably reducing brand recall and message comprehension. The carousel sideways swipe works because it is consistent, predictable, and low-effort. The seamless horizontal format (all slides as a continuous world) reinforces this: the viewer moves through a world, not flips pages.

*Production failure if ignored:* Mixed formats within a single carousel sequence (a video slide, a poll slide) introduce navigation ambiguity. Each disruption triggers a motor allocation event reducing the depth of emotional arc processing.

*System enforcement:* DEP-VIS-002 defines format as immutable per recipe — no mixed formats within a single carousel sequence. The Canva App's template system enforces this at the layout level. Slide transition design preserves the seamless pan grammar — environmental elements bleeding across slide boundaries are specified in the template design brief.

*Integration point:* DEP-VIS-002 format immutability → Canva App template enforcement → seamless edge bleed in template design brief

---

**SPEC-27 — Micro-Commitment Investment Architecture**

*Mechanism:* Each carousel swipe is a micro-commitment under Cialdini's consistency principle. By slide 3, the viewer has made two micro-commitments — creating internal motivation to complete the sequence. This accumulated investment amplifies two effects: the physiological exhale on the Relief Peak slide is deeper (B-process amplified), and the GSR spike at the Dopamine Cliff is more intense (surprise violates established consistency).

*Production failure if ignored:* Carousel designed at 3 slides for "performance optimization." Insufficient micro-commitment investment for physiological mechanisms to operate at full depth. The 3-slide carousel delivers information. The 5-slide carousel with correct arc delivers a physiological experience.

*System enforcement:* DEP-VIS-002 specifies minimum slide counts per arc type based on micro-commitment thresholds. Accumulation-Cliff: minimum 5 slides. Tension-Release: minimum 4 slides. Discovery-Revelation: minimum 4 slides. Abel enforces these minimums when generating the VCB slide count.

*Integration point:* DEP-VIS-002 minimum slide counts → Abel slide count determination → VCB total_slides

---

**SPEC-28 — Parasocial Architecture: PSI vs PSR**

*Mechanism:* Research distinguishes Parasocial Interaction (PSI — momentary, triggered by direct gaze) from Parasocial Relationship (PSR — enduring cross-episode bond requiring character allure and narrative complexity). Content built for PSI only produces consistent but shallow engagement. The transition from audience to buyer requires PSR investment — a character whose decisions carry consequences across episodes and whose internal conflicts the viewer recognizes as meaningful.

*Production failure if ignored:* Every post built for immediate PSI — direct address, commanding presence, no continuity across episodes. Audience likes content but does not form attachment. Conversion is slow because there is no relational investment.

*System enforcement:* DEP-VIS-004 stores not just reference images but narrative role specifications per character: documented internal conflict, evolutionary arc position, relationship to protagonist. Abel checks the character's current arc position when specifying expression in the VCB — expressions must be arc-consistent across the content calendar, not just emotionally appropriate for the individual slide.

*Integration point:* DEP-VIS-004 character narrative state → Abel expression specification → VCB character_spec.expression

---

**SPEC-29 — AGSS: Anti-Generic Specificity Scale**

*Mechanism:* AI diffusion models converge on training data average through sharp transition behavior — settling into the most statistically common representation. "Authentic coaching environment" returns the coaching photography average: technically competent, psychologically inert. The AGSS measures the mathematical distance between a generated image's features and the generic center of the training distribution. High AGSS = the PSSL has successfully forced specificity.

*Production failure if ignored:* VCB is well-specified but Paradoxe translates it into prompt language that collapses specificity through generic vocabulary. RunningHub output is technically correct and emotionally average. The CVE produces content indistinguishable from every other coaching account.

*System enforcement:* Visual Validation Agent scores every generated image using the AGSS immediately after RunningHub delivery. Minimum threshold: 6.5/10. Images scoring below threshold are automatically returned to Paradoxe for prompt revision and one regeneration attempt. AGSS score is logged in the VPO record.

*Integration point:* RunningHub output → Visual Validation Agent AGSS scoring → threshold check → regeneration loop or approval → Notion delivery

---

**SPEC-30 — PSSL Brief Schema as Production Law**

*Mechanism:* AI diffusion models convert descriptive language into statistical averages. The PSSL prevents this by specifying parameters at low latent space density — forcing the model away from the center of its training distribution. Every visual parameter traces back to a documented physiological outcome. No visual element exists without a somatic justification.

*Production failure if ignored:* Briefs contain adjectives without measurable values. "Warm and powerful" returns the coaching photography statistical centroid. The system cannot be audited, cannot be improved, and cannot scale deterministically.

*System enforcement:* The VCB schema (DEP-VIS-005) is the PSSL brief for every slide. All fields are required and typed. Gate C-09 rejects any VCB with:
- Lighting grammar field containing only adjectives
- Typography weight as a word (must be numeric)
- Primary text with zero concrete nouns from the TIAR active list
- PAD scores absent from environmental_grammar
- Character spec missing head_rotation_degrees or pupil_position_ratio_pct for slides with characters
- Null intentional_imperfection on any slide
- Null incomplete_tribal_artifact on any tension slide

*Integration point:* VCB DEP-VIS-005 schema → Gate C-09 → Receipt Chain Guard log → Paradoxe (only receives fully gate-passed VCBs)

---

## Section 7 — The PSSL Brief Schema and Prompt Generation Engine

### 7.1 Paradoxe: Upgraded Role Specification

**Agent Name:** Paradoxe (upgraded)
**Previous Role:** Visual Prompt Synthesizer
**New Role:** PSSL Prompt Compiler
**Department:** Expression Department
**Reads From:** DEP-VIS-005 (Visual Composition Brief), DEP-VIS-002 (Recipe Protocol Library), DEP-VIS-004 (Character Reference Archive)
**Writes To:** RunningHub API task payload, Conscious Canva App prompt metadata
**Cannot:** Modify VCB parameters, access TIAR directly, approve generated images

Paradoxe translates a fully validated VCB into RunningHub-ready prompt strings. Every prompt it generates is traceable back to specific VCB fields. Paradoxe never improvises — it compiles.

### 7.2 PSSL Field-to-Prompt Translation Rules

**Lighting Grammar → Prompt Lighting Block**

```
VCB: "Overhead institutional fluorescent — 11pm temporal signal. Single cool-white source from above, no fill, hard shadows beneath eyes and chin."
→ Prompt: "single overhead fluorescent source, no fill lighting, clinical institutional quality, late-night isolation grammar, hard shadows beneath eyes and chin, 4200K color temperature, overhead direction only"
```

**Chromatic Spec → Prompt Color Block**

```
VCB: {foundation_hue: "#2C3E50", saturation_pct: 35, temperature_direction: "cool"}
→ Prompt: "dominant dark slate blue-grey color palette, 35% color saturation, cool color temperature, muted and desaturated rendering"
```

**Dual-Vector Gaze → Prompt Character Block**

```
VCB: {head_rotation_degrees: 15, head_rotation_direction: "right", pupil_position_ratio_pct: 20}
→ Prompt: "character head turned 15 degrees to the right from camera, pupils clearly positioned in the rightmost 20% of the visible iris area, gaze directed toward upper right zone of frame, not looking at camera"
```

**Expression → Prompt Expression Block**

```
VCB: "suppressed_exhaustion_authentic — eye_mouth_congruent — visible pore detail — left eyebrow 2mm higher"
→ Prompt: "expression of suppressed authentic exhaustion, eyes slightly heavy with visible fatigue lines, mouth neutral with slight downward tension, realistic skin texture with visible pore detail, natural facial asymmetry with left eyebrow naturally higher than right, not artificially symmetrical"
```

**Environmental Grammar → Prompt Scene Block**

```
VCB: {light_quality_signal: "11pm_institutional", spatial_density: 9, temporal_signal: "stillness_late_night", world_color_temp_kelvin: 4200, subject_frame_height_ratio_pct: 40}
→ Prompt: "late night interior, institutional overhead lighting quality, 8-10 objects visible in background suggesting accumulated work, complete environmental stillness, ambient color temperature 4200K, subject occupies approximately 40% of frame height, environment feels larger and more imposing than the subject"
```

### 7.3 The Anti-Generic Constraint Block

Appended to every prompt after all PSSL field translations:

```
Anti-Generic Block (always appended):
"NOT: generic stock photography aesthetic. NOT: Canva template styling. NOT: perfectly symmetrical composition. NOT: artificial studio lighting setup. NOT: the visual average of coaching photography. This image must be specifically and recognizably different from generic motivational content."
```

Plus enemy-typology constraint from script JSON:

```
Script enemy_typology: "performative success culture"
→ Additional: "NOT: trophy or achievement imagery. NOT: external success performance poses. The scene must communicate internal reality, not external presentation."
```

### 7.4 Complete RunningHub Task Payload

```json
{
  "workflowId": "RH-WF-CAROUSEL-SEMI-001",
  "inputs": {
    "prompt": "[Full assembled prompt string]",
    "reference_image_url": "https://assets.ccp.io/characters/coach-avatar-001-ref.png",
    "reference_image_strength": 0.85,
    "aspect_ratio": "4:5",
    "style_preset": "semi_realistic_digital",
    "saturation_override": 35,
    "color_temperature_kelvin": 4200,
    "negative_prompt": "generic, stock photo, studio lighting, artificial, posed, symmetrical face, smooth skin, perfect lighting, motivational poster aesthetic",
    "seed": null,
    "quality": "high",
    "output_format": "png"
  },
  "metadata": {
    "vcb_id": "VCB-20260317-0042",
    "slide_number": 1,
    "arc_stage": "tension",
    "semiotic_injection": false,
    "fingerprint_id": "FP-20260317-0042"
  }
}
```

---

## Section 8 — The Conscious Canva App Architecture

### 8.1 Architectural Role

The Conscious Canva App is the composition preview, editing, and approval layer of the CVE. Its three jobs:

1. **Pre-populated template loading** — receives the VCB JSON, loads the recipe template, pre-populates all content slots from the VCB
2. **RunningHub output reception** — receives generated image URLs and places them into the correct canvas layer slots
3. **Human editing layer** — full canvas editing capability for the 5% of cases where the generated composition requires adjustment

Built on the canva-clone repository (https://github.com/Davronov-Alimardon/canva-clone), customized to serve the CVE workflow. The coach is not designing — the system has already designed. The canvas exists for the exception, not the rule.

### 8.2 Template Library — Wireframe Architecture

Before defining the full template specifications, each template is defined first as a wireframe of named component slots. Components are reusable — the same component appears in multiple templates with different configuration.

#### Component Library

**Component A — Coach Handle Bar**
Used in: All 4:5 single image formats (required), carousel final slide (required), carousel interior slides (never), all poll formats (never)

```
┌─────────────────────────────────────┐
│ ○  [Coach Name]          [Logo]     │
│    @handle                          │
└─────────────────────────────────────┘
Height: 120px at 1080px width
Elements: Profile picture circle (72px diameter), Coach name (semibold), Handle (@username), Brand logo (right-aligned)
Background: Transparent or brand color — specified per coach
```

**Component B — Primary Text Zone**
Used in: All formats

```
┌─────────────────────────────────────┐
│                                     │
│  [PRIMARY TEXT]                     │
│  max 6 words                        │
│                                     │
└─────────────────────────────────────┘
Font: Arc-stage driven (see SPEC-13)
Position: Variable — top, center, or bottom depending on template
Max words: 6 primary, 12 secondary
Body copy: PROHIBITED
```

**Component C — Secondary Text Zone**
Used in: Formats where secondary text is specified in the VCB

```
┌─────────────────────────────────────┐
│  [SECONDARY TEXT]                   │
│  max 12 words                       │
└─────────────────────────────────────┘
Font: Always lighter weight than primary text
```

**Component D — Full-Bleed Image Layer**
Used in: All formats — the base layer behind all other components

```
┌─────────────────────────────────────┐
│                                     │
│         [IMAGE LAYER]               │
│         Full bleed                  │
│                                     │
└─────────────────────────────────────┘
Source: RunningHub generated PNG or Photo Deck photograph
Dimensions: Full canvas — 1080x1350 (4:5) or 1080x1920 (9:16)
```

**Component E — Slide Number Indicator**
Used in: Carousel interior slides only

```
┌──┐
│ 3│
└──┘
Position: Top right corner
Style: Minimal — small numeral, high opacity
```

**Component F — Poll Option Block**
Used in: All poll formats only

```
┌─────────────────────────────────────┐
│  [OPTION A LABEL]                   │
│  ○ Option text                      │
├─────────────────────────────────────┤
│  [OPTION B LABEL]                   │
│  ○ Option text                      │
└─────────────────────────────────────┘
```

**Component G — Seamless Edge Bleed Zone**
Used in: All carousel formats (invisible in single exports, active in seamless stitch export)

```
│← 40px →│← main content →│← 40px →│
Left and right 40px edge zones contain environmental continuation elements that bleed into adjacent slides — preserving the cinematic pan grammar in the final seamless export.
```

**Component H — CTA Zone**
Used in: Final slide of all carousel formats and some single image formats

```
┌─────────────────────────────────────┐
│  [CTA TEXT]                         │
│  save / share / comment prompt      │
└─────────────────────────────────────┘
Max words: 8
Style: Lighter weight, secondary visual importance
```

---

### 8.3 Template Specifications

#### 4:5 Carousel Templates (1080×1350)

**TPL-CAROUSEL-INTERIOR-001 — Standard Interior Slide**

Wireframe:
```
┌──────────────────────────────────────┐ ← 1080px wide
│                           [E] 3      │ ← Slide number top right
│                                      │
│                                      │
│       [D] Full-Bleed Image           │
│                                      │
│ [B] PRIMARY TEXT                     │
│     (position varies by arc stage)   │
│                                      │
│ [C] Secondary text if any            │
│                                      │
│ ← [G] Edge bleed zone → ← [G] →    │
└──────────────────────────────────────┘ ← 1350px tall
```

Layer order (bottom to top): D (image) → G (edge bleed overlay) → C (secondary text) → B (primary text) → E (slide number)
Text zone position by arc stage: Tension — bottom quarter. Build — lower third. Climax — center. Resolution — lower third with generous whitespace above.

---

**TPL-CAROUSEL-FINAL-001 — Final Slide with Coach Handle**

Wireframe:
```
┌──────────────────────────────────────┐
│ ○ Coach Name          [Logo]  [A]    │ ← Coach Handle Bar 120px
│   @handle                            │
├──────────────────────────────────────┤
│                                      │
│                                      │
│       [D] Full-Bleed Image           │
│                                      │
│ [B] PRIMARY TEXT                     │
│     Identity declaration             │
│                                      │
│ [H] CTA text                         │
│                                      │
└──────────────────────────────────────┘
```

Layer order: D → B → H → A (handle bar overlays top)
Note: This slide is designed to be screenshot-shareable as a standalone image. Primary text must work without seeing any other slide.

---

**TPL-RELIEF-PEAK-SEMI-001 — Relief Peak | Semi-Realistic | 4:5**

Applied to: Slides 1-2 (tension), Slides 3-4 (build to climax), Slide 5 (resolution final)

Tension slides (1-2) configuration:
```
┌──────────────────────────────────────┐
│                           [E] 1      │
│                                      │
│  [D] Full-Bleed — 1PP encouraged     │
│      Environmental grammar dominant  │
│      Subject 40% of frame height     │
│                                      │
│                                      │
│ [B] PRIMARY TEXT ← lower zone        │
│     Serif 800 weight                 │
│                                      │
│ ←[G]→                        ←[G]→ │
└──────────────────────────────────────┘
```

Climax slide (slide 4 of 5) configuration:
```
┌──────────────────────────────────────┐
│                           [E] 4      │
│                                      │
│  [D] Full-Bleed — Expression visible │
│      Warm light entering             │
│      Subject 55% of frame height     │
│                                      │
│ [B] PRIMARY TEXT ← center zone       │
│     Sans-serif 700 weight            │
│     Maximum chromatic saturation     │
│                                      │
│ ←[G]→                        ←[G]→ │
└──────────────────────────────────────┘
```

Resolution/final slide (slide 5) configuration:
```
┌──────────────────────────────────────┐
│ ○ Coach Name          [Logo]  [A]    │
├──────────────────────────────────────┤
│                                      │
│  [D] Full-Bleed — Open environment   │
│      Warm diffused light             │
│      Subject 65% of frame height     │
│                                      │
│                                      │
│ [B] PRIMARY TEXT ← lower third       │
│     Sans-serif 300 weight            │
│     +3% tracking                     │
│                                      │
│ [H] CTA zone                         │
└──────────────────────────────────────┘
```

---

**TPL-DOPAMINE-CLIFF-SEMI-001 — Dopamine Cliff | Semi-Realistic | 4:5**

Accumulation slides (1-3) configuration:
```
┌──────────────────────────────────────┐
│                           [E] 1      │
│  [D] Full-Bleed — Approach imagery   │
│      Motion vector visible           │
│      NO completion elements          │
│      Saturation increasing           │
│                                      │
│ [B] PRIMARY TEXT ← position varies   │
│     Bold weight — desire building    │
│                                      │
│ ←[G]→                        ←[G]→ │
└──────────────────────────────────────┘
```

Cliff slide configuration:
```
┌──────────────────────────────────────┐
│                           [E] 4      │
│                                      │
│  [D] DESATURATED — Cold shock        │
│      Near-monochrome 15-25%          │
│      Reality confrontation           │
│                                      │
│ [B] PRIMARY TEXT ← center            │
│     Typography shift — sans 700      │
│     HIGH contrast text               │
│                                      │
│ ←[G]→                        ←[G]→ │
└──────────────────────────────────────┘
```

---

**TPL-LISTICLE-001 — Listicle | 4:5**

Mood setter slide (slide 1) configuration:
```
┌──────────────────────────────────────┐
│                           [E] 1      │
│                                      │
│  [D] Full-Bleed — Complete world     │
│      Environmental grammar           │
│      Establishes emotional register  │
│                                      │
│ [B] HOOK TEXT ← lower zone           │
│     Establishes the list premise     │
│     Serif or sans based on subtype   │
│                                      │
│ ←[G]→                        ←[G]→ │
└──────────────────────────────────────┘
```

List item slides configuration:
```
┌──────────────────────────────────────┐
│                           [E] 3      │
│                                      │
│  [D] Full-Bleed — Item scene         │
│      Specific tribal visual congruent│
│      Incomplete artifact if tension  │
│                                      │
│ [B] ITEM TEXT ← varies by position  │
│     Item number optional             │
│                                      │
│ ←[G]→                        ←[G]→ │
└──────────────────────────────────────┘
```

---

**TPL-TIMELINE-001 — Visual Timeline | 4:5**

Timeline slides configuration:
```
┌──────────────────────────────────────┐
│                           [E] 3      │
│                                      │
│  [D] Full-Bleed — Period environment │
│      Color temperature tracks time   │
│      Earlier = cooler, later = warmer│
│                                      │
│ [B] TIMELINE TEXT ← lower zone       │
│     Date or period indicator         │
│                                      │
│ ←[G]→                        ←[G]→ │
└──────────────────────────────────────┘
```

---

**TPL-COMPARISON-CAROUSEL-001 — Comparison Multi-Contrast | 4:5**

Per-contrast-pair slide configuration:
```
┌──────────────────────────────────────┐
│                           [E] 2      │
│                                      │
│  [D] Full-Bleed — Split environment  │
│      Background color diff L vs R    │
│      Side A gaze → upper center      │
│      Side B gaze → lower center      │
│      X-pattern not collision         │
│                                      │
│ [B] CONTRAST LABEL ← top center      │
│                                      │
│ ←[G]→                        ←[G]→ │
└──────────────────────────────────────┘
```

---

#### 4:5 Single Image Templates (1080×1350)

**TPL-SINGLE-STANDARD-001 — Standard Single Image | 4:5**

```
┌──────────────────────────────────────┐
│ ○ Coach Name          [Logo]  [A]    │ ← Handle bar 120px
├──────────────────────────────────────┤
│                                      │
│                                      │
│       [D] Full-Bleed Image           │
│           1230px available height    │
│                                      │
│                                      │
│ [B] PRIMARY TEXT                     │
│     Position varies by archetype     │
│                                      │
│ [C] Secondary text if any            │
│                                      │
└──────────────────────────────────────┘
```

Used by: Tweet-Style Quote, Worst Case Scenario, Observational Humor (with style variant), Conceptual Contrast Simultaneous, Comparison Single Contrast

---

**TPL-OBS-HUMOR-GHIBLI-001 — Observational Humor | Ghibli | 4:5**

```
┌──────────────────────────────────────┐
│ ○ Coach Name          [Logo]  [A]    │
├──────────────────────────────────────┤
│                                      │
│  [D] Full-Bleed — Ghibli illustration│
│      Warm palette                    │
│      Maximum processing fluency      │
│      Micro-smile must activate first │
│                                      │
│ [B] HUMOR TEXT ← center or lower     │
│     Sans-serif medium weight         │
│     Benign violation setup           │
│                                      │
│ [C] Punchline or secondary text      │
│                                      │
└──────────────────────────────────────┘
```

---

**TPL-WCS-CINE-001 — Worst Case Scenario | Desaturated Cinematic | 4:5**

```
┌──────────────────────────────────────┐
│ ○ Coach Name          [Logo]  [A]    │
├──────────────────────────────────────┤
│                                      │
│  [D] Full-Bleed — Desaturated cine   │
│      20-35% saturation maximum       │
│      Environmental grammar for fear  │
│      Maximum processing fluency      │
│                                      │
│ [B] PRIMARY TEXT ← center or lower   │
│     Medium sans-serif weight         │
│     High contrast text               │
│                                      │
│ [C] Secondary amplifying text        │
│                                      │
└──────────────────────────────────────┘
```

---

**TPL-TWEET-QUOTE-001 — Tweet-Style Quote | 4:5**

```
┌──────────────────────────────────────┐
│ ✓ Coach Name    @handle    [A-mod]   │ ← Twitter-style handle
├──────────────────────────────────────┤
│                                      │
│                                      │
│  [B] QUOTE TEXT ← dominant center    │
│      Large weight                    │
│      Text is the primary visual      │
│                                      │
│  [D] Minimal background              │
│      Serves the text                 │
│                                      │
│                                      │
│ ♥ Comment Share                      │ ← Engagement icons
└──────────────────────────────────────┘
```

Note: Component A is modified for this template to match Twitter/X interface styling.

---

**TPL-9GRID-001 — 9-Grid Accumulation | 4:5**

```
┌──────────────────────────────────────┐
│ ○ Coach Name          [Logo]  [A]    │ ← Handle bar
├──────────────────────────────────────┤
│ ┌──────┐ ┌──────┐ ┌──────┐          │
│ │  [D] │ │  [D] │ │  [D] │          │
│ │  img │ │  img │ │  img │          │
│ └──────┘ └──────┘ └──────┘          │
│ ┌──────┐ ┌──────┐ ┌──────┐          │
│ │  [D] │ │  [B] │ │  [D] │          │
│ │  img │ │label │ │  img │          │
│ └──────┘ └──────┘ └──────┘          │
│ ┌──────┐ ┌──────┐ ┌──────┐          │
│ │  [D] │ │  [D] │ │  [D] │          │
│ │  img │ │  img │ │  img │          │
│ └──────┘ └──────┘ └──────┘          │
└──────────────────────────────────────┘
```

Center cell: text label only (1-2 words maximum)
8 surrounding cells: RunningHub-generated images, all showing approach-state not completion

---

#### 9:16 Poll Templates (1080×1920)

**TPL-POLL-ARCH-001 — Archetypical Poll | 9:16**

```
┌──────────────────────────────────────┐ ← 1080px
│                                      │
│                                      │
│  [B] QUESTION TEXT ← upper third     │
│      Large, high contrast            │
│      Question is the hook            │
│                                      │
│  [D] Image — Option A environment    │
│      ┌────────────────────────────┐  │
│      │  [D-A] Option A visual     │  │
│      │  [C-A] Option A label      │  │
│      └────────────────────────────┘  │
│                                      │
│  [D] Image — Option B environment    │
│      ┌────────────────────────────┐  │
│      │  [D-B] Option B visual     │  │
│      │  [C-B] Option B label      │  │
│      └────────────────────────────┘  │
│                                      │
│  Gaze A → upper center               │
│  Gaze B → lower center               │
│  X-pattern — no collision            │
│                                      │
└──────────────────────────────────────┘ ← 1920px tall
```

No coach handle bar — insufficient space in 9:16 format.
Color: Graphic/vector illustration or semi-realistic digital only.
Background: Two distinct zones — one per option, differentiated by background color (background carries the primary emotional differentiation, not character expression alone).

---

**TPL-POLL-STEREO-001 — Stereotypical Poll | 9:16**

```
┌──────────────────────────────────────┐
│                                      │
│  [B] HOOK ← upper quarter            │
│      "Which one are you?"            │
│      Bold, high contrast             │
│                                      │
│  ┌─────────────────────────────────┐ │
│  │        [D-A] Option A           │ │
│  │   Image + [C-A] Stereotype A    │ │
│  │   label inside image zone       │ │
│  └─────────────────────────────────┘ │
│                                      │
│  ┌─────────────────────────────────┐ │
│  │        [D-B] Option B           │ │
│  │   Image + [C-B] Stereotype B    │ │
│  │   label inside image zone       │ │
│  └─────────────────────────────────┘ │
│                                      │
└──────────────────────────────────────┘
```

---

**TPL-POLL-DILEMMA-001 — Controversial Dilemma / Would You Rather | 9:16**

```
┌──────────────────────────────────────┐
│                                      │
│  [B] DILEMMA QUESTION ← center top   │
│      Bold — sets up the tension      │
│                                      │
│  ┌──────────────┬──────────────────┐ │
│  │ [D-A] Left   │  [D-B] Right     │ │
│  │ Option A     │  Option B        │ │
│  │ environment  │  environment     │ │
│  │              │                  │ │
│  │ [C-A] Label  │  [C-B] Label     │ │
│  └──────────────┴──────────────────┘ │
│                                      │
│  Gaze A → toward dividing line       │
│  Gaze B → toward dividing line       │
│  Creates tension toward center       │
│                                      │
└──────────────────────────────────────┘
```

---

### 8.4 Template Customizations to Canva-Clone Base

**A — Template System Replacement**
The canva-clone's generic template gallery is replaced with the CVE template registry. Templates load automatically from the VCB JSON — the coach never browses templates. Template loading is triggered by `template_id` field in the VCB.

**B — VCB Intake API (new endpoint)**
```
POST /api/compositions/create
Body: {vcb: VCB_JSON_PAYLOAD}
Response: {composition_id, canvas_state, populated_slots, pending_image_slots}
```
Text slots populate immediately. Image slots remain as placeholder elements pending RunningHub delivery.

**C — RunningHub Asset Reception (webhook)**
```
POST /api/assets/receive
Body: {task_id, output_url, slide_number, vcb_id}
```
Received image URL is placed into the correct canvas image layer slot in real-time.

**D — Coach Handle Bar Component**
New component not in canva-clone base. Implements Component A specification. Includes: profile picture upload (from Photo Deck), coach name and handle text fields, brand logo upload slot. Position is locked to top of canvas — not movable. Visibility is controlled by the VCB `coach_handle_bar` field per slide.

**E — Seamless Carousel Export Mode**
New export function not in canva-clone base. Stitches all carousel slides into one horizontal canvas, then slices at correct slide dimensions. Edge bleed zones (Component G, 40px each side) align across the stitch boundary.

**F — Stripped Features**
Removed from coach interface: template gallery browser, font selector for primary text zones (arc-stage driven), color picker for primary background (PSSL-driven), background upload to main image zone.

Retained editing capabilities: element repositioning, text editing within existing text layers, image replacement (swap RunningHub output for Photo Deck image), layer visibility toggle, export controls.

**G — Approval and Publish Controls**
- **Approve** → marks composition approved, triggers Notion sync of full VPO
- **Request Regeneration** → returns to RunningHub queue with optional revision note
- **Edit and Approve** → manual canvas edits followed by approval

---

## Section 9 — RunningHub API Integration

### 9.1 Integration Overview

Base API: `https://www.runninghub.cn/api/`
Authentication: `RUNNINGHUB_API_KEY` encrypted environment variable
Task creation: Paradoxe
Status polling: Visual Validation Agent
Asset reception: Conscious Canva App webhook

### 9.2 Core API Operations

**Task Creation**
```
POST /task/openapi/create
Body: {
  "workflowId": "RH-WF-CAROUSEL-SEMI-001",
  "apiKey": "{{RUNNINGHUB_API_KEY}}",
  "nodeInfoList": [
    {"nodeId": "6", "fieldName": "text", "fieldValue": "{{assembled_prompt}}"},
    {"nodeId": "14", "fieldName": "image", "fieldValue": "{{reference_image_base64}}"},
    {"nodeId": "22", "fieldName": "strength", "fieldValue": "0.85"}
  ]
}
```

**Status Polling**
```
POST /task/openapi/status
Body: {"taskId": "{{task_id}}", "apiKey": "{{RUNNINGHUB_API_KEY}}"}
Response data.taskStatus: "SUCCESS | FAILED | QUEUED | RUNNING"
```

Polling strategy: Exponential backoff starting 5 seconds, doubling to 60 second maximum. Timeout at 10 minutes triggers operator notification and manual retry queue.

### 9.3 RunningHub Workflow Library

| Workflow ID | Format | Style | Notes |
|---|---|---|---|
| RH-WF-CAROUSEL-SEMI-001 | Carousel | Semi-Realistic | Reference image input for character consistency |
| RH-WF-CAROUSEL-CINE-001 | Carousel | Cinematic Color-Graded | Real photo reference optional |
| RH-WF-CAROUSEL-CLIFF-001 | Dopamine Cliff | Dynamic per-slide temperature | Cliff slide receives desaturation override |
| RH-WF-LISTICLE-001 | Listicle | Semi-Realistic | Standard carousel workflow |
| RH-WF-TIMELINE-001 | Timeline | Semi-Realistic | Chronological color temperature arc |
| RH-WF-COMPARISON-001 | Comparison/Contrast | Semi-Realistic | Two-character gaze architecture enforcement |
| RH-WF-SINGLE-SEMI-001 | Single Image | Semi-Realistic | Standard single frame |
| RH-WF-SINGLE-CINE-DESAT-001 | Single Image | Desaturated Cinematic | Worst Case Scenario + Fear-Anxiety angle |
| RH-WF-SINGLE-GHIBLI-001 | Single Image | Ghibli Illustration | Observational Humor + TII-warm single images |
| RH-WF-POLL-001 | Poll | Graphic/Vector | Two-zone split layout |
| RH-WF-GRID9-001 | 9-Grid | Semi-Realistic | 8 image cells + center label |
| RH-WF-SINGLE-QUOTE-001 | Tweet Quote | Minimal Background | Text-dominant composition |

### 9.4 Reference Image Architecture

For every slide containing a named cast character, Paradoxe passes the character's canonical reference image from DEP-VIS-004. The RunningHub workflows apply this reference through an identity-preserving node maintaining identity-critical features while allowing free variation in expression, environment, and lighting.

Reference image specs: PNG, transparent background preferred, minimum 1024×1024, face and upper body, neutral expression, frontal angle.

Stored at: `https://assets.ccp.io/characters/{{coach_id}}/{{character_id}}-ref.png`

First-generation protocol: Six candidate images are generated from a clean text description. Operator selects best candidate. This selection is the locked canonical reference for all subsequent generations — irreversible without explicit operator action.

### 9.5 Error Handling

| Failure Type | Response | Receipt Chain |
|---|---|---|
| API creation failure | Retry 3× with exponential backoff, then operator alert | Logged as FAILED |
| Task timeout >10 min | Cancel, regenerate once, then operator alert | Logged as TIMEOUT |
| AGSS score below threshold | Automatic prompt revision by Paradoxe, one regeneration | Logged as AGSS_FAIL |
| Authenticity check failure (items 1-3) | Regeneration with enhanced imperfection specification | Logged as AUTH_FAIL |
| Character drift detected | Regeneration with reference_image_strength increased to 0.95 | Logged as DRIFT_DETECTED |
| All retries failed | Operator alert, slide flagged PENDING_HUMAN_REVIEW in Notion | Receipt Chain break on that slide only — batch not fully quarantined |

---

## Section 10 — New Agents, Dependencies, and Registry Updates

### 10.1 New Dependencies — Registry V5.1

**DEP-VIS-001: Tribal Imagen Activation Registry (TIAR)**
Format: Supabase JSONB | Tier 2 | Parent: DEP-ENG-007, DEP-ENG-002
Update: Human-curated quarterly + CRAL-triggered updates

**DEP-VIS-002: Visual Recipe Protocol Library**
Format: YAML | Tier 0 (Immutable Constants — Visual Layer) | Parent: DEP-LIB-008, DEP-LIB-009
Update: On recipe architecture changes only

**DEP-VIS-003: Stage Set Emotional Architecture Library**
Format: YAML + Supabase | Tier 1 | Parent: DEP-ENG-002 for cultural segment
Update: Quarterly PAD score validation + cultural variant expansion

**DEP-VIS-004: Brand Character Reference Archive**
Format: PNG assets + JSONB metadata | Tier 1 | Parent: None
Update: On new character creation or reference image refresh only

**DEP-VIS-005: Visual Composition Brief Schema**
Format: JSON Schema definition | Tier 4 | Parent: DEP-VIS-001 through DEP-VIS-004
Update: On CVE architecture updates only

### 10.2 New Agent

**Visual Validation Agent**
Department: Safety and Governance Department
Function: Post-generation image quality assessment — AGSS scoring, authenticity feature verification, character drift detection
Tools: `image_analysis_wrapper.py` (new Python tool)
Triggers: After each RunningHub task completion event
Writes to: VCB output field, Receipt Chain Guard log
Checks: AGSS ≥ 6.5/10, authenticity items 1-3 mandatory pass, character drift pass

### 10.3 Upgraded Agents

**Abel — Visual Composition Planner**
New capabilities: Full VCB generation (all PSSL parameters per slide), TIAR query, PAD-based stage set selection, latter-third semiotic injection positioning, tribal noun-visual congruent pairing, semantic conflict specification, accumulation prohibition audit, coach handle bar decision logic, format and aspect ratio assignment

**Paradoxe — PSSL Prompt Compiler**
New capabilities: PSSL field-to-prompt translation, anti-generic constraint assembly, enemy-typology-based specificity constraints, dual-vector gaze geometry prompt directives, cultural color profile incorporation, reference image parameter assembly, complete RunningHub task payload compilation

### 10.4 New Validation Gate

**Gate C-09: PSSL Completeness Check**
Runs: After VCB generation, before Paradoxe receives the VCB

Required checks:
- All slides: lighting_grammar contains temporal signal and shadow specification (adjective-only values fail)
- All slides: saturation_pct is numeric (word descriptions fail)
- All text slides: primary_text has minimum 3 concrete nouns from TIAR active list
- All character slides: head_rotation_degrees AND pupil_position_ratio_pct both numeric
- All slides: PAD scores present in environmental_grammar
- All tension slides: incomplete_tribal_artifact is non-null
- All slides: intentional_imperfection is non-null
- All resolution slides: font_weight ≤ 500 AND font_category "sans_serif"
- Carousel formats: visual_style is NOT "ghibli" or "illustrated"
- Semiotic injection slide: not slide 1 or 2 in any sequence with 4+ slides
- Coach handle bar decision: present and valid per format rules

Failure behavior: Returns specific field-level errors to Abel for revision. Does not halt the full batch — flags the specific composition while others proceed.

### 10.5 New Adapters

**`visual-arc-adapter`**
Function: Injects arc type into Abel's composition planning, ensuring all downstream PSSL generation is arc-grounded
Active for: All visual production pipeline executions

**`tiar-adapter`**
Function: Queries DEP-VIS-001 before script text element generation (upstream in Script Generation Skills) and before visual composition text finalization (downstream in Abel)
Active for: Script Generation Skills execution + Abel VCB generation

**`pssl-compiler-adapter`**
Function: Validates that Paradoxe receives a fully gate-passed VCB before compiling RunningHub payloads
Active for: All RunningHub task creation events

**`visual-format-constraint-adapter`**
Function: Enforces format constraints before style assignment — blocks Ghibli/illustrated styles from carousel formats, enforces 9:16 for polls, validates coach handle bar logic per format
Active for: Abel VCB generation

### 10.6 New Python Tool

**`image_analysis_wrapper.py`**
Function: AGSS scoring (feature distance from training distribution center), authenticity feature extraction (expression naturalness, facial proportion, skin texture), character drift detection (facial feature comparison against DEP-VIS-004 reference)

---

## Section 11 — The Full Output JSON Contract

### 11.1 Visual Production Output (VPO) Structure

```json
{
  "vpo_id": "VPO-20260317-0042",
  "asset_id": "CCFA-C01-03-26-0042",
  "fingerprint_id": "FP-20260317-0042",
  "vcb_id": "VCB-20260317-0042",
  "recipe_protocol": "relief_peak_carousel_recipe",
  "visual_output_type": "carousel",
  "aspect_ratio": "4:5",
  "canvas_dimensions": "1080x1350",
  "coaching_segment": "conscious_business",
  "visual_style": "semi_realistic_digital",
  "production_status": "approved",
  "production_timestamp": "2026-03-17T14:23:11Z",

  "script_reference": {
    "hook_text": "The 3am integrity check",
    "archetype": "recognition_story",
    "mood_state": "escape",
    "arc_type": "tension_release"
  },

  "runninghub_execution_log": [
    {
      "slide_number": 1,
      "workflow_id": "RH-WF-CAROUSEL-SEMI-001",
      "task_id": "rh_task_abc123",
      "prompt_hash": "sha256_of_prompt",
      "output_url": "https://runninghub-output.io/output/abc123.png",
      "agss_score": 7.4,
      "agss_passed": true,
      "authenticity_check": {
        "expression_naturalness": "passed",
        "facial_proportion": "passed",
        "skin_texture": "passed",
        "overall": "passed"
      },
      "character_drift_check": "passed"
    }
  ],

  "final_assets": [
    {"slide_number": 1, "canvas_url": "https://assets.ccp.io/.../slide_1_final.png", "status": "approved"},
    {"slide_number": 2, "canvas_url": "https://assets.ccp.io/.../slide_2_final.png", "status": "approved"},
    {"slide_number": 3, "canvas_url": "https://assets.ccp.io/.../slide_3_final.png", "status": "approved"},
    {"slide_number": 4, "canvas_url": "https://assets.ccp.io/.../slide_4_final.png", "status": "approved"},
    {"slide_number": 5, "canvas_url": "https://assets.ccp.io/.../slide_5_final.png", "status": "approved"}
  ],

  "seamless_export": {
    "horizontal_stitch_url": "https://assets.ccp.io/.../carousel_full.png",
    "sliced_slides_zip": "https://assets.ccp.io/.../slides.zip"
  },

  "tiar_audit": {
    "nouns_used": ["3am", "integrity", "resonance", "threshold"],
    "decay_status_at_production": {
      "3am": "in_distribution",
      "integrity": "in_distribution",
      "resonance": "in_distribution",
      "threshold": "in_distribution"
    },
    "expired_nouns_blocked": ["authentic", "freedom", "alignment"]
  },

  "notion_content_card": {
    "hook_text": "The 3am integrity check",
    "caption": "{{full caption from script JSON}}",
    "posting_recommendation": "Escape mode — Tuesday or Thursday 7-9pm. Audience arousal descending from work stress. Avoid Monday morning high-avoidance state.",
    "why_this_visual": "Relief Peak arc on Tension-Release physiology. Slides 1-3 use 11pm institutional grammar targeting somatic body-memory of late-night integrity decisions. Semiotic injection at slide 4 (latter-third position — penultimate slide) at the exhale moment. Slide 5 designed as standalone shareable identity declaration. All tribal nouns active with no decay flags. Semi-realistic style matching TII 45 warming stage — transportation contract active.",
    "leadership_farming_note": "Exercises Authentic Vulnerability (Trait 3) — coach naming their own experience of compromising integrity."
  },

  "receipt_chain": {
    "tiar_query": "PASS_2026-03-17T14:15:22Z",
    "abel_vcb_generation": "PASS_2026-03-17T14:16:44Z",
    "pssl_completeness_gate_c09": "PASS_2026-03-17T14:17:01Z",
    "paradoxe_prompt_compilation": "PASS_2026-03-17T14:17:15Z",
    "runninghub_execution_all_slides": "PASS_2026-03-17T14:19:52Z",
    "visual_validation_agent": "PASS_2026-03-17T14:20:18Z",
    "canvas_composition": "PASS_2026-03-17T14:21:44Z",
    "notion_sync": "PASS_2026-03-17T14:23:11Z",
    "chain_status": "UNBROKEN"
  }
}
```

---

## Section 12 — Production Governance, Quality Gates, and Notion Delivery

### 12.1 The Five-Gate Visual Quality Sequence

Gates operate at the individual composition level — a single composition failure does not halt other compositions in the same weekly batch.

**Gate V-01: TIAR Decay Check**
Checks: All concrete nouns in script hook_concrete_nouns and active_tribal_nouns are "in_distribution" or "tribal_potential"
On failure: TIAR warning flag set in VCB. Composition proceeds with warning logged in Notion card for operator review.

**Gate V-02: PSSL Completeness Check (C-09)**
Checks: All required PSSL fields populated and type-valid (full list in Section 10.4)
On failure: Field-level errors returned to Abel. Abel revises and resubmits. Maximum 2 revision cycles before operator escalation.

**Gate V-03: Accumulation Prohibition Audit**
Checks: No prohibited completion imagery in accumulation slide specifications
On failure: Abel revises the offending slide's visual congruent specification.

**Gate V-04: Visual Validation Post-Generation**
Checks: AGSS ≥ 6.5, authenticity items 1-3 passed, character drift clear
On failure: Automatic Paradoxe prompt revision and one regeneration attempt. On second failure: operator alert, slide flagged PENDING_HUMAN_REVIEW. Composition delivered with placeholder in flagged slot.

**Gate V-05: Receipt Chain Confirmation**
Checks: All previous gate passes logged, no broken chain links
On failure: Composition quarantined. Not delivered to Notion until chain is repaired.

### 12.2 The Notion Visual Content Card

Each approved composition delivers this Notion card structure:

**Card Header**
Universal Asset ID, recipe name in plain language, production status, date, visual style

**Preview Section**
Carousel: horizontal stitch image + individual numbered slide previews + ZIP download
Single image: full preview + individual PNG download

**Content Ready to Copy**
Hook text, full caption, hashtag recommendations, posting day and time recommendation

**Why This Visual Was Built This Way** (plain language — written for the coach, not technical)

**Leadership Farming Note** — which trait this exercises and why

**Technical Audit** (collapsed by default — operator accessible)
TIAR decay status per noun, AGSS scores per slide, authenticity check results, Receipt Chain status, Fingerprint ID

### 12.3 Weekly Visual Production Allocation

| Format | Est. Weekly Volume | Production Path |
|---|---|---|
| Carousels (all carousel recipes) | 10-14 | Full CVE → RunningHub → Canva App |
| Single images (humor, WCS, quotes, contrast) | 8-10 | Full CVE → RunningHub → Canva App |
| Polls (all poll variants) | 3-5 | Full CVE → RunningHub → Canva App |
| 9-Grid accumulation | 1-2 | Full CVE → RunningHub → Canva App |
| Short-form video | 6-8 | Visual Brief Export only |
| Webinar slides | 1-2 | Existing Excalidraw pipeline (Benjamin) |
| Tier lists | 1-2 | Existing Excalidraw pipeline (Benjamin) |

### 12.4 Complete Sovereign Image Rule

**Rule 1 (Original):** The coach's actual face is never artificially generated.

**Rule 2 (CVE Extension A):** AI-generated avatar characters and real coach photography never appear in the same visual composition.

**Rule 3 (CVE Extension B):** Real coach photography is sourced exclusively from the Personal Branding Photo Deck in Notion. If no photo matches the required register, the system generates a photo session recommendation.

**Rule 4 (CVE Extension C):** When real photography is used, PSSL parameters function as art direction specifications for the photography session — not as AI generation parameters.

---

## Appendix A — Registry V5.1 Delta

**New Dependencies:**
- DEP-VIS-001: TIAR — Tier 2
- DEP-VIS-002: Visual Recipe Protocol Library — Tier 0
- DEP-VIS-003: Stage Set Emotional Architecture Library — Tier 1
- DEP-VIS-004: Brand Character Reference Archive — Tier 1
- DEP-VIS-005: Visual Composition Brief Schema — Tier 4

**New Protocols:**
- DEP-PROTO-017: PSSL Compilation Protocol
- DEP-PROTO-018: Visual Production Quality Gate Protocol

**New Agents:**
- Visual Validation Agent (Safety and Governance Department)

**Upgraded Agents:**
- Abel: Visual Recipe Router → Visual Composition Planner
- Paradoxe: Visual Prompt Synthesizer → PSSL Prompt Compiler

**New Validation Gates:**
- Gate C-09: PSSL Completeness Check
- Gates V-01 through V-05: Visual Production Quality Sequence

**New Adapters:**
- `visual-arc-adapter`
- `tiar-adapter`
- `pssl-compiler-adapter`
- `visual-format-constraint-adapter`

**New Python Tool:**
- `image_analysis_wrapper.py`

---

## Appendix B — PRD Functional Requirements Update

**FR-VIS-01:** The system generates complete VCBs for all scripts flagged for visual production, incorporating full PSSL parameters per slide. VCBs must pass Gate C-09 before proceeding to prompt compilation.

**FR-VIS-02:** The system queries the TIAR before any script hook generation AND before visual composition text finalization, injecting active tribal nouns as required vocabulary and blocking expired nouns.

**FR-VIS-03:** The system compiles PSSL-compliant prompts via Paradoxe and executes RunningHub API workflows for all visual output types, passing character reference images for identity consistency. RunningHub task execution must complete within 10 minutes per slide.

**FR-VIS-04:** The system validates all RunningHub outputs through the Visual Validation Agent, scoring each image against the AGSS (minimum 6.5/10) and verifying three mandatory authenticity features. Images failing thresholds are automatically returned for one regeneration attempt.

**FR-VIS-05:** The system loads VCB JSON into the Conscious Canva App, pre-populates all template slots, receives RunningHub output URLs into correct canvas layer positions, and provides full canvas editing capability for operator adjustments. Final compositions export as individual PNGs and seamless horizontal stitch files for carousel formats.

**FR-VIS-06:** The system delivers complete VPO records to the coach's Notion workspace including: composition preview, hook text and caption, posting recommendations, plain-language visual rationale, leadership farming notes, and collapsed technical audit with TIAR decay status, AGSS scores, and Receipt Chain confirmation.

**FR-VIS-07:** All carousels are produced in 4:5 format (1080×1350px). Standard single images are produced in 4:5 format. Poll single images are produced in 9:16 format (1080×1920px). No other aspect ratios are supported in Version 1.0 of the CVE template library.

**FR-VIS-08:** Ghibli and illustrated visual styles are available exclusively for single image compositions. Carousel compositions use cinematic color-graded or semi-realistic digital styles only. This constraint is enforced at the format constraint layer before any other style selection logic runs.

---

*End of CVE Documentation V2.0*
*Supersedes: CVE Documentation V1.0 (2026-03-17)*
*Next update triggered by: RunningHub workflow library build completion, Canva App template build, TIAR first population*
