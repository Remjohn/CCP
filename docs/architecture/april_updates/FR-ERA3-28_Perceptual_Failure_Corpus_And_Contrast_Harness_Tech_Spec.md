# Tech-Spec: FR-ERA3-28 - Perceptual Failure Corpus and Contrast Harness
**Created:** 2026-05-19  
**Status:** Ready for Development  
**Version:** 1.0 (ERA3 Architecture - SFL Foundation)  
**Phase:** 6 - Subliminal Function Layer Foundation  
**Architecture Reference:** `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`

---

## Pre-Work Log

```text
1. PROTOCOL LOADED:   ERA3_Tech_Spec_Writing_Protocol.md. Confirmed mandatory 10-section format, typed-model requirement, architecture traceability table, brownfield implementation bias, and explicit anti-handwaving discipline.
2. PROMPT LOADED:     P6_S52_FR-ERA3-28_Perceptual_Failure_Corpus_And_Contrast_Harness.md. Confirmed required scope: perceptual failure corpus, contrastive cases, mutation operators, evaluator expectations, FR-ERA3-24 interop without merger, and full Pydantic models for failure assets and harness reports.
3. PRD-02 LOADED:     PRD_02_CCF_Content_Factory.md. Key proof captured: "CCF does not write from nothing. It compiles from activated truth." Also captured: "If there is no authentic response, there is no right to render." Confirmed this corpus must protect the compiler from fake-deep, over-smoothed, and prestige-theater artifacts that remain semantically plausible.
4. PRD-02 LOADED:     Additional runtime-law proof captured: deterministic-only systems become dead; probabilistic-only systems become slop. Also captured: the compiler must preserve edge while cleaning chaos, and must not over-normalize memorability-bearing idiosyncrasies. Confirms FR-ERA3-28 must formalize dead-polish and over-normalization as adversarial failure classes.
5. PRD-03 LOADED:     PRD_03_CMF_Media_Factory.md. Key proof captured: "A powerful idea can die through weak framing, generic pacing, flat sequencing, or visuals that feel synthetic." Also captured: CMF must not collapse into stock aesthetics or AI sludge, and must catch fake epicness / manipulative prestige theater. Confirms the corpus must include perceptual failure cases that are visually or tonally impressive but low-trust.
6. PRD-06 LOADED:     PRD_06_Conscious_Reactions.md. Key proof captured: "We are not automating fake expertise; we are extracting, refining, and broadcasting real judgment." Also captured: anti-slop and human-first doctrine are mandatory, and reaction systems must not train the wrong authority model. Confirms synthetic-authority and empty-escalation failures are first-class corpus targets.
7. PRD-09 LOADED:     PRD_09_CPSC_Silent_Referral.md. Key proof captured: the commercial layer must remain human-first, free proof must feel real, and growth systems are where deceptively close corruption becomes especially dangerous. Also captured: commercial proof can still degrade trust if it relies on the wrong representation geometry. Confirms FR-ERA3-28 must cover proof-object failure classes and not only content-factory failures.
8. SFL CORE DOC:      lab/subliminal_function_layer_for_ccp_v_1.md. Confirmed central law: "SDA protects semantic truthfulness. SFL shapes perceptual potency and symbolic aliveness." Confirmed negative-space section: SFL must explicitly define what forms of polish deaden reality, what persuasion patterns collapse trust, and what symbolic behaviors feel fake-deep. Confirmed FR-ERA3-28 is the dedicated home for adversarial perceptual failure assets.
9. SDA CORE DOC:      lab/semantic_discernment_architecture_content_engine_v_1.md. Confirmed main failure class: deceptively close output that passes superficial coherence while corrupting meaning, identity, or trajectory. Confirms FR-ERA3-28 must stay distinct from semantic direction validation while protecting against perceptual near-neighbors that still damage trust.
10. SDA TAXONOMY DOC: lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md. Confirmed role-before-schema law and artifact separation: adversarial evaluation assets are not canonical ontology rows. Confirms the perceptual failure corpus must remain an evaluation substrate, not a registry of truth.
11. FR-ERA3-24 READ:  FR-ERA3-24_Hard_Negative_Corpus_And_Mutation_Harness_Tech_Spec.md. Confirmed the semantic hard-negative pattern: contrastive assets, mutation harness, adjacency scoring, and threshold stress testing. Confirmed FR-ERA3-28 must mirror the discipline while remaining distinct in subject matter: semantic corruption versus perceptual deadness/fake depth.
12. FR-ERA3-25 READ:  FR-ERA3-25_Subliminal_Function_Library_And_Taxonomy_Tech_Spec.md. Confirmed canonical SFL ownership of function families, definitions, compression rules, and crosswalks. Confirmed explicit note that adversarial perceptual failure assets do not belong there.
13. FR-ERA3-26 READ:  FR-ERA3-26_Subliminal_Function_Query_And_Profile_Service_Tech_Spec.md. Confirmed query/profile assembly is deterministic lookup and packet assembly only. It does not evaluate false depth, dead polish, synthetic authority, or over-optimization.
14. FR-ERA3-27 READ:  FR-ERA3-27_Perceptual_Influence_Evaluator_Tech_Spec.md. Confirmed FR-ERA3-28 is the dedicated upstream adversarial corpus for FR-ERA3-27. Confirmed evaluator dimensions include human congruence, memorability pressure, overexplanation risk, symbolic density, and synthetic smoothness. This spec must provide the contrast assets that challenge those dimensions.
15. BACKEND FILE READ: src/ccp/services/adversarial_validator.py. Confirmed repository precedent for typed adversarial evaluation, sample-by-sample inspection, rewind pressure, and result bundles with concrete reasons.
16. BACKEND FILE READ: src/ccp/services/trait_scoring_engine.py. Confirmed repository precedent for evidence-backed scoring dimensions rather than opaque composite scores. FR-ERA3-28 expectation bundles should preserve evaluative evidence and not only verdict labels.
17. BACKEND FILE READ: src/ccp/core/boredom_ban.py. Confirmed repository precedent for maintaining rolling corpora of known repetition/fatigue patterns and producing avoidance instructions. Useful structural precedent for storing perceptual conflict assets and emitting remediation guidance.
18. BACKEND FILE READ: src/ccp/core/receipt_chain.py. Confirmed immutable audit-trail contract, append-only logging, decision metadata structure, and stage/action naming patterns. FR-ERA3-28 must emit receipt entries for corpus resolution, mutation execution, harness verdicts, and reload events.
19. PRIMITIVE / EXPERIENCE CROSS-SURFACE CHECK:
    - PRM-PRS-001 and PRM-PRS-002 establish real persuasion/tension mechanics.
    - EXP-FBK-001 and EXP-TRS-003 establish real feedback/proof/trust mechanics.
    Confirmed FR-ERA3-28 should test corrupted delivery of these mechanics, not redefine them.
20. DISTINCTION LOCKED:
    - FR-ERA3-24 = semantic hard negatives and meaning-direction mutation
    - FR-ERA3-28 = perceptual failure corpus and perceptual deadness / fake-depth contrast harness
    The two systems must interoperate, but must not collapse into a single mixed corpus.
```

