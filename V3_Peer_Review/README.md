# Academic Manuscript Peer Review Tool

This tool uses OpenAI's GPT-4 to perform automated peer reviews of academic manuscripts. It analyzes PDF manuscripts against a set of review criteria and provides detailed feedback, scores, and recommendations.

## Features

- Automated peer review of academic manuscripts
- Comprehensive analysis across multiple review criteria
- Detailed feedback with specific examples and suggestions
- Metadata extraction and document structure analysis
- Support for multiple PDF files
- Configurable review criteria

## Installation

1. Clone the repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
   Note: The tool will look for the .env file in the current directory first, then in the parent directory.

## Usage

1. Place your PDF manuscripts in the `manuscripts` directory
2. (Optional) Customize the review criteria in `review_criteria.json`
3. Run the review tool:
   ```bash
   python src/main.py --criteria review_criteria.json
   ```

### Command Line Arguments

- `--manuscripts-dir`: Directory containing PDF manuscripts (default: `manuscripts`)
- `--criteria`: Path to the review criteria JSON file (required)
- `--output-dir`: Directory to save review results (default: `analysis_results`)
- `--api-key`: OpenAI API key (optional if set in environment)

## Review Criteria

The tool evaluates manuscripts against the following criteria:

1. Originality and Innovation
2. Methodology
3. Results and Analysis
4. Writing and Presentation
5. Technical Accuracy
6. Literature Review
7. Figures and Tables
8. References
9. Ethical Considerations
10. Impact and Significance

Each criterion is scored on a scale of 1-5, with detailed feedback and specific examples provided.

## Output Format

The review results are saved in text files with the following sections:

- Manuscript Metadata
- Document Statistics
- Overall Assessment
- Detailed Assessment (per criterion)
  - Score
  - Feedback
  - Examples
  - Suggestions for Improvement

## Requirements

- Python 3.7+
- OpenAI API key
- PDF manuscripts to review

## License

This project is licensed under the MIT License - see the LICENSE file for details. 