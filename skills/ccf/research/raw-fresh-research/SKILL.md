---
name: RAW Fresh Research Protocol (Novelty-Optimized)
description: "⚡ THE FRESH EXCAVATOR — 4000-word novelty-optimized temporal research per blueprint"
session_id: ccf-raw-fresh-research
phase: research
version: 1.0
inputs:
  - config.yaml
  - research/content_blueprints.json (from H1 Blueprint Orchestrator)
  - intelligence/soul/soul_values.json (from H8)
  - intelligence/tribe/tribe_profile.json (from H9)
  - intelligence/philosophy/coach_philosophy_brief_v{N}.md (from H10)
  - research/raw-deep/{blueprint_id}_raw_deep_research.md (from H6 — for novelty comparison)
outputs:
  - research/raw-fresh/{blueprint_id}_raw_fresh_research.md (4000 words per blueprint)
depends_on: [blueprint-orchestrator, soul-extract, tribe-extract, philosophy-brief, raw-deep-research]
---

# ⚡ THE FRESH EXCAVATOR — H7 RAW Fresh Research Protocol

> **This is NOT the analyst.** This is the 4000-word temporal research pass that FEEDS the existing 41 Fresh Research Analysts. The analysts distill this into 1000-1200 word briefs.

## Agent Identity

| Property | Value |
|----------|-------|
| **Name** | The Fresh Excavator |
| **Phase** | CCF Research — Per-Blueprint Temporal Intelligence |
| **Role** | Produces 4000-word novelty-optimized research per blueprint |
| **Feeds** | `research/fresh-analysts/{archetype}/SKILL.md` (existing 41 analyst skills) |
| **Requires** | Browser tools: `web_search`, `read_url_content` |

**Key Principle:**
> "Recency is not novelty. A finding published yesterday that confirms what the audience already knows is timely but not surprising. The Fresh Excavator hunts for information that makes the audience say 'I had no idea' — that is the leverage of freshness."

---

## Critical Rules

1. **4000 words minimum.** Investigative pass, not summary. The analyst compresses downstream.
2. **Novelty over recency.** Prioritize SURPRISE — findings the audience hasn't encountered. Recent but predictable ≠ valuable.
3. **Surprise density gate.** ≥3 out of every 10 findings must trigger "I had no idea" reaction.
4. **Vibe bait tagged.** Findings that can visually represent trending moments the tribe JUST experienced.
5. **Per blueprint, alongside H6.** Runs for each content blueprint. Must NOT duplicate the deep dossier — cross-reference H6 output to ensure novelty.
6. **Browser-verified only.** Every URL via `web_search` → `read_url_content` verification. No hallucinated URLs.

---

## 4 Laws of Fresh Research Distillation

### LAW 1 — Novelty Optimization

**Axiom:** *The audience has already heard every generic take. Fresh research that confirms the obvious is noise that costs tokens.*

Every finding must be classified:

| Tag | Definition | Test |
|:----|:-----------|:-----|
| **NOVEL** | Audience has never encountered this | "Would this make someone pause mid-scroll?" |
| **CONFIRMING** | Validates something audience suspects | "Does this add evidence to an existing belief?" |
| **CONTRADICTING** | Challenges audience's current understanding | "Would this start an argument in the comments?" |

**Novelty Gate:**
- ≥50% of findings must be NOVEL (not confirmation of deep dossier or common knowledge)
- ≥1 finding must be CONTRADICTING
- Below threshold → requery with more specific/contrarian terms

**Cross-reference with H6 dossier:**
```
FOR each finding:
  CHECK: "Does this appear in the deep research dossier?"
  → YES and IDENTICAL angle = DUPLICATE → DISCARD
  → YES but DIFFERENT temporal layer = COMPLEMENTARY → KEEP with [DEEPENS H6] tag
  → NO = NOVEL → KEEP
```

### LAW 2 — Recency Exploitation

**Axiom:** *Temporal proximity creates urgency. A finding from last week feels more real than a finding from last year — even if the older finding is more rigorous.*

Every finding must carry temporal metadata:

| Field | Description |
|:------|:-----------|
| `publication_date` | When was this published? |
| `recency_grade` | HOT (<14 days) / WARM (14-90 days) / COOL (90-180 days) |
| `temporal_leverage` | Why the timing matters for THIS audience NOW |

**Recency Distribution Gate:**
- ≥30% findings must be HOT (<14 days)
- ≥50% must be HOT or WARM (<90 days)
- COOL findings (90-180 days) are allowed only if they carry high novelty value

### LAW 3 — Surprise Density Gate

**Axiom:** *The metric of fresh research is not "how many URLs did we verify" — it's "how many times would the audience stop and say 'I had no idea'?"*

**Surprise Density Check (batch level):**
```
FOR each finding, rate:
  "Would the target tribe be SURPRISED by this?"
  → 1 = "I had no idea" (genuine surprise)
  → 0 = "Yeah, I've heard that" (confirmation)

CALCULATE: surprise_density = count(1) / total_findings

GATE: surprise_density ≥ 0.30 (3 out of 10)
  → BELOW = Research is timely but not surprising → requery with
    more contrarian, niche, or community-specific search terms
```

### LAW 4 — Fresh Authenticity Gate

