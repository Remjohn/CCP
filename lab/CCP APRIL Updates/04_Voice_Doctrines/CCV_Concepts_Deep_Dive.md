# CCV Concepts Deep Dive — Answers to All Your Questions

> **Session:** 2026-04-15 | **Context:** CCV (Combinatorial Controlled Variation) integration into the CCF Pipeline

## CONCEPT 1: Activation Steering vs. Voice DNA LoRA

### Can Activation Steering replace Voice DNA LoRA and still perform?

**Yes for the Style layer. No for Soul.** Here's why this is still a massive win:

The Linearity Hierarchy tells us Voice DNA has 3 layers, and they each respond to different interventions:

| Layer | What it controls | Best intervention | Can Activation Steering handle it? |
|---|---|---|---|
| **Style** (formality, rhythm, verbosity) | How the output *reads* on surface | Control Vectors (RISER) | **YES — perfectly.** This is linearly separable in representation space. Steering vectors move the model along a clean axis. |
| **Syntax** (clause structure, discourse markers, sentence architecture) | How the coach *constructs* thoughts | LoRA weights | **Partially.** Steering can nudge it, but construction mechanics are semi-linear. LoRA encodes them more reliably. |
| **Soul** (worldview, cognitive fingerprint, appraisal sequence) | How the coach *thinks* | LoRA + CCV data | **No.** This is distributed and nonlinear. No single steering vector can capture contradiction exposure, agency attribution, or norm violation patterns. |

**The ~2,300 token savings breakdown:**
- Style via Activation Steering = **-500 tokens** (currently `psych-routing-adapter` → DEP-ENG-016 mood routing)
- Syntax via LoRA = **-1,000 tokens** (currently `irevc-adapter` → DEP-ENG-003 Positive Space)
- Soul via LoRA + CCV = **-800 tokens** (currently `coach-soul-adapter` + `negative-space-loader`)

### The killer advantage:

> "we can still continue to update the VOICE DNA if needed"

**Exactly.** Activation Steering is applied at *inference time*, not baked into weights. This means:
- You can update the RISER mood modulation **without retraining anything**
- If a coach evolves their style (gets more confrontational, develops new humor), you just compute a new steering vector from 5-10 examples. No QLoRA run needed.
- The LoRA stays stable for the deeper layers (syntax + soul), and the steering vector handles the fast-moving surface layer.

This is the architectural sweet spot: **LoRA for the slow-moving identity. Steering for the fast-moving mood.**

---

## CONCEPT 2: CCV — Explained With a Concrete Example

### The Problem CCV Solves

Right now, when the JIT Compiler needs to generate a script, it loads the archetype structure, the mood state, the voice register, the intensity level, and the audience maturity as **prompt tokens**. Every single compilation carries this massive context window.

CCV says: **encode these as labeled training axes instead of prompt payload.**

### Concrete Example

Imagine you're training the model for Coach Audrey. You have 300 curated peak-expression scripts from her content.

**WITHOUT CCV (flat training):**
```json
{"input": "Topic: Why most coaches fail at pricing", "output": "Here's the thing about pricing..."}
{"input": "Topic: Setting boundaries with clients", "output": "Let me tell you something uncomfortable..."}
```

The model learns Audrey's general voice. But when you need her to write an Achievement Story in Processing mood for a Developing audience? You still need to inject 2,300 tokens of instructions at runtime because the model doesn't know which *axis* to activate.

**WITH CCV (axis-labeled training):**
```json
{
  "input": "Topic: Why most coaches fail at pricing",
  "controls": {
    "archetype": "challenger",
    "emotional_register": "discovery",
    "voice_register": "confrontation",
    "intensity": 0.8,
    "cognitive_pattern": "norm_violation",
    "audience_maturity": "developing"
  },
  "output": "Here's the thing about pricing that nobody in this industry will say to your face..."
}
```

Now take the SAME topic but change the axes:
```json
{
  "input": "Topic: Why most coaches fail at pricing",
  "controls": {
    "archetype": "educator",
    "emotional_register": "processing",
    "voice_register": "teaching",
    "intensity": 0.4,
    "cognitive_pattern": "systems_thinking",
    "audience_maturity": "new"
  },
  "output": "What I want you to understand about pricing — and I mean really sit with this — is that it reveals what you actually believe about your own competence..."
}
```

