# Tech-Spec: FR-VIS-14 — ConsciousSmile Expression Adapter

**Created:** 2026-03-30
**Status:** Ready for Development
**Version:** 1.0 (Aligned to PRD Visual Control Layer Amendment v1.0)
**Architecture Reference:** PRD §CA10 Visual Control Layer, ADR-08, SPEC-INFRA-001 §3.2 (MIG Partition A)
**Skill Implementation:** `skills/visuals/conscious_smile_adapter.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:

- `docs/prd/prd-update-visual-control-layer.md` — FR-VIS-14 definition, ADR-08, DEP-VIS-008
- `docs/architecture/Infrastructure_AWS_NIM_Deployment_Spec.md` — SPEC-INFRA-001 §3.2 MIG Partition A allocation, §7 ComfyUI EFS mounting
- `docs/other files/active lab archive/conscious_smile_training_methodology.md` — Full 527-line engineering spec: CFED dataset, 16-channel FACS taxonomy, PixelSmile adaptation, training procedure
- `lab/CVE + CPSC research papers/Physiological State Specification Language.md` — PSSL formal grammar, bio-aesthetic evidence base
- `lab/CVE + CPSC research papers/Cinematographic Emotional Grammar Framework Research.md` — CEGF Color Architecture Matrix, mood state mapping
- `lab/CCP update/CVE_Documentation_V2.md` — §3 Abel's VCB architecture, expression field requirements
- `docs/architecture/FR-VIS-01_Visual_Composition_Brief_Tech_Spec.md` — VCB schema `expression_spec` field consumed by this component
- `docs/architecture/FR-VIS-03_Paradoxe_PSSL_Prompt_Compilation_Tech_Spec.md` — Downstream consumer: Paradoxe compiles expression params into ComfyUI adapter nodes

---

## 2. Overview

### Problem Statement
The Conscious Coaching Platform generates all Tier 3 (Realistic AI Character) visuals using FLUX 2 Dev with per-coach Identity LoRAs. The current pipeline relies on text prompts for facial expressions — "a warm smile," "a look of concern" — which produces generic, inconsistent, and often anatomically incorrect expressions. The coach's face looks correct (Identity LoRA), but the expression is emotionally dead or random. This is the #1 quality gap between AI-generated coaching content and real photography, and it directly undermines the Emotional Contagion research that underpins the platform's engagement model. If the viewer's mirror neuron system cannot read a genuine Duchenne smile, the parasocial bond formation documented in the CVE research does not activate.

### Solution
FR-VIS-14 defines ConsciousSmile — a FACS-based expression adapter for FLUX 2 Dev that provides continuous, composable, muscle-level control over facial expressions. The adapter operates on 28 independently controllable expression channels (each mapped to specific FACS Action Units), accepting continuous intensity values from 0.0 to 1.0. It is trained on the CFED (Conscious Facial Expression Dataset) — a synthetic dataset of ~17,280 images rendered from Unreal Engine 5.6 MetaHuman with mathematically exact expression labels derived from ARKit blendshape parameters. The adapter is loaded dynamically at inference time within the ComfyUI workflow alongside the coach's Identity LoRA — it does not modify FLUX 2 Dev's base weights.

### Scope
**In scope:**
- CFED dataset specification (identity pool, rendering pipeline, annotation schema, confusion pairs)
- Adapter architecture (multi-channel textual latent interpolation on FLUX 2 Dev MMDiT)
- Training procedure (3-phase, custom loss functions: flow matching + symmetric contrastive + identity preservation)
- ComfyUI inference integration (adapter loading, expression prompt syntax, named emotion presets)
- Evaluation metrics (channel accuracy, identity preservation, continuity)
- Database schema for expression channels and training run metadata

**Out of scope:**
- Coach Identity LoRA training (handled by FR-VIS-17)
- Body pose / ControlNet control (handled by FR-VIS-15)
- First Frame composition decisions (handled by FR-VIS-16)
- VCB generation that specifies expression parameters (handled by FR-VIS-01)

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-VIS-008` | ConsciousSmile Adapter Weights | OUTPUT — Trained `.safetensors` file stored on EFS. |
| `DEP-VIS-013` | CFED Dataset | INTERMEDIATE — ~17,280 labeled MetaHuman renders used for training. |
| `DEP-VIS-005` | Visual Composition Brief Schema | UPSTREAM — VCB `expression_spec` field specifies which channels to activate. |
| `DEP-VIS-011` | Identity LoRA Registry | CO-LOADED — Coach Identity LoRA runs alongside ConsciousSmile at inference. |
| `DEP-ENG-016` | Psychological Routing Brief | UPSTREAM — Mood state determines expression preset selection. |
| `DEP-ENG-041` | Receipt Chain Guard | AUDIT — Training runs and inference parameters hashed and recorded. |
| `SPEC-INFRA-001` §3.2 | MIG Partition A (40GB) | RUNTIME — ComfyUI + FLUX + ConsciousSmile runs on this partition. |
| `SPEC-INFRA-001` §7.3 | AWS EFS Model Store | STORAGE — Adapter weights mounted at `/efs/ccp-models/adapters/`. |

