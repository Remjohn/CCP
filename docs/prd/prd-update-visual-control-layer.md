---
stepsCompleted: [1, 2, 3, 4, 5]
parentPRD: d:\Work\The Conscious Coaching Factory\docs\prd\prd.md
updateType: brownfield-capability-upgrade
inputDocuments:
  - d:\Work\The Conscious Coaching Factory\docs\prd\prd.md
  - d:\Work\The Conscious Coaching Factory\lab\CCP update\Mood_State_Architecture_Documentation.docx.md
  - d:\Work\The Conscious Coaching Factory\lab\emotional DNA
  - d:\Work\The Conscious Coaching Factory\lab\CVE + CPSC research papers
  - d:\Work\The Conscious Coaching Factory\lab\Memetic Engine
  - d:\Work\The Conscious Coaching Factory\lab\motion
  - d:\Work\The Conscious Coaching Factory\lab\LoRa papers
  - d:\Work\The Conscious Coaching Factory\lab\CCP update\CCP_Script_Generation_Skill_Type_Guide_v1.0.docx.md
  - d:\Work\The Conscious Coaching Factory\lab\CCP update\JIT_Skill_Compiler_Architecture.docx.md
workflowType: 'prd-update'
lastStep: 5
project_name: 'Conscious Coaching Platform — Visual Control Layer'
user_name: 'Emilio'
date: '2026-03-29T20:30:00+02:00'
capabilityArea: 10
---

# PRD Update — Capability Area 10: Visual Control Layer

## Deterministic Body, Face, and Identity Control for AI-Generated Visual Assets

**Author:** Emilio
**Date:** 2026-03-29T20:30:00+02:00
**PRD Version:** 2.1.0 (Brownfield Upgrade of CA-10 Visual Intelligence Pipeline)
**Parent Document:** `docs/prd/prd.md` (Capability Areas 0–10)
**Extends:** FR-VIS-01 through FR-VIS-13 (Existing Visual Intelligence Pipeline)
**Classification:** STRATEGIC INFRASTRUCTURE — Deterministic Visual Generation Upgrade

---

## 1. Executive Summary

This PRD update introduces the **Visual Control Layer** — a three-component deterministic generation system that upgrades the existing CVE visual pipeline (Capability Area 10) from prompt-only AI generation to **ControlNet-conditioned, expression-controlled, identity-locked generation**. It also introduces the **First Frame Composer** — a new cross-format visual hook composition agent that fills the critical gap of having no dedicated engineering for the most ROI-critical visual in the pipeline: the scroll-stop first frame.

The update adds 4 new functional requirements (FR-VIS-14 through FR-VIS-17), registers 7 new dependency assets (DEP-VIS-008 through DEP-VIS-014), amends 2 existing FRs (FR-VIS-03, FR-VIS-04), introduces 1 new agent, and extends the tool stack with 4 new tools.

### Why Now

The existing CVE pipeline (Abel → Aurore → Paradoxe → RunningHub → Validation → Canva) produces visuals through **prose-only prompts**. Paradoxe translates PSSL parameters into natural language descriptions that RunningHub's AI models interpret non-deterministically. This means:

- **Body language is uncontrolled.** The prompt says "confident stance" — the model decides what that means. Two runs of the same prompt produce different poses. There is no library of validated body language atoms mapped to psychological states.
- **Facial expressions are uncontrolled.** The prompt says "subtle knowing smile" — the model produces a generic smile. There is no FACS-based parametric control. The 28 expression channels documented in the Mood State Architecture have no rendering mechanism.
- **Coach identity drifts.** Reference image strength (0.85) provides approximate identity preservation, but facial features shift across compositions. There is no persistent identity embedding trained on the coach's specific face.
- **No first frame engineering.** Across all content formats (video, carousel, thumbnail, flyer, webinar), no agent in the pipeline owns the composition of the scroll-stop first frame. The most critical visual for engagement is an afterthought — discovered in post-production, never engineered upstream.
- **RunningHub retirement.** The third-party RunningHub API is being replaced by self-hosted **ComfyUI** as the generation backend. ComfyUI is the native runtime for ControlNet + adapter + LoRA workflows — it provides node-level control over every generation parameter, eliminates external API dependencies, and enables custom workflow graphs that RunningHub's abstraction layer could not support.

The Visual Control Layer solves all four problems through three purpose-built systems and one new agent:

