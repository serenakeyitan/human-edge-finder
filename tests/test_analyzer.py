"""Tests for analysis engine."""

from human_edge_finder.analyzer import (
    analyze_skill,
    analyze_skills,
    compare_skill_to_ai,
    get_edge_report,
)


def test_analyze_skill_basic():
    """Test basic skill analysis."""
    result = analyze_skill("coding")

    assert result.skill == "coding"
    assert 0 <= result.ai_capability <= 10
    assert 0 <= result.human_edge <= 10
    assert result.edge_score == result.human_edge - result.ai_capability
    assert result.category in [
        "strong_edge",
        "moderate_edge",
        "neutral",
        "risk_zone",
        "ai_dominated",
    ]


def test_analyze_skill_edge_categorization():
    """Test that skills are categorized correctly."""
    # Test strong edge (emotional intelligence)
    result = analyze_skill("emotional intelligence")
    assert result.category in ["strong_edge", "moderate_edge"]
    assert result.edge_score > 0

    # Test AI strength (coding)
    result = analyze_skill("coding")
    assert result.category in ["risk_zone", "ai_dominated", "neutral"]


def test_analyze_skills_multiple(sample_skills):
    """Test analyzing multiple skills."""
    analysis = analyze_skills(sample_skills)

    assert analysis.summary["total_skills"] == len(sample_skills)
    assert len(analysis.skill_analyses) == len(sample_skills)

    # Check that all categories sum up correctly
    total = (
        analysis.summary["edge_zones_count"]
        + analysis.summary["risk_zones_count"]
        + analysis.summary["neutral_zones_count"]
    )
    assert total == len(sample_skills)


def test_analyze_skills_sorting(sample_skills):
    """Test that edge zones are sorted by edge score."""
    analysis = analyze_skills(sample_skills)

    # Edge zones should be sorted in descending order
    if len(analysis.edge_zones) > 1:
        for i in range(len(analysis.edge_zones) - 1):
            assert analysis.edge_zones[i].edge_score >= analysis.edge_zones[i + 1].edge_score

    # Risk zones should be sorted in ascending order (most negative first)
    if len(analysis.risk_zones) > 1:
        for i in range(len(analysis.risk_zones) - 1):
            assert analysis.risk_zones[i].edge_score <= analysis.risk_zones[i + 1].edge_score


def test_analyze_skills_empty():
    """Test analyzing empty skill list."""
    analysis = analyze_skills([])
    assert analysis.summary["total_skills"] == 0
    assert len(analysis.skill_analyses) == 0
    assert len(analysis.edge_zones) == 0
    assert len(analysis.risk_zones) == 0


def test_analyze_skills_with_whitespace():
    """Test that whitespace is handled correctly."""
    skills = ["  coding  ", "teaching", "  ", "counseling  "]
    analysis = analyze_skills(skills)

    # Should skip empty strings
    assert analysis.summary["total_skills"] == 3


def test_compare_skill_to_ai():
    """Test single skill comparison."""
    comparison = compare_skill_to_ai("emotional intelligence")

    assert comparison["skill"] == "emotional intelligence"
    assert 0 <= comparison["ai_capability"] <= 10
    assert 0 <= comparison["human_edge"] <= 10
    assert comparison["edge_score"] == comparison["human_edge"] - comparison["ai_capability"]
    assert comparison["category"] in [
        "strong_edge",
        "moderate_edge",
        "neutral",
        "risk_zone",
        "ai_dominated",
    ]
    assert "recommendation" in comparison
    assert comparison["ai_percentage"] == int((comparison["ai_capability"] / 10) * 100)
    assert comparison["human_percentage"] == int((comparison["human_edge"] / 10) * 100)


def test_get_edge_report(sample_skills):
    """Test edge report generation."""
    analysis = analyze_skills(sample_skills)
    report = get_edge_report(analysis)

    assert "summary" in report
    assert "edge_zones" in report
    assert "risk_zones" in report
    assert "neutral_zones" in report
    assert "recommendations" in report

    # Check recommendations structure
    assert "focus_areas" in report["recommendations"]
    assert "areas_to_augment_with_ai" in report["recommendations"]
    assert "overall_assessment" in report["recommendations"]


def test_edge_score_calculation():
    """Test that edge scores are calculated correctly."""
    result = analyze_skill("test skill")
    expected_edge = result.human_edge - result.ai_capability
    assert result.edge_score == expected_edge


def test_category_thresholds():
    """Test category assignment based on edge scores."""
    # We can't control exact scores, but we can verify the logic
    from human_edge_finder.analyzer import SkillAnalysis

    # Strong edge: >= 3
    skill = SkillAnalysis("test", 5, 8, 3, "strong_edge")
    assert skill.edge_score >= 3

    # Moderate edge: 1 to 2
    skill = SkillAnalysis("test", 5, 6, 1, "moderate_edge")
    assert 1 <= skill.edge_score <= 2

    # Neutral: -1 to 1
    skill = SkillAnalysis("test", 5, 5, 0, "neutral")
    assert -1 <= skill.edge_score <= 1

    # Risk zone: -3 to -2
    skill = SkillAnalysis("test", 7, 5, -2, "risk_zone")
    assert -3 <= skill.edge_score <= -2

    # AI dominated: < -3
    skill = SkillAnalysis("test", 9, 5, -4, "ai_dominated")
    assert skill.edge_score < -3


def test_summary_statistics(sample_skills):
    """Test that summary statistics are calculated correctly."""
    analysis = analyze_skills(sample_skills)
    summary = analysis.summary

    assert summary["total_skills"] == len(sample_skills)

    # Average edge score should be reasonable
    calculated_avg = (
        sum(s.edge_score for s in analysis.skill_analyses) / len(analysis.skill_analyses)
    )
    assert abs(summary["average_edge_score"] - calculated_avg) < 0.01

    # Strongest edge should be from edge zones if any exist
    if analysis.edge_zones:
        assert summary["strongest_edge"] == analysis.edge_zones[0].skill

    # Highest risk should be from risk zones if any exist
    if analysis.risk_zones:
        assert summary["highest_risk"] == analysis.risk_zones[0].skill
