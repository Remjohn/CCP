# CMF Visual Skills — MCDA Research Audit
## Cross-Analysis of 10 Motion Skills Against 8 CVE + CPSC Research Papers

> [!IMPORTANT]
> This document systematically evaluates every CMF visual motion skill against the findings of 8 academic research papers from the CVE + CPSC lab. The question at hand: **Do our production-tested prompts already implement the science, or do they need research-informed upgrades?**

---

## Methodology

### MCDA Criteria (Weighted)

| # | Criterion | Weight | Source |
|---|---|---|---|
| C1 | **Physiological Targeting** — Does the skill produce outputs that target documented somatic states (fEMG, SCR, ISC)? | 30% | PSSL, Neurocinematics |
| C2 | **Gaze Architecture** — Does the skill control where the viewer *looks* using evidence-based attention direction? | 20% | Gaze Cueing Framework |
| C3 | **Chromatic Psychology** — Does the color/lighting system map to documented PAD vectors or CGCS mood states? | 20% | Cinematographic Grammar, Carousel Architecture |
| C4 | **Narrative Coherence** — Does the temporal structure leverage ISC-maximizing narrative patterns (somatic arcs, TRWs)? | 15% | Neurocinematics, Carousel Architecture |
| C5 | **Identity & Parasocial Trust** — Does the skill build parasocial attachment through character consistency and tribal signaling? | 15% | Brand Character System, Tribal Imageability, Visual Style Psychology |

### Scoring Scale

| Score | Meaning |
|---|---|
| 5 | Already implements the research finding, no change needed |
| 4 | Partially implements — minor enhancement possible |
| 3 | Implicitly aligned but not explicitly specified — moderate improvement possible |
| 2 | Significant gap — the research reveals a missing mechanism |
| 1 | Contradicts or ignores the research finding entirely |

---

## SKILL-BY-SKILL ANALYSIS

---

### 1. GMG Expert 01 — The Neo-Schematic Architect

**Role:** Systems, Networks, Connections. Neon wireframes on black void.

