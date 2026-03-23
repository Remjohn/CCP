"""
CCP FR0E — Brand Avatar Test Suite
Verification: Content-Context Routing, Narrative Authenticity.

Tests:
- AC1: Content-Context Routing (all 7 combinations verified)
- AC2: Narrative Authenticity Test (generic FAIL, specific PASS)
- Full pipeline + receipts
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
    _test_dir = tempfile.mkdtemp(prefix="ccp_test_fr0e_")
    return _test_dir


def cleanup_test_dir():
    if _test_dir and Path(_test_dir).exists():
        shutil.rmtree(_test_dir, ignore_errors=True)


# ──────────────────────────────────────────────────────────────
# Test 1 — AC1: Content-Context Routing (7 combinations)
# ──────────────────────────────────────────────────────────────

def test_ac1_routing():
    """AC1: All 7 routing combinations verified."""
    from src.ccp.models.brand_avatar_models import (
        CopingStage, SituationCategory, route_avatar,
    )

    routing_tests = [
        # (coping_stage, emotional_mode, expected_avatar, description)
        (CopingStage.SEARCH, "processing", SituationCategory.MENTOR,
         "SEARCH + Processing → Mentor"),
        (CopingStage.SEARCH, "discovery", SituationCategory.MENTOR,
         "SEARCH + Discovery → Mentor"),
        (CopingStage.SEARCH, "T", SituationCategory.REBEL,
         "SEARCH + Tension → Rebel"),
        (CopingStage.ACTIVE, "discovery", SituationCategory.MENTOR,
         "ACTIVE + Discovery → Mentor"),
        (CopingStage.ACTIVE, "R", SituationCategory.ORIGIN,
         "ACTIVE + Recognition → Origin"),
        (CopingStage.EXHAUSTED, "V", SituationCategory.STRUGGLER,
         "EXHAUSTED + Vulnerability → Struggler"),
        (CopingStage.EXHAUSTED, "escape", SituationCategory.ORIGIN,
         "EXHAUSTED + Escape → Origin"),
    ]

    for coping, mode, expected, desc in routing_tests:
        actual, rationale = route_avatar(coping, mode)
        log_test(
            f"AC1 — {desc}",
            actual == expected,
            f"Expected: {expected.value}, Got: {actual.value}",
        )


# ──────────────────────────────────────────────────────────────
# Test 2 — AC2: Narrative Authenticity Test
# ──────────────────────────────────────────────────────────────

def test_ac2_authenticity():
    """AC2: Generic emotional_state → FAIL, specific with citation → PASS."""
    from src.ccp.models.brand_avatar_models import BrandAvatarEntry, SituationCategory
    from src.ccp.services.brand_avatar_builder import BrandAvatarBuilder

    base_dir = _test_dir or setup_test_dir()
    builder = BrandAvatarBuilder(
        coach_id="TST-0000", coach_acronym="TST", base_dir=base_dir,
    )

    # Generic entry — should FAIL
    generic_avatar = BrandAvatarEntry(
        situation_category=SituationCategory.STRUGGLER,
        emotional_state="feeling overwhelmed by work",
        source_transcript="",
        source_timestamp="",
    )

    # Specific entry — should PASS
    specific_avatar = BrandAvatarEntry(
        situation_category=SituationCategory.STRUGGLER,
        emotional_state=(
            "Saturday morning in the gym parking lot, sitting in the car "
            "with the engine off, texting 'on my way!' to the trainer "
            "while fighting the impulse to drive home — the exhaustion "
            "of performing wellness while being fundamentally depleted."
        ),
        source_transcript="transcript_07",
        source_timestamp="12:15",
    )

    result = builder._run_authenticity_test([generic_avatar, specific_avatar])

    log_test(
        "AC2 — Generic emotional_state fails",
        result.total_failed >= 1,
        f"Failed: {result.total_failed}",
    )

    # Verify the generic one specifically failed
    generic_failed = any(
        not f.passed and f.avatar_category == SituationCategory.STRUGGLER
        for f in [result.failures[0]] if result.failures
    )
    log_test(
        "AC2 — Generic failure identified",
        generic_failed,
        f"Failures: {[(f.avatar_category.value, f.reason[:50]) for f in result.failures]}",
    )

    log_test(
        "AC2 — Specific entry passes",
        result.total_passed >= 1,
        f"Passed: {result.total_passed}",
    )

    # Test with no source transcript → should also fail
    no_citation = BrandAvatarEntry(
        situation_category=SituationCategory.MENTOR,
        emotional_state=(
            "Standing in the boardroom at 6:47am with coffee in hand, "
            "watching the sunrise through floor-to-ceiling windows, "
            "the moment of quiet authority before the first meeting arrives."
        ),
        source_transcript="",
        source_timestamp="",
    )
    result_no_cite = builder._run_authenticity_test([no_citation])
    log_test(
        "AC2 — No citation → FAIL",
        result_no_cite.total_failed >= 1,
        f"Reason: {result_no_cite.failures[0].reason if result_no_cite.failures else 'N/A'}",
    )


# ──────────────────────────────────────────────────────────────
# Test 3 — Full Pipeline
# ──────────────────────────────────────────────────────────────

def test_full_pipeline():
    """Full FR0E pipeline execution."""
    from src.ccp.services.brand_avatar_builder import BrandAvatarBuilder
    from src.ccp.models.brand_avatar_models import SituationCategory

    base_dir = _test_dir or setup_test_dir()
    builder = BrandAvatarBuilder(
        coach_id="TST-0000", coach_acronym="TST", base_dir=base_dir,
    )

    collection = asyncio.run(builder.build())

    log_test("Pipeline — Collection produced", collection is not None, f"Coach: {collection.coach_acronym}")
    log_test("Pipeline — DEP-ID", collection.dep_id == "BRAND-AVATARS", f"dep_id={collection.dep_id}")
    log_test("Pipeline — 4 avatars", len(collection.avatars) == 4, f"Count: {len(collection.avatars)}")
    log_test(
        "Pipeline — All categories present",
        collection.all_categories_present(),
        f"Categories: {[a.situation_category.value for a in collection.avatars]}",
    )
    log_test(
        "Pipeline — Routing registered",
        collection.routing_function_registered,
        f"Registered: {collection.routing_function_registered}",
    )
    log_test(
        "Pipeline — Authenticity passed",
        collection.authenticity_test is not None and collection.authenticity_test.passed,
        f"Passed: {collection.authenticity_test.passed if collection.authenticity_test else 'N/A'}",
    )

    # Specific avatars have source citations
    for avatar in collection.avatars:
        log_test(
            f"Pipeline — {avatar.situation_category.value} has citation",
            bool(avatar.source_transcript),
            f"Source: {avatar.source_transcript} @ {avatar.source_timestamp}",
        )

    # Receipts
    receipts = builder.receipt_chain.query(limit=100)
    log_test("Pipeline — Receipts", len(receipts) > 0, f"Count: {len(receipts)}")

    # Output file
    output_path = Path(base_dir) / "TST" / "intelligence" / "brand_avatars.json"
    log_test("Pipeline — Output file", output_path.exists())


# ──────────────────────────────────────────────────────────────
# Test 4 — Guardian Integration
# ──────────────────────────────────────────────────────────────

def test_guardian_integration():
    from src.ccp.agents.guardian_agent import GuardianAgent
    from src.ccp.models.guardian_models import GenesisStage

    base_dir = _test_dir or setup_test_dir()
    guardian = GuardianAgent(coach_name="Test", coach_acronym="INT", base_dir=base_dir)

    has_fr0e = GenesisStage.FR0E.value in guardian._stage_skills
    log_test("Integration — FR0E auto-registered", has_fr0e, f"Registered: {list(guardian._stage_skills.keys())}")

    # Verify ALL 5 stages are now registered
    all_stages = ["FR0A", "FR0B", "FR0C", "FR0D", "FR0E"]
    all_registered = all(s in guardian._stage_skills for s in all_stages)
    log_test(
        "Integration — All 5 FR0x skills registered",
        all_registered,
        f"Registered: {list(guardian._stage_skills.keys())}",
    )


# ──────────────────────────────────────────────────────────────
# Test 5 — Imports
# ──────────────────────────────────────────────────────────────

def test_imports():
    modules = [
        ("src.ccp.models.brand_avatar_models", "BrandAvatarCollection"),
        ("src.ccp.models.brand_avatar_models", "BrandAvatarEntry"),
        ("src.ccp.models.brand_avatar_models", "SituationCategory"),
        ("src.ccp.models.brand_avatar_models", "CopingStage"),
        ("src.ccp.models.brand_avatar_models", "route_avatar"),
        ("src.ccp.services.brand_avatar_builder", "BrandAvatarBuilder"),
        ("src.ccp.services.brand_avatar_builder", "NarrativeAuthenticityFailed"),
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
    print(f"  FR0E BRAND AVATAR TEST SUITE")
    print(f"  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"{'='*60}\n")

    try:
        setup_test_dir()
        print("📦 IMPORT TESTS:")
        test_imports()
        print("\n🗺️ AC1 — CONTENT-CONTEXT ROUTING:")
        test_ac1_routing()
        print("\n🧬 AC2 — NARRATIVE AUTHENTICITY:")
        test_ac2_authenticity()
        print("\n🔬 FULL PIPELINE:")
        test_full_pipeline()
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
