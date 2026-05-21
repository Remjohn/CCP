# Family Implementation Template: Persuasion
# Plane: MEANING
# Family Code: PRS

## Instructions

You are executing the **Primitive YAML Codification** skill.

### Before You Start
1. Load and read the SKILL file: `skills/primitives/SKILL_Primitive_YAML_Codification.md`
2. Load the golden example: `primitives/meaning/_golden/PRM-HUM-009.yaml`
3. Load the registry catalog: `lab/CCP APRIL Updates/05_Core_Experience/Primitive_Packets_and_Registry_Spec.md` — Section 6.2
4. Load the PRD router: `docs/prd/modules/PRD_INDEX.md`
5. Load the relevant modular PRDs for this family:
   - `docs/prd/modules/PRD_02_CCF_Content_Factory.md`
   - `docs/prd/modules/PRD_04_CVE_Experience_Design.md`
   - `docs/prd/modules/PRD_05_CBCS_Law28.md`
   - `docs/prd/modules/PRD_06_Conscious_Reactions.md`
   - `docs/prd/modules/PRD_07_V2WS_Webinar.md`
   - `docs/prd/modules/PRD_08_Conscious_Primitives.md`
   - `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`

---

## ⚠️ ANTI-LAZINESS ENFORCEMENT — THIS TASK IS CONSIDERED FAILED IF:

1. **You did not read the book.** The audit is a filtered lens. The book is the mechanism. If `why_it_works` cannot be traced to a specific chapter, term, or author claim in the source book file — you have failed.
2. **You wrote generic examples.** Every `examples.context` must name a specific CCP workflow (CMF phase, CCF stage, Telegram mode, webinar moment). "A coach could..." is not a valid context.
3. **You left any float at 0.5.** No float may be left at 0.5. That value signals you did not make a deliberate calibration decision.
4. **Your goal_bias floats are uniformly high.** Persuasion primitives must differentiate. Not every primitive can max out on both `persuasion` AND `clarity`.
5. **You invented synergy IDs.** Verify every ID in `synergizes_with` against the Primitive_Packets_and_Registry_Spec.md catalog before listing.
6. **You wrote `key_pages: "various"`.** Open the book file. Find real chapter names. List them.

### BOOK VERIFICATION LOG (Complete Before Writing Any YAML)

For each book in this batch, confirm:
```
BOOK: [title]
├── Chapters confirmed read: [list at least 2 chapter titles]
├── One mechanism found ONLY in the book (not the audit): [write it]
├── One edge case or warning for anti_examples: [write it]
└── STATUS: VERIFIED / BLOCKED (if blocked, stop and report)
```
**Books for this template:** TED Talks (Anderson), Confessions of a Public Speaker (Berkun), Resonate (Duarte), Talk Like TED (Gallo), HBR 10 Must Reads on Public Speaking

### ANTI-DRIFT RULES (34-Primitive Batch)

- After every 7 primitives, re-read `PRM-HUM-009.yaml` and verify your quality level has not dropped.
- **Persuasion family float fingerprint**: `goal_bias.persuasion` should generally be 0.7–0.9. `goal_bias.surprise` should generally be 0.1–0.3 (persuasion is deliberate, not surprising). If a primitive breaks this pattern, document why in `notes`.
- `ccp_workflow_fit.trigger_provocation` and `ccp_workflow_fit.delivery_coaching` should be the two dominant workflow dimensions for most PRS primitives — if yours aren't, double-check your reasoning.
- No two consecutive primitives from the same source book may share the same `implementation_role`.

### PRE-SAVE CHECKLIST (Check Every Primitive Before Saving)

```
[ ] Book Verification Log completed for this primitive's source book
[ ] PRD_INDEX.md and relevant modular PRDs loaded and referenced
[ ] summary ≠ restatement of core_move
[ ] why_it_works cites a specific book mechanism (not just audit language)
[ ] EXACTLY 5 examples: 1 BOOK: prefix + 4 CCP: prefixed use cases
[ ] All CCP examples name at least one CCP surface (CCF, CMF, CVE, CBCS, Conscious Reactions, V2WS, CPSC, Telegram, AFFiNE, church/community)
[ ] Zero examples use banned phrases:
    - "a coach could use this" / "in content creation" / "in the app" / "in the platform"
[ ] At least 1 anti-example with mechanism-grounded failure reason
[ ] No float anywhere is exactly 0.5
[ ] At least 2 floats are below 0.3 across phase_fit + surface_fit combined
[ ] goal_bias has 1-2 values above 0.7 AND at least 1 at 0.2 or below
[ ] synergizes_with IDs verified in catalog
[ ] book_reference.chapters contains real chapter names
[ ] File saved to: primitives/meaning/persuasion/[ID].yaml
```

