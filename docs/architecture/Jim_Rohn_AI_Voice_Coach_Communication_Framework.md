# The Jim Rohn AI Voice Coach — Communication Framework

**Version:** 3.0 — Active Coaching Engine Specification  
**Scope:** System-to-Coach private Telegram channel only  
**Constraint:** 48 coaches maximum, zero public distribution  
**Persistent Memory:** Supabase (primary) + Redis (session cache)  
**Date:** April 2026

---

## 1. What This System Actually Is

This system is the **bridge between the CCF content pipeline and the coach**. It is not a freestanding philosophical mentor. It is not a therapy bot. It does not invent topics. The CCF weekly content batch decides **what** the coach talks about. The Jim Rohn Communication Framework decides **how** that conversation is conducted — so the coach *expresses* instead of *impresses*.

The system operates in two distinct phases, both driven by the existing CCF pipeline:

**Phase 1 — The Trigger (Voice-Based, Telegram)**  
The Scheduled Monitor Agent (FR15) detects a cultural tension, the Trigger Map (FR5) selects the activation event, and the AI sends a provocative question as a Rohn-style voice note. The coach responds with a voice note. This is the elicitation — raw, emotional, unpolished. The system extracts stories, positions, and emotional signatures from this exchange.

**Phase 2 — The Recording Session (Video, Scheduled)**  
The coach records the polished content as video. This is a booked session — 30 to 60 minutes, in the calendar, with gentle reminders. The coach receives a supportive script beforehand. A session may contain multiple video recordings. The AI analyzes both the audio AND the video, providing personalized feedback after each take.

Everything the AI "teaches" arrives as **feedback after performance** — never as upfront instruction. The coach performs first. The system observes. Then the feedback arrives, wrapped in Rohn's philosophical language, tied to the coach's own biometric data and historical trajectory. It feels personalized because it IS personalized — it references their previous sessions, their specific metrics, their exact words.

---

## 2. Phase 1 — The Trigger: Provocation via Jim Rohn Voice

### 2.1 Where the Questions Come From

The questions are NOT random philosophical prompts. They originate from the CCF content pipeline:

1. **FR15 Scheduled Monitor Agent** fires on its daily cron. It scrapes the coach's tribal community discourse and checks the `semantic_affinity` table for rising audience domains.
2. If a cultural tension exceeds the 15% novelty spike threshold against the Cultural Memory Map (DEP-ENG-023), it generates a `tension_observation_object`.
3. The Trigger Map (FR5) selects the optimal activation event — the specific moral violation and sensory anchor from the coach's `trigger_map.json` that has the highest structural match with the detected tension.
4. **The Jim Rohn Voice Coach formats this into a provocation question.** This is where the Rohn framework enters. The question is NOT the FR15 default 3-part structure ("I am seeing a lot of conversation in your community about X..."). Instead, it is rewritten in Rohn's style.

**FR15 Default (clinical):**
> "I am seeing a lot of conversation in your community about client retention struggles. Three practitioners I tracked are taking these positions: [summary]. Does this connect to something you have been thinking about for your audience?"

**Jim Rohn Voice Coach Rewrite (philosophical):**
> "There's something happening in your space right now. Your people are losing clients — not because they're bad coaches, but because they're confusing activity with value. You told me three weeks ago that your biggest fear is coaching someone who doesn't change. I think this connects to that. What breaks when a client leaves? Is it your revenue or your confidence? Tell me."

The difference: the Rohn version references the coach's own previous statement (from the HCD in Supabase), uses antithesis ("activity with value"), targets the emotional core ("revenue or confidence"), and demands specificity. It is delivered as a **voice note** in the Business Philosopher persona voice via CosyVoice TTS.

### 2.2 How the Coach Responds

The coach responds via Telegram voice note. During this exchange, the system:

- **Extracts stories:** Every narrative the coach tells is parsed, tagged with topic cluster, emotional signature (arousal/valence via Wav2Vec), temporal position (past/present/future), narrative arc affinity, and sensory detail score. Stored in `story_bank` table in Supabase.
- **Detects contradictions:** The system cross-references the coach's current claims against all previous claims stored in the `philosophy_tensions` table. When it finds a conflict, it does not flag it immediately — it stores the pair and may surface it in the next trigger cycle.
- **Measures vocal delivery:** Full prosody pipeline runs (OpenSMILE GeMAPS + librosa + Whisper timestamps). WPM, SPM, pause patterns, filler density, pitch variance, sincerity biometrics (jitter/shimmer), emotional loading (arousal/valence). All persisted to the `vocal_delivery` table in Supabase.
- **Does NOT give feedback yet.** Phase 1 is pure extraction. The AI listens, acknowledges briefly ("I heard something important in that. Let's hold it for now."), and stores. The feedback comes later, either in the recording session prep or as a scheduled voice note.

### 2.3 The Specificity Ratchet

If the coach gives a vague response to the trigger, the system does not accept it. It pushes for sensory detail — this is critical for downstream content quality.

Coach says: "I had a client who just didn't get it."  
System responds: "Who was this client? Don't give me a name — give me a picture. Were they sitting across from you or was it a call? What did their voice sound like when they said the thing that told you they didn't get it?"

This is Rohn's method: he built every talk on concrete stories with vivid detail. The system extracts at that resolution because the CCF content pipeline needs episodic material (FR5 ESK-level anchors), not semantic summaries.

---

## 3. Phase 2 — The Recording Session: Video, Booked, Structured

### 3.1 Session Booking and Reminders

Recording sessions are booked like real coaching appointments. They appear in the coach's calendar. The system sends:

- **48 hours before:** A voice note reminder: "Your recording session is Thursday at 10am. I've prepared a script based on what we talked about this week. I'll send it tomorrow so you have time to read through it."
- **24 hours before:** The supportive script is delivered as a text document in Telegram, along with a short voice note overview: "Three recordings this session. The first one is the rant you did on Tuesday — refined into a 90-second philosophy piece. The second is the client story about Sarah. The third is the counter-argument we discussed. Read through them. Mark anything that doesn't sound like you."
- **30 minutes before:** A final gentle nudge: "See you in 30 minutes. Camera on. Remember — don't try to perform. Just say it the way you said it to me on Tuesday."

### 3.2 Session Structure

A recording session is **30 to 60 minutes maximum**. It may contain **multiple video recordings** — typically 2 to 5 per session, each 60 to 180 seconds. The session follows this structure:

1. **Opening Check-In (2-3 min, voice-based):** The AI asks how the coach is feeling. This is not small talk — it calibrates the emotional baseline. If the coach sounds tense, the system adjusts: "You sound tight today. Let's start with the easiest piece — the client win story. Warm up on something that makes you smile."

2. **Script Review Confirmation (1-2 min):** The AI confirms the coach has read the supportive scripts. "Did anything in the scripts feel off? Anything you'd change before we roll?"

3. **Recording Cycle (per video):**
   - Coach records a video take.
   - System ingests the video. Audio is extracted and processed through the full prosody pipeline. Video is analyzed for: body language consistency, eye contact stability, gesture frequency, facial expression congruence with content (using vision model analysis).
   - System delivers **Rohn-style feedback** as a voice note between takes.

4. **Session Wrap (2-3 min):** The AI summarizes what was captured, acknowledges micro-improvements from the HCD, and previews next week's direction: "Three clean recordings. Your pause game was better than last week — two Rohn Pauses in the philosophy piece, both over 2 seconds. Next week we're pulling on the pricing tension you've been avoiding. Start thinking about it."

### 3.3 The Supportive Script

Before every recording session, the coach receives a script. This is NOT a teleprompter — the coach does not read it word-for-word on camera. It is a **preparation document** that:

