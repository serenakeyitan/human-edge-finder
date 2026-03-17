"""Core analysis engine for identifying human edges over AI."""

from typing import Dict, List, NamedTuple

from .domains import get_ai_capability, get_human_edge_score


class SkillAnalysis(NamedTuple):
    """Analysis result for a single skill."""
    skill: str
    ai_capability: int
    human_edge: int
    edge_score: int  # Positive means human advantage, negative means AI advantage
    category: str  # "strong_edge", "moderate_edge", "neutral", "risk_zone", "ai_dominated"


class EdgeAnalysis(NamedTuple):
    """Complete analysis of all skills."""
    skill_analyses: List[SkillAnalysis]
    edge_zones: List[SkillAnalysis]
    risk_zones: List[SkillAnalysis]
    neutral_zones: List[SkillAnalysis]
    summary: Dict[str, any]


def analyze_skill(skill: str) -> SkillAnalysis:
    """
    Analyze a single skill to determine human edge vs AI capability.

    Args:
        skill: The skill to analyze

    Returns:
        SkillAnalysis with ratings and categorization
    """
    ai_cap = get_ai_capability(skill)
    human_edge = get_human_edge_score(skill)
    edge_score = human_edge - ai_cap

    # Categorize based on edge score
    if edge_score >= 3:
        category = "strong_edge"
    elif edge_score >= 1:
        category = "moderate_edge"
    elif edge_score >= -1:
        category = "neutral"
    elif edge_score >= -3:
        category = "risk_zone"
    else:
        category = "ai_dominated"

    return SkillAnalysis(
        skill=skill,
        ai_capability=ai_cap,
        human_edge=human_edge,
        edge_score=edge_score,
        category=category
    )


def analyze_skills(skills: List[str]) -> EdgeAnalysis:
    """
    Analyze a list of skills to identify human edges.

    Args:
        skills: List of skills to analyze

    Returns:
        EdgeAnalysis with complete breakdown
    """
    skill_analyses = [analyze_skill(skill.strip()) for skill in skills if skill.strip()]

    # Categorize skills
    edge_zones = [s for s in skill_analyses if s.category in ["strong_edge", "moderate_edge"]]
    risk_zones = [s for s in skill_analyses if s.category in ["risk_zone", "ai_dominated"]]
    neutral_zones = [s for s in skill_analyses if s.category == "neutral"]

    # Sort by edge score
    edge_zones.sort(key=lambda x: x.edge_score, reverse=True)
    risk_zones.sort(key=lambda x: x.edge_score)

    # Generate summary statistics
    summary = {
        "total_skills": len(skill_analyses),
        "edge_zones_count": len(edge_zones),
        "risk_zones_count": len(risk_zones),
        "neutral_zones_count": len(neutral_zones),
        "average_edge_score": (
            sum(s.edge_score for s in skill_analyses) / len(skill_analyses)
            if skill_analyses
            else 0
        ),
        "strongest_edge": edge_zones[0].skill if edge_zones else None,
        "highest_risk": risk_zones[0].skill if risk_zones else None,
    }

    return EdgeAnalysis(
        skill_analyses=skill_analyses,
        edge_zones=edge_zones,
        risk_zones=risk_zones,
        neutral_zones=neutral_zones,
        summary=summary
    )


def compare_skill_to_ai(skill: str) -> Dict[str, any]:
    """
    Compare a specific skill against AI capabilities with detailed breakdown.

    Args:
        skill: The skill to compare

    Returns:
        Detailed comparison dictionary
    """
    analysis = analyze_skill(skill)

    return {
        "skill": skill,
        "ai_capability": analysis.ai_capability,
        "human_edge": analysis.human_edge,
        "edge_score": analysis.edge_score,
        "category": analysis.category,
        "recommendation": _get_recommendation(analysis),
        "ai_percentage": int((analysis.ai_capability / 10) * 100),
        "human_percentage": int((analysis.human_edge / 10) * 100),
    }


def _get_recommendation(analysis: SkillAnalysis) -> str:
    """Generate recommendation based on analysis."""
    if analysis.category == "strong_edge":
        return (
            f"🟢 Strong competitive advantage! Focus on '{analysis.skill}' - "
            "this is where you excel over AI."
        )
    elif analysis.category == "moderate_edge":
        return (
            f"🟡 Moderate advantage. '{analysis.skill}' is a good area to develop further."
        )
    elif analysis.category == "neutral":
        return (
            f"⚪ Level playing field. Consider combining '{analysis.skill}' "
            "with your unique context."
        )
    elif analysis.category == "risk_zone":
        return (
            f"🟠 Risk zone. AI is competitive in '{analysis.skill}'. "
            "Focus on adding human context."
        )
    else:  # ai_dominated
        return (
            f"🔴 AI-dominated. Consider leveraging AI for '{analysis.skill}' "
            "and focus on your edge zones."
        )


def get_edge_report(analysis: EdgeAnalysis) -> Dict[str, any]:
    """
    Generate a comprehensive edge report.

    Args:
        analysis: Complete edge analysis

    Returns:
        Structured report dictionary
    """
    return {
        "summary": analysis.summary,
        "edge_zones": [
            {
                "skill": s.skill,
                "edge_score": s.edge_score,
                "category": s.category,
                "ai_capability": s.ai_capability,
                "human_edge": s.human_edge,
            }
            for s in analysis.edge_zones
        ],
        "risk_zones": [
            {
                "skill": s.skill,
                "edge_score": s.edge_score,
                "category": s.category,
                "ai_capability": s.ai_capability,
                "human_edge": s.human_edge,
            }
            for s in analysis.risk_zones
        ],
        "neutral_zones": [
            {
                "skill": s.skill,
                "edge_score": s.edge_score,
                "category": s.category,
                "ai_capability": s.ai_capability,
                "human_edge": s.human_edge,
            }
            for s in analysis.neutral_zones
        ],
        "recommendations": {
            "focus_areas": [s.skill for s in analysis.edge_zones[:3]],
            "areas_to_augment_with_ai": [s.skill for s in analysis.risk_zones[:3]],
            "overall_assessment": _get_overall_assessment(analysis),
        }
    }


def _get_overall_assessment(analysis: EdgeAnalysis) -> str:
    """Generate overall assessment based on analysis."""
    avg_score = analysis.summary["average_edge_score"]
    edge_pct = (
        (analysis.summary["edge_zones_count"] / analysis.summary["total_skills"] * 100)
        if analysis.summary["total_skills"] > 0
        else 0
    )

    if avg_score >= 2 or edge_pct >= 60:
        return (
            "You have a strong overall edge over AI! "
            "Focus on leveraging your unique human strengths."
        )
    elif avg_score >= 0 or edge_pct >= 40:
        return (
            "You have a balanced skill set. "
            "Focus on your edge zones and use AI to augment risk zones."
        )
    else:
        return (
            "Many of your skills overlap with AI capabilities. "
            "Consider developing more human-centric skills or adding unique context "
            "to your existing skills."
        )
