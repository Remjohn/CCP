# Family Implementation Template: Narrative Structure
# Plane: MEANING
# Family Code: STR

## Instructions

You are executing the **Primitive YAML Codification** skill.

### Before You Start
1. Load and read the SKILL file: `skills/primitives/SKILL_Primitive_YAML_Codification.md`
2. Load the golden example: `primitives/meaning/_golden/PRM-HUM-009.yaml`
3. Load the registry catalog: `lab/CCP APRIL Updates/05_Core_Experience/Primitive_Packets_and_Registry_Spec.md` — Section 6.3
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

1. **You did not read the book.** The audit is not the book. If `why_it_works` reads like something you could write without opening the book file — rewrite it. It must carry the author's specific theoretical fingerprint.
2. **You wrote generic examples.** Every `examples.context` must name a specific CCP workflow stage. "A storytelling primitive can be used in content creation" is not an example — it is noise.
3. **You left any float at 0.5.** Float 0.5 = no decision made. Every float requires a deliberate reasoning choice.
4. **Your float rows are uniformly high.** Narrative primitives differ substantially in their phase fit. Some are pre-trigger (story discovery), some are generation-phase, some are delivery-phase. These distinctions must show in the floats.
5. **You invented synergy IDs.** Verify every `synergizes_with` ID in the catalog before listing.
6. **You wrote `key_pages: "various"`.** Open the book. Find the chapters. Name them.

### BOOK VERIFICATION LOG (Complete Before Writing Any YAML)

For each book in this batch, confirm:
```
BOOK: [title]
├── Chapters confirmed read: [list at least 2 chapter titles]
├── One mechanism found ONLY in the book (not the audit): [write it]
├── One warning or contraindication from the author for anti_examples: [write it]
└── STATUS: VERIFIED / BLOCKED (if blocked, stop and report)
```
**Books for this template:** Bird by Bird (Lamott), DataStory / Illuminate (Duarte), How to Tell a Story (Bowles), The Screenwriter's Bible (Trottier), Save the Cat (Snyder), My Story Can Beat Up Your Story (Schechter)

### ANTI-DRIFT RULES (27-Primitive Batch)

- After every 7 primitives, re-read `PRM-HUM-009.yaml` and verify quality has not drifted.
- **Narrative family float fingerprint**: `goal_bias.memorability` should generally be 0.7–0.9. `goal_bias.tension` should be present (0.5+) in most structural primitives. `goal_bias.persuasion` should be 0.3 or below for story-discovery primitives (these are about finding truth, not selling).
- Primitives from Bird by Bird typically have HIGH `phase_fit.pre_trigger` (discovery/access phase). Screenwriting primitives have HIGH `phase_fit.generation`. Make sure these distinctions show up.
- No two consecutive primitives may have the same `implementation_role`.

### PRE-SAVE CHECKLIST (Check Every Primitive Before Saving)

```
[ ] Book Verification Log completed for this primitive's source book
[ ] PRD_INDEX.md and relevant modular PRDs loaded and referenced
[ ] summary ≠ restatement of core_move
[ ] why_it_works cites a specific book mechanism (not just audit language)
[ ] EXACTLY 5 examples: 1 BOOK: prefix + 4 CCP: prefixed use cases
[ ] All CCP examples name at least one CCP surface (CCF, CMF, CVE, CBCS, Conscious Reactions, V2WS, CPSC, Telegram, AFFiNE, church/community)
[ ] Zero examples use banned phrases:
    - "for example, this could be used when..."
    - "a coach could use this"
    - "in content creation"
    - "in the app" / "in the platform"
    - "for content creators" / "when creating content"
[ ] At least 1 anti-example with mechanism-grounded failure reason
[ ] No float anywhere is exactly 0.5
[ ] At least 2 floats are below 0.3 across phase_fit + surface_fit combined
[ ] goal_bias has 1-2 values above 0.7 AND at least 1 at 0.2 or below
[ ] synergizes_with IDs verified in catalog
[ ] book_reference.chapters contains real chapter names
[ ] File saved to: primitives/meaning/narrative_structure/[ID].yaml
```

---

### Your Task
Write one YAML file per primitive listed below. Save each to: `primitives/meaning/narrative_structure/[ID].yaml`

### Source Files You Must Load

#### Audit Files
| Audit File | Path | Primitives |
|---|---|---|
| Bird by Bird | `lab/CCP APRIL Updates/Public_Speaking_Audits/04_Storytelling_and_Narrative_Design/AUDIT Bird by Bird Anne Lamott.md` | PRM-STR-001, 002, 003, 004, 005, 006, 007 |
| DataStory / Illuminate | `lab/CCP APRIL Updates/Public_Speaking_Audits/04_Storytelling_and_Narrative_Design/AUDIT DataStory Illuminate Nancy Duarte.md` | PRM-STR-008, 009, 010, 011, 012, 013 |
| How to Tell a Story | `lab/CCP APRIL Updates/Public_Speaking_Audits/04_Storytelling_and_Narrative_Design/AUDIT How to Tell a Story Meg Bowles.md` | PRM-STR-014, 015, 016, 017, 018, 019, 020 |
| Screenwriting Architecture | `lab/CCP APRIL Updates/Public_Speaking_Audits/04_Storytelling_and_Narrative_Design/AUDIT Screenwriting Architecture Trottier Snyder Schechter.md` | PRM-STR-021, 022, 023, 024, 025, 026, 027 |

