# H14: The 4 Laws of Mirror Adaptation (Stage 2) — Implementation Architecture

**Hypothesis:** If we govern the Mirror Session with four strict adaptation laws, then the resulting adapted prompt will force Stage 3 to generate highly specific, coach-authentic content, because the prompt itself will constrain the LLM from making generic choices downstream.

**Core Insight:** Prompt Adaptation fails when it relies on *instructions* rather than *injections*. The 4 Laws shift the mechanism from "tell the LLM how to act" to "inject constraints it cannot escape."

**Pipeline Position:** CCF Production Phase → Stage 2 (after SoC, before Wisdom Forge)  
**Existing Infrastructure:** `mirror-session/SKILL.md` (983 lines, v4, laws partially integrated)  
**Gap Classification:** MEDIUM — Laws exist in the skill but lack testable gates and receipts  
**Dependency:** Receives base archetype prompt, SoC output JSON, Coach Voice DNA; produces adapted prompt

---

## Section 1: Input Saturation Gate

Before the Mirror Session can adapt any prompt, the following inputs must be verified:

| Input | Minimum Quality Standard | Source | If Missing |
|:------|:------------------------|:-------|:-----------|
| Base Archetype Prompt | Must be unmodified from master library — zero alterations | `intelligence/archetype_prompts/` | ⛔ HALT — archetype integrity compromised |
| SoC Output JSON | Must have `mode_arc` fully populated (T+V+R sentences present) | H3 output via `/ccf-soc-generate` | ⛔ HALT — no voice material to inject |
| Coach Voice DNA | Must have vocabulary (L2/L3 depth), metaphor system, temperature arcs | `soul_values.json` (H8) | ⛔ HALT — adaptation produces generic voice |
| H3 Receipt | Must exist and STATUS ≠ FAILED | `scripts/soc/H3_DISTILLATION_RECEIPT.md` | ⛔ HALT — SoC output not law-validated |
| Blueprint mode assignment | T/V/R primary mode for this content piece | H1 output | FLAG — adaptation runs mode-blind |

**Saturation test:** If SoC JSON contains < 3 hook examples, < 4 body examples, or < 2 CTA examples → the SoC was thin. Mirror Session proceeds but flags LOW_SATURATION.

---

## Section 2: The 4 Laws of Mirror Adaptation

### Law 1 — The Law of Traceable Origins (Anti-Hallucination)

**Axiom:** *"If the LLM invents examples, it invents generic averages. Every injected element must trace to a source document."*

Every specific example injected into the upgraded prompt MUST be directly traceable to the SoC output or the coach's Voice DNA blueprint:

- `contextual_examples` in Hook zone → must exist in `soc_json.contextual_examples.hook_examples[]`
- `contextual_examples` in Body zone → must exist in `soc_json.contextual_examples.body_examples[]`
- `contextual_examples` in CTA zone → must exist in `soc_json.contextual_examples.cta_examples[]`
- Voice constraints → must trace to `soul_values.json` fields
- Emotional vocabulary → must be extracted from transcripts, not generated

**The adapter cannot "make up" a good hook — it must FIND the hook in the coach's stream of consciousness.**

**Micro-Hypothesis Test (MH1):** Select 5 injected examples from the adapted prompt. Each must have a source reference in `soc_output.json` or `soul_values.json`. **5/5 traceable = PASS. < 5/5 = FAIL.**

### Law 2 — The Law of Uncomfortable Specificity (Anti-Abstraction)

**Axiom:** *"'Authenticity' is an abstract concept that generates cliché output. 'The feeling of lying to clients for 6 months while drowning in $40k of debt' is an uncomfortable specificity that generates resonance."*

When defining emotional temperature, vocabulary, or targeted pain points for the adapted prompt:

```
SPECIFICITY TEST (per injected constraint):

  ABSTRACT (FAIL):
    Core Value: "Integrity"
    Pain Point: "Fear of failure"
    Vulnerability: "Being authentic"
  
  SPECIFIC (PASS):
    Core Value: "The moment I realized my integrity was costing me my marriage"
    Pain Point: "Lying awake calculating if the next client payment covers rent"
    Vulnerability: "I smiled while losing everything behind that smile"
```

**The test:** Every injected constraint must be a SCENE or a HIGHLY DEFINITIVE PHRASE — never a single word, never a category.

**Micro-Hypothesis Test (MH2):** Select 3 injected constraints. Apply the "Could this describe ANY coach?" test. **YES = FAIL. NO = PASS.**

### Law 3 — The Law of Structural Persistence (Anti-Corruption)

**Axiom:** *"The base archetypes have proven narrative architecture. Adaptation means injection, not replacement."*

The core storytelling mechanics and reasoning logic of the Base Archetype Prompt must remain 100% intact:

```
STRUCTURAL PERSISTENCE RULES:
  1. ZERO deletions from the base archetype text
  2. ZERO modifications to original instructions
  3. Adaptation applies ONLY via dedicated "Injection Zones":
     - #### VOICE PHYSICS ENFORCEMENT (Hook Zone)
     - #### VOICE PHYSICS ENFORCEMENT (Body Zone)
     - #### VOICE PHYSICS ENFORCEMENT (CTA Zone)
     - #### FINAL SCRIPT VALIDATION FRAMEWORK
  4. Injection zones are APPENDED after original archetype sections
  5. The base prompt's narrative structure (hook → value promise → body → CTA)
     remains the structural skeleton — injections add muscle, not replace bones
```

