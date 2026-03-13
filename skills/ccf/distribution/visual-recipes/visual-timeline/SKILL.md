---
name: "Visual Recipe - Visual Timeline"
description: "Visual generation formula for Visual Timeline format"
session_id: ccf-visual-recipe
phase: distribution
recipe_id: "visual-timeline"
inputs:
  - config.yaml
  - scripts/final/{blueprint_id}_script.md (AUTHORIZED)
  - intelligence/soul/soul_values.json (for brand avatar)
  - intelligence/tribe/tribe_profile.json (for H9 visual recognition codes)
outputs:
  - visuals/recipes/{blueprint_id}_visual-timeline_visual_prompt.md
depends_on: [story-5.2]
---

# <a id="_kirqcgli2mcm"></a>__🌞 Visual Timeline Visual Recipe Protocol__


---

## 🚨 CRITICAL RULES — 4 LAWS OF VISUAL RECIPE DISTILLATION

1. **Law of the Biological Hook:** Images must trigger an autonomic response. Every visual prompt MUST explicitly dictate a "Biological Hook" (e.g., vertigo, claustrophobia, grounded warmth).
2. **Law of Sensory Zoom (Compression):** Avoid flat, wide-angle summaries. Prompts MUST enforce a specific sensory focus (e.g., "macro detail of white knuckles," "dust motes in sunbeam").
3. **Law of Mode Constraints:** Every visual scene MUST align with a specific emotional MODE (TENSION, VULNERABILITY, RECOGNITION). Generic "happy" or "sad" is insufficient.
4. **Law of Visual Authenticity:** No stock photography tropes. All references must trace to real-world ethnographic artifacts (curated by H13 asset-curator).

---

This document outlines the specific operational logic for the "Conscious Art Director" agent when executing the Visual Timeline visual recipe\. This recipe is designed to transform chronological narratives into visually compelling sequences that showcase evolution, progression, and transformation over time through strategic character aging and environmental evolution\.

## <a id="_xx2eptk7hdrv"></a>__Recipe Details__

__Recipe ID:__ visual\_timeline\_recipe  
 __Archetype Category:__ Visual Timeline  
 __Purpose:__ To generate a multi\-scene visual narrative that chronologically maps change, evolution, or transformation over time, creating an emotionally resonant journey from historical context to present reality\.

## <a id="_9m7doh7nmsdh"></a>__Recipe Prompt Logic__

Your task is to generate a visual recipe for a Visual Timeline—a chronological sequence that transforms temporal progression into a visually compelling narrative of evolution and change\.

### <a id="_9t55hx760k1x"></a>__Step 1: Temporal Arc Analysis__

Analyze the validated\_content to identify the timeline structure:

- __Origin Point:__ The historical "Then" state that establishes the baseline
- __Evolution Milestones:__ 3\-5 key turning points that show progression
- __Present Climax:__ The "Now" state that represents the current transformation peak
- __Narrative Momentum:__ The emotional journey from past to present

### <a id="_9e6xv0luujit"></a>__Step 2: Character Age Progression Strategy__

For Visual Timeline content, implement strategic character aging:

- __Origin Scene:__ Use youngest available age from character\_lexicon to represent the historical starting point
- __Evolution Scenes:__ Progress through middle ages to show gradual change
- __Climax Scene:__ Use current age to represent the present\-day culmination
- __Age Consistency:__ Ensure logical age progression that supports the timeline's emotional arc

### <a id="_79o4h03cr1rk"></a>__Step 3: Generate Base Scene Prompt \(The Origin \- "Then"\)__

Create a complete, fused prompt for the historical starting point by combining:

- __CHARACTER:__ Youngest age reflecting the naive/early state of the timeline's subject
- __ENVIRONMENT:__ Period\-appropriate setting that establishes the historical context
- __EMOTIONAL STATE:__ Wonder, uncertainty, or limitation reflecting the "before" state
- __VISUAL STYLE:__ Ghibli\-style with nostalgic, sepia\-toned elements to emphasize the historical nature
- __LITERAL EXPRESSIONS:__ Use descriptive facial expressions \(no semiotic injection for base scene\)

