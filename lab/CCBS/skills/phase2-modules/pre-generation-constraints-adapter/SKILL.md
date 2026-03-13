---
name: pre-generation-constraints-adapter
description: "Takes the Design Brief's constraints and success criteria and repositions them as front-loaded construction rules that operate BEFORE generation, not as post-hoc validation checklists."
category: ccbs/phase2-modules
tier: 1
discovery:
  input_type: "skill_design_brief"
  output_type: "adapted_module_json"
  module_name: "Pre-Generation Constraints"
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
    adaptation: "Converts post-hoc evaluation criteria into front-loaded construction constraints following CCF Bible Critique v2 Principle 3."
---

# 🧬 Module-Skill: Pre-Generation Constraints Adapter

## Intent
To transform the Design Brief's constraints and success criteria from post-hoc validation checklists into front-loaded construction rules that constrain generation BEFORE output is produced. Research proves (CCF Bible Critique v2 §3) that quality criteria placed at the END of a prompt cause the model to write TOWARD passing them rather than FROM them.

## Target
A JSON object containing the repositioned constraints as pre-generation construction rules, ready for injection into the SKILL.md BEFORE the Algorithm Phases section.

## Context
Required for every Skill. The Assembler ALWAYS invokes this adapter alongside the I-R-E-V-C adapter.

## Trigger
Skill Assembler sends this Skill the Design Brief JSON.

## Inputs
1. `skill_design_brief` (Object — the full 11-field approved brief)

---

## ⚙️ The Conversion Protocol

For each constraint or success criterion from the Design Brief, the Adapter MUST classify it and reposition it:

### Classification
1. **Read** `skill_design_brief.boundaries.constraints` — all items.
2. **Read** `skill_design_brief.boundaries.success_criteria` — all items.
3. **For each item, classify:**
   - **Type A: Structural Constraint** — Can be enforced by formatting rules (word counts, JSON keys, sentence limits). → Convert to Pre-Generation Constraint.
   - **Type B: Semantic Constraint** — Requires reading comprehension to verify (relevance, coherence, voice accuracy). → Convert to Pre-Generation Constraint with a generative instruction.
   - **Type C: Mathematical Constraint** — Requires computation (scores, thresholds, counts). → Leave as Post-Validation AND add a Pre-Generation reminder.

### Conversion Rules

**Type A (Structural) Conversion:**
| ❌ Post-hoc checklist | ✅ Pre-generation constraint |
|---|---|
| "VALIDATION: Output must be ≤200 words" | "Constraint: Generate ≤200 words. Count at each paragraph." |
| "CHECK: JSON must contain key 'score'" | "Constraint: Every JSON object MUST include 'score' (float 0-1). Omission = structural failure." |

**Type B (Semantic) Conversion:**
| ❌ Post-hoc checklist | ✅ Pre-generation constraint |
|---|---|
| "VALIDATION: Does output sound authentic?" | "Constraint: ≥80% of sentences use constructions from authenticated source material." |
| "CHECK: Is there sufficient depth?" | "Constraint: Single-Thought Integrity — if more than one argument is active, return to the seed concept." |

**Type C (Mathematical) — Dual Placement:**
These stay in VALIDATE but also get a pre-generation reminder:
| Post-validation | Pre-generation reminder |
|---|---|
| "Score must be ≥7/10" | "Reminder: Target ≥7/10 on the scoring rubric. Do not accept first-draft scores without Critic review." |

---

## 🚫 Negative Space (Constraints)
*   **NO Leaving Constraints Only at the End:** If all constraints appear only in VALIDATE, the Skill will game them. At least 70% of constraints MUST be repositioned as pre-generation rules.
*   **NO Vague Constraints:** "Be high quality" is not a constraint. Every pre-generation rule must be testable.
*   **NO Duplicating Without Adapting:** Simply copying the constraint text from VALIDATE to a pre-gen section is not conversion. The constraint must be REWRITTEN as a generative instruction.

---

## 📦 Output Artifact
**Format:** JSON
**Schema:**
```json
{
  "module_name": "Pre-Generation Constraints",
  "adapted_for_skill": "string",
  "adaptation": {
    "pre_generation_rules": [
      {
        "original_source": "string (which Design Brief field this came from)",
        "original_text": "string (the constraint as written in the Design Brief)",
        "classification": "Type A|Type B|Type C",
        "converted_rule": "string (the rewritten pre-generation construction constraint)"
      }
    ],
    "post_validation_only": [
      {
        "original_text": "string",
        "reason_for_post_only": "string (why this cannot be front-loaded)",
        "pre_generation_reminder": "string (the reminder text injected before generation)"
      }
    ]
  }
}
```

## 🏁 Success Criteria
1. JSON validates against schema.
2. `pre_generation_rules` contains ≥70% of all constraints from the Design Brief.
3. Every `converted_rule` is different from its `original_text` (rewritten, not copied).
4. Every Type C constraint in `post_validation_only` has a non-empty `pre_generation_reminder`.
5. No rule contains subjective adjectives without an operationalized definition.
