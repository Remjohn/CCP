---
name: cluster2-action-brainstormer
description: "Takes the Cluster 1 Output and spawns Expansion/Constraint subagents to draft the procedural Action Logic (Inputs, Action, Method, Modules)."
category: ccbs/phase1-brief
tier: 2
discovery:
  input_type: "synthesized_core"
  output_type: "dual_draft_action"
  cluster: 2
  phase: "brainstorm"
depends_on:
  - cluster1-mcda-synthesizer
similar_to:
  - cluster1-strategic-brainstormer
  - cluster3-boundary-brainstormer
compose_with:
  - cluster2-mcda-synthesizer
estimated_tokens: 3500
execution_tier: "Deep/Premium"
reasoning_modules:
  - type: "Opposing Subagent Generation"
    adaptation: "Spawns one procedural expansive subagent to maximize cognitive depth, and one hyper-restrictive subagent to minimize cognitive cost and maximize determinism."
---

# 🧠 Cluster 2: Action Brainstormer

## Intent
To transform the validated Strategic Core into structurally conflicting proposals for procedural execution (Fields 5-8: Inputs, Action, Method, Modules).

## Target
A JSON payload containing two nested objects: `expansion_draft` and `constraint_draft`, each populated with `Inputs`, `Action`, `Method`, and `Modules`.

## Context
Operates after Cluster 1 completes. The Subagents MUST ground their procedural logic within the bounds of the validated Intent and Target provided by Cluster 1. The `synthesized_core` is provided as mandatory context.

## Trigger
Orchestrator payload containing the output from `cluster1-mcda-synthesizer` and the original `raw_user_idea`.

## Inputs
1. `raw_user_idea` (String)
2. `synthesized_core` (Object from Cluster 1)

## Action
Draft the Action Logic through forced procedural divergence.

---

## ⚙️ Reasoning Architecture: The Dual-Subagent Protocol

This Skill does not write the final brief. It executes a managed divergence protocol for procedural mechanics.

### 1. The Procedural Expansion Subagent Execution
**Persona:** The Cognitive Architect
**Instruction Set:**
You are the Cognitive Architect. Your mandate is to draft an expansive, multi-layered procedure. Assume the agent executing this skill has massive reasoning capability and can handle sophisticated cognitive heuristics. Design for maximum intelligence, not minimum cost.

For each field, you MUST produce a minimum of 3 complete sentences explaining the full procedural depth.

*   **Inputs:** What rich datasets could perfectly inform this skill? Name every file type, profile, baseline document, and contextual artifact that would maximize output quality. Express each as a typed variable: `variable_name (Type: description)`.
*   **Action:** What is the overarching cognitive leap this skill makes? Describe the transformation as a conceptual shift, not just a data operation. What intelligence emerges from the operation that didn't exist before?
*   **Method:** What complex series of reasoning steps unlocks the Target? Describe each step as a numbered phase. Include deliberation loops, scoring rubrics, and multi-pass evaluation. Minimum 4 steps.
*   **Modules:** What advanced Cognitive Modules should be composed? The CCBS Registry contains 10 canonical modules: Distillation Funnel, Contrastive Anchor, Draft→Critic→Synthesis, I-R-E-V-C, Negative Space Loader, Three-Layer Voice Separation, Pre-Generation Constraints, Graceful Degradation, Semiotic Filter, MCDA. For each module selected, explain WHY it is needed for this specific skill.

### 2. The Procedural Constraint Subagent Execution
**Persona:** The Systems Optimizer
**Instruction Set:**
You are the Systems Optimizer. Your mandate is to draft the absolute simplest, cheapest, most deterministic procedure possible. You hate complicated reasoning chains. You distrust multi-pass evaluation. Every step must justify its token cost.

For each field, you MUST produce a minimum of 3 complete sentences.

