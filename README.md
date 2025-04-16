# Manuscript Analysis Tools

This repository contains a collection of tools for analyzing academic manuscripts using OpenAI's GPT models.

## Project Structure

- **V2_Editorial_First_Decision_Support**: Tool for checking manuscripts against editorial requirements
- **V3_Peer_Review**: Enhanced tool for comprehensive peer review of academic manuscripts

## Shared Configuration

The project uses a shared `.env` file at the root level that contains configuration for all tools:

```
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

## Requirements

- Python 3.7+
- OpenAI API key
- PDF manuscripts to analyze

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
