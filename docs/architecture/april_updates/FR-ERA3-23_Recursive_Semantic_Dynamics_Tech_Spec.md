# FR-ERA3-23 — Recursive Semantic Dynamics Technical Specification

> **Phase 6 — SDA Foundation | Spec Slot S38**
> **Status:** DRAFT
> **Author:** CCP Tech-Spec Architect
> **Date:** 2026-05-13

---

## 0. Pre-Work Log

### 0.1 Protocol Loaded
`docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` — 10-section format confirmed. Section 3 must include "Existing Backend Integration" and "CBAR Mandate Enforcement" subsections.

### 0.2 Source PRD Wave 0 SDA Additions

> [!NOTE]
> No dedicated Phase 6 epic file exists. The SDA source set and Wave 0 PRD additions serve as the story source per the traceability note in the spec prompt. The PRD modules (PRD-04, 05, 06, 09) do not yet contain merged `## ERA 3 BROWNFIELD ANALYSIS` sections for SDA. The SDA Content Engine v1 and Artifact Taxonomy v1 define the Wave 0 scope.

- **PRD-04 (CVE Experience Design):** SDA grounds experience integrity — "The deceptively close failure is content that passes every existing quality gate but fails to preserve the coach's directional integrity" (Content Engine v1 §1.1).
- **PRD-05 (CBCS Law28):** SDA governs coaching interpretation — "Existential invariants are the deep structures that distinguish a coach's authentic transformation model from a surface-level approximation" (Content Engine v1 §2.3).
- **PRD-06 (Conscious Reactions):** SDA enforces reaction governance — "Recursive patterns emerge when the same semantic structure reappears across independently generated artifacts, suggesting a stable underlying attractor" (Taxonomy v1 §4.2).
- **PRD-09 (Silent Referral):** SDA ensures commercial trust transfer integrity — "Feedback loops create the mechanism by which runtime observations are validated against longitudinal evidence before influencing downstream decisions" (Taxonomy v1 §4.4).

### 0.3 SDA Source Set — Dynamics-Relevant Claims

1. **Content Engine v1:** "A recursive pattern is not a repetition defect — it is evidence that the coach's semantic field has a stable attractor that the system must protect rather than flatten" (§3.2).
2. **Artifact Taxonomy v1:** "Runtime Semantic Dynamics Objects (RecursivePattern, EmergentContextualInvariant, FeedbackLoop) are explicitly NOT canonical ontology rows. They are transient, decayable, and require stability scoring before any downstream consumer may treat them as reliable" (§4.1).
3. **Perceptual Primitives Architecture:** "Primitives are transformation operators, not edges. The hierarchy is: research evidence → primitive spaces → coalition signatures → edge products. Runtime dynamics sit between primitive activation and edge production" (§2.1).
4. **Matrix of Edging:** "The distinction between broad pre-trigger signals and sharp post-trigger execution force maps directly to the observation-vs-inference boundary that runtime dynamics must respect" (§3.4).

### 0.4 Memory/History Backend — Method Signatures

1. **`memory_tier_promotion_service.py`** — `MemoryTierPromotionService.run_pattern_sweep(episodic_nodes, existing_episodic_dates) → list[SemanticReviewProposal]` — Pattern detection over ≥3 occurrences across ≥14 days.
2. **`trigger_feedback_loop.py`** — `TriggerFeedbackLoop.calculate_precedence(trigger_map) → list[PrecedenceCalculation]` — Climb/hold/fall/dormant trend calculation via linear regression.
3. **`engagement_feedback.py`** — `EngagementFeedback.ingest(metrics) → EngagementMetrics` — Resonance marker detection at 2× rolling average.
4. **`weekly_evolution_engine.py`** — `WeeklyEvolutionEngine.apply_session(scorecard, session_data) → LeadershipScorecard` — Score evolution after ≥3 sessions with clamping to [1, 10].
5. **`cross_system_intelligence_service.py`** — `CrossSystemIntelligenceService.run_sunday_bot_meeting(client_data) → SundayBotMeetingPayload` — Weekly aggregation with PII zero-trust.

### 0.5 Experience Primitives

1. **EXP-PRG-004 (Long Loops for Habit Formation):** "By tracking and celebrating the 'Compound Arc', we anchor motivation in long-term identity shift rather than short-term spikes." Defines the macro-progression frame that recursive patterns must feed.
2. **EXP-FBK-001 (RIM Feedback Discipline):** "Relevant, Immediate, Meaningful — strictly bans delayed, disconnected, or purely vanity metrics." Constrains feedback loop projection latency.

### 0.6 Integration Tests with Longitudinal State

1. **`test_fr7_leadership_scorecard.py`** — AC7 tests: trait climbs after ≥3 exercise sessions with sophia ≥ 0.85 AND engagement > average. AC8 tests: score clamping to [1, 10]. Demonstrates multi-session state accumulation pattern.
2. **`test_step14_cross_system_integration.py`** — FR37 tests: Sunday Bot Meeting aggregation across ≥3 clients, PII zero-trust, coach-scoped isolation. Demonstrates cross-system longitudinal intelligence pattern.

### 0.7 Taxonomy Classification Confirmation

From `semantic_discernment_architecture_artifact_taxonomy_v_1.md` §4.1:

