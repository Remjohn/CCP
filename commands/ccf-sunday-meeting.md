---
name: ccf-sunday-meeting
description: "Weekly System Administrator — Runs metrics on Trigger Map expansion, MATRL health, and pipeline throughput."
---

# /ccf-sunday-meeting {client_name}

// turbo-all

> **SKILLS_BASE:** `ccf-26/skills/ccf/`
> **PHASE:** weekly (Administrator)

**Objective:**
Self-Sustaining Loop Metrics (Item 24). Evaluates the health of the CCF v3.1 architecture, specifically focusing on the Trigger Map Expansion and Neural Coupling quality over the past week.

---

## 🎯 STEP 0: INITIALIZE DOSSIER

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "PRE-FLIGHT - Validate config and memory files exist", status: "pending" },
    { id: "step-2", description: "TRIGGER METRICS - Measure map expansion and degradation", status: "pending" },
    { id: "step-3", description: "COUPLING METRICS - Measure Script Analyst scores", status: "pending" },
    { id: "step-4", description: "SYSTEM HEALTH - Report to administrator", status: "pending" }
  ]
});
```

---

## STEP 1: PRE-FLIGHT

Mark step-1 `in_progress`.

Load the core data states:
- `intelligence_library/trigger_map.json`
- `logs/ccf_experience_pool.json`
- `validation/analysis/*_analysis_report.json` (from current week)

Mark step-1 `completed`.

---

## STEP 2: TRIGGER MAP METRICS

Mark step-2 `in_progress`.

Spawn `Metrics_Agent` to evaluate `trigger_map.json`:
1. Count total active triggers.
2. Identify any triggers flagged as "degrading" (from Authenticity Score Feedback loop).
3. Identify newly mapped triggers (added this week).
4. Evaluate PTG safety (any triggers regressing to `raw_unresolved`).

Mark step-2 `completed`.

---

## STEP 3: NEURAL COUPLING METRICS

Mark step-3 `in_progress`.

Evaluate the Script Analyst reports for the week:
1. Aggregate the "Neural Coupling Prediction Score" across all scripts.
2. Determine the Average Coupling Score.
3. Count how many scripts scored `< 7` and required a Commander Rewrite.
4. Calculate Rewrite Ratio (Rewrites / Total Scripts).

Mark step-3 `completed`.

---

## STEP 4: SYSTEM HEALTH REPORT

Mark step-4 `in_progress`.

Generate the Weekly Health Digest in console:

```
📊 CCF V3.1 SUNDAY METRICS — {client_name}

🗺️ Trigger Map Health:
- Total Active Triggers: {N}
- New Triggers Discovered: +{N}
- Degrading Triggers: {N} (Requires coaching attention)
- PTG Safety Breaches: {N}

🧠 Neural Coupling Performance:
- Average Coupling Score: {X}/10
- Commander Rewrite Rate: {X}%
- Dominant Trigger Attempted: {trigger_id}

🛠️ MATRL Experience Pool:
- New False-Negative Logs Added: {N}
- New High-Performance Plays Added: {N}

RECOMMENDATION FOR NEXT WEEK:
{If rewrite rate > 30% -> "Refine generative grammar prompt instructions"}
{If degrading triggers > 0 -> "Trigger Calibration Protocol must be run"}
```

Mark step-4 `completed`.
