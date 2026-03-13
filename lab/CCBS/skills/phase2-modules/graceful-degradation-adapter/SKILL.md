---
name: graceful-degradation-adapter
description: "Takes the Design Brief and produces a structured fallback protocol defining what the Skill does when inputs are missing, malformed, or below quality thresholds."
category: ccbs/phase2-modules
tier: 1
discovery:
  input_type: "skill_design_brief"
  output_type: "adapted_module_json"
  module_name: "Graceful Degradation"
  phase: "adapt"
depends_on: []
similar_to:
  - negative-space-loader-adapter
compose_with:
  - irevc-adapter
estimated_tokens: 1500
execution_tier: "Standard"
reasoning_modules:
  - type: "Ecological Adaptation"
    adaptation: "Maps every declared input and method step to explicit failure handling using the [MISSING_DATA] pattern from CCP convention."
---

# 🧬 Module-Skill: Graceful Degradation Adapter

## Intent
To define what happens when things go wrong during Skill execution — missing inputs, malformed data, below-threshold quality scores — so the Skill never hallucinates to fill gaps and never silently fails.

## Target
A JSON object containing the degradation protocol: a mapping of every input and critical method step to its failure behavior.

## Context
Every CCP Skill must handle missing data explicitly (Skill Authoring Guide §8: The `[MISSING_DATA]` Pattern). This adapter ensures no input or step is left without a defined fallback.

## Trigger
Skill Assembler sends this Skill the Design Brief JSON.

## Inputs
1. `skill_design_brief` (Object — the full 11-field approved brief)

---

## ⚙️ The Core DNA (Universal)

```
Principle 1: NEVER HALLUCINATE TO FILL GAPS — Report [MISSING_DATA] explicitly.
Principle 2: DEGRADE GRACEFULLY — Produce partial output with clear flags, not total failure.
Principle 3: NEVER SILENTLY SKIP — If a step is impossible, log it and alert.
```

---

## ⚙️ The Adaptation Protocol

### Input Degradation Map
For each input in `skill_design_brief.action_logic.inputs`:

1. **Classify the input:**
   - **Critical:** Without this input, the Skill cannot produce meaningful output. Missing = HALT.
   - **Important:** Without this input, output quality degrades significantly. Missing = DEGRADE with flag.
   - **Optional:** Without this input, output is still valid but less rich. Missing = PROCEED with default.

2. **Define the failure behavior:**
   - For Critical: `HALT — report [MISSING_DATA: {input_name}]. Do NOT proceed. Alert Orchestrator.`
   - For Important: `DEGRADE — proceed with {default_value}. Flag output as DEGRADED. Attach degradation_reason.`
   - For Optional: `PROCEED — use {default_value}. No flag required.`

3. **Define the malformation behavior:**
   - What happens if the input exists but is in the wrong format?
   - What happens if the input exists but contains zero useful data?

### Method Step Degradation Map
For each step in `skill_design_brief.action_logic.method`:

1. **What is the minimum viable output of this step?** If the step partially fails, what can still be produced?
2. **What is the retry strategy?** (No retry? Retry once with simplified parameters? Retry with fallback algorithm?)
3. **What is the escalation path?** If the step fails completely, who gets notified?

### Quality Threshold Degradation
For each success criterion in `skill_design_brief.boundaries.success_criteria`:

1. **Define the scoring threshold:** Above = PASS. Below = what happens?
2. **Define the degradation level:**
   - **Soft fail:** Output is released with a quality warning flag.
   - **Hard fail:** Output is rejected. Trigger retry or escalation.

---

## 🚫 Negative Space (Constraints)
*   **NO Silent Failures:** Every failure MUST be logged and visible. An agent that silently succeeds with missing data is worse than one that loudly fails.
*   **NO Hallucination as Fallback:** "Generate a reasonable approximation" is NEVER an acceptable degradation behavior. Use `[MISSING_DATA]` or typed defaults.
*   **NO Undefined Inputs:** Every input declared in the Design Brief MUST have a degradation entry. No gaps.

---

## 📦 Output Artifact
**Format:** JSON
**Schema:**
```json
{
  "module_name": "Graceful Degradation",
  "adapted_for_skill": "string",
  "adaptation": {
    "input_degradation": [
      {
        "input_name": "string",
        "classification": "Critical|Important|Optional",
        "missing_behavior": "string",
        "malformed_behavior": "string",
        "default_value": "string|null"
      }
    ],
    "method_step_degradation": [
      {
        "step": "string (step description)",
        "minimum_viable_output": "string",
        "retry_strategy": "none|retry_once|retry_simplified",
        "escalation_path": "string"
      }
    ],
    "quality_threshold_degradation": [
      {
        "criterion": "string",
        "threshold": "string",
        "below_threshold_behavior": "soft_fail|hard_fail",
        "action": "string"
      }
    ]
  }
}
```

## 🏁 Success Criteria
1. JSON validates against schema.
2. `input_degradation` contains an entry for EVERY input in the Design Brief.
3. At least 1 input is classified as `Critical`.
4. No `missing_behavior` says "generate a reasonable approximation" or similar hallucination instruction.
5. Every `method_step_degradation` entry has a non-empty `escalation_path`.
