# Tech-Spec: FR-ERA3-27 - Perceptual Influence Evaluator
**Created:** 2026-05-19  
**Status:** Ready for Development  
**Version:** 1.0 (ERA3 Architecture - SFL Foundation)  
**Phase:** 6 - Subliminal Function Layer Foundation  
**Architecture Reference:** `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`

---

## Pre-Work Log

```text
1. PROTOCOL LOADED:   ERA3_Tech_Spec_Writing_Protocol.md. Confirmed mandatory 10-section spec format, typed-model expectation, architecture traceability, file-read log, and CBAR mandate enforcement table discipline.
2. PRD-02 LOADED:     PRD_02_CCF_Content_Factory.md §3.4A. Proof quote captured: "signal -> coach reaction -> invariant field -> primitive coalition -> edge product -> archetypal geometry check -> archetype container -> subliminal function stack -> composition depth profile -> variation profile -> directional integrity validation -> perceptual influence validation -> JIT script contract -> render blueprint". Confirms `perceptual influence validation` is an explicit named stage in the canonical runtime law, placed after directional integrity and before JIT contract.
3. PRD-03 LOADED:     PRD_03_CMF_Media_Factory.md §3.3A. Proof quote captured: rendering must "explicitly preserve SDA-level Representation Geometry, Invariant Field, and Directional Integrity". Confirms CMF renders can be semantically valid yet perceptually dead, too smooth, too explicit, or too flat — the exact gap this evaluator fills.
4. PRD-05 LOADED:     PRD_05_CBCS_Law28.md §7.1A. Proof quote captured: "a coaching intervention can improve short-term energy while still distorting identity, misreading local invariants, or reinforcing an unhealthy loop". Confirms that perceptual aliveness without semantic grounding is a failure class — but also that semantic correctness without perceptual force is a separate evaluable gap.
5. PRD-06 LOADED:     PRD_06_Conscious_Reactions.md §3.1. Proof quote captured: "We are not automating fake expertise; we are extracting, refining, and broadcasting real judgment." Confirms that human congruence is a first-class evaluation dimension — artifacts must feel human-generated, not synthetically assembled.
6. PRD-09 LOADED:     PRD_09_CPSC_Silent_Referral.md §5.3A. Proof quote captured: "growth/commercial systems are where deceptively close semantic corruption is especially dangerous" and "the commercial layer must now follow the same human-first doctrine as the rest of the product". Confirms commercial surfaces require perceptual evaluation to distinguish real proof from vanity display.
7. SFL CORE DOC:      lab/subliminal_function_layer_for_ccp_v_1.md §1. Evaluator-relevant claim: "SDA protects semantic truthfulness. SFL shapes perceptual potency and symbolic aliveness." Confirmed: this evaluator is the runtime scoring gate for the SFL side — it measures whether perceptual potency and symbolic aliveness are actually present.
8. SFL FUNCTION DOC:  lab/Subliminal Functions for Agentic Content Architecture.md. Evaluator-relevant claim: the 120 associations include both semantic operators and perception-shaping primitives, and must not be treated as a flat ontology. Confirmed: evaluator metrics must distinguish function activation from felt perceptual effect.
9. ASSOCIATION CHAT:  lab/120 subliminal associations Chat.md. Evaluator-relevant claim: the architectural tension between semantic truthfulness and adaptive vitality, and the need to avoid semantic ossification. Confirmed: this evaluator must reject dead polish and over-optimization without banning persuasion.
10. SDA CORE DOC:     lab/semantic_discernment_architecture_content_engine_v_1.md. Evaluator-relevant claim: the main failure class is deceptively close output that passes superficial coherence while corrupting meaning. Confirmed: FR-ERA3-27 must not duplicate this semantic validation — it evaluates perceptual delivery quality on top of assumed semantic validity from FR-ERA3-22.
11. SDA TAXONOMY DOC: lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md. Evaluator-relevant claim: Perceptual Effect Metric is a distinct artifact class from Function Definition and from Canonical Ontology. Confirmed: evaluator metrics like cognitive_imprint_score belong to the evaluator, not to FR-ERA3-25.
12. PPA DOC:          Perceptual_Primitives_Architecture.md. Evaluator-relevant claim: primitives are not edges; the stack is "CRAL evidence -> primitive spaces -> candidate survival -> coalition signature -> edge product -> CCF routing". Confirmed: this evaluator validates the perceptual quality of the emergent product, not the primitive selection itself.
13. FR-ERA3-22 READ:  Directional Integrity Engine Tech Spec. Confirmed four DI dimensions: invariant_preservation_score, representation_drift_score, hard_negative_adjacency_score, trajectory_risk_score. Confirmed PASS/REVIEW/FAIL decision states, surface-class routing, and failure-closed discipline. FR-ERA3-27 must interop with these results without re-evaluating semantic direction.
14. FR-ERA3-25 READ:  Subliminal Function Library and Taxonomy Tech Spec. Confirmed canonical SFL artifact classes, family compression rules, function definitions, crosswalks, and the explicit note: "Metrics such as cognitive_imprint_score and symbolic_density_score are intentionally not stored here as canonical records. They belong to FR-ERA3-27."
15. BACKEND FILE READ: src/ccp/services/trait_scoring_engine.py. Verified method: `TraitScoringEngine.score_all_traits(self) -> list[ScoredTrait]`. Confirmed evidence-backed per-dimension scoring with rubric points and cited source references.
16. BACKEND FILE READ: src/ccp/services/semantic_affinity_guard.py. Verified method: `SemanticAffinityGuard.evaluate(self, batch_metadata: BatchMetadata, pain_map: PainMapInput) -> SemanticAffinityClearance`. Confirmed 3-stage pipeline, PASS/OPERATOR_REVIEW/FAIL_TERMINAL gate, fallback to PROVISIONAL_MEDIUM, ghost variable prevention.
17. BACKEND FILE READ: src/ccp/services/content_machine.py. Verified method: `ContentMachinePipeline.process_session(self, session_report: dict[str, Any], coach_id: str, coach_acronym: str = "CCH") -> ContentMachineResult`. Confirmed multi-stage extraction, validation, and delivery pattern.
18. BACKEND FILE READ: src/ccp/services/conversion_sequence_router.py. Verified method: `ConversionSequenceRouter.route(...) -> ConversionSequencePayloadRow`. Confirmed failure-closed dormancy gate with FAIL_DORMANT_ABORT and PROVISIONAL states.
19. PRIMITIVE YAMLs VERIFIED:
    - PRM-PRS-001 = "Strong Title as Idea Architecture" (meaning/persuasion)
    - PRM-PRS-002 = "Tension-and-Release Narrative Engine" (meaning/persuasion)
    - EXP-FBK-001 = "RIM Feedback Discipline" (experience/feedback_scoring)
    - EXP-TRS-003 = "Reflective Social Proof (The Status Share)" (experience/trust_branding)
    Confirmed: these artifacts expose real persuasion, trust, memorability, and tension mechanics the evaluator must be able to score.
20. TEST FILES READ:
    - tests/integration/test_era3_fr22_directional_integrity_engine.py: Confirmed typed request/report contract tests, dimension-isolation tests, fallback tests, surface-policy override tests, and audit trail tests. This test pattern is the model for FR-ERA3-27 integration tests.
    - tests/integration/test_vis07_format_constraint.py: Confirmed deterministic registry completeness, envelope sealing, safety-failure assertions, and receipt chain integration. Confirmed the local style for failure-closed gates and traceable audit outputs.
21. DISTINCTION CONFIRMED:
    - Semantic Validity = does the output preserve existential invariants and representation geometry? (FR-ERA3-22)
    - Perceptual Potency = does the output actually create cognitive imprint, symbolic density, human congruence, and memorability pressure? (FR-ERA3-27)
    - Commercial Alignment = does the influence stack match the brand posture, surface, and offer without creating false depth or synthetic authority? (FR-ERA3-27 influence alignment)
    This spec must not collapse those roles.
```

