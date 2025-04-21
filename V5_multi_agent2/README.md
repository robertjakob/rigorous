# Multi-Agent Academic Paper Review System

A comprehensive system for automated academic paper review using specialized AI agents.

## Project Structure

```
V5_multi_agent2/
├── src/
│   ├── reviewer_agents/
│   │   ├── rigor/           # Scientific rigor agents (R1-R7)
│   │   └── writing/         # Writing and presentation agents (W1-W4)
│   ├── agents/
│   │   └── base/            # Base agent classes and utilities
│   ├── config/              # Configuration files
│   ├── utils/               # Utility functions
│   └── main.py              # Main entry point
├── manuscripts/             # Directory for PDF manuscripts to be analyzed
├── requirements.txt         # Project dependencies
└── README.md               # This file
```

## Agent Categories

### 1. Scientific Rigor Agents (R1-R7)

These agents evaluate the scientific quality and rigor of the research:

- **R1: Methodology Agent**
  - Focus: Research design, methodology, and approach
  - Evaluates: Study design, methods, procedures, and research approach

- **R2: Impact & Significance Agent**
  - Focus: Research impact and significance
  - Evaluates: Scientific contribution, field influence, and practical implications

- **R3: Ethics & Compliance Agent**
  - Focus: Ethical considerations and research standards
  - Evaluates: Conflicts of interest, data privacy, consent procedures, research integrity

- **R4: Data & Code Availability Agent**
  - Focus: Data and code sharing practices
  - Evaluates: Data availability, code repository, documentation, reproducibility

- **R5: Statistical Rigor Agent**
  - Focus: Statistical methods and analysis
  - Evaluates: Statistical test selection, assumptions, sample size, power analysis

- **R6: Technical Accuracy Agent**
  - Focus: Technical content and derivations
  - Evaluates: Mathematical correctness, algorithm efficiency, technical terminology

- **R7: Consistency Agent**
  - Focus: Overall consistency and coherence
  - Evaluates: Internal consistency, logical flow, cross-references

### 2. Writing and Presentation Agents (W1-W4)

These agents evaluate the writing quality and presentation of the research:

- **W1: Language & Style Agent**
  - Focus: Language quality and writing style
  - Evaluates: Grammar, vocabulary, tone, academic writing conventions

- **W2: Narrative & Structure Agent**
  - Focus: Paper structure and narrative flow
  - Evaluates: Organization, logical flow, section transitions, argument structure

- **W3: Clarity & Conciseness Agent**
  - Focus: Writing clarity and conciseness
  - Evaluates: Readability, sentence structure, paragraph organization, clarity

- **W4: Terminology Consistency Agent**
  - Focus: Terminology and notation consistency
  - Evaluates: Term usage, notation consistency, definition clarity

## Features

- Comprehensive manuscript analysis across multiple dimensions
- Specialized agents for different aspects of academic writing and research
- Structured feedback in JSON format
- Configurable review criteria
- Support for different research types
- Error handling and logging
- PDF manuscript processing

## Usage

1. Place your manuscript PDF in the `manuscripts/` directory
2. Run the main script to initiate the review process
3. Receive comprehensive feedback from all specialized agents

## Requirements

- Python 3.8+
- Dependencies listed in requirements.txt

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

The system can be configured through the files in the `config/` directory:
- Agent configurations
- Review criteria
- Output formats
- Model settings

## Output Format

Each agent provides:
- Comprehensive score (1-10)
- Critical remarks
- Improvement suggestions
- Detailed feedback
- Summary of findings

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 