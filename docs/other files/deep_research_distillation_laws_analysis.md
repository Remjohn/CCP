# First-Principles Analysis: What H2 Is Missing

## The Same Pattern Gap as H1 and H5

H2 describes a **mechanism** (7 vectors × 3 RAW queries + Distillation Ladder L1→L2→L3) but never articulates the **laws** that govern whether the research output is creatively *usable* or merely *comprehensive*.

The MCDA gave H2 a 7.25/10 — the lowest of the 5 hypotheses. Not because the Ladder is weak, but because H2 was designed as an **additive architecture** (more queries, more depth) rather than a **compression engine** (fewer, denser outputs). That's fine as a design choice. But even additive architectures need laws.

---

## What the Actual Pipeline Does (From the Skills and Commands)

### Deep Researcher SKILL.md (381 lines)

**Identity:** "E-Roll Deep Researcher V2 — 5-Mode Cultural Research Agent"

**Inputs:**
- `tribe_soul.json` — cultural DNA (slang, heroes, enemies)
- `strategy_brief.json` — arc type, unified frame, thematic SPR
- `premise_analysis.json` — scene clusters (W1-W5), quotes, timing
- `final_script.json` — actual quotes, timestamps, segment order
- `Brand Avatar` — physical DNA, cultural anchors

**Process:**
1. **Phase 1: Context Loading** — load all narrative sources, create research planning table mapping each W1-W5 cluster to visual needs
2. **Phase 2: 12 Introspection Questions** — answered from `tribe_soul.json` (Language & Codes, Aesthetics & Symbols, Rituals & Behaviors, Heroes & Icons, Opposition & Wounds, Emotional Truths)
3. **Phase 3: Browser Research** — 5 specialist modes (Influencer Scout, Ethnographer, Journalist, Archivist, Symbol Hunter) producing 24+ named references with verified URLs

**Output:** `{project_id}_ERoll_Deep_Research_Report.md` (2400-3000 words, 24+ refs, 24+ URLs)

**Validation:**
- Word count gate (2400-3000)
- Named references gate (24+)
- Source URLs gate (24+)
- No generic terms (forbidden list)
- Tribe soul traceability (30%+)

### cmf-eroll Command (401 lines)

**7-step pipeline:** Pre-flight → Load Arc Skill → Generate Research Plan → Execute Browser Research → Compile Report → Validate URLs → Generate Queries

**13 arc-specific deep-researcher skills**, each with 12 beat-aligned research questions customized to the arc's emotional structure.

### ccf-eroll-research Command (367 lines)

**6-step pipeline:** Pre-flight → Load Researcher Skill → Execute Research → Validate URLs → Soul Alignment → Output Manifest

**5 Query Strategy Formulas:** evidence, cultural_reference, environmental, symbolic, contrast

---

## The Gap: 4 Laws vs. H2's Current State

| Component | 4 Laws of Questions ✅ | H2 Deep Research ❌ |
|:---|:---|:---|
| **Axiom** | "A system cannot output signal it has not absorbed" | None — "7 vectors × 3 queries" is a specification, not an axiom |
| **Alchemy Grounding** | Each mode maps to Prediction Error / Costly Signaling / Specificity→Universality | The 5 specialist modes (Influencer, Ethnographer, Journalist, Archivist, Symbol Hunter) have cultural labels but no mapping to WHY specific modes produce resonant findings vs. generic findings |
| **Input Quality** | Saturation sources with mode-tagging, Proof Bank, Interest Ratio (4 Shades) | Pre-flight checks that input files EXIST. Research plan checks that questions are populated. But no check that the inputs carry emotionally differentiated data |
| **Output Test** | "Could ChatGPT answer this?" / "Would the tribe say 'how did you know?'" | Word count, reference count, URL verification, no-generic-terms check. All are **structural compliance tests** — none ask whether the research CREATES emotional fuel |
| **End Goal** | "The coach pauses, feels, tells a specific story" | "24+ named references with verified URLs" ← that's a count, not a goal |

---

## What H2 Currently DOESN'T Do (But Should)

### 1. No Emotional Typing of Research Findings

The Deep Research Report delivers 24+ references organized by **specialist mode** (Influencer, Ethnographer, etc.) and by **beat** (W1-W5). But the findings are NOT typed by emotional mode.

A finding like *"Documentary footage of medical discrimination in French hospitals"* is clearly TENSION fuel — it documents the enemy. But nothing in the pipeline tags it as such. When the Storyboard Composer or the Visual Researcher picks up these findings downstream, they have to intuit which findings serve Tension, which serve Vulnerability, which serve Recognition.

**What this means:** The research report is a *pile* of culturally specific references — excellent quality, but emotionally untyped. The downstream agents are forced to do the emotional classification that should have happened during research.

### 2. No Research Depth Stratification

