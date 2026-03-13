# First-Principles Analysis: What H6 Is Missing

## What H6 Maps To

H6 (RAW Deep Research) maps to the 41 archetype-specific **deep analyst** skills in `ccf-26/skills/ccf/research/deep-analysts/` plus the shared `_DEEP_RESEARCH_PROTOCOL.md`. These are the agents that produce deep research dossiers (1600-2200 words) for each content blueprint.

---

## What the Actual Pipeline Does

### _DEEP_RESEARCH_PROTOCOL.md (83 lines) — Shared Across All 41 Deep Analysts

**Architecture:** 5-phase agentic loop:

1. **Strategy Director (The Brain):**
   - Input: `strategy_brief.json`, `soul_values.md`
   - Loads strategy-director SKILL
   - Analyzes coach's "Signature Perspective" via 7-Angle Framework
   - Produces `conscious_research_plan.json` — 3 high-specificity queries per vector

2. **Agentic Execution Loop (The Body):**
   - Engine: Firecrawl CLI (NOT generic web_search)
   - For each of 7 Vectors: Historical, Scientific, Philosophical, Contrarian, Practical, Strategic, Tribal
   - Step A: Scout (wide search, 5-10 URLs)
   - Step B: Deep Dive (full markdown extraction, specific data points)

3. **Critic Loop (The Conscience):**
   - Reviews findings against Authority Rubric
   - Rejects: generic findings
   - Approves: primary sources, soul-challenging/reinforcing findings
   - Issues "Dig Deeper Directive" for retries

4. **Synergist (The Synthesis):**
   - Executive Summary (One Big Idea connecting all vectors)
   - 7-Angle Analysis (200-300 words each, verified citations)
   - Synergy Map (how Scientific proves Mythological, etc.)
   - Trend Signals (future implications)

5. **Output:** `Deep_Research_Dossier.md` (1600-2200 words)

### Sample Archetype: top-reliable-list Deep Analyst (161 lines)

**Identity:** "The Lead Researcher" — expert in credible, authoritative, timeless information.

**Analytical Framework:**
- A. Framework-Biased Analysis Protocol (guided by `content_frameworks_used`)
- B. Foundational Principles (500-600 words) — 2-3 first-principle truths
- C. Proven Strategies & Tactics (500-600 words) — 3-4 step-by-step strategies
- D. Expert Consensus & Validation (400-500 words) — expert quotes, study findings

**Tone Emulation:** Loads `soul_values.json`, writes as if coach personally researched the topic.

**Validation checks:** Contains timeless principles, historical patterns, specific data points, coach's voice, no generic/Wikipedia content.

---

## The Gap: What H6's Deep Research Phase Misses

### 1. No Emotional Typing of Research Findings

The 7-Angle Framework (Historical, Scientific, Philosophical, Contrarian, Practical, Strategic, Tribal) is a content-type classification, not an emotional-mode classification. A finding from the "Contrarian" angle could serve TENSION mode (confronting the mainstream), VULNERABILITY mode (revealing the coach's own doubt), or RECOGNITION mode (validating the tribe's suspicion).

The current pipeline tags findings by ANGLE but not by MODE (T/V/R). This means the downstream script generator receives research organized by intellectual category but not by emotional function.

| Research Finding | Angle (Current) | Mode (Missing) |
|:---|:---|:---|
| "80% of Afrodescendant women in Belgium show gut microbiome depletion within 5 years of immigration" | Scientific | **TENSION** — systemic evidence of harm |
| "Traditional Congolese root vegetables contain 3x the microbial diversity of European organic produce" | Scientific | **RECOGNITION** — ancestral wisdom validated by science |
| "A naturopath in Geneva reversed 40 cases of postpartum depression using traditional African plant protocols" | Practical | **VULNERABILITY → RECOGNITION** — from pain to proof |
| "European medical training has zero hours dedicated to Afrodescendant-specific health conditions" | Contrarian | **TENSION** — institutional failure documented |

Without mode tagging, the script generator must infer the emotional function of each finding — an inference that may be wrong.

### 2. No Depth Stratification of Sources

The Critic Loop checks: Is it generic? (REJECT) / Is it a primary source? (APPROVE) / Does it reinforce or challenge soul values? (APPROVE).

But it doesn't stratify approved sources by depth:

| Source Type | Depth | Example | Current Treatment |
|:---|:---|:---|:---|
| News article summarizing a study | L1 (Surface) | "Study finds gut health affects mood" | ✅ Approved if not generic |
| The actual study with methodology | L2 (Mechanism) | "Gut-brain axis signaling in migrant populations: a 5-year longitudinal study" | ✅ Same approval level |
| A finding that contradicts the coach's stated belief | L3 (Collision) | "Traditional African diets alone are insufficient in European climate — local adaptation required" | ✅ Same approval level |

