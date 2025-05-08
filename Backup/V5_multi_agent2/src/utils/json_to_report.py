#!/usr/bin/env python3
"""
JSON to Report Converter

This script converts the combined_results.json file into a well-structured text report.
"""

import json
import os
import argparse
from datetime import datetime
from typing import Dict, Any, List


def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load and parse a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return {}


def format_critical_remarks(remarks: List[Dict[str, Any]]) -> str:
    """Format critical remarks into a readable text section."""
    if not remarks:
        return "No critical remarks identified."
    
    formatted_remarks = []
    for i, remark in enumerate(remarks, 1):
        formatted_remark = (
            f"### Remark {i}\n\n"
            f"**Category**: {remark.get('category', 'N/A')}  \n"
            f"**Location**: {remark.get('location', 'N/A')}  \n"
            f"**Issue**: {remark.get('issue', 'N/A')}  \n"
            f"**Severity**: {remark.get('severity', 'N/A')}  \n"
            f"**Impact**: {remark.get('impact', 'N/A')}"
        )
        formatted_remarks.append(formatted_remark)
    
    return "\n\n".join(formatted_remarks)


def format_improvement_suggestions(suggestions: List[Dict[str, Any]]) -> str:
    """Format improvement suggestions into a readable text section."""
    if not suggestions:
        return "No improvement suggestions provided."
    
    formatted_suggestions = []
    for i, suggestion in enumerate(suggestions, 1):
        formatted_suggestion = (
            f"### Suggestion {i}\n\n"
            f"**Location**: {suggestion.get('location', 'N/A')}  \n"
            f"**Category**: {suggestion.get('category', 'N/A')}  \n"
            f"**Focus**: {suggestion.get('focus', 'N/A')}  \n\n"
            f"**Original Text**:  \n"
            f"> {suggestion.get('original_text', 'N/A')}\n\n"
            f"**Improved Version**:  \n"
            f"> {suggestion.get('improved_version', 'N/A')}\n\n"
            f"**Explanation**:  \n"
            f"{suggestion.get('explanation', 'N/A')}"
        )
        formatted_suggestions.append(formatted_suggestion)
    
    return "\n\n".join(formatted_suggestions)


def format_detailed_feedback(feedback: Dict[str, str]) -> str:
    """Format detailed feedback into a readable text section."""
    if not feedback:
        return "No detailed feedback provided."
    
    formatted_feedback = []
    for category, content in feedback.items():
        # Convert category name from snake_case to Title Case
        category_title = category.replace('_', ' ').title()
        formatted_feedback.append(f"### {category_title}\n\n{content}")
    
    return "\n\n".join(formatted_feedback)


def get_score_field(agent_name: str) -> str:
    """Get the appropriate score field name for each agent type."""
    score_fields = {
        # Section agents
        'S1': 'title_keywords_score',
        'S2': 'abstract_score',
        'S3': 'introduction_score',
        'S4': 'literature_review_score',
        'S5': 'methodology_score',
        'S6': 'results_score',
        'S7': 'discussion_score',
        'S8': 'conclusion_score',
        'S9': 'references_score',
        'S10': 'supplementary_materials_score',
        
        # Rigor agents
        'R1': 'originality_contribution_score',
        'R2': 'impact_significance_score',
        'R3': 'ethics_compliance_score',
        'R4': 'data_code_availability_score',
        'R5': 'statistical_rigor_score',
        'R6': 'technical_accuracy_score',
        'R7': 'consistency_score',
        
        # Writing agents
        'W1': 'language_style_score',
        'W2': 'narrative_structure_score',
        'W3': 'clarity_conciseness_score',
        'W4': 'terminology_consistency_score',
        'W5': 'inclusive_language_score',
        'W6': 'citation_formatting_score',
        'W7': 'target_audience_score',
        'W8': 'visual_presentation_score'
    }
    return score_fields.get(agent_name, 'score')