---

## 1. Files Read

| # | File | Purpose |
|---|------|---------|
| 1 | `docs/architecture/april_updates/spec_prompts/P6_S51_FR-ERA3-27_Perceptual_Influence_Evaluator.md` | Prompt source, scope boundary, and mandatory source set |
| 2 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Spec-writing protocol and mandatory format |
| 3 | `docs/prd/modules/PRD_02_CCF_Content_Factory.md` | Runtime law and compiler pipeline placement |
| 4 | `docs/prd/modules/PRD_03_CMF_Media_Factory.md` | Render-preservation and perceptual-collapse risk |
| 5 | `docs/prd/modules/PRD_05_CBCS_Law28.md` | Coaching intervention perceptual quality requirements |
| 6 | `docs/prd/modules/PRD_06_Conscious_Reactions.md` | Human-first doctrine and human congruence mandate |
| 7 | `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md` | Commercial trust transfer and false-depth risk |
| 8 | `lab/subliminal_function_layer_for_ccp_v_1.md` | SFL doctrine, artifact taxonomy, and metric ownership |
| 9 | `lab/Subliminal Functions for Agentic Content Architecture.md` | 120-association function framing |
| 10 | `lab/120 subliminal associations Chat.md` | Adaptive-vitality framing and paradox language |
| 11 | `lab/semantic_discernment_architecture_content_engine_v_1.md` | Deep semantic truth layer and deceptively-close failure |
| 12 | `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md` | Artifact taxonomy and role-before-schema law |
| 13 | `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md` | Primitive/edge separation and coalition sequence |
| 14 | `docs/architecture/april_updates/FR-ERA3-22_Directional_Integrity_Engine_Tech_Spec.md` | DI engine contract, dimensions, and interop boundary |
| 15 | `docs/architecture/april_updates/FR-ERA3-25_Subliminal_Function_Library_And_Taxonomy_Tech_Spec.md` | SFL canonical substrate and metric ownership delegation |
| 16 | `src/ccp/services/trait_scoring_engine.py` | Evidence-backed scoring precedent |
| 17 | `src/ccp/services/semantic_affinity_guard.py` | Typed gate decisions and fallback precedent |
| 18 | `src/ccp/services/content_machine.py` | Multi-stage pipeline and validation staging precedent |
| 19 | `src/ccp/services/conversion_sequence_router.py` | Failure-closed commercial gating precedent |
| 20 | `primitives/meaning/persuasion/PRM-PRS-001.yaml` | Real persuasion primitive and goal_bias structure |
| 21 | `primitives/meaning/persuasion/PRM-PRS-002.yaml` | Real tension/release primitive and crosswalk reference |
| 22 | `primitives/experience/feedback_scoring/EXP-FBK-001.yaml` | Real feedback primitive and experience metrics |
| 23 | `primitives/experience/trust_branding/EXP-TRS-003.yaml` | Real social proof primitive and status share mechanics |
| 24 | `tests/integration/test_era3_fr22_directional_integrity_engine.py` | DI engine test pattern for typed contracts and fallbacks |
| 25 | `tests/integration/test_vis07_format_constraint.py` | Deterministic registry and safety-failure test pattern |

---

## 2. Overview

### 2.1 Problem Statement — What breaks without this spec?

The canonical runtime law in PRD-02 §3.4A explicitly names `perceptual influence validation` as a required stage after directional integrity validation and before JIT script contract emission. Without `FR-ERA3-27`:

- **PRD-02 is incomplete in practice.** The runtime law names perceptual influence validation, but no executable evaluator exists to perform it. The system can produce semantically valid output that feels dead, flat, or synthetically smooth.
- **False depth ships undetected.** A carousel, proof card, or webinar transition can be directionally coherent (FR-ERA3-22 passes) while offering zero genuine cognitive imprint — performative profundity without real symbolic weight.
- **Dead polish replaces aliveness.** Output that passes semantic validation can still feel over-resolved, over-explained, and robbed of the tension, mystery, and compression that make human communication memorable.
- **Synthetic smoothness goes unmeasured.** AI-generated content tends toward a uniform texture that lacks the asymmetry, pause weight, and imperfection of authentic human expression. Without a dedicated metric, this failure class has no gate.
- **Human congruence is assumed, not scored.** The system has no way to distinguish genuinely human-feeling output from well-polished synthetic prose that happens to align semantically.
- **SFL metrics have no runtime home.** FR-ERA3-25 explicitly delegates `cognitive_imprint_score`, `symbolic_density_score`, and related metrics to FR-ERA3-27. Without this spec, those metrics remain conceptual.
- **Commercial surfaces lack perceptual governance.** A referral card or authority proof stack can pass DI validation while being perceptually flat, unmemorable, or subtly false-deep. No gate exists to catch this.
- **FR-ERA3-22 interop is undefined.** The boundary between semantic direction validation and perceptual potency evaluation remains architectural prose rather than typed contract.

### 2.2 Solution

Create a new service, `PerceptualInfluenceEvaluator`, that scores candidate artifacts on seven mandatory perceptual dimensions and returns a typed, evidence-backed decision:

- `PASS` = perceptual potency and influence alignment are sufficient for the target surface
- `REVIEW` = ambiguity or moderate weakness exists; safe continuation depends on surface risk
- `DOWNGRADE` = perceptual evidence is insufficient, contradictory, or missing; the artifact should not proceed without remediation

The evaluator will:

- consume canonical SFL function taxonomy via `FR-ERA3-25`
- consume SFL runtime profiles via `FR-ERA3-26`
- accept `DirectionalIntegrityReport` from `FR-ERA3-22` as a prerequisite input (not re-evaluate it)
- score seven mandatory perceptual dimensions:
  - `cognitive_imprint_score`
  - `symbolic_density_score`
  - `human_congruence_score`
  - `contrast_clarity_score`
  - `memorability_pressure`
  - `overexplanation_risk_score`
  - `synthetic_smoothness_score`
- evaluate influence alignment against brand posture, representation geometry, content archetype, and commercial surface sensitivity
- preserve per-dimension evidence, not only scalars
- fail closed when SFL dependencies or perceptual evidence are missing
- interop with FR-ERA3-22 by consuming its report without duplicating its logic

### 2.3 Scope

**In scope**

- evaluator input contract and output report
- seven mandatory perceptual metric dimensions with score direction semantics
- pass/review/downgrade decision states
- influence alignment evaluation against brand, geometry, archetype, and surface
- false-depth, dead-polish, and synthetic-smoothness detection
- FR-ERA3-22 interop contract (consumes DI report, does not re-evaluate)
- failure-closed downgrade behavior when evidence is missing or contradictory
- surface-specific threshold profiles
- audit logging and integration test design

**Out of scope**

- authoring SFL function families or definitions (`FR-ERA3-25`)
- SFL query service or profile composition (`FR-ERA3-26`)
- adversarial perceptual failure corpus and contrast harness (`FR-ERA3-28`)
- semantic direction validation (`FR-ERA3-22`)
- SDA ontology or crosswalk maintenance (`FR-ERA3-20`, `FR-ERA3-21`)
- hard-negative corpus management (`FR-ERA3-24`)
- DSPy inference orchestration details
- UI surfacing of evaluator results

