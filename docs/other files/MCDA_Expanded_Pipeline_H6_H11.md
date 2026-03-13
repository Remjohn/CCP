# MCDA: Expanded CCF Pipeline — Hypotheses H6-H11

**Document Type:** Multi-Criteria Decision Analysis  
**Scope:** 6 proposed pipeline hypotheses for the CCF Setup & Research Layer  
**Decision:** Which hypotheses to build, in what order, and at what priority  
**Date:** 2026-02-22

---

## 1. Problem Statement

The H0-H5 distillation funnel governs every stage of the **CCF content intelligence pipeline** — from the coach's layered questions through blueprint orchestration, deep research, voice generation, visual search, and visual prompt writing. Each stage has distillation laws, input quality gates, and validation receipts that form an unbreakable chain. CMF (Conscious Movie Factory) is the downstream **video editing pipeline** that consumes CCF's finished, distilled output — it is not where the intelligence lives.

But the funnel has a structural blind spot: **it assumes its foundational inputs are already rich, layered, and emotionally differentiated.** Specifically:

- **H1 (Blueprint Orchestrator)** assumes `soul_values.json` contains a deep, multi-layered understanding of the coach's philosophy. In reality, `soul_values.json` is a static extraction from one transcript — it captures core values and voice blueprint but has no update loop, no depth stratification, and no mechanism for the coach's philosophy to evolve as new transcripts are processed.

- **H2 (Deep Research)** assumes it receives a blueprint with enough emotional specificity to construct mode-typed, depth-stratified queries. In practice, the Deep Research currently runs at blueprint level but starts from scratch every time — no shared research foundation per theme.

- **H3 (SoC Generator)** assumes `coach_soc_batch.md` contains raw vulnerability moments. But the coach's story — the deeper narrative layers beneath the surface transcript — is never systematically extracted, depth-stratified, or made available as a structured resource.

- **H4 (E-Roll Visual Search)** assumes the researcher understands the tribe's visual codes at an insider level. But `tribe_soul.json` is a cultural artifact extraction (slang, heroes, enemies, humor) without emotional depth stratification — it knows WHAT the tribe says but not WHY they say it or what visual codes they would instantly recognize vs. instantly reject.

- **Fresh Research** exists as a 269-line browser-verified protocol, but has no distillation laws. It produces verified URLs and archetype-specific synthesis, but does not optimize for the recency bias opportunity — the specific leverage of presenting information the audience has never heard before.

**The fundamental gap:** The distillation funnel is only as strong as its weakest foundational input. Laws-governed stages (H0-H5) cannot produce laws-governed output if the setup-phase inputs were constructed without laws.

---

## 2. Proposed Hypotheses

| ID | Hypothesis | Pipeline Position | Existing Agent | Current Gap |
|:---|:----------|:-----------------|:--------------|:------------|
| **H6** | RAW Deep Research (CCF) | Per blueprint → feeds Deep Research Analyst | 44 Deep Research Analysts (per archetype) | Analysts exist but have no distillation laws; 4000-word RAW research has no formal protocol; visual-storytelling optimization missing |
| **H7** | RAW Fresh Research (CCF) | Per blueprint → feeds Fresh Research Analyst | 44 Fresh Research Analysts + 269-line protocol | Protocol is browser-verified but not laws-governed. No novelty optimization, no recency bias exploitation, no surprise density gate |
| **H8** | Coach Soul Values (CCF) | Setup phase → feeds all downstream stages | `Conscious_Soul_Values.md` (static, 48 lines) | Rich but frozen. No update loop, no depth stratification, no monthly refinement cycle |
| **H9** | Soul Tribe Profiles (CCF) | Setup phase → feeds visual search, SoC, research | Tribe Soul Extraction Engine (136 lines) | High-volume cultural harvester but surface-level: knows slang, heroes, enemies. Missing: WHY they say what they say, visual recognition codes, emotional depth layers |
| **H10** | Coach Philosophy Brief (CCF) | Setup phase → feeds SoC, blueprint, script | ❌ Does not exist | Complete gap. No agent extracts the coach's deeper narrative layers across multiple transcripts into a structured, evolving philosophy document |
| **H11** | Raw Target Audience Research (CCF) | Setup phase → feeds Tribe Soul Profiles | Deep Target Audience Research Planner (90 lines) | Planner exists (7-dimension framework) but produces a 220-word plan, not actual research. No analyst processes the raw output. No distillation laws |

---

## 3. Evaluation Criteria

Seven criteria, each weighted to reflect the pipeline's first-principles architecture:

| # | Criterion | Weight | Rationale |
|:--|:---------|:------:|:---------|
| C1 | **Downstream Impact** | 20% | How many downstream stages depend on this input? A failure here cascades furthest. |
| C2 | **Current Gap Severity** | 20% | How broken is the current state? Does the gap produce silent failures or visible ones? |
| C3 | **Distillation Law Readiness** | 15% | Can we derive falsifiable axioms, input quality gates, and validation receipts for this stage? |
| C4 | **Resource Efficiency** | 10% | What is the cost-to-value ratio? Does the hypothesis duplicate existing work or create net-new capability? |
| C5 | **Specificity Amplification** | 15% | Does this hypothesis increase the precision and specificity of downstream outputs? (The Ladder of Depth principle) |
| C6 | **Update Loop Potential** | 10% | Does this hypothesis create a refinement cycle that compounds over time, or is it a one-shot extraction? |
| C7 | **First-Principles Alignment** | 10% | Does this hypothesis follow from the 4 Distillation Laws pattern (saturation → mode → compression → authenticity gate)? |

---

## 4. Scoring Matrix

Each hypothesis scored 1-10 per criterion:

| Criterion | H6 (Raw Deep) | H7 (Raw Fresh) | H8 (Coach Soul) | H9 (Tribe Soul) | H10 (Coach Phil) | H11 (Target Aud) |
|:----------|:---:|:---:|:---:|:---:|:---:|:---:|
| **C1 Downstream Impact** (20%) | 9 | 8 | 9 | 9 | 10 | 8 |
| **C2 Gap Severity** (20%) | 7 | 6 | 8 | 7 | 10 | 9 |
| **C3 Law Readiness** (15%) | 9 | 8 | 7 | 7 | 8 | 7 |
| **C4 Resource Efficiency** (10%) | 7 | 8 | 8 | 6 | 9 | 6 |
| **C5 Specificity Amplification** (15%) | 9 | 7 | 8 | 9 | 9 | 9 |
| **C6 Update Loop** (10%) | 5 | 7 | 9 | 7 | 10 | 6 |
| **C7 First-Principles** (10%) | 9 | 8 | 7 | 7 | 8 | 7 |

---

## 5. Weighted Scores & Ranking

| Rank | Hypothesis | Weighted Score | Tier |
|:-----|:----------|:--------------|:-----|
| **1** | **H10 — Coach Philosophy Brief** | **9.15** | 🟢 CRITICAL — Build First |
| **2** | **H6 — RAW Deep Research** | **8.15** | 🟢 CRITICAL — Build Second |
| **3** | **H9 — Soul Tribe Profiles** | **7.75** | 🟡 HIGH — Build Third |
| **4** | **H8 — Coach Soul Values** | **7.90** | 🟡 HIGH — Build alongside H10 |
| **5** | **H11 — Raw Target Audience Research** | **7.55** | 🟡 HIGH — Feeds H9 directly |
| **6** | **H7 — RAW Fresh Research** | **7.25** | 🟡 HIGH — Build alongside H6 |

---

## 6. Individual Hypothesis Analysis

### H10 — Coach Philosophy Brief (Score: 9.15 — CRITICAL)

**Why it ranks #1:** This is the only hypothesis that addresses a **complete structural absence**. Every other hypothesis has at least a partial agent or protocol. H10 has nothing — and yet every downstream stage implicitly depends on a deep understanding of the coach's philosophy that goes beyond a single-transcript extraction.

**What exists today:** `Conscious_Soul_Values.md` — a 48-line static file with core values, internal temperature map, unique metaphors, emotional vocabulary, voice blueprint, and signature perspective. All extracted from one transcript. Rich for a single pass, but frozen.

**What's missing:**
1. **Multi-transcript layering.** A coach who has done 12 interviews has revealed 12 different facets of their philosophy. Currently, only the first transcript is processed. The remaining 11 contain contradictions, evolutions, and depth that are never captured.
2. **Monthly refinement loop.** The coach's philosophy evolves as they practice, learn, and encounter new clients. The brief must be a living document, not a snapshot.
3. **Depth stratification.** Surface beliefs (what the coach says publicly), Mechanism beliefs (why they believe it — the reasoning layer), and Collision beliefs (where their own philosophy has been tested by reality and survived or adapted).
4. **Story inventory.** The coach's specific personal stories, categorized by emotional mode (T/V/R) and indexed for rapid retrieval by the SoC Generator and Script Adapter.

