# Trivianar Legacy → CCP Evolution: Reconciliation Analysis

*Date: 2026-03-25*  
*Input: 6 legacy Trivianar documents (~2024)*  
*Output: What to KEEP, ADAPT, and DISCARD for CCP's Interactive Trivianar Engine*

---

## The Legacy Vision (2024)

The original Trivianar was designed as a **standalone marketing event** — a trivia+webinar hybrid hosted on Zoom/WebinarJam, promoted via ClickFunnels landing pages, with lead capture through email forms and follow-up via SMS/email sequences. It targeted generic coaching niches (holistic health, personal finance, relationships) with a "millennial Buzzfeed" tone.

It was a clever idea trapped in 2020-era infrastructure: static funnels, email lists, Zoom calls, and manual marketing sequences.

---

## What Has Changed Since Then

| 2024 Trivianar | 2026 CCP |
|---|---|
| Standalone marketing event | Integrated component of a coaching OS |
| Zoom/WebinarJam as platform | AFFiNE Studio + TribeNest streaming |
| ClickFunnels landing pages | AFFiNE workspace (no separate funnel) |
| Email/SMS lead capture | Telegram native (handle, phone, DM) |
| Manual event promotion | Automated by CCF pipeline + Atlas scheduling |
| Generic "millennial" tone | Coach's Voice DNA (3D identity object) |
| No behavioral tracking | Full CBCS pipeline (ICT, SPD, Change Talk) |
| Questions = entertainment | Questions = entertainment + CBCS assessment |
| Post-event email follow-up | Continuous Telegram community + CPSC nurture |
| No database integration | Supabase + Neo4j + AFFiNE sync |

---

## KEEP ✅ (Core Ideas That Were Ahead of Their Time)

### 1. Cognitive Bias Question Architecture
**Source:** `Trivia Quiz Question Engine Prompt Framework.md`

The 6-bias integration checklist is genuinely strong and should be preserved:
- **Curiosity Gap** — create intellectual tension
- **Dunning-Kruger Effect** — balance challenge and achievability
- **Confirmation Bias** — provide surprising twists
- **Novelty Bias** — introduce unexpected insights
- **Completion Bias** — create progression/achievement
- **Status Quo Bias Disruption** — challenge mental models

**CCP Adaptation:** These biases map directly to CRAL's evidence-based content design. The question engine's `cognitiveScores` (curiosityTrigger, learningPotential, surpriseFactor) should be retained in the `trivia_questions` schema as metadata for CRAL analysis.

### 2. Dual-Purpose Question Design
**Source:** `TRIVIANAR Experience Funnel Page Template.md` → "Problem Amplification Trivia"

The legacy docs already understood that trivia questions could simultaneously entertain AND reveal pain points. The "Problem Amplification Questions" ("Which common habit is silently sabotaging your goals?") are proto-qualifying questions. CCP's current architecture formalized this with the `cbcs_mapping` JSON field in `trivia_questions`.

**CCP Adaptation:** Retained and upgraded. Legacy used pain points for manual sales follow-up. CCP uses them as ICT Mapper inputs for automated CPSC conversion intelligence.

### 3. Question-Answer-Fact Pattern
**Source:** `Trivia Quiz Question Engine Prompt Framework.md` → Output Format

The `introMessage → question → answers → funFact` pattern is psychologically effective:
1. Story hook sets emotional context
2. Question creates engagement
3. Answer reveals truth
4. Fun fact cements the learning

**CCP Adaptation:** This 4-step structure should become the Telegram bot's question delivery format. The `introMessage` maps to the Telegram message preceding the inline button question. The `funFact` maps to the post-answer reveal message.

### 4. Engagement Style Guidelines
**Source:** `TRIVIANAR Sequences Template Prompt Framework.md` → Engagement Style

The 6 engagement styles (Unexpected Fact, Playful Challenge, Humorous Tease, Intriguing Question, Behind-the-Scenes, Community Highlight) are a useful rotational framework for keeping trivia sessions from feeling repetitive.

**CCP Adaptation:** These become parameters for the CRAL agent when generating weekly trivia question batches. Each stream's trivia set should vary its engagement style to prevent habituation.

---

## ADAPT 🔄 (Transform for CCP Architecture)

### 1. The 21-Prompt Sequence → Telegram Automation
**Source:** `TRIVIANAR Sequences Prompts.md`, `Trivianar Sequences 🟨.md`

The legacy 21-prompt sequence (registration → reminders → live → replay → feedback → next event) is a solid lifecycle framework. But the medium must change completely:

