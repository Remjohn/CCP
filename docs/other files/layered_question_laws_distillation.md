# The 4 Laws of Layered Questions (v3 — CCF Pipeline)

## Upgraded for the CCF Question Engineer Skill

---

## The Starting Axiom

The Question Engineer is CCF Weekly Subsystem 2 of 7. It converts friction points from the Intelligence Radar into **provocation questions** designed to bypass the Coach's performative layer and reach their genuine conviction. The 4 Laws govern how those provocations are constructed, compressed, and validated before delivery.

**Target CCF Skill:** `ccf-26/skills/ccf/content/question-engineer/SKILL.md`  
**Inputs:** `intelligence_radar.json`, `project_context.json` (Layer 6: contrarian positions, Layer 7: trigger archive)  
**Output:** `provocation_questions.json` — 5-7 provocation questions delivered weekly

---

## The 3 Detection Modes (Mapped to CCF Question Archetypes)

The CCF Question Engineer already uses 4 archetypes. These map cleanly to the 3 Detection Modes, with one archetype straddling a boundary:

| CCF Archetype | Detection Mode | Alchemy Grounding |
|:---|:---|:---|
| **CONTRARIAN 🔥** | TENSION | Prediction Error, Surprise Requires Understanding, Information Gap |
| **VULNERABILITY PROBE 💔** | VULNERABILITY | Costly Signaling, The Shadow, Vulnerability Precedes Connection |
| **COMPASSION MIRROR 🪞** | RECOGNITION | Specificity Creates Universality, Truth Is Recognized Not Taught |
| **SHADOW EXPLORER 🌑** | VULNERABILITY × TENSION | Costly Signaling + Information Gap (the uncomfortable edge) |

### Why These 3 and Not Others

From first principles, every provocation question that creates genuine coach reaction does ONE of these three things:

1. **Breaks a prediction** (Tension / CONTRARIAN) → The brain wakes up because a pattern was violated
2. **Exposes a cost** (Vulnerability / VULNERABILITY PROBE + SHADOW EXPLORER) → The brain trusts because the signal is expensive to fake
3. **Articulates the unnamed** (Recognition / COMPASSION MIRROR) → The brain bonds because someone said what it couldn't

These are the **3 irreducible emotional triggers**. Everything else is a VARIANT.

---

## Law 1: Saturation Before Generation

### The Axiom
*A system cannot output signal it has not absorbed.*

### CCF Saturation Sources

