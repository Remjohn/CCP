# H0 — Layered Questions: First-Principles Implementation Architecture (CCF Pipeline)

**Pipeline Stage:** CCF Weekly Subsystem 2 of 7 → Question Engineer → Provocation Questions  
**Laws Applied:** 4 Laws of Layered Questions (v3 — CCF)  
**Target Skill:** `ccf-26/skills/ccf/content/question-engineer/SKILL.md`  
**Output:** `provocation_questions.json` — 3-5 compressed, multi-mode provocation questions  
**Validation:** H0 Distillation Receipt (Required before downstream CCF subsystems use question outputs)

---

## System Overview: What H0 Actually Does in CCF

The CCF Question Engineer (Weekly Subsystem 2) converts friction points from the Intelligence Radar into **provocation questions** designed to bypass the Coach's performative layer and reach genuine conviction. The coach receives questions that are engineered to trigger specific neural pathways: origin wounds, recurring sermons, client war stories, and contrarian positions.

The goal is not to get information. The goal is to get the coach to **pause, feel, and tell a specific story** that the audience will recognize as truth. If the answer could have been given by any coach in the niche, the system has failed.

H0 Distillation Laws govern HOW those questions are constructed, compressed, and validated.

---

## Section 1: Input Quality Standards (Saturation Protocol)

### Required CCF Input Files

| # | Input Source | CCF File / Field | Minimum Quality Standard |
|:--|:-------------|:--------------|:------------------------|
| 1 | `intelligence_radar.json` | Friction points + `trigger_archive_match` | Must contain ≥3 friction points with trigger matches |
| 2 | `project_context.json` Layer 6 | Counter-Stance, Recurring Sermon | Must contain ≥1 named Counter-Stance the coach would defend publicly |
| 3 | `project_context.json` Layer 7 | Origin Wound, Secret Doubt, Client War Stories, Victory Reliving, Red Line | Must contain ≥1 Origin Wound or Secret Doubt |
| 4 | `soul_values.json` | Coach's beliefs, enemies, ideology | Must contain ≥3 positions the coach would defend publicly |
| 5 | `tribe_profile.json` | Audience pain points, fears, shared rituals | Must contain ≥5 specific pain points (not "they feel stuck") |

### Saturation Gate (Pre-Generation Check)

```
SATURATION GATE:
1. "Does project_context Layer 6 contain ≥1 Counter-Stance?"
   → NO = INSUFFICIENT (CONTRARIAN questions will be generic)
   → YES = PASS

2. "Does intelligence_radar contain ≥3 friction points with trigger_archive_match?"
   → NO = INSUFFICIENT (not enough signals to generate provocations)
   → YES = PASS

3. "Does project_context Layer 7 contain ≥1 Origin Wound or Secret Doubt?"
   → NO = INSUFFICIENT (VULNERABILITY PROBE and SHADOW EXPLORER will be unfounded)
   → YES = PASS
```

**If any gate fails:** The system flags the gap. No questions are generated on insufficient inputs. The Intelligence Radar must be re-run or project context enriched.

---

## Section 2: Law Execution Protocol

### Law 1 — Saturation Before Generation

**What it does:** Tags every friction point from `intelligence_radar.json` with its detection mode before question construction begins.

**Execution:**
```
FOR EACH friction point in intelligence_radar.json:
  → Read trigger_archive_match field
  → Route to archetype → Tag with mode:
    recurring_sermon     → CONTRARIAN         → mode: TENSION
    origin_wound         → VULNERABILITY PROBE → mode: VULNERABILITY
    client_war_stories   → COMPASSION MIRROR   → mode: RECOGNITION
    victory_reliving     → COMPASSION MIRROR   → mode: RECOGNITION
    secret_doubt         → SHADOW EXPLORER     → mode: VULNERABILITY × TENSION
    red_line             → SHADOW EXPLORER     → mode: VULNERABILITY × TENSION
    no match             → CONTRARIAN (default) → mode: TENSION
```

**Output of Law 1:** A tagged saturation map showing mode coverage across friction points.

---

### Law 2 — 3-Mode Emotional Detection (Archetype Routing)

**What it does:** Generates 5-7 mode-tagged provocation questions by routing friction points through the 4 CCF archetypes.

**Execution per archetype:**

**CONTRARIAN 🔥 (TENSION):**
> Present the mainstream belief as a "fact" and ask the Coach to destroy it.
> Template: "Everyone's saying {mainstream_belief}. Why are they wrong?"
> Expected: Heated defense of philosophy, strong language, conviction.

**VULNERABILITY PROBE 💔 (VULNERABILITY):**
> Reference a specific moment from the Coach's past or a crack in their armor.
> Template: "Tell me about the time you almost {vulnerability_event}. What actually happened?"
> Expected: Raw, unscripted vulnerability, sensory details, emotional narrative.

