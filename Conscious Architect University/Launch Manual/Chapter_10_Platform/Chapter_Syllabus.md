# Chapter 10: The Platform (Telegram + Stripe)

**Chapter Goal:** Wire the scheduled voice tracking system via Telegram and the pay-per-use credit system via Stripe into a functioning client interaction loop
**Mastery Track:** CCP System Architect
**Launch Track:** Telegram bot deployed (scheduled accountability sessions), Stripe billing live (credit-based), onboarding flow functional
**Prerequisites:** Chapter 6 (Agentic Core — agent pipeline), Chapter 9 (Dashboard — where results appear)
**Estimated Time:** 8-10 hours

---

## CCP/CMF Reality Anchor

The platform has TWO client touchpoints: Telegram (for scheduled voice-based accountability tracking) and the AFFiNE workspace (for structured content delivery). **Telegram is NOT a 24/7 chatbot.** It sends scheduled accountability prompts at designated times. **The cadence is PROGRAM-DEPENDENT (e.g., 2-3x/week as defined in `PantryConfig`), not daily.** Clients respond with voice notes. The system processes async (STT → analysis → response), keeping sessions to 3-5 messages max. This is a SCHEDULED, BOUNDED interaction. Stripe handles pay-per-use credits, not subscriptions. Every GPU-second has a cost that flows back to the coach's balance.

---

## Codebase Map

| File | Location | Size | Status |
|------|----------|------|--------|
| `client_onboarding.py` | `src/ccp/services/` | 5KB | ✅ EXISTS |
| `spt_stage_engine.py` | `src/ccp/services/` | 9KB | ✅ EXISTS |
| `scheduled_monitor.py` | `src/ccp/agents/` | 17KB | ✅ EXISTS |
| `scheduled_monitor_service.py` | `src/ccp/services/` | 22KB | ✅ EXISTS |
| `groq_transcriber.py` | `src/ccp/services/` | 6KB | ✅ EXISTS |
| `failure_prevention_gates.py` | `src/ccp/services/` | 22KB | ✅ EXISTS |
| `circuit_breaker.py` | `src/ccp/services/` | — | ⚠️ VERIFY |

**Files referenced: 7** ✅

---

## Science Sources

| Source | Location | Type |
|--------|----------|------|
| `FR-COM-01_AFFiNE_Billing_Credit_System_Tech_Spec.md` (14KB) | `docs/architecture/` | Billing spec |
| `FR-COM-02_Global_Admin_Dashboard_Tech_Spec.md` (12KB) | `docs/architecture/` | Admin dashboard |
| `FR-COM-03_Telegram_Code_Onboarding_Agent_Tech_Spec.md` (13KB) | `docs/architecture/` | Onboarding spec |
| `FR-COM-04_Program_Campaign_Manager_Tech_Spec.md` (14KB) | `docs/architecture/` | Campaign manager |
| `telegram_onboarding_architecture.md` (6KB) | `docs/` | Telegram architecture |
| `FR_CBCS_02_Social_Penetration_Depth_Gauge_Tech_Spec.md` (11KB) | `docs/architecture/` | SPT depth gauge |
| `FR_CBCS_07_Telegram_Intimacy_Index_Tech_Spec.md` (9KB) | `docs/architecture/` | Telegram intimacy |
| `FR15_Scheduled_Monitor_Agent_Tech_Spec.md` (15KB) | `docs/architecture/` | Scheduler |
| `Digital Accountability Group Research Plan.md` (41KB) | `lab/Behavioural Change/` | Accountability research |
| `Variable Reinforcement in Digital Engagement.md` (50KB) | `lab/Behavioural Change/` | Engagement science |

---

## Unit Map

