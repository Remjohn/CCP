# Conscious Visual Engine (CVE) — System Documentation V3.0

**Author:** Emilio
**Date:** 2026-03-17
**Version:** 3.0
**Status:** Architecture Specification — Integration Draft
**Supersedes:** CVE Documentation V2.0
**Feeds Into:** PRD Update, Tech Spec, Skill Templates, Conscious Canva App Build

---

## Document Purpose

This document specifies the complete architecture of the Conscious Visual Engine (CVE) — the visual execution layer of the Conscious Coaching Platform (CCP). Every section resolves to a buildable system component: an agent, a registry entry, a composable skill, a validation gate, an API contract, or a template schema.

**V3 primary changes from V2:**
- Complete image sourcing hierarchy — four tiers with clear decision logic replacing the binary real/AI split
- Aurore upgraded to Image Research Planner with multi-API orchestration
- Nine composable image search skills introduced as JIT-compiled modular units
- Canva App in-app image search panel with all five APIs
- 1:1 aspect ratio added to the template library
- Ghibli style correctly scoped to Conceptual Contrast and Supervisuals only
- Observational Humor corrected to real images always

---

## Section 1 — CVE Position in the CCP Architecture

### 1.1 The Sixth System

The CCP currently operates five integrated systems: the Content Factory (CCF), the Invisible Coaching App (CBCS), the Webinar System (V²WS), the Tierlist, and the Notion Delivery Layer. The CVE is the sixth system — extending the CCF by adding a complete visual production pipeline downstream of script validation.

```
CCF Pipeline → Script Validation (Triple-Pass Gate) → [Visual Production Flag SET]
                                                              ↓
                                              CVE Visual Composition Planning (Abel)
                                                              ↓
                                              Image Research Planning (Aurore)
                                                    ↓               ↓
                                           Real Image APIs    RunningHub AI Gen
                                                    ↓               ↓
                                              Conscious Canva App (Composition Layer)
                                                              ↓
                                              Notion Delivery (Coach Approval)
```

The script is the upstream authority. The visual serves the script — never the reverse.

### 1.2 What the CVE Produces

**Type 1 — Carousel Compositions:** Multi-slide sequences in 4:5 format (1080×1350px). Visual styles: cinematic color-graded and semi-realistic digital only.

**Type 2 — Single Image Compositions:** Standalone posts in 4:5 (1080×1350px), 1:1 (1080×1080px), or 9:16 (1080×1920px) for polls. Ghibli style available exclusively for Conceptual Contrast and Supervisuals in this category.

**Type 3 — Visual Brief Exports:** Art direction documents for video-format archetypes (Case Studies, Myth Debunking, Tier Lists, Reaction content). No image generation.

### 1.3 The Sovereign Image Rule Extension

**Rule 1 (Original):** The coach's actual face is never artificially generated.

**Rule 2 (CVE Extension A):** AI-generated avatar characters and real coach photography never appear in the same visual composition.

**Rule 3 (CVE Extension B):** Real coach photography is sourced exclusively from the Personal Branding Photo Deck in Notion. If no photo matches the required register, the system generates a photo session recommendation.

**Rule 4 (CVE Extension C):** When real photography is used, PSSL parameters function as art direction specifications for the photography session.

**Rule 5 (CVE Extension D — Image Sourcing Priority):** Real images always take priority over AI-generated images. AI generation is a fallback, not a default. The only exception paths are: brand avatar characters (no real photograph of a fictional character exists), Conceptual Contrast illustration (scenarios requiring controlled character pairs), and Supervisuals (abstract philosophical concepts existing beyond photography).

### 1.4 Agent Roles in the CVE

- **Abel** (upgraded) — Visual Composition Planner — Section 3
- **Aurore** (upgraded) — Image Research Planner — Section 4
- **Paradoxe** (upgraded) — PSSL Prompt Compiler — Section 7
- **Visual Validation Agent** (new) — post-generation quality gate — Section 10

---

## Section 2 — The Script-to-Visual Production Flow

### 2.1 Trigger Conditions

Visual production is triggered when a script has passed all three validation gates AND its archetype maps to a visual output type. The Visual Production Flag is set in DEP-ENG-011:

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

The visual system receives the complete production context that built the script:

```json
{
  "asset_id": "CCFA-C01-03-26-0042",
  "script_components": {
    "archetype_id": "relief_peak_carousel_recipe",
    "emotional_angle": "validation_relief",
    "arc_type": "tension_release",
    "hook_text": "The 3am integrity check",
    "hook_concrete_nouns": ["3am", "integrity"],
    "slide_texts": ["...", "...", "...", "...", "..."]
  },
  "psychological_routing": {
    "mood_state": "escape",
    "tii_score": 45
  },
  "tribal_context": {
    "coaching_segment": "conscious_business",
    "active_tribal_nouns": ["resonance", "integrity", "threshold"],
    "enemy_typology": "performative success culture",
    "audience_recognition_context": "late-stage burnout from values misalignment"
  },
  "known_persons_referenced": [],
  "fingerprint_id": "FP-20260317-0042"
}
```

### 2.3 Format-to-Recipe Routing

| Script Archetype | Visual Output Type | Aspect Ratio | Recipe Protocol |
|---|---|---|---|
| Relief Peak | Carousel | 4:5 | `relief_peak_carousel_recipe` |
| Dopamine Cliff | Carousel | 4:5 | `dopamine_cliff_recipe` |
| Curiosity/Funny/Nostalgia/Fear/Hope/Outrageous Listicle | Carousel | 4:5 | `listicle_visual_recipe` |
| Visual Timeline | Carousel | 4:5 | `visual_timeline_recipe` |
| Comparison (single contrast) | Single Image | 4:5 or 1:1 | `comparison_archetypes_recipe` |
| Comparison (multiple contrasts) | Carousel | 4:5 | `comparison_archetypes_recipe` |
| Conceptual Contrast (simultaneous) | Single Image | 1:1 | `conceptual_contrast_recipe` |
| Conceptual Contrast (transformational) | Carousel | 4:5 | `conceptual_contrast_recipe` |
| Observational Humor | Single Image | 1:1 or 4:5 | `observational_humor_recipe` |
| Worst Case Scenario | Single Image | 4:5 | `worst_case_scenario_recipe` |
| Tweet-Style Quote | Single Image | 1:1 | `tweet_quote_recipe` |
| Supervisual | Single Image | 1:1 | `supervisual_recipe` |
| Stereotypical Poll | Single Image | 9:16 | `poll_visual_recipe` |
| Archetypical Poll | Single Image | 9:16 | `archetypical_poll_recipe` |
| Controversial Dilemma / Would You Rather | Single Image | 9:16 | `controversial_dilemma_poll_recipe` |
| 9-Grid Accumulation | Single Image (grid) | 4:5 | `nine_grid_recipe` |
| Case Study | Visual Brief Export | — | Video-only |
| Myth Debunking | Visual Brief Export | — | Video-only |
| Recognition Story Reel | Visual Brief Export | — | Video-only |
| Tier List Hybrid | Visual Brief Export | — | Video-only |

### 2.4 The Four-Tier Image Sourcing Hierarchy

This hierarchy governs every image slot in every slide across all formats. It is the foundational philosophy of the CVE: real images carry more authenticity signal, trust, and tribal recognition than any generated equivalent.

**Tier 1 — Real photograph of a specific named person**
Applicable when: the content references or features a real person the audience can identify.
Sources:
- Coach: Personal Branding Photo Deck in Notion (queried via SKILL-IMG-009)
- Known public figure referenced in the script: SERPER Known Persons search via SKILL-IMG-006, cross-referenced against the Known Persons Registry in DEP-VIS-006

**Tier 2 — Real stock images**
Applicable when: the slide requires an environment, scene, object, atmosphere, or anonymous human moment. Stock images are searched first for all non-character image needs.
Sources: Unsplash (SKILL-IMG-001), Pexels (SKILL-IMG-002), Pixabay (SKILL-IMG-003), GIPHY for motion content (SKILL-IMG-004), SERPER Google/Bing image search for specific tribal visual congruents (SKILL-IMG-005)

