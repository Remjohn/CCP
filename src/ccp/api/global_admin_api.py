from fastapi import APIRouter, HTTPException, Depends
from typing import Any, Dict, List
from src.ccp.models.cross_system_models import DeploymentManifest
from src.ccp.models.global_admin_models import AdminAction, PipelineHealthSnapshot
from src.ccp.services.global_admin_service import GlobalAdminService
from src.ccp.services.container_cloning_service import ContainerCloningService

router = APIRouter()

# Singletons (Simulated In-Memory DI for control plane FastAPI instances)
cloning_service = ContainerCloningService()
admin_service = GlobalAdminService(cloning_service)

@router.post("/admin/provision")
async def provision_tenant(manifest: DeploymentManifest):
    """
    POST /api/admin/provision
    Provisons a brand new isolated client container environment.
    """
    try:
        tenant_row = admin_service.provision_new_client_container(manifest)
        return {
            "status": "success",
            "message": f"Tenant environment cloned and active for {manifest.coach_acronym}",
            "tenant": tenant_row.model_dump(mode="json")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/admin/preview/{coach_acronym}/{content_id}")
async def get_tenant_preview(coach_acronym: str, content_id: str):
    """
    GET /api/admin/preview/{coach_acronym}/{content_id}
    Secure Loopback Route: Queries client content inside their container.
    """
    try:
        res = await admin_service.forward_request_to_tenant(
            coach_acronym=coach_acronym,
            method="GET",
            path=f"/api/affine/studio/dashboard/{coach_acronym}"
        )
        return {
            "status": "success",
            "coach_acronym": coach_acronym,
            "content_id": content_id,
            "preview_data": res
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/admin/action")
async def submit_admin_action(action: AdminAction):
    """
    POST /api/admin/action
    Submits an approve/reject/regenerate action across container boundaries.
    """
    try:
        res = admin_service.execute_admin_action(action)
        return {
            "status": "success",
            "action_executed": res.model_dump(mode="json")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/admin/traffic-control", response_model=PipelineHealthSnapshot)
async def get_traffic_control_snapshot():
    """
    GET /api/admin/traffic-control
    Returns active GPU profiles and video rendering pipelines from client containers.
    """
    return admin_service.get_pipeline_health_snapshot()

@router.get("/admin/treasury")
async def get_treasury_metrics():
    """
    GET /api/admin/treasury
    Aggregates subscription status, credit burns, and revenue margins.
    """
    return admin_service.get_treasury_metrics()
