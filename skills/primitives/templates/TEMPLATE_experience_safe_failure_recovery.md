# Family Implementation Template: Safe Failure and Recovery
# Plane: EXPERIENCE
# Family Code: SAF

---

## ⚠️ ANTI-LAZINESS ENFORCEMENT — THIS TASK IS CONSIDERED FAILED IF:

1. **You did not read the book.** Failure and recovery theory (Jane McGonigal's "Resilience", Yu-kai Chou's "Loss & Avoidance", Wendel's "Obstacles") is psychological. If your `why_it_works` uses generic "it helps them try again" language without citing the specific mechanism (White Hat/Black Hat sequencing, Behavioral Forgiveness, Possible-Win Scarcity, Hypnosedation) — you have failed.
2. **You wrote generic examples.** Every `examples.context` must name a specific failure moment in CCP (e.g., "The moment a user receives a low speaking score after their third attempt and feels the urge to quit").
3. **You left any float at 0.5.** Every float must be a deliberate calibration decision.
4. **You confused recovery with encouragement.** SAF primitives govern the **structural handling of a lapse**, not just nice messages. If your primitive is about "telling them they did great anyway," it belongs in `feedback_scoring`.
5. **Your `implementation_targets` are vague.** Specify real comeback rules, streak-protection logic, or Mini App recovery states.
6. **You wrote `key_pages: "various"`.** Real chapter names required.

### BOOK VERIFICATION LOG (Complete Before Writing Any YAML)

For each book in this batch, confirm:
```
BOOK: [title]
├── Chapters confirmed read: [list at least 2 chapter titles]
├── One recovery mechanism found ONLY in the book (not the audit): [write it]
├── One "learned helplessness" or "death spiral" warning from the author: [write it]
└── STATUS: VERIFIED / BLOCKED (if blocked, stop and report)
```
**Books for this template:** Actionable Gamification (Yu-kai Chou), Reality Is Broken (McGonigal), Designing for Behavior Change (Wendel), Persuasive Technology (BJ Fogg), Beyond Belief (Nir Eyal)

- **SAF family float fingerprint**: `user_state_effects.safety` and `user_state_effects.confidence` should be high (0.7–0.9). `user_state_effects.replay_desire` should also be elevated (0.6–0.8).
- `experience_stage_fit.recovery` and `experience_stage_fit.retention` should be dominant.
- `experience_metrics.comeback_rate` and `experience_metrics.day7_retention` are the primary metrics.

### PRE-SAVE CHECKLIST (Check Every Primitive Before Saving)

```
[ ] Book Verification Log completed for this primitive's source book
[ ] PRD_INDEX.md and relevant modular PRDs loaded and referenced
[ ] summary ≠ restatement of core_move
[ ] why_it_works cites a specific recovery mechanism from the book
[ ] EXACTLY 5 examples: 1 BOOK: prefix + 4 CCP: prefixed use cases
[ ] All CCP examples name at least one CCP surface (CCF, CMF, CVE, CBCS, Conscious Reactions, V2WS, CPSC, Telegram, AFFiNE, church/community)
[ ] Zero examples use banned phrases:
    - "a user might use this when" / "in the app" / "in the platform"
[ ] At least 1 anti-example describing a recovery feature that feels patronizing or annoying
[ ] No float anywhere is exactly 0.5
[ ] user_state_effects.safety is 0.7 or higher
[ ] experience_stage_fit.recovery is 0.8 or higher
[ ] implementation_targets.backend_rules lists real logic (e.g., grace period rules)
[ ] synergizes_with IDs verified in experience catalog
[ ] book_reference.chapters contains real chapter names
[ ] File saved to: primitives/experience/safe_failure_recovery/[ID].yaml
```

---

## Before You Start
1. Load and read the SKILL file: `skills/primitives/SKILL_Primitive_YAML_Codification.md`
2. Load the golden example: `primitives/experience/_golden/EXP-TRG-001.yaml`
3. Load the experience registry spec: `lab/CCP APRIL Updates/05_Core_Experience/Experience_Primitive_Registry_Spec.md` — Section 4.7
4. Load the PRD router: `docs/prd/modules/PRD_INDEX.md`
5. Load the relevant modular PRDs for this family:
   - `docs/prd/modules/PRD_04_CVE_Experience_Design.md`
   - `docs/prd/modules/PRD_05_CBCS_Law28.md`
   - `docs/prd/modules/PRD_06_Conscious_Reactions.md`
   - `docs/prd/modules/PRD_07_V2WS_Webinar.md`
   - `docs/prd/modules/PRD_08_Conscious_Primitives.md`
   - `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`

## Your Task
Write one YAML file per primitive listed below. Save each to: `primitives/experience/safe_failure_recovery/[ID].yaml`

## Source Files You Must Load

#### Audit Files
| Audit File | Path | Primitives |
|---|---|---|
| Actionable Gamification | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Actionable_Gamification_Yu_kai_Chou.md` | SAF-001, SAF-002 |
| Reality Is Broken | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Reality_is_Broken_Jane_McGonigal.md` | SAF-002, SAF-003, SAF-004 |
| Designing for Behavior Change | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Designing_for_Behavior_Change_Stephen_Wendel.md` | SAF-005 |
| Persuasive Technology | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Persuasive_Technology_BJ_Fogg.md` | SAF-005 |
| Beyond Belief | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Beyond_Belief_Nir_Eyal.md` | SAF-006 |

#### Book Files (Experience Library)
| Book File | Path |
|---|---|
| Actionable Gamification | `lab/Public Speeaking Coaching/09_Experience_Engineering/Actionable Gamification - Yu-kai Chou.md` |
| Reality Is Broken | `lab/Public Speeaking Coaching/09_Experience_Engineering/Reality is Broken - Jane McGonigal.md` |
| Designing for Behavior Change | `lab/Public Speeaking Coaching/09_Experience_Engineering/Designing for Behavior Change - Stephen Wendel.md` |
| Persuasive Technology | `lab/Public Speeaking Coaching/09_Experience_Engineering/Persuasive Technology - BJ Fogg.md` |
| Beyond Belief | `lab/Public Speeaking Coaching/09_Experience_Engineering/Beyond Belief.md` |

---

## Primitive Manifest (5 primitives)

| ID | Canonical Name | Source Audit | MCDA | Core Move |
|---|---|---|---:|---|
| EXP-SAF-001 | White Hat -> Black Hat -> White Hat Emotional Sequencing | Actionable Gamification | 196 | Structure the failure experience to end with positive motivation (White Hat) after revealing a gap (Black Hat) |
| EXP-SAF-002 | Possible-Win Scarcity | Actionable Gamification / Reality is Broken | 186 | Make the next opportunity to succeed feel finite and valuable, rather than an infinite retry |
| EXP-SAF-003 | Hypnosedation Reframing | Reality Is Broken | 185 | Use a high-immersion state to distract from the sting of failure and focus on the mechanics of improvement |
| EXP-SAF-004 | Practical Play / Safe Failure | Reality Is Broken | 168 | Ensure that failing a task costs the user nothing in the real world and provides immediate learning for the next try |
| EXP-SAF-005 | Behavioral Forgiveness | Wendel / Fogg | 160 | Programmatically recognize when a user has lapsed and provide a "welcome back" path that ignores the missed days |
| EXP-SAF-006 | The Richter Rescue | Beyond Belief | 165 | Intervene immediately when a user is abandoning a task to prove their effort still matters, resetting their belief system. |

---

## Execution Rules

1. **Batch size**: Process in one batch of 6.
2. **Golden example**: Re-read `EXP-TRG-001.yaml`.
3. **Dual-source gate**: Must read BOTH audit AND book.
4. **PRD gate**: Must load `PRD_INDEX.md` and the family PRD set (PRD_04, PRD_05, PRD_06, PRD_07, PRD_08, PRD_09) before writing any primitive.
5. **Example standard**: Every primitive must produce exactly **5 examples** — 1 BOOK: prefix + 4 CCP: prefixed use cases naming actual CCP surfaces.
6. **Float consistency**: Recovery primitives should have HIGH `user_state_effects.safety` (0.7+) and HIGH `experience_stage_fit.recovery` (0.8+).

## Completion Receipt

After finishing all 6 primitives, produce the receipt format specified in the SKILL.
