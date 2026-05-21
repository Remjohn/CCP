# Family Implementation Template: Humor Distortion
# Plane: MEANING
# Family Code: HUM

## Instructions

You are executing the **Primitive YAML Codification** skill.

### Before You Start
1. Load and read the SKILL file: `skills/primitives/SKILL_Primitive_YAML_Codification.md`
2. Load the golden example: `primitives/meaning/_golden/PRM-HUM-009.yaml`
3. Load the registry catalog: `lab/CCP APRIL Updates/05_Core_Experience/Primitive_Packets_and_Registry_Spec.md` — Section 6.1
4. Load the PRD router: `docs/prd/modules/PRD_INDEX.md`
5. Load the relevant modular PRDs for this family:
   - `docs/prd/modules/PRD_02_CCF_Content_Factory.md`
   - `docs/prd/modules/PRD_03_CMF_Media_Factory.md`
   - `docs/prd/modules/PRD_04_CVE_Experience_Design.md`
   - `docs/prd/modules/PRD_05_CBCS_Law28.md`
   - `docs/prd/modules/PRD_06_Conscious_Reactions.md`
   - `docs/prd/modules/PRD_07_V2WS_Webinar.md`
   - `docs/prd/modules/PRD_08_Conscious_Primitives.md`

---

## ⚠️ ANTI-LAZINESS ENFORCEMENT — THIS TASK IS CONSIDERED FAILED IF:

1. **You did not read the book.** Reading the audit alone is not sufficient. The audit is a filtered summary. The book is the mechanism. If your `why_it_works` cannot cite a specific term, concept, or author claim from the actual book file — you have failed.
2. **You wrote generic examples.** Every `examples.context` must name a specific CCP workflow (CMF stage, Telegram mode, CCF phase). "A coach could use this when..." is not a valid context.
3. **You left any float at 0.5.** 0.5 means you did not think about it. Every float must reflect a deliberate calibration decision.
4. **Your float rows are uniformly high.** If all `phase_fit` or `goal_bias` values are above 0.7, you applied no discrimination. Primitives are specialized tools, not general utilities.
5. **You invented synergy IDs.** `synergizes_with` may only list IDs that exist in the Primitive_Packets_and_Registry_Spec.md catalog. Verify before listing.
6. **You wrote `key_pages: "various"`.** Real chapter names and page ranges are required. Open the book file. Find them.

### BOOK VERIFICATION LOG (Complete Before Writing Any YAML)

For each book in this batch, confirm:
```
BOOK: [title]
├── Chapters confirmed read: [list at least 2 chapter titles]
├── One mechanism found ONLY in the book (not the audit): [write it]
├── One edge case or warning from the book for anti_examples: [write it]
└── STATUS: VERIFIED / BLOCKED (if blocked, stop and report)
```
**Books for this template:** How to Write Funny, How to Write Funny Characters, Mastering Stand-Up, The Elements of Humor, The NEW Comedy Bible, The Serious Guide to Joke Writing

### ANTI-DRIFT RULES (40-Primitive Batch)

- After every 7 primitives (one audit source), re-read the golden example `PRM-HUM-009.yaml` and verify you are still at that quality level.
- **Humor family float fingerprint**: `goal_bias.surprise` should generally be 0.6–0.9. `goal_bias.clarity` should generally be 0.1–0.4. If a primitive breaks this pattern, document why in `notes`.
- No two consecutive primitives may share an identical `implementation_role`. If two adjacent primitives would both be `core`, the lower-MCDA one must be `supporting`.
- Your `why_it_works` must not open with the same phrase across more than 2 primitives in a row. Vary the entry point.

### PRE-SAVE CHECKLIST (Check Every Primitive Before Saving)

```
[ ] Book Verification Log completed for this primitive's source book
[ ] PRD_INDEX.md and relevant modular PRDs loaded and referenced
[ ] summary ≠ restatement of core_move
[ ] why_it_works references a specific book mechanism (not just audit language)
[ ] EXACTLY 5 examples: 1 BOOK: prefix + 4 CCP: prefixed use cases
[ ] All CCP examples name at least one CCP surface (CCF, CMF, CVE, CBCS, Conscious Reactions, V2WS, CPSC, Telegram, AFFiNE, church/community)
[ ] Zero examples use banned phrases:
    - "for example, this could be used when..."
    - "a coach could use this"
    - "in content creation"
    - "in the app" / "in the platform"
    - "for content creators" / "when creating content"
[ ] At least 1 anti-example with mechanism-grounded failure reason
[ ] No float anywhere in the file is exactly 0.5
[ ] At least 2 floats are below 0.3 across phase_fit + surface_fit combined
[ ] goal_bias has 1-2 values above 0.7 AND at least 1 value at 0.2 or below
[ ] synergizes_with IDs verified in catalog
[ ] book_reference.chapters contains real chapter names
[ ] File saved to correct path: primitives/meaning/humor_distortion/[ID].yaml
```

---

### Your Task
Write one YAML file per primitive listed below. Save each to: `primitives/meaning/humor_distortion/[ID].yaml`

### Source Files You Must Load

