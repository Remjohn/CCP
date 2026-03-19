# Tech-Spec: FR-VIS-02 — TIAR Integration

**Created:** 2026-03-18
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §Visual Intelligence Pipeline, CVE_Documentation_V2 §4, §10.5
**Skill Implementation:** `skills/visuals/tiar_adapter.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md` — FR-VIS-02 definition (line 1018)
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CVE_Documentation_V2.md` — §4 Tribal Imagen Activation Registry Architecture, §10.5 TIAR Audit Protocol
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\CVE_Documentation_V3.md` — §3 Abel's 9-step VCB process (TIAR query step), §8 Updated noun lifecycle
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Tribal Imageability and Cultural Half-Life.md` — TIRS rating scale, Shannon entropy decay tracking, 4-stage noun lifecycle, cultural half-life measurement
- `d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers\Carousel Physiological State Architecture Research.md` — Concrete noun potency in hook slides, desire compounding through tribal vocabulary
- `d:\Work\The Conscious Coaching Factory\docs\architecture\FR50_Sovereign_Image_Rule_Tech_Spec.md` — Reference template for structure and depth

---

## 2. Overview

### Problem Statement
The Conscious Coaching Platform's visual content derives its hook potency from concrete tribal nouns — words that vibrate with subcultural meaning for the coach's specific audience. These nouns have a measurable lifecycle: they emerge, peak, plateau, and decay as the audience habituates. A noun like "alignment" may score 8.7 on the TIRS (Tribal Imageability Rating Scale) in Week 1 but decay to 4.2 by Week 12 through overexposure. If the visual pipeline uses expired nouns in text overlays or image search queries, the resulting content looks superficially correct but fails to trigger the identity-recognition flash that drives engagement. The pipeline needs a deterministic mechanism to inject only active nouns and block expired ones — at both the script generation stage (where hook text is assembled) and the visual composition stage (where Abel selects text for image overlays).

### Solution
FR-VIS-02 establishes the `tiar-adapter` — a dual-firing integration layer that queries the Tribal Imagen Activation Registry (DEP-VIS-001) at two pipeline points:
1. **Upstream** — During Script Generation Skills, before hook text assembly. The adapter injects active tribal nouns as required vocabulary and blocks expired nouns from appearing in any script text that will flow into visual compositions.
2. **Downstream** — During Abel's VCB generation (FR-VIS-01), before visual text finalization. The adapter re-validates that all concrete nouns in text slides meet minimum TIRS thresholds and flags any nouns that have decayed between script generation and VCB finalization.

The TIAR tracks noun lifecycle across 4 deterministic stages derived from Shannon entropy measurements: `in_distribution` (active), `tribal_potential` (emerging), `decay_approaching` (overused, warn), `expired` (blocked). Every noun's decay status is logged in the Visual Production Output (VPO) record for full audit traceability.

### Scope
**In scope:**
- The `tiar-adapter` dual-point firing logic.
- TIAR query interface to DEP-VIS-001.
- Noun lifecycle enforcement: blocking expired nouns, warning on decay-approaching nouns.
- VPO audit logging of per-noun decay status.
- Integration with DEP-ENG-007 (Tribe Intelligence) and DEP-ENG-023 (Cultural Memory Map) as TIAR data sources.

**Out of scope:**
- The TIAR registry itself (maintained as DEP-VIS-001; this spec covers the adapter that queries it).
- Noun lifecycle promotion/demotion logic (managed by the Tribe Intelligence pipeline).
- Visual style selection (handled by FR-VIS-08).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-VIS-001` | Tribal Imagen Activation Registry (TIAR) | SOURCE — The Notion database storing all tribal nouns with their TIRS scores, decay stages, and lifecycle timestamps. |
| `DEP-ENG-007` | Tribe Intelligence | UPSTREAM DATA SOURCE — Provides the base tribal vocabulary from audience analysis. |
| `DEP-ENG-023` | Cultural Memory Map | UPSTREAM DATA SOURCE — Provides cultural memory context that informs noun decay tracking. |
| `DEP-ENG-011` | Finalized Content Output | UPSTREAM CONSUMER — Script Generation Skills receive the active noun injection before assembling hooks. |
| `DEP-VIS-005` | Visual Composition Brief Schema | DOWNSTREAM CONSUMER — VCB text slides are validated against TIAR before finalization. |
| `DEP-ENG-041` | Receipt Chain Guard | AUDIT — TIAR query results and noun decay statuses are hashed and recorded. |
| `tiar-adapter` | TIAR Adapter | TOOL — The dual-firing integration layer. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Applied |
|---|---|---|---|
| **Tribal Imageability and Cultural Half-Life** | CCP Research Lab | 2026 | The Tribal Imageability Rating Scale (TIRS) measures three dimensions of noun potency: (1) **Image Evocation Speed** — how quickly the noun conjures a concrete mental image in the target tribe (measured via reaction time in lexical decision tasks); (2) **Identity Resonance** — whether the noun triggers self-referential processing (measured via P300 ERP amplitude); (3) **Cultural Specificity** — how sharply the noun discriminates the target tribe from adjacent tribes (measured via Shannon entropy of usage distribution). A TIRS score ≥7.0 indicates a noun is "in distribution" — it reliably triggers identity recognition. Between 5.0-6.9, the noun is "tribal potential" or "decay approaching." Below 5.0, the noun is "expired" and actively harms engagement because the audience recognizes it as a stale marketing term rather than a living tribal marker. |
| **Carousel Physiological State Architecture** | CCP Research Lab | 2026 | Hook slides in carousels rely on concrete tribal nouns to generate the initial GSR arousal spike that commits the user to swiping. The research measured that high-TIRS nouns (≥7.5) in hook text produce a 340% higher initial GSR spike compared to generic nouns (e.g., "success" vs. "the 5am alarm defeat"). The desire compounding mechanism across carousel slides depends on the first-slide noun potency — if the hook noun is expired, the arousal spike fails, and no amount of brilliant downstream slides can recover the engagement arc. |

