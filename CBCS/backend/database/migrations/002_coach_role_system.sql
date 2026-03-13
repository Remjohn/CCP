-- Migration 002: Coach Role System
-- Epic 18.1: Coach Registry
-- Adds role-based routing support for distinguishing coaches from users

-- 1. Add role column to profiles
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS role TEXT NOT NULL DEFAULT 'user'
    CHECK (role IN ('user', 'coach', 'admin'));

-- 2. Add coach_id to profiles (links users to their coach)
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS coach_id UUID REFERENCES profiles(id);

-- 3. Coach Configurations table (per-coach settings)
CREATE TABLE IF NOT EXISTS coach_configs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coach_id UUID UNIQUE NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    
    -- Identity
    coach_name TEXT NOT NULL,
    coach_display_name TEXT,
    
    -- Delivery Schedule
    interview_day TEXT DEFAULT 'monday' CHECK (interview_day IN ('monday','tuesday','wednesday','thursday','friday','saturday','sunday')),
    interview_time TEXT DEFAULT '09:00',
    ideas_day TEXT DEFAULT 'thursday' CHECK (ideas_day IN ('monday','tuesday','wednesday','thursday','friday','saturday','sunday')),
    ideas_time TEXT DEFAULT '09:00',
    recording_day TEXT DEFAULT 'saturday' CHECK (recording_day IN ('monday','tuesday','wednesday','thursday','friday','saturday','sunday')),
    recording_time TEXT DEFAULT '09:00',
    timezone TEXT DEFAULT 'Europe/Paris',
    
    -- Content Preferences
    content_format TEXT DEFAULT 'mixed' CHECK (content_format IN ('tierlist', 'rating', 'mixed', 'auto')),
    ideas_per_week INTEGER DEFAULT 3 CHECK (ideas_per_week >= 1 AND ideas_per_week <= 5),
    preferred_archetypes TEXT[] DEFAULT ARRAY['authority', 'controversial', 'roast', 'relatable'],
    
    -- API Tokens (encrypted references, not raw keys)
    telegram_bot_token_env TEXT DEFAULT 'TELEGRAM_BOT_TOKEN',
    openrouter_api_key_env TEXT DEFAULT 'OPENROUTER_API_KEY',
    
    -- Paths (relative to coach's project root)
    project_root TEXT,
    intelligence_library_path TEXT DEFAULT 'intelligence_library',
    
    -- State
    current_week TEXT,  -- ISO week e.g., '2026-W08'
    last_interview_at TIMESTAMP WITH TIME ZONE,
    last_ideas_sent_at TIMESTAMP WITH TIME ZONE,
    last_recording_prep_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Coach Content Ideas table (tracks generated ideas and selections)
CREATE TABLE IF NOT EXISTS coach_content_ideas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coach_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    week_id TEXT NOT NULL,  -- e.g., '2026-W08'
    
    ideas JSONB NOT NULL,  -- Array of idea objects
    selected_idea_index INTEGER,  -- Which idea the coach picked (0-indexed)
    
    -- Lifecycle
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    sent_at TIMESTAMP WITH TIME ZONE,
    selected_at TIMESTAMP WITH TIME ZONE,
    recording_prepped_at TIMESTAMP WITH TIME ZONE,
    
    UNIQUE(coach_id, week_id)
);

-- 5. User Activity Tracking (for coach alerts)
CREATE TABLE IF NOT EXISTS user_activity_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    coach_id UUID NOT NULL REFERENCES profiles(id),
    
    activity_type TEXT NOT NULL CHECK (activity_type IN ('message', 'voice_note', 'assessment', 'ritual_completed', 'journal')),
    metadata JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 6. Indexes
CREATE INDEX IF NOT EXISTS idx_profiles_role ON profiles(role);
CREATE INDEX IF NOT EXISTS idx_profiles_coach ON profiles(coach_id);
CREATE INDEX IF NOT EXISTS idx_profiles_telegram ON profiles(telegram_chat_id);
CREATE INDEX IF NOT EXISTS idx_coach_configs_coach ON coach_configs(coach_id);
CREATE INDEX IF NOT EXISTS idx_content_ideas_coach_week ON coach_content_ideas(coach_id, week_id);
CREATE INDEX IF NOT EXISTS idx_activity_log_user ON user_activity_log(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_activity_log_coach ON user_activity_log(coach_id, created_at DESC);

-- 7. RLS Policies for coach_configs
ALTER TABLE coach_configs ENABLE ROW LEVEL SECURITY;
ALTER TABLE coach_content_ideas ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_activity_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Service role full access to coach_configs" ON coach_configs
    FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY "Service role full access to coach_content_ideas" ON coach_content_ideas
    FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY "Service role full access to user_activity_log" ON user_activity_log
    FOR ALL USING (true) WITH CHECK (true);
