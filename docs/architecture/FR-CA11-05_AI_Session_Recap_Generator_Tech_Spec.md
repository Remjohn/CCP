# Tech-Spec: FR-CA11-05 — AI Session Recap Generator

**Created:** 2026-03-24
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / PRD Update v2.0 — Capability Area 11)
**Architecture Reference:** PRD-Update-CA11 §4.2
**Skill Implementation:** `skills/perception/session-intelligence-analyst/SKILL.md`, `tools/session_recap_generator.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md` (FR2 Sacred Audio, FR29 Context Premise Extraction)
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd-update-CA11-quad-platform.md`
- `d:\Work\The Conscious Coaching Factory\CMF_Pipeline_Documentation.md`

---

## 2. Overview

### Problem Statement
Coaching sessions are the highest-density intelligence source in the CCP ecosystem — more psychologically rich than social media engagement, more authentic than CBCS text interactions. Yet in the parent PRD, session recordings go nowhere. The coach records a 60-minute call, and the intelligence dies in a `.mp4` file. No extraction. No client summary. No CRAL evidence. No Context Premise update. The richest data source in the system is completely unprocessed.

### Solution
FR-CA11-05 converts a CCP Studio recording (or legacy OBS recording) into a **structured Session Intelligence Report** delivered to both the coach's AFFiNE Session Archive and the client's Telegram within 10 minutes of session end. The pipeline: Whisper STT → LLM extraction by `Lena` (Session Intelligence Analyst) → AFFiNE push → Telegram delivery → Context Premise graph update → CRAL evidence pool injection. Every coaching session henceforth compounds the system's intelligence.

### Scope
**In scope:**
- Post-recording transcription pipeline (Whisper via NVIDIA NIM).
- Session Intelligence Report extraction (key insights, action items, emotional beats, topic clusters).
- AFFiNE Session Archive delivery.
- Telegram client summary delivery.
- Session Mind Map (auto-generated Excalidraw diagram).
- Context Premise graph feed (Neo4j).
- CRAL evidence pool feed.

**Out of scope:**
- Recording trigger (FR-CA11-16 CCP Studio Block — replaces FR-CA11-13 OBS Controller).
- Session-to-course pipeline (FR-CA11-07).
- Content machine pipeline (FR-CA11-08).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| FR2 (Sacred Audio) | Whisper Transcription | REUSED — Same local Whisper pipeline used for coach voice notes, now applied to session recordings. |
| FR29 (Context Premise Extraction) | Aria Synthesizer | EXTENDED — `Aria` updates client Context Premise from session transcript (same extraction logic, new input source). |
| `DEP-ENG-021` | CRAL Finding Index | EXTENDED — Session insights that qualify as M1-M7 moments are injected into CRAL. |
| `Benjamin` (Excalidraw Composer) | Visual Pipeline | REUSED — Generates Session Mind Map as `.excalidraw` JSON. |
| `Lena` (Session Intelligence Analyst) | New Agent | CORE — Extracts structured intelligence from raw session transcript. |

### Academic Grounding

| Framework | Author | Year | Mechanism |
|---|---|---|---|
| **Active Listening Extraction** | Rogers | 1957 | The extraction model identifies not just what was *said* but what was *meant* — emotional subtext, unspoken concerns, breakthrough moments — using the same LIWC-22 authenticity markers that Miriam applies to CBCS voice notes. |
| **Kolb's Experiential Learning Cycle** | Kolb | 1984 | The Session Intelligence Report structures insights along Kolb's cycle: Concrete Experience (what happened in session) → Reflective Observation (key insights) → Abstract Conceptualization (action items) → Active Experimentation (next session focus). |

### Technical Decisions
1. **NVIDIA NIM Whisper over Cloud ASR:** Self-hosted Whisper on NVIDIA NIM containers (GPU instances) provides: zero data leakage (sensitive coaching content never leaves infrastructure), no per-minute billing, and consistent latency. A 60-minute recording transcribes in ~3 minutes on an A10G instance.
2. **Session Mind Map via Excalidraw:** The Mind Map is not a static image — it's an `.excalidraw` JSON that can be embedded in AFFiNE (FR-CA11-10) for interactive exploration. Topic nodes are clickable, linking to specific transcript timestamps.
3. **10-Minute SLA:** The entire pipeline (upload → transcribe → extract → render → deliver) must complete within 10 minutes. This is achievable because: transcription (~3 min), LLM extraction (~2 min), Excalidraw render (~30 sec), AFFiNE sync (~30 sec), Telegram delivery (~5 sec).

---

## 4. Implementation Plan

### Stage 1: Recording Upload & Transcription
*Agent:* CCP Studio Block (FR-CA11-16) triggers pipeline on recording completion.
*Inputs:* Recording file (`.webm` or `.mp4`) uploaded to S3 from CCP Studio.
*Outputs:* Full text transcript with timestamps.
*Failure Condition:* Upload fails → retry with exponential backoff. Whisper fails → alert operator, queue for retry. Pipeline does not cascade-fail.

**Steps:**
1. CCP Studio Block `POST /studio/complete` event fires (or legacy `obs_controller.py` stop-recording event).
2. Recording file is uploaded to S3 bucket: `s3://{coach_acronym}/sessions/{session_id}.mp4`.
3. Whisper STT (NVIDIA NIM) processes the audio track. Output: timestamped transcript JSON.
4. Transcript is stored in Supabase `session_intelligence` table (new record with `session_id`, `recording_url`, `transcript_url`).

