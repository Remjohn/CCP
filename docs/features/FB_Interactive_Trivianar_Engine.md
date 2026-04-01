# Feature Brief: The Interactive Trivianar Engine

*Feature ID: FB-STUDIO-02*  
*Parent MCDA: MCDA IV §X, §XI*  
*Date: 2026-03-25*  
*Status: Brainstorm → Pending Spec*

---

## 1. Problem Statement

Live coaching sessions and webinars are currently one-directional: the coach speaks, clients listen. There is no real-time interactive layer. Engagement signals are limited to Telegram group chat messages, which are unstructured and difficult to process at scale. The CBCS pipeline collects behavioral data from daily check-ins (once/day) and voice notes (sporadic), creating significant telemetry gaps between interactions.

Crowdpurr and similar platforms solve live audience interaction for events, but they operate as external SaaS tools with zero integration into behavioral intelligence pipelines. The CCP needs an interactive engine that simultaneously: entertains, measures behavior, collects CBCS intelligence, and drives community belonging — all through the Telegram channel members already use daily.

---

## 2. Solution Overview

Build the **Interactive Trivianar Engine** — a stateless Python service (~500 lines) that delivers live trivia, polls, qualifying assessments, and microcommitment prompts through the Telegram Bot API during CCP Studio livestreams. All responses are stored permanently and processed by CBCS agents asynchronously. The engine includes a gamification layer (leaderboards, points, teams) and a viral lead capture mechanism.

---

## 3. Core Components

### 3.1 Trivia Engine (Python/FastAPI)

**Architecture:** Stateless async Python service. **Zero LLM involvement in the hot path.** All scoring, timing, and leaderboard logic is pure Python + SQL.

**Concurrency handling:**
- Each Telegram webhook delivers one response as an atomic SQL `INSERT`
- No read-modify-write patterns — no locks needed
- PostgreSQL handles 50+ concurrent inserts trivially
- For 500+ simultaneous users: Redis queue (`LPUSH trivia_responses:{question_id}`) drains into batch `INSERT`

**Pattern:** Write first, analyze later. Real-time interactions hit the database directly. CBCS agents process the accumulated data asynchronously (every 15-60 minutes).

### 3.2 Game Modes

| Mode | Description | CCP Intelligence Value |
|---|---|---|
| **Countdown Trivia** | Decreasing points timer — answer fastest = most points. `score = max(0, 1000 - elapsed_ms / 10)` | Speed reveals confidence level |
| **Team Mode** | Members organized into teams. `team_id` column in responses. Team score = sum of member scores | Team dynamics feed Social Penetration Depth |
| **Multi-Round** | Cumulative scoring across rounds. `round_id` column. Grand champion at end of stream | Sustained engagement = high commitment signal |
| **Points Wagering** | Members bet points before answering. Correct = wager × 2; wrong = -wager | Risk tolerance maps to agency scoring |
| **Survivor** | Wrong answer = eliminated. Last standing wins | Persistence metric for ICT Mapper |
| **Live Polls** | Telegram native `sendPoll` API. No scoring, just community pulse | Aggregate sentiment + content direction steering |

### 3.3 Qualifying Questions (Behavioral Assessment)

The most strategically valuable feature. Questions are designed with **dual purpose:**

**Surface layer:** Fun, engaging, low-stakes quiz question  
**Hidden layer:** Response maps to CBCS behavioral model parameters

**Generation:** CRAL agents generate qualifying questions during weekly content batches. Each question includes:
- `surface_text`: The fun version members see
- `answer_options`: 4 choices with entertainment framing
- `cbcs_mapping`: JSON mapping each answer to ICT/SPD/CT parameters
- `dimension`: Which CBCS dimension this question assesses (coping, agency, social, identity)

**Example:**

```json
{
  "surface_text": "When you feel stuck, what do you do first?",
  "answer_options": [
    {"label": "A) Call a friend", "cbcs_mapping": {"social": 0.18, "agency": 0.05}},
    {"label": "B) Research solutions", "cbcs_mapping": {"info_seek": 0.14, "cog": 0.12}},
    {"label": "C) Wait and hope", "cbcs_mapping": {"avoidance": 0.22, "cog": 0.03}},
    {"label": "D) Make a plan", "cbcs_mapping": {"agency": 0.19, "cog": 0.15}}
  ],
  "dimension": "coping_trajectory",
  "difficulty": "accessible"
}
```

