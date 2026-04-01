# 7 Research Paper Proposals — LoRA Training for the CCP Visual Pipeline

**Target Model:** FLUX 2 Dev (Black Forest Labs, 32B open-weight)
**LoRA Framework:** FLUX 2 Dev LoRA fine-tuning with GGUF quantization
**Light Editing / Inpainting:** FLUX Klein 9b (ControlNet, background removal, text removal, inpainting)
**Video Generation:** Wan 2.2 (inference only — no LoRA training recommended)

> [!IMPORTANT]
> All 7 proposals target **LoRA training on FLUX 2 Dev exclusively**. Wan 2.2 is referenced only for downstream I2V inference where the LoRA-generated T2I output feeds into video — the video model itself is not trained.

---

## PROPOSAL 1: Somatic Hook Architecture LoRA — Training Physiologically Targeted First-Frame Compositions for Maximum Inter-Subject Correlation

### Abstract

This proposal investigates the training of a domain-specific LoRA adapter for FLUX 2 Dev that deterministically generates "somatic hook" compositions — first-frame visuals engineered to trigger phasic galvanic skin response (GSR) spikes and ventral attention network activation within the first 800 milliseconds of visual exposure. Current text-to-image pipelines rely on generic prompt engineering for hook frames, producing outputs that cluster around the training distribution average (mode collapse toward "motivational quote" aesthetics). This study proposes a curated dataset of 800–1200 images exhibiting specific perceptual features documented in neurocinematic research: high luminance contrast ratios (≥4:1 foreground-to-background), warm-dominant color temperatures (CCT ≥ 5500K), center-weighted subject placement with upper-left key lighting, and shadow opacity ranges of 70–80%. The dataset construction follows the Anti-Generic Specificity Scale (AGSS) Level 4 criteria from the Physiological State Specification Language (PSSL) framework, ensuring each training image occupies a measurable latent-space distance from the generic FLUX 2 Dev training distribution. The LoRA training protocol targets a rank of 32–64 with a learning rate of 1e-4, trained for 1500–2000 steps. Evaluation methodology combines automated perceptual metrics (LPIPS divergence from baseline FLUX outputs, FID against curated hook reference set) with human physiological validation using webcam-based GSR approximation and eye-tracking fixation mapping. The hypothesis is that a specialized LoRA will increase Inter-Subject Correlation (ISC) of generated hook frames by 40–60% compared to prompt-only generation, as measured by viewer fixation convergence in A/B testing. This research directly addresses the CMF pipeline's Hook Zone architecture from the Gaze Cueing framework and the Carousel Physiological State Architecture's Stage 1 "Recognition-Arousal" requirement, where warm high-saturation colors and bold compositional elements must trigger alpha wave desynchronization in the viewer's prefrontal cortex within the first swipe.

**Pipeline Integration:** Outputs feed directly into GMG Expert 01 (Neo-Schematic Architect) and CAC Composer (Vogue Living Edition) as T2I first-generation, then into Wan 2.2 for I2V motion.

**Dataset Strategy:** 70% curated real photography (editorial advertising hooks, film title cards, high-ISC documentary frames) + 30% FLUX 2 Dev inpainting augmentations with controlled CCT/contrast variations. Zero faceswap-generated images.

---

## PROPOSAL 2: Corrugator Suppression Lighting LoRA — Training Deterministic Facial Illumination Patterns for Measurable fEMG Corrugator Supercilii Inhibition

### Abstract

This proposal examines the feasibility of training a FLUX 2 Dev LoRA adapter specialized in generating facial close-up illumination patterns that produce documented corrugator supercilii inhibition — the physiological marker of comfort, openness, and trust measured via facial electromyography (fEMG). The Physiological State Specification Language (PSSL) establishes that specific lighting parameters (CCT 2700–3000K, illuminance equivalent of 750 lux, soft-edge shadow transitions with opacity below 30%) produce this measurable relaxation response in the corrugator muscle region. However, current diffusion models, including base FLUX 2 Dev, cannot reliably reproduce these precise lighting specifications from text prompts alone — they converge on generic "soft lighting" that lacks the directional specificity required for physiological targeting. The proposed LoRA is trained on a curated dataset of 600–900 portrait photographs exhibiting Rembrandt and loop lighting patterns at precisely controlled color temperatures, sourced from editorial portrait photography, therapeutic environment documentation, and cinematographic reference frames matching the "Processing" mood state from the Cinematographic Emotional Grammar Framework (high-angle 45° key light, monochromatic warm scheme). Each training image is annotated with measured or estimated CCT, fill ratio, and shadow edge hardness. The LoRA rank is set at 16–32 (lower rank since the target domain is narrower than Proposal 1), with training at 1e-4 learning rate for 1000–1500 steps. Validation employs both automated metrics (color temperature consistency measured via white-balance analysis of generated outputs, shadow gradient softness via edge detection) and physiological benchmarking against the PSSL's corrugator suppression targets. The Cinematographic Grammar's CGCS taxonomy provides the ground truth mapping: "Processing" state lighting must produce measurable comfort responses distinct from "Escape" (backlighting) and "Status" (chiaroscuro) states. This LoRA directly serves the CAC Composer's Vogue Living editorial photography pipeline, where Section 4 (The Atmosphere) requires motivated, directional lighting that passes the "Silence Test" — generated frames must feel weighted, private, and still, not bright, chaotic, or commercial.

