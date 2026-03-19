# Tech-Spec: FR0E — Brand Avatar Generation (Capability Area 0)

**Created:** 2026-03-18
**Status:** Ready for Development
**Version:** 2.0 (Aligned to CCP Architecture V2)
**Architecture Reference:** CCP_Architecture_Documentation_V2 §2–§8, PRD §Capability Area 0 (FR0E)

---

## Overview

### Problem Statement
In earlier architectures, brand avatars were selected via fixed defaults (`is_client_default`), ensuring visual consistency but failing to establish deep psychological resonance. Fixed avatars create a sense of professional empathy rather than neural coupling.

### Solution
Stage 5 of the Capability Area 0 pipeline. Extracts visual archetypes from the coach's authenticated story corpus. V2 replaces fixed defaults with Content-Context Routing. Avatar selection is driven by the target audience's coping trajectory position and the content's active emotional mode.

### Scope
**In scope:**
- Avatar extraction from authenticated story corpus
- Schema definition (Mentor, Struggler, Rebel, Origin)
- Content-Context Routing function
- Narrative Authenticity Test

**Out of scope:**
- Downstream visual composition formatting (handled by Semiotic Composer/FR35/FR36)

---

## Context for Development

### Architecture Traceability
| DEP-ID | Name | Role | Producing FR | Consuming FRs |
|---|---|---|---|---|
| `brand_avatars` | Brand Avatar Profiles | Coach narrative visual cast — stored as entries in `character_lexicon` | FR0E | FR50, FR-VIS-03, FR54 |

### Agent Roster
| Agent | Role |
|---|---|
| **Guardian Agent** | Analyzes coach's authenticated story corpus to extract avatar states |

### Technical Decisions
| Decision | Rationale | ADR-01 Impact |
|---|---|---|
| **Content-context routing** | Context routing produces neural coupling — matching coach's narrative past to audience's narrative present. | Avatar selection query scoped to coach-tenant. |

---

## Implementation Plan

### Stage 5: FR0E — Brand Avatar Generation

**Agent:** Guardian Agent (analyzes coach's authenticated story corpus)
**Prerequisite:** Coach story corpus (from FR2 Sacred Audio + FR1 Genesis materials) + DEP-ENG-050 + `character_lexicon` (FR0C)
**ADR-01:** Avatar entries stored as `character_lexicon` entries with coach-specific `coach_id`.

#### Avatar Extraction Method
The Guardian Agent identifies distinct narrative situations in the coach's Hero's Journey — situations, not ages or titles. Each avatar represents a stage of professional evolution that the coach has authentically lived through. The extraction uses the coach's authenticated story corpus as the primary source.

#### Avatar Schema Fields
| Field | Specification |
|---|---|
| `situation_category` | Enum: Mentor / Struggler / Rebel / Origin |
| `emotional_state` | Precise description — not "stressed" but specific contextual exhaustion |
| `wardrobe_and_styling` | Context-appropriate appearance description for image generation |
| `contextual_setting` | Environment that reflects the narrative situation |
| `coping_trajectory_routing[]` | Audience coping stages where this avatar is contextually appropriate |
| `emotional_mode_routing[]` | Content emotional modes (T/V/R) where this avatar activates |

#### Content-Context Routing (V2)
| Audience Coping Stage | Emotional Mode | Recommended Avatar | Rationale |
|---|---|---|---|
| SEARCH (peak receptivity) | Processing / Discovery | Mentor | Authority figure — wisdom receiver frame |
| SEARCH | Tension | Rebel / Origin | Defiance resonance — fight validation |
| ACTIVE (executing) | Discovery / Status | Mentor | Path confirmation — authority validates current action |
| ACTIVE | Recognition | Nostalgic equivalent | Peer-level celebration rather than authority validation |
| EXHAUSTED (depleted) | Vulnerability | Struggler | Depth-match — someone has been exactly here |
| EXHAUSTED | Escape | Origin / early journey | Lightness — return to before the weight accumulated |
| Any stage | Tension (tribal) | Rebel | Righteous indignation validation |

#### Output
- Brand Avatar entries in `character_lexicon` with routing metadata
- Avatar routing function registered in Semiotic Composer's DEP-PROTO-018

#### Quality Gate: Narrative Authenticity Test
**Threshold:** Binary PASS/FAIL
**Test:** Each avatar's `emotional_state` description must trace to a specific moment in the coach's authenticated story corpus. Generic descriptions fail.
- **Fail example:** Struggler avatar with emotional_state "feeling overwhelmed by work" → FAIL.
- **Pass example:** Struggler avatar with emotional_state "...Saturday morning in the gym parking lot... texting 'on my way!'..." → PASS. Traced to transcript 03, timestamp 4:32.

#### Receipt Chain Guard
- **INGEST:** Story corpus + DEP-ENG-050 + `character_lexicon` received
- **EMIT:** Avatar entries written → receipt with `avatar_count`, `routing_function_registered`, `narrative_authenticity_test: PASS/FAIL`, `verdict`

---

## Tasks

- [ ] **Task 1:** Implement FR0E Brand Avatar extraction — story corpus analysis, avatar identification, routing metadata population, content-context routing function registration.

---

## Acceptance Criteria

- [ ] **AC1 (Content-Context Routing):** For an EXHAUSTED audience in Vulnerability mode, the routing function returns the Struggler avatar. For a SEARCH audience in Processing mode, it returns the Mentor. Test: provide routing parameters → verify correct avatar selection for all 7 combinations.
- [ ] **AC2 (Narrative Authenticity Test):** Avatar definitions lacking direct citation traces to the coach's established `coach_soul.json` or source transcripts trigger a FAILED verdict. 

---

## Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR2 Sacred Audio Ingestion | Internal prerequisite | Coach story corpus for FR0E avatar extraction |
| `character_lexicon` | Internal storage | Avatars are written to this existing table |
| Semiotic Composer | Internal downstream | Consumes routing function logic |

---

## Testing Strategy

### Routing Logic Test
- Provide combinations of Coping Stage + Emotional Mode to the router.
- Validate matched `situation_category`.