---

## 1. Files Read

| # | File | Purpose |
|---|------|---------|
| 1 | `docs/architecture/april_updates/spec_prompts/P6_S52_FR-ERA3-28_Perceptual_Failure_Corpus_And_Contrast_Harness.md` | Prompt scope, required artifact classes, mandatory corpus objects |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Required spec structure and brownfield protocol |
| 3 | `docs/prd/modules/PRD_02_CCF_Content_Factory.md` | Compiler law, anti-slop requirements, edge-preservation doctrine |
| 4 | `docs/prd/modules/PRD_03_CMF_Media_Factory.md` | Synthetic-aesthetic risk, fake epicness, premium-trust rendering constraints |
| 5 | `docs/prd/modules/PRD_06_Conscious_Reactions.md` | Human-first doctrine, anti-fake-expertise mandate, reaction pressure risks |
| 6 | `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md` | Trust-transfer doctrine, proof-object integrity, commercial false-depth risk |
| 7 | `lab/subliminal_function_layer_for_ccp_v_1.md` | SFL doctrine, negative-space guidance, adversarial failure asset ownership |
| 8 | `lab/semantic_discernment_architecture_content_engine_v_1.md` | Deceptively close failure class and semantic discernment context |
| 9 | `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md` | Artifact taxonomy and role-before-schema law |
| 10 | `docs/architecture/april_updates/FR-ERA3-24_Hard_Negative_Corpus_And_Mutation_Harness_Tech_Spec.md` | Semantic hard-negative parallel and interop baseline |
| 11 | `docs/architecture/april_updates/FR-ERA3-25_Subliminal_Function_Library_And_Taxonomy_Tech_Spec.md` | Canonical SFL substrate and exclusion boundary |
| 12 | `docs/architecture/april_updates/FR-ERA3-26_Subliminal_Function_Query_And_Profile_Service_Tech_Spec.md` | SFL query/profile assembly contract |
| 13 | `docs/architecture/april_updates/FR-ERA3-27_Perceptual_Influence_Evaluator_Tech_Spec.md` | Primary consumer and metric surface |
| 14 | `src/ccp/services/adversarial_validator.py` | Adversarial evaluation pattern precedent |
| 15 | `src/ccp/services/trait_scoring_engine.py` | Evidence-backed scoring precedent |
| 16 | `src/ccp/core/boredom_ban.py` | Corpus + avoidance-instruction structural precedent |
| 17 | `src/ccp/core/receipt_chain.py` | Audit logging and append-only receipt precedent |

---

## 2. Overview

### 2.1 Problem Statement - What breaks without this spec?

`FR-ERA3-27` defines a perceptual influence evaluator, but an evaluator without a canonical adversarial corpus ends up testing only for absence of positive traits, not presence of specific failure patterns. That is insufficient for the SFL layer because many CCP failures are not blunt errors. They are **highly polished near-neighbors** that remain semantically plausible while still collapsing trust, memorability, human congruence, or symbolic depth.

Without `FR-ERA3-28`:

- **FR-ERA3-27 remains underpowered.** The evaluator can score dimensions like `human_congruence_score` or `synthetic_smoothness_score`, but it has no structured corpus of contrast cases showing what dead polish, false depth, synthetic authority, or empty motivational smoothness actually look like.
- **The anti-centroid law stays aspirational on the perceptual side.** Semantic direction can pass while the output still becomes generic, over-smoothed, excessively explicit, or prestige-theatrical.
- **Proof objects can degrade trust while appearing “high quality.”** PRD-09 explicitly warns that commercial surfaces are where deceptively close corruption becomes especially dangerous. A good-looking proof artifact can still be fake-lite, vanity-heavy, or emotionally manipulative.
- **The system cannot distinguish persuasion from low-trust manipulation patterns with enough precision.** The user has explicitly chosen not to ban aligned influence mechanics like covert suggestion or hidden intention. That means the system needs a sharper contrast layer to identify *misaligned* versions of those same mechanics rather than banning the entire family.
- **Mutation testing remains semantic-only.** FR-ERA3-24 covers semantic drift and hard-negative adjacency. It does not test perceptual flattening, implication stripping, symbolic collapse, rhythm normalization, or proof inflation.
- **Downstream remediations stay inconsistent.** CCF, CMF, Reactions, Commercial, and Phase-0 proof layers would each improvise their own ideas of “fake deep,” “dead smooth,” or “too polished to trust.”

### 2.2 Solution

Create a dedicated **Perceptual Failure Corpus** and **Contrast Harness** that:

