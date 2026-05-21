"""
Integration tests for FR-ERA3-35A Eval Registry and Scoring Taxonomy.
"""

from __future__ import annotations

import pytest
from src.ccp.models.eval_registry_models import (
    VisibleFamilyKey,
    MetricScale,
    EvalDefinition,
    EvalCluster,
    VisibleScoreFamily,
    HiddenClusterKey,
    HiddenSupportCluster,
    EvalMeasurement,
    EvalPenaltyRule,
    EvalScoreProjection
)
from src.ccp.services.eval_registry_service import EvalRegistryService


def test_eval_registry_initialization():
    """Assert registry registers all seven public families, internal clusters, and hidden support clusters."""
    service = EvalRegistryService()
    
    # 1. Seven Visible Families check
    assert len(service.visible_families) == 7
    for key in VisibleFamilyKey:
        assert key in service.visible_families
        assert service.visible_families[key].family_key == key
        
    # 2. Clusters mapping check
    assert len(service.clusters) == 7
    for key in VisibleFamilyKey:
        assert key in service.clusters
        cluster = service.clusters[key]
        assert cluster.target_family == key
        assert len(cluster.metrics) >= 1
        
    # 3. Hidden Support check
    assert len(service.hidden_support) == 2
    assert HiddenClusterKey.STRUCTURE in service.hidden_support
    assert HiddenClusterKey.ACTIONABILITY in service.hidden_support


def test_query_metric():
    """Assert query_metric returns correct EvalDefinition or None if non-existent."""
    service = EvalRegistryService()
    
    # Known metric
    metric = service.query_metric("MET-LIVEXP")
    assert isinstance(metric, EvalDefinition)
    assert metric.name == "Lived Experience Density"
    assert metric.scale == MetricScale.PROBABILITY
    
    # Unknown metric
    assert service.query_metric("MET-NONEXISTENT") is None


def test_normalization_math():
    """Assert normalization math enforces 0-99 range across various scales."""
    service = EvalRegistryService()
    
    # 1. Probability [0.0 - 1.0] -> [0 - 99]
    assert service.normalize_value(0.0, MetricScale.PROBABILITY) == 0
    assert service.normalize_value(0.5, MetricScale.PROBABILITY) == 49
    assert service.normalize_value(1.0, MetricScale.PROBABILITY) == 99
    # Bounds safety checks
    assert service.normalize_value(-0.5, MetricScale.PROBABILITY) == 0
    assert service.normalize_value(1.5, MetricScale.PROBABILITY) == 99
    
    # 2. Percentage [0.0 - 100.0] -> [0 - 99]
    assert service.normalize_value(0.0, MetricScale.PERCENTAGE) == 0
    assert service.normalize_value(50.0, MetricScale.PERCENTAGE) == 49
    assert service.normalize_value(100.0, MetricScale.PERCENTAGE) == 99
    assert service.normalize_value(-10.0, MetricScale.PERCENTAGE) == 0
    assert service.normalize_value(120.0, MetricScale.PERCENTAGE) == 99

    # 3. Count [0 - 10] -> [0 - 99]
    assert service.normalize_value(0, MetricScale.COUNT) == 0
    assert service.normalize_value(5, MetricScale.COUNT) == 49
    assert service.normalize_value(10, MetricScale.COUNT) == 99
    assert service.normalize_value(-2, MetricScale.COUNT) == 0
    assert service.normalize_value(15, MetricScale.COUNT) == 99


