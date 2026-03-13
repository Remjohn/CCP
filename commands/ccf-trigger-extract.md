---
name: ccf-trigger-extract
description: "Genesis Pipeline — Runs full Emotional DNA extraction, Trigger Map build, and Voice DNA profiling for a new coach onboarding"
---

# /ccf-trigger-extract {client_name}

// turbo-all

> **SKILLS_BASE:** `ccf-26/skills/ccf/`
> **SKILLS:**
> - `setup/emotional-dna-extraction/SKILL.md`
> - `setup/trigger-map-builder/SKILL.md`
> - `setup/voice-dna-profiler/SKILL.md`
> **PHASE:** Genesis (runs once per coach, after `/ccf-soul-extract`)

**Objective:** Extract the coach's complete Emotional DNA profile, build their permanent trigger map, and construct the 3-layer Voice DNA SPR with Negative Space Object. This is the root system construction that all downstream content generation depends on.

> [!IMPORTANT]
> **MANDATE 8 DEPENDENCY:** This command MUST run AFTER `/ccf-soul-extract` (coach identity extraction) and BEFORE any prompt rebuild or weekly content generation. The Emotional DNA is the root system — building Voice DNA or content prompts without it produces a map of the river without the source.

---

## 🎯 STEP 0: INITIALIZE TODOS

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify soul extraction + transcript corpus", status: "pending" },
    { id: "step-2", description: "STEP 2: CORPUS AUDIT - Count words, validate 3000w threshold", status: "pending" },
    { id: "step-3", description: "STEP 3: LOAD SKILL 1 - Read Emotional DNA Extraction SKILL.md", status: "pending" },
    { id: "step-4", description: "STEP 4: GRANULARITY TRIAGE - Run Barrett framework tier assessment", status: "pending" },
    { id: "step-5", description: "STEP 5: EXTRACT EDNA - Run full 10-variable Emotional DNA extraction", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE EDNA - Cross-validate V1-V5 against V6 for coherence", status: "pending" },
    { id: "step-7", description: "STEP 7: LOAD SKILL 2 - Read Trigger Map Builder SKILL.md", status: "pending" },
    { id: "step-8", description: "STEP 8: BUILD TRIGGERS - Map permanent trigger architecture from EDNA + corpus", status: "pending" },
    { id: "step-9", description: "STEP 9: ASSESS PTG - Classify triggers by resolution status (Tedeschi & Calhoun)", status: "pending" },
    { id: "step-10", description: "STEP 10: VALIDATE TRIGGERS - Verify PTG safety, evidence provenance", status: "pending" },
    { id: "step-11", description: "STEP 11: LOAD SKILL 3 - Read Voice DNA Profiler SKILL.md", status: "pending" },
    { id: "step-12", description: "STEP 12: NEGATIVE SPACE - Build Negative Space Object (Mandate 4, runs FIRST)", status: "pending" },
    { id: "step-13", description: "STEP 13: LAYER 1 - Run 60-variable stylometric analysis", status: "pending" },
    { id: "step-14", description: "STEP 14: LAYER 2 - Derive emotional path mechanics from EDNA", status: "pending" },
    { id: "step-15", description: "STEP 15: LAYER 3 - Extract leadership elevation peaks from corpus", status: "pending" },
    { id: "step-16", description: "STEP 16: VALIDATE VDNA - LR score check, root derivation audit", status: "pending" },
    { id: "step-16b", description: "STEP 16b: GENERATIVE GRAMMAR - Encode executable construction rules", status: "pending" },
    { id: "step-17", description: "STEP 17: CHECKPOINT - Final status, pipeline readiness check", status: "pending" },
    { id: "step-18", description: "STEP 18: CALIBRATE - Verify unverified triggers via coach-elicitation", status: "pending" }
  ]
});
```

---

## STEP 1: PRE-FLIGHT

Mark step-1 `in_progress`.

| Check | Path | If Missing |
|-------|------|------------|
| 1 | `intelligence_library/coach_soul.json` with `soul_extraction_complete: true` | STOP → Run `/ccf-soul-extract` first |
| 2 | `raw/transcripts/` directory with interview/podcast transcripts | STOP → Collect coach transcripts first |
| 3 | `intelligence_library/emotional_dna.json` template exists | Auto-create from template if missing |
| 4 | `intelligence_library/trigger_map.json` template exists | Auto-create from template if missing |
| 5 | Coach sacred audio extracted? (`sacred_audio.extraction_timestamp` not null) | WARN → Proceed without acoustic data (V9 will be null) |

Mark step-1 `completed`.

---

## STEP 2: CORPUS AUDIT

Mark step-2 `in_progress`.

Count total words across all files in `raw/transcripts/`:
- Sum word counts per file
- Report total word count

| Threshold | Action |
|-----------|--------|
| ≥ 3,000 words | ✅ Proceed with full extraction |
| 1,500-2,999 words | ⚠️ WARN — Extraction will be partial. Report gap. Suggest additional sources. |
| < 1,500 words | 🛑 STOP — Insufficient corpus. Cannot extract with confidence. |

**If below threshold, suggest sources:**
```
⚠️ CORPUS GAP — Need {3000 - current} more words
Suggested sources:
1. YouTube interview transcripts (use Whisper or YouTube auto-captions)
2. Podcast guest appearances (download + transcribe)
3. Long-form social media posts (LinkedIn articles, blog posts)
4. Additional Sacred Audio voice notes (deeper interview sessions)
```

Mark step-2 `completed`.

---

## STEP 3: LOAD SKILL 1 — Emotional DNA Extraction

Mark step-3 `in_progress`.

Read FULL: `ccf-26/skills/ccf/setup/emotional-dna-extraction/SKILL.md`

**Internalize:**
- 5 scientific frameworks (Scherer CPM, Haidt MFT, Barrett, Pennebaker LIWC-22, Computational Stylometry)
- 4 pre-generation constraints (provenance, triage-first, cross-validation, no fabrication)
- 5-phase extraction protocol

Mark step-3 `completed`.

---

## STEP 4: GRANULARITY TRIAGE (Constraint B — runs BEFORE full extraction)

Mark step-4 `in_progress`.

Execute Barrett Constructionism granularity assessment:
1. Scan full corpus for distinct emotional terms
2. Count unique emotional descriptors (excluding context words)
3. Classify:

| Tier | Distinct Terms | Extraction Depth |
|------|---------------|-----------------|
| HIGH | ≥ 25 | Full V1-V10 |
| MEDIUM | 12-24 | V1-V8, V9-V10 partial |
| LOW | < 12 | V1, V3, V5, V6 only |

Record tier in `emotional_dna.json → extraction_status.triage_tier`

Mark step-4 `completed`.

---

## STEP 5: EXTRACT EMOTIONAL DNA

Mark step-5 `in_progress`.

Execute the SKILL.md extraction protocol phases 2-5:
- Phase 2: Appraisal variables V1-V5 (Scherer/Lazarus)
- Phase 3: Moral Foundations V6 (Haidt MFQ-2)
- Phase 4: Linguistic Signature V8 (Pennebaker LIWC-22)
- Phase 5: Emotional Path Mechanics (cross-reference V1-V5 with corpus)

For each variable:
- Cite specific corpus passage (Constraint A)
- Record confidence level
- Respect granularity tier depth limits (Constraint B)

**WRITE:** `intelligence_library/emotional_dna.json`

Mark step-5 `completed`.

---

## STEP 6: VALIDATE EMOTIONAL DNA

Mark step-6 `in_progress`.

Execute Constraint C — Appraisal-MFT Cross-Validation:

| Check | Coherence Rule | If Incoherent |
|-------|---------------|---------------|
| V5 (agency) vs V6 (MFT) | High Care/Harm + institutional attribution → should show low V1 threshold for institutional violations | Flag specific variable for re-examination |
| V3 (coping) vs V2 (sequence) | Action-oriented + mechanism_first should co-occur | Flag if contradictory |
| V4 (norm threshold) vs V6 (MFT) | High primary foundation weight → lower norm threshold in that domain | Flag if disconnected |

Validate all evidence passages exist and are correctly cited.
Calculate `extraction_status.confidence` = populated vars / total vars (adjusted by tier).

Mark step-6 `completed`.

---

## STEP 7: LOAD SKILL 2 — Trigger Map Builder

Mark step-7 `in_progress`.

Read FULL: `ccf-26/skills/ccf/setup/trigger-map-builder/SKILL.md`

**Internalize:**
- 5 scientific frameworks (Conway AKB, Tedeschi PTG, McAdams, Nader, Haidt)
- 4 pre-generation constraints (EDNA dependency, PTG protection, evidence-first, resolution signal)
- 6-phase extraction protocol

Mark step-7 `completed`.

---

## STEP 8: BUILD TRIGGERS

Mark step-8 `in_progress`.

Execute Trigger Map Builder phases 1-2:
- Phase 1: Trigger Identification (using V4 + V6 from EDNA, searching corpus for activation passages)
- Phase 2: Origin Classification (classify each trigger by Conway AKB level)

For each trigger:
- Assign `trigger_id` (trig_001, trig_002, etc.)
- Map to moral foundation
- Classify AKB level (ESK → highest value)
- Record activation keywords and mechanisms

Mark step-8 `completed`.

---

## STEP 9: ASSESS PTG STATUS

Mark step-9 `in_progress`.

Execute Trigger Map Builder phases 3-5:
- Phase 3: PTG Assessment (Tedeschi & Calhoun)
- Phase 4: Narrative Identity (McAdams)
- Phase 5: Reconsolidation Sensitivity (Nader)
- Phase 6: Archetype Mapping (Stage 5)

> [!CAUTION]
> **SAFETY GATE:** Any trigger classified `raw_unresolved` is IMMEDIATELY excluded from the activation pipeline. Log the exclusion. This is non-negotiable.

Mark step-9 `completed`.

---

## STEP 10: VALIDATE TRIGGERS

Mark step-10 `in_progress`.

| Check | Requirement | If Fail |
|-------|------------|---------|
| Evidence provenance | Every trigger has ≥ 1 corpus passage | Remove trigger from primary array → move to candidates |
| MFT coherence | Trigger foundation matches V6 profile | Re-examine foundation assignment |
| PTG safety | No `raw_unresolved` in activation pipeline | Remove and flag |
| Minimum viable | ≥ 2 `resolved_dual_layer` triggers | WARN if < 2 — content activation will be limited |
| Archetype eligibility | At least 1 trigger-archetype pair where coach TTT ceiling meets minimum | WARN if none eligible |

**WRITE:** `intelligence_library/trigger_map.json`

Mark step-10 `completed`.

---

## STEP 11: LOAD SKILL 3 — Voice DNA Profiler

Mark step-11 `in_progress`.

Read FULL: `ccf-26/skills/ccf/setup/voice-dna-profiler/SKILL.md`

**Internalize:**
- 5 scientific frameworks (Computational Stylometry, Schiffrin, Kensinger, Mandate 5, Normative Voice Profile)
- 4 pre-generation constraints (root-down, River Test, peak not average, negative space first)
- Phase 0 + Phase 1-3 extraction protocol

Mark step-11 `completed`.

---

## STEP 12: NEGATIVE SPACE OBJECT (Mandate 4 — runs FIRST)

Mark step-12 `in_progress`.

Execute Voice DNA Profiler Phase 0:
- Forbidden tonal registers (absent from corpus)
- Forbidden vocabulary classes (absent from natural language)
- Forbidden rhetorical moves (never used)
- Identity edge markers (from trigger_map raw_unresolved + low-weight MFT foundations)

**UPDATE:** `coach_soul.json → negative_space`

Mark step-12 `completed`.

---

## STEP 13: LAYER 1 — Construction Mechanics

Mark step-13 `in_progress`.

Execute Voice DNA Profiler Phase 1:
- Run 60-variable stylometric analysis (5 clusters × 12 vars)
- Derive sentence skeletons, discourse marker positions, rhythm patterns, metaphor deployment
- Calculate Stylometric LR score (target ≥ 0.85)
- Apply River Test to every pattern (trace to emotional root)

Mark step-13 `completed`.

---

## STEP 14: LAYER 2 — Emotional Path Mechanics

Mark step-14 `in_progress`.

Execute Voice DNA Profiler Phase 2:
- Derive conversion mechanism from `emotional_dna.json` V2
- Measure emotion residency time across corpus
- Identify escalation triggers and TTT transition markers
- Cross-reference with trigger_map activation passages

Mark step-14 `completed`.

---

## STEP 15: LAYER 3 — Leadership Elevation

Mark step-15 `in_progress`.

Execute Voice DNA Profiler Phase 3:
- Identify 12 Attractive Leader Traits present in corpus
- For present traits, find TOP 5% passages (peak, not average)
- Extract peak expression construction patterns
- Set primary_trait and secondary_trait
- Map trait_format_affinity

Mark step-15 `completed`.

---

## STEP 16: VALIDATE VOICE DNA

Mark step-16 `in_progress`.

| Check | Requirement | If Fail |
|-------|------------|---------|
| LR Score | ≥ 0.85 | WARN — extraction may not be forensic-grade |
| Root derivation | ≥ 70% of Layer 1 patterns have root explanation | Flag unexplained patterns |
| Mandate 5 separation | All 3 layers populated as SEPARATE objects | Restructure if conflated |
| Peak vs average | Layer 3 uses top 5%, not average | Re-extract from peak passages |
| Negative Space first | Negative Space was built before Layer 1 | Re-run in correct order |

**UPDATE:** `coach_soul.json → voice_dna` (all 3 layers + negative_space)

Mark step-16 `completed`.

---

## STEP 16b: GENERATIVE GRAMMAR ENCODING (Item 17)

Mark step-16b `in_progress`.

Explicitly trigger Phase 4 of the Voice DNA Profiler:
1. Extract Sentence Skeletons.
2. Formulate Discourse Marker Rules as conditional logic.
3. Establish length/rhythm constraints.
4. Apply Executability Test (Can a downstream agent execute this without aesthetic interpretation?)

**UPDATE:** `coach_soul.json → voice_dna.layer_1_construction_mechanics`

Mark step-16b `completed`.

---

## STEP 17: CHECKPOINT

Mark step-17 `in_progress`.

Update `config.yaml`:
```yaml
sessions:
  setup:
    trigger_extraction:
      status: "complete"
      timestamp: "{ISO date}"
      emotional_dna_confidence: {N}
      triggers_mapped: {N}
      ptg_resolved: {N}
      ptg_active: {N}
      ptg_raw: {N}
      voice_dna_lr_score: {N}
      negative_space_items: {N}
      pipeline_ready: true