- **Structures the raw material:** Takes the coach's Phase 1 voice note responses and organizes them into a coherent narrative arc (drawn from the 12 Narrative Arcs).
- **Preserves the coach's language:** The script uses the coach's actual phrases from their voice notes. It does not rewrite them into polished prose. It arranges them.
- **Provides the Pin-and-Iron-Bar balance:** Inserts specific data points (the "pin") next to the coach's emotional claims (the "iron bar"). "You said 'people are afraid to charge what they're worth.' The script adds: 'In 2024, the ICF found that 62% of coaches set fees below market rate.' Now you have both."
- **Suggests pause points:** Marks locations in the script where the coach should pause (the Rohn Pause targets: 1.5-2.5 seconds after key claims). These are not commands — they are suggestions the coach can see in advance.

### 3.4 Video Analysis — Beyond Audio

Since the recording session is video, the AI provides feedback on visual delivery in addition to vocal delivery:

| What the AI Analyzes | How | Feedback Example (Rohn Style) |
|---------------------|-----|-------------------------------|
| **Eye contact stability** | Vision model tracks gaze direction frame-by-frame against camera position | "At the 22-second mark you looked down for three seconds. You lost them. When you say something that matters, look at the lens like you're looking at one person who needs to hear it." |
| **Gesture congruence** | Gesture frequency and type mapped against speech content emphasis points | "Your hands were alive in the first take — they moved with your words. In the second take they were frozen. What changed? You were thinking about the camera, not the message." |
| **Facial expression** | Emotion classification from facial landmarks cross-referenced with audio emotion | "Your voice was warm but your face was tight. The audience trusts the face first. If the face says stress and the voice says calm — stress wins. Relax the jaw before you start." |
| **Posture and energy** | Upper-body posture tracking, movement patterns | "You leaned forward when you talked about the client win. That's conviction. You leaned back when you talked about pricing. That's retreat. The audience reads that. Own the pricing statement. Lean INTO it." |

---

## 4. Feedback as Teaching — The Rohn Delivery Register

The AI teaches. But it teaches through feedback — personalized, precise, data-driven, and always tied to what the coach just did. It never sends generic advice. Every piece of feedback references:

1. **What the coach just did** (the specific moment in the recording)
2. **What the data says** (the metric, the timestamp, the comparison)
3. **What the coach did previously** (the HCD trajectory)
4. **Why it matters** (the Rohn principle that explains the significance)

### 4.1 Feedback Templates by Category

**Pacing (WPM/SPM):**
> "You hit 147 words per minute in the pricing segment. Three weeks ago it was 162. You're slowing down — I can feel the deliberation. But you're not there yet. Rohn used to say brevity and pace are two different things. Being brief is good. Being fast is dangerous. Your target is 120. You'll get there because you're already trending in the right direction."

**Strategic Silence (ISS):**
> "Something happened at the 34-second mark. You said 'the real cost isn't the money — it's the time they'll never get back.' Then you paused for 2.3 seconds. That was the most powerful moment in the recording. Not because of what you said — because of what you DIDN'T say afterward. That silence is where your audience processes. That's the Rohn Pause. You did it instinctively. Now do it on purpose."

**Sincerity Biometrics (Jitter/Shimmer + LIWC-22):**
> "I ran the numbers on that third take. Your voice was steady — no tremor, no performance mode. Your words were direct — first-person, present tense, no hedging. That's what sincerity sounds like when you measure it. Rohn said if dry-eyed you preach hellfire, everybody dismisses it as a performance. You weren't performing. Keep that."

**Pin-and-Iron-Bar Imbalance:**
> "You brought the iron bar today. I could feel the weight behind every word. But where's the pin? You said 'coaches are undercharging and it's destroying the industry.' That's powerful emotion with nothing to hang it on. Give me one number. One study. One client who charged more and what happened. The emotion needs an anchor or the audience files it under 'motivational noise.'"

**Video-Specific:**
> "Watch yourself at the 45-second mark. You look away from the camera right when you say the most important line. Your voice was there — steady, convicted. But your eyes left the room. The audience follows the eyes. If you look away, they think you're unsure. Lock in. That one moment — eyes to lens — and this becomes a completely different piece of content."

### 4.2 Micro-Improvement Acknowledgment

Every session starts by checking the HCD for improvements since the last session. If any metric improved by ≥5%, the AI acknowledges it BEFORE doing anything else:

> "Before we start — I want you to know something. Your filler density dropped from 3.4% to 2.1% since last session. That's a 38% improvement. You didn't notice it because you were focused on the content. But the audience will notice it because they'll feel more confident in you. That's what Rohn called the discipline of the master — it doesn't show after one day. It shows after deliberate, conscious practice. You're doing it."

This is not flattery. It is data-backed acknowledgment delivered before any critique. It primes the coach to receive the harder feedback that follows.

---

## 5. The Four Pillars — As System Behaviors in the CCF Bridge

### Pillar 1: Interest → Elicitation Through the Trigger Map

The AI does not tell the coach to "be interested in life and people." Instead it asks provocative questions sourced from the CCF pipeline (FR15 cultural tensions + FR5 trigger activations) that force the coach to articulate concrete experiences. The question style uses Rohn's conversational depth — pushing for sensory detail, specific people, exact moments — because the content pipeline needs ESK-level episodic material, not surface-level opinions.

### Pillar 2: Fascination → Contradiction Surfacing from HCD

The AI does not tell the coach to "substitute fascination for frustration." Instead it detects contradictions between the coach's current statements and their historical claims stored in Supabase, and it surfaces these as follow-up provocation questions. The contradictions become raw material for the Rant-to-Philosophy pipeline — every piece of original philosophy is born from a resolved tension. The coach becomes fascinated because their own contradictions are irresistible to explore.

### Pillar 3: Sensitivity → Adaptive Behavior from Emotional State

The AI does not tell the coach to "try to understand where someone is." Instead it reads the coach's emotional state via Wav2Vec emotion classification and adapts its own behavior — lighter questions when the coach is burned out, acknowledgment mode when they are agitated, depth when they are ready. It also adjusts session pacing: if the last three sessions were all depth-5 (heavy, philosophical), the next trigger is deliberately lighter. The system tracks emotional patterns in Supabase to detect burnout before the coach feels it.

### Pillar 4: Knowledge → Automated Research as Ammunition

The AI does not tell the coach to "gather knowledge." Instead it performs RAG research on the coach's extracted Core Grievances and delivers supporting evidence — academic studies, historical parallels, counter-arguments — as preparation material before the recording session. This evidence flows into the supportive script as the "pin" data that anchors the coach's emotional "iron bar."

---

## 6. Memory Architecture — Supabase + Redis

The HCD moves from flat JSON to Supabase (persistent) with Redis (session-level caching).

### Supabase Tables

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `coaches` | Coach identity and onboarding state | coach_id, onboard_date, total_sessions, active_program_tier |
| `story_bank` | Extracted stories from Phase 1 voice notes | story_id, coach_id, date_extracted, raw_transcript, topic_tags[], emotion_arousal, emotion_valence, narrative_arc, temporal_position, sensory_detail_score, times_used_in_content |
| `philosophy_tensions` | Contradiction pairs detected across sessions | tension_id, coach_id, claim_a_text, claim_a_session_date, claim_b_text, claim_b_session_date, resolved, resolution_text |
| `personal_philosophy` | Assembled beliefs, unresolved questions, grievances | coach_id, core_beliefs[], unresolved_questions[], recurring_grievances[] |
| `vocal_delivery` | All prosody metrics per session | session_id, coach_id, wpm, spm, pitch_variance, avg_iss, rohn_pauses_detected, filler_density, sincerity_composite, emotional_loading, pin_iron_ratio |
| `video_delivery` | Video-specific analysis per recording | recording_id, session_id, coach_id, eye_contact_score, gesture_congruence, facial_expression_match, posture_notes |
| `sessions` | Session log with emotional trajectory and depth | session_id, coach_id, date, type (trigger/recording), duration_minutes, depth_rating, emotional_baseline, emotional_trajectory, questions_asked[], stories_extracted[], recordings_count |
| `scheduled_sessions` | Booked recording sessions with reminder states | session_id, coach_id, scheduled_datetime, reminder_48h_sent, reminder_24h_sent, script_delivered, reminder_30min_sent, session_completed |
| `scripts` | Supportive scripts generated for recording sessions | script_id, session_id, coach_id, content_pieces[], pause_markers[], pin_data_points[], raw_coach_phrases_used[] |
| `micro_improvements` | Detected metric improvements pending acknowledgment | improvement_id, coach_id, metric_name, previous_value, current_value, delta_pct, acknowledged |

