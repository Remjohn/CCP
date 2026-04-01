# Tech-Spec: FR-CA11-19 — Interactive Trivianar Engine

**Created:** 2026-03-25
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / PRD Update v2.0 — Capability Area 11)
**Architecture Reference:** PRD-Update-CA11 §4.5 (FR-CA11-19), ADR-07
**Skill Implementation:** `tools/trivianar_engine.py` (Python/FastAPI microservice)
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd-update-CA11-quad-platform.md` (§4.5 FR-CA11-19)
- `d:\Work\The Conscious Coaching Factory\docs\features\FB_Interactive_Trivianar_Engine.md` (FB-STUDIO-02, full spec)
- `d:\Work\The Conscious Coaching Factory\trivianar_reconciliation_analysis.md`

---

## 2. Overview

### Problem Statement
Live coaching streams and webinars are one-directional — the coach speaks, clients listen. There is no real-time interactive layer. Engagement signals are limited to unstructured Telegram chat. The CBCS pipeline collects behavioral data from daily check-ins (once/day) and voice notes (sporadic), creating significant telemetry gaps. Existing platforms (Crowdpurr, Kahoot) solve live interaction but operate as external SaaS with zero integration into CCP's behavioral intelligence pipeline.

### Solution
FR-CA11-19 implements the **Interactive Trivianar Engine** — a stateless Python/FastAPI microservice (~560 lines) that delivers live trivia, polls, qualifying assessments, and microcommitment prompts through the Telegram Bot API during CCP Studio livestreams. All responses are permanently stored and processed by CBCS agents asynchronously. The engine includes game modes, a reaction sticker/GIF atmosphere layer, and threaded media delivery for question images.

### Scope
**In scope:**
- FastAPI microservice (webhook receiver + game logic + Telegram Bot API).
- 6 game modes (Countdown, Team, Multi-Round, Wagering, Survivor, Polls).
- Qualifying questions with dual-purpose CBCS mapping.
- Microcommitment checkpoints (open-text prompts during streams).
- Reaction stickers & GIF atmosphere layer (S3 media library).
- Threaded media for question images/videos.
- Leaderboard computation and display.
- Data model (4 tables: questions, responses, leaderboard, leads).

**Out of scope:**
- Lead capture viral loop (FR-CA11-20).
- Stream overlay rendering (FR-CA11-22).
- CBCS agent processing (existing CBCS specs handle post-stream analysis).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-080` | Trivianar Core Engine | CORE — FastAPI app: webhook handler, game state manager, scoring logic. |
| `DEP-ENG-081` | Game Mode Controllers | LOGIC — 6 game mode implementations with distinct scoring/elimination rules. |
| `DEP-ENG-082` | Qualifying Question Processor | INTELLIGENCE — Maps responses to CBCS behavioral parameters via `cbcs_mapping` JSON. |
| `DEP-ENG-083` | Reaction Atmosphere Layer | UX — Pre/post-question sticker/GIF selection and delivery. |
| `DEP-ENG-084` | Threaded Media Handler | UX — Sends question images/videos as thread replies to main question message. |
| `DEP-ENG-085` | Leaderboard Engine | DATA — Computes per-stream and all-time rankings. |
| `DEP-ENG-086` | Microcommitment Checkpoint | INTELLIGENCE — Open-text prompts that feed Change Talk Vault & ICT Mapper. |
| FR-CBCS-01 | Change Talk Vault | DOWNSTREAM — Receives commitment responses for DARN-CAT classification. |
| FR-CBCS-04 | ICT Mapper | DOWNSTREAM — Reads qualifying question responses to update coping trajectory. |

### Academic Grounding

| Framework | Author | Year | Mechanism |
|---|---|---|---|
| **Cognitive Bias Question Design** | CCP Legacy (Trivianar 2024) | 2024 | Questions exploit 6 cognitive biases (Anchoring, Social Proof, Framing, Availability, Dunning-Kruger, FOMO) to make trivia feel surprising and shareable. |
| **Dual-Process Theory** | Kahneman | 2011 | Qualifying questions engage System 1 (fast, intuitive response to fun trivia) while the hidden CBCS mapping captures System 2-relevant behavioral data without triggering deliberate self-presentation. |
| **Variable Ratio Reinforcement** | Skinner | 1957 | Randomized question difficulty and unpredictable reward sizes (speed-based scoring) create the most addiction-resistant engagement pattern. |

