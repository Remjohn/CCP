from fastapi import APIRouter, Request
router = APIRouter()

@router.post("/cmf/arc-render/jobs")
async def create_arc_render_job(request: Request):
    body = await request.json()
    return {"status": "job_created"}

@router.get("/cmf/arc-render/jobs/{job_id}")
async def get_arc_render_job(job_id: str):
    return {"job_id": job_id, "status": "planned"}

@router.post("/cmf/arc-render/jobs/{job_id}/retry-first-frame")
async def retry_first_frame(job_id: str):
    return {"job_id": job_id, "status": "retrying"}

@router.post("/cmf/arc-render/jobs/{job_id}/request-regeneration")
async def request_regeneration(job_id: str, request: Request):
    body = await request.json()
    return {"job_id": job_id, "status": "regeneration_queued"}

@router.post("/cmf/arc-render/jobs/{job_id}/release")
async def release_job(job_id: str):
    return {"job_id": job_id, "status": "release_pending"}

@router.get("/cmf/arc-render/health")
async def arc_render_health():
    return {"skia_sidecar": "healthy", "abel": "healthy", "canvas": "healthy"}
