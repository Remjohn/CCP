# Family Implementation Template: Referral and Trust-Transfer
# Plane: MEANING
# Family Code: REF

---

## ⚠️ ANTI-LAZINESS ENFORCEMENT — THIS TASK IS CONSIDERED FAILED IF:

1. **You did not read the book.** Referral books (Giftology, Challenger Sale, etc.) contain specific psychological frameworks for trust transfer that are not in the audit. If your `why_it_works` does not cite specific terms like "Mobilizer", "Recipient-Centric", or "Trust-Transfer Ladder" from the books — you have failed.
2. **You wrote generic examples.** Every `examples.context` must name a specific CCP growth moment (partner interview, challenge handoff, proof-asset delivery). "A coach could ask for a referral when..." is not a valid context.
3. **You left any float at 0.5.** Every float must be a deliberate calibration decision.
4. **You confused referrals with general marketing.** REF primitives govern the **transfer of trust** between specific parties. If your primitive is just about general awareness, it belongs in a different family.
5. **You invented synergy IDs.** Verify every ID in `synergizes_with` against the catalog before listing.
6. **You wrote `key_pages: "various"`.** Real chapter names and page ranges are required. Open the book file.

### BOOK VERIFICATION LOG (Complete Before Writing Any YAML)

For each book in this batch, confirm:
```
BOOK: [title]
├── Chapters confirmed read: [list at least 2 chapter titles]
├── One trust mechanism found ONLY in the book (not the audit): [write it]
├── One failure mode or warning from the book: [write it for anti_examples]
└── STATUS: VERIFIED / BLOCKED (if blocked, stop and report)
```
**Books for this template:** 21 Power Principles (Abraham), Sales Success through Client Referrals, Giftology (Ruhlin), The Activator Advantage (Dixon), The Challenger Sale (Dixon), Million Dollar Referrals (Weiss), The Effortless Experience

### ANTI-DRIFT RULES (9-Primitive Batch)

- This is a small batch — no drift is acceptable. Each primitive must be sharply differentiated.
- **REF family float fingerprint**: `goal_bias.persuasion` and `goal_bias.connection` should both be high (0.7–0.9). `goal_bias.surprise` should be LOW (0.1–0.3).
- `ccp_workflow_fit.experience_flow` and `ccp_workflow_fit.premium_differentiation` should be elevated.
- No two consecutive primitives may share an identical `implementation_role`.

### PRE-SAVE CHECKLIST (Check Every Primitive Before Saving)

```
[ ] Book Verification Log completed for this primitive's source book
[ ] PRD_INDEX.md and relevant modular PRDs loaded and referenced
[ ] summary ≠ restatement of core_move
[ ] why_it_works cites a specific trust-transfer mechanism from the book
[ ] EXACTLY 5 examples: 1 BOOK: prefix + 4 CCP: prefixed use cases
[ ] All CCP examples name at least one CCP surface (CCF, CMF, CVE, CBCS, Conscious Reactions, V2WS, CPSC, Telegram, AFFiNE, church/community)
[ ] Zero examples use banned phrases:
    - "a coach could use this" / "in content creation" / "in the app" / "in the platform"
[ ] At least 1 anti-example with mechanism-grounded failure reason
[ ] No float anywhere is exactly 0.5
[ ] goal_bias.persuasion is 0.7 or higher
[ ] goal_bias.connection is 0.7 or higher
[ ] synergizes_with IDs verified in catalog
[ ] book_reference.chapters contains real chapter names
[ ] File saved to: primitives/meaning/referral_trust_transfer/[ID].yaml
```

---

## Before You Start
1. Load and read the SKILL file: `skills/primitives/SKILL_Primitive_YAML_Codification.md`
2. Load the golden example: `primitives/meaning/_golden/PRM-HUM-009.yaml`
3. Load the registry catalog: `lab/CCP APRIL Updates/05_Core_Experience/Primitive_Packets_and_Registry_Spec.md` — Section 6.9
4. Load the PRD router: `docs/prd/modules/PRD_INDEX.md`
5. Load the relevant modular PRDs for this family:
   - `docs/prd/modules/PRD_04_CVE_Experience_Design.md`
   - `docs/prd/modules/PRD_05_CBCS_Law28.md`
   - `docs/prd/modules/PRD_06_Conscious_Reactions.md`
   - `docs/prd/modules/PRD_08_Conscious_Primitives.md`
   - `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md`

