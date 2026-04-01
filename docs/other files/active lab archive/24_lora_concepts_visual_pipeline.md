# LoRA Strategy — Research-Grounded Visual Pipeline
## Revised from CVE + CPSC Research Papers

> [!IMPORTANT]
> This revision integrates 8 research papers from the CVE + CPSC lab. Every LoRA now has a **scientific justification** linked to a documented psychological mechanism, not just an aesthetic preference.

---

## The Core Insight: LoRAs Are Not Style — They Are Physiological Engineering

The **Physiological State Specification Language (PSSL)** paper establishes that visual grammar must be *deterministic*, not descriptive. Generic prompts like "cinematic" cause the diffusion model to converge on training distribution averages (mode collapse). A LoRA trained on a precise visual grammar specification — specific CCT (Kelvin), gaze angle, shadow opacity — steers generation *away* from the statistical average and toward a **measurable somatic state** in the viewer.

**AGSS (Anti-Generic Specificity Scale):** The PSSL defines 4 levels of diagnostic accuracy. Our LoRAs target Level 3 (fEMG/SCR-verified physiological response) and Level 4 (brand uniqueness / latent space distance from generic training distribution).

---

## MCDA Revised — Research-Grounded Scoring

Each LoRA is evaluated on 4 criteria weighted by research evidence:

| Criteria | Weight | Source |
|---|---|---|
| **Physiological Impact** — does it target a documented somatic state? | 35% | PSSL, Neurocinematics |
| **Anti-Generic Specificity** — does it solve model drift/mode collapse? | 30% | PSSL (AGSS), Cinematographic Grammar |
| **Pipeline Gap** — does it address a documented production failure? | 25% | CMF Pipeline, GMG Standards |
| **Training ROI** — unique vs promptable in 2026 FLUX? | 10% | MCDA practical |

---

## FINAL LIST: 16 LoRAs (from 24) — Research Priority Order

### 🔴 TIER 1: Launch Blockers (Train Before First Delivery)

---

#### LoRA 01 — Somatic Hook Architecture
**Replaces:** "Hook Punch" (too vague)

**Research justification:**
- Neurocinematics: The first 3 seconds must trigger the **ventral attention network** through high-contrast visual saliency to lock ISC. Hasson (2008) shows that structured hooks → 65% ISC vs. random content → 5% ISC.
- PSSL: CCT ≥ 6500K + high-contrast center-frame element = measurable phasic GSR spike (sympathetic arousal).
- Carousel Architecture: Stage 1 = "Recognition-Arousal" requires warm high-sat colors + bold serif font to trigger Alpha wave desynchronization.

**Training spec:**
- Warm high-contrast foreground (red/amber palette)
- Subject at visual center, upper-left key lighting
- High shadow opacity (70-80%)
- Coach face: direct or slightly averted gaze (per CBCS cold audience = Hook Zone)

**AGSS target:** Level 4 — pulls away from generic "motivational quote" training distribution

---

#### LoRA 02 — Corrugator Suppression / Compassionate Close-Up
**Replaces:** "Compassionate Close-Up" (PRIMAL-driven)

**Research justification:**
- PSSL: 3000K CCT + 750lx-equivalent + soft-edge shadows = documented **corrugator supercilii inhibition** (the biological marker of comfort and openness). This is the PAIN arc scene physiological target.
- Cinematographic Grammar: "Processing" mood state requires high-angle (45°) key light, monochromatic warm scheme, shadow opacity <30%.
- Neurocinematics: Facial close-ups produce **peak ISC** across viewers via fusiform gyrus + amygdala activation.

**Training spec:**
- 2700–3000K warm fill (golden hour equivalent)
- Soft-edge shadows, no hard fills
- Face-forward or slightly downward gaze (-5 to -10 degrees)
- Eye contact: direct (Trust/Credibility mode — per Gaze Cueing paper)

**AGSS target:** Level 3 — fEMG corrugator suppression

---

#### LoRA 03 — Gaze Vector Authority (Cold Audience Hook Direction)
**New LoRA — from Gaze Cueing research**

