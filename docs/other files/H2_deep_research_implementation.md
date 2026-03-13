# H2 — Deep Research: First-Principles Implementation Architecture

**Pipeline Stage:** CMF Phase 1b → E-Roll Research (Blueprint → Research Plan → Deep Research Report → Search Queries)  
**Laws Applied:** 4 Laws of Research Distillation  
**Target Skill:** `skills/cmf/eroll/deep-researcher/SKILL.md` (+ 13 arc-specific variants in `skills/cmf/eroll/deep-researcher-{arc}/`)  
**Target Command:** `commands/cmf-eroll.md`  
**Related Skills:** `skills/cmf/eroll/cultural-introspector/SKILL.md`, `skills/cmf/eroll/query-generator/SKILL.md`  
**Input:** `beat_cluster.json` (narrative foundation) + `final_script.json` + `tribe_soul.json` + `strategy_brief.json` + `premise_analysis.json` + Brand Avatar  
**Output:** `{project_id}_ERoll_Deep_Research_Report.md` (emotionally typed, depth-stratified, 24+ findings)  
**Validation:** ✅ E-ROLL DEEP RESEARCH COMPLETE (Command completion marker)

---

## System Overview: What H2 Actually Does

The Deep Research stage (`cmf-eroll`, Steps 1-5) sits between the Beat Cluster phase (`cmf-beat-cluster`) and the E-Roll Query Generation phase (`cmf-eroll`, Step 7). Its function is to convert the narrative emotional arc of the video — already established in the diagnosis and script phases (`cmf-diagnose` → `cmf-script`), structured into beats via `beat_cluster.json` — into a body of **culturally specific, emotionally typed, depth-stratified research findings**. These findings provide the evidentiary foundation for the E-Roll Visual Search (H4) to source the standalone visual assets used in the final edit.

This is not general research. It is not "find images related to this topic." H2 research produces findings that are **narratively load-bearing**: every finding must prove, challenge, or illuminate something specific in the coach's story at a specific beat, in a specific emotional mode, at a specific depth layer.

The current pipeline (`skills/cmf/eroll/deep-researcher/SKILL.md`) produces 24+ named references with verified URLs, organized by beat and specialist mode across 5 research agents (Influencer Scout, Ethnographer, Journalist, Archivist, Symbol Hunter). This is structurally sound but emotionally blind. The Deep Research Report is a culturally rich pile of references — but the downstream agents (E-Roll Query Generator, Storyboard Composer) have to intuit which finding serves Tension, which serves Vulnerability, which serves Recognition. They do the emotional classification that H2 should have done.

The 4 Laws of Research Distillation close this gap permanently.

---

## Section 1: Input Quality Standards (Narrative Saturation Protocol)

Research that begins before the researcher understands the story's emotional terrain produces culturally accurate but narratively disconnected findings. The H2 input gate is not a file existence check — it is a **narrative comprehension test**. The researcher must be able to articulate the viewer's complete emotional journey before constructing a single search query.

### Required Input Files & Quality Standards

| # | Input Source | File / Field | Minimum Quality Standard |
|:--|:------------|:-------------|:------------------------|
| 1 | **Beat Cluster JSON** | `{project_id}_beat_cluster.json` — narrative foundation + beat routing | Required before E-Roll begins. Must contain VCP mini-stories and emotional registers (T/V/R). |
| 2 | **strategy_brief.json** | `{project_id}_strategy_brief.json` — unified frame, selected arc, thematic SPR | Researcher must articulate the **unified frame** in one sentence before researching |
| 3 | **premise_analysis.json** | `{project_id}_premise_analysis.json` — scene clusters, quotes per beat, timestamps | Researcher must know which emotional register each beat carries before construction |
| 4 | **final_script.json** | `{project_id}_final_script.json` — exact quotes + timestamps per scene | Every finding must map to a specific script moment per deep-researcher SKILL.md |
| 5 | **tribe_soul.json** | `tribe_soul.json` (Coach level) — cultural DNA: slang, heroes, unnamed feelings | Must contain ≥1 unnamed feeling and ≥1 cultural reference the tribe uses internally |
| 6 | **Brand Avatar** | `😎 {project_id} - The Brand Avatar 😎.md` — physical DNA, cultural anchors | Researcher must understand what markers symbolize culturally — not just describe them |

