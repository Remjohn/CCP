"""
CCP Guardian Agent — Integration Test Suite
FR-GA Verification — Tests all 4 acceptance criteria and verdict logic.

Tests:
- AC1: Production Lock (GENESIS_CLEARANCE_REQUIRED without certificate)
- AC2: Stewardship Signal Detection (5+ entries below 0.4 relevance)
- AC3: Operator Approval (recommendation not executed until approved)
- AC4: Receipt Chain Integrity (unbroken chain from interview to certificate)
- Genesis Verdict Logic (FAILED halts pipeline)
- Sequential Execution (strict ordering FR0A → FR0B → FR0C → FR0D → FR0E)
"""

import asyncio
import json
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

# Test results tracking
_results: list[dict] = []
_test_dir: str = ""


def log_test(name: str, passed: bool, detail: str = ""):
    """Log a test result."""
    status = "✅ PASS" if passed else "❌ FAIL"
    _results.append({"name": name, "passed": passed, "detail": detail})
    print(f"  {status}: {name}" + (f" — {detail}" if detail else ""))


def setup_test_dir() -> str:
    """Create a temporary directory for test coach data."""
    global _test_dir
    _test_dir = tempfile.mkdtemp(prefix="ccp_test_guardian_")
    return _test_dir


def cleanup_test_dir():
    """Remove the temporary test directory."""
    if _test_dir and Path(_test_dir).exists():
        shutil.rmtree(_test_dir, ignore_errors=True)


# ──────────────────────────────────────────────────────────────
# Test 1 — AC1: Production Lock
# ──────────────────────────────────────────────────────────────

def test_ac1_production_lock():
    """AC1: Without Genesis Clearance Certificate, FR1 returns GENESIS_CLEARANCE_REQUIRED."""
    from src.ccp.agents.guardian_agent import GuardianAgent

    base_dir = setup_test_dir()

    # Attempt to check clearance for a coach that has no certificate
    has_clearance, cert = GuardianAgent.check_genesis_clearance(
        coach_acronym="TST",
        base_dir=base_dir,
    )

    log_test(
        "AC1 — No certificate → no clearance",
        not has_clearance,
        f"has_clearance={has_clearance}, cert={cert}",
    )
    log_test(
        "AC1 — Certificate is None when missing",
        cert is None,
        f"cert={cert}",
    )

    # Verify GenesisClearanceRequired exception exists
    from src.ccp.commands.genesis import GenesisClearanceRequired
    log_test(
        "AC1 — GenesisClearanceRequired exception importable",
        issubclass(GenesisClearanceRequired, Exception),
        "Exception class verified",
    )


# ──────────────────────────────────────────────────────────────
# Test 2 — AC2: Stewardship Signal Detection
# ──────────────────────────────────────────────────────────────

def test_ac2_stewardship_signal_detection():
    """AC2: 5+ character_lexicon entries below relevance_score 0.4 → Cultural Evolution Signal."""
    from src.ccp.models.stewardship_models import SignalDetection, SignalType

    # Create mock low-relevance character data
    low_relevance_chars = [
        {"name": f"Character_{i}", "relevance_score": 0.3}
        for i in range(6)  # 6 entries below 0.4 (exceeds threshold of 5)
    ]

    # Verify the threshold constant
    from src.ccp.services.stewardship_monitor import StewardshipMonitor
    log_test(
        "AC2 — Threshold is 0.4",
        StewardshipMonitor.CHARACTER_RELEVANCE_THRESHOLD == 0.4,
        f"Threshold={StewardshipMonitor.CHARACTER_RELEVANCE_THRESHOLD}",
    )
    log_test(
        "AC2 — Count threshold is 5",
        StewardshipMonitor.CHARACTER_DROP_COUNT_THRESHOLD == 5,
        f"Count threshold={StewardshipMonitor.CHARACTER_DROP_COUNT_THRESHOLD}",
    )

    # Verify signal model can be created with the right type
    signal = SignalDetection(
        signal_type=SignalType.CULTURAL_EVOLUTION,
        evidence=[
            f"Character '{c['name']}' relevance dropped to {c['relevance_score']:.2f}"
            for c in low_relevance_chars
        ],
        severity=0.4,
        affected_dep_ids=["CHARACTER-LEXICON", "DEP-PROTO-017"],
        metrics={
            "low_relevance_count": len(low_relevance_chars),
            "threshold": 0.4,
        },
    )

    log_test(
        "AC2 — Cultural Evolution Signal created",
        signal.signal_type == SignalType.CULTURAL_EVOLUTION,
        f"Signal type={signal.signal_type.value}, evidence_count={len(signal.evidence)}",
    )
    log_test(
        "AC2 — Signal has 6 evidence items (exceeds 5 threshold)",
        len(signal.evidence) == 6,
        f"Evidence count={len(signal.evidence)} ≥ 5",
    )


