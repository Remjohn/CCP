# Family Implementation Template: Progression and Replay
# Plane: EXPERIENCE
# Family Code: PRG

---

## ⚠️ ANTI-LAZINESS ENFORCEMENT — THIS TASK IS CONSIDERED FAILED IF:

1. **You did not read the book.** Progression theory (Marczewski's "Player Journey", Jane McGonigal's "Epic Wins", Hoover's "Investment Phase") is technical. If your `why_it_works` uses generic "it keeps them going" language without citing the specific stage (Discovery, Onboarding, Scaffolding, Mastery) — you have failed.
2. **You wrote generic examples.** Every `examples.context` must name a specific progression moment in CCP (e.g., "The transition from the 7-day challenge Day 7 reveal to the 'Next Level' subscription prompt").
3. **You left any float at 0.5.** Every float must be a deliberate calibration decision.
4. **You confused progression with onboarding.** PRG primitives govern the **long-term arc and repetition**, not the first 5 minutes. If your primitive is only about the first encounter, it belongs in `trust_branding`.
5. **Your `implementation_targets` are vague.** Specify real progress components, Telegram streak rules, or backend replay logic.
6. **You wrote `key_pages: "various"`.** Real chapter names required.

### BOOK VERIFICATION LOG (Complete Before Writing Any YAML)

For each book in this batch, confirm:
```
BOOK: [title]
├── Chapters confirmed read: [list at least 2 chapter titles]
├── One progression mechanism found ONLY in the book (not the audit): [write it]
├── One "progression wall" or "replay fatigue" warning from the author: [write it]
└── STATUS: VERIFIED / BLOCKED (if blocked, stop and report)
```
**Books for this template:** Reality Is Broken (McGonigal), Hooked (Eyal), The Gamification Design Handbook (Marczewski), Actionable Gamification (Yu-kai Chou), Designing for Behavior Change (Wendel), Beyond Belief (Nir Eyal), Gamify (Brian Burke)

### ANTI-DRIFT RULES (7-Primitive Batch)

- Small batch — zero drift.
- **PRG family float fingerprint**: `user_state_effects.replay_desire` and `user_state_effects.curiosity` should be high (0.7–0.9). `user_state_effects.belonging` should also be elevated (0.5–0.7).
- `experience_stage_fit.retention` and `experience_stage_fit.retention` should be dominant.
- `experience_metrics.comeback_rate` and `experience_metrics.day7_retention` are the primary metrics.

### PRE-SAVE CHECKLIST (Check Every Primitive Before Saving)

```
[ ] Book Verification Log completed for this primitive's source book
[ ] PRD_INDEX.md and relevant modular PRDs loaded and referenced
[ ] summary ≠ restatement of core_move
[ ] why_it_works cites a specific progression mechanism from the book
[ ] EXACTLY 5 examples: 1 BOOK: prefix + 4 CCP: prefixed use cases
[ ] All CCP examples name at least one CCP surface (CCF, CMF, CVE, CBCS, Conscious Reactions, V2WS, CPSC, Telegram, AFFiNE, church/community)
[ ] Zero examples use banned phrases:
    - "a user might use this when" / "in the app" / "in the platform"
[ ] At least 1 anti-example describing a progression loop that feels like a chore
[ ] No float anywhere is exactly 0.5
[ ] user_state_effects.replay_desire is 0.7 or higher
[ ] experience_stage_fit.retention is 0.8 or higher
[ ] implementation_targets.backend_rules lists real logic (e.g., streak reset rules)
[ ] synergizes_with IDs verified in experience catalog
[ ] book_reference.chapters contains real chapter names
[ ] File saved to: primitives/experience/progression_replay/[ID].yaml
```

---

## Before You Start
1. Load and read the SKILL file: `skills/primitives/SKILL_Primitive_YAML_Codification.md`
2. Load the golden example: `primitives/experience/_golden/EXP-TRG-001.yaml`
3. Load the experience registry spec: `lab/CCP APRIL Updates/05_Core_Experience/Experience_Primitive_Registry_Spec.md` — Section 4.5
4. Load the PRD router: `docs/prd/modules/PRD_INDEX.md`
5. Load the relevant modular PRDs for this family:
   - `docs/prd/modules/PRD_04_CVE_Experience_Design.md`
   - `docs/prd/modules/PRD_05_CBCS_Law28.md`
   - `docs/prd/modules/PRD_06_Conscious_Reactions.md`
   - `docs/prd/modules/PRD_07_V2WS_Webinar.md`
   - `docs/prd/modules/PRD_08_Conscious_Primitives.md`
   - `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`

## Your Task
Write one YAML file per primitive listed below. Save each to: `primitives/experience/progression_replay/[ID].yaml`

## Source Files You Must Load

#### Audit Files
| Audit File | Path | Primitives |
|---|---|---|
| Hooked | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Hooked_Ryan_Hoover.md` | PRG-001 |
| The Gamification Design Handbook | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_The_Gamification_Design_Handbook_Andrzej_Marczewski.md` | PRG-002 |
| Actionable Gamification | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Actionable_Gamification_Yu_kai_Chou.md` | PRG-002 |
| Reality Is Broken | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Reality_is_Broken_Jane_McGonigal.md` | PRG-003 |
| Designing for Behavior Change | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Designing_for_Behavior_Change_Stephen_Wendel.md` | PRG-004 |
| Beyond Belief | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Beyond_Belief_Nir_Eyal.md` | PRG-005, PRG-006 |
| Gamify | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Gamify_How_Gamification_Motivates_People_Brian_Burke.md` | PRG-007 |

#### Book Files (Experience Library)
| Book File | Path |
|---|---|
| Reality Is Broken | `lab/Public Speeaking Coaching/09_Experience_Engineering/Reality is Broken - Jane McGonigal.md` |
| Hooked | `lab/Public Speeaking Coaching/09_Experience_Engineering/Hooked - Ryan Hoover.md` |
| The Gamification Design Handbook | `lab/Public Speeaking Coaching/09_Experience_Engineering/The Gamification Design Handbook - Andrzej Marczewski.md` |
| Actionable Gamification | `lab/Public Speeaking Coaching/09_Experience_Engineering/Actionable Gamification - Yu-kai Chou.md` |
| Designing for Behavior Change | `lab/Public Speeaking Coaching/09_Experience_Engineering/Designing for Behavior Change - Stephen Wendel.md` |
| Beyond Belief | `lab/Public Speeaking Coaching/09_Experience_Engineering/Beyond Belief.md` |
| Gamify | `lab/Public Speeaking Coaching/09_Experience_Engineering/Gamify - Brian Burke.md` |

---

## Primitive Manifest (7 primitives)

| ID | Canonical Name | Source Audit | MCDA | Core Move |
|---|---|---|---:|---|
| EXP-PRG-001 | Hook Cycle Velocity | Hooked | 185 | Design the loop so the time between Trigger and Reward is as short as possible |
| EXP-PRG-002 | Discover -> On-board -> Immerse -> Master -> Replay | Marczewski / Actionable Gamification | 178 | Explicitly design the user's transition through these five distinct engagement phases |
| EXP-PRG-003 | Go for an Epic Win | Reality Is Broken | 160 | Create rare, high-stakes opportunities that require cumulative effort and yield massive emotional reward |
| EXP-PRG-004 | Long Loops for Habit Formation | Designing for Behavior Change | 145 | Design the system to support behaviors that take weeks or months to stabilize, not just one-off wins |
| EXP-PRG-005 | The Placebo Onboarding | Beyond Belief | 180 | Engineer the loading screens to create positive anticipation and lower anxiety, acting as a psychological placebo. |
| EXP-PRG-006 | Motivation Triangle UI | Beyond Belief | 175 | Ensure every challenge explicitly injects the Belief that the user can succeed, rather than just presenting Behavior and Benefit. |
| EXP-PRG-007 | Live-Ops Freshness and Embeddedness | Gamify | 178 | Refresh the system continuously through new topics and variant formats to prevent the repetition from feeling like a second job. |

---

## Execution Rules

1. **Batch size**: Process in one batch of 7.
2. **Golden example**: Re-read `EXP-TRG-001.yaml`.
3. **Dual-source gate**: Must read BOTH audit AND book.
4. **PRD gate**: Must load `PRD_INDEX.md` and the family PRD set (PRD_04, PRD_05, PRD_06, PRD_07, PRD_08, PRD_09) before writing any primitive.
5. **Example standard**: Every primitive must produce exactly **5 examples** — 1 BOOK: prefix + 4 CCP: prefixed use cases naming actual CCP surfaces.
6. **Float consistency**: Progression primitives should have HIGH `user_state_effects.replay_desire` (0.7+) and HIGH `experience_stage_fit.retention` (0.8+).

## Completion Receipt

After finishing all 7 primitives, produce the receipt format specified in the SKILL.