### Narrative Saturation Gate (Pre-Research Check)

Before any search query is constructed, the researcher must pass the following saturation interrogation. This is the equivalent of H0's Saturation Gate — it tests not file presence but narrative comprehension:

```
SATURATION GATE — Complete this sentence before any query is built:

"The viewer needs to feel _____ at beat W1, _____ at W2, _____ at W3,
 _____ at W4, and _____ at W5.

 The gap between what the tribe CURRENTLY BELIEVES and what the coach
 REVEALS is: _____.

 The one thing the tribe feels but cannot name — which this research
 must make visible — is: _____."

→ Cannot complete = NOT saturated. Research will produce illustrative
  but emotionally flat findings. STOP. Re-read all input files.
→ Can complete = PASS. Research will be emotionally directed.
```

**If the saturation gate fails:** The system does not proceed to research planning. The researcher re-engages with premise_analysis.json and tribe_soul.json until the sentence can be completed with precision.

---

## Section 2: Law Execution Protocol

### Law 1 — Narrative Saturation Before Searching

**Axiom:** *Research that is not saturated with the story's emotional terrain produces culturally accurate but narratively disconnected findings.*

**What it does:** Makes the researcher understand the emotional journey per beat BEFORE constructing any search query. The saturation is tested against the unified frame, not just the topic.

**Execution — Saturation Mapping per Beat:**

```
FOR EACH beat in premise_analysis.json:

  Declare:
  - EMOTIONAL REGISTER: What the viewer must FEEL at this beat
  - CURRENT BELIEF: What the tribe currently assumes about this topic
  - NARRATIVE GAP: The distance between the tribe's current assumption and what the coach reveals
  - VISUAL EVIDENCE NEEDED: What imagery would PROVE the gap to a viewer with no audio

  Example (W1 HOOK — Witness Arc):
  EMOTIONAL REGISTER: TENSION — the viewer's model is broken
  CURRENT BELIEF: "The medical system is imperfect but fundamentally trustworthy"
  NARRATIVE GAP: Coach reveals "the system was designed to dismiss this tribe's experience"
  VISUAL EVIDENCE: Documentation of institutional medical dismissal — not stock wellness imagery
```

**The Saturation Test (Law 1 Gate):**
> "Before your first search query, have you declared the exact NARRATIVE GAP that research must visually prove at each beat?"  
> → NO = research will produce thematic DECORATION, not narrative EVIDENCE  
> → YES = PASS — every query will target the gap, not the topic

---

### Law 2 — Emotional Mode Classification of Findings

**Axiom:** *A research finding's downstream value is proportional to its emotional specificity. Untyped findings force downstream agents to do the emotional work that research should have done.*

**What it does:** Every finding in the Deep Research Report receives a `mode` tag (T/V/R) in addition to its beat tag and specialist mode tag. The report's batch is validated for mode diversity before it is considered complete.

**Mode Classification Protocol — Finding Level:**

| Mode | The Finding Makes the Viewer... | Specialist Mode Affinity | Example Finding |
|:-----|:--------------------------------|:------------------------|:----------------|
| **TENSION (T)** | "I didn't know that was happening" | Journalist (wounds documented), Archivist (historical evidence of enemy) | Documentary footage of medical racial bias in French emergency rooms — naming the institutional failure |
| **VULNERABILITY (V)** | "They went through that too" | Ethnographer (survival rituals), Influencer Scout (trusted figures showing struggle) | Tatiane Van Laethem discussing her own health crisis before building her practice |
| **RECOGNITION (R)** | "That's MY reality — exactly" | Ethnographer (daily objects), Symbol Hunter (tribal visual codes) | Kinkeliba tea prepared in an everyday kitchen — chipped cup, morning light, ritual not ceremony |

**Classification Test (per finding):**
> "This finding documents _____ (what) and serves _____ mode (why) because it makes the viewer feel _____ (how)."  
> → If you can fill "what" but not "why" or "how" = the finding is descriptive but emotionally unclassified. Reclassify before including.  
> → All three filled = PASS. Downstream agents have emotional instruction built in.

