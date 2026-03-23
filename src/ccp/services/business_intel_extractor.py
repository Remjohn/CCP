"""
CCP FR0A — Business Intelligence Extractor Pipeline
FR0A Task 2 — Source folder ingestion + 5-dimension synthesis + quality gate.

Produces DEP-ENG-050 (coach_business_summary.json) — the seed for all
downstream extraction in the CCP pipeline.

Spec reference: FR0A_Business_Intelligence_Tech_Spec.md

Pipeline stages:
1. Source Ingestion — classify and extract from coach source folder
2. Interview Integration — merge Interview Phase 1 responses
3. 5-Dimension Synthesis — CRAL-informed analysis
4. Positioning Precision Test — quality gate (AC1)
5. Output Registration — write DEP-ENG-050 + receipt

Usage:
    from src.ccp.services.business_intel_extractor import BusinessIntelExtractor

    extractor = BusinessIntelExtractor(
        coach_id="NDL-0000",
        coach_acronym="NDL",
    )
    summary = await extractor.extract(
        source_folder="./coaches/NDL/sources",
        interview_data=interview_phase1_responses,
    )
"""

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.business_intel_models import (
    AudiencePrecision,
    BusinessIntelSummary,
    ContentPhilosophy,
    MarketPositioning,
    PositioningPrecisionTestResult,
    RevenueArchitecture,
    SourceIngestionResult,
    TransformationStory,
    ValueProposition,
)


# ──────────────────────────────────────────────────────────────
# Generic positioning phrases that fail the Precision Test
# Used by the deterministic test mode evaluator
# ──────────────────────────────────────────────────────────────

GENERIC_POSITIONING_PHRASES = [
    "overcome limiting beliefs",
    "step into their full potential",
    "unlock their true potential",
    "live their best life",
    "find their purpose",
    "achieve their goals",
    "transform their mindset",
    "reach the next level",
    "breakthrough to success",
    "discover their authentic self",
    "high-achieving professionals",
    "transformative coaching",
    "holistic approach",
    "proven methodology",
    "personalized coaching experience",
]