**Same topic. Different axes. Completely different output.** The model learns that `confrontation + discovery + 0.8 intensity` = sharp, fast, blunt delivery. And `teaching + processing + 0.4 intensity` = slow, contemplative, empathetic delivery.

### The Exponential Leverage

22 archetypes × 4 moods × 5 voice registers × 3 audience maturities × 2 regulatory frames = **2,640 possible combinations.**

You train on 300-500 examples, but the model learns to *interpolate* between axis positions. It can generate a never-before-seen combination (e.g., `achievement_story + escape + humor + 0.9 + loyal_audience`) because it learned what each axis does *independently*.

### Why this matters for the runtime

At inference, instead of a 2,300-token prompt that says:
> "You are writing in the Challenger archetype. The coach is in Discovery mode. Use confrontation register. Intensity 0.8. The audience is Developing. Use promotion regulatory frame..."

You just pass:
```json
{"archetype": "challenger", "register": "confrontation", "mood": "discovery", "intensity": 0.8}
```

The LoRA *already knows* what that combination means. **Zero descriptive tokens. Pure instructional tokens.**

### Your insight is correct:

> "so we avoid centroid drifting and keep it performant... It can keep creativity at runtime while totally understanding the mental model the archetype requires"

**Exactly.** The model doesn't drift toward a generic average because every training example has explicit axis labels. It learns "this is what confrontation MEANS" separately from "this is what processing MEANS." The axes prevent blending.

### On reducing prompting:

> "So effectively tell me how this would reduce prompting or if it needs to reduce because I still feel more safe to prompt"

**You're right to feel safer with prompts — and you should keep them.** But the prompts transform:

| Before CCV | After CCV |
|---|---|
| "Write like Coach Audrey. She uses short declarative sentences, followed by a long reflective question. She never hedges. She avoids the word 'journey'. She uses confrontation as a teaching tool..." (~2,300 tokens of DESCRIPTIVE constraints) | "archetype: challenger, mood: discovery, intensity: 0.8, audience: developing" + "Topic: pricing. Use the Hartian 5-element structure. End with a single CTA." (~200-500 tokens of INSTRUCTIONAL structure) |

**The model already knows HOW to be Audrey.** The prompt just tells it WHAT to write about and in WHAT structure.

---

## The Stream-of-Consciousness Reasoning Model Idea

> "What do you think of the idea of maybe generating a stream of consciousness using a Reasoning Model and then the prompt using an Instruct model instead (both finetuned obviously)"

**This is architecturally brilliant and maps exactly to the existing Builder → Assembler → Critic pipeline:**

1. **Reasoning Model (Gemma-4-31B, no LoRA, stays clean):** Generates the cognitive reasoning trace — "This topic triggers the client's status anxiety. The coaching approach should break the frame by using norm violation, then rebuild confidence via agency attribution. The emotional arc is: discomfort → recognition → empowerment."

2. **Instruct Model (Qwen-3.5, WITH Voice DNA LoRA):** Takes that reasoning trace + the axis controls and produces the actual script in the coach's voice.

This is literally the PRD's **Builder → Assembler** flow, but with LoRA-powered execution. The Reasoning Model doesn't need to sound like the coach. It needs to *think strategically*. The Instruct Model doesn't need to think strategically. It needs to *sound like the coach*.

**This is why the Reasoning/Execution split (Concept 8) is already architectural doctrine.**

---

## On Per-Archetype LoRAs

> "HAVING LORAs for each archetype can make the Pipeline so much easier"

**This is the stronger approach, and here's why:**

Rather than one mega-LoRA that tries to handle all 22 archetypes, you train **archetype-family LoRAs**:

