# Tech-Spec: FR-CA11-08 — Live Coaching → Content Machine Pipeline

**Created:** 2026-03-24
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / PRD Update v2.0 — Capability Area 11)
**Architecture Reference:** PRD-Update-CA11 §4.2
**Skill Implementation:** `skills/expression/session-content-extractor/SKILL.md`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md` (FR24 Weekly Pipeline, FR26 Validation Gate)
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd-update-CA11-quad-platform.md`

---

## 2. Overview

### Problem Statement
A 60-minute coaching session contains 10-15 moments of genuine insight — raw, unscripted, emotionally authentic statements that are more powerful than any CCF-generated script because they're born from real human interaction. But in the current architecture, these moments are lost forever after the session ends. The CCF operates on *scheduled* weekly production cycles with trigger-first activation — it has no mechanism to ingest *unscheduled* coaching session intelligence as content source material.

### Solution
FR-CA11-08 bridges the Session Intelligence pipeline (FR-CA11-05) with the CCF Expression Department. After `Lena` produces a Session Intelligence Report, the **Content Machine Pipeline** routes session insights to `Julio` (Micro-Content Factory) and `Cesare` (Script Artisan) as supplementary content sources. Julio extracts 5-8 micro-content pieces (Telegram insight cards, Instagram caption drafts, short-form video script candidates). Cesare evaluates whether any insights qualify for the current weekly CCF batch. All extracted content passes through the standard Triple-Pass Validation Gate (Sophia/Marcus/Chen) before delivery.

### Scope
**In scope:**
- Session Intelligence Report → CCF Expression Department routing.
- Micro-content extraction by `Julio` (5-8 pieces per session).
- CCF batch evaluation by `Cesare`.
- Standard Triple-Pass Validation + Receipt Chain Guard compliance.
- AFFiNE delivery of session-derived content.

**Out of scope:**
- Session recording and transcription (FR-CA11-05/FR-CA11-13).
- Visual asset generation (handled by existing CVE pipeline).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| FR-CA11-05 (Session Recap) | Session Intelligence Report | SOURCE — Provides key insights, emotional beats, and breakthrough moments. |
| `Julio` (Micro-Content Factory) | Expression Agent | AGENT — Extracts 5-8 micro-content pieces from session insights. |
| `Cesare` (Script Artisan) | Expression Agent | AGENT — Evaluates session insights against current CCF batch for inclusion. |
| FR26 (Triple-Pass Validation) | Sophia/Marcus/Chen | GATE — All session-derived content must pass standard validation. |
| `DEP-ENG-020` | Fingerprint Archive | CONSUMER — Session-derived content gets its own Fingerprint ID. |

### Technical Decisions
1. **Session Content Enters CCF as "Supplementary Source":** Session insights do not replace CRAL research or trigger-first activation. They are an additional source of authentic content that can be mixed into the existing weekly batch. `Cesare` evaluates whether a session insight aligns with the current batch's theme and psychological routing. If yes, it enters the batch. If no, it enters a separate content queue.
2. **Dual Fingerprint Traceability:** Session-derived content carries both the session's `session_id` (provenance) and a standard `fingerprint_id` (compilation parameters). This enables the Data Analyst (FR43) to compare performance of session-derived content vs. standard CCF content.

---

## 4. Implementation Plan

### Stage 1: Session → Micro-Content Extraction
*Agent:* `Julio` (Micro-Content Factory)
*Inputs:* Session Intelligence Report (from FR-CA11-05).
*Outputs:* 5-8 micro-content pieces.
*Failure Condition:* Extraction yields < 3 pieces → session flagged as "low content density" (no error, just metadata).

**Steps:**
1. `Lena` completes Session Intelligence Report → fires event to `Julio`.
2. `Julio` scans key insights and breakthrough moments for content candidates:
   - **Telegram Insight Cards:** One-liner insights formatted for Telegram audience delivery.
   - **Instagram Caption Drafts:** 150-300 word scripts built from session insights + coach Voice DNA.
   - **Short-Form Video Script Candidates:** Insights with high emotional intensity (beat intensity > 0.7) flagged for video production.
3. Each micro-content piece receives a Universal Asset ID (FR46) with pipeline = `SESSION`.
4. All pieces are queued for Triple-Pass Validation.

### Stage 2: CCF Batch Evaluation
*Agent:* `Cesare` (Script Artisan)
*Inputs:* Session insights, current weekly CCF batch theme, `DEP-ENG-016` (Psychological Routing Brief).
*Outputs:* Batch inclusion decision (include/queue).

