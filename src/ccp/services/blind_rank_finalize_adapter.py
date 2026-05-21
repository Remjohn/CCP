import uuid
from datetime import datetime, timedelta
from src.ccp.models.reaction_blind_rank_models import (
    BlindRankPromptPack,
    BlindRankItem,
    BlindRankStateName
)

def create_prompt_pack(coach_id: str) -> BlindRankPromptPack:
    session_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    # Mock items for now
    items = []
    for i in range(1, 6):
        items.append(BlindRankItem(
            item_id=f"{session_id}-item-{i}",
            reveal_index=i,
            surface_text_encrypted=f"encrypted_payload_{i}"
        ))

    return BlindRankPromptPack(
        session_id=session_id,
        coach_id=coach_id,
        slot_labels=["1", "2", "3", "4", "5"],
        ordered_items=items,
        current_state=BlindRankStateName.SESSION_READY,
        issued_at=now,
        expires_at=now + timedelta(days=1),
        ttl_seconds=86400
    )
