# Family Implementation Template: Friction and Ability
# Plane: EXPERIENCE
# Family Code: FRC

---

## ⚠️ ANTI-LAZINESS ENFORCEMENT — THIS TASK IS CONSIDERED FAILED IF:

1. **You did not read the book.** Friction theory (BJ Fogg's Ability factors, Steve Krug's "Don't Make Me Think" laws) is precise. If your `why_it_works` uses generic "it makes it easier" language without citing the specific factor (Time, Money, Physical Effort, Brain Cycles, Social Deviance, Non-Routine) — you have failed.
2. **You wrote generic examples.** Every `examples.context` must name a specific Telegram or Mini App friction point (e.g., "The moment the user has to record their first reaction but hasn't allowed mic permissions yet").
3. **You left any float at 0.5.** Every float must be a deliberate calibration decision.
4. **You confused ability with motivation.** FRC primitives govern the **ease** of the action, not the desire to do it. If your primitive is about "making them want it," it belongs in `trigger_timing` or `progression_replay`.
5. **Your `implementation_targets` are vague.** Specify real UI components or backend rules.
6. **You wrote `key_pages: "various"`.** Real chapter names required.

### BOOK VERIFICATION LOG (Complete Before Writing Any YAML)

For each book in this batch, confirm:
```
BOOK: [title]
├── Chapters confirmed read: [list at least 2 chapter titles]
├── One friction mechanism found ONLY in the book (not the audit): [write it]
├── One usability warning from the author: [write it for anti_examples]
└── STATUS: VERIFIED / BLOCKED (if blocked, stop and report)
```
**Books for this template:** Persuasive Technology (BJ Fogg), Don't Make Me Think (Steve Krug), Actionable Gamification (Yu-kai Chou), Designing for Behavior Change (Stephen Wendel), Beyond Belief (Nir Eyal)

### ANTI-DRIFT RULES (6-Primitive Batch)

- Small batch — zero drift.
- **FRC family float fingerprint**: `user_state_effects.clarity` and `user_state_effects.safety` should be high (0.7–0.9). `user_state_effects.urgency` should be LOW (0.1–0.3) — friction reduction is about peace, not pressure.
- `experience_stage_fit.activation` and `experience_stage_fit.recording` should be dominant.
- `experience_metrics.react_rate` and `experience_metrics.completion_rate` should be the primary metrics influenced.

### PRE-SAVE CHECKLIST (Check Every Primitive Before Saving)

```
[ ] Book Verification Log completed for this primitive's source book
[ ] PRD_INDEX.md and relevant modular PRDs loaded and referenced
[ ] summary ≠ restatement of core_move
[ ] why_it_works cites a specific ability/friction factor from the book
[ ] EXACTLY 5 examples: 1 BOOK: prefix + 4 CCP: prefixed use cases
[ ] All CCP examples name at least one CCP surface (CCF, CMF, CVE, CBCS, Conscious Reactions, V2WS, CPSC, Telegram, AFFiNE, church/community)
[ ] Zero examples use banned phrases:
    - "a user might use this when" / "in the app" / "in the platform"
[ ] At least 1 anti-example with mechanism-grounded failure reason
[ ] No float anywhere is exactly 0.5
[ ] user_state_effects.clarity is 0.7 or higher
[ ] user_state_effects.urgency is 0.3 or lower
[ ] implementation_targets.frontend_components lists real UI elements
[ ] synergizes_with IDs verified in experience catalog
[ ] book_reference.chapters contains real chapter names
[ ] File saved to: primitives/experience/friction_ability/[ID].yaml
```

---

## Before You Start
1. Load and read the SKILL file: `skills/primitives/SKILL_Primitive_YAML_Codification.md`
2. Load the golden example: `primitives/experience/_golden/EXP-TRG-001.yaml`
3. Load the experience registry spec: `lab/CCP APRIL Updates/05_Core_Experience/Experience_Primitive_Registry_Spec.md` — Section 4.2
4. Load the PRD router: `docs/prd/modules/PRD_INDEX.md`
5. Load the relevant modular PRDs for this family:
   - `docs/prd/modules/PRD_04_CVE_Experience_Design.md`
   - `docs/prd/modules/PRD_05_CBCS_Law28.md`
   - `docs/prd/modules/PRD_06_Conscious_Reactions.md`
   - `docs/prd/modules/PRD_07_V2WS_Webinar.md`
   - `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`

