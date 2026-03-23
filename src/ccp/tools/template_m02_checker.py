"""
CCP FR8 TTT Enforcement Rule — Template M-02 Compliance Checker (Unit 7)
Pre-Architecture Review tool that scans all template fields for M-02 violations.

Spec reference: FR8_TTT_Enforcement_Rule_Tech_Spec.md §Layer 1: Authoring Enforcement
                §Authoring quality gate (pre-Architecture Review)
                Task 11: "Create Template Authoring Compliance Checker — pre-Architecture
                          Review tool that scans all template fields for M-02 violations
                          before human review."

This tool is run BEFORE templates enter Architecture Review.
It surfaces M-02 violations with their specific field paths and recovery instructions,
so template authors can correct before submission.

AC11: When C-08 rejects, pipeline interruption is logged with template_id, violated_field,
      recovery_instruction — traceable to specific template for correction.
"""

import json
from pathlib import Path
from typing import Any, Optional

from src.ccp.models.ttt_models import (
    BlockALaw,
    BlockBField,
    C08Result,
    CompiledDesignBrief,
    TTTViolation,
)
from src.ccp.services.c08_ttt_enforcement import C08TTTEnforcement


class TemplateM02ComplianceResult:
    """Result of scanning a template for M-02 compliance.

    Contains compliance status, all detected violations, and
    actionable recovery instructions per field.
    """

    def __init__(
        self,
        template_id: str,
        is_compliant: bool,
        violations: list[TTTViolation],
        c08_result: C08Result,
    ):
        self.template_id = template_id
        self.is_compliant = is_compliant
        self.violations = violations
        self.c08_result = c08_result

    @property
    def violation_count(self) -> int:
        return len(self.violations)

    def to_report(self) -> dict[str, Any]:
        """Produce a structured report dict for display or writing to file."""
        return {
            "template_id": self.template_id,
            "m02_compliant": self.is_compliant,
            "violation_count": self.violation_count,
            "mandate": "M-02",
            "violations": [
                {
                    "check": v.check,
                    "violation_type": v.violation_type.value,
                    "violating_field": v.violating_field,
                    "violating_value": v.violating_value,
                    "matched_pattern": v.matched_pattern,
                    "recovery_instruction": v.recovery_instruction,
                    "pipeline_impact": v.pipeline_impact,
                }
                for v in self.violations
            ],
            "action_required": (
                "None — template is M-02 compliant."
                if self.is_compliant
                else (
                    f"CORRECT {self.violation_count} violation(s) before resubmitting "
                    f"to Architecture Review. Template will be REJECTED by C-08 "
                    f"in the JIT Skill Assembler Tier 0 pre-flight."
                )
            ),
        }

    def __repr__(self) -> str:
        status = "COMPLIANT ✅" if self.is_compliant else f"NON-COMPLIANT ❌ ({self.violation_count} violation(s))"
        return f"TemplateM02ComplianceResult(template_id={self.template_id!r}, status={status})"


