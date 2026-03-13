---
name: ccf-visual
description: Generate visual prompts using CCF visual recipe skills with CMF mechanisms
---

# /ccf-visual — CCF Visual Recipe Execution

// turbo-all

> **Usage:** `Read commands/ccf-visual.md and execute for archetype "{ARCHETYPE}" with content "{CONTENT_TOPIC}"`
>
> **Example:** `Read commands/ccf-visual.md and execute for archetype "storytelling-archetypes" with content "How I went from broke to building a 6-figure coaching business"`

---

## 🎯 STEP 0: PARSE ARGUMENTS & INITIALIZE

**Extract from the user's command:**
- `{ARCHETYPE}` — The visual recipe to use (see routing table below)
- `{CONTENT_TOPIC}` — The content idea or topic to visualize
- `{PROJECT_FOLDER}` — (Optional) Path to existing CCF project for context

**ARCHETYPE ROUTING TABLE:**

| Argument | Skill Path | Format |
|:---------|:-----------|:-------|
| `storytelling-archetypes` | `skills/ccf/visual-recipes/storytelling-archetypes/SKILL.md` | Multi-scene carousel |
| `dopamine-cliff` | `skills/ccf/visual-recipes/dopamine-cliff-carousel/SKILL.md` | 5-slide carousel |
| `case-study` | `skills/ccf/visual-recipes/case-study/SKILL.md` | Multi-scene narrative |
| `listicle` | `skills/ccf/visual-recipes/listicle/SKILL.md` | Multi-item carousel |
| `comparison` | `skills/ccf/visual-recipes/comparison-archetypes/SKILL.md` | 2-part comparison |
| `conceptual-contrast` | `skills/ccf/visual-recipes/conceptual-contrast/SKILL.md` | Split-screen contrast |
| `debunking` | `skills/ccf/visual-recipes/debunking-myths/SKILL.md` | 3-scene debunking |
| `observational-humor` | `skills/ccf/visual-recipes/observational-humor/SKILL.md` | Single frame |
| `relief-peak` | `skills/ccf/visual-recipes/relief-peak-carousel/SKILL.md` | 5-slide carousel |
| `stereotypical-poll` | `skills/ccf/visual-recipes/stereotypical-poll/SKILL.md` | Poll format |
| `archetypical-poll` | `skills/ccf/visual-recipes/archetypical-poll/SKILL.md` | Archetype poll |
| `controversial-dilemma` | `skills/ccf/visual-recipes/controversial-dilemma-poll/SKILL.md` | Dilemma poll |
| `visual-timeline` | `skills/ccf/visual-recipes/visual-timeline/SKILL.md` | 6-8 scene timeline |
| `worst-case` | `skills/ccf/visual-recipes/worst-case-scenario/SKILL.md` | Single frame |

> [!CAUTION]
> If the archetype argument does not match any entry above, **STOP** and ask the user which recipe they want. DO NOT guess.

---

## 📋 STEP 1: LOAD SKILL & SHARED GUIDE

**Read and internalize these files:**

```
1. Load the matched SKILL.md from the routing table above
   - Internalize ALL protocol steps, variant rules, and JSON output schema
   - Note the specific SENSORY ZOOM guidance for this format

2. Load the shared VDP Lite guide:
   intelligence/guides/visual_density_lite.md
   - S-Codes (S1-S5)
   - Biological Hook Rule
   - Sensory Zoom Rule
   - VDP Lite Scoring Checklist
```

---

## 📋 STEP 2: LOAD PROJECT CONTEXT

**If `{PROJECT_FOLDER}` is provided:**

```
Load from the project folder:
1. validated_content — The content topic/idea with soul alignment
2. character_lexicon — Available character ages, ethnicities, features
3. facial_expression_lexicon — Semiotic injection expression options
4. conscious_soul_values — Client's core values and worldview
```

**If no project folder:**

```
Use {CONTENT_TOPIC} directly. Generate a minimal context:
1. validated_content = {CONTENT_TOPIC}
2. character_lexicon = Use a general 30-year-old character
3. facial_expression_lexicon = Use common expressions (surprise, determination, relief)
4. conscious_soul_values = Infer from the content topic
```

> [!IMPORTANT]
> Whether from a project or inferred, you MUST have all 4 context elements before proceeding.

---

## 📋 STEP 3: BUILD CHARACTER ANCHOR

**Following the CHARACTER ANCHOR TEMPLATE from the loaded skill:**

```
"{Name}, {age} {ethnicity}. SKIN: {exact tone}. {Hair description}. 
{Defining accessories/clothing}. {Current body state}."
```

**Build the NEGATIVE PROMPT:**

```
"No generic backgrounds. No studio lighting. No stock photo compositions. 
No standard mid-shots without texture. No floating subjects."
```

