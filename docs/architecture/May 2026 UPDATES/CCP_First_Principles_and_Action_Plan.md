# CCP First Principles & Action Plan
*Synthesized from the 135-Question Architecture Audit + Emilio Commentary*
*Status: DRAFT — Awaiting 135 Commentaries to be finalized*

---

## HOW TO USE THIS DOCUMENT

This document is the **synthesis output** of the following three audits:

| Document | Questions | Status |
|---|---|---|
| `Architectural_Audit_60_Answers.md` | 60 | Pending Emilio Commentary |
| `Actual_Harness_60_Answers.md` | 60 | Pending Emilio Commentary |
| `CCP_JIT_Architecture_15_Answers.md` | 15 | Pending Emilio Commentary |

Once all 135 `[EMILIO COMMENTARY]` sections are written, this document will be completed to define:
1. The **First Principles** that govern every engineering decision going forward.
2. The **Keep / Kill / Migrate** decision for every component.
3. The **Clean Codebase Migration Plan** with only what is needed.
4. The **May 2026 Build Order** — what ships first, in what sequence.

---

## PART I — FIRST PRINCIPLES
*To be finalized after commentary review. These principles must survive every architectural decision.*

> [!IMPORTANT]
> A First Principle is not a preference or a strategy. It is a constraint that cannot be violated without breaking the system's integrity.

### P1 — The Harness Is the Product
The platform's value is not in the number of features, agents, or specs. It lives exclusively in the orchestration engine, the primitive registries, and the rendering pipelines. Every file that does not serve one of these three purposes is dead weight.

### P2 — Intelligence is Front-Loaded, Execution is Dumb
All complexity belongs at **compilation time**, not runtime. The execution agent must be a dumb loop reading a static instruction set (`SKILL.md`). If the execution agent is making decisions, the architecture is broken.

### P3 — LLM Calls Must Cross the Dichotomy Gate
No LLM output ever touches the deterministic pipeline without first passing a Pydantic schema validator. DSPy manages cognitive retries *inside* the LLM boundary. Pydantic enforces structural integrity *outside* it. These two layers must never be collapsed into one.

### P4 — The Receipt Chain Is the Source of Truth
Every state transition — success, failure, retry, skip — must produce a machine-readable receipt. No system state is valid unless it is in the receipt chain. Observability is not optional; it is structural.

### P5 — Coach DNA Is Immutable Once Locked
Once a coach's Voice DNA, Primitive Registry, and Archetype Templates reach "Stable" status, they are locked. Changes trigger a new compilation cycle, not an in-place overwrite. This prevents centroid drift across the pipeline.

### P6 — [TO BE ADDED AFTER COMMENTARY]
*Derived from Emilio's commentary on questions 1–60.*

### P7 — [TO BE ADDED AFTER COMMENTARY]
*Derived from Emilio's commentary on questions 61–120.*

### P8 — [TO BE ADDED AFTER COMMENTARY]
*Derived from Emilio's commentary on questions 121–135.*

---

## PART II — KEEP / KILL / MIGRATE REGISTRY
*To be completed after commentary review. Each row maps to an audit finding.*

> [!CAUTION]
> The migration to a clean codebase means every component must earn its place. Default is KILL unless proven essential.

### Tier 1 — KEEP AS-IS (Core Spine)
*Components confirmed built, working, and essential to the production pipeline.*

| Component | File(s) | Evidence |
|---|---|---|
| ValidationGate (Sophia/Marcus/Chen) | `validation_gate.py` | Implemented, 3-stage |
| ReceiptChain | `receipt_chain.py` | Append-only JSONL audit trail |
| Anti-Draft Calibrator | `anti_draft_calibrator.py` | Level 3 failure mode targeting |
| Saliency Analysis Service | `saliency_analysis_service.py` | Perceptual scoring |
| Pi Extension Harness | `pi_extension_harness.py` | 11 Extensions implemented |
| AdapterRegistry V2 | `adapter_registry_v2_models.py` | Pipeline isolation confirmed |
| FingerprintArchiveEngine | `fingerprint_archive_engine.py` | JIT cache checking confirmed |
| [TO BE EXPANDED] | | |

### Tier 2 — MIGRATE + CLEAN (Exists but Disorganized)
*Components that work but need to be refactored into the clean codebase.*

| Component | Current Location | Issue | Action |
|---|---|---|---|
| Neo4j Integration | 23 files, scattered | No single service layer | Consolidate into `graph_service.py` |
| Quarantine Models | `phase0_workspace_models.py`, `receipt_guard_models.py` | Models exist, retry loop missing | Build retry loop in migration |
| DSPy Structural Layer | `orchestration_dichotomy.py` | `dspy.Assert` cognitive layer missing | Implement cognitive retries |
| [TO BE EXPANDED] | | | |

### Tier 3 — KILL (Fabricated or Obsolete)
*Specs that were written but have zero codebase evidence. Do not migrate.*

| Feature | Status | Reason |
|---|---|---|
| SubliminalOrchestrator | FABRICATED | No implementation exists |
| DragonBonesJS | FABRICATED | No evidence anywhere |
| Remotion Server | FABRICATED | No remotion dependency |
| SAM3 Integration | FABRICATED | No SAM3 code |
| RLM Workspace (short-term memory) | UNBUILT | Planned, never coded |
| Social API Feedback Loop (SkillNet) | UNBUILT | No API hooks |
| Dead-Letter Queue (DLQ) | UNBUILT | No FailureReceipt object |
| Performance-Based Pattern Pruning | UNBUILT | Static lists only |
| Maturity Gating (Draft→Tested→Stable) | UNBUILT | No promotion lifecycle |
| ComfyUI Integration | UNBUILT | No VIE service code |
| [TO BE EXPANDED AFTER COMMENTARY] | | |