The MCDA proposed a Distillation Ladder (L1 Surface → L2 Mechanism → L3 Collision) but the actual skill has no depth stratification. All 12 research questions operate at one depth — "Find named references for this beat."

The questions are beat-aligned (which beat needs what), but not depth-aligned (does this question uncover surface context, underlying mechanism, or a collision/contradiction?). Compare:

| Depth | What It Asks | Current Skill Has This? |
|:---|:---|:---|
| **L1: Surface** | "Who are the recognizable faces this tribe reveres?" | ✅ Yes (Q7-8: Heroes & Icons) |
| **L2: Mechanism** | "Why does this tribe revere THESE figures specifically? What need do they fulfill that other figures don't?" | ❌ No — the skill asks for names, not for reasons |
| **L3: Collision** | "Where does reverence for these figures CONTRADICT the coach's actual message? Where is the tribal hero at odds with the coach's thesis?" | ❌ No — the skill assumes tribal references support the story |

Without L2 and L3, the research produces **illustrative** references (images that show what the story talks about) but not **provocative** references (images that create tension between what the tribe believes and what the coach is revealing).

### 3. No Beat ↔ Mode Alignment Check

The skill maps 12 questions to beats (W1-W5). The MCDA's H4 (E-Roll Visual Search) proposed a beat-to-mode routing table:

| Beat | Emotional Register | Priority Modes |
|:---|:---|:---|
| W1 HOOK | TENSION (disruption) | Journalist + Archivist |
| W2 PROBLEM | RECOGNITION (shared pain) | Ethnographer + Symbol Hunter |
| W3 MECHANISM | TENSION → RECOGNITION | Influencer Scout + Ethnographer |
| W4 PROOF | VULNERABILITY → RECOGNITION | Symbol Hunter + Influencer Scout |
| W5 CLOSE | RECOGNITION | Influencer Scout + Archivist |

**But this routing table exists only in the MCDA document, not in any skill or command.** The Deep Researcher SKILL.md runs all 5 modes for the whole project. It doesn't prioritize which mode is most emotionally relevant for which beat.

### 4. No "Could AI Find This?" Gate

The Question Funnel's CHECK 1 asks: *"Could ChatGPT answer this?"* The equivalent for research would be:

> "Could a researcher who knows NOTHING about this specific coach's story, tribe, or cultural context find this same reference by searching generic terms?"

If the answer is YES, the reference is culturally specific but **narratively generic** — it illustrates the tribe's culture without serving the story's emotional arc. The current validation checks for forbidden generic *terms* (e.g., "african woman", "herbal tea") but not for generic *research intent*.

**Example:**
- ✅ PASS: `"Tatiane Van Laethem naturopath Belgium"` — requires knowing this coach's specific tribe hero
- ❌ FAIL: `"African traditional tea ceremony photography"` — any researcher studying African wellness culture would search this

The forbidden terms list catches the second example at the query level. But it doesn't catch:
- ✅ QUERY specific, ❌ FINDING generic: Query `"Kinkeliba thé longue vie"` is specific, but the returned image is a generic stock photo of tea preparation. The query was specific but the *selected finding* is emotionally generic.

---

## Proposed: 4 Laws of Research Distillation

### Law 1: Narrative Saturation Before Searching

**Axiom:** *Research that is not saturated with the story's emotional terrain produces culturally accurate but narratively disconnected findings.*

**Alchemy Grounding:**
- *"Humans crave context, not content"* — raw cultural references are content; narrative-aligned references are context
- *"Attention is felt, not just given"* — research executed with deep understanding of the story's emotional arc produces findings that FEEL different from generic cultural research
- *"Specificity creates universality"* — the more precisely the researcher understands THIS coach's specific wound, mechanism, and proof, the more universally resonant the found imagery becomes

**What this means:** The current Phase 1 (Context Loading) loads files. But loading ≠ saturation. The researcher must understand the story's emotional trajectory BEFORE constructing queries.

**Input Quality Checks:**

| Input | Passing Saturation | Failing Saturation |
|:---|:---|:---|
| `strategy_brief.json` | Researcher can articulate the **unified frame** in one sentence AND identify where the frame CREATES TENSION with the tribe's existing beliefs | Researcher loaded the file but cannot state what emotional journey the viewer takes |
| `premise_analysis.json` | Researcher knows which beat carries which emotional register (HOOK=Tension, PROBLEM=Recognition, etc.) and can state what visual evidence each register requires | Researcher knows the timestamps and quotes but not which emotional mode each beat serves |
| `tribe_soul.json` | Researcher can name at least one **unnamed feeling** the tribe has (from `emotional_resonance`) that the story NAMES for the first time | Researcher extracted slang and heroes but can't state what the tribe FEELS but can't articulate |
| `Brand Avatar` | Researcher knows the coach's physical markers AND what those markers symbolize culturally (e.g., mahogany skin against pre-dawn light = isolation before transformation) | Researcher copied the physical description without understanding its narrative function |

