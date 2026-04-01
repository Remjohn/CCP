-- ==============================================================
-- Migration 004: Visual Control Layer
-- ==============================================================
-- FR-VIS-14: ConsciousSmile Expression Adapter tables
-- FR-VIS-15: ConsciousPose Body Language Library tables
-- FR-VIS-16: First Frame Composer tables
-- FR-VIS-17: Identity LoRA Training Pipeline tables
-- ==============================================================
-- Date: 2026-03-30
-- Version: 1.0
-- Prerequisites: 003_full_schema.sql
-- ==============================================================

-- =====================================================
-- FR-VIS-14: ConsciousSmile Expression Adapter
-- =====================================================

-- Expression channels: 28 FACS-mapped channels
CREATE TABLE IF NOT EXISTS conscious_smile_channels (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    channel_id VARCHAR(10) NOT NULL UNIQUE,
    channel_name VARCHAR(50) NOT NULL UNIQUE,
    facs_action_units VARCHAR(50),
    arkit_blendshapes JSONB NOT NULL,
    somatic_target TEXT NOT NULL,
    mood_state_affinity JSONB,
    min_intensity FLOAT DEFAULT 0.0,
    max_intensity FLOAT DEFAULT 1.0,
    training_phase INTEGER NOT NULL,
    confusion_pairs JSONB,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'trained', 'validated', 'production')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Training run history for the expression adapter
CREATE TABLE IF NOT EXISTS expression_training_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    run_id VARCHAR(50) NOT NULL UNIQUE,
    training_phase INTEGER NOT NULL,
    channels_trained JSONB NOT NULL,
    dataset_image_count INTEGER NOT NULL,
    triplet_count INTEGER,
    base_model VARCHAR(100) NOT NULL,
    lora_rank INTEGER NOT NULL,
    lora_alpha INTEGER NOT NULL,
    learning_rate FLOAT NOT NULL,
    training_steps INTEGER NOT NULL,
    gpu_type VARCHAR(50) NOT NULL,
    training_hours FLOAT,
    output_file_path TEXT NOT NULL,
    output_file_size_mb FLOAT,
    eval_channel_accuracy FLOAT,
    eval_identity_preservation FLOAT,
    eval_confusion_separation FLOAT,
    status VARCHAR(20) DEFAULT 'running' CHECK (status IN ('running', 'completed', 'failed', 'validated')),
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    receipt_chain_block VARCHAR(100)
);

-- Named emotion presets (e.g., "warm_confidence" → multi-channel values)
CREATE TABLE IF NOT EXISTS expression_presets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    preset_name VARCHAR(50) NOT NULL UNIQUE,
    display_name VARCHAR(100) NOT NULL,
    channel_values JSONB NOT NULL,
    mood_state_affinity VARCHAR(30),
    prompt_string TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


-- =====================================================
-- FR-VIS-15: ConsciousPose Body Language Library
-- =====================================================