**Research justification:**
- Gaze Cueing paper (Frischen, Bayliss & Tipper 2007): Gaze-cueing effect = **18.2ms reflexive attention shift** within 50ms of face exposure. Face facing left + gaze directed RIGHT toward text = highest fixation on Hook Zone.
- FR54 Compiler logic: Cold audience (CBCS 0-3) = gaze must be directed at Hook Zone. Variant Alpha (Hook-Directed) is required.
- The LoRA trains FLUX to generate authority poses where the coach's face is **3/4 profile, gaze offset toward text zone**, preventing "Face Priority Trap" (entire fixation on face, zero fixation on message).

**Training spec:**
- Coach face: 3/4 profile (left or right), head turn 20-45 degrees off-axis
- Gaze direction: clearly averted toward Hook Zone (15-30 degree off-axis eye vector)
- Body facing camera, head offset = maximum gaze vector clarity
- High-contrast rim lighting for separation

**AGSS target:** Level 4 — eliminates deadzone face-forward authority pose from training distribution

---

#### LoRA 04 — PAD Arousal Grade (Steel Authority / Steel Blue)
**Replaces:** "Steel Authority Grade"

**Research justification:**
- Cinematographic Grammar: "Status" psychological state → desaturated/monochromatic palette, cool temps (>5000K), **high-opacity inky shadows, chiaroscuro** → high dominance on SAM scale.
- PAD model (Pleasure-Arousal-Dominance): Steel blue + low saturation + top/Godfather lighting → High Dominance vector. This is the MECHANISM arc color target.
- PSSL: 6500K CCT + low fill ratio (1:8) = measured alpha desynchronization + increased sympathetic arousal.

**Training spec:**
- Color palette: deep blue, slate, charcoal (2-3 hue range maximum)
- Key light: top/overhead (Godfather style) — deep eye socket shadows
- Fill ratio: minimal (1:6 to 1:8)
- Background: near-black or dark gradient, high luminance ratio (subject:background)

---

#### LoRA 05 — PAD Valence Grade (Warm Intimacy / Golden Healing)
**Replaces:** "Warm Intimacy Grade"

**Research justification:**
- Cinematographic Grammar: "Escape" psychological state → backlighting/rim light, golden-hour temp, long diffuse shadows → high valence / low-moderate arousal per SAM.
- Carousel Architecture: "Physiological Exhale" (Stage 4) uses cool-to-warm transition + parasympathetic recovery signals.
- PAD model: warm amber/gold palette activates approach-motivated arousal in healing contexts.

**Training spec:**
- 2700–3200K golden hour
- Backlighting / rim lighting to create luminous subject separation
- Long, diffuse shadows (soft edges)
- High luminance ratio subject:background (silhouette potential)

---

#### LoRA 06 — Coach Brand Face (Per-Coach — Identity Lock)
**Kept as-is, scientifically upgraded**

**Research justification:**
- Brand Character System: "Identity-critical visual features" = **horizontal orientation energy (eyes/eyebrows)** is the highest diagnostic feature for face individuation. Skin texture (pores, gradients) = primary authenticity predictor.
- AI Portrait Authenticity study: Expression Naturalness (EN) + Skin Texture (ST) + Facial Proportion (FP) are top predictors. "Perfect" AI faces are *less trustworthy* than textured, slightly imperfect ones.
- PSSL: The LoRA must teach the model to reproduce the coach's **corrugator geometry** and **zygomatic positioning** accurately — these are identity-level markers that trigger parasocial trust (PSR formation).

**Training spec:**
- 30-50 real images of coach (70%) + FLUX inpainting augmentations in varied environments (30%)
- ZERO classic faceswap in training set — artifact contamination risk
- Emphasize varied expressions (neutral, warm, serious, laughing)
- Diverse lighting conditions essential for robust identity persistence

---

### 🟠 TIER 2: Month 2 — High Research ROI

---

#### LoRA 07 — Tribal Imagen Visual Hook (Per-Coaching-Tribe)
**New LoRA — from Tribal Imageability research**