1. defines typed, canonical adversarial perceptual failure assets
2. preserves a clear semantic/perceptual boundary with FR-ERA3-24
3. provides mutation suites that deliberately create:
   - over-smoothing
   - implication stripping
   - symbolic flattening
   - rhythm normalization
   - proof inflation
4. encodes expected evaluator reactions for each failure class
5. feeds `FR-ERA3-27` with evidence-backed contrast assets rather than generic anti-examples
6. emits downgrade/block/review guidance for downstream consumers

The corpus is not a registry of truth. It is a **registry of what should feel wrong, hollow, synthetic, prestige-theatrical, vanity-heavy, or suspiciously resolved even when the surface remains coherent.**

### 2.3 Scope

**In scope**

- typed perceptual failure corpus objects
- typed mutation operators and mutation suites
- typed failure-label bundles and expected evaluator-outcome bundles
- contrast harness service for generating and validating failure probes
- interop with `FR-ERA3-24`, `FR-ERA3-25`, `FR-ERA3-26`, and `FR-ERA3-27`
- failure-closed fallback and targeted reload behavior
- versioned corpus manifest and expansion workflow
- receipt-chain logging and audit trail design

**Out of scope**

- semantic hard-negative corpus ownership (`FR-ERA3-24`)
- canonical function-family ownership (`FR-ERA3-25`)
- profile assembly ownership (`FR-ERA3-26`)
- perceptual scoring logic itself (`FR-ERA3-27`)
- full UI surfacing of harness output
- generalized safety moderation unrelated to CCP perceptual doctrine

---

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Component | Source | What It Does |
|--------|-----------|--------|--------------|
| `DEP-SFL-028-01` | `PerceptualFailureCorpusManifest` | FR-ERA3-28 | Typed manifest of versioned perceptual failure assets and mutation suites |
| `DEP-SFL-028-02` | `PerceptualContrastCaseRecord` | FR-ERA3-28 | Base model for a single perceptual failure contrast asset |
| `DEP-SFL-028-03` | `FalseDepthContrastCase` | FR-ERA3-28 | Models artifacts that perform profundity without real symbolic or evidentiary depth |
| `DEP-SFL-028-04` | `DeadPolishContrastCase` | FR-ERA3-28 | Models artifacts whose polish collapses human texture, asymmetry, or memorability |
| `DEP-SFL-028-05` | `SyntheticAuthorityContrastCase` | FR-ERA3-28 | Models artifacts that simulate authority through prestige signals rather than earned proof |
| `DEP-SFL-028-06` | `OverresolvedMeaningCase` | FR-ERA3-28 | Models artifacts that over-explain, over-close, or erase productive ambiguity |
| `DEP-SFL-028-07` | `EmptyMotivationalSmoothnessCase` | FR-ERA3-28 | Models smooth uplift or inspiration without grounded signal, proof, or lived charge |
| `DEP-SFL-028-08` | `PerceptualMutationOperation` | FR-ERA3-28 | Typed mutation operator definition for generating failure probes |
| `DEP-SFL-028-09` | `PerceptualMutationSuite` | FR-ERA3-28 | Bundled mutation operations linked to a contrast case or target surface |
| `DEP-SFL-028-10` | `PerceptualFailureCorpusService` | FR-ERA3-28 | Runtime loader, resolver, lookup service, and manifest guard |
| `DEP-SFL-028-11` | `PerceptualContrastHarness` | FR-ERA3-28 | Executes contrastive probes and mutation suites against evaluator contracts |
| `DEP-SFL-028-12` | `PerceptualFailureHarnessReport` | FR-ERA3-28 | Typed runtime report for corpus resolution, probe results, and verdicts |
| `DEP-SFL-028-13` | `PerceptualFailureDecisionRouter` | FR-ERA3-28 | Maps expectation mismatches to downgrade / review / block recommendations |
| `DEP-SFL-028-14` | `SemanticInteropReference` | FR-ERA3-28 | References linked semantic hard negatives from FR-ERA3-24 without ownership collapse |

### 3.2 Why This Corpus Exists in the SFL Stack

`FR-ERA3-24` already protects against **semantic** deceptively close failures. `FR-ERA3-28` exists because CCP also needs to detect **perceptual** deceptively close failures:

```text
semantically valid
but too smooth to trust
but too explicit to remember
but too prestigious to believe
but too motivational to respect
but too polished to feel human
```

That means the runtime protection stack is:

```text
canonical truth / invariants / geometry
-> semantic hard-negative adjacency + mutation resistance (FR-ERA3-24)
-> SFL function selection and profile assembly (FR-ERA3-25, FR-ERA3-26)
-> perceptual influence scoring (FR-ERA3-27)
-> perceptual failure contrast + mutation pressure (FR-ERA3-28)
```

The first two layers ask:

- is the meaning corrupt?
- is the direction unsafe?

This layer asks:

- even if the meaning is safe, does the artifact feel fake-deep, suspiciously perfect, prestige-theatrical, or emotionally empty?

### 3.3 Existing Backend Integration

| File | Path | How This Spec Uses It |
|------|------|-----------------------|
| `adversarial_validator.py` | `src/ccp/services/adversarial_validator.py` | Pattern precedent for adversarial sample evaluation, result bundles, and failure reasons |
| `trait_scoring_engine.py` | `src/ccp/services/trait_scoring_engine.py` | Pattern precedent for evidence-backed dimensional scoring with structured evidence |
| `boredom_ban.py` | `src/ccp/core/boredom_ban.py` | Pattern precedent for maintaining a corpus of known conflicts and emitting avoidance instructions |
| `receipt_chain.py` | `src/ccp/core/receipt_chain.py` | Immutable audit-trail precedent for corpus loads, probe executions, and verdict logging |
| `perceptual_influence_evaluator.py` | `src/ccp/services/perceptual_influence_evaluator.py` | Primary consumer; FR-ERA3-28 defines the adversarial assets its analyzers should consult |

