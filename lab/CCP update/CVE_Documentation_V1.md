# Conscious Visual Engine (CVE) — System Documentation V1.0

**Author:** Emilio  
**Date:** 2026-03-17  
**Version:** 1.0  
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

The CVE produces three output types, all of which feed into the coach's Notion workspace:

**Type 1 — Carousel Compositions:** Multi-slide visual sequences (4-9 slides) for the Instagram carousel format. Built from the 12 Visual Recipe Protocols and rendered through RunningHub.

**Type 2 — Single Image Compositions:** Standalone visual posts — memes, tweet-style quotes, poll visuals, observational humor frames, worst-case scenario frames. Rendered through RunningHub and editable in the Conscious Canva App.

**Type 3 — Visual Brief Exports:** For script types assigned to Short-form video (Myth Debunking, Case Studies, Tier Lists), the CVE produces a structured visual composition brief — not a final rendered image, but a scene-by-scene art direction document that guides the coach's recording setup or a video editor's work.

### 1.3 The Sovereign Image Rule Extension

The existing PRD Sovereign Image Rule states: AI-generated visual elements may only represent abstract client scenarios or metaphorical concepts — the coach's actual face is never artificially generated.

The CVE extends this rule with two additional specifications:

**Extension A:** AI-generated avatar characters (brand avatar system) and real coach photography may never appear in the same visual composition. They operate in separate content tracks and serve separate psychological functions.

**Extension B:** Real coach photography is sourced exclusively from the Personal Branding Photo Deck in Notion. The CVE's Visual Composition Planner queries the Photo Deck before planning any composition that requires real photography. If no suitable photo exists for the required emotional register, the system flags for photo session recommendation — it does not substitute with AI generation.

### 1.4 Relationship to Existing Agents

The CVE does not introduce entirely new agents for most functions — it upgrades two existing agents and introduces two new ones:

- **Abel** (existing Visual Recipe Router) is upgraded to Visual Composition Planner — full specification in Section 3
- **Paradoxe** (existing Visual Prompt Synthesizer) is upgraded to PSSL Prompt Compiler — full specification in Section 7
- **TIAR Monitor Agent** (new) — manages the Tribal Imagen Activation Registry — full specification in Section 4
- **Visual Validation Agent** (new) — post-generation quality gate — full specification in Section 10

---

## Section 2 — The Script-to-Visual Production Flow

### 2.1 Trigger Conditions

Visual production is triggered by a specific condition in the CCF pipeline: a script that has passed all three validation gates AND whose archetype classification maps to a visual format output.

The Visual Production Flag is a boolean field in the Finalized Content Output (DEP-ENG-011):

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

The flag is set by the CCF Orchestrator (Alex) at pipeline completion. When `visual_production_flag: true`, the full script JSON package is forwarded to Abel.

### 2.2 The Full Script JSON Package

The critical architectural decision of the CVE: the visual system does not receive only the script text. It receives the complete production context package that built the script. This is what makes visual-linguistic congruence possible — the visual system knows not just what the script says, but what psychological mechanisms were used to build it, which tribal language was activated, and what emotional state the audience is expected to be in when they see it.

The full script JSON package forwarded to Abel contains:

```json
{
  "asset_id": "CCFA-C01-03-26-0042",
  "script_text": "...",
  "script_components": {
    "archetype_id": "relief_peak_carousel_recipe",
    "emotional_angle": "validation_relief",
    "arc_type": "tension_release",
    "hook_text": "The 3am spiral has a name",
    "hook_concrete_nouns": ["3am", "spiral"],
    "slide_texts": ["...", "...", "...", "...", "..."],
    "semiotic_injection_slide": 4,
    "cta_text": "..."
  },
  "psychological_routing": {
    "mood_state": "escape",
    "arousal_direction": "descending",
    "valence_target": "positive",
    "regulatory_frame": "prevention",
    "semantic_affinity_risk": "low",
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

This package is the complete input to the Visual Composition Planner. No additional context is required.

### 2.3 Format-to-Recipe Routing

Before Abel begins composition planning, the system determines which of the 12 Visual Recipe Protocols the script maps to. The routing table is maintained in DEP-VIS-002 (Visual Recipe Protocol Library):

| Script Archetype | Visual Output Type | Recipe Protocol |
|---|---|---|
| Relief Peak Carousel | Carousel | `relief_peak_carousel_recipe` |
| Dopamine Cliff Carousel | Carousel | `dopamine_cliff_recipe` |
| Curiosity Listicle | Carousel | `listicle_visual_recipe` |
| Funny Relatable Listicle | Carousel | `listicle_visual_recipe` |
| Nostalgia Listicle | Carousel | `listicle_visual_recipe` |
| Visual Timeline | Carousel | `visual_timeline_recipe` |
| Comparison (all subtypes) | Carousel (2-slide) | `comparison_archetypes_recipe` |
| Archetypical Poll | Carousel (3-slide) | `archetypical_poll_recipe` |
| Case Study | Carousel | `case_study_recipe` |
| Debunking Myths | Carousel | `debunking_myths_scams_recipe` |
| Observational Humor | Single Image | `observational_humor_recipe` |
| Worst Case Scenario | Single Image | `worst_case_scenario_recipe` |
| Tweet-Style Quote | Single Image | Single frame template |
| Stereotypical Poll | Single Image | `poll_visual_recipe` |
| Controversial Dilemma | Single Image | `controversial_dilemma_poll_recipe` |
| Conceptual Contrast | Single Image or Carousel | `conceptual_contrast_recipe` |

Short-form video archetypes (Myth Debunking Reel, Recognition Story Reel, Storytelling Case Study Reel, Tier List Hybrid) receive Visual Brief Export output — not rendered compositions.

### 2.4 Pipeline Execution Sequence

The complete visual production pipeline executes in this sequence:

1. **CCF Validation Complete** → Visual Production Flag set in DEP-ENG-011
2. **TIAR Query** → Abel queries DEP-VIS-001 for current active tribal nouns for this coaching segment, confirms entropy status of nouns present in script package
3. **Visual Composition Planning** → Abel generates the full Visual Composition Brief (VCB) — all PSSL parameters per slide, template assignment, arc type confirmation, ISC-derived climax position
4. **Photo Deck Query** (if real photography required) → Abel queries Notion Photo Deck for matching emotional register photograph
5. **VCB Validation** → All required PSSL fields populated, tribal noun-visual congruent pairs confirmed, accumulation prohibition checklist passed
6. **Template Loading** → Conscious Canva App loads the assigned recipe template, pre-populates all content slots from VCB
7. **Prompt Compilation** → Paradoxe translates VCB parameters into RunningHub-ready prompt strings for each slide requiring image generation
8. **RunningHub Execution** → API call per slide requiring AI image generation, character reference images passed for avatar consistency
9. **Asset Receipt** → Generated image URLs received and mapped to canvas layer slots in Conscious Canva App
10. **AGSS Validation** → Visual Validation Agent scores each generated image against Anti-Generic Specificity Scale thresholds
11. **Authenticity Check** → Three mandatory avatar authenticity features verified per character image
12. **Canvas Composition Final** → Conscious Canva App assembles complete composition with all elements in place
13. **Receipt Chain Confirmation** → All pipeline stages logged, Receipt Chain Guard confirms unbroken audit trail
14. **Notion Delivery** → Complete visual composition card pushed to coach's Notion workspace with preview, hook text, caption, and why-this-visual rationale

---

## Section 3 — The Visual Composition Planning Agent (Abel Upgraded)

### 3.1 Agent Specification

**Agent Name:** Abel (upgraded)  
**Previous Role:** Visual Recipe Router  
**New Role:** Visual Composition Planner  
**Department:** Expression Department  
**Reads From:** DEP-ENG-011 (Full Script JSON Package), DEP-VIS-001 (TIAR), DEP-VIS-002 (Visual Recipe Protocol Library), DEP-VIS-003 (Stage Set Emotional Architecture Library), DEP-VIS-004 (Brand Character Reference Archive), DEP-ENG-016 (Psychological Routing Brief), DEP-ENG-003 (Voice DNA), DEP-ENG-007 (Tribe Intelligence)  
**Writes To:** DEP-VIS-005 (Visual Composition Brief)  
**Cannot:** Generate final user-facing text, trigger RunningHub directly, access Tier 0 dependencies

### 3.2 Abel's Decision Process

Abel executes a structured seven-step decision process when receiving a script JSON package:

**Step 1 — Arc Type Confirmation**
Abel reads the `arc_type` field from the script package and confirms it matches the assigned recipe protocol. If the arc type embedded in the script does not match the recipe protocol's documented arc, Abel flags the mismatch for operator review before proceeding. Arc type is the foundational physiological blueprint — no composition proceeds without confirmed arc type.

**Step 2 — Slide Count and ISC Position Calculation**
Abel determines slide count based on the recipe protocol specification, then calculates the semiotic injection slide using the ISC 75% rule:

```
semiotic_injection_slide = round(total_slides × 0.75)
```

For a 5-slide carousel: slide 4. For a 7-slide carousel: slide 5. For a 9-slide carousel: slide 7. This is a calculation, not a creative judgment. The facial expression injection and maximum chromatic intensity are scheduled to this position.

**Step 3 — TIAR Query**
Abel queries DEP-VIS-001 for the target coaching segment, retrieving the current active noun list with entropy scores. Abel cross-references this list against the concrete nouns present in the script's `hook_concrete_nouns` and `active_tribal_nouns` fields. Nouns with entropy above the decay threshold are flagged — if a hook noun is flagged as bleached, Abel returns a flag to the CCF pipeline requesting hook text revision before proceeding with visual production. Production is not halted but the flag enters the Receipt Chain.

**Step 4 — PSSL Parameter Generation Per Slide**
Abel generates the complete Physiological State Specification Language (PSSL) parameters for every slide in the sequence. Each slide receives all required fields (documented in full in Section 7). Abel determines these parameters by:

- Reading the arc type to determine the somatic target state per slide position (what must the viewer's body be doing at this slide?)
- Reading the recipe protocol's chromatic bloom sequence specification to set saturation percentage and temperature direction
- Reading the PAD score requirements from DEP-VIS-003 for stage set selection
- Calculating typography weight from arc stage position
- Determining visual style from the TII score in the psychological routing brief (cold TII < 25 = cinematic realism; warming TII 26-70 = semi-realistic; warm TII > 70 = Ghibli/illustration) with archetype override rules applied

**Step 5 — Tribal Noun + Visual Congruent Pairing**
For every slide containing text, Abel pairs each tribal concrete noun with a specific visual congruent — the exact scene element that will fire the dual-coding simultaneity. The pairing must be specific, not categorical. "The 3am spiral" does not pair with "person looking stressed at night" — it pairs with "phone screen at 3am showing a specific message thread, cursor visible, timestamp readable." The visual congruent is specified as a scene grammar description, not an aesthetic description.

**Step 6 — Stage Set Selection**
Abel queries DEP-VIS-003 (Stage Set Emotional Architecture Library) using the PAD score requirements for each slide position. The library returns validated stage set options meeting the required Pleasure, Arousal, and Dominance scores for that slide's position in the arc. Abel selects the option with highest tribal specificity for the coaching segment. Stage sets are specified using five grammar parameters: light quality (time-of-day signal), spatial density (object count), temporal signal (motion cues vs. stillness), world color temperature independent of key light, and subject-to-frame height ratio.

**Step 7 — Template Assignment**
Abel assigns the specific template ID from DEP-VIS-002 to the composition. Template assignment determines which canvas layout the Conscious Canva App loads, which layer slots are available for image injection, and which RunningHub workflow ID is called for image generation.

### 3.3 Visual Composition Brief (VCB) Schema

Abel's output is the VCB — the complete specification document that drives all downstream production. The VCB schema is DEP-VIS-005:

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
  "visual_style": "ghibli_illustration",
  "aspect_ratio": "square_1x1",
  "coaching_segment": "conscious_business",
  "tii_score": 45,
  "template_id": "TPL-RELIEF-PEAK-001",
  "runninghub_workflow_id": "RH-WF-CAROUSEL-GHIBLI-001",
  "slides": [
    {
      "slide_number": 1,
      "arc_stage": "tension",
      "somatic_target": {
        "corrugator_state": "active",
        "zygomaticus_state": "suppressed",
        "scr_target": "elevated",
        "dominant_biometric": "phasic_gsr_spike"
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
        "entropy_score": 0.12,
        "entropy_status": "active",
        "visual_congruent": "Phone screen visible in frame showing timestamp 03:14, draft email open — the send button visible but untouched, cursor blinking in the message body"
      },
      "first_person_pov": false,
      "accumulation_prohibition_passed": true,
      "incomplete_tribal_artifact": null
    },
    {
      "slide_number": 2,
      "arc_stage": "tension_build",
      "somatic_target": {
        "corrugator_state": "active",
        "zygomaticus_state": "suppressed",
        "scr_target": "sustained_elevated",
        "dominant_biometric": "sustained_beta_activity"
      },
      "lighting_grammar": "Same institutional overhead source maintained — environmental continuity preserving the body-memory grammar. Slight intensification of shadow depth under eyes.",
      "chromatic_spec": {
        "foundation_hue": "#2C3E50",
        "accent_hue": "#5D6D7E",
        "saturation_pct": 38,
        "saturation_direction": "slight_increase",
        "temperature_direction": "cool_stable"
      },
      "environmental_grammar": {
        "light_quality_signal": "11pm_institutional",
        "spatial_density": 11,
        "temporal_signal": "stillness_late_night",
        "world_color_temp_kelvin": 4000,
        "subject_frame_height_ratio_pct": 38,
        "pad_scores": {"pleasure": 2, "arousal": 6, "dominance": 2}
      },
      "typography": {
        "arc_stage": "tension",
        "font_category": "serif",
        "font_weight": 750,
        "primary_text": "You wrote what they wanted",
        "primary_word_count": 5,
        "secondary_text": "Not what was true",
        "body_copy": "PROHIBITED"
      },
      "tribal_noun_visual_congruent": {
        "noun": "integrity",
        "entropy_score": 0.18,
        "entropy_status": "active",
        "visual_congruent": "Values statement document partially visible in background — three of five sections completed, the fourth section blank with cursor blinking in it"
      },
      "incomplete_tribal_artifact": "Values statement with three of five sections blank — fourth section cursor blinking, incomplete"
    },
    {
      "slide_number": 3,
      "arc_stage": "peak_tension",
      "somatic_target": {
        "corrugator_state": "peak_active",
        "zygomaticus_state": "suppressed",
        "scr_target": "maximum_elevation",
        "dominant_biometric": "maximum_lpp_amplitude"
      },
      "lighting_grammar": "Maximum shadow depth. The world is at maximum restriction. Same overhead source but fill has been fully removed — deep shadows across the lower face and neck. Subject occupies smallest frame position in the sequence.",
      "chromatic_spec": {
        "foundation_hue": "#1A252F",
        "accent_hue": "#4A4A4A",
        "saturation_pct": 25,
        "saturation_direction": "minimum",
        "temperature_direction": "coldest_in_sequence"
      },
      "environmental_grammar": {
        "light_quality_signal": "11pm_institutional_maximum_isolation",
        "spatial_density": 12,
        "temporal_signal": "complete_stillness_world_asleep",
        "world_color_temp_kelvin": 3800,
        "subject_frame_height_ratio_pct": 35,
        "pad_scores": {"pleasure": 2, "arousal": 7, "dominance": 1}
      },
      "typography": {
        "arc_stage": "peak_tension",
        "font_category": "sans_serif_bold",
        "font_weight": 700,
        "primary_text": "Because losing them felt worse",
        "primary_word_count": 6,
        "secondary_text": null,
        "body_copy": "PROHIBITED"
      },
      "tribal_noun_visual_congruent": {
        "noun": "resonance",
        "entropy_score": 0.15,
        "entropy_status": "active",
        "visual_congruent": "The absence of resonance — character's posture closed, slight forward lean, arms creating a barrier. The body communicates what was compromised."
      }
    },
    {
      "slide_number": 4,
      "arc_stage": "semiotic_climax",
      "semiotic_injection": true,
      "somatic_target": {
        "corrugator_state": "transitioning_to_suppressed",
        "zygomaticus_state": "activating",
        "scr_target": "peak_then_recovery_onset",
        "dominant_biometric": "hrv_increase_onset",
        "isc_alignment": "maximum_neural_sync_75pct_mark"
      },
      "lighting_grammar": "Transition grammar — the lighting changes here for the first time in the sequence. A warm lamp source enters from the left at 45° creating a Rembrandt triangle. This is the first warm light the viewer's body has experienced in this composition. The institutional overhead diminishes. The world is beginning to change.",
      "chromatic_spec": {
        "foundation_hue": "#4A3728",
        "accent_hue": "#D4A96A",
        "saturation_pct": 72,
        "saturation_direction": "maximum_jump",
        "temperature_direction": "warm_entry"
      },
      "character_spec": {
        "semiotic_expression": "recognition_relief_authentic",
        "expression_description": "Eyes slightly widened, the specific micro-expression of recognizing a truth you had been avoiding — not happiness yet, but the relief of naming the thing. Orbicularis oculi beginning to activate. Mouth slightly parted. The face of someone who just said the real thing out loud for the first time.",
        "expression_congruence_check": "full_duchenne_onset_eye_mouth_congruent"
      },
      "environmental_grammar": {
        "light_quality_signal": "late_night_lamp_safety_entering",
        "spatial_density": 5,
        "temporal_signal": "stillness_but_changing",
        "world_color_temp_kelvin": 3200,
        "subject_frame_height_ratio_pct": 55,
        "pad_scores": {"pleasure": 5, "arousal": 5, "dominance": 4}
      },
      "typography": {
        "arc_stage": "climax",
        "font_category": "sans_serif_bold",
        "font_weight": 700,
        "primary_text": "Integrity isn't noble. It's survival.",
        "primary_word_count": 6,
        "secondary_text": null,
        "body_copy": "PROHIBITED"
      }
    },
    {
      "slide_number": 5,
      "arc_stage": "resolution_exhale",
      "peak_end_rule_priority": "HIGH",
      "somatic_target": {
        "corrugator_state": "suppressed",
        "zygomaticus_state": "fully_active",
        "scr_target": "parasympathetic_recovery",
        "dominant_biometric": "hrv_sdnn_increase",
        "peak_end_gestalt": "standalone_shareable_identity_declaration"
      },
      "lighting_grammar": "Warm diffused source from upper-left at 45°. Soft fill from right removing all harsh shadows. The subject is fully lit for the first time in the sequence. The world has opened. This slide should feel like morning after the long night.",
      "chromatic_spec": {
        "foundation_hue": "#F5ECD7",
        "accent_hue": "#C8956C",
        "saturation_pct": 65,
        "saturation_direction": "stable_warm",
        "temperature_direction": "warmest_in_sequence"
      },
      "environmental_grammar": {
        "light_quality_signal": "early_morning_diffused_window",
        "spatial_density": 3,
        "temporal_signal": "quiet_stillness_new_beginning",
        "world_color_temp_kelvin": 3000,
        "subject_frame_height_ratio_pct": 65,
        "pad_scores": {"pleasure": 7, "arousal": 2, "dominance": 7}
      },
      "typography": {
        "arc_stage": "resolution",
        "font_category": "sans_serif_light",
        "font_weight": 300,
        "primary_text": "You already know what's true",
        "primary_word_count": 6,
        "secondary_text": "The question is whether you'll say it",
        "body_copy": "PROHIBITED",
        "tracking_adjustment": "+3pct_for_fluency"
      },
      "standalone_validity": true,
      "screenshot_shareable": true
    }
  ],
  "feed_contrast_check": {
    "feed_dominant_temperature": "warm_dark",
    "composition_temperature": "cool_to_warm_arc",
    "contrast_valid": true
  },
  "accumulation_prohibition_audit": {
    "completion_imagery_detected": false,
    "achievement_signals_detected": false,
    "passed": true
  }
}
```

