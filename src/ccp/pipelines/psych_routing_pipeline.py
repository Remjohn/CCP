"""
CCP FR18 Psychological Routing Brief Generator — Pipeline Orchestrator (Unit 4)
3-stage pipeline: INGEST → VARIABLE MATRIX → EMIT (DEP-ENG-016 output).

Spec reference: FR18_Psychological_Routing_Brief_Tech_Spec.md §4 Implementation Plan
                §6 Backward Compatibility Fallback
                §7 Tasks

Receipt writes at each of the 3 stages per FR47 DEP-ENG-041 schema:
  Stage 1: STAGE-1-ROUTING-INGEST      / Psych-Routing-Engine
  Stage 2: STAGE-2-VARIABLE-MATRIX     / Psych-Routing-Engine
  Stage 3: STAGE-3-ROUTING-EMIT        / Psych-Routing-Engine

ADR-01 strict isolation: coach_id scoped on all reads and receipt writes (AC4).
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.psych_routing_models import (
    AudienceMaturityProfile,
    MoodContextMap,
    NEUTRAL_PROCESSING_PROXY_MATURITY,
    NEUTRAL_PROCESSING_PROXY_STATE,
    OPERATOR_WARNING_FALLBACK,
    PsychRoutingBrief,
    PsychologicalClassification,
)
from src.ccp.services.payload_masking_library import get_payload_masking_instruction
from src.ccp.services.psych_routing_engine import PsychVariableMatrix


AGENT_NAME = "Psych-Routing-Engine"

# Receipt stage names — verbatim from spec §4
STAGE_INGEST = "STAGE-1-ROUTING-INGEST"
STAGE_MATRIX = "STAGE-2-VARIABLE-MATRIX"
STAGE_EMIT = "STAGE-3-ROUTING-EMIT"


class PsychRoutingBriefGenerator:
    """FR18 — Psychological Routing Brief Generator.

    Executes the 3-stage pipeline producing DEP-ENG-016 (PsychRoutingBrief).
    Injected into Block B (field_3_context) of the JIT compilation template.

    Spec §4:
      Stage 1: Ingest DEP-ENG-018 + DEP-ENG-017 → write STAGE-1-ROUTING-INGEST receipt
      Stage 2: Resolve 8-variable matrix → write STAGE-2-VARIABLE-MATRIX receipt
      Stage 3: Construct + emit DEP-ENG-016 → write STAGE-3-ROUTING-EMIT receipt

    Spec §6 Fallback:
      If DEP-ENG-018 unavailable → use NEUTRAL_PROCESSING_PROXY_STATE.
      Set is_fallback=True, raise OPERATOR_WARNING.
      Compilation continues normally.

    AC4: All inputs and receipts are scoped to the coach's private storage container.
    """

    def __init__(
        self,
        coach_id: str,
        receipt_chain: ReceiptChain,
        *,
        output_dir: Optional[Path] = None,
    ):
        """Initialize the generator.

        Args:
            coach_id: Coach identifier — enforces ADR-01 single-tenant isolation (AC4).
            receipt_chain: ReceiptChain instance scoped to this coach.
            output_dir: Optional directory to write psych_routing_brief.json.
        """
        self._coach_id = coach_id
        self._receipt_chain = receipt_chain
        self._output_dir = output_dir
        self._matrix = PsychVariableMatrix()

    def generate(
        self,
        mood_context: Optional[MoodContextMap] = None,
        maturity_profile: Optional[AudienceMaturityProfile] = None,
        batch_slot_id: Optional[str] = None,
    ) -> PsychRoutingBrief:
        """Execute the full 3-stage routing brief generation pipeline.

        Args:
            mood_context: DEP-ENG-018 input. If None, fallback is triggered.
            maturity_profile: DEP-ENG-017 input. If None, NEW cohort default used.
            batch_slot_id: Batch slot identifier for receipt chaining.

        Returns:
            PsychRoutingBrief (DEP-ENG-016) — fully resolved, receipt-signed.
        """
        # ── Stage 1: Ingest ───────────────────────────────────────────────────
        effective_mood, effective_maturity, is_fallback = self._stage_ingest(
            mood_context=mood_context,
            maturity_profile=maturity_profile,
            batch_slot_id=batch_slot_id,
        )

        # ── Stage 2: Variable Resolution Matrix ───────────────────────────────
        classification = self._stage_matrix(
            mood_context=effective_mood,
            maturity_profile=effective_maturity,
            batch_slot_id=batch_slot_id,
        )

        # ── Stage 3: Payload Construction & Emit ─────────────────────────────
        brief = self._stage_emit(
            classification=classification,
            is_fallback=is_fallback,
            batch_slot_id=batch_slot_id,
        )

        # Optionally write to file
        if self._output_dir is not None:
            self._write_brief(brief)

        return brief

    # ─── Stage Implementations ────────────────────────────────────────────────

    def _stage_ingest(
        self,
        mood_context: Optional[MoodContextMap],
        maturity_profile: Optional[AudienceMaturityProfile],
        batch_slot_id: Optional[str],
    ) -> tuple[MoodContextMap, AudienceMaturityProfile, bool]:
        """Stage 1: State Ingestion.

        Spec §4 Stage 1 failure condition: inputs missing essential metrics.
        If DEP-ENG-018 is missing → fall back to Neutral Processing Proxy State.
        """
        is_fallback = mood_context is None

        # ADR-01: Validate coach_id isolation if provided
        if mood_context is not None and mood_context.coach_id is not None:
            if mood_context.coach_id != self._coach_id:
                raise ValueError(
                    f"ADR-01 isolation violation: MoodContextMap.coach_id='{mood_context.coach_id}' "
                    f"does not match pipeline coach_id='{self._coach_id}'. "
                    "Cross-tenant data read blocked."
                )

        if maturity_profile is not None and maturity_profile.coach_id != self._coach_id:
            raise ValueError(
                f"ADR-01 isolation violation: AudienceMaturityProfile.coach_id='{maturity_profile.coach_id}' "
                f"does not match pipeline coach_id='{self._coach_id}'. "
                "Cross-tenant data read blocked."
            )

        effective_mood = mood_context if not is_fallback else NEUTRAL_PROCESSING_PROXY_STATE
        effective_maturity = maturity_profile if maturity_profile is not None else NEUTRAL_PROCESSING_PROXY_MATURITY

        input_summary = (
            f"mood_state_primary={effective_mood.mood_state_primary.value}, "
            f"arousal={effective_mood.audience_arousal_level.value}, "
            f"maturity_cohort={effective_maturity.maturity_cohort.value}, "
            f"fallback={is_fallback}"
        )
        if batch_slot_id:
            input_summary += f", batch_slot_id={batch_slot_id}"

        self._receipt_chain.log(
            agent_id=AGENT_NAME,
            action=STAGE_INGEST,
            asset_id=batch_slot_id,
            input_summary=input_summary,
            output_summary=(
                f"Inputs resolved — fallback={'YES' if is_fallback else 'NO'}. "
                f"Effective mood state: {effective_mood.mood_state_primary.value}."
            ),
            decision="ingested",
            decision_rationale=(
                "DEP-ENG-018 unavailable — using Neutral Processing Proxy State."
                if is_fallback
                else "DEP-ENG-018 available — using live psychometric feed."
            ),
            metadata={
                "coach_id": self._coach_id,
                "is_fallback": is_fallback,
                "mood_state": effective_mood.mood_state_primary.value,
                "maturity_cohort": effective_maturity.maturity_cohort.value,
            },
        )

        return effective_mood, effective_maturity, is_fallback

    def _stage_matrix(
        self,
        mood_context: MoodContextMap,
        maturity_profile: AudienceMaturityProfile,
        batch_slot_id: Optional[str],
    ) -> PsychologicalClassification:
        """Stage 2: Variable Resolution Matrix.

        Spec §4 Stage 2 failure condition: null exception on matrix lookup.
        All 8 variables resolved deterministically.
        """
        classification = self._matrix.resolve(mood_context, maturity_profile)

        input_payload = json.dumps({
            "mood_state": mood_context.mood_state_primary.value,
            "arousal": mood_context.audience_arousal_level.value,
            "regulatory": mood_context.regulatory_orientation.value,
            "cohort": maturity_profile.maturity_cohort.value,
        }, sort_keys=True)
        input_hash = hashlib.sha256(input_payload.encode()).hexdigest()[:16]

        output_payload = json.dumps({
            "arousal_direction": classification.arousal_direction.value,
            "valence_delivery": classification.valence_delivery.value,
            "regulatory_frame": classification.regulatory_frame.value,
            "sdt_need_primary": classification.sdt_need_primary.value,
            "sequencing_dependency": classification.sequencing_dependency.value,
            "comparison_type": classification.comparison_type.value,
            "tmt_function": classification.tmt_function.value,
        }, sort_keys=True)
        output_hash = hashlib.sha256(output_payload.encode()).hexdigest()[:16]

        self._receipt_chain.log(
            agent_id=AGENT_NAME,
            action=STAGE_MATRIX,
            asset_id=batch_slot_id,
            input_summary=input_payload,
            output_summary=(
                f"8 variables resolved: "
                f"arousal={classification.arousal_direction.value}, "
                f"valence={classification.valence_delivery.value}, "
                f"frame={classification.regulatory_frame.value}, "
                f"sdt={classification.sdt_need_primary.value}, "
                f"seq={classification.sequencing_dependency.value}, "
                f"comp={classification.comparison_type.value}, "
                f"tmt={classification.tmt_function.value}"
            ),
            decision="resolved",
            metadata={
                "coach_id": self._coach_id,
                "input_payload_hash": input_hash,
                "output_payload_hash": output_hash,
                "arousal_direction": classification.arousal_direction.value,
                "valence_delivery": classification.valence_delivery.value,
                "regulatory_frame": classification.regulatory_frame.value,
                "sdt_need_primary": classification.sdt_need_primary.value,
                "tmt_function": classification.tmt_function.value,
                "comparison_type": classification.comparison_type.value,
            },
        )

        return classification

    def _stage_emit(
        self,
        classification: PsychologicalClassification,
        is_fallback: bool,
        batch_slot_id: Optional[str],
    ) -> PsychRoutingBrief:
        """Stage 3: Payload Construction & Emit.

        Spec §4 Stage 3:
        1. Fetch payload_masking_instruction string based on mood_state_primary.
        2. Construct DEP-ENG-016 JSON schema.
        3. Write receipt.
        4. Pass payload to Block B of the compilation template.

        Spec §4 Stage 3 failure condition:
          Brief object fails schema typing validation.
        """
        mood_state = classification.mood_state_primary
        masking_instruction = get_payload_masking_instruction(mood_state)

        # Generate routing_id
        ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        id_seed = f"PRB-{ts}-{self._coach_id[-4:] if len(self._coach_id) >= 4 else self._coach_id}"
        routing_id = id_seed

        operator_warning = OPERATOR_WARNING_FALLBACK if is_fallback else None

        brief = PsychRoutingBrief(
            routing_id=routing_id,
            receipt_chain_hash="",  # Updated after receipt is written below
            coach_id=self._coach_id,
            psychological_classification=classification,
            payload_masking_instruction=masking_instruction,
            is_fallback=is_fallback,
            operator_warning=operator_warning,
        )

        # Write Stage 3 receipt
        brief_json = brief.model_dump_json()
        output_hash = hashlib.sha256(brief_json.encode()).hexdigest()[:16]

        receipt = self._receipt_chain.log(
            agent_id=AGENT_NAME,
            action=STAGE_EMIT,
            asset_id=routing_id,
            input_summary=f"classification resolved for mood_state={mood_state.value}",
            output_summary=(
                f"DEP-ENG-016 emitted: routing_id={routing_id}, "
                f"mood={mood_state.value}, "
                f"masking_instruction_length={len(masking_instruction)}, "
                f"is_fallback={is_fallback}"
            ),
            decision="emitted",
            decision_rationale=operator_warning,
            metadata={
                "coach_id": self._coach_id,
                "routing_id": routing_id,
                "output_payload_hash": output_hash,
                "mood_state_primary": mood_state.value,
                "is_fallback": is_fallback,
            },
        )

        # Stamp the receipt hash onto the brief
        brief = brief.model_copy(update={"receipt_chain_hash": receipt.receipt_id})

        return brief

    # ─── File I/O ─────────────────────────────────────────────────────────────

    def _write_brief(self, brief: PsychRoutingBrief) -> Path:
        """Write psych_routing_brief.json to the output directory."""
        assert self._output_dir is not None
        self._output_dir.mkdir(parents=True, exist_ok=True)
        output_path = self._output_dir / "psych_routing_brief.json"
        output_path.write_text(
            brief.model_dump_json(indent=2),
            encoding="utf-8",
        )
        return output_path
