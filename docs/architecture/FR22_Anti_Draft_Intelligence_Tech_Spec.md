# Tech-Spec: FR22 — 3-Level Anti-Draft Intelligence (DEP-PROTO-013)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v4.0 / Script Generation Skill Type Guide v1)
**Architecture Reference:** PRD §CCF Breakthroughs, Script_Generation_Skill_Type_Guide_v1 (Section III)
**Skill Implementation:** `skills/ccf/compiler/anti-draft-intelligence/`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\Architecture_Synthesis_Report.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\Script_Generation_Skill_Type_Guide_v1.docx.md`

---

## 2. Overview

### Problem Statement
Large Language Models inherently regress toward the statistical mean of their training data. When given positive instructions alone (e.g., "Write an inspiring story about overcoming failure"), they act out a generic "vocabulary costume" that passes surface grammar checks but fails L3 emotional resonance. Abstract negative instructions (e.g., "Avoid clichés") are routinely ignored because they do not trigger semantic repulsion at the vector level.

### Solution
FR22 implements the **3-Level Anti-Draft Intelligence** architecture (formally registered as the Anti-Draft Calibration Protocol `DEP-PROTO-013`), utilizing the Law of the Negative Anchor. It forces the system to generate or retrieve concrete, written examples of failure that the generation agent is explicitly instructed to maximize vector distance from. 
- **Level 1 (Archetype):** What generic AI produces for this specific format.
- **Level 2 (Mode/Belief):** The specific culturally held wrong belief (from `M3_UNDENIABLE`) applied to the current psychological routing mode.
- **Level 3 (Voice):** The coach's specific cognitive drift patterns (derived from `DEP-ENG-004`).

### Scope
**In scope:**
- Stage 1: Level 1 ingestion from the `Container Module Library` Phase Template.
- Stage 2: Level 2 dynamic generation via `payload-masking-adapter` cross-referenced with `DEP-ENG-021[M3_UNDENIABLE]`.
- Stage 3: Level 3 injection from the Negative Space Object (`DEP-ENG-004`).
- Stage 4: Contrastive evaluation by the Critic Subagent (Pass 2 of Generation).
- Receipt Chain Guard writes.

**Out of scope:**
- Generation of the raw M3 finding (CRAL Orchestrator handles this).
- Creation of the coach's Voice DNA Profile.

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-021[M3_UNDENIABLE]` | CRAL Finding: Prediction Error | INPUT — Defines the specific wrong belief the audience holds to fuel Level 2. |
| `DEP-ENG-004` | Negative Space Object | INPUT — The primary constraint logic for Level 3 Coach drift. |
| `payload-masking-adapter` | Assembler Adapter | GENERATOR — Builds the compilation-time Level 2 text. |
| `DEP-PROTO-013` | Anti-Draft Calibration Protocol | OUTPUT — The final instructional fence injected into the compiled `SKILL.md`. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Contrastive Chain-of-Thought** | Ling et al. | 2023 | *The Law of the Negative Anchor*: Explicitly generated invalid examples produce measurable semantic distance. Paired contrastive negatives outperform positive-only prompting. |

### Technical Decisions
1. **Semantic Repulsion over Avoidance:** Level 1 is *never* a list of rules to avoid. It must literally be 3-5 sentences of terrible AI cliché. This concrete text acts as a negative semantic anchor in the LLM's vector space.
2. **Absolute First Load Order (M3 Mandate):** `DEP-ENG-004` (Level 3 boundaries) MUST be loaded before *any* positive instruction is given to the agent. This constraints the first token prediction space immediately.
3. **Draft → Critic → Synthesis Loop:** The generation agent generates a draft (Pass 1), a Critic subagent scores it against the 3-Level fence (Pass 2), and if ≥ 1 violations occur, triggers a targeted regenerate (Pass 3).
4. **Ghost Variable Prevention Gate:** All input sources [DEP-ID] must be verified cryptographically prior to payload unpacking. Any field resolving to NULL or UNDEFINED triggers a hard compiler pipeline halt. The error schema emitted is: `{ "error": "DAG_VIOLATION", "missing_dep": "[DEP-ID]" }`
5. **Universal Extension Mandate (The Intuition Baseline):** The 4 Intuition Extensions (SoulResonance, PatternWeaver, GhostContext, AncestralWisdom) activate specifically when the system detects staleness or emotional flatness. Because they fire precisely when generation is exposed to centroid drift, their temporary `SKILL.md` files are bound by a hard Block A invariant: `DEP-ENG-004` MUST load ABSOLUTE FIRST, at structural array index `[0]`, before any positive ideological instructions are delivered. Ideational depth cannot be built on an unanchored foundation.

---

## 4. Implementation Plan

