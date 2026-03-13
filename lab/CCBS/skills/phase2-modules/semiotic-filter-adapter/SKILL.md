---
name: semiotic-filter-adapter
description: "Takes the Design Brief and produces a domain-adapted Semiotic Filter configuration that translates literal text into psychological, visual, or cultural symbols appropriate for the target Skill's output domain."
category: ccbs/phase2-modules
tier: 2
discovery:
  input_type: "skill_design_brief"
  output_type: "adapted_module_json"
  module_name: "Semiotic Filter"
  phase: "adapt"
depends_on: []
similar_to:
  - distillation-funnel-adapter
  - contrastive-anchor-adapter
compose_with: []
estimated_tokens: 2000
execution_tier: "Deep/Premium"
reasoning_modules:
  - type: "Ecological Adaptation"
    adaptation: "Defines the literal-to-symbolic translation axes for the target domain, preventing direct translation that feels heavy-handed or cliché."
---

# 🧬 Module-Skill: Semiotic Filter Adapter

## Intent
To define how the Semiotic Filter's 3-axis translation (Literal → Subtext → Cultural Signifier) manifests in the target Skill's specific output domain. The Semiotic Filter prevents the common failure of direct, literal translation that feels heavy-handed or produces cliché output.

## Target
A JSON object containing the adapted Semiotic Filter configuration with domain-specific translation rules, signifier libraries, and anti-cliché constraints.

## Context
Required for Skills that produce visual prompts, metaphors, cultural references, B-Roll search queries, or any output where direct literal expression is a failure mode. NOT required for data extraction, analysis, or structural transformation Skills.

## Trigger
Skill Assembler sends this Skill the Design Brief JSON.

## Inputs
1. `skill_design_brief` (Object — the full 11-field approved brief)

---

## ⚙️ The Core DNA (Universal — from Reasoning Modules Ecology §4.D)

```
Axis 1: LITERAL MEANING     — What the text explicitly says.
Axis 2: THE SUBTEXT          — What the text emotionally implies without saying it.
Axis 3: THE CULTURAL SIGNIFIER — The visual, auditory, or symbolic object that represents the subtext without stating it.
```

---

## ⚙️ The Adaptation Protocol

### Axis 1: Literal Meaning Identification
1. **What kind of literal content does this Skill process?** Coach statements? Research findings? Client testimonials? Trend data?
2. **What is the surface-level interpretation trap?** The most common way an LLM would directly translate this content without semiotic depth.
3. **What abstraction level should the Skill start from?** (Word-level? Sentence-level? Paragraph-level? Thematic?)

### Axis 2: Subtext Definition
1. **What emotional, psychological, or philosophical subtext does this domain carry?** In coaching content: the lived experience beneath the advice. In visual search: the mood/atmosphere beneath the literal description. In data: the human implication beneath the statistic.
2. **Define 3-5 subtext categories for this domain.** Each category is a type of "hidden meaning" the filter should surface:
   - E.g., Visual domain: Intimacy, Power, Fragility, Defiance, Solitude
   - E.g., Coaching domain: Suppressed Fear, Performed Confidence, Genuine Discovery, Protective Anger
3. **For each category, provide a 1-sentence operational definition** that allows consistent classification.

### Axis 3: Cultural Signifier Translation
1. **What output modality does this Skill produce?** (Visual prompts? Metaphors? Audio direction? Search queries?)
2. **Define the signifier library for this domain.** For each subtext category, what are the concrete, non-cliché cultural objects that represent it?
   - E.g., "Intimacy" ≠ stock photo of couple holding hands → kitchen counter with flour dust, a child's shoe by a door, a crumpled handwritten note
   - E.g., "Power" ≠ suit + handshake → welding sparks, worn leather work gloves, a chess clock at 00:03
3. **Define the anti-cliché gate.** What are the 5 most overused signifiers in this domain that MUST be banned?

---

## 🚫 Negative Space (Constraints)
*   **NO Direct Translation:** If Axis 3 output is a literal description of Axis 1, the filter has failed. The translation must pass through subtext.
*   **NO Stock Signifiers:** The anti-cliché gate is mandatory. Every domain has its own version of "diverse professionals smiling at laptops."
*   **NO Empty Subtext Categories:** Each subtext category must have at least 2 non-cliché signifier examples.

---

## 📦 Output Artifact
**Format:** JSON
**Schema:**
```json
{
  "module_name": "Semiotic Filter",
  "adapted_for_skill": "string",
  "adaptation": {
    "axis_1_literal": {
      "content_type": "string (what kind of literal content)",
      "surface_interpretation_trap": "string (the obvious direct-translation failure)",
      "abstraction_level": "word|sentence|paragraph|thematic"
    },
    "axis_2_subtext": {
      "subtext_categories": [
        {
          "category": "string",
          "definition": "string (1-sentence operational definition)"
        }
      ]
    },
    "axis_3_signifier": {
      "output_modality": "string (visual prompts | metaphors | audio direction | search queries)",
      "signifier_library": [
        {
          "subtext_category": "string",
          "signifiers": ["string (concrete, non-cliché cultural objects)"]
        }
      ],
      "anti_cliche_gate": ["string (5 banned overused signifiers)"]
    }
  },
  "adaptation_reasoning": {
    "axis_1_q1": "string", "axis_1_q2": "string", "axis_1_q3": "string",
    "axis_2_q1": "string", "axis_2_q2": "string", "axis_2_q3": "string",
    "axis_3_q1": "string", "axis_3_q2": "string", "axis_3_q3": "string"
  }
}
```

## 🏁 Success Criteria
1. JSON validates against schema.
2. `axis_2_subtext.subtext_categories` contains 3-5 categories, each with an operational definition.
3. `axis_3_signifier.signifier_library` has ≥2 signifiers per subtext category, all non-cliché.
4. `axis_3_signifier.anti_cliche_gate` contains exactly 5 banned signifiers.
5. All 9 `adaptation_reasoning` fields are populated.
