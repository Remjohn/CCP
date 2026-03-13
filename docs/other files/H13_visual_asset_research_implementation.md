# H13: Standalone Visual Asset Research — Implementation Architecture

**Hypothesis:** A NEW skill (no existing CCF infrastructure) that produces a curated library of research-verified REAL visual assets as alternatives to AI-generated visuals. Human editors decide per scene whether to use real images or AI-generated ones based on content mode and cultural sensitivity.

**Pipeline Position:** CCF Distribution Phase → Parallel to Visual Recipes → Visual Asset Library → Human Editor Selection  
**Existing Infrastructure:** NONE — this is a new skill  
**Gap Classification:** N/A — net-new capability  
**Dependency:** H9 (Visual Recognition Codes), H12 (Visual Recipes for scene structure), H6/H7 (Research Dossiers for topic context)

---

## Section 1: The Design Problem

The CCF pipeline currently assumes all visuals are AI-generated. For culturally specific, emotionally charged, or documentary-style content, real images carry authenticity that AI cannot replicate. H13 creates a parallel path that produces curated real assets — not replacing AI visuals but giving the human editor a CHOICE per scene.

### When Real Images Are Better Than AI

| Content Mode | Real Image Advantage | AI Image Advantage |
|:-------------|:--------------------|:-------------------|
| **TENSION** | Documentary evidence: real hospital, real policy document, real community meeting | Scale: showing systemic patterns across multiple contexts |
| **VULNERABILITY** | Community photography: authentic intimacy | Protection: abstracting pain without exploiting it |
| **RECOGNITION** | Tribal authenticity: real matembélé, real wax print, real gathering | Idealization: showing the tribe's aspirational self |

**The editorial principle:** Real images should be the DEFAULT recommendation for TENSION and RECOGNITION modes. AI should be the DEFAULT for VULNERABILITY modes (protecting dignity). The editor overrides based on context.

### Input Saturation Gate

| Input | Minimum Requirement | Source |
|:------|:-------------------|:-------|
| Content topic + mode | From blueprint (H1) | Blueprint Orchestrator output |
| Script with scene structure | Scene-by-scene breakdown | Script phase output |
| Visual Recognition Code Library | Tribal visual markers | H9 output (or fallback interchangeability test) |
| Deep Research Dossier | Topic context and evidence | H6 output |

---

## Section 2: The 4 Laws of Standalone Visual Asset Distillation

### Law 1 — Visual Asset Provenance

**Axiom:** *A real image without verified provenance is worse than an AI image.*

Every curated asset includes:

```
ASSET CARD
━━━━━━━━━━
Source:          [Publication/photographer/archive]
Context:         [What was happening when this was taken]
Date:            [When taken/published]
License:         [CC-BY / Editorial / Rights-Managed / Unknown]
Cultural Context: [What this image means to the tribe]
Authenticity:    [Photograph / Documentary / Staged / Stock]
```

**Provenance Quality Tiers:**
- **Tier 1 (Gold):** Known photographer, specific context, clear licensing, community origin
- **Tier 2 (Silver):** Credible publication, editor's context, standard licensing
- **Tier 3 (Bronze):** Stock or agency image with relevant visual content but no contextual provenance
- **Rejected:** Unknown origin, unverifiable context, or potentially exploitative framing

**Minimum:** ≥50% of curated assets must be Tier 1 or Tier 2. Tier 3 assets are included only as last resort and flagged transparently.

### Law 2 — Mode-Appropriate Visual Selection

**Axiom:** *Not all content modes benefit from real images.*

The curation algorithm tags each asset with mode recommendation:

| Asset Mode | Recommendation | Rationale |
|:-----------|:-------------|:----------|
| **TENSION** | REAL PREFERRED | Documentary evidence strengthens confrontational claims |
| **VULNERABILITY** | MIXED — Real only if dignity-preserving | Real images of private pain can be exploitative |
| **RECOGNITION** | REAL PREFERRED | Tribal recognition codes require authentic representation |

**Per-asset mode check:**
```
"This image serves _____ mode because it shows _____.
 The viewer will feel _____ seeing this in [REAL/AI] form.
 Using [the other form] instead would [strengthen/weaken/change] the emotional impact because _____."
```

Each asset includes: `mode`, `mode_justification`, `form_recommendation` (REAL / AI / EITHER), and `form_rationale`.

### Law 3 — Tribal Visual Verification

**Axiom:** *An outsider selecting images for a tribe selects what looks right to them. A tribal verification protocol selects what feels right to the tribe.*

**Verification protocol (per image):**

```
CHECK 1: Tribal Recognition Code Match
  Does the image contain recognized tribal visual codes (from H9)?
  → Matching codes: [list]
  → Missing codes: [list]

CHECK 2: Cultural Accuracy Test
  Is the cultural context accurate (not borrowed from a different culture)?
  "Would a tribe member say 'that's us' or 'that's close but not quite'?"
  → ACCURATE / APPROXIMATE / INACCURATE

CHECK 3: Representation Test
  Would a tribe member feel represented or stereotyped?
  "Does this image show the tribe as they see themselves, or as outsiders imagine them?"
  → REPRESENTED / STEREOTYPED / NEUTRAL

CHECK 4: Interchangeability Test (fallback if H9 codes not available)
  "Could this image be used for content about a DIFFERENT community without anyone noticing?"
  → YES = GENERIC — reject
  → NO = SPECIFIC — keep
```

### Law 4 — Visual Asset Authenticity Gate

