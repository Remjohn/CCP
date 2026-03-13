---
name: "Visual Recipe - Relief Peak Carousel"
description: "Visual generation formula for Relief Peak Carousel format"
session_id: ccf-visual-recipe
phase: distribution
recipe_id: "relief-peak-carousel"
inputs:
  - config.yaml
  - scripts/final/{blueprint_id}_script.md (AUTHORIZED)
  - intelligence/soul/soul_values.json (for brand avatar)
  - intelligence/tribe/tribe_profile.json (for H9 visual recognition codes)
outputs:
  - visuals/recipes/{blueprint_id}_relief-peak-carousel_visual_prompt.md
depends_on: [story-5.2]
---

# <a id="_lz3nt37e4m63"></a>__🌞 Relief Peak Carousel Visual Recipe Protocol__


---

## 🚨 CRITICAL RULES — 4 LAWS OF VISUAL RECIPE DISTILLATION

1. **Law of the Biological Hook:** Images must trigger an autonomic response. Every visual prompt MUST explicitly dictate a "Biological Hook" (e.g., vertigo, claustrophobia, grounded warmth).
2. **Law of Sensory Zoom (Compression):** Avoid flat, wide-angle summaries. Prompts MUST enforce a specific sensory focus (e.g., "macro detail of white knuckles," "dust motes in sunbeam").
3. **Law of Mode Constraints:** Every visual scene MUST align with a specific emotional MODE (TENSION, VULNERABILITY, RECOGNITION). Generic "happy" or "sad" is insufficient.
4. **Law of Visual Authenticity:** No stock photography tropes. All references must trace to real-world ethnographic artifacts (curated by H13 asset-curator).

---

This document outlines the specific operational logic for the "Conscious Art Director" agent when executing the Relief Peak Carousel visual recipe\. This recipe generates a five\-scene visual narrative that takes the audience on an emotional journey from validated struggle to empowering relief and actionable resolution\.

## <a id="_nb7ig3l8jg0a"></a>__Recipe Details__

- __Recipe ID:__ relief\_peak\_carousel\_recipe
- __Archetype Category:__ Relief Peak Carousel
- __Purpose:__ To generate a five\-part visual narrative that validates relatable struggles, builds emotional connection, and guides the audience to a satisfying relief peak with clear, attainable solutions\.

## <a id="_ktxiv8gfdkty"></a>__Recipe Prompt Logic__

Your task is to generate a visual recipe for a Relief Peak Carousel—a five\-part visual narrative that creates an emotional bridge from struggle to relief, building strategic trust through validation and empowerment\.

### <a id="_di7r8hlj9d9b"></a>__Step 1: Struggle Validation Analysis__

Analyze the validated\_content to identify the core emotional journey structure:

- __Pain Point Identification:__ Extract the specific struggle, fear, or frustration being addressed
- __Emotional Arc Mapping:__ Trace the journey from validation → amplification → relief → proof → action
- __Audience Empathy Points:__ Identify moments where the audience will feel "seen" and understood

### <a id="_vi4qtjjzutt1"></a>__Step 2: Character Age and Emotional State Assignment__

Select the most authentic age from the character\_lexicon based on the struggle type:

- __Slides 1\-2 \(Struggle\):__ Age that reflects the target audience's current life stage experiencing this pain
- __Slide 3 \(Relief Peak\):__ Same age but showing transformation and hope
- __Slides 4\-5 \(Resolution\):__ Age that represents competence and empowerment in this area

### <a id="_j1gmxhyn904t"></a>__Step 3: Generate Base Scene Prompt \(Slide 1 \- Shared Struggle\)__

Create a complete, fused prompt for the initial validation scene by combining:

- __CHARACTER:__ Selected age with expressions of relatable stress, overwhelm, or frustration
- __ENVIRONMENT:__ Setting that immediately communicates the struggle context \(cluttered workspace, overwhelming situation, etc\.\)
- __ACTION:__ Behaviors that embody the pain point the audience experiences
- __STYLE:__ Ghibli\-style with warm but slightly muted tones to convey struggle without despair
- __COMPOSITION:__ Medium shot that shows both character emotion and environmental context

### <a id="_odl32ppg83s7"></a>__Step 4: Generate Variant Prompts \(Slides 2\-5\)__

Create FOUR variant objects with modification prompts for the complete emotional journey:

__Slide 2 \- Amplifying the Pain:__

