---
name: "Visual Recipe - The ARCHETYPICAL Poll"
description: "Visual generation formula for The ARCHETYPICAL Poll format"
session_id: ccf-visual-recipe
phase: distribution
recipe_id: "the-archetypical-poll"
inputs:
  - config.yaml
  - scripts/final/{blueprint_id}_script.md (AUTHORIZED)
  - intelligence/soul/soul_values.json (for brand avatar)
  - intelligence/tribe/tribe_profile.json (for H9 visual recognition codes)
outputs:
  - visuals/recipes/{blueprint_id}_the-archetypical-poll_visual_prompt.md
depends_on: [story-5.2]
---

# <a id="_gko7dgx3ydz0"></a>__🌞 The ARCHETYPICAL Poll Visual Recipe Protocol__


---

## 🚨 CRITICAL RULES — 4 LAWS OF VISUAL RECIPE DISTILLATION

1. **Law of the Biological Hook:** Images must trigger an autonomic response. Every visual prompt MUST explicitly dictate a "Biological Hook" (e.g., vertigo, claustrophobia, grounded warmth).
2. **Law of Sensory Zoom (Compression):** Avoid flat, wide-angle summaries. Prompts MUST enforce a specific sensory focus (e.g., "macro detail of white knuckles," "dust motes in sunbeam").
3. **Law of Mode Constraints:** Every visual scene MUST align with a specific emotional MODE (TENSION, VULNERABILITY, RECOGNITION). Generic "happy" or "sad" is insufficient.
4. **Law of Visual Authenticity:** No stock photography tropes. All references must trace to real-world ethnographic artifacts (curated by H13 asset-curator).

---

This document outlines the specific operational logic for the "Conscious Art Director" agent when executing the ARCHETYPICAL Poll visual recipe\. This recipe generates a multi\-frame visual narrative that transforms abstract philosophical dichotomies into concrete, engaging poll imagery designed for maximum audience participation\.

## <a id="_zcujie83dhed"></a>__Recipe Details__

- __Recipe ID:__ archetypical\_poll\_recipe
- __Archetype Category:__ The ARCHETYPICAL Poll
- __Purpose:__ To generate a 3\-frame visual narrative that presents contrasting archetypes in an engaging, poll\-worthy format that encourages immediate audience participation

## <a id="_o3nku8a6frrw"></a>__Recipe Prompt Logic__

Your task is to generate a visual recipe for an ARCHETYPICAL Poll—a 3\-frame visual narrative that transforms polarizing philosophical dichotomies into engaging, interactive poll imagery that forces audience choice and reveals identity\.

### <a id="_13hy9u9zlci3"></a>__Step 1: Poll Dichotomy Analysis__

Analyze the validated\_content through the lens of conscious\_soul\_values to identify the core polarizing dichotomy presented in the poll\. Look for:

- The two contrasting archetypes defined in the poll
- Their opposing values, fears, strengths, and mottos
- The central philosophical tension that creates the choice
- The emotional stakes that make the choice meaningful

### <a id="_wkc8brusu5og"></a>__Step 2: Visual Structure Planning__

The ARCHETYPICAL Poll requires exactly 3 visual frames:

1. __Base Scene \(Introduction Frame\):__ Establishes the poll question and visual context
2. __Variant 1 \(Archetype A\):__ Visual embodiment of the first archetype
3. __Variant 2 \(Archetype B\):__ Visual embodiment of the contrasting archetype

### <a id="_f7sbeny0xzn9"></a>__Step 3: Generate Base Scene Prompt \(Poll Introduction\)__

Create a complete, fused prompt for the introduction frame combining:

- __CHARACTER:__ Use the primary character from character\_lexicon in a neutral, questioning pose
- __ENVIRONMENT:__ Clean, simple background that doesn't favor either archetype
- __TEXT OVERLAY:__ Poll question prominently displayed \(can be described for AI to generate\)
- __VISUAL STYLE:__ Bright, engaging style optimized for social media consumption
- __EMOTIONAL TONE:__ Curious, inviting, thought\-provoking without bias