#### Audit Files (load ALL — each contains primitives from this family)
| Audit File | Path | Primitives |
|---|---|---|
| How to Write Funny | `lab/CCP APRIL Updates/Public_Speaking_Audits/01_Humor_and_Comedy/Audit_How_to_Write_Funny_CCP.md` | PRM-HUM-001, 002, 003, 004, 005, 006, 007 |
| How to Write Funny Characters | `lab/CCP APRIL Updates/Public_Speaking_Audits/01_Humor_and_Comedy/Audit_How_to_Write_Funny_Characters.md` | PRM-HUM-008, 009, 010, 011, 012, 013 |
| Mastering Stand-Up | `lab/CCP APRIL Updates/Public_Speaking_Audits/01_Humor_and_Comedy/Audit_Mastering_Stand-Up_CCP.md` | PRM-HUM-014, 015, 016, 017, 018, 019, 020 |
| Elements of Humor | `lab/CCP APRIL Updates/Public_Speaking_Audits/01_Humor_and_Comedy/Audit_The_Elements_of_Humor_CCP.md` | PRM-HUM-021, 022, 023, 024, 025, 026, 027 |
| The NEW Comedy Bible | `lab/CCP APRIL Updates/Public_Speaking_Audits/01_Humor_and_Comedy/Audit_The_NEW_Comedy_Bible_Documentation.md` | PRM-HUM-028, 029, 030, 031, 032, 033, 034 |
| Serious Guide to Joke Writing | `lab/CCP APRIL Updates/Public_Speaking_Audits/01_Humor_and_Comedy/Audit_The_Serious_Guide_to_Joke_Writing_CCP.md` | PRM-HUM-035, 036, 037, 038, 039, 040 |

#### Book Files (load the book corresponding to each audit)
| Book File | Path |
|---|---|
| How to Write Funny | `lab/Public Speeaking Coaching/01_Humor_and_Comedy/How to Write Funny.md` |
| How to Write Funny Characters | `lab/Public Speeaking Coaching/01_Humor_and_Comedy/How to Write Funny Characters.md` |
| Mastering Stand-Up | `lab/Public Speeaking Coaching/01_Humor_and_Comedy/Mastering Stand-Up.md` |
| Elements of Humor | `lab/Public Speeaking Coaching/01_Humor_and_Comedy/The Elements of Humor.md` |
| The NEW Comedy Bible | `lab/Public Speeaking Coaching/01_Humor_and_Comedy/The NEW Comedy Bible.md` |
| Serious Guide to Joke Writing | `lab/Public Speeaking Coaching/01_Humor_and_Comedy/The Serious Guide to Joke Writing.md` |

---

## Primitive Manifest (40 primitives)

Process these in descending MCDA order. For each primitive, follow the 10-step procedure in the SKILL.