**The downstream cascade:** H10 feeds H1 (blueprint's decisive claim), H3 (SoC vulnerability source + coach voice), H5 (Brand Avatar emotional truth), and the Coach Soul Values refinement (H8). Without H10, every downstream stage improvises its understanding of the coach from a 48-line static file.

**Update Loop:** Monthly. Each new transcript or interview is processed through the Philosophy Brief extraction protocol, updating the depth stratification and story inventory. This is the only hypothesis with a built-in compounding mechanism — each cycle makes the coach representation richer.

---

### H6 — RAW Deep Research (Score: 8.15 — CRITICAL)

**Why it ranks #2:** The research layer is the fuel for the entire pipeline. H13Visual Search) and H3 (SoC Generator) both depend on research that is rich enough to provide storytelling elements — nostalgia, cultural events, memories, visual references, historical context. The current Deep Research Analysts exist (44 of them, one per archetype) but they receive no RAW research input with formal protocol.

**What exists today:** 44 Deep Research Analyst agents, each tailored to an archetype. They produce 1000-1200 word briefs. But the RAW research that feeds them (the 4000-word investigative pass) has no formal protocol, no quality gates, and no storytelling optimization.

**What's missing:**
1. **Storytelling-optimized research protocol.** The RAW Deep Research for CCF should specifically target: nostalgia triggers (events the tribe remembers), cultural objects (visual vibe baits), historical parallels (evidence for the coach's claims), and transformative moments (before/after stories the audience recognizes).
2. **Visual fuel specification.** Every finding should be tagged with its visual potential — can this research finding produce a recognizable image? This directly feeds H4 (E-Roll) downstream.
3. **Distillation laws.** Saturation gate (does the research go deep enough?), mode classification (what emotional function does each finding serve?), compression test (does every finding carry narrative weight?), authenticity gate (is it insider-level or tourist-level knowledge?).

**Execution model:** Per blueprint. The 4000-word RAW Deep Research runs for each blueprint, producing the foundation that the existing Deep Research Analyst distills into a 1000-1200 word brief.

---

### H9 — Soul Tribe Profiles (Score: 7.75 — HIGH)

**Why it ranks #3:** The Tribe Soul Extraction Engine currently harvests surface-level cultural artifacts: slang (top 10-15 terms), inside jokes (5-7), shared heroes (5), common enemies (5), humor profile, and emotional resonance (aspirations, anxieties, triggers). This is valuable — but it is a **single-depth extraction**.

**What's missing:**
1. **Depth stratification.** Surface layer (what the tribe says), Mechanism layer (why they say it — the psychological drivers beneath the slang), Collision layer (where the tribe's stated values contradict their actual behavior — the shadow of the community).
2. **Visual recognition codes.** What images does the tribe instantly recognize as "us" vs. "not us"? The current extraction captures verbal codes (slang, humor) but not visual codes (the difference between a wellness brand photo and a real home kitchen photo).
3. **Emotional mode mapping.** Which tribal artifacts serve TENSION (common enemies, wounds), which serve RECOGNITION (daily rituals, insider language), which serve VULNERABILITY (core anxieties, unspoken fears)?
4. **Anti-aspirational markers.** What does the tribe REJECT as performative, fake, or "not us"? This is critical for H4's anti-stock filtering and H5's Visual Authenticity Gate.

**Dependency:** H9 depends on H11 (Raw Target Audience Research) to provide the raw material for deeper extraction. The current Extraction Engine processes a `tribe_deep_research_document` but no formal protocol exists for producing that document to the required depth.

---

### H8 — Coach Soul Values (Score: 7.90 — HIGH)

**Why it builds alongside H10:** `Conscious_Soul_Values.md` is the existing output that H8 would upgrade. Currently it contains: core values (6), internal temperature (5 topics), unique metaphors (6), emotional vocabulary (14 words), voice blueprint, and signature perspective. This is rich for a static extraction — but it is missing:

1. **Monthly update mechanism.** As the coach produces new transcripts, the soul values should be refined — not just appended but re-evaluated. A metaphor that was provisional in month 1 may have become a signature by month 6. A value that was stated clearly may have evolved into something more nuanced.
2. **Contradiction tracking.** Where the coach's values in transcript 12 conflict with their values in transcript 1 — this is not a bug, it is depth. The evolution itself becomes content fuel.
3. **Mode-typed values.** Which soul values serve TENSION (the coach's decisive claim against the mainstream), which serve VULNERABILITY (the personal cost of holding these beliefs), which serve RECOGNITION (the values the tribe already holds but can't articulate)?

**The H8 + H10 relationship:** H10 (Coach Philosophy Brief) is the strategic document — the depth-stratified, story-indexed philosophy. H8 (Coach Soul Values) is the operational file — the JSON that every downstream agent reads. H10 informs the updating of H8. They are two views of the same intelligence, at different levels of abstraction.

---

### H11 — Raw Target Audience Research (Score: 7.55 — HIGH)

**Why it matters:** The Deep Target Audience Research Planner exists (7-dimensional framework, 90 lines) and produces a 220-240 word plan for AI research tools. But the gap is enormous: **the plan is produced, but no analyst processes the raw output into a structured brief.** The pipeline currently goes: Planner → raw research → ??? → Tribe Soul Extraction Engine. The missing step is the analyst that produces a 2200-2400 word Target Audience Research Brief.

**Proposed flow:**
```
Target Audience Research Planner (existing)
    → Raw Target Audience Research (H11 — 4000 words)
    → Coach Philosophy × Target Audience Analyst (NEW)
    → Target Audience Research Brief (2200-2400 words)
    → Feeds H9 (Soul Tribe Profile extraction)
```

**The critical innovation:** The analyst should process the raw research through the lens of the Coach's Philosophy (H10). The tribe is not studied in isolation — they are studied in relation to this specific coach's worldview. "What does this tribe fear?" is a generic question. "What does this tribe fear that this coach's philosophy directly addresses — and where does the coach's philosophy accidentally confirm that fear?" is a laws-governed question.

---

### H7 — RAW Fresh Research (Score: 7.25 — HIGH)

**Why it's important but ranks last:** The Fresh Research Protocol already exists (269 lines, browser-verified, 5 query types with temporal constraints). It is the most mature of the existing components. What it lacks is:

1. **Novelty optimization.** The protocol searches for recent information but does not specifically optimize for SURPRISE — information the audience has never encountered. The recency bias opportunity is about presenting facts that feel NEW, not just facts that ARE new.
2. **Surprise density gate.** A quality check after the raw research: "How many of these findings would make the audience say 'I had no idea'?" If the answer is less than 3 out of every 10 findings, the research is timely but not surprising.
3. **Vibe bait identification.** Fresh findings that can visually represent something the audience would recognize immediately — a trending cultural moment, a viral reference, a recent event that the tribe experienced collectively. This creates immediate engagement because the audience sees something they JUST experienced.

**Execution model:** Per blueprint, alongside H6. The 4000-word RAW Fresh Research runs for each blueprint, optimized for novelty and surprise, then the existing Fresh Research Analyst distills into a 1000-1200 word brief.

---

## 7. Build Order Recommendation

Based on the dependency analysis and MCDA scoring:

```
PHASE A — Foundational Setup (Build First)
  H10: Coach Philosophy Brief      ← Nothing exists. Everything depends on it.
  H8:  Coach Soul Values Update     ← Builds alongside H10. Same intelligence, different format.

PHASE B — Audience Intelligence (Build Second)
  H11: Raw Target Audience Research ← Feeds H9. Must exist before tribe depth is possible.
  H9:  Soul Tribe Profiles          ← Receives H11 output. Produces depth-stratified tribe intelligence.

PHASE C — Per-Blueprint Research (Build Third)
  H6:  RAW Deep Research (CCF)      ← Per blueprint. Storytelling + visual fuel optimized.
  H7:  RAW Fresh Research (CCF)     ← Per blueprint. Novelty + surprise optimized.



**Dependency chain:** H10+H8 → H11 → H9 → H6+H7

**The logic:** You cannot research a tribe deeply (H9) without first doing the raw target audience research (H11). You cannot optimize research for a coach's worldview (H6/H7) without first extracting that worldview (H10). You cannot update the operational files (H8) without the strategic brief (H10). The build order follows the dependency graph — not arbitrary priority.

---


## 9. Architectural Constants for New Hypotheses

| Constant | Value | Applies To |
|:---------|:------|:-----------|
| RAW research word count | 4000 words | H6, H7, H11 |
| Analyst brief word count | 1000-1200 words | H6→Analyst, H7→Analyst |
| Target audience brief | 2200-2400 words | H11→Analyst |
| Coach philosophy update cycle | Monthly | H10, H8 |
| Tribe profile update cycle | Per theme | H9 |
| Novelty surprise density | ≥3/10 findings | H7 |
| Visual fuel tagging | Required per finding | H6 |
| Depth stratification | L1 (Surface) / L2 (Mechanism) / L3 (Collision) | H10, H9, H11 |

---

*Pending: User decision on which hypotheses to approve for individual implementation documentation.*