**Processing:** After the stream, the ICT Mapper reads `trivia_responses` joined with `trivia_questions.cbcs_mapping` and updates each respondent's coping trajectory model. The member never knows they were assessed.

### 3.4 Microcommitment Checkpoints

During streams, the engine injects **open-text Telegram prompts** at strategic moments:

- *"Based on what you just heard, what is ONE thing you will do differently this week?"*
- *"What resonated most with you in this segment?"*
- *"Name one person you will share this insight with."*

**Processing:** These free-text responses are the highest-value data. They're processed by:
1. **Change Talk Vault (FR-CBCS-01):** DARN-CAT classification (Desire, Ability, Reason, Need, Commitment, Activation, Taking Steps)
2. **Identity Trigger (FR-CBCS-03):** Identity-level commitment detection
3. **ICT Mapper (FR-CBCS-04):** Coping trajectory position update
4. **CPSC Pipeline:** If response contains Commitment/Activation/Taking Steps language → conversion readiness score elevates

**Next-day accountability:** The daily Atlas ritual prompt (FR32) references yesterday's commitment: *"Yesterday during the live session you said you would 'wake up at 6am every day this week.' How did this morning go?"* Public commitment + follow-up = dramatically higher compliance.

### 3.5 Reaction Stickers & GIF Atmosphere Layer

Trivia in a Telegram group must feel like a **conversation with a funny friend**, not a corporate quiz engine. Before and after each question, the bot sends contextual reaction stickers and GIFs to create emotional atmosphere:

**Pre-Question Reactions (build anticipation):**
- 🥁 Drumroll GIF → sent 2 seconds before the question appears
- 🤔 "Thinking" animated sticker → primes cognitive engagement
- 🔥 "This one's tough!" GIF → for difficulty level 4-5 questions
- 🎯 "Easy warm-up!" sticker → for difficulty level 1-2 questions

**Post-Question Reactions (emotional payoff):**
- ✅ Correct: 🎉 Confetti GIF + "NAILED IT!" sticker
- ❌ Wrong (majority missed): 🤯 Mind-blown GIF + fun fact reveal
- ⚡ Speed record: 🏎️ "Lightning fast!" GIF when someone answers under 2 seconds
- 😱 Upset: Dramatic "WHAT?!" GIF when the leaderboard leader gets it wrong
- 🏆 Winner reveal: 👑 Crown sticker + custom celebration GIF

**Post-Commitment Checkpoint Reactions:**
- 💪 Empowerment stickers after commitment responses
- 🤝 Community stickers when multiple members commit to the same action

**Implementation:**
- Reaction media library stored in S3: `s3://ccp-assets/trivianar/reactions/`
- Each reaction is a `reaction_type` mapped to a pool of 5-10 variants per type (prevents repetition)
- Coach can customize which stickers/GIFs are in each pool via the Studio settings panel
- Bot selects randomly from the pool for each occurrence
- Reactions are sent with a 500ms delay after the trigger event for natural pacing

**Schema addition:**
```json
{
  "reaction_library": {
    "pre_question_hype": ["s3://ccp-assets/trivianar/reactions/drumroll_01.gif", "..."],
    "correct_answer_celebration": ["s3://ccp-assets/trivianar/reactions/confetti_01.gif", "..."],
    "wrong_answer_shock": ["s3://ccp-assets/trivianar/reactions/mindblown_01.gif", "..."],
    "speed_record": ["s3://ccp-assets/trivianar/reactions/lightning_01.gif", "..."],
    "winner_reveal": ["s3://ccp-assets/trivianar/reactions/crown_01.gif", "..."],
    "commitment_empowerment": ["s3://ccp-assets/trivianar/reactions/flexing_01.gif", "..."]
  }
}
```

### 3.6 Threaded Media for Questions

