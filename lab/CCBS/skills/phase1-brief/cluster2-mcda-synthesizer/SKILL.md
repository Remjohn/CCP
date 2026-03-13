---
name: cluster2-mcda-synthesizer
description: "Takes the expansion and constraint drafts for the Action Logic, scores them against the 3-axis MCDA rubric, runs a 5-dimension self-evaluation, and synthesizes final fields 5-8."
category: ccbs/phase1-brief
tier: 2
discovery:
  input_type: "dual_draft_action"
  output_type: "synthesized_action_logic"
  cluster: 2
  phase: "synthesize"
depends_on:
  - cluster2-action-brainstormer
similar_to:
  - cluster1-mcda-synthesizer
  - cluster3-mcda-synthesizer
compose_with: []
estimated_tokens: 3000
execution_tier: "Deep/Premium"
reasoning_modules:
  - type: "MCDA Matrix"
    adaptation: "Evaluates Cost-Awareness (L3 reductionism) vs Execution Efficacy (L2 complexity) for procedural fields."
  - type: "Self-Evaluation Gate"
    adaptation: "Post-synthesis 5-dimension quality check before output release."
---

# 🧠 Cluster 2: MCDA Synthesizer

## Intent
To calculate the optimal synthesis of the Action Logic by balancing cognitive sophistication against determinism and cost, then validating via the 5-Dimension Self-Evaluation Gate.

## Target
The finalized, self-evaluated JSON payload containing the validated `Inputs`, `Action`, `Method`, and `Modules` fields for the Phase 1 Design Brief.

## Context
Operates immediately after `cluster2-action-brainstormer`. Only executes if the Brainstormer output is schema-compliant.

## Trigger
Receives the two-draft JSON payload spanning fields 5-8 plus the `synthesized_core` as context.

## Inputs
1. `synthesized_core` (Object from Cluster 1 — context only)
2. `expansion_draft` (Object from Cluster 2 Brainstormer)
3. `constraint_draft` (Object from Cluster 2 Brainstormer)

## Action
Score conflicting drafts via MCDA, synthesize the master procedural logic, then validate via 5-Dimension Self-Evaluation Gate.

---

## ⚙️ Reasoning Architecture

### Phase A: The 3-Axis MCDA Protocol

For each field (Inputs, Action, Method, Modules), execute the following matrix in working memory. Show numerical scores in the `mcda_trace`.

#### The Scoring Matrix (1-10 Scale)

**Criterion 1: Parameter Independence (Weight 3x) [CRITICAL]**
*   *Test:* Are all inputs and variables expressed as typed abstract parameters?
*   *Pass Condition:* Every input is expressed as `variable_name (Type: description)`.
*   *Penalty:* If any field mentions specific instance data (e.g., "Maman Adele", "Jean-Pierre", "/users/coach123/"), score = 0.
*   *Penalty:* If inputs are expressed as prose descriptions instead of typed variables, score ≤ 4.

**Criterion 2: Cost & Simplification (Weight 2x)**
*   *Test:* Is the method and module composition the cheapest path that still achieves the Target?
*   *Pass Condition:* Each reasoning step justifies its token cost.
*   *Penalty:* If the procedure uses a Draft→Critic→Synthesis loop for a task that could be solved with simple parsing, score ≤ 3.
*   *Penalty:* If more than 3 Modules are proposed without explicit justification for each, score ≤ 4.

**Criterion 3: Execution Efficacy (Weight 1x)**
*   *Test:* Will this procedure actually fulfill the Target defined in Cluster 1?
*   *Pass Condition:* The method logically produces the artifact described in `synthesized_core.target`.
*   *Penalty:* If the constraints are so rigid that the Target becomes impossible to reach, score ≤ 3.

#### Synthesis Logic
For each field:
1. Calculate `(Crit1 * 3) + (Crit2 * 2) + (Crit3 * 1)` for both drafts. Record exact scores.
2. **Inputs:** Take the strict minimum from Constraint, but if Expansion identifies a genuinely critical contextual input that Constraint omitted, add it with explicit justification in the `mcda_trace`.
3. **Action:** Take whichever draft most precisely describes the transformation. Rewrite for determinism.
4. **Method:** Synthesize as a numbered list. Start with Constraint's linear flow but inject Expansion's deliberation steps ONLY where the task complexity genuinely requires them. Hard cap: 5 steps maximum.
5. **Modules:** Select the intersection of necessary (Constraint) and optimal (Expansion). Hard cap: 3 modules maximum. Each module must have a 1-sentence justification.

