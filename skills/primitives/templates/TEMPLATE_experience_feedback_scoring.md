# Family Implementation Template: Feedback and Scoring
# Plane: EXPERIENCE
# Family Code: FBK

---

## ⚠️ ANTI-LAZINESS ENFORCEMENT — THIS TASK IS CONSIDERED FAILED IF:

1. **You did not read the book.** Feedback theory (Jane McGonigal's "Reality is Broken" feedback loops, Marczewski's "Feedback Loops" laws) is deep. If your `why_it_works` uses generic "it gives them a score" language without citing the specific feedback type (Direct, Ambient, Cumulative, Social, Delayed) — you have failed.
2. **You wrote generic examples.** Every `examples.context` must name a specific score or feedback moment in CCP (e.g., "The moment the Speaking Benchmark score reveal animation finishes and the 'What this means' text appears").
3. **You left any float at 0.5.** Every float must be a deliberate calibration decision.
4. **You confused feedback with instruction.** FBK primitives govern the **communication of results**, not the teaching of the skill. If your primitive is about "telling them how to do it better," it belongs in `meaning/performance_delivery`.
5. **Your `implementation_targets` are vague.** Specify real score-card components, Telegram UI states, or backend scoring rules.
6. **You wrote `key_pages: "various"`.** Real chapter names required.

### BOOK VERIFICATION LOG (Complete Before Writing Any YAML)

For each book in this batch, confirm:
```
BOOK: [title]
├── Chapters confirmed read: [list at least 2 chapter titles]
├── One feedback mechanism found ONLY in the book (not the audit): [write it]
├── One "feedback burnout" or "meaningless score" warning from the author: [write it]
└── STATUS: VERIFIED / BLOCKED (if blocked, stop and report)
```
**Books for this template:** Reality Is Broken (McGonigal), SuperBetter (McGonigal), Actionable Gamification (Yu-kai Chou), Hooked (Eyal), The Gamification Design Handbook (Marczewski), Beyond Belief (Nir Eyal), Gamify (Brian Burke)

### ANTI-DRIFT RULES (6-Primitive Batch)

- Small batch — zero drift.
- **FBK family float fingerprint**: `user_state_effects.curiosity` and `user_state_effects.status` should be high (0.7–0.9). `user_state_effects.confidence` should also be elevated (0.6–0.8).
- `experience_stage_fit.scoring` and `experience_stage_fit.activation` should be dominant.
- `experience_metrics.react_rate` and `experience_metrics.comeback_rate` are the primary metrics.

### PRE-SAVE CHECKLIST (Check Every Primitive Before Saving)

```
[ ] Book Verification Log completed for this primitive's source book
[ ] PRD_INDEX.md and relevant modular PRDs loaded and referenced
[ ] summary ≠ restatement of core_move
[ ] why_it_works cites a specific feedback mechanism from the book
[ ] EXACTLY 5 examples: 1 BOOK: prefix + 4 CCP: prefixed use cases
[ ] All CCP examples name at least one CCP surface (CCF, CMF, CVE, CBCS, Conscious Reactions, V2WS, CPSC, Telegram, AFFiNE, church/community)
[ ] Zero examples use banned phrases:
    - "a user might use this when" / "in the app" / "in the platform"
[ ] At least 1 anti-example describing a demotivating or confusing score reveal
[ ] No float anywhere is exactly 0.5
[ ] user_state_effects.curiosity is 0.7 or higher
[ ] experience_stage_fit.scoring is 0.8 or higher
[ ] implementation_targets.frontend_components lists real UI elements
[ ] synergizes_with IDs verified in experience catalog
[ ] book_reference.chapters contains real chapter names
[ ] File saved to: primitives/experience/feedback_scoring/[ID].yaml
```

---

## Before You Start
1. Load and read the SKILL file: `skills/primitives/SKILL_Primitive_YAML_Codification.md`
2. Load the golden example: `primitives/experience/_golden/EXP-TRG-001.yaml`
3. Load the experience registry spec: `lab/CCP APRIL Updates/05_Core_Experience/Experience_Primitive_Registry_Spec.md` — Section 4.4
4. Load the PRD router: `docs/prd/modules/PRD_INDEX.md`
5. Load the relevant modular PRDs for this family:
   - `docs/prd/modules/PRD_04_CVE_Experience_Design.md`
   - `docs/prd/modules/PRD_05_CBCS_Law28.md`
   - `docs/prd/modules/PRD_06_Conscious_Reactions.md`
   - `docs/prd/modules/PRD_07_V2WS_Webinar.md`
   - `docs/prd/modules/PRD_08_Conscious_Primitives.md`
   - `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`