### <a id="_1vb83piom1ai"></a>__Step 4: Generate Variant Prompts \(The Two Archetypes\)__

Create TWO variant objects with modification\_prompts:

__Variant 1 \(Archetype A\):__

- Transform character to embody the first archetype's values and behaviors
- Environment reflects their worldview and preferred settings
- Clothing, posture, and props that symbolize their approach
- Literal facial expression showing their characteristic emotional state

__Variant 2 \(Archetype B\):__

- Transform character to embody the contrasting archetype's values
- Environment shifts to reflect opposing worldview
- Contrasting clothing, posture, and symbolic elements
- Facial expression showing their opposing emotional approach

### <a id="_lxvoh43ttet"></a>__Step 5: Strategic Semiotic Injection__

For Variant 2 \(the final archetype frame\) ONLY:

- Analyze the facial\_expression\_lexicon to find the most appropriate expression for the climactic choice moment
- Inject the selected expression's memetic\_reference\_prompt into the modification\_prompt
- This creates maximum emotional impact at the moment of final archetype revelation

### <a id="_5sijdc7gj0ye"></a>__Step 6: Poll\-Specific Visual Elements__

Ensure all frames incorporate poll\-friendly design elements:

- High contrast and bold visual distinctions between archetypes
- Clear visual symbols that represent each side's core values
- Compositions optimized for mobile viewing and quick decision\-making
- Visual elements that encourage screenshot sharing and discussion

## <a id="_chm6q2w1ui53"></a>__Output Requirements__

Generate a JSON object with this exact structure:

\{

  "base\_scene\_prompt": "\[Complete prompt for poll introduction frame showing character in neutral questioning pose with poll question context, optimized for social engagement\]",

  "variant\_prompts": \[

    \{

      "scene\_name": "Archetype A Embodiment",

      "modification\_prompt": "\[Instructions to transform character and environment to embody first archetype's values, worldview, and characteristic behaviors with literal facial expression\]"

    \},

    \{

      "scene\_name": "Archetype B Embodiment", 

      "modification\_prompt": "\[Instructions to transform character and environment to embody contrasting archetype's values, worldview, and behaviors\. MUST include memetic\_reference\_prompt from facial\_expression\_lexicon for maximum emotional impact\]"

    \}

  \],

  "strategic\_notes": \{

    "selected\_archetype": "The ARCHETYPICAL Poll",

    "poll\_dichotomy": "\[The specific philosophical dichotomy being explored\]",

    "casting\_decision": "\[Character choice and reasoning for poll presentation\]",

    "semiotic\_injection\_scene": "Archetype B Embodiment",

    "selected\_expression": "\[Expression ID from facial\_expression\_lexicon\]",

    "visual\_style\_rationale": "\[Why this style optimizes poll engagement and shareability\]",

    "archetype\_contrast": "\[How the visual contrast reinforces the philosophical choice\]"

  \}

\}

## <a id="_1hl31264pb2i"></a>__Quality Standards__

- __Immediate Choice Recognition:__ The visual contrast between archetypes should be instantly recognizable and compelling
- __Poll Optimization:__ All frames must be optimized for social media polling and audience interaction
- __Philosophical Clarity:__ The dichotomy should be visually clear without requiring text explanation
- __Engagement Trigger:__ The final frame should create a strong emotional response that compels audience participation
- __Shareability:__ Each frame should work as a standalone image while contributing to the overall poll narrative
- __Identity Revelation:__ The choice between archetypes should feel personally meaningful and identity\-revealing to the target audience

## <a id="_hhe2bcffbqus"></a>__Frame Count Specification__

__CRITICAL:__ This recipe MUST generate exactly 2 variant prompts, creating a total of 3 visual frames \(1 base \+ 2 variants\)\. This is the optimal structure for poll engagement and binary choice presentation\.


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