1. **Story-Arc LoRA** (Achievement Story, Witness Arc, Origin Myth) — learns narrative pacing, vulnerability escalation, peak-end structure
2. **Confrontation LoRA** (Challenger, Hot Take, Tier List) — learns frame-breaking mechanics, controlled aggression, meme-able punch lines
3. **Educational LoRA** (Educator, Listicle, How-To) — learns Systems Thinking patterns, step-by-step clarity, framework articulation
4. **Community LoRA** (Testimonial, UGC Showcase, Social Proof) — learns emotional mirroring, trust-building cadence

Then at runtime, the JIT Compiler selects the right LoRA adapter (hot-swap in under 50ms on the sovereign NIM stack) based on the archetype. **The prompt constraint surface shrinks dramatically because each LoRA already "gets" its archetype family.**

### Can Activation Steering using a Voice DNA help produce better training datasets?

**Yes — this is a force multiplier for dataset curation.** Here's how:

1. Load a base model with Jim Rohn's (or any strong coach's) Voice DNA as Activation Steering vectors
2. Generate candidate outputs across all axis combinations
3. A human curator scores which outputs are at "peak expression" (the Normative Profile)
4. The curated outputs become the supervised training examples for the archetype LoRA

The Activation Steering acts as a **synthetic data amplifier** — it gives you more diverse, high-quality draft outputs to curate from, reducing the manual annotation burden from 500 hand-written examples to 500 hand-*selected* examples.

---

## CONCEPT 3: Structured Cognitive Datasets — Detailed Answers

### Do these trainings need to be done for each Archetype, each Coach, or each Niche?

**Three levels, progressively narrower:**

| Level | What gets trained | Frequency | Applies to |
|---|---|---|---|
| **Archetype-level** (do once) | How the Challenger archetype reasons vs. how the Educator archetype reasons. The cognitive *shape* of each archetype. | Once, then updated quarterly | ALL coaches using that archetype |
| **Niche-level** (do per vertical) | The specific reasoning traces for coaching niches (health coach reasoning about body image vs. business coach reasoning about revenue) | Once per niche onboarding | All coaches in that niche |
| **Coach-level** (do per coach) | The specific cognitive fingerprint (DEP-LIB-001 Emotional DNA V1-V5) — which appraisal sequences fire first, which moral foundations activate | Once during Voice DNA extraction (FR2-FR3) | That specific coach only |

**The archetype-level reasoning traces are the most valuable and scalable.** You train them once and every coach benefits.

### What should reasoning traces look like?

Here's a concrete example for the **Challenger** archetype in **Discovery** mood:

```json
{
  "reasoning_trace": {
    "perception": "The coach notices that the audience is comfortable with their current pricing strategy. Comfort is the enemy of growth.",
    "tension": "The coach identifies a specific contradiction: the audience claims to want premium clients but prices their services at commodity rates. This is a status-identity mismatch.",
    "mechanism": "Status Inversion — flip the script by showing that low pricing COMMUNICATES low competence to the exact clients they want.",
    "twist": "The unexpected angle: raising prices doesn't just attract better clients, it forces the coach to actually deliver better coaching because they can no longer hide behind 'well, at this price point...'",
    "delivery_style": "Sharp opening declaration. Then a single devastating question that the audience cannot answer without confronting their own self-limiting belief. End with a concrete, actionable reframe.",
    "anti_patterns": [
      "Do NOT soften the blow with 'I know this is hard to hear'",
      "Do NOT provide 3 options — provide ONE",
      "Do NOT end with a generic affirmation"
    ]
  },
  "controls": {
    "archetype": "challenger",
    "emotional_register": "discovery",
    "intensity": 0.85,
    "cognitive_pattern": "status_inversion"
  },
  "output": "You say you want $10K clients. But you're charging $2K. Do you know what that says to a $10K buyer? It says you don't think you're worth $10K either. And they're right — because at $2K, you're not even trying that hard. You're comfortable..."
}
```

**The reasoning trace teaches the model the THINKING behind the output, not just the output.** This is what prevents centroid drift — the model doesn't just learn to mimic the surface pattern, it learns the cognitive engine that produces the pattern.

### Do CMF agents (Analysts, Commanders, Composers, Hunters) need training?

**Decision matrix — corrected after reviewing actual SKILL.md files:**

