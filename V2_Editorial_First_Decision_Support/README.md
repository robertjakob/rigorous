# V2_Editorial_First_Decision_Support

A tool that analyzes academic manuscripts against editorial requirements using OpenAI's GPT models.

## Features

- Extracts text from PDF manuscripts
- Analyzes manuscript against a list of editorial requirements
- Identifies which requirements are met and which are not
- Provides specific evidence for unmet requirements
- Generates a desk rejection recommendation
- Processes multiple PDFs in batch

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your OpenAI API key:
   - Either set it as an environment variable: `export OPENAI_API_KEY=your-key-here`
   - Or provide it via command line argument: `--api-key your-key-here`

## Usage

1. Place your PDF manuscripts in the `manuscripts/` directory
2. Create a text file with your editorial requirements (one per line)
3. Run the checker:
   ```bash
   python src/main.py --requirements path/to/requirements.txt
   ```

   Optional arguments:
   - `--manuscripts-dir`: Directory containing PDFs (default: manuscripts)
   - `--output-dir`: Directory for analysis results (default: analysis_results)
   - `--api-key`: Your OpenAI API key

## Project Structure

```
.
├── manuscripts/           # Directory for PDF manuscripts
├── analysis_results/      # Directory for analysis output files
├── src/                  # Source code
│   ├── main.py
│   ├── pdf_parser.py
│   ├── openai_client.py
│   └── requirements_checker.py
├── requirements.txt      # Python dependencies
└── example_requirements.txt  # Example requirements file
```

## Example Requirements File

```
Manuscript must be under 5000 words
Abstract must be structured (Background, Methods, Results, Conclusion)
Figures must be in high resolution (300 DPI minimum)
```

## Output

For each PDF in the manuscripts directory, the tool will:
1. Create a separate analysis file in the `analysis_results/` directory
2. Name the file `{manuscript_name}_analysis.txt`
3. Include:
   - Analysis of each requirement (met/not met)
   - Evidence for unmet requirements
   - Final desk rejection recommendation with justification

## Development

The project structure is modular and easy to extend:
- `pdf_parser.py`: Handles PDF text extraction
- `openai_client.py`: Manages OpenAI API interactions
- `requirements_checker.py`: Orchestrates the analysis process
- `main.py`: Provides the CLI interface 
