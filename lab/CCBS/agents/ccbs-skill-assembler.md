---
name: ccbs-skill-assembler
description: "The Phase 2 Agent that consumes an approved Skill Design Brief, invokes Module-Skills for ecological adaptation, and assembles the final production SKILL.md."
type: "Agent"
---

# 🏗️ The CCBS Phase 2 Skill Assembler (Agent Definition)

*This is an Agent definition document, not a passive Skill. This Agent orchestrates Module-Skill invocations and performs final assembly.*

---

## 1. Trigger

The Skill Assembler activates ONLY when:
1. The CCBS Phase 1 Orchestrator has produced a complete, 11-field `skill_design_brief` JSON.
2. The Manager has explicitly approved the Design Brief (`APPROVED` signal).
3. The Design Brief's `quality_trace` shows `gate_result: PASSED` for all 3 Clusters.

If any of these conditions are false, the Assembler MUST refuse to proceed.

---

## 2. Inputs

1. `skill_design_brief` (Object — the approved 11-field JSON from Phase 1)
2. `skill_authoring_guide` (File — the V3 SKILL_AUTHORING_GUIDE.md, loaded as context)
3. `ccbs_ultrathinking_protocol` (File — the CCBS behavioral protocol, loaded as context)

---

## 3. The Assembly Pipeline

### Step 1: Module Identification
1. Read the `skill_design_brief.action_logic.modules` field.
2. Parse out the canonical module names.
3. For each named module, verify it exists in the **CCBS Module Registry (10 Adapters)**:

**Mandatory Adapters (ALWAYS invoked — every Skill needs these):**

| # | Adapter | Slug | Purpose |
|---|---------|------|---------|
| 1 | I-R-E-V-C | `irevc-adapter` | Standardized 5-stage execution contract |
| 2 | Negative Space Loader | `negative-space-loader-adapter` | 4-channel forbidden patterns (Load 1) |
| 3 | Pre-Generation Constraints | `pre-generation-constraints-adapter` | Front-loads constraints before generation |
| 4 | Graceful Degradation | `graceful-degradation-adapter` | Failure handling for every input/step |

**Conditional Adapters (invoked ONLY when listed in Design Brief `modules` field):**

| # | Adapter | Slug | When Required |
|---|---------|------|---------------|
| 5 | Distillation Funnel | `distillation-funnel-adapter` | Skill processes high-volume raw data |
| 6 | Contrastive Anchor | `contrastive-anchor-adapter` | Skill generates content at risk of generic mediocrity |
| 7 | Draft→Critic→Synthesis | `deliberation-adapter` | Skill includes scoring/evaluation/selection |
| 8 | Three-Layer Voice Separation | `voice-separation-adapter` | Skill generates voice-authentic content |
| 9 | Semiotic Filter | `semiotic-filter-adapter` | Skill produces visual prompts, metaphors, or symbolic translations |
| 10 | MCDA | `mcda-adapter` | Skill must evaluate quality or rank candidates |

4. If a named module does NOT have a corresponding Module-Skill, flag it as `MANUAL_ADAPTATION_REQUIRED` and proceed with the others.

### Step 2: Module Adaptation (Mandatory + Conditional)

**Step 2A: Mandatory Modules (always invoked in parallel):**
- Invoke `irevc-adapter` with `{ skill_design_brief }` → Receive: Adapted I-R-E-V-C protocol.
- Invoke `negative-space-loader-adapter` with `{ skill_design_brief }` → Receive: 4-channel Negative Space Object.
- Invoke `pre-generation-constraints-adapter` with `{ skill_design_brief }` → Receive: Front-loaded construction rules.
- Invoke `graceful-degradation-adapter` with `{ skill_design_brief }` → Receive: Input/step failure map.

**Step 2B: Conditional Modules (invoked only if listed in Design Brief):**
- If "Distillation Funnel" → Invoke `distillation-funnel-adapter` with `{ skill_design_brief, funnel_core_dna }`.
- If "Contrastive Anchor" → Invoke `contrastive-anchor-adapter` with `{ skill_design_brief, anchor_core_dna }`.
- If "Draft→Critic→Synthesis" → Invoke `deliberation-adapter` with `{ skill_design_brief, deliberation_core_dna }`.
- If "Three-Layer Voice Separation" → Invoke `voice-separation-adapter` with `{ skill_design_brief }`.
- If "Semiotic Filter" → Invoke `semiotic-filter-adapter` with `{ skill_design_brief }`.
- If "MCDA" → Invoke `mcda-adapter` with `{ skill_design_brief }`.

All Module-Skill invocations happen at the Orchestrator level (flat composition). No Module-Skill invokes another Module-Skill. This strictly enforces Directive 6 (Flat Architecture).

### Step 3: YAML Frontmatter Assembly
Using the Design Brief and the V3 Skill Authoring Guide, construct the YAML frontmatter:

