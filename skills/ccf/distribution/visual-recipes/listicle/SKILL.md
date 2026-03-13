---
name: "Visual Recipe - Listicle"
description: "Visual generation formula for Listicle format"
session_id: ccf-visual-recipe
phase: distribution
recipe_id: "listicle"
inputs:
  - config.yaml
  - scripts/final/{blueprint_id}_script.md (AUTHORIZED)
  - intelligence/soul/soul_values.json (for brand avatar)
  - intelligence/tribe/tribe_profile.json (for H9 visual recognition codes)
outputs:
  - visuals/recipes/{blueprint_id}_listicle_visual_prompt.md
depends_on: [story-5.2]
---

# <a id="_ysaz8d1vasb8"></a>__🌞 Listicle Visual Recipe Protocol__


---

## 🚨 CRITICAL RULES — 4 LAWS OF VISUAL RECIPE DISTILLATION

1. **Law of the Biological Hook:** Images must trigger an autonomic response. Every visual prompt MUST explicitly dictate a "Biological Hook" (e.g., vertigo, claustrophobia, grounded warmth).
2. **Law of Sensory Zoom (Compression):** Avoid flat, wide-angle summaries. Prompts MUST enforce a specific sensory focus (e.g., "macro detail of white knuckles," "dust motes in sunbeam").
3. **Law of Mode Constraints:** Every visual scene MUST align with a specific emotional MODE (TENSION, VULNERABILITY, RECOGNITION). Generic "happy" or "sad" is insufficient.
4. **Law of Visual Authenticity:** No stock photography tropes. All references must trace to real-world ethnographic artifacts (curated by H13 asset-curator).

---

This document outlines the specific operational logic for the "Conscious Art Director" agent when executing the Listicle visual recipe\. This recipe is designed to transform informational list content into visually compelling, emotionally engaging sequential narratives that maximize comprehension and shareability across all listicle emotional angles\.

## <a id="_o4mbga10s26e"></a>__Recipe Details__

- __Recipe ID__: listicle\_visual\_recipe
- __Archetype Category__: Listicle \(All Emotional Variants\)
- __Purpose__: To generate a multi\-scene visual sequence that transforms list\-based information into emotionally resonant, easy\-to\-digest visual storytelling

## <a id="_fxgb01ib7lwy"></a>__Recipe Prompt Logic__

Your task is to generate a visual recipe for a Listicle—a multi\-scene visual narrative that transforms informational list content into compelling, sequential storytelling optimized for the specific emotional angle of the listicle type\.

### <a id="_oa1428rfnt2w"></a>__Step 1: Listicle Emotional Angle Analysis__

Analyze the validated\_content to identify the specific listicle emotional angle and adapt your visual approach accordingly:

- __Shocking Listicle__: Focus on dramatic reveals and escalating intensity
- __Funny Relatable Listicle__: Emphasize comedic timing and relatable character expressions
- __Nostalgia Listicle__: Create warm, memory\-evoking atmospheres with period\-appropriate styling
- __Curiosity\-Intriguing Listicle__: Build mystery and discovery through visual progression
- __Fear\-Anxiety Listicle__: Establish tension and resolution patterns
- __Hope & Inspiration Listicle__: Show transformation and uplifting progression
- __Outrageous Listicle__: Maximize visual spectacle and impossible scenarios

### <a id="_ul8l21tysg9o"></a>__Step 2: Determine Variant Count__

Based on the validated\_content, determine the optimal number of visual scenes:

- __3\-5 Items__: Generate ALL items as visual scenes \(Base \+ 2\-4 Variants\)
- __6\-8 Items__: Select the 5 most visually compelling items \(Base \+ 4 Variants\)
- __9\+ Items__: Condense to 5 key moments that represent the full emotional journey \(Base \+ 4 Variants\)

### <a id="_a4dpvh8neefx"></a>__Step 3: Generate Base Scene Prompt \(First List Item\)__

Create a complete, fused prompt for the opening item by combining:

- __CHARACTER__: Selected from character\_lexicon with age appropriate to content context
- __ENVIRONMENT__: Setting that establishes the listicle's thematic world
- __ACTION__: Behavior embodying the first item's core concept
- __EMOTIONAL TONE__: Literal facial expression that sets up the emotional journey
- __STYLE__: Choose based on emotional angle:
	- Ghibli\-style for Hope & Inspiration, Nostalgia
	- Mixed Ghibli\-Photorealism for Relatable, Curiosity
	- Cinematic Realism for Shocking, Fear\-Anxiety, Outrageous