**Batch Diversity Gate:**
```
MINIMUM BATCH COVERAGE:
  ≥7 TENSION findings (documents the enemy, the wound, the institutional failure)
  ≥7 RECOGNITION findings (documents the tribe's lived reality, their unnamed rituals)
  ≥5 VULNERABILITY findings (documents cost, struggle, real price of the journey)
  ≥5 MULTI-MODE findings (serve two modes simultaneously)

FAIL STATE:
  18+ findings untyped or clustering in one mode = emotional monotone research.
  The visual story will be one-note regardless of how culturally specific the references are.
```

---

### Law 3 — Depth Stratification, Not Breadth Accumulation

**Axiom:** *A research finding's creative power is proportional to its depth layer. Surface findings illustrate; mechanism findings explain; collision findings transform.*

**What it does:** Assigns every research question to a depth layer before it is executed. Each beat must have coverage at all three depths before the research plan is considered complete.

**The 3-Layer Architecture:**

| Layer | Name | Question Type | What It Produces |
|:------|:-----|:-------------|:-----------------|
| **L1** | Surface | "What exists?" | Illustrative references — imagery that SHOWS the tribal world |
| **L2** | Mechanism | "Why does it work this way?" | Explanatory references — imagery/docs that REVEAL the underlying dynamic |
| **L3** | Collision | "Where does it break or contradict itself?" | Provocative references — imagery/docs that CREATE TENSION between belief and reality |

**Depth Example (W1 HOOK beat — naturopath tribe):**

```
L1 (Surface): "Who are the wellness influencers this tribe follows?"
→ Returns: Profile photos, branded content, aesthetic imagery
→ Visual function: SHOWS the tribe's aspirational world

L2 (Mechanism): "Why does this tribe trust social media naturopaths over doctors?
  What institutional failure drives this trust?"
→ Returns: Investigative journalism, patient advocacy testimony, medical complaint records
→ Visual function: REVEALS WHY the tribe moved to alternative practitioners

L3 (Collision): "Where have wellness figures this tribe trusts given advice that
  was later debunked or harmful? What is the cost of the trust the coach asks for?"
→ Returns: Regulatory warnings, community debates, fact-checks
→ Visual function: BREAKS the viewer's simple narrative — even the alternative path has risk
```

**The Depth Coverage Gate (per beat):**
```
CHECK: "Does this beat have at least one L2 finding AND at least one L3 finding?"
  → Only L1 coverage = visual story will ILLUSTRATE but never SURPRISE
  → L2 + L3 present = PASS. The Storyboard Composer (`skills/cmf/composers/`) has depth to work with.
```

**Why L3 is the most critical layer:**  
L1 research produces B-roll that validates the world. L2 research produces B-roll that explains it. Only L3 produces B-roll that **breaks the viewer's expectation** — the visual prediction error that makes the brain wake up and pay attention. Without L3, the video is informative. With L3, it is transformative.

**Depth Distribution Requirement:**
```
Per beat, minimum:
  ≥2 L1 findings (contextual grounding)
  ≥2 L2 findings (mechanism exposure)
  ≥1 L3 finding (collision/contradiction)

Over the full report (5 beats × minimum):
  ≥10 L1 | ≥10 L2 | ≥5 L3
```

---

### Law 4 — The Narrative Provenance Gate

**Axiom:** *A research finding's value is inversely proportional to how discoverable it is without the coach's specific story.*

**What it does:** Tests every finding for narrative load-bearing status — not just cultural specificity. The current forbidden terms list catches generic TERMS. The Provenance Gate catches narratively generic FINDINGS: queries that were specific but returned emotionally interchangeable results.

**The 4 Provenance Checks (applied per finding):**

```
CHECK 1: Story-Dependency Test
  "Could a researcher who never read this coach's transcript find
   this same reference by searching generic wellness/demographic terms?"
  → YES = REJECT — culturally valid, narratively disconnected
  → NO  = PASS — requires knowledge of THIS story to find

CHECK 2: Script-Mapping Test
  "Does this finding map to a SPECIFIC quote or timestamp in the final script?"
  → NO  = REJECT — thematic decoration, not evidentiary
  → YES = PASS — finding serves a specific narrative moment

CHECK 3: Irreplaceability Test
  "If this finding were removed, would the beat's visual story
   lose something that cannot be substituted from another finding?"
  → NO  = The finding is supplementary, collect it but don't prioritize it
  → YES = PASS — the finding is load-bearing for the beat

CHECK 4: Emotional Non-Redundancy Test
  "Does this finding create an emotional response that is DIFFERENT
   from the other findings in the same beat?"
  → NO  = REJECT — two findings producing the same emotional response
           at the same beat doubles the quantity, halves the impact
  → YES = PASS — the beat's finding set creates a layered emotional progression
```

