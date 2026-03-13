---
name: contrastive-anchor-adapter
description: "Takes the Design Brief's domain context and produces an ecologically adapted Contrastive Anchor (Anti-Draft) configuration calibrated to the target Skill's specific failure mode."
category: ccbs/phase2-modules
tier: 2
discovery:
  input_type: "skill_design_brief + module_core_dna"
  output_type: "adapted_module_json"
  module_name: "Contrastive Anchor"
  phase: "adapt"
depends_on: []
similar_to:
  - distillation-funnel-adapter
  - deliberation-adapter
compose_with: []
estimated_tokens: 2500
execution_tier: "Deep/Premium"
reasoning_modules:
  - type: "Ecological Adaptation"
    adaptation: "Mutates the Anti-Draft immune system to target the specific failure mode of the host Skill's domain."
---

# 🧬 Module-Skill: Contrastive Anchor Adapter

## Intent
To define the exact "Archetypal Failure Mode" — what generic, sycophantic, mediocre AI output looks like — for the target Skill's specific domain, and produce a calibrated negative anchor that forces the LLM's output as far as possible from that failure baseline.

## Target
A JSON object containing the ecologically adapted Contrastive Anchor configuration, ready for injection into the final SKILL.md.

## Context
Invoked by the Skill Assembler Agent during Phase 2, ONLY when the approved Design Brief's `modules` field lists "Contrastive Anchor" as a required module.

## Trigger
Skill Assembler sends this Skill the Design Brief JSON + the Contrastive Anchor Core DNA.

## Inputs
1. `skill_design_brief` (Object — the full 11-field approved brief)
2. `anchor_core_dna` (Object — the universal template, provided below)

---

## ⚙️ The Core DNA (Universal — Never Modified)

The Contrastive Anchor ALWAYS operates through exactly 3 Axes, in this exact sequence:

```
Axis 1: NEGATIVE DEMONSTRATION — Generate the exact "average AI failure" for this task.
Axis 2: FALSE POSITIVE VISIBILITY — Make the failure mode explicitly visible to the model.
Axis 3: INFERENCE-TIME STEERING — Instruct the model to maximize distance from the negative anchor.
```

---

## ⚙️ The Adaptation Protocol

For each Axis, the Adapter Agent MUST answer the probing questions to determine the correct ecological mutation.

### Axis 1: Negative Demonstration (The Anti-Draft)
1. **What does "generic AI output" look like in this domain?** In content writing: "robotic, mechanically polished, corporate-safe prose." In visual prompts: "stock photography — diverse professionals smiling at laptops in glass offices." In coaching analysis: "surface-level pattern matching that tells the coach what they want to hear (sycophancy)." In data extraction: "returning the first N results without scoring or ranking."
2. **Write the actual Anti-Draft.** The Adapter MUST generate a 3-5 sentence example of what the BAD version of this Skill's output would look like. This is the negative anchor text.
3. **Why would an LLM naturally produce this bad output?** Identify the specific statistical tendency (mean reversion, sycophancy, verbosity, hedging) that drives the LLM toward the failure mode.

### Axis 2: False Positive Visibility
1. **How would a lazy evaluator mistake the bad output for a good one?** What surface features (correct formatting, confident tone, plausible structure) make the Anti-Draft look acceptable?
2. **What is the single most deceptive quality of the failure mode?** The one trait that makes it hardest to distinguish bad output from good output. Name it explicitly.

### Axis 3: Inference-Time Steering
1. **What specific instruction forces maximum distance from the negative anchor?** Write the exact contrastive instruction that will be injected into the Skill's prompt. It must reference the Anti-Draft explicitly and provide a measurable contrast direction.
2. **What vocabulary is forbidden?** List 5-10 specific words or phrases that are characteristic of the failure mode and must be banned from the Skill's output.

---

## 🚫 Negative Space (Constraints)
*   **NO Generic Anti-Drafts:** If the Anti-Draft reads "The bad version would be generic and unhelpful," the adaptation has failed. The Anti-Draft must be a SPECIFIC, DETAILED example of mediocre output.
*   **NO Copying Between Domains:** The Anti-Draft for a content-writing Skill cannot be reused for a data-extraction Skill. Each domain has a unique failure smell.
*   **NO Skipping the Actual Example:** Axis 1, Question 2 requires writing the ACTUAL BAD OUTPUT, not describing it. The Adapter must produce the literal text of the failure.

---

## 📦 Output Artifact
**Format:** JSON
**Schema:**
```json
{
  "module_name": "Contrastive Anchor",
  "adapted_for_skill": "string (Design Brief intent, first sentence)",
  "adaptation": {
    "axis_1_negative_demonstration": {
      "failure_mode_description": "string (what generic AI output looks like)",
      "anti_draft_text": "string (3-5 sentence ACTUAL example of bad output)",
      "statistical_tendency": "string (mean reversion | sycophancy | verbosity | hedging | other)"
    },
    "axis_2_false_positive_visibility": {
      "deceptive_surface_features": "string (what makes the bad output look acceptable)",
      "most_deceptive_trait": "string (the single hardest-to-detect quality of the failure)"
    },
    "axis_3_inference_steering": {
      "contrastive_instruction": "string (the exact prompt injection that steers away from the anchor)",
      "forbidden_vocabulary": ["string", "string", "string", "string", "string"]
    }
  },
  "adaptation_reasoning": {
    "axis_1_q1": "string", "axis_1_q2": "string", "axis_1_q3": "string",
    "axis_2_q1": "string", "axis_2_q2": "string",
    "axis_3_q1": "string", "axis_3_q2": "string"
  }
}
```

## 🏁 Success Criteria
1. JSON validates against schema.
2. `anti_draft_text` contains 3-5 sentences of ACTUAL example bad output, not a description.
3. `forbidden_vocabulary` contains at least 5 specific words or phrases.
4. `contrastive_instruction` explicitly references the anti-draft and provides a measurable contrast direction.
5. All 7 `adaptation_reasoning` fields are populated.
