"""
CCP Step 11 — Quality & Safety Gate Models (FR16)

Pydantic v2 models for FR16 Gate 1 (Safety) and Gate 2 (Authenticity).

FR16 §Architectural Pointer: Gate 3 (Human Evidence Bias) logic is owned
exclusively by FR14 (CRAL Research Subsystem). FR16 owns ONLY:
  - Gate 1: Safety (self-harm, hate speech, severe psychological distress)
  - Gate 2: Authenticity (biological markers vs LLM statistical averages)

Architecture reference:
    FR16_Human_Evidence_Bias_Gate_Tech_Spec.md §§2, 3
    CCP_Evolution_Architecture_Report_V4

Models defined:
    Gate1Verdict — PASS | FAIL_TERMINAL
    Gate2Verdict — PASS | FAIL_REGENERATE
    SafetyFlagCategory — classification of safety violations
    Gate1SafetyResult — Full Gate 1 evaluation result
    AuthenticitySignal — Evidence of authentic vs LLM-average language
    Gate2AuthenticityResult — Full Gate 2 evaluation result
    QualitySafetyGateReport — Combined Gate 1+2 report per pipeline payload

Critical constraints:
    - Gate 1 FAIL_TERMINAL: pipeline HALTED, no bypass, no regeneration.
    - Gate 2 FAIL_REGENERATE: pipeline returns to content generator for rewrite.
    - Both gates write to ReceiptChain on every evaluation.
    - ADR-01: coach_id scopes all gate records.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


# ─── Gate 1 ───────────────────────────────────────────────────────────────────

class Gate1Verdict(str, Enum):
    """FR16 §Gate 1 outcome.

    PASS → content cleared, proceed downstream.
    FAIL_TERMINAL → pipeline HALTED. No bypass. No regeneration.
    """
    PASS = "PASS"
    FAIL_TERMINAL = "FAIL_TERMINAL"


class SafetyFlagCategory(str, Enum):
    """Classification of Gate 1 safety violations.

    FR16 §Gate 1: 'self-harm, hate speech, severe psychological distress
    thresholds.'
    """
    SELF_HARM = "SELF_HARM"
    HATE_SPEECH = "HATE_SPEECH"
    SEVERE_PSYCHOLOGICAL_DISTRESS = "SEVERE_PSYCHOLOGICAL_DISTRESS"
    DANGEROUS_MISINFORMATION = "DANGEROUS_MISINFORMATION"
    EXPLICIT_CONTENT = "EXPLICIT_CONTENT"


class SafetyFlag(BaseModel):
    """A single safety violation detected by Gate 1."""
    category: SafetyFlagCategory = Field(
        ...,
        description="Type of safety violation.",
    )
    excerpt: str = Field(
        default="",
        description="Offending text excerpt (truncated for log safety).",
    )
    severity: str = Field(
        default="HIGH",
        description="CRITICAL | HIGH | MEDIUM",
    )
    details: str = Field(
        default="",
        description="Human-readable description of the violation.",
    )


class Gate1SafetyResult(BaseModel):
    """FR16 §Gate 2 — Gate 1 Safety evaluation result.

    Agent Name: Gate-1-Safety-Agent
    Input: Pipeline Content Payload
    Output: PASS or FAIL_TERMINAL

    FAIL_TERMINAL means the pipeline is HALTED. This is non-negotiable.
    No regeneration is permitted after a Gate 1 failure.
    """
    coach_id: str = Field(
        ..., min_length=3, max_length=3,
        description="ADR-01 tenant isolation.",
    )
    payload_id: str = Field(
        default="",
        description="ID of the content payload evaluated.",
    )
    verdict: Gate1Verdict = Field(
        default=Gate1Verdict.PASS,
    )
    flags: list[SafetyFlag] = Field(
        default_factory=list,
        description="All safety violations detected.",
    )
    flag_count: int = Field(
        default=0,
        description="Auto-derived from flags list.",
    )
    is_terminal_halt: bool = Field(
        default=False,
        description="True when verdict == FAIL_TERMINAL. Pipeline must halt.",
    )
    receipt_hash: str = Field(default="")
    evaluated_content_length: int = Field(
        default=0,
        description="Word count of the evaluated content.",
    )

    def model_post_init(self, __context: Any) -> None:
        """Auto-derive flag_count and is_terminal_halt."""
        self.flag_count = len(self.flags)
        self.is_terminal_halt = (self.verdict == Gate1Verdict.FAIL_TERMINAL)


class Gate1TerminalError(Exception):
    """Raised when Gate 1 evaluates to FAIL_TERMINAL.

    The caller MUST catch this and halt the pipeline immediately.
    No bypass or regeneration path is permitted.
    """
    def __init__(self, result: Gate1SafetyResult) -> None:
        self.result = result
        categories = [f.category.value for f in result.flags]
        super().__init__(
            f"GATE-1-SAFETY FAIL_TERMINAL: coach_id={result.coach_id} "
            f"flags={categories}"
        )


# ─── Gate 2 ───────────────────────────────────────────────────────────────────

class Gate2Verdict(str, Enum):
    """FR16 §Gate 3 outcome.

    PASS → content cleared, proceed downstream.
    FAIL_REGENERATE → pipeline returns to content generator for rewrite.
    """
    PASS = "PASS"
    FAIL_REGENERATE = "FAIL_REGENERATE"


class AuthenticitySignalType(str, Enum):
    """Type of authenticity signal detected in content.

    FR16 §Gate 2: 'genuine, biologically authentic markers rather than
    sterile, LLM-generated averages or statistically dry summaries.'
    """
    # Positive signals (authentic)
    PERSONAL_ANECDOTE = "PERSONAL_ANECDOTE"
    SPECIFIC_NAMED_PERSON = "SPECIFIC_NAMED_PERSON"
    PRECISE_DATE_OR_CONTEXT = "PRECISE_DATE_OR_CONTEXT"
    VERNACULAR_LANGUAGE = "VERNACULAR_LANGUAGE"
    EMOTIONAL_SPECIFICITY = "EMOTIONAL_SPECIFICITY"
    # Negative signals (LLM statistical average)
    GENERIC_STATEMENT = "GENERIC_STATEMENT"
    ENCYCLOPEDIC_SUMMARY = "ENCYCLOPEDIC_SUMMARY"
    PASSIVE_VOICE_ABSTRACTION = "PASSIVE_VOICE_ABSTRACTION"
    CLICHE_PHRASE = "CLICHE_PHRASE"
    HEDGING_LANGUAGE = "HEDGING_LANGUAGE"


class AuthenticitySignal(BaseModel):
    """A single authenticity signal (positive or negative) detected in content."""
    signal_type: AuthenticitySignalType = Field(...)
    is_authentic: bool = Field(
        ...,
        description="True if signal is a positive authenticity marker.",
    )
    excerpt: str = Field(
        default="",
        description="Text excerpt that triggered this signal.",
    )


class Gate2AuthenticityResult(BaseModel):
    """FR16 §Gate 3 — Gate 2 Authenticity evaluation result.

    Agent Name: Gate-2-Authenticity-Agent
    Input: Evaluated Content Segment
    Output: PASS or FAIL_REGENERATE

    FAIL_REGENERATE returns the content to the generator for a rewrite.
    The pipeline does NOT halt — it loops back for regeneration.
    """
    coach_id: str = Field(
        ..., min_length=3, max_length=3,
        description="ADR-01 tenant isolation.",
    )
    payload_id: str = Field(
        default="",
        description="ID of the content payload evaluated.",
    )
    verdict: Gate2Verdict = Field(
        default=Gate2Verdict.PASS,
    )
    authentic_signal_count: int = Field(
        default=0,
        description="Number of positive authenticity markers detected.",
    )
    inauthentic_signal_count: int = Field(
        default=0,
        description="Number of negative (LLM-average) markers detected.",
    )
    signals: list[AuthenticitySignal] = Field(
        default_factory=list,
        description="All signals detected.",
    )
    authenticity_ratio: float = Field(
        default=0.0,
        description="authentic_signals / total_signals. >= 0.60 → PASS.",
    )
    requires_regeneration: bool = Field(
        default=False,
        description="True when verdict == FAIL_REGENERATE.",
    )
    regeneration_guidance: str = Field(
        default="",
        description="Guidance text for the generator on how to rewrite.",
    )
    receipt_hash: str = Field(default="")

    def model_post_init(self, __context: Any) -> None:
        """Auto-derive counts and requires_regeneration."""
        self.authentic_signal_count = sum(1 for s in self.signals if s.is_authentic)
        self.inauthentic_signal_count = sum(1 for s in self.signals if not s.is_authentic)
        total = len(self.signals)
        if total > 0:
            self.authenticity_ratio = self.authentic_signal_count / total
        self.requires_regeneration = (self.verdict == Gate2Verdict.FAIL_REGENERATE)


# ─── Combined Gate Report ──────────────────────────────────────────────────────

class QualitySafetyGateReport(BaseModel):
    """Combined Gate 1+2 report for a pipeline content payload.

    Written to the receipt chain after both gates have evaluated the payload.
    ADR-01: coach_id scopes the report.
    """
    coach_id: str = Field(
        ..., min_length=3, max_length=3,
        description="ADR-01 tenant isolation.",
    )
    payload_id: str = Field(
        default="",
        description="ID of the content payload evaluated.",
    )
    gate_1_result: Optional[Gate1SafetyResult] = Field(
        default=None,
        description="Gate 1 Safety result.",
    )
    gate_2_result: Optional[Gate2AuthenticityResult] = Field(
        default=None,
        description="Gate 2 Authenticity result.",
    )
    overall_pass: bool = Field(
        default=False,
        description="True only when Gate 1 PASS AND Gate 2 PASS.",
    )
    pipeline_halted: bool = Field(
        default=False,
        description="True if Gate 1 FAIL_TERMINAL was triggered.",
    )
    regeneration_required: bool = Field(
        default=False,
        description="True if Gate 2 FAIL_REGENERATE was triggered.",
    )
    receipt_chain_hash: str = Field(default="")

    def model_post_init(self, __context: Any) -> None:
        """Auto-derive overall_pass, pipeline_halted, regeneration_required."""
        g1_pass = (
            self.gate_1_result is not None
            and self.gate_1_result.verdict == Gate1Verdict.PASS
        )
        g2_pass = (
            self.gate_2_result is not None
            and self.gate_2_result.verdict == Gate2Verdict.PASS
        )
        self.overall_pass = g1_pass and g2_pass
        self.pipeline_halted = (
            self.gate_1_result is not None
            and self.gate_1_result.is_terminal_halt
        )
        self.regeneration_required = (
            self.gate_2_result is not None
            and self.gate_2_result.requires_regeneration
        )
