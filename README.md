# Rigorous - AI-Powered Scientific Manuscript Analysis

> **Cloud Version Available:** A cloud version of the AI Peer Reviewer is now available at [https://www.rigorous.company/](https://www.rigorous.company/). Simply upload your manuscript, provide context on target journal and review focus, and receive a comprehensive PDF report via email within 1-2 working days. The cloud version is currently free for testing purposes.

This repository contains tools for making scientific publishing more transparent, cheaper, faster, and ensuring rigorous peer and AI review.

## Project Structure

- **Agent1_Peer_Review**: Advanced peer review system with specialized agents for comprehensive manuscript analysis, detailed feedback, and professional PDF report generation.
- **Agent2_Outlet_Fit**: (In Development) Tool for evaluating manuscript fit with target journals/conferences.

## Current Status

### Active Tools
- **Agent1_Peer_Review**: ✅ Ready for use
  - Comprehensive manuscript analysis with specialized agents
  - Detailed feedback on sections, scientific rigor, and writing quality
  - JSON output with actionable recommendations
  - PDF report generation (see below)

### In Development
- **Agent2_Outlet_Fit**: 🚧 In Development
  - Core functionality being implemented
  - Integration with Agent1_Peer_Review in progress
  - Testing and validation ongoing

## PDF Report Generation

This project includes a PDF report generator that creates a professional peer review report based on the outputs of the review agents.

### How to Generate the PDF Report

1. Ensure you have the required dependencies installed:
   - `reportlab`
   - `pillow`
   - (Other dependencies as listed in requirements.txt)

2. Make sure the following files are present and up to date:
   - `executive_summary.json` (executive summary and overall scores)
   - `quality_control_results.json` (detailed section, rigor, and writing results)
   - `logo.png` (logo for the report header)

3. Run the PDF generator script:

   ```bash
   python Agent1_Peer_Review/pdf_generator.py
   ```

4. The generated PDF will be saved to:
   - `Agent1_Peer_Review/results/review_report.pdf`

### Features
- Cover page with logo, manuscript title, and overall scores
- Executive summary and detailed analysis pages for all assessment items (S1–S10, R1–R7, W1–W7)
- Visually appealing tables for scores and suggestions
- Professional layout, color coding, and consistent formatting

For more details, see the comments in `Agent1_Peer_Review/pdf_generator.py`.

## Requirements

- Python 3.7+
- OpenAI API key
- PDF manuscripts to analyze
- Dependencies listed in each tool's requirements.txt

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
