# Manuscript Reviewer V6

A multi-agent system for comprehensive manuscript analysis and review.

## Overview

This project implements a sophisticated multi-agent system for analyzing academic manuscripts. The system uses a combination of section-specific, rigor, and writing quality agents to provide detailed feedback and suggestions for improvement. Each agent specializes in a specific aspect of manuscript analysis and provides structured JSON output.

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
- W1: Language and Style
- W2: Narrative and Structure
- W3: Clarity and Conciseness
- W4: Terminology Consistency
- W5: Inclusive Language
- W6: Citation Formatting
- W7: Target Audience Alignment
- W8: Visual Presentation

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

## Output

The system generates JSON files in the `results/` directory containing:
- Individual agent results (`{agent_name}_results.json`)
- Combined results (`combined_results.json`)
- Manuscript data (`manuscript_data.json`)

Each agent's analysis follows a consistent JSON structure:

```json
{
    "score": int,  // Score from 1-5
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

## Configuration

- Environment variables are managed in `.env`
- Agent configurations can be modified in `src/core/config.py`
- Model settings can be adjusted in `src/core/config.py`

## Development

### Project Structure
```
V6_multi_agent3/
├── src/
│   ├── reviewer_agents/
│   │   ├── section/      # Section agents (S1-S10)
│   │   ├── rigor/        # Rigor agents (R1-R7)
│   │   ├── writing/      # Writing agents (W1-W8)
│   │   └── controller_agent.py
│   ├── core/            # Core functionality and configuration
│   └── utils/           # Utility functions
├── manuscripts/         # Input manuscripts
├── results/            # Analysis results
└── tests/             # Test suite
```

### Adding New Agents

1. Create a new agent class inheriting from `BaseReviewerAgent`
2. Implement the required analysis method
3. Add the agent to the controller's agent dictionary

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

**We Need Your Help!** This is Version 6.0 - a work in progress, which means:

- **Expect imperfections**: The system is continuously being improved
- **Your expertise matters**: Help us improve agent accuracy, especially specialized agents
- **Key areas for contribution**:
  - Developing specialized agents for different research fields
  - Improving prompt engineering for existing agents
  - Enhancing analysis accuracy
  - Adding support for different document formats
  - Implementing more sophisticated error detection

**Share your feedback**: Contact us at rjakob@ethz.ch with your experiences and suggestions

**Use more powerful models**: The default implementation uses GPT-4.1-nano for accessibility, but you can configure the system to use more sophisticated models with your own API keys.

Together, we can build the best review agent team and improve the quality of scientific publishing!