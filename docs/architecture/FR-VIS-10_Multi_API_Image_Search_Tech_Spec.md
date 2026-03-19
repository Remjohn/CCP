# Tech-Spec: FR-VIS-10 — Multi-API Image Search

**Created:** 2026-03-18
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §Visual Intelligence Pipeline, CVE_Documentation_V3 §3
**Skill Implementation:** `skills/visuals/multi_api_image_search.py`, `skills/visuals/SKILL-IMG-001.md` through `SKILL-IMG-009.md`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md` — FR-VIS-10 definition (line 1034)
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CVE_Documentation_V3.md` — §3 Nine Composable Image Search Skills, §2 Image Sourcing Hierarchy, §6 API Integration Details
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CVE_Documentation_V2.md` — §8 RunningHub Integration, §9 Paradoxe Prompt Compilation
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Tribal Imageability and Cultural Half-Life.md` — Search term derivation from TIRS-weighted nouns
- `d:\Work\The Conscious Coaching Factory\docs\architecture\FR50_Sovereign_Image_Rule_Tech_Spec.md` — Reference template

---

## 2. Overview

### Problem Statement
The image sourcing hierarchy (FR-VIS-09) requires a unified interface to query 5 stock image APIs (Unsplash, Pexels, Pixabay, GIPHY, SERPER), 2 AI generation services (RunningHub Realistic, RunningHub Ghibli), and 2 internal registries (Photo Deck, Known Persons). Each API has different authentication, query parameters, response formats, rate limits, and licensing terms. Without a unified abstraction, Aurore would need format-specific API adapters for each source, creating a maintenance burden and inconsistent error handling. Additionally, without composable skill definitions, new image sources cannot be added without modifying core pipeline code.

### Solution
FR-VIS-10 establishes 9 composable image search skills (SKILL-IMG-001 through SKILL-IMG-009), each defined as a full JIT SKILL.md specification with inputs, outputs, quality gates, and error handling. The `multi_api_image_search.py` tool provides the unified Python interface that Aurore invokes — it accepts a standardized search request, dispatches to the appropriate skill(s) based on the sourcing tier, and returns a standardized response. Each skill operates independently and can be updated, replaced, or extended without affecting the pipeline's core logic.

### Scope
**In scope:**
- All 9 SKILL-IMG specifications with inputs, outputs, and quality gates.
- The `multi_api_image_search.py` unified Python tool.
- Per-API rate limiting, authentication, and error handling.
- Environment variable requirements for API keys.
- Result ranking by relevance, quality, and licensing.