---

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Component | Source | What It Does |
|--------|-----------|--------|--------------|
| `DEP-SFL-027-01` | `PerceptualInfluenceEvaluator` | FR-ERA3-27 | Main orchestrator for perceptual potency and influence alignment evaluation |
| `DEP-SFL-027-02` | `CognitiveImprintAnalyzer` | FR-ERA3-27 | Scores whether the artifact creates lasting mental imprint vs forgettable smoothness |
| `DEP-SFL-027-03` | `SymbolicDensityAnalyzer` | FR-ERA3-27 | Scores ratio of high-weight symbolic elements to total content mass |
| `DEP-SFL-027-04` | `HumanCongruenceAnalyzer` | FR-ERA3-27 | Scores whether the artifact reads as authentically human vs synthetically assembled |
| `DEP-SFL-027-05` | `ContrastClarityAnalyzer` | FR-ERA3-27 | Scores whether contrast, juxtaposition, and tension structures are legible |
| `DEP-SFL-027-06` | `MemorabilityPressureAnalyzer` | FR-ERA3-27 | Scores compounding recall probability through hooks, rhythm, and signature |
| `DEP-SFL-027-07` | `OverexplanationRiskAnalyzer` | FR-ERA3-27 | Scores whether the artifact over-resolves tension or over-explains the point |
| `DEP-SFL-027-08` | `SyntheticSmoothnessAnalyzer` | FR-ERA3-27 | Scores whether the artifact exhibits uniform AI texture lacking human asymmetry |
| `DEP-SFL-027-09` | `InfluenceAlignmentAnalyzer` | FR-ERA3-27 | Scores whether active SFL functions match brand posture, geometry, and surface |
| `DEP-SFL-027-10` | `PerceptualInfluenceDecisionRouter` | FR-ERA3-27 | Maps dimensional evidence to PASS, REVIEW, or DOWNGRADE |
| `DEP-SFL-027-11` | `PerceptualInfluenceReport` | FR-ERA3-27 | Runtime packet carrying evaluator results downstream |
| `DEP-SFL-027-12` | `PerceptualInfluenceRequest` | FR-ERA3-27 | Incoming evaluation request aggregating candidate context |
| `DEP-SFL-027-13` | `PerceptualInfluencePolicyBundle` | FR-ERA3-27 | Surface-specific threshold and constraint configuration |
| `DEP-SFL-027-14` | `FalseDepthDetectionResult` | FR-ERA3-27 | Sub-report for false-depth and dead-polish detection |

### 3.2 Why This Evaluator Exists in the SFL Stack

This evaluator sits after directional integrity validation and before JIT script contract emission.

Target runtime stack:

```text
signal
-> coach reaction / source artifact
-> invariant field
-> primitive coalition
-> edge product
-> archetypal geometry check
-> archetype container
-> subliminal function stack selection
-> composition depth profile
-> variation profile
-> directional integrity validation    <-- FR-ERA3-22
-> perceptual influence validation     <-- FR-ERA3-27
-> JIT script contract / render blueprint
```

This placement follows the SFL doctrine:

- SFL §1 defines the central law: "SDA protects semantic truthfulness. SFL shapes perceptual potency and symbolic aliveness."
- SFL §6.4 defines `Perceptual Effect Metric` as a distinct artifact class from function definitions
- FR-ERA3-25 §5 explicitly delegates metric scoring to FR-ERA3-27
- PRD-02 §3.4A names `perceptual influence validation` as a distinct runtime stage

So this evaluator must validate the **perceptual delivery quality** of an artifact that has already passed semantic direction validation. It does not re-evaluate semantic coherence.

### 3.3 Existing Backend Integration

| File | Path | How This Spec Uses It |
|------|------|-----------------------|
| `trait_scoring_engine.py` | `src/ccp/services/trait_scoring_engine.py` | Evidence-backed per-dimension scoring style precedent. PI dimensions should emit cited evidence and rationale, not only scalars. |
| `semantic_affinity_guard.py` | `src/ccp/services/semantic_affinity_guard.py` | Typed gate decisions (PASS/OPERATOR_REVIEW/FAIL_TERMINAL), NLP-crash fallback to PROVISIONAL_MEDIUM, ghost-variable prevention. |
| `content_machine.py` | `src/ccp/services/content_machine.py` | Multi-stage extraction/evaluation/validation pipeline precedent. PI evaluation should follow the same staged pattern. |
| `conversion_sequence_router.py` | `src/ccp/services/conversion_sequence_router.py` | Failure-closed commercial gate precedent with explicit block-or-pivot behavior. |
| `directional_integrity_engine.py` | `src/ccp/services/directional_integrity_engine.py` | Primary interop target. PI evaluator consumes `DirectionalIntegrityEngineResult` and attaches the DI report as prerequisite context. |

### 3.4 SFL Governance Constraints

| Constraint | Origin | Implementation Mechanism |
|---|---|---|
| Anti-Centroid Law preservation | PRD-08 + SFL doctrine | Evaluator must score whether output has been flattened into safe averages; `synthetic_smoothness_score` and `contrast_clarity_score` detect centroid collapse |
| Direction-before-polish rule | SFL doctrine §2.3 | Evaluator must not upgrade an artifact that lacks DI clearance; `DirectionalIntegrityReport` is a required prerequisite input |
| Human-congruence priority | PRD-06 + SFL doctrine | `human_congruence_score` is a mandatory first-class dimension, not an optional annotation |
| False-depth rejection | SFL doctrine §6.6 | Evaluator must detect and reject false depth, dead polish, and performative profundity as distinct failure classes |
| Failure-closed evaluator discipline | SFL doctrine + existing gate patterns | Missing SFL evidence, missing DI prerequisite, or contradictory metric signals must cause DOWNGRADE on high-risk surfaces, not silent PASS |
| Metric-vs-Function separation | FR-ERA3-25 §5 notes | Evaluator metrics are runtime scoring artifacts owned by FR-ERA3-27; they must not be stored as canonical function definitions in FR-ERA3-25 |

### 3.5 Technical Decisions

| Decision | Rationale | Alternative Rejected | Why Rejected |
|----------|-----------|----------------------|--------------|
| Make PI a separate evaluator, not extend FR-ERA3-22 | Perceptual potency is categorically different from semantic direction; mixing them creates a monolithic god-validator | Add PI dimensions to DI engine | Conflates semantic truthfulness with perceptual aliveness and violates SFL/SDA separation law |
| Use PASS / REVIEW / DOWNGRADE states | Matches existing gate style but uses DOWNGRADE instead of FAIL because PI weakness is remediable, not terminal | Binary pass/fail | Too coarse for perceptual ambiguity; also distinguishes from DI's harder FAIL semantics |
| Accept DI report as prerequisite, not re-evaluate | FR-ERA3-22 already validated semantic direction; duplication wastes compute and creates conflicting verdicts | Re-run DI checks inside PI | Violates single-responsibility and creates maintenance coupling |
| Preserve evidence per metric dimension | Mirrors `TraitScoringEngine` and supports auditability | Emit only summary scores | Impossible to debug or improve without evidence |
| Score false depth and synthetic smoothness as explicit negative dimensions | SFL doctrine §6.6 treats these as distinct adversarial failure targets | Treat as absence of positive metrics | Missing a specific detection layer allows polished-but-dead content to score well on positive dimensions |
| Fail closed on missing SFL dependencies for high-risk surfaces | Directly required by SFL governance and PRD-09 commercial doctrine | Soft-pass on missing SFL data | Would allow commercial or public surfaces to ship without perceptual evaluation |

---

## 4. Implementation Plan

### Phase A: Models and Policy Contracts

- [ ] **Task 1:** Create `src/ccp/models/perceptual_influence_models.py` with request, evidence, metric, decision, report, and policy models.
- [ ] **Task 2:** Define enums for `PerceptualInfluenceDecision`, `PerceptualInfluenceSurface`, `PerceptualInfluenceSeverity`, `PerceptualInfluenceFallbackReason`, `PerceptualInfluenceResolutionPath`, and `PerceptualInfluenceDimension`.
- [ ] **Task 3:** Add constants for default thresholds and surface-policy profiles.

