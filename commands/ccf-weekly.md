---
name: ccf-weekly
description: "Master orchestrator for the full CCF v2.5 weekly content cycle — runs all 7 subsystems + memory engine in sequence"
---

# /ccf-weekly {client_name}

// turbo-all

> **Master Orchestrator — CCF v2.5 Weekly Content Engine**
> Runs all 7 subsystems in sequence to produce a complete week of content from a single coach interaction.

**Objective:** Execute the complete Two-Step Batch Interview content cycle: find what's trending → generate provocation questions → collect coach responses → **learn from responses** → generate dynamic themes → research → write multi-format scripts → create recording guides.

---

## 🎯 STEP 0: INITIALIZE TODOS

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify project_context.json + determine week_id", status: "pending" },
    { id: "step-2", description: "STEP 2: RADAR - Run Intelligence Radar (Subsystem 1) + trigger activation scoring", status: "pending" },
    { id: "step-2b", description: "STEP 2b: TRIGGER-MATCH - Run Trigger Matching + Activation Event Design (NEW v3.1)", status: "pending" },
    { id: "step-3", description: "STEP 3: QUESTION - Run Question Engineer (trigger-first or legacy mode)", status: "pending" },
    { id: "step-4", description: "STEP 4: WAIT - Deliver questions to Coach + wait for voice notes", status: "pending" },
    { id: "step-5", description: "STEP 5: ELICIT - Run Coach Elicitation Engine (Subsystem 3)", status: "pending" },
    { id: "step-5a", description: "STEP 5a: AUTHENTICITY - LIWC-22 scoring on voice note responses (NEW v3.1)", status: "pending" },
    { id: "step-5b", description: "STEP 5b: LEARN - Run Memory Engine update (Voice DNA + Triggers + EDNA)", status: "pending" },
    { id: "step-6", description: "STEP 6: THEME - Run Dynamic Theme Generator + trigger-matched seeds", status: "pending" },
    { id: "step-7", description: "STEP 7: RESEARCH - Run Deep Research V3 per theme (Subsystem 5)", status: "pending" },
    { id: "step-8", description: "STEP 8: SCRIPT - Run Script Architect + voice_dna hooks", status: "pending" },
    { id: "step-9", description: "STEP 9: RECORD - Run Recording Director + session intel + LIWC rubric", status: "pending" },
    { id: "step-10", description: "STEP 10: CHECKPOINT - Final status + weekly summary", status: "pending" }
  ]
});
```

---

## STEP 1: PRE-FLIGHT

Mark step-1 `in_progress`.

| Check | Path | If Missing |
|-------|------|------------|
| 1 | `intelligence/project_context.json` | STOP → Run `/ccf-pillar-build` first |
| 2 | Config.yaml `pillar_build.status == "complete"` | STOP → Pillars not built |
| 3 | Previous week completed? | Check `weekly_history` for continuity |

**Determine:** `week_id` = current ISO week (e.g., `2026-W08`)
**Create:** `intelligence/weekly/{week_id}/` directory

Mark step-1 `completed`.

---

## STEP 2: RADAR (Subsystem 1)

Mark step-2 `in_progress`.

**Execute:** Load and run `ccf-26/commands/ccf-radar.md` protocol.
- Select 4 pillars via rotation algorithm
- Run multi-source sweep (Google Trends, web search, social signals)
- Compute sentiment alignment
- **NEW (v3.1):** If `trigger_map.json` exists, compute `trigger_activation_score` per friction point and re-rank by `(0.4 × sentiment) + (0.6 × trigger_activation)` _(Haidt MFT, Scherer CPM)_
- **Output:** `intelligence/weekly/{week_id}/intelligence_radar.json` (now includes `trigger_activation_score`, `matched_trigger_id`, `matched_foundation` per friction point)

Mark step-2 `completed`.

---

## STEP 2b: TRIGGER-MATCH (Trigger-First Engine — NEW v3.1) 🔥

Mark step-2b `in_progress`.

> [!IMPORTANT]
> **PIPELINE INVERSION:** This is the new step that converts the pipeline from topic-first to trigger-first. It matches audience L3 pain to coach trigger architecture, designs ESK-targeting activation events, and generates trigger-first provocation questions.

**Prerequisite:** `intelligence_library/trigger_map.json` AND `intelligence_library/emotional_dna.json` must exist with `pipeline_ready: true`. If they don't exist → **SKIP this step** and fall back to legacy question generation in STEP 3.

**Execute:** Load and run `ccf-26/commands/ccf-trigger-match.md` protocol.
- Run 2-axis matching (Moral Foundation + Temporal Position) between audience L3 data and coach triggers
- Design ESK-targeting activation events with DARN-CAT dimensions
- Generate ≤80-word Telegram provocation questions
- Build LIWC-22 authenticity scoring rubric
- **Outputs:**
  - `intelligence/weekly/{week_id}/trigger_matched_seeds.json`
  - `intelligence/weekly/{week_id}/activation_events.json`
  - `intelligence/weekly/{week_id}/provocation_questions.json` (trigger-first format)
  - `intelligence/weekly/{week_id}/liwc_scoring_rubric.json`

Mark step-2b `completed`.

---

## STEP 3: QUESTION (Subsystem 2 + Memory — Trigger-First Compatible)

Mark step-3 `in_progress`.

**MODE SELECTION (v3.1):**
- If `activation_events.json` EXISTS (from STEP 2b) → **Trigger-First Mode**: Question Engineer validates and formats the activation events. Does NOT redesign questions.
- If `activation_events.json` DOES NOT EXIST → **Legacy Mode**: Full original question generation protocol.

**Memory Read:** If `intelligence/memory/coach_memory.json` exists:
- Load `session_intelligence.question_effectiveness` → bias archetype mix toward what works for THIS Coach
- Load `session_intelligence.optimal_question_order` → sequence questions accordingly
- Load `session_intelligence.response_patterns.skipped_topics` → avoid topics Coach ignores

**Execute:** Load and run `ccf-26/commands/ccf-question.md` protocol.
- In trigger-first mode: validate activation events, apply LAW 3 compression + LAW 4 gate, format with archetype tags
- In legacy mode: map friction points to 4 question archetypes (biased by memory)
- Generate 5-7 provocation questions
- **Output:** `intelligence/weekly/{week_id}/provocation_questions.json`

Mark step-3 `completed`.

---

## STEP 4: WAIT — Coach Interaction Point ⏸️

Mark step-4 `in_progress`.

> [!IMPORTANT]
> **THIS STEP REQUIRES HUMAN INTERACTION.**
> The system pauses here. The Coach must:
> 1. Receive the 5-7 provocation questions (delivered via email/WhatsApp)
> 2. Record voice note responses (5-15 min total)
> 3. Drop audio files into `raw/voice_notes/{week_id}/`
>
> **Naming convention:** `q01_response.m4a`, `q02_response.m4a`, etc.
>
> **RESUME** this workflow once voice notes are available.

**Present to user:**
```
⏸️ WAITING FOR COACH VOICE NOTES

