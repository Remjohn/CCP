# FR-CBCS-06: SEARCH Phase Detection Engine — Tech Spec

**Created:** 2026-03-18
**Status:** Ready for Development
**Architecture Reference:** CCP_CBCS_CPSC_V3 §F6, PRD §FR-CBCS-06

---

## 1. Files Read
- `docs/prd/prd.md`
- `lab/CCP update/CCP_CBCS_CPSC_V3.docx.md`

---

## 2. Overview

### Problem Statement
Intervention timing is usually arbitrary or based on elapsed time (e.g., "send offer after 14 days"). This risks sending high-stakes commercial invitations when the client's psychological defenses are consolidated or during transient "pseudo-SEARCH" spikes. A mistimed message damages the therapeutic relationship and wastes conversion potential.

### Solution
The SEARCH Phase Detection Engine monitors the linguistic structure of all CBCS messages using LIWC-22 to detect the exact window of maximal intervention receptivity. It identifies a 4-signal convergence indicating the client is actively seeking a new paradigm. To prevent false positives, it mandates a 24-hour observation window to confirm the phase change is sustained before triggering any downstream conversion sequences.

### Scope
**In scope:**
- Identification of 4 linguistic signals (info-seeking, verb tense shift, agency increase, hedging decrease).
- The `search-phase-detector` continuous monitoring script.
- The `reconsolidation-window-validator` confirming sustained signals over 24 hours.
- Outputting the `CONFIRMED` status to trigger FR-CBCS-05 (72-Hour Anchor Protocol).

**Out of scope:**
- Action taken post-confirmation (handled by FR-CBCS-05 and FR53).
- Individual processing of raw audio to text (handled by FR3 Voice DNA extraction layer).

---

## 3. Context for Development

### Architecture Traceability
| DEP-ID | Name | Role | Produced By | Consumed By |
|---|---|---|---|---|
| `search_phase_detections` | Status Log SQL Table | Tracks active/expired detections | FR-CBCS-06 | FR-CBCS-05, FR53 |
| `PROPOSED: DEP-ENG-061` | Phase Confirmation Verdict | Hard gate for campaign fire | FR-CBCS-06 | Campaign Router |

### Academic Grounding
- **Research Paper:** *Regret Regulation Theory* (Zeelenberg & Pieters, 2007) + *Memory Reconsolidation* (Nader, 2000).
- **Mechanism:** Anticipation of regret from inaction drives receptivity. When psychological beliefs enter a labile (malleable) state (Reconsolidation Window), the message lands on an open neurological architecture. The 24-hour hold ensures the labile state is authentic, not just a fleeting emotional reaction (pseudo-SEARCH).

### Technical Decisions
- **Background Runner:** The `search_phase_monitor.py` runs over the output of the standard `liwc_scores_jsonb` ingestion pipeline. It evaluates convergence rather than single-metric spikes.
- **24-Hour Confirmation:** A client entering SEARCH is immediately tagged `DETECTING`. Only a subsequent interaction *within 24 hours* matching the linguistic pattern graduates them.

---

## 4. Implementation Plan

### Stage 1: Linguistic Convergence Detection
- **Agent:** `search-phase-detector` (Python continuous monitor)
- **Inputs:** 
  - `liwc_scores_jsonb` (DEP-ID: `DEP-ENG-047` — Produced By: FR47 LIWC-22 Global Analyzer)
- **Outputs:** Database row initialization in `search_phase_detections`.
- **Failure Condition:** If the message is $<10$ words, execution `return False` immediately. Math ratios are unstable on tiny word counts. Zero DB writes.
- **Receipt Chain Guard (DEP-ENG-041):** Cryptographic hash of `client_id` + `status` logged on successful initialization of a tracking event.
- **ADR-01 Isolation Constraint:** The detection table operates explicitly inside `WHERE coach_id = auth.uid()` scopes.

### Stage 2: Reconsolidation Window Validation
- **Agent:** `reconsolidation-window-validator` (Python cron job)
- **Inputs:** `search_phase_detections` where `status = 'DETECTING'`
- **Outputs:** `PROPOSED: DEP-ENG-061` (Phase Confirmation Verdict JSON).

**Quality Gate:** **SEARCH Phase Confirmation Gate**
- **Triggered when:** The cron job polls for follow-up client interactions inside the 24-hour window from the `DETECTING` timestamp.
- **Exact Thresholds:** A subsequent client interacting passing all 4 constraints: `info_seeking > 0.08` AND `future_focus > 0.05` AND `agency_words > 0.05` AND `hedging_words < 0.02`.
- **Verdict - PASS:** A new message passes the 4 constraints AND `< 24h` has passed AND `> 4h` has passed. *Downstream Consequence:* `status` transitions to `CONFIRMED`. Triggers FR-CBCS-05.
- **Verdict - PROVISIONAL:** A new message passes the 4 constraints BUT `< 4h` has elapsed since `DETECTING`. *Downstream Consequence:* Client might just be sending 2 messages in the exact same sitting (monologue loop). `status` transitions to `PROVISIONAL_WAIT` requiring one more message tomorrow before triggering campaigns.
- **Verdict - FAIL:** $0$ new messages pass the constraints within the strict 24-hour window. *Downstream Consequence:* `status` transitions to `EXPIRED`. Triggers nothing. Monitor resets.