| System | Problem Solved | Mechanism |
|:-------|:---------------|:----------|
| **ConsciousSmile** (FR-VIS-14) | Expression uncontrolled | 28-channel FACS adapter trained on CCP-rendered dataset, injected at inference |
| **ConsciousPose** (FR-VIS-15) | Body language uncontrolled | 298-atom composable ControlNet conditioning library, deterministic pose specification |
| **Identity LoRA** (FR-VIS-17) | Coach identity drifts | Per-coach FLUX 2 Dev LoRA from 24-concept datasets, permanent identity lock |
| **First Frame Composer** (FR-VIS-16) | No first frame engineering | Cross-format composition agent, composes scroll-stop frame BEFORE format-specific pipelines |

### What This Changes in the Parent PRD

| Parent PRD Element | Change |
|:---|:---|
| **§1.7 CVE Description** (line 50) | Extended: CVE now includes 3-layer deterministic control (Identity LoRA + ConsciousSmile + ConsciousPose) alongside the 7 immutable design principles. Generation backend migrated from RunningHub to self-hosted ComfyUI. |
| **FR-VIS-03** (Paradoxe PSSL Prompt Compilation) | AMENDED: Paradoxe now compiles ControlNet asset IDs, expression adapter parameters, and Identity LoRA references alongside prose prompts. Generation target changed from RunningHub API to self-hosted ComfyUI workflow execution. |
| **FR-VIS-04** (Visual Validation) | AMENDED: Validation agent gains expression fidelity check (FACS channel comparison) and pose fidelity check (ControlNet map comparison). |
| **DEP-VIS Registry** | Extended with 7 new entries (DEP-VIS-008 through DEP-VIS-014). |
| **DEP-PROTO-007** (Visual Trinity Pipeline) | Extended: Protocol now includes ControlNet conditioning stage between PSSL compilation and ComfyUI workflow submission. RunningHub API retired. |
| **Agent Roster** | Extended with 1 new agent (First Frame Composer). |
| **Tool Stack** | Extended with `conscious_pose_library.py`, `conscious_smile_adapter.py`, `identity_lora_trainer.py`, `first_frame_composer.py`. |
| **Existing Motion Skills** | CAC/GMG Composer SKILL.md files gain CP-ID references for deterministic body language specification. |

---

## 2. Architecture Decision Record — ADR-08: Deterministic Visual Control over Prompt-Only Generation

| | |
|:---|:---|
| **Decision** | Upgrade Tier 3 (Realistic AI Character) generation from prompt-only to ControlNet-conditioned + expression-adapted + identity-locked generation. Migrate generation backend from RunningHub API to self-hosted ComfyUI. |
| **Scope** | Tier 3 only. Tiers 1 (Real Photo), 2 (Stock), and 4 (Ghibli) are unaffected. Ghibli workflows also migrate to ComfyUI. |
| **Why Prompt-Only Fails** | Prose prompts are interpreted non-deterministically by diffusion models. "Confident crossed arms with a knowing smirk" produces different body positions, different arm angles, different facial expressions, and different identity features every run. The PSSL's deterministic precision (lighting, gaze geometry, saturation) is undermined by non-deterministic body and face generation. |
| **Why ComfyUI over RunningHub** | RunningHub is a third-party API abstraction over ComfyUI workflows. The Visual Control Layer requires node-level control (ControlNet conditioning, adapter injection, LoRA loading, multi-model composition) that RunningHub's simplified API cannot expose. Self-hosted ComfyUI on GPU infrastructure (AWS/RunPod) provides: (1) direct node graph control, (2) custom workflow versioning in Git, (3) zero API rate limits, (4) no per-image cost, (5) full ControlNet + adapter + LoRA pipeline support. ComfyUI workflows are JSON-serialized and version-controlled — every visual composition is reproducible. |
| **Why ControlNet** | ControlNet provides spatial conditioning that constrains the diffusion model's output to match a reference body pose, hand position, and depth map — without restricting style, color, or lighting. This makes body language deterministic while preserving PSSL's aesthetic control. The CCP uses open-source models (FLUX 2 Dev) with full ControlNet support, giving us composition control that closed models (DALL-E, Midjourney) cannot replicate. |
| **Why Expression Adapter over LoRA** | An adapter operates in the model's latent space and is dynamically loaded at inference time. A LoRA permanently modifies model weights. The adapter approach allows infinite expression combinations (28 channels with continuous 0.0–1.0 values) without retraining. A LoRA would require a separate model per expression. Decision validated by MCDA: Adapter scored 8.7/10 vs LoRA 5.4/10 on 6 criteria. |
| **Why Identity LoRA** | Unlike expressions (which vary per frame), coach identity is persistent. A LoRA encodes the coach's facial geometry, skin tone, and distinguishing features into the model's weight space. This produces significantly higher identity fidelity than reference image strength (0.85) at inference — the model "knows" the face rather than approximating it from a reference. |
| **Base Model** | FLUX 2 Dev (12B MMDiT). Open-source, ControlNet-compatible, adapter-compatible. |
| **Generation Runtime** | Self-hosted **ComfyUI** on AWS GPU instances (A100/H100) or RunPod serverless. Workflows stored as versioned JSON in Git. API access via ComfyUI's REST API (`/prompt`, `/history`, `/view`). |
| **Rendering Pipeline** | ControlNet maps generated via iClone 8 Python API (body poses) and Unreal Engine 5.6 MetaHuman (face expressions). Both are offline rendering — maps are pre-generated and indexed by CP-ID. |
| **Trade-off Accepted** | Upfront rendering cost: ~300 ControlNet maps (iClone), ~30,000 expression images (MetaHuman), ~40h A100 for adapter training. Self-hosted GPU cost replaces per-image RunningHub API cost. Per-inference cost is < 2s additional latency per image. |

