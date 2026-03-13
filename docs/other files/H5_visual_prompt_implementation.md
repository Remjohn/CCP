# H5 — Visual Prompt Writing: First-Principles Implementation Architecture

**Pipeline Stage:** CCF Distribution Phase → Visual Prompt Generation (Asset Library → PRIMAL Analysis → Visual Recipe Prompts)  
**Laws Applied:** 4 Laws of Visual Distillation  
**MCDA Score:** 8.95/10 (Ranked #2)  
**Target Skills:** `ccf-26/skills/ccf/distribution/art-director/SKILL.md`, `ccf-26/skills/ccf/distribution/visual-recipes/*/SKILL.md`  
**Target Command:** `commands/ccf-visual.md`  
**Input:** H13 Receipt + Accepted Asset Library + `soc_output.json` (`mode_arc`) + Brand Avatar + `scripts/final/{blueprint_id}_script.md`  
**Output:** Scene-level visual recipe prompts — emotionally saturated, mode-compressed, authenticity-verified  
**Validation:** H5 Distillation Receipt (Required before image generation begins)

---

## System Overview: What H5 Actually Does

H5 is the final translation stage in the distillation funnel. It receives everything the pipeline has produced — H0's first-party coach signal, H1's emotionally typed blueprints, H6/H7's depth-stratified research, H3's mode-arc voice material, H13's evidence-grade asset library — and converts it all into precise visual prompt instructions that an image generation model can execute.

The current pipeline's PRIMAL Analysis is structurally sophisticated: it extracts PHYSICAL REALITY, INNER WORLD, METAPHYSICAL DIMENSION, AUTHENTICITY MARKERS, LIGHTING, and BRAND INTEGRATION across 7 structured blocks per scene. It routes each scene to a MODE (TENSION, VULNERABILITY, RECOGNITION) which maps to specific technical presets: lighting temperatures, T-codes, V-codes, cinematographic grammars, verb classes.

**What MODE currently is: a routing table.** It tells the Storyboard Composer which preset to select.  
**What MODE must become: an emotional constraint.** It tells every single block in the 7-block prompt that its choices must serve ONE biological/psychological function — and provides the falsifiable axiom for WHY.

The gap is measurable: a prompt can score 95/100 on the Visual Fidelity Score (VFS) — passing all 15 technical compliance checks — and still produce an image that is emotionally interchangeable with any other coaching video. Technically perfect. Emotionally generic. The 4 Laws of Visual Distillation close this gap.

---

## Section 1: Input Quality Standards (Visual Saturation Protocol)

A visual prompt cannot convey what its inputs have not felt. Before the Storyboard Composer writes a single line, every upstream input must pass the Visual Saturation Gate — a quality check on whether the inputs carry **felt specificity** rather than narrative summary.

### Required Input Files & Quality Standards

| # | Input Source | File / Field | Minimum Quality Standard |
|:--|:------------|:-------------|:------------------------|
| 1 | **H13 Receipt** | `H13_DISTILLATION_RECEIPT.md` + accepted asset library | `asset_status: ACCEPTED` + all assets have `emotional_mode`, `compression_level ≥ L3`, all 4 authenticity checks passed |
| 2 | **soc_output.json** | `mode_arc` field — typed T/V/R sentences | `mode_arc` must be fully populated: `tension_sentence`, `vulnerability_sentence`, `recognition_sentence` each present |
| 3 | **Final Script** | `scripts/final/{blueprint_id}_script.md` — exact verbatim quotes with timestamps per scene (from `ccf-26/skills/ccf/production/script-generator/SKILL.md`) | Every scene must have: exact coach quote, timestamp, scene ID. No paraphrases. |
| 4 | **Brand Avatar** | Physical DNA — skin, costume, hair, specific cultural markers | Must specify what each marker MEANS emotionally — not just physical description |
| 5 | **tribe_soul.json** | Visual codes the tribe uses to signal membership | Must contain ≥1 anti-aspirational marker (what the tribe rejects as "not us") |

### PRIMAL Field Quality Gate (The Felt Specificity Test)

The PRIMAL Analysis produces 7 input blocks for every prompt. Each block is checked for felt specificity before the Storyboard Composer begins writing. The gate rejects summary language and requires sensory precision:

| PRIMAL Field | Failing Input (summary) | Passing Input (felt specificity) |
|:------------|:------------------------|:---------------------------------|
| **PHYSICAL REALITY** | "She looks confused" | "Hands that were gripping the edge of the counter — now pausing, lowering, as if the grip is being voluntarily released" |
| **INNER WORLD (FEELING)** | "She feels surprised but starts to understand" | "The vertigo of recognizing that a belief you built your career on was constructed for someone else's body — arrested by a sharp specific truth" |
| **METAPHYSICAL DIMENSION** | "A moment of insight" | "The exact instant the internal ceiling lifts — before she has the words for it. The gap between habitual assumption and sudden knowing" |
| **AUTHENTICITY MARKERS** | "She wears casual clothes" | "Teal sweater against dark mahogany skin — the contrast that makes her visible from across a room without trying to be" |
| **ENVIRONMENT** | "A kitchen" | "Intimate dining space. Specific food items in soft focus foreground — the domestic weight of the meal as context, not decoration" |
| **TIMESTAMP** | General scene reference | Exact verbatim quote from final script (`scripts/final/{blueprint_id}_script.md`) with HH:MM:SS |
| **BRAND INTEGRATION** | "Include brand colors" | Exact hex codes with placement: "muted terracotta on ambient object, never on skin, never centered" |

**The Felt Specificity Gate:**
```
"Does the PRIMAL ANALYSIS contain at least ONE detail that could NOT describe
 any other coach in any other moment — at any point in production history?"

→ NO  = The inputs are emotionally thin. No technical compliance will save
         the prompt from producing a generically beautiful image.
         STOP. Return to source materials for additional specificity extraction.

→ YES = PASS. The saturation carries first-party visual data.
```

---

## Section 2: Law Execution Protocol

### Law 1 — Visual Saturation Before Composition

**Axiom:** *A visual prompt cannot convey what its inputs have not felt.*

**What it does:** Ensures the PRIMAL Analysis — the extraction step that feeds prompt writing — operates at the level of felt emotional truth, not narrative summary. Saturation happens during extraction, before any prompt block is composed.

**The Biological Grounding:**  
The image generation model outputs what it is instructed to imagine. If the instruction contains the psychological precision of "the gap between habitual assumption and sudden knowing," the model accesses latent representations of internal cognitive shift — an expression, a tension in the body, a quality of stillness — that no generic briefing can locate. If the instruction says "a moment of insight," the model returns stock insight: tilted head, upward gaze, gentle smile.

Saturation is the difference between the model finding a specific image in its latent space and the model generating a category of image.

**Saturation-Mode Connection:**  
Every saturation element must be tagged to a mode before prompt composition begins:
```
→ Elements serving TENSION: tag → informs T-Code, friction verb, cold/harsh light rationale
→ Elements serving VULNERABILITY: tag → informs V-Code, release verb, warm-intimate light rationale
→ Elements serving RECOGNITION: tag → informs close shot, mirror verb, warm-expansive rationale
```

---

### Law 2 — MODE as Emotional Constraint, Not Technical Routing

**Axiom:** *A visual's emotional impact is determined by whether every element serves ONE emotional function. Elements serving different functions cancel each other out.*

**The Biological Foundation of Each MODE (why the routing works):**

**TENSION — Biological basis:**  
High-contrast cold lighting forces the visual cortex to process high-frequency edge information — the same neural pathway activated by threat detection. Harsh shadows signal environmental hostility. Wide-angle spatial compression creates a sense of inescapability. The viewer's amygdala responds to these visual properties **before conscious processing begins**. This is not metaphorical lighting preference — it is the biological mechanism of Prediction Error.

**VULNERABILITY — Biological basis:**  
Soft warm light at close focal distance mimics the physical conditions of intimate proximity: candlelight, bedside lamp, firelight. This specific combination (warm temperature + close source + soft diffusion) activates the viewer's parasympathetic nervous system — the biological system that lowers defenses and creates the physiological precondition for trust. Vulnerability only works when the viewer's body has already relaxed. Lighting creates that relaxation before the content asks for it.

**RECOGNITION — Biological basis:**  
Golden-hour and warm-expansive light at the specific color temperature range of 3200-4500K activates the brain's nostalgia circuitry — the pattern-matching system that associates this visual temperature with belonging, shared meals, sunset gatherings, late-afternoon memory. The viewer recognizes the FEELING before they process the CONTENT. This is why the tribe says "that's me" before they know what they're looking at. The visual triggers the memory; the narrative confirms it.

**The 7-Block MODE Coherence Check:**

```
"For each of the 7 prompt blocks, identify whether its choices are JUSTIFIED
 by the assigned MODE's biological logic — or merely SELECTED from the MODE's
 technical preset."

JUSTIFIED (Law 2 PASS):
  Block 3 (Lighting): "Cold high-contrast BECAUSE the system the narrator
  describes is designed to exclude — and the viewer's body should feel
  that exclusion before the word is spoken."

SELECTED (Law 2 FAIL):
  Block 3 (Lighting): "Cold high-contrast [assigned from TENSION preset]"

→ JUSTIFIED = the Composer understands WHY. The VFS Commander can verify it.
→ SELECTED = the Composer is following a table. The output may be
             technically correct and emotionally arbitrary.
```

**The Cross-Layer Coherence Test:**
> "If shown this image to 10 people with no audio and no context — and asked them to choose one word — would ≥7 choose a word from the correct mode's vocabulary?"  
>
> - TENSION vocabulary: trapped, crushed, cold, suffocating, stuck, pressure  
> - VULNERABILITY vocabulary: exposed, raw, intimate, fragile, open, seen  
> - RECOGNITION vocabulary: familiar, home, relatable, known, "that's me," warm  
>
> → <7/10 = The image is mode-ambiguous. Rewrite with stronger constraint.  
> → ≥7/10 = PASS. The image achieves emotional clarity.

---

### Law 3 — Compression Across Visual Layers

**Axiom:** *A visual prompt's density is proportional to the number of layers serving ONE emotional function. Layers serving different functions dilute the image.*

**What it does:** Tests whether all 7 prompt blocks are compressed through the MODE constraint, or whether they operate as independent technical choices that happen to sit next to each other.

**The Compression Test (per prompt):**

```
COUNT: "How many of the 7 blocks make a choice that is explicitly
        JUSTIFIED by the assigned MODE's biological logic?"

≥5/7 blocks justify through MODE = COMPRESSED prompt (PASS)
  → Every layer amplifies the same emotional function.
  → Removing any single block weakens the emotional payload.
  → The image has mode density: one feeling, rendered from multiple angles.

<5/7 blocks justify through MODE = THIN prompt (FAIL)
  → Blocks are technically selected but not emotionally unified.
  → The image will carry mixed signals — some TENSION blocks,
     some neutral blocks, perhaps an inadvertent RECOGNITION element.
  → The viewer's body receives contradictory instructions.
```

**Dense Compression Example (TENSION scene):**

```
Block 1 (PHYSICAL REALITY):  Friction verb "gripping" → MODE: TENSION ✅
Block 2 (INNER WORLD):       "Vertigo of forced exclusion" → TENSION biology ✅
Block 3 (LIGHTING):          Cold high-contrast, justified: "environment as hostile" ✅
Block 4 (CINEMATOGRAPHY):    T1 (oppressive wide) — space compresses → TENSION ✅
Block 5 (ENVIRONMENT):       Institutional surfaces, fluorescent leakage → TENSION ✅
Block 6 (BRAND INTEGRATION): No warmth — teal reads cold in this light → TENSION ✅
Block 7 (NEGATIVE PROMPT):   "No warmth, no symmetry, no softness, no invitation" ✅

COMPRESSION SCORE: 7/7 → MAXIMUM DENSITY
Collapse test: Remove Block 3 (lighting). The hostility loses physical grounding.
The image becomes narratively strong but physically ungrounded. → COLLAPSE ✅
```

---

### Law 4 — The Visual Authenticity Gate

**Axiom:** *A visual prompt's value is inversely proportional to how interchangeable it is with another coach's image.*

**What it does:** Runs 4 authenticity checks on the completed prompt before it is approved for image generation. Catches technically VFS-compliant prompts that would still produce generic coaching B-roll.

**The 4 Visual Authenticity Checks:**

```
CHECK 1: The Universal Illustration Test
  "Could this image illustrate ANY coach's story in this general niche?"
  → YES = REJECT. The prompt has no irreducible uniqueness.
           It describes a coaching moment, not THIS coach's moment.
  → NO  = PASS

CHECK 2: The Brand Avatar Dependency Test
  "Does this image require knowledge of THIS coach's Brand Avatar
   physical DNA to generate correctly?"
  → NO  = REJECT. The image could feature any person and work the same way.
           It's decorative, not narrative.
  → YES = PASS (mahogany skin in cold institutional light is a specific
           statement about THIS body in THIS world)

CHECK 3: The Transcript Mapping Test
  "Does the image contain a visual element that maps to a SPECIFIC
   verbatim quote and timestamp in the coach's transcript?"
  → NO  = REJECT. The image is AI-imagined. No first-party moment
           anchors it to the actual story.
  → YES = PASS (the gripping hands map to "[exact quote] 00:02:14")

CHECK 4: The Self-Recognition Test
  "If the coach saw this image, would they recognize their own FEELING
   in it — not their face, but the emotional truth of their specific moment?"
  → NO  = REJECT. The image is technically accurate but emotionally generic.
           It looks like a coaching moment. It doesn't feel like HER moment.
  → YES = PASS (the image achieves the recognition bridge)
```

**The Authenticity Gate vs. VFS:**  
VFS scores: character consistency, T-Code, V-Code, lighting preset, brand compliance (technical).  
Authenticity Gate scores: irreducible uniqueness, brand dependency, transcript anchoring, self-recognition (emotional).  
Both scores are required. A prompt that passes VFS but fails the Authenticity Gate produces an image that the algorithm accepts and the audience discounts.

---

## Section 3: Output Format — Authenticated Prompt File

Every approved prompt `.txt` file carries its law compliance summary in the header:

```
=== SC01_HOOK_T2I.txt ===
MODE: TENSION | VFS: 87/100 | AUTHENTICITY: 4/4 ✅ | COMPRESSION: 6/7 ✅
Transcript anchor: "[exact coach quote]" @ 00:00:03
Brand Avatar: [coach name] — mahogany skin, teal sweater, dining space
Law compliance: SAT✅ | MODE-COHERENCE✅ | COMPRESSED✅ | AUTH-GATE✅

[PRIMAL ANALYSIS]
PHYSICAL REALITY: [felt specific — friction verb class]
INNER WORLD: [felt specific — mode-justified emotional texture]
METAPHYSICAL: [mode-justified gap/threshold language]
AUTHENTICITY MARKERS: [Brand Avatar verbatim]
ENVIRONMENT: [insider-specific setting]
TIMESTAMP: "[exact verbatim quote]" @ HH:MM:SS
BRAND INTEGRATION: [exact hex + placement rule]

[PROMPT BLOCK]
...
[NEGATIVE PROMPT — Mode-directional]
...
```

---

## Section 4: Evaluation — 5 Micro-Hypothesis Tests

### MH1 — The Felt Specificity Test
**Hypothesis:** "Every PRIMAL Analysis block contains at least one detail that could not describe any other coach in any other moment — the input is first-party saturated."  
**Test:** Apply the Felt Specificity Gate to every PRIMAL field: PHYSICAL REALITY, INNER WORLD, METAPHYSICAL, AUTHENTICITY MARKERS, ENVIRONMENT. Identify any field containing summary language rather than sensory precision.  
**Pass condition:** 0 fields contain summary language. Every field has ≥1 detail that is irreducibly specific to this coach, this scene, this moment.

### MH2 — The MODE Coherence Test
**Hypothesis:** "If shown the generated image without audio or context, ≥7 of 10 people would use vocabulary from the correct emotional mode."  
**Test:** Simulate or evaluate against the Cross-Layer Coherence Test vocabulary lists (TENSION/VULNERABILITY/RECOGNITION). For each completed prompt, verify that the image description — extracted from mode-justified block choices — aligns with the correct vocabulary cluster.  
**Pass condition:** Projected coherence ≥7/10 based on block-level MODE justifications. If any block uses language from a different mode's vocabulary (e.g., "warmth" in a TENSION scene), the prompt fails coherence and returns to Law 2.

### MH3 — The Compression Yield Test
**Hypothesis:** "At least 5 of the 7 prompt blocks justify their choices through the assigned MODE's biological logic — not just by selecting from the technical preset."  
**Test:** Apply the Compression Count to every completed prompt. For each block, determine: JUSTIFIED (the biological reason is stated) or SELECTED (the preset was applied without rationale).  
**Pass condition:** ≥5/7 blocks JUSTIFIED. Prompts scoring 4/7 or lower are thin — technically valid but emotionally uncompressed. They return to Law 3 for MODE-justification rewriting.

### MH4 — The Authenticity Gate Yield
**Hypothesis:** "100% of prompts approved for image generation pass all 4 Visual Authenticity Checks."  
**Test:** Apply the 4 checks to every completed prompt: Universal Illustration Test, Brand Avatar Dependency, Transcript Mapping, Self-Recognition.  
**Pass condition:** 4/4 checks passed per prompt, 100% of prompts. A single prompt failing even one check is rejected from image generation — it would produce an interchangeable image regardless of VFS score.

### MH5 — The Pipeline Closure Test
**Hypothesis:** "The completed image generation prompt carries traceable inheritance from every upstream distillation stage (H0→H13) — the full funnel is verifiably closed."  
**Test:** For each approved prompt, trace its lineage: (a) Does the INNER WORLD field contain language from the SoC `mode_arc` (`ccf-26/skills/ccf/production/soc-generator/SKILL.md`)? (b) Does the AUTHENTICITY MARKERS field reference the Brand Avatar verbatim? (c) Does the TIMESTAMP field contain a verbatim quote from the final script (`scripts/final/{blueprint_id}_script.md`)? (d) Does the MODE assignment match the beat's `downstream_routing` from `content_blueprints.json`?  
**Pass condition:** All 4 lineage traces are present and verified. If any link in the H0→H5 chain is broken, the prompt is not a distillation output — it is an improvisation built on partial inputs.

---

## Section 5: H5 Validation Receipt

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ H5 DISTILLATION RECEIPT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Session:             [Date] — [Coach Name] — [Project ID]
H13 Receipt:         ✅ Found (Asset library verified, all beats covered)
H3 Receipt:          ✅ Found (mode_arc populated: T/V/R sentences present)
Scene Count:         [n] scenes
Prompts Generated:   [n] .txt files

VISUAL SATURATION GATE:
  PRIMAL felt specificity passed:  ✅ ([n]/[n] fields with 0 summary language)
  Brand Avatar verbatim embedded:  ✅
  Transcript quotes anchored:      ✅ (all scenes have HH:MM:SS timestamp)
  soc_output mode_arc loaded:      ✅

LAW EXECUTION:
  Law 1 — Visual Saturation:       ✅ PASSED (0 summary-language PRIMAL fields)
  Law 2 — MODE Coherence:          ✅ ([n]/[n] prompts ≥7/10 projected coherence)
  Law 3 — Compression:             ✅ ([n]/[n] prompts ≥5/7 blocks MODE-justified)
  Law 4 — Authenticity Gate:       ✅ ([n]/[n] prompts pass all 4 checks)

VFS SCORES:
  Average VFS:                     [x]/100
  Prompts ≥75 VFS:                 [n]/[n] ✅

MICRO-HYPOTHESIS EVALUATION:
  MH1 Felt Specificity:           ✅ PASS (0 summary-language fields)
  MH2 MODE Coherence:             ✅ PASS (≥7/10 projected per prompt)
  MH3 Compression Yield:          ✅ PASS ([n]/[n] at ≥5/7)
  MH4 Authenticity Yield:         ✅ PASS (100% prompts — 4/4 checks)
  MH5 Pipeline Closure:           ✅ PASS (H0→H5 lineage verified in all prompts)

OUTPUT:
  Storyboard prompt files:         ✅ [n] .txt files created
  Mode distribution:               T:[n] | V:[n] | R:[n]
  All files law-compliant:         ✅

FUNNEL CLOSURE CONFIRMATION:
  H0 → H1 → H6/H7 → H3 → H13 → H5: ✅ COMPLETE
  Full distillation receipt chain: H0✅ H1✅ H6/H7✅ H3✅ H13✅ H5✅

VERDICT: ✅ H5 DISTILLATION COMPLETE — CLEARED FOR IMAGE GENERATION
         THE CCF DISTILLATION FUNNEL IS VERIFIED CLOSED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BLOCKED STATES (if any check failed):
  ❌ Summary-language PRIMAL field → Extract from final script (`scripts/final/`) + soc_output.
     No prompt is written on thin inputs.
  ❌ MODE coherence <7/10 → Rewrite block-level choices with explicit MODE justification.
  ❌ Compression <5/7 → Return to Law 3. Force each block to name its biological rationale.
  ❌ Any authenticity check fails → No image generation. The prompt is generic regardless of VFS.
  ❌ Pipeline closure broken → Identify which upstream receipt is missing. Halt and repair.
```

---

## Architectural Constants

| Constant | Value | Rationale |
|:---------|:------|:----------|
| PRIMAL summary-language tolerance | 0 | One thin field contaminates the entire prompt's saturated-input guarantee |
| MODE coherence threshold | ≥7/10 viewers | Below 7/10, the image is mode-ambiguous — it cannot predictably deliver its emotional function |
| Compression minimum | ≥5/7 blocks | More than half the blocks must serve the MODE actively — passive selection is not compression |
| VFS minimum | ≥75 | Existing technical standard — maintained alongside law compliance |
| Authenticity gate | 4/4 required | All 4 checks are non-negotiable. One failure produces interchangeable imagery |
| Pipeline closure | H0→H5 lineage traced | The only proof the Distillation Funnel executed from start to finish |

---

## Complete Funnel Receipt Chain

With H5 complete, the full CCF Distillation Funnel is documented and verifiable end-to-end:

| Stage | Receipt | Law Set | Key Gate |
|:------|:--------|:--------|:---------|
| **H0** | H0 Distillation Receipt | 4 Laws of Layered Questions | Unpredictability Gate (4 checks) |
| **H1** | H1 Distillation Receipt | 4 Laws of Content Distillation | Collapse Test + Unpredictability Gate |
| **H6/H7**| H6/H7 Distillation Receipt| 4 Laws of Research Distillation | Provenance Gate (4 checks) |
| **H3** | H3 Distillation Receipt | 4 Laws of Voice Distillation | Alchemy Activation Gate (≥7/10) |
| **H13**| H13 Distillation Receipt| 4 Laws of Visual Search Distillation | Semiotic Authenticity Gate (4 checks) |
| **H5** | H5 Distillation Receipt | 4 Laws of Visual Distillation | Visual Authenticity Gate (4 checks) |

**The pipeline is law-governed at every stage — and every stage generates a receipt that the next stage requires. The chain cannot break silently.**

---

## Referenced CCF Skills & Commands

| Type | Name | Path |
|:-----|:-----|:-----|
| **Skill** | Art Director | `ccf-26/skills/ccf/distribution/art-director/SKILL.md` |
| **Skill** | Visual Recipes (14 skills) | `ccf-26/skills/ccf/distribution/visual-recipes/*/SKILL.md` |
| **Skill** | SoC Generator (upstream H3) | `ccf-26/skills/ccf/production/soc-generator/SKILL.md` |
| **Skill** | Script Generator (upstream) | `ccf-26/skills/ccf/production/script-generator/SKILL.md` |
| **Skill** | Blueprint Orchestrator (upstream H1) | `ccf-26/skills/ccf/research/blueprint-orchestrator/SKILL.md` |
| **Skill** | Question Engineer (upstream H0) | `ccf-26/skills/ccf/content/question-engineer/SKILL.md` |
| **Command** | ccf-visual | `commands/ccf-visual.md` |
