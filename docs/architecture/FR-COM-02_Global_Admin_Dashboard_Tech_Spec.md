# Tech-Spec: FR-COM-02 — Global Admin Dashboard (Factory Floor)

**Created:** 2026-03-30
**Status:** Ready for Development
**Version:** 1.0
**Architecture Reference:** ADR-01 (Coach Isolation — Hub Exception), SPEC-INFRA-001
**Skill Implementation:** `CBCS/frontend/admin-dashboard/`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

- `docs/other files/active lab archive/temporary lab/global_admin_dashboard_architecture.md` — Hub-and-Spoke model, Factory Floor, Traffic Control, Treasury
- `docs/other files/active lab archive/temporary lab/affine_billing_architecture.md` — Billing state consumed by Treasury view
- `docs/architecture/Infrastructure_AWS_NIM_Deployment_Spec.md` — GPU metrics consumed by Traffic Control
- `CBCS/backend/database/migrations/003_full_schema.sql` — Existing schema

---

## 2. Overview

### Problem Statement
At scale (50+ coaches), the platform operator cannot log into each coach's isolated AFFiNE workspace to review content, monitor pipeline health, or track billing. There is no centralized command center. Video review requires navigating to individual workspaces. Pipeline failures are invisible until a coach complains. Billing issues are discovered only when Stripe sends a dunning email. The multi-tenant architecture that protects coach privacy also creates an operational blindspot for the platform owner.

### Solution
FR-COM-02 implements the **Global Admin Dashboard** (code-named "Factory Floor") — a centralized Next.js web application with God-level read access across all tenant data. It provides three views: (A) Factory Floor — unified video/content review queue with one-click approve/reject/regenerate; (B) Traffic Control — real-time pipeline health, GPU utilization, failure rates, and coach engagement monitoring; (C) Treasury — global billing status, revenue metrics, CBCS credit counts, and AWS cost vs Stripe revenue comparison. The dashboard queries the central Supabase database using a service-role key (bypassing RLS) and presents aggregated views that no individual coach can access.

### Scope
**In scope:**
- Factory Floor view (unified review queue, approve/reject/regenerate actions)
- Traffic Control view (pipeline health, GPU metrics, coach engagement alerts)
- Treasury view (billing status, revenue, cost ratio, failed payments)
- Hub-and-Spoke data flow (coach workspaces → central DB → dashboard)
- Authentication (admin-only, not coach-accessible)

**Out of scope:**
- Coach-facing dashboard (coaches use AFFiNE workspace, not this dashboard)
- Content creation or editing (admin reviews, does not create)
- Individual coach AFFiNE workspace management

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role |
|---|---|---|
| `DEP-COM-005` | Admin Dashboard App | OUTPUT — Next.js web application. |
| `DEP-COM-006` | Unified Review Queue API | OUTPUT — Aggregated pending-review endpoint. |
| `DEP-COM-003` | Redis Permission State | INPUT — Coach billing status for Treasury view. |
| `DEP-ENG-041` | Receipt Chain Guard | AUDIT — Admin actions (approve/reject) recorded. |
| All coach tables | INPUT | Service-role queries bypass RLS for aggregation. |

### Technical Decisions

1. **Separate App (Not AFFiNE):** The dashboard is a standalone Next.js/React Admin app, completely separate from coach AFFiNE workspaces. Coaches do NOT have accounts on the admin dashboard. This maintains ADR-01 coach isolation — coaches pull from their siloes; the admin queries the global ocean.
2. **Service-Role Key:** The dashboard authenticates to Supabase using the `service_role` key, which bypasses Row-Level Security. This is the ONLY application in the ecosystem with this privilege. All other applications (coach AFFiNE, Telegram bots, CMF pipeline) use `anon` or coach-scoped keys.
3. **WebSocket for Real-Time:** Pipeline state changes push to the dashboard via Supabase Realtime (WebSocket). The admin sees video completions, failures, and billing events in real-time without polling.

---

## 4. Implementation Plan

### Stage 1: Factory Floor (Video Review Queue)
*Inputs:* All content with `status: pending_review` across all coaches
*Outputs:* Approve/Reject/Regenerate actions routed back to coach workspaces

