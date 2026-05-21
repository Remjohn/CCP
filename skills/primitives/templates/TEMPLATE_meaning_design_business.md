# Family Implementation Template: Design and Business
# Plane: MEANING
# Family Code: BUS

## Instructions

You are executing the **Primitive YAML Codification** skill.

### Before You Start
1. Load and read the SKILL file: `skills/primitives/SKILL_Primitive_YAML_Codification.md`
2. Load the golden example: `primitives/meaning/_golden/PRM-HUM-009.yaml`
3. Load the registry catalog: `lab/CCP APRIL Updates/05_Core_Experience/Primitive_Packets_and_Registry_Spec.md` — Section 6.6
4. Load the PRD router: `docs/prd/modules/PRD_INDEX.md`
5. Load the relevant modular PRDs for this family:
   - `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md`
   - `docs/prd/modules/PRD_02_CCF_Content_Factory.md`
   - `docs/prd/modules/PRD_03_CMF_Media_Factory.md`
   - `docs/prd/modules/PRD_04_CVE_Experience_Design.md`
   - `docs/prd/modules/PRD_06_Conscious_Reactions.md`
   - `docs/prd/modules/PRD_07_V2WS_Webinar.md`
   - `docs/prd/modules/PRD_08_Conscious_Primitives.md`

---

## ⚠️ ANTI-LAZINESS ENFORCEMENT — THIS TASK IS CONSIDERED FAILED IF:

1. **You did not read the book.** Design books contain visual theory, behavioral psychology, and business frameworks that are not present in the audit. Ellen Lupton's specific vocabulary (affordance, hierarchy, threshold) must appear in your `why_it_works`. Michael Port's specific frameworks (Red Velvet Rope, FEPS) must be traced to their source mechanisms.
2. **You wrote generic examples.** Design/business primitives apply to CMF visual outputs, Telegram Mini App UX, score cards, share assets, onboarding flows, and pricing architecture. Name the specific CCP artifact this primitive governs.
3. **You left any float at 0.5.** 0.5 = no calibration decision. Fix it.
4. **You over-assigned to the experience plane.** Some BUS primitives feel like experience primitives but belong here because they govern how content LOOKS and how value is COMMUNICATED, not how users BEHAVE in the app. Keep the plane distinction crisp.
5. **You invented synergy IDs.** Verify every `synergizes_with` ID in the catalog before listing.
6. **You wrote `key_pages: "various"`.** Open the book. Find the chapters. Name them.

### BOOK VERIFICATION LOG (Complete Before Writing Any YAML)

For each book in this batch, confirm:
```
BOOK: [title]
├── Chapters confirmed read: [list at least 2 chapter titles]
├── One design principle or vocabulary term from the book (not the audit): [write it]
├── One misuse mode the author warns about: [write it for anti_examples]
└── STATUS: VERIFIED / BLOCKED (if blocked, stop and report)
```
**Books for this template:** Design Is Storytelling (Lupton), Beautiful Users (Lupton), Book Yourself Solid for Creatives (Port), Thinking with Type (Lupton)

### ANTI-DRIFT RULES (14-Primitive Batch)

- Small batch — every primitive must be clearly differentiated.
- **BUS family float fingerprint**: `goal_bias.clarity` should dominate (0.7–0.9) for typography and hierarchy primitives. `goal_bias.connection` should dominate (0.7+) for relationship-building and sales cycle primitives. `goal_bias.surprise` should be LOW across the board (0.1–0.3) — design primitives create trust through consistency, not surprise.
- `ccp_workflow_fit.premium_differentiation` and `ccp_workflow_fit.experience_flow` should be elevated for most BUS primitives.
- Typography primitives (BUS-006, BUS-010, BUS-012) should have HIGH `surface_fit.visual` and LOW `surface_fit.voice`.

### PRE-SAVE CHECKLIST (Check Every Primitive Before Saving)

```
[ ] Book Verification Log completed for this primitive's source book
[ ] PRD_INDEX.md and relevant modular PRDs loaded and referenced
[ ] summary ≠ restatement of core_move
[ ] why_it_works cites specific design theory or business framework from the book
[ ] EXACTLY 5 examples: 1 BOOK: prefix + 4 CCP: prefixed use cases
[ ] All CCP examples name at least one CCP surface (CCF, CMF, CVE, CBCS, Conscious Reactions, V2WS, CPSC, Telegram, AFFiNE, church/community)
[ ] Zero examples use banned phrases:
    - "for example, this could be used when..."
    - "a coach could use this"
    - "in content creation"
    - "in the app" / "in the platform"
    - "for content creators" / "when creating content"
[ ] At least 1 anti-example with mechanism-grounded failure reason
[ ] No float anywhere is exactly 0.5
[ ] At least 2 floats are below 0.3 across phase_fit + surface_fit combined
[ ] goal_bias.clarity is the highest or co-highest value for design primitives
[ ] synergizes_with IDs verified in catalog
[ ] book_reference.chapters contains real chapter names
[ ] File saved to: primitives/meaning/design_business/[ID].yaml
```

