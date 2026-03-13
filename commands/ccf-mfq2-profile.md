---
name: ccf-mfq2-profile
description: "MFQ-2 Voice Onboarding — Generates scenario prompts, captures voice responses, and extracts Moral Foundations baseline."
---

# /ccf-mfq2-profile {client_name}

// turbo-all

> **SKILLS_BASE:** `ccf-26/skills/ccf/`
> **SKILL:** `setup/emotional-dna-extraction/SKILL.md` (Phase 0 mode)

**Objective:**
Extract the coach's Moral Foundations Theory (MFQ-2) baseline (Item 02) BEFORE running standard soul extraction. Written answers activate Identity-Protective Cognition; Voice Notes bypass it.

---

## 🎯 STEP 0: INITIALIZE HARNESS

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "PRE-FLIGHT - Verify init completion", status: "pending" },
    { id: "step-2", description: "GENERATE PROMPTS - Create 6 MFQ-2 scenario provocations", status: "pending" },
    { id: "step-3", description: "PROCESS RESPONSES - Transcribe voice notes", status: "pending" },
    { id: "step-4", description: "EXTRACT & SCORE - Calculate Moral Foundation weightings", status: "pending" },
    { id: "step-5", description: "CHECKPOINT - Write to intelligence_library", status: "pending" }
  ]
});
```

---

## STEP 1: PRE-FLIGHT

Mark step-1 `in_progress`.

**Validate:**
1. Does `ccf-26/Production/{client_name}/config.yaml` exist?
2. Is `sessions.setup.init.status == "complete"`?
3. Does the directory `intelligence_library/` exist?

If NO → STOP. Run `/ccf-init` first.

Mark step-1 `completed`.

---

## STEP 2: GENERATE PROMPTS (Agentic Phase A)

Mark step-2 `in_progress`.

Instead of asking static questions, spawn the `Scenario_Designer_Agent` to generate 6 highly specific, conversational voice-note prompts (one for each of Haidt's 6 foundations: Care/Harm, Fairness/Cheating, Loyalty/Betrayal, Authority/Subversion, Sanctity/Degradation, Liberty/Oppression).

**Rules:**
- **Constraint:** Must be conversational (Telegram style).
- **Constraint:** Must describe a specific, concrete scenario, NOT an abstract concept.
- **Goal:** Violate the foundation to measure the automatic recoil intensity.

**Output:** `intelligence_library/mfq2_prompts.json`

*(Note: Human operator must send these to the coach, wait for voice notes, and place them in `raw/voice_notes/mfq2/` before continuing to Step 3)*

Mark step-2 `completed`.

---

## STEP 3: PROCESS RESPONSES (Agentic Phase B)

Mark step-3 `in_progress`.

If audio files exist in `raw/voice_notes/mfq2/`:
1. Spawn `Whisper_Transcription_Agent`.
2. Transcribe verbatim (preserving all fillers, pauses, and intensity spikes).

Mark step-3 `completed`.

---

## STEP 4: EXTRACT & SCORE (Agentic Phase C)

Mark step-4 `in_progress`.

1. Spawn `MFQ2_Scorer_Agent`.
2. Analyze the verbatim transcriptions.
3. **Turn-Level Scoring:** Look for automatic recoil markers (speech rate acceleration, immediate dismissal, absolute language).
4. Score each of the 6 foundations on a 1-5 intensity scale.
5. Identify the **Primary Foundation** and **Secondary Foundation**.

Mark step-4 `completed`.

---

## STEP 5: CHECKPOINT (Write Output)

Mark step-5 `in_progress`.

Update or create `intelligence_library/emotional_dna.json`:

```json
{
  "version": "v6_mfq2_baseline",
  "moral_foundations": {
    "primary": "{highest_scoring_foundation}",
    "secondary": "{second_highest_scoring}",
    "scores": {
      "care_harm": {1-5},
      "fairness_cheating": {1-5},
      "loyalty_betrayal": {1-5},
      "authority_subversion": {1-5},
      "sanctity_degradation": {1-5},
      "liberty_oppression": {1-5}
    },
    "provenance": "mfq2_voice_onboarding"
  }
}
```

**Update Config:**
`config.yaml -> sessions.setup.mfq2_profile = { status: "complete" }`

**Update Display:**
`NEXT: Proceed to /ccf-soul-extract`

Mark step-5 `completed`.
