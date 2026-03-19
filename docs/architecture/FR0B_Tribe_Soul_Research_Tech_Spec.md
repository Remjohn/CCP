# Tech-Spec: FR0B — Tribe Soul Research (Capability Area 0)

**Created:** 2026-03-18
**Status:** Ready for Development
**Version:** 2.0 (Aligned to CCP Architecture V2)
**Architecture Reference:** CCP_Architecture_Documentation_V2 §2–§8, PRD §Capability Area 0 (FR0B)

---

## Overview

### Problem Statement
Downstream production depends on an authentic understanding of the coach's target audience. Without FR0B, content generation uses generic tribal language instead of a verified L3 verbatim corpus, leading to low resonance and ineffective messaging.

### Solution
Stage 2 of the Capability Area 0 pipeline. A comprehensive Tribe Soul Research operation producing the H11 Tribe Dossier — a 25-30 page verbatim corpus. The V2 architecture splits this research into 4 specialist skills mapping lexicon, humor, emotions, and social dynamics.

### Scope
**In scope:**
- 4-Skill Tribe Research Architecture
- `tribe-lexicon-research`, `tribe-humor-research`, `tribe-emotional-research`, `tribe-social-research`
- Cross-Dimensional Convergence Analysis synthesis step
- H11 Tribe Dossier output
- Volume Verification Test & Verbatim Ratio Test

**Out of scope:**
- Downstream character lexicon population (handled by FR0C)
- Downstream semiotic intelligence population (handled by FR0D)

---

## Context for Development

### Architecture Traceability
| DEP-ID | Name | Role | Producing FR | Consuming FRs |
|---|---|---|---|---|
| `H11` | Tribe Dossier | 25-30 page verbatim corpus — tribe language, humor, emotions, social dynamics | FR0B | FR0C, FR0D, FR6, CRAL (FR14) |
| `DEP-ENG-050` | Business Intelligence Summary | Seed for all downstream extraction (audience targeting) | FR0A | FR0B |
| `DEP-ENG-006` | Tribe Profile (Context Premises) | 12-dimension psychological map | FR6 | FR10, FR11, FR53 |

### Agent Roster
| Agent | Role |
|---|---|
| **4 Tribe Research Specialists** | `tribe-lexicon-research`, `tribe-humor-research`, `tribe-emotional-research`, `tribe-social-research` |
| **Guardian Agent** | Cross-dimensional convergence analysis synthesis |

### Technical Decisions
| Decision | Rationale | ADR-01 Impact |
|---|---|---|
| **4-Skill Tribe Research split** | Different research dimensions require different platforms, quality metrics, and analytical approaches. Monolithic execution produces quality averaging. | Each skill writes to isolated H11 section per coach. |

---

## Implementation Plan

### Stage 2: FR0B — Tribe Soul Research (4-Skill Architecture)

**Agent:** Guardian Agent orchestrates 4 specialist skills
**Prerequisite:** DEP-ENG-050 (FR0A output — audience parameters for research targeting)
**ADR-01:** Research outputs stored in coach-specific H11 sections. No cross-coach research sharing.

#### Research Planning Sub-Stage
Before executing skills, the Guardian Agent generates a 280-320 word Research Execution Plan specifying:
- Exact platform targets for this coach's audience (e.g., "r/solopreneurs, r/getmotivated, Skool community XYZ")
- Audience segment parameters derived from DEP-ENG-050
- Cultural context that restricts or directs the research (e.g., English-speaking, US-centric, millennial+Gen-Z)

#### 4 Specialist Skills

**SKILL: `tribe-lexicon-research`**
| Field | Specification |
|---|---|
| **Primary function** | Cultural artifact archiving — linguistic infrastructure of the tribe |
| **Source platforms** | Reddit (subreddit comment threads), Discord (server exports), closed Facebook groups, industry forums |
| **Volume quotas** | 100-150 verbatim slang examples with usage context; 75-100 hero/enemy posts with direct quotes; 5-7 inside jokes with reference examples |
| **Quality gate** | Verbatim ratio ≥70% (direct quotes, not paraphrases). Slang entries must include context of misuse correction by tribe members. |
| **CRAL connection** | Outputs feed `character_lexicon` Category 3 and Category 5 identification |
| **DEP output** | H11 Section A — Cultural Artifacts |
| **Academic grounding** | Computational stylometry (Koppel et al., 2009) |

