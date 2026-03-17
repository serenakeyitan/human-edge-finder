"""Tests for CLI commands."""

import json
from pathlib import Path

from click.testing import CliRunner

from human_edge_finder.cli import cli


def test_cli_version():
    """Test version option."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output.lower() or "0.1.0" in result.output


def test_cli_help():
    """Test help option."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Human Edge Finder" in result.output
    assert "analyze" in result.output
    assert "compare" in result.output
    assert "report" in result.output


def test_analyze_command_basic():
    """Test analyze command with basic input."""
    runner = CliRunner()
    result = runner.invoke(cli, ["analyze", "coding, teaching"])
    assert result.exit_code == 0


def test_analyze_command_empty():
    """Test analyze command without input."""
    runner = CliRunner()
    result = runner.invoke(cli, ["analyze"])
    assert result.exit_code != 0
    assert "Error" in result.output


def test_analyze_command_json_format():
    """Test analyze command with JSON output."""
    runner = CliRunner()
    result = runner.invoke(cli, ["analyze", "coding, teaching", "--format", "json"])
    assert result.exit_code == 0

    # Should be valid JSON
    data = json.loads(result.output)
    assert "summary" in data


def test_analyze_command_markdown_format():
    """Test analyze command with Markdown output."""
    runner = CliRunner()
    result = runner.invoke(cli, ["analyze", "coding, teaching", "--format", "markdown"])
    assert result.exit_code == 0
    assert "# Human Edge Analysis Report" in result.output


def test_analyze_command_from_file():
    """Test analyze command reading from file."""
    runner = CliRunner()

    with runner.isolated_filesystem():
        # Create a test file
        skills_file = Path("skills.txt")
        skills_file.write_text("coding\nteaching\ncounseling")

        result = runner.invoke(cli, ["analyze", "--file", "skills.txt"])
        assert result.exit_code == 0


def test_analyze_command_from_file_csv():
    """Test analyze command reading CSV from file."""
    runner = CliRunner()

    with runner.isolated_filesystem():
        # Create a test file with CSV
        skills_file = Path("skills.txt")
        skills_file.write_text("coding, teaching, counseling")

        result = runner.invoke(cli, ["analyze", "--file", "skills.txt"])
        assert result.exit_code == 0


def test_compare_command_basic():
    """Test compare command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["compare", "emotional intelligence"])
    assert result.exit_code == 0
    assert "emotional intelligence" in result.output.lower()


def test_compare_command_json_format():
    """Test compare command with JSON output."""
    runner = CliRunner()
    result = runner.invoke(cli, ["compare", "coding", "--format", "json"])
    assert result.exit_code == 0

    # Should be valid JSON
    data = json.loads(result.output)
    assert "skill" in data
    assert data["skill"] == "coding"


def test_report_command_basic():
    """Test report command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["report", "coding, teaching, counseling"])
    assert result.exit_code == 0
    assert "# Human Edge Analysis Report" in result.output


def test_report_command_json_format():
    """Test report command with JSON format."""
    runner = CliRunner()
    result = runner.invoke(cli, ["report", "coding, teaching", "--format", "json"])
    assert result.exit_code == 0

    # Should be valid JSON
    data = json.loads(result.output)
    assert "summary" in data


def test_report_command_output_file():
    """Test report command with output file."""
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(
            cli, ["report", "coding, teaching", "--output", "report.md"]
        )
        assert result.exit_code == 0
        assert Path("report.md").exists()

        # Check file content
        content = Path("report.md").read_text()
        assert "# Human Edge Analysis Report" in content


def test_report_command_from_file():
    """Test report command reading from file."""
    runner = CliRunner()

    with runner.isolated_filesystem():
        # Create a test file
        skills_file = Path("skills.txt")
        skills_file.write_text("coding\nteaching\ncounseling")

        result = runner.invoke(cli, ["report", "--file", "skills.txt"])
        assert result.exit_code == 0


def test_report_command_empty():
    """Test report command without input."""
    runner = CliRunner()
    result = runner.invoke(cli, ["report"])
    assert result.exit_code != 0
    assert "Error" in result.output


def test_analyze_help():
    """Test analyze command help."""
    runner = CliRunner()
    result = runner.invoke(cli, ["analyze", "--help"])
    assert result.exit_code == 0
    assert "Analyze skills" in result.output
    assert "--file" in result.output
    assert "--format" in result.output


def test_compare_help():
    """Test compare command help."""
    runner = CliRunner()
    result = runner.invoke(cli, ["compare", "--help"])
    assert result.exit_code == 0
    assert "Compare a specific skill" in result.output


def test_report_help():
    """Test report command help."""
    runner = CliRunner()
    result = runner.invoke(cli, ["report", "--help"])
    assert result.exit_code == 0
    assert "Generate a comprehensive" in result.output
    assert "--output" in result.output


def test_whitespace_handling():
    """Test that CLI handles whitespace correctly."""
    runner = CliRunner()
    result = runner.invoke(cli, ["analyze", "  coding  , teaching  "])
    assert result.exit_code == 0