def generate_agent_report(agent_name: str, agent_data: Dict[str, Any]) -> str:
    """Generate a report for a specific agent."""
    # Extract the score based on agent type
    score_field = get_score_field(agent_name)
    
    # Try to get the score from the specific field first, then fall back to 'score', then to 0
    score = agent_data.get(score_field)
    if score is None or score == "N/A":
        score = agent_data.get('score')
    if score is None or score == "N/A":
        score = 0
    
    # Format the report
    report = [
        f"### Score: {score}/10",
        "\n### Summary",
        agent_data.get('summary', "No summary provided."),
        "\n### Critical Remarks",
        format_critical_remarks(agent_data.get('critical_remarks', [])),
        "\n### Improvement Suggestions",
        format_improvement_suggestions(agent_data.get('improvement_suggestions', [])),
        "\n### Detailed Feedback",
        format_detailed_feedback(agent_data.get('detailed_feedback', {}))
    ]
    
    return "\n".join(report)


def get_agent_type(agent_name: str) -> str:
    """Get the descriptive type of an agent based on its name."""
    agent_types = {
        # Section agents
        "S1": "Title and Keywords",
        "S2": "Abstract",
        "S3": "Introduction",
        "S4": "Literature Review",
        "S5": "Methodology",
        "S6": "Results",
        "S7": "Discussion",
        "S8": "Conclusion",
        "S9": "References",
        "S10": "Supplementary Materials",
        
        # Rigor agents
        "R1": "Originality and Contribution",
        "R2": "Impact and Significance",
        "R3": "Ethics and Compliance",
        "R4": "Data and Code Availability",
        "R5": "Statistical Rigor",
        "R6": "Technical Accuracy",
        "R7": "Consistency",
        
        # Writing agents
        "W1": "Language and Style",
        "W2": "Narrative and Structure",
        "W3": "Clarity and Conciseness",
        "W4": "Terminology Consistency",
        "W5": "Inclusive Language",
        "W6": "Citation Formatting",
        "W7": "Target Audience Alignment",
        "W8": "Visual Presentation"
    }
    
    return agent_types.get(agent_name, "Unknown")


def generate_table_of_contents(data: Dict[str, Any]) -> str:
    """Generate a table of contents with anchor links."""
    toc = [
        "## Table of Contents",
        "- [Overall Assessment](#overall-assessment)",
        "- [Agent Reports](#agent-reports)",
        "  - [Section-Specific Agents (S1-S10)](#section-specific-agents-s1-s10)",
    ]
    
    # Add section agents
    for i in range(1, 11):
        agent_name = f"S{i}"
        if agent_name in data:
            agent_type = get_agent_type(agent_name)
            toc.append(f"    - [{agent_name} - {agent_type}](#s{i}---{agent_type.lower().replace(' ', '-')})")
    
    # Add rigor agents
    toc.append("  - [Rigor Agents (R1-R7)](#rigor-agents-r1-r7)")
    for i in range(1, 8):
        agent_name = f"R{i}"
        if agent_name in data:
            agent_type = get_agent_type(agent_name)
            toc.append(f"    - [{agent_name} - {agent_type}](#r{i}---{agent_type.lower().replace(' ', '-')})")
    
    # Add writing agents
    toc.append("  - [Writing Agents (W1-W8)](#writing-agents-w1-w8)")
    for i in range(1, 9):
        agent_name = f"W{i}"
        if agent_name in data:
            agent_type = get_agent_type(agent_name)
            toc.append(f"    - [{agent_name} - {agent_type}](#w{i}---{agent_type.lower().replace(' ', '-')})")
    
    return "\n".join(toc)


