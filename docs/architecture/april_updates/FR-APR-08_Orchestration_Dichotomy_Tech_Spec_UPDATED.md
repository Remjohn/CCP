# Tech-Spec: FR-APR-08 — Orchestration Dichotomy (DSPy + Pydantic Determinism)

**Created:** 2026-05-03
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v5.0 / April Updates Full Build)
**Architecture Reference:** April Updates Master PRD §7.3, §8.6
**Skill Implementation:** `backend/core/orchestration_dichotomy.py`, `backend/core/primitive_schemas.py`, `backend/core/coalition_engine.py`
**Role Executing:** Paige (BMAD Tech Writer)

---

## 1. Files Read
- `docs/prd/April_Updates_Master_PRD.md` (§7, §8.6)
- `lab/CCP APRIL Updates/Perceptual_Primitives_Architecture.md`
- `lab/CCP APRIL Updates/Matrix of Edging.md`
- `lab/CCP APRIL Updates/Primitive_Family_Classification_CCP_CMF.md`
- `lab/CCP APRIL Updates/Primitive_Conscious_Orchestration_Architecture.md`
- `docs/architecture/CCP_Technical_Architecture.md` (§4 JIT Skill Compiler)

---

## 2. Overview

### Problem Statement
The CCP's JIT Skill Compiler (CCSB) is a deterministic pipeline — every step is traceable, every dependency registered, every output schema-validated. But the April Updates introduce the Primitive/Coalition/Edging pipeline, which by nature requires high-variance LLM reasoning: analyzing raw coach speech for irony, identifying tribal references, scoring emotional charge. If this unpredictable LLM logic runs inside the main deterministic pipeline, a single hallucination corrupts the entire output chain. The system needs a strict architectural boundary between "things that must be deterministic" and "things that must be creative."

### Solution
FR-APR-08 implements the **Orchestration Dichotomy** — a hard boundary between the deterministic FastAPI/Modal execution loop and the creative DSPy/LLM reasoning layer. All LLM-generated outputs (Primitive Candidate lists, Coalition Signatures, Edge Products) are validated through Pydantic schemas before crossing the boundary into the deterministic pipeline. If an LLM output fails Pydantic validation, the system does NOT retry with a looser schema — it reverts to a safe fallback (the last validated coalition or a neutral archetype default). This prevents centroid drift and ensures the main pipeline never processes unvalidated creative output.

### Scope
**In scope:**
- Pydantic schemas for Primitive Candidates, Coalition Signatures, and Edge Products.
- DSPy module wrappers for LLM reasoning with structured output enforcement.
- Validation boundary (the "Dichotomy Gate") between creative and deterministic layers.
- Safe fallback mechanism on validation failure.
- Coalition Fatality logging.
- Anti-centroid gates at every handoff.

**Out of scope:**
- The CCF script generation pipeline (existing — consumes outputs from this spec).
- The CRAL Research Subsystem (FR14 — produces inputs to this spec).
- Voice DNA extraction (FR3, FR4 — consumed here for comparison).

---

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `orchestration_dichotomy.py` | Dichotomy Gate | COMPONENT — Validates LLM outputs against Pydantic schemas before forwarding. |
| `primitive_schemas.py` | Schema Library | COMPONENT — All Pydantic models for Primitives, Coalitions, Edge Products. |
| `coalition_engine.py` | Coalition Assembler | COMPONENT — Combines validated primitives into weighted coalitions. |
| `DEP-APR08-001` | PrimitiveCandidate | DATA — Structured single primitive output from DSPy. |
| `DEP-APR08-002` | CoalitionSignature | DATA — Validated assembly of 2-5 primitives. |
| `DEP-APR08-003` | EdgeProduct | DATA — Final tension-loaded routing payload. |
| DSPy | Framework | EXTERNAL — Structured LLM calls with typed outputs. |
| FR14 (CRAL Research) | Producer | UPSTREAM — Provides the Broad Signal and Research Findings that trigger primitive analysis. |
| FR24 (Weekly Pipeline) | Consumer | DOWNSTREAM — Receives validated Edge Products for CCF script routing. |

