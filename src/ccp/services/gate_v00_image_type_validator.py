"""
FR-VIS-13 — Gate V-00: Image Type Validity Gate
Phase 2B, CVE Visual Engine — spec 1 of 13

4-stage pre-sourcing gate that validates every slide's image_type
assignment in Abel's VCB before expensive sourcing/generation begins.

Spec Reference: FR-VIS-13_Image_Type_Validity_Gate_Tech_Spec.md
Every function traces to an explicit spec section.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.visual_engine_models import (
    CAROUSEL_FORMAT_PREFIXES,
    IMAGE_TYPE_TO_IMPLIED_STYLES,
    MAX_REVISION_CYCLES,
    OBSERVATIONAL_HUMOR_ALLOWED_TYPES,
    OBSERVATIONAL_HUMOR_FORMATS,
    POLL_ALLOWED_TYPES,
    POLL_FORMATS,
    SQUARE_ALLOWED_FORMATS,
    SUGGESTED_CORRECTIONS,
    VALID_IMAGE_TYPE_VALUES,
    FormatConstraintEnvelope,
    GateV00Result,
    GateV00Verdict,
    GateV00Violation,
    ImageType,
    OperatorReviewStatus,
    SlideValidationSummary,
    StyleConstraintDirective,
    VCBInput,
    VCBSlideAssignment,
    ViolationType,
)


class GateV00ImageTypeValidator:
    """Gate V-00 — Image Type Validity Gate.

    Per FR-VIS-13 §2: pre-sourcing gate that runs BEFORE the standard
    5-gate visual quality sequence (V-01 through V-05). Validates each
    slide's assigned image_type against format and style scoping rules.

    Pipeline position: V-00 → V-01 → V-02 → V-03 → V-04 → V-05
    """

    def __init__(
        self,
        coach_acronym: str,
        receipt_chain: Optional[ReceiptChain] = None,
    ):
        """Initialize Gate V-00 validator.

        Args:
            coach_acronym: ADR-01 coach scope identifier (2-4 chars).
            receipt_chain: Optional ReceiptChain instance for audit logging.
        """
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(
                f"coach_acronym must be 2-4 characters, got {len(coach_acronym)}"
            )
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = receipt_chain or ReceiptChain(
            coach_acronym=self.coach_acronym[:3]
        )

    # ─────────────────────────────────────────────────
    # STAGE 1: VCB Image Type Extraction
    # Spec §4 Stage 1
    # ─────────────────────────────────────────────────

    def _stage1_extract_and_validate_types(
        self, vcb: VCBInput
    ) -> tuple[list[VCBSlideAssignment], list[GateV00Violation]]:
        """Stage 1: Extract per-slide image_type array and validate enum membership.

        Per FR-VIS-13 §4 Stage 1:
        - Step 3: Validate each slide's image_type against the valid enum.
        - Step 4: Missing or invalid image_type → immediate fail.
        - Step 5: Also extract named_person_reference and aspect_ratio_template.

        Returns:
            Tuple of (valid slides, extraction violations).
        """
        violations: list[GateV00Violation] = []
        valid_slides: list[VCBSlideAssignment] = []

        # FR-VIS-13 §6 Backward Compatibility: check for legacy VCBs
        all_missing = all(slide.image_type is None for slide in vcb.slides)
        if all_missing and len(vcb.slides) > 0:
            # Legacy VCB without image_type fields
            for slide in vcb.slides:
                violations.append(
                    GateV00Violation(
                        rule_id="V00-LEGACY",
                        slide_index=slide.slide_index,
                        assigned_image_type=None,
                        violation_type=ViolationType.LEGACY_VCB_UPGRADE_REQUIRED.value,
                        explanation=(
                            "VCB schema version does not include per-slide image_type "
                            "fields. Abel must reprocess with current schema."
                        ),
                        suggested_correction=SUGGESTED_CORRECTIONS[
                            ViolationType.LEGACY_VCB_UPGRADE_REQUIRED.value
                        ],
                    )
                )
            return valid_slides, violations

        for slide in vcb.slides:
            # FR-VIS-13 §4 Stage 1 Step 4: missing image_type
            if slide.image_type is None:
                violations.append(
                    GateV00Violation(
                        rule_id="V00-EXTRACT",
                        slide_index=slide.slide_index,
                        assigned_image_type=None,
                        violation_type=ViolationType.MISSING_IMAGE_TYPE.value,
                        explanation=(
                            f"Slide {slide.slide_index} is missing the required "
                            f"image_type field."
                        ),
                        suggested_correction=SUGGESTED_CORRECTIONS[
                            ViolationType.MISSING_IMAGE_TYPE.value
                        ],
                    )
                )
                continue

            # FR-VIS-13 §4 Stage 1 Step 4: invalid image_type
            if slide.image_type not in VALID_IMAGE_TYPE_VALUES:
                violations.append(
                    GateV00Violation(
                        rule_id="V00-EXTRACT",
                        slide_index=slide.slide_index,
                        assigned_image_type=slide.image_type,
                        violation_type=ViolationType.INVALID_IMAGE_TYPE.value,
                        explanation=(
                            f"Slide {slide.slide_index} has invalid image_type "
                            f"'{slide.image_type}'. Valid types: "
                            f"{sorted(VALID_IMAGE_TYPE_VALUES)}"
                        ),
                        suggested_correction=SUGGESTED_CORRECTIONS[
                            ViolationType.INVALID_IMAGE_TYPE.value
                        ],
                    )
                )
                continue

            valid_slides.append(slide)

        return valid_slides, violations

    # ─────────────────────────────────────────────────
    # STAGE 2: Format-Image Type Cross-Validation
    # Spec §4 Stage 2
    # ─────────────────────────────────────────────────

    def _stage2_format_cross_validation(
        self,
        slides: list[VCBSlideAssignment],
        envelope: FormatConstraintEnvelope,
    ) -> tuple[list[GateV00Violation], dict[int, str]]:
        """Stage 2: Apply rules V00-R01 through V00-R05.

        Per FR-VIS-13 §4 Stage 2:
        - Collects ALL violations (does not halt on first).
        - Returns violations array and per-slide format_check status.

        Returns:
            Tuple of (violations list, {slide_index: "PASS"|"FAIL"}).
        """
        violations: list[GateV00Violation] = []
        format_checks: dict[int, str] = {}
        content_format = envelope.content_format
        aspect_ratio = envelope.aspect_ratio

        is_carousel = any(
            content_format.startswith(prefix)
            for prefix in CAROUSEL_FORMAT_PREFIXES
        )
        is_obs_humor = content_format in OBSERVATIONAL_HUMOR_FORMATS
        is_poll = content_format in POLL_FORMATS

        for slide in slides:
            slide_failed = False
            image_type = slide.image_type

            # V00-R01: Carousel slides cannot use tier_4_ai_ghibli
            # FR-VIS-13 §4 Stage 2 Rule V00-R01
            if is_carousel and image_type == ImageType.TIER_4_AI_GHIBLI.value:
                violations.append(
                    GateV00Violation(
                        rule_id="V00-R01",
                        slide_index=slide.slide_index,
                        assigned_image_type=image_type,
                        violation_type=ViolationType.CAROUSEL_GHIBLI_VIOLATION.value,
                        explanation=(
                            f"Carousel slides cannot use Ghibli/illustrated image "
                            f"types. Slide {slide.slide_index} was assigned "
                            f"'{image_type}' but carousels require cinematic or "
                            f"semi-realistic styles only."
                        ),
                        suggested_correction=SUGGESTED_CORRECTIONS[
                            ViolationType.CAROUSEL_GHIBLI_VIOLATION.value
                        ],
                    )
                )
                slide_failed = True

            # V00-R02: Observational Humor — never AI-generated
            # FR-VIS-13 §4 Stage 2 Rule V00-R02
            if is_obs_humor and image_type not in OBSERVATIONAL_HUMOR_ALLOWED_TYPES:
                violations.append(
                    GateV00Violation(
                        rule_id="V00-R02",
                        slide_index=slide.slide_index,
                        assigned_image_type=image_type,
                        violation_type=ViolationType.OBSERVATIONAL_HUMOR_AI_VIOLATION.value,
                        explanation=(
                            f"Observational Humor slides must use tier_1_real_person "
                            f"or tier_2_stock_* types only. Slide {slide.slide_index} "
                            f"was assigned '{image_type}' which is AI-generated."
                        ),
                        suggested_correction=SUGGESTED_CORRECTIONS[
                            ViolationType.OBSERVATIONAL_HUMOR_AI_VIOLATION.value
                        ],
                    )
                )
                slide_failed = True

            # V00-R03: Named person slides must use tier_1_real_person
            # FR-VIS-13 §4 Stage 2 Rule V00-R03
            if (
                slide.named_person_reference is not None
                and slide.named_person_reference.strip() != ""
                and image_type != ImageType.TIER_1_REAL_PERSON.value
            ):
                violations.append(
                    GateV00Violation(
                        rule_id="V00-R03",
                        slide_index=slide.slide_index,
                        assigned_image_type=image_type,
                        violation_type=ViolationType.NAMED_PERSON_TIER_VIOLATION.value,
                        explanation=(
                            f"Slide {slide.slide_index} references named person "
                            f"'{slide.named_person_reference}' but uses "
                            f"'{image_type}'. Named person slides must use "
                            f"'tier_1_real_person' to source licensed real photographs."
                        ),
                        suggested_correction=SUGGESTED_CORRECTIONS[
                            ViolationType.NAMED_PERSON_TIER_VIOLATION.value
                        ],
                    )
                )
                slide_failed = True

            # V00-R04: Poll option zones — never photographic
            # FR-VIS-13 §4 Stage 2 Rule V00-R04
            if is_poll and image_type not in POLL_ALLOWED_TYPES:
                violations.append(
                    GateV00Violation(
                        rule_id="V00-R04",
                        slide_index=slide.slide_index,
                        assigned_image_type=image_type,
                        violation_type=ViolationType.POLL_PHOTOGRAPHIC_VIOLATION.value,
                        explanation=(
                            f"Poll option zones must use graphic_vector or "
                            f"tier_3_ai_realistic only. Slide {slide.slide_index} "
                            f"was assigned '{image_type}' which is photographic."
                        ),
                        suggested_correction=SUGGESTED_CORRECTIONS[
                            ViolationType.POLL_PHOTOGRAPHIC_VIOLATION.value
                        ],
                    )
                )
                slide_failed = True

            # V00-R05: 1:1 aspect ratio only for approved formats
            # FR-VIS-13 §4 Stage 2 Rule V00-R05
            if (
                aspect_ratio == "1:1"
                and content_format not in SQUARE_ALLOWED_FORMATS
            ):
                violations.append(
                    GateV00Violation(
                        rule_id="V00-R05",
                        slide_index=slide.slide_index,
                        assigned_image_type=image_type,
                        violation_type=ViolationType.ASPECT_RATIO_FORMAT_VIOLATION.value,
                        explanation=(
                            f"1:1 aspect ratio is only available for approved formats: "
                            f"{sorted(SQUARE_ALLOWED_FORMATS)}. Content format "
                            f"'{content_format}' is not in the approved list."
                        ),
                        suggested_correction=SUGGESTED_CORRECTIONS[
                            ViolationType.ASPECT_RATIO_FORMAT_VIOLATION.value
                        ],
                    )
                )
                slide_failed = True

            format_checks[slide.slide_index] = "FAIL" if slide_failed else "PASS"

        return violations, format_checks

    # ─────────────────────────────────────────────────
    # STAGE 3: Style-Image Type Cross-Validation
    # Spec §4 Stage 3
    # ─────────────────────────────────────────────────

    def _stage3_style_cross_validation(
        self,
        slides: list[VCBSlideAssignment],
        directive: StyleConstraintDirective,
    ) -> tuple[list[GateV00Violation], dict[int, str]]:
        """Stage 3: Map image_type → implied style and check against directive.

        Per FR-VIS-13 §4 Stage 3:
        - Step 1: Map each slide's image_type to implied style(s).
        - Step 2: Check implied styles against permitted/prohibited.
        - Step 3: STYLE_IMAGE_TYPE_CONFLICT if implied style is prohibited.
        - Step 4: MANDATORY_STYLE_CONFLICT if mandatory_style doesn't match.

        Returns:
            Tuple of (violations list, {slide_index: "PASS"|"FAIL"}).
        """
        violations: list[GateV00Violation] = []
        style_checks: dict[int, str] = {}

        for slide in slides:
            slide_failed = False
            image_type = slide.image_type
            assert image_type is not None, "Stage 3 only receives validated slides"

            # Step 1: Get implied styles for this image_type
            implied_styles = IMAGE_TYPE_TO_IMPLIED_STYLES.get(image_type, [])

            # Step 2-3: Check if any implied style is in prohibited_styles
            for implied_style in implied_styles:
                if implied_style in directive.prohibited_styles:
                    violations.append(
                        GateV00Violation(
                            rule_id="V00-STYLE",
                            slide_index=slide.slide_index,
                            assigned_image_type=image_type,
                            violation_type=ViolationType.STYLE_IMAGE_TYPE_CONFLICT.value,
                            explanation=(
                                f"Slide {slide.slide_index} has image_type "
                                f"'{image_type}' which implies style "
                                f"'{implied_style}', but this style is prohibited "
                                f"by the style directive."
                            ),
                            suggested_correction=SUGGESTED_CORRECTIONS[
                                ViolationType.STYLE_IMAGE_TYPE_CONFLICT.value
                            ],
                        )
                    )
                    slide_failed = True
                    break  # One style conflict per slide is sufficient

            # Step 4: Check mandatory_style match
            if directive.mandatory_style is not None:
                if directive.mandatory_style not in implied_styles:
                    violations.append(
                        GateV00Violation(
                            rule_id="V00-STYLE",
                            slide_index=slide.slide_index,
                            assigned_image_type=image_type,
                            violation_type=ViolationType.MANDATORY_STYLE_CONFLICT.value,
                            explanation=(
                                f"Slide {slide.slide_index} has image_type "
                                f"'{image_type}' which implies styles "
                                f"{implied_styles}, but the mandatory style "
                                f"'{directive.mandatory_style}' is not among them."
                            ),
                            suggested_correction=SUGGESTED_CORRECTIONS[
                                ViolationType.MANDATORY_STYLE_CONFLICT.value
                            ],
                        )
                    )
                    slide_failed = True

            style_checks[slide.slide_index] = "FAIL" if slide_failed else "PASS"

        return violations, style_checks

    # ─────────────────────────────────────────────────
    # STAGE 4: Gate V-00 Verdict
    # Spec §4 Stage 4
    # ─────────────────────────────────────────────────

    def _stage4_verdict(
        self,
        vcb: VCBInput,
        all_violations: list[GateV00Violation],
        slide_summaries: list[SlideValidationSummary],
        violation_history: Optional[list[list[GateV00Violation]]] = None,
    ) -> GateV00Result:
        """Stage 4: Determine PASS/FAIL/ESCALATE verdict.

        Per FR-VIS-13 §4 Stage 4:
        - Step 1: Empty violations → GATE_V00_PASS, forward to V-01.
        - Step 2: Non-empty + revision_count < 2 → GATE_V00_FAIL, return to Abel.
        - Step 3: Non-empty + revision_count >= 2 → GATE_V00_ESCALATE.
        """
        if len(all_violations) == 0:
            verdict = GateV00Verdict.GATE_V00_PASS.value
            operator_status = None
            history = None
        elif vcb.revision_count < MAX_REVISION_CYCLES:
            verdict = GateV00Verdict.GATE_V00_FAIL.value
            operator_status = None
            history = None
        else:
            verdict = GateV00Verdict.GATE_V00_ESCALATE.value
            operator_status = OperatorReviewStatus.PENDING_OPERATOR_REVIEW.value
            history = violation_history

        return GateV00Result(
            content_output_id=vcb.content_output_id,
            content_format=vcb.format_envelope.content_format,
            verdict=verdict,
            revision_count=vcb.revision_count,
            violations=all_violations,
            slide_validation_summary=slide_summaries,
            format_envelope_id=vcb.format_envelope.envelope_id,
            style_directive_id=vcb.style_directive.directive_id,
            operator_review_status=operator_status,
            violation_history=history,
        )

    # ─────────────────────────────────────────────────
    # RECEIPT CHAIN INTEGRATION
    # Spec §4 Receipt Writes at each stage
    # ─────────────────────────────────────────────────

    def _write_receipt(
        self,
        stage_name: str,
        vcb_id: str,
        content_output_id: str,
        input_summary: str,
        output_summary: str,
        decision: str,
        decision_rationale: str,
        parent_receipt_id: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> str:
        """Write a receipt to the chain per FR47 DEP-ENG-041 schema.

        Returns:
            The receipt_id of the written receipt.
        """
        entry = self.receipt_chain.log(
            agent_id="gate_v00_validator",
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
    # PUBLIC API — Full Gate V-00 Execution
    # ─────────────────────────────────────────────────

    def validate(
        self,
        vcb: VCBInput,
        violation_history: Optional[list[list[GateV00Violation]]] = None,
    ) -> GateV00Result:
        """Execute the full 4-stage Gate V-00 validation pipeline.

        Per FR-VIS-13 §4:
        - Stage 1: Extract and validate image types.
        - Stage 2: Format-image type cross-validation.
        - Stage 3: Style-image type cross-validation.
        - Stage 4: Determine verdict.

        Args:
            vcb: The complete VCB input from Abel.
            violation_history: Previous violation lists from earlier revision
                attempts (used for escalation reporting).

        Returns:
            GateV00Result with verdict, violations, and slide summaries.
        """
        # ── STAGE 1: VCB Image Type Extraction ──
        # FR-VIS-13 §4 Stage 1
        valid_slides, extraction_violations = self._stage1_extract_and_validate_types(vcb)

        # Receipt Write: Stage 1
        extraction_receipt_id = self._write_receipt(
            stage_name="GATE_V00_EXTRACTION",
            vcb_id=vcb.vcb_id,
            content_output_id=vcb.content_output_id,
            input_summary=(
                f"VCB {vcb.vcb_id} with {len(vcb.slides)} slides, "
                f"format={vcb.format_envelope.content_format}"
            ),
            output_summary=(
                f"Extracted {len(valid_slides)} valid slides, "
                f"{len(extraction_violations)} extraction violations"
            ),
            decision="extraction_complete",
            decision_rationale=(
                f"{len(extraction_violations)} type errors found during extraction"
                if extraction_violations
                else "All slides have valid image_type enum values"
            ),
            metadata={
                "vcb_id": vcb.vcb_id,
                "total_slides": len(vcb.slides),
                "valid_slides": len(valid_slides),
                "extraction_violation_count": len(extraction_violations),
            },
        )

        # If all slides have extraction violations (e.g. legacy VCB), skip stages 2-3
        all_violations: list[GateV00Violation] = list(extraction_violations)
        format_checks: dict[int, str] = {}
        style_checks: dict[int, str] = {}

        if valid_slides:
            # ── STAGE 2: Format-Image Type Cross-Validation ──
            # FR-VIS-13 §4 Stage 2
            format_violations, format_checks = self._stage2_format_cross_validation(
                valid_slides, vcb.format_envelope
            )
            all_violations.extend(format_violations)

            # ── STAGE 3: Style-Image Type Cross-Validation ──
            # FR-VIS-13 §4 Stage 3
            style_violations, style_checks = self._stage3_style_cross_validation(
                valid_slides, vcb.style_directive
            )
            all_violations.extend(style_violations)

        # Receipt Write: Stages 2+3 cross-validation
        xval_receipt_id = self._write_receipt(
            stage_name="GATE_V00_CROSS_VALIDATION",
            vcb_id=vcb.vcb_id,
            content_output_id=vcb.content_output_id,
            input_summary=(
                f"{len(valid_slides)} valid slides cross-validated against "
                f"format={vcb.format_envelope.content_format}, "
                f"style_directive={vcb.style_directive.directive_id}"
            ),
            output_summary=(
                f"Total violations after cross-validation: {len(all_violations)}"
            ),
            decision="cross_validation_complete",
            decision_rationale=(
                f"{len(all_violations)} total violations found"
                if all_violations
                else "No violations — all slides pass format and style checks"
            ),
            parent_receipt_id=extraction_receipt_id,
            metadata={
                "format_violations": len(all_violations) - len(extraction_violations),
                "style_violations": len(style_checks) - sum(
                    1 for v in style_checks.values() if v == "PASS"
                ) if style_checks else 0,
                "total_violations": len(all_violations),
            },
        )

        # Build per-slide validation summaries
        # FR-VIS-13 §5: slide_validation_summary
        slide_summaries: list[SlideValidationSummary] = []
        for slide in vcb.slides:
            idx = slide.slide_index
            slide_summaries.append(
                SlideValidationSummary(
                    slide_index=idx,
                    image_type=slide.image_type,
                    format_check=format_checks.get(idx, "FAIL"),
                    style_check=style_checks.get(idx, "FAIL"),
                )
            )

        # Fix: slides that passed extraction but weren't in format/style checks
        # (because they had extraction violations) should show FAIL
        extraction_violation_indices = {
            v.slide_index for v in extraction_violations
        }
        for summary in slide_summaries:
            if summary.slide_index in extraction_violation_indices:
                summary.format_check = "FAIL"
                summary.style_check = "FAIL"

        # ── STAGE 4: Gate V-00 Verdict ──
        # FR-VIS-13 §4 Stage 4
        result = self._stage4_verdict(
            vcb=vcb,
            all_violations=all_violations,
            slide_summaries=slide_summaries,
            violation_history=violation_history,
        )

        # Receipt Write: Stage 4 verdict
        verdict_receipt_id = self._write_receipt(
            stage_name="GATE_V00_VERDICT",
            vcb_id=vcb.vcb_id,
            content_output_id=vcb.content_output_id,
            input_summary=f"{len(all_violations)} violations evaluated",
            output_summary=f"Verdict: {result.verdict}",
            decision=result.verdict,
            decision_rationale=(
                f"revision_count={vcb.revision_count}, "
                f"violation_count={len(all_violations)}, "
                f"max_revisions={MAX_REVISION_CYCLES}"
            ),
            parent_receipt_id=xval_receipt_id,
            metadata={
                "gate_id": result.gate_id,
                "verdict": result.verdict,
                "violation_count": len(all_violations),
                "revision_count": vcb.revision_count,
                "operator_review_status": result.operator_review_status,
            },
        )

        # Set the receipt chain block on the result
        result.receipt_chain_block = verdict_receipt_id

        return result

    # ─────────────────────────────────────────────────
    # REVISION CYCLE MANAGEMENT
    # Spec §4 Stage 4 Steps 2-3 + §3 Technical Decision 3
    # ─────────────────────────────────────────────────

    def validate_with_revision_tracking(
        self,
        vcb: VCBInput,
        previous_violations: Optional[list[list[GateV00Violation]]] = None,
    ) -> GateV00Result:
        """Execute Gate V-00 with full revision cycle tracking.

        Per FR-VIS-13 §3 Technical Decision 3:
        - Tracks violation_history across revision attempts.
        - On second failure (revision_count >= 2), includes full history.

        Args:
            vcb: The VCB to validate (revision_count already set).
            previous_violations: Violation lists from prior revision attempts.

        Returns:
            GateV00Result with appropriate verdict and history.
        """
        history = list(previous_violations) if previous_violations else []

        result = self.validate(vcb, violation_history=history or None)

        # If this attempt also failed, add current violations to history
        if result.verdict != GateV00Verdict.GATE_V00_PASS.value and result.violations:
            history.append(list(result.violations))

        # If escalating, attach the full history
        if result.verdict == GateV00Verdict.GATE_V00_ESCALATE.value:
            result.violation_history = history

        return result