**Micro-Hypothesis Test (MH3):** Diff the adapted prompt against the base archetype. **ZERO deletions or modifications to core instructions = PASS. Any modification = FAIL.**

### Law 4 — The Law of Hard Validation Gates (Anti-Drift)

**Axiom:** *"We cannot expect Stage 3 to output perfect voice on the first try. The adapted prompt must include an automated internal critic."*

The Mirror Session constructs a 3-Layer Validation Framework using coach-SPECIFIC parameters:

```
LAYER 1: RED FLAG DETECTOR
  Populated with THIS coach's specific red flags:
  - Banned phrases: [extracted from voice DNA]
  - Vocabulary ceiling: [profanity comfort level]
  - Structural violations: [patterns this coach NEVER uses]

LAYER 2: HUMANITY MARKER DETECTOR
  Populated with THIS coach's human tells:
  - Stammer pattern: [specific pattern from transcripts]
  - Backtrack format: [how they self-correct]
  - Thought trails: [how they trail off]
  - Filler words: [specific words, frequency]

LAYER 3: TURING TEST SIMULATION
  Populated with THIS coach's identity markers:
  - Signature closing: [their specific sign-off]
  - Weird specifics: [times, amounts, images they reference]
  - Repetition patterns: [what they repeat for emphasis]
```

**Micro-Hypothesis Test (MH4):** Does the adapted prompt append a validation checklist populated with coach-SPECIFIC metrics (not generic "sounds authentic")? **Coach-specific = PASS. Generic = FAIL.**

---

## Section 3: Blocked States

| State | Condition | Action |
|:------|:---------|:-------|
| `BLOCKED_NO_SOC` | H3 receipt missing or FAILED | HALT — cannot adapt without voice material |
| `BLOCKED_THIN_SOC` | SoC has < 3 hook, < 4 body, or < 2 CTA examples | Proceed with LOW_SATURATION flag |
| `BLOCKED_NO_VOICE_DNA` | `soul_values.json` missing or incomplete | HALT — adaptation will be generic |
| `BLOCKED_NO_ARCHETYPE` | Base archetype prompt not found in library | HALT — nothing to adapt |
| `DEGRADED_NO_MODE` | Blueprint mode assignment missing | Proceed mode-blind — flag in receipt |

---

## Section 4: 5 Micro-Hypothesis Evaluations

**MH1 — Traceability Test:** Select 5 injected examples. Each must trace to `soc_output.json` or `soul_values.json`. 5/5 = PASS.

**MH2 — Specificity Test:** Select 3 injected constraints. Apply "Could this describe ANY coach?" test. All NO = PASS.

**MH3 — Structural Integrity Test:** Diff adapted vs. base archetype. Zero deletions/modifications = PASS.

**MH4 — Validation Gate Quality:** Adapted prompt contains coach-specific (not generic) validation checklist = PASS.

**MH5 — Draft Protocol Result:** Did the micro-draft (Phase 1) of one injection zone pass before full adaptation? PASS/FAIL + discovery logged.

---

## Section 5: Validation Receipt

```
H14 VALIDATION RECEIPT
━━━━━━━━━━━━━━━━━━━━━━
Blueprint:       [ID]
Archetype:       [type]
Coach:           [name]
Date:            [timestamp]
H3 Receipt:      [STATUS from upstream]
Saturation:      [FULL | LOW_SATURATION]

LAW COMPLIANCE
━━━━━━━━━━━━━━
Law 1 — Traceable Origins:       [5/5 examples traced]  [PASS/FAIL]
Law 2 — Uncomfortable Specificity: [3/3 constraints specific]  [PASS/FAIL]
Law 3 — Structural Persistence:  [0 deletions, 0 modifications]  [PASS/FAIL]
Law 4 — Hard Validation Gates:   [coach-specific checklist present]  [PASS/FAIL]

MICRO-HYPOTHESES
━━━━━━━━━━━━━━━━
MH1 Traceability:       [PASS/FAIL]
MH2 Specificity:        [PASS/FAIL]
MH3 Structural Integrity: [PASS/FAIL]
MH4 Validation Quality: [PASS/FAIL]
MH5 Draft Protocol:     [PASS/FAIL] — discovery: [if any]

DRAFT PROTOCOL LOG
━━━━━━━━━━━━━━━━━━
Micro-draft:     [1 injection zone tested — result]
Atomic test:     [3 zones tested — mode diversity result]

STATUS: [AUTHENTICATED / PROVISIONAL / FAILED]
```

---

## Integration with Existing SKILL.md

These 4 laws are already PARTIALLY integrated into `ccf-26/skills/ccf/production/mirror-session/SKILL.md` (983 lines, v4). The upgrade adds:

1. **Input Saturation Gate** → new INGEST pre-flight section
2. **5 MH Tests** → embedded in the VALIDATE phase
3. **Validation Receipt** → emitted during CHECKPOINT
4. **Blocked States** → handled in INGEST phase
5. **Draft Protocol** → runs on 1 injection zone during REASON phase before full adaptation
