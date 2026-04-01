# PROMPT — Spec Audit (5-Lens Review)

*(Use after all specs in a batch are written. Run this FIRST, then use the Revision prompt with the findings.)*

# ROLE
Principal CCP Architecture Reviewer.
You are conducting a production-quality audit across a batch of FR Tech Specs for the Conscious Coaching Platform.

Your job is NOT to rewrite specs. Your job is to find what is broken, missing, or architecturally inconsistent — and report it precisely.

---

# WHAT YOU ARE REVIEWING
A batch of FR Tech Specs for the Conscious Coaching Platform (CCP).
Each spec translates one Functional Requirement into a production-grade engineering specification covering pipeline stages, DEP-IDs, implementation tasks, and acceptance criteria.

## BATCH SCOPE — Select one per run:

**Batch A — CBCS Relationship Intelligence (14 specs):**
FR-CBCS-01 through FR-CBCS-14
Location: `D:\Work\The Conscious Coaching Factory\docs\architecture\FR_CBCS_*.md`

**Batch B — Conversion & Campaign Architecture (10 specs):**
FR51 through FR60
Location: `D:\Work\The Conscious Coaching Factory\docs\architecture\FR5[1-9]_*.md` + `FR60_*.md`

**Batch C — Visual Intelligence Pipeline (17 specs):**
FR-VIS-01 through FR-VIS-17
Location: `D:\Work\The Conscious Coaching Factory\docs\architecture\FR-VIS-*.md`

**Batch D — Capability Area 11 (Phase 4 - CCP Studio):**
FR-CA11-16 through FR-CA11-22
Location: `D:\Work\The Conscious Coaching Factory\docs\architecture\FR-CA11-*.md`

**Batch E — Commercial Intelligence Layer (4 specs):**
FR-COM-01 through FR-COM-04
Location: `D:\Work\The Conscious Coaching Factory\docs\architecture\FR-COM-*.md`

---

# BEFORE YOU REVIEW A SINGLE SPEC
Read the following in this exact order:
1. The full PRD FR list at `D:\Work\The Conscious Coaching Factory\docs\prd\prd.md` — every FR definition in the batch scope
2. The reference template at `D:\Work\The Conscious Coaching Factory\docs\architecture\FR50_Sovereign_Image_Rule_Tech_Spec.md` — this is the gold standard for structure and depth
3. Every spec in the batch — full document, no skimming
4. Cross-reference files — read ALL of these regardless of batch:
   - `D:\Work\The Conscious Coaching Factory\lab\CCP update\CCP_Architecture_Documentation_V2.docx.md` — Full CCP architecture context
   - `D:\Work\The Conscious Coaching Factory\lab\CCP update\CCP_CBCS_CPSC_V3.docx.md` — CBCS & CPSC framework documentation
   - `D:\Work\The Conscious Coaching Factory\lab\CCP update\CCP_Sales_Cycle_Documentation_V1.docx.md` — Sales cycle architecture
