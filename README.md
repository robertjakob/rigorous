# Rigorous - AI-Powered Scientific Manuscript Analysis

> **Note:** This repository is currently private but is intended to be released as open source once the first functional version is made public on [https://www.rigorous.company/](https://www.rigorous.company/). We believe in transparency for how ratings and reviews are conducted, and we encourage others to experiment with and improve the code to advance open, rigorous peer review in science.

We want to change how scientific work is created, evaluated, and shared. This repository intends to provide the tools to make scientific publishing more transparent, affordable, and agile.

## Project Structure

- **Agent1_Peer_Review**: Advanced peer review system with specialized agents for comprehensive manuscript analysis, detailed feedback, and professional PDF report generation.
- **Agent2_Outlet_Fit**: (In Planning) Tool for evaluating manuscript fit with target journals/conferences.

## Current Status

### Active Tools
- **Agent1_Peer_Review**: ✅ Ready for use
  - Comprehensive manuscript analysis with specialized agents
  - Detailed feedback on sections, scientific rigor, and writing quality
  - JSON output with actionable recommendations
  - PDF report generation (see below)

### In Development
- **Agent2_Outlet_Fit**: 🚧 In Planning Phase
  - Will help reviewers evaluate manuscripts against specific criteria
  - Support journals/conferences in desk rejection decisions
  - Enable researchers to pre-check manuscripts before submission

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

## Earlier Iterations

Earlier iterations of the peer review system can be found in the `backup` folder:
- **V2_Editorial_First_Decision_Support**: Tool for checking manuscripts against editorial requirements.
- **V3_Peer_Review**: Enhanced tool for comprehensive peer review of academic manuscripts.
- **V4_Multi-Agent**: Advanced multi-agent system for collaborative peer review with specialized AI reviewers.
- **V5_Multi-Agent2**: Comprehensive multi-agent system with 25 specialized agents for more detailed, reliable, and specific feedback.

These are provided for reference only and are not part of the current production workflow.

## Requirements

- Python 3.7+
- OpenAI API key
- PDF manuscripts to analyze
- Dependencies listed in each tool's requirements.txt

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
