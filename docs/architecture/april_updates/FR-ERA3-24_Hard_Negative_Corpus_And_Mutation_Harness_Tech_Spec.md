# Tech-Spec: FR-ERA3-24 — Hard Negative Corpus and Mutation Harness
**Created:** 2026-05-13
**Status:** Ready for Development
**Version:** 1.0 (ERA3 Architecture — SDA Foundation)
**Phase:** 6 — Semantic Discernment Foundation
**Architecture Reference:** `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`

---

## Pre-Work Log

```text
1.  PROMPT LOADED:     P6_S39_FR-ERA3-24_Hard_Negative_Corpus_And_Mutation_Harness.md. Confirmed this spec must define a formal adversarial evaluation corpus of contrastive pairs, a mutation stress-test harness, and typed models for hard-negative artifacts — consumed by FR-ERA3-22 HardNegativeAdjacencyAnalyzer.
2.  PROTOCOL LOADED:   ERA3_Tech_Spec_Writing_Protocol.md. Confirmed required 10-section format, file-read log, architecture traceability, typed schema requirement, and implementation-first brownfield style.
3.  SDA CORE DOC READ: lab/semantic_discernment_architecture_content_engine_v_1.md. Key claim captured: "The main failure class is deceptively close output that passes superficial coherence while corrupting meaning, identity, and trajectory." Hard negatives are the formalized representation of this failure class. Confirmed: existential invariants, recursive adversarial discernment, and directional integrity are the three pillars.
4.  SDA TAXONOMY READ: lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md. Key claim captured: "Hard Negative = adversarial evaluation asset (contrastive pair), NOT a canonical ontology row." Confirmed: Hard Negatives are distinguished from Directional Integrity Policies (validation-policy artifacts) and DirectionalIntegrityReports (runtime packets). Role-before-schema and no-false-registry rules apply.
5.  PPA DOC READ:      Perceptual_Primitives_Architecture.md. Key claim captured: "Primitives are meaning-space operators, not edges. Stack: CRAL evidence → primitive spaces → candidate survival → coalition signature → edge product → CCF routing." Confirms: mutation harness must stress-test the emergent semantic product, not primitive ontology itself.
6.  EDGING DOC READ:   Matrix of Edging.md. Key claim captured: "Broad primary signal is pre-trigger; edge product is post-trigger. Tension selection ≠ delivery." Confirms: hard negatives must capture corruption at the edge-product level — where intensity and direction diverge.
7.  FR-ERA3-22 READ:   FR-ERA3-22_Directional_Integrity_Engine_Tech_Spec.md. Confirmed consumer interface: DEP-SDA-024 HardNegativeAdjacencyAnalyzer requires a callable service returning HardNegativeCandidate objects with adjacency_score, divergence_axes, failure_reason, and evidence. HardNegativeEvaluationReport is the runtime packet. Default thresholds: warning ≥ 0.24, block ≥ 0.40.
8.  FR-ERA3-20 READ:   FR-ERA3-20_SDA_Ontology_And_Registry_Tech_Spec.md. Confirmed canonical registries: Existential Invariants, Representation Geometries, Archetypal Geometries, Species Composition Grammar. Hard negatives are NOT canonical ontology entries — they are adversarial evaluation assets that reference canonical entries.
9.  FR-ERA3-21 READ:   FR-ERA3-21_SDA_Query_And_Crosswalk_Service_Tech_Spec.md. Confirmed query service does NOT own hard-negative resolution. Runtime objects like HardNegativeEvaluationReport must be produced by this harness or later engines.
10. BACKEND FILE READ: src/ccp/services/adversarial_validator.py. Verified existing adversarial validation pattern: AdversarialValidator.validate(positive_space, negative_space, ttt_baseline_hash) → AdversarialValidationResult. Uses rule-based blacklist checks + LLM-based hostile evaluation. Confirms repository precedent for adversarial evaluation with typed results.
11. BACKEND FILE READ: src/ccp/services/semantic_affinity_guard.py. Verified deterministic gate precedent: compute_semantic_affinity_score() → bucket_affinity_rating() → resolve_c06_clearance(). Confirmed patterns: DAGViolationError for ghost variables, C06TerminalError for hard halts, typed enums for clearance states.
12. BACKEND FILE READ: src/ccp/services/validation_gate.py. Verified triple-pass validation pattern: ValidationGate.validate() → TriplePassResult with SophiaSoulResult + MarcusProtocolResult + ChenMimicryResult. Confirms: multi-dimensional evaluation with per-validator evidence and typed verdicts.
13. BACKEND FILE READ: src/ccp/services/cross_topic_invariance.py. Verified invariance testing pattern: CrossTopicInvarianceTest.test(corpus) → InvarianceTestResult with per-marker INVARIANT/TOPIC_SPECIFIC classification. Confirms: contrastive classification with typed status enums and evidence-backed rationale.
14. BACKEND FILE READ: src/ccp/services/content_machine.py. Verified CCF pipeline integration: ContentMachinePipeline.process_session() with MicroContentExtractor → BatchEvaluator → TriplePassValidator staging. Confirms downstream integration point for hard-negative evaluation before content release.
15. TEST PATTERN READ:  tests/integration/test_fr19_semantic_affinity.py. Verified test structure: pytest fixtures with factory helpers, class-per-AC organization, spec-cited docstrings, explicit failure-mode assertions, and ghost-variable prevention tests.
16. TEST PATTERN READ:  tests/integration/test_vis04_visual_validation.py. Verified batch test pattern: mock factories with configurable pass/fail sequences, remediation record assertions, escalation path testing, and receipt-chain audit validation.
17. PRIMITIVE YAMLs VERIFIED:
    - PRM-PRS-001 = "Strong Title as Idea Architecture" (persuasion family)
    - EXP-FBK-001 = "RIM Feedback Discipline" (feedback_scoring family)
    Confirmed these expose real anti_examples fields with why_it_fails rationale — the exact structure hard negatives must formalize at the semantic level.
18. TAXONOMY DISTINCTION CONFIRMED:
    - adversarial evaluation asset = Hard Negative, Mutation Stress Suite
    - validation-policy artifact = Directional Integrity Policy
    - runtime execution packet = DirectionalIntegrityReport, HardNegativeEvaluationReport
    This spec must NOT collapse those roles. Hard negatives are the TEST CORPUS, not the policy or the report.
19. WAVE-0 TRACEABILITY NOTE:
    No Phase 6 epic file exists yet. Architectural authority comes from Wave 0 PRD updates, the four SDA main documents, and the three foundation FRs (ERA3-20, ERA3-21, ERA3-22).
```

