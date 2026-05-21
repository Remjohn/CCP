# Family Implementation Template: Psychological Diagnostics
# Plane: MEANING
# Family Code: PSY

## Instructions

You are executing the **Primitive YAML Codification** skill.

### Before You Start
1. Load and read the SKILL file: `skills/primitives/SKILL_Primitive_YAML_Codification.md`
2. Load the golden example: `primitives/meaning/_golden/PRM-HUM-009.yaml`
3. Load the registry catalog: `lab/CCP APRIL Updates/05_Core_Experience/Primitive_Packets_and_Registry_Spec.md` — Section 6.4
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

1. **You did not read the book.** Psychology books contain precise clinical terminology and distinct mechanisms. If your `why_it_works` uses only lay-language coaching generalities and could have been written without opening the book — you failed.
2. **You wrote generic examples.** Psychological diagnostic primitives have very specific activation contexts: client emotional state, CCP session phase, agent conversation mode. Name them precisely.
3. **You left any float at 0.5.** Every float requires a deliberate decision. 0.5 means no decision was made.
4. **You confused connection with persuasion.** PSY primitives primarily govern `goal_bias.connection`. They are not primarily persuasion tools. If `goal_bias.persuasion` is your highest float for a PSY primitive, you have misclassified it.
5. **You invented synergy IDs.** Verify every `synergizes_with` ID in the catalog before listing.
6. **You wrote `key_pages: "various"`.** Open the book. Find the chapters. Name them.

### BOOK VERIFICATION LOG (Complete Before Writing Any YAML)

For each book in this batch, confirm:
```
BOOK: [title]
├── Chapters confirmed read: [list at least 2 chapter titles]
├── One mechanism found ONLY in the book (not the audit): [write it]
├── One contraindication or failure mode from the book: [write it]
└── STATUS: VERIFIED / BLOCKED (if blocked, stop and report)
```
**Books for this template:** The Jim Rohn Guides Complete, Supercommunicators (Duhigg), The Psychology Workbook for Writers (Smith), I Haven't Been Entirely Honest With You (Hart)

### ANTI-DRIFT RULES (12-Primitive Batch)

- This is a small batch — there is no excuse for drift. Every primitive must be distinctly differentiated.
- **PSY family float fingerprint**: `goal_bias.connection` should be the dominant dimension (0.7–0.9) for most primitives. `goal_bias.surprise` should be LOW (0.1–0.2) — psychological diagnostics are not surprise tools. `goal_bias.clarity` should be moderate to high (0.5–0.8) since these primitives help diagnose and regulate.
- `ccp_workflow_fit.delivery_coaching` and `ccp_workflow_fit.authenticated_capture` should be the dominant workflow dimensions. If yours aren't, verify your reasoning.
- No two primitives in this batch may share the same `implementation_role`.

### PRE-SAVE CHECKLIST (Check Every Primitive Before Saving)

```
[ ] Book Verification Log completed for this primitive's source book
[ ] PRD_INDEX.md and relevant modular PRDs loaded and referenced
[ ] summary ≠ restatement of core_move
[ ] why_it_works cites a specific psychological mechanism from the book
[ ] EXACTLY 5 examples: 1 BOOK: prefix + 4 CCP: prefixed use cases
[ ] All CCP examples name at least one CCP surface (CCF, CMF, CVE, CBCS, Conscious Reactions, V2WS, CPSC, Telegram, AFFiNE, church/community)
[ ] Zero examples use banned phrases:
    - "a coach could use this" / "in content creation" / "in the app" / "in the platform"
[ ] At least 1 anti-example describing a harmful or counterproductive misapplication
[ ] No float anywhere is exactly 0.5
[ ] At least 2 floats are below 0.3 across phase_fit + surface_fit combined
[ ] goal_bias.connection is the highest or co-highest value
[ ] synergizes_with IDs verified in catalog
[ ] book_reference.chapters contains real chapter names
[ ] File saved to: primitives/meaning/psychological_diagnostics/[ID].yaml
```

---

### Your Task
Write one YAML file per primitive listed below. Save each to: `primitives/meaning/psychological_diagnostics/[ID].yaml`

### Source Files You Must Load

