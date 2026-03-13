# CCBS Skills Audit: Gaps Against SkillNet Signals

## Verdict: The Skills Are Structurally Sound But Operationally Thin

After re-reading SkillNet's architecture against every one of our 6 CCBS Skills, here are the **6 specific gaps** that will cause them to underperform. Each gap maps to a specific SkillNet signal.

---

## Gap 1: Missing the Discovery-Activation-Execution Lifecycle
**SkillNet Signal (§2):** Skills operate through a 3-step progressive process: (1) Discovery — only metadata is loaded, (2) Activation — full instructions loaded on match, (3) Execution — agent follows instructions.

**Our Problem:** Our Skills have no Discovery layer. The `description` field exists in YAML, but it's written for humans, not for an Orchestrator to parse programmatically. If we ever scale to 50+ CCBS skills, the Orchestrator cannot efficiently route based on our current descriptions.

**Fix:** Every CCBS Skill must have a machine-parseable `discovery` block in its YAML frontmatter:
```yaml
discovery:
  input_type: "raw_user_idea | synthesized_core | dual_draft"
  output_type: "dual_draft | synthesized_json"
  cluster: 1 | 2 | 3
  phase: "brainstorm | synthesize"
```
This allows the Orchestrator to select skills by `input_type` → `output_type` matching, not by reading 100-line SKILL.md files.

---

## Gap 2: No Skill Filtering / Deduplication Gate
**SkillNet Signal (§3.3.2):** "Automatic construction of skills does not imply indiscriminate accumulation. SkillNet introduces a data-driven filtering and consolidation pipeline."

**Our Problem:** The current CCBS pipeline generates a Design Brief but has **no mechanism to check if an equivalent Skill already exists** before creating a new one. If a manager requests "Extract paradoxes from SOC batch" and a similar `belief-paradox-extractor` already exists, the pipeline will happily build a duplicate.

**Fix:** Add a **Pre-Flight Deduplication Check** to the Orchestrator:
- Before invoking Cluster 1, the Orchestrator queries the existing Skill Relation Graph for `similar_to` edges.
- If a match with >80% semantic similarity is found, the Orchestrator halts and presents the existing skill to the manager instead of generating a new one.

---

## Gap 3: No Self-Evaluation Layer (The 5-Dimension Rubric Is Declared But Not Enforced)
**SkillNet Signal (§3.4):** "We define five core dimensions to quantitatively characterize the quality and readiness of each skill: Safety, Completeness, Executability, Maintainability, Cost-awareness."

**Our Problem:** Our CCSB paper *describes* these 5 dimensions in Section 10, but **none of the 6 CCBS Skills actually run a self-evaluation**. The Synthesizer Skills output a JSON and stop. They never score their own output against the 5 dimensions.

**Fix:** Add a **Post-Synthesis Evaluation Gate** to each MCDA Synthesizer Skill. After producing the synthesized JSON, the Synthesizer must run an explicit 5-point self-check:
1. **Safety:** Does any field authorize actions outside the Skill's declared input scope?
2. **Completeness:** Are all 4 (or 3) fields populated with non-empty, non-placeholder strings?
3. **Executability:** Could an agent actually execute the Method with only the declared Inputs?
4. **Maintainability:** Is the output modular enough that changing one field won't break others?
5. **Cost-awareness:** Does the Method imply token costs exceeding the `estimated_tokens` budget?

If any dimension scores "Poor", the Synthesizer must flag it and request a re-run of the Brainstormer.

---

## Gap 4: No Relation Graph Edges Between Generated Skills and Existing Skills
**SkillNet Signal (§3.5):** "SkillNet formulates skill analysis as a structured relations discovery problem... `similar_to`, `compose_with`, `belong_to`, `depend_on`."

**Our Problem:** Our CCBS Skills declare `similar_to` and `compose_with` edges to *each other* (Brainstormers link to Brainstormers, Synthesizers link to Synthesizers). But the **output Design Brief** — the actual skill being designed — has no mechanism to auto-generate its relation graph edges to the existing 65+ CCP skills.

**Fix:** Add a **Relation Graph Inference Step** to the Orchestrator's final assembly (Step 5). After compiling the 11-field JSON, the Orchestrator must:
1. Query the existing skill registry for `similar_to` candidates based on the new skill's `intent` and `action`.
2. Infer `compose_with` edges based on the new skill's `output_artifact` schema matching existing skills' `inputs`.
3. Infer `depend_on` edges based on the new skill's `context` and `trigger` requirements.
4. Write these edges into the Design Brief JSON as a `relation_graph` block.

---

## Gap 5: No Closed-Loop Experience Consolidation
**SkillNet Signal (§5.3 / §7):** "After completing a task, the agent proactively invokes `skillnet create` to package the solution as a standardized skill." Also: "Skills serve as the structured interface through which memory becomes executable and workflows become flexible."

**Our Problem:** The CCBS pipeline is one-directional: User idea → Design Brief → SKILL.md. There is no feedback loop. If a generated SKILL.md performs poorly in production, that failure experience is lost. The next Design Brief for a similar capability will repeat the same mistakes.

**Fix:** Define a **Post-Execution Feedback Skill** that:
1. Captures execution traces from production runs of CCBS-generated skills.
2. Extracts failure patterns (e.g., "The Constraint Agent consistently under-specifies the Module field for CMF skills").
3. Updates the relevant Brainstormer Skill's instruction set with learned negative examples.
This creates the closed-loop evolution that SkillNet identifies as the key differentiator between "static package managers" and "self-evolving skill ecosystems."

---

## Gap 6: Skills Lack the "Unified Knowledge Representation" Property
**SkillNet Signal (§2):** "A skill serves as a unified knowledge representation that integrates entities, relationships, workflows, and executable code, encompassing both textual semantics and symbolic outcomes."

**Our Problem:** Our CCBS Skills are purely textual instruction sets. They contain no executable code, no scripts, and no templates. The Brainstormer Skills tell an LLM *what to do* but provide no scaffolding, reference examples, or executable validation scripts.

**Fix:** Each Brainstormer Skill should bundle a **`/examples/` directory** containing:
1. A reference input (`example_input.json`) — a real, production-quality raw user idea.
2. A reference output (`example_output.json`) — the exact expected dual-draft JSON for that input.
3. A validation script (`validate.py` or inline JSON Schema) that programmatically asserts the output schema is correct.

This transforms each Skill from a "textual instruction" into a "self-contained capability package" — exactly what SkillNet defines as the gold standard.

---

## Summary: Priority Order for Upgrades

| Priority | Gap | Impact | Effort |
|----------|-----|--------|--------|
| 🔴 P0 | Gap 3: Self-Evaluation Gate | Prevents hollow briefs from passing | Medium |
| 🔴 P0 | Gap 6: Examples + Validation Scripts | Transforms instructions into executable packages | Medium |
| 🟡 P1 | Gap 1: Discovery Block in YAML | Enables programmatic routing at scale | Low |
| 🟡 P1 | Gap 4: Auto-Generated Relation Graph | Prevents ecosystem fragmentation | Medium |
| 🟢 P2 | Gap 2: Pre-Flight Deduplication | Prevents skill duplication | Low |
| 🟢 P2 | Gap 5: Closed-Loop Feedback | Creates self-evolving ecosystem | High |
