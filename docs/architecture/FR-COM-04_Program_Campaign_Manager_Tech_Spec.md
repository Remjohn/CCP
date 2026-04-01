# Tech-Spec: FR-COM-04 — Program & Campaign Manager

**Created:** 2026-03-30
**Status:** Ready for Development
**Version:** 1.0
**Architecture Reference:** ADR-01 (Coach Isolation), FR-COM-01 (Billing), FR-COM-03 (Onboarding)
**Skill Implementation:** `CBCS/backend/programs/program_manager.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

- `docs/other files/active lab archive/temporary lab/telegram_onboarding_architecture.md` — Program data model, campaign structure, funnel generation
- `docs/architecture/FR-COM-01_AFFiNE_Billing_Credit_System_Tech_Spec.md` — Subscription required before program creation
- `docs/architecture/FR-COM-03_Telegram_Code_Onboarding_Agent_Tech_Spec.md` — Programs consumed by onboarding agent

---

## 2. Overview

### Problem Statement
Coaches currently have no structured way to create, configure, or manage coaching programs within the platform. There is no mechanism to define a "90-Day Transform" program with specific parameters (duration, check-in schedule, max clients, special enrollment code). There is no campaign system linking a program to a funnel page or tracking enrollment performance. Coaches resort to manual spreadsheets, disconnected landing pages, and ad-hoc Telegram group management. The platform has no structured program entity — making it impossible for the onboarding bot (FR-COM-03) to validate enrollment codes or auto-assign clients to the correct program.

### Solution
FR-COM-04 implements the **Program & Campaign Manager** — an AFFiNE Block-based system where coaches create structured coaching programs (with duration, schedule, pricing, max capacity, intake fields, and auto-generated enrollment codes), and then create campaigns that link those programs to branded funnel pages with Telegram bot integration. The system provides the `DEP-COM-009` Program Registry that FR-COM-03 (Onboarding Agent) queries to validate enrollment codes and auto-assign clients.

### Scope
**In scope:**
- Program creation and configuration (AFFiNE Block)
- Auto-generated unique enrollment codes per program
- Campaign creation linking program → funnel → code
- Funnel one-pager generation (branded landing page per campaign)
- Program Registry API consumed by FR-COM-03
- Client capacity tracking and enrollment status

**Out of scope:**
- Client enrollment flow (FR-COM-03, Telegram Onboarding Agent)
- Billing for programs (FR-COM-01, coaches handle client-side payments)
- Ongoing CBCS engagement after enrollment (existing CBCS pipeline)
- Content generation for campaigns (CMF pipeline)

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role |
|---|---|---|
| `DEP-COM-009` | Program Registry | OUTPUT — Programs + codes, consumed by FR-COM-03. |
| `DEP-COM-010` | Campaign Manager | OUTPUT — Campaign → program → funnel linking. |
| `DEP-COM-011` | Funnel Page Generator | OUTPUT — Auto-generated branded landing pages. |
| `DEP-COM-001` | Billing Middleware | GATE — Coach must have active subscription to create programs. |
| `DEP-COM-004` | AFFiNE Wallet Block | SIBLING — Billing status visible alongside program management. |
| `DEP-ENG-041` | Receipt Chain Guard | AUDIT — Program creation and campaign launch events. |

### Technical Decisions

1. **AFFiNE Block (Not Standalone App):** Programs and campaigns are managed inside the coach's AFFiNE workspace using custom BlockSuite blocks. This keeps everything in one place — the coach never leaves AFFiNE to manage programs, billing, or clients.
2. **Auto-Generated Codes:** Special codes are auto-generated (8-char alphanumeric, e.g., `TRANS90A`) and guaranteed unique across the platform. Coaches can override with a custom code (validated for uniqueness).
3. **Funnel as Static Page:** Each campaign generates a simple branded one-pager (coach name, program description, Telegram bot link). Hosted on S3/CloudFront. No dynamic backend required for the funnel page itself — it's purely a static HTML page with the bot link.
4. **Capacity Enforcement at Registry Level:** `max_clients` is enforced in the Program Registry query (FR-COM-03 checks available capacity before allowing enrollment), not in the bot conversation.

---

## 4. Implementation Plan

### Stage 1: Program Creation Block
*Inputs:* Coach configures program via AFFiNE custom block
*Outputs:* Program record in database + auto-generated code + Write creation event hash → Receipt Chain Guard (DEP-ENG-041)

**Program Configuration Fields:**

| Field | Type | Required? | Example |
|---|---|---|---|
| `program_name` | String | Yes | "90-Day Transform" |
| `description` | Text | Yes | "A comprehensive 90-day coaching journey..." |
| `duration_days` | Integer | Yes | 90 |
| `check_in_schedule` | Enum[] | Yes | ["monday", "wednesday", "friday"] |
| `max_clients` | Integer | Yes | 30 |
| `client_price` | String | No | "$197" (display only — coach collects independently) |
| `enrollment_code` | String | Auto | `TRANS90A` (auto-generated, coach can override) |
| `intake_fields` | JSON | No | ["first_name", "primary_goal", "email", "age_range"] |
| `start_date` | Date | No | 2026-04-01 (null = rolling enrollment) |
| `end_date` | Date | No | 2026-06-30 |
| `status` | Enum | Auto | `enrolling`, `active`, `completed`, `archived` |

### Stage 2: Campaign Creation
*Inputs:* Coach links a program to a campaign
*Outputs:* Campaign record + funnel URL + shareable Telegram link + Write creation event hash → Receipt Chain Guard (DEP-ENG-041)

**Campaign Configuration Fields:**

| Field | Type | Required? | Example |
|---|---|---|---|
| `campaign_name` | String | Yes | "March Launch" |
| `program_id` | UUID | Yes | → "90-Day Transform" |
| `enrollment_code` | String | Inherited | From program (can override per campaign) |
| `funnel_url` | String | Auto | `conscious.co/coach-b/transform` |
| `telegram_bot_link` | String | Auto | `t.me/ccp_bot?start=TRANS90A` |
| `start_date` | Date | No | 2026-03-15 |
| `end_date` | Date | No | 2026-04-01 |
| `status` | Enum | Auto | `draft`, `live`, `paused`, `ended` |

### Stage 3: Funnel One-Pager Generator
*Inputs:* Campaign configuration + coach branding
*Outputs:* Static HTML page hosted on S3/CloudFront

**Page components:**
- Coach name and headshot (from LoRA reference photos or uploaded)
- Program name and description
- Key selling points (auto-extracted from program description)
- CTA button: "Join via Telegram" → links to `t.me/ccp_bot?start={CODE}`
- Coach branding (colors from AFFiNE workspace settings)
- Mobile-responsive single-page design

**Hosting:** Static HTML + CSS deployed to S3 with CloudFront CDN. URL pattern: `{subdomain}.conscious.co/{campaign-slug}`. SSL via ACM certificate.

### Stage 4: Program Registry API
*Outputs:* API endpoint consumed by FR-COM-03 (Telegram Onboarding Agent)

```
POST /api/programs/validate-code
Request:  { "code": "TRANS90A" }
Response: {
    "valid": true,
    "coach_id": "uuid-...",
    "program_id": "uuid-...",
    "program_name": "90-Day Transform",
    "available_capacity": 12,        // max_clients - current_enrolled
    "intake_fields": ["first_name", "primary_goal", "email"],
    "check_in_schedule": ["monday", "wednesday", "friday"],
    "status": "enrolling"
}
```

**Error responses:**
- `{"valid": false, "reason": "CODE_NOT_FOUND"}`
- `{"valid": false, "reason": "PROGRAM_FULL"}`
- `{"valid": false, "reason": "PROGRAM_EXPIRED"}`
- `{"valid": false, "reason": "CAMPAIGN_PAUSED"}`

---

## 5. Data Model

### Table: `coaching_programs`

```sql
CREATE TABLE IF NOT EXISTS coaching_programs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coach_id UUID NOT NULL,
    program_name VARCHAR(100) NOT NULL,
    description TEXT,
    duration_days INTEGER NOT NULL,
    check_in_schedule JSONB NOT NULL,                -- ["monday", "wednesday", "friday"]
    max_clients INTEGER NOT NULL DEFAULT 30,
    current_enrolled INTEGER DEFAULT 0,
    client_price_display VARCHAR(20),                -- "$197" (display only)
    enrollment_code VARCHAR(50) NOT NULL UNIQUE,
    intake_fields JSONB DEFAULT '["first_name", "primary_goal"]',
    start_date DATE,
    end_date DATE,
    status VARCHAR(20) DEFAULT 'enrolling' CHECK (status IN (
        'draft', 'enrolling', 'active', 'completed', 'archived'
    )),
    receipt_chain_block VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_programs_coach ON coaching_programs(coach_id);
