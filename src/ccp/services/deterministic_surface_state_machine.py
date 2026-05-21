from src.ccp.models.experience_ladder_models import (
    ExperienceStatePacket, RouteDecisionPacket, SurfaceType, NextStepType, RouteReason,
    LadderStage, RecoveryState
)
from uuid import uuid4
from datetime import datetime
import time

class DeterministicSurfaceStateMachine:
    def decide(self, packet: ExperienceStatePacket, start_time: float) -> tuple[SurfaceType, RouteDecisionPacket]:
        to_surface = SurfaceType.law28
        reason = RouteReason.active_surface_continuation
        next_step = NextStepType.next_drill

        if packet.recovery_state in [RecoveryState.comeback_due, RecoveryState.habit_broken]:
            to_surface = SurfaceType.law28
            reason = RouteReason.comeback_recovery
            next_step = NextStepType.recovery_invitation
        elif packet.recovery_state == RecoveryState.shame_sensitive:
            to_surface = packet.active_surface
            reason = RouteReason.comeback_recovery
            next_step = NextStepType.recovery_invitation
        else:
            if packet.stage == LadderStage.discover:
                to_surface = SurfaceType.law28
                next_step = NextStepType.next_drill
            elif packet.stage == LadderStage.onboard:
                to_surface = SurfaceType.law28
                next_step = NextStepType.scorecard_step

        latency = int((time.time() - start_time) * 1000)

        decision = RouteDecisionPacket(
            route_id=str(uuid4()),
            client_id=packet.client_id,
            from_surface=packet.active_surface,
            to_surface=to_surface,
            reason=reason,
            next_step_type=next_step,
            next_step_label="Next step",
            route_latency_ms=latency,
            decided_at=datetime.utcnow()
        )
        return to_surface, decision
