# Family Implementation Template: Visual and Sonic Guidance
# Plane: MEANING
# Family Code: VSG

## Instructions

You are executing the **Primitive YAML Codification** skill.

### Before You Start
1. Load and read the SKILL file: `skills/primitives/SKILL_Primitive_YAML_Codification.md`
2. Load the golden example: `primitives/meaning/_golden/PRM-HUM-009.yaml`
3. Load the registry catalog: `lab/CCP APRIL Updates/05_Core_Experience/Primitive_Packets_and_Registry_Spec.md` — Section 6.7
4. Load the PRD router: `docs/prd/modules/PRD_INDEX.md`
5. Load the relevant modular PRDs for this family:
   - `docs/prd/modules/PRD_02_CCF_Content_Factory.md`
   - `docs/prd/modules/PRD_03_CMF_Media_Factory.md`
   - `docs/prd/modules/PRD_04_CVE_Experience_Design.md`
   - `docs/prd/modules/PRD_06_Conscious_Reactions.md`
   - `docs/prd/modules/PRD_07_V2WS_Webinar.md`
   - `docs/prd/modules/PRD_08_Conscious_Primitives.md`

---

## ⚠️ ANTI-LAZINESS ENFORCEMENT — THIS TASK IS CONSIDERED FAILED IF:

1. **You did not read the book.** Photography composition theory (Freeman's zone system, Mercado's framing vocabulary) and sound design theory (Murch's layering philosophy, Beck/Kalinak's diegetic/non-diegetic distinction) are not in the audit. If your `why_it_works` does not contain vocabulary specific to these disciplines — you have not read the source.
2. **You wrote generic examples.** VSG primitives govern very specific CCP artifacts: CMF thumbnails, Telegram topic-brief visuals, score-card layouts, voice-note sonic texture, reaction-mode B-roll. Name the exact artifact.
3. **You left any float at 0.5.** Every float requires a deliberate calibration decision.
4. **You conflated visual and sonic primitives.** Photography primitives should have HIGH `surface_fit.visual` and LOW `surface_fit.sonic`. Sound design primitives should have HIGH `surface_fit.sonic` and HIGH `surface_fit.voice`. Never flip these.
5. **You invented synergy IDs.** Verify every `synergizes_with` ID in the catalog before listing.
6. **You wrote `key_pages: "various"`.** Open the book. Find the specific chapters on composition, framing, or layering. Name them.

### BOOK VERIFICATION LOG (Complete Before Writing Any YAML)

For each book in this batch, confirm:
```
BOOK: [title]
├── Chapters confirmed read: [list at least 2 chapter titles]
├── One technical vocabulary term or concept from the book (not the audit): [write it]
├── One compositional or sonic failure the author warns against: [write it for anti_examples]
└── STATUS: VERIFIED / BLOCKED (if blocked, stop and report)
```
**Books for this template:** The Photographer's Eye (Freeman), Designing Sound (Beck), Sound / Film Music (Kalinak), The Radio Drama Handbook, Photographer's Guide to Posing (Adler), The Dramatic Portrait (Knight), Picture Perfect Posing (Valenzuela)

### ANTI-DRIFT RULES (12-Primitive Batch)

- Small batch — every primitive must be crisply differentiated from the others.
- **VSG family float fingerprint**: `goal_bias.clarity` should dominate (0.7–0.9) — these primitives exist to remove perceptual ambiguity. `goal_bias.memorability` should be elevated (0.6+). `goal_bias.surprise` should be LOW (0.1–0.2) for photography primitives and MODERATE (0.4–0.6) for sound design primitives (sonic texture can produce pleasant surprise).
- `surface_fit.visual` vs `surface_fit.sonic` must cleanly separate photography from sound design primitives. They cannot both be 0.7+ unless the primitive is explicitly multimodal.
- `phase_fit.revision` and `phase_fit.delivery` should dominate for VSG — these are polish and delivery primitives, not research or discovery tools.

### PRE-SAVE CHECKLIST (Check Every Primitive Before Saving)

```
[ ] Book Verification Log completed for this primitive's source book
[ ] PRD_INDEX.md and relevant modular PRDs loaded and referenced
[ ] summary ≠ restatement of core_move
[ ] why_it_works cites specific technical vocabulary from the discipline (photography or sound)
[ ] EXACTLY 5 examples: 1 BOOK: prefix + 4 CCP: prefixed use cases
[ ] All CCP examples name at least one CCP surface (CCF, CMF, CVE, CBCS, Conscious Reactions, V2WS, CPSC, Telegram, AFFiNE, church/community)
[ ] Zero examples use banned phrases:
    - "a coach could use this" / "in content creation" / "in the app" / "in the platform"
[ ] At least 1 anti-example with mechanism-grounded failure reason
[ ] No float anywhere is exactly 0.5
[ ] surface_fit.visual and surface_fit.sonic are NOT both above 0.7 (unless explicitly multimodal)
[ ] At least 2 floats are below 0.3 across phase_fit + surface_fit combined
[ ] synergizes_with IDs verified in catalog
[ ] book_reference.chapters contains real chapter names
[ ] File saved to: primitives/meaning/visual_sonic_guidance/[ID].yaml
```

