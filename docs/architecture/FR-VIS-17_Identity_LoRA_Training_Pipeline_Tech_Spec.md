# Tech-Spec: FR-VIS-17 — Identity LoRA Training Pipeline

**Created:** 2026-03-30
**Status:** Ready for Development
**Version:** 1.0 (Aligned to PRD Visual Control Layer Amendment v1.0)
**Architecture Reference:** PRD §CA10 Visual Control Layer, ADR-08, SPEC-INFRA-001 §7.3 (EFS)
**Skill Implementation:** `skills/visuals/identity_lora_trainer.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

- `docs/prd/prd-update-visual-control-layer.md` — FR-VIS-17 definition, DEP-VIS-011
- `docs/architecture/Infrastructure_AWS_NIM_Deployment_Spec.md` — §7.3 EFS lora directory, §3.2 MIG partition for training
- `docs/other files/active lab archive/ccf_lora_training_methodology.md` — LoRA training methodology research
- `docs/architecture/FR-VIS-14_ConsciousSmile_Expression_Adapter_Tech_Spec.md` — Co-loading: Identity LoRA + ConsciousSmile at inference
- `docs/architecture/FR-VIS-15_ConsciousPose_Body_Language_Library_Tech_Spec.md` — Co-loading: Identity LoRA + ControlNet at inference
- `lab/CCP update/CVE_Documentation_V2.md` — §6 Character Consistency requirements
- `cmf_ai_physics_learning_guide.md` (brain artifact) — LoRA lens physics, weight orthogonality

---

## 2. Overview

### Problem Statement
The CCP's Tier 3 (Realistic AI Character) visual generation requires that every coach's AI-generated likeness is indistinguishable from a real photograph of that coach. Without a trained Identity LoRA, FLUX 2 Dev generates generic faces. Text prompts describing physical appearance ("a 35-year-old man with brown hair, angular jaw, short beard") produce inconsistent faces across generations — the coach looks different in every image. This inconsistency destroys the parasocial bond formation documented in the CVE research, because emotional contagion only triggers when the viewer recognizes a consistent, familiar face. Every coach who onboards the platform requires their own Identity LoRA to lock their facial geometry, skin texture, hair pattern, and body proportions into the generation pipeline.

### Solution
FR-VIS-17 defines the Identity LoRA Training Pipeline — an automated system that takes a coach's submitted reference photos (15-30 images), processes them through a standardized curation pipeline (background removal, caption generation, quality filtering), trains a FLUX 2 Dev LoRA (~2 hours on A100), validates the output against identity preservation metrics, and deploys the `.safetensors` file to EFS where all ComfyUI replicas immediately access it. The pipeline is triggered per-coach during onboarding and produces a single file (`{coach_id}_identity_v1.safetensors`, ~50-80MB) that is loaded at inference time alongside ConsciousSmile (FR-VIS-14).

### Scope
**In scope:**
- Reference photo submission and curation pipeline
- Training configuration (rank, alpha, learning rate, regularization)
- Automated training on AWS (A100 via MIG or RunPod)
- Validation metrics (ArcFace identity score, style flexibility test, expression neutrality test)
- EFS deployment and registry
- Database schema for LoRA registry and training jobs
- Versioning (re-training when coach appearance changes)

**Out of scope:**
- Expression control (FR-VIS-14, ConsciousSmile)
- Body pose control (FR-VIS-15, ConsciousPose)
- First frame composition (FR-VIS-16, FFC)
- Non-coach character generation (generic characters use base FLUX only)

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role |
|---|---|---|
| `DEP-VIS-011` | Identity LoRA Registry | OUTPUT — Per-coach `.safetensors` files on EFS. |
| `DEP-VIS-008` | ConsciousSmile Adapter | CO-LOADED — Expression adapter stacks with Identity LoRA. |
| `DEP-VIS-010` | ConsciousPose Library | CO-LOADED — ControlNet conditions alongside Identity LoRA. |
| `DEP-VIS-014` | Trigger Token Registry | OUTPUT — Per-coach trigger tokens (e.g., `ccp_audrey`). |
| `DEP-ENG-041` | Receipt Chain Guard | AUDIT — Training jobs and deployment hashed. |
| `SPEC-INFRA-001` §3.2 | MIG Partition A | TRAINING — Training runs on 40GB partition. |
| `SPEC-INFRA-001` §7.3 | AWS EFS | DEPLOYMENT — Trained files written to `/efs/ccp-models/loras/`. |

### Academic Grounding

| Framework | Author | Year | Mechanism Applied |
|---|---|---|---|
| **LoRA** | Hu et al. | 2021 | Low-Rank Adaptation of large language models. Applied to FLUX 2 Dev's MMDiT attention layers. Identity LoRA fine-tunes only low-rank matrices (rank 16-32), preserving the base model's generalization while locking the coach's identity. |
| **DreamBooth** | Ruiz et al. | 2022 | Subject-specific fine-tuning with prior preservation. The CCP pipeline uses DreamBooth-style regularization images to prevent language drift — the model learns "ccp_audrey = this specific face" without forgetting what other faces look like. |
| **Emotional Contagion** | Hatfield et al. | 1994 | Identity consistency is a prerequisite for emotional contagion. The viewer must recognize the same face across 50+ content pieces for parasocial bond accumulation. ArcFace similarity ≥ 0.85 is the minimum threshold for reliable cross-content recognition. |

### Technical Decisions

1. **Rank 16-32 (not 64):** Identity LoRAs use lower rank than ConsciousSmile (rank 64) because identity features (face shape, skin texture, hair) have lower intrinsic dimensionality than expression geometry. Lower rank = smaller file = faster loading = less VRAM at inference.
2. **Trigger Token (`ccp_{name}`):** Each coach gets a unique trigger token embedded in the text encoder's vocabulary. This prevents identity leakage — the model only activates Coach A's identity when `ccp_audrey` appears in the prompt.
3. **Weight 0.65 at Inference:** Identity LoRA runs at 0.65 weight, not 1.0, to leave headroom for ConsciousSmile (0.80). The total (1.45) is within FLUX's safe range because the two LoRAs modify orthogonal weight regions.
4. **Automated Retraining:** When a coach submits updated photos (significant appearance change — haircut, weight change, aging), the system trains a `v2` LoRA and retires `v1` after validation.

---

## 4. Implementation Plan

### Stage 1: Reference Photo Submission & Curation
*Inputs:* 15-30 reference photos from coach
*Outputs:* Curated training dataset (12-25 images with captions)

**Photo Requirements (communicated to coach):**
- Minimum 15 photos, recommended 25-30
- Variety: different angles (front, 3/4, profile), different lighting, different expressions
- No heavy filters, no sunglasses covering face, no group photos
- At least 5 close-ups (face/shoulders), at least 3 full-body
- At least 3 different outfits

**Curation Pipeline:**
1. **Background Removal:** BiRefNet or RMBG-2.0 removes backgrounds, replacing with solid color variations.
2. **Auto-Captioning:** Florence-2 or BLIP-2 generates per-image captions describing appearance, pose, clothing (NOT identity — captions never say "Coach Audrey").
3. **Quality Filter:** Remove images with resolution < 512×512, severe motion blur, or face detection confidence < 0.85 (using MediaPipe).
4. **Trigger Token Injection:** Prepend `ccp_{coach_name}` to every caption.

### Stage 2: Training Configuration
*Hardware:* 1× A100 80GB (MIG Partition A or RunPod)
*Duration:* ~1.5-2.5 hours per coach

| Parameter | Value | Notes |
|---|---|---|
| **Base Model** | FLUX 2 Dev (FP16) | Frozen — only LoRA weights trained |
| **LoRA Rank** | 24 | Balance of identity fidelity vs file size |
| **LoRA Alpha** | 48 | Alpha = 2× rank |
| **Target Modules** | MMDiT attention layers | Both text and image streams |
| **Learning Rate** | 4e-4 | With cosine annealing |
| **Batch Size** | 1 | Gradient accumulation: 4 |
| **Training Steps** | 1,500-2,000 | Depends on dataset size |
| **Resolution** | 1024×1024 | FLUX native |
| **Regularization** | 200 class images (generated) | DreamBooth prior preservation |
| **Mixed Precision** | bf16 | Required for FLUX |
| **Optimizer** | AdamW 8-bit | Memory optimization |

### Stage 3: Automated Validation
*Outputs:* Validation report, PASS/FAIL decision

| Metric | Target | How |
|---|---|---|
| **Identity Score (IPS)** | ≥ 0.85 | ArcFace cosine similarity across 10 generated images vs 5 reference photos |
| **Style Flexibility** | ≥ 3/5 pass | Generate coach in 5 different styles (cinematic, editorial, candid, studio, outdoor). All must be recognizable. |
| **Expression Neutrality** | ≤ 0.10 | Generate neutral face. Extract AU values via py-feat. No AU > 0.10 (LoRA should not impose a default expression). |
| **Background Independence** | ≥ 0.85 IPS | Generate coach with 3 completely different backgrounds. IPS must hold across all. |
| **ConsciousSmile Compatibility** | No artifacts | Load Identity LoRA (0.65) + ConsciousSmile (0.80). Generate 5 expressions. No visible artifacts or identity degradation. |

If **any metric fails:** Training is re-run with adjusted learning rate (halved) and additional steps (+500). If 3 re-training attempts fail, the job enters `PENDING_HUMAN_REVIEW`.

### Stage 4: EFS Deployment
*Outputs:* LoRA file on EFS, registry entry

1. Write `{coach_id}_identity_v1.safetensors` to `/efs/ccp-models/loras/`.
2. Update `identity_lora_registry` database table with file path, metrics, version.
3. All running ComfyUI instances see the new file immediately (EFS NFS mount).
4. Write `Receipt_Block_N.json` Cryptographic Hash → Receipt Chain Guard (DEP-ENG-041) documenting training completion.
5. Update the coach's AFFiNE workspace with "Visual Identity: READY" status.

---

## 5. Data Model

### Table: `identity_lora_registry`

```sql
CREATE TABLE IF NOT EXISTS identity_lora_registry (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coach_id UUID NOT NULL,
    lora_version INTEGER NOT NULL DEFAULT 1,
    trigger_token VARCHAR(50) NOT NULL UNIQUE,     -- 'ccp_audrey'
    file_path TEXT NOT NULL,                        -- '/efs/ccp-models/loras/coach_001_identity_v1.safetensors'
    file_size_mb FLOAT,
    lora_rank INTEGER NOT NULL,
    lora_alpha INTEGER NOT NULL,
    training_steps INTEGER NOT NULL,
    reference_photo_count INTEGER NOT NULL,
    identity_score FLOAT NOT NULL,                  -- ArcFace IPS ≥ 0.85
    style_flexibility_score FLOAT,                  -- 3/5 minimum
    expression_neutrality FLOAT,                    -- ≤ 0.10
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

ALTER TABLE identity_lora_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Coach sees own LoRA" ON identity_lora_registry
    FOR SELECT USING (auth.uid() = coach_id);
```

### Table: `identity_lora_training_jobs`

```sql
CREATE TABLE IF NOT EXISTS identity_lora_training_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id VARCHAR(50) NOT NULL UNIQUE,
    coach_id UUID NOT NULL,
    target_version INTEGER NOT NULL,
    reference_photos JSONB NOT NULL,                -- [{"path": "s3://...", "caption": "..."}]
    training_config JSONB NOT NULL,                 -- Full hyperparameter set
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
```

---

## 6. Backward Compatibility

If a coach does not yet have a trained Identity LoRA:
1. FLUX 2 Dev generates without any LoRA — producing a generic face based on the text prompt.
2. The VCB's `identity_lora_path` field is set to `null`.
3. Paradoxe (FR-VIS-03) skips the LoRA loading node in the ComfyUI workflow.
4. Generated content is tagged with `GENERIC_IDENTITY` and flagged for the coach to review.
5. The coach's AFFiNE workspace shows "Visual Identity: PENDING — Upload reference photos to unlock AI likeness."

---

## 7. Tasks

- [ ] **Task 1:** Build reference photo submission UI in AFFiNE (upload block, drag-and-drop, 15-30 photo requirement validation).
- [ ] **Task 2:** Implement photo curation pipeline: BiRefNet background removal → Florence-2 captioning → quality filter → trigger token injection.
- [ ] **Task 3:** Write training configuration builder (`identity_lora_trainer.py`) — generates AI-Toolkit YAML config from coach profile.
- [ ] **Task 4:** Implement automated training execution on A100 (RunPod or MIG Partition A).
- [ ] **Task 5:** Implement 5-metric validation pipeline (ArcFace IPS, style flexibility, expression neutrality, background independence, ConsciousSmile compatibility).
- [ ] **Task 6:** Implement auto-retry logic (halve LR, +500 steps, max 3 attempts).
- [ ] **Task 7:** Implement EFS deployment (write `.safetensors` + update registry + notify AFFiNE).
- [ ] **Task 8:** Implement LoRA versioning (v2 retraining on appearance change, v1 retirement).
- [ ] **Task 9:** Build training dashboard in Global Admin (queue status, GPU utilization, per-coach metrics).
- [ ] **Task 10:** Register DEP-VIS-011 and DEP-VIS-014 in the dependency registry.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Identity Fidelity):** Submit 25 reference photos of a test subject. Train Identity LoRA. Generate 10 images in different poses/scenes. Assert ArcFace IPS ≥ 0.85 for all 10. *Failure:* Generated face looks like a different person — LoRA rank too low or insufficient training steps.
- [ ] **AC2 (Style Flexibility):** Generate the coach in 5 styles: cinematic, editorial, candid, studio, outdoor. Assert the coach is recognizable in all 5 (IPS ≥ 0.85 per style). *Failure:* Coach is only recognizable in studio lighting — LoRA overfit to the training data's lighting distribution.
- [ ] **AC3 (Expression Neutrality):** Generate a neutral face with Identity LoRA loaded. Extract AU values via py-feat. Assert no AU exceeds 0.10. *Failure:* The LoRA imposes a permanent smile (AU12 at 0.4) because all reference photos showed the coach smiling — the LoRA learned "smile" as part of identity.
- [ ] **AC4 (ConsciousSmile Stacking):** Load Identity LoRA (0.65) + ConsciousSmile (0.80). Apply `expression: brow_furrow 0.6, lip_press 0.4`. Assert the expression is visible AND the coach is recognizable (IPS ≥ 0.82). *Failure:* Expression renders correctly but coach's jawline/nose shape changes — weight conflict between LoRAs.
- [ ] **AC5 (EFS Live Deployment):** Complete training and deployment. Assert a running ComfyUI instance can load the new LoRA within 60 seconds without restart. *Failure:* ComfyUI must be restarted to see the new file — EFS cache stale or file lock issue.
- [ ] **AC6 (Versioning):** Submit 5 new reference photos (coach with new haircut). Train v2. Assert v2 reflects new appearance. Assert v1 is marked `retired` in database. Assert all future generations use v2. *Failure:* Pipeline continues loading v1 — registry query not filtering by version.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| DEP-VIS-011 (Identity LoRA Registry) | Output | Per-coach `.safetensors` on EFS. |
| DEP-VIS-014 (Trigger Token Registry) | Output | Unique trigger tokens per coach. |
| DEP-VIS-008 (ConsciousSmile) | Co-loaded | Must validate stacking compatibility. |
| DEP-VIS-010 (ConsciousPose) | Co-loaded | ControlNet conditions alongside LoRA. |
| FR-VIS-03 (Prompt Compilation) | Downstream | Paradoxe loads LoRA node in ComfyUI workflow. |
| FR-VIS-14 (ConsciousSmile) | Co-dependency | Stacking test is part of validation. |
| SPEC-INFRA-001 §3.2 | Infrastructure | MIG Partition A for training. |
| SPEC-INFRA-001 §7.3 | Infrastructure | EFS at `/efs/ccp-models/loras/`. |
| AI-Toolkit (ostris) | External | FLUX LoRA training framework. |
| BiRefNet / RMBG-2.0 | External | Background removal in curation. |
| Florence-2 / BLIP-2 | External | Auto-captioning in curation. |
| ArcFace (InsightFace) | External | Identity verification in validation. |

---

## 10. Testing Strategy

### Unit Tests
- **Curation Pipeline:** Submit 30 photos including 5 with sunglasses, 2 group photos, 3 below 512px. Assert curation removes exactly those 10, outputs 20 clean images with captions + trigger tokens.
- **Trigger Token Uniqueness:** Register 3 coaches with similar names. Assert trigger tokens are unique (e.g., `ccp_audrey`, `ccp_audrey_2`).
- **Config Generation:** For a 25-image dataset, assert training config has 1,750 steps (midpoint of 1,500-2,000 range).

### Integration Tests
- **Full Onboarding Flow:** Upload photos → curation → training → validation → EFS deployment → ComfyUI generation. Assert end-to-end produces a recognizable coach image within 3 hours.
- **Multi-Coach Parallel:** Trigger 3 coach LoRA trainings simultaneously. Assert no VRAM collision (jobs queue if MIG partition is occupied).

### Safety Tests
- **Adversarial Photos:** Submit 15 photos of a public figure (not a coach). Assert training completes but validation flags `IDENTITY_MISMATCH` if the LoRA produces a known public figure's likeness.
- **LoRA Size Limit:** Assert output file size is < 200MB. If training produces a > 200MB file, flag as anomalous (likely rank too high or alpha misconfigured).
