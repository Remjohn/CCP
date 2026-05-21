from fastapi import APIRouter
import uuid
from datetime import datetime, timedelta
from src.ccp.models.reaction_elimination_models import (
    LastOneStandingPromptPack,
    EliminationOption,
    EliminationRoundPrompt,
    TimerAggressionProfile,
    TimerAggressionLevel,
    LastOneStandingSessionProjection
)

router = APIRouter()

def get_aggression_profile(active_count: int) -> TimerAggressionProfile:
    if active_count >= 6:
        return TimerAggressionProfile(level=TimerAggressionLevel.CALM, pulse_duration_ms=2000, accent_token="--timer-calm", scale_amplitude=0.05, border_flash_enabled=False)
    elif active_count >= 4:
        return TimerAggressionProfile(level=TimerAggressionLevel.PRESSURED, pulse_duration_ms=1000, accent_token="--timer-pressured", scale_amplitude=0.1, border_flash_enabled=True)
    elif active_count >= 2:
        return TimerAggressionProfile(level=TimerAggressionLevel.INTENSE, pulse_duration_ms=500, accent_token="--timer-intense", scale_amplitude=0.2, border_flash_enabled=True)
    else:
        return TimerAggressionProfile(level=TimerAggressionLevel.FINAL, pulse_duration_ms=200, accent_token="--timer-final", scale_amplitude=0.3, border_flash_enabled=True)

@router.post("/reactions/elimination/session", response_model=LastOneStandingPromptPack)
async def create_session(payload: dict):
    coach_id = payload.get("coach_id", "default")
    session_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    options = []
    for i in range(1, 9):
        options.append(EliminationOption(option_id=f"opt_{i}", surface_text=f"Option {i}"))
        
    rounds = []
    active_count = 8
    for i in range(1, 8):
        rounds.append(EliminationRoundPrompt(
            round_index=i,
            active_option_count=active_count,
            aggression_profile=get_aggression_profile(active_count)
        ))
        active_count -= 1
        
    return LastOneStandingPromptPack(
        session_id=session_id,
        coach_id=coach_id,
        title="Last One Standing",
        options=options,
        rounds=rounds,
        issued_at=now,
        expires_at=now + timedelta(hours=1),
        ttl_seconds=3600
    )

@router.post("/reactions/elimination/finalize", response_model=LastOneStandingSessionProjection)
async def finalize_session(payload: dict):
    # Adapter logic goes here
    pass