### Technical Decisions
1. **Dual-Point Firing:** The adapter fires twice because the pipeline has a temporal gap between script generation and VCB finalization. A noun that was `in_distribution` during script generation may transition to `decay_approaching` by the time Abel processes the VCB (if the weekly TIAR refresh cycle runs between the two stages). The second firing point catches these mid-pipeline decay transitions.
2. **Block Expired, Warn Decay-Approaching:** Expired nouns are hard-blocked — they cannot appear in any visual text. Decay-approaching nouns are permitted but flagged with a warning — the operator can see that a noun is approaching expiration and may choose to adjust. This prevents the adapter from being overly restrictive while still providing visibility into noun health.
3. **Minimum 3 Concrete TIAR Nouns Per Text Slide:** Gate C-09 (FR-VIS-01) enforces that every text slide contains at least 3 concrete TIAR nouns. The TIAR adapter ensures these nouns are `in_distribution` or `tribal_potential` — not just present but active.

---

## 4. Implementation Plan

### Stage 1: Upstream TIAR Injection (Script Generation)
*Agent:* `tiar-adapter` (upstream firing point)
*Inputs:* `coach_id`, `tribe_id` (from DEP-ENG-007), active noun query to DEP-VIS-001.
*Outputs:* `active_noun_vocabulary` (array of in_distribution and tribal_potential nouns), `blocked_noun_list` (array of expired nouns).
*Failure Condition:* TIAR Notion API timeout; adapter returns cached vocabulary from last successful query with `TIAR_CACHE_STALE` warning. Pipeline continues with stale data — never halts for a TIAR failure.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. Script Generation Skills request the TIAR adapter before assembling hook text.
2. The adapter queries DEP-VIS-001 (Notion database) with filters: `coach_id = {coach_id} AND tribe_id = {tribe_id}`.
3. Retrieves all nouns and their current lifecycle data: `noun`, `tirs_score`, `decay_stage`, `last_measured_date`, `usage_count_30d`, `shannon_entropy`.
4. Partitions the result set:
   - `in_distribution` (TIRS ≥ 7.0, `decay_stage: "in_distribution"`): added to `active_noun_vocabulary`.
   - `tribal_potential` (TIRS 5.0-6.9, `decay_stage: "tribal_potential"`): added to `active_noun_vocabulary` with `is_emerging: true` flag.
   - `decay_approaching` (TIRS 5.0-6.9, `decay_stage: "decay_approaching"`): added to `active_noun_vocabulary` with `decay_warning: true` flag.
   - `expired` (TIRS < 5.0, `decay_stage: "expired"`): added to `blocked_noun_list`.
