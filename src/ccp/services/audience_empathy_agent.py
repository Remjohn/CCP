"""
CCP Step 6 — FR9: Audience Empathy Agent

5-phase pipeline:
  Phase 1: INGEST — Load DEP-ENG-006, theme, coach_soul; pre-flight gates
  Phase 2: SEGMENT — Produce exactly 6 segments with unique DHD + coping combinations
  Phase 3: EXTRACT — Populate 6×12 matrix (72+ cells, no empty)
  Phase 4: VALIDATE — Enforce Four Laws of Audience Research Distillation
  Phase 5: EMIT — Compute verdict, produce {theme_slug}_context_premise.json

Architecture:
  §Context_Premise_Trigger_Matching_Layer Part 2
  Four Laws of Audience Research Distillation (hard gates)

Acceptance Criteria: AC1–AC12

DEP-IDs consumed:
  DEP-ENG-006: ContextPremiseMap (tribe_profile_models.py)
  DEP-ENG-041: Receipt Chain Guard (receipt_chain.py)

DEP-IDs produced:
  Theme-specific Context Premise JSON (consumed by FR10)
"""

from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.container_module_models import (
    AudienceSegmentProfile,
    AuthenticationVerdict,
    ContextPremiseInsight,
    CopingMechanismInsight,
    DepthDistribution,
    EmotionalTriggerInsight,
    FourLawsStatus,
    HiddenBeliefInsight,
    InGroupTerm,
    ProvenanceReport,
    RejectionTerm,
    SegmentCategories,
    ThemeContextPremise,
    TribalLanguageRegistry,
)

logger = logging.getLogger(__name__)


