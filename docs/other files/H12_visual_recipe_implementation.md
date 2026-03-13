# H12: Visual Recipe Distillation Laws — Implementation Architecture

**Hypothesis:** The 14 visual recipe skills generate visual prompts using "Strategic Semiotic Injection" — referencing known facial expressions via `facial_expression_lexicon.memetic_reference_prompt`. This creates comparison traps where AI-generated faces are judged against real references, breaking viewer trust. Additionally, recipes operate mode-blind (no T/V/R routing) and have no script-to-visual handoff validation.

**Pipeline Position:** CCF Distribution Phase → Visual Recipes → Visual Prompts → Image Generation  
**Existing Infrastructure:** 14 archetype-specific `visual-recipes/` skills, Art Director orchestration  
**Gap Classification:** HIGH — The semiotic injection model is architecturally sound but creates trust erosion per SWOT analysis  
**Dependency:** Receives AUTHORIZED script from H3/Script phase, soul_values from H8, visual recognition codes from H9 (proposed)

---

## Section 1: The Input Quality Problem

Visual recipes currently take an AUTHORIZED script file and `soul_values.json` as inputs. The script is verified for FILE EXISTENCE but not for CONTENT QUALITY. The recipe must infer emotional archetype, character casting, and environmental context from the script text — information that should be structured metadata, not free-text inference.

### Input Saturation Gate

| Input | Minimum Requirement | Source |
|:------|:-------------------|:-------|
| AUTHORIZED script | Must exist AND contain mode tags per section (from H1/H3) | Script phase output |
| `soul_values.json` | Brand avatar physical DNA must be present | H8/H10 output |
| Visual Recognition Codes (NEW) | Optional but enriches tribal authenticity | H9 output |
| Blueprint mode assignments | Mode (T/V/R) per content section | H1 output |

**Saturation test:** If the script contains no mode tags, the recipe operates mode-blind. This is the current default. With H1/H3 law integration upstream, scripts will arrive with mode metadata.

---

## Section 2: The 4 Laws of Visual Recipe Distillation

### Law 1 — Original Visual Generation (No Comparison Traps)

**Axiom:** *An AI visual that references a known face invites comparison. Comparison reveals the AI. The AI is then the story, not the content.*

**The Change:** Replace Step 6 (Strategic Semiotic Injection) across all 14 recipe skills.

**Current Step 6:**
```
Identify the climax scene → Select expression from facial_expression_lexicon
→ Inject memetic_reference_prompt into modification_prompt
→ All other scenes use literal descriptions
```

**New Step 6 — Emotional Peak Description:**
```
Identify the climax scene → Derive the peak emotion from the SCRIPT'S narrative content
→ Write an ORIGINAL text-based description of:
  - Facial expression (described by muscle movement, not reference)
  - Body language (described by action, not pose)
  - Environmental response (atmosphere changes that reflect the emotion)
→ All scenes use original text descriptions (no references to any known person/expression)
```

**Banned Pattern:**
```
❌ BAD:  "Her expression mirrors the victorious determination of Serena Williams after match point"
✅ GOOD: "Eyes wide, jaw slightly dropped, breath suspended — the micro-second between
          receiving the news and understanding what it means. Hands pressed flat
          against the table as if grounding herself against the shock."
```

**Where this integrates:** Step 6 of every visual recipe SKILL.md. The `facial_expression_lexicon.memetic_reference_prompt` is no longer injected. Instead, the recipe generates original expression text from script context.

### Law 2 — Script-to-Visual Handoff Validation

**Axiom:** *A visual recipe cannot generate what it doesn't receive.*

**Pre-flight validation before recipe execution:**

```
HANDOFF VALIDATION TABLE
| # | Check | Requirement | Missing Action |
|:--|:------|:-----------|:--------------|
| 1 | Mode tags present | Each script section has T/V/R tag | FLAG: recipe runs mode-blind |
| 2 | Character context | Script specifies who is in scene | FLAG: recipe must infer casting |
| 3 | Environmental context | Script describes setting | FLAG: recipe uses generic environment |
| 4 | Emotional progression | Script has escalation markers | FLAG: recipe cannot build arc |
```

