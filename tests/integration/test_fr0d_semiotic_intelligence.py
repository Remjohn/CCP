"""
CCP FR0D — Semiotic Intelligence Test Suite
Verification: Coverage test, Jungian anchor, Composition protocol.

Tests:
- AC1: Jungian anchor constraint (archetype without character_lexicon → JUNGIAN_ANCHOR_REQUIRED)
- AC2: Semiotic Coverage Test (< 3 tribe-specific color entries → FAIL)
- Full pipeline + receipts
- DEP-PROTO-018 composition algorithm
- Guardian Agent integration
"""

import asyncio
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

_results: list[dict] = []
_test_dir: str = ""


def log_test(name: str, passed: bool, detail: str = ""):
    status = "✅ PASS" if passed else "❌ FAIL"
    _results.append({"name": name, "passed": passed, "detail": detail})
    print(f"  {status}: {name}" + (f" — {detail}" if detail else ""))


def setup_test_dir() -> str:
    global _test_dir
    _test_dir = tempfile.mkdtemp(prefix="ccp_test_fr0d_")
    return _test_dir


def cleanup_test_dir():
    if _test_dir and Path(_test_dir).exists():
        shutil.rmtree(_test_dir, ignore_errors=True)


# ──────────────────────────────────────────────────────────────
# Test 1 — AC1: Jungian Anchor Constraint
# ──────────────────────────────────────────────────────────────

def test_ac1_jungian_constraint():
    """AC1: Archetype composition without character_lexicon → JUNGIAN_ANCHOR_REQUIRED."""
    from src.ccp.services.semiotic_intelligence_builder import SemioticIntelligenceBuilder
    from src.ccp.models.semiotic_models import (
        VisualSignifierLexicon, VisualSignifierEntry, SemioticCategory,
        CompositionQuery, AudienceMaturity, EmotionalMode,
    )

    base_dir = _test_dir or setup_test_dir()
    builder = SemioticIntelligenceBuilder(
        coach_id="TST-0000", coach_acronym="TST", base_dir=base_dir,
    )

    # Create lexicon with archetype entries
    lexicon = VisualSignifierLexicon(
        coach_id="TST-0000",
        coach_acronym="TST",
        entries=[
            VisualSignifierEntry(
                category=SemioticCategory.UNIVERSAL_ARCHETYPES,
                name="Hero Archetype",
                deployment_mechanism="Deploy with M4",
                tribal_resonance=0.6,
            ),
        ],
    )

    # Query without character_lexicon → should get JUNGIAN_ANCHOR_REQUIRED
    query = CompositionQuery(
        audience_maturity=AudienceMaturity.DEVELOPING,
        emotional_mode=EmotionalMode.VULNERABILITY,
        cral_moment="M4",
    )

    decision = builder.compose(lexicon, query, character_lexicon=None)
    log_test(
        "AC1 — No character_lexicon → JUNGIAN_ANCHOR_REQUIRED",
        decision.jungian_anchor_required,
        f"Error: {decision.jungian_anchor_error[:60]}",
    )
    log_test(
        "AC1 — Error message contains JUNGIAN_ANCHOR_REQUIRED",
        "JUNGIAN_ANCHOR_REQUIRED" in decision.jungian_anchor_error,
        decision.jungian_anchor_error[:80],
    )

    # Same query with character_lexicon → no error
    decision_ok = builder.compose(lexicon, query, character_lexicon={"entries": []})
    log_test(
        "AC1 — With character_lexicon → no error",
        not decision_ok.jungian_anchor_required,
        f"Error: '{decision_ok.jungian_anchor_error}'",
    )


# ──────────────────────────────────────────────────────────────
# Test 2 — AC2: Semiotic Coverage Test
# ──────────────────────────────────────────────────────────────

