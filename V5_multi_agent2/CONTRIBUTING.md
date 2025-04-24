# Contributing to Manuscript Reviewer

Thank you for considering contributing to Manuscript Reviewer! This document provides guidelines and instructions for contributing to the project.

## Project Status

**Important**: This project is currently in Version 1.0 (Beta), developed in a short timeframe. Expect hallucinations and errors. About 50% of feedback will likely be unusable, 30% mediocre, and 20% helpful. This is precisely why we need your contributions!

## How Can I Contribute?

### 1. Developing New Agents

We welcome contributions of new specialized agents:
- **Domain-specific agents**: Create agents specialized for specific research fields (e.g., medicine, computer science, social sciences)
- **Methodology agents**: Develop agents to assess specialized methodologies (e.g., clinical trials, machine learning, qualitative research)
- **Statistical review agents**: Create agents to validate complex statistical approaches

### 2. Improving Existing Agents

Help enhance our current agents:
- **Prompt engineering**: Refine agent prompts for better analysis
- **Error detection**: Improve the ability to identify common errors
- **Response formatting**: Enhance the structure and clarity of agent feedback

### 3. System Improvements

Contribute to the core system:
- **PDF parsing**: Enhance text and figure extraction
- **Report generation**: Improve the readability and usefulness of reports
- **Performance optimization**: Make the system faster and more efficient
- **UI/UX**: Build interfaces for easier interaction with the system

### 4. Documentation and Testing

Help make the project more accessible:
- **Documentation**: Improve installation and usage instructions
- **Tutorials**: Create examples and tutorials for different use cases
- **Testing**: Develop comprehensive tests for different components

## Getting Started

1. **Set up your environment**:
   ```bash
   git clone https://github.com/robertjakob/rigorous.git
   cd rigorous/V5_multi_agent2
   pip install -r requirements.txt
   pip install -e .  # Install in development mode
   ```

2. **Configure API keys**:
   Create a `.env` file based on the example and add your API keys if using OpenAI models.

3. **Test the system**:
   ```bash
   # Place a PDF in the manuscripts directory
   python run_analysis.py
   # Generate a report
   bash scripts/generate_report.sh
   ```

## Development Workflow

1. **Create a new branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Follow the existing code style
   - Add appropriate comments
   - Keep functions focused and modular

3. **Test your changes**:
   ```bash
   pytest
   ```

4. **Submit a pull request**:
   - Provide a clear description of your changes
   - Reference any related issues
   - Explain how your changes improve the project

## Code Standards

- Use clear, descriptive variable and function names
- Follow PEP 8 style guidelines
- Include docstrings for all functions and classes
- Write unit tests for new functionality

## Adding a New Agent

1. Create a new file in the appropriate directory:
   - `src/reviewer_agents/section/` for section agents
   - `src/reviewer_agents/rigor/` for rigor agents
   - `src/reviewer_agents/writing/` for writing agents

2. Inherit from the `BaseReviewerAgent` class:
   ```python
   from src.reviewer_agents.base_agent import BaseReviewerAgent
   
   class YourNewAgentName(BaseReviewerAgent):
       def __init__(self, model="gpt-3.5-turbo"):
           super().__init__(model)
           self.name = "YourAgentCode"  # e.g., S11, R8, W9
           self.category = "your_category"  # e.g., "section", "rigor", "writing"
   
       def analyze_your_feature(self, text, research_type=None):
           # Implement your analysis method
           # Return a properly structured response
   ```

3. Add your agent to the controller in `src/reviewer_agents/controller_agent.py`

## Communication

- **Issues**: Use GitHub issues for bug reports and feature requests
- **Discussions**: Join GitHub discussions for general questions
- **Email**: Contact rjakob@ethz.ch for private communications

## Thank You

Your contributions help improve scientific publishing and research quality. We appreciate your support in this mission! 