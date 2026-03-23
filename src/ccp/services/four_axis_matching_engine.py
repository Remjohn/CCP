"""
CCP Step 6 — FR10: Four-Axis Structural Matching Engine

4-phase pipeline:
  Phase 1: INGEST — Load DEP-LIB-001, DEP-LIB-002, FR9 output; pre-flight gates
  Phase 2: L3 EXTRACT — Extract L3 structural coordinates from audience segments
  Phase 3: FOUR-AXIS MATCH — Cross-product evaluation (N triggers × 6 segments)
  Phase 4: EMIT — Classify, sort, and emit DEP-ENG-010

Architecture:
  §Context_Premise_Trigger_Matching_Layer Part 4
  Scoring: EXACT/CONGRUENT(1.0), ADJACENT/PARTIAL(0.5), NONE(0.0)
  Classification: CONFIRMED(4.0), STRONG(3.0–3.5 no zeros), ADJACENT(any zero OR <3.0), NO_MATCH(<2.0)
  PTG safety gate: raw_unresolved triggers excluded in Phase 1

Acceptance Criteria: AC1–AC13

DEP-IDs consumed:
  DEP-LIB-001: EmotionalDNAProfile (emotional_dna_models.py)
  DEP-LIB-002: TriggerMap (trigger_map_models.py)
  FR9 output: ThemeContextPremise (container_module_models.py)

DEP-IDs produced:
  DEP-ENG-010: FourAxisMatchResult / MatchResultsPayload
"""

from __future__ import annotations

import hashlib
import json
import logging
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.container_module_models import (
    AxisCongruence,
    AxisScore,
    FourAxisMatchResult,
    L3StructuralCoordinate,
    MatchClassification,
    MatchResultsPayload,
    ThemeContextPremise,
)

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════
# Axis Scoring Constants
# ══════════════════════════════════════════════════════════════

SCORE_EXACT: float = 1.0
SCORE_ADJACENT: float = 0.5
SCORE_NONE: float = 0.0

# Moral Foundation adjacency map (per CCP spec)
MF_ADJACENCY: dict[str, set[str]] = {
    "care_harm": {"fairness_cheating"},
    "fairness_cheating": {"care_harm", "liberty_oppression"},
    "loyalty_betrayal": {"authority_subversion"},
    "authority_subversion": {"loyalty_betrayal", "sanctity_degradation"},
    "sanctity_degradation": {"authority_subversion"},
    "liberty_oppression": {"fairness_cheating"},
}

# Agency attribution adjacency
AGENCY_ADJACENCY: dict[str, set[str]] = {
    "self": {"individual"},
    "individual": {"self", "institutional"},
    "institutional": {"individual", "systemic"},
    "systemic": {"institutional"},
}

# Coping trajectory adjacency
COPING_ADJACENCY: dict[str, set[str]] = {
    "SEARCH": {"ACTIVE"},
    "ACTIVE": {"SEARCH", "EXHAUSTED"},
    "EXHAUSTED": {"ACTIVE"},
}


