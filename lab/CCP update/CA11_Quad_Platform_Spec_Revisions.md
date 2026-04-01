# CA11 Spec Revision Instructions
**Batch Scope:** Capability Area 11 (Quad-Platform Intelligence Layer) — FR-CA11-01 through FR-CA11-15
**Role:** Principal CCP Architecture Reviser
**Date:** 2026-03-25

---

## DECISION LOG (Architect-Approved)

**Decision 1 — DEP-ID Range Allocation for CA11:**
To resolve systemic Lens 2 violations, the CA11 batch is allocated the DEP-ID range `DEP-ENG-071` through `DEP-ENG-086` for all primary output schemas and configuration payloads introduced in this capability area. These are marked as PROPOSED until registered in the central schema repository.

**Decision 2 — Enum Arbitration for `content_type` (Lens 5):**
FR-CA11-04 defines the `content_type` enum, but FR-CA11-07 requires `course_chapter`. FR-CA11-04 will be expanded to include `course_chapter` to satisfy FR-CA11-07's requirement without breaking backwards compatibility.

**Decision 3 — Universal Receipt Chain Enformencement (Lens 4):**
All data state changes (database writes, file generation, API payload pushes) across CA11 must trigger a standard FR47 DEP-ENG-041 cryptographic receipt. String literals are explicitly banned.

---

## GLOBAL FIX — ALL SPECS IN THIS BATCH

**Global Fix 1 — Receipt Chain Guard Standardization (LENS 4)**

Every receipt write across this batch must conform to the FR47 DEP-ENG-041 schema. 

For specs containing string literal schemas (FR-CA11-01, 02, 03, 05), replace `receipt_chain_id` strings with a nested object or schema pointer.
For specs completely missing receipt writes, append the following step to the final stage of their Implementation Plan:

"Write Receipt Chain Guard entry per FR47 DEP-ENG-041 schema: `{ receipt_id, previous_receipt_hash, input_payload_hash, output_payload_hash, stage_name, timestamp }`."

**Applies to:** All 15 specs in the CA11 batch.

---

## PER-SPEC REVISION INSTRUCTIONS

### FR-CA11-01 — REQUIRED FIXES (2 fixes)

**Fix 1 — Assign DEP-ID (LENS 2):**
Section 5, Primary Output Schema — Replace schema intro with:
"**Data Object:** Coach Workspace Provisioning Payload (`DEP-ENG-071` PROPOSED)"

**Fix 2 — Standardize Receipt Chain (LENS 4):**
Section 5, Primary Output Schema — Replace `"receipt_chain_id": "RC-CA11-01-20260324-001"` with:
`"receipt_chain_guard": { "schema_ref": "DEP-ENG-041" }`

---

### FR-CA11-02 — REQUIRED FIXES (2 fixes)

**Fix 1 — Assign DEP-ID (LENS 2):**
Section 5, Primary Output Schema — Replace schema intro with:
"**Data Object:** Content Push Payload (`DEP-ENG-072` PROPOSED)"

**Fix 2 — Standardize Receipt Chain (LENS 4):**
Section 5, Primary Output Schema — Replace `"receipt_chain_id": "RC-CA11-02-20260324-001"` with:
`"receipt_chain_guard": { "schema_ref": "DEP-ENG-041" }`

---

### FR-CA11-03 — REQUIRED FIXES (2 fixes)

**Fix 1 — Assign DEP-ID (LENS 2):**
Section 5, Primary Output Schema — Replace schema intro with:
"**Data Object:** Client Workspace Provisioning Payload (`DEP-ENG-073` PROPOSED)"

**Fix 2 — Standardize Receipt Chain (LENS 4):**
Section 5, Primary Output Schema — Replace `"receipt_chain_id": "RC-CA11-03-20260324-001"` with:
`"receipt_chain_guard": { "schema_ref": "DEP-ENG-041" }`

---

### FR-CA11-04 — REQUIRED FIXES (3 fixes)

**Fix 1 — Assign DEP-ID (LENS 2):**
Section 5, Primary Output Schema — Replace schema intro with:
"**Data Object:** Learning Path Entry (`DEP-ENG-074` PROPOSED)"

**Fix 2 — Integrate Receipt Chain (LENS 4):**
Section 4, Implementation Plan, Stage 2 — Add Step 3:
"3. Write Receipt Chain Guard entry per FR47 DEP-ENG-041 schema."
Section 5, Primary Output Schema — Add field to JSON:
`"receipt_chain_guard": { "schema_ref": "DEP-ENG-041" }`

**Fix 3 — Expand `content_type` Enum (LENS 5 / Resolves FR-CA11-07 mismatch):**
Section 4.1, Step 3 — Replace:
`"content_type" (enum: script, video, voice_lesson, webinar, session_recap, diagram, course_video)`
with:
`"content_type" (enum: script, video, voice_lesson, webinar, session_recap, diagram, course_video, course_chapter)`

---

### FR-CA11-05 — REQUIRED FIXES (2 fixes)

**Fix 1 — Assign DEP-ID (LENS 2):**
Section 5, Primary Output Schema — Replace schema intro with:
"**Data Object:** Session Intelligence Report (`DEP-ENG-075` PROPOSED)"