---

## 3. Functional Requirements — Visual Control Layer

### 3.1 Expression Control

- **FR-VIS-14 (ConsciousSmile — Expression Adapter):** The system provides deterministic facial expression control for all Tier 3 AI-generated visual assets via a latent-space adapter (ConsciousSmile) trained on a CCP-specific expression dataset (CFED). The adapter supports 28 independently controllable FACS-based expression channels, each accepting continuous values from 0.0 to 1.0. **Channels:** `smile_duchenne`, `smile_social`, `smile_suppressed`, `smirk`, `lip_bite`, `lip_press`, `lip_purse`, `pout`, `mouth_open_awe`, `teeth_clench`, `tongue_peek`, `brow_raise_surprise`, `brow_furrow`, `brow_knit_concern`, `eye_squint_genuine`, `eye_wide`, `eye_roll`, `wink_left`, `wink_right`, `nostril_flare`, `chin_raise`, `jaw_drop`, `neck_tension`, `cheek_dimple`, `crow_feet_activation`, `nasolabial_deepen`, `forehead_wrinkle`, `micro_contempt`. Each channel maps to specific FACS Action Units (AUs) and has a documented psychological function in the Mood State Architecture. The adapter is loaded dynamically at inference time within the ComfyUI workflow alongside the Identity LoRA — it does not modify base model weights. Expression parameters are specified in the `expression_spec` field of the Visual Composition Brief (VCB), compiled by Abel (FR-VIS-01) based on the Psychological Routing Brief's mood state and core emotion. **Training Pipeline:** The CFED (Conscious Face Expression Dataset) is rendered using Unreal Engine 5.6 MetaHuman with parametric AU control across 5 identity-diverse base faces × 28 channels × ~200 intensity/combination variations = ~30,000 labeled images. Training uses the PixelSmile symmetric contrastive loss architecture on FLUX 2 Dev for ~40 hours on a single A100 GPU. The trained adapter is registered as DEP-VIS-008. *(Source: Mood State Architecture, Emotional Contagion Research, PixelSmile Architecture)*

### 3.2 Body Language Control

- **FR-VIS-15 (ConsciousPose — Body Language Library):** The system provides deterministic body language control for all Tier 3 AI-generated visual assets via a composable library of 298 pre-rendered ControlNet conditioning maps (ConsciousPose). The library is organized into 7 catalogs: **Body** (83 atoms: standing, sitting, leaning, lying, crouching, dynamic action, intimate, gendered, editorial), **Hands** (55 atoms: open palm, pointing, gesturing, holding prop, emotional hands, sensual hands, cultural hands), **Gaze** (35 atoms: direct, averted, upward, downward, sideways, multi-target, intimate/provocative), **Scene** (36 atoms: solo centered, rule-of-thirds, environmental integration, multi-character, elevated, compressed), **Mood Visual** (30 atoms: isolated, crowded, natural, urban, intimate, ethereal, 6 per mood state), **Props** (30 atoms: beverage, device, book, wearable, environmental, symbolic), **Multi-Character** (29 atoms: mirroring, contrast, power dynamic, intimate, group, triangular, solo-with-crowd). Each atom is assigned a unique **CP-ID** (e.g., `CP-B-001` for Catalog-Body atom 001) and rendered as both a depth map and an OpenPose skeleton via **iClone 8 Python API** (`Pose_Manager`, `HandGesturesPuppeteering`, `JointDrivenMorph`). Atoms are **composable** — a single visual composition specifies one atom per layer (body + hands + gaze + scene + mood + props + multi-char), and the runtime composition engine assembles them into a single ControlNet conditioning map. **Mood State Routing:** Each CP-ID is tagged with compatible mood states from the 4-state architecture (Processing, Escape, Discovery, Status). The composition engine filters available atoms by the Psychological Routing Brief's current mood state, ensuring body language is psychologically aligned. The complete library index is registered as DEP-VIS-009; rendered ControlNet maps are archived as DEP-VIS-010. *(Source: ConsciousPose Composition Schema, iClone Open API Documentation)*

