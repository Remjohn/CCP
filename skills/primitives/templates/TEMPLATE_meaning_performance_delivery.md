# Family Implementation Template: Performance and Delivery
# Plane: MEANING
# Family Code: ACT

## Instructions

You are executing the **Primitive YAML Codification** skill.

### Before You Start
1. Load and read the SKILL file: `skills/primitives/SKILL_Primitive_YAML_Codification.md`
2. Load the golden example: `primitives/meaning/_golden/PRM-HUM-009.yaml`
3. Load the registry catalog: `lab/CCP APRIL Updates/05_Core_Experience/Primitive_Packets_and_Registry_Spec.md` — Section 6.5
4. Load the PRD router: `docs/prd/modules/PRD_INDEX.md`
5. Load the relevant modular PRDs for this family:
   - `docs/prd/modules/PRD_03_CMF_Media_Factory.md`
   - `docs/prd/modules/PRD_04_CVE_Experience_Design.md`
   - `docs/prd/modules/PRD_05_CBCS_Law28.md`
   - `docs/prd/modules/PRD_06_Conscious_Reactions.md`
   - `docs/prd/modules/PRD_07_V2WS_Webinar.md`
   - `docs/prd/modules/PRD_08_Conscious_Primitives.md`

---

## ⚠️ ANTI-LAZINESS ENFORCEMENT — THIS TASK IS CONSIDERED FAILED IF:

1. **You did not read the book.** Acting books use precise craft vocabulary (Meisner's "living truthfully under imaginary circumstances", Stanislavski's "given circumstances"). If your `why_it_works` does not contain specific craft terminology from the source book — you have not read it.
2. **You wrote generic examples.** Performance primitives activate at very specific moments: before recording starts, during a live Telegram reaction, in a CMF coaching session. Name the exact moment.
3. **You left any float at 0.5.** 0.5 = no calibration. Every float must reflect a real judgment.
4. **You conflated performance delivery with persuasion.** ACT primitives primarily govern how a coach FEELS and PERFORMS, not what they argue. `goal_bias.persuasion` should generally be LOW for this family. `goal_bias.connection` and `goal_bias.memorability` should dominate.
5. **You invented synergy IDs.** Verify every `synergizes_with` ID in the catalog before listing.
6. **You wrote `key_pages: "various"`.** Open the book. Find real chapters. Name them.

### BOOK VERIFICATION LOG (Complete Before Writing Any YAML)

For each book in this batch, confirm:
```
BOOK: [title]
├── Chapters confirmed read: [list at least 2 chapter titles]
├── One craft term or mechanism found ONLY in the book (not the audit): [write it]
├── One failure mode the author warns against: [write it for anti_examples]
└── STATUS: VERIFIED / BLOCKED (if blocked, stop and report)
```
**Books for this template:** Steal the Show (Port), Sanford Meisner on Acting, Acting for the Camera (Barr), The Photographer's Guide to Posing (Adler), The Dramatic Portrait (Knight), Picture Perfect Posing (Valenzuela)

### ANTI-DRIFT RULES (10-Primitive Batch)

- Small batch — no drift is acceptable. Each primitive must be sharply differentiated from the others.
- **ACT family float fingerprint**: `goal_bias.connection` should be the dominant dimension (0.7–0.9). `goal_bias.clarity` should be LOW (0.1–0.3) — performance is felt, not explained. `phase_fit.delivery` should be the dominant phase fit (0.8–0.9) for most ACT primitives.
- `surface_fit.voice` should be HIGH (0.7+) for Meisner/Port primitives. `surface_fit.visual` should be HIGH (0.7+) for Posing/Portrait primitives. These distinctions must be reflected.
- No two primitives in this batch may share the same `implementation_role`.

### PRE-SAVE CHECKLIST (Check Every Primitive Before Saving)

```
[ ] Book Verification Log completed for this primitive's source book
[ ] PRD_INDEX.md and relevant modular PRDs loaded and referenced
[ ] summary ≠ restatement of core_move
[ ] why_it_works cites specific craft vocabulary from the book
[ ] EXACTLY 5 examples: 1 BOOK: prefix + 4 CCP: prefixed use cases
[ ] All CCP examples name at least one CCP surface (CCF, CMF, CVE, CBCS, Conscious Reactions, V2WS, CPSC, Telegram, AFFiNE, church/community)
[ ] Zero examples use banned phrases:
    - "a coach could use this" / "in content creation" / "in the app" / "in the platform"
[ ] At least 1 anti-example with mechanism-grounded failure reason
[ ] No float anywhere is exactly 0.5
[ ] At least 2 floats are below 0.3 across phase_fit + surface_fit combined
[ ] phase_fit.delivery is 0.7 or higher for delivery-phase primitives
[ ] goal_bias.connection is the highest or co-highest value
[ ] synergizes_with IDs verified in catalog
[ ] book_reference.chapters contains real chapter names
[ ] File saved to: primitives/meaning/performance_delivery/[ID].yaml
```

