"""
CCP Step 8 — Research Synthesis Protocol / Builder Engine Step 3.5 (Unit 6)
Implements FR17: Deterministic conflict-detection pass between
DEP-ENG-021 (CRAL) and DEP-ENG-010 (SoC) / DEP-ENG-005 (Auth).

Architecture reference:
    FR17_Research_Synthesis_Protocol_Tech_Spec.md
    CCP_Evolution_Architecture_Report_V4 §4.2

Stages:
    1. Dependency Ingestion — skip if cral_coverage_status == ABSENT.
    2. Type 1 Conflict Pass — Source Proximity (M6 > M2, auto-resolve).
    3. Type 2 Conflict Pass — Structural Mismatch (M4 vs SoC, operator flag).
    4. Type 3 Conflict Pass — Authenticity (M6 vs DEP-ENG-005, terminal block).

FR17 AC1: M6 vs M2 hierarchy auto-resolve (M6 wins deterministically).
FR17 AC2: SoC voice vs CRAL narrative → FLAGGED_FOR_OPERATOR.
FR17 AC3: M6 vs DEP-ENG-005 authenticity → Terminal Block (NOT operator flag).
FR17 AC4: ABSENT CRAL → skip in < 20ms, log skip code.

ADR-01: coach_id scopes all operations.
FR17 Technical Decision 1: Deterministic resolution, NOT AI arbitration.
"""

from __future__ import annotations

import hashlib
import logging
import time
from typing import TYPE_CHECKING, Any, Optional

from src.ccp.models.adapter_registry_v2_models import CRALMomentKey
from src.ccp.models.research_synthesis_models import (
    AssemblyReportExtension,
    ConflictResolution,
    ConflictResolutionStatus,
    ConflictType,
    Step35Input,
    Step35Result,
    Step35Status,
)

if TYPE_CHECKING:
    from src.ccp.core.receipt_chain import ReceiptChain

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════
# Constants
# ══════════════════════════════════════════════════════════════

AGENT_NAME = "Builder-Engine-Logic-Core"
STAGE_1_NAME = "STAGE-1-STEP35-INIT"
STAGE_2_NAME = "STAGE-2-TYPE-1-CONFLICT"
STAGE_3_NAME = "STAGE-3-TYPE-2-CONFLICT"
STAGE_4_NAME = "STAGE-4-TYPE-3-CONFLICT"


# ══════════════════════════════════════════════════════════════
# Conflict Extraction Helpers
# ══════════════════════════════════════════════════════════════

def _extract_finding_text(
    cral_index: Any, moment_key: CRALMomentKey,
) -> Optional[str]:
    """Extract finding text for a specific moment from the CRAL index.

    Handles both CRALFindingIndex objects and raw dict payloads.

    Args:
        cral_index: DEP-ENG-021 CRALFindingIndex or dict.
        moment_key: The moment to extract.

    Returns:
        Finding text string, or None if not found.
    """
    if cral_index is None:
        return None

    # Handle CRALFindingIndex object (findings is dict[str, CRALFinding])
    if hasattr(cral_index, "get_finding"):
        finding = cral_index.get_finding(moment_key)
        if finding is not None and hasattr(finding, "finding_text"):
            return finding.finding_text
        return None

    if hasattr(cral_index, "findings"):
        findings = cral_index.findings
        # dict[str, CRALFinding] keyed by moment key value
        if isinstance(findings, dict):
            finding = findings.get(moment_key.value)
            if finding is not None and hasattr(finding, "finding_text"):
                return finding.finding_text
            return None
        # list fallback
        for finding in findings:
            if hasattr(finding, "moment_key") and finding.moment_key == moment_key:
                return finding.finding_text if hasattr(finding, "finding_text") else None
        return None

    # Handle dict payload
    if isinstance(cral_index, dict):
        findings = cral_index.get("findings", [])
        for f in findings:
            if f.get("moment_key") == moment_key.value or f.get("moment_id") == moment_key.value:
                return f.get("finding_text") or f.get("finding_content")
        return None

    return None


def _extract_soc_mechanism(soc_batch: Any) -> Optional[str]:
    """Extract the primary mechanism/voice text from DEP-ENG-010 SoC.

    Handles FourAxisMatchResult objects and raw dict payloads.

    Args:
        soc_batch: DEP-ENG-010 Source of Context batch.

    Returns:
        Mechanism text string, or None.
    """
    if soc_batch is None:
        return None

    # Handle object with compute_classification or primary_voice
    if hasattr(soc_batch, "primary_voice"):
        return soc_batch.primary_voice
    if hasattr(soc_batch, "mechanism_text"):
        return soc_batch.mechanism_text

    # Handle dict payload
    if isinstance(soc_batch, dict):
        return (
            soc_batch.get("primary_voice")
            or soc_batch.get("mechanism_text")
            or soc_batch.get("voice_text")
        )

    return None


