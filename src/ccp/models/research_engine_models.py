from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class TScoreDetails(BaseModel):
    overall: float
    emotional_mode_match: float
    tribal_authenticity: float
    pssl_alignment: float
    anti_ai_score: float
    compositional_usability: float

class ImageAlternative(BaseModel):
    rank: int
    source_platform: str
    resolved_image_url: str
    t_score_overall: float
    attribution: str

class ResolutionMapEntry(BaseModel):
    slide_number: int
    image_type: str
    resolution_tier: int
    resolution_source: str
    source_platform: str
    resolved_image_url: str
    t_score: TScoreDetails
    attribution: str
    licensing_status: str
    licensing_routing_action: str
    runninghub_required: bool
    alternatives: List[ImageAlternative] = Field(default_factory=list)

class ImageResolutionMap(BaseModel):
    vcb_id: str
    resolution_map: List[ResolutionMapEntry]

# DEP-VIS-020 Schema
class TScoreDimension(BaseModel):
    name: str
    weight: float
    scoring_scale: List[float]
    vlm_prompt_instruction: str
    inputs: List[str]

class TScoreConfiguration(BaseModel):
    dependency_id: str = "DEP-VIS-020"
    name: str = "T-Score Configuration"
    version: str = "1.0"
    dimensions: List[TScoreDimension]
    passing_threshold: float = 0.65
    top_selection_count: int = 3
    alternatives_count: int = 5
