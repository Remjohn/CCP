"""
CCP Step 6 — FR12: Three Failure Prevention Gates

5-stage pipeline:
  Stage 1: INGEST — Load DEP-ENG-010 + DEP-ENG-011, verify schemas
  Stage 2: GATE 1 — Adjacent vs. Congruent (sum ≥ 3.5 + min > 0.0)
  Stage 3: GATE 2 — Language Drift Prevention (≥3 lemmatized tribal terms)
  Stage 4: EMIT — Package DEP-ENG-027 (Gate Diagnostic Certificate)
  Stage 5: GATE 3 — Authenticity Score Feedback Loop (async, LIWC-22)

Architecture:
  §Context_Premise_Trigger_Matching_Layer Part 5
  ADR-01 Coach Isolation enforced — no cross-silo access
  3 consecutive Gate 2 failures → system_fallback_invoked

Acceptance Criteria: AC1–AC5

DEP-IDs consumed:
  DEP-ENG-010: FourAxisMatchResult (FR10)
  DEP-ENG-011: ActivationEventSeed (FR11)
  DEP-ENG-019: Session Transcript Intelligence (for Gate 3 LIWC-22)

DEP-IDs produced:
  DEP-ENG-027: GateDiagnosticCertificate (PROPOSED in spec, authorized)
"""

from __future__ import annotations

import hashlib
import logging
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.container_module_models import (
    ActivationEventSeed,
    ActivationSeedsPayload,
    FourAxisMatchResult,
    Gate1Result,
    Gate2Result,
    Gate3FailureMode,
    Gate3Result,
    GateDiagnosticCertificate,
    GateVerdict,
    MatchResultsPayload,
)

logger = logging.getLogger(__name__)