| Unit | Title | 🧠 Science Topic | UNLEARN | 📂 Code Files | 📄 Science Sources | Build Target | Verify |
|------|-------|-------------------|---------|---------------|-------------------|-------------|--------|
| 10.1 | Telegram Scheduled Voice Tracking | Webhook architecture (not long polling). Scheduled prompts: the bot initiates contact at configured times. Client responds with voice note → Whisper STT → async processing → confirmation message. 3-5 message session limit. Dopamine loops through scheduled accountability | "The bot is a chatbot." False — the bot is a scheduled accountability tracker. It initiates at set times, processes voice notes async, and limits interactions to 3-5 messages. It does NOT hold open-ended conversations | `scheduled_monitor.py`, `scheduled_monitor_service.py`, `groq_transcriber.py` | `FR-COM-03`, `FR15_Scheduled_Monitor_Agent_Tech_Spec.md`, `telegram_onboarding_architecture.md`, `Digital Accountability Group Research Plan.md` | 🤖 Build scheduled Telegram bot with voice note handling | Bot sends accountability prompt at configured time → client voice note processed → confirmation sent |
| 10.2 | Social Penetration Theory — SPT Stages | How intimacy builds over time (Altman & Taylor). 4 stages: Orientation → Exploratory → Affective → Stable. Why session depth must MATCH the client's SPT stage — pushing too deep too early triggers withdrawal | "Jump straight to deep coaching." False — SPT shows intimacy unfolds in layers. Session depth must match the client's current stage. The Telegram Intimacy Index tracks this progression quantitatively | `spt_stage_engine.py` (9KB) | `FR_CBCS_02_Social_Penetration_Depth_Gauge_Tech_Spec.md`, `FR_CBCS_07_Telegram_Intimacy_Index_Tech_Spec.md`, `Variable Reinforcement in Digital Engagement.md` | — | Read the SPT engine. Identify the 4 stages and their depth thresholds |
| 10.3 | Stripe Credits — Pay-Per-Use Economics | Credit-based billing (not subscription). Each GPU-second, each agent turn, each video render has a cost. Credits purchased in packages. Webhook signatures for payment verification. Fraud prevention via receipt chain | "Use monthly subscriptions." False — subscription pricing decouples cost from usage. Credits align cost with value: a coach who generates 10 videos pays more than one who generates 2. This prevents adverse selection | `client_onboarding.py`, `failure_prevention_gates.py` | `FR-COM-01_AFFiNE_Billing_Credit_System_Tech_Spec.md` | 🤖 Build credit deduction service integrated with Stripe webhooks | Purchase credits → balance increases → run pipeline → balance decreases by exact GPU cost |
| 10.4 | The Onboarding Flow — User → Client | How a new user becomes a client: Telegram invite → Voice DNA extraction → Coach profile matching → Workspace provisioning → First scheduled session. The full lifecycle in 5 automated steps | "Onboarding is manual." False — the entire flow from Telegram invite to first scheduled accountability session is automated. Voice DNA extraction happens during the FIRST voice note | `client_onboarding.py` (5KB) | `FR-COM-03_Telegram_Code_Onboarding_Agent_Tech_Spec.md`, `FR-COM-04_Program_Campaign_Manager_Tech_Spec.md` | 🤖 Build `commands/ccp-onboard-client.md` — harness command: PRE-FLIGHT (verify coach is onboarded) → INVITE (Telegram deep-link) → FIRST-VOICE (capture + STT) → VOICE-DNA (extract TTT baseline) → PROVISION (create workspace + graph node) → SCHEDULE (configure first accountability session) → CHECKPOINT. This is the CLIENT counterpart to `ccp-onboard.md` (coach, Ch4.11) | Execute `ccp-onboard-client {coach} {client}` → workspace created → first session scheduled |

---

## Quality Gates

- [x] **Unit Count Gate:** 4 units ✅
- [x] **5-File Gate:** 7 codebase + 10 science sources ✅
- [x] **Schedule-Based Gate:** Unit 10.1 correctly reflects scheduled voice tracking, NOT chatbot ✅
