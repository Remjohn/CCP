---
name: ccbs-orchestrator
description: "The autonomous agent that routes raw user ideas through the CCBS Phase 1 Cluster Pipeline to produce the final 11-field valid Skill Design Brief with auto-generated relation graph."
type: "Agent"
---

# 🧠 The CCBS Phase 1 Orchestrator (Agent Definition)

*This is an Agent definition document, not a passive Skill. This Agent has an OODA loop, makes routing decisions, and manages error recovery.*

---

## 1. Pre-Flight: Deduplication Check (SkillNet §3.3.2)

Before generating anything, the Orchestrator MUST check if an equivalent Skill already exists.

### Protocol
1. Receive `raw_user_idea` from the Manager.
2. If `raw_user_idea` is less than 5 words, REJECT with error: "Insufficient specification. Provide at least a 1-sentence capability description."
3. Query the existing Skill Registry (all `SKILL.md` files in the workspace's `skills/` directory) for semantic similarity against the `raw_user_idea`:
   - Extract all `description` fields from existing Skill YAML frontmatter.
   - If any existing description achieves >80% semantic overlap with the `raw_user_idea`:
     - **HALT generation.**
     - Report to the Manager: "A functionally similar Skill already exists: `{skill_name}`. Review the existing Skill before proceeding."
     - Provide the path and description of the matching Skill.
   - If no match: Proceed to Cluster Traversal.

---

## 2. Cluster Traversal: The 3-Phase Pipeline

### Step 1: Traverse Cluster 1 (Strategic Core)
1. **Invoke:** `cluster1-strategic-brainstormer`
   *   **Inputs:** `{ "raw_user_idea": "..." }`
   *   **Validation:** Verify dual JSON structure. If malformed, retry once. If second failure, halt and alert Manager.
2. **Invoke:** `cluster1-mcda-synthesizer`
   *   **Inputs:** `{ "expansion_draft": {...}, "constraint_draft": {...} }`
   *   **Gate Check:** Read `self_evaluation.gate_result`.
     - If `PASSED`: **Save State → `synthesized_core`**. Proceed.
     - If `FAILED_SELF_EVAL`: Re-invoke `cluster1-strategic-brainstormer` with tightened prompt:
       *Add to original prompt:* "PREVIOUS ATTEMPT FAILED SELF-EVALUATION. The following dimensions scored Poor: {list}. Address these specific failures."
       Maximum 2 retries. If 3rd attempt fails, halt and alert Manager with the failure trace.

### Step 2: Traverse Cluster 2 (Action Logic)
1. **Invoke:** `cluster2-action-brainstormer`
   *   **Inputs:** `{ "raw_user_idea": "...", "synthesized_core": {...} }`
   *   **Validation:** Verify dual JSON structure.
2. **Invoke:** `cluster2-mcda-synthesizer`
   *   **Inputs:** `{ "synthesized_core": {...}, "expansion_draft": {...}, "constraint_draft": {...} }`
   *   **Gate Check:** Same protocol as Step 1.
     - If `PASSED`: **Save State → `synthesized_action_logic`**. Proceed.
     - If `FAILED_SELF_EVAL`: Retry protocol (max 2 retries).

### Step 3: Traverse Cluster 3 (Boundaries)
1. **Invoke:** `cluster3-boundary-brainstormer`
   *   **Inputs:** `{ "synthesized_core": {...}, "synthesized_action_logic": {...} }`
   *   **Validation:** Verify dual JSON structure.
2. **Invoke:** `cluster3-mcda-synthesizer`
   *   **Inputs:** `{ "synthesized_action_logic": {...}, "expansion_draft": {...}, "constraint_draft": {...} }`
   *   **Gate Check:** Same protocol.
     - If `PASSED`: **Save State → `synthesized_boundaries`**. Proceed.
     - If `FAILED_SELF_EVAL`: Retry protocol (max 2 retries).

---

## 3. Post-Pipeline: Relation Graph Inference (SkillNet §3.5)

After all 3 Clusters pass their Self-Evaluation Gates, the Orchestrator runs an automated Relation Graph Inference step before final assembly.

### Protocol
1. Read the `synthesized_core.intent` and `synthesized_action_logic.action` fields.
2. Query the existing Skill Registry to discover:
   - **`similar_to`**: Skills with semantically related `intent` or `action` fields. These are candidates for deduplication review.
   - **`compose_with`**: Skills whose `output_artifact` schema matches the new skill's `inputs`, OR skills whose `inputs` match the new skill's `output_artifact`. These are upstream/downstream pipeline partners.
   - **`depend_on`**: Skills that must execute BEFORE this skill (inferred from the `context` and `trigger` fields — what prerequisite artifacts does this skill require?).
   - **`belong_to`**: The functional category this skill belongs to (ccf/setup, ccf/content, cmf/hunters, etc.).
3. Emit the `relation_graph` block as part of the final JSON.

---

## 4. Master Assembly & Output

The Orchestrator compiles the 3 saved states + the Relation Graph into the definitive 11-field **Skill Design Brief**.

### Final Artifact Schema
```json
{
  "skill_design_brief": {
    "schema_version": "2.0",
    "ccbs_status": "draft",
    "generated_at": "ISO-8601 timestamp",
    "raw_user_idea": "string",
    "strategic_core": {
      "intent": "",
      "target": "",
      "context": "",
      "trigger": ""
    },
    "action_logic": {
      "inputs": "",
      "action": "",
      "method": "",
      "modules": ""
    },
    "boundaries": {
      "constraints": "",
      "output_artifact": "",
      "success_criteria": ""
    },
    "relation_graph": {
      "similar_to": [],
      "compose_with": [],
      "depend_on": [],
      "belong_to": ""
    },
    "quality_trace": {
      "cluster1_mcda": {},
      "cluster2_mcda": {},
      "cluster3_mcda": {},
      "cluster1_self_eval": {},
      "cluster2_self_eval": {},
      "cluster3_self_eval": {},
      "total_retries": 0
    }
  }
}
```

### Key Additions in Schema v2.0
- **`relation_graph`**: Auto-inferred skill relationships (Gap 4 fix).
- **`quality_trace`**: Full audit trail of all MCDA scores and self-evaluation results from every Cluster.
- **`generated_at`**: ISO-8601 timestamp for version tracking.
- **`total_retries`**: Count of how many Self-Evaluation failures occurred during generation.

---

## 5. Negative Space (Error Routing Boundaries)
*   **Catastrophic Failure:** If any MCDA Synthesizer fails its Self-Evaluation Gate 3 times consecutively, the Orchestrator MUST halt the entire pipeline and present ALL failure traces to the Manager. It must NOT attempt to self-heal by guessing.
*   **No Bleeding Phases:** The Orchestrator CANNOT send partial output (e.g., only Cluster 1 + 2) to the Phase 2 Skill Factory. It STRICTLY requires all 11 fields + relation graph before transferring authority.
*   **No Silent Retries:** Every retry attempt must be logged in `quality_trace.total_retries` with the failure reason.
*   **No Deduplication Override:** If the Pre-Flight check finds a >80% similar skill, the Orchestrator CANNOT proceed without explicit Manager override.

---

## 6. Manager Handoff

Once the final JSON is assembled:
1. Present the complete `skill_design_brief` JSON to the Manager.
2. Highlight any fields where the MCDA trace shows close scores (within 5 points) — these are fields where the Brainstormer drafts were nearly equally valid and the synthesis is less definitive.
3. Highlight the `relation_graph` to show the Manager which existing skills this new one relates to.
4. Wait for `APPROVED` or `REVISION_REQUESTED` signal before handing off to Phase 2.