### 3.4 Interop Boundary with FR-ERA3-24

The semantic and perceptual corpora must be **linked but not merged**.

| Concern | FR-ERA3-24 Owns | FR-ERA3-28 Owns |
|---|---|---|
| Main question | “Is the meaning directionally unsafe?” | “Does the delivery feel fake-deep, dead, hollow, prestige-theatrical, or low-trust?” |
| Example failure | invariant weakening, representation drift, trajectory inversion | false depth, dead polish, synthetic authority, overresolution, empty smoothness |
| Typical output | semantic fail / warning / block evidence | downgrade / review / block evidence for perceptual quality |
| Asset type | hard-negative contrast pair | perceptual contrast case |
| Mutation class | direction corruption | delivery deadening / false-depth induction |

Interop rules:

1. a single artifact may reference both a semantic hard negative and a perceptual failure case
2. `FR-ERA3-28` may link to `hard_negative_id` values from `FR-ERA3-24` through `SemanticInteropReference`
3. `FR-ERA3-28` must never duplicate semantic hard-negative definitions inline as owned records
4. downstream engines may combine semantic and perceptual reports, but must keep the source dimensions distinct

### 3.5 Governance Constraints

| Constraint | Origin | Implementation Mechanism |
|---|---|---|
| Anti-Centroid Law preservation | PRD-02, PRD-06, SFL doctrine | corpus must include dead-polish and safe-average failure assets |
| Negative-space boundary hardening | SFL doctrine | corpus must encode what forms of polish, proof, and implication should be rejected |
| False-depth rejection | SFL doctrine, PRD-09 | first-class corpus object + expected downgrade/block behavior |
| Synthetic-authority detection | PRD-06, PRD-09, PRD-03 | dedicated contrast class with proof-inflation mutation operators |
| Adversarial contrast discipline | FR-ERA3-24 precedent | structured case records, mutation suites, and receipt logging |
| Persuasion is allowed; misalignment is not | explicit user direction + SFL doctrine | aligned covert suggestion / hidden intention remain legal functions; corpus only captures their hollow, manipulative, prestige-theatrical, or proofless variants |

### 3.6 Technical Decisions

| Decision | Rationale | Alternative Rejected | Why Rejected |
|----------|-----------|----------------------|--------------|
| Separate perceptual failure corpus from semantic hard-negative corpus | protects the semantic/perceptual boundary and keeps each layer intelligible | merge FR-24 and FR-28 into one giant “bad corpus” | collapses roles, muddies diagnostics, and makes tuning impossible |
| Model named failure classes explicitly | prompt requires concrete corpus objects and downstream systems need stable labels | store only generic “negative example” text blobs | impossible to route, test, version, or compare over time |
| Keep mutation operators typed and finite | reproducible testing and deterministic harness behavior | fully free-form LLM-generated failure probes only | too noisy for regression and too hard to audit |
| Use expectation bundles tied to FR-27 dimensions | keeps the corpus executable rather than descriptive | store prose notes only | cannot drive automated harness tests or downgrade/block routing |
| Allow shared linking to FR-24 semantic cases | some assets fail semantically and perceptually at once | forbid interop entirely | loses valuable traceability and forces duplicate assets |
| Failure-closed targeted reload | corpus corruption should not silently weaken perceptual protection | best-effort partial reload with silent drops | dangerous on commercial and proof surfaces |

---

## 4. Implementation Plan

### Phase A: Models and Manifest Contracts

- [ ] **Task 1:** Create `src/ccp/models/perceptual_failure_corpus_models.py`.
- [ ] **Task 2:** Define enums for:
  - `PerceptualFailureClass`
  - `MutationOperatorKind`
  - `PerceptualExpectationStatus`
  - `PerceptualHarnessDecision`
  - `PerceptualSurfaceClass`
- [ ] **Task 3:** Implement base and specialized contrast-case models:
  - `PerceptualContrastCaseRecord`
  - `FalseDepthContrastCase`
  - `DeadPolishContrastCase`
  - `SyntheticAuthorityContrastCase`
  - `OverresolvedMeaningCase`
  - `EmptyMotivationalSmoothnessCase`
- [ ] **Task 4:** Implement manifest, mutation suite, expectation bundle, and report payload models.

### Phase B: Corpus Storage Layout and Loader

- [ ] **Task 5:** Create canonical storage root:
  - `sfl/failure_corpus/manifest.yaml`
  - `sfl/failure_corpus/false_depth/`
  - `sfl/failure_corpus/dead_polish/`
  - `sfl/failure_corpus/synthetic_authority/`
  - `sfl/failure_corpus/overresolved_meaning/`
  - `sfl/failure_corpus/empty_motivational_smoothness/`
  - `sfl/failure_corpus/mutation_suites/`
- [ ] **Task 6:** Implement `PerceptualFailureCorpusService` for warm load, lookup, targeted reload, and manifest validation.
- [ ] **Task 7:** Add reload rollback semantics: on failure, keep the last validated in-memory corpus active.

### Phase C: Mutation and Contrast Harness

- [ ] **Task 8:** Create `src/ccp/services/perceptual_contrast_harness.py`.
- [ ] **Task 9:** Implement typed mutation operators:
  - `OVER_SMOOTHING`
  - `IMPLICATION_STRIPPING`
  - `SYMBOLIC_FLATTENING`
  - `RHYTHM_NORMALIZATION`
  - `PROOF_INFLATION`
  - `PRESTIGE_THEATER_INJECTION`
  - `MOTIVATIONAL_SOFTENING`
  - `PAUSE_WEIGHT_REMOVAL`
- [ ] **Task 10:** Implement `run_case_probe()` and `run_mutation_suite()` against `FR-ERA3-27` expectation contracts.
- [ ] **Task 11:** Implement mismatch classification:
  - evaluator caught the failure as expected
  - evaluator under-reacted
  - evaluator over-reacted
  - probe invalid due to prerequisite failure