-- Individual pose atoms (298 total across 7 layers)
CREATE TABLE IF NOT EXISTS conscious_pose_atoms (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cp_id VARCHAR(20) NOT NULL UNIQUE,
    layer VARCHAR(20) NOT NULL CHECK (layer IN (
        'body', 'hands', 'gaze', 'scene', 'mood_visual', 'props', 'multi_character'
    )),
    subcategory VARCHAR(50) NOT NULL,
    position_name VARCHAR(80) NOT NULL,
    display_name VARCHAR(100),
    signal TEXT NOT NULL,
    mood_fit JSONB NOT NULL,
    archetype_fit JSONB,
    mirror_neuron_target TEXT,
    bvt_function TEXT,
    scene_constraint TEXT,
    controlnet_depth_path TEXT,
    controlnet_openpose_path TEXT,
    controlnet_normal_path TEXT,
    has_rendered_assets BOOLEAN DEFAULT false,
    render_status VARCHAR(20) DEFAULT 'pending' CHECK (render_status IN (
        'pending', 'rendering', 'rendered', 'validated', 'production'
    )),
    source_library VARCHAR(20) DEFAULT 'production' CHECK (source_library IN ('production', 'expansion')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_pose_atoms_layer ON conscious_pose_atoms(layer);
CREATE INDEX idx_pose_atoms_mood ON conscious_pose_atoms USING GIN(mood_fit);

-- Pre-composed & named pose compositions
CREATE TABLE IF NOT EXISTS conscious_pose_compositions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    composition_id VARCHAR(50) NOT NULL UNIQUE,
    composition_name VARCHAR(100) NOT NULL,
    composition_type VARCHAR(30) NOT NULL CHECK (composition_type IN (
        'archetype_default', 'memetic_recipe', 'custom', 'campaign'
    )),
    body_cp_id VARCHAR(20) REFERENCES conscious_pose_atoms(cp_id),
    hands_cp_id VARCHAR(20) REFERENCES conscious_pose_atoms(cp_id),
    gaze_cp_id VARCHAR(20) REFERENCES conscious_pose_atoms(cp_id),
    scene_cp_id VARCHAR(20) REFERENCES conscious_pose_atoms(cp_id),
    mood_visual_cp_id VARCHAR(20) REFERENCES conscious_pose_atoms(cp_id),
    props_cp_id VARCHAR(20) REFERENCES conscious_pose_atoms(cp_id),
    multi_char_cp_id VARCHAR(20) REFERENCES conscious_pose_atoms(cp_id),
    archetype_family VARCHAR(50),
    humor_architecture VARCHAR(50),
    composed_asset_path TEXT,
    is_pre_rendered BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ControlNet render job tracking
CREATE TABLE IF NOT EXISTS controlnet_render_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id VARCHAR(50) NOT NULL UNIQUE,
    atom_cp_id VARCHAR(20) NOT NULL,
    camera_cp_id VARCHAR(20),
    render_types JSONB NOT NULL,
    resolution VARCHAR(20) DEFAULT '1024x1024',
    source_rig VARCHAR(50) NOT NULL,
    output_directory TEXT NOT NULL,
    file_count INTEGER,
    status VARCHAR(20) DEFAULT 'queued' CHECK (status IN (
        'queued', 'rendering', 'completed', 'failed', 'validated'
    )),
    gpu_time_seconds FLOAT,
    queued_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT
);


-- =====================================================
-- FR-VIS-16: First Frame Composer
-- =====================================================

-- Generated first frame specifications
CREATE TABLE IF NOT EXISTS first_frame_specs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    spec_id VARCHAR(50) NOT NULL UNIQUE,
    coach_id UUID NOT NULL,
    content_output_id VARCHAR(50),
    beat_cluster_id VARCHAR(50),
    output_format VARCHAR(30) NOT NULL,
    dimensions VARCHAR(20) NOT NULL,
    mood_state VARCHAR(30) NOT NULL,
    cbcs_tier VARCHAR(10) NOT NULL,
    body_cp_id VARCHAR(20),
    hands_cp_id VARCHAR(20),
    gaze_cp_id VARCHAR(20),
    scene_cp_id VARCHAR(20),
    mood_visual_cp_id VARCHAR(20),
    props_cp_id VARCHAR(20),
    expression_channels JSONB NOT NULL,
    expression_preset_name VARCHAR(50),
    text_headline TEXT,
    text_position VARCHAR(30),
    text_font_treatment VARCHAR(50),
    controlnet_depth_path TEXT,
    controlnet_openpose_path TEXT,
    identity_lora_path TEXT NOT NULL,
    adapter_path TEXT NOT NULL,
    negative_prompt TEXT,
    reasoning JSONB,
    anti_draft_passed BOOLEAN DEFAULT true,
    routed_to VARCHAR(50),
    generated_image_path TEXT,
    receipt_chain_block VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_ffs_coach ON first_frame_specs(coach_id);
CREATE INDEX idx_ffs_format ON first_frame_specs(output_format);

-- Named composition presets for first frames
CREATE TABLE IF NOT EXISTS first_frame_presets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    preset_name VARCHAR(50) NOT NULL UNIQUE,
    display_name VARCHAR(100) NOT NULL,
    mood_state VARCHAR(30),
    archetype_family VARCHAR(50),
    output_format VARCHAR(30),
    composition JSONB NOT NULL,
    anti_draft_patterns JSONB,
    mcda_score FLOAT,
    source_hook_id VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


-- =====================================================
-- FR-VIS-17: Identity LoRA Training Pipeline
-- =====================================================

-- Per-coach Identity LoRA registry
CREATE TABLE IF NOT EXISTS identity_lora_registry (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coach_id UUID NOT NULL,
    lora_version INTEGER NOT NULL DEFAULT 1,
    trigger_token VARCHAR(50) NOT NULL UNIQUE,
    file_path TEXT NOT NULL,
    file_size_mb FLOAT,
    lora_rank INTEGER NOT NULL,
    lora_alpha INTEGER NOT NULL,
    training_steps INTEGER NOT NULL,
    reference_photo_count INTEGER NOT NULL,
    identity_score FLOAT NOT NULL,
    style_flexibility_score FLOAT,
    expression_neutrality FLOAT,
    conscious_smile_compatible BOOLEAN DEFAULT false,
    inference_weight FLOAT DEFAULT 0.65,
    status VARCHAR(20) DEFAULT 'training' CHECK (status IN (
        'training', 'validating', 'active', 'retired', 'failed'
    )),
    trained_at TIMESTAMP WITH TIME ZONE,
    deployed_at TIMESTAMP WITH TIME ZONE,
    retired_at TIMESTAMP WITH TIME ZONE,
    receipt_chain_block VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(coach_id, lora_version)
);

CREATE INDEX idx_lora_coach ON identity_lora_registry(coach_id);

-- LoRA training job tracking
CREATE TABLE IF NOT EXISTS identity_lora_training_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id VARCHAR(50) NOT NULL UNIQUE,
    coach_id UUID NOT NULL,
    target_version INTEGER NOT NULL,
    reference_photos JSONB NOT NULL,
    training_config JSONB NOT NULL,
    gpu_type VARCHAR(50) NOT NULL,
    training_duration_hours FLOAT,
    attempt_number INTEGER DEFAULT 1,
    validation_report JSONB,
    status VARCHAR(20) DEFAULT 'queued' CHECK (status IN (
        'queued', 'curating', 'training', 'validating', 'completed', 'failed', 'retrying'
    )),
    error_message TEXT,
    queued_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE
);


