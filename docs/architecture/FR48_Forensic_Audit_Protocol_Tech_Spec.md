# Tech-Spec: FR48 — Forensic Audit Protocol (DEP-ENG-042)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §Receipt Chain Guard, JIT_Skill_Compiler_Architecture §07
**Skill Implementation:** `skills/governance/forensic_auditor/`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\prd TO UPDATE.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\JIT_Skill_Compiler_Architecture.docx.md`

---

## 2. Overview

### Problem Statement
When a coach complains, "Why did the system write this post using such an aggressive tone?" an operator cannot answer that question by merely looking at the final text. In an architecture with 65 agents, dynamic mood routing, and contextual memory overrides, the final output is the result of dozens of micro-decisions. Without a protocol to reconstruct *why* those decisions were made, the CCP operates as a black-box. Black-box operations in a high-ticket coaching environment equal catastrophic brand risk.

### Solution
FR48 establishes the **Forensic Audit Protocol (DEP-ENG-042)**. It provides the System Operator with the programmatic capability to query an `Asset_ID` and instantaneously reconstruct the complete semantic lineage of the content. By traversing the `Receipt Chain Guard` (FR47) backward, and cross-referencing the `Skill Fingerprint ID` (which locked in the psychological parameters at compile time), the operator can explicitly trace the logic: *Agent X chose Tone Y because Memory Z was active during the M1 phase.*

### Scope
**In scope:**
- The Generation and Structure of the `Skill Fingerprint ID`.
- The Supabase `fingerprint_archive` repository (`DEP-ENG-020`).
- The Python utility `trace_lineage.py` that reconstructs the session logic.

**Out of scope:**
- The actual writing of the cryptographic hashes (handled by FR47).
- The weekly performance evaluations (handled by FR43).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-042` | Forensic Audit Protocol | TOOL — The operator-facing utility that decodes the black box. |
| `DEP-ENG-020` | Fingerprint Archive | STORAGE — The JSON blob mapping the compilation parameters to the `Skill_ID`. |
| `DEP-ENG-041` | Receipt Chain Guard | DEPENDENCY — The cryptographic timeline traversed during the audit. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **SkillNet (Evolving Composable Agents)** | Liang et al. | 2026 | Formalizes that establishing trackable, evolving "skill passports" (Fingerprints) allows a 40% performance gain over raw self-prompting. By tracking the exact parameters used during compilation, we can trace failures back to the specific logic branch, closing the RLHF loop. |

### Technical Decisions
1. **Fingerprint ID distinct from Asset ID:** The `Asset_ID` (FR46) tracks the *content* (e.g., `JP-CCF-20260312-001-CAROUSEL`). The `Skill Fingerprint ID` tracks the *logic* (e.g., `SKILL-STORY01-JP-P-PRV-L-20260312-001`). One single compiled skill might generate 5 different assets. Separating them allows the system to grade the *skill's* maturity independent of a single asset's virality.
2. **Snapshot Hashing:** The `fingerprint_archive` does not copy the massive `coach_soul.json` into its rows. It saves the `hash` of the dependency used at the exact moment of compilation. This prevents database bloat while mathematically proving what context was available to the agent.

---

## 4. Implementation Plan

### Stage 1: Skill Compilation & Fingerprinting
*Agent:* JIT Compiler (Research Planner)
*Inputs:* `Archetype_ID`, `Coach_ID`, `Mood_State`, `Regulatory_Frame`, `Cohort`.
*Outputs:* `Skill_Fingerprint_ID`.
*Failure Condition:* Compiler fails to register the fingerprint, creating a ghost-skill that cannot be audited downstream.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Before generating the content, the JIT Compiler resolves its target parameters.
2. **Resolution Rules for the ID String:**
   - `{ARCH_ID}`: The template identifier (e.g., `STORY01`, `LIST02`).
   - `{COACH_ID}`: 3-4 Char abbreviation (e.g., `JP`).
   - `{MOOD}`: Enum `[P, E, D, S]` (Processing, Escape, Discovery, Status).
   - `{REG_FRAME}`: Enum `[PRO, PRV]` (Promotion, Prevention).
   - `{COHORT}`: Enum `[N, DEV, L]` (New, Developing, Loyal).
   - `{DATE}-{SEQ}`: Derived from Supabase atomic counter.
