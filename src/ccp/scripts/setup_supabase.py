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