### 3.3 First Frame Engineering

- **FR-VIS-16 (First Frame Composer):** The system provides a dedicated cross-format visual hook composition agent (First Frame Composer, FFC) that engineers the scroll-stop first frame for all visual content formats: video (Reel/TikTok/YouTube), carousel cover, thumbnail, flyer, story, poll/quiz visual, webinar cover, and email header. The FFC operates **upstream** of all format-specific composition agents (CAC Composer, GMG Composer, Carousel Builder, Thumbnail Renderer). It consumes the Beat Cluster (`beat_cluster.json`), Compressed Anchor (`compressed_anchor.txt`), Psychological Routing Brief (`DEP-ENG-016`), output format, and CBCS tier. It produces a `first_frame_spec.json` (registered as DEP-VIS-012) that deterministically specifies: body pose (CP-ID from ConsciousPose), hand gesture (CP-ID), gaze vector (CP-ID), expression parameters (28-channel ConsciousSmile values), scene composition (CP-ID), text overlay (headline, position, font treatment), ControlNet asset references, Identity LoRA reference, and a reasoning block documenting the psychological rationale for each choice. **Composition Decision Engine (6 steps):** (1) Format constraints → aspect ratio, face position zone; (2) Mood State → visual energy via mood visual CP-IDs; (3) CBCS tier → gaze vector selection (cold: provocative or averted, warm: near-direct, hot: confident direct); (4) Text hook → psychological mechanism from VCP + core emotion + regulatory frame; (5) Expression → ConsciousSmile channel preset matching mood + emotion + memetic intent; (6) Compose and validate all CP-IDs exist in library. **Format Routing:** Video → CAC/GMG receives `first_frame_spec` as Frame 1 constraint; Carousel → Carousel Builder receives cover spec; Thumbnail → direct ControlNet generation; Flyer/Webinar/Poll → format-specific renderers. **Anti-Draft Architecture (2 levels):** Level 1 — Stock Thumbnail Anti-Draft (generic coaching visual description); Level 2 — Format-Specific Anti-Draft (per-format banality trap). The FFC ensures the most ROI-critical visual in the pipeline is engineered FIRST, not discovered in post-production. *(Source: First Frame Composer Architecture, Visual Hooks MCDA Audit, BVT Research)*

### 3.4 Identity Persistence

- **FR-VIS-17 (Identity LoRA — Per-Coach Identity Embedding):** The system provides deterministic facial identity persistence for all Tier 3 AI-generated visual assets via a per-coach Identity LoRA trained on FLUX 2 Dev. Each coach's LoRA is trained on a **24-concept dataset** covering: 6 lighting conditions (natural daylight, golden hour, studio, overcast, indoor ambient, dramatic), 4 angles (front, 3/4, profile, slight low-angle), and variation across expressions, clothing, and environments to prevent style collapse. Dataset construction follows strict regularization: class images use matching demographic base images to prevent identity leakage from regularization set. Training parameters: rank 16, learning rate 1e-4, 1500 steps on a single A100 GPU (~2 hours per coach). The trained LoRA is loaded alongside ConsciousSmile adapter at inference — LoRA controls identity (fixed), adapter controls expression (variable). LoRA weights are stored in the Identity LoRA Registry (DEP-VIS-011) indexed by `coach_id`. The 24-concept source dataset is stored as DEP-VIS-014. *(Source: CCF LoRA Training Methodology, 24 LoRA Concepts Visual Pipeline)*

---

## 4. Amendments to Existing Functional Requirements

### FR-VIS-03 Amendment (PSSL Prompt Compilation)

