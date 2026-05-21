from src.ccp.models.experience_ladder_models import ExperienceStatePacket, RecoveryState

class MomentumAndComebackEngine:
    async def process(self, packet: ExperienceStatePacket) -> ExperienceStatePacket:
        return packet
