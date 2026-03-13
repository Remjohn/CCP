---
name: "Visual Recipe - Stereotypical Poll"
description: "Visual generation formula for Stereotypical Poll format"
session_id: ccf-visual-recipe
phase: distribution
recipe_id: "stereotypical-poll"
inputs:
  - config.yaml
  - scripts/final/{blueprint_id}_script.md (AUTHORIZED)
  - intelligence/soul/soul_values.json (for brand avatar)
  - intelligence/tribe/tribe_profile.json (for H9 visual recognition codes)
outputs:
  - visuals/recipes/{blueprint_id}_stereotypical-poll_visual_prompt.md
depends_on: [story-5.2]
---

# <a id="_5tdt4qm1wz1a"></a>__🌞 Stereotypical Poll Visual Recipe Protocol__


---

## 🚨 CRITICAL RULES — 4 LAWS OF VISUAL RECIPE DISTILLATION

1. **Law of the Biological Hook:** Images must trigger an autonomic response. Every visual prompt MUST explicitly dictate a "Biological Hook" (e.g., vertigo, claustrophobia, grounded warmth).
2. **Law of Sensory Zoom (Compression):** Avoid flat, wide-angle summaries. Prompts MUST enforce a specific sensory focus (e.g., "macro detail of white knuckles," "dust motes in sunbeam").
3. **Law of Mode Constraints:** Every visual scene MUST align with a specific emotional MODE (TENSION, VULNERABILITY, RECOGNITION). Generic "happy" or "sad" is insufficient.
4. **Law of Visual Authenticity:** No stock photography tropes. All references must trace to real-world ethnographic artifacts (curated by H13 asset-curator).

---

This document outlines the specific operational logic for the "Conscious Art Director" agent when executing the Poll visual recipe\. This recipe is designed to generate a two\-part split\-screen visual that transforms stereotypical dichotomies into engaging, relatable, and shareable poll imagery that maximizes audience participation\.

## <a id="_xcw8yu7ojol"></a>__Recipe Details__

- __Recipe ID:__ poll\_visual\_recipe
- __Archetype Category:__ Poll
- __Purpose:__ To generate a two\-part split\-screen visual that presents contrasting stereotypes in a humorous, instantly recognizable format that compels viewers to choose sides and engage\.

## <a id="_10fy6oxthqj7"></a>__Recipe Prompt Logic__

Your task is to generate a visual recipe for a Poll—a two\-part split\-screen visual narrative that transforms stereotypical behavioral dichotomies into instantly relatable, shareable imagery that maximizes audience participation and tribal identity validation\.

### <a id="_3x48uhx1pnf7"></a>__Step 1: Stereotype Dichotomy Analysis__

Analyze the validated\_content to identify the two contrasting personas presented in the poll\. Look for:

- __Core Behavioral Opposition:__ The fundamental difference in how each stereotype approaches the topic
- __Visual Personality Markers:__ Physical traits, clothing, environments that immediately signal each type
- __Exaggerated Characteristics:__ The humorous amplifications that make each stereotype instantly recognizable
- __Cultural Signifiers:__ Modern references, props, or settings that ground each type in current culture

### <a id="_o6az5hsm6cuh"></a>__Step 2: Strategic Character Assignment__

For each side of the poll dichotomy:

- __Character Selection:__ Choose the most appropriate character from character\_lexicon that can authentically embody each stereotype
- __Age Consideration:__ Select ages that align with the stereotypical behaviors \(e\.g\., younger for "trendy" types, older for "traditional" types\)
- __Personality Mapping:__ Ensure the character's existing traits can naturally express the exaggerated behaviors

### <a id="_fviy80q6nbak"></a>__Step 3: Generate Base Scene Prompt \(Stereotype A \- Left Side\)__

Create a complete, fused prompt for the first stereotype by combining:

- __CHARACTER:__ Selected character \+ age \+ emotions reflecting the first stereotype's "vibe"
- __ENVIRONMENT:__ Settings that immediately communicate this type's lifestyle \(home, office, coffee shop, etc\.\)
- __PROPS & DETAILS:__ Specific objects that serve as visual shorthand for the stereotype
- __STYLING:__ Clothing, accessories, and physical presentation that signals the type
- __ACTION:__ Behavior or pose that embodies their approach to the topic
- __COMPOSITION:__ Left half of a split\-screen layout with clear visual separation

### <a id="_qukm4g916mkd"></a>__Step 4: Generate Variant Prompt \(Stereotype B \- Right Side\)__

Create ONE variant object with a modification\_prompt containing:

- __ENVIRONMENTAL CONTRAST:__ Transform to the opposing stereotype's natural habitat
- __PROP TRANSFORMATION:__ Replace objects with items that signal the contrasting type
- __STYLING SHIFT:__ Change clothing, accessories, and presentation to opposite aesthetic
- __BEHAVIORAL CONTRAST:__ Modify pose and action to embody the opposing approach
- __COMPOSITIONAL ADJUSTMENT:__ Right half of split\-screen with visual balance

