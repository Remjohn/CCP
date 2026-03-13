# H6: RAW Deep Research (CCF) — Implementation Architecture

**Hypothesis:** The 41 deep research analyst skills produce 1600-2200 word dossiers organized by 7 intellectual angles but without emotional mode classification, source depth stratification, or beat-mode alignment. Research arrives at the script generator as a knowledge dump, not as emotionally pre-routed intelligence.

**Pipeline Position:** CCF Research Phase → Deep Analyst → Deep Research Dossier → feeds Script/Visual pipeline  
**Existing Infrastructure:** `_DEEP_RESEARCH_PROTOCOL.md` (5-phase agentic loop), 41 archetype-specific `deep-analysts/` skills  
**Gap Classification:** MEDIUM — Infrastructure is sophisticated (Strategy Director + Critic Loop + Firecrawl), but outputs lack emotional and depth metadata  
**Dependency:** Receives blueprint from H1 (Blueprint Orchestrator), soul_values from H8/H10

---

## Section 1: The Input Quality Problem

The Deep Research Protocol already has a strong query-generation and quality-control loop (Strategy Director → Firecrawl → Critic → Synthesis). The problem is not in the EXECUTION of research but in the METADATA of findings. A finding that passes the Critic Loop ("not generic, primary source, soul-aligned") still arrives at the script generator without:

1. **Mode tag:** Which emotional function does this finding serve?
2. **Depth level:** Is this a surface illustration, mechanism explanation, or worldview collision?
3. **Beat target:** Which content section is this finding meant to fuel?

### Input Saturation Gate

| Input | Minimum Requirement | Source |
|:------|:-------------------|:-------|
| `content_blueprints.json` | Must contain `mode_primary` per blueprint (from H1) | Blueprint Orchestrator output |
| `soul_values.json` | Must be loaded for Tone Emulation Protocol | H8/H10 output |
| Strategy Director output | `conscious_research_plan.json` with 7-angle queries | Strategy Director skill |

**Saturation test:** The Strategy Director must receive the blueprint's MODE assignment as input. If blueprints.json contains no `mode_primary` field, research proceeds mode-blind — technically functional but emotionally unrouted.

---

## Section 2: The 4 Laws of Deep Research Distillation

### Law 1 — Research Emotional Typing

**Axiom:** *Research without emotional classification is ammunition without a target.*

Every finding across all 7 angles must be tagged: `mode` (T/V/R), `mode_justification`, and `deployment_recommendation`.

**Classification Test (per finding):**
```
"This finding documents _____ (what) and serves _____ mode (why)
 because it makes the viewer feel _____ (how)."

→ All three filled = PASS
→ Can fill "what" but not "why"/"how" = descriptive but emotionally unclassified → RECLASSIFY
```

**Batch Mode Diversity Gate:**
```
FOR the full dossier:
  COUNT findings tagged TENSION
  COUNT findings tagged VULNERABILITY
  COUNT findings tagged RECOGNITION

IF any mode has ZERO findings:
  → FLAG: "Research gap in [MODE] — dossier lacks [T/V/R] ammunition"
  → Critic issues "Dig Deeper Directive" targeting the missing mode
```

**Where this integrates:** Phase 4 (Synergist) — Synergy Map gains `mode` column per finding. Phase 3 (Critic) gains mode-diversity check as batch validation.

### Law 2 — Source Depth Stratification

**Axiom:** *A news article and a longitudinal study cannot have the same weight.*

Every approved finding gains a `depth_level`:
- **L1 (Surface):** Summaries, news, commentary — ILLUSTRATES but doesn't PROVE
- **L2 (Mechanism):** Studies, methodologies, expert analyses — EXPLAINS the underlying dynamic
- **L3 (Collision):** Findings that challenge or complicate the coach's stated position — SURPRISES the viewer

**Depth Coverage Gate (per angle):**
```
CHECK: "Does this angle have at least one L2 finding?"
  → Only L1 = dossier will illustrate but never prove
  → L2 present = PASS
  → L3 present = BONUS — the dossier has depth to create productive tension
```

**Minimum thresholds:** ≥30% L2, ≥10% L3 across the full dossier. Below threshold triggers Critic "Dig Deeper Directive" with specific depth instruction.

**Where this integrates:** Phase 3 (Critic Loop) adds depth assessment alongside existing generic/primary/soul-alignment checks.

### Law 3 — Beat-Mode Alignment

**Axiom:** *Research that doesn't know its destination arrives everywhere and serves nowhere.*

The Strategy Director receives the blueprint's mode assignments as additional input:

```json
{
  "research_plan": {
    "blueprint_id": "B001",
    "archetype": "top-reliable-list",
    "mode_assignments": {
      "opening": "TENSION",
      "core_strategy_1": "RECOGNITION",
      "proof_section": "VULNERABILITY",
      "closing": "RECOGNITION"
    },
    "queries": [
      {
        "id": "Q1",
        "angle": "Scientific",
        "target_mode": "TENSION",
        "target_section": "opening",
        "query": "..."
      }
    ]
  }
}
```