Questions ready: {N} questions generated
Delivery: Send questions from provocation_questions.json to coach
Expected commitment: 5-15 minutes of voice notes

Drop recordings to: raw/voice_notes/{week_id}/
Name files: q01_response.m4a, q02_response.m4a, etc.

When files are ready, re-run: /ccf-weekly {client_name} --resume-from elicit
```

Mark step-4 `completed` (when voice notes confirmed available).

---

## STEP 5: ELICIT (Subsystem 3)

Mark step-5 `in_progress`.

**Execute:** Load and run `ccf-26/commands/ccf-elicit.md` protocol.
- Transcribe all voice notes
- Tag responses by source question
- Extract key phrases and emotional peaks
- **Output:** `intelligence/weekly/{week_id}/coach_soc_batch.md`

Mark step-5 `completed`.

---

## STEP 5a: AUTHENTICITY SCORE (LIWC-22 Gate — NEW v3.1) 🔬

Mark step-5a `in_progress`.

> [!IMPORTANT]
> **NEW GATE:** This step validates whether the coach's voice note responses contain authentic episodic material (autonoetic retrieval) or rehearsed semantic output (noetic synthesis). Only runs if LIWC scoring rubric exists.

**Prerequisite:** `intelligence/weekly/{week_id}/liwc_scoring_rubric.json` must exist (from STEP 2b). If not → **SKIP** (backward-compatible).

**Execute:**
1. Load `liwc_scoring_rubric.json`
2. For each transcribed voice note in `coach_soc_batch.md`:
   - Score against 7 LIWC-22 authenticity markers (1st person singular, exclusive words, hedging, sentence length variance, verb tense ratio, filler frequency, discourse marker position)
   - Compute composite authenticity score (weighted sum, 0.0-1.0)
3. Apply gate threshold (0.6):
   - **≥ 0.6:** Response is authentic episodic material ✅ → proceed normally
   - **< 0.6:** Response is likely rehearsed semantic output ⚠️ → flag for re-activation
4. Report: per-response scores, overall batch authenticity, flagged responses

**If any response flagged:**
- Log which activation event produced the flagged response
- Recommend: higher-specificity activation event for next cycle
- Do NOT block the pipeline — flagged responses still proceed but with `authenticity_warning: true` tag

_Research: Pennebaker LIWC-22 (2022), Hatfield Emotional Contagion 3-stage mechanism (1993)_

Mark step-5a `completed`.

---

## STEP 5b: LEARN (Memory Engine + Trigger Update) 🧠

Mark step-5b `in_progress`.

**Execute:** Load and run `ccf-26/commands/ccf-memory.md` in `update` mode.
- Scan new `coach_soc_batch.md` for signature phrases, stories, metaphors
- Update Voice DNA (accumulate, don't overwrite)
- Update Session Intelligence (archetype effectiveness, response patterns)
- Run Trigger Evolution (patch Layer 7 `[PENDING]` fields if confidence ≥ 0.7)
- **NEW (v3.1) — Trigger Architecture Update:**
  - Feed LIWC-22 authenticity scores per question back to `trigger_map.json → activation_history[]`
  - Track which triggers produced the highest authenticity scores → these are the strongest fires
  - Update `emotional_dna.json` with any new evidence passages from this week's responses
  - Update `trigger_map.json → staleness_tracking` with latest activation data
- **Output:** Updated `intelligence/memory/coach_memory.json` (+ `project_context.json` if triggers patched)
- **NEW (v3.1):** Updated `intelligence_library/trigger_map.json` (activation_history + staleness)
- **NEW (v3.1):** Updated `intelligence_library/emotional_dna.json` (new evidence passages)

Mark step-5b `completed`.

---

## STEP 6: THEME (Subsystem 4 + Memory)

Mark step-6 `in_progress`.

**Memory Read:** If `intelligence/memory/coach_memory.json` exists:
- Load `performance_log.patterns` → bias toward winning formulas and best-performing archetypes
- Load `voice_dna.story_bank` → reference known stories for richer theme construction
- Load `voice_dna.energy_map` → prioritize high-energy topics

**Execute:** Load and run Dynamic Theme Generator protocol.
- Read `ccf-26/skills/ccf/content/dynamic-theme-generator/SKILL.md`
- Extract core arguments from Coach SoC
- Map DHDs, cognitive biases, viral frameworks
- Run Conscious Movie Alchemy Checklist
- **Output:** `intelligence/weekly/{week_id}/dynamic_content_themes.json`

Mark step-6 `completed`.

---

## STEP 6b: TIER LIST & RATING IDEAS (Optional)

If `coach_telegram_config.yaml` exists in the coach's project directory:

**Execute:** Generate tier list / rating video ideas from the weekly themes.
- Read `intelligence/weekly/{week_id}/dynamic_content_themes.json`
- Select 3 themes based on coach preferences
- Route each through an archetype prompt (authority / controversial / roast / relatable)
- Generate ideas via OpenRouter API
- **Output:** `intelligence/weekly/{week_id}/tierlist_rating_ideas.json`

**Delivery:** Ideas are sent to the coach's Telegram on their configured delivery day.
- Run `tools/telegram-tierlist-bot/bot.py --coach {client_name}`
- Or let the scheduler handle it: `tools/telegram-tierlist-bot/scheduler.py`

---

## STEP 7: RESEARCH (Subsystem 5)

Mark step-7 `in_progress`.

**For EACH theme in dynamic_content_themes.json:**

**Execute:** Load and run `ccf-26/commands/ccf-research-deep.md` protocol.
- Use theme's `research_directives` as the research brief
- Apply Biased Scoring (Coach philosophy alignment)
- Check research_cache.json for existing findings
- Generate dual-language queries (EN + FR for francophone coaches)
- Build Quote Bank at end of dossier
- **Output:** `intelligence/weekly/{week_id}/{theme_id}_dossier.md`

**After all themes researched:**
- Run Synergy Matrix detection across all dossiers
- Update `research_cache.json` with new entries

Mark step-7 `completed`.

---

## STEP 8: SCRIPT (Subsystem 6 + Memory)

Mark step-8 `in_progress`.

**Memory Read:** If `intelligence/memory/coach_memory.json` exists:
- Load `voice_dna.signature_phrases` → use highest-frequency phrases as hook candidates
- Load `voice_dna.vocabulary_whitelist` → use Coach's real words, not AI synonyms
- Load `voice_dna.metaphor_library` → weave Coach's natural metaphors into scripts

**Execute:** Load and run Script Architect protocol.
- Read `ccf-26/skills/ccf/content/script-architect/SKILL.md`
- For each theme, generate 3 format variants:
  - Video Note (60-90s)
  - Carousel (7-10 slides)
  - Thread/Newsletter (800-1500 words)
- Enforce vocabulary blacklist AND vocabulary whitelist (from memory)
- Enforce coach_voice_anchor in every Hook (prefer high-frequency signature phrases)
- **Output:** `intelligence/weekly/{week_id}/scripts/{theme_id}_{format}.md`

Mark step-8 `completed`.

---

## STEP 9: RECORD (Subsystem 7 + Memory)

Mark step-9 `in_progress`.

**Memory Read:** If `intelligence/memory/coach_memory.json` exists:
- Load `session_intelligence.optimal_question_order` → sequence recording beats accordingly
- Load `session_intelligence.time_of_day_preference` → include in recording logistics
- Load `voice_dna.story_bank` → suggest specific stories for the Coach to reference per beat

**Execute:** Load and run Recording Director protocol.
- Read `ccf-26/skills/ccf/content/recording-director/SKILL.md`
- Convert each video script into interview-style recording guide
- Add Coach voice anchors, bullet-point reminders, off-topic redirects
- **Output:** `intelligence/weekly/{week_id}/recording_guides/{theme_id}_{format}_guide.md`

Mark step-9 `completed`.

---

## STEP 10: CHECKPOINT — Weekly Summary

Mark step-10 `in_progress`.

Update `config.yaml`:
```yaml
sessions:
  weekly:
    "{week_id}":
      status: "complete"
      timestamp: "{ISO date}"
      pillars_used: [pillar_03, pillar_07, pillar_09, pillar_12]
      themes_generated: 4
      scripts_produced: 12
      recording_guides: 4
```

Update `project_context.json`:
- Append to `weekly_history`
- Update `rotation_metadata` for used pillars

**FINAL OUTPUT:**
```
✅ WEEKLY CONTENT CYCLE COMPLETE (Week {week_id})

📊 Production Summary:
- Pillars scanned: 4
- Friction points found: {N}
- Questions generated: {N}
- Coach responses: {N}/{M}
- Dynamic themes: {N}
- Research dossiers: {N}
- Scripts produced: {N × 3} (video + carousel + thread per theme)
- Recording guides: {N}

🧠 Memory Update:
- New signature phrases learned: {N}
- Stories added/updated: {N}
- Trigger fields patched: {N}
- Total weeks of voice data: {N}

📁 Output directory: intelligence/weekly/{week_id}/

📋 Content ready for:
  🎬 Video recording (guides in recording_guides/)
  📱 Carousel design (scripts in scripts/)
  ✍️ Newsletter publication (scripts in scripts/)

💡 After content goes live, run:
  /ccf-memory feedback {client_name}

🔄 NEXT WEEK: /ccf-weekly {client_name}
```

Mark step-10 `completed`.
