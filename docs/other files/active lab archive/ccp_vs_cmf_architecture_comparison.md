# CCP vs CMF: Architecture Comparison & Upgrade Verdict

**Date**: 2026-03-21  
**Sources**: CCP PRD v1.0 (1,438 lines), CCF Bible Critique v2, JIT Skill Compiler Architecture, CRAL Documentation v1, Script Generation Skill Type Guide v1.0, CMF Pipeline Documentation v2.0, Unified Architecture Bible v2.1

---

## The Core Question

> Should the CMF be architecturally upgraded to match the CCP's level of sophistication, or is that overkill?

**Verdict: Selective adoption of 4 CCP patterns — not a wholesale port.**

The CMF and CCP solve fundamentally different problems. Blindly copying CCP's architecture into CMF would be like putting a fighter jet's avionics into a Formula 1 car — impressive engineering, wrong context.

---

## System DNA Comparison

| Dimension | CCP | CMF |
|-----------|-----|-----|
| **Mission** | Scale intimate human coaching relationships | Produce cinema-grade video from raw transcripts |
| **Runtime Mode** | Continuous (24/7 CBCS conversations, weekly batch CCF) | Project-based (one transcript → one film) |
| **User-Facing** | Yes (clients interact via Telegram in real-time) | No (operator-driven pipeline) |
| **State Complexity** | Massive (per-client Context Premise, SPT stages, ICT positions, Change Talk vaults, Intimacy Indexes) | Moderate (per-project strategy brief, quote manifest, beat clusters) |
| **Data Persistence** | Neo4j graph + Supabase (cross-session, cross-week, cross-month) | File-based (project folder, ephemeral per-run) |
| **Agent Count** | 76 agents + 11 Pi Extensions + 4 Intuition Extensions | ~20 skill invocations across 66 skills |
| **Dependencies** | 45 immutable core deps (topologically sorted, 4-tier registry) | ~10 file deps (linear, sequential) |
| **Pipeline Shape** | Multi-loop (CRAL → JIT → Validation → Generation → Performance → Learning) | Linear waterfall (Diagnose → Hunt → Analyze → Compose → Authorize → Produce) |
| **Learning** | Yes (Fingerprint Archive → performance data → routing adjustments) | No (no feedback loop from final video quality back into pipeline) |
| **Per-Instance Isolation** | Single-tenant (dedicated Neo4j, Supabase, cloud per coach) | Single-project (folder-based isolation) |

---

## What CCP Has That CMF Doesn't (And Whether CMF Needs It)

### 1. JIT Skill Compilation (CCSB 3-Block Architecture)

**CCP**: Every SKILL.md is dynamically assembled at runtime through Block A (invariants/voice DNA), Block B (runtime injections from 16 adapters), and Block C (validation gates). Nothing is static — the system compiles intelligence contextually.

**CMF**: Skills are static `SKILL.md` files loaded whole. The arc routing selects *which* skill, but the skill itself isn't mutated at runtime.

> **Verdict: CMF DOESN'T need this.** CCP needs JIT because it must personalize output per-coach × per-client × per-mood-state × per-coping-position — a combinatorial explosion. CMF's combinatorics are low: 1 transcript × 1 arc × 1 brand avatar = consistent pipeline. Static skill routing by arc is sufficient.

---

### 2. Dependency Registry (45-DEP Topological Sort)

**CCP**: A 4-tier dependency registry where every data asset has a formal DEP ID, and the compiler enforces that upstream deps resolve before downstream execution. Ghost Variable Rule = hard compile error.

**CMF**: Implicit dependency chain — each command checks for the previous command's output file. No formal registry, no topological guarantee.

> **Verdict: CMF SHOULD adopt a lightweight version.** Not the 45-DEP formal registry, but CMF already has ~10 critical files that must exist before downstream steps run. Formalizing these into a **CMF Dependency Manifest** (a single YAML mapping `step → required_inputs → produced_outputs`) would catch errors earlier and enable the orchestrator to validate the full chain before execution. This is low-cost, high-value.

> [!TIP]
> A simple `cmf_dependency_manifest.yaml` could look like:
> ```yaml
> cmf-diagnose:
>   requires: [transcript]
>   produces: [strategy_brief.json]
> cmf-hunt:
>   requires: [strategy_brief.json, transcript]
>   produces: [Quote_Manifest.md]
> # ... etc
> ```
> The `/cmf-full` orchestrator validates the manifest before starting any step.

---

### 3. Receipt Chain Guard (Cryptographic Audit Trail)

**CCP**: Every pipeline stage produces a receipt. If any receipt is missing, the entire batch is quarantined. Full forensic reconstruction of any published content.

**CMF**: Authorization gates exist (14-point Commander, 15-point Visual Commander, VFS ≥90), but no unified chain. If GMG Analyst passes but CAC Analyst was skipped, there's no system-level catch.

> **Verdict: CMF SHOULD adopt this — simplified.** A **CMF Receipt Chain** that logs pass/fail per validation gate into a single `{project_id}_receipt_chain.json` would give operators forensic traceability. When a final video has a visual inconsistency, you can trace back to exactly which gate missed it. Implementation cost: ~2 hours (add a receipt entry at each existing gate).

---

### 4. Anti-Draft Intelligence (3-Level Contrastive Anchor)

**CCP**: Level 1 (archetype failure exemplar), Level 2 (psychological mode failure), Level 3 (coach-specific drift from Negative Space Object). Every generated script must maximize distance from these three anti-patterns.

**CMF**: No equivalent. The pipeline trusts the LLM to produce non-generic output based on the SPR priming and arc-specific skill instructions.

