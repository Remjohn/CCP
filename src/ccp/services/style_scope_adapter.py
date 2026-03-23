"""
FR-VIS-08 — Style Scope Adapter
Phase 2B, CVE Visual Engine — spec 3 of 13

Style scoping enforcement layer that fires AFTER format locking (FR-VIS-07).
Evaluates the content_format against the Style_Scope_Matrix and emits a
sealed style_constraint_directive specifying permitted, prohibited, and
mandatory visual styles plus grammar system routing.

Spec Reference: FR-VIS-08_Style_Scoping_Tech_Spec.md
Every function traces to an explicit spec section.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.visual_engine_models import (
    FormatConstraintEnvelope,
    StyleConstraintDirective,
    StyleParameters,
    StyleScopeError,
    StyleScopeMatrixEntry,
    StyleValidationResult,
)


# ─────────────────────────────────────────────────────
# MATRIX PATH — default location per FR-VIS-08 §7 Task 1
# ─────────────────────────────────────────────────────

DEFAULT_MATRIX_PATH = Path("config/visual_pipeline/style_scope_matrix.json")

# ─────────────────────────────────────────────────────
# LEGACY CONSERVATIVE DEFAULTS — FR-VIS-08 §6
# ─────────────────────────────────────────────────────

_LEGACY_CAROUSEL_DEFAULT = StyleScopeMatrixEntry(
    permitted_styles=["cinematic_color_graded", "semi_realistic_digital"],
    prohibited_styles=["ghibli_illustration", "watercolor", "vector_flat", "real_photography_only"],
    mandatory_style=None,
    style_parameters=StyleParameters(grammar_system="cinematic"),
)

_LEGACY_SINGLE_DEFAULT = StyleScopeMatrixEntry(
    permitted_styles=["cinematic_color_graded", "semi_realistic_digital"],
    prohibited_styles=["ghibli_illustration", "watercolor", "vector_flat", "real_photography_only"],
    mandatory_style=None,
    style_parameters=StyleParameters(grammar_system="cinematic"),
)


class StyleScopeAdapter:
    """Style Scope Adapter — FR-VIS-08.

    Per FR-VIS-08 §2: extends the visual pipeline with a style scoping
    enforcement layer. After format constraints are locked (FR-VIS-07),
    the style scoping layer evaluates the content_format against the
    Style_Scope_Matrix and emits a style_constraint_directive.

    Pipeline position: VIS-07 → VIS-08 (this) → VIS-01 → VIS-13 → ...
    """

    def __init__(
        self,
        coach_acronym: str,
        receipt_chain: Optional[ReceiptChain] = None,
        matrix_path: Optional[Path] = None,
    ):
        """Initialize the style scope adapter.

        Args:
            coach_acronym: ADR-01 coach scope identifier (2-4 chars).
            receipt_chain: Optional ReceiptChain for audit logging.
            matrix_path: Path to the style scope matrix JSON.
        """
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(
                f"coach_acronym must be 2-4 characters, got {len(coach_acronym)}"
            )
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = receipt_chain or ReceiptChain(
            coach_acronym=self.coach_acronym[:3]
        )
        self.matrix_path = matrix_path or DEFAULT_MATRIX_PATH
        self._matrix: dict[str, StyleScopeMatrixEntry] = {}
        self._load_matrix()

    # ─────────────────────────────────────────────────
    # MATRIX LOADING — FR-VIS-08 §7 Task 1
    # ─────────────────────────────────────────────────

    def _load_matrix(self) -> None:
        """Load and validate the Style_Scope_Matrix from JSON."""
        with open(self.matrix_path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        formats_section = raw.get("formats", raw)

        for format_name, entry_data in formats_section.items():
            if format_name.startswith("_"):
                continue
            # Parse style_parameters sub-object
            sp_data = entry_data.get("style_parameters", {})
            style_params = StyleParameters(**sp_data)
            self._matrix[format_name] = StyleScopeMatrixEntry(
                permitted_styles=entry_data["permitted_styles"],
                prohibited_styles=entry_data.get("prohibited_styles", []),
                mandatory_style=entry_data.get("mandatory_style"),
                style_parameters=style_params,
            )

    def get_matrix(self) -> dict[str, StyleScopeMatrixEntry]:
        """Return the loaded style matrix (for testing/inspection)."""
        return dict(self._matrix)

    # ─────────────────────────────────────────────────
    # RECEIPT CHAIN INTEGRATION
    # ─────────────────────────────────────────────────

    def _write_receipt(
        self,
        stage_name: str,
        content_output_id: str,
        input_summary: str,
        output_summary: str,
        decision: str,
        decision_rationale: str,
        parent_receipt_id: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> str:
        """Write a receipt per FR47 DEP-ENG-041."""
        entry = self.receipt_chain.log(
            agent_id="style_scope_adapter",
            action=stage_name,
            asset_id=content_output_id,
            input_summary=input_summary,
            output_summary=output_summary,
            decision=decision,
            decision_rationale=decision_rationale,
            parent_receipt_id=parent_receipt_id,
            metadata=metadata or {},
        )
        return entry.receipt_id

    # ─────────────────────────────────────────────────
    # STAGE 1: Style Matrix Evaluation
    # FR-VIS-08 §4 Stage 1
    # ─────────────────────────────────────────────────

    def _stage1_evaluate_matrix(
        self,
        content_format: str,
    ) -> tuple[Optional[StyleScopeMatrixEntry], list[str]]:
        """Stage 1: Look up the content format in the Style_Scope_Matrix.

        Per FR-VIS-08 §4 Stage 1 Steps 1-5.
        Per FR-VIS-08 §6: legacy fallback for unresolved formats.

        Returns:
            Tuple of (matrix entry or None, warnings list).
        """
        warnings: list[str] = []

        entry = self._matrix.get(content_format)
        if entry is not None:
            return entry, warnings

        # FR-VIS-08 §6: Legacy conservative default
        if content_format.startswith("carousel"):
            warnings.append(
                f"LEGACY_STYLE_DEFAULT: Format '{content_format}' not in Style_Scope_Matrix. "
                f"Applying conservative carousel default: "
                f"permitted=['cinematic_color_graded', 'semi_realistic_digital'], "
                f"all illustrated styles prohibited."
            )
            return _LEGACY_CAROUSEL_DEFAULT, warnings
        elif content_format.startswith(("single", "poll", "nine_grid")):
            warnings.append(
                f"LEGACY_STYLE_DEFAULT: Format '{content_format}' not in Style_Scope_Matrix. "
                f"Applying conservative single/default: "
                f"permitted=['cinematic_color_graded', 'semi_realistic_digital'], "
                f"Ghibli and real_photography_only excluded."
            )
            return _LEGACY_SINGLE_DEFAULT, warnings

        # Truly unrecognized format — should not happen if VIS-07 validated
        return None, warnings

    # ─────────────────────────────────────────────────
    # STAGE 2: Saturation Ceiling Injection + Seal
    # FR-VIS-08 §4 Stage 2
    # ─────────────────────────────────────────────────

    def _stage2_assemble_directive(
        self,
        content_format: str,
        content_output_id: str,
        envelope: FormatConstraintEnvelope,
        matrix_entry: StyleScopeMatrixEntry,
    ) -> StyleConstraintDirective:
        """Stage 2: Assemble and seal the style_constraint_directive.

        Per FR-VIS-08 §4 Stage 2 Steps 1-3:
        - Embed saturation ceiling/floor from style_parameters.
        - Set grammar_system.
        - Seal with SHA-256 hash.
        """
        sp = matrix_entry.style_parameters
        timestamp = datetime.now(timezone.utc).isoformat()

        directive = StyleConstraintDirective(
            content_format=content_format,
            content_output_id=content_output_id,
            format_constraint_envelope_id=envelope.envelope_id,
            permitted_styles=list(matrix_entry.permitted_styles),
            prohibited_styles=list(matrix_entry.prohibited_styles),
            mandatory_style=matrix_entry.mandatory_style,
            grammar_system=sp.grammar_system,
            saturation_ceiling_pct=sp.saturation_ceiling_pct,
            saturation_floor_pct=sp.saturation_floor_pct,
            timestamp_utc=timestamp,
        )

        # SHA-256 seal
        seal_payload = directive.model_dump_json(
            exclude={"seal_hash", "receipt_chain_block"}
        )
        directive.seal_hash = hashlib.sha256(
            seal_payload.encode("utf-8")
        ).hexdigest()

        return directive

    # ─────────────────────────────────────────────────
    # SEAL VERIFICATION
    # FR-VIS-08 §10 Safety: Directive Tampering Detection
    # ─────────────────────────────────────────────────

    @staticmethod
    def verify_seal(directive: StyleConstraintDirective) -> bool:
        """Verify the SHA-256 seal hash of a directive.

        Returns True if the directive has not been tampered with.
        """
        if directive.seal_hash is None:
            return False
        expected_payload = directive.model_dump_json(
            exclude={"seal_hash", "receipt_chain_block"}
        )
        expected_hash = hashlib.sha256(
            expected_payload.encode("utf-8")
        ).hexdigest()
        return expected_hash == directive.seal_hash

    # ─────────────────────────────────────────────────
    # PUBLIC API — Scope Style
    # FR-VIS-08 §4 Stages 1-2
    # ─────────────────────────────────────────────────

    def scope(
        self,
        envelope: FormatConstraintEnvelope,
        content_output_id: str,
    ) -> tuple[Optional[StyleConstraintDirective], Optional[str], list[str]]:
        """Execute Stages 1-2: evaluate matrix and assemble sealed directive.

        Args:
            envelope: Sealed format constraint envelope from FR-VIS-07.
            content_output_id: Content output ID for traceability.

        Returns:
            Tuple of (sealed directive or None, error_type or None, warnings).
        """
        content_format = envelope.content_format

        # ── STAGE 1: Matrix Evaluation ──
        matrix_entry, warnings = self._stage1_evaluate_matrix(content_format)

        # Receipt Write: Stage 1
        stage1_receipt_id = self._write_receipt(
            stage_name="VIS08_STYLE_MATRIX_EVAL",
            content_output_id=content_output_id,
            input_summary=(
                f"Content format '{content_format}' from envelope "
                f"{envelope.envelope_id}"
            ),
            output_summary=(
                f"Matrix entry found: permitted={matrix_entry.permitted_styles}, "
                f"mandatory={matrix_entry.mandatory_style}, "
                f"grammar={matrix_entry.style_parameters.grammar_system}"
                if matrix_entry
                else f"FORMAT_NOT_IN_MATRIX: '{content_format}'"
            ),
            decision="matrix_match" if matrix_entry else "matrix_miss",
            decision_rationale=(
                f"Format '{content_format}' resolved in style matrix"
                if matrix_entry
                else f"Format '{content_format}' not found in matrix and no legacy default"
            ),
            metadata={
                "content_format": content_format,
                "envelope_id": envelope.envelope_id,
                "matrix_hit": matrix_entry is not None,
                "warnings": warnings,
            },
        )

        if matrix_entry is None:
            return None, StyleScopeError.FORMAT_NOT_IN_MATRIX.value, warnings

        # ── STAGE 2: Directive Assembly + Saturation Injection ──
        directive = self._stage2_assemble_directive(
            content_format=content_format,
            content_output_id=content_output_id,
            envelope=envelope,
            matrix_entry=matrix_entry,
        )

        # Receipt Write: Stage 2
        stage2_receipt_id = self._write_receipt(
            stage_name="VIS08_DIRECTIVE_ASSEMBLY",
            content_output_id=content_output_id,
            input_summary=(
                f"Matrix entry for '{content_format}', "
                f"saturation_ceiling={matrix_entry.style_parameters.saturation_ceiling_pct}"
            ),
            output_summary=(
                f"Directive {directive.directive_id}: "
                f"grammar={directive.grammar_system}, "
                f"seal={(directive.seal_hash or '')[:16]}..."
            ),
            decision="directive_assembled",
            decision_rationale=(
                f"Style directive sealed for '{content_format}' with "
                f"grammar_system='{directive.grammar_system}'"
            ),
            parent_receipt_id=stage1_receipt_id,
            metadata={
                "directive_id": directive.directive_id,
                "grammar_system": directive.grammar_system,
                "mandatory_style": directive.mandatory_style,
                "saturation_ceiling_pct": directive.saturation_ceiling_pct,
                "saturation_floor_pct": directive.saturation_floor_pct,
                "seal_hash": directive.seal_hash,
            },
        )

        directive.receipt_chain_block = stage2_receipt_id

        return directive, None, warnings

    # ─────────────────────────────────────────────────
    # STAGE 3: Pre-Abel Style Validation Gate
    # FR-VIS-08 §4 Stage 3
    # ─────────────────────────────────────────────────

    def validate_style_assignment(
        self,
        directive: StyleConstraintDirective,
        assigned_style: str,
        saturation_pct: Optional[int] = None,
    ) -> StyleValidationResult:
        """Stage 3: Validate Abel's style assignment against the directive.

        Per FR-VIS-08 §4 Stage 3 Steps 1-6:
        - Check mandatory_style match
        - Check prohibited_styles exclusion
        - Check permitted_styles membership
        - Check saturation ceiling/floor

        Args:
            directive: The sealed style constraint directive.
            assigned_style: The visual_style Abel assigned in the VCB.
            saturation_pct: Optional saturation percentage from PSSL params.

        Returns:
            StyleValidationResult with pass/fail and error details.
        """
        content_format = directive.content_format or "unknown"

        # FR-VIS-08 §4 Stage 3 Step 3: Mandatory style check
        if directive.mandatory_style is not None:
            if assigned_style != directive.mandatory_style:
                result = StyleValidationResult(
                    valid=False,
                    error_type=StyleScopeError.STYLE_VIOLATION.value,
                    error_detail=(
                        f"STYLE_VIOLATION — mandatory style is "
                        f"'{directive.mandatory_style}', received "
                        f"'{assigned_style}'"
                    ),
                    content_format=content_format,
                    assigned_style=assigned_style,
                    permitted_styles=list(directive.permitted_styles),
                )
                self._write_validation_receipt(
                    directive, assigned_style, result, saturation_pct
                )
                return result

        # FR-VIS-08 §4 Stage 3 Step 4: Prohibited style check
        if assigned_style in directive.prohibited_styles:
            result = StyleValidationResult(
                valid=False,
                error_type=StyleScopeError.STYLE_VIOLATION.value,
                error_detail=(
                    f"STYLE_VIOLATION — style '{assigned_style}' is prohibited "
                    f"for format '{content_format}'. "
                    f"Permitted: {directive.permitted_styles}"
                ),
                content_format=content_format,
                assigned_style=assigned_style,
                permitted_styles=list(directive.permitted_styles),
            )
            self._write_validation_receipt(
                directive, assigned_style, result, saturation_pct
            )
            return result

        # Check permitted_styles membership
        if assigned_style not in directive.permitted_styles:
            result = StyleValidationResult(
                valid=False,
                error_type=StyleScopeError.STYLE_VIOLATION.value,
                error_detail=(
                    f"STYLE_VIOLATION — style '{assigned_style}' is not in "
                    f"permitted styles for format '{content_format}'. "
                    f"Permitted: {directive.permitted_styles}"
                ),
                content_format=content_format,
                assigned_style=assigned_style,
                permitted_styles=list(directive.permitted_styles),
            )
            self._write_validation_receipt(
                directive, assigned_style, result, saturation_pct
            )
            return result

        # FR-VIS-08 §4 Stage 3 Step 5: Saturation check
        if saturation_pct is not None:
            ceiling = directive.saturation_ceiling_pct
            floor = directive.saturation_floor_pct
            if ceiling is not None and saturation_pct > ceiling:
                result = StyleValidationResult(
                    valid=False,
                    error_type=StyleScopeError.SATURATION_VIOLATION.value,
                    error_detail=(
                        f"SATURATION_VIOLATION — maximum {ceiling}%, "
                        f"received {saturation_pct}%"
                    ),
                    content_format=content_format,
                    assigned_style=assigned_style,
                    permitted_styles=list(directive.permitted_styles),
                )
                self._write_validation_receipt(
                    directive, assigned_style, result, saturation_pct
                )
                return result
            if floor is not None and saturation_pct < floor:
                result = StyleValidationResult(
                    valid=False,
                    error_type=StyleScopeError.SATURATION_VIOLATION.value,
                    error_detail=(
                        f"SATURATION_VIOLATION — minimum {floor}%, "
                        f"received {saturation_pct}%"
                    ),
                    content_format=content_format,
                    assigned_style=assigned_style,
                    permitted_styles=list(directive.permitted_styles),
                )
                self._write_validation_receipt(
                    directive, assigned_style, result, saturation_pct
                )
                return result

        # FR-VIS-08 §4 Stage 3 Step 6: All checks pass
        result = StyleValidationResult(
            valid=True,
            content_format=content_format,
            assigned_style=assigned_style,
            permitted_styles=list(directive.permitted_styles),
        )
        self._write_validation_receipt(
            directive, assigned_style, result, saturation_pct
        )
        return result

    def _write_validation_receipt(
        self,
        directive: StyleConstraintDirective,
        assigned_style: str,
        result: StyleValidationResult,
        saturation_pct: Optional[int],
    ) -> None:
        """Write receipt for pre-Abel validation gate (Stage 3)."""
        self._write_receipt(
            stage_name="VIS08_PRE_ABEL_VALIDATION",
            content_output_id=directive.content_output_id or "unknown",
            input_summary=(
                f"Style assignment: '{assigned_style}', "
                f"saturation_pct={saturation_pct}, "
                f"directive={directive.directive_id}"
            ),
            output_summary=(
                "STYLE_VALID" if result.valid
                else f"{result.error_type}: {result.error_detail}"
            ),
            decision="style_valid" if result.valid else "style_rejected",
            decision_rationale=(
                f"Style '{assigned_style}' passes all checks for "
                f"'{directive.content_format}'"
                if result.valid
                else result.error_detail or "Unknown violation"
            ),
            parent_receipt_id=directive.receipt_chain_block,
            metadata={
                "directive_id": directive.directive_id,
                "assigned_style": assigned_style,
                "saturation_pct": saturation_pct,
                "valid": result.valid,
                "error_type": result.error_type,
            },
        )
