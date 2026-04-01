# CCP Expression Adapter: PixelSmile-Style Training with MetaHuman Data

> **Date:** 2026-03-29
> **Question:** If we train our own PixelSmile using 16 CCP expressions + MetaHuman data, what do we gain vs. their FFE dataset? What would the CVE research advocate?

---

## Part 1: What PixelSmile Actually Built (Paper Deep-Dive)

### Their Architecture
- **Base Model:** Frozen MMDiT (Multi-Modal Diffusion Transformer) — likely Qwen2.5-VL
- **Adaptation:** LoRA fine-tuning on the MMDiT
- **Control:** Textual Latent Interpolation — α slider (0→1) interpolates between neutral and target expression in text embedding space
- **Disentanglement:** Symmetric Contrastive Loss — pulls generated image toward target expression while pushing AWAY from confusing similar expressions (e.g., Surprise vs. Fear)
- **Identity Lock:** ArcFace identity preservation loss — penalizes the model if the generated face's biometric signature changes

### Their FFE Dataset
| Attribute | FFE Dataset |
| :--- | :--- |
| **Size** | 60,000 images (30k real + 30k anime) |
| **Base identities** | ~6,000 real-world portraits + ~6,000 anime (629 characters from 207 productions) |
| **Expressions** | 12 categories: 6 basic (happy, sad, angry, surprised, fear, disgust) + 6 extended (confused, contempt, confident, shy, sleepy, anxious) |
| **Labels** | 12-dimensional continuous score vector v ∈ [0,1]¹² per image |
| **Label source** | Gemini 3 Pro vision-language model + human spot-verification |
| **Generation** | Nano Banana Pro (image editing model) |
| **Prompt design** | Dual-part: global expression category + localized facial attributes (mouth shape, brow, eye openness) |

### Their Key Innovation
**Textual Latent Interpolation.** Instead of using LoRA weight as the intensity dial (our original approach), PixelSmile interpolates in the TEXT EMBEDDING space:

```
e_cond(α) = e_neutral + α × (e_target - e_neutral)
```

When α=0 → neutral face. When α=1 → full target expression. **Also supports α>1 for exaggeration.** The α is supervised during training so that α=0.5 actually produces a 50%-intensity expression, not random garbage.

### Their Critical Limitation
**Only 12 expression categories.** No gaze control, no asymmetric expressions, no micro-expressions, no head tilt. The 12 categories are emotion-centric, not muscle-centric.

---

## Part 2: CCP 16-Expression MetaHuman Architecture vs. FFE

### What We Would Build Differently

| Dimension | PixelSmile FFE | CCP MetaHuman Dataset | Advantage |
| :--- | :--- | :--- | :--- |
| **Expression taxonomy** | 12 emotion categories (happy, sad, angry, surprised, fear, disgust, confused, contempt, confident, shy, sleepy, anxious) | 16 FACS-based muscle groups (smile, gaze_vert, gaze_horiz, brow_raise, brow_furrow, eye_squint, eye_wide, jaw_open, lip_press, mouth_frown, lip_pucker, nose_wrinkle, chin_raise, dimpler, head_tilt, eye_moisture) | **CCP wins.** FACS is composable — you can BUILD any emotion from muscle groups. FFE's emotions are pre-composed and can't be decomposed. |
| **Composability** | Can blend 2 categories (e.g., 40% happy + 60% surprised) via multi-category interpolation | Can compose arbitrary combinations from independent muscle groups | **CCP wins.** "Warm but slightly concerned" = smile(0.3) + brow_furrow(0.25). FFE can't express this without training a "warm_but_concerned" category. |
| **Gaze control** | ❌ None | ✅ Dedicated gaze_vertical and gaze_horizontal channels | **CCP wins.** Eye direction is the #1 signal for emotional connection in coaching content. PixelSmile cannot control where the eyes look. |
| **Data source quality** | AI-generated expression edits (Nano Banana Pro on real photos) | MetaHuman renders (ground-truth 3D muscle positions) | **CCP wins.** MetaHuman expressions are geometrically precise — the blendshape values ARE the ground truth. FFE relies on an AI model (Nano Banana Pro) to generate expressions, introducing a quality bottleneck: the data is only as good as Nano Banana's expression editing ability. |
| **Label precision** | 12-dim continuous score predicted by Gemini 3 Pro (proxy labels, ~80-90% accurate) | Exact ARKit blendshape values used in rendering (100% accurate by construction) | **CCP wins massively.** Our labels are DEFINITIONALLY correct because we defined the expression parameters before rendering. FFE's labels are estimated after generation. |
| **Dataset diversity** | ~6,000 base identities (photos of real humans) | MetaHuman-rendered faces (diverse but synthetic) | **PixelSmile wins.** Real human faces have infinitely more texture variety, asymmetry, and imperfection. MetaHuman faces, even with 152 texture variations, still feel subtly synthetic. |
| **Training base model** | Qwen2.5-VL (closed-source, image editing model) | FLUX 2 Dev (open-weight, text-to-image model) | **CCP wins for our pipeline.** FLUX is our production model. Training directly on FLUX means zero model-switching at inference. PixelSmile requires Qwen2.5-VL, which doesn't integrate into ComfyUI natively. |
| **Number of images** | 60,000 | Target: 5,000-10,000 (start), expandable | **PixelSmile wins on scale** but our per-image label quality is higher. |

