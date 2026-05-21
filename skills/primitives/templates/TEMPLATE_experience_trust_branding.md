# Family Implementation Template: Trust and Premium Branding
# Plane: EXPERIENCE
# Family Code: TRS

---

## ⚠️ ANTI-LAZINESS ENFORCEMENT — THIS TASK IS CONSIDERED FAILED IF:

1. **You did not read the book.** Trust and design books (Lupton, Norman, Chou) contain specific visual and psychological cues for "visceral" and "reflective" trust that are not in the audit. If your `why_it_works` does not cite specific design or behavioral terminology from the source book — you have failed.
2. **You wrote generic examples.** Every `examples.context` must name a specific premium CCP touchpoint (onboarding welcome, score-reveal card, payment wall, expert-pairing screen).
3. **You left any float at 0.5.** Every float must be a deliberate calibration decision.
4. **You confused branding with marketing.** TRS primitives govern the **felt authority and safety** of the product experience, not the slogans. If your primitive is about "selling the benefit," it belongs in `persuasion`.
5. **Your `implementation_targets` are vague.** Specify real CSS tokens, UI components, or UX flow rules.
6. **You wrote `key_pages: "various"`.** Real chapter names required.

### BOOK VERIFICATION LOG (Complete Before Writing Any YAML)

For each book in this batch, confirm:
```
BOOK: [title]
├── Chapters confirmed read: [list at least 2 chapter titles]
├── One trust/design mechanism found ONLY in the book (not the audit): [write it]
├── One "uncanny valley" or trust-breaking warning from the author: [write it]
└── STATUS: VERIFIED / BLOCKED (if blocked, stop and report)
```
**Books for this template:** Design Is Storytelling (Lupton), Actionable Gamification (Yu-kai Chou), Emotional Design (Norman), Hooked (Eyal), Reality Is Broken (McGonigal)

### ANTI-DRIFT RULES (5-Primitive Batch)

- Small batch — zero drift.
- **TRS family float fingerprint**: `user_state_effects.safety` and `user_state_effects.status` should be high (0.7–0.9). `user_state_effects.clarity` should also be elevated (0.6–0.8).
- `experience_stage_fit.entry` and `experience_stage_fit.retention` should be dominant.
- `experience_metrics.upgrade_signal` and `experience_metrics.comeback_rate` are the primary metrics.

### PRE-SAVE CHECKLIST (Check Every Primitive Before Saving)

```
[ ] Book Verification Log completed for this primitive's source book
[ ] PRD_INDEX.md and relevant modular PRDs loaded and referenced
[ ] summary ≠ restatement of core_move
[ ] why_it_works cites a specific design or trust mechanism from the book
[ ] EXACTLY 5 examples: 1 BOOK: prefix + 4 CCP: prefixed use cases
[ ] All CCP examples name at least one CCP surface (CCF, CMF, CVE, CBCS, Conscious Reactions, V2WS, CPSC, Telegram, AFFiNE, church/community)
[ ] Zero examples use banned phrases:
    - "a user might use this when" / "in the app" / "in the platform"
[ ] At least 1 anti-example describing a trust-breaking implementation
[ ] No float anywhere is exactly 0.5
[ ] user_state_effects.safety is 0.7 or higher
[ ] user_state_effects.status is 0.7 or higher
[ ] implementation_targets.frontend_components lists real UI elements
[ ] synergizes_with IDs verified in experience catalog
[ ] book_reference.chapters contains real chapter names
[ ] File saved to: primitives/experience/trust_branding/[ID].yaml
```

---