> [!CAUTION]
> This anchor is **NON-NEGOTIABLE** — it appears in base_scene_prompt AND every variant modification_prompt.

---

## 📋 STEP 4: EXECUTE RECIPE PROTOCOL

**Follow the loaded skill's protocol steps IN ORDER:**

1. **Soul-Aligned Analysis** — Analyze the content through the lens of the recipe's archetype
2. **Character Selection** — Apply the Character Anchor Lock from Step 3
3. **Base Scene Prompt** — Generate with BIOLOGICAL HOOK as first line + SENSORY ZOOM
4. **Variant Prompts** — Generate per recipe variant rules, each with its own SENSORY ZOOM
5. **Semiotic Injection** — Apply to the designated injection scene per recipe
6. **VDP Lite Scoring** — Score EACH scene (see Step 5 below)

**BIOLOGICAL HOOK ENFORCEMENT:**

Every prompt MUST open with a physical texture detail. Examples:
- ❌ "A young woman stands in her apartment"
- ✅ "Her thumb traces the cracked screen of her phone, nail catching on the spider-web fracture"

**SENSORY ZOOM ENFORCEMENT:**

Every scene MUST include: `[Body Part] + [Object] + [Texture]`
- ❌ "She holds a coffee cup"
- ✅ "Her fingertips press into the warm ceramic mug, heat spreading through chipped nail polish"

---

## 📋 STEP 5: VDP LITE SCORING GATE

**Score EACH scene prompt against this checklist:**

| Check | Points |
|:------|:-------|
| S1: Body part showing tension/action? | +2 |
| S2: Private/intimate behavior visible? | +2 |
| S3: Hand touching a specific object? | +1 |
| S4: Sensory texture described? | +2 |
| S5: One weird/unique detail from content? | +2 |
| Sensory Zoom present (body + object + texture)? | +2 |
| Biological Hook in opening line? | +1 |

**PASS: ≥ 7 points per scene.**

> [!CAUTION]
> If ANY scene scores below 7, **REWRITE IT** before proceeding. Do not output failing scenes.

---

## 📋 STEP 6: OUTPUT JSON

**Generate the final JSON exactly matching the recipe's output schema.**

The JSON MUST include:
- `character_anchor` — Full character DNA string
- `negative_prompt` — Standard negative prompt
- `base_scene_prompt` — Opens with biological texture detail
- `variant_prompts` — Array of scene objects (or empty for single-frame recipes)
- `strategic_notes` — Including `vdp_lite_scores` per scene

**Output location:** Print JSON to console.

If `{PROJECT_FOLDER}` is provided, also save to:
```
{PROJECT_FOLDER}/visuals/{ARCHETYPE}_visual.json
```

---

## 📋 STEP 7: VALIDATION SUMMARY

**Print a validation report:**

```
✅ CCF VISUAL RECIPE COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Archetype:        {ARCHETYPE}
Content:          {CONTENT_TOPIC}
Scenes generated: {N} (base + variants)
VDP Lite scores:  {list scores per scene}
All scenes ≥ 7:   ✅/❌
Character Anchor: Present in all scenes: ✅/❌
Biological Hook:  Present in all scenes: ✅/❌
Sensory Zoom:     Present in all scenes: ✅/❌
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 📋 STEP 8: H5 DISTILLATION GATE

> [!CAUTION]
> **MANDATORY GATE — Image generation blocks if this fails.**

1. Read FULL: `ccf-26/skills/ccf/distillation/visual-distiller/SKILL.md`
2. Execute 4-Phase Audit on the visual output:
   - Law 1: Visual Saturation Audit (felt specificity per PRIMAL field, 0 summary-language)
   - Law 2: MODE Coherence Audit (7-block justification, cross-layer coherence ≥7/10)
   - Law 3: Compression Audit (≥5/7 blocks MODE-justified per prompt)
   - Law 4: Visual Authenticity Gate Audit (4 checks per prompt)
3. **CREATE FILE:** `{PROJECT_FOLDER}/visuals/{ARCHETYPE}_H5_DISTILLATION_RECEIPT.md`

**IF FAIL:** Return to STEP 4 — rewrite specific prompts with remediation from receipt.
**IF PASS:** Image generation is approved.

```
✅ H5 DISTILLATION GATE: PASS
- Felt Specificity: 0 summary-language fields
- MODE Coherence: [n]/[n] prompts pass
- Compression: [n]/[n] prompts ≥5/7
- Authenticity Gate: [n]/[n] prompts 4/4 checks
```

---

## 🔗 NEXT STEPS

After generating visual prompts, the user can:
- Use the JSON output directly with image generation tools
- Feed prompts into Midjourney, DALL-E, or Seedream
- Iterate on specific scenes by re-running with modified content

---

**END OF CCF-VISUAL COMMAND**