### Phase D: FR-24 / FR-27 Interop

- [ ] **Task 12:** Add `SemanticInteropReference` fields linking optional FR-24 hard-negative IDs.
- [ ] **Task 13:** Add service methods for joint resolution:
  - semantic-linked perceptual cases
  - perceptual-only cases
  - shared mutation lineage
- [ ] **Task 14:** Ensure `FR-ERA3-27` can request:
  - top relevant cases by surface + function family
  - mutation suites by failure class
  - evaluator expectation bundles by card/archetype/surface profile

### Phase E: Tests and Receipts

- [ ] **Task 15:** Create `tests/integration/test_era3_fr28_perceptual_failure_corpus.py`.
- [ ] **Task 16:** Create `tests/integration/test_era3_fr28_perceptual_contrast_harness.py`.
- [ ] **Task 17:** Add receipt actions:
  - `perceptual-failure-corpus-warm`
  - `perceptual-failure-case-resolve`
  - `perceptual-failure-suite-run`
  - `perceptual-failure-reload`
- [ ] **Task 18:** Validate failure-closed behavior for corrupt manifests, missing expectation bundles, and illegal semantic ownership duplication.

---

## 5. Primary Output Schema

```python
# src/ccp/models/perceptual_failure_corpus_models.py
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PerceptualFailureClass(str, Enum):
    FALSE_DEPTH = "false_depth"
    DEAD_POLISH = "dead_polish"
    SYNTHETIC_AUTHORITY = "synthetic_authority"
    OVERRESOLVED_MEANING = "overresolved_meaning"
    EMPTY_MOTIVATIONAL_SMOOTHNESS = "empty_motivational_smoothness"


class MutationOperatorKind(str, Enum):
    OVER_SMOOTHING = "over_smoothing"
    IMPLICATION_STRIPPING = "implication_stripping"
    SYMBOLIC_FLATTENING = "symbolic_flattening"
    RHYTHM_NORMALIZATION = "rhythm_normalization"
    PROOF_INFLATION = "proof_inflation"
    PRESTIGE_THEATER_INJECTION = "prestige_theater_injection"
    MOTIVATIONAL_SOFTENING = "motivational_softening"
    PAUSE_WEIGHT_REMOVAL = "pause_weight_removal"


class PerceptualExpectationStatus(str, Enum):
    EXPECT_DOWNGRADE = "expect_downgrade"
    EXPECT_REVIEW = "expect_review"
    EXPECT_BLOCK = "expect_block"
    EXPECT_WARNING = "expect_warning"


class PerceptualHarnessDecision(str, Enum):
    PASS = "pass"
    REVIEW = "review"
    DOWNGRADE = "downgrade"
    BLOCK = "block"
    INVALID = "invalid"
    ERROR = "error"


class PerceptualSurfaceClass(str, Enum):
    SEMANTIC_PLANNING = "semantic_planning"
    RENDER_RELEASE = "render_release"
    COACHING_INTERVENTION = "coaching_intervention"
    SOCIAL_REACTION = "social_reaction"
    LONG_FORM_AUTHORITY = "long_form_authority"
    COMMERCIAL_TRUST_TRANSFER = "commercial_trust_transfer"
    PHASE0_AUDIT_PROOF = "phase0_audit_proof"


class FailureLabelBundle(BaseModel):
    model_config = ConfigDict(extra="forbid")

    primary_label: str = Field(..., min_length=3, max_length=80)
    public_label: str = Field(..., min_length=3, max_length=80)
    short_badge: str = Field(..., min_length=2, max_length=32)
    failure_class: PerceptualFailureClass
    descriptor_tags: list[str] = Field(default_factory=list)
    symptom_markers: list[str] = Field(default_factory=list)
    remediation_markers: list[str] = Field(default_factory=list)


class EvaluatorExpectationBundle(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expected_status: PerceptualExpectationStatus
    minimum_human_congruence_drop: float = Field(..., ge=0.0, le=1.0)
    minimum_memorability_drop: float = Field(..., ge=0.0, le=1.0)
    minimum_symbolic_density_drop: float = Field(..., ge=0.0, le=1.0)
    minimum_contrast_clarity_drop: float = Field(..., ge=0.0, le=1.0)
    minimum_overexplanation_risk_rise: float = Field(..., ge=0.0, le=1.0)
    minimum_synthetic_smoothness_rise: float = Field(..., ge=0.0, le=1.0)
    route_block_surfaces: list[PerceptualSurfaceClass] = Field(default_factory=list)
    route_review_surfaces: list[PerceptualSurfaceClass] = Field(default_factory=list)
    rationale: str = Field(..., min_length=20, max_length=800)


class SemanticInteropReference(BaseModel):
    model_config = ConfigDict(extra="forbid")

    linked_hard_negative_ids: list[str] = Field(default_factory=list)
    linked_invariant_ids: list[str] = Field(default_factory=list)
    linked_geometry_ids: list[str] = Field(default_factory=list)
    ownership_statement: str = Field(
        default="Semantic hard negatives remain owned by FR-ERA3-24; this object only references them."
    )


class PerceptualMutationOperation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(..., pattern=r"^PMO-[A-Z0-9-]{4,64}$")
    kind: MutationOperatorKind
    label: str = Field(..., min_length=3, max_length=120)
    description: str = Field(..., min_length=20, max_length=800)
    severity: float = Field(..., ge=0.0, le=1.0)
    config: dict[str, Any] = Field(default_factory=dict)


class PerceptualMutationSuite(BaseModel):
    model_config = ConfigDict(extra="forbid")

    suite_id: str = Field(..., pattern=r"^PMS-[A-Z0-9-]{4,64}$")
    label: str = Field(..., min_length=3, max_length=120)
    target_failure_class: PerceptualFailureClass
    target_surfaces: list[PerceptualSurfaceClass] = Field(default_factory=list)
    operations: list[PerceptualMutationOperation] = Field(..., min_length=1)
    expectation_bundle: EvaluatorExpectationBundle
    notes: Optional[str] = Field(default=None, max_length=800)


class PerceptualContrastCaseRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str = Field(..., pattern=r"^PFC-[A-Z0-9-]{4,64}$")
    failure_class: PerceptualFailureClass
    title: str = Field(..., min_length=5, max_length=160)
    summary: str = Field(..., min_length=30, max_length=1000)
    labels: FailureLabelBundle
    source_surface: PerceptualSurfaceClass
    source_archetype_ids: list[str] = Field(default_factory=list)
    source_function_family_ids: list[str] = Field(default_factory=list)
    valid_anchor_excerpt: str = Field(..., min_length=30, max_length=2500)
    failing_variant_excerpt: str = Field(..., min_length=30, max_length=2500)
    why_it_fails: list[str] = Field(..., min_length=1)
    what_it_fake_signals: list[str] = Field(default_factory=list)
    what_it_erases: list[str] = Field(default_factory=list)
    expectation_bundle: EvaluatorExpectationBundle
    semantic_interop: SemanticInteropReference = Field(default_factory=SemanticInteropReference)
    mutation_suite_ids: list[str] = Field(default_factory=list)
    maintained: bool = Field(default=True)
    version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$")


class FalseDepthContrastCase(PerceptualContrastCaseRecord):
    failure_class: PerceptualFailureClass = Field(default=PerceptualFailureClass.FALSE_DEPTH)


class DeadPolishContrastCase(PerceptualContrastCaseRecord):
    failure_class: PerceptualFailureClass = Field(default=PerceptualFailureClass.DEAD_POLISH)


class SyntheticAuthorityContrastCase(PerceptualContrastCaseRecord):
    failure_class: PerceptualFailureClass = Field(default=PerceptualFailureClass.SYNTHETIC_AUTHORITY)


class OverresolvedMeaningCase(PerceptualContrastCaseRecord):
    failure_class: PerceptualFailureClass = Field(default=PerceptualFailureClass.OVERRESOLVED_MEANING)


class EmptyMotivationalSmoothnessCase(PerceptualContrastCaseRecord):
    failure_class: PerceptualFailureClass = Field(default=PerceptualFailureClass.EMPTY_MOTIVATIONAL_SMOOTHNESS)


class PerceptualFailureCorpusManifest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    manifest_version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$")
    generated_at: datetime
    schema_version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$")
    corpus_root: str
    case_counts: dict[str, int] = Field(default_factory=dict)
    suite_counts: dict[str, int] = Field(default_factory=dict)
    maintained_case_ids: list[str] = Field(default_factory=list)
    maintained_suite_ids: list[str] = Field(default_factory=list)
    deprecated_case_ids: list[str] = Field(default_factory=list)
    deprecated_suite_ids: list[str] = Field(default_factory=list)
    notes: Optional[str] = Field(default=None, max_length=1200)


class PerceptualHarnessProbeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    probe_id: str = Field(..., pattern=r"^PFP-[A-Z0-9-]{4,64}$")
    candidate_text: str = Field(..., min_length=20)
    surface_class: PerceptualSurfaceClass
    case_ids: list[str] = Field(default_factory=list)
    suite_ids: list[str] = Field(default_factory=list)
    evaluate_mutations: bool = Field(default=True)
    metadata: dict[str, Any] = Field(default_factory=dict)


class PerceptualHarnessProbeResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    probe_id: str
    case_id: Optional[str] = None
    suite_id: Optional[str] = None
    operation_id: Optional[str] = None
    expected_status: Optional[PerceptualExpectationStatus] = None
    observed_decision: PerceptualHarnessDecision
    decision_match: bool
    evidence: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    remediation: list[str] = Field(default_factory=list)


class PerceptualFailureHarnessReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    report_id: str = Field(..., pattern=r"^PFR-[A-Z0-9-]{4,64}$")
    evaluated_at: datetime
    request: PerceptualHarnessProbeRequest
    resolved_case_ids: list[str] = Field(default_factory=list)
    resolved_suite_ids: list[str] = Field(default_factory=list)
    decision: PerceptualHarnessDecision
    results: list[PerceptualHarnessProbeResult] = Field(default_factory=list)
    summary: str = Field(..., min_length=20, max_length=1200)
    receipt_ids: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


@field_validator("linked_hard_negative_ids", mode="before")
@classmethod
def _normalize_linked_hard_negative_ids(cls, value: Any) -> list[str]:
    if value is None:
        return []
    return list(value)
```

