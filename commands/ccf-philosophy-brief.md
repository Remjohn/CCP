---
name: ccf-philosophy-brief
description: Extract coach's depth-stratified philosophy from transcripts into coach_philosophy_brief.md
---

# /ccf-philosophy-brief {client_name}

// turbo-all

> **SKILLS_BASE:** `ccf-26/skills/ccf/`
> **SKILL:** `setup/philosophy-brief/SKILL.md`

**Objective:** Extract the coach's multi-transcript, depth-stratified philosophy — beliefs (L1/L2/L3), story inventory (T/V/R), contradiction map, and evolution agenda — producing `coach_philosophy_brief_v{N}.md`.

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify config.yaml and transcripts exist", status: "pending" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Philosophy Brief SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: INDOCTRINATE - State extraction commitments aloud", status: "pending" },
    { id: "step-4", description: "STEP 4: INGEST - Load transcripts + existing soul_values + previous brief", status: "pending" },
    { id: "step-5", description: "STEP 5: REASON - Execute 4-Law philosophy extraction", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write coach_philosophy_brief_v{N}.md", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Depth distribution + mode coverage + authenticity gate", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml + emit distillation receipt", status: "pending" }
  ]
});
```

**DO NOT PROCEED until you have called `write_todos` above.**

---

## 📋 Step Execution Protocol (MANDATORY)

> [!CAUTION]
> **You MUST call `write_todos` at EVERY step transition.**
> This is not optional. Skipping todo updates = workflow failure.

**For EACH step, follow this pattern:**

1. **START STEP:** Update todo status to `in_progress`
2. **EXECUTE:** Perform the step actions
3. **VALIDATE:** Verify outputs exist
4. **COMPLETE STEP:** Update todo status to `completed`

---

## STEP 1: PRE-FLIGHT

Mark step-1 `in_progress`.

**ACTIONS:**

| Check | Path | If Missing |
|-------|------|------------|
| 1 | `ccf-26/Production/{client_name}/config.yaml` | STOP → Run `/ccf-init {client_name}` first |
| 2 | `raw/transcripts/` (≥1 file) | STOP → "ERROR: No transcripts found" |
| 3 | `intelligence/soul/soul_values.json` | WARN → Will run in PURE BOOTSTRAP mode (no baseline) |
| 4 | `intelligence/philosophy/coach_philosophy_brief_v*.md` | If exists → MONTHLY UPDATE mode. If not → BOOTSTRAP or LAYERED |

**Determine operating mode:**
- **1 transcript:** BOOTSTRAP (provisional brief, relaxed thresholds)
- **2+ transcripts:** LAYERED (cross-referencing, full thresholds)
- **Previous brief exists + new transcript:** MONTHLY UPDATE (evolution tracking required)

Report: "Mode: {BOOTSTRAP|LAYERED|MONTHLY_UPDATE}, {N} transcripts available, {X} total words"

Mark step-1 `completed`.

---

## STEP 2: LOAD SKILL

Mark step-2 `in_progress`.

**ACTIONS:**

1. Read FULL: `ccf-26/skills/ccf/setup/philosophy-brief/SKILL.md`
2. Internalize:
   - The **4 Laws of Philosophy Distillation**
   - The **I-R-E-V-C Protocol** with law-governed extraction steps
   - The **operating mode thresholds** (BOOTSTRAP vs LAYERED vs MONTHLY UPDATE)
3. If `soul_values.json` exists, read it for baseline values/metaphors/vocabulary

> [!IMPORTANT]
> **CONSTRAINT:** You are the Philosophy Cartographer. You EXTRACT — you do NOT generate. Every belief, story, and contradiction must trace to a verbatim transcript moment.

Mark step-2 `completed`.

---

## STEP 3: INDOCTRINATE

Mark step-3 `in_progress`.

**State aloud before proceeding:**

"I am the Philosophy Cartographer. I will:
1. Extract beliefs at THREE depth layers — surface, mechanism, and collision
2. Build a story inventory tagged by emotional mode (T/V/R)
3. Map contradictions as philosophical depth, not errors
4. Verify every extraction traces to a specific transcript moment
5. Flag what the next monthly cycle should explore"

Mark step-3 `completed`.

---

## STEP 4: INGEST (I-R-E-V-C Phase I)

Mark step-4 `in_progress`.

**ACTIONS:**

1. Load ALL transcripts from `raw/transcripts/`
2. Load `soul_values.json` (baseline, if exists)
3. Load `content_themes.json` from `intelligence/themes/` (if exists)
4. Load previous `coach_philosophy_brief_v{N-1}.md` (if MONTHLY UPDATE mode)
5. Count total word count
6. Report: "Loaded {N} transcripts, {X} total words"

**Cross-transcript analysis (LAYERED/MONTHLY only):**
- Map each transcript by: date, topic focus, emotional intensity
- Identify beliefs across multiple transcripts → SIGNATURE
- Identify beliefs in single transcript → PERIPHERAL
- Identify beliefs present early but absent later → ABANDONED

> [!NOTE]
> **Context Window Guard:** If transcript word count exceeds 80,000 words, load the 3 longest + any new transcripts (for MONTHLY mode). Log exclusions.

Mark step-4 `completed`.

---

## STEP 5: REASON (I-R-E-V-C Phase R — 4-Law Extraction)

Mark step-5 `in_progress`.

**Execute ALL 4 Laws sequentially:**

### LAW 1 — DEPTH STRATIFICATION

Extract every belief and classify:
- **L1 (Surface):** Public, consistent, would appear on their website → "Would this appear on their LinkedIn?"
- **L2 (Mechanism):** WHY they believe it — personal experience behind the conviction
- **L3 (Collision):** Where the belief was tested, where two beliefs create tension, where values contradicted behavior

**Gate check:** BOOTSTRAP: L2 ≥ 20%, L3 ≥ 5% | LAYERED: L2 ≥ 30%, L3 ≥ 10%

### LAW 2 — STORY INVENTORY WITH MODE TAGS

Extract every story and tag:
- `mode`: TENSION / VULNERABILITY / RECOGNITION
- `depth_layer`: L1 / L2 / L3
- `transcript_source`: which transcript(s), with timestamp/quote
- `classification`: SIGNATURE (≥2 appearances) / PERIPHERAL (1 appearance)
- `evolution_notes`: how story changed across tellings (if applicable)

**Gate check:** BOOTSTRAP: ≥ 8 stories | LAYERED: ≥ 15 stories | All 3 modes must have ≥1 story

### LAW 3 — CONTRADICTION MAPPING

Extract:
1. **Value Tensions:** Two beliefs that conflict when applied simultaneously
2. **Story-Belief Mismatches:** A story that undermines a stated belief
3. **Evolution Artifacts:** Beliefs modified or abandoned across transcripts

**Gate check:** Total items ≥ 2. Zero contradictions = SHALLOW flag.

### LAW 4 — PHILOSOPHY AUTHENTICITY GATE

Run 4 checks:
1. **First-party verification:** Every item traces to transcript verbatim
2. **Depth distribution:** Meets mode thresholds
3. **Mode coverage:** T + V + R all represented in story inventory
4. **Evolution readiness:** Evolution Agenda section is populated

> [!CAUTION]
> **If any law gates fail after 2 re-extraction attempts:** Report which law failed and what's missing. Do NOT fabricate data to pass gates.

Mark step-5 `completed`.

---

## STEP 6: EMIT (I-R-E-V-C Phase E)

Mark step-6 `in_progress`.

**CREATE FILE:** `intelligence/philosophy/coach_philosophy_brief_v{N}.md`

Structure:
```
├── METADATA (coach, version, mode, date, transcript sources, depth distribution)
├── CORE BELIEFS (depth-stratified: L1 → L2 → L3)
├── STORY INVENTORY (mode-tagged, signature vs peripheral)
├── CONTRADICTION MAP (value tensions + story-belief mismatches + evolution artifacts)
├── VOICE DNA (recurring metaphors, emotional vocabulary, temperature by topic)
└── EVOLUTION AGENDA (gaps, beliefs in flux, stories needing deeper telling)
```

Mark step-6 `completed`.

---

## STEP 7: VALIDATE (I-R-E-V-C Phase V)

Mark step-7 `in_progress`.

| # | Gate | Requirement | If Fail |
|---|------|-------------|---------|
| 1 | Depth distribution | L2 ≥ threshold, L3 ≥ threshold | Re-extract from transcripts |
| 2 | Story count | ≥ 8 (BOOTSTRAP) or ≥ 15 (LAYERED) | Extract more stories |
| 3 | Mode coverage | All 3 modes (T/V/R) have ≥1 story | Flag missing mode |
| 4 | Contradictions | ≥ 2 items in contradiction map | Dig deeper for tensions |
| 5 | Provenance | Every item traces to verbatim quote | Remove untraceable items |
| 6 | Evolution agenda | Non-empty — next cycle has a mission | Add at least 3 exploration points |
| 7 | No AI artifacts | Zero "leverage", "optimize", "moreover" | Replace with coach vocabulary |

**CREATE FILE:** `intelligence/philosophy/H10_DISTILLATION_RECEIPT.md`

Mark step-7 `completed`.

---

## STEP 8: CHECKPOINT (I-R-E-V-C Phase C)

Mark step-8 `in_progress`.

1. Update `config.yaml`:
   ```yaml
   sessions:
     setup:
       philosophy_brief:
         status: "complete"
         version: "{N}"
         mode: "{BOOTSTRAP|LAYERED|MONTHLY_UPDATE}"
         timestamp: "{ISO date}"
         output: "intelligence/philosophy/coach_philosophy_brief_v{N}.md"
   ```

2. **OUTPUT:**
```
✅ PHILOSOPHY BRIEF COMPLETE
- Mode: {BOOTSTRAP|LAYERED|MONTHLY_UPDATE}
- Beliefs: L1:{N} L2:{N} L3:{N} (L2:{X}%, L3:{Y}%)
- Stories: {N} total (T:{N} V:{N} R:{N})
- Contradictions: {N}
- Files: coach_philosophy_brief_v{N}.md, H10_DISTILLATION_RECEIPT.md
- NEXT: /ccf-soul-extract {client_name}
```

Mark step-8 `completed`.

---

## 🔗 NEXT: `/ccf-soul-extract {client_name}` (H8 informed by H10)
