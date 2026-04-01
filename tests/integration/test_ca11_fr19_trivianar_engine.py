"""FR-CA11-19 — Interactive Trivianar Engine — Integration Tests.

Target: 10 ACs + batch receipt + SQL tables + constants.
Pattern: _run() helper for async, no pytest-asyncio.
"""
from __future__ import annotations

import asyncio

import pytest

from src.ccp.models.ca11_models import (
    COUNTDOWN_DIVISOR,
    COUNTDOWN_MAX_SCORE,
    DEFAULT_TIME_LIMIT_SECONDS,
    LEADERBOARD_SIZE,
    REACTION_DELAY_MS,
    SPEED_RECORD_THRESHOLD_MS,
    TRIVIA_AGENT_NAME,
    WAGER_MAX,
    WAGER_MIN,
    BatchReceiptPayload,
    LeaderboardEntry,
    MicrocommitmentResponse,
    QuestionDifficulty,
    ReactionPool,
    ScoringResult,
    TriviaError,
    TriviaGameMode,
    TriviaQuestion,
    TriviaResponse,
    TriviaSessionConfig,
    TrivianarResult,
)
from src.ccp.services.trivianar_engine_service import (
    DEFAULT_REACTION_POOLS,
    TRIVIA_LEADERBOARD_SQL,
    TRIVIA_QUESTIONS_SQL,
    TRIVIA_RESPONSES_SQL,
    TrivianarEngine,
    calculate_countdown_score,
    calculate_team_score,
    check_survivor_status,
    compute_batch_receipt_hash,
    compute_leaderboard,
    extract_cbcs_mapping,
    process_wager,
    select_reaction,
)


def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_question(**overrides) -> TriviaQuestion:
    defaults = dict(
        coach_id="coach-1",
        surface_text="What is CCP?",
        answer_options=[
            {"key": "A", "text": "Conscious Coaching Platform"},
            {"key": "B", "text": "Cloud Compute Provider"},
            {"key": "C", "text": "Custom Content Pipeline"},
        ],
        correct_answer="A",
    )
    defaults.update(overrides)
    return TriviaQuestion(**defaults)


def _make_response(user_id: int = 1, score: int = 0, **overrides) -> TriviaResponse:
    defaults = dict(
        user_id=user_id,
        question_id="q-1",
        stream_id="stream-1",
        answer="A",
        is_correct=True,
        score=score,
    )
    defaults.update(overrides)
    return TriviaResponse(**defaults)


# ═══════════════════════════════════════════════════════════════════════
# AC1: Question Delivery
# ═══════════════════════════════════════════════════════════════════════


class TestQuestionDelivery:
    """AC1: POST /trivia/question → question shows with countdown."""

    def test_question_has_required_fields(self):
        q = _make_question()
        assert q.surface_text
        assert len(q.answer_options) >= 2
        assert q.correct_answer == "A"

    def test_question_default_time_limit(self):
        q = _make_question()
        assert q.time_limit_seconds == DEFAULT_TIME_LIMIT_SECONDS

    def test_question_custom_time_limit(self):
        q = _make_question(time_limit_seconds=30)
        assert q.time_limit_seconds == 30

    def test_question_difficulty_default(self):
        q = _make_question()
        assert q.difficulty == QuestionDifficulty.ACCESSIBLE.value

    def test_question_with_media(self):
        q = _make_question(media_url="https://cdn.example.com/img.png")
        assert q.media_url is not None

    def test_session_start(self):
        engine = TrivianarEngine()
        config = TriviaSessionConfig(
            stream_id="stream-1", coach_id="coach-1",
            game_mode=TriviaGameMode.COUNTDOWN.value,
        )
        result = engine.start_session(config)
        assert result.success is True
        assert result.session_config == config


# ═══════════════════════════════════════════════════════════════════════
# AC2: Countdown Scoring
# ═══════════════════════════════════════════════════════════════════════


class TestCountdownScoring:
    """AC2: score = max(0, 1000 - elapsed_ms / 10). 3s → 700."""

    def test_3s_gives_700_points(self):
        score = calculate_countdown_score(3000, is_correct=True)
        assert score == 700

    def test_instant_answer(self):
        score = calculate_countdown_score(0, is_correct=True)
        assert score == COUNTDOWN_MAX_SCORE

    def test_10s_gives_zero(self):
        score = calculate_countdown_score(10000, is_correct=True)
        assert score == 0

    def test_wrong_answer_gives_zero(self):
        score = calculate_countdown_score(500, is_correct=False)
        assert score == 0

    def test_over_10s_clamped_to_zero(self):
        score = calculate_countdown_score(15000, is_correct=True)
        assert score == 0

    def test_5s_gives_500(self):
        score = calculate_countdown_score(5000, is_correct=True)
        assert score == 500

    def test_engine_score_response_countdown(self):
        engine = TrivianarEngine()
        q = _make_question()
        result = engine.score_response(q, "A", 3000, game_mode=TriviaGameMode.COUNTDOWN.value)
        assert result.score == 700
        assert result.is_correct is True


