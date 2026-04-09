"""
Stage 1: SAM 3 Saliency Analysis Service
========================================
Extracts subject masks, text safe zones, and surface quadrilaterals
utilizing Meta's SAM 3 via Nvidia NIM API.

Integrates Constraint Precedence Hierarchy:
- CPH-7: Validated Asset Trust bypass for abstract/scene assets.
- CPH-3: Secondary mask extraction for depth occlusion.
"""

from __future__ import annotations

import hashlib
import json
import os
from typing import Any, List, Optional, Tuple

import httpx
from pydantic import BaseModel

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.spatial_engine_models import (
    CoordinateBox,
    SaliencyAnalysisOutput,
    SaliencyOverrideInfo,
)

# In production, Redis connection would be injected or imported globally
# Here we mock the interface for simplicity
class DummyRedis:
    def get(self, key: str) -> Optional[str]: return None
    def setex(self, key: str, ttl: int, val: str) -> None: pass

class NimVisionAPIClient:
    """Wrapper for Nvidia NIM Vision API (e.g., SAM, Llama 3.2 Vision)."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("NVIDIA_NIM_API_KEY", "")
        self.http_client = httpx.Client(timeout=30.0)

    def generate_saliency(self, image_url: str, query: str) -> dict:
        """
        Calls NVIDIA NIM SAM endpoint.
        Returns a mock response here to satisfy the architectural spec.
        """
        # In a real environment:
        # response = self.http_client.post(
        #     "https://integrate.api.nvidia.com/v1/cv/meta/segment-anything", 
        #     json={"image_url": image_url, "query": query}, 
        #     headers={"Authorization": f"Bearer {self.api_key}"}
        # )
        # return response.json()
        
        # Simulated response:
        return {
            "subject_mask": [[100.0, 100.0], [200.0, 100.0], [200.0, 400.0], [100.0, 400.0]],
            "subject_bbox": {"x": 100.0, "y": 100.0, "w": 100.0, "h": 300.0},
            "text_safe_zones": [{"x": 220.0, "y": 50.0, "w": 300.0, "h": 500.0}],
            "confidence": 0.85
        }


class SaliencyAnalysisService:
    """
    Executes Stage 1 of the Spatial Composition Engine Pipeline.
    """

    def __init__(
        self,
        coach_acronym: str,
        receipt_chain: ReceiptChain,
    ) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(f"Invalid coach acronym: '{coach_acronym}'")
        self._coach = coach_acronym
        self._rc = receipt_chain
        self._redis = DummyRedis()
        self._vision_client = NimVisionAPIClient()

    def analyze(
        self,
        image_url: str,
        image_type: str,
        agss_score: Optional[float] = None,
        depth_occlusion_requested: bool = False
    ) -> tuple[SaliencyAnalysisOutput, Optional[SaliencyOverrideInfo], str]:
        """
        Processes image URL and returns analysis.
        Returns SaliencyAnalysisOutput, Optional SaliencyOverrideInfo, and validation status ('PASS' or 'PENDING_HUMAN_REVIEW').
        """
        img_hash = hashlib.sha256(image_url.encode()).hexdigest()
        cache_key = f"sam3:saliency:{img_hash}:{image_type}"
        
        # Check cache
        cached = self._redis.get(cache_key)
        if cached:
            data = json.loads(cached)
            return SaliencyAnalysisOutput(**data), None, "PASS"

        # Construct Query
        query = self._construct_query(image_type)
        raw_output = self._vision_client.generate_saliency(image_url, query)

        confidence = raw_output.get("confidence", 0.0)
        validation_status = "PASS"
        saliency_override = None

        # CPH-7: Validated Asset Trust
        if confidence < 0.70:
            if agss_score is not None and agss_score >= 7.0:
                if image_type in ("environment_scene", "abstract_illustration"):
                    # Bypass saliency gate, use full canvas as text safe zone
                    saliency_override = SaliencyOverrideInfo(
                        reason="AGSS_TRUST",
                        upstream_agss_score=agss_score,
                        sam3_confidence=confidence
                    )
                    raw_output["text_safe_zones"] = [{"x": 0.0, "y": 0.0, "w": 1080.0, "h": 1350.0}]
                    validation_status = "PASS_WITH_OVERRIDE"
                elif image_type.startswith("character_"):
                    # Downgrade to advisory, conservative safe zone
                    saliency_override = SaliencyOverrideInfo(
                        reason="AGSS_TRUST",
                        upstream_agss_score=agss_score,
                        sam3_confidence=confidence
                    )
                    raw_output["text_safe_zones"] = [{"x": 0.0, "y": 0.0, "w": 1080.0, "h": 1350.0}]
                    validation_status = "PENDING_HUMAN_REVIEW"
            else:
                validation_status = "PENDING_HUMAN_REVIEW"

        # CPH-3: Secondary mask extraction for depth occlusion
        foreground_mask = None
        if depth_occlusion_requested and validation_status in ("PASS", "PASS_WITH_OVERRIDE"):
            fg_query = "Segment the foreground occluding element separately."
            fg_output = self._vision_client.generate_saliency(image_url, fg_query)
            if fg_output.get("confidence", 0) >= 0.70:
                foreground_mask = fg_output.get("subject_mask")
            else:
                # Fallback flat
                validation_status = "PROVISIONAL"

        output = SaliencyAnalysisOutput(
            subject_mask=raw_output.get("subject_mask"),
            subject_bbox=CoordinateBox(**raw_output.get("subject_bbox", {})) if "subject_bbox" in raw_output else None,
            text_safe_zones=[CoordinateBox(**z) for z in raw_output.get("text_safe_zones", [])],
            surface_quadrilateral=raw_output.get("surface_quadrilateral"),
            gaze_direction=raw_output.get("gaze_direction"),
            confidence=confidence,
            cache_key=cache_key,
            foreground_mask=foreground_mask
        )

        self._redis.setex(cache_key, 86400, output.model_dump_json())

        # Receipt writes
        self._rc.log(
            agent_id="saliency-analysis-service",
            action="saliency-extraction",
            asset_id=cache_key,
            input_summary=f"url_hash={img_hash[:8]} query={query}",
            output_summary=f"status={validation_status} confidence={confidence}",
            metadata={"coach": self._coach}
        )

        return output, saliency_override, validation_status


    def _construct_query(self, image_type: str) -> str:
        if image_type == "environment_scene":
            return "Identify the largest visually calm, low-contrast negative space zone."
        if image_type == "character_specific_emotion":
            return "Segment the person's face and upper body. Return bounding box."
        if image_type == "character_brand_avatar":
            return "Segment the person. Return alpha mask polygon and gaze direction vector."
        if "surface" in image_type.lower():
            return "Segment the blank writable surface the person is holding. Return quadrilateral corners."
        return "Segment the primary subject and return text safe zones."