**The Saturation Test:**
> "Before your first search query, can you complete this sentence: 'The viewer needs to feel _____ at beat W1, _____ at W2, _____ at W3, _____ at W4, and _____ at W5 — and the gap between what the tribe currently feels and what the coach reveals is _____.'"
> → Cannot complete = NOT saturated. Research will produce illustrative but emotionally flat findings.
> → Can complete = PASS. Queries will be emotionally directed.

---

### Law 2: Emotional Mode Classification of Findings

**Axiom:** *A research finding's downstream value is proportional to its emotional specificity. Untyped findings force downstream agents to do the emotional work that research should have done.*

**Alchemy Grounding:**
- *"Prediction Error"* — TENSION findings must document something that BREAKS the viewer's expectation (the enemy, the contradiction, the wound the system inflicts)
- *"Costly Signaling"* — VULNERABILITY findings must document something that is EXPENSIVE to acknowledge (the coach's real struggle, the community's hidden shame, the price of the transformation)
- *"Truth is recognized, not taught"* — RECOGNITION findings must document something the tribe already KNOWS but has never seen articulated (their daily rituals, their unnamed feelings, their unspoken codes)

**What this means:** Every finding in the Deep Research Report must carry a `mode` tag — not just a beat tag and a specialist mode tag.

**Mode Classification Protocol:**

| Mode | Finding Makes the Viewer... | Specialist Mode Affinity | Example Finding |
|:---|:---|:---|:---|
| **TENSION** | "I didn't know that was happening" | Journalist (documentation of wounds), Archivist (historical evidence of enemy) | Documentary footage of medical racism in French emergency rooms |
| **VULNERABILITY** | "They went through that too" | Ethnographer (rituals of survival), Influencer (trusted figures showing struggle) | Video of Tatiane Van Laethem discussing her own health crisis before becoming a naturopath |
| **RECOGNITION** | "That's MY reality" | Ethnographer (daily objects), Symbol Hunter (tribal visual codes) | Close-up of Kinkeliba being prepared in an everyday kitchen, not a magazine spread |

**The Classification Test (per finding):**
> "This finding documents _____ (what) and serves _____ mode (why) because it makes the viewer feel _____ (how)."
> → If you can only fill in "what" but not "why" or "how" = the finding is descriptive but emotionally unclassified.
> → If all three are filled = PASS. Downstream agents know exactly how to use this.

**The Batch Diversity Gate:**
> "Do the 24+ findings cover all 3 modes? Minimum: 7 TENSION + 7 RECOGNITION + 5 VULNERABILITY + 5 multi-mode."
> → If 18+ are untyped or cluster in one mode = emotional monotone. The research will produce a one-note visual story.

---

### Law 3: Depth Stratification, Not Breadth Accumulation

**Axiom:** *A research finding's creative power is proportional to its depth layer. Surface findings illustrate; mechanism findings explain; collision findings transform.*

**Alchemy Grounding:**
- *"Surprise requires understanding"* — surface findings (L1) provide context, but only mechanism findings (L2) reveal the "why" that surprises. Only collision findings (L3) reveal the shadow — where the coach's own thesis has a blind spot
- *"The Shadow"* — L3 findings are the research equivalent of the Shadow: the contradictory, uncomfortable truth that makes the story three-dimensional instead of flat
- *"Meaning emerges from constraint"* — depth layers are a constraint that forces the researcher to go BELOW the surface answer. Without L3, research stays at the level of "supporting evidence"

**What this means:** The 12 research questions must be depth-stratified. For each beat, at least one question should probe mechanism (L2) and at least one should probe collision (L3).

**The 3-Layer Question Architecture:**

| Layer | Name | Question Type | What It Produces | Example (Witness Arc, HOOK Beat) |
|:---|:---|:---|:---|:---|
| **L1** | Surface | What exists? | Illustrative references — images that SHOW the topic | "Who are the wellness influencers this tribe follows?" → Returns profile photos, branded content |
| **L2** | Mechanism | Why does it work? | Explanatory references — images/docs that REVEAL the underlying dynamic | "Why does this tribe trust social media naturopaths over doctors? What institutional failure drives this?" → Returns investigative journalism, patient advocacy docs |
| **L3** | Collision | Where does it break? | Provocative references — images/docs that CREATE TENSION between the coach's message and reality | "Where have wellness influencers THIS tribe trusts given advice that was later debunked or harmful? What is the cost of the trust the coach asks for?" → Returns fact-checks, counter-evidence, community debates |

