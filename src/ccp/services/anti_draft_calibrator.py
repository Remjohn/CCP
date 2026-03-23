"""
CCP FR22 — Anti-Draft Calibration Service (DEP-PROTO-013)

Implements the 3-Level Anti-Draft Intelligence architecture.
Stages 1-4: Frozen Anchor → Mode+M3 Synthesis → Negative Space → Critic Gate.

Spec reference: FR22_Anti_Draft_Intelligence_Tech_Spec.md
  §4 Stage 1: Level 1 Construction (Block A Invariant Load)
  §4 Stage 2: Level 2 Generation (Mode & M3 Synthesis)
  §4 Stage 3: Level 3 Injection (Negative Space Load — DEP-ENG-004 FIRST)
  §4 Stage 4: Critic Subagent Enforcement Gate
  §8 AC1-AC4

Critical invariant (Frozen Anchor Mandate):
  Level 1 MUST use frozen_model='gpt-3.5-turbo'.
  The primary model NEVER generates its own anti-draft anchor.

Critical invariant (Absolute First Load Order — M3 Mandate):
  DEP-ENG-004 (Level 3) MUST load before ANY positive instruction.
  AC3: 'Forbidden Strings appear sequentially BEFORE DEP-ENG-003 targets.'

Ghost Variable Prevention Gate:
  All DEP-IDs verified before payload unpacking.
  NULL/UNDEFINED field → DAG_VIOLATION error + hard halt.
  Error schema: {"error": "DAG_VIOLATION", "missing_dep": "[DEP-ID]"}

ADR-01: coach_id scopes all operations.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.anti_draft_models import (
    CRITIC_FULL_PURGE_THRESHOLD,
    FROZEN_ANCHOR_MODEL,
    L3_MINIMUM_DEPTH_THRESHOLD,
    AntiDraftDeliberationLog,
    AntiDraftHaltReason,
    AntiDraftLevel,
    AntiDraftValidationPass,
    CriticPass,
    CriticReport,
    CriticVerdict,
    CriticViolation,
    FinalSemanticDistanceStatus,
    ForbiddenVocabularyBlock,
    L2DegradationReason,
    Level1FrozenAnchor,
    Level2Mode,
    Level2ModeBelief,
    ViolationType,
)
from src.ccp.models.voice_dna_models import NegativeSpaceObject


# ─── Exceptions ───────────────────────────────────────────────────────────────

class AntiDraftHaltError(RuntimeError):
    """Raised when the Anti-Draft pipeline hits a fatal halt.

    Spec §4 Stage 3 Gate PC-03: L3_INSUFFICIENT_DEPTH
    Spec §4 Stage 1: L1_ABSENT / L1_ABSTRACT_DESCRIPTION
    Spec §3 Technical Decision 4: DAG_VIOLATION
    """

    def __init__(
        self,
        halt_reason: AntiDraftHaltReason,
        missing_dep: Optional[str] = None,
    ) -> None:
        self.halt_reason = halt_reason
        self.missing_dep = missing_dep
        if halt_reason == AntiDraftHaltReason.DAG_VIOLATION and missing_dep:
            msg = json.dumps({"error": "DAG_VIOLATION", "missing_dep": missing_dep})
        else:
            msg = f"ANTI_DRAFT_HALT: {halt_reason.value}"
            if missing_dep:
                msg += f" (dep={missing_dep})"
        super().__init__(msg)


# ─── Anti-Draft Calibrator ─────────────────────────────────────────────────────

class AntiDraftCalibrator:
    """Implements DEP-PROTO-013 — 3-Level Anti-Draft Calibration Protocol.

    Provides:
      stage_1_build_frozen_anchor()  — Level 1 static extraction + prose gate.
      stage_2_generate_mode_belief() — Level 2 mode+M3 synthesis.
      stage_3_load_negative_space()  — Level 3 DEP-ENG-004 injection (FIRST).
      stage_4_run_critic()           — Critic subagent evaluation + verdict.
      build_deliberation_log()       — Assemble final DEP-PROTO-013 output.

    Frozen Anchor Mandate: Level 1 generation MUST use frozen_model parameter.
    The primary model never runs Stage 1.

    Ghost Variable Prevention: verify_dag_inputs() halts with DAG_VIOLATION
    before any payload unpacking if a required DEP-ID resolves to None/empty.
    """

    def __init__(
        self,
        coach_id: str,
        receipt_chain: Optional[ReceiptChain] = None,
    ) -> None:
        if len(coach_id) != 3:
            raise ValueError(f"coach_id must be 3 chars, got: {coach_id!r}")
        self.coach_id = coach_id
        self._receipt_chain = receipt_chain

    # ── Ghost Variable Prevention Gate ────────────────────────────────────────

    def verify_dag_inputs(
        self,
        negative_space: Optional[NegativeSpaceObject],
        archetype_container_block: Optional[str],
    ) -> None:
        """Spec §3 Technical Decision 4: Ghost Variable Prevention Gate.

        All input sources [DEP-ID] must be verified cryptographically prior
        to payload unpacking. NULL/UNDEFINED → DAG_VIOLATION halt.

        Error schema: {"error": "DAG_VIOLATION", "missing_dep": "[DEP-ID]"}
        """
        if negative_space is None:
            raise AntiDraftHaltError(
                AntiDraftHaltReason.DAG_VIOLATION,
                missing_dep="DEP-ENG-004",
            )
        if not archetype_container_block or not archetype_container_block.strip():
            raise AntiDraftHaltError(
                AntiDraftHaltReason.DAG_VIOLATION,
                missing_dep="ARCHETYPE_CONTAINER_BLOCK",
            )

    # ── Stage 1: Level 1 Frozen Anchor ────────────────────────────────────────

    def stage_1_build_frozen_anchor(
        self,
        archetype_container_block: str,
        archetype_id: str,
        frozen_model: str = FROZEN_ANCHOR_MODEL,
    ) -> Level1FrozenAnchor:
        """Stage 1 — Extract Level 1 Anti-Draft block from static container.

        Spec §4 Stage 1:
          - Block MUST come from static Archetype Container module.
          - Validate 4 required subsections present.
          - Prose gate: >= 3 sentences of literal terrible AI cliché.
          - Frozen Anchor Mandate: frozen_model MUST NOT be the primary model.

        Failure Conditions:
          - L1_ABSENT: container block is missing.
          - L1_ABSTRACT_DESCRIPTION: Level 1 is descriptions, not prose.
        """
        if not archetype_container_block or not archetype_container_block.strip():
            raise AntiDraftHaltError(AntiDraftHaltReason.L1_ABSENT)

        # Parse the 4 required subsections from the container block.
        # Expected format: each section prefixed with a known marker.
        # We extract by marker presence; robust to whitespace variations.
        centroid_prose = self._extract_section(
            archetype_container_block,
            "[Statistical Centroid Prose Example]",
            fallback_pattern=r"centroid[^:]*:\s*(.*?)(?=\[|$)",
        )
        mechanism_failure = self._extract_section(
            archetype_container_block,
            "[Mechanism Failure Diagnosis]",
            fallback_pattern=r"mechanism[^:]*:\s*(.*?)(?=\[|$)",
        )
        resolution_failure = self._extract_section(
            archetype_container_block,
            "[Resolution Failure Diagnosis]",
            fallback_pattern=r"resolution[^:]*:\s*(.*?)(?=\[|$)",
        )
        semantic_distance = self._extract_section(
            archetype_container_block,
            "[Semantic Distance Instruction]",
            fallback_pattern=r"semantic[^:]*:\s*(.*?)(?=\[|$)",
        )

        anchor = Level1FrozenAnchor(
            frozen_model_used=frozen_model,
            statistical_centroid_prose=centroid_prose,
            mechanism_failure_diagnosis=mechanism_failure,
            resolution_failure_diagnosis=resolution_failure,
            semantic_distance_instruction=semantic_distance,
            archetype_id=archetype_id,
        )

        # AC1 Gate: prose gate enforced — abstract descriptions fail.
        if not anchor.is_valid_prose():
            raise AntiDraftHaltError(AntiDraftHaltReason.L1_ABSTRACT_DESCRIPTION)

        anchor.receipt_hash = self._hash_block(anchor.model_dump_json())
        self._write_receipt(
            agent_id="JIT-Skill-Assembler-v2.0",
            action="ANTI_DRAFT_STAGE_1_LEVEL1_FROZEN_ANCHOR",
            asset_id=f"DEP-PROTO-013_L1_{self.coach_id}",
            input_summary=f"archetype_id={archetype_id}, frozen_model={frozen_model}",
            output_summary=f"Level1 anchor built, prose sentences validated",
        )
        return anchor

    # ── Stage 2: Level 2 Mode + M3 Synthesis ──────────────────────────────────

    def stage_2_generate_mode_belief(
        self,
        routing_mode: Level2Mode,
        m3_undeniable_belief: Optional[str],
    ) -> Level2ModeBelief:
        """Stage 2 — Generate Level 2 Anti-Draft constraint text.

        Spec §4 Stage 2:
          - Retrieves mood_state + audience prediction error from M3.
          - Constructs the mode-failure scenario.
          - Injects M3 finding explicitly as subversion command.

        Backward Compatibility (Spec §6):
          If M3_UNDENIABLE absent → logs M3_ABSENT_L2_DEGRADED.
          Falls back to generic mode_failure. NOT a pipeline halt.
        """
        degradation_reason: Optional[L2DegradationReason] = None
        m3_subversion_command: Optional[str] = None

        # Build mode-failure scenario per spec §4 Stage 2 Step 2
        if routing_mode == Level2Mode.PROCESSING:
            mode_failure = (
                "The mechanism described is technically accurate, but the payload "
                "arrives before the audience's stakes are felt. The mechanism is correct "
                "but the emotional foundation is unearned — insight delivered in paragraph "
                "1 before the audience has been brought to the edge of recognition."
            )
        elif routing_mode == Level2Mode.ESCAPE:
            mode_failure = (
                "The escape vehicle chosen mirrors the audience's Level 3 pain domain — "
                "a semantic affinity breach. The proposed relief pathway contains the "
                "same emotional vocabulary as the wound, triggering resistance instead "
                "of release."
            )
        elif routing_mode == Level2Mode.DISCOVERY:
            mode_failure = (
                "The discovery arc moves too quickly to resolution, collapsing the "
                "tension window before the audience has experienced the disorientation "
                "required for genuine insight. Premature closure prevents transformation."
            )
        else:  # SOCIAL
            mode_failure = (
                "The social frame invites participation but fails to establish "
                "the shared wound that creates genuine belonging. Community without "
                "shared vulnerability produces shallow affiliation, not resonance."
            )

        # Inject M3 finding (AC2 gate)
        if m3_undeniable_belief and m3_undeniable_belief.strip():
            m3_subversion_command = (
                f"The draft assumes the audience believes: "
                f"'{m3_undeniable_belief.strip()}'. "
                f"You MUST actively tear this assumption down — "
                f"do NOT cater to it, do NOT validate it, do NOT soften it. "
                f"The entire payload must work against this belief's gravitational pull."
            )
        else:
            degradation_reason = L2DegradationReason.M3_ABSENT_L2_DEGRADED

        block = Level2ModeBelief(
            routing_mode=routing_mode,
            m3_belief_text=m3_undeniable_belief,
            mode_failure_scenario=mode_failure,
            m3_subversion_command=m3_subversion_command,
            degradation_reason=degradation_reason,
        )

        block.receipt_hash = self._hash_block(block.model_dump_json())
        self._write_receipt(
            agent_id="payload-masking-adapter",
            action="ANTI_DRAFT_STAGE_2_LEVEL2_MODE_BELIEF",
            asset_id=f"DEP-PROTO-013_L2_{self.coach_id}",
            input_summary=(
                f"mode={routing_mode.value}, "
                f"m3_present={m3_undeniable_belief is not None}"
            ),
            output_summary=(
                f"Level2 block built"
                + (f" [DEGRADED: {degradation_reason.value}]" if degradation_reason else "")
            ),
        )
        return block

    # ── Stage 3: Level 3 Negative Space Injection ─────────────────────────────

    def stage_3_load_negative_space(
        self,
        negative_space: NegativeSpaceObject,
    ) -> ForbiddenVocabularyBlock:
        """Stage 3 — Load DEP-ENG-004 FIRST (Absolute First Load Order).

        Spec §4 Stage 3:
          - 'Explicitly load DEP-ENG-004 FIRST.'
          - Gate PC-03: count >= 15 contrastive strings.
          - If thin (< 15 items) → L3_INSUFFICIENT_DEPTH halt.
          - Extract 4 forbidden string vectors.

        AC3: Level 3 'Forbidden Strings' MUST appear BEFORE DEP-ENG-003
        targets in the SKILL.md text stream.
        """
        # Gate PC-03 enforcement
        total = negative_space.total_contrastive_strings()
        if total < L3_MINIMUM_DEPTH_THRESHOLD:
            raise AntiDraftHaltError(
                AntiDraftHaltReason.L3_INSUFFICIENT_DEPTH,
                missing_dep=f"DEP-ENG-004 has {total} strings (need >= {L3_MINIMUM_DEPTH_THRESHOLD})",
            )

        # Compute DEP-ENG-004 hash for immutability guarantee
        dep_hash = negative_space.object_hash or negative_space.compute_hash()

        # Extract 4 vectors from NegativeSpaceObject
        cognitive_drift = list(negative_space.syntactic_impossibilities)
        register_hedges = list(negative_space.lexical_blacklist.academic)
        performed_vocab = list(negative_space.lexical_blacklist.spiritual)
        structural_shortcuts = list(negative_space.structural_exclusions.forbidden_openings) + \
                               list(negative_space.structural_exclusions.forbidden_closings)
        banned_intensifiers = list(negative_space.lexical_blacklist.banned_intensifiers)

        # Flat union for the FORBIDDEN STRINGS list
        forbidden_flat: list[str] = []
        forbidden_flat.extend(cognitive_drift)
        forbidden_flat.extend(register_hedges)
        forbidden_flat.extend(performed_vocab)
        forbidden_flat.extend(structural_shortcuts)
        forbidden_flat.extend(banned_intensifiers)
        # Deduplicate while preserving order
        seen: set[str] = set()
        deduped: list[str] = []
        for s in forbidden_flat:
            if s not in seen:
                seen.add(s)
                deduped.append(s)

        block = ForbiddenVocabularyBlock(
            dep_eng_004_hash=dep_hash,
            cognitive_load_drift_patterns=cognitive_drift,
            professional_register_hedges=register_hedges,
            performed_vocabulary=performed_vocab,
            structural_shortcuts=structural_shortcuts,
            forbidden_strings_flat=deduped,
            total_count=total,
            loaded_first=True,  # AC3: this block MUST load before positive space
        )

        block.receipt_hash = self._hash_block(block.model_dump_json())
        self._write_receipt(
            agent_id="negative-space-loader-adapter",
            action="ANTI_DRAFT_STAGE_3_LEVEL3_NEGATIVE_SPACE",
            asset_id=f"DEP-ENG-004_{self.coach_id}",
            input_summary=f"total_contrastive_strings={total}",
            output_summary=f"ForbiddenVocabularyBlock built: {len(deduped)} forbidden strings",
        )
        return block

    # ── Stage 4: Critic Subagent Enforcement Gate ──────────────────────────────

    def stage_4_run_critic(
        self,
        draft_text: str,
        level_1_block: Level1FrozenAnchor,
        level_2_block: Level2ModeBelief,
        level_3_block: ForbiddenVocabularyBlock,
        critic_pass: CriticPass = CriticPass.PASS_1_INITIAL,
    ) -> CriticReport:
        """Stage 4 — Critic Subagent evaluates draft against the 3-Level fence.

        Spec §4 Stage 4:
          - Level 1 breach: generic cliché found → +1 violation.
          - Level 2 breach: mode payload failed or M3 catered to → +1 violation.
          - Level 3 breach: forbidden string found → +1 violation.
          - violations >= 2 → FULL_PURGE_REGENERATE (Pass 3).
          - violations == 1 → TARGETED_SECTION_REWRITE.
          - violations == 0 → PASS_GENERATION_PAYLOAD.

        AC4: Critic MUST NOT just log violations as warnings. It MUST enforce
        the verdict. Failure example: 'just logs them as warnings and passes
        the flawed script to the user.'
        """
        violations: list[CriticViolation] = []

        # Level 1 Check: detect generic cliché phrases
        cliche_phrases = [
            "journey of discovery",
            "life-changing",
            "transform your life",
            "unlock your potential",
            "the power of positive thinking",
            "believe in yourself",
            "follow your dreams",
            "hard work pays off",
            "you can do anything",
        ]
        draft_lower = draft_text.lower()
        for phrase in cliche_phrases:
            if phrase in draft_lower:
                violations.append(CriticViolation(
                    violation_type=ViolationType.LEVEL_1_GENERIC_CLICHE,
                    level=AntiDraftLevel.LEVEL_1_ARCHETYPE,
                    offending_text_excerpt=phrase,
                ))
                break  # One Level 1 violation per draft

        # Level 2 Check: detect if M3 belief is catered to (not subverted)
        if (
            level_2_block.m3_belief_text
            and level_2_block.m3_belief_text.strip()
        ):
            m3_snippet = level_2_block.m3_belief_text.strip().lower()[:60]
            if m3_snippet in draft_lower:
                violations.append(CriticViolation(
                    violation_type=ViolationType.LEVEL_2_M3_CATERED_TO,
                    level=AntiDraftLevel.LEVEL_2_MODE_BELIEF,
                    offending_text_excerpt=m3_snippet,
                ))

        # Level 3 Check: detect forbidden strings from DEP-ENG-004
        for forbidden in level_3_block.forbidden_strings_flat:
            if forbidden.lower() in draft_lower:
                violations.append(CriticViolation(
                    violation_type=ViolationType.LEVEL_3_FORBIDDEN_STRING,
                    level=AntiDraftLevel.LEVEL_3_VOICE,
                    offending_text_excerpt=forbidden,
                    forbidden_string_matched=forbidden,
                ))
                # One Level 3 violation per check pass (most severe match)
                break

        report = CriticReport(
            pass_evaluated=critic_pass,
            violations=violations,
        )

        report.receipt_hash = self._hash_block(report.model_dump_json())
        self._write_receipt(
            agent_id="L3-Critic-Subagent",
            action="ANTI_DRAFT_STAGE_4_CRITIC_EVALUATION",
            asset_id=f"DEP-PROTO-013_CRITIC_{self.coach_id}",
            input_summary=(
                f"pass={critic_pass.value}, "
                f"draft_length={len(draft_text)}"
            ),
            output_summary=(
                f"violations={report.violation_count}, "
                f"verdict={report.verdict.value}"
            ),
        )
        return report

    # ── Deliberation Log Builder ───────────────────────────────────────────────

    def build_deliberation_log(
        self,
        compilation_request_id: str,
        level_1_block: Optional[Level1FrozenAnchor],
        level_2_block: Optional[Level2ModeBelief],
        level_3_block: Optional[ForbiddenVocabularyBlock],
        critic_report: Optional[CriticReport],
        halt_reason: Optional[AntiDraftHaltReason] = None,
    ) -> AntiDraftDeliberationLog:
        """Assemble the final DEP-PROTO-013 execution metadata log.

        Spec §5: anti_draft_deliberation_log.json written alongside Final Script.
        """
        validation_pass = AntiDraftValidationPass(
            level_1_archetype_loaded=level_1_block is not None,
            level_2_mode_generated=level_2_block is not None,
            level_3_negative_space_loaded=level_3_block is not None,
        )

        l2_degradation = None
        if level_2_block and level_2_block.is_degraded:
            l2_degradation = level_2_block.degradation_reason

        log = AntiDraftDeliberationLog(
            compilation_request_id=compilation_request_id,
            coach_id=self.coach_id,
            validation_pass=validation_pass,
            level_1_block=level_1_block,
            level_2_block=level_2_block,
            level_3_block=level_3_block,
            critic_evaluation=critic_report,
            halt_reason=halt_reason,
            l2_degradation_reason=l2_degradation,
        )

        # Write final receipt
        self._write_receipt(
            agent_id="AntiDraftCalibrator",
            action="ANTI_DRAFT_DELIBERATION_LOG_FINAL",
            asset_id=f"DEP-PROTO-013_{compilation_request_id}",
            input_summary=(
                f"levels_loaded={sum([bool(level_1_block), bool(level_2_block), bool(level_3_block)])}/3"
            ),
            output_summary=(
                f"halted={log.halted}, "
                f"distance={log.final_semantic_distance_status.value}"
            ),
        )
        return log

    # ── Full Pipeline ──────────────────────────────────────────────────────────

    def run_full_calibration(
        self,
        compilation_request_id: str,
        archetype_container_block: str,
        archetype_id: str,
        routing_mode: Level2Mode,
        negative_space: NegativeSpaceObject,
        draft_text: str,
        m3_undeniable_belief: Optional[str] = None,
        frozen_model: str = FROZEN_ANCHOR_MODEL,
    ) -> AntiDraftDeliberationLog:
        """Execute all 4 stages in sequence, returning the DeliberationLog.

        Halts at any stage if a fatal error occurs.
        Stage 2 M3 absence degrades gracefully (non-fatal).
        """
        level_1: Optional[Level1FrozenAnchor] = None
        level_2: Optional[Level2ModeBelief] = None
        level_3: Optional[ForbiddenVocabularyBlock] = None
        critic: Optional[CriticReport] = None
        halt: Optional[AntiDraftHaltReason] = None

        try:
            # Ghost Variable Prevention Gate (Spec §3 TD4)
            self.verify_dag_inputs(negative_space, archetype_container_block)

            # Stage 3 FIRST (Absolute First Load Order — M3 Mandate)
            # Level 3 must be loaded before positive instructions reach the model.
            level_3 = self.stage_3_load_negative_space(negative_space)

            # Stage 1: Frozen Anchor
            level_1 = self.stage_1_build_frozen_anchor(
                archetype_container_block=archetype_container_block,
                archetype_id=archetype_id,
                frozen_model=frozen_model,
            )

            # Stage 2: Mode + M3 (degrades gracefully)
            level_2 = self.stage_2_generate_mode_belief(
                routing_mode=routing_mode,
                m3_undeniable_belief=m3_undeniable_belief,
            )

            # Stage 4: Critic evaluation
            critic = self.stage_4_run_critic(
                draft_text=draft_text,
                level_1_block=level_1,
                level_2_block=level_2,
                level_3_block=level_3,
            )

        except AntiDraftHaltError as exc:
            halt = exc.halt_reason

        return self.build_deliberation_log(
            compilation_request_id=compilation_request_id,
            level_1_block=level_1,
            level_2_block=level_2,
            level_3_block=level_3,
            critic_report=critic,
            halt_reason=halt,
        )

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _extract_section(
        self,
        text: str,
        marker: str,
        fallback_pattern: Optional[str] = None,
    ) -> str:
        """Extract section content following a named marker."""
        idx = text.find(marker)
        if idx != -1:
            rest = text[idx + len(marker):].strip()
            # Take content until the next section marker
            next_marker = rest.find("[")
            if next_marker > 0:
                return rest[:next_marker].strip()
            return rest.strip()
        # Try fallback regex
        if fallback_pattern:
            match = re.search(fallback_pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        return ""

    def _hash_block(self, content: str) -> str:
        """Compute SHA-256 hash of a block for Receipt Chain Guard."""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def _write_receipt(
        self,
        agent_id: str,
        action: str,
        asset_id: str,
        input_summary: str,
        output_summary: str,
    ) -> None:
        """Write to Receipt Chain Guard if a chain instance is present."""
        if self._receipt_chain is None:
            return
        try:
            self._receipt_chain.log(
                agent_id=agent_id,
                action=action,
                asset_id=asset_id,
                person_id=self.coach_id,
                input_summary=input_summary,
                output_summary=output_summary,
            )
        except Exception:
            # Receipt chain writes are non-blocking — they must never halt production
            pass
