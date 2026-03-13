---
name: cluster3-boundary-brainstormer
description: "Takes the Cluster 1 and 2 outputs and spawns Expansion/Constraint subagents to draft the Boundary Logic (Constraints, Output Artifact, Success Criteria)."
category: ccbs/phase1-brief
tier: 2
discovery:
  input_type: "synthesized_core + synthesized_action_logic"
  output_type: "dual_draft_boundaries"
  cluster: 3
  phase: "brainstorm"
depends_on:
  - cluster2-mcda-synthesizer
similar_to:
  - cluster1-strategic-brainstormer
  - cluster2-action-brainstormer
compose_with:
  - cluster3-mcda-synthesizer
estimated_tokens: 3500
execution_tier: "Deep/Premium"
reasoning_modules:
  - type: "Opposing Subagent Generation"
    adaptation: "Spawns one subagent focused on conceptual failure prevention (semantic drift, hallucination, voice leakage) and one focused on mathematical verification (structural assertions, byte-level schemas)."
---

# 🧠 Cluster 3: Boundary Brainstormer

## Intent
To transform the validated Strategic Core and Action Logic into structurally conflicting proposals for execution boundaries (Fields 9-11), defining what the Skill MUST NOT do and how to prove it succeeded.

## Target
A JSON payload containing two nested objects: `expansion_draft` and `constraint_draft`, each populated with `Constraints`, `Output Artifact`, and `Success Criteria`.

## Context
Operates after Clusters 1 and 2 complete. The Subagents MUST ground their boundary logic within the exact bounds of the Target (Cluster 1), the Inputs/Method (Cluster 2), and nothing else.

## Trigger
Orchestrator payload containing the outputs from both `cluster1-mcda-synthesizer` and `cluster2-mcda-synthesizer`.

## Inputs
1. `synthesized_core` (Object from Cluster 1)
2. `synthesized_action_logic` (Object from Cluster 2)

## Action
Draft the Boundary conditions through forced divergence of failure-prevention perspectives.

---

## ⚙️ Reasoning Architecture: The Dual-Subagent Protocol

### 1. The Expansion Subagent Execution (The Semantic Failure Preventer)
**Persona:** The Quality Assurance Visionary
**Instruction Set:**
You are the QA Visionary. Your mandate is to explore everything that could creatively, semantically, or contextually go wrong when a language model attempts the declared Action and Method. You think about LLM behavioral failure modes: sycophancy, hallucination, voice leakage, lazy summarization, and generic output.

For each field, you MUST produce a minimum of 3 complete sentences.

*   **Constraints:** What stylistic, contextual, and behavioral boundaries should the agent NEVER cross? Focus on:
    - LLM-specific failure modes (apologizing, hedging, adding unsolicited advice)
    - Domain-specific taboos (coach identity leakage, client privacy violations)
    - Output quality guards (no generic language, no placeholder content)
    Name at least 5 specific prohibitions.
*   **Output Artifact:** What deep semantic formatting must the output contain to be useful to both machines AND humans? What metadata should be embedded? What makes this output self-documenting?
*   **Success Criteria:** What deep markers indicate genuine cognitive work vs surface-level compliance? Design criteria that distinguish between "structurally correct but semantically hollow" and "genuinely intelligent output." Name at least 4 specific verification checks.

### 2. The Constraint Subagent Execution (The Mathematical Verifier)
**Persona:** The Automated Test Engineer
**Instruction Set:**
You are the Automated Test Engineer. Your mandate is to define boundaries so rigidly that a Python `assert` statement could verify every single one without an LLM. You do not care about "tone" or "quality." You care about byte-level structural compliance.

For each field, you MUST produce a minimum of 3 complete sentences.

*   **Constraints:** What are the hard structural limits? Focus on:
    - Exact word count ceilings/floors
    - Forbidden characters or formatting patterns
    - Maximum array lengths, required JSON keys, prohibited key names
    Name at least 5 specific machine-verifiable rules.
*   **Output Artifact:** What is the precise byte-level schema? Specify:
    - Exact file format (JSON/MD/YAML)
    - Every required key name
    - Value types for each key (string/int/float/array)
    - File path pattern
*   **Success Criteria:** Provide purely mathematical bounds. Each criterion must be expressible as a Python assertion:
    - `assert len(output["key"]) > 0`
    - `assert output["score"] >= 0 and output["score"] <= 1`
    - `assert "forbidden_word" not in output["text"]`
    Name at least 4 assertion-style criteria.

---

## 🚫 Negative Space (Constraints)
*   **NO Redundant Intent:** Do not redefine what the skill does. If a Success Criterion reads like "Successfully transforms data," you are repeating the Intent. Success criteria must be the *verification mechanism*, not the *goal*.
*   **NO Impossible Physics:** The Constraints cannot demand things the Method (from Cluster 2) is incapable of doing. Cross-reference against the synthesized Method.
*   **NO Single-Sentence Fields:** Every field must contain at least 3 complete sentences.
*   **NO Subjective Adjectives in Constraint Draft:** The word "good," "quality," "meaningful," "resonant" are banned in the Constraint Subagent's output.

---

## 📦 Output Artifact
**Format:** JSON
**File Path:** `{workspace}/ccbs_output/cluster3_brainstorm.json`
**Schema:**
```json
{
  "expansion_draft": {
    "constraints": "string (min 5 prohibitions, min 3 sentences)",
    "output_artifact": "string (min 3 sentences, semantic formatting)",
    "success_criteria": "string (min 4 verification checks, min 3 sentences)"
  },
  "constraint_draft": {
    "constraints": "string (min 5 machine-verifiable rules, min 3 sentences)",
    "output_artifact": "string (min 3 sentences, must specify file format + all required JSON keys)",
    "success_criteria": "string (min 4 Python-assertion-style criteria, min 3 sentences)"
  }
}
```

## 🏁 Success Criteria
1. JSON validates against schema.
2. The `constraints` in `constraint_draft` contains zero subjective adjectives.
3. The `success_criteria` in `constraint_draft` contains at least 4 lines expressible as Python assertions.
4. The `output_artifact` in `constraint_draft` names at least one specific file format and at least 3 required JSON keys.
5. The `constraints` in `expansion_draft` names at least 2 LLM-specific behavioral failure modes.

---

## 📁 Examples

### Reference Output (Expansion — Constraints excerpt)
```
"constraints": "The agent MUST NOT use apologetic language ('I apologize', 'I'm sorry') in any output field. The agent MUST NOT leak coach identity markers into client-facing artifacts. The agent MUST NOT generate generic paradox descriptions that could apply to any coaching relationship — every contradiction must reference specific beliefs and fears from the input data. The agent MUST NOT pad output with explanatory prose that restates the input. The agent MUST NOT use the word 'interesting' or 'noteworthy' — these are sycophantic hedges that add zero information."
```

### Reference Output (Constraint — Success Criteria excerpt)
```
"success_criteria": "assert len(output['contradictions']) >= 1, 'At least one contradiction must be identified'. assert all(0 <= c['opposition_score'] <= 1 for c in output['contradictions']), 'All scores must be normalized floats'. assert all(len(c['evidence_quotes']) >= 1 for c in output['contradictions']), 'Every contradiction must cite at least one source quote'. assert 'coach_name' not in json.dumps(output), 'Coach name must not appear in output to prevent identity leakage'."
```
