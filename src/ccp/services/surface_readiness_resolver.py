from src.ccp.models.experience_ladder_models import ExperienceStatePacket, SurfaceReadinessSnapshot

class SurfaceReadinessResolver:
    async def resolve(self, packet: ExperienceStatePacket) -> list[SurfaceReadinessSnapshot]:
        return []
