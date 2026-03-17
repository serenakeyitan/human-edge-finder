"""Shared fixtures for tests."""

import pytest


@pytest.fixture
def sample_skills():
    """Sample skills for testing."""
    return [
        "coding",
        "counseling",
        "teaching",
        "data analysis",
        "emotional intelligence",
    ]


@pytest.fixture
def edge_skills():
    """Skills that should have strong human edge."""
    return [
        "emotional intelligence",
        "counseling",
        "improvisation",
    ]


@pytest.fixture
def ai_skills():
    """Skills where AI should be strong."""
    return [
        "coding",
        "math",
        "grammar correction",
    ]
