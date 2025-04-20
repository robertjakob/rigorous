# Multi-Agent Scientific Paper Review System

A sophisticated system that uses multiple AI agents to provide comprehensive peer review of scientific papers. The system simulates a team of expert reviewers, each with specific expertise and focus areas, to analyze papers from multiple perspectives.

## Features

### 1. Specialized Review Agents
- **Core Reviewers** (Always included):
  - Language and Style Expert
  - Methodology Expert
  - Ethics and Compliance Expert
  - Literature Review Expert
  - Impact and Significance Expert
  - Research Gap and Contribution Expert

- **Domain-Specific Reviewers** (Added based on paper content):
  - Technical Area Experts (e.g., Machine Learning, Healthcare Systems)
  - Field-Specific Experts (e.g., Computer Science, Medical Research)

- **Specialized Reviewers** (Added based on requirements):
  - Data Analysis Expert
  - Experimental Design Expert
  - Literature Coverage Expert
  - Research Gap and Contribution Expert

### 2. Key Scientist Simulation
- Identifies influential scientists in the field
- Simulates their likely perspective and feedback
- Considers their research focus and typical review style
- Provides realistic reviewer comments

### 3. Comprehensive Analysis
- Paper analysis and domain identification
- Research gap analysis
- Contribution positioning
- Literature coverage assessment
- Methodology evaluation
- Impact assessment

### 4. Detailed Reporting
- Executive summary
- Individual reviewer feedback
- Thematic analysis across reviews
- Specific recommendations
- Final assessment and timeline

## Technical Details

### Model Configuration
- Supports multiple OpenAI models:
  - Default: GPT-3.5-turbo (for testing)
  - Production: GPT-4-turbo-preview (for high-quality reviews)
- Easy model switching for different use cases

### Output Format
```json
{
    "review_plan": {
        "paper_analysis": {...},
        "review_team": {...},
        "key_scientists": [...],
        "simulated_feedback": {...}
    },
    "final_report": {
        "executive_summary": {...},
        "reviewer_feedback": {...},
        "thematic_analysis": {...},
        "specific_recommendations": {...},
        "final_assessment": {...}
    }
}
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure OpenAI API key:
- Create a `.env` file in the project root
- Add your OpenAI API key:
```
OPENAI_API_KEY=your-api-key-here
```

3. Run the system:
```bash
python src/test_editor.py
```

## Usage

1. Initialize the editor agent:
```python
from editor_agent import EditorAgent

# Use default model (GPT-3.5-turbo)
editor = EditorAgent()

# Or specify custom model configuration
editor = EditorAgent({
    "default": "gpt-3.5-turbo",
    "production": "gpt-4-turbo-preview",
    "current": "default"
})
```

2. Generate a review:
```python
result = editor.generate_review_plan(paper_content)
```

3. Switch models if needed:
```python
editor.set_model("production")  # Switch to GPT-4
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 