### Stage 2: Intelligence Extraction
*Agent:* `Lena` (Session Intelligence Analyst)
*Inputs:* Timestamped transcript, client's current Context Premise (from Neo4j), coach's Voice DNA (DEP-ENG-003).
*Outputs:* Session Intelligence Report.

**Steps:**
1. `Lena` receives the transcript and client's Context Premise snapshot.
2. Extract structured intelligence:
   - **Key Insights** (3-7): Most significant coaching moments. Each insight includes transcript timestamp, coach statement, client response, and psychological significance.
   - **Action Items** (2-5): Concrete takeaways for the client. Framed using Implementation Intentions (Gollwitzer) format: "When [X], I will [Y]."
   - **Emotional Beats**: Timeline of emotional intensity across the session (low → high → resolution). Each beat annotated with dominant mood state (Processing/Escape/Discovery/Status).
   - **Topic Clusters**: Thematic categories covered in the session, mapped to Context Premise dimensions.
   - **Breakthrough Moments**: Instances where the client's language shifts from Information Avoidance/Passive Consumption to Active Engagement (DARN-CAT markers).
3. Store the full Session Intelligence Report in `session_intelligence` table.

### Stage 3: Mind Map Generation & Delivery
*Agent:* `Benjamin` (Excalidraw Composer) + `affine_sync.py`
*Inputs:* Topic clusters, emotional beats from Session Intelligence Report.
*Outputs:* `.excalidraw` JSON mind map, AFFiNE page, Telegram message.

**Steps:**
1. `Benjamin` generates a mind map from topic clusters: central node = session title, branch nodes = topic clusters, leaf nodes = key insights.
2. Emotional beats are overlaid as a color gradient on the mind map (warm = high emotional intensity, cool = low).
3. The mind map `.excalidraw` JSON is stored in S3 and pushed to coach's AFFiNE Session Archive via `affine_sync.py`.
4. A formatted text summary (key takeaways + action items) is sent to the client via Telegram bot.
5. Full Session Intelligence Report is pushed to the coach's AFFiNE workspace.

### Stage 4: Intelligence Propagation
*Agent:* `Aria` (Context Premise Extractor) + CRAL Router
*Inputs:* Session Intelligence Report.
*Outputs:* Updated Neo4j Context Premise, updated CRAL Finding Index (DEP-ENG-021).

**Steps:**
1. `Aria` receives the Session Intelligence Report and updates the client's Context Premise in Neo4j with new insights, emotional patterns, and topic shifts.
2. CRAL Router evaluates whether any session insights qualify as CRAL M1-M7 moments. Qualifying insights are injected into the CRAL Finding Index with source provenance = "coaching_session".
3. If breakthrough moments are detected (DARN-CAT Change Talk), they are logged in the Change Talk Vault (FR-CBCS-01).

---

## 5. Primary Output Schema

**Data Object:** Session Intelligence Report (`DEP-ENG-075` PROPOSED)