### Academic Grounding

| Framework | Author | Year | Mechanism Applied |
|---|---|---|---|
| **PixelSmile** | arXiv 2603.25728v1 | 2026 | Symmetric contrastive training architecture for continuous expression editing via textual latent interpolation. ConsciousSmile extends PixelSmile from 12 emotion-level categories to 28 FACS muscle-level channels, and replaces proxy-labeled AI-generated training data with ground-truth MetaHuman renders. |
| **FACS (Facial Action Coding System)** | Ekman & Friesen | 1978 | Each ConsciousSmile channel maps to specific Action Units (AUs). AU decomposition enables composable expression control — "warm confidence" = `smile:0.6 + eye_squint:0.4 + brow_raise:0.1` rather than a single atomic "happy" category. |
| **Emotional Contagion** | Hatfield et al. | 1994 | The viewer's mirror neuron system involuntarily mimics observed facial expressions within 200ms. Precise AU control ensures the generated expression triggers the intended somatic response (corrugator → concern, zygomaticus → warmth, orbicularis oculi → trust). |
| **Mood State Architecture** | CCP Research Lab | 2026 | The 28 channels are mapped to the platform's mood states (Processing, Escape, Discovery, Status). Named emotion presets translate mood states to multi-channel expression vectors. |

### Technical Decisions

1. **Adapter over LoRA for Expressions:** Validated by MCDA (8.7/10 vs 5.4/10). An adapter operates in the model's latent space and is dynamically loaded. Expressions vary per frame; a LoRA per expression would require hundreds of model files and weight-stacking conflicts with the Identity LoRA.
2. **MetaHuman over AI-Generated Training Data:** PixelSmile used Nano Banana Pro (AI editing) + Gemini 3 Pro (VLM annotation) — both introduce noise. MetaHuman's blendshape parameters ARE the ground-truth labels. Zero annotation error.
3. **28 Channels (expanded from initial 16):** The original 16 channels were expanded to 28 based on MCDA audit identifying gaps in: lip subtlety (`lip_bite`, `lip_purse`, `pout`), social signaling (`smirk`, `tongue_peek`, `wink`), and micro-expression detection (`micro_contempt`, `crow_feet_activation`, `nasolabial_deepen`).
4. **LoRA Weight Budget (1.45 total):** Identity LoRA at 0.65 + ConsciousSmile at 0.80 = 1.45. Acceptable because the two LoRAs modify orthogonal weight regions — Identity learned face structure/texture, ConsciousSmile learned expression geometry transformations.

---

## 4. Implementation Plan

### Stage 1: MetaHuman Identity Pool Construction
*Tools:* Unreal Engine 5.6, MetaHuman Creator
*Inputs:* None (greenfield)
*Outputs:* 20 diverse MetaHuman characters (`CFED_ID_01` through `CFED_ID_20`)

**Steps:**
1. Create 20 MetaHuman identities spanning: gender (10M/10F), age (18-65), ethnicity (5+ groups), body type.
2. Each identity uses a unique Face Texture Index from MetaHuman's 152 available textures.
3. Identities must NOT resemble any specific CCP coach (adapter must stay identity-agnostic).
4. Export all to the Unreal project content folder.

### Stage 2: CFED Dataset Rendering
*Tools:* Unreal Engine 5.6 Python API, custom batch render script
*Inputs:* 20 MetaHuman identities, 28 expression channel definitions
*Outputs:* ~17,280 labeled images + JSON annotation files

**Per-Channel Rendering Protocol:**
```
FOR each identity (20 identities):
  FOR each intensity α ∈ {0.0, 0.2, 0.4, 0.6, 0.8, 1.0}:
    SET all blendshapes to neutral (0.0)
    SET ONLY the target channel's blendshapes to α
    FOR each camera_angle ∈ {front, 30°_left, 30°_right}:
      FOR each lighting_setup ∈ {studio_soft, studio_hard, natural_warm}:
        RENDER at 1024×1024 (FLUX native resolution)
        SAVE image + metadata JSON
```

