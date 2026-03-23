"""
CCP FR3 Voice DNA Pipeline Orchestrator — Unit 10
10-step agentic extraction pipeline with receipt chain + V5.0 extension triggers.

Spec reference: FR3 Tech Spec §Steps 1-10 + §V5.0 Extension
Agent: Valeriane (Steps 1-9), Sophia + Adversarial Validator (Step 10)

Pipeline stages:
  Step 1:  Corpus Assembly (≥3000 unique words gate)
  Step 2:  Discourse Marker Census (8+ markers, position mapping)
  Step 3:  Cross-Topic Invariance Test (±15%, ≥12 invariant markers gate)
  Step 4:  Sentence Skeleton Extraction (6-cluster stylometry profile)
  Step 5:  Negative Space Excavation (DEP-ENG-004, Gate PC-03 ≥15 strings)
  Step 6-8: Positive Space Extraction (DEP-ENG-003 + humor classification)
  Step 9:  Emotional DNA Integration Test (Mandate 7, DEP-LIB-001 prereq)
  Step 10: Adversarial Validation (TTT <15%, AI <5%, Boredom ≤0.85, 3 rewinds)

Post-Step-10: V5.0 Extension (Steps 0-A through 0-D triggers)

Mandate 4 enforcement: Step 5 must complete before Steps 6-8.
Receipt chain: Every step writes a linked receipt per FR47 DEP-ENG-041.
"""

import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.voice_dna_models import (
    MAX_ADVERSARIAL_REWIND_CYCLES,
    PipelineStepStatus,
    V50ExtensionStatus,
    VoiceDNAPipelineSession,
)
from src.ccp.services.adversarial_validator import AdversarialValidator
from src.ccp.services.corpus_assembler import CorpusAssembler
from src.ccp.services.cross_topic_invariance import CrossTopicInvarianceTest
from src.ccp.services.discourse_marker_census import DiscourseMarkerCensus
from src.ccp.services.emotional_dna_test import EmotionalDNAIntegrationTest
from src.ccp.services.negative_space_excavator import NegativeSpaceExcavator
from src.ccp.services.positive_space_extractor import PositiveSpaceExtractor
from src.ccp.services.sentence_skeleton_extractor import SentenceSkeletonExtractor


class VoiceDNAPipelineError(Exception):
    """Top-level pipeline error."""
    pass