---

### Your Task
Write one YAML file per primitive listed below. Save each to: `primitives/meaning/visual_sonic_guidance/[ID].yaml`

### Source Files You Must Load

#### Audit Files
| Audit File | Path | Primitives |
|---|---|---|
| The Photographers Eye | `lab/CCP APRIL Updates/Public_Speaking_Audits/07_Photography_and_Composition/AUDIT The Photographers Eye Michael Freeman.md` | PRM-VSG-001, 003, 007, 009, 012 |
| Designing Sound | `lab/CCP APRIL Updates/Public_Speaking_Audits/08_Sound_Design/AUDIT Designing Sound Beck Kalinak.md` | PRM-VSG-002, 006, 011 |
| Sound Design Short Radio | `lab/CCP APRIL Updates/Public_Speaking_Audits/08_Sound_Design/AUDIT Sound Design for Short Radio Broadcasting.md` | PRM-VSG-004, 010 |
| Posing Portrait | `lab/CCP APRIL Updates/Public_Speaking_Audits/07_Photography_and_Composition/AUDIT Posing Portrait Adler Knight Valenzuela.md` | PRM-VSG-005, 008 |

#### Book Files
| Book File | Path |
|---|---|
| The Photographers Eye | `lab/Public Speeaking Coaching/07_Photography_and_Composition/The photographers Eye - Michael Freeman.md` |
| Designing Sound | `lab/Public Speeaking Coaching/08_Sound_Design/Designing Sound - Jay Beck.md` |
| Sound | `lab/Public Speeaking Coaching/08_Sound_Design/Sound - Kathryn Kalinak.md` |
| The Radio Drama Handbook | `lab/Public Speeaking Coaching/08_Sound_Design/The Radio Drama Handbook - Audio Drama in Context and Practice.md` |
| Photographer's Guide to Posing | `lab/Public Speeaking Coaching/07_Photography_and_Composition/The photographers guide to posing - Lindsay Adler.md` |
| The Dramatic Portrait | `lab/Public Speeaking Coaching/07_Photography_and_Composition/The Dramatic Portrait - Chris Knight.md` |
| Picture Perfect Posing | `lab/Public Speeaking Coaching/07_Photography_and_Composition/Picture Perfect Posing Practicing the Art - Roberto Valenzuela.md` |

---

## Primitive Manifest (12 primitives)

| ID | Canonical Name | Source Audit | MCDA | Core Move |
|---|---|---|---:|---|
| PRM-VSG-001 | Composition as Eye-Path Engineering | The Photographers Eye | 198 | Control viewer's scan path through deliberate sequence |
| PRM-VSG-002 | Workflow Creates Aesthetics | Designing Sound | 198 | Treat process design as source of aesthetic quality |
| PRM-VSG-003 | Intent Governs Style | The Photographers Eye | 196 | Let communication goal decide treatment, not fashion |
| PRM-VSG-004 | Silence as Narrative Device | Sound Design Short Radio | 196 | Use silence as active meaning and pressure |
| PRM-VSG-005 | Visual Emphasis Must Be Intentional | Posing Portrait | 196 | Force a dominant target so viewer knows what to notice |
| PRM-VSG-006 | Polyphony and Controlled Density | Designing Sound | 195 | Allow layered richness without sacrificing clarity |
| PRM-VSG-007 | Order Imposed on Chaos | The Photographers Eye | 194 | Reduce clutter by selecting and structuring perception |
| PRM-VSG-008 | Character Coherence Beats Beauty | Posing Portrait | 194 | Make every visual cue agree on a narrative thesis |
| PRM-VSG-009 | Process Systematization | The Photographers Eye | 193 | Convert judgment into repeatable composition workflow |
| PRM-VSG-010 | Invisible Medium / Imagination | Sound Design Short Radio | 193 | Let sound trigger listener's imagination to co-create |
| PRM-VSG-011 | Sound as Attention Architecture | Designing Sound | 192 | Treat sonic layers as routing devices for focus |
| PRM-VSG-012 | Frame as Active Meaning Device | The Photographers Eye | 192 | Use the boundaries of the image to create tension/balance |

---

## Execution Rules

1. **Batch size**: Process in one batch of 12.
2. **Golden example**: Re-read `PRM-HUM-009.yaml`.
3. **Dual-source gate**: Must read BOTH audit AND book.
4. **PRD gate**: Must load `PRD_INDEX.md` and the family PRD set (PRD_02, PRD_03, PRD_04, PRD_06, PRD_07, PRD_08) before writing any primitive.
5. **Example standard**: Every primitive must produce exactly **5 examples** — 1 BOOK: prefix + 4 CCP: prefixed use cases naming actual CCP surfaces.
6. **Float consistency**: VSG primitives should have HIGH `goal_bias.clarity` (0.7+) and HIGH `goal_bias.memorability` (0.6+).

## Completion Receipt

After finishing all 12 primitives, produce the receipt format specified in the SKILL.
