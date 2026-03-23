"""
CCP FR8 TTT Enforcement Rule — TTT Enforcement Pipeline (Unit 8)
Full pipeline orchestrating C-08, TTT baseline extraction, affinity advisory,
and Sophia validation for the JIT Skill Assembler pre-flight.

Spec reference: FR8_TTT_Enforcement_Rule_Tech_Spec.md
                §Layer 2: Compilation Detection — C-08 Tier 0 Pre-flight
                §Layer 3: Runtime Resolution — DEP-ENG-005
                §Architecture: TTT Enforcement Pipeline

Receipt stage: TTT-BASELINE-RESOLUTION
Agent ID:      authentication_adapter
DEP:           DEP-ENG-005 (ttt_baseline.json Authentication Certificate)

Pipeline phases (in order):
  PHASE 1: C-08 Tier 0 pre-flight gate
  PHASE 2: TTT baseline resolution (load DEP-ENG-005)
  PHASE 3: Affinity range advisory (logging only — never blocks)
  PHASE 4: Sophia TTT validation (drift, similarity, emotional peaks)
  PHASE 5: Assembly report write
  PHASE 6: Receipt log (TTT-BASELINE-RESOLUTION)
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.ttt_models import (
    AssemblyReport,
    AssemblyReportC08Section,
    C08Result,
    C08Status,
    CompiledDesignBrief,
    SophiaDriftVerdict,
    SophiaTTTValidationResult,
    TTTBaselineData,
)
from src.ccp.services.assembly_report_writer import AssemblyReportWriter
from src.ccp.services.c08_ttt_enforcement import C08TTTEnforcement
from src.ccp.services.sophia_ttt_validator import SophiaTTTValidator
from src.ccp.services.ttt_affinity_advisor import TTTAffinityAdvisor
from src.ccp.services.ttt_baseline_extractor import (
    LIWCAuthenticationError,
    TTTBaselineExtractor,
)


AGENT_ID = "authentication_adapter"
RECEIPT_ACTION = "TTT-BASELINE-RESOLUTION"


class TTTPipelineError(Exception):
    """Raised when the TTT pipeline encounters an unrecoverable error."""


class TTTEnforcementSession:
    """Captures the complete state of one TTT enforcement pipeline run."""

    def __init__(self, compilation_id: str):
        self.compilation_id = compilation_id
        self.started_at: str = datetime.now(timezone.utc).isoformat()
        self.completed_at: Optional[str] = None

        # Phase results
        self.c08_result: Optional[C08Result] = None
        self.baseline: Optional[TTTBaselineData] = None
        self.affinity_results: list[Any] = []
        self.sophia_result: Optional[SophiaTTTValidationResult] = None
        self.assembly_report: Optional[AssemblyReport] = None
        self.assembly_report_path: Optional[Path] = None
        self.receipt_id: Optional[str] = None

        # Flow control
        self.pipeline_halted: bool = False
        self.halt_reason: Optional[str] = None
        self.liwc_auth_error: Optional[LIWCAuthenticationError] = None

    @property
    def deployment_status(self) -> str:
        """ACCEPTED or REJECTED based on all gate results."""
        if self.pipeline_halted:
            return "REJECTED"
        if self.c08_result and not self.c08_result.passed:
            return "REJECTED"
        if self.sophia_result and self.sophia_result.verdict != SophiaDriftVerdict.PASS:
            return "REJECTED"
        return "ACCEPTED"

    def to_summary(self) -> dict[str, Any]:
        """Return a structured summary for logging and reporting."""
        return {
            "compilation_id": self.compilation_id,
            "deployment_status": self.deployment_status,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "pipeline_halted": self.pipeline_halted,
            "halt_reason": self.halt_reason,
            "c08_passed": self.c08_result.passed if self.c08_result else None,
            "baseline_loaded": self.baseline is not None,
            "sophia_verdict": self.sophia_result.verdict.value if self.sophia_result else None,
            "receipt_id": self.receipt_id,
        }


class TTTEnforcementPipeline:
    """Full TTT enforcement pipeline for the JIT Skill Assembler.

    Runs C-08 pre-flight, resolves DEP-ENG-005, checks affinity range,
    validates via Sophia, and writes the assembly report.

    Spec §Layer 2 C-08 Tier 0 guarantee:
    - Zero tokens consumed on REJECT
    - Zero adapter invocations on REJECT
    - REJECT halts the pipeline before any LLM call

    Spec §Layer 3 Runtime Resolution:
    - TTT value is NEVER embedded in the compiled brief
    - JIT Assembler loads ttt_baseline.json at runtime (DEP-ENG-005)
    - Sophia validates that the generated output matches the baseline

    Usage:
        pipeline = TTTEnforcementPipeline(
            coach_dir=Path("coaches/NDL"),
            coach_acronym="NDL",
            receipt_chain=rc,
        )
        session = pipeline.run(
            brief=compiled_brief,
            generated_content_analysis=liwc_analysis_of_generated_output,
            model_id="gpt-4",
        )
    """

    def __init__(
        self,
        coach_dir: Path,
        coach_acronym: str,
        receipt_chain: ReceiptChain,
        *,
        report_dir: Optional[Path] = None,
    ):
        self._coach_dir = Path(coach_dir)
        self._coach_acronym = coach_acronym
        self._receipt_chain = receipt_chain
        self._report_dir = report_dir or (self._coach_dir / "assembly_reports")

        # Services
        self._c08 = C08TTTEnforcement()
        self._baseline_extractor = TTTBaselineExtractor(self._coach_dir)
        self._affinity_advisor = TTTAffinityAdvisor()
        self._sophia = SophiaTTTValidator()
        self._report_writer = AssemblyReportWriter()

    def run(
        self,
        brief: CompiledDesignBrief,
        generated_content_analysis: Optional[dict[str, Any]] = None,
        model_id: str = "gpt-4",
    ) -> TTTEnforcementSession:
        """Execute the full TTT enforcement pipeline.

        Args:
            brief: CompiledDesignBrief to validate (must NOT contain TTT values).
            generated_content_analysis: LIWC-style analysis dict of generated output.
                Optional: Sophia validation is skipped if not provided.
            model_id: LLM model ID used for generation (for model offset registry).

        Returns:
            TTTEnforcementSession with complete pipeline state.
        """
        session = TTTEnforcementSession(compilation_id=brief.compilation_id)

        # ── Phase 1: C-08 Tier 0 Pre-flight Gate ────────────────────────────
        session.c08_result = self._run_c08_phase(brief, session)
        if session.pipeline_halted:
            self._finalize(session, brief)
            return session

        # ── Phase 2: TTT Baseline Resolution (DEP-ENG-005) ──────────────────
        baseline = self._run_baseline_phase(brief, session)
        if session.pipeline_halted:
            self._finalize(session, brief)
            return session
        session.baseline = baseline

        # ── Phase 3: Affinity Range Advisory (logging only) ─────────────────
        self._run_affinity_phase(brief, session)

        # ── Phase 4: Sophia TTT Validation ──────────────────────────────────
        if generated_content_analysis is not None and session.baseline is not None:
            session.sophia_result = self._run_sophia_phase(
                session.baseline,
                generated_content_analysis,
                brief.compilation_id,
                model_id,
                session,
            )

        # ── Phase 5: Assembly Report Write ──────────────────────────────────
        self._write_report(brief, session)

        # ── Phase 6: Receipt Log ─────────────────────────────────────────────
        self._finalize(session, brief)
        return session

    # ─── Phase Implementations ────────────────────────────────────────────────

    def _run_c08_phase(
        self, brief: CompiledDesignBrief, session: TTTEnforcementSession
    ) -> C08Result:
        """Phase 1: C-08 Tier 0 gate — zero-token guarantee on REJECT."""
        c08_result = self._c08.run(brief)

        if not c08_result.passed:
            first = c08_result.first_violation
            session.pipeline_halted = True
            session.halt_reason = (
                f"C-08 REJECT: M-02 violation in '{first.violating_field}' — "
                f"{first.violation_type.value}. Recovery: {first.recovery_instruction}"
                if first
                else "C-08 REJECT: M-02 violation detected."
            )

        return c08_result

    def _run_baseline_phase(
        self, brief: CompiledDesignBrief, session: TTTEnforcementSession
    ) -> Optional[TTTBaselineData]:
        """Phase 2: Load DEP-ENG-005 (ttt_baseline.json)."""
        try:
            baseline = self._baseline_extractor.load()
        except Exception as exc:
            session.pipeline_halted = True
            session.halt_reason = f"DEP-ENG-005 resolution failed: {exc}"
            return None

        if baseline is None:
            session.pipeline_halted = True
            session.halt_reason = (
                "DEP-ENG-005 not found. TTT baseline authentication certificate "
                "must exist at config/ttt_baseline.json before JIT assembly."
            )
            return None

        return baseline

    def _run_affinity_phase(
        self, brief: CompiledDesignBrief, session: TTTEnforcementSession
    ) -> None:
        """Phase 3: Affinity range advisory — NEVER blocks compilation (AC8)."""
        if session.baseline is None:
            return

        affinity_result = self._affinity_advisor.evaluate(
            archetype_id=brief.archetype_id,
            coach_temperature=session.baseline.temperature,
        )
        session.affinity_results.append(affinity_result)

        if affinity_result.ttt_outside_affinity_range:
            # Advisory only — pipeline continues regardless
            import logging
            logging.getLogger(__name__).warning(
                "TTT Affinity Advisory: coach TTT-0%s is outside the %s affinity range "
                "[TTT-0%s to TTT-0%s]. Requires human review. Compilation PROCEEDS.",
                session.baseline.temperature,
                brief.archetype_id,
                affinity_result.affinity_min,
                affinity_result.affinity_max,
            )

    def _run_sophia_phase(
        self,
        baseline: TTTBaselineData,
        generated_content_analysis: dict[str, Any],
        compilation_id: str,
        model_id: str,
        session: TTTEnforcementSession,
    ) -> SophiaTTTValidationResult:
        """Phase 4: Sophia TTT validation (drift, similarity, emotional peaks)."""
        return self._sophia.validate(
            baseline=baseline,
            generated_content_analysis=generated_content_analysis,
            compilation_id=compilation_id,
            model_id=model_id,
        )

    def _write_report(
        self, brief: CompiledDesignBrief, session: TTTEnforcementSession
    ) -> None:
        """Phase 5: Write assembly_report.json."""
        try:
            report_path = self._report_dir / f"{brief.compilation_id}_assembly_report.json"
            report = self._report_writer.write_report(
                brief=brief,
                session=session,
                output_path=report_path,
            )
            session.assembly_report = report
            session.assembly_report_path = report_path
        except Exception as exc:
            # Report writing failure does not halt the pipeline — log and continue
            import logging
            logging.getLogger(__name__).error(
                "Assembly report write failed for %s: %s",
                brief.compilation_id,
                exc,
            )

    # ─── Finalization ─────────────────────────────────────────────────────────

    def _finalize(
        self, session: TTTEnforcementSession, brief: CompiledDesignBrief
    ) -> None:
        """Phase 6: Log receipt and mark session complete."""
        session.completed_at = datetime.now(timezone.utc).isoformat()

        c08_violation_info = ""
        if session.c08_result and not session.c08_result.passed:
            fv = session.c08_result.first_violation
            if fv:
                c08_violation_info = f" | C-08 violation: {fv.violating_field} ({fv.violation_type.value})"

        sophia_info = ""
        if session.sophia_result:
            sophia_info = (
                f" | Sophia: {session.sophia_result.verdict.value} "
                f"(drift={session.sophia_result.ttt_drift_percentage:.1%}, "
                f"sim={session.sophia_result.cosine_similarity:.3f})"
            )

        output_summary = (
            f"TTT enforcement {session.deployment_status} "
            f"for compilation '{brief.compilation_id}'"
            f"{c08_violation_info}{sophia_info}"
        )

        entry = self._receipt_chain.log(
            agent_id=AGENT_ID,
            action=RECEIPT_ACTION,
            asset_id=brief.compilation_id,
            input_summary=(
                f"CompiledDesignBrief archetype='{brief.archetype_id}', "
                f"block_b_fields={len(brief.block_b_fields)}, "
                f"block_a_laws={len(brief.block_a_structural_laws)}"
            ),
            output_summary=output_summary,
            decision=session.deployment_status.lower(),
            decision_rationale=session.halt_reason,
            metadata=session.to_summary(),
        )
        session.receipt_id = entry.receipt_id