## Your Task
Write one YAML file per primitive listed below. Save each to: `primitives/experience/friction_ability/[ID].yaml`

## Source Files You Must Load

#### Audit Files
| Audit File | Path | Primitives |
|---|---|---|
| Don't Make Me Think | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Dont_Make_Me_Think_Steve_Krug.md` | FRC-001, FRC-004 |
| Actionable Gamification | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Actionable_Gamification_Yu_kai_Chou.md` | FRC-001 |
| Designing for Behavior Change | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Designing_for_Behavior_Change_Stephen_Wendel.md` | FRC-002 |
| Persuasive Technology | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Persuasive_Technology_BJ_Fogg.md` | FRC-002, FRC-003, FRC-004 |
| Beyond Belief | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Beyond_Belief_Nir_Eyal.md` | FRC-005, FRC-006 |

#### Book Files (Experience Library)
| Book File | Path |
|---|---|
| Don't Make Me Think | `lab/Public Speeaking Coaching/09_Experience_Engineering/Don't Make Me Think - Steve Krug.md` |
| Actionable Gamification | `lab/Public Speeaking Coaching/09_Experience_Engineering/Actionable Gamification - Yu-kai Chou.md` |
| Designing for Behavior Change | `lab/Public Speeaking Coaching/09_Experience_Engineering/Designing for Behavior Change - Stephen Wendel.md` |
| Persuasive Technology | `lab/Public Speeaking Coaching/09_Experience_Engineering/Persuasive Technology - BJ Fogg.md` |
| Beyond Belief | `lab/Public Speeaking Coaching/09_Experience_Engineering/Beyond Belief.md` |

---

## Primitive Manifest (6 primitives)

| ID | Canonical Name | Source Audit | MCDA | Core Move |
|---|---|---|---:|---|
| EXP-FRC-001 | Evolved UI + Glowing Choice | Krug / Actionable Gamification | 191 | Eliminate visual noise and highlight the single most important next action |
| EXP-FRC-002 | System 1 to System 2 Escalation | Wendel / Fogg | 175 | Keep user in fast/intuitive mode for as long as possible before requiring deep thought |
| EXP-FRC-003 | The B=MAP Friction Audit | Fogg | 175 | Systematically identify and remove any factor that lowers Ability (Time, Effort, Cycles) |
| EXP-FRC-004 | Friction-Zero Ability | Fogg / Krug | 160 | Ensure the target behavior requires almost zero mental or physical start-up cost |
| EXP-FRC-005 | Ritualized Agency | Beyond Belief | 170 | Transform a mundane functional tap into a deliberate, physical "Commitment Swipe" that generates agency rather than passivity. |
| EXP-FRC-006 | Hypnosedation Reframing | Beyond Belief | 185 | Reframe a stressful constraint (like a 60-second timer) as a "flow state activator" to neutralize anxiety and bypass the inner critic. |

---

## Execution Rules

1. **Batch size**: Process in one batch of 6.
2. **Golden example**: Re-read `EXP-TRG-001.yaml`.
3. **Dual-source gate**: Must read BOTH audit AND book.
4. **PRD gate**: Must load `PRD_INDEX.md` and the family PRD set (PRD_04, PRD_05, PRD_06, PRD_07, PRD_09) before writing any primitive.
5. **Example standard**: Every primitive must produce exactly **5 examples** — 1 BOOK: prefix + 4 CCP: prefixed use cases naming actual CCP surfaces.
6. **Float consistency**: Friction primitives should have HIGH `user_state_effects.clarity` (0.7+) and LOW `user_state_effects.urgency` (0.3 or lower).

## Completion Receipt

After finishing all 6 primitives, produce the receipt format specified in the SKILL.
