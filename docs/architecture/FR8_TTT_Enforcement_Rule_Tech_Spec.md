# Tech-Spec: FR8 — TTT Enforcement Rule (Temperature, Texture, Tone)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v2.1)
**Architecture Reference:** §7.1 (JIT Skill Assembler v2.0), §6.3 (Governance Ministers), Script_Generation_Skill_Type_Guide_v1.0 §I Mandate M-02, §II Variants-vs-Invariants Test, §III.2 Field 4 Trigger, §VIII Block C Pre-Flight Gate Design
**Source:** [Script_Generation_Skill_Type_Guide_v1.0](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/CCP%20update/CCP_Script_Generation_Skill_Type_Guide_v1.0.docx.md) §M-02, [CCP_Evolution_Architecture_Report_V3](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/CCP%20update/CCP_Evolution_Architecture_Report_V3.docx.md) §Block C, [CCP_Evolution_Architecture_Report_V4](file:///d:/Work/The%20Conscious%20Coaching%20Factory/lab/CCP%20update/CCP_Evolution_Architecture_Report_V4.docx.md) §Trigger-First Engine Inversion

---

## Overview

### Problem Statement

Statistical centralization is the default failure mode of LLM-based content generation. Given positive instructions ("write in a warm, empathetic tone"), the model converges on the statistical centroid of its training data for "warm, empathetic tone" — a register that is technically correct, emotionally dead, and indistinguishable from every other "warm, empathetic" output it has ever generated. This is the mean-reversion problem.

TTT (Temperature, Texture, Tone) is the coach's emotional frequency — the specific combination of emotional intensity (Temperature), stylistic surface quality (Texture), and vocal register (Tone) that makes their voice irreducibly theirs. If TTT is hardcoded into Design Brief Templates, Skills, or compiled outputs, two catastrophic failures occur:

1. **iRAV collapse (Cooney, 2021):** The iRAV framework demonstrates that virality is predicted by the intensity of authentic emotional peaks — not average tone. A pre-specified TTT value produces average tone by definition. The emotional peaks that drive audience engagement are the moments where the coach's emotional state departs from their average — and a hardcoded TTT value mechanically prevents this departure.

2. **Template universality destruction:** A Design Brief Template with a hardcoded TTT value is only valid for compilations at that specific emotional temperature. The same archetype compiled for a coach at TTT-03 (reflective, introspective) and TTT-08 (high-conviction, boundary-staking) requires fundamentally different emotional access. A hardcoded value forces every compilation into one register, violating the Variants-vs-Invariants Test ("Is this statement true for every compilation of this archetype, regardless of coach, mood state, cohort, or date?").

The legacy system had no mechanical enforcement. TTT values could appear in Block A, Block B, or template instructions without detection. The result: emotionally static skills that sounded like the same person regardless of context.

### Solution

A three-layer enforcement architecture:

1. **Authoring Layer (Prevention):** Mandate M-02 of the Script Generation Skill Type Guide prohibits any TTT value in any Block A or Block B field. Template authors are trained that TTT is an undefined runtime value — not a compilation variable.

2. **Compilation Layer (Detection):** Block C check C-08 in the JIT Skill Assembler v2.0 Tier 0 pre-flight mechanically scans all Block B fields for hardcoded TTT values. Any detection → immediate REJECT status. No assembly begins.

3. **Runtime Layer (Resolution):** TTT is resolved dynamically at production time via the Authentication Certificate (DEP-ENG-005). The coach's authenticated emotional state — verified by LIWC-22 from their session voice note — determines the TTT value for that specific compilation. Each production session receives contextually accurate emotional temperature.

### Scope

**In scope:**
- M-02 Mandate enforcement specification
- Block C C-08 validation gate (detection logic, scanning algorithm, rejection protocol)
- TTT runtime resolution via DEP-ENG-005 Authentication Certificate
- TTT natural affinity range (advisory system for archetype-appropriate temperature windows)
- JIT Skill Assembler v2.0 Tier 0 integration
- Template authoring compliance rules
- Acceptance criteria and testing strategy

**Out of scope:**
- Full JIT Skill Assembler v2.0 architecture (separate spec — covers all 10 Block C checks + 4 tiers)
- Sacred Audio extraction mechanics (FR2 — produces LIWC-22 data)
- Voice DNA extraction mechanics (FR3 — produces DEP-ENG-003/004)
- Content generation pipeline (FR1 — downstream consumer)
- Anti-Draft Three-Level Architecture (FR22 — related but separate enforcement)
- CRAL Wiring Protocol (FR-CRAL — separate spec)

---

## Context for Development

### Architecture Traceability

| DEP-ID | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-005` | Authentication Certificate (TTT Baseline) | PRIMARY RUNTIME SOURCE — the ONLY permitted source for TTT resolution |
| `DEP-ENG-003` | Positive Space (Voice DNA) | CONTEXT — vocal authority patterns inform TTT natural affinity range |
| `DEP-ENG-004` | Negative Space | CONTEXT — drift patterns confirm when TTT is being defaulted vs. authentically expressed |
| `DEP-LIB-001` | Emotional DNA Profile | CONTEXT — appraisal architecture influences emotional peak detection |
| `DEP-ENG-016` | Psychological Routing Brief | DOWNSTREAM — receives the resolved TTT and routes to mood-appropriate content strategy |

### The TTT System — What It Is

| Component | Definition | Scale |
|---|---|---|
| **Temperature** | Emotional intensity — how much emotional energy the coach is channeling into this content | TTT-01 (minimal emotional charge) → TTT-10 (maximum emotional intensity) |
| **Texture** | Stylistic surface quality — the grain, roughness, and polish of the language | Raw/unpolished ↔ Crafted/literary |
| **Tone** | Vocal register — the emotional mode the coach's voice occupies | Reflective / Confrontational / Nurturing / Instructional / etc. |

**Critical distinction:** TTT is not a setting. It is a measurement. The coach's TTT for a given production session is determined by their authenticated emotional state at the moment of recording — not by the template, not by the archetype, not by the operator.

### Academic Grounding

| Concept | Framework | Why It Matters for TTT |
|---|---|---|
| iRAV — intensity of emotional peaks predicts virality | Cooney (2021) *iRAV: Intensity of Reflected Affect in Virality* | Pre-specified TTT flattens emotional peaks to a static average. The emotional variance that drives engagement is eliminated. |
| Statistical centralization / mean-reversion | Ling et al. (2023) *Contrastive Chain-of-Thought* | LLMs default to the centroid of training examples matching positive instructions. A hardcoded TTT provides the centroid a specific target to converge on — making mean-reversion MORE likely, not less. |
| Specification gaming | Krakovna et al. (2022) *Specification Gaming* | The model satisfies the TTT specification while violating the spirit of authentic voice expression. "Write at TTT-07" produces content that satisfies TTT-07 surface markers while lacking the authentic conviction that makes TTT-07 content recognizable. |
| Linguistic relativity (Whorf-Sapir) | Sapir (1929); Whorf (1956) | The vocabulary structure determines emotional experience before semantic content is processed. TTT sets the vocabulary structure — hardcoding it means every compilation reaches for the same vocabulary set. |
| LIWC-22 authenticity scoring | Pennebaker et al. (2015) | The Authentication Certificate (DEP-ENG-005) is grounded in LIWC-22 validation of the coach's voice note. The LIWC-22 score confirms the emotional state is authentic, not performed. |

### Key Files

| File | Purpose |
|---|---|
| `lab/CCP update/CCP_Script_Generation_Skill_Type_Guide_v1.0.docx.md` | Primary authoring doctrine — M-02 mandate definition |
| `lab/CCP update/CCP_Evolution_Architecture_Report_V3.docx.md` | C-08 check definition in Block C pre-flight |
| `lab/CCP update/CCP_Evolution_Architecture_Report_V4.docx.md` | Trigger-First Engine Inversion context |
| Design Brief Templates (all archetypes) | Templates that must comply with M-02 |
| `ttt_baseline.json` (DEP-ENG-005) | The Authentication Certificate — runtime resolution source |
| `assembly_report.json` | JIT Assembler output — records C-08 pass/fail |

### Technical Decisions

| Decision | Rationale |
|---|---|
| **C-08 at Tier 0 (zero tokens, zero generation)** | TTT violation is a structural error, not a generation quality issue. Detecting it after generation is wasteful — all tokens spent on the rejected compilation are wasted. Tier 0 catches it before any computational cost is incurred. |
| **REJECT, not DOWNGRADE or FLAG** | A hardcoded TTT value is not a degraded condition — it is a template authoring error. The template itself must be corrected and resubmitted. Allowing a DOWNGRADE would compile the skill with the hardcoded value intact, defeating the entire enforcement mechanism. |
| **TTT natural affinity range as ADVISORY, not GATE** | Each archetype has a temperature range where it naturally performs best (e.g., story_transformation works best at TTT-03/04, myth_indignation at TTT-07/08). But the coach's authenticated emotional state OVERRIDES the affinity range. A coach at TTT-08 doing story_transformation produces unconventional but potentially powerful content. Gating would prevent this. |
| **No TTT in ANY of the 3 SPR layers** | The Three-Layer SPR Loading Protocol (Layer 0: Negative Space, Layer 1: Positive Space, Layer 2: Emotional DNA) does not include TTT in any layer. TTT is orthogonal to the voice identity layers — it is the emotional state AT THE MOMENT OF PRODUCTION, not a persistent identity trait. |
| **Scanning all Block B fields, not just known field names** | A naive scanner checking for fields named "TTT" or "temperature" would miss aliased fields ("emotional_register", "heat_level", "voice_intensity") that serve the same function. The scanner must detect any field that constrains emotional register to a specific static value. |

---

## Implementation Plan

### Layer 1: Authoring Enforcement (Prevention)

**What:** Template authors are prohibited from including any TTT value or TTT-equivalent field in Block A or Block B.

**Mandate M-02 (Script Generation Skill Type Guide v1.0):**

> *"TTT Is Never Pre-Specified. Temperature, Texture, and Tone are not compilation variables. No Block A or Block B field may contain a hardcoded TTT value. TTT is resolved at runtime by DEP-ENG-005 Authentication Certificate only."*

**Variants-vs-Invariants Test (the authoritative classification):**

| Example | Classification | Block |
|---|---|---|
| "Stakes precede Result" | Invariant (true for all compilations) | Block A |
| "Hook leads with loss framing" | Variable (true only for prevention regulatory frame) | Block B / psych-routing-adapter |
| "Temperature is TTT-04" | **UNDEFINED** — runtime value, rejected by Block C C-08 | **NOT in any block** |
| "Use tribal vocabulary from DEP-ENG-007" | Invariant (directive); specific vocabulary = variable | Block A (directive); Block B field_3 (specific values) |

**Permitted TTT references in templates:**

| Context | Permitted? | Example |
|---|---|---|
| Block A Field 4 (Trigger) — TTT natural affinity range as advisory | ✅ Yes | "Natural affinity range: TTT-03 to TTT-05. Human review flag: TTT ≥ TTT-08 for this archetype." |
| Block C C-08 — TTT Enforcement check reference | ✅ Yes | "C-08: TTT Enforcement — No hardcoded TTT value in any Block B field" |
| Block A structural law — specifying a TTT value | ❌ No | "This phase should be written at TTT-07 for maximum impact" |
| Block B field_3 — TTT as a compilation variable | ❌ No | "ttt_temperature: TTT-06" |
| Block B field_9 — TTT as a voice constraint | ❌ No | "Voice register: maintain TTT-04 throughout" |

**Authoring quality gate (pre-Architecture Review):**

Mandate Compliance Checklist item M-02:
> "No TTT value appears in any Block A or Block B field."

Template authors must confirm this before submission. Violation caught at Architecture Review = template returned to author with M-02 citation.

---

### Layer 2: Compilation Enforcement (Detection) — Block C C-08

**What:** The JIT Skill Assembler v2.0 Tier 0 pre-flight mechanically detects hardcoded TTT values before any assembly begins.

**Check definition:**

| Check | Name | Pass Condition | Failure Behaviour |
|---|---|---|---|
| C-08 | TTT Enforcement | No hardcoded TTT value in any Block B field | REJECT — TTT is never a compilation variable |

**Detection Algorithm:**

```
FUNCTION c08_ttt_enforcement(compiled_brief):
  
  # Phase 1: Explicit TTT field detection
  # Scan all Block B fields for fields named with TTT-related identifiers
  TTT_FIELD_PATTERNS = [
    "ttt", "temperature", "texture", "tone",
    "emotional_register", "emotional_temperature",
    "voice_temperature", "heat_level", "voice_intensity",
    "ttt_value", "ttt_setting", "ttt_target"
  ]
  
  FOR EACH field IN compiled_brief.block_b:
    IF field.name MATCHES ANY TTT_FIELD_PATTERNS (case-insensitive):
      IF field.value IS a static value (not a DEP-ENG-005 reference):
        RETURN REJECT {
          check: "C-08",
          violation: "TTT_HARDCODED_IN_BLOCK_B",
          field: field.name,
          value: field.value,
          message: "TTT is never a compilation variable. Remove {field.name} 
                    from Block B. TTT is resolved at runtime via DEP-ENG-005.",
          mandate: "M-02"
        }
  
  # Phase 2: Implicit TTT value detection
  # Scan all Block B field VALUES for TTT scale references
  TTT_VALUE_PATTERNS = [
    r"TTT-\d{1,2}",           # "TTT-04", "TTT-07"
    r"temperature\s*[:=]\s*\d", # "temperature: 7", "temperature = 4"
    r"tone\s*[:=]",            # "tone: confrontational"
    r"register\s*[:=]",       # "register: warm"
    r"write at TTT",          # "write at TTT-07"
    r"maintain.*TTT",         # "maintain TTT-04 throughout"
  ]
  
  FOR EACH field IN compiled_brief.block_b:
    FOR EACH value_string IN field.all_string_values():
      IF value_string MATCHES ANY TTT_VALUE_PATTERNS:
        RETURN REJECT {
          check: "C-08",
          violation: "TTT_VALUE_EMBEDDED_IN_BLOCK_B",
          field: field.name,
          matched_pattern: matched_pattern,
          message: "TTT value detected in Block B field '{field.name}'. 
                    TTT is resolved at runtime via DEP-ENG-005 only.",
          mandate: "M-02"
        }
  
  # Phase 3: Block A structural law scan (secondary check)
  # Block A should contain TTT affinity range as ADVISORY only
  FOR EACH law IN compiled_brief.block_a.structural_laws:
    IF law.text CONTAINS TTT_VALUE_PATTERNS:
      IF NOT law.context == "natural_affinity_range_advisory":
        RETURN REJECT {
          check: "C-08",
          violation: "TTT_DIRECTIVE_IN_BLOCK_A",
          law: law.id,
          message: "TTT value found in Block A structural law. 
                    Only TTT natural affinity range (advisory) is permitted in Block A.",
          mandate: "M-02"
        }
  
  RETURN PASS { check: "C-08", status: "TTT_ENFORCEMENT_CLEAN" }
```

**Tier 0 integration:**

```
TIER 0 — PRE-FLIGHT (zero generation, zero tokens)
═══════════════════════════════════════════════════
  Run C-01: DEP Resolution
  Run C-02: Psychological Routing Brief Present
  Run C-03: L3 Layer Threshold
  Run C-05: Authentication Certificate Valid
  Run C-06: Semantic Affinity Pre-Check
  Run C-07: TMT/Cohort Alignment
  Run C-08: TTT Enforcement         ← THIS CHECK
  Run C-09: CRAL Coverage Check
  Run C-10: CRAL Moment Object Completeness
  
  FAIL any check → REJECTED status
  Return diagnostic JSON
  DO NOT PROCEED to Tier 1
```

**Diagnostic output on C-08 failure (written to `assembly_report.json`):**

```json
{
  "compilation_id": "comp_2026-W12_story_transformation_001",
  "deployment_status": "REJECTED",
  "tier_0_pre_flight": {
    "c08_ttt_enforcement": {
      "status": "FAIL",
      "violation_type": "TTT_HARDCODED_IN_BLOCK_B",
      "violating_field": "field_3.emotional_register",
      "violating_value": "TTT-06",
      "mandate_violated": "M-02",
      "recovery_instruction": "Remove 'emotional_register: TTT-06' from Block B field_3. TTT is resolved at production time via DEP-ENG-005 Authentication Certificate. The template author must correct this field and resubmit.",
      "pipeline_impact": "Full compilation halted. Zero tokens consumed. No assembly began."
    }
  }
}
```

---

### Layer 3: Runtime Resolution — DEP-ENG-005 Authentication Certificate

**What:** TTT is resolved dynamically at production time using the coach's authenticated emotional state from their session voice note.

**Resolution flow:**

```
┌─────────────────────────────────────────────────────────┐
│  PRODUCTION SESSION START                                │
│                                                          │
│  1. Scheduled Monitor Agent delivers observation         │
│  2. Coach responds with voice note (Telegram)            │
│  3. Voice note → FR2 LIWC-22 authenticity gate           │
│     IF score < 7/10 → OARS re-elicitation question       │
│     IF score ≥ 7/10 → AUTHENTICATED                      │
│  4. Authenticated voice note → TTT extraction:           │
│     ┌──────────────────────────────────────────────┐     │
│     │  TEMPERATURE: Emotional intensity measured    │     │
│     │    from vocal markers (speed, pitch variance, │     │
│     │    volume dynamics, pause patterns)            │     │
│     │  TEXTURE: Stylistic surface quality from      │     │
│     │    linguistic analysis (sentence complexity,   │     │
│     │    metaphor density, register formality)       │     │
│     │  TONE: Vocal register classification from     │     │
│     │    semantic analysis (confrontational,         │     │
│     │    reflective, nurturing, instructional)       │     │
│     └──────────────────────────────────────────────┘     │
│  5. TTT value → DEP-ENG-005 Authentication Certificate   │
│  6. DEP-ENG-005 → JIT Skill Assembler (at Tier 1)       │
│  7. Assembler injects TTT contextually into compiled     │
│     SKILL.md — NOT as a hardcoded value, but as a        │
│     runtime emotional context injected by the            │
│     authentication adapter                               │
│                                                          │
│  RESULT: Generated content carries the coach's TRUE      │
│  emotional temperature for THIS specific session         │
└─────────────────────────────────────────────────────────┘
```

**TTT natural affinity range (advisory system):**

Each archetype has a temperature range where its structural function is most naturally expressed:

| Archetype Family | Natural Affinity Range | Why |
|---|---|---|
| Story (Transformation, Recognition) | TTT-02 to TTT-05 | Narrative access requires reflective depth — high temperature burns through nuance |
| Myth (Indignation, Empowering) | TTT-06 to TTT-09 | Conviction-based content requires high emotional intensity — low temperature reads as ambivalent |
| Listicle (Helpful, Shocking) | TTT-03 to TTT-06 | Informational + emotional blend — pure heat overwhelms structure |
| Reaction (Surprising, Funny) | TTT-04 to TTT-07 | Requires enough emotional energy for genuine reaction — too low reads as disinterested |
| Comparison (Profound, Shocking) | TTT-05 to TTT-08 | Comparative judgments require conviction — soft comparisons create no delta |
| Tweet (Warning, Recognition, Wisdom) | TTT-03 to TTT-08 | Maximum range — short-form works across temperatures |
| Tier List (Controversial) | TTT-07 to TTT-09 | Position-staking requires fire — low-temperature tier lists read as indecisive |

**Advisory, not gate:** If the coach's authenticated TTT falls outside the archetype's natural affinity range:
- The Orchestrator logs `ttt_outside_affinity_range: true`
- The Orchestrator flags the compilation for human review
- The compilation PROCEEDS — the coach's authentic emotional state overrides the advisory
- Content may be unconventional but potentially more powerful than affinity-standard content

---

### Layer 4: Post-Generation Verification — Sophia (Minister of Identity)

After content is generated, Sophia validates that the produced content's emotional register is consistent with the DEP-ENG-005 authentication:

| Check | Target | Method | Threshold |
|---|---|---|---|
| TTT Drift | Generated content vs. DEP-ENG-005 authenticated temperature | LIWC-22 emotional markers comparison | Drift < 15% from authenticated baseline |
| Emotional Peak Detection | Generated content emotional peaks | iRAV-inspired peak analysis | ≥1 emotional peak exceeding the average by ≥20% in each script |
| Register Consistency | Generated content vocal register vs. Voice DNA baseline | TTT cosine similarity against `ttt_baseline.json` | Similarity ≥ 0.85 |

---

## TTT Contamination Vectors — What C-08 Must Catch

| Vector | Where It Hides | Example | Detection Method |
|---|---|---|---|
| **Explicit field assignment** | Block B field_3 | `"ttt_temperature": "TTT-06"` | Phase 1: field name pattern match |
| **Embedded in voice constraints** | Block B field_9 | `"Voice register: maintain warm, nurturing TTT-04"` | Phase 2: value string pattern match |
| **Aliased field name** | Block B field_3 | `"emotional_heat": 7` | Phase 1: expanded TTT_FIELD_PATTERNS list |
| **Structural law directive** | Block A Field 7 | `"The Turn phase must hit TTT-07 for maximum cognitive revision"` | Phase 3: Block A structural law scan |
| **Adapter inline override** | Block B field_8 | `"psych-routing-adapter: { override_ttt: TTT-05 }"` | Phase 2: value string pattern match within adapter specs |
| **Natural language instruction** | Block A Field 6 Action | `"Write in a calm, reflective register (TTT-03)"` | Phase 2: regex pattern for TTT-NN within natural language |
| **Implicit temperature specification** | Block B field_9 | `"All content should be calm and measured"` — effectively hardcoding low temperature | PARTIAL DETECTION — Phase 2 catches explicit TTT references. Implicit register instructions without TTT labels require Sophia post-generation validation |

> **Note:** Implicit register instructions ("write calmly", "be confrontational") without explicit TTT labels are NOT caught by C-08. This is by design — Block A Field 4 (Trigger) must be permitted to describe the archetype's natural emotional territory. The enforcement boundary is: NO SPECIFIC TTT VALUE OR SCALE REFERENCE in compilation fields. General emotional descriptors in structural context are permitted.

---

## Tasks

- [ ] **Task 1:** Implement C-08 Phase 1 — Explicit TTT field detection (field name pattern matching against TTT_FIELD_PATTERNS)
- [ ] **Task 2:** Implement C-08 Phase 2 — Implicit TTT value detection (value string regex scanning for TTT-NN patterns, temperature/tone/register assignments)
- [ ] **Task 3:** Implement C-08 Phase 3 — Block A structural law secondary scan (detect TTT directives in structural laws, permit natural affinity range advisories)
- [ ] **Task 4:** Implement C-08 diagnostic output — structured rejection JSON to `assembly_report.json` with violation_type, violating_field, violating_value, mandate_violated, recovery_instruction
- [ ] **Task 5:** Integrate C-08 into JIT Skill Assembler v2.0 Tier 0 pre-flight sequence (after C-07, before C-09)
- [ ] **Task 6:** Implement TTT natural affinity range advisory system — archetype-to-range mapping, outside-range flagging for human review, no blocking
- [ ] **Task 7:** Implement DEP-ENG-005 runtime TTT resolution — Authentication Certificate extraction from session voice note → TTT components (Temperature, Texture, Tone)
- [ ] **Task 8:** Implement TTT injection at Tier 1 — authentication adapter loads DEP-ENG-005 TTT as runtime emotional context into compiled SKILL.md
- [ ] **Task 9:** Implement Sophia post-generation TTT drift validation — LIWC-22 emotional markers comparison, drift threshold < 15%
- [ ] **Task 10:** Implement iRAV-inspired emotional peak detection — verify ≥1 emotional peak per script exceeding average by ≥20%
- [ ] **Task 11:** Create Template Authoring Compliance Checker — pre-Architecture Review tool that scans all template fields for M-02 violations before human review

---

## Acceptance Criteria

- [ ] **AC1 (C-08 Explicit Detection):** A Design Brief with Block B field `ttt_temperature: "TTT-06"` → C-08 returns REJECT with `TTT_HARDCODED_IN_BLOCK_B` diagnostic. Zero tokens consumed. No assembly begins.
- [ ] **AC2 (C-08 Inline Detection):** A Design Brief with Block B field_9 containing `"maintain warm register at TTT-04 throughout"` → C-08 returns REJECT with `TTT_VALUE_EMBEDDED_IN_BLOCK_B`.
- [ ] **AC3 (C-08 Block A Detection):** A Design Brief with Block A structural law containing `"The Hook must hit TTT-08 for maximum impact"` → C-08 returns REJECT with `TTT_DIRECTIVE_IN_BLOCK_A`.
- [ ] **AC4 (C-08 Advisory Permit):** A Design Brief with Block A Field 4 containing `"Natural affinity range: TTT-03 to TTT-05. Human review flag: TTT ≥ TTT-08."` → C-08 returns PASS. Advisory references are permitted.
- [ ] **AC5 (C-08 Aliased Field Detection):** A Design Brief with Block B field `emotional_heat: 7` → C-08 returns REJECT. Field name pattern matching catches aliases.
- [ ] **AC6 (Zero-Token Guarantee):** When C-08 rejects, `assembly_report.json` confirms: zero tokens consumed, zero adapter invocations, zero section assemblies. The rejection is a pure logical check with no computational cost.
- [ ] **AC7 (Runtime Resolution):** A production session with a coach voice note scoring LIWC-22 ≥ 7/10 → DEP-ENG-005 populated with session-specific TTT values. The compiled SKILL.md contains no hardcoded TTT — the TTT is injected via the authentication adapter at Tier 1.
- [ ] **AC8 (Affinity Range Advisory):** A coach authenticated at TTT-08 assigned to `story_transformation` (affinity range TTT-02 to TTT-05) → Orchestrator logs `ttt_outside_affinity_range: true` and flags for human review. Compilation PROCEEDS — does not block.
- [ ] **AC9 (Post-Generation Drift):** Generated content with TTT drift > 15% from DEP-ENG-005 baseline → Sophia validation fails. Content rejected for revision. Drift ≤ 15% → passes.
- [ ] **AC10 (Emotional Peak):** Generated content with zero emotional peaks exceeding the average by ≥20% → fails iRAV-inspired peak check. Content flagged as emotionally flat. ≥1 peak above threshold → passes.
- [ ] **AC11 (Pipeline Interruption Logging):** When C-08 rejects a compilation, the pipeline interruption is logged with: template_id, violated_field, recovery_instruction. The authoring error is traceable to the specific template for correction.
- [ ] **AC12 (Compliant Template Pass):** A well-formed Design Brief with NO TTT values in Block A structural laws or Block B fields, with a valid DEP-ENG-005 reference in Field 4, and with C-08 referenced in Block C → all pre-flight checks pass. Assembly proceeds to Tier 1.

---

## Dependencies

| Dependency | Type | Notes |
|---|---|---|
| JIT Skill Assembler v2.0 Tier 0 | Infrastructure | C-08 runs within the existing pre-flight gate alongside C-01 through C-10 |
| DEP-ENG-005 Authentication Certificate | Runtime data | Produced by the coach's session voice note → LIWC-22 → TTT extraction |
| FR2 Sacred Audio Ingestion | Internal prerequisite | LIWC-22 authenticity gate produces the authentication score |
| FR3 Voice DNA Extraction | Internal prerequisite | `ttt_baseline.json` provides the persistent TTT reference for drift checks |
| Sophia (Soul Validator) | Downstream consumer | Post-generation TTT drift validation |
| Script_Generation_Skill_Type_Guide_v1.0 | Authoring doctrine | M-02 mandate definition — governs all template authors |
| Design Brief Template Library v1.2 | Templates | All templates must comply with M-02 — no TTT in Block A/B fields |

---

## Testing Strategy

### Unit Tests
- **Explicit field detection:** 5 synthetic templates with TTT field names (`ttt`, `temperature`, `tone`, `emotional_register`, `voice_intensity`) → all 5 return REJECT from C-08
- **Value pattern detection:** 5 synthetic templates with TTT values embedded in string fields (`"write at TTT-07"`, `"maintain TTT-04"`, `"temperature: 8"`, `"register = warm"`, `"TTT-06 throughout"`) → all 5 return REJECT
- **Advisory permit:** 3 synthetic templates with TTT natural affinity range in Block A Field 4 → all 3 return PASS from C-08
- **Clean template pass:** 5 synthetic templates with zero TTT contamination → all 5 return PASS
- **Aliased detection:** Synthetic template with field named `heat_setting: 6` → returns REJECT

### Integration Tests
- **Full Tier 0 sequence:** Run complete pre-flight (C-01 through C-10) on a compliant template with valid DEP-ENG-005 → all checks pass. Run same template with hardcoded TTT in field_3 → C-08 REJECTS, rest of Tier 0 does not execute.
- **Runtime resolution end-to-end:** Coach records voice note → LIWC-22 ≥ 7/10 → TTT extracted → DEP-ENG-005 populated → compilation runs → Sophia validates TTT drift < 15% against baseline
- **Affinity range advisory:** Compile `myth_indignation` for a coach authenticated at TTT-02 (outside affinity range TTT-06 to TTT-09) → compilation proceeds with human review flag

### Safety Tests
- **Token consumption on rejection:** C-08 REJECT → verify zero API calls, zero tokens consumed, zero adapter invocations. The rejection is computationally free.
- **Cascade prevention:** C-08 REJECT does not trigger downstream error handlers — it returns a clean diagnostic JSON that the Builder Engine interprets without error propagation.
- **Template correction loop:** After C-08 REJECT, template author corrects the violating field and resubmits → C-08 returns PASS on the corrected template.