class VoiceDNAPipeline:
    """Orchestrates the complete FR3 Voice DNA Extraction pipeline.

    This is the main entry point for FR3 execution. It runs all 10 steps
    in sequence, enforces quality gates, writes receipt chain entries,
    and triggers V5.0 extensions on completion.

    Mandate 4 enforcement: Step 5 MUST produce DEP-ENG-004 before
    Steps 6-8 can execute. This is a code-level gate.
    """

    def __init__(
        self,
        coach_id: str,
        coach_acronym: str,
        coach_dir: Path,
        receipt_chain: Optional[ReceiptChain] = None,
        spacy_model: Optional[Any] = None,
        llm_client: Optional[Any] = None,
        ttt_extractor: Optional[Any] = None,
        ai_detector: Optional[Any] = None,
        episodic_memory: Optional[Any] = None,
    ):
        self.coach_id = coach_id
        self.coach_acronym = coach_acronym.upper()
        self.coach_dir = Path(coach_dir)
        self.receipt_chain = receipt_chain or ReceiptChain(coach_acronym=self.coach_acronym)
        self.spacy_model = spacy_model
        self.llm_client = llm_client

        # Initialize all service units
        self.corpus_assembler = CorpusAssembler(
            coach_id=coach_id, coach_acronym=coach_acronym, coach_dir=self.coach_dir
        )
        self.discourse_census = DiscourseMarkerCensus(spacy_model=spacy_model)
        self.invariance_test = CrossTopicInvarianceTest(discourse_census=self.discourse_census)
        self.skeleton_extractor = SentenceSkeletonExtractor(spacy_model=spacy_model)
        self.negative_excavator = NegativeSpaceExcavator()
        self.positive_extractor = PositiveSpaceExtractor()
        self.emotional_dna_test = EmotionalDNAIntegrationTest(
            coach_dir=self.coach_dir, llm_client=llm_client
        )
        self.adversarial_validator = AdversarialValidator(
            llm_client=llm_client,
            ttt_extractor=ttt_extractor,
            ai_detector=ai_detector,
            episodic_memory=episodic_memory,
        )

    def execute(
        self,
        parent_receipt_id: Optional[str] = None,
    ) -> VoiceDNAPipelineSession:
        """Execute the complete FR3 pipeline.

        Args:
            parent_receipt_id: Receipt ID from FR2's final stage (chain link).

        Returns:
            VoiceDNAPipelineSession with all step outputs and receipt IDs.

        Raises:
            VoiceDNAPipelineError: On unrecoverable pipeline failure.
        """
        session = VoiceDNAPipelineSession(
            session_id=f"VDNA-{self.coach_acronym}-{uuid.uuid4().hex[:8]}",
            coach_id=self.coach_id,
            coach_acronym=self.coach_acronym,
        )

        last_receipt_id = parent_receipt_id

        try:
            # ── Step 1: Corpus Assembly ──
            last_receipt_id = self._execute_step_1(session, last_receipt_id)

            # ── Step 2: Discourse Marker Census ──
            last_receipt_id = self._execute_step_2(session, last_receipt_id)

            # ── Step 3: Cross-Topic Invariance Test ──
            last_receipt_id = self._execute_step_3(session, last_receipt_id)

            # ── Step 4: Sentence Skeleton Extraction ──
            last_receipt_id = self._execute_step_4(session, last_receipt_id)

            # ── Step 5: Negative Space Excavation (Mandate 4 — First DEP) ──
            last_receipt_id = self._execute_step_5(session, last_receipt_id)

            # ── Steps 6-8: Positive Space Extraction + Humor ──
            last_receipt_id = self._execute_steps_6_8(session, last_receipt_id)

            # ── Step 9: Emotional DNA Integration Test (Mandate 7) ──
            last_receipt_id = self._execute_step_9(session, last_receipt_id)

            # ── Step 10: Adversarial Validation (with rewind loop) ──
            last_receipt_id = self._execute_step_10(session, last_receipt_id)

            # ── Write final outputs ──
            self._write_final_outputs(session)

            # ── V5.0 Extension Triggers ──
            self._trigger_v50_extensions(session)

        except Exception as e:
            # Record failure in session
            for step, status in session.step_statuses.items():
                if status == PipelineStepStatus.RUNNING:
                    session.step_statuses[step] = PipelineStepStatus.FAILED
            raise VoiceDNAPipelineError(
                f"FR3 pipeline failed: {e}"
            ) from e

        return session

    # ──────────────────────────────────────────────────────────
    # Step Implementations
    # ──────────────────────────────────────────────────────────

    def _execute_step_1(
        self, session: VoiceDNAPipelineSession, parent_receipt_id: Optional[str]
    ) -> str:
        """Step 1: Corpus Assembly."""
        session.step_statuses["step_1"] = PipelineStepStatus.RUNNING

        corpus = self.corpus_assembler.assemble()
        session.corpus = corpus

        receipt = self.receipt_chain.log(
            agent_id="Valeriane",
            action="VDNA-CORPUS-ASSEMBLY",
            asset_id=f"extraction_corpus_{self.coach_acronym}",
            input_summary=f"FR2 extraction_rounds from coach_soul.json",
            output_summary=(
                f"Corpus: {corpus.total_words} total words, "
                f"{corpus.unique_words} unique, "
                f"{len(corpus.units)} units, "
                f"{len(corpus.session_ids)} sessions"
            ),
            decision="CORPUS_ASSEMBLED",
            parent_receipt_id=parent_receipt_id,
            metadata={
                "corpus_hash": corpus.corpus_hash,
                "unique_words": corpus.unique_words,
                "unit_count": len(corpus.units),
            },
        )
        session.receipt_ids["step_1"] = receipt.receipt_id
        session.step_statuses["step_1"] = PipelineStepStatus.COMPLETE
        return receipt.receipt_id

    def _execute_step_2(
        self, session: VoiceDNAPipelineSession, parent_receipt_id: str
    ) -> str:
        """Step 2: Discourse Marker Census."""
        session.step_statuses["step_2"] = PipelineStepStatus.RUNNING
        assert session.corpus is not None, "Step 2 requires Step 1 corpus"

        marker_map = self.discourse_census.census(session.corpus)
        session.discourse_marker_map = marker_map

        receipt = self.receipt_chain.log(
            agent_id="Valeriane",
            action="DISCOURSE-MARKER-CENSUS",
            asset_id=f"discourse_marker_map_{self.coach_acronym}",
            input_summary=f"Corpus hash: {session.corpus.corpus_hash}",
            output_summary=(
                f"Markers found: {len(marker_map.markers)} "
                f"({', '.join(list(marker_map.markers.keys())[:5])}...)"
            ),
            decision="CENSUS_COMPLETE",
            parent_receipt_id=parent_receipt_id,
            metadata={"marker_count": len(marker_map.markers)},
        )
        session.receipt_ids["step_2"] = receipt.receipt_id
        session.step_statuses["step_2"] = PipelineStepStatus.COMPLETE
        return receipt.receipt_id

    def _execute_step_3(
        self, session: VoiceDNAPipelineSession, parent_receipt_id: str
    ) -> str:
        """Step 3: Cross-Topic Invariance Test."""
        session.step_statuses["step_3"] = PipelineStepStatus.RUNNING
        assert session.corpus is not None, "Step 3 requires Step 1 corpus"
        assert session.discourse_marker_map is not None, "Step 3 requires Step 2 marker map"

        invariance_result = self.invariance_test.test(session.corpus)
        session.invariance_result = invariance_result

        # Gate: ≥12 invariant markers
        if not invariance_result.passes_invariance_gate():
            session.step_statuses["step_3"] = PipelineStepStatus.HALTED
            raise VoiceDNAPipelineError(
                f"Invariance gate FAILED: {len(invariance_result.invariant_markers)} "
                f"invariant markers (minimum 12 required). "
                f"Topic-specific markers: {invariance_result.topic_specific_markers}. "
                f"Expand corpus (more Sacred Audio) or broaden subject clusters."
            )

        receipt = self.receipt_chain.log(
            agent_id="Valeriane",
            action="CROSS-TOPIC-INVARIANCE",
            asset_id=f"invariance_result_{self.coach_acronym}",
            input_summary=f"Discourse marker map ({len(session.discourse_marker_map.markers)} markers)",
            output_summary=(
                f"Invariant: {len(invariance_result.invariant_markers)}, "
                f"Topic-specific: {len(invariance_result.topic_specific_markers)}"
            ),
            decision="INVARIANCE_GATE_PASSED",
            parent_receipt_id=parent_receipt_id,
            metadata={
                "invariant_count": len(invariance_result.invariant_markers),
                "topic_specific_count": len(invariance_result.topic_specific_markers),
                "invariant_markers": invariance_result.invariant_markers,
            },
        )
        session.receipt_ids["step_3"] = receipt.receipt_id
        session.step_statuses["step_3"] = PipelineStepStatus.COMPLETE
        return receipt.receipt_id

    def _execute_step_4(
        self, session: VoiceDNAPipelineSession, parent_receipt_id: str
    ) -> str:
        """Step 4: Sentence Skeleton Extraction."""
        session.step_statuses["step_4"] = PipelineStepStatus.RUNNING
        assert session.corpus is not None, "Step 4 requires Step 1 corpus"
        assert session.invariance_result is not None, "Step 4 requires Step 3 invariance result"

        profile = self.skeleton_extractor.extract(
            corpus=session.corpus,
            invariant_markers=session.invariance_result.invariant_markers,
        )
        session.stylometry_profile = profile

        receipt = self.receipt_chain.log(
            agent_id="Valeriane",
            action="SENTENCE-SKELETON-EXTRACT",
            asset_id=f"stylometry_profile_{self.coach_acronym}",
            input_summary=f"Corpus hash: {session.corpus.corpus_hash}",
            output_summary=(
                f"Profile: TTR={profile.lexical.type_token_ratio:.3f}, "
                f"WPS_mean={profile.structural.wps_mean:.1f}, "
                f"hash={profile.profile_hash[:12]}"
            ),
            decision="STYLOMETRY_COMPLETE",
            parent_receipt_id=parent_receipt_id,
            metadata={"profile_hash": profile.profile_hash},
        )
        session.receipt_ids["step_4"] = receipt.receipt_id
        session.step_statuses["step_4"] = PipelineStepStatus.COMPLETE
        return receipt.receipt_id

    def _execute_step_5(
        self, session: VoiceDNAPipelineSession, parent_receipt_id: str
    ) -> str:
        """Step 5: Negative Space Excavation (Mandate 4 — First DEP).

        GATE: This step must complete and produce a validated DEP-ENG-004
        before subsequent steps can execute.
        """
        session.step_statuses["step_5"] = PipelineStepStatus.RUNNING
        assert session.corpus is not None, "Step 5 requires Step 1 corpus"
        assert session.stylometry_profile is not None, "Step 5 requires Step 4 stylometry"
        assert session.invariance_result is not None, "Step 5 requires Step 3 invariance"

        neg_space = self.negative_excavator.excavate(
            corpus=session.corpus,
            stylometry_profile=session.stylometry_profile,
            invariant_markers=session.invariance_result.invariant_markers,
        )
        session.negative_space = neg_space

        receipt = self.receipt_chain.log(
            agent_id="Valeriane",
            action="NEGATIVE-SPACE-EXCAVATION",
            asset_id=f"DEP-ENG-004_{self.coach_acronym}",
            input_summary=f"Corpus + stylometry profile",
            output_summary=(
                f"DEP-ENG-004: {neg_space.total_contrastive_strings()} contrastive strings "
                f"(academic: {len(neg_space.lexical_blacklist.academic)}, "
                f"spiritual: {len(neg_space.lexical_blacklist.spiritual)}, "
                f"intensifiers: {len(neg_space.lexical_blacklist.banned_intensifiers)}, "
                f"syntactic: {len(neg_space.syntactic_impossibilities)}, "
                f"structural: {len(neg_space.structural_exclusions.forbidden_openings) + len(neg_space.structural_exclusions.forbidden_closings)})"
            ),
            decision="DEP_ENG_004_PRODUCED",
            parent_receipt_id=parent_receipt_id,
            metadata={
                "dep_hash": neg_space.object_hash,
                "total_contrastive_strings": neg_space.total_contrastive_strings(),
            },
        )
        session.receipt_ids["step_5"] = receipt.receipt_id
        session.step_statuses["step_5"] = PipelineStepStatus.COMPLETE
        return receipt.receipt_id

    def _execute_steps_6_8(
        self, session: VoiceDNAPipelineSession, parent_receipt_id: str
    ) -> str:
        """Steps 6-8: Positive Space Extraction + Humor Classification.

        Prerequisite gate: DEP-ENG-004 must exist (Mandate 4 — hardcoded).
        """
        session.step_statuses["steps_6_8"] = PipelineStepStatus.RUNNING
        assert session.stylometry_profile is not None, "Steps 6-8 require Step 4 stylometry"
        assert session.negative_space is not None, "Steps 6-8 require Step 5 DEP-ENG-004 (Mandate 4)"
        assert session.corpus is not None, "Steps 6-8 require Step 1 corpus"

        positive_space, humor = self.positive_extractor.extract(
            stylometry_profile=session.stylometry_profile,
            negative_space=session.negative_space,  # Mandate 4 gate enforced inside
            corpus=session.corpus,
        )
        session.positive_space = positive_space
        session.humor_classification = humor

        receipt = self.receipt_chain.log(
            agent_id="Valeriane",
            action="POSITIVE-SPACE-EXTRACT",
            asset_id=f"DEP-ENG-003_{self.coach_acronym}",
            input_summary=f"Stylometry profile + DEP-ENG-004",
            output_summary=(
                f"DEP-ENG-003: {positive_space.total_variables} variables, "
                f"{len(positive_space.clusters)} clusters. "
                f"Humor: {humor.primary_style.value if humor else 'N/A'}"
            ),
            decision="DEP_ENG_003_PRODUCED",
            parent_receipt_id=parent_receipt_id,
            metadata={
                "dep_hash": positive_space.object_hash,
                "total_variables": positive_space.total_variables,
                "humor_style": humor.primary_style.value if humor else None,
            },
        )
        session.receipt_ids["steps_6_8"] = receipt.receipt_id
        session.step_statuses["steps_6_8"] = PipelineStepStatus.COMPLETE
        return receipt.receipt_id

    def _execute_step_9(
        self, session: VoiceDNAPipelineSession, parent_receipt_id: str
    ) -> str:
        """Step 9: Emotional DNA Integration Test (Mandate 7).

        Prerequisite gate: DEP-LIB-001 must exist from FR4.
        If absent → SKIP (not fail).
        """
        session.step_statuses["step_9"] = PipelineStepStatus.RUNNING
        assert session.positive_space is not None, "Step 9 requires Steps 6-8 DEP-ENG-003"
        assert session.negative_space is not None, "Step 9 requires Step 5 DEP-ENG-004"

        mandate7_result = self.emotional_dna_test.test(
            positive_space=session.positive_space,
            negative_space=session.negative_space,
        )
        session.mandate7_result = mandate7_result

        if mandate7_result.skipped:
            decision = "STEP_9_SKIPPED_DEP_LIB_001_ABSENT"
            session.step_statuses["step_9"] = PipelineStepStatus.SKIPPED
        elif mandate7_result.passed:
            decision = "MANDATE_7_PASSED"
            session.step_statuses["step_9"] = PipelineStepStatus.COMPLETE
        else:
            decision = "MANDATE_7_FAILED_OPERATOR_REVIEW"
            session.step_statuses["step_9"] = PipelineStepStatus.COMPLETE
            # Note: Mandate 7 failure does NOT halt the pipeline per spec.
            # It flags for operator review but adversarial validation continues.

        receipt = self.receipt_chain.log(
            agent_id="Charlotte" if not mandate7_result.skipped else "Valeriane",
            action="EMOTIONAL-DNA-TEST",
            asset_id=f"mandate7_result_{self.coach_acronym}",
            input_summary=f"DEP-ENG-003 + DEP-ENG-004 + DEP-LIB-001",
            output_summary=(
                f"Mandate 7: {'SKIPPED' if mandate7_result.skipped else 'PASSED' if mandate7_result.passed else 'FAILED'}, "
                f"cycles: {mandate7_result.cycles_used}"
            ),
            decision=decision,
            parent_receipt_id=parent_receipt_id,
            metadata={
                "passed": mandate7_result.passed,
                "skipped": mandate7_result.skipped,
                "cycles_used": mandate7_result.cycles_used,
            },
        )
        session.receipt_ids["step_9"] = receipt.receipt_id
        return receipt.receipt_id

    def _execute_step_10(
        self, session: VoiceDNAPipelineSession, parent_receipt_id: str
    ) -> str:
        """Step 10: Adversarial Validation (with rewind loop).

        Spec §Step 10: 'Maximum 3 rewind cycles. After 3 cycles without
        passing → operator review required.'
        """
        session.step_statuses["step_10"] = PipelineStepStatus.RUNNING
        assert session.corpus is not None, "Step 10 requires Step 1 corpus"
        assert session.positive_space is not None, "Step 10 requires Steps 6-8 DEP-ENG-003"
        assert session.negative_space is not None, "Step 10 requires Step 5 DEP-ENG-004"

        baseline_hash = session.corpus.corpus_hash

        for rewind in range(MAX_ADVERSARIAL_REWIND_CYCLES + 1):
            validation = self.adversarial_validator.validate(
                positive_space=session.positive_space,
                negative_space=session.negative_space,
                ttt_baseline_hash=baseline_hash,
            )
            validation.rewind_cycles_used = rewind

            if validation.passed:
                session.adversarial_result = validation
                break

            # Rewind: add flagged structures to Negative Space
            if rewind < MAX_ADVERSARIAL_REWIND_CYCLES:
                for structure in validation.structures_added_to_negative_space:
                    self.negative_excavator.add_flagged_structure(
                        session.negative_space, structure
                    )
            else:
                # Max rewinds exhausted
                session.adversarial_result = validation
                break

        assert session.adversarial_result is not None, "Adversarial validation must produce a result"
        adv = session.adversarial_result

        receipt = self.receipt_chain.log(
            agent_id="Adversarial Validator",
            action="ADVERSARIAL-VALIDATION",
            asset_id=f"ttt_baseline_{self.coach_acronym}",
            input_summary=f"5 adversarial samples against DEP-ENG-003 + DEP-ENG-004",
            output_summary=(
                f"{'PASSED' if adv.passed else 'FAILED'}: "
                f"TTT drift={adv.max_ttt_drift_pct:.1f}%, "
                f"AI={adv.max_ai_detection_pct:.1f}%, "
                f"Boredom={adv.max_boredom_cosine:.3f}, "
                f"rewinds={adv.rewind_cycles_used}"
            ),
            decision=(
                "ADVERSARIAL_PASSED"
                if adv.passed
                else "ADVERSARIAL_FAILED_OPERATOR_REVIEW"
            ),
            parent_receipt_id=parent_receipt_id,
            metadata={
                "passed": adv.passed,
                "ttt_baseline_hash": adv.ttt_baseline_hash,
                "rewind_cycles": adv.rewind_cycles_used,
            },
        )
        session.receipt_ids["step_10"] = receipt.receipt_id
        session.step_statuses["step_10"] = PipelineStepStatus.COMPLETE
        return receipt.receipt_id

    # ──────────────────────────────────────────────────────────
    # Final Output Writing
    # ──────────────────────────────────────────────────────────

    def _write_final_outputs(self, session: VoiceDNAPipelineSession) -> None:
        """Write DEP-ENG-003 + DEP-ENG-004 + ttt_baseline.json to coach_soul.json.

        Spec §Step 10: 'Write DEP-ENG-003 + DEP-ENG-004 + ttt_baseline.json
        to coach_soul.json and Supabase.'
        """
        config_dir = self.coach_dir / "config"
        config_dir.mkdir(parents=True, exist_ok=True)

        neg_space = session.negative_space
        pos_space = session.positive_space
        if neg_space is None or pos_space is None:
            raise RuntimeError("Final output requires DEP-ENG-003 and DEP-ENG-004")

        # Write DEP-ENG-004
        dep_004_path = config_dir / "dep_eng_004.json"
        dep_004_path.write_text(
            neg_space.model_dump_json(indent=2),
            encoding="utf-8",
        )
        session.dep_eng_004_written = True

        # Write DEP-ENG-003
        dep_003_path = config_dir / "dep_eng_003.json"
        dep_003_path.write_text(
            pos_space.model_dump_json(indent=2),
            encoding="utf-8",
        )
        session.dep_eng_003_written = True

        # Write ttt_baseline.json
        if session.adversarial_result and session.adversarial_result.passed:
            ttt_path = config_dir / "ttt_baseline.json"
            ttt_data = {
                "baseline_hash": session.adversarial_result.ttt_baseline_hash,
                "sample_count": len(session.adversarial_result.samples),
                "max_ttt_drift_pct": session.adversarial_result.max_ttt_drift_pct,
                "max_ai_detection_pct": session.adversarial_result.max_ai_detection_pct,
                "max_boredom_cosine": session.adversarial_result.max_boredom_cosine,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            ttt_path.write_text(
                json.dumps(ttt_data, indent=2),
                encoding="utf-8",
            )
            session.ttt_baseline_written = True

        # Write humor classification
        if session.humor_classification:
            humor_path = config_dir / "humor_style_classification.json"
            humor_path.write_text(
                session.humor_classification.model_dump_json(indent=2),
                encoding="utf-8",
            )

    # ──────────────────────────────────────────────────────────
    # V5.0 Extension Triggers
    # ──────────────────────────────────────────────────────────

    def _trigger_v50_extensions(
        self, session: VoiceDNAPipelineSession
    ) -> None:
        """Trigger V5.0 post-Step-10 onboarding chain.

        Spec §V5.0 Extension: 'When Step 12 passes, the extraction pipeline
        has completed. The V5.0 onboarding prerequisites (§12.3) now proceed.'

        Steps 0-A through 0-D are triggered within the same execution cycle.
        """
        if not session.is_complete():
            return

        v50 = session.v50_status

        # Step 0-A: CMM Extraction trigger
        v50.step_0a_cmm_triggered = True

        # Step 0-B: Story Archive Seeding trigger
        v50.step_0b_story_archive_triggered = True

        # Step 0-C: Humor Mechanism Registry creation
        v50.step_0c_humor_registry_created = True

        # Step 0-D: Context Performance Registry creation
        v50.step_0d_context_performance_created = True

        # Log V5.0 trigger receipt
        self.receipt_chain.log(
            agent_id="Morgan",
            action="V50-EXTENSION-TRIGGERS",
            asset_id=f"v50_triggers_{self.coach_acronym}",
            input_summary="FR3 pipeline completed",
            output_summary=(
                f"V5.0 triggers: CMM={v50.step_0a_cmm_triggered}, "
                f"StoryArchive={v50.step_0b_story_archive_triggered}, "
                f"HumorRegistry={v50.step_0c_humor_registry_created}, "
                f"ContextPerf={v50.step_0d_context_performance_created}"
            ),
            decision="V50_CHAIN_TRIGGERED",
        )
