---
name: ccf-soul-extract
description: Extract coach's authentic voice DNA from transcripts into soul_values.json
---

# /ccf-soul-extract {client_name}

// turbo-all

> **SKILLS_BASE:** `ccf-26/skills/ccf/`
> **SKILL:** `setup/client-soul-extraction/SKILL.md`

**Objective:** Extract the coach's psychological and philosophical DNA from transcripts, producing `soul_values.json` and `voice_blueprint.md`.

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify config.yaml and transcripts exist", status: "pending" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Client Soul Extraction SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: INGEST - Load transcripts and business materials", status: "pending" },
    { id: "step-4", description: "STEP 4: REASON - Execute Soul Cartographer analysis", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write soul_values.json and voice_blueprint.md", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Schema check + voice fidelity gates", status: "pending" },
    { id: "step-7", description: "STEP 7: H10/H8 DISTILLATION GATE - Run philosophy-distiller", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "pending" }
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

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify config.yaml and transcripts exist", status: "in_progress" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Client Soul Extraction SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: INGEST - Load transcripts and business materials", status: "pending" },
    { id: "step-4", description: "STEP 4: REASON - Execute Soul Cartographer analysis", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write soul_values.json and voice_blueprint.md", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Schema check + voice fidelity gates", status: "pending" },
    { id: "step-7", description: "STEP 7: H10/H8 DISTILLATION GATE - Run philosophy-distiller", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "pending" }
  ]
});
```

**ACTIONS:**

| Check | Path | If Missing |
|-------|------|------------|
| 1 | `ccf-26/Production/{client_name}/config.yaml` | STOP → Run `/ccf-init {client_name}` first |
| 2 | `ccf-26/Production/{client_name}/raw/transcripts/` (≥1 file) | STOP → "ERROR: No transcripts found" |
| 3 | `config.yaml → sessions.setup.init.status == "complete"` | STOP → Run `/ccf-init {client_name}` first |

> [!IMPORTANT]
> **Minimum transcript requirement:** ≥20,000 words total across all transcript files. Below this threshold, voice extraction quality degrades significantly. WARN operator if under threshold but allow to proceed.

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify config.yaml and transcripts exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Client Soul Extraction SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: INGEST - Load transcripts and business materials", status: "pending" },
    { id: "step-4", description: "STEP 4: REASON - Execute Soul Cartographer analysis", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write soul_values.json and voice_blueprint.md", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Schema check + voice fidelity gates", status: "pending" },
    { id: "step-7", description: "STEP 7: H10/H8 DISTILLATION GATE - Run philosophy-distiller", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "pending" }
  ]
});
```

---

## STEP 2: LOAD SKILL

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify config.yaml and transcripts exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Client Soul Extraction SKILL.md", status: "in_progress" },
    { id: "step-3", description: "STEP 3: INGEST - Load transcripts and business materials", status: "pending" },
    { id: "step-4", description: "STEP 4: REASON - Execute Soul Cartographer analysis", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write soul_values.json and voice_blueprint.md", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Schema check + voice fidelity gates", status: "pending" },
    { id: "step-7", description: "STEP 7: H10/H8 DISTILLATION GATE - Run philosophy-distiller", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "pending" }
  ]
});
```

**ACTIONS:**

1. Read the full SKILL.md file at: `ccf-26/skills/ccf/setup/client-soul-extraction/SKILL.md`
2. **Internalize** all instructions from the skill — this is your operating manual for this session
3. Pay special attention to:
   - The **Enhanced Analytical Framework** (sections A-E)
   - The **Quality Assurance Protocol**
   - The **I-R-E-V-C Session Protocol** at the end

> [!CAUTION]
> **CONSTRAINT:** You are the Soul Cartographer. Your ONLY job is to extract what ALREADY EXISTS in the transcripts. You must NOT invent voice patterns, values, or metaphors. Every element must be verifiable against the source transcripts.

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify config.yaml and transcripts exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Client Soul Extraction SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load transcripts and business materials", status: "pending" },
    { id: "step-4", description: "STEP 4: REASON - Execute Soul Cartographer analysis", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write soul_values.json and voice_blueprint.md", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Schema check + voice fidelity gates", status: "pending" },
    { id: "step-7", description: "STEP 7: H10/H8 DISTILLATION GATE - Run philosophy-distiller", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "pending" }
  ]
});
```

---