---

## Section 4 — The Tribal Imagen Activation Registry (TIAR)

### 4.1 Registry Specification

**Dependency ID:** DEP-VIS-001  
**Format:** Supabase JSONB + monthly corpus analysis pipeline  
**Managed By:** TIAR Monitor Agent (new)  
**Queried By:** Abel (pre-composition), Script Generation Skills (pre-generation, upstream)  
**Update Cadence:** Monthly corpus analysis, automated entropy monitoring, manual refresh on threshold trigger

The TIAR is the living lexical database that guarantees every concrete noun used in visual hooks and text elements carries currently active tribal imageability for the target coaching segment. It solves two problems simultaneously: the extraction problem (which nouns have active tribal charge right now?) and the half-life problem (when has a noun's charge expired and needs replacement?).

### 4.2 TIAR Data Structure

Each entry in the registry corresponds to one concrete noun within one coaching segment:

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
  "entropy_baseline": 0.142,
  "entropy_current": 0.188,
  "entropy_pct_above_baseline": 32.4,
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
  "last_entropy_check": "2026-03-01",
  "next_refresh_date": "2026-04-01",
  "replacement_candidates": ["liminal", "crossing", "edge_moment"],
  "activation_history": {
    "uses_last_30_days": 4,
    "performance_avg_save_rate": 0.087
  }
}
```

### 4.3 Decay Stage Classifications

The TIAR Monitor Agent assigns every noun to one of five decay stages based on Shannon entropy measurement:

| Decay Stage | Entropy vs. Baseline | Action | System Behavior |
|---|---|---|---|
| Tribal Potential | < -10% | Emerging high-value term | Flag for TIRS validation onboarding |
| In-Distribution | ±25% | Active, healthy charge | Approved for visual recipe use |
| Bleaching Onset | +26% to +50% | Monitor closely | Yellow flag in Abel's query response |
| Mainstream Dilution | +51% to +70% | Deprecate from hooks | Red flag — replaced in new productions |
| Terminal Obsolescence | > +70% | Expired | Hard block on all new productions |

### 4.4 Upstream Integration: Script Generation Skills

The TIAR's most important integration point is upstream — inside the Script Generation Skill templates, not inside the visual pipeline. This is the architectural decision that makes the congruence system coherent: concrete nouns are selected with tribal charge in mind at the script generation stage, not retroactively matched after the fact.

The Script Generation Skill template includes a mandatory pre-generation step:

```yaml
# Pre-generation TIAR query — mandatory before hook generation
tiar_query:
  target_segment: "{{coaching_segment}}"
  required_entropy_status: ["in_distribution", "tribal_potential"]
  output: "active_noun_list"
  
# Active noun list injected into script generation instruction
hook_generation_instruction: |
  Generate the hook for this {{archetype}} script.
  Required vocabulary — minimum 3 concrete nouns from this active tribal list:
  {{active_noun_list}}
  Explicitly EXCLUDE these expired terms:
  {{expired_noun_list}}
```

This means the script arrives at the visual pipeline with tribal nouns already validated. Abel's TIAR query at the visual stage is a confirmation check — verifying entropy status at the moment of visual production — not the first point of tribal validation.

### 4.5 Four Coaching Segment Noun Libraries

The TIAR maintains separate noun libraries for each of the four primary coaching segments:

**Conscious Business Coaches:** resonance, integrity, congruence, wholeness, threshold, emergence, embodied, alignment, sovereignty, discernment

**High-Performance Executive Coaches:** leverage, constraint, bottleneck, throughput, compounding, capacity, flywheel, friction, iteration, scalable

**Healing and Transformation Coaches:** window_of_tolerance, dysregulation, nervous_system, rupture, breakthrough, somatic, activation, completion, witnessing, attunement

**Financial Freedom Coaches:** spreadsheet, dividend, constraint, timeline, compounding, net_worth, cash_flow, asset, leverage, iteration

### 4.6 TIAR Monitor Agent

**Agent Name:** TIAR Monitor Agent (new)  
**Department:** Perception Department  
**Runs:** Monthly corpus analysis cycle (automated), plus triggered checks when entropy threshold crossings are detected

The TIAR Monitor Agent executes the seven-stage maintenance pipeline:

1. **Ingestion** — Crawls 50,000 coaching content posts per month per segment via Firecrawl wrapper
2. **Segmentation** — EDTS (entropy-optimized dynamic text segmentation) identifies tribal noun usage contexts
3. **Potency Filtering** — Cross-references against current TIRS baseline scores
4. **Decay Monitoring** — Calculates Shannon entropy per noun, compares against baseline, updates `entropy_pct_above_baseline`
5. **Steered Sampling** — Jensen-Shannon divergence penalty applied to prevent redundant or bleached output
6. **Refresh Triggering** — Automatically flags nouns crossing decay thresholds, populates `replacement_candidates`
7. **Engine Interface** — Writes updated active noun lists to Supabase, notifies Abel and Script Generation Skills of changes

---

## Section 5 — The 12 Visual Recipe Protocol Library

### 5.1 Library Overview

**Dependency ID:** DEP-VIS-002  
**Format:** YAML  
**Contains:** All 12 visual recipe protocol specifications  
**Queried By:** Abel (template assignment), Conscious Canva App (template loading), RunningHub integration (workflow ID mapping)

Each recipe protocol in the library contains a complete production specification. The library is the bridge between the theoretical framework and buildable templates.

### 5.2 Recipe Protocol Specifications

#### RECIPE-001: Relief Peak Carousel (`relief_peak_carousel_recipe`)

```yaml
protocol_id: "relief_peak_carousel_recipe"
archetype_family: "multi_scene_narrative"
format: "carousel"
emotional_angle_matrix:
  primary: "validation_relief"
  secondary: "recognition_intimacy"
arc_type: "tension_release"
slide_count:
  minimum: 4
  default: 5
  maximum: 6
isc_injection_formula: "round(total_slides * 0.75)"
chromatic_bloom:
  slides_1_to_2: {saturation_pct: 30-40, temperature: "cool_dominant", direction: "stable"}
  slide_climax: {saturation_pct: 68-78, temperature: "warm_entry", direction: "jump"}
  slides_final: {saturation_pct: 60-68, temperature: "warm_stable", direction: "stabilize"}
pad_requirements_by_position:
  struggle_slides: {pleasure: "2-4", arousal: "4-6", dominance: "1-3"}
  transition_slide: {pleasure: "4-5", arousal: "4-5", dominance: "3-5"}
  resolution_slides: {pleasure: "6-7", arousal: "2-3", dominance: "6-7"}
typography_arc:
  tension: {category: "serif", weight: "700-900"}
  build: {category: "sans_serif_medium", weight: "500-600"}
  climax: {category: "sans_serif_bold", weight: "700"}
  resolution: {category: "sans_serif_light", weight: "300-400", tracking: "+3pct"}
visual_style_defaults:
  tii_cold: "cinematic_realism_desaturated"
  tii_warming: "semi_realistic_digital"
  tii_warm: "ghibli_warm_illustration"
aspect_ratio: "square_1x1"
first_person_pov_slides: [1, 2]
semiotic_injection: "slide_climax_only"
accumulation_prohibition: true
peak_end_rule:
  peak_slide: "isc_injection_slide"
  end_slide: "last_slide"
  end_slide_standalone_required: true