class TemplateM02Checker:
    """Pre-Architecture Review M-02 compliance checker for Design Brief Templates.

    Spec §Authoring quality gate (pre-Architecture Review):
    "Template authors must confirm this before submission.
     Violation caught at Architecture Review = template returned to author with M-02 citation."

    Mandate Compliance Checklist item M-02:
    "No TTT value appears in any Block A or Block B field."

    Usage:
        checker = TemplateM02Checker()
        result = checker.scan_template_dict(template_data, template_id="story_transformation_v2")
        if not result.is_compliant:
            print(result.to_report())
    """

    def __init__(self):
        self._c08 = C08TTTEnforcement()

    def scan_template_dict(
        self,
        template_data: dict[str, Any],
        template_id: str = "unknown",
    ) -> TemplateM02ComplianceResult:
        """Scan a template dict for M-02 violations.

        Args:
            template_data: The template dict. Expected keys:
                - "block_b_fields": list of {"name": str, "value": Any} dicts
                - "block_a_structural_laws": list of {"law_id": str, "text": str, "context": str} dicts
                - "compilation_id": optional str (defaults to template_id)
            template_id: Template identifier for reporting.

        Returns:
            TemplateM02ComplianceResult with compliance status and all violations.
        """
        brief = self._parse_template_dict(template_data, template_id)
        c08_result = self._c08.run(brief)

        return TemplateM02ComplianceResult(
            template_id=template_id,
            is_compliant=c08_result.passed,
            violations=c08_result.violations,
            c08_result=c08_result,
        )

    def scan_template_file(
        self,
        template_path: Path,
        template_id: Optional[str] = None,
    ) -> TemplateM02ComplianceResult:
        """Scan a template JSON file for M-02 violations.

        Args:
            template_path: Path to the template JSON file.
            template_id: Optional override for template ID. Defaults to filename stem.

        Returns:
            TemplateM02ComplianceResult.

        Raises:
            FileNotFoundError: If the template file does not exist.
            json.JSONDecodeError: If the file is not valid JSON.
        """
        if not template_path.exists():
            raise FileNotFoundError(f"Template file not found: {template_path}")

        template_data = json.loads(template_path.read_text(encoding="utf-8"))
        tid = template_id or template_path.stem

        return self.scan_template_dict(template_data, tid)

    def scan_template_directory(
        self,
        directory: Path,
        glob_pattern: str = "**/*.json",
    ) -> list[TemplateM02ComplianceResult]:
        """Scan all template files in a directory for M-02 violations.

        Args:
            directory: Directory containing template JSON files.
            glob_pattern: Glob pattern for template files (default: **/*.json).

        Returns:
            List of TemplateM02ComplianceResult, one per template file found.
        """
        results: list[TemplateM02ComplianceResult] = []

        for template_path in sorted(directory.glob(glob_pattern)):
            try:
                result = self.scan_template_file(template_path)
                results.append(result)
            except (json.JSONDecodeError, ValueError) as e:
                # Non-parseable file → create a synthetic non-compliant result
                from src.ccp.models.ttt_models import C08ViolationType
                violation = TTTViolation(
                    violation_type=C08ViolationType.HARDCODED_IN_BLOCK_B,
                    violating_field="<file>",
                    violating_value=str(e)[:200],
                    mandate_violated="M-02",
                    recovery_instruction=f"Template file '{template_path.name}' is not valid JSON. Fix syntax before M-02 scan.",
                )
                from src.ccp.models.ttt_models import C08Status
                c08 = C08Result(
                    status=C08Status.FAIL,
                    violations=[violation],
                    compilation_id=template_path.stem,
                )
                results.append(TemplateM02ComplianceResult(
                    template_id=template_path.stem,
                    is_compliant=False,
                    violations=[violation],
                    c08_result=c08,
                ))

        return results

    def write_compliance_report(
        self,
        results: list[TemplateM02ComplianceResult],
        output_path: Path,
    ) -> None:
        """Write a JSON compliance report for a batch of template scan results.

        Args:
            results: List of TemplateM02ComplianceResult from scanning.
            output_path: Path to write the JSON compliance report.
        """
        compliant = [r for r in results if r.is_compliant]
        non_compliant = [r for r in results if not r.is_compliant]

        report = {
            "m02_compliance_report": {
                "total_templates_scanned": len(results),
                "compliant": len(compliant),
                "non_compliant": len(non_compliant),
                "pass_rate": f"{100 * len(compliant) / len(results):.1f}%" if results else "N/A",
            },
            "templates": {r.template_id: r.to_report() for r in results},
            "action_summary": (
                "All templates are M-02 compliant. Ready for Architecture Review."
                if not non_compliant
                else (
                    f"{len(non_compliant)} template(s) have M-02 violations and must be corrected "
                    f"before Architecture Review submission."
                )
            ),
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(report, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    # ─── Private Helpers ───────────────────────────────────────────────────────

    def _parse_template_dict(
        self, data: dict[str, Any], template_id: str
    ) -> CompiledDesignBrief:
        """Parse a raw template dict into a CompiledDesignBrief for C-08 scanning."""
        # Parse Block B fields
        raw_block_b = data.get("block_b_fields", data.get("block_b", []))
        block_b_fields: list[BlockBField] = []
        for raw_field in raw_block_b:
            if isinstance(raw_field, dict):
                block_b_fields.append(BlockBField(
                    name=str(raw_field.get("name", "unknown_field")),
                    value=raw_field.get("value"),
                    context=raw_field.get("context"),
                ))

        # Parse Block A structural laws
        raw_block_a_laws = data.get("block_a_structural_laws", data.get("structural_laws", []))
        block_a_laws: list[BlockALaw] = []
        for i, raw_law in enumerate(raw_block_a_laws):
            if isinstance(raw_law, dict):
                block_a_laws.append(BlockALaw(
                    law_id=str(raw_law.get("law_id", f"law_{i:02d}")),
                    text=str(raw_law.get("text", "")),
                    context=raw_law.get("context"),
                ))
            elif isinstance(raw_law, str):
                block_a_laws.append(BlockALaw(
                    law_id=f"law_{i:02d}",
                    text=raw_law,
                ))

        return CompiledDesignBrief(
            compilation_id=str(data.get("compilation_id", template_id)),
            archetype_id=str(data.get("archetype_id", template_id)),
            block_b_fields=block_b_fields,
            block_a_structural_laws=block_a_laws,
            dep_eng_005_reference=data.get("dep_eng_005_reference"),
        )
