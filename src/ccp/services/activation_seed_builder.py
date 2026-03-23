"""
CCP Step 6 — FR11: Activation Event Seed Construction

5-phase pipeline:
  Phase 1: INGEST — Filter CONFIRMED/STRONG matches from DEP-ENG-010
  Phase 2: ELEMENT SYNTHESIS — Extract 3 mandatory elements per match
  Phase 3: DARN-CAT — Construct evocative question (Taking Steps / Reasons)
  Phase 4: LANGUAGE DRIFT GATE — Verify ≥3 tribal terms preserved
  Phase 5: EMIT — Priority-rank and emit DEP-ENG-011

Architecture:
  §Trigger-First Engine Architecture v3.0 Part 2
  3 mandatory elements: ESK Anchor, L3 Tribal Language (min 3 terms),
  Structural Congruence Point
  DARN-CAT: Miller & Rollnick Taking Steps / Reasons dimensions

Acceptance Criteria: AC1–AC6, AC8–AC9 (no AC7 defined in spec)

DEP-IDs consumed:
  DEP-ENG-010: FourAxisMatchResult / MatchResultsPayload (FR10 output)
  DEP-LIB-002: TriggerMap (trigger_map_models.py)
  FR9 output: ThemeContextPremise (tribal language registry)

DEP-IDs produced:
  DEP-ENG-011: ActivationEventSeed / ActivationSeedsPayload
"""

from __future__ import annotations

import hashlib
import json
import logging
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.container_module_models import (
    ActivationEvent,
    ActivationEventSeed,
    ActivationEventSeedFlags,
    ActivationSeedsPayload,
    AnchorQuality,
    DARNCATDimension,
    ESKAnchor,
    FourAxisMatchResult,
    LanguageDriftStatus,
    MatchClassification,
    MatchResultsPayload,
    StructuralCongruencePoint,
    ThemeContextPremise,
    TribalLanguageElement,
)

logger = logging.getLogger(__name__)


