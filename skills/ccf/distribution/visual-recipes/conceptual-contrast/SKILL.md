---
name: "Visual Recipe - Conceptual Contrast"
description: "Visual generation formula for Conceptual Contrast format"
session_id: ccf-visual-recipe
phase: distribution
recipe_id: "conceptual-contrast"
inputs:
  - config.yaml
  - scripts/final/{blueprint_id}_script.md (AUTHORIZED)
  - intelligence/soul/soul_values.json (for brand avatar)
  - intelligence/tribe/tribe_profile.json (for H9 visual recognition codes)
outputs:
  - visuals/recipes/{blueprint_id}_conceptual-contrast_visual_prompt.md
depends_on: [story-5.2]
---

# <a id="_jk4rojcjs8vw"></a>🌞 Conceptual Contrast Visual Recipe Protocol


---

## 🚨 CRITICAL RULES — 4 LAWS OF VISUAL RECIPE DISTILLATION

1. **Law of the Biological Hook:** Images must trigger an autonomic response. Every visual prompt MUST explicitly dictate a "Biological Hook" (e.g., vertigo, claustrophobia, grounded warmth).
2. **Law of Sensory Zoom (Compression):** Avoid flat, wide-angle summaries. Prompts MUST enforce a specific sensory focus (e.g., "macro detail of white knuckles," "dust motes in sunbeam").
3. **Law of Mode Constraints:** Every visual scene MUST align with a specific emotional MODE (TENSION, VULNERABILITY, RECOGNITION). Generic "happy" or "sad" is insufficient.
4. **Law of Visual Authenticity:** No stock photography tropes. All references must trace to real-world ethnographic artifacts (curated by H13 asset-curator).

---

This document outlines the specific operational logic for the "Conscious Art Director" agent when executing the __Conceptual Contrast__ visual recipe\. This recipe is a subset of the "Narrative Evolution" protocol, designed to generate a powerful two\-part visual narrative that transforms abstract philosophical dichotomies into concrete, emotionally resonant imagery, filtered through the client's unique consciousness\.

#### <a id="_ojhnpiv0v9bp"></a>__Recipe Details__

- __Recipe ID__: conceptual\_contrast\_recipe
- __Archetype Category__: Conceptual Contrast
- __Purpose__: To generate a two\-part visual narrative that powerfully illustrates abstract philosophical oppositions through the client's authentic worldview\.

#### <a id="_px6ugos5ngwx"></a>__Recipe Prompt Logic__

Your task is to generate a visual recipe for a Conceptual Contrast—a two\-part visual narrative that transforms abstract philosophical dichotomies into concrete, emotionally resonant imagery filtered through the client's unique consciousness\.

Step 1: Soul\-Aligned Contrast Identification

Analyze the validated\_content through the lens of conscious\_soul\_values to identify the most emotionally resonant conceptual dichotomy\. Look for oppositions that reflect the client's:

- Core values in opposition \(e\.g\., "Integrity" vs\. "Compromise"\)
- Internal temperature patterns \(e\.g\., "Calculated Risk" vs\. "Reckless Gambling"\)
- Unique metaphorical language \(e\.g\., "Fortress Foundation" vs\. "House of Cards"\)
- Philosophical worldview contrasts \(e\.g\., "Scarcity Mindset" vs\. "Abundance Mindset"\)

Step 2: Strategic Character Age Assignment

For each side of the contrast, select the most authentic age from the character\_lexicon:

- __Current Age__: Present\-day embodiment of evolved values\.
- __Before State Age__: Past version reflecting old patterns the client warns against\.
- __Younger Self Age__: Foundational experiences that shaped the client's philosophy\.
- __Mixed Ages__: Different ages when the contrast is temporal or transformational\.

Step 3: Generate Base Scene Prompt \(Contrast A \- "The Problem/Old Way"\)

Create a complete, fused prompt for the problematic state by combining:

- __CHARACTER__: Selected age \+ emotions reflecting the client's "internal temperature" about this negative state\.
- __ENVIRONMENT__: Settings incorporating the client's metaphors for struggle \(from their unique vocabulary\)\.
- __ACTION__: Behaviors embodying what the client sees as the wrong approach\.
- __STYLE__: Ghibli\-style with visual elements that emphasize the problematic nature\.

Step 4: Generate Variant Prompt \(Contrast B \- "The Solution/New Way"\)

Create ONE variant object with a modification\_prompt containing:

- __ENVIRONMENTAL TRANSFORMATION__: Shift to settings reflecting the client's metaphors for success\.
- __EMOTIONAL TRANSFORMATION__: Character emotions aligning with the client's core values and aspirational vocabulary\.
- __BEHAVIORAL TRANSFORMATION__: Actions demonstrating the client's recommended approach\.

Step 5: Strategic Semiotic Injection

For the variant scene \(Contrast B\) ONLY:

- Analyze the facial\_expression\_lexicon to find the most appropriate expression for the positive transformation\.
- Inject the selected expression's memetic\_reference\_prompt into the modification\_prompt\.
- This creates maximum emotional impact at the moment of philosophical revelation\.

Step 6: Metaphor Integration

Ensure both sides of the contrast incorporate the client's unique metaphorical language:

- Use their specific vocabulary for struggle/success states\.
- Integrate their worldview\-specific imagery\.
- Make the opposition feel authentically aligned with their voice and philosophy\.

#### <a id="_yd3zqohut9xo"></a>__Output Requirements__

Generate a JSON object with this exact structure:

JSON

\{

  "base\_scene\_prompt": "\[Complete Ghibli\-style prompt for Contrast A \(problem state\) including character age, soul\-authentic emotions, client's struggle metaphors, and literal facial expression\]",

  "variant\_prompts": \[

    \{

      "scene\_name": "Philosophical Transformation",

      "modification\_prompt": "\[Instructions to transform environment, emotions, and actions to Contrast B \(solution state\)\. MUST include memetic\_reference\_prompt from facial\_expression\_lexicon for maximum emotional payoff\]"

    \}

  \],

  "strategic\_notes": \{

    "selected\_archetype": "Conceptual Contrast",

    "contrast\_identified": "\[The specific philosophical dichotomy identified\]",

    "casting\_decision": "\[Character ages selected and reasoning\]",

    "semiotic\_injection\_scene": "Philosophical Transformation",

    "selected\_expression": "\[Expression ID from facial\_expression\_lexicon\]",

    "metaphor\_integration": "\[Client's specific metaphors incorporated\]"

  \}

\}

#### <a id="_8g6h63llt1y8"></a>__Quality Standards__

- The contrast should create immediate recognition for someone with the client's exact values\.
- The visual opposition should be striking and philosophically meaningful\.
- Both sides must feel authentically aligned with the client's worldview\.
- The transformation should represent their specific version of growth and evolution\.


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