**Yield:** 20 × 6 × 3 × 3 = 1,080 images per channel. Total: 28 × 1,080 = ~30,240 images (before deduplication of shared α=0.0 neutrals). After deduplication: ~28,800 unique + 1,440 neutrals.

### Stage 3: Confusion Pair Triplet Generation
*Inputs:* CFED base images
*Outputs:* ~1,600 triplet sets for confusion pairs

**Confusion pairs (8 defined):** `smile ↔ dimpler`, `smile ↔ eye_squint`, `brow_raise ↔ eye_wide`, `brow_furrow ↔ eye_squint`, `jaw_open ↔ mouth_frown`, `lip_press ↔ chin_raise`, `nose_wrinkle ↔ lip_pucker`, `gaze_vertical ↔ brow_raise`.

### Stage 4: Custom Training Extension Development
*Tools:* Python, AI-Toolkit (ostris)
*Outputs:* 4 custom training modules

| Module | Purpose |
|---|---|
| `contrastive_loss.py` | InfoNCE symmetric contrastive loss for confusion pair separation |
| `identity_loss.py` | ArcFace identity preservation during expression editing |
| `multi_channel_conditioning.py` | 28-channel textual latent interpolation at training time |
| `cfed_dataloader.py` | Custom dataloader for CFED images + JSON labels + confusion pairs |

### Stage 5: 3-Phase Adapter Training
*Hardware:* 1× A100 80GB (SPEC-INFRA-001 MIG Partition A or RunPod)
*Outputs:* `conscious_smile_v1.safetensors` (DEP-VIS-008)

| Phase | Channels | Images | Training Time |
|---|---|---|---|
| Phase 1 (Core) | 5: smile, gaze_vertical, brow_raise, brow_furrow, eye_squint | 5,400 + 800 triplets | ~48-72h |
| Phase 2 (Extended) | +11: gaze_horizontal, lip_press, mouth_frown, eye_wide, jaw_open, chin_raise, smirk, lip_bite, wink_left, wink_right, nostril_flare | 11,880 + 600 triplets | ~36-48h |
| Phase 3 (Refinement) | +12: dimpler, head_tilt, lip_pucker, nose_wrinkle, eye_moisture, pout, teeth_clench, tongue_peek, lip_purse, cheek_dimple, crow_feet_activation, micro_contempt | 12,960 + 200 triplets | ~24-36h |

### Stage 6: ComfyUI Integration & Validation
*Tools:* ComfyUI, py-feat, ArcFace, CLIP
*Outputs:* Working inference workflow, named emotion presets, evaluation report

---

## 5. Data Model

### Table: `conscious_smile_channels`

```sql
CREATE TABLE IF NOT EXISTS conscious_smile_channels (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    channel_id VARCHAR(10) NOT NULL UNIQUE,       -- 'CH01'...'CH28'
    channel_name VARCHAR(50) NOT NULL UNIQUE,      -- 'smile_duchenne'
    facs_action_units VARCHAR(50),                 -- 'AU6 + AU12'
    arkit_blendshapes JSONB NOT NULL,              -- ["mouthSmileL", "mouthSmileR", "cheekSquintL", "cheekSquintR"]
    somatic_target TEXT NOT NULL,                   -- 'Zygomaticus + Orbicularis → viewer warmth/trust'
    mood_state_affinity JSONB,                     -- {"Processing": 0.2, "Escape": 0.8, "Discovery": 0.5, "Status": 0.3}
    min_intensity FLOAT DEFAULT 0.0,
    max_intensity FLOAT DEFAULT 1.0,
    training_phase INTEGER NOT NULL,               -- 1, 2, or 3
    confusion_pairs JSONB,                         -- ["CH14_dimpler"]
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'trained', 'validated', 'production')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

ALTER TABLE conscious_smile_channels ENABLE ROW LEVEL SECURITY;
```

### Table: `expression_training_runs`

