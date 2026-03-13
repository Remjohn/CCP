---
name: cluster1-mcda-synthesizer
description: "Takes the expansion and constraint drafts for the Strategic Core, scores them against the 3-axis MCDA rubric, runs a 5-dimension self-evaluation, and synthesizes the final 4 fields."
category: ccbs/phase1-brief
tier: 2
discovery:
  input_type: "dual_draft_strategic"
  output_type: "synthesized_core"
  cluster: 1
  phase: "synthesize"
depends_on:
  - cluster1-strategic-brainstormer
similar_to:
  - cluster2-mcda-synthesizer
  - cluster3-mcda-synthesizer
compose_with: []
estimated_tokens: 3000
execution_tier: "Deep/Premium"
reasoning_modules:
  - type: "MCDA Matrix"
    adaptation: "Evaluates L1 strategy vs L3 determinism using weighted architectural validity."
  - type: "Self-Evaluation Gate"
    adaptation: "Post-synthesis 5-dimension quality check (Safety, Completeness, Executability, Maintainability, Cost-awareness) before output release."
---

# 🧠 Cluster 1: MCDA Synthesizer

## Intent
To calculate the optimal synthesis of the Strategic Core by applying rigorous mathematical scoring to divergent proposals, then self-evaluating the result before release.

## Target
The finalized, self-evaluated JSON payload containing the validated `Intent`, `Target`, `Context`, and `Trigger` fields for the Phase 1 Design Brief.

## Context
Operates immediately after `cluster1-strategic-brainstormer`. Only executes if the Brainstormer output is schema-compliant.

## Trigger
Receives the two-draft JSON payload from the Orchestrator.

## Inputs
1. `expansion_draft` (Object — 4 strategic fields)
2. `constraint_draft` (Object — 4 procedural fields)

## Action
Score conflicting drafts via MCDA, synthesize the master strategic core, then validate via the 5-Dimension Self-Evaluation Gate.

---

## ⚙️ Reasoning Architecture

### Phase A: The 3-Axis MCDA Protocol

For each of the four fields (Intent, Target, Context, Trigger), the Agent MUST explicitly execute the following scoring matrix in its working memory before writing the final output. The Agent MUST show the numerical scores in the `mcda_trace` output — not just the winner label.

#### The Scoring Matrix (1-10 Scale)

**Criterion 1: Architectural Validity (Weight 3x)**
*   *Test:* Does this describe a Skill procedure (passive instruction set) or an Agentic behavior (autonomous routing)?
*   *Pass Condition:* The field describes what HAPPENS, not what the Skill DECIDES.
*   *Penalty:* If it requires the Skill to make routing decisions ("if X then do Y"), score = 0.
*   *Penalty:* If it uses the word "decides," "chooses," or "evaluates options," score ≤ 2.

**Criterion 2: Procedural Determinism (Weight 2x)**
*   *Test:* Can a machine verify this without subjective interpretation?
*   *Pass Condition:* The field references concrete artifacts, file formats, or system events.
*   *Penalty:* If it uses words like "feels," "good," "creative," "resonates," "quality," or "meaningful," score ≤ 3.
*   *Penalty:* If a human would need to read the field twice to understand what it means, score ≤ 5.

**Criterion 3: Strategic Alignment (Weight 1x)**
*   *Test:* Does it capture the fundamental "Why" behind the capability?
*   *Pass Condition:* A manager reading only this field would understand the skill's pipeline purpose.

#### Synthesis Logic
For each field:
1. Calculate `(Crit1 * 3) + (Crit2 * 2) + (Crit3 * 1)` for both the Expansion and Constraint drafts.
2. Record the exact numerical scores in the `mcda_trace`.
3. If Constraint draft wins: Use it as the base. Append **exactly 1 sentence** from Expansion draft to add strategic context. Do not exceed 1 sentence.
4. If Expansion draft wins: Rewrite it entirely using the vocabulary precision of the Constraint draft. Replace every subjective adjective with a concrete noun or verb.
5. If scores are tied (within 2 points): Default to Constraint-heavy logic. Append Expansion's strategic "Why" as a parenthetical.

---

### Phase B: The 5-Dimension Self-Evaluation Gate (SkillNet §3.4)

After producing the synthesized output, the Agent MUST run the following 5-point quality check. Each dimension is scored as `Good | Average | Poor`.

**1. Safety:** Does any synthesized field authorize actions outside the Skill's declared input scope? Does any field implicitly grant the Skill access to data it should not touch (e.g., other coaches' profiles)?
- `Good`: All fields stay within declared scope.
- `Poor`: Any field implies access to undeclared data.