**View Components:**
- **TikTok-style feed** OR **Kanban board** — toggleable display of all pending content
- Per-item metadata: coach name, program, content type, generation timestamp, pipeline stage
- **One-click actions:**
  - ✅ Approve → status: `approved` → push event to coach's AFFiNE workspace ("Your video is ready!") → Write action hash → Receipt Chain Guard (DEP-ENG-041)
  - 🔄 Regenerate → status: `regenerating` → re-trigger CMF pipeline for that content → Write action hash → Receipt Chain Guard (DEP-ENG-041)
  - ❌ Reject → status: `rejected` + notes field → push rejection reason to coach workspace → Write action hash → Receipt Chain Guard (DEP-ENG-041)
- **Filters:** By coach, by content type, by date range, by pipeline stage

### Stage 2: Traffic Control (Pipeline Health)
*Inputs:* CMF pipeline state, GPU metrics (CloudWatch), coach engagement data
*Outputs:* Health dashboard, alerts

**Metrics Panels:**
- "N videos currently rendering on NVIDIA NIMs"
- "N failed in last 24h (by failure type: audio sync, ControlNet, LoRA loading, timeout)"
- "Average render time: Xs (trend: up/down vs last week)"
- GPU utilization (% of A100/H100 capacity)

**Coach Engagement Alerts:**
- "Coach B hasn't submitted a voice note in 4 days" → Option to trigger Telegram nudge
- "Coach D has 0 videos in review queue (pipeline idle)" → Engagement risk flag
- "Coach A's LoRA needs retraining (identity drift detected)" → Flag for FR-VIS-17

**Bulk Actions:**
- Retry all failed pipeline stages (by failure type)
- Pause/resume pipeline for specific coach (maintenance)

### Stage 3: Treasury (Billing & Revenue)
*Inputs:* `coach_subscriptions`, `billing_events`, AWS Cost Explorer API
*Outputs:* Financial health dashboard

**Metrics Panels:**
- Total active coaches: N (by tier: base/premium/concierge)
- This week's CBCS credits injected: N end-users
- Revenue breakdown: Subscriptions ($X) + CBCS ($Y) = Total ($Z)
- **Friction Feed:** "Coach D's $25 weekly payment failed. Pipeline paused." → One-click "Send payment reminder"
- **Overhead Check:** "AWS/GPU cost this week: $X. Stripe revenue: $Y. Margin: Z%"
- Revenue trend chart (4-week rolling)

**Alerts:**
- Payment failure > 48h without resolution → Escalation flag
- AWS cost exceeding 40% of revenue → Warning
- CBCS churn: Coach lost > 5 clients in one week → Investigation flag

---

## 5. Data Model

### Table: `admin_actions`

```sql
CREATE TABLE IF NOT EXISTS admin_actions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    admin_user_id UUID NOT NULL,
    action_type VARCHAR(30) NOT NULL CHECK (action_type IN (
        'approve', 'reject', 'regenerate', 'pause_pipeline',
        'resume_pipeline', 'retry_failed', 'send_nudge', 'send_payment_reminder'
    )),
    target_coach_id UUID,
    target_content_id UUID,
    notes TEXT,
    receipt_chain_block VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_admin_actions_type ON admin_actions(action_type);
CREATE INDEX idx_admin_actions_coach ON admin_actions(target_coach_id);

-- No RLS — admin-only table, accessed only via service role
```

### Table: `pipeline_health_snapshots`

```sql
CREATE TABLE IF NOT EXISTS pipeline_health_snapshots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    snapshot_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    active_renders INTEGER DEFAULT 0,
    failed_24h INTEGER DEFAULT 0,
    failed_by_type JSONB,                           -- {"audio_sync": 2, "controlnet": 1}
    avg_render_time_seconds FLOAT,
    gpu_utilization_pct FLOAT,
    total_active_coaches INTEGER,
    total_pending_review INTEGER,
    total_cbcs_users_week INTEGER,
    revenue_week_cents INTEGER,
    aws_cost_week_cents INTEGER,
    margin_pct FLOAT
);

-- Snapshots taken every 15 minutes by a cron job
CREATE INDEX idx_health_time ON pipeline_health_snapshots(snapshot_time);
```