Question-related images and videos are sent as **thread replies** to the question message, not as separate messages in the main chat. This prevents the group from getting cluttered with media while keeping the main chat flow clean and readable.

**Flow:**
1. Bot sends the question as a text message with inline answer buttons → this is the **main message**
2. Bot immediately replies **to that message** (creating a thread) with the question image/video
3. The fun fact reveal after answering is also sent as a **thread reply** to the same question message
4. Reaction GIFs (pre/post question) go in the **main chat** (they ARE the atmosphere)

**Why threading matters:**
- In a fast-paced stream with 10+ questions, media assets would flood the main chat
- Threading keeps each question's media self-contained and reviewable later
- Members can tap the thread to see the full context (image + fun fact + discussion)
- The main chat stays clean: question → reactions → answers → leaderboard → next question

**Telegram API:** `reply_to_message_id` parameter in `sendPhoto` / `sendVideo` / `sendAnimation` — this creates a thread in groups that have topics enabled, or a reply chain in standard groups.

---

## 4. Telegram UX Architecture

### Venue: Telegram Group (NOT Channel)

| Feature | Channel | Group | Decision |
|---|---|---|---|
| Members can respond | ❌ | ✅ | Can't run trivia in a channel |
| Bot reads all messages | ❌ | ✅ | Required for CBCS processing |
| Inline buttons | ❌ | ✅ | Required for trivia answers |
| Members invite friends | ✅ | ✅ | Both support invite links |

### Stream Video Delivery

Telegram Bot API **cannot embed live video** in groups natively. The architecture:

1. Bot **pins a message** with the stream URL at group top
2. Members watch stream in browser/YouTube (external player)
3. Members interact via Telegram simultaneously (split-screen on mobile/desktop)
4. This mirrors the Twitch model: video in one window, chat/interaction in another

### Message Flow During Stream

```
┌──────────────────────────────────────────────────┐
│              TELEGRAM GROUP                       │
├──────────────────────────────────────────────────┤
│ 📌 PINNED: Coach is LIVE → [Watch Link]          │
│                                                  │
│ 🤖 Bot: [🥁 Drumroll GIF]                        │ ← Reaction (main chat)
│                                                  │
│ 🤖 Bot: ❓ TRIVIA Q1 (15s countdown)             │ ← Question (main chat)
│ "What drives lasting behavior change?"           │
│ [A] [B] [C] [D]  ← Inline keyboard buttons      │
│   └─ 🧵 THREAD:                                  │
│      🖼 [Question image/video]                   │ ← Media (threaded)
│                                                  │
│ 🤖 Bot: [🎉 Confetti GIF]                        │ ← Reaction (main chat)
│ 🤖 Bot: ⏱ Time's up!                            │
│ ✅ Correct: B) Identity Shift                    │
│   └─ 🧵 THREAD:                                  │
│      💡 Fun fact: "James Clear's research..."    │ ← Fun fact (threaded)
│                                                  │
│ 🏆 1. @sarah — 850pts (+100)                    │
│    2. @mike — 720pts (+80)                       │
│    3. @lisa — 690pts (+60)                       │
│                                                  │
│ 🤖 Bot: 📊 POLL                                  │
│ "What topic next?"                               │
│ ○ Morning Routines (47%)                         │
│ ○ Nutrition (31%)                                │
│ ○ Sleep (22%)                                    │
│                                                  │
│ 🤖 Bot: [🤔 Thinking sticker]                    │ ← Reaction (main chat)
│ 🤖 Bot: 💬 COMMITMENT CHECK                      │
│ "What's ONE thing you'll change?"                │
│                                                  │
│ 👤 @sarah: I'll wake up at 6am this week        │
│ 🤖 Bot: [💪 Flexing GIF]                         │ ← Reaction to commitment
│ 👤 @lisa: I want to try journaling               │
│                                                  │
│ 👤 @random_friend: This is amazing!             │ ← New lead
└──────────────────────────────────────────────────┘
```

### Message Persistence

**Every message is permanently stored:**