#### Audit Files
| Audit File | Path | Primitives |
|---|---|---|
| Jim Rohn Guides | `lab/CCP APRIL Updates/Public_Speaking_Audits/05_Psychology_and_Communication/AUDIT_Jim_Rohn_Communication_Guides.md` | PRM-PSY-007, 008 |
| Supercommunicators | `lab/CCP APRIL Updates/Public_Speaking_Audits/05_Psychology_and_Communication/AUDIT_Supercommunicators.md` | PRM-PSY-001, 002, 006, 010 |
| Psychology Workbook | `lab/CCP APRIL Updates/Public_Speaking_Audits/05_Psychology_and_Communication/AUDIT_The_Psychology_Workbook_for_Writers.md` | PRM-PSY-003, 011, 012 |
| Entirely Honest | `lab/CCP APRIL Updates/Public_Speaking_Audits/05_Psychology_and_Communication/AUDIT_I_havent_been_entirely_honest_with_you.md` | PRM-PSY-004, 005, 009 |

#### Book Files
| Book File | Path |
|---|---|
| Jim Rohn Guides | `lab/Public Speeaking Coaching/05_Psychology_and_Communication/The Jim Rohn Guides Complete.md` |
| Supercommunicators | `lab/Public Speeaking Coaching/05_Psychology_and_Communication/Supercommunicators_-_Charles_Duhigg.md` |
| Psychology Workbook | `lab/Public Speeaking Coaching/05_Psychology_and_Communication/The_Psychology_Workbook_for_Writers__Tools_-_Darian_Smith.md` |
| Entirely Honest | `lab/Public Speeaking Coaching/05_Psychology_and_Communication/I_havent_been_entirely_honest_with_you_-_Miranda_Hart.md` |

---

## Primitive Manifest (12 primitives)

| ID | Canonical Name | Source Audit | MCDA | Core Move |
|---|---|---|---:|---|
| PRM-PSY-007 | Identification Builds the Bridge | Jim Rohn Guides | 196 | Establish felt similarity before challenge |
| PRM-PSY-008 | Attack Problem Not Person | Jim Rohn Guides | 193 | Separate human from issue to preserve alliance |
| PRM-PSY-001 | Matching Principle | Supercommunicators | 192 | Detect conversation layer (practical/emotional/social) |
| PRM-PSY-002 | Looping for Understanding | Supercommunicators | 192 | Prove comprehension back to regulate nervous system |
| PRM-PSY-003 | Narrative Script Flipping | Psychology Workbook | 192 | Rotate rigid internal scripts into usable reality |
| PRM-PSY-004 | Stress Pot Regulator | Entirely Honest | 190 | Monitor and manage biological stress load |
| PRM-PSY-005 | Play as Physiological Medicine | Entirely Honest | 190 | Use play and relief as real intervention technology |
| PRM-PSY-006 | Deep Questions | Supercommunicators | 190 | Move conversation from surface to meaning |
| PRM-PSY-009 | Inner Critic Externalisation | Entirely Honest | 188 | Name and objectify the self-attacking voice |
| PRM-PSY-010 | Pre-Conversation Architecture | Supercommunicators | 188 | Prepare interaction conditions before speaking |
| PRM-PSY-011 | Drama Triangle Rotation | Psychology Workbook | 188 | Detect and rotate role structure (rescuer/victim/etc) |
| PRM-PSY-012 | Ego State Switching | Psychology Workbook | 187 | Guide interaction to Adult-to-Adult state |

---

## Execution Rules

1. **Batch size**: Process in one batch of 12.
2. **Golden example**: Re-read `PRM-HUM-009.yaml`.
3. **Dual-source gate**: Must read BOTH audit AND book.
4. **PRD gate**: Must load `PRD_INDEX.md` and the family PRD set (PRD_04, PRD_05, PRD_06, PRD_07, PRD_08, PRD_09) before writing any primitive.
5. **Example standard**: Every primitive must produce exactly **5 examples** — 1 BOOK: prefix + 4 CCP: prefixed use cases naming actual CCP surfaces.
6. **Float consistency**: Psychological primitives should have HIGH `goal_bias.connection` (0.7+) and HIGH `goal_bias.clarity` (0.6+).

## Completion Receipt

After finishing all 12 primitives, produce the receipt format specified in the SKILL.
