---
name: "Visual Recipe - The Controversial Dilemma Poll"
description: "Visual generation formula for The Controversial Dilemma Poll format"
session_id: ccf-visual-recipe
phase: distribution
recipe_id: "the-controversial-dilemma-poll"
inputs:
  - config.yaml
  - scripts/final/{blueprint_id}_script.md (AUTHORIZED)
  - intelligence/soul/soul_values.json (for brand avatar)
  - intelligence/tribe/tribe_profile.json (for H9 visual recognition codes)
outputs:
  - visuals/recipes/{blueprint_id}_the-controversial-dilemma-poll_visual_prompt.md
depends_on: [story-5.2]
---

# <a id="_d7r2fr30ugzp"></a>__🌞 The Controversial Dilemma Poll Visual Recipe Protocol__


---

## 🚨 CRITICAL RULES — 4 LAWS OF VISUAL RECIPE DISTILLATION

1. **Law of the Biological Hook:** Images must trigger an autonomic response. Every visual prompt MUST explicitly dictate a "Biological Hook" (e.g., vertigo, claustrophobia, grounded warmth).
2. **Law of Sensory Zoom (Compression):** Avoid flat, wide-angle summaries. Prompts MUST enforce a specific sensory focus (e.g., "macro detail of white knuckles," "dust motes in sunbeam").
3. **Law of Mode Constraints:** Every visual scene MUST align with a specific emotional MODE (TENSION, VULNERABILITY, RECOGNITION). Generic "happy" or "sad" is insufficient.
4. **Law of Visual Authenticity:** No stock photography tropes. All references must trace to real-world ethnographic artifacts (curated by H13 asset-curator).

---

This document outlines the specific operational logic for the "Conscious Art Director" agent when executing the Controversial Dilemma Poll visual recipe\. This recipe is designed to generate a powerful two\-part visual narrative that transforms current polarizing debates into emotionally resonant, split\-screen comparison imagery that forces immediate viewer engagement\.

## <a id="_kpp14u8x1ast"></a>__Recipe Details__

__Recipe ID:__ controversial\_dilemma\_poll\_recipe  
 __Archetype Category:__ The Controversial Dilemma Poll  
 __Purpose:__ To generate a two\-part visual narrative that transforms current controversial issues into stark, split\-screen comparisons that immediately convey the opposing philosophies and force audience engagement\.

## <a id="_jijxq022qj1o"></a>__Recipe Prompt Logic__

Your task is to generate a visual recipe for a Controversial Dilemma Poll—a two\-part visual narrative that transforms current polarizing debates into emotionally resonant imagery that forces immediate viewer choice and engagement\.

### <a id="_3jw2ulkzqu5z"></a>__Step 1: Current Event Dichotomy Analysis__

Analyze the validated\_content to identify the core controversial dilemma and its two opposing philosophies\. Look for:

- __The Central Conflict:__ The specific current event or social issue driving the controversy
- __Viewpoint A vs\. Viewpoint B:__ The two clearly defined opposing philosophies
- __The Hard Trade\-Offs:__ What each side sacrifices to maintain their position
- __Visual Symbols:__ How each philosophy can be represented through environment, body language, and symbolic elements

### <a id="_vb5rk9bixuue"></a>__Step 2: Strategic Character Positioning__

For this archetype, character positioning is critical to convey neutrality while showing the emotional weight of each choice:

- __Consistent Character:__ Use the SAME character across both scenes to maintain viewer focus on the philosophical choice, not the person
- __Neutral Age Selection:__ Choose the character's most relatable age from the character\_lexicon
- __Emotional Authenticity:__ Character should embody the genuine emotional weight of each philosophical position

### <a id="_asgtx5ty2m21"></a>__Step 3: Generate Base Scene Prompt \(Viewpoint A \- "First Philosophy"\)__

Create a complete, fused prompt for the first philosophical position by combining:

- __CHARACTER:__ Selected character embodying the emotional state and values of Viewpoint A
- __ENVIRONMENT:__ Setting that symbolically represents the first philosophy's priorities and worldview
- __VISUAL SYMBOLISM:__ Environmental and prop elements that immediately communicate this viewpoint's core values
- __BODY LANGUAGE:__ Posture and positioning that reflects this philosophy's approach to the dilemma
- __STYLE:__ Cinematic realism or mixed Ghibli\-photorealism for maximum emotional impact and credibility

### <a id="_vb3635ptxvmv"></a>__Step 4: Generate Variant Prompt \(Viewpoint B \- "Opposing Philosophy"\)__

Create ONE variant object with a modification\_prompt containing:

- __ENVIRONMENTAL TRANSFORMATION:__ Complete shift to setting that represents the opposing philosophy's worldview
- __SYMBOLIC REVERSAL:__ Props and visual elements that communicate Viewpoint B's priorities
- __EMOTIONAL SHIFT:__ Character's expression and body language reflecting the different emotional approach of this philosophy
- __CONTEXTUAL ELEMENTS:__ Background details that reinforce this viewpoint's values and consequences

### <a id="_eo3t89hoby5h"></a>__Step 5: Strategic Semiotic Injection__

For the variant scene \(Viewpoint B\) ONLY:

- Analyze the facial\_expression\_lexicon to find the expression that best captures the emotional core of the opposing philosophy
- Inject the selected expression's memetic\_reference\_prompt into the modification\_prompt
- This creates maximum emotional contrast between the two philosophical positions

### <a id="_yyx0s6w5whya"></a>__Step 6: Controversy Amplification__

Ensure both scenes maximize the visual tension of the dilemma:

- __Equal Visual Weight:__ Both philosophies should appear equally valid and compelling
- __Stark Contrast:__ The environmental and symbolic differences should be immediately apparent
- __Emotional Authenticity:__ Each scene should feel genuine to someone who holds that viewpoint
- __No Easy Answers:__ The visual should make the choice feel genuinely difficult

## <a id="_80tbsbkp2gdf"></a>__Output Requirements__

Generate a JSON object with this exact structure:

\{

  "base\_scene\_prompt": "\[Complete cinematic/mixed\-style prompt for Viewpoint A including character, environment symbolizing first philosophy's values, authentic emotional state, and literal facial expression\]",

  "variant\_prompts": \[

    \{

      "scene\_name": "Philosophical Opposition",

      "modification\_prompt": "\[Instructions to transform environment, symbolism, and character emotion to represent Viewpoint B\. MUST include memetic\_reference\_prompt from facial\_expression\_lexicon for maximum emotional contrast\]"

    \}

  \],

  "strategic\_notes": \{

    "selected\_archetype": "The Controversial Dilemma Poll",

    "controversy\_identified": "\[The specific current event/dilemma being visualized\]",

    "casting\_decision": "\[Character age selected and reasoning for consistency\]",

    "semiotic\_injection\_scene": "Philosophical Opposition",

    "selected\_expression": "\[Expression ID from facial\_expression\_lexicon\]",

    "visual\_philosophy\_contrast": "\[How the two environments/symbols represent opposing values\]"

  \}

\}

## <a id="_yx0whicxpcsp"></a>__Quality Standards__

- The visual contrast should make the philosophical opposition immediately clear within 3 seconds
- Both viewpoints must be presented with equal visual weight and emotional validity
- The controversy should feel current, relevant, and genuinely difficult to resolve
- The character consistency should keep focus on the philosophical choice, not personality differences
- The environmental symbolism should speak directly to each philosophy's core values
- The final images should work perfectly as a split\-screen poll format for maximum engagement

## <a id="_4eco7q28qhnr"></a>__Key Execution Notes__

- __EXACTLY 2 SCENES:__ Base scene \+ 1 variant \(no more, no less\)
- __SAME CHARACTER:__ Maintain perfect character consistency across both scenes
- __MAXIMUM CONTRAST:__ Environmental and symbolic elements should create stark philosophical opposition
- __NEUTRAL PRESENTATION:__ Both sides should appear equally valid and compelling
- __IMMEDIATE COMPREHENSION:__ The core dilemma should be visually apparent within seconds


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