**What changes:** Paradoxe (PSSL Prompt Compiler) now compiles ControlNet asset IDs, expression adapter parameters, and Identity LoRA references alongside prose prompts for all Tier 3 slides. The generation target is migrated from RunningHub API to self-hosted ComfyUI. The ComfyUI workflow payload gains 3 new node entries. All existing Paradoxe compilation operations (field-to-prompt translation, anti-generic constraints, gaze geometry, cultural color, reference image, imperfection spec) remain unchanged — only the submission target changes.

**New compilation operations (added to the existing 6):**

7. **ControlNet Map Assembly:** For each Tier 3 slide, Paradoxe reads the VCB's `body_pose_id`, `hand_gesture_id`, `gaze_vector_id`, and `scene_composition_id`, resolves them against the ConsciousPose Library Index (DEP-VIS-009), and assembles the composite ControlNet conditioning map reference (depth + OpenPose) for the RunningHub payload.

8. **Expression Adapter Parameter Assembly:** Paradoxe reads the VCB's `expression_spec` (28 floating-point values from FR-VIS-14) and compiles them into the expression adapter node parameters. Adapter weights are loaded from DEP-VIS-008 (ConsciousSmile Adapter Weights).

9. **Identity LoRA Reference Assembly:** Paradoxe reads the `coach_id` from the Psychological Routing Brief, queries the Identity LoRA Registry (DEP-VIS-011) for the coach's trained LoRA file path, and compiles it into the LoRA node.

10. **ComfyUI Workflow Submission:** Paradoxe submits the assembled workflow JSON to the self-hosted ComfyUI instance via its REST API (`POST /prompt`). Polling uses `GET /history/{prompt_id}` with exponential backoff (5s → 60s max, 10-minute timeout). On completion, generated images are retrieved via `GET /view` and passed to the Visual Validation Agent. This replaces the former RunningHub task submission and polling protocol.

**ComfyUI Workflow Payload (3 new nodes added to existing workflow graph):**

```json
{
  "workflow": "workflows/tier3_controlnet_expression_v1.json",
  "client_id": "paradoxe_compiler",
  "prompt": {
    // ... existing KSampler, CLIP, VAE, checkpoint loader nodes ...
    {
      "nodeId": "controlnet_depth_node",
      "fieldName": "image",
      "fieldValue": "{controlnet_depth_map_path}"
    },
    {
      "nodeId": "controlnet_openpose_node",
      "fieldName": "image",
      "fieldValue": "{controlnet_openpose_map_path}"
    },
    {
      "nodeId": "expression_adapter_node",
      "fieldName": "weights",
      "fieldValue": "{expression_channel_values_json}"
    },
    {
      "nodeId": "expression_adapter_model_node",
      "fieldName": "model_path",
      "fieldValue": "{conscious_smile_adapter_path}"
    },
    {
      "nodeId": "identity_lora_node",
      "fieldName": "lora_name",
      "fieldValue": "{coach_identity_lora_path}"
    }
  }
}
```

**Backward Compatibility:** If a VCB does not contain `body_pose_id` or `expression_spec` (legacy pipeline version), Paradoxe falls back to prompt-only compilation using the simplified ComfyUI workflow (no ControlNet/adapter nodes). A `LEGACY_PROMPT_ONLY` warning is logged. For any remaining RunningHub-dependent workflows during migration, Paradoxe maintains the legacy RunningHub submission path until full ComfyUI migration is complete.

### FR-VIS-04 Amendment (Visual Validation)

**What changes:** The Visual Validation Agent gains 2 new validation checks for ControlNet-conditioned generation.

**New checks (added to the existing 3):**

4. **Expression Fidelity Check:** For slides generated with ConsciousSmile parameters, the validation agent compares the generated face's detected FACS AU activations (via face analysis model) against the specified expression channels. Deviation threshold: ≤ 15% per channel. Channels with deviation > 15% are flagged. On failure: Paradoxe resubmits with increased adapter strength (from 0.7 to 0.85). On second failure: `PENDING_HUMAN_REVIEW`.

5. **Pose Fidelity Check:** For slides generated with ControlNet conditioning, the validation agent extracts an OpenPose skeleton from the generated image and compares it against the source ControlNet map. Deviation threshold: ≤ 10° per major joint. On failure: regeneration with increased ControlNet strength (from 0.8 to 0.95). On second failure: `PENDING_HUMAN_REVIEW`.

---

## 5. New Dependency Registry Entries