**Tier 3 — Realistic cinematic AI character (RunningHub)**
Applicable when: the content requires a specific character in a specific emotional state, pose, or scenario that real photography cannot reliably provide. Prompts always target realistic and cinematic output. Never stylized.
Source: RunningHub via SKILL-IMG-007

**Tier 4 — Ghibli style AI illustration (RunningHub + LoRAs)**
Applicable exclusively to: Conceptual Contrast and Supervisuals.
Two sub-use-cases:
- Conceptual Contrast: scenario-based comparisons showing two characters in specific situations that would be impossible or unreliable to source through photography
- Supervisuals: abstract philosophical concepts that cannot be represented through physical reality
Source: RunningHub via SKILL-IMG-008

**What never happens:**
- Stock images are never used for characters — a generated character with a specific expression in a specific environment is more precise than any stock photograph of a person
- Ghibli style never used for any format except Conceptual Contrast and Supervisuals
- Observational Humor never uses illustration — the tribal recognition mechanism requires the viewer to feel "yes that IS real life"
- AI generation is never attempted before the stock image search is completed and returned no viable result

### 2.5 Image Type Classification per Slide

Abel assigns an `image_type` field to every slide in the VCB. This field determines which image research skills Aurore invokes and what tier is appropriate:

| Image Type | Tier Applied | Skills Invoked |
|---|---|---|
| `environment_scene` | Tier 2 | SKILL-IMG-001, 002, 003, 005 |
| `motion_content` | Tier 2 | SKILL-IMG-004 (GIPHY) |
| `named_person_coach` | Tier 1 | SKILL-IMG-009 |
| `named_person_public_figure` | Tier 1 | SKILL-IMG-006 |
| `character_specific_emotion` | Tier 3 | SKILL-IMG-007 (RunningHub realistic) |
| `character_brand_avatar` | Tier 3 | SKILL-IMG-007 + DEP-VIS-004 reference |
| `conceptual_contrast_illustration` | Tier 4 | SKILL-IMG-008 (RunningHub Ghibli) |
| `supervisual_abstract` | Tier 4 | SKILL-IMG-008 (RunningHub Ghibli) |

For `environment_scene` and `motion_content`: Aurore runs the stock search first. If no viable result is returned, she escalates to `character_specific_emotion` path with RunningHub.

For `character_specific_emotion`: RunningHub is called directly — no stock search is attempted for character slots.

### 2.6 Complete Pipeline Execution Sequence

1. Visual Production Flag set in DEP-ENG-011
2. Abel receives full script JSON package
3. Abel confirms arc type match against recipe protocol
4. Abel assigns `image_type` per slide and generates full VCB
5. Gate C-09 validates all required PSSL fields
6. **Aurore receives VCB — executes Image Research Plan per slide**
7. Aurore returns `image_resolution_map` — approved real images or RunningHub escalations per slide
8. Paradoxe compiles RunningHub prompt payloads only for slides escalated to Tier 3 or 4
9. RunningHub API executes image generation for escalated slides
10. Visual Validation Agent scores RunningHub outputs (AGSS + authenticity)
11. All images (real + generated) placed into Canva App canvas layer slots
12. Canvas composition assembled and available for operator editing
13. Operator approves, requests regeneration, or edits and approves
14. Receipt Chain confirmed, VPO record created
15. Notion delivery — complete visual content card

---

## Section 3 — The Visual Composition Planning Agent (Abel Upgraded)

### 3.1 Agent Specification

**Agent Name:** Abel (upgraded)
**Role:** Visual Composition Planner
**Department:** Expression Department
**Reads From:** DEP-ENG-011, DEP-VIS-001 (TIAR), DEP-VIS-002 (Recipe Library), DEP-VIS-003 (Stage Set Library), DEP-VIS-004 (Character Reference Archive), DEP-VIS-006 (Known Persons Registry), DEP-ENG-016, DEP-ENG-003, DEP-ENG-007
**Writes To:** DEP-VIS-005 (Visual Composition Brief)

### 3.2 Abel's Decision Process

**Step 1 — Arc Type Confirmation**
Confirms arc type from script package matches recipe protocol. Mismatch flags for operator review.

**Step 2 — Format, Aspect Ratio, and Image Type Assignment**
Assigns format, aspect ratio, and `image_type` per slide from routing table. 4:5 default for carousels and standard single images. 1:1 for tweet quotes, supervisuals, observational humor, and single-contrast comparisons. 9:16 for all polls.

**Step 3 — Semiotic Injection Position**
Determines semiotic injection slide using the latter-third principle. Arc type determines position within that range. Not a formula — a positioning principle with story-logic application.

**Step 4 — Visual Style Assignment**
Format constraint (binding) → archetype override → TII score. Carousels: cinematic or semi-realistic only. Conceptual Contrast and Supervisuals: Ghibli. Observational Humor: real image (no illustration, no AI character).

**Step 5 — PSSL Parameter Generation Per Slide**
Full somatic target, lighting grammar, chromatic spec, character spec, environmental grammar, typography spec per slide.

**Step 6 — Tribal Noun + Visual Congruent Pairing**
Pairs each tribal concrete noun with a specific scene grammar description. Congruents must be specific — any description containing "generic," "typical," or "person looking" fails Gate C-09.

**Step 7 — Stage Set Selection**
Queries DEP-VIS-003 using PAD score requirements.

**Step 8 — Known Persons Check**
Scans `known_persons_referenced` field in script JSON. If a named real person is referenced, adds a `named_person_search_required: true` flag to the relevant slide's image spec, setting `image_type: named_person_public_figure` and querying DEP-VIS-006 for the person's registry entry.

**Step 9 — Template Assignment and Coach Handle Bar Decision**
Assigns template ID from DEP-VIS-002. Coach handle bar: present on 4:5 and 1:1 single images (required), carousel final slide (required), carousel interior slides (never), all poll formats (never).

### 3.3 VCB Schema — Image Resolution Fields Added

The VCB schema (DEP-VIS-005) includes new per-slide image resolution fields:

```json
{
  "vcb_id": "VCB-20260317-0042",
  "asset_id": "CCFA-C01-03-26-0042",
  "recipe_protocol": "relief_peak_carousel_recipe",
  "visual_output_type": "carousel",
  "arc_type": "tension_release",
  "total_slides": 5,
  "semiotic_injection_slide": 4,
  "semiotic_injection_rationale": "Tension-Release arc — exhale fires on penultimate slide",
  "visual_style": "semi_realistic_digital",
  "aspect_ratio": "4:5",
  "canvas_dimensions": "1080x1350",
  "template_id": "TPL-RELIEF-PEAK-SEMI-001",
  "coach_handle_bar": {"final_slide": true, "interior_slides": false},
  "slides": [
    {
      "slide_number": 1,
      "arc_stage": "tension",
      "image_type": "environment_scene",
      "image_sourcing_tier": 2,
      "image_search_query": "late night institutional office fluorescent light overhead isolated person desk documents",
      "image_search_fallback_query": "11pm work desk overhead light exhausted",
      "image_search_skills_to_invoke": ["SKILL-IMG-001", "SKILL-IMG-002", "SKILL-IMG-003", "SKILL-IMG-005"],
      "runninghub_fallback": true,
      "named_person_search_required": false,
      "somatic_target": {
        "corrugator_state": "active",
        "zygomaticus_state": "suppressed",
        "scr_target": "elevated"
      },
      "lighting_grammar": "Overhead institutional fluorescent — 11pm temporal signal. Single cool-white source from above, no fill, hard shadows beneath eyes and chin.",
      "chromatic_spec": {
        "foundation_hue": "#2C3E50",
        "accent_hue": "#7F8C8D",
        "saturation_pct": 35,
        "saturation_direction": "stable",
        "temperature_direction": "cool"
      },
      "character_spec": null,
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
        "body_copy": "PROHIBITED"
      },
      "tribal_noun_visual_congruent": {
        "noun": "3am",
        "visual_congruent": "Phone screen visible showing timestamp 03:14, draft email open — send button visible but untouched, cursor blinking in message body"
      },
      "incomplete_tribal_artifact": "Values statement document with three of five sections blank — cursor blinking in fourth section",
      "intentional_imperfection": "Slightly askew notebook at desk edge — not repositioned",
      "semantic_conflict_spec": {
        "aspirational_state": "values-led entrepreneur operating from integrity",
        "depicted_reality": "draft email written from fear of losing the client"
      },
      "first_person_pov": false,
      "accumulation_prohibition_passed": true
    },
    {
      "slide_number": 4,
      "arc_stage": "semiotic_climax",
      "semiotic_injection": true,
      "image_type": "character_brand_avatar",
      "image_sourcing_tier": 3,
      "image_search_query": null,
      "runninghub_required": true,
      "character_spec": {
        "reference_url": "https://assets.ccp.io/characters/coach-avatar-001-ref.png",
        "head_rotation_degrees": 0,
        "head_rotation_direction": "center",
        "pupil_position_ratio_pct": 50,
        "gaze_target_zone": "direct_camera_engagement",
        "expression": "recognition_relief_authentic",
        "expression_description": "Eyes slightly widened — the specific micro-expression of recognizing a truth avoided. Not happiness yet, but the relief of naming the thing. Orbicularis oculi beginning to activate. Mouth slightly parted.",
        "expression_congruence_check": "full_duchenne_onset_eye_mouth_congruent",
        "skin_texture": "visible_pore_detail_required",
        "intentional_asymmetry": "left_eyebrow_2mm_higher"
      }
    }
  ]
}
```