def test_calculate_projection_clean_run():
    """Assert canonical scoring projection computes weighted cluster averages and enforces range bounds."""
    service = EvalRegistryService()
    
    # Baseline raw measurements representing an excellent prospect target
    raw_measurements = {
        "MET-LIVEXP": 0.85,
        "MET-PROCTR": 0.80,
        "MET-EMOTSP": 0.90,
        "MET-HUMTXT": 0.85,
        
        "MET-CONVDN": 0.90,
        "MET-AURAIT": 0.85,
        "MET-DELMAG": 0.80,
        
        "MET-PROFDN": 0.85,
        "MET-VISANC": 0.90,
        "MET-CRECON": 0.85,
        
        "MET-PHRCOM": 0.80,
        "MET-SYMREC": 0.75,
        "MET-HKPERS": 0.85,
        
        "MET-EMOCHG": 0.80,
        "MET-SUBDEP": 0.85,
        "MET-FLTREL": 0.80,
        
        "MET-ANTGEN": 0.85,
        "MET-OPSHRP": 0.90,
        "MET-NICSPC": 0.80,
        
        # Low AI Slop Risk (0.15) to prevent slop penalties
        "MET-DEDPOL": 0.15,
        "MET-OVSMTH": 0.10,
        "MET-STAFTY": 0.20
    }
    
    projection = service.calculate_projection(
        raw_measurements=raw_measurements,
        is_qa_reviewed=True,
        operator_id="JP1"
    )
    
    assert isinstance(projection, EvalScoreProjection)
    assert projection.overall_score >= 70
    assert projection.overall_score <= 99
    assert projection.is_internally_approved is True
    assert projection.qa_signature is not None
    assert "JP1" in projection.qa_signature
    
    # Ensure all visible families are mapped in visible_scores dictionary
    assert len(projection.visible_scores) == 7
    for key in VisibleFamilyKey:
        assert key in projection.visible_scores
        score = projection.visible_scores[key]
        assert 0 <= score <= 99


def test_ai_slop_risk_penalty_rules():
    """Assert AI Slop Risk penalty caps the overall score at 59 and reduces overall score when slop exceeds 40."""
    service = EvalRegistryService()
    
    # Measurements with high AI Slop Risk (0.80 -> normalized 79 score)
    raw_measurements = {
        "MET-LIVEXP": 0.85, "MET-PROCTR": 0.80, "MET-EMOTSP": 0.90, "MET-HUMTXT": 0.85,
        "MET-CONVDN": 0.90, "MET-AURAIT": 0.85, "MET-DELMAG": 0.80,
        "MET-PROFDN": 0.85, "MET-VISANC": 0.90, "MET-CRECON": 0.85,
        "MET-PHRCOM": 0.80, "MET-SYMREC": 0.75, "MET-HKPERS": 0.85,
        "MET-EMOCHG": 0.80, "MET-SUBDEP": 0.85, "MET-FLTREL": 0.80,
        "MET-ANTGEN": 0.85, "MET-OPSHRP": 0.90, "MET-NICSPC": 0.80,
        
        # High AI Slop Risk metrics
        "MET-DEDPOL": 0.80,
        "MET-OVSMTH": 0.85,
        "MET-STAFTY": 0.75
    }
    
    projection = service.calculate_projection(
        raw_measurements=raw_measurements,
        is_qa_reviewed=False
    )
    
    # Hard RUL-SLOP-CAP enforces a hard overall score cap of 59
    assert projection.visible_scores[VisibleFamilyKey.AI_SLOP_RISK] > 40
    assert projection.overall_score <= 59
    assert projection.is_internally_approved is False
    assert projection.qa_signature is None


def test_critical_score_floor_caps():
    """Assert that if Humanity or Trust falls below 40, the overall score is capped at 59."""
    service = EvalRegistryService()
    
    # Trust is extremely low (0.25 -> 24 score)
    raw_measurements = {
        "MET-LIVEXP": 0.85, "MET-PROCTR": 0.80, "MET-EMOTSP": 0.90, "MET-HUMTXT": 0.85,
        "MET-CONVDN": 0.90, "MET-AURAIT": 0.85, "MET-DELMAG": 0.80,
        
        # Critically Low Trust
        "MET-PROFDN": 0.20,
        "MET-VISANC": 0.30,
        "MET-CRECON": 0.25,
        
        "MET-PHRCOM": 0.80, "MET-SYMREC": 0.75, "MET-HKPERS": 0.85,
        "MET-EMOCHG": 0.80, "MET-SUBDEP": 0.85, "MET-FLTREL": 0.80,
        "MET-ANTGEN": 0.85, "MET-OPSHRP": 0.90, "MET-NICSPC": 0.80,
        "MET-DEDPOL": 0.15, "MET-OVSMTH": 0.10, "MET-STAFTY": 0.20
    }
    
    projection = service.calculate_projection(
        raw_measurements=raw_measurements,
        is_qa_reviewed=True,
        operator_id="JP1"
    )
    
    assert projection.visible_scores[VisibleFamilyKey.TRUST] < 40
    assert projection.overall_score <= 59
