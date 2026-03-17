"""Tests for domain definitions."""

from human_edge_finder.domains import (
    AI_CAPABILITIES,
    HUMAN_EDGE_DOMAINS,
    get_ai_capability,
    get_human_edge_score,
)


def test_ai_capabilities_structure():
    """Test AI capabilities are properly structured."""
    assert len(AI_CAPABILITIES) > 0
    for key, capability in AI_CAPABILITIES.items():
        assert isinstance(key, str)
        assert isinstance(capability.name, str)
        assert 0 <= capability.strength <= 10
        assert isinstance(capability.description, str)
        assert isinstance(capability.examples, list)


def test_human_edge_domains_structure():
    """Test human edge domains are properly structured."""
    assert len(HUMAN_EDGE_DOMAINS) > 0
    for key, domain in HUMAN_EDGE_DOMAINS.items():
        assert isinstance(key, str)
        assert isinstance(domain.name, str)
        assert 0 <= domain.strength <= 10
        assert isinstance(domain.description, str)
        assert isinstance(domain.examples, list)


def test_get_ai_capability_exact_match():
    """Test AI capability for exact matches."""
    # Test exact match
    assert get_ai_capability("coding") >= 8

    # Test case insensitive
    assert get_ai_capability("CODING") >= 8


def test_get_ai_capability_partial_match():
    """Test AI capability for partial matches."""
    # Should match "coding" domain
    assert get_ai_capability("Python coding") >= 8

    # Should match "math" domain
    assert get_ai_capability("mathematical analysis") >= 9


def test_get_ai_capability_default():
    """Test AI capability returns reasonable default for unknown skills."""
    result = get_ai_capability("completely unknown skill xyz")
    assert 0 <= result <= 10


def test_get_human_edge_score_exact_match():
    """Test human edge score for exact matches."""
    # Test exact match
    assert get_human_edge_score("emotional intelligence") >= 9

    # Test case insensitive
    assert get_human_edge_score("EMOTIONAL INTELLIGENCE") >= 9


def test_get_human_edge_score_partial_match():
    """Test human edge score for partial matches."""
    # Should match emotional intelligence
    assert get_human_edge_score("emotional counseling") >= 9

    # Should match physical experience
    assert get_human_edge_score("physical craftsmanship") >= 9


def test_get_human_edge_score_default():
    """Test human edge score returns reasonable default for unknown skills."""
    result = get_human_edge_score("completely unknown skill xyz")
    assert 0 <= result <= 10


def test_coding_vs_counseling():
    """Test that coding favors AI while counseling favors humans."""
    coding_ai = get_ai_capability("coding")
    coding_human = get_human_edge_score("coding")
    assert coding_ai > coding_human

    counseling_ai = get_ai_capability("counseling")
    counseling_human = get_human_edge_score("counseling")
    assert counseling_human > counseling_ai
