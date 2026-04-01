# Tech-Spec: FR-CA11-20 — Trivianar Lead Generation Viral Loop

**Created:** 2026-03-25
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / PRD Update v2.0 — Capability Area 11)
**Architecture Reference:** PRD-Update-CA11 §4.5 (FR-CA11-20), ADR-07
**Skill Implementation:** Extension to `tools/trivianar_engine.py` + CBCS bot DM flow
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

- `d:\Work\The Conscious Coaching Factory\docs\prd\prd-update-CA11-quad-platform.md` (§4.5 FR-CA11-20)
- `d:\Work\The Conscious Coaching Factory\docs\features\FB_Interactive_Trivianar_Engine.md` (§5 Lead Capture)

---

## 2. Overview

### Problem Statement
Traditional lead capture in coaching is cold — a landing page form captures name/email with zero behavioral data. The coach then nurtures from zero context. The CCP's CBCS pipeline requires behavioral data to personalize nurturing, but no behavioral data exists for a lead who has never interacted with the system.

### Solution
FR-CA11-20 implements a **viral lead capture loop** through the Trivianar Engine. When members invite friends to join live trivia sessions via Telegram, every new joiner's trivia responses become behavioral data. Qualifying questions map to CBCS parameters, giving the system a partial coping trajectory *before* any direct coaching interaction. Post-stream, the bot sends a DM to new participants offering a contact-sharing prompt and follow-up sequence.

### Scope
**In scope:**
- New group member detection (Telegram `message.new_chat_members`).
- Automatic data capture (`user.id`, `user.first_name`).
- Post-stream bot DM flow (consent-based phone via `request_contact`, email via conversational prompt).
- `trivia_leads` table creation.
- Warm-start CBCS entry (partial coping trajectory from trivia data).
- 21-day commercial cooldown enforcement.

**Out of scope:**
- Trivianar Engine core (FR-CA11-19).
- CBCS nurturing pipeline logic (existing FR-CBCS-14).
- Payment processing or direct sales.

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-090` | New Member Detection | TRIGGER — Detects `new_chat_members` event in Telegram group. |
| `DEP-ENG-091` | Contact Capture DM Flow | UX — Post-stream bot sends DM with `request_contact` keyboard. |
| `DEP-ENG-092` | CBCS Warm Start Entry | INTELLIGENCE — Creates partial coping trajectory from trivia responses. |
| FR-CA11-19 | Trivianar Engine | UPSTREAM — Provides trivia responses and qualifying question data. |
| FR-CBCS-14 | Conscious Nurturing Architecture | DOWNSTREAM — Receives lead with partial behavioral profile. |

### Academic Grounding

| Framework | Author | Year | Mechanism |
|---|---|---|---|
| **Warm Start Problem** | CCP Internal | 2025 | Cold leads have zero context. Trivianar provides N qualifying question responses before the first DM, eliminating the cold-start problem in CBCS nurturing. |
| **Social Proof Lead Gen** | Cialdini | 1984 | Joining a trivia game because a friend invited you is a social-proof-driven action. The lead enters with positive association to the community (vs. a cold ad click). |

### Technical Decisions
1. **Consent-First Contact:** Phone number is requested via Telegram's `request_contact` keyboard button (user must explicitly tap "Share Contact"). Email is requested via conversational prompt. Neither is required — partial leads (Telegram ID only) are still valuable.
2. **21-Day Commercial Cooldown:** No CPSC conversion evaluation occurs within 21 days of lead capture. This prevents the perception that trivia is a sales funnel.
3. **Referral Attribution:** `referred_by_user_id` links the new lead to the member who invited them, enabling referral tracking.

---

## 4. Implementation Plan

### Stage 1: New Member Detection
*DEP-ID:* `DEP-ENG-090`

**Steps:**
1. In `trivianar_engine.py`, add handler for `message.new_chat_members` Telegram event.
2. On new member join during active trivia session: insert into `trivia_leads` with `telegram_user_id`, `first_name`, `referred_by_user_id` (the invite link creator, if available).
3. Track the new member's trivia responses as normal in `trivia_responses`.

### Stage 2: Post-Stream Bot DM Flow
*DEP-ID:* `DEP-ENG-091`

**Steps:**
1. After stream ends: query `trivia_leads` for leads captured during this session with `phone_number IS NULL`.
2. For each: send bot DM via `sendMessage(chat_id=user_id)`:
   - Message: "🎉 Great job in today's trivia! Want to stay connected for future sessions?"
   - Send `ReplyKeyboardMarkup` with `KeyboardButton(text="Share my contact", request_contact=True)`.
3. On `contact` message received: update `trivia_leads.phone_number`.
4. Follow-up (24h later, if phone shared): "Thanks! What's your email so [Coach Name] can send you exclusive content?"
5. On email text reply: update `trivia_leads.email`.
6. Respect opt-outs: if user blocks the bot or doesn't respond, mark `nurture_status = 'passive'`.
7. Write receipt to Receipt Chain Guard documenting the data acquisition/PII event whenever contact data is explicitly captured.

### Stage 3: CBCS Warm Start Entry
*DEP-ID:* `DEP-ENG-092`

**Steps:**
1. After trivia session ends: for each lead with ≥3 qualifying question responses, generate `cbcs_initial_assessment` JSONB from qualifying mappings.
2. Store in `trivia_leads.cbcs_initial_assessment`.
3. Enqueue lead into Conscious Nurturing Architecture (FR-CBCS-14) with warm-start flag.
4. Set `commercial_cooldown_until = NOW() + INTERVAL '21 days'`.

---

## 5. Data Model

```sql
CREATE TABLE trivia_leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    telegram_user_id BIGINT NOT NULL, -- Identical equivalence to & joins against trivia_responses.user_id
    first_name VARCHAR(255),
    phone_number VARCHAR(30),
    email VARCHAR(255),
    referred_by_user_id BIGINT,
    coach_id UUID NOT NULL REFERENCES coaches(id),
    stream_id UUID,
    cbcs_initial_assessment JSONB,
    nurture_status VARCHAR(20) DEFAULT 'new', -- new, active, passive, converted
    commercial_cooldown_until TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_trivia_leads_coach ON trivia_leads(coach_id);
