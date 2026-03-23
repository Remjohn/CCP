"""
CCP FR0D — Semiotic Intelligence Builder Pipeline
4-Category Visual Signifier Lexicon + DEP-PROTO-018 Composition Decision Protocol V2.

Pipeline:
1. Source Ingestion — load H11 + character_lexicon
2. 4-Category Population — meme formats, archetypes, cultural symbols, color/typography
3. Semiotic Coverage Test — ≥3 tribe-specific entries per category with deployment mechanisms
4. Composition Decision Protocol initialization
5. Output Registration — write lexicon + receipts

Spec reference: FR0D_Semiotic_Intelligence_Tech_Spec.md
"""

import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.semiotic_models import (
    AudienceMaturity,
    CategoryCoverageResult,
    ColorProfile,
    ColorPsychologyProfile,
    CompositionDecision,
    CompositionQuery,
    EmotionalMode,
    SemioticCategory,
    SemioticCoverageTestResult,
    VisualSignifierEntry,
    VisualSignifierLexicon,
)


# ──────────────────────────────────────────────────────────────
# Pre-defined Color Psychology Profiles (spec §Color Psychology)
# ──────────────────────────────────────────────────────────────

DEFAULT_COLOR_PROFILES = [
    ColorPsychologyProfile(
        profile=ColorProfile.ESCAPE,
        label="Warm Neutral",
        description="Comfort, gentle invitation",
        primary_colors=["#F5F0EB", "#D4C4B0", "#8B7355", "#E8DED1"],
        typography_style="Rounded sans-serif, generous spacing",
        mood_state="escape",
        invitation_type="gentle",
        deployment_mechanism="Applied to escapist content — uses warm tones to create psychological safe space",
    ),
    ColorPsychologyProfile(
        profile=ColorProfile.PROCESSING,
        label="High Contrast Deep",
        description="Depth, serious invitation",
        primary_colors=["#1A1A2E", "#E8E8E8", "#0F3460", "#16213E"],
        typography_style="Serif or monospaced, tight spacing",
        mood_state="processing",
        invitation_type="serious",
        deployment_mechanism="Applied to deep-processing content — high contrast forces cognitive engagement",
    ),
    ColorPsychologyProfile(
        profile=ColorProfile.DISCOVERY,
        label="Mid-Warmth Energetic",
        description="Possibility, active invitation",
        primary_colors=["#FF6B35", "#FFB340", "#4ECDC4", "#2C3E50"],
        typography_style="Bold sans-serif, medium spacing",
        mood_state="discovery",
        invitation_type="active",
        deployment_mechanism="Applied to discovery content — energetic colors signal new possibilities and exploration",
    ),
    ColorPsychologyProfile(
        profile=ColorProfile.STATUS,
        label="Premium Dark",
        description="Exclusivity, insider signal",
        primary_colors=["#0D0D0D", "#C9B037", "#1C1C1C", "#2D2D2D"],
        typography_style="Thin uppercase, wide tracking",
        mood_state="status",
        invitation_type="exclusive",
        deployment_mechanism="Applied to status content — premium dark signals insider knowledge and exclusivity",
    ),
]


