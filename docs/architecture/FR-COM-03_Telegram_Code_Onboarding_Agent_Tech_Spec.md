# Tech-Spec: FR-COM-03 — Telegram Code Onboarding Agent

**Created:** 2026-03-30
**Status:** Ready for Development
**Version:** 1.0
**Architecture Reference:** ADR-01 (Coach Isolation), FR-COM-01 (Billing Middleware)
**Skill Implementation:** `CBCS/backend/onboarding/telegram_onboarding_agent.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

- `docs/other files/active lab archive/temporary lab/telegram_onboarding_architecture.md` — Special code flow, program data model, payment integration
- `docs/architecture/FR-COM-01_AFFiNE_Billing_Credit_System_Tech_Spec.md` — Billing middleware consumed during onboarding
- `docs/other files/active lab archive/temporary lab/affine_billing_architecture.md` — $4/user instant charge on first bot message

---

## 2. Overview

### Problem Statement
Coach clients currently have no self-service enrollment mechanism. Coaches must manually add each client to their AFFiNE workspace, manually configure the CBCS Telegram bot for that client, and manually report usage to billing. This creates three problems: (1) coaches are bottlenecked — every new client requires manual work; (2) client onboarding is slow — hours/days instead of minutes; (3) billing leakage — coaches forget to report usage, and $4 credits are never charged. The system needs a zero-friction enrollment flow where prospects self-enroll via a program code, the bot collects their information conversationally, and the backend auto-provisions everything without coach intervention.

### Solution
FR-COM-03 implements the **Telegram Code Onboarding Agent** — a Telegram bot flow where prospects enter a program-specific code (e.g., `TRANSFORM90`), the bot validates the code, collects client information (name, goal, contact details) via conversational prompts, and the backend auto-provisions the client: creates the CBCS profile, assigns them to the correct coach and program, reports the $4 CBCS credit to Stripe, adds the client to the coach's AFFiNE workspace, and schedules the first check-in message. Zero manual work from the coach.

### Scope
**In scope:**
- Telegram bot `/start` + code validation flow
- Conversational client intake (name, goal, optional fields)
- Auto-provisioning: CBCS profile → Stripe usage → AFFiNE workspace → scheduled check-in
- Code validation against program registry (FR-COM-04)
- Error handling (invalid code, duplicate client, expired program)

**Out of scope:**
- Program creation (FR-COM-04)
- Campaign/funnel page generation (FR-COM-04)
- Ongoing CBCS engagement (existing CBCS pipeline)
- Payment collection from the end-client (coaches handle their own model)

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role |
|---|---|---|
| `DEP-COM-007` | Telegram Onboarding Bot | OUTPUT — Telegram bot handling code-based enrollment. |
| `DEP-COM-008` | Client Onboarding API | OUTPUT — Backend endpoint processing enrollments. |
| `DEP-COM-001` | Billing Middleware | CONSUMED — $4 usage reported on first bot message. |
| `DEP-COM-009` | Program Registry | INPUT — Code → coach + program lookup (produced by FR-COM-04). |
| `DEP-ENG-041` | Receipt Chain Guard | AUDIT — Enrollment events hashed. |

### Technical Decisions

1. **Code-First (Not Link-First):** The prospect enters a code into the Telegram bot, not a deep link. This allows the code to be shared across any medium (Instagram bio, email, printed flyer, word of mouth) without requiring a specific URL. The bot link is generic; the code identifies the program.
2. **Conversational Intake (Not Form):** The bot collects information one question at a time (name, goal) via Telegram messages, not a web form. This feels personal and aligned with coaching culture. Fields are configurable per program in FR-COM-04.
3. **First-Message Billing Trigger:** The $4 CBCS credit is charged when the bot sends its FIRST message to the client (not during enrollment). This aligns with FR-COM-01's instant usage lock and prevents the "enroll-and-delete" billing exploit.

---

## 4. Implementation Plan

### Stage 1: Code Validation Flow
*Inputs:* Telegram message from prospect with code
*Outputs:* Validated code → coach + program resolution

```
Prospect opens Telegram bot → /start
Bot: "Welcome to Conscious Coaching! 🎯 Enter your program code:"
Prospect: "TRANSFORM90"
Bot → Backend: validate_code("TRANSFORM90")
Backend: Lookup program_codes table → code matches Coach B + "90-Day Transform"
Backend → Bot: VALID. Proceed with intake.
```

**Error paths:**
- Invalid code → "Sorry, that code wasn't found. Double-check it and try again."
- Expired program → "That program has ended. Contact your coach for the latest code."
- Program full (max_clients reached) → "That program is currently full. Contact your coach."

### Stage 2: Conversational Intake
*Inputs:* Validated code context
*Outputs:* Client profile data

**Default intake fields:**
1. "What's your first name?" → `first_name` (required)
2. "What's your #1 goal for this program?" → `primary_goal` (required)
3. "What's the best email to reach you?" → `email` (optional, configurable)

**Configurable per program:** Coaches can define additional intake questions (max 5) in FR-COM-04's program configuration. The bot dynamically adapts its conversational flow based on the program's `intake_fields` configuration.

### Stage 3: Auto-Provisioning
*Inputs:* Completed client intake data + validated program context
*Outputs:* Fully provisioned client

**Provisioning sequence (atomic — all succeed or all rollback):**

1. **Create CBCS Profile:** Insert client into the core `profiles` table with `coach_id`, `program_id`, `telegram_user_id`, and `intake_data`.
2. **Report Usage to Stripe:** Call FR-COM-01 billing middleware — flag usage for billing on first bot message.
3. **Add to AFFiNE:** Push client to coach's AFFiNE workspace client board via API (auto-appearing card).
4. **Schedule First Check-In:** Based on program's `check_in_schedule`, schedule the first CBCS message linking to this `profiles.id`.
5. **Confirm to Prospect:** "You're in, Maria! 🎉 Your first check-in arrives Monday."
6. **Notify Coach:** Push notification to coach's AFFiNE: "New client enrolled: Maria → 90-Day Transform."
7. **Write Receipt Chain Guard:** Hash enrollment event to DEP-ENG-041.

### Stage 4: Duplicate Detection
*Inputs:* Client Telegram ID or email
*Outputs:* Allow (new) or block (duplicate)

- Same Telegram user enrolling in the same program → **Block:** "You're already enrolled in this program!"
- Same Telegram user enrolling in a different program → **Allow:** Create new enrollment, inform coach.
- Same email across different Telegram accounts → **Warn coach** (possible duplicate client), allow enrollment pending coach review.

---

## 5. Data Model

### Table: `profiles` (Extension)

The core CMF system (Migration 003) defines the `profiles` table. The Onboarding Agent extends this table with enrollment-specific columns.

```sql
ALTER TABLE profiles 
    ADD COLUMN IF NOT EXISTS program_id UUID,
    ADD COLUMN IF NOT EXISTS telegram_user_id BIGINT UNIQUE,
    ADD COLUMN IF NOT EXISTS primary_goal TEXT,
    ADD COLUMN IF NOT EXISTS intake_data JSONB,
    ADD COLUMN IF NOT EXISTS enrollment_code VARCHAR(50),
    ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'active' CHECK (status IN (
        'active', 'paused', 'completed', 'dropped', 'billing_muted'
    )),
    ADD COLUMN IF NOT EXISTS first_message_sent BOOLEAN DEFAULT false,
    ADD COLUMN IF NOT EXISTS first_message_sent_at TIMESTAMP WITH TIME ZONE,
    ADD COLUMN IF NOT EXISTS billing_reported BOOLEAN DEFAULT false,
    ADD COLUMN IF NOT EXISTS enrolled_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ADD COLUMN IF NOT EXISTS completed_at TIMESTAMP WITH TIME ZONE,
    ADD COLUMN IF NOT EXISTS receipt_chain_block VARCHAR(100);

