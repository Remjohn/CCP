# Tech-Spec: FR2 — Sacred Audio Ingestion & Authenticity Scoring

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 2.0 (Aligned to CCP Architecture v2.1)
**Architecture Reference:** §10.6 (Audio Pipeline), §11.5 (Quality Gates), §7.6 (Voice Processing Skill Type Guide), §3.3 (Supabase Schemas)

---

## Overview

### Problem Statement

Raw coach audio is the primary source material for every downstream intelligence object in the CCP: Voice DNA (DEP-ENG-003, DEP-ENG-004), Emotional DNA (DEP-LIB-001), Session Transcript Intelligence (DEP-ENG-019), and the Coach Story Archive (DEP-ENG-024). If audio ingestion is performed without rigorous authenticity validation, all downstream dependencies are poisoned by curated-performance material — the coach's identity-protection layer, not their authentic voice.

The Authenticity Gate exists because the 3D Voice DNA extraction pipeline produces meaningless output from material where the coach is *teaching* rather than *expressing*. A coach explaining a concept in seminar mode uses different syntax, different pause cadence, and different emotional register than a coach reacting to a client situation or genuinely processing their own experience.

### Solution

A 4-stage ingestion pipeline that transforms raw coach audio (voice notes via Telegram, .ogg/.mp3/.m4a) into a scored array of `Thought_Units` — logic-bounded segments of authentic speech — suitable for downstream Voice DNA extraction. The pipeline runs exclusively via the Groq Whisper API (not local Whisper) with per-coach credential isolation, applies spaCy-based Thought Unit segmentation, scores each segment with the 7-Factor LIWC-22 Authenticity Algorithm at a ≥7/10 threshold, and writes only validated material to the coach's isolated instance.

### Scope

**In scope:**
- Telegram voice note ingestion (.ogg, .mp3, .m4a)
- Groq Whisper transcription with non-verbal preservation
- Thought Unit segmentation (spaCy syntactic dependency parsing)
- 7-Factor LIWC-22 Authenticity Gate (threshold ≥7/10)
- Receipt Chain Guard integration at every pipeline step
- Storage to `coach_soul.json` (validated Thought Units) and `memory_episodic` (Supabase)
- Telegram re-elicitation prompt generation on gate failure

**Out of scope:**
- Voice DNA extraction (FR3 Tech Spec)
- Sacred Audio used within CBCS client interactions (DEP-ENG-019 pipeline — separate spec)
- Coach Story Archive extraction (FR5 — separate spec)
- Any content generation from audio

---

## Context for Development

### Architecture Traceability

| DEP-ID | Name | Role in This Spec |
|---|---|---|
| `DEP-ENG-019` | Session Transcript Intelligence | Output target — validated Thought Units populate this object |
| `DEP-ENG-003` | Positive Space (Voice DNA) | Downstream consumer — populated by FR3 after this pipeline completes |
| `DEP-ENG-004` | Negative Space | Downstream consumer — populated by FR3 after this pipeline completes |
| `DEP-LIB-001` | Emotional DNA | Downstream consumer — populated by FR3 (Cognitive Appraisal mapping) |
| `DEP-PROTO-016` | Story Archive Approval Gate | Not triggered here — but this pipeline's output is the source material for DEP-ENG-024 |

### Voice Processing Skill Type Guide Constraints (§7.6)

The following constraints from the CCP Architecture v2.1 §7.6 are **mandatory** for all skills built within this pipeline:

1. **Input validation first.** Any audio file that arrives without a corresponding coach `coach_soul.json` baseline entry (at onboarding: the baseline doesn't exist yet, so this check is deferred to post-Stage-A) must be flagged for baseline establishment before processing.
2. **LIWC-22 gate is mandatory.** Every voice note receives an Authenticity Score before any downstream pipeline can consume the transcript. There is no bypass path.
3. **Tier-based activation.** This spec covers Tier 1 (basic transcript + authentication). Tier 2 skills (client intelligence extraction) are NOT activated from this pipeline — they require minimum 5 previous session records in `DEP-ENG-019`.
4. **Never generate from voice alone.** This pipeline produces structured data objects (transcripts, Authenticity Scores, Thought Unit arrays). It does not generate content. All generation is downstream.

### Key Files to Reference

| File | Purpose |
|---|---|
| `coach_soul.json` | Coach instance config — stores validated Thought Units in the extraction rounds |
| `coach_registry.json` | Per-coach instance manifest — confirms LIWC-22 dictionary residency |
| `Supabase: memory_episodic` | Episodic storage for validated sessions |
| `Supabase: coach_soul_json` | Persistent storage for extraction-round outputs |
| `Redis` | Message queue for Telegram delivery on gate failure |

### Technical Decisions

| Decision | Rationale |
|---|---|
| **Groq Whisper API (not local)** | Architecture v2.1 §10.6 specifies Groq. Local Whisper was an earlier design that was superseded. Groq provides sub-2s transcription at coaching audio lengths with fallback to Gemini Flash. |
| **LIWC-22 threshold ≥7/10 (not 0.60)** | Architecture v2.1 §11.5 specifies ≥7/10. The 0.60 threshold in the previous spec was from an earlier calibration. 7/10 reflects post-testing calibration. |
| **Thought Unit segmentation over token chunking** | Voice DNA Framework Principal 1: logic-driven chunking. Arbitrary token limits split mid-claim, destroying the syntactic fingerprint needed for stylometry. |
| **Preservation of non-verbals** | Filled pauses (um/uh), stutters, and false starts are authenticity signals in the LIWC-22 Marker 6 (Filler Frequency). Stripping them at ingestion corrupts the gate. Inverse Text Normalization (ITN) is bypassed at this stage. |
| **Re-elicitation via Telegram** | System does not reject the coach — it deepens the session. The therapeutic interview framework (DARN-CAT + OARS) governs re-elicitation phrasing to return the coach to episodic memory rather than declarative explanation. |

---

## Implementation Plan

### Stage A: Ingestion & Triage

**Trigger:** Coach sends `.ogg`, `.mp3`, or `.m4a` file via Telegram.

**Agent:** Telegram interceptor (Python bot handler)

**Steps:**
1. File received → written to ephemeral local buffer (in-process memory, not disk — Sacred Audio designation)
2. Validate file format: accept `.ogg`, `.mp3`, `.m4a` — reject all others with a silent discard (no coach notification for unsupported formats — handled by Telegram bot's file type check upstream)
3. Validate file duration: if `< 15 seconds` → implicit rejection. System responds: *"Could you share a bit more? I want to make sure I can really work with what you're giving me."*
4. No external API calls at this stage. The audio is not transmitted until Stage B.
5. Write `receipt` → Receipt Chain Guard (RCG) via Supabase + crypto hash

**Receipt Write (Stage A):** Per FR47 DEP-ENG-041 schema —
```json
{
  "receipt_id": "RCP-{COACH_ACRONYM}-SACRED-{DATE}-{SEQUENCE}-001",
  "previous_receipt_hash": null,
  "input_payload_hash": "sha256:{audio_file_hash}",
  "output_payload_hash": "sha256:{validated_audio_hash}",
  "stage_name": "SACRED-AUDIO-INGEST",
  "agent_name": "TelegramInterceptor",
  "timestamp": "{ISO8601}"
}
```

---

### Stage B: ASR via Groq Whisper API

**Engine:** Groq API (Whisper model) — per-coach API key from environment variables

**Fallback:** Gemini Flash transcription if Groq rate limit exceeded or API error

**Steps:**
1. Submit audio to Groq Whisper endpoint with `language` parameter set to coach's configured locale
2. **Non-standard Whisper configuration — mandatory:**
   - Disable ITN (Inverse Text Normalization): preserve `um`, `uh`, stutters, false starts
   - Request word-level timestamps for Thought Unit boundary detection in Stage C
   - Return raw transcript with all non-verbal utterances preserved
3. Validate API response — if `status != 200` → `DamageControl` extension triggers single retry. If retry fails → halt and alert coach: *"I'm having trouble processing your audio right now. Please try again in a few minutes."*
4. Write intermediate transcript to Working Memory (LangGraph state dict — volatile, single session)
5. **Receipt Write (Stage B):** Per FR47 DEP-ENG-041 schema —
```json
{ "receipt_id": "RCP-{COACH_ACRONYM}-SACRED-{DATE}-{SEQUENCE}-002",
  "previous_receipt_hash": "{STAGE_A_RECEIPT_HASH}",
  "input_payload_hash": "{AUDIO_API_PAYLOAD_HASH}",
  "output_payload_hash": "{RAW_TRANSCRIPT_HASH}",
  "stage_name": "ASR-TRANSCRIPTION",
  "agent_name": "Groq Whisper API",
  "timestamp": "{ISO8601}" }
```

---

### Stage C: Thought Unit Segmentation

**Engine:** Pi Coding Agent + `spaCy` (en_core_web_sm or equivalent) for syntactic dependency parsing

**Principle:** Voice DNA Framework Principal 1 — logic-driven chunking. A `Thought_Unit` is a complete logical move: `[claim → mechanism → emotional assertion]`. Token limits are irrelevant. Timestamp boundaries are irrelevant.

**Segmentation Rules:**
1. Parse transcript via spaCy dependency tree
2. A segment boundary is drawn **only** when:
   - A complete logical move (claim + mechanism + emotional assertion) resolves, AND
   - The dependency tree returns to a root state (no open subordinate clauses), AND
   - A natural pause marker (≥500ms silence from Whisper timestamps, or filler-pause sequence) is detected
3. Segments shorter than 30 words are merged with the subsequent segment (too short for LIWC-22 scoring)
4. Output: array of `Thought_Units`, each with: `unit_id`, `text`, `word_count`, `whisper_timestamps`

**Edge cases:**
- Long continuous streams (>500 words without a root return): force-segment at the 300-word mark with a "hard boundary" flag for LIWC-22 scoring adjustment
- Multilingual code-switching: flag for manual review — do not segment cross-language units

**Receipt Write (Stage C):** Per FR47 DEP-ENG-041 schema —
```json
{ "receipt_id": "RCP-{COACH_ACRONYM}-SACRED-{DATE}-{SEQUENCE}-003",
  "previous_receipt_hash": "{STAGE_B_RECEIPT_HASH}",
  "input_payload_hash": "{RAW_TRANSCRIPT_HASH}",
  "output_payload_hash": "{THOUGHT_UNIT_ARRAY_HASH}",
  "stage_name": "THOUGHT-UNIT-SEGMENTATION",
  "agent_name": "Pi Coding Agent",
  "timestamp": "{ISO8601}" }
```

---

### Stage D: 7-Factor LIWC-22 Authenticity Gate

**Engine:** LIWC-22 scoring dictionary (per-coach instance — stored in `coach_registry.json` boundaries per Architecture §10.6)

Each `Thought_Unit` is independently scored on 7 markers. Score = count of markers in-range / 7. Minimum passing score: **≥7/10** (i.e., all 7 markers must be within authentic range — the ≥7/10 means the composite indicator, not a ratio).

**The 7 Authenticity Markers:**

| # | Marker | Authentic Signal | Out-of-Range Signal |
|---|---|---|---|
| 1 | **First-Person Singular** | Elevated `I/me/my` — demonstrated ownership of experience | Low FPS → teaching/explaining mode, not experiencing |
| 2 | **Exclusive Words** | High density of `but`, `except`, `without` — cognitive distinction, nuanced processing | Near-zero → declarative mode, no complexity |
| 3 | **Absence of Hedging** | Zero or near-zero `maybe`, `perhaps`, `I think`, `I believe`, `kind of` | High hedging → identity-protection layer activating |
| 4 | **Sentence Compression** | Reduced WPS ratio — short burst sentences indicating emotional urgency | Long sentences → explanation, not reaction |
| 5 | **Verb Tense Distribution** | Spike in Simple Present ("it IS" not "it WAS") — Figural Deictic Present | Past-tense dominant → narrative recollection, not re-experiencing |
| 6 | **Filler Frequency** | Natural distribution of `um`/`uh` matching coach's established baseline | Zero fillers → scripted/curated; extreme fillers → anxiety (separate flag) |
| 7 | **Discourse Marker Position** | Transitions (`actually`, `so`, `look`) at mid-sentence, not sentence-opening | All transitions at sentence-open → structured academic delivery |

**Gate Logic:**
```
FOR EACH Thought_Unit:
  score = evaluate_7_markers(unit.text)
  IF score.pass_count >= 7:
    unit.status = "AUTHENTIC"
    → append to Authentic_Material_Payload
  ELSE:
    unit.status = "SYNTHETIC_CANDIDATE"
    unit.failed_markers = [list of failed markers]
    → queue for re-elicitation OR discard (based on session context)
```

**On Gate Failure (SYNTHETIC_CANDIDATE):**

The system does NOT tell the coach they failed. It deepens the session using a DARN-CAT framework prompt dispatched via Telegram. Examples calibrated to the failed marker:

| Failed Marker | Re-Elicitation Prompt |
|---|---|
| High hedging | *"I understood the idea, but I want to get closer to the actual moment. Tell me specifically: when did you first feel this? What were you doing?"* |
| Past-tense dominant | *"Walk me through it as if you're there right now. Not what happened — what is actually happening?"* |
| Low FPS | *"Tell me about a time when this personally affected YOU — not a client, not the industry. You."* |
| Zero fillers + low WPS (scripted) | *"That came through clearly — but I want the version you'd say to a close friend at 11pm. Less polished, more real."* |

**Receipt Write (Re-Elicitation Event):** Per FR47 DEP-ENG-041 schema —
```json
{ "receipt_id": "RCP-{COACH_ACRONYM}-SACRED-{DATE}-{SEQUENCE}-RETRY",
  "previous_receipt_hash": "{STAGE_C_RECEIPT_HASH}",
  "input_payload_hash": "{SYNTHETIC_UNIT_HASH}",
  "output_payload_hash": "{DARN_CAT_PROMPT_HASH}",
  "stage_name": "AUTH-GATE-REJECTION-RETRY",
  "agent_name": "LIWC-22 Evaluator",
  "timestamp": "{ISO8601}" }
```

**On Persistent Gate Failure (≥2 re-elicitation attempts on same unit):**
- Unit is permanently dropped from Working Memory per Architecture §10.6 data residency rules
- Session continues with remaining units — a session with ≥3 AUTHENTIC units proceeds to Stage E
- If total AUTHENTIC units < 3 → session is marked INSUFFICIENT and coach is notified to continue the conversation over the week
- **Receipt Write:** Stage fails, immutable rejection log written with `stage_name: "AUTH-GATE-PERSISTENT-FAILURE"`

**Receipt Write (Stage D Success):** Per FR47 DEP-ENG-041 schema —
```json
{ "receipt_id": "RCP-{COACH_ACRONYM}-SACRED-{DATE}-{SEQUENCE}-004",
  "previous_receipt_hash": "{LAST_RETRY_OR_STAGE_C_HASH}",
  "input_payload_hash": "{THOUGHT_UNIT_ARRAY_HASH}",
  "output_payload_hash": "{VALIDATED_UNITS_HASH}",
  "stage_name": "LIWC-AUTHENTICITY-GATE",
  "agent_name": "LIWC-22 Evaluator",
  "timestamp": "{ISO8601}" }
```

---

### Stage E: Storage & Downstream Handoff

**Condition:** Session contains ≥3 AUTHENTIC Thought_Units

**Storage targets:**

| Data | Target | Notes |
|---|---|---|
| `Authentic_Material_Payload` (full Thought_Unit array) | `coach_soul.json` extraction_rounds field | Append — not overwrite. Running total across sessions. |
| Session metadata (session_id, date, unit_count, authenticity_scores) | `Supabase: memory_episodic` | Per Architecture §6.1 Working → Episodic promotion |
| Failed units | Permanently dropped from Working Memory | No storage per Architecture §10.6 |
| Raw audio file | `Supabase Storage` (encrypted AES-256) | Sacred Audio designation — not transmitted to any external API except Groq Whisper |

**Minimum corpus requirement for FR3 (Voice DNA Extraction):**
- Minimum of **3,000 validated words** (Post-LIWC-22 gate) across all sessions before FR3 pipeline can be triggered
- Word count is tracked in `coach_soul.json` → `extraction_readiness.authenticated_word_count`
- When count crosses 3,000: system notifies Morgan (Setup Orchestrator) to initiate FR3

**Receipt Write (Stage E Final Store):** Per FR47 DEP-ENG-041 schema —
```json
{ "receipt_id": "RCP-{COACH_ACRONYM}-SACRED-{DATE}-{SEQUENCE}-005",
  "previous_receipt_hash": "{STAGE_D_RECEIPT_HASH}",
  "input_payload_hash": "{VALIDATED_UNITS_HASH}",
  "output_payload_hash": "{STORAGE_COMMIT_HASH}",
  "stage_name": "EPISODIC-STORAGE-COMMIT",
  "agent_name": "ArchitectStorage",
  "timestamp": "{ISO8601}" }
```

Chain integrity: all receipts A through E must be resolvable. If any predecessor is missing, pipeline halts.

---

## Tasks

- [ ] **Task 1:** Build Telegram bot handler for audio file ingestion (duration check + format validation)
- [ ] **Task 2:** Integrate Groq Whisper API with non-standard config (ITN disabled, word timestamps, non-verbal preservation) + Gemini Flash fallback
- [ ] **Task 3:** Implement spaCy Thought Unit segmentation with dependency tree boundary logic
- [ ] **Task 4:** Implement LIWC-22 7-Factor Authenticity Gate with per-marker scoring and SYNTHETIC_CANDIDATE flagging
- [ ] **Task 5:** Build DARN-CAT re-elicitation prompt generator with marker-specific responses
- [ ] **Task 6:** Implement storage pipeline (coach_soul.json append, memory_episodic insert, Supabase Storage AES-256)
- [ ] **Task 7:** Integrate Receipt Chain Guard at every stage (A through E) with hash chaining
- [ ] **Task 8:** Implement 3,000-word threshold tracker and FR3 readiness notification to Morgan

---

## Acceptance Criteria

- [ ] **AC1:** Audio files ≥15s in accepted formats (.ogg/.mp3/.m4a) are successfully ingested. Files <15s are silently rejected with a gentle coach prompt.
- [ ] **AC2:** Groq Whisper transcription preserves all filled pauses (um/uh), stutters, and false starts. A test transcript with 10 inserted fillers must return all 10 in the output (ITN not applied).
- [ ] **AC3:** Thought Unit segmentation produces segments where no segment contains an open subordinate clause at its final word (spaCy dependency tree validation).
- [ ] **AC4 (Gate Pass):** A test Thought Unit with all 7 authentic markers present scores status=AUTHENTIC. The unit is appended to the Authentic_Material_Payload.
- [ ] **AC5 (Gate Fail):** A test Thought Unit with hedging language (`maybe`, `I think`, `kind of`) AND past-tense dominant verbs scores status=SYNTHETIC_CANDIDATE. The system dispatches the correct re-elicitation prompt variant (hedging prompt, not generic).
- [ ] **AC6 (Persistent Failure):** After 2 re-elicitation attempts that both fail, the unit is dropped. No error is raised. Session continues with remaining units.
- [ ] **AC7 (Insufficient Session):** A session with only 2 AUTHENTIC units after all attempts ends in status=INSUFFICIENT. Coach is notified without alarm.
- [ ] **AC8 (Receipt Chain):** After a complete 5-stage session, all receipts A through E exist in Supabase with resolvable predecessor_receipt fields. Receipt chain integrity check passes.
- [ ] **AC9 (Threshold):** When `extraction_readiness.authenticated_word_count` crosses 3,000, Morgan receives a pipeline trigger notification within the same execution cycle.
- [ ] **AC10 (Isolation):** Raw audio is never transmitted to any service other than Groq Whisper. A network intercept test on a simulated session must show only one external TLS connection (Groq endpoint).

---

## Dependencies

| Dependency | Type | Notes |
|---|---|---|
| Groq API key (per coach) | External service | Stored in environment variable — never committed to code |
| LIWC-22 scoring dictionary | License | Stored per-coach instance in `coach_registry.json` boundaries |
| spaCy `en_core_web_sm` (or locale equivalent) | Python package | Version-pinned in requirements.txt |
| `coach_soul.json` schema v4.0 | Internal | Must include `extraction_readiness.authenticated_word_count` field |
| Receipt Chain Guard (Supabase + crypto hash) | Internal | Supabase `receipts` table must exist — created in Build Step 1 |
| Redis message queue | Internal | For Telegram re-elicitation delivery queueing |

---

## Testing Strategy

### Unit Tests
- Groq Whisper API mock: verify ITN-disabled config is sent in request header
- Thought Unit segmentation: 10 synthetic transcripts with known dependency tree structures → validate boundary placement
- LIWC-22 gate: 14 synthetic Thought Units (7 authentic, 7 with single-marker failures) → validate pass/fail classification for each marker independently

### Integration Tests
- End-to-end: submit a real 2-minute voice note → validate receipt chain A→E is intact
- Re-elicitation flow: submit a heavily hedged voice note → validate DARN-CAT prompt dispatched via Telegram within 2 seconds

### Data Isolation Test
- Submit audio for Coach A while Coach B instance is running → validate Coach A's Thought Units appear only in Coach A's `coach_soul.json` and `memory_episodic`

### Performance Test
- Groq transcription latency: 2-minute audio → transcript < 10 seconds (P95)
- Full pipeline (Stage A through E): < 30 seconds for a 5-minute voice note (P95)