| Message Type | Storage | CBCS Processing |
|---|---|---|
| Trivia answers (button clicks) | `trivia_responses` table | ICT Mapper (batch, post-stream) |
| Free-text comments | CBCS message log (existing) | Change Talk Vault, Identity Trigger |
| Poll responses | `poll_responses` table | Aggregate sentiment analysis |
| Commitment checkpoint responses | CBCS message log + flagged priority | Full CBCS pipeline (Aria → Miriam → CT Detector → ICT Mapper) |
| Reaction stickers/GIFs | Not stored (atmosphere only) | N/A — decorative, not data |
| Threaded media (images/videos/fun facts) | Linked to `trivia_questions` via `media_url` field | Available for VOD recap generation |

---

## 4b. Stream Overlay Layer (CCP Studio React Component)

While Telegram handles the participant interaction, the **stream itself** needs a visual overlay so viewers (including those not in the Telegram group) see the trivia experience on screen. This overlay renders as a semi-transparent React component composited onto the Studio Block's stream canvas.

### Overlay Components

**Question Display Overlay:**
```
┌──────────────────────────────────┐
│ Q3: "What drives behavior..."    │
│ ⏱ ████████░░░░ 8s remaining     │  ← Countdown bar depletes visually
│                                  │
│ A: ████     27%                  │  ← Color-coded bars (Crowdpurr-style)
│ B: █████████ 45% ← CORRECT      │  ← Highlighted green after reveal
│ C: ██       12%                  │
│ D: ████     16%                  │
└──────────────────────────────────┘
```

**Leaderboard Overlay (slides in from right):**
```
┌─────────────────┐
│  🏆 LEADERBOARD │
│ 1. @sarah   850 │
│ 2. @mike    720 │
│ 3. @lisa    690 │
│ 4. @tom     550 │
│ 5. @amy     480 │
└─────────────────┘
```

**Winner Reveal Animation (end of stream):**
- Dark overlay covers stream
- Suspenseful pause (2 seconds)
- 3rd place revealed → slide in from left
- 2nd place revealed → slide in from right
- 1st place revealed → center + confetti explosion (CSS particles)
- Champion name displayed in large branded typography