## Before You Start
1. Load and read the SKILL file: `skills/primitives/SKILL_Primitive_YAML_Codification.md`
2. Load the golden example: `primitives/experience/_golden/EXP-TRG-001.yaml`
3. Load the experience registry spec: `lab/CCP APRIL Updates/05_Core_Experience/Experience_Primitive_Registry_Spec.md` — Section 4.3
4. Load the PRD router: `docs/prd/modules/PRD_INDEX.md`
5. Load the relevant modular PRDs for this family:
   - `docs/prd/modules/PRD_03_CMF_Media_Factory.md`
   - `docs/prd/modules/PRD_04_CVE_Experience_Design.md`
   - `docs/prd/modules/PRD_06_Conscious_Reactions.md`
   - `docs/prd/modules/PRD_07_V2WS_Webinar.md`
   - `docs/prd/modules/PRD_08_Conscious_Primitives.md`
   - `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`

## Your Task
Write one YAML file per primitive listed below. Save each to: `primitives/experience/trust_branding/[ID].yaml`

## Source Files You Must Load

#### Audit Files
| Audit File | Path | Primitives |
|---|---|---|
| Design Is Storytelling | `lab/CCP APRIL Updates/Public_Speaking_Audits/06_Design_and_Business/AUDIT_Design_is_Storytelling_Ellen_Lupton.md` | TRS-001, TRS-002 |
| Actionable Gamification | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Actionable_Gamification_Yu_kai_Chou.md` | TRS-005 |
| Reality Is Broken | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Reality_is_Broken_Jane_McGonigal.md` | TRS-003 |
| Hooked | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Hooked_Ryan_Hoover.md` | TRS-003, TRS-004 |
| Emotional Design | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Emotional_design_why_we_love_or_hate_everyday_things_Donald_A_Norman.md` | TRS-004 |

#### Book Files (Experience Library)
| Book File | Path |
|---|---|
| Design Is Storytelling | `lab/Public Speeaking Coaching/06_Design_and_Business/Design is Storytelling - Ellen Lupton.md` |
| Actionable Gamification | `lab/Public Speeaking Coaching/09_Experience_Engineering/Actionable Gamification - Yu-kai Chou.md` |
| Reality Is Broken | `lab/Public Speeaking Coaching/09_Experience_Engineering/Reality is Broken - Jane McGonigal.md` |
| Hooked | `lab/Public Speeaking Coaching/09_Experience_Engineering/Hooked - Ryan Hoover.md` |
| Emotional Design | `lab/Public Speeaking Coaching/09_Experience_Engineering/Emotional design - Donald A Norman.md` |

---

## Primitive Manifest (5 primitives)

| ID | Canonical Name | Source Audit | MCDA | Core Move |
|---|---|---|---:|---|
| EXP-TRS-001 | Perception and Behavioral Guidance as a Unified Stack | Lupton | 199 | Ensure every visual choice actively steers the user toward the intended behavior |
| EXP-TRS-002 | Design for Lived Use, Not Abstract Intent | Lupton | 194 | Optimize the UI for how people actually move their thumbs and eyes under stress |
| EXP-TRS-003 | Placebo Onboarding | McGonigal / Hooked | 180 | Give the user small, early "fake" responsibilities that build real psychological ownership |
| EXP-TRS-004 | Visceral Hooking | Hooked / Norman | 175 | Use first-impression aesthetics (color, motion, sound) to trigger immediate biological trust |
| EXP-TRS-005 | The Trust Architecture | Actionable Gamification | 170 | Build long-term authority by being transparent about system logic and data security |

---

## Execution Rules

1. **Batch size**: Process in one batch of 5.
2. **Golden example**: Re-read `EXP-TRG-001.yaml`.
3. **Dual-source gate**: Must read BOTH audit AND book.
4. **PRD gate**: Must load `PRD_INDEX.md` and the family PRD set (PRD_03, PRD_04, PRD_06, PRD_07, PRD_08, PRD_09) before writing any primitive.
5. **Example standard**: Every primitive must produce exactly **5 examples** — 1 BOOK: prefix + 4 CCP: prefixed use cases naming actual CCP surfaces.
6. **Float consistency**: Trust primitives should have HIGH `user_state_effects.safety` (0.7+) and HIGH `user_state_effects.status` (0.7+).

## Completion Receipt

After finishing all 5 primitives, produce the receipt format specified in the SKILL.
