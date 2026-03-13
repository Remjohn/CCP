---
name: ccf-elicit
description: "Weekly Subsystem 3 — Process coach voice notes into structured transcriptions"
---

# /ccf-elicit {client_name}

// turbo-all

> **SKILLS_BASE:** `ccf-26/skills/ccf/`
> **SKILL:** `content/coach-elicitation/SKILL.md`
> **TOOL:** `tools/transcribe_voice.py`

**Objective:** Transcribe coach voice note responses, tag by source question, extract key phrases, and output `coach_soc_batch.md`.

---

## 🎯 STEP 0: INITIALIZE TODOS

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify provocation_questions.json + voice notes exist", status: "pending" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Coach Elicitation SKILL.md", status: "pending" },
    { id: "step-3", description: "STEP 3: INVENTORY - Scan voice notes dir, match to questions", status: "pending" },
    { id: "step-4", description: "STEP 4: TRANSCRIBE - Run transcribe_voice.py batch on all files", status: "pending" },
    { id: "step-5", description: "STEP 5: TAG - Associate transcriptions with question metadata", status: "pending" },
    { id: "step-6", description: "STEP 6: EXTRACT - Pull key phrases, emotional peaks, story fragments", status: "pending" },
    { id: "step-7", description: "STEP 7: EMIT - Write coach_soc_batch.md", status: "pending" },
    { id: "step-8", description: "STEP 8: CHECKPOINT - Update config.yaml", status: "pending" }
  ]
});
```

---

## STEP 1: PRE-FLIGHT

| Check | Path | If Missing |
|-------|------|------------|
| 1 | `intelligence/weekly/{week_id}/provocation_questions.json` | STOP → Run `/ccf-question` |
| 2 | `raw/voice_notes/{week_id}/` directory with audio files | STOP → Coach hasn't responded yet |
| 3 | `GROQ_API_KEY` env variable | WARN → Will use local whisper (slower) |

---

## STEP 2: LOAD SKILL

Read FULL: `ccf-26/skills/ccf/content/coach-elicitation/SKILL.md`

---

## STEP 3: INVENTORY

Scan `raw/voice_notes/{week_id}/` → list all audio files → match `q01_response.*` to question IDs.

---

## STEP 4: TRANSCRIBE

Run: `python tools/transcribe_voice.py batch "raw/voice_notes/{week_id}/"`

---

## STEP 5: TAG

For each transcription, associate with question metadata from `provocation_questions.json`:
- `question_id`, `archetype`, `pillar_id`, `friction_point_id`

---

## STEP 6: EXTRACT

For each transcription:
- Signature phrases, emotional peaks, story fragments, named references, contrarian markers
- Depth assessment (Deep >200w / Standard 50-200w / Shallow <50w)
- Generate Depth Probes for shallow responses

---

## STEP 7: EMIT

**CREATE FILE:** `intelligence/weekly/{week_id}/coach_soc_batch.md`

---

## STEP 8: CHECKPOINT

```
✅ COACH ELICITATION COMPLETE (Week {week_id})
- Responses: {N}/{M} questions answered
- Total duration: ~{X} minutes
- Depth distribution: {N} deep, {M} standard, {K} shallow
- NEXT: /ccf-theme-discover --mode dynamic {client_name}
```

---

## 🔗 NEXT: `/ccf-theme-discover --mode dynamic {client_name}`