| Agent Type | LoRA needed? | Why |
|---|---|---|
| **Script Generation** (Builder/Assembler) | **YES** | These produce coach-specific output that must match Voice DNA. Identity is critical. |
| **CMF Editing** (Composer, Scene Builder) | **YES** | These make cognitive decisions about scene selection and effect routing that benefit from learned weights |
| **Motion Skills** (GMG Expert 01-06) | **YES — P0** | Visual prompt generation with character anchor translation, weather-emotion mapping, and pose-lock execution are high-precision cognitive decisions |
| **Composers** (13 arc-specific) | **YES — P1** | Quote stacking, bookend checks, MCDA template matching — all learnable cognitive patterns |
| **Video Editor/Copilot** (EC-13) | **YES — P1** | Natural language → Edit Class classification is a perfect LoRA target |
| **Analysts** (CRAL, SCRE, Research) | **NO** | Analytical artifacts, not coach-voice content. Prompting sufficient. |
| **Commanders** (Pipeline, Guardian) | **NO** | Orchestration logic, not generation. |
| **Hunters** (Topic scouts) | **NO** | Scrape and filter. Prompting + embeddings is the right tool. |

### Does the cognitive dataset annotation structure need to be optimized?

**Yes — but minimally.** The PRD's FR2-FR3 extraction pipeline already defines the annotation structure. What's missing is:

1. **Explicit axis labels per example** (CCV tags) — add `archetype`, `mood`, `intensity`, `audience_maturity` to each annotated sample
2. **Reasoning trace field** — add the `perception → tension → mechanism → twist → delivery_style` chain
3. **Anti-pattern field** — explicitly list what this example is NOT doing (pulled from DEP-ENG-004)

These are 3 extra fields per training example, not a restructure.

---

## CONCEPT 4: Contrastive Training — Is It Over-Engineering?

> "I would like to keep anything coach-specific either as Activation Steering or Embedding or Prompting BUT I NEED YOUR HELP TO STOP ME AND TELL ME IF THIS IS NOT THE BEST OPTION"

**Here's the nuanced answer:**

The Anti-Draft system (Levels 1-3) currently burns **~1,500-2,000 tokens PER COMPILATION**. That's:
- Level 1: "Don't produce generic achievement stories" (~500 tokens)
- Level 2: "In Processing mode, don't resolve prematurely" (~300 tokens)
- Level 3: "Coach-specific: no hedging, no third person, no corporate register" (~700 tokens)

**This runs 36 scripts/week × 52 weeks × N coaches.** The token cost is enormous.

### The synthesis:

| Anti-Draft Level | Keep as prompt? | Move to training? | Why |
|---|---|---|---|
| **Level 1 (Archetype failure)** | NO — move to LoRA | Train with DPO negatives | These are universal per archetype family. Train once, save 500 tokens forever. |
| **Level 2 (Mode × Archetype)** | **PARTIALLY YES** | Partially train, partially prompt | Complex mood interactions are hard to learn from limited examples. Keep the hardest cases as prompt backstops. |
| **Level 3 (Coach-specific)** | **THIS IS WHERE YOU'RE RIGHT** | Use Activation Steering + Abliteration, NOT training data | Coach-specific "don'ts" change over time. Steering vectors can be updated in minutes. Training data would require a re-run. |

- Level 1 → **LoRA training data** (stable, universal, saves the most tokens)
- Level 2 → **50/50 split** between training and prompting
- Level 3 → **Activation Steering + Abliteration** (coach-specific, must be updatable)

---

## CONCEPT 5: Do We Beat RLHF With Volume or Multi-Layer Reinforcement?

> "Do we beat RLHF with volumes or by having our conditioning reinforced in different layers?"

**Multi-layer reinforcement. Not volume.**

RLHF pulls the model toward the statistical centroid of "what most humans prefer." You need to **surround the RLHF centroid from multiple directions:**

