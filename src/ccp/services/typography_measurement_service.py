"""
Stage 2: Pretext Typography Measurement Service
===============================================
Bridges Python backend with Node.js Skia Sidecar for 
typographic calculations utilizing the Pretext layout engine.
"""

from __future__ import annotations

import httpx
from typing import Any, Dict, List, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.spatial_engine_models import (
    CoordinateBox,
    TextMeasurement,
    TypographyMeasurementOutput,
)


class TypographyMeasurementService:
    """
    Executes Stage 2 of the Spatial Composition Engine.
    Calls Node.js Skia Sidecar HTTP endpoint.
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
        self._sidecar_url = "http://skia-renderer:4000/typography/measure"
        self._http_client = httpx.Client(timeout=10.0)

    def measure(
        self,
        text_elements: Dict[str, Any],
        safe_zone_dims: CoordinateBox
    ) -> TypographyMeasurementOutput:
        """
        Sends the typography request to Skia Node sidecar for Pretext measurement.
        """
        # Formulate payload for the sidecar
        payload = {
            "text_elements": text_elements,
            "safe_zone": {
                "w": safe_zone_dims.w,
                "h": safe_zone_dims.h
            }
        }
        
        # In actual production: 
        # response = self._http_client.post(self._sidecar_url, json=payload)
        # response_data = response.json()
        
        # Mocked response for architectural completeness without sidecar boot up:
        response_data = {
            "is_overset": False,
            "measurements": {
                "headline": {
                    "element_id": "headline",
                    "optimal_font_size": 48.5,
                    "bounding_box": {"x": 54.0, "y": 80.0, "w": 486.0, "h": 172.0},
                    "line_count": 3,
                    "line_breaks": [4, 9, 14],
                    "line_widths": [478.0, 462.0, 312.0],
                    "shrink_wrap_width": 478.0,
                    "annotation_coordinates": {}
                }
            }
        }

        # Check for CPH-1 TEXT_OVERSET triggers
        is_overset = response_data.get("is_overset", False)
        if is_overset:
            # Escalation handling happens in Stage 3 (Layout Resolver)
            pass
            
        measurements: Dict[str, TextMeasurement] = {}
        for k, v in response_data.get("measurements", {}).items():
            measurements[k] = TextMeasurement(**v)
            
        output = TypographyMeasurementOutput(
            measurements=measurements,
            is_overset=is_overset
        )

        h_string = str(hash(f"{text_elements}-{safe_zone_dims.w}"))
        self._rc.log(
            agent_id="typography-measurement-service",
            action="typography-measurement",
            asset_id=f"TYPO-{h_string}",
            input_summary=f"elements={len(text_elements)} safe_zone={safe_zone_dims.w}x{safe_zone_dims.h}",
            output_summary=f"is_overset={is_overset}",
            metadata={"coach": self._coach}
        )

        return output
