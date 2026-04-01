"""FR-CA11-19 — Interactive Trivianar Engine.

DEP-ENG-104: Trivianar Core Engine (FastAPI webhook + game state)
DEP-ENG-105: Game Mode Controllers (6 modes)
DEP-ENG-106: Qualifying Question Processor (CBCS mapping)
DEP-ENG-107: Reaction Atmosphere Layer (sticker/GIF)
DEP-ENG-108: Threaded Media Handler
DEP-ENG-109: Leaderboard Engine (per-stream + all-time)
DEP-ENG-110: Microcommitment Checkpoint
DEP-ENG-111-113: Reserved (session lifecycle, batch receipt, Redis fallback)

Agent: Marco (Trivianar Engine Operator)
Stress Test Q36: stream_latency_offset for HLS delta pacing
"""
from __future__ import annotations

import hashlib
import json
import random
import uuid
from datetime import datetime, timezone
from typing import Any, Optional, Protocol

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

# ---------------------------------------------------------------------------
# SQL (§5 Data Model)
# ---------------------------------------------------------------------------

TRIVIA_QUESTIONS_SQL = """
CREATE TABLE IF NOT EXISTS trivia_questions (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    coach_id            UUID NOT NULL REFERENCES coaches(id),
    surface_text        TEXT NOT NULL,
    answer_options      JSONB NOT NULL,
    correct_answer      VARCHAR(1) NOT NULL,
    dimension           VARCHAR(30),
    difficulty          VARCHAR(15) DEFAULT 'accessible',
    time_limit_seconds  INTEGER DEFAULT 15,
    media_url           TEXT,
    fun_fact            TEXT,
    cbcs_mapping        JSONB,
    round_id            UUID,
    created_at          TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_trivia_questions_coach ON trivia_questions(coach_id);
"""

TRIVIA_RESPONSES_SQL = """
CREATE TABLE IF NOT EXISTS trivia_responses (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             BIGINT NOT NULL,
    question_id         UUID NOT NULL REFERENCES trivia_questions(id),
    stream_id           UUID NOT NULL REFERENCES studio_sessions(id),
    answer              VARCHAR(1) NOT NULL,
    is_correct          BOOLEAN NOT NULL,
    score               INTEGER DEFAULT 0,
    response_time_ms    INTEGER,
    team_id             UUID,
    is_eliminated       BOOLEAN DEFAULT FALSE,
    qualifying_assessment JSONB,
    responded_at        TIMESTAMPTZ NOT NULL,
    created_at          TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_trivia_responses_stream ON trivia_responses(stream_id);
CREATE INDEX IF NOT EXISTS idx_trivia_responses_user ON trivia_responses(user_id);
"""

TRIVIA_LEADERBOARD_SQL = """
CREATE TABLE IF NOT EXISTS trivia_leaderboard (
    user_id         BIGINT NOT NULL,
    coach_id        UUID NOT NULL REFERENCES coaches(id),
    total_score     INTEGER DEFAULT 0,
    games_played    INTEGER DEFAULT 0,
    win_count       INTEGER DEFAULT 0,
    current_streak  INTEGER DEFAULT 0,
    longest_streak  INTEGER DEFAULT 0,
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (user_id, coach_id)
);
"""

# ---------------------------------------------------------------------------
# Default reaction pools (S3 URLs — §4 Stage 4)
# ---------------------------------------------------------------------------

DEFAULT_REACTION_POOLS: dict[str, list[str]] = {
    ReactionPool.PRE_QUESTION_HYPE.value: [
        "s3://ccp-assets/trivianar/reactions/hype/drumroll.gif",
        "s3://ccp-assets/trivianar/reactions/hype/countdown.gif",
        "s3://ccp-assets/trivianar/reactions/hype/thinking.gif",
    ],
    ReactionPool.CORRECT_ANSWER_CELEBRATION.value: [
        "s3://ccp-assets/trivianar/reactions/correct/party.gif",
        "s3://ccp-assets/trivianar/reactions/correct/fireworks.gif",
        "s3://ccp-assets/trivianar/reactions/correct/highfive.gif",
    ],
    ReactionPool.WRONG_ANSWER_SHOCK.value: [
        "s3://ccp-assets/trivianar/reactions/wrong/shocked.gif",
        "s3://ccp-assets/trivianar/reactions/wrong/facepalm.gif",
    ],
    ReactionPool.SPEED_RECORD.value: [
        "s3://ccp-assets/trivianar/reactions/speed/lightning.gif",
        "s3://ccp-assets/trivianar/reactions/speed/flash.gif",
    ],
    ReactionPool.COMMITMENT_EMPOWERMENT.value: [
        "s3://ccp-assets/trivianar/reactions/commit/muscle.gif",
        "s3://ccp-assets/trivianar/reactions/commit/champion.gif",
    ],
}

# ---------------------------------------------------------------------------
# Protocols
# ---------------------------------------------------------------------------


