# Tech-Spec: FR61 — Jim Rohn AI Voice Coach Engine

**Created:** 2026-04-06
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0)
**Architecture Reference:** Jim_Rohn_AI_Voice_Coach_Communication_Framework.md (v3.0), The "Philosophical Resonance" Engine.md, CCP Architecture §10.1
**Skill Implementation:** `skills/ccf/coaching/rohn-voice-coach/SKILL.md`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\architecture\Jim_Rohn_AI_Voice_Coach_Communication_Framework.md` (v3.0)
- `d:\Work\The Conscious Coaching Factory\The _Philosophical Resonance_ Engine.md`
- `d:\Work\The Conscious Coaching Factory\docs\architecture\FR15_Scheduled_Monitor_Agent_Tech_Spec.md`
- `d:\Work\The Conscious Coaching Factory\docs\architecture\FR5_Trigger_Map_Builder_Tech_Spec.md`
- `d:\Work\The Conscious Coaching Factory\docs\architecture\FR2_Sacred_Audio_Ingestion_Tech_Spec.md`
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\The Jim Rohn Guides Complete.md`
- `d:\Work\The Conscious Coaching Factory\VoiceCoach Interactive Evidence-based Training for Voice.md`
- `d:\Work\The Conscious Coaching Factory\The Effect of Euphony in Persuasive Communication.md`
- `d:\Work\The Conscious Coaching Factory\Textual Paralanguage and Its Implications for Marketing Communications.md`
- `d:\Work\The Conscious Coaching Factory\Persuasive Natural Language Generation .md`

---

## 2. Overview

### Problem Statement

The CCF pipeline currently delivers provocation questions to coaches via **clinical text messages** (FR15 Stage 3: "I am seeing a lot of conversation in your community about X…"). The coach responds with a voice note that is processed through Sacred Audio (FR2). This flow works mechanically, but it produces **mask output** — the coach responds from a professional persona because the question format reads like a research debriefing, not a conversation with a mentor. The result is semantic synthesis, not episodic invocation.

Additionally, the system currently provides **zero feedback on the coach's vocal or visual delivery**. The coach records content and receives no coaching on how they spoke, how they looked on camera, whether they were sincere or performing, whether they paused effectively, or whether they improved since last session. Delivery coaching — the thing that separates a coach their audience trusts from one they scroll past — does not exist in the current pipeline.

### Solution

FR61 introduces the **Jim Rohn AI Voice Coach Engine** — a 2-phase coaching wrapper that sits between the CCF pipeline (FR15/FR5/FR2) and the coach. It:

1. **Rewrites FR15 provocation questions** into the Jim Rohn philosophical delivery register — antithetical, personally referenced from the HCD, and delivered as a TTS voice note in the Business Philosopher persona.
2. **Manages scheduled recording sessions** — calendar booking, 48h/24h/30min reminders, supportive script generation, multi-take video sessions (30-60 min).
3. **Provides biometric-level feedback on vocal AND visual delivery** — prosody analysis (OpenSMILE GeMAPS, librosa, Whisper timestamps), sincerity biometrics (jitter/shimmer + LIWC-22 cross-validation), video analysis (eye contact, gesture congruence, facial expression, posture), and persistent memory-aware micro-improvement acknowledgment.
4. **Teaches exclusively through post-performance feedback** — every piece of coaching references what the coach just did, what the data says, what their trajectory looks like, and the Rohn principle that explains why it matters.

### Scope

**In scope:**
- Stage 1: Rohn-style provocation question formatting and TTS voice note delivery (Phase 1 — Trigger)
- Stage 2: Coach voice note response intake, prosody extraction, story/contradiction extraction
- Stage 3: Supportive script generation from Phase 1 extracted material + RAG evidence
- Stage 4: Recording session booking, calendar integration, reminder pipeline
- Stage 5: Video intake, audio prosody analysis, video visual analysis
- Stage 6: Rohn-style feedback generation (vocal + visual), micro-improvement acknowledgment
- Stage 7: Supabase persistence, Redis session caching
- Receipt Chain Guard checks at each stage transition