### 3.2 Technical Decisions
1. **Pydantic Strict Mode:** All schemas use `model_config = ConfigDict(strict=True)`. No coercion. A `str` field that receives an `int` fails validation. This eliminates the "almost right" problem where LLM outputs are type-coerced into valid-looking but semantically wrong structures.
2. **DSPy over Raw API Calls:** DSPy provides `dspy.TypedPredictor` which enforces output type contracts at the framework level. This is more reliable than post-hoc validation of raw `ChatCompletion` responses.
3. **Fallback is Conservative, Not Creative:** When validation fails, the fallback is the last successfully validated coalition for this coach, not a freshly generated "safer" output. This prevents the system from generating increasingly bland content in response to validation failures (anti-centroid drift).
4. **Coalition Fatality is Data:** When a promising coalition collapses during downstream CCF/CMF execution (audience doesn't engage, coach rejects output), the fatality is logged with full context. Over time, this creates a high-value training signal for improving primitive selection.

<!-- UPDATED: Added Section 3.3 for ADR-05 Primitive-loading mandate and Dual-Source Validation -->
### 3.3 ADR-05 Primitives and Dual-Source Validation

**ADR-05 Primitive-Loading Mandate:**
Every orchestration decision must reference specific primitive YAML IDs (e.g., `PRM-STR-008`), not primitive family names (e.g., `STR`). This ensures absolute traceability and prevents the system from reverting to vague, family-level generalizations during coalition assembly.

| Primitive ID | Name | Role in Architecture |
|---|---|---|
| **ADR-05** | Primitive Loading Mandate | Enforces strict, ID-level primitive referencing in all orchestration workflows. |

**Dual-Source Validation Requirement:**
Every primitive invoked must be strictly validated against both:
1. **The YAML Registry:** Confirming the primitive matches its codified geometric constraints, float boundaries, and synergistic/antagonistic rules.
2. **The PRD Module Source:** Verifying the primitive's alignment with its underlying literature audit and mechanistic definition.

If a primitive candidate fails to pass this Dual-Source Validation, it is rejected by the Dichotomy Gate and blocked from entering the Coalition Engine.

---

## 4. Implementation Plan

### Stage 1: Pydantic Schema Library
*Agent:* Backend (`primitive_schemas.py`)
*Inputs:* Primitive Family Classification document.
*Outputs:* Validated Pydantic models.

```python
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Literal
from enum import Enum

class PrimitiveFamily(str, Enum):
    STRUCTURAL = "structural"
    TENSION = "tension"
    IDENTITY = "identity"
    COMPRESSION = "compression"
    EMOTIONAL = "emotional"

class PrimitiveCandidate(BaseModel):
    model_config = ConfigDict(strict=True)
    
    # <!-- UPDATED: Enforce ADR-05 specific YAML IDs over primitive family names -->
    primitive_id: str = Field(..., min_length=11, max_length=15)  # e.g. PRM-STR-008
    primitive_name: str = Field(..., min_length=3, max_length=80)
    family: PrimitiveFamily
    evidence_quote: str = Field(..., min_length=20)       # Must cite real coach speech
    evidence_fidelity: float = Field(..., ge=0.0, le=1.0)
    emotional_charge: float = Field(..., ge=0.0, le=1.0)
    tribal_density: float = Field(..., ge=0.0, le=1.0)
    speakability: float = Field(..., ge=0.0, le=1.0)
    
    @field_validator('evidence_quote')
    @classmethod
    def evidence_must_not_be_generic(cls, v):
        generic_phrases = ["in general", "most people", "it is said", "studies show"]
        for phrase in generic_phrases:
            if phrase.lower() in v.lower():
                raise ValueError(f"Evidence quote contains generic phrase '{phrase}'. Must cite specific coach speech.")
        return v

class CoalitionSignature(BaseModel):
    model_config = ConfigDict(strict=True)
    
    coalition_id: str
    primitives: list[PrimitiveCandidate] = Field(..., min_length=2, max_length=5)
    # <!-- UPDATED: Dominant primitive must be a specific YAML ID -->
    dominant_primitive_id: str
    combined_force_score: float = Field(..., ge=0.0, le=1.0)
    edge_product_type: str
    
class EdgeProduct(BaseModel):
    model_config = ConfigDict(strict=True)
    
    edge_id: str
    coalition_id: str
    tension_object: str = Field(..., min_length=10)
    ccf_routing_target: str                     # Which CCF archetype/format receives this
    cmf_routing_target: str | None = None       # Optional CMF routing
    anti_centroid_score: float = Field(..., ge=0.0, le=1.0)
```

### Stage 2: DSPy Modules
*Agent:* Backend (`orchestration_dichotomy.py`)
*Inputs:* Coach transcript + CRAL Research Findings.
*Outputs:* List of `PrimitiveCandidate` objects.

**Steps:**
1. Define DSPy signature: `class ExtractPrimitives(dspy.Signature): transcript: str = dspy.InputField(); research_context: str = dspy.InputField(); candidates: list[PrimitiveCandidate] = dspy.OutputField()`.
2. Wrap in `dspy.TypedPredictor(ExtractPrimitives)`.
3. LLM call returns structured list of candidates with all fields populated.
4. Each candidate is validated against `PrimitiveCandidate` schema automatically by DSPy.
5. If ANY candidate fails validation, DSPy retries with a correction prompt (max 2 retries).
6. After 2 failed retries: abort extraction, log `PRIMITIVE_EXTRACTION_FAILED`, use fallback.

### Stage 3: The Dichotomy Gate
*Agent:* Backend (`orchestration_dichotomy.py`)
*Inputs:* DSPy outputs (PrimitiveCandidates, CoalitionSignatures, EdgeProducts).
*Outputs:* Validated objects forwarded to deterministic pipeline OR fallback.

**Steps:**
1. DSPy produces a list of `PrimitiveCandidate` objects.
2. The Dichotomy Gate runs additional business logic validation:
   - **Anti-Centroid Gate:** If ALL candidates have `emotional_charge < 0.3`, the output is too safe. Reject with `CENTROID_DRIFT_DETECTED`.
   - **Evidence Minimum:** At least 2 candidates must have `evidence_fidelity >= 0.6`.
   - **Family Diversity:** Candidates must span at least 2 different `PrimitiveFamily` values.
   <!-- UPDATED: Added Dual-Source Validation check step -->
   - **Dual-Source Validation (Runtime):** Each candidate must successfully cross-reference its specific `primitive_id` with the existing YAML registry definition. *Note: PRD module source alignment is validated at build-time to preserve deterministic runtime execution.*
3. If gate PASSES: forward to Coalition Engine.
4. If gate FAILS: load the last validated coalition for this coach from `coalition_history` table. Log the failure reason.

### Stage 4: Coalition Engine
*Agent:* Backend (`coalition_engine.py`)
*Inputs:* Validated PrimitiveCandidates.
*Outputs:* CoalitionSignature + EdgeProduct.

**Steps:**
1. Sort candidates by `combined_score = (evidence_fidelity * 0.3) + (emotional_charge * 0.25) + (tribal_density * 0.2) + (speakability * 0.25)`.
2. Select top 2-5 candidates (minimum 2 required for a coalition).
3. Identify dominant primitive (highest `combined_score`).
4. Calculate `combined_force_score` as weighted average of selected candidates.
<!-- UPDATED: Edge product type generation must reference specific primitive YAML IDs, not primitive family names -->
5. Generate `edge_product_type` based on the dominant primitive's specific `primitive_id` matching rules.
6. Extract the `tension_object` by identifying the core conflict generated by the dominant primitive's ruleset.
7. Calculate the `anti_centroid_score` by taking the inverse average of the `emotional_charge` and `speakability` properties of the selected primitives.
8. Validate the coalition against `CoalitionSignature` schema.
9. Write the validated `CoalitionSignature` and `EdgeProduct` to the `coalition_history` table with `validation_status: 'validated'`.
10. Route the Edge Product to the appropriate CCF archetype via the `ccf_routing_target` field.

### Stage 5: Coalition Fatality Logging
*Agent:* Background monitoring
*Inputs:* Post-publication performance data (from FR43 Data Analyst Agent).
*Outputs:* Fatality records.

**Steps:**
1. After CCF processes the Edge Product and publishes content, FR43 tracks engagement.
2. If engagement metrics fall below the coach's rolling 8-week average by >40%, the coalition is flagged as a potential fatality.
3. Execute DSPy `AnalyzeFatality` module (Inputs: `coalition_history` payload, `post_publication_data`. Output: `diagnosis_string` detailing why the evidence, tribal density, or emotional charge failed).
4. Log to `coalition_fatalities` table: `coalition_id`, `edge_product_id`, `expected_performance`, `actual_performance`, `delta`, `diagnosis`.

---

## 5. Data Model

### Table: `coalition_history`

```sql
CREATE TABLE IF NOT EXISTS coalition_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coach_id UUID NOT NULL,
    coalition_signature JSONB NOT NULL,          -- Full CoalitionSignature object
    edge_product JSONB NOT NULL,                 -- Full EdgeProduct object
    primitive_candidates JSONB NOT NULL,          -- Array of PrimitiveCandidate objects
    validation_status VARCHAR(20) NOT NULL CHECK (validation_status IN (
        'validated', 'fallback_used', 'centroid_rejected'
    )),
    anti_centroid_score FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_coalition_coach ON coalition_history(coach_id);
CREATE INDEX idx_coalition_status ON coalition_history(validation_status);
```

### Table: `coalition_fatalities`

```sql
CREATE TABLE IF NOT EXISTS coalition_fatalities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coalition_id UUID NOT NULL REFERENCES coalition_history(id),
    edge_product_id VARCHAR(100) NOT NULL,
    expected_engagement FLOAT,
    actual_engagement FLOAT,
    delta_percentage FLOAT,
    diagnosis TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 6. Tasks

- [ ] **Task 1:** Implement Pydantic schema library (`primitive_schemas.py`) with all models and validators.
- [ ] **Task 2:** Build DSPy module for Primitive Candidate extraction with `TypedPredictor`.
- [ ] **Task 3:** Implement the Dichotomy Gate with Anti-Centroid, Evidence Minimum, and Family Diversity checks.
<!-- UPDATED: Added Dual-Source Validation task -->
- [ ] **Task 4:** Build Dual-Source Validation in the Dichotomy Gate to check candidates against both YAML registry and PRD module sources.
- [ ] **Task 5:** Build the Coalition Engine (scoring, selection, dominant identification, edge product generation).
- [ ] **Task 6:** Implement safe fallback mechanism (load last validated coalition on gate failure).
- [ ] **Task 7:** Build Coalition Fatality logging with post-publication performance monitoring.
- [ ] **Task 8:** Create `coalition_history` and `coalition_fatalities` tables.
- [ ] **Task 9:** Wire Edge Product output to CCF routing (existing `framework_archetype_mapping.yaml`).

---

## 7. Acceptance Criteria

- [ ] **AC1 (Schema Rejection):** Submit a PrimitiveCandidate with `evidence_quote: "Most people agree"`. Assert: Pydantic `field_validator` raises ValueError. Candidate rejected.
- [ ] **AC2 (Anti-Centroid Gate):** Submit 4 candidates all with `emotional_charge: 0.2`. Assert: Dichotomy Gate rejects with `CENTROID_DRIFT_DETECTED`. Fallback coalition loaded.
- [ ] **AC3 (DSPy Retry):** First DSPy call returns a candidate with `tribal_density: "high"` (string, not float). Assert: DSPy retries with correction. If retry produces valid float, candidate accepted.
- [ ] **AC4 (Fallback Mechanism):** Dichotomy Gate rejects current extraction. Assert: Last validated coalition for this coach is loaded from `coalition_history`. Pipeline continues with fallback. `validation_status: fallback_used` logged.
- [ ] **AC5 (Coalition Minimum):** DSPy returns only 1 valid candidate after filtering. Assert: Coalition Engine rejects — minimum 2 candidates required. Fallback loaded.
- [ ] **AC6 (Fatality Logging):** Published content from a coalition gets 45% below the 8-week rolling average. Assert: `coalition_fatalities` record created with `delta_percentage: -45`. Diagnosis generated.
- [ ] **AC7 (Edge Product Routing):** Coalition with dominant primitive YAML ID `PRM-TNS-001`. Assert: `edge_product_type: "transformation-pressure-edge"`. `ccf_routing_target` maps to the correct CCF archetype.
<!-- UPDATED: Added Acceptance Criteria for Dual-Source Validation -->
- [ ] **AC8 (Dual-Source Validation):** A primitive is referenced by its generic family name without a specific YAML ID or the YAML constraint validation fails. Assert: The Dichotomy Gate rejects the primitive and raises a `DualSourceValidationError`.

---

## 8. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| DSPy | External | Structured LLM calls with typed outputs. |
| Pydantic v2 | Library | Schema validation with strict mode. |
| FR14 (CRAL Research) | Upstream | Provides research context for primitive extraction. |
| FR24 (Weekly Pipeline) | Downstream | Consumes validated Edge Products. |
| FR43 (Data Analyst Agent) | Downstream | Provides post-publication performance data for fatality detection. |
| `framework_archetype_mapping.yaml` | Internal | CCF routing targets. |

---

## 9. Failure Examples (Anti-Drafting)

**Failure Example 1: LLM Output Directly in Pipeline**
If DSPy output is forwarded to CCF without Pydantic validation, the LLM could generate a `PrimitiveCandidate` with `evidence_quote: ""` (empty string). The CCF generates a script with no grounding. The coach's output is AI slop with no connection to their real words. **Every LLM output MUST cross the Dichotomy Gate.**

**Failure Example 2: Retry with Looser Schema**
If validation fails and the system retries with `emotional_charge: Optional[float] = 0.5` (making the field optional with a default), the LLM learns it can skip difficult fields. Over time, all outputs converge to defaults — centroid drift. **Schema strictness NEVER decreases on retry. The retry prompt gets more specific; the schema stays identical.**

**Failure Example 3: No Fatality Memory**
If the system never logs coalition failures, it keeps producing the same failed combinations. A tribal reference that resonated 6 months ago but now falls flat gets reused indefinitely. **Fatalities must be logged and surfaced during future coalition assembly.**

<!-- UPDATED: Added Failure Example for ADR-05 violation -->
**Failure Example 4: ADR-05 Family Name Fallback**
If the orchestration pipeline allows "STR" (Narrative Structure) to be selected instead of an explicit ID like "PRM-STR-008", the system loses its deterministic footing. The CCF script generator won't know which structural primitive to apply, resulting in generic "storytelling" rather than a mathematically constrained narrative operation. **Every primitive must be invoked by its specific YAML ID.**

