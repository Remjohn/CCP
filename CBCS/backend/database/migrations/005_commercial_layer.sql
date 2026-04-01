-- ==============================================================
-- Migration 005: Commercial Intelligence Layer
-- ==============================================================
-- FR-COM-01: AFFiNE Billing & Credit System tables
-- FR-COM-02: Global Admin Dashboard tables
-- FR-COM-03: Telegram Code Onboarding Agent tables
-- FR-COM-04: Program & Campaign Manager tables
-- ==============================================================
-- Date: 2026-03-30
-- Version: 1.1 (CBAR Stress Test amendments: Q5, Q8, Q9)
-- Prerequisites: 004_visual_control_layer.sql
-- ==============================================================

-- =====================================================
-- FR-COM-01: AFFiNE Billing & Credit System
-- =====================================================

-- Coach subscription state (synced from Stripe)
CREATE TABLE IF NOT EXISTS coach_subscriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coach_id UUID NOT NULL UNIQUE,
    stripe_customer_id VARCHAR(50) NOT NULL UNIQUE,
    stripe_subscription_id VARCHAR(50) NOT NULL UNIQUE,
    stripe_metered_item_id VARCHAR(50),
    tier VARCHAR(20) NOT NULL DEFAULT 'base' CHECK (tier IN (
        'free_trial', 'base', 'premium', 'concierge'
    )),
    weekly_base_price_cents INTEGER NOT NULL DEFAULT 2500,
    cbcs_unit_price_cents INTEGER NOT NULL DEFAULT 400,
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN (
        'active', 'past_due', 'cancelled', 'trialing', 'paused'
    )),
    payment_method_last4 VARCHAR(4),
    current_period_start TIMESTAMP WITH TIME ZONE,
    current_period_end TIMESTAMP WITH TIME ZONE,
    active_client_count INTEGER DEFAULT 0,
    total_weekly_cost_cents INTEGER DEFAULT 2500,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_sub_coach ON coach_subscriptions(coach_id);
CREATE INDEX idx_sub_status ON coach_subscriptions(status);

-- Billing event history
CREATE TABLE IF NOT EXISTS billing_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coach_id UUID NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    stripe_event_id VARCHAR(100) UNIQUE,
    amount_cents INTEGER,
    client_id UUID,
    description TEXT,
    receipt_chain_block VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_billing_coach ON billing_events(coach_id);
CREATE INDEX idx_billing_type ON billing_events(event_type);

-- Billing queue: async pre-billing buffer (CBAR Q5 — Metered Billing Race Condition)
CREATE TABLE IF NOT EXISTS billing_queue (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coach_id UUID NOT NULL,
    client_telegram_user_id BIGINT NOT NULL,
    program_id UUID,
    idempotency_key VARCHAR(200) NOT NULL UNIQUE, -- (coach_id + client_id + message_scheduled_at)
    scheduled_dispatch_at TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN (
        'pending', 'billed', 'failed', 'grace_dispatched'
    )),
    stripe_usage_record_id VARCHAR(100),
    retry_count INTEGER DEFAULT 0,
    billed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_billing_queue_status ON billing_queue(status);
CREATE INDEX idx_billing_queue_dispatch ON billing_queue(scheduled_dispatch_at);
CREATE INDEX idx_billing_queue_coach ON billing_queue(coach_id);


-- =====================================================
-- FR-COM-02: Global Admin Dashboard
-- =====================================================

-- Admin action audit log
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

-- Pipeline health snapshots (15-min cron)
CREATE TABLE IF NOT EXISTS pipeline_health_snapshots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    snapshot_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    active_renders INTEGER DEFAULT 0,
    failed_24h INTEGER DEFAULT 0,
    failed_by_type JSONB,
    avg_render_time_seconds FLOAT,
    gpu_utilization_pct FLOAT,
    total_active_coaches INTEGER,
    total_pending_review INTEGER,
    total_cbcs_users_week INTEGER,
    revenue_week_cents INTEGER,
    aws_cost_week_cents INTEGER,
    margin_pct FLOAT
);

CREATE INDEX idx_health_time ON pipeline_health_snapshots(snapshot_time);


-- =====================================================
-- FR-COM-03: Telegram Code Onboarding Agent
-- =====================================================

-- CBAR Q8 FIX: composite unique constraint to allow multi-coach enrollment
-- (telegram_user_id BIGINT UNIQUE was too restrictive -- one user can join multiple coaches)
ALTER TABLE profiles
    ADD COLUMN IF NOT EXISTS program_id UUID,
    ADD COLUMN IF NOT EXISTS telegram_user_id BIGINT,         -- NOT globally unique
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