### Phase B: Core Analyzer Services

- [ ] **Task 4:** Create `src/ccp/services/perceptual_influence_evaluator.py` with `PerceptualInfluenceEvaluator`.
- [ ] **Task 5:** Implement `CognitiveImprintAnalyzer`. Must evaluate whether the artifact creates a lasting mental model, an identifiable anchor, or a portable concept vs forgettable generic phrasing.
- [ ] **Task 6:** Implement `SymbolicDensityAnalyzer`. Must calculate the ratio of high-gravity symbolic elements (metaphors, identity markers, compressed meaning) to total token mass.
- [ ] **Task 7:** Implement `HumanCongruenceAnalyzer`. Must detect markers of authentic human expression (asymmetry, imperfection, personal specificity, lived rhythm) vs synthetic uniformity.
- [ ] **Task 8:** Implement `ContrastClarityAnalyzer`. Must score whether tension structures, juxtapositions, and contrast pairs are legible and unresolved where intended.
- [ ] **Task 9:** Implement `MemorabilityPressureAnalyzer`. Must score compounding recall probability through hooks, verbal anchors, rhythm signatures, and pattern recognition triggers.
- [ ] **Task 10:** Implement `OverexplanationRiskAnalyzer`. Must detect whether the artifact over-resolves tension, over-explains the core insight, or eliminates productive ambiguity.
- [ ] **Task 11:** Implement `SyntheticSmoothnessAnalyzer`. Must detect uniform AI texture: consistent sentence length, predictable transitions, absence of pause weight, missing idiosyncratic markers.
- [ ] **Task 12:** Implement `InfluenceAlignmentAnalyzer`. Must check active SFL function stack against brand posture constraints, representation geometry, archetype expectations, and surface sensitivity.
- [ ] **Task 13:** Implement `FalseDepthDetector`. Sub-analyzer that specifically flags performative profundity, dead polish, and empty motivational smoothness.
- [ ] **Task 14:** Implement `PerceptualInfluenceDecisionRouter` that maps dimensional evidence to `PASS`, `REVIEW`, `DOWNGRADE`.

### Phase C: Dependency Integration and Fallback

- [ ] **Task 15:** Integrate FR-ERA3-25 SFL registry service for function family and definition lookup.
- [ ] **Task 16:** Integrate FR-ERA3-26 SFL query/profile service for runtime function stack and profile resolution.
- [ ] **Task 17:** Integrate FR-ERA3-22 DI report consumption as prerequisite context.
- [ ] **Task 18:** Create `PerceptualInfluencePolicyRegistry` loaded from typed Python config or YAML.
- [ ] **Task 19:** Add failure-closed behavior for: missing SFL registry, missing DI prerequisite, missing function stack, null candidate text, contradictory metric signals.
- [ ] **Task 20:** Add receipt-chain logging for all evaluation stages.

### Phase D: Integration SDKs

- [ ] **Task 21:** Build `PIEvaluatorClient` SDK for upstream semantic planning execution boundaries.
- [ ] **Task 22:** Build `PIRenderGuard` SDK for media generation execution boundaries.
- [ ] **Task 23:** Build surface-class helper functions mapping commercial, coaching, social, and authority surfaces to standard evaluation payloads.
- [ ] **Task 24:** Add operator-facing remediation payloads describing which dimension failed and what must be corrected.

### Phase E: Test and Audit Hardening

- [ ] **Task 25:** Create `tests/integration/test_era3_fr27_perceptual_influence_evaluator.py`.
- [ ] **Task 26:** Create `tests/integration/test_era3_fr27_perceptual_influence_fallbacks.py`.
- [ ] **Task 27:** Create fixture policies, fixture SFL stacks, and fixture DI reports.
- [ ] **Task 28:** Add representative negative cases for: false depth, dead polish, synthetic smoothness, over-explanation, and misaligned influence.

---

## 5. Data Contracts and Pydantic Models

### 5.1 Enumerations

```python
from enum import Enum

class PerceptualInfluenceDecision(str, Enum):
    PASS = "PASS"
    REVIEW = "REVIEW"
    DOWNGRADE = "DOWNGRADE"

class PerceptualInfluenceSurface(str, Enum):
    SEMANTIC_PLANNING = "SEMANTIC_PLANNING"
    RENDER_RELEASE = "RENDER_RELEASE"
    COMMERCIAL_TRUST_TRANSFER = "COMMERCIAL_TRUST_TRANSFER"
    SOCIAL_SHARE = "SOCIAL_SHARE"
    COACHING_INTERVENTION = "COACHING_INTERVENTION"
    INTERNAL_REVIEW = "INTERNAL_REVIEW"

class PerceptualInfluenceDomain(str, Enum):
    CCF = "CCF"
    CMF = "CMF"
    CBCS = "CBCS"
    REACTIONS = "REACTIONS"
    COMMERCIAL = "COMMERCIAL"
    WEBINAR = "WEBINAR"

class PerceptualInfluenceFallbackReason(str, Enum):
    MISSING_SFL_REGISTRY = "MISSING_SFL_REGISTRY"
    MISSING_DI_PREREQUISITE = "MISSING_DI_PREREQUISITE"
    MISSING_FUNCTION_STACK = "MISSING_FUNCTION_STACK"
    NULL_CANDIDATE = "NULL_CANDIDATE"
    CONTRADICTORY_METRICS = "CONTRADICTORY_METRICS"
    MISSING_POLICY = "MISSING_POLICY"
    MISSING_BRAND_POSTURE = "MISSING_BRAND_POSTURE"
    ANALYZER_CRASH = "ANALYZER_CRASH"

class PerceptualInfluenceResolutionPath(str, Enum):
    REGENERATE = "REGENERATE"
    OPERATOR_REVIEW = "OPERATOR_REVIEW"
    SURFACE_DOWNGRADE = "SURFACE_DOWNGRADE"
    ENRICH_SFL_STACK = "ENRICH_SFL_STACK"
    RESTORE_TENSION = "RESTORE_TENSION"

class PerceptualInfluenceDimension(str, Enum):
    COGNITIVE_IMPRINT = "COGNITIVE_IMPRINT"
    SYMBOLIC_DENSITY = "SYMBOLIC_DENSITY"
    HUMAN_CONGRUENCE = "HUMAN_CONGRUENCE"
    CONTRAST_CLARITY = "CONTRAST_CLARITY"
    MEMORABILITY_PRESSURE = "MEMORABILITY_PRESSURE"
    OVEREXPLANATION_RISK = "OVEREXPLANATION_RISK"
    SYNTHETIC_SMOOTHNESS = "SYNTHETIC_SMOOTHNESS"
    INFLUENCE_ALIGNMENT = "INFLUENCE_ALIGNMENT"

class PerceptualInfluenceSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"
    NONE = "NONE"

class FalseDepthClass(str, Enum):
    PERFORMATIVE_PROFUNDITY = "PERFORMATIVE_PROFUNDITY"
    DEAD_POLISH = "DEAD_POLISH"
    SYNTHETIC_AUTHORITY = "SYNTHETIC_AUTHORITY"
    EMPTY_MOTIVATIONAL_SMOOTHNESS = "EMPTY_MOTIVATIONAL_SMOOTHNESS"
    OVERRESOLVED_MEANING = "OVERRESOLVED_MEANING"
```

### 5.2 Evidence and Metric Models

