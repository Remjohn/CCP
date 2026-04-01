# Tech-Spec: FR-VIS-15 — ConsciousPose Body Language Library

**Created:** 2026-03-30
**Status:** Ready for Development
**Version:** 1.0 (Aligned to PRD Visual Control Layer Amendment v1.0)
**Architecture Reference:** PRD §CA10 Visual Control Layer, ADR-08, SPEC-INFRA-001 §7.3 (EFS)
**Skill Implementation:** `skills/visuals/conscious_pose_resolver.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

- `docs/prd/prd-update-visual-control-layer.md` — FR-VIS-15 definition, DEP-VIS-010
- `docs/architecture/Infrastructure_AWS_NIM_Deployment_Spec.md` — §7.3 EFS directory structure for ControlNet maps
- `docs/other files/active lab archive/conscious_pose_production_library.md` — 168-atom production catalog (9 catalogs: Body, Hands, Gaze, Scene, Mood Visual, Props, Multi-Character, Memetic recipes, Archetype recipes)
- `docs/other files/active lab archive/conscious_pose_expansion_library.md` — 130-atom expansion catalog (ASFW, romantic, masculine/feminine)
- `lab/CVE + CPSC research papers/Gaze Cueing in Design Framework.md` — Gaze geometry vectors
- `lab/CVE + CPSC research papers/Physiological State Specification Language.md` — PSSL body language mapping
- `docs/architecture/FR-VIS-01_Visual_Composition_Brief_Tech_Spec.md` — VCB schema consuming pose specifications
- `docs/architecture/FR-VIS-14_ConsciousSmile_Expression_Adapter_Tech_Spec.md` — Co-dependency: expression + pose compose the full character

---

## 2. Overview

### Problem Statement
The CCP's visual pipeline currently specifies body language through prose descriptions embedded in text prompts — "standing confidently with arms crossed" or "leaning forward engagingly." This approach produces inconsistent, non-reproducible, and non-composable results. The same text prompt generates wildly different poses across seeds and even across identical generation runs. When ControlNet is not conditioned with explicit depth/openpose maps, FLUX 2 Dev defaults to its training distribution — producing generic stock-photo poses that fail to trigger the specific mirror neuron responses documented in the CVE research. Coaches cannot be reliably depicted in the precisely engineered body language positions that match their content's psychological intent.

### Solution
FR-VIS-15 defines the ConsciousPose library — a deterministic, composable body language control system that replaces prose-based pose descriptions with explicit ControlNet conditioning maps (depth + openpose). The library catalogues 298 composable atoms organized into 9 layers: Body Positions (36), Hand/Finger Gestures (36), Gaze Compositions (24), Scene/Camera (24), Mood Visual / Lighting (24), Props (24), Multi-Character (12), plus cross-referenced Memetic Engine recipes (14) and Archetype default recipes (7 families). Each atom has a unique `CP-ID` that can be composed into a full-body specification. ControlNet maps are rendered from iClone/MetaHuman 3D rigs and stored on AWS EFS for instant mounting by all ComfyUI replicas.

### Scope
**In scope:**
- CP-ID taxonomy (9 catalogs, 298 atoms)
- Composition schema (how atoms from different layers combine)
- ControlNet map rendering pipeline (iClone Python API → depth/openpose/normal exports)
- EFS storage and manifest system
- Database schema for atom registry, compositions, and asset tracking
- Abel (FR-VIS-01) integration: VCB `pose_spec` field
- Paradoxe (FR-VIS-03) integration: ControlNet node injection in ComfyUI workflow

**Out of scope:**
- Facial expression control (handled by FR-VIS-14, ConsciousSmile)
- Identity LoRA training (handled by FR-VIS-17)
- First Frame composition decisions (handled by FR-VIS-16)
- Pose animation / video motion (handled by motion skills in CA10)

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-VIS-010` | ConsciousPose ControlNet Map Library | OUTPUT — Rendered depth/openpose PNGs stored on EFS. |
| `DEP-VIS-005` | Visual Composition Brief Schema | UPSTREAM — VCB `pose_spec` field specifies CP-IDs. |
| `DEP-VIS-008` | ConsciousSmile Adapter | CO-LOADED — Expression adapter stacks alongside ControlNet conditioning. |
| `DEP-VIS-011` | Identity LoRA Registry | CO-LOADED — Coach identity + pose + expression = complete character. |
| `DEP-ENG-016` | Psychological Routing Brief | UPSTREAM — Mood state determines default pose recipe. |
| `DEP-ENG-041` | Receipt Chain Guard | AUDIT — Composition selections and asset references hashed. |
| `SPEC-INFRA-001` §3.2 | MIG Partition A (40GB) | RUNTIME — ControlNet maps loaded into VRAM alongside FLUX. |
| `SPEC-INFRA-001` §7.3 | AWS EFS Model Store | STORAGE — Maps mounted at `/efs/ccp-models/controlnet/`. |