**Axiom:** *Curated real images must meet a higher standard than AI images — because real images claim to BE real.*

**5 Gate Checks (per asset):**

```
CHECK 1: Provenance
  Source, context, licensing verified → Tier 1/2/3

CHECK 2: Not Stock
  Image is not from a commercial stock library (or flagged if it is)

CHECK 3: Mode-Appropriate
  Image serves the content mode it's assigned to

CHECK 4: Tribal Verification
  Image passes 3/4 tribal verification checks

CHECK 5: Editorial Guidance
  Asset includes clear recommendation:
  "Use INSTEAD of AI when: [condition]"
  "Do NOT use when: [condition]"
```

---

## Section 3: New Skill Architecture

Since H13 is new, this defines the skill from scratch:

```yaml
# SKILL.md frontmatter
name: "Visual Asset Researcher"
description: "Curates research-verified real visual assets as alternatives to AI-generated visuals"
session_id: ccf-visual-assets
phase: distribution
inputs:
  - config.yaml
  - scripts/final/{blueprint_id}_script.md (AUTHORIZED)
  - intelligence/soul/soul_values.json
  - intelligence/tribe/tribe_profile.json (for visual recognition codes)
  - research/deep/{blueprint_id}_deep_research.md
outputs:
  - visuals/assets/{blueprint_id}_visual_asset_library.json
depends_on: [story-5.2]
```

**I-R-E-V-C Protocol:**

```
INGEST:
  - Load authorized script (scene structure + mode tags)
  - Load tribe_profile.json for visual recognition codes
  - Load deep research dossier for topic context

REASON:
  Per scene:
    1. Identify visual need (what should the viewer see?)
    2. Determine mode (T/V/R from script tag)
    3. Assess real-vs-AI recommendation
    4. If REAL recommended: generate search strategy for authentic images
    5. Curate 2-3 candidate assets per scene
    6. Apply provenance, mode, and tribal verification

EMIT:
  Output visual_asset_library.json with per-scene assets

VALIDATE:
  - ≥50% Tier 1/2 provenance
  - All assets mode-tagged
  - Tribal verification passed (3/4 checks per asset)
  - Editorial guidance included per asset

CHECKPOINT:
  - Update config.yaml with visual asset status
```

---

## Section 4: Output Format

```json
{
  "blueprint_id": "B001",
  "coach": "Coach Adele",
  "date": "2025-02-22",
  "scenes": [
    {
      "scene_id": "SC01",
      "mode": "TENSION",
      "form_recommendation": "REAL",
      "form_rationale": "Documentary evidence strengthens the systemic injustice claim",
      "assets": [
        {
          "asset_id": "A001",
          "description": "Belgian hospital waiting room, 2023",
          "source": "Belga Press Agency",
          "license": "Editorial",
          "provenance_tier": 2,
          "cultural_accuracy": "ACCURATE",
          "representation": "NEUTRAL",
          "tribal_codes_matched": ["institutional_space", "waiting"],
          "editorial_guidance": {
            "use_when": "Content confronts systemic medical neglect",
            "avoid_when": "Content is about personal healing journey (mode: VULNERABILITY)"
          }
        }
      ]
    }
  ],
  "gate_results": {
    "provenance_distribution": { "tier_1": 2, "tier_2": 3, "tier_3": 1 },
    "mode_coverage": { "T": 3, "V": 1, "R": 2 },
    "tribal_verification_pass_rate": "5/6 = 83%"
  }
}
```

---

## Section 5: 5 Micro-Hypothesis Evaluations

**MH1 — Provenance Quality Test:** ≥50% of assets Tier 1 or 2. Verifiable: count `provenance_tier` values.

**MH2 — Mode-Form Alignment Test:** ≥80% of assets follow the mode recommendation (TENSION/RECOGNITION → REAL, VULNERABILITY → MIXED/AI). Verifiable: cross-reference `mode` against `form_recommendation`.

**MH3 — Tribal Verification Coverage:** All assets pass ≥3/4 tribal verification checks. Verifiable: check verification fields.

**MH4 — Editorial Guidance Completeness:** All assets include both `use_when` and `avoid_when` guidance. Verifiable: check field presence.

**MH5 — Stock Detection:** Zero Tier 3 assets without explicit flagging. Verifiable: verify all stock images are transparently labeled.

---

## Validation Receipt

```
H13 VALIDATION RECEIPT
━━━━━━━━━━━━━━━━━━━━━━
Blueprint:       [ID]
Coach:           [name]
Date:            [timestamp]
Script Source:   [filename]
Assets Curated:  [count]

LAW COMPLIANCE
━━━━━━━━━━━━━━
Law 1 — Provenance:              [Tier 1: n, Tier 2: n, Tier 3: n]  [PASS/FAIL if <50% T1/T2]
Law 2 — Mode-Form Alignment:     [n/total aligned = x%]  [PASS/FAIL if <80%]
Law 3 — Tribal Verification:     [n/total passed 3/4 checks]  [PASS/FAIL]
Law 4 — Authenticity Gate:       [5/5 checks per asset]  [PASS/FAIL]

MICRO-HYPOTHESES
━━━━━━━━━━━━━━━━
MH1 Provenance Quality:    [PASS/FAIL]
MH2 Mode-Form Alignment:   [PASS/FAIL]
MH3 Tribal Verification:   [PASS/FAIL]
MH4 Editorial Guidance:    [PASS/FAIL]
MH5 Stock Detection:       [PASS/FAIL]

STATUS: [AUTHENTICATED / PROVISIONAL / FAILED]
```