> "Layer 4 — Runtime Semantic Dynamics Objects: RecursivePattern, EmergentContextualInvariant, FeedbackLoop. These are runtime-derived forms. They are NOT canonical ontology. They require stability scoring, decay windows, and human-review hooks before downstream consumption."

**Classification: CONFIRMED** — All three objects are runtime semantic dynamics, not canonical registry artifacts.

---

## 1. Files Read

| Category | File | Purpose |
|---|---|---|
| **Protocol** | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | 10-section format, CBAR enforcement rules |
| **Spec Prompt** | `docs/architecture/april_updates/spec_prompts/P6_S38_FR-ERA3-23_Recursive_Semantic_Dynamics.md` | Assignment, scope, rejection criteria |
| **SDA Source** | `lab/semantic_discernment_architecture_content_engine_v_1.md` | Deceptively close failure problem, directional integrity |
| **SDA Source** | `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md` | 4-layer taxonomy, runtime dynamics classification |
| **SDA Source** | `lab/CCP APRIL Updates/05_Core_Experience/Perceptual_Primitives_Architecture.md` | Primitive hierarchy, transformation operators |
| **SDA Source** | `lab/CCP APRIL Updates/05_Core_Experience/Matrix of Edging.md` | Pre-trigger vs post-trigger boundary |
| **Backend** | `src/ccp/services/memory_tier_promotion_service.py` | Pattern sweep, governance gate, stale decay |
| **Backend** | `src/ccp/services/trigger_feedback_loop.py` | Precedence calculation, dormancy detection |
| **Backend** | `src/ccp/services/engagement_feedback.py` | Resonance marker ingestion |
| **Backend** | `src/ccp/services/weekly_evolution_engine.py` | Score evolution, session history |
| **Backend** | `src/ccp/services/trait_scoring_engine.py` | 12-trait rubric scoring with evidence |
| **Backend** | `src/ccp/services/cross_system_intelligence_service.py` | Weekly intelligence aggregation |
| **Primitives** | `primitives/experience/progression_replay/EXP-PRG-004.yaml` | Long Loops for Habit Formation |
| **Primitives** | `primitives/experience/feedback_scoring/EXP-FBK-001.yaml` | RIM Feedback Discipline |
| **Tests** | `tests/integration/test_fr7_leadership_scorecard.py` | AC7/AC8 longitudinal state assertions |
| **Tests** | `tests/integration/test_step14_cross_system_integration.py` | Cross-system intelligence assertions |

---

## 2. Overview

### 2.1 Problem

The CCP backend maintains multiple longitudinal intelligence services (memory tier promotion, trigger feedback loops, weekly evolution, engagement feedback) that each track patterns independently. However, there is no unified semantic dynamics layer that can:

1. **Detect recursive patterns** across these independent services and flag when the same semantic structure reappears across independently generated artifacts.
2. **Infer emergent contextual invariants** — deep structures that distinguish a coach's authentic transformation model from surface-level approximation.
3. **Track feedback loops** — the mechanism by which runtime observations are validated against longitudinal evidence before influencing downstream decisions.

Without this layer, the system is vulnerable to the "deceptively close failure" (Content Engine v1 §1.1) — content that passes every existing quality gate but fails to preserve directional integrity.

### 2.2 Solution

FR-ERA3-23 introduces a **Recursive Semantic Dynamics** layer that formalizes three runtime semantic objects:

- **`RecursivePattern`** — Observation: detects recurring semantic structures across artifact generations with stability scoring and decay.
- **`EmergentContextualInvariant`** — Inference: derives stable existential constraints from accumulated pattern evidence, with human-review gates.
- **`FeedbackLoop`** — Projection: tracks how observations and inferences feed back into downstream eval interpretation, with history and expiry.

These objects are explicitly **NOT canonical ontology**. They are transient, decayable runtime intelligence that informs eval interpretation without overwriting the primitive registry or coach soul data.

### 2.3 Scope

| In Scope | Out of Scope |
|---|---|
| Pydantic models for all 3 runtime objects | Modifications to the primitive YAML registry |
| Detection service with cadence configuration | Overwriting canonical ontology (coach_soul, tribe_soul) |
| Stability scoring algorithm | Real-time streaming detection (batch only) |
| Decay/expiry rules with configurable windows | Neo4j schema changes (uses existing graph manager) |
| Human-review hooks (Telegram operator flow) | Frontend Mini App surfaces |
| Downstream projection interfaces | LLM fine-tuning integration |
| Storage in Supabase JSONB + receipt chain | Payment or commercial logic |

---

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Artifact | Description |
|---|---|---|
| DEP-SDA-001 | `RecursivePatternObservation` | Runtime observation of recurring semantic structures |
| DEP-SDA-002 | `EmergentContextualInvariant` | Inferred existential constraint from pattern evidence |
| DEP-SDA-003 | `FeedbackLoopProjection` | History/projection of how dynamics influence eval |
| DEP-SDA-004 | `SemanticDynamicsService` | Orchestrator for detection, inference, and projection |
| DEP-SDA-005 | `DynamicsDecayEngine` | Configurable decay/expiry for all runtime objects |

### 3.2 Existing Backend Integration

This spec **extends** the following existing services — it does NOT replace them:

| Existing Service | Integration Point |
|---|---|
| `memory_tier_promotion_service.py` | `PatternFlaggingEngine.sweep()` output feeds `RecursivePattern` detection as one signal source |
| `trigger_feedback_loop.py` | `TriggerFeedbackLoop.calculate_precedence()` results feed `FeedbackLoopProjection` as precedence history |
| `engagement_feedback.py` | `EngagementFeedback.get_resonance_markers()` provides resonance evidence for `EmergentContextualInvariant` inference |
| `weekly_evolution_engine.py` | `WeeklyEvolutionEngine.apply_session()` trait history feeds `RecursivePattern` cross-session detection |
| `trait_scoring_engine.py` | `TraitScoringEngine.score_all_traits()` evidence citations are consumed by `EmergentContextualInvariant` as supporting signals |
| `cross_system_intelligence_service.py` | `SundayBotMeetingPayload` aggregation metrics feed weekly pattern sweep |

**Database Extension:**

| Table | Change | Fields |
|---|---|---|
| `semantic_dynamics` | NEW | `dynamics_id`, `coach_id`, `object_type` (enum), `payload` (JSONB), `stability_score`, `created_at`, `expires_at`, `status` |
| `dynamics_audit_log` | NEW | `audit_id`, `dynamics_id`, `action`, `actor`, `timestamp`, `previous_state`, `new_state` |
| `receipt_chain` | EXTEND (existing) | New `action` values: `SDA_PATTERN_DETECTED`, `SDA_INVARIANT_INFERRED`, `SDA_LOOP_PROJECTED` |

### 3.3 ADR-05 Primitives

| Primitive ID | Constraint Applied |
|---|---|
| **EXP-PRG-004** (Long Loops) | RecursivePattern detection must span ≥14 days (matches `PATTERN_MIN_SPAN_DAYS` in memory tier service). Pattern projection must feed the macro-progression frame, not just daily scores. |
| **EXP-FBK-001** (RIM Feedback) | FeedbackLoopProjection must emit results within 3 seconds of query (matches scoring engine SLA). No delayed batch-only access to active loop state. |
| **EXP-PRG-001** (Hook Cycle Velocity) | Short-loop feedback must not be conflated with long-loop recursive patterns. The system must distinguish micro-activation (EXP-PRG-001) from macro-recurrence (EXP-PRG-004). |

### 3.4 CBAR Mandate Enforcement — SDA Governance Constraints

> [!NOTE]
> Per the spec prompt traceability note: No formal Phase 6 epic file exists. CBAR mandates below are derived from SDA governance constraints in the Content Engine v1 and Artifact Taxonomy v1.

| Constraint ID | Constraint | Enforcement Mechanism |
|---|---|---|
| **SDA-G1** | No False Canonicalization | Runtime dynamics objects MUST have `status` field with values `OBSERVED`, `INFERRED`, `PROJECTED`, `EXPIRED`, `REJECTED`. No runtime object may be written to canonical ontology tables without explicit human APPROVE verdict. |
| **SDA-G2** | Long-Loop Trust Preservation | RecursivePattern requires ≥3 occurrences across ≥14 calendar days before stability_score > 0.5. Matches existing `PATTERN_OCCURRENCE_THRESHOLD` and `PATTERN_MIN_SPAN_DAYS` constants. |
| **SDA-G3** | Feedback-Loop Visibility | Every FeedbackLoopProjection must carry a `provenance_chain` listing the exact observation IDs and inference IDs that contributed to it. No opaque projections. |
| **SDA-G4** | Emergent-Context Awareness | EmergentContextualInvariant inference requires ≥2 supporting RecursivePattern observations with stability_score ≥ 0.7 each. Single-pattern inference is prohibited. |
| **SDA-G5** | Decay Mandate | All runtime objects expire. Default TTL: RecursivePattern = 90 days, EmergentContextualInvariant = 180 days, FeedbackLoopProjection = 30 days. Expired objects are soft-deleted (`status = EXPIRED`), never hard-deleted. |
| **SDA-G6** | Observation Before Inference | The system MUST NOT infer an EmergentContextualInvariant without at least one completed detection cycle. Detection → Observation → Inference → Projection is the mandatory sequence. |
| **SDA-G7** | Anti-Slop Gate | Any downstream consumer that receives a projection must check `stability_score ≥ consumer_threshold` before acting. Default consumer threshold = 0.6. |

### 3.5 Technical Decisions

| Decision | Rationale |
|---|---|
| **JSONB storage over dedicated columns** | Runtime dynamics payloads are polymorphic (3 object types). JSONB in `semantic_dynamics` table avoids schema explosion while maintaining queryability via GIN indexes. Matches existing `cultural_memory_map.entries` pattern. |
| **Batch detection cadence, not streaming** | Pattern detection runs as a scheduled sweep (nightly, matching `PatternFlaggingEngine.sweep()` cadence). Real-time detection would add latency to the critical path without proportional value. |
| **Stability score as float [0.0, 1.0]** | Continuous scoring enables threshold-based consumption by different downstream services with different confidence requirements. Matches existing trait scoring pattern (1–10 normalized). |
| **Soft-delete expiry, not hard-delete** | Expired dynamics remain queryable for audit and forensic purposes. Matches existing `receipt_chain` append-only philosophy. |
| **Human-review for inference, not observation** | Observations are algorithmic and high-volume. Inferences require human judgment (Telegram operator flow, matching `GovernanceGate` pattern in memory tier service). |

---

## 4. Implementation Plan