CREATE INDEX idx_trivia_leads_status ON trivia_leads(nurture_status);
CREATE UNIQUE INDEX idx_trivia_leads_unique_user ON trivia_leads(telegram_user_id, coach_id);
```

---

## 6. Tasks

- [ ] **Task 1:** Add `new_chat_members` handler to `trivianar_engine.py`.
- [ ] **Task 2:** Build post-stream bot DM flow (`request_contact` + email follow-up).
- [ ] **Task 3:** Implement CBCS warm start assessment (qualifying question aggregation).
- [ ] **Task 4:** Implement 21-day commercial cooldown enforcement.
- [ ] **Task 5:** Add `trivia_leads` table migration to Supabase.

---

## 7. Acceptance Criteria

- [ ] **AC1 (Auto-Detect):** A new user joins the Telegram group during trivia. Assert `trivia_leads` row created with `telegram_user_id` and `first_name`.
- [ ] **AC2 (Phone Capture):** After stream, bot sends DM with contact request. User shares contact. Assert `phone_number` stored.
- [ ] **AC3 (Email Capture):** 24h after phone shared, bot sends email prompt. User replies with email. Assert `email` stored.
- [ ] **AC4 (Warm Start):** Lead answers 5 qualifying questions. Assert `cbcs_initial_assessment` contains mapped behavioral parameters.
- [ ] **AC5 (Cooldown):** Lead captured on Day 1. Assert CPSC conversion evaluation is blocked until Day 22.
- [ ] **AC6 (Referral Attribution):** User A invites User B via invite link. User B joins. Assert `referred_by_user_id = User A's ID`.

---

## 8. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| FR-CA11-19 (Trivianar Engine) | Internal | Lead detection happens within the trivia session context. |
| FR-CBCS-14 (Nurturing Architecture) | Internal | Lead enters nurturing pipeline with warm-start data. |
| Telegram Bot API | External | DM capabilities require the bot to be able to message users privately. |

---

## 9. Testing Strategy

### Unit Tests
- **Warm Start Assessment:** Insert 5 qualifying responses with known CBCS mappings. Assert `cbcs_initial_assessment` aggregation produces expected values.
- **Cooldown Calculation:** Assert `commercial_cooldown_until` = `created_at + 21 days`.

### Integration Tests
- **Full Lead Flow:** New member joins → plays trivia → stream ends → receives DM → shares contact → assert all fields populated.