> **Verdict: CMF SHOULD adopt Level 1 only.** CMF doesn't have the per-coach voice DNA complexity that requires Level 2/3, but each of the 13 arcs *does* have predictable failure modes (e.g., "The Witness" arc tends to produce saccharine sentimentality, "The Confrontation" arc tends to lose nuance). Adding a brief `anti_draft_exemplar` section to each arc's Hunter and Composer skills — showing what generic AI output looks like for that arc — would meaningfully improve output quality. Low cost, medium impact.

---

### 5. Psychological Routing & Mood State Architecture

**CCP**: 4 mood states (Processing, Escape, Discovery, Status) × 3 audience maturity cohorts × Semantic Affinity Guard × Audience Maturity Lifecycle. Content is psychologically targeted per audience segment.

**CMF**: No psychological routing. The video targets whoever watches it.

> **Verdict: CMF DOESN'T need this.** CMF produces one video per transcript. There's no audience segmentation because there's no audience — the video is the coach's asset. The arc routing system already provides narrative-level emotional targeting.

---

### 6. CRAL Research Subsystem (9-Skill Cultural Research)

**CCP**: Before any content is compiled, 9 CRAL skills execute research across 7 "Diagonal" moments (M1-M7), each with quality gates and Human Evidence Bias enforcement.

**CMF**: E-Roll Research exists (Step 9) — but it's 1 skill vs. CCP's 9, and the research feeds B-roll visual ideas rather than narrative intelligence.

> **Verdict: CMF DOESN'T need CRAL.** CMF's narrative comes from the raw transcript — it's grounded in real human speech, not LLM-generated content. The E-Roll research serves a downstream visual function that is architecturally appropriate.

---

### 7. Guardian Agent (Pre-Production Intelligence Layer)

**CCP**: Sequential orchestrator executing 5 foundation stages (FR0A→FR0E) with AUTHENTICATED/PROVISIONAL/FAILED verdicts. Stewardship Mode monitors for drift weekly.

**CMF**: No equivalent. The Story Doctor diagnose step is the closest — it validates the transcript and selects the arc.

> **Verdict: CMF DOESN'T need this.** The Guardian Agent exists because CCP has a permanent coach identity that must be maintained across hundreds of production cycles. CMF projects are episodic — each starts fresh from a new transcript. There's nothing to steward.

---

### 8. Fingerprint Archive & Performance Feedback Loop

**CCP**: Every generated piece gets a Skill Fingerprint ID linking it to the exact compilation parameters. Performance data (saves, replays, DMs) traces back to specific upstream decisions. The system learns.

**CMF**: No performance tracking. No closed-loop learning.

> **Verdict: CMF WOULD BENEFIT from a simplified version — but it's Phase 2.** Tracking which arc + quote selection + storyboard composition → best-performing videos would make CMF self-improving. But this requires downstream video performance data that CMF currently has no way to ingest. Flag for future.

---

## The 4 Adoptable CCP Patterns (Ordered by Impact/Effort Ratio)

| # | Pattern | Estimated Effort | Expected Impact | Priority |
|---|---------|-----------------|-----------------|----------|
| 1 | **CMF Dependency Manifest** (from CCP's Dependency Registry) | 2-3 hours | High — catches broken chains before `/cmf-full` fails mid-run | **P0** |
| 2 | **CMF Receipt Chain** (from CCP's Receipt Chain Guard) | 2-4 hours | High — forensic traceability for all 7+ validation gates | **P1** |
| 3 | **Arc Anti-Draft Exemplars** (from CCP's 3-Level Anti-Draft) | 4-6 hours (13 arcs × ~30 min each) | Medium — measurably reduces generic AI output per arc | **P1** |
| 4 | **Project Fingerprint ID** (from CCP's Fingerprint Archive) | 1-2 hours | Low now, high later — enables future learning loop | **P2** |

**Total upgrade effort: ~10-15 hours** for all 4 patterns. Manageable. Not a rewrite.

---

## What Would Be Overkill

| CCP Pattern | Why It's Overkill for CMF |
|-------------|--------------------------|
| JIT Skill Compilation (CCSB) | CMF has no combinatorial personalization — static arc-routed skills are correct |
| 16 Transformation Adapters | Adapters solve per-audience × per-coach mutation — CMF has neither |
| Psychological Routing / Mood States | CMF produces assets, not audience-targeted content sequences |
| CBCS Relationship Intelligence (14 FRs) | CMF has no client-facing interaction at all |
| CPSC Sales Cycle (10 FRs) | CMF has no commercial conversion layer |
| Guardian Agent + Stewardship Mode | CMF projects are episodic, not persistent |
| 76-agent departmental governance | CMF's 66 skills operate in a clean waterfall — no cross-department coordination needed |
| Neo4j Graph Database per project | File-based project folders are architecturally appropriate for CMF's scope |
| Monthly Cross-Ecosystem Meeting | CMF doesn't run multiple persistent instances |

---

## Bottom Line

```
CMF is a production studio.  CCP is a living organism.

You don't give a studio a nervous system.
You give it better quality control on the assembly line.
```

The CMF's current architecture — 13-arc routing, 10 skill families, 13-step pipeline, multi-format output (storyboard, GMG, CAC, sonic) — is **already well-engineered for its purpose**. The pipeline shape (linear waterfall with validation gates) is correct for a project-based system.

The 4 patterns above would harden CMF without bloating it. Everything else in the CCP PRD exists to solve problems CMF doesn't have.

> [!IMPORTANT]
> **The previous MCDA/SWOT analysis** (which evaluated ACC, MATRL, Flow GRPO, and Visual Reasoning upgrades from the research papers) and **this CCP comparison** converge on the same conclusion: CMF benefits from targeted hardening, not architectural reimagining. The research papers propose agentic upgrades that would make CMF more like CCP — which is the wrong direction for a production pipeline.