---

## 6. Backward Compatibility

The admin dashboard is a greenfield application. No existing system is replaced. Coach-facing AFFiNE workspaces remain unchanged. The dashboard reads from existing tables (via service-role) and writes only to `admin_actions` and `pipeline_health_snapshots`.

---

## 7. Tasks

- [ ] **Task 1:** Scaffold Next.js admin dashboard with authentication (admin-only, no coach access).
- [ ] **Task 2:** Build Factory Floor view: unified review queue with TikTok-feed/Kanban toggle.
- [ ] **Task 3:** Build approve/reject/regenerate action handlers with AFFiNE workspace push notifications.
- [ ] **Task 4:** Build Traffic Control view: GPU metrics (CloudWatch API), pipeline state, failure breakdown.
- [ ] **Task 5:** Build coach engagement alert system (voice note gaps, idle pipelines, LoRA drift).
- [ ] **Task 6:** Build Treasury view: revenue dashboard, cost ratio, friction feed.
- [ ] **Task 7:** Implement 15-minute health snapshot cron job.
- [ ] **Task 8:** Build Supabase Realtime WebSocket integration for live pipeline events.
- [ ] **Task 9:** Register DEP-COM-005 and DEP-COM-006 in the dependency registry.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Review Queue):** 3 coaches have pending videos. Assert: Factory Floor shows all pending items from all 3 coaches in a single view. Admin clicks "Approve" on one. Assert: Item status → `approved`, coach's AFFiNE workspace receives "Video ready!" notification.
- [ ] **AC2 (Rejection with Notes):** Admin rejects a video with note "Audio out of sync at 0:15." Assert: Coach's AFFiNE workspace shows the rejection reason. Content status → `rejected`.
- [ ] **AC3 (Traffic Control):** 2 renders are active, 1 failed (audio sync). Assert: Traffic Control shows "2 active, 1 failed (audio_sync: 1)". Admin clicks "Retry Failed" → failed render re-enters pipeline.
- [ ] **AC4 (Treasury):** 10 coaches on $25/week, 5 on $50/week, total 200 CBCS users. Assert: Treasury shows "Revenue: $500 + $800 = $1,300/week". AWS cost panel shows current week's GPU spend.
- [ ] **AC5 (Coach Isolation):** A coach attempts to access the admin dashboard URL. Assert: Authentication blocks access. 403 Forbidden. No coach can see another coach's data through the admin interface.
- [ ] **AC6 (Real-Time):** A video finishes rendering while admin has Factory Floor open. Assert: New item appears in the review queue within 5 seconds (WebSocket push, no page refresh needed).

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| DEP-COM-005 (Admin Dashboard) | Output | Next.js web application. |
| DEP-COM-006 (Review Queue API) | Output | Aggregated endpoint. |
| DEP-COM-001 (Billing Middleware) | Input | Subscription status for Treasury. |
| DEP-COM-003 (Redis State) | Input | Coach status for billing alerts. |
| Supabase Service Role | Infrastructure | Bypasses RLS for global queries. |
| Supabase Realtime | Infrastructure | WebSocket for live updates. |
| AWS CloudWatch API | External | GPU utilization metrics. |
| CMF Pipeline Commander | Integration | Pipeline state consumed. |

---

## 10. Testing Strategy

### Unit Tests
- **Access Control:** Assert admin token → 200 OK. Assert coach token → 403 Forbidden. Assert no token → 401 Unauthorized.
- **Action Routing:** Assert approve action updates content status AND pushes to correct coach workspace (not another coach's).

### Integration Tests
- **Full Review Flow:** CMF finishes render → content enters `pending_review` → appears in Factory Floor → admin approves → coach receives notification in AFFiNE.
- **Treasury Accuracy:** Create 5 test subscriptions with known billing. Assert Treasury revenue calculation matches expected total.

### Safety Tests
- **Cross-Tenant Leakage:** Admin approves Coach A's video. Assert no data from Coach B is affected.
- **Concurrent Admin:** Two admins approve the same video simultaneously. Assert idempotent handling (no double-approval, no duplicate notifications).