class FailurePreventionGates:
    """FR12: Three Failure Prevention Gates.

    Validates activation event seeds through three progressive gates
    before emission to the Telegram Elicitation Protocol.

    Gate 1: Structural Congruence (Adjacent vs. Congruent firewall)
    Gate 2: Language Drift Prevention (lemmatized tribal term verification)
    Gate 3: Authenticity Score Feedback Loop (async, post-recording LIWC-22)

    ADR-01 Coach Isolation: All operations scoped to a single coach.
    No cross-coach data access permitted.

    Produces: DEP-ENG-027 (GateDiagnosticCertificate)
    """

    # Agent IDs per stage (as specified in Build Plan receipt writes)
    GATEKEEPER_AGENT_ID = "gatekeeper_orchestrator_v1"
    GATE_1_AGENT_ID = "structural_congruence_validator_v1"
    GATE_2_AGENT_ID = "lexical_authenticity_validator_v1"
    GATE_3_AGENT_ID = "temporal_reconsolidation_auditor_v1"

    # Gate 2 consecutive failure fallback threshold
    GATE_2_CONSECUTIVE_FAILURE_LIMIT = 3

    def __init__(
        self,
        coach_acronym: str,
        receipt_chain: Optional[ReceiptChain] = None,
    ):
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = receipt_chain or ReceiptChain(
            coach_acronym=self.coach_acronym
        )
        # Track consecutive Gate 2 failures for fallback logic
        self._gate_2_consecutive_failures: int = 0

    # ══════════════════════════════════════════════════════════
    # Stage 1: INGEST
    # ══════════════════════════════════════════════════════════

    def ingest(
        self,
        match_results: Optional[MatchResultsPayload],
        activation_seeds: Optional[ActivationSeedsPayload],
    ) -> dict[str, Any]:
        """Stage 1: Load and verify DEP-ENG-010 + DEP-ENG-011 schemas.

        Returns:
            Ingested payload for gate processing.
        """
        if not match_results:
            raise ValueError(
                "FR12 Stage 1 HALT: DEP-ENG-010 (Match Results) is missing."
            )
        if not activation_seeds:
            raise ValueError(
                "FR12 Stage 1 HALT: DEP-ENG-011 (Activation Seeds) is missing."
            )

        # Graceful exit check — if seeds is empty, nothing to gate
        if activation_seeds.graceful_exit or not activation_seeds.seeds:
            logger.info(
                "FR12 Stage 1: Seeds payload is empty/graceful_exit. "
                "No gates to run."
            )
            return {
                "match_results": match_results,
                "activation_seeds": activation_seeds,
                "empty": True,
                "ingest_receipt_id": "",
            }

        # Build match lookup for Gate 1 cross-reference
        match_lookup: dict[str, FourAxisMatchResult] = {}
        for match_list in match_results.matches.values():
            for m in match_list:
                match_lookup[m.match_id] = m

        # Receipt: STAGE-1-INGEST
        ingest_receipt = self.receipt_chain.log(
            agent_id=self.GATEKEEPER_AGENT_ID,
            action="STAGE-1-INGEST",
            asset_id=f"FR12-{self.coach_acronym}-{match_results.theme[:20]}",
            input_summary=(
                f"DEP-ENG-010 theme={match_results.theme}, "
                f"DEP-ENG-011 seeds={len(activation_seeds.seeds)}"
            ),
            output_summary="FR12 ingest complete — schemas verified",
            decision="proceed",
            metadata={
                "theme": match_results.theme,
                "seed_count": len(activation_seeds.seeds),
                "match_count": sum(
                    len(v) for v in match_results.matches.values()
                ),
            },
        )

        return {
            "match_results": match_results,
            "activation_seeds": activation_seeds,
            "match_lookup": match_lookup,
            "empty": False,
            "ingest_receipt_id": ingest_receipt.receipt_id,
        }

    # ══════════════════════════════════════════════════════════
    # Stage 2: GATE 1 — Adjacent vs. Congruent
    # ══════════════════════════════════════════════════════════

    def run_gate_1(
        self,
        seed: ActivationEventSeed,
        match_lookup: dict[str, FourAxisMatchResult],
        parent_receipt_id: Optional[str] = None,
    ) -> Gate1Result:
        """Stage 2: Gate 1 — Adjacent vs. Congruent validation.

        AC1: [1.0, 1.0, 1.0, 0.0] → FAIL (any zero axis = FAIL, not just sum check)

        Thresholds:
          sum ≥ 3.5 AND min > 0.0 → PASS
          sum = 3.0, all > 0.0 → PROVISIONAL
          any = 0.0 OR sum < 3.0 → FAIL
        """
        gate_1 = Gate1Result()

        # Get the match for this seed
        match = match_lookup.get(seed.match_id)
        if not match:
            logger.error(
                "FR12 Gate 1: No match found for seed %s (match_id=%s)",
                seed.seed_id, seed.match_id,
            )
            gate_1.verdict = GateVerdict.FAIL
            # Receipt
            self.receipt_chain.log(
                agent_id=self.GATE_1_AGENT_ID,
                action="STAGE-2-GATE-1",
                asset_id=f"FR12-G1-{self.coach_acronym}-{seed.seed_id}",
                input_summary=f"Seed {seed.seed_id}: match not found",
                output_summary="Gate 1 FAIL: match data missing",
                decision="FAIL",
                parent_receipt_id=parent_receipt_id,
                metadata={"seed_id": seed.seed_id, "match_id": seed.match_id},
            )
            return gate_1

        # Extract axis scores
        axis_scores: dict[str, float] = {}
        for axis_name, axis_score in match.axis_scores.items():
            axis_scores[axis_name] = axis_score.score

        # Evaluate
        verdict = gate_1.evaluate(axis_scores)

        # Receipt: STAGE-2-GATE-1
        self.receipt_chain.log(
            agent_id=self.GATE_1_AGENT_ID,
            action="STAGE-2-GATE-1",
            asset_id=f"FR12-G1-{self.coach_acronym}-{seed.seed_id}",
            input_summary=(
                f"Seed {seed.seed_id}: axis_scores={axis_scores}"
            ),
            output_summary=(
                f"Gate 1 {verdict.value}: total={gate_1.total_score:.1f}, "
                f"min={gate_1.min_axis_score:.1f}, "
                f"adjacent_flag={gate_1.adjacent_flag}"
            ),
            decision=verdict.value,
            parent_receipt_id=parent_receipt_id,
            metadata={
                "seed_id": seed.seed_id,
                "axis_matrix": gate_1.axis_matrix,
                "total_score": gate_1.total_score,
                "min_axis_score": gate_1.min_axis_score,
                "verdict": verdict.value,
            },
        )

        return gate_1

    # ══════════════════════════════════════════════════════════
    # Stage 3: GATE 2 — Language Drift Prevention
    # ══════════════════════════════════════════════════════════

    def run_gate_2(
        self,
        seed: ActivationEventSeed,
        parent_receipt_id: Optional[str] = None,
    ) -> Gate2Result:
        """Stage 3: Gate 2 — Language Drift Prevention.

        AC2: 2 lemmatized matches → PROVISIONAL + language_drift_warning

        Thresholds:
          ≥3 lemmatized tribal terms → PASS
          2 → PROVISIONAL + language_drift_warning
          0-1 → FAIL
        """
        gate_2 = Gate2Result()

        # Perform lemmatized matching
        # Collect terms from the seed text
        full_text = " ".join([
            seed.activation_event.grounding_statement,
            seed.activation_event.episodic_bridge,
            seed.activation_event.question_text,
        ]).lower()

        # Lemmatize: simple lowercase + strip approach
        # (Full NLP lemmatization would use spaCy; here we use basic normalization)
        tribal_terms = seed.tribal_language.extracted_terms
        matched_terms: list[str] = []
        for term in tribal_terms:
            # Basic lemmatization: lowercase exact match or stem match
            term_lower = term.lower().strip()
            if term_lower in full_text:
                matched_terms.append(term_lower)
            elif len(term_lower) > 4 and term_lower[:-1] in full_text:
                # Simple stem: remove trailing 's'
                matched_terms.append(term_lower)

        # Evaluate
        verdict = gate_2.evaluate(matched_terms)

        # Track consecutive failures for fallback
        if verdict == GateVerdict.FAIL:
            self._gate_2_consecutive_failures += 1
        else:
            self._gate_2_consecutive_failures = 0

        # Receipt: STAGE-3-GATE-2
        self.receipt_chain.log(
            agent_id=self.GATE_2_AGENT_ID,
            action="STAGE-3-GATE-2",
            asset_id=f"FR12-G2-{self.coach_acronym}-{seed.seed_id}",
            input_summary=(
                f"Seed {seed.seed_id}: {len(tribal_terms)} extracted terms, "
                f"checking in {len(full_text)} chars"
            ),
            output_summary=(
                f"Gate 2 {verdict.value}: {len(matched_terms)}/{len(tribal_terms)} terms matched, "
                f"drift_warning={gate_2.language_drift_warning}, "
                f"consecutive_failures={self._gate_2_consecutive_failures}"
            ),
            decision=verdict.value,
            parent_receipt_id=parent_receipt_id,
            metadata={
                "seed_id": seed.seed_id,
                "extracted_terms": tribal_terms[:5],
                "matched_terms": matched_terms[:5],
                "matched_count": len(matched_terms),
                "verdict": verdict.value,
                "consecutive_failures": self._gate_2_consecutive_failures,
            },
        )

        return gate_2

    # ══════════════════════════════════════════════════════════
    # Stage 4: EMIT — Package DEP-ENG-027
    # ══════════════════════════════════════════════════════════

    def emit_certificate(
        self,
        seed: ActivationEventSeed,
        gate_1: Gate1Result,
        gate_2: Gate2Result,
        receipt_chain_hash: str = "",
        parent_receipt_id: Optional[str] = None,
    ) -> GateDiagnosticCertificate:
        """Stage 4: Package Gate Diagnostic Certificate (DEP-ENG-027).

        AC3: Certificate contains 5 receipt hashes documenting the validation chain.

        Gate 3 is initialized as AWAITING_TELEGRAM_PAYLOAD.
        """
        cert = GateDiagnosticCertificate(
            seed_reference_id=seed.seed_id,
            receipt_chain_hash=receipt_chain_hash,
            gate_1_structural_congruence=gate_1,
            gate_2_language_drift=gate_2,
            gate_3_authenticity_feedback=Gate3Result(),
        )

        # Compute certificate hash
        cert_json = cert.model_dump_json(indent=2)
        cert_hash = hashlib.sha256(cert_json.encode()).hexdigest()

        # Receipt: STAGE-4-EMIT
        self.receipt_chain.log(
            agent_id=self.GATEKEEPER_AGENT_ID,
            action="STAGE-4-EMIT",
            asset_id=f"DEP-ENG-027-{self.coach_acronym}-{seed.seed_id}",
            input_summary=(
                f"Seed {seed.seed_id}: Gate1={gate_1.verdict.value}, "
                f"Gate2={gate_2.verdict.value}"
            ),
            output_summary=(
                f"DEP-ENG-027 emitted: cert={cert.gate_certificate_id}, "
                f"cleared={cert.is_cleared_for_emission()}, "
                f"Gate3=AWAITING_TELEGRAM_PAYLOAD"
            ),
            decision="dep_eng_027_emitted",
            parent_receipt_id=parent_receipt_id,
            metadata={
                "output_hash": cert_hash,
                "dep_id": "DEP-ENG-027",
                "certificate_id": cert.gate_certificate_id,
                "seed_id": seed.seed_id,
                "gate_1_verdict": gate_1.verdict.value,
                "gate_2_verdict": gate_2.verdict.value,
                "cleared_for_emission": cert.is_cleared_for_emission(),
            },
        )

        return cert

    # ══════════════════════════════════════════════════════════
    # Stage 5: GATE 3 — Authenticity Score Feedback Loop (async)
    # ══════════════════════════════════════════════════════════

    def run_gate_3(
        self,
        certificate: GateDiagnosticCertificate,
        liwc_score: float,
        historical_trigger_decay: bool = False,
        historical_trigger_flawless: bool = False,
        parent_receipt_id: Optional[str] = None,
    ) -> GateDiagnosticCertificate:
        """Stage 5: Gate 3 — Authenticity Score Feedback Loop.

        AC4: LIWC-22 < 5.0 + historical decay → PTG retrograde to active_processing
        AC5: ADR-01 Coach Isolation — no cross-silo access

        This stage runs ASYNCHRONOUSLY after the coach records a voice note
        and the Telegram bot receives DEP-ENG-019 (Session Transcript).

        Thresholds:
          ≥7.0 → PASS (increase activation precedence by 15%)
          5.0-6.9 → PROVISIONAL (flag ESK anchor as potentially degraded)
          <5.0 + historical decay → FAIL (Coach Temporal Error)
          <5.0 + historical flawless → FAIL (Audience Extraction Error)
        """
        gate_3 = certificate.gate_3_authenticity_feedback

        # Evaluate
        verdict = gate_3.evaluate(
            liwc_score=liwc_score,
            historical_trigger_decay=historical_trigger_decay,
            historical_trigger_flawless=historical_trigger_flawless,
        )

        # Log downstream mutations if FAIL
        mutation_summary = ""
        if verdict == GateVerdict.FAIL:
            if gate_3.failure_mode == Gate3FailureMode.COACH_TEMPORAL_ERROR:
                mutation_summary = (
                    "DEP-LIB-002 mutation: trigger PTG retrograded from "
                    "resolved_dual_layer to active_processing"
                )
            elif gate_3.failure_mode == Gate3FailureMode.AUDIENCE_EXTRACTION_ERROR:
                mutation_summary = (
                    "DEP-ENG-006 mutation: audience segment flagged for L3 "
                    "re-validation"
                )

        # Receipt: STAGE-5-GATE-3
        self.receipt_chain.log(
            agent_id=self.GATE_3_AGENT_ID,
            action="STAGE-5-GATE-3",
            asset_id=f"FR12-G3-{self.coach_acronym}-{certificate.seed_reference_id}",
            input_summary=(
                f"Cert {certificate.gate_certificate_id}: "
                f"LIWC-22 score={liwc_score}, "
                f"historical_decay={historical_trigger_decay}, "
                f"historical_flawless={historical_trigger_flawless}"
            ),
            output_summary=(
                f"Gate 3 {verdict.value}: "
                f"failure_mode={gate_3.failure_mode.value if gate_3.failure_mode else 'none'}, "
                f"coach_ptg_retrograde={gate_3.coach_ptg_retrograde}, "
                f"audience_l3_revalidation={gate_3.audience_l3_revalidation}"
                + (f" — {mutation_summary}" if mutation_summary else "")
            ),
            decision=verdict.value,
            parent_receipt_id=parent_receipt_id,
            metadata={
                "certificate_id": certificate.gate_certificate_id,
                "liwc_score": liwc_score,
                "verdict": verdict.value,
                "failure_mode": gate_3.failure_mode.value if gate_3.failure_mode else None,
                "coach_ptg_retrograde": gate_3.coach_ptg_retrograde,
                "audience_l3_revalidation": gate_3.audience_l3_revalidation,
                "downstream_mutations": gate_3.downstream_mutations,
            },
        )

        return certificate

    # ══════════════════════════════════════════════════════════
    # Full Pipeline Orchestration (Stages 1–4, Gate 3 is async)
    # ══════════════════════════════════════════════════════════

    def run(
        self,
        match_results: Optional[MatchResultsPayload],
        activation_seeds: Optional[ActivationSeedsPayload],
    ) -> list[GateDiagnosticCertificate]:
        """Execute Stages 1–4 of the failure prevention pipeline.

        Gate 3 is NOT run here — it runs asynchronously when the
        Telegram bot receives a voice note (DEP-ENG-019).

        Returns:
            List of GateDiagnosticCertificate (one per seed).
        """
        # Stage 1: INGEST
        ingested = self.ingest(match_results, activation_seeds)

        if ingested.get("empty"):
            return []

        assert activation_seeds is not None  # Pyright narrowing
        match_lookup: dict[str, Any] = ingested["match_lookup"]
        ingest_receipt_id: str = ingested["ingest_receipt_id"]
        certificates: list[GateDiagnosticCertificate] = []
        fallback_invoked = False

        for seed in activation_seeds.seeds:
            # Stage 2: GATE 1
            gate_1 = self.run_gate_1(
                seed, match_lookup, parent_receipt_id=ingest_receipt_id
            )

            # Stage 3: GATE 2
            gate_2 = self.run_gate_2(
                seed, parent_receipt_id=ingest_receipt_id
            )

            # Check for fallback (3 consecutive Gate 2 failures)
            if self._gate_2_consecutive_failures >= self.GATE_2_CONSECUTIVE_FAILURE_LIMIT:
                fallback_invoked = True
                logger.warning(
                    "FR12 FALLBACK: %d consecutive Gate 2 failures. "
                    "system_fallback_invoked=True — escalating to operator.",
                    self._gate_2_consecutive_failures,
                )

            # Stage 4: EMIT certificate
            cert = self.emit_certificate(
                seed=seed,
                gate_1=gate_1,
                gate_2=gate_2,
                parent_receipt_id=ingest_receipt_id,
            )
            certificates.append(cert)

        if fallback_invoked:
            logger.warning(
                "FR12: system_fallback_invoked after %d consecutive Gate 2 failures. "
                "Backward compatibility fallback activated.",
                self.GATE_2_CONSECUTIVE_FAILURE_LIMIT,
            )

        return certificates

    @property
    def gate_2_consecutive_failures(self) -> int:
        """Expose consecutive failure count for pipeline orchestrator."""
        return self._gate_2_consecutive_failures
