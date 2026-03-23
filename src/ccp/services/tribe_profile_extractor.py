"""
CCP FR6 — Tribe Profile Extractor (Stage A) (Unit 2)
Stage A pipeline: INGEST → Research Planning → Cultural Harvesting → EMIT → VALIDATE → CHECKPOINT.

Consumes H11 TribeDossier (FR0B) → produces tribe_profile.json.

Spec reference: FR6 Tech Spec
  §Phase A1 INGEST — load audience raw data, coach_soul, philosophy brief
  §Phase A2 RESEARCH PLANNING — 4-dimension research framework
  §Phase A3 CULTURAL HARVESTING — I-R-E-V-C extraction with volume quotas
  §Phase A4 EMIT — write tribe_profile.json
  §Phase A5 VALIDATE — schema validation against all volume quotas
  §Phase A6 CHECKPOINT — config.yaml status update

Research basis: Kozinets Netnography (2020)
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.tribe_profile_models import (
    AntiAspirationalMarker,
    CulturalArtifactsSection,
    DepthLevel,
    EmotionalMode,
    EmotionalQuoteItem,
    EmotionalResonanceSection,
    HeroEnemyItem,
    HighArousalTriggerItem,
    HumorExampleItem,
    HumorProfileSection,
    HumorTargetItem,
    InsideJokeItem,
    ResearchDimension,
    TabooItem,
    TribeProfile,
    TribeSlangItem,
    VisualCodeType,
    VisualRecognitionCode,
    VolumeQuotaResult,
)
from src.ccp.models.tribe_research_models import (
    CulturalArtifacts,
    EmotionalLandscape,
    HumorDNAProfile,
    SocialArchitecture,
    TribeDossier,
)


class TribeProfileExtractor:
    """FR6 Stage A: Tribe Soul Extraction (The Tribe Cartographer).

    Processes the H11 Tribe Dossier into a structured tribe_profile.json
    covering cultural artifacts, humor DNA, emotional resonance, visual
    recognition codes, and in-group language.

    Governed by the 4 Laws of Tribe Profile Distillation (validation).
    ADR-01: All outputs scoped to coach tenant.
    """

    def __init__(
        self,
        coach_id: str,
        coach_acronym: str,
        receipt_chain: ReceiptChain,
        base_dir: str = "./coaches",
    ):
        self.coach_id = coach_id
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = receipt_chain
        self.base_dir = Path(base_dir)
        self.coach_dir = self.base_dir / self.coach_acronym
        self.intelligence_dir = self.coach_dir / "intelligence" / "tribe"
        self.intelligence_dir.mkdir(parents=True, exist_ok=True)

    # ──────────────────────────────────────────────────────────
    # Phase A1: INGEST
    # ──────────────────────────────────────────────────────────

    def ingest(
        self,
        tribe_dossier: Optional[TribeDossier],
        audience_raw_data: Optional[list[dict[str, Any]]],
        coach_soul: Optional[dict[str, Any]],
        coach_philosophy_brief: Optional[str],
        tshala_sentiment_report: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Spec §Phase A1: Load all inputs and perform PRE-FLIGHT check.

        AC1: Pipeline halts with descriptive error when audience raw data
        is empty or missing.
        """
        # PRE-FLIGHT: Verify audience raw data exists and is non-empty
        has_dossier = tribe_dossier is not None
        has_raw = audience_raw_data is not None and len(audience_raw_data) > 0

        if not has_dossier and not has_raw:
            raise ValueError(
                "Cannot extract tribe profile. Audience raw data not found. "
                "Conduct audience research first (FR0B Tribe Soul Research)."
            )

        # Receipt write (Phase A1)
        ingest_receipt = self.receipt_chain.log(
            agent_id="tribe_soul_extraction_engine_v2",
            action="TRIBE-EXTRACT-INGEST",
            asset_id=f"DEP-H11-{self.coach_acronym}",
            input_summary=(
                f"H11 dossier: {'present' if has_dossier else 'absent'}, "
                f"raw data: {len(audience_raw_data) if audience_raw_data else 0} entries, "
                f"coach_soul: {'present' if coach_soul else 'absent'}, "
                f"philosophy_brief: {'present' if coach_philosophy_brief else 'absent'}, "
                f"tshala: {'present' if tshala_sentiment_report else 'absent'}"
            ),
            output_summary="Tribe extraction ingest phase complete",
            decision="proceed",
            metadata={
                "has_dossier": has_dossier,
                "has_raw_data": has_raw,
                "raw_data_count": len(audience_raw_data) if audience_raw_data else 0,
            },
        )

        return {
            "tribe_dossier": tribe_dossier,
            "audience_raw_data": audience_raw_data or [],
            "coach_soul": coach_soul or {},
            "coach_philosophy_brief": coach_philosophy_brief or "",
            "tshala_sentiment_report": tshala_sentiment_report,
            "ingest_receipt_id": ingest_receipt.receipt_id,
        }

    # ──────────────────────────────────────────────────────────
    # Phase A2: RESEARCH PLANNING
    # ──────────────────────────────────────────────────────────

    def plan_research(
        self,
        ingest_data: dict[str, Any],
    ) -> dict[str, list[str]]:
        """Spec §Phase A2: 4-dimensional research planning.
        Generates platform targets for each dimension."""
        research_plan: dict[str, list[str]] = {
            ResearchDimension.CULTURAL_ARTIFACT.value: [
                "Subreddits", "Discord channels",
                "closed Facebook groups", "industry forums",
            ],
            ResearchDimension.HUMOR_PROFILE.value: [
                "Flair-filtered posts", "top-voted funny content",
                "downvoted humor analysis",
            ],
            ResearchDimension.EMOTIONAL_LANDSCAPE.value: [
                "Rant/vent threads", "success/celebration posts",
                "high-engagement discussions",
            ],
            ResearchDimension.SOCIAL_DYNAMICS.value: [
                "Newcomer correction threads", "moderation actions",
                "status signaling",
            ],
        }
        return research_plan

    # ──────────────────────────────────────────────────────────
    # Phase A3: CULTURAL HARVESTING (I-R-E-V-C)
    # ──────────────────────────────────────────────────────────

    def harvest_cultural_artifacts(
        self,
        tribe_dossier: Optional[TribeDossier],
        audience_raw_data: list[dict[str, Any]],
    ) -> CulturalArtifactsSection:
        """Spec §Phase A3 3A: Extract cultural artifacts from dossier.
        Volume quotas: slang ≥10, inside jokes ≥5, heroes ≥5, enemies ≥5."""
        section = CulturalArtifactsSection()

        if tribe_dossier is not None:
            # Extract from H11 Section A (Cultural Artifacts)
            ca = tribe_dossier.section_a_cultural_artifacts
            for slang in ca.slang_entries:
                section.tribe_slang.append(TribeSlangItem(
                    term=slang.term,
                    definition=slang.definition,
                    example_quote=(
                        slang.usage_examples[0].quote
                        if slang.usage_examples else ""
                    ),
                ))

            for joke in ca.inside_jokes:
                section.inside_jokes.append(InsideJokeItem(
                    joke_reference=joke.joke_reference,
                    context=joke.context,
                    example_quote=(
                        joke.examples[0].quote if joke.examples else ""
                    ),
                ))

            for hero_enemy in ca.hero_enemy_posts:
                item = HeroEnemyItem(
                    name=hero_enemy.figure_name,
                    role=hero_enemy.role,
                    evidence_quote=(
                        hero_enemy.quotes[0].quote if hero_enemy.quotes else ""
                    ),
                )
                if hero_enemy.role == "hero":
                    section.shared_heroes.append(item)
                else:
                    section.common_enemies.append(item)

        # Supplement from raw data if needed
        for raw in audience_raw_data:
            raw_type = raw.get("type", "")
            if raw_type == "slang" and len(section.tribe_slang) < 10:
                section.tribe_slang.append(TribeSlangItem(
                    term=raw.get("term", ""),
                    definition=raw.get("definition", ""),
                    example_quote=raw.get("quote", ""),
                ))

        return section

    def harvest_humor_profile(
        self,
        tribe_dossier: Optional[TribeDossier],
        audience_raw_data: list[dict[str, Any]],
    ) -> HumorProfileSection:
        """Spec §Phase A3 3B: Humor DNA profiling.
        Volume quotas: ≥3 examples per style, ≥5 targets, ≥2 taboos."""
        section = HumorProfileSection()

        if tribe_dossier is not None:
            hd = tribe_dossier.section_b_humor_dna
            if hd.styles_identified:
                section.dominant_style = hd.styles_identified[0].value
                if len(hd.styles_identified) > 1:
                    section.secondary_style = hd.styles_identified[1].value

            for post in hd.humor_posts:
                section.style_examples.append(HumorExampleItem(
                    style=post.style.value,
                    content=post.content.quote,
                    source=post.content.source_platform,
                ))

            for taboo in hd.taboo_entries:
                section.taboos_and_no_go_zones.append(TabooItem(
                    topic=taboo.topic,
                    evidence_reaction=taboo.community_reaction,
                ))

        return section

    def harvest_emotional_resonance(
        self,
        tribe_dossier: Optional[TribeDossier],
        audience_raw_data: list[dict[str, Any]],
    ) -> EmotionalResonanceSection:
        """Spec §Phase A3 3C: Emotional resonance mapping.
        Volume quotas: ≥5 aspirations, ≥5 anxieties, ≥3+3 triggers."""
        section = EmotionalResonanceSection()

        if tribe_dossier is not None:
            el = tribe_dossier.section_c_emotional_landscape
            for asp in el.aspiration_quotes:
                section.primary_aspirations.append(EmotionalQuoteItem(
                    text=asp.content.quote,
                    source=asp.content.source_platform,
                    depth=DepthLevel(f"L{asp.depth_level}"),
                ))

            for anx in el.anxiety_quotes:
                section.core_anxieties.append(EmotionalQuoteItem(
                    text=anx.content.quote,
                    source=anx.content.source_platform,
                    depth=DepthLevel(f"L{anx.depth_level}"),
                ))

            for trig in el.positive_triggers:
                section.high_arousal_triggers.append(HighArousalTriggerItem(
                    event_type=trig.content.category,
                    valence="positive",
                    reaction_quote=trig.content.quote,
                ))

            for trig in el.negative_triggers:
                section.high_arousal_triggers.append(HighArousalTriggerItem(
                    event_type=trig.content.category,
                    valence="negative",
                    reaction_quote=trig.content.quote,
                ))

        return section

    def harvest_visual_codes(
        self,
        tribe_dossier: Optional[TribeDossier],
        audience_raw_data: list[dict[str, Any]],
    ) -> list[VisualRecognitionCode]:
        """Spec §Phase A3 3D Law 1: Visual Recognition Codes.
        ≥5 insider objects, ≥3 rejection triggers."""
        codes: list[VisualRecognitionCode] = []

        # Extract from raw data entries with visual_code type
        for raw in audience_raw_data:
            if raw.get("type") == "visual_code":
                code_type_str = raw.get("code_type", "insider")
                try:
                    code_type = VisualCodeType(code_type_str)
                except ValueError:
                    code_type = VisualCodeType.INSIDER
                codes.append(VisualRecognitionCode(
                    code_type=code_type,
                    description=raw.get("description", ""),
                    tribe_significance=raw.get("significance", ""),
                    handling_notes=raw.get("handling_notes", ""),
                    examples=raw.get("examples", []),
                ))

        return codes

    def harvest_anti_aspirational_markers(
        self,
        tribe_dossier: Optional[TribeDossier],
        audience_raw_data: list[dict[str, Any]],
    ) -> list[AntiAspirationalMarker]:
        """Spec §Phase A3 3D Law 5: Anti-Aspirational Markers.
        ≥3 items the tribe actively rejects."""
        markers: list[AntiAspirationalMarker] = []

        for raw in audience_raw_data:
            if raw.get("type") == "anti_aspirational":
                markers.append(AntiAspirationalMarker(
                    marker=raw.get("marker", ""),
                    why_rejected=raw.get("why_rejected", ""),
                    evidence_quotes=raw.get("evidence_quotes", []),
                ))

        return markers

    # ──────────────────────────────────────────────────────────
    # Phase A4: EMIT
    # ──────────────────────────────────────────────────────────

    def emit(
        self,
        profile: TribeProfile,
        ingest_receipt_id: str,
    ) -> str:
        """Spec §Phase A4: Write tribe_profile.json and receipt."""
        output_path = self.intelligence_dir / "tribe_profile.json"
        output_path.write_text(
            profile.model_dump_json(indent=2),
            encoding="utf-8",
        )

        # Receipt write (Phase A4)
        emit_receipt = self.receipt_chain.log(
            agent_id="tribe_soul_extraction_engine_v2",
            action="TRIBE-EXTRACT-EMIT",
            asset_id=f"tribe_profile-{self.coach_acronym}",
            input_summary=f"Extracted tribe profile with {len(profile.cultural_artifacts.tribe_slang)} slang terms",
            output_summary=f"tribe_profile.json written to {output_path}",
            decision="emit",
            parent_receipt_id=ingest_receipt_id,
            metadata={
                "output_path": str(output_path),
                "slang_count": len(profile.cultural_artifacts.tribe_slang),
                "jokes_count": len(profile.cultural_artifacts.inside_jokes),
                "heroes_count": len(profile.cultural_artifacts.shared_heroes),
                "enemies_count": len(profile.cultural_artifacts.common_enemies),
            },
        )

        return emit_receipt.receipt_id

    # ──────────────────────────────────────────────────────────
    # Phase A5: VALIDATE
    # ──────────────────────────────────────────────────────────

    def validate(self, profile: TribeProfile) -> list[VolumeQuotaResult]:
        """Spec §Phase A5: Schema-validate against all volume quotas.
        AC3: Any quota unmet → validation fails."""
        return profile.validate_volume_quotas()

    # ──────────────────────────────────────────────────────────
    # Phase A6: CHECKPOINT
    # ──────────────────────────────────────────────────────────

    def checkpoint(
        self,
        profile: TribeProfile,
        quota_results: list[VolumeQuotaResult],
    ) -> dict[str, Any]:
        """Spec §Phase A6: Log counts and update config status."""
        return {
            "status": "complete" if profile.passes_all_volume_quotas() else "failed",
            "cultural_artifacts_count": len(profile.cultural_artifacts.tribe_slang),
            "verbatim_quotes_count": (
                len(profile.emotional_resonance.primary_aspirations)
                + len(profile.emotional_resonance.core_anxieties)
            ),
            "visual_codes_count": len(profile.visual_recognition_codes),
            "depth_distribution": profile.depth_distribution,
            "quota_failures": [
                q.field_name for q in quota_results if not q.passed
            ],
        }

    # ──────────────────────────────────────────────────────────
    # Full Stage A Orchestration
    # ──────────────────────────────────────────────────────────

    def run_stage_a(
        self,
        tribe_dossier: Optional[TribeDossier],
        audience_raw_data: Optional[list[dict[str, Any]]],
        coach_soul: Optional[dict[str, Any]],
        coach_philosophy_brief: Optional[str],
        tshala_sentiment_report: Optional[dict[str, Any]] = None,
    ) -> tuple[TribeProfile, str, list[VolumeQuotaResult]]:
        """Run full Stage A pipeline. Returns (profile, emit_receipt_id, quotas)."""
        # Phase A1: INGEST
        ingest_data = self.ingest(
            tribe_dossier=tribe_dossier,
            audience_raw_data=audience_raw_data,
            coach_soul=coach_soul,
            coach_philosophy_brief=coach_philosophy_brief,
            tshala_sentiment_report=tshala_sentiment_report,
        )

        # Phase A2: RESEARCH PLANNING
        _research_plan = self.plan_research(ingest_data)

        # Phase A3: CULTURAL HARVESTING
        dossier = ingest_data["tribe_dossier"]
        raw_data = ingest_data["audience_raw_data"]

        cultural = self.harvest_cultural_artifacts(dossier, raw_data)
        humor = self.harvest_humor_profile(dossier, raw_data)
        emotional = self.harvest_emotional_resonance(dossier, raw_data)
        visuals = self.harvest_visual_codes(dossier, raw_data)
        anti_asp = self.harvest_anti_aspirational_markers(dossier, raw_data)

        # Build profile
        profile = TribeProfile(
            coach_id=self.coach_id,
            coach_acronym=self.coach_acronym,
            cultural_artifacts=cultural,
            humor_profile=humor,
            emotional_resonance=emotional,
            visual_recognition_codes=visuals,
            anti_aspirational_markers=anti_asp,
        )

        # Phase A4: EMIT
        emit_receipt_id = self.emit(
            profile=profile,
            ingest_receipt_id=ingest_data["ingest_receipt_id"],
        )

        # Phase A5: VALIDATE
        quota_results = self.validate(profile)

        # Phase A6: CHECKPOINT
        _checkpoint = self.checkpoint(profile, quota_results)

        return profile, emit_receipt_id, quota_results