**The Key Distinction (Provenance Gate vs. Forbidden Terms List):**

| Filter | What It Catches | What It Misses |
|:-------|:----------------|:---------------|
| **Forbidden Terms List** | Query: "african woman" → REJECT | Query: "Kinkeliba tea preparation" → PASS (but the finding is a magazine stock shot) |
| **Provenance Gate** | Catches the magazine stock shot — it passes the term check but fails the Story-Dependency test | Nothing — it validates the FINDING, not just the query |

The forbidden terms list is a query-level filter. The Provenance Gate is a finding-level filter. Both are required; only the Provenance Gate catches what survives the terms filter but remains emotionally generic.

---

## Section 3: Output Format — Typed Research Report

After Law 4, the Deep Research Report is restructured to carry emotional intelligence:

```markdown
## W1 BEAT ASSETS — HOOK (TENSION Primary)

### Finding W1-T-01 [MODE: TENSION | DEPTH: L3 | LOAD-BEARING: YES]
**Reference:** [Named reference + institution]  
**URL:** [Verified URL]  
**Why This Finding:** Documents medical dismissal of African-diaspora patient complaints —
  directly maps to quote: "[coach timestamp quote]"  
**Visual Instruction:** TENSION — breaks viewer assumption about institutional fairness  
**Script Mapping:** SC01 / W1 / 00:01-00:09  

### Finding W1-R-01 [MODE: RECOGNITION | DEPTH: L1 | LOAD-BEARING: YES]
**Reference:** [Named reference]
**URL:** [Verified URL]
**Why This Finding:** Kinkeliba preparation — everyday kitchen, non-aspirational —
  the tribe recognizes THIS version of their ritual, not the magazine spread version
**Visual Instruction:** RECOGNITION — viewer says "that's mine"
**Script Mapping:** SC02 / W1 / 00:09-00:15
```

**New fields in `ERoll_Search_Queries.json`:**
```json
{
  "id": "W1_Q1",
  "query": "Kinkeliba thé longue vie African morning ritual kitchen",
  "beat": "W1",
  "mode": "RECOGNITION",
  "depth_level": "L1",
  "provenance_checks": {
    "story_dependency": "PASS",
    "script_mapping": "SC02 / 00:09",
    "irreplaceable": "PASS",
    "non_redundant": "PASS"
  },
  "source_reference": "[Named finding]",
  "source_url": "[Verified URL]"
}
```

---

## Section 4: Evaluation — 5 Micro-Hypothesis Tests

Before the Deep Research Report is approved for query generation, the following 5 micro-hypotheses are tested against the full finding set.

### MH1 — The Saturation Comprehension Test
**Hypothesis:** "The researcher can articulate the viewer's complete emotional journey (beat by beat) and the specific narrative gap research must visually prove — without re-reading the strategy_brief."  
**Test:** After research planning is complete but before any query is executed, the researcher completes the Saturation Gate sentence from memory. Can they name: (a) the emotional register per beat, (b) the tribe's current belief, (c) the narrative gap?  
**Pass condition:** All 5 beats have a declared emotional register, current belief, and narrative gap. If any beat lacks a gap declaration, research for that beat will produce illustration-only findings.

### MH2 — The Mode Diversity Test
**Hypothesis:** "The 24+ findings cover all 3 emotional modes with the minimum batch distribution."  
**Test:** Count findings by mode tag: T-count, V-count, R-count, multi-count.  
**Pass condition:** ≥7 TENSION | ≥7 RECOGNITION | ≥5 VULNERABILITY | ≥5 MULTI. If any mode is under minimum, the finding set is emotionally monotone and must be supplemented before approval.

### MH3 — The Depth Coverage Test
**Hypothesis:** "Every beat in the script has at least one L2 finding and at least one L3 finding."  
**Test:** For each beat (W1-W5 or equivalent), check the depth layer distribution: L1 count, L2 count, L3 count.  
**Pass condition:** ≥1 L2 and ≥1 L3 per beat. Any beat with only L1 findings produces a visually illustrative segment with no surprise capability — the viewer's brain never wakes up.

