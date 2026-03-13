---
name: ccf-visual-assets
description: Curate research-verified REAL visual assets per blueprint with tribal verification and mode-appropriate selection
---

# /ccf-visual-assets {client_name}

// turbo-all

> **SKILLS_BASE:** `ccf-26/skills/ccf/`
> **SKILL:** `research/visual-asset-curator/SKILL.md`

**Objective:** Curate real visual assets as alternatives to AI-generated visuals. Per scene: provenance-verified, mode-tagged (REAL/AI/MIXED recommendation), tribally verified against H9 recognition codes. Human editors use the library to choose REAL vs AI per scene.

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify script, tribe profile, research exist", status: "pending" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Visual Asset Curator SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: INGEST - Load script scene structure + tribe visual codes", status: "pending" },
    { id: "step-4", description: "STEP 4: REASON - Curate assets per scene with mode + tribal checks", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write visual_asset_library.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Provenance + mode alignment + tribal verification", status: "pending" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml + emit distillation receipt", status: "pending" }
  ]
});
```

**DO NOT PROCEED until you have called `write_todos` above.**

---

## 📋 Step Execution Protocol (MANDATORY)

> [!CAUTION]
> **You MUST call `write_todos` at EVERY step transition.**

---

## STEP 1: PRE-FLIGHT

Mark step-1 `in_progress`.

| Check | Path | If Missing |
|-------|------|------------|
| 1 | `config.yaml` | STOP |
| 2 | `scripts/final/{blueprint_id}_script.md` (AUTHORIZED) | STOP → Run `/ccf-generate` first |
| 3 | `intelligence/tribe/tribe_profile.json` | WARN → Fallback to interchangeability test |
| 4 | `research/raw-deep/{blueprint_id}_raw_deep_research.md` | WARN → Proceed without topic context |
| 5 | `intelligence/soul/soul_values.json` | WARN → Proceed without cultural vocabulary |

Mark step-1 `completed`.

---

## STEP 2: LOAD SKILL

Mark step-2 `in_progress`.

1. Read FULL: `ccf-26/skills/ccf/research/visual-asset-curator/SKILL.md`
2. Internalize:
   - **4 Laws of Visual Asset Distillation**
   - Mode-appropriate selection matrix (TENSION → REAL, VULNERABILITY → MIXED/AI, RECOGNITION → REAL)
   - Tribal verification protocol (4 checks per image)
   - Provenance tiers (Gold/Silver/Bronze/Rejected)

Mark step-2 `completed`.

---

## STEP 3: INGEST

Mark step-3 `in_progress`.

1. Load authorized script → extract scene structure + mode tag per scene
2. Load `tribe_profile.json` → visual recognition codes:
   - `visual_recognition_codes.insider_objects[]`
   - `visual_recognition_codes.rejection_triggers[]`
   - `anti_aspirational_markers[]`
3. Load deep research dossier → topic context for search strategy
4. Load `soul_values.json` → cultural vocabulary for search terms

Report: "{N} scenes parsed. Visual codes: {N} insider, {N} rejection. Modes: T:{N} V:{N} R:{N}"

Mark step-3 `completed`.

---

## STEP 4: REASON

Mark step-4 `in_progress`.

**FOR EACH SCENE:**

1. **Identify visual need:** What should the viewer see?
2. **Determine mode** from script tag (T/V/R)
3. **Apply mode-form matrix:**
   - TENSION → recommend REAL (documentary evidence)
   - VULNERABILITY → recommend MIXED/AI (protect dignity)
   - RECOGNITION → recommend REAL (tribal authenticity)
4. **If REAL recommended:**
   - Generate search strategy using tribal codes + research context
   - Target: community archives, press agencies, cultural photography, documentary sources
   - Execute: `web_search("{tribal-specific search}") → read_url_content(url)`
   - **AVOID:** generic stock libraries, AI images labeled as real
5. **Curate 2-3 candidate assets per scene**
6. **Per asset, apply 4 Laws:**
   - Law 1 — Provenance: source, context, date, license, cultural context, authenticity → Tier 1/2/3
   - Law 2 — Mode check: "This image serves ___ mode because ___, viewer feels ___"
   - Law 3 — Tribal verification: 4 checks (recognition match, cultural accuracy, representation, interchangeability)
   - Law 4 — Authenticity gate: all 5 checks per asset

Mark step-4 `completed`.

---

## STEP 5: EMIT

Mark step-5 `in_progress`.

**CREATE FILE:** `visuals/assets/{blueprint_id}_visual_asset_library.json`

Per scene:
```json
{
  "scene_id": "SC01",
  "mode": "TENSION",
  "form_recommendation": "REAL",
  "form_rationale": "Documentary evidence strengthens the systemic claim",
  "assets": [
    {
      "asset_id": "A001",
      "description": "...",
      "source": "...",
      "provenance_tier": 1,
      "cultural_accuracy": "ACCURATE",
      "representation": "REPRESENTED",
      "tribal_codes_matched": ["..."],
      "editorial_guidance": {
        "use_when": "...",
        "avoid_when": "..."
      }
    }
  ]
}
```

Mark step-5 `completed`.

---

## STEP 6: VALIDATE

Mark step-6 `in_progress`.

| # | Gate | Requirement | If Fail |
|---|------|-------------|---------|
| 1 | Provenance | ≥50% Tier 1 or 2 | Search for higher-quality sources |
| 2 | Mode alignment | ≥80% follow mode recommendation | Re-assess form_recommendation |
| 3 | Tribal verification | All assets pass ≥3/4 checks | Replace failing assets |
| 4 | Editorial guidance | All assets have use_when + avoid_when | Add missing guidance |
| 5 | Stock detection | Zero unlabeled stock images | Flag or replace |

**CREATE FILE:** `visuals/assets/H13_DISTILLATION_RECEIPT.md`

Mark step-6 `completed`.

---

## STEP 7: CHECKPOINT

Mark step-7 `in_progress`.

1. Update `config.yaml`: `sessions.distribution.visual_assets.status = "complete"`

2. **OUTPUT:**
```
✅ VISUAL ASSETS CURATED
- Scenes: {N} processed
- Assets: {N} curated ({N} Tier1, {N} Tier2, {N} Tier3)
- Mode alignment: {X}%
- Tribal verification: {X}% passed
- File: visual_asset_library.json
- NEXT: Human editor selects REAL vs AI per scene
```

Mark step-7 `completed`.

---

## 🔗 NEXT: Human editor reviews `visual_asset_library.json` and selects per scene
