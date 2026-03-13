# H7: RAW Fresh Research (CCF) — Implementation Architecture

**Hypothesis:** The 41 fresh research analyst skills produce 500-600 word briefs with current data but without temporal classification, mode typing, or cross-validation with the deep research dossier. Fresh findings arrive as isolated news clippings rather than as confirmation, contradiction, or expansion of established deep research.

**Pipeline Position:** CCF Research Phase → Fresh Analyst → Fresh Research Brief → feeds Script/Visual pipeline (alongside Deep Dossier)  
**Existing Infrastructure:** `_FRESH_RESEARCH_PROTOCOL.md`, 41 archetype-specific `fresh-analysts/` skills, Smart Query Generator  
**Gap Classification:** MEDIUM — Infrastructure works (query generation, search API, caching) but outputs lack relational metadata  
**Dependency:** Receives blueprint from H1, soul_values from H8/H10, SHOULD receive deep dossier from H6

---

## Section 1: The Input Quality Problem

The Fresh Analyst currently receives `content_blueprints.json` and `soul_values.json` as inputs. It does NOT receive the Deep Research Dossier. This means fresh findings are produced in isolation — the fresh analyst doesn't know what the deep research already established, so it cannot classify findings as confirming, contradicting, or expanding the deep findings.

### Input Saturation Gate

| Input | Minimum Requirement | Source |
|:------|:-------------------|:-------|
| `content_blueprints.json` | Must contain archetype + mode assignment | H1 output |
| `soul_values.json` | Must be loaded for Tone Emulation | H8/H10 output |
| **`Deep_Research_Dossier.md` (NEW)** | Must be loaded as reference baseline | H6 output |

**Saturation test:** Fresh research cannot be produced without the deep dossier as baseline context. Without it, the fresh analyst has no reference for what is "new" vs. "already known."

---

## Section 2: The 4 Laws of Fresh Research Distillation

### Law 1 — Temporal Relevance Classification

**Axiom:** *Recency without classification is a timestamp, not intelligence.*

Every fresh finding gains a `temporal_type`:

| Type | Definition | Downstream Signal |
|:-----|:-----------|:-----------------|
| **trend-validating** | Confirms what deep research established | "This is still true" — authority reinforcement |
| **trend-contradicting** | Challenges or nuances deep findings | "Wait, this is more complicated" — productive tension |
| **event-triggered** | Tied to a specific current event | "This is happening RIGHT NOW" — urgency |
| **culturally-timed** | Tied to cultural calendar/moment | "This matters to the tribe THIS WEEK" — relevance |

**Classification Test:**
```
"This finding is [temporal_type] because:
 - It [confirms/contradicts/is triggered by/coincides with] _____.
 - The deep dossier said _____ about this topic.
 - This new data means _____."

→ All fields filled = PASS
→ Cannot reference deep dossier = fresh analyst is operating in isolation → FLAG
```

**Where this integrates:** Fresh research brief output gains `temporal_type` and `deep_reference` per finding.

### Law 2 — Fresh Mode Typing

**Axiom:** *A fresh statistic can be a weapon, a wound, or a validation — the mode determines which.*

Same structure as H6 Law 1. Every fresh finding tagged: `mode` (T/V/R), `mode_justification`, `deployment_recommendation`.

**Mode Classification Test (identical to H6):**
```
"This finding documents _____ (what) and serves _____ mode (why)
 because it makes the viewer feel _____ (how)."
```

**Where this integrates:** Fresh brief per-finding metadata.

### Law 3 — Deep-Fresh Cross-Validation

**Axiom:** *Fresh research that doesn't reference deep research is a news clipping. Deep research that fresh data doesn't confirm is aging theory.*

Each fresh finding must explicitly link to the deep dossier:

```json
{
  "finding": "...",
  "temporal_type": "trend-validating",
  "mode": "TENSION",
  "deep_reference": {
    "angle": "Scientific",
    "finding_id": "W1-R-01",
    "relationship": "confirms",
    "relationship_detail": "Deep dossier cited 2019 microbiome study; this 2025 follow-up confirms same pattern in larger population"
  }
}
```

**Relationship types:**
- **confirms:** New data validates deep finding → HIGH authority signal
- **challenges:** New data contradicts or nuances → content opportunity for productive tension
- **expands:** New data adds dimension the deep research missed → depth expansion
- **independent:** No relationship found → supplementary only