### Stage 1: Pydantic Models (NEW — `src/ccp/models/semantic_dynamics_models.py`)

Define all runtime object models, enums, and constants.

```python
# Constants
PATTERN_MIN_OCCURRENCES = 3          # SDA-G2
PATTERN_MIN_SPAN_DAYS = 14           # SDA-G2, matches memory_tier
INVARIANT_MIN_PATTERNS = 2           # SDA-G4
INVARIANT_MIN_PATTERN_STABILITY = 0.7  # SDA-G4
DEFAULT_CONSUMER_THRESHOLD = 0.6     # SDA-G7
PATTERN_TTL_DAYS = 90               # SDA-G5
INVARIANT_TTL_DAYS = 180            # SDA-G5
LOOP_TTL_DAYS = 30                  # SDA-G5
STALE_REVIEW_DAYS = 14              # Auto-expire unreviewed inferences

# Enums
class DynamicsObjectType(str, Enum):
    RECURSIVE_PATTERN = "RECURSIVE_PATTERN"
    EMERGENT_INVARIANT = "EMERGENT_INVARIANT"
    FEEDBACK_LOOP = "FEEDBACK_LOOP"

class DynamicsStatus(str, Enum):
    OBSERVED = "OBSERVED"
    INFERRED = "INFERRED"
    PROJECTED = "PROJECTED"
    EXPIRED = "EXPIRED"
    REJECTED = "REJECTED"
    PENDING_REVIEW = "PENDING_REVIEW"
```

### Stage 2: Detection Service (NEW — `src/ccp/services/semantic_dynamics_detector.py`)

Scheduled nightly sweep that:
1. Queries `memory_tier_promotion_service.PatternFlaggingEngine` output for new semantic review proposals
2. Queries `trigger_feedback_loop.TriggerFeedbackLoop` precedence calculations for trend data
3. Queries `engagement_feedback.EngagementFeedback` resonance markers
4. Queries `weekly_evolution_engine` trait history for cross-session patterns
5. Runs semantic similarity clustering (Aria in production, label-prefix in dev — matching `PatternFlaggingEngine._extract_root_driver()` pattern)
6. Emits `RecursivePatternObservation` objects with initial `stability_score`

### Stage 3: Inference Engine (NEW — `src/ccp/services/semantic_dynamics_inference.py`)

Post-detection analysis that:
1. Groups RecursivePatterns by semantic cluster
2. Checks SDA-G4: ≥2 patterns with stability ≥ 0.7
3. Derives candidate `EmergentContextualInvariant` with supporting evidence chain
4. Dispatches to `GovernanceGate`-style Telegram operator review (SDA-G1)
5. On APPROVE: status → `INFERRED`, stored with provenance chain
6. On REJECT: status → `REJECTED`, logged to `dynamics_audit_log`

### Stage 4: Projection Service (NEW — `src/ccp/services/semantic_dynamics_projection.py`)

Downstream interface that:
1. Accepts queries from eval interpretation consumers (FR-ERA3-22, FR-ERA3-18, FR-ERA3-05-CORE)
2. Returns `FeedbackLoopProjection` with stability score + provenance chain (SDA-G3)
3. Enforces consumer threshold check (SDA-G7): `stability_score ≥ consumer_threshold`
4. Tracks projection history for audit trail
5. Emits receipt chain entries: `SDA_LOOP_PROJECTED`

### Stage 5: Decay Engine (EXTEND — integrated into `src/ccp/services/semantic_dynamics_service.py`)

Scheduled sweep (weekly) that:
1. Scans all `semantic_dynamics` rows where `expires_at < NOW()`
2. Sets `status = EXPIRED` (soft-delete, SDA-G5)
3. Logs to `dynamics_audit_log`
4. Emits receipt chain entry: `SDA_DYNAMICS_EXPIRED`

### Stage 6: Orchestrator (NEW — `src/ccp/services/semantic_dynamics_service.py`)

Central service that wires Stages 2–5:
```python
class SemanticDynamicsService:
    def __init__(self, coach_id: str, neo4j_client=None, telegram_bot=None):
        ...

    def run_nightly_detection(self) -> list[RecursivePatternObservation]:
        """Stage 2: Nightly pattern sweep across all signal sources."""

    def run_inference_cycle(self) -> list[EmergentContextualInvariant]:
        """Stage 3: Post-detection inference with governance gate."""

    def query_projection(self, consumer_id: str, context: dict,
                         threshold: float = DEFAULT_CONSUMER_THRESHOLD
                         ) -> list[FeedbackLoopProjection]:
        """Stage 4: Downstream query interface."""

    def run_decay_sweep(self) -> list[str]:
        """Stage 5: Expire stale dynamics objects."""

    def process_operator_verdict(self, dynamics_id: str,
                                  verdict: str, operator_id: str
                                  ) -> Optional[EmergentContextualInvariant]:
        """Stage 3b: Human review processing."""
```

---

## 5. Primary Output Schema

### 5.1 RecursivePatternObservation

