# human-edge-finder

> Find where you have a competitive edge over AI models

A Python CLI tool that analyzes your skills and expertise to identify where you have a genuine competitive advantage over AI models, and where AI might be catching up or surpassing human capabilities.

## Motivation

Inspired by discussions about AI automation and human expertise, this tool helps you:

- **Identify your edge zones**: Skills where your human expertise gives you a competitive advantage
- **Spot risk zones**: Areas where AI is becoming increasingly competitive
- **Make strategic decisions**: Focus on developing skills where humans excel
- **Leverage AI effectively**: Understand where to augment your work with AI tools

As AI capabilities expand, understanding where humans maintain unique advantages becomes crucial for career planning, skill development, and strategic positioning.

## Installation

### From PyPI (once published)

```bash
pip install human-edge-finder
```

### From Source

```bash
git clone https://github.com/serenakeyitan/human-edge-finder.git
cd human-edge-finder
pip install -e .
```

### For Development

```bash
git clone https://github.com/serenakeyitan/human-edge-finder.git
cd human-edge-finder
pip install -e ".[dev]"
```

## Usage

### Analyze Skills

Analyze a list of skills to identify your edge zones:

```bash
# Comma-separated skills
human-edge-finder analyze "coding, counseling, teaching, data analysis"

# From a file
human-edge-finder analyze --file my-skills.txt

# JSON output
human-edge-finder analyze "writing, math, emotional intelligence" --format json

# Markdown output
human-edge-finder analyze "design, coding, improvisation" --format markdown
```

### Compare Single Skill

Compare a specific skill against AI capabilities:

```bash
human-edge-finder compare "emotional intelligence"
human-edge-finder compare "python programming"
human-edge-finder compare "creative writing" --format json
```

### Generate Report

Create a comprehensive edge report:

```bash
# Output to terminal
human-edge-finder report "coding, teaching, counseling, design"

# Save to file
human-edge-finder report --file skills.txt -o edge-report.md

# JSON format
human-edge-finder report "data science, therapy, cooking" --format json -o report.json
```

## Sample Output

### Table Format (analyze command)

```
╭──────────────────────── Analysis Summary ────────────────────────╮
│ Total Skills Analyzed: 5                                          │
│ Edge Zones (Your Advantage): 2                                    │
│ Risk Zones (AI Competitive): 2                                    │
│ Neutral Zones: 1                                                  │
│ Average Edge Score: +0.40                                         │
╰───────────────────────────────────────────────────────────────────╯

                          Skill Analysis
┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Skill                 ┃ AI Cap ┃ Human Edge ┃ Edge Score┃ Category     ┃
┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ counseling            │   3    │     10     │    +7     │ Strong Edge  │
│ teaching              │   6    │      9     │    +3     │ Strong Edge  │
│ design                │   6    │      9     │    +3     │ Strong Edge  │
│ writing               │   7    │      8     │    +1     │ Moderate Edge│
│ data analysis         │   8    │      6     │    -2     │ Risk Zone    │
│ coding                │   9    │      6     │    -3     │ Risk Zone    │
└───────────────────────┴────────┴────────────┴───────────┴──────────────┘

╭─────────── 🎯 Focus on These (Your Competitive Advantage) ───────────╮
│ 1. counseling (Edge: +7)                                             │
│ 2. teaching (Edge: +3)                                               │
│ 3. design (Edge: +3)                                                 │
╰──────────────────────────────────────────────────────────────────────╯

╭──────────── ⚠️  Risk Zones (Consider AI Augmentation) ──────────────╮
│ 1. coding (Edge: -3)                                                 │
│ 2. data analysis (Edge: -2)                                          │
╰──────────────────────────────────────────────────────────────────────╯
```

### Comparison Output (compare command)

```
╭──────────────────── Skill Comparison ────────────────────────╮
│ Skill: emotional intelligence                                │
│                                                               │
│ AI Capability: 3/10 (30%)                                     │
│ Human Edge: 10/10 (100%)                                      │
│ Edge Score: +7                                                │
│                                                               │
│ Category: Strong Edge                                         │
│                                                               │
│ 🟢 Strong competitive advantage! Focus on 'emotional         │
│ intelligence' - this is where you excel over AI.             │
╰───────────────────────────────────────────────────────────────╯
```

## How It Works

The tool evaluates skills across three dimensions:

1. **AI Capability Domains**: Areas where AI models excel (coding, math, translation, pattern recognition, etc.)

2. **Human Edge Domains**: Areas where humans maintain unique advantages:
   - Physical world experience
   - Emotional intelligence
   - Deep cultural context
   - Tacit knowledge
   - Ethical judgment
   - Creative intuition
   - Real-time adaptation
   - Relationship building
   - Sensory experience
   - Personal authenticity

3. **Hybrid Domains**: Areas where both AI and humans have significant but different strengths

Each skill is scored on a 0-10 scale for both AI capability and human edge. The **Edge Score** is calculated as:

```
Edge Score = Human Edge - AI Capability
```

Skills are then categorized:
- **Strong Edge** (+3 or higher): Your competitive advantage
- **Moderate Edge** (+1 to +2): Good area to develop
- **Neutral** (-1 to +1): Level playing field
- **Risk Zone** (-3 to -2): AI is competitive
- **AI Dominated** (-3 or lower): Consider AI augmentation

## Skills File Format

You can provide skills in a file using either format:

**Comma-separated:**
```
coding, teaching, counseling, data analysis, creative writing
```

**Newline-separated:**
```
coding
teaching
counseling
data analysis
creative writing
```

## Development

### Run Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=human_edge_finder --cov-report=html
```

### Lint Code

```bash
ruff check .
```

### Format Code

```bash
ruff format .
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by discussions about AI capabilities and human expertise
- Built with [Click](https://click.palletsprojects.com/) and [Rich](https://rich.readthedocs.io/)

## Roadmap

- [ ] Add more domain definitions
- [ ] Machine learning model for skill categorization
- [ ] Integration with LinkedIn for automatic skill import
- [ ] Trend analysis over time
- [ ] Personalized recommendations based on career goals
- [ ] Web interface

## Author

**Serena Tan** - [@serenakeyitan](https://github.com/serenakeyitan)

---

*Remember: This tool provides general guidance. Your unique combination of skills, experiences, and context is what truly sets you apart from AI.*
