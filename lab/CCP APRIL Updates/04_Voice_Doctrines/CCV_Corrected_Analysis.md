# CCV Corrected Analysis — Grounded in Actual Codebase

> **Session:** 2026-04-15 | **Context:** Corrections to initial CCV analysis after deep reading of actual SKILL.md files, Design Briefs, and Script Prompts
>
> **Correction notice:** The initial analysis used generic archetype examples instead of the actual 76 Script Prompts, ignored the Script_Generation_Skill_Type_Guide_v1, and dismissed CMF agents as not needing training without reading any of their SKILLs. This document corrects all of that.

---

## 1. Skills Are NOT Removed — They Become Leaner

**This is the correct framing.** Here's the precise relationship:

| Layer | Role | Example from Codebase |
|---|---|---|
| **Skill (SKILL.md)** | The TEACHER — authoritative reasoning architecture, structural laws, quality gates, negative space, causal construction sequence | `achievement-story-design-brief-v1.2.yaml` (1057 lines of pure reasoning architecture) |
| **LoRA** | The STUDENT — learns to execute the Skill's reasoning patterns with consistency, speed, and reduced token cost | Trained on successful compilation traces where the Design Brief produced outputs that passed all SG-01 through SG-08 gates |
| **Activation Steering** | The MOOD KNOB — fast-changing surface layer (style, formality, emotional register) that doesn't need retraining | The `psych-routing-adapter` behavior across Processing/Escape/Discovery/Status modes |

**What gets leaner:** The prompt payload at compilation time. Right now, the Builder Engine loads the entire Design Brief + DEP-ENG-004 + DEP-ENG-003 + DEP-ENG-006 + DEP-ENG-021 + all adapters. That's 2,300+ tokens of structural instruction.

**What stays:** The Skill itself stays as the source of truth. You still develop, test, and iterate on Skill files. But the deployed model has INTERNALIZED the reasoning patterns, so the prompt can shrink from "here's the full reasoning architecture" to "execute Achievement Story, axis: challenger × discovery × 0.8 intensity × developing audience."

**The workflow becomes:**
1. **Develop** the massive Skill prompts (exactly as done now)
2. **Test** them on bigger/more expensive models (Gemma-4-31B, Claude Opus 4.6)
3. **Record** the successful compilation traces (input → reasoning → output)
4. **Fine-tune** the smaller execution model (Qwen-3.5) on those traces
5. **Deploy** with lean prompts + LoRA weights + Activation Steering

The bigger model acts as the teacher during testing. The smaller LoRA model learns to replicate the teacher's behavior. The Skill itself is the curriculum.

---

## 2. The Script_Generation_Skill_Type_Guide IS the Reasoning Trace Architecture

The Skill Type Guide v1 is not just "trying to engineer reasoning" — it already IS a full reasoning trace specification with 6 mandatory competencies:

| Section | What It Specifies | Reasoning Trace It Produces |
|---|---|---|
| **Section I: 8 Architectural Mandates** | M1-M8 non-negotiable laws (Anti-Draft at 3 levels, CRAL wiring, Negative Space first, Ghost Variable prohibition, Phase-specific falsifiable laws) | **Validator traces:** "M7 check: Is Level 1 Anti-Draft written as prose? YES/NO" |
| **Section II: 3-Layer SPR Loading Protocol** | Negative Space → Positive Space → Contextual Intelligence loading order | **Loading traces:** "Layer 1: DEP-ENG-004 loaded FIRST. Layer 2: DEP-ENG-003 loaded. Layer 3: DEP-ENG-016 → DEP-ENG-021 → DEP-ENG-006" |
| **Section III: Anti-Draft 3-Level Architecture** | Level 1 (archetype centroid as prose), Level 2 (mood × archetype failure), Level 3 (coach-specific DEP-ENG-004) | **Contrastive traces:** "Generic centroid: 'I worked incredibly hard...' → Distance metric: 0.87" |
| **Section IV: Causal Construction Sequence** | 5-step per-phase: Cognitive Function → DEP Source → Structural Law → CRAL Source Mapping → SG Gate | **Phase construction traces:** "Phase 1 Stakes: Cognitive Function = audience occupies emotional reality. Primary DEP = DEP-ENG-010. CRAL = M2 + M3. SG-06 written." |
| **Section V: CRAL Wiring Protocol** | 7 moments mapped to arc phases, 3 decision tests, 5 Builder Tests | **Routing traces:** "M2_BELIEVABLE → Stakes_phase. M5_SURPRISING → Turn_phase." |
| **Section VI: Emotional DNA Integration Test** | T1-T5 promotion gate | **Validation traces:** "T1 PASS, T2 PASS, T3 PASS, T4 PASS, T5 PASS → TESTED" |

This is already a structured cognitive dataset spec. When you fine-tune, you're not inventing a new reasoning format — you're serializing what the Skill Type Guide already mandates into training examples.