3. String format: `SKILL-{ARCH_ID}-{COACH_ID}-{MOOD}-{REG_FRAME}-{COHORT}-{DATE}-{SEQ}`.
4. Generates the `dep_snapshot` hashes (hashes of the current state of `Emotional DNA`, `Context Premise`, etc.).
5. POSTs the schema to the Supabase `fingerprint_archive` (`DEP-ENG-020`).

### Stage 2: Binding Asset to Skill
*Agent:* Content Orchestrator (Alex)
*Inputs:* `Skill_Fingerprint_ID`, `Universal_Asset_ID`.
*Outputs:* Updated `fingerprint_archive`.
*Failure Condition:* Orchestrator writes the file but fails to bind ID, breaking the RLHF feedback loop.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. The Orchestrator manages the actual content generation using the Compiled Skill.
2. Upon successful generation (and ID assignment via FR46), it executes an `UPDATE` to the `fingerprint_archive` table.
3. It appends the newly created `Universal_Asset_ID` to the `outputs: []` array inside the Fingerprint JSON.

### Stage 3: The Forensic Query (Operator Trace)
*Agent:* System Operator (Via CLI Tool `trace_lineage.py`)
*Inputs:* `Universal_Asset_ID`.
*Outputs:* Formatted Terminal Lineage Tree.
*Failure Condition:* `Asset_ID` not found or Receipt Chain broken, returning a 404 tree.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Operator inputs: `python trace_lineage.py JP-CCF-20260312-001-CAROUSEL`.
2. Script queries Supabase `fingerprint_archive` where `outputs` contains the `Asset_ID`. Returns the `Skill_Fingerprint_ID` and the `context` parameters (Mood, Frame, etc).
3. Script queries Supabase `receipt_chain` using the `Asset_ID`. Retrieves all receipts.
4. Script sorts receipts by chronological hash linkage (`previous_receipt_hash`).
5. **Output Delivery:** Prints the reconstruction:
   * "Asset X generated on [Date]."
   * "Driven by Skill Baseline: [Archetype] under [Mood] and [Frame]."
   * "Agent sequence: [Aria -> Planner -> Artisan -> Validator]."
   * "CRAL Override: True (Reasoning: <extract rationale from planner receipt>)."

---

## 5. Primary Output Schema (DEP-ENG-042 & DEP-ENG-020)

**Schema Name:** `fingerprint_archive_registration.json`

```json
{
  "skill_id": "SKILL-STORY01-JP-P-PRV-L-20260312-001",
  "archetype_template_id": "ARCH-STORY-01",
  "archetype_template_version": "1.1",
  "compilation_date": "2026-03-12T10:00:00Z",
  "maturity": "draft",
  "assembly_status": "COMPLETE",
  "context": {
    "coach_id": "JP",
    "mood_state": "Processing",
    "regulatory_frame": "prevention",
    "audience_cohort": "loyal",
    "tmt_function": "worldview_construction",
    "sdt_need_primary": "relatedness"
  },
  "dep_snapshot": {
    "DEP-ENG-003_emotional_dna": "a1b2c3d4e5...",
    "DEP-ENG-006_context_premise": "f6g7h8i9j0...",
    "DEP-ENG-016_routing_brief": "k1l2m3n4o5..."
  },
  "outputs": ["JP-CCF-20260312-001-CAROUSEL", "JP-CCF-20260312-002-REEL"],
  "promoted_to_stable": false
}
```

---