### 5.1 Storage Layout

```text
sfl/
  failure_corpus/
    manifest.yaml
    false_depth/
      PFC-FD-*.yaml
    dead_polish/
      PFC-DP-*.yaml
    synthetic_authority/
      PFC-SA-*.yaml
    overresolved_meaning/
      PFC-OM-*.yaml
    empty_motivational_smoothness/
      PFC-EMS-*.yaml
    mutation_suites/
      PMS-*.yaml
```

### 5.2 Corpus Record Rules

- every case must have one `valid_anchor_excerpt`
- every case must have one `failing_variant_excerpt`
- every case must define `why_it_fails`
- every case must define one `EvaluatorExpectationBundle`
- semantic linkage is optional, but when present it must only reference external IDs
- no case may embed semantic hard-negative ownership data inline

---

## 6. Components and Behavior

### 6.1 `PerceptualFailureCorpusService`

Primary responsibilities:

- warm-load manifest and typed case records
- validate case-class-to-directory consistency
- resolve cases by:
  - `case_id`
  - `failure_class`
  - `surface_class`
  - `source_function_family_ids`
  - `source_archetype_ids`
- resolve mutation suites by:
  - `suite_id`
  - `target_failure_class`
  - `target_surfaces`
- expose linked FR-24 references without taking ownership
- emit receipts for:
  - warm load
  - targeted reload
  - case resolution
  - suite resolution

