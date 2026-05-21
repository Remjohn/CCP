# Family Implementation Template: Voice and Audio Intimacy
# Plane: MEANING
# Family Code: VOC

---

## ⚠️ ANTI-LAZINESS ENFORCEMENT — THIS TASK IS CONSIDERED FAILED IF:

1. **You did not read the book.** Voice and audio books contain specific technical advice on breathing, cadence, and spatial proximity that are not in the audit. If your `why_it_works` does not contain specific audio or broadcast terminology from the source book — you have failed.
2. **You wrote generic examples.** Every `examples.context` must name a specific CCP workflow stage (CMF generation, CCF capture, Conscious Reaction delivery). "A voice note could use this when..." is not a valid context.
3. **You left any float at 0.5.** Every float must be a deliberate calibration decision.
4. **You conflated text with voice.** Most VOC primitives should have HIGH `surface_fit.voice` and LOW `surface_fit.text`. If `text` is higher than `voice` for a VOC primitive, you have misclassified it.
5. **You invented synergy IDs.** Verify every ID in `synergizes_with` against the catalog before listing.
6. **You wrote `key_pages: "various"`.** Real chapter names and page ranges are required. Open the book file.

### BOOK VERIFICATION LOG (Complete Before Writing Any YAML)

For each book in this batch, confirm:
```
BOOK: [title]
├── Chapters confirmed read: [list at least 2 chapter titles]
├── One audio mechanism found ONLY in the book (not the audit): [write it]
├── One warning or failure mode for anti_examples: [write it]
└── STATUS: VERIFIED / BLOCKED (if blocked, stop and report)
```
**Books for this template:** Better Broadcast Writing (Dobbs), Finding Your Voice (Quicke), Interviewing for Radio (Beaman), Sound Design for Short Radio Broadcasting

### ANTI-DRIFT RULES (12-Primitive Batch)

- After every 6 primitives, re-read the golden example `PRM-HUM-009.yaml` and verify quality levels.
- **VOC family float fingerprint**: `goal_bias.connection` should be the dominant dimension (0.7–0.9). `surface_fit.voice` and `surface_fit.sonic` should be the dominant surfaces. `phase_fit.delivery` should be high (0.7+) for most VOC primitives.
- `ccp_workflow_fit.delivery_coaching` and `ccp_workflow_fit.authenticated_capture` should be elevated.
- No two consecutive primitives may share an identical `implementation_role`.

### PRE-SAVE CHECKLIST (Check Every Primitive Before Saving)

```
[ ] Book Verification Log completed for this primitive's source book
[ ] PRD_INDEX.md and relevant modular PRDs loaded and referenced
[ ] summary ≠ restatement of core_move
[ ] why_it_works cites a specific audio mechanism from the book
[ ] EXACTLY 5 examples: 1 BOOK: prefix + 4 CCP: prefixed use cases
[ ] All CCP examples name at least one CCP surface (CCF, CMF, CVE, CBCS, Conscious Reactions, V2WS, CPSC, Telegram, AFFiNE, church/community)
[ ] Zero examples use banned phrases:
    - "a coach could use this" / "in content creation" / "in the app" / "in the platform"
[ ] At least 1 anti-example with mechanism-grounded failure reason
[ ] No float anywhere in the file is exactly 0.5
[ ] surface_fit.voice is 0.7 or higher
[ ] goal_bias.connection is the highest or co-highest value
[ ] synergizes_with IDs verified in catalog
[ ] book_reference.chapters contains real chapter names
[ ] File saved to: primitives/meaning/voice_audio_intimacy/[ID].yaml
```

---

## Before You Start
1. Load and read the SKILL file: `skills/primitives/SKILL_Primitive_YAML_Codification.md`
2. Load the golden example: `primitives/meaning/_golden/PRM-HUM-009.yaml`
3. Load the registry catalog: `lab/CCP APRIL Updates/05_Core_Experience/Primitive_Packets_and_Registry_Spec.md` — Section 6.8
4. Load the PRD router: `docs/prd/modules/PRD_INDEX.md`
5. Load the relevant modular PRDs for this family:
   - `docs/prd/modules/PRD_02_CCF_Content_Factory.md`
   - `docs/prd/modules/PRD_03_CMF_Media_Factory.md`
   - `docs/prd/modules/PRD_04_CVE_Experience_Design.md`
   - `docs/prd/modules/PRD_05_CBCS_Law28.md`
   - `docs/prd/modules/PRD_06_Conscious_Reactions.md`
   - `docs/prd/modules/PRD_07_V2WS_Webinar.md`
   - `docs/prd/modules/PRD_08_Conscious_Primitives.md`
   - `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`

## Your Task
Write one YAML file per primitive listed below. Save each to: `primitives/meaning/voice_audio_intimacy/[ID].yaml`

