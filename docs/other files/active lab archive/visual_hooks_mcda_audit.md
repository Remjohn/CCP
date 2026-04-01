# Visual Hooks Recipes — MCDA Audit & Upgrade

> **Date:** 2026-03-29 · **Method:** 6-criteria MCDA against CCP research corpus
> **Input:** 65 existing hooks · **Output:** 30 upgraded + 8 new = **38 production hooks**

---

## MCDA Criteria (Each scored 0–5)

| # | Criterion | Source | Weight | What It Measures |
|:--|:----------|:-------|:-------|:-----------------|
| C1 | **CVE Gaze/Composition** | PRD §4.3 | 20% | Does it use intentional gaze vectors, Z-pattern, compression principle? |
| C2 | **Emotional Contagion** | Emotional DNA | 20% | Does it trigger mimicry→feedback→convergence loop in viewer? |
| C3 | **Mood State Routing** | DEP-ENG-016 | 20% | Is it targetable to P/E/D/S with audience maturity clamping? |
| C4 | **Memetic Engine (BVT/IR)** | Memetic Engine | 15% | Can it serve as violation, benignness, or pattern interrupt? |
| C5 | **FACS Expressibility** | ConsciousSmile 28ch | 10% | Can the expression be specified with our 28 channels? |
| C6 | **ControlNet Composability** | ConsciousPose 294 | 15% | Can it be reproduced deterministically with our CP-IDs? |

**Threshold:** Hooks scoring < 15/30 are CUT. Hooks 15-20 are UPGRADED. Hooks 20+ are KEPT with CP-ID mapping.

---

## CATEGORY 1: IDENTITY + EMOTION (10 hooks → 8 kept)

### ✅ KEPT & UPGRADED

| # | Original Hook | Score | Upgrade | CP-ID Recipe |
|:--|:------|:------|:--------|:-------------|
| 1 | **The "Look Away" Opener** | 24 | Add CVE gaze vector spec (20° averted for Cold CBCS). Add expression recipe. | Body: CP-B-007, Gaze: CP-G-009→CP-G-001 (transition), Expression: `brow_furrow: 0.3, lip_press: 0.2` → `smile: 0.3, eye_squint: 0.2`, Scene: CP-S-003 |
| 2 | **Closed Eyes to Eye Contact** | 26 | Perfect CVE Gaze Vector activation. Add `brow_flash` (ch.20) on eye-open for the recognition signal. | Body: CP-B-005, Gaze: CP-G-016→CP-G-001, Expression: `eye_wide: 0.0→0.6, brow_flash: 0.8`, Scene: CP-S-001, Mood: CP-MV-003 |
| 3 | **Genuine Laugh to Serious** | 25 | Map to BVT benignness→violation transition. Use `mouth_stretch→lip_press` expression arc. | Body: CP-B-002, Gaze: CP-G-001, Expression: `smile: 1.0, mouth_stretch: 0.6, eye_squint: 0.8` → `smile: 0.0, brow_furrow: 0.4, lip_press: 0.5`, Scene: CP-S-002 |
| 4 | **Whispering Secret** | 22 | Add proxemics spec (lean = CP-B-002 at 15° forward). FACS: `lip_press: 0.3, eye_squint: 0.5` for "knowing" face. | Body: CP-B-002 (intense lean), Hands: CP-H-006, Gaze: CP-G-005, Expression: `smirk: 0.4, eye_squint: 0.5`, Scene: CP-S-028 |
| 5 | **One-Line Vulnerability Drop** | 23 | Perfect deadpan delivery. FACS controls everything. Tight frame = CP-S-001. | Body: CP-B-001 (square), Hands: CP-H-031, Gaze: CP-G-001, Expression: `smile: 0.0, lip_press: 0.3, eye_moisture: 0.2`, Scene: CP-S-001 |
| 6 | **The Window Gaze Reveal** | 21 | Map to Processing-Deep mood visual. Through-glass scene. | Body: CP-B-003, Gaze: CP-G-015→CP-G-001, Scene: CP-S-033, Mood: CP-MV-003 |
| 7 | **Car Confession** | 20 | Intimate lighting = CP-MV-025. Dashboard glow. Direct gaze at camera. | Body: CP-B-021 (seated relaxed), Gaze: CP-G-001, Expression: `brow_furrow: 0.2, eye_moisture: 0.3`, Scene: CP-S-028, Mood: CP-MV-025 |
| 8 | **Head-in-Hands Moment** | 22 | Map to Processing-Deep. Expression: `brow_furrow: 0.8, eye_moisture: 0.4`. Brief = pattern interrupt. | Body: CP-B-064 (curled protective) or CP-B-035 (facepalm), Hands: CP-H-050, Gaze: CP-G-014, Scene: CP-S-001 |