**Pipeline Integration:** Primary use in CAC Composer W2 (PAIN arc), W3 (SOLUTION arc) scenes. Stacks with Coach Brand Face LoRA (06) at 0.4/0.7 weight ratio.

**Dataset Strategy:** 60% curated Rembrandt/loop-lit portraits from editorial photography + 25% therapeutic/counseling environment photography + 15% FLUX 2 Dev inpainting augmentations varying CCT from 2500K–3200K. All images annotated with estimated CCT and fill ratio.

---

## PROPOSAL 3: Gaze Vector Authority LoRA — Training CBCS-Adaptive Facial Orientation for Reflexive Attention Direction in Conversion-Centric Visual Design

### Abstract

This proposal presents research into a LoRA adapter that trains FLUX 2 Dev to generate coach portrait compositions with precise, controllable gaze vectors aligned to the Conscious Behavioral Change Score (CBCS) framework's audience temperature model. The Gaze Cueing research paper (building on Frischen, Bayliss & Tipper's 2007 meta-analysis) documents an 18.2-millisecond reflexive attention shift triggered by perceived gaze direction — a pre-conscious orienting response that occurs before the viewer can voluntarily redirect attention. Current T2I models overwhelmingly generate front-facing "authority poses" where the subject gazes directly at camera, creating what the Gaze Cueing framework identifies as the "Face Priority Trap": 100% of viewer fixation consumed by the face, zero fixation reaching the Hook Zone (text/message area) or Action Zone (CTA). The proposed LoRA trains FLUX 2 Dev on 500–800 images of 3/4 profile portraits where the subject's head is turned 20–45 degrees off-axis while their eye gaze vector is directed 15–30 degrees toward a compositional target zone. The dataset is segmented into three CBCS tiers: Cold audience (CBCS 0–3, gaze toward Hook Zone), Warm audience (CBCS 4–7, mild gaze offset toward social proof elements), and Hot audience (CBCS 8–10, gaze toward Action Zone/CTA). Each image is tagged with measured head-turn angle, eye-gaze offset angle, and the compositional zone being targeted. FLUX 2 Dev's VLM backbone (Mistral-3 24B) enables prompt-level control over which CBCS tier to activate at inference time, while the LoRA provides the geometric precision that text prompts alone cannot achieve. Training uses rank 32, learning rate 1e-4, 1200–1800 steps. Validation measures gaze vector accuracy via automated facial landmark detection (MediaPipe Face Mesh) on generated outputs, comparing actual eye-gaze angle against target angle per CBCS tier. A/B testing with eye-tracking quantifies whether Hook Zone fixation increases by the predicted 35–50% when using the LoRA versus prompt-only generation.

**Pipeline Integration:** Activated across all CCF visual recipes (dopamine-cliff-carousel, relief-peak-carousel, storytelling-archetypes) wherever coach faces appear in carousel slides. Weight modulated by CBCS score: 0.8 for cold, 0.3 for warm, 0.6 for hot.

**FLUX Klein 9b Integration:** Post-generation pose refinement using ControlNet pose transfer — if the LoRA output's gaze angle deviates >5° from target, Klein 9b ControlNet applies corrective inpainting to the eye region only, preserving the rest of the composition. This two-pass pipeline (FLUX 2 Dev LoRA generation → Klein 9b ControlNet correction) achieves sub-3° gaze accuracy.

---

## PROPOSAL 4: PAD-Driven Cinematic Color Grade LoRA Pair — Training Pleasure-Arousal-Dominance Emotional Color Spaces for Deterministic Mood State Induction