---

## Section 4 — Image Research Architecture (Aurore Upgraded + Composable Skills)

### 4.1 Aurore: Upgraded Role Specification

**Agent Name:** Aurore (upgraded)
**Previous Role:** Visual Asset Researcher
**New Role:** Image Research Planner
**Department:** Perception Department
**Reads From:** DEP-VIS-005 (VCB — specifically the image_type and image_search_query fields per slide), DEP-VIS-006 (Known Persons Registry), DEP-VIS-004 (Brand Character Reference Archive)
**Writes To:** `image_resolution_map` — a JSON object mapping every slide to either an approved real image URL or a RunningHub escalation flag
**Uses:** Nine composable image search skills assembled per slide by the JIT compiler

Aurore's single job: for every slide in the VCB, resolve the image slot to the highest available tier. She processes all slides in parallel, returning the `image_resolution_map` before any RunningHub call is made. Paradoxe only receives slides where Aurore's map shows `resolution: "runninghub_required"`.

### 4.2 The Nine Composable Image Search Skills

These are JIT-compiled SKILL.md files in the image research domain. They follow the same three-block schema (Invariants, Runtime Injections, Validation Gates) as all other CCP skills. Each skill is self-contained and composable — Aurore assembles the right combination per slide based on the `image_type` field.

---

**SKILL-IMG-001: Unsplash Image Search**

```yaml
skill_id: "SKILL-IMG-001"
skill_name: "unsplash_image_search"
skill_family: "image_research"
composable: true

api_endpoint: "https://api.unsplash.com/search/photos"
api_key_env: "UNSPLASH_ACCESS_KEY"

block_a_invariants:
  - "Search query must derive directly from VCB image_search_query field — never from aesthetic preference"
  - "Results must be scored against PSSL parameters — color temperature, spatial density, temporal signal"
  - "Minimum resolution: 1080px on shortest edge"
  - "Orientation filter applied from VCB aspect_ratio field"

block_b_runtime_injections:
  primary_query: "{{vcb.image_search_query}}"
  fallback_query: "{{vcb.image_search_fallback_query}}"
  orientation: "{{derived_from_aspect_ratio}}"
  color_filter: "{{derived_from_chromatic_spec.foundation_hue}}"
  results_per_query: 10

scoring_against_pssl:
  - "Estimated color temperature match (±1000K acceptable)"
  - "Spatial density visual scan (object count estimate)"
  - "Temporal signal presence (time-of-day readable from image)"
  - "PAD score rough match (pleasure, arousal, dominance)"
  - "Absence of prohibited elements (accumulation prohibition check)"

block_c_validation:
  - "Minimum 1 result must score above PSSL match threshold (0.65)"
  - "If no result clears threshold: flag as no_viable_result, escalate to fallback_query"
  - "If fallback also fails: return escalation_required flag to Aurore"

output:
  format: "ranked_image_candidates_list"
  fields: ["image_url", "download_url", "pssl_match_score", "color_temp_estimate", "attribution"]
```

---

**SKILL-IMG-002: Pexels Image Search**

```yaml
skill_id: "SKILL-IMG-002"
skill_name: "pexels_image_search"
skill_family: "image_research"
composable: true

api_endpoint: "https://api.pexels.com/v1/search"
api_key_env: "PEXELS_API_KEY"

block_a_invariants:
  - "Query derives from VCB image_search_query — not aesthetic preference"
  - "Results scored against PSSL parameters"
  - "Minimum resolution: 1080px shortest edge"
  - "Video results excluded — photo search only"

block_b_runtime_injections:
  query: "{{vcb.image_search_query}}"
  orientation: "{{derived_from_aspect_ratio}}"
  per_page: 10

scoring_against_pssl:
  - "Color temperature match"
  - "Spatial density estimate"
  - "Temporal signal"
  - "PAD rough match"
  - "Accumulation prohibition check"

block_c_validation:
  - "Minimum 1 result above threshold (0.65) or escalate"

output:
  format: "ranked_image_candidates_list"
  fields: ["src.original", "src.large2x", "pssl_match_score", "photographer", "alt"]
```

---

**SKILL-IMG-003: Pixabay Image Search**

```yaml
skill_id: "SKILL-IMG-003"
skill_name: "pixabay_image_search"
skill_family: "image_research"
composable: true

api_endpoint: "https://pixabay.com/api/"
api_key_env: "PIXABAY_API_KEY"

block_a_invariants:
  - "Query derives from VCB image_search_query"
  - "image_type filter: photo (not illustration, not vector)"
  - "Results scored against PSSL parameters"
  - "Safesearch: true"

block_b_runtime_injections:
  q: "{{vcb.image_search_query}}"
  image_type: "photo"
  orientation: "{{derived_from_aspect_ratio}}"
  min_width: 1080
  per_page: 10

scoring_against_pssl:
  - "Color temperature match"
  - "Spatial density estimate"
  - "Temporal signal"
  - "PAD rough match"

block_c_validation:
  - "Minimum 1 result above threshold (0.65) or escalate"

output:
  format: "ranked_image_candidates_list"
  fields: ["largeImageURL", "webformatURL", "pssl_match_score", "user", "tags"]
```

---

**SKILL-IMG-004: GIPHY Search**

```yaml
skill_id: "SKILL-IMG-004"
skill_name: "giphy_search"
skill_family: "image_research"
composable: true

api_endpoint: "https://api.giphy.com/v1/gifs/search"
api_key_env: "GIPHY_API_KEY"
applicable_when: "image_type = motion_content"

block_a_invariants:
  - "Only invoked for motion content image types"
  - "Rating filter: g or pg — no explicit content"
  - "Results must match emotional register of arc stage"

block_b_runtime_injections:
  q: "{{vcb.image_search_query}}"
  rating: "pg"
  limit: 10

scoring_against_pssl:
  - "Emotional register match against arc stage"
  - "Content appropriateness"

block_c_validation:
  - "Minimum 1 result with appropriate emotional register or escalate to static image search"

output:
  format: "ranked_gif_candidates_list"
  fields: ["images.original.url", "images.fixed_height.url", "pssl_match_score", "title"]
```

---

**SKILL-IMG-005: SERPER General Image Search**