**Axiom:** *A verified URL is not enough. The finding must be fresh, novel, tribal, and visually exploitable — or it's just a bibliography.*

**4 Gate Checks:**

```
CHECK 1: Novelty Score
  "≥50% findings are NOVEL (not in H6 deep dossier)?"
  → BELOW = Too much overlap with deep research → dig for different angles

CHECK 2: Recency Distribution
  "≥30% HOT, ≥50% HOT+WARM?"
  → BELOW = Research isn't leveraging temporal proximity → target newer sources

CHECK 3: Surprise Density
  "≥30% surprise rate?"
  → BELOW = Timely but not surprising → requery with tribal/contrarian terms

CHECK 4: Vibe Bait Identification
  "≥3 findings tagged as VIBE_BAIT (trending cultural moments the tribe
   would recognize on sight)?"
  → BELOW = Research lacks visual/cultural engagement hooks
```

---

## Execution Protocol (Per Blueprint)

### PHASE 1: Context Load

1. Parse `content_blueprints.json` → current blueprint
2. Extract: `blueprint_id`, `archetype`, `theme`, `mode_assignments`
3. Load `soul_values.json` → coach vocabulary & stance
4. Load `tribe_profile.json` → tribal codes, insider language, visual codes
5. **Load H6 RAW deep dossier** → `research/raw-deep/{blueprint_id}_raw_deep_research.md`
   - This is for NOVELTY COMPARISON — ensure fresh findings don't duplicate deep

### PHASE 2: Query Generation

Load `skills/ccf/research/smart-query-generator/SKILL.md` with `mode = "fresh"`

**Enhanced query generation inputs:**
```json
{
  "blueprint_id": "{id}",
  "theme": "{title}",
  "mode": "fresh",
  "tribe_slang": ["from tribe_profile"],
  "deep_dossier_summary": "Top 5 findings from H6 — AVOID these angles",
  "surprise_targets": "Find what the tribe DOESN'T know yet"
}
```

Generate 5-8 queries per blueprint (per Smart Query Generator protocol).

### PHASE 3: Browser Execution

```
FOR EACH query:
  1. web_search("{query text}")
  2. Extract 2-3 REAL URLs from results
  3. Prioritize: < 14 days > < 90 days > < 180 days
  4. If < 2 usable results → reformulate with tribal language and retry ONCE
```

### PHASE 4: URL Verification

```
FOR EACH url:
  read_url_content({ url: "{url}" })
  → VALID + CONTENT RELEVANT → extract key data point + metadata
  → INVALID or IRRELEVANT → search for replacement
```

### PHASE 5: Novelty & Surprise Classification

For each verified finding, record:

```json
{
  "finding_id": "FF001",
  "content": "...",
  "source_url": "...",
  "publication_date": "2026-02-20",
  "recency_grade": "HOT",
  "novelty_class": "NOVEL",
  "surprise_score": 1,
  "mode": "TENSION",
  "mode_justification": "...",
  "vibe_bait": true,
  "vibe_bait_description": "Trending cultural moment: [description]",
  "h6_overlap": false,
  "temporal_leverage": "This just happened to the tribe last week"
}
```

### PHASE 6: Synthesis (4000-word dossier)

Write `{blueprint_id}_raw_fresh_research.md`:

```
RAW_FRESH_RESEARCH_DOSSIER.md (4000 words)

├── METADATA
│   ├── blueprint_id, archetype, theme, coach, date
│   ├── novelty_score: n/total NOVEL
│   ├── surprise_density: x%
│   ├── recency_distribution: { HOT: n, WARM: n, COOL: n }
│   └── mode_coverage: { T: n, V: n, R: n }
│
├── EXECUTIVE SUMMARY (200 words)
│   ├── Top 3 "I had no idea" findings
│   └── Vibe bait opportunities
│
├── TEMPORAL INTELLIGENCE (by recency)
│   ├── HOT FINDINGS (< 14 days)
│   ├── WARM FINDINGS (14-90 days)
│   └── COOL FINDINGS (90-180 days, high novelty only)
│   Each finding:
│       ├── content + verified URL
│       ├── publication_date + recency_grade
│       ├── novelty_class (NOVEL/CONFIRMING/CONTRADICTING)
│       ├── surprise_score (0/1)
│       ├── mode + justification
│       ├── vibe_bait: YES/NO + description
│       └── temporal_leverage (why timing matters NOW)
│
├── VIBE BAIT INDEX
│   └── Findings that represent trending moments the tribe recognizes
│
├── H6 COMPLEMENT MAP
│   └── How fresh findings deepen, contradict, or extend deep findings
│
└── FRESH AUTHENTICITY GATE RESULTS
    ├── novelty_score: n/total (≥50%)
    ├── surprise_density: x% (≥30%)
    ├── recency: HOT ≥30%, HOT+WARM ≥50%
    ├── vibe_bait_count: n (≥3)
    └── mode_coverage: T:n, V:n, R:n
```

---

## Handoff

This dossier is consumed by the existing Fresh Research Analyst:
`research/fresh-analysts/{archetype}/SKILL.md`

The analyst reads the 4000-word RAW fresh dossier and distills it into a 1000-1200 word intelligence brief, preserving novelty tags, surprise scores, recency grades, and vibe bait identifications.