### Academic Grounding

| Framework | Author | Year | Mechanism Applied |
|---|---|---|---|
| **Mirror Neuron System** | Rizzolatti & Craighero | 2004 | Observed body positions activate the same motor cortex regions in the viewer. A power pose (CP-B-004) triggers sympathetic arousal; a vulnerability pose (CP-B-017) activates the default mode network. ControlNet guarantees the exact body position, not an approximation. |
| **Gaze Cueing Effect** | Friesen & Kingstone | 1998 | Viewer attention reflexively follows the observed subject's gaze direction within 18.2ms. CP-G-001 through CP-G-024 provide deterministic gaze vectors that Abel maps to VCB engagement zones. |
| **Benign Violation Theory (BVT)** | McGraw & Warren | 2010 | Humor requires simultaneous violation and benignness. The Memetic Engine atoms (CP-B-031 through CP-B-036) provide the visual violation signal while body warmth signals provide benignness. |
| **Environmental Psychology** | Kaplan & Kaplan | 1989 | Scene context (CP-S-013 through CP-S-018) triggers cognitive frameworks that bias interpretation. Office = credibility, outdoor = freedom, home = trust. ControlNet scene compositions lock the environmental context. |

### Technical Decisions

1. **ControlNet over Pose-in-Prompt:** Text prompts cannot reliably specify 36 distinct body positions × 36 hand gestures × 24 gaze directions. ControlNet depth/openpose maps provide pixel-level spatial conditioning that is seed-invariant and fully reproducible.
2. **Composable Layers over Monolithic Poses:** Instead of rendering 36 × 36 × 24 = 31,104 pre-composed ControlNet maps (storage: ~94GB), the system composes maps at request time from layered renders. Body + hands compose in the depth domain; gaze composes in the expression domain (FR-VIS-14).
3. **iClone over Blender:** iClone's Python API provides direct bone manipulation with inverse kinematics, enabling programmatic pose authoring for all 298 atoms. Blender requires manual rigging per character mesh.
4. **EFS over S3:** ControlNet maps must be immediately available to ComfyUI without download latency. EFS NFS mounts provide filesystem-level access. S3 would require a download step on each generation request.

---

## 4. Implementation Plan

### Stage 1: Atom Registry Population
*Inputs:* ConsciousPose Production Library catalog (168 atoms) + Expansion Library (130 atoms)
*Outputs:* Populated `conscious_pose_atoms` database table (298 rows)

**Steps:**
1. Parse both library catalogs into structured JSON.
2. For each atom: create database record with `cp_id`, `layer`, `subcategory`, `position_name`, `signal`, `mood_fit`, `archetype_fit`, `mirror_neuron_target`.
3. Register all Memetic Engine composition recipes as `conscious_pose_compositions`.
4. Register all Archetype default recipes as `conscious_pose_compositions`.

### Stage 2: 3D Rig Setup (iClone)
*Tools:* iClone 8, Character Creator 4, Python API
*Inputs:* None (greenfield)
*Outputs:* Base rig template with standardized bone naming

**Steps:**
1. Import a neutral humanoid mesh into iClone.
2. Configure bone hierarchy matching the ARKit/ControlNet OpenPose 18-keypoint format.
3. Set up Python automation for batch pose rendering:
   - Camera positions matching all 24 CP-S scene compositions
   - Depth map export (16-bit float PNG)
   - OpenPose skeleton overlay export (standard 18/25-keypoint)
   - Normal map export (for advanced lighting ControlNet)

