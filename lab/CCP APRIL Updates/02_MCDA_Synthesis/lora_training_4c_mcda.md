# LoRA Training Methodology: 4C Framework + MCDA Synthesis

> **Objective:** A proprietary CCF LoRA training methodology optimized for **Coach Cinematic Image Consistency**, first-prompt accuracy, and physiological engagement — grounded in 14 LoRA research papers and 8 CVE+CPSC neuroscience papers.

---

## What Is Signal-to-Noise Ratio (SNR) and Why It Matters

SNR in LoRA training describes the **ratio of meaningful learned features (signal) to random artifacts and base-model interference (noise)** at each stage of the denoising process.

### The Two-Phase Model (from Klein Training Research)

| Phase | Denoising Steps | What the Model "Sees" | What Gets Encoded |
|---|---|---|---|
| **High-Noise** | Steps 0–10 (of 20) | Blurry blobs — composition, layout, spatial relationships | WHERE things are, overall color temperature, scene structure |
| **Low-Noise** | Steps 11–20 | Fine detail — textures, skin pores, light artifacts, grain | HOW things look — surface quality, film grain, halation |

### Why This Matters for CCF

When training a LoRA with **balanced** timesteps (default), the model learns composition and texture with **equal weight**. This means:
- It may **miss compositional trends** (gaze direction, subject placement) because it's also trying to learn grain patterns
- It may **miss texture nuances** because it's also learning where objects go

### Practical Implication: The Decay Parameter

The **decay** parameter is the single most impactful "knob" for style control (per Klein research, 30+ training runs):

| Decay Value | Visual Effect | CCF Use Case |
|---|---|---|
| **Default (0.001)** | Balanced, neutral output | Baseline — not optimal for any specific look |
| **10x lower (0.0001)** | Wider waveform channels → preserved shadow detail, bloom, halation, desaturated palette | **GMG Expert 02** (Noir Triad), **CAC Composer** (editorial dirty light) |
| **20x lower (0.00005)** | Even more washed out, elevated black point, cross-processed look | Specific vintage/expired film effects |
| **5x higher (0.005)** | Crunched channels → extreme contrast, punchy, OLED-like | **GMG Expert 06** (binary geometry), high-contrast hook frames |

> [!IMPORTANT]
> **Key Finding:** Changing the learning rate by even 0.005% on FLUX 2 architecture "ripped apart" the image. **Lock learning rate at 0.0001 and never change it.** Use decay as the primary aesthetic control instead.

---

## The 4C Framework

### C1: COLLECT — Dataset Curation Protocol

The dataset determines 80% of the LoRA's quality. Every paper converges on this principle.

#### Identity LoRAs (Coach Face)
| Parameter | Specification | Source |
|---|---|---|
| **Image Count** | 30–50 real high-res images | Brand Avatar Identity |
| **Source Quality** | Full-res screenshots from IG Reels / 4K YouTube — NOT airbrushed | Brand Avatar Identity |
| **Faceswap Policy** | **ZERO faceswaps** — skin-boundary artifacts encode as identity features | Brand Avatar Identity, Neurocinematic LoRA |
| **Synthetic Augmentation** | 13–18 additional via FLUX inpainting (face preserved, environment varied) | Brand Avatar Identity |
| **Lighting Stratification** | 25% hard sunlight + 25% soft studio + 25% warm indoor + 25% blue-hour | Brand Avatar Identity |
| **Expression Stratification** | 30% active (smiling/speaking) + 20% neutral/serious + 30% diverse micro-expressions + 20% contemplative | Brand Avatar Identity, PSSL |
| **Angle Stratification** | 20% frontal + 40% 3/4 profile (L+R) + 20% slight pitch up/down + 20% synthetic environments | Brand Avatar Identity |

