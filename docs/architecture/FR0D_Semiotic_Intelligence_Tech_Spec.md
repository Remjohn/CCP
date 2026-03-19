# Tech-Spec: FR0D — Semiotic Intelligence Library Initialization (Capability Area 0)

**Created:** 2026-03-18
**Status:** Ready for Development
**Version:** 2.0 (Aligned to CCP Architecture V2)
**Architecture Reference:** CCP_Architecture_Documentation_V2 §2–§8, PRD §Capability Area 0 (FR0D)

---

## Overview

### Problem Statement
Visual content generation traditionally relies on unstructured aesthetic intuition. Without a properly initialized Semiotic Intelligence Library and deterministic decision protocol, visual compositions lack depth, fail to map to intended emotional modes, and result in campaign fatigue.

### Solution
Stage 4 of the Capability Area 0 pipeline. Initializes the `visual_signifier_lexicon` leveraging 4 categorical layers, establishing a dual JSON/SQL split storage. Guided by the Composition Decision Protocol V2 (DEP-PROTO-018) via the Semiotic Composer Agent.

### Scope
**In scope:**
- 4 semiotic categories (Meme Formats, Archetypes, Cultural Symbols, Color/Typography)
- Composition Decision Protocol V2 (DEP-PROTO-018)
- Pre-defined color psychology profiles mapped to mood states
- Dual storage architecture (Baseline JSON + Tribal SQL)
- Semiotic Coverage Test

**Out of scope:**
- Character validation (handled by FR0C)
- Visual asset generation (handled downstream by FR-VIS-01+)

---

## Context for Development

### Architecture Traceability
| DEP-ID | Name | Role | Producing FR | Consuming FRs |
|---|---|---|---|---|
| `visual_signifier_lexicon` | Semiotic Intelligence Library | Visual communication vocabulary (objects, colors, spatial, gestural) | FR0D | FR35, FR36, FR-VIS-01, Composer |
| `semiotic_combination_registry` | Semiotic Combination Registry | 8-week freshness tracking for compositions | FR0D | Composition Decision Protocol V2 |
| `DEP-PROTO-018` | Composition Decision Protocol V2 | 4-question deterministic visual decision algorithm | FR0D (defined) | Semiotic Composer Agent |

### Agent Roster
| Agent | Role |
|---|---|
| **Semiotic Composer Agent** | Composition Decision Protocol V2 formulation, color profile selection, split management |

### Technical Decisions
| Decision | Rationale | ADR-01 Impact |
|---|---|---|
| **Split Storage (JSON/SQL)** | Base definitions are shared (JSON). Coach-specific nuances require queries and tracking (SQL). | Both targets enforce tenant isolation for tribal layers. |

---

## Implementation Plan

### Stage 4: FR0D — Semiotic Intelligence Library Initialization

**Agent:** Semiotic Composer Agent
**Prerequisite:** H11 Tribe Dossier (FR0B) + `character_lexicon` (FR0C)
**ADR-01:** Universal baseline JSON is read-only shared; tribal enrichment layer in Supabase is per-coach isolated.

#### 4 Semiotic Categories
| Category | Layer | Content | Source |
|---|---|---|---|
| **Celebrity/Meme Formats** | Layer 2 | Recurring formats mapped to cognitive mechanisms | H11 Sec B (Humor DNA) |
| **Universal Archetypes** | Layer 1 | Hero, Sage, Shadow, Trickster (Jungian rule anchors) | Baseline + FR0C |
| **Cultural Symbols** | Layer 3 | Tribal insider objects, spatial/gestural references | H11 Sec A + D |
| **Color/Typography** | Layer 4 | 4 color temp profiles mapped to mood states | V2 Spec |

#### Composition Decision Protocol V2 (DEP-PROTO-018) — 4-Question Algorithm
The Semiotic Composer answers four sequential questions for deterministic decisions:
1. **Audience maturity level:** New (L2 primary), Developing (L2+L3), or Loyal (L1 primary)
2. **Content's emotional mode:** T-Tension (L3+Cat 4/5), V-Vulnerability (L1+Cat 1/2), R-Recognition (L2+Cat 2)
3. **CRAL moment served:** e.g., M1 Relevant (L3), M4 Resonant (L1), M5 Surprising (L2 juxtaposition)
4. **8-week freshness check:** Is this combination un-used? If no, rotate through API. 3+ rotations triggers fatigue signal.

#### Color Psychology — 4 Pre-Defined Profiles
Applied at the profile selection layer, not per-piece logic:
- **Escape:** Warm Neutral (Comfort, gentle invitation)
- **Processing:** High Contrast Deep (Depth, serious invitation)
- **Discovery:** Mid-Warmth Energetic (Possibility, active invitation)
- **Status:** Premium Dark (Exclusivity, insider signal)

#### Split Storage Architecture
| Storage | Content | Rationale |
|---|---|---|
| **JSON (read-only)** | Universal baseline definitions | Complete-object load, shared across all coaches. |
| **Supabase SQL (per-coach)** | Tribal enrichment layer + combination tracking | Filtered at query time based on `tribal_resonance`. |

#### Output
- `visual_signifier_lexicon` Supabase table (tribal layer) — populated
- `visual_signifier_lexicon_baseline.json` loaded as read-only reference
- `semiotic_combination_registry` — initialized (empty)
- DEP-PROTO-018 Composition Decision Protocol V2 defined

#### Quality Gate: Semiotic Coverage Test
**Threshold:** Binary PASS/FAIL
**Test:** All 4 semiotic categories must have ≥3 tribe-specific entries with documented deployment mechanisms.
- **Fail example:** Color category has only generic "use warm colors" → FAIL.

#### Receipt Chain Guard
- **INGEST:** H11 + `character_lexicon` received → receipt with counts + versions
- **EMIT:** Tribal enrichment complete → receipt with `entries_per_category`, `coverage_test: PASS/FAIL`, `verdict`

---

## Tasks

- [ ] **Task 1:** Implement Semiotic Composer Agent — populate `visual_signifier_lexicon` across 4 categories, split storage architecture initialization
- [ ] **Task 2:** Implement Composition Decision Protocol V2 (DEP-PROTO-018) — 4-question sequential algorithm with 8-week registry freshness checking

---

## Acceptance Criteria

- [ ] **AC1 (Jungian Anchor Constraint):** Any visual composition request that deploys a Jungian archetype without a corresponding `character_lexicon` anchor is rejected by the Semiotic Composer with `JUNGIAN_ANCHOR_REQUIRED` error.
- [ ] **AC2 (Semiotic Coverage):** A `visual_signifier_lexicon` initialization failing to present at least 3 explicitly documented, tribe-calibrated entries in the Color/Typography layer is rejected by the Semiotic Coverage Test.

---

## Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR0C Character Lexicon | Internal prerequisite | Required for Jungian anchors |
| FR0B Tribe Soul Research | Internal prerequisite | H11 provides format logic |
| FR-VIS-01+ Visual Pipeline | Internal downstream | Consumes combinations |
| Supabase | External service | SQL storage layer |

---

## Testing Strategy

### Composition Algorithm Test
- Simulate various inputs for Audience Maturity, Content Emotional Mode, and CRAL Moments
- Validate correct layer selection mapped deterministically vs the expected baseline mapping
- Validate rejection handling (fatigue rotation on >8 week repeated usages)