---

### Your Task
Write one YAML file per primitive listed below. Save each to: `primitives/meaning/design_business/[ID].yaml`

### Source Files You Must Load

#### Audit Files
| Audit File | Path | Primitives |
|---|---|---|
| Design Is Storytelling | `lab/CCP APRIL Updates/Public_Speaking_Audits/06_Design_and_Business/AUDIT_Design_Is_Storytelling_Ellen_Lupton.md` | PRM-BUS-001, 002, 003, 013 |
| Beautiful Users | `lab/CCP APRIL Updates/Public_Speaking_Audits/06_Design_and_Business/AUDIT Beautiful Users Ellen Lupton.md` | PRM-BUS-004, 009, 014 |
| Book Yourself Solid | `lab/CCP APRIL Updates/Public_Speaking_Audits/06_Design_and_Business/AUDIT Book Yourself Solid Michael Port.md` | PRM-BUS-005, 007, 008, 011 |
| Thinking with Type | `lab/CCP APRIL Updates/Public_Speaking_Audits/06_Design_and_Business/AUDIT Thinking with Type Graphic Design Ellen Lupton.md` | PRM-BUS-006, 010, 012 |

#### Book Files
| Book File | Path |
|---|---|
| Design Is Storytelling | `lab/Public Speeaking Coaching/06_Design_and_Business/Design Is Storytelling - Ellen Lupton.md` |
| Beautiful Users | `lab/Public Speeaking Coaching/06_Design_and_Business/Beautiful Users - Ellen Lupton.md` |
| Book Yourself Solid | `lab/Public Speeaking Coaching/06_Design_and_Business/Book Yourself Solid for Creatives - Michael Port.md` |
| Thinking with Type | `lab/Public Speeaking Coaching/06_Design_and_Business/Thinking with Type 3rd Edition - Ellen Lupton.md` |

---

## Primitive Manifest (14 primitives)

| ID | Canonical Name | Source Audit | MCDA | Core Move |
|---|---|---|---:|---|
| PRM-BUS-001 | Perception and Guidance Stack | Design Is Storytelling | 199 | Design visuals and action cues as one integrated system |
| PRM-BUS-002 | Emotional Journey / Peak-End | Design Is Storytelling | 196 | Structure path so remembered ending compounds trust |
| PRM-BUS-003 | Narrative Structural Backbone | Design Is Storytelling | 194 | Give UX a meaningful progression rather than flat assets |
| PRM-BUS-004 | Design for Lived Use | Beautiful Users | 194 | Optimize for real user state and moment of use |
| PRM-BUS-005 | FEPS Benefit Translation | Book Yourself Solid | 194 | Translate features into functional/emotional/physical/spiritual benefits |
| PRM-BUS-006 | Hierarchy as Attention Routing | Thinking with Type | 192 | Route eye/mind through visual and semantic hierarchy |
| PRM-BUS-007 | Social Media as Relationship | Book Yourself Solid | 192 | Treat distribution as ongoing trust-building |
| PRM-BUS-008 | Invitation-Based Sales | Book Yourself Solid | 190 | Replace pressure with progressive invitations |
| PRM-BUS-009 | Dignity Reduces Friction | Beautiful Users | 189 | Reduce hesitation by preserving user dignity |
| PRM-BUS-010 | The Grid as Program | Thinking with Type | 188 | Use invisible structures for scalable consistency |
| PRM-BUS-011 | Red Velvet Rope Policy | Book Yourself Solid | 188 | Explicitly disqualify bad fits to compound trust |
| PRM-BUS-013 | Journey Threshold Design | Design Is Storytelling | 184 | Shape experience around meaningful entries/pivots/completions |
| PRM-BUS-012 | Typography as Voice | Thinking with Type | 182 | Make type act as a nonverbal extension of tone |
| PRM-BUS-014 | Affordance as Invitation | Beautiful Users | 176 | Make next action feel obvious and behaviorally inviting |

---

## Execution Rules

1. **Batch size**: Process in one batch of 14.
2. **Golden example**: Re-read `PRM-HUM-009.yaml`.
3. **Dual-source gate**: Must read BOTH audit AND book.
4. **PRD gate**: Must load `PRD_INDEX.md` and the family PRD set (PRD_01, PRD_02, PRD_03, PRD_04, PRD_06, PRD_07, PRD_08) before writing any primitive.
5. **Example standard**: Every primitive must produce exactly **5 examples** — 1 BOOK: prefix + 4 CCP: prefixed use cases naming actual CCP surfaces.
6. **Float consistency**: Design primitives should have HIGH `goal_bias.clarity` (0.7+) and HIGH `goal_bias.connection` (0.6+).

## Completion Receipt

After finishing all 14 primitives, produce the receipt format specified in the SKILL.
