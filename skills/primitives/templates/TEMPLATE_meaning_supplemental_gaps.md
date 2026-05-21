# Family Implementation Template: Supplemental Gaps (PSY & VSG)
# Plane: MEANING
# Family Code: PSY / VSG

---

## ⚠️ ANTI-LAZINESS ENFORCEMENT — THIS TASK IS CONSIDERED FAILED IF:

1. **You did not read the book.** These primitives come from sophisticated books on performance, photography, filmmaking, and sound design. If your `why_it_works` does not contain specific terminology from the source book (e.g. Transactional Analysis, punctum, rack focus, density budgeting) — you have failed.
2. **You wrote generic examples.** Every `examples.context` must name a specific CCP workflow stage (CMF carousel generation, V2WS Webinar composition, CCF archetype visual curation). "A coach could use this when..." is not a valid context.
3. **You left any float at 0.5.** Every float must be a deliberate calibration decision based on the specific primitive's role.
4. **You conflated text with visual or sonic.** For VSG primitives, `surface_fit.visual` or `surface_fit.sonic` must be the highest. For PSY primitives, `surface_fit.text` and `surface_fit.voice` usually lead. If you fail to distinguish these properly, you have misclassified it.
5. **You invented synergy IDs.** Verify every ID in `synergizes_with` against the catalog before listing.
6. **You wrote `key_pages: "various"`.** Real chapter names and page ranges are required. Open the book file.

### BOOK VERIFICATION LOG (Complete Before Writing Any YAML)

For each book in this batch, confirm:
```
BOOK: [title]
├── Chapters confirmed read: [list at least 2 chapter titles]
├── One mechanism found ONLY in the book (not the audit): [write it]
├── One warning or failure mode for anti_examples: [write it]
└── STATUS: VERIFIED / BLOCKED (if blocked, stop and report)
```
**Books for this template:** Born a Crime (Noah), Photography Story Composition (Beales/Freeman/Barthes), The Filmmaker's Eye (Mercado), Sound Design (Harrison/Lawrence/Murch).

### ANTI-DRIFT RULES (27-Primitive Batch)

- After every 6 primitives, re-read the golden example `PRM-HUM-009.yaml` and verify quality levels.
- **VSG family float fingerprint**: `goal_bias.clarity` or `goal_bias.tension` should be dominant. `surface_fit.visual` and `surface_fit.sonic` should be the dominant surfaces. `phase_fit.delivery` and `phase_fit.revision` should be high (0.7+) for most VSG primitives.
- **PSY family float fingerprint**: `goal_bias.connection` and `goal_bias.persuasion` should be elevated. `phase_fit.pre_trigger` and `phase_fit.post_trigger` are usually high for diagnostics.
- No two consecutive primitives may share an identical `implementation_role`.

### PRE-SAVE CHECKLIST (Check Every Primitive Before Saving)

```
[ ] Book Verification Log completed for this primitive's source book
[ ] PRD_INDEX.md and relevant modular PRDs loaded and referenced
[ ] summary ≠ restatement of core_move
[ ] why_it_works cites a specific mechanism from the book
[ ] EXACTLY 5 examples: 1 BOOK: prefix + 4 CCP: prefixed use cases
[ ] All CCP examples name at least one CCP surface (CCF, CMF, CVE, CBCS, Conscious Reactions, V2WS, CPSC, Telegram, AFFiNE, church/community)
[ ] Zero examples use banned phrases:
    - "a coach could use this" / "in content creation" / "in the app" / "in the platform"
[ ] At least 1 anti-example with mechanism-grounded failure reason
[ ] No float anywhere in the file is exactly 0.5
[ ] For VSG: surface_fit.visual or surface_fit.sonic is 0.7 or higher
[ ] synergizes_with IDs verified in catalog
[ ] book_reference.chapters contains real chapter names
[ ] File saved to: primitives/meaning/[family_name]/[ID].yaml
```

---

## Before You Start
1. Load and read the SKILL file: `skills/primitives/SKILL_Primitive_YAML_Codification.md`
2. Load the golden example: `primitives/meaning/_golden/PRM-HUM-009.yaml`
3. Load the registry catalog: `lab/CCP APRIL Updates/05_Core_Experience/Primitive_Packets_and_Registry_Spec.md` — Section 6.4 (PSY) and 6.7 (VSG).
4. Load the PRD router: `docs/prd/modules/PRD_INDEX.md`
5. Load the relevant modular PRDs for this family:
   - `docs/prd/modules/PRD_02_CCF_Content_Factory.md`
   - `docs/prd/modules/PRD_03_CMF_Media_Factory.md`
   - `docs/prd/modules/PRD_04_CVE_Experience_Design.md`
   - `docs/prd/modules/PRD_05_CBCS_Law28.md`
   - `docs/prd/modules/PRD_06_Conscious_Reactions.md`
   - `docs/prd/modules/PRD_07_V2WS_Webinar.md`
   - `docs/prd/modules/PRD_08_Conscious_Primitives.md`
   - `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`