### <a id="_wdhy4hevfs72"></a>__Step 4: Generate Variant Prompts \(The Evolution Journey\)__

Create 6\-8 variant objects representing the chronological progression:

__Variants 1\-5: The Milestones__

- Each modification\_prompt should age the character and evolve the environment
- Progress through available character ages chronologically
- Show technological, social, or conceptual advancement in each scene
- Use literal facial expressions to maintain focus on temporal progression

__Variant 6\-7: The Climax \(Present Day\)__

- Transform to contemporary setting representing "Now"
- Use current character age
- Show the full transformation and current state

### <a id="_qhyw5xjjg19v"></a>__Step 5: Strategic Semiotic Injection__

For the final "Present Day" scene ONLY:

- Analyze the facial\_expression\_lexicon to find the most appropriate expression for the timeline's emotional payoff
- Select expressions that capture amazement, realization, or triumph \(e\.g\., "mind\_blown", "success\_kid\_triumph"\)
- Inject the selected expression's memetic\_reference\_prompt into the final modification\_prompt
- This creates maximum emotional impact at the moment of present\-day revelation

### <a id="_5dfl5w4gmn6u"></a>__Step 6: Environmental Evolution Integration__

Ensure each scene reflects authentic temporal progression:

- __Technology Evolution:__ Show relevant technological advancement for each era
- __Social Context:__ Reflect changing social norms and environments
- __Visual Markers:__ Include period\-appropriate clothing, architecture, and cultural elements
- __Consistency:__ Maintain character recognition while showing natural aging

## <a id="_qoo7cd308hzi"></a>__Output Requirements__

Generate a JSON object with this exact structure:

\{

  "base\_scene\_prompt": "\[Complete Ghibli\-style prompt for origin point including youngest character age, historical environment, wonder/limitation emotions, and literal facial expression\]",

  "variant\_prompts": \[

    \{

      "scene\_name": "First Evolution",

      "modification\_prompt": "\[Age character slightly, update environment to show early progress, maintain literal expressions\]"

    \},

    \{

      "scene\_name": "Major Milestone",

      "modification\_prompt": "\[Continue aging character, show significant environmental/technological advancement\]"

    \},

    \{

      "scene\_name": "Acceleration Period",

      "modification\_prompt": "\[Further character aging, show rapid change in environment/context\]"

    \},

    \{

      "scene\_name": "Modern Transition",

      "modification\_prompt": "\[Near\-current character age, show contemporary elements emerging\]"

    \},

    \{

      "scene\_name": "Present Day Peak",

      "modification\_prompt": "\[Current character age, full contemporary environment\]"

    \},

    \{

      "scene\_name": "Timeline Climax",

      "modification\_prompt": "\[Final scene with current age, present\-day setting\. MUST include memetic\_reference\_prompt from facial\_expression\_lexicon for emotional payoff of timeline realization\]"

    \}

  \],

  "strategic\_notes": \{

    "selected\_archetype": "Visual Timeline",

    "temporal\_span": "\[Time period covered by the timeline\]",

    "casting\_decision": "\[Character age progression strategy and reasoning\]",

    "semiotic\_injection\_scene": "Timeline Climax",

    "selected\_expression": "\[Expression ID from facial\_expression\_lexicon\]",

    "evolution\_theme": "\[Core transformation theme visualized\]"

  \}

\}

## <a id="_njiul9em53wu"></a>__Quality Standards__

- The timeline should show clear visual progression from past to present
- Character aging should feel natural and support the narrative arc
- Environmental changes should authentically reflect temporal progression
- The present\-day climax should feel surprising and emotionally satisfying
- Each scene should build narrative momentum toward the final revelation
- The progression should make complex temporal changes feel intuitive and engaging

## <a id="_lph2yie67tfl"></a>__Variant Count Specification__

__Required Number of Variants:__ 6\-8 scenes total \(including base scene\)

- 1 Base Scene \(Origin Point\)
- 4\-6 Evolution/Milestone Scenes
- 1\-2 Present Day Climax Scenes

This structure ensures comprehensive temporal coverage while maintaining visual engagement and narrative momentum throughout the chronological journey\.


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