# ═══════════════════════════════════════════════════════════════════════
# AC3: Leaderboard (top 10)
# ═══════════════════════════════════════════════════════════════════════


class TestLeaderboard:
    """AC3: Leaderboard top 10 by score."""

    def test_empty_responses(self):
        board = compute_leaderboard([])
        assert board == []

    def test_single_user(self):
        responses = [_make_response(user_id=1, score=700)]
        board = compute_leaderboard(responses)
        assert len(board) == 1
        assert board[0].rank == 1
        assert board[0].total_score == 700

    def test_ranking_order(self):
        responses = [
            _make_response(user_id=1, score=700),
            _make_response(user_id=2, score=900),
            _make_response(user_id=3, score=500),
        ]
        board = compute_leaderboard(responses)
        assert board[0].user_id == 2
        assert board[1].user_id == 1
        assert board[2].user_id == 3

    def test_aggregates_scores(self):
        responses = [
            _make_response(user_id=1, score=300),
            _make_response(user_id=1, score=400),
            _make_response(user_id=2, score=600),
        ]
        board = compute_leaderboard(responses)
        assert board[0].user_id == 1
        assert board[0].total_score == 700

    def test_caps_at_leaderboard_size(self):
        responses = [
            _make_response(user_id=i, score=i * 10)
            for i in range(1, 20)
        ]
        board = compute_leaderboard(responses)
        assert len(board) == LEADERBOARD_SIZE

    def test_engine_get_leaderboard(self):
        engine = TrivianarEngine()
        responses = [
            _make_response(user_id=1, score=700),
            _make_response(user_id=2, score=500),
        ]
        board = engine.get_leaderboard(responses)
        assert len(board) == 2
        assert board[0].user_id == 1


# ═══════════════════════════════════════════════════════════════════════
# AC4: Qualifying Question CBCS Mapping
# ═══════════════════════════════════════════════════════════════════════


class TestQualifyingCBCS:
    """AC4: Qualifying question extracts CBCS mapping."""

    def test_extract_mapping(self):
        q = _make_question(cbcs_mapping={"A": {"social": 0.18}, "B": {"analytical": 0.22}})
        mapping = extract_cbcs_mapping(q, "A")
        assert mapping == {"social": 0.18}

    def test_no_mapping_returns_none(self):
        q = _make_question()
        mapping = extract_cbcs_mapping(q, "A")
        assert mapping is None

    def test_wrong_key_returns_none(self):
        q = _make_question(cbcs_mapping={"A": {"social": 0.18}})
        mapping = extract_cbcs_mapping(q, "X")
        assert mapping is None

    def test_engine_process_qualifying(self):
        engine = TrivianarEngine()
        q = _make_question(cbcs_mapping={"A": {"social": 0.18}, "B": {"analytical": 0.22}})
        result = engine.process_qualifying(q, "B")
        assert result == {"analytical": 0.22}


# ═══════════════════════════════════════════════════════════════════════
# AC5: Reaction GIFs (Atmosphere Layer)
# ═══════════════════════════════════════════════════════════════════════


class TestReactionAtmosphere:
    """AC5: Reaction GIF selection from named pools."""

    def test_hype_reaction_exists(self):
        url = select_reaction(ReactionPool.PRE_QUESTION_HYPE.value)
        assert url is not None
        assert url.startswith("s3://")

    def test_correct_celebration(self):
        url = select_reaction(ReactionPool.CORRECT_ANSWER_CELEBRATION.value)
        assert url is not None

    def test_wrong_shock(self):
        url = select_reaction(ReactionPool.WRONG_ANSWER_SHOCK.value)
        assert url is not None

    def test_speed_record_reaction(self):
        url = select_reaction(ReactionPool.SPEED_RECORD.value)
        assert url is not None

    def test_commitment_empowerment(self):
        url = select_reaction(ReactionPool.COMMITMENT_EMPOWERMENT.value)
        assert url is not None

    def test_unknown_pool_returns_none(self):
        url = select_reaction("nonexistent_pool")
        assert url is None

    def test_custom_pools(self):
        custom = {"custom_pool": ["https://example.com/reaction.gif"]}
        url = select_reaction("custom_pool", pools=custom)
        assert url == "https://example.com/reaction.gif"

    def test_speed_record_flag_on_fast_answer(self):
        engine = TrivianarEngine()
        q = _make_question()
        result = engine.score_response(q, "A", 1500)
        assert result.is_speed_record is True
        assert result.score > 0

    def test_no_speed_record_if_slow(self):
        engine = TrivianarEngine()
        q = _make_question()
        result = engine.score_response(q, "A", 5000)
        assert result.is_speed_record is False