### Abstract

This proposal investigates the training of a paired LoRA system (two complementary adapters) on FLUX 2 Dev that implements the Pleasure-Arousal-Dominance (PAD) emotional model as deterministic color grading. The Cinematographic Emotional Grammar Framework's Color-Grammar Correlation System (CGCS) establishes that specific lighting/color parameters map to four discrete psychological states: Processing (warm monochromatic, high-angle diffused), Escape (backlighting, golden hour, long shadows), Discovery (mixed temperature, high saturation, cool-warm tension), and Status (desaturated chiaroscuro, cool temperatures above 5000K, low fill ratios 1:6 to 1:8). These four states correspond to specific PAD vectors measurable via the Self-Assessment Manikin (SAM) scale: Status maps to high Dominance, Escape maps to high Valence with moderate Arousal, Processing maps to low Arousal with moderate Valence, and Discovery maps to high Arousal. Current FLUX 2 Dev generation treats color grading as aesthetic decoration — prompts like "cinematic color grade" or "warm tones" produce unpredictable, distribution-average results that fail to target specific PAD coordinates. The proposed LoRA pair consists of: **(A) Steel Authority Grade** trained on 400–600 images exhibiting high-Dominance visual parameters (desaturated blue-grey-charcoal palette, 2–3 hue maximum, overhead top-lighting with deep eye socket shadows, fill ratios 1:6–1:8, alpha desynchronization-targeting CCT ≥ 6500K); and **(B) Warm Intimacy Grade** trained on 400–600 images exhibiting high-Valence parameters (2700–3200K golden hour backlighting, rim-light subject separation, long diffuse shadows, luminous skin rendering). The two LoRAs are designed for weighted stacking: at inference, the prompt selects which PAD vector to target and the pipeline applies the corresponding LoRA at 0.5–0.8 weight, optionally blending both for "Discovery" state (high Arousal) by applying both at 0.3 each. Training protocol: rank 16 per adapter (intentionally low to prevent cross-contamination), 800–1200 steps at 1e-4 learning rate. Evaluation uses automated colorimetry (histogram analysis of generated outputs for hue range, saturation distribution, and estimated CCT) benchmarked against CGCS ground truth tables.