def test_ac2_coverage():
    """AC2: < 3 tribe-specific color entries with deployment mechanism → FAIL."""
    from src.ccp.models.semiotic_models import (
        VisualSignifierLexicon, VisualSignifierEntry, SemioticCategory,
    )

    # Lexicon with insufficient Color/Typography entries
    lexicon_fail = VisualSignifierLexicon(
        coach_id="TST-0000",
        coach_acronym="TST",
        entries=[
            VisualSignifierEntry(
                category=SemioticCategory.COLOR_TYPOGRAPHY,
                name="Generic warm colors",
                deployment_mechanism="",  # No mechanism → fails
                tribal_resonance=0.5,
                is_baseline=False,
            ),
        ],
    )
    result_fail = lexicon_fail.run_coverage_test()
    color_result = next(
        (r for r in result_fail.category_results
         if r.category == SemioticCategory.COLOR_TYPOGRAPHY), None
    )
    log_test(
        "AC2 — < 3 color entries → FAIL",
        color_result is not None and not color_result.passed,
        f"Color: {color_result.reason if color_result else 'N/A'}",
    )
    log_test(
        "AC2 — Overall coverage FAIL",
        not result_fail.all_passed,
        f"All passed: {result_fail.all_passed}",
    )

    # Lexicon with sufficient entries (all categories)
    sufficient_entries = []
    for cat in SemioticCategory:
        for i in range(4):
            sufficient_entries.append(VisualSignifierEntry(
                category=cat,
                name=f"{cat.value}_entry_{i}",
                deployment_mechanism=f"Deploy in context {i} per DEP-PROTO-018",
                tribal_resonance=0.7,
                is_baseline=False,
            ))
    lexicon_pass = VisualSignifierLexicon(
        coach_id="TST-0000",
        coach_acronym="TST",
        entries=sufficient_entries,
    )
    result_pass = lexicon_pass.run_coverage_test()
    log_test(
        "AC2 — ≥ 3 per category → PASS",
        result_pass.all_passed,
        f"All passed: {result_pass.all_passed}, total tribe-specific: {result_pass.total_tribe_specific}",
    )


# ──────────────────────────────────────────────────────────────
# Test 3 — Full Pipeline
# ──────────────────────────────────────────────────────────────

def test_full_pipeline():
    """Full FR0D pipeline execution."""
    from src.ccp.services.semiotic_intelligence_builder import SemioticIntelligenceBuilder

    base_dir = _test_dir or setup_test_dir()
    builder = SemioticIntelligenceBuilder(
        coach_id="TST-0000", coach_acronym="TST", base_dir=base_dir,
    )

    lexicon = asyncio.run(builder.build())

    log_test("Pipeline — Lexicon produced", lexicon is not None, f"Coach: {lexicon.coach_acronym}")
    log_test("Pipeline — DEP-ID", lexicon.dep_id == "VISUAL-SIGNIFIER-LEXICON", f"dep_id={lexicon.dep_id}")
    log_test("Pipeline — Protocol ID", lexicon.protocol_id == "DEP-PROTO-018", f"protocol_id={lexicon.protocol_id}")

    counts = lexicon.count_by_category()
    log_test(
        "Pipeline — All 4 categories populated",
        all(v > 0 for v in counts.values()),
        f"Counts: {counts}",
    )
    log_test(
        "Pipeline — Color profiles loaded",
        len(lexicon.color_profiles) == 4,
        f"Profiles: {len(lexicon.color_profiles)}",
    )
    log_test(
        "Pipeline — Coverage passed",
        lexicon.coverage_test is not None and lexicon.coverage_test.all_passed,
        f"Coverage: {lexicon.coverage_test.all_passed if lexicon.coverage_test else 'N/A'}",
    )

    # Receipts
    receipts = builder.receipt_chain.query(limit=100)
    log_test("Pipeline — Receipts", len(receipts) > 0, f"Count: {len(receipts)}")

    # Output files
    output_path = Path(base_dir) / "TST" / "intelligence" / "visual_signifier_lexicon.json"
    baseline_path = Path(base_dir) / "TST" / "intelligence" / "visual_signifier_lexicon_baseline.json"
    log_test("Pipeline — Lexicon file", output_path.exists())
    log_test("Pipeline — Baseline file", baseline_path.exists())


# ──────────────────────────────────────────────────────────────
# Test 4 — DEP-PROTO-018 Composition Algorithm
# ──────────────────────────────────────────────────────────────