### Stage 3: Body Layer Rendering (36 atoms)
*Outputs:* 36 × 3 (depth + openpose + preview) = 108 base body renders per camera angle; total ~1,296 files across 12 camera angles

**Rendering matrix:**
```
FOR each body_atom (36):
  FOR each camera_angle ∈ CP-S subset (12 framing × angle combos):
    SET body bone rotations per atom specification
    SET hands to CP-H-031 (relaxed neutral default)
    RENDER depth_map → {CP_ID}_depth.png (1024×1024)
    RENDER openpose → {CP_ID}_openpose.png (1024×1024)
    RENDER preview → {CP_ID}_preview.png (1024×1024)
    EXPORT metadata → {CP_ID}_meta.json
```

### Stage 4: Hand Layer Rendering (36 atoms)
*Outputs:* 36 × 12 × 3 = ~1,296 hand overlay renders

Hand gestures render as **overlay composites** onto the body base. The hand render pipeline:
1. Set body to CP-B-001 (standing neutral baseline).
2. Set ONLY hand/finger bone rotations per hand atom.
3. Render depth map — hand region only (masked).
4. Composite hand mask onto body depth map at inference time.

### Stage 5: Scene & Mood Visual Configuration
*Outputs:* 24 camera preset files, 24 lighting preset files

Scene compositions (CP-S) and Mood Visuals (CP-MV) are NOT ControlNet maps — they are ComfyUI workflow parameters:
- **CP-S:** Camera position, framing, angle → translated to FLUX prompt modifiers and ControlNet depth perspective
- **CP-MV:** Lighting, color temperature, saturation → translated to PSSL fields in the VCB (FR-VIS-01 handles this)

### Stage 6: EFS Upload & Manifest Generation
*Outputs:* Complete ControlNet library on EFS with `manifest.json`

```
/efs/ccp-models/controlnet/
├── body/
│   ├── CP-B-001_standing_square_shoulders_back/
│   │   ├── CP-S-002_depth.png
│   │   ├── CP-S-002_openpose.png
│   │   ├── CP-S-002_preview.png
│   │   ├── CP-S-005_depth.png
│   │   └── ... (per camera angle)
│   └── ... (36 body atoms)
├── hands/
│   ├── CP-H-001_index_point_camera_firm/
│   │   ├── mask_depth.png
│   │   └── mask_openpose.png
│   └── ... (36 hand atoms)
├── composed/
│   ├── CP-B-014_CP-H-017_CP-G-001_CP-S-002_v01_depth.png
│   ├── CP-B-014_CP-H-017_CP-G-001_CP-S-002_v01_openpose.png
│   └── ... (pre-composed popular combos)
└── manifest.json
```

---

## 5. Data Model

### Table: `conscious_pose_atoms`

```sql
CREATE TABLE IF NOT EXISTS conscious_pose_atoms (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cp_id VARCHAR(20) NOT NULL UNIQUE,              -- 'CP-B-001', 'CP-H-017', etc.
    layer VARCHAR(20) NOT NULL CHECK (layer IN (
        'body', 'hands', 'gaze', 'scene', 'mood_visual', 'props', 'multi_character'
    )),
    subcategory VARCHAR(50) NOT NULL,               -- 'standing_authority', 'seated_intimacy', etc.
    position_name VARCHAR(80) NOT NULL,             -- 'standing_square_shoulders_back'
    display_name VARCHAR(100),                      -- 'Square Shoulders, Authority Stance'
    signal TEXT NOT NULL,                            -- 'Full authority, grounded'
    mood_fit JSONB NOT NULL,                        -- ["Status", "Processing"]
    archetype_fit JSONB,                            -- ["The Educator", "The Challenger"]
    mirror_neuron_target TEXT,                       -- 'Gaze cueing → parasocial lock'
    bvt_function TEXT,                              -- For memetic atoms: 'Benignness signal (body)'
    scene_constraint TEXT,                           -- 'Requires CP-S-005 or wider'
    controlnet_depth_path TEXT,                      -- '/efs/ccp-models/controlnet/body/CP-B-001/'
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

ALTER TABLE conscious_pose_atoms ENABLE ROW LEVEL SECURITY;
```

### Table: `conscious_pose_compositions`