All three are approved and appear in the dossier with equal weight. The downstream script generator has no signal for which findings are surface-level context vs. mechanism-level proof vs. worldview-challenging depth.

### 3. No Beat-Mode Alignment Check

The Strategy Director creates a research plan from `strategy_brief.json` and `soul_values.json`. But the research plan doesn't reference the content blueprint's mode assignments.

In the full CCF pipeline, by the time research runs, the blueprint already exists with mode assignments per section (e.g., "Opening: TENSION, Core strategy #1: RECOGNITION, Proof: VULNERABILITY"). The research plan should be mode-aware — deliberately seeking TENSION-serving evidence for TENSION sections and RECOGNITION-serving evidence for RECOGNITION sections.

Currently, research is mode-blind: 7 vectors × 3 queries = 21 queries, all generated from a subject/angle matrix without knowing what emotional function the content will need.

### 4. No Tribe-Invisible Detail Test

The Critic Loop checks for "generic" vs. "primary source" but doesn't test whether a finding contains a detail that would be invisible to an outsider but obvious to the tribe.

From the Coach Adele context:
- **Tribe-invisible:** "Matembélé consumption correlates with gut microbiome resilience in Congolese diaspora" — only Congolese people know what matembélé IS
- **Tribe-visible (generic):** "Eating local traditional foods supports gut health" — anyone would know this

The tribe-invisible detail is what makes research feel like the coach's own intelligence, not a Google summary. The current pipeline has no mechanism to prioritize these.

---

## The 4 Derived Laws for H6

### Law 1 — Law of Research Emotional Typing

**Axiom:** "Research without emotional classification is ammunition without a target. The pipeline cannot deploy findings to the right content mode if it doesn't know which mode they serve."

Every research finding across all 7 angles must be tagged with: mode (T/V/R), mode justification (why this finding serves this mode), and deployment recommendation (which content section it naturally feeds).

**Where this integrates:** The Synergy Map in Phase 4 gains a `mode` field per finding.

### Law 2 — Law of Source Depth Stratification

**Axiom:** "A news article and a longitudinal study cannot have the same weight. Depth without classification is noise with a bibliography."

Every approved source must be tagged L1 (Surface — summaries, news, commentary), L2 (Mechanism — studies, methodologies, expert analyses), or L3 (Collision — findings that challenge or complicate the coach's stated position). Minimum depth distribution: ≥30% L2, ≥10% L3. Below threshold triggers a "Dig Deeper Directive" from the Critic.

**Where this integrates:** The Critic Loop (Phase 3) adds depth assessment alongside the existing generic/primary/soul-alignment checks.

### Law 3 — Law of Beat-Mode Alignment

**Axiom:** "Research that doesn't know its destination arrives everywhere and serves nowhere."

The Strategy Director must receive the blueprint's mode assignments as input. The 7-angle × 3-query matrix must include a `target_mode` field per query, ensuring that each research vector deliberately serves a specific content mode requirement.

**Where this integrates:** The Strategy Director's `conscious_research_plan.json` gains `target_mode` and `blueprint_section` fields per query.

### Law 4 — Law of Research Authenticity Gate

**Axiom:** "If a competitor could use this finding without changing a word, it's not tribal research — it's a Google search."

Gate checks:
1. **Tribe-invisible detail:** ≥20% of findings contain detail invisible to an outsider
2. **Depth distribution:** ≥30% L2, ≥10% L3
3. **Mode coverage:** Findings span all 3 modes (T/V/R)
4. **Soul-challenge presence:** ≥1 finding that CHALLENGES the coach's stated position (L3 collision)

**Where this integrates:** Added to the Critic Loop as a final batch validation before synthesis.

---

## Current vs. Law-Governed Comparison

| What Happens Now | What Happens With Laws |
|:---|:---|
| 7-angle research organized by intellectual category | Findings also mode-tagged (T/V/R) for emotional deployment |
| Critic checks: generic vs. primary | Critic also checks: L1/L2/L3 depth with minimum thresholds |
| Research plan blind to content mode | Strategy Director receives blueprint mode assignments as input |
| "Not generic" as quality floor | Tribe-invisible detail as quality ceiling |
| All findings equally weighted | Depth-stratified: surface context vs mechanism proof vs collision depth |

---

*This analysis grounds the H6 implementation architecture document. The 4 laws (Research Emotional Typing, Source Depth Stratification, Beat-Mode Alignment, Research Authenticity Gate) are derived from gaps in `_DEEP_RESEARCH_PROTOCOL.md` (5-phase agentic loop) and the archetype-specific `top-reliable-list` deep analyst, illustrated with Coach Adele's content domain as a real CCF use case.*