**Where this integrates:** Strategy Director's `conscious_research_plan.json` gains `target_mode` and `target_section` fields per query.

### Law 4 — Research Authenticity Gate

**Axiom:** *If a competitor could use this finding without changing a word, it's not tribal research — it's a Google search.*

**4 Gate Checks (per finding):**

```
CHECK 1: Tribe-Invisible Detail Test
  "Does this finding contain detail invisible to an outsider but obvious to the tribe?"
  → NO = SUPPLEMENTARY (usable but not differentiating)
  → YES = LOAD-BEARING (this finding IS the story)

CHECK 2: Depth Distribution
  "Does the batch have ≥30% L2, ≥10% L3?"
  → BELOW = Critic "Dig Deeper Directive"

CHECK 3: Mode Coverage
  "Does the batch span all 3 modes (T/V/R)?"
  → MISSING MODE = FLAG + targeted research directive

CHECK 4: Soul-Challenge Presence
  "Is there ≥1 finding that CHALLENGES the coach's stated position?"
  → NO = Research is echo-chamber (validating but not deepening)
  → YES = PASS — the dossier has intellectual honesty
```

**Where this integrates:** Phase 3 (Critic Loop) as batch-level final validation before proceeding to Phase 4 (Synthesis).

---

## Section 3: Output Format Enhancement

```
Deep_Research_Dossier.md (enhanced)

├── Executive Summary
│   ├── One Big Idea
│   └── mode_coverage: { T: n findings, V: n, R: n }
│
├── 7-Angle Analysis (200-300 words each)
│   └── Per finding:
│       ├── content (existing)
│       ├── mode: T | V | R
│       ├── mode_justification: "..."
│       ├── depth_level: L1 | L2 | L3
│       ├── tribe_invisible: YES | NO
│       └── verified_url (existing)
│
├── Synergy Map (existing — enhanced)
│   └── Per connection: mode routing (how this synergy serves a specific mode)
│
├── Trend Signals (existing)
│
└── RESEARCH AUTHENTICITY GATE RESULTS
    ├── tribe_invisible_count: n / total
    ├── depth_distribution: L1: x%, L2: y%, L3: z%
    ├── mode_distribution: T: n, V: n, R: n
    └── soul_challenge_present: YES/NO
```

---

## Section 4: 5 Micro-Hypothesis Evaluations

**MH1 — Mode Diversity Test:** Count findings per mode. All 3 modes must have ≥1 finding. Verifiable: parse the dossier mode tags and count.

**MH2 — Depth Distribution Test:** Calculate L1/L2/L3 percentages. ≥30% L2 and ≥10% L3 required. Verifiable: parse depth_level tags and compute ratios.

**MH3 — Tribe-Invisible Detail Test:** Count findings marked `tribe_invisible: YES`. ≥20% of findings should contain tribe-invisible detail. Verifiable: count against total findings.

**MH4 — Beat-Mode Alignment Test:** For each finding, check if `mode` matches `target_section`'s mode assignment from the blueprint. ≥70% alignment = PASS. Verifiable: cross-reference finding mode against blueprint mode_assignments.

**MH5 — Soul-Challenge Presence:** Confirm ≥1 L3 finding challenges the coach's stated position. Verifiable: check L3 findings for contradiction with soul_values core beliefs.

---

## Validation Receipt

```
H6 VALIDATION RECEIPT
━━━━━━━━━━━━━━━━━━━━━
Blueprint:       [ID]
Archetype:       [type]
Coach:           [name]
Date:            [timestamp]
Queries:         [n] executed across [7] angles

LAW COMPLIANCE
━━━━━━━━━━━━━━
Law 1 — Emotional Typing:     [T: n, V: n, R: n]  [PASS/FAIL if missing mode]
Law 2 — Depth Stratification:  [L1: x%, L2: y%, L3: z%]  [PASS/FAIL if L2<30% or L3<10%]
Law 3 — Beat-Mode Alignment:   [n/total aligned]  [PASS/FAIL if <70%]
Law 4 — Authenticity Gate:     [4/4 checks]  [PASS/FAIL]

MICRO-HYPOTHESES
━━━━━━━━━━━━━━━━
MH1 Mode Diversity:        [PASS/FAIL]
MH2 Depth Distribution:    [PASS/FAIL]
MH3 Tribe-Invisible:       [n/total = x%]  [PASS/FAIL if <20%]
MH4 Beat Alignment:        [n/total = x%]  [PASS/FAIL if <70%]
MH5 Soul Challenge:        [PRESENT/ABSENT]

STATUS: [AUTHENTICATED / PROVISIONAL / FAILED]
```