CREATE INDEX IF NOT EXISTS idx_profiles_program ON profiles(program_id);
CREATE INDEX IF NOT EXISTS idx_profiles_telegram ON profiles(telegram_user_id);
```

### Table: `onboarding_events`

```sql
CREATE TABLE IF NOT EXISTS onboarding_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    telegram_user_id BIGINT NOT NULL,
    event_type VARCHAR(30) NOT NULL CHECK (event_type IN (
        'code_entered', 'code_valid', 'code_invalid', 'code_expired',
        'program_full', 'intake_started', 'intake_completed',
        'provisioning_started', 'provisioning_completed', 'provisioning_failed',
        'duplicate_blocked'
    )),
    program_code VARCHAR(50),
    coach_id UUID,
    program_id UUID,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_onboarding_telegram ON onboarding_events(telegram_user_id);
```

---

## 6. Backward Compatibility

Existing CBCS clients (manually added before the Telegram onboarding agent) remain in the system inside the `profiles` table. Manual client addition via AFFiNE is still supported; it creates a `profiles` row with `enrollment_code: 'MANUAL'` and `telegram_user_id: NULL` (bot configured later).

---

## 7. Tasks

- [ ] **Task 1:** Build Telegram bot shell with `/start` handler and conversational state machine.
- [ ] **Task 2:** Implement code validation endpoint (`POST /api/onboarding/validate-code`).
- [ ] **Task 3:** Build conversational intake flow with configurable per-program fields.
- [ ] **Task 4:** Implement atomic auto-provisioning sequence (CBCS profile → Stripe → AFFiNE → schedule → confirm → notify → receipt).
- [ ] **Task 5:** Build duplicate detection (Telegram ID × program, email cross-check).
- [ ] **Task 6:** Implement first-message billing trigger (report $4 usage on first bot → client message).
- [ ] **Task 7:** Build error handling (invalid code, expired program, full program, provisioning failure rollback).
- [ ] **Task 8:** Register DEP-COM-007 and DEP-COM-008 in the dependency registry.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Happy Path):** Prospect enters valid code `TRANSFORM90`. Bot asks name + goal. Prospect answers. Assert: CBCS client created, coach notified in AFFiNE, check-in scheduled.
- [ ] **AC2 (Invalid Code):** Prospect enters `FAKE123`. Assert: Bot responds "code not found." No client created. `onboarding_events` logged as `code_invalid`.
- [ ] **AC3 (Billing Trigger):** Client enrolled. Bot sends first check-in. Assert: $4 usage reported to Stripe at first-message time. `first_message_sent: true`. `billing_reported: true`.
- [ ] **AC4 (Duplicate Block):** Same Telegram user enters `TRANSFORM90` again. Assert: Bot responds "You're already enrolled." No duplicate client created.
- [ ] **AC5 (Program Full):** Program has `max_clients: 30` and 30 enrolled. Prospect enters code. Assert: Bot responds "program is full." No enrollment.
- [ ] **AC6 (Zero Coach Work):** Complete the entire enrollment flow. Assert: Coach did NOT perform any manual action. Client appeared automatically in AFFiNE workspace.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| DEP-COM-007 (Onboarding Bot) | Output | Telegram bot. |
| DEP-COM-008 (Onboarding API) | Output | Backend enrollment endpoint. |
| DEP-COM-001 (Billing Middleware) | Consumed | $4 usage report. |
| DEP-COM-009 (Program Registry) | Input | Code → coach/program lookup (from FR-COM-04). |
| FR-COM-01 (Billing) | Prerequisite | Stripe subscription must exist before usage reporting. |
| FR-COM-04 (Campaign Manager) | Prerequisite | Programs and codes must exist before onboarding can validate them. |
| Telegram Bot API | External | Bot messaging. |
| Supabase | Infrastructure | Client data storage. |

---

## 10. Testing Strategy

### Unit Tests
- **Code Validation:** Test 5 valid codes, 5 invalid codes, 1 expired, 1 full program. Assert correct outcome for each.
- **Intake State Machine:** Simulate Telegram message sequence. Assert bot asks questions in correct order and stores responses.
- **Provisioning Atomicity:** Fail provisioning at step 3 (AFFiNE push). Assert steps 1-2 rolled back (no orphan CBCS client, no orphan Stripe usage).

### Integration Tests
- **Full Enrollment:** Real Telegram bot → code → intake → provisioning → verify client in database + AFFiNE + Stripe.
- **Billing Integration:** Enroll client → bot sends first message → verify Stripe usage record exists.

### Safety Tests
- **Rate Limiting:** Send 100 code validation requests in 10 seconds from same Telegram user. Assert rate limit kicks in after 5 (anti-abuse).
- **SQL Injection:** Enter `'; DROP TABLE cbcs_clients; --` as code. Assert parameterized queries prevent injection.
