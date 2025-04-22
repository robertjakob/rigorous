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
            f"{i}. Category: {remark.get('category', 'N/A')}\n"
            f"   Location: {remark.get('location', 'N/A')}\n"
            f"   Issue: {remark.get('issue', 'N/A')}\n"
            f"   Severity: {remark.get('severity', 'N/A')}\n"
            f"   Impact: {remark.get('impact', 'N/A')}"
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
            f"{i}. Location: {suggestion.get('location', 'N/A')}\n"
            f"   Category: {suggestion.get('category', 'N/A')}\n"
            f"   Focus: {suggestion.get('focus', 'N/A')}\n"
            f"   Original Text: {suggestion.get('original_text', 'N/A')}\n"
            f"   Improved Version: {suggestion.get('improved_version', 'N/A')}\n"
            f"   Explanation: {suggestion.get('explanation', 'N/A')}"
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
        formatted_feedback.append(f"{category_title}:\n{content}")
    
    return "\n\n".join(formatted_feedback)


def generate_agent_report(agent_name: str, agent_data: Dict[str, Any]) -> str:
    """Generate a report for a specific agent."""
    # Extract the score based on agent type
    score_key = None
    for key in agent_data.keys():
        if key.endswith('_score'):
            score_key = key
            break
    
    score = agent_data.get(score_key, "N/A")
    score_name = score_key.replace('_score', '').replace('_', ' ').title() if score_key else "Overall"
    
    # Format the report
    report = [
        f"# {agent_name} Report",
        f"\n## {score_name} Score: {score}/10",
        "\n## Summary",
        agent_data.get('summary', "No summary provided."),
        "\n## Critical Remarks",
        format_critical_remarks(agent_data.get('critical_remarks', [])),
        "\n## Improvement Suggestions",
        format_improvement_suggestions(agent_data.get('improvement_suggestions', [])),
        "\n## Detailed Feedback",
        format_detailed_feedback(agent_data.get('detailed_feedback', {}))
    ]
    
    return "\n".join(report)


def generate_overall_report(data: Dict[str, Any]) -> str:
    """Generate an overall report summarizing all agent reports."""
    # Calculate average scores
    scores = []
    for agent_name, agent_data in data.items():
        for key, value in agent_data.items():
            if key.endswith('_score') and isinstance(value, (int, float)):
                scores.append(value)
    
    avg_score = sum(scores) / len(scores) if scores else 0
    
    # Count total critical remarks and improvement suggestions
    total_critical_remarks = sum(len(agent_data.get('critical_remarks', [])) for agent_data in data.values())
    total_improvement_suggestions = sum(len(agent_data.get('improvement_suggestions', [])) for agent_data in data.values())
    
    # Generate the overall report
    report = [
        "# Manuscript Review Report",
        f"\nGenerated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"\n## Overall Assessment",
        f"\nThe manuscript received an average score of {avg_score:.2f}/10 across all evaluation criteria.",
        f"A total of {total_critical_remarks} critical remarks and {total_improvement_suggestions} improvement suggestions were identified.",
        "\n## Agent Reports",
    ]
    
    # Add individual agent reports
    for agent_name, agent_data in data.items():
        report.append(f"\n\n{generate_agent_report(agent_name, agent_data)}")
    
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