## Your Task
Write one YAML file per primitive listed below. Save each to: `primitives/meaning/referral_trust_transfer/[ID].yaml`

## Source Files You Must Load

#### Audit Files
| Audit File | Path | Primitives |
|---|---|---|
| Mitano Referral Leverage | `lab/CCP APRIL Updates/03_Growth_Library/AUDIT Mitano Referral Leverage CCP Referral Magnitude.md` | ALL REF Primitives |

#### Book Files
| Book File | Path |
|---|---|
| 21 Power Principles | `Mitano Referral Leverage/21PowerPrinciples.md` |
| Sales Success through Client Referrals | `Mitano Referral Leverage/Creating a Million-Dollar-a-Year Sales Income_ Sales Success through Client Referrals ( PDFDrive ).md` |
| Giftology | `Mitano Referral Leverage/Giftology - John Ruhlin.md` |
| The Activator Advantage | `Mitano Referral Leverage/The Activator Advantage - Matthew Dixon.md` |
| The Challenger Sale | `Mitano Referral Leverage/The Challenger Sale - Matthew Dixon.md` |
| Million Dollar Referrals | `Mitano Referral Leverage/Million Dollar Referrals - Alan Weiss.md` |
| The Effortless Experience | `Mitano Referral Leverage/The Effortless Experience - Matthew Dixon.md` |

---

## Primitive Manifest (9 primitives)

| ID | Canonical Name | Source Audit | MCDA | Core Move |
|---|---|---|---:|---|
| PRM-REF-001 | Partner Over Source | Mitano Referral | 193 | Select operating partners with shared upside rather than passive link-sharers |
| PRM-REF-007 | Commercial Reframe Architecture | Mitano Referral | 193 | Change the prospect's understanding of their problem before pitching a solution |
| PRM-REF-006 | Preemptive Value Shaping | Mitano Referral | 192 | Deliver insight before the prospect enters commodity-comparison mode |
| PRM-REF-002 | Trust-Transfer Ladder | Mitano Referral | 191 | Stage the introduction so the guest experiences value (interview, output, benchmark) before any ask |
| PRM-REF-005 | Recipient-Centric Relationship Artifact Design | Mitano Referral | 191 | Deliver proof outputs that make the recipient feel proud, avoiding overt platform branding |
| PRM-REF-003 | Hidden Asset Mining | Mitano Referral | 189 | Convert byproducts like interview footage and benchmark data into primary acquisition tools |
| PRM-REF-004 | Piggyback Distribution | Mitano Referral | 188 | Leverage the partner's existing audience trust rather than building from zero |
| PRM-REF-008 | Message-to-Role Resonance Mapping | Mitano Referral | 187 | Translate the same core capability differently for the coach, the audience, and the partner |
| PRM-REF-009 | Constructive Tension Control | Mitano Referral | 182 | Apply enough pressure to force a decision without breaking the underlying trust |

---

## Execution Rules

1. **Batch size**: Process in one batch of 9.
2. **Golden example**: Re-read `PRM-HUM-009.yaml`.
3. **Dual-source gate**: Must read BOTH audit AND book.
4. **PRD gate**: Must load `PRD_INDEX.md` and the family PRD set (PRD_04, PRD_05, PRD_06, PRD_08, PRD_09) before writing any primitive.
5. **Example standard**: Every primitive must produce exactly **5 examples** — 1 BOOK: prefix + 4 CCP: prefixed use cases naming actual CCP surfaces.
6. **Float consistency**: Referral primitives should have HIGH `goal_bias.persuasion` (0.7+) and HIGH `goal_bias.connection` (0.7+).

## Completion Receipt

After finishing all 9 primitives, produce the receipt format specified in the SKILL.