class FourAxisMatchingEngine:
    """FR10: Four-Axis Structural Matching Engine.

    Evaluates structural congruence between coach resolved triggers
    (DEP-LIB-002) and audience L3 pain segments (FR9 output) across
    four axes:
      1. Moral Foundation
      2. Coping Potential
      3. Agency Attribution
      4. Temporal Position (PTG status)

    Produces: DEP-ENG-010 (MatchResultsPayload)
    """

    AGENT_ID = "four_axis_matching_engine_v1"

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
    # Phase 1: INGEST + Pre-Flight Gates
    # ══════════════════════════════════════════════════════════

    def ingest(
        self,
        emotional_dna: Optional[dict[str, Any]],
        trigger_map: Optional[dict[str, Any]],
        context_premise: Optional[ThemeContextPremise],
    ) -> dict[str, Any]:
        """Phase 1: Load and validate all three upstream dependencies.

        AC1: Pipeline halts when DEP-LIB-001, DEP-LIB-002, or FR9 output missing.
        AC2: raw_unresolved triggers excluded with logging.

        Pre-flight gates:
          Gate A: DEP-LIB-001 exists + overall_confidence ≥ 0.5
          Gate B: DEP-LIB-002 has ≥1 resolved trigger
          Gate C: FR9 output exists AND verdict ≠ FAILED
          Gate D: PTG raw_unresolved exclusion (safety filter)
        """
        # Gate A: DEP-LIB-001
        if not emotional_dna:
            raise ValueError(
                "FR10 Pre-Flight HALT (Gate A): DEP-LIB-001 (Emotional DNA Profile) "
                "is missing. Cannot match without coach psychological coordinates. "
                "Run FR4 (Emotional DNA Extraction) first."
            )
        confidence = emotional_dna.get("overall_confidence", 0.0)
        if confidence < 0.5:
            raise ValueError(
                f"FR10 Pre-Flight HALT (Gate A): DEP-LIB-001 overall_confidence "
                f"= {confidence} (minimum: 0.5). Emotional DNA is insufficient."
            )

        # Gate B: DEP-LIB-002
        if not trigger_map:
            raise ValueError(
                "FR10 Pre-Flight HALT (Gate B): DEP-LIB-002 (Trigger Map) is "
                "missing. Cannot match without resolved coach triggers. "
                "Run FR5 (Trigger Map Extraction) first."
            )
        triggers = trigger_map.get("triggers", [])
        if not triggers:
            raise ValueError(
                "FR10 Pre-Flight HALT (Gate B): DEP-LIB-002 has zero triggers. "
                "At least 1 resolved trigger is required."
            )

        # Gate C: FR9 output
        if not context_premise:
            raise ValueError(
                "FR10 Pre-Flight HALT (Gate C): FR9 Context Premise output is "
                "missing. Run FR9 (Audience Empathy Agent) first."
            )
        if context_premise.four_laws_status.overall_status == "FAILED":
            raise ValueError(
                "FR10 Pre-Flight HALT (Gate C): FR9 Context Premise verdict is "
                "FAILED. Cannot proceed with failed audience intelligence."
            )

        # Gate D: PTG safety exclusion (AC2)
        safe_triggers: list[dict[str, Any]] = []
        excluded_triggers: list[dict[str, Any]] = []
        for trigger in triggers:
            ptg_status = trigger.get("ptg_assessment", {}).get("status", "")
            if ptg_status == "raw_unresolved":
                excluded_triggers.append(trigger)
                logger.warning(
                    "FR10 Gate D: Excluding trigger %s — PTG status raw_unresolved",
                    trigger.get("trigger_id", "unknown"),
                )
            else:
                safe_triggers.append(trigger)

        if not safe_triggers:
            raise ValueError(
                "FR10 Pre-Flight HALT (Gate D): All triggers are raw_unresolved. "
                "No safe triggers available for matching."
            )

        # Compute input hash
        input_data = json.dumps({
            "emotional_dna_keys": sorted(emotional_dna.keys()),
            "trigger_count": len(safe_triggers),
            "theme": context_premise.theme,
        }, sort_keys=True)
        input_hash = hashlib.sha256(input_data.encode()).hexdigest()

        # Receipt: PHASE-1-INGEST
        ingest_receipt = self.receipt_chain.log(
            agent_id=self.AGENT_ID,
            action="PHASE-1-INGEST",
            asset_id=f"FR10-{self.coach_acronym}-{context_premise.theme[:20]}",
            input_summary=(
                f"DEP-LIB-001 confidence={confidence}, "
                f"DEP-LIB-002 triggers={len(triggers)} (safe={len(safe_triggers)}, "
                f"excluded={len(excluded_triggers)}), "
                f"FR9 theme={context_premise.theme} verdict={context_premise.four_laws_status.overall_status}"
            ),
            output_summary="FR10 ingest complete — all pre-flight gates PASSED",
            decision="proceed",
            metadata={
                "theme": context_premise.theme,
                "input_hash": input_hash,
                "triggers_total": len(triggers),
                "triggers_safe": len(safe_triggers),
                "triggers_excluded_raw_unresolved": len(excluded_triggers),
                "fr9_verdict": context_premise.four_laws_status.overall_status,
            },
        )

        return {
            "emotional_dna": emotional_dna,
            "safe_triggers": safe_triggers,
            "excluded_triggers": excluded_triggers,
            "context_premise": context_premise,
            "ingest_receipt_id": ingest_receipt.receipt_id,
            "input_hash": input_hash,
        }

    # ══════════════════════════════════════════════════════════
    # Phase 2: L3 EXTRACT
    # ══════════════════════════════════════════════════════════

    def extract_l3_coordinates(
        self,
        context_premise: ThemeContextPremise,
    ) -> list[L3StructuralCoordinate]:
        """Phase 2: Extract L3 structural coordinates from each audience segment.

        AC3: Only L3 entries used for matching. L1/L2 filtered out.

        Returns:
            List of L3StructuralCoordinate, one per segment.
        """
        coordinates: list[L3StructuralCoordinate] = []

        for seg in context_premise.segments:
            # Extract moral foundations from L3 emotional triggers only
            moral_foundations: list[str] = []
            for trigger in seg.categories.emotional_triggers:
                if trigger.depth == "L3":
                    moral_foundations.append(trigger.moral_foundation)

            # Extract coping mechanism pattern from L3 entries only
            coping_pattern: dict[str, str] = {}
            for coping in seg.categories.coping_mechanism:
                if coping.depth == "L3":
                    coping_pattern["mechanism"] = coping.text[:100]
                    coping_pattern["agency_attribution"] = (
                        coping.agency_attribution_pattern
                    )
                    coping_pattern["coping_potential"] = (
                        coping.coping_potential_assessment
                    )
                    break  # Use first L3 coping mechanism

            # Extract agency attribution target
            agency_target = coping_pattern.get("agency_attribution", "")

            # Extract temporal position from L3 hidden beliefs (currently_inside evidence)
            temporal_evidence: dict[str, Any] = {
                "currently_inside": False,
                "frustration_indicators": [],
                "hidden_belief_indicators": [],
                "search_phase_markers": [],
            }
            for belief in seg.categories.hidden_beliefs:
                if belief.depth == "L3":
                    temporal_evidence["hidden_belief_indicators"].append(
                        belief.text[:80]
                    )

            # Collect L3 tribal language terms from all L3 insights
            tribal_terms: list[str] = []
            for insight in seg.categories.all_insights():
                if insight.depth == "L3":
                    tribal_terms.extend(insight.tribal_terms)
            # Deduplicate
            tribal_terms = list(dict.fromkeys(tribal_terms))

            coord = L3StructuralCoordinate(
                segment_id=seg.segment_id,
                moral_foundations_violated=list(set(moral_foundations)),
                coping_mechanism_pattern=coping_pattern,
                agency_attribution_target=agency_target,
                temporal_position_evidence=temporal_evidence,
                tribal_language_terms=tribal_terms,
            )
            coordinates.append(coord)

        return coordinates

    # ══════════════════════════════════════════════════════════
    # Phase 3: FOUR-AXIS MATCH
    # ══════════════════════════════════════════════════════════

    def match(
        self,
        safe_triggers: list[dict[str, Any]],
        l3_coordinates: list[L3StructuralCoordinate],
        emotional_dna: dict[str, Any],
        theme: str,
    ) -> MatchResultsPayload:
        """Phase 3+4: Cross-product evaluation of triggers × segments.

        AC4: Score [1.0,1.0,1.0,0.0] → ADJACENT (not CONFIRMED)
        AC5: 2-axis match → ADJACENT, no seed
        AC12: N triggers × 6 segments = N×6 combinations evaluated

        Returns:
            MatchResultsPayload with classified results.
        """
        payload = MatchResultsPayload(
            theme=theme,
            triggers_evaluated=len(safe_triggers),
            segments_evaluated=len(l3_coordinates),
            total_combinations_evaluated=len(safe_triggers) * len(l3_coordinates),
            inputs_used={
                "emotional_dna_version": emotional_dna.get("version", "unknown"),
                "trigger_map_version": emotional_dna.get("trigger_map_version", "unknown"),
                "context_premise_version": "FR9-v1",
            },
        )

        for trigger in safe_triggers:
            for coord in l3_coordinates:
                match_result = self._evaluate_single_match(
                    trigger, coord, emotional_dna, theme
                )

                # Classify and bin
                classification = match_result.match_classification
                if classification == MatchClassification.CONFIRMED:
                    payload.matches["confirmed"].append(match_result)
                elif classification == MatchClassification.STRONG:
                    payload.matches["strong"].append(match_result)
                elif classification == MatchClassification.ADJACENT:
                    payload.matches["adjacent"].append(match_result)
                else:
                    payload.no_match_count += 1

        return payload

    def _evaluate_single_match(
        self,
        trigger: dict[str, Any],
        coord: L3StructuralCoordinate,
        emotional_dna: dict[str, Any],
        theme: str,
    ) -> FourAxisMatchResult:
        """Evaluate a single trigger × segment match across 4 axes."""
        trigger_id = trigger.get("trigger_id", "unknown")
        segment_id = coord.segment_id

        # Axis 1: Moral Foundation
        axis_1 = self._score_moral_foundation(trigger, coord)

        # Axis 2: Coping Potential
        axis_2 = self._score_coping_potential(trigger, coord, emotional_dna)

        # Axis 3: Agency Attribution
        axis_3 = self._score_agency_attribution(trigger, coord, emotional_dna)

        # Axis 4: Temporal Position (PTG alignment)
        axis_4 = self._score_temporal_position(trigger, coord)

        result = FourAxisMatchResult(
            trigger_id=trigger_id,
            segment_id=segment_id,
            theme=theme,
            axis_scores={
                "moral_foundation": axis_1,
                "coping_potential": axis_2,
                "agency_attribution": axis_3,
                "temporal_position": axis_4,
            },
        )

        # Compute classification
        result.compute_classification()

        # Build diagnostic for non-CONFIRMED matches
        if result.match_classification != MatchClassification.CONFIRMED:
            failing_axes = [
                name for name, ax in result.axis_scores.items()
                if ax.score < SCORE_EXACT
            ]
            result.diagnostic = (
                f"Non-CONFIRMED: failing axes = {failing_axes}, "
                f"scores = {[result.axis_scores[a].score for a in failing_axes]}"
            )

        return result

    def _score_moral_foundation(
        self, trigger: dict[str, Any], coord: L3StructuralCoordinate
    ) -> AxisScore:
        """Axis 1: Moral Foundation matching.
        Coach trigger's MFT → audience segment's violated MFT foundations.
        EXACT if same foundation, ADJACENT if adjacent (per MF_ADJACENCY), NONE otherwise."""
        coach_mf = trigger.get("moral_foundation", "").lower().strip()
        audience_mfs = [mf.lower().strip() for mf in coord.moral_foundations_violated]

        if coach_mf in audience_mfs:
            return AxisScore(
                axis_name="moral_foundation",
                congruence=AxisCongruence.EXACT,
                score=SCORE_EXACT,
                coach_value=coach_mf,
                audience_value=", ".join(audience_mfs),
            )

        # Check adjacency
        adjacent_set = MF_ADJACENCY.get(coach_mf, set())
        if any(amf in adjacent_set for amf in audience_mfs):
            return AxisScore(
                axis_name="moral_foundation",
                congruence=AxisCongruence.ADJACENT,
                score=SCORE_ADJACENT,
                coach_value=coach_mf,
                audience_value=", ".join(audience_mfs),
                failure_mode="adjacent_moral_foundation",
            )

        return AxisScore(
            axis_name="moral_foundation",
            congruence=AxisCongruence.NONE,
            score=SCORE_NONE,
            coach_value=coach_mf,
            audience_value=", ".join(audience_mfs),
            failure_mode="no_moral_foundation_overlap",
        )

    def _score_coping_potential(
        self,
        trigger: dict[str, Any],
        coord: L3StructuralCoordinate,
        emotional_dna: dict[str, Any],
    ) -> AxisScore:
        """Axis 2: Coping Potential matching.
        Coach's coping trajectory position → audience segment's coping trajectory.
        CONGRUENT if same position, PARTIAL if adjacent, NONE otherwise."""
        coach_coping = trigger.get("coping_trajectory_position", "").upper().strip()
        audience_coping = coord.coping_mechanism_pattern.get(
            "coping_potential", ""
        ).upper().strip()

        # Normalize audience coping to trajectory position
        # (audience coping_potential_assessment maps to trajectory position)
        audience_trajectory = self._normalize_coping_to_trajectory(audience_coping)

        if coach_coping == audience_trajectory:
            return AxisScore(
                axis_name="coping_potential",
                congruence=AxisCongruence.CONGRUENT,
                score=SCORE_EXACT,
                coach_value=coach_coping,
                audience_value=audience_trajectory,
            )

        adjacent_set = COPING_ADJACENCY.get(coach_coping, set())
        if audience_trajectory in adjacent_set:
            return AxisScore(
                axis_name="coping_potential",
                congruence=AxisCongruence.PARTIAL,
                score=SCORE_ADJACENT,
                coach_value=coach_coping,
                audience_value=audience_trajectory,
                failure_mode="adjacent_coping_trajectory",
            )

        return AxisScore(
            axis_name="coping_potential",
            congruence=AxisCongruence.NONE,
            score=SCORE_NONE,
            coach_value=coach_coping,
            audience_value=audience_trajectory,
            failure_mode="no_coping_overlap",
        )

    def _normalize_coping_to_trajectory(self, coping_value: str) -> str:
        """Map coping_potential_assessment labels to trajectory positions."""
        mapping = {
            "LOW": "EXHAUSTED",
            "MEDIUM": "ACTIVE",
            "HIGH": "SEARCH",
            "EXHAUSTED": "EXHAUSTED",
            "ACTIVE": "ACTIVE",
            "SEARCH": "SEARCH",
        }
        return mapping.get(coping_value.upper(), coping_value.upper())

    def _score_agency_attribution(
        self,
        trigger: dict[str, Any],
        coord: L3StructuralCoordinate,
        emotional_dna: dict[str, Any],
    ) -> AxisScore:
        """Axis 3: Agency Attribution matching.
        Coach's attribution target → audience attribution target.
        CONGRUENT if same, ADJACENT if adjacent, NONE otherwise."""
        coach_agency = trigger.get("agency_attribution", "").lower().strip()
        # Fallback to emotional DNA agency attribution type
        if not coach_agency:
            coach_agency = emotional_dna.get(
                "agency_attribution_type", ""
            ).lower().strip()

        audience_agency = coord.agency_attribution_target.lower().strip()

        if coach_agency == audience_agency:
            return AxisScore(
                axis_name="agency_attribution",
                congruence=AxisCongruence.CONGRUENT,
                score=SCORE_EXACT,
                coach_value=coach_agency,
                audience_value=audience_agency,
            )

        adjacent_set = AGENCY_ADJACENCY.get(coach_agency, set())
        if audience_agency in adjacent_set:
            return AxisScore(
                axis_name="agency_attribution",
                congruence=AxisCongruence.PARTIAL,
                score=SCORE_ADJACENT,
                coach_value=coach_agency,
                audience_value=audience_agency,
                failure_mode="adjacent_agency_attribution",
            )

        return AxisScore(
            axis_name="agency_attribution",
            congruence=AxisCongruence.NONE,
            score=SCORE_NONE,
            coach_value=coach_agency,
            audience_value=audience_agency,
            failure_mode="no_agency_overlap",
        )

    def _score_temporal_position(
        self, trigger: dict[str, Any], coord: L3StructuralCoordinate
    ) -> AxisScore:
        """Axis 4: Temporal Position matching.
        Coach PTG status = resolved_dual_layer → audience pre-PTG (currently inside).
        CONGRUENT: coach resolved + audience has indicators.
        ADJACENT: coach active_processing + audience has indicators.
        NONE: coach raw_unresolved (should be excluded) or no alignment.
        INVALID: coach raw_unresolved (should never reach here)."""
        coach_ptg = trigger.get("ptg_assessment", {}).get("status", "").lower()

        # raw_unresolved should be filtered in Phase 1 — defensive check
        if coach_ptg == "raw_unresolved":
            return AxisScore(
                axis_name="temporal_position",
                congruence=AxisCongruence.INVALID,
                score=SCORE_NONE,
                coach_value=coach_ptg,
                audience_value="filtered",
                failure_mode="raw_unresolved_reached_matching — should have been excluded",
            )

        has_temporal_evidence = bool(
            coord.temporal_position_evidence.get("hidden_belief_indicators")
            or coord.temporal_position_evidence.get("frustration_indicators")
            or coord.temporal_position_evidence.get("search_phase_markers")
        )

        if coach_ptg == "resolved_dual_layer" and has_temporal_evidence:
            return AxisScore(
                axis_name="temporal_position",
                congruence=AxisCongruence.CONGRUENT,
                score=SCORE_EXACT,
                coach_value=coach_ptg,
                audience_value="pre_ptg_with_evidence",
            )

        if coach_ptg == "active_processing" and has_temporal_evidence:
            return AxisScore(
                axis_name="temporal_position",
                congruence=AxisCongruence.ADJACENT,
                score=SCORE_ADJACENT,
                coach_value=coach_ptg,
                audience_value="pre_ptg_with_evidence",
                failure_mode="coach_still_processing",
            )

        return AxisScore(
            axis_name="temporal_position",
            congruence=AxisCongruence.NONE,
            score=SCORE_NONE,
            coach_value=coach_ptg,
            audience_value="no_temporal_evidence" if not has_temporal_evidence else "evidence_present",
            failure_mode="no_temporal_alignment",
        )

    # ══════════════════════════════════════════════════════════
    # Phase 4+6: EMIT
    # ══════════════════════════════════════════════════════════

    def emit(
        self,
        match_payload: MatchResultsPayload,
        parent_receipt_id: Optional[str] = None,
    ) -> MatchResultsPayload:
        """Phase 4+6: Emit match results with receipt chain.

        Receipts: MATCH-EMIT, PHASE-6-EMIT
        """
        # Compute output hash
        output_json = match_payload.model_dump_json(indent=2)
        output_hash = hashlib.sha256(output_json.encode()).hexdigest()

        total_confirmed = len(match_payload.matches["confirmed"])
        total_strong = len(match_payload.matches["strong"])
        total_adjacent = len(match_payload.matches["adjacent"])

        # Receipt: MATCH-EMIT
        self.receipt_chain.log(
            agent_id=self.AGENT_ID,
            action="MATCH-EMIT",
            asset_id=f"FR10-{self.coach_acronym}-{match_payload.theme[:20]}",
            input_summary=(
                f"Cross-product: {match_payload.triggers_evaluated} triggers × "
                f"{match_payload.segments_evaluated} segments = "
                f"{match_payload.total_combinations_evaluated} combinations"
            ),
            output_summary=(
                f"CONFIRMED={total_confirmed}, STRONG={total_strong}, "
                f"ADJACENT={total_adjacent}, NO_MATCH={match_payload.no_match_count}"
            ),
            decision="emit",
            parent_receipt_id=parent_receipt_id,
            metadata={
                "theme": match_payload.theme,
                "output_hash": output_hash,
                "confirmed": total_confirmed,
                "strong": total_strong,
                "adjacent": total_adjacent,
                "no_match": match_payload.no_match_count,
            },
        )

        # Receipt: PHASE-6-EMIT
        emit_receipt = self.receipt_chain.log(
            agent_id=self.AGENT_ID,
            action="PHASE-6-EMIT",
            asset_id=f"DEP-ENG-010-{self.coach_acronym}-{match_payload.theme[:20]}",
            input_summary=f"DEP-ENG-010 emit for theme: {match_payload.theme}",
            output_summary=(
                f"DEP-ENG-010 emitted: {total_confirmed + total_strong} "
                f"seedable matches ({total_confirmed} confirmed, {total_strong} strong)"
            ),
            decision="dep_eng_010_emitted",
            metadata={
                "dep_id": "DEP-ENG-010",
                "seedable_count": total_confirmed + total_strong,
            },
        )

        logger.info(
            "FR10 EMIT: theme=%s confirmed=%d strong=%d adjacent=%d no_match=%d",
            match_payload.theme,
            total_confirmed,
            total_strong,
            total_adjacent,
            match_payload.no_match_count,
        )

        return match_payload

    # ══════════════════════════════════════════════════════════
    # Full Pipeline Orchestration
    # ══════════════════════════════════════════════════════════

    def run(
        self,
        emotional_dna: Optional[dict[str, Any]],
        trigger_map: Optional[dict[str, Any]],
        context_premise: Optional[ThemeContextPremise],
    ) -> MatchResultsPayload:
        """Execute the full FR10 matching pipeline.

        Args:
            emotional_dna: DEP-LIB-001 dictionary.
            trigger_map: DEP-LIB-002 dictionary.
            context_premise: FR9 ThemeContextPremise output.

        Returns:
            MatchResultsPayload (DEP-ENG-010).

        Raises:
            ValueError: On any pre-flight gate failure.
        """
        # Phase 1: INGEST
        ingested = self.ingest(emotional_dna, trigger_map, context_premise)

        assert context_premise is not None  # Pyright narrowing — guaranteed by ingest

        # Phase 2: L3 EXTRACT
        l3_coords = self.extract_l3_coordinates(context_premise)

        # Phase 3: FOUR-AXIS MATCH
        match_payload = self.match(
            safe_triggers=ingested["safe_triggers"],
            l3_coordinates=l3_coords,
            emotional_dna=ingested["emotional_dna"],
            theme=context_premise.theme,
        )

        # Store exclusion data
        match_payload.exclusions = {
            "raw_unresolved_triggers_excluded": [
                t.get("trigger_id", "unknown")
                for t in ingested["excluded_triggers"]
            ],
            "l1_l2_entries_filtered": "L3-only extraction performed",
        }

        # Phase 4+6: EMIT
        result = self.emit(
            match_payload,
            parent_receipt_id=ingested.get("ingest_receipt_id"),
        )

        return result
