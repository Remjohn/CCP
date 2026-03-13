---
name: "Visual Recipe - Observational Humor"
description: "Visual generation formula for Observational Humor format"
session_id: ccf-visual-recipe
phase: distribution
recipe_id: "observational-humor"
inputs:
  - config.yaml
  - scripts/final/{blueprint_id}_script.md (AUTHORIZED)
  - intelligence/soul/soul_values.json (for brand avatar)
  - intelligence/tribe/tribe_profile.json (for H9 visual recognition codes)
outputs:
  - visuals/recipes/{blueprint_id}_observational-humor_visual_prompt.md
depends_on: [story-5.2]
---

# <a id="_yyjrl6b0z0ul"></a>__🌞 Observational Humor Visual Recipe Protocol__


---

## 🚨 CRITICAL RULES — 4 LAWS OF VISUAL RECIPE DISTILLATION

1. **Law of the Biological Hook:** Images must trigger an autonomic response. Every visual prompt MUST explicitly dictate a "Biological Hook" (e.g., vertigo, claustrophobia, grounded warmth).
2. **Law of Sensory Zoom (Compression):** Avoid flat, wide-angle summaries. Prompts MUST enforce a specific sensory focus (e.g., "macro detail of white knuckles," "dust motes in sunbeam").
3. **Law of Mode Constraints:** Every visual scene MUST align with a specific emotional MODE (TENSION, VULNERABILITY, RECOGNITION). Generic "happy" or "sad" is insufficient.
4. **Law of Visual Authenticity:** No stock photography tropes. All references must trace to real-world ethnographic artifacts (curated by H13 asset-curator).

---

This document outlines the specific operational logic for the "Conscious Art Director" agent when executing the Observational Humor visual recipe\. This recipe is designed to transform relatable, everyday comedy into visually engaging single\-frame moments that maximize shareability and community connection through shared laughter\.

## <a id="_h6hucv348lv4"></a>__Recipe Details__

__Recipe ID:__ observational\_humor\_recipe  
 __Archetype Category:__ Observational Humor  
 __Purpose:__ To generate a single, powerful visual moment that captures the essence of everyday absurdity, making viewers instantly recognize themselves and compulsively share the relatable truth\.

## <a id="_g1dgzjryqn27"></a>__Recipe Prompt Logic__

Your task is to generate a visual recipe for Observational Humor—a single\-frame visual that transforms everyday frustrations and universal truths into an instantly recognizable, shareable moment of comedic connection\.

### <a id="_crrwsnpcpe47"></a>__Step 1: Comedy Moment Analysis__

Analyze the validated\_content to identify the core comedic elements:

- __The Universal Situation__: What everyday scenario is being highlighted?
- __The Relatable Frustration__: What specific human quirk or struggle is being exposed?
- __The Comedic Truth__: What "it's funny because it's true" revelation drives the humor?
- __The Shareability Factor__: What makes this so relatable that people MUST tag their friends?

### <a id="_e4iu78val3ub"></a>__Step 2: Visual Comedy Staging__

Determine the most comedically effective visual approach based on the humor type:

__For "Isn't it weird that\.\.\." observations:__

- Focus on capturing the absurd behavior in action
- Emphasize the contradiction between intention and reality

__For "Expectation vs\. Reality" scenarios:__

- Create a visual that simultaneously shows both the hope and the disappointing truth
- Use environmental details to heighten the contrast

__For "Universal Internal Monologue" content:__

- Focus heavily on facial expressions that externalize internal thoughts
- Use body language that screams the unspoken frustration

### <a id="_uqavu8ypndmg"></a>__Step 3: Strategic Character Selection and Age Assignment__

Select the most relatable character age from the character\_lexicon based on:

- __Target demographic alignment__ with the tribe\_soul\_profile
- __Maximum relatability__ for the specific everyday situation
- __Optimal expression potential__ for the comedic moment

### <a id="_276o51f24481"></a>__Step 4: Generate Base Scene Prompt \(The Comedy Gold Moment\)__

Create a complete, fused prompt that captures the peak comedic moment by combining:

__CHARACTER__: Selected age \+ the perfect comedic expression that embodies the universal frustration or realization\.

__ENVIRONMENT__: Hyper\-specific, recognizable setting that every viewer has experienced \(kitchen at 2am, cluttered desk, bathroom mirror, etc\.\)\.

__ACTION__: The exact moment of comedic truth \- the behavior, gesture, or situation that makes everyone go "OMG that's literally me\."

__COMEDIC DETAILS__: Specific visual elements that amplify the humor \(empty fridge with one condiment, 47 browser tabs open, laundry pile that's achieved sentience, etc\.\)\.

__STYLE__: Ghibli\-style with enhanced emotional expressiveness to maximize the comedic impact and relatability\.

### <a id="_dzfbqeeo09a5"></a>__Step 5: Strategic Semiotic Injection__

This is CRITICAL for Observational Humor:

- Analyze the facial\_expression\_lexicon to find the expression that perfectly captures the comedic emotion
- Select expressions that embody: exasperation, recognition, "I can't even", knowing resignation, or comedic despair
- Inject the selected expression's memetic\_reference\_prompt into the base\_scene\_prompt
- This creates maximum comedic impact and instant recognition

### <a id="_63ip5r6ooze"></a>__Step 6: Relatability Amplification__

Ensure the visual incorporates elements from the tribe\_soul\_profile that create immediate recognition:

- Use visual markers that signal "this person gets my life"
- Include environmental details that reflect the audience's actual living situations
- Make every element feel like it was pulled directly from the viewer's own experience

## <a id="_sdvxvzababmm"></a>__Output Requirements__

Generate a JSON object with this exact structure:

\{

  "base\_scene\_prompt": "\[Complete Ghibli\-style prompt capturing the peak comedic moment\. Must include character age, hyper\-specific relatable environment, the exact moment of comedic truth, and memetic\_reference\_prompt from facial\_expression\_lexicon for maximum comedic impact\]",

  "variant\_prompts": \[\],

  "strategic\_notes": \{

    "selected\_archetype": "Observational Humor",

    "comedy\_type\_identified": "\[Specific type: 'Isn't it weird', 'Expectation vs Reality', or 'Internal Monologue'\]",

    "casting\_decision": "\[Character age selected and reasoning for maximum relatability\]",

    "semiotic\_injection\_scene": "Base Scene",

    "selected\_expression": "\[Expression ID from facial\_expression\_lexicon\]",

    "relatability\_factors": "\[Specific elements included to maximize 'that's so me' response\]",

    "shareability\_triggers": "\[Visual elements designed to compel tagging and sharing\]"

  \}

\}

## <a id="_gymoyl8yvv8v"></a>__Quality Standards__

- The visual must trigger an immediate "That is literally me\!" response
- The comedic moment should be so relatable it feels like surveillance
- The expression must perfectly externalize what everyone thinks but doesn't say
- Every environmental detail should amplify the shared human experience
- The image should be so shareable that NOT tagging a friend feels impossible
- The visual should create instant community through shared comedic recognition

## <a id="_jx3bh38pujun"></a>__Key Success Metrics__

__Instant Recognition__: Viewer immediately sees themselves in the scenario  
 __Comedic Timing__: The visual captures the exact moment of peak comedy  
 __Social Currency__: The relatability is so high it demands to be shared  
 __Tribal Bonding__: Creates "we're all in this together" feeling through humor  
 __Authentic Voice__: Feels genuinely aligned with the client's comedic perspective


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
