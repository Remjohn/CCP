---
name: irevc-adapter
description: "Takes the Design Brief and produces a domain-adapted I-R-E-V-C Session Protocol specifying what to Ingest, how to Reason, what to Emit, how to Validate, and what to Checkpoint."
category: ccbs/phase2-modules
tier: 1
discovery:
  input_type: "skill_design_brief"
  output_type: "adapted_module_json"
  module_name: "I-R-E-V-C"
  phase: "adapt"
depends_on: []
similar_to:
  - distillation-funnel-adapter
  - deliberation-adapter
compose_with: []
estimated_tokens: 2000
execution_tier: "Standard"
reasoning_modules:
  - type: "Ecological Adaptation"
    adaptation: "Maps the Design Brief's 11 fields onto the 5-stage I-R-E-V-C protocol, ensuring each stage has domain-specific instructions."
---

# 🧬 Module-Skill: I-R-E-V-C Adapter

## Intent
To take the Design Brief's declared inputs, method, output artifact, success criteria, and context, and produce a fully populated I-R-E-V-C Session Protocol that an executing Agent can follow as a standardized execution contract.

## Target
A JSON object containing the 5-stage I-R-E-V-C protocol adapted to the target Skill's domain.

## Context
The I-R-E-V-C protocol is MANDATORY for every CCP Skill (Skill Authoring Guide §4.14). It is the Skill's standardized execution contract. The Assembler ALWAYS invokes this adapter — it is not optional like the Distillation Funnel or Contrastive Anchor.

## Trigger
Skill Assembler sends this Skill the Design Brief JSON.

## Inputs
1. `skill_design_brief` (Object — the full 11-field approved brief)

---

## ⚙️ The Core DNA (Universal — Never Modified)

```
Stage 1: INGEST   — What to load, in what order, what to validate before starting.
Stage 2: REASON   — The algorithm to execute (the Skill's core transformation).
Stage 3: EMIT     — What output to produce, in what format.
Stage 4: VALIDATE — Quality gates to check before declaring complete.
Stage 5: CHECKPOINT — What to update in config.yaml or return to the orchestrator.
```

---

## ⚙️ The Adaptation Protocol

### Stage 1: INGEST Adaptation
1. **Read** `skill_design_brief.action_logic.inputs` — list every input as a numbered loading instruction.
2. **Define loading order.** Rule: If the Design Brief declares a `negative_space` or `constraints` input, it MUST be Load 1 (Boundaries First — Skill Authoring Guide §4.7). All other inputs follow in dependency order.
3. **Define validation gates.** For each input, define what happens if the input is missing or malformed:
   - If mandatory: `HALT — report [MISSING_DATA] for {input_name}. Do NOT hallucinate.`
   - If optional: `PROCEED — apply default value: {default}.`

### Stage 2: REASON Adaptation
1. **Read** `skill_design_brief.action_logic.method` — translate each numbered step into the REASON block.
2. **Read** `skill_design_brief.action_logic.modules` — for each module listed, insert a reference to its adapted configuration (from the corresponding Module-Skill adapter).
3. **Insert Pre-Generation Constraints** (from `skill_design_brief.boundaries.constraints`) BEFORE the first reasoning step. These are construction rules, not post-hoc checks.
4. **If the method includes a scoring/evaluation step:** Insert a reference to the Deliberation Protocol (Draft → Critic → Synthesis).

### Stage 3: EMIT Adaptation
1. **Read** `skill_design_brief.boundaries.output_artifact` — specify the exact file format, file path, and JSON schema.
2. **Define enrichment fields** — what metadata should be attached to the output (e.g., `version`, `generated_at`, `source_inputs`, `quality_score`).

### Stage 4: VALIDATE Adaptation
1. **Read** `skill_design_brief.boundaries.success_criteria` — translate each criterion into a checklist item with `[ ]` notation.
2. **Each checklist item MUST be machine-verifiable.** If a criterion from the Design Brief is subjective, rewrite it as a structural assertion.
3. **Define failure behavior:** If any validation check fails, what happens? (Regenerate? Flag? Halt?)

### Stage 5: CHECKPOINT Adaptation
1. **Define** what state should be updated in `config.yaml` upon successful completion.
2. **Define** what should be returned to the Orchestrator (status code, output path, quality summary).

---

## 🚫 Negative Space (Constraints)
*   **NO Empty Stages:** Every stage must contain at least 2 concrete instructions. An I-R-E-V-C with a vague REASON block is useless.
*   **NO Post-Hoc Validation Only:** Constraints from the Design Brief MUST appear in REASON (as pre-generation constraints), NOT only in VALIDATE. Validation is a double-check, not the primary enforcement mechanism.
*   **NO Invented Inputs:** Only reference inputs declared in the Design Brief. Do not add inputs the Skill didn't declare.

---

## 📦 Output Artifact
**Format:** JSON
**Schema:**
```json
{
  "module_name": "I-R-E-V-C",
  "adapted_for_skill": "string",
  "adaptation": {
    "ingest": {
      "loading_sequence": [
        { "order": 1, "input": "string", "type": "mandatory|optional", "validation": "string" }
      ]
    },
    "reason": {
      "pre_generation_constraints": ["string"],
      "algorithm_steps": ["string"],
      "module_references": ["string"]
    },
    "emit": {
      "file_format": "string",
      "file_path": "string",
      "schema_keys": ["string"],
      "enrichment_fields": ["string"]
    },
    "validate": {
      "checklist": [
        { "check": "string", "type": "structural|semantic", "failure_action": "string" }
      ]
    },
    "checkpoint": {
      "config_update": "string",
      "orchestrator_return": "string"
    }
  }
}
```

## 🏁 Success Criteria
1. JSON validates against schema.
2. `ingest.loading_sequence` contains every input from the Design Brief, with constraints/negative_space as Load 1 (if present).
3. `reason.pre_generation_constraints` is non-empty (at least 1 constraint).
4. `validate.checklist` contains at least 4 items.
5. No stage contains zero instructions.