```python
class PatternOccurrence(BaseModel):
    """Single occurrence of a pattern in a specific artifact."""
    occurrence_id: str = Field(description="UUID")
    source_service: str = Field(description="e.g. 'memory_tier', 'trigger_feedback'")
    source_artifact_id: str = Field(description="ID of the artifact where pattern was observed")
    observed_at: datetime
    semantic_label: str = Field(description="Normalized semantic label (root driver)")
    raw_evidence: str = Field(description="Quoted text or metric that evidences the pattern")

class RecursivePatternObservation(BaseModel):
    """DEP-SDA-001: Runtime observation of recurring semantic structures."""
    pattern_id: str = Field(description="UUID, prefixed SDA-PAT-")
    coach_id: str = Field(min_length=2, max_length=4)
    object_type: Literal[DynamicsObjectType.RECURSIVE_PATTERN]
    status: DynamicsStatus = DynamicsStatus.OBSERVED
    semantic_cluster: str = Field(description="Normalized root driver label")
    occurrences: list[PatternOccurrence] = Field(min_length=PATTERN_MIN_OCCURRENCES)
    first_observed: date
    most_recent: date
    span_days: int = Field(ge=PATTERN_MIN_SPAN_DAYS)
    stability_score: float = Field(ge=0.0, le=1.0)
    stability_method: str = Field(default="frequency_span_weighted")
    created_at: datetime
    expires_at: datetime  # created_at + PATTERN_TTL_DAYS
    supporting_evidence_summary: str

    @model_validator(mode="after")
    def validate_span(self) -> "RecursivePatternObservation":
        actual_span = (self.most_recent - self.first_observed).days
        if actual_span < PATTERN_MIN_SPAN_DAYS:
            raise ValueError(f"Span {actual_span} < minimum {PATTERN_MIN_SPAN_DAYS}")
        return self
```

### 5.2 EmergentContextualInvariant

```python
class InvariantEvidence(BaseModel):
    """Link to a supporting RecursivePattern."""
    pattern_id: str
    stability_score: float = Field(ge=INVARIANT_MIN_PATTERN_STABILITY)
    contribution_weight: float = Field(ge=0.0, le=1.0)

class EmergentContextualInvariant(BaseModel):
    """DEP-SDA-002: Inferred existential constraint from pattern evidence."""
    invariant_id: str = Field(description="UUID, prefixed SDA-INV-")
    coach_id: str = Field(min_length=2, max_length=4)
    object_type: Literal[DynamicsObjectType.EMERGENT_INVARIANT]
    status: DynamicsStatus = DynamicsStatus.PENDING_REVIEW
    invariant_statement: str = Field(description="Natural language existential claim")
    directional_vector: str = Field(description="Which direction this invariant protects")
    supporting_patterns: list[InvariantEvidence] = Field(
        min_length=INVARIANT_MIN_PATTERNS
    )
    confidence_score: float = Field(ge=0.0, le=1.0)
    operator_verdict: Optional[str] = None  # APPROVE / REJECT / MODIFY
    operator_id: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime
    expires_at: datetime  # created_at + INVARIANT_TTL_DAYS
    provenance_chain: list[str] = Field(description="Ordered list of pattern_ids")

    @model_validator(mode="after")
    def validate_min_patterns(self) -> "EmergentContextualInvariant":
        if len(self.supporting_patterns) < INVARIANT_MIN_PATTERNS:
            raise ValueError(
                f"Requires ≥{INVARIANT_MIN_PATTERNS} supporting patterns"
            )
        for p in self.supporting_patterns:
            if p.stability_score < INVARIANT_MIN_PATTERN_STABILITY:
                raise ValueError(
                    f"Pattern {p.pattern_id} stability {p.stability_score} "
                    f"< minimum {INVARIANT_MIN_PATTERN_STABILITY}"
                )
        return self
```

### 5.3 FeedbackLoopProjection

```python
class ProjectionHistoryEntry(BaseModel):
    """Record of a single projection query."""
    query_id: str
    consumer_id: str
    queried_at: datetime
    threshold_used: float
    projection_accepted: bool

class FeedbackLoopProjection(BaseModel):
    """DEP-SDA-003: History/projection of how dynamics influence eval."""
    projection_id: str = Field(description="UUID, prefixed SDA-LOOP-")
    coach_id: str = Field(min_length=2, max_length=4)
    object_type: Literal[DynamicsObjectType.FEEDBACK_LOOP]
    status: DynamicsStatus = DynamicsStatus.PROJECTED
    source_invariant_id: Optional[str] = Field(
        description="The EmergentContextualInvariant this loop tracks"
    )
    source_pattern_ids: list[str] = Field(
        description="RecursivePattern IDs feeding this loop"
    )
    loop_direction: str = Field(description="'reinforcing' or 'corrective'")
    current_strength: float = Field(ge=0.0, le=1.0)
    trend: str = Field(description="'strengthening', 'stable', 'weakening', 'dormant'")
    projection_summary: str = Field(
        description="Natural language description of projected impact"
    )
    provenance_chain: list[str] = Field(
        description="Ordered IDs: pattern → invariant → loop (SDA-G3)"
    )
    query_history: list[ProjectionHistoryEntry] = Field(default_factory=list)
    created_at: datetime
    expires_at: datetime  # created_at + LOOP_TTL_DAYS
    downstream_consumers: list[str] = Field(
        default_factory=list,
        description="FR IDs that have consumed this projection"
    )
```

### 5.4 Stability Score Calculation

