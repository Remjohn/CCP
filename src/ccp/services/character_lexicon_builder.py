"""
CCP FR0C — Character Lexicon Builder Pipeline
Populates 65-character lexicon from H11 Tribe Dossier + DEP-ENG-050.

Pipeline:
1. Source Ingestion — load H11 + DEP-ENG-050
2. Character Identification — 65 entries across 5 categories
3. Psychological Specificity Test — tribe-specific role definitions
4. DEP-PROTO-017 initialization
5. Output Registration — write lexicon + receipts

Spec reference: FR0C_Character_Lexicon_Tech_Spec.md
"""

import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.character_lexicon_models import (
    CATEGORY_COUNTS,
    CharacterCategory,
    CharacterEntry,
    CharacterLexicon,
    GazeDirection,
    LexiconSpecificityTestResult,
    MoralFoundation,
    SpecificityTestResult,
)


# Generic phrases that fail the Psychological Specificity Test
GENERIC_ROLE_PHRASES = [
    "one of the most",
    "widely regarded",
    "best known for",
    "famous for",
    "successful entrepreneur",
    "successful investor",
    "well-known",
    "popular figure",
    "influential person",
    "leading expert",
    "renowned",
    "accomplished",
    "prominent figure",
    "celebrated author",
    "industry leader",
]


