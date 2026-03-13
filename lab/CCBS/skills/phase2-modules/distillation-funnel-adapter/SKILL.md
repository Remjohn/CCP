---
name: distillation-funnel-adapter
description: "Takes the Design Brief's domain context and the generic Distillation Funnel Core DNA, and produces an ecologically adapted Funnel configuration specific to the target Skill's environment."
category: ccbs/phase2-modules
tier: 2
discovery:
  input_type: "skill_design_brief + module_core_dna"
  output_type: "adapted_module_json"
  module_name: "Distillation Funnel"
  phase: "adapt"
depends_on: []
similar_to:
  - contrastive-anchor-adapter
  - deliberation-adapter
compose_with: []
estimated_tokens: 3000
execution_tier: "Deep/Premium"
reasoning_modules:
  - type: "Ecological Adaptation"
    adaptation: "Mutates the 4-Law Distillation Funnel DNA to fit the specific domain context from the Design Brief."
---

# 🧬 Module-Skill: Distillation Funnel Adapter

## Intent
To take the universal 4-Law Distillation Funnel blueprint and produce a domain-specific mutation that is calibrated to the target Skill's unique environment. The adapter guarantees that "Compression" and "Gate" mean something precise and different for every Skill that invokes the Funnel.

## Target
A JSON object containing the ecologically adapted Distillation Funnel configuration, ready to be injected into the final SKILL.md by the Skill Assembler.

## Context
Invoked by the Skill Assembler Agent during Phase 2, ONLY when the approved Design Brief's `modules` field lists "Distillation Funnel" as a required module.

## Trigger
Skill Assembler sends this Skill the Design Brief JSON + the Funnel Core DNA template.

## Inputs
1. `skill_design_brief` (Object — the full 11-field approved brief)
2. `funnel_core_dna` (Object — the universal 4-Law template, provided below)

---

## ⚙️ The Core DNA (Universal — Never Modified)

The Distillation Funnel ALWAYS operates through exactly 4 Laws, in this exact sequence. The Laws themselves are immutable. Only their EXPRESSION mutates.

```
Law 1: SATURATION — Load all relevant inputs into working memory.
Law 2: CLASSIFICATION — Tag each input signal with a domain-specific category.
Law 3: COMPRESSION — Merge, collapse, or discard signals to increase density.
Law 4: THE GATE — Apply a final authenticity/quality check that rejects surface-level output.
```

---

## ⚙️ The Adaptation Protocol

For each of the 4 Laws, the Adapter Agent MUST answer 3 probing questions to determine the correct ecological mutation. The Agent MUST NOT skip any question.

### Law 1: Saturation (Input Loading)
1. **What inputs does the Design Brief declare?** (Read the `inputs` field verbatim.)
2. **Is passive loading sufficient, or must the Funnel actively collide inputs against each other?** If the skill requires finding tensions/contradictions between inputs, Saturation mutates into "Cross-Input Collision" (as in Voice Emulation). If inputs are independent, standard parallel loading is correct.
3. **What is the loading order?** Does one input need to be loaded before another to establish context?

### Law 2: Classification (Signal Tagging)
1. **What are the domain-specific signal categories?** In content generation: Tension/Vulnerability/Recognition. In visual search: Semiotic Distance (Journalist/Ethnography/Abstract). In data analysis: Structure/Anomaly/Pattern. The Adapter MUST invent the correct taxonomy for the target domain.
2. **How many categories are needed?** Minimum 3, maximum 5. Each category must be mutually exclusive.
3. **Can the categories be machine-verified?** Each category must have a 1-sentence definition that allows an LLM to consistently classify signals.

### Law 3: Compression (Density Engine)
1. **What does "density" mean in this domain?** In H0 (Questions): merging two question types into one hybrid question. In H1 (Blueprints): The Collapse Test ("If I remove one layer, does the idea collapse?"). In H4 (Visuals): The Evidence Test ("Would this image prove the sentence with audio muted?"). The Adapter MUST define a domain-specific Compression Test.
2. **What is the compression threshold?** Below what score or condition does a signal get discarded?
3. **What is the output format after compression?** (Ranked list? Merged artifact? Filtered array?)

### Law 4: The Gate (Authenticity Check)
1. **What does "authenticity" mean in this domain?** In content: unpredictability and emotional specificity. In data: statistical significance. In visuals: cinematic verité vs. stock photography.
2. **What specific test does the Gate apply?** The Adapter MUST define a single, unambiguous pass/fail criterion.
3. **What happens to signals that fail the Gate?** (Discard? Flag for human review? Re-process through Compression?)

---

## 🚫 Negative Space (Constraints)
*   **NO Copying Core DNA Verbatim:** If the adapted output looks identical to the Core DNA template, the adaptation has failed. Every domain requires a unique mutation.
*   **NO Inventing New Laws:** The Funnel is ALWAYS exactly 4 Laws. Do not add a Law 5 or merge Laws.
*   **NO Generic Compression:** If the Compression Test reads "Merge signals for density" without a domain-specific verb (Collapse, Evidence, Collision, etc.), the adaptation is invalid.
*   **NO Skipping Questions:** All 12 probing questions (3 per Law) must be explicitly answered in the `adaptation_reasoning` output.

---

## 📦 Output Artifact
**Format:** JSON
**Schema:**
```json
{
  "module_name": "Distillation Funnel",
  "adapted_for_skill": "string (Design Brief intent, first sentence)",
  "adaptation": {
    "law_1_saturation": {
      "expression": "string (how saturation works in this domain)",
      "loading_type": "Passive|Cross-Input Collision",
      "loading_order": "string"
    },
    "law_2_classification": {
      "expression": "string (how classification works)",
      "categories": ["string", "string", "string"],
      "category_definitions": {
        "category_1": "string (1-sentence machine-verifiable definition)",
        "category_2": "string",
        "category_3": "string"
      }
    },
    "law_3_compression": {
      "expression": "string (domain-specific compression test name)",
      "compression_test": "string (the exact test question)",
      "threshold": "string (below what condition signals are discarded)",
      "output_format": "string (ranked list | merged artifact | filtered array)"
    },
    "law_4_gate": {
      "expression": "string (what authenticity means here)",
      "gate_test": "string (single pass/fail criterion)",
      "failure_action": "discard | flag_for_review | reprocess"
    }
  },
  "adaptation_reasoning": {
    "law_1_q1": "string", "law_1_q2": "string", "law_1_q3": "string",
    "law_2_q1": "string", "law_2_q2": "string", "law_2_q3": "string",
    "law_3_q1": "string", "law_3_q2": "string", "law_3_q3": "string",
    "law_4_q1": "string", "law_4_q2": "string", "law_4_q3": "string"
  }
}
```

## 🏁 Success Criteria
1. JSON validates against schema.
2. All 12 `adaptation_reasoning` fields are populated (no empty strings).
3. `law_3_compression.compression_test` contains a domain-specific question, not a generic "merge for density."
4. `law_2_classification.categories` contains between 3-5 items, all mutually exclusive.
5. `law_4_gate.gate_test` is a single sentence expressible as a pass/fail check.
