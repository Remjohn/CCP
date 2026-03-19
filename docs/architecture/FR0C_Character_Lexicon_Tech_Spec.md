# Tech-Spec: FR0C — Character Lexicon Population (Capability Area 0)

**Created:** 2026-03-18
**Status:** Ready for Development
**Version:** 2.0 (Aligned to CCP Architecture V2)
**Architecture Reference:** CCP_Architecture_Documentation_V2 §2–§8, PRD §Capability Area 0 (FR0C)

---

## Overview

### Problem Statement
Downstream pipelines, like CRAL (FR14) and the Semiotic Composer, require Character Lexicon entries to build resonance, contrast, and relatability in content. If a centralized, culturally grounded lexicon does not exist, characters are either manually inserted without tribal validation or randomly generated, causing significant degradation in asset resonance. 

### Solution
Stage 3 of the Capability Area 0 pipeline. Populates a Character Lexicon of 65 entries across 5 functional categories based on the converged findings of the H11 Tribe Dossier. Governed by the DEP-PROTO-017 Character Invocation Protocol for deterministic runtime selection.

### Scope
**In scope:**
- 65-Character Schema population (5 functional categories)
- Character Invocation Protocol (DEP-PROTO-017)
- `character_lexicon` SQL table and `character_usage_registry` initialization
- Psychological Specificity Test
- Jungian Specificity Rule mappings

**Out of scope:**
- Semiotic combinations and visual formats (handled by FR0D)
- Brand Avatars (handled by FR0E)

---

## Context for Development

### Architecture Traceability
| DEP-ID | Name | Role | Producing FR | Consuming FRs |
|---|---|---|---|---|
| `character_lexicon` | Character Lexicon (65 entries) | Cultural pantheon database (heroes, icons, validators, enemies, opposition) | FR0C | FR14 (M2-M5), FR35, FR36, Semiotic Composer |
| `character_usage_registry` | Character Usage Registry | Non-repetition enforcement + relevance scoring data | FR0C | Data Analyst, Stewardship Mode |
| `DEP-PROTO-017` | Character Invocation Protocol | Structured query API for runtime character selection | FR0C (defined) | All downstream agents |

### Agent Roster
| Agent | Role |
|---|---|
| **Character Research Strategist** | Character identification from H11 Tribe Dossier, 65 entries across 5 categories |
| **SQL Coder Agent** | Writes `character_lexicon` entries to Supabase with full schema compliance |

### Technical Decisions
| Decision | Rationale | ADR-01 Impact |
|---|---|---|
| **V2 65-character schema** | Characters organized by content deployment function, not hero/enemy valence. A figure can be heroic in one context and cautionary in another. | Per-coach `character_lexicon` table with `coach_id` column isolation. |
| **SQL for filtered queries** | Needs queries like "all Category 1 matching M4 + fairness_cheating". Filter queries require SQL storage. | Storage targets enforce coach-tenant isolation. |

---

## Implementation Plan

### Stage 3: FR0C — Character Lexicon Population

**Agent:** Character Research Strategist + SQL Coder Agent
**Prerequisite:** H11 Tribe Dossier (FR0B) + DEP-ENG-050 (FR0A)
**ADR-01:** `character_lexicon` Supabase table filtered by `coach_id`. All queries include coach_id WHERE clause.

#### The 65-Character Schema (V2)

| Category | Count | Function | Primary CRAL Moment | Content Mode |
|---|---|---|---|---|
| 1 — Aspirational Heroes | 20 | Figures the tribe wants to become. | M4 RESONANT — parallel story anchoring | Status / Processing |
| 2 — Nostalgic Icons | 15 | Figures from the tribe's formative period. | M7 RELATABLE — shared reference activation | Escape / Recognition |
| 3 — Credibility Validators | 10 | Currently active respected voices. | M2 BELIEVABLE — human evidence anchoring | Discovery / Processing |
| 4 — Cautionary Enemies | 10 | Figures representing wrong paths. | M3 UNDENIABLE — contrast evidence | Tension / T-mode |
| 5 — Ideological Opposition | 10 | Figures holding the opposing worldview. | M5 SURPRISING — unexpected validation | Tension / high-arousal |

