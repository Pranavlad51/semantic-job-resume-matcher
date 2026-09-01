"""
tests/test_similarity.py
Unit tests for similarity calculation module
"""

import pytest
import numpy as np
from src.similarity import (
    calculate_cosine_similarity,
    similarity_to_percentage,
    get_similarity_level
)


def test_cosine_similarity_identical():
    """Test cosine similarity with identical vectors."""
    vec1 = np.array([1, 0, 0])
    vec2 = np.array([1, 0, 0])
    similarity = calculate_cosine_similarity(vec1, vec2)
    assert similarity == pytest.approx(1.0, abs=0.01)


def test_cosine_similarity_perpendicular():
    """Test cosine similarity with perpendicular vectors."""
    vec1 = np.array([1, 0, 0])
    vec2 = np.array([0, 1, 0])
    similarity = calculate_cosine_similarity(vec1, vec2)
    assert similarity == pytest.approx(0.0, abs=0.01)


def test_cosine_similarity_partial():
    """Test cosine similarity with partially similar vectors."""
    vec1 = np.array([1, 1, 0])
    vec2 = np.array([1, 0, 0])
    similarity = calculate_cosine_similarity(vec1, vec2)
    # Should be around 0.707 (cos(45°))
    assert 0.5 < similarity < 1.0


def test_similarity_to_percentage():
    """Test conversion to percentage."""
    assert similarity_to_percentage(0.0) == 0.0
    assert similarity_to_percentage(1.0) == 100.0
    assert similarity_to_percentage(0.5) == 50.0


def test_get_similarity_level():
    """Test qualitative similarity levels."""
    assert get_similarity_level(95) == "Excellent Match"
    assert get_similarity_level(75) == "Good Match"
    assert get_similarity_level(60) == "Moderate Match"
    assert get_similarity_level(45) == "Weak Match"
    assert get_similarity_level(20) == "Poor Match"
