"""
FR-VIS-03 — PSSL Prompt Compilation (Paradoxe)
===============================================
Translates VCB PSSL parameters into complete RunningHub task payloads.

Pipeline stages:
  Stage 1 — PSSL Field-to-Prompt Translation
  Stage 2 — Anti-Generic Constraint Assembly
  Stage 3 — Reference Image & Imperfection Specification
  Stage 4 — RunningHub Task Payload Assembly & Submission
"""

from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.visual_engine_models import (
    AntiGenericConstraints,
    CompiledPromptPayload,
    DEFAULT_IMPERFECTION_SPEC,
    ENEMY_ANTI_PATTERNS,
    GazeCompilation,
    GrammarSystem,
    PADVector,
    PSSLBlock,
    PSSLCompilationError,
    PerSlideAssignment,
    PollingStatus,
    REFERENCE_IMAGE_STRENGTH_DEFAULT,
    REFERENCE_IMAGE_STRENGTH_HIGH,
    RUNNINGHUB_INITIAL_BACKOFF_S,
    RUNNINGHUB_MAX_BACKOFF_S,
    RUNNINGHUB_TIMEOUT_TOTAL_S,
    ReferenceImageConfig,
    RunningHubPayload,
    SATURATION_RANGES,
    SaturationTranslation,
    UNIVERSAL_ANTI_GENERIC,
    VisualCompositionBrief,
)

# ────────────────────────────────────────────────────────────────────────
# C-11 persona masking
# ────────────────────────────────────────────────────────────────────────
_AGENT_ID = "paradoxe_pssl_compiler"