### MH4 — The Load-Bearing Test
**Hypothesis:** "At least 15 of the 24+ findings are load-bearing — their removal would leave a specific beat's visual story incomplete."  
**Test:** Apply CHECK 3 (Irreplaceability) from the Provenance Gate to every finding. Mark as: LOAD-BEARING vs SUPPLEMENTARY.  
**Pass condition:** ≥15/24 findings are load-bearing. If fewer than 15 are load-bearing, the research has produced a surplus of illustrative decoration and a deficit of evidentiary material. The downstream composer will be working from a weaker foundation than the pipeline requires.

### MH5 — The Downstream Utility Test
**Hypothesis:** "A storyboard composer who has never read the transcript can open the Deep Research Report and immediately know: (a) which finding serves which beat, (b) which emotional mode each finding activates, (c) at what narrative depth each finding operates."  
**Test:** Simulate the composer handoff: given only the typed Deep Research Report (with mode tags, depth levels, load-bearing flags, and script mappings), can the Storyboard Composer (`skills/cmf/composers/`) make all visual decisions without re-reading premise_analysis.json or tribe_soul.json?  
**Pass condition:** Every finding has enough metadata (mode, depth, script_mapping, why_this_finding) that the composer's decisions are constrained by the research — not left to improvisation. If the composer must guess about mode or depth for any finding, the report has failed its downstream utility test.

---

## Section 5: H2 Completion & Asset Delivery

Upon completion of the full H2 protocol, the system confirms the output is ready for the **E-Roll Search Query Generation**. No search queries are generated without the verified Deep Research Report.

```markdown
✅ E-ROLL DEEP RESEARCH COMPLETE

Files Created:
├── {project_id}_research_plan.json (12 questions from arc skill)
├── {project_id}_ERoll_Deep_Research_Report.md
└── {project_id}_ERoll_Search_Queries.json (Step 7)
```

**Completion Metrics Tracking:**
- **Narrative Gap declared** per beat (`beat_cluster.json` alignment)
- **Tribe unnamed feeling** identified and documented
- **Mode Diversity Score** (T:7 | R:7 | V:5 minimum)
- **Depth Stratification Yield** (L2+L3 present at every beat)
- **Load-Bearing Ratio** (≥15/24 findings pass provenance checks)


---

## Architectural Constants

| Constant | Value | Rationale |
|:---------|:------|:----------|
| Minimum findings | 24 | Existing pipeline standard — maintained |
| Mode diversity (T) | ≥7 | Sufficient to cover 5 beats without tension clustering |
| Mode diversity (V) | ≥5 | Vulnerability is hardest to find — dedicated minimum enforces depth |
| Mode diversity (R) | ≥7 | Recognition is the highest-frequency mode for tribal resonance |
| Depth layers | L1 + L2 + L3 per beat | L3 is the non-negotiable — without collision, no prediction error |
| Load-bearing findings | ≥15/24 | More than half must earn their place narratively, not just culturally |
| Saturation gate | Mandatory pre-research | No query is built until the narrative gap is declared |

---

## Referenced CMF Skills & Commands

| Type | Name | Path |
|:-----|:-----|:-----|
| **Skill** | Deep Researcher V2 (generic) | `skills/cmf/eroll/deep-researcher/SKILL.md` |
| **Skill** | Deep Researcher — Witness (arc-specific) | `skills/cmf/eroll/deep-researcher-witness/SKILL.md` |
| **Skill** | Deep Researcher — Breakthrough | `skills/cmf/eroll/deep-researcher-breakthrough/SKILL.md` |
| **Skill** | Deep Researcher — (+11 more arc variants) | `skills/cmf/eroll/deep-researcher-{arc}/SKILL.md` |
| **Skill** | Cultural Introspector | `skills/cmf/eroll/cultural-introspector/SKILL.md` |
| **Skill** | E-Roll Query Generator | `skills/cmf/eroll/query-generator/SKILL.md` |
| **Command** | cmf-eroll | `commands/cmf-eroll.md` |
| **Command** | cmf-beat-cluster (upstream) | `commands/cmf-beat-cluster.md` |
| **Downstream** | Final Video Edit | E-Roll assets sourced via H4 for standalone use in edit |

*Next Document: [H3 — Stream of Consciousness: 4 Laws of Voice Distillation Implementation Architecture]*