class TriviaDatabaseProtocol(Protocol):
    async def get_questions(self, question_set_id: str) -> list[dict[str, Any]]: ...
    async def insert_response(self, record: dict[str, Any]) -> str: ...
    async def get_stream_responses(self, stream_id: str) -> list[dict[str, Any]]: ...
    async def update_leaderboard(self, user_id: int, coach_id: str, score_delta: int) -> None: ...


# ---------------------------------------------------------------------------
# Receipt utilities (FR47 DEP-ENG-041)
# ---------------------------------------------------------------------------


def _sha256(payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _build_receipt(
    stage_name: str, agent_name: str,
    input_payload: Any, output_payload: Any,
    previous_receipt_hash: str = "",
) -> dict[str, Any]:
    return {
        "receipt_id": str(uuid.uuid4()),
        "previous_receipt_hash": previous_receipt_hash,
        "input_payload_hash": _sha256(input_payload),
        "output_payload_hash": _sha256(output_payload),
        "stage_name": stage_name,
        "agent_name": agent_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Scoring functions (Stage 2 — DEP-ENG-105)
# ---------------------------------------------------------------------------


def calculate_countdown_score(elapsed_ms: int, is_correct: bool) -> int:
    """§4 Stage 2 Step 1: Countdown scoring.

    score = max(0, 1000 - elapsed_ms / 10). AC2: 3000ms → 700 points.
    """
    if not is_correct:
        return 0
    return max(0, COUNTDOWN_MAX_SCORE - elapsed_ms // COUNTDOWN_DIVISOR)


def calculate_team_score(member_scores: list[int]) -> int:
    """§4 Stage 2 Step 2: Team score = sum of member scores."""
    return sum(member_scores)


def process_wager(wager: int, is_correct: bool) -> int:
    """§4 Stage 2 Step 4: Wagering mode.

    Correct = wager × 2, wrong = -wager.
    Wager clamped to [100, 500].
    """
    clamped = max(WAGER_MIN, min(WAGER_MAX, wager))
    return clamped * 2 if is_correct else -clamped


def check_survivor_status(
    previous_responses: list[TriviaResponse],
) -> bool:
    """§4 Stage 2 Step 5: Survivor mode — check if user is eliminated.

    Returns True if the user has been eliminated (has any wrong answer).
    """
    return any(not r.is_correct for r in previous_responses)


# ---------------------------------------------------------------------------
# Reaction selection (Stage 4 — DEP-ENG-107)
# ---------------------------------------------------------------------------


def select_reaction(
    pool_name: str,
    pools: dict[str, list[str]] | None = None,
) -> Optional[str]:
    """§4 Stage 4: Select random reaction from named pool."""
    source = pools or DEFAULT_REACTION_POOLS
    pool = source.get(pool_name, [])
    if not pool:
        return None
    return random.choice(pool)


# ---------------------------------------------------------------------------
# Qualifying question processor (Stage 3 — DEP-ENG-106)
# ---------------------------------------------------------------------------


def extract_cbcs_mapping(
    question: TriviaQuestion,
    answer_key: str,
) -> Optional[dict[str, Any]]:
    """§4 Stage 3 Step 1: Extract CBCS mapping from selected answer option.

    Each answer option may have a `cbcs_mapping` dict that maps to
    behavioral parameters (e.g., {"social": 0.18}).
    """
    if not question.cbcs_mapping:
        return None

    # cbcs_mapping is keyed by answer letter
    return question.cbcs_mapping.get(answer_key)


# ---------------------------------------------------------------------------
# Leaderboard computation (Stage 6 — DEP-ENG-109)
# ---------------------------------------------------------------------------


def compute_leaderboard(
    responses: list[TriviaResponse],
    limit: int = LEADERBOARD_SIZE,
) -> list[LeaderboardEntry]:
    """§4 Stage 6 Step 1: Compute per-stream leaderboard.

    GROUP BY user_id, SUM(score), ORDER BY total DESC.
    """
    user_scores: dict[int, int] = {}
    for r in responses:
        user_scores[r.user_id] = user_scores.get(r.user_id, 0) + r.score

    sorted_users = sorted(user_scores.items(), key=lambda x: x[1], reverse=True)

    entries: list[LeaderboardEntry] = []
    for rank, (user_id, total) in enumerate(sorted_users[:limit], start=1):
        entries.append(LeaderboardEntry(
            rank=rank,
            user_id=user_id,
            total_score=total,
        ))
    return entries


# ---------------------------------------------------------------------------
# Batch receipt (Stage 6 Step 5 — exemption + batch-hash)
# ---------------------------------------------------------------------------


def compute_batch_receipt_hash(responses: list[TriviaResponse]) -> str:
    """§4 Stage 6 Step 5: Single batch hash for all stream responses.

    Individual trivia responses are exempt from per-row receipting.
    Instead, hash all response IDs + scores for the stream.
    """
    payload = [
        {"id": r.response_id, "user_id": r.user_id, "score": r.score, "answer": r.answer}
        for r in sorted(responses, key=lambda r: r.responded_at)
    ]
    return _sha256(payload)


# ---------------------------------------------------------------------------
# Trivianar Engine Service
# ---------------------------------------------------------------------------


class TrivianarEngine:
    """FR-CA11-19 — Interactive Trivianar Engine.

    Stateless scoring + game logic. All state via DB.
    Batch receipt at end-of-stream (no per-response receipting).
    """

    def __init__(self, db: TriviaDatabaseProtocol | None = None) -> None:
        self._db = db
        self._receipt_chain: list[dict[str, Any]] = []

    @property
    def receipt_chain(self) -> list[dict[str, Any]]:
        return list(self._receipt_chain)

    def _emit_receipt(
        self, stage_name: str, input_payload: Any, output_payload: Any,
    ) -> dict[str, Any]:
        prev_hash = ""
        if self._receipt_chain:
            prev_hash = _sha256(self._receipt_chain[-1])
        receipt = _build_receipt(
            stage_name=stage_name,
            agent_name=TRIVIA_AGENT_NAME,
            input_payload=input_payload,
            output_payload=output_payload,
            previous_receipt_hash=prev_hash,
        )
        self._receipt_chain.append(receipt)
        return receipt

    # -- Session lifecycle --

    def start_session(self, config: TriviaSessionConfig) -> TrivianarResult:
        """§4 Stage 1 Step 4: Activate trivia for a stream."""
        return TrivianarResult(success=True, session_config=config)

    # -- Score a response --

    def score_response(
        self,
        question: TriviaQuestion,
        answer: str,
        elapsed_ms: int,
        game_mode: str = TriviaGameMode.COUNTDOWN.value,
        wager: int = 0,
        previous_responses: Optional[list[TriviaResponse]] = None,
    ) -> ScoringResult:
        """Score a single response based on game mode."""
        is_correct = answer == question.correct_answer
        is_speed = elapsed_ms < SPEED_RECORD_THRESHOLD_MS and is_correct
        is_eliminated = False
        score = 0

        if game_mode == TriviaGameMode.COUNTDOWN.value:
            score = calculate_countdown_score(elapsed_ms, is_correct)

        elif game_mode == TriviaGameMode.TEAM.value:
            score = calculate_countdown_score(elapsed_ms, is_correct)

        elif game_mode == TriviaGameMode.MULTI_ROUND.value:
            score = calculate_countdown_score(elapsed_ms, is_correct)

        elif game_mode == TriviaGameMode.WAGERING.value:
            score = process_wager(wager, is_correct)

        elif game_mode == TriviaGameMode.SURVIVOR.value:
            if previous_responses and check_survivor_status(previous_responses):
                return ScoringResult(is_eliminated=True)
            score = COUNTDOWN_MAX_SCORE if is_correct else 0
            is_eliminated = not is_correct

        elif game_mode == TriviaGameMode.POLLS.value:
            score = 0

        return ScoringResult(
            score=score,
            is_correct=is_correct,
            is_speed_record=is_speed,
            is_eliminated=is_eliminated,
        )

    # -- Leaderboard --

    def get_leaderboard(self, responses: list[TriviaResponse]) -> list[LeaderboardEntry]:
        """Compute current leaderboard from responses."""
        return compute_leaderboard(responses)

    # -- Qualifying question --

    def process_qualifying(
        self, question: TriviaQuestion, answer_key: str,
    ) -> Optional[dict[str, Any]]:
        """Extract CBCS mapping from a qualifying question response."""
        return extract_cbcs_mapping(question, answer_key)

    # -- Reactions --

    @staticmethod
    def get_reaction(pool_name: str) -> Optional[str]:
        """Select a reaction GIF/sticker from a pool."""
        return select_reaction(pool_name)

    # -- End-of-stream batch receipt --

    def emit_batch_receipt(
        self,
        stream_id: str,
        responses: list[TriviaResponse],
    ) -> dict[str, Any]:
        """§4 Stage 6 Step 5: Batch-hash receipt for all stream responses."""
        response_hash = compute_batch_receipt_hash(responses)
        user_ids = set(r.user_id for r in responses)

        payload = BatchReceiptPayload(
            stream_id=stream_id,
            total_responses=len(responses),
            total_users=len(user_ids),
            response_hash=response_hash,
        )

        receipt = self._emit_receipt(
            stage_name="trivianar-batch",
            input_payload={"stream_id": stream_id, "response_count": len(responses)},
            output_payload=payload.model_dump(),
        )
        return receipt

    # -- Receipt chain verification --

    def verify_receipt_chain(self) -> bool:
        if not self._receipt_chain:
            return True
        if self._receipt_chain[0]["previous_receipt_hash"] != "":
            return False
        for i in range(1, len(self._receipt_chain)):
            expected = _sha256(self._receipt_chain[i - 1])
            if self._receipt_chain[i]["previous_receipt_hash"] != expected:
                return False
        return True