def _extract_auth_claim(auth_certificate: Any) -> Optional[str]:
    """Extract the authenticated result/claim from DEP-ENG-005.

    Handles TTTBaselineData objects and raw dict payloads.

    Args:
        auth_certificate: DEP-ENG-005 Authentication Certificate.

    Returns:
        Authenticated claim text string, or None.
    """
    if auth_certificate is None:
        return None

    # Handle object
    if hasattr(auth_certificate, "authenticated_result"):
        return auth_certificate.authenticated_result
    if hasattr(auth_certificate, "result_claim"):
        return auth_certificate.result_claim

    # Handle dict payload
    if isinstance(auth_certificate, dict):
        return (
            auth_certificate.get("authenticated_result")
            or auth_certificate.get("result_claim")
            or auth_certificate.get("claim")
        )

    return None


def _texts_contradict(text_a: str, text_b: str) -> bool:
    """Determine if two mechanism texts semantically contradict.

    FR17 Technical Decision 1: For Type 1, resolution is purely
    hierarchical — no semantic analysis needed. For Type 2/3,
    this provides a structural heuristic. In production, an LLM
    semantic diff would replace this.

    Simple heuristic: texts contradict if both are non-empty and
    differ substantially (not substrings of each other).

    Args:
        text_a: First text.
        text_b: Second text.

    Returns:
        True if texts appear contradictory.
    """
    if not text_a or not text_b:
        return False

    a_lower = text_a.lower().strip()
    b_lower = text_b.lower().strip()

    # Identical or substring → no contradiction
    if a_lower == b_lower:
        return False
    if a_lower in b_lower or b_lower in a_lower:
        return False

    # Both non-empty and not substrings — structural heuristic
    # considers them potentially contradictory.
    return True


# ══════════════════════════════════════════════════════════════
# Research Synthesis Protocol
# ══════════════════════════════════════════════════════════════