CREATE UNIQUE INDEX idx_programs_code ON coaching_programs(enrollment_code);

ALTER TABLE coaching_programs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Coach sees own programs"
    ON coaching_programs FOR SELECT
    USING (auth.uid() = coach_id);
CREATE POLICY "Coach manages own programs"
    ON coaching_programs FOR ALL
    USING (auth.uid() = coach_id);
```

### Table: `campaigns`

```sql
CREATE TABLE IF NOT EXISTS campaigns (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coach_id UUID NOT NULL,
    program_id UUID NOT NULL REFERENCES coaching_programs(id),
    campaign_name VARCHAR(100) NOT NULL,
    enrollment_code_override VARCHAR(50),
    funnel_url TEXT,
    funnel_s3_path TEXT,
    telegram_bot_link TEXT,
    start_date DATE,
    end_date DATE,
    total_enrollments INTEGER DEFAULT 0,
    total_funnel_views INTEGER DEFAULT 0,
    conversion_rate FLOAT,
    status VARCHAR(20) DEFAULT 'draft' CHECK (status IN (
        'draft', 'live', 'paused', 'ended'
    )),
    receipt_chain_block VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_campaigns_coach ON campaigns(coach_id);
CREATE INDEX idx_campaigns_program ON campaigns(program_id);

ALTER TABLE campaigns ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Coach sees own campaigns"
    ON campaigns FOR SELECT
    USING (auth.uid() = coach_id);
CREATE POLICY "Coach manages own campaigns"
    ON campaigns FOR ALL
    USING (auth.uid() = coach_id);
```

---

## 6. Backward Compatibility

Programs and campaigns are new entities. No existing system is replaced. Coaches who have been manually managing clients can continue to do so. The Program Manager adds structure on top, not a replacement. Existing CBCS clients (added manually) are NOT retroactively assigned to programs — they exist as standalone clients with `program_id: NULL`.

---

## 7. Tasks

- [ ] **Task 1:** Design and build AFFiNE Program Creation Block (BlockSuite custom block).
- [ ] **Task 2:** Implement program creation API (`POST /api/programs`) with auto-code generation.
- [ ] **Task 3:** Build enrollment code auto-generator (8-char alphanumeric, uniqueness guarantee).
- [ ] **Task 4:** Design and build AFFiNE Campaign Creation Block.
- [ ] **Task 5:** Implement campaign creation API with auto-generated funnel URL and Telegram link.
- [ ] **Task 6:** Build Funnel One-Pager Generator (HTML template → S3/CloudFront deployment).
- [ ] **Task 7:** Implement Program Registry API (`POST /api/programs/validate-code`) for FR-COM-03.
- [ ] **Task 8:** Build capacity tracking (increment `current_enrolled` on enrollment, decrement on drop).
- [ ] **Task 9:** Build campaign analytics (funnel views, enrollments, conversion rate).
- [ ] **Task 10:** Register DEP-COM-009, DEP-COM-010, DEP-COM-011 in the dependency registry.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Program Creation):** Coach creates "90-Day Transform" program in AFFiNE. Assert: Program record created in database. Enrollment code auto-generated and unique. `status: enrolling`.
- [ ] **AC2 (Code Uniqueness):** Two coaches create programs. Assert: Both codes are globally unique. If Coach B enters Coach A's code as a custom override, system rejects it.
- [ ] **AC3 (Campaign Launch):** Coach creates campaign for "90-Day Transform". Assert: Funnel URL generated. Telegram link generated with embedded code. Static page deployed to S3.
- [ ] **AC4 (Registry Query):** FR-COM-03 sends `validate-code("TRANS90A")`. Assert: Response contains correct `coach_id`, `program_name`, `available_capacity`, `intake_fields`.
- [ ] **AC5 (Capacity Enforcement):** Program has `max_clients: 30`, `current_enrolled: 30`. Assert: Registry query returns `{"valid": false, "reason": "PROGRAM_FULL"}`.
- [ ] **AC6 (Campaign Paused):** Admin pauses a campaign. Assert: Registry query returns `{"valid": false, "reason": "CAMPAIGN_PAUSED"}`. No new enrollments accepted.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| DEP-COM-009 (Program Registry) | Output | Programs + codes consumed by FR-COM-03. |
| DEP-COM-010 (Campaign Manager) | Output | Campaign → program → funnel linking. |
| DEP-COM-011 (Funnel Generator) | Output | Static landing pages on S3. |
| DEP-COM-001 (Billing Middleware) | Gate | Active subscription required for program creation. |
| FR-COM-03 (Onboarding Agent) | Downstream | Consumes program registry for code validation. |
| AWS S3 + CloudFront | Infrastructure | Funnel page hosting. |
| AFFiNE BlockSuite | Framework | Custom blocks for program/campaign management. |

---

## 10. Testing Strategy

### Unit Tests
- **Code Generation:** Generate 1,000 codes. Assert all unique. Assert all 8-char alphanumeric.
- **Capacity Math:** Program with `max_clients: 30`, `current_enrolled: 28`. Assert `available_capacity: 2`. Enroll 2. Assert `available_capacity: 0`. Attempt enroll → assert `PROGRAM_FULL`.
- **Status Transitions:** Assert `draft` → `enrolling` → `active` → `completed` → `archived` transitions are valid. Assert invalid transitions (e.g., `archived` → `enrolling`) are blocked.

### Integration Tests
- **Full Campaign Launch:** Create program → create campaign → deploy funnel → access funnel URL → click Telegram link → verify bot flow starts with correct code.
- **Cross-FR Integration:** Create program in FR-COM-04 → enroll client via FR-COM-03 → verify billing via FR-COM-01 → verify client appears in coach's AFFiNE.

### Safety Tests
- **Coach Isolation:** Coach A creates a program. Coach B attempts to modify it via API. Assert: 403 — RLS blocks cross-tenant access.
- **Code Enumeration:** Attempt to brute-force validate 10,000 codes. Assert rate limiting kicks in after 20 requests/minute for non-authenticated callers.