```python
def calculate_stability_score(
    occurrence_count: int,
    span_days: int,
    source_diversity: int,  # number of distinct signal sources
    recency_weight: float,  # 0.0-1.0, how recent the latest occurrence is
) -> float:
    """Weighted stability score for RecursivePattern.

    Formula:
      base = min(1.0, occurrence_count / (PATTERN_MIN_OCCURRENCES * 2))
      span_factor = min(1.0, span_days / (PATTERN_MIN_SPAN_DAYS * 3))
      diversity_bonus = min(0.2, source_diversity * 0.05)
      score = (base * 0.4) + (span_factor * 0.3) + (recency_weight * 0.2) + diversity_bonus

    Clamped to [0.0, 1.0].
    """
```

---

## 6. Backward Compatibility & Fallback

### 6.1 Zero-Impact on Existing Services

All existing services continue to function identically. The semantic dynamics layer is purely additive:

- `memory_tier_promotion_service.py` — No changes. Its `SemanticReviewProposal` output is **read** by the dynamics detector, not modified.
- `trigger_feedback_loop.py` — No changes. Its `PrecedenceCalculation` output is **read** as a signal source.
- `engagement_feedback.py` — No changes. Resonance markers are **read** as evidence.
- `weekly_evolution_engine.py` — No changes. Trait history is **read** for cross-session detection.

### 6.2 Graceful Degradation

| Failure Mode | Behavior |
|---|---|
| Dynamics detector fails to run | All downstream consumers receive empty projection lists. No eval interpretation changes. Existing quality gates remain authoritative. |
| Inference engine fails | Observations are stored but no invariants are inferred. Manual operator review queue remains empty. |
| Database unavailable | In-memory fallback: dynamics objects are logged to receipt chain only, without persistent storage. |
| Operator does not review within 14 days | Candidate invariant auto-expires to `REJECTED` with reason `STALE_REVIEW_TIMEOUT`. Matches `check_stale_decay()` pattern in memory tier service. |

### 6.3 Feature Flag

```python
SEMANTIC_DYNAMICS_ENABLED: bool = False  # Default OFF until Phase 6 rollout
```

When disabled, the `SemanticDynamicsService` returns empty results for all queries. The nightly detection sweep is skipped. No database writes occur.

---

## 7. Tasks

| # | Task | New/Extend | Output |
|---|---|---|---|
| T1 | Create `semantic_dynamics_models.py` with all Pydantic models, enums, constants | NEW | `src/ccp/models/semantic_dynamics_models.py` |
| T2 | Create `semantic_dynamics` + `dynamics_audit_log` Supabase tables | NEW | `src/ccp/scripts/setup_supabase.py` (extend) |
| T3 | Create `semantic_dynamics_detector.py` — nightly pattern sweep | NEW | `src/ccp/services/semantic_dynamics_detector.py` |
| T4 | Create `semantic_dynamics_inference.py` — invariant derivation + governance gate | NEW | `src/ccp/services/semantic_dynamics_inference.py` |
| T5 | Create `semantic_dynamics_projection.py` — downstream query interface | NEW | `src/ccp/services/semantic_dynamics_projection.py` |
| T6 | Create `semantic_dynamics_service.py` — orchestrator + decay engine | NEW | `src/ccp/services/semantic_dynamics_service.py` |
| T7 | Extend `receipt_chain` with SDA action types | EXTEND | `src/ccp/core/receipt_chain.py` |
| T8 | Create integration test suite | NEW | `tests/integration/test_sda_recursive_dynamics.py` |
| T9 | Create feature flag configuration | NEW | Config / environment variable |

---

## 8. Acceptance Criteria

### AC1 — RecursivePattern Minimum Thresholds (SDA-G2)

**Criterion:** A `RecursivePatternObservation` with fewer than 3 occurrences OR a span < 14 days MUST be rejected at Pydantic validation time.

**FAILURE EXAMPLE:** A pattern with 2 occurrences over 21 days is accepted. This violates SDA-G2 because occurrence_count < PATTERN_MIN_OCCURRENCES.

**CBAR Ref:** SDA-G2 (Long-Loop Trust Preservation)

### AC2 — EmergentContextualInvariant Requires ≥2 Stable Patterns (SDA-G4)

**Criterion:** An `EmergentContextualInvariant` MUST NOT be created with fewer than 2 supporting `RecursivePattern` observations, each with `stability_score ≥ 0.7`.

**FAILURE EXAMPLE:** An invariant is inferred from a single pattern with stability 0.95. Despite high confidence in one pattern, single-pattern inference is prohibited.

**CBAR Ref:** SDA-G4 (Emergent-Context Awareness)

### AC3 — No False Canonicalization (SDA-G1)

**Criterion:** No runtime dynamics object may have its `status` set to anything other than `OBSERVED`, `INFERRED`, `PROJECTED`, `EXPIRED`, `REJECTED`, or `PENDING_REVIEW`. No dynamics object may be written to canonical ontology tables (`coach_soul`, `tribe_soul`, `ttt_baseline`).

**FAILURE EXAMPLE:** A `RecursivePatternObservation` is written directly to the `coach_soul.json` voice profile. This treats runtime dynamics as static ontology.

**CBAR Ref:** SDA-G1 (No False Canonicalization)

### AC4 — Feedback Loop Provenance Chain (SDA-G3)

**Criterion:** Every `FeedbackLoopProjection` MUST carry a non-empty `provenance_chain` listing the exact observation IDs and inference IDs that contributed to it.

