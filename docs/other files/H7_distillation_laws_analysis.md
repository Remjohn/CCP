# First-Principles Analysis: What H7 Is Missing

## What H7 Maps To

H7 (RAW Fresh Research) maps to the 41 archetype-specific **fresh analyst** skills in `ccf-26/skills/ccf/research/fresh-analysts/` plus the shared `_FRESH_RESEARCH_PROTOCOL.md`. These produce short, hyper-current research briefs (500-600 words) that complement the deep research dossiers.

---

## What the Actual Pipeline Does

### Fresh Analyst Architecture (Sample: top-reliable-list, 171 lines)

**Identity:** "The Fact-Checker" — scans real-time data for the most potent tactical intelligence.

**Output:** `fresh_research_brief.md` (500-600 words) containing:
- A. Framework-Biased Analysis Protocol (same as deep)
- B. The Latest Validating Statistic (150-200 words) — last 6 months, confirms a timeless principle
- C. The Recent Proof-in-Action Case Study (200-250 words) — last 12 months, demonstrates strategy in action
- D. The Timely Expert Endorsement (150-200 words) — recent quote from credible authority

**Real-Time Search Integration:**
1. Smart Query Generator creates 5-8 targeted queries
2. Queries executed via search API (Tavily or SerpApi)
3. Results filtered for: recency (<6 months), relevance, authority
4. 24-hour result caching by query hash

**Validation:** Brief contains real dates, specific numbers, recent data points (<6 months), coach's voice, all source citations.

### How Fresh Differs From Deep

| Dimension | Deep (H6) | Fresh (H7) |
|:---|:---|:---|
| **Length** | 1600-2200 words | 500-600 words |
| **Focus** | Timeless principles, proven strategies | Current data, recent proof |
| **Time window** | Any era | Last 6-12 months |
| **Role** | Authority/depth | Currency/urgency |
| **Engine** | Firecrawl CLI (deep scraping) | Smart Query Generator → Search API |
| **Critic Loop** | Yes (3-check rubric) | No explicit critic loop |

---

## The Gap: What H7's Fresh Research Phase Misses

### 1. No Temporal Relevance Classification

The fresh analyst finds "recent" data (last 6-12 months) but doesn't classify WHY a finding is timely:

| Temporal Type | Definition | Example (Coach Adele domain) |
|:---|:---|:---|
| **Trend-validating** | Data that confirms what the deep research already established | "2025 EU study confirms microbiome depletion in immigrant populations — matches 2019 findings" |
| **Trend-contradicting** | Data that challenges or nuances the deep research | "New Rotterdam study shows second-generation Afrodescendants have RECOVERED microbiome diversity — possibly invalidating the 'permanent damage' narrative" |
| **Event-triggered** | Data tied to a specific current event | "Belgian government announces new integration health screening — includes gut health for the first time" |
| **Culturally-timed** | Data tied to cultural calendar | "African Heritage Month features traditional medicine practitioners for the first time in Brussels" |

Without temporal classification, the script generator doesn't know if the fresh research CONFIRMS the deep research (reinforcing authority), CHALLENGES it (creating productive tension), or CONTEXTUALIZES it (making it feel urgent).

### 2. No Mode Classification on Current Findings

Same gap as H6 but with fresh-specific implications. A recent statistic that "postpartum depression rates among African immigrant women have increased 40% since 2020" could serve:
- **TENSION:** The system is failing these women (confrontational deployment)
- **VULNERABILITY:** "This is what happened to me — and now the numbers prove it" (personal deployment)
- **RECOGNITION:** "Your pain is real and it's getting worse — you're not imagining it" (validating deployment)

The fresh analyst delivers the statistic without mode guidance.

### 3. No Deep-Fresh Cross-Validation

The deep and fresh research dossiers are produced independently. The fresh analyst doesn't explicitly reference the deep dossier to check:
- Does the fresh finding REINFORCE a deep principle? (convergence = high authority)
- Does the fresh finding CONTRADICT a deep finding? (divergence = content opportunity)
- Does the fresh finding ADD a new dimension the deep research missed? (expansion = depth)

Currently, the script generator must manually cross-reference the deep and fresh briefs. There's no structured link.

### 4. No Critic Loop for Fresh Research

The deep analyst has a 3-check Critic Loop (generic? primary source? soul-aligned?). The fresh analyst has NO equivalent. Fresh findings go directly from search results to the brief without:
- Generic/primary source filtering
- Soul-alignment check
- Depth stratification

This means fresh briefs can include generic, SEO-optimized recent articles that happen to match the query but contain no tribal depth.

---

## The 4 Derived Laws for H7

### Law 1 — Law of Temporal Relevance Classification

**Axiom:** "Recency without classification is a timestamp, not intelligence. The pipeline needs to know whether new data confirms, challenges, or contextualizes existing research."

Every fresh finding must be tagged: `temporal_type` (trend-validating / trend-contradicting / event-triggered / culturally-timed) and `deep_research_relationship` (confirms / challenges / expands / independent).

**Where this integrates:** The fresh research brief output gains structured metadata per finding.

### Law 2 — Law of Fresh Mode Typing

**Axiom:** "A fresh statistic can be a weapon, a wound, or a validation — the mode determines which."

Every fresh finding must be tagged with mode (T/V/R) and deployment recommendation, following the same pattern as H6 Law 1.

**Where this integrates:** Same structure as H6 — `mode` and `mode_justification` fields per finding.

### Law 3 — Law of Deep-Fresh Cross-Validation

**Axiom:** "Fresh research that doesn't reference deep research is a news clipping. Deep research that fresh data doesn't confirm is aging theory."

The fresh analyst must receive the deep research dossier as an input (currently it only receives `content_blueprints.json` and `soul_values.json`). Each fresh finding must explicitly reference which deep finding it relates to, with the relationship type (confirms / challenges / expands).

**Where this integrates:** The fresh analyst I-R-E-V-C INGEST phase adds the deep research dossier as a required input. The output format includes a `deep_research_link` field per finding.

### Law 4 — Law of Fresh Research Authenticity Gate

**Axiom:** "Recent doesn't mean relevant. A 2025 article that says nothing a 2020 article didn't say is not fresh research — it's a cached opinion."

Gate checks:
1. **Novelty:** Does the finding contain information NOT present in the deep dossier?
2. **Mode tag:** Every finding has T/V/R classification
3. **Temporal classification:** Every finding has a temporal type
4. **Source quality:** Minimum standard equivalent to the deep Critic Loop (not generic, credible source, soul-relevant)

**Where this integrates:** New validation step in the fresh analyst I-R-E-V-C VALIDATE phase, mirroring the deep analyst's Critic Loop.

---

## Current vs. Law-Governed Comparison

| What Happens Now | What Happens With Laws |
|:---|:---|
| "Recent" data = anything from last 6-12 months | Each finding classified by temporal type (trend/event/cultural) |
| No mode tagging on fresh findings | Mode-tagged (T/V/R) with deployment guidance |
| Fresh and deep briefs produced independently | Fresh explicitly cross-references deep (confirms/challenges/expands) |
| No critic loop for fresh analyst | Fresh gets equivalent quality gate (novelty, source quality, soul-alignment) |
| Fresh brief is a self-contained 500-word document | Fresh brief includes structured metadata linking each finding to deep research and content mode |

---

*This analysis grounds the H7 implementation architecture document. The 4 laws (Temporal Relevance Classification, Fresh Mode Typing, Deep-Fresh Cross-Validation, Fresh Research Authenticity Gate) are derived from gaps in the fresh analyst architecture and its relationship to the deep analyst pipeline, using Coach Adele's content domain as a real CCF use case.*
