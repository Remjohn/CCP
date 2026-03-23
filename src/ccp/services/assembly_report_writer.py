"""
CCP FR8 TTT Enforcement Rule — Assembly Report Writer (Unit 9)
Writes assembly_report.json for each compilation run.

Spec reference: FR8_TTT_Enforcement_Rule_Tech_Spec.md
                §Assembly Report Schema (assembly_report.json)
                §AC11: Pipeline interruption logged with:
                         template_id, violated_field, recovery_instruction

The assembly report captures the full C-08 diagnostic and Sophia validation
outcome for a single compilation run. It is written per-compilation and is
the primary audit artifact for the TTT enforcement layer.

Deployment status:
  - REJECTED: C-08 FAIL or Sophia drift/similarity/peak failure
  - ACCEPTED: C-08 PASS + Sophia PASS (or Sophia skipped — no generated output)
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional

from src.ccp.models.ttt_models import (
    AssemblyReport,
    AssemblyReportC08Section,
    C08Status,
    CompiledDesignBrief,
)

if TYPE_CHECKING:
    from src.ccp.pipelines.ttt_enforcement_pipeline import TTTEnforcementSession


class AssemblyReportWriter:
    """Writes assembly_report.json for a TTT enforcement pipeline run.

    Spec AC11: When pipeline is interrupted by C-08 rejection, the report
    MUST contain:
        - template_id (= compilation_id)
        - violated_field
        - recovery_instruction
    These allow template authors to trace the exact cause and correct it.
    """

    def write_report(
        self,
        brief: CompiledDesignBrief,
        session: "TTTEnforcementSession",
        output_path: Path,
    ) -> AssemblyReport:
        """Write the assembly report for a pipeline session.

        Args:
            brief: The CompiledDesignBrief that was evaluated.
            session: The TTTEnforcementSession with all phase results.
            output_path: Where to write the JSON file.

        Returns:
            The AssemblyReport model that was written.
        """
        # ── Build C-08 section ────────────────────────────────────────────────
        c08_section = self._build_c08_section(brief, session)

        # ── Build Sophia section ──────────────────────────────────────────────
        sophia_section = self._build_sophia_section(session)

        # ── Build pipeline interruption log (AC11) ────────────────────────────
        pipeline_interruption_log = self._build_interruption_log(brief, session)

        # ── Assemble report ───────────────────────────────────────────────────
        report = AssemblyReport(
            compilation_id=brief.compilation_id,
            archetype_id=brief.archetype_id,
            deployment_status=session.deployment_status,
            generated_at=datetime.now(timezone.utc).isoformat(),
            c08_section=c08_section,
            sophia_section=sophia_section,
            pipeline_interruption_log=pipeline_interruption_log,
        )

        session.assembly_report = report
        self._write_json(report, output_path)
        return report

    def write_report_dict(
        self,
        brief: CompiledDesignBrief,
        session: "TTTEnforcementSession",
    ) -> dict[str, Any]:
        """Build the report dict without writing to disk.

        Useful for testing or embedding in larger reports.
        """
        c08_section = self._build_c08_section(brief, session)
        sophia_section = self._build_sophia_section(session)
        interruption_log = self._build_interruption_log(brief, session)

        return {
            "compilation_id": brief.compilation_id,
            "archetype_id": brief.archetype_id,
            "deployment_status": session.deployment_status,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "c08_section": c08_section.model_dump() if c08_section else None,
            "sophia_section": sophia_section,
            "pipeline_interruption_log": interruption_log,
        }

    # ─── Section Builders ─────────────────────────────────────────────────────

    def _build_c08_section(
        self,
        brief: CompiledDesignBrief,
        session: "TTTEnforcementSession",
    ) -> AssemblyReportC08Section:
        """Build the C-08 diagnostic section of the report."""
        if session.c08_result is None:
            return AssemblyReportC08Section(
                status=C08Status.FAIL,
                violations=[],
                tokens_consumed=0,
                adapter_invocations=0,
                section_assemblies=0,
                check_performed_at=datetime.now(timezone.utc).isoformat(),
            )

        cr = session.c08_result
        return AssemblyReportC08Section(
            status=cr.status,
            violations=cr.violations,
            tokens_consumed=cr.tokens_consumed,
            adapter_invocations=cr.adapter_invocations,
            section_assemblies=cr.section_assemblies,
            check_performed_at=datetime.now(timezone.utc).isoformat(),
        )

    def _build_sophia_section(
        self, session: "TTTEnforcementSession"
    ) -> Optional[dict[str, Any]]:
        """Build the Sophia validation section, or None if Sophia was not run."""
        sr = session.sophia_result
        if sr is None:
            return None

        return {
            "verdict": sr.verdict.value,
            "drift_percentage": round(sr.ttt_drift_percentage, 4),
            "drift_threshold": sr.drift_threshold,
            "drift_passed": sr.drift_passed,
            "cosine_similarity": round(sr.cosine_similarity, 4),
            "similarity_threshold": sr.similarity_threshold,
            "similarity_passed": sr.similarity_passed,
            "emotional_peaks": [
                {
                    "position_index": p.position_index,
                    "intensity": p.intensity,
                    "content_segment": p.content_segment,
                }
                for p in sr.emotional_peaks
            ],
            "average_intensity": round(sr.average_intensity, 4),
            "peaks_passed": sr.peaks_passed,
            "peak_threshold_pct": sr.peak_threshold_pct,
            "model_id": sr.model_id,
            "model_offset_applied": sr.model_offset_applied,
        }

    def _build_interruption_log(
        self,
        brief: CompiledDesignBrief,
        session: "TTTEnforcementSession",
    ) -> Optional[dict[str, Any]]:
        """Build AC11 pipeline interruption log when C-08 rejects.

        Returns dict with template_id, violated_field, recovery_instruction
        if the pipeline was halted by C-08; None otherwise.
        """
        if not session.pipeline_halted:
            return None

        # C-08 was the cause of the halt
        if session.c08_result and not session.c08_result.passed:
            first_violation = session.c08_result.first_violation
            if first_violation:
                return {
                    "template_id": brief.compilation_id,
                    "violated_field": first_violation.violating_field,
                    "violation_type": first_violation.violation_type.value,
                    "violating_value": first_violation.violating_value,
                    "matched_pattern": first_violation.matched_pattern,
                    "mandate_violated": first_violation.mandate_violated,
                    "recovery_instruction": first_violation.recovery_instruction,
                    "pipeline_impact": first_violation.pipeline_impact,
                    "all_violations": [
                        {
                            "violating_field": v.violating_field,
                            "violation_type": v.violation_type.value,
                            "recovery_instruction": v.recovery_instruction,
                        }
                        for v in session.c08_result.violations
                    ],
                }

        # Baseline resolution failure or other halt
        return {
            "template_id": brief.compilation_id,
            "violated_field": "pipeline",
            "violation_type": "PIPELINE_HALT",
            "violating_value": None,
            "matched_pattern": None,
            "mandate_violated": "DEP-ENG-005",
            "recovery_instruction": session.halt_reason or "Unknown pipeline halt.",
            "pipeline_impact": "JIT assembly aborted.",
            "all_violations": [],
        }

    # ─── File I/O ─────────────────────────────────────────────────────────────

    def _write_json(self, report: AssemblyReport, output_path: Path) -> None:
        """Write the AssemblyReport to a JSON file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Serialize using Pydantic's JSON-safe serialization
        report_dict = report.model_dump(mode="json")
        output_path.write_text(
            json.dumps(report_dict, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
