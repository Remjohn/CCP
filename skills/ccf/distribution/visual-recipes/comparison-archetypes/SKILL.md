---
name: "Visual Recipe - Comparison Archetypes"
description: "Visual generation formula for Comparison Archetypes format"
session_id: ccf-visual-recipe
phase: distribution
recipe_id: "comparison-archetypes"
inputs:
  - config.yaml
  - scripts/final/{blueprint_id}_script.md (AUTHORIZED)
  - intelligence/soul/soul_values.json (for brand avatar)
  - intelligence/tribe/tribe_profile.json (for H9 visual recognition codes)
outputs:
  - visuals/recipes/{blueprint_id}_comparison-archetypes_visual_prompt.md
depends_on: [story-5.2]
---

# <a id="_l5s9utkr5ns2"></a>__🌞 Comparison Archetypes Visual Recipe Protocol__


---

## 🚨 CRITICAL RULES — 4 LAWS OF VISUAL RECIPE DISTILLATION

1. **Law of the Biological Hook:** Images must trigger an autonomic response. Every visual prompt MUST explicitly dictate a "Biological Hook" (e.g., vertigo, claustrophobia, grounded warmth).
2. **Law of Sensory Zoom (Compression):** Avoid flat, wide-angle summaries. Prompts MUST enforce a specific sensory focus (e.g., "macro detail of white knuckles," "dust motes in sunbeam").
3. **Law of Mode Constraints:** Every visual scene MUST align with a specific emotional MODE (TENSION, VULNERABILITY, RECOGNITION). Generic "happy" or "sad" is insufficient.
4. **Law of Visual Authenticity:** No stock photography tropes. All references must trace to real-world ethnographic artifacts (curated by H13 asset-curator).

---

This document outlines the specific operational logic for the "Conscious Art Director" agent when executing Comparison Archetype visual recipes\. This recipe is designed to generate powerful two\-part visual narratives that create immediate emotional impact through strategic juxtaposition, optimized for each comparison subtype's unique psychological trigger\.

## <a id="_ead00btogxsk"></a>__Recipe Details__

__Recipe ID:__ comparison\_archetypes\_recipe  
 __Archetype Category:__ Comparison Archetypes  
 __Purpose:__ To generate two\-part visual narratives that maximize emotional response through strategic contrast presentation, tailored to the specific psychological mechanism of each comparison subtype\.

## <a id="_n3ajhxx7nbfs"></a>__Recipe Prompt Logic__

Your task is to generate a visual recipe for a Comparison Archetype—a two\-part visual narrative that creates maximum emotional impact through strategic juxtaposition\. Each comparison subtype has unique requirements for emotional trigger optimization\.

### <a id="_tafrrv1xgy0p"></a>__Step 1: Comparison Subtype Analysis__

Analyze the validated\_content to identify the specific comparison archetype and its emotional mechanism:

__The Nostalgia Comparison:__ Triggers warm familiarity through temporal contrast

- Focus on cultural markers, childhood elements, and generational signifiers
- Emphasize warmth, comfort, and bittersweet emotions

__The Funny Relatable Comparison:__ Triggers social bonding through shared experience

- Focus on universal experiences, everyday absurdities, and "we've all been there" moments
- Emphasize humor, recognition, and social connection

__The Shocking Comparison:__ Triggers awe and disbelief through scale revelation

- Focus on dramatic scale differences, transformations, or mind\-bending facts
- Emphasize surprise, amazement, and cognitive recalibration

__The Outrageous Comparison:__ Triggers indignation and moral outrage

- Focus on injustices, inequalities, and hypocrisies that demand action
- Emphasize anger, injustice, and call\-to\-action energy

__The Surprising Comparison:__ Triggers curiosity and perspective expansion

- Focus on unexpected connections, hidden similarities, and assumption challenges
- Emphasize discovery, insight, and intellectual satisfaction

### <a id="_4hsg3gp00z6"></a>__Step 2: Strategic Character Selection__

Choose character age and type based on comparison requirements:

- __Temporal Comparisons \(Nostalgia\):__ Use different ages of the same character or generational representatives
- __Universal Comparisons \(Funny Relatable\):__ Use current age character in relatable situations
- __Scale Comparisons \(Shocking\):__ Use character as scale reference or reaction vessel
- __Justice Comparisons \(Outrageous\):__ Use character as victim/beneficiary of the contrast
- __Insight Comparisons \(Surprising\):__ Use character as discovery agent or perspective guide

