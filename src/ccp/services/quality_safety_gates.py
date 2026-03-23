"""
CCP Step 11 — Quality & Safety Gate Service (FR16)

Implements FR16 Gate 1 (Safety) and Gate 2 (Authenticity).

Architecture reference:
    FR16_Human_Evidence_Bias_Gate_Tech_Spec.md §§2, 3
    CCP_Evolution_Architecture_Report_V4

Gate 1 (Safety):
    Agent: Gate-1-Safety-Agent
    Outcome: PASS | FAIL_TERMINAL (non-recoverable halt)
    Checks: self-harm, hate speech, severe psychological distress triggers.

Gate 2 (Authenticity):
    Agent: Gate-2-Authenticity-Agent
    Outcome: PASS | FAIL_REGENERATE (loops back to content generator)
    Checks: biological authentic markers vs LLM statistical-average language.

FR16 AC1: Content with >0 FAIL_TERMINAL flags → pipeline halted, receipt written.
FR16 AC2: Content with majority LLM-average markers → FAIL_REGENERATE, not FAIL_TERMINAL.

ADR-01: coach_id scopes all operations.
"""

from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING, Optional

from src.ccp.models.quality_safety_gate_models import (
    AuthenticitySignal,
    AuthenticitySignalType,
    Gate1SafetyResult,
    Gate1TerminalError,
    Gate1Verdict,
    Gate2AuthenticityResult,
    Gate2Verdict,
    QualitySafetyGateReport,
    SafetyFlag,
    SafetyFlagCategory,
)

if TYPE_CHECKING:
    from src.ccp.core.receipt_chain import ReceiptChain

logger = logging.getLogger(__name__)

# ── Stage names ───────────────────────────────────────────────────────────────

STAGE_1_GATE_1_NAME = "PHASE-1-GATE-1-SAFETY"
STAGE_2_GATE_2_NAME = "PHASE-2-GATE-2-AUTHENTICITY"
GATE_1_AGENT_ID = "Gate-1-Safety-Agent"
GATE_2_AGENT_ID = "Gate-2-Authenticity-Agent"

# ── Gate 1: Safety keyword banks ─────────────────────────────────────────────
# Minimal heuristic banks — in production these feed an LLM classifier.

_SELF_HARM_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\b(kill myself|end my life|suicide|self.?harm|cut myself)\b", re.IGNORECASE),
    re.compile(r"\b(worthless|no reason to live|want to die)\b", re.IGNORECASE),
]

_HATE_SPEECH_PATTERNS: list[re.Pattern[str]] = [
    re.compile(
        r"\b(all \w+ are|those people deserve|inferior race|subhuman)\b",
        re.IGNORECASE,
    ),
]

_SEVERE_DISTRESS_PATTERNS: list[re.Pattern[str]] = [
    re.compile(
        r"\b(psychiatric crisis|severe trauma|PTSD|psychotic break|suicidal ideation)\b",
        re.IGNORECASE,
    ),
]

# ── Gate 2: Authenticity heuristic patterns ───────────────────────────────────

# Negative patterns (LLM-average)
_GENERIC_STATEMENT_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\bin (today's|our modern|the current) (world|society|landscape)\b", re.IGNORECASE),
    re.compile(r"\bit (is|was) (important|crucial|vital|essential) to\b", re.IGNORECASE),
    re.compile(r"\b(many people|a lot of people|individuals) (feel|experience|struggle)\b", re.IGNORECASE),
    re.compile(r"\bstatistics show that\b", re.IGNORECASE),
    re.compile(r"\bstudies have shown\b", re.IGNORECASE),
    re.compile(r"\bthe fact of the matter is\b", re.IGNORECASE),
]

_HEDGING_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\b(it could be argued|one might say|in some ways|arguably)\b", re.IGNORECASE),
    re.compile(r"\b(perhaps|maybe|possibly) (this|that|it) (could|might|may)\b", re.IGNORECASE),
]