**Research justification:**
- Tribal Imageability paper: High-TIRS nouns trigger **gamma-band ignition** (30-70Hz) in tribe members = identity-level recognition ("That is exactly who I am"), producing longer fixation durations and higher affective valence vs generic nouns ("I do that").
- This LoRA trains FLUX on **visual compositions where tribe-specific imagery is foregrounded**: conscious business coaches → resonance/wholeness imagery; high-performance → leverage/optimization iconography; healing → somatic/breakthrough light imagery.
- Shannon entropy tracking: the LoRA's image targets must be refreshed when tribal imageability bleaches (corporatization).

**Training spec:**
- Tribe-specific: 4 variants (conscious business, high-performance, healing, financial freedom)
- Images must contain high-charge tribal visual metaphors — not generic inspirational stock
- Composition: tribal nouns/imagery in Hook Zone of visual frame (per Gaze Cueing architecture)

---

#### LoRA 08 — Neurocinematic Vulnerability Arc (Emotional Anchoring)
**Replaces:** "Environmental Isolation" + "Proof of Life" merged

**Research justification:**
- Neurocinematics: Strategy 2 "Emotional Anchoring" requires **slow pacing, facial close-ups, DMN activation** to achieve top-down neural synchrony. This targets amygdala + default mode network for emotional stickiness.
- ISC data: Emotional face close-ups with relatable body language = peak ISC. The PAIN scene requires 15-30 second slow-paced emotional depth.
- Visual Style Psychology: "Warm Audiences" (high TII) need illustrated or semi-realistic styles — but for video/image, the equivalent is lower depth-of-field, soft focus on background, emotional foreground emphasis.

**Training spec:**
- Subject in soft, intimate environment (not studio)
- Background: significantly defocused (f/1.4–2.0 equivalent depth)
- Lighting: warm Rembrandt (one-sided 45°) — maximum facial texture visible
- Expression: genuine vulnerability (orbicularis oculi activation — Duchenne micro-expression)

---

#### LoRA 09 — GMG-03 Collage / Stick Figure Consistency
**Kept — highest priority GMG LoRA**

**Research justification:**
- GMG Expert 03 Visual Standards KI: documented consistency failures — stick figure color drift, border inconsistency. This is a **production quality gate failure** not solvable via prompting alone.
- Neurocinematics: Biological motion (even stylized) activates motor/premotor cortex ISC — the stick figure must maintain consistent proportions for this mirroring mechanism to function.
- Brand Character System: "Learning variability" in brand character training (Phase 1) = high variability improves audience's ability to "tell faces together" later. The LoRA establishes the canonical GMG style before introducing variation.

**Training spec:**
- Stick figures: black/very dark charcoal, no borders
- Cutout collage elements: consistent paper texture, no digital glow
- Movement lines: consistent weight and style
- Must maintain style on white, black, and colored CMF backgrounds

---

#### LoRA 10 — Symbolic GMG Metaphor (Mechanism Arc)
**Replaces:** "GMG-04 Symbolic/Surrealist" — research upgraded

**Research justification:**
- Tribal Imageability: High-TIRS visual metaphors trigger identity-level recognition ("gamma ignition") — surrealist visual metaphors for coaching tribes must be *specific*, not generic.
- Neurocinematics: Narrative structure dramatically outperforms non-narrative montage for ISC. The mechanism arc metaphor must sustain a **causal narrative logic** (A causes B causes C) to engage the DMN.
- PSSL: "Symbolic Architect" expert must produce scenes with high semantic coherence (neuroaesthetics finding: semantically coherent images are processed in the prefrontal cortex via text-trained pathways — meaning visual metaphors must be linguistically grounded).

---

#### LoRA 11 — Carousel Somatic Arc Chromatic Transitions
**New LoRA — from Carousel Architecture research**

**Research justification:**
- Carousel Architecture: **Achromatic-to-chromatic transition** (Condition A) → significantly greater PFC and orbitofrontal cortex neural activation vs reverse. A carousel that "blooms into color" as the user swipes leverages this neurocognitive response.
- The LoRA trains FLUX to generate **matched achromatic variants** of the same composition for "Before" state (slide 1-2) and **high-saturation chromatic variants** for "Peak" state (slide 4-5).
- Peak-End Rule: The "Peak" slide must be optimized for maximum positive valence → highest saturation, warmest emotional tone, maximum zygomaticus activation target.

