---
name: mcda-adapter
description: "Takes the Design Brief and produces a domain-adapted Multi-Criteria Decision Analysis configuration with weighted principles, feature mapping, and verdict thresholds for any Skill that must evaluate quality or make selections."
category: ccbs/phase2-modules
tier: 2
discovery:
  input_type: "skill_design_brief"
  output_type: "adapted_module_json"
  module_name: "MCDA"
  phase: "adapt"
depends_on: []
similar_to:
  - deliberation-adapter
compose_with:
  - distillation-funnel-adapter
estimated_tokens: 2500
execution_tier: "Deep/Premium"
reasoning_modules:
  - type: "Ecological Adaptation"
    adaptation: "Defines the domain-specific evaluation axes, weights, and verdict thresholds that replace vibes-based quality assessment with evidence-based structural rigor."
---

# 🧬 Module-Skill: MCDA Adapter (Multi-Criteria Decision Analysis)

## Intent
To define the domain-specific evaluation axes, weight distributions, scoring scales, and verdict thresholds that allow a Skill to make quality assessments, selections, or rankings through structural rigor rather than subjective "vibes-based" judgment.

## Target
A JSON object containing the adapted MCDA configuration with weighted criteria, scoring penalties, and verdict generation rules.

## Context
Required for any Skill that evaluates quality, selects candidates, ranks options, or must justify a decision. This includes scoring rubrics, quote selection, content evaluation, and any "which one is best?" operation. NOT required for pure extraction, formatting, or generation Skills.

## Trigger
Skill Assembler sends this Skill the Design Brief JSON.

## Inputs
1. `skill_design_brief` (Object — the full 11-field approved brief)

---

## ⚙️ The Core DNA (Universal — from Reasoning Modules Ecology §4.C)

```
Phase 1: PRINCIPLE IDENTIFICATION — Define the evaluation criteria.
Phase 2: WEIGHTING              — Assign relative importance to each criterion.
Phase 3: FEATURE MAPPING         — Score each candidate against each criterion.
Phase 4: VERDICT GENERATION      — Calculate final scores and produce a justified selection.
```

---

## ⚙️ The Adaptation Protocol

### Phase 1: Principle Identification
1. **What is being evaluated?** (Quotes? Content quality? Visual prompts? Coaching responses? Data completeness?)
2. **Define 3-5 evaluation criteria specific to this domain.** Each criterion must:
   - Target a specific quality dimension (not "is it good?")
   - Be measurable on a consistent scale
   - Be independent of the other criteria (no double-counting)
3. **For each criterion, define:**
   - Name (≤3 words)
   - Definition (1 sentence)
   - Scale (1-10? Binary? Categorical?)
   - What a score of 1 looks like (the floor)
   - What a score of 10 looks like (the ceiling)

### Phase 2: Weighting
1. **Rank the criteria by importance.** Which one is the non-negotiable gatekeeper?
2. **Assign weight multipliers.** The most critical criterion gets 3x weight. The least critical gets 1x. Others fall between.
3. **Define penalty conditions.** When does a criterion score override the total? (e.g., "If Safety scores ≤2, the candidate is rejected regardless of total score.")
4. **Justify the weighting.** Why is criterion X weighted 3x while criterion Y is only 1x? The justification must reference the Design Brief's intent or constraints.

### Phase 3: Feature Mapping
1. **How are candidates scored?** Does the agent assess each candidate independently, or compare them against each other?
2. **What evidence supports each score?** Every score must cite a specific feature of the candidate. No scores without evidence.
3. **How is scoring bias prevented?** Define an anchoring prevention mechanism (e.g., "Score criterion 3 first, then criterion 1, to prevent halo effect from first impression").

### Phase 4: Verdict Generation
1. **What is the aggregation formula?** `(Criterion1 * Weight1) + (Criterion2 * Weight2) + ...`
2. **What is the passing threshold?** Above what total score is a candidate accepted?
3. **What happens on a tie?** Define the tiebreaker criterion.
4. **What is the verdict format?** Must include: winner, total scores for all candidates, per-criterion breakdown, and 1-sentence justification.

---

## 🚫 Negative Space (Constraints)
*   **NO Vibes-Based Criteria:** "Is it high quality?" or "Does it resonate?" are banned. Every criterion must be operationalized with a measurable scale.
*   **NO Equal Weights:** If all criteria have the same weight, the MCDA adds no value over simple averaging. At least one criterion must be weighted higher than the others.
*   **NO Scores Without Evidence:** A score of 8/10 without citing the specific feature that earned it is a hallucinated score.
*   **NO Single-Criterion Dominance:** If one criterion's weight is >50% of the total weight, the other criteria are decorative. Rebalance.

---

## 📦 Output Artifact
**Format:** JSON
**Schema:**
```json
{
  "module_name": "MCDA",
  "adapted_for_skill": "string",
  "adaptation": {
    "evaluation_target": "string (what is being evaluated)",
    "criteria": [
      {
        "name": "string (≤3 words)",
        "definition": "string (1 sentence)",
        "scale": "string (1-10 | binary | categorical)",
        "floor_example": "string (what a 1 looks like)",
        "ceiling_example": "string (what a 10 looks like)",
        "weight": "integer (1-3)"
      }
    ],
    "penalty_overrides": [
      {
        "criterion": "string",
        "condition": "string (e.g., 'score ≤ 2')",
        "action": "string (e.g., 'reject candidate regardless of total')"
      }
    ],
    "weight_justification": "string (why the weights are distributed this way)",
    "scoring_protocol": {
      "assessment_mode": "independent|comparative",
      "evidence_requirement": "string",
      "bias_prevention": "string (scoring order, anchoring prevention)"
    },
    "verdict_rules": {
      "aggregation_formula": "string",
      "passing_threshold": "string",
      "tiebreaker_criterion": "string",
      "verdict_format": "string"
    }
  }
}
```

## 🏁 Success Criteria
1. JSON validates against schema.
2. `criteria` contains 3-5 entries, each with a non-generic `definition`.
3. Weight distribution is unequal — at least one criterion has weight ≥2x another.
4. `penalty_overrides` contains at least 1 override for the highest-weighted criterion.
5. `scoring_protocol.evidence_requirement` is non-empty.
6. `verdict_rules.aggregation_formula` is a concrete mathematical expression.
