# First-Principles Analysis: What H12 Is Missing

## What H12 Maps To

H12 (Visual Recipe Distillation Laws) maps to the 14 archetype-specific **visual recipe** skills in `ccf-26/skills/ccf/distribution/visual-recipes/`. These are the agents that take an AUTHORIZED script and generate visual prompts (image generation instructions) for the content.

---

## What the Actual Pipeline Does

### Visual Recipe Architecture (Sample: storytelling-archetypes, 253 lines)

**Identity:** "Conscious Art Director" executing archetype-specific visual recipe protocol.

**7-Step Process:**
1. **Emotional Archetype Analysis** — classify content into one of 16 storytelling archetypes (4 clusters: Transformation, Connection, Anticipation, Emotional Resonance)
2. **Narrative Structure Determination** — 3/4/5 scene structure based on archetype
3. **Character Casting & Age Selection** — from `character_lexicon`, age based on archetype needs
4. **Base Scene Prompt** — character foundation, environmental context, visual style (Ghibli/photorealism/cinematic)
5. **Variant Prompts** — narrative progression through modification prompts per scene
6. **Strategic Semiotic Injection** — injects `facial_expression_lexicon.memetic_reference_prompt` at the climax scene
7. **Emotional Continuity Verification** — escalation, injection feels natural, resolution closure, character consistency

**Output:** JSON with `base_scene_prompt`, `variant_prompts[]`, `strategic_notes{}`

**14 Recipe Types:**
case-study, comparison-archetypes, conceptual-contrast, debunking-myths-scams, dopamine-cliff-carousel, listicle, observational-humor, relief-peak-carousel, stereotypical-poll, storytelling-archetypes, the-archetypical-poll, the-controversial-dilemma-poll, visual-timeline, worst-case-scenario

**Brand Avatar Injection (CCF Addition):** Loads physical DNA from `soul_values.json` — every person-based prompt uses the brand avatar's physical description.

---

## The Gap: What H12's Visual Recipes Miss

### 1. Semiotic Injection Creates Trust Erosion

This was identified in the SWOT analysis and confirmed by the user. The current pipeline uses "Strategic Semiotic Injection" — injecting a `memetic_reference_prompt` from the `facial_expression_lexicon` at the climax scene. This means:

- The visual references a known facial expression from a real person or cultural reference
- The AI generates an image that tries to match that reference
- The viewer compares the AI image to the real reference
- Any discrepancy is perceived as "SLOP" — fake, uncanny, untrustworthy

**Example:** If the lexicon says "inject Serena Williams' victory expression," the AI generates a face that tries to replicate Serena's expression. The viewer immediately sees it's NOT Serena, and the entire image loses credibility.

**User's directive:** Replace reference-based generation with original emotional descriptions. The AI should generate ORIGINAL characters with TEXT-DESCRIBED emotions, avoiding all comparison traps.

### 2. No Input Validation Between Script and Visual

The recipe takes an "AUTHORIZED" script as input (file existence check) but doesn't validate whether the script contains the information the visual recipe needs:

| What the Recipe Needs | What the Script Provides | Gap |
|:---|:---|:---|
| Emotional archetype classification | No explicit archetype tag in script | Recipe must infer archetype from content |
| Character age and casting | No character specification | Recipe determines casting independently |
| Mode (T/V/R) per scene | No mode tags in script | Recipe generates visuals mode-blind |
| Environmental context | Scene descriptions vary | May not contain enough environmental detail |

The recipe operates on inference from the script text, not on structured handoff data. This means two different recipe agents processing the same script might make different casting and environmental decisions.

### 3. No Visual Authenticity Gate

The "Quality Standards" section lists 6 checks (emotional authenticity, progressive intensity, cultural resonance, character consistency, strategic impact, viral optimization) but none test for:

- **Comparison trap:** Does the prompt invite comparison to a known face or reference?
- **Interchangeability:** Could a competitor's content use this exact visual?
- **Tribal recognition:** Would the tribe see themselves in this visual?
- **Original vs. derivative:** Is this an original visual or a reference-dependent one?

### 4. No Mode-to-Visual Routing

