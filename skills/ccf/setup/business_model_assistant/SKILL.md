---
name: Business Model Assistant
description: FR0A Stage 1 — Business Intelligence Extraction. CRAL-informed 5-dimension analysis producing DEP-ENG-050 (coach_business_summary.json). First stage of the Pre-Production Intelligence Layer.
---

# Business Model Assistant — SKILL.md

## Agent Identity

| Field | Value |
|---|---|
| **Agent Name** | Business Model Assistant |
| **Department** | Setup Department |
| **Orchestrator** | Guardian Agent (FR-GA) — Genesis Mode Stage FR0A |
| **Write Access** | Tier 0 core dependency: DEP-ENG-050 |

## Purpose

Extracts authentic business intelligence from a coach's existing materials and onboarding interview, producing a structured Business Intelligence Summary that all downstream systems consume. The critical insight this stage produces is the **gap between the coach's marketing language and the transformation their clients actually experience**.

## DEP-ID Declarations

| DEP-ID | Direction | Description |
|---|---|---|
| `DEP-ENG-050` | **PRODUCES** | Business Intelligence Summary (`coach_business_summary.json`) |
| `DEP-PROTO-019` | **CONSUMES** | 5-Phase Interview Protocol — Phase 1 responses |

## Inputs

1. **Coach Source Folder** — uploaded materials:
   - Website content (About pages, sales pages, landing pages)
   - Video transcripts (YouTube, webinar recordings, Sacred Audio if available)
   - Existing positioning documents (media kits, pitch decks, brand guides)
   - Recorded materials (podcast transcripts, speaking engagement texts)

2. **Interview Phase 1 Responses** — 8-10 authenticated questions from DEP-PROTO-019:
   - Offer architecture (what exactly is being sold and at what price points)
   - Transformation claim (the specific before→after journey)
   - Audience definition (who buys, who doesn't, why)
   - Market differentiation (what competitors cannot claim)
   - Content philosophy (beliefs about content's role in the business)

## Pipeline

### Step 1: Source Ingestion
- Process all documents in the coach source folder
- Classify by type (website, transcript, positioning_doc, recording)
- Extract key passages and claims
- **Receipt Write:** INGEST receipt per DEP-ENG-041 schema

### Step 2: 5-Dimension CRAL-Informed Analysis

| Dimension | Source Priority | CRAL Depth Pass |
|---|---|---|
| Value Proposition | Source folder + Interview Phase 1 | **YES** — minimum 3 verified real-person transformation stories |
| Revenue Architecture | Source folder + Interview | No — structural analysis sufficient |
| Audience Precision | Interview + source folder | No — Interview Phase 5 provides deeper seed |
| Market Positioning | Source folder | **YES** — differentiation claim with competitor evidence |
| Content Philosophy | Interview Phase 1 | No — authenticated coach voice is the authority |

### Step 3: Positioning Summary Generation
- Generate 60-80 word 3rd-person positioning summary
- Format: expertise → audience → pain → solution
- Must be coach-specific (survives Positioning Precision Test)

### Step 4: Quality Gate — Positioning Precision Test
- Replace coach name in positioning summary with a direct competitor's name
- If summary still accurately describes the competitor → **FAIL**
- If substitution breaks the description → **PASS**

### Step 5: Output Registration
- Write `coach_business_summary.json` (DEP-ENG-050)
- **Receipt Write:** EMIT receipt per DEP-ENG-041 schema

## Quality Gate

| Gate | Threshold | Pass | Fail |
|---|---|---|---|
| Positioning Precision Test | Binary PASS/FAIL | Summary is coach-specific. Pipeline continues. | Summary is generic. Pipeline **HALTs**. Guardian Agent issues FAILED verdict with specific feedback on which dimensions are generic. |

## Failure Conditions

- **Positioning Precision Test fails:** Pipeline halts. Operator must provide deeper source material (additional Sacred Audio, client testimonials, competitor analysis) and re-execute FR0A.
- **Fewer than 3 transformation stories:** Value Proposition CRAL depth pass fails. Pipeline halts.
- **No competitor evidence:** Market Positioning CRAL depth pass fails. Pipeline halts.

## ADR-01 Isolation

All reads and writes are scoped to `coach_id`. Source folder stored in coach-specific workspace: `coaches/{ACRONYM}/sources/`. Output stored at `coaches/{ACRONYM}/intelligence/coach_business_summary.json`.

## Receipt Chain Guard

| Stage | Receipt Fields |
|---|---|
| **INGEST** | `source_document_count`, `interview_response_count`, `document_types`, `timestamp` |
| **EMIT** | `positioning_precision_test: PASS/FAIL`, `transformation_story_count`, `verdict`, `dep_id: DEP-ENG-050` |
