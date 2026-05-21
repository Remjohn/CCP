"""
tests/unit/test_frera35b_weight_validation.py
============================================
Unit tests for weight map sum and range validation under FR-ERA3-35B.
"""

import pytest
from pydantic import ValidationError
from src.ccp.models.benchmark_profile_models import VisibleScoreWeightMap


def test_weight_sum_exactly_one_passes():
    """Verify that a weight map summing to exactly 1.0 is valid."""
    weight_map = VisibleScoreWeightMap(
        humanity=0.20,
        presence=0.15,
        trust=0.25,
        memorability=0.15,
        resonance=0.10,
        signal=0.15
    )
    assert weight_map.humanity == 0.20
    assert weight_map.presence == 0.15
    assert weight_map.trust == 0.25
    assert weight_map.memorability == 0.15
    assert weight_map.resonance == 0.10
    assert weight_map.signal == 0.15


def test_weight_sum_below_099_fails():
    """Verify that a weight map summing to less than 0.99 raises a validation error."""
    with pytest.raises(ValidationError) as exc_info:
        VisibleScoreWeightMap(
            humanity=0.10,
            presence=0.10,
            trust=0.25,
            memorability=0.15,
            resonance=0.10,
            signal=0.15
        )
    assert "Weights must sum to 1.0" in str(exc_info.value)


def test_weight_sum_above_101_fails():
    """Verify that a weight map summing to more than 1.01 raises a validation error."""
    with pytest.raises(ValidationError) as exc_info:
        VisibleScoreWeightMap(
            humanity=0.30,
            presence=0.30,
            trust=0.25,
            memorability=0.15,
            resonance=0.10,
            signal=0.15
        )
    assert "Weights must sum to 1.0" in str(exc_info.value)


def test_individual_weight_negative_fails():
    """Verify that any individual weight below 0.0 raises a validation error."""
    with pytest.raises(ValidationError) as exc_info:
        VisibleScoreWeightMap(
            humanity=-0.10,
            presence=0.30,
            trust=0.25,
            memorability=0.15,
            resonance=0.15,
            signal=0.25
        )
    assert "Input should be greater than or equal to 0" in str(exc_info.value)


def test_individual_weight_above_one_fails():
    """Verify that any individual weight above 1.0 raises a validation error."""
    with pytest.raises(ValidationError) as exc_info:
        VisibleScoreWeightMap(
            humanity=1.20,
            presence=0.00,
            trust=0.00,
            memorability=0.00,
            resonance=0.00,
            signal=0.00
        )
    assert "Input should be less than or equal to 1" in str(exc_info.value)
