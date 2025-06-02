# Agent1_Peer_Review
A multi-agent system for comprehensive manuscript analysis and review.

> **Note:** This is an open-source project under the MIT License. We welcome contributions from the community to help improve the AI Reviewer system. Please feel free to submit issues, pull requests, or suggestions for improvements.

> **Cloud Version Available:** A cloud version of the AI Reviewer is now available at [https://www.rigorous.company/](https://www.rigorous.company/). Simply upload your manuscript, provide context on target journal and review focus, and receive a comprehensive PDF report via email within 1-2 working days. The cloud version is currently free for testing purposes. We would greatly appreciate your feedback in return via [this short form](https://docs.google.com/forms/d/1EhQvw-HdGRqfL01jZaayoaiTWLSydZTI4V0lJSvNpds) 


## Overview

This project implements a sophisticated multi-agent system for analyzing academic manuscripts. The system uses a combination of section-specific, rigor, and writing quality agents to provide detailed feedback and suggestions for improvement. Each agent specializes in a specific aspect of manuscript analysis and provides structured JSON output.

## Agent Structure

The system currently includes 24 spezialized agents focusing on the following review criteria across three main categories:

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

Per default spezialised agents use GPT-4.1-nano (long-context, cost-efficient model). You can also choose another (local) model.

### Quality Control Agents
Quality Control Agent serve as a validation layer across each category, they..
- Review and validate outputs from spezialized agents
- Ensure consistency and quality across analyses
- Provide a comprehensive final report with:
  - Validated scores and feedback
  - Critical remarks and improvement suggestions
  - Detailed explanations for each suggestion
  - Overall quality assessment
- Per default Quality Control Agents use GPT-4.1 for high-quality structured output. You can also choose another (local) model.

### Executive Summary Agent
The Executive Summary Agent provides a high-level synthesis through a two-step reasoning process:
1. Independent Review Generation
   - Analyzes the manuscript independently
   - Generates comprehensive review including summary, strengths/weaknesses, and suggestions
   - Focuses on target journal requirements and user priorities

2. Balanced Summary Generation
   - Synthesizes insights from both independent review and quality controlled results
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

1. Configure your manuscript details in `manuscript.json`:
```json
{
    "manuscript_src": "path/to/your/manuscript.pdf",
    "publicationOutlets" : "e.g. Nature Medicine",
    "reviewFocus" : "e.g. Statistics and Writing"
}
```

2. Run the analysis:
```bash
python run_local_aipeer_review.py
```

The script will:
- Process your manuscript using all specialized agents
- Generate a comprehensive analysis
- Create a detailed PDF report
- Save the report in the `reports/` directory

Note: The analysis typically takes about 15 minutes to complete.

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
├── reports/            # Generated PDF reports
├── manuscript.json     # Manuscript configuration
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

This project is open source under the MIT License. We welcome contributions from the community to help improve the AI Reviewer system. Please feel free to submit issues, pull requests, or suggestions for improvements.

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

3. **Manuscript Configuration**
   - Create or update `manuscript.json` with your manuscript details
   - Specify the PDF path and publication context
   - Define target journal and review focus areas

4. **Running the Analysis**
   ```bash
   python run_local_aipeer_review.py
   ```
   The script will process your manuscript and generate a PDF report in the `reports/` directory.

## Results

All results are saved in the `results`