```yaml
skill_id: "SKILL-IMG-005"
skill_name: "serper_general_image_search"
skill_family: "image_research"
composable: true

api_endpoint: "https://google.serper.dev/images"
api_key_env: "SERPER_API_KEY"
use_case: "Tribal visual congruents that are too specific for stock photography libraries — real-world moments, specific cultural contexts, niche environments"

block_a_invariants:
  - "Query derives from VCB tribal_noun_visual_congruent.visual_congruent field — not the generic image_search_query"
  - "SERPER reaches Google and Bing image indexes — use for specific tribal environments that stock APIs miss"
  - "Results are reference images — used directly in composition"

block_b_runtime_injections:
  q: "{{vcb.tribal_noun_visual_congruent.visual_congruent}} real photo"
  num: 10
  gl: "{{audience_geographic_context}}"

scoring_against_pssl:
  - "Tribal specificity match"
  - "Environmental grammar match"
  - "Emotional register alignment"

block_c_validation:
  - "Minimum 1 result matching tribal congruent description or escalate"

output:
  format: "ranked_image_candidates_list"
  fields: ["imageUrl", "thumbnailUrl", "title", "source", "pssl_match_score"]
```

---

**SKILL-IMG-006: SERPER Known Persons Search**

```yaml
skill_id: "SKILL-IMG-006"
skill_name: "serper_known_persons_search"
skill_family: "image_research"
composable: true

api_endpoint: "https://google.serper.dev/images"
api_key_env: "SERPER_API_KEY"
applicable_when: "image_type = named_person_public_figure"
prerequisite: "Person must exist in DEP-VIS-006 Known Persons Registry"

block_a_invariants:
  - "Only invoked when a named real person is referenced in the script JSON known_persons_referenced field"
  - "Person must be in DEP-VIS-006 Known Persons Registry before search is attempted"
  - "Search targets a specific named person in a context matching the script reference"
  - "Results must show the person in a context coherent with the script's use of them"

block_b_runtime_injections:
  person_name: "{{dep_vis_006.person.full_name}}"
  context_descriptor: "{{script_reference_context}}"
  q: "{{person_name}} {{context_descriptor}} photo"
  num: 10

scoring_against_pssl:
  - "Person correctly identified in image"
  - "Context matches script reference"
  - "Emotional register appropriate to arc stage"

block_c_validation:
  - "Person must be clearly identifiable in returned images"
  - "If person not clearly identifiable: return no_viable_result, escalate to RunningHub Tier 3"

output:
  format: "ranked_person_image_candidates"
  fields: ["imageUrl", "thumbnailUrl", "title", "source", "pssl_match_score", "person_confirmed"]
```

---

**SKILL-IMG-007: RunningHub Realistic Cinematic Character Generation**

```yaml
skill_id: "SKILL-IMG-007"
skill_name: "runninghub_realistic_character"
skill_family: "image_research"
composable: true
applicable_when: "image_type = character_specific_emotion OR character_brand_avatar"
tier: 3

block_a_invariants:
  - "Only invoked when stock image search has returned no_viable_result OR image_type is character"
  - "Prompts always target realistic and cinematic output — never stylized, illustrated, or cartoon"
  - "Character reference image from DEP-VIS-004 must be passed when character_brand_avatar"
  - "Dual-vector gaze specification required: head_rotation_degrees + pupil_position_ratio_pct"
  - "Expression congruence required: eye-mouth congruent, never expression on mouth alone"
  - "Skin texture: visible pore detail always — smooth skin invalid"
  - "Intentional asymmetry: one named asymmetry always specified"

block_b_runtime_injections:
  workflow_id: "{{dep_vis_002.runninghub_workflow_ids.realistic}}"
  prompt: "{{paradoxe_compiled_prompt}}"
  reference_image_url: "{{dep_vis_004.character.reference_url}}"
  reference_image_strength: 0.85
  negative_prompt: "illustration, cartoon, anime, ghibli, stylized, smooth skin, perfect symmetry, stock photo, generic"
  aspect_ratio: "{{vcb.aspect_ratio}}"
  quality: "high"

block_c_validation:
  - "AGSS score ≥ 6.5 (Visual Validation Agent)"
  - "Authenticity items 1-3 passed (expression naturalness, facial proportion, skin texture)"
  - "Character drift check against DEP-VIS-004 reference"
  - "On failure: one automatic regeneration with enhanced specificity"

output:
  format: "generated_image_url"
  fields: ["output_url", "task_id", "agss_score", "authenticity_check_results"]
```

---

**SKILL-IMG-008: RunningHub Ghibli Style Generation**

```yaml
skill_id: "SKILL-IMG-008"
skill_name: "runninghub_ghibli_illustration"
skill_family: "image_research"
composable: true
applicable_when: "image_type = conceptual_contrast_illustration OR supervisual_abstract"
tier: 4

block_a_invariants:
  - "EXCLUSIVELY for Conceptual Contrast and Supervisual formats"
  - "NEVER used for any carousel format"
  - "NEVER used for Observational Humor"
  - "NEVER used when a real photograph can represent the concept"
  - "Ghibli style signals: distilled truth, not documentary claim"
  - "LoRA specified in workflow when available — falls back to Ghibli style prompt"

block_b_runtime_injections:
  workflow_id: "{{dep_vis_002.runninghub_workflow_ids.ghibli}}"
  prompt: "{{paradoxe_compiled_ghibli_prompt}}"
  lora_id: "{{dep_vis_007.active_ghibli_lora_id}}"
  style_preset: "ghibli_illustration"
  negative_prompt: "photorealistic, cinematic, stock photo, 3d render, blurry"
  aspect_ratio: "{{vcb.aspect_ratio}}"

block_c_validation:
  - "Style consistency check: illustration grammar confirmed, not photorealistic drift"
  - "Concept legibility: the abstract concept is visually readable"
  - "On failure: one automatic regeneration"

output:
  format: "generated_image_url"
  fields: ["output_url", "task_id", "style_confirmed"]
```

---

**SKILL-IMG-009: Photo Deck Query**

```yaml
skill_id: "SKILL-IMG-009"
skill_name: "photo_deck_query"
skill_family: "image_research"
composable: true
applicable_when: "image_type = named_person_coach"

block_a_invariants:
  - "Only invoked for coach image slots"
  - "Queries Notion Personal Branding Photo Deck database"
  - "Match must be on emotional register AND setting — not just availability"
  - "If no photo matches the required register: return no_viable_result AND generate photo session recommendation"
  - "Photo session recommendation is logged in VPO and surfaced in Notion coach card"

block_b_runtime_injections:
  notion_database_id: "{{coach_photo_deck_notion_db_id}}"
  query_filter:
    emotional_register: "{{vcb.slide.arc_stage}}"
    setting_tags: "{{derived_from_environmental_grammar}}"
  results_limit: 5

block_c_validation:
  - "Returned photo must match emotional register of arc stage (operator tagged at upload)"
  - "If no match: generate photo session recommendation, return no_viable_result"

output:
  format: "photo_deck_match"
  fields: ["notion_file_url", "photo_id", "emotional_register_tag", "setting_tag", "match_confidence"]
```

---

### 4.3 Aurore's Image Research Execution

Aurore receives the VCB and executes image research for all slides in parallel. For each slide she:

1. Reads the `image_type` and `image_sourcing_tier` fields from the VCB
2. Assembles the correct skill combination from the composable skill library based on the JIT compiler's skill routing table
3. Executes the appropriate skills concurrently
4. Scores returned candidates against the slide's PSSL parameters
5. Selects the highest-scoring viable real image (Tier 1 or 2) when available
6. Escalates to RunningHub (Tier 3 or 4) when no viable real image is found

**Skill routing table (JIT compiled per slide):**

```yaml
image_type_to_skills:
  environment_scene:
    primary: ["SKILL-IMG-001", "SKILL-IMG-002", "SKILL-IMG-003"]
    secondary: ["SKILL-IMG-005"]
    fallback: "SKILL-IMG-007"
    execution: "parallel_primary_then_secondary_if_needed"

  motion_content:
    primary: ["SKILL-IMG-004"]
    fallback: ["SKILL-IMG-001", "SKILL-IMG-002"]
    execution: "sequential"

  named_person_coach:
    primary: ["SKILL-IMG-009"]
    fallback: "photo_session_recommendation_no_ai_substitute"
    execution: "direct"

  named_person_public_figure:
    prerequisite_check: "DEP-VIS-006 registry lookup"
    primary: ["SKILL-IMG-006"]
    fallback: "SKILL-IMG-007"
    execution: "sequential"

  character_specific_emotion:
    primary: ["SKILL-IMG-007"]
    no_stock_search: true
    execution: "direct"

  character_brand_avatar:
    primary: ["SKILL-IMG-007"]
    requires: "DEP-VIS-004 reference_url"
    no_stock_search: true
    execution: "direct"

  conceptual_contrast_illustration:
    primary: ["SKILL-IMG-008"]
    no_stock_search: true
    execution: "direct"

  supervisual_abstract:
    primary: ["SKILL-IMG-008"]
    no_stock_search: true
    execution: "direct"
```