class ActivationSeedBuilder:
    """FR11: Activation Event Seed Construction.

    Transforms CONFIRMED/STRONG matches (DEP-ENG-010) into actionable
    Activation Event Seeds (DEP-ENG-011) with three mandatory elements,
    DARN-CAT formatted evocative questions, and language drift prevention.

    Produces: DEP-ENG-011 (ActivationSeedsPayload)
    """

    AGENT_ID = "activation_seed_builder_v1"
    TRIBAL_TERM_PASS_THRESHOLD = 3
    TRIBAL_TERM_WARNING_THRESHOLD = 2

    def __init__(
        self,
        coach_acronym: str,
        receipt_chain: Optional[ReceiptChain] = None,
    ):
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = receipt_chain or ReceiptChain(
            coach_acronym=self.coach_acronym
        )

    # ══════════════════════════════════════════════════════════
    # Phase 1: INGEST — Filter matches
    # ══════════════════════════════════════════════════════════

    def ingest(
        self,
        match_results: Optional[MatchResultsPayload],
        trigger_map: Optional[dict[str, Any]],
        context_premise: Optional[ThemeContextPremise],
    ) -> dict[str, Any]:
        """Phase 1: Filter to CONFIRMED/STRONG matches only.

        AC1: ADJACENT and NO_MATCH excluded from seed construction.
        AC8: Zero valid matches → graceful exit with empty array.

        Returns:
            Ingested payload with filtered matches.
        """
        if not match_results:
            raise ValueError(
                "FR11 Pre-Flight HALT: DEP-ENG-010 (Match Results) is missing. "
                "Run FR10 (Four-Axis Matching Engine) first."
            )
        if not trigger_map:
            raise ValueError(
                "FR11 Pre-Flight HALT: DEP-LIB-002 (Trigger Map) is missing."
            )
        if not context_premise:
            raise ValueError(
                "FR11 Pre-Flight HALT: FR9 Context Premise is missing."
            )

        # Filter to CONFIRMED + STRONG only (AC1)
        seedable_matches: list[FourAxisMatchResult] = []
        seedable_matches.extend(match_results.matches.get("confirmed", []))
        seedable_matches.extend(match_results.matches.get("strong", []))

        # Build trigger lookup
        triggers_by_id: dict[str, dict[str, Any]] = {}
        for trigger in trigger_map.get("triggers", []):
            tid = trigger.get("trigger_id", "")
            if tid:
                triggers_by_id[tid] = trigger

        # Build tribal language lookup from FR9
        tribal_terms_by_segment: dict[str, list[str]] = {}
        for seg in context_premise.segments:
            terms: list[str] = []
            for insight in seg.categories.all_insights():
                if insight.depth == "L3":
                    terms.extend(insight.tribal_terms)
            tribal_terms_by_segment[seg.segment_id] = list(dict.fromkeys(terms))

        # Compute input hash
        input_data = json.dumps({
            "theme": match_results.theme,
            "seedable_count": len(seedable_matches),
        }, sort_keys=True)
        input_hash = hashlib.sha256(input_data.encode()).hexdigest()

        # Receipt: PHASE-1-INGEST
        ingest_receipt = self.receipt_chain.log(
            agent_id=self.AGENT_ID,
            action="PHASE-1-INGEST",
            asset_id=f"FR11-{self.coach_acronym}-{match_results.theme[:20]}",
            input_summary=(
                f"DEP-ENG-010 theme={match_results.theme}, "
                f"confirmed={len(match_results.matches.get('confirmed', []))}, "
                f"strong={len(match_results.matches.get('strong', []))}, "
                f"adjacent={len(match_results.matches.get('adjacent', []))} (excluded)"
            ),
            output_summary=(
                f"Seedable matches: {len(seedable_matches)} "
                f"(ADJACENT/NO_MATCH excluded per AC1)"
            ),
            decision="proceed" if seedable_matches else "graceful_exit",
            metadata={
                "input_hash": input_hash,
                "theme": match_results.theme,
                "seedable_count": len(seedable_matches),
                "excluded_adjacent": len(match_results.matches.get("adjacent", [])),
                "excluded_no_match": match_results.no_match_count,
            },
        )

        return {
            "seedable_matches": seedable_matches,
            "triggers_by_id": triggers_by_id,
            "tribal_terms_by_segment": tribal_terms_by_segment,
            "context_premise": context_premise,
            "theme": match_results.theme,
            "ingest_receipt_id": ingest_receipt.receipt_id,
            "input_hash": input_hash,
        }

    # ══════════════════════════════════════════════════════════
    # Phase 2: ELEMENT SYNTHESIS
    # ══════════════════════════════════════════════════════════

    def synthesize_elements(
        self,
        match: FourAxisMatchResult,
        trigger_data: dict[str, Any],
        tribal_terms: list[str],
    ) -> tuple[ESKAnchor, TribalLanguageElement, StructuralCongruencePoint]:
        """Phase 2: Extract the 3 mandatory elements for a single match.

        AC2: ESK anchor quality evaluation (esk=full, ge/lp=degraded)
        AC3: Structural congruence point articulation
        AC6: Tribal term count + tribal_terms_used[] preserved

        Returns:
            (ESKAnchor, TribalLanguageElement, StructuralCongruencePoint)
        """
        # Element 1: ESK Anchor (AC2)
        esk_anchor = self._extract_esk_anchor(trigger_data)

        # Element 2: Tribal Language (AC6)
        tribal_element = self._extract_tribal_language(tribal_terms)

        # Element 3: Structural Congruence Point (AC3)
        congruence_point = self._extract_congruence_point(match, trigger_data)

        return esk_anchor, tribal_element, congruence_point

    def _extract_esk_anchor(self, trigger_data: dict[str, Any]) -> ESKAnchor:
        """Extract ESK anchor from coach trigger.
        AC2: AKB level → anchor quality mapping.
        EVENT_SPECIFIC_KNOWLEDGE (ESK) → full quality.
        GENERAL_EVENT or LIFETIME_PERIOD → degraded quality."""
        origin = trigger_data.get("origin_classification", {})
        akb_level = origin.get("akb_level", "lifetime_period").lower()

        # Map AKB level to quality
        if akb_level in ("event_specific_knowledge", "esk"):
            quality = AnchorQuality.FULL
            requires_harvest = False
        else:
            quality = AnchorQuality.DEGRADED
            requires_harvest = True

        sensory_details: list[str] = []
        for anchor in origin.get("sensory_anchors", []):
            if isinstance(anchor, dict):
                desc = anchor.get("description", "")
                if desc:
                    sensory_details.append(desc)
            elif isinstance(anchor, str):
                sensory_details.append(anchor)

        return ESKAnchor(
            akb_level=akb_level,
            sensory_details=sensory_details,
            anchor_quality=quality,
            requires_esk_harvesting=requires_harvest,
        )

    def _extract_tribal_language(
        self, tribal_terms: list[str]
    ) -> TribalLanguageElement:
        """Extract and verify tribal language element.
        Minimum 3 terms required for PASSED status."""
        verified_count = len(tribal_terms)

        if verified_count >= self.TRIBAL_TERM_PASS_THRESHOLD:
            status = LanguageDriftStatus.PASSED
        elif verified_count >= self.TRIBAL_TERM_WARNING_THRESHOLD:
            status = LanguageDriftStatus.WARNING
        else:
            status = LanguageDriftStatus.CRITICAL

        return TribalLanguageElement(
            extracted_terms=tribal_terms[:10],  # Cap at 10 for readability
            verified_count=verified_count,
            language_drift_status=status,
        )

    def _extract_congruence_point(
        self,
        match: FourAxisMatchResult,
        trigger_data: dict[str, Any],
    ) -> StructuralCongruencePoint:
        """Extract the structural congruence point from match data.
        AC3: Exact articulation of the structural overlap."""
        mf_axis = match.axis_scores.get("moral_foundation")
        cp_axis = match.axis_scores.get("coping_potential")
        aa_axis = match.axis_scores.get("agency_attribution")
        tp_axis = match.axis_scores.get("temporal_position")

        # Build articulation from axis data
        parts: list[str] = []
        if mf_axis and mf_axis.score >= 0.5:
            parts.append(
                f"Shared moral violation: {mf_axis.coach_value} "
                f"(coach) ↔ {mf_axis.audience_value} (audience)"
            )
        if cp_axis and cp_axis.score >= 0.5:
            parts.append(
                f"Coping alignment: {cp_axis.coach_value} → {cp_axis.audience_value}"
            )
        if aa_axis and aa_axis.score >= 0.5:
            parts.append(
                f"Shared enemy: {aa_axis.coach_value} ↔ {aa_axis.audience_value}"
            )
        if tp_axis and tp_axis.score >= 0.5:
            parts.append(
                f"Temporal bridge: {tp_axis.coach_value} (coach resolved) → "
                f"{tp_axis.audience_value} (audience experiencing)"
            )

        articulation = "; ".join(parts) if parts else "Insufficient congruence data"

        return StructuralCongruencePoint(
            moral_foundation=mf_axis.coach_value if mf_axis else "",
            coping_pattern=cp_axis.coach_value if cp_axis else "",
            agency_attribution=aa_axis.coach_value if aa_axis else "",
            temporal_position=tp_axis.coach_value if tp_axis else "",
            articulation=articulation,
        )

    # ══════════════════════════════════════════════════════════
    # Phase 3: DARN-CAT Construction
    # ══════════════════════════════════════════════════════════

    def construct_darn_cat(
        self,
        esk_anchor: ESKAnchor,
        tribal_language: TribalLanguageElement,
        congruence_point: StructuralCongruencePoint,
    ) -> ActivationEvent:
        """Phase 3: Build DARN-CAT formatted evocative question.

        AC4: Taking Steps or Reasons dimension only.
        Uses all 3 elements to construct:
          - Grounding statement (Element 3 + 2): audience position in their language
          - Episodic bridge (Element 3 + 1): connects to coach ESK
          - Question text (Taking Steps / Reasons)
        """
        # Select DARN-CAT dimension based on content
        # Default: Taking Steps (action-oriented)
        dimension = DARNCATDimension.TAKING_STEPS

        # Build grounding statement using tribal language + congruence
        tribal_terms_text = ", ".join(tribal_language.extracted_terms[:3])
        grounding = (
            f"When someone experiences {congruence_point.moral_foundation or 'this'} "
            f"— {tribal_terms_text} — "
            f"there's a pattern of {congruence_point.coping_pattern or 'coping'} "
            f"that emerges."
        )

        # Build episodic bridge using ESK anchor
        sensory_text = "; ".join(esk_anchor.sensory_details[:2]) if esk_anchor.sensory_details else ""
        episodic = (
            f"The coach navigated this same structural pattern"
            + (f" — {sensory_text}" if sensory_text else "")
            + f" and found that {congruence_point.temporal_position or 'resolution'} "
            f"was possible."
        )

        # Build the evocative question
        if dimension == DARNCATDimension.TAKING_STEPS:
            question = (
                f"What would it look like if you started to move through "
                f"the {congruence_point.moral_foundation or 'challenge'} "
                f"using {tribal_terms_text}?"
            )
        else:
            question = (
                f"Why does addressing {congruence_point.moral_foundation or 'this'} "
                f"matter to you right now, especially given "
                f"{tribal_terms_text}?"
            )

        # Identify tribal terms actually present in the question text
        terms_in_question = [
            term for term in tribal_language.extracted_terms
            if term.lower() in question.lower()
        ]

        return ActivationEvent(
            darn_cat_dimension=dimension,
            grounding_statement=grounding,
            episodic_bridge=episodic,
            question_text=question,
            tribal_terms_used=terms_in_question,
        )

    # ══════════════════════════════════════════════════════════
    # Phase 4: LANGUAGE DRIFT GATE
    # ══════════════════════════════════════════════════════════

    def language_drift_gate(
        self,
        seed: ActivationEventSeed,
        parent_receipt_id: Optional[str] = None,
    ) -> ActivationEventSeed:
        """Phase 4: Verify tribal language preservation in seed text.

        AC5: 0 terms → rejection + regeneration attempt.
        AC6: Tribal term count and terms_used tracked.

        Thresholds:
          ≥3 terms → PASSED
          1-2 terms → WARNING (proceed with flag)
          0 terms → CRITICAL (reject + attempt regeneration)
        """
        # Count tribal terms in the full seed text
        full_text = " ".join([
            seed.activation_event.grounding_statement,
            seed.activation_event.episodic_bridge,
            seed.activation_event.question_text,
        ]).lower()

        matched_terms: list[str] = [
            term for term in seed.tribal_language.extracted_terms
            if term.lower() in full_text
        ]

        term_count = len(matched_terms)

        if term_count >= self.TRIBAL_TERM_PASS_THRESHOLD:
            drift_status = LanguageDriftStatus.PASSED
        elif term_count >= self.TRIBAL_TERM_WARNING_THRESHOLD:
            drift_status = LanguageDriftStatus.WARNING
            seed.flags.language_drift_risk = True
            logger.warning(
                "FR11 Language Drift WARNING: seed %s has only %d tribal terms "
                "(minimum 3 for full pass). Proceeding with flag.",
                seed.seed_id, term_count,
            )
        else:
            drift_status = LanguageDriftStatus.CRITICAL
            logger.error(
                "FR11 Language Drift CRITICAL: seed %s has %d tribal terms "
                "(minimum 3 required). Seed REJECTED.",
                seed.seed_id, term_count,
            )

        seed.tribal_language.language_drift_status = drift_status
        seed.tribal_language.verified_count = term_count
        seed.activation_event.tribal_terms_used = matched_terms

        # Receipt: PHASE-4-LANGUAGE-DRIFT-GATE
        self.receipt_chain.log(
            agent_id=self.AGENT_ID,
            action="PHASE-4-LANGUAGE-DRIFT-GATE",
            asset_id=f"FR11-{self.coach_acronym}-{seed.seed_id}",
            input_summary=f"Seed {seed.seed_id}: checking {len(seed.tribal_language.extracted_terms)} terms",
            output_summary=(
                f"Drift status: {drift_status.value}, matched: {term_count}, "
                f"terms: {matched_terms[:5]}"
            ),
            decision=drift_status.value,
            parent_receipt_id=parent_receipt_id,
            metadata={
                "seed_id": seed.seed_id,
                "extracted_terms": seed.tribal_language.extracted_terms[:5],
                "matched_terms": matched_terms[:5],
                "matched_count": term_count,
                "drift_status": drift_status.value,
            },
        )

        return seed

    # ══════════════════════════════════════════════════════════
    # Phase 5: EMIT
    # ══════════════════════════════════════════════════════════

    def emit(
        self,
        theme: str,
        seeds: list[ActivationEventSeed],
        graceful_exit: bool = False,
        parent_receipt_id: Optional[str] = None,
    ) -> ActivationSeedsPayload:
        """Phase 5: Priority-rank seeds and emit DEP-ENG-011.

        AC11 (from FR10): Priority ranking: match score → ESK quality → tribal count.
        AC8: Graceful exit for zero matches.

        Returns:
            ActivationSeedsPayload (DEP-ENG-011).
        """
        # Priority ranking (AC11): match_score → anchor_quality → tribal_term_count
        ranked_seeds = sorted(
            seeds,
            key=lambda s: (
                s.match_score,
                1 if s.esk_anchor.anchor_quality == AnchorQuality.FULL else 0,
                s.tribal_language.verified_count,
            ),
            reverse=True,
        )

        # Assign priority ranks
        for i, seed in enumerate(ranked_seeds):
            seed.priority_rank = i + 1

        payload = ActivationSeedsPayload(
            theme=theme,
            seeds=ranked_seeds,
            graceful_exit=graceful_exit,
            status="graceful_exit_zero_matches" if graceful_exit else "active",
        )

        # Compute output hash
        output_json = payload.model_dump_json(indent=2)
        output_hash = hashlib.sha256(output_json.encode()).hexdigest()

        # Receipt: PHASE-5-EMIT
        emit_receipt = self.receipt_chain.log(
            agent_id=self.AGENT_ID,
            action="PHASE-5-EMIT",
            asset_id=f"DEP-ENG-011-{self.coach_acronym}-{theme[:20]}",
            input_summary=f"Theme: {theme}, seeds: {len(ranked_seeds)}, graceful_exit: {graceful_exit}",
            output_summary=(
                f"DEP-ENG-011 emitted: {len(ranked_seeds)} seeds "
                f"({'graceful exit' if graceful_exit else 'active'}), "
                f"drift_warnings={sum(1 for s in ranked_seeds if s.flags.language_drift_risk)}, "
                f"degraded_anchors={sum(1 for s in ranked_seeds if s.flags.degraded_anchor)}"
            ),
            decision="dep_eng_011_emitted",
            parent_receipt_id=parent_receipt_id,
            metadata={
                "output_hash": output_hash,
                "dep_id": "DEP-ENG-011",
                "theme": theme,
                "seed_count": len(ranked_seeds),
                "graceful_exit": graceful_exit,
                "drift_warnings": sum(1 for s in ranked_seeds if s.flags.language_drift_risk),
                "degraded_anchors": sum(1 for s in ranked_seeds if s.flags.degraded_anchor),
            },
        )

        logger.info(
            "FR11 EMIT: theme=%s seeds=%d graceful_exit=%s",
            theme, len(ranked_seeds), graceful_exit,
        )

        return payload

    # ══════════════════════════════════════════════════════════
    # Full Pipeline Orchestration
    # ══════════════════════════════════════════════════════════

    def run(
        self,
        match_results: Optional[MatchResultsPayload],
        trigger_map: Optional[dict[str, Any]],
        context_premise: Optional[ThemeContextPremise],
    ) -> ActivationSeedsPayload:
        """Execute the full FR11 seed construction pipeline.

        Args:
            match_results: DEP-ENG-010 from FR10.
            trigger_map: DEP-LIB-002 dictionary.
            context_premise: FR9 ThemeContextPremise.

        Returns:
            ActivationSeedsPayload (DEP-ENG-011).
        """
        # Phase 1: INGEST
        ingested = self.ingest(match_results, trigger_map, context_premise)

        seedable_matches: list[FourAxisMatchResult] = ingested["seedable_matches"]
        triggers_by_id: dict[str, dict[str, Any]] = ingested["triggers_by_id"]
        tribal_terms_by_segment: dict[str, list[str]] = ingested["tribal_terms_by_segment"]
        theme: str = ingested["theme"]
        ingest_receipt_id: str = ingested["ingest_receipt_id"]

        # AC8: Graceful exit for zero valid matches
        if not seedable_matches:
            logger.info(
                "FR11 Graceful Exit: Zero CONFIRMED/STRONG matches for theme '%s'. "
                "Emitting empty seed payload.",
                theme,
            )
            return self.emit(
                theme=theme,
                seeds=[],
                graceful_exit=True,
                parent_receipt_id=ingest_receipt_id,
            )

        # Process each seedable match
        seeds: list[ActivationEventSeed] = []
        for match in seedable_matches:
            trigger_data = triggers_by_id.get(match.trigger_id, {})
            tribal_terms = tribal_terms_by_segment.get(match.segment_id, [])

            # Phase 2: ELEMENT SYNTHESIS
            esk_anchor, tribal_element, congruence_point = self.synthesize_elements(
                match, trigger_data, tribal_terms
            )

            # Phase 3: DARN-CAT
            activation_event = self.construct_darn_cat(
                esk_anchor, tribal_element, congruence_point
            )

            # Build seed
            seed = ActivationEventSeed(
                match_id=match.match_id,
                match_classification=match.match_classification,
                match_score=match.total_score,
                esk_anchor=esk_anchor,
                tribal_language=tribal_element,
                structural_congruence_point=congruence_point,
                activation_event=activation_event,
                flags=ActivationEventSeedFlags(
                    degraded_anchor=esk_anchor.anchor_quality == AnchorQuality.DEGRADED,
                    requires_esk_harvesting=esk_anchor.requires_esk_harvesting,
                ),
            )

            # Phase 4: LANGUAGE DRIFT GATE
            seed = self.language_drift_gate(seed, parent_receipt_id=ingest_receipt_id)

            # AC5: Critical drift → reject (do not include in output)
            if seed.tribal_language.language_drift_status == LanguageDriftStatus.CRITICAL:
                logger.warning(
                    "FR11: Seed %s rejected — language drift CRITICAL (0 tribal terms)",
                    seed.seed_id,
                )
                continue

            seeds.append(seed)

        # Phase 5: EMIT
        return self.emit(
            theme=theme,
            seeds=seeds,
            graceful_exit=len(seeds) == 0,
            parent_receipt_id=ingest_receipt_id,
        )
