---
name: ccf-raw-research
description: Execute H6 deep + H7 fresh RAW research (4000 words each) per blueprint, feeding downstream analysts
---

# /ccf-raw-research {client_name}

// turbo-all

> **SKILLS_BASE:** `ccf-26/skills/ccf/`
> **H6 SKILL:** `research/raw-deep-research/SKILL.md`
> **H7 SKILL:** `research/raw-fresh-research/SKILL.md`
> **DISTILLER:** `distillation/research-distiller/SKILL.md`

**Objective:** Execute both the 4000-word deep AND fresh RAW research per blueprint, then validate via the research-distiller gatekeeper. This produces the upstream fuel that the existing 41 deep/fresh analysts will consume.

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify blueprints, soul, tribe, philosophy exist", status: "pending" },
    { id: "step-2", description: "STEP 2: LOAD SKILLS - Read H6 + H7 + Distiller SKILL.md files", status: "pending" },
    { id: "step-3", description: "STEP 3: CONTEXT LOAD - Load blueprint + soul + tribe + philosophy", status: "pending" },
    { id: "step-4", description: "STEP 4: H6 DEEP RAW - Execute deep research per blueprint (4000w)", status: "pending" },
    { id: "step-5", description: "STEP 5: H7 FRESH RAW - Execute fresh research per blueprint (4000w)", status: "pending" },
    { id: "step-6", description: "STEP 6: DISTILLATION GATE - Run research-distiller on both dossiers", status: "pending" },
    { id: "step-7", description: "STEP 7: CHECKPOINT - Update config.yaml + log metrics", status: "pending" }
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

**ACTIONS:**

| Check | Path | If Missing |
|-------|------|------------|
| 1 | `config.yaml` | STOP → Run `/ccf-init` first |
| 2 | `research/content_blueprints.json` | STOP → Run `/ccf-blueprint` first |
| 3 | `intelligence/soul/soul_values.json` | STOP → Run `/ccf-soul-extract` first |
| 4 | `intelligence/tribe/tribe_profile.json` | STOP → Run `/ccf-tribe-extract` first |
| 5 | `intelligence/philosophy/coach_philosophy_brief_v*.md` | WARN → Proceed without philosophy guidance |
| 6 | `tools/firecrawl_wrapper.py` | STOP → Firecrawl unavailable for deep research |

**Read `content_blueprints.json`:**
- Count blueprints: {N}
- For each: note `blueprint_id`, `archetype`, `theme`, `mode_assignments`

Report: "{N} blueprints to research. Firecrawl: ✅, Browser: ✅, Philosophy brief: ✅/⚠️"

Mark step-1 `completed`.

---

## STEP 2: LOAD SKILLS

Mark step-2 `in_progress`.

**Read ALL THREE skill files:**

1. `ccf-26/skills/ccf/research/raw-deep-research/SKILL.md` — H6 Deep Excavator
2. `ccf-26/skills/ccf/research/raw-fresh-research/SKILL.md` — H7 Fresh Excavator
3. `ccf-26/skills/ccf/distillation/research-distiller/SKILL.md` — Gatekeeper

**Also read support skills:**
4. `ccf-26/skills/ccf/research/strategy-director/SKILL.md` — Designs research queries for H6
5. `ccf-26/skills/ccf/research/smart-query-generator/SKILL.md` — Generates queries for H7

> [!IMPORTANT]
> **H6 and H7 are DIFFERENT from the existing analyst protocols.** H6/H7 produce 4000-word RAW dossiers. The existing analysts (which you are NOT running here) will later consume these to produce 1000-1200 word briefs.

Mark step-2 `completed`.

---

## STEP 3: CONTEXT LOAD

Mark step-3 `in_progress`.

**Load per-blueprint context:**

For EACH blueprint in `content_blueprints.json`:

1. Extract: `blueprint_id`, `archetype`, `theme`, `mode_assignments`
2. Load `soul_values.json` → coach's vocabulary, metaphors, stance
3. Load `tribe_profile.json` → tribal codes, visual recognition, language
4. Load `coach_philosophy_brief` → belief layers L1/L2/L3, stories, contradictions
5. Prepare Strategy Director input (for H6):
   ```json
   {
     "blueprint_id": "{id}",
     "archetype": "{type}",
     "theme": "{title}",
     "mode_assignments": {...},
     "coaching_philosophy_l2_beliefs": [...],
     "tribe_visual_codes": [...]
   }
   ```

Mark step-3 `completed`.

---

## STEP 4: H6 DEEP RAW (Per Blueprint)

Mark step-4 `in_progress`.

**FOR EACH blueprint:**

### Phase A: Strategy Direction
- Execute Strategy Director → `conscious_research_plan.json` with 7 angles × 3 queries = 21 targeted queries
- Queries must target **storytelling fuel**, not just information

### Phase B: Deep Execution (Firecrawl)
```bash
# Per query:
python tools/firecrawl_wrapper.py search "QUERY" --limit 5
python tools/firecrawl_wrapper.py scrape "URL"
```