| DEP-ID | Name | Format | Purpose |
|:-------|:-----|:-------|:--------|
| DEP-VIS-008 | ConsciousSmile Adapter Weights | `.safetensors` | Trained expression adapter for FLUX 2 Dev. 28-channel FACS control. Loaded dynamically at inference. |
| DEP-VIS-009 | ConsciousPose Library Index | JSON | Master index of 298 composable pose atoms with CP-IDs, catalog membership, mood state compatibility tags, and ControlNet map file references. |
| DEP-VIS-010 | ControlNet Conditioning Map Archive | PNG (Depth + OpenPose) | Pre-rendered ControlNet maps for all 298 ConsciousPose atoms. ~600 files (2 maps per atom). Generated via iClone 8 Python API. |
| DEP-VIS-011 | Identity LoRA Registry | JSON + `.safetensors` | Index of per-coach Identity LoRA files. Maps `coach_id` → LoRA file path + training metadata (date, concept count, training steps). |
| DEP-VIS-012 | First Frame Specification Schema | JSON | Output schema for the First Frame Composer. Contains composed CP-IDs, expression parameters, text overlay spec, ControlNet references, and reasoning block. |
| DEP-VIS-013 | CFED Training Dataset | PNG + JSON labels | Conscious Face Expression Dataset. ~30,000 MetaHuman-rendered face images with per-image FACS AU labels. Used to train DEP-VIS-008. |
| DEP-VIS-014 | Coach Identity Dataset (24-Concept) | PNG + metadata | Per-coach photo datasets (24 images per coach) used to train Identity LoRAs. Stored per `coach_id`. |

---

## 6. New Agent

| Agent | Department | Mandate |
|:------|:-----------|:--------|
| `Iris` (First Frame Composer) | Visual | Composes the scroll-stop first frame for all content formats. Queries ConsciousPose library + ConsciousSmile channels based on Psychological Routing Brief. Produces `first_frame_spec.json` consumed by downstream format-specific agents (CAC, GMG, Carousel Builder, Thumbnail Renderer). Operates upstream of all visual composition agents. |

**Updated Agent Count:** 83 → **84 named agents** across 6 departments.

---

## 7. New Tool Stack

| Tool | Purpose |
|:-----|:--------|
| `conscious_pose_library.py` | ConsciousPose Library management. Index query, CP-ID resolution, mood state filtering, composition assembly (multi-layer → single ControlNet map). |
| `conscious_smile_adapter.py` | ConsciousSmile adapter inference interface. Accepts 28 channel values, loads adapter weights, injects into FLUX 2 Dev inference pipeline. |
| `identity_lora_trainer.py` | Per-coach Identity LoRA training pipeline. Accepts 24-concept dataset, runs FLUX 2 Dev LoRA training, registers output in DEP-VIS-011. |
| `first_frame_composer.py` | First Frame Composer agent logic. 6-step composition decision engine, `first_frame_spec.json` output, format-specific routing. |

---

## 8. New Data Infrastructure

| Table | Primary Key | Purpose |
|:------|:------------|:--------|
| `conscious_pose_atoms` | `cp_id` (String) | Master registry of all 298 pose atoms. Fields: `catalog` (body/hands/gaze/scene/mood/props/multi), `name`, `description`, `mood_states` (JSONB array), `depth_map_path`, `openpose_map_path`, `iclone_preset_path`, `created_at`. |
| `conscious_smile_channels` | `channel_id` (String) | Registry of 28 expression channels. Fields: `name`, `facs_aus` (JSONB array of AU codes), `psychological_function`, `min_value`, `max_value`, `default_value`. |
| `identity_lora_registry` | `coach_id` (UUID) | Per-coach Identity LoRA tracking. Fields: `lora_file_path`, `concept_count`, `training_steps`, `base_model`, `trained_at`, `dataset_path`, `quality_score`. |
| `first_frame_specs` | `spec_id` (UUID) | Produced first frame specifications. Fields: `beat_cluster_id`, `output_format`, `body_cp_id`, `hands_cp_id`, `gaze_cp_id`, `expression_spec` (JSONB, 28 channels), `text_overlay` (JSONB), `reasoning` (JSONB), `created_at`. |
| `expression_training_runs` | `run_id` (UUID) | CFED training run tracking. Fields: `dataset_version`, `training_hours`, `loss_final`, `channels_active`, `base_model`, `adapter_path`, `completed_at`. |

---

## 9. Non-Functional Requirements Extension

### Performance

