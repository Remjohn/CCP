---
name: voice-separation-adapter
description: "Takes the Design Brief and produces a domain-adapted Three-Layer Voice Separation configuration defining what to say (Soul), how to construct it (Mechanics), and the emotional path (Path)."
category: ccbs/phase2-modules
tier: 2
discovery:
  input_type: "skill_design_brief"
  output_type: "adapted_module_json"
  module_name: "Three-Layer Voice Separation"
  phase: "adapt"
depends_on: []
similar_to:
  - distillation-funnel-adapter
compose_with:
  - negative-space-loader-adapter
estimated_tokens: 2000
execution_tier: "Deep/Premium"
reasoning_modules:
  - type: "Ecological Adaptation"
    adaptation: "Maps the Design Brief's voice requirements onto the Soul/Mechanics/Path triple, defining how each layer manifests in the target domain."
---

# 🧬 Module-Skill: Three-Layer Voice Separation Adapter

## Intent
To define how the three voice layers (Soul Alignment, Voice Mechanics, Emotional Path) manifest in the target Skill's specific domain, preventing the common failure of collapsing all three into a single undifferentiated "voice instruction."

## Target
A JSON object containing the adapted Three-Layer Voice Separation configuration specifying which input variables map to each layer and how each layer constrains generation.

## Context
Required for any Skill that generates voice-authentic content (SoC, scripts, copy, responses). NOT required for data extraction, analysis, or routing skills. The Assembler invokes this adapter when the Design Brief's `modules` field lists "Three-Layer Voice Separation."

## Trigger
Skill Assembler sends this Skill the Design Brief JSON.

## Inputs
1. `skill_design_brief` (Object — the full 11-field approved brief)

---

## ⚙️ The Core DNA (Universal — from Skill Authoring Guide §5.4)

```
Layer 1: SOUL ALIGNMENT — What to say (beliefs, worldview, collision points).
          Input Variable: {conscious_soul_values}
Layer 2: VOICE MECHANICS — How to construct it (sentence skeletons, rhythm, discourse markers).
          Input Variable: {voice_dna_spr} Layer 1
Layer 3: EMOTIONAL PATH  — The path from belief to expression (emotional travel, conversion).
          Input Variable: {voice_dna_spr} Layers 2+3
```

---

## ⚙️ The Adaptation Protocol

### Layer 1: Soul Alignment Adaptation
1. **What is "soul" in this domain?** In content writing: the coach's beliefs and worldview. In data analysis: the analytical framework's core assumptions. In coaching responses: the therapeutic orientation.
2. **What input variable carries the soul?** Map the Design Brief's inputs to identify which one contains the "what to say" information.
3. **What happens if the soul layer is violated?** Define the specific consequence: "The output says something the coach would never say" / "The analysis applies assumptions foreign to the framework."

### Layer 2: Voice Mechanics Adaptation
1. **What is "mechanics" in this domain?** In content: sentence skeletons, clause depth, discourse markers. In data reports: formatting conventions, notation standards. In coaching: conversation flow patterns, question scaffolding.
2. **What input variable carries the mechanics?** Map to the specific Voice DNA or construction ruleset.
3. **What structural features define this voice?** List 3-5 concrete mechanical properties (avg sentence length, key syntactic patterns, marker usage).

### Layer 3: Emotional Path Adaptation
1. **What is "emotional path" in this domain?** In content: the journey from belief to expression, the emotional temperature. In analysis: the progression from observation to insight. In coaching: the empathic trajectory.
2. **What input variable carries the path?** Map to the emotional layer of the voice data.
3. **What emotional arc does this Skill's output follow?** Define the shape: escalating? de-escalating? oscillating? flat?

---

## 🚫 Negative Space (Constraints)
*   **NO Collapsing Layers:** If all three layers reference the same input variable with no differentiation, the adaptation has failed. Each layer MUST draw from different aspects of the input data.
*   **NO Skipping Layers:** Even if the Skill's domain seems "purely analytical," all three layers must be populated. Layer 3 for an analytical Skill might be "professional detachment — the output maintains calm authority regardless of findings."
*   **NO Generic Mechanics:** "Write in the coach's voice" is not a mechanical instruction. List specific structural features.

---

## 📦 Output Artifact
**Format:** JSON
**Schema:**
```json
{
  "module_name": "Three-Layer Voice Separation",
  "adapted_for_skill": "string",
  "adaptation": {
    "layer_1_soul": {
      "domain_meaning": "string (what 'soul' means here)",
      "input_variable": "string (which Design Brief input carries this)",
      "violation_consequence": "string (what happens if violated)"
    },
    "layer_2_mechanics": {
      "domain_meaning": "string (what 'mechanics' means here)",
      "input_variable": "string",
      "structural_features": ["string (3-5 concrete properties)"]
    },
    "layer_3_path": {
      "domain_meaning": "string (what 'emotional path' means here)",
      "input_variable": "string",
      "arc_shape": "string (escalating | de-escalating | oscillating | flat | custom)"
    }
  },
  "adaptation_reasoning": {
    "layer_1_q1": "string", "layer_1_q2": "string", "layer_1_q3": "string",
    "layer_2_q1": "string", "layer_2_q2": "string", "layer_2_q3": "string",
    "layer_3_q1": "string", "layer_3_q2": "string", "layer_3_q3": "string"
  }
}
```

## 🏁 Success Criteria
1. JSON validates against schema.
2. All three layers reference different input variables or different aspects of the same variable.
3. `layer_2_mechanics.structural_features` contains 3-5 concrete properties.
4. `layer_3_path.arc_shape` is populated with a specific shape.
5. All 9 `adaptation_reasoning` fields are populated.