-- =====================================================
-- Row-Level Security
-- =====================================================

ALTER TABLE conscious_smile_channels ENABLE ROW LEVEL SECURITY;
ALTER TABLE expression_training_runs ENABLE ROW LEVEL SECURITY;
ALTER TABLE expression_presets ENABLE ROW LEVEL SECURITY;
ALTER TABLE conscious_pose_atoms ENABLE ROW LEVEL SECURITY;
ALTER TABLE conscious_pose_compositions ENABLE ROW LEVEL SECURITY;
ALTER TABLE controlnet_render_jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE first_frame_specs ENABLE ROW LEVEL SECURITY;
ALTER TABLE first_frame_presets ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_lora_registry ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity_lora_training_jobs ENABLE ROW LEVEL SECURITY;

-- Coach-scoped policies (first_frame_specs and identity_lora_registry)
CREATE POLICY "Coach sees own first_frame_specs"
    ON first_frame_specs FOR SELECT
    USING (auth.uid() = coach_id);

CREATE POLICY "Coach sees own identity_lora"
    ON identity_lora_registry FOR SELECT
    USING (auth.uid() = coach_id);

-- Service role full access for all tables (platform backend)
CREATE POLICY "Service role: conscious_smile_channels" ON conscious_smile_channels FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Service role: expression_training_runs" ON expression_training_runs FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Service role: expression_presets" ON expression_presets FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Service role: conscious_pose_atoms" ON conscious_pose_atoms FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Service role: conscious_pose_compositions" ON conscious_pose_compositions FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Service role: controlnet_render_jobs" ON controlnet_render_jobs FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Service role: first_frame_specs" ON first_frame_specs FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Service role: first_frame_presets" ON first_frame_presets FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Service role: identity_lora_registry" ON identity_lora_registry FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Service role: identity_lora_training_jobs" ON identity_lora_training_jobs FOR ALL USING (true) WITH CHECK (true);
