# SWOT Analysis: H12 (Visual Recipe Distillation) & H13 (Standalone Visual Asset Research)

**Document Type:** SWOT Analysis — System Thinking & First Principles  
**Scope:** Two proposed visual-layer hypotheses for the CCF pipeline  
**Decision:** Architecture choice, shared vs. separated protocols, build priority  
**Date:** 2026-02-22  
**Updated:** 2026-02-22 — Corrected H13 scope, analyst scaling, pipeline timing, semiotics removal

---

## 0. System Context — Where H12 and H13 Sit

The CCF pipeline produces visual content posts. Every post is visual. The current architecture has two parallel visual tracks, both activated **only after content is validated:**

```
RESEARCH LAYER (H6 + H7)
  1 Deep Analyst (for selected archetype) → Deep Research Brief (1000-1200 words)
  1 Fresh Analyst (for selected archetype) → Fresh Research Brief (1000-1200 words)
         ↓
SCRIPT LAYER (existing)
  Script Generator → Script → VALIDATED script
         ↓ (only after validation)
VISUAL LAYER — TWO PARALLEL TRACKS
  Track A: 14 Visual Recipes → AI-generated visual prompts → Image generation (H12 governs this)
  Track B: Visual Asset Research → Real found images → Ready-to-use editor assets (H13 governs this)
```

> [!IMPORTANT]
> **Pipeline gate:** ALL visual production (both Track A and Track B) only begins after the script is validated. Nothing visual is produced before content validation.

**H12** governs **Track A — Visual Recipes** — the 14 specialized skills that transform validated scripts into AI-generated visual prompts. These recipes exist and function, but have no distillation laws, no input quality gates, and no validation receipts.

**H13** governs **Track B — Standalone Visual Asset Research** — a post-validation step that finds and curates real visual assets from research (actual images, cultural references, vibe baits) that the editor can use alongside AI-generated visuals. These are **not inputs to the AI visual recipes** — they are a separate, parallel output track providing the editor with ready-to-use alternatives.

The question is: **how should these two hypotheses be architected, and do they share a protocol?**

---

## 1. H12 — Visual Recipe Distillation Laws

### 1.1 Current State

14 Visual Recipe skills exist in `skills/ccf/distribution/visual-recipes/`. Each produces JSON-structured visual prompts with:

- ~~**Strategic semiotic injection** — facial expressions from `facial_expression_lexicon` injected at climax scene only~~ **(DEPRECATED — see Section 6)**
- **Style selection** — Ghibli / Mixed / Cinematic Realism based on emotional angle
- **Brand Avatar injection** — physical DNA from `soul_values.json` injected into every person-based prompt
- **Scene structure** — 3/4/5 scenes depending on archetype complexity
- **Character casting** from `character_lexicon` with age selection

### 1.2 SWOT: H12

#### Strengths

**S1. Mature skill architecture.** The 14 recipes are fully built (150-250 lines each), archetype-specialized, and follow a consistent structure (Step 1→7 with output JSON schema). This is not a gap that requires building from zero — it requires upgrading what exists.

**S2. Natural distillation law pattern.** The recipes already perform implicit distillation: script→emotional analysis→character casting→scene structure→output. The existing workflow maps cleanly onto the 4-law pattern (saturation→mode→compression→authenticity gate). The laws would formalize what the recipes already attempt informally.

**S3. Shared protocol is architecturally native.** The research layer already uses this exact pattern — `_DEEP_RESEARCH_PROTOCOL.md` shared across 41 analysts, `_FRESH_RESEARCH_PROTOCOL.md` shared across 41 analysts. Adding a `_VISUAL_RECIPE_DISTILLATION_PROTOCOL.md` shared across 14 recipes follows the established CCF convention.

**S4. Brand Avatar DNA is already injected.** The CCF Addition section at the bottom of each recipe already injects the brand avatar's physical description. This means visual consistency infrastructure exists — the distillation laws would extend it to emotional consistency, not replace it.

#### Weaknesses

**W1. No visual input quality gate.** The recipes take a validated script as input, but there's no verification that the script contains enough visual information to produce rich scenes. A script might be linguistically powerful but visually barren — all abstract claims, no concrete imagery. The recipe would then produce generic visuals because the input gave it nothing specific to work with.

