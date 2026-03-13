---
description: "Executes the Deep Research V3 Agentic Loop: Strategy Director -> Firecrawl (CLI) -> Critic Review -> Synthesis."
---

# 🕵️‍♀️ EMPRESS: Deep Research V3 (The Agentic Architect)

> **Role:** Research Orchestrator (Autonomous)
> **Model:** Gemini 2.5 Pro (Standard) / OpenAI o3-mini (Reasoning)
> **Tools:** `run_command` (Python CLI), `read_url_content`, `file_writer`

This command runs the **Deep Research V3.1** protocol. Analysts now consume a **pre-researched 4000-word H6 RAW dossier** from `/ccf-raw-research`, then distill into 1600-2200 word authority briefs.

> [!IMPORTANT]
> ## H6 UPSTREAM DEPENDENCY
> **Run `/ccf-raw-research {client_name}` FIRST.** This command expects `research/raw-deep/{blueprint_id}_raw_deep_research.md` to exist.
> If the RAW dossier is missing, the command falls back to V3.0 (original Firecrawl-based research loop).
> Each finding in the RAW dossier carries: `mode` (T/V/R), `depth_level` (L1/L2/L3), `storytelling_tag`, `visual_potential`, `tribe_invisible`.

**CRITICAL:** This environment requires EXPLICIT CLI execution. You must run `python tools/firecrawl_wrapper.py ...` for all research.

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify setup + BROWSER ACCESS", status: "pending" },
    { id: "step-2", description: "STEP 2: LOAD SKILLS - Strategy Director + Critic + Protocol", status: "pending" },
    { id: "step-3", description: "STEP 3: STRATEGY PHASES - Execute V3 Loop for ALL Themes", status: "pending" },
    { id: "step-4", description: "STEP 4: VALIDATION - Enforce 1,600 word minimum", status: "pending" },
    { id: "step-5", description: "STEP 5: H6/H7 DISTILLATION GATE - Run research-distiller", status: "pending" },
    { id: "step-6", description: "STEP 6: CHECKPOINT - Update config.yaml", status: "pending" }
  ]
});
```

**DO NOT PROCEED until you have called `write_todos` above.**

---

## 📋 Step Execution Protocol (MANDATORY)

> [!CAUTION]
> **You MUST call `write_todos` at EVERY step transition.**

**For EACH step:** START → `in_progress` → Execute → Verify → `completed`

---

## STEP 1: PRE-FLIGHT & FIRECRAWL CHECK

**EXECUTE:** `write_todos` with STEP 1 as `in_progress`

### 1A. Verify Prerequisites
1.  **Project Context:** Ensure `strategy_brief.json`, `soul_values.md`, `tribe_profile.md` exist.
2.  **Firecrawl Tool:** Verify `tools/firecrawl_wrapper.py` exists.

### 1B. FIRECRAWL CONNECTIVITY TEST

> [!CAUTION]
> ## 🚨 MANDATORY CLI TEST
> **DO NOT proceed without a working Firecrawl CLI.**

**Test your tool access NOW:**

```bash
python tools/firecrawl_wrapper.py search "test connection" --limit 1 --no-scrape
```

**IF SUCCESS:** JSON output received. Continue.
**IF FAILURE:** STOP. "ERROR: Firecrawl CLI failed."

**EXECUTE:** `write_todos` with STEP 1 as `completed`

---

## STEP 2: LOAD V3 SKILLS

**EXECUTE:** `write_todos` with STEP 2 as `in_progress`

**Load the Persona Skills:**
1.  `skills/ccf/research/strategy-director/SKILL.md` (The Planner)
2.  `skills/ccf/research/critic/SKILL.md` (The Judge)
3.  `skills/ccf/research/deep-analysts/_DEEP_RESEARCH_PROTOCOL.md` (The Rules)

**EXECUTE:** `write_todos` with STEP 2 as `completed`

---

## STEP 3: THE V3 EXECUTION LOOP (Per Theme)

**EXECUTE:** `write_todos` with STEP 3 as `in_progress`

**For Each Theme in `tasks.json`:**

### Phase A: Strategy Direction (The Plan)
- **Persona:** Strategy Director
- **Action:** Analyze Theme vs Blueprint.
- **Output:** Generate `[Theme]_Research_Plan.json` (7 vectors).

### Phase B: Firecrawl Execution (The Hunt)
- **Persona:** Deep Analyst (Worker)
- **Action:**
  - **For each vector:**
    ```bash
    # 1. Wide Search
    python tools/firecrawl_wrapper.py search "QUERY" --limit 5
    
    # 2. Deep Dive (Choice of best URL)
    python tools/firecrawl_wrapper.py scrape "URL"
    ```
  - **Constraint:** READ the markdown JSON output.

### Phase C: The Critic's Gate (The Reflection)
- **Persona:** The Critic
- **Action:** Review findings.
- **Loop:** If "Generic", REPEAT Phase B with refined query.

### Phase D: Synthesis
- **Persona:** Deep Analyst (Synthesizer)
- **Action:** Write `[Theme]_Deep_Research.md` (Min 1,600 words).

**EXECUTE:** `write_todos` with STEP 3 as `completed` after ALL themes.

---

## STEP 4: VALIDATON

**EXECUTE:** `write_todos` with STEP 4 as `in_progress`

**Check each generated dossier:**
1.  **Word Count:** > 1,600 words?
2.  **Links:** Are all links valid 200 OK?
3.  **Forbidden Terms:** No `[Insert Link]`, `Wikipedia`.

**Refuse to finish if gates fail.**

**EXECUTE:** `write_todos` with STEP 4 as `completed`

---


---

## STEP 5: H6/H7 DISTILLATION GATE

**EXECUTE:** `write_todos` with STEP 5 as `in_progress`

> [!CAUTION]
> **MANDATORY GATE — Pipeline blocks if this fails.**

1. Read FULL: `ccf-26/skills/ccf/distillation/research-distiller/SKILL.md`
2. Execute 4-Phase Audit on BOTH `fresh_research.md` AND `deep_research_dossier.md`:
   - Law 1: Depth & Novelty Audit (L2/L3 in Deep, >50% New in Fresh)
   - Law 2: Mode Classification Audit (T/V/R mapping)
   - Law 3: Provenance Gate Audit (Verified URLs)
   - Law 4: Structural Integrity Audit (7 Angles + Temporal bounds)
3. **CREATE FILE:** `research/H6_H7_DISTILLATION_RECEIPT.md`

**IF FAIL:** Return to STEP 3 — re-execute either fresh or deep analysis targeted by the receipt's remediation directive.
**IF PASS:** Continue to STEP 6.

**EXECUTE:** `write_todos` with STEP 5 as `completed`


## STEP 6: CHECKPOINT

**EXECUTE:** `write_todos` with STEP 6 as `in_progress`

**Output:**
```
✅ DEEP RESEARCH COMPLETE (V3 Agentic Loop)
- Themes processed: {N}
- Firecrawl Reads: {count}
- Critic Rejections: {count}
- Validation: PASS
```

**EXECUTE:** `write_todos` with STEP 6 as `completed`
