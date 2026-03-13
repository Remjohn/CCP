# Tech-Spec: FR23 — Skill Fingerprint ID & Archive Engine (DEP-ENG-020)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v4.0 / JIT Compiler Architecture v1.0)
**Architecture Reference:** JIT_Skill_Compiler_Architecture §Section 7, CCP_Evolution_Architecture_Report_V3
**Skill Implementation:** `infrastructure/ccp/memory/fingerprint-archive-engine/`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\JIT_Skill_Compiler_Architecture.docx.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CCP_Evolution_Architecture_Report_V3.docx.md`

---

## 2. Overview

### Problem Statement
When a viral piece of content is produced, or conversely, when a generated piece spectacularly fails the audience resonance test, the system historically had no deterministic way to backtrack *why*. It could not point to the exact CRAL finding, the active emotional DNA hash, or the psychological routing variable that caused the success or failure. Without unique, trackable linkages between the compiled constraint set (the SKILL) and the downstream outcomes (the content performance), the AI system acts as a static script generator rather than a self-evolving intelligence loop.

### Solution
FR23 implements the **Skill Fingerprint ID Schema** and the **Fingerprint Archive Engine (DEP-ENG-020)**. Every time the JIT Assembler successfully compiles a `SKILL.md`, it assigns a cryptographically unique Fingerprint ID. This ID records a snapshot of the exact dependency SHAs used (Voice DNA, CRAL bindings, Psych Routing variables). Downstream, when content generates engagement signals, those metrics are securely written back to the Fingerprint ID inside the Archive. High-performing skills automatically graduate through Promotion Tiers (Draft → Tested → Stable → Reference).

### Scope
**In scope:**
- Stage 1: ID string synthesis based on compilation inputs.
- Stage 2: Registration of the `skill_id` alongside dependency hashes into `DEP-ENG-020`.
- Stage 3: The Output Linkage API that maps downstream metrics (`saves`, `viral_quartet_score`) back to the parent skill.
- Stage 4: Promotion Tier graduation logic.
- Receipt Chain Guard integration.

**Out of scope:**
- The extraction APIs for Instagram/TikTok. The Archive expects clean JSON metric payloads fed into Stage 3.

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-020` | Fingerprint Archive Index | OUTPUT — The primary JSON ledger tracking all compilations and their lifetimes. |
| `DEP-PROTO-012` | Fingerprint Scoring Protocol | LOGIC — Governs how the raw metrics advance a skill through the Promotion Tiers. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **SkillNet** | Liang et al. | 2026 | Formalizing skills as composable assets with tracked performance improves agent outputs by 40%. It establishes the feedback loop — skills that *worked* inform the next generation of skills. |
| **Agent Skills Benchmark** | Li et al. | 2025 | Curated agent skills boost LLM performance (+16.2%), whereas self-generated skills without curation offer zero gain. This FR acts as the curation mechanism. |

### Technical Decisions
1. **Human-Readable Schema:** The `skill_id` is consciously NOT a random UUID. It is a concatenated string of the critical routing decisions (Archetype, Coach, Mood, Frame, Cohort, Date) for immediate operator diagnosis.
2. **Hash-Based Snapshotting:** The exact data state of the dependencies (like the specific negative space loaded) is stored via SHA-256 hash. This guarantees the archive can detect if an upstream voice profile was modified after compilation.

---

## 4. Implementation Plan

### Stage 1: Fingerprint String Synthesis
*Agent Name:* JIT Skill Assembler v2.0 (Post-Assembly module)
*Inputs:* Validated Design Brief inputs.
*Outputs:* `skill_id` string.
*Failure Condition:* Missing variables inside the Design Brief block out string compilation.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Extract routing values: `ARCH_ID`, `COACH_ID`, `MOOD` (P, E, D, S), `REG_FRAME` (PRO, PRV), `COHORT` (N, DEV, L).
2. Grab the UTC compilation date: `YYYYMMDD`.
3. Query `DEP-ENG-020` for compilations matching these exact parameters today to assign the sequence number (`SEQ`), starting at `001`.
4. Synthesize: `SKILL-{ARCH_ID}-{COACH_ID}-{MOOD}-{REG_FRAME}-{COHORT}-{YYYYMMDD}-{SEQ}`
*(Example: `SKILL-STORY01-EMI-P-PRV-L-20260315-001`)*