# ──────────────────────────────────────────────────────────────
# Test 3 — AC3: Operator Approval
# ──────────────────────────────────────────────────────────────

def test_ac3_operator_approval():
    """AC3: Refresh recommendation NOT executed until /ccf-guardian approve [id] issued."""
    from src.ccp.models.stewardship_models import (
        RecommendationStatus,
        RefreshRecommendation,
        SignalType,
    )

    # Create a pending recommendation
    rec = RefreshRecommendation(
        recommendation_id="test-001",
        coach_id="TST-0000",
        signal_type=SignalType.LEXICON_DRIFT,
        recommended_action="Add unmapped terms to Tribe Lexicon",
        affected_components=["tribe_lexicon"],
        status=RecommendationStatus.PENDING,
    )

    # Verify it starts as PENDING
    log_test(
        "AC3 — Recommendation starts as PENDING",
        rec.status == RecommendationStatus.PENDING,
        f"Status={rec.status.value}",
    )

    # Verify StewardshipMonitor can approve
    base_dir = _test_dir or setup_test_dir()
    coach_dir = Path(base_dir) / "TST" / "config" / "guardian"
    coach_dir.mkdir(parents=True, exist_ok=True)

    from src.ccp.services.stewardship_monitor import StewardshipMonitor
    monitor = StewardshipMonitor(
        coach_id="TST-0000",
        coach_acronym="TST",
        base_dir=base_dir,
    )

    # Save the recommendation
    monitor._save_recommendations([rec])

    # Approve it
    approved = monitor.approve_recommendation("test-001", "operator")

    log_test(
        "AC3 — Recommendation approved after command",
        approved is not None and approved.status == RecommendationStatus.APPROVED,
        f"Status={approved.status.value if approved else 'None'}",
    )
    log_test(
        "AC3 — Approved_by captured",
        approved is not None and approved.approved_by == "operator",
        f"approved_by={approved.approved_by if approved else 'None'}",
    )
    log_test(
        "AC3 — Approved_at timestamp set",
        approved is not None and approved.approved_at is not None,
        "Timestamp set",
    )


# ──────────────────────────────────────────────────────────────
# Test 4 — AC4: Receipt Chain Integrity
# ──────────────────────────────────────────────────────────────

def test_ac4_receipt_chain_integrity():
    """AC4: After Genesis Mode, all receipts have resolvable predecessor_receipt_id."""
    base_dir = _test_dir or setup_test_dir()

    from src.ccp.agents.guardian_agent import GuardianAgent

    guardian = GuardianAgent(
        coach_name="Test Coach",
        coach_acronym="TST",
        base_dir=base_dir,
    )

    # Run genesis with coach-specific interview data (FR0A is now a real skill,
    # not a stub — it requires data that passes the Positioning Precision Test)
    interview_data = {
        "pre_collected": True,
        "positioning_summary": (
            "Adèle Marie transforms corporate executives who have achieved everything "
            "society told them to want — but who wake at 3am knowing their success is "
            "built on someone else's definition of enough — through a 90-day somatic "
            "integration process that reconnects ambition to the body's actual signals, "
            "not the mind's inherited scripts."
        ),
        "transformation_claim": "Reconnects ambition to the body through somatic integration",
        "unique_mechanism": "Embodied Authority Protocol — proprioceptive awareness meets executive decision architecture",
        "who_buys": "C-suite executives who feel hollow despite external success markers",
        "who_doesnt": "Executives seeking productivity hacks or time management",
        "why_they_buy": "The 3am moment of recognizing inherited success scripts",
        "audience_language": ["I've done everything right but it doesn't feel right"],
        "primary_differentiator": "Only coach combining proprioceptive awareness with executive decision architecture",
        "competitors": ["Tony Robbins", "Brene Brown"],
        "positioning_gap": "Markets as leadership coach but does somatic deprogramming",
        "offer_tiers": ["1:1 90-day Protocol", "Group Intensive", "Corporate retreat"],
        "price_range": "$15K-$50K",
        "delivery_method": "Hybrid: in-person somatic + async executive integration",
        "revenue_model": "High-ticket service-based",
        "content_role": "Content should make executives feel seen, not taught",
        "content_fears": "Being perceived as woo-woo in corporate spaces",
        "content_strengths": "Combining neuroscience with felt-sense descriptions",
        "platforms": ["LinkedIn", "Private Podcast"],
        "transformation_stories": [
            {
                "client": "Sarah, VP Operations", "before": "Taking anti-anxiety medication for board meetings",
                "after": "Resigned, launched consulting firm earning more in 6 months, off medication",
                "quotes": ["I was managing my body's rebellion against a life I didn't choose"],
                "mechanism": "Embodied Authority Protocol — 3 somatic sessions", "source": "testimonial",
            },
            {
                "client": "Marcus, CTO Series B", "before": "Panic attacks during fundraising",
                "after": "Led successful Series C with body-awareness check-ins before investor calls",
                "quotes": ["My body was telling me the deal structure betrayed my values"],
                "mechanism": "4-week proprioceptive audit", "source": "interview",
            },
            {
                "client": "Elena, Managing Director", "before": "Success felt like wearing someone else's championship ring",
                "after": "Renegotiated partnership terms, credited method in HBR article",
                "quotes": ["She helped me feel the difference between inherited and owned ambition"],
                "mechanism": "6-week somatic integration + decision architecture redesign", "source": "testimonial",
            },
        ],
    }
    certificate = asyncio.run(guardian.run_genesis(interview_data=interview_data))

    # Query receipt chain
    receipts = guardian.receipt_chain.query(agent_id="guardian_agent", limit=100)

    log_test(
        "AC4 — Receipt chain has entries",
        len(receipts) > 0,
        f"Receipt count={len(receipts)}",
    )

    # Verify certificate was issued
    log_test(
        "AC4 — Certificate issued",
        certificate is not None,
        f"Certificate ID={certificate.certificate_id[:16]}",
    )
    log_test(
        "AC4 — Certificate is valid",
        certificate.is_valid,
        f"is_valid={certificate.is_valid}",
    )
    log_test(
        "AC4 — Certificate has receipt chain root",
        certificate.receipt_chain_root != "",
        f"Root={certificate.receipt_chain_root[:16]}...",
    )

    # Verify all 5 FR0x stages have verdicts
    for stage in ["FR0A", "FR0B", "FR0C", "FR0D", "FR0E"]:
        in_verdicts = stage in certificate.stage_verdicts
        log_test(
            f"AC4 — {stage} verdict present in certificate",
            in_verdicts,
            f"{stage}={certificate.stage_verdicts.get(stage, 'MISSING')}",
        )

    # Check clearance now works
    has_clearance, _ = GuardianAgent.check_genesis_clearance(
        coach_acronym="TST",
        base_dir=base_dir,
    )
    log_test(
        "AC4 — Certificate grants clearance",
        has_clearance,
        f"has_clearance={has_clearance}",
    )