*   **Inputs:** What are the absolute minimum primitive files or strings required? Strip away everything that is "nice to have." Express each as a typed variable: `variable_name (Type: description)`.
*   **Action:** What is the literal data transformation? Express it as: "Maps [precise input structure] to [precise output structure] via [specific algorithm]."
*   **Method:** What is the shortest linear algorithm? No reasoning loops, no deliberation protocols. Just parsing, mapping, and outputting. Maximum 3 steps.
*   **Modules:** What is the single cheapest standard module required to prevent the most common failure mode? Justify why more than one module is unnecessary.

---

## 🚫 Negative Space (Constraints)
*   **Parameter Independence:** Neither subagent may hardcode instance-specific variables. Inputs must be abstract types, never specific coach names, specific file paths, or instance data.
*   **NO Boundary Bleed:** Do not draft output schemas, specific constraints, or success criteria here. Those belong exclusively to Cluster 3.
*   **NO Agentic Routing:** Method CANNOT say "If condition A, invoke Skill X, else invoke Skill Y." Skills strictly execute transformations. If the Method requires an OODA loop, the Skill is structurally invalid and must be reclassified as an Agent.
*   **NO Single-Sentence Fields:** Every field must contain at least 3 complete sentences.
*   **Module Names Must Be Canonical:** Only reference modules from the official CCBS Module Registry. Do not invent module names.

---

## 📦 Output Artifact
**Format:** JSON
**File Path:** `{workspace}/ccbs_output/cluster2_brainstorm.json`
**Schema:**
```json
{
  "expansion_draft": {
    "inputs": "string (min 3 sentences, typed variables)",
    "action": "string (min 3 sentences)",
    "method": "string (min 4 numbered steps)",
    "modules": "string (min 3 sentences, canonical module names only)"
  },
  "constraint_draft": {
    "inputs": "string (min 3 sentences, typed variables)",
    "action": "string (min 3 sentences, must start with 'Maps')",
    "method": "string (max 3 numbered steps)",
    "modules": "string (must name exactly 1 module with justification)"
  }
}
```

## 🏁 Success Criteria
1. JSON validates against schema above.
2. The `action` string in `constraint_draft` starts with the word "Maps".
3. The `method` in `expansion_draft` contains at least 4 numbered steps.
4. The `method` in `constraint_draft` contains at most 3 numbered steps.
5. The `modules` in `constraint_draft` names exactly 1 canonical module.
6. All `inputs` fields use typed variable notation: `variable_name (Type: description)`.
7. No field contains hardcoded instance data (specific names, specific file paths, specific dates).

---

## 📁 Examples

### Reference Input
```json
{
  "raw_user_idea": "Find contradictions between coach beliefs and client fears",
  "synthesized_core": {
    "intent": "Transforms coach_beliefs.json and client_fears.json into contradiction_matrix.json via semantic opposition scoring.",
    "target": "A contradiction_matrix.json with scored belief-fear pairs.",
    "context": "Requires voice-dna-profiler and client-intake-processor outputs.",
    "trigger": "PIPELINE_STAGE_COMPLETE for 'client-intake'."
  }
}
```

### Reference Output (Expansion Draft — Method excerpt)
```
"method": "Step 1: Saturation — Load coach_beliefs.json and client_fears.json into parallel working memory. Parse each belief and fear into semantic embeddings. Step 2: Cross-Matrix Generation — Generate a full N×M matrix of every belief-fear pair combination. Step 3: Opposition Scoring — For each pair, apply the Contrastive Anchor module to score semantic opposition (0 = aligned, 1 = directly contradictory). Use the Distillation Funnel to compress low-opposition pairs below threshold 0.4.  Step 4: Deliberation — Apply Draft→Critic→Synthesis: Draft selects top contradictions, Critic challenges whether opposition is genuine or merely surface-level semantic distance, Synthesis resolves."
```

### Reference Output (Constraint Draft — Method excerpt)
```
"method": "Step 1: Parse coach_beliefs.json and client_fears.json into flat string arrays. Step 2: For each belief-fear pair, calculate cosine distance of TF-IDF vectors; pairs with distance > 0.6 are flagged as contradictions. Step 3: Output flagged pairs as contradiction_matrix.json."
```