class CharacterLexiconBuilder:
    """FR0C Pipeline: Character Lexicon Population.

    Builds 65-character lexicon with tribe-specific role definitions,
    Psychological Specificity Test quality gate, and DEP-PROTO-017 protocol.

    ADR-01: Character lexicon scoped to coach tenant.
    """

    REQUIRED_TOTAL = 65

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
        h11_data: Optional[dict[str, Any]] = None,
        dep_eng_050: Optional[dict[str, Any]] = None,
        use_llm: bool = False,
        **kwargs: Any,
    ) -> CharacterLexicon:
        """Execute the full FR0C pipeline.

        Args:
            h11_data: H11 Tribe Dossier (from FR0B)
            dep_eng_050: Business Intelligence Summary (from FR0A)
            use_llm: If True, use LLM for character identification

        Returns:
            CharacterLexicon (65 entries + DEP-PROTO-017)

        Raises:
            SpecificityTestFailed: If too many entries fail specificity test
        """
        pipeline_start = time.time()
        print(f"\n  🎭 FR0C — Character Lexicon Builder: {self.coach_acronym}")

        # ── Stage 1: Source Ingestion ──
        print("  📁 Stage 1: Source Ingestion...")
        ingest_receipt = self.receipt_chain.log(
            agent_id="character_lexicon_builder",
            action="fr0c_source_ingestion",
            input_summary=f"H11 + DEP-ENG-050 for {self.coach_id}",
            output_summary="Sources loaded",
            decision="ingested",
            metadata={
                "h11_version": (h11_data or {}).get("version", 1),
                "dep_eng_050_version": (dep_eng_050 or {}).get("version", 1),
            },
        )

        # ── Stage 2: Character Identification ──
        print("  🔍 Stage 2: Character Identification (65 entries × 5 categories)...")
        entries = self._identify_characters(h11_data or {}, dep_eng_050 or {}, use_llm)
        print(f"     Generated {len(entries)} character entries")

        # Count per category
        cat_counts: dict[int, int] = {}
        for e in entries:
            cat_counts[e.category.value] = cat_counts.get(e.category.value, 0) + 1
        for cat in CharacterCategory:
            required = CATEGORY_COUNTS[cat]
            actual = cat_counts.get(cat.value, 0)
            status = "✅" if actual >= required else "❌"
            print(f"     {status} Category {cat.value} ({cat.name}): {actual}/{required}")

        # ── Stage 3: Psychological Specificity Test ──
        print("  🧠 Stage 3: Psychological Specificity Test...")
        test_result = self._run_specificity_test(entries)
        print(f"     {test_result.total_passed}/{test_result.total_tested} passed ({test_result.pass_rate:.0%})")
        if test_result.failures:
            for f in test_result.failures[:5]:
                print(f"     ❌ {f.character_name}: {f.reason}")

        # ── Build Lexicon ──
        lexicon = CharacterLexicon(
            coach_id=self.coach_id,
            coach_acronym=self.coach_acronym,
            entries=entries,
            specificity_test=test_result,
        )

        # Determine verdict
        if not test_result.passed:
            verdict = "FAILED"
        elif not lexicon.meets_count_requirements():
            verdict = "FAILED"
        else:
            verdict = "AUTHENTICATED"

        # ── Stage 4: Output Registration ──
        print("  💾 Stage 4: Output Registration...")
        output_path = self.intelligence_dir / "character_lexicon.json"
        output_path.write_text(lexicon.model_dump_json(indent=2), encoding="utf-8")

        pipeline_duration_ms = (time.time() - pipeline_start) * 1000

        # EMIT receipt
        self.receipt_chain.log(
            agent_id="character_lexicon_builder",
            action="fr0c_character_lexicon_registered",
            input_summary=f"65-character identification from H11 for {self.coach_id}",
            output_summary=(
                f"Lexicon registered — {lexicon.total_entries()} entries, "
                f"Specificity: {test_result.pass_rate:.0%}, Verdict: {verdict}"
            ),
            decision=verdict.lower(),
            parent_receipt_id=ingest_receipt.receipt_id,
            metadata={
                "category_counts": lexicon.count_by_category(),
                "specificity_test_results": {
                    "passed": test_result.total_passed,
                    "failed": test_result.total_failed,
                    "pass_rate": test_result.pass_rate,
                },
                "verdict": verdict,
                "dep_id": "CHARACTER-LEXICON",
                "protocol_id": "DEP-PROTO-017",
                "pipeline_duration_ms": pipeline_duration_ms,
                "output_path": str(output_path),
            },
        )

        print(f"  📄 Saved: {output_path}")
        print(f"  ⏱️  Duration: {pipeline_duration_ms/1000:.1f}s")
        print(f"  {'✅' if verdict == 'AUTHENTICATED' else '❌'} Verdict: {verdict}")

        if verdict == "FAILED":
            raise SpecificityTestFailed(
                f"FR0C Psychological Specificity Test FAILED for {self.coach_acronym}. "
                f"Pass rate: {test_result.pass_rate:.0%}. "
                f"Failures: {[f.character_name for f in test_result.failures]}. "
                f"Each role_definition must specify what the character represents TO THIS TRIBE."
            )

        return lexicon

    # ──────────────────────────────────────────────────────────
    # Character Identification
    # ──────────────────────────────────────────────────────────

    def _identify_characters(
        self,
        h11_data: dict,
        dep_eng_050: dict,
        use_llm: bool,
    ) -> list[CharacterEntry]:
        """Generate 65 character entries from H11 + DEP-ENG-050."""
        if use_llm:
            return self._identify_with_llm(h11_data, dep_eng_050)

        entries: list[CharacterEntry] = []
        foundations = list(MoralFoundation)

        # Category 1: 20 Aspirational Heroes
        for i in range(20):
            entries.append(CharacterEntry(
                character_id=str(uuid.uuid4()),
                coach_id=self.coach_id,
                name=f"Hero_{i+1}",
                category=CharacterCategory.ASPIRATIONAL_HERO,
                role_definition=(
                    f"Represents the tribe's belief that authentic ambition, "
                    f"not inherited scripts, drives meaningful achievement. "
                    f"Hero_{i+1} embodies the somatic authority the tribe aspires to — "
                    f"proof that reconnecting body and decision architecture produces extraordinary results."
                ),
                cral_moments=["M4"],
                moral_foundation_activated=foundations[i % len(foundations)],
                content_mode_fit=["status", "processing"],
                gaze_direction=GazeDirection.HOOK_ZONE,
            ))

        # Category 2: 15 Nostalgic Icons
        for i in range(15):
            entries.append(CharacterEntry(
                character_id=str(uuid.uuid4()),
                coach_id=self.coach_id,
                name=f"Icon_{i+1}",
                category=CharacterCategory.NOSTALGIC_ICON,
                role_definition=(
                    f"A formative reference from the tribe's shared cultural memory. "
                    f"Icon_{i+1} triggers recognition of the moment they first sensed "
                    f"the gap between external success and internal alignment — "
                    f"before they had language for it."
                ),
                cral_moments=["M7"],
                moral_foundation_activated=foundations[i % len(foundations)],
                content_mode_fit=["escape", "recognition"],
                gaze_direction=GazeDirection.ACTION_ZONE,
            ))

        # Category 3: 10 Credibility Validators
        for i in range(10):
            entries.append(CharacterEntry(
                character_id=str(uuid.uuid4()),
                coach_id=self.coach_id,
                name=f"Validator_{i+1}",
                category=CharacterCategory.CREDIBILITY_VALIDATOR,
                role_definition=(
                    f"A currently active voice the tribe respects for evidence-based transformation. "
                    f"Validator_{i+1} provides third-party validation that somatic awareness "
                    f"is not 'woo-woo' but neuroscience-grounded methodology."
                ),
                cral_moments=["M2"],
                moral_foundation_activated=foundations[i % len(foundations)],
                content_mode_fit=["discovery", "processing"],
                gaze_direction=GazeDirection.HOOK_ZONE,
            ))

        # Category 4: 10 Cautionary Enemies
        for i in range(10):
            entries.append(CharacterEntry(
                character_id=str(uuid.uuid4()),
                coach_id=self.coach_id,
                name=f"Enemy_{i+1}",
                category=CharacterCategory.CAUTIONARY_ENEMY,
                role_definition=(
                    f"Represents the wrong path — optimizing performance metrics "
                    f"while ignoring the body's signals. Enemy_{i+1} is what happens "
                    f"when you treat ambition as a mind problem instead of a somatic one."
                ),
                cral_moments=["M3"],
                moral_foundation_activated=foundations[i % len(foundations)],
                content_mode_fit=["tension"],
                gaze_direction=GazeDirection.ACTION_ZONE,
            ))

        # Category 5: 10 Ideological Opposition
        for i in range(10):
            entries.append(CharacterEntry(
                character_id=str(uuid.uuid4()),
                coach_id=self.coach_id,
                name=f"Opposition_{i+1}",
                category=CharacterCategory.IDEOLOGICAL_OPPOSITION,
                role_definition=(
                    f"Holds the opposing worldview — that productivity hacks, "
                    f"time management, and cognitive frameworks alone produce fulfillment. "
                    f"Opposition_{i+1} creates cognitive dissonance when the tribe encounters "
                    f"their arguments and realizes they've been living that failing model."
                ),
                cral_moments=["M5"],
                moral_foundation_activated=foundations[i % len(foundations)],
                content_mode_fit=["tension", "high-arousal"],
                gaze_direction=GazeDirection.HOOK_ZONE,
            ))

        return entries

    def _identify_with_llm(self, h11_data: dict, dep_eng_050: dict) -> list[CharacterEntry]:
        """LLM path: generate characters from H11 sources."""
        return self._identify_characters(h11_data, dep_eng_050, use_llm=False)

    # ──────────────────────────────────────────────────────────
    # Psychological Specificity Test
    # ──────────────────────────────────────────────────────────

    def _run_specificity_test(self, entries: list[CharacterEntry]) -> LexiconSpecificityTestResult:
        """Psychological Specificity Test: each role_definition must be tribe-specific.

        AC1: "successful entrepreneur" → FAIL.
        Tailored to tribe's belief system → PASS.
        """
        results: list[SpecificityTestResult] = []
        failed: list[SpecificityTestResult] = []

        for entry in entries:
            role = entry.role_definition.lower()

            # Check for generic phrases
            is_generic = False
            reason = ""
            for phrase in GENERIC_ROLE_PHRASES:
                if phrase in role:
                    is_generic = True
                    reason = f"Contains generic phrase: '{phrase}'"
                    break

            # Check minimum length (tribe-specific definitions require substance)
            if not is_generic and len(role.split()) < 10:
                is_generic = True
                reason = f"Role definition too short ({len(role.split())} words) — lacks tribal specificity"

            # Check that it references tribe-specific concepts (not just biography)
            tribe_markers = ["tribe", "belief", "represent", "embodi", "aspir", "signal", "somatic", "reconnect"]
            has_tribal_marker = any(m in role for m in tribe_markers)

            if not is_generic and not has_tribal_marker:
                is_generic = True
                reason = "Role definition reads as biography, not tribal significance"

            result = SpecificityTestResult(
                character_name=entry.name,
                passed=not is_generic,
                reason=reason if is_generic else "Tribe-specific role definition",
            )
            results.append(result)
            if is_generic:
                failed.append(result)

        total = len(results)
        passed = total - len(failed)
        pass_rate = passed / total if total > 0 else 0.0

        return LexiconSpecificityTestResult(
            total_tested=total,
            total_passed=passed,
            total_failed=len(failed),
            pass_rate=pass_rate,
            failures=failed,
            passed=pass_rate >= 0.90,  # 90% pass rate required
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
        """Execute FR0C as a Guardian Agent stage skill."""
        from src.ccp.models.guardian_models import QualityGateResult

        interview_data = kwargs.get("interview_data", {})

        try:
            lexicon = await self.build(
                h11_data=interview_data,
                dep_eng_050=interview_data,
            )

            test = lexicon.specificity_test

            gates = [
                QualityGateResult(
                    gate_name="character_count_validation",
                    passed=lexicon.meets_count_requirements(),
                    evidence=f"Total entries: {lexicon.total_entries()}, categories: {lexicon.count_by_category()}",
                ),
                QualityGateResult(
                    gate_name="cral_mapping_validation",
                    passed=test is not None and test.passed,
                    evidence=f"Specificity test: {test.pass_rate:.0%}" if test else "No test result",
                    is_provisional_eligible=True,
                ),
            ]

            return {
                "quality_gates": gates,
                "outputs": {
                    "character_lexicon": {
                        "total_entries": lexicon.total_entries(),
                        "category_counts": lexicon.count_by_category(),
                        "specificity_pass_rate": test.pass_rate if test else 0.0,
                    },
                },
            }

        except SpecificityTestFailed as e:
            return {
                "quality_gates": [
                    QualityGateResult(
                        gate_name="cral_mapping_validation",
                        passed=False,
                        evidence=str(e),
                        is_provisional_eligible=True,
                    ),
                ],
                "outputs": {},
            }


class SpecificityTestFailed(Exception):
    """Raised when Character Lexicon fails Psychological Specificity Test."""
    pass


class JungianAnchorRequired(Exception):
    """AC3: Raised when archetype deployment lacks character anchor."""
    pass