### Phase C: Critic Loop
- Load `skills/ccf/research/critic/SKILL.md`
- Apply enhanced checks: mode classified? depth tagged? storytelling tagged?
- If rejected → reformulate and retry (max 2 retries per query)

### Phase D: Synthesis
- Write 4000-word dossier: `research/raw-deep/{blueprint_id}_raw_deep_research.md`
- Structure: Executive Summary → 7-Angle Analysis → Storytelling Fuel Index → Synergy Map → Gate Results
- **Every finding tagged:** `mode` (T/V/R), `depth_level` (L1/L2/L3), `storytelling_tag`, `visual_potential`, `tribe_invisible`

### Law Gates After Synthesis:
- Law 1: Mode coverage — all 3 modes present
- Law 2: Depth — L2 ≥ 30%, L3 ≥ 10%
- Law 3: Storytelling fuel — ≥ 2 per category
- Law 4: Authenticity — ≥ 1 soul-challenge finding

**If any gate fails:** Re-execute targeted research for the failing dimension.

Mark step-4 `completed`.

---

## STEP 5: H7 FRESH RAW (Per Blueprint)

Mark step-5 `in_progress`.

**FOR EACH blueprint:**

### Phase A: Query Generation
- Execute Smart Query Generator with `mode = "fresh"`
- Generate 5-8 queries optimized for recency + surprise
- **Include deep dossier summary** — "avoid these angles" to ensure novelty

### Phase B: Browser Execution
```
FOR EACH query:
  1. web_search("{query}")
  2. Extract 2-3 REAL URLs
  3. Prioritize: HOT (<14 days) > WARM (14-90) > COOL (90-180)
  4. If <2 results → reformulate with tribal language, retry ONCE
```

### Phase C: URL Verification
```
FOR EACH url:
  read_url_content({ url: "{url}" })
  → VALID + RELEVANT → extract data point + metadata
  → INVALID → search for replacement
```

### Phase D: Synthesis
- Write 4000-word dossier: `research/raw-fresh/{blueprint_id}_raw_fresh_research.md`
- Structure: Executive Summary → Temporal Intelligence (HOT/WARM/COOL) → Vibe Bait Index → H6 Complement Map → Gate Results
- **Every finding tagged:** `novelty_class`, `surprise_score`, `recency_grade`, `mode`, `vibe_bait`, `temporal_leverage`

### Law Gates After Synthesis:
- Law 1: Novelty ≥ 50% (not duplicating deep dossier)
- Law 2: Recency — HOT ≥ 30%, HOT+WARM ≥ 50%
- Law 3: Surprise density ≥ 30%
- Law 4: Vibe bait count ≥ 3

**If any gate fails:** Re-execute with more contrarian/tribal/niche queries.

Mark step-5 `completed`.

---

## STEP 6: DISTILLATION GATE

Mark step-6 `in_progress`.

> [!CAUTION]
> **MANDATORY GATE — Pipeline blocks if this fails for ≥2 laws.**

1. Read FULL: `ccf-26/skills/ccf/distillation/research-distiller/SKILL.md`
2. **Per blueprint**, execute 4-phase audit:
   - Phase 1: Deep Research Audit (H6 — 4 laws)
   - Phase 2: Fresh Research Audit (H7 — 4 laws)
   - Phase 3: Cross-Dossier Coherence (0 duplicates, ≥3 [DEEPENS H6] tags)
   - Phase 4: Emit Receipt

3. **CREATE FILE per blueprint:** `research/H6_H7_DISTILLATION_RECEIPT.md`

**Decision logic:**
- ALL PASS → STATUS: AUTHENTICATED → proceed to `/ccf-research-deep`
- 1 law FAIL → STATUS: PROVISIONAL → proceed with WARNING
- ≥2 laws FAIL → STATUS: FAILED → return to STEP 4/5 with remediation

Mark step-6 `completed`.

---

## STEP 7: CHECKPOINT

Mark step-7 `in_progress`.

1. Update `config.yaml`:
   ```yaml
   sessions:
     research:
       raw_research:
         status: "complete"
         timestamp: "{ISO date}"
         blueprints_processed: {N}
         deep_output: "research/raw-deep/"
         fresh_output: "research/raw-fresh/"
   ```

2. **OUTPUT:**
```
✅ RAW RESEARCH COMPLETE
- Blueprints: {N} processed
- Deep dossiers: {N} × 4000w (mode-typed, depth-stratified, storytelling-tagged)
- Fresh dossiers: {N} × 4000w (novelty-scored, surprise-gated, vibe-baited)
- Distillation: {N} receipts generated
- NEXT: /ccf-research-deep {client_name} (analysts consume RAW dossiers)
```

Mark step-7 `completed`.

---

## 🔗 NEXT: `/ccf-research-deep {client_name}` then `/ccf-research-fresh {client_name}`
