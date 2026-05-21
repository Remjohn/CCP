# Family Implementation Template: Personalization and Identity
# Plane: EXPERIENCE
# Family Code: PER

---

## ⚠️ ANTI-LAZINESS ENFORCEMENT — THIS TASK IS CONSIDERED FAILED IF:

1. **You did not read the book.** Identity theory (Jane McGonigal's "Secret Identities", Nir Eyal's "Cumulative Investment", BJ Fogg's "Tailoring") is precise. If your `why_it_works` uses generic "it makes it feel personal" language without citing the specific mechanism (Self-Signaling, Investment Loop, Alter-Ego, Role-Based Tailoring) — you have failed.
2. **You wrote generic examples.** Every `examples.context` must name a specific identity moment in CCP (e.g., "The moment the user is asked to choose their 'Expert Persona' before starting their first Conscious Reaction").
3. **You left any float at 0.5.** Every float must be a deliberate calibration decision.
4. **You confused personalization with data entry.** PER primitives govern the **user's self-perception and investment**, not just their profile settings. If your primitive is about "entering your name," it belongs in `trust_branding` (onboarding).
5. **Your `implementation_targets` are vague.** Specify real identity components, Telegram user-state rules, or backend personalization logic.
6. **You wrote `key_pages: "various"`.** Real chapter names required.

### BOOK VERIFICATION LOG (Complete Before Writing Any YAML)

For each book in this batch, confirm:
```
BOOK: [title]
├── Chapters confirmed read: [list at least 2 chapter titles]
├── One identity mechanism found ONLY in the book (not the audit): [write it]
├── One "identity lock-in" or "investment loss" warning from the author: [write it]
└── STATUS: VERIFIED / BLOCKED (if blocked, stop and report)
```
**Books for this template:** Reality Is Broken (McGonigal), SuperBetter (McGonigal), Actionable Gamification (Yu-kai Chou), Hooked (Eyal), Persuasive Technology (BJ Fogg), Beyond Belief (Nir Eyal), Gamify (Brian Burke)

### ANTI-DRIFT RULES (6-Primitive Batch)

- Small batch — zero drift.
- **PER family float fingerprint**: `user_state_effects.status` and `user_state_effects.belonging` should be high (0.7–0.9). `user_state_effects.confidence` should also be elevated (0.6–0.8).
- `experience_stage_fit.activation` and `experience_stage_fit.retention` should be dominant.
- `experience_metrics.comeback_rate` and `experience_metrics.upgrade_signal` are the primary metrics.

### PRE-SAVE CHECKLIST (Check Every Primitive Before Saving)

```
[ ] Book Verification Log completed for this primitive's source book
[ ] PRD_INDEX.md and relevant modular PRDs loaded and referenced
[ ] summary ≠ restatement of core_move
[ ] why_it_works cites a specific identity mechanism from the book
[ ] EXACTLY 5 examples: 1 BOOK: prefix + 4 CCP: prefixed use cases
[ ] All CCP examples name at least one CCP surface (CCF, CMF, CVE, CBCS, Conscious Reactions, V2WS, CPSC, Telegram, AFFiNE, church/community)
[ ] Zero examples use banned phrases:
    - "a user might use this when" / "in the app" / "in the platform"
[ ] At least 1 anti-example describing a personalization feature that feels invasive or shallow
[ ] No float anywhere is exactly 0.5
[ ] user_state_effects.status is 0.7 or higher
[ ] experience_stage_fit.retention is 0.8 or higher
[ ] implementation_targets.telemetry_events lists real events (e.g., `persona_chosen`)
[ ] synergizes_with IDs verified in experience catalog
[ ] book_reference.chapters contains real chapter names
[ ] File saved to: primitives/experience/personalization_identity/[ID].yaml
```

---

## Before You Start
1. Load and read the SKILL file: `skills/primitives/SKILL_Primitive_YAML_Codification.md`
2. Load the golden example: `primitives/experience/_golden/EXP-TRG-001.yaml`
3. Load the experience registry spec: `lab/CCP APRIL Updates/05_Core_Experience/Experience_Primitive_Registry_Spec.md` — Section 4.8
4. Load the PRD router: `docs/prd/modules/PRD_INDEX.md`
5. Load the relevant modular PRDs for this family:
   - `docs/prd/modules/PRD_04_CVE_Experience_Design.md`
   - `docs/prd/modules/PRD_05_CBCS_Law28.md`
   - `docs/prd/modules/PRD_06_Conscious_Reactions.md`
   - `docs/prd/modules/PRD_07_V2WS_Webinar.md`
   - `docs/prd/modules/PRD_08_Conscious_Primitives.md`
   - `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`

## Your Task
Write one YAML file per primitive listed below. Save each to: `primitives/experience/personalization_identity/[ID].yaml`

## Source Files You Must Load

#### Audit Files
| Audit File | Path | Primitives |
|---|---|---|
| Reality Is Broken | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Reality_is_Broken_Jane_McGonigal.md` | PER-001, PER-002 |
| SuperBetter | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_SuperBetter_Jane_McGonigal.md` | PER-002 |
| Actionable Gamification | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Actionable_Gamification_Yu_kai_Chou.md` | PER-001 |
| Hooked | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Hooked_Ryan_Hoover.md` | PER-003 |
| Persuasive Technology | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Persuasive_Technology_BJ_Fogg.md` | PER-004 |
| Beyond Belief | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Beyond_Belief_Nir_Eyal.md` | PER-005 |
| Gamify | `lab/CCP APRIL Updates/Public_Speaking_Audits/09_Experience_Engineering/AUDIT_Gamify_How_Gamification_Motivates_People_Brian_Burke.md` | PER-006 |

#### Book Files (Experience Library)
| Book File | Path |
|---|---|
| Reality Is Broken | `lab/Public Speeaking Coaching/09_Experience_Engineering/Reality is Broken - Jane McGonigal.md` |
| SuperBetter | `lab/Public Speeaking Coaching/09_Experience_Engineering/SuperBetter - Jane McGonigal.md` |
| Actionable Gamification | `lab/Public Speeaking Coaching/09_Experience_Engineering/Actionable Gamification - Yu-kai Chou.md` |
| Hooked | `lab/Public Speeaking Coaching/09_Experience_Engineering/Hooked - Ryan Hoover.md` |
| Persuasive Technology | `lab/Public Speeaking Coaching/09_Experience_Engineering/Persuasive Technology - BJ Fogg.md` |
| Beyond Belief | `lab/Public Speeaking Coaching/09_Experience_Engineering/Beyond Belief.md` |
| Gamify | `lab/Public Speeaking Coaching/09_Experience_Engineering/Gamify - Brian Burke.md` |

---

## Primitive Manifest (6 primitives)

| ID | Canonical Name | Source Audit | MCDA | Core Move |
|---|---|---|---:|---|
| EXP-PER-001 | Monitor Attachment + Alfred Personalization | Reality Is Broken / Actionable Gamification | 193 | Use an agent persona (like Alfred) that mirrors the user's intent and protects their status |
| EXP-PER-002 | Adopt a Secret Identity | SuperBetter / Reality is Broken | 175 | Let users choose a heroic or expert persona to bypass their real-world communication fears |
| EXP-PER-003 | Cumulative Investment | Hooked | 165 | Increase the cost of leaving by asking the user to load their own voice, data, and history into the system |
| EXP-PER-004 | Tailoring & Suggestion | Fogg | 165 | Use telemetry to suggest the single most relevant persona or topic brief for the user's current state |
| EXP-PER-005 | Identity De-Labeling | Beyond Belief | 170 | Use dynamic, growth-oriented statuses (e.g., "Building Jury Influence") instead of static negative labels to prevent limiting beliefs from calcifying. |
| EXP-PER-006 | Shared-Goal Player-Centric Design | Gamify | 196 | Align the business goal (retention) with the player's personal goal (mastery) so gamification feels empowering, not manipulative. |

---

## Execution Rules

1. **Batch size**: Process in one batch of 6.
2. **Golden example**: Re-read `EXP-TRG-001.yaml`.
3. **Dual-source gate**: Must read BOTH audit AND book.
4. **PRD gate**: Must load `PRD_INDEX.md` and the family PRD set (PRD_04, PRD_05, PRD_06, PRD_07, PRD_08, PRD_09) before writing any primitive.
5. **Example standard**: Every primitive must produce exactly **5 examples** — 1 BOOK: prefix + 4 CCP: prefixed use cases naming actual CCP surfaces.
6. **Float consistency**: Personalization primitives should have HIGH `user_state_effects.status` (0.7+) and HIGH `experience_stage_fit.retention` (0.8+).

## Completion Receipt

After finishing all 6 primitives, produce the receipt format specified in the SKILL.