template_ids:
  ghibli: "TPL-RELIEF-PEAK-001"
  semi_realistic: "TPL-RELIEF-PEAK-002"
  cinematic: "TPL-RELIEF-PEAK-003"
runninghub_workflow_ids:
  ghibli: "RH-WF-CAROUSEL-GHIBLI-001"
  semi_realistic: "RH-WF-CAROUSEL-SEMI-001"
  cinematic: "RH-WF-CAROUSEL-CINE-001"
```

#### RECIPE-002: Dopamine Cliff (`dopamine_cliff_recipe`)

```yaml
protocol_id: "dopamine_cliff_recipe"
archetype_family: "multi_scene_narrative"
format: "carousel"
emotional_angle_matrix:
  primary: "desire_disruption"
  secondary: "reality_contrast"
arc_type: "accumulation_cliff"
slide_count:
  minimum: 5
  default: 6
  maximum: 7
isc_injection_formula: "round(total_slides * 0.75)"
accumulation_slides: "slides_1_through_3"
cliff_slide: 4
chromatic_bloom:
  accumulation: {saturation_pct: 55-90, temperature: "warm_progressive", direction: "increasing_per_slide"}
  cliff: {saturation_pct: 15-25, temperature: "cold_shock", direction: "maximum_drop"}
  bridge: {saturation_pct: 45-55, temperature: "neutral", direction: "recovering"}
  resolution: {saturation_pct: 62-70, temperature: "warm_stable", direction: "stabilize"}
accumulation_prohibition:
  enabled: true
  prohibited_elements:
    - "completed_metrics"
    - "testimonial_screenshots"
    - "after_photography"
    - "awards_certificates"
    - "environmental_completeness"
    - "static_authority_poses"
    - "sentences_with_periods"
  required_elements:
    - "motion_vector_toward_goal"
    - "approach_state_not_arrival"
pad_requirements_by_position:
  accumulation: {pleasure: "5-6", arousal: "6-7", dominance: "3-4"}
  cliff: {pleasure: "2-3", arousal: "6-7", dominance: "2-3"}
  resolution: {pleasure: "6-7", arousal: "2-3", dominance: "6-7"}
nine_grid_variant:
  enabled: true
  format: "9_grid_single_page"
  grid_rule: "wanting_without_completion_all_9_frames"
visual_style_defaults:
  tii_cold: "cinematic_color_graded"
  tii_warming: "semi_realistic_digital"
  tii_warm: "semi_realistic_digital"
template_ids:
  default: "TPL-DOPAMINE-CLIFF-001"
  nine_grid: "TPL-9GRID-001"
runninghub_workflow_ids:
  carousel: "RH-WF-CAROUSEL-CLIFF-001"
  nine_grid: "RH-WF-GRID9-001"
```

#### RECIPE-003: Case Study (`case_study_recipe`)

```yaml
protocol_id: "case_study_recipe"
archetype_family: "multi_scene_narrative"
format: "carousel"
subtypes: ["social_proof", "surprising", "recognition_story"]
emotional_angle_matrix:
  primary: "transformation_evidence"
  secondary: "tribal_recognition"
arc_type: "discovery_revelation"
slide_count:
  minimum: 3
  default: 4
  maximum: 5
isc_injection_formula: "round(total_slides * 0.75)"
scene_requirements:
  scene_1: "struggle_environment_somatic_grammar"
  scenes_2_to_3: "transformation_in_progress_not_complete"
  scene_final: "transformation_gestalt_standalone"
pad_requirements_by_position:
  initial: {pleasure: "2-4", arousal: "5-6", dominance: "2-3"}
  revelation: {pleasure: "6-7", arousal: "4-5", dominance: "5-6"}
visual_style_note: "Social proof subtype uses real photo for credibility contract. Surprising and recognition subtypes may use semi-realistic illustration."
template_ids:
  real_photo: "TPL-CASE-STUDY-PHOTO-001"
  illustration: "TPL-CASE-STUDY-ILLUS-001"
runninghub_workflow_ids:
  illustration: "RH-WF-CASE-STUDY-001"
```

#### RECIPE-004: Debunking Myths (`debunking_myths_scams_recipe`)

```yaml
protocol_id: "debunking_myths_scams_recipe"
archetype_family: "multi_scene_narrative"
format: "carousel"
slide_count:
  minimum: 3
  default: 3
  maximum: 4
arc_type: "contrast_resolution"
emotional_angle_matrix:
  indignation: {color_spec: "orange_dominant #CC5000", motivation: "approach_norm_violation"}
  fear_anxiety: {color_spec: "deep_red #990000", motivation: "avoidance_warning"}
  revelation: {color_spec: "discovery_amber #E8A020", motivation: "approach_curiosity"}
color_angle_rule: "NEVER use red for indignation angle — activates avoidance in competence context. Red ONLY for fear-anxiety angle."
isc_injection_formula: "round(total_slides * 0.75)"
scene_3_revelation_required: true
visual_style_defaults:
  tii_cold: "cinematic_realism"
  tii_warming: "semi_realistic_digital"
  tii_warm: "ghibli_illustration"
template_ids:
  default: "TPL-DEBUNKING-001"
runninghub_workflow_ids:
  default: "RH-WF-DEBUNKING-001"
```

#### RECIPE-005: Observational Humor (`observational_humor_recipe`)

```yaml
protocol_id: "observational_humor_recipe"
archetype_family: "single_frame"
format: "single_image"
arc_type: "benign_violation_recognition"
slide_count: 1
visual_style_rule: "Ghibli or cartoon stylization REQUIRED regardless of TII — stylization creates psychological safety for benign violation perception. Realism breaks the humor mechanism."
color_spec: "warm_neutral_dominant with single_pop_accent"
fluency_priority: "maximum — micro-smile must activate before text is read"
tribal_recognition: "behavioral_level_minimum — identity_level_preferred"
template_ids:
  ghibli: "TPL-OBS-HUMOR-GHIBLI-001"
  cartoon: "TPL-OBS-HUMOR-CARTOON-001"
runninghub_workflow_ids:
  ghibli: "RH-WF-SINGLE-GHIBLI-001"
```

#### RECIPE-006: Worst Case Scenario (`worst_case_scenario_recipe`)

```yaml
protocol_id: "worst_case_scenario_recipe"
archetype_family: "single_frame"
format: "single_image"
arc_type: "fear_recognition"
slide_count: 1
visual_style_rule: "Desaturated cinematic realism REQUIRED regardless of TII — credibility of the possible must be maintained for fear-reality mechanism. Stylization creates safety buffer that allows viewer to dismiss as fantasy — mechanism fails."
fluency_priority: "maximum — Winkielman-Cacioppo dual signal: fear from content + micro-smile from fluency simultaneously. Fluency specs MORE critical here than any other recipe."
color_spec: "desaturated #808080 dominant, single muted accent only"
environmental_grammar_priority: "somatic_grammar_over_aesthetics"
template_ids:
  default: "TPL-WCS-CINE-001"
runninghub_workflow_ids:
  default: "RH-WF-SINGLE-CINE-001"
```

#### RECIPE-007: Listicle Visual (`listicle_visual_recipe`)

```yaml
protocol_id: "listicle_visual_recipe"
archetype_family: "multi_scene_narrative"
format: "carousel"
subtypes: ["curiosity_intriguing", "funny_relatable", "nostalgia", "outrageous", "fear_anxiety", "hope_inspiration"]
slide_count:
  minimum: 3
  default: 5
  maximum: 6
arc_type: "discovery_revelation"
isc_injection_formula: "round(total_slides * 0.75)"
zeigarnik_requirement: "tribe_specific_incomplete_artifact_on_tension_slides"
climactic_item_rule: "Most powerful item ALWAYS at ISC position — not saved for last"
mood_setter_compositing: "slide_1_establishes_complete_emotional_world_before_list_begins"
visual_style_defaults:
  curiosity: "semi_realistic_digital"
  funny_relatable: "ghibli_illustration"
  nostalgia: "warm_illustration_vintage_grain"
  fear_anxiety: "cinematic_realism_desaturated"
  hope_inspiration: "ghibli_warm_illustration"
template_ids:
  base: "TPL-LISTICLE-001"
runninghub_workflow_ids:
  default: "RH-WF-LISTICLE-001"
```

#### RECIPE-008: Comparison Archetypes (`comparison_archetypes_recipe`)

```yaml
protocol_id: "comparison_archetypes_recipe"
archetype_family: "two_part_contrast"
format: "carousel_2slide"
arc_type: "contrast_resolution"
gaze_architecture_rule: "FACE PRIORITY TRAP PREVENTION — Side A character gaze toward upper center (comparison label). Side B character gaze toward lower center (CTA zone). Creates X-pattern not collision. NEVER both characters facing center simultaneously."
color_spec:
  side_a: "background_carries_primary_emotional_signal — not character expression"
  side_b: "temperature_shift_minimum_1500K_from_side_a"
  background_rule: "background_processes_25ms_before_character — background IS the emotional differentiation between sides"
template_ids:
  default: "TPL-COMPARISON-001"
runninghub_workflow_ids:
  default: "RH-WF-COMPARISON-001"
```

#### RECIPE-009: Poll Recipes

Three poll recipe variants handled by a unified poll specification:

```yaml
protocols: ["poll_visual_recipe", "archetypical_poll_recipe", "controversial_dilemma_poll_recipe"]
archetype_family: "two_part_contrast"
format: "single_image_or_carousel_2_3_slides"
arc_type: "contrast_resolution"
visual_style_rule: "Single image format for stereotypical and controversial dilemma. Carousel for archetypical poll."
face_priority_trap_rule: "Applied per comparison recipe — gaze vectors must not create mutual collision"
template_ids:
  stereotypical: "TPL-POLL-STEREO-001"
  archetypical: "TPL-POLL-ARCH-001"
  dilemma: "TPL-POLL-DILEMMA-001"
runninghub_workflow_ids:
  poll: "RH-WF-POLL-001"
```

#### RECIPE-010: Visual Timeline (`visual_timeline_recipe`)

```yaml
protocol_id: "visual_timeline_recipe"
archetype_family: "multi_scene_narrative"
format: "carousel"
slide_count:
  minimum: 7
  default: 8
  maximum: 9
arc_type: "discovery_revelation"
isc_injection_formula: "round(total_slides * 0.75)"
chronological_color_arc: "environment_color_temperature_tracks_timeline_progression — past slides cooler, present slides warmer, future slides warmest"
template_ids:
  default: "TPL-TIMELINE-001"
runninghub_workflow_ids:
  default: "RH-WF-TIMELINE-001"
```

#### RECIPE-011: Conceptual Contrast (`conceptual_contrast_recipe`)

```yaml
protocol_id: "conceptual_contrast_recipe"
archetype_family: "two_part_contrast"
format:
  philosophical_simultaneous: "single_image"
  transformational: "carousel_2slide"
arc_type: "contrast_resolution"
format_selection_rule: "Simultaneous activation more powerful than sequential argument for philosophical recognition — use single image. Transformation requiring sequential understanding — use 2-slide carousel."
background_primary_signal_rule: "Background color must carry primary emotional differentiation between the two states — not character expression alone"
template_ids:
  simultaneous: "TPL-CONTRAST-SINGLE-001"
  sequential: "TPL-CONTRAST-CAROUSEL-001"
runninghub_workflow_ids:
  default: "RH-WF-CONTRAST-001"
