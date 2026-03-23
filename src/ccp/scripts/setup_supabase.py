"""
CCP Supabase Schema Setup
Task 1.04 — Creates the required tables and storage buckets in Supabase.

Tables:
  - receipt_chain: Immutable audit logs
  - asset_registry: Universal Asset ID registry
  - person_registry: Person ID registry

Storage Buckets:
  - sacred-audio: Coach voice recordings
  - voice-notes: Client voice messages
  - coach-photos: Personal branding photos
  - visual-assets: Generated visual content

Usage:
    python -m src.ccp.scripts.setup_supabase
"""

import os
import sys

from supabase import create_client, Client


def get_supabase_client() -> Client:
    """Create a Supabase client from environment variables."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    if not url or not key:
        raise ValueError(
            "SUPABASE_URL and SUPABASE_SERVICE_KEY must be set"
        )
    return create_client(url, key)


# SQL for table creation (run via Supabase SQL editor or migration)
SCHEMA_SQL = """
-- Receipt Chain: Immutable audit log
CREATE TABLE IF NOT EXISTS receipt_chain (
    id BIGSERIAL PRIMARY KEY,
    receipt_id TEXT UNIQUE NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    coach_acronym CHAR(3) NOT NULL,
    agent_id TEXT NOT NULL,
    action TEXT NOT NULL,
    asset_id TEXT,
    person_id TEXT,
    input_hash TEXT,
    output_hash TEXT,
    input_summary TEXT,
    output_summary TEXT,
    decision TEXT,
    decision_rationale TEXT,
    parent_receipt_id TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_receipt_coach ON receipt_chain(coach_acronym);
CREATE INDEX IF NOT EXISTS idx_receipt_asset ON receipt_chain(asset_id);
CREATE INDEX IF NOT EXISTS idx_receipt_agent ON receipt_chain(agent_id);
CREATE INDEX IF NOT EXISTS idx_receipt_timestamp ON receipt_chain(timestamp DESC);

-- Asset Registry: All Universal Asset IDs
CREATE TABLE IF NOT EXISTS asset_registry (
    id BIGSERIAL PRIMARY KEY,
    asset_id TEXT UNIQUE NOT NULL,
    asset_type CHAR(4) NOT NULL,
    coach_acronym CHAR(3) NOT NULL,
    month SMALLINT NOT NULL,
    year SMALLINT NOT NULL,
    status TEXT DEFAULT 'active',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_asset_coach ON asset_registry(coach_acronym);
CREATE INDEX IF NOT EXISTS idx_asset_type ON asset_registry(asset_type);

-- Person Registry: All Person IDs
CREATE TABLE IF NOT EXISTS person_registry (
    id BIGSERIAL PRIMARY KEY,
    person_id TEXT UNIQUE NOT NULL,
    coach_acronym CHAR(3) NOT NULL,
    person_name TEXT NOT NULL,
    person_type TEXT NOT NULL DEFAULT 'client',  -- 'coach' or 'client'
    telegram_user_id TEXT,
    status TEXT DEFAULT 'active',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_person_coach ON person_registry(coach_acronym);

-- Enable Row Level Security
ALTER TABLE receipt_chain ENABLE ROW LEVEL SECURITY;
ALTER TABLE asset_registry ENABLE ROW LEVEL SECURITY;
ALTER TABLE person_registry ENABLE ROW LEVEL SECURITY;

-- ── FR1 V5.0 EXTENSIONS ──────────────────────────────────────────────────────
-- Spec: FR1 Tech Spec §Phase 0, Steps 0-A through 0-D
-- Architecture §3.1: V5 capabilities require non-negotiable migrations before
-- the first production session.

-- DEP-ENG-023: Cultural Memory Map
-- Spec Step 0-A: 'Morgan runs the CMM extraction pass... Operator reviews all
-- 7 CMM layer entries.' PK: cmm_id per Architecture §3.1.
CREATE TABLE IF NOT EXISTS cultural_memory_map (
    cmm_id TEXT PRIMARY KEY,
    coach_id CHAR(3) NOT NULL,
    status TEXT NOT NULL DEFAULT 'initialized',
    operator_confirmed BOOLEAN NOT NULL DEFAULT FALSE,
    confirmed_at TIMESTAMPTZ,
    entries JSONB NOT NULL DEFAULT '[]',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_cmm_coach ON cultural_memory_map(coach_id);

-- DEP-ENG-024: Coach Story Archive
-- Spec Step 0-B: 'Enforces the Hartian 5-element schema' PK: story_id per Architecture §3.1.
CREATE TABLE IF NOT EXISTS coach_story_archive (
    story_id TEXT PRIMARY KEY,
    coach_id CHAR(3) NOT NULL,
    story_type TEXT NOT NULL,
    hartian_schema JSONB NOT NULL,
    mechanism_tag TEXT NOT NULL DEFAULT '',
    arc_phase_fit TEXT NOT NULL DEFAULT '',
    cral_moment_fit TEXT NOT NULL DEFAULT '',
    emotional_register TEXT NOT NULL DEFAULT '',
    operator_approved BOOLEAN NOT NULL DEFAULT FALSE,
    approved_at TIMESTAMPTZ,
    rejection_reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_story_coach ON coach_story_archive(coach_id);
CREATE INDEX IF NOT EXISTS idx_story_type ON coach_story_archive(story_type);
CREATE INDEX IF NOT EXISTS idx_story_cral ON coach_story_archive(cral_moment_fit);
CREATE INDEX IF NOT EXISTS idx_story_approved ON coach_story_archive(operator_approved);

-- Humor Mechanism Registry
-- Spec Step 0-C: 'Create empty humor_mechanism_registry table entry for this coach.'
-- Architecture §3.1: PK: registry_id. Logs humor arcs for Boredom Ban compliance.
CREATE TABLE IF NOT EXISTS humor_mechanism_registry (
    registry_id TEXT PRIMARY KEY,
    coach_id CHAR(3) NOT NULL,
    status TEXT NOT NULL DEFAULT 'initialized',
    entries JSONB NOT NULL DEFAULT '[]',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_humor_coach ON humor_mechanism_registry(coach_id);

-- DEP-ENG-045: Context Performance Registry
-- Spec Step 0-D: 'Create empty context_performance_registry table entry.
-- Confidence score defaults to routing rules until ≥5 sessions are recorded.'
-- Architecture §3.1: PK: registry_id. Maps context selection rationale against
-- public performance metrics.
CREATE TABLE IF NOT EXISTS context_performance_registry (
    registry_id TEXT PRIMARY KEY,
    coach_id CHAR(3) NOT NULL,
    status TEXT NOT NULL DEFAULT 'initialized',
    confidence_model TEXT NOT NULL DEFAULT 'default_routing_rules',
    session_count INTEGER NOT NULL DEFAULT 0,
    context_selections JSONB NOT NULL DEFAULT '[]',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_cpr_coach ON context_performance_registry(coach_id);

-- Standing Trigger Intelligence Library
-- Spec §Phase 2: Library entries indexed by trigger_category_id (NOT archetype).
-- AC6: 'A research finding submitted with archetype_id as the primary index key is rejected.'
-- Entry gate: quality_score ≥0.65, human_evidence_count ≥3.
CREATE TABLE IF NOT EXISTS standing_trigger_library (
    entry_id TEXT PRIMARY KEY,
    coach_id CHAR(3) NOT NULL,
    trigger_category_id TEXT NOT NULL,  -- MUST be trigger category — never archetype
    trigger_category_name TEXT NOT NULL,
    quality_score NUMERIC(4,3) NOT NULL CHECK (quality_score >= 0.65),  -- Gate G-LIB
    human_evidence_count INTEGER NOT NULL CHECK (human_evidence_count >= 3),  -- DEP-ENG-021
    freshness_window_days INTEGER NOT NULL DEFAULT 90,
    entry_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    research_content JSONB NOT NULL DEFAULT '{}',
    cral_moment TEXT NOT NULL,
    session_number INTEGER NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_stl_coach ON standing_trigger_library(coach_id);
CREATE INDEX IF NOT EXISTS idx_stl_trigger ON standing_trigger_library(trigger_category_id);
CREATE INDEX IF NOT EXISTS idx_stl_quality ON standing_trigger_library(quality_score);

-- Enable RLS on V5 tables
ALTER TABLE cultural_memory_map ENABLE ROW LEVEL SECURITY;
ALTER TABLE coach_story_archive ENABLE ROW LEVEL SECURITY;
ALTER TABLE humor_mechanism_registry ENABLE ROW LEVEL SECURITY;
ALTER TABLE context_performance_registry ENABLE ROW LEVEL SECURITY;
ALTER TABLE standing_trigger_library ENABLE ROW LEVEL SECURITY;

-- Content Performance table (for humor_mechanism_tag JSONB — AC8)
-- Spec AC8: 'every generated script has a humor_mechanism_tag JSONB field
-- populated in content_performance'
CREATE TABLE IF NOT EXISTS content_performance (
    content_id TEXT PRIMARY KEY,
    coach_id CHAR(3) NOT NULL,
    session_id TEXT NOT NULL,
    script_id TEXT NOT NULL,
    humor_mechanism_tag JSONB NOT NULL DEFAULT '{"architectures_fired": [], "reason": "no_applicable_mechanism"}',
    ttt_drift_score NUMERIC(5,4),
    ai_detection_score NUMERIC(5,4),
    sophia_verdict TEXT,
    marcus_verdict TEXT,
    chen_verdict TEXT,
    performance_metrics JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_cp_coach ON content_performance(coach_id);
CREATE INDEX IF NOT EXISTS idx_cp_session ON content_performance(session_id);

ALTER TABLE content_performance ENABLE ROW LEVEL SECURITY;
"""

STORAGE_BUCKETS = [
    {"name": "sacred-audio", "public": False},
    {"name": "voice-notes", "public": True},  # Public for Notion audio embeds
    {"name": "coach-photos", "public": True},  # Public for Notion image embeds
    {"name": "visual-assets", "public": True},  # Public for Notion image embeds
]


def setup_storage(client: Client) -> None:
    """Create storage buckets if they don't exist."""
    for bucket in STORAGE_BUCKETS:
        try:
            client.storage.create_bucket(
                bucket["name"],
                options={"public": bucket["public"]},
            )
            print(f"  ✅ Created bucket: {bucket['name']} (public={bucket['public']})")
        except Exception as e:
            if "already exists" in str(e).lower():
                print(f"  ⏭️  Bucket already exists: {bucket['name']}")
            else:
                print(f"  ❌ Failed to create bucket {bucket['name']}: {e}")


def main():
    print("🔧 CCP Supabase Schema Setup")
    print("=" * 40)

    try:
        client = get_supabase_client()
        print("✅ Connected to Supabase")
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)

    print("\n📦 Creating storage buckets...")
    setup_storage(client)

    print("\n📋 SQL Schema (run in Supabase SQL Editor):")
    print("-" * 40)
    print(SCHEMA_SQL)
    print("-" * 40)
    print("\n💡 Copy the SQL above and run it in your Supabase SQL Editor.")
    print("   Dashboard → SQL Editor → New Query → Paste → Run")


if __name__ == "__main__":
    main()
