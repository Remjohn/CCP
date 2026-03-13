---
name: "Visual Recipe - Storytelling Archetypes"
description: "Visual generation formula for Storytelling Archetypes format"
session_id: ccf-visual-recipe
phase: distribution
ccp_layer: Expression (L7)
pi_extensions: [SoulResonance]
recipe_id: "storytelling-archetypes"
inputs:
  - config.yaml
  - scripts/final/{blueprint_id}_script.md (AUTHORIZED)
  - intelligence/soul/coach_soul.json (for brand avatar)
  - intelligence/tribe/tribe_profile.json (for H9 visual recognition codes)
outputs:
  - visuals/recipes/{blueprint_id}_storytelling-archetypes_visual_prompt.md
depends_on: [story-5.2]
---

# <a id="_ij095ndd4w2b"></a>__🌞 Storytelling Archetypes Visual Recipe Protocol__


---

## 🚨 CRITICAL RULES — 4 LAWS OF VISUAL RECIPE DISTILLATION

1. **Law of the Biological Hook:** Images must trigger an autonomic response. Every visual prompt MUST explicitly dictate a "Biological Hook" (e.g., vertigo, claustrophobia, grounded warmth).
2. **Law of Sensory Zoom (Compression):** Avoid flat, wide-angle summaries. Prompts MUST enforce a specific sensory focus (e.g., "macro detail of white knuckles," "dust motes in sunbeam").
3. **Law of Mode Constraints:** Every visual scene MUST align with a specific emotional MODE (TENSION, VULNERABILITY, RECOGNITION). Generic "happy" or "sad" is insufficient.
4. **Law of Visual Authenticity:** No stock photography tropes. All references must trace to real-world ethnographic artifacts (curated by H13 asset-curator).

---

This document outlines the specific operational logic for the "Conscious Art Director" agent when executing the Storytelling Archetypes visual recipe\. This recipe is designed to generate emotionally resonant multi\-scene visual narratives that leverage the 16 core emotional triggers through strategic narrative progression\.

## <a id="_dzcprh9cforq"></a>__Recipe Details__

__Recipe ID:__ storytelling\_archetypes\_recipe  
 __Archetype Category:__ Storytelling Archetypes  
 __Purpose:__ To generate a 3\-5 scene visual narrative that creates powerful emotional resonance through classic story structure, culminating in a strategic semiotic injection at the climax moment\.

## <a id="_8tuurcml2cxi"></a>__Recipe Prompt Logic__

Your task is to generate a visual recipe for a Storytelling Archetype—a multi\-scene visual narrative that leverages one of the 16 core emotional triggers through strategic narrative progression and character evolution\.

### <a id="_n1zml7fe56wz"></a>__Step 1: Emotional Archetype Analysis__

Analyze the validated\_content to identify which of the 16 Storytelling Archetypes it represents:

__Transformation Cluster:__

- The Achievement Story \(triumph over obstacles\)
- The Transformation Story \(personal evolution\)
- The Discovery Story \(revelation/learning\)
- The Empowerment Story \(gaining strength/confidence\)

__Connection Cluster:__

- The Connection Story \(relationships/bonding\)
- The Romance Story \(love/attraction\)
- The Recognition Story \(validation/acknowledgment\)
- The Joy Story \(pure happiness/celebration\)

__Anticipation Cluster:__

- The Anticipation Story \(building excitement\)
- The Curiosity Story \(mystery/investigation\)
- The Surprise Story \(unexpected twists\)
- The Relief Story \(tension release\)

__Emotional Resonance Cluster:__

- The Inspiration Story \(motivation/aspiration\)
- The Nostalgia Story \(bittersweet memories\)
- The Longing Story \(desire/yearning\)
- The Cuteness Story \(warmth/affection\)

### <a id="_41mjfxyhb43h"></a>__Step 2: Narrative Structure Determination__

Based on the identified archetype, determine the optimal scene count and structure:

__3\-Scene Structure__ \(Setup → Challenge/Development → Climax/Resolution\):

- Achievement, Transformation, Discovery, Empowerment
- Connection, Romance, Recognition, Joy
- Relief, Surprise

__4\-Scene Structure__ \(Setup → Rising Action → Climax → Resolution\):

- Anticipation, Curiosity, Inspiration
- Nostalgia, Longing

__5\-Scene Structure__ \(Setup → Rising Action → Midpoint → Climax → Resolution\):

- Complex Cuteness stories with multiple emotional beats

### <a id="_27j78mfdddjh"></a>__Step 3: Character Casting and Age Selection__

Select character and age from character\_lexicon based on archetype requirements:

- __Achievement/Empowerment Stories:__ Current age or aspirational age
- __Transformation/Discovery Stories:__ Use age progression \(younger → current\)
- __Connection/Romance/Recognition Stories:__ Age appropriate to relationship dynamic
- __Nostalgia/Longing Stories:__ Mixed ages or younger self focus
- __Joy/Surprise/Cuteness Stories:__ Age that maximizes emotional authenticity

### <a id="_61w1svjkb94o"></a>__Step 4: Generate Base Scene Prompt \(Setup\)__

Create a complete, fused prompt for the opening scene that establishes:

__CHARACTER FOUNDATION:__

- Selected character age and baseline emotional state
- Physical positioning that suggests the journey ahead
- Facial expression that reflects the pre\-transformation state

__ENVIRONMENTAL CONTEXT:__

- Setting that embodies the story's initial conditions
- Visual metaphors aligned with conscious\_soul\_values
- Atmospheric elements that hint at the emotional journey

__VISUAL STYLE:__

- Ghibli\-style for transformation/inspiration narratives
- Mixed Ghibli\-photorealism for relatable connection stories
- Cinematic realism for high\-stakes achievement stories

### <a id="_j9xtmgt06yau"></a>__Step 5: Generate Variant Prompts \(Narrative Progression\)__

Create an array of modification prompts for each subsequent scene:

__For 3\-Scene Structure:__

- Variant 1: Challenge/Development \(literal emotional expressions\)
- Variant 2: Climax/Resolution \(STRATEGIC SEMIOTIC INJECTION\)

__For 4\-Scene Structure:__

- Variant 1: Rising Action \(literal expressions\)
- Variant 2: Climax \(STRATEGIC SEMIOTIC INJECTION\)
- Variant 3: Resolution \(literal expressions showing aftermath\)

__For 5\-Scene Structure:__

- Variant 1: Rising Action \(literal expressions\)
- Variant 2: Midpoint \(literal expressions\)
- Variant 3: Climax \(STRATEGIC SEMIOTIC INJECTION\)
- Variant 4: Resolution \(literal expressions\)

### <a id="_n7ghy4uk1dgn"></a>__Step 6: Strategic Semiotic Injection__

Identify the single most emotionally powerful moment in the narrative arc \(typically the Climax scene\):

1. __Analyze__ the facial\_expression\_lexicon to find the expression that best amplifies the specific emotional archetype
2. __Select__ the expression that creates maximum resonance with the story's emotional peak
3. __Inject__ the selected expression's memetic\_reference\_prompt into that scene's modification\_prompt ONLY
4. __Ensure__ all other scenes use literal facial expression descriptions

### <a id="_uj8tf428mh8i"></a>__Step 7: Emotional Continuity Verification__

Ensure the narrative progression creates authentic emotional escalation:

- Each scene should build emotional intensity toward the climax
- The strategic injection should feel like the natural emotional peak
- The resolution should provide satisfying emotional closure
- Character consistency must be maintained throughout all transformations

## <a id="_76nwdjq5ldqt"></a>__Output Requirements__

Generate a JSON object with this exact structure:

\{

  "base\_scene\_prompt": "\[Complete Ghibli\-style prompt for Setup scene including character selection, baseline emotional state, environmental context, and literal facial expression\]",

  "variant\_prompts": \[

    \{

      "scene\_name": "\[Descriptive name for Rising Action/Challenge scene\]",

      "modification\_prompt": "\[Instructions to evolve environment and character state with literal emotional descriptions\]"

    \},

    \{

      "scene\_name": "\[Descriptive name for Climax scene\]",

      "modification\_prompt": "\[Environmental and emotional transformation instructions\. MUST include memetic\_reference\_prompt from facial\_expression\_lexicon for maximum emotional impact\]"

    \},

    \{

      "scene\_name": "\[Descriptive name for Resolution scene \- only for 4\-5 scene structures\]",

      "modification\_prompt": "\[Instructions showing aftermath/completion with literal emotional descriptions\]"

    \}

  \],

  "strategic\_notes": \{

    "selected\_archetype": "\[Specific storytelling archetype from the 16 types\]",

    "narrative\_structure": "\[3\-scene, 4\-scene, or 5\-scene with justification\]",

    "casting\_decision": "\[Character and age selection reasoning\]",

    "semiotic\_injection\_scene": "\[Which scene received the strategic emotional injection\]",

    "selected\_expression": "\[Expression ID from facial\_expression\_lexicon\]",

    "emotional\_journey": "\[Brief description of the emotional progression\]",

    "visual\_style\_rationale": "\[Why this style was chosen for this story type\]"

  \}

\}

## <a id="_oga3hbumx6ng"></a>__Quality Standards__

- __Emotional Authenticity:__ Each scene must feel genuinely connected to the specific storytelling archetype
- __Progressive Intensity:__ Emotional stakes should escalate naturally toward the climax
- __Cultural Resonance:__ Visual elements should speak to the target tribe's values and experiences
- __Character Consistency:__ Perfect visual continuity across all scene transformations
- __Strategic Impact:__ The semiotic injection should create the maximum emotional payoff at the perfect moment
- __Viral Optimization:__ Each scene should be individually compelling while serving the greater narrative arc

## <a id="_hqacl437sxez"></a>__Archetype\-Specific Guidance__

__Achievement Stories:__ Focus on obstacle progression and triumph moments __Transformation Stories:__ Emphasize visible character evolution and growth __Connection Stories:__ Highlight relationship dynamics and emotional bonding __Anticipation Stories:__ Build suspense through environmental and character tension __Nostalgia Stories:__ Use age regression and memory\-evoking environments __Surprise Stories:__ Create visual misdirection leading to revelation moments


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
