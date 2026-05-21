from src.ccp.models.experience_ladder_models import ExperienceStatePacket, RouteDecisionPacket

class ExperienceStateRepository:
    async def get_packet(self, client_id: str) -> ExperienceStatePacket | None:
        pass
        
    async def save_packet(self, packet: ExperienceStatePacket):
        pass

    async def save_route_event(self, decision: RouteDecisionPacket):
        pass
