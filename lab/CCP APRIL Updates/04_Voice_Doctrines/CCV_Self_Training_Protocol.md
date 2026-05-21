# CCV Self-Training Protocol — Receipt-Based Dataset Generation

> **Session:** 2026-04-15 | **Status:** VALIDATED — This is the production training methodology
>
> **Key Insight:** The pipeline already produces receipts at every step. Every successful run where all gates return PASS is a supervised training example. Every run where a gate returns FAIL and the Critic corrects it is a DPO training pair.

---

## The Core Realization

The system doesn't need a separate "dataset creation phase." **Running the pipeline IS creating the dataset.** The validators already tag every output as PASS or FAIL. The receipts already contain the full reasoning trace. The CCV axis labels already exist in `field_3_context` of every compilation.

All that's needed is:
1. A dataset schema that captures the receipt structure
2. A filter that keeps only verified examples
3. A training pipeline that consumes the filtered traces

---

## What the Pipeline Already Produces

### Per-Step Receipts (Already Exist)

| Pipeline Step | Receipt Produced | Contains |
|---|---|---|
| **CRAL Research** (M1-M7) | `cral_finding_index.json` | 7 moment findings with use_at addresses, verifiability citations, human evidence |
| **Strategy Brief** | `strategy_brief.json` | `selected_arc`, `ideal_pacing_template`, `arc_diagnosis.confidence_score` |
| **Quote Manifest** (Witness arc) | `Quote_Manifest_Enriched.md` | All candidate quotes for W1-W5 with V3 Tags: `PACING_CLASS`, `POLARITY`, `THEMATIC_FIT` |
| **Composition** | `premise_analysis.json` + `COMPOSITION_LOG.md` | Script sequence with per-cluster reasoning, template match scores, bookend logic, viral scores |
| **Beat Cluster** | `beat_cluster.json` | EDL with per-beat `arc_stage`, `duration_sec`, `visual_prompt_ref`, `narration_text` |
| **Scene Builder** | Scene decisions per beat | Container → Component → Template → Effects selection with LAW_1-4 validation |
| **Manifest Assembly** | `receipt_MANIFEST_ASSEMBLY` | Frame timing, transition assignments, asset resolution, Gate E validation |
| **Legitimacy Gate** | `receipt_SCENE_LEGITIMACY_GATE` | APPROVE / BLOCK per beat with violation codes |
| **SG Gates** (v1.2) | SG-01 through SG-08 | Binary PASS/FAIL per gate with specific failure reason |

### Validation Status (Already Exists)

| Validator | What It Tags | Dataset Signal |
|---|---|---|
| **SG-01** (Distillation Funnel Gate) | Stakes derived from authenticated SoC? | PASS = verified positive. FAIL = pre-correction negative |
| **SG-02** (Contrastive Anchor) | Mechanism transferable to stranger? | PASS/FAIL → DPO pair if corrected |
| **SG-03** (MCDA Critic) | Turn is a single identifiable frame? | PASS/FAIL → binary quality signal |
| **SG-04** (Authentication Certificate) | Result contains falsifiable data point? | PASS/FAIL → hard constraint |
| **SG-05** (Context Premise + Tribal Terms) | Implication uses tribal language? | PASS/FAIL → voice fidelity signal |
| **SG-06** (CRAL Router) | M2_BELIEVABLE deployed in Stakes? | PASS/FAIL → CRAL integration quality |
| **SG-07** (CRAL Router) | M7_RELATABLE passes tribal recognition? | PASS/FAIL → audience resonance signal |
| **SG-08** (Builder Engine 3.5) | No unresolved CRAL/SoC conflicts? | PASS/FAIL → consistency signal |
| **Legitimacy Runner** | Full compilation passes all gates? | APPROVE = verified training example |
| **CBAR Gate Pack** | Scene builder constraints met? | APPROVE = verified CMF training example |

---

## The Dataset Schema

### For Script Generation Training (Reasoning + Execution)

