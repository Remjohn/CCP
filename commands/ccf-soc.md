---
name: ccf-soc
description: "Stage 1: Voice Priming — Stream of Consciousness generation"
---

# /ccf-soc {client_name} --blueprint {blueprint_id}

// turbo-all

> **SKILLS_BASE:** `ccf-26/skills/ccf/`
> **SKILL:** `production/soc-generator/SKILL.md`
> **STAGE:** 1 of 4 (Voice Priming)
> **TEMPERATURE:** 0.9

**Objective:** Generate a soul-infused Stream of Consciousness — authentic voice material that serves as priming fuel for downstream script generation. Output: `soc_output.json`

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify blueprint + inputs exist", status: "pending" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read SoC Generator v5 SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: INDOCTRINATE - State Alchemy Principles", status: "pending" },
    { id: "step-4", description: "STEP 4: REASON - Analyze inputs, calculate TTT", status: "pending" },
    { id: "step-5", description: "STEP 5: EXECUTE - Generate SoC monologue (160-240 words)", status: "pending" },
    { id: "step-6", description: "STEP 6: EMIT - Write soc_output.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Voice fidelity + TTT + word count gates", status: "pending" },
    { id: "step-8", description: "STEP 8: H3 DISTILLATION GATE - Run voice-distiller 4-Law audit", status: "pending" },
    { id: "step-9", description: "STEP 9: CHECKPOINT - Update config.yaml", status: "pending" }
  ]
});
```

---

## STEP 1: PRE-FLIGHT

Mark step-1 `in_progress`.

| Check | Path | If Missing |
|-------|------|------------|
| 1 | `intelligence/soul/soul_values.json` | STOP → Run `/ccf-soul-extract` |
| 2 | `output/batches/batch_001/blueprints/content_blueprints.json` → find `{blueprint_id}` | STOP → Run `/ccf-blueprint` |
| 3 | `research/vibe_comments/vibe_comments_processed.json` | STOP → Run `/ccf-vibe-comments` |
| 4 | `intelligence/context_premises/` → relevant context premise SPR | WARN → Use tribe_profile as fallback |
| 5 | Research briefs for this theme (fresh + deep) | WARN → Proceed without research integration |

Mark step-1 `completed`.

---

## STEP 2: LOAD SKILL

Mark step-2 `in_progress`.

1. Read FULL: `ccf-26/skills/ccf/production/soc-generator/SKILL.md` (599 lines)
2. **Internalize** every section — this is the most detailed skill in the CCF
3. Pay critical attention to:
   - **Context Premise Analysis** (12 dimensions → dominant 2-3)
   - **TTT Palette Calculation** (dimension → TTT mapping table)
   - **Voice Authenticity Requirements** (filler frequency, sentence rhythm, concrete objects)
   - **TTT-Specific Voice Modulation** (TTT-02 through TTT-07 rules)
   - **Contextual Examples Extraction Strategy** (Hook/Body/CTA parsing)

Mark step-2 `completed`.

---

## STEP 3: INDOCTRINATE (I-R-E-V-C Phase I)

Mark step-3 `in_progress`.

> [!CAUTION]
> **MANDATORY:** State the 10 Alchemy Principles aloud before generating ANY content. This is not ceremony — it primes your context for constraint-aware generation.

**State:** "I have loaded and will enforce:
1. Three-Part Vulnerability Move
2. One Decisive Claim  
3. Information Gap Hook
4. Context Over Content
5. Raw Unfiltered Quotes
6. Specific Language — zero clichés
7. Story Over Lecture
8. Clear Tribal Alignment
9. Complexity Acknowledged
10. Accuracy Over Polish"

> [!IMPORTANT]
> **CRITICAL RULE:** The SoC Generator must NEVER apply structural formatting or word count constraints prematurely. Its ONLY job is authentic voice material — raw, unfiltered, messy. Structure comes in Stage 3.

Mark step-3 `completed`.

---

## STEP 4: REASON (I-R-E-V-C Phase R)

Mark step-4 `in_progress`.

**Execute the SKILL.md analysis protocol:**

1. **Parse context premise** → Identify top 2-3 dominant dimensions
2. **Calculate TTT** → Map dominant dimensions to TTT level using the mapping table
3. **Extract coach voice patterns** from `soul_values.json`:
   - Filler words and frequency
   - Natural sentence length
   - Profanity comfort level
   - Metaphor domains
   - Concrete objects vocabulary
4. **Identify tribe integration points** from `vibe_comments_processed.json`:
   - Which VRC/VCC to activate
   - Tribal slang to weave in naturally
5. **Select research atoms** from fresh + deep briefs:
   - 1 timely hook (fresh)
   - 1 timeless truth (deep)

Mark step-4 `completed`.

---

## STEP 5: EXECUTE (I-R-E-V-C Phase E)

Mark step-5 `in_progress`.

**Generate the Stream of Consciousness (160-240 words):**

**Voice Rules (from SKILL.md):**
- "you know": 3-5 instances
- "like I said": 1-2 instances
- Coach-specific fillers at natural frequency
- Sentence length ±2 words of coach's average
- Concrete objects from coach's vocabulary
- Metaphors within coach's natural domains
- Profanity at coach's comfort level (never exceed)

**TTT Modulation (from SKILL.md):**
- TTT-02: Shorter sentences, validation language, no profanity
- TTT-03: Medium sentences, practical language, strategic "damn/hell"
- TTT-05: Direct sentences, confrontational, strategic profanity
- TTT-07: Punchy sentences, protective, elevated profanity

**Extract simultaneously:**
- 2-3 hook examples (15-20 words each)
- 3-5 body examples (30-50 words each)
- 2-3 CTA examples (15-25 words each)
- 5-8 concrete objects
- 8-12 priming words

Mark step-5 `completed`.

---

## STEP 6: EMIT

Mark step-6 `in_progress`.

**CREATE FILE:** `output/batches/batch_001/soc/{blueprint_id}_soc_output.json`

Follow the EXACT JSON schema from the SKILL.md — including:
- `meta` (content_idea, calculated_ttt, dominant dimensions, reasoning)
- `stream_of_consciousness` (160-240 words)
- `priming_words` (8-12 items)
- `contextual_examples` (hook, body, CTA, concrete objects)
- `emotional_arc_language` (opening, transition, closing phrases)
- `tribe_integration_notes` (heroes, enemies, slang, humor, aspirations, anxieties)

Mark step-6 `completed`.

---

## STEP 7: VALIDATE

Mark step-7 `in_progress`.

**Execute ALL 6 validation checklists from the SKILL.md:**

| # | Checklist | Key Checks | If Fail |
|---|-----------|------------|---------|
| 1 | Voice Fidelity | Sounds like coach, signature phrases, no AI-tells | Regenerate with more coach patterns |
| 2 | Topic Relevance | Content_idea addressed, dimensions surface | Regenerate with topic focus |
| 3 | TTT Calibration | Calculated TTT justified, intensity matches | Recalibrate emotional arc |
| 4 | Tribe Integration | Cultural fluency, insider feeling | Increase tribe integration |
| 5 | Structural Utility | Hook/body/CTA usable, priming words in SoC | Regenerate examples |
| 6 | Variety Mechanism | Different from transcript, topic-specific objects | Vary while preserving voice |

> [!CAUTION]
> **HARD GATE — Word Count:** SoC must be 160-240 words. Outside this range = REJECT and regenerate. No exceptions.

> [!CAUTION]
> **HARD GATE — AI Artifact Scan:** Zero instances of: "leverage", "optimize", "moreover", "furthermore", "in conclusion", "it's important to note", "delve", "utilize". Any found = REJECT that specific section.

Mark step-7 `completed`.

---

## STEP 8: H3 DISTILLATION GATE

Mark step-8 `in_progress`.

> [!CAUTION]
> **MANDATORY GATE — Pipeline blocks if this fails.**

1. Read FULL: `ccf-26/skills/ccf/distillation/voice-distiller/SKILL.md`
2. Execute 4-Phase Audit on `{blueprint_id}_soc_output.json`:
   - Law 1: Emotional Saturation Audit (collision test + input tagging + TTT timing)
   - Law 2: Mode Arc Audit (T + V + R sentences present)
   - Law 3: First-Party Vulnerability Audit (provenance, cost test, mess preserved, fabrication check)
   - Law 4: Alchemy Activation Gate Audit (≥7/10 principles)
3. **CREATE FILE:** `scripts/soc/{blueprint_id}_H3_DISTILLATION_RECEIPT.md`

**IF FAIL:** Return to STEP 5 (EXECUTE) — regenerate with specific remediation from receipt.
**IF PASS:** Continue to STEP 9.

Mark step-8 `completed`.

---

## STEP 9: CHECKPOINT

Mark step-9 `in_progress`.

Update `config.yaml`:
```yaml
sessions:
  production:
    soc:
      "{blueprint_id}":
        status: "complete"
        timestamp: "{ISO date}"
        calculated_ttt: "TTT-XX"
        word_count: {N}
        h3_distillation: "PASS"
```

**OUTPUT:**
```
✅ SOC GENERATION COMPLETE ({blueprint_id})
- Word count: {N} (160-240 range)
- TTT: TTT-{XX}
- Priming words: {N}
- All 6 validation checklists passed
- H3 Distillation Receipt: ✅ PASS
- NEXT: /ccf-adapt {client_name} --blueprint {blueprint_id}
```

Mark step-9 `completed`.

---

## 🔗 NEXT: `/ccf-adapt {client_name} --blueprint {blueprint_id}`