---

### Your Task
Write one YAML file per primitive listed below. Save each to: `primitives/meaning/persuasion/[ID].yaml`

### Source Files You Must Load

#### Audit Files
| Audit File | Path | Primitives |
|---|---|---|
| TED Talks | `lab/CCP APRIL Updates/Public_Speaking_Audits/03_Public_Speaking_and_Presentations/AUDIT_TED_Talks_Chris_Anderson.md` | PRM-PRS-028, 030, 029, 034, 031, 032, 033 |
| Confessions of a Public Speaker | `lab/CCP APRIL Updates/Public_Speaking_Audits/03_Public_Speaking_and_Presentations/AUDIT_Confessions_of_a_Public_Speaker_Scott_Berkun.md` | PRM-PRS-001, 002, 003, 005, 004, 006, 007 |
| Resonate | `lab/CCP APRIL Updates/Public_Speaking_Audits/03_Public_Speaking_and_Presentations/AUDIT_Resonate_Nancy_Duarte.md` | PRM-PRS-015, 017, 016, 020, 018, 019, 021 |
| Talk Like TED | `lab/CCP APRIL Updates/Public_Speaking_Audits/03_Public_Speaking_and_Presentations/AUDIT_Talk_Like_TED_Carmine_Gallo.md` | PRM-PRS-022, 024, 023, 026, 025, 027 |
| HBR 10 Must Reads | `lab/CCP APRIL Updates/Public_Speaking_Audits/03_Public_Speaking_and_Presentations/AUDIT_HBRs_10_Must_Reads_on_Public_Speaking_Harvard_Business_Review.md` | PRM-PRS-008, 009, 012, 011, 010, 013, 014 |

#### Book Files
| Book File | Path |
|---|---|
| TED Talks | `lab/Public Speeaking Coaching/03_Public_Speaking_and_Presentations/TED_Talks_-_Chris_J_Anderson.md` |
| Confessions of a Public Speaker | `lab/Public Speeaking Coaching/03_Public_Speaking_and_Presentations/Confessions_of_a_Public_Speaker_-_Scott_Berkun.md` |
| Resonate | `lab/Public Speeaking Coaching/03_Public_Speaking_and_Presentations/Resonate_Present_Visual_Stories_that_Transform_Audiences_-_Nancy_Duarte.md` |
| Talk Like TED | `lab/Public Speeaking Coaching/03_Public_Speaking_and_Presentations/Talk_Like_Ted_-_Carmine_Gallo.md` |
| HBR 10 Must Reads | `lab/Public Speeaking Coaching/03_Public_Speaking_and_Presentations/HBRs_10_Must_Reads_on_Public_Speaking_and_-_Harvard_Business_Review.md` |

---

## Primitive Manifest (34 primitives)