#### Style LoRAs (GMG/CAC Aesthetics)
| Parameter | Specification | Source |
|---|---|---|
| **Image Count** | 300–500 (complex styles like Expert 03) / 40–80 (focused styles like Noir Triad) | Animation Consistency, Klein Research |
| **Selection Principle** | **Push the needle further than desired** — base model will water down the style | Klein Research (critical insight) |
| **Pose-Color Matrix** | For Expert 03: all 12 poses × 6 palettes = 72 minimum concept intersections | Animation Consistency |
| **Out-of-Distribution Test Set** | Reserve 10% of prompts with tokens NOT in the training data | Klein Research |
| **Caption Strategy** | Describe ONLY content, NOT style — "what you don't caption is what the trigger word learns" | FLUX.2 Tutorial, Animation Consistency |

#### The "Anti-Uncanny" Data Principle
> **Research Reference:** Brand Character System + Klein Research
>
> Training images should preserve natural imperfections:
> - Retain pore-level detail and micro-pigmentation (ST metric)
> - Keep micro-expression asymmetries (EN metric)
> - Include environmental grain and texture artifacts
>
> "Images that are overly smoothed are rated as **less authentic** than those that retain textured, slightly imperfect details" — the **Perfection-Trust Paradox**.

---

### C2: CONFIGURE — Hyperparameter Protocol

#### Universal Constants (Never Change These)
| Parameter | Value | Rationale |
|---|---|---|
| **Learning Rate** | 0.0001 | FLUX 2 architecture extremely sensitive; ±0.005% destroys output |
| **Optimizer** | AdamW / AdamW8Bit | Standard for transformer LoRA; 8bit version for ≤24GB VRAM |
| **Weight Decay** | 0.01 | Standard generalization term |
| **Precision** | BF16 (training) / BF16 (save) | FP32 training was NOT conclusively better and costs 5x more |
| **Resolution** | 1024×1024 | Native scaling requirement for FLUX 2's 4MP architecture |
| **CFG/Guidance** | 1.0 (training) | Guidance-distilled model — CFG 1 is a no-op, this is how it's trained |

#### LoRA-Type-Specific Configuration
| Parameter | Identity LoRA | Style LoRA (Simple) | Style LoRA (Complex) |
|---|---|---|---|
| **Rank (Linear)** | 16 | 128 | 48–64 |
| **Rank Alpha (Linear)** | 8 | 64 | 24–32 |
| **Rank (Conv)** | 16 | 64 | 48–64 |
| **Rank Alpha (Conv)** | 8 | 32 | 24–32 |
| **Ratio** | 2:1:2:1 | **4:2:2:1** | 2:1:2:1 |
| **Decay** | Default (0.001) | **0.0001** (10x lower) | Default (0.001) |
| **Steps** | 1,200–1,800 | 7,000 (fidelity) / 3,000 (artistic) | 2,000–2,500 |
| **Timestep Type** | Weighted | Weighted | Weighted |
| **DOP Enabled** | Yes (if stacking) | Yes (essential) | Yes (essential) |
| **Caption Dropout** | Low (0.05) | Low (0.05) | Low (0.05) |

> [!TIP]
> **The 4:2:2:1 Network Dimension Ratio** was validated across 64+ training runs on both FLUX 2 Dev and Klein. It consistently outperforms all other ratios for style LoRAs. The staggered values help the model learn fine-grain details at multiple spatial scales.

#### The "Two-Version" Release Pattern
From the Klein research, a critical production insight:
- **3K steps** = more artistic degradation, light leaks, film artifacts → use for **Hook frames** (W1)
- **7K steps** = more structural fidelity, subject accuracy → use for **Proof/Close frames** (W4-W5)
- Ship BOTH versions and select per arc position in the pipeline

---

### C3: CALIBRATE — Validation & Quality Gates

#### Automated Metrics
| Metric | Target | What It Measures | Source |
|---|---|---|---|
| **IPS** (Identity Persistence Score) | ≥ 0.92 across 5 novel prompts | CLIP cosine similarity between generated output and source images | Brand Avatar Identity |
| **AGSS** (Anti-Generic Specificity) | Level 4 | Euclidean distance from "generic professional" cluster in latent space | Brand Avatar Identity, Neurocinematic LoRA |
| **MSSIM** (Mean Structural Similarity) | ≥ 0.90 across frames | Cross-frame structural consistency for sequential content | Animation Consistency |
| **Color Histogram Intersection** | ≥ 0.90 | Palette adherence to target hex codes | Animation Consistency |
| **Canny Edge Thickness** | Within spec (e.g., 2–4px for Expert 03) | Outline weight consistency via edge detection | Animation Consistency |
| **LPIPS** (Perceptual Distance) | Higher = better (from base model) | Confirms LoRA is producing non-generic imagery | Neurocinematic LoRA |

