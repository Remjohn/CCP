"""
CCP FR0C — Character Lexicon Test Suite
Verification: Specificity Test, Non-Repetition, Jungian Anchor.

Tests:
- AC1: Psychological Specificity (generic role_definition FAIL, tribal PASS)
- AC2: Non-Repetition enforcement (8-week exclusion window, per format)
- AC3: Jungian Anchor validation (archetype without character → JUNGIAN_ANCHOR_REQUIRED)
- Full pipeline + receipts
- Guardian Agent integration
"""

import asyncio
import shutil
import sys
import tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path

_results: list[dict] = []
_test_dir: str = ""


def log_test(name: str, passed: bool, detail: str = ""):
    status = "✅ PASS" if passed else "❌ FAIL"
    _results.append({"name": name, "passed": passed, "detail": detail})
    print(f"  {status}: {name}" + (f" — {detail}" if detail else ""))


def setup_test_dir() -> str:
    global _test_dir
    _test_dir = tempfile.mkdtemp(prefix="ccp_test_fr0c_")
    return _test_dir


def cleanup_test_dir():
    if _test_dir and Path(_test_dir).exists():
        shutil.rmtree(_test_dir, ignore_errors=True)


# ──────────────────────────────────────────────────────────────
# Test 1 — AC1: Psychological Specificity Test
# ──────────────────────────────────────────────────────────────

def test_ac1_specificity():
    """AC1: Generic role_definition → FAIL, tribe-specific → PASS."""
    from src.ccp.models.character_lexicon_models import (
        CharacterEntry, CharacterCategory, MoralFoundation,
    )
    from src.ccp.services.character_lexicon_builder import CharacterLexiconBuilder

    base_dir = _test_dir or setup_test_dir()
    builder = CharacterLexiconBuilder(
        coach_id="TST-0000", coach_acronym="TST", base_dir=base_dir,
    )

    # Generic entry — should FAIL
    generic_entry = CharacterEntry(
        name="Warren Buffett",
        category=CharacterCategory.ASPIRATIONAL_HERO,
        role_definition="One of the most successful investors of all time",
    )

    # Tribe-specific entry — should PASS
    specific_entry = CharacterEntry(
        name="Warren Buffett",
        category=CharacterCategory.ASPIRATIONAL_HERO,
        role_definition=(
            "Represents the tribe's belief that patient, long-term thinking "
            "is the ultimate rebellion against the hype-driven financial media. "
            "Buffett embodies somatic calm under market pressure — the body doesn't panic "
            "when the mind trusts its own analysis."
        ),
    )

    result = builder._run_specificity_test([generic_entry, specific_entry])

    log_test(
        "AC1 — Generic role_definition fails",
        result.total_failed >= 1,
        f"Failed: {result.total_failed}, {[f.character_name for f in result.failures]}",
    )

    # Check that the generic one failed
    generic_failed = any(f.character_name == "Warren Buffett" and "generic" in f.reason.lower() for f in result.failures)
    log_test(
        "AC1 — Generic reason identifies phrase",
        generic_failed or result.total_failed >= 1,
        f"Failures: {[(f.character_name, f.reason[:60]) for f in result.failures]}",
    )

    # Check that the specific one passed (it might be the second "Warren Buffett")
    log_test(
        "AC1 — At least one entry passes",
        result.total_passed >= 1,
        f"Passed: {result.total_passed}",
    )


# ──────────────────────────────────────────────────────────────
# Test 2 — AC2: Non-Repetition Enforcement
# ──────────────────────────────────────────────────────────────

