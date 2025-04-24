# Manuscript Reviewer

A multi-agent system for comprehensive manuscript review and analysis.

## Overview

This project implements a sophisticated multi-agent system for reviewing and analyzing academic manuscripts. The system uses a combination of section-specific, rigor, and writing quality agents to provide detailed feedback and suggestions for improvement.

## Agent Structure

The system consists of three main categories of agents:

### Section Agents (S1-S10)
- S1: Title and Keywords Analysis
- S2: Abstract Review
- S3: Introduction Assessment
- S4: Literature Review Analysis
- S5: Methodology Evaluation
- S6: Results Analysis
- S7: Discussion Review
- S8: Conclusion Assessment
- S9: References Analysis
- S10: Supplementary Materials Review

### Rigor Agents (R1-R7)
- R1: Originality and Contribution
- R2: Impact and Significance
- R3: Ethics and Compliance
- R4: Data and Code Availability
- R5: Statistical Rigor
- R6: Technical Accuracy
- R7: Consistency

### Writing Agents (W1-W8)
- W1: Clarity
- W2: Organization
- W3: Grammar
- W4: Style
- W5: Technical Accuracy
- W6: Consistency
- W7: Readability
- W8: Overall Writing Quality

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your manuscript PDF in the `manuscripts/` directory
2. Run the analysis:
```bash
python run_analysis.py
```

For information on using more powerful models (like GPT-4), see [MODEL_GUIDE.md](MODEL_GUIDE.md).

## Output

The system generates a comprehensive report in `results/manuscript_report.md` containing:
- Overall assessment
- Section-by-section analysis
- Critical remarks
- Improvement suggestions
- Detailed feedback
- Summary of findings

For information on using more powerful models (like GPT-4), see [MODEL_GUIDE.md](MODEL_GUIDE.md).

## Report Generator

The report generator component takes the combined output from all agents and creates a well-structured markdown report.

### Report Structure

1. **Header**
   - Title and generation timestamp
   - Important notes about the tool's status
   - Overall assessment summary

2. **Section Analysis (S1-S10)**
   - Title and Keywords through Supplementary Materials

3. **Rigor Analysis (R1-R7)**
   - Originality, Impact, Ethics, Data Availability, etc.

4. **Writing Quality (W1-W8)**
   - Language, Structure, Clarity, Terminology, etc.

### Agent Response Format

Each agent's analysis follows a consistent JSON structure:

```json
{
    "score": int,  // Score from 1-10
    "critical_remarks": [
        {
            "category": str,
            "location": str,
            "issue": str,
            "severity": str,
            "impact": str
        }
    ],
    "improvement_suggestions": [
        {
            "location": str,
            "category": str,
            "focus": str,
            "original_text": str,
            "improved_version": str,
            "explanation": str
        }
    ],
    "detailed_feedback": {
        // Agent-specific detailed analysis
    },
    "summary": str  // Overall assessment summary
}
```

### Customization

The report template and formatting can be modified in:
- `src/core/report_template.py`: Main report structure
- `src/utils/json_to_report.py`: JSON to markdown conversion

## Configuration

- Environment variables are managed in `.env`
- Agent configurations can be modified in `src/config/`
- Logging settings in `src/config/logging_config.py`

## Development

### Project Structure
```
V5_multi_agent2/
├── src/
│   ├── reviewer_agents/
│   │   ├── section/      # Section agents (S1-S10)
│   │   ├── rigor/        # Rigor agents (R1-R7)
│   │   ├── writing/      # Writing agents (W1-W8)
│   │   └── controller_agent.py
│   ├── core/
│   ├── utils/
│   └── config/
├── manuscripts/          # Input manuscripts
├── results/             # Generated reports
└── tests/              # Test suite
```

### Adding New Agents

1. Create a new agent class inheriting from `BaseReviewerAgent`
2. Implement the required analysis method
3. Add the agent to the controller's agent dictionary
4. Update the report template if needed

## Testing

Run the test suite:
```bash
pytest tests/
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 

For detailed guidelines on how to contribute, please see [CONTRIBUTING.md](CONTRIBUTING.md).

## Join the Project

**We Need Your Help!** This is Version 1.0 (Beta) - a work in progress developed over just a few days, which means:

- **Expect imperfections**: About 50% of feedback may be unusable, 30% mediocre, and 20% genuinely helpful
- **Your expertise matters**: Help us improve agent accuracy, especially specialized agents
- **Key areas for contribution**:
  - Developing specialized agents for different research fields
  - Improving prompt engineering for existing agents
  - Enhancing report generation and visualization
  - Adding support for different document formats
  - Implementing more sophisticated error detection

**Share your feedback**: Contact us at rjakob@ethz.ch with your experiences and suggestions

**Use more powerful models**: The default implementation uses ChatGPT 3.5 for accessibility, but you can configure the system to use more sophisticated models like GPT-4 with your own API keys.

Together, we can build the best review agent team and improve the quality of scientific publishing!