```python
from pydantic import BaseModel, Field
from typing import Optional

class PerceptualEvidenceItem(BaseModel):
    evidence_id: str = Field(..., description="Unique ID for this evidence item")
    dimension: PerceptualInfluenceDimension
    observation: str = Field(..., description="What was observed in the candidate")
    rationale: str = Field(..., description="Why this observation matters for this dimension")
    contribution: float = Field(..., ge=-1.0, le=1.0, description="Signed contribution to dimension score")
    source_span: Optional[str] = Field(None, description="Text span or location in candidate that triggered this evidence")
    sfl_function_ref: Optional[str] = Field(None, description="SFL function ID if evidence relates to a specific function activation")

class PerceptualDimensionScore(BaseModel):
    dimension: PerceptualInfluenceDimension
    score: float = Field(..., ge=0.0, le=1.0, description="Normalized score for this dimension")
    severity: PerceptualInfluenceSeverity
    evidence: list[PerceptualEvidenceItem] = Field(default_factory=list, min_length=1)
    explanation: str = Field(..., description="Human-readable summary of the dimensional assessment")

    # Score direction semantics:
    # cognitive_imprint:      higher = more lasting imprint (good)
    # symbolic_density:       higher = more symbolic weight per unit (good)
    # human_congruence:       higher = more authentically human (good)
    # contrast_clarity:       higher = more legible contrast/tension (good)
    # memorability_pressure:  higher = more recall-forcing pressure (good)
    # overexplanation_risk:   higher = MORE over-explanation (bad)
    # synthetic_smoothness:   higher = MORE synthetic texture (bad)
    # influence_alignment:    higher = better brand/surface alignment (good)

class FalseDepthDetectionResult(BaseModel):
    detected: bool = Field(..., description="Whether any false-depth failure class was detected")
    detected_classes: list[FalseDepthClass] = Field(default_factory=list)
    evidence: list[PerceptualEvidenceItem] = Field(default_factory=list)
    severity: PerceptualInfluenceSeverity = PerceptualInfluenceSeverity.NONE
    explanation: str = ""
```

### 5.3 Influence Alignment Models

```python
class BrandPostureContext(BaseModel):
    brand_posture_id: str
    authority_source: str = Field(..., description="earned, institutional, experiential, etc.")
    belonging_mode: str = Field(..., description="invitational, tribal, aspirational, etc.")
    identity_frame: str = Field(..., description="sovereign, collaborative, etc.")
    forbidden_influence_patterns: list[str] = Field(default_factory=list)
    permitted_influence_families: list[str] = Field(default_factory=list)

class InfluenceAlignmentResult(BaseModel):
    aligned: bool
    alignment_score: float = Field(..., ge=0.0, le=1.0)
    brand_posture_match: bool
    representation_geometry_match: bool
    archetype_match: bool
    surface_sensitivity_match: bool
    misalignment_details: list[str] = Field(default_factory=list)
    evidence: list[PerceptualEvidenceItem] = Field(default_factory=list)
```

### 5.4 Request and Report Models

```python
from datetime import datetime

class SFLFunctionStackSnapshot(BaseModel):
    stack_id: str
    active_families: list[str]
    active_functions: list[str]
    weight_profile: dict[str, float] = Field(default_factory=dict)
    intended_effects: list[str] = Field(default_factory=list)

class PerceptualInfluenceRequest(BaseModel):
    request_id: str
    domain: PerceptualInfluenceDomain
    surface_class: PerceptualInfluenceSurface
    actor_id: str
    coach_id: str
    candidate_text: str = Field(..., min_length=1, description="The artifact text to evaluate")
    sfl_function_stack: Optional[SFLFunctionStackSnapshot] = None
    brand_posture: Optional[BrandPostureContext] = None
    content_archetype_id: Optional[str] = None
    representation_geometry_id: Optional[str] = None
    directional_integrity_report_id: Optional[str] = Field(None, description="ID of the prerequisite DI report from FR-ERA3-22")
    directional_integrity_decision: Optional[str] = Field(None, description="DI decision: PASS, REVIEW, or FAIL")
    coalition_signature_id: Optional[str] = None
    edge_product_id: Optional[str] = None

class PerceptualInfluenceDecisionSummary(BaseModel):
    decision: PerceptualInfluenceDecision
    resolution_path: Optional[PerceptualInfluenceResolutionPath] = None
    required_corrections: list[str] = Field(default_factory=list)
    rationale: str = ""

class PerceptualInfluenceMetricBundle(BaseModel):
    cognitive_imprint_score: PerceptualDimensionScore
    symbolic_density_score: PerceptualDimensionScore
    human_congruence_score: PerceptualDimensionScore
    contrast_clarity_score: PerceptualDimensionScore
    memorability_pressure: PerceptualDimensionScore
    overexplanation_risk_score: PerceptualDimensionScore
    synthetic_smoothness_score: PerceptualDimensionScore

class PerceptualInfluenceReport(BaseModel):
    report_id: str = Field(..., description="Unique report ID, prefixed PIR-")
    request_id: str
    metric_bundle: PerceptualInfluenceMetricBundle
    influence_alignment: InfluenceAlignmentResult
    false_depth_result: FalseDepthDetectionResult
    decision_summary: PerceptualInfluenceDecisionSummary
    fallback_reason: Optional[PerceptualInfluenceFallbackReason] = None
    policy_id: str = Field(default="NONE", description="ID of the surface policy applied")
    di_prerequisite_report_id: Optional[str] = None
    di_prerequisite_decision: Optional[str] = None
    lineage_refs: list[str] = Field(default_factory=list, description="IDs of consumed artifacts: SFL stack, DI report, coalition, etc.")
    evaluated_at_utc: datetime = Field(default_factory=datetime.utcnow)

class PerceptualInfluenceEvaluatorResult(BaseModel):
    report: PerceptualInfluenceReport
    receipt_ids: list[str] = Field(default_factory=list)
```

### 5.5 Policy Bundle Model

```python
class PerceptualInfluencePolicyBundle(BaseModel):
    policy_id: str
    domain: PerceptualInfluenceDomain
    surface_class: PerceptualInfluenceSurface
    pass_thresholds: dict[str, float] = Field(
        ...,
        description="Minimum positive-dimension scores for PASS. Keys are dimension names."
    )
    risk_ceilings: dict[str, float] = Field(
        ...,
        description="Maximum negative-dimension scores for PASS. Keys: overexplanation_risk, synthetic_smoothness."
    )
    influence_alignment_required: bool = True
    false_depth_blocks: bool = True
    missing_sfl_behavior: PerceptualInfluenceDecision = PerceptualInfluenceDecision.DOWNGRADE
    missing_di_behavior: PerceptualInfluenceDecision = PerceptualInfluenceDecision.DOWNGRADE
    notes: str = ""
```

### 5.6 Default Surface Policy Profiles

| Surface | `cognitive_imprint` min | `symbolic_density` min | `human_congruence` min | `contrast_clarity` min | `memorability_pressure` min | `overexplanation_risk` max | `synthetic_smoothness` max | `influence_alignment` required | `false_depth` blocks | Missing SFL | Missing DI |
|---------|----|----|----|----|----|----|----|----|----|----|-----|
| `SEMANTIC_PLANNING` | 0.40 | 0.35 | 0.45 | 0.35 | 0.35 | 0.65 | 0.60 | yes | yes | REVIEW | REVIEW |
| `RENDER_RELEASE` | 0.55 | 0.50 | 0.60 | 0.50 | 0.50 | 0.50 | 0.45 | yes | yes | DOWNGRADE | DOWNGRADE |
| `COMMERCIAL_TRUST_TRANSFER` | 0.65 | 0.55 | 0.70 | 0.55 | 0.55 | 0.40 | 0.35 | yes | yes | DOWNGRADE | DOWNGRADE |
| `SOCIAL_SHARE` | 0.60 | 0.50 | 0.65 | 0.50 | 0.60 | 0.45 | 0.40 | yes | yes | DOWNGRADE | DOWNGRADE |
| `COACHING_INTERVENTION` | 0.50 | 0.40 | 0.70 | 0.45 | 0.40 | 0.50 | 0.40 | yes | yes | REVIEW | REVIEW |
| `INTERNAL_REVIEW` | 0.30 | 0.25 | 0.35 | 0.25 | 0.25 | 0.75 | 0.70 | no | no | REVIEW | REVIEW |

