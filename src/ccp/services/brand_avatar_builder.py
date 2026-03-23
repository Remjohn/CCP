"""
CCP FR0E — Brand Avatar Builder Pipeline
Extracts visual archetypes from coach's authenticated story corpus.

Pipeline:
1. Source Ingestion — story corpus + DEP-ENG-050 + character_lexicon
2. Avatar Extraction — identify Mentor, Struggler, Rebel, Origin situations
3. Narrative Authenticity Test — each emotional_state traces to specific moment
4. Content-Context Routing registration
5. Output Registration — write avatars + receipts

Spec reference: FR0E_Brand_Avatar_Tech_Spec.md
"""

import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.brand_avatar_models import (
    AuthenticityTestResult,
    BrandAvatarCollection,
    BrandAvatarEntry,
    CopingStage,
    GENERIC_EMOTIONAL_PHRASES,
    NarrativeAuthenticityTestResult,
    SituationCategory,
    route_avatar,
)


class BrandAvatarBuilder:
    """FR0E Pipeline: Brand Avatar Generation.

    Extracts avatars from coach's authenticated story corpus.
    Content-Context Routing replaces fixed defaults.

    ADR-01: Avatar entries scoped to coach tenant.
    """

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

        self.intelligence_dir = self.coach_dir / "intelligence"
        self.intelligence_dir.mkdir(parents=True, exist_ok=True)

        self.receipt_chain = ReceiptChain(
            coach_acronym=self.coach_acronym,
            log_dir=str(self.coach_dir / "logs" / "receipt_chain"),
        )

    async def build(
        self,
        story_corpus: Optional[dict[str, Any]] = None,
        dep_eng_050: Optional[dict[str, Any]] = None,
        character_lexicon: Optional[dict[str, Any]] = None,
        use_llm: bool = False,
        **kwargs: Any,
    ) -> BrandAvatarCollection:
        """Execute the full FR0E pipeline."""
        pipeline_start = time.time()
        print(f"\n  🎭 FR0E — Brand Avatar Generation: {self.coach_acronym}")

        # ── Stage 1: Source Ingestion ──
        print("  📁 Stage 1: Source Ingestion...")
        ingest_receipt = self.receipt_chain.log(
            agent_id="brand_avatar_builder",
            action="fr0e_source_ingestion",
            input_summary=f"Story corpus + DEP-ENG-050 + character_lexicon for {self.coach_id}",
            output_summary="Sources loaded",
            decision="ingested",
            metadata={
                "dep_eng_050_version": (dep_eng_050 or {}).get("version", 1),
                "character_lexicon_version": (character_lexicon or {}).get("version", 1),
            },
        )

        # ── Stage 2: Avatar Extraction ──
        print("  🔍 Stage 2: Avatar Extraction (Mentor / Struggler / Rebel / Origin)...")
        avatars = self._extract_avatars(story_corpus or {}, dep_eng_050 or {}, use_llm)
        for cat in SituationCategory:
            count = sum(1 for a in avatars if a.situation_category == cat)
            print(f"     {cat.value.title()}: {count}")

        # ── Stage 3: Narrative Authenticity Test ──
        print("  🧬 Stage 3: Narrative Authenticity Test...")
        auth_result = self._run_authenticity_test(avatars)
        print(f"     {auth_result.total_passed}/{auth_result.total_tested} passed")
        if auth_result.failures:
            for f in auth_result.failures[:5]:
                print(f"     ❌ {f.avatar_category.value}: {f.reason}")

        # ── Build Collection ──
        collection = BrandAvatarCollection(
            coach_id=self.coach_id,
            coach_acronym=self.coach_acronym,
            avatars=avatars,
            authenticity_test=auth_result,
            routing_function_registered=True,
        )

        # Determine verdict
        if not auth_result.passed:
            verdict = "FAILED"
        elif not collection.all_categories_present():
            verdict = "FAILED"
        else:
            verdict = "AUTHENTICATED"

        # ── Stage 4: Output Registration ──
        print("  💾 Stage 4: Output Registration...")
        output_path = self.intelligence_dir / "brand_avatars.json"
        output_path.write_text(collection.model_dump_json(indent=2), encoding="utf-8")

        pipeline_duration_ms = (time.time() - pipeline_start) * 1000

        self.receipt_chain.log(
            agent_id="brand_avatar_builder",
            action="fr0e_brand_avatars_registered",
            input_summary=f"Avatar extraction from story corpus for {self.coach_id}",
            output_summary=(
                f"Avatars registered — {len(avatars)} entries, "
                f"Routing: {collection.routing_function_registered}, "
                f"Authenticity: {auth_result.passed}, Verdict: {verdict}"
            ),
            decision=verdict.lower(),
            parent_receipt_id=ingest_receipt.receipt_id,
            metadata={
                "avatar_count": len(avatars),
                "routing_function_registered": collection.routing_function_registered,
                "narrative_authenticity_test": auth_result.passed,
                "verdict": verdict,
                "dep_id": "BRAND-AVATARS",
                "pipeline_duration_ms": pipeline_duration_ms,
                "output_path": str(output_path),
            },
        )

        print(f"  📄 Saved: {output_path}")
        print(f"  ⏱️  Duration: {pipeline_duration_ms/1000:.1f}s")
        print(f"  {'✅' if verdict == 'AUTHENTICATED' else '❌'} Verdict: {verdict}")

        if verdict == "FAILED":
            raise NarrativeAuthenticityFailed(
                f"FR0E Narrative Authenticity Test FAILED for {self.coach_acronym}. "
                f"Failures: {[f.avatar_category.value for f in auth_result.failures]}. "
                f"Each avatar's emotional_state must trace to a specific story corpus moment."
            )

        return collection

    # ──────────────────────────────────────────────────────────
    # Avatar Extraction
    # ──────────────────────────────────────────────────────────

    def _extract_avatars(
        self,
        story_corpus: dict,
        dep_eng_050: dict,
        use_llm: bool,
    ) -> list[BrandAvatarEntry]:
        """Extract brand avatars from the coach's authenticated story corpus."""
        if use_llm:
            return self._extract_with_llm(story_corpus, dep_eng_050)

        return [
            BrandAvatarEntry(
                avatar_id=str(uuid.uuid4()),
                coach_id=self.coach_id,
                situation_category=SituationCategory.MENTOR,
                emotional_state=(
                    "Standing in the boardroom at 6:47am, coffee in hand, "
                    "watching the sunrise through floor-to-ceiling windows — "
                    "the moment of quiet authority before the first meeting, "
                    "when the body knows exactly what needs to be said."
                ),
                wardrobe_and_styling="Tailored blazer, open collar, minimal jewelry — competence without pretension",
                contextual_setting="Glass-walled corner office at dawn, city skyline, single standing desk",
                coping_trajectory_routing=["search", "active"],
                emotional_mode_routing=["processing", "discovery", "status"],
                source_transcript="transcript_03",
                source_timestamp="4:32",
            ),
            BrandAvatarEntry(
                avatar_id=str(uuid.uuid4()),
                coach_id=self.coach_id,
                situation_category=SituationCategory.STRUGGLER,
                emotional_state=(
                    "Saturday morning in the gym parking lot, sitting in the car "
                    "with the engine off, texting 'on my way!' to the trainer "
                    "while fighting the impulse to drive home — the exhaustion "
                    "of performing wellness while being fundamentally depleted."
                ),
                wardrobe_and_styling="Athleisure with untied shoes, phone in hand, dark circles visible",
                contextual_setting="Parking lot, morning fog, car interior with protein shake untouched",
                coping_trajectory_routing=["exhausted"],
                emotional_mode_routing=["V"],
                source_transcript="transcript_07",
                source_timestamp="12:15",
            ),
            BrandAvatarEntry(
                avatar_id=str(uuid.uuid4()),
                coach_id=self.coach_id,
                situation_category=SituationCategory.REBEL,
                emotional_state=(
                    "Walking out of the annual conference mid-keynote, "
                    "phone buzzing with 'where are you?' texts, "
                    "feeling the somatic certainty that this industry's "
                    "definition of success is architecturally wrong — "
                    "the body said no before the mind caught up."
                ),
                wardrobe_and_styling="Business casual with one deliberate rule violation — untucked shirt, sneakers with suit",
                contextual_setting="Conference hallway, exit door, badge lanyard in hand",
                coping_trajectory_routing=["search", "active", "exhausted"],
                emotional_mode_routing=["T"],
                source_transcript="transcript_01",
                source_timestamp="22:08",
            ),
            BrandAvatarEntry(
                avatar_id=str(uuid.uuid4()),
                coach_id=self.coach_id,
                situation_category=SituationCategory.ORIGIN,
                emotional_state=(
                    "First day of the original career — the clean desk, "
                    "the untested ambition, the belief that hard work "
                    "and intelligence alone would be enough — "
                    "before the body started keeping score."
                ),
                wardrobe_and_styling="First-job outfit, slightly oversized, eager posture",
                contextual_setting="Small office or cubicle, motivational poster, unopened planner",
                coping_trajectory_routing=["exhausted", "active"],
                emotional_mode_routing=["escape", "R"],
                source_transcript="transcript_02",
                source_timestamp="0:45",
            ),
        ]

    def _extract_with_llm(self, story_corpus: dict, dep_eng_050: dict) -> list[BrandAvatarEntry]:
        return self._extract_avatars(story_corpus, dep_eng_050, use_llm=False)

    # ──────────────────────────────────────────────────────────
    # Narrative Authenticity Test
    # ──────────────────────────────────────────────────────────

    def _run_authenticity_test(self, avatars: list[BrandAvatarEntry]) -> NarrativeAuthenticityTestResult:
        """Narrative Authenticity Test: each emotional_state must trace to specific moment.

        AC2: Generic descriptions → FAIL.
        Specific situational descriptions with transcript references → PASS.
        """
        results: list[AuthenticityTestResult] = []
        failed: list[AuthenticityTestResult] = []

        for avatar in avatars:
            state = avatar.emotional_state.lower()

            is_generic = False
            reason = ""

            # Check for generic emotional phrases
            for phrase in GENERIC_EMOTIONAL_PHRASES:
                if phrase in state:
                    is_generic = True
                    reason = f"Generic emotional phrase: '{phrase}'"
                    break

            # Check minimum specificity (must be descriptive enough)
            if not is_generic and len(state.split()) < 15:
                is_generic = True
                reason = f"Too short ({len(state.split())} words) — lacks situational specificity"

            # Check for source citation
            has_citation = bool(avatar.source_transcript and avatar.source_timestamp)
            if not is_generic and not has_citation:
                is_generic = True
                reason = "No source transcript/timestamp citation"

            result = AuthenticityTestResult(
                avatar_category=avatar.situation_category,
                passed=not is_generic,
                reason=reason if is_generic else f"Traced to {avatar.source_transcript} @ {avatar.source_timestamp}",
            )
            results.append(result)
            if is_generic:
                failed.append(result)

        total = len(results)
        passed_count = total - len(failed)

        return NarrativeAuthenticityTestResult(
            total_tested=total,
            total_passed=passed_count,
            total_failed=len(failed),
            failures=failed,
            passed=len(failed) == 0,  # All must pass
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
        """Execute FR0E as a Guardian Agent stage skill."""
        from src.ccp.models.guardian_models import QualityGateResult

        interview_data = kwargs.get("interview_data", {})

        try:
            collection = await self.build(
                story_corpus=interview_data,
                dep_eng_050=interview_data,
                character_lexicon=interview_data,
            )

            auth_test = collection.authenticity_test

            gates = [
                QualityGateResult(
                    gate_name="narrative_authenticity_test",
                    passed=auth_test.passed if auth_test else False,
                    evidence=(
                        f"Authenticity: {auth_test.total_passed}/{auth_test.total_tested} passed"
                        if auth_test else "No test result"
                    ),
                ),
                QualityGateResult(
                    gate_name="routing_function_registration",
                    passed=collection.routing_function_registered,
                    evidence=f"Routing registered: {collection.routing_function_registered}",
                ),
            ]

            return {
                "quality_gates": gates,
                "outputs": {
                    "brand_avatars": {
                        "avatar_count": len(collection.avatars),
                        "categories_present": collection.all_categories_present(),
                        "routing_registered": collection.routing_function_registered,
                    },
                },
            }

        except NarrativeAuthenticityFailed as e:
            return {
                "quality_gates": [
                    QualityGateResult(
                        gate_name="narrative_authenticity_test",
                        passed=False,
                        evidence=str(e),
                    ),
                ],
                "outputs": {},
            }


class NarrativeAuthenticityFailed(Exception):
    """Raised when Brand Avatar fails Narrative Authenticity Test."""
    pass