### <a id="_yorm9tcfu44u"></a>__Step 4: Generate Variant Prompts \(Subsequent List Items\)__

Create an array of modification prompts for each subsequent scene, ensuring:

- __Progressive Revelation__: Each scene builds upon the previous
- __Environmental Evolution__: Settings change to match each item's unique context
- __Character Consistency__: Same character, evolving emotions and actions
- __Emotional Escalation__: Intensity builds toward the strategic payoff moment

### <a id="_exj88byqlzuu"></a>__Step 5: Strategic Semiotic Injection__

Identify the climactic item \(typically the final or most impactful list item\):

- For __Shocking__: The most jaw\-dropping revelation
- For __Funny Relatable__: The biggest laugh or most relatable moment
- For __Nostalgia__: The deepest emotional memory trigger
- For __Curiosity\-Intriguing__: The most mind\-blowing discovery
- For __Fear\-Anxiety__: The ultimate warning or protection
- For __Hope & Inspiration__: The most triumphant transformation
- For __Outrageous__: The most impossible/spectacular feat

For this climactic scene ONLY:

- Analyze the facial\_expression\_lexicon for the most appropriate expression
- Inject the selected expression's memetic\_reference\_prompt into the modification\_prompt
- This creates maximum emotional payoff at the moment of greatest impact

### <a id="_l1tai78x8h1s"></a>__Step 6: Ensure List Logic Coherence__

Verify that the visual sequence:

- Maintains clear progression from item to item
- Builds emotional momentum toward the payoff
- Remains true to the listicle's informational purpose
- Creates natural stopping points that encourage continued viewing

## <a id="_2tp023vkksqo"></a>__Output Requirements__

Generate a JSON object with this exact structure:

\{

  "base\_scene\_prompt": "\[Complete prompt for first list item including character selection, environment, action, literal facial expression, and chosen visual style\]",

  "variant\_prompts": \[

    \{

      "scene\_name": "Item 2: \[Brief Description\]",

      "modification\_prompt": "\[Instructions to evolve scene for second list item\]"

    \},

    \{

      "scene\_name": "Item 3: \[Brief Description\]",

      "modification\_prompt": "\[Instructions to evolve scene for third list item\]"

    \},

    \{

      "scene\_name": "Item 4: \[Brief Description\]",

      "modification\_prompt": "\[Instructions to evolve scene for fourth list item\]"

    \},

    \{

      "scene\_name": "Item 5: \[Brief Description\] \- CLIMAX",

      "modification\_prompt": "\[Instructions for final/climactic item\. MUST include memetic\_reference\_prompt from facial\_expression\_lexicon for maximum emotional payoff\]"

    \}

  \],

  "strategic\_notes": \{

    "selected\_archetype": "Listicle",

    "listicle\_emotional\_angle": "\[Specific listicle type identified\]",

    "total\_items\_in\_content": "\[Number of items in original listicle\]",

    "visual\_scenes\_created": "\[Number of scenes generated\]",

    "casting\_decision": "\[Character choice and reasoning\]",

    "semiotic\_injection\_scene": "\[Which scene received strategic emotional injection\]",

    "selected\_expression": "\[Expression ID from facial\_expression\_lexicon if used\]",

    "visual\_style\_rationale": "\[Why this style was chosen for this emotional angle\]",

    "emotional\_progression": "\[How emotional intensity builds through the sequence\]"

  \}

\}

## <a id="_bo9g8z7drcci"></a>__Quality Standards__

- __Information Clarity__: Each scene clearly represents its corresponding list item
- __Emotional Escalation__: Intensity builds naturally toward the climactic moment
- __Visual Variety__: Each scene offers distinct visual elements while maintaining character consistency
- __Shareability__: Individual scenes can stand alone while the sequence tells a complete story
- __Cultural Resonance__: Content aligns with the target tribe's values and visual language
- __Immediate Comprehension__: Each item's value is instantly recognizable

## <a id="_vxzq5aoijoku"></a>__Special Considerations by Emotional Angle__

- __Shocking__: Use dramatic lighting and composition changes to emphasize reveals
- __Funny Relatable__: Focus on character expressions and situational comedy
- __Nostalgia__: Incorporate period\-specific visual elements and warm, golden lighting
- __Curiosity\-Intriguing__: Create visual mystery with selective reveals and intriguing compositions
- __Fear\-Anxiety__: Build tension through environmental changes and character body language
- __Hope & Inspiration__: Show clear character transformation and uplifting environmental shifts
- __Outrageous__: Maximize visual spectacle with impossible scenarios and dramatic scale changes


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