---

## 6. FR-ERA3-22 Interop Boundary

### 6.1 The Non-Duplication Rule

FR-ERA3-22 (Directional Integrity Engine) validates **semantic direction**. It scores:

- `invariant_preservation_score` — does the artifact preserve existential invariants?
- `representation_drift_score` — does the artifact drift from declared representation geometry?
- `hard_negative_adjacency_score` — is the artifact deceptively close to known manipulative templates?
- `trajectory_risk_score` — does the artifact create dependency or coercive trajectory risk?

FR-ERA3-27 must **not** re-evaluate these four dimensions.

Instead, FR-ERA3-27 consumes the DI report as a prerequisite input and evaluates a **different question**: given that the semantic direction has been validated (or flagged), how perceptually alive, symbolically dense, humanly congruent, and memorably compelling is the delivery?

### 6.2 Interop Contract

```python
# FR-ERA3-27 CONSUMES FR-ERA3-22 output:
class DIPrerequisiteContext(BaseModel):
    di_report_id: str
    di_decision: str  # "PASS", "REVIEW", or "FAIL"
    invariant_preservation_score: float
    representation_drift_score: float
    hard_negative_adjacency_score: float
    trajectory_risk_score: float
```

**Rules:**

1. If `di_decision == "FAIL"`, the PI evaluator must **not override**. The PI evaluator should still run (to provide diagnostic data), but its decision cannot upgrade the overall pipeline verdict from FAIL to PASS.
2. If `di_decision == "REVIEW"`, the PI evaluator's result is advisory. Both reports travel downstream together.
3. If `di_decision == "PASS"`, the PI evaluator's verdict becomes the determining gate.
4. If no DI report is provided and the surface is `RENDER_RELEASE`, `COMMERCIAL_TRUST_TRANSFER`, or `SOCIAL_SHARE`, the PI evaluator must return `DOWNGRADE` with `fallback_reason = MISSING_DI_PREREQUISITE`.
5. If no DI report is provided and the surface is `SEMANTIC_PLANNING` or `INTERNAL_REVIEW`, the PI evaluator must return `REVIEW` with a warning.

### 6.3 What FR-ERA3-27 Adds That FR-ERA3-22 Cannot

| Capability | FR-ERA3-22 | FR-ERA3-27 |
|---|---|---|
| Detect invariant corruption | ✅ | ❌ (consumes DI verdict) |
| Detect representation drift | ✅ | ❌ |
| Detect hard-negative adjacency | ✅ | ❌ |
| Detect trajectory risk | ✅ | ❌ |
| Score cognitive imprint | ❌ | ✅ |
| Score symbolic density | ❌ | ✅ |
| Score human congruence | ❌ | ✅ |
| Score contrast clarity | ❌ | ✅ |
| Score memorability pressure | ❌ | ✅ |
| Detect over-explanation | ❌ | ✅ |
| Detect synthetic smoothness | ❌ | ✅ |
| Detect false depth / dead polish | ❌ | ✅ |
| Evaluate influence alignment | ❌ | ✅ |

### 6.4 Combined Pipeline Verdict Logic

```text
DI = FAIL  → pipeline = FAIL (PI runs for diagnostics only)
DI = REVIEW, PI = DOWNGRADE → pipeline = FAIL
DI = REVIEW, PI = REVIEW   → pipeline = REVIEW (both reports travel)
DI = REVIEW, PI = PASS     → pipeline = REVIEW (DI ambiguity dominates)
DI = PASS,  PI = DOWNGRADE → pipeline = DOWNGRADE
DI = PASS,  PI = REVIEW    → pipeline = REVIEW
DI = PASS,  PI = PASS      → pipeline = PASS
```

---

## 7. CBAR Mandate Enforcement

### 7.1 Anti-Centroid Law

| What | How | Metric |
|------|-----|--------|
| Detect centroid collapse | `contrast_clarity_score` drops when juxtaposition is absent and positions are averaged | `contrast_clarity_score < pass_threshold` |
| Detect uniformity flattening | `synthetic_smoothness_score` rises when sentence length variance, transition variety, and asymmetry drop below human baselines | `synthetic_smoothness_score > risk_ceiling` |
| Prevent safe-average outputs | `cognitive_imprint_score` requires at least one identifiable anchor concept, not generic well-phrased generality | `cognitive_imprint_score < pass_threshold` |

### 7.2 Direction-Before-Polish Rule

| What | How |
|------|-----|
| Require DI prerequisite before final verdict | PI evaluator checks `di_prerequisite_report_id` presence and `di_prerequisite_decision` value |
| Never upgrade from DI FAIL | Combined verdict logic (§6.4) guarantees FAIL propagation |
| Flag polish without direction | If DI is REVIEW but all PI positive dimensions are high, flag as "polish-without-direction-clarity" advisory |

### 7.3 Human-Congruence Priority

| What | How |
|------|-----|
| First-class dimension | `human_congruence_score` is a mandatory metric dimension, not derived from other scores |
| Dedicated analyzer | `HumanCongruenceAnalyzer` runs as its own pass, looking for asymmetry markers, personal specificity, lived rhythm, and verbal imperfection signals |
| High threshold on public surfaces | `COMMERCIAL_TRUST_TRANSFER` and `SOCIAL_SHARE` require `human_congruence_score >= 0.65-0.70` |

### 7.4 False-Depth Rejection

| What | How |
|------|-----|
| Dedicated detection | `FalseDepthDetector` classifies five failure types: performative profundity, dead polish, synthetic authority, empty motivational smoothness, overresolved meaning |
| Blocking on high-risk surfaces | When `false_depth_result.detected == True` and `false_depth_result.severity >= HIGH`, decision is DOWNGRADE on commercial/social surfaces |
| Evidence-backed | Each detected class must carry at least one `PerceptualEvidenceItem` pointing to the offending text span |

### 7.5 Failure-Closed Evaluator Discipline

| Missing Dependency | Low-Risk Surface (SEMANTIC_PLANNING, INTERNAL_REVIEW) | High-Risk Surface (All Others) |
|---|---|---|
| SFL function stack | `REVIEW` + warning | `DOWNGRADE` |
| DI prerequisite | `REVIEW` + warning | `DOWNGRADE` |
| Brand posture context | `REVIEW` + warning | `DOWNGRADE` |
| SFL registry service | `REVIEW` + warning | `DOWNGRADE` |
| Policy bundle | `REVIEW` + default policy | `DOWNGRADE` |
| Null candidate text | `DOWNGRADE` | `DOWNGRADE` |
| Analyzer crash | `REVIEW` + partial report | `DOWNGRADE` |
| Contradictory metrics | `REVIEW` + investigation flag | `REVIEW` + investigation flag |

---

## 8. Backend Integration Plan

### 8.1 New Files

| File | Purpose |
|------|---------|
| `src/ccp/models/perceptual_influence_models.py` | All Pydantic models, enums, and constants from §5 |
| `src/ccp/services/perceptual_influence_evaluator.py` | Main evaluator orchestrator with four-pass scoring logic |
| `src/ccp/services/perceptual_influence_policy_registry.py` | Surface-policy resolution and threshold lookup |

### 8.2 Modified Files