| Legacy Medium | CCP Medium | Rationale |
|---|---|---|
| Email (Mailchimp/ConvertKit) | Telegram Bot DM | Zero-friction. Client is already in Telegram daily. |
| SMS (Twilio) | Telegram Bot DM | Same channel as accountability check-ins. No SMS cost. |
| ClickFunnels registration page | AFFiNE event page + Telegram `/join-trivia` command | Registration happens inside the OS, not on an external funnel. |
| Zoom event link | CCP Studio stream link (pinned in Telegram group) | Stream lives inside the coaching OS. |
| Post-event email replay | AFFiNE session archive + Telegram VOD link | Replay is in the workspace + delivered via notification. |

**Adapted sequence (15 touchpoints instead of 21):**

| # | Touchpoint | Channel | Timing |
|---|---|---|---|
| 1 | Event announcement + `/join-trivia` | Telegram Group | 7 days before |
| 2 | Teaser question (curiosity hook) | Telegram Group | 5 days before |
| 3 | Host intro + behind-the-scenes | Telegram Group | 3 days before |
| 4 | Preparation tips + warm-up question | Telegram Group | 1 day before |
| 5 | 1-hour reminder | Telegram Group + DM to registered | 1 hour before |
| 6 | 15-minute "doors open" | Telegram Group | 15 min before |
| 7 | LIVE: Stream link pinned | Telegram Group | Stream start |
| 8 | LIVE: Trivia rounds + polls + commitments | Telegram Group (Trivianar Engine) | During stream |
| 9 | LIVE: Leaderboard + winner reveal | Telegram Group | Stream end |
| 10 | Post-stream: DM to new participants (lead capture) | Telegram Bot DM | 5 min after |
| 11 | Post-stream: Replay link + session recap | Telegram Group + AFFiNE | 30 min after |
| 12 | Post-stream: Commitment follow-up reference | Atlas daily prompt (next day) | Next morning |
| 13 | Post-stream: Highlight reel (top moments) | Telegram Group | 2 days after |
| 14 | Feedback request | Telegram Bot DM | 3 days after |
| 15 | Next event teaser | Telegram Group | 7 days after |

**Key differences:** No email. No SMS. No external landing pages. Everything flows through Telegram + AFFiNE. The sequence is automated by the CCF pipeline, not manually configured per event.

### 2. Host Persona → Voice DNA
**Source:** `TRIVIANAR Sequences Template Prompt Framework.md` → Role Definition

Legacy: "Write as {trivia_host_name}, a charismatic trivia master known for {unique_hosting_style}."

This was a manual persona prompt. CCP replaces it with the coach's **3D Voice DNA object** (FR3). The trivia bot's messages, question delivery tone, and reveal messages are all filtered through the Voice DNA pipeline — the bot sounds like the coach, not like a generic "game show host."

**CCP Adaptation:** The trivia engine's text generation (intro messages, fact reveals, leaderboard commentary) receives the same Voice DNA injection as all other CCP content pipelines. Mandate 4 (Negative Space) ensures the bot never uses language the coach would never use.

### 3. Funnel Page → AFFiNE Event Block
**Source:** `TRIVIANAR Experience Funnel Page Template.md`

The 352-line funnel page template was designed for ClickFunnels (registration page, confirmation page, trivia section, FAQ). This entire construct is obsolete in CCP. There is no separate "funnel" — the event lives inside the AFFiNE workspace.

**CCP Adaptation:** A custom AFFiNE block type (`ccp-blocks/trivianar-event/`) renders event details, countdown timer, and past trivia results inline in the coach's workspace. The "registration" is a Telegram `/join-trivia` command. The "confirmation" is a Telegram Bot DM. The "funnel" disappears because the community already exists in the Telegram group.

### 4. Prizes → Gamification Persistence
**Source:** `What is TRIVIANAR?.md` → "Winners walk away with prizes"

Legacy relied on external prizes (coaching sessions, gift cards) as motivation. CCP replaces transient prizes with **persistent gamification** — leaderboard scores that accumulate across streams, visible in the member's AFFiNE dashboard, contributing to their Accountability System streak.

**CCP Adaptation:** The `trivia_leaderboard` table tracks cumulative scores, win count, and streaks. Top performers can earn "Trivia Champion" badges visible in their AFFiNE profile. The real prize is social status within the community — far more powerful than a gift card.

### 5. Question JSON Schema → Enriched with CBCS Mapping
**Source:** `Trivia Quiz Question Engine Prompt Framework.md` → Output Format

Legacy schema:
```json
{
  "questionNumber": 1,
  "introMessage": "...",
  "question": "...",
  "answers": ["...", "...", "...", "..."],
  "correctAnswerIndex": 0,
  "difficultyLevel": 3,
  "funFact": "...",
  "cognitiveScores": { "curiosityTrigger": 8, "learningPotential": 7, "surpriseFactor": 9 }
}
```