class ResearchSynthesisProtocol:
    """FR17 — Builder Engine Step 3.5 Conflict Detection.

    Positioned between DEP resolution (Step 3) and Template Selection
    (Step 4). Runs a deterministic conflict-detection pass across:
        - DEP-ENG-021 (CRAL Finding Index)
        - DEP-ENG-010 (Source of Context)
        - DEP-ENG-005 (Authentication Certificate)

    Only fires when cral_coverage_status ≠ ABSENT.

    Usage:
        protocol = ResearchSynthesisProtocol(coach_id="coach_88ab")
        result = protocol.execute(Step35Input(
            coach_id="coach_88ab",
            cral_coverage_status="COMPLETE",
            cral_finding_index=index,
            soc_batch=soc,
            auth_certificate=auth,
        ))
    """

    def __init__(
        self,
        coach_id: str,
        receipt_chain: Optional[ReceiptChain] = None,
    ):
        self.coach_id = coach_id
        self.receipt_chain = receipt_chain

    # ──────────────────────────────────────────────────────────
    # Stage 1: Dependency Ingestion
    # ──────────────────────────────────────────────────────────

    def _stage_1_init(
        self, step_input: Step35Input,
    ) -> tuple[bool, Step35Result]:
        """Stage 1: Load and validate dependencies.

        FR17 §Stage 1: Check cral_coverage_status. If ABSENT,
        write skip event and return immediately.

        Returns:
            (should_continue, result) — False means skip.
        """
        start_time = time.perf_counter()

        # FR17 AC4: Skip if ABSENT
        if step_input.cral_coverage_status == "ABSENT":
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            result = Step35Result(
                coach_id=self.coach_id,
                step_35_status=Step35Status.SKIPPED_CRAL_ABSENT,
                compilation_allowed=True,
                execution_time_ms=elapsed_ms,
                warnings=["cral_coverage_status=ABSENT — Step 3.5 skipped."],
            )
            result.assembly_report.step_35_status = Step35Status.SKIPPED_CRAL_ABSENT

            self._write_receipt(
                STAGE_1_NAME,
                f"cral_status={step_input.cral_coverage_status}",
                f"SKIPPED in {elapsed_ms:.2f}ms",
                {"skip_code": "CRAL_ABSENT", "elapsed_ms": elapsed_ms},
            )

            logger.info(
                "Step 3.5 skipped: cral_coverage_status=ABSENT (%.2fms)",
                elapsed_ms,
            )
            return False, result

        # Validate inputs present
        self._write_receipt(
            STAGE_1_NAME,
            f"cral_status={step_input.cral_coverage_status}",
            "Dependencies loaded, proceeding to conflict passes.",
            {
                "cral_index_present": step_input.cral_finding_index is not None,
                "soc_present": step_input.soc_batch is not None,
                "auth_present": step_input.auth_certificate is not None,
            },
        )

        return True, Step35Result(coach_id=self.coach_id)

    # ──────────────────────────────────────────────────────────
    # Stage 2: Type 1 Conflict Pass (Source Proximity)
    # ──────────────────────────────────────────────────────────

    def _stage_2_type_1(
        self,
        step_input: Step35Input,
        report: AssemblyReportExtension,
    ) -> AssemblyReportExtension:
        """Stage 2: Type 1 Conflict Pass — Source Proximity.

        FR17 §Stage 2: M2 (External) vs M6 (Internal). If contradictory,
        M6 overrides M2 deterministically. Auto-resolve.

        FR17 AC1: M6 wins without operator flag.
        """
        m2_text = _extract_finding_text(
            step_input.cral_finding_index, CRALMomentKey.M2_BELIEVABLE,
        )
        m6_text = _extract_finding_text(
            step_input.cral_finding_index, CRALMomentKey.M6_IRREFUTABLE,
        )

        if m2_text and m6_text and _texts_contradict(m2_text, m6_text):
            # Type 1 detected — auto-resolve M6 > M2
            resolution = ConflictResolution(
                conflict_type=ConflictType.TYPE_1_PROXIMITY,
                status=ConflictResolutionStatus.AUTO_RESOLVED,
                details=(
                    f"M2 (External Documentary Evidence) asserted: '{m2_text[:100]}...'; "
                    f"M6 (Internal Institutional Evidence) asserted: '{m6_text[:100]}...'. "
                    "M6 overrides M2 based on internal proximity precedence."
                ),
                action_taken="M6 forced as primary evidentiary anchor for script template.",
                source_a="DEP-ENG-021[M2_BELIEVABLE]",
                source_b="DEP-ENG-021[M6_IRREFUTABLE]",
            )

            report.cral_conflict_resolution.append(resolution)
            report.type_1_count += 1
            report.auto_resolved_count += 1

            self._write_receipt(
                STAGE_2_NAME,
                "M2 vs M6 proximity check",
                "TYPE_1 AUTO_RESOLVED: M6 overrides M2",
                {"conflict_type": "TYPE_1_PROXIMITY", "resolution": "AUTO_RESOLVED"},
            )

            logger.info("Type 1 conflict: M6 overrides M2 (auto-resolved).")
        else:
            # No Type 1 conflict detected
            resolution = ConflictResolution(
                conflict_type=ConflictType.TYPE_1_PROXIMITY,
                status=ConflictResolutionStatus.NO_CONFLICT,
                details="No contradictory claims between M2 and M6.",
                action_taken="No action required.",
                source_a="DEP-ENG-021[M2_BELIEVABLE]",
                source_b="DEP-ENG-021[M6_IRREFUTABLE]",
            )
            report.cral_conflict_resolution.append(resolution)

            self._write_receipt(
                STAGE_2_NAME,
                "M2 vs M6 proximity check",
                "No Type 1 conflict detected",
                {"conflict_type": "TYPE_1_PROXIMITY", "resolution": "NO_CONFLICT"},
            )

        return report

    # ──────────────────────────────────────────────────────────
    # Stage 3: Type 2 Conflict Pass (Structural Mismatch)
    # ──────────────────────────────────────────────────────────

    def _stage_3_type_2(
        self,
        step_input: Step35Input,
        report: AssemblyReportExtension,
    ) -> AssemblyReportExtension:
        """Stage 3: Type 2 Conflict Pass — Structural Mismatch.

        FR17 §Stage 3: M4 CRAL narrative vs DEP-ENG-010 SoC.
        If root mechanisms differ materially, FLAG for operator.
        Do NOT auto-resolve.

        FR17 AC2: FLAGGED_FOR_OPERATOR, pipeline halts.
        """
        m4_text = _extract_finding_text(
            step_input.cral_finding_index, CRALMomentKey.M4_RESONANT,
        )
        soc_text = _extract_soc_mechanism(step_input.soc_batch)

        if m4_text and soc_text and _texts_contradict(m4_text, soc_text):
            # Type 2 detected — flag for operator
            queue_id = hashlib.sha256(
                f"{self.coach_id}:TYPE_2:{m4_text[:50]}:{soc_text[:50]}".encode()
            ).hexdigest()[:12]
            operator_queue_id = f"REQ-{queue_id.upper()}"

            resolution = ConflictResolution(
                conflict_type=ConflictType.TYPE_2_STRUCTURAL,
                status=ConflictResolutionStatus.FLAGGED_FOR_OPERATOR,
                details=(
                    f"M4 CRAL finding: '{m4_text[:120]}...'. "
                    f"SoC DEP-ENG-010: '{soc_text[:120]}...'. "
                    "Root mechanism differs materially."
                ),
                action_taken=(
                    f"Execution Halted. Placed in Operator Resolution Queue "
                    f"ID: {operator_queue_id}"
                ),
                source_a="DEP-ENG-021[M4_RESONANT]",
                source_b="DEP-ENG-010",
                operator_queue_id=operator_queue_id,
            )

            report.cral_conflict_resolution.append(resolution)
            report.type_2_count += 1
            report.operator_flags_count += 1

            self._write_receipt(
                STAGE_3_NAME,
                "M4 vs SoC structural check",
                f"TYPE_2 FLAGGED: {operator_queue_id}",
                {
                    "conflict_type": "TYPE_2_STRUCTURAL",
                    "resolution": "FLAGGED_FOR_OPERATOR",
                    "operator_queue_id": operator_queue_id,
                },
            )

            logger.warning(
                "Type 2 conflict: M4 vs SoC flagged for operator (%s).",
                operator_queue_id,
            )
        else:
            resolution = ConflictResolution(
                conflict_type=ConflictType.TYPE_2_STRUCTURAL,
                status=ConflictResolutionStatus.NO_CONFLICT,
                details="No structural mismatch between M4 and SoC.",
                action_taken="No action required.",
                source_a="DEP-ENG-021[M4_RESONANT]",
                source_b="DEP-ENG-010",
            )
            report.cral_conflict_resolution.append(resolution)

            self._write_receipt(
                STAGE_3_NAME,
                "M4 vs SoC structural check",
                "No Type 2 conflict detected",
                {"conflict_type": "TYPE_2_STRUCTURAL", "resolution": "NO_CONFLICT"},
            )

        return report

    # ──────────────────────────────────────────────────────────
    # Stage 4: Type 3 Conflict Pass (Authenticity)
    # ──────────────────────────────────────────────────────────

    def _stage_4_type_3(
        self,
        step_input: Step35Input,
        report: AssemblyReportExtension,
    ) -> AssemblyReportExtension:
        """Stage 4: Type 3 Conflict Pass — Authenticity.

        FR17 §Stage 4: M6 Irrefutable vs DEP-ENG-005 Auth Certificate.
        If M6 contradicts the coach's authenticated result, TERMINAL BLOCK.
        Return to Phase 1. Do NOT flag for operator.

        FR17 AC3: Terminal Block (NOT operator flag).
        """
        m6_text = _extract_finding_text(
            step_input.cral_finding_index, CRALMomentKey.M6_IRREFUTABLE,
        )
        auth_claim = _extract_auth_claim(step_input.auth_certificate)

        if m6_text and auth_claim and _texts_contradict(m6_text, auth_claim):
            # Type 3 detected — TERMINAL BLOCK
            resolution = ConflictResolution(
                conflict_type=ConflictType.TYPE_3_AUTHENTICITY,
                status=ConflictResolutionStatus.TERMINAL_BLOCK,
                details=(
                    f"M6 Irrefutable: '{m6_text[:120]}...'. "
                    f"DEP-ENG-005 Auth Certificate: '{auth_claim[:120]}...'. "
                    "M6 directly contradicts coach's authenticated result."
                ),
                action_taken=(
                    "TERMINAL BLOCK issued. Pipeline returns to Phase 1. "
                    "Do not proceed to Step 4 (Template Selection)."
                ),
                source_a="DEP-ENG-021[M6_IRREFUTABLE]",
                source_b="DEP-ENG-005",
            )

            report.cral_conflict_resolution.append(resolution)
            report.type_3_count += 1
            report.terminal_blocks_count += 1

            self._write_receipt(
                STAGE_4_NAME,
                "M6 vs DEP-ENG-005 authenticity check",
                "TYPE_3 TERMINAL_BLOCK issued",
                {
                    "conflict_type": "TYPE_3_AUTHENTICITY",
                    "resolution": "TERMINAL_BLOCK",
                },
            )

            logger.error(
                "Type 3 conflict: M6 vs Auth Certificate — TERMINAL BLOCK."
            )
        else:
            resolution = ConflictResolution(
                conflict_type=ConflictType.TYPE_3_AUTHENTICITY,
                status=ConflictResolutionStatus.NO_CONFLICT,
                details="No authenticity conflict between M6 and Auth Certificate.",
                action_taken="No action required.",
                source_a="DEP-ENG-021[M6_IRREFUTABLE]",
                source_b="DEP-ENG-005",
            )
            report.cral_conflict_resolution.append(resolution)

            self._write_receipt(
                STAGE_4_NAME,
                "M6 vs DEP-ENG-005 authenticity check",
                "No Type 3 conflict detected",
                {"conflict_type": "TYPE_3_AUTHENTICITY", "resolution": "NO_CONFLICT"},
            )

        return report

    # ──────────────────────────────────────────────────────────
    # Compute Overall Status
    # ──────────────────────────────────────────────────────────

    def _compute_overall_status(
        self, report: AssemblyReportExtension,
    ) -> tuple[Step35Status, bool]:
        """Compute the overall Step 3.5 status from conflict results.

        Returns:
            (status, compilation_allowed) tuple.
        """
        if report.terminal_blocks_count > 0:
            return Step35Status.TERMINAL_BLOCK, False

        if report.operator_flags_count > 0:
            return Step35Status.PENDING_OPERATOR_CLEARANCE, False

        if report.auto_resolved_count > 0:
            return Step35Status.RESOLVED, True

        return Step35Status.CLEAR, True

    # ──────────────────────────────────────────────────────────
    # Main Execution
    # ──────────────────────────────────────────────────────────

    def execute(self, step_input: Step35Input) -> Step35Result:
        """Execute the full Research Synthesis Protocol (Step 3.5).

        Stages 1-4 in sequence. Returns Step35Result with the
        assembly report extension.

        FR17 AC4: If ABSENT, completes in < 20ms.

        Args:
            step_input: Step35Input with all dependency payloads.

        Returns:
            Step35Result with conflict resolution log.
        """
        start_time = time.perf_counter()

        # ── Stage 1: Init ──
        should_continue, result = self._stage_1_init(step_input)
        if not should_continue:
            return result

        report = AssemblyReportExtension()

        # ── Stage 2: Type 1 (Source Proximity) ──
        report = self._stage_2_type_1(step_input, report)

        # ── Stage 3: Type 2 (Structural Mismatch) ──
        report = self._stage_3_type_2(step_input, report)

        # ── Stage 4: Type 3 (Authenticity) ──
        report = self._stage_4_type_3(step_input, report)

        # ── Compute overall status ──
        overall_status, compilation_allowed = self._compute_overall_status(report)
        report.step_35_status = overall_status

        elapsed_ms = (time.perf_counter() - start_time) * 1000

        result.step_35_status = overall_status
        result.assembly_report = report
        result.compilation_allowed = compilation_allowed
        result.execution_time_ms = elapsed_ms

        # Warnings
        if report.auto_resolved_count > 0:
            result.warnings.append(
                f"{report.auto_resolved_count} conflict(s) auto-resolved "
                f"(Type 1 proximity hierarchy)."
            )

        logger.info(
            "Step 3.5 complete: status=%s, compilation_allowed=%s, "
            "conflicts=%d, elapsed=%.2fms",
            overall_status.value,
            compilation_allowed,
            len(report.cral_conflict_resolution),
            elapsed_ms,
        )

        return result

    # ──────────────────────────────────────────────────────────
    # Receipt Helpers
    # ──────────────────────────────────────────────────────────

    def _write_receipt(
        self,
        stage_name: str,
        input_summary: str,
        output_summary: str,
        metadata: Optional[dict[str, Any]] = None,
    ) -> None:
        """Write receipt chain entry for a Step 3.5 stage.

        FR47 DEP-ENG-041 schema compliance.
        """
        if self.receipt_chain is None:
            return

        self.receipt_chain.log(
            agent_id=AGENT_NAME,
            action=stage_name,
            input_summary=input_summary,
            output_summary=output_summary,
            metadata={
                "stage_name": stage_name,
                "agent_name": AGENT_NAME,
                "coach_id": self.coach_id,
                **(metadata or {}),
            },
        )