- Intensify the struggle elements from Slide 1
- Deepen environmental markers of the problem
- Show escalated emotional state while maintaining relatability

__Slide 3 \- The Relief Peak \(STRATEGIC SEMIOTIC INJECTION\):__

- Transform environment to show the "turning point" moment
- THIS IS THE CRITICAL SCENE: Query facial\_expression\_lexicon for the most appropriate relief/hope expression
- Inject the selected expression's memetic\_reference\_prompt
- Show the character in a moment of realization, breakthrough, or newfound clarity

__Slide 4 \- Proof of Possibility:__

- Environment shifts to show evidence of the solution working
- Character displays confidence and calm competence
- Visual elements that suggest measurable progress or positive change

__Slide 5 \- Empowered Action:__

- Show character actively implementing the solution
- Environment reflects organization, clarity, and forward momentum
- Expression of determined focus and empowered action

### <a id="_gd9r6qm0ateh"></a>__Step 5: Visual Consistency Protocol__

Ensure perfect character and style consistency across all five scenes:

- Same character age and core visual identity throughout
- Consistent Ghibli art style with evolving color temperature \(muted → warm → bright\)
- Environmental elements that logically transform to support the emotional journey
- Facial expressions that authentically progress through the emotional arc

### <a id="_huf5a4widqo1"></a>__Step 6: Relief Peak Optimization__

The Slide 3 transformation must be the emotional climax:

- Maximum contrast with Slides 1\-2 in terms of lighting, environment, and character state
- Strategic semiotic injection creates the "exhale" moment of relief
- Visual metaphors for breakthrough, clarity, or hope \(sunrise, clearing sky, opened door, etc\.\)

## <a id="_uyvw7vtkj4xg"></a>__Output Requirements__

Generate a JSON object with this exact structure:

\{

  "base\_scene\_prompt": "\[Complete Ghibli\-style prompt for Slide 1 \(Shared Struggle\) including character age, relatable struggle environment, authentic stress/overwhelm expressions, and warm but muted visual tone\]",

  "variant\_prompts": \[

    \{

      "scene\_name": "Amplifying the Pain",

      "modification\_prompt": "\[Instructions to intensify the struggle elements, deepen environmental markers of the problem, and escalate emotional state while maintaining relatability\]"

    \},

    \{

      "scene\_name": "Relief Peak",

      "modification\_prompt": "\[Transform environment to breakthrough moment\. MUST include memetic\_reference\_prompt from facial\_expression\_lexicon for maximum relief/hope emotional payoff\. Show character in moment of realization or newfound clarity\]"

    \},

    \{

      "scene\_name": "Proof of Possibility", 

      "modification\_prompt": "\[Shift environment to show solution evidence\. Character displays confidence and calm competence\. Visual elements suggesting measurable progress\]"

    \},

    \{

      "scene\_name": "Empowered Action",

      "modification\_prompt": "\[Show character actively implementing solution\. Environment reflects organization and forward momentum\. Expression of determined focus and empowerment\]"

    \}

  \],

  "strategic\_notes": \{

    "selected\_archetype": "Relief Peak Carousel",

    "emotional\_journey": "\[The specific struggle\-to\-relief journey identified\]",

    "casting\_decision": "\[Character age selected and reasoning\]",

    "semiotic\_injection\_scene": "Relief Peak",

    "selected\_expression": "\[Expression ID from facial\_expression\_lexicon\]",

    "visual\_progression": "\[How the visual tone evolves from muted struggle to bright empowerment\]"

  \}

\}

## <a id="_n97o99jjbeap"></a>__Quality Standards__

- __Slide 1 must create immediate recognition:__ "That's exactly how I feel"
- __Slides 1\-2 build emotional connection__ through validated struggle without creating despair
- __Slide 3 provides genuine relief moment__ with maximum emotional contrast
- __Slides 4\-5 maintain hope__ while showing practical, attainable resolution
- __Visual progression feels complete__ from authentic problem to authentic solution
- __Character remains relatable__ throughout the transformation journey

## <a id="_qkkhvbetd3ga"></a>__Key Success Metrics__

- Audience feels deeply "seen" in Slides 1\-2
- Slide 3 creates a genuine "exhale" moment of relief
- Slides 4\-5 feel actionable and immediately implementable
- Complete carousel provides satisfying emotional resolution
- Visual narrative builds strategic trust through empathy and empowerment


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