**CCP Adaptation — enriched schema:**
```json
{
  "id": "uuid",
  "surface_text": "...",
  "intro_message": "...",
  "answer_options": [
    {"label": "A) ...", "cbcs_mapping": {"social": 0.18, "agency": 0.05}},
    {"label": "B) ...", "cbcs_mapping": {"info_seek": 0.14, "cog": 0.12}},
    ...
  ],
  "correct_answer": "B",
  "fun_fact": "...",
  "difficulty_level": 3,
  "dimension": "coping_trajectory",
  "cognitive_scores": { "curiosity_trigger": 8, "learning_potential": 7, "surprise_factor": 9 },
  "engagement_style": "unexpected_fact",
  "voice_dna_filter": true,
  "time_limit_seconds": 15
}
```

The cognitive scores are retained from legacy. The `cbcs_mapping` and `dimension` fields are new — they enable the dual-purpose qualifying mechanism.

---

## DISCARD ❌ (Architecturally Obsolete)

### 1. ClickFunnels Dependency
The entire funnel page infrastructure (registration page, confirmation page, React+Tailwind prototype, FAQ section) is replaced by AFFiNE workspace blocks + Telegram bot flows. No separate website needed.

### 2. Email-Based Lead Capture
Email opt-in forms are legacy SaaS marketing. CCP captures leads via Telegram (`user.id`, `user.first_name`, `request_contact`). Email is collected conversationally in bot DMs as an enrichment step, not as the primary capture mechanism.

### 3. SMS via Twilio
All SMS touchpoints are replaced by Telegram Bot DMs. Telegram is free, instant, and the client is already in the ecosystem. SMS adds cost and a disconnected channel.

### 4. "Millennial Buzzfeed" Generic Tone
The legacy documents enforce a "millennial tone (Buzzfeed quizzes, witty tweets)" across all communications. This is a persona violation in CCP. Every coach has a unique Voice DNA. The trivia bot must sound like the coach — which might be cerebral and clinical (not Buzzfeed), or warm and nurturing (not witty tweets). The Voice DNA system replaces the generic tone instruction.

### 5. Standalone Event Model
Legacy Trivianar was a standalone event: register → attend → follow up → invite to next. CCP's Trivianar is a **recurring community feature** embedded in the coach's weekly rhythm. There is no "next event to register for" — trivia happens during live streams as a natural component of the coaching community experience.

### 6. Manual Copywriting Per Event
The 21 sequence prompts were designed to be manually customized per event. CCP automates this entirely — the CCF pipeline generates event announcements, the Atlas scheduling system triggers reminders, and the trivia engine manages the live experience. The coach's only action is showing up and streaming.

### 7. Static React Prototype
The funnel page specified a "Frontend Functional Prototype UI with static data" in React+Tailwind. This is replaced by the AFFiNE BlockSuite plugin architecture — the trivia UI lives inside the coaching OS, not as a separate React app.

---

## Summary Matrix

| Legacy Element | Keep | Adapt | Discard |
|---|:---:|:---:|:---:|
| Cognitive Bias Question Framework | ✅ | | |
| Dual-purpose question design | ✅ | | |
| Question-Answer-Fact pattern | ✅ | | |
| Engagement style rotation | ✅ | | |
| 21-prompt event sequence | | 🔄 → 15 Telegram touchpoints | |
| Host persona prompts | | 🔄 → Voice DNA injection | |
| Funnel page template | | 🔄 → AFFiNE event block | |
| Prize-based motivation | | 🔄 → Persistent gamification | |
| Question JSON schema | | 🔄 → Enriched with CBCS mapping | |
| ClickFunnels dependency | | | ❌ |
| Email lead capture | | | ❌ |
| SMS via Twilio | | | ❌ |
| "Millennial Buzzfeed" tone | | | ❌ |
| Standalone event model | | | ❌ |
| Manual copywriting per event | | | ❌ |
| Static React prototype | | | ❌ |

---

**Bottom line:** The original Trivianar vision was genuinely innovative — using gamified trivia for lead generation was ahead of its time. The core question design principles (cognitive bias framework, dual-purpose questions, engagement style rotation) remain excellent and should be preserved in the CCP Trivianar Engine. But the infrastructure layer (email funnels, SMS, ClickFunnels, Zoom, manual sequences) is completely obsolete now that CCP has Telegram as the nervous system, AFFiNE as the brain, and the CBCS pipeline as the behavioral intelligence layer. The Trivianar concept evolves from "a marketing event you host sometimes" to "a permanent, recurring, intelligence-collecting community feature embedded in the coaching OS."

---
*End of Reconciliation Analysis.*