**Training spec:**
- Paired dataset: same composition × 3 chromatic states (grayscale → muted → full-saturation)
- Warm reds/oranges for Peak slides
- Cool blues/greens for Resolution slides
- Must maintain composition consistency across chromatic variants

---

#### LoRA 12 — CAC Still Life Witness (Ambient Cinema)
**Kept — confirmed by PSSL research**

**Research justification:**
- PSSL: "Escape" mood state (Immersion & Transcendence) → backlighting + golden hour + long diffuse shadows + high luminance ratio. Still life ambient scenes with **first-person perspective (1PP)** produce stronger autonomic arousal (SCR spike) than third-person.
- Neurocinematics: The 95% frozen body El Shaddai spec is neurologically justified — **unedited long takes promote superior emotional coherence via sustained amygdala activation**, compensating for the loss of cut-based theta synchronization.

---

#### LoRA 13 — Electric Breakthrough Grade (PAD Activation)
**Kept — confirmed by research**

**Research justification:**
- PAD + Carousel: "Empowerment" resolution targets the **nucleus accumbens (NAcc)** — the brain's central reward structure. High-energy electric palette (electric blue, vivid yellow, bright white) is the visual correlate of the emotional "chills" or conflict resolution = increased NAcc activity.
- "Happy Face Advantage": Empowerment expressions are recognized faster than neutral or fearful — this color grade must accompany the coach's most confident/breakthrough expression in the CLOSE arc.

---

#### LoRA 14 — Film Grain / Analog Texture (Authenticity Signal)
**Kept — research validated**

**Research justification:**
- Brand Character System: "Technical flaws in real film are often tolerated as signs of authenticity, whereas even minor anomalies in synthetic film are interpreted as evidence of unreality." Analog grain = **anti-uncanny signal**.
- AI Portrait Authenticity: "Perfect AI visuals may be less trustworthy than imperfect but plausible reconstructions." Film grain is the lightest-touch intervention to prevent plastic AI skin artifacts.
- AGSS: Grain increases latent space distance from "clean AI output" training distribution = higher anti-generic specificity score.

---

#### LoRA 15 — Coach Color Palette (Per-Coach Brand Drift Prevention)
**Kept — scientifically upgraded**

**Research justification:**
- Cinematographic Grammar: "Color-in-Context" theory — hue meaning is inseparable from the lighting environment. A per-coach palette LoRA enforces **consistent CCT progressions** (warm-to-cool = rationalization arc; cool-to-warm = discovery arc) unique to each brand.
- Brand Character System: Cross-platform storytelling with consistent color = +30% engagement increase, +23% trust (documented).
- Anti-drift: Without a palette LoRA, FLUX will regress each coach's identity toward its training distribution's color average.

---

#### LoRA 16 — Narrative Universe Style Bridge (Cold→Warm Audience Style)
**New LoRA — from Visual Style Psychology research**

**Research justification:**
- Visual Style Psychology: **Optimal style is NOT fixed** — it is dynamic based on audience relationship depth (TII score).
  - Cold (TII 0-25): Cinematic Realism → credibility/expertise
  - Warm (TII 26-70): Semi-Realistic Digital → connection/trust  
  - Hot (TII 71+): Illustrated/Ghibli style → identity/transportation
- This LoRA trains FLUX on the **semi-realistic digital style** (Warm tier) — human proportions with subtle digital enhancement. Most coaches are producing for warm audiences but using cold-audience photorealism, leaving transportation value untapped.
- Brand Character System: NPR (non-photorealistic rendering) dampens arousal but provides **psychological safety** for processing challenging content — ideal for PAIN arc delivery to warm audiences.

---

## SKIPPED — Research Invalidated or Code-Level Solutions