**FAILURE EXAMPLE:** A projection is returned with `provenance_chain = []`. The downstream consumer has no way to trace why this projection was generated.

**CBAR Ref:** SDA-G3 (Feedback-Loop Visibility)

### AC5 — Decay Expiry Enforcement (SDA-G5)

**Criterion:** When `run_decay_sweep()` executes, all dynamics objects with `expires_at < NOW()` MUST have their `status` set to `EXPIRED`. The object MUST NOT be hard-deleted.

**FAILURE EXAMPLE:** An expired pattern is deleted from the database entirely. A forensic audit later needs to query what patterns existed during a specific period and cannot.

**CBAR Ref:** SDA-G5 (Decay Mandate)

### AC6 — Observation Before Inference Ordering (SDA-G6)

**Criterion:** `run_inference_cycle()` MUST NOT produce any `EmergentContextualInvariant` if `run_nightly_detection()` has not produced at least one `RecursivePatternObservation` with `status = OBSERVED` for the target coach.

**FAILURE EXAMPLE:** The inference engine runs against an empty observations table and generates a speculative invariant from historical coach_soul data alone.

**CBAR Ref:** SDA-G6 (Observation Before Inference)

### AC7 — Consumer Threshold Gate (SDA-G7)

**Criterion:** `query_projection()` MUST filter results where `current_strength < threshold`. Default threshold = 0.6. A consumer calling with `threshold=0.8` must receive only projections with `current_strength ≥ 0.8`.

**FAILURE EXAMPLE:** A consumer with `threshold=0.8` receives a projection with `current_strength=0.55` because the threshold check was skipped.

**CBAR Ref:** SDA-G7 (Anti-Slop Gate)

### AC8 — Human Review Gate for Inference (SDA-G1)

**Criterion:** No `EmergentContextualInvariant` may transition from `PENDING_REVIEW` to `INFERRED` without an explicit operator verdict of `APPROVE`. The `operator_id` and `reviewed_at` fields MUST be populated.

**FAILURE EXAMPLE:** An invariant is auto-approved because no operator responded within 24 hours. The system assumed approval by silence.

**CBAR Ref:** SDA-G1 (No False Canonicalization)

### AC9 — Feature Flag Isolation

**Criterion:** When `SEMANTIC_DYNAMICS_ENABLED = False`, all public methods of `SemanticDynamicsService` return empty/no-op results. No database writes occur. No receipt chain entries are emitted.

**FAILURE EXAMPLE:** The feature flag is off but the nightly detector still runs and writes observations to the database.

### AC10 — Receipt Chain Integration

**Criterion:** Every state transition (detection, inference, projection, decay, operator verdict) MUST emit a receipt chain entry with the appropriate `SDA_*` action type.

**FAILURE EXAMPLE:** A pattern is detected and stored but no receipt chain entry exists for the detection event. The audit trail is broken.

---

## 9. Dependencies

### 9.1 Internal Dependencies

| Dependency | Service/Module | Required For |
|---|---|---|
| `ReceiptChain` | `src/ccp/core/receipt_chain.py` | Audit trail for all dynamics state transitions |
| `PatternFlaggingEngine` | `src/ccp/services/memory_tier_promotion_service.py` | Signal source: semantic review proposals |
| `TriggerFeedbackLoop` | `src/ccp/services/trigger_feedback_loop.py` | Signal source: precedence calculations |
| `EngagementFeedback` | `src/ccp/services/engagement_feedback.py` | Signal source: resonance markers |
| `WeeklyEvolutionEngine` | `src/ccp/services/weekly_evolution_engine.py` | Signal source: trait history |
| `TraitScoringEngine` | `src/ccp/services/trait_scoring_engine.py` | Signal source: evidence citations |
| `GovernanceGate` (pattern) | `src/ccp/services/memory_tier_promotion_service.py` | Architecture pattern for Telegram operator review |

### 9.2 External Dependencies

| Dependency | Purpose | Fallback |
|---|---|---|
| Supabase (PostgreSQL) | Persistent storage of dynamics objects | In-memory with receipt chain logging |
| Telegram Bot API | Operator review notifications | Queue without notification; stale-decay auto-reject at 14 days |
| Aria (production) | Semantic similarity for pattern clustering | Label-prefix matching (matching `_extract_root_driver()` dev stub) |

### 9.3 Downstream Consumers

| Consumer FR | How It Consumes | What It Receives |
|---|---|---|
| FR-ERA3-22 (Semantic Eval) | Calls `query_projection()` before eval scoring | Active projections with stability ≥ consumer threshold |
| FR-ERA3-18 (Content Governance) | Checks invariants before content approval | List of active invariants for directional integrity check |
| FR-ERA3-05-CORE (Conscious Reactions) | Queries patterns for reaction topic relevance | Active patterns for the coach's semantic field |
| FR-ERA3-03 (Score Interpretation) | Uses projections to contextualize scores | Feedback loop trend data (strengthening/weakening/stable) |
| FR-ERA3-04 (OFO Engine) | Checks invariants for offer framing | Directional vectors that must be preserved in OFO assets |
| FR-ERA3-09 (Silent Referral) | Validates referral trust transfer | Active invariants ensuring commercial integrity |

---

## 10. Testing Strategy

### 10.1 Unit Tests — `tests/integration/test_sda_recursive_dynamics.py`

Following the existing pytest pattern (matching `test_fr7_leadership_scorecard.py` structure):

