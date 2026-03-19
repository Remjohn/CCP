# Tech-Spec: FR0A — Business Intelligence Extraction (Capability Area 0)

**Created:** 2026-03-18
**Status:** Ready for Development
**Version:** 2.0 (Aligned to CCP Architecture V2)
**Architecture Reference:** CCP_Architecture_Documentation_V2 §2–§8, CCP_Sales_Cycle_Documentation_V1 §Capability Area 0, PRD §Capability Area 0 (FR0A)

---

## Overview

### Problem Statement
Every FR in the CCP assumes foundational intelligence objects already exist. Content generation and campaign positioning (FR51–FR60) expect `coach_business_summary.json` (DEP-ENG-050) to contain authentic positioning intelligence. Without FR0A, campaign positioning uses the coach's generic marketing language instead of their verified transformation evidence. 

### Solution
Stage 1 of the Capability Area 0 intelligence extraction pipeline. The Business Model Assistant agent creates a structured Business Intelligence Summary using a CRAL-informed extraction approach. It produces DEP-ENG-050 as the seed for all downstream extraction.

### Scope
**In scope:**
- FR0A Business Intelligence Extraction (DEP-ENG-050)
- 5-dimension CRAL-informed analysis (Value Proposition, Revenue Architecture, Audience Precision, Market Positioning, Content Philosophy)
- Positioning Precision Test quality gate
- ADR-01 isolation constraints

**Out of scope:**
- Downstream CPSC Campaign Layer (FR51–FR60)
- 5-Phase Guardian Interview Protocol orchestration (handled by FR-GA)

---

## Context for Development

### Architecture Traceability
| DEP-ID | Name | Role | Producing FR | Consuming FRs |
|---|---|---|---|---|
| `DEP-ENG-050` | Business Intelligence Summary | Seed for all downstream extraction — positioning, audience, differentiation | FR0A | FR0B, FR1, FR7, FR51, FR52 |
| `PROPOSED: DEP-PROTO-019` | 5-Phase Interview Protocol | OARS-structured onboarding interview specification | FR-GA Genesis | FR0A, FR0B seed data |

### Agent Roster
| Agent | Role |
|---|---|
| **Business Model Assistant** | Business intelligence extraction — 5-dimension CRAL-informed analysis |

### Technical Decisions
| Decision | Rationale | ADR-01 Impact |
|---|---|---|
| **Strict sequential execution** | Epistemological order: business → tribe. Produces the intelligence the next stage requires. | All reads/writes scoped to current coach tenant. |
| **OARS interview architecture** | Coaches answer questions from their coaching mask, not their authentic self, unless the interview structure prevents it. | Interview data stored per coach only. |

---

## Implementation Plan

### Stage 1: FR0A — Business Intelligence Extraction

**Agent:** Business Model Assistant (formalized SKILL.md)
**Prerequisite:** 5-Phase Interview Protocol Phase 1 complete + coach source folder uploaded
**ADR-01:** All reads/writes scoped to `coach_id`. Source folder stored in coach-specific workspace.

#### Source Ingestion

The Guardian Agent accepts a coach source folder containing website content, video transcripts, existing positioning documents, and recorded materials. The folder-based ingestion eliminates manual data entry — the system processes what the coach already has.

The 5-Phase Interview Protocol Phase 1 supplements the folder with 8-10 authenticated questions covering:
- Offer architecture (what exactly is being sold and at what price points)
- Transformation claim (the specific before→after journey the coach delivers)
- Audience definition (who buys, who doesn't, why)
- Market differentiation (what competitors cannot claim)
- Content philosophy (beliefs about content's role in the business)

#### Intelligence Synthesis — 5-Dimension Analysis

| Dimension | Source Priority | CRAL Depth Pass |
|---|---|---|
| Value Proposition | Source folder + Interview Phase 1 | **Yes** — minimum 3 verified real-person transformation stories (Human Evidence Bias gate, per CRAL_Documentation_V1) |
| Revenue Architecture | Source folder + Interview | No — structural analysis sufficient |
| Audience Precision | Interview + source folder | No — Interview Phase 5 provides deeper audience seed |
| Market Positioning | Source folder | **Yes** — CRAL vertical on differentiation claim with competitor evidence |
| Content Philosophy | Interview Phase 1 | No — authenticated coach voice is the authority |

The CRAL-informed vertical depth pass on Value Proposition and Market Positioning surfaces the gap between the coach's marketing language and the transformation their clients actually experience. This gap is frequently the most strategically valuable intelligence FR0A produces.

#### Output
**Primary:** `coach_business_summary.json` (DEP-ENG-050)
- 60-80 word positioning summary (3rd person: expertise→audience→pain→solution)
- Extended intelligence appendix with all 5 dimensions fully documented
- Transformation evidence corpus (≥3 real-person stories with verbatim language)

#### Quality Gate: Positioning Precision Test
**Threshold:** Binary PASS/FAIL
**Test:** Replace the coach's name in the positioning summary with the name of a direct competitor in the same niche. If the summary still accurately describes the competitor, the extraction has failed — it captured category-level intelligence, not coach-specific intelligence.

**Pass example:** "Adèle Marie transforms corporate executives who have achieved everything society told them to want — but who wake at 3am knowing their success is built on someone else's definition of enough — through a 90-day somatic integration process that reconnects ambition to the body's actual signals, not the mind's inherited scripts."
→ Replacing "Adèle Marie" with any competitor breaks the description. The method, the audience specificity, and the transformation language are unique.

**Fail example:** "X helps high-achieving professionals overcome limiting beliefs and step into their full potential through transformative coaching."
→ FAIL. This describes any transformation coach. No competitor would be uncomfortable reading it.

#### Failure Condition
If Positioning Precision Test fails → pipeline halts. Guardian Agent issues FAILED verdict with specific feedback: which dimensions are generic. Operator must provide deeper source material (additional Sacred Audio, client testimonials, competitor analysis) and re-execute FR0A.

#### Receipt Chain Guard
- **INGEST:** Source folder received + Interview Phase 1 complete → receipt written with `source_document_count`, `interview_response_count`, `timestamp`
- **EMIT:** DEP-ENG-050 registered → receipt written with `positioning_precision_test: PASS/FAIL`, `transformation_story_count`, `verdict`

---

## Tasks

- [ ] **Task 1:** Formalize Business Model Assistant as SKILL.md — add Receipt Chain Guard writes, DEP-ID declarations, quality gate formalization, failure conditions, ADR-01 isolation constraint
- [ ] **Task 2:** Implement FR0A pipeline — source folder ingestion + Interview Phase 1 integration + 5-dimension synthesis + CRAL vertical depth pass + Positioning Precision Test

---

## Acceptance Criteria

- [ ] **AC1 (Positioning Precision):** A `coach_business_summary.json` where the coach name can be replaced with a competitor's name without breaking accuracy is rejected by the Positioning Precision Test. Test: generate summary → substitute name → verify FAIL verdict with specific feedback.

---

## Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR-GA Guardian Agent | Internal orchestrator | Manages the execution sequence and 5-Phase Interview |
| FR1 Genesis Pipeline | Internal downstream | Consumes Capability Area 0 outputs |
| FR51–FR60 CPSC | Internal downstream | Consumes DEP-ENG-050 |
| FR47 Receipt Chain Guard | Internal standard | All receipt writes follow DEP-ENG-041 schema |

---

## Testing Strategy

### Quality Gate Boundary Test
- Test at the exact threshold boundary:
  - Positioning Precision: summary that barely passes vs. barely fails
- Validate: gate produces the correct verdict at the boundary.