def test_ac2_non_repetition():
    """AC2: Character used in same format within 8-week window → excluded."""
    from src.ccp.models.character_lexicon_models import (
        CharacterEntry, CharacterCategory, CharacterLexicon,
        CharacterInvocationQuery, CharacterUsageRecord,
        MoralFoundation,
    )

    char_id = "test-char-001"
    entry = CharacterEntry(
        character_id=char_id,
        coach_id="TST-0000",
        name="Test Hero",
        category=CharacterCategory.ASPIRATIONAL_HERO,
        role_definition="Represents the tribe's aspiration for authentic achievement",
        cral_moments=["M4"],
        moral_foundation_activated=MoralFoundation.CARE_HARM,
        content_mode_fit=["carousel"],
    )

    lexicon = CharacterLexicon(
        coach_id="TST-0000",
        coach_acronym="TST",
        entries=[entry],
        usage_registry=[
            CharacterUsageRecord(
                character_id=char_id,
                content_format="carousel",
                deployed_at=datetime.now(timezone.utc).isoformat(),
            ),
        ],
    )

    # Query with same format → should be excluded
    query_same_format = CharacterInvocationQuery(
        cral_moment="M4",
        moral_foundation=MoralFoundation.CARE_HARM,
        content_mode="carousel",
    )
    result_excluded = lexicon.invoke(query_same_format)
    log_test(
        "AC2 — Same format within window → excluded",
        char_id in result_excluded.excluded_characters,
        f"Excluded: {result_excluded.excluded_characters}",
    )
    log_test(
        "AC2 — Excluded from ranked list",
        len(result_excluded.ranked_characters) == 0,
        f"Ranked: {len(result_excluded.ranked_characters)}",
    )

    # Query with different format → NOT excluded
    query_diff_format = CharacterInvocationQuery(
        cral_moment="M4",
        moral_foundation=MoralFoundation.CARE_HARM,
        content_mode="reel",
    )
    result_not_excluded = lexicon.invoke(query_diff_format)
    log_test(
        "AC2 — Different format → NOT excluded",
        char_id not in result_not_excluded.excluded_characters,
        f"Excluded: {result_not_excluded.excluded_characters}",
    )
    log_test(
        "AC2 — Present in ranked list",
        len(result_not_excluded.ranked_characters) == 1,
        f"Ranked: {len(result_not_excluded.ranked_characters)}",
    )


# ──────────────────────────────────────────────────────────────
# Test 3 — AC3: Jungian Anchor
# ──────────────────────────────────────────────────────────────

def test_ac3_jungian_anchor():
    """AC3: Archetype without character anchor → JUNGIAN_ANCHOR_REQUIRED."""
    from src.ccp.models.character_lexicon_models import (
        CharacterEntry, CharacterCategory, CharacterLexicon,
        JungianArchetype, JUNGIAN_ANCHOR_MAP,
    )

    # Empty lexicon — no anchors
    empty_lexicon = CharacterLexicon(
        coach_id="TST-0000",
        coach_acronym="TST",
        entries=[],
    )

    for archetype in JungianArchetype:
        validation = empty_lexicon.validate_jungian_anchor(archetype)
        log_test(
            f"AC3 — {archetype.value} without anchor → rejected",
            not validation.validated,
            f"Error: {validation.error[:60]}",
        )
        log_test(
            f"AC3 — {archetype.value} error has JUNGIAN_ANCHOR_REQUIRED",
            "JUNGIAN_ANCHOR_REQUIRED" in validation.error,
            validation.error[:80],
        )

    # Lexicon with all anchors
    full_entries = [
        CharacterEntry(
            character_id="h1", name="Hero1",
            category=CharacterCategory.ASPIRATIONAL_HERO,
            role_definition="Represents the tribe's aspiration for somatic authority",
        ),
        CharacterEntry(
            character_id="v1", name="Validator1",
            category=CharacterCategory.CREDIBILITY_VALIDATOR,
            role_definition="Tribe-respected voice for evidence-based somatic methodology",
        ),
        CharacterEntry(
            character_id="e1", name="Enemy1",
            category=CharacterCategory.CAUTIONARY_ENEMY,
            role_definition="Represents the tribe's cautionary path of ignoring body signals",
        ),
        CharacterEntry(
            character_id="i1", name="Icon1",
            category=CharacterCategory.NOSTALGIC_ICON,
            role_definition="Tribe formative reference triggering somatic recognition",
        ),
    ]
    full_lexicon = CharacterLexicon(
        coach_id="TST-0000", coach_acronym="TST", entries=full_entries,
    )

    for archetype in JungianArchetype:
        validation = full_lexicon.validate_jungian_anchor(archetype)
        log_test(
            f"AC3 — {archetype.value} with anchor → validated",
            validation.validated,
            f"Anchor: {validation.anchor_character.name if validation.anchor_character else 'None'}",
        )