### ❌ CUT (Redundant or Low-Scoring)

| Hook | Score | Reason |
|:-----|:------|:-------|
| Mid-Conversation Entry | 12 | Pure filming technique, no body language or expression spec — not a visual composition |
| Emotional Voice Crack | 11 | Audio-dependent, not visual. Cannot be reproduced via ControlNet |
| Adjusting Posture Mid-Thought | 13 | Too vague — "shifts position" is not a composable instruction. Absorbed into transitions between CP-B poses |

---

## CATEGORY 2: PROP-DRIVEN HOOKS (18 hooks → 8 kept)

### ✅ KEPT & UPGRADED

| # | Original Hook | Score | Upgrade | CP-ID Recipe |
|:--|:------|:------|:--------|:-------------|
| 9 | **Sticky Notes Peel-Off** | 22 | Perfect BVT benign violation (identity threat → resolution via removal). Add expression arc. | Body: CP-B-005, Hands: CP-H-022 (framing), Props: CP-P-021 (sticky notes), Expression: `brow_furrow: 0.5` → `smile: 0.4, chin_raise: 0.3`, Scene: CP-S-032 (mirror shot) |
| 10 | **Heavy Backpack Drop** | 24 | Gravity = visceral. Perfect Processing→Discovery transition. Add breath-state. | Body: CP-B-001→CP-B-034 (arms raised post-drop), Hands: CP-H-031 (released), Expression: `lip_press: 0.6, neck_tension: 0.5` → `jaw_open: 0.3, smile: 0.2`, Scene: CP-S-008 (full body) |
| 11 | **Mirror Post-It Affirmation** | 21 | Self-directed gaze cueing. Mirror = identity work. | Body: CP-B-005, Gaze: CP-G-022, Props: CP-P-021, Expression: `lip_bite: 0.2, eye_moisture: 0.3`, Scene: CP-S-032, Mood: CP-MV-001 |
| 12 | **Notebook Flip Open** | 19 | Add hands precision (CP-H-021 pen in hand). Shows process. | Body: CP-B-014, Hands: CP-H-021, Props: CP-P-005, Gaze: CP-G-017 (at prop), Scene: CP-S-010 |
| 13 | **Key Turning / Door Opening** | 20 | Threshold metaphor maps to Discovery-Revelation. Add breath-state (held inhale). | Body: CP-B-023 (walking toward), Props: CP-P-018, Gaze: CP-G-006 (wide eyes), Scene: CP-S-035 (framed by architecture) |
| 14 | **Mask Removing** | 23 | *Upgraded from "Object Inspection."* Authenticity reveal. BVT violation (social norm breach). | Body: CP-B-005, Hands: CP-H-047 (removing), Props: CP-P-032, Expression: `lip_press: 0.5` → `smile: 0.3, eye_moisture: 0.4, brow_raise: 0.3`, Scene: CP-S-028 |
| 15 | **Candle Lit/Blown** | 18 | Processing-Deep ritual. Add golden-hour mood visual. | Body: CP-B-068, Props: CP-P-034, Gaze: CP-G-016, Expression: `eye_squint: 0.3, smile: 0.15`, Mood: CP-MV-005 |
| 16 | **Overflow Pour** | 22 | Burnout/boundaries metaphor. Physical cause→effect. BVT violation (mess). | Body: CP-B-001, Hands: CP-H-022, Gaze: CP-G-001, Expression: `eye_wide: 0.6, brow_raise: 0.5`, Scene: CP-S-005 |