### 4.4 The Image Resolution Map

Aurore outputs an `image_resolution_map` — a JSON object mapping every slide to its resolved image:

```json
{
  "vcb_id": "VCB-20260317-0042",
  "resolution_map": [
    {
      "slide_number": 1,
      "image_type": "environment_scene",
      "resolution_tier": 2,
      "resolution_source": "SKILL-IMG-001",
      "resolved_image_url": "https://images.unsplash.com/photo-abc123.jpg",
      "pssl_match_score": 0.78,
      "runninghub_required": false,
      "attribution": "Photo by John Doe on Unsplash"
    },
    {
      "slide_number": 4,
      "image_type": "character_brand_avatar",
      "resolution_tier": 3,
      "resolution_source": "SKILL-IMG-007",
      "resolved_image_url": null,
      "runninghub_required": true,
      "runninghub_workflow_id": "RH-WF-CAROUSEL-SEMI-001",
      "paradoxe_prompt_required": true
    }
  ]
}
```

Paradoxe only receives slides where `runninghub_required: true`. The Canva App receives the complete resolution map and places both real images and generated images into their respective canvas layer slots.

### 4.5 Known Persons Registry (DEP-VIS-006)

A new dependency storing metadata on public figures the coaching audience recognizes and who may be referenced in scripts:

```json
{
  "person_id": "KP-001",
  "full_name": "Brené Brown",
  "known_for": "Vulnerability and shame research, coaching space recognition",
  "search_aliases": ["Brene Brown", "Brené Brown researcher"],
  "coaching_segments_applicable": ["conscious_business", "healing_transformation"],
  "image_usage_contexts": ["credibility_reference", "story_evidence", "cral_m3_undeniable"],
  "last_serper_search": "2026-03-01"
}
```

A person must be in DEP-VIS-006 before SKILL-IMG-006 can be invoked. Adding new persons to the registry requires operator action — not automated population.

---

## Section 5 — The Visual Recipe Protocol Library

### 5.1 Library Overview

**Dependency ID:** DEP-VIS-002
**Format:** YAML

Each recipe now includes `default_image_types` per slide position — the expected image type for each slot in the sequence.

### 5.2 Recipe Protocol Specifications

#### RECIPE-001: Relief Peak Carousel

```yaml
protocol_id: "relief_peak_carousel_recipe"
format: "carousel"
aspect_ratio: "4:5"
canvas_dimensions: "1080x1350"
visual_styles_permitted: ["cinematic_color_graded", "semi_realistic_digital"]
arc_type: "tension_release"
slide_count: {minimum: 4, default: 5, maximum: 6}
semiotic_injection_position: "latter_third — exhale moment, typically penultimate slide"
default_image_types:
  struggle_slides: "environment_scene"
  climax_slide: "character_brand_avatar"
  resolution_slide: "environment_scene OR character_brand_avatar"
first_person_pov_slides: [1, 2]
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
slide_count: {minimum: 5, default: 6, maximum: 7}
semiotic_injection_position: "cliff_slide — latter_third"
default_image_types:
  accumulation_slides: "environment_scene"
  cliff_slide: "environment_scene OR character_brand_avatar"
  resolution_slide: "environment_scene"
accumulation_prohibition: true
coach_handle_bar: "final_slide_only"
template_ids:
  semi_realistic: "TPL-DOPAMINE-CLIFF-SEMI-001"
  cinematic: "TPL-DOPAMINE-CLIFF-CINE-001"
```

#### RECIPE-003: 9-Grid Accumulation

```yaml
protocol_id: "nine_grid_recipe"
format: "single_image_grid"
aspect_ratio: "4:5"
canvas_dimensions: "1080x1350"
visual_styles_permitted: ["semi_realistic_digital", "cinematic_color_graded"]
default_image_types:
  all_8_surrounding_cells: "environment_scene"
  center_label_cell: "text_only"
accumulation_prohibition: true
coach_handle_bar: false
template_ids:
  default: "TPL-9GRID-001"
```

#### RECIPE-004: Listicle Visual

```yaml
protocol_id: "listicle_visual_recipe"
format: "carousel"
aspect_ratio: "4:5"
canvas_dimensions: "1080x1350"
visual_styles_permitted: ["cinematic_color_graded", "semi_realistic_digital"]
arc_type: "discovery_revelation"
slide_count: {minimum: 3, default: 5, maximum: 6}
semiotic_injection_position: "latter_third — revelation moment"
default_image_types:
  mood_setter_slide_1: "environment_scene"
  list_item_slides: "environment_scene"
  climax_slide: "environment_scene OR character_brand_avatar"
note: "ALL subtypes including funny_relatable use semi_realistic_digital — NOT Ghibli"
coach_handle_bar: "final_slide_only"
template_ids:
  base: "TPL-LISTICLE-001"
```

#### RECIPE-005: Visual Timeline

```yaml
protocol_id: "visual_timeline_recipe"
format: "carousel"
aspect_ratio: "4:5"
canvas_dimensions: "1080x1350"
visual_styles_permitted: ["cinematic_color_graded", "semi_realistic_digital"]
arc_type: "discovery_revelation"
slide_count: {minimum: 7, default: 8, maximum: 9}
default_image_types:
  all_timeline_slides: "environment_scene"
coach_handle_bar: "final_slide_only"
```

#### RECIPE-006: Comparison

```yaml
protocol_id: "comparison_archetypes_recipe"
format:
  single_contrast: "single_image"
  multiple_contrasts: "carousel"
aspect_ratio:
  single_image: "4:5 or 1:1"
  carousel: "4:5"
visual_styles_permitted: ["cinematic_color_graded", "semi_realistic_digital"]
arc_type: "contrast_resolution"
default_image_types:
  comparison_slides: "environment_scene OR character_brand_avatar"
  note: "Real photos of coach or recognized public figures take priority when applicable"
gaze_architecture_rule: "Side A gaze toward upper center. Side B gaze toward lower center. X-pattern not collision."
background_primary_signal_rule: "Background color carries primary emotional differentiation — processes 25ms before character"
coach_handle_bar:
  single_image: true
  carousel_final_slide: true
  carousel_interior_slides: false
template_ids:
  single_4x5: "TPL-COMPARISON-SINGLE-4x5-001"
  single_1x1: "TPL-COMPARISON-SINGLE-1x1-001"
  carousel: "TPL-COMPARISON-CAROUSEL-001"
```

#### RECIPE-007: Conceptual Contrast

```yaml
protocol_id: "conceptual_contrast_recipe"
format:
  philosophical_simultaneous: "single_image"
  transformational_sequential: "carousel"
aspect_ratio:
  single_image: "1:1"
  carousel: "4:5"
visual_style:
  single_image: "ghibli_illustration — REQUIRED"
  carousel: "cinematic_color_graded OR semi_realistic_digital"
style_rationale: "Ghibli for simultaneous conceptual contrast because illustration permits scenario-based character comparisons impossible to source reliably through photography. Carousel transformational uses realistic style."
arc_type: "contrast_resolution"
default_image_types:
  single_image: "conceptual_contrast_illustration"
  carousel_slides: "environment_scene OR character_brand_avatar"
coach_handle_bar:
  single_image: true
  carousel_final_slide: true
template_ids:
  simultaneous_1x1: "TPL-CONTRAST-SINGLE-1x1-001"
  sequential_carousel: "TPL-CONTRAST-CAROUSEL-001"
runninghub_workflow_ids:
  ghibli: "RH-WF-SINGLE-GHIBLI-001"
  carousel: "RH-WF-CONTRAST-001"
```