def generate_overall_report(data: Dict[str, Any]) -> str:
    """Generate an overall report summarizing all agent reports."""
    # Calculate average scores
    scores = []
    for agent_name, agent_data in data.items():
        if isinstance(agent_data, dict):
            score_field = get_score_field(agent_name)
            score = agent_data.get(score_field)
            
            # Try specific field first, then generic 'score', then default to 0
            if score is None or not isinstance(score, (int, float)):
                score = agent_data.get('score')
            if score is None or not isinstance(score, (int, float)):
                score = 0
                
            scores.append(score)
    
    avg_score = sum(scores) / len(scores) if scores else 0
    
    # Count total critical remarks and improvement suggestions
    total_critical_remarks = sum(len(agent_data.get('critical_remarks', [])) for agent_data in data.values() if isinstance(agent_data, dict))
    total_improvement_suggestions = sum(len(agent_data.get('improvement_suggestions', [])) for agent_data in data.values() if isinstance(agent_data, dict))
    
    # Generate the overall report
    report = [
        "# Manuscript Review Report",
        f"\nGenerated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "\n## Important Notes",
        "\n> **Version 1.0 (Beta)**: This tool was developed in a short timeframe and may contain hallucinations and errors. Approximately 50% of feedback will likely be unusable, 30% may be mediocre, and 20% should be helpful in highlighting issues that might have been overlooked. Please send feedback to rjakob@ethz.ch so we can continue to improve our agents.",
        "\n> **Model Limitations**: This report was generated using a basic model (ChatGPT 3.5). For more sophisticated analysis, the code is open access and users can run more advanced models (such as GPT-4) with their own API keys. Visit [https://github.com/robertjakob/rigorous](https://github.com/robertjakob/rigorous) for more information.",
        "\n> **Development Status**: This tool is still in testing mode with many agents in their first iteration. We welcome contributions to build the best review agent team to improve the quality of scientific publishing. Join us at [https://github.com/robertjakob/rigorous](https://github.com/robertjakob/rigorous).",
        "\n",
        generate_table_of_contents(data),
        "\n## Overall Assessment",
        f"\nThe manuscript received an average score of {avg_score:.2f}/10 across all evaluation criteria.",
        f"A total of {total_critical_remarks} critical remarks and {total_improvement_suggestions} improvement suggestions were identified.",
        "\n## Agent Reports",
        "\n### Section-Specific Agents (S1-S10)",
    ]
    
    # Add section agent reports
    for i in range(1, 11):
        agent_name = f"S{i}"
        if agent_name in data and isinstance(data[agent_name], dict):
            agent_type = get_agent_type(agent_name)
            report.append(f"\n## {agent_name} - {agent_type}")
            report.append(generate_agent_report(agent_name, data[agent_name]))
    
    # Add rigor agent reports
    report.append("\n### Rigor Agents (R1-R7)")
    for i in range(1, 8):
        agent_name = f"R{i}"
        if agent_name in data and isinstance(data[agent_name], dict):
            agent_type = get_agent_type(agent_name)
            report.append(f"\n## {agent_name} - {agent_type}")
            report.append(generate_agent_report(agent_name, data[agent_name]))
    
    # Add writing agent reports
    report.append("\n### Writing Agents (W1-W8)")
    for i in range(1, 9):
        agent_name = f"W{i}"
        if agent_name in data and isinstance(data[agent_name], dict):
            agent_type = get_agent_type(agent_name)
            report.append(f"\n## {agent_name} - {agent_type}")
            report.append(generate_agent_report(agent_name, data[agent_name]))
    
    return "\n".join(report)


def save_report(report: str, output_path: str) -> None:
    """Save the report to a file."""
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(report)
        print(f"Report successfully saved to {output_path}")
    except Exception as e:
        print(f"Error saving report: {e}")


def main():
    """Main function to run the script."""
    parser = argparse.ArgumentParser(description='Convert JSON results to a text report')
    parser.add_argument('--input', '-i', type=str, 
                        default='/Users/robertjakob/rigorous-1/V5_multi_agent2/results/combined_results.json',
                        help='Path to the input JSON file')
    parser.add_argument('--output', '-o', type=str,
                        default='/Users/robertjakob/rigorous-1/V5_multi_agent2/results/manuscript_report.md',
                        help='Path to save the output report')
    
    args = parser.parse_args()
    
    # Load the JSON data
    data = load_json_file(args.input)
    if not data:
        print("Failed to load JSON data. Exiting.")
        return
    
    # Generate the report
    report = generate_overall_report(data)
    
    # Save the report
    save_report(report, args.output)


if __name__ == "__main__":
    main() 