**Out of scope:**
- The FR15 Scheduled Monitor Agent itself (upstream — provides the `tension_observation_object`)
- The FR5 Trigger Map Builder (upstream — provides `trigger_map.json`)
- The FR2 Sacred Audio Ingestion pipeline (parallel — still processes content independently)
- The downstream CCF/CMF production pipeline (consumes recording outputs)
- CosyVoice TTS model training (infrastructure — consumed as a service)
- Client-facing CBCS interactions (unchanged — uses coach's own Voice DNA)

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-005` | Trigger Profile | INPUT — The authenticated trigger from FR15 Stage 4, containing the cultural tension and coach response |
| `DEP-LIB-002` | Trigger Map | INPUT — Activation event selection for provocation question design |
| `DEP-ENG-023` | Cultural Memory Map | INPUT — Baseline for FR15 novelty assessment (upstream, not directly consumed) |
| `DEP-LIB-001` | Emotional DNA | INPUT — V1-V10 profile informs feedback tonality adaptation |
| `DEP-ENG-003` | Positive Space (Voice DNA) | INPUT — Coach's linguistic fingerprint used for script generation in their voice |
| `DEP-ENG-019` | Session Transcript Intelligence | OUTPUT — Enriched transcripts with prosody data feed back into FR5 activation history |
| `DEP-ENG-041` | Receipt Chain Guard | INFRASTRUCTURE — Non-negotiable sequence auditing at every stage |
| `NEW: vocal_delivery` | Vocal Delivery Metrics | OUTPUT — Supabase table containing per-session prosody biometrics |
| `NEW: video_delivery` | Video Delivery Metrics | OUTPUT — Supabase table containing per-recording visual analysis |
| `NEW: story_bank` | Extracted Story Bank | OUTPUT — Supabase table containing tagged stories from Phase 1 |
| `NEW: philosophy_tensions` | Contradiction Pairs | OUTPUT — Supabase table containing cross-session claim contradictions |
| `NEW: scheduled_sessions` | Session Calendar | OUTPUT — Supabase table containing booked recording sessions + reminder state |
| `NEW: scripts` | Supportive Scripts | OUTPUT — Supabase table containing generated recording prep scripts |

### Academic Research Grounding

| Component | Framework | Key Papers | Application in FR61 |
|---|---|---|---|
| Prosody analysis targets | VoiceCoach (Weber et al., 2023) | *VoiceCoach: Interactive Evidence-based Training for Voice Modulation* | SPM/WPM tracking, F0 variance targets, pause benchmarks from TED Talk analysis |
| Euphony in provocation phrasing | Euphonic Persuasion (Aryani et al., 2023) | *The Effect of Euphony in Persuasive Communication* | Alliteration/rhyme/homogeneity injection into Rohn-style provocation questions |
| Textual paralanguage in scripts | TPL (Luangrath et al., 2017) | *Textual Paralanguage and Its Implications for Marketing Communications* | Visual/auditory text cues in supportive scripts and Telegram text messages |
| NLG feedback quality | Persuasive NLG (Duerr & Gloor, 2021) | *Persuasive Natural Language Generation — A Literature Review* | Linguistic appropriacy, temporal overlap matching in feedback generation |
| Sincerity biometrics | Mehrabian (1967), Hochschild Emotional Labor (1983) | Mehrabian *Decoding of Inconsistent Communications*; Hochschild *The Managed Heart* | Jitter/shimmer as involuntary sincerity proxy; deep acting vs. surface acting detection |
| Cognitive reappraisal | Barrett Constructionist Theory (2017) | Barrett *How Emotions Are Made* | Fascination-frustration reframe in coach response processing |
| Strategic silence | Goldman-Eisler (1968), Duez (1982) | Goldman-Eisler *Psycholinguistics*; Duez *Silent and Non-Silent Pauses* | Rohn Pause detection (1.5-2.5s ISS after key statements) |
| Micro-improvement feedback | Hattie & Timperley (2007) | *The Power of Feedback* | Feedback most effective when specific, immediate, tied to observable behavior |
| Emotional loading | Russell Circumplex Model (1980), Scherer CPM (2001) | Russell *A Circumplex Model of Affect*; Scherer *Appraisal Considered as a Process* | Arousal/valence quadrant mapping — target: Low Arousal + High Valence ("philosopher's zone") |
| Narrative transportation | Green & Brock (2000) | *The Role of Transportation in the Persuasiveness of Public Narratives* | 3-Temporal Transport verb tense tracking (past:present:future target = 20:50:30) |

### Technical Decisions

| Decision | Rationale |
|---|---|
| **Supabase for persistent memory, Redis for session cache** | JSON files do not scale to 48 concurrent coaches with real-time metric ingestion. Supabase provides row-level security (coach isolation), real-time subscriptions for dashboard integration, and SQL joins for cross-session trend analysis. Redis caches the active session state for sub-100ms feedback generation latency. |
| **Phase 1 is extraction-only, not feedback** | Feedback during raw elicitation contaminates authenticity. The coach should rant freely. Prosody data is captured but feedback is withheld until the recording session prep or a dedicated follow-up voice note. This preserves the LIWC-22 authenticity signal for FR5 activation history. |
| **Recording sessions are booked, not ad-hoc** | Coaches who record "when they feel like it" produce inconsistent output. Scheduled sessions with prep materials create structure. 30-60 min max prevents quality degradation from fatigue. Multiple recordings per session (2-5 videos) match the weekly content batch volume. |
| **Supportive script uses coach's OWN language** | If the script is rewritten into "better" prose, the coach performs someone else's words on camera — surface acting (Hochschild). The script ARRANGES the coach's original phrases from Phase 1 into narrative arc order with evidence inserts, but does not rewrite them. |
| **Video analysis is session-phase only, not Phase 1** | Phase 1 is Telegram voice notes — no video. Video analysis only applies to Phase 2 recording sessions where the coach is on camera. |
| **Feedback as teaching, never upfront instruction** | Rohn's own method: never prescriptive before performance. The coach records, THEN receives observations. This maps to Ericsson's Deliberate Practice requirement: feedback must be tied to specific observable behavior, not abstract directives. |
| **CosyVoice TTS NOT Jim Rohn's actual voice** | Legal compliance — post-mortem publicity rights. Custom-trained on a licensed voice actor performing Business Philosopher delivery patterns (measured pace, antithesis rhythm, strategic pauses, warm baritone). |
| **ADR-01 Coach Isolation extends to all FR61 tables** | All Supabase tables enforce `coach_id` row-level security policies. No cross-coach data leakage. Redis keys are namespaced by `coach_id`. |

---

## 4. Implementation Plan

### Stage 1: Rohn-Style Provocation Question Formatting & TTS Delivery

*Agent Name:* Rohn-Voice-Coach-Agent
*Inputs:* `tension_observation_object` (from FR15 Stage 2), `trigger_map.json` activation event (from FR5), coach HCD state (from Supabase `story_bank`, `philosophy_tensions`, `vocal_delivery` tables).
*Outputs:* Rohn-style provocation voice note (.ogg) + TPL-enhanced text message, delivered to Telegram.
*Failure Condition:* Generated question does not contain at least 1 HCD personal reference AND 1 antithetical construction.

**Steps:**
1. Receive `tension_observation_object` from FR15 Stage 2 (cultural tension + source data + frequency delta).
2. Query Supabase for the coach's latest state:
   - `story_bank` — recent stories related to this topic cluster
   - `philosophy_tensions` — unresolved contradictions that map to this tension
   - `vocal_delivery` — latest session metrics for optional micro-improvement reference
   - `personal_philosophy.recurring_grievances` — chronic frustrations that connect to the detected tension
3. Load the matching activation event from `trigger_map.json` (FR5) — moral foundation, sensory anchors, mechanism description.
4. Generate the provocation question using the Rohn-Voice-Coach-Agent with strict formatting constraints:
   - **MUST** reference at least 1 item from the coach's HCD (a previous statement, a stored story, an unresolved tension)
   - **MUST** contain at least 1 antithetical construction (e.g., "not because X, but because Y")
   - **MUST** end with a specific, direct question that demands the coach choose a position
   - **MUST NOT** use prohibited AI assistant language ("I can help with that," "as an AI," "delve," "unlock," "game-changing")
   - **SHOULD** incorporate euphonic devices (alliteration, phonetic homogeneity) per the Persuasive Communication research. Extract the detected strings into the `euphony_devices` schema array.
   - **SHOULD** include textual paralanguage cues in the text version (e.g., *pauses*, emphasis markers, ellipses). Log these into the `tpl_markers` schema array.
5. Route the generated text to CosyVoice TTS service → produce .ogg voice note.
6. Deliver to coach via Telegram: voice note (primary) + TPL-enhanced text (reference).
7. Receipt Write: Per FR47 DEP-ENG-041 schema —
```json
{ "receipt_id": "RCP-{COACH_ACRONYM}-ROHN-PROVOCATION-{DATE}",
  "previous_receipt_hash": "{FR15_STAGE2_RECEIPT_HASH}",
  "input_payload_hash": "{TENSION_OBJ+HCD_STATE_HASH}",
  "output_payload_hash": "{VOICE_NOTE_HASH}",
  "stage_name": "STAGE-1-ROHN-PROVOCATION",
  "agent_name": "Rohn-Voice-Coach-Agent",
  "timestamp": "{ISO8601}" }
```

---

### Stage 2: Coach Response Intake & Multi-Layer Extraction

*Agent Name:* Rohn-Intake-Processor
*Inputs:* Coach Telegram voice note response, `tension_observation_object` context.
*Outputs:* Enriched response object → Supabase (`story_bank`, `philosophy_tensions`, `vocal_delivery`), `DEP-ENG-005` trigger profile (routed to CRAL).
*Failure Condition:* Voice note < 15 seconds OR coach explicitly opts out.

**Steps:**
1. Receive coach's voice note response via Telegram webhook.
2. **Audio processing (parallel):**
   - a. Route audio to Whisper NIM → word-level transcription with timestamps
   - b. Route audio to OpenSMILE → GeMAPS extraction (F0, jitter, shimmer, alpha ratio, HNR, spectral flux)
   - c. Route audio to librosa → tempo detection, SPM calculation, onset detection
   - d. Route audio to Wav2Vec 2.0 Emotion NIM → arousal/valence per segment
3. **Transcript processing (serial, after Whisper):**
   - a. LIWC-22 authenticity gate (7-factor scoring per FR2)
   - b. Story extraction — identify narrative passages (simile/metaphor density, temporal indicators, named entities, sensory detail score 0-10)
   - c. Contradiction detection — compare major claims against `philosophy_tensions` table + `personal_philosophy.core_beliefs` in Supabase
   - d. Topic clustering — tag extracted material against FR5 trigger categories
   - e. Temporal position classification — past/present/future verb tense ratio (LIWC-22)
4. **Specificity Ratchet Check:**
   - If the coach's response scores < 4/10 on sensory detail AND < 3 named entities: flag `needs_specificity_followup = true`.
   - Generate a follow-up voice note that pushes for concreteness: target the vaguest claim in the response and ask for a specific moment, person, or scene. Deliver as voice note.
   - Allow up to 2 follow-up ratchets per trigger cycle before accepting the material as-is.
5. **Supabase writes:**
   - `story_bank` — insert extracted stories with all metadata tags
   - `philosophy_tensions` — insert new contradiction pairs if detected
   - `vocal_delivery` — insert session prosody metrics
   - `sessions` — insert session record (type: `trigger`, depth_rating, emotional trajectory)
   - `personal_philosophy` — update core_beliefs reinforcement counts, add new grievances
6. **CRAL routing:** Pass the enriched response transcript and URL back to FR15's Telegram-Intake-Router. FR15 retains architectural ownership of combining the `tension_observation_object` with the response to map the standard `DEP-ENG-005` Trigger Profile for M2-M7 progression.
7. **No feedback delivered.** Phase 1 is extraction-only. Prosody data is stored, not surfaced.
8. Receipt Write: Per FR47 DEP-ENG-041 schema —
```json
{ "receipt_id": "RCP-{COACH_ACRONYM}-ROHN-INTAKE-{DATE}",
  "previous_receipt_hash": "{STAGE1_RECEIPT_HASH}",
  "input_payload_hash": "{VOICE_NOTE_HASH}",
  "output_payload_hash": "{SUPABASE_WRITES_HASH}",
  "stage_name": "STAGE-2-ROHN-INTAKE",
  "agent_name": "Rohn-Intake-Processor",
  "timestamp": "{ISO8601}" }
```

---

### Stage 3: Supportive Script Generation

*Agent Name:* Script-Composer-Agent
*Inputs:* `story_bank` entries from this week's Phase 1 extractions, RAG evidence from CRAL M2-M7 research, `DEP-ENG-003` (Voice DNA), 12 Narrative Arcs template.
*Outputs:* `scripts` table entry in Supabase, delivered to coach via Telegram.
*Failure Condition:* Script rewrites coach language instead of arranging it. Script exceeds 3 pages per recording piece. Script contains no pause markers.

**Steps:**
1. Query Supabase for all Phase 1 material from the current weekly cycle:
   - `story_bank` entries tagged to this week's trigger cycles
   - `philosophy_tensions` surfaced this week
   - `vocal_delivery` latest baselines (for pause marker calibration)
2. Receive CRAL research output (M2-M7) — the "pin" data: academic citations, statistics, historical parallels.
3. For each content piece in the weekly batch (typically 2-5 pieces):
   - a. **Select narrative arc** from the 12 Narrative Arcs based on the emotional trajectory of the extracted material (e.g., frustration → resolution = "The Epiphany"; warning + future risk = "The Warning").
   - b. **Arrange coach's original phrases** from Phase 1 transcripts into the arc structure. The script uses the coach's EXACT words — it does NOT rewrite them. It sequences them.
   - c. **Insert Pin Data:** Place CRAL evidence at structural anchor points — one data point per 90-second segment. Format: `[PIN: ICF 2024 study — 62% of coaches set fees below market rate]`.
   - d. **Insert Pause Markers:** Place `[PAUSE: 2s]` markers after every key claim (identified by sentiment intensity peaks in the Phase 1 prosody data). Calibrated to the coach's current pause capability from `vocal_delivery.avg_iss`.
   - e. **Apply Voice DNA filter:** Run the arranged script through the Voice DNA (DEP-ENG-003) compatibility check — ensure sentence structures match the coach's natural WPS flow, discourse marker patterns, and TTR range. Flag any lines that read as "not this coach."
4. Assemble the complete script document. Structure per content piece:
   ```
   RECORDING PIECE 1: [Title — from narrative arc]
   Narrative Arc: [Arc name]
   Estimated Duration: [60-180s]
   Script Type: ARRANGEMENT (not rewrite)
   
   [Coach's arranged phrases with PIN inserts and PAUSE markers]
   
   NOTE: Anything that doesn't sound like you — change it.
   This is YOUR material, arranged for flow.
   ```
5. Write to `scripts` table in Supabase.
6. Deliver to coach via Telegram — as a formatted text document + a brief voice note overview: "Three pieces for Thursday's session. The first one is the client retention rant from Tuesday, shaped into a 90-second philosophy piece. Read through them. Mark anything that doesn't sound like you."
7. Receipt Write: Per FR47 DEP-ENG-041 schema —
```json
{ "receipt_id": "RCP-{COACH_ACRONYM}-ROHN-SCRIPT-{DATE}",
  "previous_receipt_hash": "{STAGE2_RECEIPT_HASH}",
  "input_payload_hash": "{STORY_BANK+CRAL_EVIDENCE_HASH}",
  "output_payload_hash": "{SCRIPT_DOCUMENT_HASH}",
  "stage_name": "STAGE-3-ROHN-SCRIPT",
  "agent_name": "Script-Composer-Agent",
  "timestamp": "{ISO8601}" }
```

---

### Stage 4: Recording Session Booking & Reminder Pipeline

*Agent Name:* Session-Scheduler-Agent
*Inputs:* Coach availability preferences (from onboarding), weekly batch readiness signal.
*Outputs:* `scheduled_sessions` entry in Supabase, calendar event, 3 reminder voice notes.
*Failure Condition:* Session booked outside coach's availability window. Reminder pipeline fires after session has already occurred.

**Steps:**
1. **Session booking trigger:** When Stage 3 (Script Generation) completes for the weekly batch, the scheduler activates.
2. **Determine session slot:**
   - Read coach's configured availability from `coaches` table (e.g., "Thursdays 10:00-12:00 local time")
   - If no custom availability: default to 48h after script delivery, morning slot in coach's timezone
   - Write `scheduled_sessions` entry to Supabase with `status: booked`
3. **Calendar integration:** Push event to coach's connected calendar (Google Calendar API / CalDAV):
   - Title: "Recording Session — [Weekly Batch Theme]"
   - Duration: 60 minutes (default, coach-adjustable)
   - Description: "Recording session for this week's content. You'll receive your script 24h before. [N] pieces to record."
4. **Reminder pipeline (3-stage):**

   | Timing | Delivery | Content |
   |---|---|---|
   | **T-48h** | Voice note (Rohn persona) | "Your recording session is [DAY] at [TIME]. I've prepared a script based on what we talked about this week. I'll send it tomorrow so you have time to read through it." |
   | **T-24h** | Script delivery (text) + voice note overview | Full script document from Stage 3 + "Three recordings this session. Read through them. Mark anything that doesn't sound like you." |
   | **T-30min** | Voice note (Rohn persona) | "See you in 30 minutes. Camera on. Remember — don't try to perform. Just say it the way you said it to me on [DAY]." |

5. Update `scheduled_sessions` entry: `reminder_48h_sent`, `reminder_24h_sent`, `script_delivered`, `reminder_30min_sent` — each flagged with timestamp when delivered.
6. **No-show handling:** If no recording is received within 2 hours after scheduled time, send a gentle follow-up voice note: "I noticed you didn't make it to the session today. No pressure. Let me know if you want to reschedule for tomorrow." Update session status to `missed`. Log to `sessions` table.
7. Receipt Write: Per FR47 DEP-ENG-041 schema —
```json
{ "receipt_id": "RCP-{COACH_ACRONYM}-ROHN-SCHEDULE-{DATE}",
  "previous_receipt_hash": "{STAGE3_RECEIPT_HASH}",
  "input_payload_hash": "{AVAILABILITY+BATCH_READY_HASH}",
  "output_payload_hash": "{CALENDAR_EVENT_HASH}",
  "stage_name": "STAGE-4-ROHN-SCHEDULE",
  "agent_name": "Session-Scheduler-Agent",
  "timestamp": "{ISO8601}" }
```

---

### Stage 5: Recording Session — Video Intake & Multi-Modal Analysis

*Agent Name:* Recording-Session-Agent
*Inputs:* Video recordings (.mp4) from coach during scheduled session, `scripts` table context, `vocal_delivery` history from Supabase.
*Outputs:* Per-recording analysis objects → `vocal_delivery` + `video_delivery` tables in Supabase.
*Failure Condition:* Session exceeds 60 minutes without wrap signal. Video analysis returns no face-track (camera not on). Audio extraction fails.

**Steps:**
1. **Session opening (voice-based, 2-3 min):**
   - Agent sends a check-in voice note: "How are you feeling today? Before we start recording, let me know where your head is at."
   - Coach responds via voice note. System runs Wav2Vec emotion classification to establish session `emotional_baseline`.
   - **Adaptive calibration:** If coach is at high arousal / low valence (stressed, anxious): "You sound tight today. Let's start with the easiest piece — the client win story. Warm up on something that makes you smile." Re-order the recording sequence from the script.
2. **Script review confirmation (1-2 min):**
   - "Did you read through the scripts? Anything feel off? Anything you'd change before we roll?"
   - Coach confirms or flags changes. Script changes logged to `scripts` table.
3. **Recording cycle (per video, 2-5 videos per session):**

   For each video recording:

   **3a. Coach records video.**
   Video file (.mp4) received via Telegram or direct upload.

   **3b. Audio extraction and prosody analysis (parallel):**
   - Extract audio track → 16kHz Mono WAV (FFmpeg)
   - Whisper NIM → word-level transcription with timestamps
   - OpenSMILE GeMAPS → F0 (pitch + variance), jitter, shimmer, alpha ratio, HNR
   - librosa → SPM, tempo, onset detection
   - Wav2Vec Emotion → arousal/valence per 5-second segment
   - LIWC-22 → authenticity score, hedging density, pronoun ratios, verb tense distribution
   - **Computed metrics:**
     - WPM = total words / duration in minutes
     - SPM = estimated syllables / duration in minutes
     - Rohn Pause count = ISS events between 1.5-2.5 seconds following key statements (identified by sentiment intensity peaks)
     - Pin-Iron-Bar ratio = (entity_count + citation_count) / emotional_loading_score
     - Sincerity composite = f(LIWC_authenticity, jitter_stability, shimmer_stability)
     - Filler density = filler_count / total_words

   **3c. Video visual analysis (parallel with audio):**
   - **Eye contact stability:** Vision model tracks gaze direction frame-by-frame against camera lens position. Output: percentage of recording time with direct camera eye contact + timestamps of gaze breaks > 1 second.
   - **Gesture congruence:** Gesture detection model identifies hand/arm movement patterns. Cross-reference movement frequency with speech emphasis points from the prosody pipeline. Output: congruence score (0-10) — high if gestures align with content emphasis, low if frozen or random.
   - **Facial expression analysis:** Facial landmark detection → emotion classification per 2-second window. Cross-reference with audio emotion classification. Output: face-voice congruence score — high if facial emotion aligns with vocal emotion, low if mismatched (e.g., voice says calm, face says stress).
   - **Posture tracking:** Upper body pose estimation. Track forward lean (conviction signal) vs. backward lean (retreat signal) mapped to content segments. Output: posture engagement map with timestamps.

   **3d. Write analysis to Supabase:**
   - `vocal_delivery` — insert per-recording prosody metrics
   - `video_delivery` — insert per-recording visual analysis metrics

   **3e. Generate Rohn-style feedback (Stage 6) and deliver between takes.**

4. **Session wrap (2-3 min, after final recording):**
   - Summarize what was captured: "[N] clean recordings. Total session time: [MM:SS]."
   - Pull micro-improvements from `micro_improvements` table (see Stage 6).
   - Acknowledge improvements FIRST, then give one forward-looking direction: "Next week we're pulling on the pricing tension you've been avoiding. Start thinking about it."
   - Update `sessions` table: type = `recording`, `session_completed = true`, final depth rating, emotional trajectory.
5. **Session time enforcement:** If session reaches 55 minutes without all recordings complete, agent intervenes: "We're at 55 minutes. Let's wrap the last take clean and save the remaining piece for next session." This prevents quality degradation from fatigue.
6. Receipt Write: Per FR47 DEP-ENG-041 schema —
```json
{ "receipt_id": "RCP-{COACH_ACRONYM}-ROHN-RECORDING-{DATE}",
  "previous_receipt_hash": "{STAGE4_RECEIPT_HASH}",
  "input_payload_hash": "{ALL_VIDEO_FILES_HASH}",
  "output_payload_hash": "{ANALYSIS_RESULTS_HASH}",
  "stage_name": "STAGE-5-ROHN-RECORDING",
  "agent_name": "Recording-Session-Agent",
  "timestamp": "{ISO8601}" }
```

---

### Stage 6: Rohn-Style Feedback Generation & Micro-Improvement Acknowledgment

*Agent Name:* Rohn-Feedback-Agent
*Inputs:* Analysis results from Stage 5 (vocal + visual), coach HCD history from Supabase, Rohn Communication Framework delivery register.
*Outputs:* Voice note feedback (.ogg) delivered after each recording take. `micro_improvements` table updates.
*Failure Condition:* Feedback contains raw metric dumps without Rohn-style philosophical framing. Feedback references no HCD history. Feedback uses prohibited AI assistant language.

**Steps:**

1. **Micro-Improvement Detection:**
   - Query `vocal_delivery` table for previous session metrics (same coach_id, ordered by date DESC).
   - For each metric, calculate delta: `(current - previous) / previous * 100`.
   - If any metric improved by ≥ 5%: insert to `micro_improvements` table with `acknowledged = false`.
   - If multiple metrics improved: prioritize acknowledgment by improvement magnitude.

2. **Feedback Generation (per recording take):**

   The feedback is generated by the Rohn-Feedback-Agent with the following strict constraints:

   **Structure — Every feedback message contains exactly 4 elements:**
   - **Element 1 — Micro-Improvement Acknowledgment (if applicable):** Data-backed, specific, delivered BEFORE any critique. References the coach's trajectory.
   - **Element 2 — Strongest Moment:** Identify the single most effective moment in the recording (highest sincerity composite, best Rohn Pause, strongest eye contact, most congruent gesture). Describe it with timestamp. Explain WHY it worked using a Rohn principle.
   - **Element 3 — One Growth Area:** Identify the single most impactful thing the coach could improve in the NEXT take. Not a list of problems — ONE thing. Describe the specific moment (with timestamp) where it happened. Explain the impact using Rohn antithesis framing. Offer a concrete action for the re-take.
   - **Element 4 — Forward Reference:** Connect this session to the coach's trajectory. Use 3-Temporal Transport: where they were (past data), where they are (today's data), where this is heading (projected trajectory).

   **Delivery Register (Rohn Constraints):**
   - MUST use antithesis in every feedback ("Not X — Y")
   - MUST reference at least 1 previous session data point from the HCD
   - MUST tie every metric to a Rohn philosophical principle (never raw numbers without context)
   - MUST use "Let's" framing for growth suggestions, never "You need to"
   - MUST NOT exceed 60 seconds when synthesized as voice note
   - MUST NOT use prohibited words: "I can help with that," "as an AI," "delve," "unlock," "game-changing"
   - SHOULD include 1 Rohn direct quotation per session (e.g., "Jim Rohn once said...")

   **Example feedback (synthesized as voice note between takes):**

   > "Before we go to the next piece — your filler density dropped from 3.4% to 2.1% since last session. That's a 38% improvement. You didn't notice it because you were focused on the content. But the audience will notice because they'll feel more confident in you. That's what Rohn called the discipline of the master — it doesn't show after one day.
   >
   > The strongest moment was at 34 seconds. You said 'the real cost isn't the money — it's the time they'll never get back.' Then you paused for 2.3 seconds. That was the most powerful moment in the recording. That silence is where your audience processes.
   >
   > One thing for the next take. At the 22-second mark, you looked away from the camera right when you said the most important line. Your voice was there — steady, convicted. But your eyes left. Let's try it again — and this time, lock into the lens when you hit that line. Eyes to camera. Let the words and the eyes arrive together.
   >
   > Three weeks ago your sincerity composite was a 5.2. Today it's 7.1. If you keep this trajectory, by the end of the quarter your audience won't just hear information — they'll feel a leader."

3. Route generated text to CosyVoice TTS → .ogg voice note.
4. Deliver via Telegram between recording takes.
5. Update `micro_improvements` entries: `acknowledged = true`.
6. Receipt Write: Per FR47 DEP-ENG-041 schema —
```json
{ "receipt_id": "RCP-{COACH_ACRONYM}-ROHN-FEEDBACK-{DATE}-{TAKE_N}",
  "previous_receipt_hash": "{STAGE5_RECEIPT_HASH}",
  "input_payload_hash": "{ANALYSIS+HCD_HASH}",
  "output_payload_hash": "{FEEDBACK_VOICE_NOTE_HASH}",
  "stage_name": "STAGE-6-ROHN-FEEDBACK",
  "agent_name": "Rohn-Feedback-Agent",
  "timestamp": "{ISO8601}" }
```

---

### Stage 7: Supabase Persistence & Redis Session Management

*Agent Name:* HCD-Persistence-Service (not an LLM agent — a data service)
*Inputs:* All outputs from Stages 1-6.
*Outputs:* Durable state in Supabase, ephemeral state in Redis, downstream signals to FR5 feedback loop.

**Supabase Schema:**

```sql
-- Coach identity and program state
CREATE TABLE coaches (
  coach_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id TEXT UNIQUE NOT NULL,
  onboard_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  total_sessions INTEGER DEFAULT 0,
  active_program_tier TEXT DEFAULT 'full_program',
  availability_config JSONB DEFAULT '{}',
  timezone TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Extracted stories from Phase 1 voice notes
CREATE TABLE story_bank (
  story_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  coach_id UUID REFERENCES coaches(coach_id) NOT NULL,
  session_id UUID REFERENCES sessions(session_id),
  date_extracted TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  raw_transcript TEXT NOT NULL,
  topic_tags TEXT[] DEFAULT '{}',
  trigger_category_id TEXT,
  emotion_arousal FLOAT,
  emotion_valence FLOAT,
  narrative_arc TEXT,
  temporal_position TEXT CHECK (temporal_position IN ('past','present','future')),
  sensory_detail_score FLOAT CHECK (sensory_detail_score BETWEEN 0 AND 10),
  times_used_in_content INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Contradiction pairs detected across sessions
CREATE TABLE philosophy_tensions (
  tension_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  coach_id UUID REFERENCES coaches(coach_id) NOT NULL,
  claim_a_text TEXT NOT NULL,
  claim_a_session_date TIMESTAMPTZ NOT NULL,
  claim_b_text TEXT NOT NULL,
  claim_b_session_date TIMESTAMPTZ NOT NULL,
  resolved BOOLEAN DEFAULT FALSE,
  resolution_text TEXT,
  resolution_date TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Assembled personal philosophy
CREATE TABLE personal_philosophy (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  coach_id UUID REFERENCES coaches(coach_id) UNIQUE NOT NULL,
  core_beliefs JSONB DEFAULT '[]',
  unresolved_questions JSONB DEFAULT '[]',
  recurring_grievances JSONB DEFAULT '[]',
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Per-session prosody metrics (Phase 1 + Phase 2)
CREATE TABLE vocal_delivery (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID REFERENCES sessions(session_id) NOT NULL,
  recording_id UUID,
  coach_id UUID REFERENCES coaches(coach_id) NOT NULL,
  wpm FLOAT,
  spm FLOAT,
  pitch_variance FLOAT,
  avg_iss FLOAT,
  rohn_pauses_detected INTEGER DEFAULT 0,
  filler_density FLOAT,
  sincerity_composite FLOAT,
  liwc_authenticity FLOAT,
  jitter FLOAT,
  shimmer FLOAT,
  emotional_loading_arousal FLOAT,
  emotional_loading_valence FLOAT,
  pin_iron_ratio FLOAT,
  measured_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Per-recording video visual analysis (Phase 2 only)
CREATE TABLE video_delivery (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  recording_id UUID NOT NULL,
  session_id UUID REFERENCES sessions(session_id) NOT NULL,
  coach_id UUID REFERENCES coaches(coach_id) NOT NULL,
  eye_contact_pct FLOAT,
  gaze_break_timestamps JSONB DEFAULT '[]',
  gesture_congruence_score FLOAT,
  facial_expression_congruence FLOAT,
  posture_engagement_map JSONB DEFAULT '[]',
  analyzed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Session log
CREATE TABLE sessions (
  session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  coach_id UUID REFERENCES coaches(coach_id) NOT NULL,
  session_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  session_type TEXT CHECK (session_type IN ('trigger','recording')) NOT NULL,
  duration_minutes INTEGER,
  depth_rating INTEGER CHECK (depth_rating BETWEEN 1 AND 5),
  emotional_baseline_arousal FLOAT,
  emotional_baseline_valence FLOAT,
  emotional_trajectory TEXT CHECK (emotional_trajectory IN ('ascending','stable','descending')),
  recordings_count INTEGER DEFAULT 0,
  questions_asked JSONB DEFAULT '[]',
  stories_extracted UUID[] DEFAULT '{}',
  contradictions_surfaced UUID[] DEFAULT '{}',
  topics_covered TEXT[] DEFAULT '{}',
  session_completed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Scheduled recording sessions with reminder state
CREATE TABLE scheduled_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID REFERENCES sessions(session_id),
  coach_id UUID REFERENCES coaches(coach_id) NOT NULL,
  scheduled_datetime TIMESTAMPTZ NOT NULL,
  duration_minutes INTEGER DEFAULT 60,
  batch_theme TEXT,
  recordings_planned INTEGER DEFAULT 0,
  reminder_48h_sent TIMESTAMPTZ,
  reminder_24h_sent TIMESTAMPTZ,
  script_delivered TIMESTAMPTZ,
  reminder_30min_sent TIMESTAMPTZ,
  status TEXT CHECK (status IN ('booked','confirmed','in_progress','completed','missed','rescheduled')) DEFAULT 'booked',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Supportive scripts for recording sessions
CREATE TABLE scripts (
  script_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID REFERENCES scheduled_sessions(id),
  coach_id UUID REFERENCES coaches(coach_id) NOT NULL,
  content_pieces JSONB NOT NULL DEFAULT '[]',
  pause_markers JSONB DEFAULT '[]',
  pin_data_points JSONB DEFAULT '[]',
  raw_coach_phrases_used TEXT[] DEFAULT '{}',
  voice_dna_compatibility_score FLOAT,
  delivered_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Micro-improvement detections pending acknowledgment
CREATE TABLE micro_improvements (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  coach_id UUID REFERENCES coaches(coach_id) NOT NULL,
  metric_name TEXT NOT NULL,
  previous_value FLOAT NOT NULL,
  current_value FLOAT NOT NULL,
  delta_pct FLOAT NOT NULL,
  session_id UUID REFERENCES sessions(session_id),
  acknowledged BOOLEAN DEFAULT FALSE,
  acknowledged_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Row Level Security (ADR-01 Coach Isolation)
ALTER TABLE story_bank ENABLE ROW LEVEL SECURITY;
ALTER TABLE philosophy_tensions ENABLE ROW LEVEL SECURITY;
ALTER TABLE personal_philosophy ENABLE ROW LEVEL SECURITY;
ALTER TABLE vocal_delivery ENABLE ROW LEVEL SECURITY;
ALTER TABLE video_delivery ENABLE ROW LEVEL SECURITY;
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE scheduled_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE scripts ENABLE ROW LEVEL SECURITY;
ALTER TABLE micro_improvements ENABLE ROW LEVEL SECURITY;

-- Policy: coach can only access their own data
CREATE POLICY coach_isolation ON story_bank
  USING (coach_id = current_setting('app.current_coach_id')::UUID);
-- (Repeat for all tables above)
```

**Redis Session Cache:**

| Key Pattern | TTL | Content |
|---|---|---|
| `session:{coach_id}:active` | 90 min | Current session state: emotional baseline, active script, recording count, running metrics |
| `session:{coach_id}:prosody_buffer` | 90 min | In-progress prosody metrics for current recording (flushed to Supabase on recording completion) |
| `provocation:{coach_id}:pending` | 12 h | Active provocation question awaiting coach response (expires if no response) |
| `schedule:{coach_id}:reminders` | 72 h | Reminder pipeline state (which reminders sent, scheduled times) |

**FR5 Feedback Signal:**
After each recording session, emit a webhook to the FR5 Weekly Pipeline Stage 5 (Trigger Architecture Update) containing:
- `trigger_id` used for this week's content
- LIWC-22 authenticity score from the recording (not Phase 1 — the final polished recording)
- Session `sincerity_composite`

This feeds back into `activation_history` for trigger precedence updates.

---

## 5. Primary Output Schemas

### Provocation Question Output (Stage 1)

```json
{
  "provocation_id": "PROV-20260406-001",
  "coach_tenant_id": "coach_88ab",
  "trigger_source": {
    "fr15_tension_id": "TENSION-20260406-003",
    "fr5_trigger_id": "TRG-001",
    "topic_cluster": "client_retention"
  },
  "hcd_references": [
    {
      "type": "previous_statement",
      "source_session": "SES-20260330-002",
      "quote": "my biggest fear is coaching someone who doesn't change"
    }
  ],
  "generated_question": {
    "text": "There's something happening in your space right now...",
    "antithesis_count": 2,
    "euphony_devices": ["alliteration: 'confusing...coaching...clients'"],
    "tpl_markers": ["*pauses*", "emphasis: REVENUE or CONFIDENCE"]
  },
  "voice_note_url": "s3://private-bucket/voice-notes/PROV-20260406-001.ogg",
  "delivered_at": "2026-04-06T08:00:00Z"
}
```

### Recording Session Analysis Output (Stage 5)

```json
{
  "session_id": "SES-20260410-001",
  "coach_tenant_id": "coach_88ab",
  "session_type": "recording",
  "duration_minutes": 42,
  "recordings": [
    {
      "recording_id": "REC-001",
      "script_piece_title": "The Real Cost of Client Churn",
      "narrative_arc": "The Epiphany",
      "duration_seconds": 94,
      "vocal_analysis": {
        "wpm": 128,
        "spm": 185,
        "pitch_variance_f0": 0.58,
        "rohn_pauses": 2,
        "filler_density": 0.021,
        "sincerity_composite": 7.1,
        "emotional_loading": {"arousal": 0.35, "valence": 0.72},
        "pin_iron_ratio": 0.45
      },
      "video_analysis": {
        "eye_contact_pct": 0.82,
        "gesture_congruence": 7.5,
        "facial_expression_congruence": 8.1,
        "posture_notes": [
          {"timestamp": 22, "observation": "forward_lean", "content_match": "key_claim"},
          {"timestamp": 67, "observation": "backward_lean", "content_match": "pricing_statement"}
        ]
      },
      "micro_improvements_detected": [
        {"metric": "filler_density", "previous": 0.034, "current": 0.021, "delta_pct": -38.2}
      ]
    }
  ],
  "session_emotional_trajectory": "ascending",
  "session_depth_rating": 4
}
```

---

## 6. Backward Compatibility Fallback

If FR61 is not deployed or encounters failure, the system gracefully degrades:

1. **FR15 continues to send clinical text-format provocation questions** — no Rohn rewrite, no voice note. Coach still receives the prompt and responds.
2. **FR2 Sacred Audio processes the voice note as before** — content extraction, LIWC-22 gate, Thought Unit segmentation. No prosody feedback.
3. **No recording session management** — coach records whenever, no script, no reminders, no video analysis.
4. **No micro-improvement tracking** — HCD is not populated. Every session resets.
5. **Downstream CCF/CMF pipeline is unaffected** — it receives `DEP-ENG-005` trigger profiles and raw recordings regardless of whether FR61 is active.

**Exit from fallback:** When FR61 services are deployed and Supabase tables are initialized, the system begins enriching FR15 Stage 3 output with Rohn rewrites and activates the recording session pipeline. No migration needed — the first session creates the coach's baseline.

---

## 7. Tasks

- [ ] **Task 1 (Stage 1):** Implement the Rohn-Voice-Coach-Agent provocation question formatter — HCD query from Supabase, antithesis injection, euphony device insertion, TTS routing to CosyVoice.
- [ ] **Task 2 (Stage 1):** Integrate Rohn-style prompt formatting as a post-processor for FR15 Stage 3 output. Maintain backward compatibility if FR61 agent is unavailable.
- [ ] **Task 3 (Stage 2):** Implement multi-layer extraction pipeline — parallel audio processing (OpenSMILE + librosa + Whisper + Wav2Vec), serial transcript processing (LIWC-22 + story extraction + contradiction detection).
- [ ] **Task 4 (Stage 2):** Implement the Specificity Ratchet — sensory detail scoring, auto-generated follow-up voice notes for vague responses, 2-ratchet limit per trigger cycle.
- [ ] **Task 5 (Stage 3):** Implement Script-Composer-Agent — narrative arc selection, coach phrase arrangement (NOT rewrite), Pin Data insertion, Pause Marker calibration, Voice DNA compatibility check.
- [ ] **Task 6 (Stage 4):** Implement Session-Scheduler-Agent — availability parsing, calendar API integration (Google Calendar / CalDAV), 3-stage reminder voice note pipeline, no-show handling.
- [ ] **Task 7 (Stage 5):** Implement audio extraction and prosody pipeline for video recordings — FFmpeg audio extraction, parallel OpenSMILE + librosa + Whisper + Wav2Vec + LIWC-22 processing.
- [ ] **Task 8 (Stage 5):** Implement video visual analysis pipeline — eye contact tracking (gaze vs. camera lens), gesture congruence scoring, facial expression cross-validation with audio emotion, posture lean mapping.
- [ ] **Task 9 (Stage 5):** Implement session lifecycle management — opening check-in, adaptive calibration from emotional baseline, script review confirmation, session time enforcement (55-min warning).
- [ ] **Task 10 (Stage 6):** Implement Rohn-Feedback-Agent — 4-element feedback structure, micro-improvement detection (≥5% delta), Rohn delivery register constraints (antithesis, HCD reference, principle linking, "Let's" framing), TTS routing.
- [ ] **Task 11 (Stage 7):** Implement Supabase schema — all 10 tables, Row Level Security policies, coach_id isolation enforcement.
- [ ] **Task 12 (Stage 7):** Implement Redis session cache — 4 key patterns, TTL management, flush-to-Supabase on session completion.
- [ ] **Task 13 (Stage 7):** Implement FR5 feedback signal — emit trigger_id + LIWC-22 score + sincerity_composite to FR5 Weekly Pipeline Stage 5 after recording session completion.
- [ ] **Task 14 (Cross-Stage):** Inject Receipt Chain Guard writes at all 7 stages. Enforce ADR-01 Coach Graph Isolation across all Supabase queries and Redis key namespacing.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Rohn Provocation Quality):** A provocation question generated by Stage 1 contains: (a) ≥1 reference to the coach's previous statement from Supabase, (b) ≥1 antithetical construction, (c) a specific closing question that demands a position. *Failure Example:* The agent generates "I am seeing a lot of conversation in your community about client retention. Does this connect to something you've been thinking about?" — this is the clinical FR15 format, not the Rohn rewrite.
- [ ] **AC2 (Phase 1 No-Feedback Enforcement):** During Phase 1 (trigger response), the system stores prosody data to `vocal_delivery` but does NOT deliver feedback to the coach. *Failure Example:* After the coach sends a trigger response voice note, the system immediately responds with "Your WPM was 155, which is above target." This contaminates the authenticity of the raw extraction.
- [ ] **AC3 (Script Arrangement, Not Rewrite):** The supportive script generated in Stage 3 uses the coach's exact phrases from Phase 1 transcripts. The script arranges them into narrative arc order with Pin Data and Pause Markers but does NOT rewrite the language. *Failure Example:* Coach said "my clients are scared to charge what they're worth." Script rewrites this to "many professionals undervalue their services in competitive markets." The coach's language has been replaced.
- [ ] **AC4 (Recording Session Time Enforcement):** A session that reaches 55 minutes triggers a wrap warning. A session cannot exceed 60 minutes total. *Failure Example:* Session runs 78 minutes because the agent kept asking for more takes without enforcing the time limit.
- [ ] **AC5 (Multi-Video Session):** A recording session successfully processes 4 separate video recordings, each with independent vocal_delivery and video_delivery analysis rows in Supabase. *Failure Example:* System treats the entire session as one video — prosody metrics are averaged across all 4 takes instead of tracked individually.
- [ ] **AC6 (Micro-Improvement Detection):** When a coach's filler_density drops from 0.034 to 0.021 between sessions, the system: (a) inserts a `micro_improvements` row with delta_pct = -38.2, (b) includes this in the feedback BEFORE any critique in the next session. *Failure Example:* The improvement is detected but the feedback opens with critique: "Your eye contact dropped at the 22-second mark."
- [ ] **AC7 (Reminder Pipeline Ordering):** The 3-stage reminder pipeline fires in order: T-48h voice note → T-24h script delivery + voice note → T-30min voice note. Each marks its completion timestamp in `scheduled_sessions`. *Failure Example:* Script is delivered at T-48h instead of T-24h, giving the coach too much time (or script arrives on session day without prep time).
- [ ] **AC8 (Video Analysis — No Camera):** If the video recording contains no detectable face track (camera off, screen share, or audio-only), the system: (a) skips video_delivery analysis, (b) still processes audio prosody, (c) flags `video_analysis_available = false` on the recording. *Failure Example:* System throws an error and fails to process the recording because face detection returned null.
- [ ] **AC9 (ADR-01 Supabase Isolation):** Coach_A's Supabase queries return zero rows from Coach_B's data across all 10 tables. Row Level Security policies enforced at the database level. *Failure Example:* A cross-coach pattern detection query accidentally returns another coach's story_bank entries.
- [ ] **AC10 (Rohn Feedback Register):** Every feedback voice note generated by Stage 6: (a) contains antithesis, (b) references ≥1 HCD data point, (c) ties the metric to a Rohn principle, (d) uses "Let's" framing for growth suggestions. (e) does NOT contain prohibited words. *Failure Example:* "Your WPM is 152. You should try to slow down to 120. I can help you with that." — raw metric dump, "You should" framing, prohibited phrase.
- [ ] **AC11 (FR5 Feedback Loop):** After a recording session completes, a webhook fires to FR5 Weekly Pipeline Stage 5 containing the trigger_id, LIWC-22 authenticity score, and sincerity_composite. *Failure Example:* Recording session completes but no feedback signal is emitted — FR5 activation_history never updates, trigger precedence stagnates.
- [ ] **AC12 (Backward Compatibility):** If FR61 services are down, FR15 continues to deliver clinical text prompts. FR2 continues to process voice notes. No downstream pipeline breaks. *Failure Example:* FR15 Stage 3 fails because it tries to route through the unavailable Rohn rewrite service and has no fallback path.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR15 Scheduled Monitor Agent | Upstream | Provides `tension_observation_object` — the cultural tension that drives the provocation question |
| FR5 Trigger Map Builder | Upstream | Provides `trigger_map.json` — activation events matched to the cultural tension |
| FR2 Sacred Audio Ingestion | Parallel | Still processes voice notes independently for content pipeline. FR61 adds prosody extraction as a parallel branch. |
| FR3 Voice DNA Extraction | Input | `DEP-ENG-003` used for script compatibility check (Stage 3) |
| FR4 Emotional DNA Extraction | Input | `DEP-LIB-001` V1-V10 profile informs feedback tonality adaptation |
| CosyVoice TTS Service | Infrastructure | Synthesizes Rohn-style voice notes. NIM container on AWS. |
| OpenSMILE GeMAPS | Infrastructure | F0, jitter, shimmer, alpha ratio, HNR extraction |
| librosa | Infrastructure | SPM, tempo, onset detection |
| Whisper NIM | Infrastructure | Word-level transcription with timestamps |
| Wav2Vec 2.0 Emotion NIM | Infrastructure | Arousal/valence classification per segment |
| LIWC-22 | License | Authenticity scoring, verb tense distribution, pronoun analysis |
| Supabase | Infrastructure | Persistent storage for all FR61 tables |
| Redis | Infrastructure | Session-level ephemeral cache |
| Google Calendar API / CalDAV | Infrastructure | Recording session booking and reminders |
| Vision Model (face/pose/gaze) | Infrastructure | Video visual analysis — eye contact, gesture, facial expression, posture |
| Receipt Chain Guard (DEP-ENG-041, FR47) operating under Protocol DEP-PROTO-010 (FR21) | Infrastructure | Non-negotiable sequence auditing |
| Telegram Bot API | Infrastructure | Voice note delivery and intake |

---

## 10. Testing Strategy

### Unit Tests
- **Provocation formatting:** Feed a mock `tension_observation_object` + mock HCD state. Assert output contains ≥1 HCD reference, ≥1 antithesis, and a closing question. Assert zero prohibited words.
- **Specificity Ratchet:** Feed a mock transcript scoring 2/10 sensory detail. Assert `needs_specificity_followup = true`. Feed a transcript scoring 7/10. Assert no follow-up triggered.
- **Script arrangement vs. rewrite:** Feed mock coach phrases + mock CRAL evidence. Assert output script contains the EXACT original phrases (string match), not paraphrases. Assert Pin Data is present. Assert ≥1 Pause Marker per content piece.
- **Micro-improvement detection:** Feed two mock `vocal_delivery` rows (current vs. previous). Current filler_density = 0.021, previous = 0.034. Assert delta_pct = -38.2 and improvement is flagged.
- **Feedback register validation:** Feed mock analysis + HCD. Assert feedback output contains antithesis (regex check for "not X — Y" pattern), HCD reference, Rohn principle, "Let's" framing. Assert zero prohibited words.
- **Session time enforcement:** Mock a session at 56 minutes elapsed with 1 recording remaining. Assert wrap warning is triggered.

### Integration Tests
- **Full Phase 1 flow:** Trigger FR15 Stage 2 mock → Rohn rewrite → TTS generation → Telegram delivery → mock coach voice note response → multi-layer extraction → Supabase writes. Assert all tables populated correctly.
- **Full Phase 2 flow:** Script generation from Supabase Phase 1 data → session booking → reminder pipeline (verify 3 reminders in correct sequence) → mock video upload → audio + video analysis → feedback generation with micro-improvement ACK → Supabase writes. Assert all analysis rows created, micro-improvements acknowledged, FR5 feedback signal emitted.
- **Multi-video session:** Upload 4 mock videos in a single session. Assert 4 separate `vocal_delivery` rows, 4 separate `video_delivery` rows, 4 separate feedback voice notes, 1 session wrap summary.
- **Calendar integration:** Book a session via Stage 4. Assert calendar event created in mock Google Calendar. Assert reminder pipeline fires at correct offsets (T-48h, T-24h, T-30min). Assert no-show detected if no recording received within 2h.

### Safety Tests (ADR-01 & Coach Isolation)
- **Supabase RLS enforcement:** Create Coach_A and Coach_B with populated tables. Set `app.current_coach_id` to Coach_A. Run a SELECT on every table. Assert zero rows from Coach_B in all results.
- **Redis key isolation:** Set session cache for Coach_A and Coach_B. Query `session:coach_a_id:active`. Assert Coach_B data is not returned. Assert key namespace enforces coach_id prefix.
- **Cross-coach pattern detection quarantine:** Verify that the story_bank query in Stage 1 (HCD reference loading) ONLY returns rows for the current coach. Even if a cross-coach trend is mentioned in the framework document, the implementation must NOT query other coaches' data.