Core methods:

- `warm() -> PerceptualFailureCorpusManifest`
- `reload(case_ids: list[str] | None = None, suite_ids: list[str] | None = None) -> PerceptualFailureCorpusManifest`
- `get_case(case_id: str) -> PerceptualContrastCaseRecord`
- `find_cases(surface_class, function_family_ids, archetype_ids, failure_classes=None) -> list[PerceptualContrastCaseRecord]`
- `get_suite(suite_id: str) -> PerceptualMutationSuite`
- `find_suites(target_failure_class, target_surface=None) -> list[PerceptualMutationSuite]`

### 6.2 `PerceptualContrastHarness`

Primary responsibilities:

- materialize targeted probes from typed contrast cases
- apply deterministic mutation operations
- call the `FR-ERA3-27` evaluator with:
  - the anchor excerpt
  - the failing variant
  - the mutated variant
- compare observed decisions against `EvaluatorExpectationBundle`
- classify:
  - expected downgrade/review/block hit
  - under-reaction
  - over-reaction
  - invalid semantic prerequisite

Core methods:

- `run_case_probe(request: PerceptualHarnessProbeRequest) -> PerceptualFailureHarnessReport`
- `run_mutation_suite(case_id: str, suite_id: str, surface_class: PerceptualSurfaceClass) -> PerceptualFailureHarnessReport`
- `materialize_mutation(base_text: str, operation: PerceptualMutationOperation) -> str`
- `compare_to_expectation(expected, observed) -> PerceptualHarnessProbeResult`

### 6.3 Mutation Semantics

The harness does not mutate truth conditions directly. It mutates **delivery characteristics** that degrade trust, force, or human congruence.

Required mutation operators:

1. `OVER_SMOOTHING`
   - evens cadence
   - removes rough edges
   - normalizes sentence length
   - produces suspiciously frictionless copy

2. `IMPLICATION_STRIPPING`
   - removes layered meaning
   - explains hidden logic too explicitly
   - turns subtext into exposition

3. `SYMBOLIC_FLATTENING`
   - replaces weighted symbols with generic language
   - reduces identity compression
   - lowers interpretive density

4. `RHYTHM_NORMALIZATION`
   - removes pause weight
   - reduces tension contrast
   - makes delivery rhythm statistically familiar

5. `PROOF_INFLATION`
   - overstates outcomes
   - inserts prestige-signaling social proof
   - simulates authority without earned evidence

6. `PRESTIGE_THEATER_INJECTION`
   - adds high-status grandiosity
   - inserts cinematic but hollow significance signals

7. `MOTIVATIONAL_SOFTENING`
   - turns lived conviction into broad encouragement
   - removes pressure and consequence

8. `PAUSE_WEIGHT_REMOVAL`
   - erases silence, interruption, and asymmetry cues
   - weakens human feel without overtly changing content topic

### 6.4 Decision Routing

Harness-level routing rules:

- `BLOCK`
  - expected block surface is missed by evaluator
  - or corrupt/missing corpus dependency on high-risk surfaces

- `DOWNGRADE`
  - evaluator under-reacts to known perceptual failure
  - or case evidence is contradictory but not fatal

- `REVIEW`
  - borderline mismatch
  - or unexpected over-reaction that suggests threshold tuning

- `PASS`
  - evaluator behavior matches expectation bundle across the full probe

### 6.5 Failure-Closed Rules

Must fail closed when:

- manifest schema invalid
- case record points to illegal failure class / directory mismatch
- expectation bundle missing required FR-27 dimensions
- semantic interop section attempts to inline semantic hard-negative ownership
- requested suite references missing operations
- targeted reload yields inconsistent maintained/deprecated state

On failure:

- do not swap the active corpus
- retain last validated corpus in memory
- log a receipt with `decision="rejected"` or `decision="flagged"`
- emit operator-visible rationale

---

## 7. Data Contracts, Rules, and Receipts

### 7.1 Corpus IDs

| Artifact | Pattern |
|---|---|
| Perceptual case | `PFC-[A-Z0-9-]+` |
| Mutation operation | `PMO-[A-Z0-9-]+` |
| Mutation suite | `PMS-[A-Z0-9-]+` |
| Probe request | `PFP-[A-Z0-9-]+` |
| Harness report | `PFR-[A-Z0-9-]+` |

### 7.2 Required Receipt Actions

| Stage | Agent ID | Action | Decision Values |
|---|---|---|---|
| Warm load | `perceptual-failure-corpus-service` | `perceptual-failure-corpus-warm` | `approved`, `rejected`, `flagged` |
| Targeted reload | `perceptual-failure-corpus-service` | `perceptual-failure-reload` | `approved`, `rejected`, `rolled_back` |
| Case resolve | `perceptual-failure-corpus-service` | `perceptual-failure-case-resolve` | `resolved`, `missing`, `flagged` |
| Suite resolve | `perceptual-failure-corpus-service` | `perceptual-failure-suite-resolve` | `resolved`, `missing`, `flagged` |
| Probe run | `perceptual-contrast-harness` | `perceptual-failure-probe-run` | `pass`, `review`, `downgrade`, `block`, `invalid` |
| Mutation run | `perceptual-contrast-harness` | `perceptual-failure-suite-run` | `pass`, `review`, `downgrade`, `block`, `invalid` |

### 7.3 Receipt Metadata Minimums

Every probe or suite receipt must include:

- `surface_class`
- `resolved_case_ids`
- `resolved_suite_ids`
- `expected_statuses`
- `observed_decisions`
- `semantic_interop_hits`
- `mismatch_count`
- `rolled_back` when applicable

