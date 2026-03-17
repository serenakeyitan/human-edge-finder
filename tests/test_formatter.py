"""Tests for output formatting."""

import json
from human_edge_finder.analyzer import analyze_skills
from human_edge_finder.formatter import format_as_json, format_as_markdown


def test_format_as_json(sample_skills):
    """Test JSON formatting."""
    analysis = analyze_skills(sample_skills)
    json_output = format_as_json(analysis)

    # Should be valid JSON
    data = json.loads(json_output)

    # Check structure
    assert "summary" in data
    assert "edge_zones" in data
    assert "risk_zones" in data
    assert "neutral_zones" in data
    assert "recommendations" in data


def test_format_as_json_structure(sample_skills):
    """Test JSON output structure in detail."""
    analysis = analyze_skills(sample_skills)
    json_output = format_as_json(analysis)
    data = json.loads(json_output)

    # Check summary
    assert "total_skills" in data["summary"]
    assert "edge_zones_count" in data["summary"]
    assert "risk_zones_count" in data["summary"]
    assert "average_edge_score" in data["summary"]

    # Check edge zones format
    for zone in data["edge_zones"]:
        assert "skill" in zone
        assert "edge_score" in zone
        assert "category" in zone
        assert "ai_capability" in zone
        assert "human_edge" in zone

    # Check recommendations
    assert "focus_areas" in data["recommendations"]
    assert "areas_to_augment_with_ai" in data["recommendations"]
    assert "overall_assessment" in data["recommendations"]


def test_format_as_markdown(sample_skills):
    """Test Markdown formatting."""
    analysis = analyze_skills(sample_skills)
    md_output = format_as_markdown(analysis)

    # Should contain expected sections
    assert "# Human Edge Analysis Report" in md_output
    assert "## Summary" in md_output
    assert "## 💡 Recommendations" in md_output

    # Should contain markdown table syntax
    assert "|" in md_output
    assert "---" in md_output


def test_format_as_markdown_structure(sample_skills):
    """Test Markdown output structure in detail."""
    analysis = analyze_skills(sample_skills)
    md_output = format_as_markdown(analysis)

    # Check for key sections
    assert "Total Skills Analyzed" in md_output
    assert "Edge Zones (Your Advantage)" in md_output
    assert "Risk Zones (AI Competitive)" in md_output

    # Should have tables if there are edge zones
    if analysis.edge_zones:
        assert "🎯 Your Edge Zones" in md_output
        assert "| Skill |" in md_output


def test_format_as_markdown_edge_zones(edge_skills):
    """Test Markdown formatting with edge zone skills."""
    analysis = analyze_skills(edge_skills)
    md_output = format_as_markdown(analysis)

    # Should have edge zones section
    assert "🎯 Your Edge Zones" in md_output

    # Should list the skills
    for skill in edge_skills:
        assert skill in md_output


def test_format_as_markdown_risk_zones(ai_skills):
    """Test Markdown formatting with risk zone skills."""
    analysis = analyze_skills(ai_skills)
    md_output = format_as_markdown(analysis)

    # Should have risk zones section if any exist
    if analysis.risk_zones:
        assert "⚠️ Risk Zones" in md_output


def test_format_empty_analysis():
    """Test formatting with empty analysis."""
    analysis = analyze_skills([])

    # JSON should still be valid
    json_output = format_as_json(analysis)
    data = json.loads(json_output)
    assert data["summary"]["total_skills"] == 0

    # Markdown should still have headers
    md_output = format_as_markdown(analysis)
    assert "# Human Edge Analysis Report" in md_output
    assert "## Summary" in md_output


def test_json_serialization_types(sample_skills):
    """Test that JSON output uses proper types."""
    analysis = analyze_skills(sample_skills)
    json_output = format_as_json(analysis)
    data = json.loads(json_output)

    # Numbers should be numbers, not strings
    assert isinstance(data["summary"]["total_skills"], int)
    assert isinstance(data["summary"]["average_edge_score"], (int, float))

    # Lists should be lists
    assert isinstance(data["edge_zones"], list)
    assert isinstance(data["recommendations"]["focus_areas"], list)


def test_markdown_edge_score_formatting(sample_skills):
    """Test that edge scores are formatted with proper signs in markdown."""
    analysis = analyze_skills(sample_skills)
    md_output = format_as_markdown(analysis)

    # Positive scores should have + sign
    for skill in analysis.edge_zones:
        if skill.edge_score > 0:
            assert f"+{skill.edge_score}" in md_output


def test_markdown_table_structure(sample_skills):
    """Test that markdown tables are properly structured."""
    analysis = analyze_skills(sample_skills)
    md_output = format_as_markdown(analysis)

    # Count table separators
    if analysis.edge_zones:
        lines = md_output.split("\n")
        # Should have at least one table header separator
        separator_lines = [line for line in lines if "---|" in line or "|---|" in line]
        assert len(separator_lines) >= 1