**Technical implementation:**
- React component: `<TriviaOverlay />` rendered on the Studio Block's `<canvas>` compositing layer
- Driven by WebSocket events from the Trivianar Engine (`question_started`, `answers_revealed`, `leaderboard_updated`, `winner_revealed`)
- Semi-transparent background (rgba) so the coach's webcam is visible behind the overlay
- Animation library: Framer Motion (already in AFFiNE's React dependency tree)
- Confetti: `canvas-confetti` npm package (~3KB)

---

## 5. Lead Generation Viral Loop

### The Mechanism

```
Member invites friend → Friend joins group → Experiences trivia (entertainment first)
        ↓
Bot sends private DM after stream: "You scored 340pts! 🎉 Want weekly invites?"
        ↓
DM presents: [Share Contact] button (request_contact = True)
        ↓
On consent: phone number captured → stored in leads table
        ↓
Bot asks: "What's your email?" → email captured
        ↓
Lead enters Conscious Nurturing Architecture (FR-CBCS-14)
        ↓
21-day commercial cooldown → value-first content → CPSC conversion evaluation
```

### Telegram Data Capture

| Data | Method | When |
|---|---|---|
| Name, handle, user ID | Automatic on group join | Instant |
| Phone number | `KeyboardButton(request_contact=True)` in bot DM | Post-stream (consent required) |
| Email | Conversational prompt in bot DM | Post-stream |

> **Constraint:** `request_contact` only works in private chats (bot DM), not in groups. The trivia experience provides the motivation — capture happens after value is delivered, not before.

### Lead Quality Signal

Every lead captured through trivia arrives with **behavioral data attached:** trivia scores, qualifying question responses (mapped to CBCS dimensions), and participation frequency. This gives the CPSC pipeline a warm start — the lead's coping position is partially estimated before their first 1:1 interaction.

---

## 6. Data Model

### New Tables

```sql
-- Trivia questions (generated by CRAL agents weekly)
CREATE TABLE trivia_questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    coach_id UUID NOT NULL REFERENCES coaches(id),
    surface_text TEXT NOT NULL,
    answer_options JSONB NOT NULL,  -- [{label, cbcs_mapping}]
    correct_answer VARCHAR(1) NOT NULL, -- A/B/C/D
    dimension VARCHAR(30), -- coping_trajectory, identity, social, agency
    difficulty VARCHAR(15) DEFAULT 'accessible',
    time_limit_seconds INTEGER DEFAULT 15,
    round_id UUID, -- for multi-round games
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Trivia responses (one row per user per question)
CREATE TABLE trivia_responses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id BIGINT NOT NULL, -- Telegram user ID
    question_id UUID NOT NULL REFERENCES trivia_questions(id),
    stream_id UUID NOT NULL, -- FK to stream session
    answer VARCHAR(1) NOT NULL,
    is_correct BOOLEAN NOT NULL,
    score INTEGER DEFAULT 0,
    response_time_ms INTEGER, -- for speed-based scoring
    team_id UUID, -- for team mode
    responded_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Trivia leaderboard (materialized, updated per-round)
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

-- Leads captured from trivia viral loop
CREATE TABLE trivia_leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    telegram_user_id BIGINT NOT NULL UNIQUE,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    username VARCHAR(100),
    phone_number VARCHAR(20),
    email VARCHAR(255),
    referred_by_user_id BIGINT, -- the member who invited them
    first_stream_id UUID,
    trivia_scores_summary JSONB, -- aggregated behavioral data
    cbcs_initial_assessment JSONB, -- from qualifying questions
    nurture_status VARCHAR(20) DEFAULT 'new', -- new, warming, qualified, converted
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 7. Technical Specifications

| Aspect | Specification |
|---|---|
| **Language** | Python 3.11+ (async) |
| **Framework** | FastAPI (stateless microservice) |
| **Telegram SDK** | `python-telegram-bot` v20+ (async) |
| **Database** | Supabase (PostgreSQL) via `supabase-py` |
| **Cache** | Redis (for high-concurrency response buffering if >500 users) |
| **Deployment** | Docker container on AWS ECS/EC2 |
| **Latency target** | < 200ms from button click to leaderboard update |
| **Concurrency target** | 200 simultaneous responses without degradation |

---

## 8. Crowdpurr Feature Parity

| Crowdpurr Feature | CCP Implementation | Lines of Code |
|---|---|---|
| Decreasing Points Timer | `score = max(0, 1000 - elapsed_ms / 10)` | ~20 |
| Rankings Leaderboard | `SELECT user_id, SUM(score) ... ORDER BY score DESC` | 1 SQL query |
| Team Modes | `team_id` column in `trivia_responses`, group by team | ~10 |
| Multi-Round | `round_id` column, cumulative scoring | Trivial |
| Points Wagering | Wager prompt before question, `score = wager × multiplier` | ~30 |
| Survivor Mode | `eliminated` boolean per user per stream | ~15 |
| Winner Animations | Studio overlay renders confetti + name (React component) | CSS/JS only |
| Lead Capture | Telegram `request_contact` + bot DM flow | ~50 |
| Live Polls | Telegram native `sendPoll` API | 1 API call |
| Reaction Stickers/GIFs | Pre/post question atmosphere via `sendAnimation` / `sendSticker` | ~40 |
| Threaded Media | `reply_to_message_id` on `sendPhoto` / `sendVideo` | ~20 |

**Total engine size: ~560 lines Python + ~400 lines React overlay (including animations)**

---

## 9. Success Criteria

| Criterion | Target | Measurement |
|---|---|---|
| Stream engagement | ≥60% of live viewers participate in at least one trivia round | `trivia_responses` count / stream viewer count |
| CBCS intelligence gain | Qualifying questions update ≥40% of participant coping trajectories per stream | ICT Mapper update log |
| Lead capture rate | ≥25% of new group joiners share contact via bot DM | `trivia_leads` creation rate |
| Microcommitment follow-through | ≥35% of commitment checkpoint responses referenced in next-day accountability | Atlas prompt delivery log |

---

*End of Feature Brief FB-STUDIO-02.*