### Stage 3: Variable Resolution Rules for State (Enum)
The `status` enum string resolves precisely by these conditions:
- **"DETECTING"**: The exact moment Stage 1 logic finds a single payload passing the 4 LIWC constraints.
- **"CONFIRMED"**: Triggers globally IF Stage 2 Gate evaluates to PASS.
- **"PROVISIONAL_WAIT"**: Triggers globally IF Stage 2 Gate evaluates to PROVISIONAL.
- **"EXPIRED"**: Triggers globally IF Stage 2 Gate evaluates to FAIL.
- **"MANUAL_OVERRIDE"**: String executed ONLY when the human operator executes `/cpsc-search override [client_id]` bypassing algorithms entirely.

### Stage 4: Resolution Rules for Output Schema
Every field in the `SearchPhaseDetectionRow` utilizes exact internal logic mapping:
- `detection_id`: `uuid.uuid4()` PK.
- `client_id` / `coach_id`: Synchronous passage.
- `analytical_thinking_score`: Float extraction from `liwc_scores_jsonb.analytical_thinking`.
- `discrepancy_word_freq`: Float extraction from `liwc_scores_jsonb.discrep.freq`.
- `future_focus_freq`: Float extraction from `liwc_scores_jsonb.focusfuture.freq`.
- `self_reference_freq`: Float extraction from `liwc_scores_jsonb.i.freq`.
- `cluster_confidence_score`: Average of the normalized 4 metric float values (0.0-1.0 band).
- `status`: String explicitly tied to Stage 3 Enum Resolution rules.
- `triggered_priming_at`: Populates with ISO8601 string ONLY when status hits `CONFIRMED` or `MANUAL_OVERRIDE`. Null otherwise.
- `last_updated`: `datetime.now(timezone.utc).isoformat()`.

---

## 5. Primary Output Schema

```typescript
type SearchPhaseDetectionRow = {
  detection_id: string; // uuid4
  client_id: string; // uuid4
  coach_id: string; // uuid4 (ADR-01 boundary)
  analytical_thinking_score: number;
  discrepancy_word_freq: number;
  future_focus_freq: number;
  self_reference_freq: number;
  cluster_confidence_score: number; // Float 0.0 - 1.0
  status: "DETECTING" | "CONFIRMED" | "PROVISIONAL_WAIT" | "EXPIRED" | "MANUAL_OVERRIDE";
  triggered_priming_at: string | null; // ISO8601
  last_updated: string; // ISO8601
};
```

---

## 6. Backward Compatibility Fallback
For FR30/FR53 campaigns natively triggering on "time elapsed" (e.g., dormant 14 days):
- The `IntelligenceGateRouter` disables pure time-based triggers for new enrollments.
- If a client currently has no active `CONFIRMED` SEARCH phase row in the database, legacy workflows simply remain dormant until natural linguistic detection occurs or the operator triggers the `MANUAL_OVERRIDE` enum state.

---

## 7. Tasks
- [ ] **Task 1: AI Detector Integration** - Create `search_phase_detector.py` executing the 4-LIWC-threshold check mapping to the `DETECTING` enum initial write.
- [ ] **Task 2: State Machine Logic** - Build `reconsolidation-window-validator.py` executing the exact `timestamp_delta` (4h-24h window limitation) to gate PASS versus PROVISIONAL.
- [ ] **Task 3: Downstream Trigger Hooks** - Wire the `CONFIRMED` enum update database trigger to POST an event bus payload into FR-CBCS-05's `pre-invitation-priming-orchestrator`.
- [ ] **Task 4: Slash Command Setup** - Register `/cpsc-search override [id]` to enforce the `MANUAL_OVERRIDE` DB write explicitly.

---

## 8. Acceptance Criteria
- [ ] **AC1 (False Positive Prohibition):** A client emitting `info_seeking = 0.9` but `future_focus = 0.0` MUST return a `False` boolean in Stage 1, writing zero rows to the `search_phase_detections` table. **Failure Example:** The system trips on a single dimension outlier, opening vulnerable grief clients to commercial solicitation.
- [ ] **AC2 (Provisional Window Gating):** A client hitting the 4 constraints twice within exactly 2 hours MUST update `status` to `PROVISIONAL_WAIT`. **Failure Example:** System ignores the `<4h` monologue constraint, triggering `CONFIRMED` and sending campaigns while the user is still dictating a 60-part voice note.
- [ ] **AC3 (Expiration Check):** A `DETECTING` row older than exactly 24 hours `0 minutes` without seeing client activity dropping subsequent constraints MUST update to `EXPIRED`. **Failure Example:** The state stays open indefinitely, and a random message 3 months later suddenly chains to `CONFIRMED` erroneously.
