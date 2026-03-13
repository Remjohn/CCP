---
name: "Visual Recipe - Dopamine Cliff Carousel"
description: "Visual generation formula for Dopamine Cliff Carousel format"
session_id: ccf-visual-recipe
phase: distribution
recipe_id: "dopamine-cliff-carousel"
inputs:
  - config.yaml
  - scripts/final/{blueprint_id}_script.md (AUTHORIZED)
  - intelligence/soul/soul_values.json (for brand avatar)
  - intelligence/tribe/tribe_profile.json (for H9 visual recognition codes)
outputs:
  - visuals/recipes/{blueprint_id}_dopamine-cliff-carousel_visual_prompt.md
depends_on: [story-5.2]
---

# <a id="_b1aco834dc8"></a>__🌞 Dopamine Cliff Carousel Visual Recipe Protocol__


---

## 🚨 CRITICAL RULES — 4 LAWS OF VISUAL RECIPE DISTILLATION

1. **Law of the Biological Hook:** Images must trigger an autonomic response. Every visual prompt MUST explicitly dictate a "Biological Hook" (e.g., vertigo, claustrophobia, grounded warmth).
2. **Law of Sensory Zoom (Compression):** Avoid flat, wide-angle summaries. Prompts MUST enforce a specific sensory focus (e.g., "macro detail of white knuckles," "dust motes in sunbeam").
3. **Law of Mode Constraints:** Every visual scene MUST align with a specific emotional MODE (TENSION, VULNERABILITY, RECOGNITION). Generic "happy" or "sad" is insufficient.
4. **Law of Visual Authenticity:** No stock photography tropes. All references must trace to real-world ethnographic artifacts (curated by H13 asset-curator).

---

This document outlines the specific operational logic for the "Conscious Art Director" agent when executing the Dopamine Cliff Carousel visual recipe\. This recipe is designed to generate a powerful five\-part visual narrative that creates an emotional journey from aspiration to reality check to empowerment, optimized for maximum engagement and viral potential\.

## <a id="_vupi8ax5blue"></a>__Recipe Details__

__Recipe ID:__ dopamine\_cliff\_carousel\_recipe  
 __Archetype Category:__ Dopamine Cliff Carousel  
 __Purpose:__ To generate a five\-part visual carousel that hooks viewers with aspirational imagery, delivers a strategic reality check, and provides actionable solutions through emotional contrast and pattern interruption\.

## <a id="_dvy8unhjct63"></a>__Recipe Prompt Logic__

Your task is to generate a visual recipe for a Dopamine Cliff Carousel—a five\-part visual narrative that creates a powerful emotional journey from fantasy to reality to empowerment, designed for maximum scroll\-stopping impact and social currency\.

### <a id="_drad7dad85b"></a>__Step 1: Aspirational Hook Analysis__

Analyze the validated\_content to identify the core fantasy or aspiration being explored\. Extract from the script:

- __The Peak Fantasy:__ What is the ultimate dream state being presented in slides 1\-2?
- __Visual Pleasure Points:__ What specific imagery will create maximum dopamine response?
- __Tribal Desires:__ What does this audience secretly crave or envy?

### <a id="_jj6xc8b0smif"></a>__Step 2: Reality Cliff Identification__

Identify the strategic "cliff moment" from the script:

- __The Pattern Interrupt:__ What shocking truth shatters the fantasy?
- __The Hidden Cost:__ What consequence or reality check creates cognitive dissonance?
- __The Wake\-Up Call:__ What statistic or insight creates the emotional pivot?

### <a id="_bpxtpzxtcam7"></a>__Step 3: Solution Architecture__

Extract the empowerment elements:

- __The Path Forward:__ What actionable steps resolve the tension?
- __Do vs\. Don't Framework:__ What specific behaviors create success vs\. failure?

### <a id="_n1zafj3w41ii"></a>__Step 4: Generate Base Scene Prompt \(Slide 1 \- The Aspirational Hook\)__

Create a complete, fused prompt for the opening hook combining:

- __CHARACTER:__ Selected from character\_lexicon showing peak aspiration/success
- __ENVIRONMENT:__ Luxurious, aspirational setting that embodies the fantasy
- __VISUAL STYLE:__ High\-end, polished aesthetic \(cinematic realism or premium ghibli\)
- __EMOTIONAL STATE:__ Pure joy, confidence, or achievement \(literal expression\)
- __COMPOSITION:__ 4\-grid layout of complementary aspirational elements

### <a id="_t8l5sqea9qlw"></a>__Step 5: Generate Variant Prompts \(Slides 2\-5\)__

Create exactly __4 variant objects__ with specific scene progression:

__Variant 1 \(Slide 2 \- Deepening Desire\):__