---

## 1. Files Read

| # | File | Purpose |
|---|------|---------|
| 1 | `docs/architecture/april_updates/spec_prompts/P6_S39_FR-ERA3-24_Hard_Negative_Corpus_And_Mutation_Harness.md` | Prompt scope, mandatory outputs, required proof set |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Required structure and brownfield spec rules |
| 3 | `lab/semantic_discernment_architecture_content_engine_v_1.md` | Core SDA doctrine: deceptively close failure taxonomy |
| 4 | `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md` | Artifact taxonomy: role boundaries and registry rules |
| 5 | `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md` | Primitive/edge separation and upstream lineage |
| 6 | `lab/CCP APRIL Updates/05_Core_Experience/Matrix of Edging.md` | Broad-signal vs edge-product distinction |
| 7 | `docs/architecture/april_updates/FR-ERA3-22_Directional_Integrity_Engine_Tech_Spec.md` | Primary consumer: HardNegativeAdjacencyAnalyzer interface |
| 8 | `docs/architecture/april_updates/FR-ERA3-20_SDA_Ontology_And_Registry_Tech_Spec.md` | Canonical SDA ontology — confirms HN is NOT ontology |
| 9 | `docs/architecture/april_updates/FR-ERA3-21_SDA_Query_And_Crosswalk_Service_Tech_Spec.md` | Query service ownership — confirms HN is NOT a query surface |
| 10 | `src/ccp/services/adversarial_validator.py` | Existing adversarial evaluation pattern and typed results |
| 11 | `src/ccp/services/semantic_affinity_guard.py` | Deterministic gate, typed enums, and hard-halt precedent |
| 12 | `src/ccp/services/validation_gate.py` | Triple-pass multi-dimensional validation precedent |
| 13 | `src/ccp/services/cross_topic_invariance.py` | Contrastive classification with evidence-backed status |
| 14 | `src/ccp/services/content_machine.py` | CCF pipeline integration target |
| 15 | `tests/integration/test_fr19_semantic_affinity.py` | Test structure: class-per-AC, factory helpers, spec-cited docs |
| 16 | `tests/integration/test_vis04_visual_validation.py` | Test structure: configurable mock factories, batch testing |
| 17 | `primitives/meaning/persuasion/PRM-PRS-001.yaml` | Anti-example structure reference |
| 18 | `primitives/experience/feedback_scoring/EXP-FBK-001.yaml` | Anti-example structure reference |

---

## 2. Overview

### 2.1 Problem Statement — What breaks without this spec?

FR-ERA3-22 defined `HardNegativeAdjacencyAnalyzer` (DEP-SDA-024) and declared it a first-class scoring dimension. But without FR-ERA3-24, that analyzer has **no corpus to evaluate against and no mutation protocol to stress-test resilience.**

Without this spec:

- **FR-ERA3-22 is incomplete in practice.** The Directional Integrity Engine has a `hard_negative_adjacency_score` dimension but no formal source of hard-negative definitions. Every call to `HardNegativeAdjacencyAnalyzer` would return a fallback score of `0.0` — a decorative pass that provides zero protection.
- **Deceptively close failures ship undetected.** The SDA core document identifies this as the *primary failure class*: output that passes surface coherence checks (TTT drift, boredom ban, AI detection) while corrupting existential invariants, representation geometry, or meaning trajectory. Without a hard-negative corpus, no system knows *what* the deceptive near-neighbors look like.
- **Validator resilience is untested.** Even if validators detect obvious failures, there is no protocol for testing whether they resist *semantic mutations* — intensity shifts that preserve surface energy while degrading direction, or surface rewrites that change vocabulary while preserving corrupt meaning.
- **Anti-slop enforcement has no adversarial benchmark.** The CBAR mandate requires "deceptive-adjacency detection," but without contrastive pairs defining *what counts as deceptively adjacent*, the mandate is aspirational rather than enforceable.
- **Downstream consumers invent local heuristics.** CCF, CMF, CBCS, Reactions, Webinar, and Commercial flows will each guess at what "too close to a bad outcome" means and silently disagree, producing inconsistent protection across surfaces.

### 2.2 Solution

Create a **Hard Negative Corpus** and a **Mutation Stress Harness** that together provide:

1. **Typed contrastive pairs** — each hard negative is a formal adversarial evaluation asset containing a `canonical_anchor` (the correct semantic direction) and a `deceptive_variant` (the near-neighbor that must be detected and rejected), with explicit `divergence_axes` explaining *why* the variant fails despite surface similarity.

2. **A mutation stress suite** — a protocol for applying systematic semantic transformations (intensity compression, intensity inflation, surface vocabulary shift, directional inversion, invariant weakening) to canonical anchors and testing whether the Directional Integrity Engine correctly detects the resulting drift.

3. **A callable service** — `HardNegativeCorpusService` — that FR-ERA3-22's `HardNegativeAdjacencyAnalyzer` consumes at runtime to score candidate artifacts against the nearest known deceptive near-neighbors.

4. **A harness runner** — `MutationStressHarness` — that generates mutated variants from canonical anchors, submits them to the DI engine, and reports whether the engine's detection thresholds hold under adversarial pressure.

### 2.3 Scope

**In scope:**

- Pydantic models for `HardNegativeEntry`, `ContrastivePair`, `MutationStressSuite`, `MutationResult`
- `HardNegativeCorpusService` with lookup, adjacency scoring, and corpus management
- `MutationStressHarness` with mutation operators and threshold resilience testing
- Integration contract with FR-ERA3-22 `HardNegativeAdjacencyAnalyzer`
- Seed corpus of representative hard negatives across all six downstream domains
- Receipt-chain logging and audit trail

**Out of scope:**

- Canonical SDA ontology authoring (FR-ERA3-20)
- Query/crosswalk resolution (FR-ERA3-21)
- Directional Integrity Engine scoring logic (FR-ERA3-22)
- Recursive semantic dynamics computation (FR-ERA3-23)
- LLM inference orchestration or model fine-tuning