**COMPASSION MIRROR 🪞 (RECOGNITION):**
> Describe a client's pain in detail and ask the Coach to speak directly to that person.
> Template: "One of your clients is lying awake because {client_pain}. What would you say to them right now?"
> Expected: Protective, nurturing, specific advice from real client experience.

**SHADOW EXPLORER 🌑 (VULNERABILITY × TENSION):**
> Ask about the uncomfortable edge — the thing they don't usually talk about.
> Template: "What's the one thing about {pillar_topic} that you sometimes doubt?"
> Expected: Genuine surprise, potentially uncomfortable authenticity.

**Guard-rail from Alchemy:**
`"Demonstrated competence precedes permission to be uncertain."` — VULNERABILITY PROBE and SHADOW EXPLORER questions are ONLY generated if `project_context.json` Layer 7 contains competence evidence (client results, testimonials). Otherwise, these archetypes are skipped in favor of CONTRARIAN and COMPASSION MIRROR.

**Batch archetype mix (existing CCF requirement):**
- Minimum 2 CONTRARIAN
- Minimum 1 VULNERABILITY PROBE
- Minimum 1 COMPASSION MIRROR
- Maximum 1 SHADOW EXPLORER
- Maximum 1 CONTRARIAN_NUCLEAR (red_line) per month

---

### Law 3 — Compression, Not Elimination

**What it does:** Merges single-archetype questions into multi-mode compressed questions.

**Layer 1 Example (Cross-Archetype Merge):**
```
CONTRARIAN-ONLY: "Why do most financial advisors avoid talking about emotional spending?"
COMPASSION MIRROR-ONLY: "What would you say to a client who just panic-sold everything?"

→ CONTRARIAN × COMPASSION MIRROR (TENSION + RECOGNITION):
"Your client just panic-sold their entire portfolio because a TikTok video told them to.
 Financial Twitter is celebrating the selloff. Why are they BOTH wrong — and what
 would you say to your client right now, not on camera, just to her?"
```

**Compression Rules:**
- A compressed question must activate ≥2 modes
- Word limit: 60-100 words per compressed question
- The coach must need a SPECIFIC MEMORY to answer — not general knowledge
- Output: 3-5 compressed questions (from 5-7 single-archetype questions)

---

### Law 4 — The Unpredictability Gate

**What it does:** Filters compressed questions through 4 checks. Fails are returned for re-compression.

```
CHECK 1: "Could ChatGPT answer this with 5 words of context?"
  → YES = REJECT — no specific memory required
  → NO  = PASS

CHECK 2: "Could another coach in the same niche give the exact same answer?"
  → YES = REJECT — no irreducible uniqueness (project_context not embedded)
  → NO  = PASS

CHECK 3: "Does the coach need a SPECIFIC memory, feeling, or client to answer?"
  → NO  = REJECT — theoretical, not experiential
  → YES = PASS

CHECK 4: "Would the coach's answer make someone in the tribe say
          'How did you know that about me?'"
  → NO  = The question lacks RECOGNITION mode
  → YES = PASS — the specificity→universality bridge is operational
```

**If any check fails:** The question returns to compression. Failed questions are NOT included in `provocation_questions.json`.

---

## Section 3: Enhanced Output Format

```json
{
  "week_id": "2026-W08",
  "generated_date": "{ISO date}",
  "questions": [
    {
      "id": "q_01",
      "archetype": "contrarian",
      "mode": "TENSION",
      "mode_justification": "Breaks mainstream prediction about market timing",
      "merged_archetypes": ["contrarian", "compassion_mirror"],
      "merged_modes": ["TENSION", "RECOGNITION"],
      "pillar_id": "pillar_03",
      "friction_point_id": "fp_01",
      "question_text": "...",
      "stimulus": {
        "type": "video",
        "url": "https://tiktok.com/...",
        "description": "Finance influencer telling followers to liquidate"
      },
      "trigger_target": "recurring_sermon",
      "expected_reaction": "heated_defense",
      "intensity": 7,
      "unpredictability_gate": {
        "check_1_chatgpt": "PASS",
        "check_2_competitor": "PASS",
        "check_3_specific_memory": "PASS",
        "check_4_recognition": "PASS"
      }
    }
  ],
  "archetype_distribution": {
    "contrarian": 2,
    "vulnerability_probe": 1,
    "compassion_mirror": 1,
    "shadow_explorer": 1
  },
  "mode_distribution": {
    "tension": 3,
    "vulnerability": 2,
    "recognition": 2
  },
  "compression_ratio": "6 → 4 questions",
  "total_questions": 4
}
```

---

## Section 4: Evaluation — 5 Micro-Hypothesis Tests

### MH1 — The Tribe Recognition Test
**Hypothesis:** "If a member of the coach's tribe read the coach's answer verbatim, they would feel 'How did you know that about me?' within 10 seconds."
**Test:** Extract 2-3 sentences from the anticipated answer space. Would a tribe member identify their own experience?
**Pass condition:** Contains ≥1 specific detail only recognizable inside the tribe.