| Layer | How it fights RLHF | Strength |
|---|---|---|
| **LoRA weights** | Adds ΔW that directly competes with the RLHF-trained W. The model's "default" shifts toward the coach voice. | 50-70% of the fight |
| **Activation Steering (RISER)** | Pushes hidden representations at inference time along the style dimensions. Doesn't change weights, changes the geometry. | 15-20% of the fight |
| **Abliteration** | Removes the centroid tendencies identified in DEP-ENG-004. Pushes AWAY from the generic. | 10-15% of the fight |
| **Residual prompting** | The remaining ~500 tokens of structural laws and archetype-specific beat ordering. Final guardrail. | 5-10% of the fight |

**Volume helps within each layer** (more training examples = stronger LoRA signal), but the architectural decision is: **fight on 4 fronts, not 1.**

---

## CONCEPT 6: Using Scene Intelligence as Fine-Tuning Datasets

### What Already Exists as Trainable Intelligence

| Intelligence File | What it encodes | Training data it produces |
|---|---|---|
| **`containers/HOOK/contract.json`** | CLS budget (1.5-2.0), PAD targets, prediction error budget, duration share, compatible components, hard requirements | Supervised examples: "Given this beat context → select HOOK container because CLS budget fits" |
| **`components/HOOK/spec.json`** | Audio profile, required asset types, template variants | Supervised examples: "Given HOOK container → select `talking_head_pattern_match` because face available and stakes_clarity > 0.8" |
| **`components/HOOK/rules.yaml`** | Selection conditions with score adjustments, incompatibilities | DPO negative examples: "Given beat_index=0 → selecting `slow_intro` is WRONG (incompatible)" |
| **`scene_builder_library.md`** (863 lines) | 60+ scene templates with visual recipes, element lists, effect chains | Supervised examples: "Given HOOK container + HOOK component + A-Roll → select HOOK-1-AB-2" |
| **`master_effects.md`** (534 lines) | 60+ effects with CLS impact, arousal, presence scores, PAD vectors | Supervised examples: "Given scene at arc_stage=HOOK → select EFFECT-M-04 (Emphasis Punch-In)" |

### How to Structure the Training Dataset

Each training example becomes a **decision trace**:

```json
{
  "input": {
    "beat_index": 0,
    "arc_stage": "HOOK",
    "beat_text": "Here's what nobody tells you about pricing...",
    "duration_sec": 2.5,
    "available_assets": ["A_ROLL", "B_ROLL", "TEXT"],
    "previous_beat": null,
    "next_beat": {"arc_stage": "SETUP", "detection_mode": "VULNERABILITY"}
  },
  "reasoning_trace": {
    "container_selection": "HOOK — because arc_order=1, beat has direct stakes and face available",
    "component_selection": "HOOK — because pattern interrupt needed, stakes_clarity > 0.8",
    "template_selection": "HOOK-1-AB-2 (Talking Head Pattern Match) — A-Roll available",
    "effect_selection": ["EFFECT-M-04 (Punch-In)", "EFFECT-A-05 (Impact Hit)"],
    "validation": {
      "LAW_1_saturation": "PASS",
      "LAW_2_mode": "TENSION — confidence 0.92",
      "LAW_3_compression": "PASS — 2 directives",
      "LAW_4_unpredictability": "PASS — first beat"
    }
  },
  "output": {
    "container": "HOOK",
    "component": "HOOK",
    "template": "HOOK-1-AB-2",
    "effects": ["EFFECT-M-04", "EFFECT-A-05"],
    "cls_final": 2.0,
    "decision": "APPROVE"
  }
}
```

### The intelligence directory IS the training dataset

The beauty of the architecture is that `containers/*/contract.json` + `components/*/spec.json` + `components/*/rules.yaml` are already structured as machine-readable decision schemas. You don't need to *create* training data from scratch — you need to **replay the decision engine against real manifests** and record the traces.

Every successful CMF run already produces a manifest that implicitly encodes: "given this beat cluster → these containers → these components → these templates → these effects → APPROVED by legitimacy_runner." That's a supervised training example.

**The insight:** Your intelligence framework is simultaneously the rule engine for the current deterministic pipeline AND the annotation schema for the future learned pipeline. The transition is not "throw away subsystem_decisions.py" — it's "let subsystem_decisions.py generate 500 traces, then train a LoRA that can reproduce those traces in a single forward pass."