## Your Task
Write one YAML file per primitive listed below. 
Save PSY primitives to: `primitives/meaning/psychological_diagnostics/[ID].yaml`
Save VSG primitives to: `primitives/meaning/visual_sonic_guidance/[ID].yaml`

## Source Files You Must Load

#### Audit Files
| Audit File | Path | Primitives |
|---|---|---|
| Born a Crime | `lab/CCP APRIL Updates/Public_Speaking_Audits/05_Psychology_and_Communication/AUDIT_Born_a_Crime.md` | PRM-PSY-013 to 019 |
| One to Many (Fladlien) | `lab/Public Speeaking Coaching/05_Psychology_and_Communication/AUDIT_One_to_Many_Jason_Fladlien.md` | PRM-PSY-020 to 026 |
| Photography / Composition | `lab/CCP APRIL Updates/Public_Speaking_Audits/07_Photography_and_Composition/AUDIT Photography Story Composition Beales Freeman Barthes.md` | PRM-VSG-015 to 021 |
| The Filmmaker's Eye | `lab/CCP APRIL Updates/Public_Speaking_Audits/07_Photography_and_Composition/AUDIT The Filmmakers Eye Gustavo Mercado.md` | PRM-VSG-022 to 028 |
| Sound Design | `lab/CCP APRIL Updates/Public_Speaking_Audits/08_Sound_Design/AUDIT Sound Design Harrison Lawrence Murch.md` | PRM-VSG-029 to 034 |

#### Book Files
Ensure you locate and read the corresponding source books in the `lab/Public Speeaking Coaching/` directories to extract precise page numbers, chapter titles, and technical vocabulary.

---

## Primitive Manifest (27 primitives)

### PSYCHOLOGY AND COMMUNICATION (PSY)
| ID | Canonical Name | Source Audit | MCDA | Core Move |
|---|---|---|---:|---|
| PRM-PSY-013 | Chameleon Protocol: Language as Identity | Born a Crime | 186 | Calibrate linguistic identity (register, diction) so the audience recognizes you as a peer. |
| PRM-PSY-014 | Trojan Horse Narrative: Comedy as Bypass | Born a Crime | 178 | Use humor to bypass cognitive resistance before delivering a challenging truth. |
| PRM-PSY-015 | Outsider Advantage: Marginality as Strategy | Born a Crime | 178 | Leverage an outsider perspective to make invisible constraints visible to the audience. |
| PRM-PSY-016 | Systemic Subversion Model | Born a Crime | 184 | Reframe a personal story to make it a diagnostic lens of a broken system. |
| PRM-PSY-017 | Empathy Inversion | Born a Crime | 182 | Force the listener to experience the emotional reality of the opposition. |
| PRM-PSY-018 | Layered Narrative Architecture | Born a Crime | 176 | Teach structural insights implicitly through story sequencing. |
| PRM-PSY-019 | Resilience Reframe | Born a Crime | 186 | Transform vulnerability from victimhood into authority by demonstrating agency. |
| PRM-PSY-020 | The Paradox of Value (Singular Path Mechanism) | One to Many | 194 | Artificially restrict options to provide one clear, easy route to the desired outcome, destroying decision fatigue. |
| PRM-PSY-021 | Knowing vs. Feeling (Emotional Context) | One to Many | 181 | Shift the speaker's responsibility from information delivery to state management. |
| PRM-PSY-022 | The Iterative Filter (Spew and Whittle) | One to Many | 179 | Dump information without censorship, then ruthlessly delete anything not serving the Singular Path. |
| PRM-PSY-023 | Audience Ecological Checks | One to Many | 177 | Systematically review content to ensure it does not violate the internal emotional ecosystem of the audience. |
| PRM-PSY-024 | Universal Webinar Emotion Palette | One to Many | 188 | Deliberately orchestrate specific neurotransmitter cascades (Fear, Enthusiasm, Safety) at precise moments in the narrative arc. |
| PRM-PSY-025 | Clearly Defined Outcome Formula | One to Many | 185 | Define the premise using a rigid Audience + Feeling + Result formula that passes the 60-minute test. |
| PRM-PSY-026 | Instant Gratification Hook | One to Many | 183 | Provide a micro-result achievable immediately to bridge the trust gap before a long-term promise. |