Handoff passes if ≥3/4 checks are met. If ≤2/4, the recipe must request manual annotation before proceeding.

**Where this integrates:** New step in I-R-E-V-C INGEST phase, before recipe logic executes.

### Law 3 — Mode-to-Visual Routing

**Axiom:** *A TENSION visual and a RECOGNITION visual for the same topic should look fundamentally different.*

Each recipe gains a mode-to-visual parameter table:

| Parameter | TENSION | VULNERABILITY | RECOGNITION |
|:----------|:--------|:-------------|:------------|
| **Framing** | Documentary, observational | Intimate, close-up | Communal, wide-shot |
| **Lighting** | Harsh, unforgiving, clinical | Soft, warm, private | Natural, golden hour |
| **Environment** | Institutional, public | Private, personal space | Familiar, tribal space |
| **Camera perspective** | Observer (3rd person) | Subjective (1st person feel) | Inclusive (group perspective) |
| **Color palette** | Desaturated, cold | Warm, muted | Rich, saturated, cultural |
| **Expression style** | Controlled tension, jaw set | Open vulnerability, soft eyes | Warm recognition, communal belonging |

**Where this integrates:** New sub-section in each visual recipe SKILL.md. The recipe reads the script's mode tag per section and applies the corresponding visual parameters.

**Archetype-Specific MODE Overrides (per recipe type):**

The generic table above provides defaults. Each archetype has unique visual failure modes:

| Recipe Archetype | TENSION Override | VULNERABILITY Override | RECOGNITION Override |
|:----------------|:----------------|:----------------------|:--------------------|
| authority-tier-list | Split-screen comparison, cold evidence | Coach alone with data, warm-close | Tribe items visually ranked, communal judging |
| contrarian-pivot | Before/after visual contradiction | Coach admitting the previous frame was wrong | Tribe nodding, shared "I knew it" moment |
| raw-confession | Harsh spotlight, nowhere to hide | Extreme close-up, raw unfiltered | Tribe as silent witnesses, communal exhale |
| nostalgia-story | Sepia-to-cold transition, time contrast | Coach in memory space, soft dissolve | Tribe sharing parallel memories, generational |
| cautionary-tale | Aftermath scene, consequences visible | Coach in the wreckage of their mistake | Tribe recognizing their own close call |
| villain-reveal | Dramatic unveiling, exposé framing | Coach shows they were once the villain | Tribe seeing their own blind spots |
| how-to-method | Step-by-step progression, clinical | Coach showing the messy reality behind the method | Tribe attempting the method, real struggle |
| myth-buster | Evidence wall, forensic analysis | Coach admits they believed the myth too | Tribe's collective "wait, WHAT?" |

> [!IMPORTANT]
> Each recipe SKILL.md gets a `## MODE OVERRIDE` section appended — NOT a rewrite. The override table supplements the generic defaults for scenes where the archetype's storytelling structure demands specific visual treatment.

**Visual Novelty Protocol (Boredom Ban for Visuals):**

```
BEFORE generating visual prompts for a new content piece:
  1. CHECK: Have we used this exact framing/composition in the last 5 pieces?
     → If YES: shift camera perspective OR environment OR lighting model
  2. CHECK: Is the emotional peak using the same expression type as last time?
     → If YES: find a different physical manifestation of the same emotion
  3. IF stuck in visual monotony for 3+ consecutive pieces:
     → TRIGGER SoulResonance extension to find an unexpected visual metaphor
     → The best visuals are the ones the system didn't predict it would generate
```

### Law 4 — Visual Authenticity Gate

**Axiom:** *A visual that could belong to any brand is a visual that belongs to no brand.*

**4 Gate Checks (per visual prompt):**