## Your Task
Write one YAML file per primitive listed below. Save each to: `primitives/experience/feedback_scoring/[ID].yaml`

## Source Files You Must Load

#### Audit Files
| Audit File | Path | Primitives |
|---|---|---|
| SuperBetter | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_SuperBetter_Jane_McGonigal.md` | FBK-001 |
| Reality Is Broken | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Reality_is_Broken_Jane_McGonigal.md` | FBK-001, FBK-003, FBK-004 |
| Actionable Gamification | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Actionable_Gamification_Yu_kai_Chou.md` | FBK-002 |
| Hooked | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Hooked_Ryan_Hoover.md` | FBK-003 |
| Beyond Belief | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Beyond_Belief_Nir_Eyal.md` | FBK-005 |
| Gamify | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Gamify_How_Gamification_Motivates_People_Brian_Burke.md` | FBK-006 |

#### Book Files (Experience Library)
| Book File | Path |
|---|---|
| Reality Is Broken | `lab/Public Speeaking Coaching/09_Experience_Engineering/Reality is Broken - Jane McGonigal.md` |
| SuperBetter | `lab/Public Speeaking Coaching/09_Experience_Engineering/SuperBetter - Jane McGonigal.md` |
| Actionable Gamification | `lab/Public Speeaking Coaching/09_Experience_Engineering/Actionable Gamification - Yu-kai Chou.md` |
| Hooked | `lab/Public Speeaking Coaching/09_Experience_Engineering/Hooked - Ryan Hoover.md` |
| Beyond Belief | `lab/Public Speeaking Coaching/09_Experience_Engineering/Beyond Belief.md` |
| Gamify | `lab/Public Speeaking Coaching/09_Experience_Engineering/Gamify - Brian Burke.md` |

---

## Primitive Manifest (6 primitives)

| ID | Canonical Name | Source Audit | MCDA | Core Move |
|---|---|---|---:|---|
| EXP-FBK-001 | RIM Feedback Discipline | SuperBetter / Reality is Broken | 180 | Deliver feedback that is Relevant, Immediate, and Meaningful to the user's current goal |
| EXP-FBK-002 | Reflective Scoring | Actionable Gamification / Reality is Broken | 175 | Use scores that mirror the user's own identity and growth path, not just generic points |
| EXP-FBK-003 | The Signature Moment | Reality is Broken / Hooked | 170 | Create a distinct, memorable UI/UX event for the most important feedback reveal |
| EXP-FBK-004 | Bring the Data Forward | Reality is Broken | 170 | Expose hidden progress metrics (e.g., total words spoken, frequency) to build cumulative meaning |
| EXP-FBK-005 | Attention Filtering | Beyond Belief | 175 | Hijack the user's attentional keyhole to focus entirely on progress and allies, nesting and minimizing negative data. |
| EXP-FBK-006 | Theory/Practice Feedback Loops | Gamify | 185 | Ensure that every piece of feedback immediately leads to an opportunity for the user to practice and improve. |

---

## Execution Rules

1. **Batch size**: Process in one batch of 6.
2. **Golden example**: Re-read `EXP-TRG-001.yaml`.
3. **Dual-source gate**: Must read BOTH audit AND book.
4. **PRD gate**: Must load `PRD_INDEX.md` and the family PRD set (PRD_04, PRD_05, PRD_06, PRD_07, PRD_08, PRD_09) before writing any primitive.
5. **Example standard**: Every primitive must produce exactly **5 examples** — 1 BOOK: prefix + 4 CCP: prefixed use cases naming actual CCP surfaces.
6. **Float consistency**: Feedback primitives should have HIGH `user_state_effects.curiosity` (0.7+) and HIGH `experience_stage_fit.scoring` (0.8+).

## Completion Receipt

After finishing all 6 primitives, produce the receipt format specified in the SKILL.