#### The Out-of-Distribution (OOD) Test Protocol
> **The most important validation step.** (From Klein Research)
>
> 1. Write 5 prompts where **zero tokens** appear in the training data (e.g., "dog on a log" for a portrait LoRA)
> 2. Generate at 1024×1024 (a resolution NOT in the training data if you trained on 1920×1080)
> 3. If the style transfers cleanly → the LoRA has learned the **concept**, not memorized the **data**
> 4. If the style only works on training-similar prompts → the LoRA is overfit, reduce steps or increase dataset diversity

#### The "Waveform" Diagnostic
From Klein research — use RGB waveform analysis to measure the actual pixel-level effect of your LoRA:
- **Channel separation** = contrast/saturation level
- **Black point elevation** = shadow rendering (lower = cinematic depth)
- **White point consistency** = highlight behavior
- Compare waveform of LoRA output vs. base model to quantify the LoRA's actual contribution

---

### C4: CASCADE — Pipeline Integration & Stacking

#### LoRA Stacking Weight Budget
> **Total combined weight of all active LoRAs must stay below 1.1** to avoid fuzzy artifacts. (Brand Avatar Identity)

| LoRA Layer | Purpose | Weight Range | Priority |
|---|---|---|---|
| **Coach Identity** | Facial persistence | 0.40–0.55 | Highest — non-negotiable |
| **PAD Color Grade** | Brand-specific cinematic palette | 0.20–0.30 | High — defines emotional tone |
| **Somatic Hook** | Posture/body language alignment | 0.15–0.25 | Medium — for full-body scenes |
| **Gaze Vector** | Eye contact control | 0.10–0.20 | Medium — CBCS-tier dependent |
| **Style (GMG/CAC)** | Visual language enforcement | 0.15–0.25 | Conditional — only for non-identity scenes |

#### Multi-Reference Anchoring (FLUX 2 Exclusive)
FLUX 2 supports **up to 10 reference images** in a single generation. Use this to:
1. Provide 2–3 real coach photos alongside the LoRA for identity reinforcement
2. Include 1–2 "style anchor" frames from previous generations for continuity
3. This creates a **dual-lock system**: LoRA weights + pixel-level reference cross-checking

#### Asset-First Generation Pipeline
From Animation Consistency paper — the sequence matters:
1. **Generate Last Frame** (T2I + LoRA + locked seed) → visual anchor
2. **Generate First Frame** (I2I from Last Frame) → contextual stability
3. **Animate** (I2V via Wan 2.2 using First + Last as keyframes) → motion synthesis
4. **Refine** (FLUX Klein 9b for inpainting corrections) → post-production polish

---

## MCDA Synthesis: Signal vs. Noise Analysis

### Evaluation Criteria (Weighted by CCF Goals)

| Criterion | Weight | Description |
|---|---|---|
| **W1: Coach Identity Consistency** | 30% | Does it produce recognizable coach faces across diverse prompts? |
| **W2: First-Prompt Accuracy** | 25% | Does the style/identity work correctly on the first generation? |
| **W3: Physiological Engagement** | 20% | Does it encode research-backed visual triggers (PSSL, ISC targets)? |
| **W4: Production Speed** | 15% | Does it reduce iteration time and cost? |
| **W5: Dataset Scalability** | 10% | Can the methodology scale to 100+ coaches without quality loss? |

### Parameter-Level MCDA