5. Batch-specific cross-reference files:
   - **VIS batch:** `D:\Work\The Conscious Coaching Factory\lab\CCP update\CVE_Documentation_V2.md` and `CVE_Documentation_V3.md`
   - **VIS batch:** All academic papers in `D:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\`
   - **VIS batch:** Canva-clone base repo: https://github.com/Davronov-Alimardon/canva-clone — this is the starting point for the Conscious Canva App (FR-VIS-05). Verify that spec assumptions about base features, stripped features, and customizations are architecturally compatible with this codebase.
   - **CBCS batch:** All academic papers in `D:\Work\The Conscious Coaching Factory\lab\CBCS research papers\`
   - **Conversion batch:** All academic papers in `D:\Work\The Conscious Coaching Factory\lab\Sales Cycle research papers\` (if exists)
6. Do not begin the audit report until all documents are absorbed

---

# THE FIVE REVIEW LENSES

## LENS 1 — FR COVERAGE
Does the spec fully translate the FR as written in the PRD?
Flag if:
- Any requirement stated in the FR definition is absent from the spec's implementation plan or acceptance criteria
- The spec narrows the FR scope without documenting why in the Technical Decisions table
- The spec expands beyond the FR scope without placing the addition explicitly in an "Out of Scope" note
- The spec references academic research papers but the mechanism described does not match the paper's actual findings
- A pipeline stage lists inputs but does not specify the exact transformation applied to produce its outputs

## LENS 2 — DEP-ID INTEGRITY
Every data object that enters or exits a pipeline must have a registered DEP-ID or be explicitly flagged as PROPOSED.
Flag if:
- A data object is named in a pipeline stage but has no DEP-ID assigned and no PROPOSED flag
- A DEP-ID is used in this spec but defined differently in another spec in the batch (naming conflict)
- A DEP-ID is listed as OUTPUT here but listed as INPUT in an earlier FR spec without a producing stage defined
- A PROPOSED DEP-ID exists but no registration requirement is stated in the Tasks section
- Two specs in the batch claim to produce the same DEP-ID (collision — see FR44/FR30 precedent)

## LENS 3 — BOUNDARY PRECISION
Each spec owns exactly one FR. No more. No less.
Flag if:
- A pipeline stage implements logic that belongs to an upstream FR (already specified elsewhere)
- A pipeline stage implements logic that belongs to a downstream FR (specified elsewhere or not yet specified)
- The spec's Scope section says something is "Out of Scope" but the Implementation Plan implements it anyway
- Two specs implement the same pipeline stage under different names (duplication — see FR35/FR36 precedent)

## LENS 4 — GATE & RECEIPT COMPLETENESS
Every quality gate must be complete. Every stage must write a receipt.
Flag if:
- A gate exists without an exact numeric threshold
- A gate has PASS and FAIL verdicts but no PROVISIONAL verdict where one is architecturally warranted
- A gate verdict has no named downstream consequence
- A pipeline stage changes data state but has no Receipt Chain Guard write specified
- Receipt Chain Guard entries use string-literal formats instead of the FR47 DEP-ENG-041 schema (see CRITICAL precedent from FR40-50 audit)
- The Receipt Chain Guard entries do not form a complete unbroken chain from ingestion to emit

## LENS 5 — CROSS-SPEC CONSISTENCY
The specs must form a coherent system, not independent documents.
Flag if:
- A DEP-ID produced by FR-X is consumed by FR-Y but the schema defined in FR-X does not contain the fields FR-Y expects to read
- An academic framework is cited differently across specs (e.g., same metric under different names or thresholds)
- A coach isolation constraint (ADR-01) is enforced in one spec but absent in another spec that touches the same data layer
- A Receipt Chain Guard naming convention is inconsistent across specs
- A JSON schema field exists in the output schema but has no corresponding resolution rule in the Implementation Plan (orphaned field)

---

# OUTPUT FORMAT

## AUDIT REPORT

### PASS — Specs with zero flags across all five lenses
List spec names only.

### FLAGS — One entry per flag, formatted as:
**[FR-NUMBER] | LENS [1-5] | SEVERITY: CRITICAL / WARNING / NOTE**
- **Finding:** One sentence describing exactly what is wrong
- **Location:** Section and stage where the issue occurs
- **Required Action:** Exactly what must be fixed before implementation

### SEVERITY DEFINITIONS
- **CRITICAL:** Implementation will break or produce incorrect output if this is not fixed before development begins
- **WARNING:** Implementation will proceed but will produce architectural debt or inconsistency that compounds across dependent FRs
- **NOTE:** Minor inconsistency or missing detail that does not block implementation but should be resolved

### SUMMARY STATISTICS
- Total specs reviewed:
- Specs with zero flags:
- Total CRITICAL flags:
- Total WARNING flags:
- Total NOTE flags:
- DEP-IDs flagged as PROPOSED requiring registration:
- Cross-spec consistency issues requiring arbitration:

---

# RULES FOR THIS REVIEW
- Do not rewrite any spec. Flag only.
- Do not suggest improvements. Flag only.
- Do not praise specs that pass. List them once under PASS.
- Every flag must name the exact FR, the exact section, and the exact required action.
- If a flag requires a decision that only the architect can make — say so explicitly in the Required Action field.
- If two specs contradict each other — flag both, not just the later one.
- Reference the following audit precedents and ensure the same class of issues is not repeated:
  - FR3/FR4 boundary violation (DEP-LIB-001 dual ownership) — resolved by surgical amputation
  - FR35/FR36 boundary violation (duplicated pipeline stages) — resolved by clean upstream ingestion
  - FR37 Context Premise overwrite (destructive DEP-ENG-006 collision) — resolved by temporal node update
  - FR44/FR30 DEP-ID namespace collision — resolved by re-assignment
  - FR40-50 Receipt Chain schema violations (string literals instead of FR47 hashes) — resolved by global standardization
  - FR42/FR46 asset ID mismatch (legacy UUIDs vs Universal Asset ID) — resolved by migration

---

## PREVIOUSLY COMPLETED AUDITS (REFERENCE ONLY)

- **FR1-9:** Audited + Revised ✅
- **FR10-19:** Audited + Revised ✅
- **FR20-29:** Audited + Revised ✅
- **FR30-39:** Audited + Revised ✅
- **FR40-50:** Audited + Revised ✅
