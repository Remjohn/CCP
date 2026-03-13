---
name: deliberation-adapter
description: "Takes the Design Brief's domain context and produces an ecologically adapted Draft→Critic→Synthesis deliberation protocol calibrated to the target Skill's evaluation domain."
category: ccbs/phase2-modules
tier: 2
discovery:
  input_type: "skill_design_brief + module_core_dna"
  output_type: "adapted_module_json"
  module_name: "Draft→Critic→Synthesis"
  phase: "adapt"
depends_on: []
similar_to:
  - distillation-funnel-adapter
  - contrastive-anchor-adapter
compose_with: []
estimated_tokens: 2500
execution_tier: "Deep/Premium"
reasoning_modules:
  - type: "Ecological Adaptation"
    adaptation: "Mutates the Deliberation Protocol's Critic questions and Synthesis rules to match the specific evaluation domain of the host Skill."
---

# 🧬 Module-Skill: Deliberation Adapter (Draft → Critic → Synthesis)

## Intent
To take the universal Draft→Critic→Synthesis deliberation protocol and produce domain-specific Critic questions, Synthesis rules, and failure thresholds calibrated to the target Skill's specific evaluation needs.

## Target
A JSON object containing the ecologically adapted Deliberation Protocol configuration, ready for injection into the final SKILL.md.

## Context
Invoked by the Skill Assembler Agent during Phase 2, ONLY when the approved Design Brief's `modules` field lists "Draft→Critic→Synthesis" as a required module.

## Trigger
Skill Assembler sends this Skill the Design Brief JSON + the Deliberation Core DNA.

## Inputs
1. `skill_design_brief` (Object — the full 11-field approved brief)
2. `deliberation_core_dna` (Object — the universal template, provided below)

---

## ⚙️ The Core DNA (Universal — Never Modified)

The Deliberation Protocol ALWAYS operates through exactly 3 Phases:

```
Phase 1: DRAFT — Generate the initial output following the Skill's Method.
Phase 2: CRITIC — Challenge the Draft with domain-specific scrutiny questions.
Phase 3: SYNTHESIS — Resolve Critic concerns, either confirming the Draft or producing a revision.
```

The sequence is immutable. The CONTENT of each phase mutates per domain.

---

## ⚙️ The Adaptation Protocol

### Phase 1: Draft Configuration
1. **What is being drafted?** Read the Design Brief's `action` and `output_artifact` fields. The Draft phase produces a first-pass version of this exact artifact.
2. **What format does the Draft take?** (JSON object? Markdown document? Array of scored items?) Must match the `output_artifact` specification.
3. **Do any Pre-Generation Constraints apply before drafting?** If the Design Brief's `constraints` field contains front-loaded rules (word limits, forbidden patterns), these must be enforced BEFORE the Draft is generated, not checked after.

### Phase 2: Critic Configuration (The Most Critical Adaptation)
The Critic must ask questions that are specific to the evaluation domain. Generic questions like "Is this good?" are structurally invalid.

1. **What are the 4-6 Critic questions for this domain?** Each question must:
   - Target a specific failure mode unique to this Skill's output type
   - Be answerable with evidence from the Draft (not subjective opinion)
   - Reference a measurable quality (score, count, presence/absence)
   
   *Examples from existing CCP Skills:*
   - Quote Extraction: "Is the Specificity score inflated? Does the quote contain ACTUAL numbers or just IMPLIES them?"
   - Visual Prompts: "Would this prompt produce a stock-photo result or a cinematic-verité result?"
   - Content Writing: "Does this paragraph contain the coach's actual words, or has the AI paraphrased them into corporate smoothness?"

2. **What is the Critic's evaluation scale?** (Binary pass/fail? 1-10 score? Category labels?) Must be machine-verifiable.

3. **What is the concern threshold?** How many Critic concerns trigger a re-draft? (e.g., "If ≥2 concerns are flagged, re-draft the artifact.")

### Phase 3: Synthesis Configuration
1. **What happens when the Critic flags concerns?** Options:
   - `REVISE_AND_REPLACE`: Generate a new Draft addressing the flagged concerns.
   - `REVISE_FLAGGED_ONLY`: Keep unflagged sections, revise only flagged sections.
   - `EXPAND_CANDIDATES`: Generate 2 additional Draft candidates, then select the best.
2. **What happens when the Critic flags zero concerns?** Confirm and release.
3. **Maximum deliberation rounds?** To prevent infinite loops. Recommended: 2 rounds maximum.

---

## 🚫 Negative Space (Constraints)
*   **NO Generic Critic Questions:** If a Critic question is "Is this output high quality?", the adaptation has failed. Every question must reference a specific, domain-bound failure mode.
*   **NO Skipping Pre-Generation Constraints:** If the Design Brief specifies constraints, they must be enforced BEFORE the Draft phase, not post-hoc.
*   **NO Infinite Deliberation:** Maximum 2 Critic rounds. After round 2, the best available Draft is released with a quality flag, not endlessly re-processed.

---

## 📦 Output Artifact
**Format:** JSON
**Schema:**
```json
{
  "module_name": "Draft→Critic→Synthesis",
  "adapted_for_skill": "string (Design Brief intent, first sentence)",
  "adaptation": {
    "phase_1_draft": {
      "draft_target": "string (what is being drafted)",
      "draft_format": "string (JSON | Markdown | Array)",
      "pre_generation_constraints": ["string", "string"]
    },
    "phase_2_critic": {
      "critic_questions": [
        {
          "question": "string (domain-specific scrutiny question)",
          "target_failure_mode": "string (what this question catches)",
          "evidence_type": "string (what measurable quality answers this)"
        }
      ],
      "evaluation_scale": "string (binary | 1-10 | category labels)",
      "concern_threshold": "string (e.g., '≥2 concerns trigger re-draft')"
    },
    "phase_3_synthesis": {
      "revision_strategy": "REVISE_AND_REPLACE | REVISE_FLAGGED_ONLY | EXPAND_CANDIDATES",
      "zero_concerns_action": "Confirm and release",
      "max_rounds": 2
    }
  },
  "adaptation_reasoning": {
    "draft_q1": "string", "draft_q2": "string", "draft_q3": "string",
    "critic_q1": "string", "critic_q2": "string", "critic_q3": "string",
    "synthesis_q1": "string", "synthesis_q2": "string", "synthesis_q3": "string"
  }
}
```

## 🏁 Success Criteria
1. JSON validates against schema.
2. `critic_questions` contains 4-6 questions, each with a named `target_failure_mode`.
3. No Critic question uses subjective adjectives ("good," "quality," "meaningful").
4. `max_rounds` is ≤ 2.
5. `pre_generation_constraints` lists at least 1 constraint from the Design Brief.
6. All 9 `adaptation_reasoning` fields are populated.
