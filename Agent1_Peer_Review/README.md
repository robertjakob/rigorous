# Agent1_Peer_Review

This directory contains the advanced peer review system for scientific manuscripts. Follow these steps to analyze your manuscript and generate a professional PDF report.

## Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/rigorous-7.git
   cd rigorous-7/Agent1_Peer_Review
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment:**
   - Add your OpenAI API key to the `.env` file:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

4. **Prepare Your Manuscript:**
   - Place your PDF manuscript in the `manuscripts` folder.
   - Ensure the `manuscripts` folder is included in the repository (it contains a `.gitkeep` file).

## Running the Analysis

1. **Run the Analysis:**
   ```bash
   python run_analysis.py
   ```
   This will analyze your manuscript using specialized agents and save the results in the `results` directory.

2. **Run Quality Control:**
   ```bash
   python run_quality_control.py
   ```
   This step validates the outputs from all agents and ensures consistency.

3. **Generate the Executive Summary:**
   ```bash
   python run_executive_summary.py
   ```
   This will create a high-level synthesis of the review, saved as `results/executive_summary.json`.

## Generating the PDF Report

1. **Run the PDF Generator:**
   ```bash
   python pdf_generator.py
   ```
   This will create a professional PDF report at `results/review_report.pdf`.

## Output Files

- **JSON Results:**
  - `results/section_results.json`: Detailed section analysis.
  - `results/rigor_results.json`: Rigor assessment results.
  - `results/writing_results.json`: Writing quality assessment.
  - `results/executive_summary.json`: High-level synthesis of the review.

- **PDF Report:**
  - `results/review_report.pdf`: Professional PDF report summarizing the review.

## Additional Information

- The `manuscripts` folder is included in the repository, but PDF files are ignored (see `.gitignore`).
- The `results` directory is ignored by Git to avoid pushing individual results to GitHub.

For more details, refer to the main project README.