-- Composite constraint: one enrollment per (telegram_user, coach)
ALTER TABLE profiles
    ADD CONSTRAINT uq_profiles_telegram_coach UNIQUE (telegram_user_id, coach_id);

CREATE INDEX IF NOT EXISTS idx_profiles_program ON profiles(program_id);
CREATE INDEX IF NOT EXISTS idx_profiles_telegram ON profiles(telegram_user_id);

-- Onboarding event tracking
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


-- =====================================================
-- FR-COM-04: Program & Campaign Manager
-- =====================================================

-- Coaching programs
CREATE TABLE IF NOT EXISTS coaching_programs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coach_id UUID NOT NULL,
    program_name VARCHAR(100) NOT NULL,
    description TEXT,
    duration_days INTEGER NOT NULL,
    check_in_schedule JSONB NOT NULL,
    max_clients INTEGER NOT NULL DEFAULT 30,
    current_enrolled INTEGER DEFAULT 0,
    client_price_display VARCHAR(20),
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

-- Campaigns
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

-- Analytics events: funnel view tracking (CBAR Q9 — Isolated from RLS layer)
CREATE TABLE IF NOT EXISTS analytics_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type VARCHAR(30) NOT NULL CHECK (event_type IN (
        'funnel_view', 'telegram_click', 'enrollment_complete'
    )),
    campaign_id UUID NOT NULL REFERENCES campaigns(id),
    coach_id UUID NOT NULL,           -- populated server-side from campaign_id
    signed_token_hash VARCHAR(100),   -- validates event authenticity, prevents inflation
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_analytics_campaign ON analytics_events(campaign_id);
CREATE INDEX idx_analytics_coach ON analytics_events(coach_id);

-- Materialized view: Admin Dashboard aggregates (strips coach_id — CBAR Q9)
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_campaign_analytics AS
SELECT
    DATE_TRUNC('day', ae.created_at)          AS day,
    ae.event_type,
    COUNT(*)                                   AS event_count,
    COUNT(DISTINCT ae.campaign_id)             AS active_campaigns
FROM analytics_events ae
GROUP BY 1, 2
WITH DATA;

CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_campaign_analytics
    ON mv_campaign_analytics (day, event_type);

-- Refresh schedule: run via pg_cron every 15 minutes
-- SELECT cron.schedule('refresh-campaign-analytics', '*/15 * * * *',
--     'REFRESH MATERIALIZED VIEW CONCURRENTLY mv_campaign_analytics');


-- =====================================================
-- Row-Level Security
-- =====================================================

ALTER TABLE coach_subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE billing_events ENABLE ROW LEVEL SECURITY;
-- admin_actions: No RLS (admin-only, service role access)
-- pipeline_health_snapshots: No RLS (admin-only, service role access)
ALTER TABLE onboarding_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE coaching_programs ENABLE ROW LEVEL SECURITY;
ALTER TABLE campaigns ENABLE ROW LEVEL SECURITY;

-- Coach-scoped read policies
CREATE POLICY "Coach sees own subscription" ON coach_subscriptions
    FOR SELECT USING (auth.uid() = coach_id);
CREATE POLICY "Coach sees own billing events" ON billing_events
    FOR SELECT USING (auth.uid() = coach_id);
CREATE POLICY "Coach sees own programs" ON coaching_programs
    FOR SELECT USING (auth.uid() = coach_id);
CREATE POLICY "Coach manages own programs" ON coaching_programs
    FOR ALL USING (auth.uid() = coach_id);
CREATE POLICY "Coach sees own campaigns" ON campaigns
    FOR SELECT USING (auth.uid() = coach_id);
CREATE POLICY "Coach manages own campaigns" ON campaigns
    FOR ALL USING (auth.uid() = coach_id);

-- Service role full access for all tables (platform backend)
CREATE POLICY "Service role: coach_subscriptions" ON coach_subscriptions FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Service role: billing_events" ON billing_events FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Service role: admin_actions" ON admin_actions FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Service role: pipeline_health_snapshots" ON pipeline_health_snapshots FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Service role: onboarding_events" ON onboarding_events FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Service role: coaching_programs" ON coaching_programs FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Service role: campaigns" ON campaigns FOR ALL USING (true) WITH CHECK (true);