#### Schema Fields per Entry
| Field | Type | Source | Resolution Rule |
|---|---|---|---|
| `character_id` | UUID | Auto-generated | Supabase UUID primary key |
| `coach_id` | UUID | Coach registry | ADR-01 tenant isolation key |
| `name` | String | H11 convergence analysis | Figure's recognizable name |
| `category` | Integer (1-5) | Strategist | Functional classification per 5-category schema |
| `role_definition` | String | H11 + FR0A | Why this figure matters TO THIS TRIBE — not biography |
| `cral_moments[]` | Array[String] | Default + override | CRAL moment IDs where this character is deployable |
| `moral_foundation_activated` | String | E-DNA analysis | Which of the 6 MFT foundations this character activates |
| `content_mode_fit[]` | Array[String] | Default + override | Emotional modes this character is appropriate for |
| `character_prompt` | String | Strategist | Image generation prompt for visual deployment |
| `last_deployed_date` | ISO8601 | System-maintained | Most recent content deployment timestamp |
| `relevance_score` | Float (0.0-1.0) | Data Analyst | Weekly scoring (below 0.4 triggers Evolution flag) |
| `gaze_direction` | Enum | Rel depth | Directed at hook zone or action zone |

#### Character Invocation Protocol (DEP-PROTO-017)
The `character_lexicon` is queried, not browsed. Downstream agents use 5 parameters: `cral_moment`, `moral_foundation`, `content_mode`, `audience_maturity`, `exclusion_window` (defaults to 8 weeks).
**Response:** Ranked list of eligible characters with `selection_justification`.
**Non-Repetition Rule:** Applied per format type, not globally.
**Usage Logging:** Every invocation logged to `character_usage_registry`.

#### Jungian Specificity Rule
Archetypes are never deployed without a character lexicon anchor. 
| Archetype | Character Lexicon Anchor |
|---|---|
| Hero | Category 1 — Aspirational Hero |
| Sage | Category 3 — Credibility Validator |
| Shadow | Category 4 — Cautionary Enemy |
| Trickster | Category 2 — Nostalgic Icon |

#### CRAL Connection Mapping
- **M2 (Believable):** Cat 3 filtered by moral foundation
- **M3 (Undeniable):** Cat 4 + 5 for contrast mechanism
- **M4 (Resonant):** Cat 1 + 2 for parallel story anchoring
- **M5 (Surprising):** Cat 5 for cognitive dissonance events

#### Output
- 65 entries in `character_lexicon` Supabase table
- `character_usage_registry` initialized
- DEP-PROTO-017 defined and API-ready

#### Quality Gate: Psychological Specificity Test
**Threshold:** Binary PASS/FAIL per entry.
**Test:** Each `role_definition` must specify what the character represents to this specific tribe, not a biographical summary.
- **Pass example:** Warren Buffett → "Represents the tribe's belief that patient, long-term thinking is the ultimate rebellion against the hype-driven financial media..."
- **Fail example:** Warren Buffett → "One of the most successful investors of all time..." → FAIL.

#### Receipt Chain Guard
- **INGEST:** H11 + DEP-ENG-050 received → receipt with `h11_version`, `dep_eng_050_version`
- **EMIT:** 65 entries written → receipt with `category_counts[]`, `specificity_test_results`, `verdict`

---

## Tasks

- [ ] **Task 1:** Build Character Research Strategist agent — H11 analysis, 65-character identification across 5 categories, `role_definition` generation, CRAL moment mapping
- [ ] **Task 2:** Implement Character Invocation Protocol (DEP-PROTO-017) — structured query API (5 parameters), ranked response with `selection_justification`, non-repetition enforcement, Usage Registry logging
- [ ] **Task 3:** Build SQL Coder Agent integration — `character_lexicon` Supabase table schema, batch write with validation, `character_usage_registry` initialization

---

## Acceptance Criteria

- [ ] **AC1 (Character Specificity):** A `character_lexicon` entry with `role_definition` "successful entrepreneur" is rejected by the Psychological Specificity Test. An entry tailored to the tribe's belief system passes. Test: submit varying specificities → verify rejection/acceptance.
- [ ] **AC2 (Non-Repetition):** A Character Invocation API query for a character deployed in the same content format within the 8-week exclusion window returns the character EXCLUDED from the ranked list. The same character used in a different format is NOT excluded. Test: log usage → query → verify exclusion logic.
- [ ] **AC3 (Jungian Anchor):** Any visual composition request that deploys a Jungian archetype without a corresponding character anchor is rejected with `JUNGIAN_ANCHOR_REQUIRED` error. Test: request archetype without character → verify rejection.

---

## Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR0A Business Intelligence | Internal prerequisite | For `dep_eng_050` seed |
| FR0B Tribe Soul Research | Internal prerequisite | H11 provides source material |
| FR14 CRAL Research Subsystem | Internal downstream | Queries API via DEP-PROTO-017 |
| Supabase | External service | SQL storage targets |

---

## Testing Strategy

### Character Invocation Protocol Test
- Populate `character_lexicon` with 65 entries
- Execute 100 invocation queries with varying parameters
- Validate: Non-repetition rule enforced correctly (per format type, not globally)
- Validate: Relevance score threshold respected
- Validate: All invocations logged to `character_usage_registry`
- Validate: Jungian Specificity Rule enforced