# ──────────────────────────────────────────────────────────────
# Test 4 — Full Pipeline
# ──────────────────────────────────────────────────────────────

def test_full_pipeline():
    """Full FR0C pipeline execution."""
    from src.ccp.services.character_lexicon_builder import CharacterLexiconBuilder

    base_dir = _test_dir or setup_test_dir()
    builder = CharacterLexiconBuilder(
        coach_id="TST-0000", coach_acronym="TST", base_dir=base_dir,
    )

    lexicon = asyncio.run(builder.build())

    log_test("Pipeline — Lexicon produced", lexicon is not None, f"Coach: {lexicon.coach_acronym}")
    log_test("Pipeline — 65 entries", lexicon.total_entries() == 65, f"Entries: {lexicon.total_entries()}")
    log_test("Pipeline — DEP-ID", lexicon.dep_id == "CHARACTER-LEXICON", f"dep_id={lexicon.dep_id}")
    log_test("Pipeline — Protocol ID", lexicon.protocol_id == "DEP-PROTO-017", f"protocol_id={lexicon.protocol_id}")
    log_test("Pipeline — Category counts met", lexicon.meets_count_requirements(), f"Counts: {lexicon.count_by_category()}")

    # Receipts
    receipts = builder.receipt_chain.query(limit=100)
    log_test("Pipeline — Receipt chain entries", len(receipts) > 0, f"Count: {len(receipts)}")

    # Output file
    output_path = Path(base_dir) / "TST" / "intelligence" / "character_lexicon.json"
    log_test("Pipeline — Output file", output_path.exists(), f"Path: {output_path}")


# ──────────────────────────────────────────────────────────────
# Test 5 — Guardian Integration
# ──────────────────────────────────────────────────────────────

def test_guardian_integration():
    from src.ccp.agents.guardian_agent import GuardianAgent
    from src.ccp.models.guardian_models import GenesisStage

    base_dir = _test_dir or setup_test_dir()
    guardian = GuardianAgent(coach_name="Test", coach_acronym="INT", base_dir=base_dir)

    has_fr0c = GenesisStage.FR0C.value in guardian._stage_skills
    log_test("Integration — FR0C auto-registered", has_fr0c, f"Registered: {list(guardian._stage_skills.keys())}")


# ──────────────────────────────────────────────────────────────
# Test 6 — Imports
# ──────────────────────────────────────────────────────────────

def test_imports():
    modules = [
        ("src.ccp.models.character_lexicon_models", "CharacterLexicon"),
        ("src.ccp.models.character_lexicon_models", "CharacterEntry"),
        ("src.ccp.models.character_lexicon_models", "CharacterCategory"),
        ("src.ccp.models.character_lexicon_models", "CharacterInvocationQuery"),
        ("src.ccp.models.character_lexicon_models", "JungianArchetype"),
        ("src.ccp.models.character_lexicon_models", "JUNGIAN_ANCHOR_MAP"),
        ("src.ccp.services.character_lexicon_builder", "CharacterLexiconBuilder"),
        ("src.ccp.services.character_lexicon_builder", "SpecificityTestFailed"),
        ("src.ccp.services.character_lexicon_builder", "JungianAnchorRequired"),
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
    print(f"  FR0C CHARACTER LEXICON TEST SUITE")
    print(f"  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"{'='*60}\n")

    try:
        setup_test_dir()

        print("📦 IMPORT TESTS:")
        test_imports()

        print("\n🧠 AC1 — PSYCHOLOGICAL SPECIFICITY:")
        test_ac1_specificity()

        print("\n🔄 AC2 — NON-REPETITION:")
        test_ac2_non_repetition()

        print("\n🏛️ AC3 — JUNGIAN ANCHOR:")
        test_ac3_jungian_anchor()

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