| Context | Requirement | Rationale |
|:--------|:------------|:----------|
| ControlNet conditioning injection | Additional latency per Tier 3 image: **< 2 seconds** | Depth + OpenPose map loading is file I/O, not compute-heavy. |
| Expression adapter inference | Additional latency per Tier 3 image: **< 1 second** | Adapter operates in latent space, minimal compute overhead. |
| Identity LoRA loading | LoRA swap per coach: **< 3 seconds** | LoRA weights are small (~50MB). Cached in GPU VRAM per session. |
| First Frame Composer decision | Composition decision: **< 5 seconds** | 6-step tree traversal against indexed library. No generation, only query. |
| iClone ControlNet map rendering | Per-atom rendering: **< 30 seconds** | Offline. One-time batch job for library construction. |
| MetaHuman expression rendering | Per-image rendering: **< 10 seconds** | Offline. One-time batch job for CFED dataset. |
| Identity LoRA training | Per-coach training: **< 3 hours** on single A100 | One-time per coach onboarding. |

### Reliability

- **ControlNet Map Integrity:** All CP-ID references in a `first_frame_spec.json` must resolve to existing files in DEP-VIS-010. The First Frame Composer validates all references before emitting. Missing map = `CP_ID_NOT_FOUND` error, FFC falls back to prompt-only for that layer.
- **Adapter Versioning:** ConsciousSmile adapter weights (DEP-VIS-008) are versioned. All VCBs record the adapter version used. If the adapter is retrained, historical VCBs can be reproduced with the original adapter version.
- **LoRA Registry Consistency:** Identity LoRA registry entries are immutable once created. Re-training a coach's LoRA creates a new version entry, not an overwrite.

---

## 10. Risk Mitigation Matrix Extension

| Risk | Description | Mitigation |
|:-----|:------------|:-----------|
| **ControlNet Quality on FLUX 2** | ControlNet conditioning may produce artifacts on MMDiT architecture | FLUX 2 Dev has validated ControlNet support. Test with first 10 atoms before full library render. Fallback: prompt-only with reference image (existing behavior). |
| **Expression Adapter Underfitting** | 28 channels may be too many for adapter to learn discriminatively | Phased training: start with 12 core channels, validate, then expand to 28. Core 12 cover the most psychologically impactful expressions. |
| **Identity LoRA Style Collapse** | Coach LoRA overfits to training photos, restricting style diversity | 24-concept dataset ensures variety across lighting, angle, expression, clothing. Regularization with demographic-matched class images. Training step limit prevents memorization. |
| **iClone API Limitations** | iClone Python API may not support all required joint manipulations | Validated against iClone 8 Open API documentation. `Pose_Manager`, `HandGesturesPuppeteering`, `JointDrivenMorph` cover all 298 atoms. Fallback: manual posing in iClone GUI for edge cases. |
| **Large Asset Storage** | 600 ControlNet maps + 30,000 CFED images = significant storage | ControlNet maps: ~2GB total (600 × ~3MB PNG). CFED: ~60GB (30K × ~2MB). Stored on S3 with CDN caching for inference. One-time storage cost. |
| **First Frame Agent Overfit** | FFC produces repetitive first frames across similar mood states | Anti-repetition via Fingerprint Archive query: FFC checks the last 30 days of `first_frame_specs` for the same coach and avoids re-using the same CP-ID combinations. |

---

## 11. Phased Build Sequence

### Phase 0: Asset Rendering Infrastructure (Weeks 1-3)

| Step | What Gets Built | Depends On |
|:-----|:----------------|:-----------|
| VCL-01 | UE5 MetaHuman scripting for CFED dataset — 28-channel AU control, 5 base faces, lighting variation | Nothing |
| VCL-02 | iClone Python API automation — batch ControlNet map rendering from pose presets | Nothing |
| VCL-03 | CFED dataset generation — ~30,000 labeled expression images | VCL-01 |
| VCL-04 | ConsciousPose library rendering — 298 atoms × 2 maps (depth + openpose) = 600 files | VCL-02 |
| VCL-05 | `conscious_pose_atoms` Supabase table + CP-ID index (DEP-VIS-009) | VCL-04 |

### Phase 1: Model Training (Weeks 4-6)

| Step | What Gets Built | Depends On |
|:-----|:----------------|:-----------|
| VCL-06 | ConsciousSmile adapter training — PixelSmile architecture on CFED, ~40h A100 | VCL-03 |
| VCL-07 | First coach Identity LoRA — 24-concept dataset collection + training (~2h A100) | Nothing |
| VCL-08 | Adapter validation — test all 28 channels for discriminative control | VCL-06 |
| VCL-09 | LoRA validation — test identity consistency across 50 varied compositions | VCL-07 |

