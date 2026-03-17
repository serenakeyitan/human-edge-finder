"""Command-line interface for Human Edge Finder."""

import click
import sys
from pathlib import Path
from typing import List

from .analyzer import analyze_skills, compare_skill_to_ai, get_edge_report
from .formatter import format_as_table, format_as_json, format_as_markdown, format_comparison
from . import __version__


@click.group()
@click.version_option(version=__version__)
def cli():
    """
    Human Edge Finder - Analyze your competitive edge over AI models.

    Identify where your human expertise gives you an advantage over AI,
    and where AI might be catching up to your skills.
    """
    pass


@cli.command()
@click.argument('skills', required=False)
@click.option(
    '--file', '-f',
    type=click.Path(exists=True),
    help='Path to file containing skills (one per line or comma-separated)'
)
@click.option(
    '--format',
    type=click.Choice(['table', 'json', 'markdown'], case_sensitive=False),
    default='table',
    help='Output format (default: table)'
)
def analyze(skills: str, file: str, format: str):
    """
    Analyze skills and identify your edge over AI.

    \b
    Examples:
        human-edge-finder analyze "coding, writing, counseling"
        human-edge-finder analyze --file skills.txt
        human-edge-finder analyze "data analysis, teaching" --format json
    """
    skill_list = _get_skills_list(skills, file)

    if not skill_list:
        click.echo("Error: No skills provided. Use --help for usage information.", err=True)
        sys.exit(1)

    # Perform analysis
    analysis = analyze_skills(skill_list)

    # Format output
    if format == 'table':
        format_as_table(analysis)
    elif format == 'json':
        click.echo(format_as_json(analysis))
    elif format == 'markdown':
        click.echo(format_as_markdown(analysis))


@cli.command()
@click.argument('skill')
@click.option(
    '--format',
    type=click.Choice(['table', 'json'], case_sensitive=False),
    default='table',
    help='Output format (default: table)'
)
def compare(skill: str, format: str):
    """
    Compare a specific skill against AI capabilities.

    \b
    Examples:
        human-edge-finder compare "emotional intelligence"
        human-edge-finder compare "python programming" --format json
    """
    comparison = compare_skill_to_ai(skill)

    if format == 'table':
        format_comparison(comparison)
    elif format == 'json':
        import json
        click.echo(json.dumps(comparison, indent=2))


@cli.command()
@click.argument('skills', required=False)
@click.option(
    '--file', '-f',
    type=click.Path(exists=True),
    help='Path to file containing skills (one per line or comma-separated)'
)
@click.option(
    '--format',
    type=click.Choice(['json', 'markdown'], case_sensitive=False),
    default='markdown',
    help='Output format (default: markdown)'
)
@click.option(
    '--output', '-o',
    type=click.Path(),
    help='Output file path (optional)'
)
def report(skills: str, file: str, format: str, output: str):
    """
    Generate a comprehensive edge report.

    \b
    Examples:
        human-edge-finder report "coding, teaching, counseling"
        human-edge-finder report --file skills.txt --format json
        human-edge-finder report --file skills.txt -o report.md
    """
    skill_list = _get_skills_list(skills, file)

    if not skill_list:
        click.echo("Error: No skills provided. Use --help for usage information.", err=True)
        sys.exit(1)

    # Perform analysis
    analysis = analyze_skills(skill_list)

    # Generate report
    if format == 'json':
        report_content = format_as_json(analysis)
    else:  # markdown
        report_content = format_as_markdown(analysis)

    # Output
    if output:
        output_path = Path(output)
        output_path.write_text(report_content)
        click.echo(f"Report saved to: {output_path.absolute()}")
    else:
        click.echo(report_content)


def _get_skills_list(skills: str, file: str) -> List[str]:
    """
    Get list of skills from argument or file.

    Args:
        skills: Comma-separated skills string
        file: Path to file containing skills

    Returns:
        List of skill strings
    """
    skill_list = []

    if file:
        # Read from file
        file_path = Path(file)
        content = file_path.read_text()

        # Try to parse as comma-separated first
        if ',' in content:
            skill_list = [s.strip() for s in content.split(',')]
        else:
            # Parse as newline-separated
            skill_list = [s.strip() for s in content.split('\n')]

    elif skills:
        # Parse from argument
        skill_list = [s.strip() for s in skills.split(',')]

    # Filter out empty strings
    return [s for s in skill_list if s]


if __name__ == '__main__':
    cli()