| ID | Canonical Name | Source Audit | MCDA | Core Move |
|---|---|---|---:|---|
| PRM-PRS-028 | Throughline | TED Talks | 196 | Carry one coherent line through the whole experience |
| PRM-PRS-001 | Strong Title as Idea Architecture | Confessions | 194 | Compress the whole idea into a title-level center of gravity |
| PRM-PRS-015 | What-Is / What-Could-Be Contrast Engine | Resonate | 194 | Alternate present reality and possible reality to activate the gap |
| PRM-PRS-022 | 65/25/10 Pathos Allocation | Talk Like TED | 194 | Calibrate emotional load rather than treating passion as an accident |
| PRM-PRS-017 | Big Idea Formulation Protocol | Resonate | 192 | Reduce the whole communication to one transferable idea |
| PRM-PRS-002 | Tension-and-Release Narrative Engine | Confessions | 191 | Hold attention by alternating pressure and relief |
| PRM-PRS-008 | Warmth-Before-Competence Sequencing | HBR 10 | 190 | Establish human safety before making status claims |
| PRM-PRS-009 | Inciting Incident | HBR 10 | 190 | Begin with the event that makes the communication necessary |
| PRM-PRS-030 | Connection Before Content | TED Talks | 190 | Win permission and trust before teaching |
| PRM-PRS-012 | Motivating Language Theory Triad | HBR 10 | 188 | Use direction, empathy, and meaning as distinct channels |
| PRM-PRS-016 | Audience-as-Hero Inversion | Resonate | 188 | Let the audience carry the transformation while you guide |
| PRM-PRS-024 | 18-Minute Cognitive Load Constraint | Talk Like TED | 188 | Respect hard limits of attention and use soft breaks |
| PRM-PRS-029 | Idea-Building as Gift Architecture | TED Talks | 188 | Reconstruct the idea in the listener's mind as an act of generosity |
| PRM-PRS-003 | Audience-First Preparation Protocol | Confessions | 186 | Design from objection, audience need, and reception first |
| PRM-PRS-011 | Conger Four-Step Persuasion Architecture | HBR 10 | 186 | Sequence credibility, shared ground, evidence, and appeal |
| PRM-PRS-020 | Audience Journey Map | Resonate | 186 | Define the movement from current state to desired state |
| PRM-PRS-023 | Emotionally Competent Stimulus | Talk Like TED | 186 | Plant one emotionally vivid moment for memory branding |
| PRM-PRS-034 | Curiosity Ignition | TED Talks | 184 | Open the audience's prediction loop before trying to close it |
| PRM-PRS-018 | S.T.A.R. Moment Architecture | Resonate | 182 | Design a sharp memorable peak to reorganize attention |
| PRM-PRS-026 | Multisensory Delivery Architecture | Talk Like TED | 182 | Stack visual, auditory, and felt signals for retention |
| PRM-PRS-031 | Explanation Engine | TED Talks | 182 | Make complex content traversable without insulting intelligence |
| PRM-PRS-032 | Uncanny Valley Warning | TED Talks | 182 | Avoid over-prepared artificiality that feels inhuman |
| PRM-PRS-005 | Logos-Ethos-Pathos Persuasion Triad | Confessions | 181 | Balance logic, credibility, and emotion |
| PRM-PRS-004 | 10-Minute Attention Architecture | Confessions | 180 | Structure attention in reset-sized blocks |
| PRM-PRS-010 | Four Intents of Authentic Delivery | HBR 10 | 180 | Define delivery intent rather than merely content correctness |
| PRM-PRS-019 | Three-Channel Contrast System | Resonate | 180 | Build contrast at content, emotional, and delivery layers |
| PRM-PRS-025 | Passion-as-Contagion Engine | Talk Like TED | 180 | Let perceived passion transfer state across the audience |
| PRM-PRS-013 | Narrative Coherence Architecture | HBR 10 | 178 | Make identity stories internally legible and credible |
| PRM-PRS-021 | AI-Era Presence Imperative | Resonate | 178 | Use human presence as a defense against genericity |
| PRM-PRS-033 | Five Talk Tools as Modular Palette | TED Talks | 178 | Combine explanation, story, example, humor, and visual |
| PRM-PRS-006 | Eating-the-Microphone Failure Taxonomy | Confessions | 176 | Diagnose common over-performance behaviors |
| PRM-PRS-027 | Authenticity Imperative | Talk Like TED | 176 | Keep preparation from falsifying selfhood |
| PRM-PRS-014 | Berinato Data-Story Visualization Matrix | HBR 10 | 174 | Choose visual form based on the story the data carries |
| PRM-PRS-007 | Teaching as Compassion | Confessions | 172 | Treat explanation as care rather than display |

---

## Execution Rules

1. **Batch size**: Process in groups of 7.
2. **Golden example**: Re-read `PRM-HUM-009.yaml` for calibration.
3. **Dual-source gate**: Must read BOTH audit AND book.
4. **PRD gate**: Must load `PRD_INDEX.md` and the family PRD set (PRD_02, PRD_04, PRD_05, PRD_06, PRD_07, PRD_08, PRD_09) before writing any primitive.
5. **Example standard**: Every primitive must produce exactly **5 examples** — 1 BOOK: prefix + 4 CCP: prefixed use cases naming actual CCP surfaces.
6. **Float consistency**: Persuasion primitives should generally have HIGH `goal_bias.persuasion` (0.7+) and HIGH `goal_bias.clarity` (0.6+).

## Completion Receipt

After finishing all 34 primitives, produce the receipt format specified in the SKILL.