| ID | Canonical Name | Source Audit | MCDA | Core Move |
|---|---|---|---:|---|
| PRM-HUM-009 | Reference Funny Filter | How to Write Funny Characters | 195 | Sweeten the character with shared references that make the audience recognize themselves |
| PRM-HUM-037 | Hyper-Specificity Anchoring | Serious Guide to Joke Writing | 195 | Move away from generic nouns into narrow, lived, detailed material |
| PRM-HUM-031 | The Mix | NEW Comedy Bible | 191 | Force two distant domains into one surprising analogy system |
| PRM-HUM-036 | Directed Emotional Stance | Serious Guide to Joke Writing | 190 | Choose the emotional attitude first so the material has charge |
| PRM-HUM-025 | Analogy Bridge | Elements of Humor | 188 | Translate a heavy or abstract truth into a vivid familiar comparison |
| PRM-HUM-010 | High-Contrast Conflict | How to Write Funny Characters | 185 | Cast a character into a setting or opposition where their nature clashes hard |
| PRM-HUM-030 | Setup-Premise-Payoff Architecture | NEW Comedy Bible | 185 | Organize the joke or idea around attitude-bearing premise logic before the release |
| PRM-HUM-035 | Associative Web | Serious Guide to Joke Writing | 185 | Spread laterally through idea associations until something fresh appears |
| PRM-HUM-032 | Rule of Three | NEW Comedy Bible + Talk Like TED | 182 | Establish pattern, establish pattern, break pattern |
| PRM-HUM-002 | Irreducible Truth / Subtext Payload | How to Write Funny + Characters | 182 | Use humor as delivery for a deeper bitter truth rather than as empty decoration |
| PRM-HUM-014 | Joyous Communication | Mastering Stand-Up | 180 | Let the message feel like delighted human broadcast rather than duty |
| PRM-HUM-001 | Dual-Processor Cognitive Engine | How to Write Funny | 178 | Split generation from censorship by separating clown-state production from editor-state refinement |
| PRM-HUM-029 | Act-Out | NEW Comedy Bible | 178 | Shift from description into embodied live scene |
| PRM-HUM-016 | Setup-Punchline Temporal Architecture | Mastering Stand-Up | 176 | Engineer time-based release through setup, delay, and collision |
| PRM-HUM-017 | Attitude-Emotion Binding | Mastering Stand-Up | 176 | Attach a clear emotional attitude to the line so the audience feels intent, not just meaning |
| PRM-HUM-040 | Radical Observational Truth | Serious Guide to Joke Writing | 175 | Start from the deeply true observation before trying to embellish it |
| PRM-HUM-018 | Working Backward Methodology | Mastering Stand-Up | 172 | Begin with what the audience must feel or receive, then reverse-engineer the path |
| PRM-HUM-021 | Irony Inversion | Elements of Humor + Serious Guide | 172 | Expose the gap between what should happen and what actually happens |
| PRM-HUM-003 | Filter Constraints | How to Write Funny | 171 | Distort material through constrained funny filters rather than vague comedic intention |
| PRM-HUM-005 | Absolute Verisimilitude | How to Write Funny | 171 | Keep the world micro-coherent so absurdity lands as believable rather than sloppy |
| PRM-HUM-007 | Production Over-Saturation | How to Write Funny | 170 | Generate enough variants that quality emerges through selection rather than first-pass hope |
| PRM-HUM-034 | Comedy Buddy | NEW Comedy Bible | 168 | Use dialectical punch-up through a second intelligence instead of solo generation |
| PRM-HUM-015 | Persona Sculpting Protocol | Mastering Stand-Up | 165 | Let identity be shaped against audience response rather than declared in abstraction |
| PRM-HUM-026 | Misplaced Focus | Elements of Humor | 165 | Obsess over the wrong detail so the audience auto-corrects and laughs at the distortion |
| PRM-HUM-028 | Authentic Topic Extraction | NEW Comedy Bible | 163 | Mine pain, weirdness, and fear as the real entry point for humor |
| PRM-HUM-019 | Struggle Principle | Mastering Stand-Up | 161 | Make struggle visible so likability rises through vulnerability |
| PRM-HUM-011 | Archetype Shorthand | How to Write Funny Characters | 160 | Use a culturally familiar archetype to reduce explanation cost and accelerate comprehension |
| PRM-HUM-023 | Tribal Reference | Elements of Humor | 160 | Use in-group references that instantly create belonging and recognition |
| PRM-HUM-038 | Expectation Reversal | Serious Guide to Joke Writing | 160 | Let the expected frame harden, then pivot it |
| PRM-HUM-020 | Thought Moment Illusion | Mastering Stand-Up | 158 | Inject human-seeming spontaneity, asymmetry, and live-thought texture |
| PRM-HUM-033 | Dialogue Joke | NEW Comedy Bible | 158 | Reconstruct the conversation as it should have happened so the rebuttal lands cleanly |
| PRM-HUM-006 | Temporal Resolution Delay | How to Write Funny | 156 | Hold the funny or revealing part until the latest viable position |
| PRM-HUM-024 | Metahumor and Frame Breaking | Elements of Humor | 154 | Comment on the frame itself to create a second-level release |
| PRM-HUM-004 | Contrastive Extreme Polarization | How to Write Funny | 150 | Heighten semantic distance to sharpen the anomaly and force attention |
| PRM-HUM-008 | Character Funny Filter | How to Write Funny Characters | 145 | Create laughter by making the character act predictably according to a clear trait rule |
| PRM-HUM-022 | Character Mask | Elements of Humor | 145 | Borrow a persona or role to create safer distance for sharper truths |
| PRM-HUM-039 | What-If Sandbox | Serious Guide to Joke Writing | 145 | Explore absurd extrapolations safely to reveal overlooked truths |
| PRM-HUM-027 | Hyperbolic Scaling | Elements of Humor | 138 | Stretch scale beyond normal bounds to intensify a truth |
| PRM-HUM-012 | Two-Dimensional Representation Strategy | How to Write Funny Characters | 135 | Compress a comic persona into a narrow representational function instead of full realism |
| PRM-HUM-013 | Intuiting Method | How to Write Funny Characters | 110 | Observe real humans and translate their strange live traits into material |

---

## Execution Rules

1. **Batch size**: Process in groups of 7 (matching audit source). Complete one audit's primitives before moving to the next.
2. **Golden example**: Re-read `PRM-HUM-009.yaml` before starting each batch to maintain calibration.
3. **Dual-source gate**: For each primitive, confirm you have read BOTH the audit description AND the book chapter. If either is missing, log the gap and move to the next primitive.
4. **PRD gate**: Must load `PRD_INDEX.md` and the family PRD set (PRD_02, PRD_03, PRD_04, PRD_05, PRD_06, PRD_07, PRD_08) before writing any primitive.
5. **Example standard**: Every primitive must produce exactly **5 examples** — 1 BOOK: prefix + 4 CCP: prefixed use cases naming actual CCP surfaces.
6. **Float consistency**: Within this family, humor primitives should generally have HIGH `goal_bias.surprise` (0.6+) and LOW `goal_bias.clarity` (0.1-0.4). If a primitive breaks this pattern, explain why in `notes`.
7. **Synergy mapping**: Within the humor family, map synergies liberally. Across families, be selective — only list cross-family synergies that are genuinely useful in coalition formation.

## Completion Receipt

After finishing all 40 primitives, produce the receipt format specified in the SKILL.
