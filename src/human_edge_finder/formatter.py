"""Output formatting for analysis results."""

import json
from typing import Dict, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from .analyzer import EdgeAnalysis, SkillAnalysis


def format_as_table(analysis: EdgeAnalysis) -> None:
    """
    Format analysis results as a rich table.

    Args:
        analysis: Complete edge analysis
    """
    console = Console()

    # Summary panel
    summary_text = Text()
    summary_text.append(f"Total Skills Analyzed: ", style="bold cyan")
    summary_text.append(f"{analysis.summary['total_skills']}\n")
    summary_text.append(f"Edge Zones (Your Advantage): ", style="bold green")
    summary_text.append(f"{analysis.summary['edge_zones_count']}\n")
    summary_text.append(f"Risk Zones (AI Competitive): ", style="bold red")
    summary_text.append(f"{analysis.summary['risk_zones_count']}\n")
    summary_text.append(f"Neutral Zones: ", style="bold yellow")
    summary_text.append(f"{analysis.summary['neutral_zones_count']}\n")
    summary_text.append(f"Average Edge Score: ", style="bold magenta")
    summary_text.append(f"{analysis.summary['average_edge_score']:.2f}")

    console.print(Panel(summary_text, title="Analysis Summary", border_style="blue"))
    console.print()

    # All skills table
    table = Table(title="Skill Analysis", show_header=True, header_style="bold")
    table.add_column("Skill", style="cyan", no_wrap=False)
    table.add_column("AI Cap", justify="center", style="magenta")
    table.add_column("Human Edge", justify="center", style="green")
    table.add_column("Edge Score", justify="center", style="yellow")
    table.add_column("Category", justify="center")

    for skill in analysis.skill_analyses:
        category_style = _get_category_style(skill.category)
        edge_sign = "+" if skill.edge_score >= 0 else ""
        table.add_row(
            skill.skill,
            str(skill.ai_capability),
            str(skill.human_edge),
            f"{edge_sign}{skill.edge_score}",
            Text(skill.category.replace("_", " ").title(), style=category_style)
        )

    console.print(table)
    console.print()

    # Edge zones
    if analysis.edge_zones:
        console.print(Panel(
            _format_skill_list(analysis.edge_zones, "Your Strongest Edges"),
            title="🎯 Focus on These (Your Competitive Advantage)",
            border_style="green"
        ))
        console.print()

    # Risk zones
    if analysis.risk_zones:
        console.print(Panel(
            _format_skill_list(analysis.risk_zones, "AI is Competitive Here"),
            title="⚠️  Risk Zones (Consider AI Augmentation)",
            border_style="red"
        ))


def format_as_json(analysis: EdgeAnalysis) -> str:
    """
    Format analysis results as JSON.

    Args:
        analysis: Complete edge analysis

    Returns:
        JSON string
    """
    from .analyzer import get_edge_report

    report = get_edge_report(analysis)
    return json.dumps(report, indent=2)


