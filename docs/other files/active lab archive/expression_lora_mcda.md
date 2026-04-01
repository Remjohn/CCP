# Modular Expression LoRA Architecture: MCDA Analysis

> **Date:** 2026-03-29
> **Context:** CCP Visual Pipeline — Universal Expression Control Tools
> **Architecture:** Each LoRA is trained on diverse MetaHuman-rendered faces where ONLY ONE variable changes. At inference, they stack with any Coach Identity LoRA to compose precise emotional compositions.
> **Based On:** FACS (Facial Action Coding System), ARKit 52 Blendshapes, CCP Mood Intelligence Framework

---

## Part 1: The 16 Expression LoRA Candidates

Each LoRA maps to one or more FACS Action Units (AU). The ARKit blendshape column shows which MetaHuman sliders drive the training data.

| # | LoRA Name | FACS Action Units | ARKit Blendshapes Used | What It Controls |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `smile` | AU6 + AU12 | `mouthSmileLeft/Right`, `cheekSquintLeft/Right` | Full Duchenne smile (mouth + eye crinkle) |
| 2 | `gaze_vertical` | — | `eyeLookUpLeft/Right`, `eyeLookDownLeft/Right` | Eyes looking up or down |
| 3 | `gaze_horizontal` | — | `eyeLookInLeft/Right`, `eyeLookOutLeft/Right` | Eyes looking left or right |
| 4 | `brow_raise` | AU1 + AU2 | `browInnerUp`, `browOuterUpLeft/Right` | Raised eyebrows (surprise, openness, curiosity) |
| 5 | `brow_furrow` | AU4 | `browDownLeft/Right` | Furrowed brows (intensity, anger, focus) |
| 6 | `eye_squint` | AU6 + AU7 | `eyeSquintLeft/Right`, `cheekSquintLeft/Right` | Eye narrowing (warmth, Duchenne marker, sincerity) |
| 7 | `eye_wide` | AU5 | `eyeWideLeft/Right` | Eyes opening wide (shock, alertness, emphasis) |
| 8 | `jaw_open` | AU26 + AU27 | `jawOpen`, `mouthClose` | Mouth openness (speaking, surprise, gasp) |
| 9 | `lip_press` | AU24 | `mouthPressLeft/Right` | Lips pressed together (determination, restraint, resolve) |
| 10 | `mouth_frown` | AU15 | `mouthFrownLeft/Right` | Corners of mouth pulled down (sadness, disappointment) |
| 11 | `lip_pucker` | AU18 + AU22 | `mouthPucker`, `mouthFunnel` | Puckered/funneled lips (thought, kiss, "ooh") |
| 12 | `nose_wrinkle` | AU9 | `noseSneerLeft/Right` | Nose scrunched (disgust, playful scrunching) |
| 13 | `chin_raise` | AU17 | `mouthShrugLower` | Chin pushed up (defiance, holding back tears, pouting) |
| 14 | `dimpler` | AU14 | `mouthDimpleLeft/Right` | Cheek dimples (smirk, knowing smile, smugness) |
| 15 | `head_tilt` | AU55 + AU56 | Head rotation in MetaHuman (not blendshape — requires pose data) | Tilted head (empathy, curiosity, active listening) |
| 16 | `eye_moisture` | — | Post-processing: specular highlight on eye + subtle skin redness | Wet/glossy eyes (emotion, tears welling, vulnerability) |

---

## Part 2: MCDA Evaluation

### Scoring Criteria

| Criterion | Weight | Description |
| :--- | :--- | :--- |
| **Visual Impact** | 25% | How much does this LoRA change the perceived emotion of a PSSL close-up? |
| **Content Frequency** | 20% | How often will CCP content require this expression across all arcs? |
| **Training Feasibility** | 20% | Can MetaHuman cleanly isolate this variable? Is the data generation straightforward? |
| **Stack Compatibility** | 15% | Will this LoRA combine cleanly with others without bleeding? |
| **Competitive Moat** | 10% | Does this give CCP something no competitor has? |
| **Mood Intelligence Alignment** | 10% | Does this map to a specific emotional state in our Visual Frameworks? |

### Scoring Scale: 1 (Poor) → 5 (Exceptional)

### MCDA Scores