```sql
CREATE TABLE IF NOT EXISTS conscious_pose_compositions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    composition_id VARCHAR(50) NOT NULL UNIQUE,     -- 'COMP-EDUCATOR-DEFAULT-001'
    composition_name VARCHAR(100) NOT NULL,          -- 'Educator Default - Teaching Authority'
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
    archetype_family VARCHAR(50),                    -- 'The Educator'
    humor_architecture VARCHAR(50),                  -- 'Observational' (for memetic recipes)
    composed_asset_path TEXT,                        -- '/efs/ccp-models/controlnet/composed/...'
    is_pre_rendered BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

ALTER TABLE conscious_pose_compositions ENABLE ROW LEVEL SECURITY;
```

### Table: `controlnet_render_jobs`

```sql
CREATE TABLE IF NOT EXISTS controlnet_render_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id VARCHAR(50) NOT NULL UNIQUE,
    atom_cp_id VARCHAR(20) NOT NULL,
    camera_cp_id VARCHAR(20),
    render_types JSONB NOT NULL,                     -- ["depth", "openpose", "normal", "preview"]
    resolution VARCHAR(20) DEFAULT '1024x1024',
    source_rig VARCHAR(50) NOT NULL,                 -- 'iclone_base_v1'
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
```

### Primary Output Schema: `pose_spec` (embedded in VCB)

```json
{
  "pose_spec": {
    "body": "CP-B-014",
    "hands": "CP-H-017",
    "gaze": "CP-G-001",
    "scene": "CP-S-002",
    "mood_visual": "CP-MV-001",
    "props": "CP-P-024",
    "multi_character": "CP-MC-001",
    "composition_id": "COMP-STORYTELLER-DEEP-003",
    "controlnet_depth": "/efs/ccp-models/controlnet/composed/CP-B-014_CP-H-017_CP-S-002_v01_depth.png",
    "controlnet_openpose": "/efs/ccp-models/controlnet/composed/CP-B-014_CP-H-017_CP-S-002_v01_openpose.png",
    "controlnet_strength": 0.85
  }
}
```

---

## 6. Backward Compatibility

If a VCB does not contain a `pose_spec` field (legacy pipeline), Paradoxe falls back to prompt-only pose description using prose in the PSSL `body_language` field. ControlNet nodes are NOT injected into the ComfyUI workflow. A `LEGACY_POSE_PROMPT_ONLY` warning is logged. Output will be non-deterministic but visually acceptable.

---

## 7. Tasks

- [ ] **Task 1:** Parse production library (168 atoms) and expansion library (130 atoms) into database seed script.
- [ ] **Task 2:** Write DB migration `004_visual_control_layer.sql` — create `conscious_pose_atoms`, `conscious_pose_compositions`, `controlnet_render_jobs` tables.
- [ ] **Task 3:** Seed database with all 298 atoms and all composition recipes (Archetype + Memetic).
- [ ] **Task 4:** Set up iClone 8 Python automation for batch bone manipulation and rendering.
- [ ] **Task 5:** Render Body layer (36 atoms × 12 camera angles × 3 render types = ~1,296 files).
- [ ] **Task 6:** Render Hand layer (36 atoms, masked overlays).
- [ ] **Task 7:** Pre-compose top-priority compositions (Archetype defaults × 7 + Memetic recipes × 14 = ~21 pre-rendered sets).
- [ ] **Task 8:** Upload all ControlNet maps to EFS at `/efs/ccp-models/controlnet/`.
- [ ] **Task 9:** Generate `manifest.json` index of all assets with checksums.
- [ ] **Task 10:** Write `conscious_pose_resolver.py` — resolves CP-IDs from VCB `pose_spec` to EFS file paths.
- [ ] **Task 11:** Integrate ControlNet depth + openpose nodes into ComfyUI Tier 3 workflow.
- [ ] **Task 12:** Validate: same CP-ID composition + same seed = identical output across 10 runs.
- [ ] **Task 13:** Register DEP-VIS-010 in the dependency registry.

---

## 8. Acceptance Criteria

