# 🧬 SHARED PROTOCOL: Deep Research V3.1 (Laws-Governed Analyst)

> **VERSION:** 3.1 (Laws-Governed — consumes H6 RAW dossier)
> **ARCHITECT:** Strategy Director + Critic Loop
> **ENGINE:** Firecrawl CLI (Mandatory)
> **TARGET:** 1,600 - 2,200 Words (Deep Authority Brief)
> **UPSTREAM:** `research/raw-deep/{blueprint_id}_raw_deep_research.md` (4000-word H6 RAW dossier)

> [!IMPORTANT]
> ## H6 RAW Research Integration (V3.1)
> As of V3.1, the Deep Analyst receives a **pre-researched 4000-word RAW dossier** from H6 (`raw-deep-research/SKILL.md`).
> Each finding in the RAW dossier already carries: `mode` (T/V/R), `depth_level` (L1/L2/L3), `storytelling_tag`, `visual_potential`, and `tribe_invisible` metadata.
> **Your job as analyst:** Distill the 4000-word dossier into a 1600-2200 word intelligence brief **preserving these metadata fields** in your output.
> If the H6 RAW dossier is not available, fall back to the original V3 protocol below.

---

## 📜 The Protocol

This protocol defines the **MANDATORY** execution capability for all "Deep Analyst" agents in the CCF ecosystem. You are no longer a linear script. You are part of an **Autonomous Research Hive**.

### Phase 1: The Strategy Director (The Brain) — Trigger Ammunition (Item 19)
**Input:** `strategy_brief.json`, `soul_values.md`, `intelligence_library/trigger_map.json`
1.  **Load Skill:** `skills/ccf/research/strategy-director/SKILL.md`
2.  **Action:** Extract the targeted `trigger_id` for this content batch.
3.  **Design:** Construct a **Conscious Research Plan** (`conscious_research_plan.json`) with 3 high-specificity queries per vector.
    - *Constraint:* Analysts DO NOT hunt for general "topic support." They hunt exclusively for **Trigger Ammunition** — external validation, empirical data, or societal contrast that specifically escalates the tension of the target trigger. If it doesn't feed the trigger, discard it.

### Phase 2: The Agentic Execution Loop (The Body)
 **Input:** `conscious_research_plan.json`
 **Engine:** `python tools/firecrawl_wrapper.py` (Do NOT use generic `web_search`)

**For Each of the 7 Vectors (Historical, Scientific, Philosophical, Contrarian, Practical, Strategic, Tribal):**

#### Step A: The Scout (Wide Search)
- **Command:**
  ```bash
  python tools/firecrawl_wrapper.py search "YOUR QUERY HERE" --limit 5
  ```
- **Goal:** Map the territory. Find 5-10 high-potential URLs.

#### Step B: The Deep Dive (Read & Extract)
- **Command:**
  ```bash
  python tools/firecrawl_wrapper.py scrape "https://VALID-URL.com"
  ```
- **Rule:** Read the FULL Markdown output. Extract specific Data Points, Quotes, and Concepts.
- **Constraint:** If output contains error or is low quality, **DISCARD** and try next result.

### Phase 3: The Critic Loop (The Conscience)
**Input:** Raw findings from Phase 2.
1.  **Load Skill:** `skills/ccf/research/critic/SKILL.md`
2.  **Action:** The Critic reviews the extracted findings against the **Authority Rubric**.
    - *Is it generic?* (REJECT)
    - *Is it a primary source?* (APPROVE)
    - *Does it challenge/reinforce the Soul Value?* (APPROVE)
3.  **Correction:** If REJECTED, the Critic issues a **"Dig Deeper Directive"**.
    - *Loop:* The Analyst must run **one retry cycle** (Phase 2) with the refined directive.

### Phase 4: The Synergist (The Synthesis)
**Input:** Approved findings from all 7 Vectors.
1.  **Action:** Synthesize the "Dossier".
2.  **Structure:**
    - **Executive Summary:** The "One Big Idea" that connects all vectors.
    - **7-Angle Analysis:** Detailed breakdown of each vector with *verified citations*.
    - **The Synergy Map:** How the Scientific proves the Mythological (etc.).
    - **Trend Signals:** Future-looking implications.

### Phase 5: Output Generation
**Format:** `Deep_Research_Dossier.md`

| Section | Content |
| :--- | :--- |
| **Headline** | The "Hook" of the research. |
| **Angle 1...7** | 200-300 words each. **MUST** cite verified URLs. |
| **Data Table** | Verified Statistics, Dates, Names. |
| **Bibliography** | List of all valid Firecrawl URLs. |

---

## 🚫 Forbidden Actions
- **Using Generic Search:** You must use `tools/firecrawl_wrapper.py`.
- **Hallucinating URLs:** If Firecrawl returns error, you cite nothing.
- **Ignoring the Critic:** If the Critic rejects a finding, you CANNOT include it in the final report.
- **Forbidden Sources:** Wikipedia, wikihow, buzzfeed, generic AI blogs.

---

## 🔗 Handoff
This protocol hands off to the **Concept Developer** (Phase 2) who will turn these raw truths into narrative gold.

---

## V3.1 — Preserved Metadata in Analyst Output

When consuming H6 RAW dossier, the analyst brief MUST include per finding:
- `mode`: T/V/R (from RAW dossier)
- `depth_level`: L1/L2/L3 (from RAW dossier)
- `storytelling_tag`: (from RAW dossier)
- `visual_potential`: HIGH/MEDIUM/LOW (from RAW dossier)
- `tribe_invisible`: YES/NO (from RAW dossier)