```json
{
  "session_id": "uuid-session-001",
  "coach_id": "uuid-coach-001",
  "client_id": "uuid-client-042",
  "recording_url": "s3://JP/sessions/uuid-session-001.mp4",
  "transcript_url": "s3://JP/transcripts/uuid-session-001.json",
  "key_insights": [
    {
      "timestamp": "00:14:32",
      "coach_statement": "What does success look like without the approval?",
      "client_response": "I... I've never actually thought about that.",
      "psychological_significance": "Client confronting dependency on external validation — L3 Hidden Belief exposure."
    }
  ],
  "action_items": [
    {
      "implementation_intention": "When I catch myself seeking approval at work, I will pause and write down what I actually want.",
      "context_premise_dimension": "Hidden Beliefs",
      "difficulty": "developing"
    }
  ],
  "emotional_beats": [
    {"timestamp": "00:05:00", "intensity": 0.3, "mood_state": "Processing"},
    {"timestamp": "00:14:32", "intensity": 0.9, "mood_state": "Discovery"},
    {"timestamp": "00:42:00", "intensity": 0.5, "mood_state": "Processing"}
  ],
  "topic_clusters": ["external_validation", "self_worth", "career_identity"],
  "breakthrough_moments": [
    {"timestamp": "00:14:32", "darn_cat_category": "Activation", "raw_text": "I've never actually thought about that."}
  ],
  "mind_map_url": "s3://JP/excalidraw/session_uuid-session-001_mindmap.json",
  "receipt_chain_guard": { "schema_ref": "DEP-ENG-041" }
}
```

---

## 6. Backward Compatibility Fallback
If Whisper transcription fails (GPU unavailable, recording corrupt), the system stores the raw recording in S3 and queues transcription for retry. The coach is notified via Telegram: "Your session recording is saved. Recap is being processed (delayed)." No data is lost. If LLM extraction fails, the raw transcript is still delivered to AFFiNE — the coach can read it manually.

---

## 7. Tasks

- [ ] **Task 1:** Create Supabase `session_intelligence` table with schema defined in §5.
- [ ] **Task 2:** Build `Lena` agent persona YAML (Session Intelligence Analyst, Perception Department).
- [ ] **Task 3:** Write `Lena`'s extraction SKILL.md with 5 extraction targets (insights, actions, beats, clusters, breakthroughs).
- [ ] **Task 4:** Build S3 upload trigger hook from CCP Studio Block `POST /studio/complete` (replaces `obs_controller.py` trigger).
- [ ] **Task 5:** Wire Whisper STT (NVIDIA NIM) for session recording transcription.
- [ ] **Task 6:** Implement Excalidraw mind map generation in `Benjamin` (session-specific template).
- [ ] **Task 7:** Wire `Aria` to accept Session Intelligence Report as input source for Context Premise updates.
- [ ] **Task 8:** Wire CRAL Router to evaluate session insights for M1-M7 qualification.
- [ ] **Task 9:** Implement Telegram client summary delivery format.

---

## 8. Acceptance Criteria

- [ ] **AC1 (End-to-End SLA):** Record a 30-minute test session via CCP Studio Block. Assert the Session Intelligence Report is delivered to AFFiNE and Telegram within 10 minutes of recording stop.
- [ ] **AC2 (Extraction Quality):** Review the extracted key insights for a known test session. Assert ≥80% of insights match human-identified key moments.
- [ ] **AC3 (Context Premise Update):** After session recap, query the client's Neo4j Context Premise. Assert new topic clusters from the session appear in the graph.
- [ ] **AC4 (CRAL Feed):** Include a statistically verifiable insight in a test session. Assert it appears in the CRAL Finding Index with source = "coaching_session".
- [ ] **AC5 (Mind Map Integrity):** Assert the generated `.excalidraw` JSON contains nodes for all extracted topic clusters and renders correctly in AFFiNE.
- [ ] **AC6 (Change Talk Detection):** Include client commitment language in test session. Assert it appears in the Change Talk Vault with correct DARN-CAT category.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR-CA11-16 (CCP Studio Block) | Internal | Triggers the pipeline on recording completion (replaces FR-CA11-13 OBS Controller). |
| NVIDIA NIM Whisper Container | Infrastructure | GPU-accelerated transcription. |
| FR29 (Aria / Context Premise Extraction) | Internal | Extended for session input. |
| FR-CBCS-01 (Change Talk Vault) | Internal | Receives breakthrough moments. |
| Benjamin (Excalidraw Composer) | Internal | Generates mind map. |
| `affine_sync.py` (FR-CA11-02) | Internal | Delivers to AFFiNE. |

---

## 10. Testing Strategy

### Unit Tests
- **Extraction Accuracy:** Pass a known transcript. Assert correct insights, action items, and topic clusters extracted.
- **Mind Map Structure:** Pass 5 topic clusters. Assert generated `.excalidraw` JSON has 1 central node + 5 branch nodes + correct edges.

### Integration Tests
- **Full Pipeline:** Upload a test recording → transcribe → extract → render mind map → push to AFFiNE → send Telegram summary. Assert all deliverables are correct.

### Performance Tests
- **SLA Verification:** Run the pipeline on 30-min, 60-min, and 90-min recordings. Assert all complete within 10, 15, and 20 minutes respectively.