### What fine-tuning adds that the Skill alone can't:

The Skill Type Guide specifies the WHAT. Fine-tuning teaches the model the HOW — the specific weight-level patterns that consistently pass SG-01 through SG-08 without needing 2,300 tokens of instruction.

**The Skill Type Guide is the driving manual. Fine-tuning is the 10,000 hours of practice that makes the driver stop reading the manual while driving.**

---

## 3. Reasoning Model vs. Instruct Model — Where Each Goes

### The Split, Mapped to the Actual Pipeline

| Pipeline Stage | Model Type | Why | Existing Architecture Equivalent |
|---|---|---|---|
| **CRAL Research** (M1-M7 moment finding) | **Reasoning** (Gemma-4-31B, NO LoRA) | Needs to think strategically about tribal intelligence, prediction gaps, optimal incongruity. No voice identity needed. | The 7-moment CRAL research is analysis, not coach-voice output |
| **Causal Construction** (Skill Type Guide Section IV) | **Reasoning** (Gemma-4-31B, NO LoRA) | Needs to determine cognitive function per phase, identify primary DEP source, write falsifiable structural laws. Pure analytical work. | This is the Builder/Analyst work — it designs the brief |
| **SPR Loading + Generation** (actual script writing) | **Instruct + LoRA** (Qwen-3.5, WITH Voice DNA LoRA) | Needs to EXECUTE the brief in the coach's voice. Must sound like the coach, not like a reasoning engine. | This is the Assembler/Artisan work — it writes the output |
| **SG Gate Validation** (SG-01 through SG-08) | **Reasoning** (Gemma-4-31B, NO LoRA) | Needs to evaluate whether the generated output passes falsifiability tests. Analytical judgment, not voice execution. | This is the Critic Subagent work |

### The key insight on "conditioning the reasoning itself"

The Skill Type Guide's Section IV (Causal Construction Sequence) IS conditioned reasoning. Each step has:
- A specific question to answer
- A decision tree
- A format requirement
- A failure test

When you fine-tune a reasoning model on these structured traces, you're not letting it reason freely — you're teaching it to reason WITHIN the construction framework. The LoRA doesn't override the centroid — it replaces it with the framework.

But the critical rule stays: **The reasoning model NEVER generates the final coach-voiced output.** It produces the structured plan. The instruct model with Voice DNA LoRA writes the actual words.

---

## 4. Few-Shot Examples + Activation Steering

**Not dumb — but scope it to archetype FAMILY, not individual archetype.**

The 76 Script Prompts in `Script Prompts/` already group into families:
- **Story Family:** Achievement, Discovery, Inspiration, Connection, Nostalgia, etc. (13 Generative Story variants)
- **Comparison/Contrast Family:** Funny Relatable, Nostalgia, Outrageous, Shocking, Surprising (5 Comparison variants)
- **Case Study Family:** FOMO, Inspirational, Intriguing, Relatable, Social Proof, Surprising (6 Case Study variants)
- **Reaction Family:** Nostalgia, Outrage, Validation (3 Reaction variants)
- **Tier List Family:** Authority, Controversial, Red Flag, Relatable (4 Tier List variants)
- **Meme Family:** Benign Violation, Incongruity, Relief, Superiority (4 Meme variants)

Activation Steering with few-shot calibration at the **family** level makes sense:
- "This is what Story Family outputs look like at THIS coach's style" → 2-3 examples per family
- The individual archetype within the family is handled by the LoRA weights + the axis controls

---

## 5. CMF Agents — Corrected. They Need Training.

After reading the actual skills, the initial assessment was completely wrong. Here's what was found:

### The `witness-composer` (16KB SKILL.md) — 8 Assembly Rules with Pseudocode

This is not a simple routing agent. It has:
- **Rule 0:** Artificial VAE Decoder Protocol (4-step reasoning chain: SEMANTIC_CHECK → SHADOW_FILTER → ANTI-CLICHÉ_GATE → EXECUTE)
- **Rule 3:** Conditional Quote Stacking with density thresholds, stacking trigger logic, and super-cut preferences
- **Rule 5:** MCDA Template Matching with template_match_score computation
- **Rule 6:** Sequence Affinity Prioritization with chain evaluation
- **Rule 8:** Bookend Check with polarity inversion detection

Every one of these rules involves cognitive judgment that would benefit from LoRA training.

### The `gmg-expert-02` (23KB SKILL.md) — 4-Step Visual Reasoning Protocol

This is a 426-line instruction set for visual prompt generation with:
- **STEP 0:** Beat Cluster Context interpretation (VCP → emotion → frozen pose → weather element)
- **STEP 2:** Elemental Library Application (5 weather-to-emotion mappings)
- **STEP 4:** Prompt Synthesis (character anchor + weather + pose + typography + texture)
- **Quality Gates:** 9 binary checks before output