class AudienceEmpathyAgent:
    """FR9: Audience Empathy Agent — 5-phase pipeline.

    Transforms standing DEP-ENG-006 (Context Premise Map) into a theme-specific
    audience intelligence artefact, validated by the Four Laws of Audience
    Research Distillation.

    Produces: {theme_slug}_context_premise.json
    """

    AGENT_ID = "audience_empathy_agent_v1"
    REQUIRED_SEGMENT_COUNT = 6
    REQUIRED_CATEGORIES = 12
    STRUCTURAL_CATEGORIES = ("hidden_beliefs", "emotional_triggers", "coping_mechanism")
    STRUCTURAL_L3_MINIMUM = 2

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
    # Phase 1: INGEST
    # ══════════════════════════════════════════════════════════

    def ingest(
        self,
        theme: str,
        context_premise_map: Optional[dict[str, Any]],
        coach_soul: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Phase 1: Load and validate inputs.

        AC1: Pipeline halts with descriptive error when DEP-ENG-006
        (Context Premise Map) is missing or empty.

        Returns:
            Ingested payload dict for Phase 2.
        """
        # PRE-FLIGHT: DEP-ENG-006 must exist and be non-empty
        if not context_premise_map:
            raise ValueError(
                "FR9 Pre-Flight HALT: DEP-ENG-006 (Context Premise Map) is missing "
                "or empty. Cannot run Audience Empathy Agent without standing audience "
                "intelligence. Run FR6 (Tribe Profile Distillation) first."
            )

        if not theme or not theme.strip():
            raise ValueError(
                "FR9 Pre-Flight HALT: Theme is required. Cannot generate a "
                "theme-specific Context Premise without a theme."
            )

        # Compute input hash for receipt
        input_data = json.dumps(
            {"theme": theme, "context_premise_map_keys": sorted(context_premise_map.keys())},
            sort_keys=True,
        )
        input_hash = hashlib.sha256(input_data.encode()).hexdigest()

        # Receipt: AUDIENCE-EMPATHY-INGEST
        ingest_receipt = self.receipt_chain.log(
            agent_id=self.AGENT_ID,
            action="AUDIENCE-EMPATHY-INGEST",
            asset_id=f"FR9-{self.coach_acronym}-{theme[:20]}",
            input_summary=(
                f"Theme: {theme}, "
                f"DEP-ENG-006 keys: {len(context_premise_map)}, "
                f"coach_soul: {'present' if coach_soul else 'absent'}"
            ),
            output_summary="FR9 ingest phase complete — pre-flight PASSED",
            decision="proceed",
            metadata={
                "theme": theme,
                "input_hash": input_hash,
                "dep_eng_006_keys": sorted(context_premise_map.keys())[:10],
                "coach_soul_present": coach_soul is not None,
            },
        )

        return {
            "theme": theme,
            "context_premise_map": context_premise_map,
            "coach_soul": coach_soul or {},
            "ingest_receipt_id": ingest_receipt.receipt_id,
            "input_hash": input_hash,
        }

    # ══════════════════════════════════════════════════════════
    # Phase 2: SEGMENT
    # ══════════════════════════════════════════════════════════

    def segment(
        self,
        ingested: dict[str, Any],
        segments_data: list[dict[str, Any]],
    ) -> list[AudienceSegmentProfile]:
        """Phase 2: Produce exactly 6 audience segments.

        AC2: Exactly 6 audience segments, each with unique segment_id,
        dhd_label, and coping_trajectory_position.
        AC10: No two segments share the same DHD + coping combination.

        Args:
            ingested: Output of Phase 1.
            segments_data: List of 6 segment dictionaries with required fields.

        Returns:
            List of 6 AudienceSegmentProfile instances.
        """
        if len(segments_data) != self.REQUIRED_SEGMENT_COUNT:
            raise ValueError(
                f"FR9 Phase 2 HALT: Exactly {self.REQUIRED_SEGMENT_COUNT} segments "
                f"required, got {len(segments_data)}. Each segment must represent a "
                f"genuine psychological boundary within the audience."
            )

        segments: list[AudienceSegmentProfile] = []
        seen_combos: set[tuple[str, str]] = set()

        for i, seg_data in enumerate(segments_data):
            profile = AudienceSegmentProfile(
                segment_id=seg_data.get("segment_id", f"SEG-{i+1:02d}"),
                dhd_label=seg_data.get("dhd_label", ""),
                coping_trajectory_position=seg_data.get(
                    "coping_trajectory_position", "SEARCH"
                ),
                regulatory_focus=seg_data.get("regulatory_focus", "mixed"),
                primary_moral_foundation_violated=seg_data.get(
                    "primary_moral_foundation_violated", ""
                ),
                description=seg_data.get("description", ""),
            )

            # AC10: Unique DHD + coping trajectory combination
            combo = (profile.dhd_label, profile.coping_trajectory_position)
            if combo in seen_combos:
                raise ValueError(
                    f"FR9 Phase 2 HALT (AC10): Duplicate DHD + coping_trajectory "
                    f"combination detected: {combo}. Each segment must represent a "
                    f"unique psychological position."
                )
            seen_combos.add(combo)
            segments.append(profile)

        return segments

    # ══════════════════════════════════════════════════════════
    # Phase 3: EXTRACT
    # ══════════════════════════════════════════════════════════

    def extract(
        self,
        segments: list[AudienceSegmentProfile],
        extraction_data: dict[str, dict[str, list[dict[str, Any]]]],
    ) -> list[AudienceSegmentProfile]:
        """Phase 3: Populate the 6×12 matrix.

        AC3: All 72 cells (6 segments × 12 categories) populated,
        no empty cells.

        Args:
            segments: The 6 segments from Phase 2.
            extraction_data: Dict of {segment_id: {category_name: [insight_dicts]}}.

        Returns:
            Segments with populated categories.
        """
        for seg in segments:
            seg_data = extraction_data.get(seg.segment_id, {})
            seg.categories = self._build_categories(seg_data)

            # Verify no empty categories (AC3)
            filled = seg.categories.category_count()
            if filled < self.REQUIRED_CATEGORIES:
                raise ValueError(
                    f"FR9 Phase 3 HALT (AC3): Segment {seg.segment_id} has only "
                    f"{filled}/12 categories populated. All 12 categories must have "
                    f"at least one insight."
                )

        return segments

    def _build_categories(
        self, seg_data: dict[str, list[dict[str, Any]]]
    ) -> SegmentCategories:
        """Build SegmentCategories from extraction data, using correct model per category."""
        return SegmentCategories(
            wants=[ContextPremiseInsight(**i) for i in seg_data.get("wants", [])],
            frustrations=[ContextPremiseInsight(**i) for i in seg_data.get("frustrations", [])],
            dreams=[ContextPremiseInsight(**i) for i in seg_data.get("dreams", [])],
            fears=[ContextPremiseInsight(**i) for i in seg_data.get("fears", [])],
            suspicions=[ContextPremiseInsight(**i) for i in seg_data.get("suspicions", [])],
            insecurities=[ContextPremiseInsight(**i) for i in seg_data.get("insecurities", [])],
            envy_feelings=[ContextPremiseInsight(**i) for i in seg_data.get("envy_feelings", [])],
            enemies=[ContextPremiseInsight(**i) for i in seg_data.get("enemies", [])],
            coping_mechanism=[
                CopingMechanismInsight(**i) for i in seg_data.get("coping_mechanism", [])
            ],
            hidden_beliefs=[
                HiddenBeliefInsight(**i) for i in seg_data.get("hidden_beliefs", [])
            ],
            emotional_triggers=[
                EmotionalTriggerInsight(**i) for i in seg_data.get("emotional_triggers", [])
            ],
            success_markers=[
                ContextPremiseInsight(**i) for i in seg_data.get("success_markers", [])
            ],
        )

    # ══════════════════════════════════════════════════════════
    # Phase 4: VALIDATE (Four Laws of Audience Research Distillation)
    # ══════════════════════════════════════════════════════════

    def validate(
        self,
        segments: list[AudienceSegmentProfile],
        tribal_language_data: Optional[dict[str, Any]] = None,
    ) -> tuple[FourLawsStatus, DepthDistribution, TribalLanguageRegistry, ProvenanceReport]:
        """Phase 4: Enforce Four Laws.

        AC4: Law 2 — L2 ≥ 30%, L3 ≥ 10%
        AC5: Law 1 — 2am test via LIWC-22 ≥ 70th percentile for L3
        AC6: Law 3 — ≥10 in-group terms, ≥5 rejection terms
        AC7: Law 4 — ≤20% unverified data
        AC8: Structural weighting (Hidden Beliefs, Emotional Triggers, Coping Mechanism)
             ≥2 L3 entries per structural category per segment

        Returns:
            (FourLawsStatus, DepthDistribution, TribalLanguageRegistry, ProvenanceReport)
        """
        all_insights: list[ContextPremiseInsight] = []
        for seg in segments:
            all_insights.extend(seg.categories.all_insights())

        # ── Law 1: Lived Reality (2am Test) ──
        law_1_pass = self._validate_law_1(all_insights)

        # ── Law 2: Depth Stratification ──
        depth_dist = self._compute_depth_distribution(all_insights)
        law_2_pass = depth_dist.passes_law_2()

        # ── Law 3: Tribal Language ──
        tribal_registry = self._build_tribal_registry(tribal_language_data)
        law_3_pass = tribal_registry.passes_law_3()

        # ── Law 4: Data Provenance ──
        provenance = self._compute_provenance(all_insights)
        law_4_pass = provenance.passes_law_4()

        # ── AC8: Structural Weighting ──
        self._validate_structural_weighting(segments)

        # Compose status
        status = FourLawsStatus(
            law_1_lived_reality="PASS" if law_1_pass else "FAIL",
            law_2_depth_stratification="PASS" if law_2_pass else "FAIL",
            law_3_tribal_language="PASS" if law_3_pass else "FAIL",
            law_4_data_provenance="PASS" if law_4_pass else "FAIL",
        )
        status.compute_verdict()

        return status, depth_dist, tribal_registry, provenance

    def _validate_law_1(self, insights: list[ContextPremiseInsight]) -> bool:
        """Law 1 — Lived Reality (2am test):
        All L3 entries must pass the neurobiological 2am test.
        LIWC-22 authenticity ≥ 70th percentile for L3.
        Entries failing are reclassified to L2 or L1.

        Returns True if at least some L3 remain after reclassification."""
        l3_entries = [i for i in insights if i.depth == "L3"]
        if not l3_entries:
            return False

        passed_l3 = 0
        for entry in l3_entries:
            if entry.two_am_test:
                passed_l3 += 1
            else:
                # Reclassify to L2
                entry.depth = "L2"
                logger.info(
                    "FR9 Law 1: L3 entry reclassified to L2 (failed 2am test): %s",
                    entry.text[:60],
                )

        return passed_l3 > 0

    def _compute_depth_distribution(
        self, insights: list[ContextPremiseInsight]
    ) -> DepthDistribution:
        """Law 2 — Depth Stratification: L2 ≥ 30%, L3 ≥ 10%."""
        total = len(insights)
        if total == 0:
            return DepthDistribution(l1=0.0, l2=0.0, l3=0.0)
        l1 = sum(1 for i in insights if i.depth == "L1") / total
        l2 = sum(1 for i in insights if i.depth == "L2") / total
        l3 = sum(1 for i in insights if i.depth == "L3") / total
        return DepthDistribution(l1=l1, l2=l2, l3=l3)

    def _build_tribal_registry(
        self, data: Optional[dict[str, Any]]
    ) -> TribalLanguageRegistry:
        """Law 3 — Tribal Language: ≥10 in-group terms, ≥5 rejection terms."""
        if not data:
            return TribalLanguageRegistry()
        in_group = [
            InGroupTerm(**t)
            for t in data.get("in_group_terms", [])
        ]
        rejection = [
            RejectionTerm(**t)
            for t in data.get("rejection_terms", [])
        ]
        return TribalLanguageRegistry(
            in_group_terms=in_group,
            rejection_terms=rejection,
        )

    def _compute_provenance(
        self, insights: list[ContextPremiseInsight]
    ) -> ProvenanceReport:
        """Law 4 — Data Provenance: ≤20% unverified."""
        total = len(insights)
        if total == 0:
            return ProvenanceReport()
        verified = sum(
            1 for i in insights
            if i.source and not i.source.lower().startswith("inferred")
            and "likely based on" not in i.source.lower()
        )
        unverified = total - verified
        return ProvenanceReport(
            total_insights=total,
            verified_count=verified,
            unverified_count=unverified,
            provenance_percentage=verified / total if total > 0 else 0.0,
        )

    def _validate_structural_weighting(
        self, segments: list[AudienceSegmentProfile]
    ) -> None:
        """AC8: Each structural category (hidden_beliefs, emotional_triggers,
        coping_mechanism) must have ≥2 L3 entries per segment."""
        for seg in segments:
            for cat_name in self.STRUCTURAL_CATEGORIES:
                cat_list = getattr(seg.categories, cat_name, [])
                l3_count = sum(1 for i in cat_list if i.depth == "L3")
                if l3_count < self.STRUCTURAL_L3_MINIMUM:
                    raise ValueError(
                        f"FR9 AC8 HALT: Segment {seg.segment_id}, category "
                        f"'{cat_name}' has only {l3_count} L3 entries — "
                        f"minimum {self.STRUCTURAL_L3_MINIMUM} required. "
                        f"Structural categories carry disproportionate weight in "
                        f"downstream matching and must be L3 saturated."
                    )

    # ══════════════════════════════════════════════════════════
    # Phase 5: EMIT
    # ══════════════════════════════════════════════════════════

    def emit(
        self,
        theme: str,
        segments: list[AudienceSegmentProfile],
        four_laws_status: FourLawsStatus,
        depth_distribution: DepthDistribution,
        tribal_language_registry: TribalLanguageRegistry,
        provenance_report: ProvenanceReport,
        parent_receipt_id: Optional[str] = None,
        output_dir: Optional[Path] = None,
    ) -> ThemeContextPremise:
        """Phase 5: Compose final output, compute verdict, write receipt.

        AC9: AUTHENTICATED/PROVISIONAL/FAILED verdict logic.
        AC11: Output schema consumable by FR10.
        AC12: Enrichment without DEP-ENG-006 mutation.

        Returns:
            ThemeContextPremise with computed verdict.
        """
        # Build the output artefact
        result = ThemeContextPremise(
            theme=theme,
            segments=segments,
            depth_distribution=depth_distribution,
            tribal_language_registry=tribal_language_registry,
            four_laws_status=four_laws_status,
            provenance_report=provenance_report,
        )

        # Compute output hash
        output_data = result.model_dump_json(indent=2)
        output_hash = hashlib.sha256(output_data.encode()).hexdigest()

        # Receipt: AUDIENCE-EMPATHY-EMIT
        emit_receipt = self.receipt_chain.log(
            agent_id=self.AGENT_ID,
            action="AUDIENCE-EMPATHY-EMIT",
            asset_id=f"FR9-{self.coach_acronym}-{theme[:20]}",
            input_summary=f"6 segments validated by Four Laws for theme: {theme}",
            output_summary=(
                f"Verdict: {four_laws_status.overall_status}, "
                f"L3: {depth_distribution.l3:.1%}, "
                f"Tribal terms: {len(tribal_language_registry.in_group_terms)}, "
                f"Provenance: {provenance_report.provenance_percentage:.1%}"
            ),
            decision=four_laws_status.overall_status.lower(),
            parent_receipt_id=parent_receipt_id,
            metadata={
                "theme": theme,
                "output_hash": output_hash,
                "verdict": four_laws_status.overall_status,
                "l1_pct": round(depth_distribution.l1, 3),
                "l2_pct": round(depth_distribution.l2, 3),
                "l3_pct": round(depth_distribution.l3, 3),
                "in_group_terms_count": len(tribal_language_registry.in_group_terms),
                "rejection_terms_count": len(tribal_language_registry.rejection_terms),
                "provenance_pct": round(provenance_report.provenance_percentage, 3),
            },
        )

        # Optionally write to disk
        if output_dir is not None:
            self._write_output(result, output_dir)

        logger.info(
            "FR9 EMIT: theme=%s verdict=%s receipt=%s",
            theme,
            four_laws_status.overall_status,
            emit_receipt.receipt_id,
        )

        return result

    def _write_output(self, result: ThemeContextPremise, output_dir: Path) -> None:
        """Write the context premise JSON to disk."""
        output_dir.mkdir(parents=True, exist_ok=True)
        slug = (
            result.theme.lower()
            .replace(" ", "_")
            .replace("-", "_")
            .replace("'", "")
            .replace('"', "")
        )
        path = output_dir / f"{slug}_context_premise.json"
        path.write_text(result.model_dump_json(indent=2), encoding="utf-8")
        logger.info("FR9: Wrote context premise to %s", path)

    # ══════════════════════════════════════════════════════════
    # Full Pipeline Orchestration
    # ══════════════════════════════════════════════════════════

    def run(
        self,
        theme: str,
        context_premise_map: Optional[dict[str, Any]],
        segments_data: list[dict[str, Any]],
        extraction_data: dict[str, dict[str, list[dict[str, Any]]]],
        tribal_language_data: Optional[dict[str, Any]] = None,
        coach_soul: Optional[dict[str, Any]] = None,
        output_dir: Optional[Path] = None,
    ) -> ThemeContextPremise:
        """Execute the full 5-phase Audience Empathy Agent pipeline.

        Args:
            theme: The theme to generate context premise for.
            context_premise_map: DEP-ENG-006 standing audience intelligence.
            segments_data: 6 segment definitions.
            extraction_data: 6×12 insight extraction data.
            tribal_language_data: In-group/rejection terms.
            coach_soul: Coach soul document (optional enrichment).
            output_dir: Optional output directory.

        Returns:
            ThemeContextPremise with verdict.

        Raises:
            ValueError: On any pre-flight or validation failure.
        """
        # Phase 1: INGEST
        ingested = self.ingest(
            theme=theme,
            context_premise_map=context_premise_map,
            coach_soul=coach_soul,
        )

        # Phase 2: SEGMENT
        segments = self.segment(ingested, segments_data)

        # Phase 3: EXTRACT
        segments = self.extract(segments, extraction_data)

        # Phase 4: VALIDATE (Four Laws)
        four_laws, depth_dist, tribal_reg, provenance = self.validate(
            segments, tribal_language_data
        )

        # Phase 5: EMIT
        result = self.emit(
            theme=theme,
            segments=segments,
            four_laws_status=four_laws,
            depth_distribution=depth_dist,
            tribal_language_registry=tribal_reg,
            provenance_report=provenance,
            parent_receipt_id=ingested.get("ingest_receipt_id"),
            output_dir=output_dir,
        )

        return result