### Stage 1: Level 1 Construction (Block A Invariant Load)
*Agent Name:* JIT Skill Assembler v2.0
*Inputs:* Validated Design Brief Template (Block A).
*Outputs:* Level 1 Anti-Draft Block.
*Failure Condition:* Level 1 contains descriptions (e.g., "avoid tropes") instead of concrete written prose.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Frozen Anchor Generation:** The Level 1 Anti-Draft baseline generation is fundamentally isolated from the premier JIT compiler. The archetype's 'AI Cliché' anchor is intentionally generated by a frozen, low-capability model (e.g., gpt-3.5-turbo) to permanently lock the statistical centroid. The generation agent (running on GPT-4o or equivalent) uses this low-temperature anchor for mathematical semantic repulsion.

**Steps:**
1. Extract the Level 1 block from the static Archetype Container module.
2. Validate the block has 4 required subsections: [Statistical Centroid Prose Example], [Mechanism Failure Diagnosis], [Resolution Failure Diagnosis], [Semantic Distance Instruction].
3. Append to the compiling `SKILL.md` contrastive section.

### Stage 2: Level 2 Generation (Mode & M3 Synthesis)
*Agent Name:* `payload-masking-adapter` (Assembler Tier 2)
*Inputs:* `DEP-ENG-016` (Psychological Brief Mode), `DEP-ENG-021[M3_UNDENIABLE]`.
*Outputs:* The compiled Level 2 Anti-Draft constraint text.
*Failure Condition:* `M3_UNDENIABLE` is missing (CRAL_DEGRADED) preventing the adapter from defining the specific cultural misconception.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Retrieve the target `mood_state` and the specific audience prediction error from `M3`.
2. Construct the mode-failure scenario. 
   - *If Processing Mode:* Instruct that the mechanism is correct but the payload unearned (arriving in paragraph 1 before stakes are felt).
   - *If Escape Mode:* Instruct that the vehicle unfortunately mirrors the audience's L3 pain domain (semantic affinity breach).
3. Inject the `M3` finding explicitly: *"The draft assumes the audience believes [M3 belief]. You must actively tear this assumption down, do not cater to it."*
4. Append to the compiling `SKILL.md` contrastive section.

### Stage 3: Level 3 Injection (Negative Space Load)
*Agent Name:* `negative-space-loader-adapter` (Assembler Tier 1)
*Inputs:* `DEP-ENG-004`.
*Outputs:* Forbidden Vocabulary List.
*Failure Condition:* `DEP-ENG-004` is absent or the extraction regex fails to map the four categories.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Explicitly load `DEP-ENG-004` **FIRST**. Gate PC-03 requires `DEP-ENG-004` to be a flat Array of exact string literals. **Furthermore, PC-03 enforces the L3 Minimum Depth Threshold. The array must contain `count >= 15` exact contrastive strings across the forbidden categories. If the valid array is technically formatted but 'thin' (e.g., `< 15` items), Gate PC-03 triggers an `L3_INSUFFICIENT_DEPTH` halt. The compiler pauses and the Guardian Agent dispatches a Telegram micro-interview to extract more Negative Space anchors before compilation can resume.**
2. Extract the four vectors:
   - Cognitive Load Drift Patterns (sentence openers used when unsure).
   - Professional Register Hedges (latinate substitutions).
   - Performed vs. Lived Vocabulary (aspirational language marked FORBIDDEN-PERFORMED).
   - Structural Shortcuts (e.g., summary bullets).
3. Format as absolute constraints: *"FORBIDDEN STRINGS: [...]"*

### Stage 4: Critic Subagent Enforcement Gate
*Agent Name:* L3-Critic-Subagent
*Inputs:* `draft_v1.md`, The compiled 3-Level Anti-Draft Fence.
*Outputs:* `deliberation_log.json`, `critic_report.json`.
*Failure Condition:* Critic fails to evaluate cleanly due to context window truncation.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Run Pass 1: Emilio standard draft.
2. Spawns the Critic Subagent.
3. Evaluate `draft_v1.md` against the 3 levels.
   - *If Level 1 breach:* Found generic cliché → Score +1 violation.
   - *If Level 2 breach:* Mode payload delivery failed or M3 catered to → Score +1 violation.
   - *If Level 3 breach:* Found Forbidden string → Score +1 violation.
4. *IF violations ≥ 2*: Complete regeneration (Pass 3) passing the `critic_report.json` as the constraint.
5. *IF violations == 1*: Targeted section rewrite.
6. *IF violations == 0*: Pass generation payload.

---

## 5. Primary Output Schema (DEP-PROTO-013 execution metadata)

**Schema Name:** `anti_draft_deliberation_log.json` (Written alongside Final Script)

```json
{
  "compilation_request_id": "REQ-20260313-099",
  "receipt_chain_hash": "ad_fence_44x9a...",
  "validation_pass": {
    "level_1_archetype_loaded": true,
    "level_2_mode_generated": true,
    "level_3_negative_space_loaded": true
  },
  "critic_evaluation": {
    "pass_1_violations": 1,
    "violation_types": ["LEVEL_3_PROFESSIONAL_HEDGE"],
    "targeted_rewrite_triggered": true,
    "pass_2_violations": 0
  },
  "deliberation_override": true,
  "final_semantic_distance_status": "MAXIMIZED"
}
```