```json
{
  "trace_id": "UUID",
  "timestamp": "ISO_TIMESTAMP",
  "coach_id": "string",
  "project_id": "string",
  
  "ccv_axes": {
    "archetype": "achievement_story",
    "archetype_family": "story_arc",
    "mood_state": "processing",
    "arousal_direction": "raises",
    "regulatory_frame": "promotion",
    "audience_cohort": "developing",
    "intensity": 0.8,
    "sdt_need_primary": "competence"
  },
  
  "inputs": {
    "dep_eng_010_soc_batch": "hash_ref",
    "dep_eng_003_emotional_dna": "hash_ref",
    "dep_eng_004_negative_space": "hash_ref",
    "dep_eng_006_context_premise": "hash_ref",
    "dep_eng_021_cral_finding_index": "hash_ref",
    "dep_eng_016_psych_routing": "hash_ref"
  },
  
  "reasoning_trace": {
    "causal_construction": {
      "phase_1_stakes": {
        "cognitive_function": "audience occupies emotional reality of failure cost",
        "dep_source": "DEP-ENG-010",
        "cral_source": ["M2_BELIEVABLE", "M3_UNDENIABLE"],
        "structural_law": "Name the specific cost of failure before any result",
        "sg_gate": "SG-06"
      },
      "phase_2_mechanism": { "..." : "..." },
      "phase_3_turn": { "..." : "..." },
      "phase_4_result": { "..." : "..." },
      "phase_5_implication": { "..." : "..." }
    },
    "anti_draft_check": {
      "level_1_centroid_distance": 0.87,
      "level_2_mood_archetype_check": "PASS",
      "level_3_coach_specific_check": "PASS"
    }
  },
  
  "output": {
    "generated_script": "The full generated text...",
    "word_count": 165,
    "structure": "5-phase Achievement Story"
  },
  
  "validation": {
    "sg_01": "PASS",
    "sg_02": "PASS",
    "sg_03": "PASS",
    "sg_04": "PASS",
    "sg_05": "PASS",
    "sg_06": "PASS",
    "sg_07": "PASS",
    "sg_08": "PASS",
    "legitimacy_verdict": "APPROVE",
    "deployment_status": "COMPLETE"
  },
  
  "dataset_label": "positive",
  "dpo_pair_id": null
}
```

### For CMF Agent Training (Visual/Composition Decisions)

```json
{
  "trace_id": "UUID",
  "skill_id": "SKILL-VID-XXX or SKILL-CMF-XXX",
  "skill_family": "motion | composer | eroll | editor",
  
  "input_context": {
    "beat_index": 0,
    "arc_stage": "HOOK",
    "beat_text": "...",
    "vcp": "...",
    "available_assets": ["A_ROLL", "B_ROLL", "TEXT"],
    "previous_beat": null
  },
  
  "reasoning_trace": {
    "step_0_interpretation": "VCP portrays defeat. Frozen pose: deep crouch. Weather: RAIN",
    "step_1_character_anchor": "Noir translation: luminous highlights, charcoal dress",
    "step_2_elemental_selection": "RAIN — sadness + struggle + cleansing",
    "step_3_composition": "Plane 0: #050505. Plane 1: 'HEAVY'. Plane 2: crouch. Plane 3: vertical sheets",
    "step_4_synthesis": "168-word T2I prompt combining all elements"
  },
  
  "output": {
    "t2i_prompt": "Full generated prompt...",
    "i2i_prompt": "Full I2I instruction...",
    "i2v_prompt": "Full I2V instruction..."
  },
  
  "validation": {
    "character_anchor_used": true,
    "silhouette_noir_style": true,
    "weather_motivated": true,
    "palette_compliant": true,
    "motion_verbs_valid": true,
    "word_count_160_180": true,
    "first_frame_keeps_pose": true,
    "single_word_only": true,
    "prompt_original": true,
    "all_9_gates_pass": true
  },
  
  "dataset_label": "positive"
}
```

---

## The Self-Training Loop