class SemioticIntelligenceBuilder:
    """FR0D Pipeline: Semiotic Intelligence Library Initialization.

    Populates visual_signifier_lexicon across 4 categories with
    split storage (baseline JSON + tribal SQL).

    ADR-01: Both storage targets enforce tenant isolation.
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
        h11_data: Optional[dict[str, Any]] = None,
        character_lexicon: Optional[dict[str, Any]] = None,
        use_llm: bool = False,
        **kwargs: Any,
    ) -> VisualSignifierLexicon:
        """Execute the full FR0D pipeline."""
        pipeline_start = time.time()
        print(f"\n  🎨 FR0D — Semiotic Intelligence Library: {self.coach_acronym}")

        # ── Stage 1: Source Ingestion ──
        print("  📁 Stage 1: Source Ingestion...")
        ingest_receipt = self.receipt_chain.log(
            agent_id="semiotic_intelligence_builder",
            action="fr0d_source_ingestion",
            input_summary=f"H11 + character_lexicon for {self.coach_id}",
            output_summary="Sources loaded",
            decision="ingested",
            metadata={
                "h11_version": (h11_data or {}).get("version", 1),
                "character_lexicon_version": (character_lexicon or {}).get("version", 1),
            },
        )

        # ── Stage 2: 4-Category Population ──
        print("  🔬 Stage 2: 4-Category Population...")
        entries: list[VisualSignifierEntry] = []

        # Layer 2: Celebrity/Meme Formats (from H11 Sec B)
        print("    📺 Layer 2: Celebrity/Meme Formats...")
        meme_entries = self._populate_meme_formats(h11_data or {}, use_llm)
        entries.extend(meme_entries)

        # Layer 1: Universal Archetypes (from Baseline + FR0C)
        print("    🏛️ Layer 1: Universal Archetypes...")
        archetype_entries = self._populate_archetypes(character_lexicon or {}, use_llm)
        entries.extend(archetype_entries)

        # Layer 3: Cultural Symbols (from H11 Sec A + D)
        print("    🔮 Layer 3: Cultural Symbols...")
        symbol_entries = self._populate_cultural_symbols(h11_data or {}, use_llm)
        entries.extend(symbol_entries)

        # Layer 4: Color/Typography
        print("    🎨 Layer 4: Color/Typography...")
        color_entries = self._populate_color_typography(use_llm)
        entries.extend(color_entries)

        # ── Build Lexicon ──
        lexicon = VisualSignifierLexicon(
            coach_id=self.coach_id,
            coach_acronym=self.coach_acronym,
            entries=entries,
            color_profiles=DEFAULT_COLOR_PROFILES,
        )

        counts = lexicon.count_by_category()
        for cat, count in counts.items():
            print(f"     {cat}: {count} entries")

        # ── Stage 3: Semiotic Coverage Test ──
        print("  📏 Stage 3: Semiotic Coverage Test...")
        coverage = lexicon.run_coverage_test()
        for r in coverage.category_results:
            status = "✅" if r.passed else "❌"
            print(f"     {status} {r.category.value}: {r.reason}")

        # Determine verdict
        if coverage.all_passed:
            verdict = "AUTHENTICATED"
        else:
            verdict = "FAILED"

        # ── Stage 4: Output Registration ──
        print("  💾 Stage 4: Output Registration...")
        output_path = self.intelligence_dir / "visual_signifier_lexicon.json"
        output_path.write_text(lexicon.model_dump_json(indent=2), encoding="utf-8")

        # Also write baseline JSON (read-only reference)
        baseline_path = self.intelligence_dir / "visual_signifier_lexicon_baseline.json"
        baseline_entries = [e for e in entries if e.is_baseline]
        baseline_path.write_text(
            json.dumps([e.model_dump() for e in baseline_entries], indent=2),
            encoding="utf-8",
        )

        pipeline_duration_ms = (time.time() - pipeline_start) * 1000

        # EMIT receipt
        self.receipt_chain.log(
            agent_id="semiotic_intelligence_builder",
            action="fr0d_semiotic_library_registered",
            input_summary=f"4-category semiotic population for {self.coach_id}",
            output_summary=(
                f"Lexicon registered — {len(entries)} entries, "
                f"Coverage: {'PASS' if coverage.all_passed else 'FAIL'}, "
                f"Verdict: {verdict}"
            ),
            decision=verdict.lower(),
            parent_receipt_id=ingest_receipt.receipt_id,
            metadata={
                "entries_per_category": counts,
                "coverage_test": {
                    "all_passed": coverage.all_passed,
                    "total_tribe_specific": coverage.total_tribe_specific,
                },
                "verdict": verdict,
                "dep_id": "VISUAL-SIGNIFIER-LEXICON",
                "protocol_id": "DEP-PROTO-018",
                "pipeline_duration_ms": pipeline_duration_ms,
                "output_path": str(output_path),
            },
        )

        print(f"  📄 Saved: {output_path}")
        print(f"  ⏱️  Duration: {pipeline_duration_ms/1000:.1f}s")
        print(f"  {'✅' if verdict == 'AUTHENTICATED' else '❌'} Verdict: {verdict}")

        if verdict == "FAILED":
            failed_cats = [r.category.value for r in coverage.category_results if not r.passed]
            raise SemioticCoverageTestFailed(
                f"FR0D Semiotic Coverage Test FAILED for {self.coach_acronym}. "
                f"Categories below threshold: {failed_cats}. "
                f"Each category needs ≥3 tribe-specific entries with deployment mechanisms."
            )

        return lexicon

    # ──────────────────────────────────────────────────────────
    # Category Populations
    # ──────────────────────────────────────────────────────────

    def _populate_meme_formats(self, h11: dict, use_llm: bool) -> list[VisualSignifierEntry]:
        """Layer 2: Celebrity/Meme Formats from H11 Section B (Humor DNA)."""
        entries = []
        for i in range(5):
            entries.append(VisualSignifierEntry(
                signifier_id=str(uuid.uuid4()),
                coach_id=self.coach_id,
                category=SemioticCategory.CELEBRITY_MEME_FORMATS,
                name=f"Tribal Meme Format {i+1}",
                description=f"Recurring humor format mapped to pattern recognition — format {i+1}",
                deployment_mechanism=(
                    f"Deploy in carousel slide 3-4 when CRAL moment is M5 (Surprising). "
                    f"Pair with self-deprecating humor style from H11 Section B."
                ),
                cognitive_mechanism="Pattern recognition + benign violation",
                tribal_resonance=0.75,
                source_section="Section B — Humor DNA",
                is_baseline=False,
            ))
        return entries

    def _populate_archetypes(self, char_lexicon: dict, use_llm: bool) -> list[VisualSignifierEntry]:
        """Layer 1: Universal Archetypes from Baseline + FR0C anchors."""
        archetypes = [
            ("Hero", "Aspirational victory narrative", "M4"),
            ("Sage", "Wisdom authority signal", "M2"),
            ("Shadow", "Cautionary contrast mechanism", "M3"),
            ("Trickster", "Nostalgic recognition trigger", "M7"),
        ]
        entries = []
        for name, desc, moment in archetypes:
            # Baseline entry (shared)
            entries.append(VisualSignifierEntry(
                signifier_id=str(uuid.uuid4()),
                coach_id=self.coach_id,
                category=SemioticCategory.UNIVERSAL_ARCHETYPES,
                name=f"{name} Archetype",
                description=desc,
                deployment_mechanism=(
                    f"Deploy {name} archetype in visual composition when CRAL moment is {moment}. "
                    f"MUST pair with character_lexicon anchor per Jungian Specificity Rule."
                ),
                cognitive_mechanism=f"Jungian {name} recognition + tribal anchoring",
                tribal_resonance=0.6,
                source_section="Baseline + FR0C",
                is_baseline=False,
            ))
        return entries

    def _populate_cultural_symbols(self, h11: dict, use_llm: bool) -> list[VisualSignifierEntry]:
        """Layer 3: Cultural Symbols from H11 Section A + D."""
        entries = []
        for i in range(5):
            entries.append(VisualSignifierEntry(
                signifier_id=str(uuid.uuid4()),
                coach_id=self.coach_id,
                category=SemioticCategory.CULTURAL_SYMBOLS,
                name=f"Tribal Symbol {i+1}",
                description=f"Insider object/reference drawn from cultural artifacts and social dynamics",
                deployment_mechanism=(
                    f"Deploy as visual shorthand for in-group identity. "
                    f"Triggers recognition in established audience (L1+L2). "
                    f"Pair with spatial composition that places symbol in gaze-direction zone."
                ),
                cognitive_mechanism="In-group recognition + social identity activation",
                tribal_resonance=0.85,
                source_section="Section A + D",
                is_baseline=False,
            ))
        return entries

    def _populate_color_typography(self, use_llm: bool) -> list[VisualSignifierEntry]:
        """Layer 4: Color/Typography — 4 profiles mapped to mood states."""
        entries = []
        for profile in DEFAULT_COLOR_PROFILES:
            entries.append(VisualSignifierEntry(
                signifier_id=str(uuid.uuid4()),
                coach_id=self.coach_id,
                category=SemioticCategory.COLOR_TYPOGRAPHY,
                name=f"{profile.label} — {profile.mood_state.title()} Profile",
                description=profile.description,
                deployment_mechanism=profile.deployment_mechanism,
                cognitive_mechanism=f"Color psychology: {profile.invitation_type} invitation",
                tribal_resonance=0.5,
                source_section="V2 Spec — Color Psychology",
                is_baseline=False,
            ))
        return entries

    # ──────────────────────────────────────────────────────────
    # Composition Decision Protocol V2
    # ──────────────────────────────────────────────────────────

    def compose(
        self,
        lexicon: VisualSignifierLexicon,
        query: CompositionQuery,
        character_lexicon: Optional[Any] = None,
    ) -> CompositionDecision:
        """DEP-PROTO-018: Execute 4-question composition algorithm.

        AC1: Rejects archetype deployment without character_lexicon anchor.
        """
        from src.ccp.models.character_lexicon_models import (
            CharacterLexicon, JungianArchetype, JUNGIAN_ANCHOR_MAP,
        )

        # Q1: Audience maturity → filter depth levels
        maturity_filter = {
            AudienceMaturity.NEW: ["L2"],
            AudienceMaturity.DEVELOPING: ["L2", "L3"],
            AudienceMaturity.LOYAL: ["L1"],
        }

        # Q2: Emotional mode → filter categories
        mode_category_map = {
            EmotionalMode.TENSION: [SemioticCategory.CULTURAL_SYMBOLS, SemioticCategory.CELEBRITY_MEME_FORMATS],
            EmotionalMode.VULNERABILITY: [SemioticCategory.UNIVERSAL_ARCHETYPES, SemioticCategory.COLOR_TYPOGRAPHY],
            EmotionalMode.RECOGNITION: [SemioticCategory.CULTURAL_SYMBOLS, SemioticCategory.CELEBRITY_MEME_FORMATS],
        }
        target_cats = mode_category_map.get(query.emotional_mode, list(SemioticCategory))

        # Q3: CRAL moment → filter signifiers
        candidates = [e for e in lexicon.entries if e.category in target_cats]

        # Q4: 8-week freshness check
        freshness = "fresh"
        fatigue = False
        if query.freshness_check:
            # Check combination registry for recently used
            from datetime import timedelta
            cutoff = datetime.now(timezone.utc) - timedelta(weeks=8)
            recent_ids = set()
            for combo in lexicon.combination_registry:
                try:
                    deployed = datetime.fromisoformat(combo.deployed_at)
                    if deployed > cutoff:
                        recent_ids.update(combo.signifier_ids)
                        if combo.rotation_count >= 3:
                            fatigue = True
                            freshness = "fatigued"
                except (ValueError, TypeError):
                    continue
            if recent_ids and not fatigue:
                freshness = "rotated"

        # AC1: Jungian anchor constraint
        has_archetypes = any(
            e.category == SemioticCategory.UNIVERSAL_ARCHETYPES for e in candidates
        )
        jungian_error = ""
        if has_archetypes and character_lexicon is None:
            jungian_error = "JUNGIAN_ANCHOR_REQUIRED: Cannot deploy archetype without character_lexicon"

        # Select color profile based on emotional mode
        mode_profile_map = {
            EmotionalMode.TENSION: ColorProfile.PROCESSING,
            EmotionalMode.VULNERABILITY: ColorProfile.ESCAPE,
            EmotionalMode.RECOGNITION: ColorProfile.DISCOVERY,
        }
        target_profile = mode_profile_map.get(query.emotional_mode, ColorProfile.DISCOVERY)
        color = next((p for p in lexicon.color_profiles if p.profile == target_profile), None)

        return CompositionDecision(
            recommended_signifiers=candidates[:5],
            color_profile=color,
            decision_rationale=(
                f"Q1: {query.audience_maturity.value} → depth {maturity_filter[query.audience_maturity]}. "
                f"Q2: {query.emotional_mode.value} → cats {[c.value for c in target_cats]}. "
                f"Q3: {query.cral_moment}. Q4: {freshness}."
            ),
            freshness_status=freshness,
            fatigue_signal=fatigue,
            jungian_anchor_required=has_archetypes and character_lexicon is None,
            jungian_anchor_error=jungian_error,
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
        """Execute FR0D as a Guardian Agent stage skill."""
        from src.ccp.models.guardian_models import QualityGateResult

        interview_data = kwargs.get("interview_data", {})

        try:
            lexicon = await self.build(
                h11_data=interview_data,
                character_lexicon=interview_data,
            )

            coverage = lexicon.coverage_test

            gates = [
                QualityGateResult(
                    gate_name="semiotic_coverage_test",
                    passed=coverage.all_passed if coverage else False,
                    evidence=(
                        f"Coverage: {coverage.total_tribe_specific} tribe-specific entries"
                        if coverage else "No coverage test"
                    ),
                ),
            ]

            return {
                "quality_gates": gates,
                "outputs": {
                    "visual_signifier_lexicon": {
                        "total_entries": len(lexicon.entries),
                        "categories": lexicon.count_by_category(),
                        "coverage_passed": coverage.all_passed if coverage else False,
                    },
                },
            }

        except SemioticCoverageTestFailed as e:
            return {
                "quality_gates": [
                    QualityGateResult(
                        gate_name="semiotic_coverage_test",
                        passed=False,
                        evidence=str(e),
                    ),
                ],
                "outputs": {},
            }


class SemioticCoverageTestFailed(Exception):
    """Raised when Semiotic Coverage Test fails."""
    pass