### Phase 2: Pipeline Integration (Weeks 7-9)

| Step | What Gets Built | Depends On |
|:-----|:----------------|:-----------|
| VCL-10 | `conscious_pose_library.py` — library query, composition assembly, CP-ID validation | VCL-05 |
| VCL-11 | `conscious_smile_adapter.py` — inference interface for 28 channels | VCL-06 |
| VCL-12 | `identity_lora_trainer.py` — per-coach training pipeline + DEP-VIS-011 registry | VCL-07 |
| VCL-13 | ComfyUI workflow — ControlNet + adapter + LoRA integrated generation | VCL-10 + VCL-11 + VCL-12 |
| VCL-14 | FR-VIS-03 amendment — Paradoxe gains ControlNet/adapter/LoRA compilation | VCL-13 |
| VCL-15 | FR-VIS-04 amendment — Validation agent gains expression + pose fidelity checks | VCL-14 |

### Phase 3: First Frame Composer (Weeks 10-12)

| Step | What Gets Built | Depends On |
|:-----|:----------------|:-----------|
| VCL-16 | `first_frame_composer.py` — 6-step composition decision engine | VCL-10 + VCL-11 |
| VCL-17 | First Frame Composer SKILL.md — full JIT-compatible skill specification | VCL-16 |
| VCL-18 | Integration with CAC/GMG — first_frame_spec as Frame 1 constraint | VCL-17 |
| VCL-19 | Integration with Carousel/Thumbnail — cover/hero spec routing | VCL-17 |
| VCL-20 | `first_frame_specs` table + Fingerprint Archive anti-repetition query | VCL-16 |

### Phase 4: Motion Skill Upgrade (Weeks 13-14)

| Step | What Gets Built | Depends On |
|:-----|:----------------|:-----------|
| VCL-21 | CAC Composer SKILL.md upgrade — body language via CP-IDs instead of prose | VCL-10 + VCL-18 |
| VCL-22 | GMG Composer SKILL.md upgrade — pose reference via CP-IDs | VCL-10 + VCL-18 |
| VCL-23 | GMG Expert 01-06 audit — validate ControlNet compatibility with all motion styles | VCL-21 + VCL-22 |

---

## 12. Files Made Obsolete

| File | Disposition | Replacement |
|:-----|:------------|:------------|
| `🟨 VISUAL HOOKS RECIPES 🟨.md` | ARCHIVE to `lab/archive/` | ConsciousPose library (DEP-VIS-009) + First Frame Composer (FR-VIS-16) |
| `✨ ADVANCED CONTENT HOOK GENERATION PROMPT.md` | ARCHIVE to `lab/archive/` | First Frame Composer (FR-VIS-16) — 100% obsolete: no CVE, no Mood State, no FACS, no ControlNet, no anti-draft, no DEP-IDs |
| Legacy pose files (6 files in `lab/`, ~240 generic poses) | ARCHIVE to `lab/archive/` | ConsciousPose production library (298 composable atoms with CP-IDs) |

---

## 13. Success Criteria Extension

| Criterion | Target | Measurement |
|:----------|:-------|:------------|
| **Expression Control Fidelity** | ≥85% of generated faces match specified FACS channels within 15% deviation | Expression Fidelity Check pass rate in Visual Validation Agent |
| **Pose Control Fidelity** | ≥90% of generated bodies match ControlNet conditioning within 10° joint deviation | Pose Fidelity Check pass rate in Visual Validation Agent |
| **Identity Consistency** | ≥95% of generated faces recognized as same identity across 50 varied compositions | Character Drift Detection improvement over reference-image-only baseline |
| **First Frame CTR Uplift** | ≥15% improvement in carousel cover and thumbnail CTR vs. non-FFC baseline | Social Performance Registry (DEP-VIS via FR-CA11-18) A/B comparison |
| **Generation Determinism** | Same VCB inputs produce visually consistent outputs across 5 runs (SSIM ≥ 0.85) | Automated consistency test in CI pipeline |
| **Library Coverage** | 100% of visual hooks in the MCDA audit (38 hooks) can be composed from ConsciousPose atoms | Manual composition verification against `visual_hooks_mcda_audit.md` |

---

*End of PRD Update — Visual Control Layer. This document extends the parent PRD (v1.0, Capability Areas 0–10) and should be read as an addendum to Capability Area 10. All FRs, ADRs, and architectural mandates from the parent PRD remain in force unless explicitly amended above.*