### The `cmf-editor` (27KB SKILL.md) — 13-Class Edit Taxonomy

This has a full deterministic routing matrix (13 edit classes × 7 routing properties). The Copilot (EC-13) classifies natural language into edit classes and generates JSON Patches.

### Revised CMF Training Priority

| Skill Family | Training Priority | Reasoning |
|---|---|---|
| **Motion Skills** (GMG Expert 01-06) | **P0 — Train first** | These generate visual prompts that become the video's visual identity. Consistency is CRITICAL. |
| **E-Roll Skills** (13 deep-researcher variants) | **P0 — Train alongside motion** | Finding the RIGHT found clip for the RIGHT narrative beat is enormous cognitive precision. |
| **Composers** (13 arc-specific composers) | **P1 — Train second** | Quote stacking, bookend checks, MCDA template matching — all learnable cognitive patterns |
| **Video Editor/Copilot** (EC-13 classification) | **P1 — Train second** | Natural language → Edit Class classification is a perfect LoRA target |
| **Manifest Assembler** | **P2 — Defer** | Mostly deterministic (frame math, transition lookup). Keep at prompt level |
| **Pipeline Commander** | **P2 — Defer** | Orchestration logic, not cognitive judgment. Keep at prompt level |

---

## 6. The 76 Script Prompts vs. The Design Brief v1.2

These are two different evolutionary stages of the same thing:

| Aspect | Legacy Script Prompt | Design Brief v1.2 |
|---|---|---|
| **Size** | ~100 lines | 1,057 lines |
| **Reasoning depth** | Generic 3-act structure | 5-phase Causal Construction with CRAL moment mapping per phase |
| **Anti-Draft** | None | 3-level (prose centroid + mood × archetype failure + coach-specific DEP-ENG-004) |
| **Research integration** | Simple "DEEP + FRESH research" separation | Full 7-moment CRAL wiring (M1-M7) with use_at addresses per arc phase |
| **Validation** | 5-item checklist (subjective) | 8 SG gates (SG-01 through SG-08, each binary falsifiable) |
| **Voice DNA** | "Analyze {Conscious_Soul_Values}" (vague) | 3-layer SPR loading protocol with explicit DEP IDs |
| **Psychological routing** | None | 4 mood states × 3 regulatory frames × 3 audience cohorts with full adapter specifications |

Both are valuable training data:
- **Legacy prompts:** Training data for the "understand the archetype's intent" layer
- **Design Briefs:** Training data for the "execute with architectural precision" layer

The legacy prompts should NOT be updated to match the Design Briefs. Instead:
1. Keep them as **archetype intent calibration** data
2. Use them alongside peak-expression outputs as **Activation Steering calibration** samples
3. The Design Briefs remain the **authoritative execution specifications**

---

## Summary: The Architecture After CCV Integration

```
┌──────────────────────────────────────────────────────────────────┐
│                     SKILL FILES (Stay Full)                      │
│  Script_Generation_Skill_Type_Guide + Design Briefs + CMF Skills │
│  └── These are the TEACHER. You develop, test, iterate on them.  │
└────────────────────┬─────────────────────────────────────────────┘
                     │ Generate successful compilation traces
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│                CCV TRAINING DATASET (New)                         │
│  Traces: input → reasoning → output WITH axis labels             │
│  Negatives: Anti-Draft Level 1 prose centroids as DPO negatives  │
│  Sources: Design Brief fields + Skill reasoning + SG gate results│
└────────────────────┬─────────────────────────────────────────────┘
                     │ Fine-tune
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│              DEPLOYED STACK (Lean Prompts)                        │
│                                                                  │
│  Reasoning Model (Gemma-4-31B, clean)                            │
│  ├── CRAL Research (M1-M7)                                       │
│  ├── Causal Construction (Section IV)                            │
│  └── SG Gate Validation (Critic)                                 │
│                                                                  │
│  Execution Model (Qwen-3.5 + Voice DNA LoRA)                    │
│  ├── Script Generation (SPR → Coach Voice)                       │
│  └── CMF Agent Tasks (Composition, Visual Reasoning, Edit Class) │
│                                                                  │
│  Activation Steering (RISER, per family)                         │
│  ├── Style modulation (mood × register)                          │
│  └── Archetype family calibration (2-3 few-shot per family)      │
│                                                                  │
│  Residual Prompts (~500 tokens, structural only)                 │
│  └── "Execute Achievement Story, axis: X, audience: Y, CRAL: Z" │
└──────────────────────────────────────────────────────────────────┘
```

The Skills stay massive. The prompts get lean. The model gets precise. And the architecture already in place (Skill Type Guide + Design Briefs + CMF Skills) IS the training curriculum — no need to invent new data structures. Just serialize what already exists into training format.