class ParadoxePSSLCompiler:
    """
    Paradoxe — deterministic PSSL-to-prompt translator.

    Parameters
    ----------
    coach_acronym : str
        2-4 character coach identifier (ADR-01).
    receipt_chain : ReceiptChain
        Shared receipt chain for audit logging.
    """

    # ------------------------------------------------------------------ #
    # Construction
    # ------------------------------------------------------------------ #

    def __init__(
        self,
        coach_acronym: str,
        receipt_chain: ReceiptChain,
    ) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(
                f"coach_acronym must be 2-4 characters, got '{coach_acronym}'"
            )
        self._coach = coach_acronym
        self._rc = receipt_chain

    # ================================================================== #
    # PUBLIC API
    # ================================================================== #

    def compile_vcb(
        self,
        vcb: VisualCompositionBrief,
        *,
        enemy_typology: str | None = None,
        grammar_system: str = GrammarSystem.CINEMATIC,
        character_reference_ids: dict[int, str] | None = None,
        lora_paths: dict[int, str] | None = None,
    ) -> list[CompiledPromptPayload]:
        """
        Compile all slides of a VCB into RunningHub payloads.

        Returns one ``CompiledPromptPayload`` per slide.
        """
        character_reference_ids = character_reference_ids or {}
        lora_paths = lora_paths or {}
        payloads: list[CompiledPromptPayload] = []

        for slide in vcb.per_slide_assignments:
            payload = self._compile_slide(
                slide=slide,
                vcb=vcb,
                enemy_typology=enemy_typology,
                grammar_system=grammar_system,
                char_ref_id=character_reference_ids.get(slide.slide_index),
                lora_path=lora_paths.get(slide.slide_index),
            )
            payloads.append(payload)

        self._rc.log(
            agent_id=_AGENT_ID,
            action="compile_vcb",
            asset_id=vcb.vcb_id,
            output_summary=f"slides={len(payloads)}",
        )

        return payloads

    # ================================================================== #
    # STAGE 1 — PSSL FIELD-TO-PROMPT TRANSLATION
    # ================================================================== #

    @staticmethod
    def translate_lighting(lighting_grammar: str) -> str:
        """Deterministic prose translation of the lighting_grammar field."""
        parts: list[str] = []
        # Extract lighting type
        base = lighting_grammar.split(",")[0].strip()
        parts.append(f"{base} lighting")

        # Extract temporal_signal
        ts_match = re.search(r"temporal_signal:\s*(.+?)(?:,|$)", lighting_grammar)
        if ts_match:
            ts = ts_match.group(1).strip()
            parts.append(f"color temperature {ts}")

        # Extract shadow spec
        shadow_match = re.search(r"shadow:\s*(.+?)(?:,|$)", lighting_grammar)
        if shadow_match:
            parts.append(f"shadow at {shadow_match.group(1).strip()}")

        # Extract fill ratio
        fill_match = re.search(r"fill ratio\s*(.+?)(?:,|$)", lighting_grammar)
        if fill_match:
            parts.append(f"key-to-fill ratio {fill_match.group(1).strip()}")

        return ", ".join(parts)

    @staticmethod
    def translate_saturation(saturation_pct: int) -> SaturationTranslation:
        """Map numeric saturation to descriptive text."""
        descriptor = "moderate, naturalistic saturation"
        for lo, hi, desc in SATURATION_RANGES:
            if lo <= saturation_pct <= hi:
                descriptor = desc
                break
        full = (
            f"{descriptor.capitalize()} at approximately "
            f"{saturation_pct}% saturation"
        )
        return SaturationTranslation(
            saturation_pct=saturation_pct,
            descriptor=descriptor,
            full_text=full,
        )

    @staticmethod
    def translate_gaze(
        head_rotation_degrees: float,
        pupil_position_ratio_pct: float,
    ) -> GazeCompilation:
        """Compile dual-vector gaze geometry into character pose directives."""
        if head_rotation_degrees < 0:
            head_dir = "left"
            abs_rot = abs(head_rotation_degrees)
        elif head_rotation_degrees > 0:
            head_dir = "right"
            abs_rot = head_rotation_degrees
        else:
            head_dir = "center"
            abs_rot = 0.0

        if head_dir == "center":
            head_text = "Subject facing directly forward"
        else:
            head_text = (
                f"Subject's head turned {abs_rot:.0f} degrees "
                f"to the viewer's {head_dir} of center"
            )

        if pupil_position_ratio_pct < 40:
            pupil_dir = "leftward"
        elif pupil_position_ratio_pct > 60:
            pupil_dir = "rightward"
        else:
            pupil_dir = "forward"

        pupil_text = (
            f"Eyes directed {pupil_dir} with pupils at approximately "
            f"{pupil_position_ratio_pct:.0f}% width from inner corner"
        )

        compiled = f"{head_text}, {pupil_text}"

        return GazeCompilation(
            head_rotation_degrees=head_rotation_degrees,
            head_direction_text=head_dir,
            pupil_position_ratio_pct=pupil_position_ratio_pct,
            pupil_direction_text=pupil_dir,
            compiled_text=compiled,
        )

    @staticmethod
    def translate_pad(pad: PADVector) -> str:
        """Translate PAD vector to environmental descriptor."""
        descriptors: list[str] = []

        # Pleasure axis
        if pad.P >= 0.5:
            descriptors.append("warm, inviting")
        elif pad.P <= -0.5:
            descriptors.append("cold, unwelcoming")
        else:
            descriptors.append("neutral atmosphere")

        # Arousal axis
        if pad.A >= 0.7:
            descriptors.append("tense anticipation")
        elif pad.A >= 0.4:
            descriptors.append("engaged alertness")
        elif pad.A <= -0.3:
            descriptors.append("calm stillness")
        else:
            descriptors.append("moderate energy")

        # Dominance axis
        if pad.D >= 0.6:
            descriptors.append("expansive, commanding space")
        elif pad.D <= -0.3:
            descriptors.append("confined, constrained space")
        else:
            descriptors.append("balanced spatial presence")

        return f"Environment expressing {' — '.join(descriptors)}"

    @staticmethod
    def translate_chromatic_bloom(sequence: list[str]) -> str:
        """Translate chromatic bloom array into gradient directives."""
        parts: list[str] = []
        for entry in sequence:
            # Pattern: "#HEX→#HEX ease Ns"
            parts.append(f"Color transition: {entry}")
        return ". ".join(parts)

    @staticmethod
    def translate_artifact(artifact: str | None) -> str:
        """Translate incomplete_tribal_artifact to visual directive."""
        if not artifact:
            return ""
        return (
            f"Include a visible {artifact} in the scene — incomplete, "
            f"suggesting a process in progress, not a finished endpoint"
        )

    def compile_pssl_text(self, pssl: PSSLBlock) -> str:
        """Assemble the full compiled prompt text from a PSSL block."""
        sections: list[str] = []

        sections.append(self.translate_lighting(pssl.lighting_grammar))
        sections.append(
            self.translate_saturation(pssl.saturation_pct).full_text
        )
        gaze = self.translate_gaze(
            pssl.head_rotation_degrees,
            pssl.pupil_position_ratio_pct,
        )
        sections.append(gaze.compiled_text)
        sections.append(
            self.translate_pad(pssl.pad_environmental_grammar)
        )
        sections.append(
            self.translate_chromatic_bloom(pssl.chromatic_bloom_sequence)
        )
        artifact = self.translate_artifact(pssl.incomplete_tribal_artifact)
        if artifact:
            sections.append(artifact)

        return ". ".join(sections)

    # ================================================================== #
    # STAGE 2 — ANTI-GENERIC CONSTRAINT ASSEMBLY
    # ================================================================== #

    @staticmethod
    def assemble_anti_generic(
        enemy_typology: str | None = None,
    ) -> AntiGenericConstraints:
        """Build the negative-prompt constraints block."""
        enemy_pattern = None
        if enemy_typology:
            lower = enemy_typology.lower().strip()
            enemy_pattern = ENEMY_ANTI_PATTERNS.get(lower)

        parts: list[str] = []
        if enemy_pattern:
            parts.append(enemy_pattern)
        parts.append(UNIVERSAL_ANTI_GENERIC)

        compiled = " ".join(parts)

        return AntiGenericConstraints(
            enemy_typology=enemy_typology,
            enemy_anti_pattern=enemy_pattern,
            universal_constraints=UNIVERSAL_ANTI_GENERIC,
            compiled_text=compiled,
        )

    # ================================================================== #
    # STAGE 3 — REFERENCE IMAGE & IMPERFECTION
    # ================================================================== #

    @staticmethod
    def build_reference_config(
        image_type: str,
        char_ref_id: str | None = None,
        lora_path: str | None = None,
        strength: float = REFERENCE_IMAGE_STRENGTH_DEFAULT,
    ) -> ReferenceImageConfig:
        """Assemble reference image configuration."""
        is_ghibli = "ghibli" in image_type.lower() or "tier_4" in image_type.lower()

        if is_ghibli:
            return ReferenceImageConfig(
                has_reference=False,
                lora_model_path=lora_path,
                is_ghibli=True,
                strength=strength,
            )

        if char_ref_id:
            return ReferenceImageConfig(
                has_reference=True,
                reference_source="DEP-VIS-004",
                character_id=char_ref_id,
                strength=strength,
            )

        return ReferenceImageConfig(has_reference=False, strength=strength)

    # ================================================================== #
    # STAGE 4 — RUNNINGHUB PAYLOAD ASSEMBLY
    # ================================================================== #

    @staticmethod
    def assemble_runninghub_payload(
        prompt_text: str,
        anti_generic_text: str,
        reference_config: ReferenceImageConfig,
        imperfection_text: str = DEFAULT_IMPERFECTION_SPEC,
    ) -> RunningHubPayload:
        """Build the RunningHub task payload."""
        if reference_config.is_ghibli:
            workflow_id = "WF-GHIBLI-V1-001"
        else:
            workflow_id = "WF-REALISTIC-V3-001"

        return RunningHubPayload(
            workflow_id=workflow_id,
            prompt_text=prompt_text,
            anti_generic_text=anti_generic_text,
            imperfection_text=imperfection_text,
            reference_image_config=reference_config,
        )

    @staticmethod
    def compute_next_backoff(current: int) -> int:
        """Compute the next exponential backoff interval."""
        return min(current * 2, RUNNINGHUB_MAX_BACKOFF_S)

    @staticmethod
    def backoff_sequence() -> list[int]:
        """Return the full polling backoff schedule."""
        seq: list[int] = []
        current = RUNNINGHUB_INITIAL_BACKOFF_S
        elapsed = 0
        while elapsed < RUNNINGHUB_TIMEOUT_TOTAL_S:
            seq.append(current)
            elapsed += current
            current = min(current * 2, RUNNINGHUB_MAX_BACKOFF_S)
        return seq

    # ================================================================== #
    # INTERNAL — per-slide compilation
    # ================================================================== #

    def _compile_slide(
        self,
        slide: PerSlideAssignment,
        vcb: VisualCompositionBrief,
        enemy_typology: str | None,
        grammar_system: str,
        char_ref_id: str | None,
        lora_path: str | None,
    ) -> CompiledPromptPayload:
        """Compile a single slide through all 4 stages."""
        warnings: list[str] = []

        # Stage 1 — Translation
        prompt_text = self.compile_pssl_text(slide.pssl)

        # Stage 2 — Anti-generic
        anti_gen = self.assemble_anti_generic(enemy_typology)

        # Stage 3 — Reference + Imperfection
        ref_config = self.build_reference_config(
            image_type=slide.image_type,
            char_ref_id=char_ref_id,
            lora_path=lora_path,
        )

        # Stage 4 — Payload assembly
        rh_payload = self.assemble_runninghub_payload(
            prompt_text=prompt_text,
            anti_generic_text=anti_gen.compiled_text,
            reference_config=ref_config,
        )

        comp_id = (
            f"CPL-{self._coach}-"
            f"{datetime.now(timezone.utc).strftime('%Y%m%d')}-"
            f"{uuid.uuid4().hex[:6]}-S{slide.slide_index:02d}"
        )

        self._rc.log(
            agent_id=_AGENT_ID,
            action="compile_slide",
            asset_id=vcb.vcb_id,
            output_summary=f"slide={slide.slide_index}, wf={rh_payload.workflow_id}",
        )

        return CompiledPromptPayload(
            compilation_id=comp_id,
            vcb_id=vcb.vcb_id,
            slide_index=slide.slide_index,
            coach_acronym=vcb.coach_acronym,
            grammar_system=grammar_system,
            compiled_prompt_text=prompt_text,
            anti_generic_constraints=anti_gen,
            imperfection_spec=DEFAULT_IMPERFECTION_SPEC,
            reference_image=ref_config,
            runninghub_payload=rh_payload,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            warnings=warnings,
        )

    # ================================================================== #
    # TRANSLATION DETERMINISM VERIFICATION
    # ================================================================== #

    def compile_pssl_text_deterministic(self, pssl: PSSLBlock, n: int = 5) -> bool:
        """
        Compile the same PSSL block *n* times and verify identical output.
        Returns True if all compilations match character-for-character.
        """
        results = [self.compile_pssl_text(pssl) for _ in range(n)]
        return all(r == results[0] for r in results)