**Out of scope:**
- Tier routing decisions (handled by FR-VIS-09).
- PSSL prompt compilation for RunningHub (handled by FR-VIS-03).
- In-App Image Search Panel UI (handled by FR-VIS-11).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-VIS-006` | Known Persons Registry | SOURCE — SKILL-IMG-006 and SKILL-IMG-009 query this registry. |
| `DEP-VIS-007` | Ghibli LoRA Registry | SOURCE — SKILL-IMG-008 queries LoRA model paths. |
| `DEP-VIS-004` | Brand Character Reference Archive | SOURCE — SKILL-IMG-007 uses reference images for identity-preserving generation. |
| `DEP-ENG-041` | Receipt Chain Guard | AUDIT — All API calls, results, and selections are hashed and recorded. |
| `FR-VIS-09` | Image Sourcing Hierarchy | UPSTREAM — Aurore invokes `multi_api_image_search.py` based on tier routing decisions. |
| `FR-VIS-03` | PSSL Prompt Compilation | DOWNSTREAM — SKILL-IMG-007 and SKILL-IMG-008 receive compiled prompts from Paradoxe. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Applied |
|---|---|---|---|
| **Tribal Imageability and Cultural Half-Life** | CCP Research Lab | 2026 | Search queries must use TIRS-weighted tribal nouns rather than generic keywords. The `multi_api_image_search.py` tool converts tribal nouns into multi-word visual descriptors: "the 5am alarm defeat" → `query: "person hand reaching alarm clock dark bedroom morning"`. Generic queries like "morning routine" return corporate stock imagery that scores 0.0 on tribal relevance. The TIRS weight of each noun influences the number of search terms derived: a TIRS 9.0 noun generates 4-5 specific descriptors; a TIRS 6.0 noun generates 2-3 broader descriptors. |

### Technical Decisions
1. **Composable Skill Architecture:** Each API integration is a self-contained SKILL.md file with defined inputs, outputs, and error handling. This allows adding new image sources (e.g., Adobe Stock, Shutterstock) by creating a new SKILL-IMG-XXX specification without modifying the core search tool.
2. **Staggered API Calls:** To avoid rate limiting, Aurore dispatches API calls with 100ms stagger between each API provider. Within a single provider, calls are parallelized up to the provider's rate limit.
3. **Result Normalization:** All API responses are normalized to a common `SearchResult` schema before ranking, regardless of source API. This allows Aurore to compare an Unsplash result against a Pexels result using identical scoring criteria.

---

## 4. Implementation Plan

### Stage 1: Search Request Assembly
*Agent:* `multi_api_image_search.py`
*Inputs:* `search_request` object from Aurore — containing search terms, orientation preference, color filter, resolution minimum, licensing filter, source tier.
*Outputs:* Dispatched API calls to appropriate skills based on tier and search parameters.
*Failure Condition:* Required environment variables missing; tool halts with `MISSING_API_KEY` and lists the missing keys.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Environment Variables Required:**

| Variable | API | Notes |
|---|---|---|
| `UNSPLASH_ACCESS_KEY` | Unsplash | Free tier: 50 req/hour |
| `PEXELS_API_KEY` | Pexels | Free tier: 20,000 req/month |
| `PIXABAY_API_KEY` | Pixabay | Free tier: 100 req/minute |
| `GIPHY_API_KEY` | GIPHY | Free tier: 42 search/hour |
| `SERPER_API_KEY` | SERPER | Paid: 50,000 req/month |

### Stage 2: Parallel Skill Dispatch
*Agent:* `multi_api_image_search.py`
*Inputs:* Search parameters, tier determination.
*Outputs:* Raw API responses from each dispatched skill.
*Failure Condition:* Individual API timeout (10s per skill) — failed skill returns empty result set. Pipeline continues with remaining results. Fallback cascading: primary API fails → next API in tier.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Skill Specifications:**

| Skill ID | Name | Input Parameters | Output | Quality Gate | Timeout |
|---|---|---|---|---|---|
| SKILL-IMG-001 | Unsplash Search | `query`, `orientation` (landscape/portrait/squarish), `color` (hex filter) | Array of `{url, width, height, photographer, license}` | Min resolution 1080px shortest edge | 10s |
| SKILL-IMG-002 | Pexels Search | `query`, `orientation`, `size` (small/medium/large), `color` | Array of `{url, width, height, photographer, license}` | Min resolution 1080px shortest edge | 10s |
| SKILL-IMG-003 | Pixabay Search | `query`, `image_type` (photo/illustration/vector), `orientation`, `category` | Array of `{url, width, height, tags, license}` | Min resolution 1080px shortest edge | 10s |
| SKILL-IMG-004 | GIPHY Search | `query` | Array of `{url, width, height, title, rating}` | Rating G or PG only | 10s |
| SKILL-IMG-005 | SERPER General Image Search | `query`, licensing filter | Array of `{url, source_page, width, height, context_snippet}` | Must pass licensing check | 10s |
| SKILL-IMG-006 | SERPER Known Persons Lookup | `person_name` | Array of `{url, source_page, licensing_status, context}` | Licensed editorial or CC images only | 10s |
| SKILL-IMG-007 | RunningHub Realistic Generation | `prompt` (from Paradoxe), `reference_image_base64`, `strength` (0.85 default) | `{task_id, status_url}` | AGSS ≥ 6.5 (validated by FR-VIS-04) | 600s (10min) |
| SKILL-IMG-008 | RunningHub Ghibli Generation | `prompt` (from Paradoxe), `lora_model_path` (from DEP-VIS-007) | `{task_id, status_url}` | AGSS ≥ 6.5 (validated by FR-VIS-04) | 600s (10min) |
| SKILL-IMG-009 | Photo Deck Query | `coach_id`, `mood`, `format` | Array of `{notion_page_id, file_url, mood_tags, usage_count}` | Coach-uploaded and tagged | 10s |

### Stage 3: Result Normalization & Ranking
*Agent:* `multi_api_image_search.py`
*Inputs:* Raw API responses from all dispatched skills.
*Outputs:* Ranked `SearchResultSet` — normalized results sorted by combined relevance score.
*Failure Condition:* All skills return empty results; tool returns `NO_RESULTS_FOUND` with attempted search terms for debugging.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Normalization Schema:**

```json
{
  "result_id": "SR-001",
  "source_skill": "SKILL-IMG-001",
  "source_api": "unsplash",
  "image_url": "https://images.unsplash.com/photo-abc123",
  "thumbnail_url": "https://images.unsplash.com/photo-abc123?w=400",
  "width_px": 2400,
  "height_px": 3200,
  "aspect_ratio": "3:4",
  "licensing_type": "Unsplash License",
  "licensing_restrictions": "Attribution not required, commercial use permitted",
  "photographer": "Jane Doe",
  "relevance_score": 0.84,
  "resolution_adequate": true,
  "color_match_score": 0.72,
  "tribal_noun_alignment": 0.91,
  "combined_score": 0.82
}
```

**Ranking Weights:**
- `relevance_score` (semantic similarity to search terms): 40%
- `tribal_noun_alignment` (visual match to TIAR noun's concrete referent): 30%
- `resolution_adequate` (≥1080px shortest edge): binary gate (excluded if false)
- `color_match_score` (alignment with PSSL color parameters): 20%
- `licensing_type` (Creative Commons > Editorial > Unsplash License): 10%

---

## 5. Primary Output Schema

### Schema Name: `Multi_API_Search_Response.json`

```json
{
  "search_id": "MAPIS-JP-20260318-001",
  "slide_index": 1,
  "search_terms": ["flat revenue graph stagnant office desk", "business person looking at declining chart"],
  "orientation": "portrait",
  "color_filter": null,
  "resolution_minimum_px": 1080,
  "skills_dispatched": ["SKILL-IMG-001", "SKILL-IMG-002", "SKILL-IMG-003", "SKILL-IMG-005"],
  "skills_succeeded": ["SKILL-IMG-001", "SKILL-IMG-002", "SKILL-IMG-003"],
  "skills_failed": ["SKILL-IMG-005"],
  "skills_failed_reasons": { "SKILL-IMG-005": "SERPER API timeout after 10s" },
  "total_results_raw": 47,
  "total_results_after_filtering": 12,
  "ranked_results": [
    {
      "rank": 1,
      "result_id": "SR-001",
      "source_skill": "SKILL-IMG-001",
      "source_api": "unsplash",
      "image_url": "https://images.unsplash.com/photo-abc123",
      "combined_score": 0.84,
      "selected": true
    },
    {
      "rank": 2,
      "result_id": "SR-007",
      "source_skill": "SKILL-IMG-002",
      "source_api": "pexels",
      "image_url": "https://images.pexels.com/photos/456789",
      "combined_score": 0.79,
      "selected": false
    }
  ],
  "receipt_chain_block": "RCB-MAPIS-20260318-001",
  "timestamp_utc": "2026-03-18T01:38:30Z"
}
```

---

## 6. Backward Compatibility Fallback

If a specific API key environment variable is missing:
1. The tool logs `MISSING_API_KEY: {VARIABLE_NAME}` as a warning.
2. The corresponding skill is skipped — it does not halt the entire search.
3. The remaining available skills are dispatched normally.
4. If ALL API keys are missing, the tool returns `ALL_APIS_UNAVAILABLE` and the slide cascades to Tier 3/4 AI generation.
5. The search response includes `skills_skipped` with the reason for each.

---

## 7. Tasks

- [ ] **Task 1:** Write `multi_api_image_search.py` — the unified Python interface that accepts standardized search requests, dispatches to skills, and returns normalized results.
- [ ] **Task 2:** Write SKILL-IMG-001 (Unsplash Search) as a JIT SKILL.md specification with input schema, output schema, quality gates, rate limit handling, and error responses.
- [ ] **Task 3:** Write SKILL-IMG-002 (Pexels Search) specification.
- [ ] **Task 4:** Write SKILL-IMG-003 (Pixabay Search) specification.
- [ ] **Task 5:** Write SKILL-IMG-004 (GIPHY Search) specification.
- [ ] **Task 6:** Write SKILL-IMG-005 (SERPER General Image Search) specification.
- [ ] **Task 7:** Write SKILL-IMG-006 (SERPER Known Persons Lookup) specification.
- [ ] **Task 8:** Write SKILL-IMG-007 (RunningHub Realistic Generation) specification.
- [ ] **Task 9:** Write SKILL-IMG-008 (RunningHub Ghibli Generation) specification.
- [ ] **Task 10:** Write SKILL-IMG-009 (Photo Deck Query) specification.
- [ ] **Task 11:** Implement the result normalization engine — convert all API-specific response formats to the common `SearchResult` schema.
- [ ] **Task 12:** Implement the ranking engine with configurable weights (relevance 40%, tribal noun alignment 30%, color match 20%, licensing 10%).
- [ ] **Task 13:** Implement staggered API dispatch with 100ms intervals and per-provider rate limit compliance.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Multi-API Dispatch):** Submit a Tier 2 search request. Assert all available stock skills (SKILL-IMG-001 through SKILL-IMG-005) are dispatched. Assert results from all 5 APIs are normalized to the common schema and ranked by combined score. *Failure Example:* Only Unsplash is queried, ignoring 4 other APIs that may have better results.
- [ ] **AC2 (Result Ranking):** Submit a search with two results: Unsplash (relevance 0.9, tribal alignment 0.5, color match 0.4) and Pexels (relevance 0.7, tribal alignment 0.9, color match 0.8). Assert Pexels ranks higher (weighted score: 0.7×0.4 + 0.9×0.3 + 0.8×0.2 = 0.71) over Unsplash (0.9×0.4 + 0.5×0.3 + 0.4×0.2 = 0.59). *Failure Example:* Ranking uses only relevance, and Unsplash's generic "meeting room" image beats Pexels' tribally aligned "person at stagnant desk."
- [ ] **AC3 (Resolution Filter):** Submit results where 15 images pass semantic relevance but 7 have resolution < 1080px shortest edge. Assert those 7 are excluded from the ranked results. *Failure Example:* A 640x480 thumbnail passes through and gets stretched to 1080×1350 in the Canva App, producing a pixelated slide.
- [ ] **AC4 (API Failure Resilience):** Simulate Unsplash and SERPER timeouts. Assert the remaining 3 APIs (Pexels, Pixabay, GIPHY) return results and the pipeline continues. Assert `skills_failed` includes the two timed-out skills with reasons. *Failure Example:* The entire search halts because one API is down.
- [ ] **AC5 (Missing API Key):** Remove `PIXABAY_API_KEY` from environment. Assert SKILL-IMG-003 is skipped with `MISSING_API_KEY` warning and the remaining skills execute normally. *Failure Example:* Tool crashes on initialization because a required environment variable is missing.
- [ ] **AC6 (RunningHub Task Dispatch):** Submit a Tier 3 search request with a compiled prompt. Assert SKILL-IMG-007 creates a RunningHub task, returns `task_id`, and implements exponential backoff polling (5s → 10s → 20s → 40s → 60s max). *Failure Example:* Polling uses fixed 5s intervals, hitting RunningHub rate limits.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| Unsplash API | External | `UNSPLASH_ACCESS_KEY` required. Free tier: 50 req/hour. |
| Pexels API | External | `PEXELS_API_KEY` required. Free tier: 20,000 req/month. |
| Pixabay API | External | `PIXABAY_API_KEY` required. Free tier: 100 req/minute. |
| GIPHY API | External | `GIPHY_API_KEY` required. Free tier: 42 search/hour. |
| SERPER API | External | `SERPER_API_KEY` required. Paid: 50,000 req/month. |
| RunningHub API | External | Task creation, polling, output retrieval. 10-minute timeout per task. |
| Notion API | External | Photo Deck and Known Persons Registry queries. |
| DEP-VIS-004 (Brand Character Reference Archive) | Internal | Reference images for SKILL-IMG-007. |
| DEP-VIS-006 (Known Persons Registry) | Internal | Named person images for SKILL-IMG-006 and SKILL-IMG-009. |
| DEP-VIS-007 (Ghibli LoRA Registry) | Internal | LoRA model paths for SKILL-IMG-008. |
| DEP-ENG-041 (Receipt Chain Guard) | Internal | Audit trail for all API calls and selections. |
| FR-VIS-09 (Image Sourcing Hierarchy) | Internal | UPSTREAM — determines which skills to dispatch. |

---

## 10. Testing Strategy

### Unit Tests
- **Normalization:** Provide raw responses from each of the 5 stock APIs. Assert all normalize to the common `SearchResult` schema with identical fields.
- **Ranking Weights:** Provide 5 normalized results with pre-computed score components. Assert the ranking engine produces the correct sorted order using the configured weights.
- **Rate Limit Stagger:** Assert API dispatch timestamps show ≥100ms intervals between different providers.

### Integration Tests
- **Live API Smoke Test:** Execute a search for "person sitting at desk with laptop" across all available APIs. Assert ≥1 result from each API, all normalized correctly, all with resolution ≥1080px.
- **RunningHub Round Trip:** Submit a prompt to SKILL-IMG-007, poll for completion, retrieve the output URL. Assert the full round trip completes within 10 minutes.

### Safety Tests (ADR-01 Quarantine Security)
- **Query Injection:** Submit `query: "alarm clock; curl evil.com"`. Assert the search APIs receive the full string as a single query parameter, not as multiple commands.
- **API Key Exposure:** Assert no API key appears in any log output, error message, or Receipt Chain record since they are handled strictly via environment variables.
