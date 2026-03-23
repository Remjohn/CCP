"""
CCP FR4 Emotional DNA Pipeline Orchestrator — Unit 7
7-phase extraction pipeline with receipt chain + coach_soul update.

Spec reference: FR4 Tech Spec §Phase 1-7

Pipeline phases:
  Phase 1:  INGEST — Validate corpus ≥3000 words, write EDNA-INGEST receipt
  Phase 2:  REASON (Triage) — Barrett granularity triage → tier classification
  Phase 3:  REASON (Extract) — V1-V5 appraisal + V6-V10 MFQ-2 extraction
  Phase 4:  REASON (CSIP) — EXT-1 through EXT-5 behavioral extensions
  Phase 5:  EMIT — Build DEP-LIB-001 output profile, compute confidence
  Phase 6:  VALIDATE — Constraints A/B/C/D cross-validation
  Phase 7:  CHECKPOINT — Write DEP-LIB-001 JSON, update coach_soul,
            write EDNA-VALIDATION-COMPLETE receipt, check FR3 readiness

Receipt chain:
  - EDNA-INGEST at Phase 1
  - EDNA-VALIDATION-COMPLETE at Phase 6/7 boundary

Mandate 7 enforcement: corpus citation for every variable (via extractors).
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.emotional_dna_models import (
    MINIMUM_CORPUS_WORDS,
    CrossValidationResult,
    EmotionalDNAPipelineSession,
    EmotionalDNAPipelineStepStatus,
    EmotionalDNAProfile,
    ExtractionStatus,
    GranularityTriageResult,
    TriageTier,
)
from src.ccp.services.appraisal_extractor import AppraisalExtractor
from src.ccp.services.cross_validator import CrossValidator
from src.ccp.services.csip_v3_extractor import CSIPv3Extractor
from src.ccp.services.granularity_triage import GranularityTriageService
from src.ccp.services.moral_foundation_extractor import MoralFoundationExtractor


class EmotionalDNAPipelineError(Exception):
    """Top-level pipeline error for FR4."""
    pass


class EmotionalDNAPipeline:
    """Orchestrates the complete FR4 Emotional DNA Extraction pipeline.

    This is the main entry point for FR4 execution. It runs all 7 phases
    in sequence, enforces quality gates, writes receipt chain entries,
    and updates the coach_soul.json on completion.

    Spec §Phase 1 Gate: corpus ≥ 3000 authenticated words.
    Spec §Phase 6: Cross-validation constraints A-D.
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
        self.triage_service = GranularityTriageService()
        self.appraisal_extractor = AppraisalExtractor()
        self.mft_extractor = MoralFoundationExtractor()
        self.csip_extractor = CSIPv3Extractor()
        self.cross_validator = CrossValidator()

    def execute(
        self,
        corpus_text: str,
        corpus_sources: Optional[list[str]] = None,
        parent_receipt_id: Optional[str] = None,
    ) -> EmotionalDNAPipelineSession:
        """Execute the complete FR4 pipeline.

        Args:
            corpus_text: Full concatenated corpus text (≥3000 words).
            corpus_sources: List of source identifiers for the corpus.
            parent_receipt_id: Receipt ID from FR3's final stage (chain link).

        Returns:
            EmotionalDNAPipelineSession with all phase outputs and receipt IDs.

        Raises:
            EmotionalDNAPipelineError: On unrecoverable pipeline failure.
        """
        session = EmotionalDNAPipelineSession(
            session_id=f"EDNA-{self.coach_acronym}-{uuid.uuid4().hex[:8]}",
            coach_id=self.coach_id,
            coach_acronym=self.coach_acronym,
        )
        session.corpus_sources = corpus_sources or []

        last_receipt_id = parent_receipt_id

        try:
            # ── Phase 1: INGEST ──
            last_receipt_id = self._execute_phase_1(
                session, corpus_text, last_receipt_id
            )

            # ── Phase 2: REASON — Granularity Triage ──
            last_receipt_id = self._execute_phase_2(
                session, corpus_text, last_receipt_id
            )

            # ── Phase 3: REASON — V1-V5 + V6-V10 Extraction ──
            last_receipt_id = self._execute_phase_3(
                session, corpus_text, last_receipt_id
            )

            # ── Phase 4: REASON — CSIP v3 Extensions ──
            last_receipt_id = self._execute_phase_4(
                session, corpus_text, last_receipt_id
            )

            # ── Phase 5: EMIT — Build Profile ──
            last_receipt_id = self._execute_phase_5(
                session, last_receipt_id
            )

            # ── Phase 6: VALIDATE — Cross-Validation ──
            last_receipt_id = self._execute_phase_6(
                session, last_receipt_id
            )

            # ── Phase 7: CHECKPOINT — Write Outputs ──
            last_receipt_id = self._execute_phase_7(
                session, last_receipt_id
            )

        except EmotionalDNAPipelineError:
            raise
        except Exception as e:
            session.step_statuses["pipeline"] = EmotionalDNAPipelineStepStatus.FAILED
            raise EmotionalDNAPipelineError(
                f"FR4 pipeline failed: {e}"
            ) from e

        return session

    # ──────────────────────────────────────────────────────────
    # Phase 1: INGEST
    # ──────────────────────────────────────────────────────────

    def _execute_phase_1(
        self,
        session: EmotionalDNAPipelineSession,
        corpus_text: str,
        parent_receipt_id: Optional[str],
    ) -> Optional[str]:
        """Phase 1 INGEST: Validate corpus word count ≥ 3000.
        Write EDNA-INGEST receipt."""
        session.step_statuses["phase_1_ingest"] = (
            EmotionalDNAPipelineStepStatus.RUNNING
        )

        word_count = len(corpus_text.split())
        session.corpus_word_count = word_count

        if word_count < MINIMUM_CORPUS_WORDS:
            session.step_statuses["phase_1_ingest"] = (
                EmotionalDNAPipelineStepStatus.HALTED
            )
            raise EmotionalDNAPipelineError(
                f"Corpus word count {word_count} < minimum {MINIMUM_CORPUS_WORDS}. "
                f"Pipeline halted at Phase 1 INGEST gate."
            )

        # Receipt: EDNA-INGEST
        entry = self.receipt_chain.log(
            agent_id="emotional_dna_pipeline",
            action="EDNA-INGEST",
            asset_id=session.session_id,
            input_summary=f"Corpus: {word_count} words from {len(session.corpus_sources)} sources",
            output_summary=f"INGEST passed: {word_count} ≥ {MINIMUM_CORPUS_WORDS}",
            decision="approved",
            parent_receipt_id=parent_receipt_id,
            metadata={
                "word_count": word_count,
                "minimum_required": MINIMUM_CORPUS_WORDS,
                "source_count": len(session.corpus_sources),
            },
        )
        session.receipt_ids["EDNA-INGEST"] = entry.receipt_id
        session.step_statuses["phase_1_ingest"] = (
            EmotionalDNAPipelineStepStatus.COMPLETE
        )
        return entry.receipt_id

    # ──────────────────────────────────────────────────────────
    # Phase 2: REASON — Granularity Triage
    # ──────────────────────────────────────────────────────────

    def _execute_phase_2(
        self,
        session: EmotionalDNAPipelineSession,
        corpus_text: str,
        parent_receipt_id: Optional[str],
    ) -> Optional[str]:
        """Phase 2 REASON: Barrett granularity triage classification."""
        session.step_statuses["phase_2_triage"] = (
            EmotionalDNAPipelineStepStatus.RUNNING
        )

        triage_result = self.triage_service.triage(corpus_text)
        session.triage_result = triage_result

        entry = self.receipt_chain.log(
            agent_id="emotional_dna_pipeline",
            action="EDNA-TRIAGE",
            asset_id=session.session_id,
            input_summary=f"Corpus for granularity triage",
            output_summary=(
                f"Tier: {triage_result.tier.value if triage_result.tier else 'UNKNOWN'}, "
                f"Distinct terms: {triage_result.distinct_emotional_term_count}"
            ),
            decision="classified",
            parent_receipt_id=parent_receipt_id,
            metadata={
                "tier": triage_result.tier.value if triage_result.tier else None,
                "distinct_term_count": triage_result.distinct_emotional_term_count,
            },
        )
        session.receipt_ids["EDNA-TRIAGE"] = entry.receipt_id
        session.step_statuses["phase_2_triage"] = (
            EmotionalDNAPipelineStepStatus.COMPLETE
        )
        return entry.receipt_id

    # ──────────────────────────────────────────────────────────
    # Phase 3: REASON — V1-V5 + V6-V10 Extraction
    # ──────────────────────────────────────────────────────────

    def _execute_phase_3(
        self,
        session: EmotionalDNAPipelineSession,
        corpus_text: str,
        parent_receipt_id: Optional[str],
    ) -> Optional[str]:
        """Phase 3 REASON: Extract V1-V5 + V6-V10 from corpus."""
        session.step_statuses["phase_3_extraction"] = (
            EmotionalDNAPipelineStepStatus.RUNNING
        )

        # Determine triage tier (default to MEDIUM if somehow missing)
        tier = TriageTier.MEDIUM
        if session.triage_result and session.triage_result.tier:
            tier = session.triage_result.tier

        # V1-V5 Cognitive Appraisal
        appraisal_vars = self.appraisal_extractor.extract(
            corpus_text=corpus_text,
            triage_tier=tier,
            session_id=session.session_id,
        )
        session.profile.appraisal_variables = appraisal_vars

        # V6-V10 Moral Foundations
        moral_foundations = self.mft_extractor.extract(
            corpus_text=corpus_text,
            session_id=session.session_id,
        )
        session.profile.moral_foundations = moral_foundations

        appraisal_count = appraisal_vars.populated_count()
        mft_count = moral_foundations.populated_count()

        entry = self.receipt_chain.log(
            agent_id="emotional_dna_pipeline",
            action="EDNA-EXTRACTION",
            asset_id=session.session_id,
            input_summary=f"Corpus extraction at {tier.value} tier",
            output_summary=(
                f"V1-V5: {appraisal_count}/5 populated, "
                f"V6-V10: {mft_count}/5 populated"
            ),
            decision="extracted",
            parent_receipt_id=parent_receipt_id,
            metadata={
                "triage_tier": tier.value,
                "appraisal_populated": appraisal_count,
                "mft_populated": mft_count,
            },
        )
        session.receipt_ids["EDNA-EXTRACTION"] = entry.receipt_id
        session.step_statuses["phase_3_extraction"] = (
            EmotionalDNAPipelineStepStatus.COMPLETE
        )
        return entry.receipt_id

    # ──────────────────────────────────────────────────────────
    # Phase 4: REASON — CSIP v3.0 Extensions
    # ──────────────────────────────────────────────────────────

    def _execute_phase_4(
        self,
        session: EmotionalDNAPipelineSession,
        corpus_text: str,
        parent_receipt_id: Optional[str],
    ) -> Optional[str]:
        """Phase 4 REASON: Extract CSIP v3 extensions EXT-1 through EXT-5."""
        session.step_statuses["phase_4_csip"] = (
            EmotionalDNAPipelineStepStatus.RUNNING
        )

        csip_extensions = self.csip_extractor.extract(
            corpus_text=corpus_text,
            session_id=session.session_id,
        )
        session.profile.csip_v3_extensions = csip_extensions

        csip_count = csip_extensions.populated_count()

        entry = self.receipt_chain.log(
            agent_id="emotional_dna_pipeline",
            action="EDNA-CSIP",
            asset_id=session.session_id,
            input_summary="CSIP v3 extension extraction",
            output_summary=f"EXT-1 through EXT-5: {csip_count}/5 populated",
            decision="extracted",
            parent_receipt_id=parent_receipt_id,
            metadata={
                "csip_populated": csip_count,
            },
        )
        session.receipt_ids["EDNA-CSIP"] = entry.receipt_id
        session.step_statuses["phase_4_csip"] = (
            EmotionalDNAPipelineStepStatus.COMPLETE
        )
        return entry.receipt_id

    # ──────────────────────────────────────────────────────────
    # Phase 5: EMIT — Build Profile
    # ──────────────────────────────────────────────────────────

    def _execute_phase_5(
        self,
        session: EmotionalDNAPipelineSession,
        parent_receipt_id: Optional[str],
    ) -> Optional[str]:
        """Phase 5 EMIT: Assemble final DEP-LIB-001 output."""
        session.step_statuses["phase_5_emit"] = (
            EmotionalDNAPipelineStepStatus.RUNNING
        )

        profile = session.profile

        # Compute confidence scores
        profile.compute_confidence()

        # Fill extraction status metadata
        tier = TriageTier.MEDIUM
        if session.triage_result and session.triage_result.tier:
            tier = session.triage_result.tier

        profile.extraction_status.triage_tier = tier
        profile.extraction_status.corpus_word_count = session.corpus_word_count
        profile.extraction_status.sources_used = session.corpus_sources
        profile.extraction_status.last_extracted = (
            datetime.now(timezone.utc).isoformat()
        )

        # Compute profile hash for integrity
        profile.compute_hash()

        entry = self.receipt_chain.log(
            agent_id="emotional_dna_pipeline",
            action="EDNA-EMIT",
            asset_id=session.session_id,
            input_summary="Profile assembly",
            output_summary=(
                f"Confidence: {profile.extraction_status.confidence:.2f}, "
                f"Variables: {profile.extraction_status.populated_variables}/10, "
                f"CSIP: {profile.extraction_status.csip_v3_populated}/5"
            ),
            decision="assembled",
            parent_receipt_id=parent_receipt_id,
            metadata={
                "confidence": profile.extraction_status.confidence,
                "populated_variables": profile.extraction_status.populated_variables,
                "csip_populated": profile.extraction_status.csip_v3_populated,
                "profile_hash": profile.profile_hash,
            },
        )
        session.receipt_ids["EDNA-EMIT"] = entry.receipt_id
        session.step_statuses["phase_5_emit"] = (
            EmotionalDNAPipelineStepStatus.COMPLETE
        )
        return entry.receipt_id

    # ──────────────────────────────────────────────────────────
    # Phase 6: VALIDATE — Cross-Validation
    # ──────────────────────────────────────────────────────────

    def _execute_phase_6(
        self,
        session: EmotionalDNAPipelineSession,
        parent_receipt_id: Optional[str],
    ) -> Optional[str]:
        """Phase 6 VALIDATE: Run constraint checks A-D."""
        session.step_statuses["phase_6_validate"] = (
            EmotionalDNAPipelineStepStatus.RUNNING
        )

        triage_result = session.triage_result or GranularityTriageResult(
            tier=TriageTier.MEDIUM,
        )

        validation_result = self.cross_validator.validate(
            profile=session.profile,
            triage_result=triage_result,
        )
        session.cross_validation = validation_result

        # Recompute confidence after potential nullifications
        session.profile.compute_confidence()
        session.profile.compute_hash()

        decision = "validated" if validation_result.all_passed() else "flagged"
        if validation_result.operator_review_required:
            decision = "flagged_operator_review"

        # Receipt: EDNA-VALIDATION-COMPLETE
        entry = self.receipt_chain.log(
            agent_id="emotional_dna_pipeline",
            action="EDNA-VALIDATION-COMPLETE",
            asset_id=session.session_id,
            input_summary="Cross-validation constraints A-D",
            output_summary=(
                f"A:{validation_result.constraint_a_passed} "
                f"B:{validation_result.constraint_b_passed} "
                f"C:{validation_result.constraint_c_passed} "
                f"D:{validation_result.constraint_d_passed} "
                f"Nullified: {validation_result.variables_forced_to_null} "
                f"Flags: {len(validation_result.incoherence_flags)}"
            ),
            decision=decision,
            parent_receipt_id=parent_receipt_id,
            metadata={
                "constraint_a": validation_result.constraint_a_passed,
                "constraint_b": validation_result.constraint_b_passed,
                "constraint_c": validation_result.constraint_c_passed,
                "constraint_d": validation_result.constraint_d_passed,
                "nullified_count": len(validation_result.variables_forced_to_null),
                "incoherence_count": len(validation_result.incoherence_flags),
                "operator_review": validation_result.operator_review_required,
                "final_confidence": session.profile.extraction_status.confidence,
                "final_hash": session.profile.profile_hash,
            },
        )
        session.receipt_ids["EDNA-VALIDATION-COMPLETE"] = entry.receipt_id
        session.step_statuses["phase_6_validate"] = (
            EmotionalDNAPipelineStepStatus.COMPLETE
        )
        return entry.receipt_id

    # ──────────────────────────────────────────────────────────
    # Phase 7: CHECKPOINT — Write Outputs
    # ──────────────────────────────────────────────────────────

    def _execute_phase_7(
        self,
        session: EmotionalDNAPipelineSession,
        parent_receipt_id: Optional[str],
    ) -> Optional[str]:
        """Phase 7 CHECKPOINT: Write DEP-LIB-001, update coach_soul,
        check FR3 readiness."""
        session.step_statuses["phase_7_checkpoint"] = (
            EmotionalDNAPipelineStepStatus.RUNNING
        )

        # 1. Write DEP-LIB-001 JSON
        dep_lib_path = self._write_dep_lib_001(session)
        session.dep_lib_001_written = True

        # 2. Update coach_soul.json
        self._update_coach_soul(session)
        session.coach_soul_updated = True

        # 3. Check FR3 readiness (voice DNA must exist)
        fr3_ready = self._check_fr3_readiness()
        session.fr3_readiness_checked = True

        entry = self.receipt_chain.log(
            agent_id="emotional_dna_pipeline",
            action="EDNA-CHECKPOINT",
            asset_id=session.session_id,
            input_summary="Writing outputs and updating coach_soul",
            output_summary=(
                f"DEP-LIB-001 written: {session.dep_lib_001_written}, "
                f"Coach soul updated: {session.coach_soul_updated}, "
                f"FR3 ready: {fr3_ready}"
            ),
            decision="checkpoint_complete",
            parent_receipt_id=parent_receipt_id,
            metadata={
                "dep_lib_001_path": str(dep_lib_path),
                "coach_soul_updated": session.coach_soul_updated,
                "fr3_readiness": fr3_ready,
            },
        )
        session.receipt_ids["EDNA-CHECKPOINT"] = entry.receipt_id
        session.step_statuses["phase_7_checkpoint"] = (
            EmotionalDNAPipelineStepStatus.COMPLETE
        )
        return entry.receipt_id

    # ──────────────────────────────────────────────────────────
    # Output Writers
    # ──────────────────────────────────────────────────────────

    def _write_dep_lib_001(
        self,
        session: EmotionalDNAPipelineSession,
    ) -> Path:
        """Write the DEP-LIB-001 emotional_dna.json file.

        Output path: coaches/{ACRONYM}/intelligence_library/emotional_dna.json
        """
        output_dir = self.coach_dir / "intelligence_library"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "emotional_dna.json"

        profile_data = session.profile.model_dump(mode="json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(profile_data, f, indent=2, default=str)

        return output_path

    def _update_coach_soul(
        self,
        session: EmotionalDNAPipelineSession,
    ) -> None:
        """Update coach_soul.json with DEP-LIB-001 reference.

        Spec §Phase 7: "Update coach_soul.json → emotional_dna_profile → dep_id,
        version, confidence, last_extracted"
        """
        soul_path = self.coach_dir / "coach_soul.json"

        soul_data: dict[str, Any] = {}
        if soul_path.exists():
            with open(soul_path, "r", encoding="utf-8") as f:
                soul_data = json.load(f)

        # Update emotional_dna_profile section
        soul_data["emotional_dna_profile"] = {
            "dep_id": session.profile.dep_id,
            "version": session.profile.version,
            "confidence": session.profile.extraction_status.confidence,
            "populated_variables": session.profile.extraction_status.populated_variables,
            "total_variables": session.profile.extraction_status.total_variables,
            "csip_v3_populated": session.profile.extraction_status.csip_v3_populated,
            "triage_tier": (
                session.profile.extraction_status.triage_tier.value
                if session.profile.extraction_status.triage_tier
                else None
            ),
            "last_extracted": session.profile.extraction_status.last_extracted,
            "profile_hash": session.profile.profile_hash,
        }

        with open(soul_path, "w", encoding="utf-8") as f:
            json.dump(soul_data, f, indent=2, default=str)

    def _check_fr3_readiness(self) -> bool:
        """Check that FR3 Voice DNA assets exist (prerequisite for downstream).

        Returns True if voice_dna.json exists in the intelligence_library.
        """
        voice_dna_path = self.coach_dir / "intelligence_library" / "voice_dna.json"
        return voice_dna_path.exists()