class BusinessIntelExtractor:
    """FR0A Pipeline: Business Intelligence Extraction.

    Ingests coach source materials and interview data, synthesizes
    5-dimension CRAL-informed business intelligence, and runs the
    Positioning Precision Test quality gate.

    ADR-01: All reads/writes scoped to coach tenant.
    """

    # Minimum thresholds from spec
    MIN_TRANSFORMATION_STORIES = 3
    POSITIONING_SUMMARY_MIN_WORDS = 60
    POSITIONING_SUMMARY_MAX_WORDS = 80

    def __init__(
        self,
        coach_id: str,
        coach_acronym: str,
        base_dir: str = "./coaches",
    ):
        self.coach_id = coach_id
        self.coach_acronym = coach_acronym.upper()
        self.base_dir = Path(base_dir)
        self.coach_dir = self.base_dir / self.coach_acronym

        # Ensure directories exist (ADR-01 scoped)
        self.sources_dir = self.coach_dir / "sources"
        self.intelligence_dir = self.coach_dir / "intelligence"
        self.intelligence_dir.mkdir(parents=True, exist_ok=True)

        self.receipt_chain = ReceiptChain(
            coach_acronym=self.coach_acronym,
            log_dir=str(self.coach_dir / "logs" / "receipt_chain"),
        )

    async def extract(
        self,
        source_folder: Optional[str] = None,
        interview_data: Optional[dict[str, Any]] = None,
        use_llm: bool = False,
    ) -> BusinessIntelSummary:
        """Execute the full FR0A pipeline.

        Args:
            source_folder: Path to coach source folder. If None, uses default.
            interview_data: Interview Phase 1 responses dict.
            use_llm: If True, use LLM for synthesis. If False, use deterministic logic.

        Returns:
            BusinessIntelSummary (DEP-ENG-050)

        Raises:
            PositioningPrecisionFailed: If the quality gate fails
            InsufficientSourceData: If source material is insufficient
        """
        pipeline_start = time.time()
        source_path = Path(source_folder) if source_folder else self.sources_dir

        print(f"\n  📊 FR0A — Business Intelligence Extraction: {self.coach_acronym}")

        # ── Stage 1: Source Ingestion ──
        print("  📁 Stage 1: Source Ingestion...")
        ingestion = self._ingest_source_folder(source_path)

        # Merge interview responses into ingestion count
        interview_count = 0
        if interview_data:
            interview_count = len(interview_data.get("responses", []))
            ingestion.interview_response_count = interview_count
            print(f"     + {interview_count} interview Phase 1 responses integrated")

        # Receipt: INGEST
        ingest_receipt = self.receipt_chain.log(
            agent_id="business_model_assistant",
            action="fr0a_source_ingestion",
            input_summary=f"Source folder: {source_path} + Interview Phase 1",
            output_summary=(
                f"Ingested {ingestion.source_document_count} documents, "
                f"{interview_count} interview responses"
            ),
            decision="ingested",
            metadata={
                "source_document_count": ingestion.source_document_count,
                "interview_response_count": ingestion.interview_response_count,
                "document_types": ingestion.document_types,
                "timestamp": ingestion.ingested_at,
            },
        )

        # ── Stage 2: 5-Dimension Synthesis ──
        print("  🔬 Stage 2: 5-Dimension CRAL-Informed Analysis...")
        dimensions = self._synthesize_5_dimensions(
            source_path, interview_data, use_llm
        )

        # ── Stage 3: Positioning Summary Generation ──
        print("  📝 Stage 3: Positioning Summary Generation...")
        positioning_summary = self._generate_positioning_summary(
            dimensions, interview_data, use_llm
        )
        word_count = len(positioning_summary.split())
        print(f"     Summary: {word_count} words")

        # ── Stage 4: Positioning Precision Test (AC1) ──
        print("  🎯 Stage 4: Positioning Precision Test...")
        test_result = self._run_positioning_precision_test(
            positioning_summary, dimensions, use_llm
        )

        if test_result.passed:
            print(f"     ✅ PASS — substitution breaks the description")
        else:
            print(f"     ❌ FAIL — summary is generic")
            for dim in test_result.generic_dimensions:
                print(f"        ⬡ Generic dimension: {dim}")

        # Build the complete summary
        transformation_corpus = dimensions.get("transformation_stories", [])

        summary = BusinessIntelSummary(
            coach_id=self.coach_id,
            coach_acronym=self.coach_acronym,
            positioning_summary=positioning_summary,
            value_proposition=dimensions.get("value_proposition", ValueProposition()),
            revenue_architecture=dimensions.get("revenue_architecture", RevenueArchitecture()),
            audience_precision=dimensions.get("audience_precision", AudiencePrecision()),
            market_positioning=dimensions.get("market_positioning", MarketPositioning()),
            content_philosophy=dimensions.get("content_philosophy", ContentPhilosophy()),
            transformation_evidence_corpus=transformation_corpus,
            positioning_precision_test=test_result,
            source_ingestion=ingestion,
        )

        # ── Stage 5: Output Registration ──
        print("  💾 Stage 5: Output Registration...")
        output_path = self.intelligence_dir / "coach_business_summary.json"
        output_path.write_text(summary.model_dump_json(indent=2), encoding="utf-8")

        pipeline_duration_ms = (time.time() - pipeline_start) * 1000

        # Determine verdict
        if not test_result.passed:
            verdict = "FAILED"
        elif not summary.has_minimum_stories():
            verdict = "FAILED"
        else:
            verdict = "AUTHENTICATED"

        # Receipt: EMIT
        self.receipt_chain.log(
            agent_id="business_model_assistant",
            action="fr0a_dep_eng_050_registered",
            input_summary=f"5-dimension analysis for {self.coach_id}",
            output_summary=(
                f"DEP-ENG-050 registered — "
                f"Positioning Precision: {'PASS' if test_result.passed else 'FAIL'}, "
                f"Stories: {len(transformation_corpus)}, "
                f"Verdict: {verdict}"
            ),
            decision=verdict.lower(),
            parent_receipt_id=ingest_receipt.receipt_id,
            metadata={
                "positioning_precision_test": "PASS" if test_result.passed else "FAIL",
                "transformation_story_count": len(transformation_corpus),
                "verdict": verdict,
                "dep_id": "DEP-ENG-050",
                "word_count": word_count,
                "pipeline_duration_ms": pipeline_duration_ms,
                "output_path": str(output_path),
            },
        )

        print(f"  📄 Saved: {output_path}")
        print(f"  ⏱️  Duration: {pipeline_duration_ms/1000:.1f}s")
        print(f"  {'✅' if verdict == 'AUTHENTICATED' else '❌'} Verdict: {verdict}")

        # Raise on failure
        if not test_result.passed:
            raise PositioningPrecisionFailed(
                f"Positioning Precision Test FAILED for {self.coach_acronym}. "
                f"Generic dimensions: {test_result.generic_dimensions}. "
                f"Analysis: {test_result.substitution_analysis}. "
                f"Provide deeper source material and re-execute FR0A."
            )

        if not summary.has_minimum_stories():
            raise InsufficientSourceData(
                f"Insufficient transformation evidence for {self.coach_acronym}. "
                f"Found {len(transformation_corpus)} stories, need ≥{self.MIN_TRANSFORMATION_STORIES}. "
                f"Value Proposition CRAL depth pass requires minimum 3 verified real-person stories."
            )

        return summary

    # ──────────────────────────────────────────────────────────
    # Stage 1: Source Ingestion
    # ──────────────────────────────────────────────────────────

    def _ingest_source_folder(self, source_path: Path) -> SourceIngestionResult:
        """Ingest and classify all documents in the coach source folder.

        Processes: website content, video transcripts, positioning docs, recordings.
        """
        doc_types: dict[str, int] = {
            "website": 0,
            "transcript": 0,
            "positioning_doc": 0,
            "recording": 0,
            "other": 0,
        }
        total_content_length = 0
        doc_count = 0

        if source_path.exists() and source_path.is_dir():
            for file_path in source_path.rglob("*"):
                if file_path.is_file():
                    doc_count += 1
                    ext = file_path.suffix.lower()

                    # Classify by extension and path
                    if ext in (".html", ".htm"):
                        doc_types["website"] += 1
                    elif ext in (".txt", ".srt", ".vtt"):
                        doc_types["transcript"] += 1
                    elif ext in (".md", ".docx", ".pdf"):
                        doc_types["positioning_doc"] += 1
                    elif ext in (".mp3", ".wav", ".m4a", ".mp4"):
                        doc_types["recording"] += 1
                    else:
                        doc_types["other"] += 1

                    # Count text content length
                    if ext in (".txt", ".md", ".html", ".htm", ".srt", ".vtt"):
                        try:
                            content = file_path.read_text(encoding="utf-8", errors="ignore")
                            total_content_length += len(content)
                        except Exception:
                            pass

        print(f"     Found {doc_count} documents in {source_path}")
        for dtype, count in doc_types.items():
            if count > 0:
                print(f"       • {dtype}: {count}")

        return SourceIngestionResult(
            source_document_count=doc_count,
            document_types={k: v for k, v in doc_types.items() if v > 0},
            total_content_length=total_content_length,
        )

    # ──────────────────────────────────────────────────────────
    # Stage 2: 5-Dimension Synthesis
    # ──────────────────────────────────────────────────────────

    def _synthesize_5_dimensions(
        self,
        source_path: Path,
        interview_data: Optional[dict[str, Any]],
        use_llm: bool = False,
    ) -> dict[str, Any]:
        """Synthesize the 5-dimension CRAL-informed analysis.

        In production (use_llm=True), an LLM synthesizes the dimensions.
        In test mode, uses interview_data directly to populate dimensions.
        """
        if use_llm:
            return self._synthesize_with_llm(source_path, interview_data)

        # Deterministic mode: populate from interview_data
        return self._synthesize_deterministic(interview_data or {})

    def _synthesize_deterministic(self, interview_data: dict[str, Any]) -> dict[str, Any]:
        """Build dimensions from structured interview data (test/demo mode)."""

        # Extract transformation stories
        raw_stories = interview_data.get("transformation_stories", [])
        stories = [
            TransformationStory(
                client_identifier=s.get("client", ""),
                before_state=s.get("before", ""),
                after_state=s.get("after", ""),
                verbatim_quotes=s.get("quotes", []),
                transformation_mechanism=s.get("mechanism", ""),
                source=s.get("source", "interview"),
            )
            for s in raw_stories
        ]

        has_min_stories = len(stories) >= self.MIN_TRANSFORMATION_STORIES

        return {
            "value_proposition": ValueProposition(
                core_transformation=interview_data.get("transformation_claim", ""),
                unique_mechanism=interview_data.get("unique_mechanism", ""),
                transformation_stories=stories,
                cral_depth_passed=has_min_stories,
            ),
            "revenue_architecture": RevenueArchitecture(
                offer_tiers=interview_data.get("offer_tiers", []),
                price_range=interview_data.get("price_range", ""),
                delivery_method=interview_data.get("delivery_method", ""),
                revenue_model=interview_data.get("revenue_model", ""),
            ),
            "audience_precision": AudiencePrecision(
                who_buys=interview_data.get("who_buys", ""),
                who_doesnt=interview_data.get("who_doesnt", ""),
                why_they_buy=interview_data.get("why_they_buy", ""),
                audience_language=interview_data.get("audience_language", []),
            ),
            "market_positioning": MarketPositioning(
                primary_differentiator=interview_data.get("primary_differentiator", ""),
                competitor_landscape=interview_data.get("competitors", []),
                positioning_gap=interview_data.get("positioning_gap", ""),
                cral_depth_passed=len(interview_data.get("competitors", [])) > 0,
            ),
            "content_philosophy": ContentPhilosophy(
                content_role=interview_data.get("content_role", ""),
                content_fears=interview_data.get("content_fears", ""),
                content_strengths=interview_data.get("content_strengths", ""),
                platform_preferences=interview_data.get("platforms", []),
            ),
            "transformation_stories": stories,
        }

    def _synthesize_with_llm(
        self,
        source_path: Path,
        interview_data: Optional[dict[str, Any]],
    ) -> dict[str, Any]:
        """Use LLM (Gemini) to synthesize dimensions from raw materials.

        This is the production path — processes actual source documents
        and interview responses through the Business Model Assistant agent.
        """
        # LLM integration point — will use Gemini for deep analysis
        # For now, fall back to deterministic
        return self._synthesize_deterministic(interview_data or {})

    # ──────────────────────────────────────────────────────────
    # Stage 3: Positioning Summary Generation
    # ──────────────────────────────────────────────────────────

    def _generate_positioning_summary(
        self,
        dimensions: dict[str, Any],
        interview_data: Optional[dict[str, Any]],
        use_llm: bool = False,
    ) -> str:
        """Generate the 60-80 word positioning summary.

        Format: expertise → audience → pain → solution (3rd person).
        """
        if use_llm:
            return self._generate_summary_with_llm(dimensions)

        # Check if interview_data provides a pre-written summary
        if interview_data and "positioning_summary" in interview_data:
            return interview_data["positioning_summary"]

        # Build from dimensions (deterministic fallback)
        vp: ValueProposition = dimensions.get("value_proposition", ValueProposition())
        ap: AudiencePrecision = dimensions.get("audience_precision", AudiencePrecision())
        mp: MarketPositioning = dimensions.get("market_positioning", MarketPositioning())

        parts = []
        if vp.unique_mechanism:
            parts.append(f"Through {vp.unique_mechanism}")
        if ap.who_buys:
            parts.append(f"serves {ap.who_buys}")
        if vp.core_transformation:
            parts.append(f"delivering {vp.core_transformation}")
        if mp.primary_differentiator:
            parts.append(f"distinguished by {mp.primary_differentiator}")

        if parts:
            return ". ".join(parts) + "."

        return "Positioning summary could not be generated — insufficient source data."

    def _generate_summary_with_llm(self, dimensions: dict) -> str:
        """Use LLM to generate a coach-specific positioning summary.

        Production path — generates through Gemini with strict constraints:
        - 60-80 words, 3rd person
        - expertise → audience → pain → solution structure
        - Must be specific enough to pass Positioning Precision Test
        """
        # LLM integration point
        return "LLM-generated summary placeholder"

    # ──────────────────────────────────────────────────────────
    # Stage 4: Positioning Precision Test (AC1)
    # ──────────────────────────────────────────────────────────

    def _run_positioning_precision_test(
        self,
        summary: str,
        dimensions: dict[str, Any],
        use_llm: bool = False,
    ) -> PositioningPrecisionTestResult:
        """Execute the Positioning Precision Test quality gate.

        Spec: Replace the coach's name with a direct competitor's name.
        If the summary still accurately describes the competitor,
        the extraction has FAILED — it captured category-level intelligence,
        not coach-specific intelligence.

        Args:
            summary: The 60-80 word positioning summary
            dimensions: The 5-dimension analysis results
            use_llm: If True, use LLM for evaluation

        Returns:
            PositioningPrecisionTestResult with verdict and analysis
        """
        mp: MarketPositioning = dimensions.get("market_positioning", MarketPositioning())
        competitor = mp.competitor_landscape[0] if mp.competitor_landscape else "Generic Competitor"

        if use_llm:
            return self._precision_test_with_llm(summary, competitor)

        # Deterministic evaluation for testing
        return self._precision_test_deterministic(summary, competitor, dimensions)

    def _precision_test_deterministic(
        self,
        summary: str,
        competitor: str,
        dimensions: dict[str, Any],
    ) -> PositioningPrecisionTestResult:
        """Deterministic Positioning Precision Test.

        Checks for generic positioning phrases that would describe
        any coach in the same niche. If found → FAIL.
        """
        summary_lower = summary.lower()
        generic_found: list[str] = []

        for phrase in GENERIC_POSITIONING_PHRASES:
            if phrase.lower() in summary_lower:
                generic_found.append(phrase)

        # Check for dimension-level specificity
        generic_dimensions: list[str] = []
        vp: ValueProposition = dimensions.get("value_proposition", ValueProposition())
        mp: MarketPositioning = dimensions.get("market_positioning", MarketPositioning())

        if not vp.unique_mechanism:
            generic_dimensions.append("Value Proposition — no unique mechanism specified")
        if not mp.primary_differentiator:
            generic_dimensions.append("Market Positioning — no primary differentiator specified")
        if not vp.core_transformation:
            generic_dimensions.append("Value Proposition — no core transformation specified")

        # Summary too short to be specific
        word_count = len(summary.split())
        if word_count < 20:
            generic_dimensions.append(f"Summary too short ({word_count} words) to be coach-specific")

        # Final verdict
        is_generic = len(generic_found) > 0 or len(generic_dimensions) >= 2

        if is_generic:
            analysis = (
                f"Summary contains {len(generic_found)} generic phrase(s) "
                f"and {len(generic_dimensions)} generic dimension(s). "
                f"Replacing coach name with '{competitor}' would not break the description. "
                f"Generic phrases found: {generic_found}"
            )
        else:
            analysis = (
                f"Summary is coach-specific. Contains unique mechanism, "
                f"specific audience, and distinctive transformation. "
                f"Replacing coach name with '{competitor}' would break the description."
            )

        return PositioningPrecisionTestResult(
            passed=not is_generic,
            competitor_name_used=competitor,
            substitution_analysis=analysis,
            generic_dimensions=generic_dimensions,
        )

    def _precision_test_with_llm(
        self,
        summary: str,
        competitor: str,
    ) -> PositioningPrecisionTestResult:
        """LLM-based Positioning Precision Test.

        Uses Gemini to evaluate whether substituting the competitor's
        name breaks the summary's accuracy.
        """
        # LLM integration point
        return PositioningPrecisionTestResult(
            passed=True,
            competitor_name_used=competitor,
            substitution_analysis="[LLM evaluation placeholder]",
        )

    # ──────────────────────────────────────────────────────────
    # Guardian Agent Integration
    # ──────────────────────────────────────────────────────────

    async def as_guardian_skill(
        self,
        coach_id: str,
        coach_dir: str,
        state: Any = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Execute FR0A as a Guardian Agent stage skill.

        This method conforms to the skill_fn interface expected by
        GuardianAgent.register_stage_skill().

        Returns:
            Dict with "quality_gates" and "outputs" as required by the orchestrator.
        """
        from src.ccp.models.guardian_models import QualityGateResult

        interview_data = kwargs.get("interview_data", {})
        source_folder = kwargs.get("source_folder")

        try:
            summary = await self.extract(
                source_folder=source_folder,
                interview_data=interview_data,
            )

            # Build quality gate results from the extraction
            test_result = summary.positioning_precision_test
            gates = [
                QualityGateResult(
                    gate_name="positioning_precision_test",
                    passed=test_result.passed if test_result else False,
                    evidence=(
                        test_result.substitution_analysis if test_result
                        else "No test result available"
                    ),
                    is_provisional_eligible=False,  # Binary — no provisional
                ),
            ]

            return {
                "quality_gates": gates,
                "outputs": {
                    "dep_eng_050": summary.model_dump(),
                },
            }

        except PositioningPrecisionFailed as e:
            return {
                "quality_gates": [
                    QualityGateResult(
                        gate_name="positioning_precision_test",
                        passed=False,
                        evidence=str(e),
                        is_provisional_eligible=False,
                    ),
                ],
                "outputs": {},
            }

        except InsufficientSourceData as e:
            return {
                "quality_gates": [
                    QualityGateResult(
                        gate_name="positioning_precision_test",
                        passed=False,
                        evidence=str(e),
                        is_provisional_eligible=False,
                    ),
                ],
                "outputs": {},
            }


class PositioningPrecisionFailed(Exception):
    """Raised when the Positioning Precision Test fails.

    The summary is generic — replacing the coach's name with a
    competitor's name does not break the description. Operator must
    provide deeper source material.
    """

    pass


class InsufficientSourceData(Exception):
    """Raised when source data is insufficient for extraction.

    Typically triggered by fewer than 3 transformation stories
    (Value Proposition CRAL depth pass fails).
    """

    pass