**W2. No tribe visual code verification.** The recipes reference `cultural resonance` in their quality standards but have no mechanism to verify that the generated visuals use codes the tribe would recognize vs. codes that would alienate them.

**W3. Style selection is fixed per archetype.** "Nostalgia = Ghibli, Shocking = Cinematic Realism" is a rigid mapping. The tribe's visual culture should inform style selection, not just the archetype category.

**W4. Semiotic injection creates trust-killing comparison traps.** (See Section 6 — this is flagged for removal, not improvement.)

#### Opportunities

**O1. Visual Authenticity Gate.** A distillation law that tests every visual prompt for originality and emotional clarity. The test: "Does this visual invite comparison to a known reference?" If yes, REJECT. "Does it express the emotion through text description alone, without copying recognizable faces or meme formats?" If yes, PASS.

**O2. Script-to-Visual Saturation Test.** Before the recipe begins, test the validated script for visual density: How many concrete, filmable moments does it contain? How many sensory details? If below threshold, the recipe requests a visual enrichment pass rather than producing generic visuals from abstract content.

**O3. Cross-recipe emotional coherence.** A shared protocol could enforce that all 14 recipes produce visuals that are emotionally consistent with the blueprint's MODE (from H1). A Nostalgia Story recipe and a Nostalgia Listicle recipe producing visuals for the same blueprint should feel emotionally coherent — warm, specific cultural objects — even though their scene structures differ.

**O4. Compression law across scenes.** Currently, recipes produce 3-5 scenes without testing whether each scene carries unique emotional weight. A compression law would require that removing any scene from the sequence creates a perceptible gap in the emotional arc. No decorative scenes.

#### Threats

**T1. Over-engineering disrupts existing workflow.** The 14 recipes work. Adding 4 distillation laws per recipe without carefully scoping the shared protocol could turn a functional system into a bureaucratic one. The laws must accelerate creative output, not slow it down.

**T2. Tribal visual codes are hard to operationalize.** The Soul Tribe Profile (H9) may not produce visual codes at the specificity level that a Visual Authenticity Gate requires. If the gate depends on H9 output that doesn't yet exist at sufficient depth, H12 becomes blocked on H9.

**T3. Style rigidity vs. creative freedom.** Distillation laws that are too prescriptive about style selection could eliminate the art director agent's creative discretion. The laws must constrain the emotional truth of the output without prescribing the exact visual execution.

---

## 2. H13 — Standalone Visual Asset Research

### 2.1 Current State & Corrected Scope

H13 is **not** a bridge between research briefs and visual recipes. It is a **separate, post-validation production step** that produces standalone visual assets for the editor.

**What H13 produces:** Real, research-verified images and visual references that the editor can use as-is — cultural objects, vibe baits, trending visual references, nostalgic artifacts, editorial photography. These are **alternative assets** that exist alongside AI-generated visuals from the visual recipes.

**When H13 runs:** Only after the blueprint is confirmed, the script is written, and the **content is validated.** H13 is a production-phase operation, not a research-phase operation.

**What H13 does NOT do:** H13 does NOT feed into visual recipes. It does NOT modify research analyst output. It does NOT add visual tags to text briefs. It is a separate parallel track.

### 2.2 SWOT: H13

#### Strengths

**S1. Clear production-phase identity.** H13 runs only when content is validated and entering production. This means it doesn't add complexity to the research or scripting phases. It operates in a clean, bounded scope.

**S2. Research already contains visual intelligence — it just doesn't find the actual assets.** The Deep and Fresh Research Briefs already reference cultural moments, historical events, trending topics, and tribal experiences. H13 takes these references and hunts for the real visual assets — actual images, real photographs, cultural artifacts — that correspond to them.

**S3. Editor empowerment.** The editor receives two parallel visual tracks: AI-generated visuals (from recipes) and real found assets (from H13). This gives creative flexibility — some posts work better with AI visuals, others with authentic found imagery, and the best posts combine both.

**S4. Trust advantage.** Real visual assets carry inherent authenticity. An actual photograph of a cultural moment cannot be compared to an AI reference and tagged as "slop." Found assets are immune to the uncanny valley problem that plagues AI-generated content.

