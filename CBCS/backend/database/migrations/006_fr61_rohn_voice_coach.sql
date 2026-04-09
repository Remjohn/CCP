-- ============================================================
-- Migration 006: FR61 — Jim Rohn AI Voice Coach Engine
-- Created: 2026-04-06
-- Spec: FR61_Jim_Rohn_Voice_Coach_Engine_Tech_Spec.md §4.Stage7
-- ============================================================
-- 10 tables + Row Level Security policies for coach isolation
-- All tables enforce ADR-01 Single-Tenant Coach Isolation via RLS
-- ============================================================

-- 1. Coach identity and program state (FR61 §4.Stage7)
CREATE TABLE IF NOT EXISTS coaches (
    coach_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id TEXT UNIQUE NOT NULL,
    onboard_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    total_sessions INTEGER DEFAULT 0,
    active_program_tier TEXT DEFAULT 'full_program',
    availability_config JSONB DEFAULT '{}',
    timezone TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Session log (FR61 §4.Stage7 — referenced by story_bank, vocal_delivery, etc.)
CREATE TABLE IF NOT EXISTS sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    coach_id UUID REFERENCES coaches(coach_id) NOT NULL,
    session_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    session_type TEXT CHECK (session_type IN ('trigger','recording')) NOT NULL,
    duration_minutes INTEGER,
    depth_rating INTEGER CHECK (depth_rating BETWEEN 1 AND 5),
    emotional_baseline_arousal FLOAT,
    emotional_baseline_valence FLOAT,
    emotional_trajectory TEXT CHECK (emotional_trajectory IN ('ascending','stable','descending')),
    recordings_count INTEGER DEFAULT 0,
    questions_asked JSONB DEFAULT '[]',
    stories_extracted UUID[] DEFAULT '{}',
    contradictions_surfaced UUID[] DEFAULT '{}',
    topics_covered TEXT[] DEFAULT '{}',
    session_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Extracted stories from Phase 1 voice notes (FR61 §4.Stage7)
CREATE TABLE IF NOT EXISTS story_bank (
    story_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    coach_id UUID REFERENCES coaches(coach_id) NOT NULL,
    session_id UUID REFERENCES sessions(session_id),
    date_extracted TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    raw_transcript TEXT NOT NULL,
    topic_tags TEXT[] DEFAULT '{}',
    trigger_category_id TEXT,
    emotion_arousal FLOAT,
    emotion_valence FLOAT,
    narrative_arc TEXT,
    temporal_position TEXT CHECK (temporal_position IN ('past','present','future')),
    sensory_detail_score FLOAT CHECK (sensory_detail_score BETWEEN 0 AND 10),
    times_used_in_content INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Contradiction pairs detected across sessions (FR61 §4.Stage7)
CREATE TABLE IF NOT EXISTS philosophy_tensions (
    tension_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    coach_id UUID REFERENCES coaches(coach_id) NOT NULL,
    claim_a_text TEXT NOT NULL,
    claim_a_session_date TIMESTAMPTZ NOT NULL,
    claim_b_text TEXT NOT NULL,
    claim_b_session_date TIMESTAMPTZ NOT NULL,
    resolved BOOLEAN DEFAULT FALSE,
    resolution_text TEXT,
    resolution_date TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Assembled personal philosophy (FR61 §4.Stage7)
CREATE TABLE IF NOT EXISTS personal_philosophy (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    coach_id UUID REFERENCES coaches(coach_id) UNIQUE NOT NULL,
    core_beliefs JSONB DEFAULT '[]',
    unresolved_questions JSONB DEFAULT '[]',
    recurring_grievances JSONB DEFAULT '[]',
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Per-session prosody metrics (FR61 §4.Stage7)
CREATE TABLE IF NOT EXISTS vocal_delivery (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES sessions(session_id) NOT NULL,
    recording_id UUID,
    coach_id UUID REFERENCES coaches(coach_id) NOT NULL,
    wpm FLOAT,
    spm FLOAT,
    pitch_variance FLOAT,
    avg_iss FLOAT,
    rohn_pauses_detected INTEGER DEFAULT 0,
    filler_density FLOAT,
    sincerity_composite FLOAT,
    liwc_authenticity FLOAT,
    jitter FLOAT,
    shimmer FLOAT,
    emotional_loading_arousal FLOAT,
    emotional_loading_valence FLOAT,
    pin_iron_ratio FLOAT,
    measured_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 7. Per-recording video visual analysis (FR61 §4.Stage7)
CREATE TABLE IF NOT EXISTS video_delivery (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recording_id UUID NOT NULL,
    session_id UUID REFERENCES sessions(session_id) NOT NULL,
    coach_id UUID REFERENCES coaches(coach_id) NOT NULL,
    eye_contact_pct FLOAT,
    gaze_break_timestamps JSONB DEFAULT '[]',
    gesture_congruence_score FLOAT,
    facial_expression_congruence FLOAT,
    posture_engagement_map JSONB DEFAULT '[]',
    analyzed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 8. Scheduled recording sessions with reminder state (FR61 §4.Stage7)
CREATE TABLE IF NOT EXISTS scheduled_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES sessions(session_id),
    coach_id UUID REFERENCES coaches(coach_id) NOT NULL,
    scheduled_datetime TIMESTAMPTZ NOT NULL,
    duration_minutes INTEGER DEFAULT 60,
    batch_theme TEXT,
    recordings_planned INTEGER DEFAULT 0,
    reminder_48h_sent TIMESTAMPTZ,
    reminder_24h_sent TIMESTAMPTZ,
    script_delivered TIMESTAMPTZ,
    reminder_30min_sent TIMESTAMPTZ,
    status TEXT CHECK (status IN ('booked','confirmed','in_progress','completed','missed','rescheduled')) DEFAULT 'booked',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 9. Supportive scripts for recording sessions (FR61 §4.Stage7)
CREATE TABLE IF NOT EXISTS scripts (
    script_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES scheduled_sessions(id),
    coach_id UUID REFERENCES coaches(coach_id) NOT NULL,
    content_pieces JSONB NOT NULL DEFAULT '[]',
    pause_markers JSONB DEFAULT '[]',
    pin_data_points JSONB DEFAULT '[]',
    raw_coach_phrases_used TEXT[] DEFAULT '{}',
    voice_dna_compatibility_score FLOAT,
    delivered_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 10. Micro-improvement detections pending acknowledgment (FR61 §4.Stage7)
CREATE TABLE IF NOT EXISTS micro_improvements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    coach_id UUID REFERENCES coaches(coach_id) NOT NULL,
    metric_name TEXT NOT NULL,
    previous_value FLOAT NOT NULL,
    current_value FLOAT NOT NULL,
    delta_pct FLOAT NOT NULL,
    session_id UUID REFERENCES sessions(session_id),
    acknowledged BOOLEAN DEFAULT FALSE,
    acknowledged_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- Row Level Security (ADR-01 Coach Isolation)
-- ============================================================

ALTER TABLE story_bank ENABLE ROW LEVEL SECURITY;
ALTER TABLE philosophy_tensions ENABLE ROW LEVEL SECURITY;
ALTER TABLE personal_philosophy ENABLE ROW LEVEL SECURITY;
ALTER TABLE vocal_delivery ENABLE ROW LEVEL SECURITY;
ALTER TABLE video_delivery ENABLE ROW LEVEL SECURITY;
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE scheduled_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE scripts ENABLE ROW LEVEL SECURITY;
ALTER TABLE micro_improvements ENABLE ROW LEVEL SECURITY;

-- Policy: coach can only access their own data
CREATE POLICY coach_isolation_story_bank ON story_bank
    USING (coach_id = current_setting('app.current_coach_id')::UUID);

CREATE POLICY coach_isolation_philosophy_tensions ON philosophy_tensions
    USING (coach_id = current_setting('app.current_coach_id')::UUID);

CREATE POLICY coach_isolation_personal_philosophy ON personal_philosophy
    USING (coach_id = current_setting('app.current_coach_id')::UUID);

CREATE POLICY coach_isolation_vocal_delivery ON vocal_delivery
    USING (coach_id = current_setting('app.current_coach_id')::UUID);

CREATE POLICY coach_isolation_video_delivery ON video_delivery
    USING (coach_id = current_setting('app.current_coach_id')::UUID);

CREATE POLICY coach_isolation_sessions ON sessions
    USING (coach_id = current_setting('app.current_coach_id')::UUID);

CREATE POLICY coach_isolation_scheduled_sessions ON scheduled_sessions
    USING (coach_id = current_setting('app.current_coach_id')::UUID);

CREATE POLICY coach_isolation_scripts ON scripts
    USING (coach_id = current_setting('app.current_coach_id')::UUID);

CREATE POLICY coach_isolation_micro_improvements ON micro_improvements
    USING (coach_id = current_setting('app.current_coach_id')::UUID);
