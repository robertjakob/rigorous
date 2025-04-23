#!/usr/bin/env python3
"""
Run Analysis Script

This script runs the analysis using the controller agent and generates a consistent report.
"""

import os
import json
import argparse
from datetime import datetime
from typing import Dict, Any, List

from reviewer_agents.controller_agent import ControllerAgent
from utils.pdf_parser import PDFParser
from utils.json_to_report import generate_overall_report, save_report


def load_manuscript(file_path: str) -> str:
    """Load the manuscript text from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error loading manuscript: {e}")
        return ""


def save_results(results: Dict[str, Any], output_path: str) -> None:
    """Save the analysis results to a JSON file."""
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(results, file, indent=2)
        print(f"Results successfully saved to {output_path}")
    except Exception as e:
        print(f"Error saving results: {e}")


def main():
    """Main function to run the analysis and generate the report."""
    parser = argparse.ArgumentParser(description='Run analysis and generate a consistent report')
    parser.add_argument('--input', '-i', type=str, 
                        default='/Users/robertjakob/rigorous-1/V5_multi_agent2/data/manuscript.txt',
                        help='Path to the input manuscript file')
    parser.add_argument('--results', '-r', type=str,
                        default='/Users/robertjakob/rigorous-1/V5_multi_agent2/results/combined_results.json',
                        help='Path to save the analysis results')
    parser.add_argument('--output', '-o', type=str,
                        default='/Users/robertjakob/rigorous-1/V5_multi_agent2/results/manuscript_report.md',
                        help='Path to save the output report')
    parser.add_argument('--model', '-m', type=str,
                        default='gpt-4',
                        help='Model to use for analysis')
    
    args = parser.parse_args()
    
    # Load the manuscript
    manuscript_text = load_manuscript(args.input)
    if not manuscript_text:
        print("Failed to load manuscript. Exiting.")
        return
    
    # Initialize the controller agent
    controller = ControllerAgent(model=args.model)
    
    # Run the analysis
    print("Running analysis...")
    results = controller.run_analysis(manuscript_text)
    
    # Save the results
    save_results(results, args.results)
    
    # Generate the report
    print("Generating report...")
    report = generate_overall_report(results)
    
    # Save the report
    save_report(report, args.output)
    
    print(f"Analysis complete. Report saved to {args.output}")


if __name__ == "__main__":
    main() 