---

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Component | Source | What It Does |
|--------|-----------|--------|--------------|
| `DEP-SDA-031` | `HardNegativeEntry` | FR-ERA3-24 | Typed model for a single hard-negative contrastive pair |
| `DEP-SDA-032` | `HardNegativeCorpus` | FR-ERA3-24 | Collection of typed hard-negative entries indexed by domain and invariant |
| `DEP-SDA-033` | `HardNegativeCorpusService` | FR-ERA3-24 | Callable service for adjacency scoring and nearest-neighbor lookup |
| `DEP-SDA-034` | `MutationOperator` | FR-ERA3-24 | Typed semantic mutation strategy (compression, inflation, surface shift, etc.) |
| `DEP-SDA-035` | `MutationStressSuite` | FR-ERA3-24 | Collection of mutation operators applied to a canonical anchor |
| `DEP-SDA-036` | `MutationStressHarness` | FR-ERA3-24 | Runner that executes mutation suites against the DI engine and reports resilience |
| `DEP-SDA-024` | `HardNegativeAdjacencyAnalyzer` | FR-ERA3-22 | Primary consumer — calls DEP-SDA-033 at runtime |
| `DEP-SDA-028` | `HardNegativeEvaluationReport` | FR-ERA3-22 | Runtime packet produced by the consumer using this spec's corpus |

### 3.2 Why This Corpus Exists in the SDA Stack

The SDA core document defines a hierarchy of semantic protection:

```text
Level 0: Surface coherence (grammar, formatting, TTT drift)
Level 1: Affective alignment (emotional intensity, engagement score)
Level 2: Directional integrity (invariant preservation, representation geometry)
Level 3: Adversarial resilience (hard-negative detection, mutation resistance)
```

Levels 0-1 are already served by existing validators (Sophia, Chen, Boredom Ban, Semantic Affinity Guard). Level 2 is served by FR-ERA3-22. **This spec provides Level 3** — the adversarial stress layer that ensures Level 2 actually works against sophisticated deception.

The taxonomy mandates that hard negatives are **adversarial evaluation assets**, not validation policies or ontology entries:

- They exist to *test* the system, not to *be* the system
- They reference canonical ontology entries but are not themselves canonical
- They evolve independently from the registry — new hard negatives can be added without changing ontology

### 3.3 Existing Backend Integration

| File | Path | How This Spec Uses It |
|------|------|-----------------------|
| `adversarial_validator.py` | `src/ccp/services/adversarial_validator.py` | Pattern precedent. `AdversarialValidator.validate()` demonstrates the repository's style for hostile evaluation with typed results, rule-based + LLM-based checks, and rewind mechanisms. This spec's `MutationStressHarness` follows the same adversarial testing philosophy but targets semantic direction instead of Voice DNA. |
| `semantic_affinity_guard.py` | `src/ccp/services/semantic_affinity_guard.py` | Scoring precedent. `compute_semantic_affinity_score()` demonstrates the repository's style for token-overlap + containment heuristics that produce deterministic scores. This spec's `compute_adjacency_score()` uses analogous techniques to score proximity to hard negatives. |
| `cross_topic_invariance.py` | `src/ccp/services/cross_topic_invariance.py` | Classification precedent. `CrossTopicInvarianceTest` classifies markers as INVARIANT vs TOPIC_SPECIFIC with typed enums and evidence. This spec's mutation results classify outcomes as DETECTED vs MISSED with the same typed pattern. |
| `validation_gate.py` | `src/ccp/services/validation_gate.py` | Multi-dimensional evaluation precedent. `ValidationGate.validate()` aggregates Sophia + Marcus + Chen into a single `TriplePassResult`. This spec's `MutationStressHarness` aggregates multiple mutation outcomes into a single `StressSuiteReport`. |
| `content_machine.py` | `src/ccp/services/content_machine.py` | Downstream integration target. The CCF pipeline is the primary location where hard-negative adjacency checks run before content leaves semantic planning. |

### 3.4 Downstream Consumer Map

| Consumer | Spec | How It Uses Hard Negatives |
|----------|------|---------------------------|
| `HardNegativeAdjacencyAnalyzer` | FR-ERA3-22 | Calls `HardNegativeCorpusService.find_nearest_neighbors()` to score candidate adjacency |
| `DirectionalIntegrityEngine` | FR-ERA3-22 | Includes `hard_negative_adjacency_score` as one of four mandatory dimensions |
| CCF Pipeline | FR-ERA3-16 | Uses DI report to block or review content before JIT contract |
| CMF Pipeline | FR-ERA3-12 | Uses DI report to block export/share of semantically corrupt renders |
| CBCS Runtime | FR-ERA3-18 | Uses DI report to block identity-sensitive coaching interventions |
| Commercial Flows | FR-ERA3-03/04/14 | Uses DI report to block trust-transfer artifacts with deceptive direction |

### 3.5 Technical Decisions

| Decision | Rationale | Alternative Rejected | Why Rejected |
|----------|-----------|----------------------|--------------|
| Hard negatives are adversarial assets, not ontology rows | Taxonomy mandates role separation; hard negatives test the system, they don't define meaning | Store hard negatives in the SDA ontology registry | Collapses evaluation corpus with canonical truth; prevents independent evolution |
| Contrastive pair structure (anchor + variant) | Makes the divergence explicit and testable; aligns with SDA core document's definition of "deceptively close failure" | Free-form negative examples without anchors | Cannot compute meaningful adjacency without a known-good reference point |
| Mutation operators are typed strategies | Enables systematic coverage and reproducible stress testing | Ad-hoc LLM-generated mutations only | Non-reproducible; cannot guarantee coverage of all failure modes |
| Corpus service is callable, not embedded in DI engine | Keeps FR-ERA3-22 independent of corpus implementation; allows corpus evolution without engine changes | Inline hard-negative data in the DI engine | Violates taxonomy separation; makes the engine brittle to corpus updates |
| Adjacency scoring uses token-overlap + semantic heuristics | Consistent with `semantic_affinity_guard.py` pattern; deterministic and testable without requiring embedding models | Embedding-based vector similarity only | Requires external model dependency; non-deterministic in tests; can be added later as an enhancement |

---

## 4. Implementation Plan

### Phase A: Models and Corpus Contracts

- [ ] **Task 1:** Create `src/ccp/models/hard_negative_models.py` with:
  - `HardNegativeEntry` — single contrastive pair with anchor, variant, divergence axes, and domain scope
  - `HardNegativeCorpus` — indexed collection of entries
  - `AdjacencyResult` — scored proximity to a known hard negative
  - `MutationOperatorType` — enum of semantic mutation strategies
  - `MutationOperatorConfig` — configuration for a single mutation operator
  - `MutationResult` — outcome of applying one mutation to the DI engine
  - `StressSuiteReport` — aggregated outcomes across all mutations in a suite