## Source Files You Must Load

#### Audit Files
| Audit File | Path | Primitives |
|---|---|---|
| Better Broadcast Writing | `lab/CCP APRIL Updates/Public_Speaking_Audits/08_Sound_Design/AUDIT_Better_Broadcast_Writing_Greg_Dobbs.md` | PRM-VOC-001, 004, 006, 008 |
| Finding Your Voice | `lab/CCP APRIL Updates/Public_Speaking_Audits/08_Sound_Design/AUDIT_Finding_Your_Voice_Rob_Quicke.md` | PRM-VOC-002, 003, 005, 009 |
| Interviewing for Radio | `lab/CCP APRIL Updates/Public_Speaking_Audits/08_Sound_Design/AUDIT_Interviewing_for_Radio.md` | PRM-VOC-007, 010, 012 |
| Short Radio Broadcasting | `lab/CCP APRIL Updates/Public_Speaking_Audits/08_Sound_Design/AUDIT_Sound_Design_for_Short_Radio_Broadcasting.md` | PRM-VOC-011 |

#### Book Files
| Book File | Path |
|---|---|
| Better Broadcast Writing | `lab/Public Speeaking Coaching/08_Sound_Design/Better Broadcast Writing.md` |
| Finding Your Voice | `lab/Public Speeaking Coaching/08_Sound_Design/Finding Your Voice.md` |
| Interviewing for Radio | `lab/Public Speeaking Coaching/08_Sound_Design/Interviewing for Radio.md` |
| Sound Design Short Radio | `lab/Public Speeaking Coaching/08_Sound_Design/Sound Design for Short Radio Broadcasting.md` |

---

## Primitive Manifest (12 primitives)

| ID | Canonical Name | Source Audit | MCDA | Core Move |
|---|---|---|---:|---|
| PRM-VOC-001 | Write for the Distracted Ear | Better Broadcast Writing | 197 | Write so the message remains clear and memorable even when heard once in imperfect attention conditions |
| PRM-VOC-002 | Audience-of-One Intimacy | Finding Your Voice | 196 | Speak directly to a single imagined listener to create psychological closeness |
| PRM-VOC-003 | Writing for the Ear, Not the Eye | Finding Your Voice | 194 | Draft content specifically for spoken rhythm, breathing cadence, and auditory processing |
| PRM-VOC-004 | Proofread Aloud as Broadcast Validation | Better Broadcast Writing | 193 | Test every spoken line aloud before shipping it so dead phrasing and synthetic rhythm are caught early |
| PRM-VOC-005 | R.E.A.L. Audio Quality Gate | Finding Your Voice | 191 | Validate that audio feels relatable, engaging, authentic, and liberating before adding more polish |
| PRM-VOC-006 | Start Strong, End Strong | Better Broadcast Writing | 191 | Maximize the first and last lines because they disproportionately shape emotion, memory, and continuation |
| PRM-VOC-007 | The Theatre of the Mind | Interviewing for Radio | 185 | Use sound and speech to make the listener visualize the scene instead of merely receiving information |
| PRM-VOC-008 | Lead-In and Tag Architecture | Better Broadcast Writing | 184 | Make the opening orientation and closing handoff structurally deliberate rather than improvised |
| PRM-VOC-009 | Sensory Scene Anchoring | Finding Your Voice | 183 | Use vivid sensory cues to build the theater of the mind for the listener |
| PRM-VOC-010 | The Edited Essence | Interviewing for Radio | 180 | Compress aggressively until only the most signal-rich spoken material remains |
| PRM-VOC-011 | Microphonic Intimacy and Spatial Proximity | Sound Design Short Radio | 173 | Use proximity, mic feel, and acoustic nearness to increase disclosure, trust, and warmth |
| PRM-VOC-012 | The Silent Facilitator | Interviewing for Radio | 174 | Create better spoken output by listening actively and intervening minimally so the subject's real signal can surface |

---

## Execution Rules

1. **Batch size**: Process in one batch of 12.
2. **Golden example**: Re-read `PRM-HUM-009.yaml`.
3. **Dual-source gate**: Must read BOTH audit AND book.
4. **PRD gate**: Must load `PRD_INDEX.md` and the family PRD set (PRD_02, PRD_03, PRD_04, PRD_05, PRD_06, PRD_07, PRD_08, PRD_09) before writing any primitive.
5. **Example standard**: Every primitive must produce exactly **5 examples** — 1 BOOK: prefix + 4 CCP: prefixed use cases naming actual CCP surfaces.
6. **Float consistency**: Voice primitives should have HIGH `goal_bias.connection` (0.7+) and HIGH `surface_fit.voice` (0.7+).

## Completion Receipt

After finishing all 12 primitives, produce the receipt format specified in the SKILL.
