from fastapi import APIRouter
import uuid
from datetime import datetime, timedelta
from src.ccp.models.reaction_alphabet_models import (
    AlphabetChallengePromptPack,
    AlphabetChallengeRoundPrompt,
    AlphabetFinalizePayload,
    AlphabetChallengeSessionProjection,
    TimingVerificationStatus
)
from src.ccp.services.alphabet_answer_validation_service import AlphabetAnswerValidationService
from src.ccp.services.alphabet_timing_verifier import AlphabetTimingVerifier

router = APIRouter()
validation_service = AlphabetAnswerValidationService()
timing_verifier = AlphabetTimingVerifier()

@router.post("/reactions/alphabet/session", response_model=AlphabetChallengePromptPack)
async def create_session(payload: dict):
    coach_id = payload.get("coach_id", "default")
    session_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    rounds = []
    for i, letter in enumerate(["A", "C", "T", "I", "O", "N"], start=1):
        rounds.append(AlphabetChallengeRoundPrompt(
            round_index=i,
            letter=letter,
            category_prompt="Industry Terms",
            answer_window_ms=3000
        ))
        
    return AlphabetChallengePromptPack(
        session_id=session_id,
        coach_id=coach_id,
        challenge_title="Action Alphabet",
        rounds=rounds,
        issued_at=now,
        expires_at=now + timedelta(hours=1),
        ttl_seconds=3600
    )

@router.post("/reactions/alphabet/finalize", response_model=AlphabetChallengeSessionProjection)
async def finalize_session(payload: AlphabetFinalizePayload):
    # Verify Timing
    verified_timing = timing_verifier.verify(payload.timing_payload)
    
    # Process semantic validity and build projection
    rounds_passed_in_time = 0
    rounds_semantically_valid = 0
    
    for i, round_res in enumerate(verified_timing.round_results):
        # Determine pass/fail
        if round_res.timing.timing_pass:
            rounds_passed_in_time += 1
            
        semantic_val = validation_service.evaluate(payload.coach_id, round_res.prompt, round_res.captured_phrase)
        round_res.semantic_validity = semantic_val
        if semantic_val == "valid":
            rounds_semantically_valid += 1
            
        if not round_res.timing.timing_pass:
            round_res.failure_reason = "timeout"
        elif semantic_val == "invalid":
            round_res.failure_reason = "invalid_term"
        elif i in verified_timing.suspicious_round_indexes:
            round_res.failure_reason = "suspicious_timing"
            
    export_eligible = False
    if verified_timing.verification_status != TimingVerificationStatus.SUSPICIOUS:
        if rounds_semantically_valid >= (len(verified_timing.round_results) * 0.8):
            export_eligible = True

    return AlphabetChallengeSessionProjection(
        session_id=payload.session_id,
        coach_id=payload.coach_id,
        prompt_pack=payload.prompt_pack,
        round_results=verified_timing.round_results,
        rounds_passed_in_time=rounds_passed_in_time,
        rounds_semantically_valid=rounds_semantically_valid,
        verification_status=verified_timing.verification_status,
        scoring_status="processing",
        export_eligible=export_eligible,
        score_ready=False
    )