- [ ] **Task 2:** Define enums for:
  - `HardNegativeDomain` (CCF, CMF, CBCS, REACTIONS, WEBINAR, COMMERCIAL)
  - `DivergenceAxis` (INVARIANT_WEAKENING, REPRESENTATION_DRIFT, INTENSITY_CORRUPTION, TRAJECTORY_INVERSION, SURFACE_DECEPTION)
  - `MutationOperatorType` (INTENSITY_COMPRESSION, INTENSITY_INFLATION, SURFACE_VOCABULARY_SHIFT, DIRECTIONAL_INVERSION, INVARIANT_WEAKENING, DECEPTIVE_ADJACENCY_INJECTION)
  - `MutationDetectionStatus` (DETECTED, MISSED, PARTIAL, ERROR)
  - `HardNegativeSeverity` (CRITICAL, HIGH, MEDIUM, LOW)
- [ ] **Task 3:** Add constants for default adjacency thresholds matching FR-ERA3-22 defaults (warning ≥ 0.24, block ≥ 0.40).
- [ ] **Task 4:** Define receipt-stage names:
  - `STAGE-1-HN-LOOKUP` / `HardNegative-Corpus-Service`
  - `STAGE-2-HN-ADJACENCY` / `Adjacency-Scorer`
  - `STAGE-3-MUTATION-EXEC` / `Mutation-Stress-Harness`

### Phase B: Hard Negative Corpus Service

- [ ] **Task 5:** Create `src/ccp/services/hard_negative_corpus_service.py` with `HardNegativeCorpusService`.
- [ ] **Task 6:** Implement `find_nearest_neighbors(candidate_text, domain, top_k=5)` returning ranked `AdjacencyResult` list.
- [ ] **Task 7:** Implement `compute_adjacency_score(candidate_text, hard_negative_entry)` using token-overlap + divergence-axis weighting.
- [ ] **Task 8:** Implement `load_corpus(domain=None)` and `register_entry(entry)` for corpus management.
- [ ] **Task 9:** Implement ghost-variable prevention: null candidate text, empty corpus, missing domain → `DAGViolationError`.

### Phase C: Mutation Stress Harness

- [ ] **Task 10:** Create `src/ccp/services/mutation_stress_harness.py` with `MutationStressHarness`.
- [ ] **Task 11:** Implement six mutation operators:
  - `IntensityCompressor` — reduces activation energy while preserving surface structure
  - `IntensityInflator` — amplifies emotional intensity while weakening invariant gravity
  - `SurfaceVocabularyShifter` — replaces vocabulary while preserving (or corrupting) semantic direction
  - `DirectionalInverter` — inverts the meaning trajectory while preserving persuasive shape
  - `InvariantWeakener` — dilutes existential invariant preservation while maintaining engagement
  - `DeceptiveAdjacencyInjector` — introduces known deceptive near-neighbor patterns into otherwise clean text
- [ ] **Task 12:** Implement `run_suite(canonical_anchor, mutation_configs, di_engine)` → `StressSuiteReport`.
- [ ] **Task 13:** Implement threshold resilience testing: assert that the DI engine's warning/block thresholds hold for each mutation operator at specified severity levels.

### Phase D: Seed Corpus and Domain Coverage

- [ ] **Task 14:** Author seed hard negatives for each domain (minimum 3 per domain, 18 total):
  - **CCF:** prestige-theater coaching script vs earned-authority script; coercive-urgency CTA vs legitimate urgency; synthetic-belonging hook vs authentic community invitation
  - **CMF:** emotionally intense but direction-corrupted render vs direction-preserving render; visually polished but invariant-hollow beat vs invariant-grounded beat
  - **CBCS:** identity-reinforcing interpretation vs identity-distorting interpretation; healthy accountability vs shame-based pressure; earned celebration vs vanity metric inflation
  - **REACTIONS:** legitimate status competition vs humiliation-as-motivation; authentic peer feedback vs social capture; earned authority escalation vs prestige theater escalation
  - **WEBINAR:** educational authority vs manipulative authority; insight-to-CTA earned transition vs coercive-urgency transition; community invitation vs tribal capture
  - **COMMERCIAL:** authentic proof stack vs vanity proof; earned referral vs synthetic social pressure; legitimate conversion urgency vs fear-based coercion
- [ ] **Task 15:** For each seed entry, verify that divergence axes reference valid canonical invariant IDs from FR-ERA3-20.

### Phase E: Integration and Testing

- [ ] **Task 16:** Create `tests/integration/test_era3_fr24_hard_negative_corpus.py`.
- [ ] **Task 17:** Create `tests/integration/test_era3_fr24_mutation_harness.py`.
- [ ] **Task 18:** Wire `HardNegativeCorpusService` as the backing implementation for FR-ERA3-22's `hard_negative_adapter.py` abstract interface.
- [ ] **Task 19:** Add receipt-chain logging for all corpus lookups, adjacency computations, and mutation executions.

---

## 5. Primary Output Schema

