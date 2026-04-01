# CA11 Spec Audit Report
**Batch Scope:** Capability Area 11 (Quad-Platform Intelligence Layer) — FR-CA11-01 through FR-CA11-15
**Role:** Principal CCP Architecture Reviewer
**Date:** 2026-03-25

## PASS
*(Specs with zero flags across all five lenses)*
None. The entire batch suffers from systematic Layer 2 and Layer 4 violations.

## FLAGS

**FR-CA11-01 | LENS 2 | SEVERITY: WARNING**
- **Finding:** The `workspace_provisioning_payload.json` data object has no DEP-ID assigned and no PROPOSED flag.
- **Location:** Section 5 (Primary Output Schema)
- **Required Action:** Assign a new DEP-ID (e.g., DEP-ENG-071 PROPOSED) or register it appropriately.

**FR-CA11-01 | LENS 4 | SEVERITY: CRITICAL**
- **Finding:** The Receipt Chain Guard entry uses a string-literal format (`RC-CA11-01-20260324-001`) instead of the FR47 DEP-ENG-041 cryptographic hash schema.
- **Location:** Section 5 (Primary Output Schema)
- **Required Action:** Update `receipt_chain_id` to use the standardized FR47 hash specification.

**FR-CA11-02 | LENS 2 | SEVERITY: WARNING**
- **Finding:** The `content_push_payload.json` data object has no DEP-ID assigned and no PROPOSED flag.
- **Location:** Section 5 (Primary Output Schema)
- **Required Action:** Assign a new DEP-ID or register it appropriately.

**FR-CA11-02 | LENS 4 | SEVERITY: CRITICAL**
- **Finding:** The Receipt Chain Guard entry uses a string-literal format (`RC-CA11-02-20260324-001`) instead of the FR47 DEP-ENG-041 schema.
- **Location:** Section 5 (Primary Output Schema)
- **Required Action:** Update to the FR47 standardized hash format.

**FR-CA11-03 | LENS 2 | SEVERITY: WARNING**
- **Finding:** The `client_workspace_payload.json` data object has no DEP-ID assigned and no PROPOSED flag.
- **Location:** Section 5 (Primary Output Schema)
- **Required Action:** Assign a DEP-ID and mark as PROPOSED.

**FR-CA11-03 | LENS 4 | SEVERITY: CRITICAL**
- **Finding:** The Receipt Chain Guard entry uses a string-literal format (`RC-CA11-03-20260324-001`).
- **Location:** Section 5 (Primary Output Schema)
- **Required Action:** Standardize to the FR47 DEP-ENG-041 schema.

**FR-CA11-04 | LENS 2 | SEVERITY: WARNING**
- **Finding:** The `learning_path_entry.json` data object is not assigned a DEP-ID and lacks a PROPOSED flag.
- **Location:** Section 5 (Primary Output Schema)
- **Required Action:** Assign a DEP-ID (e.g., DEP-ENG-061 PROPOSED).

**FR-CA11-04 | LENS 4 | SEVERITY: CRITICAL**
- **Finding:** The pipeline changes data state (creating registry entries and Neo4j nodes) but lacks a Receipt Chain Guard write entirely.
- **Location:** Section 4 (Implementation Plan) & Section 5 (Schema)
- **Required Action:** Add Receipt Chain Guard write steps using the DEP-ENG-041 schema.

**FR-CA11-05 | LENS 2 | SEVERITY: WARNING**
- **Finding:** Data object `session_intelligence_report.json` lacks a DEP-ID and PROPOSED flag.
- **Location:** Section 5 (Primary Output Schema)
- **Required Action:** Assign a PROPOSED DEP-ID.

**FR-CA11-05 | LENS 4 | SEVERITY: CRITICAL**
- **Finding:** Receipt Chain Guard entry uses a string literal (`RC-CA11-05-20260324-001`).
- **Location:** Section 5 (Primary Output Schema)
- **Required Action:** Standardize to the FR47 hash schema.

**FR-CA11-06 | LENS 2 | SEVERITY: WARNING**
- **Finding:** Primary output schema lacks a DEP-ID or PROPOSED flag.
- **Location:** Section 5 (Primary Output Schema)
- **Required Action:** Assign a DEP-ID.

**FR-CA11-06 | LENS 4 | SEVERITY: CRITICAL**
- **Finding:** Pipeline changes data state (creating structured lessons and Neo4j learning path tags) but lacks any Receipt Chain write mechanism.
- **Location:** Section 4 & 5
- **Required Action:** Define Receipt Chain write steps using DEP-ENG-041.

**FR-CA11-07 | LENS 2 | SEVERITY: WARNING**
- **Finding:** The course definition output schema lacks a DEP-ID or PROPOSED flag.
- **Location:** Section 5 (Primary Output Schema)
- **Required Action:** Assign a DEP-ID.

**FR-CA11-07 | LENS 4 | SEVERITY: CRITICAL**
- **Finding:** Course assembly and drip scheduling change data states but omit Receipt Chain Guard logging.
- **Location:** Section 4
- **Required Action:** Include Receipt Chain logging per FR47 rules.