# ═══════════════════════════════════════════════════════════════════════
# AC6: Threaded Media Handler
# ═══════════════════════════════════════════════════════════════════════


class TestThreadedMedia:
    """AC6: Questions with media_url."""

    def test_question_with_media_url(self):
        q = _make_question(media_url="s3://assets/image.png")
        assert q.media_url == "s3://assets/image.png"

    def test_question_without_media(self):
        q = _make_question()
        assert q.media_url is None

    def test_question_with_fun_fact(self):
        q = _make_question(fun_fact="CCP was founded in 2024.")
        assert q.fun_fact == "CCP was founded in 2024."


# ═══════════════════════════════════════════════════════════════════════
# AC7: Survivor Mode
# ═══════════════════════════════════════════════════════════════════════


class TestSurvivorMode:
    """AC7: Survivor — wrong answer = eliminated."""

    def test_not_eliminated_initially(self):
        assert check_survivor_status([]) is False

    def test_eliminated_after_wrong(self):
        responses = [
            _make_response(is_correct=True),
            _make_response(is_correct=False),
        ]
        assert check_survivor_status(responses) is True

    def test_all_correct_not_eliminated(self):
        responses = [_make_response(is_correct=True) for _ in range(5)]
        assert check_survivor_status(responses) is False

    def test_engine_survivor_eliminates(self):
        engine = TrivianarEngine()
        q = _make_question()
        result = engine.score_response(
            q, "B", 3000,
            game_mode=TriviaGameMode.SURVIVOR.value,
        )
        assert result.is_eliminated is True
        assert result.score == 0

    def test_engine_survivor_correct(self):
        engine = TrivianarEngine()
        q = _make_question()
        result = engine.score_response(
            q, "A", 3000,
            game_mode=TriviaGameMode.SURVIVOR.value,
        )
        assert result.is_eliminated is False
        assert result.score == COUNTDOWN_MAX_SCORE

    def test_engine_already_eliminated_returns_early(self):
        engine = TrivianarEngine()
        q = _make_question()
        prev = [_make_response(is_correct=False)]
        result = engine.score_response(
            q, "A", 1000,
            game_mode=TriviaGameMode.SURVIVOR.value,
            previous_responses=prev,
        )
        assert result.is_eliminated is True
        assert result.score == 0


# ═══════════════════════════════════════════════════════════════════════
# AC8: Concurrency (Multiple Concurrent Answers)
# ═══════════════════════════════════════════════════════════════════════


class TestConcurrency:
    """AC8: Multiple users can answer concurrently (scoring is pure)."""

    def test_many_users_scored_independently(self):
        engine = TrivianarEngine()
        q = _make_question()
        results = [
            engine.score_response(q, "A", elapsed)
            for elapsed in [1000, 2000, 3000, 4000, 5000]
        ]
        scores = [r.score for r in results]
        assert scores == [900, 800, 700, 600, 500]

    def test_team_scoring(self):
        member_scores = [300, 400, 500]
        total = calculate_team_score(member_scores)
        assert total == 1200

    def test_team_empty(self):
        assert calculate_team_score([]) == 0


# ═══════════════════════════════════════════════════════════════════════
# AC9: Microcommitment Checkpoint
# ═══════════════════════════════════════════════════════════════════════


class TestMicrocommitment:
    """AC9: Microcommitment checkpoint model."""

    def test_create_microcommitment(self):
        mc = MicrocommitmentResponse(
            user_id=1,
            stream_id="stream-1",
            commitment_text="I will practice daily.",
        )
        assert mc.is_cbcs_priority is True
        assert mc.commitment_text == "I will practice daily."

    def test_microcommitment_validation(self):
        with pytest.raises(Exception):
            MicrocommitmentResponse(
                user_id=1,
                stream_id="stream-1",
                commitment_text="",
            )


# ═══════════════════════════════════════════════════════════════════════
# Wagering Mode
# ═══════════════════════════════════════════════════════════════════════


class TestWageringMode:
    """Wagering: correct = wager × 2, wrong = -wager, clamped [100, 500]."""

    def test_correct_wager(self):
        score = process_wager(200, is_correct=True)
        assert score == 400

    def test_wrong_wager(self):
        score = process_wager(200, is_correct=False)
        assert score == -200

    def test_wager_clamped_min(self):
        score = process_wager(50, is_correct=True)
        assert score == WAGER_MIN * 2  # 200

    def test_wager_clamped_max(self):
        score = process_wager(1000, is_correct=True)
        assert score == WAGER_MAX * 2  # 1000

    def test_engine_wagering_mode(self):
        engine = TrivianarEngine()
        q = _make_question()
        result = engine.score_response(
            q, "A", 3000,
            game_mode=TriviaGameMode.WAGERING.value,
            wager=300,
        )
        assert result.score == 600

    def test_engine_wagering_wrong(self):
        engine = TrivianarEngine()
        q = _make_question()
        result = engine.score_response(
            q, "B", 3000,
            game_mode=TriviaGameMode.WAGERING.value,
            wager=300,
        )
        assert result.score == -300