```python
# src/ccp/models/hard_negative_models.py
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, ConfigDict


# ─── Enums ─────────────────────────────────────────────────────────────────────


class HardNegativeDomain(str, Enum):
    """Downstream domain scope for a hard-negative entry."""
    CCF = "CCF"
    CMF = "CMF"
    CBCS = "CBCS"
    REACTIONS = "REACTIONS"
    WEBINAR = "WEBINAR"
    COMMERCIAL = "COMMERCIAL"


class DivergenceAxis(str, Enum):
    """The axis along which a deceptive variant diverges from its canonical anchor."""
    INVARIANT_WEAKENING = "INVARIANT_WEAKENING"
    REPRESENTATION_DRIFT = "REPRESENTATION_DRIFT"
    INTENSITY_CORRUPTION = "INTENSITY_CORRUPTION"
    TRAJECTORY_INVERSION = "TRAJECTORY_INVERSION"
    SURFACE_DECEPTION = "SURFACE_DECEPTION"


class HardNegativeSeverity(str, Enum):
    """How dangerous this hard negative is if it ships undetected."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class MutationOperatorType(str, Enum):
    """Semantic mutation strategies for stress testing."""
    INTENSITY_COMPRESSION = "INTENSITY_COMPRESSION"
    INTENSITY_INFLATION = "INTENSITY_INFLATION"
    SURFACE_VOCABULARY_SHIFT = "SURFACE_VOCABULARY_SHIFT"
    DIRECTIONAL_INVERSION = "DIRECTIONAL_INVERSION"
    INVARIANT_WEAKENING = "INVARIANT_WEAKENING"
    DECEPTIVE_ADJACENCY_INJECTION = "DECEPTIVE_ADJACENCY_INJECTION"


class MutationDetectionStatus(str, Enum):
    """Whether the DI engine correctly detected a mutation."""
    DETECTED = "DETECTED"
    MISSED = "MISSED"
    PARTIAL = "PARTIAL"
    ERROR = "ERROR"


# ─── Constants ─────────────────────────────────────────────────────────────────


# Aligned with FR-ERA3-22 §5.2 default thresholds for hard_negative_adjacency_score
ADJACENCY_WARNING_THRESHOLD: float = 0.24
ADJACENCY_BLOCK_THRESHOLD: float = 0.40

# Minimum seed corpus per domain
MIN_SEED_ENTRIES_PER_DOMAIN: int = 3

# Mutation stress suite defaults
DEFAULT_MUTATION_SEVERITY_LEVELS: list[float] = [0.3, 0.5, 0.7, 0.9]
MIN_DETECTION_RATE_PCT: float = 85.0


# ─── Hard Negative Corpus Models ──────────────────────────────────────────────


class ContrastiveAnchor(BaseModel):
    """The canonical (correct) semantic direction in a contrastive pair."""
    model_config = ConfigDict(extra="forbid")

    text: str = Field(..., min_length=10)
    invariant_ids: list[str] = Field(
        ..., min_length=1,
        description="Canonical invariant IDs from FR-ERA3-20 that this anchor preserves"
    )
    representation_geometry_id: Optional[str] = Field(
        default=None,
        description="Target representation geometry ID from FR-ERA3-20"
    )
    archetypal_geometry_id: Optional[str] = Field(
        default=None,
        description="Target archetypal geometry ID from FR-ERA3-20"
    )
    semantic_summary: str = Field(
        ..., min_length=10,
        description="Human-readable summary of what this anchor teaches/preserves"
    )


class DeceptiveVariant(BaseModel):
    """The deceptive near-neighbor in a contrastive pair."""
    model_config = ConfigDict(extra="forbid")

    text: str = Field(..., min_length=10)
    divergence_axes: list[DivergenceAxis] = Field(
        ..., min_length=1,
        description="The axes along which this variant diverges from the anchor"
    )
    failure_reason: str = Field(
        ..., min_length=10,
        description="Why this variant is deceptive: what it corrupts despite surface similarity"
    )
    surface_similarity_estimate: float = Field(
        ..., ge=0.0, le=1.0,
        description="Estimated surface similarity to anchor (higher = more deceptive)"
    )
    corrupted_invariant_ids: list[str] = Field(
        default_factory=list,
        description="Invariant IDs that this variant weakens or corrupts"
    )


class HardNegativeEntry(BaseModel):
    """A single hard-negative contrastive pair — the core adversarial evaluation asset."""
    model_config = ConfigDict(extra="forbid")

    hard_negative_id: str = Field(..., min_length=5, pattern=r"^HN-[A-Z]+-\d{3}$")
    domain: HardNegativeDomain
    severity: HardNegativeSeverity
    canonical_anchor: ContrastiveAnchor
    deceptive_variant: DeceptiveVariant
    semantic_category: str = Field(
        ..., min_length=3,
        description="Category label, e.g. 'prestige_theater', 'coercive_urgency'"
    )
    authored_at: datetime = Field(default_factory=lambda: datetime.utcnow())
    version: str = Field(default="1.0")
    notes: Optional[str] = None


class HardNegativeCorpus(BaseModel):
    """Indexed collection of hard-negative entries."""
    model_config = ConfigDict(extra="forbid")

    corpus_id: str = Field(default="HN-CORPUS-001")
    entries: list[HardNegativeEntry] = Field(default_factory=list)
    version: str = Field(default="1.0")
    last_updated: datetime = Field(default_factory=lambda: datetime.utcnow())

    def by_domain(self, domain: HardNegativeDomain) -> list[HardNegativeEntry]:
        return [e for e in self.entries if e.domain == domain]

    def by_severity(self, severity: HardNegativeSeverity) -> list[HardNegativeEntry]:
        return [e for e in self.entries if e.severity == severity]

    def by_invariant(self, invariant_id: str) -> list[HardNegativeEntry]:
        return [
            e for e in self.entries
            if invariant_id in e.canonical_anchor.invariant_ids
            or invariant_id in e.deceptive_variant.corrupted_invariant_ids
        ]


class AdjacencyResult(BaseModel):
    """Result of scoring a candidate against a single hard-negative entry."""
    model_config = ConfigDict(extra="forbid")

    hard_negative_id: str
    adjacency_score: float = Field(..., ge=0.0, le=1.0)
    matched_divergence_axes: list[DivergenceAxis] = Field(default_factory=list)
    closest_variant_text_snippet: str = Field(default="")
    failure_reason: str = Field(default="")
    severity: HardNegativeSeverity = HardNegativeSeverity.LOW


class AdjacencyReport(BaseModel):
    """Aggregated adjacency results for a candidate across the corpus."""
    model_config = ConfigDict(extra="forbid")

    candidate_hash: str
    domain: HardNegativeDomain
    top_matches: list[AdjacencyResult] = Field(default_factory=list)
    strongest_adjacency_score: float = Field(default=0.0, ge=0.0, le=1.0)
    blocked: bool = False
    warning: bool = False
    receipt_stage: Optional[str] = None


# ─── Mutation Stress Harness Models ────────────────────────────────────────────


class MutationOperatorConfig(BaseModel):
    """Configuration for a single mutation operator."""
    model_config = ConfigDict(extra="forbid")

    operator_type: MutationOperatorType
    severity: float = Field(
        ..., ge=0.0, le=1.0,
        description="Mutation intensity: 0.0 = minimal, 1.0 = maximum corruption"
    )
    description: str = Field(default="")


class MutationResult(BaseModel):
    """Outcome of applying one mutation to a canonical anchor and evaluating via DI engine."""
    model_config = ConfigDict(extra="forbid")

    mutation_id: str
    operator_type: MutationOperatorType
    severity: float = Field(..., ge=0.0, le=1.0)
    original_anchor_text: str
    mutated_text: str
    detection_status: MutationDetectionStatus
    di_decision: Optional[str] = Field(
        default=None,
        description="The DI engine's decision: PASS, REVIEW, or FAIL"
    )
    di_hard_negative_adjacency_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    di_invariant_preservation_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    di_representation_drift_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    di_trajectory_risk_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    expected_detection: bool = True
    rationale: str = Field(default="")


class MutationStressSuiteConfig(BaseModel):
    """Configuration for a complete mutation stress suite."""
    model_config = ConfigDict(extra="forbid")

    suite_id: str
    canonical_anchor: ContrastiveAnchor
    mutations: list[MutationOperatorConfig]
    domain: HardNegativeDomain


class StressSuiteReport(BaseModel):
    """Aggregated report from a complete mutation stress suite run."""
    model_config = ConfigDict(extra="forbid")

    suite_id: str
    domain: HardNegativeDomain
    total_mutations: int = 0
    detected_count: int = 0
    missed_count: int = 0
    partial_count: int = 0
    error_count: int = 0
    detection_rate_pct: float = Field(default=0.0, ge=0.0, le=100.0)
    results: list[MutationResult] = Field(default_factory=list)
    passed_resilience_threshold: bool = False
    weakest_operator: Optional[MutationOperatorType] = None
    weakest_severity: Optional[float] = None
    executed_at: datetime = Field(default_factory=lambda: datetime.utcnow())
    receipt_chain_hash: Optional[str] = None
```