- Amplify the aspirational elements from the base scene
- Maintain same character and style but intensify the luxury/success markers
- Keep emotional state positive but add subtle hints of the "too good to be true" feeling

__Variant 2 \(Slide 3 \- The Dopamine Cliff\):__

- __CRITICAL:__ This is your Strategic Semiotic Injection point
- Complete environmental transformation to stark, reality\-based setting
- Character expression must shift to shock, realization, or disappointment
- __MUST include:__ Selected memetic\_reference\_prompt from facial\_expression\_lexicon
- Visual style shifts to more documentary/realistic to emphasize contrast

__Variant 3 \(Slide 4 \- Sobering Reality\):__

- Minimal, clean environment focusing on data/statistics
- Character in contemplative, processing state
- Visual style emphasizes clarity and truth\-telling

__Variant 4 \(Slide 5 \- The Path Forward\):__

- Split\-screen or comparison layout showing wrong vs\. right approach
- Character in empowered, determined state showing the solution
- Return to hopeful but grounded visual style

### <a id="_be7hfjsjjkz9"></a>__Step 6: Strategic Semiotic Injection__

For Variant 2 \(The Cliff\) ONLY:

- Analyze the facial\_expression\_lexicon to find the most appropriate expression for the reality check moment
- Select expressions that convey shock, realization, disappointment, or "wake\-up call" emotions
- Inject the selected expression's memetic\_reference\_prompt into the modification\_prompt
- This creates maximum emotional impact at the crucial pattern interrupt moment

### <a id="_xvgpb36ecvf3"></a>__Step 7: Character Consistency Strategy__

Ensure the same character appears across all 5 scenes but with appropriate emotional evolution:

- __Slides 1\-2:__ Aspirational, confident, successful
- __Slide 3:__ Shocked, disillusioned, processing reality
- __Slide 4:__ Contemplative, learning, absorbing truth
- __Slide 5:__ Empowered, wise, taking action

## <a id="_x6onqfu4iqfj"></a>__Output Requirements__

Generate a JSON object with this exact structure:

\{

  "base\_scene\_prompt": "\[Complete prompt for Slide 1 \(Aspirational Hook\) including character selection, 4\-grid aspirational composition, cinematic/premium style, and literal confident expression\]",

  "variant\_prompts": \[

    \{

      "scene\_name": "Deepening Desire",

      "modification\_prompt": "\[Instructions to amplify aspirational elements while maintaining same character and adding subtle tension hints\]"

    \},

    \{

      "scene\_name": "The Dopamine Cliff",

      "modification\_prompt": "\[Complete environmental and emotional transformation\. MUST include memetic\_reference\_prompt from facial\_expression\_lexicon for reality check shock\]"

    \},

    \{

      "scene\_name": "Sobering Reality", 

      "modification\_prompt": "\[Transform to minimal, data\-focused environment with character in contemplative processing state\]"

    \},

    \{

      "scene\_name": "The Path Forward",

      "modification\_prompt": "\[Create split\-screen comparison layout with character in empowered, solution\-oriented state\]"

    \}

  \],

  "strategic\_notes": \{

    "selected\_archetype": "Dopamine Cliff Carousel",

    "aspirational\_hook": "\[The core fantasy identified\]",

    "cliff\_moment": "\[The specific reality check/pattern interrupt\]",

    "casting\_decision": "\[Character choice and reasoning\]",

    "semiotic\_injection\_scene": "The Dopamine Cliff",

    "selected\_expression": "\[Expression ID from facial\_expression\_lexicon\]",

    "visual\_journey": "\[Description of the emotional arc across all 5 scenes\]"

  \}

\}

## <a id="_gs3zvyzf7nzj"></a>__Quality Standards__

- __Immediate Hook:__ Slide 1 must create instant aspiration and desire
- __Emotional Whiplash:__ The contrast between Slides 2 and 3 must be jarring and scroll\-stopping
- __Pattern Interrupt Power:__ Slide 3 must genuinely surprise and challenge assumptions
- __Solution Value:__ Slides 4\-5 must provide real, actionable value that justifies the emotional journey
- __Character Consistency:__ Same character with believable emotional evolution across all scenes
- __Tribal Resonance:__ Every slide must speak directly to the target audience's specific desires and fears
- __Social Currency:__ The complete carousel must feel valuable enough to save and share

## <a id="_20m1tvak75ls"></a>__Key Instructions__

- The base\_scene\_prompt must establish a luxurious, aspirational foundation
- Exactly 4 variants are required \(total 5 scenes\)
- Only Slide 3 \(The Dopamine Cliff\) receives strategic semiotic injection
- Maintain perfect character consistency while showing emotional evolution
- Each scene must build toward the next for maximum narrative impact
- Optimize for scroll\-stopping power and viral shareability


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
