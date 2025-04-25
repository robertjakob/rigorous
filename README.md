# Rigorous - AI-Powered Scientific Manuscript Analysis

This repository contains a comprehensive suite of tools aimed at liberating science by making scientific publishing more transparent, cheaper, faster, and ensuring rigorous peer and AI review.

## Project Structure

- **V2_Editorial_First_Decision_Support**: Tool for checking manuscripts against editorial requirements
- **V3_Peer_Review**: Enhanced tool for comprehensive peer review of academic manuscripts
- **V4_Multi-Agent**: Advanced multi-agent system for collaborative peer review with specialized AI reviewers
- **V5_Multi-Agent2**: Comprehensive multi-agent system with 25 specialized agents for more detailed, reliable, and specific feedback

## Shared Configuration

The project uses a shared `.env` file at the root level that contains configuration for all tools:

```bash
# OpenAI API Key
OPENAI_API_KEY=your_api_key_here
```

This shared configuration allows you to use the same API key across all versions of the tools without duplicating it in multiple locations.

## Installation

1. Clone the repository
2. Create a `.env` file in the root directory with your OpenAI API key
3. Install the required dependencies for each tool:

```bash
# For V2_Editorial_First_Decision_Support
cd V2_Editorial_First_Decision_Support
pip install -r requirements.txt

# For V3_Peer_Review
cd V3_Peer_Review
pip install -r requirements.txt

# For V4_Multi-Agent
cd V4_multi_agent
pip install -r requirements.txt
```

## Usage

### V2_Editorial_First_Decision_Support

This tool checks manuscripts against a set of editorial requirements.

1. Place your PDF manuscripts in the `manuscripts` directory
2. Create a requirements file (e.g., `requirements_1.txt`)
3. Run the tool:
```bash
cd V2_Editorial_First_Decision_Support
python src/main.py --requirements requirements_1.txt
```

### V3_Peer_Review

This tool performs comprehensive peer reviews of academic manuscripts.

1. Place your PDF manuscripts in the `manuscripts` directory
2. (Optional) Customize the review criteria in `review_criteria.json`
3. Run the tool:
```bash
cd V3_Peer_Review
python src/main.py --criteria review_criteria.json
```

### V4_Multi-Agent

The V4 system implements a sophisticated multi-agent approach to peer review, where specialized AI agents collaborate to provide comprehensive manuscript evaluation.

#### Key Features:
- Multiple specialized reviewer agents (Language, Methodology, Ethics)
- Coordinated review process with synthesis
- Detailed individual reviews from each agent
- Comprehensive final report with actionable insights

#### Running the System:
1. Place your manuscript in the `manuscripts` directory
2. Ensure review criteria are set in `review_criteria.txt`
3. Run the tool:
```bash
cd V4_multi_agent
python src/main.py --manuscript manuscripts/your_paper.pdf --criteria review_criteria.txt --output output/review_results.json
```

#### Arguments:
- `--manuscript`: Path to the PDF manuscript
- `--criteria`: Path to review criteria file (default: review_criteria.txt)
- `--output`: Path for saving review results

#### System Components:

1. **Editor Agent** (`editor_agent.py`):
   - Analyzes manuscript requirements
   - Creates specialized review teams
   - Manages review workflow

2. **Specialized Review Agents** (`specialized_agent.py`):
   - Language and Clarity Expert
   - Methodology Expert
   - Ethics and Compliance Expert
   - Domain-specific reviewers (as needed)

3. **Coordinator Agent** (`coordinator_agent.py`):
   - Synthesizes individual reviews
   - Resolves conflicting feedback
   - Generates final recommendations

4. **Support Components**:
   - `pdf_parser.py`: PDF document processing
   - `review_criteria_parser.py`: Review criteria management
   - `openai_client.py`: AI model interactions

#### Output Files:
- `review_plan.json`: Initial review strategy
- Individual agent reviews (e.g., `language_reviewer_review.json`)
- `specialized_reviews.json`: All specialized reviews
- `synthesis.json`: Coordinated synthesis
- `review_results.json`: Final comprehensive report

### V5_Multi-Agent2

The V5 system represents a significant advancement over previous versions, featuring a comprehensive suite of 25 specialized agents that provide more reliable, specific, and actionable feedback.

#### Key Features:
- **Three Categories of Specialized Agents**:
  - **Section Agents (S1-S10)**: Analyze specific sections (Title/Keywords, Abstract, Introduction, etc.)
  - **Rigor Agents (R1-R7)**: Evaluate scientific rigor (Originality, Ethics, Data Availability, etc.)
  - **Writing Agents (W1-W8)**: Assess writing quality (Language, Structure, Clarity, etc.)
- **Comprehensive Report**: Detailed assessment with scores, critical remarks, and improvement suggestions
- **Modular Design**: Easy to extend with new specialized agents
- **Better Reliability**: Multiple specialized agents provide more consistent and reliable feedback
- **Actionable Feedback**: Specific, section-focused recommendations for manuscript improvement

#### Running the System:
1. Place your manuscript PDF in the `manuscripts/` directory
2. Run the analysis:
```bash
cd V5_multi_agent2
python run_analysis.py
```
3. Generate the report:
```bash
bash scripts/generate_report.sh
```

The comprehensive report will be saved in `results/manuscript_report.md`.

#### Advanced Features:
- Support for more powerful models (GPT-4, Claude) for enhanced analysis
- Configurable agent behavior through environment variables
- Extensible architecture for adding domain-specific agents

#### Why V5 Is Better:
Through development and testing, we found that having a larger number of highly specialized agents produces more reliable and specific feedback compared to fewer general-purpose agents. Each agent in V5 focuses on a narrow aspect of the manuscript, allowing for deeper analysis and more precise recommendations.

## Requirements

- Python 3.7+
- OpenAI API key
- PDF manuscripts to analyze
- Dependencies listed in each tool's requirements.txt

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