# Positive patterns (authentic markers)
_PERSONAL_ANECDOTE_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\b(I|I've|I was|I had|I remember|I told|I asked|I watched)\b"),
    re.compile(r"\b(my client|my student|she told me|he said|they said)\b", re.IGNORECASE),
]

_SPECIFIC_PERSON_PATTERNS: list[re.Pattern[str]] = [
    # Capitalized first+last name (simple heuristic)
    re.compile(r"\b[A-Z][a-z]+ [A-Z][a-z]+\b"),
]

_VERNACULAR_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\b(hustle|grind|vibe|lowkey|literally|honestly|real talk|ngl)\b", re.IGNORECASE),
]

_EMOTIONAL_SPECIFICITY_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\b(furious|terrified|devastated|elated|gutted|ashamed|proud)\b", re.IGNORECASE),
    re.compile(r"\b(three months|six weeks|that Tuesday|last summer|that morning)\b", re.IGNORECASE),
]

# Authenticity ratio threshold: >= 0.60 → PASS
AUTHENTICITY_RATIO_THRESHOLD: float = 0.60


class QualitySafetyGateService:
    """FR16 Quality & Safety Gate Service.

    Runs Gate 1 (Safety) and Gate 2 (Authenticity) on pipeline content.
    Both gates write to the ReceiptChain on every evaluation.

    ADR-01: coach_id scopes all gate records.

    Args:
        coach_id: 3-char coach acronym.
        receipt_chain: Optional ReceiptChain for cryptographic audit.
    """

    def __init__(
        self,
        coach_id: str,
        receipt_chain: Optional["ReceiptChain"] = None,
    ) -> None:
        if len(coach_id) != 3:
            raise ValueError(f"coach_id must be 3 characters, got '{coach_id}'")
        self.coach_id = coach_id.upper()
        self.receipt_chain = receipt_chain

    # ── Gate 1 ────────────────────────────────────────────────────────────────

    def run_gate_1_safety(
        self,
        content: str,
        payload_id: str = "",
    ) -> Gate1SafetyResult:
        """FR16 §Gate 1: Safety check on pipeline content.

        FR16 AC1: Any content with self-harm / hate speech / severe distress
        patterns → Gate1Verdict.FAIL_TERMINAL.

        The result is written to ReceiptChain regardless of verdict.
        Callers SHOULD check result.is_terminal_halt and halt if True.
        Use run_gate_1_safety_raising() to get an automatic exception.

        Args:
            content: The pipeline content payload text to evaluate.
            payload_id: Identifier for the content payload.

        Returns:
            Gate1SafetyResult with verdict PASS or FAIL_TERMINAL.
        """
        flags: list[SafetyFlag] = []
        words = content.split()
        word_count = len(words)

        # Self-harm scan
        for pattern in _SELF_HARM_PATTERNS:
            for match in pattern.finditer(content):
                flags.append(SafetyFlag(
                    category=SafetyFlagCategory.SELF_HARM,
                    excerpt=match.group()[:80],
                    severity="CRITICAL",
                    details="Self-harm language detected in pipeline content.",
                ))
                break  # one flag per category type

        # Hate speech scan
        for pattern in _HATE_SPEECH_PATTERNS:
            for match in pattern.finditer(content):
                flags.append(SafetyFlag(
                    category=SafetyFlagCategory.HATE_SPEECH,
                    excerpt=match.group()[:80],
                    severity="CRITICAL",
                    details="Hate speech pattern detected.",
                ))
                break

        # Severe psychological distress scan
        for pattern in _SEVERE_DISTRESS_PATTERNS:
            for match in pattern.finditer(content):
                flags.append(SafetyFlag(
                    category=SafetyFlagCategory.SEVERE_PSYCHOLOGICAL_DISTRESS,
                    excerpt=match.group()[:80],
                    severity="HIGH",
                    details="Severe psychological distress marker detected.",
                ))
                break

        verdict = Gate1Verdict.FAIL_TERMINAL if flags else Gate1Verdict.PASS

        result = Gate1SafetyResult(
            coach_id=self.coach_id,
            payload_id=payload_id,
            verdict=verdict,
            flags=flags,
            evaluated_content_length=word_count,
        )

        if self.receipt_chain:
            self.receipt_chain.log(
                agent_id=GATE_1_AGENT_ID,
                action=STAGE_1_GATE_1_NAME,
                input_summary=f"payload_id={payload_id} words={word_count}",
                output_summary=f"verdict={verdict.value} flags={len(flags)}",
                decision=verdict.value,
                decision_rationale=(
                    f"Safety flags: {[f.category.value for f in flags]}"
                    if flags else "No safety violations detected."
                ),
            )

        return result

    def run_gate_1_safety_raising(
        self,
        content: str,
        payload_id: str = "",
    ) -> Gate1SafetyResult:
        """Run Gate 1 and raise Gate1TerminalError on FAIL_TERMINAL.

        FR16: Pipeline MUST halt on FAIL_TERMINAL. Use this variant when
        you want automatic exception propagation.

        Raises:
            Gate1TerminalError: If verdict is FAIL_TERMINAL.
        """
        result = self.run_gate_1_safety(content, payload_id)
        if result.is_terminal_halt:
            raise Gate1TerminalError(result)
        return result

    # ── Gate 2 ────────────────────────────────────────────────────────────────

    def run_gate_2_authenticity(
        self,
        content: str,
        payload_id: str = "",
    ) -> Gate2AuthenticityResult:
        """FR16 §Gate 2: Authenticity check on pipeline content.

        FR16 AC2: Majority LLM-average language → Gate2Verdict.FAIL_REGENERATE.
        Returns content to generator for rewrite — does NOT halt the pipeline.

        Evaluates:
        - Generic statements, hedging language → inauthentic (negative)
        - Personal anecdotes, specific named people, vernacular, emotional
          specificity → authentic (positive)

        Args:
            content: The pipeline content payload text to evaluate.
            payload_id: Identifier for the content payload.

        Returns:
            Gate2AuthenticityResult with verdict PASS or FAIL_REGENERATE.
        """
        signals: list[AuthenticitySignal] = []

        # Negative signals — LLM statistical average
        for pattern in _GENERIC_STATEMENT_PATTERNS:
            if pattern.search(content):
                signals.append(AuthenticitySignal(
                    signal_type=AuthenticitySignalType.GENERIC_STATEMENT,
                    is_authentic=False,
                    excerpt=str(pattern.search(content).group())[:80],  # type: ignore[union-attr]
                ))

        for pattern in _HEDGING_PATTERNS:
            if pattern.search(content):
                signals.append(AuthenticitySignal(
                    signal_type=AuthenticitySignalType.HEDGING_LANGUAGE,
                    is_authentic=False,
                    excerpt=str(pattern.search(content).group())[:80],  # type: ignore[union-attr]
                ))

        # Positive signals — biologically authentic markers
        for pattern in _PERSONAL_ANECDOTE_PATTERNS:
            if pattern.search(content):
                signals.append(AuthenticitySignal(
                    signal_type=AuthenticitySignalType.PERSONAL_ANECDOTE,
                    is_authentic=True,
                    excerpt=str(pattern.search(content).group())[:80],  # type: ignore[union-attr]
                ))
                break  # count once per type

        for pattern in _SPECIFIC_PERSON_PATTERNS:
            if pattern.search(content):
                signals.append(AuthenticitySignal(
                    signal_type=AuthenticitySignalType.SPECIFIC_NAMED_PERSON,
                    is_authentic=True,
                    excerpt=str(pattern.search(content).group())[:80],  # type: ignore[union-attr]
                ))
                break

        for pattern in _VERNACULAR_PATTERNS:
            if pattern.search(content):
                signals.append(AuthenticitySignal(
                    signal_type=AuthenticitySignalType.VERNACULAR_LANGUAGE,
                    is_authentic=True,
                    excerpt=str(pattern.search(content).group())[:80],  # type: ignore[union-attr]
                ))
                break

        for pattern in _EMOTIONAL_SPECIFICITY_PATTERNS:
            if pattern.search(content):
                signals.append(AuthenticitySignal(
                    signal_type=AuthenticitySignalType.EMOTIONAL_SPECIFICITY,
                    is_authentic=True,
                    excerpt=str(pattern.search(content).group())[:80],  # type: ignore[union-attr]
                ))
                break

        # Derive verdict
        authentic_count = sum(1 for s in signals if s.is_authentic)
        total = len(signals)
        ratio = (authentic_count / total) if total > 0 else 0.0

        # If no signals detected at all, treat as borderline authentic (PASS)
        if total == 0:
            verdict = Gate2Verdict.PASS
            regeneration_guidance = ""
        elif ratio >= AUTHENTICITY_RATIO_THRESHOLD:
            verdict = Gate2Verdict.PASS
            regeneration_guidance = ""
        else:
            verdict = Gate2Verdict.FAIL_REGENERATE
            regeneration_guidance = (
                "Content contains too many generic/hedging statements. "
                "Rewrite using specific named individuals, personal anecdotes, "
                "precise dates/contexts, and vernacular language native to the tribe. "
                f"Authenticity ratio: {ratio:.2f} (threshold: {AUTHENTICITY_RATIO_THRESHOLD})."
            )

        result = Gate2AuthenticityResult(
            coach_id=self.coach_id,
            payload_id=payload_id,
            verdict=verdict,
            signals=signals,
            authenticity_ratio=ratio,
            regeneration_guidance=regeneration_guidance,
        )

        if self.receipt_chain:
            self.receipt_chain.log(
                agent_id=GATE_2_AGENT_ID,
                action=STAGE_2_GATE_2_NAME,
                input_summary=f"payload_id={payload_id} words={len(content.split())}",
                output_summary=(
                    f"verdict={verdict.value} authentic={authentic_count}/{total} "
                    f"ratio={ratio:.2f}"
                ),
                decision=verdict.value,
                decision_rationale=(
                    regeneration_guidance or "Authenticity ratio above threshold."
                ),
            )

        return result

    # ── Combined Pipeline ─────────────────────────────────────────────────────

    def run_both_gates(
        self,
        content: str,
        payload_id: str = "",
        raise_on_terminal: bool = False,
    ) -> QualitySafetyGateReport:
        """Run Gate 1 then Gate 2 and return a combined report.

        Gate 2 is skipped if Gate 1 results in FAIL_TERMINAL (no point
        checking authenticity on halted content).

        Args:
            content: The pipeline content payload text.
            payload_id: Identifier for the content payload.
            raise_on_terminal: If True, raise Gate1TerminalError on FAIL_TERMINAL.

        Returns:
            QualitySafetyGateReport with gate_1_result and gate_2_result.

        Raises:
            Gate1TerminalError: If raise_on_terminal=True and Gate 1 fails.
        """
        # Gate 1 first
        gate_1_result = self.run_gate_1_safety(content, payload_id)

        if gate_1_result.is_terminal_halt:
            if raise_on_terminal:
                raise Gate1TerminalError(gate_1_result)
            # Skip Gate 2 on terminal halt
            return QualitySafetyGateReport(
                coach_id=self.coach_id,
                payload_id=payload_id,
                gate_1_result=gate_1_result,
                gate_2_result=None,
            )

        # Gate 2
        gate_2_result = self.run_gate_2_authenticity(content, payload_id)

        return QualitySafetyGateReport(
            coach_id=self.coach_id,
            payload_id=payload_id,
            gate_1_result=gate_1_result,
            gate_2_result=gate_2_result,
        )
