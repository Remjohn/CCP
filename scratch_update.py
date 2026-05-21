filepath = 'd:\\Work\\The Conscious Coaching Factory\\src\\ccp\\scripts\\setup_supabase.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
target = '\n"""'
replacement = '''

-- FR-ERA3-17 Voice Prompt Engine Tables
CREATE TABLE IF NOT EXISTS voice_prompt_packets (
    voice_prompt_id              TEXT PRIMARY KEY,
    coach_id                     TEXT NOT NULL,
    user_id                      TEXT NOT NULL,
    emotional_job                TEXT NOT NULL,
    job_selection_reason         TEXT NOT NULL,
    delivery_surface             TEXT NOT NULL,
    locale                       TEXT NOT NULL,
    script_text                  TEXT NOT NULL,
    voice_dna_profile_ref        TEXT NOT NULL,
    render_source_preference     TEXT NOT NULL,
    prompt_status                TEXT NOT NULL,
    created_at                   TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_vpp_coach ON voice_prompt_packets(coach_id);
CREATE INDEX IF NOT EXISTS idx_vpp_user ON voice_prompt_packets(user_id);
ALTER TABLE voice_prompt_packets ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS voice_prompt_render_attempts (
    render_attempt_id            TEXT PRIMARY KEY,
    voice_prompt_id              TEXT NOT NULL,
    render_source                TEXT NOT NULL,
    provider_reference           TEXT NOT NULL,
    audio_asset_id               TEXT,
    sample_rate_hz               INTEGER NOT NULL,
    duration_seconds             INTEGER NOT NULL,
    prestige_gate_passed         BOOLEAN NOT NULL DEFAULT FALSE,
    rejection_reason             TEXT,
    created_at                   TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_vpra_prompt ON voice_prompt_render_attempts(voice_prompt_id);
ALTER TABLE voice_prompt_render_attempts ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS voice_prompt_delivery_records (
    delivery_id                  TEXT PRIMARY KEY,
    voice_prompt_id              TEXT NOT NULL,
    delivery_surface             TEXT NOT NULL,
    delivery_status              TEXT NOT NULL,
    retry_count                  INTEGER NOT NULL DEFAULT 0,
    telegram_chat_id             TEXT,
    dispatched_at                TIMESTAMPTZ,
    created_at                   TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_vpdr_prompt ON voice_prompt_delivery_records(voice_prompt_id);
ALTER TABLE voice_prompt_delivery_records ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS voice_prompt_fallback_packs (
    fallback_pack_id             TEXT PRIMARY KEY,
    coach_id                     TEXT NOT NULL,
    emotional_job                TEXT NOT NULL,
    locale                       TEXT NOT NULL,
    audio_asset_id               TEXT NOT NULL,
    transcript_reference         TEXT NOT NULL,
    duration_seconds             INTEGER NOT NULL,
    created_at                   TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_vpfp_coach_job ON voice_prompt_fallback_packs(coach_id, emotional_job);
ALTER TABLE voice_prompt_fallback_packs ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS voice_prompt_telemetry (
    telemetry_id                 TEXT PRIMARY KEY,
    voice_prompt_id              TEXT NOT NULL,
    replay_count                 INTEGER NOT NULL DEFAULT 0,
    completion_count             INTEGER NOT NULL DEFAULT 0,
    forward_count                INTEGER NOT NULL DEFAULT 0,
    reply_count                  INTEGER NOT NULL DEFAULT 0,
    resonance_marker             BOOLEAN NOT NULL DEFAULT FALSE,
    recorded_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_vpt_prompt ON voice_prompt_telemetry(voice_prompt_id);
ALTER TABLE voice_prompt_telemetry ENABLE ROW LEVEL SECURITY;
"""'''
if target in content:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.replace(target, replacement))
    print("OK")
else:
    print("Target not found.")