| CCF Source | File / Field | Detection Mode It Feeds |
|:---|:---|:---|
| `intelligence_radar.json` | Friction points + `trigger_archive_match` | All 3 modes (determines archetype routing) |
| `project_context.json` Layer 6 | Counter-Stance, Recurring Sermon | TENSION (contrarian positions to trigger) |
| `project_context.json` Layer 7 | Origin Wound, Secret Doubt, Client War Stories, Victory Reliving, Red Line | VULNERABILITY + RECOGNITION |
| `soul_values.json` | Coach's ideology, enemies, beliefs | TENSION (what they believe vs mainstream) |
| `tribe_profile.json` | Audience pain points, fears, rituals | RECOGNITION (what the tribe feels but can't say) |

### Saturation Gate (Pre-Generation Check)

Before proceeding to Law 2, the system must pass this gate:

```
SATURATION GATE QUESTIONS:
1. "Does project_context.json Layer 6 contain ≥1 named Counter-Stance?"
   → NO = INSUFFICIENT (no contrarian positions to trigger TENSION)
   → YES = PASS

2. "Does intelligence_radar.json contain ≥3 friction points with trigger_archive_match?"
   → NO = INSUFFICIENT (not enough signals to generate provocations)
   → YES = PASS

3. "Does project_context.json Layer 7 contain ≥1 Origin Wound or Secret Doubt?"
   → NO = INSUFFICIENT (vulnerability questions will be generic)
   → YES = PASS
```

**If any gate fails:** The system flags the gap and requests additional intelligence collection before question generation proceeds.

---

## Law 2: 3-Mode Emotional Detection (via Archetype Routing)

### The Axiom (Upgraded)
*A question's value is proportional to the emotional trigger it activates. The CCF archetype determines the trigger.*

### How It Works in CCF

The Question Engineer already routes friction points to archetypes via `trigger_archive_match`:

```
recurring_sermon → CONTRARIAN         → TENSION
origin_wound     → VULNERABILITY PROBE → VULNERABILITY
client_war_stories → COMPASSION MIRROR → RECOGNITION
victory_reliving → COMPASSION MIRROR   → RECOGNITION
secret_doubt     → SHADOW EXPLORER     → VULNERABILITY × TENSION
red_line         → SHADOW EXPLORER     → VULNERABILITY × TENSION
```

**Law 2 adds the mode tag as an EXPLICIT field** in `provocation_questions.json`:

```json
{
  "id": "q_01",
  "archetype": "contrarian",
  "mode": "TENSION",
  "mode_justification": "Breaks the mainstream prediction about market timing",
  "pillar_id": "pillar_03",
  "friction_point_id": "fp_01",
  "question_text": "..."
}
```

### Mode Collision Types

**TENSION (CONTRARIAN archetype):**

| Collision | Example |
|:---|:---|
| Coach Belief vs Mainstream Advice | Coach preaches calm investing → Finance Twitter says panic-sell |
| Surface Advice vs Deeper Obstacle | "Just start saving" → Real blocker is inherited money shame |

**VULNERABILITY (VULNERABILITY PROBE + SHADOW EXPLORER archetypes):**

| Collision | Example |
|:---|:---|
| Public Image vs Private Doubt | Coach appears confident → Still questions their method privately |
| Competence vs Current Edge | Expert in X → Currently failing at Y in real-time |

**RECOGNITION (COMPASSION MIRROR archetype):**

| Collision | Example |
|:---|:---|
| Unnamed Feeling vs Specific Words | Tribe feels financial anxiety → Coach names it "money guilt inheritance" |
| Shared Ritual vs Underlying Reason | Tribe does Sunday meal prep → It's actually a control ritual |

**Critical guard-rail from Alchemy:** *"Demonstrated competence precedes permission to be uncertain."* VULNERABILITY PROBE and SHADOW EXPLORER questions are ONLY generated if `project_context.json` Layer 7 contains evidence of demonstrated competence (client results, testimonials). Otherwise, these archetypes are temporarily skipped.

---

## Law 3: Compression, Not Elimination

### The Axiom
*Distillation absorbs weaker questions into denser ones that activate multiple modes simultaneously.*

### What This Means for CCF

The Question Engineer currently generates 5-7 single-archetype questions. Law 3 adds a compression pass:

**Before compression (current CCF behavior):**
```
q_01: CONTRARIAN (TENSION only)
q_02: CONTRARIAN (TENSION only)
q_03: VULNERABILITY PROBE (VULNERABILITY only)
q_04: COMPASSION MIRROR (RECOGNITION only)
q_05: SHADOW EXPLORER (VULNERABILITY only)
```

**After compression (Law 3 applied):**
```
q_01: CONTRARIAN × COMPASSION MIRROR (TENSION + RECOGNITION)
  → "Everyone says 'just start saving' — but your client Sarah stopped
     crying in the shower after week 4 of your program. It wasn't about
     the savings. What was it ACTUALLY about?"

q_02: VULNERABILITY PROBE × CONTRARIAN (VULNERABILITY + TENSION)
  → "You tell your clients that relapse is part of growth — but was there
     a period YOU couldn't apply your own framework?"

q_03: SHADOW EXPLORER × COMPASSION MIRROR (V + T + R = triple-mode)
  → "What's the one thing about investing that you sometimes wonder about
     at 2am — and would your client who just lost 30% feel better or worse
     knowing you wonder too?"
```

### The Density Test
A properly compressed question makes the coach:
1. **Pause** — they haven't been asked this before (TENSION activated)
2. **Feel** — the question touches something personal (VULNERABILITY activated)
3. **Tell a specific story** — the only way to answer requires a lived detail (RECOGNITION activated)

### Compression Rules
- A compressed question must activate ≥2 modes (dual-mode minimum)
- Word limit: 60-100 words per compressed question
- The coach must need a SPECIFIC MEMORY to answer — not general knowledge
- Output batch after compression: 3-5 questions (compressed from 5-7)

---

## Law 4: The Unpredictability Gate

### The Axiom
*A question's quality is inversely proportional to the predictability of its answer.*

### The 4 Checks (applied per compressed question before delivery)

```
CHECK 1: "Could ChatGPT answer this with 5 words of context?"
  → YES = REJECT (no specific memory required, no first-party data accessed)
  → NO  = PASS

CHECK 2: "Could another coach in the same niche answer identically?"
  → YES = REJECT (no irreducible uniqueness — project_context not embedded)
  → NO  = PASS

CHECK 3: "Does the coach need a SPECIFIC memory, feeling, or client to answer?"
  → NO  = REJECT (theoretical, not experiential)
  → YES = PASS (first-party data accessed)

CHECK 4: "Would the coach's answer make someone in the tribe
          say 'How did you know that about me?'"
  → NO  = The question lacks RECOGNITION mode
  → YES = PASS — the specificity→universality bridge is operational
```

**If any check fails:** The question returns to compression. Failed questions are NOT delivered.

---

## Alchemy ↔ Laws Mapping

| Alchemy Principle | Law It Grounds | CCF Archetype |
|:---|:---|:---|
| Prediction Error | Law 2 | CONTRARIAN |
| Costly Signaling | Law 2 | VULNERABILITY PROBE |
| The Shadow | Law 2 | SHADOW EXPLORER |
| Specificity creates universality | Law 2, Law 3 | COMPASSION MIRROR |
| Vulnerability precedes connection | Law 2 | VULNERABILITY PROBE |
| Surprise requires understanding | Law 1, Law 2 | CONTRARIAN |
| Truth is recognized, not taught | Law 2, Law 4 | COMPASSION MIRROR |
| Emotion requires accuracy | Law 2, Law 3 | COMPASSION MIRROR |
| Information Gap | Law 2 | CONTRARIAN + SHADOW EXPLORER |
| Demonstrated competence precedes permission | Law 2 guard-rail | VULNERABILITY + SHADOW |
| Meaning emerges from constraint | Law 3 | Compression logic |

---

## The Full Distillation Cycle (v3 — CCF)

```
┌──────────────────────────────────────────────────────────┐
│                 LAW 1: SATURATION                         │
│  intelligence_radar.json + project_context.json           │
│  (Layer 6: Counter-Stance, Layer 7: Trigger Archive)      │
│  + soul_values.json + tribe_profile.json                  │
│  Gate: ≥1 Counter-Stance, ≥3 friction points, ≥1 wound   │
└────────────────────────┬─────────────────────────────────┘
                         ▼
┌──────────────────────────────────────────────────────────┐
│         LAW 2: 3-MODE DETECTION via ARCHETYPE ROUTING     │
│  friction_point → trigger_archive_match → archetype       │
│  CONTRARIAN → TENSION                                     │
│  VULNERABILITY PROBE → VULNERABILITY                      │
│  COMPASSION MIRROR → RECOGNITION                          │
│  SHADOW EXPLORER → VULNERABILITY × TENSION                │
│  Generate 5-7 mode-tagged provocation questions           │
└────────────────────────┬─────────────────────────────────┘
                         ▼
┌──────────────────────────────────────────────────────────┐
│       LAW 3: COMPRESSION                                  │
│  Merge across archetypes → 3-5 dual/triple-mode Qs       │
│  Each compressed Q activates ≥2 modes                     │
│  Word limit: 60-100 words per question                    │
└────────────────────────┬─────────────────────────────────┘
                         ▼
┌──────────────────────────────────────────────────────────┐
│       LAW 4: UNPREDICTABILITY GATE                        │
│  4 checks per question                                    │
│  PASS → Include in provocation_questions.json             │
│  FAIL → Return to compression for re-merge                │
└────────────────────────┬─────────────────────────────────┘
                         ▼
          ✅ 3-5 Final Questions → provocation_questions.json
```