| Criterion | Score | Evidence | Research Gap |
|---|---|---|---|
| C1: Physiological Targeting | 3 | The "Exponential Ease-Out" physics and "Scale Pop" micro-interactions produce satisfying motion patterns, but these are designed for aesthetic "premium feel" rather than targeting specific somatic states. The PSSL paper establishes that high-contrast neon on deep black (#050505 at ≥4:1 contrast ratio) naturally triggers sympathetic arousal — so Expert 01 achieves phasic GSR activation *accidentally* through its palette, not intentionally. | **Upgrade: Add explicit CCT targeting.** The neon cyan (#00FFFF) and coral (#FF6B6B) are intuitively chosen but not mapped to PSSL's CCT specifications. Neon Cyan corresponds to ≈9000K+ equivalent — extreme cold-spectrum that the PSSL maps to "Alert/Analytical" processing. This is actually *correct* for Expert 01's "Systems" domain. However, the skill should document *why* this palette works physiologically, and add a rule: "Structure Color = cold-spectrum (analytical state); Energy Color = warm-spectrum (arousal state)." This transforms an intuitive palette into a physiologically intentional one. |
| C2: Gaze Architecture | 4 | The Node-A → Connection → Node-B topology naturally creates a left-to-right reading path that aligns with the Gaze Cueing paper's "Identity-Hook-Action" spatial architecture. The arrow connection between nodes functions as a gaze vector directing attention from the "problem" to the "solution." The 60-70% negative space prevents visual clutter that would dilute gaze direction. | **Minor upgrade: Formalize the gaze path as CBCS-adaptive.** Currently the topology is always bilateral (A-left, B-right). For cold audiences (CBCS 0-3), the Power Word should appear in the Hook Zone (upper-left quadrant per the Gaze Cueing framework). For warm audiences, the word could shift to the Action Zone (lower-right). This is a subtle positional adjustment, not a structural change. |
| C3: Chromatic Psychology | 4 | The domain → color mapping (Health = Cyan/Coral, Finance = Green/Gold, Relationships = Pink/Blush, Career = Blue/Coral) is highly aligned with the Cinematographic Grammar's CGCS taxonomy. The "Status" psychological state maps to Expert 01's career palette (cool blue, high-dominance), and the "Discovery" state maps to the mixed-temperature palettes. | **Minor upgrade: Add explicit PAD vector annotations.** Each domain palette should document its PAD (Pleasure-Arousal-Dominance) target vector. Example: "Career palette targets High Dominance (blue + minimal fill); Health palette targets Moderate Arousal + Moderate Valence (cyan + coral warmth)." This doesn't change the palettes but makes the psychological intent explicit for future LoRA training. |
| C4: Narrative Coherence | 5 | The "Seed-to-System" workflow (First Frame = disconnected/dormant → Last Frame = connected/resolved → Motion = deployment) is a textbook "Tension-Release" somatic arc from the Carousel Architecture paper. The Neurocinematics paper confirms that causal narrative structure (A causes B, B causes C) dramatically outperforms non-narrative montage for ISC — Expert 01's A→connection→B topology is literally this principle visualized. | No change needed. |
| C5: Identity & Parasocial Trust | 2 | Expert 01 is deliberately identity-free (no human subjects, pure systems). The Brand Character System paper establishes that parasocial trust requires "character persistence" — but Expert 01's abstract nodes don't generate parasocial attachment. This is acceptable for the MECHANISM arc (W3) where authority comes from logic, not personality. | **No change needed, but context-flag:** Expert 01 should NEVER be used for Hook (W1) or Close (W5) scenes because those require identity-level parasocial engagement. The GMG Composer already routes this correctly (Expert 01 → "Relationships/Systems" category), but the routing guidance doesn't explicitly cite the parasocial reasoning for *why* Expert 01 is wrong for emotional arcs. |

**OVERALL SCORE: 3.6 / 5 — Solid foundation, needs explicit physiological documentation.**

**Verdict:** Expert 01 works. The primary upgrade is *documentation*, not *restructuring*. Add PAD vector annotations to the color palettes and formalize the accidental ISC compliance as intentional.

---

### 2. GMG Expert 02 — The Mono-Kinetic Protagonist

**Role:** Human Struggle, Silhouette, Weather. Noir aesthetic.

| Criterion | Score | Evidence | Research Gap |
|---|---|---|---|
| C1: Physiological Targeting | 4 | The "Living Statue" mandate — 95% frozen body, atmospheric motion — is directly validated by the Neurocinematics paper. Hasson's data shows that unedited long takes with minimal motion produce *superior emotional coherence* via sustained amygdala activation. The Carousel Architecture paper confirms that "Physiological Tension" (stage 2) targets sympathetic stress responses through high-contrast, environmental urgency — which is exactly what Expert 02's weather system delivers. The rain/wind/fog → emotion mapping accidentally mirrors the PSSL's environmental-to-physiological mapping. | **Upgrade: Add PSSL breath-state alignment.** The CAC Composer already has a "Breath State" protocol (grief = held mid-exhale, anticipation = held mid-inhale), but Expert 02 does not. Since Expert 02's poses ARE the emotional content, each pose from the library should map to a documented breath state. "SLUMPED" → "Breath held mid-exhale, chest deflated." This grounds the silhouette's emotional specificity in physiological language. |
| C2: Gaze Architecture | 3 | Expert 02's "One Person. One Void. One Word. One Weather" mandate creates a clean two-element composition (figure + text). However, the skill does not specify WHERE the text appears relative to the figure's implied gaze vector. The Gaze Cueing paper establishes that the face — even in silhouette — creates a reflexive gaze-following response. If the text is placed in the direction the silhouette faces, fixation converges on the text. If placed opposite, the text competes with the face for attention. | **Upgrade: Add a "Text Placement" rule tied to gaze direction.** "The Power Word must appear in the direction the silhouette faces or gazes. If the figure faces right, the text enters from the right. If the figure's head is bowed, the text appears above (the direction of 'escape' from the pose). NEVER place the text behind the figure's back — this creates gaze conflict." |
| C3: Chromatic Psychology | 5 | The strict Noir Triad (Black #050505 / Grayscale / Gold #FFC727) maps perfectly to the Cinematographic Grammar's "Status" psychological state: desaturated/monochromatic + high-contrast chiaroscuro = maximum Dominance on the PAD scale. The single gold accent is neurologically justified: the Von Restorff isolation effect (a single color element in a monochromatic field receives disproportionate attentional weighting). The gold IS the message. | No change needed. The Noir Triad is research-perfect. |
| C4: Narrative Coherence | 4 | The "Elemental Library" emotion-to-weather mapping (Wind=Chaos, Rain=Sadness, Fog=Mystery, Thunder=Realization, Snow=Isolation) provides strong narrative coherence per scene. However, Expert 02 doesn't specify how scenes *sequence* across the full arc (W1→W5). The Neurocinematics paper's "Strategy 2: Emotional Anchoring" requires slow pacing and DMN activation — Expert 02's "Statue" principle delivers this, but the sequencing across the HOOK→PAIN→MECHANISM→PROOF→CLOSE arc is left to the GMG Composer's routing logic, not embedded in Expert 02 itself. | **Upgrade: Add an Arc-Level Weather Progression rule.** "If Expert 02 is used for multiple scenes in a single project, the weather system must progress climatically: Rain (struggle) → Thunder (realization) → Wind (release/power). DO NOT use the same weather element for consecutive scenes." |
| C5: Identity & Parasocial Trust | 5 | The "Character Anchor" protocol requiring a specific 50-60 word compressed anchor from `compressed_anchor.txt` is one of the strongest identity mechanisms in the entire CMF pipeline. The Brand Character System paper's core finding — that parasocial trust (PSR formation) requires consistent "identity-critical visual features" — is exactly what the Character Anchor enforces. The Noir Translation protocol (skin → luminous highlights, costume → charcoal/white) preserves identity structure even through stylistic transformation. | No change needed. Expert 02's Character Anchor protocol is the gold standard. |

**OVERALL SCORE: 4.2 / 5 — Very strong, needs breath-state and text-placement upgrades.**

**Verdict:** Expert 02 is the most research-aligned CMF skill. The two upgrades (PSSL breath states on poses, Gaze Cueing text placement rule) are *additive enhancements*, not corrections.

---

### 3. GMG Expert 03 — The Emotional Animator

**Role:** Stick Figures + Photo Cutouts. Mixed media collage.

| Criterion | Score | Evidence | Research Gap |
|---|---|---|---|
| C1: Physiological Targeting | 3 | The 12-pose library (SLUMPED, COLLAPSED, CRUSHED, etc.) intuitively maps to emotional states, but these mappings are described in psychological terms ("Defeat/sadness," "Fear/anticipation"), not physiological terms. The PSSL establishes that genuine emotional impact must target *specific* muscles: corrugator supercilii inhibition for comfort, zygomaticus major activation for joy. Expert 03's stick figures don't have facial muscles — but the POSES themselves produce mirror neuron activation in viewers. The Neurocinematics paper confirms biological motion perception activates motor/premotor cortex ISC. | **Upgrade: Add physiological target annotations to each pose.** "SLUMPED → targets corrugator activation (brow tension) + SCR decrease (sympathetic withdrawal) in viewer." "TRIUMPHANT → targets zygomaticus activation (smile response) + SCR spike (sympathetic arousal)." This doesn't change the poses but documents their physiological function for LoRA training datasets. |
| C2: Gaze Architecture | 2 | Expert 03's critical gap: the "Interaction Rule" (figure must TOUCH/REACH/RELATE to cutout object) creates an internal gaze direction (figure → object), but the skill does not specify how this internal gaze relates to the VIEWER's gaze. The Gaze Cueing paper's reflexive attention shift (18.2ms) applies even to stick figures — viewers follow the figure's gaze direction. If the figure gazes LEFT at an object, the viewer's attention shifts LEFT, potentially away from any text overlay or Hook Zone. | **Upgrade: Add a Gaze-to-Composition rule.** "The cutout object should be placed in the direction that serves the compositional hierarchy: if a text overlay will be added (in Remotion), the object should NOT be in the text zone. The figure's gaze vector CREATES the viewer's scan path: Figure → Object → Hook Zone. Place the object BETWEEN the figure and the Hook Zone, not opposite." |
| C3: Chromatic Psychology | 3 | The color palette by emotional state (Muted Blue-Grey for Pain, Vibrant Teal for Joy, etc.) is intuitively correct but not mapped to CGCS or PAD specifications. The Cinematographic Grammar paper maps specific CCT + saturation levels to psychological states. Expert 03's palette uses named colors but not CCT values. | **Upgrade: Map each emotional-state color to its CGCS equivalent.** "Pain/Stress (#6B7B8C on #E8E8E8) → CGCS 'Processing' state: desaturated, moderate CCT ≈5500K, low arousal." "Joy/Triumph (#0D7377 on #F5E6D3) → CGCS 'Discovery' state: high saturation, mixed CCT, high arousal." This enriches the palette with scientific grounding without changing the colors. |
| C4: Narrative Coherence | 5 | The "3-Act Micro-Story" timestamp protocol (Setup 0-1s → Confrontation 1-3s → Resolution 3-5s) is perfectly aligned with the Neurocinematics paper's "Temporal Receptive Windows" (TRWs). TRW research shows that the brain segments continuous input into discrete chunks of 2-5 seconds — Expert 03's 5-second clips with three internal beats fall precisely within a single TRW, maximizing within-segment neural synchrony. The Squash/Stretch/Exaggeration animation principles create the "emotional contrast" that the Carousel Architecture paper identifies as necessary for sustained engagement. | No change needed. The micro-story structure is neurologically optimized. |
| C5: Identity & Parasocial Trust | 3 | The stick figure is deliberately "universal" — no identity features, gender-neutral (with optional gender injection). This aligns with the Visual Style Psychology paper's finding that illustrated/stylized content provides "psychological safety" for processing challenging content. However, the Brand Character System paper warns that too much stylization without identity markers prevents parasocial attachment. | **Upgrade: Add per-coach stick figure consistency rules.** Documented in the GMG Expert 03 Visual Standards KI: color drift between scenes breaks the biological motion mirroring mechanism. A LoRA (Proposal 5 in the research proposals) addresses this at the generation level, but the SKILL itself should add a quality gate: "The stick figure's fill color MUST be identical across all scenes in a single project. Verify hex code match before output." |

**OVERALL SCORE: 3.2 / 5 — Strong narrative structure, needs gaze and identity upgrades.**

**Verdict:** Expert 03's emotional effectiveness is high, but the gaze architecture gap is the most significant finding. The stick figure's gaze vector directly controls where viewers look — and the current skill doesn't account for this.

---

### 4. GMG Expert 04 — The Paper Architect

**Role:** Documents, Evidence, Archives. Collage/assembly aesthetic.

| Criterion | Score | Evidence | Research Gap |
|---|---|---|---|
| C1: Physiological Targeting | 3 | The "Authenticity Through Imperfection" philosophy accidentally implements the Brand Character System paper's core finding: "Technical flaws in real film are tolerated as signs of authenticity, whereas even minor anomalies in synthetic film are interpreted as evidence of unreality." The ripped edges, coffee stains, and halftone textures are anti-uncanny signals. However, the physiological *impact* of these textures is not documented. | **Upgrade: Annotate the "Damage Tokens" with their anti-uncanny function.** "Film Grain → prevents uncanny valley detection in AI-generated textures (GSR normalization)." "Ripped Edges → triggers 'documentary authenticity' perception via material semiotics." |
| C2: Gaze Architecture | 3 | The "Single Artifact Rule" (one object, center of void) creates a clean focal point. But the "Hand of God Markup" (golden highlights, tape, stamps) serves as an implicit gaze vector — the yellow accent on monochromatic background is the single most attention-attracting element (Von Restorff effect). | **Upgrade: Make the markup a deliberate gaze director.** "The golden highlight/stamp must be placed on the artifact's most important content — the specific word, the diagnosis line, the date. The viewer's gaze path is: Artifact Edge → Golden Accent → Content. Position the accent to create this scan order." |
| C3: Chromatic Psychology | 4 | The Noir Triad + Sepia/Silver Gelatin treatment maps well to the CGCS "Processing" state (desaturated, cool-warm, introspective). The intentional aging of the paper color (sepia, kraft) communicates temporal distance — aligned with the Tribal Imageability paper's "Cultural Half-Life" concept (older visual signatures signal established cultural authority). | No significant change needed. |
| C4: Narrative Coherence | 4 | The "Exploded View" assembly animation (scattered fragments → magnetic snap → assembled artifact) is a strong "Chaos-to-Order" arc satisfying the Carousel Architecture's "Tension-Release" somatic arc type. The 12fps stutter feel creates cognitive engagement through intentional imperfection (processing fluency disruption → increased attention). | **Minor upgrade: Specify the assembly order based on emotional weight.** "Assemble peripheral fragments first, leaving the most emotionally charged piece (the diagnosis line, the face in the photo) as the LAST piece to snap into place. This creates a micro-suspense arc within the assembly animation, maximizing the ISC peak at the reveal moment." |
| C5: Identity & Parasocial Trust | 3 | Expert 04's artifacts can contain coach photographs (the "BEFORE" example), which creates indirect parasocial attachment through the vintage/documentary treatment. The silver gelatin aesthetic communicates "this is real evidence" which the Brand Character System paper maps to "plausibility indexicality" — the viewer treats the artifact as proof of real transformation. | No significant change needed. |

**OVERALL SCORE: 3.4 / 5 — Good foundation, needs gaze direction and assembly sequencing upgrades.**

---

### 5. GMG Expert 05 — The Editorial Scribe

**Role:** Duotone flat editorial illustration. Data/metrics.

| Criterion | Score | Evidence | Research Gap |
|---|---|---|---|
| C1: Physiological Targeting | 2 | Expert 05 is the least physiologically targeted skill. Its "Flat Only" mandate (no gradients, no shadows, no 3D) produces clean, pleasant illustrations, but the PSSL's framework requires *specific lighting parameters* (CCT, shadow opacity, fill ratio) to produce measurable somatic states — and flat illustrations have none of these parameters. Expert 05 operates in a physiological blind spot. | **Upgrade: Introduce "Emotional Temperature" to the palette.** While flat illustration cannot achieve the lighting specificity of CAC Composer, the duotone color pairs CAN be selected for PAD targeting. The current domain → palette mapping is content-driven (Health → Teal/Coral), not emotion-driven. Add an override: "If the beat cluster specifies a W1 (HOOK) or W2 (PAIN) scene, shift the palette toward lower-valence duotones (cooler primaries, muted accents). If W4 (PROOF) or W5 (CLOSE), shift toward higher-valence duotones (warmer primaries, brighter accents)." |
| C2: Gaze Architecture | 2 | Expert 05's composition rules ("Central Focus, Generous Margins") don't specify gaze direction. The "Hand-Drawn Typography" is integrated INTO the illustration, which is good (prevents the "Face Priority Trap"), but the spatial relationship between icon and text is not formalized. | **Upgrade: Add a "Read Path" rule.** "The illustration hierarchy must create a top-to-bottom or left-to-right reading path: Icon → Metric → Supporting Element. The metric/number is the primary hook — place it at the compositional focal point. If the illustration contains a directional element (arrow, pointing hand, eye), it must point TOWARD the metric." |
| C3: Chromatic Psychology | 4 | The duotone domain mapping (Health → Teal + Coral, Finance → Green + Gold, etc.) is well-constructed and intuitively aligns with the CGCS taxonomy. The strict "2 colors + paper" constraint prevents the visual noise that would dilute the PAD emotional targeting. | No significant change needed. The constraint itself is the strength. |
| C4: Narrative Coherence | 4 | The "Draw-On Reveal" motion sequence (Outline → Fill → Label → Settle) is a clean build-up arc that keeps the viewer engaged across the full 5-second clip. The "Stamp Bounce" settle is a satisfying micro-resolution. | No change needed. |
| C5: Identity & Parasocial Trust | 2 | Expert 05 is identity-free (icons, not people). No parasocial mechanism. This is acceptable for its function (MECHANISM/PROOF arcs where data authority replaces personal authority). | No change needed contextually — Expert 05 should ONLY be used for data/metric scenes as the Composer already specifies. |

**OVERALL SCORE: 2.8 / 5 — Functional but the least research-aligned skill. Needs gaze and temperature upgrades.**

**Verdict:** Expert 05 is the most "utilitarian" skill — it works for explaining mechanisms, but it doesn't leverage the research's most powerful findings. The upgrades are additive, not corrective.

---

### 6. GMG Expert 06 — The Visual Synthesizer

**Role:** Pure geometry. Logic, truth, minimalism. Black + White only.

| Criterion | Score | Evidence | Research Gap |
|---|---|---|---|
| C1: Physiological Targeting | 3 | The "Active Void" principle (80% negative space, binary contrast) creates extreme figure-ground separation that neurologically maximizes perceptual clarity. The PSSL's "Alert/Analytical" mode maps to high-contrast, cool-spectrum stimuli — and Expert 06's pure white on pure black is the maximum-contrast possible, producing peak alpha desynchronization (analytical processing). But this is accidental, not documented. | **Upgrade: Document the intended physiological state.** "Expert 06 targets Alpha Desynchronization (analytical/logical processing state). The binary B&W palette produces the highest possible contrast ratio, requiring maximum cognitive engagement. This is the MECHANISM arc's physiological function: the viewer should be THINKING, not FEELING." |
| C2: Gaze Architecture | 5 | Expert 06's geometric compositions naturally create perfect gaze paths. The "Trim Path" draw animation literally TRACES the viewer's gaze through the composition in real-time. The "Fractal Zoom" technique (zooming into a detail that becomes the next scene's container) chains gaze across transitions seamlessly. This is the most gaze-optimized skill in the pipeline. | No change needed. Expert 06's geometry IS a gaze architecture. |
| C3: Chromatic Psychology | 3 | Binary B&W is maximally effective for analytical states but cannot target valence-driven emotions (warmth, comfort, hope). This is by design — Expert 06 rejects emotion entirely. The CGCS taxonomy's "Status" state is the closest match (desaturated, high-contrast, dominant). | No change needed — the limitation is intentional and correct for Expert 06's function. |
| C4: Narrative Coherence | 5 | The Thesis → Antithesis → Synthesis timestamp protocol (2s → 2s → 1s) mirrors the Hegelian dialectic while also implementing the Neurocinematics paper's finding that narrative structure dramatically outperforms montage for ISC. The morph transitions (knot → straight line; staircase → flywheel; scattered dots → aligned array) are semantic transformations, not arbitrary animations — each morph IS the coaching insight rendered visually. | No change needed. Expert 06's dialectical structure is the most intellectually rigorous in the pipeline. |
| C5: Identity & Parasocial Trust | 1 | Deliberately identity-free. The abstract stick figure is intentionally non-parasocial. This is correct for Expert 06's logic/truth domain. | No change needed — Expert 06's anti-identity stance is a feature, not a bug. |

**OVERALL SCORE: 3.4 / 5 — Excellent for its domain, limited by design to analytical states.**

---

### 7. CAC Composer — Vogue Living Edition

**Role:** Conscious Ambient Cinema. Editorial photography prompts, 6-section structure.

| Criterion | Score | Evidence | Research Gap |
|---|---|---|---|
| C1: Physiological Targeting | 4 | The CAC Composer is the closest skill to PSSL compliance. The "Breath State" protocol maps emotions to specific respiratory patterns (grief = held mid-exhale, anticipation = held mid-inhale). The "Silence Rule" ("This should feel soundless") targets the parasympathetic processing mode required for deep emotional engagement. The "95% Frozen Body" motion spec is neurocinemiatically validated for sustained amygdala activation. The "Color Temperature as Emotional Code" table maps emotions to CCT ranges (Grief → Cool/Tungsten; Warmth → Golden Hour; Tension → Harsh Midday). | **Upgrade: Add explicit fEMG/SCR targets.** The Breath State and Color Temperature tables should annotate their physiological targets: "Grief (Cool/Tungsten) → targets corrugator supercilii activation (brow tension) + SCR decrease." "Hope (Dawn/Mixed) → targets zygomaticus activation + SCR increase." This transforms intuitive emotional mapping into PSSL-grade physiological specifications. |
| C2: Gaze Architecture | 3 | The "Posture & Gaze" composition rule (Section 3, Rule 4) specifies gaze direction as part of the editorial frame. The "One Action" rule creates a focal gesture that anchors attention. However, these are described as aesthetic choices, not as attention-direction mechanisms. The Gaze Cueing paper's 18.2ms reflexive shift is not referenced or leveraged. | **Upgrade: Formalize the Gaze-to-Hook connection.** "Section 3, Rule 4 (Posture & Gaze) must specify whether the subject's gaze is directed AT camera (Trust/Credibility mode — for warm audiences, CBCS 4-7) or AWAY from camera toward a compositional element (Mystery/Intrigue mode — for cold audiences, CBCS 0-3). Gaze AT camera creates parasocial connection but prevents the viewer from processing environmental details. Gaze AWAY from camera directs the viewer to process the environment and text overlays." |
| C3: Chromatic Psychology | 5 | The Color Temperature table (Grief=Cool, Warmth=Warm, Numbness=Neutral, Tension=Hot, Hope=Mixed) is strongly aligned with the CGCS taxonomy. The "Contradictory Texture Requirement" (sterile hospital + mascara smudge; warm kitchen + cold condensation) creates the "cognitive dissonance" that the Neurocinematics paper identifies as an ISC amplifier — the brain detects the inconsistency and engages more deeply. | No change needed. The Contradictory Texture Requirement is one of the most research-aligned mechanisms in the entire pipeline. |
| C4: Narrative Coherence | 4 | The "Temporal Question" (Before vs After — never During) is a sophisticated narrative tool that the Neurocinematics paper validates: anticipation and aftermath produce stronger ISC than peak moments because they engage the Default Mode Network (imagination/projection). The "Before/After" structure forces the viewer to mentally construct the missing event. | **Minor upgrade: Add an explicit DMN annotation.** "CAC captures Before or After because these states engage the Default Mode Network — the viewer's brain constructs the missing event internally, creating a personalized emotional intensity that surpasses the literal depiction." |
| C5: Identity & Parasocial Trust | 5 | The Full Physical DNA requirement (SKIN + HAIR + FACE + BUILD + COSTUME, verbatim from Brand Avatar) is the most rigorous identity mechanism in the pipeline. The compressed anchor (50-60 words) with Z-Image optimization ensures character persistence across all 5 scenes. The Brand Character System paper's "facial individuation" hierarchy (horizontal orientation energy → skin texture → facial proportion) is directly served by CAC's requirement to describe all five DNA elements. | No change needed. CAC Composer's identity system is research-optimal. |

**OVERALL SCORE: 4.2 / 5 — The most research-aligned skill alongside Expert 02. Needs minor gaze and physiological annotations.**

---

### 8–10. GMG Composer, GMG Analyst, CAC Analyst (Orchestration & Validation)

These three skills are routing and validation agents, not prompt-generation agents. They don't directly produce visual outputs, so the MCDA criteria apply differently.

| Skill | Key Research Finding | Current Status | Recommended Upgrade |
|---|---|---|---|
| **GMG Composer** (Router) | Gaze Cueing's "Face Priority Trap" — Expert selection should consider whether the scene needs gaze direction or cognitive processing | ✅ The routing table correctly maps emotional scenes to Expert 02/03 (face-based) and mechanism scenes to Expert 05/06 (abstract). But the routing doesn't differentiate by CBCS audience temperature. | **Add CBCS-aware routing guidance.** "For cold audience content (CBCS 0-3), prioritize Expert 06 (analytical authority) and Expert 01 (systems credibility) for W3 (MECHANISM) scenes. For warm audience content (CBCS 4-7), Expert 03 and Expert 02 are acceptable for mechanism delivery because the audience trusts the coach enough to receive mechanisms emotionally." |
| **GMG Analyst** (Validator) | PSSL's AGSS scale — prompts should be evaluated for anti-generic specificity, not just palette compliance | ✅ Checks palette, word count, expert voice, and 3-phase completeness. ❌ Does NOT check physiological targeting or gaze architecture. | **Add CHECK G8: Physiological Intentionality.** "Does the prompt specify a target somatic state? If Expert 02 (silhouette + weather), verify that the weather element maps to a documented emotional-physiological pairing. If Expert 03 (stick figure), verify that the pose targets a specific mirror-neuron activation pattern." |
| **CAC Analyst** (Validator) | PSSL's breath state → fEMG mapping; Gaze Cueing's text-vs-face fixation | ✅ Checks breath state, temporal state, sensory stacking. ⚠️ Does not check gaze direction against CBCS or verify Color Temperature against CGCS specifications. | **Add CHECK C10: Gaze-CBCS Alignment.** "If content targets cold audiences, subject gaze must be averted (not direct-to-camera). If warm audiences, direct gaze is acceptable. Verify that gaze direction in Section 3 (Composition) matches the CBCS tier of the target content." |

---

## AGGREGATE MCDA MATRIX

| Skill | C1 Physio (30%) | C2 Gaze (20%) | C3 Color (20%) | C4 Narrative (15%) | C5 Identity (15%) | **Weighted Total** |
|---|---|---|---|---|---|---|
| GMG Expert 01 | 3 | 4 | 4 | 5 | 2 | **3.55** |
| GMG Expert 02 | 4 | 3 | 5 | 4 | 5 | **4.15** |
| GMG Expert 03 | 3 | 2 | 3 | 5 | 3 | **3.15** |
| GMG Expert 04 | 3 | 3 | 4 | 4 | 3 | **3.35** |
| GMG Expert 05 | 2 | 2 | 4 | 4 | 2 | **2.80** |
| GMG Expert 06 | 3 | 5 | 3 | 5 | 1 | **3.35** |
| CAC Composer | 4 | 3 | 5 | 4 | 5 | **4.15** |

---

## PRIORITY UPGRADE MATRIX (Ranked by Impact × Effort)

| Priority | Skill | Upgrade | Impact | Effort | Research Source |
|---|---|---|---|---|---|
| 🔴 **P1** | Expert 03 | Add Gaze-to-Composition rule for stick figure → object → Hook Zone | HIGH | LOW | Gaze Cueing |
| 🔴 **P1** | Expert 02 | Add Text Placement rule tied to silhouette gaze direction | HIGH | LOW | Gaze Cueing |
| 🔴 **P1** | CAC Composer | Formalize gaze direction as CBCS-adaptive (at-camera vs away-from-camera) | HIGH | LOW | Gaze Cueing, CBCS |
| 🟠 **P2** | Expert 02 | Add PSSL breath-state annotations to pose library | MED | LOW | PSSL |
| 🟠 **P2** | Expert 03 | Add physiological target annotations to 12-pose library | MED | LOW | PSSL, Neurocinematics |
| 🟠 **P2** | Expert 04 | Specify assembly order by emotional weight (most charged piece last) | MED | LOW | Neurocinematics (ISC peak) |
| 🟡 **P3** | Expert 01 | Add PAD vector annotations to domain palettes | LOW | LOW | CGCS, PAD model |
| 🟡 **P3** | Expert 05 | Add arc-position temperature shift to duotone selection | LOW | MED | PSSL, CGCS |
| 🟡 **P3** | GMG Analyst | Add CHECK G8: Physiological Intentionality validation | LOW | MED | PSSL |
| 🟡 **P3** | CAC Analyst | Add CHECK C10: Gaze-CBCS Alignment validation | LOW | MED | Gaze Cueing |
| 🟢 **P4** | Expert 06 | Document intended physiological state (Alpha Desync) | DOC | LOW | PSSL |
| 🟢 **P4** | GMG Composer | Add CBCS-aware routing guidance for audience temperature | DOC | LOW | CBCS, Visual Style Psych |
| 🟢 **P4** | CAC Composer | Add DMN annotation to Before/After temporal protocol | DOC | LOW | Neurocinematics |

---

## CONCLUSION

**The prompts are good. The research says they're better than you think — but they could be *intentionally* good instead of *accidentally* good.**

The core finding of this audit: **8 out of 10 CMF motion skills already implement research-validated mechanisms**, but they do so intuitively rather than explicitly. The practical upgrades fall into three categories:

1. **Gaze Architecture Formalization (P1 — do first):** Three skills (Expert 02, Expert 03, CAC Composer) need explicit gaze-direction rules because the Gaze Cueing research reveals that gaze vectors control 18.2ms-level reflexive attention — and the current skills leave text/object placement to aesthetic judgment rather than attentional science.

2. **Physiological Annotation (P2 — do second):** Adding PSSL-grade physiological targets to existing pose libraries, color palettes, and breath states. This doesn't change the visual outputs but transforms the *documentation* into training data for LoRA development (per the 7 research proposals).

3. **Validation Gate Expansion (P3 — do third):** The GMG Analyst and CAC Analyst validators should check for gaze-CBCS alignment and physiological intentionality, not just technical compliance (palette, word count, structure).

> [!TIP]
> **None of the prompts need to be rewritten.** The upgrades are annotations, rules, and validation gates — additive layers on top of an already-functional architecture. The research validates the intuition that built these prompts. Now we can make that intuition explicit, measurable, and trainable.