**Where this integrates:** Fresh analyst INGEST phase adds deep dossier as required input. Output format includes `deep_reference` per finding.

### Law 4 — Fresh Research Authenticity Gate

**Axiom:** *Recent doesn't mean relevant. A 2025 article that says nothing a 2020 article didn't say is not fresh research — it's a cached opinion.*

**4 Gate Checks (per finding):**

```
CHECK 1: Novelty Test
  "Does this finding contain information NOT present in the deep dossier?"
  → NO = REDUNDANT (discard or mark as confirmation-only)
  → YES = NOVEL

CHECK 2: Mode Tag Present
  "Is this finding tagged T/V/R?"
  → NO = UNCLASSIFIED → classify before including

CHECK 3: Temporal Classification Present
  "Is this finding tagged with temporal_type?"
  → NO = UNCLASSIFIED → classify before including

CHECK 4: Source Quality
  "Is the source credible, specific, and verifiable?"
  → Generic/SEO blog = REJECT
  → Named expert, study, or verifiable event = PASS
```

**Where this integrates:** New validation step in fresh analyst I-R-E-V-C VALIDATE phase, mirroring H6's Critic Loop.

---

## Section 3: Output Format Enhancement

```
Fresh_Research_Brief.md (enhanced)

├── "The Proof Is In" Opening
│
├── Findings (3-4 items)
│   └── Per finding:
│       ├── content (existing)
│       ├── temporal_type: trend-validating | trend-contradicting | event-triggered | culturally-timed
│       ├── mode: T | V | R
│       ├── mode_justification: "..."
│       ├── deep_reference: { angle, finding_id, relationship, detail }
│       ├── novelty: NOVEL | CONFIRMATION_ONLY
│       └── source_url (existing)
│
├── "Bottom Line" (existing)
│
└── FRESH RESEARCH GATE RESULTS
    ├── novel_findings: n / total
    ├── mode_distribution: T: n, V: n, R: n
    ├── temporal_types: validating: n, contradicting: n, event: n, cultural: n
    └── deep_cross_references: n / total linked to deep dossier
```

---

## Section 4: 5 Micro-Hypothesis Evaluations

**MH1 — Deep-Fresh Linkage Test:** Every fresh finding must reference a deep dossier finding or be explicitly marked "independent." ≥60% must have a direct link. Verifiable: count `deep_reference` fields.

**MH2 — Novelty Test:** ≥50% of findings must be NOVEL (contain info not in deep dossier). If all findings are confirmation-only, the fresh research added no value. Verifiable: count `novelty: NOVEL` entries.

**MH3 — Temporal Classification Coverage:** All findings must have a `temporal_type`. Verifiable: check field presence.

**MH4 — Mode Presence:** All findings must have a mode tag. Verifiable: check `mode` field presence.

**MH5 — Source Quality:** No findings from generic/SEO sources. All must cite named experts, studies, or verifiable events. Verifiable: inspect source URLs for quality.

---

## Validation Receipt

```
H7 VALIDATION RECEIPT
━━━━━━━━━━━━━━━━━━━━━
Blueprint:       [ID]
Archetype:       [type]
Coach:           [name]
Date:            [timestamp]
Deep Dossier:    [version referenced]
Queries:         [n] executed

LAW COMPLIANCE
━━━━━━━━━━━━━━
Law 1 — Temporal Classification:  [validating: n, contradicting: n, event: n, cultural: n]  [PASS/FAIL]
Law 2 — Mode Typing:              [T: n, V: n, R: n]  [PASS/FAIL]
Law 3 — Deep-Fresh Linkage:       [n/total linked = x%]  [PASS/FAIL if <60%]
Law 4 — Authenticity Gate:        [4/4 checks per finding]  [PASS/FAIL]

MICRO-HYPOTHESES
━━━━━━━━━━━━━━━━
MH1 Deep Linkage:       [x% linked]  [PASS/FAIL if <60%]
MH2 Novelty:            [x% novel]  [PASS/FAIL if <50%]
MH3 Temporal Coverage:  [PASS/FAIL]
MH4 Mode Presence:      [PASS/FAIL]
MH5 Source Quality:     [PASS/FAIL]

STATUS: [AUTHENTICATED / PROVISIONAL / FAILED]
```