def test_composition_algorithm():
    """DEP-PROTO-018: 4-question deterministic decisions."""
    from src.ccp.services.semiotic_intelligence_builder import SemioticIntelligenceBuilder
    from src.ccp.models.semiotic_models import (
        CompositionQuery, AudienceMaturity, EmotionalMode,
    )

    base_dir = _test_dir or setup_test_dir()
    builder = SemioticIntelligenceBuilder(
        coach_id="TST-0000", coach_acronym="TST", base_dir=base_dir,
    )

    lexicon = asyncio.run(builder.build())

    # Test various queries
    queries = [
        CompositionQuery(audience_maturity=AudienceMaturity.NEW, emotional_mode=EmotionalMode.TENSION, cral_moment="M3"),
        CompositionQuery(audience_maturity=AudienceMaturity.DEVELOPING, emotional_mode=EmotionalMode.VULNERABILITY, cral_moment="M4"),
        CompositionQuery(audience_maturity=AudienceMaturity.LOYAL, emotional_mode=EmotionalMode.RECOGNITION, cral_moment="M7"),
    ]

    for i, query in enumerate(queries):
        decision = builder.compose(lexicon, query, character_lexicon={"entries": []})
        log_test(
            f"Composition — Q{i+1} ({query.emotional_mode.value}+{query.audience_maturity.value})",
            len(decision.recommended_signifiers) > 0,
            f"Signifiers: {len(decision.recommended_signifiers)}, Color: {decision.color_profile.label if decision.color_profile else 'None'}",
        )


# ──────────────────────────────────────────────────────────────
# Test 5 — Guardian Integration
# ──────────────────────────────────────────────────────────────

def test_guardian_integration():
    from src.ccp.agents.guardian_agent import GuardianAgent
    from src.ccp.models.guardian_models import GenesisStage

    base_dir = _test_dir or setup_test_dir()
    guardian = GuardianAgent(coach_name="Test", coach_acronym="INT", base_dir=base_dir)

    has_fr0d = GenesisStage.FR0D.value in guardian._stage_skills
    log_test("Integration — FR0D auto-registered", has_fr0d, f"Registered: {list(guardian._stage_skills.keys())}")


# ──────────────────────────────────────────────────────────────
# Test 6 — Imports
# ──────────────────────────────────────────────────────────────

def test_imports():
    modules = [
        ("src.ccp.models.semiotic_models", "VisualSignifierLexicon"),
        ("src.ccp.models.semiotic_models", "VisualSignifierEntry"),
        ("src.ccp.models.semiotic_models", "SemioticCategory"),
        ("src.ccp.models.semiotic_models", "CompositionQuery"),
        ("src.ccp.models.semiotic_models", "CompositionDecision"),
        ("src.ccp.models.semiotic_models", "ColorProfile"),
        ("src.ccp.services.semiotic_intelligence_builder", "SemioticIntelligenceBuilder"),
        ("src.ccp.services.semiotic_intelligence_builder", "SemioticCoverageTestFailed"),
    ]
    for module_path, class_name in modules:
        try:
            mod = __import__(module_path, fromlist=[class_name])
            getattr(mod, class_name)
            log_test(f"Import {class_name}", True)
        except Exception as e:
            log_test(f"Import {class_name}", False, str(e))


def run_all():
    print(f"\n{'='*60}")
    print(f"  FR0D SEMIOTIC INTELLIGENCE TEST SUITE")
    print(f"  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"{'='*60}\n")

    try:
        setup_test_dir()
        print("📦 IMPORT TESTS:")
        test_imports()
        print("\n🏛️ AC1 — JUNGIAN ANCHOR CONSTRAINT:")
        test_ac1_jungian_constraint()
        print("\n📏 AC2 — SEMIOTIC COVERAGE TEST:")
        test_ac2_coverage()
        print("\n🔬 FULL PIPELINE:")
        test_full_pipeline()
        print("\n🎨 DEP-PROTO-018 COMPOSITION:")
        test_composition_algorithm()
        print("\n🔌 GUARDIAN INTEGRATION:")
        test_guardian_integration()
    finally:
        cleanup_test_dir()

    passed = sum(1 for r in _results if r["passed"])
    failed = sum(1 for r in _results if not r["passed"])
    total = len(_results)

    print(f"\n{'='*60}")
    print(f"  RESULTS: {passed}/{total} passed, {failed} failed")
    if failed == 0:
        print(f"  ✅ ALL TESTS PASSED")
    else:
        print(f"  ❌ FAILURES:")
        for r in _results:
            if not r["passed"]:
                print(f"    - {r['name']}: {r['detail']}")
    print(f"{'='*60}\n")
    return failed == 0


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
