-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- PROFILES TABLE
-- Extends the auth.users table (if using Supabase Auth) or stands alone
CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    telegram_chat_id BIGINT UNIQUE,
    first_name TEXT,
    last_name TEXT,
    capacity_score INTEGER CHECK (capacity_score >= 0 AND capacity_score <= 100),
    identity_pillar TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ASSESSMENTS TABLE
-- Stores the raw intake data
CREATE TABLE IF NOT EXISTS assessments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    answers JSONB NOT NULL, -- Stores the 12 dimensions
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- RLS POLICIES (Basic)
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE assessments ENABLE ROW LEVEL SECURITY;

-- Allow anonymous access for MVP (since we might not have Auth User yet)
-- In production, this should be restricted to the service role or authenticated users
CREATE POLICY "Allow Service Role full access to profiles" ON profiles
    FOR ALL
    USING (true)
    WITH CHECK (true);

CREATE POLICY "Allow Service Role full access to assessments" ON assessments
    FOR ALL
    USING (true)
    WITH CHECK (true);