#### RECIPE-008: Supervisual

```yaml
protocol_id: "supervisual_recipe"
format: "single_image"
aspect_ratio: "1:1"
canvas_dimensions: "1080x1080"
visual_style: "ghibli_illustration — REQUIRED"
style_rationale: "Supervisuals represent abstract philosophical concepts that exist beyond what any physical scenario or real photograph can represent. Ghibli signals: distilled truth, not documentary claim."
arc_type: "identity_declaration"
default_image_types:
  single_frame: "supervisual_abstract"
coach_handle_bar: true
template_ids:
  ghibli: "TPL-SUPERVISUAL-GHIBLI-001"
runninghub_workflow_ids:
  ghibli: "RH-WF-SINGLE-GHIBLI-001"
```

#### RECIPE-009: Observational Humor

```yaml
protocol_id: "observational_humor_recipe"
format: "single_image"
aspect_ratio: "1:1 or 4:5"
canvas_dimensions: "1080x1080 or 1080x1350"
visual_style: "real_image_REQUIRED — no illustration, no AI character"
style_rationale: "The benign violation mechanism requires the viewer to feel 'yes that IS real life.' Illustration or AI generation removes the authenticity signal that makes the recognition fire. The humor lands on 'I recognize this from real life' not 'this is a clever illustration of the concept.'"
arc_type: "benign_violation_recognition"
default_image_types:
  single_frame: "environment_scene"
image_sourcing_note: "Stock image search runs first. If no viable real image found: escalate to RunningHub Tier 3 realistic (not Ghibli). Never use illustration for this format."
coach_handle_bar: true
template_ids:
  standard: "TPL-OBS-HUMOR-001"
```

#### RECIPE-010: Worst Case Scenario

```yaml
protocol_id: "worst_case_scenario_recipe"
format: "single_image"
aspect_ratio: "4:5"
canvas_dimensions: "1080x1350"
visual_style: "desaturated_cinematic_realism — real image preferred, RunningHub fallback"
style_rationale: "Credibility of the possible must be maintained. Winkielman-Cacioppo dual signal: fear from content + micro-smile from fluency fires simultaneously. Real desaturated photography produces stronger somatic fear-recognition than AI generation."
arc_type: "fear_recognition"
default_image_types:
  single_frame: "environment_scene"
saturation_override: "20-35% maximum — applied in Canva App post-placement"
coach_handle_bar: true
template_ids:
  default: "TPL-WCS-001"
```

#### RECIPE-011: Poll Visuals

```yaml
protocols: ["poll_visual_recipe", "archetypical_poll_recipe", "controversial_dilemma_poll_recipe"]
format: "single_image"
aspect_ratio: "9:16"
canvas_dimensions: "1080x1920"
visual_styles_permitted: ["semi_realistic_digital", "real_image_composite"]
note: "All poll variants are single image. Archetypical Poll is NOT a carousel."
default_image_types:
  option_zones: "environment_scene OR character_brand_avatar"
gaze_rule: "Side A gaze toward upper center. Side B gaze toward lower center. Never mutual collision."
coach_handle_bar: false
template_ids:
  stereotypical: "TPL-POLL-STEREO-001"
  archetypical: "TPL-POLL-ARCH-001"
  dilemma: "TPL-POLL-DILEMMA-001"
```

#### RECIPE-012: Tweet-Style Quote

```yaml
protocol_id: "tweet_quote_recipe"
format: "single_image"
aspect_ratio: "1:1"
canvas_dimensions: "1080x1080"
visual_style: "minimal — text is the primary visual"
default_image_types:
  background: "environment_scene — minimal, serves text not competes with it"
coach_handle_bar: true
template_ids:
  default: "TPL-TWEET-QUOTE-001"
```

#### VIDEO FORMATS (Visual Brief Export Only)

```yaml
video_only_formats: ["case_study_recipe", "debunking_myths_scams_recipe", "recognition_story_reel_recipe", "tier_list_hybrid_recipe"]
output_type: "visual_brief_export"
no_image_generation: true
```

---

## Section 6 — The 30 Visual Design Architecture Specifications

*(Sections 6 specifications are unchanged from V2. All 30 SPEC entries remain as documented in CVE Documentation V2.0 with one correction to SPEC-22.)*

**SPEC-22 — CORRECTED: Visual Style Selection by Format and Relationship Stage**

*Mechanism:* Style is constrained first by format, then by archetype, then by TII score.

Format constraints (binding, no override):
- All carousel formats → cinematic or semi-realistic only. Ghibli never on carousels.
- All poll formats → semi-realistic or real image composite. No Ghibli, no cinematic desaturated.
- Conceptual Contrast single image → Ghibli required
- Supervisuals → Ghibli required
- Observational Humor → real image required, never illustration

Archetype overrides (applied after format, before TII):
- Worst Case Scenario → desaturated cinematic always
- Fear-anxiety emotional angle → desaturated cinematic always

TII score applied when no override and format permits non-illustration styles:
- TII < 25 → cinematic color-graded
- TII 26-70 → semi-realistic digital
- TII > 70 → semi-realistic digital (carousel) or Ghibli (single image supervisual/contrast only)

---

## Section 7 — The PSSL Brief Schema and Prompt Generation Engine

### 7.1 Paradoxe: Upgraded Role

**Agent Name:** Paradoxe (upgraded)
**Role:** PSSL Prompt Compiler
**New scope:** Paradoxe only compiles prompts for slides where Aurore's `image_resolution_map` shows `runninghub_required: true`. Slides resolved by real images do not go through Paradoxe.

### 7.2 Two Prompt Modes

**Mode A — Realistic Cinematic (SKILL-IMG-007)**
All prompts in this mode target photorealistic, cinematic output. Negative prompt always includes: `illustration, cartoon, anime, ghibli, stylized, smooth skin, perfect symmetry, stock photo, generic`.

**Mode B — Ghibli Illustration (SKILL-IMG-008)**
All prompts in this mode target Studio Ghibli illustration style. Negative prompt includes: `photorealistic, cinematic photography, 3d render, stock photo, blurry, western cartoon`.

Mode is determined by the slide's `image_type` field in the VCB — no manual selection.

### 7.3 PSSL Field-to-Prompt Translation Rules

*(Translation rules unchanged from V2 — see CVE Documentation V2.0 Section 7.2)*

Anti-Generic Constraint Block (appended to all Tier 3 prompts):
```
"NOT: generic stock photography aesthetic. NOT: Canva template styling. NOT: perfectly symmetrical composition. NOT: artificial studio lighting setup. NOT: the visual average of coaching photography."
```

Anti-Generic Block for Ghibli (appended to all Tier 4 prompts):
```
"NOT: western animation style. NOT: Disney aesthetic. NOT: harsh outlines. Studio Ghibli illustration style — soft, warm, emotionally expressive. The concept must be immediately legible to a non-art-educated viewer."
```

---

## Section 8 — The Conscious Canva App Architecture

### 8.1 Architectural Role

The Conscious Canva App is the composition, editing, and approval layer. Three jobs:
1. Pre-populated template loading from VCB JSON
2. Image placement — receives both real image URLs (from Aurore) and generated image URLs (from RunningHub) and places them into correct canvas layer slots
3. Human editing layer — full canvas editing for the 5% exception

### 8.2 In-App Image Search Panel

All five image APIs are available directly inside the Canva App composition view. This allows the operator to search and replace any image without leaving the composition environment — no separate tab, no re-running the full Aurore pipeline for a single swap.

The in-app search panel is a sidebar that opens when any image layer is selected. It provides:

```
┌─────────────────────────────────────────┐
│ IMAGE SEARCH                            │
│                                         │
│ Query: [________________________] [🔍]  │
│                                         │
│ Sources:                                │
│ [x] Unsplash  [x] Pexels  [x] Pixabay  │
│ [x] SERPER    [ ] GIPHY                 │
│                                         │
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐   │
│ │ img  │ │ img  │ │ img  │ │ img  │   │
│ └──────┘ └──────┘ └──────┘ └──────┘   │
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐   │
│ │ img  │ │ img  │ │ img  │ │ img  │   │
│ └──────┘ └──────┘ └──────┘ └──────┘   │
│                                         │
│ [Generate with AI instead →]            │
└─────────────────────────────────────────┘
```

