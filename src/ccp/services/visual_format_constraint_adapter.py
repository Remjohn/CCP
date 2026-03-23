"""
FR-VIS-07 — Visual Format Constraint Adapter
Phase 2B, CVE Visual Engine — spec 2 of 13

Deterministic pre-production gate that fires BEFORE any other style
selection, recipe protocol, or image sourcing logic. Reads the format
designation from upstream script output (DEP-ENG-011) and emits a locked
format_constraint_envelope with exact pixel dimensions, aspect ratio,
DPI, and color space for every slide.

Spec Reference: FR-VIS-07_Format_Aspect_Ratio_Enforcement_Tech_Spec.md
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
    ContentOutputInput,
    FormatAdapterError,
    FormatAdapterResult,
    FormatConstraintEnvelope,
    FormatRegistryEntry,
    PerSlideDimension,
    RECIPE_ID_TO_FORMAT,
)


# ─────────────────────────────────────────────────────
# REGISTRY PATH — default location per FR-VIS-07 §7 Task 1
# ─────────────────────────────────────────────────────

DEFAULT_REGISTRY_PATH = Path("config/visual_pipeline/format_constraint_registry.json")


class VisualFormatConstraintAdapter:
    """Visual Format Constraint Adapter — FR-VIS-07.

    Per FR-VIS-07 §2: deterministic pre-production gate that fires as
    the absolute first operation in the visual pipeline. Reads format
    designation, validates against the Format_Constraint_Registry, and
    emits a sealed format_constraint_envelope.

    Pipeline position: VIS-07 (this) → VIS-08 → VIS-01 → VIS-13 → ...
    """

    def __init__(
        self,
        coach_acronym: str,
        receipt_chain: Optional[ReceiptChain] = None,
        registry_path: Optional[Path] = None,
    ):
        """Initialize the format constraint adapter.

        Args:
            coach_acronym: ADR-01 coach scope identifier (2-4 chars).
            receipt_chain: Optional ReceiptChain for audit logging.
            registry_path: Path to the format constraint registry JSON.
                           Defaults to config/visual_pipeline/format_constraint_registry.json.
        """
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(
                f"coach_acronym must be 2-4 characters, got {len(coach_acronym)}"
            )
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = receipt_chain or ReceiptChain(
            coach_acronym=self.coach_acronym[:3]
        )
        self.registry_path = registry_path or DEFAULT_REGISTRY_PATH
        self._registry: dict[str, FormatRegistryEntry] = {}
        self._load_registry()

    # ─────────────────────────────────────────────────
    # REGISTRY LOADING
    # FR-VIS-07 §7 Task 1
    # ─────────────────────────────────────────────────

    def _load_registry(self) -> None:
        """Load and validate the Format_Constraint_Registry from JSON.

        Per FR-VIS-07 §5: all entries must have non-null values for
        width_px, height_px, aspect_ratio, dpi, color_space, bleed_zone_px.
        """
        with open(self.registry_path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        formats_section = raw.get("formats", raw)
        # If the JSON has a top-level "formats" key, use it; otherwise treat
        # the entire dict as the formats mapping.

        for format_name, entry_data in formats_section.items():
            if format_name.startswith("_"):
                continue  # Skip metadata keys
            self._registry[format_name] = FormatRegistryEntry(**entry_data)

    def get_registry(self) -> dict[str, FormatRegistryEntry]:
        """Return the loaded format registry (for testing/inspection)."""
        return dict(self._registry)

    # ─────────────────────────────────────────────────
    # STAGE 1: Format Designation Extraction
    # FR-VIS-07 §4 Stage 1
    # ─────────────────────────────────────────────────

    def _stage1_extract_format(
        self, content_input: ContentOutputInput
    ) -> tuple[Optional[str], Optional[str], list[str]]:
        """Stage 1: Extract and validate the content_format designation.

        Per FR-VIS-07 §4 Stage 1:
        - Step 2: Extract content_format field.
        - Step 3: Validate against Format_Constraint_Registry.
        - Step 4: FORMAT_NOT_RECOGNIZED if not found; pipeline halts.

        Per FR-VIS-07 §6 Backward Compatibility:
        - If content_format is missing, attempt recipe_id cross-reference.

        Returns:
            Tuple of (validated content_format or None, error_type or None, warnings list).
        """
        warnings: list[str] = []
        content_format = content_input.content_format

        # FR-VIS-07 §4 Stage 1 Step 1-2: missing content_format
        if content_format is None or content_format.strip() == "":
            # FR-VIS-07 §6: Attempt legacy recipe_id cross-reference
            if content_input.recipe_id:
                derived_format = RECIPE_ID_TO_FORMAT.get(content_input.recipe_id)
                if derived_format and derived_format in self._registry:
                    warnings.append(
                        f"LEGACY_FORMAT_DERIVATION: content_format derived from "
                        f"recipe_id '{content_input.recipe_id}' → '{derived_format}'. "
                        f"Upstream pipeline should be updated to include content_format."
                    )
                    return derived_format, None, warnings
                else:
                    return None, FormatAdapterError.FORMAT_NOT_RECOGNIZED.value, warnings
            else:
                return None, FormatAdapterError.MISSING_CONTENT_FORMAT.value, warnings

        # FR-VIS-07 §4 Stage 1 Step 3-4: validate against registry
        if content_format not in self._registry:
            return None, FormatAdapterError.FORMAT_NOT_RECOGNIZED.value, warnings

        return content_format, None, warnings

    # ─────────────────────────────────────────────────
    # STAGE 2: Constraint Envelope Assembly
    # FR-VIS-07 §4 Stage 2
    # ─────────────────────────────────────────────────

    def _stage2_assemble_envelope(
        self,
        content_input: ContentOutputInput,
        content_format: str,
    ) -> tuple[Optional[FormatConstraintEnvelope], Optional[str]]:
        """Stage 2: Look up registry entry and assemble the sealed envelope.

        Per FR-VIS-07 §4 Stage 2:
        - Step 1: Look up format in registry.
        - Step 2: Validate required fields.
        - Step 3: Assemble envelope with per-slide dimensions.
        - Step 4-5: Generate SHA-256 seal hash.

        Returns:
            Tuple of (sealed envelope or None, error_type or None).
        """
        entry = self._registry.get(content_format)
        if entry is None:
            return None, FormatAdapterError.FORMAT_NOT_RECOGNIZED.value

        # FR-VIS-07 §4 Stage 2 Step 2: validate required fields
        required_fields = ["width_px", "height_px", "aspect_ratio", "dpi", "color_space"]
        for field_name in required_fields:
            if getattr(entry, field_name, None) is None:
                return None, FormatAdapterError.REGISTRY_INTEGRITY_ERROR.value

        # FR-VIS-07 §4 Stage 2 Step 3: build per-slide dimensions
        per_slide_dims = [
            PerSlideDimension(
                slide_index=i,
                width_px=entry.width_px,
                height_px=entry.height_px,
            )
            for i in range(content_input.slide_count)
        ]

        timestamp = datetime.now(timezone.utc).isoformat()

        envelope = FormatConstraintEnvelope(
            content_format=content_format,
            aspect_ratio=entry.aspect_ratio,
            total_slides=content_input.slide_count,
            width_px=entry.width_px,
            height_px=entry.height_px,
            dpi=entry.dpi,
            color_space=entry.color_space,
            bleed_zone_px=entry.bleed_zone_px,
            per_slide_dimensions=per_slide_dims,
            timestamp_utc=timestamp,
        )

        # FR-VIS-07 §4 Stage 2 Step 4: Generate SHA-256 seal hash
        seal_payload = envelope.model_dump_json(exclude={"seal_hash", "receipt_chain_block"})
        seal_hash = hashlib.sha256(seal_payload.encode("utf-8")).hexdigest()
        envelope.seal_hash = seal_hash

        return envelope, None

    # ─────────────────────────────────────────────────
    # SEAL HASH VERIFICATION
    # FR-VIS-07 §7 Task 7 — Dimension Override Detection
    # ─────────────────────────────────────────────────

    @staticmethod
    def verify_seal(envelope: FormatConstraintEnvelope) -> bool:
        """Verify the SHA-256 seal hash of an envelope.

        Per FR-VIS-07 §4 Stage 3 Step 4: if any downstream agent modifies
        dimensions, the hash mismatch is detected.

        Returns:
            True if the envelope has not been tampered with.
        """
        if envelope.seal_hash is None:
            return False
        expected_payload = envelope.model_dump_json(
            exclude={"seal_hash", "receipt_chain_block"}
        )
        expected_hash = hashlib.sha256(expected_payload.encode("utf-8")).hexdigest()
        return expected_hash == envelope.seal_hash

    # ─────────────────────────────────────────────────
    # RECEIPT CHAIN INTEGRATION
    # FR-VIS-07 §4 Receipt Writes
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
        """Write a receipt to the chain per FR47 DEP-ENG-041 schema.

        Returns:
            The receipt_id of the written receipt.
        """
        entry = self.receipt_chain.log(
            agent_id="visual_format_constraint_adapter",
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
    # PUBLIC API — Full Adapter Execution
    # FR-VIS-07 §4 Stages 1-3
    # ─────────────────────────────────────────────────

    def adapt(self, content_input: ContentOutputInput) -> FormatAdapterResult:
        """Execute the full 3-stage format constraint adapter pipeline.

        Per FR-VIS-07 §4:
        - Stage 1: Extract and validate format designation.
        - Stage 2: Assemble sealed format_constraint_envelope.
        - Stage 3: Downstream injection (envelope emission + receipt).

        Args:
            content_input: Upstream content output from DEP-ENG-011.

        Returns:
            FormatAdapterResult with either sealed envelope or error payload.
        """
        content_output_id = content_input.content_output_id

        # ── STAGE 1: Format Designation Extraction ──
        content_format, error_type, warnings = self._stage1_extract_format(
            content_input
        )

        # Receipt Write: Stage 1
        extraction_receipt_id = self._write_receipt(
            stage_name="VIS07_FORMAT_EXTRACTION",
            content_output_id=content_output_id,
            input_summary=(
                f"Content output {content_output_id}, "
                f"content_format={content_input.content_format!r}, "
                f"recipe_id={content_input.recipe_id!r}, "
                f"slide_count={content_input.slide_count}"
            ),
            output_summary=(
                f"Extracted format: {content_format!r}"
                if content_format
                else f"Extraction failed: {error_type}"
            ),
            decision="format_extracted" if content_format else "extraction_failed",
            decision_rationale=(
                f"Format '{content_format}' found in registry"
                if content_format
                else f"Error: {error_type}"
            ),
            metadata={
                "content_output_id": content_output_id,
                "input_content_format": content_input.content_format,
                "input_recipe_id": content_input.recipe_id,
                "resolved_format": content_format,
                "error_type": error_type,
                "warnings": warnings,
            },
        )

        # If extraction failed, return error result
        if error_type is not None:
            return FormatAdapterResult(
                success=False,
                envelope=None,
                error_type=error_type,
                error_detail=(
                    f"Format extraction failed for content_output_id "
                    f"'{content_output_id}': {error_type}. "
                    f"content_format={content_input.content_format!r}, "
                    f"recipe_id={content_input.recipe_id!r}"
                ),
                content_output_id=content_output_id,
                warnings=warnings,
                receipt_chain_block=extraction_receipt_id,
            )

        assert content_format is not None  # Type narrowing

        # ── STAGE 2: Constraint Envelope Assembly ──
        envelope, assembly_error = self._stage2_assemble_envelope(
            content_input, content_format
        )

        # Receipt Write: Stage 2
        assembly_receipt_id = self._write_receipt(
            stage_name="VIS07_ENVELOPE_ASSEMBLY",
            content_output_id=content_output_id,
            input_summary=(
                f"Format '{content_format}', slide_count={content_input.slide_count}"
            ),
            output_summary=(
                f"Envelope assembled: {envelope.envelope_id}, "
                f"{envelope.width_px}x{envelope.height_px}, "
                f"seal_hash={envelope.seal_hash[:16]}..."
                if envelope
                else f"Assembly failed: {assembly_error}"
            ),
            decision="envelope_assembled" if envelope else "assembly_failed",
            decision_rationale=(
                f"Registry entry found, {content_input.slide_count} slides at "
                f"{envelope.width_px}x{envelope.height_px}"
                if envelope
                else f"Error: {assembly_error}"
            ),
            parent_receipt_id=extraction_receipt_id,
            metadata={
                "content_format": content_format,
                "envelope_id": envelope.envelope_id if envelope else None,
                "seal_hash": envelope.seal_hash if envelope else None,
                "error_type": assembly_error,
            },
        )

        if assembly_error is not None:
            return FormatAdapterResult(
                success=False,
                envelope=None,
                error_type=assembly_error,
                error_detail=(
                    f"Envelope assembly failed for format '{content_format}': "
                    f"{assembly_error}"
                ),
                content_output_id=content_output_id,
                warnings=warnings,
                receipt_chain_block=assembly_receipt_id,
            )

        assert envelope is not None  # Type narrowing

        # ── STAGE 3: Downstream Injection ──
        # FR-VIS-07 §4 Stage 3: emit sealed envelope for downstream consumers
        envelope.receipt_chain_block = assembly_receipt_id

        # Receipt Write: Stage 3
        injection_receipt_id = self._write_receipt(
            stage_name="VIS07_DOWNSTREAM_INJECTION",
            content_output_id=content_output_id,
            input_summary=f"Sealed envelope {envelope.envelope_id}",
            output_summary=(
                f"Envelope injected downstream: "
                f"format={content_format}, "
                f"{envelope.width_px}x{envelope.height_px}, "
                f"aspect_ratio={envelope.aspect_ratio}"
            ),
            decision="envelope_injected",
            decision_rationale=(
                f"Sealed envelope delivered for {content_format} at "
                f"{envelope.width_px}x{envelope.height_px} "
                f"({envelope.aspect_ratio})"
            ),
            parent_receipt_id=assembly_receipt_id,
            metadata={
                "envelope_id": envelope.envelope_id,
                "content_format": content_format,
                "width_px": envelope.width_px,
                "height_px": envelope.height_px,
                "aspect_ratio": envelope.aspect_ratio,
                "bleed_zone_px": envelope.bleed_zone_px,
                "seal_hash": envelope.seal_hash,
                "slide_count": envelope.total_slides,
            },
        )

        return FormatAdapterResult(
            success=True,
            envelope=envelope,
            content_output_id=content_output_id,
            warnings=warnings,
            receipt_chain_block=injection_receipt_id,
        )

    # ─────────────────────────────────────────────────
    # DIMENSION OVERRIDE DETECTION
    # FR-VIS-07 §7 Task 7
    # ─────────────────────────────────────────────────

    def check_dimension_override(
        self,
        sealed_envelope: FormatConstraintEnvelope,
        downstream_width: int,
        downstream_height: int,
        downstream_agent: str = "unknown",
    ) -> Optional[str]:
        """Check if a downstream agent has overridden sealed dimensions.

        Per FR-VIS-07 §8 AC5: if any agent writes dimensions differing
        from the sealed envelope, trigger DIMENSION_OVERRIDE_VIOLATION.

        Args:
            sealed_envelope: The sealed envelope from VIS-07.
            downstream_width: Width claimed by the downstream agent.
            downstream_height: Height claimed by the downstream agent.
            downstream_agent: Name of the downstream agent (for error message).

        Returns:
            None if dimensions match; violation string if mismatch detected.
        """
        if (
            sealed_envelope.width_px != downstream_width
            or sealed_envelope.height_px != downstream_height
        ):
            violation = (
                f"DIMENSION_OVERRIDE_VIOLATION: Agent '{downstream_agent}' "
                f"attempted to use {downstream_width}x{downstream_height} "
                f"but sealed envelope specifies "
                f"{sealed_envelope.width_px}x{sealed_envelope.height_px} "
                f"({sealed_envelope.aspect_ratio}). "
                f"Sealed hash: {sealed_envelope.seal_hash}"
            )

            # Write violation receipt
            self._write_receipt(
                stage_name="VIS07_DIMENSION_OVERRIDE_VIOLATION",
                content_output_id=sealed_envelope.envelope_id,
                input_summary=(
                    f"Downstream check: {downstream_agent} claims "
                    f"{downstream_width}x{downstream_height}"
                ),
                output_summary=violation,
                decision=FormatAdapterError.DIMENSION_OVERRIDE_VIOLATION.value,
                decision_rationale=(
                    f"Sealed dimensions are "
                    f"{sealed_envelope.width_px}x{sealed_envelope.height_px} "
                    f"but downstream agent used "
                    f"{downstream_width}x{downstream_height}"
                ),
            )

            return violation

        return None