**The Depth Coverage Test (per beat):**
> "Does this beat have at least one L2 finding and at least one L3 finding?"
> → If a beat has only L1 findings = the visual story for that beat will be illustrative but never surprising.
> → If the beat has L2 and L3 = PASS. The Storyboard Composer has emotional fuel at all three depths.

**Why L3 matters most for emotional impact:**

L1 references produce B-roll that says *"here is the tribal world."*
L2 references produce B-roll that says *"here is WHY the tribal world works this way."*
L3 references produce B-roll that says *"here is where the tribal world's own logic contradicts itself."*

Only L3 creates the visual prediction error that makes the viewer's brain wake up.

---

### Law 4: The Narrative Provenance Gate

**Axiom:** *A research finding's value is inversely proportional to how discoverable it is without the coach's specific story.*

**Alchemy Grounding:**
- *"Scarcity is psychological, not physical"* — in an era where any AI can search "African wellness" and find beautiful imagery, true scarcity = findings that REQUIRE knowledge of this specific story to even think of searching for
- *"Authenticity is non-negotiable"* — audiences detect whether the visual world of a video was assembled from generic cultural research or from deep understanding of ONE coach's specific journey
- *"Story is the vessel, not the decoration"* — research findings are not decoration for the video; they are the EVIDENTIARY LAYER of the story. A finding must prove or challenge something the coach said

**The 4 Provenance Checks:**

```
CHECK 1: "Could a researcher who never read the transcript find this?"
  → YES = REJECT (the finding is culturally valid but narratively disconnected)
  → NO  = PASS (the finding requires knowledge of THIS coach's story)

CHECK 2: "Does this finding map to a SPECIFIC quote in the final script?"
  → NO  = REJECT (it's thematic decoration, not evidentiary)
  → YES = PASS (it serves a specific narrative moment)

CHECK 3: "If this finding were removed, would the beat's visual story 
         lose something irreplaceable?"
  → NO  = The finding is supplementary, not structural
  → YES = PASS (the finding is load-bearing)

CHECK 4: "Does this finding create an emotional response that is 
         DIFFERENT from the other findings for the same beat?"
  → NO  = REJECT (emotional redundancy — two findings creating the 
          same response is waste)
  → YES = PASS (the findings for this beat create a layered 
          emotional progression)
```

**Current gap:** The forbidden terms list catches `"african woman"`, `"herbal tea"`, `"colorful fabric"` — generic TERMS. But it doesn't catch findings that use specific terms yet serve generic purposes. A query for `"Kinkeliba traditional tea preparation"` passes the forbidden terms check but the returned finding might be a magazine-spread stock photo that could appear in ANY African wellness video, not specifically THIS coach's story.

The Provenance Gate tests whether the finding is **narratively load-bearing**, not just culturally specific.

---

## Summary: 4 Laws Comparison

| Law | Question Funnel ✅ | H2 Deep Research ❌ (current) | H2 Deep Research ✅ (proposed) |
|:---|:---|:---|:---|
| **1. Saturation** | Coach soul + tribe + topic + research + proof bank → verified before generation | Input files exist (pre-flight) → research plan populated | Emotional terrain saturation test: researcher must articulate the viewer's emotional journey per beat BEFORE any query |
| **2. Mode Classification** | 12 raw Qs tagged as 4T + 4V + 4R | 24+ findings tagged by beat + specialist mode | 24+ findings tagged by beat + specialist mode + **emotional mode (T/V/R)** with batch diversity gate (7T + 7R + 5V + 5 multi) |
| **3. Depth** | 12→6→3 with cross-mode compression | 12 questions at uniform depth | 12 questions with depth stratification (L1/L2/L3) per beat — at minimum 1 L2 and 1 L3 per beat |
| **4. Gate** | "Could ChatGPT answer?" + "Would tribe say 'how did you know?'" | Word count, ref count, URL verification, no-generic-terms | 4 provenance checks: story-dependency, script-mapping, irreplaceability, emotional non-redundancy |

---

## End Goal Comparison

| System | Current End Goal | Laws-Derived End Goal |
|:---|:---|:---|
| **Question Funnel** | "The coach pauses, feels, tells a specific story" | (same — already law-governed) |
| **H1 Blueprint** | "12 blueprints generated" | "Every blueprint activates 2+ modes and collapses if one fusion layer is removed" |
| **H5 Visual** | "VFS ≥ 75" | "The viewer's body responds before their mind — and the response matches the intended mode" |
| **H2 Deep Research** | "24+ named references with verified URLs" | **"Every finding is emotionally typed, depth-stratified, and narratively irreplaceable — and downstream agents know exactly which emotional mode each finding serves without having to guess"** |

The end goal isn't "comprehensive research." The end goal is: **the finding set directly leads to the sourcing of standalone visual assets (E-roll) that precisely execute the emotional arc of each beat**, so that the final edit is emotionally orchestrated, not accidentally assembled.