**API integrations in the Canva App:**

The canva-clone base has Unsplash built in. The following additions are required:

```javascript
// Pexels integration
const PEXELS_API = "https://api.pexels.com/v1/search";
// Headers: {"Authorization": process.env.PEXELS_API_KEY}

// Pixabay integration
const PIXABAY_API = "https://pixabay.com/api/";
// Params: {key: process.env.PIXABAY_API_KEY, image_type: "photo"}

// GIPHY integration (activated when GIPHY checkbox selected)
const GIPHY_API = "https://api.giphy.com/v1/gifs/search";
// Params: {api_key: process.env.GIPHY_API_KEY, rating: "pg"}

// SERPER integration
const SERPER_API = "https://google.serper.dev/images";
// Headers: {"X-API-KEY": process.env.SERPER_API_KEY}
```

All searches run client-side in the app through a lightweight API proxy layer. Results display as thumbnails in the panel. Single click replaces the selected canvas layer.

The "Generate with AI instead →" button opens a RunningHub generation panel where the operator can trigger Paradoxe prompt compilation for the selected slide and submit directly to RunningHub from within the app.

### 8.3 Template Library — Aspect Ratio Additions

1:1 templates added to the library:

```
TPL-COMPARISON-SINGLE-1x1-001: Comparison Single Contrast | 1:1 | 1080×1080
TPL-CONTRAST-SINGLE-1x1-001: Conceptual Contrast Simultaneous | Ghibli | 1:1 | 1080×1080
TPL-SUPERVISUAL-GHIBLI-001: Supervisual | Ghibli | 1:1 | 1080×1080
TPL-OBS-HUMOR-001: Observational Humor | Real Image | 1:1 or 4:5 | 1080×1080 or 1080×1350
TPL-TWEET-QUOTE-001: Tweet-Style Quote | 1:1 | 1080×1080
```

### 8.4 Component Library Update

**Component I — In-App Image Search Panel**
New component not in canva-clone base. Available on any image layer slot via sidebar. Queries all five APIs simultaneously with configurable source toggles. Includes "Generate with AI" fallback trigger.

*(All other components unchanged from V2 — see CVE Documentation V2.0 Section 8.2)*

### 8.5 Template Wireframes — 1:1 Additions

**TPL-CONTRAST-SINGLE-1x1-001 — Conceptual Contrast | Ghibli | 1:1**

```
┌──────────────────────────────────────┐ ← 1080px
│ ○ Coach Name          [Logo]  [A]    │ ← Handle bar 100px
├──────────────────────────────────────┤
│                                      │
│  [B] HOOK TEXT ← top zone            │
│      The philosophical question      │
│      Bold, large                     │
│                                      │
│ ┌─────────────┬──────────────────┐   │
│ │ [D-A] Left  │  [D-B] Right     │   │
│ │ Concept A   │  Concept B       │   │
│ │ Ghibli illus│  Ghibli illus    │   │
│ └─────────────┴──────────────────┘   │
│                                      │
│  [C] Bottom text — resolution        │
│      The insight that bridges both   │
│                                      │
└──────────────────────────────────────┘ ← 1080px
```

**TPL-SUPERVISUAL-GHIBLI-001 — Supervisual | Ghibli | 1:1**

```
┌──────────────────────────────────────┐
│ ○ Coach Name          [Logo]  [A]    │
├──────────────────────────────────────┤
│                                      │
│                                      │
│  [D] Full-Frame — Ghibli illustration│
│      Single abstract concept         │
│      Emotionally self-evident        │
│      No explanation needed           │
│                                      │
│                                      │
│  [B] TEXT ← minimal, serves image    │
│      1-4 words maximum               │
│      Light weight, integrated        │
│                                      │
└──────────────────────────────────────┘
```

**TPL-TWEET-QUOTE-001 — Tweet-Style Quote | 1:1**

```
┌──────────────────────────────────────┐
│ ✓ Coach Name  @handle  [A-modified]  │
├──────────────────────────────────────┤
│                                      │
│                                      │
│  [B] QUOTE TEXT ← dominant center    │
│      Large, bold weight              │
│      Text IS the visual              │
│      Tribal noun required            │
│                                      │
│  [D] Minimal background              │
│      Serves the text                 │
│                                      │
│                                      │
│ ♥  💬  ↗                            │
└──────────────────────────────────────┘
```

---

## Section 9 — RunningHub API Integration

*(Unchanged from V2. See CVE Documentation V2.0 Section 9 for full API specification, workflow library, reference image architecture, and error handling.)*

**Updated workflow library entries:**

| Workflow ID | Format | Style | Notes |
|---|---|---|---|
| RH-WF-CAROUSEL-SEMI-001 | Carousel | Semi-Realistic | Character reference input |
| RH-WF-CAROUSEL-CINE-001 | Carousel | Cinematic | Real photo reference optional |
| RH-WF-CAROUSEL-CLIFF-001 | Dopamine Cliff | Dynamic temperature | Desaturation override on cliff slide |
| RH-WF-SINGLE-SEMI-001 | Single Image | Semi-Realistic | Standard character generation |
| RH-WF-SINGLE-CINE-DESAT-001 | Single Image | Desaturated Cinematic | Worst Case Scenario + Fear-Anxiety |
| RH-WF-SINGLE-GHIBLI-001 | Single Image | Ghibli + LoRA | Conceptual Contrast + Supervisuals ONLY |
| RH-WF-COMPARISON-001 | Comparison | Semi-Realistic | Two-character gaze architecture |
| RH-WF-POLL-001 | Poll | Semi-Realistic | Two-zone split layout |
| RH-WF-GRID9-001 | 9-Grid | Semi-Realistic | 8 image cells |
| RH-WF-LISTICLE-001 | Listicle | Semi-Realistic | Standard carousel |
| RH-WF-TIMELINE-001 | Timeline | Semi-Realistic | Chronological color arc |

---

## Section 10 — New Agents, Dependencies, and Registry Updates

### 10.1 New Dependencies — Registry V5.2

**DEP-VIS-001: Tribal Imagen Activation Registry (TIAR)**
*(Unchanged from V2)*

**DEP-VIS-002: Visual Recipe Protocol Library**
*(Updated with image_type defaults per slide position)*

**DEP-VIS-003: Stage Set Emotional Architecture Library**
*(Unchanged from V2)*

**DEP-VIS-004: Brand Character Reference Archive**
*(Unchanged from V2)*

**DEP-VIS-005: Visual Composition Brief Schema**
*(Updated with image_type, image_sourcing_tier, image_search_query, image_search_fallback_query, image_search_skills_to_invoke fields per slide)*

**DEP-VIS-006: Known Persons Registry** *(NEW)*
Format: Supabase JSONB
Tier: 1
Parent: DEP-ENG-007 (Tribe Intelligence)
Contains: Named real persons the coaching audience recognizes who may be referenced in scripts. Prerequisite for SKILL-IMG-006 invocation. Operator-managed — not automated.
Update: Manual operator addition when new recognized persons appear in CRAL research

**DEP-VIS-007: Ghibli LoRA Registry** *(NEW)*
Format: JSON
Tier: 1
Contains: Active LoRA IDs for Ghibli style generation in RunningHub, versioned, with fallback to style prompt when no LoRA is loaded
Update: On LoRA update or addition

### 10.2 New Agent

**Visual Validation Agent** *(unchanged from V2)*

### 10.3 Upgraded Agents

**Aurore — Image Research Planner** *(upgraded from Visual Asset Researcher)*

New capabilities:
- Multi-API image research orchestration across nine composable skills
- JIT skill assembly per slide based on `image_type` field
- PSSL-parameter-based image scoring and candidate ranking
- Known persons registry lookup and SERPER known persons search
- Photo Deck query with emotional register matching
- Image resolution map generation
- Parallel slide processing
- RunningHub escalation flagging