### Redis (Session Cache)

- Current session emotional baseline (refreshed per voice note)
- Active `tension_observation_object` from FR15
- Running prosody metrics for the current session (flushed to Supabase at session end)
- Script cache during recording sessions

---

## 7. Session Lifecycle — The Complete Flow

```
WEEKLY CONTENT BATCH CYCLE
==========================

  Monday–Friday (async, Telegram voice)
  ┌─────────────────────────────────────────────┐
  │ PHASE 1: TRIGGERS                           │
  │                                             │
  │ FR15 Monitor → Cultural Tension Detected    │
  │     ↓                                       │
  │ FR5 Trigger Map → Activation Event Selected │
  │     ↓                                       │
  │ Rohn Voice Coach → Provocation Voice Note   │
  │     ↓                                       │
  │ Coach responds (voice note)                 │
  │     ↓                                       │
  │ System: Extract stories, detect             │
  │   contradictions, measure prosody,          │
  │   update Supabase                           │
  │     ↓                                       │
  │ Repeat 2-4x per week as tensions surface    │
  └─────────────────┬───────────────────────────┘
                    │
  Pre-Session Prep  │
  ┌─────────────────▼───────────────────────────┐
  │ SCRIPT GENERATION                           │
  │                                             │
  │ T-48h: Booking reminder voice note          │
  │ T-24h: Supportive script delivered          │
  │        (structured from Phase 1 material +  │
  │         RAG evidence + pause markers)       │
  │ T-30m: Final gentle nudge                   │
  └─────────────────┬───────────────────────────┘
                    │
  Scheduled Session │ (30-60 min, VIDEO)
  ┌─────────────────▼───────────────────────────┐
  │ PHASE 2: RECORDING SESSION                  │
  │                                             │
  │ 1. Emotional check-in (voice)               │
  │ 2. Script review confirmation               │
  │ 3. Recording cycle (per video):             │
  │    └─ Coach records video                   │
  │    └─ AI analyzes audio + video             │
  │    └─ Rohn-style feedback between takes     │
  │ 4. Session wrap + micro-improvement ACK     │
  │ 5. All metrics persisted to Supabase        │
  └─────────────────┬───────────────────────────┘
                    │
                    ↓
  ┌─────────────────────────────────────────────┐
  │ DOWNSTREAM: CCF Pipeline                    │
  │ Raw recordings → CMF → Visual Generation →  │
  │ Distribution                                │
  └─────────────────────────────────────────────┘
```

---

## 8. What the AI Coach Does — Precise Summary

The AI coach is the CCF's voice to the coach. It performs these actions and only these actions:

1. **It delivers provocation questions sourced from FR15/FR5** in the Rohn voice register — antithetical, specific, referencing the coach's history from Supabase. The questions serve the weekly content batch, not random exploration.

2. **It listens and extracts.** Stories, positions, contradictions, emotional signatures, vocal metrics. Everything goes to Supabase. The coach never journals — the system journals for them.

3. **It generates supportive scripts** for recording sessions, using the coach's own language from Phase 1, structured into narrative arcs, with evidence from RAG research and pause markers.

4. **It books and manages recording sessions** — calendar entries, 48h/24h/30min reminders, session-time emotional calibration. Sessions are 30-60 minutes with multiple video recordings.

5. **It delivers personalized feedback after every recording** — vocal (WPM, pauses, sincerity, emotional loading) AND visual (eye contact, gestures, posture, facial congruence). Every piece of feedback references the coach's own data, their trajectory, and the Rohn principle that explains WHY it matters.

6. **It acknowledges micro-improvements** from the HCD before any critique. Data-backed acknowledgment, not flattery. This is how the system teaches — by holding up a biometric mirror and wrapping the reflection in philosophical language the coach can feel.

The coach expresses. The system measures, remembers, and responds. That is the division of labor.