#### Book Files
| Book File | Path |
|---|---|
| Bird by Bird | `lab/Public Speeaking Coaching/04_Storytelling_and_Narrative_Design/Bird By Bird Instructions On Writing n Life 2020 edition UK - Anne Lamott.md` |
| DataStory | `lab/Public Speeaking Coaching/04_Storytelling_and_Narrative_Design/DataStory Explain Data and Inspire Action Through Story - Nancy Duarte.md` |
| Illuminate | `lab/Public Speeaking Coaching/04_Storytelling_and_Narrative_Design/Illuminate Ignite Change Through Speeches - Nancy Duarte.md` |
| How to Tell a Story | `lab/Public Speeaking Coaching/04_Storytelling_and_Narrative_Design/How to Tell a Story - Meg Bowles.md` |
| Screenwriter's Bible | `lab/Public Speeaking Coaching/04_Storytelling_and_Narrative_Design/The Screenwriters Bible - David trottler.md` |
| Save the Cat | `lab/Public Speeaking Coaching/04_Storytelling_and_Narrative_Design/Save the Cat - Blake Snyder.md` |
| My Story Can Beat Up Your Story | `lab/Public Speeaking Coaching/04_Storytelling_and_Narrative_Design/My Story Can Beat Up Your Story - Jeffrey Schechter.md` |

---

## Primitive Manifest (27 primitives)

| ID | Canonical Name | Source Audit | MCDA | Core Move |
|---|---|---|---:|---|
| PRM-STR-013 | Change Choreography | DataStory / Illuminate | 194 | Use stories and symbols as transformation moments |
| PRM-STR-006 | Unsilenced Voice | Bird by Bird | 192 | Recover owned voice by removing borrowed permission |
| PRM-STR-008 | Data Point of View | DataStory / Illuminate | 192 | Force data to carry a stance and a consequence |
| PRM-STR-019 | Narrative Stepping Stones | How to Tell a Story | 190 | Break the journey into usable units that preserve movement |
| PRM-STR-023 | Goal-Opposition-Stakes Spine | Screenwriting | 189 | Organize movement around desire, obstruction, and consequence |
| PRM-STR-026 | Scene Engineering | Screenwriting | 188 | Give every unit a purpose, motion, and polarity |
| PRM-STR-011 | Humanize Information | DataStory / Illuminate | 187 | Attach character and conflict to abstract information |
| PRM-STR-015 | Stakes as the Personal Why | How to Tell a Story | 187 | Define what is truly at stake internally and externally |
| PRM-STR-018 | One-Sentence Lens | How to Tell a Story | 186 | Compress the heart of the story into one sentence |
| PRM-STR-024 | Beat Architecture | Screenwriting | 186 | Sequence emotional thresholds rather than information |
| PRM-STR-020 | Vulnerable Specificity | How to Tell a Story | 185 | Use concrete vulnerable detail to magnify trust |
| PRM-STR-009 | Audience-State Empathy | DataStory / Illuminate | 184 | Detect audience stage before choosing tone |
| PRM-STR-025 | Theme as Argument | Screenwriting | 184 | Let content stage and test a worldview claim |
| PRM-STR-001 | Bird-by-Bird Framing | Bird by Bird | 183 | Reduce scale to approach truth without overwhelm |
| PRM-STR-016 | Anecdote-to-Story Conversion | How to Tell a Story | 182 | Turn a recounting into a story with shift and meaning |
| PRM-STR-021 | Promise of the Premise | Screenwriting | 182 | Promise a definite experience, then cash it |
| PRM-STR-014 | Memory Mining Through Story Seeds | How to Tell a Story | 180 | Locate alive memory fragments before grand narrative |
| PRM-STR-027 | Dual-Track Transformation | Screenwriting | 180 | Bind outer events and inner identity change |
| PRM-STR-002 | Shitty First Drafts | Bird by Bird | 179 | Separate access from evaluation to surface material |
| PRM-STR-005 | Moral Point of View | Bird by Bird | 179 | Ensure the piece stands for something beyond competence |
| PRM-STR-010 | Recommendation Trees | DataStory / Illuminate | 178 | Support claims with what/why/how branching logic |
| PRM-STR-017 | Decision-Change Arc | How to Tell a Story | 178 | Track the choice that changed the path and self |
| PRM-STR-022 | Sympathy Engineering | Screenwriting | 176 | Build bonding before challenge or complexity |
| PRM-STR-007 | Writing as Gift | Bird by Bird | 175 | Frame communication as offering rather than display |
| PRM-STR-004 | Broccoli vs KFKD | Bird by Bird | 173 | Distinguish living intuition from inner-noise |
| PRM-STR-012 | Reveal Design | DataStory / Illuminate | 171 | Control order of exposure for staged understanding |
| PRM-STR-003 | Polaroid Development Model | Bird by Bird | 163 | Let the truth come into focus gradually |

---

## Execution Rules

1. **Batch size**: Process in groups of 7.
2. **Golden example**: Re-read `PRM-HUM-009.yaml`.
3. **Dual-source gate**: Must read BOTH audit AND book.
4. **PRD gate**: Must load `PRD_INDEX.md` and the family PRD set (PRD_02, PRD_03, PRD_04, PRD_05, PRD_06, PRD_07, PRD_08) before writing any primitive.
5. **Example standard**: Every primitive must produce exactly **5 examples** — 1 BOOK: prefix + 4 CCP: prefixed use cases naming actual CCP surfaces.
6. **Float consistency**: Narrative primitives should have HIGH `goal_bias.memorability` (0.7+) and HIGH `goal_bias.tension` (0.6+).

## Completion Receipt

After finishing all 27 primitives, produce the receipt format specified in the SKILL.