#### Weaknesses

**W1. Research-to-asset gap is large.** A research brief might mention "the 1980s kitchen experience" — but finding a specific, high-quality, rights-cleared image of that exact cultural reference requires targeted visual search capability that doesn't currently exist as a formalized skill.

**W2. Asset quality is unpredictable.** Unlike AI generation where you control the output quality through prompt engineering, found assets vary in resolution, style, framing, and emotional tone. The editor must curate from whatever is available.

**W3. Rights and licensing complexity.** Real images have rights considerations. The asset research protocol needs clear guidelines on what constitutes usable imagery (public domain, Creative Commons, editorial use, etc.).

**W4. Archetype-specific visual needs vary widely.** A Nostalgia Story needs period-specific photography. A Shocking Listicle needs dramatic real-world documentation. A Funny Relatable Comparison needs cultural meme references. One generic "find images" protocol won't serve all 14+ archetypes equally.

#### Opportunities

**O1. Archetype-specialized search protocols.** H13 could have archetype-specific search directives (similar to how the 41 deep analysts are archetype-specialized). "For Nostalgia Stories, search for: period photography, cultural objects from the tribe's era, 'you remember this?' visual triggers." "For Shocking Listicles, search for: dramatic statistics visualized, before/after documentation, scale-revealing photography."

**O2. Vibe bait curation.** Fresh Research already surfaces trending cultural moments. H13's visual search can specifically target currently trending visual references that the audience would recognize immediately — creating instant engagement through visual recency.

**O3. Asset library accumulation.** Over time, H13 builds a coach-specific visual asset library. Assets found for one blueprint may be relevant to future blueprints. This creates a compounding resource that becomes more valuable with each production cycle.

**O4. Mode-typed asset organization.** Found assets can be tagged by emotional mode (TENSION / VULNERABILITY / RECOGNITION), making it easy for the editor to select the right asset for the right emotional beat in the content.

#### Threats

**T1. Search quality depends on query intelligence.** If the visual search queries are generic ("African woman cooking"), the found assets will be generic stock imagery — defeating the purpose. The search queries must be as specific and insider-level as the research brief itself.

**T2. Scope creep into rights management.** If H13 takes responsibility for rights verification, it becomes a legal-operational task, not a creative-research task. The protocol should focus on finding the best assets and flagging rights status for editorial decision.

**T3. Diminishing returns for abstract content.** Content about abstract concepts (mindset, philosophy, spiritual practices) produces fewer findable real-world assets than content about concrete experiences (cooking, migration, motherhood). H13 will naturally be more productive for some archetypes than others.

---

## 3. System Thinking: The Interaction Between H12 and H13

### 3.1 The Corrected Architecture

H12 and H13 operate as **parallel tracks**, not a sequential pipeline:

```
VALIDATED SCRIPT
  │
  ├── Track A (H12): Visual Recipes → AI-generated visual prompts
  │     Governed by: Visual Recipe Distillation Laws
  │     Output: Multi-scene AI visual prompts with validation receipt
  │
  └── Track B (H13): Visual Asset Research → Real found images
        Governed by: Visual Asset Research Protocol
        Output: Curated asset collection (mode-typed, provenance-linked)
  │
  └── Both tracks → Editor receives parallel visual options
```

**H12 and H13 do NOT feed each other.** They are independent production tracks triggered by the same event (script validation) and consumed by the same person (the editor).

### 3.2 Shared Protocol Decision

**First-principles answer:** H12 and H13 should **NOT share a protocol.** They are fundamentally different operations:

| Aspect | H12 (AI Visual Generation) | H13 (Real Asset Research) |
|:-------|:--------------------------|:------------------------|
| **Operation** | Generate prompts for AI image creation | Search and curate real existing images |
| **Output** | Text prompts → AI renders | Actual image files/URLs |
| **Quality control** | Prompt engineering + distillation laws | Search query quality + curation judgment |
| **Trust model** | Must avoid comparison traps (Section 6) | Inherently authentic — real images |
| **Archetype specialization** | Recipe-level (14 recipes) | Search-directive-level (could mirror 14+) |