---

## PART III — CLEAN CODEBASE MIGRATION PLAN
*Structure of the new, minimal codebase. Only Tier 1 and Tier 2 components migrate.*

> [!NOTE]
> The goal is NOT a full rewrite. It is an extraction: pull the working spine out of 16,000 files and rebuild around it cleanly.

### Proposed New Structure

```
src/
├── ccp/
│   ├── core/                    # The Spine — immutable once stable
│   │   ├── receipt_chain.py     ✅ KEEP
│   │   ├── validation_gate.py   ✅ KEEP
│   │   └── graph_service.py     🔨 MIGRATE (consolidate Neo4j)
│   │
│   ├── harness/                 # Compilation Engine
│   │   ├── fingerprint_archive_engine.py  ✅ KEEP
│   │   ├── adapter_registry_v2.py         ✅ KEEP
│   │   ├── skill_compiler.py              🔨 BUILD — the JIT executor
│   │   └── subliminal_orchestrator.py     🔨 BUILD — the dumb loop runner
│   │
│   ├── models/                  # Pydantic Schemas — the Dichotomy Gate
│   │   ├── [all validated models from audit]
│   │   └── failure_receipt.py   🔨 BUILD — DLQ receipt model
│   │
│   ├── services/                # Business Logic
│   │   ├── anti_draft_calibrator.py   ✅ KEEP
│   │   ├── saliency_analysis.py       ✅ KEEP
│   │   ├── pi_extension_harness.py    ✅ KEEP
│   │   └── dspy_orchestrator.py       🔨 BUILD — cognitive retry layer
│   │
│   ├── pipelines/               # Pipeline-Specific Adapters
│   │   ├── ccf/
│   │   ├── cmf/
│   │   └── cbcs/
│   │
│   └── coaches/                 # Coach DNA Storage (per-coach)
│       └── {coach_acronym}/
│           ├── primitive_registry.json
│           └── logs/receipt_chain/
```

### Migration Phases

**Phase 0 — Extraction** *(Before May Updates)*
- [ ] Identify all Tier 1 files and copy to new clean repo
- [ ] Run all existing tests against the extracted files
- [ ] Confirm the core spine works in isolation

**Phase 1 — Core Build** *(May Updates — Week 1-2)*
- [ ] Build `FailureReceipt` model and DLQ logging
- [ ] Build `skill_compiler.py` — the JIT SKILL.md executor
- [ ] Build `subliminal_orchestrator.py` — the dumb loop runner
- [ ] Consolidate Neo4j into single `graph_service.py`

**Phase 2 — Intelligence Layer** *(May Updates — Week 3-4)*
- [ ] Implement `dspy_orchestrator.py` with `dspy.Assert` cognitive retries
- [ ] Implement Maturity Gating lifecycle (`Draft → Tested → Stable`)
- [ ] Implement short-term session memory (replace RLM with Redis or in-memory)

**Phase 3 — Go Live Gate**
- [ ] 100% receipt coverage on all state transitions
- [ ] ValidationGate passing on all pipeline outputs
- [ ] Fingerprint Archive caching all compiled SKILL.md files
- [ ] End-to-end test: one coach, one trigger, one rendered output

---

## PART IV — MAY 2026 BUILD ORDER
*To be finalized after commentary review. Ordered by dependency.*

> [!IMPORTANT]
> Build Order = Dependency Order. Nothing can be built before its dependencies are confirmed stable.

| # | Component to Build | Depends On | Owner | Target |
|---|---|---|---|---|
| 1 | `FailureReceipt` + DLQ | `receipt_chain.py` | — | Week 1 |
| 2 | `skill_compiler.py` (JIT executor) | `fingerprint_archive_engine.py`, `adapter_registry_v2.py` | — | Week 1 |
| 3 | `subliminal_orchestrator.py` (dumb loop) | `skill_compiler.py` | — | Week 2 |
| 4 | Neo4j `graph_service.py` (consolidation) | All models | — | Week 2 |
| 5 | `dspy_orchestrator.py` (cognitive retries) | DSPy + Pydantic gate | — | Week 3 |
| 6 | Maturity Gating lifecycle | Archetype templates | — | Week 3 |
| 7 | Session memory (Redis/in-memory) | `subliminal_orchestrator.py` | — | Week 4 |
| 8 | End-to-end pipeline test (1 coach) | All above | — | Week 4 |

---

## PART V — GO LIVE CHECKLIST
*Every item must be checked before go-live is declared.*

### Architecture
- [ ] Single source of truth: every state is in the ReceiptChain
- [ ] Every LLM output crosses the Pydantic Dichotomy Gate
- [ ] Every validation failure generates a FailureReceipt (no silent crashes)
- [ ] SKILL.md compilation is JIT with Fingerprint Archive caching
- [ ] All pipelines (CCF, CMF, CBCS) use isolated Adapter Registries

### Codebase
- [ ] No files outside the agreed folder structure
- [ ] No dead code (Tier 3 components fully removed)
- [ ] Every Tier 1 component has at least one passing test
- [ ] Neo4j connection consolidated to single service layer

### Coach Readiness (per coach)
- [ ] Voice DNA extracted and locked
- [ ] Primitive Registry populated and validated
- [ ] At least one Archetype Template at "Stable"
- [ ] First SKILL.md compiled and verified end-to-end

---

## REVISION HISTORY

| Date | Author | Change |
|---|---|---|
| 2026-05-28 | Antigravity | Initial skeleton created — awaiting 135 Emilio commentaries |
| — | Emilio | To be updated after commentary review |

