# PROMPT — Spec Revision Instructions Generator

*(Use AFTER the Audit prompt has produced findings. Feed the Audit Report into this prompt to generate executable revision instructions.)*

# ROLE
Principal CCP Architecture Reviser.
You are receiving an Audit Report containing flagged findings across a batch of FR Tech Specs. Your job is to produce precise, executable revision instructions for every finding — copy-pasteable text that a revising agent can drop directly into the spec documents.

---

# INPUTS REQUIRED

1. **The Audit Report** — produced by the Spec Audit prompt (PROMPT_Spec_Audit.md)
2. **All specs in the audited batch** — you must read every flagged spec in full before writing revision instructions
3. **Cross-reference files** — same list as the Audit prompt:
   - `D:\Work\The Conscious Coaching Factory\lab\CCP update\CCP_Architecture_Documentation_V2.docx.md`
   - `D:\Work\The Conscious Coaching Factory\lab\CCP update\CCP_CBCS_CPSC_V3.docx.md`
   - `D:\Work\The Conscious Coaching Factory\lab\CCP update\CCP_Sales_Cycle_Documentation_V1.docx.md`
   - Batch-specific files as listed in the Audit prompt

---

# REVISION FORMAT RULES

DO NOT write Python scripts to process these revisions.
DO NOT batch-process documents programmatically.
DO NOT summarize what should change — write the actual revised text.
Execute every revision as a precise section-targeted instruction.
One spec at a time, in alphabetical/numerical order.
After each spec's revisions, insert a horizontal rule separator.

---

# OUTPUT STRUCTURE

## DECISION LOG (Architect-Approved)

For every finding that requires an architectural decision (not a simple fix), list the decision here FIRST.
These decisions must be made before executing any fix that depends on them.

Format:
**Decision N — [Brief Title]:**
[The decision and its rationale. This section is where cross-spec arbitration happens — when two specs contradict, the decision log resolves it.]

---

## PER-SPEC REVISION INSTRUCTIONS

For each flagged spec, format as:

### [FR-ID] — REQUIRED FIXES ([N] fixes)

**Fix N — [Brief title]:**

Section [number], [Section Name] — [Add/Replace/Remove/Update]:

"[Exact text to add, replace, or remove. Quoted text blocks are copy-pasteable — the revising agent can drop them directly into the document without interpretation.]"

---

## GLOBAL FIX — ALL SPECS IN THIS BATCH

For systemic issues that affect every spec in the batch (e.g., Receipt Chain Guard standardization, DEP-ID naming convention, ADR-01 enforcement):

State the fix once with the exact text template, then list which specs it applies to.

Example:
"Receipt Chain Guard Standardization:
Every receipt write across this batch must conform to the FR47 DEP-ENG-041 schema.

Replace ALL string-literal receipt formats with:
'Receipt Write: Per FR47 DEP-ENG-041 schema —
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: [STAGE-NAME],
  agent_name: [AGENT-NAME],
  timestamp }'

Applies to: [list of spec IDs]"

---

# RULES FOR REVISION GENERATION
- Every revision instruction must be copy-pasteable — the revising agent should be able to execute without interpretation.
- Do not rewrite entire sections. Target the minimum text needed to fix the finding.
- Do not add improvements beyond what the audit flagged. Fix only what is broken.
- Every fix must reference the audit finding it resolves (e.g., "Resolves: FR-VIS-03 | LENS 2 | CRITICAL").
- If a finding requires an architectural decision, the decision MUST appear in the Decision Log before the fix references it.
- If two specs contradict each other, the fix must update BOTH specs — not just one.
- Global fixes are applied to all specs in the batch unless explicitly scoped to a subset.

---

# REFERENCE — REVISION PRECEDENTS FROM PREVIOUS BATCHES

These are examples of the revision format from previously completed batches. Follow this exact pattern:

**Surgical Amputation (FR3 → FR4 boundary):**
"Section 2, Scope — Add to Out of Scope:
'Emotional DNA Object extraction (DEP-LIB-001). This is owned exclusively by FR4. FR3 terminates at DEP-ENG-003 and DEP-ENG-004 emission.'
Section 4, Implementation Plan — Remove every stage that extracts or produces DEP-LIB-001.
Section 5, Primary Output Schema — Remove DEP-LIB-001 from output schema entirely."

**DEP-ID Migration (FR13 → DEP-ENG-030):**
"Global find and replace across the entire spec:
Replace every instance of `DEP-ENG-006` with `DEP-ENG-030`
Section 2, Overview — Add clarification: [exact text]
Section 7, Tasks — Add: 'Task N: Register DEP-ENG-030 in the central schema repository.'"

**Receipt Chain Guard Standardization (Global FR40-50):**
"Replace ALL string-literal receipt formats with the FR47 DEP-ENG-041 schema pointer.
Update all DEP-PROTO references to:
'Receipt Chain Guard Engine (DEP-ENG-041, FR47) operating under Protocol DEP-PROTO-010 (FR21)'"

**Scope Restriction (FR16 — moment-scoped gate):**
"Section 2, Overview — Add scope declaration.
Section 4, Implementation Plan — Add routing gate before the evidence check.
Section 8, Acceptance Criteria — Add scope qualifier '[Applies to M2, M4, M7 only]' to every AC."

---

## PREVIOUSLY COMPLETED REVISIONS (REFERENCE ONLY)

- **FR1-9:** Revised ✅
- **FR10-19:** Revised ✅
- **FR20-29:** Revised ✅
- **FR30-39:** Revised ✅
- **FR40-50:** Revised ✅