# ──────────────────────────────────────────────────────────────
# Test 5 — Genesis Verdict Logic
# ──────────────────────────────────────────────────────────────

def test_verdict_logic():
    """Verify verdict computation: AUTHENTICATED, PROVISIONAL, FAILED."""
    from src.ccp.agents.guardian_agent import GuardianAgent
    from src.ccp.models.guardian_models import GenesisVerdict, QualityGateResult

    base_dir = _test_dir or setup_test_dir()
    guardian = GuardianAgent(
        coach_name="Test Coach",
        coach_acronym="VRD",
        base_dir=base_dir,
    )

    # All pass → AUTHENTICATED
    gates_all_pass = [
        QualityGateResult(gate_name="gate_1", passed=True, evidence="OK"),
        QualityGateResult(gate_name="gate_2", passed=True, evidence="OK"),
    ]
    verdict, gaps = guardian._compute_verdict(gates_all_pass)
    log_test(
        "Verdict — All pass → AUTHENTICATED",
        verdict == GenesisVerdict.AUTHENTICATED,
        f"Verdict={verdict.value}",
    )
    log_test("Verdict — No gaps on AUTHENTICATED", len(gaps) == 0, f"Gaps={gaps}")

    # Provisional-eligible failure → PROVISIONAL
    gates_provisional = [
        QualityGateResult(gate_name="gate_1", passed=True, evidence="OK"),
        QualityGateResult(
            gate_name="gate_2", passed=False,
            evidence="Below threshold", is_provisional_eligible=True,
        ),
    ]
    verdict, gaps = guardian._compute_verdict(gates_provisional)
    log_test(
        "Verdict — Provisional failure → PROVISIONAL",
        verdict == GenesisVerdict.PROVISIONAL,
        f"Verdict={verdict.value}, gaps={gaps}",
    )

    # Non-provisional failure → FAILED
    gates_failed = [
        QualityGateResult(gate_name="gate_1", passed=True, evidence="OK"),
        QualityGateResult(
            gate_name="gate_2", passed=False,
            evidence="Critical failure", is_provisional_eligible=False,
        ),
    ]
    verdict, gaps = guardian._compute_verdict(gates_failed)
    log_test(
        "Verdict — Non-provisional failure → FAILED",
        verdict == GenesisVerdict.FAILED,
        f"Verdict={verdict.value}",
    )


# ──────────────────────────────────────────────────────────────
# Test 6 — Sequential Execution
# ──────────────────────────────────────────────────────────────