```
CHECK 1: No Comparison Trap
  "Does this prompt reference any real person, celebrity, or known expression?"
  → YES = REJECT — rewrite with original description
  → NO = PASS

CHECK 2: Not Interchangeable
  "Could a competitor in a different niche use this exact visual?"
  → YES = ADD tribal recognition code (from H9 library)
  → NO = PASS — visual is already niche-specific

CHECK 3: Brand Avatar Present
  "Does every person-based prompt use the brand avatar's physical DNA?"
  → NO = INJECT from soul_values.json physical_description
  → YES = PASS (existing CCF addition — validated)

CHECK 4: Mode Coherence
  "Do the visual parameters match the tagged content mode (T/V/R)?"
  → MISMATCH = REVISE visual parameters to match mode
  → MATCH = PASS
```

**Where this integrates:** I-R-E-V-C VALIDATE phase of each visual recipe.

---

## Section 3: Output Format Enhancement

```json
{
  "base_scene_prompt": "...",
  "variant_prompts": [
    {
      "scene_name": "...",
      "modification_prompt": "...",
      "mode": "TENSION | VULNERABILITY | RECOGNITION",
      "visual_parameters_applied": "documentary | intimate | communal"
    }
  ],
  "strategic_notes": {
    "selected_archetype": "...",
    "narrative_structure": "...",
    "casting_decision": "...",
    "emotional_peak_scene": "[scene that received the emotional peak description]",
    "peak_emotion_source": "[script passage that drove the peak emotion]",
    "mode_routing": { "scene_1": "T", "scene_2": "V", "scene_3": "R" },
    "tribal_recognition_codes_used": ["..."],
    "visual_style_rationale": "..."
  },
  "authenticity_gate": {
    "comparison_trap": "CLEAR",
    "interchangeability": "PASSED — [tribal code used]",
    "brand_avatar": "INJECTED",
    "mode_coherence": "ALL SCENES MATCHED"
  }
}
```

---

## Section 4: 5 Micro-Hypothesis Evaluations

**MH1 — Comparison Trap Test:** Scan all prompts for references to real people, celebrities, or known expressions. Zero references = PASS. Verifiable: string search for proper nouns and "like [person]" patterns.

**MH2 — Mode Routing Test:** Each scene should have a mode tag. Visual parameters should match the mode table. Verifiable: cross-reference scene mode against parameter table.

**MH3 — Brand Avatar Coverage:** Every person-based prompt must include brand avatar physical DNA. Verifiable: check for physical_description elements in person prompts.

**MH4 — Tribal Recognition Test:** ≥1 scene should include a tribal recognition code (from H9). Verifiable: check `tribal_recognition_codes_used` field.

**MH5 — Emotional Peak Quality:** The peak emotion scene should derive from the script narrative (not a reference). Verifiable: check `peak_emotion_source` traces to an actual script passage.

---

## Validation Receipt

```
H12 VALIDATION RECEIPT
━━━━━━━━━━━━━━━━━━━━━━
Blueprint:       [ID]
Recipe:          [type]
Coach:           [name]
Date:            [timestamp]
Script Source:   [filename]

LAW COMPLIANCE
━━━━━━━━━━━━━━
Law 1 — No Comparison Traps:     [0 references found]  [PASS/FAIL]
Law 2 — Handoff Validation:      [n/4 checks passed]   [PASS/FAIL if <3]
Law 3 — Mode Routing:            [n/n scenes mode-matched]  [PASS/FAIL]
Law 4 — Authenticity Gate:       [4/4 checks]  [PASS/FAIL]

MICRO-HYPOTHESES
━━━━━━━━━━━━━━━━
MH1 Comparison Trap:     [PASS/FAIL]
MH2 Mode Routing:        [PASS/FAIL]
MH3 Brand Avatar:        [PASS/FAIL]
MH4 Tribal Recognition:  [PASS/FAIL]
MH5 Peak Quality:        [PASS/FAIL]

STATUS: [AUTHENTICATED / PROVISIONAL / FAILED]
```