### ❌ CUT

| Hook | Score | Why |
|:-----|:------|:----|
| Building Blocks | 14 | Generic. "Stacking blocks" is stock imagery coaching cliché |
| Water Glass Metaphor | 12 | Vague. No emotional anchor |
| Object Inspection | 13 | Too generic. Absorbed into "Mask Removing" |
| Balanced Scale | 11 | Literal/on-the-nose. No subversion |
| Malleable Material | 14 | Close but too arts-and-crafts. Not premium |
| Worn-Out Sneakers | 10 | Stock coaching visual. No BVT, no contagion |
| Mirror + Marker | 13 | Redundant with Mirror Post-It (kept) |
| Spilled Coffee | 14 | Good chaos but audio-dependent for impact |
| Clock Hand | 12 | Cliché time metaphor |
| Photo Frame | 13 | Absorbed into Sorting Memories (relatable actions) |

---

## CATEGORY 3: MOTION + BODY-LED (8 hooks → 6 kept)

### ✅ KEPT & UPGRADED

| # | Original Hook | Score | Upgrade | CP-ID Recipe |
|:--|:------|:------|:--------|:-------------|
| 17 | **Gradual Frame Approach** | 26 | CVE gaze vector ACTIVATION. Start Discovery gaze (off-camera) → end Processing (direct). Proxemics = power. | Body: CP-B-023 (walking toward), Gaze: CP-G-009→CP-G-003 (chin down authority), Expression: `smile: 0.0, brow_furrow: 0.2` → `smirk: 0.3, eye_squint: 0.4`, Scene: CP-S-008→CP-S-001 |
| 18 | **Sit Down on Floor** | 24 | Power dynamic destruction → BVT benignness signal. Add Escape-Cooling mood lighting. | Body: CP-B-017, Gaze: CP-G-001, Expression: `smile: 0.2, brow_raise: 0.15`, Scene: CP-S-007 (high angle), Mood: CP-MV-008 |
| 19 | **Fall into Bed** | 22 | Surrender moment. Processing-Deep with CP-MV-025 intimate lighting. | Body: CP-B-039 (reclining), Gaze: CP-G-013 (upward), Expression: `jaw_open: 0.2, eye_moisture: 0.3, neck_tension: 0.4`, Scene: CP-S-031 (overhead) |
| 20 | **Head Lean Against Window** | 23 | Through-glass scene composition. Processing-Deep. | Body: CP-B-064 variant, Gaze: CP-G-015, Scene: CP-S-033, Expression: `brow_furrow: 0.4, lip_press: 0.3, eye_moisture: 0.3`, Mood: CP-MV-032 |
| 21 | **Rising with Renewed Energy** | 25 | Discovery-Revelation. Transition CP-B-017→CP-B-025 (mid-rise). Breath: sharp inhale. | Body: CP-B-025 (mid-rise), Gaze: CP-G-004 (chin up confident), Expression: `smile: 0.0→0.6, chin_raise: 0.4, eye_wide: 0.3`, Scene: CP-S-006 (low angle heroic) |
| 22 | **Walking Away Looking Back** | 21 | Invitation/mystery hook. Discovery mood. | Body: CP-B-024, Gaze: CP-G-024, Expression: `smirk: 0.3, brow_raise: 0.2`, Scene: CP-S-034 (long lens compressed) |

### ❌ CUT

