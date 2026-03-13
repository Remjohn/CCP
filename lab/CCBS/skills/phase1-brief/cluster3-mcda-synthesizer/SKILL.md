---
name: cluster3-mcda-synthesizer
description: "Takes the expansion and constraint drafts for the Boundaries, scores them, runs a 5-dimension self-evaluation, and synthesizes final fields 9-11."
category: ccbs/phase1-brief
tier: 2
discovery:
  input_type: "dual_draft_boundaries"
  output_type: "synthesized_boundaries"
  cluster: 3
  phase: "synthesize"
depends_on:
  - cluster3-boundary-brainstormer
similar_to:
  - cluster1-mcda-synthesizer
  - cluster2-mcda-synthesizer
compose_with: []
estimated_tokens: 3000
execution_tier: "Deep/Premium"
reasoning_modules:
  - type: "MCDA Matrix"
    adaptation: "Evaluates Deterministic Verification (L3 machine-testability) vs Systemic Safety (safeguarding against LLM semantic drift)."
  - type: "Self-Evaluation Gate"
    adaptation: "Post-synthesis 5-dimension quality check before output release."
---

# 🧠 Cluster 3: MCDA Synthesizer

## Intent
To calculate the optimal synthesis of the Action Boundaries by balancing rigid machine-testable verification against systemic LLM safety needs, then self-evaluating before release.

## Target
The finalized, self-evaluated JSON payload containing the validated `Constraints`, `Output Artifact`, and `Success Criteria` fields for the Phase 1 Design Brief.

## Context
Operates immediately after `cluster3-boundary-brainstormer`. Only executes if the Brainstormer output is schema-compliant.

## Trigger
Receives the two-draft JSON payload spanning fields 9-11.

## Inputs
1. `synthesized_action_logic` (Object from Cluster 2 — context only)
2. `expansion_draft` (Object from Cluster 3 Brainstormer)
3. `constraint_draft` (Object from Cluster 3 Brainstormer)

## Action
Score conflicting drafts via MCDA, synthesize the master boundaries, then validate via the 5-Dimension Self-Evaluation Gate.

---

## ⚙️ Reasoning Architecture

### Phase A: The 3-Axis MCDA Protocol

For each field (Constraints, Output Artifact, Success Criteria), execute the following matrix. Show numerical scores in `mcda_trace`.

#### The Scoring Matrix (1-10 Scale)

**Criterion 1: Deterministic Verification (Weight 3x) [CRITICAL]**
*   *Test:* Can this be asserted to be True or False in a script without LLM interpretation?
*   *Pass Condition:* The field can be expressed as a Python `assert` statement.
*   *Penalty:* If it says "The text flows naturally" or "output is high quality," score = 0.
*   *Penalty:* If a human must make a subjective judgment to verify, score ≤ 3.

**Criterion 2: Pipeline Schema Compliance (Weight 2x)**
*   *Test:* Is the Output Artifact unambiguous enough for a downstream skill to ingest it blindly without parsing errors?
*   *Pass Condition:* Output Artifact specifies exact file format, every required key, and value types.
*   *Penalty:* If Output Artifact says "a report" or "a summary" without exact schema, score = 0.
*   *Penalty:* If any required key is missing from the schema definition, score ≤ 4.

**Criterion 3: Safety Coverage (Weight 1x)**
*   *Test:* Does it explicitly address known LLM behavioral failure modes?
*   *Pass Condition:* Constraints address at least: (a) sycophancy, (b) hallucination, (c) output padding.
*   *Penalty:* If Constraints do not mention any LLM-specific failure mode, score ≤ 3.

#### Synthesis Logic
For each field:
1. Calculate `(Crit1 * 3) + (Crit2 * 2) + (Crit3 * 1)` for both drafts. Record exact scores.
2. **Constraints:** Merge. Take all machine-verifiable rules from Constraint draft AND all LLM behavioral guards from Expansion draft. Produce a unified numbered list.
3. **Output Artifact:** Take the Constraint draft's byte-level schema as the base. Append Expansion's metadata requirements if they don't conflict with the schema.
4. **Success Criteria:** Take the Constraint draft's Python assertions as the base. Append Expansion's semantic checks ONLY if they can be rephrased as measurable assertions (e.g., "output feels relevant" → `assert len(output['evidence_quotes']) >= 1`).

---

### Phase B: The 5-Dimension Self-Evaluation Gate (SkillNet §3.4)

After producing the synthesized output, run the following 5-point quality check.

**1. Safety:** Do the synthesized Constraints cover coach identity leakage, client data privacy, and LLM sycophancy?
- `Good`: All three safety vectors are explicitly addressed.
- `Poor`: Any of the three vectors is missing.

**2. Completeness:** Does the synthesized Output Artifact define: file format, all required keys, all value types, and file path pattern?
- `Good`: All four output dimensions are specified.
- `Poor`: Any dimension is missing.

**3. Executability:** Could an automated test suite verify every Success Criterion without an LLM?
- `Good`: Every criterion is a machine-verifiable assertion.
- `Poor`: Any criterion requires subjective human judgment.

**4. Maintainability:** Can the Constraints be updated independently of the Success Criteria?
- `Good`: No circular references between Constraints and Success Criteria.
- `Poor`: Changing one field requires updating the other.

**5. Cost-awareness:** Does the Success Criteria verification itself stay cheap (no additional LLM calls needed)?
- `Good`: All criteria are structural/mathematical checks.
- `Poor`: Criteria require semantic evaluation (additional LLM invocation).

#### Gate Logic
- If **any dimension scores `Poor`**: `FAILED_SELF_EVAL` — Orchestrator re-invokes the Brainstormer.
- If **all dimensions score `Good` or `Average`**: Output released.

---

## 🚫 Negative Space (Constraints)
*   **NO Redundant Definitions:** A Success Criterion does not redefine the Action. It defines how we PROVE the Action happened correctly.
*   **NO Inferred Schemas:** If the output is JSON, write out the literal keys and types. Do not say "standard format."
*   **NO Skipping Self-Evaluation:** The 5-Dimension Gate is mandatory.

---

## 📦 Output Artifact
**Format:** JSON
**File Path:** `{workspace}/ccbs_output/cluster3_synthesized.json`
**Schema:**
```json
{
  "synthesized_boundaries": {
    "constraints": "string (numbered list, includes both machine rules and LLM behavioral guards)",
    "output_artifact": "string (file format + full key schema + value types + file path)",
    "success_criteria": "string (numbered assertions, each expressible as Python assert)"
  },
  "mcda_trace": {
    "constraints": { "expansion_score": 0, "constraint_score": 0, "winner": "Expansion|Constraint|Hybrid" },
    "output_artifact": { "expansion_score": 0, "constraint_score": 0, "winner": "Expansion|Constraint|Hybrid" },
    "success_criteria": { "expansion_score": 0, "constraint_score": 0, "winner": "Expansion|Constraint|Hybrid" }
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
4. The `constraints` output contains at least 5 numbered rules.
5. The `success_criteria` output contains at least 4 numbered assertions.
6. The `output_artifact` specifies file format, at least 3 required keys, and value types for each.