| Parameter / Decision | W1 (30%) | W2 (25%) | W3 (20%) | W4 (15%) | W5 (10%) | **Weighted Score** | **Verdict** |
|---|---|---|---|---|---|---|---|
| **Network Dim 4:2:2:1** | 9 | 9 | 7 | 8 | 9 | **8.5** | ✅ SIGNAL — universally validated |
| **Decay 10x lower (0.0001)** | 7 | 8 | 9 | 8 | 8 | **7.9** | ✅ SIGNAL — for cinematic styles |
| **Decay 5x higher (0.005)** | 5 | 6 | 7 | 8 | 8 | **6.2** | ⚠️ CONDITIONAL — only for Expert 06 |
| **Rank 16 (identity)** | 9 | 8 | 6 | 9 | 9 | **8.2** | ✅ SIGNAL — tight focus prevents overfitting |
| **Rank 48-64 (complex style)** | 8 | 9 | 8 | 6 | 7 | **8.0** | ✅ SIGNAL — necessary for pose-color matrix |
| **Rank 128 (simple style)** | 6 | 9 | 8 | 5 | 6 | **7.1** | ⚠️ CONDITIONAL — only for focused style LoRAs |
| **FP32 training** | 6 | 6 | 5 | 2 | 3 | **4.9** | ❌ NOISE — 5x cost, inconclusive benefit |
| **High/Low noise split** | 5 | 5 | 6 | 3 | 4 | **4.8** | ❌ NOISE — "didn't beat single-pass" (Klein) |
| **EMA (0.997)** | 4 | 5 | 4 | 6 | 6 | **4.7** | ❌ NOISE — worse outputs across tests |
| **Caption dropout >0.1** | 5 | 4 | 5 | 7 | 6 | **5.0** | ❌ NOISE — reduces prompt adherence |
| **DOP (Differential Output Preservation)** | 9 | 9 | 7 | 7 | 9 | **8.4** | ✅ SIGNAL — essential for stacking |
| **Zero-Faceswap Policy** | 10 | 8 | 9 | 6 | 8 | **8.7** | ✅ SIGNAL — highest-impact data quality rule |
| **Synthetic Inpainting Augmentation** | 7 | 7 | 6 | 8 | 9 | **7.2** | ✅ SIGNAL — doubles env diversity safely |
| **Multi-Reference Anchoring** | 9 | 9 | 7 | 7 | 9 | **8.4** | ✅ SIGNAL — FLUX 2 unique advantage |
| **OOD Testing Protocol** | 8 | 10 | 7 | 7 | 8 | **8.2** | ✅ SIGNAL — the real validation method |
| **Waveform Diagnostics** | 7 | 8 | 9 | 6 | 7 | **7.5** | ✅ SIGNAL — measurable aesthetic control |
| **Two-Version Release (3K/7K)** | 7 | 7 | 8 | 9 | 8 | **7.6** | ✅ SIGNAL — arc-position selection |
| **Gradient Accumulation** | 5 | 5 | 4 | 3 | 5 | **4.6** | ❌ NOISE — increases cost, no quality gain |
| **LR Factor tuning** | 4 | 4 | 4 | 3 | 4 | **3.9** | ❌ NOISE — untested, high risk |
| **Sigmoid timestep** | 5 | 5 | 5 | 7 | 6 | **5.3** | ⚠️ MARGINAL — default weighted is better |
| **Asset-First (Last→First→I2V)** | 9 | 9 | 8 | 8 | 9 | **8.7** | ✅ SIGNAL — critical for animation consistency |

### Final Signal/Noise Summary

#### ✅ SIGNAL (Implement Immediately) — Score ≥ 7.0
1. **Zero-Faceswap Policy** (8.7) — Data quality foundation
2. **Asset-First Pipeline** (8.7) — Generation sequence
3. **4:2:2:1 Network Dimensions** (8.5) — Universal rank ratio
4. **DOP (Differential Output Preservation)** (8.4) — Stacking prerequisite
5. **Multi-Reference Anchoring** (8.4) — FLUX 2 identity reinforcement
6. **Rank 16 for Identity** (8.2) — Tight focus
7. **OOD Testing** (8.2) — Real validation
8. **Rank 48-64 for Complex Styles** (8.0) — Pose-color matrix
9. **Decay 0.0001 for Cinematic** (7.9) — Aesthetic control
10. **Two-Version Release** (7.6) — Arc-position matching
11. **Waveform Diagnostics** (7.5) — Measurable aesthetics
12. **Inpainting Augmentation** (7.2) — Safe dataset expansion

