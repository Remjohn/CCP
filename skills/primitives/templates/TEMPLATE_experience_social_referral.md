# Family Implementation Template: Social Referral and Status
# Plane: EXPERIENCE
# Family Code: SOC

---

## ⚠️ ANTI-LAZINESS ENFORCEMENT — THIS TASK IS CONSIDERED FAILED IF:

1. **You did not read the book.** Social theory (Yu-kai Chou's "Social Influence & Relatedness", Jane McGonigal's "Social Treasures", Nir Eyal's "Social Rewards") is nuanced. If your `why_it_works` uses generic "people like to share" language without citing the specific social driver (Social Pressure, Social Capital, Social Treasures, Group Quests, Status Signaling) — you have failed.
2. **You wrote generic examples.** Every `examples.context` must name a specific social moment in CCP (e.g., "The moment a coach receives a 'Top 1% Reactivator' badge and is prompted to share it to their channel").
3. **You left any float at 0.5.** Every float must be a deliberate calibration decision.
4. **You confused social spread with marketing.** SOC primitives govern the **peer-to-peer behavior**, not the brand ads. If your primitive is about "the company posting to Twitter," it belongs in `meaning/referral_trust_transfer`.
5. **Your `implementation_targets` are vague.** Specify real share-card components, Telegram invite rules, or group-chat integration logic.
6. **You wrote `key_pages: "various"`.** Real chapter names required.

### BOOK VERIFICATION LOG (Complete Before Writing Any YAML)

For each book in this batch, confirm:
```
BOOK: [title]
├── Chapters confirmed read: [list at least 2 chapter titles]
├── One social mechanism found ONLY in the book (not the audit): [write it]
├── One "social fatigue" or "invitation spam" warning from the author: [write it]
└── STATUS: VERIFIED / BLOCKED (if blocked, stop and report)
```
**Books for this template:** Reality Is Broken (McGonigal), Actionable Gamification (Yu-kai Chou), Hooked (Eyal), Gamify (Brian Burke)

### ANTI-DRIFT RULES (5-Primitive Batch)

- Small batch — zero drift.
- **SOC family float fingerprint**: `user_state_effects.status` and `user_state_effects.belonging` should be high (0.7–0.9). `user_state_effects.confidence` should also be elevated (0.5–0.7).
- `experience_stage_fit.social_spread` and `experience_stage_fit.retention` should be dominant.
- `experience_metrics.share_rate` and `experience_metrics.upgrade_signal` are the primary metrics.

### PRE-SAVE CHECKLIST (Check Every Primitive Before Saving)

```
[ ] Book Verification Log completed for this primitive's source book
[ ] PRD_INDEX.md and relevant modular PRDs loaded and referenced
[ ] summary ≠ restatement of core_move
[ ] why_it_works cites a specific social mechanism from the book
[ ] EXACTLY 5 examples: 1 BOOK: prefix + 4 CCP: prefixed use cases
[ ] All CCP examples name at least one CCP surface (CCF, CMF, CVE, CBCS, Conscious Reactions, V2WS, CPSC, Telegram, AFFiNE, church/community)
[ ] Zero examples use banned phrases:
    - "a user might use this when" / "in the app" / "in the platform"
[ ] At least 1 anti-example describing a social feature that feels forced or embarrassing
[ ] No float anywhere is exactly 0.5
[ ] user_state_effects.status is 0.7 or higher
[ ] experience_stage_fit.social_spread is 0.8 or higher
[ ] implementation_targets.telemetry_events lists real events (e.g., `referral_invite_sent`)
[ ] synergizes_with IDs verified in experience catalog
[ ] book_reference.chapters contains real chapter names
[ ] File saved to: primitives/experience/social_referral/[ID].yaml
```

---

## Before You Start
1. Load and read the SKILL file: `skills/primitives/SKILL_Primitive_YAML_Codification.md`
2. Load the golden example: `primitives/experience/_golden/EXP-TRG-001.yaml`
3. Load the experience registry spec: `lab/CCP APRIL Updates/05_Core_Experience/Experience_Primitive_Registry_Spec.md` — Section 4.6
4. Load the PRD router: `docs/prd/modules/PRD_INDEX.md`
5. Load the relevant modular PRDs for this family:
   - `docs/prd/modules/PRD_04_CVE_Experience_Design.md`
   - `docs/prd/modules/PRD_05_CBCS_Law28.md`
   - `docs/prd/modules/PRD_06_Conscious_Reactions.md`
   - `docs/prd/modules/PRD_08_Conscious_Primitives.md`
   - `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`

## Your Task
Write one YAML file per primitive listed below. Save each to: `primitives/experience/social_referral/[ID].yaml`

## Source Files You Must Load

#### Audit Files
| Audit File | Path | Primitives |
|---|---|---|
| Reality Is Broken | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Reality_is_Broken_Jane_McGonigal.md` | SOC-001, SOC-003 |
| Actionable Gamification | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Actionable_Gamification_Yu_kai_Chou.md` | SOC-002, SOC-004 |
| Hooked | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Hooked_Ryan_Hoover.md` | SOC-003 |
| Gamify | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Gamify_How_Gamification_Motivates_People_Brian_Burke.md` | SOC-002, SOC-005 |

#### Book Files (Experience Library)
| Book File | Path |
|---|---|
| Reality Is Broken | `lab/Public Speeaking Coaching/09_Experience_Engineering/Reality is Broken - Jane McGonigal.md` |
| Actionable Gamification | `lab/Public Speeaking Coaching/09_Experience_Engineering/Actionable Gamification - Yu-kai Chou.md` |
| Hooked | `lab/Public Speeaking Coaching/09_Experience_Engineering/Hooked - Ryan Hoover.md` |
| Gamify | `lab/Public Speeaking Coaching/09_Experience_Engineering/Gamify - Brian Burke.md` |

---

## Primitive Manifest (5 primitives)

| ID | Canonical Name | Source Audit | MCDA | Core Move |
|---|---|---|---:|---|
| EXP-SOC-001 | Social Treasures + Group Quests | Reality Is Broken | 194 | Create rewards that can only be earned or given by helping other users |
| EXP-SOC-002 | Social Capital and Self-Esteem Economy | Actionable Gamification / Gamify | 186 | Design sharing loops where the primary reward is an increase in perceived status or peer recognition |
| EXP-SOC-003 | Identity-Driven Social Proof | Hooked / Reality is Broken | 180 | Show the user examples of people "just like them" who are succeeding, rather than distant celebrities |
| EXP-SOC-004 | Balanced Social Status Architecture | Actionable Gamification | 176 | Ensure the status system has both upward mobility (for new users) and protected elite states (for masters) |
| EXP-SOC-005 | Collaborative Role Architecture | Gamify | 182 | Assign distinct, interdependent roles within a community so users must rely on each other to succeed. |

---

## Execution Rules

1. **Batch size**: Process in one batch of 5.
2. **Golden example**: Re-read `EXP-TRG-001.yaml`.
3. **Dual-source gate**: Must read BOTH audit AND book.
4. **PRD gate**: Must load `PRD_INDEX.md` and the family PRD set (PRD_04, PRD_05, PRD_06, PRD_08, PRD_09) before writing any primitive.
5. **Example standard**: Every primitive must produce exactly **5 examples** — 1 BOOK: prefix + 4 CCP: prefixed use cases naming actual CCP surfaces.
6. **Float consistency**: Social primitives should have HIGH `user_state_effects.status` (0.7+) and HIGH `experience_stage_fit.social_spread` (0.8+).

## Completion Receipt

After finishing all 5 primitives, produce the receipt format specified in the SKILL.