## STEP 3: INGEST (I-R-E-V-C Phase I)

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify config.yaml and transcripts exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Client Soul Extraction SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load transcripts and business materials", status: "in_progress" },
    { id: "step-4", description: "STEP 4: REASON - Execute Soul Cartographer analysis", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write soul_values.json and voice_blueprint.md", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Schema check + voice fidelity gates", status: "pending" },
    { id: "step-7", description: "STEP 7: H10/H8 DISTILLATION GATE - Run philosophy-distiller", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "pending" }
  ]
});
```

**ACTIONS:**

1. Read `config.yaml` for all input paths
2. Load ALL transcript files from `raw/transcripts/`
3. Load business materials from `raw/business/` (if available)
4. Count total word count across all transcripts
5. Report: "Loaded {N} transcripts, {X} total words, {Y} business documents"

> [!NOTE]
> **Context Window Guard:** If total transcript word count exceeds 80,000 words, load only the 3 longest transcripts. Log which transcripts were excluded and why.

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify config.yaml and transcripts exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Client Soul Extraction SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load transcripts and business materials", status: "completed" },
    { id: "step-4", description: "STEP 4: REASON - Execute Soul Cartographer analysis", status: "pending" },
    { id: "step-5", description: "STEP 5: EMIT - Write soul_values.json and voice_blueprint.md", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Schema check + voice fidelity gates", status: "pending" },
    { id: "step-7", description: "STEP 7: H10/H8 DISTILLATION GATE - Run philosophy-distiller", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "pending" }
  ]
});
```

---

## STEP 4: REASON (I-R-E-V-C Phase R)

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify config.yaml and transcripts exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Client Soul Extraction SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load transcripts and business materials", status: "completed" },
    { id: "step-4", description: "STEP 4: REASON - Execute Soul Cartographer analysis", status: "in_progress" },
    { id: "step-5", description: "STEP 5: EMIT - Write soul_values.json and voice_blueprint.md", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Schema check + voice fidelity gates", status: "pending" },
    { id: "step-7", description: "STEP 7: H10/H8 DISTILLATION GATE - Run philosophy-distiller", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "pending" }
  ]
});
```

**ACTIONS — Execute the SKILL.md Soul Cartographer analysis protocol:**

**A. Core Values Extraction (4-6 values):**
- Scan for "I believe", "What's important", "The key is always"
- Verify each value appears ≥2 times across different transcripts
- Each value must have specific context, NOT generic industry wisdom

**B. Internal Temperature Mapping (4-5 sub-topics):**
- Map emotional reactions across different topic areas
- Use exact phrasing from transcripts to describe each temperature

**C. Unique Metaphors & Language Patterns (≥3):**
- Extract recurring analogies and visual metaphors
- Must be SPECIFIC to this coach, not generic

**D. Signature Emotional Vocabulary (≥6 words):**
- Document the coach's specific word choices for emotions
- Note: "excited" vs "thrilled", "concerned" vs "worried"

**E. Voice Blueprint (EXACTLY 200 words):**
- Capture: pacing, filler words, sentence structure, transitions, emphasis patterns
- Must enable downstream agents to replicate the voice

**F. TTT Baseline Calculation:**
- Determine the coach's natural emotional gravity center (TTT-01 to TTT-09)
- Based on their default speaking intensity across all transcripts

> [!CAUTION]
> **EXTRACTION RULE:** Every value, metaphor, vocabulary item, and pattern must be VERIFIABLE against the source transcripts. If you can't point to where it appears, don't include it.

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify config.yaml and transcripts exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Client Soul Extraction SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load transcripts and business materials", status: "completed" },
    { id: "step-4", description: "STEP 4: REASON - Execute Soul Cartographer analysis", status: "completed" },
    { id: "step-5", description: "STEP 5: EMIT - Write soul_values.json and voice_blueprint.md", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Schema check + voice fidelity gates", status: "pending" },
    { id: "step-7", description: "STEP 7: H10/H8 DISTILLATION GATE - Run philosophy-distiller", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "pending" }
  ]
});
```

---

