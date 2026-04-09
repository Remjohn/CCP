from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any

from src.ccp.pipelines.spatial_composition_pipeline import SpatialCompositionPipeline
from src.ccp.core.receipt_chain import ReceiptChain

router = APIRouter()

class SceComposeRequest(BaseModel):
    coach_acronym: str
    vcb: Dict[str, Any]
    image_url: str
    image_type: str
    agss_score: Optional[float] = None

@router.post("/spatial/compose")
async def compose_spatial_layout(body: SceComposeRequest):
    """
    Orchestrates the full Spatial Composition Pipeline
    SAM 3 -> Pretext -> Layout -> Skia -> Variant Score
    """
    try:
        tmp_dir = "/tmp"  # Mock dir for ReceiptChain logs
        rc = ReceiptChain(coach_acronym=body.coach_acronym, log_dir=tmp_dir)
        pipeline = SpatialCompositionPipeline(
            coach_acronym=body.coach_acronym,
            receipt_chain=rc
        )
        
        result = pipeline.execute(
            vcb=body.vcb,
            image_url=body.image_url,
            image_type=body.image_type,
            agss_score=body.agss_score
        )
        
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