---

### Phase B: The 5-Dimension Self-Evaluation Gate (SkillNet §3.4)

After producing the synthesized output, run the following 5-point quality check.

**1. Safety:** Does the Method authorize the Skill to perform actions beyond its declared Inputs (e.g., fetching data from external APIs not listed in Inputs)?
- `Good`: Method strictly operates on declared Inputs.
- `Poor`: Method implies undeclared data access.

**2. Completeness:** Are all 4 fields populated with substantive, multi-sentence content that fully specifies the procedure?
- `Good`: All fields contain ≥2 sentences. Method contains numbered steps. Modules list canonical names.
- `Poor`: Any field is empty, placeholder, or single-word.

**3. Executability:** Could an agent given ONLY this JSON produce the Target without additional guidance?
- `Good`: The Method is a complete, self-contained algorithm.
- `Poor`: The Method references undefined steps, external documents, or "use your judgment."

**4. Maintainability:** Can the Modules list be changed without rewriting the Method?
- `Good`: Method references modules by name but does not hardcode module internals.
- `Poor`: Module-specific logic is tangled into the Method steps.

**5. Cost-awareness:** Does the Method stay within the `estimated_tokens` budget (3500)?
- `Good`: Method has ≤5 steps, ≤3 modules.
- `Poor`: Method has >5 steps or >3 modules without explicit cost justification.

#### Gate Logic
- If **any dimension scores `Poor`**: `FAILED_SELF_EVAL` — Orchestrator re-invokes the Brainstormer.
- If **all dimensions score `Good` or `Average`**: Output released.

---

## 🚫 Negative Space (Constraints)
*   **NO Hallucinated Modules:** Only reference canonical cognitive modules from the CCBS Module Registry (Distillation Funnel, Contrastive Anchor, Draft→Critic→Synthesis, I-R-E-V-C, Negative Space Loader, Three-Layer Voice Separation, Pre-Generation Constraints, Graceful Degradation).
*   **NO OODA Loops in Method:** If either draft contains open-ended routing, the Synthesizer MUST rewrite as a linear sequence.
*   **NO Skipping Self-Evaluation:** The 5-Dimension Gate is mandatory.

---

## 📦 Output Artifact
**Format:** JSON
**File Path:** `{workspace}/ccbs_output/cluster2_synthesized.json`
**Schema:**
```json
{
  "synthesized_action_logic": {
    "inputs": "string (typed variables)",
    "action": "string",
    "method": "string (numbered steps, max 5)",
    "modules": "string (canonical names, max 3, each with 1-sentence justification)"
  },
  "mcda_trace": {
    "inputs": { "expansion_score": 0, "constraint_score": 0, "winner": "Expansion|Constraint|Hybrid" },
    "action": { "expansion_score": 0, "constraint_score": 0, "winner": "Expansion|Constraint|Hybrid" },
    "method": { "expansion_score": 0, "constraint_score": 0, "winner": "Expansion|Constraint|Hybrid" },
    "modules": { "expansion_score": 0, "constraint_score": 0, "winner": "Expansion|Constraint|Hybrid" }
  },
  "self_evaluation": {
    "safety": "Good|Average|Poor",
    "completeness": "Good|Average|Poor",
    "executability": "Good|Average|Poor",
    "maintainability": "Good|Average|Poor",
    "cost_awareness": "Good|Average|Poor",
    "gate_result": "PASSED|FAILED_SELF_EVAL"
  }
}
```

## 🏁 Success Criteria
1. JSON validates against schema.
2. The `mcda_trace` contains exact numerical scores.
3. The `self_evaluation.gate_result` is `PASSED`.
4. The `method` contains ≤5 numbered steps.
5. The `modules` lists ≤3 canonical module names, each with justification.
6. The `inputs` uses typed variable notation exclusively.