## STEP 5: EMIT (I-R-E-V-C Phase E)

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify config.yaml and transcripts exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Client Soul Extraction SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load transcripts and business materials", status: "completed" },
    { id: "step-4", description: "STEP 4: REASON - Execute Soul Cartographer analysis", status: "completed" },
    { id: "step-5", description: "STEP 5: EMIT - Write soul_values.json and voice_blueprint.md", status: "in_progress" },
    { id: "step-6", description: "STEP 6: VALIDATE - Schema check + voice fidelity gates", status: "pending" },
    { id: "step-7", description: "STEP 7: H10/H8 DISTILLATION GATE - Run philosophy-distiller", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "pending" }
  ]
});
```

**CREATE FILE 1:** `intelligence/soul/soul_values.json`

```json
{
  "Conscious_Soul_Values": {
    "content_theme": "Core Identity (All-Theme Baseline)",
    "core_values": [
      "Value 1: [description with transcript context]",
      "Value 2: [description with transcript context]",
      "Value 3: [description with transcript context]",
      "Value 4: [description with transcript context]"
    ],
    "internal_temperature": {
      "sub_topic_1": "[emotional stance with transcript evidence]",
      "sub_topic_2": "[emotional stance with transcript evidence]",
      "sub_topic_3": "[emotional stance with transcript evidence]",
      "sub_topic_4": "[emotional stance with transcript evidence]"
    },
    "unique_metaphors": [
      "Metaphor 1: [how they use it, with transcript example]",
      "Metaphor 2: [how they use it, with transcript example]",
      "Metaphor 3: [how they use it, with transcript example]"
    ],
    "emotional_vocabulary": ["word1", "word2", "word3", "word4", "word5", "word6"],
    "voice_blueprint": "[EXACTLY 200 words — pacing, fillers, sentence structure, transitions, emphasis]",
    "signature_perspective": "[1-2 sentences, first person, what makes them unique]",
    "ttt_baseline": {
      "gravity_center": "TTT-XX",
      "natural_range": "TTT-XX to TTT-XX",
      "reasoning": "[Why this is their natural center based on transcript evidence]"
    },
    "speech_patterns": {
      "filler_words": ["you know", "like I said"],
      "avg_sentence_length": 14,
      "profanity_level": 2,
      "pacing": { "words_per_minute": 150, "pause_frequency": "medium" }
    }
  }
}
```

**CREATE FILE 2:** `intelligence/soul/voice_blueprint.md`

A human-readable 200-word voice blueprint document expanding on the JSON `voice_blueprint` field. Include:
- Speaking rhythm description
- Filler word patterns with frequency
- Sentence structure examples
- Transition phrase examples
- Emphasis and repetition patterns
- Profanity comfort level
- Natural metaphor domains

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify config.yaml and transcripts exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Client Soul Extraction SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load transcripts and business materials", status: "completed" },
    { id: "step-4", description: "STEP 4: REASON - Execute Soul Cartographer analysis", status: "completed" },
    { id: "step-5", description: "STEP 5: EMIT - Write soul_values.json and voice_blueprint.md", status: "completed" },
    { id: "step-6", description: "STEP 6: VALIDATE - Schema check + voice fidelity gates", status: "pending" },
    { id: "step-7", description: "STEP 7: H10/H8 DISTILLATION GATE - Run philosophy-distiller", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "pending" }
  ]
});
```

---

## STEP 6: VALIDATE (I-R-E-V-C Phase V)

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify config.yaml and transcripts exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Client Soul Extraction SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load transcripts and business materials", status: "completed" },
    { id: "step-4", description: "STEP 4: REASON - Execute Soul Cartographer analysis", status: "completed" },
    { id: "step-5", description: "STEP 5: EMIT - Write soul_values.json and voice_blueprint.md", status: "completed" },
    { id: "step-6", description: "STEP 6: VALIDATE - Schema check + voice fidelity gates", status: "in_progress" },
    { id: "step-7", description: "STEP 7: H10/H8 DISTILLATION GATE - Run philosophy-distiller", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "pending" }
  ]
});
```

**VALIDATION GATES:**

| # | Gate | Requirement | If Fail |
|---|------|-------------|---------|
| 1 | JSON valid | `soul_values.json` parses without error | FIX → Correct JSON syntax |
| 2 | Core values | ≥4 values, each with transcript evidence | FIX → Re-extract from transcripts |
| 3 | Internal temperature | ≥4 sub-topics mapped | FIX → Add missing sub-topics |
| 4 | Unique metaphors | ≥3 metaphors, each coach-specific | FIX → Replace generic with specific |
| 5 | Emotional vocabulary | ≥6 words | FIX → Extract more from transcripts |
| 6 | Voice blueprint | EXACTLY 200 words | FIX → Trim or expand to 200 |
| 7 | Signature perspective | 1-2 sentences, first person | FIX → Rewrite in first person |
| 8 | TTT baseline | Valid TTT level (01-09) with reasoning | FIX → Recalculate from evidence |
| 9 | Speech patterns | Filler words, avg sentence length, profanity level all present | FIX → Extract missing patterns |
| 10 | No AI artifacts | Zero instances of "leverage", "optimize", "moreover", "furthermore" | FIX → Replace with coach's actual vocabulary |

> [!CAUTION]
> **HARD STOP:** If gates 1, 2, or 8 fail after 2 fix attempts, STOP and report: "SOUL EXTRACTION FAILED — insufficient transcript data or extraction quality too low."

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify config.yaml and transcripts exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Client Soul Extraction SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load transcripts and business materials", status: "completed" },
    { id: "step-4", description: "STEP 4: REASON - Execute Soul Cartographer analysis", status: "completed" },
    { id: "step-5", description: "STEP 5: EMIT - Write soul_values.json and voice_blueprint.md", status: "completed" },
    { id: "step-6", description: "STEP 6: VALIDATE - Schema check + voice fidelity gates", status: "completed" },
    { id: "step-7", description: "STEP 7: H10/H8 DISTILLATION GATE - Run philosophy-distiller", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "pending" }
  ]
});
```