### Stage 2: Archive Engine Registration 
*Agent Name:* Fingerprint Archive Engine
*Inputs:* The `skill_id`, the `assembly_status` (from FR21), the Dependency Stack hashes.
*Outputs:* A new object appended to `DEP-ENG-020`.
*Failure Condition:* Failed to lock the JSON file for writing (system IO collision).
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Generate SHA-256 hashes for the current state of `DEP-ENG-003`, `DEP-ENG-006`, and `DEP-ENG-016` used in this compile.
2. Construct the JSON schema block (defined in Section 5).
3. Append to `fingerprint_archive.json`.
4. Save the actual `SKILL.md` flat file to the local directory utilizing the `skill_id` as the filename identifier.

### Stage 3: Output Linkage API
*Agent Name:* Archive-Telemetry-Listener
*Inputs:* `OUTPUT_PAYLOAD` (Content Title, platform, performance metrics, audience behavioral signals).
*Outputs:* Updated `DEP-ENG-020` schema.
*Failure Condition:* API receives payload with no `skill_id` association.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Listener receives an update ping containing structured post-publishing analytics.
2. Find the target `skill_id` inside `DEP-ENG-020`.
3. Append the payload to the `outputs` array for that parent skill.
4. Trigger Stage 4 check.

### Stage 4: Promotion Tier Protocol (DEP-PROTO-012)
*Agent Name:* Archive-Promotion-Monitor
*Inputs:* Updated `DEP-ENG-020` metrics.
*Outputs:* Mutated `maturity` status in JSON.
*Failure Condition:* Math calculation rules fail due to null payload values.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Decision Logic:**
- **Draft:** Default state upon Stage 2 registration. High plasticity.
- **Tested:** Requires `outputs.length >= 3` where `assembly_failure == false`. Medium plasticity.
- **Stable:** Requires `outputs.length >= 10` across diverse inputs AND `performance.saves > (2x category average)`. Low plasticity, locked structure.
- **Reference:** Requires `<Stable>` AND manual Architecture Review approval. Contributes complete Block A + B back to the Archetype Template as a canonical working example.

---

## 5. Primary Output Schema (DEP-ENG-020)

**Schema Name:** `fingerprint_archive.json`

```json
{
  "skill_id": "SKILL-STORY01-EMI-P-PRV-L-20260315-001",
  "archetype_template_id": "ARCH-STORY-01",
  "archetype_template_version": "1.2",
  "compilation_date": "2026-03-15",
  "maturity": "draft",
  "assembly_status": "COMPLETE",
  "context": {
    "coach_id": "EMI",
    "mood_state": "Processing",
    "regulatory_frame": "prevention",
    "audience_cohort": "loyal",
    "tmt_function": "worldview_construction",
    "sdt_need_primary": "relatedness"
  },
  "dep_snapshot": {
    "DEP-ENG-003": "e3b0c44298...",
    "DEP-ENG-006": "8a9f3b...",
    "DEP-ENG-016": "c4ca423..."
  },
  "outputs": [
    {
      "output_id": "OUT-STORY01-EMI-20260316-001",
      "content_title": "The day I got promoted was the loneliest",
      "platform": "instagram",
      "published_date": "2026-03-16",
      "performance": {
        "saves": 2847,
        "shares": 1203,
        "comments": 892,
        "viral_quartet_score": 4.2
      },
      "audience_signals": {
        "dm_vulnerability_ratio": 0.18,
        "comment_depth_score": 3.4,
        "save_to_share_ratio": 2.37
      }
    }
  ],
  "performance_scores": {},
  "promoted_to_stable": false
}
```

---

## 6. Backward Compatibility Fallback
Because the Fingerprint Archive (`DEP-ENG-020`) essentially functions as the immutable database mapping generations to intelligence, **legacy skills lacking a fingerprint are strictly read-only and cannot be updated with performance telemetry.** If the Listener API (Stage 3) attempts to write metrics for a legacy output that has no corresponding `skill_id` parent, the system safely ignores the write, logging an `<UNLINKED_ORPHAN_OUTPUT>` warning, preserving system stability without destroying the analytics data.