### <a id="_f4lo6817yzxj"></a>__Step 5: Strategic Semiotic Injection__

For the variant scene \(Stereotype B\) ONLY:

- Analyze the facial\_expression\_lexicon to find the most appropriate expression that amplifies the stereotype's personality
- Inject the selected expression's memetic\_reference\_prompt into the modification\_prompt
- This creates maximum comedic impact and relatability for the contrasting stereotype

### <a id="_rrg1lwv9gaw"></a>__Step 6: Split\-Screen Optimization__

Ensure both sides work together as a cohesive visual unit:

- __Visual Balance:__ Each side should be equally detailed and engaging
- __Clear Contrast:__ The opposition should be immediately apparent
- __Unified Style:__ Both sides maintain consistent art style and quality
- __Text Space:__ Leave appropriate areas for poll text overlay
- __Shareability:__ Optimize for social media platform dimensions

## <a id="_mssy4mkjz86p"></a>__Output Requirements__

Generate a JSON object with this exact structure:

\{

  "base\_scene\_prompt": "\[Complete Ghibli\-style or cinematic realism prompt for Stereotype A \(left side\) including character selection, environment, props, styling, action, and literal facial expression\. Must specify left half of split\-screen composition\]",

  "variant\_prompts": \[

    \{

      "scene\_name": "Stereotype Contrast",

      "modification\_prompt": "\[Instructions to transform right half of split\-screen to show contrasting stereotype\. MUST include environmental change, prop swaps, styling shifts, behavioral contrast, and memetic\_reference\_prompt from facial\_expression\_lexicon for maximum comedic impact\]"

    \}

  \],

  "strategic\_notes": \{

    "selected\_archetype": "Poll",

    "dichotomy\_identified": "\[The specific behavioral opposition being visualized\]",

    "casting\_decision": "\[Character selections and reasoning for each stereotype\]",

    "semiotic\_injection\_scene": "Stereotype Contrast",

    "selected\_expression": "\[Expression ID from facial\_expression\_lexicon\]",

    "visual\_style\_rationale": "\[Why this style enhances the stereotypical contrast\]"

  \}

\}

## <a id="_6h5sfzd6aqku"></a>__Quality Standards__

- __Immediate Recognition:__ Each stereotype should be identifiable within 2 seconds of viewing
- __Humorous Exaggeration:__ Amplified traits that feel funny, not mean\-spirited
- __Cultural Relevance:__ Props and settings that feel current and relatable to target audience
- __Split\-Screen Balance:__ Both sides equally engaging and visually compelling
- __Shareability Factor:__ Optimized composition that works across social media platforms
- __Engagement Catalyst:__ Visual elements that naturally prompt "Which one are you?" responses

## <a id="_gj0xh3g8pkj"></a>__Technical Considerations__

- __Aspect Ratio:__ Optimize for 1:1 \(Instagram\) or 16:9 \(LinkedIn/Facebook\) formats
- __Text Overlay Space:__ Ensure key areas are available for poll question and options
- __Visual Hierarchy:__ Clear distinction between left and right without competing for attention
- __Color Psychology:__ Use colors that subtly reinforce each stereotype's personality
- __Memetic Potential:__ Include subtle references that reward closer inspection and sharing


---

## Brand Avatar Injection (CCF Addition)

Before generating image prompts, inject the brand avatar's physical DNA:
- Load from soul_values.json: physical_description, styling_preferences, recurring_visual_motifs
- EVERY visual prompt that includes a person must use the brand avatar's physical DNA
- This ensures visual consistency across all content pieces

## I-R-E-V-C Session Protocol

### INGEST
- Load AUTHORIZED script
- Load soul_values.json for brand avatar physical DNA
- Load tribe_profile.json for H9 visual recognition codes (insider_objects, rejection_triggers)
- Load visual recipe protocol

### REASON
- [ORIGINAL VISUAL RECIPE LOGIC - UNCHANGED]
- Apply Brand Avatar Injection for person-based prompts
- Apply H9 Tribal Semiotic Check: verify visual elements match tribe recognition codes
- Cross-reference H13 visual asset library for REAL image alternatives per scene

### EMIT
- Output visual prompt to visuals/recipes/ directory

### VALIDATE
- Visual prompts include brand avatar physical DNA where applicable
  - **LAW 1**: Prompts explicitly define a Biological Hook.
  - **LAW 2**: Prompts utilize Sensory Zoom (macro/texture focus).
  - **LAW 3**: Prompts are constrained to a specific MODE (TENSION, VULNERABILITY, RECOGNITION).
  - **LAW 4**: Visual elements pass H9 tribal recognition code match (no generic stock tropes).
- Camera angles, lighting, and composition match recipe spec
- Prompts are production-ready for image generation APIs

### CHECKPOINT
- Update config.yaml with visual recipe status