### VISUAL AND SONIC GUIDANCE (VSG)
| ID | Canonical Name | Source Audit | MCDA | Core Move |
|---|---|---|---:|---|
| PRM-VSG-015 | Composition as Attention Routing | Photography Composition | 192 | Deliberately route attention so the viewer knows what to notice first, second, and third. |
| PRM-VSG-016 | Light and Color as Emotional Architecture | Photography Composition | 186 | Turn a scene from inert description into mood, tension, or aspiration. |
| PRM-VSG-017 | Character, Location, Event | Photography Composition | 182 | Ensure the image contains a narrative triad rather than being a generic pose. |
| PRM-VSG-018 | Sequence Over Single Image | Photography Composition | 178 | Build meaning across multiple frames (carousels, reels) rather than one visual. |
| PRM-VSG-019 | Story Gap as Visual Engine | Photography Composition | 171 | Leave enough ambiguity that the viewer is forced to infer the larger reality. |
| PRM-VSG-020 | Perspective and Layering as Meaning | Photography Composition | 167 | Use depth and framing to imply psychological relationship and scale. |
| PRM-VSG-021 | Punctum, Air, and Felt Truth | Photography Composition | 160 | Include an arresting detail or flaw that gives the image a feeling of lived reality. |
| PRM-VSG-022 | Selective Focus as Meaning Control | Filmmaker's Eye | 191 | Use focus to determine what remains dominant and what lingers as contextual pressure. |
| PRM-VSG-023 | Lens Choice as Emotional Syntax | Filmmaker's Eye | 188 | Use focal length to imply emotional relationships between subjects and environments. |
| PRM-VSG-024 | Space as Psychological Relationship | Filmmaker's Eye | 183 | Manipulate perspective to convert geography into psychology. |
| PRM-VSG-025 | Intangibles and Optical Personality | Filmmaker's Eye | 178 | Use optical imperfections to imply history, realism, and documentary presence. |
| PRM-VSG-026 | Image Systems, Not Isolated Shots | Filmmaker's Eye | 176 | Establish a visual norm and break it to communicate psychological shifts. |
| PRM-VSG-027 | Movement Perception Through Lens Behavior | Filmmaker's Eye | 169 | Alter felt velocity and tension through focal length and spacing. |
| PRM-VSG-028 | Distortion as Subjectivity | Filmmaker's Eye | 160 | Use optical warping intentionally to communicate altered perception. |
| PRM-VSG-029 | Density / Clarity Budgeting | Sound Design | 188 | Manage density of sound layers so the core signal remains perfectly clear. |
| PRM-VSG-030 | Listener Custody / Greatest-Impact Thinking | Sound Design | 186 | Ensure the most important sound is always the easiest to hear. |
| PRM-VSG-031 | Negative Space / Silence Control | Sound Design | 183 | Use the absence of sound dynamically to create tension or reveal context. |
| PRM-VSG-032 | Reason-for-Everything Verification | Sound Design | 180 | Interrogate every sonic choice to ensure it serves the primary narrative intent. |
| PRM-VSG-033 | Encoded vs Embodied Sound Routing | Sound Design | 178 | Balance intellectual sound cues with visceral sound cues for total impact. |
| PRM-VSG-034 | Motif / Foreshadowing Map | Sound Design | 175 | Structure repeating sonic signatures so the ear learns the language. |

---

## Execution Rules

1. **Batch size**: Process in groups of 6-7.
2. **Golden example**: Re-read `PRM-HUM-009.yaml`.
3. **Dual-source gate**: Must read BOTH audit AND book.
4. **PRD gate**: Must load `PRD_INDEX.md` and the combined family PRD set before writing any primitive.
5. **Example standard**: Every primitive must produce exactly **5 examples** — 1 BOOK: prefix + 4 CCP: prefixed use cases naming actual CCP surfaces.
6. **Float consistency**: PSY primitives should have HIGH `goal_bias.connection` (0.7+). VSG primitives should have HIGH `goal_bias.clarity` (0.7+) or `goal_bias.tension` (0.7+).

## Completion Receipt

After finishing all 27 primitives, produce the receipt format specified in the SKILL.