| File | Change |
|------|--------|
| `src/ccp/services/content_machine.py` | Add PI evaluation stage after DI validation in `ContentMachinePipeline.process_session()`. Insert between existing DI validation call and JIT contract emission. The PI evaluator receives the DI report plus the current candidate text and SFL function stack snapshot. |
| `src/ccp/services/directional_integrity_engine.py` | No code change. FR-ERA3-27 consumes its output type `DirectionalIntegrityEngineResult`. Confirm export compatibility only. |
| `src/ccp/core/receipt_chain.py` | No structural change. PI evaluator will call existing `ReceiptChain.write()` method with PI-specific action tags: `PI27_PREREQUISITE_CHECK`, `PI27_METRIC_SCORING`, `PI27_INFLUENCE_ALIGNMENT`, `PI27_FALSE_DEPTH_DETECTION`, `PI27_DECISION_ROUTING`. |

### 8.3 Four-Pass Scoring Architecture

The evaluator executes four sequential passes:

**Pass 1: Prerequisite Validation**
- Check for null candidate text → immediate DOWNGRADE
- Resolve DI prerequisite: verify `directional_integrity_report_id` and `directional_integrity_decision`
- Resolve SFL function stack: verify `sfl_function_stack` presence
- Resolve brand posture: verify `brand_posture` presence
- Resolve surface policy: look up `PerceptualInfluencePolicyBundle` for domain + surface
- If any prerequisite is missing, apply failure-closed behavior per §7.5

**Pass 2: Dimensional Metric Scoring**
- Run all seven analyzers independently on the candidate text
- Each analyzer emits a `PerceptualDimensionScore` with evidence items
- Assemble `PerceptualInfluenceMetricBundle`
- Run `FalseDepthDetector` across the candidate and metric results
- Receipt: `PI27_METRIC_SCORING`

**Pass 3: Influence Alignment Evaluation**
- Run `InfluenceAlignmentAnalyzer` using SFL function stack, brand posture, representation geometry, and content archetype context
- Emit `InfluenceAlignmentResult`
- Receipt: `PI27_INFLUENCE_ALIGNMENT`

**Pass 4: Decision Routing**
- Feed metric bundle, influence alignment, false depth result, and policy thresholds to `PerceptualInfluenceDecisionRouter`
- Apply combined DI + PI verdict logic (§6.4)
- Emit final `PerceptualInfluenceReport`
- Receipt: `PI27_DECISION_ROUTING`

### 8.4 Service Method Signature

```python
class PerceptualInfluenceEvaluator:
    def __init__(
        self,
        policy_registry: PerceptualInfluencePolicyRegistry | None = None,
        sfl_registry: SFLRegistryService | None = None,
        receipt_chain: ReceiptChain | None = None,
    ):
        ...

    def evaluate(
        self,
        request: PerceptualInfluenceRequest,
    ) -> PerceptualInfluenceEvaluatorResult:
        """
        Four-pass perceptual influence evaluation.
        Returns typed report with per-dimension evidence,
        influence alignment result, false-depth detection,
        and PASS/REVIEW/DOWNGRADE decision.
        Fails closed on missing dependencies per surface policy.
        """
        ...
```

### 8.5 ContentMachinePipeline Integration Point

```python
# In content_machine.py, after directional integrity validation:

# Existing:
di_result = self.di_engine.evaluate(di_request)

# New addition:
pi_request = PerceptualInfluenceRequest(
    request_id=f"PIR-{session_id}",
    domain=PerceptualInfluenceDomain.CCF,
    surface_class=PerceptualInfluenceSurface.SEMANTIC_PLANNING,
    actor_id=actor_id,
    coach_id=coach_id,
    candidate_text=compiled_script_text,
    sfl_function_stack=current_sfl_stack,
    brand_posture=resolved_brand_posture,
    content_archetype_id=selected_archetype_id,
    representation_geometry_id=rep_geometry_id,
    directional_integrity_report_id=di_result.report.report_id,
    directional_integrity_decision=di_result.report.decision_summary.decision.value,
    coalition_signature_id=coalition_id,
    edge_product_id=edge_product_id,
)
pi_result = self.pi_evaluator.evaluate(pi_request)

# Combined verdict:
pipeline_verdict = _combine_di_pi_verdict(
    di_result.report.decision_summary.decision,
    pi_result.report.decision_summary.decision,
)
```

### 8.6 Receipt Chain Actions

| Action Tag | Trigger | Payload Contents |
|---|---|---|
| `PI27_PREREQUISITE_CHECK` | After Pass 1 | Missing dependencies, resolved policy ID, DI prerequisite status |
| `PI27_METRIC_SCORING` | After Pass 2 | Seven dimension scores (scalar only), false-depth detection flag |
| `PI27_INFLUENCE_ALIGNMENT` | After Pass 3 | Alignment score, brand match, geometry match, archetype match |
| `PI27_DECISION_ROUTING` | After Pass 4 | Final decision, resolution path, policy ID, combined verdict |
| `PI27_FALLBACK_TRIGGERED` | On any fallback | Fallback reason, surface class, missing dependency details |

---

## 9. Future Couplings

### 9.1 FR-ERA3-28 — Perceptual Failure Corpus and Contrast Harness

When implemented, the PI evaluator should consume adversarial perceptual failure assets from FR-ERA3-28 to improve false-depth detection, dead-polish identification, and synthetic-smoothness scoring. The FalseDepthDetector should accept an optional `PerceptualFailureCorpus` input containing contrastive case pairs.

### 9.2 FR-ERA3-26 — SFL Profile Service

The PI evaluator currently accepts an `SFLFunctionStackSnapshot` in the request. When FR-ERA3-26 is fully implemented, the evaluator should resolve the function stack directly from the profile service rather than requiring it as an input parameter.

### 9.3 Longitudinal Perceptual Memory

SFL §6.8 defines `PerceptualEvolutionRecord`, `ImprintHistoryRecord`, and `AudienceFamiliarityTrace`. Future versions of the PI evaluator should read these records to calibrate scoring against the coach's perceptual evolution trajectory, enabling detection of regression patterns (e.g., a coach whose output is becoming progressively more synthetic over time).

### 9.4 Mini-App Surface Integration

When mini-app surfaces are implemented, the PI evaluator should expose a lightweight `PIRenderGuard` SDK that can be called from media release gates to prevent perceptually dead content from reaching social share or commercial trust transfer surfaces.

### 9.5 Domain Policy Expansion

| Domain | Target Spec | PI Role |
|--------|-------------|---------|
| CCF | `FR-ERA3-16` | Guards script compile progression |
| CMF | `FR-ERA3-12` | Guards render/export/share release |
| CBCS | `FR-ERA3-18` | Guards coaching intervention delivery |
| Reactions CORE | `FR-ERA3-05-CORE` | Guards reaction framing and social proof assets |
| Webinar | future update | Guards educational authority and CTA transitions |
| Silent Referral / OFO / Commercial | `FR-ERA3-03`, `FR-ERA3-04`, `FR-ERA3-14` | Guards trust-transfer and prestige integrity |
| Conscious Editor | `FR-ERA3-09` | Surfaces PI findings during review |

These future couplings must enrich the evaluator's policy substrate, not change the current role boundary.

---

## 10. Testing Strategy

### 10.1 Integration Test Files

Create:

- `tests/integration/test_era3_fr27_perceptual_influence_evaluator.py`
- `tests/integration/test_era3_fr27_perceptual_influence_fallbacks.py`
- `tests/integration/test_era3_fr27_perceptual_influence_surface_policies.py`

### 10.2 Required Test Classes

#### A. Contract Tests

