from src.ccp.models.experience_ladder_models import AsyncExhaustJob, SurfaceType
from uuid import uuid4
from datetime import datetime

class AsyncContentExhaustLauncher:
    def launch(self, route_id: str, client_id: str, surface: SurfaceType) -> AsyncExhaustJob:
        job_type = "unknown"
        if surface == SurfaceType.law28:
            job_type = "transcript_analysis_and_cmf_render"
        elif surface == SurfaceType.webinar:
            job_type = "session_telemetry_aggregation"
        elif surface == SurfaceType.networking:
            job_type = "ofap_connection_scoring"
        elif surface == SurfaceType.social:
            job_type = "reaction_clip_export"
            
        return AsyncExhaustJob(
            job_id=str(uuid4()),
            client_id=client_id,
            surface=surface,
            source_route_id=route_id,
            job_type=job_type,
            status="enqueued",
            created_at=datetime.utcnow()
        )