---


---

## STEP 7: H10/H8 DISTILLATION GATE

Mark step-7 `in_progress`.

> [!CAUTION]
> **MANDATORY GATE — Pipeline blocks if this fails.**

1. Read FULL: `ccf-26/skills/ccf/distillation/philosophy-distiller/SKILL.md`
2. Execute 4-Phase Audit on `soul_values.json` and `story_inventory.json`:
   - Law 1: Belief Depth Audit (L2/L3 stratification)
   - Law 2: Story Inventory Audit (T/V/R mode coverage)
   - Law 3: Evolution Tracking Audit
   - Law 4: Philosophy Authenticity Gate (100% Provenance)
3. **CREATE FILE:** `intelligence/soul/H10_DISTILLATION_RECEIPT.md`

**IF FAIL:** Return to STEP 4 (REASON) — re-execute extraction targeting failing depth layers or missing provenance.
**IF PASS:** Continue to STEP 8.

Mark step-7 `completed`.


## STEP 8: CHECKPOINT (I-R-E-V-C Phase C)

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify config.yaml and transcripts exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Client Soul Extraction SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load transcripts and business materials", status: "completed" },
    { id: "step-4", description: "STEP 4: REASON - Execute Soul Cartographer analysis", status: "completed" },
    { id: "step-5", description: "STEP 5: EMIT - Write soul_values.json and voice_blueprint.md", status: "completed" },
    { id: "step-6", description: "STEP 6: VALIDATE - Schema check + voice fidelity gates", status: "completed" },
    { id: "step-7", description: "STEP 7: H10/H8 DISTILLATION GATE - Run philosophy-distiller", status: "completed" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "in_progress" }
  ]
});
```

**ACTIONS:**

1. Update `config.yaml`:
   ```yaml
   sessions:
     setup:
       soul_extract:
         status: "complete"
         timestamp: "{ISO date}"
         output: "intelligence/soul/soul_values.json"
         word_count: {transcript_word_count}
   ```

2. Log session metrics to `output/logs/`:
   - Session duration
   - Input token count
   - Output token count
   - Transcript word count processed

**OUTPUT (25-35 words):**
```
✅ SOUL EXTRACTION COMPLETE
- Core values: {N} extracted
- TTT baseline: TTT-{XX}
- Voice blueprint: 200 words
- Files: soul_values.json, voice_blueprint.md
- NEXT: /ccf-tribe-extract {client_name}
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify config.yaml and transcripts exist", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Client Soul Extraction SKILL.md", status: "completed" },
    { id: "step-3", description: "STEP 3: INGEST - Load transcripts and business materials", status: "completed" },
    { id: "step-4", description: "STEP 4: REASON - Execute Soul Cartographer analysis", status: "completed" },
    { id: "step-5", description: "STEP 5: EMIT - Write soul_values.json and voice_blueprint.md", status: "completed" },
    { id: "step-6", description: "STEP 6: VALIDATE - Schema check + voice fidelity gates", status: "completed" },
    { id: "step-7", description: "STEP 7: H10/H8 DISTILLATION GATE - Run philosophy-distiller", status: "completed" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml session status", status: "completed" }
  ]
});
```

---

## 🔗 NEXT: `/ccf-tribe-extract {client_name}`