**SKILL: `tribe-humor-research`**
| Field | Specification |
|---|---|
| **Primary function** | Humor DNA profiling — comedic signature and taboo mapping |
| **Source platforms** | Top-voted humor/meme content from tribe subreddits, Twitter/X humor threads, downvoted content analysis |
| **Volume quotas** | 50-100 top-voted humor posts with style classification; minimum 3 verbatim examples per style; 2-3 taboo entries |
| **Quality gate** | Style coverage: ≥3 distinct humor styles identified. Taboo list: ≥2 entries with community reaction evidence. |
| **Semiotic connection** | Outputs feed `visual_signifier_lexicon` Layer 2 (Cultural Meme Formats) |
| **DEP output** | H11 Section B — Humor DNA Profile |
| **Academic grounding** | Benign Violation Theory (McGraw & Warren, 2010) |

**SKILL: `tribe-emotional-research`**
| Field | Specification |
|---|---|
| **Primary function** | Emotional landscape mapping — L3 fear and aspiration corpus |
| **Source platforms** | Anonymous forums (Mind After Midnight methodology: 11pm-4am posting), support community threads, rant/vent tagged posts |
| **Volume quotas** | 5-7 verbatim aspiration quotes (L2 min, L3 pref); 5-7 verbatim anxiety quotes (L3 required); 3 pos + 3 neg high-arousal trigger examples |
| **Quality gate** | L3 minimum ratio: ≥40% of collected emotional posts must score above LIWC-22 70th percentile authenticity threshold. |
| **CRAL connection** | Same L3 verification methodology as CRAL M4 RESONANT (Human Evidence Bias gate) |
| **DEP output** | H11 Section C — Emotional Landscape. Seeds DEP-ENG-006 `emotional_triggers` and `fears` dimensions. |
| **Academic grounding** | LIWC-22 (Pennebaker et al., 2022), Mind After Midnight (Perlis et al., 2016) |

**SKILL: `tribe-social-research`**
| Field | Specification |
|---|---|
| **Primary function** | Social dynamics investigation — hierarchy, status, and unwritten rules |
| **Source platforms** | Newcomer correction threads, moderation action patterns, status-signaling posts, membership milestone celebrations |
| **Volume quotas** | 3-5 unwritten rules with evidence; 5+ in-group signals with context; 3+ boundary enforcement examples |
| **Quality gate** | Specificity test: each unwritten rule must be specific enough that violating it would produce an observable community reaction. Generic rules FAIL. |
| **DEP output** | H11 Section D — Social Architecture. Seeds DEP-ENG-006 `enemies` and `suspicions` dimensions. |
| **Academic grounding** | Social Identity Theory (Tajfel & Turner, 1979), Cialdini's Social Proof (2001) |

#### Guardian Agent Synthesis Step
After all 4 skills complete, the Guardian Agent runs a cross-dimensional convergence analysis. A figure who appears as a cultural hero in lexicon research, is referenced in protective humor, AND triggers emotional rant posts is a Category 1 Aspirational Hero with multi-dimensional tribal significance. This convergence intelligence is invisible to any individual skill and is architecturally more valuable.

#### Output
**Primary:** H11 Tribe Dossier (25-30 page verbatim corpus, 4 sections)
- Section A: Cultural Artifacts
- Section B: Humor DNA Profile
- Section C: Emotional Landscape
- Section D: Social Architecture
- Section E: Cross-Dimensional Convergence Analysis (synthesis output)

#### Quality Gates
**Volume Verification Test:** Combined H11 corpus ≥25 pages. Binary PASS/FAIL.
- **Fail example:** 4 skills produce 6 pages each = 24 pages → FAIL (below minimum)

