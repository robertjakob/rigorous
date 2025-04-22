# Manuscript Review Report Generator

This tool converts the JSON results from the multi-agent manuscript review system into a well-structured Markdown report.

## Overview

The report generator takes the `combined_results.json` file produced by the multi-agent review system and transforms it into a comprehensive Markdown report that includes:

- Overall assessment with average scores
- Individual agent reports with:
  - Specific scores for each evaluation criterion
  - Summaries of findings
  - Critical remarks with severity levels
  - Improvement suggestions with original and improved text
  - Detailed feedback for each evaluation category

## Usage

### Using the Shell Script

The easiest way to generate a report is to use the provided shell script:

```bash
./scripts/generate_report.sh
```

This will:
1. Read the combined results from `/results/combined_results.json`
2. Generate a report at `/results/manuscript_report.md`
3. Automatically open the report if you're on macOS

### Using the Python Script Directly

You can also use the Python script directly with custom input and output paths:

```bash
python src/utils/json_to_report.py --input /path/to/input.json --output /path/to/output.md
```

### Command Line Arguments

- `--input`, `-i`: Path to the input JSON file (default: `/results/combined_results.json`)
- `--output`, `-o`: Path to save the output report (default: `/results/manuscript_report.md`)

## Report Structure

The generated report follows this structure:

1. **Overall Assessment**
   - Average score across all evaluation criteria
   - Total number of critical remarks and improvement suggestions

2. **Individual Agent Reports**
   - For each agent (R1, R2, W1, etc.):
     - Specific score for the agent's evaluation criterion
     - Summary of findings
     - Critical remarks with category, location, issue, severity, and impact
     - Improvement suggestions with original text, improved version, and explanation
     - Detailed feedback for each evaluation category

## Customization

To modify the report format, you can edit the following functions in `src/utils/json_to_report.py`:

- `format_critical_remarks()`: Change how critical remarks are formatted
- `format_improvement_suggestions()`: Change how improvement suggestions are formatted
- `format_detailed_feedback()`: Change how detailed feedback is formatted
- `generate_agent_report()`: Modify the structure of individual agent reports
- `generate_overall_report()`: Change the overall report structure

## Requirements

- Python 3.6+
- No additional dependencies beyond the standard library 