**2. Completeness:** Are all 4 fields populated with non-empty, non-placeholder, multi-sentence strings?
- `Good`: All 4 fields contain ≥2 sentences with concrete content.
- `Poor`: Any field is empty, placeholder, or single-sentence.

**3. Executability:** Could an agent receiving only the `synthesized_core` JSON understand what this Skill does without reading any other document?
- `Good`: The JSON is self-explanatory.
- `Poor`: The JSON requires external context to interpret.

**4. Maintainability:** If one field changes (e.g., the Trigger), would the other 3 fields still be valid?
- `Good`: Fields are logically independent.
- `Poor`: Fields contain cross-references that would break on modification.

**5. Cost-awareness:** Does the synthesized strategic scope imply a Skill that would exceed 8,000 tokens to execute?
- `Good`: Scope is bounded and focused.
- `Poor`: Scope implies multi-document processing or open-ended generation.

#### Gate Logic
- If **any dimension scores `Poor`**: Output is flagged as `FAILED_SELF_EVAL`. The Orchestrator MUST re-invoke the Brainstormer with a tightened constraint prompt.
- If **all dimensions score `Good` or `Average`**: Output is released.

---

## 🚫 Negative Space (Constraints)
*   **NO Halving:** Do not merge the two drafts into a bloated paragraph. Synthesis means extracting the rigid frame and filling it with the highest-leverage strategy.
*   **NO Implementation Bleed:** Do not add Actions, Methods, or Modules to the output. Only resolve the 4 fields assigned to this Cluster.
*   **NO Skipping Self-Evaluation:** The 5-Dimension Gate is mandatory. If you skip it, the output is structurally invalid regardless of content quality.

---

## 📦 Output Artifact
**Format:** JSON
**File Path:** `{workspace}/ccbs_output/cluster1_synthesized.json`
**Schema:**
```json
{
  "synthesized_core": {
    "intent": "string (min 2 sentences)",
    "target": "string (min 2 sentences)",
    "context": "string (min 2 sentences)",
    "trigger": "string (min 2 sentences)"
  },
  "mcda_trace": {
    "intent": { "expansion_score": 0, "constraint_score": 0, "winner": "Expansion|Constraint" },
    "target": { "expansion_score": 0, "constraint_score": 0, "winner": "Expansion|Constraint" },
    "context": { "expansion_score": 0, "constraint_score": 0, "winner": "Expansion|Constraint" },
    "trigger": { "expansion_score": 0, "constraint_score": 0, "winner": "Expansion|Constraint" }
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
1. JSON validates against schema above.
2. The `mcda_trace` contains exact numerical scores, not just winner labels.
3. The `self_evaluation.gate_result` is `PASSED`.
4. The synthesized fields contain no generative AI fluff; they are rigid architectural constraints.
5. Every synthesized field contains a minimum of 2 complete sentences.

---

## 📁 Examples

### Reference Input
*(Two drafts from the Brainstormer example in `cluster1-strategic-brainstormer`)*

### Reference Output
```json
{
  "synthesized_core": {
    "intent": "Transforms a coach_beliefs.json array and a client_fears.json array into a contradiction_matrix.json by applying semantic opposition scoring between each belief-fear pair. This surfaces the invisible fault lines between a coach's explicit methodology and their clients' experienced reality, enabling evidence-based coaching refinement.",
    "target": "A contradiction_matrix.json file containing an array of scored belief-fear pairs with opposition_score (float 0-1) and evidence_quotes. This artifact enables the downstream Strategy Refinement engine to generate targeted coaching adjustments.",
    "context": "Requires voice-dna-profiler output (coach_beliefs.json) and client-intake-processor output (client_fears.json) to exist in the pipeline workspace. Operates within the CCF coaching pipeline after both intake stages complete.",
    "trigger": "Orchestrator emits a PIPELINE_STAGE_COMPLETE event for stage 'client-intake' with payload containing valid paths to both prerequisite JSON files."
  },
  "mcda_trace": {
    "intent": { "expansion_score": 32, "constraint_score": 38, "winner": "Constraint" },
    "target": { "expansion_score": 28, "constraint_score": 42, "winner": "Constraint" },
    "context": { "expansion_score": 30, "constraint_score": 40, "winner": "Constraint" },
    "trigger": { "expansion_score": 22, "constraint_score": 48, "winner": "Constraint" }
  },
  "self_evaluation": {
    "safety": "Good",
    "completeness": "Good",
    "executability": "Good",
    "maintainability": "Good",
    "cost_awareness": "Good",
    "gate_result": "PASSED"
  }
}
```
