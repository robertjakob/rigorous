# Agent1_Peer_Review

> **Note:** This is an open-source project under the MIT License. We welcome contributions from the community to help improve the AI Reviewer system. Please feel free to submit issues, pull requests, or suggestions for improvements.

> **Cloud Version Available:** A cloud version of the AI Reviewer is now available at [https://www.rigorous.company/](https://www.rigorous.company/). Simply upload your manuscript, provide context on target journal and review focus, and receive a comprehensive PDF report via email within 1-2 working days. The cloud version is currently free for testing purposes. We would greatly appreciate your feedback in return via [this short form](https://docs.google.com/forms/d/1EhQvw-HdGRqfL01jZaayoaiTWLSydZTI4V0lJSvNpds) 

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

### Writing Agents (W1-W7)
- W1: Language and Style
- W2: Narrative and Structure
- W3: Clarity and Conciseness
- W4: Terminology Consistency
- W5: Inclusive Language
- W6: Citation Formatting
- W7: Target Audience Alignment

### Quality Control Agent
The Quality Control Agent serves as a final validation layer that:
- Reviews and validates outputs from all other agents
- Ensures consistency and quality across all analyses
- Provides a comprehensive final report with:
  - Validated scores and feedback
  - Critical remarks and improvement suggestions
  - Detailed explanations for each suggestion
  - Overall quality assessment
- Uses GPT-4.1 for high-quality structured output

### Executive Summary Agent
The Executive Summary Agent provides a high-level synthesis through a two-step reasoning process:
1. Independent Review Generation
   - Analyzes the manuscript without bias
   - Generates comprehensive review including summary, strengths/weaknesses, and suggestions
   - Focuses on target journal requirements and user priorities

2. Balanced Summary Generation
   - Synthesizes insights from both independent review and quality control results
   - Creates a unified executive summary in three paragraphs:
     * Overview of content and contribution
     * Balanced assessment of strengths and weaknesses
     * Actionable recommendations
   - Ensures natural flow while incorporating key insights
   - Maintains consistency with detailed assessment

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
3. Run quality control:
```bash
python run_quality_control.py
```
4. Generate executive summary:
```bash
python run_executive_summary.py
```

## Output

The system generates JSON files in the `results/` directory containing:
- Individual agent results (`{agent_name}_results.json`)
- Combined results (`combined_results.json`)
- Manuscript data (`manuscript_data.json`)
- Quality control results (`quality_control_results.json`)
- Executive summary (`executive_summary.json`)

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

The executive summary follows a specific structure:
```json
{
    "manuscript_title": str,
    "executive_summary": str,  // Three-paragraph synthesis
    "independent_review": {
        "summary": str,
        "strengths_weaknesses": {
            "strengths": [str],
            "weaknesses": [str]
        },
        "critical_suggestions": [str]
    },
    "scores": {
        "section_score": float,
        "rigor_score": float,
        "writing_score": float,
        "final_score": float
    }
}
```

## Configuration

- Environment variables are managed in `.env`
- Agent configurations can be modified in `src/core/config.py`
- Model settings can be adjusted in `src/core/config.py`

## Development

### Project Structure
```
Agent1_Peer_Review/
├── src/
│   ├── reviewer_agents/
│   │   ├── section/      # Section agents (S1-S10)
│   │   ├── rigor/        # Rigor agents (R1-R7)
│   │   ├── writing/      # Writing agents (W1-W7)
│   │   ├── quality/      # Quality control agent
│   │   └── executive_summary_agent.py
│   ├── core/            # Core functionality and configuration
│   └── utils/           # Utility functions
├── manuscripts/         # Input manuscripts
├── results/            # Analysis results
├── context/           # User context and preferences
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

This project is open source under the MIT License. We welcome contributions from the community to help improve the AI Peer Reviewer system. Please feel free to submit issues, pull requests, or suggestions for improvements.

## Join the Project

**We Need Your Help!** This a work in progress, which means:

- **Expect imperfections**: The system is continuously being improved
- **Your expertise matters**: Help us improve agent accuracy, especially specialized agents
- **Key areas for contribution**:
  - Developing specialized agents for different research fields
  - Improving prompt engineering for existing agents
  - Enhancing analysis accuracy
  - Adding support for different document formats
  - Implementing more sophisticated error detection

**Share your feedback**: Contact us at rjakob@ethz.ch with your experiences and suggestions

**Use more powerful models**: The default implementation uses GPT-4.1 for accessibility, but you can configure the system to use more sophisticated models with your own API keys.

Together, we can build the best review agent team and improve the quality of scientific publishing!

## Manuscripts Folder

The `manuscripts` folder is where you should place the PDF manuscripts you want to analyze. Please ensure your PDF files are stored here before running the review process.

## Environment Configuration

A `.env` file is provided in this directory. You can add your OpenAI API key to this file as follows:

```
OPENAI_API_KEY=your_openai_api_key_here
```

Replace `your_openai_api_key_here` with your actual OpenAI API key.

## Additional Information

For more details on how to use this system, please refer to the main project README.

## Setup Instructions

1. **Environment Setup**
   ```bash
   # Create and activate a virtual environment (optional but recommended)
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install required dependencies
   pip install -r requirements.txt
   ```

2. **API Key Configuration**
   - Create a `.env` file in the Agent1_Peer_Review directory
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     DEFAULT_MODEL=gpt-4.1-nano
     ```

3. **Manuscript Preparation**
   - Place your PDF manuscript in the `manuscripts` folder
   - The system will automatically use the first PDF file it finds

4. **Context Configuration**
   - Review and update `context/context.json` with your specific requirements
   - This file contains target journal information and review focus areas

## Running the Analysis

1. **Initial Analysis**
   ```bash
   python run_analysis.py
   ```
   This generates:
   - Section results (S1-S10)
   - Rigor results (R1-R7)
   - Writing results (W1-W7)

2. **Quality Control**
   ```bash
   python run_quality_control.py
   ```
   Validates and processes the analysis results

3. **Executive Summary**
   ```bash
   python run_executive_summary.py
   ```
   Creates a high-level synthesis of the review

4. **PDF Report Generation**
   ```bash
   python pdf_generator.py
   ```
   Generates a professional PDF report at `results/review_report.pdf`

## Results

All results are saved in the `results` directory:
- `section_results.json`: Detailed section analysis
- `rigor_results.json`: Scientific rigor assessment
- `writing_results.json`: Writing quality evaluation
- `quality_control_results.json`: Validated results
- `executive_summary.json`: High-level synthesis
- `review_report.pdf`: Professional PDF report

## Future Improvements

1. **Visual Content Analysis**
   - New agent category for figures and tables (F1-F5)
   - Assessment criteria:
     - F1: Figure clarity and readability
     - F2: Data visualization best practices
     - F3: Statistical representation accuracy
     - F4: Figure-text consistency
     - F5: Accessibility and color scheme

2. **Enhanced Quality Control**
   - Cross-validation between different agent categories
   - Automated consistency checks for scoring
   - Confidence scoring for each assessment

3. **Interactive Review Interface**
   - Real-time progress tracking
   - Customizable review criteria

4. **Advanced Analytics**
   - Comparative analysis against similar manuscripts
   - Trend analysis for specific research areas
   - Automated recommendation engine for improvements

5. **Integration Capabilities**
   - Direct submission to journal systems
   - Integration with reference management software
   - Export to various academic formats

## Additional Information

For more details on how to use this system, please refer to the main project README.