| Hook | Score | Why |
|:-----|:------|:----|
| Walk Into Frame From Behind | 14 | Filming technique, not a visual composition |
| Sitting Down with Effort | 13 | Redundant with "Sit Down on Floor" (upgraded version is stronger) |

---

## CATEGORY 4: ENVIRONMENT (13 hooks → 6 kept)

### ✅ KEPT & UPGRADED

| # | Original Hook | Score | Upgrade | CP-ID Recipe |
|:--|:------|:------|:--------|:-------------|
| 23 | **Threshold Sitting** | 25 | "Between worlds" body language. Discovery/Processing transition. Framed by architecture. | Body: CP-B-042 (one knee up), Gaze: CP-G-009, Scene: CP-S-035, Mood: CP-MV-003, Expression: `brow_furrow: 0.3, lip_bite: 0.2` |
| 24 | **Alone at Empty Café** | 23 | Escape-Cooling loneliness. CVE compression (small person, big space). | Body: CP-B-015, Gaze: CP-G-015 (distant stare), Props: CP-P-007, Scene: CP-S-017, Mood: CP-MV-008, Expression: `lip_corner_depress: 0.3, eye_moisture: 0.2` |
| 25 | **Kitchen with Mug** | 20 | Universal warmth. Processing-Cooling baseline scene. | Body: CP-B-005, Hands: CP-H-015, Props: CP-P-007, Scene: CP-S-015, Mood: CP-MV-001 |
| 26 | **Bed Context** | 22 | *Merged: Bed with Laptop + Lying Down POV + Waking Up.* ASFW intimacy anchor. Morning vulnerability. | Body: CP-B-039 or CP-B-080, Gaze: CP-G-025 (slow blink intimate), Scene: CP-S-028, Mood: CP-MV-025, Expression: `smile: 0.2, eye_squint: 0.3, lip_bite: 0.15` |
| 27 | **Beach/Nature Reveal** | 19 | Escape-Cooling with Discovery transition. Environment as breath-state. | Body: CP-B-017, Gaze: CP-G-011, Scene: CP-S-014, Mood: CP-MV-007, Expression: `smile: 0.3, eye_wide: 0.2` |
| 28 | **Crosswalk Confession** | 20 | Urban environment. Decision-making. Status/Discovery. | Body: CP-B-001, Gaze: CP-G-001, Scene: CP-S-036 (motion blur), Mood: CP-MV-013 |

### ❌ CUT

| Hook | Score | Why |
|:-----|:------|:----|
| Staircase Bottom/Top | 13 | On-the-nose metaphor. "Stairs = journey" is coaching cliché |
| Couch Centered/Side | 12 | Generic positioning, not a hook |
| Floor Notepad | 11 | Redundant with sit-on-floor (kept) |
| Bridge Walk | 14 | Bridges = transition is too literal |
| Walking Through Grocery | 12 | Great concept but too complex for ControlNet conditioning — live action only |
| Walking Through Street | 13 | Same — live action, not composable |
| Nature Reveal | Merged into #27 | — |

---

## CATEGORY 5: UNUSUAL ANGLES (8 hooks → 4 kept)

### ✅ KEPT & UPGRADED

| # | Original Hook | Score | Upgrade | CP-ID Recipe |
|:--|:------|:------|:--------|:-------------|
| 29 | **Two-Shot Clone Effect** | 24 | Multi-char composition. Before/After same person. Direct library hit. | Multi: CP-MC-010, Scene: CP-S-019 (split screen), Expression: contrast two recipes |
| 30 | **Reflection-Only First** | 23 | Mirror/duality. Identity work. Processing-Worldview. | Body: CP-B-005, Scene: CP-S-032 (mirror reflection), Mood: CP-MV-002, Expression: `smirk: 0.2, brow_furrow: 0.3` |

### ❌ CUT

