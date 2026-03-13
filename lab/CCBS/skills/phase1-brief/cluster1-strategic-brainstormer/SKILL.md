---
name: cluster1-strategic-brainstormer
description: "Takes a raw user capability idea and spawns Expansion/Constraint subagents to draft the Strategic Core of a Phase 1 Skill Design Brief (Intent, Target, Context, Trigger)."
category: ccbs/phase1-brief
tier: 2
discovery:
  input_type: "raw_user_idea"
  output_type: "dual_draft_strategic"
  cluster: 1
  phase: "brainstorm"
depends_on: []
similar_to:
  - cluster2-action-brainstormer
  - cluster3-boundary-brainstormer
compose_with:
  - cluster1-mcda-synthesizer
estimated_tokens: 3500
execution_tier: "Deep/Premium"
reasoning_modules:
  - type: "Opposing Subagent Generation"
    adaptation: "Spawns one strategic maximizer and one procedural restrictor to force cognitive tension around environment variables."
---

# 🧠 Cluster 1: Strategic Brainstormer

## Intent
To transform a raw user concept into two structurally distinct proposals for the Strategic Core (Fields 1-4) of a Phase 1 Skill Design Brief.

## Target
A JSON payload containing two nested objects: `expansion_draft` and `constraint_draft`, each populated with `Intent`, `Target`, `Context`, and `Trigger`.

## Context
Operates as the very first step in the CCBS Phase 1 Pipeline. Triggered directly by the CCBS Orchestrator when a new Skill request is instantiated.

## Trigger
Orchestrator payload containing the `raw_user_idea` string.

## Inputs
1. `raw_user_idea` (String)

## Action
Draft the Strategic Core through forced cognitive divergence.

---

## ⚙️ Reasoning Architecture: The Dual-Subagent Protocol

This Skill does not write the final brief. It executes a managed divergence protocol that forces two opposing cognitive stances to generate structurally incompatible drafts, maximizing the MCDA Synthesizer's comparative leverage downstream.

### 1. The Expansion Subagent Execution
**Persona:** The Ecosystem Strategist
**Instruction Set:**
You are the Expansion Strategist. Your single mandate is to draft the Strategic Core of this skill to maximize organizational impact and strategic leverage. Ignore exact implementation details entirely. Answer the profound 'Why' behind this capability.

For each field, you MUST produce a minimum of 2 complete sentences. Single-phrase answers are structurally invalid.

*   **Intent:** What is the highest-level architectural purpose of this capability? Why does this transformation need to exist in the pipeline? What systemic gap does it fill?
*   **Target:** What is the visionary end-state when this succeeds? Describe the data payload that exists afterwards AND the organizational consequence it enables.
*   **Context:** What is the broadest environmental zone this skill could operate within? What upstream pipelines feed into it, and what downstream consumers depend on it?
*   **Trigger:** What conceptual event or pipeline state-change demands this capability?

### 2. The Constraint Subagent Execution
**Persona:** The Systems Auditor
**Instruction Set:**
You are the Procedural Restrictor. Your single mandate is to draft the Strategic Core so rigidly that a machine parser could verify every field without subjective interpretation. You hate vague language. You distrust adjectives. You demand exact digital primitives.

For each field, you MUST produce a minimum of 2 complete sentences. Single-phrase answers are structurally invalid.

*   **Intent:** What is the single, isolated functional transformation this skill performs? Express it as: "Transforms [Input Type] into [Output Type] by applying [Specific Operation]."
*   **Target:** What is the exact digital footprint left behind? Name the file format, the JSON keys, or the database state change.
*   **Context:** What are the absolute minimum prerequisite states required for execution? Name the exact files, environment variables, or pipeline outputs that must exist.
*   **Trigger:** What is the exact digital event (webhook, file drop, pipeline state change, Orchestrator signal) that fires this? No conceptual triggers — only observable system events.

---

## 🚫 Negative Space (Constraints)
*   **NO L3 (Implementation) Detail:** Neither subagent is allowed to write algorithm steps, prompt constraints, scoring rubrics, or output schemas. This is CLUSTER 1. Stay in the Strategic Core.
*   **NO Synthesis:** Do not combine the outputs. Keep them absolutely isolated to enforce cognitive tension for the downstream Synthesizer.
*   **NO Placeholders:** Output precise language, not `[Insert Target here]` or `TBD`.
*   **NO Single-Sentence Fields:** Every field must contain at least 2 complete sentences to ensure structural depth.

---

## 📦 Output Artifact
**Format:** JSON
**File Path:** `{workspace}/ccbs_output/cluster1_brainstorm.json`
**Schema:**
```json
{
  "expansion_draft": {
    "intent": "string (min 2 sentences)",
    "target": "string (min 2 sentences)",
    "context": "string (min 2 sentences)",
    "trigger": "string (min 2 sentences)"
  },
  "constraint_draft": {
    "intent": "string (min 2 sentences, must start with 'Transforms')",
    "target": "string (min 2 sentences, must name file format or JSON keys)",
    "context": "string (min 2 sentences, must name specific prerequisite files)",
    "trigger": "string (min 2 sentences, must name observable system event)"
  }
}
```

## 🏁 Success Criteria
1. JSON validates against schema above.
2. The `intent` string in `constraint_draft` starts with the word "Transforms".
3. The `target` string in `constraint_draft` names at least one concrete file format or JSON key.
4. The `trigger` string in `constraint_draft` names an observable system event, not a conceptual trigger.
5. Every field in both drafts contains a minimum of 2 complete sentences.
6. The semantic distance between expansion and constraint versions of the same field is maximized (no paraphrasing — genuinely distinct cognitive stances).

---

## 📁 Examples

### Reference Input
```json
{
  "raw_user_idea": "Make a skill that finds contradictions between a coach's stated beliefs and their clients' reported fears."
}
```

### Reference Output (Expansion Draft)
```json
{
  "intent": "To surface the invisible fault lines between a coach's conscious belief system and the unconscious fear patterns their clients experience. This capability transforms the coaching relationship from one of assumed alignment into one of evidenced tension, revealing where a coach's methodology may inadvertently reinforce the very patterns their clients are trying to break.",
  "target": "A Paradox Map artifact that visualizes the specific points of contradiction between stated coach principles and documented client fears. This map serves as the foundation for the coach's self-awareness development and enables targeted refinement of their methodology.",
  "context": "Operates within the CCF coaching pipeline after both the Voice DNA Profiler has captured the coach's belief architecture and the Client Intake system has documented client fear patterns. Downstream, the Paradox Map feeds into the Strategy Refinement engine.",
  "trigger": "When a complete coaching engagement dataset exists — meaning both coach belief profiles and client fear inventories are available for the same coaching relationship."
}
```

### Reference Output (Constraint Draft)
```json
{
  "intent": "Transforms a coach_beliefs.json array and a client_fears.json array into a contradiction_matrix.json by applying semantic opposition scoring between each belief-fear pair. The skill performs no interpretation — it identifies structural contradictions through vector distance measurement.",
  "target": "A contradiction_matrix.json file containing an array of objects, each with keys: belief_id, fear_id, opposition_score (float 0-1), and evidence_quotes (array of strings). The file is written to the pipeline output directory.",
  "context": "Requires two prerequisite files: coach_beliefs.json (output of voice-dna-profiler) and client_fears.json (output of client-intake-processor). Both files must exist in the pipeline workspace and conform to their respective JSON schemas.",
  "trigger": "Orchestrator emits a PIPELINE_STAGE_COMPLETE event for stage 'client-intake' with payload containing paths to both coach_beliefs.json and client_fears.json."
}
```