#### Test Class: `TestAC1PatternMinimumThresholds`
```python
def test_pattern_below_min_occurrences_raises():
    """AC1: 2 occurrences must fail Pydantic validation."""

def test_pattern_below_min_span_raises():
    """AC1: 3 occurrences over 10 days must fail validation."""

def test_pattern_at_threshold_succeeds():
    """AC1: 3 occurrences over 14 days must succeed."""
```

#### Test Class: `TestAC2InvariantMinPatterns`
```python
def test_invariant_with_one_pattern_raises():
    """AC2: Single-pattern inference must fail."""

def test_invariant_with_low_stability_pattern_raises():
    """AC2: Pattern stability 0.5 < 0.7 must fail."""

def test_invariant_with_two_stable_patterns_succeeds():
    """AC2: 2 patterns, each stability ≥ 0.7, must succeed."""
```

#### Test Class: `TestAC3NoCanonicalization`
```python
def test_dynamics_status_enum_values():
    """AC3: Only valid status values exist in enum."""

def test_dynamics_never_writes_to_coach_soul():
    """AC3: Service does not modify canonical ontology."""
```

#### Test Class: `TestAC5DecayExpiry`
```python
def test_expired_objects_set_to_expired_status():
    """AC5: Objects past expires_at become EXPIRED."""

def test_expired_objects_not_hard_deleted():
    """AC5: Expired objects remain queryable."""
```

#### Test Class: `TestAC6ObservationBeforeInference`
```python
def test_inference_without_observations_returns_empty():
    """AC6: No observations → no inferences."""
```

#### Test Class: `TestAC7ConsumerThreshold`
```python
def test_threshold_filters_weak_projections():
    """AC7: threshold=0.8 filters projection with strength=0.55."""

def test_default_threshold_applied():
    """AC7: Default 0.6 threshold is enforced."""
```

#### Test Class: `TestAC8HumanReviewGate`
```python
def test_invariant_requires_approve_verdict():
    """AC8: PENDING_REVIEW → INFERRED requires APPROVE."""

def test_stale_review_auto_rejects():
    """AC8: Unreviewed after 14 days → REJECTED."""
```

#### Test Class: `TestAC9FeatureFlag`
```python
def test_disabled_flag_returns_empty():
    """AC9: Flag OFF → all methods return empty."""

def test_disabled_flag_no_db_writes():
    """AC9: Flag OFF → no database operations."""
```

### 10.2 Manual QA Flow — Long-Loop Behavior Validation

> [!IMPORTANT]
> This manual QA flow validates the end-to-end recursive dynamics lifecycle over a simulated multi-week period.

**Scenario: Coach "EMI" — Financial Fear Recursive Pattern**

| Step | Action | Expected Result | Verification |
|---|---|---|---|
| **Day 1** | Ingest 1st episode with `root_driver = "financial_fear"` via `memory_tier_promotion_service` | Episode stored in episodic tier. No pattern detected (< 3 occurrences). | Query `semantic_dynamics` table: 0 rows for coach EMI. |
| **Day 8** | Ingest 2nd episode with same root driver | Still no pattern (< 3 occurrences). | Query: 0 rows. |
| **Day 16** | Ingest 3rd episode. Run `run_nightly_detection()` | `RecursivePatternObservation` created. `span_days = 15`. `stability_score` calculated. `status = OBSERVED`. | Query: 1 row, type = RECURSIVE_PATTERN, status = OBSERVED. Receipt chain has `SDA_PATTERN_DETECTED` entry. |
| **Day 17** | Ingest separate `trigger_feedback_loop` precedence showing "financial_fear" in CLIMB. Run detection again. | Existing pattern updated. `stability_score` increases (multi-source diversity bonus). | `stability_score` > previous. `source_diversity` incremented. |
| **Day 20** | Create 2nd pattern: "imposter_syndrome" (same coach, ≥3 occurrences, ≥14 days). Run inference. | If both patterns have stability ≥ 0.7: `EmergentContextualInvariant` candidate created with `status = PENDING_REVIEW`. | Query: 1 invariant row. Telegram operator notification sent. |
| **Day 21** | Operator sends APPROVE via Telegram | Invariant transitions to `status = INFERRED`. `operator_id` and `reviewed_at` populated. | Query: invariant status = INFERRED. Receipt chain has `SDA_INVARIANT_INFERRED`. |
| **Day 22** | Downstream consumer FR-ERA3-22 calls `query_projection(threshold=0.6)` | `FeedbackLoopProjection` returned with provenance chain linking to both patterns + invariant. | Projection has non-empty `provenance_chain`. `current_strength ≥ 0.6`. |
| **Day 52** | Run `run_decay_sweep()` | FeedbackLoopProjection (30-day TTL) expires. `status = EXPIRED`. Patterns and invariant still active. | Loop: EXPIRED. Patterns: OBSERVED. Invariant: INFERRED. |
| **Day 106** | Run `run_decay_sweep()` | RecursivePatterns (90-day TTL) expire. Invariant still active (180-day TTL). | Patterns: EXPIRED. Invariant: INFERRED. All rows still in database (soft-delete). |

**Pass Criteria:** All steps produce expected results. No canonical ontology is modified. Receipt chain is complete. Expired objects remain queryable.

---

*End of FR-ERA3-23 Technical Specification*
