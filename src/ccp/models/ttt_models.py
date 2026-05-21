"""
CCP FR8 TTT Enforcement Rule — Data Models (Unit 1)
Pydantic v2 models for the C-08 TTT Enforcement Gate and TTT runtime resolution.

Spec reference: FR8_TTT_Enforcement_Rule_Tech_Spec.md
Architecture reference: §JIT Skill Assembler v2.0 Tier 0 pre-flight,
                        §Script_Generation_Skill_Type_Guide_v1.0 §M-02

DEP-ENG-005: Authentication Certificate (TTT Baseline) — PRIMARY RUNTIME SOURCE
  ttt_baseline.json is consumed by the JIT Assembler Tier 1 (authentication adapter)
  and validated post-generation by Sophia.

Scale: TTT-01 (minimal) → TTT-10 (maximum emotional intensity)

Tone classification registry (Spec §Layer 3 runtime resolution):
  REFLECTIVE, CONFRONTATIONAL, NURTURING, INSTRUCTIONAL (4 primary registers)
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


# ─── Enums ────────────────────────────────────────────────────────────────────

class C08ViolationType(str, Enum):
    """C-08 rejection diagnostic violation type codes.

    Spec §Detection Algorithm:
      TTT_HARDCODED_IN_BLOCK_B — field name matched TTT_FIELD_PATTERNS
      TTT_VALUE_EMBEDDED_IN_BLOCK_B — value string matched TTT_VALUE_PATTERNS
      TTT_DIRECTIVE_IN_BLOCK_A — structural law in Block A is a TTT directive
    """
    HARDCODED_IN_BLOCK_B = "TTT_HARDCODED_IN_BLOCK_B"
    VALUE_EMBEDDED_IN_BLOCK_B = "TTT_VALUE_EMBEDDED_IN_BLOCK_B"
    DIRECTIVE_IN_BLOCK_A = "TTT_DIRECTIVE_IN_BLOCK_A"


class C08Status(str, Enum):
    """C-08 check result status."""
    PASS = "TTT_ENFORCEMENT_CLEAN"
    FAIL = "REJECT"


class ToneRegister(str, Enum):
    """Vocal register classifications for Tone component of TTT.

    Spec §Layer 3: tone = vocal register classification from semantic analysis.
    """
    REFLECTIVE = "reflective"
    CONFRONTATIONAL = "confrontational"
    NURTURING = "nurturing"
    INSTRUCTIONAL = "instructional"
    DECLARATIVE = "declarative"
    QUESTIONING = "questioning"
    CELEBRATORY = "celebratory"
    GRIEVING = "grieving"


class TextureQuality(str, Enum):
    """Texture classifications for TTT — stylistic surface quality.

    Spec: Raw/unpolished ↔ Crafted/literary
    """
    RAW = "raw"
    COLLOQUIAL = "colloquial"
    CONVERSATIONAL = "conversational"
    POLISHED = "polished"
    LITERARY = "literary"


class SophiaDriftVerdict(str, Enum):
    """Sophia post-generation TTT validation verdict."""
    PASS = "PASS"
    DRIFT_EXCEEDED = "DRIFT_EXCEEDED"
    SIMILARITY_FAILED = "SIMILARITY_FAILED"
    FLAT_EMOTIONAL_ARC = "FLAT_EMOTIONAL_ARC"


# ─── C-08 Detection Models ────────────────────────────────────────────────────

class TTTViolation(BaseModel):
    """Structured C-08 violation record.

    Spec §Detection Algorithm — REJECT payload structure.
    """
    check: str = Field(default="C-08", description="The JIT assembler check that detected this violation.")
    violation_type: C08ViolationType = Field(
        description="The type of TTT violation detected."
    )
    violating_field: str = Field(
        description="The full dotted field path that contains the violation."
    )
    violating_value: Optional[str] = Field(
        default=None,
        description="The actual field value or substring that matched a TTT pattern.",
    )
    matched_pattern: Optional[str] = Field(
        default=None,
        description="The regex or field-name pattern that triggered detection.",
    )
    mandate_violated: str = Field(
        default="M-02",
        description="The Script Generation Skill Type Guide mandate violated.",
    )
    recovery_instruction: str = Field(
        description=(
            "Human-readable instruction for the template author to correct the violation. "
            "Must identify the exact field and resolution path."
        )
    )
    pipeline_impact: str = Field(
        default=(
            "Full compilation halted. Zero tokens consumed. "
            "No assembly began."
        ),
        description="Impact statement confirming the zero-token guarantee (AC6).",
    )


class C08Result(BaseModel):
    """Result of the C-08 TTT Enforcement check.

    Spec §Check definition:
    Pass condition: No hardcoded TTT value in any Block B field.
    Failure: REJECT — TTT is never a compilation variable.
    """
    status: C08Status = Field(description="PASS or REJECT status of C-08.")
    violations: list[TTTViolation] = Field(
        default_factory=list,
        description="List of detected violations. Empty if status=PASS.",
    )
    tokens_consumed: int = Field(
        default=0,
        description="Must always be 0 — C-08 is a zero-token Tier 0 check (AC6).",
    )
    adapter_invocations: int = Field(
        default=0,
        description="Must always be 0 — no adapters are invoked on REJECT (AC6).",
    )
    section_assemblies: int = Field(
        default=0,
        description="Must always be 0 — no assembly begins on REJECT (AC6).",
    )
    compilation_id: Optional[str] = Field(
        default=None,
        description="The JIT compilation ID being checked.",
    )

    @property
    def passed(self) -> bool:
        """True if C-08 passed with no violations."""
        return self.status == C08Status.PASS

    @property
    def first_violation(self) -> Optional[TTTViolation]:
        """First detected violation, or None if status is PASS."""
        return self.violations[0] if self.violations else None


# ─── Block Field Models ───────────────────────────────────────────────────────

class BlockBField(BaseModel):
    """A single Block B field in a compiled Design Brief.

    Spec §Detection Algorithm — the scanner iterates over compiled_brief.block_b fields.
    """
    name: str = Field(description="Field name (dotted path for nested fields).")
    value: Any = Field(default=None, description="Field value — may be scalar or nested dict.")
    context: Optional[str] = Field(
        default=None,
        description="Optional context tag. Used by Phase 3 to classify Block A advisory references.",
    )

    def all_string_values(self) -> list[str]:
        """Extract all string values from this field (handles scalar and nested dicts)."""
        results: list[str] = []
        self._extract_strings(self.value, results)
        return results

    def _extract_strings(self, value: Any, out: list[str]) -> None:
        """Recursively extract string values from any nested structure."""
        if isinstance(value, str):
            out.append(value)
        elif isinstance(value, dict):
            for v in value.values():
                self._extract_strings(v, out)
        elif isinstance(value, list):
            for item in value:
                self._extract_strings(item, out)


class BlockALaw(BaseModel):
    """A single structural law from Block A of a compiled Design Brief.

    Spec §Phase 3: Block A structural laws are scanned for TTT directives.
    Natural affinity range advisories are permitted; directives are not.
    """
    law_id: str = Field(description="Unique identifier for this structural law (e.g., 'law_01').")
    text: str = Field(description="Full text of the structural law.")
    context: Optional[str] = Field(
        default=None,
        description="Classification context. 'natural_affinity_range_advisory' = PERMITTED.",
    )

    @property
    def is_affinity_advisory(self) -> bool:
        """True if this law is classified as a natural affinity range advisory."""
        return self.context == "natural_affinity_range_advisory"


class CompiledDesignBrief(BaseModel):
    """The compiled Design Brief passed to C-08 for TTT scanning.

    Represents the output of the JIT Skill Assembler's template compilation,
    before any assembly begins (Tier 0 pre-flight input).
    """
    compilation_id: str = Field(description="Unique JIT compilation ID.")
    archetype_id: str = Field(description="The content archetype being compiled.")
    block_b_fields: list[BlockBField] = Field(
        default_factory=list,
        description="All Block B fields from the compiled brief.",
    )
    block_a_structural_laws: list[BlockALaw] = Field(
        default_factory=list,
        description="All Block A structural laws.",
    )
    dep_eng_005_reference: Optional[str] = Field(
        default=None,
        description="DEP-ENG-005 reference field value (should be present in compliant briefs).",
    )


# ─── TTT Baseline / DEP-ENG-005 Models ───────────────────────────────────────

class TTTBaselineData(BaseModel):
    """DEP-ENG-005 Authentication Certificate — TTT extraction output.

    Spec §Layer 3 Runtime Resolution:
    - Temperature (TTT-01 to TTT-10): emotional intensity from vocal markers
    - Texture: stylistic surface quality from linguistic analysis
    - Tone: vocal register classification from semantic analysis

    Written to: config/ttt_baseline.json
    """
    temperature: int = Field(
        ge=1, le=10,
        description="Emotional intensity on a 1-10 scale (TTT-01 to TTT-10).",
    )
    texture: TextureQuality = Field(
        description="Stylistic surface quality of the session voice note.",
    )
    tone: ToneRegister = Field(
        description="Vocal register classification of the authenticated state.",
    )
    liwc_authenticity_score: float = Field(
        ge=0.0, le=10.0,
        description="LIWC-22 authenticity score from voice note validation. Must be ≥7.0 (AC7).",
    )
    session_id: str = Field(description="The production session ID this TTT baseline belongs to.")
    coach_id: str = Field(description="Coach person ID.")
    extraction_timestamp: str = Field(
        description="ISO-8601 timestamp of extraction from voice note.",
    )
    voice_note_hash: str = Field(
        description="SHA-256 hash of the processed voice note for audit trail.",
    )
    liwc_authenticated: bool = Field(
        default=False,
        description="True when liwc_authenticity_score ≥ 7.0 (AC7 gate: score ≥ 7/10).",
    )
    raw_temperature_reading: Optional[float] = Field(
        default=None,
        description="Raw extracted temperature before integer rounding.",
    )

    @model_validator(mode="before")
    @classmethod
    def derive_authenticated_flag(cls, data: Any) -> Any:
        """If not explicitly set, derive from liwc_authenticity_score."""
        if isinstance(data, dict):
            score = data.get("liwc_authenticity_score", 0.0)
            if "liwc_authenticated" not in data:
                data["liwc_authenticated"] = score >= 7.0
        return data


# ─── Affinity Range Models ────────────────────────────────────────────────────

class TTTAffinityRange(BaseModel):
    """Natural affinity range for a content archetype.

    Spec §TTT natural affinity range (advisory system):
    Each archetype has a temperature range where it naturally performs best.
    ADVISORY ONLY — coach's authenticated state always overrides (AC8).
    """
    archetype_id: str = Field(description="Content archetype identifier.")
    min_temperature: int = Field(ge=1, le=10, description="Lower bound of affinity range.")
    max_temperature: int = Field(ge=1, le=10, description="Upper bound of affinity range.")
    human_review_flag_threshold: Optional[int] = Field(
        default=None,
        description="Temperature above which human review flag is triggered (e.g., TTT ≥ 8).",
    )
    rationale: str = Field(
        description="Why this archetype performs best in this temperature range.",
    )


class AffinityRangeResult(BaseModel):
    """Result of advisory affinity range check for a specific production session.

    AC8: outside range → log ttt_outside_affinity_range=True, flag for human review,
    compilation PROCEEDS.
    """
    archetype_id: str
    coach_temperature: int = Field(ge=1, le=10)
    affinity_min: int = Field(ge=1, le=10)
    affinity_max: int = Field(ge=1, le=10)
    ttt_outside_affinity_range: bool = Field(
        description="True if coach's authenticated temperature is outside the archetype's affinity range.",
    )
    requires_human_review: bool = Field(
        default=False,
        description="True if temperature triggers the human review flag threshold.",
    )
    compilation_blocked: bool = Field(
        default=False,
        description="Must ALWAYS be False — affinity range is advisory only (AC8).",
    )
    advisory_note: Optional[str] = Field(
        default=None,
        description="Human-readable advisory note logged to orchestrator.",
    )


# ─── Sophia Post-Generation Validation Models ─────────────────────────────────

class EmotionalPeak(BaseModel):
    """A detected emotional intensity peak within generated content.

    Spec §Layer 4 iRAV-inspired peak detection:
    ≥1 peak per script must exceed the average by ≥20%.
    """
    position_index: int = Field(description="Position index in the generated content.")
    intensity: float = Field(ge=0.0, le=1.0, description="Normalized emotional intensity (0.0-1.0).")
    content_segment: Optional[str] = Field(
        default=None,
        description="The content segment where the peak was detected.",
    )


class SophiaTTTValidationResult(BaseModel):
    """Sophia (Minister of Identity) post-generation TTT validation result.

    Spec §Layer 4 Post-Generation Verification:
    - TTT drift < 15% from DEP-ENG-005 baseline
    - iRAV-inspired ≥1 emotional peak exceeding average by ≥20%
    - Cosine similarity ≥ 0.85 against ttt_baseline.json

    Model Offset Calibration: Sophia applies model offset before drift calculation.
    E.g., Groq: -0.12 offset applied to baseline before threshold check.
    """
    verdict: SophiaDriftVerdict = Field(description="Overall Sophia TTT validation verdict.")
    compilation_id: str = Field(description="The JIT compilation ID validated.")
    session_id: str = Field(description="The production session ID.")

    # Drift check
    ttt_drift_percentage: float = Field(
        ge=0.0,
        description="Calculated TTT drift from DEP-ENG-005 baseline (after model offset applied).",
    )
    drift_threshold: float = Field(
        default=0.15,
        description="Maximum allowed drift (15%).",
    )
    drift_passed: bool = Field(description="True if ttt_drift_percentage < drift_threshold.")

    # Cosine similarity check
    cosine_similarity: float = Field(
        ge=0.0, le=1.0,
        description="Cosine similarity of generated content TTT markers vs ttt_baseline.json.",
    )
    similarity_threshold: float = Field(
        default=0.85,
        description="Minimum required cosine similarity (0.85).",
    )
    similarity_passed: bool = Field(description="True if cosine_similarity ≥ similarity_threshold.")

    # iRAV peak check
    emotional_peaks: list[EmotionalPeak] = Field(
        default_factory=list,
        description="Detected emotional peaks in the generated content.",
    )
    average_intensity: float = Field(
        ge=0.0, le=1.0,
        description="Average emotional intensity of the generated content.",
    )
    peaks_passed: bool = Field(
        description="True if ≥1 peak exceeds average by ≥20% (iRAV-inspired AC10).",
    )
    peak_threshold_pct: float = Field(
        default=0.20,
        description="Required exceedance above average (20%).",
    )

    # Model offset calibration
    model_id: Optional[str] = Field(
        default=None,
        description="Executing LLM model ID. Used to look up offset in Global Model Offset Registry.",
    )
    model_offset_applied: float = Field(
        default=0.0,
        description="Model temperature offset applied to baseline before drift calculation. E.g., -0.12 for Groq.",
    )


# ─── Assembly Report Models ───────────────────────────────────────────────────

class AssemblyReportC08Section(BaseModel):
    """C-08 section of assembly_report.json.

    Spec §Diagnostic output on C-08 failure.
    """
    status: str = Field(description="'PASS' or 'FAIL'.")
    violation_type: Optional[str] = Field(default=None)
    violating_field: Optional[str] = Field(default=None)
    violating_value: Optional[str] = Field(default=None)
    mandate_violated: Optional[str] = Field(default=None)
    recovery_instruction: Optional[str] = Field(default=None)
    pipeline_impact: Optional[str] = Field(default=None)
    tokens_consumed: int = Field(default=0)
    adapter_invocations: int = Field(default=0)
    section_assemblies: int = Field(default=0)


class AssemblyReport(BaseModel):
    """assembly_report.json — JIT Skill Assembler diagnostic output.

    Written to: assembly_report.json (per-compilation)
    Contains: deployment_status, tier_0_pre_flight results including C-08.
    """
    compilation_id: str
    template_id: Optional[str] = Field(default=None)
    archetype_id: Optional[str] = Field(default=None)
    deployment_status: str = Field(
        description="'ACCEPTED' if all checks pass, 'REJECTED' if any Tier 0 check fails.",
    )
    tier_0_pre_flight: dict[str, Any] = Field(
        default_factory=dict,
        description="Full Tier 0 check results keyed by check name.",
    )
    sophia_ttt_validation: Optional[SophiaTTTValidationResult] = Field(
        default=None,
        description="Sophia post-generation TTT validation. Only present for accepted compilations.",
    )
    pipeline_interruption_log: Optional[dict[str, Any]] = Field(
        default=None,
        description=(
            "AC11: When C-08 rejects, records template_id, violated_field, recovery_instruction. "
            "Traceable to specific template for correction."
        ),
    )