**FR-CA11-08 | LENS 2 | SEVERITY: WARNING**
- **Finding:** Primary output schema (Micro-Content array) lacks a DEP-ID or PROPOSED flag.
- **Location:** Section 5 (Primary Output Schema)
- **Required Action:** Assign a DEP-ID.

**FR-CA11-08 | LENS 4 | SEVERITY: NOTE**
- **Finding:** Receipt Chain Guard mentions an "update" but the Output Schema does not specify the `receipt_chain_id` field.
- **Location:** Section 4 & 5
- **Required Action:** Add the FR47 DEP-ENG-041 schema explicitly to the JSON payload.

**FR-CA11-09 | LENS 2 | SEVERITY: WARNING**
- **Finding:** The accountability chart output schema lacks a DEP-ID or PROPOSED flag.
- **Location:** Section 5 (Primary Output Schema)
- **Required Action:** Assign a DEP-ID.

**FR-CA11-09 | LENS 4 | SEVERITY: CRITICAL**
- **Finding:** Generation of weekly chart and recording of daily data changes state but lacks Receipt Chain writes.
- **Location:** Section 4 & 5
- **Required Action:** Define Receipt Chain entry logic adhering to FR47.

**FR-CA11-10 | LENS 2 | SEVERITY: WARNING**
- **Finding:** The block schema (`excalidraw-embed`) does not define a DEP-ID or PROPOSED flag.
- **Location:** Section 5 (Primary Output Schema)
- **Required Action:** Assign a DEP-ID for the custom block schema.

**FR-CA11-10 | LENS 4 | SEVERITY: NOTE**
- **Finding:** State sync via YJS CRDT does not define a Receipt Chain write on edit operations.
- **Location:** Section 4 (Implementation Plan)
- **Required Action:** Determine if CRDT collaborative edits require Receipt Chain persistence or if the initial injection suffices.

**FR-CA11-11 | LENS 2 | SEVERITY: WARNING**
- **Finding:** The Visual Production Console database entry payload lacks a DEP-ID.
- **Location:** Section 5 (Primary Output Schema)
- **Required Action:** Assign a PROPOSED DEP-ID.

**FR-CA11-11 | LENS 4 | SEVERITY: CRITICAL**
- **Finding:** The `affine_sync.py` entry creation does not specify a Receipt Chain write step, despite passing `receipt_chain_status` metadata.
- **Location:** Section 4 (Implementation Plan)
- **Required Action:** Add explicit Receipt Chain Guard write step using the DEP-ENG-041 schema.

**FR-CA11-12 | LENS 2 | SEVERITY: WARNING**
- **Finding:** Course video output schema lacks a DEP-ID and PROPOSED flag.
- **Location:** Section 5 (Primary Output Schema)
- **Required Action:** Assign a DEP-ID.

**FR-CA11-12 | LENS 4 | SEVERITY: CRITICAL**
- **Finding:** Pipeline registers the video in the learning path registry but lacks a standard Receipt Chain Guard write.
- **Location:** Section 4 & 5
- **Required Action:** Add Receipt Chain Guard write.

**FR-CA11-13 | LENS 2 | SEVERITY: WARNING**
- **Finding:** The recording status payload lacks a DEP-ID and PROPOSED flag.
- **Location:** Section 5 (Primary Output Schema)
- **Required Action:** Assign a DEP-ID.

**FR-CA11-13 | LENS 4 | SEVERITY: CRITICAL**
- **Finding:** Stage 3 Step 1 creates a `session_intelligence` record in Supabase but lacks a Receipt Chain Guard write.
- **Location:** Section 4 (Implementation Plan)
- **Required Action:** Add Receipt Chain Guard logging for the new database entry.

**FR-CA11-14 | LENS 2 | SEVERITY: WARNING**
- **Finding:** The overlay status payload lacks a DEP-ID.
- **Location:** Section 5 (Primary Output Schema)
- **Required Action:** Assign a DEP-ID.

**FR-CA11-15 | LENS 2 | SEVERITY: WARNING**
- **Finding:** The `resolved_palette` schema and extended `branding.json` override schema lack DEP-ID registration.
- **Location:** Section 4 & 5
- **Required Action:** Assign DEP-IDs for these configuration schemas.

**FR-CA11-04 & FR-CA11-07 | LENS 5 | SEVERITY: CRITICAL**
- **Finding:** FR-CA11-07 writes `content_type = course_chapter` to the `learning_path_registry`, but FR-CA11-04 defines the enum as `script, video, voice_lesson, webinar, session_recap, diagram, course_video` — entirely omitting `course_chapter`.
- **Location:** FR-CA11-04 (Section 4.1 enum definition) vs FR-CA11-07 (Section 4.1 Step 5 assignment).
- **Required Action:** Add `course_chapter` to the `content_type` enum in FR-CA11-04 to enable cross-pipeline compatibility.

## SUMMARY STATISTICS
- Total specs reviewed: 15
- Specs with zero flags: 0
- Total CRITICAL flags: 13
- Total WARNING flags: 15
- Total NOTE flags: 2
- DEP-IDs flagged as PROPOSED requiring registration: All 15 Primary Output Schemas across the batch.
- Cross-spec consistency issues requiring arbitration: 1 enum mismatch between FR-CA11-04 and FR-CA11-07.