5. Injects the `active_noun_vocabulary` into the Script Generation Skills context as required vocabulary. Hook text assembly must draw from this vocabulary.
6. Injects the `blocked_noun_list` as a prohibition constraint. Any hook text containing a blocked noun is rejected for rewording.

### Stage 2: Downstream TIAR Re-Validation (VCB Finalization)
*Agent:* `tiar-adapter` (downstream firing point)
*Inputs:* Abel's draft VCB (DEP-VIS-005), `tiar_query_result` from a fresh query to DEP-VIS-001.
*Outputs:* Per-slide `noun_decay_audit` array, `TIAR_VALID` (continue) or `TIAR_DECAY_DETECTED` (return to Abel with specific noun violations).
*Failure Condition:* TIAR Notion API timeout at the downstream point; adapter uses the upstream query result (Stage 1 cache) instead of blocking the pipeline. `TIAR_STALE_DOWNSTREAM` warning logged.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. After Abel completes the VCB draft, the adapter fires a second TIAR query to get the freshest noun lifecycle data.
2. For each text slide in the VCB, extracts all concrete nouns from the `slide_text`, `hook_text`, and `overlay_text` fields.
3. Cross-references each extracted noun against the fresh TIAR query result.
4. For each noun found in the TIAR:
   - If `decay_stage: "expired"` (noun decayed between script generation and VCB finalization): flags `NOUN_EXPIRED_SINCE_SCRIPT` with the noun, its current TIRS score, and the slide index.
   - If `decay_stage: "decay_approaching"`: logs `NOUN_DECAY_WARNING` in the audit but permits the noun.
   - If `decay_stage: "in_distribution"` or `"tribal_potential"`: logs `NOUN_ACTIVE` in the audit.
5. For each noun NOT found in the TIAR: logs `NOUN_NOT_IN_REGISTRY` — this is informational, not a violation (generic nouns are permitted alongside TIAR nouns).
6. Assembles the `noun_decay_audit` array for the VPO record.
7. If any `NOUN_EXPIRED_SINCE_SCRIPT` violations are found: returns the VCB to Abel with the violation details and a list of active replacement nouns from the `in_distribution` pool.
8. If no violations: emits `TIAR_VALID` and the VCB proceeds to Gate C-09.