```sql
CREATE TABLE IF NOT EXISTS expression_training_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    run_id VARCHAR(50) NOT NULL UNIQUE,            -- 'CS-TRAIN-001'
    training_phase INTEGER NOT NULL,               -- 1, 2, or 3
    channels_trained JSONB NOT NULL,               -- ["CH01", "CH02", ...]
    dataset_image_count INTEGER NOT NULL,
    triplet_count INTEGER,
    base_model VARCHAR(100) NOT NULL,              -- 'FLUX 2 Dev FP16'
    lora_rank INTEGER NOT NULL,                    -- 64
    lora_alpha INTEGER NOT NULL,                   -- 128
    learning_rate FLOAT NOT NULL,                  -- 1e-4
    training_steps INTEGER NOT NULL,
    gpu_type VARCHAR(50) NOT NULL,                 -- 'A100-80GB'
    training_hours FLOAT,
    output_file_path TEXT NOT NULL,                 -- '/efs/ccp-models/adapters/conscious_smile_v1.safetensors'
    output_file_size_mb FLOAT,
    eval_channel_accuracy FLOAT,                   -- ≥ 0.85
    eval_identity_preservation FLOAT,              -- ≥ 0.85
    eval_confusion_separation FLOAT,               -- ≥ 0.75
    status VARCHAR(20) DEFAULT 'running' CHECK (status IN ('running', 'completed', 'failed', 'validated')),
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    receipt_chain_block VARCHAR(100)
);

ALTER TABLE expression_training_runs ENABLE ROW LEVEL SECURITY;
```

### Table: `expression_presets`

