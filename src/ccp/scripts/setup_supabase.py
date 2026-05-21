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

-- FR-ERA3-01 Webinar Companion Tables
CREATE TABLE IF NOT EXISTS webinar_companion_sessions (
    session_id TEXT PRIMARY KEY,
    webinar_id TEXT NOT NULL,
    session_mode TEXT NOT NULL,
    video_url TEXT NOT NULL,
    protected_focal_region JSONB NOT NULL,
    participation_open BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS webinar_participation_captures (
    capture_id TEXT PRIMARY KEY,
    webinar_id TEXT NOT NULL,
    participant_person_id TEXT NOT NULL,
    prompt_id TEXT NOT NULL,
    slide_index_start INTEGER NOT NULL,
    slide_index_end INTEGER NOT NULL,
    reaction_type TEXT NOT NULL,
    submitted_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS webinar_rep_slide_scores (
    rep_session_id TEXT NOT NULL,
    slide_index INTEGER NOT NULL,
    hedge_density NUMERIC NOT NULL,
    pause_architecture_score NUMERIC NOT NULL,
    cta_pressure_stability NUMERIC NOT NULL,
    feedback_summary TEXT NOT NULL,
    delivered_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (rep_session_id, slide_index)
);

CREATE TABLE IF NOT EXISTS webinar_prompt_anchors (
    prompt_id TEXT PRIMARY KEY,
    webinar_id TEXT NOT NULL,
    trigger_at_seconds NUMERIC NOT NULL,
    prompt_type TEXT NOT NULL,
    preferred_geometry TEXT NOT NULL
);

ALTER TABLE webinar_companion_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE webinar_participation_captures ENABLE ROW LEVEL SECURITY;
ALTER TABLE webinar_rep_slide_scores ENABLE ROW LEVEL SECURITY;
ALTER TABLE webinar_prompt_anchors ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-10 Onboarding Flow Tables
CREATE TABLE IF NOT EXISTS anonymous_onboarding_sessions (
    session_id TEXT PRIMARY KEY,
    coach_id TEXT NOT NULL,
    state TEXT NOT NULL,
    referral_token_id TEXT,
    anonymous_device_nonce TEXT NOT NULL,
    benchmark_revealed_at TIMESTAMPTZ,
    linked_person_id TEXT,
    created_at_utc TIMESTAMPTZ NOT NULL,
    updated_at_utc TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS anonymous_onboarding_audio_assets (
    audit_asset_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES anonymous_onboarding_sessions(session_id),
    storage_path TEXT NOT NULL,
    duration_seconds INTEGER NOT NULL,
    mime_type TEXT NOT NULL,
    upload_status TEXT NOT NULL,
    uploaded_at_utc TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS anonymous_onboarding_teasers (
    teaser_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES anonymous_onboarding_sessions(session_id),
    benchmark_score INTEGER NOT NULL,
    score_label TEXT NOT NULL,
    one_line_insight TEXT NOT NULL,
    next_move_hint TEXT NOT NULL,
    confidence_note TEXT NOT NULL,
    revealed_at_utc TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS onboarding_offer_impressions (
    impression_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES anonymous_onboarding_sessions(session_id),
    offer_tier_ceiling TEXT NOT NULL,
    target_campaign_tier INTEGER NOT NULL,
    gate_verdict TEXT NOT NULL,
    decision TEXT,
    created_at_utc TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS anonymous_registration_links (
    link_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES anonymous_onboarding_sessions(session_id),
    registration_mode TEXT NOT NULL,
    person_id TEXT,
    lead_id TEXT,
    linked_at_utc TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS onboarding_referral_tokens (
    referral_token_id TEXT PRIMARY KEY,
    coach_id TEXT NOT NULL,
    source_artifact_id TEXT,
    channel TEXT NOT NULL,
    created_at_utc TIMESTAMPTZ NOT NULL
);

ALTER TABLE anonymous_onboarding_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE anonymous_onboarding_audio_assets ENABLE ROW LEVEL SECURITY;
ALTER TABLE anonymous_onboarding_teasers ENABLE ROW LEVEL SECURITY;
ALTER TABLE onboarding_offer_impressions ENABLE ROW LEVEL SECURITY;
ALTER TABLE anonymous_registration_links ENABLE ROW LEVEL SECURITY;
ALTER TABLE onboarding_referral_tokens ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-11 Challenge Arena Tables
CREATE TABLE IF NOT EXISTS challenge_arena_participants (
    participant_id TEXT PRIMARY KEY,
    capacity_track TEXT NOT NULL,
    current_layer TEXT NOT NULL,
    session_index INTEGER NOT NULL,
    layer_attempt_count INTEGER NOT NULL,
    active_days_this_week INTEGER NOT NULL,
    streak_count INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS challenge_arena_sessions (
    session_id TEXT PRIMARY KEY,
    participant_id TEXT NOT NULL REFERENCES challenge_arena_participants(participant_id),
    command_key TEXT NOT NULL,
    variation_key TEXT NOT NULL,
    readiness_verdict TEXT,
    completion_status TEXT NOT NULL,
    completed_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS challenge_arena_variation_history (
    history_id TEXT PRIMARY KEY,
    participant_id TEXT NOT NULL REFERENCES challenge_arena_participants(participant_id),
    layer TEXT NOT NULL,
    ui_route_fingerprint TEXT NOT NULL,
    assigned_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS challenge_arena_weekly_rollups (
    rollup_id TEXT PRIMARY KEY,
    participant_id TEXT NOT NULL REFERENCES challenge_arena_participants(participant_id),
    week_start_utc TIMESTAMPTZ NOT NULL,
    week_end_utc TIMESTAMPTZ NOT NULL,
    sessions_completed INTEGER NOT NULL,
    cumulative_words_spoken INTEGER NOT NULL,
    cumulative_micro_pauses INTEGER NOT NULL,
    delta_words_spoken INTEGER NOT NULL,
    delta_hedge_frequency NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS challenge_arena_sunday_postcards (
    postcard_id TEXT PRIMARY KEY,
    participant_id TEXT NOT NULL REFERENCES challenge_arena_participants(participant_id),
    rollup_id TEXT NOT NULL REFERENCES challenge_arena_weekly_rollups(rollup_id),
    qualitative_interpretation TEXT NOT NULL,
    forward_forecast TEXT NOT NULL,
    status TEXT NOT NULL,
    published_at TIMESTAMPTZ NOT NULL,
    acknowledged_at TIMESTAMPTZ
);

ALTER TABLE challenge_arena_participants ENABLE ROW LEVEL SECURITY;
ALTER TABLE challenge_arena_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE challenge_arena_variation_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE challenge_arena_weekly_rollups ENABLE ROW LEVEL SECURITY;
ALTER TABLE challenge_arena_sunday_postcards ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-13 Experience Ladder Tables
CREATE TABLE IF NOT EXISTS experience_state_packets (
    packet_id TEXT PRIMARY KEY,
    client_id TEXT NOT NULL,
    coach_id TEXT NOT NULL,
    active_surface TEXT NOT NULL,
    stage TEXT NOT NULL,
    momentum_level TEXT NOT NULL,
    recovery_state TEXT NOT NULL,
    packet_json JSONB NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    UNIQUE(client_id, coach_id)
);
CREATE INDEX IF NOT EXISTS idx_experience_state_packets_coach_id ON experience_state_packets(coach_id);
CREATE INDEX IF NOT EXISTS idx_experience_state_packets_active_surface ON experience_state_packets(active_surface);

CREATE TABLE IF NOT EXISTS experience_route_events (
    route_id TEXT PRIMARY KEY,
    client_id TEXT NOT NULL,
    coach_id TEXT NOT NULL,
    from_surface TEXT NOT NULL,
    to_surface TEXT NOT NULL,
    reason TEXT NOT NULL,
    next_step_type TEXT NOT NULL,
    route_latency_ms INTEGER NOT NULL CHECK (route_latency_ms <= 3000),
    created_at TIMESTAMPTZ NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_experience_route_events_client_id ON experience_route_events(client_id);
CREATE INDEX IF NOT EXISTS idx_experience_route_events_to_surface ON experience_route_events(to_surface);

CREATE TABLE IF NOT EXISTS surface_readiness_snapshots (
    snapshot_id TEXT PRIMARY KEY,
    client_id TEXT NOT NULL,
    surface TEXT NOT NULL,
    readiness_score NUMERIC NOT NULL,
    journey_id TEXT,
    active_task_id TEXT,
    calculated_at TIMESTAMPTZ NOT NULL,
    UNIQUE(client_id, surface)
);
CREATE INDEX IF NOT EXISTS idx_surface_readiness_snapshots_surface ON surface_readiness_snapshots(surface);
CREATE INDEX IF NOT EXISTS idx_surface_readiness_snapshots_readiness_score ON surface_readiness_snapshots(readiness_score);

CREATE TABLE IF NOT EXISTS inline_reward_packets (
    reward_id TEXT PRIMARY KEY,
    client_id TEXT NOT NULL,
    surface TEXT NOT NULL,
    next_step_type TEXT NOT NULL,
    headline TEXT NOT NULL,
    body TEXT NOT NULL,
    task_ticket_id TEXT,
    created_at TIMESTAMPTZ NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_inline_reward_packets_client_id ON inline_reward_packets(client_id);
CREATE INDEX IF NOT EXISTS idx_inline_reward_packets_surface ON inline_reward_packets(surface);

CREATE TABLE IF NOT EXISTS async_content_exhaust_jobs (
    job_id TEXT PRIMARY KEY,
    client_id TEXT NOT NULL,
    surface TEXT NOT NULL,
    source_route_id TEXT NOT NULL,
    job_type TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_async_content_exhaust_jobs_source_route_id ON async_content_exhaust_jobs(source_route_id);
CREATE INDEX IF NOT EXISTS idx_async_content_exhaust_jobs_status ON async_content_exhaust_jobs(status);

ALTER TABLE experience_state_packets ENABLE ROW LEVEL SECURITY;
ALTER TABLE experience_route_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE surface_readiness_snapshots ENABLE ROW LEVEL SECURITY;
ALTER TABLE inline_reward_packets ENABLE ROW LEVEL SECURITY;
ALTER TABLE async_content_exhaust_jobs ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-19 Testimonial Builder Tables
CREATE TABLE IF NOT EXISTS testimonial_capture_sessions (
    capture_session_id TEXT PRIMARY KEY,
    person_id TEXT NOT NULL,
    coach_id TEXT NOT NULL,
    trigger_json JSONB NOT NULL,
    preferred_media_mode TEXT NOT NULL,
    status TEXT NOT NULL,
    current_step TEXT NOT NULL,
    reflection_text_transcript TEXT,
    primary_media_asset_id TEXT,
    attachment_asset_ids JSONB,
    tags JSONB,
    consent_level TEXT,
    created_at_utc TIMESTAMPTZ NOT NULL,
    updated_at_utc TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS testimonial_media_assets (
    asset_id TEXT PRIMARY KEY,
    asset_type TEXT NOT NULL,
    storage_path TEXT NOT NULL,
    duration_seconds INTEGER,
    mime_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS testimonial_proof_objects (
    proof_object_id TEXT PRIMARY KEY,
    capture_session_id TEXT NOT NULL REFERENCES testimonial_capture_sessions(capture_session_id),
    person_id TEXT NOT NULL,
    coach_id TEXT NOT NULL,
    title TEXT NOT NULL,
    narrative_summary TEXT NOT NULL,
    primary_media_asset_id TEXT NOT NULL,
    attachment_asset_ids JSONB,
    consent_level TEXT NOT NULL,
    trigger_kind TEXT NOT NULL,
    delta_headline TEXT,
    share_ready BOOLEAN NOT NULL DEFAULT FALSE,
    created_at_utc TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS user_card_snapshots (
    snapshot_id TEXT PRIMARY KEY,
    person_id TEXT NOT NULL,
    weekly_period_key TEXT NOT NULL,
    solo_tier TEXT NOT NULL,
    strongest_primitive_id TEXT,
    streak_count INTEGER NOT NULL,
    metrics JSONB NOT NULL,
    created_at_utc TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS peer_endorsement_verdicts (
    verdict_id TEXT PRIMARY KEY,
    person_id TEXT NOT NULL,
    verdict TEXT NOT NULL,
    evidence JSONB,
    rationale TEXT NOT NULL,
    locked_message TEXT,
    decided_at_utc TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS peer_endorsement_policies (
    policy_id TEXT PRIMARY KEY,
    program_id TEXT NOT NULL,
    threshold_required INTEGER NOT NULL,
    accepted_pathways JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS community_peer_certifications (
    certification_id TEXT PRIMARY KEY,
    person_id TEXT NOT NULL,
    certified_as TEXT NOT NULL,
    certified_at_utc TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS testimonial_share_events (
    share_event_id TEXT PRIMARY KEY,
    artifact_kind TEXT NOT NULL,
    artifact_id TEXT NOT NULL,
    published_destinations JSONB NOT NULL,
    silent_referral_routed BOOLEAN NOT NULL DEFAULT FALSE,
    receipt_id TEXT NOT NULL
);

ALTER TABLE testimonial_capture_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE testimonial_media_assets ENABLE ROW LEVEL SECURITY;
ALTER TABLE testimonial_proof_objects ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_card_snapshots ENABLE ROW LEVEL SECURITY;
ALTER TABLE peer_endorsement_verdicts ENABLE ROW LEVEL SECURITY;
ALTER TABLE peer_endorsement_policies ENABLE ROW LEVEL SECURITY;
ALTER TABLE community_peer_certifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE testimonial_share_events ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-ScoreCard Viewer Tables
CREATE TABLE IF NOT EXISTS score_viewer_sessions (
    session_id TEXT PRIMARY KEY,
    coach_id TEXT NOT NULL,
    scorecard_version TEXT NOT NULL,
    opened_at_utc TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS score_viewer_reflection_acks (
    ack_id TEXT PRIMARY KEY,
    coach_id TEXT NOT NULL,
    session_id TEXT NOT NULL REFERENCES score_viewer_sessions(session_id),
    insight_key TEXT NOT NULL,
    acknowledged_next_step TEXT NOT NULL,
    receipt_id TEXT NOT NULL,
    created_at_utc TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS score_viewer_projection_cache (
    cache_id TEXT PRIMARY KEY,
    coach_id TEXT NOT NULL,
    scorecard_version TEXT NOT NULL,
    projection_json JSONB NOT NULL,
    cached_at_utc TIMESTAMPTZ NOT NULL,
    UNIQUE(coach_id, scorecard_version)
);

ALTER TABLE score_viewer_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE score_viewer_reflection_acks ENABLE ROW LEVEL SECURITY;
ALTER TABLE score_viewer_projection_cache ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-14 Stealth Course Commercial Ladder Tables
CREATE TABLE IF NOT EXISTS commercial_ladder_events (
    event_id TEXT PRIMARY KEY,
    client_id TEXT NOT NULL,
    coach_id TEXT NOT NULL,
    journey_id TEXT NOT NULL,
    locked_node_id TEXT NOT NULL,
    governor_evaluation_id TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL
);

ALTER TABLE commercial_ladder_events ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-21 SDA Query and Crosswalk Service Tables
CREATE TABLE IF NOT EXISTS sda_query_audit (
    audit_id              TEXT PRIMARY KEY,
    action_type           TEXT NOT NULL,
    queryable_surface     TEXT NOT NULL,
    request_payload       JSONB NOT NULL,
    response_summary      JSONB NOT NULL,
    provenance_bundle     JSONB NOT NULL,
    used_stale_fallback   BOOLEAN NOT NULL DEFAULT FALSE,
    fallback_reason       TEXT,
    latency_ms            REAL NOT NULL,
    created_at            TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE sda_query_audit ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-02 In-Chat Telegram Payments Tables
CREATE TABLE IF NOT EXISTS payment_transactions (
    transaction_id TEXT PRIMARY KEY,
    telegram_user_id BIGINT NOT NULL,
    coach_id TEXT NOT NULL,
    tier TEXT NOT NULL,
    amount_cents INTEGER NOT NULL,
    status TEXT NOT NULL,
    stripe_charge_id TEXT DEFAULT '',
    eligibility_id TEXT NOT NULL,
    reward_dispatched BOOLEAN NOT NULL DEFAULT FALSE,
    provisioning_complete BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS tier_subscriptions (
    subscription_id TEXT PRIMARY KEY,
    telegram_user_id BIGINT NOT NULL,
    coach_id TEXT NOT NULL,
    tier TEXT NOT NULL,
    stripe_subscription_id TEXT DEFAULT '',
    status TEXT NOT NULL DEFAULT 'active',
    started_at TIMESTAMPTZ NOT NULL
);

ALTER TABLE payment_transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE tier_subscriptions ENABLE ROW LEVEL SECURITY;

-- FR-COM-01 AFFiNE Billing & Credit System Tables
CREATE TABLE IF NOT EXISTS coach_subscriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coach_id UUID NOT NULL UNIQUE,
    stripe_customer_id VARCHAR(50) NOT NULL UNIQUE,
    stripe_subscription_id VARCHAR(50) NOT NULL UNIQUE,
    stripe_metered_item_id VARCHAR(50),
    tier VARCHAR(30) NOT NULL DEFAULT 'proof_layer' CHECK (tier IN ('proof_layer', 'speaking_learning', 'coach_os', 'elite')),
    monthly_base_price_cents INTEGER NOT NULL DEFAULT 0,
    alacarte_video_price_cents INTEGER NOT NULL DEFAULT 999,
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'past_due', 'cancelled', 'paused')),
    payment_method_last4 VARCHAR(4),
    current_period_start TIMESTAMPTZ,
    current_period_end TIMESTAMPTZ,
    total_monthly_cost_cents INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sub_coach ON coach_subscriptions(coach_id);
CREATE INDEX IF NOT EXISTS idx_sub_status ON coach_subscriptions(status);
ALTER TABLE coach_subscriptions ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS billing_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coach_id UUID NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    stripe_event_id VARCHAR(100) UNIQUE,
    amount_cents INTEGER,
    description TEXT,
    receipt_chain_block VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_billing_coach ON billing_events(coach_id);
CREATE INDEX IF NOT EXISTS idx_billing_type ON billing_events(event_type);
ALTER TABLE billing_events ENABLE ROW LEVEL SECURITY;

-- FR-APR-08 Orchestration Dichotomy Tables
CREATE TABLE IF NOT EXISTS coalition_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coach_id UUID NOT NULL,
    coalition_signature JSONB NOT NULL,
    edge_product JSONB NOT NULL,
    primitive_candidates JSONB NOT NULL,
    validation_status VARCHAR(20) NOT NULL CHECK (validation_status IN ('validated', 'fallback_used', 'centroid_rejected')),
    anti_centroid_score FLOAT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_coalition_coach ON coalition_history(coach_id);
CREATE INDEX IF NOT EXISTS idx_coalition_status ON coalition_history(validation_status);
ALTER TABLE coalition_history ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS coalition_fatalities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coalition_id UUID NOT NULL,
    edge_product_id VARCHAR(100) NOT NULL,
    expected_engagement FLOAT,
    actual_engagement FLOAT,
    delta_percentage FLOAT,
    diagnosis TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE coalition_fatalities ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-18 CBCS Four-Engine Runtime Tables
CREATE TABLE IF NOT EXISTS semantic_evolution_record (
    record_id TEXT PRIMARY KEY,
    client_id TEXT NOT NULL,
    coach_id TEXT NOT NULL,
    recursive_patterns JSONB NOT NULL DEFAULT '[]',
    feedback_loops JSONB NOT NULL DEFAULT '[]',
    last_updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_ser_client ON semantic_evolution_record(client_id);
CREATE INDEX IF NOT EXISTS idx_ser_coach ON semantic_evolution_record(coach_id);
ALTER TABLE semantic_evolution_record ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-25 AR Overlay Capture Pipeline Tables
CREATE TABLE IF NOT EXISTS overlay_interaction_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    timestamp_ms BIGINT NOT NULL,
    round_index INTEGER,
    from_state TEXT,
    to_state TEXT,
    overlay_elements JSONB DEFAULT '{}',
    capture_state JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_overlay_events_session ON overlay_interaction_events(session_id);
CREATE INDEX IF NOT EXISTS idx_overlay_events_type ON overlay_interaction_events(event_type);
ALTER TABLE overlay_interaction_events ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS overlay_capture_metadata (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id TEXT NOT NULL,
    coach_id TEXT NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    frame_rate INTEGER NOT NULL,
    media_format TEXT NOT NULL,
    device_tier TEXT NOT NULL,
    resolution_downgraded BOOLEAN DEFAULT FALSE,
    capture_status TEXT NOT NULL,
    started_at TIMESTAMPTZ,
    stopped_at TIMESTAMPTZ,
    duration_ms INTEGER DEFAULT 0,
    blob_size_bytes BIGINT DEFAULT 0,
    upload_status TEXT DEFAULT 'pending_background',
    interaction_event_count INTEGER DEFAULT 0,
    audio_track_present BOOLEAN DEFAULT TRUE,
    video_track_present BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_overlay_capture_session ON overlay_capture_metadata(session_id);
CREATE INDEX IF NOT EXISTS idx_overlay_capture_coach ON overlay_capture_metadata(coach_id);
ALTER TABLE overlay_capture_metadata ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-16 Archetype Container Runtime Tables
CREATE TABLE IF NOT EXISTS archetype_runtime_sessions (
    runtime_session_id          TEXT PRIMARY KEY,
    coach_id                    TEXT NOT NULL,
    capture_id                  TEXT NOT NULL,
    coalition_id                TEXT NOT NULL,
    runtime_status              TEXT NOT NULL,
    selected_archetype          TEXT,
    trigger_guard_session_id    TEXT,
    receipt_chain_hash          TEXT NOT NULL,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_acr_sessions_coach ON archetype_runtime_sessions(coach_id);
ALTER TABLE archetype_runtime_sessions ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS archetype_runtime_sentence_audits (
    sentence_audit_id           TEXT PRIMARY KEY,
    runtime_session_id          TEXT NOT NULL,
    sentence_id                 TEXT NOT NULL,
    sentence_index              INTEGER NOT NULL,
    sentence_text               TEXT NOT NULL,
    start_offset                INTEGER NOT NULL,
    end_offset                  INTEGER NOT NULL,
    similarity_score            DOUBLE PRECISION NOT NULL,
    similarity_band             TEXT NOT NULL,
    collapse_reason             TEXT NOT NULL,
    failed                      BOOLEAN NOT NULL DEFAULT FALSE,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_acr_audits_session ON archetype_runtime_sentence_audits(runtime_session_id);
ALTER TABLE archetype_runtime_sentence_audits ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS archetype_container_manifests (
    container_id                TEXT PRIMARY KEY,
    runtime_session_id          TEXT NOT NULL,
    coach_id                    TEXT NOT NULL,
    selected_archetype          TEXT NOT NULL,
    manifest_json               JSONB NOT NULL,
    sfl_function_stack_json     JSONB,
    composition_depth_json      JSONB,
    variation_binding_json      JSONB,
    sfl_binding_status          TEXT NOT NULL DEFAULT 'sfl_not_bound',
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_acr_manifests_session ON archetype_container_manifests(runtime_session_id);
ALTER TABLE archetype_container_manifests ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS archetype_sfl_execution_contracts (
    contract_id              TEXT PRIMARY KEY,
    runtime_session_id       TEXT NOT NULL,
    archetype_choice         TEXT NOT NULL,
    contract_json            JSONB NOT NULL,
    sfl_binding_status       TEXT NOT NULL,
    created_at               TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE archetype_sfl_execution_contracts ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS archetype_runtime_rejections (
    rejection_id                TEXT PRIMARY KEY,
    runtime_session_id          TEXT NOT NULL,
    rejection_code              TEXT NOT NULL,
    similarity_score            DOUBLE PRECISION NOT NULL,
    coaching_fix                TEXT NOT NULL,
    rerecord_prompt             TEXT NOT NULL,
    reroute_token               TEXT,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_acr_rejections_session ON archetype_runtime_rejections(runtime_session_id);
ALTER TABLE archetype_runtime_rejections ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-07 AFFiNE Studio Block Orchestration Tables
CREATE TABLE IF NOT EXISTS affine_client_card_projections (
    projection_id               TEXT PRIMARY KEY,
    coach_id                    TEXT NOT NULL,
    client_id                   TEXT NOT NULL,
    workspace_id                TEXT NOT NULL,
    projection_json             JSONB NOT NULL,
    updated_at                  TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(coach_id, client_id)
);

CREATE INDEX IF NOT EXISTS idx_affine_ccproj_coach ON affine_client_card_projections(coach_id);
ALTER TABLE affine_client_card_projections ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS affine_red_flag_evidence (
    flag_id                     TEXT PRIMARY KEY,
    coach_id                    TEXT NOT NULL,
    client_id                   TEXT NOT NULL,
    severity                    TEXT NOT NULL,
    excerpt_hash                TEXT NOT NULL,
    excerpt_text                TEXT NOT NULL,
    source_type                 TEXT NOT NULL,
    session_id                  TEXT NOT NULL,
    asset_id                    TEXT NOT NULL,
    workspace_entry_id          TEXT NOT NULL,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_affine_rfevid_coach ON affine_red_flag_evidence(coach_id);
CREATE INDEX IF NOT EXISTS idx_affine_rfevid_client ON affine_red_flag_evidence(client_id);
CREATE INDEX IF NOT EXISTS idx_affine_rfevid_hash ON affine_red_flag_evidence(excerpt_hash);
ALTER TABLE affine_red_flag_evidence ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS affine_intercept_review_acks (
    acknowledgement_id          TEXT PRIMARY KEY,
    flag_id                     TEXT NOT NULL,
    coach_id                    TEXT NOT NULL,
    client_id                   TEXT NOT NULL,
    excerpt_hash                TEXT NOT NULL,
    ack_phrase                  TEXT NOT NULL,
    acknowledged_at             TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(flag_id, coach_id, excerpt_hash)
);

CREATE INDEX IF NOT EXISTS idx_affine_acks_acked_at ON affine_intercept_review_acks(acknowledged_at);
ALTER TABLE affine_intercept_review_acks ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS affine_intercept_sessions (
    intercept_id                TEXT PRIMARY KEY,
    flag_id                     TEXT NOT NULL,
    coach_id                    TEXT NOT NULL,
    client_id                   TEXT NOT NULL,
    workspace_id                TEXT NOT NULL,
    recorder_session_id         TEXT DEFAULT '',
    gate_status                 TEXT NOT NULL CHECK (gate_status IN ('locked', 'ready', 'recording', 'completed', 'blocked')),
    started_at                  TIMESTAMPTZ,
    completed_at                TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_affine_intercepts_coach ON affine_intercept_sessions(coach_id);
ALTER TABLE affine_intercept_sessions ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS affine_broadcast_queue (
    broadcast_session_id        TEXT PRIMARY KEY,
    coach_id                    TEXT NOT NULL,
    workspace_id                TEXT NOT NULL,
    program_id                  TEXT NOT NULL,
    studio_session_id           TEXT DEFAULT '',
    title                       TEXT NOT NULL,
    status                      TEXT NOT NULL,
    audience_surface            TEXT NOT NULL DEFAULT 'telegram',
    planned_start_at            TIMESTAMPTZ,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_affine_bcast_coach ON affine_broadcast_queue(coach_id);
CREATE INDEX IF NOT EXISTS idx_affine_bcast_status ON affine_broadcast_queue(status);
ALTER TABLE affine_broadcast_queue ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-09 Conscious Editor Mini App Tables
CREATE TABLE IF NOT EXISTS conscious_editor_sessions (
    editor_session_id           TEXT PRIMARY KEY,
    coach_id                    TEXT NOT NULL,
    source_audio_asset_id       TEXT NOT NULL,
    content_output_id           TEXT,
    vcb_id                      TEXT,
    composition_id              TEXT,
    status                      TEXT NOT NULL,
    tier                        TEXT NOT NULL,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_ced_sessions_coach ON conscious_editor_sessions(coach_id);
CREATE INDEX IF NOT EXISTS idx_ced_sessions_source ON conscious_editor_sessions(source_audio_asset_id);
ALTER TABLE conscious_editor_sessions ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS conscious_editor_transcript_revisions (
    revision_id                 TEXT PRIMARY KEY,
    editor_session_id           TEXT NOT NULL,
    source_kind                 TEXT NOT NULL,
    author_person_id            TEXT NOT NULL,
    revision_note               TEXT DEFAULT '',
    revised_plaintext           TEXT NOT NULL,
    revised_json_payload        TEXT NOT NULL,
    token_patches_json          JSONB DEFAULT '[]',
    requires_timing_reflow      BOOLEAN DEFAULT FALSE,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_ced_revisions_session ON conscious_editor_transcript_revisions(editor_session_id);
ALTER TABLE conscious_editor_transcript_revisions ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS conscious_editor_rerender_jobs (
    job_id                      TEXT PRIMARY KEY,
    editor_session_id           TEXT NOT NULL,
    revision_id                 TEXT NOT NULL,
    scope                       TEXT NOT NULL,
    rationale                   TEXT NOT NULL,
    affected_slide_indices      JSONB DEFAULT '[]',
    requires_vcb_refresh        BOOLEAN DEFAULT FALSE,
    requires_audio_rerecord     BOOLEAN DEFAULT FALSE,
    requires_nim_rerun          BOOLEAN DEFAULT FALSE,
    status                      TEXT NOT NULL DEFAULT 'queued',
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at                TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_ced_rerender_session ON conscious_editor_rerender_jobs(editor_session_id);
CREATE INDEX IF NOT EXISTS idx_ced_rerender_composition ON conscious_editor_rerender_jobs(editor_session_id);
ALTER TABLE conscious_editor_rerender_jobs ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS conscious_editor_lineage_links (
    node_id                     TEXT PRIMARY KEY,
    editor_session_id           TEXT NOT NULL,
    node_type                   TEXT NOT NULL,
    referenced_id               TEXT NOT NULL,
    label                       TEXT NOT NULL,
    parent_node_id              TEXT,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_ced_lineage_session ON conscious_editor_lineage_links(editor_session_id);
ALTER TABLE conscious_editor_lineage_links ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS conscious_editor_operator_decisions (
    decision_id                 TEXT PRIMARY KEY,
    editor_session_id           TEXT NOT NULL,
    coach_id                    TEXT NOT NULL,
    decision                    TEXT NOT NULL,
    decision_note               TEXT DEFAULT '',
    resulting_status            TEXT NOT NULL,
    receipt_event_id            TEXT NOT NULL,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_ced_decisions_session ON conscious_editor_operator_decisions(editor_session_id);
ALTER TABLE conscious_editor_operator_decisions ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-12 CMF Arc-Governed Rendering Tables
CREATE TABLE IF NOT EXISTS cmf_arc_render_jobs (
    job_id                      TEXT PRIMARY KEY,
    content_output_id           TEXT NOT NULL,
    coach_id                    TEXT NOT NULL,
    selected_format             TEXT NOT NULL,
    status                      TEXT NOT NULL,
    manifest_id                 TEXT DEFAULT '',
    composition_id              TEXT DEFAULT '',
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at                  TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(content_output_id, selected_format)
);
CREATE INDEX IF NOT EXISTS idx_cmf_arj_coach ON cmf_arc_render_jobs(coach_id);
CREATE INDEX IF NOT EXISTS idx_cmf_arj_status ON cmf_arc_render_jobs(status);
ALTER TABLE cmf_arc_render_jobs ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS cmf_beat_cluster_plans (
    cluster_id                  TEXT PRIMARY KEY,
    job_id                      TEXT NOT NULL,
    cluster_type                TEXT NOT NULL,
    order_index                 INTEGER NOT NULL,
    start_ms                    INTEGER NOT NULL,
    end_ms                      INTEGER NOT NULL CHECK (end_ms > start_ms),
    shot_grammar                TEXT NOT NULL,
    cluster_json                JSONB NOT NULL,
    UNIQUE(job_id, order_index)
);
CREATE INDEX IF NOT EXISTS idx_cmf_bcp_job ON cmf_beat_cluster_plans(job_id);
ALTER TABLE cmf_beat_cluster_plans ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS cmf_first_frame_checks (
    check_id                    TEXT PRIMARY KEY,
    job_id                      TEXT NOT NULL,
    cluster_id                  TEXT NOT NULL,
    verdict                     TEXT NOT NULL,
    authority_score             DOUBLE PRECISION NOT NULL,
    contrast_score              DOUBLE PRECISION NOT NULL,
    recognizability_score       DOUBLE PRECISION NOT NULL,
    anti_generic_flags          JSONB DEFAULT '[]',
    checked_at                  TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(job_id, cluster_id)
);
CREATE INDEX IF NOT EXISTS idx_cmf_ffc_verdict ON cmf_first_frame_checks(verdict);
ALTER TABLE cmf_first_frame_checks ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS cmf_epic_meaning_gate_results (
    gate_id                     TEXT PRIMARY KEY,
    job_id                      TEXT NOT NULL UNIQUE,
    verdict                     TEXT NOT NULL,
    blandness_confidence        DOUBLE PRECISION DEFAULT 0.0,
    failed_rules                JSONB DEFAULT '[]',
    rationale                   TEXT NOT NULL,
    checked_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_cmf_emg_verdict ON cmf_epic_meaning_gate_results(verdict);
ALTER TABLE cmf_epic_meaning_gate_results ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS cmf_render_manifests (
    manifest_id                 TEXT PRIMARY KEY,
    job_id                      TEXT NOT NULL UNIQUE,
    vcb_id                      TEXT NOT NULL,
    render_target_path          TEXT NOT NULL,
    manifest_json               JSONB NOT NULL,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_cmf_rm_vcb ON cmf_render_manifests(vcb_id);
ALTER TABLE cmf_render_manifests ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS cmf_render_perceptual_plans (
    plan_id                      TEXT PRIMARY KEY,
    content_output_id            TEXT NOT NULL,
    coach_id                     TEXT NOT NULL,
    surface_type                 TEXT NOT NULL,
    function_stack_packet_id     TEXT NOT NULL,
    directional_integrity_report_id TEXT NOT NULL,
    perceptual_influence_report_id TEXT NOT NULL,
    depth_profile_json           JSONB NOT NULL,
    variation_hints_json         JSONB NOT NULL,
    temporal_hints_json          JSONB NOT NULL,
    target_thumbnail_count       INTEGER NOT NULL,
    card_safe                    BOOLEAN NOT NULL DEFAULT FALSE,
    pdf_safe                     BOOLEAN NOT NULL DEFAULT FALSE,
    generated_at                 TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_cmf_rpp_coach ON cmf_render_perceptual_plans(coach_id);
ALTER TABLE cmf_render_perceptual_plans ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS cmf_render_preservation_reports (
    report_id                    TEXT PRIMARY KEY,
    plan_id                      TEXT NOT NULL,
    manifest_id                  TEXT DEFAULT '',
    fallback_decision            TEXT NOT NULL,
    dimensions_json              JSONB NOT NULL,
    lost_intents                 JSONB NOT NULL DEFAULT '[]',
    downgraded_surfaces          JSONB NOT NULL DEFAULT '[]',
    reviewer_notes               JSONB NOT NULL DEFAULT '[]',
    created_at                   TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_cmf_rpr_plan ON cmf_render_preservation_reports(plan_id);
ALTER TABLE cmf_render_preservation_reports ENABLE ROW LEVEL SECURITY;


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
"""

import os
import sys

from supabase import create_client, Client
from src.ccp.models.primitive_registry_models import PRIMITIVE_QUERY_AUDIT_SQL


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

-- FR-ERA3-05b Debate With Jury Tables
CREATE TABLE IF NOT EXISTS reaction_debates (
    debate_id TEXT PRIMARY KEY,
    source_artifact_id TEXT NOT NULL,
    counter_artifact_id TEXT,
    lane_key TEXT NOT NULL,
    render_format TEXT DEFAULT 'split_screen_vs',
    tally_for INTEGER DEFAULT 0,
    tally_against INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_debates_source ON reaction_debates(source_artifact_id);

CREATE TABLE IF NOT EXISTS reaction_vote_prompts (
    prompt_id TEXT PRIMARY KEY,
    source_vote_id TEXT NOT NULL,
    selected_stance TEXT NOT NULL,
    deep_link_url TEXT NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_vote_prompts_source ON reaction_vote_prompts(source_vote_id);

ALTER TABLE reaction_debates ENABLE ROW LEVEL SECURITY;
ALTER TABLE reaction_vote_prompts ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-05c Reaction Duel Tables
CREATE TABLE IF NOT EXISTS reaction_duels (
    duel_id TEXT PRIMARY KEY,
    topic_id TEXT NOT NULL,
    inviter_coach_id TEXT NOT NULL,
    invitee_coach_id TEXT NOT NULL,
    lifecycle_state TEXT NOT NULL,
    unified_artifact_id TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS reaction_duel_brackets (
    coach_id TEXT NOT NULL,
    topic_id TEXT NOT NULL,
    bracket_tier TEXT NOT NULL,
    local_bracket_key TEXT NOT NULL,
    calculated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (coach_id, topic_id)
);

CREATE TABLE IF NOT EXISTS reaction_duel_invites (
    duel_id TEXT PRIMARY KEY,
    inviter_coach_id TEXT NOT NULL,
    invitee_coach_id TEXT NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL
);

ALTER TABLE reaction_duels ENABLE ROW LEVEL SECURITY;
ALTER TABLE reaction_duel_brackets ENABLE ROW LEVEL SECURITY;
ALTER TABLE reaction_duel_invites ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-05d Reaction Tierlist Tables
CREATE TABLE IF NOT EXISTS reaction_tierlist_sessions (
    session_id TEXT PRIMARY KEY,
    topic_id TEXT NOT NULL,
    speech_degraded BOOLEAN DEFAULT FALSE,
    snap_animation_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS reaction_tierlist_moves (
    event_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    item_id TEXT NOT NULL,
    spoken_phrase TEXT NOT NULL,
    target_tier TEXT NOT NULL,
    target_rank_index INTEGER NOT NULL,
    confidence NUMERIC NOT NULL,
    source TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_tierlist_moves_session ON reaction_tierlist_moves(session_id);

ALTER TABLE reaction_tierlist_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE reaction_tierlist_moves ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-01 Webinar Companion Tables
CREATE TABLE IF NOT EXISTS webinar_companion_sessions (
    session_id TEXT PRIMARY KEY,
    webinar_id TEXT NOT NULL,
    session_mode TEXT NOT NULL,
    video_url TEXT NOT NULL,
    protected_focal_region JSONB NOT NULL,
    participation_open BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS webinar_participation_captures (
    capture_id TEXT PRIMARY KEY,
    webinar_id TEXT NOT NULL,
    participant_person_id TEXT NOT NULL,
    prompt_id TEXT NOT NULL,
    slide_index_start INTEGER NOT NULL,
    slide_index_end INTEGER NOT NULL,
    reaction_type TEXT NOT NULL,
    submitted_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS webinar_rep_slide_scores (
    rep_session_id TEXT NOT NULL,
    slide_index INTEGER NOT NULL,
    hedge_density NUMERIC NOT NULL,
    pause_architecture_score NUMERIC NOT NULL,
    cta_pressure_stability NUMERIC NOT NULL,
    feedback_summary TEXT NOT NULL,
    delivered_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (rep_session_id, slide_index)
);

CREATE TABLE IF NOT EXISTS webinar_prompt_anchors (
    prompt_id TEXT PRIMARY KEY,
    webinar_id TEXT NOT NULL,
    trigger_at_seconds NUMERIC NOT NULL,
    prompt_type TEXT NOT NULL,
    preferred_geometry TEXT NOT NULL
);

ALTER TABLE webinar_companion_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE webinar_participation_captures ENABLE ROW LEVEL SECURITY;
ALTER TABLE webinar_rep_slide_scores ENABLE ROW LEVEL SECURITY;
ALTER TABLE webinar_prompt_anchors ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-10 Onboarding Flow Tables
CREATE TABLE IF NOT EXISTS anonymous_onboarding_sessions (
    session_id TEXT PRIMARY KEY,
    coach_id TEXT NOT NULL,
    state TEXT NOT NULL,
    referral_token_id TEXT,
    anonymous_device_nonce TEXT NOT NULL,
    benchmark_revealed_at TIMESTAMPTZ,
    linked_person_id TEXT,
    created_at_utc TIMESTAMPTZ NOT NULL,
    updated_at_utc TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS anonymous_onboarding_audio_assets (
    audit_asset_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES anonymous_onboarding_sessions(session_id),
    storage_path TEXT NOT NULL,
    duration_seconds INTEGER NOT NULL,
    mime_type TEXT NOT NULL,
    upload_status TEXT NOT NULL,
    uploaded_at_utc TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS anonymous_onboarding_teasers (
    teaser_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES anonymous_onboarding_sessions(session_id),
    benchmark_score INTEGER NOT NULL,
    score_label TEXT NOT NULL,
    one_line_insight TEXT NOT NULL,
    next_move_hint TEXT NOT NULL,
    confidence_note TEXT NOT NULL,
    revealed_at_utc TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS onboarding_offer_impressions (
    impression_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES anonymous_onboarding_sessions(session_id),
    offer_tier_ceiling TEXT NOT NULL,
    target_campaign_tier INTEGER NOT NULL,
    gate_verdict TEXT NOT NULL,
    decision TEXT,
    created_at_utc TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS anonymous_registration_links (
    link_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES anonymous_onboarding_sessions(session_id),
    registration_mode TEXT NOT NULL,
    person_id TEXT,
    lead_id TEXT,
    linked_at_utc TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS onboarding_referral_tokens (
    referral_token_id TEXT PRIMARY KEY,
    coach_id TEXT NOT NULL,
    source_artifact_id TEXT,
    channel TEXT NOT NULL,
    created_at_utc TIMESTAMPTZ NOT NULL
);

ALTER TABLE anonymous_onboarding_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE anonymous_onboarding_audio_assets ENABLE ROW LEVEL SECURITY;
ALTER TABLE anonymous_onboarding_teasers ENABLE ROW LEVEL SECURITY;
ALTER TABLE onboarding_offer_impressions ENABLE ROW LEVEL SECURITY;
ALTER TABLE anonymous_registration_links ENABLE ROW LEVEL SECURITY;
ALTER TABLE onboarding_referral_tokens ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-11 Challenge Arena Tables
CREATE TABLE IF NOT EXISTS challenge_arena_participants (
    participant_id TEXT PRIMARY KEY,
    capacity_track TEXT NOT NULL,
    current_layer TEXT NOT NULL,
    session_index INTEGER NOT NULL,
    layer_attempt_count INTEGER NOT NULL,
    active_days_this_week INTEGER NOT NULL,
    streak_count INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS challenge_arena_sessions (
    session_id TEXT PRIMARY KEY,
    participant_id TEXT NOT NULL REFERENCES challenge_arena_participants(participant_id),
    command_key TEXT NOT NULL,
    variation_key TEXT NOT NULL,
    readiness_verdict TEXT,
    completion_status TEXT NOT NULL,
    completed_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS challenge_arena_variation_history (
    history_id TEXT PRIMARY KEY,
    participant_id TEXT NOT NULL REFERENCES challenge_arena_participants(participant_id),
    layer TEXT NOT NULL,
    ui_route_fingerprint TEXT NOT NULL,
    assigned_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS challenge_arena_weekly_rollups (
    rollup_id TEXT PRIMARY KEY,
    participant_id TEXT NOT NULL REFERENCES challenge_arena_participants(participant_id),
    week_start_utc TIMESTAMPTZ NOT NULL,
    week_end_utc TIMESTAMPTZ NOT NULL,
    sessions_completed INTEGER NOT NULL,
    cumulative_words_spoken INTEGER NOT NULL,
    cumulative_micro_pauses INTEGER NOT NULL,
    delta_words_spoken INTEGER NOT NULL,
    delta_hedge_frequency NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS challenge_arena_sunday_postcards (
    postcard_id TEXT PRIMARY KEY,
    participant_id TEXT NOT NULL REFERENCES challenge_arena_participants(participant_id),
    rollup_id TEXT NOT NULL REFERENCES challenge_arena_weekly_rollups(rollup_id),
    qualitative_interpretation TEXT NOT NULL,
    forward_forecast TEXT NOT NULL,
    status TEXT NOT NULL,
    published_at TIMESTAMPTZ NOT NULL,
    acknowledged_at TIMESTAMPTZ
);

ALTER TABLE challenge_arena_participants ENABLE ROW LEVEL SECURITY;
ALTER TABLE challenge_arena_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE challenge_arena_variation_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE challenge_arena_weekly_rollups ENABLE ROW LEVEL SECURITY;
ALTER TABLE challenge_arena_sunday_postcards ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-13 Experience Ladder Tables
CREATE TABLE IF NOT EXISTS experience_state_packets (
    packet_id TEXT PRIMARY KEY,
    client_id TEXT NOT NULL,
    coach_id TEXT NOT NULL,
    active_surface TEXT NOT NULL,
    stage TEXT NOT NULL,
    momentum_level TEXT NOT NULL,
    recovery_state TEXT NOT NULL,
    packet_json JSONB NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    UNIQUE(client_id, coach_id)
);
CREATE INDEX IF NOT EXISTS idx_experience_state_packets_coach_id ON experience_state_packets(coach_id);
CREATE INDEX IF NOT EXISTS idx_experience_state_packets_active_surface ON experience_state_packets(active_surface);

CREATE TABLE IF NOT EXISTS experience_route_events (
    route_id TEXT PRIMARY KEY,
    client_id TEXT NOT NULL,
    coach_id TEXT NOT NULL,
    from_surface TEXT NOT NULL,
    to_surface TEXT NOT NULL,
    reason TEXT NOT NULL,
    next_step_type TEXT NOT NULL,
    route_latency_ms INTEGER NOT NULL CHECK (route_latency_ms <= 3000),
    created_at TIMESTAMPTZ NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_experience_route_events_client_id ON experience_route_events(client_id);
CREATE INDEX IF NOT EXISTS idx_experience_route_events_to_surface ON experience_route_events(to_surface);

CREATE TABLE IF NOT EXISTS surface_readiness_snapshots (
    snapshot_id TEXT PRIMARY KEY,
    client_id TEXT NOT NULL,
    surface TEXT NOT NULL,
    readiness_score NUMERIC NOT NULL,
    journey_id TEXT,
    active_task_id TEXT,
    calculated_at TIMESTAMPTZ NOT NULL,
    UNIQUE(client_id, surface)
);
CREATE INDEX IF NOT EXISTS idx_surface_readiness_snapshots_surface ON surface_readiness_snapshots(surface);
CREATE INDEX IF NOT EXISTS idx_surface_readiness_snapshots_readiness_score ON surface_readiness_snapshots(readiness_score);

CREATE TABLE IF NOT EXISTS inline_reward_packets (
    reward_id TEXT PRIMARY KEY,
    client_id TEXT NOT NULL,
    surface TEXT NOT NULL,
    next_step_type TEXT NOT NULL,
    headline TEXT NOT NULL,
    body TEXT NOT NULL,
    task_ticket_id TEXT,
    created_at TIMESTAMPTZ NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_inline_reward_packets_client_id ON inline_reward_packets(client_id);
CREATE INDEX IF NOT EXISTS idx_inline_reward_packets_surface ON inline_reward_packets(surface);

CREATE TABLE IF NOT EXISTS async_content_exhaust_jobs (
    job_id TEXT PRIMARY KEY,
    client_id TEXT NOT NULL,
    surface TEXT NOT NULL,
    source_route_id TEXT NOT NULL,
    job_type TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_async_content_exhaust_jobs_source_route_id ON async_content_exhaust_jobs(source_route_id);
CREATE INDEX IF NOT EXISTS idx_async_content_exhaust_jobs_status ON async_content_exhaust_jobs(status);

ALTER TABLE experience_state_packets ENABLE ROW LEVEL SECURITY;
ALTER TABLE experience_route_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE surface_readiness_snapshots ENABLE ROW LEVEL SECURITY;
ALTER TABLE inline_reward_packets ENABLE ROW LEVEL SECURITY;
ALTER TABLE async_content_exhaust_jobs ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-19 Testimonial Builder Tables
CREATE TABLE IF NOT EXISTS testimonial_capture_sessions (
    capture_session_id TEXT PRIMARY KEY,
    person_id TEXT NOT NULL,
    coach_id TEXT NOT NULL,
    trigger_json JSONB NOT NULL,
    preferred_media_mode TEXT NOT NULL,
    status TEXT NOT NULL,
    current_step TEXT NOT NULL,
    reflection_text_transcript TEXT,
    primary_media_asset_id TEXT,
    attachment_asset_ids JSONB,
    tags JSONB,
    consent_level TEXT,
    created_at_utc TIMESTAMPTZ NOT NULL,
    updated_at_utc TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS testimonial_media_assets (
    asset_id TEXT PRIMARY KEY,
    asset_type TEXT NOT NULL,
    storage_path TEXT NOT NULL,
    duration_seconds INTEGER,
    mime_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS testimonial_proof_objects (
    proof_object_id TEXT PRIMARY KEY,
    capture_session_id TEXT NOT NULL REFERENCES testimonial_capture_sessions(capture_session_id),
    person_id TEXT NOT NULL,
    coach_id TEXT NOT NULL,
    title TEXT NOT NULL,
    narrative_summary TEXT NOT NULL,
    primary_media_asset_id TEXT NOT NULL,
    attachment_asset_ids JSONB,
    consent_level TEXT NOT NULL,
    trigger_kind TEXT NOT NULL,
    delta_headline TEXT,
    share_ready BOOLEAN NOT NULL DEFAULT FALSE,
    created_at_utc TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS user_card_snapshots (
    snapshot_id TEXT PRIMARY KEY,
    person_id TEXT NOT NULL,
    weekly_period_key TEXT NOT NULL,
    solo_tier TEXT NOT NULL,
    strongest_primitive_id TEXT,
    streak_count INTEGER NOT NULL,
    metrics JSONB NOT NULL,
    created_at_utc TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS peer_endorsement_verdicts (
    verdict_id TEXT PRIMARY KEY,
    person_id TEXT NOT NULL,
    verdict TEXT NOT NULL,
    evidence JSONB,
    rationale TEXT NOT NULL,
    locked_message TEXT,
    decided_at_utc TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS peer_endorsement_policies (
    policy_id TEXT PRIMARY KEY,
    program_id TEXT NOT NULL,
    threshold_required INTEGER NOT NULL,
    accepted_pathways JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS community_peer_certifications (
    certification_id TEXT PRIMARY KEY,
    person_id TEXT NOT NULL,
    certified_as TEXT NOT NULL,
    certified_at_utc TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS testimonial_share_events (
    share_event_id TEXT PRIMARY KEY,
    artifact_kind TEXT NOT NULL,
    artifact_id TEXT NOT NULL,
    published_destinations JSONB NOT NULL,
    silent_referral_routed BOOLEAN NOT NULL DEFAULT FALSE,
    receipt_id TEXT NOT NULL
);

ALTER TABLE testimonial_capture_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE testimonial_media_assets ENABLE ROW LEVEL SECURITY;
ALTER TABLE testimonial_proof_objects ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_card_snapshots ENABLE ROW LEVEL SECURITY;
ALTER TABLE peer_endorsement_verdicts ENABLE ROW LEVEL SECURITY;
ALTER TABLE peer_endorsement_policies ENABLE ROW LEVEL SECURITY;
ALTER TABLE community_peer_certifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE testimonial_share_events ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-ScoreCard Viewer Tables
CREATE TABLE IF NOT EXISTS score_viewer_sessions (
    session_id TEXT PRIMARY KEY,
    coach_id TEXT NOT NULL,
    scorecard_version TEXT NOT NULL,
    opened_at_utc TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS score_viewer_reflection_acks (
    ack_id TEXT PRIMARY KEY,
    coach_id TEXT NOT NULL,
    session_id TEXT NOT NULL REFERENCES score_viewer_sessions(session_id),
    insight_key TEXT NOT NULL,
    acknowledged_next_step TEXT NOT NULL,
    receipt_id TEXT NOT NULL,
    created_at_utc TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS score_viewer_projection_cache (
    cache_id TEXT PRIMARY KEY,
    coach_id TEXT NOT NULL,
    scorecard_version TEXT NOT NULL,
    projection_json JSONB NOT NULL,
    cached_at_utc TIMESTAMPTZ NOT NULL,
    UNIQUE(coach_id, scorecard_version)
);

ALTER TABLE score_viewer_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE score_viewer_reflection_acks ENABLE ROW LEVEL SECURITY;
ALTER TABLE score_viewer_projection_cache ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-14 Stealth Course Commercial Ladder Tables
CREATE TABLE IF NOT EXISTS commercial_ladder_events (
    event_id TEXT PRIMARY KEY,
    client_id TEXT NOT NULL,
    coach_id TEXT NOT NULL,
    journey_id TEXT NOT NULL,
    locked_node_id TEXT NOT NULL,
    governor_evaluation_id TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL
);

ALTER TABLE commercial_ladder_events ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-21 SDA Query and Crosswalk Service Tables
CREATE TABLE IF NOT EXISTS sda_query_audit (
    audit_id              TEXT PRIMARY KEY,
    action_type           TEXT NOT NULL,
    queryable_surface     TEXT NOT NULL,
    request_payload       JSONB NOT NULL,
    response_summary      JSONB NOT NULL,
    provenance_bundle     JSONB NOT NULL,
    used_stale_fallback   BOOLEAN NOT NULL DEFAULT FALSE,
    fallback_reason       TEXT,
    latency_ms            REAL NOT NULL,
    created_at            TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE sda_query_audit ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-02 In-Chat Telegram Payments Tables
CREATE TABLE IF NOT EXISTS payment_transactions (
    transaction_id TEXT PRIMARY KEY,
    telegram_user_id BIGINT NOT NULL,
    coach_id TEXT NOT NULL,
    tier TEXT NOT NULL,
    amount_cents INTEGER NOT NULL,
    status TEXT NOT NULL,
    stripe_charge_id TEXT DEFAULT '',
    eligibility_id TEXT NOT NULL,
    reward_dispatched BOOLEAN NOT NULL DEFAULT FALSE,
    provisioning_complete BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS tier_subscriptions (
    subscription_id TEXT PRIMARY KEY,
    telegram_user_id BIGINT NOT NULL,
    coach_id TEXT NOT NULL,
    tier TEXT NOT NULL,
    stripe_subscription_id TEXT DEFAULT '',
    status TEXT NOT NULL DEFAULT 'active',
    started_at TIMESTAMPTZ NOT NULL
);

ALTER TABLE payment_transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE tier_subscriptions ENABLE ROW LEVEL SECURITY;

-- FR-COM-01 AFFiNE Billing & Credit System Tables
CREATE TABLE IF NOT EXISTS coach_subscriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coach_id UUID NOT NULL UNIQUE,
    stripe_customer_id VARCHAR(50) NOT NULL UNIQUE,
    stripe_subscription_id VARCHAR(50) NOT NULL UNIQUE,
    stripe_metered_item_id VARCHAR(50),
    tier VARCHAR(30) NOT NULL DEFAULT 'proof_layer' CHECK (tier IN ('proof_layer', 'speaking_learning', 'coach_os', 'elite')),
    monthly_base_price_cents INTEGER NOT NULL DEFAULT 0,
    alacarte_video_price_cents INTEGER NOT NULL DEFAULT 999,
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'past_due', 'cancelled', 'paused')),
    payment_method_last4 VARCHAR(4),
    current_period_start TIMESTAMPTZ,
    current_period_end TIMESTAMPTZ,
    total_monthly_cost_cents INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sub_coach ON coach_subscriptions(coach_id);
CREATE INDEX IF NOT EXISTS idx_sub_status ON coach_subscriptions(status);
ALTER TABLE coach_subscriptions ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS billing_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coach_id UUID NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    stripe_event_id VARCHAR(100) UNIQUE,
    amount_cents INTEGER,
    description TEXT,
    receipt_chain_block VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_billing_coach ON billing_events(coach_id);
CREATE INDEX IF NOT EXISTS idx_billing_type ON billing_events(event_type);
ALTER TABLE billing_events ENABLE ROW LEVEL SECURITY;

-- FR-APR-08 Orchestration Dichotomy Tables
CREATE TABLE IF NOT EXISTS coalition_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coach_id UUID NOT NULL,
    coalition_signature JSONB NOT NULL,
    edge_product JSONB NOT NULL,
    primitive_candidates JSONB NOT NULL,
    validation_status VARCHAR(20) NOT NULL CHECK (validation_status IN ('validated', 'fallback_used', 'centroid_rejected')),
    anti_centroid_score FLOAT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_coalition_coach ON coalition_history(coach_id);
CREATE INDEX IF NOT EXISTS idx_coalition_status ON coalition_history(validation_status);
ALTER TABLE coalition_history ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS coalition_fatalities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coalition_id UUID NOT NULL,
    edge_product_id VARCHAR(100) NOT NULL,
    expected_engagement FLOAT,
    actual_engagement FLOAT,
    delta_percentage FLOAT,
    diagnosis TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE coalition_fatalities ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-18 CBCS Four-Engine Runtime Tables
CREATE TABLE IF NOT EXISTS semantic_evolution_record (
    record_id TEXT PRIMARY KEY,
    client_id TEXT NOT NULL,
    coach_id TEXT NOT NULL,
    recursive_patterns JSONB NOT NULL DEFAULT '[]',
    feedback_loops JSONB NOT NULL DEFAULT '[]',
    last_updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_ser_client ON semantic_evolution_record(client_id);
CREATE INDEX IF NOT EXISTS idx_ser_coach ON semantic_evolution_record(coach_id);
ALTER TABLE semantic_evolution_record ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-25 AR Overlay Capture Pipeline Tables
CREATE TABLE IF NOT EXISTS overlay_interaction_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    timestamp_ms BIGINT NOT NULL,
    round_index INTEGER,
    from_state TEXT,
    to_state TEXT,
    overlay_elements JSONB DEFAULT '{}',
    capture_state JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_overlay_events_session ON overlay_interaction_events(session_id);
CREATE INDEX IF NOT EXISTS idx_overlay_events_type ON overlay_interaction_events(event_type);
ALTER TABLE overlay_interaction_events ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS overlay_capture_metadata (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id TEXT NOT NULL,
    coach_id TEXT NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    frame_rate INTEGER NOT NULL,
    media_format TEXT NOT NULL,
    device_tier TEXT NOT NULL,
    resolution_downgraded BOOLEAN DEFAULT FALSE,
    capture_status TEXT NOT NULL,
    started_at TIMESTAMPTZ,
    stopped_at TIMESTAMPTZ,
    duration_ms INTEGER DEFAULT 0,
    blob_size_bytes BIGINT DEFAULT 0,
    upload_status TEXT DEFAULT 'pending_background',
    interaction_event_count INTEGER DEFAULT 0,
    audio_track_present BOOLEAN DEFAULT TRUE,
    video_track_present BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_overlay_capture_session ON overlay_capture_metadata(session_id);
CREATE INDEX IF NOT EXISTS idx_overlay_capture_coach ON overlay_capture_metadata(coach_id);
ALTER TABLE overlay_capture_metadata ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-16 Archetype Container Runtime Tables
CREATE TABLE IF NOT EXISTS archetype_runtime_sessions (
    runtime_session_id          TEXT PRIMARY KEY,
    coach_id                    TEXT NOT NULL,
    capture_id                  TEXT NOT NULL,
    coalition_id                TEXT NOT NULL,
    runtime_status              TEXT NOT NULL,
    selected_archetype          TEXT,
    trigger_guard_session_id    TEXT,
    receipt_chain_hash          TEXT NOT NULL,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_acr_sessions_coach ON archetype_runtime_sessions(coach_id);
ALTER TABLE archetype_runtime_sessions ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS archetype_runtime_sentence_audits (
    sentence_audit_id           TEXT PRIMARY KEY,
    runtime_session_id          TEXT NOT NULL,
    sentence_id                 TEXT NOT NULL,
    sentence_index              INTEGER NOT NULL,
    sentence_text               TEXT NOT NULL,
    start_offset                INTEGER NOT NULL,
    end_offset                  INTEGER NOT NULL,
    similarity_score            DOUBLE PRECISION NOT NULL,
    similarity_band             TEXT NOT NULL,
    collapse_reason             TEXT NOT NULL,
    failed                      BOOLEAN NOT NULL DEFAULT FALSE,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_acr_audits_session ON archetype_runtime_sentence_audits(runtime_session_id);
ALTER TABLE archetype_runtime_sentence_audits ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS archetype_container_manifests (
    container_id                TEXT PRIMARY KEY,
    runtime_session_id          TEXT NOT NULL,
    coach_id                    TEXT NOT NULL,
    selected_archetype          TEXT NOT NULL,
    manifest_json               JSONB NOT NULL,
    sfl_function_stack_json     JSONB,
    composition_depth_json      JSONB,
    variation_binding_json      JSONB,
    sfl_binding_status          TEXT NOT NULL DEFAULT 'sfl_not_bound',
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_acr_manifests_session ON archetype_container_manifests(runtime_session_id);
ALTER TABLE archetype_container_manifests ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS archetype_sfl_execution_contracts (
    contract_id              TEXT PRIMARY KEY,
    runtime_session_id       TEXT NOT NULL,
    archetype_choice         TEXT NOT NULL,
    contract_json            JSONB NOT NULL,
    sfl_binding_status       TEXT NOT NULL,
    created_at               TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE archetype_sfl_execution_contracts ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS archetype_runtime_rejections (
    rejection_id                TEXT PRIMARY KEY,
    runtime_session_id          TEXT NOT NULL,
    rejection_code              TEXT NOT NULL,
    similarity_score            DOUBLE PRECISION NOT NULL,
    coaching_fix                TEXT NOT NULL,
    rerecord_prompt             TEXT NOT NULL,
    reroute_token               TEXT,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_acr_rejections_session ON archetype_runtime_rejections(runtime_session_id);
ALTER TABLE archetype_runtime_rejections ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-07 AFFiNE Studio Block Orchestration Tables
CREATE TABLE IF NOT EXISTS affine_client_card_projections (
    projection_id               TEXT PRIMARY KEY,
    coach_id                    TEXT NOT NULL,
    client_id                   TEXT NOT NULL,
    workspace_id                TEXT NOT NULL,
    projection_json             JSONB NOT NULL,
    updated_at                  TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(coach_id, client_id)
);

CREATE INDEX IF NOT EXISTS idx_affine_ccproj_coach ON affine_client_card_projections(coach_id);
ALTER TABLE affine_client_card_projections ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS affine_red_flag_evidence (
    flag_id                     TEXT PRIMARY KEY,
    coach_id                    TEXT NOT NULL,
    client_id                   TEXT NOT NULL,
    severity                    TEXT NOT NULL,
    excerpt_hash                TEXT NOT NULL,
    excerpt_text                TEXT NOT NULL,
    source_type                 TEXT NOT NULL,
    session_id                  TEXT NOT NULL,
    asset_id                    TEXT NOT NULL,
    workspace_entry_id          TEXT NOT NULL,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_affine_rfevid_coach ON affine_red_flag_evidence(coach_id);
CREATE INDEX IF NOT EXISTS idx_affine_rfevid_client ON affine_red_flag_evidence(client_id);
CREATE INDEX IF NOT EXISTS idx_affine_rfevid_hash ON affine_red_flag_evidence(excerpt_hash);
ALTER TABLE affine_red_flag_evidence ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS affine_intercept_review_acks (
    acknowledgement_id          TEXT PRIMARY KEY,
    flag_id                     TEXT NOT NULL,
    coach_id                    TEXT NOT NULL,
    client_id                   TEXT NOT NULL,
    excerpt_hash                TEXT NOT NULL,
    ack_phrase                  TEXT NOT NULL,
    acknowledged_at             TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(flag_id, coach_id, excerpt_hash)
);

CREATE INDEX IF NOT EXISTS idx_affine_acks_acked_at ON affine_intercept_review_acks(acknowledged_at);
ALTER TABLE affine_intercept_review_acks ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS affine_intercept_sessions (
    intercept_id                TEXT PRIMARY KEY,
    flag_id                     TEXT NOT NULL,
    coach_id                    TEXT NOT NULL,
    client_id                   TEXT NOT NULL,
    workspace_id                TEXT NOT NULL,
    recorder_session_id         TEXT DEFAULT '',
    gate_status                 TEXT NOT NULL CHECK (gate_status IN ('locked', 'ready', 'recording', 'completed', 'blocked')),
    started_at                  TIMESTAMPTZ,
    completed_at                TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_affine_intercepts_coach ON affine_intercept_sessions(coach_id);
ALTER TABLE affine_intercept_sessions ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS affine_broadcast_queue (
    broadcast_session_id        TEXT PRIMARY KEY,
    coach_id                    TEXT NOT NULL,
    workspace_id                TEXT NOT NULL,
    program_id                  TEXT NOT NULL,
    studio_session_id           TEXT DEFAULT '',
    title                       TEXT NOT NULL,
    status                      TEXT NOT NULL,
    audience_surface            TEXT NOT NULL DEFAULT 'telegram',
    planned_start_at            TIMESTAMPTZ,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_affine_bcast_coach ON affine_broadcast_queue(coach_id);
CREATE INDEX IF NOT EXISTS idx_affine_bcast_status ON affine_broadcast_queue(status);
ALTER TABLE affine_broadcast_queue ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-09 Conscious Editor Mini App Tables
CREATE TABLE IF NOT EXISTS conscious_editor_sessions (
    editor_session_id           TEXT PRIMARY KEY,
    coach_id                    TEXT NOT NULL,
    source_audio_asset_id       TEXT NOT NULL,
    content_output_id           TEXT,
    vcb_id                      TEXT,
    composition_id              TEXT,
    status                      TEXT NOT NULL,
    tier                        TEXT NOT NULL,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_ced_sessions_coach ON conscious_editor_sessions(coach_id);
CREATE INDEX IF NOT EXISTS idx_ced_sessions_source ON conscious_editor_sessions(source_audio_asset_id);
ALTER TABLE conscious_editor_sessions ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS conscious_editor_transcript_revisions (
    revision_id                 TEXT PRIMARY KEY,
    editor_session_id           TEXT NOT NULL,
    source_kind                 TEXT NOT NULL,
    author_person_id            TEXT NOT NULL,
    revision_note               TEXT DEFAULT '',
    revised_plaintext           TEXT NOT NULL,
    revised_json_payload        TEXT NOT NULL,
    token_patches_json          JSONB DEFAULT '[]',
    requires_timing_reflow      BOOLEAN DEFAULT FALSE,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_ced_revisions_session ON conscious_editor_transcript_revisions(editor_session_id);
ALTER TABLE conscious_editor_transcript_revisions ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS conscious_editor_rerender_jobs (
    job_id                      TEXT PRIMARY KEY,
    editor_session_id           TEXT NOT NULL,
    revision_id                 TEXT NOT NULL,
    scope                       TEXT NOT NULL,
    rationale                   TEXT NOT NULL,
    affected_slide_indices      JSONB DEFAULT '[]',
    requires_vcb_refresh        BOOLEAN DEFAULT FALSE,
    requires_audio_rerecord     BOOLEAN DEFAULT FALSE,
    requires_nim_rerun          BOOLEAN DEFAULT FALSE,
    status                      TEXT NOT NULL DEFAULT 'queued',
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at                TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_ced_rerender_session ON conscious_editor_rerender_jobs(editor_session_id);
CREATE INDEX IF NOT EXISTS idx_ced_rerender_composition ON conscious_editor_rerender_jobs(editor_session_id);
ALTER TABLE conscious_editor_rerender_jobs ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS conscious_editor_lineage_links (
    node_id                     TEXT PRIMARY KEY,
    editor_session_id           TEXT NOT NULL,
    node_type                   TEXT NOT NULL,
    referenced_id               TEXT NOT NULL,
    label                       TEXT NOT NULL,
    parent_node_id              TEXT,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_ced_lineage_session ON conscious_editor_lineage_links(editor_session_id);
ALTER TABLE conscious_editor_lineage_links ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS conscious_editor_operator_decisions (
    decision_id                 TEXT PRIMARY KEY,
    editor_session_id           TEXT NOT NULL,
    coach_id                    TEXT NOT NULL,
    decision                    TEXT NOT NULL,
    decision_note               TEXT DEFAULT '',
    resulting_status            TEXT NOT NULL,
    receipt_event_id            TEXT NOT NULL,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_ced_decisions_session ON conscious_editor_operator_decisions(editor_session_id);
ALTER TABLE conscious_editor_operator_decisions ENABLE ROW LEVEL SECURITY;

-- FR-ERA3-12 CMF Arc-Governed Rendering Tables
CREATE TABLE IF NOT EXISTS cmf_arc_render_jobs (
    job_id                      TEXT PRIMARY KEY,
    content_output_id           TEXT NOT NULL,
    coach_id                    TEXT NOT NULL,
    selected_format             TEXT NOT NULL,
    status                      TEXT NOT NULL,
    manifest_id                 TEXT DEFAULT '',
    composition_id              TEXT DEFAULT '',
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at                  TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(content_output_id, selected_format)
);
CREATE INDEX IF NOT EXISTS idx_cmf_arj_coach ON cmf_arc_render_jobs(coach_id);
CREATE INDEX IF NOT EXISTS idx_cmf_arj_status ON cmf_arc_render_jobs(status);
ALTER TABLE cmf_arc_render_jobs ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS cmf_beat_cluster_plans (
    cluster_id                  TEXT PRIMARY KEY,
    job_id                      TEXT NOT NULL,
    cluster_type                TEXT NOT NULL,
    order_index                 INTEGER NOT NULL,
    start_ms                    INTEGER NOT NULL,
    end_ms                      INTEGER NOT NULL CHECK (end_ms > start_ms),
    shot_grammar                TEXT NOT NULL,
    cluster_json                JSONB NOT NULL,
    UNIQUE(job_id, order_index)
);
CREATE INDEX IF NOT EXISTS idx_cmf_bcp_job ON cmf_beat_cluster_plans(job_id);
ALTER TABLE cmf_beat_cluster_plans ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS cmf_first_frame_checks (
    check_id                    TEXT PRIMARY KEY,
    job_id                      TEXT NOT NULL,
    cluster_id                  TEXT NOT NULL,
    verdict                     TEXT NOT NULL,
    authority_score             DOUBLE PRECISION NOT NULL,
    contrast_score              DOUBLE PRECISION NOT NULL,
    recognizability_score       DOUBLE PRECISION NOT NULL,
    anti_generic_flags          JSONB DEFAULT '[]',
    checked_at                  TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(job_id, cluster_id)
);
CREATE INDEX IF NOT EXISTS idx_cmf_ffc_verdict ON cmf_first_frame_checks(verdict);
ALTER TABLE cmf_first_frame_checks ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS cmf_epic_meaning_gate_results (
    gate_id                     TEXT PRIMARY KEY,
    job_id                      TEXT NOT NULL UNIQUE,
    verdict                     TEXT NOT NULL,
    blandness_confidence        DOUBLE PRECISION DEFAULT 0.0,
    failed_rules                JSONB DEFAULT '[]',
    rationale                   TEXT NOT NULL,
    checked_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_cmf_emg_verdict ON cmf_epic_meaning_gate_results(verdict);
ALTER TABLE cmf_epic_meaning_gate_results ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS cmf_render_manifests (
    manifest_id                 TEXT PRIMARY KEY,
    job_id                      TEXT NOT NULL UNIQUE,
    vcb_id                      TEXT NOT NULL,
    render_target_path          TEXT NOT NULL,
    manifest_json               JSONB NOT NULL,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_cmf_rm_vcb ON cmf_render_manifests(vcb_id);
ALTER TABLE cmf_render_manifests ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS cmf_render_perceptual_plans (
    plan_id                      TEXT PRIMARY KEY,
    content_output_id            TEXT NOT NULL,
    coach_id                     TEXT NOT NULL,
    surface_type                 TEXT NOT NULL,
    function_stack_packet_id     TEXT NOT NULL,
    directional_integrity_report_id TEXT NOT NULL,
    perceptual_influence_report_id TEXT NOT NULL,
    depth_profile_json           JSONB NOT NULL,
    variation_hints_json         JSONB NOT NULL,
    temporal_hints_json          JSONB NOT NULL,
    target_thumbnail_count       INTEGER NOT NULL,
    card_safe                    BOOLEAN NOT NULL DEFAULT FALSE,
    pdf_safe                     BOOLEAN NOT NULL DEFAULT FALSE,
    generated_at                 TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_cmf_rpp_coach ON cmf_render_perceptual_plans(coach_id);
ALTER TABLE cmf_render_perceptual_plans ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS cmf_render_preservation_reports (
    report_id                    TEXT PRIMARY KEY,
    plan_id                      TEXT NOT NULL,
    manifest_id                  TEXT DEFAULT '',
    fallback_decision            TEXT NOT NULL,
    dimensions_json              JSONB NOT NULL,
    lost_intents                 JSONB NOT NULL DEFAULT '[]',
    downgraded_surfaces          JSONB NOT NULL DEFAULT '[]',
    reviewer_notes               JSONB NOT NULL DEFAULT '[]',
    created_at                   TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_cmf_rpr_plan ON cmf_render_preservation_reports(plan_id);
ALTER TABLE cmf_render_preservation_reports ENABLE ROW LEVEL SECURITY;


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
"""

SCHEMA_SQL = f"{SCHEMA_SQL}\n{PRIMITIVE_QUERY_AUDIT_SQL}\n"

# -- FR-CA11-16 Studio Block Tables
STUDIO_BLOCK_SQL = """
CREATE TABLE IF NOT EXISTS studio_sessions (
    id                              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    coach_id                        UUID NOT NULL,
    source_page_id                  VARCHAR(255),
    recording_mode                  VARCHAR(30) NOT NULL,
    aspect_ratio                    VARCHAR(5) NOT NULL,
    resolution                      VARCHAR(10) NOT NULL,
    s3_recording_url                TEXT,
    s3_vod_url                      TEXT,
    duration_seconds                INTEGER,
    is_stream                       BOOLEAN DEFAULT FALSE,
    stream_destinations             JSONB,
    affine_broadcast_target_page_id VARCHAR(255),
    cmf_pipeline_template           VARCHAR(50),
    cmf_job_id                      UUID,
    receipt_chain_id                UUID,
    status                          VARCHAR(20) DEFAULT 'recording',
    started_at                      TIMESTAMPTZ NOT NULL,
    ended_at                        TIMESTAMPTZ,
    created_at                      TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_studio_sessions_coach ON studio_sessions(coach_id);
CREATE INDEX IF NOT EXISTS idx_studio_sessions_status ON studio_sessions(status);
ALTER TABLE studio_sessions ENABLE ROW LEVEL SECURITY;
"""

SCHEMA_SQL = f"{SCHEMA_SQL}\n{STUDIO_BLOCK_SQL}\n"

PHASE0_WORKSPACE_SQL = """
-- FR-ERA3-34 Phase-0 Prospect Workspace and Artifact Store Tables
CREATE TABLE IF NOT EXISTS phase0_workspaces (
    workspace_id               TEXT PRIMARY KEY,
    prospect_id                TEXT NOT NULL,
    prospect_packet_id         TEXT NOT NULL,
    coach_id                   TEXT,
    display_name               TEXT NOT NULL,
    status                     TEXT NOT NULL DEFAULT 'created'
        CHECK (status IN ('created','intake_received','artifacts_collecting',
            'audit_in_progress','preview_ready','delivered',
            'payment_unlocked','upgraded','archived','blocked')),
    artifact_count             INTEGER NOT NULL DEFAULT 0,
    campaign_id                TEXT,
    delivery_sla_deadline_utc  TIMESTAMPTZ,
    created_at                 TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at                 TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by_receipt_id      TEXT NOT NULL,
    last_transition_receipt_id TEXT
);
CREATE INDEX IF NOT EXISTS idx_p0w_prospect ON phase0_workspaces(prospect_id);
CREATE INDEX IF NOT EXISTS idx_p0w_status ON phase0_workspaces(status);
ALTER TABLE phase0_workspaces ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS phase0_artifacts (
    artifact_id            TEXT PRIMARY KEY,
    workspace_id           TEXT NOT NULL REFERENCES phase0_workspaces(workspace_id),
    prospect_id            TEXT NOT NULL,
    family                 TEXT NOT NULL CHECK (family IN (
        'intake_source','normalized_source','audit_report',
        'preview_asset','produced_proof','payment_bridge','upgrade_metadata')),
    status                 TEXT NOT NULL DEFAULT 'uploaded' CHECK (status IN (
        'uploaded','normalized','audit_ready','preview_ready',
        'delivered','payment_unlocked','upgraded','quarantined','rejected')),
    display_label          TEXT NOT NULL,
    mime_type              TEXT,
    file_size_bytes        BIGINT,
    storage_uri            TEXT,
    checksum_sha256        TEXT,
    parent_artifact_ids    JSONB NOT NULL DEFAULT '[]',
    source_receipt_id      TEXT NOT NULL,
    metadata               JSONB NOT NULL DEFAULT '{}',
    created_at             TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at             TIMESTAMPTZ NOT NULL DEFAULT now(),
    transitioned_at        TIMESTAMPTZ,
    transition_receipt_id  TEXT
);
CREATE INDEX IF NOT EXISTS idx_p0a_workspace ON phase0_artifacts(workspace_id);
CREATE INDEX IF NOT EXISTS idx_p0a_family ON phase0_artifacts(family);
CREATE INDEX IF NOT EXISTS idx_p0a_status ON phase0_artifacts(status);
ALTER TABLE phase0_artifacts ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS phase0_artifact_manifests (
    manifest_id              TEXT PRIMARY KEY,
    workspace_id             TEXT NOT NULL REFERENCES phase0_workspaces(workspace_id),
    prospect_id              TEXT NOT NULL,
    assembled_at             TIMESTAMPTZ NOT NULL DEFAULT now(),
    assembly_receipt_id      TEXT NOT NULL,
    intake_sources           JSONB NOT NULL DEFAULT '[]',
    normalized_sources       JSONB NOT NULL DEFAULT '[]',
    audit_reports            JSONB NOT NULL DEFAULT '[]',
    preview_assets           JSONB NOT NULL DEFAULT '[]',
    produced_proofs          JSONB NOT NULL DEFAULT '[]',
    payment_bridges          JSONB NOT NULL DEFAULT '[]',
    upgrade_metadata_refs    JSONB NOT NULL DEFAULT '[]',
    total_artifact_count     INTEGER NOT NULL DEFAULT 0,
    completeness_summary     JSONB NOT NULL DEFAULT '{}',
    is_delivery_ready        BOOLEAN NOT NULL DEFAULT FALSE,
    is_payment_bridge_ready  BOOLEAN NOT NULL DEFAULT FALSE
);
CREATE INDEX IF NOT EXISTS idx_p0am_workspace ON phase0_artifact_manifests(workspace_id);
ALTER TABLE phase0_artifact_manifests ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS phase0_upgrade_bridges (
    bridge_id              TEXT PRIMARY KEY,
    workspace_id           TEXT NOT NULL REFERENCES phase0_workspaces(workspace_id),
    prospect_id            TEXT NOT NULL,
    target_tier            TEXT NOT NULL CHECK (target_tier IN (
        'speaking_learning','coach_os','operator')),
    payment_confirmed      BOOLEAN NOT NULL DEFAULT FALSE,
    payment_receipt_id     TEXT,
    payment_amount_cents   INTEGER CHECK (payment_amount_cents >= 0),
    credit_applied_cents   INTEGER CHECK (credit_applied_cents >= 0),
    migration_status       TEXT NOT NULL DEFAULT 'pending' CHECK (migration_status IN (
        'pending','in_progress','completed','failed','aborted')),
    target_coach_acronym   CHAR(3),
    migration_receipt_id   TEXT,
    initiated_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    confirmed_at           TIMESTAMPTZ,
    completed_at           TIMESTAMPTZ,
    abort_reason           TEXT
);
CREATE INDEX IF NOT EXISTS idx_p0ub_workspace ON phase0_upgrade_bridges(workspace_id);
CREATE INDEX IF NOT EXISTS idx_p0ub_migration ON phase0_upgrade_bridges(migration_status);
ALTER TABLE phase0_upgrade_bridges ENABLE ROW LEVEL SECURITY;
"""

SCHEMA_SQL = f"{SCHEMA_SQL}\n{PHASE0_WORKSPACE_SQL}\n"

STORAGE_BUCKETS = [
    {"name": "sacred-audio", "public": False},
    {"name": "voice-notes", "public": True},  # Public for Notion audio embeds
    {"name": "coach-photos", "public": True},  # Public for Notion image embeds
    {"name": "visual-assets", "public": True},  # Public for Notion image embeds
    {"name": "phase0-artifacts", "public": False},
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