### Stage 3: VPO Audit Logging
*Agent:* `tiar-adapter`
*Inputs:* `noun_decay_audit` array from Stage 2, `content_output_id`.
*Outputs:* VPO record enriched with per-noun TIAR decay status.
*Failure Condition:* VPO write failure; audit data is queued for retry. Pipeline continues — audit logging failure is non-blocking.
*Receipt Write:* `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041).

**Steps:**
1. The `noun_decay_audit` array is attached to the Visual Production Output (VPO) record for the composition.
2. Each entry in the audit contains: `noun`, `tirs_score`, `decay_stage`, `slide_index`, `position_in_text` (character offset), `last_measured_date`.
3. The audit enables longitudinal analysis: operators can track which nouns are decaying across multiple compositions and proactively refresh the TIAR vocabulary.
4. The Receipt Chain Guard hashes the complete audit payload and appends to the receipt chain.

---

## 5. Primary Output Schema

### Schema Name: `TIAR_Injection_Result.json`

```json
{
  "injection_id": "TIAR-INJ-JP-20260318-001",
  "coach_id": "coach_jean_pierre",
  "tribe_id": "tribe_conscious_leaders",
  "query_timestamp_utc": "2026-03-18T01:35:00Z",
  "active_noun_vocabulary": [
    { "noun": "the 5am alarm defeat", "tirs_score": 8.7, "decay_stage": "in_distribution", "is_emerging": false, "decay_warning": false },
    { "noun": "Sunday night dread spiral", "tirs_score": 9.1, "decay_stage": "in_distribution", "is_emerging": false, "decay_warning": false },
    { "noun": "client ghost", "tirs_score": 7.4, "decay_stage": "in_distribution", "is_emerging": false, "decay_warning": false },
    { "noun": "revenue plateau confession", "tirs_score": 6.8, "decay_stage": "decay_approaching", "is_emerging": false, "decay_warning": true },
    { "noun": "launch anxiety loop", "tirs_score": 5.9, "decay_stage": "tribal_potential", "is_emerging": true, "decay_warning": false }
  ],
  "blocked_noun_list": [
    { "noun": "alignment", "tirs_score": 3.2, "decay_stage": "expired", "expired_since": "2026-03-04" },
    { "noun": "hustle culture", "tirs_score": 4.1, "decay_stage": "expired", "expired_since": "2026-03-11" }
  ],
  "vocabulary_size": { "active": 5, "blocked": 2 },
  "cache_status": "FRESH",
  "receipt_chain_block": "RCB-TIAR-INJ-20260318-001"
}
```

### Schema Name: `Noun_Decay_Audit.json` (per VPO)

```json
{
  "audit_id": "TIAR-AUD-JP-20260318-001",
  "content_output_id": "CO-JP-20260318-012-CAROUSEL",
  "slide_audits": [
    {
      "slide_index": 0,
      "nouns_found": [
        { "noun": "the 5am alarm defeat", "tirs_score": 8.7, "decay_stage": "in_distribution", "position_in_text": 12, "last_measured_date": "2026-03-17" },
        { "noun": "Sunday night dread spiral", "tirs_score": 9.1, "decay_stage": "in_distribution", "position_in_text": 47, "last_measured_date": "2026-03-17" },
        { "noun": "client ghost", "tirs_score": 7.4, "decay_stage": "in_distribution", "position_in_text": 89, "last_measured_date": "2026-03-17" }
      ],
      "nouns_not_in_registry": ["coaching"],
      "violations": []
    },
    {
      "slide_index": 3,
      "nouns_found": [
        { "noun": "revenue plateau confession", "tirs_score": 6.8, "decay_stage": "decay_approaching", "position_in_text": 5, "last_measured_date": "2026-03-17" }
      ],
      "nouns_not_in_registry": ["business", "growth"],
      "violations": [],
      "warnings": ["NOUN_DECAY_WARNING: 'revenue plateau confession' is approaching decay (TIRS 6.8, stage: decay_approaching)"]
    }
  ],
  "total_tiar_nouns": 4,
  "total_active": 3,
  "total_decay_warning": 1,
  "total_expired": 0,
  "receipt_chain_block": "RCB-TIAR-AUD-20260318-001"
}
```

---

## 6. Backward Compatibility Fallback

If the Tribal Imagen Activation Registry (DEP-VIS-001) has not been initialized for a coach (new coach onboarding, TIAR data not yet populated):
1. The upstream adapter returns an empty `active_noun_vocabulary` and empty `blocked_noun_list`.
2. Script Generation Skills proceed without TIAR vocabulary constraints — all nouns are permitted.
3. The downstream adapter skips noun validation and logs `TIAR_NOT_INITIALIZED` in the VPO audit.
4. Gate C-09's "minimum 3 concrete TIAR nouns" check is relaxed to "minimum 3 concrete nouns" (any concrete noun, not requiring TIAR registry presence) when the `TIAR_NOT_INITIALIZED` flag is set.
5. The first 4 weeks of a coach's content production are flagged as `TIAR_CALIBRATION_PERIOD` in the Receipt Chain.

---

## 7. Tasks

- [ ] **Task 1:** Write `tiar_adapter.py` — the dual-firing adapter that queries DEP-VIS-001 at both pipeline points (upstream script generation, downstream VCB finalization).
- [ ] **Task 2:** Implement the TIAR Notion API query interface — filter by `coach_id` and `tribe_id`, retrieve noun lifecycle data (`noun`, `tirs_score`, `decay_stage`, `last_measured_date`, `usage_count_30d`, `shannon_entropy`).
- [ ] **Task 3:** Implement the upstream noun injection logic — partition query results into `active_noun_vocabulary` and `blocked_noun_list`, inject into Script Generation Skills context.
- [ ] **Task 4:** Implement the downstream re-validation logic — extract concrete nouns from VCB text slides, cross-reference against fresh TIAR query, detect mid-pipeline decay transitions.
- [ ] **Task 5:** Build the `noun_decay_audit` assembly for VPO records — per-noun, per-slide decay status logging with character-offset position tracking.
- [ ] **Task 6:** Implement the caching mechanism — if the Notion API is unavailable at either firing point, use the cached result from the last successful query. Log `TIAR_CACHE_STALE` or `TIAR_STALE_DOWNSTREAM` warnings.
- [ ] **Task 7:** Implement the `TIAR_NOT_INITIALIZED` fallback for new coaches — empty vocabulary, relaxed Gate C-09 constraints, `TIAR_CALIBRATION_PERIOD` flag.
- [ ] **Task 8:** Integrate with Receipt Chain Guard (DEP-ENG-041) — hash TIAR injection results and noun decay audits at every stage.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Upstream Injection — Active Nouns):** Query TIAR for a coach with 10 active nouns (TIRS ≥ 7.0) and 3 expired nouns. Assert the adapter returns all 10 in `active_noun_vocabulary` and all 3 in `blocked_noun_list`. Assert Script Generation Skills receive the vocabulary constraint. *Failure Example:* The adapter returns all 13 nouns without filtering, and an expired noun ("alignment", TIRS 3.2) appears in a hook text.
- [ ] **AC2 (Upstream Injection — Expired Noun Block):** Attempt to generate hook text containing the expired noun "hustle culture" (TIRS 4.1, `expired`). Assert the Script Generation Skills reject the text and request rewording with active alternatives. *Failure Example:* The expired noun passes through, is included in the hook, and the carousel's opening slide uses a dead marketing term that the audience has habituated to.
- [ ] **AC3 (Downstream Re-Validation — Mid-Pipeline Decay):** Between script generation and VCB finalization, update the TIAR to mark "client ghost" as `expired` (TIRS dropped from 7.4 to 4.8). Assert the downstream adapter detects the decay transition and returns the VCB to Abel with `NOUN_EXPIRED_SINCE_SCRIPT` and a list of active replacement nouns. *Failure Example:* Abel finalizes the VCB with a newly expired noun, and the visual text uses a term that was active yesterday but dead today.
- [ ] **AC4 (Decay Warning — Non-Blocking):** Include the noun "revenue plateau confession" (TIRS 6.8, `decay_approaching`) in a text slide. Assert the adapter permits the noun but logs `NOUN_DECAY_WARNING` in the VPO audit. Assert no VCB rejection. *Failure Example:* The adapter blocks a decay-approaching noun, unnecessarily restricting Abel's text options and forcing a suboptimal replacement.
- [ ] **AC5 (VPO Audit Completeness):** Generate a 7-slide carousel with TIAR nouns in slides 0, 2, 3, and 5. Assert the VPO `noun_decay_audit` contains entries for all 4 text slides with complete per-noun data: `noun`, `tirs_score`, `decay_stage`, `position_in_text`, `last_measured_date`. Assert slides 1, 4, and 6 (image-only) have empty `nouns_found` arrays. *Failure Example:* The VPO audit is missing slide 3's entries because the adapter only tracks the first and last text slides.
- [ ] **AC6 (API Timeout Resilience):** Simulate a TIAR Notion API timeout at the upstream firing point. Assert the adapter returns the cached vocabulary from the last successful query with `TIAR_CACHE_STALE` status. Assert the pipeline continues without halting. *Failure Example:* The pipeline crashes on Notion timeout, blocking the entire weekly CCF run because a single API call failed.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| DEP-VIS-001 (TIAR) | Internal | SOURCE — The Notion database storing tribal noun lifecycle data. |
| DEP-ENG-007 (Tribe Intelligence) | Internal | UPSTREAM — Provides base tribal vocabulary that populates the TIAR. |
| DEP-ENG-023 (Cultural Memory Map) | Internal | UPSTREAM — Provides cultural memory context for decay tracking. |
| DEP-ENG-011 (Finalized Content Output) | Internal | UPSTREAM — Script Generation Skills consume TIAR vocabulary. |
| DEP-VIS-005 (VCB Schema) | Internal | DOWNSTREAM — VCB text slides are validated against TIAR. |
| DEP-ENG-041 (Receipt Chain Guard) | Internal | AUDIT — TIAR injection and audit results are hashed and recorded. |
| FR-VIS-01 (VCB Generation) | Internal | DOWNSTREAM — Abel's VCB generation depends on TIAR vocabulary for text slides. Gate C-09 enforces minimum 3 TIAR nouns per text slide. |
| Notion API | External | TIAR is stored as a Notion database; queries use `POST /databases/{id}/query`. |

---

## 10. Testing Strategy

### Unit Tests
- **Noun Partitioning:** Provide 20 mock nouns with varying TIRS scores (3.0 to 9.5) and decay stages. Assert the partitioner correctly sorts them into `in_distribution`, `tribal_potential`, `decay_approaching`, `expired` buckets with no misclassification.
- **Decay Warning Flag:** Provide a noun with TIRS 6.2 and `decay_stage: "decay_approaching"`. Assert the `decay_warning: true` flag is set. Provide a noun with TIRS 6.2 and `decay_stage: "tribal_potential"`. Assert `is_emerging: true` is set and `decay_warning` is false.
- **Noun Extraction from VCB Text:** Provide a VCB text slide with "The 5am alarm defeat is the first sign of the Sunday night dread spiral." Assert the extractor identifies "the 5am alarm defeat" and "Sunday night dread spiral" as TIAR nouns (multi-word phrases, not individual words).

### Integration Tests
- **Dual-Fire Sequence:** Run the full pipeline from script generation through VCB finalization. Assert the TIAR adapter fires at both points. Assert the upstream injection constrains the script's vocabulary. Assert the downstream re-validation audits the VCB's text slides.
- **Cache Failover:** Block the TIAR Notion API (return 503). Run the pipeline. Assert the adapter uses cached data at both firing points and the pipeline completes successfully with `TIAR_CACHE_STALE` logged at each point.

### Safety Tests (ADR-01 Quarantine Security)
- **Noun Injection Attack:** Inject `noun: "alignment'; DROP TABLE tiar_registry;"` into the TIAR Notion database. Assert the adapter retrieves the noun as a literal string, evaluates its TIRS score normally, and does not execute any embedded SQL.
- **TIAR Bypass Attempt:** Attempt to submit a VCB to Gate C-09 without the TIAR adapter's downstream validation having fired. Assert Gate C-09 detects the missing `tiar_validation_timestamp` in the VCB metadata and rejects with `TIAR_VALIDATION_MISSING`.