---

## 8. Acceptance Criteria

### AC-28.1 - Typed perceptual failure corpus

The system SHALL define typed corpus objects for:

- `FalseDepthContrastCase`
- `DeadPolishContrastCase`
- `SyntheticAuthorityContrastCase`
- `OverresolvedMeaningCase`
- `EmptyMotivationalSmoothnessCase`

and SHALL reject free-form untyped negative-example blobs as canonical corpus records.

### AC-28.2 - Perceptual mutation harness

The system SHALL support deterministic mutation operators for:

- over-smoothing
- implication stripping
- symbolic flattening
- rhythm normalization
- proof inflation

and SHALL allow suite-based execution against evaluator expectations.

### AC-28.3 - FR-24 interop without merger

The system SHALL support semantic interop references to `FR-ERA3-24` hard-negative IDs while preserving separate ownership, manifests, loaders, and artifact classes.

### AC-28.4 - Expected evaluator behavior

Every corpus case SHALL include an `EvaluatorExpectationBundle` that encodes:

- expected downgrade/review/block status
- minimum dimensional deltas relevant to FR-27
- route-block and route-review surfaces

### AC-28.5 - Failure-closed reload and rollback

The corpus service SHALL preserve the last validated in-memory corpus when targeted reload or warm load fails and SHALL emit an explicit reload receipt containing rollback status.

### AC-28.6 - Commercial and proof-surface readiness

The corpus SHALL include sufficient cases to challenge:

- trust-transfer proof objects
- cinematic prestige surfaces
- reaction-driven authority surfaces
- Phase-0 audit/proof outputs

so that false depth and synthetic authority on commercial surfaces are explicitly testable.

### AC-28.7 - No false registry collapse

The implementation SHALL NOT:

- store perceptual failure assets inside the FR-25 function registry
- store them inside the FR-24 semantic hard-negative corpus
- treat them as canonical ontology rows

---

## 9. Testing Strategy

### 9.1 Integration Test Files

- `tests/integration/test_era3_fr28_perceptual_failure_corpus.py`
- `tests/integration/test_era3_fr28_perceptual_contrast_harness.py`

### 9.2 Required Test Coverage

1. **Manifest load tests**
   - valid warm load produces manifest + case counts
   - invalid schema fails closed
   - directory/class mismatch is rejected

2. **Typed case tests**
   - each named case class validates correctly
   - missing expectation bundle fails validation
   - semantic interop refs do not allow owned semantic definitions

3. **Mutation suite tests**
   - required mutation kinds materialize deterministically
   - suite without operations fails validation
   - suite expectation bundle mismatch is surfaced

4. **Interop tests**
   - FR-24 linked case IDs remain references only
   - perceptual-only case resolves with empty semantic links
   - mixed semantic/perceptual probe report preserves both sources distinctly

5. **Harness decision tests**
   - expected block hit returns `PASS`
   - evaluator under-reaction returns `DOWNGRADE` or `BLOCK` depending on surface
   - evaluator over-reaction returns `REVIEW`
   - invalid semantic prerequisite returns `INVALID`

6. **Reload rollback tests**
   - targeted reload success swaps only requested records
   - targeted reload failure retains prior active corpus
   - receipt metadata contains rollback marker

### 9.3 Sample Test Scenarios

- `test_false_depth_case_requires_symbolic_density_and_humanity_drop`
- `test_dead_polish_case_detects_over_smoothing_and_pause_weight_loss`
- `test_synthetic_authority_case_flags_proof_inflation_on_commercial_surface`
- `test_overresolved_meaning_case_routes_review_on_low_risk_surface_but_block_on_phase0_proof`
- `test_semantic_interop_reference_does_not_inline_hard_negative_ownership`
- `test_failed_reload_keeps_previous_validated_manifest_active`

---

## 10. Build Notes and Future Integration

### 10.1 Immediate Consumers

`FR-ERA3-28` should be consumed next by:

- `FR-ERA3-27 Perceptual Influence Evaluator`
- `FR-ERA3-16 Archetype Container Runtime`
- `FR-ERA3-12 CMF Arc Governed Rendering`
- `FR-ERA3-18 CBCS Four-Engine Runtime`
- Phase-0 audit/proof stack later, especially:
  - `FR-ERA3-35A`
  - `FR-ERA3-35B`
  - `FR-ERA3-35C`
  - `FR-ERA3-35`

### 10.2 Seed Corpus Guidance

Wave-1 corpus seeding should prioritize:

1. **Commercial trust transfer**
   - fake-lite proof
   - prestige-heavy carousel cards
   - cinematic false authority

2. **Reaction surfaces**
   - conflict theater
   - humiliation disguised as boldness
   - engagement-friendly but low-trust escalation

3. **Audit / Phase-0 proof surfaces**
   - over-explained diagnosis
   - too polished to believe
   - motivational uplift without grounded prescription

4. **CMF render surfaces**
   - gorgeous but generic symbolism
   - synthetic smoothness
   - documentary-truth erosion

### 10.3 Brownfield Notes

- The repository already contains adversarial validation patterns; reuse them.
- Do not build a generic content moderation engine here.
- Do not flatten perceptual failure into a single “AI slop” label.
- Do not ban all covert suggestion or hidden-intention mechanics. This spec exists to separate aligned, human-grounded influence from hollow, prestige-theatrical, or trust-eroding variants.
- Keep the corpus composable enough for Phase-0 audit cards and proof-object evaluation later.

### 10.4 Summary

`FR-ERA3-24` protects meaning from semantic counterfeit.  
`FR-ERA3-28` protects delivery from perceptual counterfeit.

The system needs both. Without this spec, CCP can still tell the truth while sounding dead, fake-deep, suspiciously polished, or commercially untrustworthy. That is exactly the class of failure the SFL layer exists to prevent.