---

## 7. Tasks

- [ ] **Task 1:** Build the `ID-Synthesis-Engine` that reads the 6 variables from the active Brief, accesses the DB to find the sequence count, and prints the human-readable string.
- [ ] **Task 2:** Introduce a Cryptography Helper in the Assembler that reads the active memory states of `DEP-ENG-003/006/016` immediately post-assembly, returning deterministic SHA-256 strings for the `dep_snapshot` map.
- [ ] **Task 3:** Create the `Archive-Telemetry-Listener` endpoint that accepts incoming JSON payloads from the upstream platform scrapers, validates the schema structure, and appends it to the `outputs` array.
- [ ] **Task 4:** Codify the Promotion Engine `DEP-PROTO-012` logic loop. It must run asynchronously against the `fingerprint_archive.json` every time the Telemetry Listener fires, automatically promoting `Draft` to `Tested` if thresholds cross.
- [ ] **Task 5:** Write Receipt Chain verifications across all four stages, including `tenant_id` tags for ADR-01 validation.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Synthesis Validity):** A design brief compiled for Ana, Shocking Listicle, Escape Mode, Promotion Frame, New Cohort on March 15th results perfectly in the generated string `SKILL-LIST02-ANA-E-PRO-N-20260315-001`. *Failure Example:* Extraneous spaces or null pointers break the hyphenated formatting rendering `SKILL-LIST02-ANA-E-PRO-null-...`
- [ ] **AC2 (Hash Integrity):** If a compiled skill's JSON Ledger lists `"DEP-ENG-003": "e3b0xyz..."`, running the same hashing algorithm on the coach's Voice DNA file from that exact timestamp produces the exact same hash. *Failure Example:* The system hashes a blank RAM buffer resulting in empty or random strings, breaking the memory audit capability.
- [ ] **AC3 (Promotion Math):** A `draft` skill receives its 3rd telemetry payload payload reflecting zero assembly errors. The asynchronous monitor immediately changes `"maturity": "Tested"`. *Failure Example:* The threshold algorithm counts an error-flagged assembly, letting a broken skill pass to Tested.
- [ ] **AC4 (ADR-01 Strict Isolation):** When the Telemetry Listener receives an engagement payload for Emilio's output, the JSON write explicitly locks to Emilio's isolated `fingerprint_archive.json` bucket. *Failure Example:* The system writes Emilio's viral metric payload into Maria's skill tracking JSON, corrupting her promotion threshold math.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| JIT Skill Assembler v2.0 | Upstream | Generates the raw data triggering Stage 1. |
| Engagement Intelligence Feed | Upstream | Assumes an external microservice pushes formatted JSON payloads containing saves/shares to the Telemetry Listener. |
| Receipt Chain Guard | Infrastructure | Non-negotiable sequence auditing. |

---

## 10. Testing Strategy

### Unit Tests
- **String Concat Test:** Feed the `ID-Synthesis-Engine` 100 sets of varied, valid routing variables. Assert 100 perfectly matched string schemas. Feed it an invalid mood (e.g., `<Z>`). Assert it throws a validation exception.
- **Rules Engine Promotion:** Submit a mock JSON blob representing a skill with 11 successful outputs and 3x average saves. Assert the Rules Engine instantly processes it and mutates the status to `<Stable>`.

### Integration Tests
- **The Orchestration Chain:** Run the pipeline end to end. Upon successful assembly to `COMPLETE`, retrieve the JSON object inside the `DEP-ENG-020` ledger. Assert the `dep_snapshot` is populated, the `outputs` array is `[]` (empty), and `maturity` is `<draft>`.
- **Telem Queue Processing:** Fire 5 fast sequential payloads to the Telemetry Listener API containing identical `skill_id`s. Assert the system successfully appends all 5 objects to the target `outputs` array without IO locks breaking the file map.

### Safety Tests (ADR-01 Quarantine Security)
- **Tenant Context Bleed Check:** Initiate simultaneous database writes to the Listener Queue for Coach A and Coach B. Verify that Coach A's metrics are written ONLY to the partition belonging to Coach A. Retrieve both files and assert zero cross-contamination.