---

## 6. Backward Compatibility Fallback
If `DEP-ENG-021[M3_UNDENIABLE]` is absent during Stage 2 compilation (a `CRAL_DEGRADED` scenario):
1. The `payload-masking-adapter` cannot inject the specific cultural misconception. 
2. It falls back to the generic `mode_failure` specification outlined for the target Mood State without the specific belief anchor.
3. Logs `M3_ABSENT_L2_DEGRADED` to the `assembly_report.json`.
*Note: Absence of Level 1 (Archetype) or Level 3 (DEP-ENG-004) are fatal PIPELINE HALTs. There is no fallback for missing invariant structural or core negative space rules.*

---

## 7. Tasks

- [ ] **Task 1:** Build the `negative-space-loader-adapter` ensuring programmatic insertion sequence physically places the output text before the `irevc-adapter` in Phase 1.
- [ ] **Task 2:** Update the `payload-masking-adapter` to read the incoming `DEP-ENG-021` payload, specifically searching for the `M3_UNDENIABLE` key to parse the audience's wrong prediction.
- [ ] **Task 3:** Implement the L3-Critic-Subagent script that handles the evaluation logic. It must return standardized violation arrays to trigger the Synthesis Pass (Pass 3).
- [ ] **Task 4:** Construct the Regex validation gate in Block C (`C-XX`) that scans the drafted `SKILL.md` to guarantee Level 1 contains ≥ 3 sentences of literal prose and not bulleted lists of abstract descriptions.
- [ ] **Task 5:** Implement Receipt Chain Guard writes for all four evaluation stages.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Semantic Repulsion vs Avoidance):** Submitting a Block A Design Brief where Level 1 Anti-Draft is written as "Avoid clichés and generic tone." results in an immediate Block C Compilation failure. *Failure Example:* The system allows the abstract list to pass, leading to Emilio reverting to mean.
- [ ] **AC2 (M3 Wire-up):** An Escape Mode compile targeting the M3 belief "Working harder is the only way out" results in a Level 2 block explicitly commanding the subversion of that exact sentence. *Failure Example:* M3 is loaded but ignored by the payload-masking-adapter, leaving Level 2 generic.
- [ ] **AC3 (First Load Rule):** In the final `SKILL.md` text stream sent to the LLM, the `DEP-ENG-004` Level 3 "Forbidden Strings" appear sequentially *before* the `DEP-ENG-003` Authentic Voice targets. *Failure Example:* Positive constraints load first, nullifying the negative anchor effect on initial token generation.
- [ ] **AC4 (Critic Subagent Rerun):** If the Critic detects 2 violations in the `draft_v1.md`, it automatically halts, purges the draft, and restarts generation with the `critic_report.json` as context. *Failure Example:* The Critic successfully spots 3 violations but just logs them as warnings and passes the flawed script to the user.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| `DEP-ENG-004` | Upstream | Non-negotiable L3 constraint. The coach's Negative Space structure. |
| `DEP-ENG-021` | Upstream | CRAL Finding Index. specifically `M3_UNDENIABLE`. |
| `payload-masking-adapter` | Internal | Adapter responsible for Tier 2 evaluation generation. |
| L3-Critic-Subagent | Internal | Evaluation model invoked during the Generation Loop. |
| Receipt Chain Guard | Infrastructure | Non-negotiable sequence auditing. |

---

## 10. Testing Strategy

### Unit Tests
- **Critic Accuracy Test:** Feed the `L3-Critic-Subagent` an intentionally terrible essay riddled with latinate corporate vocabulary that exists on the Forbidden List. Assert it correctly scores `> 1` violations and targets the exact strings.
- **Level 1 Formatting Test:** Submit a mock template with a single sentence description for Level 1. Assert Block C Rejects it for insufficient prose demonstration. Submit a 4-sentence terrible-AI narrative. Assert it Passes.

### Integration Tests
- **Full Assembly Flow:** Run a complete Design Brief Builder pipeline to JIT Skill compilation. Assert that the resulting `.md` file contains: Header 1 "Archetype Anti-Draft", Header 2 "Mode Specific Anti-Draft (M3)", and Header 3 "Forbidden Coach Vocabulary".
- **Degraded CRAL Flow:** Run a compile with `DEP-ENG-021` missing from the bus. Assert the compile completes successfully but explicitly logs `M3_ABSENT_L2_DEGRADED` inside the Level 2 payload.

### Safety Tests (ADR-01 Strict Isolation)
- **Negative Space Bleed Check:** Compile skills concurrently for Coach A and Coach B. Sabotage Coach A's compile to fail. Verify that in the logging output and prompt generation, Coach B's `FORBIDDEN STRINGS` never appear in Coach A's output stream or memory dump.