### <a id="_6wuigzshroiw"></a>__Step 3: Generate Base Scene Prompt \(Side A \- Setup/Before State\)__

Create a complete, fused prompt for the first side of the comparison by combining:

- __CHARACTER:__ Selected from character\_lexicon with appropriate age and emotional state
- __ENVIRONMENT:__ Setting that establishes the first comparative element with rich contextual details
- __EMOTIONAL TONE:__ Aligned with the comparison subtype's initial emotional setup
- __VISUAL STYLE:__ Ghibli\-style optimized for the comparison's emotional requirements
- __FACIAL EXPRESSION:__ Literal description that sets up the emotional contrast \(NOT from facial\_expression\_lexicon\)

### <a id="_njemne9mjpdm"></a>__Step 4: Generate Single Variant Prompt \(Side B \- Reveal/After State\)__

Create ONE variant object with a modification\_prompt containing:

- __ENVIRONMENTAL TRANSFORMATION:__ Complete shift to the contrasting comparative element
- __EMOTIONAL TRANSFORMATION:__ Character reaction appropriate to the comparison revelation
- __CONTEXTUAL SHIFT:__ All supporting visual elements that reinforce the contrast
- __NARRATIVE PAYOFF:__ Visual elements that deliver the comparison's intended impact

### <a id="_tveas7pt4mrs"></a>__Step 5: Strategic Semiotic Injection__

For the variant scene \(Side B\) ONLY:

- Analyze the facial\_expression\_lexicon to find the most appropriate expression for the comparison's emotional payoff:
	- __Nostalgia:__ Expressions of wistful recognition or bittersweet realization
	- __Funny Relatable:__ Expressions of humorous recognition or comedic realization
	- __Shocking:__ Expressions of amazement, disbelief, or mind\-blown revelation
	- __Outrageous:__ Expressions of indignation, anger, or moral outrage
	- __Surprising:__ Expressions of delighted discovery or intellectual satisfaction
- Inject the selected expression's memetic\_reference\_prompt into the modification\_prompt
- This creates maximum emotional impact at the moment of comparative revelation

### <a id="_pe6ak97yzf9t"></a>__Step 6: Comparison Optimization__

Ensure both sides maximize the intended psychological trigger:

- __Visual Clarity:__ Both sides should be immediately comprehensible
- __Emotional Escalation:__ Side B should amplify the emotional setup from Side A
- __Cultural Resonance:__ Use tribe\-specific markers that enhance recognition and impact
- __Shareability Elements:__ Include visual hooks that compel social sharing

## <a id="_e8k5caodbjdk"></a>__Output Requirements__

Generate a JSON object with this exact structure:

\{

  "base\_scene\_prompt": "\[Complete Ghibli\-style prompt for Side A \(setup/before state\) including character selection, environment establishing first comparative element, emotional setup, and literal facial expression\]",

  "variant\_prompts": \[

    \{

      "scene\_name": "Comparison Reveal",

      "modification\_prompt": "\[Instructions to transform to Side B \(reveal/after state\)\. MUST include environmental shift, emotional transformation, and memetic\_reference\_prompt from facial\_expression\_lexicon for maximum comparative impact\]"

    \}

  \],

  "strategic\_notes": \{

    "selected\_archetype": "\[Specific comparison subtype identified\]",

    "comparison\_mechanism": "\[The psychological trigger being leveraged\]",

    "casting\_decision": "\[Character choice and age reasoning\]",

    "semiotic\_injection\_scene": "Comparison Reveal",

    "selected\_expression": "\[Expression ID from facial\_expression\_lexicon\]",

    "emotional\_journey": "\[Side A emotion → Side B emotion pathway\]",

    "shareability\_factors": "\[Key elements that drive viral potential\]"

  \}

\}

## <a id="_pqd00g8q79td"></a>__Variant Count Specification__

__CRITICAL:__ Comparison Archetypes always generate exactly ONE variant scene\.

- Base Scene: Establishes Side A of the comparison
- Single Variant: Delivers Side B reveal with strategic semiotic injection
- Total Visual Output: 2 images \(Base \+ 1 Variant\)

## <a id="_1el0h4bbdzy2"></a>__Quality Standards__

- The comparison should create immediate emotional recognition within 3 seconds
- Side B should deliver a clear emotional payoff that compels sharing
- Both sides must feel culturally authentic to the target tribe
- The contrast should be visually striking and psychologically impactful
- The transformation from A to B should maximize the specific comparison archetype's emotional mechanism


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