The recipe classifies content by emotional archetype (16 types in 4 clusters) but not by content MODE (T/V/R). Different modes require fundamentally different visual approaches:

| Mode | Visual Approach | What the Recipe Currently Does |
|:---|:---|:---|
| **TENSION** | Documentary-style, evidence-gathering, confrontational framing | No mode-specific routing — same recipe logic for all modes |
| **VULNERABILITY** | Intimate, close-up, soft lighting, private setting | Same as above |
| **RECOGNITION** | Communal, wide-shot, familiar environment, tribal markers | Same as above |

The 16 emotional archetypes partially overlap with modes (e.g., Recognition Story ≈ RECOGNITION mode) but the mapping is implicit and incomplete.

---

## The 4 Derived Laws for H12

### Law 1 — Law of Original Visual Generation

**Axiom:** "An AI visual that references a known face invites comparison. Comparison reveals the AI. The AI is then the story, not the content."

All visual prompts must describe emotions, expressions, and body language through TEXT — never through reference to a specific person, memetic reference, or known facial expression. The `facial_expression_lexicon.memetic_reference_prompt` injection system must be replaced with original emotional descriptions derived from the script's emotional content.

**Where this integrates:** Step 6 (Strategic Semiotic Injection) is replaced with "Emotional Peak Description" — a text-based description of the climax emotion written from the script's narrative content.

### Law 2 — Law of Script-to-Visual Handoff Validation

**Axiom:** "A visual recipe cannot generate what it doesn't receive. The gap between script and visual is where authenticity dies."

Before executing the recipe, validate that the authorized script contains: explicit emotional archetype or mode tag per section, character context (who is in this scene), environmental context (where this scene takes place), and emotional progression markers. If missing, flag for manual annotation before proceeding.

**Where this integrates:** New pre-flight validation step in the I-R-E-V-C INGEST phase, checking script metadata fields.

### Law 3 — Law of Mode-to-Visual Routing

**Axiom:** "A TENSION visual and a RECOGNITION visual for the same topic should look fundamentally different. If they don't, the MODE is decoration, not direction."

Each recipe must include mode-specific visual parameters:
- **TENSION:** Documentary framing, evidence lighting, institutional settings, observer perspective
- **VULNERABILITY:** Intimate framing, soft/warm lighting, private settings, subjective perspective
- **RECOGNITION:** Communal framing, natural lighting, familiar tribal settings, inclusive perspective

**Where this integrates:** New sub-section in each visual recipe SKILL.md mapping mode to visual parameters.

### Law 4 — Law of Visual Authenticity Gate

**Axiom:** "A visual that could belong to any brand is a visual that belongs to no brand."

Gate checks:
1. **No comparison trap:** Prompt contains no reference to real people, celebrities, or known memetic expressions
2. **Not interchangeable:** Visual contains a tribal recognition code (from H9's visual recognition code library)
3. **Brand Avatar present:** Every person-based prompt uses the brand avatar's physical DNA (existing CCF addition — validated)
4. **Mode coherence:** Visual parameters match the tagged content mode (T/V/R)

**Where this integrates:** Added to the I-R-E-V-C VALIDATE phase of each visual recipe.

---

## Current vs. Law-Governed Comparison

| What Happens Now | What Happens With Laws |
|:---|:---|
| Semiotic injection from facial_expression_lexicon at climax | Original emotional description from script narrative |
| Script input validated only for file existence | Script-to-visual handoff validated for emotional/mode/character metadata |
| Same visual logic regardless of content mode | Mode-specific visual parameters (TENSION ≠ VULNERABILITY ≠ RECOGNITION) |
| Quality checks for consistency and intensity only | Authenticity gate: no comparison traps, tribal recognition, brand avatar, mode coherence |
| 16 emotional archetypes as implicit mode proxy | Explicit mode (T/V/R) routing with archetype as secondary classification |

---

*This analysis grounds the H12 implementation architecture document. The 4 laws (Original Visual Generation, Script-to-Visual Handoff, Mode-to-Visual Routing, Visual Authenticity Gate) are derived from gaps in the 14 visual recipe skills and the SWOT-identified semiotics trust erosion problem, grounded in the actual CCF pipeline.*