```sql
CREATE TABLE IF NOT EXISTS expression_presets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    preset_name VARCHAR(50) NOT NULL UNIQUE,        -- 'warm_confidence'
    display_name VARCHAR(100) NOT NULL,             -- 'Warm Confidence'
    channel_values JSONB NOT NULL,                  -- {"smile": 0.6, "eye_squint": 0.4, "brow_raise": 0.1}
    mood_state_affinity VARCHAR(30),                -- 'Escape'
    prompt_string TEXT NOT NULL,                    -- 'expression: smile 0.6, eye_squint 0.4, brow_raise 0.1'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Primary Output Schema: `expression_spec` (embedded in VCB)

```json
{
  "expression_spec": {
    "mode": "preset",
    "preset_name": "warm_confidence",
    "channel_overrides": {
      "smile_duchenne": 0.7
    },
    "adapter_weight": 0.80,
    "adapter_file": "/efs/ccp-models/adapters/conscious_smile_v1.safetensors"
  }
}
```

---

## 6. Backward Compatibility

If a VCB does not contain an `expression_spec` field (legacy pipeline), Paradoxe falls back to prompt-only expression description using prose. A `LEGACY_EXPRESSION_PROMPT_ONLY` warning is logged. The ConsciousSmile adapter is NOT loaded in the ComfyUI workflow for legacy VCBs. This ensures zero disruption to existing visual generation while the adapter is being trained and validated.

---

## 7. Tasks

- [ ] **Task 1:** Create 20 diverse MetaHuman identities in UE5.6 (`CFED_ID_01` through `CFED_ID_20`).
- [ ] **Task 2:** Write Python automation script for UE5 batch rendering (`cfed_render_pipeline.py`).
- [ ] **Task 3:** Render CFED Phase 1 dataset (5 core channels × 20 identities × variations = ~5,400 images).
- [ ] **Task 4:** Generate confusion pair triplets for Phase 1 (~800 triplet sets).
- [ ] **Task 5:** Implement `contrastive_loss.py` (InfoNCE symmetric contrastive loss).
- [ ] **Task 6:** Implement `identity_loss.py` (ArcFace identity preservation wrapper).
- [ ] **Task 7:** Implement `multi_channel_conditioning.py` (28-channel textual interpolation).
- [ ] **Task 8:** Implement `cfed_dataloader.py` (custom dataloader for CFED + confusion pairs).
- [ ] **Task 9:** Train ConsciousSmile Phase 1 adapter on A100 (~48-72h).
- [ ] **Task 10:** Evaluate Phase 1 against metrics (channel accuracy ≥ 0.85, IPS ≥ 0.85).
- [ ] **Task 11:** Train Phase 2 (+11 channels, ~36-48h) and Phase 3 (+12 channels, ~24-36h).
- [ ] **Task 12:** Build ComfyUI inference workflow with adapter + Identity LoRA stacking.
- [ ] **Task 13:** Define and validate 8+ named emotion presets against CCP mood states.
- [ ] **Task 14:** Upload `conscious_smile_v1.safetensors` to EFS at `/efs/ccp-models/adapters/`.
- [ ] **Task 15:** Register DEP-VIS-008 in the dependency registry.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Channel Activation Precision):** Prompt `expression: smile 0.7`. Extract AU12 activation from output using py-feat. Assert extracted value ≈ 0.7 ± 0.15. *Failure:* AU12 reads 0.3 — the adapter ignores the intensity parameter.
- [ ] **AC2 (Channel Isolation):** Activate CH01 (smile) at 0.8. Assert all non-target channels (brow, gaze, jaw) remain < 0.15 AU activation. *Failure:* Activating smile also activates brow_raise at 0.4 — channels are not independent.
- [ ] **AC3 (Confusion Pair Separation):** Generate `smile at α=0.8` and `dimpler at α=0.8`. Assert CLIP cosine similarity < 0.75. *Failure:* Both outputs look identical — the adapter cannot distinguish cheek dimple from full smile.
- [ ] **AC4 (Identity Preservation):** Apply ConsciousSmile with `smile:0.9, brow_furrow:0.5` to Coach Audrey's Identity LoRA. Assert ArcFace cosine similarity ≥ 0.85 between neutral and expression-edited output. *Failure:* Expression editing changes the coach's jawline/cheekbones — adapter is modifying identity, not just expression.
- [ ] **AC5 (LoRA Stacking):** Load Coach Identity LoRA (0.65) + ConsciousSmile (0.80) simultaneously. Generate 10 images. Assert zero burn/artifact/deep-fry on any output. *Failure:* Total weight 1.45 causes image corruption.
- [ ] **AC6 (Monotonic Intensity):** Generate α = {0.2, 0.4, 0.6, 0.8} for `smile`. Assert py-feat AU12 values monotonically increase. *Failure:* α=0.6 produces a stronger smile than α=0.8 — intensity control is non-monotonic.
- [ ] **AC7 (Named Preset):** Apply preset `empathic_concern`. Assert output shows visible brow_furrow + eye_squint + slight smile matching the preset's channel values. *Failure:* Preset produces a neutral face — prompt syntax not recognized by the adapter.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| DEP-VIS-008 (ConsciousSmile Adapter) | Output | Trained adapter `.safetensors` stored on EFS. |
| DEP-VIS-013 (CFED Dataset) | Intermediate | ~28,800 MetaHuman renders + JSON labels. |
| DEP-VIS-011 (Identity LoRA Registry) | Co-loaded | Coach Identity LoRA runs alongside this adapter at inference. |
| DEP-VIS-005 (VCB Schema) | Upstream | VCB `expression_spec` field specifies channel values. |
| FR-VIS-01 (VCB Generation) | Upstream | Abel specifies expression parameters based on mood state. |
| FR-VIS-03 (PSSL Prompt Compilation) | Downstream | Paradoxe compiles expression params into ComfyUI adapter node. |
| FR-VIS-04 (Visual Validation) | Downstream | Validation agent checks expression fidelity post-generation. |
| FR-VIS-17 (Identity LoRA) | Co-dependency | Must be trained first — ConsciousSmile validation requires stacking test. |
| SPEC-INFRA-001 §3.2 | Infrastructure | MIG Partition A (40GB) hosts ComfyUI + FLUX + this adapter. |
| SPEC-INFRA-001 §7.3 | Infrastructure | EFS provides shared adapter weight storage across ComfyUI replicas. |

---

## 10. Testing Strategy

### Unit Tests
- **Channel Prompt Parsing:** Provide expression string `"expression: smile 0.6, brow_furrow 0.3, eye_squint 0.2"`. Assert parser extracts 3 channels with correct values. Assert unmentioned channels default to 0.0.
- **Preset Resolution:** Provide preset name `"warm_confidence"`. Assert resolver returns correct multi-channel vector from database/presets file.
- **Weight Budget Validation:** Provide Identity LoRA weight 0.65 + ConsciousSmile weight 0.80. Assert total ≤ 1.50 threshold passes. Provide 0.90 + 0.80 = 1.70. Assert threshold violation warning is logged.

### Integration Tests
- **End-to-End VCB→Expression:** Submit a VCB with `expression_spec: {preset: "determined_resolve"}` through FR-VIS-03 → ComfyUI. Assert the generated image shows visible brow_furrow + lip_press + eye_squint.
- **EFS Mounting:** Boot a new ComfyUI container on a fresh EC2 instance. Assert it can load `conscious_smile_v1.safetensors` from EFS without downloading or copying.
- **Backward Compatibility:** Submit a legacy VCB without `expression_spec`. Assert Paradoxe falls back to prose description. Assert no adapter node is added to the ComfyUI workflow.

### Safety Tests
- **Expression Injection:** Inject `expression: smile 9999.0` into prompt. Assert adapter clamps to max 1.0, does not crash or produce artifacts.
- **Identity Preservation Under Extreme Expression:** Apply `jaw_drop:1.0, eye_wide:1.0, brow_raise:1.0` simultaneously. Assert ArcFace IPS ≥ 0.80 (relaxed threshold for extreme expressions). Assert the coach is still recognizable.