```

Update `coach_soul.json`:
```json
{
    "extraction_pipeline_status": {
        "soul_extraction_complete": true,
        "emotional_dna_complete": true,
        "trigger_map_complete": true,
        "voice_dna_3layer_complete": true,
        "negative_space_complete": true,
        "pipeline_ready": true,
        "last_updated": "{ISO date}"
    }
}
```

**FINAL OUTPUT:**
```
✅ TRIGGER-FIRST EXTRACTION COMPLETE ({client_name})

🧬 Emotional DNA:
- Granularity Tier: {HIGH/MEDIUM/LOW}
- Variables Populated: {N}/10
- Confidence: {N}%
- Corpus: {N} words across {N} transcripts

🗺️ Trigger Map:
- Triggers Mapped: {N}
- PTG Resolved (dual-layer): {N} ✅
- PTG Active: {N} ⚠️
- PTG Raw (excluded): {N} 🛑
- Archetype-Eligible Pairs: {N}

🔬 Voice DNA (3-Layer SPR):
- Layer 1 (Construction): {N} patterns derived
- Layer 2 (Emotional Path): Conversion = {mechanism}
- Layer 3 (Leadership): Primary = {trait}, Secondary = {trait}
- Stylometric LR: {N}
- Root Derivation Rate: {N}%

🚫 Negative Space: {N} items (consulted before positive DNA)

📋 Pipeline Ready: ⚠️ Pending Calibration. Use /ccf-elicit trigger-calibration

💡 NEXT STEPS:
1. Run `/ccf-elicit trigger-calibration` to verify triggers mapped today.
2. Begin weekly cycle: `/ccf-weekly {client_name}`
```

Mark step-17 `completed`.

---

## STEP 18: TRIGGER CALIBRATION (Item 04)

Mark step-18 `in_progress`.

This step utilizes the `coach-elicitation` harness in **Calibration Mode**.
1. Identify all `unverified` triggers in `trigger_map.json`.
2. Send precision activation events to the coach.
3. Wait for voice note responses.
4. **Agentic Check:** Responses must pass the LIWC-22 Authenticity Gate (Score ≥0.6) to become `verified`.

*(Note: Command pauses here until coach responds)*

Mark step-18 `completed`.

---

## 🔗 NEXT: `/ccf-elicit trigger-calibration`