### MH2 — The First-Party Test
**Hypothesis:** "The coach's answer could not have been generated by AI or copied from a competitor."
**Test:** Does answering require a named person, specific date, location, or lived sensory detail?
**Pass condition:** ≥1 irreducibly specific element forced by the question design.

### MH3 — The Compression Yield Test
**Hypothesis:** "Compressed questions produce answers with higher signal density than single-archetype questions."
**Test:** Compare mode density: does the expected answer span ≥2 modes within 3 sentences?
**Pass condition:** A 3-sentence response block activates ≥2 emotional modes.

### MH4 — The Alchemy Activation Test
**Hypothesis:** "The coach's answer activates ≥5 of the 10 Conscious Movement Alchemy principles."
**Test:** Score against: Specificity Creates Universality, Vulnerability Precedes Connection, Prediction Error, Costly Signaling, The Shadow, Information Gap, Emotion Requires Accuracy, Truth Is Recognized Not Taught, Attention Is Felt, The Mess.
**Pass condition:** ≥5/10 principles activated in the combined response.

### MH5 — The Downstream Utility Test
**Hypothesis:** "This week's provocation output directly feeds ≥3 distinct CCF content archetypes without additional coach input."
**Test:** Map each compressed question to a CCF content archetype:
- TENSION-dominant → Confrontation, Warning, Pattern Interrupt
- VULNERABILITY-dominant → Witness, Breakthrough, Sacred Return
- RECOGNITION-dominant → Shared Struggle, Quiet Reflection
**Pass condition:** Each question maps to a distinct archetype with minimal overlap.

---

## Section 5: H0 Validation Receipt

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ H0 DISTILLATION RECEIPT (CCF)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Week:             [week_id]
Coach:            [Coach Name]

SATURATION GATE:
  intelligence_radar loaded:  ✅ (≥3 friction points)
  project_context Layer 6:    ✅ (≥1 Counter-Stance)
  project_context Layer 7:    ✅ (≥1 Origin Wound/Secret Doubt)
  soul_values loaded:         ✅
  tribe_profile loaded:       ✅

LAW EXECUTION:
  Law 1 — Saturation:        ✅ PASSED (friction points mode-tagged)
  Law 2 — Archetype Routing:  ✅ [n] questions generated (distribution: nC/nVP/nCM/nSE)
  Law 3 — Compression:       ✅ [n] → [m] compressed questions
  Law 4 — Unpredictability:  ✅ All [m] passed 4-check gate

MODE DISTRIBUTION:
  TENSION:        [n]
  VULNERABILITY:  [n]
  RECOGNITION:    [n]

MICRO-HYPOTHESES:
  MH1 Tribe Recognition:     [PASS/FAIL]
  MH2 First-Party:           [PASS/FAIL]
  MH3 Compression Yield:     [PASS/FAIL]
  MH4 Alchemy Activation:    [PASS/FAIL] ([n]/10 principles)
  MH5 Downstream Utility:    [PASS/FAIL] ([n] archetypes mapped)

OUTPUT:
  provocation_questions.json: ✅ Created at intelligence/weekly/{week_id}/

VERDICT: ✅ H0 DISTILLATION COMPLETE — CLEARED FOR CCF DOWNSTREAM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Architectural Constants

| Constant | Value | Rationale |
|:---------|:------|:----------|
| Raw questions generated | 5-7 | CCF Question Engineer batch size |
| Compression output | 3-5 | Post-compression, multi-mode |
| Mode coverage minimum | ≥2 modes present | Prevents single-mode dominance |
| Unpredictability checks | 4 per question | Each targets a different signal quality |
| Alchemy activation threshold | ≥5/10 | System performs at Alchemy standards |
| Downstream utility | ≥3 distinct archetypes | Ensures weekly output feeds multiple content pieces |

---

## V2WS (Voice2WebinarSystem) Integration

The 3-5 provocation questions compiled in `provocation_questions.json` are not just for written content. They serve as the modular voice intake questions for the V2WS (Voice2WebinarSystem) pipeline:

1. **Trigger:** The coach executes a slash command to launch V2WS mode.
2. **Voice Intake:** The system presents the provocation questions, and the coach uses voice input to respond, capturing raw, authentic emotion.
3. **Script Compilation:** The system compiles the voice inputs into the structured Webinar Script.
4. **Webinar Pipeline:** This initiates the delivery loop:
   - **Delivery Training:** Rehearsing delivery metrics.
   - **Recording Session:** Executing the full session once ready.
   - **Final Editing:** Rendering and editing the recorded webinar as the closing loop event.

---

*Next Document: [H1 — Blueprint Orchestrator: 4 Laws of Content Distillation — CCF Pipeline]*