- [ ] **AC1 (Deterministic Reproduction):** Generate 10 images using `CP-B-002 + CP-H-009 + CP-G-001 + CP-S-002` with the same seed. Assert all 10 outputs are pixel-identical (SSIM ≥ 0.99). *Failure:* Two outputs show different arm positions — ControlNet conditioning is not overriding FLUX's stochastic pose generation.
- [ ] **AC2 (Composition Resolution):** Submit VCB with `composition_id: "COMP-EDUCATOR-DEFAULT-001"`. Assert resolver returns the correct 7-layer CP-ID decomposition and valid EFS file paths. *Failure:* Resolver returns a 404 for the depth map — asset not uploaded to EFS.
- [ ] **AC3 (Layer Independence):** Change ONLY `hands_cp_id` from CP-H-031 (relaxed) to CP-H-001 (point at camera). Assert body position remains identical (depth map difference < 5% in non-hand regions). *Failure:* Changing hands also shifts the torso — layers are not independently composable.
- [ ] **AC4 (Mood-State Query):** Query `conscious_pose_atoms` for atoms with `mood_fit @> '["Processing"]'`. Assert result includes CP-B-001 (authority), CP-B-014 (forward lean), CP-MV-001 (warm intimate). Assert result excludes CP-B-034 (victory arms). *Failure:* Query returns all 298 atoms — mood_fit index is not filtering.
- [ ] **AC5 (EFS Hot Mount):** Add a new pre-composed ControlNet map to EFS while ComfyUI is running. Submit a generation request referencing the new file within 60 seconds. Assert ComfyUI loads the new map without restart. *Failure:* ComfyUI returns file-not-found — NFS cache is stale.
- [ ] **AC6 (Manifest Integrity):** Run `manifest.json` validation against EFS directory. Assert every path in the manifest resolves to an existing file. Assert every file on EFS is listed in the manifest. *Failure:* 3 orphan files on EFS not tracked by manifest.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| DEP-VIS-010 (ControlNet Map Library) | Output | Rendered depth/openpose PNGs on EFS. |
| DEP-VIS-005 (VCB Schema) | Upstream | VCB `pose_spec` field specifies CP-IDs. |
| DEP-VIS-008 (ConsciousSmile) | Co-loaded | Expression adapter runs alongside ControlNet. |
| DEP-VIS-011 (Identity LoRA) | Co-loaded | Coach identity + pose + expression = character. |
| FR-VIS-01 (VCB Generation) | Upstream | Abel selects CP-IDs based on mood state + archetype. |
| FR-VIS-03 (Prompt Compilation) | Downstream | Paradoxe injects ControlNet nodes into workflow. |
| FR-VIS-04 (Visual Validation) | Downstream | Validates pose fidelity post-generation. |
| FR-VIS-14 (ConsciousSmile) | Co-dependency | Expression + pose are applied simultaneously. |
| SPEC-INFRA-001 §3.2 | Infrastructure | MIG Partition A (40GB). |
| SPEC-INFRA-001 §7.3 | Infrastructure | EFS at `/efs/ccp-models/controlnet/`. |
| iClone 8 + Python API | External | 3D rig and batch rendering. |

---

## 10. Testing Strategy

### Unit Tests
- **CP-ID Validation:** Provide `CP-B-037` (non-existent). Assert resolver throws `INVALID_CP_ID`.
- **Composition Validation:** Provide composition with `body: CP-B-001, scene: CP-S-001` (extreme closeup — incompatible with full body standing). Assert validation warns `FRAMING_MISMATCH`.
- **Manifest Checksum:** Corrupt one depth map file. Assert manifest validation catches the checksum mismatch.

### Integration Tests
- **Full Tier 3 Pipeline:** Submit VCB with `pose_spec` + `expression_spec` + Identity LoRA. Run through FR-VIS-03 → ComfyUI. Assert output shows correct body position, correct expression, and correct coach identity.
- **Horizontal Scaling:** Boot 2 ComfyUI replicas on different EC2 instances, both mounting the same EFS volume. Submit the same composition to both. Assert identical outputs.

### Safety Tests
- **Path Traversal:** Inject `controlnet_depth: "../../../../etc/passwd"` into `pose_spec`. Assert resolver sanitizes the path and rejects non-EFS paths.
- **Oversized ControlNet Map:** Provide a 4096×4096 depth map instead of 1024×1024. Assert ComfyUI resizes it or rejects it, does not OOM.
