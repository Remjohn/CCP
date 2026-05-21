# Family Implementation Template: Trigger and Timing
# Plane: EXPERIENCE
# Family Code: TRG

## Instructions

You are executing the **Primitive YAML Codification** skill.

### Before You Start
1. Load and read the SKILL file: `skills/primitives/SKILL_Primitive_YAML_Codification.md`
2. Load the golden example: `primitives/experience/_golden/EXP-TRG-001.yaml`
3. Load the experience registry spec: `lab/CCP APRIL Updates/05_Core_Experience/Experience_Primitive_Registry_Spec.md` — Section 4.1
4. Load the PRD router: `docs/prd/modules/PRD_INDEX.md`
5. Load the relevant modular PRDs for this family:
   - `docs/prd/modules/PRD_04_CVE_Experience_Design.md`
   - `docs/prd/modules/PRD_05_CBCS_Law28.md`
   - `docs/prd/modules/PRD_06_Conscious_Reactions.md`
   - `docs/prd/modules/PRD_07_V2WS_Webinar.md`
   - `docs/prd/modules/PRD_08_Conscious_Primitives.md`
   - `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`

---

## ⚠️ ANTI-LAZINESS ENFORCEMENT — THIS TASK IS CONSIDERED FAILED IF:

1. **You did not read the book.** Hogg's B=MAP model has precise mathematical logic. Eyal's Hook Model has a specific four-phase architecture. McGonigal's win-state theory has a distinct psychological rationale. If your `why_it_works` could be written from memory of what these books are "about" rather than from reading their chapters — you have failed.
2. **You wrote generic examples.** Every `examples.context` must name a specific Telegram moment, Mini App state, or CCP onboarding event. "A user might open the app when..." is not a valid example context.
3. **You left any float at 0.5.** 0.5 = no decision made. Every float requires deliberate calibration.
4. **You confused trigger timing with friction reduction.** Trigger primitives govern WHEN and WHY a user acts. They do not govern HOW EASY the action is (that is the `friction_ability` family). If your primitive is mostly about removing obstacles, it belongs in a different family.
5. **Your `implementation_targets` are vague.** Experience primitives must specify real frontend components, real telemetry event names, and real backend rules. "The app should notify the user" is not an implementation target.
6. **You invented synergy IDs.** Verify every `synergizes_with` ID in the experience catalog before listing.
7. **You wrote `key_pages: "various"`.** Open the book. Find the chapters on trigger theory. Name them.

### BOOK VERIFICATION LOG (Complete Before Writing Any YAML)

For each book in this batch, confirm:
```
BOOK: [title]
├── Chapters confirmed read: [list at least 2 chapter titles]
├── One behavioral mechanism found ONLY in the book (not the audit): [write it]
├── One failure mode or anti-pattern the author warns about: [write it for anti_examples]
└── STATUS: VERIFIED / BLOCKED (if blocked, stop and report)
```
**Books for this template:** Hooked (Eyal/Hoover), Persuasive Technology (BJ Fogg), Reality Is Broken (McGonigal), Gamify (Brian Burke)

### ANTI-DRIFT RULES (9-Primitive Batch)

- Small batch — every primitive must be crisply differentiated.
- **TRG family float fingerprint**: `user_state_effects.urgency` should be elevated (0.6–0.9) for most trigger primitives. `experience_stage_fit.entry` and `experience_stage_fit.retention` should both be present and non-trivial. `experience_stage_fit.scoring` should be LOW (0.1–0.2) — triggers precede scoring.
- `implementation_targets.telemetry_events` must contain real event names (e.g., `reaction_triggered`, `internal_trigger_activated`, `daily_prompt_delivered`). Never leave this as `["TBD"]`.
- EXP-TRG-001 (External to Internal Trigger) and EXP-TRG-003 (Kairos) are closely related but fundamentally different: TRG-001 is about the TRANSITION over time; TRG-003 is about the MOMENT of perfect timing. Make this distinction show in the floats and summary.

### PRE-SAVE CHECKLIST (Check Every Primitive Before Saving)

