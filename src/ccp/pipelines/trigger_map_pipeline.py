"""
CCP FR5 Trigger Map Builder — Pipeline Orchestrator (Unit 10)
9-phase orchestrator with receipt chain + coach_soul update.

Spec reference: FR5 Tech Spec §Phases 1-9

Pipeline phases:
  Phase 1: INGEST — Load emotional_dna.json, validate confidence ≥ 0.5,
           load coach_soul.json + transcripts. Write TMAP-INGEST receipt.
  Phase 2: Trigger Identification — 6 LIWC-22 markers + V6-V10 MFT mapping
  Phase 3: Origin Classification — Conway AKB hierarchy (ESK/GE/LP)
  Phase 4: PTG Assessment — Tedeschi & Calhoun (resolved/active/raw_unresolved)
           HARD EXCLUDE raw_unresolved at code level (AC2)
  Phase 5: Narrative Identity — McAdams (redemption/contamination/mixed + positioning)
  Phase 6: Reconsolidation Sensitivity — Nader (1-10, V1 cross-validated) (AC7)
  Phase 7: Archetype Mapping — emotional state → archetypes, TTT eligibility
  Phase 8: EMIT — Build DEP-LIB-002 trigger_map.json
  Phase 9: VALIDATE & CHECKPOINT — 9 checks, receipt write TMAP-COMPLETE,
           update coach_soul.json

Receipt chain writes:
  - TMAP-INGEST at Phase 1
  - TMAP-COMPLETE at Phase 9

Mandate 7 enforcement: corpus citation for every classification.
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.emotional_dna_models import (
    EmotionalDNAProfile,
)
from src.ccp.models.trigger_map_models import (
    EMOTIONAL_DNA_MINIMUM_CONFIDENCE,
    MINIMUM_RESOLVED_TRIGGERS,
    VALIDATION_CHECK_COUNT,
    TriggerMap,
    TriggerMapPipelineSession,
    TriggerMapPipelineStepStatus,
    TriggerMapValidationCheck,
    TriggerMapValidationResult,
)
from src.ccp.services.akb_origin_classifier import AKBOriginClassifier
from src.ccp.services.narrative_identity_classifier import NarrativeIdentityClassifier
from src.ccp.services.ptg_assessor import PTGAssessor
from src.ccp.services.reconsolidation_scorer import ReconsolidationScorer
from src.ccp.services.trigger_archetype_mapper import TriggerArchetypeMapper
from src.ccp.services.trigger_identifier import TriggerIdentifier


class TriggerMapPipelineError(Exception):
    """Top-level pipeline error for FR5."""
    pass


class TriggerMapPipeline:
    """Orchestrates the complete FR5 Trigger Map Builder pipeline.

    This is the main entry point for FR5 execution. It runs all 9 phases
    in sequence, enforces quality gates, writes receipt chain entries,
    and updates coach_soul.json on completion.

    Prerequisite gate: emotional_dna.json must exist with confidence ≥ 0.5.
    Safety gate: raw_unresolved PTG triggers are HARD EXCLUDED (AC2).
    Minimum viable map: ≥2 resolved_dual_layer triggers (AC4).
    """

    def __init__(
        self,
        coach_id: str,
        coach_acronym: str,
        coach_dir: Path,
        receipt_chain: Optional[ReceiptChain] = None,
    ):
        self.coach_id = coach_id
        self.coach_acronym = coach_acronym.upper()
        self.coach_dir = Path(coach_dir)
        self.receipt_chain = receipt_chain or ReceiptChain(
            coach_acronym=self.coach_acronym
        )

        # Initialize all service units
        self.trigger_identifier = TriggerIdentifier()
        self.akb_classifier = AKBOriginClassifier()
        self.ptg_assessor = PTGAssessor()
        self.narrative_classifier = NarrativeIdentityClassifier()
        self.reconsolidation_scorer = ReconsolidationScorer()
        self.archetype_mapper = TriggerArchetypeMapper()

    def execute(
        self,
        corpus_text: str,
        emotional_dna: EmotionalDNAProfile,
        ttt_baseline: Optional[dict[str, object]] = None,
        parent_receipt_id: Optional[str] = None,
    ) -> TriggerMapPipelineSession:
        """Execute the complete FR5 pipeline.

        Args:
            corpus_text: Full concatenated corpus text.
            emotional_dna: DEP-LIB-001 profile (from FR4).
            ttt_baseline: Coach's TTT baseline dict (from FR3).
            parent_receipt_id: Receipt ID from FR4's final stage (chain link).

        Returns:
            TriggerMapPipelineSession with all phase outputs and receipt IDs.

        Raises:
            TriggerMapPipelineError: On unrecoverable pipeline failure.
        """
        session = TriggerMapPipelineSession(
            session_id=f"TMAP-{self.coach_acronym}-{uuid.uuid4().hex[:8]}",
            coach_id=self.coach_id,
            coach_acronym=self.coach_acronym,
        )

        last_receipt_id = parent_receipt_id

        try:
            # ── Phase 1: INGEST ──
            last_receipt_id = self._execute_phase_1(
                session, emotional_dna, last_receipt_id
            )

            # ── Phase 2: Trigger Identification ──
            last_receipt_id = self._execute_phase_2(
                session, corpus_text, emotional_dna, last_receipt_id
            )

            # ── Phase 3: Origin Classification ──
            last_receipt_id = self._execute_phase_3(
                session, corpus_text, last_receipt_id
            )

            # ── Phase 4: PTG Assessment (HARD EXCLUDE gate) ──
            last_receipt_id = self._execute_phase_4(
                session, corpus_text, last_receipt_id
            )

            # ── Phase 5: Narrative Identity ──
            last_receipt_id = self._execute_phase_5(
                session, corpus_text, last_receipt_id
            )

            # ── Phase 6: Reconsolidation Sensitivity ──
            last_receipt_id = self._execute_phase_6(
                session, emotional_dna, corpus_text, last_receipt_id
            )

            # ── Phase 7: Archetype Mapping ──
            last_receipt_id = self._execute_phase_7(
                session, ttt_baseline, last_receipt_id
            )

            # ── Phase 8: EMIT ──
            last_receipt_id = self._execute_phase_8(
                session, last_receipt_id
            )

            # ── Phase 9: VALIDATE & CHECKPOINT ──
            last_receipt_id = self._execute_phase_9(
                session, last_receipt_id
            )

        except TriggerMapPipelineError:
            raise
        except Exception as e:
            session.step_statuses["pipeline"] = (
                TriggerMapPipelineStepStatus.FAILED
            )
            raise TriggerMapPipelineError(
                f"FR5 pipeline failed: {e}"
            ) from e

        return session

    # ──────────────────────────────────────────────────────────
    # Phase 1: INGEST
    # ──────────────────────────────────────────────────────────

    def _execute_phase_1(
        self,
        session: TriggerMapPipelineSession,
        emotional_dna: EmotionalDNAProfile,
        parent_receipt_id: Optional[str],
    ) -> Optional[str]:
        """Phase 1 INGEST: Validate emotional_dna confidence ≥ 0.5.
        Write TMAP-INGEST receipt."""
        session.step_statuses["phase_1_ingest"] = (
            TriggerMapPipelineStepStatus.RUNNING
        )

        confidence = emotional_dna.extraction_status.confidence
        session.emotional_dna_confidence = confidence

        # Gate: confidence must be ≥ 0.5
        if confidence < EMOTIONAL_DNA_MINIMUM_CONFIDENCE:
            session.step_statuses["phase_1_ingest"] = (
                TriggerMapPipelineStepStatus.HALTED
            )
            raise TriggerMapPipelineError(
                f"DEP-LIB-001 confidence {confidence:.2f} < minimum "
                f"{EMOTIONAL_DNA_MINIMUM_CONFIDENCE}. Pipeline halted at "
                f"Phase 1 INGEST gate. Emotional DNA extraction must reach "
                f"≥{EMOTIONAL_DNA_MINIMUM_CONFIDENCE} confidence before "
                f"Trigger Map Builder can execute."
            )

        # Receipt: TMAP-INGEST
        entry = self.receipt_chain.log(
            agent_id="trigger_map_pipeline",
            action="TMAP-INGEST",
            asset_id=session.session_id,
            input_summary=(
                f"DEP-LIB-001 confidence: {confidence:.2f}, "
                f"populated: {emotional_dna.extraction_status.populated_variables}/10"
            ),
            output_summary=(
                f"INGEST passed: confidence {confidence:.2f} ≥ "
                f"{EMOTIONAL_DNA_MINIMUM_CONFIDENCE}"
            ),
            decision="approved",
            parent_receipt_id=parent_receipt_id,
            metadata={
                "emotional_dna_confidence": confidence,
                "populated_variables": emotional_dna.extraction_status.populated_variables,
                "minimum_required_confidence": EMOTIONAL_DNA_MINIMUM_CONFIDENCE,
            },
        )
        session.receipt_ids["TMAP-INGEST"] = entry.receipt_id
        session.step_statuses["phase_1_ingest"] = (
            TriggerMapPipelineStepStatus.COMPLETE
        )
        return entry.receipt_id

    # ──────────────────────────────────────────────────────────
    # Phase 2: Trigger Identification
    # ──────────────────────────────────────────────────────────

    def _execute_phase_2(
        self,
        session: TriggerMapPipelineSession,
        corpus_text: str,
        emotional_dna: EmotionalDNAProfile,
        parent_receipt_id: Optional[str],
    ) -> Optional[str]:
        """Phase 2: Identify triggers using LIWC-22 + V6-V10 MFT mapping."""
        session.step_statuses["phase_2_identification"] = (
            TriggerMapPipelineStepStatus.RUNNING
        )

        triggers = self.trigger_identifier.identify(
            corpus_text=corpus_text,
            emotional_dna=emotional_dna,
            session_id=session.session_id,
        )
        session.identified_triggers = triggers
        session.raw_trigger_count = len(triggers)

        entry = self.receipt_chain.log(
            agent_id="trigger_map_pipeline",
            action="TMAP-IDENTIFY",
            asset_id=session.session_id,
            input_summary="LIWC-22 + V6-V10 trigger scan",
            output_summary=f"Identified {len(triggers)} candidate triggers",
            decision="identified",
            parent_receipt_id=parent_receipt_id,
            metadata={
                "trigger_count": len(triggers),
            },
        )
        session.receipt_ids["TMAP-IDENTIFY"] = entry.receipt_id
        session.step_statuses["phase_2_identification"] = (
            TriggerMapPipelineStepStatus.COMPLETE
        )
        return entry.receipt_id

    # ──────────────────────────────────────────────────────────
    # Phase 3: Origin Classification
    # ──────────────────────────────────────────────────────────

    def _execute_phase_3(
        self,
        session: TriggerMapPipelineSession,
        corpus_text: str,
        parent_receipt_id: Optional[str],
    ) -> Optional[str]:
        """Phase 3: Conway AKB origin classification."""
        session.step_statuses["phase_3_origin"] = (
            TriggerMapPipelineStepStatus.RUNNING
        )

        triggers = self.akb_classifier.classify(
            triggers=session.identified_triggers,
            corpus_text=corpus_text,
            session_id=session.session_id,
        )
        session.identified_triggers = triggers

        # Count AKB levels
        esk_count = sum(
            1
            for t in triggers
            if t.originating_experience.akb_level
            and t.originating_experience.akb_level.value == "event_specific_knowledge"
        )

        entry = self.receipt_chain.log(
            agent_id="trigger_map_pipeline",
            action="TMAP-AKB-CLASSIFY",
            asset_id=session.session_id,
            input_summary=f"AKB classification for {len(triggers)} triggers",
            output_summary=(
                f"Classified: {len(triggers)} triggers, "
                f"ESK-level: {esk_count}"
            ),
            decision="classified",
            parent_receipt_id=parent_receipt_id,
            metadata={
                "trigger_count": len(triggers),
                "esk_count": esk_count,
            },
        )
        session.receipt_ids["TMAP-AKB-CLASSIFY"] = entry.receipt_id
        session.step_statuses["phase_3_origin"] = (
            TriggerMapPipelineStepStatus.COMPLETE
        )
        return entry.receipt_id

    # ──────────────────────────────────────────────────────────
    # Phase 4: PTG Assessment (HARD EXCLUDE)
    # ──────────────────────────────────────────────────────────

    def _execute_phase_4(
        self,
        session: TriggerMapPipelineSession,
        corpus_text: str,
        parent_receipt_id: Optional[str],
    ) -> Optional[str]:
        """Phase 4: PTG assessment with HARD EXCLUDE for raw_unresolved.
        AC2: raw_unresolved triggers are EXCLUDED at code level."""
        session.step_statuses["phase_4_ptg"] = (
            TriggerMapPipelineStepStatus.RUNNING
        )

        resolved, active, excluded = self.ptg_assessor.assess(
            triggers=session.identified_triggers,
            corpus_text=corpus_text,
            session_id=session.session_id,
        )

        # HARD EXCLUDE: raw_unresolved triggers are removed from pipeline
        # They will NEVER appear in the output
        session.excluded_trigger_count = len(excluded)

        # Only resolved + active continue through the pipeline
        session.identified_triggers = resolved + active

        entry = self.receipt_chain.log(
            agent_id="trigger_map_pipeline",
            action="TMAP-PTG-ASSESS",
            asset_id=session.session_id,
            input_summary=f"PTG assessment for {len(resolved) + len(active) + len(excluded)} triggers",
            output_summary=(
                f"Resolved: {len(resolved)}, Active: {len(active)}, "
                f"EXCLUDED (raw_unresolved): {len(excluded)}"
            ),
            decision="assessed",
            parent_receipt_id=parent_receipt_id,
            metadata={
                "resolved_count": len(resolved),
                "active_count": len(active),
                "excluded_count": len(excluded),
                "safety_gate": "raw_unresolved_hard_exclude",
            },
        )
        session.receipt_ids["TMAP-PTG-ASSESS"] = entry.receipt_id
        session.step_statuses["phase_4_ptg"] = (
            TriggerMapPipelineStepStatus.COMPLETE
        )
        return entry.receipt_id

    # ──────────────────────────────────────────────────────────
    # Phase 5: Narrative Identity
    # ──────────────────────────────────────────────────────────

    def _execute_phase_5(
        self,
        session: TriggerMapPipelineSession,
        corpus_text: str,
        parent_receipt_id: Optional[str],
    ) -> Optional[str]:
        """Phase 5: McAdams narrative identity classification."""
        session.step_statuses["phase_5_narrative"] = (
            TriggerMapPipelineStepStatus.RUNNING
        )

        triggers = self.narrative_classifier.classify(
            triggers=session.identified_triggers,
            corpus_text=corpus_text,
            session_id=session.session_id,
        )
        session.identified_triggers = triggers

        entry = self.receipt_chain.log(
            agent_id="trigger_map_pipeline",
            action="TMAP-NARRATIVE",
            asset_id=session.session_id,
            input_summary=f"Narrative identity for {len(triggers)} triggers",
            output_summary=f"Classified {len(triggers)} triggers with narrative identity",
            decision="classified",
            parent_receipt_id=parent_receipt_id,
            metadata={
                "trigger_count": len(triggers),
            },
        )
        session.receipt_ids["TMAP-NARRATIVE"] = entry.receipt_id
        session.step_statuses["phase_5_narrative"] = (
            TriggerMapPipelineStepStatus.COMPLETE
        )
        return entry.receipt_id

    # ──────────────────────────────────────────────────────────
    # Phase 6: Reconsolidation Sensitivity
    # ──────────────────────────────────────────────────────────

    def _execute_phase_6(
        self,
        session: TriggerMapPipelineSession,
        emotional_dna: EmotionalDNAProfile,
        corpus_text: str,
        parent_receipt_id: Optional[str],
    ) -> Optional[str]:
        """Phase 6: Nader reconsolidation sensitivity + V1 cross-validation.
        AC7: Score cross-validated against V1 Trigger Specificity Threshold."""
        session.step_statuses["phase_6_reconsolidation"] = (
            TriggerMapPipelineStepStatus.RUNNING
        )

        triggers = self.reconsolidation_scorer.score(
            triggers=session.identified_triggers,
            emotional_dna=emotional_dna,
            corpus_text=corpus_text,
            session_id=session.session_id,
        )
        session.identified_triggers = triggers

        # Count V1-validated triggers
        v1_validated = sum(
            1
            for t in triggers
            if t.reconsolidation_sensitivity.v1_cross_validated
        )

        entry = self.receipt_chain.log(
            agent_id="trigger_map_pipeline",
            action="TMAP-RECONSOLIDATION",
            asset_id=session.session_id,
            input_summary=f"Reconsolidation scoring for {len(triggers)} triggers",
            output_summary=(
                f"Scored {len(triggers)} triggers, "
                f"V1 cross-validated: {v1_validated}"
            ),
            decision="scored",
            parent_receipt_id=parent_receipt_id,
            metadata={
                "trigger_count": len(triggers),
                "v1_cross_validated": v1_validated,
            },
        )
        session.receipt_ids["TMAP-RECONSOLIDATION"] = entry.receipt_id
        session.step_statuses["phase_6_reconsolidation"] = (
            TriggerMapPipelineStepStatus.COMPLETE
        )
        return entry.receipt_id

    # ──────────────────────────────────────────────────────────
    # Phase 7: Archetype Mapping
    # ──────────────────────────────────────────────────────────

    def _execute_phase_7(
        self,
        session: TriggerMapPipelineSession,
        ttt_baseline: Optional[dict[str, object]],
        parent_receipt_id: Optional[str],
    ) -> Optional[str]:
        """Phase 7: Archetype mapping + TTT eligibility."""
        session.step_statuses["phase_7_archetype"] = (
            TriggerMapPipelineStepStatus.RUNNING
        )

        triggers, archetype_mappings = self.archetype_mapper.map_triggers(
            triggers=session.identified_triggers,
            ttt_baseline=ttt_baseline,
            session_id=session.session_id,
        )
        session.identified_triggers = triggers
        session.trigger_map.trigger_archetype_map = archetype_mappings

        eligible_count = sum(
            1 for m in archetype_mappings if m.coach_eligible is True
        )

        entry = self.receipt_chain.log(
            agent_id="trigger_map_pipeline",
            action="TMAP-ARCHETYPE",
            asset_id=session.session_id,
            input_summary=f"Archetype mapping for {len(triggers)} triggers",
            output_summary=(
                f"Mapped {len(archetype_mappings)} archetypes, "
                f"coach eligible: {eligible_count}"
            ),
            decision="mapped",
            parent_receipt_id=parent_receipt_id,
            metadata={
                "archetype_count": len(archetype_mappings),
                "eligible_count": eligible_count,
            },
        )
        session.receipt_ids["TMAP-ARCHETYPE"] = entry.receipt_id
        session.step_statuses["phase_7_archetype"] = (
            TriggerMapPipelineStepStatus.COMPLETE
        )
        return entry.receipt_id

    # ──────────────────────────────────────────────────────────
    # Phase 8: EMIT
    # ──────────────────────────────────────────────────────────

    def _execute_phase_8(
        self,
        session: TriggerMapPipelineSession,
        parent_receipt_id: Optional[str],
    ) -> Optional[str]:
        """Phase 8 EMIT: Build DEP-LIB-002 trigger_map.json output.
        Partitions triggers into triggers[] and candidate_triggers[]."""
        session.step_statuses["phase_8_emit"] = (
            TriggerMapPipelineStepStatus.RUNNING
        )

        trigger_map = session.trigger_map
        trigger_map.coach_id = self.coach_id

        # Partition triggers by PTG status
        for trigger in session.identified_triggers:
            if trigger.ptg_status.is_fully_resolved():
                trigger_map.triggers.append(trigger)
            else:
                # active_processing → candidate_triggers[]
                trigger_map.candidate_triggers.append(trigger)

        session.classified_trigger_count = (
            len(trigger_map.triggers) + len(trigger_map.candidate_triggers)
        )

        # Compute status and confidence
        trigger_map.compute_status()
        trigger_map.compute_confidence()
        trigger_map.compute_hash()

        entry = self.receipt_chain.log(
            agent_id="trigger_map_pipeline",
            action="TMAP-EMIT",
            asset_id=session.session_id,
            input_summary="Trigger map assembly",
            output_summary=(
                f"triggers[]: {len(trigger_map.triggers)}, "
                f"candidate_triggers[]: {len(trigger_map.candidate_triggers)}, "
                f"excluded: {session.excluded_trigger_count}, "
                f"confidence: {trigger_map.map_status.confidence or 0:.2f}"
            ),
            decision="assembled",
            parent_receipt_id=parent_receipt_id,
            metadata={
                "resolved_triggers": len(trigger_map.triggers),
                "candidate_triggers": len(trigger_map.candidate_triggers),
                "excluded_triggers": session.excluded_trigger_count,
                "confidence": trigger_map.map_status.confidence,
                "map_hash": trigger_map.map_hash,
            },
        )
        session.receipt_ids["TMAP-EMIT"] = entry.receipt_id
        session.step_statuses["phase_8_emit"] = (
            TriggerMapPipelineStepStatus.COMPLETE
        )
        return entry.receipt_id

    # ──────────────────────────────────────────────────────────
    # Phase 9: VALIDATE & CHECKPOINT
    # ──────────────────────────────────────────────────────────

    def _execute_phase_9(
        self,
        session: TriggerMapPipelineSession,
        parent_receipt_id: Optional[str],
    ) -> Optional[str]:
        """Phase 9: Run 9 validation checks, write outputs, TMAP-COMPLETE receipt."""
        session.step_statuses["phase_9_validate"] = (
            TriggerMapPipelineStepStatus.RUNNING
        )

        trigger_map = session.trigger_map

        # Run 9 validation checks
        validation = self._run_validation_checks(session)
        session.validation_result = validation

        # Write trigger_map.json
        self._write_trigger_map(session)

        # Update coach_soul.json
        self._update_coach_soul(session)

        # Receipt: TMAP-COMPLETE
        entry = self.receipt_chain.log(
            agent_id="trigger_map_pipeline",
            action="TMAP-COMPLETE",
            asset_id=session.session_id,
            input_summary="Validation + checkpoint",
            output_summary=(
                f"Validation: {'PASSED' if validation.all_passed else 'FLAGGED'}, "
                f"Minimum viable: {validation.minimum_viable}, "
                f"DEP-LIB-002 written: {session.dep_lib_002_written}"
            ),
            decision="validated" if validation.all_passed else "flagged",
            parent_receipt_id=parent_receipt_id,
            metadata={
                "checks_passed": sum(1 for c in validation.checks if c.passed),
                "checks_total": len(validation.checks),
                "minimum_viable": validation.minimum_viable,
                "dep_lib_002_written": session.dep_lib_002_written,
                "coach_soul_updated": session.coach_soul_updated,
            },
        )
        session.receipt_ids["TMAP-COMPLETE"] = entry.receipt_id
        session.step_statuses["phase_9_validate"] = (
            TriggerMapPipelineStepStatus.COMPLETE
        )
        return entry.receipt_id

    def _run_validation_checks(
        self, session: TriggerMapPipelineSession
    ) -> TriggerMapValidationResult:
        """Run all 9 validation checks per spec."""
        trigger_map = session.trigger_map
        checks: list[TriggerMapValidationCheck] = []

        # Check 1: At least 1 trigger identified
        checks.append(
            TriggerMapValidationCheck(
                check_id="V1",
                check_name="trigger_count",
                passed=trigger_map.map_status.total_triggers_mapped > 0,
                detail=(
                    f"Total triggers: {trigger_map.map_status.total_triggers_mapped}"
                ),
            )
        )

        # Check 2: Minimum 2 resolved_dual_layer triggers (AC4)
        checks.append(
            TriggerMapValidationCheck(
                check_id="V2",
                check_name="minimum_resolved_triggers",
                passed=len(trigger_map.triggers) >= MINIMUM_RESOLVED_TRIGGERS,
                detail=(
                    f"Resolved triggers: {len(trigger_map.triggers)} "
                    f"(minimum: {MINIMUM_RESOLVED_TRIGGERS})"
                ),
            )
        )

        # Check 3: All triggers have moral foundation mapping
        all_triggers = trigger_map.triggers + trigger_map.candidate_triggers
        mft_mapped = sum(
            1 for t in all_triggers if t.moral_foundation.is_populated()
        )
        checks.append(
            TriggerMapValidationCheck(
                check_id="V3",
                check_name="moral_foundation_coverage",
                passed=mft_mapped == len(all_triggers) if all_triggers else True,
                detail=f"MFT mapped: {mft_mapped}/{len(all_triggers)}",
            )
        )

        # Check 4: All triggers have AKB classification
        akb_classified = sum(
            1
            for t in all_triggers
            if t.originating_experience.is_populated()
        )
        checks.append(
            TriggerMapValidationCheck(
                check_id="V4",
                check_name="akb_classification_coverage",
                passed=akb_classified == len(all_triggers) if all_triggers else True,
                detail=f"AKB classified: {akb_classified}/{len(all_triggers)}",
            )
        )

        # Check 5: All triggers have narrative identity
        narrative_classified = sum(
            1
            for t in all_triggers
            if t.narrative_identity.is_populated()
        )
        checks.append(
            TriggerMapValidationCheck(
                check_id="V5",
                check_name="narrative_identity_coverage",
                passed=narrative_classified == len(all_triggers) if all_triggers else True,
                detail=f"Narrative classified: {narrative_classified}/{len(all_triggers)}",
            )
        )

        # Check 6: All triggers have reconsolidation score
        recon_scored = sum(
            1
            for t in all_triggers
            if t.reconsolidation_sensitivity.is_populated()
        )
        checks.append(
            TriggerMapValidationCheck(
                check_id="V6",
                check_name="reconsolidation_coverage",
                passed=recon_scored == len(all_triggers) if all_triggers else True,
                detail=f"Reconsolidation scored: {recon_scored}/{len(all_triggers)}",
            )
        )

        # Check 7: No raw_unresolved triggers in output (AC2)
        raw_in_output = sum(
            1
            for t in all_triggers
            if not t.is_content_safe()
        )
        checks.append(
            TriggerMapValidationCheck(
                check_id="V7",
                check_name="ptg_safety_gate",
                passed=raw_in_output == 0,
                detail=(
                    f"raw_unresolved in output: {raw_in_output} "
                    f"(must be 0 — HARD EXCLUDE)"
                ),
            )
        )

        # Check 8: Archetype mapping table present
        checks.append(
            TriggerMapValidationCheck(
                check_id="V8",
                check_name="archetype_mapping_present",
                passed=len(trigger_map.trigger_archetype_map) > 0,
                detail=f"Archetype mappings: {len(trigger_map.trigger_archetype_map)}",
            )
        )

        # Check 9: Map hash computed
        checks.append(
            TriggerMapValidationCheck(
                check_id="V9",
                check_name="integrity_hash",
                passed=bool(trigger_map.map_hash),
                detail=f"Map hash: {trigger_map.map_hash[:16] if trigger_map.map_hash else 'MISSING'}",
            )
        )

        result = TriggerMapValidationResult(
            checks=checks,
            minimum_viable=len(trigger_map.triggers) >= MINIMUM_RESOLVED_TRIGGERS,
        )
        result.compute_result()
        return result

    def _write_trigger_map(self, session: TriggerMapPipelineSession) -> None:
        """Write DEP-LIB-002 trigger_map.json to coach directory."""
        output_dir = self.coach_dir / "intelligence_library"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "trigger_map.json"

        data = session.trigger_map.model_dump(mode="json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)

        session.dep_lib_002_written = True

    def _update_coach_soul(self, session: TriggerMapPipelineSession) -> None:
        """Update coach_soul.json with trigger map reference."""
        coach_soul_path = self.coach_dir / "intelligence_library" / "coach_soul.json"

        if coach_soul_path.exists():
            try:
                with open(coach_soul_path, "r", encoding="utf-8") as f:
                    coach_soul = json.load(f)
            except (json.JSONDecodeError, OSError):
                coach_soul = {}
        else:
            coach_soul = {}

        # Update trigger map reference
        coach_soul["trigger_map_ref"] = {
            "dep_id": "DEP-LIB-002",
            "status": "built",
            "last_built": datetime.now(timezone.utc).isoformat(),
            "resolved_triggers": len(session.trigger_map.triggers),
            "candidate_triggers": len(session.trigger_map.candidate_triggers),
            "confidence": session.trigger_map.map_status.confidence,
            "session_id": session.session_id,
        }

        # Write back
        coach_soul_dir = coach_soul_path.parent
        coach_soul_dir.mkdir(parents=True, exist_ok=True)

        with open(coach_soul_path, "w", encoding="utf-8") as f:
            json.dump(coach_soul, f, indent=2, default=str)

        session.coach_soul_updated = True