### Technical Decisions
1. **Stateless Service, Zero LLM in Hot Path:** All scoring, timing, and leaderboard logic is pure Python + SQL. No LLM inference during the game. LLM involvement is limited to weekly question generation by CRAL agents (outside this spec's scope).
2. **Atomic INSERT Concurrency:** Each Telegram webhook delivers one response as an atomic `INSERT INTO trivia_responses`. No read-modify-write patterns, no locks needed. PostgreSQL handles 50+ concurrent inserts trivially.
3. **Redis Queue for 500+ Users:** If concurrency exceeds 500 simultaneous responses: `LPUSH trivia_responses:{question_id}` drains into batch INSERT. This is a scaling fallback, not default behavior.
4. **Telegram Group (not Channel):** Trivia requires members to respond (inline buttons), which channels do not support. The Telegram venue must be a Group.
5. **Reactions in Main Chat, Media in Threads:** Reaction GIFs go in the main chat flow (they ARE the atmosphere). Question images/videos go as thread replies to the question message (keeps chat clean, media reviewable later).

---

## 4. Implementation Plan

### Stage 1: Core Engine & Webhook Handler
*Agent:* `Marco` (Trivianar Engine Operator)
*Inputs:* Telegram Bot API webhook events.
*Outputs:* Running FastAPI microservice on Docker.
*DEP-ID:* `DEP-ENG-080`

**Steps:**
1. Create `trivianar_engine.py` FastAPI app with: `/webhook` endpoint (Telegram updates), `/health` endpoint.
2. Register Telegram bot webhook URL pointing to the deployed service.
3. Implement message handler: detect inline keyboard callback queries (trivia answers), detect text messages (commitment responses).
4. Implement stream session lifecycle: `POST /trivia/start { stream_id, coach_id, question_set_id }` → activates game for a specific Telegram group. Note: `stream_id` must perfectly map to the `studio_sessions.id` produced by FR-CA11-16 to preserve downstream telemetry joins.
5. Implement question sequencing: load questions from `trivia_questions` table, send them in order with configurable intervals.

### Stage 2: Game Modes
*Agent:* `Marco`
*Inputs:* Game mode config per stream session.
*Outputs:* Mode-specific scoring and behavior.
*DEP-ID:* `DEP-ENG-081`

**Steps:**
1. **Countdown Trivia:** `score = max(0, 1000 - elapsed_ms / 10)`. First correct answer gets highest points.
2. **Team Mode:** `team_id` assigned to each user. Team score = sum of member scores. Sent as group leaderboard.
3. **Multi-Round:** `round_id` per question batch. Cumulative scoring across rounds. Grand champion at stream end.
4. **Points Wagering:** Pre-question prompt: "Wager 100-500 points." Correct = wager × 2, wrong = -wager.
5. **Survivor:** Wrong answer = `eliminated = true`. Last standing wins. Eliminated users spectate but can't answer.
6. **Live Polls:** Use Telegram native `sendPoll` API. No scoring. Results aggregated for sentiment analysis.

### Stage 3: Qualifying Questions & CBCS Mapping
*Agent:* `Marco`
*Inputs:* `trivia_questions` with `cbcs_mapping` JSON per answer option.
*Outputs:* Behavioral parameter updates posted to CBCS queue.
*DEP-ID:* `DEP-ENG-082`

**Steps:**
1. When a qualifying question is answered: retrieve the `cbcs_mapping` from the selected answer option.
2. Batch qualifying results per user per stream into `qualifying_assessment` JSONB on `trivia_responses`.
3. Post-stream: CBCS batch processor reads `trivia_responses JOIN trivia_questions` and feeds ICT Mapper (FR-CBCS-04) with behavioral parameter updates.
4. Members never see the CBCS mapping — they only see the "fun" surface text.

### Stage 4: Reaction Atmosphere Layer
*Agent:* `Marco`
*Inputs:* Reaction media library from S3 (`s3://ccp-assets/trivianar/reactions/`).
*Outputs:* Sticker/GIF messages sent to Telegram group.
*DEP-ID:* `DEP-ENG-083`

**Steps:**
1. Load reaction library configuration from coach's settings (defaults to standard pool).
2. Pre-question (2s before): select random reaction from `pre_question_hype` pool → `sendAnimation()`.
3. Post-question (correct): select from `correct_answer_celebration` pool → `sendAnimation()`.
4. Post-question (majority wrong): select from `wrong_answer_shock` pool → `sendAnimation()`.
5. Speed record (answer < 2s): select from `speed_record` pool → `sendAnimation()`.
6. Post-commitment: select from `commitment_empowerment` pool → `sendAnimation()`.
7. All reactions sent with 500ms delay after trigger for natural pacing.

### Stage 5: Threaded Media
*Agent:* `Marco`
*Inputs:* `trivia_questions.media_url` field.
*Outputs:* Media messages sent as thread replies.
*DEP-ID:* `DEP-ENG-084`

**Steps:**
1. After sending the question message (with inline buttons), capture the `message_id`.
2. If `question.media_url` exists: `sendPhoto(reply_to_message_id=question_message_id)` or `sendVideo()`.
3. After answer reveal: send fun fact as thread reply to the same question message.

### Stage 6: Leaderboard Engine
*Agent:* `Marco`
*Inputs:* `trivia_responses` table.
*Outputs:* Per-stream and all-time rankings.
*DEP-ID:* `DEP-ENG-085`

**Steps:**
1. After each question: `SELECT user_id, SUM(score) as total FROM trivia_responses WHERE stream_id = ? GROUP BY user_id ORDER BY total DESC LIMIT 10`.
2. Format leaderboard as Telegram message: `🏆 1. @sarah — 850pts (+100)\n   2. @mike — 720pts (+80)`.
3. Send leaderboard to group.
4. Emit `leaderboard_updated` WebSocket event to Studio Block for stream overlay (FR-CA11-22).
4. Post-stream: update `trivia_leaderboard` materialized table (all-time cumulative scores).
5. Post-stream (Receipting Exemption & Batch): Individual trivia responses are exempt from single-row receipting due to volume. Instead, batch-hash all responses for the `stream_id` and write a single end-of-stream Receipt Chain Guard transaction.

---

## 5. Data Model

```sql
CREATE TABLE trivia_questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    coach_id UUID NOT NULL REFERENCES coaches(id),
    surface_text TEXT NOT NULL,
    answer_options JSONB NOT NULL,
    correct_answer VARCHAR(1) NOT NULL,
    dimension VARCHAR(30),
    difficulty VARCHAR(15) DEFAULT 'accessible',
    time_limit_seconds INTEGER DEFAULT 15,
    media_url TEXT,
    fun_fact TEXT,
    round_id UUID,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE trivia_responses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id BIGINT NOT NULL,
    question_id UUID NOT NULL REFERENCES trivia_questions(id),
    stream_id UUID NOT NULL REFERENCES studio_sessions(id),
    answer VARCHAR(1) NOT NULL,
    is_correct BOOLEAN NOT NULL,
    score INTEGER DEFAULT 0,
    response_time_ms INTEGER,
    team_id UUID,
    responded_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE trivia_leaderboard (
    user_id BIGINT NOT NULL,
    coach_id UUID NOT NULL REFERENCES coaches(id),
    total_score INTEGER DEFAULT 0,
    games_played INTEGER DEFAULT 0,
    win_count INTEGER DEFAULT 0,
    current_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (user_id, coach_id)
);

CREATE INDEX idx_trivia_responses_stream ON trivia_responses(stream_id);
CREATE INDEX idx_trivia_responses_user ON trivia_responses(user_id);
CREATE INDEX idx_trivia_questions_coach ON trivia_questions(coach_id);
```

---

## 6. Tasks

- [ ] **Task 1:** Create `trivianar_engine.py` FastAPI app with webhook endpoint + health check.
- [ ] **Task 2:** Implement question sequencing engine (load from DB, send with timing, collect responses).
- [ ] **Task 3:** Implement 6 game mode controllers (Countdown, Team, Multi-Round, Wagering, Survivor, Polls).
- [ ] **Task 4:** Implement qualifying question CBCS mapping processor.
- [ ] **Task 5:** Build reaction atmosphere layer (S3 media pool, random selection, timed delivery).
- [ ] **Task 6:** Build threaded media handler (`reply_to_message_id` for images/videos/fun facts).
- [ ] **Task 7:** Build leaderboard engine (per-stream ranking + all-time materialized table).
- [ ] **Task 8:** Implement microcommitment checkpoint handler (open-text prompts → CBCS queue).
- [ ] **Task 9:** Add `trivia_questions`, `trivia_responses`, `trivia_leaderboard` table migrations.
- [ ] **Task 10:** Build `Marco` agent persona YAML (Trivianar Engine Operator) in the Engagement Department.
- [ ] **Task 11:** Dockerize and deploy trivianar_engine on AWS ECS/EC2.
- [ ] **Task 12:** Populate default reaction media library in `s3://ccp-assets/trivianar/reactions/`.

---

## 7. Acceptance Criteria

- [ ] **AC1 (Question Delivery):** Start a trivia session. Assert bot sends question with 4 inline buttons to the Telegram group within 1 second of trigger.
- [ ] **AC2 (Scoring):** Answer a question in 3 seconds (time limit 15s). Assert score = `max(0, 1000 - 3000/10)` = 700 points.
- [ ] **AC3 (Leaderboard):** 3 users answer a question. Assert leaderboard message shows correct ranking by score.
- [ ] **AC4 (Qualifying CBCS):** Answer a qualifying question with option A (which maps `social: 0.18`). Assert `trivia_responses` row includes the mapping and post-stream batch processes it.
- [ ] **AC5 (Reaction GIFs):** Start a trivia question. Assert a drumroll GIF is sent 2 seconds before the question. Assert a celebration GIF is sent after correct answers.
- [ ] **AC6 (Threaded Media):** Send a question with `media_url`. Assert the image is sent as a reply to the question message (thread), not as a standalone message.
- [ ] **AC7 (Survivor Mode):** 5 users play Survivor. User 3 answers wrong. Assert user 3 gets `eliminated = true` and cannot answer subsequent questions.
- [ ] **AC8 (Concurrency):** Simulate 200 simultaneous webhook deliveries. Assert all 200 responses are stored with no data loss and leaderboard reflects all answers.
- [ ] **AC9 (Microcommitment):** Send a commitment checkpoint. User responds with "I will exercise daily." Assert response is flagged for CBCS priority processing.
- [ ] **AC10 (Latency):** Measure time from button click to leaderboard update. Assert < 200ms.

---

## 8. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| Telegram Bot API | External | Bot must be created, token stored in environment variables. |
| Telegram Group | External | Trivia runs in a Group (not Channel). Bot must be admin with message permissions. |
| Supabase (PostgreSQL) | Internal | For trivia tables. |
| S3 bucket: `ccp-assets` | Infrastructure | For reaction media library. |
| CBCS Agent Swarm | Internal (existing) | Post-stream processing of qualifying question data + commitment responses. |
| CCP Studio Block (FR-CA11-16) | Internal | Stream session context enables trivia activation. |

---

## 9. Testing Strategy

### Unit Tests
- **Scoring:** Test all 6 game mode scoring algorithms with known inputs/outputs.
- **Qualifying Mapping:** Test CBCS mapping extraction from answer options JSONB.
- **Reaction Selection:** Test random selection from reaction pools (assert non-None, assert variety over 10 calls).
- **Leaderboard SQL:** Test ranking query with known response data.

### Integration Tests
- **Full Question Cycle:** Send question → receive 5 responses → assert scoring → assert leaderboard → assert reactions sent.
- **CBCS Pipeline Handoff:** Complete a trivia session with qualifying questions. Assert ICT Mapper receives the batch data.
- **Concurrent Load:** Fire 200 webhook POSTs simultaneously. Assert all stored, no duplicates, no errors.

### Manual Verification
- **Telegram UX:** Run a full 10-question trivia session in a test Telegram group. Verify: question rendering, button responsiveness, reaction GIF delivery, threaded media, leaderboard formatting.