**The only shared element:** Both tracks should produce outputs tagged with emotional mode (T/V/R) so the editor can combine Track A and Track B assets by emotional beat.

### 3.3 Build Independence

Unlike the H6-H11 dependency chain, H12 and H13 have **no mutual dependency.** They can be built in any order or in parallel:

- **H12** can be built and tested with the 14 existing recipes, using only validated scripts as input (which is what they already use).
- **H13** can be built as a new skill that takes validated scripts + research briefs and produces standalone visual asset collections.

Neither blocks the other.

---

## 4. Build Priority

### 4.1 Recommendation

| Priority | Hypothesis | Rationale |
|:---------|:----------|:---------|
| **Build first** | **H12 — Visual Recipe Distillation** | Upgrades 14 existing, functioning skills with laws. Immediate quality improvement. No new infrastructure needed. |
| **Build second** | **H13 — Visual Asset Research** | New skill to build. Requires defining search protocols per archetype. Higher build cost, but provides a fundamentally new asset type. |

**H12 first** because it improves what already runs. H13 second because it adds a net-new capability that requires more design work (archetype-specific search directives, asset curation criteria, mode-typing schema).

---

## 5. Risk Summary

| Risk | Severity | Mitigation |
|:-----|:---------|:-----------|
| Over-engineering 14 recipes | Medium | Shared protocol keeps per-recipe additions minimal |
| H13 search queries too generic | High | Archetype-specific search directives, informed by research brief |
| Asset rights complexity | Medium | Flag rights status in output, don't make H13 responsible for legal clearance |
| Style rigidity in H12 | Medium | Laws constrain emotional truth, not visual style |
| H13 thin for abstract content | Low | Expected and acceptable — some archetypes are naturally more visual |

---

## 6. Architectural Decision: Semiotics Removal

> [!CAUTION]
> **This is a trust-critical architectural change that affects all 14 visual recipes.**

### The Problem

The current visual recipes include a "Strategic Semiotic Injection" system:
- `facial_expression_lexicon` — a library of recognizable facial expressions from known references
- `memetic_reference_prompt` — injected at the climax scene to evoke a specific emotional response
- `character_lexicon` — character casting based on recognizable archetypes

### Why It Must Be Removed

**The Comparison Trap Principle:** Any AI-generated visual that invites comparison to a known reference will be judged by the discrepancy, not by the quality. The brain doesn't evaluate "how good is this?" — it evaluates "how far is this from the real thing?" Every deviation is scored as artificiality.

**The trust mathematics:**
- **Without semiotic reference:** Viewer sees an original character, an original expression. No comparison target. The brain evaluates the image on its own terms: "Does this feel authentic?"
- **With semiotic reference:** Viewer's brain loads the real reference (a famous person's expression, a viral meme format). Every pixel is compared. The AI can never win — it can only lose by varying degrees. Each discrepancy is tagged as SLOP, killing trust.

### The New Philosophy

> **Never give people references that make your output be compared and tagged with AI-generated.**

The LLM is intelligent enough to understand and reproduce emotions from text description alone. The semiotic library was useful for early-stage AI image generation where models struggled with emotional expression from text. Current models do not have this limitation.

### What Changes

| Component | Current State | After Removal |
|:----------|:-------------|:-------------|
| `facial_expression_lexicon` | Referenced in all 14 recipes | **Deprecated.** Emotional expressions described in natural text. |
| `memetic_reference_prompt` | Injected at climax scene | **Removed.** Climax scene described with felt specificity, no external reference. |
| Semiotic injection step | Step 6 in every recipe | **Replaced** with emotional escalation verification (text-based). |
| Character casting | May reference known archetypes | **Original characters only.** No recognizable face templates. |

### Impact on H12

H12's distillation laws should **encode this removal** as a negative law:

**Law of Visual Originality:** No visual prompt shall contain references to recognizable persons, meme formats, or facial expression templates that invite comparison to known sources. Every character is original. Every emotion is described, not referenced. The test: "If the viewer Google Image Searches the person in this visual, will they find a match?" If yes, REJECT.

---

*Pending: User decision on build order for H distillation law implementation documents.*
