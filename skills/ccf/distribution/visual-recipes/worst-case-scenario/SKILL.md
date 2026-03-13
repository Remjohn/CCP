---
name: "Visual Recipe - Worst Case Scenario"
description: "Visual generation formula for Worst Case Scenario format"
session_id: ccf-visual-recipe
phase: distribution
recipe_id: "worst-case-scenario"
inputs:
  - config.yaml
  - scripts/final/{blueprint_id}_script.md (AUTHORIZED)
  - intelligence/soul/soul_values.json (for brand avatar)
  - intelligence/tribe/tribe_profile.json (for H9 visual recognition codes)
outputs:
  - visuals/recipes/{blueprint_id}_worst-case-scenario_visual_prompt.md
depends_on: [story-5.2]
---

# <a id="_wpd82sizxwp0"></a>__🌞 Worst Case Scenario Visual Recipe Protocol__


---

## 🚨 CRITICAL RULES — 4 LAWS OF VISUAL RECIPE DISTILLATION

1. **Law of the Biological Hook:** Images must trigger an autonomic response. Every visual prompt MUST explicitly dictate a "Biological Hook" (e.g., vertigo, claustrophobia, grounded warmth).
2. **Law of Sensory Zoom (Compression):** Avoid flat, wide-angle summaries. Prompts MUST enforce a specific sensory focus (e.g., "macro detail of white knuckles," "dust motes in sunbeam").
3. **Law of Mode Constraints:** Every visual scene MUST align with a specific emotional MODE (TENSION, VULNERABILITY, RECOGNITION). Generic "happy" or "sad" is insufficient.
4. **Law of Visual Authenticity:** No stock photography tropes. All references must trace to real-world ethnographic artifacts (curated by H13 asset-curator).

---

This document outlines the specific operational logic for the "Conscious Art Director" agent when executing the Worst Case Scenario visual recipe\. This recipe is designed to generate a single, powerfully haunting image that captures the audience's deepest fears through the client's authentic worldview and emotional vocabulary\.

## <a id="_xhtk1fiefwiy"></a>__Recipe Details__

__Recipe ID:__ worst\_case\_scenario\_recipe  
 __Archetype Category:__ Worst Case Scenario  
 __Purpose:__ To generate a single, emotionally charged visual that represents a core fear or "worst\-case scenario" moment, creating profound emotional resonance and validation for the audience's deepest concerns\.

## <a id="_eaudyrlb5rky"></a>__Recipe Prompt Logic__

Your task is to generate a visual recipe for a Worst Case Scenario—a single, powerfully haunting image that captures the most visceral moment of fear or crisis, filtered through the client's unique consciousness and their audience's specific anxieties\.

### <a id="_1k45p0ilgwi4"></a>__Step 1: Soul\-Aligned Fear Identification__

Analyze the validated\_content through the lens of conscious\_soul\_values to identify the single most visceral fear that would resonate with this specific audience\. Look for fears that align with the client's:

- "Internal temperature" around failure, scams, debt, or other specific anxieties
- Core values being threatened or compromised
- Unique metaphorical language for describing crisis \(e\.g\., "leaky bucket," "house of cards," "fortress under siege"\)
- Philosophical worldview about what constitutes genuine rock bottom

### <a id="_bxoauf10ajzn"></a>__Step 2: Strategic Character Age Assignment__

Select the most authentic age from the character\_lexicon that creates maximum emotional connection:

- __Current Age:__ Present\-day crises reflecting the client's current concerns
- __Before State Age:__ Past versions embodying the client's fears about regression
- __Younger Self Age:__ Foundational fears that shaped the client's philosophy
- Choose the age that would make someone with the client's values think "That's exactly what I'm terrified of"

### <a id="_5zwum3jld7ik"></a>__Step 3: Generate Base Scene Prompt \(The Worst Case Moment\)__

Create a complete, soul\-filtered Ghibli\-style prompt combining:

__CHARACTER:__ Selected age \+ emotions that reflect the client's "internal temperature" about this specific crisis

- Vulnerability that feels authentic to their worldview \(not generic fear\)
- Expressions resonating with someone who shares their core values
- Body language showing how THIS audience experiences being "trapped" or "overwhelmed"

__ENVIRONMENT:__ Oppressive atmospheres incorporating:

- The client's unique metaphors for crisis and struggle
- Environmental symbols resonating with their audience's specific fears
- Settings that reflect their version of "foundation cracking" or "fortress under siege"

__ACTION:__ Peak vulnerability moments that:

- Capture how someone with the client's values would experience this crisis
- Show the specific emotional vocabulary the client uses to describe rock bottom
- Reflect the type of overwhelm this particular audience fears most

### <a id="_xlktq4yl3xa1"></a>__Step 4: Strategic Semiotic Injection__

For this single image ONLY:

- Analyze the facial\_expression\_lexicon to find the most appropriate expression for maximum emotional impact
- Select an expression that captures authentic despair, overwhelm, or vulnerability specific to this client's worldview
- Inject the selected expression's memetic\_reference\_prompt into the base\_scene\_prompt
- This creates immediate recognition and emotional validation for the audience

### <a id="_syh82rwo8005"></a>__Step 5: Audience\-Specific Fear Amplification__

Ensure the visual captures not just generic fear, but the specific type of worst\-case scenario that would make THIS client's audience stop scrolling and experience profound recognition of their deepest concerns\.

### <a id="_l1a6x9njfa7q"></a>__Step 6: Generate Empty Variant Array__

__CRITICAL:__ Worst Case Scenario is a single\-frame archetype\. The variant\_prompts array MUST be empty \[\] to indicate no additional scenes are needed\.

## <a id="_eo9852c8f22j"></a>__Output Requirements__

Generate a JSON object with this exact structure:

\{

  "base\_scene\_prompt": "\[Complete Ghibli\-style prompt capturing the worst\-case moment with selected character age, soul\-authentic emotions reflecting client's internal temperature, client's crisis metaphors, oppressive environment, peak vulnerability action, and memetic\_reference\_prompt from facial\_expression\_lexicon for maximum emotional impact\]",

  "variant\_prompts": \[\],

  "strategic\_notes": \{

    "selected\_archetype": "Worst Case Scenario",

    "fear\_identified": "\[The specific core fear or crisis identified\]",

    "casting\_decision": "\[Character age selected and reasoning\]",

    "semiotic\_injection\_scene": "Base Scene Only",

    "selected\_expression": "\[Expression ID from facial\_expression\_lexicon\]",

    "soul\_authenticity\_check": "\[Confirmation this represents rock bottom for someone with client's values\]"

  \}

\}

## <a id="_uqzzkdo08z2k"></a>__Quality Standards__

- The image should create immediate recognition for someone with the client's exact fears and values
- The crisis should feel authentically aligned with the client's worldview and emotional vocabulary
- The vulnerability should be specific to this audience's version of worst\-case scenario
- The visual should validate the audience's deepest concerns rather than creating generic fear
- The single image must carry the full emotional weight of the narrative without needing additional frames

## <a id="_wovtcx7e8hwj"></a>__Soul Authenticity Check__

Before finalizing, ensure this image would feel like a genuine representation of rock bottom to someone who shares the client's core values and worldview—not generic fear, but THEIR specific version of worst\-case scenario that would make them think "That's exactly what keeps me up at night\."


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
