---
name: "Visual Recipe - Debunking Myths & Scams"
description: "Visual generation formula for Debunking Myths & Scams format"
session_id: ccf-visual-recipe
phase: distribution
recipe_id: "debunking-myths-scams"
inputs:
  - config.yaml
  - scripts/final/{blueprint_id}_script.md (AUTHORIZED)
  - intelligence/soul/soul_values.json (for brand avatar)
  - intelligence/tribe/tribe_profile.json (for H9 visual recognition codes)
outputs:
  - visuals/recipes/{blueprint_id}_debunking-myths-scams_visual_prompt.md
depends_on: [story-5.2]
---

# <a id="_28mx20b0jeq"></a>__🌞 Debunking Myths & Scams Visual Recipe Protocol__


---

## 🚨 CRITICAL RULES — 4 LAWS OF VISUAL RECIPE DISTILLATION

1. **Law of the Biological Hook:** Images must trigger an autonomic response. Every visual prompt MUST explicitly dictate a "Biological Hook" (e.g., vertigo, claustrophobia, grounded warmth).
2. **Law of Sensory Zoom (Compression):** Avoid flat, wide-angle summaries. Prompts MUST enforce a specific sensory focus (e.g., "macro detail of white knuckles," "dust motes in sunbeam").
3. **Law of Mode Constraints:** Every visual scene MUST align with a specific emotional MODE (TENSION, VULNERABILITY, RECOGNITION). Generic "happy" or "sad" is insufficient.
4. **Law of Visual Authenticity:** No stock photography tropes. All references must trace to real-world ethnographic artifacts (curated by H13 asset-curator).

---

This document outlines the specific operational logic for the "Conscious Art Director" agent when executing the Debunking Myths & Scams visual recipe\. This recipe is designed to transform myth\-busting content into powerful visual narratives that expose deception, empower audiences, and create authentic resonance through strategic emotional triggers\.

## <a id="_kxe3ou4psbgi"></a>__Recipe Details__

- __Recipe ID__: debunking\_myths\_scams\_recipe
- __Archetype Category__: Debunking Myths & Scams
- __Purpose__: To generate a multi\-scene visual narrative that transforms abstract misinformation into concrete, emotionally compelling exposés that empower audiences with truth and critical thinking tools\.

## <a id="_gn54enx2t2q"></a>__Recipe Prompt Logic__

Your task is to generate a visual recipe for a Debunking Myths & Scams narrative—a strategic 3\-scene visual sequence that systematically dismantles misinformation while empowering the audience through emotional revelation and factual clarity\.

### <a id="_w4n7p26d4yuo"></a>__Step 1: Myth Vulnerability Analysis__

Analyze the validated\_content to identify the core deception and its emotional manipulation strategy\. Determine which of the six emotional angles is being deployed:

- __Curiosity/Intrigue__: Detective\-style investigation into hidden truths
- __Indignation__: Righteous anger at injustice and deception
- __Fear\-Anxiety__: Exposure of hidden dangers and threats
- __Disgusting__: Moral revulsion at repugnant scams
- __Empowering__: Tools and knowledge for taking back control
- __Schadenfreude__: Satisfaction in seeing deceivers face consequences

### <a id="_ln6fw3e65cqs"></a>__Step 2: Strategic Character Casting__

Select character from character\_lexicon based on credibility requirements:

- __Expert Authority__: For technical debunking requiring credible expertise
- __Relatable Investigator__: For curiosity\-driven myth exploration
- __Righteous Defender__: For indignation\-based content protecting the vulnerable
- __Concerned Guide__: For fear\-based protective warnings

### <a id="_uc3a1pm4d2hb"></a>__Step 3: Three\-Scene Narrative Structure__

Generate exactly __3 scenes__ following this proven debunking sequence:

#### <a id="_v9la4k3zu65d"></a>__Scene 1 \- BASE SCENE: "The Lie in Action"__

- __Purpose__: Establish the myth/scam as it appears to victims
- __Emotional State__: Show the character observing or encountering the deceptive information
- __Environment__: Setting where the myth typically spreads \(social media, sales presentations, etc\.\)
- __Expression__: Literal description of skepticism, concern, or initial investigation

#### <a id="_7v836ip86lel"></a>__Scene 2 \- VARIANT 1: "The Investigation/Evidence"__