**Fix 2 — Standardize Receipt Chain (LENS 4):**
Section 5, Primary Output Schema — Replace `"receipt_chain_id": "RC-CA11-05-20260324-001"` with:
`"receipt_chain_guard": { "schema_ref": "DEP-ENG-041" }`

---

### FR-CA11-06 — REQUIRED FIXES (2 fixes)

**Fix 1 — Assign DEP-ID (LENS 2):**
Section 5, Primary Output Schema — Replace schema intro with:
"**Data Object:** Structured Lesson Output (`DEP-ENG-076` PROPOSED)"

**Fix 2 — Integrate Receipt Chain (LENS 4):**
Section 4, Stage 3 — Add Step 4:
"4. Write Receipt Chain Guard entry per FR47 DEP-ENG-041 schema."

---

### FR-CA11-07 — REQUIRED FIXES (2 fixes)

**Fix 1 — Assign DEP-ID (LENS 2):**
Section 5, Primary Output Schema — Replace schema intro with:
"**Data Object:** Course Definition Document (`DEP-ENG-077` PROPOSED)"

**Fix 2 — Integrate Receipt Chain (LENS 4):**
Section 4, Stage 3 — Add Step 4:
"4. Write Receipt Chain Guard entry per FR47 DEP-ENG-041 schema."

---

### FR-CA11-08 — REQUIRED FIXES (2 fixes)

**Fix 1 — Assign DEP-ID (LENS 2):**
Section 5, Primary Output Schema — Replace schema intro with:
"**Data Object:** Content Machine Array (`DEP-ENG-078` PROPOSED)"

**Fix 2 — Integrate Receipt Chain (LENS 4):**
Section 5, Primary Output Schema — Add field to each array object:
`"receipt_chain_guard": { "schema_ref": "DEP-ENG-041" }`

---

### FR-CA11-09 — REQUIRED FIXES (2 fixes)

**Fix 1 — Assign DEP-ID (LENS 2):**
Section 5, Primary Output Schema — Replace schema intro with:
"**Data Object:** Accountability Visual Chart Payload (`DEP-ENG-079` PROPOSED)"

**Fix 2 — Integrate Receipt Chain (LENS 4):**
Section 4, Stage 2 — Add Step 5:
"5. Write Receipt Chain Guard entry per FR47 DEP-ENG-041 schema after database commit."

---

### FR-CA11-10 — REQUIRED FIXES (2 fixes)

**Fix 1 — Assign DEP-ID (LENS 2):**
Section 5, Primary Output Schema — Replace schema intro with:
"**Data Object:** Excalidraw Embed Block Schema (`DEP-ENG-080` PROPOSED)"

**Fix 2 — Clarify Receipt Logging for CRDT (LENS 4):**
Section 4, Stage 2 — Add Step 4:
"4. Write Receipt Chain Guard entry per FR47 DEP-ENG-041 upon initial block creation (CRDT intermediate edits exclude receipt overhead)."

---

### FR-CA11-11 — REQUIRED FIXES (2 fixes)

**Fix 1 — Assign DEP-ID (LENS 2):**
Section 5, Primary Output Schema — Replace schema intro with:
"**Data Object:** Visual Production Console Database Entry (`DEP-ENG-081` PROPOSED)"

**Fix 2 — Integrate Receipt Chain (LENS 4):**
Section 4, Stage 2 — Add Step 7:
"7. Write Receipt Chain Guard entry per FR47 DEP-ENG-041 after creating the database entry."

---

### FR-CA11-12 — REQUIRED FIXES (2 fixes)

**Fix 1 — Assign DEP-ID (LENS 2):**
Section 5, Primary Output Schema — Replace schema intro with:
"**Data Object:** Course Video Manifest (`DEP-ENG-082` PROPOSED)"

**Fix 2 — Integrate Receipt Chain (LENS 4):**
Section 4, Stage 4 — Add Step 5:
"5. Write Receipt Chain Guard entry per FR47 DEP-ENG-041."

---

### FR-CA11-13 — REQUIRED FIXES (2 fixes)

**Fix 1 — Assign DEP-ID (LENS 2):**
Section 5, Primary Output Schema — Replace schema intro with:
"**Data Object:** Recording Status Payload (`DEP-ENG-083` PROPOSED)"

**Fix 2 — Integrate Receipt Chain (LENS 4):**
Section 4, Stage 3 — Adjust Step 1 to include:
"1d. Write Receipt Chain Guard entry per FR47 DEP-ENG-041 schema after saving the `session_intelligence` record."

---

### FR-CA11-14 — REQUIRED FIXES (1 fix)

**Fix 1 — Assign DEP-ID (LENS 2):**
Section 5, Primary Output Schema — Replace schema intro with:
"**Data Object:** OBS Overlay Status Payload (`DEP-ENG-084` PROPOSED)"

---

### FR-CA11-15 — REQUIRED FIXES (2 fixes)

**Fix 1 — Assign DEP-ID to Output Payload (LENS 2):**
Section 5, Primary Output Schema — Add text before "Resolved Palette":
"**Data Object:** Resolved Palette Schema (`DEP-ENG-085` PROPOSED)"

**Fix 2 — Assign DEP-ID to Ext Branding (LENS 2):**
Section 4, Extended Schema — Add text above schemablock:
"**Data Object:** Extended Branding Configuration (`DEP-ENG-086` PROPOSED)"