New reads: DEP-VIS-005 (VCB image fields), DEP-VIS-006 (Known Persons Registry), DEP-VIS-004
New tools: Nine composable SKILL-IMG-001 through SKILL-IMG-009 files

**Abel — Visual Composition Planner** *(updated from V2)*

New capabilities added to V2 spec:
- `image_type` assignment per slide
- `image_search_query` generation per slide (derived from tribal_noun_visual_congruent and environmental_grammar)
- `image_search_fallback_query` generation
- `image_search_skills_to_invoke` list population per slide
- Known persons check from script JSON `known_persons_referenced` field

**Paradoxe — PSSL Prompt Compiler** *(updated from V2)*

New scope clarification: Only compiles prompts for slides where Aurore's resolution map shows `runninghub_required: true`. Receives the filtered resolution map from Aurore, not the full VCB.

Two prompt modes: Realistic Cinematic (Mode A) and Ghibli Illustration (Mode B), determined by slide `image_type`.

### 10.4 New Composable Skills

Nine new SKILL.md files added to the skill library:

| Skill ID | Skill Name | Tier Served | API |
|---|---|---|---|
| SKILL-IMG-001 | unsplash_image_search | 2 | Unsplash API |
| SKILL-IMG-002 | pexels_image_search | 2 | Pexels API |
| SKILL-IMG-003 | pixabay_image_search | 2 | Pixabay API |
| SKILL-IMG-004 | giphy_search | 2 | GIPHY API |
| SKILL-IMG-005 | serper_general_image_search | 2 | SERPER API |
| SKILL-IMG-006 | serper_known_persons_search | 1 | SERPER API + DEP-VIS-006 |
| SKILL-IMG-007 | runninghub_realistic_character | 3 | RunningHub |
| SKILL-IMG-008 | runninghub_ghibli_illustration | 4 | RunningHub + LoRA |
| SKILL-IMG-009 | photo_deck_query | 1 | Notion API |

All nine follow the standard JIT SKILL.md three-block schema and are composable — Aurore assembles them at runtime based on the slide's `image_type` field.

### 10.5 New Validation Gate Updates

**Gate C-09 additions:**

Added checks:
- All slides: `image_type` field present and valid value from permitted list
- All slides: `image_search_query` present and non-generic (must contain at least one tribal noun or specific environmental descriptor)
- Character slides: `image_type` is `character_brand_avatar` or `character_specific_emotion` — never `environment_scene`
- Ghibli slides: `image_type` is `conceptual_contrast_illustration` or `supervisual_abstract` — never applied to carousel slides
- Observational Humor: `image_type` is `environment_scene` — never `conceptual_contrast_illustration` or `supervisual_abstract`

### 10.6 New Python Tool

**`multi_api_image_search.py`**
Unified image search wrapper for Aurore's multi-API execution. Handles: concurrent API calls across Unsplash/Pexels/Pixabay/GIPHY/SERPER, PSSL-parameter-based scoring of returned results, candidate ranking and threshold filtering, resolution map assembly.

Environment variables required: `UNSPLASH_ACCESS_KEY`, `PEXELS_API_KEY`, `PIXABAY_API_KEY`, `GIPHY_API_KEY`, `SERPER_API_KEY`

---

## Section 11 — The Full Output JSON Contract

*(VPO schema unchanged from V2 with one addition — image attribution tracking)*

```json
{
  "vpo_id": "VPO-20260317-0042",
  "image_attribution_log": [
    {
      "slide_number": 1,
      "image_source": "unsplash",
      "image_url": "https://images.unsplash.com/photo-abc123.jpg",
      "attribution": "Photo by John Doe on Unsplash",
      "pssl_match_score": 0.78,
      "sourcing_tier": 2
    },
    {
      "slide_number": 4,
      "image_source": "runninghub",
      "image_url": "https://runninghub-output.io/output/abc123.png",
      "workflow_id": "RH-WF-CAROUSEL-SEMI-001",
      "agss_score": 7.4,
      "sourcing_tier": 3
    }
  ]
}
```

---

## Section 12 — Production Governance, Quality Gates, and Notion Delivery

### 12.1 The Six-Gate Visual Quality Sequence

*(Five gates from V2 remain. One new gate added.)*

**Gate V-00: Image Type Validity Check** *(NEW — runs before Gate V-01)*
Checks: All slides have valid `image_type` values, Ghibli image types only appear on Conceptual Contrast and Supervisual formats, Observational Humor slides have `environment_scene` image type only
On failure: Abel revises image_type assignments before proceeding

**Gates V-01 through V-05:** *(unchanged from V2)*

### 12.2 Notion Visual Content Card

*(Unchanged from V2 with one addition)*

**Image Sourcing Summary** (new field in Technical Audit section — collapsed by default):
Per-slide breakdown showing: source API, PSSL match score, sourcing tier. Gives operator visibility into how many slides used real images vs generated images. Over time this data feeds into the TIAR performance tracking — tribal noun-visual congruent pairs that consistently require RunningHub fallback (no viable real image found) are flagged for stock search query refinement.

### 12.3 Weekly Visual Production Allocation

*(Unchanged from V2)*

### 12.4 Complete Sovereign Image Rule

*(V2 rules 1-4 unchanged. Rule 5 added in Section 1.3 of this document.)*

---

## Appendix A — Registry V5.2 Delta (V3 Additions to V2)

**New Dependencies:**
- DEP-VIS-006: Known Persons Registry — Tier 1
- DEP-VIS-007: Ghibli LoRA Registry — Tier 1

**New Composable Skills:**
- SKILL-IMG-001 through SKILL-IMG-009 (nine image search/generation skills)

**Upgraded Agents:**
- Aurore: Visual Asset Researcher → Image Research Planner
- Abel: Visual Composition Planner (updated with image_type assignment)
- Paradoxe: PSSL Prompt Compiler (updated scope — Tier 3/4 only)

**New Validation Gate:**
- Gate V-00: Image Type Validity Check

**New Python Tool:**
- `multi_api_image_search.py`

**New Environment Variables Required:**
- `UNSPLASH_ACCESS_KEY`
- `PEXELS_API_KEY`
- `PIXABAY_API_KEY`
- `GIPHY_API_KEY`
- `SERPER_API_KEY`

---

## Appendix B — PRD Functional Requirements Update (V3 Additions)

**FR-VIS-09:** The system executes a multi-API image research pass (Aurore Image Research Planner) for every slide requiring visual content before any RunningHub AI generation is triggered. Stock image sources — Unsplash, Pexels, Pixabay, GIPHY, SERPER — are searched first. RunningHub is only invoked for slides where stock search returns no viable result, or for character-type and Ghibli-type image slots where real photography is not the appropriate source.

**FR-VIS-10:** The system maintains a Known Persons Registry (DEP-VIS-006) of real public figures the coaching audience recognizes. When a named person is referenced in a script, SERPER image search attempts to source a real photograph of that person in the relevant context before any AI generation is attempted.

**FR-VIS-11:** The Conscious Canva App provides an in-app image search panel accessible on any image layer, querying all five stock APIs (Unsplash, Pexels, Pixabay, GIPHY, SERPER) simultaneously. Operators can search, preview, and replace any image without leaving the composition environment.

**FR-VIS-12:** Ghibli illustration style (Tier 4 sourcing) is available exclusively for Conceptual Contrast single image compositions and Supervisual single image compositions. It is architecturally blocked from all carousel formats, all poll formats, and all Observational Humor formats. This constraint is enforced at Gate V-00 before any composition proceeds.

**FR-VIS-13:** The system supports three aspect ratios: 4:5 (1080×1350px) for carousels and standard single images, 1:1 (1080×1080px) for tweet quotes, supervisuals, observational humor, and single-contrast comparisons, and 9:16 (1080×1920px) for all poll variants. Template selection in the Canva App enforces the correct canvas dimensions per recipe protocol.

---

*End of CVE Documentation V3.0*
*Supersedes: CVE Documentation V2.0 (2026-03-17)*
*Next update triggered by: Multi-API image search wrapper build, Known Persons Registry initial population, Ghibli LoRA registration, Canva App in-app search panel implementation*