**Pipeline Integration:** These LoRAs are the color backbone for the entire CMF and CCF pipeline. Steel Authority serves the MECHANISM arc (GMG Expert 01's "Status" domain palette). Warm Intimacy serves the PAIN arc's vulnerability scenes (CAC Composer W1–W2). Both are referenced in the 16-LoRA stacking protocol.

**Dataset Strategy:** Real-source-only for both sets. Steel Authority: Vogue editorial, Godfather-style cinematography, corporate authority photography. Warm Intimacy: Golden Hour editorial, Kodak Portra aesthetic photography, candlelit portraiture. No AI-generated images in training sets — the LoRA must learn from authenticated color science, not from other models' color approximations.

---

## PROPOSAL 5: GMG Expert 03 Collage Consistency LoRA — Training Style-Locked Mixed-Media Stick Figure Generation for Biological Motion Perception Fidelity

### Abstract

This proposal addresses a documented production quality failure in the CMF pipeline's GMG Expert 03 (The Emotional Animator) by training a FLUX 2 Dev LoRA specifically for the mixed-media stick figure + photorealistic cutout collage style. The GMG Expert 03 Visual Standards knowledge item documents persistent consistency failures: stick figure color drift between scenes, border style inconsistency (some frames gain borders, others lose them), and paper texture variation that breaks the visual continuity required for the brain's biological motion perception system to maintain activation. Neurocinematics research demonstrates that stylized biological motion (even in stick figures) activates the motor and premotor cortex through Inter-Subject Correlation — but this mirroring mechanism requires consistent visual identity across sequential frames. When the stick figure's proportions, color fill, or outline weight vary between frames (as happens with prompt-only generation), the viewer's brain treats each frame as a new character, destroying the parasocial engagement that GMG Expert 03 depends on. The proposed LoRA is trained on 300–500 purpose-built mixed-media images following GMG Expert 03's strict specifications: simple stick figure anatomy (circle head ~20% of height, oval torso, stick limbs), single duotone fill from the emotional state palette (Muted Blue-Grey #6B7B8C for pain, Vibrant Teal #0D7377 for joy, etc.), brush-stroke outline of 2–4px in a darker shade, minimal face (two dots for eyes, single curved line for mouth), and interaction with exactly one photorealistic PNG cutout object on a paper-textured background. The dataset includes all 12 core poses (SLUMPED, COLLAPSED, CRUSHED, HUNCHED, FROZEN, SINKING, TRIUMPHANT, OPEN, REACHING, DANCING, STANDING TALL, EMBRACING) across all 6 emotional-state color palettes, ensuring the LoRA encodes the complete pose × color matrix. Training rank is set at 48–64 (higher rank to capture the complex multi-layered aesthetic), 2000–2500 steps at 8e-5 learning rate. Validation measures cross-frame consistency using structural similarity (SSIM) between sequential stick figure generations, color histogram variance across the emotional palette, and outline weight consistency via edge-detection analysis.

**Pipeline Integration:** This LoRA is the backbone of all GMG Expert 03 scenes in the CMF pipeline. It enables consistent T2I generation of the "Last Frame" (Phase A), which then feeds into I2I for the "First Frame" (blank paper) and I2V for the 3-keyframe animation. Without this LoRA, each T2I call produces a visually different stick figure, breaking the 5-second micro-story's narrative coherence.

**FLUX Klein 9b Integration:** Post-generation, Klein 9b handles two critical editing tasks: (1) Background removal of the photorealistic cutout object to ensure transparent PNG quality, and (2) Inpainting corrections if the stick figure's outline weight or color fill deviate from spec. The Canva Clone interface exposes these as one-click editing tools: "Fix outline weight," "Correct figure color," "Remove background from cutout."

---

## PROPOSAL 6: Carousel Somatic Arc Chromatic Transition LoRA — Training Matched Achromatic-to-Chromatic Composition Pairs for Prefrontal Cortex Activation in Swipe-Based Content

### Abstract

This proposal presents research into a novel LoRA training methodology for FLUX 2 Dev that generates matched composition pairs across chromatic states — enabling the neurologically validated achromatic-to-chromatic transition effect documented in the Carousel Physiological State Architecture research paper. The research establishes that presentations transitioning from achromatic (grayscale) to chromatic (full-color) conditions produce significantly greater neural activation in the prefrontal cortex and orbitofrontal cortex compared to presentations in the reverse direction or in static chromatic conditions. This neurocognitive effect directly applies to carousel-format social media content: a carousel where the visual narrative "blooms into color" across swipes (Slides 1–2 in desaturated grayscale, Slides 3–4 in muted transitional tones, Slide 5 in full vibrant saturation) leverages this PFC activation pathway for maximum engagement and emotional peak. Training a LoRA for this purpose is non-trivial because the model must learn to generate the same compositional elements (same subject pose, same environment, same spatial relationships) at three discrete chromatic states while maintaining structural identity. The proposed dataset consists of 400–600 composition triplets: each triplet contains (A) a fully desaturated/achromatic version, (B) a muted partially-chromatic version at ~40% saturation, and (C) a fully-saturated high-chromatic version. The triplets are constructed from real editorial photography by creating controlled desaturation variants from color originals, ensuring compositional identity across the three states. The LoRA is trained with a conditioning token system: `[ACHRO]`, `[TRANSITIONAL]`, and `[CHROMATIC]` tokens control which chromatic state is generated for a given composition. Training uses rank 48, learning rate 5e-5, 2500–3000 steps (higher step count due to the paired-generation complexity). Additionally, the LoRA encodes the PAD-aligned color logic from the Carousel Architecture research: warm reds and oranges dominate the "Peak" (full-chromatic) slides to maximize positive valence, while cool blues and greens appear in "Resolution" (post-peak) slides. The Peak-End Rule is enforced: the final slide must achieve maximum positive valence through highest saturation combined with warmest emotional tone, targeting zygomaticus major activation (genuine smile response). Validation measures compositional consistency across chromatic triplets using structural similarity (SSIM ≥ 0.85 between achromatic and chromatic versions), saturation accuracy per state using HSV histogram analysis, and A/B engagement testing comparing chromatic-arc carousels against flat-chromatic controls.

**Pipeline Integration:** This LoRA spans the entire CCF visual recipe system. In the Dopamine Cliff Carousel recipe, the chromatic arc maps to: Slides 1–2 (aspirational, polished) at full chromatic → Slide 3 (the cliff, reality shock) at achromatic → Slides 4–5 (recovery, path forward) transitioning back to chromatic. In the Relief Peak Carousel, the progression is: Slides 1–2 (struggle validation) at achromatic → Slide 3 (relief peak, breakthrough) at full chromatic → Slides 4–5 (empowered action) at sustained chromatic. The Storytelling Archetypes recipe uses the arc most flexibly, mapping chromatic state to the emotional escalation structure (setup → rising → climax → resolution).

**FLUX Klein 9b Integration:** Klein 9b performs post-generation saturation correction for slides that need precise chromatic values. The Canva Clone interface exposes a "Chromatic Arc Slider" that lets the coach preview the desaturation-to-saturation transition across carousel slides before export, with Klein 9b inpainting corrective adjustments in real-time.

---

## PROPOSAL 7: Coach Brand Face Identity LoRA — Training Per-Coach Facial Individuation Adapters with Authenticity-Preserving Imperfection Encoding

### Abstract

This proposal addresses the most commercially critical LoRA in the CCP platform: per-coach facial identity adapters that enable consistent, trustworthy coach face generation across all visual pipeline outputs. The Brand Character System research paper identifies that "identity-critical visual features" for face individuation are hierarchically ordered: horizontal orientation energy (eyes and eyebrows) dominates as the highest diagnostic feature, followed by skin texture (pores, micro-gradients), then facial proportion geometry (corrugator geometry and zygomatic positioning). Critically, the AI Portrait Authenticity literature establishes that "perfect" AI-generated faces are paradoxically *less trustworthy* than textured, slightly imperfect reconstructions — Expression Naturalness (EN), Skin Texture (ST), and Facial Proportion (FP) are the top predictors of perceived authenticity, and sterile perfection activates uncanny valley detection mechanisms. The proposed LoRA training protocol for each coach uses 30–50 high-quality real photographs (70% of dataset) sourced across varied lighting conditions (natural daylight, golden hour, artificial interior, overcast), varied expressions (neutral, warm, serious, laughing, contemplative — covering Duchenne and non-Duchenne expressions), and varied angles (frontal, 3/4 profile left, 3/4 profile right, slight overhead, slight below). The remaining 30% of the dataset consists of FLUX 2 Dev inpainting augmentations where the coach's real face is contextually composited into varied environments (office, outdoor, stage, casual) with controlled lighting changes — never classic faceswap, which introduces artifact contamination (edge bleeding, lighting inconsistency, skin tone discontinuity) that trains the LoRA on errors rather than identity features. Each LoRA is trained at rank 8–16 (intentionally low rank: face identity is a narrow domain that risks overfitting), learning rate 1e-4, 500–800 steps. A critical training consideration specific to the CCP platform is PSSL compliance: the LoRA must accurately reproduce the coach's corrugator geometry (brow tension pattern) and zygomatic positioning (cheekbone-to-smile relationship), as these are the identity markers that trigger parasocial trust (PSR formation) documented in the Brand Character System paper. Validation combines automated face verification (ArcFace cosine similarity ≥ 0.75 between generated and real photographs), identity coherence testing (generating the same coach across 50 varied prompts and measuring face clustering consistency), and authenticity scoring (automated skin texture analysis ensuring micro-imperfections are preserved — pore visibility, subtle discoloration, expression asymmetry). The anti-uncanny protocol explicitly penalizes outputs that achieve "too perfect" skin renders by measuring the standard deviation of skin luminance in facial regions: authentic faces show σ ≥ 12 (micro-variation from pores, capillaries, uneven pigmentation), while AI-perfect faces show σ < 8.

**Pipeline Integration:** This LoRA is the identity backbone for all coach-facing visual content across both CMF and CCF pipelines. In CMF: CAC Composer requires the compressed anchor to match the coach's real appearance. In CCF: all 14 visual recipes (dopamine-cliff-carousel through worst-case-scenario) inject the Character Anchor into every slide prompt. The per-coach LoRA ensures that the Character Anchor isn't just text — it's baked into the model's latent space, making identity consistency automatic rather than prompt-dependent. This LoRA stacks with all other pipeline LoRAs at 0.4–0.5 weight (lower weight to prevent identity features from overwhelming compositional LoRAs).

**FLUX 2 Dev Multi-Reference Synergy:** FLUX 2 Dev's native multi-reference composition capability (2–10 reference images) is leveraged alongside the LoRA for maximum identity fidelity. At inference, the pipeline provides 3–5 real coach photos as reference images *plus* activates the trained LoRA — the multi-reference system handles per-instance consistency while the LoRA encodes learned identity priors that persist even when reference images are not provided. This hybrid approach (LoRA + multi-reference) achieves higher identity fidelity than either method alone.

**FLUX Klein 9b Integration:** Post-generation, Klein 9b provides critical identity-preserving editing: background removal for clean coach portraits, text overlay removal if the model hallucinates text artifacts near the face, and targeted inpainting for expression correction (e.g., adjusting a generated smile to match the exact Duchenne characteristics of the coach's real smile). The Canva Clone exposes these as "Identity-Preserving Edit" tools with automatic face-region masking.

**Cost Model:** $4 per coach (compute cost for 500–800 steps on quantized FLUX 2 Dev). Storage: ~10MB per LoRA adapter. This directly integrates with the CCP's $4/user metered CBCS billing system — the LoRA training cost is absorbed into the per-client onboarding fee.

---

## Cross-Proposal Integration Matrix

| Proposal | Primary Pipeline Target | Stacks With | CBCS Sensitivity |
|---|---|---|---|
| 1. Somatic Hook | Hook Zone (all recipes, GMG Expert 01) | 3, 4A, 7 | Cold (0–3) |
| 2. Corrugator Suppression | PAIN arc (CAC Composer W2–W3) | 4B, 7 | Warm (4–7) |
| 3. Gaze Vector Authority | All coach-face content (CMF + CCF) | 1, 7 | All tiers (weight varies) |
| 4. PAD Color Grade Pair | Color backbone (all pipelines) | 1, 2, 5, 6 | N/A (mood-driven) |
| 5. GMG 03 Collage | GMG Expert 03 scenes (CMF) | 4 (for color) | N/A (style-driven) |
| 6. Chromatic Arc | Carousel recipes (CCF) | 4, 7 | N/A (format-driven) |
| 7. Coach Brand Face | All coach visual content | ALL | All tiers |

---

## Recommended Training Order

```
WEEK 1 — Platform Launch Blockers:
├── Proposal 7: Coach Brand Face (per-coach, must exist before any content)
├── Proposal 4: PAD Color Grade Pair (color backbone for all content)
└── Proposal 1: Somatic Hook Architecture (hook frames for all formats)

WEEK 2 — Full Pipeline Activation:
├── Proposal 3: Gaze Vector Authority (all coach-face compositions)
├── Proposal 2: Corrugator Suppression (vulnerability/trust scenes)
└── Proposal 5: GMG 03 Collage (motion graphics pipeline)

MONTH 2 — Carousel Optimization:
└── Proposal 6: Chromatic Arc Transitions (carousel engagement boost)
```

---

## Note on Wan 2.2 (Video)

Wan 2.2 is used **at inference only** for I2V (image-to-video) generation. The LoRA-generated T2I outputs from FLUX 2 Dev serve as the input frames for Wan 2.2's motion synthesis. No LoRA training is recommended for Wan 2.2 because:

1. **Cost-prohibitive:** Video model LoRA training requires significantly more compute/VRAM than image model training, with diminishing returns for our use case (5-second clips with minimal body motion).
2. **Quality sufficient:** Wan 2.2's base model handles the motion specs required by our pipeline — CAC's "95% frozen body" with subtle environment motion (curtain sway, dust motes, steam) and GMG Expert 03's stick figure keyframe animation both fall within Wan 2.2's native capabilities.
3. **Motion is code-controlled:** The critical motion parameters (BODY_STRENGTH 0.15–0.25, ENVIRONMENT_STRENGTH 0.35–0.50) are controlled via inference-time prompt engineering, not model weights.

## Note on FLUX Klein 9b (Editing)

FLUX Klein 9b is positioned as the **post-generation editing layer** in the Canva Clone interface, handling:

- **Background Removal:** One-click subject isolation for carousel slides and social media assets
- **Text Removal:** Clean removal of hallucinated text artifacts from FLUX 2 Dev LoRA outputs
- **Inpainting:** Targeted region editing (expression correction, color fix, accessory addition/removal)
- **ControlNet Pose Transfer:** Precise pose refinement using OpenPose/DWPose ControlNet adapters for gaze angle correction (Proposal 3 integration) and body posture adjustment
- **Outpainting:** Canvas extension for format adaptation (9:16 vertical to 1:1 square crop with generated fill)

> [!TIP]
> Canva has not implemented AI-native inpainting/editing because their business model is template-driven, not generation-driven. Our Canva Clone's competitive advantage is precisely this: generation-first (FLUX 2 Dev LoRA output) + editing-second (Klein 9b ControlNet/inpainting), creating a pipeline that Canva's architecture cannot replicate without rebuilding their entire rendering engine.
