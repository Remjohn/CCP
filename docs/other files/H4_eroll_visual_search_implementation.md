# H4 — E-Roll Visual Search: First-Principles Implementation Architecture

**Pipeline Stage:** CMF Phase 1b → Visual Research (Deep Research Report → Search Queries → Downloaded Assets)  
**Laws Applied:** 4 Laws of Visual Search Distillation  
**MCDA Score:** 9.05/10 (Ranked #1 — Strongest Hypothesis)  
**Target Skill:** `skills/cmf/eroll/query-generator/SKILL.md`  
**Target Command:** `commands/cmf-eroll.md` (Step 7: Query Generation)  
**Upstream Skill:** `skills/cmf/eroll/deep-researcher/SKILL.md` (H2 output)  
**Input:** `ERoll_Deep_Research_Report.md` (typed, depth-stratified) + `beat_cluster.json` (beat → mode routing) + `final_script.json` + `tribe_soul.json` + Brand Avatar  
**Output:** `ERoll_Search_Queries.json` (mode-aligned, provenance-verified) + Downloaded asset library  
**Validation:** ✅ E-ROLL DEEP RESEARCH COMPLETE (Command completion marker)

---

## System Overview: What H4 Actually Does

The E-Roll Visual Search is the translation layer between narrative and imagery. It receives the H2 Deep Research Report — a body of emotionally typed, depth-stratified, narratively load-bearing findings — and converts those findings into precise search queries that locate **standalone visual assets** capable of carrying the video's emotional arc in the final edit.

The current pipeline excels at **Cultural Accuracy**: it finds the right tea ceremony, the right face of the right cultural figure, the right urban texture. Five specialist research modes (Influencer Scout, Ethnographer, Journalist, Archivist, Symbol Hunter), each with their domain-specific expertise, produce queries that are culturally informed and historically grounded.

**What the pipeline does not guarantee is Emotional Truth.** Cultural accuracy is necessary but insufficient. The gap is this: 90% of culturally correct B-roll is still emotionally interchangeable. An image of Kinkeliba tea preparation in the correct cultural context can be a RECOGNITION image (the tribe's everyday morning ritual, chipped cup, ordinary kitchen) or a TENSION image (the contrast between artisanal wellness culture and the medical system the coach critiques) — depending entirely on the semiotic distance, lighting, and composition. Currently, the query system searches for the cultural reference without specifying the emotional function. The result is technically correct imagery that the editor must re-interpret at download.

The 4 Laws of Visual Search Distillation eliminate this re-interpretation burden: every query targets a specific emotional function, and every downloaded asset is tested against first-principles checks before acceptance.

---

## Section 1: Input Quality Standards (Query Saturation Protocol)

A search result can only be as narrative as the question that triggered it. Before any query is constructed, the Query Generator must verify that both the research findings and the beat-mode routing are available and emotionally differentiated.

### Required Input Files & Quality Standards

| # | Input Source | File / Field | Minimum Quality Standard |
|:--|:------------|:-------------|:------------------------|
| 1 | **Deep Research Report** | `ERoll_Deep_Research_Report.md` — typed findings with mode + depth + script_mapping | Every finding must carry its `mode` (T/V/R), `depth_level` (L1/L2/L3), and `script_mapping` field |
| 3 | **beat_cluster.json** | `{project_id}_beat_cluster.json` — beat → mode routing (from `/cmf-beat-cluster`) | Provides the mode priority per beat — must already be populated from H1 |
| 4 | **final_script.json** | `{project_id}_final_script.json` — exact quotes + timestamps per scene | Every search query must map to a specific script moment |
| 5 | **tribe_soul.json** | `tribe_soul.json` (Coach level) — slang, visual codes, daily objects, forbidden aesthetics | Must identify ≥1 visual element the tribe considers aspirational and ≥1 they consider inauthentic ("magazine spread wellness" vs. "everyday kitchen") |
| 6 | **Brand Avatar** | `😎 {project_id} - The Brand Avatar 😎.md` — physical and cultural markers | Must specify what each physical marker MEANS narratively, not just what it looks like |

### Query Saturation Gate (Pre-Query Construction Check)

Before any query is constructed, the system verifies that the research being queried reveals insider knowledge — not tourist-level cultural information:

```
QUERY SATURATION GATE:

For each research finding being converted to a query, ask:
"Does this finding contain a detail that is INVISIBLE to an outsider but
 IMMEDIATELY OBVIOUS to a member of this tribe?"

→ NO  = TOURIST-MODE finding. Queries will return generic stock imagery.
         The cultural reference is accurate but the insider signal is absent.
         STOP. This finding needs depth enrichment before query generation.

→ YES = PASS. The finding carries tribal insider knowledge.
         Queries will return imagery the tribe recognizes as their own reality,
         not someone's idea of their reality.
```

**Why this gate matters:**  
Tourist-mode findings produce tourist-mode queries. `"Kinkeliba tea preparation"` is a culturally specific query — but it returns results from tea brand websites, wellness magazines, and tourism studies. These images are accurate to the culture but foreign to the tribe. The insider-knowledge version of this query would be: `"Kinkeliba matin cuisine ordinaire quotidien"` — the specific combination of morning, everyday kitchen, and ordinary that locates the RECOGNITION image the tribe actually sees in their own life.

---

## Section 2: Law Execution Protocol

### Law 1 — Narrative Saturation Before Query

**Axiom:** *A search result can only be as narrative as the question that triggered it.*

**What it does:** Ensures every query is built from research that contains first-principles narrative intelligence — not just cultural accuracy. The query construction formula is upgraded to embed emotional function:

**Current Formula:**
```
[Cultural Reference] + [Context Modifier] + [Visual Anchor]
Example: "Kinkeliba thé" + "artisanal" + "tasse céramique"
```

**Laws-Upgraded Formula:**
```
[Insider Cultural Reference] + [Beat Mode Modifier] + [Emotional Visual Anchor] + [Anti-Stock Qualifier]

TENSION query: [specific wound reference] + [documentary/archival context] + [evidence anchor] + [raw/unfiltered]
RECOGNITION query: [insider daily object] + [ordinary domestic context] + [tactile/worn anchor] + [non-aspirational]
VULNERABILITY query: [unguarded moment reference] + [unpolished/private context] + [cost signal anchor] + [unstaged]

Example (RECOGNITION beat):
"Kinkeliba matin cuisine ordinaire quotidien" + [tribe-specific morning ritual context]
→ Returns: everyday kitchen imagery, not wellness brand photography

Example (TENSION beat):
"urgencies hôpital attente longue France discrimination" + [documentary evidence context]
→ Returns: journalistic documentation of institutional failure, not health system marketing
```

**Saturation Test per query:**
> "If someone who knew nothing about this tribe ran this query, would they understand why it's relevant to this specific video?"  
> → YES = the query is culturally specific but narratively surface  
> → NO = PASS — the query requires insider knowledge of the story to construct

---

### Law 2 — Semiotic Mode Classification

**Axiom:** *An image's emotional function is determined by its semiotic distance. Tension is far (macro/wide/harsh); Recognition is near (tactile/intimate/warm); Vulnerability is unguarded (unstaged/private/unpolished).*

**What it does:** Routes every query to an emotional mode BEFORE selecting a specialist research mode. The current pipeline routes by specialist (Journalist for wounds), but has no axiom for WHY. This law provides the axiom and makes the routing a first-principles decision.

**Beat-to-Mode Routing Table:**

| Beat | Emotional Register | Primary Mode | Dominant Specialist | Visual Distance |
|:-----|:-----------------|:------------|:-------------------|:----------------|
| **W1 HOOK** | Pattern interrupt, disruption | TENSION | Journalist + Archivist | Wide/macro — the broken world at scale |
| **W2 PROBLEM** | Shared pain, the tribe sees itself | RECOGNITION | Ethnographer + Symbol Hunter | Close/intimate — the daily object that names the feeling |
| **W3 MECHANISM** | Understanding the "why" | TENSION → RECOGNITION | Journalist + Ethnographer | Mid/evidence — documents the mechanism in lived reality |
| **W4 PROOF** | Transformation cost + result | VULNERABILITY → RECOGNITION | Influencer Scout + Symbol Hunter | Unguarded/private — the unpolished truth of change |
| **W5 CLOSE** | Belonging, the tribe reunited | RECOGNITION | Ethnographer + Influencer Scout | Warm/intimate — the new daily ritual, after |

**The Mode Alignment Gate (per query):**
```
"Does this query's visual anchor match the beat's semiotic distance and mode?"

TENSION (W1): Visual anchors = "documentary," "journalistic," "archival," "raw,"
              "macro," "decay," "institutional"
              → FAIL if anchor is "community," "warm," "intimate," "celebration"

RECOGNITION (W2): Visual anchors = "domestic," "tactile," "worn," "everyday,"
                  "hand-held," "morning," "ordinary kitchen"
                  → FAIL if anchor is "aspirational," "studio," "professional"

VULNERABILITY (W4): Visual anchors = "unstaged," "private," "unpolished,"
                    "unguarded," "candid," "before"
                    → FAIL if anchor is "success," "achievement," "polished"
```

---

### Law 3 — Visual Compression (The Evidence Test)

**Axiom:** *B-Roll is not decoration; it is evidence. If an image doesn't prove the narrator's claim, it is noise.*

**What it does:** Converts the asset evaluation from an aesthetic judgment ("does this look good?") to a forensic judgment ("does this image PROVE the specific claim being made at this timestamp?").

**The Evidence Test (applied to every downloaded asset):**

```
EVIDENCE TEST:
"If you muted the audio entirely, would this specific image STILL PROVE
 the narrator's current sentence — to a viewer who has never heard the video?"

→ NO  = DECORATION. Reject. The image illustrates the topic without
         serving as evidence of the claim.
         (Example: Wide shot of "urban poverty" when narrator says
          "the medical system dismissed 78% of Black women's pain reports")

→ YES = EVIDENCE. Pass. The image is forensically load-bearing.
         (Example: Actual documentary footage/photo of the specific
          institutional context the narrator names)
```

**Compression Yield Principle:**  
One high-compression evidence clip is worth ten wide-angle decoration shots. A single close-up of a specific cultural object at the exact moment of narrative tension carries more emotional weight than ten generic establishing shots. The query system must prioritize finding THE ONE image that proves the claim — not the ten images that illustrate the theme.

**The Specificity Hierarchy for Evidence:**

```
LEVEL 1 (Weakest Evidence): Generic cultural imagery
  "African women cooking" — shows the world, proves nothing specific

LEVEL 2 (Supporting Evidence): Specific cultural reference
  "Kinkeliba tea preparation" — shows the tribe's ritual, supports the context

LEVEL 3 (Narrative Evidence): Specific reference + beat context
  "Kinkeliba matin cuisine ordinaire quotidien" — shows the tribe's daily
  morning ritual in a non-aspirational setting. PROVES "this is your world."

LEVEL 4 (Forensic Evidence): Specific reference + narrative contradiction
  "naturopathe France formation médecine conventionnelle refus" —
  documents the institutional rejection that created the alternative
  health space the tribe now inhabits. PROVES "here is the wound."
```

Only Level 3 and Level 4 assets pass the Evidence Test. Level 1 and Level 2 assets are decoration and must be rejected regardless of cultural accuracy.

---

### Law 4 — The Semiotic Authenticity Gate

**Axiom:** *An image's emotional impact is inversely proportional to its predictability. The most powerful image is the one that looks like a private memory, not a public asset.*

**What it does:** Runs a 4-check authenticity filter on every downloaded asset before it is accepted into the asset library. This is the final quality gate — it catches images that passed the Evidence Test but still carry the "stock smell" that the tribe's visual intelligence immediately recognizes and discounts.

**The 4 Visual Authenticity Checks:**

```
CHECK 1: The Stock Smell Test
  "Does this image look like it was produced for a commercial,
   a brand campaign, or a stock library?"
  → YES = REJECT. No matter how culturally specific, commercial production
           values signal "this was made for you to feel something" —
           and that meta-awareness kills the authentic response.
  → NO  = PASS

CHECK 2: The Niche Non-Generality Test
  "Would a competitor in a completely different niche (fitness, tech,
   finance) find this image equally relevant to their content?"
  → YES = REJECT. The image is emotionally generic — it carries
           universal symbolism but no tribal specificity.
  → NO  = PASS (The image requires context to understand)

CHECK 3: The Mess Test (Alchemy Principle 10)
  "Does this image contain 'The Mess' — imperfection, disorder,
   or unpolished reality that signals this was not staged?"
  → NO  = REJECT. Images without mess are aspirational. Aspirational
           imagery creates distance, not connection.
  → YES = PASS. The presence of imperfection signals authenticity.

CHECK 4: The One Decisive Signifier Test
  "Is there a single visual element in this image that carries
   the entire emotional read — without needing to analyze the composition?"
  → NO  = REJECT. Visual clutter means the image requires cognitive
           effort to decode. Emotional response must be immediate.
  → YES = PASS. The image has semiotic efficiency — one element that
           does all the emotional work.
```

**Failed asset routing:**  
- Fails 1-2 checks → Return to search. Refine query with stronger anti-stock qualifiers.  
- Fails 3-4 checks → The research finding itself may be at issue. Escalate to L3 depth research.  
- No asset in the result set passes → Flag the beat as visually under-served. Trigger additional search session with Archivist or Symbol Hunter.

---

## Section 3: Output Format — Annotated Query & Asset Library

Every query in `ERoll_Search_Queries.json` carries its law compliance metadata:

```json
{
  "id": "W1_Q1",
  "query": "urgences hôpital attente longue nuit france documentary",
  "beat": "W1",
  "emotional_mode": "TENSION",
  "depth_level": "L3",
  "specialist_mode": "Journalist",
  "semiotic_distance": "Wide/macro",
  "visual_anchor": "documentary-evidence-institutional",
  "anti_stock_qualifier": "candid unposed raw",
  "insider_knowledge_required": true,
  "saturation_gate": "PASS",
  "mode_alignment_gate": "PASS",
  "script_mapping": "SC01 / W1 / 00:03-00:09",
  "asset_status": "ACCEPTED",
  "authenticity_all_checks_passed": true,
  "evidence_test": "PASS",
  "compression_level": "L4_FORENSIC"
}
```

---

## Section 4: Evaluation — 5 Micro-Hypothesis Tests

### MH1 — The Insider Knowledge Test
**Hypothesis:** "Every query in `ERoll_Search_Queries.json` contains a detail that would be invisible to an outsider but recognizable to a member of the tribe."  
**Test:** For each query, ask: "Could a researcher who knows nothing about this coach's tribe or story have constructed this exact query?" If yes, the query is outsider-mode.  
**Pass condition:** ≥90% of queries fail the "outsider construction test" — meaning they require tribal insider knowledge to construct. Queries that pass the outsider test (could be constructed by anyone) are flagged for re-saturation.

### MH2 — The Mode-Beat Alignment Test
**Hypothesis:** "Every query's semiotic distance and visual anchor correctly match the emotional mode required by its beat."  
**Test:** Apply the Mode Alignment Gate to every query in the library. Check that TENSION queries use documentary/archival anchors, RECOGNITION queries use domestic/tactile anchors, and VULNERABILITY queries use unstaged/private anchors.  
**Pass condition:** 100% alignment. A single mode-beat mismatch means an entire beat's visual assets will carry the wrong emotional register — the video's emotional arc breaks at that point.

### MH3 — The Evidence Test Yield
**Hypothesis:** "At least 70% of accepted assets pass the Evidence Test at Level 3 or Level 4 (Narrative or Forensic Evidence) — not Level 1 or Level 2 (Generic or Supporting)."  
**Test:** Apply the Evidence Test specificity hierarchy to every accepted asset. Score: Level 1, 2, 3, or 4.  
**Pass condition:** ≥70% of accepted assets are Level 3 or Level 4. If less than 70%, the asset library is predominantly decoration rather than evidence — the edit will be forced to use visual wallpaper rather than visual proof.

### MH4 — The Authenticity Gate Yield
**Hypothesis:** "At least 80% of initially downloaded assets pass all 4 Semiotic Authenticity Checks without requiring a re-search."  
**Test:** Track the pass/fail rate of the 4 Authenticity Checks across all downloaded assets in the first-pass library.  
**Pass condition:** ≥80% pass all 4 checks on first download. A lower rate indicates that the query formulas are not yet producing sufficiently specific results — the anti-stock qualifiers need to be strengthened.

### MH5 — The Downstream Utility Test
**Hypothesis:** "An editor who has never read the transcript can open the Asset Library and immediately assign each asset to its beat and understand its emotional function — without re-reading the Deep Research Report."  
**Test:** Simulate the edit handoff: given only the annotated Visual Search Queries JSON and the downloaded assets — can the editor make all final visual decisions without additional context?  
**Pass condition:** Every accepted asset has sufficient metadata that the editing decisions are instruction-driven, not improvised. No asset should be marked "TBD — decide in edit."

---

## Section 5: H4 Completion & Asset Delivery

Upon completion of the full H4 protocol, the system confirms the standalone visual assets are ready for delivery to the **Final Edit**. 

```markdown
✅ E-ROLL ASSET DELIVERY COMPLETE

Project: [Project ID]
Assets Downloaded: [Number]
Assets at L3/L4: [x]% (target ≥70% ✅)
Authenticity Pass: [x]% (target ≥80% ✅)
```

**Completion Metrics Tracking:**
- **MH1 Insider Knowledge Test:** ✅ PASS ([x]% outsider-proof)
- **MH2 Mode-Beat Alignment:** ✅ PASS (100% aligned)
- **MH3 Evidence Test Yield:** ✅ PASS ([x]% at L3/L4)
- **MH4 Authenticity Gate Yield:** ✅ PASS ([x]% first-pass pass rate)
- **MH5 Downstream Utility:** ✅ PASS (full metadata on all assets)

**VERDICT: ✅ E-ROLL ASSETS CLEARED FOR FINAL EDIT**

**BLOCKED STATES (if any check failed):**
- ❌ Outsider-proof <90% → Re-saturate queries with deeper tribal insider detail
- ❌ Mode-beat mismatch on any beat → Rewrite affected queries with correct anchors
- ❌ Evidence yield <70% → Trigger L3 depth research session for under-served beats
- ❌ Authenticity rate <80% → Strengthen anti-stock qualifiers across query formulas
- ❌ Any beat has zero assets → Emergency search session required before delivery


---

## Architectural Constants

| Constant | Value | Rationale |
|:---------|:------|:----------|
| Evidence level minimum | ≥70% at L3/L4 | Below 70%, the storyboard is built on illustrated decoration rather than visual proof |
| Authenticity check pass rate | ≥80% first-pass | Enforces query quality upstream — refine the query, not just reject the asset |
| Mode-beat alignment | 100% required | One misaligned beat breaks the emotional arc of the whole video |
| Insider knowledge requirement | ≥90% of queries | Tourist-mode queries produce tourist-mode results — generic stock that the tribe's visual intelligence rejects |
| Evidence Test scope | Every accepted asset | No asset enters the library without a forensic evidence classification (L1-L4) |
| Beat coverage | All beats mandatory | Missing visual coverage at any beat creates an edit-phase crisis — the pipeline cannot continue |

---

## Referenced CMF Skills & Commands

| Type | Name | Path |
|:-----|:-----|:-----|
| **Skill** | E-Roll Query Generator | `skills/cmf/eroll/query-generator/SKILL.md` |
| **Skill** | Deep Researcher V2 (upstream H2) | `skills/cmf/eroll/deep-researcher/SKILL.md` |
| **Skill** | Cultural Introspector | `skills/cmf/eroll/cultural-introspector/SKILL.md` |
| **Skill** | E-Roll Commander | `skills/cmf/commanders/eroll-commander/SKILL.md` |
| **Skill** | Storyboard Composer (downstream) | `skills/cmf/composers/{arc}-composer/SKILL.md` |
| **Edit** | Final Video Edit | Standalone E-Roll assets delivered for assembly |
| **Command** | cmf-eroll | `commands/cmf-eroll.md` |
| **Command** | cmf-beat-cluster (upstream) | `commands/cmf-beat-cluster.md` |

*Next Document: [H5 — Visual Prompt Writing: 4 Laws of Visual Distillation Implementation Architecture]*
