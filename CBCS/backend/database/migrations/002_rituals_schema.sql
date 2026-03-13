-- RITUALS TABLE
-- Stores the "Lego Blocks" of the coaching program
CREATE TABLE IF NOT EXISTS rituals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    description TEXT,
    level_threshold INTEGER CHECK (level_threshold >= 0 AND level_threshold <= 100), -- Min capacity required
    identity_fit TEXT[], -- Array of strings (e.g., ['The Builder', 'The Rebel'])
    goal_fit TEXT, -- Primary pain/goal (e.g., 'Anxiety', 'Focus')
    media_url TEXT,
    script_template TEXT, -- The base script to be modified by the Artisan
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- RLS
ALTER TABLE rituals ENABLE ROW LEVEL SECURITY;

-- Allow read access to everyone (or authenticated users)
CREATE POLICY "Allow Service Role full access to rituals" ON rituals
    FOR ALL
    USING (true)
    WITH CHECK (true);