### The Honest Bottom Line

> **PixelSmile has better DATA DIVERSITY (real human photos).**
> **CCP has better LABEL PRECISION (ground-truth blendshapes) and COMPOSABILITY (FACS-based).**
> **CCP has better PIPELINE INTEGRATION (native FLUX, native ComfyUI).**

---

## Part 3: What the CVE Research Advocates

Our CVE research audit scores visual tools on 5 criteria. Here's how each training approach performs against them:

### C1: Physiological Targeting (30% weight)

The CVE research demands expressions that target SPECIFIC somatic states:
- Corrugator supercilii activation (brow tension) for stress/concern
- Zygomaticus major activation (smile) for joy
- SCR (skin conductance) spikes for arousal
- fEMG (facial electromyography) patterns for empathy

| Approach | Score | Why |
| :--- | :--- | :--- |
| PixelSmile FFE | 3/5 | Generic emotions, not physiologically targeted |
| CCP 16 FACS | 5/5 | FACS Action Units MAP DIRECTLY to specific muscles that drive somatic responses in viewers |

**CVE verdict: FACS-based expressions are scientifically superior.** "Happy" is vague. `smile(0.7) + eye_squint(0.5) + brow_raise(0.1)` is a Duchenne smile that triggers mirror neuron zygomaticus activation in the viewer. The CVE demands this level of specificity.

### C2: Gaze Architecture (20% weight)

The CVE's Gaze Cueing research documents 18.2ms reflexive attention shifts triggered by gaze direction.

| Approach | Score | Why |
| :--- | :--- | :--- |
| PixelSmile FFE | 1/5 | Zero gaze control |
| CCP 16 FACS | 5/5 | Dedicated gaze_vertical and gaze_horizontal channels |

**CVE verdict: Gaze control is non-negotiable.** The CVE research is EXPLICIT: gaze direction controls where viewers look. PixelSmile has no gaze control. This alone makes our approach superior for CCP content.

### C3: Chromatic Psychology (20% weight)

Not directly relevant to expression training — both approaches are neutral here.

### C4: Narrative Coherence (15% weight)

The CVE's Neurocinematics research requires temporal emotional arcs (tension → release). Expression control enables this.

| Approach | Score | Why |
| :--- | :--- | :--- |
| PixelSmile FFE | 3/5 | Can create emotional progression (happy α=0.3 → happy α=0.9) |
| CCP 16 FACS | 5/5 | Can create nuanced arcs: concern(brow_furrow=0.5) → realization(brow_raise=0.7) → joy(smile=0.8, squint=0.6) — each frame composable from independent channels |

### C5: Identity & Parasocial Trust (15% weight)

Both approaches use identity preservation loss (ArcFace). Equal.

### CVE MCDA Total Score

| Approach | C1 (30%) | C2 (20%) | C3 (20%) | C4 (15%) | C5 (15%) | **Weighted** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| PixelSmile FFE | 3 | 1 | 3 | 3 | 4 | **2.75** |
| CCP 16 FACS + MetaHuman | 5 | 5 | 3 | 5 | 4 | **4.55** |