| LoRA | Reason | Alternative |
|---|---|---|
| Sacred Threshold | Promptable in FLUX | GMG metaphor framing |
| Horizon Return | Low TIRS charge (generic "freedom" image) | PAD Valence Grade covers |
| GMG-02 Data Sculptor | Audience-dependent, low tribal charge | Coach-specific brand LoRA |
| GMG-05 Texture Poet | Promptable | PSSL lighting grammar |
| GMG-06 Kinetic Typography | Remotion handles this better | Remotion animation code |
| CAC Sacred Geometry | Generic — high Shannon entropy, bleached | Still Life Witness covers |
| CAC Urban Meditation | Promptable | Ambient Cinema covers |
| Cinematic Captions | Remotion code + font psychology | Typography rules in Remotion |
| Seamless Transitions | Remotion transitions | Code |
| Coach Visual DNA | Redundant with LoRA 06 + 15 | Merged |

---

## Training Priority Order

```
WEEK 1 (Before first delivery):
├── LoRA 06  Coach Brand Face (per coach — $4 per client)
├── LoRA 01  Somatic Hook Architecture
├── LoRA 04  PAD Arousal Grade (Steel Authority)
└── LoRA 05  PAD Valence Grade (Warm Intimacy)

WEEK 2 (Platform-level):
├── LoRA 02  Corrugator Suppression / Compassionate Close-Up
├── LoRA 03  Gaze Vector Authority
├── LoRA 09  GMG-03 Collage Consistency
└── LoRA 15  Coach Color Palette (per coach)

MONTH 2:
├── LoRA 07  Tribal Imagen Hook (per coaching tribe)
├── LoRA 08  Neurocinematic Vulnerability Arc
├── LoRA 10  Symbolic GMG Metaphor
├── LoRA 11  Carousel Somatic Arc Chromatic Transitions
├── LoRA 12  CAC Still Life Witness
├── LoRA 13  Electric Breakthrough Grade
├── LoRA 14  Film Grain / Analog Texture
└── LoRA 16  Narrative Universe Style Bridge
```

---

## LoRA Stacking Protocol (Research-Based)

At inference time, stack multiple LoRAs per scene type with weighted application:

| Scene Type | Stack | Weights |
|---|---|---|
| **HOOK (PAIN arc, cold audience)** | Somatic Hook (01) + Steel Authority (04) + Coach Brand (06) + Film Grain (14) | 0.8 / 0.5 / 0.4 / 0.3 |
| **VULNERABILITY (PAIN arc, warm)** | Corrugator Suppression (02) + Warm Intimacy (05) + Coach Brand (06) + Tribal Hook (07) | 0.7 / 0.6 / 0.4 / 0.5 |
| **MECHANISM (authority)** | Steel Authority (04) + Gaze Vector (03) + Symbolic GMG (10) + Coach Palette (15) | 0.7 / 0.6 / 0.8 / 0.4 |
| **CLOSE (conversion)** | Electric Breakthrough (13) + Coach Brand (06) + Film Grain (14) + Gaze Vector (03) | 0.7 / 0.5 / 0.2 / 0.5 |
| **CAROUSEL Hook Slide** | Somatic Hook (01) + Carousel Chromatic (11) achromatic variant | 0.9 / 0.7 |
| **CAROUSEL Peak Slide** | Tribal Hook (07) + Carousel Chromatic (11) full-saturation + Breakthrough (13) | 0.8 / 0.8 / 0.5 |

**CBCS-Adaptive Gaze Rule (per Gaze Cueing paper):**
- CBCS 0-3 (Cold): LoRA 03 active → gaze toward Hook Zone
- CBCS 4-7 (Warm): LoRA 03 at 0.3 weight → mild gaze offset toward social proof
- CBCS 8-10 (Hot): LoRA 03 at 0.6 weight → gaze toward Action Zone (CTA)

---

## Cost Estimate

| Category | Count | Cost/Unit | Total |
|---|---|---|---|
| Platform LoRAs (01-05, 07-16) | 14 | ~$3 | ~$42 one-time |
| Per-Coach Brand Face (06) | Per coach | ~$4 | $4/coach |
| Per-Coach Color Palette (15) | Per coach | ~$1 | $1/coach |
| Storage | Pipeline | ~10MB/LoRA | ~150MB/coach |