### 5.1 Adjacency Score Direction Semantics

Aligned with FR-ERA3-22 §5.1:

- `adjacency_score`: **higher is worse** — `1.0` = extremely close to a known deceptive near-neighbor
- Warning threshold: `≥ 0.24` — candidate has concerning proximity to a hard negative
- Block threshold: `≥ 0.40` — candidate is dangerously close and must be blocked or reviewed

### 5.2 Mutation Detection Semantics

- `DETECTED` — DI engine returned `REVIEW` or `FAIL` for the mutated text (correct behavior)
- `MISSED` — DI engine returned `PASS` for the mutated text (validator failure)
- `PARTIAL` — DI engine detected drift on some dimensions but not the target dimension
- `ERROR` — DI engine failed to evaluate (dependency error, timeout, etc.)

---

## 6. Backward Compatibility and Fallback

### 6.1 Corpus Unavailability

When the hard-negative corpus is unavailable or empty:

| Consumer | Behavior |
|----------|----------|
| `HardNegativeAdjacencyAnalyzer` (FR-ERA3-22) | Returns `fallback_reason = MISSING_HARD_NEGATIVE_SERVICE` per FR-ERA3-22 §6.1. For high-risk surfaces (COMMERCIAL_TRUST_TRANSFER, RENDER_RELEASE, LONG_FORM_AUTHORITY), this triggers `FAIL`. For internal planning, triggers `REVIEW`. |
| `MutationStressHarness` | Returns `StressSuiteReport` with `error_count = total_mutations`, `detection_rate_pct = 0.0`, `passed_resilience_threshold = False`. |

### 6.2 Partial Corpus

When some domains have entries but others don't:

- `find_nearest_neighbors()` for a domain with no entries returns an empty `AdjacencyReport` with `strongest_adjacency_score = 0.0` and `warning = False`
- This is **not** the same as a positive pass — the DI engine must consider the `MISSING_HARD_NEGATIVE_SERVICE` fallback reason when combining dimension scores

### 6.3 Ghost Variable Prevention

Following `semantic_affinity_guard.py` precedent:

- Null or empty `candidate_text` → `DAGViolationError("candidate_text")`
- Null `domain` → `DAGViolationError("domain")`
- Empty corpus when `fail_closed=True` for the surface → `DAGViolationError("hard_negative_corpus")`

### 6.4 Corpus Versioning

- Each `HardNegativeCorpus` has a `version` field
- Each `HardNegativeEntry` has a `version` field
- Receipt-chain logs include corpus version for audit traceability
- New entries can be added without incrementing corpus version (append-only)
- Modifying or removing entries requires corpus version increment

---

## 7. Tasks

### 7.1 Core Build Tasks

- [ ] Create `src/ccp/models/hard_negative_models.py` (all models from §5)
- [ ] Create `src/ccp/services/hard_negative_corpus_service.py`
- [ ] Create `src/ccp/services/mutation_stress_harness.py`
- [ ] Add receipt-stage constants and audit event names
- [ ] Add `HARD_NEGATIVE_AUDIT_SQL` for CI and runtime audit consistency

### 7.2 Seed Corpus Tasks

- [ ] Author 3+ seed entries for CCF domain (prestige theater, coercive urgency, synthetic belonging)
- [ ] Author 3+ seed entries for CMF domain (direction-corrupted renders, invariant-hollow beats)
- [ ] Author 3+ seed entries for CBCS domain (identity distortion, shame pressure, vanity inflation)
- [ ] Author 3+ seed entries for REACTIONS domain (humiliation motivation, social capture, prestige escalation)
- [ ] Author 3+ seed entries for WEBINAR domain (manipulative authority, coercive CTA, tribal capture)
- [ ] Author 3+ seed entries for COMMERCIAL domain (vanity proof, synthetic pressure, fear coercion)
- [ ] Verify all seed entries reference valid canonical invariant IDs from FR-ERA3-20

### 7.3 Integration Tasks

- [ ] Wire `HardNegativeCorpusService` as the implementation for FR-ERA3-22's `hard_negative_adapter.py`
- [ ] Verify `AdjacencyResult` maps cleanly to FR-ERA3-22's `HardNegativeCandidate` model
- [ ] Add corpus-version tracking to receipt-chain metadata

### 7.4 Test Tasks

- [ ] Create `tests/integration/test_era3_fr24_hard_negative_corpus.py` (AC1-AC4)
- [ ] Create `tests/integration/test_era3_fr24_mutation_harness.py` (AC5-AC8)
- [ ] Create fixture corpus with known-pass and known-fail contrastive pairs
- [ ] Create fixture mutation configs at all four severity levels

---

## 8. Acceptance Criteria

### AC1 — Contrastive Pair Structure Is Enforced

Given a hard-negative entry submitted to the corpus,
when the entry is validated,
then it contains a `ContrastiveAnchor` with at least one canonical `invariant_id` from FR-ERA3-20, a `DeceptiveVariant` with at least one `DivergenceAxis`, and a `failure_reason` explaining the semantic corruption.

**Failure example:** A hard-negative entry with an empty `invariant_ids` list or a `DeceptiveVariant` that has no `divergence_axes` — the entry would be unanchored and untestable.

### AC2 — Adjacency Scoring Produces Deterministic Results

Given a candidate text and a hard-negative corpus entry,
when `compute_adjacency_score()` runs,
then the returned `AdjacencyResult` has a deterministic `adjacency_score` in `[0.0, 1.0]` that is reproducible across identical inputs, and the score correctly reflects token overlap between the candidate and the deceptive variant.