- valid request returns typed `PerceptualInfluenceReport`
- report ID starts with `PIR-`
- all seven metric dimensions present in `metric_bundle`
- `influence_alignment` result always present
- `false_depth_result` always present
- `decision_summary` always present
- evidence arrays are non-empty for every dimension
- malformed request with empty candidate text returns DOWNGRADE before silent evaluation
- per-dimension evidence survives serialization round-trip

#### B. Dimension Tests

- `cognitive_imprint_score` drops when candidate contains only generic motivational phrasing with no identifiable anchor concept
- `symbolic_density_score` drops when candidate has high token count but no metaphors, identity markers, or compressed meaning
- `human_congruence_score` drops when candidate has uniform sentence length, predictable transitions, and no personal specificity
- `contrast_clarity_score` drops when candidate averages conflicting positions into polite compromise
- `memorability_pressure` drops when candidate lacks hooks, rhythm signatures, or pattern recognition triggers
- `overexplanation_risk_score` rises when candidate over-resolves tension or adds unnecessary explanation after the insight
- `synthetic_smoothness_score` rises when candidate exhibits uniform AI texture with consistent paragraph structure and missing pause weight

#### C. False-Depth Tests

- `PERFORMATIVE_PROFUNDITY` detected when candidate uses grand language ("transcend", "unlock your potential") with no specific evidence or grounding
- `DEAD_POLISH` detected when candidate is grammatically flawless and well-structured but carries zero emotional charge or surprise
- `SYNTHETIC_AUTHORITY` detected when candidate claims expertise through abstract framing without lived proof
- `EMPTY_MOTIVATIONAL_SMOOTHNESS` detected when candidate reads like generic coaching advice with interchangeable nouns
- `OVERRESOLVED_MEANING` detected when candidate eliminates all productive ambiguity and spells out every implication

#### D. Influence Alignment Tests

- aligned SFL function stack with matching brand posture returns `aligned = True`
- covert suggestion function active on a brand with `forbidden_influence_patterns = ["covert_suggestion"]` returns `aligned = False`
- mismatched authority source (e.g., institutional authority on a sovereign-identity brand) lowers alignment score
- commercial surface with aggressive persuasion functions and earned-authority brand flags misalignment

#### E. Fallback Tests

- missing SFL function stack on `RENDER_RELEASE` → `DOWNGRADE`
- missing SFL function stack on `SEMANTIC_PLANNING` → `REVIEW`
- missing DI prerequisite on `COMMERCIAL_TRUST_TRANSFER` → `DOWNGRADE`
- missing DI prerequisite on `INTERNAL_REVIEW` → `REVIEW`
- missing brand posture on `SOCIAL_SHARE` → `DOWNGRADE`
- missing policy for domain/surface → `DOWNGRADE` on high-risk, `REVIEW` on low-risk
- null candidate text → `DOWNGRADE` on all surfaces
- analyzer crash → `REVIEW` with partial report on low-risk, `DOWNGRADE` on high-risk

#### F. DI Interop Tests

- DI = FAIL → pipeline = FAIL regardless of PI outcome
- DI = REVIEW, PI = DOWNGRADE → pipeline = FAIL
- DI = REVIEW, PI = PASS → pipeline = REVIEW (DI ambiguity dominates)
- DI = PASS, PI = DOWNGRADE → pipeline = DOWNGRADE
- DI = PASS, PI = PASS → pipeline = PASS
- PI report always carries `di_prerequisite_report_id` and `di_prerequisite_decision`

#### G. Surface Policy Tests

- same candidate passes `INTERNAL_REVIEW` but fails `COMMERCIAL_TRUST_TRANSFER` due to stricter thresholds
- same candidate reviews in `COACHING_INTERVENTION` but downgrades in `SOCIAL_SHARE`
- commercial surface with detected false depth always downgrades

#### H. Audit Tests

- receipt chain contains five receipts for a full evaluation
- `PI27_FALLBACK_TRIGGERED` receipt emitted when any fallback fires
- report retains lineage refs to SFL stack, DI report, coalition signature, and edge product
- `required_corrections` populated on REVIEW and DOWNGRADE decisions

### 10.3 Seed Test Scenarios

At minimum include these fixtures:

1. **Healthy authority proof with perceptual aliveness**
   - candidate: earned authority content with specific examples, asymmetric phrasing, memorable hook
   - SFL stack: framing_and_contrast + identity_signaling
   - brand posture: earned authority + invitational belonging
   - DI prerequisite: PASS
   - expected: PI = `PASS`, all positive dimensions above thresholds, negative dimensions below ceilings

2. **Semantically valid but perceptually dead**
   - candidate: grammatically correct coaching advice with no hooks, no contrast, uniform sentence length
   - SFL stack: present but not reflected in output
   - DI prerequisite: PASS
   - expected: PI = `DOWNGRADE`, low cognitive_imprint, low memorability_pressure, high synthetic_smoothness

3. **False depth — performative profundity**
   - candidate: "Unlock the transcendent power of your authentic leadership potential to transform every dimension of your professional existence"
   - DI prerequisite: PASS (semantic direction is technically valid)
   - expected: PI = `DOWNGRADE`, `FalseDepthDetectionResult.detected = True`, `PERFORMATIVE_PROFUNDITY` class flagged

4. **Over-explained insight**
   - candidate: delivers the insight in sentence 1, then spends 5 paragraphs explaining why it matters, what it means, and how to apply it, eliminating all tension
   - DI prerequisite: PASS
   - expected: PI = `REVIEW`, high overexplanation_risk_score, low contrast_clarity_score

5. **Misaligned influence on commercial surface**
   - candidate: aggressive scarcity framing with countdown urgency and prestige theater
   - brand posture: earned authority + invitational belonging (not coercive)
   - SFL stack: suggestive_guidance + identity_signaling
   - surface: `COMMERCIAL_TRUST_TRANSFER`
   - expected: PI = `DOWNGRADE`, `influence_alignment.aligned = False`

6. **High-potency human-congruent content**
   - candidate: personal story with specific details, imperfect phrasing, strong tension-release structure, memorable verbal anchor
   - SFL stack: narrative_tension_preservation + symbolic_compression
   - DI prerequisite: PASS
   - expected: PI = `PASS`, high human_congruence, high cognitive_imprint, high memorability_pressure, low synthetic_smoothness

7. **Missing DI prerequisite on commercial surface**
   - candidate: any text
   - DI prerequisite: not provided
   - surface: `COMMERCIAL_TRUST_TRANSFER`
   - expected: PI = `DOWNGRADE`, fallback_reason = `MISSING_DI_PREREQUISITE`

8. **Synthetic smoothness detection**
   - candidate: 5 paragraphs of uniform 3-sentence structure, each starting with a transition word, each ending with a generic call-to-action, zero verbal imperfections
   - DI prerequisite: PASS
   - expected: PI = `REVIEW` or `DOWNGRADE`, high synthetic_smoothness_score

### 10.4 Manual Validation Checklist

- verify the evaluator never reports `PASS` with unresolved missing DI prerequisite on high-risk surfaces
- verify the evaluator never reports `PASS` when `false_depth_result.detected == True` and `severity >= HIGH` on commercial or social surfaces
- verify all `REVIEW` results include actionable `required_corrections` text
- verify all `DOWNGRADE` results include a `resolution_path`
- verify downstream adapters do not reinterpret `DOWNGRADE` as advisory
- verify the evaluator does not re-score any of the four FR-ERA3-22 dimensions (invariant preservation, representation drift, hard-negative adjacency, trajectory risk)
- verify the taxonomy distinction remains intact:
  - policy resolved from policy bundle
  - report emitted by evaluator
  - SFL functions consumed as composition inputs, not inlined prose rules
  - false-depth cases consumed as adversarial targets, not evaluator instructions

---

**End of Spec**
