-- Migration: FR-ERA3-35B Content Benchmark Profiles and Card Weighting Bundles Schema
-- Created: 2026-05-19

CREATE TABLE IF NOT EXISTS benchmark_profiles (
    profile_id           TEXT PRIMARY KEY,
    profile_version      TEXT NOT NULL DEFAULT '1.0',
    content_type         TEXT NOT NULL,
    profile_json         JSONB NOT NULL,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS archetype_score_bundles (
    bundle_id            TEXT PRIMARY KEY,
    archetype_choice     TEXT NOT NULL,
    content_type         TEXT NOT NULL,
    bundle_json          JSONB NOT NULL,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (archetype_choice, content_type)
);

CREATE TABLE IF NOT EXISTS card_weighting_bundles (
    bundle_id            TEXT PRIMARY KEY,
    content_type         TEXT NOT NULL,
    archetype_choice     TEXT NOT NULL,
    card_role            TEXT NOT NULL,
    resolved_json        JSONB NOT NULL,
    source_profile_id    TEXT NOT NULL REFERENCES benchmark_profiles(profile_id),
    source_bundle_id     TEXT NOT NULL REFERENCES archetype_score_bundles(bundle_id),
    created_at           TIMESTAMPTZ NOT NULL DEFAULT now()
);
