# Rigorous - AI-Powered Scientific Manuscript Analysis

This repository contains a comprehensive suite of tools aimed at liberating science by making scientific publishing more transparent, cheaper, faster, and ensuring rigorous peer and AI review.

## Project Structure

- **V2_Editorial_First_Decision_Support**: Tool for checking manuscripts against editorial requirements
- **V3_Peer_Review**: Enhanced tool for comprehensive peer review of academic manuscripts
- **V4_Multi-Agent**: Advanced multi-agent system for collaborative peer review with specialized AI reviewers

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

## Requirements

- Python 3.7+
- OpenAI API key
- PDF manuscripts to analyze
- Dependencies listed in each tool's requirements.txt

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
