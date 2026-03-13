# H10: Coach Philosophy Brief — Implementation Architecture

**Hypothesis:** The Coach Philosophy Brief is the deepest, most layered representation of a coach's worldview, narrative identity, and belief system. It is the upstream intelligence source that every downstream stage implicitly depends on — yet it does not exist.

**Pipeline Position:** CCF Setup Phase → feeds H1 (Blueprint), H3 (SoC Generator), H8 (Soul Values), all scripts  
**Existing Infrastructure:** `Conscious_Soul_Values.md` (48 lines, static extraction from 1 transcript)  
**Gap Classification:** CRITICAL — Complete structural absence  
**MCDA Score:** 9.15 / 10 (Rank #1)

---

## Section 1: The Input Quality Problem

The Coach Philosophy Brief requires inputs that go beyond a single transcript. A coach who has recorded 12 interviews has revealed 12 different facets of their philosophy — contradictions, evolutions, deepening convictions, abandoned beliefs, stories they've told from different angles. Currently, the pipeline processes one transcript and freezes the result into `Conscious_Soul_Values.md`. The other 11 transcripts are never systematically mined for philosophical depth.

### Input Saturation Gate

Before the Philosophy Brief can be written, the following inputs must be verified as present and sufficient:

| Input | Minimum Requirement | Source |
|:------|:-------------------|:-------|
| Coach transcripts | ≥ 2 (initial setup); accumulated over monthly cycle | Interview recordings, voice notes, live sessions |
| Existing `soul_values.json` | Must be loaded for baseline values, metaphors, vocabulary | Setup phase output |
| Content theme definitions | Current content themes the coach is producing around | `content_themes.json` |
| Previous Philosophy Brief | If exists (monthly update cycle), load for evolution tracking | Previous cycle output |

**Saturation test:** If only 1 transcript is available, the Philosophy Brief runs in BOOTSTRAP mode — producing a first-pass brief that is explicitly marked as provisional. If ≥ 2 transcripts are available, the Brief runs in LAYERED mode — cross-referencing beliefs, stories, and values across sources to detect depth, contradictions, and evolution.

---

## Section 2: The 4 Laws of Philosophy Distillation

### Law 1 — Depth Stratification

Every extracted belief, value, or narrative from the coach's transcripts must be classified into one of three depth layers:

- **L1 — Surface Beliefs:** What the coach says publicly and consistently. Their stated mission, explicit values, market positioning. Example: *"La santé des afrodescendants ne peut être traitée avec les protocoles médicaux standards."* This is what the coach says on stage.

- **L2 — Mechanism Beliefs:** Why the coach holds this belief — the reasoning layer, the lived experience behind the conviction, the specific moments that forged the belief. Example: *"Because my own integration in Europe nearly destroyed my health before I understood that my body was not designed for this climate's bacteria."* This is WHY they believe it.

- **L3 — Collision Beliefs:** Where the coach's philosophy has been tested by reality and either survived, adapted, or been abandoned. Where their stated values contradict their behavior. Where two deeply held beliefs create tension with each other. Example: *"I tell my clients to honor their African food traditions — but I myself had to abandon some of those traditions to survive my first winter in France."* This is where the philosophy has scars.

**Every belief extracted must carry its depth tag.** A Philosophy Brief that contains only L1 beliefs is a marketing document, not a philosophy brief. The minimum depth requirement: ≥ 30% of extracted beliefs at L2, ≥ 10% at L3.

### Law 2 — Story Inventory with Mode Tags

The Philosophy Brief is not just a belief system — it is a **narrative inventory.** Every coach has stories they tell to illustrate their beliefs. These stories are the raw material that H3 (SoC Generator) will later transform into voice, that H1 (Blueprint) will use for decisive claims, and that scripts will reference for emotional resonance.

Each extracted story must be tagged with:

- **Emotional mode:** TENSION (the story creates conflict/urgency), VULNERABILITY (the story reveals personal cost/failure), or RECOGNITION (the story connects to shared tribal experience)
- **Depth layer:** Which layer of belief does this story illustrate?
- **Repetition index:** Has the coach told this story in multiple transcripts? If yes, it's a **signature story** — part of the coach's core narrative identity. If told only once, it's a **peripheral story** — potentially powerful but not yet established.
- **Evolution tracking:** Has the story changed across tellings? Different details, different emotional emphasis, different conclusions? The evolution itself is L3 intelligence.
- **Deployment tracking:** `deployment_count` (times used in content), `last_used_date`, `last_used_in` (blueprint ID). Tracks freshness.
- **Staleness flag:** `staleness_flag: true` when `deployment_count > 3` in the same quarter. Stale stories are DEPRIORITIZED — the system must find fresh alternatives first.

**Minimum story count:** ≥ 8 stories for BOOTSTRAP mode, ≥ 15 for LAYERED mode.

**The Staleness Gate (Boredom Ban):**

```
BEFORE deploying a story to a new blueprint:
  1. Check deployment_count for this quarter
  2. IF > 3 → story is STALE. Search inventory for an alternative in the same mode.
  3. IF no alternative exists → FLAG for coach interview:
     "We've used [story_title] 4 times. Got a new angle or a different story?"
  4. IF ALL available stories in the required mode are stale → 
     TRIGGER PatternWeaver extension to search for cross-domain story
     analogies from the coach's wider experience that haven't been deployed.

NOVELTY IS NON-NEGOTIABLE. Repetition = boredom. Boredom = death of resonance.
```

### Law 3 — Contradiction Mapping

A coach's philosophy contains contradictions. These are not bugs — they are **the most important signals in the brief.** A philosophy without contradictions is either shallow or dishonest.

The Contradiction Map identifies:

1. **Value tensions:** Two stated beliefs that create conflict when applied simultaneously. Example: "Honor your African food traditions" + "Adapt to your local environment's bacteria" — these two values are in productive tension.

2. **Story-belief mismatches:** A story the coach tells that actually undermines a stated belief. Example: The coach advocates for community-based healing but tells a story of healing alone in exile. The contradiction reveals a deeper, more nuanced truth.

3. **Evolution artifacts:** Beliefs that the coach held in early transcripts but has since modified or abandoned. These show philosophical growth and are L3 gold.

**The contradiction map is not about exposing hypocrisy.** It is about surfacing the complexity that makes the coach's voice authentic and irreplaceable. A Philosophy Brief that presents a clean, contradiction-free philosophy is a brochure, not intelligence.

### Law 4 — Philosophy Authenticity Gate

Before the Philosophy Brief is finalized, it must pass 4 checks:

1. **First-party verification:** Every belief, story, and contradiction traces to a specific moment in a specific transcript (with timestamp or quote). No inferred beliefs. No statements the coach "probably" believes.

2. **Depth distribution:** ≥ 30% L2 beliefs, ≥ 10% L3 beliefs. If these thresholds are not met, the brief is flagged as SHALLOW.

3. **Mode coverage:** The story inventory must contain stories tagged with all three modes (T/V/R). If one mode is missing, the brief flags which mode is absent — this signals a gap in the coach's narrative vulnerability that future interviews should address.

4. **Evolution readiness:** The brief must include a section explicitly flagging what should be explored in the next monthly update. What stories need more depth? What contradictions need clarification? What beliefs seem to be in flux? This ensures the monthly cycle has a clear mission.

---

## Section 3: The Monthly Update Loop

The Philosophy Brief is a **living document.** After the initial BOOTSTRAP or LAYERED creation, it enters a monthly refinement cycle:

```
Month 1: BOOTSTRAP Brief (from 1-2 transcripts)
  → Marked as provisional
  → Evolution section flags gaps

Month 2: New transcript(s) processed
  → Cross-referenced against existing brief
  → New stories added to inventory
  → Contradictions updated
  → Depth layers re-evaluated
  → Evolution tracked: what changed? what deepened? what was abandoned?

Month N: Brief becomes increasingly rich
  → Signature stories stabilize (high repetition index)
  → Contradictions resolve or deepen
  → L3 beliefs accumulate as the coach's philosophy matures
```

**Each update produces a version-stamped brief.** The previous version is archived, not overwritten. This creates a historical record of the coach's philosophical evolution — itself a valuable content source.

---

## Section 4: Output Format

The Philosophy Brief produces a structured markdown document:

```
coach_philosophy_brief_v{N}.md

├── METADATA
│   ├── Coach name, version, date, transcript sources
│   ├── Mode: BOOTSTRAP | LAYERED
│   └── Depth distribution: L1: X%, L2: Y%, L3: Z%
│
├── CORE BELIEFS (depth-stratified)
│   ├── L1 — Surface Beliefs (stated, consistent, public)
│   ├── L2 — Mechanism Beliefs (why they believe, evidence from experience)
│   └── L3 — Collision Beliefs (where philosophy was tested by reality)
│
├── STORY INVENTORY (mode-tagged, deployment-tracked)
│   ├── Signature Stories (repetition index ≥ 2)
│   └── Peripheral Stories (single occurrence)
│   Each: { story_id, mode, depth_layer, transcript_source, evolution_notes,
│           deployment_count, last_used_date, last_used_in, staleness_flag }
│
├── CONTRADICTION MAP
│   ├── Value Tensions
│   ├── Story-Belief Mismatches
│   └── Evolution Artifacts
│
├── VOICE DNA (extracted from across transcripts)
│   ├── Recurring metaphors (with frequency)
│   ├── Emotional vocabulary (expanded from soul_values)
│   └── Internal temperature by topic (updated)
│
└── EVOLUTION AGENDA (for next monthly cycle)
    ├── Gaps to explore
    ├── Beliefs in flux
    └── Stories needing deeper telling
```

---

## Section 5: 5 Micro-Hypothesis Evaluations

**MH1 — Depth Distribution Test:** Extract all beliefs from the brief. Calculate L1/L2/L3 percentages. If L2 < 30% or L3 < 10%, the brief fails the depth test and requires additional transcript processing. This verifiable: count the tagged beliefs and compute ratios.

**MH2 — Story Mode Coverage Test:** Count stories per mode (T/V/R). If any mode has zero stories, the brief flags a gap. This is verifiable but also actionable — the gap becomes a question for the next coach interview (feeds back to H0 Layered Questions).

**MH3 — Contradiction Density Test:** A brief with zero contradictions is suspicious. Count value tensions, story-belief mismatches, and evolution artifacts. If total < 2, the brief is likely SHALLOW and operating only at L1. This is verifiable: count the items in the contradiction map.

**MH4 — First-Party Provenance Test:** Randomly select 5 beliefs and 3 stories from the brief. Each must trace to a specific timestamp or verbatim quote from a specific transcript. If any cannot be traced, the brief fails provenance. This is verifiable: check the source references.

**MH5 — Downstream Utility Test:** Take the completed Philosophy Brief and feed it to the H1 Blueprint Orchestrator alongside a content theme. Does the Blueprint produce a more specific decisive claim than it would with only `soul_values.json`? Does the SoC Generator (H3) find more vulnerability source material? This is verifiable: compare output quality with and without the brief.

---

## Validation Receipt

```
H10 VALIDATION RECEIPT
━━━━━━━━━━━━━━━━━━━━━
Coach:           [name]
Version:         [N]
Mode:            [BOOTSTRAP | LAYERED]
Transcripts:     [count] sources processed
Date:            [timestamp]

LAW COMPLIANCE
━━━━━━━━━━━━━━
Law 1 — Depth Stratification:    [L1: X% | L2: Y% | L3: Z%]  [PASS/FAIL]
Law 2 — Story Inventory:         [count] stories, modes: [T:n V:n R:n]  [PASS/FAIL]
Law 3 — Contradiction Map:       [count] items  [PASS/FAIL if < 2]
Law 4 — Authenticity Gate:       [4/4 checks passed]  [PASS/FAIL]

MICRO-HYPOTHESES
━━━━━━━━━━━━━━━━
MH1 Depth Distribution:    [PASS/FAIL]
MH2 Mode Coverage:         [PASS/FAIL] — missing modes: [list]
MH3 Contradiction Density: [PASS/FAIL]
MH4 Provenance:            [5/5 beliefs, 3/3 stories verified]
MH5 Downstream Utility:    [Tested against H1/H3: improvement noted: Y/N]

EVOLUTION AGENDA
━━━━━━━━━━━━━━━━
Gaps:            [list]
Beliefs in flux: [list]
Next update:     [date]

STATUS: [AUTHENTICATED / PROVISIONAL / FAILED]
```