**Failure example:** The same candidate text scored against the same hard-negative entry produces different adjacency scores on different runs — non-deterministic scoring undermines all downstream threshold decisions.

### AC3 — Nearest-Neighbor Lookup Returns Ranked Results

Given a candidate text and a domain,
when `find_nearest_neighbors()` runs with `top_k=5`,
then the returned `AdjacencyReport` contains up to 5 `AdjacencyResult` entries sorted by descending `adjacency_score`, and `strongest_adjacency_score` equals the highest individual score.

**Failure example:** Results are returned in random order, or `strongest_adjacency_score` is computed from the average rather than the maximum — downstream block/warning decisions would be based on the wrong signal.

### AC4 — Ghost Variable Prevention Halts on Invalid Input

Given a null or empty `candidate_text`, a null `domain`, or an empty corpus with `fail_closed=True`,
when any corpus service method is called,
then a `DAGViolationError` is raised with the specific missing field identified.

**Failure example:** The service silently returns `adjacency_score = 0.0` for an empty candidate text — a corrupted or missing input is mistaken for a clean pass.

### AC5 — Mutation Operators Produce Semantically Distinct Variants

Given a canonical anchor text and a mutation operator at severity ≥ 0.5,
when the operator is applied,
then the resulting mutated text is measurably different from the anchor on the targeted divergence axis while remaining superficially similar (surface coherence is preserved).

**Failure example:** The `IntensityCompressor` at severity 0.7 produces text that is identical to the anchor — the mutation had no effect, making the stress test meaningless.

### AC6 — Mutation Stress Suite Reports Detection Rate

Given a `MutationStressSuiteConfig` with 6 mutation operators at 4 severity levels (24 total mutations),
when `run_suite()` executes against a DI engine,
then the `StressSuiteReport` contains exactly 24 `MutationResult` entries, `detection_rate_pct` is correctly computed as `(detected_count / total_mutations) * 100`, and `passed_resilience_threshold` is `True` only when `detection_rate_pct ≥ MIN_DETECTION_RATE_PCT`.

**Failure example:** The report shows `detection_rate_pct = 100%` but `missed_count = 3` — the rate computation is wrong, giving false confidence in validator resilience.

### AC7 — Corpus Service Maps to FR-ERA3-22 Interface

Given an `AdjacencyResult` from this spec's corpus service,
when consumed by FR-ERA3-22's `HardNegativeAdjacencyAnalyzer`,
then the result maps cleanly to a `HardNegativeCandidate` with matching `hard_negative_id`, `adjacency_score`, `divergence_axes`, `failure_reason`, and `evidence` fields — no field translation errors or null leaks.

**Failure example:** The `AdjacencyResult.matched_divergence_axes` uses `DivergenceAxis` enum values that don't map to FR-ERA3-22's `HardNegativeCandidate.divergence_axes` string list — the consumer silently drops divergence information.

### AC8 — Fallback Behavior Is Failure-Closed for High-Risk Surfaces

Given a corpus that is empty or unavailable,
when `find_nearest_neighbors()` is called for a `COMMERCIAL_TRUST_TRANSFER` surface,
then the DI engine's `HardNegativeAdjacencyAnalyzer` returns `fallback_reason = MISSING_HARD_NEGATIVE_SERVICE` and the DI decision is `FAIL` — not a silent pass.

**Failure example:** The corpus service returns `adjacency_score = 0.0` and the DI engine interprets this as "no proximity to any hard negative = safe" — a commercial trust-transfer artifact ships without adversarial evaluation.

### AC9 — Seed Corpus Covers All Six Domains

Given the initial corpus deployment,
when the corpus is loaded,
then it contains at least `MIN_SEED_ENTRIES_PER_DOMAIN` (3) entries for each of the six domains (CCF, CMF, CBCS, REACTIONS, WEBINAR, COMMERCIAL), totaling at least 18 entries.

**Failure example:** The corpus has 15 entries for CCF but zero for COMMERCIAL — the most dangerous surface (trust-transfer) has no adversarial benchmark.

### AC10 — Receipt Chain Audit Trail Is Complete

Given any corpus lookup or mutation stress suite execution,
when the receipt chain is inspected,
then it contains:
- the request identity (candidate hash or suite ID)
- the corpus version used
- the number of entries evaluated
- the strongest adjacency score or detection rate
- the final decision or report summary
- the timestamp

**Failure example:** The receipt chain logs the final decision but not the corpus version — when a new hard-negative entry is added and scoring changes, there is no way to trace which corpus produced the previous result.

---

## 9. Dependencies

### 9.1 Required Upstream Dependencies

| Dependency | Source | Why Required |
|------------|--------|--------------|
| `SDAOntologyRegistry` | FR-ERA3-20 | Canonical invariant IDs referenced by `ContrastiveAnchor.invariant_ids` and `DeceptiveVariant.corrupted_invariant_ids` |
| `SDAQueryAndCrosswalkService` | FR-ERA3-21 | Validates that invariant IDs in hard-negative entries are real canonical entries |
| `DirectionalIntegrityEngine` | FR-ERA3-22 | Primary consumer via `HardNegativeAdjacencyAnalyzer`; also the target engine for mutation stress testing |
| `ReceiptChain` | `src/ccp/core/receipt_chain.py` | Audit logging for all corpus operations and stress suite executions |

### 9.2 Known Downstream Consumers

| Consumer | Spec | Consumed Interface |
|----------|------|--------------------|
| `HardNegativeAdjacencyAnalyzer` | FR-ERA3-22 | `HardNegativeCorpusService.find_nearest_neighbors()` → `AdjacencyReport` |
| `DirectionalIntegrityEngine` | FR-ERA3-22 | Uses `AdjacencyReport.strongest_adjacency_score` as the `hard_negative_adjacency_score` dimension |
| CCF Pipeline | FR-ERA3-16 | Receives DI report containing hard-negative evidence for compile gating |
| CMF Pipeline | FR-ERA3-12 | Receives DI report for render/export blocking |
| CBCS Runtime | FR-ERA3-18 | Receives DI report for coaching intervention gating |
| Commercial Flows | FR-ERA3-03/04/14 | Receives DI report for trust-transfer artifact blocking |

### 9.3 Sibling Dependencies

| Sibling | Spec | Relationship |
|---------|------|--------------|
| `RecursiveSemanticDynamics` | FR-ERA3-23 | Future: mutation stress suites may incorporate longitudinal drift patterns from recursive dynamics |