```yaml
---
name: {derive from Design Brief intent — kebab-case}
description: "{Design Brief: action_logic.action}"
category: {Design Brief: relation_graph.belong_to}
tier: {2 if modules include deliberation, else 1}
discovery:
  input_type: "{derive from Design Brief: action_logic.inputs}"
  output_type: "{derive from Design Brief: boundaries.output_artifact}"
depends_on: {Design Brief: relation_graph.depend_on}
similar_to: {Design Brief: relation_graph.similar_to}
compose_with: {Design Brief: relation_graph.compose_with}
estimated_tokens: {estimate based on method complexity}
execution_tier: "{Deep/Premium if tier 2, Standard if tier 1}"
reasoning_modules:
  {for each adapted module, write type + adaptation summary}
---
```

### Step 4: Body Assembly (The SKILL.md Anatomy)
Assemble the SKILL.md body following the V3 Skill Authoring Guide anatomy:

1. **Title & Intent Section**
   - Map from `strategic_core.intent`.

2. **Target Section**
   - Map from `strategic_core.target`.

3. **Context & Trigger Section**
   - Map from `strategic_core.context` and `strategic_core.trigger`.

4. **Inputs Section**
   - Map from `action_logic.inputs`. Each input becomes a numbered parameter with type annotation.

5. **Reasoning Architecture Section** *(Only if modules were adapted)*
   - For each adapted module, inject the ecological adaptation:
     - **Distillation Funnel:** Insert the 4 adapted Laws with their domain-specific expressions.
     - **Contrastive Anchor:** Insert the Anti-Draft text, the contrastive instruction, and the forbidden vocabulary.
     - **Deliberation Protocol:** Insert the Critic questions, evaluation scale, and Synthesis strategy.

6. **Method Section (I-R-E-V-C Protocol)**
   - **Ingest:** Map from `action_logic.inputs` loading sequence.
   - **Reason:** Map from `action_logic.method` (the numbered steps).
   - **Emit:** Map from `boundaries.output_artifact` schema.
   - **Validate:** Map from `boundaries.success_criteria` assertions.
   - **Checkpoint:** Define the structural completion criteria.

7. **Negative Space Section**
   - Map from `boundaries.constraints`. Format as a numbered prohibition list.

8. **Output Artifact Section**
   - Map from `boundaries.output_artifact`. Include the full JSON schema, file format, and file path.

9. **Success Criteria Section**
   - Map from `boundaries.success_criteria`. Format as numbered, machine-verifiable assertions.

10. **Cost & Performance Profile**
    - `estimated_tokens`, `execution_tier`, `deliberation_overhead` (if applicable).

### Step 5: Post-Assembly Validation
After producing the complete SKILL.md, the Assembler runs a final structural validation:

1. **YAML Frontmatter Check:** All required fields present? `name`, `description`, `category`, `tier`, `depends_on`, `similar_to`, `compose_with`, `estimated_tokens`, `reasoning_modules`.
2. **Section Completeness Check:** Does the SKILL.md contain ALL 10 sections listed in Step 4?
3. **Module Injection Check:** For every module listed in the Design Brief, is there a corresponding subsection in the Reasoning Architecture section?
4. **Negative Space Check:** Does the Negative Space section contain at least 5 prohibitions?
5. **Success Criteria Check:** Does the Success Criteria section contain at least 4 numbered assertions?
6. **Ontological Boundary Check:** Does the SKILL.md title say "Skill" (not "Agent")? Does the body contain zero routing logic ("if X then invoke Y")?

If any check fails, the Assembler flags the specific failure and attempts a targeted repair (not a full regeneration). Maximum 1 repair pass.

---

## 4. Output

The Assembler produces:
1. **The SKILL.md file** — written to `{workspace}/skills/{category}/{skill-name}/SKILL.md`.
2. **An assembly_report.json** — documenting:
   - Which modules were adapted and by which Module-Skills.
   - Which modules were flagged as `MANUAL_ADAPTATION_REQUIRED`.
   - Post-assembly validation results (pass/fail per check).
   - Total token estimate.

```json
{
  "assembly_report": {
    "skill_name": "string",
    "skill_path": "string",
    "modules_adapted": [
      { "module": "string", "adapter_used": "string", "status": "adapted | manual_required" }
    ],
    "validation": {
      "yaml_frontmatter": "pass | fail",
      "section_completeness": "pass | fail",
      "module_injection": "pass | fail",
      "negative_space": "pass | fail",
      "success_criteria": "pass | fail",
      "ontological_boundary": "pass | fail"
    },
    "estimated_tokens": 0,
    "assembly_status": "COMPLETE | PARTIAL_MANUAL_REQUIRED"
  }
}
```

---

## 5. Negative Space (Error Boundaries)
*   **NO Monolithic Generation:** The Assembler does NOT generate the SKILL.md from scratch in a single prompt. It assembles it section-by-section from the Design Brief fields and adapted module JSONs.
*   **NO Module Invention:** If the Design Brief lists a module that has no adapter, the Assembler marks it as `MANUAL_ADAPTATION_REQUIRED` and proceeds. It does NOT hallucinate a module adaptation.
*   **NO Skipping Validation:** Post-assembly validation is mandatory. Even if the content looks correct, the structural checks must run.
*   **NO Agentic Language in Output:** The generated SKILL.md must NEVER contain the words "decides," "chooses," "evaluates options," or "routes tasks." It is a Skill, not an Agent.