- __Purpose__: Show the character uncovering the truth
- __Environmental Transformation__: Shift to research/investigation setting
- __Action__: Character analyzing evidence, consulting sources, revealing facts
- __Expression__: Literal description of focused determination or growing understanding

#### <a id="_3tf04ntlzne1"></a>__Scene 3 \- VARIANT 2: "The Revelation/Empowerment"__

- __Purpose__: The emotional payoff where truth is revealed and audience is empowered
- __Strategic Semiotic Injection__: CRITICAL \- This scene MUST receive the strategic emotional expression from facial\_expression\_lexicon
- __Environmental Transformation__: Setting that represents clarity, truth, or justice
- __Expression__: Inject memetic\_reference\_prompt for maximum emotional impact

### <a id="_jn56jq2vzwp"></a>__Step 4: Emotional Angle Integration__

Ensure each scene authentically reflects the identified emotional angle:

- __Curiosity/Intrigue__: Progress from mystery → investigation → revelation
- __Indignation__: Build from injustice → evidence gathering → righteous triumph
- __Fear\-Anxiety__: Move from threat exposure → protective analysis → empowered vigilance
- __Disgusting__: Escalate from repugnant discovery → thorough exposure → moral vindication
- __Empowering__: Develop from problem identification → tool gathering → confident mastery
- __Schadenfreude__: Advance from deception exposure → consequence documentation → justice satisfaction

### <a id="_tfsmusm3n85i"></a>__Step 5: Truth Amplification Strategy__

Incorporate visual elements that amplify the debunking message:

- __Contrast Emphasis__: Visual opposition between lie and truth
- __Evidence Integration__: Charts, documents, or proof elements in investigation scene
- __Empowerment Symbols__: Tools, knowledge, or strength symbols in final scene
- __Cultural Resonance__: Tribe\-specific visual language for credibility

## <a id="_jbtcjg9jxtwa"></a>__Output Requirements__

Generate a JSON object with this exact structure:

\{

  "base\_scene\_prompt": "\[Complete Ghibli\-style or cinematic prompt for Scene 1 \(The Lie in Action\) including character selection, myth presentation environment, literal facial expression of skepticism/concern, and atmospheric elements suggesting deception\]",

  "variant\_prompts": \[

    \{

      "scene\_name": "The Investigation",

      "modification\_prompt": "\[Instructions to transform environment to investigation/research setting, character action to evidence analysis, literal expression of focused determination\]"

    \},

    \{

      "scene\_name": "The Revelation",

      "modification\_prompt": "\[Instructions to transform environment to truth/clarity setting, character action to empowered revelation\. MUST include memetic\_reference\_prompt from facial\_expression\_lexicon for maximum emotional payoff matching the identified emotional angle\]"

    \}

  \],

  "strategic\_notes": \{

    "selected\_archetype": "Debunking Myths & Scams",

    "emotional\_angle": "\[Specific angle: Curiosity/Indignation/Fear/Disgusting/Empowering/Schadenfreude\]",

    "myth\_identified": "\[The specific myth or scam being debunked\]",

    "casting\_decision": "\[Character choice and credibility reasoning\]",

    "semiotic\_injection\_scene": "The Revelation",

    "selected\_expression": "\[Expression ID from facial\_expression\_lexicon\]",

    "truth\_amplification\_strategy": "\[Specific visual elements used to enhance debunking impact\]"

  \}

\}

## <a id="_gziyz9q8lc25"></a>__Quality Standards__

- __Credibility First__: Visual elements must enhance rather than undermine the factual message
- __Emotional Precision__: The final scene's emotional injection must perfectly match the identified angle
- __Empowerment Focus__: All three scenes should build toward audience empowerment, not just destruction of the myth
- __Tribal Alignment__: Visual language should speak to the specific audience being protected from the misinformation
- __Evidence Integration__: Investigation scene should visually represent the research/fact\-checking process
- __Justice Satisfaction__: Final scene should provide emotional closure and sense of truth prevailing

## <a id="_nhw0etqh5m1g"></a>__Special Considerations__

- __Avoid Amplifying the Myth__: Base scene should present the lie without inadvertently promoting it
- __Maintain Ethical Standards__: Debunking should be factual and educational, not character assassination
- __Cultural Sensitivity__: Consider how different tribes process authority and evidence
- __Shareability Balance__: Content should be viral but not sensationalized beyond factual accuracy


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