```
[ ] Book Verification Log completed for this primitive's source book
[ ] PRD_INDEX.md and relevant modular PRDs loaded and referenced
[ ] summary ≠ restatement of core_move
[ ] why_it_works cites specific behavioral mechanism from the book
[ ] EXACTLY 5 examples: 1 BOOK: prefix + 4 CCP: prefixed use cases
[ ] All CCP examples name at least one CCP surface (CCF, CMF, CVE, CBCS, Conscious Reactions, V2WS, CPSC, Telegram, AFFiNE, church/community)
[ ] Zero examples use banned phrases:
    - "a user might use this when" / "in the app" / "in the platform"
[ ] At least 1 anti-example (e.g., wrong timing destroying goodwill)
[ ] No float anywhere is exactly 0.5
[ ] experience_stage_fit.scoring is 0.2 or below for most TRG primitives
[ ] user_state_effects.urgency is 0.6 or higher
[ ] implementation_targets.telemetry_events has real event names (not TBD)
[ ] synergizes_with IDs verified in the experience primitive catalog
[ ] book_reference.chapters contains real chapter names
[ ] File saved to: primitives/experience/trigger_timing/[ID].yaml
```

---

### Your Task
Write one YAML file per primitive listed below. Save each to: `primitives/experience/trigger_timing/[ID].yaml`

### Source Files You Must Load

#### Audit Files
| Audit File | Path | Primitives |
|---|---|---|
| Hooked | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Hooked_Ryan_Hoover.md` | EXP-TRG-001, 002 |
| Persuasive Tech (Fogg) | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Persuasive_Technology_BJ_Fogg.md` | EXP-TRG-003, 004 |
| Reality Is Broken | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Reality_is_Broken_Jane_McGonigal.md` | EXP-TRG-005, 006, 007 |
| Gamify | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Gamify_How_Gamification_Motivates_People_Brian_Burke.md` | EXP-TRG-008, 009 |

#### Book Files
| Book File | Path |
|---|---|
| Hooked | `lab/Public Speeaking Coaching/09_Experience_Engineering/Hooked - Ryan Hoover.md` |
| Persuasive Technology | `lab/Public Speeaking Coaching/09_Experience_Engineering/Persuasive Technology - BJ Fogg.md` |
| Reality Is Broken | `lab/Public Speeaking Coaching/09_Experience_Engineering/Reality is Broken - Jane McGonigal.md` |
| Gamify | `lab/Public Speeaking Coaching/09_Experience_Engineering/Gamify - Brian Burke.md` |

---

## Primitive Manifest (9 primitives)

| ID | Canonical Name | Source Audit | MCDA | Core Move |
|---|---|---|---:|---|
| EXP-TRG-001 | External to Internal Trigger Mapping | Hooked | 175 | Transition from push notifications to emotional cues |
| EXP-TRG-002 | Hook Cycle Velocity | Hooked | 185 | Force rapid daily engagement to cement routine |
| EXP-TRG-003 | Kairos / Opportune Moment | Fogg | 175 | Deliver prompts exactly when receptivity and ability are high |
| EXP-TRG-004 | Tailoring & Suggestion | Fogg | 165 | Intervene with relevant info based on user state/telemetry |
| EXP-TRG-005 | First Major Win-State | Reality Is Broken | 197 | Trigger social expansion only after user feels success |
| EXP-TRG-006 | Context-Aware System Triggers | Reality Is Broken | 170 | Use environmental signals to prompt relevant action |
| EXP-TRG-007 | Contextual Timing Triggers | Reality Is Broken | 140 | Align prompts with the user's real-world time-pockets |
| EXP-TRG-008 | Digital Motivation Leverage | Gamify | 192 | Trigger digital systems not to replace human motivation, but to amplify and direct the existing desire to master a skill. |
| EXP-TRG-009 | Habit Path Architecture | Gamify | 188 | Sequence triggers carefully over time to move the user from conscious, effortful action into automatic, habitual loops. |

---

## Execution Rules

1. **Batch size**: Process in one batch of 9.
2. **Golden example**: Re-read `EXP-TRG-001.yaml` for calibration.
3. **Dual-source gate**: Must read BOTH audit AND book.
4. **PRD gate**: Must load `PRD_INDEX.md` and the family PRD set (PRD_04, PRD_05, PRD_06, PRD_07, PRD_08, PRD_09) before writing any primitive.
5. **Example standard**: Every primitive must produce exactly **5 examples** — 1 BOOK: prefix + 4 CCP: prefixed use cases naming actual CCP surfaces.
6. **Float consistency**: Trigger primitives should have HIGH `user_state_effects.urgency` (0.6+) and HIGH `experience_stage_fit.entry` (0.7+).

## Completion Receipt

After finishing all 9 primitives, produce the receipt format specified in the SKILL.