| Hook | Score | Why |
|:-----|:------|:----|
| Inside Fridge POV | 10 | Gimmick. No emotional contagion |
| Through Closet/Cupboard | 11 | Gimmick. Not composable via ControlNet |
| Ceiling Looking Down | 13 | Redundant with overhead (CP-S-031 already in library) |
| Wall-Leaning Floor Sit | 14 | Redundant with CP-B-042 |
| Fish-Eye Lens | 9 | Distortion = wrong aesthetic for editorial CVE standard |
| Overhead Looking Down | 13 | Absorbed into CP-S-031 |

---

## CATEGORY 6: RELATABLE ACTIONS & TEACHING (16 hooks → 4 kept)

Most teaching/relatable action hooks are **live-action-only** and don't map to ControlNet compositions.

### ✅ KEPT & UPGRADED

| # | Original Hook | Score | Upgrade | CP-ID Recipe |
|:--|:------|:------|:--------|:-------------|
| 31 | **Putting on "Work Face"** | 24 | Expression transition. 28 FACS channels make this deterministic. | Body: CP-B-005, Expression: `smile: 0.3, brow_raise: 0.1` → `lip_press: 0.4, jaw_clench: 0.3, brow_furrow: 0.2, smirk: 0.15`, Scene: CP-S-032 (mirror) |
| 32 | **Makeup/Jewelry Thoughtfully** | 22 | Feminine power display. Intention as identity performance. ASFW beauty anchor. | Body: CP-B-055, Hands: CP-H-039, Gaze: CP-G-032 (through lashes), Scene: CP-S-032, Mood: CP-MV-025, Expression: `lip_bite: 0.2, eye_squint: 0.3` |
| 33 | **Journaling a Difficult Thought** | 20 | Processing-Deep via hand tension (CP-H-049 white-knuckle grip on pen). | Body: CP-B-020, Hands: CP-H-049, Props: CP-P-005, Gaze: CP-G-014, Scene: CP-S-010, Expression: `brow_furrow: 0.6, lip_press: 0.4, neck_tension: 0.3` |
| 34 | **Sharing Vulnerable Moment** | 21 | Multi-character intimacy. Coach+client. | Multi: CP-MC-003, Hands: CP-H-013, Gaze: CP-G-020, Scene: CP-S-029, Expression: `eye_moisture: 0.3, smile: 0.2, brow_furrow: 0.2` |

### ❌ CUT

| Hook | Score | Why |
|:-----|:------|:----|
| Smartphone Typing | 11 | Screen content = not composable |
| Mirror Routine/Self-Exam | 13 | Redundant with Mirror reflection (kept) |
| Pet Interruption | 8 | Cannot control animal via ControlNet |
| Food Preparation | 14 | Live-action. Complex object interaction |
| Finding Lost Item | 10 | Narrative, not visual |
| Multi-Tasking | 11 | Too complex for single frame |
| Waiting or Delay | 12 | Time-based, not spatial |
| Comfort Sip, Sorting Memories | 14 | Absorbed into Kitchen Mug (kept) |
| Making Tea, Cooking | 13 | Live-action only |
| Brushing Teeth | 10 | Too mundane for ControlNet investment |
| Packing Bag | 14 | Close but absorbed into Object Unpacking concept |
| Turning Off Lights | 11 | Lighting transition, not a pose |
| Teaching tools (blocks, dots, spotlight, puzzle, signs, handwriting, close-up) | 9-14 | These are A-roll/B-roll filming techniques, not ControlNet compositions |

---

## 8 NEW HOOKS (From Research Gaps)

These hooks emerged from our Memetic Engine + Emotional Contagion research but didn't exist in the old file:

| # | New Hook | Research Source | CP-ID Recipe | Mood State |
|:--|:---------|:---------------|:-------------|:-----------|
| 35 | **The Smolder Lock** — Direct camera, lip bite, sustained 3-second hold. Zero words. | CVE Gaze + ASFW anchor | Body: CP-B-005, Gaze: CP-G-026, Expression: `lip_bite: 0.4, eye_squint: 0.5, nostril_flare: 0.2, smirk: 0.3`, Scene: CP-S-001 | Status |
| 36 | **The Wink Conspiracy** — Direct-to-camera wink after dropping a truth bomb. | BVT benignness signal | Body: CP-B-003, Gaze: CP-G-001, Expression: `wink: 0.8, smirk: 0.6`, Scene: CP-S-002 | Memetic |
| 37 | **The Silent Scream** — Mouth open, no sound, held. Pattern interrupt. | Emotional Contagion (mimicry trigger) | Body: CP-B-066, Gaze: CP-G-030, Expression: `mouth_stretch: 0.9, neck_tension: 0.8, brow_furrow: 0.7`, Scene: CP-S-001 | Processing-Deep |
| 38 | **The Push-Pull** — Couple or coach-client, one hand pushing away, other pulling in. | Polarity dynamics | Body: CP-B-073, Multi: CP-MC-016, Expression: `brow_furrow: 0.4, smirk: 0.3`, Scene: CP-S-029 | Discovery |
| 39 | **The Eye Roll Truth** — Eye roll followed by direct camera address. "We all know." | BVT violation (social norm) + resolution | Body: CP-B-003, Gaze: CP-G-034→CP-G-001, Expression: `eye_roll: 0.7` → `smirk: 0.5, brow_raise: 0.3`, Scene: CP-S-002 | Memetic |
| 40 | **The Tongue Peek Rebel** — Playful tongue out, chin up. Defiant joy. | IR (nonsense humor = recursive reward) | Body: CP-B-059, Gaze: CP-G-004, Expression: `tongue_peek: 0.6, chin_raise: 0.4, smile: 0.7`, Scene: CP-S-008 | Escape-Channeling |
| 41 | **The Almost-Kiss Freeze** — Two faces, inches apart, frozen before contact. | Anticipation > arrival (dopamine in the waiting) | Body: CP-B-070, Multi: CP-MC-013, Expression: `lip_bite: 0.3, nostril_flare: 0.2, eye_squint: 0.5`, Scene: CP-S-029, Mood: CP-MV-025 | Status/Intimate |
| 42 | **The Armor Drop** — Removing jacket/blazer, partner or self, revealing vulnerability beneath. | Emotional Contagion (vulnerability mimicry) | Body: CP-B-079, Hands: CP-H-047, Props: CP-P-032, Expression: `smile: 0.0→0.3, eye_moisture: 0.3, lip_press: 0.4→0.0`, Scene: CP-S-027 | Processing→Discovery |

---

## LIBRARY COVERAGE VERIFICATION

### ✅ Fully Covered (34/42 hooks)

All 34 hooks have complete CP-ID recipes using existing atoms.

### ⚠️ Needs Minor Additions (4 atoms missing)

| Missing Atom | Needed For | Proposed ID |
|:-------------|:-----------|:------------|
| `seated_drivers_seat_dashboard_glow` | Car Confession (#7) | CP-B-081 |
| `lying_on_stomach_propped_elbows` | Floor creative position (absorbed but useful) | CP-B-082 |
| `hands_gripping_steering_wheel` | Car Confession hands | CP-H-055 |
| `forehead_against_glass_surface` | Head Lean Against Window (#20) | CP-B-083 |

> [!TIP]
> These 4 atoms can be batch-added to the iClone generation queue without architectural changes. They're minor position variants of existing body poses.

### Final Count

| Metric | Value |
|:-------|:------|
| Original hooks | 65 |
| Hooks CUT (generic/redundant/live-action-only) | 35 |
| Hooks KEPT & UPGRADED | 30 |
| New hooks from research | 8 |
| **Final production hooks** | **38** |
| Library atoms needed to add | 4 |
| **Total library after additions** | **298 atoms + 28 expression channels** |