| # | LoRA | Visual Impact (25%) | Content Freq (20%) | Training Feasibility (20%) | Stack Compat (15%) | Competitive Moat (10%) | Mood Alignment (10%) | **Weighted Score** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `smile` | 5 | 5 | 5 | 5 | 4 | 5 | **4.85** |
| 2 | `gaze_vertical` | 5 | 5 | 5 | 5 | 5 | 4 | **4.90** |
| 3 | `gaze_horizontal` | 4 | 4 | 5 | 5 | 5 | 3 | **4.30** |
| 4 | `brow_raise` | 5 | 4 | 5 | 5 | 4 | 5 | **4.70** |
| 5 | `brow_furrow` | 5 | 4 | 5 | 5 | 4 | 5 | **4.70** |
| 6 | `eye_squint` | 5 | 5 | 4 | 4 | 5 | 5 | **4.70** |
| 7 | `eye_wide` | 4 | 3 | 5 | 5 | 3 | 4 | **4.05** |
| 8 | `jaw_open` | 4 | 4 | 5 | 4 | 3 | 3 | **3.95** |
| 9 | `lip_press` | 4 | 4 | 4 | 5 | 4 | 5 | **4.25** |
| 10 | `mouth_frown` | 4 | 3 | 5 | 5 | 3 | 5 | **4.15** |
| 11 | `lip_pucker` | 3 | 2 | 5 | 5 | 3 | 3 | **3.40** |
| 12 | `nose_wrinkle` | 3 | 2 | 5 | 5 | 3 | 3 | **3.40** |
| 13 | `chin_raise` | 4 | 3 | 4 | 4 | 4 | 5 | **3.95** |
| 14 | `dimpler` | 3 | 3 | 4 | 5 | 4 | 4 | **3.70** |
| 15 | `head_tilt` | 4 | 4 | 2 | 3 | 5 | 5 | **3.70** |
| 16 | `eye_moisture` | 5 | 2 | 1 | 3 | 5 | 5 | **3.35** |

### Ranked Results

| Rank | LoRA | Score | Build Priority |
| :--- | :--- | :--- | :--- |
| 1 | `gaze_vertical` | 4.90 | 🔴 **Phase 1 — Build First** |
| 2 | `smile` | 4.85 | 🔴 **Phase 1 — Build First** |
| 3 | `brow_raise` | 4.70 | 🔴 **Phase 1 — Build First** |
| 4 | `brow_furrow` | 4.70 | 🔴 **Phase 1 — Build First** |
| 5 | `eye_squint` | 4.70 | 🔴 **Phase 1 — Build First** |
| 6 | `gaze_horizontal` | 4.30 | 🟡 **Phase 2 — Build Next** |
| 7 | `lip_press` | 4.25 | 🟡 **Phase 2 — Build Next** |
| 8 | `mouth_frown` | 4.15 | 🟡 **Phase 2 — Build Next** |
| 9 | `eye_wide` | 4.05 | 🟡 **Phase 2 — Build Next** |
| 10 | `jaw_open` | 3.95 | 🟡 **Phase 2 — Build Next** |
| 11 | `chin_raise` | 3.95 | 🟡 **Phase 2 — Build Next** |
| 12 | `dimpler` | 3.70 | 🟢 **Phase 3 — Refinement** |
| 13 | `head_tilt` | 3.70 | 🟢 **Phase 3 — Refinement** |
| 14 | `lip_pucker` | 3.40 | 🟢 **Phase 3 — Refinement** |
| 15 | `nose_wrinkle` | 3.40 | 🟢 **Phase 3 — Refinement** |
| 16 | `eye_moisture` | 3.35 | 🟢 **Phase 3 — Refinement** |

---

## Part 3: Why These Top 5 Form a Complete Emotional Toolkit

With ONLY the Phase 1 LoRAs stacked, you can compose virtually every coaching emotion:

| Emotion | smile | gaze_vert | brow_raise | brow_furrow | eye_squint |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Warm confidence** | 0.6 | 0.0 | 0.1 | 0.0 | 0.4 |
| **Vulnerable openness** | 0.2 | 0.3 ↑ | 0.5 | 0.0 | 0.0 |
| **Empathic concern** | 0.1 | 0.0 | 0.0 | 0.4 | 0.3 |
| **Determined resolve** | 0.0 | 0.0 | 0.0 | 0.6 | 0.5 |
| **Joyful celebration** | 0.9 | 0.0 | 0.3 | 0.0 | 0.7 |
| **Deep listening** | 0.0 | 0.2 ↓ | 0.2 | 0.2 | 0.3 |
| **Gentle challenge** | 0.3 | 0.0 | 0.4 | 0.3 | 0.2 |
| **Authentic sadness** | 0.0 | 0.4 ↓ | 0.5 | 0.2 | 0.0 |

> [!TIP]
> 5 LoRAs × 10 intensity levels each = **100,000 theoretically possible expression combinations.** This is your competitive moat.

---

## Part 4: The Reference Image Pipeline

### The User's Insight

> "What do you think of starting with an image reference for the expressions? We find the best images to represent the expression we want and then from there get the parameters."

This is a brilliant quality-control mechanism. The pipeline:

```
Step 1: Curate "Gold Standard" reference photos
        Find the PERFECT photo of a real human making the exact expression
        Example: a photo of a therapist showing genuine empathic concern

Step 2: Extract expression vector
        MediaPipe / InsightFace / OpenFace → facial landmarks
        Convert landmarks → ARKit blendshape values (52 parameters)
        Result: {"mouthSmileLeft": 0.35, "browInnerUp": 0.22, ...}

Step 3: Apply to MetaHuman
        Feed ARKit JSON → MetaHuman Control Rig (Python/UE5)
        Render across 10+ diverse MetaHuman faces
        Vary lighting, angle, background

Step 4: Verify accuracy
        Compare rendered MetaHuman expression to original reference photo
        Human QA: "Does this FEEL the same?"
        Adjust parameters if needed → re-render

Step 5: Train LoRA on verified dataset
```

### Why This Pipeline is Superior

1. **Ground Truth from Reality** — The expression came from a REAL human, not from guessing slider values
2. **Testable Quality** — You can compare the LoRA's output to the original reference photo
3. **Emotionally Calibrated** — You're not training on arbitrary blendshape values; you're training on expressions that actually FEEL right
4. **Iterative Refinement** — Find the expression is 80% right? Adjust 2-3 parameters and re-render

### ChatGPT's Assessment (Honest Review)

ChatGPT's pipeline (`Image → AI extractor → ARKit JSON → MetaHuman → Render`) is **architecturally correct.** Here's what's real and what's aspirational:

| Claim | Verdict | Notes |
| :--- | :--- | :--- |
| MediaPipe can extract facial landmarks from images | ✅ Real | Google's MediaPipe Face Mesh outputs 468 landmarks |
| Landmarks can be converted to ARKit blendshapes | ✅ Real | Libraries exist (face-mesh-to-arkit, py-feat) |
| Conversion is perfectly accurate | ⚠️ Overstated | Single images are ambiguous; extraction is ~70-80% accurate |
| Python can drive MetaHuman Control Rig | ✅ Real | Unreal Python API supports this |
| "Ready-to-run script" available | ❌ Doesn't exist | Would need custom engineering (~1-2 weeks) |
| No official "Image → MetaHuman" plugin | ✅ Correct | Only video → MetaHuman is officially supported |

### The Honest Limitation

Single-image expression extraction has a core ambiguity problem: is that a polite smile or a genuine smile? A subtle smirk or a suppressed laugh? The landmark positions look nearly identical.

**Solution:** Use multiple reference images of the same emotion, extract from all, and average the ARKit values. Then have a human (you) validate the MetaHuman render against the reference before training.

---

## Part 5: Expression LoRA Composition Presets (For CCP Arcs)

Once all 16 LoRAs are built, we can define **named presets** that map to our visual framework emotions:

```json
{
  "the_witness_empathy": {
    "smile": 0.15,
    "gaze_vertical": -0.2,
    "brow_raise": 0.0,
    "brow_furrow": 0.25,
    "eye_squint": 0.35,
    "lip_press": 0.20
  },
  "breakthrough_joy": {
    "smile": 0.85,
    "gaze_vertical": 0.1,
    "brow_raise": 0.30,
    "brow_furrow": 0.0,
    "eye_squint": 0.70,
    "jaw_open": 0.15
  },
  "vulnerable_confession": {
    "smile": 0.0,
    "gaze_vertical": -0.35,
    "brow_raise": 0.45,
    "brow_furrow": 0.15,
    "eye_squint": 0.0,
    "chin_raise": 0.30
  },
  "gentle_authority": {
    "smile": 0.25,
    "gaze_vertical": 0.0,
    "brow_raise": 0.0,
    "brow_furrow": 0.40,
    "eye_squint": 0.45,
    "lip_press": 0.35
  }
}
```

These presets become **one-click emotional recipes** that any CMF operator can apply without understanding the underlying FACS system.

---

## Part 6: Engineering Roadmap

| Phase | Work | Timeline | Output |
| :--- | :--- | :--- | :--- |
| **Phase 0** | Set up MetaHuman + UE5 Python scripting environment | 1 week | Working render pipeline |
| **Phase 0.5** | Build Image → ARKit extraction tool (MediaPipe/py-feat) | 3-5 days | Reference expression → JSON converter |
| **Phase 1** | Train top 5 LoRAs (smile, gaze_vert, brow_raise, brow_furrow, eye_squint) | 2-3 weeks | Core emotional toolkit |
| **Phase 2** | Train next 6 LoRAs (gaze_horiz, lip_press, mouth_frown, eye_wide, jaw_open, chin_raise) | 2 weeks | Extended control set |
| **Phase 3** | Train final 5 LoRAs (dimpler, head_tilt, lip_pucker, nose_wrinkle, eye_moisture) | 2 weeks | Full 16-LoRA expression engine |
| **Phase 4** | Define named presets for all CCP emotional arcs | 1 week | Emotion recipe library |