```
┌──────────────────────────────────────────────────────────────────┐
│  STEP 1: RUN THE PIPELINE                                       │
│  Use current Skills + big model (Gemma-4-31B)                    │
│  Produce real content for real coaches                            │
│  Every step automatically generates receipts                     │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│  STEP 2: COLLECT RECEIPTS                                        │
│  Validators tag every output as PASS/FAIL                        │
│  assembly_report.json → COMPLETE / REJECTED                      │
│  SG-01 through SG-08 → binary verdicts                           │
│  COMPOSITION_LOG.md → deliberation traces                        │
│  Legitimacy Runner → APPROVE / BLOCK                             │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│  STEP 3: BUILD DATASET                                           │
│  Schema from existing receipt structure (schemas/ already exist)  │
│  Filter: deployment_status: COMPLETE + all SG gates PASS         │
│  → Positive examples (supervised)                                │
│  Filter: REJECTED + critic correction applied                    │
│  → DPO pairs (pre-correction = negative, post = positive)       │
│  Add CCV axis labels from field_3_context                        │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│  STEP 4: TRAIN                                                   │
│  Qwen-3.5 + QLoRA on filtered, axis-labeled traces               │
│  Voice DNA LoRA (Syntax + Soul layers)                           │
│  Archetype-Family LoRAs (Story-Arc, Confrontation, etc.)         │
│  CMF Agent LoRAs (Motion, Composer, Editor)                      │
│  DPO alignment using REJECTED/corrected pairs                    │
└────────────────────┬─────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│  STEP 5: DEPLOY                                                  │
│  Lean prompts (~500 tokens) + LoRA weights + Activation Steering │
│  Validators STILL RUN (they don't go away)                       │
│  Failed outputs become new training data (continuous learning)   │
│  The system improves with every production cycle                 │
└──────────────────────────────────────────────────────────────────┘
```

---

## Three Prerequisites (All Addressed)

| Prerequisite | Status | How |
|---|---|---|
| **Voice DNA trained into LoRA** | Architecture defined | QLoRA on Qwen-3.5 using FR2-FR3 extraction traces. Syntax + Soul layers. Style handled by Activation Steering. |
| **Activation Steering working** | Architecture defined | RISER framework. Style modulation per mood state. Archetype-family calibration vectors from 2-3 peak-expression samples per family. |
| **Validators producing structured receipts** | **ALREADY BUILT** | SG-01 through SG-08, legitimacy_runner, CBAR gate packs, LAW_1 through LAW_4 — all produce machine-readable PASS/FAIL signals. |

---

## Why This Works

The validators are the automatic quality filter. No human annotators are needed reviewing 500 examples — the SG gates, legitimacy_runner, and CBAR gates already do that at production time.

If `deployment_status: COMPLETE` and all 8 SG gates returned PASS, that's a verified training example. Period.

If a gate returned FAIL and the Critic Subagent corrected the output, that's a DPO pair — the pre-correction output is the negative example, the post-correction output is the positive example.

**The system literally trains itself by running.** Every production cycle generates more training data. The validators are the labeling function. The receipts are the dataset. Just run it enough times to accumulate sufficient traces, then serialize them into training format.

---

## Minimum Viable Dataset Targets

| Training Target | Minimum Examples | Source |
|---|---|---|
| **Script Generation LoRA** | 300-500 verified compilations | Run the pipeline on real content with big model |
| **Voice DNA LoRA** (per coach) | 50-100 peak-expression scripts | FR2-FR3 extraction + curator selection |
| **Archetype-Family LoRA** (per family) | 100-200 per family | Pipeline traces filtered by archetype family |
| **CMF Motion LoRA** | 200-300 scene decisions | GMG Expert runs with quality gate PASS |
| **CMF Composer LoRA** | 150-200 composition traces | Witness/Confrontation/etc. composer runs |
| **DPO Negative Examples** | ~20% of total (auto-generated) | All REJECTED/corrected outputs from pipeline |

At 36 scripts/week, with ~6 CMF runs per script, **4-6 weeks of production running generates enough traces to train the first LoRAs.** The validators ensure quality. The receipts ensure structure. The CCV axes ensure diversity.

---

## Next Actions

1. **Instrument receipt collection** — Ensure every pipeline step writes its receipt to a standardized location with the dataset schema fields
2. **Add CCV axis labels** — Ensure `field_3_context` values propagate to every receipt
3. **Build the filter script** — Pull all COMPLETE + all-PASS examples, separate DPO pairs
4. **Start running** — Every production run is now dual-purpose: content delivery + training data generation
5. **Train iteratively** — First LoRA after 300 examples. Retrain monthly as dataset grows.