**Steps:**
1. `Cesare` receives session insights and cross-references with the current weekly batch's:
   - Active theme (from `Divine` theme discovery).
   - Psychological routing (from `DEP-ENG-016`).
   - Boredom Ban window (no semantic overlap with last 8 weeks).
2. Insights that align are inserted into the current batch as supplementary scripts.
3. Insights that don't align are stored in a "Session Content Queue" for future batch consideration.

### Stage 3: Validation & Delivery
*Agent:* Sophia/Marcus/Chen → `affine_sync.py`
*Inputs:* Micro-content pieces + any batch-included scripts.
*Outputs:* Validated content pushed to AFFiNE Content Calendar.

**Steps:**
1. Triple-Pass Validation Gate applied (TTT drift ≤15%, structural compliance, AI detection < 5%).
2. Passed content receives Fingerprint ID with `source_type = SESSION`.
3. Content pushed to coach's AFFiNE Content Calendar via `affine_sync.py` with session provenance metadata.
4. Receipt Chain Guard updated.

---

## 5. Primary Output Schema

**Data Object:** Content Machine Array (`DEP-ENG-078` PROPOSED)

```json
{
  "session_id": "uuid-session-001",
  "content_pieces": [
    {
      "asset_id": "JP-SESSION-20260324-001-CAPTION",
      "content_type": "instagram_caption",
      "text": "The moment you stop asking for permission to be yourself...",
      "source_insight_timestamp": "00:14:32",
      "validation_status": "PASSED",
      "fingerprint_id": "SKILL-SESSION-JP-DISC-PROM-DEV-20260324-001",
      "batch_included": false,
      "queue_status": "session_content_queue",
      "receipt_chain_guard": { "schema_ref": "DEP-ENG-041" }
    }
  ],
  "total_extracted": 7,
  "batch_included_count": 2,
  "queued_count": 5
}
```

---

## 6. Backward Compatibility Fallback
Session content extraction is entirely additive — it does not replace or interfere with the standard CCF weekly pipeline. If `Julio` or `Cesare` fail, the Session Intelligence Report still exists and is delivered to AFFiNE (FR-CA11-05). No standard CCF production is affected.

---

## 7. Tasks

- [ ] **Task 1:** Write session-content-extractor SKILL.md for `Julio` (micro-content extraction from Session Intelligence Reports).
- [ ] **Task 2:** Implement `Cesare` batch evaluation logic (session insight ↔ current batch theme matching).
- [ ] **Task 3:** Add `source_type` field to Fingerprint Archive schema (new enum: `SESSION`).
- [ ] **Task 4:** Wire Session Intelligence Report completion event to `Julio` and `Cesare`.
- [ ] **Task 5:** Wire extracted content through Triple-Pass Validation Gate.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Content Multiplication):** Process a session with 5 key insights. Assert ≥5 micro-content pieces extracted.
- [ ] **AC2 (Batch Inclusion):** Session insight matches current batch theme. Assert it's included in the CCF batch.
- [ ] **AC3 (Queue Routing):** Session insight doesn't match current batch. Assert it enters the session content queue.
- [ ] **AC4 (Triple-Pass Validation):** Assert all session-derived content passes Sophia/Marcus/Chen before delivery.
- [ ] **AC5 (Fingerprint Traceability):** Assert `source_type = SESSION` in the Fingerprint Archive for all session-derived content.
- [ ] **AC6 (Non-Interference):** Run the Content Machine Pipeline during an active CCF weekly pipeline. Assert CCF batch is not disrupted.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR-CA11-05 (Session Recap) | Internal | Source of Session Intelligence Reports. |
| FR24 (Weekly Pipeline) | Internal | CCF batch evaluation context. |
| FR26 (Validation Gate) | Internal | Triple-Pass compliance. |
| FR46 (Universal Asset ID) | Internal | Asset ID minting for content pieces. |

---

## 10. Testing Strategy

### Unit Tests
- **Extraction Quality:** Pass a known Session Intelligence Report. Assert extracted micro-content meets minimum quality standards (Voice DNA adherence, minimum word count, no AI slop).

### Integration Tests
- **Dual Pipeline:** Run CCF weekly batch + session content machine simultaneously. Assert no conflicts, no duplicate Asset IDs, no Receipt Chain corruption.

### Performance Tests
- **Content Multiplication Ratio:** Process 5 sessions. Assert average ≥ 8 content pieces per session.