```

---

## Section 6 — The 30 Visual Design Architecture Specifications

Each specification below names: the exact mechanism, the production failure if ignored, the system component that enforces it, and the integration point in the CVE pipeline.

### Group A — Lighting and Chromatic Grammar

**SPEC-01 — Cinematographic Lighting Grammar**

*Mechanism:* Lighting direction, Kelvin temperature, and shadow opacity must be specified simultaneously as a unified grammar. The visual system routes light information to emotional processing centers before content recognition begins. A 3000K CCT at 750 lux produces the lowest measurable mental workload. 6500K increases alertness but risks visual fatigue. The light-from-above neurological bias is universal but modulated by reading direction — left-to-right readers default to upper-left key light; right-to-left readers show reversed lateral bias.

*Production failure if ignored:* Brief reads "warm cinematic feel" — RunningHub samples the center of its training distribution and produces the coaching photography average.

*System enforcement:* Abel populates all three lighting fields in the VCB for every slide (lighting_grammar field — natural language cinematographic description). Paradoxe validates completeness before compiling the RunningHub prompt. The PSSL Completeness Gate (C-09) rejects any VCB slide missing lighting grammar specification.

*Integration point:* VCB → Lighting Grammar field → Paradoxe prompt compilation → RunningHub prompt string

---

**SPEC-02 — Color Assignment by Archetype Angle**

*Mechanism:* Elliot and Maier's color-in-context research proves the same hue produces opposite motivational responses depending on semantic framing. Red in achievement contexts fires avoidance motivation. Orange fires approach motivation AND moral norm violation signal — the correct specification for indignation-angle content. Red is reserved exclusively for fear-anxiety angles where avoidance IS the intended response.

*Production failure if ignored:* Debunking Myths carousel uses red for urgency. Viewer's nervous system reads "I am failing" rather than "wrong is being named." Engagement is damaged before any content is processed.

*System enforcement:* DEP-VIS-002 (Recipe Protocol Library) specifies color-angle rules explicitly per recipe. Abel reads both the recipe protocol AND the emotional angle from the script JSON package before setting the chromatic spec. Color selection is never a standalone decision.

*Integration point:* Script JSON emotional_angle field → Abel color-angle lookup in DEP-VIS-002 → VCB chromatic_spec → RunningHub prompt

---

**SPEC-03 — Chromatic Bloom Sequence**

*Mechanism:* Background color processes 25ms before shape, face, or text. In a carousel, this creates a pre-cognitive emotional arc parallel to the content arc. Transitioning from achromatic to chromatic stimuli elicits significantly greater prefrontal and orbitofrontal cortex activation than the reverse. The body reads the color arc before the eyes reach the words.

*Production failure if ignored:* Random color assignments per slide. The viewer's body receives contradictory pre-cognitive loading. The peak lands flat because the body was not pre-loaded into the right state.

*System enforcement:* Every recipe protocol in DEP-VIS-002 includes a `chromatic_bloom` specification — saturation percentage and temperature direction per slide position. Abel writes saturation_pct and saturation_direction for every slide in the VCB. The Accumulation Prohibition Audit in the VCB validates that saturation increases progressively across accumulation slides.

*Integration point:* DEP-VIS-002 chromatic_bloom spec → VCB chromatic_spec per slide → Paradoxe → RunningHub prompt color specification

---

**SPEC-04 — Accumulation: Wanting Without Completion**

*Mechanism:* The mesolimbic wanting pathway and the opioid liking pathway operate independently. Wanting activates on approach toward reward. Once arrival is shown, liking's satiety mechanism fires and desire habituates. High-aspiration stimuli maintain sustained LPP (Late Positive Potential) ERP amplitudes specifically when showing approach, not completion. A single completion image in an accumulation sequence collapses the entire LPP build that preceded it.

*Production failure if ignored:* Slide 2 of the Dopamine Cliff shows a client testimonial — a completed success story. Desire habituates immediately. The cliff lands against a body that is no longer in approach state.

*System enforcement:* The Accumulation Prohibition Checklist runs as a required field in the VCB (`accumulation_prohibition_audit`). Abel verifies all accumulation slides pass before composition is approved. Prohibited elements list is hardcoded in DEP-VIS-002 and cannot be overridden.

*Integration point:* Abel checklist execution → VCB accumulation_prohibition_audit field → PSSL Completeness Gate blocks VCBs with failed audit

---

**SPEC-05 — Chromatic Bloom: Saturation Numbering**

*Mechanism:* Saturation is a numbered specification in the VCB, not a mood description. Each slide position receives a specific saturation percentage based on its arc stage. High saturation (85-90%) is reserved for the accumulation peak and the semiotic injection slide. Desaturation (15-25%) signals the cliff or the lowest emotional point in the sequence. Resolution returns to a warm stable 62-68%.

*Production failure if ignored:* Designer estimates "vibrant" for peak slides — actual saturation is 65% because the estimation was made against the previous slide, not against the arc specification. The peak fails to land with maximum physiological impact.

*System enforcement:* Saturation percentage is a required numeric field in the VCB chromatic_spec. Paradoxe translates saturation percentage into RunningHub prompt syntax. Post-generation, the Visual Validation Agent verifies saturation alignment using image analysis.

*Integration point:* VCB chromatic_spec.saturation_pct → Paradoxe → RunningHub prompt parameter

---

### Group B — Somatic Architecture

**SPEC-06 — Arc Type as Foundational Brief Decision**

*Mechanism:* Four carousel arcs produce distinct biometric trajectories: Tension-Release (A-process then B-process HRV increase), Discovery-Revelation (sustained Beta + progressive GSR peaks), Contrast-Resolution (corrugator activation then zygomaticus activation), Accumulation-Cliff (escalating LPP then acute GSR spike). Everything — lighting, color, typography, PAD scores, chromatic bloom — derives from the declared arc type.

*Production failure if ignored:* Visual parameters are selected by recipe convention without arc type confirmation. The somatic arc collapses into incoherence because the body receives contradictory pre-loading across slides.

*System enforcement:* Arc type is the first field Abel reads from the script JSON package. Arc type must match the recipe protocol's documented arc. Mismatch triggers an operator flag before composition proceeds. Arc type is required field in the VCB.

*Integration point:* Script JSON arc_type → Abel confirmation check against DEP-VIS-002 → VCB arc_type → All downstream parameter generation

---

**SPEC-07 — Environmental Grammar for Somatic Recognition**

*Mechanism:* Damasio's somatic marker hypothesis confirms environments trigger body-memory through environmental grammar — the syntax of light quality, spatial density, and temporal signals — not through surface similarity. An 11pm kitchen triggers somatic recognition not because it looks like the viewer's kitchen but because overhead institutional light + high object density + temporal stillness matches the autobiographical body-memory of late-night problem-solving. Somatic recognition fires SCR signatures measurably different from intellectual recognition.

*Production failure if ignored:* Stage set is specified as "coaching struggle scene" — AI generates a stock-photography tired person against a white background. Intellectual recognition fires ("yes that is a tired person") but somatic recognition does not. The Relief Peak never reaches full physiological depth.

*System enforcement:* Abel queries DEP-VIS-003 (Stage Set Emotional Architecture Library) using PAD score requirements, not aesthetic categories. Every stage set specification in the VCB must include all five grammar parameters: light quality (time-of-day signal), spatial density (object count), temporal signal, world color temperature independent of key light, and subject-to-frame height ratio.

*Integration point:* PAD score requirements → DEP-VIS-003 library query → VCB environmental_grammar fields → Paradoxe → RunningHub prompt

---

**SPEC-08 — PAD Framework: All Three Dimensions Required**

*Mechanism:* The PAD (Pleasure-Arousal-Dominance) framework's Dominance dimension is the most underspecified element in coaching visual content and the most architecturally powerful. High-dominance environments communicate the subject controls the world. Low-dominance environments communicate the subject is contained by the world. Menzies' pictorial architecture principle — subordinating the human figure to the larger graphic structure — is the validated mechanism for environments that feel psychologically inevitable. AI-generated environments fail specifically on Dominance.

*Production failure if ignored:* Struggle slides accidentally place the coach in high-dominance environments (power office, commanding spatial field) because "it looks professional." The body reads authority and control where it should read overwhelm and restriction. The narrative arc breaks.

*System enforcement:* DEP-VIS-003 contains PAD scores for every stage set in the library. Abel specifies PAD target ranges per slide position in the VCB. Stage set selection from DEP-VIS-003 filters exclusively by PAD range match — not by aesthetic similarity.

*Integration point:* Recipe protocol PAD requirements → Abel PAD range specification → DEP-VIS-003 library filter → VCB environmental_grammar.pad_scores

---

**SPEC-09 — Tribe-Specific Incompleteness**

*Mechanism:* The Zeigarnik Effect only creates persistent cognitive tension when the incomplete task is personally relevant. Generic visual incompleteness produces mild visual interest. Tribal incompleteness — an artifact the viewer has a specific embodied relationship with, left unfinished — activates working memory persistence. The open loop is felt, not observed.

*Production failure if ignored:* Tension slides show generic incompleteness signals — an unfinished diagram, a blurred future, a half-drawn arrow. Visual metaphors, not tribal artifacts. No persistent pull.

*System enforcement:* Abel populates the `incomplete_tribal_artifact` field in the VCB for every tension slide. This field is populated using the tribal context from the script JSON package (coaching segment + enemy typology + recognition context) combined with DEP-ENG-007 (Tribe Intelligence). The field cannot be null for tension slides — null triggers a validation failure.

*Integration point:* Script JSON tribal_context → Abel tribal artifact query → VCB incomplete_tribal_artifact field → Paradoxe → RunningHub environmental scene composition

---

**SPEC-10 — ISC 75% Rule for Semiotic Climax Position**

*Mechanism:* Inter-Subject Correlation research confirms neural synchronization peaks at the 75% mark of a narrative sequence. This is the moment of maximum collective physiological alignment. The semiotic injection — facial expression climax, maximum chromatic intensity, identity declaration — belongs at exactly this position for maximum physiological impact.

*Production failure if ignored:* The emotional climax is placed at the midpoint because "that feels like the middle of the story." The peak fires at 60% collective arousal instead of 100%.

*System enforcement:* Abel calculates `semiotic_injection_slide = round(total_slides × 0.75)` as a required formula-driven field in the VCB. This is not a parameter Abel decides — it is a calculation. The `semiotic_injection: true` flag on the calculated slide position is what triggers the facial expression injection specification in Paradoxe.

*Integration point:* VCB total_slides → Abel formula → VCB semiotic_injection_slide → Paradoxe expression injection trigger → RunningHub character expression parameter

---

**SPEC-11 — Peak-End Rule: Two Priority Slides**

*Mechanism:* The remembered experience of a carousel is determined by the most intense moment (the peak) and the final moment (the end). Duration neglect means intermediate slides are almost irrelevant to remembered quality. A 9-slide carousel with a powerful peak and weak final slide is remembered worse than a 5-slide carousel with a strong peak and strong final slide.

*Production failure if ignored:* The carousel is optimized for information flow. The final slide is a CTA template. The remembered experience is "follow me for more." No save behavior. No DM.

*System enforcement:* DEP-VIS-002 marks the peak slide (ISC position) and the final slide as `peak_end_rule_priority: HIGH`. Abel adds `peak_end_rule_priority` flag to both slides in the VCB. Paradoxe receives elevated specification requirements for these two slides. The final slide receives the `standalone_validity: true` and `screenshot_shareable: true` flags — both must be achievable from the VCB specification before production proceeds.

*Integration point:* VCB slide flags → Paradoxe priority weighting → RunningHub → Visual Validation Agent screenshot_shareable check

---

**SPEC-12 — Corrugator as Semantic Conflict Signal**

*Mechanism:* The corrugator supercilii activates specifically in response to goal-relevant vs. goal-irrelevant information conflict — situations where what the viewer wants and what they are seeing are in tension. This is not generic negativity. It fires when the viewer's aspirational self-identity is confronted by the reality being depicted. Visual content that creates semantic conflict between tribal identity aspiration and depicted reality produces sharper, more personally resonant corrugator activation than visual content that merely depicts difficulty.

*Production failure if ignored:* Struggle slides are dark and difficult visually, producing mild corrugator activation through negative valence. A semantically conflicting image — showing the exact gap between who the viewer wants to be and what they are currently doing — produces the specific corrugator response that creates persistent tension and drives swipe continuation.

*System enforcement:* Abel populates a `semantic_conflict_specification` field in the VCB for every tension slide: naming the viewer's aspirational state AND the reality depicted. This field is used by Paradoxe to compose the scene brief for RunningHub — the conflict is specified, not left to chance.

*Integration point:* Script JSON tribal_context.audience_recognition_context → Abel semantic conflict specification → VCB semantic_conflict_specification → Paradoxe scene composition

---

### Group C — Typography and Processing Systems

**SPEC-13 — Typography-Arc Synchronization**

*Mechanism:* Font weight communicates arousal level independently of semantic content. Bold weights are neurologically processed as louder and more energetically demanding — they prime corrugator activation. Light weights activate processing fluency and prime the zygomaticus micro-smile. The Fourier amplitude spectrum research specifies fonts approximating the 1/f spatial frequency distribution minimize visual fatigue and maximize the fluency response at resolution slides.

*Production failure if ignored:* Bold serif used throughout the entire carousel for "brand consistency." Resolution slide delivers the physiological exhale content in the same high-arousal typographic register as the tension slides. The body never receives the fluency signal. The exhale doesn't happen.

*System enforcement:* Typography specification in the VCB is derived from the arc stage for each slide — not from brand guidelines. The arc stage → typography mapping is hardcoded in DEP-VIS-002. The VCB typography field contains arc_stage, font_category, font_weight, and for resolution slides, tracking_adjustment. Brand-consistent typography applies to elements outside the primary text zone only.

*Integration point:* VCB arc_stage per slide → DEP-VIS-002 typography mapping → VCB typography field → Paradoxe → Conscious Canva App text layer specification

---

**SPEC-14 — Processing Fluency: Resolution Slide Font Requirements**

*Mechanism:* Processing fluency triggers zygomaticus major activation (micro-smile) below conscious awareness. This physiological response is misattributed to the content — the viewer feels the brand is more trustworthy and likeable without knowing why. Resolution slides must maximize fluency signal to complete the physiological exhale. This requires sans-serif, weight 300-400, generous letter spacing, high contrast text-to-background (minimum 7:1), maximum 6 words primary text.

*Production failure if ignored:* Resolution slide uses decorative serif font for visual consistency. Processing disfluency fires a mild corrugator response. The physiological exhale never completes. The post feels relentless.

*System enforcement:* Resolution arc stage slides receive mandatory font requirements in the VCB typography field. The PSSL Completeness Gate checks resolution slides specifically for font_weight < 500 and font_category "sans_serif." Any resolution slide specifying weight > 500 fails the completeness check and requires revision.

*Integration point:* VCB arc_stage "resolution" flag → PSSL Completeness Gate weight check → Conscious Canva App text layer → final composition

---

**SPEC-15 — Six-Word Law with Concrete Noun Requirement**

*Mechanism:* Paivio's Dual Coding Theory requires concrete nouns to activate both verbal and imagery systems simultaneously. Abstract words only fire the verbal system. The 6-word law is not just a word count constraint — it requires minimum 3 of 6 words to be concrete nouns or action verbs activating dual-coding. Ghost nouns ("freedom," "purpose," "impact") count as words but do not count toward the concrete noun requirement.

*Production failure if ignored:* Hook text reads "Our happiness is primarily based on our gratitude" (a real example from the previous carousels reviewed). Nine abstract words. Zero dual-coding activation. Behavioral recognition at best.

*System enforcement:* TIAR query returns only concrete nouns with active entropy status. Script generation skills receive these as required vocabulary. The VCB typography primary_text field has a `primary_word_count` maximum of 6 and a `concrete_noun_count` minimum of 3. The PSSL Completeness Gate validates this ratio. Any primary text failing the ratio is flagged for revision before RunningHub execution.

*Integration point:* TIAR active noun list → Script Generation Skill injection → Script JSON hook_concrete_nouns → Abel VCB validation → PSSL Gate

---

### Group D — Linguistic-Visual Congruence System

**SPEC-16 — Tribal Noun + Visual Congruent Pairing**

*Mechanism:* Identity-level recognition — the "I know you" response that drives saves and DMs — requires simultaneous activation of both the verbal system (tribal noun) and the imagery system (congruent visual element). When both fire simultaneously, the response is identity-level recognition ("that is exactly who I am"). Neither the word alone nor the image alone produces the identity-level Gamma ignition. The pairing does.

*Production failure if ignored:* Text says "the 3am spiral." Visual shows a generic stressed person at a laptop with morning light. Noun fires correctly. Visual fires generic "stressed person" recognition. No dual-coding simultaneity. Post performs adequately. Never creates the "how did they know?" response.

*System enforcement:* Abel populates `tribal_noun_visual_congruent` pairs for every slide containing text. The congruent description is a scene grammar specification — the exact environmental and compositional elements that match the noun's tribal meaning. The pair is validated for specificity: any congruent description containing the words "generic," "typical," "standard," or "person looking" fails validation and requires revision.

*Integration point:* TIAR visual_congruent_mappings → Abel pairing generation → VCB tribal_noun_visual_congruent → Paradoxe → RunningHub environmental composition

---

**SPEC-17 — TIRS Integration in Script Generation Skills (Upstream)**

*Mechanism:* The TIAR's primary integration point is upstream in the Script Generation Skills — not downstream in the visual pipeline. Concrete nouns must be selected with tribal charge at the script generation stage. The visual pipeline's TIAR query is a confirmation check, not the first point of tribal validation. This architectural decision is what makes congruence coherent — the script and the visual are built from the same tribal vocabulary.

*Production failure if ignored:* Script generation proceeds without TIAR query. Script uses "freedom," "abundance," "purpose," "authentic" — all high-entropy expired nouns. The visual recipe builds perfect congruents for expired vocabulary. The content performs adequately and moves no one.

*System enforcement:* Script Generation Skill YAML files include mandatory `tiar_query` pre-generation step. Active noun list and expired noun list are both injected into the hook generation instruction as required/excluded vocabulary respectively. The Receipt Chain Guard logs the TIAR query result as part of the script compilation audit trail.

*Integration point:* Script Generation Skill YAML → TIAR query → active/expired noun list injection → script hook → script JSON hook_concrete_nouns → Abel confirmation

---

### Group E — Character and Cast Systems

**SPEC-18 — Gaze Geometry: Dual-Vector Specification**

*Mechanism:* Langton's 2000 research established the joint attention mechanism requires TWO congruent signals simultaneously: iris eccentricity (pupil position within visible iris) AND face eccentricity (feature position within head contour). In stylized illustration, large simplified eyes make iris eccentricity ambiguous. A head turned 20° left with centered pupils reads as looking forward. The mechanism fails silently — gaze does not transfer to the text zone.

*Production failure if ignored:* Character is described as "looking toward the hook text" with head turned left. Ghibli-style character has pupils drawn centered in large eyes. Joint attention mechanism fails. Viewer's eye does not transfer to the text. The hook is invisible.

*System enforcement:* Abel populates two required character_spec fields in the VCB: `head_rotation_degrees` (numeric) and `pupil_position_ratio_pct` (numeric, percentage of visible iris width from center). "Looking toward the text" is not a valid specification — it is rejected by the PSSL Completeness Gate. For Ghibli style, Paradoxe's prompt template includes a mandatory override instruction: "pupils clearly offset toward the specified edge of the visible iris area, not centered."

*Integration point:* VCB character_spec.head_rotation_degrees + pupil_position_ratio_pct → Paradoxe → RunningHub character generation prompt

---

**SPEC-19 — Character Consistency via Image Reference Architecture**

*Mechanism:* AI image editing models (img2img, identity-preserving generation) can reproduce a specific face from a reference image with high fidelity — maintaining identity-critical features across different environments and expressions. AI-generated faces are actually more consistently reproduced than real photographs because they lack authentic micro-variation. Identity-critical features (iris color and shape, eyebrow geometry, facial proportions, skin texture approach) must never vary. Identity-neutral features (background, lighting, pose, camera angle) vary freely per recipe and arc stage.

*Production failure if ignored:* Every generation session produces subtle character drift. The iris is slightly different, the eyebrow arch changes. Across 36 pieces per week, the cast never quite looks the same. Parasocial attachment formation never builds because the character lacks consistency.

*System enforcement:* DEP-VIS-004 (Brand Character Reference Archive) stores the canonical reference image for each cast character. Abel includes the reference image URL in the VCB character_spec. RunningHub receives the reference image alongside the prompt. The PSSL Completeness Gate rejects any VCB slide with a named character that does not include a DEP-VIS-004 reference URL.

*Integration point:* DEP-VIS-004 reference archive → Abel VCB character_spec.reference_url → RunningHub API reference_image parameter

---

**SPEC-20 — Avatar Authenticity: Eight-Feature Hierarchy**

*Mechanism:* A 508-participant study identified eight micro-level visual cues predicting AI portrait perceived authenticity, ranked by predictive strength. Facial features dominate: Expression Naturalness (eye-mouth congruence), Facial Proportion (geometric reasonableness), Skin Texture (pore-level detail) are the three strongest predictors. "Perfect" AI visuals are perceived as LESS trustworthy than "imperfect but plausible" ones. Intentional asymmetry and visible imperfection signal "real world," not "constructed."

*Production failure if ignored:* System generates polished, technically perfect avatar images with smooth skin and symmetrical features. Audience experiences reduced trust response without consciously identifying the cause. Parasocial relationship formation is slower.

*System enforcement:* Abel populates three mandatory avatar generation parameters in the VCB character_spec: `expression_congruence_check` (eye-mouth congruent — not just mouth expression), `skin_texture` (requires visible pore detail — "smooth" is not valid), `intentional_asymmetry` (one specific asymmetry named). Post-generation, the Visual Validation Agent runs a 6-point authenticity checklist. Failures at items 1-3 (Expression Naturalness, Facial Proportion, Skin Texture) trigger regeneration. Failures at items 4-6 trigger post-processing or regeneration.

*Integration point:* VCB character_spec authenticity params → Paradoxe → RunningHub → Visual Validation Agent post-generation check → regeneration loop or approval

---

**SPEC-21 — Documentary Authenticity Effect**

*Mechanism:* AI authenticity research confirms "perfect" AI visuals paradoxically signal "constructed" through their very perfection. Minor authentic imperfections — slight environmental disorder, natural asymmetry, uncontrolled background elements — activate somatic markers signaling "this is from a real world" before any conscious evaluation occurs. Intentional imperfection is not a quality failure — it is a trust architecture specification.

*Production failure if ignored:* All compositions are generated at maximum technical quality with flawlessly resolved environments. The somatic marker "constructed" fires below conscious threshold. Trust formation slows.

*System enforcement:* The VCB contains a required `intentional_imperfection` field per slide. For cinematic realism: one named environmental irregularity (a slightly askew object, a stray shadow, a texture inconsistency). For Ghibli illustration: intentional line weight variation, one element slightly less resolved than others. For mixed media: visible seam between real and illustrated elements. "None" is not a valid value — the field is mandatory. Paradoxe incorporates the imperfection specification into the RunningHub prompt.

*Integration point:* VCB intentional_imperfection field → Paradoxe → RunningHub prompt → Visual Validation Agent imperfection confirmation

---

**SPEC-22 — Visual Style Selection by Relationship Stage (TII)**

*Mechanism:* The TII (Total Interaction Index) measures audience relationship depth. At low TII (cold audience), Fogg's web credibility research confirms "real-world feel" is the dominant trust variable — photorealism fulfills the authentication contract. At high TII (warm audience), Green and Brock's Transportation-Imagery research predicts illustrated stylization facilitates deeper transportation and identity projection — the viewer uses the illustration's emotional safety to project their desired self. Archetype override rules apply regardless of TII.

*Production failure if ignored:* Coach uses photorealistic imagery universally for "professionalism." Cold audience posts correctly fulfill the authentication contract. Warm audience recognition posts are delivered in photorealistic register — viewer remains observer, never participant. Transportation never deepens into identity-level response.

*System enforcement:* Abel reads `tii_score` from the psychological routing brief. The style selection decision tree is hardcoded in DEP-VIS-002:
- TII < 25 → cinematic_realism
- TII 26-70 → semi_realistic_digital
- TII > 70 → ghibli_warm_illustration
- Worst Case Scenario override → desaturated_cinematic_realism (always)
- Observational Humor override → ghibli_illustration (always)
- Fear-anxiety angle override → desaturated_cinematic_realism (always)

*Integration point:* Psychological Routing Brief TII score → Abel style selection → VCB visual_style field → Template selection in DEP-VIS-002 → RunningHub workflow ID

---

### Group F — Production Quality Gates

**SPEC-23 — First-Person POV Architecture**

*Mechanism:* VR research confirms first-person perspective elicits stronger somatic presence and higher SCR elevation than third-person in high-fidelity imagery. The 1PP is the mechanism behind the date posts' environmental immersion — legs in hammock, feet toward campfire, hands in frame. It eliminates the observer and places the viewer inside the experience. It should be used on struggle slides specifically because its higher somatic impact amplifies the pain-state recognition that powers the Relief Peak arc.

*Production failure if ignored:* Struggle slides use third-person perspective (viewer watching a stressed person). Intellectual recognition fires. Somatic recognition does not. The Relief Peak builds on an intellectual foundation, not a somatic one. The exhale is shallow.

*System enforcement:* DEP-VIS-002 specifies `first_person_pov_slides` for each recipe protocol. Abel includes a `first_person_pov: true/false` flag per slide in the VCB. When true, Paradoxe's prompt template switches to first-person composition directives: hands in frame at bottom, subject environmental elements at eye level, no full-body character visible.

*Integration point:* DEP-VIS-002 first_person_pov_slides → VCB per-slide flag → Paradoxe composition directive → RunningHub camera perspective specification

---

**SPEC-24 — Aspect Ratio as Social Contract**

*Mechanism:* Kress and van Leeuwen's Visual Grammar establishes image format creates an Interpersonal Metafunction — a social relationship contract. Portrait creates intimacy and scale dominance (image enters personal space). Square creates equality (peer relationship). Landscape creates detachment and panoramic authority (viewer observes a world). These are documented social contracts with measurable physiological correlates.

*Production failure if ignored:* Coach posts landscape format intimate emotional disclosure. Format signals "world to observe" while content signals "personal confession." Social contracts contradict. Viewer processes with cognitive distance.

*System enforcement:* Abel specifies `aspect_ratio` in the VCB based on archetype function — not platform default. The mapping is defined in DEP-VIS-002:
- Intimate delivery (healing, recognition, emotional truth) → square_1x1 or portrait_4x5
- Status and authority content → landscape_16x9 or landscape_4x3
- Comparison and contrast archetypes → square_1x1
- Seamless horizontal carousel → wide_landscape

*Integration point:* Script JSON archetype + mood_state → Abel aspect_ratio selection → VCB aspect_ratio → Conscious Canva App canvas configuration → RunningHub output dimensions

---

**SPEC-25 — Cultural Color Architecture**

*Mechanism:* Elliot and Maier's color-in-context research was conducted on Western cohorts. The pseudoneglect leftward lighting bias is reversed for right-to-left readers. White signals mourning in East Asian cultural contexts. Red signals fortune in Chinese contexts. Yellow signals wealth and fertility in West African contexts. Green signals sacred authority in Islamic contexts. These are not surface cultural variations — they are documented differences in emotional meaning through lifetime exposure.

*Production failure if ignored:* The color architecture matrix built on Western research norms is applied to a coach whose audience is predominantly West African diaspora. "White for clarity and purity" triggers mourning associations. The carefully built physiological architecture is undermined at the color layer.

*System enforcement:* DEP-ENG-002 (Audience Avatar) contains `primary_cultural_context` field. Abel reads this field before setting chromatic_spec in the VCB. DEP-VIS-003 (Stage Set Library) contains four cultural color profiles per mood state. The profile selection uses `primary_cultural_context` as the lookup key. Western profile is not the default — it is one of four equally valid options.

*Integration point:* DEP-ENG-002 cultural context → Abel profile selection → DEP-VIS-003 cultural color profiles → VCB chromatic_spec

---

**SPEC-26 — Motoric Vampire Effect: Seamless Swipe Imperative**

*Mechanism:* Every counter-intuitive or friction-introducing gesture diverts cognitive resources from content processing to motor control management — measurably reducing brand recall and message comprehension. The carousel sideways swipe works specifically because it is consistent, predictable, and low-effort. The seamless horizontal format reinforces this: the viewer is moving through a continuous world, not flipping pages.

*Production failure if ignored:* Mixed formats within a single carousel (a video slide in position 3, or a poll slide interrupting the sequence) introduce navigation ambiguity. Each disruption triggers a motor allocation event that reduces the depth of the emotional arc processing.

*System enforcement:* DEP-VIS-002 Recipe Protocol Library defines format as immutable per recipe — no mixed formats within a single carousel sequence. The Conscious Canva App's template system enforces this at the layout level — slides in a carousel template are all the same format type. The slide transition design must preserve the seamless pan grammar — environmental elements bleeding across slide boundaries are specified in the template design brief.

*Integration point:* DEP-VIS-002 format immutability → Canva App template enforcement → seamless edge bleed specification in template design brief

---

**SPEC-27 — Micro-Commitment Investment Architecture**

*Mechanism:* Each carousel swipe is a micro-commitment under Cialdini's consistency principle. By slide 3, the viewer has made two micro-commitments — creating internal motivation to complete the sequence. This accumulated investment amplifies two effects: the physiological exhale on the Relief Peak slide is deeper (B-process amplified by commitment investment), and the GSR spike at the Dopamine Cliff is more intense (the surprise violates established consistency). The body experiences the disruption more acutely when it has physically committed to the journey.

*Production failure if ignored:* Carousel is designed at 3 slides for "performance optimization." Insufficient micro-commitment investment for physiological mechanisms to operate at full depth. The 3-slide carousel delivers information. The 6-slide carousel with correct arc delivers a physiological experience.

*System enforcement:* DEP-VIS-002 specifies minimum slide counts per arc type based on micro-commitment thresholds:
- Accumulation-Cliff: minimum 5 slides (3 accumulation slides required before cliff)
- Tension-Release: minimum 4 slides
- Discovery-Revelation: minimum 4 slides
- Contrast-Resolution: minimum 2 slides (format minimum)

Abel enforces these minimums when generating VCB slide count. Requests for shorter formats below minimum are flagged for operator review.

*Integration point:* DEP-VIS-002 minimum slide counts → Abel slide count determination → VCB total_slides → micro-commitment validation check

---

**SPEC-28 — Parasocial Architecture: PSI vs PSR**

*Mechanism:* Dibble et al.'s research distinguishes Parasocial Interaction (PSI — momentary, within-viewing, triggered by direct gaze) from Parasocial Relationship (PSR — enduring cross-episode bond requiring character allure and narrative complexity). PSI requires direct gaze and address. PSR requires a character whose decisions carry consequences across episodes and whose internal conflicts the viewer recognizes. Content built for PSI only produces consistent but shallow engagement. The transition from audience to buyer requires PSR investment.

*Production failure if ignored:* Every post built for immediate PSI — direct address, commanding presence. No episode references previous episodes. No character arc develops. Audience likes content but does not form attachment. Conversion is slow.

*System enforcement:* DEP-VIS-004 (Brand Character Reference Archive) stores not just reference images but narrative role specifications per character: documented internal conflict, evolutionary arc position, relationship to protagonist. Abel checks the character's current arc position when specifying expression in the VCB — expressions must be arc-consistent with the character's current narrative state, not just emotionally appropriate for the slide.

*Integration point:* DEP-VIS-004 character narrative state → Abel expression specification → VCB character_spec.expression + expression description

---

**SPEC-29 — AGSS: Anti-Generic Specificity Scale**

*Mechanism:* AI diffusion models converge on their training data average through sharp transition behavior — the model settles into the most statistically common representation of any prompt. "Authentic coaching environment" returns the Amazon Standard of photography: technically competent, psychologically inert. The AGSS measures the mathematical distance between a generated image's features and the generic center of the training distribution. High AGSS score = the image is far from the statistical average = the PSSL has successfully forced specificity.

*Production failure if ignored:* VCB is well-specified but Paradoxe translates it into a prompt that collapses specificity through generic vocabulary. The RunningHub output is technically correct and emotionally average. The CVE produces content identical to every other coaching account.

*System enforcement:* The Visual Validation Agent (new — Section 10) scores every generated image using the AGSS immediately after RunningHub delivery. Minimum AGSS threshold: 6.5/10. Images scoring below threshold are automatically returned to Paradoxe for prompt revision and regeneration. The AGSS score is logged in the VCB output field and included in the Notion delivery card as part of the production audit trail.

*Integration point:* RunningHub output URL → Visual Validation Agent AGSS scoring → threshold check → regeneration loop or approval gate → Notion delivery

---

**SPEC-30 — PSSL Brief Schema as Production Law**

*Mechanism:* AI diffusion models convert descriptive language into statistical averages. The PSSL prevents this by specifying parameters at low latent space density — forcing the model away from the center of its training distribution. Every visual parameter in a PSSL brief traces back to a documented physiological outcome. No visual element exists without a somatic justification. This is not a design philosophy — it is the specification language that makes deterministic visual production possible.

*Production failure if ignored:* Briefs contain adjectives without measurable values. "Warm and powerful" returns the coaching photography statistical centroid. The system cannot be audited, cannot be improved, and cannot scale deterministically.

*System enforcement:* The VCB schema (DEP-VIS-005) is the PSSL brief for every slide. All fields are required and typed. The PSSL Completeness Gate (C-09 in the validation pipeline) rejects any VCB with:
- Lighting grammar field containing only adjectives (no temporal signal, no shadow specification)
- Typography weight specified as a word (must be numeric)
- Primary text containing zero concrete nouns from the TIAR active list
- PAD scores absent from environmental_grammar
- Character spec missing head_rotation_degrees or pupil_position_ratio_pct for slides with characters

The Receipt Chain Guard logs the completeness gate pass/fail as an immutable audit record.

*Integration point:* VCB DEP-VIS-005 schema → PSSL Completeness Gate (C-09) → Receipt Chain Guard log → Paradoxe (only receives complete VCBs)

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

Paradoxe's single job is to translate a fully validated VCB into RunningHub-ready prompt strings that are maximally specific, low in latent space density, and congruent with the PSSL parameters. Paradoxe never improvises — it compiles. Every prompt it generates must be traceable back to specific VCB fields.

### 7.2 PSSL Field-to-Prompt Translation Rules

Paradoxe uses a translation rule set to convert each VCB field into prompt language:

**Lighting Grammar → Prompt Lighting Block**
The natural language lighting grammar description in the VCB is used directly. Paradoxe wraps it with technical cinematographic terminology that RunningHub's models respond to:
```
VCB: "Overhead institutional fluorescent — 11pm temporal signal"
→ Prompt: "single overhead fluorescent source, no fill lighting, clinical institutional quality, late-night isolation grammar, hard shadows beneath eyes and chin, 4200K color temperature"
```

**Chromatic Spec → Prompt Color Block**
Saturation percentage translates to a Vibrancy/Saturation parameter. Temperature direction translates to specific color temperature descriptor:
```
VCB: {foundation_hue: "#2C3E50", saturation_pct: 35, temperature_direction: "cool"}
→ Prompt: "dominant dark slate blue-grey color palette, 35% color saturation, cool color temperature, muted and desaturated rendering, color grading consistent with institutional isolation"
```

**Character Spec → Prompt Character Block**
The dual-vector gaze specification and expression details translate to specific character directives:
```
VCB: {head_rotation_degrees: 15, head_rotation_direction: "right", pupil_position_ratio_pct: 20}
→ Prompt: "character head turned 15 degrees to the right from camera, pupils clearly positioned in the rightmost 20% of the visible iris area, gaze directed toward upper right zone of frame, not looking at camera"
```

**Expression → Prompt Expression Block**
The expression description from the VCB (which has already been validated for eye-mouth congruence and intentional asymmetry) translates directly:
```
VCB: "suppressed_exhaustion_authentic — visible pore detail required — left eyebrow 2mm higher"
→ Prompt: "expression of suppressed authentic exhaustion, eyes slightly heavy with visible fatigue lines, mouth neutral with slight downward tension, realistic skin texture with visible pore detail across nose bridge and cheeks, natural facial asymmetry with left eyebrow naturally higher than right, not artificially symmetrical"
```

**Environmental Grammar → Prompt Scene Block**
The five grammar parameters translate to scene composition:
```
VCB: {light_quality_signal: "11pm_institutional", spatial_density: 9, temporal_signal: "stillness_late_night", world_color_temp_kelvin: 4200, subject_frame_height_ratio_pct: 40}
→ Prompt: "late night interior environment, institutional overhead lighting quality consistent with past midnight, 8-10 objects visible in background including documents and everyday items suggesting accumulated work, complete environmental stillness suggesting the world is asleep, background ambient color temperature 4200K, subject occupies approximately 40% of frame height positioned lower in frame, environment feels larger and more imposing than the subject"
```

**Intentional Imperfection → Prompt Imperfection Block**
```
VCB: "slightly askew book on desk edge"
→ Prompt: "one book on the desk edge slightly askew as if moved and not repositioned, minor environmental irregularity, authentic inhabited quality, not a perfectly styled set"
```

### 7.3 The Anti-Generic Specificity Mechanism

After assembling all blocks, Paradoxe appends a mandatory anti-generic constraint block to every prompt. This constraint explicitly names what the image must NOT resemble — using the Level 2 Anti-Draft principle from the existing CCF architecture:

```
Anti-Generic Block (always appended):
"NOT: generic stock photography. NOT: Canva template aesthetic. NOT: artificial lighting setup with visible studio quality. NOT: overly posed or staged composition. NOT: the visual average of coaching photography. The image must be specifically and recognizably different from generic motivational content."
```

For coaching segment-specific anti-generic constraint, Paradoxe reads the enemy typology from the script JSON package:
```
Script enemy_typology: "performative success culture"
→ Additional constraint: "NOT: trophy or achievement imagery. NOT: external success performance poses. The scene must communicate internal reality, not external presentation."
```

### 7.4 Complete RunningHub Task Payload

Paradoxe compiles the complete RunningHub API task payload per slide:

```json
{
  "workflowId": "RH-WF-CAROUSEL-GHIBLI-001",
  "inputs": {
    "prompt": "[Full assembled prompt string from all PSSL field translations + anti-generic block]",
    "reference_image_url": "https://assets.ccp.io/characters/coach-avatar-001-ref.png",
    "reference_image_strength": 0.85,
    "aspect_ratio": "1:1",
    "style_preset": "ghibli_warm_illustration",
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

The Conscious Canva App is the composition preview, editing, and approval layer of the CVE. It sits between RunningHub (render execution) and Notion delivery (coach approval). Its three jobs are:

1. **Pre-populated template loading** — receives the VCB JSON, loads the correct recipe template, pre-populates all content slots (text, image placeholders, layout parameters) from the VCB
2. **RunningHub output reception** — receives generated image URLs from the RunningHub API response and places them into the correct canvas layer slots
3. **Human editing layer** — provides full canvas editing capability for the 5% of cases where the generated composition requires adjustment before approval

The Conscious Canva App is built on the canva-clone repository (https://github.com/Davronov-Alimardon/canva-clone), customized to serve the CVE's specific workflow. The coach is not designing — the system has already designed. The canvas exists for the 5% exception, not the 95% case.

### 8.2 Customizations to the Canva-Clone Base

The canva-clone base requires the following customizations:

**A — Template System**
The existing canva-clone's template system is replaced with a CVE template registry. Templates are not generic design layouts — they are recipe-specific structural containers. Each template corresponds to one recipe protocol variant (by recipe × visual style × aspect ratio). Templates contain:
- Named layer slots mapped to VCB fields (background_layer, character_layer_slide_1 through N, text_layer_primary, text_layer_secondary, etc.)
- Pre-configured layout constraints (text zone positions, character zone dimensions, bleed specifications for seamless carousel edges)
- Typography defaults per arc stage (font family, size, weight, tracking — all pre-set from the recipe specification)
- Color zone assignments (which canvas areas map to which chromatic spec fields in the VCB)

**B — VCB Intake API**
A new endpoint receives the VCB JSON from Abel and auto-populates all template slots:
```
POST /api/compositions/create
Body: {vcb: VCB_JSON_PAYLOAD}
Response: {composition_id, canvas_state, populated_slots, pending_slots}
```
Text slots (primary_text, secondary_text, CTA text) are populated immediately from VCB typography fields. Image slots remain as placeholder elements pending RunningHub delivery.

**C — RunningHub Asset Reception**
A webhook endpoint receives RunningHub task completion events:
```
POST /api/assets/receive
Body: {task_id, output_url, slide_number, vcb_id}
```
On receipt, the specified image URL is placed into the correct canvas image layer slot. The composition panel updates in real-time as each slide's image arrives from RunningHub.

**D — Stripped Features**
The following canva-clone features are removed or hidden from the coach interface as they are irrelevant to the CVE workflow:
- Template gallery browser (replaced by auto-loaded VCB-driven template)
- Font selector (typography is arc-stage driven, not manual)
- Color picker for primary elements (chromatic spec is PSSL-driven, not manual)
- Background upload (backgrounds are RunningHub-generated or from Photo Deck)

The editing capabilities that REMAIN available:
- Element repositioning (move, resize, realign)
- Text editing within existing text layers
- Image replacement (swap a RunningHub output for a Photo Deck image or alternative)
- Layer visibility toggle
- Export controls

**E — Approval and Publish Flow**
The canvas interface includes three action controls:
- **Approve** — marks composition as approved, triggers Notion sync of full output JSON
- **Request Regeneration** — returns the composition to the RunningHub queue with an optional text note specifying what needs to change (note goes to Paradoxe for prompt revision)
- **Edit and Approve** — manual canvas edits followed by approval

### 8.3 Template Library Structure

The template library contains entries for each combination of recipe protocol × visual style × aspect ratio:

```
TPL-RELIEF-PEAK-001: Relief Peak | Ghibli Warm Illustration | 1x1 Square
TPL-RELIEF-PEAK-002: Relief Peak | Semi-Realistic Digital | 1x1 Square
TPL-RELIEF-PEAK-003: Relief Peak | Cinematic Realism | 1x1 Square
TPL-DOPAMINE-CLIFF-001: Dopamine Cliff | Semi-Realistic | 1x1 Square
TPL-9GRID-001: 9-Grid Accumulation | Semi-Realistic | 3x3 grid layout
TPL-CASE-STUDY-PHOTO-001: Case Study | Real Photography | 1x1 Square
TPL-CASE-STUDY-ILLUS-001: Case Study | Illustration | 1x1 Square
TPL-DEBUNKING-001: Debunking | All Styles | 1x1 Square
TPL-OBS-HUMOR-GHIBLI-001: Observational Humor | Ghibli | 1x1 Square
TPL-WCS-CINE-001: Worst Case Scenario | Cinematic | 1x1 Square
TPL-LISTICLE-001: Listicle | Multi-Style | 1x1 Square
TPL-COMPARISON-001: Comparison | All Styles | Square or 4x5
TPL-POLL-STEREO-001: Poll Stereotypical | All Styles | 1x1 Square
TPL-TIMELINE-001: Visual Timeline | All Styles | 1x1 Square
TPL-CONTRAST-SINGLE-001: Conceptual Contrast Simultaneous | All Styles | 1x1 Square
TPL-CONTRAST-CAROUSEL-001: Conceptual Contrast Sequential | All Styles | 1x1 Square
```

### 8.4 Seamless Horizontal Carousel Export

For carousel formats, the Conscious Canva App must support a seamless horizontal export mode — the original architecture that made the previous carousel work successful. This outputs all slides as a single wide horizontal canvas, then slices them at the correct dimensions for individual slide delivery. Environmental elements specified with edge bleed in the template design brief are designed to continue across slide boundaries, preserving the cinematic pan grammar on the final Instagram carousel.

Export pipeline:
```
All slides composed → Stitch to single wide canvas → Slice to individual slide dimensions → Export individual PNGs → Package as ZIP → Deliver to Notion photo stack
```

---

## Section 9 — RunningHub API Integration

### 9.1 Integration Overview

RunningHub (https://www.runninghub.cn/runninghub-api-doc-en/) provides the AI image generation execution layer. The CVE uses RunningHub's workflow execution API to run pre-built ComfyUI workflows per recipe protocol and visual style combination.

Base API endpoint: `https://www.runninghub.cn/api/`  
Authentication: API key stored as encrypted environment variable `RUNNINGHUB_API_KEY`  
Integration managed by: Paradoxe (task creation and parameter compilation), Visual Validation Agent (status polling and output receipt)

### 9.2 Core API Operations

**Task Creation**
```
POST /task/openapi/create
Headers: {Content-Type: application/json}
Body: {
  "workflowId": "RH-WF-CAROUSEL-GHIBLI-001",
  "apiKey": "{{RUNNINGHUB_API_KEY}}",
  "nodeInfoList": [
    {
      "nodeId": "6",
      "fieldName": "text",
      "fieldValue": "{{assembled_prompt_string}}"
    },
    {
      "nodeId": "14",
      "fieldName": "image",
      "fieldValue": "{{reference_image_base64_or_url}}"
    },
    {
      "nodeId": "22",
      "fieldName": "strength",
      "fieldValue": "0.85"
    }
  ]
}
Response: {
  "code": 0,
  "msg": "success",
  "data": {
    "taskId": "{{task_id}}",
    "clientId": "{{client_id}}"
  }
}
```

**Task Status Polling**
```
POST /task/openapi/status
Body: {"taskId": "{{task_id}}", "apiKey": "{{RUNNINGHUB_API_KEY}}"}
Response: {
  "code": 0,
  "data": {
    "taskStatus": "SUCCESS | FAILED | QUEUED | RUNNING",
    "outputs": [
      {
        "nodeId": "30",
        "fileUrl": "{{generated_image_url}}"
      }
    ]
  }
}
```

**Status Polling Strategy:** Exponential backoff starting at 5 seconds, doubling up to 60 seconds. Maximum wait: 10 minutes per slide. Timeout triggers operator notification and queues for manual retry.

**Task Cancellation**
```
POST /task/openapi/cancel
Body: {"taskId": "{{task_id}}", "apiKey": "{{RUNNINGHUB_API_KEY}}"}
```

### 9.3 RunningHub Workflow Library

The CVE maintains pre-built ComfyUI workflows in RunningHub for each production requirement:

| Workflow ID | Recipe Family | Visual Style | Notes |
|---|---|---|---|
| RH-WF-CAROUSEL-GHIBLI-001 | Carousel (all) | Ghibli Warm Illustration | Reference image input for character consistency |
| RH-WF-CAROUSEL-SEMI-001 | Carousel (all) | Semi-Realistic Digital | Reference image input |
| RH-WF-CAROUSEL-CINE-001 | Carousel (all) | Cinematic Color-Graded | Real photo reference optional |
| RH-WF-CAROUSEL-CLIFF-001 | Dopamine Cliff | Mixed (accumulation warm, cliff cold) | Dynamic color temperature per slide |
| RH-WF-SINGLE-GHIBLI-001 | Single Image | Ghibli Illustration | Standard single frame |
| RH-WF-SINGLE-CINE-001 | Single Image | Desaturated Cinematic | Worst Case Scenario + Fear-Anxiety |
| RH-WF-GRID9-001 | 9-Grid Accumulation | Semi-Realistic | Full grid output, sliced post-generation |
| RH-WF-COMPARISON-001 | Comparison/Poll | Semi-Realistic | Two-character gaze architecture enforcement |
| RH-WF-CASE-STUDY-001 | Case Study | Illustration | Character arc expression matching |
| RH-WF-DEBUNKING-001 | Debunking | Semi-Realistic | Color angle parameter injection |
| RH-WF-LISTICLE-001 | Listicle | Multi-Style | Style set per subtype |
| RH-WF-TIMELINE-001 | Visual Timeline | Semi-Realistic | Chronological color arc across slides |

### 9.4 Reference Image Architecture

For every slide containing a named cast character, Paradoxe passes the character's canonical reference image from DEP-VIS-004. The RunningHub workflows are built with an IP-Adapter or equivalent identity-preserving node that applies the reference image to maintain character identity-critical features while allowing free variation in expression, environment, and lighting.

Reference image specifications:
- Format: PNG, transparent background preferred
- Resolution: minimum 1024×1024
- Framing: face and upper body, neutral expression, frontal angle
- Stored at: `https://assets.ccp.io/characters/{{coach_id}}/{{character_id}}-ref.png`
- Backed up to: Supabase storage bucket `character_references`

First-generation protocol: when a new cast character is created, the first generation session produces 6 candidate images from a clean text description. The operator selects the best candidate. This selection becomes the locked canonical reference image for all subsequent generations. The character's first generation is the identity anchor — this decision is irreversible without explicit operator action.

### 9.5 Error Handling and Failure Protocols

| Failure Type | Detection | Response | Receipt Chain |
|---|---|---|---|
| Task creation failure (API error) | HTTP non-200 response | Retry 3× with exponential backoff, then operator alert | Logged as FAILED, batch not halted |
| Task timeout (>10 minutes) | Status polling timeout | Cancel task, regenerate with same parameters once, then operator alert | Logged as TIMEOUT |
| AGSS score below threshold | Visual Validation Agent post-generation | Automatic prompt revision by Paradoxe, regeneration once | Logged as AGSS_FAIL, second attempt logged |
| Authenticity check failure | Visual Validation Agent post-generation | Regeneration with enhanced imperfection specification | Logged as AUTH_FAIL |
| Character drift detected | Visual Validation Agent facial comparison | Regeneration with reference_image_strength increased to 0.95 | Logged as DRIFT_DETECTED |
| All retries failed | Three consecutive failures | Operator alert, slide flagged in Notion as PENDING_HUMAN_REVIEW | Receipt Chain break, batch quarantined per slide not per full batch |

---

## Section 10 — New Agents, Dependencies, and Registry Updates

### 10.1 New Dependencies — Registry V5.1 Update

The CVE introduces five new dependency entries into the Registry:

**DEP-VIS-001: Tribal Imagen Activation Registry (TIAR)**  
Format: Supabase JSONB + monthly corpus pipeline  
Parent Dependencies: DEP-ENG-007 (Tribe Intelligence), DEP-ENG-002 (Audience Avatar)  
Tier: 2 (Pattern Recognition and Dynamic Context)  
Update Cadence: Monthly automated cycle + triggered updates on entropy threshold crossing

**DEP-VIS-002: Visual Recipe Protocol Library**  
Format: YAML  
Parent Dependencies: DEP-LIB-008 (Archetype Classification Library), DEP-LIB-009 (Compiled Skill Template Registry)  
Tier: 0 (Immutable Constants — Visual Layer)  
Update Cadence: On recipe architecture changes only

**DEP-VIS-003: Stage Set Emotional Architecture Library**  
Format: YAML + Supabase lookup  
Parent Dependencies: DEP-ENG-002 (Audience Avatar) for cultural segment  
Tier: 1 (Strategic Foundational Context)  
Update Cadence: Quarterly PAD score validation updates + cultural variant expansion

**DEP-VIS-004: Brand Character Reference Archive**  
Format: PNG assets + JSONB metadata  
Parent Dependencies: None (visual identity data)  
Tier: 1 (Strategic Foundational Context)  
Update Cadence: On new character creation or reference image refresh only

**DEP-VIS-005: Visual Composition Brief Schema**  
Format: JSON Schema definition  
Parent Dependencies: DEP-VIS-001, DEP-VIS-002, DEP-VIS-003, DEP-VIS-004  
Tier: 4 (Output Schema Definition)  
Update Cadence: On CVE architecture updates only

### 10.2 New Agents

**TIAR Monitor Agent**  
Department: Perception Department  
Function: Monthly corpus analysis, Shannon entropy calculation, decay monitoring, refresh triggering  
Tools: `firecrawl_wrapper.py` (corpus ingestion), `entropy_calculator.py` (new Python tool)  
Schedule: Monthly automated execution + triggered on entropy threshold crossing  
Writes to: DEP-VIS-001

**Visual Validation Agent**  
Department: Safety and Governance Department  
Function: Post-generation image quality assessment — AGSS scoring, authenticity feature verification, character drift detection  
Tools: `image_analysis_wrapper.py` (new Python tool for feature extraction and comparison)  
Triggers: After each RunningHub task completion event  
Writes to: VCB output field, Receipt Chain Guard log  
Passes/Fails: AGSS threshold (6.5/10 minimum), authenticity checklist (items 1-3 mandatory), character drift detection

### 10.3 Upgraded Agents

**Abel — Visual Composition Planner**  
Previous capabilities: Visual recipe routing, basic template assignment  
New capabilities: Full VCB generation (all 30 PSSL parameters per slide), TIAR query and entropy confirmation, PAD-based stage set selection, ISC injection position calculation, tribal noun-visual congruent pairing, semantic conflict specification, accumulation prohibition audit, peak-end priority flagging  
New reads: DEP-VIS-001, DEP-VIS-002, DEP-VIS-003, DEP-VIS-004, DEP-ENG-011 full script JSON package

**Paradoxe — PSSL Prompt Compiler**  
Previous capabilities: Basic visual prompt synthesis  
New capabilities: PSSL field-to-prompt translation (all field types), anti-generic constraint block assembly, enemy-typology-based specificity constraints, dual-vector gaze geometry prompt directives, cultural color profile incorporation, reference image parameter assembly, complete RunningHub task payload compilation  
New reads: DEP-VIS-005 (VCB), DEP-VIS-004 (Character Reference Archive)

### 10.4 New Validation Gate

**Gate C-09: PSSL Completeness Check**  
Runs: After VCB generation, before Paradoxe receives the VCB  
Checks:
- All slides have populated lighting_grammar (must contain temporal signal and shadow specification — adjective-only values fail)
- All slides have numeric saturation_pct (word descriptions fail)
- All text slides have primary_text with minimum 3 concrete nouns from TIAR active list
- All slides with characters have numeric head_rotation_degrees AND pupil_position_ratio_pct
- All stages have PAD scores in environmental_grammar
- All tension slides have non-null incomplete_tribal_artifact
- All slides have non-null intentional_imperfection
- Resolution slides have font_weight ≤ 500 and font_category "sans_serif"

Failure behavior: Returns specific field-level errors to Abel for revision. Does not halt the full batch — flags the specific composition for revision while other compositions proceed.

### 10.5 New Adapter

**`visual-arc-adapter`**  
Function: Injects arc type from the script JSON package into Abel's composition planning process, ensuring all downstream PSSL parameter generation is arc-grounded  
Active for: All visual production pipeline executions

**`tiar-adapter`**  
Function: Queries DEP-VIS-001 before script text element generation (upstream in Script Generation Skills) and before visual composition text finalization (downstream in Abel). Injects active noun list and expired noun list.  
Active for: Script Generation Skills execution + Abel VCB generation

**`pssl-compiler-adapter`**  
Function: Validates that Paradoxe receives a fully gate-passed VCB before compiling RunningHub payloads  
Active for: All RunningHub task creation events

---

## Section 11 — The Full Output JSON Contract

### 11.1 Visual Production Output Structure

Every completed visual production unit is stored as a Visual Production Output (VPO) — the complete record of what was produced and how. This is the closed-loop document that makes visual production fully auditable.

```json
{
  "vpo_id": "VPO-20260317-0042",
  "asset_id": "CCFA-C01-03-26-0042",
  "fingerprint_id": "FP-20260317-0042",
  "vcb_id": "VCB-20260317-0042",
  "recipe_protocol": "relief_peak_carousel_recipe",
  "visual_output_type": "carousel",
  "coaching_segment": "conscious_business",
  "visual_style": "ghibli_warm_illustration",
  "production_status": "approved",
  "production_timestamp": "2026-03-17T14:23:11Z",
  
  "script_reference": {
    "script_text": "...",
    "hook_text": "The 3am integrity check",
    "archetype": "recognition_story",
    "mood_state": "escape",
    "arc_type": "tension_release"
  },
  
  "composition_brief": {
    "vcb_snapshot": "{{full_VCB_JSON_as_specified_in_Section_3}}"
  },
  
  "runninghub_execution_log": [
    {
      "slide_number": 1,
      "workflow_id": "RH-WF-CAROUSEL-GHIBLI-001",
      "task_id": "rh_task_abc123",
      "prompt_compiled_by": "Paradoxe",
      "prompt_hash": "sha256_hash_of_prompt_string",
      "execution_start": "2026-03-17T14:18:02Z",
      "execution_complete": "2026-03-17T14:19:47Z",
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
    {
      "slide_number": 1,
      "canvas_composition_url": "https://assets.ccp.io/compositions/VPO-20260317-0042/slide_1_final.png",
      "status": "approved"
    }
  ],
  
  "seamless_export": {
    "horizontal_stitch_url": "https://assets.ccp.io/compositions/VPO-20260317-0042/carousel_full.png",
    "sliced_slides_zip": "https://assets.ccp.io/compositions/VPO-20260317-0042/slides.zip"
  },
  
  "tiar_audit": {
    "nouns_used": ["3am", "integrity", "resonance", "threshold"],
    "entropy_status_at_production": {
      "3am": "active_0.12",
      "integrity": "active_0.18",
      "resonance": "active_0.15",
      "threshold": "active_0.19"
    },
    "expired_nouns_blocked": ["authentic", "freedom", "alignment"],
    "tiar_query_timestamp": "2026-03-17T14:15:22Z"
  },
  
  "notion_content_card": {
    "hook_text": "The 3am integrity check",
    "caption": "{{full_caption_from_script_JSON}}",
    "posting_recommendation": "Escape mode content — post Tuesday or Thursday 7-9pm when audience arousal is descending from work stress. Avoid Monday mornings (high avoidance state) and Friday afternoons (escape to leisure, not introspection).",
    "why_this_visual": "Relief Peak arc built on Tension-Release physiology. Struggle slides (1-3) use 11pm institutional grammar targeting somatic body-memory of late-night integrity decisions. Semiotic injection at slide 4 fires the ISC peak alignment at 75% of sequence. Resolution slide designed as standalone shareable identity declaration. All tribal nouns (3am, integrity, resonance, threshold) confirmed active with entropy below decay threshold. Visual style: Ghibli warm illustration matching TII 45 (warming audience stage) — transportation contract over authentication contract.",
    "leadership_farming_note": "This post exercises Authentic Vulnerability (Leadership Trait 3) — coach is naming their own experience of compromising integrity, not observing it in others. High-scoring moment for the Leadership Development Engine."
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

### 11.2 VPO Storage and Retrieval

Visual Production Outputs are stored in Supabase table `visual_production_outputs` with the `asset_id` and `fingerprint_id` as foreign keys linking to the CCF's content production records. This creates the closed-loop performance tracking architecture: downstream engagement metrics from the Publer API (save rate, share rate, comment rate) are written back to the VPO record, and the TIAR Monitor Agent reads VPO performance data when updating entropy monitoring and visual congruent performance ratings.

---

## Section 12 — Production Governance, Quality Gates, and Notion Delivery

### 12.1 The Visual Production Quality Gate Sequence

Visual production runs a five-stage quality gate sequence. Unlike the CCF's Triple-Pass Gate (which can halt the entire batch), CVE gates operate at the individual composition level — a single composition failure does not halt other compositions in the same weekly batch.

**Gate V-01: TIAR Entropy Check**  
Runs: Abel pre-composition, before VCB generation  
Checks: All concrete nouns in the script JSON hook_concrete_nouns and active_tribal_nouns have entropy_status "active" or "tribal_potential"  
On failure: Returns entropy warning flag to CCF pipeline. Script hook text flagged for revision. Visual production proceeds with a `tiar_warning: true` flag in the VCB — composition can complete but the Notion delivery card includes the warning for operator review.

**Gate V-02: PSSL Completeness Check (C-09)**  
Runs: After Abel VCB generation, before Paradoxe receives VCB  
Checks: All 30 required PSSL fields populated and type-valid (full field list in Section 10.4)  
On failure: Returns specific field-level errors to Abel. Abel revises and resubmits. Maximum 2 revision cycles before operator escalation.

**Gate V-03: Accumulation Prohibition Audit**  
Runs: Within Gate V-02 for accumulation-type recipes  
Checks: No prohibited completion imagery specified in any accumulation slide's tribal_noun_visual_congruent or environmental_grammar  
On failure: Abel revises the offending slide's visual congruent specification.

**Gate V-04: Visual Validation Post-Generation**  
Runs: After each RunningHub task completion  
Checks: AGSS score ≥ 6.5, authenticity checklist items 1-3 passed, character drift not detected  
On failure: Automatic prompt revision by Paradoxe and one regeneration attempt. On second failure: operator alert, slide flagged as PENDING_HUMAN_REVIEW in Notion. Composition delivered with placeholder in the flagged slide slot.

**Gate V-05: Receipt Chain Confirmation**  
Runs: After all slides confirmed and canvas composition complete  
Checks: All previous gate passes logged with timestamps, no broken chain links  
On failure: Full composition quarantined and operator notified. Not delivered to Notion until chain is repaired.

### 12.2 The Notion Visual Content Card

Every approved visual production unit delivers the following card structure to the coach's Notion workspace:

**Card Header**
- Universal Asset ID (linked to parent script card)
- Recipe protocol name in plain language ("Relief Peak Carousel")
- Production status (Approved / Pending Review)
- Production date and visual style

**Preview Section**
- Carousel preview: horizontal stitch image showing all slides in sequence
- Individual slide preview: each slide numbered and labeled with arc stage
- Download link: ZIP file containing all individual slide PNGs at final export dimensions

**Content Ready to Copy**
- Hook text (ready to paste as Instagram caption first line)
- Full caption with hashtag recommendations
- Posting day and time recommendation (derived from mood state routing)

**Why This Visual Was Built This Way** (plain language summary — not technical, written for the coach)

Example:
> "Your 5-slide carousel follows an arc designed to move the audience through tension and release — the physiological pattern that produces the deepest sense of having been understood. Slides 1-3 use late-night environmental grammar (institutional light, visible cognitive load, world slightly overwhelming) to activate your audience's body-memory of their own integrity moments. Slide 4 is where everything shifts — warm light enters for the first time, your character's expression names the recognition, the color world changes. Slide 5 is designed to be a standalone image your audience could screenshot and save. All four tribal words in this carousel (3am, integrity, resonance, threshold) are currently active with no decay flags. Your audience will feel found, not lectured."

**Leadership Farming Note**
- Which leadership trait this content exercises (from the Leadership Scorecard)
- Why it develops that specific trait

**Technical Audit Summary** (collapsed by default — operator accessible)
- TIAR entropy status per noun
- AGSS scores per slide
- Authenticity check results
- Receipt Chain status
- Fingerprint ID linking to full VPO record

### 12.3 The 36 Weekly Pieces: Visual Production Allocation

The CVE integrates into the existing 36-piece weekly production target. Not every piece requires full CVE visual production — format assignments determine what visual production path each piece takes:

| Format | Weekly Volume (est.) | Visual Production Path |
|---|---|---|
| Carousels (all types) | 12-15 | Full CVE pipeline → RunningHub → Canva App |
| Single images (memes, polls, quotes) | 8-10 | Full CVE pipeline → RunningHub → Canva App |
| Short-form video | 6-8 | Visual Brief Export only (art direction document) |
| Webinar slides | 1-2 (when applicable) | Existing Excalidraw pipeline (Benjamin) |
| Tier lists | 1-2 | Existing Excalidraw pipeline (Benjamin) |

The visual production queue runs in parallel with script validation — as scripts pass the Triple-Pass Gate, they immediately enter the CVE queue. The weekly batch timing tolerates the CVE pipeline's full execution window (RunningHub generation + canvas composition + Notion sync) within the overall CCF weekly pipeline window.

### 12.4 The Sovereign Image Rule: Complete Specification

The PRD's Sovereign Image Rule is extended by the CVE as follows:

**Rule 1 (Original):** The coach's actual face, likeness, or personal embodiment is never artificially generated. AI-generated visual elements may only represent abstract client scenarios or metaphorical concepts.

**Rule 2 (CVE Extension A):** AI-generated avatar characters and real coach photography exist in separate content tracks and never appear in the same visual composition. There is no composite of real + avatar.

**Rule 3 (CVE Extension B):** Real coach photography used in visual compositions is sourced exclusively from the Personal Branding Photo Deck in Notion. Abel queries the Photo Deck before planning any composition requiring real photography. If no suitable photo exists for the required emotional register, the system generates a photo session recommendation in the Notion workspace rather than substituting AI generation.

**Rule 4 (CVE Extension C):** When real photography is used in a composition, the PSSL parameters for lighting grammar, chromatic spec, and environmental grammar are used as production direction specifications for the photography session — not as AI generation parameters. The PSSL does not only serve AI generation. It serves the entire visual production pipeline, including real photography art direction.

---

## Appendix A — Registry V5.1 Delta (CVE Additions)

Summary of all new Registry entries introduced by the CVE:

**New Dependencies:**
- DEP-VIS-001: Tribal Imagen Activation Registry (TIAR) — Tier 2
- DEP-VIS-002: Visual Recipe Protocol Library — Tier 0
- DEP-VIS-003: Stage Set Emotional Architecture Library — Tier 1
- DEP-VIS-004: Brand Character Reference Archive — Tier 1
- DEP-VIS-005: Visual Composition Brief Schema — Tier 4

**New Protocols:**
- DEP-PROTO-017: PSSL Compilation Protocol — governs VCB generation and Paradoxe compilation
- DEP-PROTO-018: Visual Production Quality Gate Protocol — governs V-01 through V-05 gate sequence
- DEP-PROTO-019: TIAR Entropy Monitoring Protocol — governs monthly corpus analysis and refresh triggering

**New Agents:**
- TIAR Monitor Agent (Perception Department)
- Visual Validation Agent (Safety and Governance Department)

**Upgraded Agents:**
- Abel: Visual Recipe Router → Visual Composition Planner
- Paradoxe: Visual Prompt Synthesizer → PSSL Prompt Compiler

**New Validation Gates:**
- Gate C-09: PSSL Completeness Check
- Gate V-01: TIAR Entropy Check
- Gate V-02: PSSL Completeness Check (composition level)
- Gate V-03: Accumulation Prohibition Audit
- Gate V-04: Visual Validation Post-Generation
- Gate V-05: Receipt Chain Confirmation

**New Adapters:**
- `visual-arc-adapter`
- `tiar-adapter`
- `pssl-compiler-adapter`

**New Python Tools:**
- `entropy_calculator.py` — Shannon entropy computation for TIAR monitoring
- `image_analysis_wrapper.py` — AGSS scoring, authenticity feature extraction, character drift detection

---

## Appendix B — Functional Requirements Update to PRD

The following Functional Requirements are added to the PRD's Capability Area 6 (Webinar & Visual Content):

**FR-VIS-01:** The system can generate complete Visual Composition Briefs (VCBs) for all script archetypes flagged for visual production, incorporating full PSSL parameters (somatic targets, lighting grammar, chromatic specifications, character specifications, environmental grammar, typography arc, and tribal noun-visual congruent pairs) per slide. VCBs must pass Gate C-09 (PSSL Completeness Check) before proceeding to prompt compilation.

**FR-VIS-02:** The system can query the Tribal Imagen Activation Registry (DEP-VIS-001) before any script generation AND before visual composition text finalization, injecting active high-charge tribal nouns as required vocabulary and blocking expired high-entropy nouns. The registry maintains entropy monitoring for minimum 150 core tribal nouns per coaching segment on a monthly update cadence.

**FR-VIS-03:** The system can compile PSSL-compliant prompts via Paradoxe and execute RunningHub API workflows for all visual output types (carousel, single image, 9-grid accumulation), passing character reference images for identity-critical feature consistency. RunningHub task execution must complete within 10 minutes per slide, with automatic retry and operator escalation on timeout.

**FR-VIS-04:** The system can validate all RunningHub outputs through the Visual Validation Agent, scoring each generated image against the Anti-Generic Specificity Scale (minimum 6.5/10) and verifying the three mandatory avatar authenticity features (Expression Naturalness, Facial Proportion, Skin Texture) before composition approval. Images failing thresholds are automatically returned to Paradoxe for prompt revision and one regeneration attempt.

**FR-VIS-05:** The system can load VCB JSON into the Conscious Canva App, pre-populate all template slots, receive RunningHub output URLs into correct canvas layer positions, and provide full canvas editing capability for operator adjustments, exporting final compositions as individual PNG files and seamless horizontal stitch files for carousel formats.

**FR-VIS-06:** The system can deliver complete Visual Production Output (VPO) records to the coach's Notion workspace including: composition preview, hook text and caption ready to copy, posting recommendations, plain-language "why this visual was built this way" rationale, leadership farming notes, and a collapsed technical audit summary with TIAR entropy status, AGSS scores, and Receipt Chain confirmation.

---

*End of CVE Documentation V1.0*  
*Next update triggered by: RunningHub workflow library expansion, TIAR first validation run, Canva App template library build completion*