---

### Your Task
Write one YAML file per primitive listed below. Save each to: `primitives/meaning/performance_delivery/[ID].yaml`

### Source Files You Must Load

#### Audit Files
| Audit File | Path | Primitives |
|---|---|---|
| Steal the Show | `lab/CCP APRIL Updates/Public_Speaking_Audits/02_Acting_and_Performance/AUDIT_Steal_the_Show_Michael_Port.md` | PRM-ACT-001, 004, 005, 007 |
| Meisner on Acting | `lab/CCP APRIL Updates/Public_Speaking_Audits/02_Acting_and_Performance/AUDIT_Sanford_Meisner_on_Acting.md` | PRM-ACT-002, 003, 006, 009 |
| Acting for Camera | `lab/CCP APRIL Updates/Public_Speaking_Audits/02_Acting_and_Performance/AUDIT_Acting_for_the_Camera_Barr.md` | PRM-ACT-008 |
| Posing Portrait | `lab/CCP APRIL Updates/Public_Speaking_Audits/07_Photography_and_Composition/AUDIT Posing Portrait Adler Knight Valenzuela.md` | PRM-ACT-010 |

#### Book Files
| Book File | Path |
|---|---|
| Steal the Show | `lab/Public Speeaking Coaching/02_Acting_and_Performance/Steal_the_Show_-_Michael_Port.md` |
| Meisner on Acting | `lab/Public Speeaking Coaching/02_Acting_and_Performance/Sanford_Meisner_on_Acting_-_Sanford_Meisner.md` |
| Acting for Camera | `lab/Public Speeaking Coaching/02_Acting_and_Performance/Acting_for_the_Camera_-_Barr_Tony.md` |
| Photographer's Guide to Posing | `lab/Public Speeaking Coaching/07_Photography_and_Composition/The photographers guide to posing - Lindsay Adler.md` |
| The Dramatic Portrait | `lab/Public Speeaking Coaching/07_Photography_and_Composition/The Dramatic Portrait - Chris Knight.md` |
| Picture Perfect Posing | `lab/Public Speeaking Coaching/07_Photography_and_Composition/Picture Perfect Posing Practicing the Art - Roberto Valenzuela.md` |

---

## Primitive Manifest (10 primitives)

| ID | Canonical Name | Source Audit | MCDA | Core Move |
|---|---|---|---:|---|
| PRM-ACT-001 | Superobjective | Steal the Show | 194 | Define the singular overarching desire driving performance |
| PRM-ACT-002 | Magic As If / Particularisation | Meisner | 192 | Substitute personal emotional trigger for authentic reaction |
| PRM-ACT-003 | Pinch and Ouch | Meisner | 190 | Let real stimulus justify real response for caused delivery |
| PRM-ACT-010 | Body Language Calibration | Posing Portrait | 190 | Align micro-expressions and posture with narrative intent |
| PRM-ACT-004 | Three-Act Contrast Architecture | Steal the Show | 189 | Organize performance around a meaningful contrastive movement |
| PRM-ACT-005 | Backstory Architecture | Steal the Show | 189 | Anchor authority in a coherent owned personal history |
| PRM-ACT-006 | Preparation | Meisner | 184 | Enter right emotional pre-state before first word |
| PRM-ACT-007 | Yes, And Generative Engine | Steal the Show | 184 | Expand live thought by accepting and building on offered reality |
| PRM-ACT-008 | The Bottom Line | Acting for Camera | 180 | Assign one driving force to the moment for a clear center |
| PRM-ACT-009 | Repetition Game | Meisner | 176 | Break overthinking by forcing contact with live stimulus |

---

## Execution Rules

1. **Batch size**: Process in one batch of 10.
2. **Golden example**: Re-read `PRM-HUM-009.yaml`.
3. **Dual-source gate**: Must read BOTH audit AND book.
4. **PRD gate**: Must load `PRD_INDEX.md` and the family PRD set (PRD_03, PRD_04, PRD_05, PRD_06, PRD_07, PRD_08) before writing any primitive.
5. **Example standard**: Every primitive must produce exactly **5 examples** — 1 BOOK: prefix + 4 CCP: prefixed use cases naming actual CCP surfaces.
6. **Float consistency**: Performance primitives should have HIGH `goal_bias.connection` (0.7+) and HIGH `goal_bias.memorability` (0.6+).

## Completion Receipt

After finishing all 10 primitives, produce the receipt format specified in the SKILL.