#### ⚠️ CONDITIONAL (Use Case Specific) — Score 5.0–6.9
13. **Rank 128 Simple Style** (7.1) — Only for focused single-concept LoRAs
14. **Decay 5x Higher** (6.2) — Only for Expert 06 / binary contrast
15. **Sigmoid Timestep** (5.3) — Only if default weighted fails

#### ❌ NOISE (Do Not Implement) — Score < 5.0
16. **Caption Dropout >0.1** (5.0) — Reduces prompt adherence
17. **FP32 Training** (4.9) — Inconclusive, 5x cost
18. **High/Low Noise Split** (4.8) — Tested extensively, failed to beat single-pass
19. **EMA 0.997** (4.7) — Worse outputs
20. **Gradient Accumulation** (4.6) — Cost increase, no quality gain
21. **LR Factor Tuning** (3.9) — Untested, high risk of destroying model

---

## The CCF Proprietary LoRA Training SOP

### Phase 1: COLLECT (Day 1)
1. Source 30-50 real high-res images per coach (NO faceswaps)
2. Stratify: Lighting (4 conditions) × Expression (4 states) × Angle (4 views)
3. Augment with 13-18 FLUX inpainting variants
4. Caption using trigger + content-only format (never describe style)

### Phase 2: CONFIGURE (Day 1-2)
1. Set universal constants (LR=0.0001, BF16, 1024px, CFG=1)
2. Select rank by LoRA type (16 identity / 128 style / 48-64 complex)
3. Set decay by target aesthetic (0.0001 for noir/editorial, 0.001 for neutral)
4. Enable DOP with preservation class "photo"
5. Train: Identity=1,500 steps / Style=7,000 steps (save every 500)

### Phase 3: CALIBRATE (Day 2)
1. Run OOD test: 5 prompts with zero training tokens
2. Test at non-training resolution (1024x1024 if trained on 1920x1080)
3. Run multiple seeds (minimum 10) to assess seed dependence
4. Measure IPS ≥ 0.92 (identity) or MSSIM ≥ 0.90 (consistency)
5. Compare RGB waveforms against base model
6. Select optimal step count from saved epochs

### Phase 4: CASCADE (Day 2-3)
1. Set inference weights within the <1.1 budget
2. Enable Multi-Reference Anchoring (2-3 real coach photos)
3. Implement Asset-First pipeline (Last Frame → First Frame → I2V)
4. Deploy FLUX Klein 9b for post-production corrections
5. Validate final output against physiological targets (PSSL/ISC)

> [!CAUTION]
> **Cost Estimate:** Based on research data, training a single coach LoRA (identity + style) on enterprise GPU costs **$0.50–$5.00**. At the $50/week CMF subscription, this represents a one-time investment of less than 10% of the first week's revenue per coach.

---

## Key Research Sources

| Paper | Primary Contribution to 4C Framework |
|---|---|
| **How to Train FLUX.2 LoRA (AI Toolkit)** | DOP mechanism, trigger word architecture, CFG=1 training |
| **LoRA Training for Flux.2 Klein** | Decay as aesthetic control, 4:2:2:1 ratio, OOD testing, high/low noise failure |
| **Brand Avatar Identity** | Dataset stratification, zero-faceswap, IPS/AGSS metrics, stacking weights |
| **Neurocinematic LoRA for Visual Hooks** | SHA framework, ISC validation, luminance contrast targets |
| **Animation Consistency LoRA** | Rank 48-64 justification, DOP, SSIM validation, Asset-First pipeline |
| **PAD-Driven Cinematic Color** | Emotional color encoding via LoRA |
| **Gaze Vector LoRA** | Conversion-centric gaze control |
| **Chromatic Arc LoRA** | Arc-position color temperature shifts |