def format_as_markdown(analysis: EdgeAnalysis) -> str:
    """
    Format analysis results as Markdown.

    Args:
        analysis: Complete edge analysis

    Returns:
        Markdown string
    """
    md = []

    # Title
    md.append("# Human Edge Analysis Report\n")

    # Summary
    md.append("## Summary\n")
    md.append(f"- **Total Skills Analyzed**: {analysis.summary['total_skills']}")
    md.append(f"- **Edge Zones (Your Advantage)**: {analysis.summary['edge_zones_count']}")
    md.append(f"- **Risk Zones (AI Competitive)**: {analysis.summary['risk_zones_count']}")
    md.append(f"- **Neutral Zones**: {analysis.summary['neutral_zones_count']}")
    md.append(f"- **Average Edge Score**: {analysis.summary['average_edge_score']:.2f}")
    md.append("")

    # Edge zones
    if analysis.edge_zones:
        md.append("## 🎯 Your Edge Zones (Competitive Advantage)\n")
        md.append("| Skill | AI Capability | Human Edge | Edge Score | Category |")
        md.append("|-------|---------------|------------|------------|----------|")
        for skill in analysis.edge_zones:
            edge_sign = "+" if skill.edge_score >= 0 else ""
            md.append(
                f"| {skill.skill} | {skill.ai_capability}/10 | {skill.human_edge}/10 | "
                f"{edge_sign}{skill.edge_score} | {skill.category.replace('_', ' ').title()} |"
            )
        md.append("")

    # Risk zones
    if analysis.risk_zones:
        md.append("## ⚠️ Risk Zones (AI is Competitive)\n")
        md.append("| Skill | AI Capability | Human Edge | Edge Score | Category |")
        md.append("|-------|---------------|------------|------------|----------|")
        for skill in analysis.risk_zones:
            edge_sign = "+" if skill.edge_score >= 0 else ""
            md.append(
                f"| {skill.skill} | {skill.ai_capability}/10 | {skill.human_edge}/10 | "
                f"{edge_sign}{skill.edge_score} | {skill.category.replace('_', ' ').title()} |"
            )
        md.append("")

    # Neutral zones
    if analysis.neutral_zones:
        md.append("## ⚪ Neutral Zones\n")
        md.append("| Skill | AI Capability | Human Edge | Edge Score |")
        md.append("|-------|---------------|------------|------------|")
        for skill in analysis.neutral_zones:
            edge_sign = "+" if skill.edge_score >= 0 else ""
            md.append(
                f"| {skill.skill} | {skill.ai_capability}/10 | {skill.human_edge}/10 | "
                f"{edge_sign}{skill.edge_score} |"
            )
        md.append("")

    # Recommendations
    md.append("## 💡 Recommendations\n")
    if analysis.edge_zones:
        md.append("### Focus Areas (Leverage Your Strengths)")
        for skill in analysis.edge_zones[:3]:
            md.append(f"- **{skill.skill}** (Edge Score: +{skill.edge_score})")
        md.append("")

    if analysis.risk_zones:
        md.append("### Areas to Augment with AI")
        for skill in analysis.risk_zones[:3]:
            md.append(f"- **{skill.skill}** (Edge Score: {skill.edge_score})")
        md.append("")

    return "\n".join(md)


def format_comparison(comparison: Dict[str, any]) -> None:
    """
    Format a single skill comparison.

    Args:
        comparison: Comparison dictionary from compare_skill_to_ai
    """
    console = Console()

    # Create comparison panel
    text = Text()
    text.append(f"Skill: ", style="bold cyan")
    text.append(f"{comparison['skill']}\n\n", style="bold white")

    text.append(f"AI Capability: ", style="bold magenta")
    text.append(f"{comparison['ai_capability']}/10 ({comparison['ai_percentage']}%)\n")

    text.append(f"Human Edge: ", style="bold green")
    text.append(f"{comparison['human_edge']}/10 ({comparison['human_percentage']}%)\n")

    text.append(f"Edge Score: ", style="bold yellow")
    edge_sign = "+" if comparison['edge_score'] >= 0 else ""
    text.append(f"{edge_sign}{comparison['edge_score']}\n\n")

    text.append(f"Category: ", style="bold")
    text.append(f"{comparison['category'].replace('_', ' ').title()}\n\n")

    text.append(comparison['recommendation'])

    category_color = _get_category_color(comparison['category'])
    console.print(Panel(text, title="Skill Comparison", border_style=category_color))


def _format_skill_list(skills: List[SkillAnalysis], header: str) -> str:
    """Format a list of skills for panel display."""
    lines = []
    for i, skill in enumerate(skills[:5], 1):  # Show top 5
        edge_sign = "+" if skill.edge_score >= 0 else ""
        lines.append(f"{i}. {skill.skill} (Edge: {edge_sign}{skill.edge_score})")
    return "\n".join(lines) if lines else "None"


def _get_category_style(category: str) -> str:
    """Get rich style for category."""
    styles = {
        "strong_edge": "bold green",
        "moderate_edge": "green",
        "neutral": "yellow",
        "risk_zone": "red",
        "ai_dominated": "bold red"
    }
    return styles.get(category, "white")


def _get_category_color(category: str) -> str:
    """Get border color for category."""
    colors = {
        "strong_edge": "green",
        "moderate_edge": "green",
        "neutral": "yellow",
        "risk_zone": "red",
        "ai_dominated": "red"
    }
    return colors.get(category, "white")