**The CVE research unambiguously advocates for the CCP FACS-based approach.**

---

## Part 4: The Training Architecture (How to Actually Build This)

### What We Borrow From PixelSmile
1. **Textual Latent Interpolation** — the α slider mechanism. This is the core innovation that makes continuous control work without stacking LoRAs.
2. **Symmetric Contrastive Loss** — prevents confusion between similar expressions (e.g., brow_raise vs eye_wide both involve the upper face).
3. **ArcFace Identity Loss** — preserves facial identity during expression editing.
4. **LoRA on frozen MMDiT** — except we target FLUX 2 Dev instead of Qwen2.5-VL.

### What We Change
1. **16-dimensional score vector** instead of 12 — one dimension per FACS channel.
2. **Multi-channel conditioning** — instead of interpolating between neutral and ONE target, we interpolate in a 16-dimensional expression space.
3. **MetaHuman ground-truth data** instead of AI-generated edits — exact blendshape values = perfect labels.
4. **FLUX 2 Dev as base model** — native integration with our ComfyUI production pipeline.

### The Modified α Mechanism

PixelSmile uses:
```
e_cond(α) = e_neutral + α × (e_target - e_neutral)
```

We would use:
```
e_cond(α₁...α₁₆) = e_neutral + Σᵢ αᵢ × (e_targetᵢ - e_neutral)
```

Where each αᵢ corresponds to one FACS channel. The prompt becomes:
```
"portrait of a person, smile:0.45, gaze_up:0.2, brow_raise:0.15, eye_squint:0.65"
```

And the model learns to apply each transformation independently because the training data isolated each variable.

> [!WARNING]
> **Key risk:** Multi-channel interpolation in text embedding space is more complex than single-channel. The semantic directions may NOT be linearly independent in FLUX's embedding space, even if the training data was perfectly isolated. This needs empirical validation.

### Training Data Requirements

| Expression Channel | MetaHuman Variations | Intensities | Diverse Faces | Angles | **Images Per Channel** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Each of 16 channels | 1 (isolated variable) | 5 (α = 0.2, 0.4, 0.6, 0.8, 1.0) | 20 | 3 | **300** |
| **Total** | | | | | **4,800 base** |
| + Confusion pairs (symmetric contrastive) | 8 confusing pairs × 200 triplets | | | | **+1,600** |
| **Grand Total** | | | | | **~6,400 images** |

This is 10x smaller than PixelSmile's FFE (60,000) but with 100% accurate labels vs. ~85% accuracy proxy labels.

---

## Part 5: Strategic Decision — Which Approach?

### Option A: Pure PixelSmile Clone (On FLUX)
Replicate PixelSmile exactly but on FLUX 2 Dev with their 12 emotion categories. Use their FFE dataset if/when it's released.
- **Pros:** Proven architecture, less engineering risk
- **Cons:** No gaze control, no FACS decomposition, limited composability

### Option B: CCP FACS Adapter (Our Proposal)
Build a 16-channel FACS-based expression adapter on FLUX 2 Dev using MetaHuman-generated data.
- **Pros:** Gaze control, composability, CVE-aligned, ground-truth labels, native FLUX
- **Cons:** Unproven multi-channel interpolation, requires MetaHuman rendering pipeline, smaller dataset

### Option C: Hybrid
Start with PixelSmile's proven single-channel architecture but use MetaHuman data for 5 priority channels (smile, gaze_vert, brow_raise, brow_furrow, eye_squint). Train 5 SEPARATE adapters, each with its own α slider.
- **Pros:** Proven architecture per channel, no stacking weight conflicts (only 1 expression adapter active at a time + identity LoRA), ground-truth MetaHuman data
- **Cons:** Can't compose multiple expressions in a single generation (but can sequence them)

> [!IMPORTANT]
> **Option C avoids the LoRA stacking problem entirely.** Each generation uses exactly 2 LoRAs: Coach Identity + ONE expression channel. Total weight stays under 1.0. The composition happens across a carousel of images, not within a single image.
