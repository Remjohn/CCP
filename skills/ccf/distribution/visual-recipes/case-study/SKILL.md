---
name: "Visual Recipe - Case Study"
description: "Visual generation formula for Case Study format"
session_id: ccf-visual-recipe
phase: distribution
ccp_layer: Expression (L7)
pi_extensions: [SoulResonance]
recipe_id: "case-study"
inputs:
  - config.yaml
  - scripts/final/{blueprint_id}_script.md (AUTHORIZED)
  - intelligence/soul/coach_soul.json (for brand avatar)
  - intelligence/tribe/tribe_profile.json (for H9 visual recognition codes)
outputs:
  - visuals/recipes/{blueprint_id}_case-study_visual_prompt.md
depends_on: [story-5.2]
---

# <a id="_nxl6qfu9il"></a>__🌞 Case Study Visual Recipe Protocol__


---

## 🚨 CRITICAL RULES — 4 LAWS OF VISUAL RECIPE DISTILLATION

1. **Law of the Biological Hook:** Images must trigger an autonomic response. Every visual prompt MUST explicitly dictate a "Biological Hook" (e.g., vertigo, claustrophobia, grounded warmth).
2. **Law of Sensory Zoom (Compression):** Avoid flat, wide-angle summaries. Prompts MUST enforce a specific sensory focus (e.g., "macro detail of white knuckles," "dust motes in sunbeam").
3. **Law of Mode Constraints:** Every visual scene MUST align with a specific emotional MODE (TENSION, VULNERABILITY, RECOGNITION). Generic "happy" or "sad" is insufficient.
4. **Law of Visual Authenticity:** No stock photography tropes. All references must trace to real-world ethnographic artifacts (curated by H13 asset-curator).

---

This document outlines the specific operational logic for the "Conscious Art Director" agent when executing the Case Study visual recipe\. This recipe is designed to generate compelling multi\-scene visual narratives that transform success stories into emotionally resonant, trust\-building visual sequences that inspire action through authentic storytelling\.

## <a id="_2bydn2pqm3q3"></a>__Recipe Details__

__Recipe ID:__ case\_study\_recipe  
 __Archetype Category:__ Case Study  
 __Purpose:__ To generate a 3\-4 scene visual narrative that tells compelling success stories with specific emotional triggers to build trust and inspire action through authentic transformation journeys\.

## <a id="_cvigutwnxc1s"></a>__Recipe Prompt Logic__

Your task is to generate a visual recipe for a Case Study—a multi\-scene visual narrative that transforms success stories into emotionally resonant, trust\-building sequences that inspire action through authentic storytelling\.

### <a id="_dbyinrk22t04"></a>__Step 1: Case Study Archetype Analysis__

Analyze the validated\_content to identify the specific Case Study sub\-archetype and its emotional framework:

- __The Surprising Case Study:__ Focus on the "before assumption" → "unexpected reality" revelation
- __The Inspirational Case Study:__ Emphasize the struggle → transformation → triumph journey
- __The Relatable Case Study:__ Highlight everyday problem → practical solution → tangible improvement
- __The Intriguing Case Study:__ Structure as mystery → investigation → eureka moment revelation
- __The Social Proof\-Testimonial Case Study:__ Showcase skepticism → experience → authentic results
- __The FOMO Case Study:__ Present missed opportunity → decisive action → competitive advantage

### <a id="_ve17hk773atl"></a>__Step 2: Narrative Arc Deconstruction__

Break the case study into 3\-4 key visual beats based on archetype:

__3\-Scene Structure \(Standard\):__

1. __Setup/Problem State:__ The initial challenge, struggle, or status quo
2. __Process/Journey:__ The method, struggle, or transformation process
3. __Result/Transformation:__ The successful outcome and emotional payoff

__4\-Scene Structure \(Complex/Intriguing\):__

1. __Setup/Problem State:__ Initial challenge or mystery
2. __Investigation/Process:__ The method or discovery process
3. __Breakthrough/Revelation:__ The key insight or turning point
4. __Result/Transformation:__ Final success and emotional validation

### <a id="_dq02jzlorzm0"></a>__Step 3: Strategic Character Selection and Age Mapping__

Select characters from the character\_lexicon that best represent the transformation journey:

- __Protagonist:__ The success story subject \(choose age that reflects their journey stage\)
- __Supporting Elements:__ Environmental characters that reinforce the narrative context
- __Age Progression:__ Consider showing character growth through age changes if the timeline spans significant periods

### <a id="_v8dsjk3sq5ml"></a>__Step 4: Generate Base Scene Prompt \(Setup/Problem State\)__

Create a complete, fused prompt for the initial challenge state by combining:

- __CHARACTER:__ Selected character with emotions reflecting the initial struggle/challenge state
- __ENVIRONMENT:__ Settings that embody the problem context using client's metaphors for struggle
- __ACTION:__ Behaviors demonstrating the initial problematic situation or status quo
- __STYLE:__ Ghibli\-style with visual elements emphasizing the challenge or mystery
- __EMOTIONAL TONE:__ Authentic struggle, confusion, or status quo dissatisfaction

### <a id="_yzcof99642xl"></a>__Step 5: Generate Variant Prompts \(Journey \+ Transformation\)__

Create 2\-3 variant objects with modification\_prompts:

__Variant 1: Process/Journey Scene__

- Environmental shift to show active engagement with the solution
- Character emotions showing determination, focus, or discovery
- Actions demonstrating the method or process being implemented

__Variant 2: \[Optional\] Breakthrough/Revelation Scene__ \(for 4\-scene structure\)

- Environmental transformation to moment of insight
- Character emotions showing realization or eureka moment
- Actions capturing the pivotal breakthrough moment

__Variant 3: Result/Transformation Scene__ \(STRATEGIC SEMIOTIC INJECTION\)

- Complete environmental transformation to success state
- Character emotions showing fulfillment, confidence, or achievement
- Actions demonstrating the successful outcome or new capability

### <a id="_h0koboaw818l"></a>__Step 6: Strategic Semiotic Injection__

For the FINAL transformation scene ONLY:

- Analyze the facial\_expression\_lexicon to find the most appropriate expression for the specific case study emotional trigger
- __Surprising:__ Use expressions conveying "mind\-blown" or revelation
- __Inspirational:__ Use expressions of triumph and overcoming
- __Relatable:__ Use expressions of satisfied accomplishment
- __Intriguing:__ Use expressions of "eureka" or discovery satisfaction
- __Social Proof:__ Use expressions of authentic confidence and results
- __FOMO:__ Use expressions of competitive satisfaction or advantage

Inject the selected expression's memetic\_reference\_prompt into the final scene's modification\_prompt for maximum emotional impact\.

### <a id="_v03qnj4pik90"></a>__Step 7: Credibility and Authenticity Integration__

Ensure all scenes incorporate elements that build trust:

- Realistic, relatable challenges in the setup
- Genuine process documentation in journey scenes
- Tangible, believable results in transformation scenes
- Environmental details that support the authenticity of the story

## <a id="_uu9pvdqlu9al"></a>__Output Requirements__

Generate a JSON object with this exact structure:

\{

  "base\_scene\_prompt": "\[Complete Ghibli\-style prompt for Setup/Problem scene including character selection, authentic struggle emotions, challenge environment, and literal facial expression\]",

  "variant\_prompts": \[

    \{

      "scene\_name": "Process/Journey",

      "modification\_prompt": "\[Instructions to transform to active solution engagement\. Show character determination and method implementation\.\]"

    \},

    \{

      "scene\_name": "\[Optional: Breakthrough/Revelation\]",

      "modification\_prompt": "\[Instructions for pivotal insight moment\. Show environmental shift to discovery and character realization\.\]"

    \},

    \{

      "scene\_name": "Result/Transformation", 

      "modification\_prompt": "\[Instructions to transform to success state\. MUST include memetic\_reference\_prompt from facial\_expression\_lexicon for maximum emotional payoff matching the case study archetype\.\]"

    \}

  \],

  "strategic\_notes": \{

    "selected\_archetype": "Case Study",

    "case\_study\_subtype": "\[Specific sub\-archetype identified\]",

    "casting\_decision": "\[Character selection and reasoning\]",

    "scene\_structure": "\[3\-scene or 4\-scene structure used\]",

    "semiotic\_injection\_scene": "Result/Transformation",

    "selected\_expression": "\[Expression ID from facial\_expression\_lexicon\]",

    "credibility\_elements": "\[Specific authenticity factors incorporated\]"

  \}

\}

## <a id="_v63xy9j1awte"></a>__Quality Standards__

- The transformation should feel authentic and achievable, not exaggerated
- Each scene should build logical progression toward the successful outcome
- The emotional arc should match the specific case study archetype's trigger
- Visual elements should support credibility and trust\-building throughout
- The final transformation should inspire action while maintaining believability
- Character consistency must be maintained across all scenes while showing growth/change
- Environmental progression should reinforce the narrative of positive transformation


---

## Brand Avatar Injection (CCF Addition)

Before generating image prompts, inject the brand avatar's physical DNA:
- Load from coach_soul.json: physical_description, styling_preferences, recurring_visual_motifs
- EVERY visual prompt that includes a person must use the brand avatar's physical DNA
- This ensures visual consistency across all content pieces

## I-R-E-V-C Session Protocol

### INGEST
- Load AUTHORIZED script
- Load coach_soul.json for brand avatar physical DNA
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