## 6. Backward Compatibility Fallback
If the `fingerprint_archive` table is inaccessible during Stage 1 compilation, the orchestrator logs a `WARN_FINGERPRINT_FAILED` to the active Receipt Chain and drops the physical `.json` dump into the S3 local `/tmp/` staging bucket alongside the `Asset_ID`. The generation proceeds, avoiding system halt. A CRON janitor script sweeps `/tmp/` hourly, performing back-insertions to Supabase to reconstruct the audit linkage once DB parity returns.

---

## 7. Tasks

- [ ] **Task 1:** Execute Supabase migration to build `fingerprint_archive` matching the Stage 5 JSON schema.
- [ ] **Task 2:** Refactor the JIT Compiler block to execute the Stage 1 fingerprint string formulation before handing off to the Content Orchestrator.
- [ ] **Task 3:** Implement the cryptographic hashing utility within the JIT Compiler that dynamically hashes `DEP-ENG-003`, `006`, and `016` to populate the `dep_snapshot` object.
- [ ] **Task 4:** Build the `trace_lineage.py` CLI utility.
- [ ] **Task 5:** Write the visual parsing logic for the CLI that traverses the `Receipt Chain` linked list and prints it as a readable text-based tree in the terminal.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Syntax Construction):** Pass mock parameters (Listicle 02, Coach Ana, Escape, Promotion, New). Assert the Orchestrator outputs the exact string `SKILL-LIST02-ANA-E-PRO-N-[DATE]-[SEQ]`. *Failure Example:* The system outputs `SKILL-uuid-v4-string`, destroying the human-readable parameter tracking.
- [ ] **AC2 (Asset Binding):** Mock the generation of 3 subsequent posts using a single pre-compiled Reference Skill. Assert that the `outputs: []` array in the `fingerprint_archive` correctly holds exactly 3 `Universal_Asset_IDs`. *Failure Example:* The array overwrites itself, linking only the most recent asset to the skill.
- [ ] **AC3 (Dependency Hashing Validation):** Trigger compilation. Manually alter 1 character in the Coach's Core Protocol (`DEP-ENG-003`). Trigger compilation again. Assert the `dep_snapshot` hashes are mathematically distinct. *Failure Example:* The system hardcodes a static string, making it impossible to audit if the prompt changed between day 1 and day 40.
- [ ] **AC4 (Forensic Reconstruction):** Execute `python trace_lineage.py {VALID_ASSET_ID}`. Assert the terminal outputs the `Skill_ID`, the exact Context parameters used (e.g., "Mood: Escape"), and the full linked list of acting agents. *Failure Example:* The script throws a `KeyError` because it cannot JOIN the Asset ID back to the `fingerprint_archive`.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| `receipt_chain_guard` | Internal | The cryptographic logs traversed by the forensic script. |
| `id_generator.py` | Internal | The Universal Asset ID acts as the search index for this entire operation. |

---

## 10. Testing Strategy

### Unit Tests
- **String Formatting Guard:** Pass invalid inputs `('INVALID_ARCH', 'COACH', 'SAD', 'PRO')` to the Fingerprint string compiler. Assert it throws a strict `Pydantic ValidationError` demanding the `[P,E,D,S]` enums.

### Integration Tests
- **The Audit Walkthrough:**
  1. Mint a complete artifact from scratch via the CCF pipeline.
  2. Take the resulting Notion page `Asset_ID`.
  3. Query `fingerprint_archive` for that ID.
  4. Assert the returned JSON perfectly matches the active session state parameters (e.g., you asked for a "Status" post, the Fingerprint recorded a "Status" post).

### Safety Tests (ADR-01 Quarantine Security)
- **Lineage Spoofing Rejection:** Manually insert an `Asset_ID` from Coach A into the `outputs` array of Coach B's `Skill_Fingerprint`. Assert that when the System Operator runs `trace_lineage.py`, the script identifies the Tenant ID mismatch between the Asset string prefix and the Skill string prefix, throwing a critical Security Alert rather than completing the audit.