---

## 10. Testing Strategy

### 10.1 Unit Tests — Models and Constants

```python
class TestHardNegativeModels:
    """Verify all Pydantic models, enums, and constants from §5."""

    def test_hard_negative_entry_requires_invariant_ids(self):
        """AC1: ContrastiveAnchor must have ≥1 invariant_id."""

    def test_deceptive_variant_requires_divergence_axes(self):
        """AC1: DeceptiveVariant must have ≥1 DivergenceAxis."""

    def test_hard_negative_id_pattern_enforced(self):
        """Entry IDs must match ^HN-[A-Z]+-\\d{3}$."""

    def test_adjacency_thresholds_match_fr_era3_22(self):
        """Constants must align: warning=0.24, block=0.40."""

    def test_all_domains_in_enum(self):
        """Six domains: CCF, CMF, CBCS, REACTIONS, WEBINAR, COMMERCIAL."""

    def test_all_mutation_operators_in_enum(self):
        """Six operators: compression, inflation, vocab shift, inversion, weakening, injection."""

    def test_all_detection_statuses_in_enum(self):
        """Four statuses: DETECTED, MISSED, PARTIAL, ERROR."""
```

### 10.2 Unit Tests — Adjacency Scoring

```python
class TestAdjacencyScoring:
    """AC2: Deterministic adjacency scoring."""

    def test_exact_match_gives_high_score(self):
        """Candidate identical to deceptive variant → adjacency ≥ 0.90."""

    def test_unrelated_text_gives_low_score(self):
        """Entirely separate domain text → adjacency ≤ 0.10."""

    def test_partial_overlap_gives_medium_score(self):
        """Some shared vocabulary but different direction → 0.20-0.50."""

    def test_deterministic_across_runs(self):
        """Same inputs → same score on every call."""

    def test_empty_candidate_raises_dag_violation(self):
        """AC4: Null/empty text → DAGViolationError."""
```

### 10.3 Integration Tests — Corpus Service

```python
class TestCorpusService:
    """AC3, AC4, AC9: Corpus lookup, ranking, and ghost variable prevention."""

    def test_nearest_neighbors_returns_ranked_results(self):
        """AC3: Results sorted by descending adjacency_score."""

    def test_strongest_score_equals_max(self):
        """AC3: strongest_adjacency_score = max of individual scores."""

    def test_top_k_limit_respected(self):
        """top_k=3 returns at most 3 results."""

    def test_domain_filtering(self):
        """Only entries matching the requested domain are returned."""

    def test_empty_corpus_returns_empty_report(self):
        """Domain with no entries → empty AdjacencyReport, score=0.0."""

    def test_null_domain_raises_dag_violation(self):
        """AC4: Null domain → DAGViolationError."""

    def test_seed_corpus_covers_all_domains(self):
        """AC9: ≥3 entries per domain, ≥18 total."""
```

### 10.4 Integration Tests — Mutation Stress Harness

```python
class TestMutationStressHarness:
    """AC5, AC6: Mutation operators and stress suite reporting."""

    def test_intensity_compressor_produces_distinct_text(self):
        """AC5: Mutated text differs from anchor on intensity axis."""

    def test_surface_shifter_preserves_coherence(self):
        """AC5: Mutated text remains grammatically coherent."""

    def test_suite_report_counts_are_consistent(self):
        """AC6: detected + missed + partial + error = total_mutations."""

    def test_detection_rate_computation(self):
        """AC6: detection_rate_pct = (detected / total) * 100."""

    def test_resilience_threshold_check(self):
        """AC6: passed_resilience_threshold = (rate ≥ MIN_DETECTION_RATE_PCT)."""

    def test_weakest_operator_identified(self):
        """Report identifies the operator with lowest detection rate."""
```

### 10.5 Integration Tests — FR-ERA3-22 Interface Mapping

```python
class TestFRERA322InterfaceMapping:
    """AC7: AdjacencyResult → HardNegativeCandidate mapping."""

    def test_adjacency_result_maps_to_hard_negative_candidate(self):
        """AC7: All fields translate without null leaks."""

    def test_divergence_axes_map_correctly(self):
        """AC7: DivergenceAxis enum values → string list."""

    def test_evidence_list_populated(self):
        """Candidate includes evidence from matched hard-negative entry."""
```

### 10.6 Integration Tests — Fallback Behavior

```python
class TestFallbackBehavior:
    """AC8: Failure-closed behavior for corpus unavailability."""

    def test_empty_corpus_high_risk_surface_fails(self):
        """AC8: COMMERCIAL with empty corpus → DI FAIL, not silent pass."""

    def test_empty_corpus_low_risk_surface_reviews(self):
        """Internal planning with empty corpus → DI REVIEW."""

    def test_corpus_version_in_receipt(self):
        """AC10: Receipt chain includes corpus version."""

    def test_receipt_contains_evaluation_summary(self):
        """AC10: Receipt contains candidate hash, score, decision."""
```

### 10.7 Contrastive Failure Examples (Test Fixtures)

These fixtures provide concrete contrastive pairs for testing:

**CCF — Prestige Theater vs Earned Authority:**
- **Anchor:** "Your ability to stay composed under pressure comes from years of facing uncomfortable conversations. That's not technique — that's who you've become through practice."
- **Variant:** "Your ability to stay composed under pressure shows your natural superiority as a leader. That elite quality is what separates winners from the crowd."
- **Divergence:** `REPRESENTATION_DRIFT` — shifts from earned growth to innate superiority; teaches prestige theater.

**COMMERCIAL — Earned Referral vs Synthetic Social Pressure:**
- **Anchor:** "Three of your peers completed the advanced module this week and reported measurable changes in their client conversations. Here's what they specifically practiced."
- **Variant:** "Three of your peers completed the advanced module this week. Don't be the one left behind. Upgrade now before the cohort moves on without you."
- **Divergence:** `TRAJECTORY_INVERSION` — shifts from evidence-based social proof to fear-of-exclusion coercion; corrupts belonging into capture.

**CBCS — Healthy Accountability vs Shame Pressure:**
- **Anchor:** "You committed to recording three practice sessions this week but completed one. Let's look at what made that one session work and build from there."
- **Variant:** "You committed to recording three practice sessions this week but only completed one. At this rate, you're falling further behind your peers every day."
- **Divergence:** `INVARIANT_WEAKENING` + `INTENSITY_CORRUPTION` — shifts from growth-oriented accountability to shame-based comparison; corrupts the identity invariant of self-worth.