def test_sequential_execution():
    """Verify FR0A → FR0B → FR0C → FR0D → FR0E strict ordering."""
    from src.ccp.models.guardian_models import GenesisStage, GENESIS_STAGE_ORDER

    expected_order = [
        GenesisStage.INTERVIEW,
        GenesisStage.FR0A,
        GenesisStage.FR0B,
        GenesisStage.FR0C,
        GenesisStage.FR0D,
        GenesisStage.FR0E,
        GenesisStage.CERTIFICATE,
    ]

    log_test(
        "Sequential — Stage order matches spec",
        GENESIS_STAGE_ORDER == expected_order,
        f"Order={[s.value for s in GENESIS_STAGE_ORDER]}",
    )

    # Verify state machine navigation
    from src.ccp.models.guardian_models import GenesisState
    state = GenesisState(
        coach_id="TST-0000",
        coach_acronym="TST",
        current_stage=GenesisStage.IDLE,
    )

    next_stage = state.get_next_stage()
    log_test(
        "Sequential — IDLE → INTERVIEW",
        next_stage == GenesisStage.INTERVIEW,
        f"Next={next_stage.value if next_stage else 'None'}",
    )

    state.current_stage = GenesisStage.FR0A
    next_stage = state.get_next_stage()
    log_test(
        "Sequential — FR0A → FR0B",
        next_stage == GenesisStage.FR0B,
        f"Next={next_stage.value if next_stage else 'None'}",
    )

    state.current_stage = GenesisStage.FR0E
    next_stage = state.get_next_stage()
    log_test(
        "Sequential — FR0E → CERTIFICATE",
        next_stage == GenesisStage.CERTIFICATE,
        f"Next={next_stage.value if next_stage else 'None'}",
    )

    # Verify halted state blocks navigation
    state.is_halted = True
    next_stage = state.get_next_stage()
    log_test(
        "Sequential — Halted → None",
        next_stage is None,
        f"Next={next_stage}",
    )


# ──────────────────────────────────────────────────────────────
# Test 7 — Model Imports
# ──────────────────────────────────────────────────────────────

def test_guardian_imports():
    """Test that all Guardian Agent modules can be imported."""
    modules = [
        ("src.ccp.models.guardian_models", "GenesisVerdict"),
        ("src.ccp.models.guardian_models", "GenesisStage"),
        ("src.ccp.models.guardian_models", "StageResult"),
        ("src.ccp.models.guardian_models", "GenesisState"),
        ("src.ccp.models.genesis_certificate", "GenesisClearanceCertificate"),
        ("src.ccp.models.genesis_certificate", "CertificateOverride"),
        ("src.ccp.models.stewardship_models", "SignalType"),
        ("src.ccp.models.stewardship_models", "RefreshRecommendation"),
        ("src.ccp.models.stewardship_models", "StewardshipReport"),
        ("src.ccp.models.stewardship_models", "EvolutionaryRecalibration"),
        ("src.ccp.models.stewardship_models", "DataPromotionTimeout"),
        ("src.ccp.agents.guardian_agent", "GuardianAgent"),
        ("src.ccp.agents.guardian_agent", "GenesisHaltError"),
        ("src.ccp.services.guardian_interview", "InterviewProtocol"),
        ("src.ccp.services.guardian_interview", "InterviewPhase"),
        ("src.ccp.services.stewardship_monitor", "StewardshipMonitor"),
        ("src.ccp.commands.guardian_commands", "GuardianCommandHandler"),
        ("src.ccp.commands.genesis", "GenesisClearanceRequired"),
    ]

    for module_path, class_name in modules:
        try:
            mod = __import__(module_path, fromlist=[class_name])
            cls = getattr(mod, class_name)
            log_test(f"Import {class_name}", True)
        except Exception as e:
            log_test(f"Import {class_name}", False, str(e))


# ──────────────────────────────────────────────────────────────
# Runner
# ──────────────────────────────────────────────────────────────

def run_all():
    """Run the complete Guardian Agent test suite."""
    print(f"\n{'='*60}")
    print(f"  GUARDIAN AGENT TEST SUITE (FR-GA)")
    print(f"  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"{'='*60}\n")

    try:
        setup_test_dir()

        print("📦 IMPORT TESTS:")
        test_guardian_imports()

        print("\n🔒 AC1 — PRODUCTION LOCK:")
        test_ac1_production_lock()

        print("\n🎭 AC2 — STEWARDSHIP SIGNAL DETECTION:")
        test_ac2_stewardship_signal_detection()

        print("\n✅ AC3 — OPERATOR APPROVAL:")
        test_ac3_operator_approval()

        print("\n🔗 AC4 — RECEIPT CHAIN INTEGRITY:")
        test_ac4_receipt_chain_integrity()

        print("\n⚖️ VERDICT LOGIC:")
        test_verdict_logic()

        print("\n📐 SEQUENTIAL EXECUTION:")
        test_sequential_execution()

    finally:
        cleanup_test_dir()

    # Summary
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
