# V5 Multi-Agent Manuscript Review System

A sophisticated multi-agent system for comprehensive scientific manuscript review, leveraging GPT models to evaluate various aspects of research quality, writing, and presentation.

## Overview

This system employs a team of specialized AI agents to perform thorough manuscript reviews, each focusing on specific aspects of research quality and presentation. The system is designed to provide detailed, structured feedback that helps authors improve their manuscripts.

## Agent Structure

### Research Quality Agents (R1-R7)

1. **R1 - Originality & Contribution Agent**
   - Evaluates research novelty and contributions
   - Assesses advancement of knowledge
   - Verifies claims of innovation

2. **R2 - Impact & Significance Agent**
   - Analyzes field influence
   - Evaluates broader implications
   - Assesses practical applications

3. **R3 - Ethics & Compliance Agent**
   - Reviews ethical considerations
   - Checks research integrity
   - Evaluates consent procedures

4. **R4 - Data & Code Availability Agent**
   - Assesses data sharing practices
   - Evaluates code availability
   - Reviews reproducibility

5. **R5 - Statistical Rigor Agent**
   - Analyzes statistical methods
   - Evaluates sample size justification
   - Reviews statistical reporting

6. **R6 - Technical Accuracy Agent**
   - Verifies technical details
   - Checks mathematical derivations
   - Evaluates algorithm descriptions

7. **R7 - Consistency Agent**
   - Ensures internal consistency
   - Verifies cross-references
   - Checks terminology usage

### Writing & Presentation Agents (W1-W8)

1. **W1 - Language Style Agent**
   - Evaluates writing style
   - Checks grammar and clarity
   - Assesses academic tone

2. **W2 - Narrative Structure Agent**
   - Analyzes logical flow
   - Evaluates section organization
   - Checks argument coherence

3. **W3 - Clarity & Conciseness Agent**
   - Reviews sentence structure
   - Evaluates paragraph organization
   - Checks for redundancy

4. **W4 - Terminology Consistency Agent**
   - Ensures consistent terminology
   - Checks acronym usage
   - Verifies field-specific terms

5. **W5 - Inclusive Language Agent**
   - Evaluates language inclusivity
   - Checks for bias
   - Assesses accessibility

6. **W6 - Citation Formatting Agent**
   - Verifies citation style
   - Checks reference list
   - Evaluates in-text citations

7. **W7 - Target Audience Agent**
   - Assesses audience alignment
   - Evaluates technical depth
   - Checks field-specific conventions

8. **W8 - Visual Presentation Agent**
   - Reviews figure quality
   - Evaluates table formatting
   - Checks visual elements

## Features

- **Comprehensive Analysis**: Each agent provides detailed feedback on specific aspects of the manuscript
- **Structured Output**: Results are provided in a clear, organized format
- **Actionable Feedback**: Each evaluation includes specific improvement suggestions
- **Automated Report Generation**: Creates a detailed markdown report combining all agent feedback
- **Error Handling**: Robust error handling and recovery mechanisms
- **Configurable**: Easy to modify agent parameters and evaluation criteria

## Usage

1. **Setup**
   ```bash
   # Clone the repository
   git clone https://github.com/yourusername/rigorous.git
   cd rigorous/V5_multi_agent2

   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Running Analysis**
   ```bash
   # Run the analysis on a manuscript
   python run_analysis.py
   ```

3. **Generating Reports**
   ```bash
   # Generate a comprehensive report
   ./scripts/generate_report.sh
   ```

## Output

The system generates several types of output:

1. **Individual Agent Results**: JSON files containing detailed feedback from each agent
2. **Combined Results**: A comprehensive JSON file combining all agent feedback
3. **Manuscript Report**: A well-formatted markdown report with all findings and suggestions

## Configuration

- Model selection can be configured in `config.py`
- Agent parameters can be adjusted in individual agent files
- Report generation settings can be modified in `src/utils/json_to_report.py`

## Requirements

- Python 3.8+
- OpenAI API access
- Required Python packages (see requirements.txt)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 