# ═══════════════════════════════════════════════════════════════════════
# Polls Mode
# ═══════════════════════════════════════════════════════════════════════


class TestPollsMode:
    """Polls mode: no scoring."""

    def test_polls_no_score(self):
        engine = TrivianarEngine()
        q = _make_question()
        result = engine.score_response(q, "A", 3000, game_mode=TriviaGameMode.POLLS.value)
        assert result.score == 0


# ═══════════════════════════════════════════════════════════════════════
# Batch Receipt + Receipt Chain
# ═══════════════════════════════════════════════════════════════════════


class TestBatchReceipt:
    """End-of-stream batch receipt for all responses."""

    def test_batch_receipt_hash_deterministic(self):
        responses = [
            _make_response(user_id=1, score=700),
            _make_response(user_id=2, score=500),
        ]
        h1 = compute_batch_receipt_hash(responses)
        h2 = compute_batch_receipt_hash(responses)
        assert h1 == h2

    def test_batch_receipt_changes_with_score(self):
        r1 = [_make_response(user_id=1, score=700)]
        r2 = [_make_response(user_id=1, score=800)]
        assert compute_batch_receipt_hash(r1) != compute_batch_receipt_hash(r2)

    def test_engine_emit_batch_receipt(self):
        engine = TrivianarEngine()
        responses = [
            _make_response(user_id=1, score=700),
            _make_response(user_id=2, score=500),
        ]
        receipt = engine.emit_batch_receipt("stream-1", responses)
        assert receipt["stage_name"] == "trivianar-batch"
        assert receipt["agent_name"] == TRIVIA_AGENT_NAME

    def test_receipt_chain_valid(self):
        engine = TrivianarEngine()
        r1 = [_make_response(user_id=1, score=700)]
        r2 = [_make_response(user_id=2, score=500)]
        engine.emit_batch_receipt("stream-1", r1)
        engine.emit_batch_receipt("stream-2", r2)
        assert engine.verify_receipt_chain() is True

    def test_receipt_chain_empty_is_valid(self):
        engine = TrivianarEngine()
        assert engine.verify_receipt_chain() is True


# ═══════════════════════════════════════════════════════════════════════
# SQL Tables + Constants
# ═══════════════════════════════════════════════════════════════════════


class TestSQLAndConstants:
    """Verify SQL schemas and constants."""

    def test_trivia_questions_sql(self):
        assert "trivia_questions" in TRIVIA_QUESTIONS_SQL
        assert "surface_text" in TRIVIA_QUESTIONS_SQL
        assert "correct_answer" in TRIVIA_QUESTIONS_SQL

    def test_trivia_responses_sql(self):
        assert "trivia_responses" in TRIVIA_RESPONSES_SQL
        assert "is_correct" in TRIVIA_RESPONSES_SQL
        assert "response_time_ms" in TRIVIA_RESPONSES_SQL
        assert "studio_sessions" in TRIVIA_RESPONSES_SQL  # FK

    def test_trivia_leaderboard_sql(self):
        assert "trivia_leaderboard" in TRIVIA_LEADERBOARD_SQL
        assert "total_score" in TRIVIA_LEADERBOARD_SQL
        assert "win_count" in TRIVIA_LEADERBOARD_SQL

    def test_countdown_max_score(self):
        assert COUNTDOWN_MAX_SCORE == 1000

    def test_countdown_divisor(self):
        assert COUNTDOWN_DIVISOR == 10

    def test_default_time_limit(self):
        assert DEFAULT_TIME_LIMIT_SECONDS == 15

    def test_leaderboard_size(self):
        assert LEADERBOARD_SIZE == 10

    def test_wager_range(self):
        assert WAGER_MIN == 100
        assert WAGER_MAX == 500

    def test_speed_threshold(self):
        assert SPEED_RECORD_THRESHOLD_MS == 2000

    def test_reaction_delay(self):
        assert REACTION_DELAY_MS == 500

    def test_agent_name(self):
        assert TRIVIA_AGENT_NAME == "Marco"

    def test_reaction_pools_defined(self):
        assert len(DEFAULT_REACTION_POOLS) == 5
        for pool_name in ReactionPool:
            assert pool_name.value in DEFAULT_REACTION_POOLS

    def test_game_modes(self):
        modes = [m.value for m in TriviaGameMode]
        assert "countdown" in modes
        assert "survivor" in modes
        assert "polls" in modes
        assert len(modes) == 6