**Verbatim Ratio Test:** ≥70% of all text in H11 must be direct quotes from real audience sources — not paraphrased summaries.
- **Fail example:** H11 contains "tribe members typically express frustration about work-life balance" → FAIL. Must contain: "honestly I'm so tired of pretending I have my shit together when my business is literally held together by duct tape and caffeine" [r/solopreneurs, u/exhausted_founder, 2am post]

#### Failure Conditions
- Volume fails → Guardian Agent identifies which skill produced insufficient volume. That skill re-executes with expanded platform list.
- Verbatim ratio fails → Guardian Agent identifies which sections contain analysis instead of quotes. Researcher re-executes with explicit "archive, don't analyze" instruction.

#### Receipt Chain Guard
- **INGEST:** Research plan generated → receipt with `platform_targets[]`, `audience_segment`, `dep_eng_050_version`
- **Per-skill EMIT:** Each skill writes receipt with `section`, `verbatim_ratio`, `volume_pages`, `source_count`
- **Synthesis EMIT:** Final H11 receipt with `total_pages`, `aggregate_verbatim_ratio`, `convergence_events_count`, `verdict`

---

## Tasks

- [ ] **Task 1:** Build `tribe-lexicon-research` SKILL.md — platform-specific scraping, verbatim archiving protocol, volume enforcement, CRAL Category 3/5 output connection
- [ ] **Task 2:** Build `tribe-humor-research` SKILL.md — humor flair filtering, style classification taxonomy, taboo detection with reaction evidence, semiotic connection
- [ ] **Task 3:** Build `tribe-emotional-research` SKILL.md — Mind After Midnight post identification, LIWC-22 authenticity scoring integration, L3 depth verification, emotional landscape mapping
- [ ] **Task 4:** Build `tribe-social-research` SKILL.md — newcomer correction analysis, status hierarchy extraction, unwritten rule documentation with specificity test
- [ ] **Task 5:** Implement Guardian Agent synthesis step — cross-dimensional convergence analysis across 4 research outputs + Volume/Verbatim quality gate enforcement

---

## Acceptance Criteria

- [ ] **AC1 (Verbatim Ratio):** An H11 Tribe Dossier with 65% verbatim ratio (below 70% threshold) receives a FAILED verdict from the Guardian Agent. An H11 with exactly 70% receives AUTHENTICATED. Test: submit corpus with controlled ratio → verify verdict boundary.
- [ ] **AC2 (Sequential Execution):** Attempting to execute FR0C before FR0B completes returns `PREREQUISITE_PENDING: FR0B` from the Guardian Agent — the stage is not queued, it is blocked. Test: trigger FR0C with FR0B incomplete → verify hard block.
- [ ] **AC3 (PROVISIONAL Degradation Flag):** A PROVISIONAL verdict on FR0B (e.g., volume passes but verbatim ratio = 68%) produces a Genesis Clearance Certificate with `provisional_gaps: ["fr0b: verbatim_ratio_68_below_70_threshold"]` and all downstream content generated using FR0B outputs carries a `degradation_flag: true`. Test: force PROVISIONAL → verify flag propagation.

---

## Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR0A Business Intelligence | Internal prerequisite | DEP-ENG-050 restricts/directs search targets |
| FR14 CRAL Research Subsystem | Internal downstream | Consumes H11 |
| FR6 Tribe Profile | Internal downstream | Consumes H11 |
| LIWC-22 | External library | Authenticity scoring for `tribe-emotional-research` |
| Exa / Gemini / Perplexity | External services | Deep research platforms |

---

## Testing Strategy

### Quality Gate Boundary Test
- Test at the exact threshold boundary:
  - Volume: H11 at 24 pages (FAIL) vs. 25 pages (PASS)
  - Verbatim ratio: 69% (FAIL) vs. 70% (PASS)
- Validate: Each gate produces the correct verdict at the boundary

### Performance Test
- FR0B 4-skill execution: <4 hours autonomous execution time (platform scraping + synthesis)
